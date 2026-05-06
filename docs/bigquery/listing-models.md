Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 列出模型

本頁說明如何列出資料集中的 BigQuery ML 模型。您可透過以下方式來列出 BigQuery ML 模型：

* 使用 Google Cloud 控制台。
* 在 bq 指令列工具中使用 `bq ls` 指令。
* 直接呼叫 [`models.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models/list?hl=zh-tw) API 方法，或是使用用戶端程式庫。

## 所需權限

如要列出資料集中的模型，您必須取得資料集的 [`READER`](https://docs.cloud.google.com/bigquery/docs/access-control-basic-roles?hl=zh-tw#dataset-basic-roles) 角色，或取得包含 `bigquery.models.list` 權限的專案層級身分與存取權管理 (IAM) 角色。如果您取得專案層級的 `bigquery.models.list` 權限，就能列出專案中任何資料集的模型。下列預先定義的專案層級身分與存取權管理角色包含 `bigquery.models.list` 權限：

* `bigquery.dataViewer`
* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.metadataViewer`
* `bigquery.user`
* `bigquery.admin`

如要進一步瞭解 BigQuery ML 中的身分與存取權管理角色以及權限，請參閱[存取權控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。如要進一步瞭解資料集層級角色，請參閱[資料集的基本角色](https://docs.cloud.google.com/bigquery/docs/access-control-basic-roles?hl=zh-tw#dataset-basic-roles)。

## 列出模型

如要列出資料集中的模型：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)。
4. 按一下包含模型的資料集。
5. 按一下「模型」分頁標籤。

### bq

發出含有 `--models` 或 `-m` 旗標的 `bq ls` 指令。[`--format`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#global_flags) 標記可用來控管輸出。如您正在列出非預設專案中的模型，請以下列格式將專案 ID 新增至資料集：`[PROJECT_ID]:[DATASET]`。

```
bq ls -m --format=pretty PROJECT_ID:DATASET
```

更改下列內容：

* `PROJECT_ID` 是您的專案 ID。
* `DATASET` 是資料集名稱。

使用 `--format=pretty` 標記時，指令輸出內容如下所示。`--format=pretty` 會產生格式化表格輸出內容。`Model Type`
欄會顯示模型類型，例如 `KMEANS`。

```
+-------------------------+------------+--------+-----------------+
|           Id            | Model Type | Labels |  Creation Time  |
+-------------------------+------------+--------+-----------------+
| mymodel                 | KMEANS     |        | 03 May 03:02:27 |
+-------------------------+------------+--------+-----------------+
```

範例：

輸入下列指令，列出預設專案中資料集 `mydataset` 內的模型。

```
bq ls --models --format=pretty mydataset
```

輸入下列指令，列出 `myotherproject` 中資料集 `mydataset` 內的模型。這個指令使用 `-m` 捷徑來列出模型。

```
bq ls -m --format=pretty myotherproject:mydataset
```

### API

如要使用 API 列出模型，請呼叫 [`models.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models/list?hl=zh-tw) 方法，並提供 `projectId` 和 `datasetId`。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// listModels demonstrates iterating through the collection of ML models in a dataset
// and printing a basic identifier of the model.
func listModels(w io.Writer, projectID, datasetID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	fmt.Fprintf(w, "Models contained in dataset %q\n", datasetID)
	it := client.Dataset(datasetID).Models(ctx)
	for {
		m, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintf(w, "Model: %s\n", m.FullyQualifiedName())
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.paging.Page;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQuery.ModelListOption;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Model;

public class ListModels {

  public static void runListModels() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    listModels(datasetName);
  }

  public static void listModels(String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Page<Model> models = bigquery.listModels(datasetName, ModelListOption.pageSize(100));
      if (models == null) {
        System.out.println("Dataset does not contain any models.");
        return;
      }
      models
          .iterateAll()
          .forEach(model -> System.out.printf("Success! Model ID: %s", model.getModelId()));
    } catch (BigQueryException e) {
      System.out.println("Models not listed in dataset due to error: \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function listModels() {
  // Lists all existing models in the dataset.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";

  const dataset = bigquery.dataset(datasetId);

  dataset.getModels().then(data => {
    const models = data[0];
    console.log('Models:');
    models.forEach(model => console.log(model.metadata));
  });
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset that contains
#                  the models you are listing.
# dataset_id = 'your-project.your_dataset'

models = client.list_models(dataset_id)  # Make an API request.

print("Models contained in '{}':".format(dataset_id))
for model in models:
    full_model_id = "{}.{}.{}".format(
        model.project, model.dataset_id, model.model_id
    )
    friendly_name = model.friendly_name
    print("{}: friendly_name='{}'".format(full_model_id, friendly_name))
```

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要開始使用 BigQuery ML，請參閱[在 BigQuery ML 中建立機器學習模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model?hl=zh-tw)。
* 如要進一步瞭解模型的使用方式，請參閱以下說明：
  + [取得模型中繼資料](https://docs.cloud.google.com/bigquery/docs/getting-model-metadata?hl=zh-tw)
  + [更新模型中繼資料](https://docs.cloud.google.com/bigquery/docs/updating-model-metadata?hl=zh-tw)
  + [管理模型](https://docs.cloud.google.com/bigquery/docs/managing-models?hl=zh-tw)
  + [刪除模型](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]