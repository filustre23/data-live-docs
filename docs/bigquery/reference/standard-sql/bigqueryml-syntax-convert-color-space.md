* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.CONVERT\_COLOR\_SPACE function

This document describes the `ML.CONVERT_COLOR_SPACE` scalar function, which lets
you convert images that have an `RGB` color space to a different color space.
You can use `ML.CONVERT_COLOR_SPACE` with the [`ML.PREDICT`
function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict) or
chain it with other functions or subqueries.

## Syntax

```
ML.CONVERT_COLOR_SPACE(image, target_color_space)
```

### Arguments

`ML.CONVERT_COLOR_SPACE` takes the following arguments:

* `image`: a `STRUCT` value that represents an `RGB` image in one of the
  following forms:

  + `STRUCT<ARRAY<INT64>, ARRAY<FLOAT64>>`
  + `STRUCT<ARRAY<INT64>, ARRAY<INT64>>`

  The first array in the struct must contain the dimensions of the image.
  It must contain three `INT64` values, which represent the image height (H),
  width (W), and number of channels (C).

  The second array in the struct must contain the image data. The
  length of the array must be equivalent to H x W x C from the preceding
  array. If the image data is in `FLOAT64`, each value in the array must be
  between `[0, 1)`. If the image data is in `INT64`, each value in the array
  must be between `[0, 255)`.

  The struct value must be <= 60 MB.
* `target_color_space`: a `STRING` value that specifies the target color space.
  Valid values are `HSV`, `GRAYSCALE`, `YIQ`, and `YUV`.

## Output

`ML.CONVERT_COLOR_SPACE` returns a `STRUCT` value that represents the
modified image in the form `STRUCT<ARRAY<INT64>, ARRAY<FLOAT64>>`.

The first array in the struct represents the dimensions of the image, and
the second array in the struct contains the image data, similar
to the `image` input argument. Each value in the second array is between
`[0, 1)`.

**Note:** If you reference `ML.CONVERT_COLOR_SPACE` in SQL statements in the
BigQuery editor, it is possible for the function output to be
too large to display. If this occurs, write the output to a table instead.

## Example

The following example uses the `ML.CONVERT_COLOR_SPACE` function within the
`ML.PREDICT` function to change the color space for input images from `RGB` to
`GRAYSCALE`:

```
CREATE OR REPLACE TABLE mydataset.model_output
AS (
  SELECT *
  FROM
    ML.PREDICT(
      MODEL `mydataset.mymodel`,
      SELECT
        ML.CONVERT_COLOR_SPACE(ML.DECODE_IMAGE(data), 'GRAYSCALE')
          AS image,
        uri
      FROM `mydataset.images`)
);
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).
* For more information about supported SQL statements and functions for each
  model type, see the following documents:

  + [End-to-end user journeys for generative AI models](/bigquery/docs/e2e-journey-genai)
  + [End-to-end user journeys for time series forecasting models](/bigquery/docs/e2e-journey-forecast)
  + [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
  + [End-to-end user journeys for imported models](/bigquery/docs/e2e-journey-import)
  + [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-08 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-08 UTC."],[],[]]