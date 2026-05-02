* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Table functions (built in) Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports built-in table functions.

This topic includes functions that produce columns of a table.
You can only use these functions in the `FROM` clause.

## Function list

| Name | Summary |
| --- | --- |
| [`APPENDS`](/bigquery/docs/reference/standard-sql/time-series-functions#appends) | Returns all rows appended to a table for a given time range.  For more information, see [Time series functions](/bigquery/docs/reference/standard-sql/time-series-functions). |
| [`CHANGES`](/bigquery/docs/reference/standard-sql/time-series-functions#changes) | Returns all rows that have changed in a table for a given time range.  For more information, see [Time series functions](/bigquery/docs/reference/standard-sql/time-series-functions). |
| [`EXTERNAL_OBJECT_TRANSFORM`](/bigquery/docs/reference/standard-sql/table-functions-built-in#external_object_transform) | Produces an object table with the original columns plus one or more additional columns. |
| [`GAP_FILL`](/bigquery/docs/reference/standard-sql/time-series-functions#gap_fill) | Finds and fills gaps in a time series.  For more information, see [Time series functions](/bigquery/docs/reference/standard-sql/time-series-functions). |
| [`RANGE_SESSIONIZE`](/bigquery/docs/reference/standard-sql/range-functions#range_sessionize) | Produces a table of sessionized ranges.  For more information, see [Range functions](/bigquery/docs/reference/standard-sql/range-functions). |

## `EXTERNAL_OBJECT_TRANSFORM`

```
EXTERNAL_OBJECT_TRANSFORM(TABLE object_table_name, transform_types_array)
```

**Description**

This function returns a transformed object table with the original columns plus
one or more additional columns, depending on the `transform_types` values
specified.

This function only supports
[object tables](https://cloud.google.com/bigquery/docs/object-table-introduction)
as inputs. Subqueries or any other types of tables aren't supported.

`object_table_name` is the name of the object table to be transformed, in
the format `dataset_name.object_table_name`.

`transform_types_array` is an array of `STRING` literals. Currently, the only
supported `transform_types_array` value is `SIGNED_URL`. Specifying `SIGNED_URL`
creates read-only signed URLs for the objects in the identified object table,
which are returned in a `signed_url` column. Generated signed URLs are
valid for 6 hours.

**Return Type**

TABLE

**Example**

Run the following query to return URIs and signed URLs for the objects in the
`mydataset.myobjecttable` object table.

```
SELECT uri, signed_url
FROM EXTERNAL_OBJECT_TRANSFORM(TABLE mydataset.myobjecttable, ['SIGNED_URL']);

--The preceding statement returns results similar to the following:
/*-----------------------------------------------------------------------------------------------------------------------------+
 |  uri                                 | signed_url                                                                           |
 +-----------------------------------------------------------------------------------------------------------------------------+
 | gs://myobjecttable/1234_Main_St.jpeg | https://storage.googleapis.com/mybucket/1234_Main_St.jpeg?X-Goog-Algorithm=1234abcd… |
 +-----------------------------------------------------------------------------------------------------------------------------+
 | gs://myobjecttable/345_River_Rd.jpeg | https://storage.googleapis.com/mybucket/345_River_Rd.jpeg?X-Goog-Algorithm=2345bcde… |
 +-----------------------------------------------------------------------------------------------------------------------------*/
```




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-01 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-01 UTC."],[],[]]