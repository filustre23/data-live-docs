On this page

# Cloud storage integrations

Import and export files between your Amazon S3 cloud storage and Hex projects.

info

* Available on Professional, Team, and Enterprise [plans](https://hex.tech/pricing/).
* Users will need the Admin workspace [role](/docs/collaborate/sharing-and-permissions/roles) to create and grant access to cloud storage integrations.
* Users will need access to the integration and **Can Edit** or higher [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to import and export files.

Hex cloud storage integrations allow you and your team to easily import CSV, JSON, and other files from your cloud storage into your Hex projects for use in your data notebooks and data apps.

## Create a cloud storage integration[​](#create-a-cloud-storage-integration "Direct link to Create a cloud storage integration")

To create a cloud storage integration, go to **Settings > Integrations > External file integrations** and click **+ Connection**. Select your cloud storage provider to open the integration form.

### Amazon S3[​](#amazon-s3 "Direct link to Amazon S3")

You will need to enter the bucket name, AWS region, and access keys for an IAM user. The IAM user must be allowed to perform the `ListBucket` and `GetObject` actions on the bucket, and on files and folders in the bucket.

The **Enable writeback** toggle will control whether or not the integration can [export files from Hex to S3](#export-files-to-your-cloud-storage-integration). If this is enabled, the IAM user will also need to have `PutObject` permissions in order to update files or create new files in the bucket.

Users with access to this integration will have the ability to read in files from the integration, and writeback abilities (if enabled).

### Google Cloud Storage (GCS)[​](#google-cloud-storage-gcs "Direct link to Google Cloud Storage (GCS)")

To set up your Service Account, you will need to enter the bucket name and a service account key JSON.

The service account will need to be granted the following permissions as a baseline for read access:

* storage.buckets.get
* storage.folders.get
* storage.folders.list
* storage.managedFolders.get
* storage.managedFolders.list
* storage.objects.get
* storage.objects.list

The **Enable writeback** toggle controls whether or not the integration can export files from Hex to GCS. If enabled, the service account needs to also be granted the following permissions:

* storage.folders.create
* storage.folders.delete
* storage.folders.rename
* storage.managedFolders.create
* storage.managedFolders.delete
* storage.multipartUploads.abort
* storage.multipartUploads.create
* storage.multipartUploads.list
* storage.multipartUploads.listParts
* storage.objects.create
* storage.objects.delete
* storage.objects.move
* storage.objects.restore
* storage.objects.update

If you give the service account the `Storage Object User` role, most of these permissions are covered. You will just need to add the `storage.buckets.get` permission on top.

### Google Drive[​](#google-drive "Direct link to Google Drive")

Go through the authorization flow to authorize Hex to connect to your Google Drive account. Once you authorize your account, other users in the workspace will be able to use these credentials to set up Google Drive connections.

After you authenticate, you will be brought back to the new integration modal in Hex where you can connect to a specific Google Drive directory. Because members of the workspace can use these credentials, it's not possible to connect to a user's "My Drive". Instead a Subdirectory ID is required to connect to a specific directory.

tip

Set up a separate Google Drive directory for Hex to connect to, rather than reusing an existing directory.

To find your Subdirectory ID, navigate to the directory in Google Drive, and copy the ID after `folders/` in the URL. Due to limitations of the Google Drive API, any nested subdirectories within this folder will need to be created as separate integrations.

The **Enable writeback** toggle will control whether or not the integration can [export files from Hex to the specified Google Drive folder](/docs/explore-data/projects/environment-configuration/files#export-files-to-external-file-integrations).

Users with access to this integration will have the ability to read in files from the specified Google Drive folder, and writeback abilities (if enabled).

## Import files from your cloud storage integration[​](#import-files-from-your-cloud-storage-integration "Direct link to Import files from your cloud storage integration")

In your project, open the Files sidebar. Under the **External file integrations** header, select Import on the appropriate integration and select the files you want to import.

Files imported from a cloud storage integration will count towards the project's 100 file limit. Each individual file is limited to 10 GB.

[](/assets/medias/import-files-from-cloud-storage-integration-df79c0c91dc862b3a1ac93c38721a251.mp4)

tip

Files imported to your project will be downloaded at time of import, and again each time your [project kernel](/docs/explore-data/projects/environment-configuration/project-kernels) starts. The larger the total file size in your project, the longer it will take to start your project each time it's opened. We recommend deleting any unused files to optimize project performance. [Learn more about working with files.](/docs/explore-data/projects/environment-configuration/files)

## Reference imported files in Python[​](#reference-imported-files-in-python "Direct link to Reference imported files in Python")

Files you import from your cloud storage integration are stored in a subdirectory of your project’s Hex directory with the naming pattern `external-files/\{integration_type\}/\{integration_name\}`. The integration name will be in lower-case with any non-alphanumeric characters removed, and spaces replaced by underscores. For example, the path for an S3 integration named "Hex's Testing Bucket" would be `external-files/s3/hexs_testing_bucket`. The path for a Google Drive integration named "Hex's Test Drive" would be `external-files/googledrive/hexs_test_drive`.

## Export files to your cloud storage integration[​](#export-files-to-your-cloud-storage-integration "Direct link to Export files to your cloud storage integration")

Hex watches the subdirectory associated with your cloud storage integration for new files and for updates to existing files. Changes are automatically exported to your cloud storage provider.

For example, if a CSV file were created from a dataframe using `dataframe.to_csv('external-files/s3/hexs_testing_bucket/my_new_data.csv')`, Hex would write the file `my_new_data.csv` to the appropriate Amazon S3 bucket. Similarly, `dataframe.to_csv('external-files/googledrive/hexs_test_drive/my_new_data.csv')` will write the file `my_new_data.csv` to the Google Drive folder designated in the integration configuration.

Note that files created in this way will not be automatically imported into the project and will no longer be present once the kernel restarts.

#### On this page

* [Create a cloud storage integration](#create-a-cloud-storage-integration)
  + [Amazon S3](#amazon-s3)
  + [Google Cloud Storage (GCS)](#google-cloud-storage-gcs)
  + [Google Drive](#google-drive)
* [Import files from your cloud storage integration](#import-files-from-your-cloud-storage-integration)
* [Reference imported files in Python](#reference-imported-files-in-python)
* [Export files to your cloud storage integration](#export-files-to-your-cloud-storage-integration)