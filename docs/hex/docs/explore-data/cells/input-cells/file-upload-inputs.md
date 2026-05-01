On this page

# File upload inputs

Add a file upload input to your project to allow app users to upload files such as CSVs, Excel files, PDFs, and more to your app.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to create and edit input cells.
* Users with **Can View App** permissions and higher can interact with input cells in published [Apps](/docs/share-insights/apps/apps-introduction).

## Best practices for file upload inputs[​](#best-practices-for-file-upload-inputs "Direct link to Best practices for file upload inputs")

The file uploaded to the file upload cell at the time of publish will be the default file used in the published app. Files that are uploaded in the published app will override the default file.

Uploading a file to the input cell in a published app will trigger a rerun of all cells that are dependent on the returned dataframe.

When developing the logic in your Notebook, keep in mind that the file uploaded in the app may not have the same content or structure as the default file that the project has been developed with. If you anticipate this occurring, consider using a python cell to evaluate the data types and column names of the uploaded file.

tip

File upload cells are intended to be used by viewers of a published app. If a project editor wants to upload a file to be processed by the project, consider using the [Files tab](/docs/connect-to-data/upload-files) in the Notebook.

## Selecting file upload type[​](#selecting-file-upload-type "Direct link to Selecting file upload type")

Click the gear icon above the file upload input to change the upload type. Select from **CSV**, **Excel**, or **file (binary)** for any file you intend to use downstream in a python cell such as PDFs, Parquet files, or images.

## CSV uploads[​](#csv-uploads "Direct link to CSV uploads")

Selecting CSV as the upload type allows app users to upload a CSV to an app, and returns the CSV as a dataframe that can be used in downstream cells.

[](/assets/medias/csv_upload_input-b2b03f8e3b0b8aa1fa7f5ed1fd2e61e7.mp4)

## Excel uploads[​](#excel-uploads "Direct link to Excel uploads")

Choosing Excel as the upload type returns a dictionary. Each tab on your spreadsheet will be recorded in the dictionary by its name, and the value of that entry will be a dataframe of that tab's contents.

[](/assets/medias/excel-file-upload-6b71a4e95af0c03d8953684a2c626b5b.mp4)

## Other file uploads (binary)[​](#other-file-uploads-binary "Direct link to Other file uploads (binary)")

Choose the file upload type to upload any file type, such as PDFs, images, or Parquet files that you can use downstream in a Python cell. Uploaded files are returned as a read-only bytestream that must be processed in Python.

[](/assets/medias/binary-file-upload-1b596ff0c21aad17fe5f6fc494cfad2c.mp4)

#### On this page

* [Best practices for file upload inputs](#best-practices-for-file-upload-inputs)
* [Selecting file upload type](#selecting-file-upload-type)
* [CSV uploads](#csv-uploads)
* [Excel uploads](#excel-uploads)
* [Other file uploads (binary)](#other-file-uploads-binary)