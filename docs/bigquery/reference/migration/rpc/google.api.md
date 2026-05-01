* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Package google.api Stay organized with collections Save and categorize content based on your preferences.

## Index

* `Distribution` (message)
* `Distribution.BucketOptions` (message)
* `Distribution.BucketOptions.Explicit` (message)
* `Distribution.BucketOptions.Exponential` (message)
* `Distribution.BucketOptions.Linear` (message)
* `Distribution.Exemplar` (message)
* `Distribution.Range` (message)
* `MetricDescriptor` (message)
* `MetricDescriptor.MetricKind` (enum)
* `MetricDescriptor.ValueType` (enum)

## Distribution

`Distribution` contains summary statistics for a population of values. It optionally contains a histogram representing the distribution of those values across a set of buckets.

The summary statistics are the count, mean, sum of the squared deviation from the mean, the minimum, and the maximum of the set of population of values. The histogram is based on a sequence of buckets and gives a count of values that fall into each bucket. The boundaries of the buckets are given either explicitly or by formulas for buckets of fixed or exponentially increasing widths.

Although it is not forbidden, it is generally a bad idea to include non-finite values (infinities or NaNs) in the population of values, as this will render the `mean` and `sum_of_squared_deviation` fields meaningless.

| Fields | |
| --- | --- |
| `count` | `int64`  The number of values in the population. Must be non-negative. This value must equal the sum of the values in `bucket_counts` if a histogram is provided. |
| `mean` | `double`  The arithmetic mean of the values in the population. If `count` is zero then this field must be zero. |
| `sum_of_squared_deviation` | `double`  The sum of squared deviations from the mean of the values in the population. For values x\_i this is:     ``` Sum[i=1..n]((x_i - mean)^2) ```   Knuth, "The Art of Computer Programming", Vol. 2, page 232, 3rd edition describes Welford's method for accumulating this sum in one pass.  If `count` is zero then this field must be zero. |
| `range` | `Range`  If specified, contains the range of the population values. The field must not be present if the `count` is zero. |
| `bucket_options` | `BucketOptions`  Defines the histogram bucket boundaries. If the distribution does not contain a histogram, then omit this field. |
| `bucket_counts[]` | `int64`  The number of values in each bucket of the histogram, as described in `bucket_options`. If the distribution does not have a histogram, then omit this field. If there is a histogram, then the sum of the values in `bucket_counts` must equal the value in the `count` field of the distribution.  If present, `bucket_counts` should contain N values, where N is the number of buckets specified in `bucket_options`. If you supply fewer than N values, the remaining values are assumed to be 0.  The order of the values in `bucket_counts` follows the bucket numbering schemes described for the three bucket types. The first value must be the count for the underflow bucket (number 0). The next N-2 values are the counts for the finite buckets (number 1 through N-2). The N'th value in `bucket_counts` is the count for the overflow bucket (number N-1). |
| `exemplars[]` | `Exemplar`  Must be in increasing order of `value` field. |

## BucketOptions

`BucketOptions` describes the bucket boundaries used to create a histogram for the distribution. The buckets can be in a linear sequence, an exponential sequence, or each bucket can be specified explicitly. `BucketOptions` does not include the number of values in each bucket.

A bucket has an inclusive lower bound and exclusive upper bound for the values that are counted for that bucket. The upper bound of a bucket must be strictly greater than the lower bound. The sequence of N buckets for a distribution consists of an underflow bucket (number 0), zero or more finite buckets (number 1 through N - 2) and an overflow bucket (number N - 1). The buckets are contiguous: the lower bound of bucket i (i > 0) is the same as the upper bound of bucket i - 1. The buckets span the whole range of finite values: lower bound of the underflow bucket is -infinity and the upper bound of the overflow bucket is +infinity. The finite buckets are so-called because both bounds are finite.

| Fields | |
| --- | --- |
| Union field `options`. Exactly one of these three fields must be set. `options` can be only one of the following: | |
| `linear_buckets` | `Linear`  The linear bucket. |
| `exponential_buckets` | `Exponential`  The exponential buckets. |
| `explicit_buckets` | `Explicit`  The explicit buckets. |

## Explicit

Specifies a set of buckets with arbitrary widths.

There are `size(bounds) + 1` (= N) buckets. Bucket `i` has the following boundaries:

Upper bound (0 <= i < N-1): bounds[i] Lower bound (1 <= i < N); bounds[i - 1]

The `bounds` field must contain at least one element. If `bounds` has only one element, then there are no finite buckets, and that single element is the common boundary of the overflow and underflow buckets.

| Fields | |
| --- | --- |
| `bounds[]` | `double`  The values must be monotonically increasing. |

## Exponential

Specifies an exponential sequence of buckets that have a width that is proportional to the value of the lower bound. Each bucket represents a constant relative uncertainty on a specific value in the bucket.

There are `num_finite_buckets + 2` (= N) buckets. Bucket `i` has the following boundaries:

Upper bound (0 <= i < N-1): scale \* (growth\_factor ^ i).

Lower bound (1 <= i < N): scale \* (growth\_factor ^ (i - 1)).

| Fields | |
| --- | --- |
| `num_finite_buckets` | `int32`  Must be greater than 0. |
| `growth_factor` | `double`  Must be greater than 1. |
| `scale` | `double`  Must be greater than 0. |

## Linear

Specifies a linear sequence of buckets that all have the same width (except overflow and underflow). Each bucket represents a constant absolute uncertainty on the specific value in the bucket.

There are `num_finite_buckets + 2` (= N) buckets. Bucket `i` has the following boundaries:

Upper bound (0 <= i < N-1): offset + (width \* i).

Lower bound (1 <= i < N): offset + (width \* (i - 1)).

| Fields | |
| --- | --- |
| `num_finite_buckets` | `int32`  Must be greater than 0. |
| `width` | `double`  Must be greater than 0. |
| `offset` | `double`  Lower bound of the first bucket. |

## Exemplar

Exemplars are example points that may be used to annotate aggregated distribution values. They are metadata that gives information about a particular value added to a Distribution bucket, such as a trace ID that was active when a value was added. They may contain further information, such as a example values and timestamps, origin, etc.

| Fields | |
| --- | --- |
| `value` | `double`  Value of the exemplar point. This value determines to which bucket the exemplar belongs. |
| `timestamp` | `Timestamp`  The observation (sampling) time of the above value. |
| `attachments[]` | `Any`  Contextual information about the example value. Examples are:  Trace: type.googleapis.com/google.monitoring.v3.SpanContext  Literal string: type.googleapis.com/google.protobuf.StringValue  Labels dropped during aggregation: type.googleapis.com/google.monitoring.v3.DroppedLabels  There may be only a single attachment of any given message type in a single exemplar, and this is enforced by the system. |

## Range

The range of the population values.

| Fields | |
| --- | --- |
| `min` | `double`  The minimum of the population values. |
| `max` | `double`  The maximum of the population values. |

## MetricDescriptor

This type has no fields.

Defines a metric type and its schema. Once a metric descriptor is created, deleting or altering it stops data collection and makes the metric type's existing data unusable.

## MetricKind

The kind of measurement. It describes how the data is reported. For information on setting the start time and end time based on the MetricKind, see [TimeInterval][google.monitoring.v3.TimeInterval].

| Enums | |
| --- | --- |
| `METRIC_KIND_UNSPECIFIED` | Do not use this default value. |
| `GAUGE` | An instantaneous measurement of a value. |
| `DELTA` | The change in a value during a time interval. |
| `CUMULATIVE` | A value accumulated over a time interval. Cumulative measurements in a time series should have the same start time and increasing end times, until an event resets the cumulative value to zero and sets a new start time for the following points. |

## ValueType

The value type of a metric.

| Enums | |
| --- | --- |
| `VALUE_TYPE_UNSPECIFIED` | Do not use this default value. |
| `BOOL` | The value is a boolean. This value type can be used only if the metric kind is `GAUGE`. |
| `INT64` | The value is a signed 64-bit integer. |
| `DOUBLE` | The value is a double precision floating point number. |
| `STRING` | The value is a text string. This value type can be used only if the metric kind is `GAUGE`. |
| `DISTRIBUTION` | The value is a `Distribution`. |
| `MONEY` | The value is money. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]