On this page

# Connect to Google Sheets

tip

Check out the companion Hex project for this tutorial [here](https://app.hex.tech/hex-public/app/c2d24cea-6ab9-4e24-a8d7-d118d30af246/latest)!

If you have data stored in Google Sheets that you’d like to analyze with Hex, this guide is for you! In the following tutorial, we’ll walk though how to use GoogleAPI to establish a connection between Hex and Google Sheets, how to read from & write to a spreadsheet, as well as how to create & delete a spreadsheet.

## Set up Google API credentials[​](#set-up-google-api-credentials "Direct link to Set up Google API credentials")

First, we’ll need to set up a Service Account via Google API. The Service Account is what we’ll use to connect Hex to Google Sheets. Take the following steps in order to create the necessary credentials:

1. Navigate to [Google API service](https://console.developers.google.com/apis/library)
2. Create a project
3. Search for the Google Sheets API, and enable it
4. Go to the Credentials tab on the left navbar
5. Click **+ Credentials** and create a Service Account
6. Name the Service Account, and assign it the Owner role for your project. Click **Done** to save the account
7. From the **Service Accounts** page, click on the Service Account you just created
8. Go to the **Keys** tab. Then click **Add Key** > **Create new key**
9. Choose JSON, then click **Create**. The JSON file will download automatically

For more detailed instructions on how to set up your Service Account, you can check out [this guide](https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/).

## Create a Secret for your Google API credentials[​](#create-a-secret-for-your-google-api-credentials "Direct link to Create a Secret for your Google API credentials")

Once you have the JSON file with the Service Account credentials, add the information from the JSON file as a Secret in your project.

Navigate to the Variables tab, and use the **+ Add** button to [create a Secret](/docs/explore-data/projects/environment-configuration/environment-views#variables) where the Secret’s value is the contents of the Google API JSON file. In this example, the Secret is named `google_json`.

## Connect to Google Sheets[​](#connect-to-google-sheets "Direct link to Connect to Google Sheets")

Begin by importing `gspread` and the other packages required to establish a connection to your Google API account.

```
import pandas as pd  
import gspread  
from google.oauth2 import service_account  
import json
```

Use the credentials from the Secret you created (in this case, `google_json`) to create your connection.

```
service_account_info = json.loads(google_json)  
credentials = service_account.Credentials.from_service_account_info(service_account_info)
```

Define an API scope including Sheets and Drive and assign this scope to the credentials.

```
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']  
creds = credentials.with_scopes(scope)
```

Authorize a new client with your credentials and scope.

```
client = gspread.authorize(creds)
```

## Read data values from a spreadsheet[​](#read-data-values-from-a-spreadsheet "Direct link to Read data values from a spreadsheet")

In this example, we’re using a table of commentary data from a cricket match between India and Bangladesh. The exact dataset can be found [here](https://docs.google.com/spreadsheets/d/13J4c24SoKCanfTVS4NfrKvPH2aHYF0vxDGiu5YKETws/edit?usp=sharing).

Note: If you use this data, you will need to copy + paste the rows from the above spreadsheet into a separate spreadsheet that you own.

To make your spreadsheet accessible, navigate to Google Sheets and share it with your Service Account. Specifically, use the `client_email` value from the JSON file (this is the Service Account's associated email address) and assign the “Editor” permission.

Using the client created in the previous section, open the spreadsheet via the spreadsheet’s url.

```
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/13J4c24SoKCanfTVS4NfrKvPH2aHYF0vxDGiu5YKETws/edit?usp=sharing')
```

Get the worksheet you would like to use from the spreadsheet. This example picks the first worksheet using the index 0.

```
sheet_instance = sheet.get_worksheet(0)
```

You can get the value of a specific cell with code like this:

```
val = sheet_instance.cell(col=1,row=3).value
```

## Read data from a spreadsheet into a dataframe[​](#read-data-from-a-spreadsheet-into-a-dataframe "Direct link to Read data from a spreadsheet into a dataframe")

Get all the records as JSON.

```
records_data = sheet_instance.get_all_records()
```

Convert the JSON records to a dataframe.

```
records_df = pd.DataFrame.from_dict(records_data)
```

View the top records of the dataframe.

```
records_df.head()
```

## Create and write to a new worksheet[​](#create-and-write-to-a-new-worksheet "Direct link to Create and write to a new worksheet")

First, create a dataframe that you’d like to write to a new worksheet.

Let’s say we want to calculate the count of runs scored by each batsman. We do that here by creating a new dataframe, `runs_batsman`:

```
runs_batsman = records_df.groupby(['Batsman_Name'])['Runs'].count().reset_index()
```

Create a new empty worksheet, specifying the number of rows, number of columns, and title.

```
worksheet_title='runs_batsman'  
sheet.add_worksheet(rows=20,cols=2,title='runs_batsman')
```

Insert data from the dataframe into the new worksheet.

```
sheet.worksheet(worksheet_title).insert_rows(runs_batsman.values.tolist())
```

## Delete a worksheet[​](#delete-a-worksheet "Direct link to Delete a worksheet")

Specify the title of the worksheet you'd like to delete.

```
sheet.del_worksheet(sheet.worksheet('runs_batsman'))
```

Now we’ve covered the basics when it comes to how you can work with Google Sheets in Hex! If you're curious to learn what else is possible when it comes to integrating with Google Sheets, you can read more about Google Sheets's API, `gspread`, [here](https://docs.gspread.org/en/latest/).

As a reminder, if you’d like to see what this looks like in Hex, you can check out this tutorial’s [companion project](https://app.hex.tech/hex-public/app/c2d24cea-6ab9-4e24-a8d7-d118d30af246/latest).

#### On this page

* [Set up Google API credentials](#set-up-google-api-credentials)
* [Create a Secret for your Google API credentials](#create-a-secret-for-your-google-api-credentials)
* [Connect to Google Sheets](#connect-to-google-sheets)
* [Read data values from a spreadsheet](#read-data-values-from-a-spreadsheet)
* [Read data from a spreadsheet into a dataframe](#read-data-from-a-spreadsheet-into-a-dataframe)
* [Create and write to a new worksheet](#create-and-write-to-a-new-worksheet)
* [Delete a worksheet](#delete-a-worksheet)