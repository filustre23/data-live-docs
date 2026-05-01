On this page

# Debug Apps

Use the debug view to track down errors or diagnose slow-running apps.

info

* Available on all pricing plans.
* Users will need **Can Explore** project permissions.

The debug view lets users access the notebook behind a run of the published App, including the current value of inputs, and any error messages. While in the debug view, the App is interactive (for example, input cells can be updated) while the Notebook is in a read-only state.

This mode can also be useful for understanding app run performance, since it's possible to see all cells that are run when the App is run.

To enter the debug view, use the three dot menu on the app, or the button in the error modal.

## Cell run behavior in apps[​](#cell-run-behavior-in-apps "Direct link to Cell run behavior in apps")

When running a published App, Hex skips running cells that are not used by the App, to improve the performance of the App and reduce unnecessary queries against the warehouse.

Skipped cells will be indicated in the debug view with the "Skipped" label.

Hex follows the following rules when choosing which cells to skip:

* Python cells, SQL cells that mutate the database, and writeback cells will never be skipped
* A cell must not be included in the app and also have no dependent cells included in the App in order to be eligible to be skipped

#### On this page

* [Cell run behavior in apps](#cell-run-behavior-in-apps)