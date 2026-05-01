On this page

# Using Jinja

Parameterize SQL queries, and reference Python variables in Text, Table, and other cell types by using Jinja.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there).

Hex uses [Jinja](https://jinja.palletsprojects.com/templates/) to allow Editors to combine Python variables with SQL, Text, and other places where you can type in text (including Table Display filters, and Single Value cells).

## SQL parameterization[​](#sql-parameterization "Direct link to SQL parameterization")

tip

Check out the [Parameterize SQL](/tutorials/connect-to-data/parameterize-sql) tutorial for more hands-on examples!

For security and performance, we handle all parameterized SQL queries as [prepared statements](https://en.wikipedia.org/wiki/Prepared_statement). Prepared statements are a way to template queries and substitute values where desired during execution. Not only is there some performance benefit when using prepared statements, they are also robust against SQL injection.

Watch a quick intro for how to parameterize your queries here:

### Using variables in queries[​](#using-variables-in-queries "Direct link to Using variables in queries")

You can parameterize your queries with both Input parameters and Python variables! We use [Jinja](https://jinja.palletsprojects.com/en/3.1.x/intro/) templating syntax to indicate the parameters which should be substituted into your query. See the screenshot at the bottom of the page for an example of how to use Jinja's if blocks and for loops in your queries.

To pass a Python variable into your query you'll need to wrap it in double curly braces, `{{ }}`. For multi-index variables (e.g. lists, arrays), you'll also need to declare that you're passing in an array-type variable (e.g. `{{list_variable | array}}`)

caution

Individual databases have limits on how many parameters can be bound to a single query. For example, PostgreSQL allows 32767 variables, however Snowflake's maximum is 16384.

By default, prepared statements cannot accept query attributes as parameters and only allow for substituting in values. For example, the phrase `WHERE column = {{value}}` is allowed by default while `WHERE {{column}} = value` is not. You can force the literal parameterization of a query attribute by passing `| sqlsafe` as an additional flag with your parameter. e.g. `WHERE {{column | sqlsafe}} = value`.

warning

If you use the `sqlsafe` flag to force a parameterization you are removing the protection that prepared statements offer against sql injection!

Jinja is a very powerful way to parameterize your queries. Additional Jinja functions like for loops, loop variables, and if conditionals are all available for use in SQL queries. See below for an example query with more advanced Jinja functions.

## Markdown & Text Cells[​](#markdown--text-cells "Direct link to Markdown & Text Cells")

Both [Markdown and Text cells](/docs/explore-data/cells/text-cells) allow you to mix python variables with your text via Jinja.

In Markdown cells, type your text as usual but in place of hard-coding the value you want, wrap the variable name in `{{ }}` braces to dynamically update your Markdown text. See the screenshot below for an example.

Text cells also support variable substitution using the usual double curly braces, `{{ }}`, of [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) syntax. In order to render values, you'll need to run the cell.

[](/assets/medias/Text-cell-jinja-syntax-e71b066f45aab28ee266e244e21e596c.mp4)

warning

Complex logic such as if statements and for loops are not yet supported in Text cells.

## Additional Jinja support[​](#additional-jinja-support "Direct link to Additional Jinja support")

You can also use Jinja in some input fields in Hex. In particular, Jinja is supported in:

* The label field in a [Single Value Cell](/docs/explore-data/cells/visualization-cells/single-value-cells) allows you to use Jinja.

* Filters in a [Table Display](/docs/explore-data/cells/visualization-cells/table-display-cells#filters) can reference Jinja values.

Note that only Jinja variables (i.e. values inside `{{ }}` brackets) are supported - Jinja expressions (with `{% %}`) are not supported.

#### On this page

* [SQL parameterization](#sql-parameterization)
  + [Using variables in queries](#using-variables-in-queries)
* [Markdown & Text Cells](#markdown--text-cells)
* [Additional Jinja support](#additional-jinja-support)