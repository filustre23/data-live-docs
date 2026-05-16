* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.NGRAMS function

This document describes the `ML.NGRAMS` function, which lets you create
[n-grams](https://wikipedia.org/wiki/N-gram) of the input values.

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)).

## Syntax

```
ML.NGRAMS(array_input, range [, separator])
```

### Arguments

`ML.NGRAMS` takes the following arguments:

* `array_input`: an `ARRAY<STRING>` value that represent the tokens to be
  merged.
* `range`: an `ARRAY` of two `INT64` elements or a single `INT64` value. If
  you specify an `ARRAY` value, the `INT64` elements provide the range
  of n-gram sizes to return. Provide the numerical values in order, lower to
  higher. If you specify a single `INT64` value of *x*, the
  range of n-gram sizes to return is `[x, x]`.
* `separator`: a `STRING` value that specifies the separator to
  connect two adjacent tokens in the output. The default value is
  whitespace .

## Output

`ML.NGRAMS` returns an `ARRAY<STRING>` value that contain the n-grams.

## Example

The following example outputs all possible 2-token and 3-token combinations
for a set of three input strings:

```
SELECT
  ML.NGRAMS(['a', 'b', 'c'], [2,3], '#') AS output;
```

The output looks similar to the following:

```
+-----------------------+
|        output         |
+-----------------------+
| ["a#b","a#b#c","b#c"] |
+-----------------------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-15 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-15 UTC."],[],[]]