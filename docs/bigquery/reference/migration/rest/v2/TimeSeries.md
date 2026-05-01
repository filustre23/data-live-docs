* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# TimeSeries Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [Point](#Point)
  + [JSON representation](#Point.SCHEMA_REPRESENTATION)
* [TimeInterval](#TimeInterval)
  + [JSON representation](#TimeInterval.SCHEMA_REPRESENTATION)
* [TypedValue](#TypedValue)
  + [JSON representation](#TypedValue.SCHEMA_REPRESENTATION)

The metrics object for a SubTask.

| JSON representation |
| --- |
| ``` {   "metric": string,   "valueType": enum (ValueType),   "metricKind": enum (MetricKind),   "points": [     {       object (Point)     }   ] } ``` |

| Fields | |
| --- | --- |
| `metric` | `string`  Required. The name of the metric.  If the metric is not known by the service yet, it will be auto-created. |
| `valueType` | `enum (ValueType)`  Required. The value type of the time series. |
| `metricKind` | `enum (MetricKind)`  Optional. The metric kind of the time series.  If present, it must be the same as the metric kind of the associated metric. If the associated metric's descriptor must be auto-created, then this field specifies the metric kind of the new descriptor and must be either `GAUGE` (the default) or `CUMULATIVE`. |
| `points[]` | `object (Point)`  Required. The data points of this time series. When listing time series, points are returned in reverse time order.  When creating a time series, this field must contain exactly one point and the point's type must be the same as the value type of the associated metric. If the associated metric's descriptor must be auto-created, then the value type of the descriptor is determined by the point's type, which must be `BOOL`, `INT64`, `DOUBLE`, or `DISTRIBUTION`. |

## Point

A single data point in a time series.

| JSON representation |
| --- |
| ``` {   "interval": {     object (TimeInterval)   },   "value": {     object (TypedValue)   } } ``` |

| Fields | |
| --- | --- |
| `interval` | `object (TimeInterval)`  The time interval to which the data point applies. For `GAUGE` metrics, the start time does not need to be supplied, but if it is supplied, it must equal the end time. For `DELTA` metrics, the start and end time should specify a non-zero interval, with subsequent points specifying contiguous and non-overlapping intervals. For `CUMULATIVE` metrics, the start and end time should specify a non-zero interval, with subsequent points specifying the same start time and increasing end times, until an event resets the cumulative value to zero and sets a new start time for the following points. |
| `value` | `object (TypedValue)`  The value of the data point. |

## TimeInterval

A time interval extending just after a start time through an end time. If the start time is the same as the end time, then the interval represents a single point in time.

| JSON representation |
| --- |
| ``` {   "startTime": string,   "endTime": string } ``` |

| Fields | |
| --- | --- |
| `startTime` | `string (Timestamp format)`  Optional. The beginning of the time interval. The default value for the start time is the end time. The start time must not be later than the end time. |
| `endTime` | `string (Timestamp format)`  Required. The end of the time interval. |

## TypedValue

A single strongly-typed value.

| JSON representation |
| --- |
| ``` {    // Union field value can be only one of the following:   "boolValue": boolean,   "int64Value": string,   "doubleValue": number,   "stringValue": string,   "distributionValue": {     object (Distribution)   }   // End of list of possible types for union field value. } ``` |

| Fields | |
| --- | --- |
| Union field `value`. The typed value field. `value` can be only one of the following: | |
| `boolValue` | `boolean`  A Boolean value: `true` or `false`. |
| `int64Value` | `string (int64 format)`  A 64-bit integer. Its range is approximately `+/-9.2x10^18`. |
| `doubleValue` | `number`  A 64-bit double-precision floating-point number. Its magnitude is approximately `+/-10^(+/-300)` and it has 16 significant digits of precision. |
| `stringValue` | `string`  A variable-length string value. |
| `distributionValue` | `object (Distribution)`  A distribution value. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]