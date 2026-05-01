* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 取得模型中繼資料

本頁說明如何取得關於 BigQuery ML 模型的資訊或中繼資料。您可透過以下方式來取得模型中繼資料：

* 使用 Google Cloud 控制台
* 使用 `bq show` CLI 指令
* 直接呼叫 [`models.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models/get?hl=zh-tw) API 方法或使用用戶端程式庫

**注意：** 系統不支援透過查詢 `INFORMATION_SCHEMA` 檢視表取得模型相關資訊。

## 所需權限

如要取得模型中繼資料，您必須在資料集上獲派 [`READER`](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset) 角色，或獲派包含 `bigquery.models.getMetadata` 權限的專案層級身分與存取權管理 (IAM) 角色。如果您獲得專案層級的 `bigquery.models.getMetadata` 權限，即可取得專案內任何資料集中模型的中繼資料。以下是擁有 `bigquery.models.getMetadata` 權限的預先定義專案層級身分與存取權管理角色：

* `bigquery.dataViewer`
* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.metadataViewer`
* `bigquery.admin`

如要進一步瞭解 BigQuery ML 中的身分與存取權管理角色和權限，請參閱[存取權控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

## 取得模型中繼資料

如要取得有關模型的中繼資料：

### 控制台

1. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
3. 按一下「模型」分頁標籤，然後按一下模型名稱選取模型。
4. 按一下「詳細資料」分頁標籤。這個分頁會顯示模型的中繼資料，包括說明、標籤、模型類型和訓練選項。

### bq

發出具有 `--model` 或 `-m` 標記的 `bq show` 指令，以顯示模型中繼資料。[`--format`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#global_flags) 標記可用來控管輸出。

如果只想查看您模型的特徵欄，請使用 `--schema` 標記和 `--model` 標記。使用 `--schema` 旗標時，`--format` 必須設為 `json` 或 `prettyjson`。

如要取得非預設專案中模型的相關資訊，請以下列格式將專案 ID 新增至資料集：`[PROJECT_ID]:[DATASET]`。

```
bq show --model --format=prettyjson PROJECT_ID:DATASET.MODEL
```

更改下列內容：

* `PROJECT_ID` 是您的專案 ID。
* `DATASET` 是資料集名稱。
* `MODEL` 是模型的名稱。

使用 `--format=pretty` 標記時，指令輸出內容如下所示。如要查看完整詳細資料，請使用 `--format=prettyjson` 格式。範例輸出會顯示邏輯迴歸模型的中繼資料。

```
+--------------+---------------------+---------------------+---------------------------+--------+-----------------+-----------------+
|      Id      |     Model Type      |   Feature Columns   |       Label Columns       | Labels |  Creation Time  | Expiration Time |
+--------------+---------------------+---------------------+---------------------------+--------+-----------------+-----------------+
| sample_model | LOGISTIC_REGRESSION | |- column1: string  | |- label_column: int64    |        | 03 May 23:14:42 |                 |
|              |                     | |- column2: bool    |                           |        |                 |                 |
|              |                     | |- column3: string  |                           |        |                 |                 |
|              |                     | |- column4: int64   |                           |        |                 |                 |
+--------------+---------------------+---------------------+---------------------------+--------+-----------------+-----------------+
```

範例：

輸入下列指令，顯示 `mydataset` 中 `mymodel` 的所有相關資訊。`mydataset` 在您的預設專案中。

```
bq show --model --format=prettyjson mydataset.mymodel
```

輸入下列指令，顯示 `mydataset` 中 `mymodel` 的所有相關資訊。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq show --model --format=prettyjson myotherproject:mydataset.mymodel
```

輸入下列指令，只顯示 `mydataset` 中 `mymodel` 的特徵欄。`mydataset` 在 `myotherproject` 中，而不是在您的預設專案中。

```
bq show --model --schema --format=prettyjson \
myotherproject:mydataset.mymodel
```

### API

如要使用 API 取得模型中繼資料，請呼叫 [`models.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models/get?hl=zh-tw) 方法，並提供 `projectId`、`datasetId` 和 `modelId`。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
)

// printModelInfo demonstrates fetching metadata about a BigQuery ML model and printing some of
// it to an io.Writer.
func printModelInfo(w io.Writer, projectID, datasetID, modelID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// modelID := "mymodel"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	meta, err := client.Dataset(datasetID).Model(modelID).Metadata(ctx)
	if err != nil {
		return fmt.Errorf("couldn't retrieve metadata: %w", err)
	}
	fmt.Fprintf(w, "Got model '%q' with friendly name '%q'\n", modelID, meta.Name)
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Model;
import com.google.cloud.bigquery.ModelId;

public class GetModel {

  public static void runGetModel() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String modelName = "MY_MODEL_ID";
    getModel(datasetName, modelName);
  }

  public static void getModel(String datasetName, String modelName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      ModelId modelId = ModelId.of(datasetName, modelName);
      Model model = bigquery.getModel(modelId);
      System.out.println("Model: " + model.getDescription());

      System.out.println("Successfully retrieved model");
    } catch (BigQueryException e) {
      System.out.println("Cannot retrieve model \n" + e.toString());
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

async function getModel() {
  // Retrieves model named "my_existing_model" in "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample
   */
  // const datasetId = "my_dataset";
  // const modelId = "my_existing_model";

  const dataset = bigquery.dataset(datasetId);
  const [model] = await dataset.model(modelId).get();

  console.log('Model:');
  console.log(model.metadata.modelReference);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set model_id to the ID of the model to fetch.
# model_id = 'your-project.your_dataset.your_model'

model = client.get_model(model_id)  # Make an API request.

full_model_id = "{}.{}.{}".format(model.project, model.dataset_id, model.model_id)
friendly_name = model.friendly_name
print(
    "Got model '{}' with friendly_name '{}'.".format(full_model_id, friendly_name)
)
```

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要開始使用 BigQuery ML，請參閱[在 BigQuery ML 中建立機器學習模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model?hl=zh-tw)。
* 如要進一步瞭解模型的使用方式，請參閱以下說明：
  + [列出模型](https://docs.cloud.google.com/bigquery/docs/listing-models?hl=zh-tw)
  + [更新模型中繼資料](https://docs.cloud.google.com/bigquery/docs/updating-model-metadata?hl=zh-tw)
  + [管理模型](https://docs.cloud.google.com/bigquery/docs/managing-models?hl=zh-tw)
  + [刪除模型](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]