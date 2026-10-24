* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: routines Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Routine](#Routine)
  + [JSON representation](#Routine.SCHEMA_REPRESENTATION)
* [RoutineReference](#RoutineReference)
  + [JSON representation](#RoutineReference.SCHEMA_REPRESENTATION)
* [RoutineType](#RoutineType)
* [Language](#Language)
* [Argument](#Argument)
  + [JSON representation](#Argument.SCHEMA_REPRESENTATION)
* [ArgumentKind](#ArgumentKind)
* [Mode](#Mode)
* [StandardSqlTableType](#StandardSqlTableType)
  + [JSON representation](#StandardSqlTableType.SCHEMA_REPRESENTATION)
* [DeterminismLevel](#DeterminismLevel)
* [RemoteFunctionOptions](#RemoteFunctionOptions)
  + [JSON representation](#RemoteFunctionOptions.SCHEMA_REPRESENTATION)
* [SparkOptions](#SparkOptions)
  + [JSON representation](#SparkOptions.SCHEMA_REPRESENTATION)
* [DataGovernanceType](#DataGovernanceType)
* [PythonOptions](#PythonOptions)
  + [JSON representation](#PythonOptions.SCHEMA_REPRESENTATION)
* [ExternalRuntimeOptions](#ExternalRuntimeOptions)
  + [JSON representation](#ExternalRuntimeOptions.SCHEMA_REPRESENTATION)
* [RoutineBuildStatus](#RoutineBuildStatus)
  + [JSON representation](#RoutineBuildStatus.SCHEMA_REPRESENTATION)
* [BuildState](#BuildState)
* [Methods](#METHODS_SUMMARY)

## Resource: Routine

A user-defined function or a stored procedure.

| JSON representation |
| --- |
| ``` {   "etag": string,   "routineReference": {     object (RoutineReference)   },   "routineType": enum (RoutineType),   "creationTime": string,   "lastModifiedTime": string,   "language": enum (Language),   "arguments": [     {       object (Argument)     }   ],   "returnType": {     object (StandardSqlDataType)   },   "returnTableType": {     object (StandardSqlTableType)   },   "importedLibraries": [     string   ],   "definitionBody": string,   "description": string,   "determinismLevel": enum (DeterminismLevel),   "strictMode": boolean,   "remoteFunctionOptions": {     object (RemoteFunctionOptions)   },   "sparkOptions": {     object (SparkOptions)   },   "dataGovernanceType": enum (DataGovernanceType),   "pythonOptions": {     object (PythonOptions)   },   "externalRuntimeOptions": {     object (ExternalRuntimeOptions)   },   "buildStatus": {     object (RoutineBuildStatus)   } } ``` |

| Fields | |
| --- | --- |
| `etag` | `string`  Output only. A hash of this resource. |
| `routineReference` | `object (RoutineReference)`  Required. Reference describing the ID of this routine. |
| `routineType` | `enum (RoutineType)`  Required. The type of routine. |
| `creationTime` | `string (int64 format)`  Output only. The time when this routine was created, in milliseconds since the epoch. |
| `lastModifiedTime` | `string (int64 format)`  Output only. The time when this routine was last modified, in milliseconds since the epoch. |
| `language` | `enum (Language)`  Optional. Defaults to "SQL" if remoteFunctionOptions field is absent, not set otherwise. |
| `arguments[]` | `object (Argument)`  Optional. |
| `returnType` | `object (StandardSqlDataType)`  Optional if language = "SQL"; required otherwise. Cannot be set if routineType = "TABLE\_VALUED\_FUNCTION".  If absent, the return type is inferred from definitionBody at query time in each query that references this routine. If present, then the evaluated result will be cast to the specified returned type at query time.  For example, for the functions created with the following statements:   * `CREATE FUNCTION Add(x FLOAT64, y FLOAT64) RETURNS FLOAT64 AS (x + y);` * `CREATE FUNCTION Increment(x FLOAT64) AS (Add(x, 1));` * `CREATE FUNCTION Decrement(x FLOAT64) RETURNS FLOAT64 AS (Add(x, -1));`   The returnType is `{typeKind: "FLOAT64"}` for `Add` and `Decrement`, and is absent for `Increment` (inferred as FLOAT64 at query time).  Suppose the function `Add` is replaced by `CREATE OR REPLACE FUNCTION Add(x INT64, y INT64) AS (x + y);`  Then the inferred return type of `Increment` is automatically changed to INT64 at query time, while the return type of `Decrement` remains FLOAT64. |
| `returnTableType` | `object (StandardSqlTableType)`  Optional. Can be set only if routineType = "TABLE\_VALUED\_FUNCTION".  If absent, the return table type is inferred from definitionBody at query time in each query that references this routine. If present, then the columns in the evaluated table result will be cast to match the column types specified in return table type, at query time. |
| `importedLibraries[]` | `string`  Optional. If language = "JAVASCRIPT", this field stores the path of the imported JAVASCRIPT libraries. |
| `definitionBody` | `string`  Required. The body of the routine.  For functions, this is the expression in the AS clause.  If `language = "SQL"`, it is the substring inside (but excluding) the parentheses. For example, for the function created with the following statement:  `CREATE FUNCTION JoinLines(x string, y string) as (concat(x, "\n", y))`  The definitionBody is `concat(x, "\n", y)` (\n is not replaced with linebreak).  If `language="JAVASCRIPT"`, it is the evaluated string in the AS clause. For example, for the function created with the following statement:  `CREATE FUNCTION f() RETURNS STRING LANGUAGE js AS 'return "\n";\n'`  The definitionBody is  `return "\n";\n`  Note that both \n are replaced with linebreaks.  If `definitionBody` references another routine, then that routine must be fully qualified with its project ID. |
| `description` | `string`  Optional. The description of the routine, if defined. |
| `determinismLevel` | `enum (DeterminismLevel)`  Optional. The determinism level of the JavaScript UDF, if defined. |
| `strictMode` | `boolean`  Optional. Use this option to catch many common errors. Error checking is not exhaustive, and successfully creating a procedure doesn't guarantee that the procedure will successfully execute at runtime. If `strictMode` is set to `TRUE`, the procedure body is further checked for errors such as non-existent tables or columns. The `CREATE PROCEDURE` statement fails if the body fails any of these checks.  If `strictMode` is set to `FALSE`, the procedure body is checked only for syntax. For procedures that invoke themselves recursively, specify `strictMode=FALSE` to avoid non-existent procedure errors during validation.  Default value is `TRUE`. |
| `remoteFunctionOptions` | `object (RemoteFunctionOptions)`  Optional. Remote function specific options. |
| `sparkOptions` | `object (SparkOptions)`  Optional. Spark specific options. |
| `dataGovernanceType` | `enum (DataGovernanceType)`  Optional. If set to `DATA_MASKING`, the function is validated and made available as a masking function. For more information, see [Create custom masking routines](https://cloud.google.com/bigquery/docs/user-defined-functions#custom-mask). |
| `pythonOptions` | `object (PythonOptions)`  Optional. Options for the Python UDF. [Preview](https://cloud.google.com/products/#product-launch-stages) |
| `externalRuntimeOptions` | `object (ExternalRuntimeOptions)`  Optional. Options for the runtime of the external system executing the routine. This field is only applicable for Python UDFs. [Preview](https://cloud.google.com/products/#product-launch-stages) |
| `buildStatus` | `object (RoutineBuildStatus)`  Output only. The build status of the routine. This field is only applicable to Python UDFs. [Preview](https://cloud.google.com/products/#product-launch-stages) |

## RoutineReference

Id path of a routine.

| JSON representation |
| --- |
| ``` {   "projectId": string,   "datasetId": string,   "routineId": string } ``` |

| Fields | |
| --- | --- |
| `projectId` | `string`  Required. The ID of the project containing this routine. |
| `datasetId` | `string`  Required. The ID of the dataset containing this routine. |
| `routineId` | `string`  Required. The ID of the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (\_). The maximum length is 256 characters. |

## RoutineType

The fine-grained type of the routine.

| Enums | |
| --- | --- |
| `ROUTINE_TYPE_UNSPECIFIED` | Default value. |
| `SCALAR_FUNCTION` | Non-built-in persistent scalar function. |
| `PROCEDURE` | Stored procedure. |
| `TABLE_VALUED_FUNCTION` | Non-built-in persistent TVF. |

## Language

The language of the routine.

| Enums | |
| --- | --- |
| `LANGUAGE_UNSPECIFIED` | Default value. |
| `SQL` | SQL language. |
| `JAVASCRIPT` | JavaScript language. |
| `PYTHON` | Python language. |
| `JAVA` | Java language. |
| `SCALA` | Scala language. |

## Argument

Input/output argument of a function or a stored procedure.

| JSON representation |
| --- |
| ``` {   "name": string,   "argumentKind": enum (ArgumentKind),   "mode": enum (Mode),   "dataType": {     object (StandardSqlDataType)   },   "tableType": {     object (StandardSqlTableType)   } } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Optional. The name of this argument. Can be absent for function return argument. |
| `argumentKind` | `enum (ArgumentKind)`  Optional. Defaults to FIXED\_TYPE. |
| `mode` | `enum (Mode)`  Optional. Specifies whether the argument is input or output. Can be set for procedures only. |
| `dataType` | `object (StandardSqlDataType)`  Set if argumentKind == FIXED\_TYPE. |
| `tableType` | `object (StandardSqlTableType)`  Optional. Set if argumentKind == FIXED\_TABLE. |

## ArgumentKind

Represents the kind of a given argument.

| Enums | |
| --- | --- |
| `ARGUMENT_KIND_UNSPECIFIED` | Default value. |
| `FIXED_TYPE` | The argument is a variable with fully specified type, which can be a struct or an array, but not a table. |
| `ANY_TYPE` | The argument is any type, including struct or array, but not a table. |
| `FIXED_TABLE` | The argument is a table with fully specified column names and types. |
| `ANY_TABLE` | The argument is any table type. |

## Mode

The input/output mode of the argument.

| Enums | |
| --- | --- |
| `MODE_UNSPECIFIED` | Default value. |
| `IN` | The argument is input-only. |
| `OUT` | The argument is output-only. |
| `INOUT` | The argument is both an input and an output. |

## StandardSqlTableType

A table type

| JSON representation |
| --- |
| ``` {   "columns": [     {       object (StandardSqlField)     }   ] } ``` |

| Fields | |
| --- | --- |
| `columns[]` | `object (` |