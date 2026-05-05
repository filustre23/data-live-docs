On this page

# Syncing from Snowflake Semantic Views

Snowflake Semantic Views are a way to define business metrics and logic directly in your database, using a native schema-level object. For more information, see [documentation](https://docs.snowflake.com/en/user-guide/views-semantic/overview#interfaces-for-working-with-semantic-views).

info

Snowflake Semantic Views is in **beta** on [Team and Enterprise plans](https://hex.tech/pricing/).

Reach out to [[email protected]](/cdn-cgi/l/email-protection#12616762627d6066527a776a3c6677717a) to learn more or [request a demo](https://hex.tech/request-a-demo/).

With Snowflake Semantic Views, you can explore and analyze trusted measures, dimensions, and joins defined in Snowflake — all from Hex’s no-code [Explore](/docs/share-insights/explore) experience. This means less time rewriting calculations and reconciling discrepancies, and more time digging deeper into analyses and delivering consistent insights to the business.

## Concepts[​](#concepts "Direct link to Concepts")

To effectively leverage your Snowflake Semantic Views within Hex, check how key concepts translate between the two platforms.

| **Snowflake** | **Hex** |
| --- | --- |
| semantic view | semantic project |
| table | model |
| relationship | join |
| fact | dimension |
| dimension | dimension |
| metric | measure |

## Viewing transient joins[​](#viewing-transient-joins "Direct link to Viewing transient joins")

Only the join paths originating from the currently selected model are shown. Intermediary models in a join sequence will only display subsequent joins. When the final model in a join is selected, no preceding joins are shown in the [Explore](/docs/share-insights/explore) interface.

For example, consider the join sequence: `CUSTOMERS` → `ORDERS` → `PRODUCT`.

Selecting `CUSTOMERS`: shows joins to `ORDERS` and `PRODUCT`.

Selecting `ORDERS`: shows only the join to `PRODUCT` (with `ORDERS` as the starting point).

Selecting `PRODUCT`: shows no joins.

### Best Practices for Relationship Naming[​](#best-practices-for-relationship-naming "Direct link to Best Practices for Relationship Naming")

Provide clear and descriptive names for relationships when defining them in Snowflake. Snowflake will auto-generate default names if none are given, which may be unclear when viewed in Hex. In Explore, relationship names appear in the format `<relationship_name> (logical_table_name)`. For example: `ACCOUNT_TO (CUSTOMERS)`.

## Prepare the project for import into Hex[​](#prepare-the-project-for-import-into-hex "Direct link to Prepare the project for import into Hex")

Users can create a Semantic View in Snowflake Cortex Studio, or use [DDL commands](https://docs.snowflake.com/en/sql-reference/sql-ddl-summary) from a Hex notebook. We recommend using DDL statements to create Semantic Views.
Please reference the Snowflake documentation on how to [use SQL to set up a Semantic View](https://docs.snowflake.com/en/user-guide/views-semantic/sql).

## Supported Features[​](#supported-features "Direct link to Supported Features")

Not all Snowflake features translate directly in Hex; check the following table to see what is supported.

| Feature | Supported |
| --- | --- |
| **Dimension features** |  |
| Time, String, Number, Boolean | ✅ |
| **Measure features** |  |
| Count, Count distinct, Sum, Average, Min, Max, String, Time, Boolean | ✅ |
| Derived metrics | ❌ |
| **Join features** |  |
| left join | ✅ |
| inner join | ❌ |
| **Other features** |  |
| Filters | ❌ |

#### On this page

* [Concepts](#concepts)
* [Viewing transient joins](#viewing-transient-joins)
  + [Best Practices for Relationship Naming](#best-practices-for-relationship-naming)
* [Prepare the project for import into Hex](#prepare-the-project-for-import-into-hex)
* [Supported Features](#supported-features)