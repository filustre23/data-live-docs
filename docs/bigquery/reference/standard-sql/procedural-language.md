* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Procedural language Stay organized with collections Save and categorize content based on your preferences.

The GoogleSQL procedural language lets you execute multiple statements
in one query as a multi-statement query. You can use
a multi-statement query to:

* Run multiple statements in a sequence, with shared state.
* Automate management tasks such as creating or dropping tables.
* Implement complex logic using programming constructs such as `IF` and `WHILE`.

This reference contains the statements that are part of the GoogleSQL
procedural language. To learn more about how you can use this
procedural language to write multi-statement queries, see
[Work with multi-statement queries](/bigquery/docs/multi-statement-queries). To learn how you
can convert multi-statement queries into stored procedures, see
[Work with stored procedures](/bigquery/docs/procedures).

## `DECLARE`

```
DECLARE variable_name[, ...] [variable_type] [DEFAULT expression];
```

`variable_name` must be a valid identifier, and `variable_type` is any
GoogleSQL [type](/bigquery/docs/reference/standard-sql/data-types).

**Description**

Declares a variable of the specified type. If the `DEFAULT` clause is specified,
the variable is initialized with the value of the expression; if no
`DEFAULT` clause is present, the variable is initialized with the value
`NULL`.

If `[variable_type]` is omitted then a `DEFAULT` clause must be specified. The
variable’s type will be inferred by the type of the expression in the `DEFAULT`
clause.

Variable declarations must appear before other procedural statements, or at the
start of a `BEGIN` block. Variable names are case-insensitive.

Multiple variable names can appear in a single `DECLARE` statement, but only
one `variable_type` and `expression`.

It's an error to declare a variable with the same name as a variable
declared earlier in the current block or in a containing block.

If the `DEFAULT` clause is present, the value of the expression must be
coercible to the specified type. The expression may reference other variables
declared previously within the same block or a containing block.

GoogleSQL also supports [system variables](/bigquery/docs/reference/system-variables). You don't
need to declare system variables, but you can set any of them that aren't
marked read-only. You can reference system variables in queries.

**Examples**

The following example initializes the variable `x` as an
`INT64` with the value `NULL`.

```
DECLARE x INT64;
```

The following example initializes the variable `d` as a
`DATE` object with the value of the current date.

```
DECLARE d DATE DEFAULT CURRENT_DATE();
```

The following example initializes the variables `x`, `y`, and `z` as
`INT64` with the value 0.

```
DECLARE x, y, z INT64 DEFAULT 0;
```

The following example declares a variable named `item` corresponding to an
arbitrary item in the `schema1.products` table. The type of `item` is inferred
from the table schema.

```
DECLARE item DEFAULT (SELECT item FROM schema1.products LIMIT 1);
```

## `SET`

**Syntax**

```
SET variable_name = expression;
```

```
SET (variable_name[, ...]) = (expression[, ...]);
```

**Description**

Sets a variable to have the value of the provided expression, or sets multiple
variables at the same time based on the result of multiple expressions.

The `SET` statement may appear anywhere within a multi-statement query.

**Examples**

The following example sets the variable `x` to have the value 5.

```
SET x = 5;
```

The following example sets the variable `a` to have the value 4, `b` to have the
value 'foo', and the variable `c` to have the value `false`.

```
SET (a, b, c) = (1 + 3, 'foo', false);
```

The following example assigns the result of a query to multiple variables.
First, it declares two variables, `target_word` and `corpus_count`; next, it
assigns the results of a
[`SELECT AS STRUCT` query](/bigquery/docs/reference/standard-sql/query-syntax#select_as_struct)
to the two variables. The result of the query is a single row containing a
`STRUCT` with two fields; the first element is
assigned to the first variable, and the second element is assigned to the second
variable.

```
DECLARE target_word STRING DEFAULT 'methinks';
DECLARE corpus_count, word_count INT64;

SET (corpus_count, word_count) = (
  SELECT AS STRUCT COUNT(DISTINCT corpus), SUM(word_count)
  FROM bigquery-public-data.samples.shakespeare
  WHERE LOWER(word) = target_word
);

SELECT
  FORMAT('Found %d occurrences of "%s" across %d Shakespeare works',
         word_count, target_word, corpus_count) AS result;
```

This statement list outputs the following string:

```
Found 151 occurrences of "methinks" across 38 Shakespeare works
```

## `EXECUTE IMMEDIATE`

**Syntax**

```
EXECUTE IMMEDIATE sql_expression [ INTO variable[, ...] ] [ USING identifier[, ...] ];

sql_expression:
  { "query_statement" | expression("query_statement") }

identifier:
  { variable | value } [ AS alias ]
```

**Description**

Executes a dynamic SQL statement on the fly.

* `sql_expression`: An expression that can represent one of the following:

  + A [query statement](/bigquery/docs/reference/standard-sql/query-syntax)
  + An expression that you can use on a query statement
  + A single [DDL statement](/bigquery/docs/reference/standard-sql/data-definition-language)
  + A single [DML statement](/bigquery/docs/reference/standard-sql/data-manipulation-language)
  + A single [DCL statement](/bigquery/docs/reference/standard-sql/data-control-language)

  This expression can't be a control statement like `IF`.
* `expression`: Can be a
  [function](/bigquery/docs/reference/standard-sql/functions-all), [conditional expression](/bigquery/docs/reference/standard-sql/conditional_expressions), or
  [expression subquery](/bigquery/docs/reference/standard-sql/subqueries#expression_subquery_concepts).
* `query_statement`: Represents a valid standalone SQL statement to execute.
  If this returns a value, the `INTO` clause must contain values of the same
  type. You may access both system variables and values present in the `USING`
  clause; all other local variables and query parameters aren't exposed to
  the query statement.
* `INTO` clause: After the SQL expression is executed, you can store the
  results in one or more [variables](#declare), using the `INTO` clause.
* `USING` clause: Before you execute your SQL expression, you can pass in one
  or more identifiers from the `USING` clause into the SQL expression.
  These identifiers function similarly to query parameters, exposing values to
  the query statement. An identifier can be a variable or a value.

You can include these placeholders in the `query_statement` for identifiers
referenced in the `USING` clause:

* `?`: The value for this placeholder is bound to an identifier in the `USING`
  clause by index.

  ```
  DECLARE y INT64;
  -- y = 1 * (3 + 2) = 5
  EXECUTE IMMEDIATE "SELECT ? * (? + 2)" INTO y USING 1, 3;
  ```
* `@identifier`: The value for this placeholder is bound to an identifier in
  the `USING` clause by name. This syntax is identical to
  the query parameter syntax.

  ```
  DECLARE y INT64;
  -- y = 1 * (3 + 2) = 5
  EXECUTE IMMEDIATE "SELECT @a * (@b + 2)" INTO y USING 1 as a, 3 as b;
  ```

Here are some additional notes about the behavior of the `EXECUTE IMMEDIATE`
statement:

* `EXECUTE IMMEDIATE` is restricted from being executed dynamically as a
  nested element. This means `EXECUTE IMMEDIATE` can't be nested in another
  `EXECUTE IMMEDIATE` statement.
* If an `EXECUTE IMMEDIATE` statement returns results, then those results
  become the result of the entire statement and any appropriate
  system variables are updated.
* The same variable can appear in both the `INTO` and `USING` clauses.
* `query_statement` can contain a single parsed statement that contains other
  statements (for example, BEGIN...END)
* If zero rows are returned from `query_statement`, including from zero-row
  value tables, all variables in the `INTO` clause are set to NULL.
* If one row is returned from `query_statement`, including from zero-row
  value tables, values are assigned by position, not variable name.
* If an `INTO` clause is present, an error is thrown if you attempt to return
  more than one row from `query_statement`.

**Examples**

In this example, we create a table of books and populate it with data. Note
the different ways that you can reference variables, save values to
variables, and use expressions.

```
-- Create some variables.
DECLARE book_name STRING DEFAULT 'Ulysses';
DECLARE book_year INT64 DEFAULT 1922;
DECLARE first_date INT64;

-- Create a temporary table called Books.
EXECUTE IMMEDIATE
  "CREATE TEMP TABLE Books (title STRING, publish_date INT64)";

-- Add a row for Hamlet (less secure).
EXECUTE IMMEDIATE
  "INSERT INTO Books (title, publish_date) VALUES('Hamlet', 1599)";

-- Add a row for Ulysses, using the variables declared and the ? placeholder.
EXECUTE IMMEDIATE
  "INSERT INTO Books (title, publish_date) VALUES(?, ?)"
  USING book_name, book_year;

-- Add a row for Emma, using the identifier placeholder.
EXECUTE IMMEDIATE
  "INSERT INTO Books (title, publish_date) VALUES(@name, @year)"
  USING 1815 as year, "Emma" as name;

-- Add a row for Middlemarch, using an expression.
EXECUTE IMMEDIATE
  CONCAT(
    "INSERT INTO Books (title, publish_date)", "VALUES('Middlemarch', 1871)"
  );

-- The table looks similar to the following:
/*------------------+------------------+
 | title            | publish_date     |
 +------------------+------------------+
 | Hamlet           | 1599             |
 | Ulysses          | 1922             |
 | Emma             | 1815             |
 | Middlemarch      | 1871             |
 +------------------+------------------*/

-- Save the publish date of the earliest book, Hamlet, to a variable called
-- first_date.
EXECUTE IMMEDIATE "SELECT MIN(publish_date) FROM Books LIMIT 1" INTO first_date;
```

## `BEGIN...END`

**Syntax**

```
BEGIN
  sql_statement_list
END;
```

**Description**

`BEGIN` initiates a block of statements where declared variables exist only
until the corresponding `END`. `sql_statement_list` is a list of zero or more
SQL statements ending with semicolons.

Variable declarations must appear at the start of the block, prior to other
types of statements. Variables declared inside a block may only be referenced
within that block and in any nested blocks. It's an error to declare a variable
with the same name as a variable declared in the same block or an outer block.

There is a maximum nesting level of 50 for blocks and conditional statements
such as `BEGIN`/`END`, `IF`/`ELSE`/`END IF`, and `WHILE`/`END WHILE`.

`BEGIN`/`END` is restricted from being executed dynamically as a nested element.

You can use a label with this statement. To learn more, see [Labels](#labels).

**Examples**

The following example declares a variable `x` with the default value 10; then,
it initiates a block, in which a variable `y` is assigned the value of `x`,
which is 10, and returns this value; next, the `END` statement ends the
block, ending the scope of variable `y`; finally, it returns the value of `x`.

```
DECLARE x INT64 DEFAULT 10;
BEGIN
  DECLARE y INT64;
  SET y = x;
  SELECT y;
END;
SELECT x;
```

## `BEGIN...EXCEPTION...END`

**Syntax**

```
BEGIN
  sql_statement_list
EXCEPTION WHEN
```