On this page

# Query caching for performant projects

Use query caching to decrease load time and database spend.



tip

Check out the companion Hex project for this tutorial [here](https://app.hex.tech/hex-public/app/ccd5fd68-d9fc-4c25-83a8-dcf4dadbd68f/latest)!

### SQL query caching[​](#sql-query-caching "Direct link to SQL query caching")

In this tutorial, we take advantage of Hex's [query caching functionality](/docs/explore-data/cells/sql-cells/query-caching) to build a performant app for users to monitor Citi Bike usage in New York City.

SQL cells use cached results if your queries have been run by anyone in your workspace in the [set timeout window](/docs/explore-data/cells/sql-cells/query-caching#adjusting-cache-settings). Projects default to the workspace timeouts for the Notebook view and published apps, which are set by Admins and default to 60 minutes. You can override the workspace-level settings for a given project in the Environment tab of the left sidebar.

### Step 1: Configure project-level query caching settings[​](#step-1-configure-project-level-query-caching-settings "Direct link to Step 1: Configure project-level query caching settings")

We expect stakeholders to visit the published app throughout the week, and always want to be displaying the freshest data available. Our ETL schedules update these underlying tables daily, so we'll set the published app caching timeout to one day. As the users developing the Notebook behind the app, we don't necessarily need to be working with the freshest data as we're testing and rerunning the project. So, let's set the developing logic timeout to one week.

### Step 2: Pull in data from an expensive query[​](#step-2-pull-in-data-from-an-expensive-query "Direct link to Step 2: Pull in data from an expensive query")

We'll start by pulling the Citi Bike data into our project. This query returns the times and durations of Citi Bike trips, as well as their departure and destination stations. This query takes around one minute to return, which is far too slow to expect app viewers to wait for a project to run. Since we've set our cache in the developing logic to one week, this query will only hit the warehouse once as we work on this project over the course of the week.

Here's the SQL query:

```
SELECT STARTTIME AS START_TIME,  
       STOPTIME AS STOP_TIME,  
       START_STATION_NAME,  
       END_STATION_NAME,  
       USERTYPE AS user_type,  
       TRIPDURATION AS TRIP_DURATION  
FROM DEMO_DATA.DEMOS.CITIBIKE_TRIPS
```

We'll name the dataframe that is output by this query `trips`.

### Step 3: User input and data manipulation[​](#step-3-user-input-and-data-manipulation "Direct link to Step 3: User input and data manipulation")

Now that we've got the data we want in local memory, we can manipulate it however we'd like. Let's use some input parameters and take advantage of [Dataframe SQL](/docs/explore-data/cells/sql-cells/sql-cells-introduction). Hex's Dataframe SQL allows you write SQL against any dataframe in your project.

Let's create a [multiselect input parameter](/docs/explore-data/cells/input-cells/multiselect-inputs) to allow app users to filter by user type. This will allow app viewers to filter analysis to Citi Bike subscribers, regular customers, or to look at both.

Next, we'll use Dataframe SQL to apply this filter, and also look at the most popular stations to take Citi Bike trips from. Since we have all of this data stored locally, we can use Dataframe SQL for snappy results.

```
SELECT START_STATION_NAME,  
COUNT(*) as NUMBER_OF_TRIPS,  
AVG(TRIP_DURATION) as AVG_TRIP_DURATION  
FROM trips  
WHERE "USER_TYPE" IN ({{user_type | array}})  
GROUP BY 1  
ORDER BY 2 DESC
```

I've named this resulting dataframe `start_stations`.

Before we begin charting this data, we'll narrow it down to the 20 most popular departure stations using a Python cell:

```
top_start_stations = start_stations.head(20)
```

### Step 4: Visualizing data[​](#step-4-visualizing-data "Direct link to Step 4: Visualizing data")

Now that we've got the filtered data we want, let's chart!

As of now, the most popular Citi Bike departure station is at **1st Ave and E 68th Street**.

With a little more work, we can also display this in a map cell!

Let's first query the latitude and longitude data for the Citi Bike stations:

```
SELECT DISTINCT START_STATION_NAME,  
                START_STATION_LATITUDE,  
                START_STATION_LONGITUDE  
FROM DEMO_DATA.DEMOS.CITIBIKE_TRIPS
```

Now, let's use Dataframe SQL join this back to our aggregated data to create a dataframe ready for mapping.

```
SELECT *  
from start_stations  
JOIN start_geos USING(START_STATION_NAME)
```

This is another way to visualize the most used Citi Bike departure stations.

### Step 5: Configuring app settings and scheduled runs[​](#step-5-configuring-app-settings-and-scheduled-runs "Direct link to Step 5: Configuring app settings and scheduled runs")

For the purpose of this demo, we're assuming the table we're querying gets updated daily at midnight. To further optimize the new caching settings, we can schedule this app to run everyday at 6AM, *and* set the app to [show results from a previous run](/docs/share-insights/apps/app-run-settings#update-published-results) upon opening.

This way, any time an app user visits the published app, the data is the freshest we have available, and they don't have to wait for the long queries to run, or for the app to load.

tip

If an app viewer changes an input parameter, the entire app will be run. However, queries will still be pulled from the cache if they are within the timeout window. Check out our [app configuration docs](/docs/share-insights/apps/app-run-settings) for more information.

### What's next?[​](#whats-next "Direct link to What's next?")

This is a specific example of a feature that can be used in different ways for different situations. Think about the apps you've built: are there large queries that could be run less frequently to create a faster end-user or developer experience, or reduce database spend?

You can review the docs on [caching](/docs/explore-data/cells/sql-cells/query-caching) here.

#### On this page

* [SQL query caching](#sql-query-caching)
* [Step 1: Configure project-level query caching settings](#step-1-configure-project-level-query-caching-settings)
* [Step 2: Pull in data from an expensive query](#step-2-pull-in-data-from-an-expensive-query)
* [Step 3: User input and data manipulation](#step-3-user-input-and-data-manipulation)
* [Step 4: Visualizing data](#step-4-visualizing-data)
* [Step 5: Configuring app settings and scheduled runs](#step-5-configuring-app-settings-and-scheduled-runs)
* [What's next?](#whats-next)