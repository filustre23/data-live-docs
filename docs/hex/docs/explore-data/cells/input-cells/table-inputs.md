On this page

# Table inputs

Use table inputs to enable common spreadsheet-like input workflows.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to create and edit input cells.
* Users with **Can View App** permissions and higher can interact with input cells in published [Apps](/docs/share-insights/apps/apps-introduction).

## Configure table inputs[​](#configure-table-inputs "Direct link to Configure table inputs")

You can start from an empty table and fill in values individually or you can pre-populate a Table with a defined dataframe.

tip

If you pre-populate a Table, only the first 250 rows of the referenced dataframe will be included.

Table inputs return as Pandas DataFrames, and can be accessed and manipulated the same as any others:

Currently, columns can be configured as string, numeric, & boolean data types. Additional column formatting and manipulation can be done downstream in code.

## Pre-populate Input tables[​](#pre-populate-input-tables "Direct link to Pre-populate Input tables")

If you pre-populate an Input Table and make subsequent changes, you can recover the original input data by pressing the **Reset data** button at the top of the table.

Changes made to an Input Table are always preserved until a user presses the **Reset data** button to ensure that user input is never lost. If a user has changed table values, those edits will be retained even if they re-run the project.

The output of any Input Table is saved as a separate DataFrame, so you don't have to worry about accidentally overwriting your original data.

#### On this page

* [Configure table inputs](#configure-table-inputs)
* [Pre-populate Input tables](#pre-populate-input-tables)