* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.LP\_NORM function

This document describes the `ML.LP_NORM` scalar function, which lets you
compute the [Lp](https://en.wikipedia.org/wiki/Lp_space) norm for
a vector, where p is the degree.

## Syntax

```
ML.LP_NORM(vector, degree)
```

### Arguments

`ML.LP_NORM` has the following arguments:

* `vector`: an `ARRAY<Numerical type>` value that represents a vector,
  where `Numerical type` can be `BIGNUMERIC`, `FLOAT64`,
  `INT64` or `NUMERIC`. For example `ARRAY<BIGNUMERIC>`.

  Each element of the array denotes one dimension of the vector. An example
  of a four-dimensional vector is `[0.0, 1.0, 1.0, 0.0]`.

  The function calculates the p degree norm of the numerical type
  values in all the values in the array.
* `degree`: a `FLOAT64` value that specifies the degree. This can be `0.0`,
  any value >= `1.0`, or `CAST('INF' AS FLOAT64)` to return the L\_infinity
  norm of the vector, which is the largest magnitude of the values in
  the vector.

  Commonly used values are `1.0` to calculate the [Manhattan
  norm](https://en.wikipedia.org/wiki/Norm_(mathematics)#Taxicab_norm_or_Manhattan_norm)
  of the vector and `2.0` to calculate the [Euclidean
  norm](https://en.wikipedia.org/wiki/Norm_(mathematics)#Euclidean_norm) of
  the vector.

## Output

`ML.LP_NORM` returns a `FLOAT64` value that represents the Lp norm
for the vector. Returns `NULL` if `vector` is `NULL`.

## Example

The following example gets the Euclidean norm for vectors consisting of
`ARRAY<FLOAT64>` values:

1. Create the table `t1`:

   ```
   CREATE TABLE mydataset.t1
   (
     v1 ARRAY<FLOAT64>,
     v2 ARRAY<FLOAT64>
   )
   ```
2. Populate `t1`:

   ```
   INSERT mydataset.t1 (v1,v2)
   VALUES ([4.1,0.5,1.0], [3.0,0.0,2.5])
   ```
3. Calculate the Euclidean norm for `v1` and `v2`:

   ```
   SELECT v1, ML.LP_NORM(v1, 2.0) AS v1_norm, v2, ML.LP_NORM(v2, 2.0) AS v2_norm
   FROM mydataset.t1;
   ```

   This query produces the following output:

   ```
   +---------------------------+-----+-------------------+
   | v1  | v1_norm             | v2  | v2_norm           |
   +---------------------------+-----+-------------------+
   | 4.1 | 4.2497058721751557  | 3.0 | 3.905124837953327 |
   +-----|                     |-----|                   |
   | 0.5 |                     | 0.0 |                   |
   +-----|                     |-----+                   |
   | 1.0 |                     | 2.5 |                   |
   +---------------------------+-----+-------------------+
   ```

## What's next

* For information about the supported SQL statements and functions for each
  model type, see
  [End-to-end user journey for each model](/bigquery/docs/e2e-journey).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-08 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-08 UTC."],[],[]]