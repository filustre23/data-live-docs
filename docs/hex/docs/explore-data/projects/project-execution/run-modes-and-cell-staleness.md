On this page

# Run modes and cell staleness

## Run modes[​](#run-modes "Direct link to Run modes")

The **Run mode** menu at the bottom lets you define how the cell executes in Notebook view.

Projects always run using Auto mode in the app run mode.

* **Auto**: Executes in an automatic, graph-based fashion, updating downstream and stale cells on each run. This is the default execution mode for logic, and the only execution mode for apps.
* **Cell + upstream:** Executes all upstream ancestor cells.
* **Cell only**: runs only the selected cell. This is basically the default traditional notebook behavior.
* **Cell + downstream:** runs only downstream descendent cells. Similar to Auto, but without updating stale cells.

## Cell staleness[​](#cell-staleness "Direct link to Cell staleness")

In any mode other than Auto, cells can become "stale" if an upstream ancestor cell has been run more recently than it.

In this example below, the project is in **Cell only** mode, and Cell 1 was run more recently than Cell 2 and 3. Thus, Cells 2 and 3 are considered "Stale" (note the orange squiggles):

In **Auto mode**, it will first re-run any stale upstream ancestor cells to make sure state is constant.

#### On this page

* [Run modes](#run-modes)
* [Cell staleness](#cell-staleness)