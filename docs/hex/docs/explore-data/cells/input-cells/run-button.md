On this page

# Run button inputs

Add button input to control when certain code in your project executes.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to create and edit input cells.
* Users with **Can View App** permissions and higher can interact with input cells in published [Apps](/docs/share-insights/apps/apps-introduction).

Run buttons are useful if you need to wait for user input before writing back to your database, or if you have expensive logic you want to be intentional about running.

## Configure Run button inputs[​](#configure-run-button-inputs "Direct link to Configure Run button inputs")

When setting up a Run button input you can customize several settings, in addition to the standard label and name.

* Color: Select the color of the button. Current options are grey, blue, green, orange, & red
* Icon: Select the icon displayed on the button by typing the name of any icon from the [Blueprint icon library](https://blueprintjs.com/docs/#icons)
* Text: Input the text that will display on the button

## Usage[​](#usage "Direct link to Usage")

The output of a Run button input is a boolean which evaluates `True` if a user has pressed the button and `False` if they have not. For example, when a user refreshes an app (in the App builder) or re-runs the project (in Notebook view), your Run buttons have not explicitly been pressed and so will evaluate to `False`. When a user presses a Run button, dependent cells will be run. During that set of cell runs, the button parameter will be evaluated as `True`. Because of this, if you are using multiple Run buttons in your project, only one can evaluate to `True` at a time. If you would like the value to persist, consider using a [Checkbox input](/docs/explore-data/cells/input-cells/text-number-slider-and-date-inputs#checkbox).

To connect the cells that run when a Run button has or has not been pressed, use the name of the button parameter in some conditional logic downstream, as shown in the gif below.

Run buttons are great for when you want your app users to be very intentional with a portion of an app. For example, you can require users to click a Run button in order to execute an expensive query.

Check out the example below:

In the screenshot above, the **SQL method** cell uses [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) to evaluate whether the Run button has been pressed, i.e. whether the `green_button` variable is `True` or `False`. When the Run button is pressed, `green_button` evaluates to `True`, and the query in the `{% if %}` statement is kicked off. If the button isn't pressed, the `{% else %}` statement evaluates when the cell executes, and a dummy query runs instead.

It's also possible to perform similar logic in a Python cell, as shown in the **Python method** cell in the screenshot. This cell uses [`hextoolkit`](/tutorials/connect-to-data/using-the-hextoolkit) to pull the data connection into the code cell, and similarly executes conditional code depending on whether or not the Run button has been pressed.

tip

Check out [this tutorial](/tutorials/connect-to-data/read-and-write-to-your-database#put-it-into-practice) for an example of using a Run button to writeback to your database!

#### On this page

* [Configure Run button inputs](#configure-run-button-inputs)
* [Usage](#usage)