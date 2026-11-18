Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 更新模型中繼資料

更新 BigQuery ML 模型中繼資料，有助於整理及管理機器學習資產的生命週期。您可以修改模型的[**說明**](#description)、[**標籤**](#labels)和[**到期時間**](#expiration)，以便識別資源、使用鍵/值組合追蹤用量，以及自動刪除過時的模型。

## 所需權限

如要更新模型中繼資料，您必須具備資料集的 [`WRITER`](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset) 角色，或具備包含 `bigquery.models.updateMetadata` 權限的專案層級 Identity and Access Management (IAM) 角色。如果您在專案層級獲得 `bigquery.models.updateMetadata` 權限，則可更新專案中任何資料集的模型中繼資料。下列預先定義的專案層級 IAM 角色包含 `bigquery.models.updateMetadata` 權限：

* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.admin`

如要進一步瞭解 BigQuery ML 的 IAM 角色和權限，請參閱「[存取控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 更新模型說明

模型說明是用來識別模型的文字字串。

如何更新模型的說明：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
4. 按一下「Models」(模型) 分頁標籤，然後點選模型名稱來選取模型。
5. 點按「Details」(詳細資料) 分頁標籤。
6. 如要更新模型說明，請按一下「Edit」(編輯) edit。
7. 在「Edit detail」(編輯詳細資料) 對話方塊中，更新說明，然後按一下「Save」(儲存)。

### bq

如要更新模型說明，請發出 `bq update` 指令，並加上 `--model` 或 `-m` 旗標和 `--description` 旗標。

如要更新預設專案以外的模型，請按照下列格式，將專案 ID 新增至資料集：`[PROJECT_ID]:[DATASET]`。

```
bq update --model --description "[STRING]" PROJECT_ID:DATASET.MODEL
```

更改下列內容：

* `STRING` 是描述模型的文字字串 (置於引號之中)。
* `PROJECT_ID` 是您的專案 ID。
* `DATASET` 是資料集名稱。
* `MODEL` 是模型的名稱。

指令輸出內容如下所示：

```
Model 'myproject.mydataset.mymodel' successfully updated.
```

您可以發出 `bq show` 指令來確認變更。詳情請參閱「[取得模型中繼資料](https://docs.cloud.google.com/bigquery/docs/getting-model-metadata?hl=zh-tw)」。

範例：

輸入下列指令，更新預設專案中 `mydataset` 內 `mymodel` 的說明。

```
bq update --model --description "My updated description" \
mydataset.mymodel
```

輸入下列指令，更新 `myotherproject` 中 `mydataset` 的 `mymodel` 說明。

```
bq update --model --description "My updated description" \
myotherproject:mydataset.mymodel
```

### API

如要使用 API 更新模型說明，請呼叫 [`models.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models/patch?hl=zh-tw) 方法，並提供 `projectId`、`datasetId` 和 `modelId`。如要修改說明，請新增或更新[模型資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models?hl=zh-tw#Model)的「description」屬性。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// updateModelDescription demonstrates fetching BigQuery ML model metadata and updating the
// Description metadata.
func updateModelDescription(projectID, datasetID, modelID string) error {
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
	oldMeta, err := model.Metadata(ctx)
	if err != nil {
		return fmt.Errorf("couldn't retrieve model metadata: %w", err)
	}
	update := bigquery.ModelMetadataToUpdate{
		Description: "This model was modified from a Go program",
	}
	if _, err = model.Update(ctx, update, oldMeta.ETag); err != nil {
		return fmt.Errorf("couldn't update model: %w", err)
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Model;
import com.google.cloud.bigquery.ModelId;

// Sample to update description on a model
public class UpdateModelDescription {

  public static void runUpdateModelDescription() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String modelName = "MY_MODEL_NAME";
    String newDescription = "A really great model.";
    updateModelDescription(datasetName, modelName, newDescription);
  }

  public static void updateModelDescription(
      String datasetName, String modelName, String newDescription) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Model model = bigquery.getModel(ModelId.of(datasetName, modelName));
      bigquery.update(model.toBuilder().setDescription(newDescription).build());
      System.out.println("Model description updated successfully to " + newDescription);
    } catch (BigQueryException e) {
      System.out.println("Model description was not updated \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function updateModel() {
  // Updates a model's metadata.

  /**
   * TODO(developer): Uncomment the following lines before running the sample
   */
  // const datasetId = "my_dataset";
  // const modelId = "my__model";

  const metadata = {
    description: 'A really great model.',
  };

  const dataset = bigquery.dataset(datasetId);
  const [apiResponse] = await dataset.model(modelId).setMetadata(metadata);
  const newDescription = apiResponse.description;

  console.log(`${modelId} description: ${newDescription}`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set model_id to the ID of the model to fetch.
# model_id = 'your-project.your_dataset.your_model'

model = client.get_model(model_id)  # Make an API request.
model.description = "This model was modified from a Python program."
model = client.update_model(model, ["description"])  # Make an API request.

full_model_id = "{}.{}.{}".format(model.project, model.dataset_id, model.model_id)
print(
    "Updated model '{}' with description '{}'.".format(
        full_model_id, model.description
    )
)
```

## 更新模型標籤

標籤是您可以附加至資源的鍵/值組合。建立 BigQuery ML 資源時可以選擇是否要加入標籤。詳情請參閱「[新增及使用標籤](https://docs.cloud.google.com/bigquery/docs/adding-using-labels?hl=zh-tw)」。

如要更新模型標籤：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
3. 按一下「Models」(模型) 分頁標籤，然後點選模型名稱來選取模型。
4. 點按「Details」(詳細資料) 分頁標籤。
5. 如要更新模型的標籤，請按一下「Edit」(編輯) edit。
6. 在「Edit detail」(編輯詳細資料) 對話方塊中，新增、刪除或修改標籤，然後按一下「Save」(儲存)。

### bq

如要更新模型的標籤，請發出 `bq update` 指令，並加上 `--model` 或 `-m` 旗標和 `--set_label` 旗標。重複使用 `--set_label` 旗標，即可新增或更新多個標籤。

如要更新預設專案以外的模型，請按照下列格式，將專案 ID 新增至資料集：`[PROJECT_ID]:[DATASET]`。

```
bq update --model --set_label KEY:VALUE \
PROJECT_ID:DATASET.MODEL
```

更改下列內容：

* `KEY:VALUE` 對應至要新增或更新的標籤鍵/值組合。如果您指定與現有標籤相同的鍵，該標籤的值就會更新。鍵不得重複。
* `PROJECT_ID` 是您的專案 ID。
* `DATASET` 是資料集名稱。
* `MODEL` 是模型的名稱。

指令輸出內容如下所示：

```
Model 'myproject.mydataset.mymodel' successfully updated.
```

您可以發出 `bq show` 指令來確認變更。詳情請參閱「[取得模型中繼資料](https://docs.cloud.google.com/bigquery/docs/getting-model-metadata?hl=zh-tw)」。

範例：

如要更新 `mymodel` 上的 `department` 標籤，請輸入 `bq update` 指令，並指定 `department` 做為標籤鍵。舉例來說，如要將 `department:shipping` 標籤更新為 `department:logistics`，請輸入下列指令。`mydataset` 位於 `myotherproject`，而非預設專案。

```
bq update --model --set_label department:logistics \
myotherproject:mydataset.mymodel
```

### API

如要使用 API 更新模型的標籤，請呼叫 [`models.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models/patch?hl=zh-tw) 方法，並提供 `projectId`、`datasetId` 和 `modelId`。如要修改標籤，請新增或更新[模型資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models?hl=zh-tw#Model)的「labels」屬性。

## 更新模型的到期時間

模型的到期時間是一種時間戳記值，此值會決定刪除模型的時間。您可在使用 CLI、API 或用戶端程式庫時，設定模型的到期時間。您也可以在建立模型後，設定或更新模型的到期時間。模型的到期時間通常稱為「存留時間」或 TTL。

如果未設定模型的到期時間，模型就永不失效，您必須手動[刪除](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw)模型。

**注意：** Google Cloud 控制台不支援設定或更新模型的到期時間。

到期時間的值會依該值的設定位置而有不同的表示方式。請使用可為您提供適當精細層級的方法：

* 在指令列工具中，到期時間會以目前 UTC 時間表示 (單位為秒)。一旦您在指令列指定到期時間，系統就會將您設定的整數值 (以秒為單位) 加至當下的 UTC 時間戳記。
* 在 API 中，到期時間會自訓練週期開始計算，並以毫秒為單位表示。如果您指定的到期值小於當下的時間戳記，則模型會立即到期。

如要更新模型的到期時間：

### 控制台

Google Cloud 控制台不支援設定或更新模型的到期時間。

### bq

如要更新模型的到期時間，請發出 `bq update` 指令，並加上 `--model` 或 `-m` 旗標和 `--expiration` 旗標。

如要更新預設專案以外的模型，請按照下列格式，將專案 ID 新增至資料集：`[PROJECT_ID]:[DATASET]`。

```
bq update --model --expiration INTEGER \
PROJECT_ID:DATASET.MODEL
```

更改下列內容：

* `INTEGER` 是模型的生命週期 (單位為秒)。最小值是 3600 秒 (1 小時)。到期時間為目前世界標準時間加整數值。
* `PROJECT_ID` 是您的專案 ID。
* `DATASET` 是資料集名稱。
* `MODEL` 是模型的名稱。

指令輸出內容如下所示：

```
Model 'myproject.mydataset.mymodel' successfully updated.
```

您可以發出 `bq show` 指令來確認變更。詳情請參閱「[取得模型中繼資料](https://docs.cloud.google.com/bigquery/docs/getting-model-metadata?hl=zh-tw)」。

範例：

輸入下列指令，將 `mydataset` 中的 `mymodel` 到期時間更新為 5 天 (432000 秒)。`mydataset` 位於您的預設專案中。

```
bq update --model --expiration 432000 mydataset.mymodel
```

輸入下列指令，將 `mydataset` 中的 `mymodel` 到期時間更新為 5 天 (432000 秒)。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq update --model --expiration 432000 myotherproject:mydataset.mymodel
```

### API

如要使用 API 更新模型的到期時間，請呼叫 [`models.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models/patch?hl=zh-tw) 方法，並提供 `projectId`、`datasetId` 和 `modelId`。如要修改到期時間，請新增或更新[模型資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models?hl=zh-tw#Model)的「expirationTime」屬性。「expirationTime」以毫秒為單位，自 Epoch 紀元時間起算。

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要開始使用 BigQuery ML，請參閱「[在 BigQuery ML 中建立機器學習模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model?hl=zh-tw)」。
* 如要進一步瞭解如何使用模型，請參閱：
  + [取得模型中繼資料](https://docs.cloud.google.com/bigquery/docs/getting-model-metadata?hl=zh-tw)
  + [列出模型](https://docs.cloud.google.com/bigquery/docs/listing-models?hl=zh-tw)
  + [管理模型](https://docs.cloud.google.com/bigquery/docs/managing-models?hl=zh-tw)
  + [刪除模型](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-17 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-17 (世界標準時間)。"],[],[]]