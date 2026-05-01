On this page

# Get your data

Learn simple methods to get your data into Hex by uploading files and setting up data connections

tip

Follow along with this tutorial in its companion [Hex Project!](https://app.hex.tech/hex/app/c5386acd-bcc2-4d24-9f8b-5d1bc27ed4ca/latest)

There are two primary ways to get your data into a Hex project:

1. through an individual project's file uploader option or
2. setting up a data connection to your database(s).

In this tutorial, we'll walk through both options so you can decide which option suits your workflow best.

## File uploader[​](#file-uploader "Direct link to File uploader")

To upload files, navigate to the **Files** tab in the project sidebar. Then drag your files into the **Drop files here** area or select your files from the **browse files** option. You can upload up to 100 files, each up to 2GB, into a project.

Press the **Upload file** button to confirm that you would like to upload your files. You are able to upload multiple files in parallel and the count on this button will inform you of the number of files you'll be uploading.

You are able to see the upload status along with some baseline metadata about the file(s) including the file name, size, and last updated timestamp.

For example files to practice with, you can download and use any of [these csv files](https://people.sc.fsu.edu/~jburkardt/data/csv/csv.html) from Florida State University's computer science department. Clicking on any of these file names will download the csv file to your local directory.

Once your file is uploaded, you'll be able to read in and reference your data in multiple ways. Select the ellipses next to the uploaded file to reveal options to manage the file.

To create a DataFrame from your file, you can either select **Copy DataFrame creation code** and paste that code into a new python cell or choose **Query in new SQL Cell** which will automatically create a new SQL cell with a pre-populated SQL statement. Run the resulting cells for either option to obtain a DataFrame using your file.

## Set up a data connection to your database[​](#set-up-a-data-connection-to-your-database "Direct link to Set up a data connection to your database")

We currently support a number of connections types, including Snowflake, BigQuery & Redshift, among others. See the full list [here](/docs/connect-to-data/data-connections/data-connections-introduction).

You'll need to add our IP addresses to your allow-list in order to allow Hex to connect to your databases. Find more details on how to do this in the [docs](/docs/connect-to-data/data-connections/allow-connections-from-hex-ip-addresses).

tip

Do you use a data source we don't support right now? Let us know at `[email protected]` if there's one you want us to prioritize adding.

To add a data connection, go to a project's **Data sources** tab in the sidebar, click the **+ Add** button in the Data Connections section, and fill in your details. More detailed instruction [here](/docs/connect-to-data/data-connections/data-connections-introduction#add-a-new-connection).

As with the manually uploaded files, you can [use a SQL Cell](/docs/explore-data/cells/sql-cells/sql-cells-introduction#querying-data-with-sql-cells) to query your data from the data connection directly.

If you are a Workspace Admin, we recommend setting up any common data connections in the Settings panel as a Workspace asset. This way, those connections will be accessible to all Workspace users as a project's Data sources option. This is much more efficient, and secure, method than having to manually add that data connection to each project individually!

#### On this page

* [File uploader](#file-uploader)
* [Set up a data connection to your database](#set-up-a-data-connection-to-your-database)