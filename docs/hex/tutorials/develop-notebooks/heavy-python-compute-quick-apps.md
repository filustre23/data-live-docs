On this page

# Heavy Python compute, quick apps

How to configure your app for high performance when you have long-running Python processes.

tip

Check out the companion Hex project for this tutorial [here](https://app.hex.tech/hex-public/app/7a3beac0-c942-484e-9cea-04c1c15f5501/latest)!

## Overview[​](#overview "Direct link to Overview")

Say your project utilizes some heavy Python computation to process your data, and it takes a while to run. You don't want your end users waiting around for several minutes while your app loads! Instead, you'd like to have the published app run against cached results of the long-running Python process. If you've found yourself in a situation like this, you've come to the right place! 😄

The following tutorial will show you how to run different lines of code depending on the context a project is being executed in, through the use of the [built-in variable](/docs/explore-data/projects/environment-configuration/environment-views#built-in-variables) `hex_run_context`. The project's long-running Python code will only run in Notebook sessions, and then write the results of the heavy compute to an S3 bucket, as a way to cache the data. In App sessions, the app will pull the pre-computed results from S3, avoiding the long compute time and resulting in a quick, snappy app experience for end users.

tip

For more detailed instructions on how to connect Hex to an Amazon S3 bucket, check out our [dedicated tutorial](/tutorials/connect-to-data/connect-to-s3)!

## Import required packages[​](#import-required-packages "Direct link to Import required packages")

Begin by importing the required packages! In this project, `sys`, `os`, & `pandas` are used to write to and read from S3, `seaborn` is used to generate sample data, and `tqdm` & `time` are extra packages used to make this project a little more interesting.

```
import sys,os  
import pandas as pd  
import seaborn as sns  
from tqdm import tqdm  
import time
```

## Create Secrets for AWS credentials & set environment variables[​](#create-secrets-for-aws-credentials--set-environment-variables "Direct link to Create Secrets for AWS credentials & set environment variables")

To read & write to your S3 bucket, you'll need to enter `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as [Secrets](/docs/explore-data/projects/environment-configuration/environment-views#secrets) in your project. If these credentials have already been entered at the workspace level as [Shared Secrets](/docs/administration/workspace_settings/workspace-assets#shared-secrets), go ahead and import those into the project.

Next, define environment variables using the Secret values.

```
os.environ['AWS_ACCESS_KEY_ID']= aws_access_key_id  
os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
```

## `hex_run_context` magic[​](#hex_run_context-magic "Direct link to hex_run_context-magic")

This is where we get to the meat of the logic!

First a bit of background on `hex_run_context`’s possible values:

* If the project is being run in a Notebook session (i.e. when developing, which includes runs in the App builder), `hex_run_context` == 'logic'.
* If the project is being run as part of a [publish preview](/docs/share-insights/apps/publish-and-share-apps#preview-and-publish), `hex_run_context` == 'publish-preview'.
* If the published App is being run, `hex_run_context` == 'app'.
* If the project is being run as part of a [Scheduled run](/docs/share-insights/scheduled-runs), `hex_run_context` == 'scheduled'.
* If the project is being run from the [Hex API](/docs/api-integrations/api/overview), `hex_run_context` == 'api-triggered'.

You'll notice we're using an `if` statement in the Python cell below, which checks the value of `hex_run_context` to see if the cell is running in a Logic session. If it is, we simulate some long-running logic via the `sleep()` function. Next we load the 'planets' dataset from `seaborn` and write that data to our S3 bucket, caching the results of the heavy compute.

Here's what the code looks like:

```
# If this cell is running in Notebook mode, run the "expensive" logic (time.sleep())  
# and write the result (new_df) to S3  
if hex_run_context == "logic":  
    print(  
        """This cell is running in a Logic session, so the expensive Python  
code runs and the results are loaded into S3:\n"""  
    )  
    for i in tqdm(range(0, sleep_time), desc="Simulating heavy-compute logic"):  
        time.sleep(1)  
    new_df = sns.load_dataset("planets")  
    new_df.to_csv(f"s3://{s3_bucket_name}/planets/planet_data.csv")  
    print("\n\nData has been loaded and written to S3!")  
    df_planets = new_df.copy()  
  
# If this cell runs outside of Logic mode (i.e. if hex_run_context is equal to 'app'  
# or 'scheduled'), read in the results from S3 as a dataframe  
else:  
    print(  
        """This cell is running in an App or Schedule session, so we'll skip the  
sleep() function and quickly retrieve the results from S3. \n"""  
    )  
    df_planets = pd.read_csv(f"s3://{s3_bucket_name}/planets/planet_data.csv")  
    df_planets = df_planets.drop(columns=["Unnamed: 0"])  
    print("Data has been read from S3!")
```

Since our expensive code is tucked in the `if` logic, we will not run `sleep()` if the project is being run outside of Logic mode. Instead, if `hex_run_context` is equal to 'app' or 'scheduled', we'll simply read the data in from S3 and define it as a dataframe in our project, sidestepping the heavy compute!

Lastly, note that sleep\_time is a [sliding input parameter](/docs/explore-data/cells/input-cells/text-number-slider-and-date-inputs#slider) we included to make the project a bit interactive - changing this value will dictate many seconds the `sleep()` function will take.

*Pop quiz:* If you're viewing the published app, change the value of the slider. What do you expect to happen?

*Answer:* Nothing! `time.sleep()` is only called in logic sessions, so we'll continue to read the data in from S3.

To speed up runtimes, we based the remainder of the project’s analysis on the data that we wrote to S3, which is held in the dataframe `df_planets`. Since the subsequent filtering and aggregation runs against `df_planets`, the expensive Python logic is never triggered, which makes for quick runtimes. Interact with the “Method filter” in the project to see for yourself!

tip

Do you want to be able to cache the results of long-running SQL queries for a quicker app experience? [This tutorial](/tutorials/develop-notebooks/sql-query-caching) is best suited for that use case!

#### On this page

* [Overview](#overview)
* [Import required packages](#import-required-packages)
* [Create Secrets for AWS credentials & set environment variables](#create-secrets-for-aws-credentials--set-environment-variables)
* [`hex_run_context` magic](#hex_run_context-magic)