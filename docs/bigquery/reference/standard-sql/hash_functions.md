* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Hash functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following hash functions.

## Function list

| Name | Summary |
| --- | --- |
| [`FARM_FINGERPRINT`](/bigquery/docs/reference/standard-sql/hash_functions#farm_fingerprint) | Computes the fingerprint of a `STRING` or `BYTES` value, using the FarmHash Fingerprint64 algorithm. |
| [`MD5`](/bigquery/docs/reference/standard-sql/hash_functions#md5) | Computes the hash of a `STRING` or `BYTES` value, using the MD5 algorithm. |
| [`SHA1`](/bigquery/docs/reference/standard-sql/hash_functions#sha1) | Computes the hash of a `STRING` or `BYTES` value, using the SHA-1 algorithm. |
| [`SHA256`](/bigquery/docs/reference/standard-sql/hash_functions#sha256) | Computes the hash of a `STRING` or `BYTES` value, using the SHA-256 algorithm. |
| [`SHA512`](/bigquery/docs/reference/standard-sql/hash_functions#sha512) | Computes the hash of a `STRING` or `BYTES` value, using the SHA-512 algorithm. |

## `FARM_FINGERPRINT`

```
FARM_FINGERPRINT(value)
```

**Description**

Computes the fingerprint of the `STRING` or `BYTES` input using the
`Fingerprint64` function from the
[open-source FarmHash library](https://github.com/google/farmhash). The output
of this function for a particular input will never change.

**Return type**

INT64

**Examples**

```
WITH example AS (
  SELECT 1 AS x, "foo" AS y, true AS z UNION ALL
  SELECT 2 AS x, "apple" AS y, false AS z UNION ALL
  SELECT 3 AS x, "" AS y, true AS z
)
SELECT
  *,
  FARM_FINGERPRINT(CONCAT(CAST(x AS STRING), y, CAST(z AS STRING)))
    AS row_fingerprint
FROM example;
/*---+-------+-------+----------------------+
 | x | y     | z     | row_fingerprint      |
 +---+-------+-------+----------------------+
 | 1 | foo   | true  | -1541654101129638711 |
 | 2 | apple | false | 2794438866806483259  |
 | 3 |       | true  | -4880158226897771312 |
 +---+-------+-------+----------------------*/
```

## `MD5`

```
MD5(input)
```

**Description**

Computes the hash of the input using the
[MD5 algorithm](https://en.wikipedia.org/wiki/MD5). The input can either be
`STRING` or `BYTES`. The string version treats the input as an array of bytes.

This function returns 16 bytes.

**Warning:** MD5 is no longer considered secure.
For increased security use another hashing function.

**Return type**

`BYTES`

**Example**

```
SELECT MD5("Hello World") as md5;

-- Note that the result of MD5 is of type BYTES, displayed as a base64-encoded string.
/*--------------------------+
 | md5                      |
 +--------------------------+
 | sQqNsWTgdUEFt6mb5y4/5Q== |
 +--------------------------*/
```

## `SHA1`

```
SHA1(input)
```

**Description**

Computes the hash of the input using the
[SHA-1 algorithm](https://en.wikipedia.org/wiki/SHA-1). The input can either be
`STRING` or `BYTES`. The string version treats the input as an array of bytes.

This function returns 20 bytes.

**Warning:** SHA1 is no longer considered secure.
For increased security, use another hashing function.

**Return type**

`BYTES`

**Example**

```
SELECT SHA1("Hello World") as sha1;

-- Note that the result of SHA1 is of type BYTES, displayed as a base64-encoded string.
/*------------------------------+
 | sha1                         |
 +------------------------------+
 | Ck1VqNd45QIvq3AZd8XYQLvEhtA= |
 +------------------------------*/
```

## `SHA256`

```
SHA256(input)
```

**Description**

Computes the hash of the input using the
[SHA-256 algorithm](https://en.wikipedia.org/wiki/SHA-2). The input can either be
`STRING` or `BYTES`. The string version treats the input as an array of bytes.

This function returns 32 bytes.

**Return type**

`BYTES`

**Example**

```
SELECT SHA256("Hello World") as sha256;
```

## `SHA512`

```
SHA512(input)
```

**Description**

Computes the hash of the input using the
[SHA-512 algorithm](https://en.wikipedia.org/wiki/SHA-2). The input can either be
`STRING` or `BYTES`. The string version treats the input as an array of bytes.

This function returns 64 bytes.

**Return type**

`BYTES`

**Example**

```
SELECT SHA512("Hello World") as sha512;
```




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-08 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-08 UTC."],[],[]]