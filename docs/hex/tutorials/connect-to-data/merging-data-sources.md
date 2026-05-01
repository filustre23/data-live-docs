On this page

# Merging data sources

tip

Link to [Hex Project](https://app.hex.tech/hex-public/app/3336b9e6-4a58-4fc0-8365-cf7202ec1092/latest)

A common challenge data analysts face is combining several datasets from different sources (a csv, a database, an API endpoint) into one merged dataset to do analysis on. Even when you have matching keys, it can be frustrating to not be able to just JOIN them together like tables in a database.

Say no more, analysts. This tutorial demonstrates how to merge data from diverse sources in SQL using Hex's Dataframe SQL feature.

If you want to jump straight into the documentation, [here is more on Dataframe SQL](/docs/explore-data/cells/sql-cells/sql-cells-introduction).

## Step 1: Upload and read a csv file[​](#step-1-upload-and-read-a-csv-file "Direct link to Step 1: Upload and read a csv file")

Before we merge anything, we need to get all our data into the same workspace. We'll start with a csv.

We've uploaded a csv file to this Hex project by dragging and dropping it into the **Files** tab in the project sidebar. Now `avocado.csv` appears in the files list, which contains avocado prices from 2015-2018 (find the file [here](https://www.kaggle.com/neuromusic/avocado-prices)).

Once the file has been uploaded, you can easily get the code to reference it with pandas by selecting **Copy file reference** option in the ellipses dropdown for the file.

This option copies `pd.read_csv("avocado.csv")` to our clipboard, which we can then use to create a dataframe by pasting into a new python cell.

```
avocado = pd.read_csv("avocado.csv")
```

## Step 2: Get some more data[​](#step-2-get-some-more-data "Direct link to Step 2: Get some more data")

Now that we have csv data loaded into the project, we'll add another data source — a SQL database.

We'll use a SQL cell to do this. There's an image below, but you can click **View** in the top bar to see the actual cell and query.

Note that we've [parameterized](/docs/explore-data/cells/using-jinja) the SQL query with the min and max dates from the avocado dataset, to make sure we're only querying relevant data. This isn't the main focus of this tutorial, but is a really powerful feature!

## Step 3: Merge the datasets with Dataframe SQL[​](#step-3-merge-the-datasets-with-dataframe-sql "Direct link to Step 3: Merge the datasets with Dataframe SQL")

Now that both data sources have been loaded into Hex as dataframes, they can be easily joined together using Dataframe SQL.

Add a new SQL Cell and select **Dataframes** as the Source instead of a database. Now, you can query any dataframes in the project as if they are tables in the same database.

We can easily JOIN the two datasets together on their date fields and return a merged result.

## What's next?[​](#whats-next "Direct link to What's next?")

Though it seems unlikely there's a relationship between avocado prices and air travel, this merged dataset could now be used in any Hex code or chart cells to find out. You can repeat this process with data from any source! As long as it can be turned into a dataframe, it can be easily joined with other data in your Hex projects.

Bonus: Because the result of the final query is also a dataframe, you can even run further SQL queries against it if you want to keep exploring in SQL.

#### On this page

* [Step 1: Upload and read a csv file](#step-1-upload-and-read-a-csv-file)
* [Step 2: Get some more data](#step-2-get-some-more-data)
* [Step 3: Merge the datasets with Dataframe SQL](#step-3-merge-the-datasets-with-dataframe-sql)
* [What's next?](#whats-next)