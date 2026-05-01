On this page

# Input parameters

Input parameters are a core, unique part of Hex. Input parameters can be created in the Notebook view and then added, optionally, to an app.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to create and edit input cells.
* Users with **Can View App** permissions and higher can interact with input cells in published [Apps](/docs/share-insights/apps/apps-introduction).

## Add an Input cell[​](#add-an-input-cell "Direct link to Add an Input cell")

### Cell menus[​](#cell-menus "Direct link to Cell menus")

Add an Input cell to your project from the cell bar at the bottom of your Notebook, or from the **+ Add** option between cells.

### Right-click to replace code with a parameter[​](#right-click-to-replace-code-with-a-parameter "Direct link to Right-click to replace code with a parameter")

If you highlight and right-click some code in a Python or SQL cell, you can use the **Add Input Parameter** option to replace your code with an input value directly.

[](/assets/medias/right-click-to-replace-a83c553b13c69005fb591f2f84345bea.mp4)

## Configure an Input cell[​](#configure-an-input-cell "Direct link to Configure an Input cell")

All Input parameters have two base options, accessible from the configuration menu:

**Label**: text label displayed above the element, primarily in the [App builder](/docs/share-insights/apps/app-builder).

**Name:** the name of the Python variable, and the way to reference the output of the input parameter downstream in your project. Changing this name will automatically update references to the parameter throughout the Notebook.

## Reference Input parameters[​](#reference-input-parameters "Direct link to Reference Input parameters")

Inputs are stored as Python variables, e.g., `input_1` that can be referenced throughout your project, just like other variables.

Input variables cannot have their values reassigned, e.g., `input_1 = 123` will not effectively re-assign the parameter to `123`. Instead, you will have created a new variable, which is not connected to the input parameter, with the name `input_1` and value `123`.

Inputs can be referenced in SQL cells through the use of [Jinja](https://jinja.palletsprojects.com/en/3.0.x/), using syntax like `{{ input_1 }}`. For an example of this, see our tutorial on [parameterizing SQL queries](/tutorials/connect-to-data/parameterize-sql#finally-parameterize-the-sql-query-with-the-input-value).

## Include Input parameters as URL parameters[​](#include-input-parameters-as-url-parameters "Direct link to Include Input parameters as URL parameters")

For published apps, Input parameter values can be specified as part of the URL. For more information and examples, see our documentation on [sharing links to Published apps](/docs/share-insights/apps/publish-and-share-apps#input-parameters-as-url-parameters).

## Types of Input parameters[​](#types-of-input-parameters "Direct link to Types of Input parameters")

* [Text](/docs/explore-data/cells/input-cells/text-number-slider-and-date-inputs)
* [Number](/docs/explore-data/cells/input-cells/text-number-slider-and-date-inputs)
* [Slider](/docs/explore-data/cells/input-cells/text-number-slider-and-date-inputs)
* [Date](/docs/explore-data/cells/input-cells/text-number-slider-and-date-inputs)
* [Dropdown](/docs/explore-data/cells/input-cells/dropdown-inputs)
* [Checkbox](/docs/explore-data/cells/input-cells/text-number-slider-and-date-inputs)
* [Multiselect](/docs/explore-data/cells/input-cells/multiselect-inputs)
* [Table](/docs/explore-data/cells/input-cells/table-inputs)
* [Run Button](/docs/explore-data/cells/input-cells/run-button)
* [File upload](/docs/explore-data/cells/input-cells/file-upload-inputs)

#### On this page

* [Add an Input cell](#add-an-input-cell)
  + [Cell menus](#cell-menus)
  + [Right-click to replace code with a parameter](#right-click-to-replace-code-with-a-parameter)
* [Configure an Input cell](#configure-an-input-cell)
* [Reference Input parameters](#reference-input-parameters)
* [Include Input parameters as URL parameters](#include-input-parameters-as-url-parameters)
* [Types of Input parameters](#types-of-input-parameters)