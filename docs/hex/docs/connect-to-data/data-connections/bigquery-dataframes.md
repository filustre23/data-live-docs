On this page

# BigQuery DataFrame integration

warning

As of October 2025, some parts of the Bigframe integration have been deprecated. [Learn more below](#deprecated-features).

BigQuery users can now take advantage of BigQuery DataFrames within Hex. Unlike standard Pandas DataFrames, these are not loaded into the memory of a Hex project. Operations on BigQuery DataFrames are executed on BigQuery’s infrastructure, enabling Hex users to work with large datasets without requiring additional memory in Hex.

To learn more about BigQuery DataFrames, visit the [BigQuery DataFrames docs](https://cloud.google.com/python/docs/reference/bigframes/latest).

## Create a BigQuery DataFrame session from a Python cell[​](#create-a-bigquery-dataframe-session-from-a-python-cell "Direct link to Create a BigQuery DataFrame session from a Python cell")

To create a BigQuery DataFrame session from a Python cell, create a cell with the following code, replacing the argument of the get\_data\_connection method with the name of your connection.

```
import hextoolkit  
hex_bigquery_conn = hextoolkit.get_data_connection('Demo Bigquery')  
session = hex_bigquery_conn.get_bigquery_session()
```

You can also generate a Python cell with this code from the “Get BigQuery session” button in the [Data browser](/docs/explore-data/data-browser) menu:

Once your connection is established, you can interact with BigQuery DataFrames in python cells - just reference “session” in places where you might reference the [bigframes.pandas package](https://cloud.google.com/python/docs/reference/bigframes/latest). For example, to query data, you can write:

```
df1 = session.read_gbq("select * from demo_data.cc_cards")
```

## Working with BigQuery DataFrames[​](#working-with-bigquery-dataframes "Direct link to Working with BigQuery DataFrames")

BigQuery DataFrames will, by default, not be brought into memory in Hex. If you want to bring the DataFrame into Hex memory, you can use the function “to\_pandas” to convert it into a Pandas DataFrame in memory.

Note that BigQuery DataFrames uses a BigQuery session, which is tied to a [BigQuery location](https://cloud.google.com/bigquery/docs/locations). To learn more about locations and how to set them appropriately, check out [Google’s docs on BigQuery DataFrames.](https://cloud.google.com/python/docs/reference/bigframes/latest#locations)

## Deprecated features[​](#deprecated-features "Direct link to Deprecated features")

As of October 2025, some parts of the Bigframes integration have been deprecated, in order to reduce system complexity, and simplify how projects can be run.

In particular, it is no longer possible to **return a Bigframe dataframe from a SQL cell**. If you were relying on this feature, you can either:

1. Use [query mode](https://learn.hex.tech/docs/explore-data/cells/sql-cells/sql-cells-introduction#when-should-i-use-query-mode-vs-dataframe-mode) to work with large datasets
2. Create a Bigframe dataframe with Python if you intend to operate on this object via Python. You'll need to convert the final Bigframe dataframe to a Pandas dataframe to use it in a chart cell, with the `to_pandas()` method.

#### On this page

* [Create a BigQuery DataFrame session from a Python cell](#create-a-bigquery-dataframe-session-from-a-python-cell)
* [Working with BigQuery DataFrames](#working-with-bigquery-dataframes)
* [Deprecated features](#deprecated-features)