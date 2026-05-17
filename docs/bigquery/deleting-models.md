Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 可刪除模型

本頁說明如何刪除 BigQuery ML 模型。您可透過以下方式刪除模型：

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具的 `bq rm` 指令或 `bq query` 指令
* 呼叫 [`models.delete`](https://docs.cloud.google.com/bigquery/docs/reference/v2/models/delete?hl=zh-tw) API 方法或 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 方法
* 使用用戶端程式庫

一次只能刪除一個模型。刪除模型時，也會刪除模型中的所有資料。

如要在指定時間過後自動刪除模型，您可在使用 bq 指令列工具、API 或用戶端程式庫時，設定模型的到期時間。如您在建立模型時未設定到期，則可[更新模型的到期時間](https://docs.cloud.google.com/bigquery/docs/updating-model-metadata?hl=zh-tw#expiration)。

## 刪除模型的限制

刪除模型有下列限制：

* 您無法同時刪除多個模型，你必須個別刪除這些項目。
* 刪除模型後無法復原。

## 所需權限

如要刪除資料集中的模型，您必須取得資料集的 [`WRITER`](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset) 角色，或取得包含 `bigquery.models.delete` 權限的專案層級身分與存取權管理 (IAM) 角色。如您已取得專案層級的 `bigquery.models.delete` 權限，則可刪除專案內任何資料集中的模型。下列專案層級身分與存取權管理角色包含 `bigquery.models.delete` 權限：

* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.admin`

如要進一步瞭解 BigQuery ML 中的 IAM 角色和權限，請參閱[存取權控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

## 刪除模型

如要刪除模型，請按照下列步驟操作：

### 控制台

您可使用 Google Cloud 控制台的「Delete Model」(刪除模型) 選項，或是執行內含 [`DROP MODEL | DROP MODEL IF EXISTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-drop-model?hl=zh-tw) DDL 陳述式的查詢，以刪除模型。

**選項一：**使用「Delete Model」(刪除模型) 選項。

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下資料集。
3. 按一下「模型」分頁標籤，然後按一下模型名稱選取模型。
4. 點按模型選項圖示 more\_vert，然後點選「刪除」。
5. 在「Delete Model」(刪除模型) 對話方塊中，輸入 `delete`，然後點選「Delete」(刪除)。

**選項二：**使用 DDL 陳述式。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 [Compose new query] (撰寫新查詢)。
3. 在「Query editor」(查詢編輯器) 的文字區域中輸入 DDL 陳述式。

   ```
    DROP MODEL mydataset.mymodel
   ```
4. 按一下「執行」。當查詢完成時，就會從導覽窗格中移除模型。

### bq

您可使用 bq 指令列工具輸入以下指令來刪除模型：

* `bq rm` 指令，並加上 `--model` 或 `-m` 旗標
* `bq query` 指令，並提供 DDL 陳述式做為查詢參數

如要刪除非預設專案中的模型，請使用下列格式將專案 ID 新增至資料集：`[PROJECT_ID]:[DATASET].[MODEL]`。

**選項一：**輸入 `bq rm` 指令

當您使用 `bq rm` 指令移除模型時，必須確認該操作。您可以使用 `--force flag` (或 `-f` 捷徑) 來略過確認程序。

```
bq rm -f --model PROJECT_ID:DATASET.MODEL
```

更改下列內容：

* `PROJECT_ID` 是您的專案 ID。
* `DATASET` 是資料集名稱。
* `MODEL` 是模型的名稱。

`rm` 指令不會產生任何輸出。

範例：

輸入下列指令從 `mydataset` 刪除 `mymodel`。`mydataset` 在您的預設專案中。

```
bq rm --model mydataset.mymodel
```

輸入下列指令從 `mydataset` 刪除 `mymodel`。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq rm --model myotherproject:mydataset.mymodel
```

輸入下列指令從 `mydataset` 刪除 `mymodel`。`mydataset` 在您的預設專案中。這個指令使用 `-f` 捷徑略過確認程序。

```
bq rm -f --model mydataset.mymodel
```

您可以發出 `bq ls` 指令，確認模型已刪除。
詳情請參閱「[列出模型](https://docs.cloud.google.com/bigquery/docs/listing-models?hl=zh-tw)」。

**選項二：**輸入 `bq query` 指令

如要使用 `bq query` 指令刪除模型，請在查詢參數中提供 `DROP MODEL` 陳述式，並提供 `--use_legacy_sql=false` 標記以指定 GoogleSQL 查詢語法。

範例：

輸入下列指令從 `mydataset` 刪除 `mymodel`。`mydataset` 在您的預設專案中。

```
bq query --use_legacy_sql=false 'DROP MODEL mydataset.mymodel'
```

輸入下列指令從 `mydataset` 刪除 `mymodel`。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq query --use_legacy_sql=false \
'DROP MODEL myotherproject:mydataset.mymodel'
```

### API

**選項一：**呼叫 `models.delete` 方法

如要刪除模型，請呼叫 [`models.delete`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models/delete?hl=zh-tw) 方法，並提供 `projectId`、`datasetId` 和 `modelId`。

**選項二：**呼叫 `jobs.query` 方法

如要刪除模型，請呼叫 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 方法，並在要求主體的 [query](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw#queryrequest) 屬性中提供 `DROP MODEL` DDL 陳述式。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// deleteModel demonstrates deletion of BigQuery ML model.
func deleteModel(projectID, datasetID, modelID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// modelID := "mymodel"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	model := client.Dataset(datasetID).Model(modelID)
	if err := model.Delete(ctx); err != nil {
		return fmt.Errorf("couldn't delete model: %w", err)
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.ModelId;

// Sample to delete a model
public class DeleteModel {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String modelName = "MY_MODEL_NAME";
    deleteModel(datasetName, modelName);
  }

  public static void deleteModel(String datasetName, String modelName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();
      boolean success = bigquery.delete(ModelId.of(datasetName, modelName));
      if (success) {
        System.out.println("Model deleted successfully");
      } else {
        System.out.println("Model was not found");
      }
    } catch (BigQueryException e) {
      System.out.println("Model was not deleted. \n" + e.toString());
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

async function deleteModel() {
  // Deletes a model named "my_model" from "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample
   */
  // const datasetId = "my_dataset";
  // const modelId = "my_model";

  const dataset = bigquery.dataset(datasetId);
  const model = dataset.model(modelId);
  await model.delete();

  console.log(`Model ${modelId} deleted.`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set model_id to the ID of the model to fetch.
# model_id = 'your-project.your_dataset.your_model'

client.delete_model(model_id)  # Make an API request.

print("Deleted model '{}'.".format(model_id))
```

## 還原已刪除的模型

刪除模型後無法復原。

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要開始使用 BigQuery ML，請參閱[在 BigQuery ML 中建立機器學習模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model?hl=zh-tw)。
* 如要進一步瞭解模型的使用方式，請參閱以下說明：
  + [取得模型中繼資料](https://docs.cloud.google.com/bigquery/docs/getting-model-metadata?hl=zh-tw)
  + [列出模型](https://docs.cloud.google.com/bigquery/docs/listing-models?hl=zh-tw)
  + [更新模型中繼資料](https://docs.cloud.google.com/bigquery/docs/updating-model-metadata?hl=zh-tw)
  + [管理模型](https://docs.cloud.google.com/bigquery/docs/managing-models?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]