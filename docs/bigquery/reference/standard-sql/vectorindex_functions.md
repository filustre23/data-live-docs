* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Vector index functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following vector index functions.

## Function list

| Name | Summary |
| --- | --- |
| [`VECTOR_INDEX.STATISTICS`](/bigquery/docs/reference/standard-sql/vectorindex_functions#vector_indexstatistics) | Calculate how much an indexed table's data has drifted between when a vector index was trained and the present. |

## `VECTOR_INDEX.STATISTICS`

```
VECTOR_INDEX.STATISTICS(
  TABLE table_name
)
```

**Description**

The `VECTOR_INDEX.STATISTICS` function calculates how much an indexed table's
data has drifted between when a [vector index](/bigquery/docs/vector-index) was trained and the
present. Use this function to determine if table data has changed enough to
require a vector index rebuild. If necessary, you can use the
[`ALTER VECTOR INDEX REBUILD` statement](/bigquery/docs/reference/standard-sql/data-definition-language#alter_vector_index_rebuild_statement) to rebuild the vector index.

To alter vector indexes, you must have the BigQuery Data Editor
(`roles/bigquery.dataEditor`) or BigQuery Data Owner
(`roles/bigquery.dataOwner`) IAM role on the table that contains the
vector index.

**Definitions**

* `table_name`: The name of the table that contains the vector index,
  in the format `dataset_name.table_name`.

  If there is no active vector index on the table, the function returns empty
  results. If there is an active vector index on the table, but the index
  training isn't complete, the function returns a `NULL` drift score.

**Output**

A `FLOAT64` value in the range `[0,1)`. A lower value indicates less drift.
Typically, a change of `0.3` or greater is considered significant.

**Example**

This example returns the drift for the table `mytable`.

```
SELECT * FROM VECTOR_INDEX.STATISTICS(TABLE mydataset.mytable);
```




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-05 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-05 UTC."],[],[]]