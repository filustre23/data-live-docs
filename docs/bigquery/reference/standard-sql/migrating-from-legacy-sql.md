* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# Migrating to GoogleSQL

BigQuery supports two SQL dialects:
[GoogleSQL](/bigquery/docs/introduction-sql) and
[legacy SQL](/bigquery/docs/reference/legacy-sql). This document explains the
differences between the two dialects, including [syntax](#syntax_differences),
[functions](#function_comparison), and [semantics](#semantic_differences),
and gives examples of some of the
[highlights of GoogleSQL](#standard_sql_highlights).

## Comparison of legacy and GoogleSQL

When initially released, BigQuery ran queries using a
non-GoogleSQL dialect known as [BigQuery
SQL](/bigquery/docs/reference/legacy-sql). With the launch of
BigQuery 2.0, BigQuery released support for
[GoogleSQL](/bigquery/docs/introduction-sql), and
renamed BigQuery SQL to legacy SQL. GoogleSQL is the
preferred SQL dialect for querying data stored in BigQuery.

### Do I have to migrate to GoogleSQL?

We recommend migrating from legacy SQL to GoogleSQL, but it's not
required for existing queries that use legacy SQL in some cases. For more
information, see [Legacy SQL feature availability](/bigquery/docs/legacy-sql-feature-availability).

### Enabling GoogleSQL

You have a choice of whether to use legacy or GoogleSQL when you run a
query. For information about switching between SQL dialects, see
[BigQuery SQL dialects](/bigquery/docs/introduction-sql#bigquery-sql-dialects).

### Advantages of GoogleSQL

GoogleSQL complies with the SQL 2011 standard, and has extensions that
support querying nested and repeated data. It has several advantages over legacy
SQL, including:

* Composability using [`WITH` clauses](#composability_using_with_clauses) and
  [SQL functions](#composability_using_sql_functions)
* [Subqueries in the `SELECT` list and `WHERE` clause](#subqueries_in_more_places)
* [Correlated subqueries](#correlated_subqueries)
* [`ARRAY` and `STRUCT` data types](#arrays_and_structs)
* [Inserts, updates, and deletes](/bigquery/docs/data-manipulation-language)
* `COUNT(DISTINCT <expr>)` is exact and scalable, providing the accuracy of
  `EXACT_COUNT_DISTINCT` without its limitations
* Automatic predicate push-down through `JOIN`s
* Complex `JOIN` predicates, including arbitrary expressions

For examples that demonstrate some of these features, see
[GoogleSQL highlights](#standard_sql_highlights).

## GoogleSQL highlights

This section discusses some of the highlights of GoogleSQL compared to
legacy SQL.

### Composability using `WITH` clauses

Some of the GoogleSQL examples on this page make use of a
[`WITH` clause](/bigquery/docs/reference/standard-sql/query-syntax#with_clause),
which enables extraction or reuse of named subqueries. For example:

```
#standardSQL
WITH T AS (
  SELECT x FROM UNNEST([1, 2, 3, 4]) AS x
)
SELECT x / (SELECT SUM(x) FROM T) AS weighted_x
FROM T;
```

This query defines a named subquery `T` that contains `x` values of 1, 2, 3,
and 4. It selects `x` values from `T` and divides them by the sum of all `x`
values in `T`. This query is equivalent to a query where the contents of `T`
are inline:

```
#standardSQL
SELECT
  x / (SELECT SUM(x)
       FROM (SELECT x FROM UNNEST([1, 2, 3, 4]) AS x)) AS weighted_x
FROM (SELECT x FROM UNNEST([1, 2, 3, 4]) AS x);
```

As another example, consider this query, which uses multiple named subqueries:

```
#standardSQL
WITH T AS (
  SELECT x FROM UNNEST([1, 2, 3, 4]) AS x
),
TPlusOne AS (
  SELECT x + 1 AS y
  FROM T
),
TPlusOneTimesTwo AS (
  SELECT y * 2 AS z
  FROM TPlusOne
)
SELECT z
FROM TPlusOneTimesTwo;
```

This query defines a sequence of transformations of the original data, followed
by a `SELECT` statement over `TPlusOneTimesTwo`. This query is equivalent to the
following query, which inlines the computations:

```
#standardSQL
SELECT (x + 1) * 2 AS z
FROM (SELECT x FROM UNNEST([1, 2, 3, 4]) AS x);
```

For more information, see
[`WITH` clause](/bigquery/docs/reference/standard-sql/query-syntax#with_clause).

### Composability using SQL functions

GoogleSQL supports
[user-defined SQL functions](/bigquery/docs/user-defined-functions#sql-udf-structure).
You can use user-defined SQL functions to define common expressions and then
reference them from the query. For example:

```
#standardSQL
-- Computes the harmonic mean of the elements in 'arr'.
-- The harmonic mean of x_1, x_2, ..., x_n can be expressed as:
--   n / ((1 / x_1) + (1 / x_2) + ... + (1 / x_n))
CREATE TEMPORARY FUNCTION HarmonicMean(arr ARRAY<FLOAT64>) AS
(
  ARRAY_LENGTH(arr) / (SELECT SUM(1 / x) FROM UNNEST(arr) AS x)
);

WITH T AS (
  SELECT GENERATE_ARRAY(1.0, x * 4, x) AS arr
  FROM UNNEST([1, 2, 3, 4, 5]) AS x
)
SELECT arr, HarmonicMean(arr) AS h_mean
FROM T;
```

This query defines a SQL function named `HarmonicMean` and then applies it to
the array column `arr` from `T`.

### Subqueries in more places

GoogleSQL supports subqueries in the `SELECT` list, `WHERE` clause, and
anywhere else in the query that expects an expression. For example, consider the
following GoogleSQL query that computes the fraction of warm days in Seattle
in 2015:

```
#standardSQL
WITH SeattleWeather AS (
  SELECT *
  FROM `bigquery-public-data.noaa_gsod.gsod2015`
  WHERE stn = '994014'
)
SELECT
  COUNTIF(max >= 70) /
    (SELECT COUNT(*) FROM SeattleWeather) AS warm_days_fraction
FROM SeattleWeather;
```

The Seattle weather station has an ID of `'994014'`. The query computes the
number of warm days based on those where the temperature reached 70 degrees
Fahrenheit, or approximately 21 degrees Celsius, divided by the total number of
recorded days for that station in 2015.

### Correlated subqueries

In GoogleSQL, subqueries can reference correlated columns; that is, columns
that originate from the outer query. For example, consider the following
GoogleSQL query:

```
#standardSQL
WITH WashingtonStations AS (
  SELECT weather.stn AS station_id, ANY_VALUE(station.name) AS name
  FROM `bigquery-public-data.noaa_gsod.stations` AS station
  INNER JOIN `bigquery-public-data.noaa_gsod.gsod2015` AS weather
  ON station.usaf = weather.stn
  WHERE station.state = 'WA' AND station.usaf != '999999'
  GROUP BY station_id
)
SELECT washington_stations.name,
  (SELECT COUNT(*)
   FROM `bigquery-public-data.noaa_gsod.gsod2015` AS weather
   WHERE washington_stations.station_id = weather.stn
   AND max >= 70) AS warm_days
FROM WashingtonStations AS washington_stations
ORDER BY warm_days DESC;
```

This query computes the names of weather stations in Washington state and the
number of days in 2015 that the temperature reached 70 degrees Fahrenheit, or
approximately 21 degrees Celsius. Notice that there is a subquery in the
`SELECT` list, and that the subquery references `washington_stations.station_id`
from the outer scope, namely `FROM WashingtonStations AS washington_stations`.

### Arrays and structs

`ARRAY` and `STRUCT` are powerful concepts in GoogleSQL. As an example that
uses both, consider the following query, which computes the top two articles
for each day in the HackerNews dataset:

```
#standardSQL
WITH TitlesAndScores AS (
  SELECT
    ARRAY_AGG(STRUCT(title, score)) AS titles,
    EXTRACT(DATE FROM time_ts) AS date
  FROM `bigquery-public-data.hacker_news.stories`
  WHERE score IS NOT NULL AND title IS NOT NULL
  GROUP BY date)
SELECT date,
  ARRAY(SELECT AS STRUCT title, score
        FROM UNNEST(titles)
        ORDER BY score DESC
        LIMIT 2)
  AS top_articles
FROM TitlesAndScores
ORDER BY date DESC;
```

The `WITH` clause defines `TitlesAndScores`, which contains two columns. The
first is an array of structs, where one field is an article title and the second
is a score. The `ARRAY_AGG` expression returns an array of these structs for
each day.

The `SELECT` statement following the `WITH` clause uses an `ARRAY` subquery to
sort and return the top two articles within each array in accordance with the
`score`, then returns the results in descending order by date.

For more information about arrays and `ARRAY` subqueries, see
[Working with arrays](/bigquery/docs/arrays). See also the
references for [arrays](/bigquery/docs/reference/standard-sql/data-types#array_type)
and [structs](/bigquery/docs/reference/standard-sql/data-types#struct_type).

## Data type differences

Legacy SQL types have an equivalent in GoogleSQL. In
some cases, the type has a different name. The following table lists each legacy
SQL data type and its GoogleSQL equivalent.

| Legacy SQL | GoogleSQL | Notes |
| --- | --- | --- |
| `BOOLEAN` | `BOOLEAN` |  |
| `INTEGER` | `INT64` |  |
| `FLOAT` | `FLOAT64` |  |
| `NUMERIC` | `NUMERIC` | Legacy SQL has limited support for `NUMERIC` |
| `BIGNUMERIC` | `BIGNUMERIC` | Legacy SQL has limited support for `BIGNUMERIC` |
| `STRING` | `STRING` |  |
| `BYTES` | `BYTES` |  |
| `RECORD` | `STRUCT` |  |
| `REPEATED` | `ARRAY` |  |
| `TIMESTAMP` | `TIMESTAMP` | See [`TIMESTAMP` differences](#timestamp_type_differences) |
| `DATE` | `DATE` | Legacy SQL has limited support for `DATE` |
| `TIME` | `TIME` | Legacy SQL has limited support for `TIME` |
| `DATETIME` | `DATETIME` | Legacy SQL has limited support for `DATETIME` |

For more information see:

* [GoogleSQL data types reference](/bigquery/docs/reference/standard-sql/data-types)
* [Legacy SQL data types reference](/bigquery/docs/data-types)

### `TIMESTAMP` type differences

GoogleSQL has a
[stricter range of valid `TIMESTAMP` values](/bigquery/docs/reference/standard-sql/data-types#timestamp_type)
than legacy SQL does. In GoogleSQL, valid `TIMESTAMP` values are in the
range of `0001-01-01 00:00:00.000000` to `9999-12-31 23:59:59.999999`. For
example, you can select the minimum and maximum `TIMESTAMP` values using
GoogleSQL:

```
#standardSQL
SELECT
  min_timestamp,
  max_timestamp,
  UNIX_MICROS(min_timestamp) AS min_unix_micros,
  UNIX_MICROS(max_timestamp) AS max_unix_micros
FROM (
  SELECT
    TIMESTAMP '0001-01-01 00:00:00.000000' AS min_timestamp,
    TIMESTAMP '9999-12-31 23:59:59.999999' AS max_timestamp
);
```

This query returns `-62135596800000000` as `min_unix_micros` and
`253402300799999999` as `max_unix_micros`.

If you select a column that contains timestamp values outside of this
range, you receive an error:

```
#standardSQL
SELECT timestamp_column_with_invalid_values
FROM MyTableWithInvalidTimestamps;
```

This query returns the following error:

```
Cannot return an invalid timestamp value of -8446744073709551617
microseconds relative to the Unix epoch. The range of valid
timestamp values is [0001-01-1 00:00:00, 9999-12-31 23:59:59.999999]
```

To correct the error, one option is to define and use a
[user-defined function](/bigquery/docs/user-defined-functions)
to filter the invalid timestamps:

```
#standardSQL
CREATE TEMP FUNCTION TimestampIsValid(t TIMESTAMP) AS (
  t >= TIMESTAMP('0001-01-01 00:00:00') AND
  t <= TIMESTAMP('9999-12-31 23:59:59.999999')
);

SELECT timestamp_column_with_invalid_values
FROM MyTableWithInvalidTimestamps
WHERE TimestampIsValid(timestamp_column_with_invalid_values);
```

Another option to correct the error is to use the
[`SAFE_CAST`](/bigquery/docs/reference/standard-sql/conversion_functions#safe_casting)
function with the timestamp column. For example:

```
#standardSQL
SELECT SAFE_CAST(timestamp_column_with_invalid_values AS STRING) AS timestamp_string
FROM MyTableWithInvalidTimestamps;
```

This query returns `NULL` rather than a timestamp string for invalid
timestamp values.

### Automatic data type coercions

Both legacy and GoogleSQL support coercions (automatic conversions) between
certain data types. For example, BigQuery coerces a value of type `INT64` to
`FLOAT64` if the query passes it to a function that requires `FLOAT64` as input.

The following legacy SQL coercions are not supported in GoogleSQL and need to be explicitly cast to the correct type:

| Coercion | Translation |
| --- | --- |
| `BOOLEAN` to `INT64` or `FLOAT64` | Use `SAFE_CAST(bool AS INT64)` or `SAFE_CAST(bool AS FLOAT64)` |
| `INT64` to `TIMESTAMP` | Use `TIMESTAMP_MICROS(micros_value)` |
| `STRING` to `BYTES` | Use `SAFE_CAST(str AS BYTES)` |
| `STRING` to `INT64`, `FLOAT64`, or `BOOL` | Mostly supported by GoogleSQL. For corner cases use `SAFE_CAST(str AS INT64)`, `SAFE_CAST(str AS FLOAT64)`, or `SAFE_CAST(str AS BOOL)` |
| `STRING` to `TIMESTAMP` | Mostly supported by GoogleSQL. For corner cases use `TIMESTAMP(str)` or `SAFE_CAST(str AS TIMESTAMP)` |

For example, the following legacy SQL query uses implicit coercions:

```
#legacySQL
SELECT
  1 + true as boolean_int_coercion,
  TIMESTAMP(1234567890) as integer_timestamp_coercion;
```

In GoogleSQL, this query is invalid. To achieve the same result, you must use explicit casting:

```
#standardSQL
SELECT
  1 + SAFE_CAST(true AS INT64) as boolean_coercion,
  TIMESTAMP_MICROS(1234567890) as integer_timestamp_coercion;
```

## Syntax differences

While GoogleSQL and legacy SQL syntaxes are similar, there are some crucial differences.

### Escaping reserved keywords and invalid identifiers

In legacy SQL, you escape reserved keywords and identifiers that contain
invalid characters such as a space  or hyphen `-` using square brackets `[]`.
In GoogleSQL, you escape such keywords and identifiers using backticks
`` ` ``. For example:

```
#standardSQL
SELECT
  word,
  SUM(word_count) AS word_count
FROM
  `bigquery-public-data.samples.shakespeare`
WHERE word IN ('me', 'I', 'you')
GROUP BY word;
```

Legacy SQL allows reserved keywords in some places that GoogleSQL does not.
For example, the following query fails due to a `Syntax error` using standard
SQL:

```
#standardSQL
SELECT
  COUNT(*) AS rows
FROM
  `bigquery-public-data.samples.shakespeare`;
```

To fix the error, escape the alias `rows` using backticks:

```
#standardSQL
SELECT
  COUNT(*) AS `rows`
FROM
  `bigquery-public-data.samples.shakespeare`;
```

The following is a list of keywords allowed in legacy SQL, but not in GoogleSQL:

|  |  |  |  |
| --- | --- | --- | --- |
| * `ALL` * `AND` * `ANY` * `ARRAY` * `ASSERT_ROWS_MODIFIED` * `AT` * `COLLATE` * `CURRENT` * `DEFAULT` * `DESC` * `END` * `ENUM` | * `ESCAPE` * `EXCEPT` * `EXCLUDE` * `EXTRACT` * `FETCH` * `FOR` * `GROUP` * `GROUPING` * `GROUPS` * `IF` * `INTERVAL` * `IS` | * `LATERAL` * `NATURAL` * `NEW` * `NO` * `NULLS` * `OF` * `ORDER` * `PROTO` * `QUALIFY` * `RANGE` * `RECURSIVE` | * `RESPECT` * `ROLLUP` * `ROWS` * `SOME` * `STRUCT` * `TABLESAMPLE` * `TO` * `TREAT` * `UNNEST` * `WHEN` * `WINDOW` |

For a more comprehensive list of reserved keywords and what constitutes valid identifiers, see the [Reserved keywords](/bigquery/docs/reference/standard-sql/lexical#reserved_keywords) section in [Lexical structure](/bigquery/docs/reference/standard-sql/lexical).

### Project-qualified table names

In legacy SQL, to query a table with a project-qualified name, you can use either a colon `:` or a period `.`.
In GoogleSQL however, you must use only periods `.`.

Example legacy SQL query:

```
#legacySQL
SELECT
```