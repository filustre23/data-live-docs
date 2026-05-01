On this page

# Writeback cells

Write dataframes back to your database with Writeback cells.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) and access to a data connection with writeback enabled.

Writeback cell types are a unique cell type that let you write dataframes back to your database. These cells provide a simple and easy method of doing so, without the need for more advanced SQL queries or external Python libraries.

## Allow writeback on a data connection[​](#allow-writeback-on-a-data-connection "Direct link to Allow writeback on a data connection")

Writeback cells work on a double opt-in model:

* Each data connection must specifically be configured to allow writeback.
* The credentials used in the data connection must have permission to writeback to the database.

To enable writeback for a connection, an Admin must head to the **Data Sources** section of Settings and enable the **Allow use in Writeback cells** option. You can also choose to only share this connection with a certain group of people using the permissions outlined [here](/docs/administration/workspace_settings/workspace-assets#understand-shared-asset-permissions).

### Supported data connections[​](#supported-data-connections "Direct link to Supported data connections")

Some data connection types are not supported in Writeback cells.

info

Athena, Clickhouse, Starburst, Transform, Trino, and MotherDuck connectors are not supported in Writeback cells.

The Writeback cell can be used with the following data connection types:

* AlloyDB
* BigQuery
* Google CloudSQL (all dialects)
* Databricks
* MariaDB
* Materialize
* MySQL
* Postgres
* Presto
* Redshift
* Snowflake
* SQL Server

## Writeback to a database[​](#writeback-to-a-database "Direct link to Writeback to a database")

A Writeback cell can be created from the **Add cell** menu. Once the cell has been created, you will be prompted to select a connection, database, and schema to writeback to, as well as two key options:

* To overwrite the specified table if it already exists or append data (inserting new rows) to it. For both of these options, the table will be created if it does not yet exist.
* A static name for the table or a dynamic name for the table, based on a Python variable.

caution

Dynamic table names that rely on a variable with many possible values can lead to the creation of many tables in your database. These tables will exist until they are dropped manually.

When the cell is run, the dataframe will be written back to the database and the cell will return metadata regarding the writeback.

### Configure write mode options[​](#configure-write-mode-options "Direct link to Configure write mode options")

By default, Writeback cells have write mode turned off in order to avoid continually writing to your database. If you do not change the **Write mode** option, Writeback cells will *only* execute if you manually run the cell.

In addition to the manual method, there are three different automated write mode settings for Writeback cells, which can be independently enabled after selecting the **Write mode** menu at the upper-right of the cell:

* **Notebook session**: The dataframe will be written when the cell is executed in by a user with "Can Edit" permissions while developing. When this setting is off, developers can still manually run the cell to writeback to the database.
* **App session**: The dataframe will be written when the cell is run in a Published App.
* **Scheduled run**: The dataframe will be written when the cell is run during scheduled runs of the project.

### Writeback to a database via code[​](#writeback-to-a-database-via-code "Direct link to Writeback to a database via code")

Hex also provides a Python package (`hextoolkit`) that makes it easier to write to your database. This can be useful if you need to wrap the writeback code in more fine-grained, pythonic, logic.

```
import hextoolkit  
hex_data_connection = hextoolkit.get_data_connection(<"Data Connection Name">)  
writeback_metadata = hex_data_connection.write_dataframe(df=<dataframe_name>, database="<database_name>", schema="<schema_name>", table="<table_name>", overwrite=<True/False>)
```

It is also possible to write to your database using completely custom logic [using Python](/tutorials/connect-to-data/read-and-write-to-your-database) and a connector library for your database.

#### On this page

* [Allow writeback on a data connection](#allow-writeback-on-a-data-connection)
  + [Supported data connections](#supported-data-connections)
* [Writeback to a database](#writeback-to-a-database)
  + [Configure write mode options](#configure-write-mode-options)
  + [Writeback to a database via code](#writeback-to-a-database-via-code)