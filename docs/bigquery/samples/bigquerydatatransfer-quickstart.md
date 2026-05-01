* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 列出資料來源 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

列出 BigQuery 資料移轉服務支援的所有資料來源。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [BigQuery 資料移轉服務 API 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/libraries?hl=zh-tw)

## 程式碼範例

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Api.Gax.ResourceNames;
using Google.Cloud.BigQuery.DataTransfer.V1;
using System;

namespace GoogleCloudSamples
{
    public class QuickStart
    {
        public static void Main(string[] args)
        {
            // Instantiates a client
            DataTransferServiceClient client = DataTransferServiceClient.Create();

            // Your Google Cloud Platform project ID
            string projectId = "YOUR-PROJECT-ID";

            ProjectName project = ProjectName.FromProject(projectId);
            var sources = client.ListDataSources(project);
            Console.WriteLine("Supported Data Sources:");
            foreach (DataSource source in sources)
            {
                Console.WriteLine(
                    $"{source.DataSourceId}: " +
                    $"{source.DisplayName} ({source.Description})");
            }
        }
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Sample bigquery-quickstart creates a Google BigQuery dataset.
package main

import (
	"context"
	"fmt"
	"log"

	"google.golang.org/api/iterator"

	// Imports the BigQuery Data Transfer client package.
	datatransfer "cloud.google.com/go/bigquery/datatransfer/apiv1"
	"cloud.google.com/go/bigquery/datatransfer/apiv1/datatransferpb"
)

func main() {
	ctx := context.Background()

	// Sets your Google Cloud Platform project ID.
	projectID := "YOUR_PROJECT_ID"

	// Creates a client.
	client, err := datatransfer.NewClient(ctx)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}
	defer client.Close()

	req := &datatransferpb.ListDataSourcesRequest{
		Parent: fmt.Sprintf("projects/%s", projectID),
	}
	it := client.ListDataSources(ctx, req)
	fmt.Println("Supported Data Sources:")
	for {
		ds, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			log.Fatalf("Failed to list sources: %v", err)
		}
		fmt.Println(ds.DisplayName)
		fmt.Println("\tID: ", ds.DataSourceId)
		fmt.Println("\tFull path: ", ds.Name)
		fmt.Println("\tDescription: ", ds.Description)
	}
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Imports the Google Cloud client library

import com.google.cloud.bigquery.datatransfer.v1.DataSource;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient.ListDataSourcesPagedResponse;
import com.google.cloud.bigquery.datatransfer.v1.ListDataSourcesRequest;

public class QuickstartSample {
  /** List available data sources for the BigQuery Data Transfer service. */
  public static void main(String... args) throws Exception {
    // Sets your Google Cloud Platform project ID.
    // String projectId = "YOUR_PROJECT_ID";
    String projectId = args[0];

    // Instantiate a client. If you don't specify credentials when constructing a client, the
    // client library will look for credentials in the environment, such as the
    // GOOGLE_APPLICATION_CREDENTIALS environment variable.
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
      // Request the list of available data sources.
      String parent = String.format("projects/%s", projectId);
      ListDataSourcesRequest request =
          ListDataSourcesRequest.newBuilder().setParent(parent).build();
      ListDataSourcesPagedResponse response = client.listDataSources(request);

      // Print the results.
      System.out.println("Supported Data Sources:");
      for (DataSource dataSource : response.iterateAll()) {
        System.out.println(dataSource.getDisplayName());
        System.out.printf("\tID: %s%n", dataSource.getDataSourceId());
        System.out.printf("\tFull path: %s%n", dataSource.getName());
        System.out.printf("\tDescription: %s%n", dataSource.getDescription());
      }
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {
  DataTransferServiceClient,
} = require('@google-cloud/bigquery-data-transfer');
const {status} = require('@grpc/grpc-js');

const client = new DataTransferServiceClient();

/**
 * Lists all available data sources for a project.
 * Data sources are the services that can be used to create data transfers into BigQuery.
 *
 * @param {string} projectId The Google Cloud project ID, for example 'example-project-id'.
 */
async function listDataSources(projectId) {
  const request = {
    parent: `projects/${projectId}`,
  };

  try {
    const [dataSources] = await client.listDataSources(request);

    if (dataSources.length === 0) {
      console.log(`No data sources found in project ${projectId}.`);
      return;
    }

    console.log('Supported data sources:');
    for (const dataSource of dataSources) {
      console.log(`\nData source: ${dataSource.name}`);
      console.log(`  ID: ${dataSource.dataSourceId}`);
      console.log(`  Display Name: ${dataSource.displayName}`);
    }
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(`Project ${projectId} not found.`);
    } else {
      console.error('An error occurred:', err);
    }
  }
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# Includes the autoloader for libraries installed with composer
require __DIR__ . '/vendor/autoload.php';

# Imports the Google Cloud client library
use Google\Cloud\BigQuery\DataTransfer\V1\Client\DataTransferServiceClient;
use Google\Cloud\BigQuery\DataTransfer\V1\ListDataSourcesRequest;

# Instantiates a client
$bqdtsClient = new DataTransferServiceClient();

# Your Google Cloud Platform project ID
$projectId = 'YOUR_PROJECT_ID';
$parent = sprintf('projects/%s/locations/us', $projectId);

try {
    echo 'Supported Data Sources:', PHP_EOL;
    $listDataSourcesRequest = (new ListDataSourcesRequest())
        ->setParent($parent);
    $pagedResponse = $bqdtsClient->listDataSources($listDataSourcesRequest);
    foreach ($pagedResponse->iterateAllElements() as $dataSource) {
        echo 'Data source: ', $dataSource->getDisplayName(), PHP_EOL;
        echo 'ID: ', $dataSource->getDataSourceId(), PHP_EOL;
        echo 'Full path: ', $dataSource->getName(), PHP_EOL;
        echo 'Description: ', $dataSource->getDescription(), PHP_EOL;
    }
} finally {
    $bqdtsClient->close();
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery_datatransfer

client = bigquery_datatransfer.DataTransferServiceClient()

# TODO: Update to your project ID.
project_id = "my-project"

# Get the full path to your project.
parent = client.common_project_path(project_id)

print("Supported Data Sources:")

# Iterate over all possible data sources.
for data_source in client.list_data_sources(parent=parent):
    print("{}:".format(data_source.display_name))
    print("\tID: {}".format(data_source.data_source_id))
    print("\tFull path: {}".format(data_source.name))
    print("\tDescription: {}".format(data_source.description))
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# Imports the Google Cloud client library
require "google/cloud/bigquery/data_transfer"

# Your Google Cloud Platform project ID
# project_id = "YOUR_PROJECT_ID"

# Instantiate a client
data_transfer = Google::Cloud::Bigquery::DataTransfer.data_transfer_service

# Get the full path to your project.
project_path = data_transfer.project_path project: project_id

puts "Supported Data Sources:"

# Iterate over all possible data sources.
data_transfer.list_data_sources(parent: project_path).each do |data_source|
  puts "Data source: #{data_source.display_name}"
  puts "ID: #{data_source.data_source_id}"
  puts "Full path: #{data_source.name}"
  puts "Description: #{data_source.description}"
end
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]