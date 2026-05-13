* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Functions (alphabetical) Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL is the new name for Google Standard SQL!
New name, same great SQL dialect.

This topic contains all functions supported by GoogleSQL for BigQuery.

## Function list

| Name | Summary |
| --- | --- |
| [`ABS`](/bigquery/docs/reference/standard-sql/mathematical_functions#abs) | Computes the absolute value of `X`. |
| [`ACOS`](/bigquery/docs/reference/standard-sql/mathematical_functions#acos) | Computes the inverse cosine of `X`. |
| [`ACOSH`](/bigquery/docs/reference/standard-sql/mathematical_functions#acosh) | Computes the inverse hyperbolic cosine of `X`. |
| [`AEAD.DECRYPT_BYTES`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#aeaddecrypt_bytes) | Uses the matching key from a keyset to decrypt a `BYTES` ciphertext. |
| [`AEAD.DECRYPT_STRING`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#aeaddecrypt_string) | Uses the matching key from a keyset to decrypt a `BYTES` ciphertext into a `STRING` plaintext. |
| [`AEAD.ENCRYPT`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#aeadencrypt) | Encrypts `STRING` plaintext, using the primary cryptographic key in a keyset. |
| [`AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#agg) | Aggregates a measure type. |
| [`ANY_VALUE`](/bigquery/docs/reference/standard-sql/aggregate_functions#any_value) | Gets an expression for some row. |
| [`APPENDS`](/bigquery/docs/reference/standard-sql/time-series-functions#appends) | Returns all rows appended to a table for a given time range. |
| [`APPROX_COUNT_DISTINCT`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_count_distinct) | Gets the approximate result for `COUNT(DISTINCT expression)`. |
| [`APPROX_QUANTILES`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_quantiles) | Gets the approximate quantile boundaries. |
| [`APPROX_TOP_COUNT`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_top_count) | Gets the approximate top elements and their approximate count. |
| [`APPROX_TOP_SUM`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_top_sum) | Gets the approximate top elements and sum, based on the approximate sum of an assigned weight. |
| [`ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#array) | Produces an array with one element for each row in a subquery. |
| [`ARRAY_AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#array_agg) | Gets an array of values. |
| [`ARRAY_CONCAT`](/bigquery/docs/reference/standard-sql/array_functions#array_concat) | Concatenates one or more arrays with the same element type into a single array. |
| [`ARRAY_CONCAT_AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#array_concat_agg) | Concatenates arrays and returns a single array as a result. |
| [`ARRAY_FIRST`](/bigquery/docs/reference/standard-sql/array_functions#array_first) | Gets the first element in an array. |
| [`ARRAY_LAST`](/bigquery/docs/reference/standard-sql/array_functions#array_last) | Gets the last element in an array. |
| [`ARRAY_LENGTH`](/bigquery/docs/reference/standard-sql/array_functions#array_length) | Gets the number of elements in an array. |
| [`ARRAY_REVERSE`](/bigquery/docs/reference/standard-sql/array_functions#array_reverse) | Reverses the order of elements in an array. |
| [`ARRAY_SLICE`](/bigquery/docs/reference/standard-sql/array_functions#array_slice) | Produces an array containing zero or more consecutive elements from an input array. |
| [`ARRAY_TO_STRING`](/bigquery/docs/reference/standard-sql/array_functions#array_to_string) | Produces a concatenation of the elements in an array as a `STRING` value. |
| [`ASCII`](/bigquery/docs/reference/standard-sql/string_functions#ascii) | Gets the ASCII code for the first character or byte in a `STRING` or `BYTES` value. |
| [`ASIN`](/bigquery/docs/reference/standard-sql/mathematical_functions#asin) | Computes the inverse sine of `X`. |
| [`ASINH`](/bigquery/docs/reference/standard-sql/mathematical_functions#asinh) | Computes the inverse hyperbolic sine of `X`. |
| [`ATAN`](/bigquery/docs/reference/standard-sql/mathematical_functions#atan) | Computes the inverse tangent of `X`. |
| [`ATAN2`](/bigquery/docs/reference/standard-sql/mathematical_functions#atan2) | Computes the inverse tangent of `X/Y`, using the signs of `X` and `Y` to determine the quadrant. |
| [`ATANH`](/bigquery/docs/reference/standard-sql/mathematical_functions#atanh) | Computes the inverse hyperbolic tangent of `X`. |
| [`AVG`](/bigquery/docs/reference/standard-sql/aggregate_functions#avg) | Gets the average of non-`NULL` values. |
| [`AVG` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_avg) | `DIFFERENTIAL_PRIVACY`-supported `AVG`.   Gets the differentially-private average of non-`NULL`, non-`NaN` values in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`BAG_OF_WORDS`](/bigquery/docs/reference/standard-sql/text-analysis-functions#bag_of_words) | Gets the frequency of each term (token) in a tokenized document. |
| [`BIT_AND`](/bigquery/docs/reference/standard-sql/aggregate_functions#bit_and) | Performs a bitwise AND operation on an expression. |
| [`BIT_COUNT`](/bigquery/docs/reference/standard-sql/bit_functions#bit_count) | Gets the number of bits that are set in an input expression. |
| [`BIT_OR`](/bigquery/docs/reference/standard-sql/aggregate_functions#bit_or) | Performs a bitwise OR operation on an expression. |
| [`BIT_XOR`](/bigquery/docs/reference/standard-sql/aggregate_functions#bit_xor) | Performs a bitwise XOR operation on an expression. |
| [`BOOL`](/bigquery/docs/reference/standard-sql/json_functions#bool_for_json) | Converts a JSON boolean to a SQL `BOOL` value. |
| [`BYTE_LENGTH`](/bigquery/docs/reference/standard-sql/string_functions#byte_length) | Gets the number of `BYTES` in a `STRING` or `BYTES` value. |
| [`CAST`](/bigquery/docs/reference/standard-sql/conversion_functions#cast) | Convert the results of an expression to the given type. |
| [`CBRT`](/bigquery/docs/reference/standard-sql/mathematical_functions#cbrt) | Computes the cube root of `X`. |
| [`CEIL`](/bigquery/docs/reference/standard-sql/mathematical_functions#ceil) | Gets the smallest integral value that isn't less than `X`. |
| [`CEILING`](/bigquery/docs/reference/standard-sql/mathematical_functions#ceiling) | Synonym of `CEIL`. |
| [`CHANGES`](/bigquery/docs/reference/standard-sql/time-series-functions#changes) | Returns all rows that have changed in a table for a given time range. |
| [`CHAR_LENGTH`](/bigquery/docs/reference/standard-sql/string_functions#char_length) | Gets the number of characters in a `STRING` value. |
| [`CHARACTER_LENGTH`](/bigquery/docs/reference/standard-sql/string_functions#character_length) | Synonym for `CHAR_LENGTH`. |
| [`CHR`](/bigquery/docs/reference/standard-sql/string_functions#chr) | Converts a Unicode code point to a character. |
| [`CODE_POINTS_TO_BYTES`](/bigquery/docs/reference/standard-sql/string_functions#code_points_to_bytes) | Converts an array of extended ASCII code points to a `BYTES` value. |
| [`CODE_POINTS_TO_STRING`](/bigquery/docs/reference/standard-sql/string_functions#code_points_to_string) | Converts an array of extended ASCII code points to a `STRING` value. |
| [`COLLATE`](/bigquery/docs/reference/standard-sql/string_functions#collate) | Combines a `STRING` value and a collation specification into a collation specification-supported `STRING` value. |
| [`CONCAT`](/bigquery/docs/reference/standard-sql/string_functions#concat) | Concatenates one or more `STRING` or `BYTES` values into a single result. |
| [`CONTAINS_SUBSTR`](/bigquery/docs/reference/standard-sql/string_functions#contains_substr) | Performs a normalized, case-insensitive search to see if a value exists as a substring in an expression. |
| [`CORR`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#corr) | Computes the Pearson coefficient of correlation of a set of number pairs. |
| [`COS`](/bigquery/docs/reference/standard-sql/mathematical_functions#cos) | Computes the cosine of `X`. |
| [`COSH`](/bigquery/docs/reference/standard-sql/mathematical_functions#cosh) | Computes the hyperbolic cosine of `X`. |
| [`COSINE_DISTANCE`](/bigquery/docs/reference/standard-sql/mathematical_functions#cosine_distance) | Computes the cosine distance between two vectors. |
| [`COT`](/bigquery/docs/reference/standard-sql/mathematical_functions#cot) | Computes the cotangent of `X`. |
| [`COTH`](/bigquery/docs/reference/standard-sql/mathematical_functions#coth) | Computes the hyperbolic cotangent of `X`. |
| [`COUNT`](/bigquery/docs/reference/standard-sql/aggregate_functions#count) | Gets the number of rows in the input, or the number of rows with an expression evaluated to any value other than `NULL`. |
| [`COUNT` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_count) | `DIFFERENTIAL_PRIVACY`-supported `COUNT`.   Signature 1: Gets the differentially-private count of rows in a query with a `DIFFERENTIAL_PRIVACY` clause.     Signature 2: Gets the differentially-private count of rows with a non-`NULL` expression in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`COUNTIF`](/bigquery/docs/reference/standard-sql/aggregate_functions#countif) | Gets the number of `TRUE` values for an expression. |
| [`COVAR_POP`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#covar_pop) | Computes the population covariance of a set of number pairs. |
| [`COVAR_SAMP`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#covar_samp) | Computes the sample covariance of a set of number pairs. |
| [`CSC`](/bigquery/docs/reference/standard-sql/mathematical_functions#csc) | Computes the cosecant of `X`. |
| [`CSCH`](/bigquery/docs/reference/standard-sql/mathematical_functions#csch) | Computes the hyperbolic cosecant of `X`. |
| [`CUME_DIST`](/bigquery/docs/reference/standard-sql/numbering_functions#cume_dist) | Gets the cumulative distribution (relative position (0,1]) of each row within a window. |
| [`CURRENT_DATE`](/bigquery/docs/reference/standard-sql/date_functions#current_date) | Returns the current date as a `DATE` value. |
| [`CURRENT_DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#current_datetime) | Returns the current date and time as a `DATETIME` value. |
| [`CURRENT_TIME`](/bigquery/docs/reference/standard-sql/time_functions#current_time) | Returns the current time as a `TIME` value. |
| [`CURRENT_TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#current_timestamp) | Returns the current date and time as a `TIMESTAMP` object. |
| [`DATE`](/bigquery/docs/reference/standard-sql/date_functions#date) | Constructs a `DATE` value. |
| [`DATE_ADD`](/bigquery/docs/reference/standard-sql/date_functions#date_add) | Adds a specified time interval to a `DATE` value. |
| [`DATE_BUCKET`](/bigquery/docs/reference/standard-sql/time-series-functions#date_bucket) | Gets the lower bound of the date bucket that contains a date. |
| [`DATE_DIFF`](/bigquery/docs/reference/standard-sql/date_functions#date_diff) | Gets the number of unit boundaries between two `DATE` values at a particular time granularity. |
| [`DATE_FROM_UNIX_DATE`](/bigquery/docs/reference/standard-sql/date_functions#date_from_unix_date) | Interprets an `INT64` expression as the number of days since 1970-01-01. |
| [`DATE_SUB`](/bigquery/docs/reference/standard-sql/date_functions#date_sub) | Subtracts a specified time interval from a `DATE` value. |
| [`DATE_TRUNC`](/bigquery/docs/reference/standard-sql/date_functions#date_trunc) | Truncates a `DATE`, `DATETIME`, or `TIMESTAMP` value at a particular granularity. |
| [`DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#datetime) | Constructs a `DATETIME` value. |
| [`DATETIME_ADD`](/bigquery/docs/reference/standard-sql/datetime_functions#datetime_add) | Adds a specified time interval to a `DATETIME` value. |
| [`DATETIME_BUCKET`](/bigquery/docs/reference/standard-sql/time-series-functions#datetime_bucket) | Gets the lower bound of the datetime bucket that contains a datetime. |
| [`DATETIME_DIFF`](/bigquery/docs/reference/standard-sql/datetime_functions#datetime_diff) | Gets the number of unit boundaries between two `DATETIME` values at a particular time granularity. |
| [`DATETIME_SUB`](/bigquery/docs/reference/standard-sql/datetime_functions#datetime_sub) | Subtracts a specified time interval from a `DATETIME` value. |
| [`DATETIME_TRUNC`](/bigquery/docs/reference/standard-sql/datetime_functions#datetime_trunc) | Truncates a `DATETIME` or `TIMESTAMP` value at a particular granularity. |
| [`DENSE_RANK`](/bigquery/docs/reference/standard-sql/numbering_functions#dense_rank) | Gets the dense rank (1-based, no gaps) of each row within a window. |
| [`DESTINATION_NODE_ID`](/bigquery/docs/reference/standard-sql/graph-sql-functions#destination_node_id) | Gets a unique identifier of a graph edge's destination node. |
| [`DETERMINISTIC_DECRYPT_BYTES`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#deterministic_decrypt_bytes) | Uses the matching key from a keyset to decrypt a `BYTES` ciphertext, using deterministic AEAD. |
| [`DETERMINISTIC_DECRYPT_STRING`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#deterministic_decrypt_string) | Uses the matching key from a keyset to decrypt a `BYTES` ciphertext into a `STRING` plaintext, using deterministic AEAD. |
| [`DETERMINISTIC_ENCRYPT`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#deterministic_encrypt) | Encrypts `STRING` plaintext, using the primary cryptographic key in a keyset, using deterministic AEAD encryption. |
| [`DIV`](/bigquery/docs/reference/standard-sql/mathematical_functions#div) | Divides integer `X` by integer `Y`. |
| [`DLP_DETERMINISTIC_ENCRYPT`](/bigquery/docs/reference/standard-sql/dlp_functions#dlp_deterministic_encrypt) | Encrypts data with a DLP compatible algorithm. |
| [`DLP_DETERMINISTIC_DECRYPT`](/bigquery/docs/reference/standard-sql/dlp_functions#dlp_deterministic_decrypt) | Decrypts DLP-encrypted data. |
| [`DLP_KEY_CHAIN`](/bigquery/docs/reference/standard-sql/dlp_functions#dlp_key_chain) | Gets a data encryption key that's wrapped by Cloud Key Management Service. |
| [`FLOAT64`](/bigquery/docs/reference/standard-sql/json_functions#double_for_json) | Converts a JSON number to a SQL `FLOAT64` value. |
| [`EDGES`](/bigquery/docs/reference/standard-sql/graph-sql-functions#edges) | Gets the edges in a graph path. The resulting array retains the original order in the graph path. |
| [`EDIT_DISTANCE`](/bigquery/docs/reference/standard-sql/string_functions#edit_distance) | Computes the Levenshtein distance between two `STRING` or `BYTES` values. |
| [`ELEMENT_ID`](/bigquery/docs/reference/standard-sql/graph-sql-functions#element_id) | Gets a graph element's unique identifier. |
| [`ENDS_WITH`](/bigquery/docs/reference/standard-sql/string_functions#ends_with) | Checks if a `STRING` or `BYTES` value is the suffix of another value. |
| [`ERROR`](/bigquery/docs/reference/standard-sql/debugging_functions#error) | Produces an error with a custom error message. |
| [`EXP`](/bigquery/docs/reference/standard-sql/mathematical_functions#exp) | Computes `e` to the power of `X`. |
| [`EXTERNAL_OBJECT_TRANSFORM`](/bigquery/docs/reference/standard-sql/table-functions-built-in#external_object_transform) | Produces an object table with the original columns plus one or more additional columns. |
| [`EXTERNAL_QUERY`](/bigquery/docs/reference/standard-sql/federated_query_functions#external_query) | Executes a query on an external database and returns the results as a temporary table. |
| [`EXTRACT`](/bigquery/docs/reference/standard-sql/date_functions#extract) | Extracts part of a date from a `DATE` value. |
| [`EXTRACT`](/bigquery/docs/reference/standard-sql/datetime_functions#extract) | Extracts part of a date and time from a `DATETIME` value. |
| [`EXTRACT`](/bigquery/docs/reference/standard-sql/interval_functions#extract) | Extracts part of an `INTERVAL` value. |
| [`EXTRACT`](/bigquery/docs/reference/standard-sql/time_functions#extract) | Extracts part of a `TIME` value. |
| [`EXTRACT`](/bigquery/docs/reference/standard-sql/timestamp_functions#extract) | Extracts part of a `TIMESTAMP` value. |
| [`EUCLIDEAN_DISTANCE`](/bigquery/docs/reference/standard-sql/mathematical_functions#euclidean_distance) | Computes the Euclidean distance between two vectors. |
| [`FARM_FINGERPRINT`](/bigquery/docs/reference/standard-sql/hash_functions#farm_fingerprint) | Computes the fingerprint of a `STRING` or `BYTES` value, using the FarmHash Fingerprint64 algorithm. |
| [`FIRST_VALUE`](/bigquery/docs/reference/standard-sql/navigation_functions#first_value) | Gets a value for the first row in the current window frame. |
| [`FLOOR`](/bigquery/docs/reference/standard-sql/mathematical_functions#floor) | Gets the largest integral value that isn't greater than `X`. |
| [`FORMAT_DATE`](/bigquery/docs/reference/standard-sql/date_functions#format_date) | Formats a `DATE` value according to a specified format string. |
| [`FORMAT_DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#format_datetime) | Formats a `DATETIME` value according to a specified format string. |
| [`FORMAT_TIME`](/bigquery/docs/reference/standard-sql/time_functions#format_time) | Formats a `TIME` value according to the specified format string. |
| [`FORMAT_TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#format_timestamp) | Formats a `TIMESTAMP` value according to the specified format string. |
| [`FORMAT`](/bigquery/docs/reference/standard-sql/string_functions#format_string) | Formats data and produces the results as a `STRING` value. |
| [`FROM_BASE32`](/bigquery/docs/reference/standard-sql/string_functions#from_base32) | Converts a base32-encoded `STRING` value into a `BYTES` value. |
| [`FROM_BASE64`](/bigquery/docs/reference/standard-sql/string_functions#from_base64) | Converts a base64-encoded `STRING` value into a `BYTES` value. |
| [`FROM_HEX`](/bigquery/docs/reference/standard-sql/string_functions#from_hex) | Converts a hexadecimal-encoded `STRING` value into a `BYTES` value. |
| [`GAP_FILL`](/bigquery/docs/reference/standard-sql/time-series-functions#gap_fill) | Finds and fills gaps in a time series. |
| [`GENERATE_ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#generate_array) | Generates an array of values in a range. |
| [`GENERATE_DATE_ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#generate_date_array) | Generates an array of dates in a range. |
| [`GENERATE_RANGE_ARRAY`](/bigquery/docs/reference/standard-sql/range-functions#generate_range_array) | Splits a range into an array of subranges. |
| [`GENERATE_TIMESTAMP_ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#generate_timestamp_array) | Generates an array of timestamps in a range. |
| [`GENERATE_UUID`](/bigquery/docs/reference/standard-sql/utility-functions#generate_uuid) | Produces a random universally unique identifier (UUID) as a `STRING` value. |
| [`GREATEST`](/bigquery/docs/reference/standard-sql/mathematical_functions#greatest) | Gets the greatest value among `X1,...,XN`. |
| [`GROUPING`](/bigquery/docs/reference/standard-sql/aggregate_functions#grouping) | Checks if a groupable value in the `GROUP BY` clause is aggregated. |
| [`HLL_COUNT.EXTRACT`](/bigquery/docs/reference/standard-sql/hll_functions#hll_countextract) | Extracts a cardinality estimate of an HLL++ sketch. |
| [`HLL_COUNT.INIT`](/bigquery/docs/reference/standard-sql/hll_functions#hll_countinit) | Aggregates values of the same underlying type into a new HLL++ sketch. |
| [`HLL_COUNT.MERGE`](/bigquery/docs/reference/standard-sql/hll_functions#hll_countmerge) | Merges HLL++ sketches of the same underlying type into a new sketch, and then gets the cardinality of the new sketch. |
| [`HLL_COUNT.MERGE_PARTIAL`](/bigquery/docs/reference/standard-sql/hll_functions#hll_countmerge_partial) | Merges HLL++ sketches of the same underlying type into a new sketch. |
| [`IEEE_DIVIDE`](/bigquery/docs/reference/standard-sql/mathematical_functions#ieee_divide) | Divides `X` by `Y`, but doesn't generate errors for division by zero or overflow. |
| [`INITCAP`](/bigquery/docs/reference/standard-sql/string_functions#initcap) | Formats a `STRING` as proper case, which means that the first character in each word is uppercase and all other characters are lowercase. |
| [`INSTR`](/bigquery/docs/reference/standard-sql/string_functions#instr) | Finds the position of a subvalue inside another value, optionally starting the search at a given offset or occurrence. |
| [`INT64`](/bigquery/docs/reference/standard-sql/json_functions#int64_for_json) | Converts a JSON number to a SQL `INT64` value. |
| [`IS_INF`](/bigquery/docs/reference/standard-sql/mathematical_functions#is_inf) | Checks if `X` is positive or negative infinity. |
| [`IS_NAN`](/bigquery/docs/reference/standard-sql/mathematical_functions#is_nan) | Checks if `X` is a `NaN` value. |
| [`JSON_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_array) | Creates a JSON array. |
| [`JSON_ARRAY_APPEND`](/bigquery/docs/reference/standard-sql/json_functions#json_array_append) | Appends JSON data to the end of a JSON array. |
| [`JSON_ARRAY_INSERT`](/bigquery/docs/reference/standard-sql/json_functions#json_array_insert) | Inserts JSON data into a JSON array. |
| [`JSON_EXTRACT`](/bigquery/docs/reference/standard-sql/json_functions#json_extract) | (Deprecated) Extracts a JSON value and converts it to a SQL JSON-formatted `STRING` or `JSON` value. |
| [`JSON_EXTRACT_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_extract_array) | (Deprecated) Extracts a JSON array and converts it to a SQL `ARRAY<JSON-formatted STRING>` or `ARRAY<JSON>` value. |
| [`JSON_EXTRACT_SCALAR`](/bigquery/docs/reference/standard-sql/json_functions#json_extract_scalar) | (Deprecated) Extracts a JSON scalar value and converts it to a SQL `STRING` value. |
| [`JSON_EXTRACT_STRING_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_extract_string_array) | (Deprecated) Extracts a JSON array of scalar values and converts it to a SQL `ARRAY<STRING>` value. |
| [`JSON_FLATTEN`](/bigquery/docs/reference/standard-sql/json_functions#json_flatten) | Produces a new SQL `ARRAY<JSON>` value containing all non-array values that are either directly in the input JSON value or children of one or more consecutively nested arrays in the input JSON value. |
| [`JSON_KEYS`](/bigquery/docs/reference/standard-sql/json_functions#json_keys) | Extracts unique JSON keys from a JSON expression. |
| [`JSON_OBJECT`](/bigquery/docs/reference/standard-sql/json_functions#json_object) | Creates a JSON object. |
| [`JSON_QUERY`](/bigquery/docs/reference/standard-sql/json_functions#json_query) | Extracts a JSON value and converts it to a SQL JSON-formatted `STRING` or `JSON` value. |
| [`JSON_QUERY_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_query_array) | Extracts a JSON array and converts it to a SQL `ARRAY<JSON-formatted STRING>` or `ARRAY<JSON>` value. |
| [`JSON_REMOVE`](/bigquery/docs/reference/standard-sql/json_functions#json_remove) | Produces JSON with the specified JSON data removed. |
| [`JSON_SET`](/bigquery/docs/reference/standard-sql/json_functions#json_set) | Inserts or replaces JSON data. |
| [`JSON_STRIP_NULLS`](/bigquery/docs/reference/standard-sql/json_functions#json_strip_nulls) | Removes JSON nulls from JSON objects and JSON arrays. |
| [`JSON_TYPE`](/bigquery/docs/reference/standard-sql/json_functions#json_type) | Gets the JSON type of the outermost JSON value and converts the name of this type to a SQL `STRING` value. |
| [`JSON_VALUE`](/bigquery/docs/reference/standard-sql/json_functions#json_value) | Extracts a JSON scalar value and converts it to a SQL `STRING` value. |
| [`JSON_VALUE_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_value_array) | Extracts a JSON array of scalar values and converts it to a SQL `ARRAY<STRING>` value. |
| [`JUSTIFY_DAYS`](/bigquery/docs/reference/standard-sql/interval_functions#justify_days) | Normalizes the day part of an `INTERVAL` value. |
| [`JUSTIFY_HOURS`](/bigquery/docs/reference/standard-sql/interval_functions#justify_hours) | Normalizes the time part of an `INTERVAL` value. |
| [`JUSTIFY_INTERVAL`](/bigquery/docs/reference/standard-sql/interval_functions#justify_interval) | Normalizes the day and time parts of an `INTERVAL` value. |
| [`KEYS.ADD_KEY_FROM_RAW_BYTES`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysadd_key_from_raw_bytes) | Adds a key to a keyset, and return the new keyset as a serialized `BYTES` value. |
| [`KEYS.KEYSET_CHAIN`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keyskeyset_chain) | Produces a Tink keyset that's encrypted with a Cloud KMS key. |
| [`KEYS.KEYSET_FROM_JSON`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keyskeyset_from_json) | Converts a `STRING` JSON keyset to a serialized `BYTES` value. |
| [`KEYS.KEYSET_LENGTH`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keyskeyset_length) | Gets the number of keys in the provided keyset. |
| [`KEYS.KEYSET_TO_JSON`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keyskeyset_to_json) | Gets a JSON `STRING` representation of a keyset. |
| [`KEYS.NEW_KEYSET`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysnew_keyset) | Gets a serialized keyset containing a new key based on the key type. |
| [`KEYS.NEW_WRAPPED_KEYSET`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysnew_wrapped_keyset) | Creates a new keyset and encrypts it with a Cloud KMS key. |
| [`KEYS.REWRAP_KEYSET`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysrewrap_keyset) | Re-encrypts a wrapped keyset with a new Cloud KMS key. |
| [`KEYS.ROTATE_KEYSET`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysrotate_keyset) | Adds a new primary cryptographic key to a keyset, based on the key type. |
| [`KEYS.ROTATE_WRAPPED_KEYSET`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#keysrotate_wrapped_keyset) | Rewraps a keyset and rotates it. |
| [`KLL_QUANTILES.EXTRACT_INT64`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesextract_int64) | Gets a selected number of quantiles from an `INT64`-initialized KLL sketch. |
| [`KLL_QUANTILES.EXTRACT_FLOAT64`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesextract_double) | Gets a selected number of quantiles from a `FLOAT64`-initialized KLL sketch. |
| [`KLL_QUANTILES.EXTRACT_POINT_INT64`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesextract_point_int64) | Gets a specific quantile from an `INT64`-initialized KLL sketch. |
| [`KLL_QUANTILES.EXTRACT_POINT_FLOAT64`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesextract_point_double) | Gets a specific quantile from a `FLOAT64`-initialized KLL sketch. |
| [`KLL_QUANTILES.INIT_INT64`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesinit_int64) | Aggregates values into an `INT64`-initialized KLL sketch. |
| [`KLL_QUANTILES.INIT_FLOAT64`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesinit_double) | Aggregates values into a `FLOAT64`-initialized KLL sketch. |
| [`KLL_QUANTILES.MERGE_INT64`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesmerge_int64) | Merges `INT64`-initialized KLL sketches into a new sketch, and then gets the quantiles from the new sketch. |
| [`KLL_QUANTILES.MERGE_FLOAT64`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesmerge_double) | Merges `FLOAT64`-initialized KLL sketches into a new sketch, and then gets the quantiles from the new sketch. |
| [`KLL_QUANTILES.MERGE_PARTIAL`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesmerge_partial) | Merges KLL sketches of the same underlying type into a new sketch. |
| [`KLL_QUANTILES.MERGE_POINT_INT64`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesmerge_point_int64) | Merges `INT64`-initialized KLL sketches into a new sketch, and then gets a specific quantile from the new sketch. |
| [`KLL_QUANTILES.MERGE_POINT_FLOAT64`](/bigquery/docs/reference/standard-sql/kll_functions#kll_quantilesmerge_point_double) | Merges `FLOAT64`-initialized KLL sketches into a new sketch, and then gets a specific quantile from the new sketch. |
| [`LABELS`](/bigquery/docs/reference/standard-sql/graph-sql-functions#labels) | Gets the labels associated with a graph element. |
| [`LAG`](/bigquery/docs/reference/standard-sql/navigation_functions#lag) | Gets a value for a preceding row. |
| [`LAST_DAY`](/bigquery/docs/reference/standard-sql/date_functions#last_day) | Gets the last day in a specified time period that contains a `DATE` value. |
| [`LAST_DAY`](/bigquery/docs/reference/standard-sql/datetime_functions#last_day) | Gets the last day in a specified time period that contains a `DATETIME` value. |
| [`LAST_VALUE`](/bigquery/docs/reference/standard-sql/navigation_functions#last_value) | Gets a value for the last row in the current window frame. |
| [`LAX_BOOL`](/bigquery/docs/reference/standard-sql/json_functions#lax_bool) | Attempts to convert a JSON value to a SQL `BOOL` value. |
| [`LAX_FLOAT64`](/bigquery/docs/reference/standard-sql/json_functions#lax_double) | Attempts to convert a JSON value to a SQL `FLOAT64` value. |
| [`LAX_INT64`](/bigquery/docs/reference/standard-sql/json_functions#lax_int64) | Attempts to convert a JSON value to a SQL `INT64` value. |
| [`LAX_STRING`](/bigquery/docs/reference/standard-sql/json_functions#lax_string) | Attempts to convert a JSON value to a SQL `STRING` value. |
| [`LEAD`](/bigquery/docs/reference/standard-sql/navigation_functions#lead) | Gets a value for a subsequent row. |
| [`LEAST`](/bigquery/docs/reference/standard-sql/mathematical_functions#least) | Gets the least value among `X1,...,XN`. |
| [`LEFT`](/bigquery/docs/reference/standard-sql/string_functions#left) | Gets the specified leftmost portion from a `STRING` or `BYTES` value. |
| [`LENGTH`](/bigquery/docs/reference/standard-sql/string_functions#length) | Gets the length of a `STRING` or `BYTES` value. |
| [`LN`](/bigquery/docs/reference/standard-sql/mathematical_functions#ln) | Computes the natural logarithm of `X`. |
| [`LOG`](/bigquery/docs/reference/standard-sql/mathematical_functions#log) | Computes the natural logarithm of `X` or the logarithm of `X` to base `Y`. |
| [`LOG10`](/bigquery/docs/reference/standard-sql/mathematical_functions#log10) | Computes the natural logarithm of `X` to base 10. |
| [`LOGICAL_AND`](/bigquery/docs/reference/standard-sql/aggregate_functions#logical_and) | Gets the logical AND of all non-`NULL` expressions. |
| [`LOGICAL_OR`](/bigquery/docs/reference/standard-sql/aggregate_functions#logical_or) | Gets the logical OR of all non-`NULL` expressions. |
| [`LOWER`](/bigquery/docs/reference/standard-sql/string_functions#lower) | Formats alphabetic characters in a `STRING` value as lowercase.    Formats ASCII characters in a `BYTES` value as lowercase. |
| [`LPAD`](/bigquery/docs/reference/standard-sql/string_functions#lpad) | Prepends a `STRING` or `BYTES` value with a pattern. |
| [`LTRIM`](/bigquery/docs/reference/standard-sql/string_functions#ltrim) | Identical to the `TRIM` function, but only removes leading characters. |
| [`MAKE_INTERVAL`](/bigquery/docs/reference/standard-sql/interval_functions#make_interval) | Constructs an `INTERVAL` value. |
| [`MAX`](/bigquery/docs/reference/standard-sql/aggregate_functions#max) | Gets the maximum non-`NULL` value. |
| [`MAX_BY`](/bigquery/docs/reference/standard-sql/aggregate_functions#max_by) | Synonym for `ANY_VALUE(x HAVING MAX y)`. |
| [`MD5`](/bigquery/docs/reference/standard-sql/hash_functions#md5) | Computes the hash of a `STRING` or `BYTES` value, using the MD5 algorithm. |
| [`MIN`](/bigquery/docs/reference/standard-sql/aggregate_functions#min) | Gets the minimum non-`NULL` value. |
| [`MIN_BY`](/bigquery/docs/reference/standard-sql/aggregate_functions#min_by) | Synonym for `ANY_VALUE(x HAVING MIN y)`. |
| [`MOD`](/bigquery/docs/reference/standard-sql/mathematical_functions#mod) | Gets the remainder of the division of `X` by `Y`. |
| [`NET.HOST`](/bigquery/docs/reference/standard-sql/net_functions#nethost) | Gets the hostname from a URL. |
| [`NET.IP_FROM_STRING`](/bigquery/docs/reference/standard-sql/net_functions#netip_from_string) | Converts an IPv4 or IPv6 address from a `STRING` value to a `BYTES` value in network byte order. |
| [`NET.IP_NET_MASK`](/bigquery/docs/reference/standard-sql/net_functions#netip_net_mask) | Gets a network mask. |
| [`NET.IP_TO_STRING`](/bigquery/docs/reference/standard-sql/net_functions#netip_to_string) | Converts an IPv4 or IPv6 address from a `BYTES` value in network byte order to a `STRING` value. |
| [`NET.IP_TRUNC`](/bigquery/docs/reference/standard-sql/net_functions#netip_trunc) | Converts a `BYTES` IPv4 or IPv6 address in network byte order to a `BYTES` subnet address. |
| [`NET.IPV4_FROM_INT64`](/bigquery/docs/reference/standard-sql/net_functions#netipv4_from_int64) | Converts an IPv4 address from an `INT64` value to a `BYTES` value in network byte order. |
| [`NET.IPV4_TO_INT64`](/bigquery/docs/reference/standard-sql/net_functions#netipv4_to_int64) | Converts an IPv4 address from a `BYTES` value in network byte order to an `INT64` value. |
| [`NET.PUBLIC_SUFFIX`](/bigquery/docs/reference/standard-sql/net_functions#netpublic_suffix) | Gets the public suffix from a URL. |
| [`NET.REG_DOMAIN`](/bigquery/docs/reference/standard-sql/net_functions#netreg_domain) | Gets the registered or registrable domain from a URL. |
| [`NET.SAFE_IP_FROM_STRING`](/bigquery/docs/reference/standard-sql/net_functions#netsafe_ip_from_string) | Similar to the `NET.IP_FROM_STRING`, but returns `NULL` instead of producing an error if the input is invalid. |
| [`NODES`](/bigquery/docs/reference/standard-sql/graph-sql-functions#nodes) | Gets the nodes in a graph path. The resulting array retains the original order in the graph path. |
| [`NORMALIZE`](/bigquery/docs/reference/standard-sql/string_functions#normalize) | Case-sensitively normalizes the characters in a `STRING` value. |
| [`NORMALIZE_AND_CASEFOLD`](/bigquery/docs/reference/standard-sql/string_functions#normalize_and_casefold) | Case-insensitively normalizes the characters in a `STRING` value. |
| [`NTH_VALUE`](/bigquery/docs/reference/standard-sql/navigation_functions#nth_value) | Gets a value for the Nth row of the current window frame. |
| [`NTILE`](/bigquery/docs/reference/standard-sql/numbering_functions#ntile) | Gets the quantile bucket number (1-based) of each row within a window. |
| [`OBJ.FETCH_METADATA`](/bigquery/docs/reference/standard-sql/objectref_functions#objfetch_metadata) | Fetches Cloud Storage metadata for a partially populated `ObjectRef` value. |
| [`OBJ.GET_ACCESS_URL`](/bigquery/docs/reference/standard-sql/objectref_functions#objget_access_url) | Returns access URLs for a Cloud Storage object. |
| [`OBJ.GET_READ_URL`](/bigquery/docs/reference/standard-sql/objectref_functions#objget_read_url) | Returns a read URL and status for a Cloud Storage object. |
| [`OBJ.MAKE_REF`](/bigquery/docs/reference/standard-sql/objectref_functions#objmake_ref) | Creates an `ObjectRef` value that contains reference information for a Cloud Storage object. |
| [`OCTET_LENGTH`](/bigquery/docs/reference/standard-sql/string_functions#octet_length) | Alias for `BYTE_LENGTH`. |
| [`PARSE_BIGNUMERIC`](/bigquery/docs/reference/standard-sql/conversion_functions#parse_bignumeric) | Converts a `STRING` value to a `BIGNUMERIC` value. |
| [`PARSE_DATE`](/bigquery/docs/reference/standard-sql/date_functions#parse_date) | Converts a `STRING` value to a `DATE` value. |
| [`PARSE_DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#parse_datetime) | Converts a `STRING` value to a `DATETIME` value. |
| [`PARSE_JSON`](/bigquery/docs/reference/standard-sql/json_functions#parse_json) | Converts a JSON-formatted `STRING` value to a `JSON` value. |
| [`PARSE_NUMERIC`](/bigquery/docs/reference/standard-sql/conversion_functions#parse_numeric) | Converts a `STRING` value to a `NUMERIC` value. |
| [`PARSE_TIME`](/bigquery/docs/reference/standard-sql/time_functions#parse_time) | Converts a `STRING` value to a `TIME` value. |
| [`PARSE_TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#parse_timestamp) | Converts a `STRING` value to a `TIMESTAMP` value. |
| [`PATH_FIRST`](/bigquery/docs/reference/standard-sql/graph-sql-functions#path_first) | Gets the first node in a graph path. |
| [`PATH_LAST`](/bigquery/docs/reference/standard-sql/graph-sql-functions#path_last) | Gets the last node in a graph path. |
| [`PATH_LENGTH`](/bigquery/docs/reference/standard-sql/graph-sql-functions#path_length) | Gets the number of edges in a graph path. |
| [`PERCENT_RANK`](/bigquery/docs/reference/standard-sql/numbering_functions#percent_rank) | Gets the percentile rank (from 0 to 1) of each row within a window. |
| [`PERCENTILE_CONT`](/bigquery/docs/reference/standard-sql/navigation_functions#percentile_cont) | Computes the specified percentile for a value, using linear interpolation. |
| [`PERCENTILE_CONT` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_percentile_cont) | `DIFFERENTIAL_PRIVACY`-supported `PERCENTILE_CONT`.   Computes a differentially-private percentile across privacy unit columns in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`PERCENTILE_DISC`](/bigquery/docs/reference/standard-sql/navigation_functions#percentile_disc) | Computes the specified percentile for a discrete value. |
| [`POW`](/bigquery/docs/reference/standard-sql/mathematical_functions#pow) | Produces the value of `X` raised to the power of `Y`. |
| [`POWER`](/bigquery/docs/reference/standard-sql/mathematical_functions#power) | Synonym of `POW`. |
| [`RAND`](/bigquery/docs/reference/standard-sql/mathematical_functions#rand) | Generates a pseudo-random value of type `FLOAT64` in the range of `[0, 1)`. |
| [`RANGE`](/bigquery/docs/reference/standard-sql/range-functions#range) |  |