Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 列出資料集

本文說明如何在 BigQuery 中列出資料集並取得相關資訊。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文件各項工作所需的權限。

### 必要角色

如要取得列出資料集或取得資料集資訊所需的權限，請要求系統管理員授予您專案的「[BigQuery 中繼資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.metadataViewer) 」(`roles/bigquery.metadataViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.datasets.get` 權限，可列出資料集或取得資料集資訊。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

在專案或機構層級套用 `roles/bigquery.metadataViewer` 角色時，您可以列出專案中的所有資料集。在資料集層級套用 `roles/bigquery.metadataViewer` 角色時，您可以列出您已獲授該角色的所有資料集。

## 列出資料集

選取下列選項之一：

### 控制台

1. 在導覽選單中，按一下「Studio」。
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)，即可查看該專案中的資料集，接著按一下資料集名稱。你也可以使用搜尋欄位或篩選器尋找資料集。

### SQL

查詢 [`INFORMATION_SCHEMA.SCHEMATA` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     schema_name
   FROM
     PROJECT_ID.`region-REGION`.INFORMATION_SCHEMA.SCHEMATA;
   ```

   更改下列內容：

   * `PROJECT_ID`：專案的 ID。Google Cloud 如未指定，系統會使用預設專案。
   * `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`us`。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

發出 `bq ls` 指令，依資料集 ID 列出資料集。`--format` 標記可用來控管輸出。如要列出預設專案以外的專案資料集，請將 `--project_id` 旗標新增至該指令。

如要列出專案中的所有資料集，包括[隱藏資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#hidden_datasets)，請使用 `--all` 標記或 `-a` 捷徑。

如要列出專案中除了隱藏資料集以外的所有資料集，請使用 `--datasets` 標記或 `-d` 捷徑。這個標記是選用的，隱藏資料集預設為不列出。

其他標記包括：

* `--filter`：列出符合篩選器運算式的資料集。以空格分隔的方式列出標籤鍵和值，格式為 `labels.key:value`。如要進一步瞭解如何使用標籤篩選資料集，請參閱「[新增及使用標籤](https://docs.cloud.google.com/bigquery/docs/filtering-labels?hl=zh-tw#filtering_datasets_using_labels)」。使用 `status:live` 關鍵字，根據狀態篩選資料集。`status` 的有效值為 `live`(預設值)、`deleted` 和 `any`。
* `--max_results` 或 `-n`：用來表示結果數量上限的整數。預設值為 `50`。

```
bq ls --filter labels.key:value \
--max_results integer \
--format=prettyjson \
--project_id project_id
```

更改下列內容：

* key:value：標籤鍵和值
* integer：代表要列出資料集數量的整數
* project\_id：換成您的專案名稱

範例：

輸入下列指令，列出預設專案中的資料集。`--
format` 已設為「pretty」，藉此傳回基本格式的資料表。

```
bq ls --format=pretty
```

輸入下列指令，列出 `myotherproject` 中的資料集。`--format` 已設為 `prettyjson`，藉此傳回 JSON 格式的詳細結果。

```
bq ls --format=prettyjson --project_id myotherproject
```

輸入下列指令，列出預設專案中的所有資料集 (包括隱藏資料集)。在輸出內容中，隱藏資料集的名稱會以底線開頭。

```
bq ls -a
```

輸入下列指令，從預設專案傳回超過 50 個 (預設值) 輸出資料集。

```
bq ls --max_results 60
```

輸入下列指令，列出預設專案中附有 `org:dev` 標籤的資料集。

```
bq ls --filter labels.org:dev
```

### API

如要使用 API 列出資料集，請呼叫 [`datasets.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list?hl=zh-tw) API 方法。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;
using System;
using System.Collections.Generic;
using System.Linq;

public class BigQueryListDatasets
{
    public void ListDatasets(
        string projectId = "your-project-id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        // Retrieve list of datasets in project
        List<BigQueryDataset> datasets = client.ListDatasets().ToList();
        // Display the results
        if (datasets.Count > 0)
        {
            Console.WriteLine($"Datasets in project {projectId}:");
            foreach (var dataset in datasets)
            {
                Console.WriteLine($"\t{dataset.Reference.DatasetId}");
            }
        }
        else
        {
            Console.WriteLine($"{projectId} does not contain any datasets.");
        }
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// listDatasets demonstrates iterating through the collection of datasets in a project.
func listDatasets(projectID string, w io.Writer) error {
	// projectID := "my-project-id"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	it := client.Datasets(ctx)
	for {
		dataset, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintln(w, dataset.DatasetID)
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.paging.Page;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQuery.DatasetListOption;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;

public class ListDatasets {

  public static void runListDatasets() {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    listDatasets(projectId);
  }

  public static void listDatasets(String projectId) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Page<Dataset> datasets = bigquery.listDatasets(projectId, DatasetListOption.pageSize(100));
      if (datasets == null) {
        System.out.println("Dataset does not contain any models");
        return;
      }
      datasets
          .iterateAll()
          .forEach(
              dataset -> System.out.printf("Success! Dataset ID: %s ", dataset.getDatasetId()));
    } catch (BigQueryException e) {
      System.out.println("Project does not contain any datasets \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function listDatasets() {
  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const projectId = "my_project_id";

  // Lists all datasets in the specified project.
  // If projectId is not specified, this method will take
  // the projectId from the authenticated BigQuery Client.
  const [datasets] = await bigquery.getDatasets({projectId});
  console.log('Datasets:');
  datasets.forEach(dataset => console.log(dataset.id));
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/** Uncomment and populate these variables in your code */
// $projectId  = 'The Google project ID';

$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$datasets = $bigQuery->datasets();
foreach ($datasets as $dataset) {
    print($dataset->id() . PHP_EOL);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

datasets = list(client.list_datasets())  # Make an API request.
project = client.project

if datasets:
    print("Datasets in project {}:".format(project))
    for dataset in datasets:
        print("\t{}".format(dataset.dataset_id))
else:
    print("{} project does not contain any datasets.".format(project))
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def list_datasets project_id = "your-project-id"
  bigquery = Google::Cloud::Bigquery.new project: project_id

  puts "Datasets in project #{project_id}:"
  bigquery.datasets.each do |dataset|
    puts "\t#{dataset.dataset_id}"
  end
end
```

## 取得資料集相關資訊

選取下列選項之一：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)，即可查看該專案中的資料集，接著按一下資料集名稱。你也可以使用搜尋欄位或篩選器尋找資料集。

   說明和詳細資料會顯示在「詳細資料」分頁中。
3. 選用：您可以前往其他分頁，查看資料集中的資料表、常式和模型清單。

根據預設，[隱藏資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#hidden_datasets)不會顯示在 Google Cloud 控制台中。如要顯示隱藏資料集的相關資訊，請使用 bq 指令列工具或 API。

### SQL

查詢 [`INFORMATION_SCHEMA.SCHEMATA` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     * EXCEPT (schema_owner)
   FROM
     PROJECT_ID.`region-REGION`.INFORMATION_SCHEMA.SCHEMATA;
   ```

   請替換下列項目：

   * `PROJECT_ID`：專案的 ID。 Google Cloud 如未指定，系統會使用預設專案。
   * `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`us`。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

您也可以查詢 [`INFORMATION_SCHEMA.SCHEMATA_OPTIONS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata-options?hl=zh-tw)。

```
SELECT
  *
FROM
  PROJECT_ID.`region-REGION`.INFORMATION_SCHEMA.SCHEMATA_OPTIONS;
```

### bq

請發出 `bq show` 指令。`--format` 旗標可用來控制輸出內容。如要取得預設專案以外的資料集相關資訊，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。
輸出內容會顯示資料集的資訊，例如存取權控管、標籤和位置。這項指令不會顯示資料集的繼承權限，但您可以在 Google Cloud 控制台中查看。

如要顯示[隱藏資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#hidden_datasets)的相關資訊，請使用 [`bq ls --all`](https://docs.cloud.google.com/bigquery/docs/listing-datasets?hl=zh-tw) 指令列出所有資料集，然後在 `bq show` 指令中使用隱藏資料集的名稱。

```
bq show --format=prettyjson project_id:dataset
```

更改下列內容：

* project\_id 是您的專案名稱。
* dataset 是資料集名稱。

範例：

輸入下列指令，顯示預設專案中的 `mydataset` 相關資訊。

```
bq show --format=prettyjson mydataset
```

輸入下列指令，顯示 `myotherproject` 中的 `mydataset` 相關資訊。

```
bq show --format=prettyjson myotherproject:mydataset
```

輸入下列指令，顯示預設專案中隱藏資料集 `_1234abcd56efgh78ijkl1234` 的相關資訊。

```
bq show --format=prettyjson _1234abcd56efgh78ijkl1234
```

### API

呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) API 方法，並提供所有相關參數。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// printDatasetInfo demonstrates fetching dataset metadata and printing some of it to an io.Writer.
func printDatasetInfo(w io.Writer, projectID, datasetID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	meta, err := client.Dataset(datasetID).Metadata(ctx)
	if err != nil {
		return err
	}

	fmt.Fprintf(w, "Dataset ID: %s\n", datasetID)
	fmt.Fprintf(w, "Description: %s\n", meta.Description)
	fmt.Fprintln(w, "Labels:")
	for k, v := range meta.Labels {
		fmt.Fprintf(w, "\t%s: %s", k, v)
	}
	fmt.Fprintln(w, "Tables:")
	it := client.Dataset(datasetID).Tables(ctx)

	cnt := 0
	for {
		t, err := it.Next()
		if err == iterator.Done {
			break
		}
		cnt++
		fmt.Fprintf(w, "\t%s\n", t.TableID)
	}
	if cnt == 0 {
		fmt.Fprintln(w, "\tThis dataset does not contain any tables.")
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.paging.Page;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQuery.TableListOption;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import com.google.cloud.bigquery.DatasetId;
import com.google.cloud.bigquery.Table;

public class GetDatasetInfo {

  public static void runGetDatasetInfo() {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    getDatasetInfo(projectId, datasetName);
  }

  public static void getDatasetInfo(String projectId, String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();
      DatasetId datasetId = DatasetId.of(projectId, datasetName);
      Dataset dataset = bigquery.getDataset(datasetId);

      // View dataset properties
      String description = dataset.getDescription();
      System.out.println(description);

      // View tables in the dataset
      // For more information on listing tables see:
      // https://javadoc.io/static/com.google.cloud/google-cloud-bigquery/0.22.0-beta/com/google/cloud/bigquery/BigQuery.html
      Page<Table> tables = bigquery.listTables(datasetName, TableListOption.pageSize(100));

      tables.iterateAll().forEach(table -> System.out.print(table.getTableId().getTable() + "\n"));

      System.out.println("Dataset info retrieved successfully.");
    } catch (BigQueryException e) {
      System.out.println("Dataset info not retrieved. \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function getDataset() {
  // Retrieves dataset named "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample
   */
  // const datasetId = "my_dataset";

  // Retrieve dataset reference
  const [dataset] = await bigquery.dataset(datasetId).get();

  console.log('Dataset:');
  console.log(dataset.metadata.datasetReference);
}
getDataset();
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset to fetch.
# dataset_id = 'your-project.your_dataset'

dataset = client.get_dataset(dataset_id)  # Make an API request.

full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
friendly_name = dataset.friendly_name
print(
    "Got dataset '{}' with friendly_name '{}'.".format(
        full_dataset_id, friendly_name
    )
)

# View dataset properties.
print("Description: {}".format(dataset.description))
print("Labels:")
labels = dataset.labels
if labels:
    for label, value in labels.items():
        print("\t{}: {}".format(label, value))
else:
    print("\tDataset has no labels defined.")

# View tables in dataset.
print("Tables:")
tables = list(client.list_tables(dataset))  # Make an API request(s).
if tables:
    for table in tables:
        print("\t{}".format(table.table_id))
else:
    print("\tThis dataset does not contain any tables.")
```

## 確認資料集名稱

下列範例說明如何檢查資料集是否存在：

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import com.google.cloud.bigquery.DatasetId;

// Sample to check dataset exist
public class DatasetExists {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    datasetExists(datasetName);
  }

  public static void datasetExists(String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Dataset dataset = bigquery.getDataset(DatasetId.of(datasetName));
      if (dataset != null) {
        System.out.println("Dataset already exists.");
      } else {
        System.out.println("Dataset not found.");
      }
    } catch (BigQueryException e) {
      System.out.println("Something went wrong. \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset to determine existence.
# dataset_id = "your-project.your_dataset"

try:
    client.get_dataset(dataset_id)  # Make an API request.
    print("Dataset {} already exists".format(dataset_id))
except NotFound:
    print("Dataset {} is not found".format(dataset_id))
```

## 後續步驟

* 參閱[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)一文，進一步瞭解如何建立資料集。
* 如要進一步瞭解如何指派存取權控管權限給資料集，請參閱[控管資料集存取權](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-tw)。
* 如要進一步瞭解如何變更資料集屬性，請參閱[更新資料集屬性](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw)。
* 要進一步瞭解如何建立及管理標籤，請參閱[建立及管理標籤](https://docs.cloud.google.com/bigquery/docs/labels?hl=zh-tw)相關頁面。
* 如要查看 `INFORMATION_SCHEMA` 的總覽，請前往 [BigQuery `INFORMATION_SCHEMA` 簡介](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)頁面。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]