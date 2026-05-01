On this page

# Files

Upload local files to your Hex project, or import them directly from an external file integration.

## Add files to your project[​](#add-files-to-your-project "Direct link to Add files to your project")

You can add up to 100 files to your Hex project from the **Files** sidebar. The file size limit is 2 GB for uploads and 10 GB for S3 or Google Drive imports.

tip

Every file you add to your project will be downloaded at time of import, and again each time your [project kernel](/docs/explore-data/projects/environment-configuration/project-kernels) starts. The larger the total file size in your project, the longer it will take to start your project each time it's opened. We recommend deleting any unused files to optimize project performance.

### Local files[​](#local-files "Direct link to Local files")

Upload files to your Hex project by dragging and dropping into the **Files** tab, or by clicking **browse files** and following the prompts. The file size limit for uploads is 2 GB.

[](/assets/medias/upload-local-files-0e33c204c5e00310fd62a82c25fc1539.mp4)

### External files[​](#external-files "Direct link to External files")

Admins can set up [external file integrations](/docs/administration/workspace_settings/workspace-assets#external-file-integrations) which allow users to import files from S3 or Google Drive into Hex projects.

Import a file from an external source from the **External file integrations** section of the **Files** tab. Click **Import** next to the appropriate integration and follow the prompts. The files size limit for external file integration imports is 10 GB.

[](/assets/medias/adding-external-file-integration-df79c0c91dc862b3a1ac93c38721a251.mp4)

## File directory[​](#file-directory "Direct link to File directory")

Every project has its own directory, `/hex`, where local imported files are stored. If files from an external source are present, they are stored in subdirectories of the `/hex/external-files` directory.

caution

Any local files created in a sub directory will *not* be persisted after the project's kernel has been restarted.

### Referencing imported files[​](#referencing-imported-files "Direct link to Referencing imported files")

Local files are located in the current working directory and can be referenced by name. External files will be located in a subdirectory with the naming pattern `external-files/${integration_type}/${integration_name}`. The integration name is lower-cased and sanitized to remove any non-alphanumeric characters, with spaces replaced by underscores. For example, the path for an S3 integration named "Hex's Testing Bucket" would be `external-files/s3/hexs_testing_bucket`. The path for a Google Drive integration named "Hex's Test Drive" would be `external-files/googledrive/hexs_test_drive`.

You can always copy the filename, including its path, from the three-dot menu next to the file. For CSV files, you can copy the DataFrame creation code, or create a SQL Cell with the CSV as its source.

[](/assets/medias/referencing-imported-files-7024804cd4d056a6f587b96e45bc22ac.mp4)

### Download files[​](#download-files "Direct link to Download files")

You can download any imported files from the file browser.

[](/assets/medias/download-files-2d3891fe368f2fee1dc42a16a3c40e2a.mp4)

## Export files to external file integrations[​](#export-files-to-external-file-integrations "Direct link to Export files to external file integrations")

Hex watches the external file directories for new files and updates to existing files, which will automatically export or push updates to the external source. For example, if a .csv file is created from a dataframe using `dataframe.to_csv('external-files/s3/hexs_testing_bucket/my_new_data.csv')`, Hex will write the file `my_new_data.csv` to the bucket in S3. Similarly, `dataframe.to_csv('external-files/googledrive/hexs_test_drive/my_new_data.csv')` will write the file `my_new_data.csv` to the Google Drive folder designated in the integration configuration.

Note that files created in this way will not automatically be imported into the project and will no longer be present once the kernel restarts.

caution

The credentials for your external file integration will need to have permissions to write data in order for Hex to successfully create or update the file.

## Files in different run contexts[​](#files-in-different-run-contexts "Direct link to Files in different run contexts")

Local files written in Notebook sessions are persisted between runs of the project. Published apps and scheduled runs execute with different [run contexts](/docs/explore-data/projects/environment-configuration/environment-views#built-in-variables), and local files written during runs in these contexts will not be persisted. If you want to save a file during a scheduled run or published app session, the data must be written to an external source, such as your [database](/tutorials/connect-to-data/use-writeback-cells), or as [external files](#external-files).

## Frequently asked questions[​](#frequently-asked-questions "Direct link to Frequently asked questions")

#### Render images[​](#render-images "Direct link to Render images")

You can use a Markdown or Text cell to [display images](/docs/explore-data/cells/text-cells#image-support) in your project.

You can also render imported image files through the use of `IPython.display`, using code like the following in a Python cell:

```
from IPython.display import Image  
Image(filename='file.png')
```

#### Duplicate a project with imported files[​](#duplicate-a-project-with-imported-files "Direct link to Duplicate a project with imported files")

When you duplicate a project, local files in the main `/hex` directory and all external files (as visible in the **Files** tab) will be included in the new duplicate. If you have created any local files in subdirectories, their contents will not be duplicated with the new project.

#### View all files in project[​](#view-all-files-in-project "Direct link to View all files in project")

To see what files exist in your current project, check out the [Files tab](/docs/explore-data/projects/environment-configuration/environment-views#files) of the left sidebar or use this code in a Python cell:

```
from os import walk  
from pathlib import PurePath  
for path, subdirs, files in walk('.'):  
    for name in files:  
        print(PurePath(path, name))
```

#### Delete all local files in project[​](#delete-all-local-files-in-project "Direct link to Delete all local files in project")

To programmatically delete all local files in your project's directory, you can loop through the contents of your directory:

```
import os  
for file in os.listdir():  
    if os.path.isfile(file):  
        os.remove(file)
```

warning

Deleted files are not recoverable. Be certain you want to delete all files in your project before using this code.

#### On this page

* [Add files to your project](#add-files-to-your-project)
  + [Local files](#local-files)
  + [External files](#external-files)
* [File directory](#file-directory)
  + [Referencing imported files](#referencing-imported-files)
  + [Download files](#download-files)
* [Export files to external file integrations](#export-files-to-external-file-integrations)
* [Files in different run contexts](#files-in-different-run-contexts)
* [Frequently asked questions](#frequently-asked-questions)