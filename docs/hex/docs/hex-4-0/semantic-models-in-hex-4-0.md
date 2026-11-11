On this page

# Semantic querying in Hex 4.0 reference

Semantic queries are YAML files that retrieve data from [semantic models](/docs/connect-to-data/semantic-models/intro-to-semantic-models) in Hex 4.0 projects. This reference covers their configuration, syntax, and supported operations.

## Declaring a semantic project[​](#declaring-a-semantic-project "Direct link to Declaring a semantic project")

Before querying a semantic project, declare it under `semantic_projects` in your project's `hexdag.yaml`. The Hex agent adds this declaration automatically when it first queries a semantic project, but you can also add it manually.

```
databases:



analytics:



type: hex.dataconnection



db_id: 2f1b665d-73f6-4e5f-9ae8-282e6fc75493



name: Analytics



connection_type: snowflake



semantic_projects:



commerce:



id: 0b6a3c1e-7d2f-4f7a-9a51-3c1d2b4e5f60



database: analytics
```

* `commerce` is the alias referenced by queries.
* `id` is the semantic project's ID, not its name.
* `database` references the connection under `databases` that the semantic project uses.

## Query files[​](#query-files "Direct link to Query files")

Semantic queries live in `dataflow/` and use the `.query.yml` or `.query.yaml` extension. Each file produces a table named after the file.

For example, `monthly_revenue.query.yml` produces `monthly_revenue`.

Every query has three required top-level keys:

| Key | Description |
| --- | --- |
| `semantic_project` | Alias declared in `hexdag.yaml`. |
| `base` | Starting model or view. |
| `transforms` | Operations applied in order. |

For models, `base: orders` is shorthand for `base: { model: orders }`. Views require `base: { view: all_sales, reference_by: name }`.

Unrecognized keys at any level cause validation errors.

## Transforms[​](#transforms "Direct link to Transforms")

Each transform is an **aggregate** or **select** step. Steps run in order, with each operating on the previous step's output.

### Aggregate[​](#aggregate "Direct link to Aggregate")

Aggregate steps group and summarize data. They require `aggregate`, `group_by`, or both.

```
transforms:



- aggregate:



- measure: total_revenue



alias: revenue



- expr: "countdistinct(customer_id)"



alias: customers



group_by:



- dimension: created_at



time_unit: month



- dimension: region



model: customers



where:



- expr: "status = 'complete'"
```

| Key | Description |
| --- | --- |
| `aggregate` | Modeled measures or aggregate expressions. |
| `group_by` | Dimensions or expressions to group by. |
| `where` | Filters applied before grouping and aggregation. |
| `having` | Filters applied after aggregation, using output column names. |
| `order_by` | Sort order. |
| `limit`, `offset` | Limit and paginate results. `offset` requires `limit`. |
| `detail` | Extra row-level columns. |
| `append_detail` | Adds all base-model dimensions as detail columns. Default `false`. |

Additional options:

* **`alias`:** Optional on measures, required on expressions. Not supported on dimensions, so they keep their own name.
* **`time_unit`:** Groups dates by intervals such as `day`, `week`, `weekmonday`, `month`, `quarter`, or `year`. The output retains the dimension's original name.
* **`binning`:** Groups numeric dimensions into bins using `maxbins`, `step`, `minstep`, or `base`.
* **`model`:** References a field from a joined model. Without it, fields resolve against the base model.

Modeled measures are already aggregates, so expressions like `sum(total_revenue)` are invalid when `total_revenue` is a modeled measure.

### Select[​](#select "Direct link to Select")

Select steps add or choose columns without aggregating.

```
transforms:



- select:



- dimension: region



- expr: "total_revenue / order_count"



alias: avg_order_value



append: false
```

| Key | Description |
| --- | --- |
| `select` | Dimensions or expressions to return. |
| `append` | Default `true`: retain existing columns. Set `false` to return only selected columns. |
| `invalid_items` | `fail` or `skip`. Default `fail`. |
| `where`, `order_by`, `limit`, `offset` | Same as aggregate steps. |

Select steps can reference columns produced by previous aggregate steps. On a base model, `append: true` includes existing dimensions.

A select step preserves the number of rows unless it includes `where` or `limit`. Division by zero returns null.

### Filters and sorting[​](#filters-and-sorting "Direct link to Filters and sorting")

```
where:



- expr: "status = 'complete'"



having:



- "revenue > 1000"



order_by:



- expr: revenue



direction: desc



limit: 10
```

* `where` filters rows before grouping and aggregation, even when it appears after `group_by` in the YAML.
* Multiple `where` conditions are combined with AND.
* `having` filters aggregated results using output column names.
* `order_by` defaults to ascending order.
* `offset` can be used with `limit` for pagination.

### Top N with "Other"[​](#top-n-with-other "Direct link to Top N with \"Other\"")

Use `lump` to keep the top N dimension values and group the rest into "Other":

```
group_by:



- dimension: product



lump:



window_function: rank



order_by:



measure: revenue



order_direction: desc



predicate: rank <= 5



other_label: Other
```

The predicate can use `rank` (the window result), `original_value` (the dimension value), and `measure_value`. Omit `other_label` to drop the non-matching values, or put a `lump_by` item in `where` to filter to the top N before aggregating.

Supported window functions: `row_number`, `rank`, `dense_rank`, `percent_rank`, `cume_dist`, `ntile`, `lag`, and `lead`. `window_args` passes arguments (e.g. `[10]` for `ntile`), and `include_window_value: { alias, other_value }` adds the result as a column.

## Querying views[​](#querying-views "Direct link to Querying views")

Views use display paths instead of underlying model field names.

```
semantic_project: commerce



base:



view: all_sales



reference_by: name



transforms:



- aggregate:



- measure: Sales.Revenue



alias: revenue



group_by:



- expr: Buyers.Region



alias: region
```

The `view` key uses the view's name, not its display title. Field paths use group and field titles separated by dots, such as `Sales.Revenue`. Nested groups include parent titles.

Paths are case-sensitive. Wrap components containing spaces or dots in backticks, such as `` Sales.`Gross.Total` `` . Renaming a field or group changes its path, and duplicate paths cause errors.

**Restrictions on the first transform of a view query:**

* `aggregate` supports modeled measures only, not expression aggregates.
* `select` and `group_by` support dimensions or expressions with aliases.
* `where` supports expressions only.
* Fields must be explicitly selected or aggregated.
* Raw SQL, `model`, `segment`, `time_unit`, `binning`, and `append: true` are unsupported.
* Only fields exposed by the view can be referenced.

Later transforms follow the normal rules. To group dates, use an expression like `` truncmonth(Sales.`Order Date`) `` instead of `time_unit`.

## Expressions and parameters[​](#expressions-and-parameters "Direct link to Expressions and parameters")

Expressions use the [Hex Calc](/docs/explore-data/cells/calculations) language, not warehouse SQL. The Hex agent writes these for you, but the reference lists the available functions if you need them.

Use `{{name}}` inside expressions to reference project parameters or single values computed earlier in the project:

```
where:



- expr: "region = {{region}}"
```

* References are passed as typed values.
* Quoting `'{{region}}'` makes it literal text.
* Referenced values must exist in the project.
* Changes to referenced values trigger query reruns.

## Troubleshooting[​](#troubleshooting "Direct link to Troubleshooting")

| Issue | Resolution |
| --- | --- |
| Semantic project not declared | Check the alias under `semantic_projects` in `hexdag.yaml`. |
| Definition file missing | Confirm the project is linked in `hexdag.yaml`. |
| Connection identity mismatch | Verify that `database` references the semantic project's connection. |
| Unknown measure or dimension | Check the field name or add `model:` for joined-model fields. |
| Unknown function | Use a supported Hex Calc function. |
| Unsupported top-level key | Move `where`, `limit`, and other operations inside a transform. |
| Invalid base | Use a model name, `{ model: … }`, or `{ view: …, reference_by: name }`. |
| Unknown or ambiguous view field | Check display paths, capitalization, and backticks. |
| Unsupported view options | Check the first-transform restrictions above. |
| Unknown query input | Confirm the referenced `{{name}}` exists. |
| A view field stopped working | Check whether its display title changed. |

## Callouts[​](#callouts "Direct link to Callouts")

* Semantic queries cannot read other project tables. Combine results in subsequent SQL or Python steps.
* Semantic queries are part of the [Hex 4.0 beta](/docs/hex-4-0/what-is-hex-4-0).

#### On this page

* [Declaring a semantic project](#declaring-a-semantic-project)
* [Query files](#query-files)
* [Transforms](#transforms)
  + [Aggregate](#aggregate)
  + [Select](#select)
  + [Filters and sorting](#filters-and-sorting)
  + [Top N with "Other"](#top-n-with-other)
* [Querying views](#querying-views)
* [Expressions and parameters](#expressions-and-parameters)
* [Troubleshooting](#troubleshooting)
* [Callouts](#callouts)