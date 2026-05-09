* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.HASH\_BUCKETIZE function

This document describes the `ML.HASH_BUCKETIZE` function, which lets you
convert a string expression to a deterministic hash and then bucketize it by the
modulo value of that hash.

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.HASH_BUCKETIZE(string_expression, hash_bucket_size)
```

### Arguments

`ML.HASH_BUCKETIZE` takes the following arguments:

* `string_expression`: the `STRING` expression to bucketize.
* `hash_bucket_size`: an `INT64` value that specifies the number of buckets to
  create. This value must be greater than or equal to `0`. If
  `hash_bucket_size` equals `0`, the function only hashes the string without
  bucketizing the hashed value.

## Output

`ML.HASH_BUCKETIZE` returns an `INT64` value that identifies the bucket.

## Example

The following example bucketizes string expressions into three buckets:

```
SELECT
  f, ML.HASH_BUCKETIZE(f, 3) AS bucket
FROM UNNEST(['a', 'b', 'c', 'd']) AS f;
```

The output looks similar to the following:

```
+---+--------+
| f | bucket |
+---+--------+
| a |   0    |
+---+--------+
| b |   1    |
+---+--------+
| c |   1    |
+---+--------+
| d |   2    |
+------------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-08 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-08 UTC."],[],[]]