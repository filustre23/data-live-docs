On this page

# SQL formatting

Hex offers built-in SQL formatting, as well as the option to configure custom SQL linting.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there).

## Built-in SQL formatting[​](#built-in-sql-formatting "Direct link to Built-in SQL formatting")

Clicking “Format code” from the 3-dot menu of a SQL cell will automatically format your query. To invoke the keyboard shortcut, first use `esc` to enter command mode, then `f + s`.

[](/assets/medias/format-sql-7c51553ed80fe39c0ed6cd4e1d276f37.mp4)

## Custom SQL formatting[​](#custom-sql-formatting "Direct link to Custom SQL formatting")

tip

This feature is available for workspaces on Professional, Teams, & Enterprise plans.

It is possible to use a custom linter to format your workspace’s SQL queries whenever “Format code” is triggered.

Hex accepts [SQLFluff](https://docs.sqlfluff.com/en/stable/index.html) configs to format your queries. In a data connection’s settings, simply upload a SQLFluff config; then the config’s rules will be used each time a query using that data connection is formatted. The uploaded file can be of any type, although `.sqlfluff` is considered the standard practice.

If no config file has been uploaded, Hex will use SQLFluff's [default config](https://docs.sqlfluff.com/en/stable/configuration/default_configuration.html) to format your SQL. If you'd like to use your own formatting rules, you can use this config as a jumping off point, or create your own from scratch. SQLFluff’s [configuration](https://docs.sqlfluff.com/en/stable/configuration/index.html) and [rules reference](https://docs.sqlfluff.com/en/stable/rules.html) docs are great resources for guidance on how to define your config file.

Please note that Hex uses SQLFluff 2.0. See the [upgrade guide](https://docs.sqlfluff.com/en/stable/releasenotes.html#upgrading-from-1-x-to-2-0) if you have any questions on how to update your config.

#### On this page

* [Built-in SQL formatting](#built-in-sql-formatting)
* [Custom SQL formatting](#custom-sql-formatting)