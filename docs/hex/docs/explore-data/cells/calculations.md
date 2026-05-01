On this page

# Calculations

Use Calculations to write spreadsheet-style formulas.

info

Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there).

Hex calculations allow you to write ad-hoc formulas using a familiar spreadsheet interface. Creating a formula will add a new column to your table.

Calculations can be created wherever you use Tables (in a Table Display cell, the Table tab of a SQL/Chart cell, or in [Explore](/docs/share-insights/explore#calculations)). To get started, click the **+** icon at the right of a table. The formula bar will open and a new column will appear on the right. Then, type a formula using the syntax in the language documentation below. To reference columns, begin typing to bring up a list of matching column names. Use the arrow keys to move up and down the suggestions list, and select the desired column by hitting `Tab` or `Enter`. Alternatively, click a column in the table to reference it in your formula.

A preview of your calculated values will be rendered as you type. Hit `Enter` or `⌘ + Enter` to run the calculation in earnest. The calculation will be applied to every row in the table.

[](/assets/medias/calcs-example-c4b64e8dea5bcc13be9cebe97239556c.mp4)

To edit an existing calculation, either click the **fx** icon in the column header or click the column's header and select **Edit formula…**.

[](/assets/medias/calcs-edit-formula-b7564d9de39dfe4d4639210a52eef934.mp4)

Calculated columns can be filtered, formatted, and sorted, just like a regular column. If a cell with a calculation has a cell-level filter applied to it, the calculation will run before the filter is applied.

[](/assets/medias/calcs-column-actions-2103df7e085ec690eb9afd7c885ad037.mp4)

## Formulas[​](#formulas "Direct link to Formulas")

The Hex calculation language is designed to be familiar to spreadsheet users. You can perform basic arithmetic using mathematical operators:

```
numerator / denominator
```

You can compose functions to perform more sophisticated logic:

```
If(end_date < Today(), 'Closed', 'Active')
```

The data types, operators, and functions that are available in the Hex calculation language are documented below.

## Parameterized calculations[​](#parameterized-calculations "Direct link to Parameterized calculations")

It's possible to make calculations dynamic based on project variables. You can use Jinja to reference Python variables in calculation formulas.

Variables can be referenced in a formula using syntax like the following: `{{variable_name}}`. See [Using Jinja](/docs/explore-data/cells/using-jinja) for more details on Jinja usage.

warning

Complex jinja logic such as if statements, for loops, and references to lists are not supported.

Changing an input parameter upstream will reactively update parameterized calculations downstream.

[](/assets/medias/parameterized-calculation-updating-205323f66171f8bec41fe9c40ed3a211.mp4)

## Data types[​](#data-types "Direct link to Data types")

The calculation language presents four data types: **Text**, **Number**, **Boolean**, and **Datetime**. They map to the underlying dataframe data types as follows:

| Calcs Type | Pandas Type | SQL Type | Example Literals |
| --- | --- | --- | --- |
| Text | object | `VARCHAR`, `CHAR` | 'Hello!', '', null |
| Number | int64, float64 | `INT`, `BIGINT`, `SMALLINT`, `FLOAT`, `DOUBLE`, `DECIMAL` | 42, -42.0, 2.5e12, null |
| Boolean | bool | `BOOLEAN` | True, False, null |
| Datetime | datetime64 | `DATE`, `DATETIME`, `TIMESTAMP` | '2020-01-28 04:08:10', null |

## Operators[​](#operators "Direct link to Operators")

##### + - / \* ^ %[​](#------ "Direct link to + - / * ^ %")

Performs arithmetic between two numbers.

`/` always produces a float, and never truncates. Division by zero produces null.

`^` raises one number to the power of another number.

`%` (modulo) returns the remainder when dividing one number by another.

> `number`

##### AND, OR, NOT[​](#and-or-not "Direct link to AND, OR, NOT")

Logical operators for combining or negating boolean values. OR is inclusive.

AND or OR are also available as `&&` and `||` respectively.
NOT is also available as `!`.

> `boolean`

##### =, !=, <, <=, >, >=[​](#----- "Direct link to =, !=, <, <=, >, >=")

Compares a value to another. Equals and not-equals work on any value types. Only numbers and datetime values can be used for `<`, `<=`, `>` and `>=` comparisons.

Values with different data types can not be compared.

Equals and not-equals are also available as `==` and `<>` respectively.

> `boolean`

##### &

Concatenates two or more text values.

> `text`
>
> > `'Jane' & ' ' & 'Doe'` → 'Jane Doe'

## Functions[​](#functions "Direct link to Functions")

### 📝 Text[​](#-text "Direct link to 📝 Text")

##### Concat(text\_1, ..., text\_n)[​](#concattext_1--text_n "Direct link to Concat(text_1, ..., text_n)")

Concatenates multiple `text` values together into one. Equivalent to the `&` operator.

* `text` : A text value to concatenate. Any number of additional text values
  can be added.

> `text`
>
> > `Concat('Jane', ' ', 'Doe')` → 'Jane Doe'

##### Length(text)[​](#lengthtext "Direct link to Length(text)")

Counts the number of characters in `text`.

* `text` : A text value to measure the length of.

> `number`
>
> > `Length('Hex')` → 3

##### Left(text, n)[​](#lefttext-n "Direct link to Left(text, n)")

Returns the first `n` characters of `text`.

* `text` : A text value to take the first n characters of.
* `n` : The number of characters to take.

> `text`
>
> > `Left('abcd', 3)` → 'abc'

##### Right(text, n)[​](#righttext-n "Direct link to Right(text, n)")

Returns the last `n` characters of `text`.

* `text` : A text value to take the last n characters of.
* `n` : The number of characters to take.

> `text`
>
> > `Right('abcd', 3)` → 'bcd'

##### Lower(text)[​](#lowertext "Direct link to Lower(text)")

Converts a text value to lowercase.

* `text` : A text value to make lowercase.

> `text`
>
> > `Lower('Jane Doe')` → 'jane doe'

##### Upper(text)[​](#uppertext "Direct link to Upper(text)")

Converts a text value to uppercase.

* `text` : A text value to make uppercase.

> `text`
>
> > `Upper('Jane Doe')` → 'JANE DOE'

##### Contains(text, search\_text)[​](#containstext-search_text "Direct link to Contains(text, search_text)")

Returns True if `text` contains `search_text`, and False otherwise.

* `text` : A text value to search in.
* `search_text` : A text literal to search for within text. Cannot be an expression or reference.

> `boolean`
>
> > `Contains('abcd', 'abc')` → True

##### StartsWith(text, search\_text)[​](#startswithtext-search_text "Direct link to StartsWith(text, search_text)")

Returns True if `text` starts with `search_text`, and False otherwise.

* `text` : A text value to search in.
* `search_text` : A text literal to search for at the start of text. Cannot be an expression or reference.

> `boolean`
>
> > `StartsWith('abcd', 'abc')` → True

##### EndsWith(text, search\_text)[​](#endswithtext-search_text "Direct link to EndsWith(text, search_text)")

Returns True if `text` ends with `search_text`, and False otherwise.

* `text` : A text value to search in.
* `search_text` : A text literal to search for at the end of text. Cannot be an expression or reference.

> `boolean`
>
> > `EndsWith('abcd', 'bcd')` → True

##### Substitute(value, search\_text, replacement\_text)[​](#substitutevalue-search_text-replacement_text "Direct link to Substitute(value, search_text, replacement_text)")

Changes all occurrences of `search_text` in `value` to be `replacement_text`.

* `value` : A value to search in.
* `search_text` : A sub-value to search for inside of `value`.
* `replacement_text` : The value to replace `search_text` with.

> `text`
>
> > `Substitute('abcabc', 'bc', 'BC')` → 'aBCaBC'

##### SplitPart(text, delimiter, part\_number)[​](#splitparttext-delimiter-part_number "Direct link to SplitPart(text, delimiter, part_number)")

Splits `text` into separate parts separated by `delimiter` and returns the `part_number` part.

`SplitPart` is only available in [Explore](/docs/share-insights/explore).

* `text` : A text value to concatenate. Any number of additional text values
  can be added.
* `delimiter` : A text value to split the text along.
* `part_number` : The part number to select.

> `text`
>
> > `SplitPart("[email protected]", "@", 1)` → 'jane'

### 🧮 Math[​](#-math "Direct link to 🧮 Math")

##### Abs(number)[​](#absnumber "Direct link to Abs(number)")

Computes the absolute value of `number`.

* `number` : A number to take the absolute value of.

> `number`
>
> > `Abs(-3)` → 3

##### Ceiling(number)[​](#ceilingnumber "Direct link to Ceiling(number)")

Rounds up `number` to the nearest integer.

* `number` : A number to round up.

> `number`
>
> > `Ceiling(3.14)` → 4

##### Floor(number)[​](#floornumber "Direct link to Floor(number)")

Rounds down `number` to the nearest integer.

* `number` : A number to round down.

> `number`
>
> > `Floor(3.14)` → 3

##### Power(number, power)[​](#powernumber-power "Direct link to Power(number, power)")

Raises `number` to the power of `power`. Functionally equivalent to `^`.

* `number` : A number to raise by the power of power.
* `power` : The power to raise number by.

> `number`
>
> > `Power(3, 2)` → 9

##### Sqrt(number)[​](#sqrtnumber "Direct link to Sqrt(number)")

Takes the square root of `number`.

* `number` : The number to take the square root of.

> `number`
>
> > `Sqrt(9)` → 3

##### Exp(power)[​](#exppower "Direct link to Exp(power)")

Raises the mathematical constant **e** to the power of `power`.

* `power` : The power to raise e by.

> `number`
>
> > `Exp(1)` → 2.718281828459045

##### Round(number)[​](#roundnumber "Direct link to Round(number)")

Rounds `number` up or down to the nearest integer.

* `number` : The number to round.

> `number`
>
> > `Round(3.14)` → 3

### 🔀 Logical[​](#-logical "Direct link to 🔀 Logical")

##### If(condition, value\_if\_true, value\_if\_otherwise)[​](#ifcondition-value_if_true-value_if_otherwise "Direct link to If(condition, value_if_true, value_if_otherwise)")

Returns `value_if_true` if `condition` is True, and `value_if_otherwise` otherwise.

* `condition` : An expression resulting in True or False.
* `value_if_true` : A value to return if condition is True.
* `value_if_otherwise` : A value to return if condition is not True. Must be the same data type as value\_if\_true.

> `text`, `number`, `boolean`, `datetime`
>
> > `If(num % 2 = 0, 'Even', 'Odd')`

##### Switch(switch\_value, if\_matches\_1, result\_1, ..., if\_matches\_n, result\_n)[​](#switchswitch_value-if_matches_1-result_1--if_matches_n-result_n "Direct link to Switch(switch_value, if_matches_1, result_1, ..., if_matches_n, result_n)")

A more succinct and readable way of nesting many `If()` statements based on one single input value. Returns the result value corresponding to the paired if\_matches value that equals the switch\_value.

* `switch_value` : The value to compare against all the if\_matches values.
* `if_matches_1` : The first value to compare against switch\_value. If they are equal, the function returns result\_1. Otherwise, it compares switch\_value to the next if\_matches value.
* `result_1` : The value to return if switch\_value equals if\_matches\_1.

> `text`, `number`, `boolean`, `datetime`
>
> > `Switch(status_code, 1, 'Processing', 2, 'Confirmed', 3, 'Shipped', 4, 'Delivered')`

##### Coalesce(value\_1, ..., value\_n)[​](#coalescevalue_1--value_n "Direct link to Coalesce(value_1, ..., value_n)")

Returns the first non-null `value`.

* `value_1` : A value to return if not null. If null, the next value input is considered, and so on.

> `text`, `number`, `boolean`, `datetime`
>
> > `Coalesce(null, 0, 42)` → 0

##### IsFinite(number)[​](#isfinitenumber "Direct link to IsFinite(number)")

Returns True if `number` is not ***null***, not ***NaN***, and not ***Inf***. Otherwise, returns False.

* `number` : A number to check for being finite.

> `boolean`
>
> > `IsFinite(42)` → True

##### IsOneOf(value, match\_1, ..., match\_n)[​](#isoneofvalue-match_1--match_n "Direct link to IsOneOf(value, match_1, ..., match_n)")

Returns True if `value` equals any of `match`.

* `value` : A `value` to compare against all the `match` values.
* `match_1` : The first value to compare against value. If they are equal, the function returns True. Otherwise, it compares value to the next match value.

> `boolean`
>
> > `IsOneOf(1, 2, 3, 4)` → False (1 is not equal to 2, 3, or 4)

##### IsNull(value)[​](#isnullvalue "Direct link to IsNull(value)")

Returns True if `value` is null, and False otherwise.

* `value` : A text, number, boolean, or datetime value to check for being null.

> `boolean`
>
> > `IsNull(null)` → True

### 🪄 Casting[​](#-casting "Direct link to 🪄 Casting")

##### ToText(number)[​](#totextnumber "Direct link to ToText(number)")

Converts `number` into a text data type.

* `number` : A number to convert to text.

> `text`
>
> > `ToText(123)` → '123'

##### ToNumber(text)[​](#tonumbertext "Direct link to ToNumber(text)")

Converts `text` into a number data type.

* `text` : A text value to convert to a number.

> `number`
>
> > `ToNumber('123')` → 123

##### ToDatetime(text)[​](#todatetimetext "Direct link to ToDatetime(text)")

Converts `text` into a datetime data type.

* `text` : A text value to convert to a datetime.

> `datetime`
>
> > `ToDatetime('2024-02-19')` → 2024-02-19T00:00:00

##### ToBoolean(number)[​](#tobooleannumber "Direct link to ToBoolean(number)")

Converts `number` into a boolean data type, where 0 is False and 1 is True.

* `number` : A number to convert to a boolean.

> `boolean`
>
> > `ToBoolean(0)` → False

### 📅 Date & Time[​](#-date--time "Direct link to 📅 Date & Time")

##### Year(datetime), Quarter(datetime), Month(datetime), Day(datetime), Hour(datetime), Minute(datetime), Second(datetime), Millisecond(datetime)[​](#yeardatetime-quarterdatetime-monthdatetime-daydatetime-hourdatetime-minutedatetime-seconddatetime-milliseconddatetime "Direct link to Year(datetime), Quarter(datetime), Month(datetime), Day(datetime), Hour(datetime), Minute(datetime), Second(datetime), Millisecond(datetime)")

Extracts the date part specified in the function name from `datetime`.

* `datetime` : A datetime value to extract from.

> `number`
>
> > `Day('2024-02-14')` → 14

##### TruncYear(datetime), TruncQuarter(datetime), TruncMonth(datetime), TruncWeek(datetime), TruncWeekMonday(datetime), TruncDay(datetime), TruncHour(datetime), TruncMinute(datetime), TruncSecond(datetime)[​](#truncyeardatetime-truncquarterdatetime-truncmonthdatetime-truncweekdatetime-truncweekmondaydatetime-truncdaydatetime-trunchourdatetime-truncminutedatetime-truncseconddatetime "Direct link to TruncYear(datetime), TruncQuarter(datetime), TruncMonth(datetime), TruncWeek(datetime), TruncWeekMonday(datetime), TruncDay(datetime), TruncHour(datetime), TruncMinute(datetime), TruncSecond(datetime)")

Truncates `datetime` down to the nearest datepart as specified in the function name.

`TruncWeekMonday` is only available in [Explore](/docs/share-insights/explore).

* `datetime` : A datetime value to be truncated.

> `datetime`
>
> > `TruncMonth('2024-02-14 10:31:50')` → 2024-02-01 00:00:00

##### DiffDays(start\_datetime, end\_datetime), DiffHours(start\_datetime, end\_datetime), DiffMinutes(start\_datetime, end\_datetime), DiffSeconds(start\_datetime, end\_datetime), DiffMilliseconds(start\_datetime, end\_datetime)[​](#diffdaysstart_datetime-end_datetime-diffhoursstart_datetime-end_datetime-diffminutesstart_datetime-end_datetime-diffsecondsstart_datetime-end_datetime-diffmillisecondsstart_datetime-end_datetime "Direct link to DiffDays(start_datetime, end_datetime), DiffHours(start_datetime, end_datetime), DiffMinutes(start_datetime, end_datetime), DiffSeconds(start_datetime, end_datetime), DiffMilliseconds(start_datetime, end_datetime)")

Calculates the amount of time between `start_datetime` and `end_datetime`. If `start_datetime` is after `end_datetime`, the result will be negative.

* `start_datetime` : A datetime value to calculate from.
* `end_datetime` : A datetime value to subtract from `start_datetime`.

> `number`
>
> > `DiffSeconds('2024-02-03 04:05:06', '2024-02-03 04:05:08')` → 2

##### DayOfWeek(datetime)[​](#dayofweekdatetime "Direct link to DayOfWeek(datetime)")

Extracts the day of the week from `datetime` (1 for Sunday, 7 for Saturday).

* `datetime` : A datetime value to extract from.

> `number`
>
> > `DayOfWeek('2024-01-02')` → 3

##### Now()[​](#now "Direct link to Now()")

Returns the current date and time.

> `datetime`
>
> > `Now()` → 2024-02-15 13:04:56

##### Today()[​](#today "Direct link to Today()")

Returns the current date.

> `datetime`
>
> > `Today()` → 2024-02-15

### ➕ Aggregates[​](#-aggregates "Direct link to ➕ Aggregates")

##### Avg(number)[​](#avgnumber "Direct link to Avg(number)")

Computes the mean of the input column.

* `number` : A numeric column you want to compute the average of.

> `number`
>
> > `Avg(column)` → 2.53

##### Count(column)[​](#countcolumn "Direct link to Count(column)")

Counts the number of all values in the input column.

* `column` : A column (of any type) whose values you want to count.

> `number`
>
> > `Count(column)` → 1640

##### CountDistinct(column)[​](#countdistinctcolumn "Direct link to CountDistinct(column)")

Counts the number of unique values in the input column.

* `column` : A column (of any type) whose values you want to count.

> `number`
>
> > `CountDistinct(column)` → 1201

##### Max(column)[​](#maxcolumn "Direct link to Max(column)")

Returns the value in the input column that would come first if it were sorted descending.

* `column` : A column (of any type) you want to compute the maximum of.

> `text`, `number`, `boolean`, `datetime`
>
> > `Max(column)` → 5007

##### Median(number)[​](#mediannumber "Direct link to Median(number)")

Returns the median number from the input column.

* `number` : A numeric column you want to compute the median of.

> `number`
>
> > `Median(column)` → 52

##### Min(column)[​](#mincolumn "Direct link to Min(column)")

Returns the value in the input column that would come first if it were sorted ascending.

* `column` : A column (of any type) you want to compute the minimum of.

> `text`, `number`, `boolean`, `datetime`
>
> > `Min(column)` → -47

##### StdDev(number)[​](#stddevnumber "Direct link to StdDev(number)")

Returns the sample standard deviation of the input column.

* `number` : A numeric column you want to compute the sample standard deviation of.

> `number`
>
> > `StdDev(column)` → 1.43

##### StdDevPop(number)[​](#stddevpopnumber "Direct link to StdDevPop(number)")

Returns the population standard deviation of the input column.

* `number` : A numeric column you want to compute the population standard deviation of.

> `number`
>
> > `StdDevPop(column)` → 1.47

##### Sum(number)[​](#sumnumber "Direct link to Sum(number)")

Returns the sum of all the values in the input column.

* `number` : A numeric column whose values you want to take the sum of.

> `number`
>
> > `Sum(column)` → 387

##### Variance(number)[​](#variancenumber "Direct link to Variance(number)")

Returns the sample variance of the input column.

* `number` : A numeric column you want to compute the sample variance of.

> `number`
>
> > `Variance(column)` → 2.12

##### VariancePop(number)[​](#variancepopnumber "Direct link to VariancePop(number)")

Returns the population variance of the input column.

* `number` : A numeric column you want to compute the population variance of.

> `number`
>
> > `VariancePop(column)` → 2.42

## Other Syntax[​](#other-syntax "Direct link to Other Syntax")

### Order of operations[​](#order-of-operations "Direct link to Order of operations")

Parenthesis can be used to group operations together to explicitly specify the order of operations, most often in arithmetic. For example: `(a + b) / c`.

Expressions are evaluated in the following order:

1. Parenthesis
2. Functions
3. Unary operators (`!`, `-` negation)
4. Arithmetic operators (`^`, `*`, `/`, `+`, `-` subtraction)
5. Comparative operators (`<=`, `<`, `>` and `>=`)
6. Equality (`=`, `!=`, `==` and `<>`)
7. Logical operators (`AND`, `OR`, `&&` and `||`)
8. Concatenation operator (`&`)

All operations are left-associative, meaning that compound expressions with multiple operators evaluate the leftmost sub-expression first. For example: `a AND b OR c` is treated as `(a AND b) OR c`.

### Escaping column names[​](#escaping-column-names "Direct link to Escaping column names")

Backticks (``) may used as a wrapper for references. This is only required if the column name contains special characters such as whitespace, such as in `` `Total Price` ``.

## Nulls[​](#nulls "Direct link to Nulls")

The result of a calculation will be `null` if `null` is one of the formula's arguments, and substituting the `null` argument with different values would produce different outcomes. For example, `startswith(null, 'Hello')` returns `null` because substituting `null` with different values produces different outcomes (substituting with `'Hello'` produces `True`, while substituting with `'Hi'` returns `False`). Some more examples are below:

* `1 + null` → null
* `If(null, b, c)` → c
* `Switch(null, b, c)` → null
* `True OR null` → null
* `False OR null` → null
* `True AND null` → null
* `False AND null` → False
* `null OR null` → null
* `null AND null` → null

Null values are ignored for all aggregate calculations. For example, `Count(column)` will ignore null values when calculating count of values in `column`.

## Known limitations[​](#known-limitations "Direct link to Known limitations")

* **Not all databases support calculations with Query mode:** It is not possible to configure calculations on [query objects](/docs/explore-data/cells/sql-cells/sql-cells-introduction#query-mode) from certain connections. See the [table below](#supported-connections) to understand which connections are supported.
* **No windows:** Window operations (`Rank()`, `PercentOfTotal()`, offset range inputs, etc.) are not currently supported.
* **Column-level, not cell-level:** Calculations happen on the column level. It is not possible to perform a calculation on a single row without applying it to the rest of the column. Similarly, you must reference whole columns in your formulas. It is not possible to reference an individual row, or range of rows, in your formula.

## Supported connections[​](#supported-connections "Direct link to Supported connections")

The below table details which data connections are supported when using Calculations on [query objects](/docs/explore-data/cells/sql-cells/sql-cells-introduction#query-mode).

| Database | Supported? |
| --- | --- |
| AlloyDB | ✅ |
| Athena | ✅ |
| BigQuery | ✅ |
| ClickHouse | ✅ |
| CloudSQL (MySQL) | ✅ |
| CloudSQL (PostgreSQL) | ✅ |
| CloudSQL (MS SQL Server) | ❌ |
| Databricks | ✅ |
| DuckDB | ✅ |
| MS SQL Server | ❌ |
| MariaDB | ✅ |
| Motherduck | ✅ |
| MySQL | ✅ |
| PostgreSQL | ✅ |
| Presto | ❌ |
| Redshift | ✅ |
| Snowflake | ✅ |
| Starburst | ❌ |
| Trino | ❌ |

#### On this page

* [Formulas](#formulas)
* [Parameterized calculations](#parameterized-calculations)
* [Data types](#data-types)
* [Operators](#operators)
* [Functions](#functions)
  + [📝 Text](#-text)
  + [🧮 Math](#-math)
  + [🔀 Logical](#-logical)
  + [🪄 Casting](#-casting)
  + [📅 Date & Time](#-date--time)
  + [➕ Aggregates](#-aggregates)
* [Other Syntax](#other-syntax)
  + [Order of operations](#order-of-operations)
  + [Escaping column names](#escaping-column-names)
* [Nulls](#nulls)
* [Known limitations](#known-limitations)
* [Supported connections](#supported-connections)