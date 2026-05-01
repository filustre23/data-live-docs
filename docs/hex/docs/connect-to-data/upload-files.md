On this page

# Upload files

Upload CSV, JSON, and other files to your Hex project.

info

* Users need **Can Edit** or higher [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to upload files to the Notebook.

## Upload files to your project[​](#upload-files-to-your-project "Direct link to Upload files to your project")

Upload CSV, JSON, and other file types to your Hex project from the Files sidebar. You can drag and drop files into the Drop files here area, or click browse files, select your files, and click Upload.

tip

If you want to allow viewers to upload files to a published app, consider using a [file upload input parameter](/docs/explore-data/cells/input-cells/file-upload-inputs).

## Reference files in your project[​](#reference-files-in-your-project "Direct link to Reference files in your project")

You can reference uploaded files in Python cells.

You can also query a CSV file from a SQL cell using dataframe SQL.

To quickly query a CSV, locate the three-dot menu next to the file name in your Files sidebar, then click "Query in new SQL cell".

## Manage uploaded files[​](#manage-uploaded-files "Direct link to Manage uploaded files")

Each project is limited to 100 files, and each file must be less than 2 GB in size. All uploaded files count towards your project upload limit, even if they aren’t referenced in your project.

tip

Delete any files that are no longer referenced in your project. This will free up project storage and optimize performance.

Every project has its own directory, `/hex`, where uploaded files are stored. Uploaded files are processed each time the project kernel starts, which can lead to longer kernel load times. We recommend deleting project files that are no longer in use.

caution

Any local files created in a subdirectory will not be persisted after the project's kernel restarts.

### Delete files[​](#delete-files "Direct link to Delete files")

You can delete an uploaded file from the Files sidebar in your project. Click the **Delete** icon by the file name. You will be prompted to confirm before the file is deleted.

### Programmatically delete all project files[​](#programmatically-delete-all-project-files "Direct link to Programmatically delete all project files")

To programmatically delete all local files in your project's directory, you can loop through the contents of your directory by running the below code snippet in a Python cell in your project.

caution

Deleted files are not recoverable. Be certain you want to delete all files from your project before using this code.

```
import os  
for file in os.listdir():  
    if os.path.isfile(file):  
        os.remove(file)
```

### Files in different run contexts[​](#files-in-different-run-contexts "Direct link to Files in different run contexts")

Local files written in Notebook sessions are persisted between runs of the project. Published apps and scheduled runs execute with different [run contexts](/docs/explore-data/projects/environment-configuration/environment-views#built-in-variables), and local files written during runs in these contexts will not be persisted.

If you want to save a file during a scheduled run or published app session, the data must be written to an external source, such as your [database](/tutorials/connect-to-data/use-writeback-cells), or as [external files](/docs/explore-data/projects/environment-configuration/files#external-files).

#### On this page

* [Upload files to your project](#upload-files-to-your-project)
* [Reference files in your project](#reference-files-in-your-project)
* [Manage uploaded files](#manage-uploaded-files)
  + [Delete files](#delete-files)
  + [Programmatically delete all project files](#programmatically-delete-all-project-files)
  + [Files in different run contexts](#files-in-different-run-contexts)