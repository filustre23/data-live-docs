* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Window function calls Stay organized with collections Save and categorize content based on your preferences.

A window function, also known as an analytic function, computes values
over a group of rows and returns a single result for *each* row. This is
different from an aggregate function, which returns a single result for
*a group* of rows.

A window function includes an `OVER` clause, which defines a window of rows
around the row being evaluated. For each row, the window function result
is computed using the selected window of rows as input, possibly
doing aggregation.

With window functions you can compute moving averages, rank items, calculate
cumulative sums, and perform other analyses.

## Window function syntax

```
function_name ( [ argument_list ] ) OVER over_clause

over_clause:
  { named_window | ( [ window_specification ] ) }

window_specification:
  [ named_window ]
  [ PARTITION BY partition_expression [, ...] ]
  [ ORDER BY expression [ { ASC | DESC }  ] [, ...] ]
  [ window_frame_clause ]

window_frame_clause:
  { rows_range } { frame_start | frame_between }

rows_range:
  { ROWS | RANGE }
```

**Description**

A window function computes results over a group of rows. You can use the
following syntax to build a window function:

* `function_name`: The function that performs a window operation.

  For example, the numbering function `RANK()` could be used here.
* `argument_list`: Arguments that are specific to the function.
  Some functions have them, some don't.
  Not all clauses are supported
  when the function is used with the `OVER` clause as a window function. For
  example, the `DISTINCT` clause can't be used with the `OVER` clause. For
  more information, see
  [Aggregate function calls](/bigquery/docs/reference/standard-sql/aggregate-function-calls).
* `OVER`: Keyword required in the window function syntax preceding
  the [`OVER` clause](#def_over_clause).
* [`over_clause`](#def_over_clause): References a window that defines a group
  of rows in a table upon which to use a window function.
* [`window_specification`](#def_window_spec): Defines the specifications for
  the window.
* [`window_frame_clause`](#def_window_frame): Defines the window frame
  for the window.
* [`rows_range`](#def_window_frame): Defines the physical rows or a
  logical range for a window frame.

**Notes**

A window function can appear as a scalar expression operand in
the following places in the query:

* The `SELECT` list. If the window function appears in the `SELECT` list,
  its argument list and `OVER` clause can't refer to aliases introduced
  in the same `SELECT` list.
* The `ORDER BY` clause. If the window function appears in the `ORDER BY`
  clause of the query, its argument list can refer to `SELECT`
  list aliases.
* The `QUALIFY` clause.

A window function can't refer to another window function in its
argument list or its `OVER` clause, even indirectly through an alias.

A window function is evaluated after aggregation. For example, the
`GROUP BY` clause and non-window aggregate functions are evaluated first.
Because aggregate functions are evaluated before window functions,
aggregate functions can be used as input operands to window functions.

**Returns**

A single result for each row in the input.

### Defining the `OVER` clause

```
function_name ( [ argument_list ] ) OVER over_clause

over_clause:
  { named_window | ( [ window_specification ] ) }
```

**Description**

The `OVER` clause references a window that defines a group of rows in a table
upon which to use a window function. You can provide a
[`named_window`](#ref_named_window) that is
[defined in your query](/bigquery/docs/reference/standard-sql/query-syntax#window_clause), or you can
define the [specifications for a new window](#def_window_spec).

**Notes**

If neither a named window nor window specification is provided, all
input rows are included in the window for every row.

**Examples using the `OVER` clause**

These queries use window specifications:

* [Compute a grand total](#compute_a_grand_total)
* [Compute a subtotal](#compute_a_subtotal)
* [Compute a cumulative sum](#compute_a_cumulative_sum)
* [Compute a moving average](#compute_a_moving_average)
* [Compute the number of items within a range](#compute_the_number_of_items_within_a_range)
* [Get the most popular item in each category](#get_the_most_popular_item_in_each_category)
* [Get the last value in a range](#get_the_last_value_in_a_range)
* [Compute rank](#compute_rank)

These queries use a named window:

* [Get the last value in a range](#get_the_last_value_in_a_range)
* [Use a named window in a window frame clause](#def_use_named_window)

### Defining the window specification

```
window_specification:
  [ named_window ]
  [ PARTITION BY partition_expression [, ...] ]
  [ ORDER BY expression [ { ASC | DESC } ] [, ...] ]
  [ window_frame_clause ]
```

**Description**

Defines the specifications for the window.

* [`named_window`](#ref_named_window): The name of an existing window that was
  defined with a [`WINDOW` clause](/bigquery/docs/reference/standard-sql/query-syntax#window_clause).

**Important:** If you use a named window, special rules apply to
`PARTITION BY`, `ORDER BY`, and `window_frame_clause`. See
[Rules for using a named window in the window specification](#named_window_rules).

* `PARTITION BY`: Breaks up the input rows into separate partitions, over
  which the window function is independently evaluated.
  + A `partition_expression` computes a value that determines which partition
    each row falls into.
  + Multiple partition expressions are allowed in the `PARTITION BY` clause.
  + An expression can't contain floating point types, non-groupable types,
    constants, or window functions.
  + If this optional clause isn't used, all rows in the input table
    comprise a single partition.
* `ORDER BY`: Defines how rows are ordered within a partition.

  This clause is optional in most situations, but is required in some
  cases for [navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions).
* [`window_frame_clause`](#def_window_frame): For aggregate analytic
  functions, defines the window frame within the current partition.
  The window frame determines what to include in the window.
  If this clause is used, `ORDER BY` is required except for fully
  unbounded windows.

**Notes**

If neither the `ORDER BY` clause nor window frame clause are present,
the window frame includes all rows in that partition.

For aggregate analytic functions, if the `ORDER BY` clause is present but
the window frame clause isn't, the following window frame clause is
used by default:

```
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

For example, the following queries are equivalent:

```
SELECT book, LAST_VALUE(book)
  OVER (ORDER BY year)
FROM Library
```

```
SELECT book, LAST_VALUE(book)
  OVER (
    ORDER BY year
    RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
FROM Library
```

**Rules for using a named window in the window specification**

If you use a named window in your window specifications, these rules apply:

* The specifications in the named window can be extended
  with new specifications that you define in the window specification clause.
* You can't have redundant definitions. If you have an `ORDER BY` clause
  in the named window and the window specification clause, an
  error is thrown.
* The order of clauses matters. `PARTITION BY` must come first,
  followed by `ORDER BY` and `window_frame_clause`. If you add a named window,
  its window specifications are processed first.

  ```
  --this works:
  SELECT item, purchases, LAST_VALUE(item)
    OVER (ItemWindow ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING) AS most_popular
  FROM Produce
  WINDOW ItemWindow AS (ORDER BY purchases)

  --this doesn't work:
  SELECT item, purchases, LAST_VALUE(item)
    OVER (ItemWindow ORDER BY purchases) AS most_popular
  FROM Produce
  WINDOW ItemWindow AS (ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING)
  ```
* A named window and `PARTITION BY` can't appear together in the
  window specification. If you need `PARTITION BY`, add it to the named window.
* You can't refer to a named window in an `ORDER BY` clause, an outer query,
  or any subquery.

**Examples using the window specification**

These queries define partitions in a window function:

* [Compute a subtotal](#compute_a_subtotal)
* [Compute a cumulative sum](#compute_a_cumulative_sum)
* [Get the most popular item in each category](#get_the_most_popular_item_in_each_category)
* [Get the last value in a range](#get_the_last_value_in_a_range)
* [Compute rank](#compute_rank)
* [Use a named window in a window frame clause](#def_use_named_window)

These queries include a named window in a window specification:

* [Get the last value in a range](#get_the_last_value_in_a_range)
* [Use a named window in a window frame clause](#def_use_named_window)

These queries define how rows are ordered in a partition:

* [Compute a subtotal](#compute_a_subtotal)
* [Compute a cumulative sum](#compute_a_cumulative_sum)
* [Compute a moving average](#compute_a_moving_average)
* [Compute the number of items within a range](#compute_the_number_of_items_within_a_range)
* [Get the most popular item in each category](#get_the_most_popular_item_in_each_category)
* [Get the last value in a range](#get_the_last_value_in_a_range)
* [Compute rank](#compute_rank)
* [Use a named window in a window frame clause](#def_use_named_window)

### Defining the window frame clause

```
window_frame_clause:
  { rows_range } { frame_start | frame_between }

rows_range:
  { ROWS | RANGE }

frame_between:
  {
    BETWEEN  unbounded_preceding AND frame_end_a
    | BETWEEN numeric_preceding AND frame_end_a
    | BETWEEN current_row AND frame_end_b
    | BETWEEN numeric_following AND frame_end_c
  }

frame_start:
  { unbounded_preceding | numeric_preceding | [ current_row ] }

frame_end_a:
  { numeric_preceding | current_row | numeric_following | unbounded_following }

frame_end_b:
  { current_row | numeric_following | unbounded_following }

frame_end_c:
  { numeric_following | unbounded_following }

unbounded_preceding:
  UNBOUNDED PRECEDING

numeric_preceding:
  numeric_expression PRECEDING

unbounded_following:
  UNBOUNDED FOLLOWING

numeric_following:
  numeric_expression FOLLOWING

current_row:
  CURRENT ROW
```

The window frame clause defines the window frame around the current row within
a partition, over which the window function is evaluated.
Only aggregate analytic functions can use a window frame clause.

* `rows_range`: A clause that defines a window frame with physical rows
  or a logical range.

  + `ROWS`: Computes the window frame based on physical offsets from the
    current row. For example, you could include two rows before and after
    the current row.
  + `RANGE`: Computes the window frame based on a logical range of rows
    around the current row, based on the current row’s `ORDER BY` key value.
    The provided range value is added or subtracted to the current row's
    key value to define a starting or ending range boundary for the
    window frame. In a range-based window frame, there must be exactly one
    expression in the `ORDER BY` clause, and the expression must have a
    numeric type.**Tip:** If you want to use a range with a date, use `ORDER BY` with the
  `UNIX_DATE()` function. If you want to use a range with a timestamp,
  use the `UNIX_SECONDS()`, `UNIX_MILLIS()`, or `UNIX_MICROS()` function.
* `frame_between`: Creates a window frame with a lower and upper boundary.
  The first boundary represents the lower boundary. The second boundary
  represents the upper boundary. Only certain boundary combinations can be
  used, as show in the preceding syntax.

  + Define the beginning of the window frame with `unbounded_preceding`,
    `numeric_preceding`, `numeric_following`, or `current_row`.
    - `unbounded_preceding`: The window frame starts at the beginning of the
      partition.
    - `numeric_preceding` or `numeric_following`: The start of the window
      frame is relative to the
      current row.
    - `current_row`: The window frame starts at the current row.
  + Define the end of the window frame with `numeric_preceding`,
    `numeric_following`, `current_row`, or `unbounded_following`.
    - `numeric_preceding` or `numeric_following`: The end of the window
      frame is relative to the current row.
    - `current_row`: The window frame ends at the current row.
    - `unbounded_following`: The window frame ends at the end of the
      partition.
* `frame_start`: Creates a window frame with a lower boundary.
  The window frame ends at the current row.

  + `unbounded_preceding`: The window frame starts at the beginning of the
    partition.
  + `numeric_preceding`: The start of the window frame is relative to the
    current row.
  + `current_row`: The window frame starts at the current row.
* `numeric_expression`: An expression that represents a numeric type.
  The numeric expression must be a constant, non-negative integer
  or parameter.

**Notes**

If a boundary extends beyond the beginning or end of a partition,
the window frame will only include rows from within that partition.

You can't use a window frame clause with some
[navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions) and
[numbering functions](/bigquery/docs/reference/standard-sql/numbering_functions),
such as `RANK()`.

**Examples using the window frame clause**

These queries compute values with `ROWS`:

* [Compute a cumulative sum](#compute_a_cumulative_sum)
* [Compute a moving average](#compute_a_moving_average)
* [Get the most popular item in each category](#get_the_most_popular_item_in_each_category)
* [Get the last value in a range](#get_the_last_value_in_a_range)
* [Use a named window in a window frame clause](#def_use_named_window)

These queries compute values with `RANGE`:

* [Compute the number of items within a range](#compute_the_number_of_items_within_a_range)

These queries compute values with a partially or fully unbound window:

* [Compute a grand total](#compute_a_grand_total)
* [Compute a subtotal](#compute_a_subtotal)
* [Compute a cumulative sum](#compute_a_cumulative_sum)
* [Get the most popular item in each category](#get_the_most_popular_item_in_each_category)
* [Compute rank](#compute_rank)

These queries compute values with numeric boundaries:

* [Compute a cumulative sum](#compute_a_cumulative_sum)
* [Compute a moving average](#compute_a_moving_average)
* [Compute the number of items within a range](#compute_the_number_of_items_within_a_range)
* [Get the last value in a range](#get_the_last_value_in_a_range)
* [Use a named window in a window frame clause](#def_use_named_window)

These queries compute values with the current row as a boundary:

* [Compute a grand total](#compute_a_grand_total)
* [Compute a subtotal](#compute_a_subtotal)
* [Compute a cumulative sum](#compute_a_cumulative_sum)

### Referencing a named window

```
SELECT query_expr,
  function_name ( [ argument_list ] ) OVER over_clause
FROM from_item
WINDOW named_window_expression [, ...]

over_clause:
  { named_window | ( [ window_specification ] ) }

window_specification:
  [ named_window ]
  [ PARTITION BY partition_expression [, ...] ]
  [ ORDER BY expression [ { ASC | DESC } ] [, ...] ]
  [ window_frame_clause ]

named_window_expression:
  named_window AS { named_window | ( [ window_specification ] ) }
```

A named window represents a group of rows in a table upon which to use an
window function. A named window is defined in the
[`WINDOW` clause](/bigquery/docs/reference/standard-sql/query-syntax#window_clause), and referenced in
a window function's [`OVER` clause](#def_over_clause).
In an `OVER` clause, a named window can appear either by itself or embedded
within a [window specification](#def_window_spec).

**Examples**

* [Get the last value in a range](#get_the_last_value_in_a_range)
* [Use a named window in a window frame clause](#def_use_named_window)

## Filtering results with the QUALIFY clause

The `QUALIFY` clause can be used to filter the results of a window function.
For more information and examples, see the
[`QUALIFY` clause](/bigquery/docs/reference/standard-sql/query-syntax#qualify_clause).

## Window function examples

In these examples, the highlighted item is the current row. The **bolded
items** are the rows that are included in the analysis.

### Common tables used in examples

The following tables are used in the subsequent aggregate analytic
query examples: [`Produce`](#produce_table), [`Employees`](#employees_table),
and [`Farm`](#farm_table).

#### Produce table

Some examples reference a table called `Produce`:

```
WITH Produce AS
 (SELECT 'kale' as item, 23 as purchases, 'vegetable' as category
  UNION ALL SELECT 'banana', 2, 'fruit'
  UNION ALL SELECT 'cabbage', 9, 'vegetable'
  UNION ALL SELECT 'apple', 8, 'fruit'
  UNION ALL SELECT 'leek', 2, 'vegetable'
  UNION ALL SELECT 'lettuce', 10, 'vegetable')
SELECT * FROM Produce

/*-------------------------------------+
 | item      | category   | purchases  |
 +-------------------------------------+
 | kale      | vegetable  | 23         |
 | banana    | fruit      | 2          |
 | cabbage   | vegetable  | 9          |
 | apple     | fruit      | 8          |
 | leek      | vegetable  | 2          |
 | lettuce   | vegetable  | 10         |
 +-------------------------------------*/
```

#### Employees table

Some examples reference a table called `Employees`:

```
WITH Employees AS
 (SELECT 'Isabella' as name, 2 as department, DATE(1997, 09, 28) as start_date
  UNION ALL SELECT 'Anthony', 1, DATE(1995, 11, 29)
  UNION ALL SELECT 'Daniel', 2, DATE(2004, 06, 24)
  UNION ALL SELECT 'Andrew', 1, DATE(1999, 01, 23)
  UNION ALL SELECT 'Jacob', 1, DATE(1990, 07, 11)
  UNION ALL SELECT 'Jose', 2, DATE(2013, 03, 17))
SELECT * FROM Employees

/*-------------------------------------+
 | name      | department | start_date |
 +-------------------------------------+
 | Isabella  | 2          | 1997-09-28 |
 | Anthony   | 1          | 1995-11-29 |
 | Daniel    | 2          | 2004-06-24 |
 | Andrew    | 1          | 1999-01-23 |
 | Jacob     | 1          | 1990-07-11 |
 | Jose      | 2          | 2013-03-17 |
 +-------------------------------------*/
```

#### Farm table

Some examples reference a table called `Farm`:

```
WITH Farm AS
 (SELECT 'cat' as animal, 23 as population, 'mammal' as category
  UNION ALL SELECT 'duck', 3, 'bird'
  UNION ALL SELECT 'dog', 2, 'mammal'
  UNION ALL SELECT 'goose', 1, 'bird'
  UNION ALL SELECT 'ox', 2, 'mammal'
  UNION ALL SELECT 'goat', 2, 'mammal')
SELECT * FROM Farm

/*-------------------------------------+
 | animal    | category   | population |
 +-------------------------------------+
 | cat       | mammal     | 23         |
 | duck      | bird       | 3          |
 | dog       | mammal     | 2          |
 | goose     | bird       | 1          |
 | ox        | mammal     | 2          |
 | goat      | mammal     | 2          |
 +-------------------------------------*/
```

### Compute a grand total

This computes a grand total for all items in the
[`Produce`](#produce_table) table.

* (**banana**, **apple**, **leek**, **cabbage**, **lettuce**, **kale**) = 54 total purchases
* (**banana**, **apple**, **leek**, **cabbage**, **lettuce**, **kale**) = 54 total purchases
* (**banana**, **apple**, **leek**, **cabbage**, **lettuce**, **kale**) = 54 total purchases
* (**banana**, **apple**, **leek**, **cabbage**, **lettuce**, **kale**) = 54 total purchases
* (**banana**, **apple**, **leek**, **cabbage**, **lettuce**, **kale**) = 54 total purchases
* (**banana**, **apple**, **leek**, **cabbage**, **lettuce**, **kale**) = 54 total purchases

```
SELECT item, purchases, category, SUM(purchases)
  OVER () AS total_purchases
FROM Produce

/*-------------------------------------------------------+
 | item      | purchases  | category   | total_purchases |
 +-------------------------------------------------------+
 | banana    | 2          | fruit      | 54              |
 | leek      | 2          | vegetable  | 54              |
 | apple     | 8          | fruit      | 54              |
 | cabbage   | 9          | vegetable  | 54              |
 | lettuce   | 10         | vegetable  | 54              |
 | kale      | 23         | vegetable  | 54              |
 +-------------------------------------------------------*/
```

### Compute a subtotal

This computes a subtotal for each category in the
[`Produce`](#produce_table) table.

* fruit
  + (**banana**, **apple**) = 10 total purchases
  + (**banana**, **apple**) = 10 total purchases
* vegetable
  + (**leek**, **cabbage**, **lettuce**, **kale**) = 44 total purchases
  + (**leek**, **cabbage**, <