* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Collation Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports collation. Collation
defines rules to sort and compare strings in certain
[operations](#collate_operations), such as conditional expressions, joins, and
groupings.

By default, GoogleSQL sorts strings case-sensitively. This means that `a` and
`A` are treated as different letters, and `Z` would come before `a`.

**Example default sorting:** Apple, Zebra, apple

By contrast, collation lets you sort and compare strings case-insensitively or
according to specific language rules.

**Example case-insensitive collation:** Apple, apple, Zebra

To customize collation for a
collation-supported operation, you typically [assign a collation
specification](#collate_define) to at least one string in the operation inputs.
Some operations can't use collation, but can [propagate collation through
them](#collate_propagate).

Collation is useful when you need fine-tuned control over how values are sorted,
joined, or grouped in tables.

## Operations affected by collation

The following example query operations are affected by collation when
sorting and comparing strings:

| Operations |
| --- |
| Collation-supported [comparison operations](#collate_funcs) |
| [Join operations](/bigquery/docs/reference/standard-sql/query-syntax#join_types) |
| [`ORDER BY`](/bigquery/docs/reference/standard-sql/query-syntax#order_by_clause) |
| [`GROUP BY`](/bigquery/docs/reference/standard-sql/query-syntax#group_by_clause) |
| [`WINDOW`](/bigquery/docs/reference/standard-sql/query-syntax#window_clause) for window functions |
| Collation-supported [scalar functions](#collate_funcs) |
| Collation-supported [aggregate functions](#collate_funcs) |
| [Set operations](/bigquery/docs/reference/standard-sql/query-syntax#set_operators) |
| [`NULLIF` conditional expression](/bigquery/docs/reference/standard-sql/conditional_expressions#nullif) |

## Operations that propagate collation

Collation can pass through some query operations to other parts
of a query. When collation passes through an operation in a
query, this is known as *propagation*. During propagation:

* If an input contains no collation specification or an empty
  collation specification and another input contains an explicitly defined
  collation, the explicitly defined collation is used for all of the inputs.
* All inputs with a non-empty explicitly defined collation specification must
  have the same type of collation specification, otherwise an error is thrown.

GoogleSQL has several [functions](#functions_propagation),
[operators](#operators_propagation), and [expressions](#expressions_propagation)
that can propagate collation.

In the following example, the `'und:ci'` collation specification is propagated
from the `character` column to the `ORDER BY` operation.

```
-- With collation
SELECT *
FROM UNNEST([
  COLLATE('B', 'und:ci'),
  'b',
  'a'
]) AS character
ORDER BY character

/*-----------+
 | character |
 +-----------+
 | a         |
 | B         |
 | b         |
 +-----------*/
```

```
-- Without collation
SELECT *
FROM UNNEST([
  'B',
  'b',
  'a'
]) AS character
ORDER BY character

/*-----------+
 | character |
 +-----------+
 | B         |
 | a         |
 | b         |
 +-----------*/
```

### Functions

The following example functions propagate collation.

| Function | Notes |
| --- | --- |
| [`AEAD.DECRYPT_STRING`](/bigquery/docs/reference/standard-sql/aead_encryption_functions#aeaddecrypt_string) |  |
| [`ANY_VALUE`](/bigquery/docs/reference/standard-sql/aggregate_functions#any_value) |  |
| [`ARRAY_AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#array_agg) | Collation on input arguments are propagated as collation on the array element. |
| [`ARRAY_FIRST`](/bigquery/docs/reference/standard-sql/array_functions#array_first) |  |
| [`ARRAY_LAST`](/bigquery/docs/reference/standard-sql/array_functions#array_last) |  |
| [`ARRAY_SLICE`](/bigquery/docs/reference/standard-sql/array_functions#array_slice) |  |
| [`ARRAY_TO_STRING`](/bigquery/docs/reference/standard-sql/array_functions#array_to_string) | Collation on array elements are propagated to output. |
| [`COLLATE`](/bigquery/docs/reference/standard-sql/string_functions#collate) |  |
| [`CONCAT`](/bigquery/docs/reference/standard-sql/string_functions#concat) |  |
| [`FORMAT`](/bigquery/docs/reference/standard-sql/string_functions#format_string) | Collation from `format_string` to the returned string is propagated. |
| [`FORMAT_DATE`](/bigquery/docs/reference/standard-sql/date_functions#format_date) | Collation from `format_string` to the returned string is propagated. |
| [`FORMAT_DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#format_datetime) | Collation from `format_string` to the returned string is propagated. |
| [`FORMAT_TIME`](/bigquery/docs/reference/standard-sql/time_functions#format_time) | Collation from `format_string` to the returned string is propagated. |
| [`FORMAT_TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#format_timestamp) | Collation from `format_string` to the returned string is propagated. |
| [`GREATEST`](/bigquery/docs/reference/standard-sql/mathematical_functions#greatest) |  |
| [`LAG`](/bigquery/docs/reference/standard-sql/navigation_functions#lag) |  |
| [`LEAD`](/bigquery/docs/reference/standard-sql/navigation_functions#lead) |  |
| [`LEAST`](/bigquery/docs/reference/standard-sql/mathematical_functions#least) |  |
| [`LEFT`](/bigquery/docs/reference/standard-sql/string_functions#left) |  |
| [`LOWER`](/bigquery/docs/reference/standard-sql/string_functions#lower) |  |
| [`LPAD`](/bigquery/docs/reference/standard-sql/string_functions#lpad) |  |
| [`MAX`](/bigquery/docs/reference/standard-sql/aggregate_functions#max) |  |
| [`MIN`](/bigquery/docs/reference/standard-sql/aggregate_functions#min) |  |
| [`NET.HOST`](/bigquery/docs/reference/standard-sql/net_functions#nethost) |  |
| [`NET.PUBLIC_SUFFIX`](/bigquery/docs/reference/standard-sql/net_functions#netpublic_suffix) |  |
| [`NET.REG_DOMAIN`](/bigquery/docs/reference/standard-sql/net_functions#netreg_domain) |  |
| [`NTH_VALUE`](/bigquery/docs/reference/standard-sql/navigation_functions#nth_value) |  |
| [`NORMALIZE`](/bigquery/docs/reference/standard-sql/string_functions#normalize) |  |
| [`NORMALIZE_AND_CASEFOLD`](/bigquery/docs/reference/standard-sql/string_functions#normalize_and_casefold) |  |
| [`REPEAT`](/bigquery/docs/reference/standard-sql/string_functions#repeat) |  |
| [`REPLACE`](/bigquery/docs/reference/standard-sql/string_functions#replace) |  |
| [`REVERSE`](/bigquery/docs/reference/standard-sql/string_functions#reverse) |  |
| [`RIGHT`](/bigquery/docs/reference/standard-sql/string_functions#right) |  |
| [`RPAD`](/bigquery/docs/reference/standard-sql/string_functions#rpad) |  |
| [`SOUNDEX`](/bigquery/docs/reference/standard-sql/string_functions#soundex) |  |
| [`SPLIT`](/bigquery/docs/reference/standard-sql/string_functions#split) | Collation on input arguments are propagated as collation on the array element. |
| [`STRING_AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#string_agg) |  |
| [`SUBSTR`](/bigquery/docs/reference/standard-sql/string_functions#substr) |  |
| [`UPPER`](/bigquery/docs/reference/standard-sql/string_functions#upper) |  |

### Operators

The following example operators propagate collation.

| Operator | Notes |
| --- | --- |
| [`||` concatenation operator](/bigquery/docs/reference/standard-sql/operators#concatenation_operator) |  |
| [Array subscript operator](/bigquery/docs/reference/standard-sql/operators#array_subscript_operator) | Propagated to output. |
| [Set operators](/bigquery/docs/reference/standard-sql/query-syntax#set_operators) | Collation of an output column is decided by the collations of input columns at the same position. |
| [`STRUCT` field access operator](/bigquery/docs/reference/standard-sql/operators#field_access_operator) | When getting a `STRUCT`, collation on the `STRUCT` field is propagated as the output collation. |
| [`UNNEST`](/bigquery/docs/reference/standard-sql/query-syntax#unnest_operator) | Collation on the input array element is propagated to output. |

### Expressions

The following example expressions propagate collation.

| Expression | Notes |
| --- | --- |
| [`ARRAY`](/bigquery/docs/reference/standard-sql/data-types#array_type) | When you construct an `ARRAY`, collation on input arguments is propagated on the elements in the `ARRAY`. |
| [`CASE`](/bigquery/docs/reference/standard-sql/conditional_expressions#case) |  |
| [`CASE` expr](/bigquery/docs/reference/standard-sql/conditional_expressions#case_expr) |  |
| [`COALESCE`](/bigquery/docs/reference/standard-sql/conditional_expressions#coalesce) |  |
| [`IF`](/bigquery/docs/reference/standard-sql/conditional_expressions#if) |  |
| [`IFNULL`](/bigquery/docs/reference/standard-sql/conditional_expressions#ifnull) |  |
| [`NULLIF`](/bigquery/docs/reference/standard-sql/conditional_expressions#nullif) |  |
| [`STRUCT`](/bigquery/docs/reference/standard-sql/data-types#struct_type) | When you construct a `STRUCT`, collation on input arguments is propagated on the fields in the `STRUCT`. |

## Additional features that support collation

These features in BigQuery generally support collation:

| Feature | Notes |
| --- | --- |
| [Views](/bigquery/docs/views-intro) |  |
| [Materialized views](/bigquery/docs/materialized-views-intro) | This feature supports collation, but [limitations apply](#limitations) |
| [Table functions](/bigquery/docs/table-functions) | This feature supports collation, but [limitations apply](#limitations) |
| [BI engine](/bigquery/docs/bi-engine-intro) |  |

## Where you can assign a collation specification

You can assign a [collation specification](#collate_spec_details) to these
collation-supported types:

* A `STRING`
* A `STRING` field in a `STRUCT`
* A `STRING` element in an `ARRAY`

In addition:

* You can assign a default collation specification to a dataset when you
  create or alter it. This assigns a default collation specification to all
  future tables that are added to the dataset if the tables don't have their
  own default collation specifications.
* You can assign a default collation specification to a table when you create
  or alter it. This assigns a collation specification to all future
  collation-supported columns that are added to the table if the columns don't
  have collation specifications. This overrides a
  default collation specification on a dataset.
* You can assign a collation specification to a collation-supported type
  in a column. A column that contains a collation-supported type in its
  column dataset is a collation-supported column. This overrides a
  default collation specification on a table.
* You can assign a collation specification to a collation-supported
  query operation.
* You can assign a collation specification to a collation-supported expression
  with the `COLLATE` function. This overrides any collation specifications set
  previously.

In summary:

You can define a default collation specification for a dataset. For example:

```
CREATE SCHEMA (...)
DEFAULT COLLATE 'und:ci'
```

You can define a default collation specification for a table. For example:

```
CREATE TABLE (...)
DEFAULT COLLATE 'und:ci'
```

You can define a collation specification for a collation-supported column.
For example:

```
CREATE TABLE (
  case_insensitive_column STRING COLLATE 'und:ci'
)
```

You can specify a collation specification for a collation-supported expression
with the `COLLATE` function. For example:

```
SELECT COLLATE('a', 'und:ci') AS character
```

### DDL statements

You can assign a collation specification to the following DDL statements.

| Location | Support | Notes |
| --- | --- | --- |
| Dataset | [`CREATE SCHEMA`](/bigquery/docs/reference/standard-sql/data-definition-language#create_schema_statement) | Create a dataset and optionally add a default collation specification to the dataset. |
| Dataset | [`ALTER SCHEMA`](/bigquery/docs/reference/standard-sql/data-definition-language#alter_schema_collate_statement) | Updates the default collation specification for a dataset. |
| Table | [`CREATE TABLE`](/bigquery/docs/reference/standard-sql/data-definition-language#create_table_statement) | Create a table and optionally add a default collation specification to a table or a collation specification to a collation-supported type in a column.    You can't have collation on a column used with `CLUSTERING`. |
| Table | [`ALTER TABLE`](/bigquery/docs/reference/standard-sql/data-definition-language#alter_table_collate_statement) | Update the default collation specification for collation-supported type in a table. |
| Column | [`ADD COLUMN`](/bigquery/docs/reference/standard-sql/data-definition-language#alter_table_add_column_statement) | Add a collation specification to a collation-supported type in a new column in an existing table. |

### Data types

You can assign a collation specification to the following data types.

| Type | Notes |
| --- | --- |
| [`STRING`](/bigquery/docs/reference/standard-sql/data-types#string_type) | You can apply a collation specification directly to this data type. |
| [`STRUCT`](/bigquery/docs/reference/standard-sql/data-types#struct_type) | You can apply a collation specification to a `STRING` field in a `STRUCT`. A `STRUCT` can have `STRING` fields with different collation specifications. A `STRUCT` can only be used in comparisons with the following operators and conditional expressions: `=`, `!=`, `IN`, `NULLIF`, and `CASE`. |
| [`ARRAY`](/bigquery/docs/reference/standard-sql/data-types#array_type) | You can apply a collation specification to a `STRING` element in an `ARRAY`. An `ARRAY` can have `STRING` elements with different collation specifications. |

**Note:** Use the [`COLLATE`](/bigquery/docs/reference/standard-sql/string_functions#collate) function to apply a collation specification
to collation-supported expressions.

### Functions, operators, and conditional expressions

You can assign a collation specification to the following functions, operators,
and conditional expressions.

#### Functions

| Type | Support | Notes |
| --- | --- | --- |
| Scalar | [`COLLATE`](/bigquery/docs/reference/standard-sql/string_functions#collate) |  |
| Scalar | [`ENDS_WITH`](/bigquery/docs/reference/standard-sql/string_functions#ends_with) |  |
| Scalar | [`GREATEST`](/bigquery/docs/reference/standard-sql/mathematical_functions#greatest) |  |
| Scalar | [`INSTR`](/bigquery/docs/reference/standard-sql/string_functions#instr) |  |
| Scalar | [`LEAST`](/bigquery/docs/reference/standard-sql/mathematical_functions#least) |  |
| Scalar | [`REPLACE`](/bigquery/docs/reference/standard-sql/string_functions#replace) |  |
| Scalar | [`SPLIT`](/bigquery/docs/reference/standard-sql/string_functions#split) |  |
| Scalar | [`STARTS_WITH`](/bigquery/docs/reference/standard-sql/string_functions#starts_with) |  |
| Scalar | [`STRPOS`](/bigquery/docs/reference/standard-sql/string_functions#strpos) |  |
| Aggregate | [`COUNT`](/bigquery/docs/reference/standard-sql/aggregate_functions#count) | This operator is only affected by collation when the input includes the `DISTINCT` argument. |
| Aggregate | [`MAX`](/bigquery/docs/reference/standard-sql/aggregate_functions#max) |  |
| Aggregate | [`MIN`](/bigquery/docs/reference/standard-sql/aggregate_functions#min) |  |

#### Operators

| Support | Notes |
| --- | --- |
| [`<`](/bigquery/docs/reference/standard-sql/operators#comparison_operators) |  |
| [`<=`](/bigquery/docs/reference/standard-sql/operators#comparison_operators) |  |
| [`>`](/bigquery/docs/reference/standard-sql/operators#comparison_operators) |  |
| [`>=`](/bigquery/docs/reference/standard-sql/operators#comparison_operators) |  |
| [`=`](/bigquery/docs/reference/standard-sql/operators#comparison_operators) |  |
| [`!=`](/bigquery/docs/reference/standard-sql/operators#comparison_operators) |  |
| [`[NOT] BETWEEN`](/bigquery/docs/reference/standard-sql/operators#comparison_operators) |  |
| [`[NOT] IN`](/bigquery/docs/reference/standard-sql/operators#in_operators) | [Limitations apply](/bigquery/docs/reference/standard-sql/operators#in_operators). |
| [`[NOT] LIKE`](/bigquery/docs/reference/standard-sql/operators#like_operator) | [Limitations apply](/bigquery/docs/reference/standard-sql/operators#like_operator). |
| [Quantified `[NOT] LIKE`](/bigquery/docs/reference/standard-sql/operators#like_operator_quantified) | [Limitations apply](/bigquery/docs/reference/standard-sql/operators#like_operator_quantified). |

#### Conditional expressions

| Support |  |
| --- | --- |
| [`CASE`](/bigquery/docs/reference/standard-sql/conditional_expressions#case) |  |
| [`CASE` expr](/bigquery/docs/reference/standard-sql/conditional_expressions#case_expr) |  |
| [`NULLIF`](/bigquery/docs/reference/standard-sql/conditional_expressions#nullif) |  |

The preceding collation-supported operations
(functions, operators, and conditional expressions)
can include input with explicitly defined collation specifications for
collation-supported types. In a collation-supported operation:

* All inputs with a non-empty, explicitly defined collation specification must
  be the same, otherwise an error is thrown.
* If an input doesn't contain an explicitly defined collation
  and another input contains an explicitly defined collation, the
  explicitly defined collation is used for both.

For example:

```
-- Assume there's a table with this column declaration:
CREATE TABLE table_a
(
    col_a STRING COLLATE 'und:ci',
    col_b STRING COLLATE '',
    col_c STRING,
    col_d STRING COLLATE 'und:ci'
);

-- This runs. Column 'b' has a collation specification and the
-- column 'c' doesn't.
SELECT STARTS_WITH(col_b_expression, col_c_expression)
FROM table_a;

-- This runs. Column 'a' and 'd' have the same collation specification.
SELECT STARTS_WITH(col_a_expression, col_d_expression)
FROM table_a;

-- This runs. Even though column 'a' and 'b' have different
-- collation specifications, column 'b' is considered the default collation
-- because it's assigned to an empty collation specificat
```