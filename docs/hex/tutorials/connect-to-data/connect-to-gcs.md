On this page

# Connect to GCS

tip

Check out the companion Hex project for this tutorial [here](https://app.hex.tech/hex-public/app/2bcf54ce-f039-45bc-91ab-d5858a0c116e/latest)!

While working in Hex, you may want to pull data from or save data to your Google Cloud Storage (GCS) buckets. This tutorial shows you how to do both!

## Set up Google Service Account key[​](#set-up-google-service-account-key "Direct link to Set up Google Service Account key")

As a first step, you'll need to create a Service Account key in Google Cloud that has access to the GCS bucket you want to access in your project. Take the following steps in order to create the key:

1. Navigate to Google IAM & Admin [Service Accounts](https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts).
2. Select a project or create a new one.
3. Select a Service Account or select **+ Create Service Account** .
4. Click the **Keys** tab.
5. Click the **Add key** drop-down menu, then select **Create new key**.
6. Select **JSON** as the **Key type** and click **Create**. The JSON file will download automatically.

For more detailed instructions on how to set up your Service Account, you can check out [this guide](https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/).

## Create a Secret for your Service Account key[​](#create-a-secret-for-your-service-account-key "Direct link to Create a Secret for your Service Account key")

Once you have the JSON file with the Service Account credentials, add the JSON file as a Secret in your project.

Navigate to the Variables tab, and use the **+ Add** button to [create a Secret](/docs/explore-data/projects/environment-configuration/environment-views#variables) where the Secret’s value is the entire service account key JSON. In this example, the Secret is named `sa_json`.

## Connect to GCS[​](#connect-to-gcs "Direct link to Connect to GCS")

Start by importing the packages required to establish a connection to your GCS bucket.

```
from google.cloud import storage  
import pandas as pd  
import json
```

Use the credentials from the Secret you created (in this case, `sa_json`) to create your connection. Use `json.loads` to process the JSON and store it in the variable, `service_account_info`. Next, Use the name of your GCS bucket in place of our bucket, `hex-demo-test`. If a bucket by this name doesn't exist, it will be created.

```
bucket_name = 'hex-demo-test'  
  
service_account_info = json.loads(sa_json)  
client2 = storage.Client.from_service_account_info(service_account_info)  
bucket = client2.get_bucket(bucket_name)
```

## Upload blob to GCS[​](#upload-blob-to-gcs "Direct link to Upload blob to GCS")

In this example, we’ll upload a dataset of restaurant orders we have in our database. The dataframe we have is called `orders_2021`.

Convert the dataframe to CSV to be uploaded to GCS.

```
orders_2021.to_csv('orders_to_upload.csv')
```

Create a variable, `source_file_name`, to hold the name of the csv we just created, `orders_to_upload.csv`. Next, create a variable, `destination_blob_name`, to hold the name of the blob you are creating in the GCS bucket defined above (`hex-demo-test`).

```
source_file_name = 'orders_to_upload.csv'  
destination_blob_name = 'uploaded_orders.csv'
```

Upload the `orders_to_upload.csv` file to a blob named `uploaded_orders.csv` in the `hex-demo-test` bucket.

```
blob = bucket.blob(destination_blob_name)  
blob.upload_from_filename(source_file_name)
```

## Download blob from GCS[​](#download-blob-from-gcs "Direct link to Download blob from GCS")

Now let's download the data that was just uploaded. Start by defining a variable, `source_blob_name`, to hold the the name of the blob we'll be accessing, `uploaded_orders.csv`. Then, define a variable for the name of the downloaded file, `orders_downloaded.csv`.

```
source_blob_name = 'uploaded_orders.csv'  
destination_file_name = 'orders_downloaded.csv'
```

Pull the data we uploaded in `uploaded_orders.csv` back into our project.

```
blob = bucket.blob(source_blob_name)  
blob.download_to_filename(destination_file_name)
```

And lastly, let's look at the downloaded data!

```
df = pd.read_csv('orders_downloaded.csv')  
df.head()
```

#### On this page

* [Set up Google Service Account key](#set-up-google-service-account-key)
* [Create a Secret for your Service Account key](#create-a-secret-for-your-service-account-key)
* [Connect to GCS](#connect-to-gcs)
* [Upload blob to GCS](#upload-blob-to-gcs)
* [Download blob from GCS](#download-blob-from-gcs)