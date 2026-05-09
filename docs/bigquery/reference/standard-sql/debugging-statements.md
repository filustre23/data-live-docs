* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Debugging statements Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following debugging statements.

## `ASSERT`

```
ASSERT expression [AS description]
```

**Description**

Evaluates `expression`.

If `expression` evaluates to `TRUE`, the statement returns successfully
without any result.

If `expression` evaluates to `FALSE` or `NULL`, the statement generates an
error. If `AS description` is present, `description` will appear in the error
message.

`expression` must evaluate to a `BOOL`.

`description` must be a `STRING` literal.

An `ASSERT` statement is billed in the same way as the query
`SELECT expression`, except that the result of an `ASSERT` statement is never
cached.

**Examples**

The following examples assert that the data source contains more than a specific
number of rows.

```
-- This query succeeds and no error is produced.
ASSERT (
  (SELECT COUNT(*) > 5 FROM UNNEST([1, 2, 3, 4, 5, 6]))
) AS 'Table must contain more than 5 rows.';
```

```
-- Error: Table must contain more than 10 rows.
ASSERT (
  (SELECT COUNT(*) > 10 FROM UNNEST([1, 2, 3, 4, 5, 6]))
) AS 'Table must contain more than 10 rows.';
```

The following examples assert that the data source contains a particular value.

```
-- This query succeeds and no error is produced.
ASSERT
  EXISTS(
    (SELECT X FROM UNNEST([7877, 7879, 7883, 7901, 7907]) AS X WHERE X = 7907))
AS 'Column X must contain the value 7907.';
```

```
-- Error: Column X must contain the value 7919.
ASSERT
  EXISTS(
    (SELECT X FROM UNNEST([7877, 7879, 7883, 7901, 7907]) AS X WHERE X = 7919))
AS 'Column X must contain the value 7919';
```




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-08 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-08 UTC."],[],[]]