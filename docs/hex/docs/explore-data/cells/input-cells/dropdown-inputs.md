On this page

# Dropdown inputs

Parameterize your analysis based on users' selection of a single value from a list of enumerated numbers or strings.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to create and edit input cells.
* Users with **Can View App** permissions and higher can interact with input cells in published [Apps](/docs/share-insights/apps/apps-introduction).

## Static values[​](#static-values "Direct link to Static values")

Static values are input manually. Hex supports several methods:

* Typing them one-by-one and hitting `Enter/Return` on your keyboard
* Entering a comma-separated list (`option 1, option 2, option 3`) and hitting `Enter/Return` on your keyboard
* Copy-pasting a comma separated list

## Dynamic values[​](#dynamic-values "Direct link to Dynamic values")

Dynamic values allow you to link a dropdown's available options to a dataframe column, list, numpy array, or Pandas series from the code itself.

In both the Notebook view and App builder, if the selected value is no longer available in the input object (i.e., an upstream change eliminates that option), the selection will default to the first value in the input object.

tip

Dropdowns will only show the first 10,000 results, all following options will be truncated.

## Optional input[​](#optional-input "Direct link to Optional input")

Enable the "Optional" toggle if you want users to be able to clear their selection. When enabled, users can click "Clear selection" in the dropdown to clear their selection. When this occurs, the output variable will pass `None` to any downstream cells that reference the output.

#### On this page

* [Static values](#static-values)
* [Dynamic values](#dynamic-values)
* [Optional input](#optional-input)