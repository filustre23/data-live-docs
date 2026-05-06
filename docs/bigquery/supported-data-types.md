* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 支持的协议缓冲区和 Arrow 数据类型

本文档介绍了每种 BigQuery 数据类型支持的协议缓冲区和 Arrow 数据类型。在阅读本文档之前，请先阅读 [BigQuery Storage Write API 概览](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-cn#overview)。

## 支持的协议缓冲区数据类型

下表显示了协议缓冲区中支持的数据类型以及 BigQuery 中对应的输入格式：

| BigQuery 数据类型 | 支持的协议缓冲区类型 |
| --- | --- |
| `BOOL` | `bool`、`int32`、`int64`、`uint32`、`uint64`、`google.protobuf.BoolValue` |
| `BYTES` | `bytes`、`string`、`google.protobuf.BytesValue` |
| `DATE` | `int32`（首选）、`int64`、`string` 该值是自 Unix 纪元（1970-01-01）开始计算的天数。有效范围在 `-719162` (0001-01-01) 至 `2932896` (9999-12-31) 之间。 |
| `DATETIME`、`TIME` | `string` 该值必须是 [`DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-cn#datetime_literals) 或 [`TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-cn#time_literals) 字面量。 |
| `int64` 使用 [`CivilTimeEncoder` 类](https://github.com/googleapis/java-bigquerystorage/blob/main/google-cloud-bigquerystorage/src/main/java/com/google/cloud/bigquery/storage/v1/CivilTimeEncoder.java)执行转换。 |
| `FLOAT` | `double`、`float`、`google.protobuf.DoubleValue`、`google.protobuf.FloatValue` |
| `GEOGRAPHY` | `string` 该值是 WKT 或 GeoJson 格式的几何图形。 |
| `INTEGER` | `int32`、`int64`、`uint32`、`enum`、`google.protobuf.Int32Value`、`google.protobuf.Int64Value`、`google.protobuf.UInt32Value` |
| `JSON` | `string` |
| `NUMERIC`、`BIGNUMERIC` | `int32`、`int64`、`uint32`、`uint64`、`double`、`float`、`string` |
| `bytes`、`google.protobuf.BytesValue` 使用 [`BigDecimalByteStringEncoder` 类](https://github.com/googleapis/java-bigquerystorage/blob/main/google-cloud-bigquerystorage/src/main/java/com/google/cloud/bigquery/storage/v1/BigDecimalByteStringEncoder.java)执行转换。 |
| `STRING` | `string`、`enum`、`google.protobuf.StringValue` |
| `TIME` | `string` 该值必须是 [`TIME` 字面量](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-cn#time_literals)。 |
| `TIMESTAMP` | `int64`（首选）、`int32`、`uint32`、`google.protobuf.Timestamp` 该值是自 Unix 计时原点（1970-01-01）开始计算的毫秒数。 |
| `INTERVAL` | `string`, `google.protobuf.Duration` 字符串值必须是 [`INTERVAL` 字面量](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-cn#interval_literals)。 |
| `RANGE<T>` | `message` proto 中包含两个字段（`start` 和 `end`）的嵌套消息类型，这两个字段必须采用与 BigQuery 数据类型 `T` 对应的相同受支持协议缓冲区类型。`T` 必须是 `DATE`、`DATETIME` 或 `TIMESTAMP` 中的一个。如果某个字段（`start` 或 `end`）未在 proto 消息中进行设置，它表示无界限边界。在以下示例中，`f_range_date` 表示表中的 `RANGE` 列。由于 `end` 字段未在 proto 消息中进行设置，因此此范围的结束边界是无界限的。     ``` {   f_range_date: {     start: 1   } } ``` |
| `REPEATED FIELD` | `array` proto 中的数组类型对应于 BigQuery 中的重复字段。 |
| `RECORD` | `message` proto 中的嵌套消息类型对应于 BigQuery 中的记录字段。 |

## 支持的 Apache Arrow 数据类型

下表显示了 Apache Arrow 中支持的数据类型以及 BigQuery 中对应的输入格式。

| BigQuery 数据类型 | 支持的 Apache Arrow 类型 | 支持的类型参数 |
| --- | --- | --- |
| `BOOL` | `Boolean` |  |
| `BYTES` | `Binary` |  |
| `DATE` | `Date` | unit = Day |
| `String`、`int32` |  |
| `DATETIME` | `Timestamp` | unit = MICROSECONDS timezone 为空 |
| `FLOAT` | `FloatingPoint` | {SINGLE, DOUBLE} 中的精度 |
| `GEOGRAPHY` | `Utf8` 该值是 WKT 或 GeoJson 格式的几何图形。 |  |
| `INTEGER` | `int` | {8, 16, 32, 64} 中的位宽度 is\_signed = false |
| `JSON` | `Utf8` |  |
| `NUMERIC` | `Decimal128` | 您可以提供具有小于 [BigQuery 支持的范围](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-cn#decimal_types)的任何精度或标度的 NUMERIC。 |
| `BIGNUMERIC` | `Decimal256` | 您可以提供具有小于 [BigQuery 支持的范围](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-cn#decimal_types)的任何精度或标度的 BIGNUMERIC。 |
| `STRING` | `Utf8` |  |
| `TIMESTAMP` | `Timestamp` | unit = MICROSECONDS timezone = UTC |
| `INTERVAL` | `Interval` | {YEAR\_MONTH, DAY\_TIME, MONTH\_DAY\_NANO} 中的单位 |
| `Utf8` |  |
| `RANGE<T>` | `Struct` Arrow 结构体必须具有两个名为 `start` 和 `end` 的子字段。  对于 `RANGE<DATE>` 列，字段必须是 Arrow 类型 `Date`，且 `unit=Day`。  对于 `RANGE<DATETIME>` 列，字段必须是 Arrow 类型 `Timestamp`，且 `unit=MICROSECONDS`，但不含时区。  对于 `RANGE<TIMESTAMP>`，字段必须是 Arrow 类型 `Timestamp`，且 `unit=MICROSECONDS`、`timezone=UTC`。  任何 `start` 和 `end` 字段中的 `NULL` 值都将被视为 `UNBOUNDED`。 |  |
| `REPEATED FIELD` | `List` | `NULL` 值必须以空列表来表示。 |
| `RECORD` | `Struct` |  |




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-05-06。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-05-06。"],[],[]]