* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Lexical structure and syntax Stay organized with collections Save and categorize content based on your preferences.

A GoogleSQL statement comprises a series of tokens. Tokens include
identifiers, quoted identifiers, literals, keywords, operators, and
special characters. You can separate tokens with comments or whitespace such
as spaces, backspaces, tabs, or newlines.

## Identifiers

Identifiers are names that are associated with columns, tables,
fields, path expressions, and more. They can be
[unquoted](#unquoted_identifiers) or [quoted](#quoted_identifiers) and some
are [case-sensitive](#case_sensitivity).

### Unquoted identifiers

* Must begin with a letter or an underscore (\_) character.
* Subsequent characters can be letters, numbers, or underscores (\_).

### Quoted identifiers

* Must be enclosed by backtick (`) characters.
* Can't be empty.
* Have the same escape sequences as [string literals](#string_and_bytes_literals).
* If an identifier is the same as a [reserved keyword](#reserved_keywords), the
  identifier must be quoted. For example, the identifier `FROM` must be quoted.
  Additional rules apply for [path expressions](#path_expressions)
  ,
  [table names](#table_names), [column names](#column_names), and
  [field names](#field_names).

### Identifier examples

Path expression examples:

```
-- Valid. _5abc and dataField are valid identifiers.
_5abc.dataField

-- Valid. `5abc` and dataField are valid identifiers.
`5abc`.dataField

-- Invalid. 5abc is an invalid identifier because it's unquoted and starts
-- with a number rather than a letter or underscore.
5abc.dataField

-- Valid. abc5 and dataField are valid identifiers.
abc5.dataField

-- Invalid. abc5! is an invalid identifier because it's unquoted and contains
-- a character that isn't a letter, number, or underscore.
abc5!.dataField

-- Valid. `GROUP` and dataField are valid identifiers.
`GROUP`.dataField

-- Invalid. GROUP is an invalid identifier because it's unquoted and is a
-- stand-alone reserved keyword.
GROUP.dataField

-- Valid. abc5 and GROUP are valid identifiers.
abc5.GROUP
```

Function examples:

```
-- Valid. dataField is a valid identifier in a function called foo().
foo().dataField
```

Array access operation examples:

```
-- Valid. dataField is a valid identifier in an array called items.
items[OFFSET(3)].dataField
```

Named query parameter examples:

```
-- Valid. param and dataField are valid identifiers.
@param.dataField
```

Table name examples:

```
-- Valid table path.
myproject.mydatabase.mytable287
```

```
-- Valid table path.
myproject287.mydatabase.mytable
```

```
-- Invalid table path. The project name starts with a number and is unquoted.
287myproject.mydatabase.mytable
```

```
-- Invalid table name. The table name is unquoted and isn't a valid
-- dashed identifier, as the part after the dash is neither a number nor
-- an identifier starting with a letter or an underscore.
mytable-287a
```

```
-- Valid table path.
my-project.mydataset.mytable
```

```
-- Valid table name.
my-table
```

```
-- Invalid table path because the dash isn't in the first part
-- of the path.
myproject.mydataset.my-table
```

```
-- Invalid table path because a dataset name can't contain dashes.
my-dataset.mytable
```

## Path expressions

A path expression describes how to navigate to an object in a graph of objects
and generally follows this structure:

```
path:
  [path_expression][. ...]

path_expression:
  [first_part]/subsequent_part[ { / | : | - } subsequent_part ][...]

first_part:
  { unquoted_identifier | quoted_identifier }

subsequent_part:
  { unquoted_identifier | quoted_identifier | number }
```

* `path`: A graph of one or more objects.
* `path_expression`: An object in a graph of objects.
* `first_part`: A path expression can start with a quoted or
  unquoted identifier. If the path expressions starts with a
  [reserved keyword](#reserved_keywords), it must be a quoted identifier.
* `subsequent_part`: Subsequent parts of a path expression can include
  non-identifiers, such as reserved keywords. If a subsequent part of a
  path expressions starts with a [reserved keyword](#reserved_keywords), it
  may be quoted or unquoted.

Examples:

```
foo.bar
foo.bar/25
foo/bar:25
foo/bar/25-31
/foo/bar
/25/foo/bar
```

## Table names

A table name represents the name of a table.

* Table names can be quoted identifiers or unquoted identifiers.
* A table name that's an unquoted identifier can additionally include
  single dashes if the table name is referenced in a `FROM` or `TABLE` clause.
  Only the first identifier in the table path (the project ID or the table name)
  can have dashes. Dashes aren't supported in datasets.
* A table name can be a
  [fully qualified table name (table path)](/bigquery/docs/reference/standard-sql/data-definition-language#table_path)
  that includes up to three quoted or unquoted identifiers:

  + An optional [project ID](/resource-manager/docs/creating-managing-projects#before_you_begin)
  + An optional [dataset name](/bigquery/docs/datasets#dataset-naming)
  + A required table name.

  For example: `myproject.mydataset.mytable`
* Table names can be path expressions.
* Table names have [case-sensitivity rules](#case_sensitivity).
* Table names have [additional rules](/bigquery/docs/tables#table_naming).

Examples:

```
my-project.mydataset.mytable
mydataset.mytable
my-table
mytable
`287mytable`
```

## Column names

A column name represents the name of a column in a table. Column names can be
quoted identifiers or unquoted identifiers. Column names also
have [additional rules](/bigquery/docs/schemas#column_names).

Examples:

```
columnA
`column-a`
`287column`
```

## Field names

A field name represents the name of a field inside a complex data type such
as a struct or
JSON object.

* A field name can be a quoted identifier or an unquoted identifier.
* Field names must adhere to all of the rules for column names.

## Literals

A literal represents a constant value of a built-in data type. Some, but not
all, data types can be expressed as literals.

### String and bytes literals

A string literal represents a constant value of the
[string data type](/bigquery/docs/reference/standard-sql/data-types#string_type). A bytes literal represents a
constant value of the [bytes data type](/bigquery/docs/reference/standard-sql/data-types#bytes_type).

Both string and bytes literals must be *quoted*, either with single (`'`) or
double (`"`) quotation marks, or *triple-quoted* with groups of three single
(`'''`) or three double (`"""`) quotation marks.

#### Formats for quoted literals

The following table lists all of the ways you can format a quoted literal.

| Literal | Examples | Description |
| --- | --- | --- |
| Quoted string | * `"abc"` * `"it's"` * `'it\'s'` * `'Title: "Boy"'` | Quoted strings enclosed by single (`'`) quotes can contain unescaped double (`"`) quotes, as well as the inverse.  Backslashes (`\`) introduce escape sequences. See the Escape Sequences table below. Quoted strings can't contain newlines, even when preceded by a backslash (`\`). |
| Triple-quoted string | * `"""abc"""` * `'''it's'''` * `'''Title:"Boy"'''` * `'''two lines'''` * `'''why\?'''` | Embedded newlines and quotes are allowed without escaping - see fourth example. Backslashes (`\`) introduce escape sequences. See Escape Sequences table below. A trailing unescaped backslash (`\`) at the end of a line isn't allowed. End the string with three unescaped quotes in a row that match the starting quotes. |
| Raw string | * `r"abc+"` * `r'''abc+'''` * `r"""abc+"""` * `r'f\(abc,(.*),def\)'` | Quoted or triple-quoted literals that have the raw string literal prefix (`r` or `R`) are interpreted as raw strings (sometimes described as regex strings). Backslash characters (`\`) don't act as escape characters. If a backslash followed by another character occurs inside the string literal, both characters are preserved. A raw string can't end with an odd number of backslashes. Raw strings are useful for constructing regular expressions. The prefix is case-insensitive. |
| Bytes | * `B"abc"` * `B'''abc'''` * `b"""abc"""` | Quoted or triple-quoted literals that have the bytes literal prefix (`b` or `B`) are interpreted as bytes. |
| Raw bytes | * `br'abc+'` * `RB"abc+"` * `RB'''abc'''` | A bytes literal can be interpreted as raw bytes if both the `r` and `b` prefixes are present. These prefixes can be combined in any order and are case-insensitive. For example, `rb'abc*'` and `rB'abc*'` and `br'abc*'` are all equivalent. See the description for raw string to learn more about what you can do with a raw literal. |

Like in many other languages, such as Python and C++, you can divide a
GoogleSQL string or bytes literal into chunks, each with its own quoting
or raw specification. The literal value is the concatenation of all these parts.

This is useful for a variety of purposes, including readability, organization,
formatting and maintainability, for example:

* You can break a literal into multiple chunks fit into a width of 80
  characters.
* You can break a literal into chunks of different quotings and raw
  specifications to avoid escaping. For example, a string value inside a
  `JSON` string.
* You can change only one part of a literal through a macro, while the rest of
  the literal is unchanged.
* You can use string literal concatenation in other literals that include
  strings such as `DATE`, `TIMESTAMP`, `JSON`, etc.

The following restrictions apply to these literal concatenations:

* You can't mix string and byte literals.
* You must ensure there is some separation between the concatenated parts,
  such as whitespace or comments.
* `r` specifiers apply only to the immediate chunk, not the rest of the
  literal parts.
* Quoted identifiers don't concatenate.

Examples:

| Literals divided into chunks | Equivalent literals |
| --- | --- |
| ``` SELECT  r'\n' /*Only the prev is raw!*/ '\n' "b" """c"d"e""" '''f'g'h''' "1" "2",  br'\n'/*Only the prev is raw!*/ b'\n' b"b" b"""c"d"e""" b'''f'g'h''' b"1" b"2",   NUMERIC "1" r'2',   DECIMAL /*whole:*/ '1' /*fractional:*/ ".23" /*exponent=*/ "e+6",   BIGNUMERIC '1' r"2",   BIGDECIMAL /*sign*/ '-' /*whole:*/ '1' /*fractional:*/ ".23" /*exponent=*/ "e+6",   RANGE<DATE> '[2014-01-01,' /*comment*/ "2015-01-01)",   DATE '2014' "-01-01",   DATETIME '2016-01-01 ' r"12:00:00",   TIMESTAMP '2018-10-01 ' "12:00:00+08" ``` | ``` SELECT  "\\n\nbc\"d\"ef'g'h12",  b"\\n\nbc\"d\"ef'g'h12",   NUMERIC "12",   DECIMAL '1.23e+6',   BIGNUMERIC '12',   BIGDECIMAL "-1.23e+6",   RANGE<DATE> '[2014-01-01 2015-01-01)',   DATE '2014-01-01',   DATETIME '2016-01-01 12:00:00',   TIMESTAMP "2018-10-01 12:00:00+08" ``` |

#### Escape sequences for string and bytes literals

The following table lists all valid escape sequences for representing
non-alphanumeric characters in string and bytes literals. Any sequence not in
this table produces an error.

| Escape Sequence | Description |
| --- | --- |
| `\a` | Bell |
| `\b` | Backspace |
| `\f` | Formfeed |
| `\n` | Newline |
| `\r` | Carriage Return |
| `\t` | Tab |
| `\v` | Vertical Tab |
| `\\` | Backslash (`\`) |
| `\?` | Question Mark (`?`) |
| `\"` | Double Quote (`"`) |
| `\'` | Single Quote (`'`) |
| `` \` `` | Backtick (`` ` ``) |
| `\ooo` | Octal escape, with exactly 3 digits (in the range 0–7). Decodes to a single Unicode character (in string literals) or byte (in bytes literals). |
| `\xhh` or `\Xhh` | Hex escape, with exactly 2 hex digits (0–9 or A–F or a–f). Decodes to a single Unicode character (in string literals) or byte (in bytes literals). Examples:  * `'\x41'` == `'A'` * `'\x41B'` is `'AB'` * `'\x4'` is an error |
| `\uhhhh` | Unicode escape, with lowercase 'u' and exactly 4 hex digits. Valid only in string literals or identifiers. Note that the range D800-DFFF isn't allowed, as these are surrogate unicode values. |
| `\Uhhhhhhhh` | Unicode escape, with uppercase 'U' and exactly 8 hex digits. Valid only in string literals or identifiers. The range D800-DFFF isn't allowed, as these values are surrogate unicode values. Also, values greater than 10FFFF aren't allowed. |

### Integer literals

Integer literals are either a sequence of decimal digits (0–9) or a hexadecimal
value that's prefixed with "`0x`" or "`0X`". Integers can be prefixed by "`+`"
or "`-`" to represent positive and negative values, respectively.
Examples:

```
123
0xABC
-123
```

An integer literal is interpreted as an `INT64`.

A integer literal represents a constant value of the
[integer data type](/bigquery/docs/reference/standard-sql/data-types#integer_types).

### `NUMERIC` literals

You can construct `NUMERIC` literals using the
`NUMERIC` keyword followed by a floating point value in quotes.

Examples:

```
SELECT NUMERIC '0';
SELECT NUMERIC '123456';
SELECT NUMERIC '-3.14';
SELECT NUMERIC '-0.54321';
SELECT NUMERIC '1.23456e05';
SELECT NUMERIC '-9.876e-3';
```

A `NUMERIC` literal represents a constant value of the
[`NUMERIC` data type](/bigquery/docs/reference/standard-sql/data-types#decimal_types).

### `BIGNUMERIC` literals

You can construct `BIGNUMERIC` literals using the `BIGNUMERIC` keyword followed
by a floating point value in quotes.

Examples:

```
SELECT BIGNUMERIC '0';
SELECT BIGNUMERIC '123456';
SELECT BIGNUMERIC '-3.14';
SELECT BIGNUMERIC '-0.54321';
SELECT BIGNUMERIC '1.23456e05';
SELECT BIGNUMERIC '-9.876e-3';
```

A `BIGNUMERIC` literal represents a constant value of the
[`BIGNUMERIC` data type](/bigquery/docs/reference/standard-sql/data-types#decimal_types).

### Floating point literals

Syntax options:

```
[+-]DIGITS.[DIGITS][e[+-]DIGITS]
[+-][DIGITS].DIGITS[e[+-]DIGITS]
DIGITSe[+-]DIGITS
```

`DIGITS` represents one or more decimal numbers (0 through 9) and `e` represents
the exponent marker (e or E).

Examples:

```
123.456e-67
.1E4
58.
4e2
```

Numeric literals that contain
either a decimal point or an exponent marker are presumed to be type double.

Implicit coercion of floating point literals to float type is possible if the
value is within the valid float range.

There is no literal
representation of NaN or infinity, but the following case-insensitive strings
can be explicitly cast to float:

* "NaN"
* "inf" or "+inf"
* "-inf"

A floating-point literal represents a constant value of the
[floating-point data type](/bigquery/docs/reference/standard-sql/data-types#floating_point_types).

### Array literals

Array literals are comma-separated lists of elements
enclosed in square brackets. The `ARRAY` keyword is optional, and an explicit
element type T is also optional.

Examples:

```
[1, 2, 3]
['x', 'y', 'xy']
ARRAY[1, 2, 3]
ARRAY<STRING>['x', 'y', 'xy']
ARRAY<INT64>[]
```

An array literal represents a constant value of the
[array data type](/bigquery/docs/reference/standard-sql/data-types#array_type).

### Struct literals

A struct literal is a struct whose fields are all literals. Struct literals can
be written using any of the syntaxes for [constructing a
struct](/bigquery/docs/reference/standard-sql/data-types#constructing_a_struct) (tuple syntax, typeless struct syntax, or typed
struct syntax).

Note that tuple syntax requires at least two fields, in order to distinguish it
from an ordinary parenthesized expression. To write a struct literal with a
single field, use typeless struct syntax or typed struct syntax.

| Example | Output Type |
| --- | --- |
| `(1, 2, 3)` | `STRUCT<INT64, INT64, INT64>` |
| `(1, 'abc')` | `STRUCT<INT64, STRING>` |
| `STRUCT(1 AS foo, 'abc' AS bar)` | `STRUCT<foo INT64, bar STRING>` |
| `STRUCT<INT64, STRING>(1, 'abc')` | `STRUCT<INT64, STRING>` |
| `STRUCT(1)` | `STRUCT<INT64>` |
| `STRUCT<INT64>(1)` | `STRUCT<INT64>` |

A struct literal represents a constant value of the
[struct data type](/bigquery/docs/reference/standard-sql/data-types#struct_type).

### Date literals

Syntax:

```
DATE 'date_canonical_format'
```

Date literals contain the `DATE` keyword followed by
[`date_canonical_format`](/bigquery/docs/reference/standard-sql/data-types#canonical_format_for_date_literals),
a string literal that conforms to the canonical date format, enclosed in single
quotation marks. Date literals support a range between the
years 1 and 9999, inclusive. Dates outside of this range are invalid.

For example, the following date literal represents September 27, 2014:

```
DATE '2014-09-27'
```