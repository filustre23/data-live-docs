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
| [`FARM_FINGERPRINT`](/bigquery/docs/reference/standard-sql/hash_functions#farm_fingerprint) | Computes the fingerprint of a `STRING` or `BYTES` value using the FarmHash Fingerprint64 algorithm. |
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
| [`IS_ACYCLIC`](/bigquery/docs/reference/standard-sql/graph-sql-functions#is_acyclic) | Checks if a graph path has a repeating node. |
| [`IS_INF`](/bigquery/docs/reference/standard-sql/mathematical_functions#is_inf) | Checks if `X` is positive or negative infinity. |
| [`IS_NAN`](/bigquery/docs/reference/standard-sql/mathematical_functions#is_nan) | Checks if `X` is a `NaN` value. |
| [`IS_SIMPLE`](/bigquery/docs/reference/standard-sql/graph-sql-functions#is_simple) | Checks if a graph path is simple. |
| [`IS_TRAIL`](/bigquery/docs/reference/standard-sql/graph-sql-functions#is_trail) | Checks if a graph path has a repeating edge. |<