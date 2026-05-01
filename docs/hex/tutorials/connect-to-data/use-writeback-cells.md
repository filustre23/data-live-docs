On this page

# Writeback to your database

tip

You can access the companion app for this tutorial [here](https://app.hex.tech/hex-public/app/baf06855-80fe-4a20-aa74-066cf691c425/latest).

Hex has native [Writeback cells](/docs/explore-data/cells/data-cells/writeback-cells) which allow you to write a dataframe directly to a database. This tutorial walks through how to create (or replace) tables with the results of a dataframe, as well as how to append results to an existing table.

If you need more control over how Hex writes to your database, you can always use Python to establish a connection to your database and writeback data a la `sqlalchemy` and the like, or using the `hextoolkit`. See [this tutorial](/tutorials/connect-to-data/read-and-write-to-your-database) for using Python connectors and [this tutorial](/tutorials/connect-to-data/using-the-hextoolkit) for the toolkit!

For this tutorial, we will be using COVID-19 vaccination rate data from the CDC's COVID Data Tracker accessed via their their API. More info on the dataset and how to access it can be found on their website [here](https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-County/8xkx-amqh).

## Append data to an existing table[​](#append-data-to-an-existing-table "Direct link to Append data to an existing table")

### The existing table[​](#the-existing-table "Direct link to The existing table")

We have a table in our database that contains COVID vaccination data by U.S. County. We originally downloaded a CSV of [the dataset](https://covid.cdc.gov/covid-data-tracker/#county-view?list_select_state=all_states&data-type=CommunityLevels) and wrote it back to our database.

But, the data is updated by the CDC weekly, so we want to append the new data to our existing data without the need to overwrite the existing table.

### Get the new data[​](#get-the-new-data "Direct link to Get the new data")

To grab the new data, we will be querying our recently created table to get the most recent date, and then grabbing all results after that date:

```
select max(date)::DATE as max_date from hex_app_data.hex_production.county_covid_vaccinations
```

With our max date in hand, we can use it in our request and add the returned data into a dataframe.

```
# Grab the max date value from the dataframe  
max_date = max_date_dataframe.iloc[0,0]  
# Format the date to be YYYY-MM-DD  
max_date = date(max_date.year, max_date.month, max_date.day)  
# Make the request to get the new data  
# The CDC's API leverages SoQL syntax: https://dev.socrata.com/docs/functions/#,  
data = get("https://data.cdc.gov/resource/8xkx-amqh.json?$where=date > '" + str(max_date) + "'&$order=recip_county, date DESC&$limit=5000000")  
# Iterate through the response json and turn it into a dataframe  
new_data = pd.DataFrame([entry for entry in data.json()])  
new_data.head()
```

### Write the data back[​](#write-the-data-back "Direct link to Write the data back")

Now that our data is in a dataframe, we can use a writeback cell and the **Append to** option to add it to our existing table. It's important that we use the same name as our existing table, in order to avoid creating a new one.

When we run this cell, we will see metadata about the writeback, and our table will be updated with the newest data.

### Schedule the writeback[​](#schedule-the-writeback "Direct link to Schedule the writeback")

Having an updated table is great, but having an updated table every week is even better! Conveniently, Writeback cells have a [Write mode](/docs/explore-data/cells/data-cells/writeback-cells#configure-write-mode-options) option that allows us to only perform the writeback during a scheduled run.

This dataset is updated on Wednesdays, so we have created a schedule to run at 11:59 p.m. on Wednesdays, appending the newest data to table weekly, without any additional effort.

## Drop tables[​](#drop-tables "Direct link to Drop tables")

Writeback cells make it easy to create new tables in your database, but this also makes it easy to generate unwanted tables, especially during development. Hex will not drop these tables automatically, but it's possible to do so using DROP statements in a SQL Cell.

### Find tables to drop[​](#find-tables-to-drop "Direct link to Find tables to drop")

Many SQL dialects have metadata tables that can be queried in order to find what tables exist in a particular database or schema. On our Snowflake connection, for example:

```
select table_name from information_schema.tables where table_schema = 'HEX_DEVELOPMENT';
```

This can make it especially easy to find tables that were written back that can be dropped, especially if you choose to utilize a single schema or naming structure for tables created via Hex.

### Create a dynamic drop statement[​](#create-a-dynamic-drop-statement "Direct link to Create a dynamic drop statement")

With a list of table names coming from one or more queries, we can create a drop statement connected to an input parameter, to make it easy to drop tables in Hex. If you are not already familiar with this concept, there is a thorough tutorial on parameterized queries [here](/tutorials/connect-to-data/parameterize-sql).

The first step here will be to create a [Dropdown input](/docs/explore-data/cells/input-cells/dropdown-inputs#dynamic-values) that connects to our table names query. In order to avoid accidentally dropping tables, we are also going to connect our drop statement to a [Run button](/docs/explore-data/cells/input-cells/run-button). Once these are created, we can reference them both in a drop query that runs when our run button is selected

```
{% if table_dropper %}  
DROP TABLE HEX_APP_DATA.HEX_DEVELOPMENT.{{ droppable_tables | sqlsafe }}  
{% else %}  
select 'Click the "Drop it!" button to drop the table.'  
{% endif %}
```

warning

If you use the `sqlsafe` flag to force a parameterization like this, you are removing the protection that prepared statements offer against sql injection!

## Conclusion[​](#conclusion "Direct link to Conclusion")

Writeback cells are a simple and powerful option for making your dataframes more permanent by storing them in your database, all without the complexities of DDL queries or Python connection libraries. Hex can also make it easy to clean up these tables so that you can keep things organized, and avoid incurring additional storage costs for tables you might not need.

#### On this page

* [Append data to an existing table](#append-data-to-an-existing-table)
  + [The existing table](#the-existing-table)
  + [Get the new data](#get-the-new-data)
  + [Write the data back](#write-the-data-back)
  + [Schedule the writeback](#schedule-the-writeback)
* [Drop tables](#drop-tables)
  + [Find tables to drop](#find-tables-to-drop)
  + [Create a dynamic drop statement](#create-a-dynamic-drop-statement)
* [Conclusion](#conclusion)