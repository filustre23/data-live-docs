On this page

# Execution Model

## Reactive graph-based execution model[​](#reactive-graph-based-execution-model "Direct link to Reactive graph-based execution model")

Hex projects are backed by a graph which links cells together and defines how they re-execute. This graph can be visualized in the [Graph View](/docs/explore-data/projects/project-execution/graph-view), activated by pressing the **Graph** button.

This differs from a traditional code notebook, and offers several advantages:

* **Interpretability**: it's easy to see how cells relate to each other, and how re-computes flow through the project. The Graph View is a visual "mind map" of the complexity you'd previously have to keep track of in your head.
* **Reproducibility**: Hex projects are reproducible by default, in that a given change will trigger a predictable, consistent set of re-computes through the graph.
* **Performance**: in logic development, but especially in published apps, this new [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) model is a massive leap forward. Input parameters will only trigger downstream, dependent logic, without any additional overhead or complexity.

## How cells link together[​](#how-cells-link-together "Direct link to How cells link together")

The graph is built automatically based on variable references in Python and SQL code. In the simple example below, we can see that `x` and `y` are both defined in and then referenced down in cells 2 and 3. These linkages are automatically inferred, without any need for user definition.

warning

Because the graph is dependent on detecting variable references, the usage of `globals()` to create variables or generate variable references is not advised. This can lead to unexpected behavior where cells do not execute reactively and/or error during execution.

## Skipping cells in published apps[​](#skipping-cells-in-published-apps "Direct link to Skipping cells in published apps")

In order to run apps as quickly as possible, Hex will skip the execution of some cells during app runs (including scheduled runs).

Cells that are required for the app to run successfully should never be skipped. Note the following rules to understand which cells will never be skipped:

* Cells that are [included in the app](/docs/share-insights/apps/app-builder#add-cells-to-your-app) are never skipped
* Code cells and Writeback cells are never skipped
* Cells whose outputs are referenced in a downstream cell are never skipped
* SQL cells that use DDL statements or anything other than a select statement are never skipped

If a cell does not meet any of the above criteria, it will be skipped. For example, a SQL cell that has not been added to the app and does not have any downstream dependencies will be skipped in an app run. Note that if a warehouse SQL cell's output is only referenced in other downstream warehouse SQL cells, the cell will still run in order to compile the query for [Chained SQL](/docs/explore-data/cells/sql-cells/sql-cells-introduction#chained-sql), but the query itself will not execute in your warehouse.

## Parallel cell execution[​](#parallel-cell-execution "Direct link to Parallel cell execution")

Hex will attempt to execute SQL cells in parallel while other cells run as soon as two conditions have been met:

1. All dependent upstream cells have run. For example, if an input parameter is referenced in a SQL cell, the input must run before the query executes.
2. All upstream writeback cells or non `select` statement queries using the same data connection have finished executing.

For SSH connections and Redshift connections, up to four queries will execute concurrently. For all other data connections, up to eight queries will execute concurrently.

info

If you need to disable parallel execution, toggle off the [allow execution reordering](/docs/explore-data/projects/environment-configuration/environment-views#cell-execution-order) setting in the environment tab

#### On this page

* [Reactive graph-based execution model](#reactive-graph-based-execution-model)
* [How cells link together](#how-cells-link-together)
* [Skipping cells in published apps](#skipping-cells-in-published-apps)
* [Parallel cell execution](#parallel-cell-execution)