* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Debugging functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following debugging functions.

## Function list

| Name | Summary |
| --- | --- |
| [`ERROR`](/bigquery/docs/reference/standard-sql/debugging_functions#error) | Produces an error with a custom error message. |

## `ERROR`

```
ERROR(error_message)
```

**Description**

Returns an error.

**Definitions**

* `error_message`: A `STRING` value that represents the error message to
  produce. Any whitespace characters beyond a
  single space are trimmed from the results.

**Details**

`ERROR` is treated like any other expression that may
result in an error: there is no special guarantee of evaluation order.

**Return Data Type**

GoogleSQL infers the return type in context.

**Examples**

In the following example, the query produces an error message:

```
-- ERROR: Show this error message (while evaluating error("Show this error message"))
SELECT ERROR('Show this error message')
```

In the following example, the query returns an error message if the value of the
row doesn't match one of two defined values.

```
SELECT
  CASE
    WHEN value = 'foo' THEN 'Value is foo.'
    WHEN value = 'bar' THEN 'Value is bar.'
    ELSE ERROR(CONCAT('Found unexpected value: ', value))
  END AS new_value
FROM (
  SELECT 'foo' AS value UNION ALL
  SELECT 'bar' AS value UNION ALL
  SELECT 'baz' AS value);

-- Found unexpected value: baz
```

The following example demonstrates bad usage of the `ERROR` function. In this
example, GoogleSQL might evaluate the `ERROR` function before or after
the `x > 0` condition, because GoogleSQL doesn't guarantee
ordering between `WHERE` clause conditions. Therefore, the results with the
`ERROR` function might vary.

```
SELECT *
FROM (SELECT -1 AS x)
WHERE x > 0 AND ERROR('Example error');
```

In the next example, the `WHERE` clause evaluates an `IF` condition, which
ensures that GoogleSQL only evaluates the `ERROR` function if the
condition fails.

```
SELECT *
FROM (SELECT -1 AS x)
WHERE IF(x > 0, true, ERROR(FORMAT('Error: x must be positive but is %t', x)));

-- Error: x must be positive but is -1
```




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-29 UTC."],[],[]]