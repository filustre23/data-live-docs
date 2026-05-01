On this page

# Hex's built-in hextoolkit package

tip

Check out the companion Hex project for this tutorial [here](https://app.hex.tech/hex-public/app/de39ad12-4389-4980-a4ce-76cf4e1eaf2a/latest)!

`hextoolkit` is a package usable only from within Hex projects that allows for programmatic access to data connections and other Hex functionality. We'll be continually updating the `hextoolkit`, so keep an eye on our release notes for the latest info. This tutorial will guide you through a bit of what is possible!

## Import the package[​](#import-the-package "Direct link to Import the package")

The `hextoolkit` package comes pre-installed in all Hex projects, and gets imported similar to any other module.

```
import hextoolkit as htk
```

## Access data connections[​](#access-data-connections "Direct link to Access data connections")

Any project or imported workspace connections can be referenced in Python code, retrieving the connection using its name. You can find these data connections in the **Data sources** tab in the left sidebar of a project, and import those you need to access.

```
my_snowflake_connection = htk.get_data_connection("Demo Snowflake")
```

`HexDataConnection` objects contain basic metadata about the connection, most notably:

* **name**: the connection name
* **id**: the connection ID
* **conn\_type**: the connection type (e.g. "snowflake", "postgres", etc.)
* **allow\_writeback**: whether or not writeback is enabled for the connection

There are separate subclasses of `HexDataConnection` for different connection types (`HexPostgresConnection`, `HexSnowflakeConnection`, etc.), some of which may have slightly different functionality (e.g. only `HexSnowflakeConnection` objects have methods for getting a Snowpark session).

It is worth noting that the `hextoolkit` does **not** allow access to database credentials from these objects.

You can display the type and \_\_dict\_\_ attribute of one of the objects to see all of its attributes:

```
display(type(my_snowflake_connection))  
display(my_snowflake_connection.__dict__)  
  
hextoolkit.hex_data_connection.HexSnowflakeConnection  
{'name': 'Demo Snowflake',  
 'id': '42c8668e-d750-4b7b-9adf-d6697c78a125',  
 'connection_type': 'snowflake',  
 'enable_snowpark': True,  
 'allow_writeback': False}
```

### Run queries[​](#run-queries "Direct link to Run queries")

Once a `HexDataConnection` object has been created, you can invoke the `query` method to execute an input string as a SQL query against a database. The results of the query will be returned as a dataframe, just like our SQL Cells - Jinja syntax is also supported! Here, the `usertypes_input` variable is would be defined upstream in an Input cell or another Python cell.

```
query_string = '''select tripduration,  
start_station_id,  
start_station_name,  
end_station_id,  
end_station_name,  
usertype  
from demo_data.demos.citibike_trips  
where usertype = {{ usertypes_input }}  
limit 10  
'''  
query_results = my_snowflake_connection.query(query_string)
```

caution

Because the `query` method accepts a string directly, these queries are vulnerable to SQL injection. Extreme caution should be used when accepting user input that is passed to one of these methods. This is equivalent to using a `sqlsafe` Jinja filter when [referencing a variable in a SQL cell](/docs/explore-data/cells/using-jinja#using-variables-in-queries).

### Executing SQL in a for loop[​](#executing-sql-in-a-for-loop "Direct link to Executing SQL in a for loop")

Because `hextoolkit` executes SQL queries in Python, workflows such as running a query in a for loop are now possible in Hex! This means we can run the same query multiple times or iterate through an array of values passing them into queries separately. For simplicity, we'll run the same query repeatedly and concatenate all of the results into a single dataframe. In this example, we'll be taking several samples of a larger dataset using Snowflake's [sample](https://docs.snowflake.com/en/sql-reference/constructs/sample.html) functionality. Normally, this would require writing out and unioning multiple queries, but it's relatively easy with a simple loop!

```
samples = 7  
sample_probability = 1  
# Create a dataframe to append results too  
data = pd.DataFrame()  
  
for samp in range(samples):  
    subset = my_snowflake_connection.query("SELECT * FROM demo_data.demos.electronics_retail SAMPLE ({{sample_probability}})")  
    # Append the subset to the existing dataframe  
    data = pd.concat([data, subset], ignore_index=True)  
  
data
```

This will create seven distinct sample sets (from seven query runs!) that now exist in a single dataframe, all from the work of a simple for loop. The applications here are endless!

### Execute writebacks[​](#execute-writebacks "Direct link to Execute writebacks")

For connections with writeback enabled, the `write_dataframe` method allows you to write a dataframe back to your database, from the `HexDataConnection` object. This replicates the functionality of [Writeback cells](/docs/explore-data/cells/data-cells/writeback-cells). To keep things very explicit when writing back, all arguments are required (meaning you must explicitly specify `database=None` when using a connection that does not support multiple databases).

```
my_snowflake_connection.write_dataframe(  
     df=my_dataframe, database="TEST_DB", schema="PUBLIC", table="WRITEBACK_EXAMPLE", overwrite=True)
```

### Snowpark sessions and DataFrames[​](#snowpark-sessions-and-dataframes "Direct link to Snowpark sessions and DataFrames")

For Snowflake connections with Snowpark enabled, you can also use the connection object to fetch a fully functional, authenticated Snowpark `Session` object.

```
snowpark_session = my_snowflake_connection.get_snowpark_session()
```

The query method also accepts an optional `output_type` argument, which allows you to fetch results as a Snowpark DataFrame.

```
my_snowflake_connection.query(query_string, output_type="snowpark")
```

For more information on using Snowpark with Hex, see our documentation on using [Snowpark in a Hex project](/docs/connect-to-data/data-connections/snowpark#use-snowpark-in-a-hex-project).

### BigQuery DataFrames Session - BETA[​](#bigquery-dataframes-session---beta "Direct link to BigQuery DataFrames Session - BETA")

For BigQuery connections, you can also use the connection object to fetch a fully functional, authenticated BigQuery `Session` object.

```
hex_bigquery_conn = hextoolkit.get_data_connection('My data connection')  
session = hex_bigquery_conn.get_bigquery_session()
```

For more information on using BigQuery DataFrames with Hex, see our documentation on using [BigQuery DataFrames in a Hex project](/docs/connect-to-data/data-connections/bigquery-dataframes).

## Run dataframe SQL[​](#run-dataframe-sql "Direct link to Run dataframe SQL")

The `query_dataframes` function allows you to mimic querying a dataframe from a SQL cell using pure Python.

```
import seaborn as sns  
  
penguins = sns.load_dataset("penguins")  
htk.query_dataframes("select * from penguins limit 100")
```

## Get kernel information[​](#get-kernel-information "Direct link to Get kernel information")

`hextoolkit` also provides an API to get kernel information, including CPU count and memory limit in bytes.

```
import hextoolkit as htk  
  
htk.kernel.cpu_count()  
  
htk.kernel.memory_limit()
```

This functionality is limited to the Python implementation of `hextoolkit`.

## hextoolkit in R Projects[​](#hextoolkit-in-r-projects "Direct link to hextoolkit in R Projects")

The `hextoolkit` is also available in R projects, with similar functionality. You can view examples of the `hextoolkit` in the companion R app [here](https://app.hex.tech/hex-public/app/13ca8de8-ec31-4118-a02c-f82f6821b3f9/latest).

#### On this page

* [Import the package](#import-the-package)
* [Access data connections](#access-data-connections)
  + [Run queries](#run-queries)
  + [Executing SQL in a for loop](#executing-sql-in-a-for-loop)
  + [Execute writebacks](#execute-writebacks)
  + [Snowpark sessions and DataFrames](#snowpark-sessions-and-dataframes)
  + [BigQuery DataFrames Session - BETA](#bigquery-dataframes-session---beta)
* [Run dataframe SQL](#run-dataframe-sql)
* [Get kernel information](#get-kernel-information)
* [hextoolkit in R Projects](#hextoolkit-in-r-projects)