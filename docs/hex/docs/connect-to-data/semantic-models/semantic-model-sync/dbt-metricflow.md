On this page

# Syncing from dbt MetricFlow

dbt MetricFlow is an open-source semantic model that powers dbt’s Semantic Layer. For more information, see [their documentation](https://docs.getdbt.com/docs/build/about-metricflow).

caution

The data connection used cannot have the [dbt semantic layer integration](/docs/connect-to-data/data-connections/dbt-integration) enabled. This will break prepared statements, which [Explore](/docs/share-insights/explore) requires for no code filtering.

## Concepts[​](#concepts "Direct link to Concepts")

To effectively leverage your dbt MetricFlow models within Hex, check how key concepts translate between the two platforms.

| MetricFlow | Hex |
| --- | --- |
| project | semantic project |
| semantic model | model |
| dimension | dimension |
| entity (primary, unique, natural, foreign) | dimension |
| foreign entity | join |
| measure, if create\_metric is set to “true” | measure |
| metric | measure |

## Prepare the project for import into Hex[​](#prepare-the-project-for-import-into-hex "Direct link to Prepare the project for import into Hex")

In order to successfully import dbt MetricFlow files into Hex, the following conditions are required:

1. **Specify project paths**

   In order to import the dbt MetricFlow YAML files correctly, each semantic project needs to specify the underlying data warehouse table. This is specified as `table: <value>` in a `config.meta.hex` section for the model:

   ```
   model: ref('customers')  
   config:  
     meta:  
       hex:  
         table: analytics.prod_core.customers
   ```

   The value should be in the format `database.schema.table` or `schema.table`. This is currently case-insensitive (with no quotation (””) characters).
2. **Ensure schema is up to date**

   Verify that all tables and columns referenced in the semantic project are present in the data connection's schema. It is recommended to add the needed columns to your data connection, refresh the schema, and then reference those newly added columns in your semantic project.

   Consider refreshing the data connection’s schema [on a schedule](https://learn.hex.tech/docs/connect-to-data/data-connections/data-connections-introduction#schedule-schema-refreshes).

   * If the semantic project is referencing a column that doesn’t yet exist in the data connection schema, then the import will skip any references column because Hex doesn’t have the correct type information. Add in a column type annotation as a workaround.
   * **Column type annotations**
     + If you’d prefer to avoid refreshing your data connection schema within Hex, you can specify the types directly in your dimension definitions like so:

       ```
       - name: "Customer Name"  
         expr: "customer_name"  
         type:  "categorical"  # @dtype: string
       ```

       - dtype is one of: numeric, string, boolean, date, timestamp, timestamptz

## Supported Features[​](#supported-features "Direct link to Supported Features")

Not all MetricFlow features translate directly in Hex; check the following table to see what is supported.

| Feature | Supported |
| --- | --- |
| **Dimension features** |  |
| Categorical, Time, Entity, Boolean, Numeric | ✅ |
| SCD Type II dimensions | ❌ |
| **Measure features** |  |
| Sum, Count, Count distinct, Average, Min, Max, Median, Sum boolean | ✅ |
| Percentile | ❌ |
| Measures with non-additive dimensions | ✅ |
| **Metric features** |  |
| Simple | ✅ |
| Cumulative | ✅ |
| Window | ✅ |
| Grain to date | ✅ |
| Ratio | ✅ |
| Derived | ✅ |
| Offsets for Ratio and Derived | ✅ |
| Conversion | ❌ |
| Metrics with fill\_nulls\_with | ✅ |
| Metric filters | ✅ |
| **Other features** |  |
| Time spines | ✅ |

#### On this page

* [Concepts](#concepts)
* [Prepare the project for import into Hex](#prepare-the-project-for-import-into-hex)
* [Supported Features](#supported-features)