* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Package google.cloud.bigquery.migration.tasks.translation.v2alpha Stay organized with collections Save and categorize content based on your preferences.

## Index

* `BteqOptions` (message)
* `DatasetReference` (message)
* `Filter` (message)
* `IdentifierSettings` (message)
* `IdentifierSettings.IdentifierCase` (enum)
* `IdentifierSettings.IdentifierRewriteMode` (enum)
* `TeradataOptions` (message)
* `TranslationFileMapping` (message)
* `TranslationTaskDetails` (message)
* `TranslationTaskDetails.FileEncoding` (enum)
* `TranslationTaskDetails.TokenType` (enum)

## BteqOptions

BTEQ translation task related settings.

| Fields | |
| --- | --- |
| `project_dataset` | `DatasetReference`  Specifies the project and dataset in BigQuery that will be used for external table creation during the translation. |
| `default_path_uri` | `string`  The Cloud Storage location to be used as the default path for files that are not otherwise specified in the file replacement map. |
| `file_replacement_map` | `map<string, string>`  Maps the local paths that are used in BTEQ scripts (the keys) to the paths in Cloud Storage that should be used in their stead in the translation (the value). |

## DatasetReference

| Fields | |
| --- | --- |
| `dataset_id` | `string`  Required. A unique ID for this dataset, without the project name. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (\_). The maximum length is 1,024 characters. |
| `project_id` | `string`  Optional. The ID of the project containing this dataset. |

## Filter

The filter applied to fields of translation details.

| Fields | |
| --- | --- |
| `input_file_exclusion_prefixes[]` | `string`  The list of prefixes used to exclude processing for input files. |

## IdentifierSettings

Settings related to SQL identifiers.

| Fields | |
| --- | --- |
| `output_identifier_case` | `IdentifierCase`  The setting to control output queries' identifier case. |
| `identifier_rewrite_mode` | `IdentifierRewriteMode`  Specifies the rewrite mode for SQL identifiers. |

## IdentifierCase

The identifier case type.

| Enums | |
| --- | --- |
| `IDENTIFIER_CASE_UNSPECIFIED` | The identifier case is not specified. |
| `ORIGINAL` | Identifiers' cases will be kept as the original cases. |
| `UPPER` | Identifiers will be in upper cases. |
| `LOWER` | Identifiers will be in lower cases. |

## IdentifierRewriteMode

The SQL identifier rewrite mode.

| Enums | |
| --- | --- |
| `IDENTIFIER_REWRITE_MODE_UNSPECIFIED` | SQL Identifier rewrite mode is unspecified. |
| `NONE` | SQL identifiers won't be rewrite. |
| `REWRITE_ALL` | All SQL identifiers will be rewrite. |

## TeradataOptions

This type has no fields.

Teradata SQL specific translation task related settings.

## TranslationFileMapping

Mapping between an input and output file to be translated in a subtask.

| Fields | |
| --- | --- |
| `input_path` | `string`  The Cloud Storage path for a file to translation in a subtask. |
| `output_path` | `string`  The Cloud Storage path to write back the corresponding input file to. |

## TranslationTaskDetails

DEPRECATED! Use TranslationTaskDetails defined in com.google.cloud.bigquery.migration.v2alpha.TranslationTaskDetails instead. The translation task details to capture necessary settings for a translation task and subtask.

| Fields | |
| --- | --- |
| `input_path` | `string`  The Cloud Storage path for translation input files. |
| `output_path` | `string`  The Cloud Storage path for translation output files. |
| `file_paths[]` | `TranslationFileMapping`  Cloud Storage files to be processed for translation. |
| `schema_path` | `string`  The Cloud Storage path to DDL files as table schema to assist semantic translation. |
| `file_encoding` | `FileEncoding`  The file encoding type. |
| `identifier_settings` | `IdentifierSettings`  The settings for SQL identifiers. |
| `special_token_map` | `map<string, TokenType>`  The map capturing special tokens to be replaced during translation. The key is special token in string. The value is the token data type. This is used to translate SQL query template which contains special token as place holder. The special token makes a query invalid to parse. This map will be applied to annotate those special token with types to let parser understand how to parse them into proper structure with type information. |
| `filter` | `Filter`  The filter applied to translation details. |
| `translation_exception_table` | `string`  Specifies the exact name of the bigquery table ("dataset.table") to be used for surfacing raw translation errors. If the table does not exist, we will create it. If it already exists and the schema is the same, we will re-use. If the table exists and the schema is different, we will throw an error. |
| Union field `language_options`. The language specific settings for the translation task. `language_options` can be only one of the following: | |
| `teradata_options` | `TeradataOptions`  The Teradata SQL specific settings for the translation task. |
| `bteq_options` | `BteqOptions`  The BTEQ specific settings for the translation task. |

## FileEncoding

The file encoding types.

| Enums | |
| --- | --- |
| `FILE_ENCODING_UNSPECIFIED` | File encoding setting is not specified. |
| `UTF_8` | File encoding is UTF\_8. |
| `ISO_8859_1` | File encoding is ISO\_8859\_1. |
| `US_ASCII` | File encoding is US\_ASCII. |
| `UTF_16` | File encoding is UTF\_16. |
| `UTF_16LE` | File encoding is UTF\_16LE. |
| `UTF_16BE` | File encoding is UTF\_16BE. |

## TokenType

The special token data type.

| Enums | |
| --- | --- |
| `TOKEN_TYPE_UNSPECIFIED` | Token type is not specified. |
| `STRING` | Token type as string. |
| `INT64` | Token type as integer. |
| `NUMERIC` | Token type as numeric. |
| `BOOL` | Token type as boolean. |
| `FLOAT64` | Token type as float. |
| `DATE` | Token type as date. |
| `TIMESTAMP` | Token type as timestamp. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]