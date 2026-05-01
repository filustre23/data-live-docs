On this page

# Multiselect inputs

Parameterize your analysis based on a user's input of multiple selected values.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to create and edit input cells.
* Users with **Can View App** permissions and higher can interact with input cells in published [Apps](/docs/share-insights/apps/apps-introduction).

Multiselect input cells allow users to select multiple values for an input parameter. Multiselect input cells can accept string or numeric data types. Selected values are returned as a variable containing an array of strings or numbers that you can reference in your code.

tip

When referencing a multiselect input variable in your code with Jinja, you must declare it as an array e.g. `{{multiselect_input | array}}` Continue below to see an example or read more about using Jinja [here](/docs/explore-data/cells/using-jinja).

## Static multiselect values[​](#static-multiselect-values "Direct link to Static multiselect values")

Static values are input manually. Hex supports several methods:

* Type them one-by-one and pressing `Enter/Return`
* Enter a comma-separated list (`option 1, option 2, option 3`) and hit `Enter/Return`
* Copy-paste a comma separated list

## Dynamic multiselect values[​](#dynamic-multiselect-values "Direct link to Dynamic multiselect values")

Dynamic values allow you to link a multiselect's available values to a list that has been defined in the project itself. A common use case is querying the distinct values for a column, and setting those values as the dynamic inputs for a multiselect.

tip

Multiselect inputs will only show the first 10,000 results, all following options will be truncated.

#### On this page

* [Static multiselect values](#static-multiselect-values)
* [Dynamic multiselect values](#dynamic-multiselect-values)