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
#GoogleSQL
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
#GoogleSQL
SELECT
  x / (SELECT SUM(x)
       FROM (SELECT x FROM UNNEST([1, 2, 3, 4]) AS x)) AS weighted_x
FROM (SELECT x FROM UNNEST([1, 2, 3, 4]) AS x);
```

As another example, consider this query, which uses multiple named subqueries:

```
#GoogleSQL
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
#GoogleSQL
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
#GoogleSQL
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
#GoogleSQL
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
#GoogleSQL
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
#GoogleSQL
WITH TitlesAndScores AS (
  SELECT
    ARRAY_AGG(STRUCT(title, score)) AS titles,
    EXTRACT(DATE FROM time_ts) AS date
  FROM `bigquery-public-data.hacker_news.stories`
  WHERE score IS NOT NULL AND title IS NOT NULL
  GROUP BY date)
SELECT date,
  ARRAY(SELECT AS STRUCT title, score
```