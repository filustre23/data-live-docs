Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用標籤篩選資源

如要使用標籤篩選資源，請執行下列其中一項操作：

* 使用 Google Cloud 控制台中的搜尋列。
* 建立用於 API、bq 指令列工具或用戶端程式庫的篩選規格。

## 限制

* API、bq 指令列工具和用戶端程式庫僅支援對資料集進行篩選。
* 您無法在任何 BigQuery 工具中使用標籤篩選工作。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文件各項工作所需的權限。

### 所需權限

如要使用標籤篩選資源，您必須具備擷取資源中繼資料的權限，如要使用標籤篩選資源，您需要下列 IAM 權限：

* `bigquery.datasets.get` (可篩選資料集)
* `bigquery.tables.get` (可篩選資料表和檢視表)

下列每個預先定義的 IAM 角色都包含篩選資料集所需的權限：

* `roles/bigquery.user`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.admin`

下列預先定義的 IAM 角色都包含篩選表格和檢視畫面所需的權限：

* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.admin`

此外，如果您有 `bigquery.datasets.create` 權限，可以篩選您建立的資源。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 在 Google Cloud 控制台中篩選資源

如要產生資源的篩選清單，請使用 Google Cloud 控制台：

1. 前往 Google Cloud 控制台的「Explorer」窗格。
2. 在搜尋列中，輸入 `key` 或 `key:value` 組合。搜尋結果會包含所有部分相符的結果。

   舉例來說，如只要顯示具有 `department:shipping` 標籤的資料集，您可以輸入 `department` 或 `department:shipping`。

## 在 API 或 bq 指令列工具中篩選資料集

API、bq 指令列工具和用戶端程式庫僅支援對資料集進行篩選。

如要使用 API、bq 工具或用戶端程式庫來篩選資料集，請建立並使用篩選規格：

* 做為 bq 工具中 `--filter` 標記的參數
* 做為 API `datasets.list` 方法中 `filter` 屬性的值

### 篩選規格的限制

篩選規格有下列限制：

* 僅支援 `AND` 邏輯運算子。系統會將以空格分隔的比較結果，視為具有隱性 `AND` 運算子。
* 唯一符合篩選規格的欄位是 `labels.key`，其中 `key` 是標籤名稱。
* 篩選運算式中的每個 `key` 都不得重複。
* 篩選規格最多可以包含十個運算式。
* 篩選規格須區分大小寫。
* API、bq 指令列工具和用戶端程式庫僅支援對資料集進行篩選。

### 篩選規格範例

篩選規格使用下列語法：

`"field[:value][ field[:value]]..."`

更改下列內容：

* `field` 表示為 `labels.key`，其中 key 是標籤鍵。
* `value` 是選用的標籤值。

下列範例說明如何產生篩選器運算式。

如要列出具有 `department:shipping` 標籤的資源，請使用下列篩選規格：

`labels.department:shipping`

如要列出使用多個標籤的資源，請以空格分隔 `key:value` 組合。空格會被視為邏輯 `AND` 運算子。舉例來說，如要列出具有 `department:shipping` 和 `location:usa` 標籤的資料集，請使用下列篩選規格：

`labels.department:shipping labels.location:usa`

您可以單獨篩選某個鍵是否存在，而非比對鍵/值組合。無論值為何，下列篩選規格都會列出所有已加上 `department` 標籤的資料集：

`labels.department`

等效的篩選規格會使用星號來表示所有與 `department` 鍵相關聯的可能值：

`labels.department:*`

您也可以在篩選規格中使用標記。舉例來說，如要列出所有具備 `department:shipping` 標籤和 `test_data` 標記的資源，可使用下列篩選規格：

`labels.department:shipping labels.test_data`

### 在 bq 指令列工具和 API 中篩選資料集

如要使用 API、bq 指令列工具或用戶端程式庫來篩選資料集，請按照以下步驟操作：

### bq

發出含有 `--filter` 旗標的 `bq ls` 指令。如果要列出預設專案以外的專案資料集，請指定 `--project_id` 旗標。

```
bq ls \
--filter "filter_specification" \
--project_id project_id
```

更改下列內容：

* `filter_specification` 是有效的篩選規格。
* `project_id` 是您的專案 ID。

範例：

輸入下列指令，列出預設專案中含有 `department:shipping` 標籤的資料集：

```
bq ls --filter "labels.department:shipping"
```

輸入下列指令，列出預設專案中含有 `department:shipping` 標籤和 `test_data` 標記的資料集。

```
bq ls --filter "labels.department:shipping labels.test_data"
```

輸入下列指令，列出 `myotherproject` 中含有 `department:shipping` 標籤的資料集：

```
bq ls --filter "labels.department:shipping" --project_id myotherproject
```

各指令的輸出內容會傳回資料集清單，如下所示：

```
+-----------+
| datasetId |
+-----------+
| mydataset |
| mydataset2|
+-----------+
```

### API

呼叫 [`datasets.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list?hl=zh-tw) API 方法，並使用 `filter` 屬性提供篩選規格。

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

// listDatasetsByLabel demonstrates walking the collection of datasets in a project, and
// filtering that list to a subset that has specific label metadata.
func listDatasetsByLabel(w io.Writer, projectID string) error {
	// projectID := "my-project-id"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	it := client.Datasets(ctx)
	it.Filter = "labels.color:green"
	for {
		dataset, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintf(w, "dataset: %s\n", dataset.DatasetID)
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
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;

// Sample to get list of datasets by label
public class ListDatasetsByLabel {

  public static void runListDatasetsByLabel() {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String filter = "MY_LABEL_FILTER";
    listDatasetsByLabel(projectId, filter);
  }

  public static void listDatasetsByLabel(String projectId, String filter) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Page<Dataset> datasets =
          bigquery.listDatasets(
              projectId,
              BigQuery.DatasetListOption.pageSize(100),
              BigQuery.DatasetListOption.labelFilter(filter)); // "labels.color:green"
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

async function listDatasetsByLabel() {
  // Lists all datasets in current GCP project, filtering by label color:green.

  const options = {
    filter: 'labels.color:green',
  };
  // Lists all datasets in the specified project
  const [datasets] = await bigquery.getDatasets(options);

  console.log('Datasets:');
  datasets.forEach(dataset => console.log(dataset.id));
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

label_filter = "labels.color:green"
datasets = list(client.list_datasets(filter=label_filter))  # Make an API request.

if datasets:
    print("Datasets filtered by {}:".format(label_filter))
    for dataset in datasets:
        print("\t{}.{}".format(dataset.project, dataset.dataset_id))
else:
    print("No datasets found with this filter.")
```

## 後續步驟

* 瞭解如何為 BigQuery 資源[加上標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw)。
* 瞭解如何[使用標籤識別及分析代理程式產生的查詢](https://docs.cloud.google.com/bigquery/docs/conversational-analytics?hl=zh-tw#agent-queries)。
* 瞭解如何在 BigQuery 資源中[查看標籤](https://docs.cloud.google.com/bigquery/docs/viewing-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[更新標籤](https://docs.cloud.google.com/bigquery/docs/updating-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[刪除標籤](https://docs.cloud.google.com/bigquery/docs/deleting-labels?hl=zh-tw)。
* 請參閱 Resource Manager 說明文件中的[使用標籤](https://docs.cloud.google.com/resource-manager/docs/using-labels?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]