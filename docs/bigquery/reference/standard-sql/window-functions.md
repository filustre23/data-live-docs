* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Window functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following
[window functions](/bigquery/docs/reference/standard-sql/window-function-calls).

## Function list

| Name | Summary |
| --- | --- |
| [`CUME_DIST`](/bigquery/docs/reference/standard-sql/numbering_functions#cume_dist) | Gets the cumulative distribution (relative position (0,1]) of each row within a window.  For more information, see [Numbering functions](/bigquery/docs/reference/standard-sql/numbering_functions). |
| [`DENSE_RANK`](/bigquery/docs/reference/standard-sql/numbering_functions#dense_rank) | Gets the dense rank (1-based, no gaps) of each row within a window.  For more information, see [Numbering functions](/bigquery/docs/reference/standard-sql/numbering_functions). |
| [`FIRST_VALUE`](/bigquery/docs/reference/standard-sql/navigation_functions#first_value) | Gets a value for the first row in the current window frame.  For more information, see [Navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions). |
| [`LAG`](/bigquery/docs/reference/standard-sql/navigation_functions#lag) | Gets a value for a preceding row.  For more information, see [Navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions). |
| [`LAST_VALUE`](/bigquery/docs/reference/standard-sql/navigation_functions#last_value) | Gets a value for the last row in the current window frame.  For more information, see [Navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions). |
| [`LEAD`](/bigquery/docs/reference/standard-sql/navigation_functions#lead) | Gets a value for a subsequent row.  For more information, see [Navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions). |
| [`NTH_VALUE`](/bigquery/docs/reference/standard-sql/navigation_functions#nth_value) | Gets a value for the Nth row of the current window frame.  For more information, see [Navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions). |
| [`NTILE`](/bigquery/docs/reference/standard-sql/numbering_functions#ntile) | Gets the quantile bucket number (1-based) of each row within a window.  For more information, see [Numbering functions](/bigquery/docs/reference/standard-sql/numbering_functions). |
| [`PERCENT_RANK`](/bigquery/docs/reference/standard-sql/numbering_functions#percent_rank) | Gets the percentile rank (from 0 to 1) of each row within a window.  For more information, see [Numbering functions](/bigquery/docs/reference/standard-sql/numbering_functions). |
| [`PERCENTILE_CONT`](/bigquery/docs/reference/standard-sql/navigation_functions#percentile_cont) | Computes the specified percentile for a value, using linear interpolation.  For more information, see [Navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions). |
| [`PERCENTILE_DISC`](/bigquery/docs/reference/standard-sql/navigation_functions#percentile_disc) | Computes the specified percentile for a discrete value.  For more information, see [Navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions). |
| [`RANK`](/bigquery/docs/reference/standard-sql/numbering_functions#rank) | Gets the rank (1-based) of each row within a window.  For more information, see [Numbering functions](/bigquery/docs/reference/standard-sql/numbering_functions). |
| [`ROW_NUMBER`](/bigquery/docs/reference/standard-sql/numbering_functions#row_number) | Gets the sequential row number (1-based) of each row within a window.  For more information, see [Numbering functions](/bigquery/docs/reference/standard-sql/numbering_functions). |
| [`ST_CLUSTERDBSCAN`](/bigquery/docs/reference/standard-sql/geography_functions#st_clusterdbscan) | Performs DBSCAN clustering on a group of `GEOGRAPHY` values and produces a 0-based cluster number for this row.  For more information, see [Geography functions](/bigquery/docs/reference/standard-sql/geography_functions). |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-15 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-15 UTC."],[],[]]