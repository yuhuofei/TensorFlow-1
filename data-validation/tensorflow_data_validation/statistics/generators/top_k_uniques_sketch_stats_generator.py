# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module that estimates top-k and unique statistics for categorical features.

Uses the Misra-Gries sketch to estimate top unweighted item counts and weighted
(if provided) item counts and the K-Minimum Values sketch to estimate number of
unique items.
"""

from __future__ import absolute_import
from __future__ import division

from __future__ import print_function

import collections
from typing import Dict, Iterable, Optional, Text

import numpy as np
import pyarrow as pa
from tensorflow_data_validation import types as tfdv_types
from tensorflow_data_validation.arrow import arrow_util
from tensorflow_data_validation.statistics.generators import stats_generator
from tensorflow_data_validation.utils import schema_util
from tensorflow_data_validation.utils import stats_util
from tensorflow_data_validation.utils import top_k_uniques_stats_util

from tfx_bsl.sketches import KmvSketch
from tfx_bsl.sketches import MisraGriesSketch

from tensorflow_metadata.proto.v0 import schema_pb2
from tensorflow_metadata.proto.v0 import statistics_pb2

# Tuple for containing estimates from querying a _CombinedSketch.
_CombinedEstimate = collections.namedtuple(
    "_CombinedEstimate", ["distinct", "topk_unweighted", "topk_weighted"])


class _CombinedSketch(object):
  """Wrapper for the three sketches for a single feature."""
  __slots__ = ["_distinct", "_topk_unweighted", "_topk_weighted"]

  def __init__(self, distinct, topk_unweighted, topk_weighted=None):
    self._distinct = distinct
    self._topk_unweighted = topk_unweighted
    self._topk_weighted = topk_weighted

  def add(self, values, weights=None):
    self._distinct.AddValues(values)
    self._topk_unweighted.AddValues(values)
    if weights is not None:
      self._topk_weighted.AddValues(values, weights)

  def merge(self, other_sketch):
    # pylint: disable=protected-access
    self._distinct.Merge(other_sketch._distinct)
    self._topk_unweighted.Merge(other_sketch._topk_unweighted)
    self._topk_weighted.Merge(other_sketch._topk_weighted)
    # pylint: enable=protected-access

  def estimate(self):
    # Converts the result struct array into list of FeatureValueCounts.
    topk_unweighted = self._topk_unweighted.Estimate().to_pylist()
    topk_unweighted_counts = [top_k_uniques_stats_util.FeatureValueCount(
        pair["values"], pair["counts"]) for pair in topk_unweighted]
    topk_weighted = self._topk_weighted.Estimate().to_pylist()
    topk_weighted_counts = [top_k_uniques_stats_util.FeatureValueCount(
        pair["values"], pair["counts"]) for pair in topk_weighted]
    return _CombinedEstimate(
        self._distinct.Estimate(), topk_unweighted_counts, topk_weighted_counts)


class TopKUniquesSketchStatsGenerator(stats_generator.CombinerStatsGenerator):
  """Generates statistics for number unique and top-k item counts.

  Uses mergeable K-Minimum Values (KMV) and Misra-Gries sketches to estimate
  statistics.
  """

  def __init__(
      self,
      name: Text = "TopKUniquesSketchStatsGenerator",
      schema: Optional[schema_pb2.Schema] = None,
      weight_feature: Optional[tfdv_types.FeatureName] = None,
      num_top_values: int = 2,
      num_rank_histogram_buckets: int = 128,
      frequency_threshold: int = 1,
      weighted_frequency_threshold: float = 1.0,
      num_misragries_buckets: int = 128,
      num_kmv_buckets: int = 128
  ):
    """Initializes a top-k and uniques sketch combiner statistics generator.

    Args:
      name: An optional unique name associated with the statistics generator.
      schema: An optional schema for the dataset.
      weight_feature: Feature name whose numeric value represents the weight of
        an example. None if there is no weight feature.
      num_top_values: The number of most frequent feature values to keep for
        string features.
      num_rank_histogram_buckets: The number of buckets in the rank histogram
        for string features.
      frequency_threshold: An optional minimum number of examples the most
        frequent values must be present in (defaults to 1).
      weighted_frequency_threshold: An optional minimum weighted number of
        examples the most frequent weighted values must be present in (defaults
        to 1.0).
      num_misragries_buckets: Number of buckets to use for MisraGries sketch.
      num_kmv_buckets: Number of buckets to use for KMV sketch.

    """
    super(
        TopKUniquesSketchStatsGenerator,
        self,
    ).__init__(name, schema)
    self._num_misragries_buckets = num_misragries_buckets
    self._num_kmv_buckets = num_kmv_buckets
    self._num_top_values = num_top_values
    self._weight_feature = weight_feature
    self._num_rank_histogram_buckets = num_rank_histogram_buckets
    self._categorical_features = set(
        schema_util.get_categorical_numeric_features(schema) if schema else [])
    self._frequency_threshold = frequency_threshold
    self._weighted_frequency_threshold = weighted_frequency_threshold

  def _update_combined_sketch_for_feature(
      self, feature_name: tfdv_types.FeaturePath, values: pa.Array,
      weights: Optional[np.ndarray],
      accumulator: Dict[tfdv_types.FeaturePath, _CombinedSketch]):
    """Updates combined sketch with values (and weights if provided)."""
    flattened_values, parent_indices = arrow_util.flatten_nested(
        values, weights is not None)

    combined_sketch = accumulator.get(feature_name, None)
    if combined_sketch is None:
      combined_sketch = _CombinedSketch(
          distinct=KmvSketch(self._num_kmv_buckets),
          topk_unweighted=MisraGriesSketch(self._num_misragries_buckets),
          topk_weighted=MisraGriesSketch(self._num_misragries_buckets),
      )
    weight_array = None
    if weights is not None:
      flattened_weights = weights[parent_indices]
      weight_array = pa.array(flattened_weights, type=pa.float32())
    combined_sketch.add(flattened_values, weight_array)
    accumulator[feature_name] = combined_sketch

  def create_accumulator(self) -> Dict[tfdv_types.FeaturePath, _CombinedSketch]:
    return {}

  def add_input(
      self, accumulator: Dict[tfdv_types.FeaturePath, _CombinedSketch],
      input_record_batch: pa.RecordBatch
      ) -> Dict[tfdv_types.FeaturePath, _CombinedSketch]:
    for feature_path, leaf_array, weights in arrow_util.enumerate_arrays(
        input_record_batch,
        weight_column=self._weight_feature,
        enumerate_leaves_only=True):
      feature_type = stats_util.get_feature_type_from_arrow_type(
          feature_path, leaf_array.type)
      # Only compute top-k and unique stats for categorical and string features.
      if (feature_path in self._categorical_features or
          feature_type == statistics_pb2.FeatureNameStatistics.STRING):
        self._update_combined_sketch_for_feature(
            feature_path, leaf_array, weights, accumulator)
    return accumulator

  def merge_accumulators(
      self,
      accumulators: Iterable[Dict[tfdv_types.FeaturePath, _CombinedSketch]]
      ) -> Dict[tfdv_types.FeaturePath, _CombinedSketch]:
    result = {}
    for accumulator in accumulators:
      for feature_name, combined_sketch in accumulator.items():
        existing_sketch = result.get(feature_name, None)
        if existing_sketch is None:
          result[feature_name] = combined_sketch
        else:
          existing_sketch.merge(combined_sketch)
          result[feature_name] = existing_sketch
    return result

  def extract_output(
      self, accumulator: Dict[tfdv_types.FeaturePath, _CombinedSketch]
  ) -> statistics_pb2.DatasetFeatureStatistics:
    result = statistics_pb2.DatasetFeatureStatistics()
    for feature_path, combined_sketch in accumulator.items():
      combined_estimate = combined_sketch.estimate()
      if not combined_estimate.topk_unweighted:
        assert not combined_estimate.topk_weighted
        continue
      feature_stats_proto = (
          top_k_uniques_stats_util.make_feature_stats_proto_topk_uniques(
              feature_path=feature_path,
              is_categorical=feature_path in self._categorical_features,
              frequency_threshold=self._frequency_threshold,
              weighted_frequency_threshold=self._weighted_frequency_threshold,
              num_top_values=self._num_top_values,
              num_rank_histogram_buckets=self._num_rank_histogram_buckets,
              num_unique=combined_estimate.distinct,
              value_count_list=combined_estimate.topk_unweighted,
              weighted_value_count_list=combined_estimate.topk_weighted))

      new_feature_stats_proto = result.features.add()
      new_feature_stats_proto.CopyFrom(feature_stats_proto)
    return result
