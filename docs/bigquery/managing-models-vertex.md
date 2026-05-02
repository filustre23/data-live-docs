* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 Vertex AI 中管理 BigQuery ML 模型

您可以將 BigQuery ML 模型註冊至 Vertex AI Model Registry，以便與 Vertex AI 模型一併管理，無須匯出模型。向 Model Registry 註冊模型後，您就能透過單一介面建立版本、評估及部署模型，進行線上預測，而且不需要提供模型的容器。如果您不熟悉 Vertex AI，以及如何與 BigQuery ML 整合，請參閱 [Vertex AI for BigQuery users](https://docs.cloud.google.com/vertex-ai/docs/beginner/bqml?hl=zh-tw)。

如要進一步瞭解 Vertex AI 預測，請參閱「[Vertex AI 預測總覽](https://docs.cloud.google.com/vertex-ai/docs/predictions/overview?hl=zh-tw)」。

**注意：** 雖然可以註冊所有模型類型，但某些模型類型的部署作業會受到限制。詳情請參閱[模型部署](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw#model-deployment)。

如要瞭解如何透過 Vertex AI Model Registry 管理 BigQuery ML 模型，請參閱「[Vertex AI Model Registry 簡介](https://docs.cloud.google.com/vertex-ai/docs/model-registry/introduction?hl=zh-tw)」。

## 事前準備

啟用 Vertex AI API。

**啟用 API 時所需的角色**

如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

[啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com&hl=zh-tw)

## 所需權限

如要取得將 BigQuery ML 模型註冊至 Model Registry 所需的權限，請要求管理員在專案中授予您 [Vertex AI 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.admin)  (`roles/aiplatform.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 註冊模型

建立 BigQuery ML 模型時，您可以透過下列方式將模型註冊至 Model Registry：

* 在 Google Cloud 控制台中，選取「Explorer」窗格中的模型，然後按一下「Registry」分頁中的「Register」。([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))
* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)。在 `CREATE MODEL` 陳述式中，您可以使用下列選項將模型註冊至 Model Registry：

  + `MODEL_REGISTRY`：將模型註冊至 Model Registry。
  + `VERTEX_AI_MODEL_ID`：指定要在 Model Registry 中使用的模型 ID。模型 ID 與 BigQuery ML 模型相關聯，且會顯示在 Model Registry 中。每個 BigQuery ML 模型只能在 Model Registry 中註冊一個模型 ID。
  + `VERTEX_AI_MODEL_VERSION_ALIASES`：指定一或多個模型版本別名，以便簡化部署作業、管理模型，並為模型啟用 [Vertex Explainable AI](https://docs.cloud.google.com/vertex-ai/docs/explainable-ai/overview?hl=zh-tw)。

  如果您在建立模型時設定 `MODEL_REGISTRY` 選項，模型就會註冊至 Model Registry，並在 BigQuery ML 中完成訓練後，自動顯示在該處。您可以在Google Cloud 控制台的「模型登錄」頁面中，使用「來源」欄查看模型的來源。

註冊 BigQuery ML 模型後，您可以使用下列 Model Registry 功能：

* [將模型部署至端點](https://docs.cloud.google.com/vertex-ai/docs/predictions/deploy-model-console?hl=zh-tw)
* [比較模型版本](https://docs.cloud.google.com/vertex-ai/docs/model-registry/versioning?hl=zh-tw)
* [取得預測結果](https://docs.cloud.google.com/vertex-ai/docs/predictions/get-predictions?hl=zh-tw#get_predictions_from_custom_trained_models)
* [監控模型](https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview?hl=zh-tw)
* [查看模型評估結果](https://docs.cloud.google.com/vertex-ai/docs/evaluation/introduction?hl=zh-tw)
* [取得模型的特徵式說明](https://docs.cloud.google.com/vertex-ai/docs/explainable-ai/overview?hl=zh-tw#feature-based)

無論是否已向 Model Registry 註冊，使用 BigQuery ML 建立的所有模型仍會顯示在 BigQuery 使用者介面中。

下列範例說明如何建立及註冊 k-means 模型：

```
CREATE OR REPLACE MODEL `mydataset.my_kmeans_model`
  MODEL_TYPE = 'KMEANS',
  MODEL_REGISTRY = 'VERTEX_AI',
  VERTEX_AI_MODEL_ID = 'customer_clustering';
```

### 將現有的 BigQuery ML 模型註冊至 Model Registry

如果您在建立模型時未將模型登錄至 Vertex AI，之後可以使用 SQL、bq 指令列工具或 BigQuery API 登錄模型。

下列範例說明如何註冊現有模型：

### 控制台

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中，依序點選「Datasets」和含有模型的資料集。
4. 按一下「模型」分頁標籤，然後點選要註冊的模型。
5. 在模型詳細資料窗格中，選取「登錄」分頁標籤。
6. 按一下「註冊」。
7. 在「向 Vertex Model Registry 註冊模型」窗格中，執行下列其中一項操作：

   * 選取「註冊為新的模型」。在「Model name」(模型名稱) 中，輸入模型名稱。
   * 選取「註冊為現有模型的新版本」。

     1. 在「模型名稱」中，輸入模型名稱。
     2. 選用。如要使用版本別名，請選取「版本別名」，然後輸入版本別名。
8. 按一下「註冊」。

### SQL

使用 [`ALTER MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-alter-model?hl=zh-tw)：

```
ALTER MODEL IF EXISTS mymodel SET OPTIONS (vertex_ai_model_id='my_vertex_ai_model_id');
```

### bq

使用加上 `--model` 旗標的 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)：

```
  bq update --model --vertex_ai_model_id 'my_vertex_ai_model_id' myproject:mydataset.mymodel
```

### API

請使用 [`models.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models/patch?hl=zh-tw)。傳入包含 [`trainingRuns` 物件的 [`Model` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models?hl=zh-tw#Model)](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models?hl=zh-tw#TrainingRun)，並填入 `vertexAiModelId` 欄位：

```
{
  "trainingRuns": [
    {
      "vertexAiModelId": my_vertex_ai_model_id
    }
}
```

### 註冊多個版本的 BigQuery ML 模型

在特定模型 ID 下註冊的第一個 BigQuery ML 模型，會以該模型的版本 1 顯示在 Model Registry 中。建立或變更其他 BigQuery ML 模型時，只要指定相同的 Vertex AI 模型 ID，即可將這些模型註冊為已註冊模型的不同版本。

舉例來說，您可以在 BigQuery ML 中建立 `model1`，並在 Model Registry 中將其註冊為 `regression_model`。`model1`
在 Model Registry 中會顯示為 `regression_model` 的版本 1。如果您接著在 BigQuery ML 中建立 `model2`，並在 Model Registry 中將其註冊為 `regression_model`，則 `model2` 會在 Model Registry 中顯示為 `regression_model` 的第 2 版。

如果您建立或取代 BigQuery ML 模型，並使用已與 Model Registry 中的模型建立關聯的 BigQuery ML 模型名稱，系統會刪除現有的 Model Registry 模型版本，並以新模型取代。以上述範例為基礎，如果您使用 `CREATE OR REPLACE MODEL` 陳述式和 `MODEL_REGISTRY` 和 `VERTEX_AI_MODEL_ID` 選項，在 BigQuery ML 中建立或取代 `model2`，則模型登錄中的 `regression_model` 第 2 版會遭到取代，且模型登錄會顯示 `regression_model` 模型第 1 版和第 3 版。

### 變更已註冊 BigQuery ML 模型的模型 ID

BigQuery ML 模型註冊至 Model Registry 後，就無法變更 `VERTEX_AI_MODEL_ID` 值。如要使用新的 `VERTEX_AI_MODEL_ID` 註冊模型，請使用下列任一選項：

* [刪除模型](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw#delete_a_model)並重新建立，指定 `VERTEX_AI_MODEL_ID` 選項的新值。但這種做法會產生重新訓練的費用。
* [複製模型](https://docs.cloud.google.com/bigquery/docs/managing-models?hl=zh-tw#copy_a_model)，然後使用 `ALTER MODEL` 陳述式，以新的 `VERTEX_AI_MODEL_ID` 值註冊新模型。

### 位置注意事項

如果您將多區域 BigQuery ML 模型註冊至 Model Registry，該模型就會成為 Vertex AI 中的區域模型。BigQuery ML 美國多區域模型會同步至 Vertex AI (us-central1)，而 BigQuery ML 歐洲多區域模型則會同步至 Vertex AI (europe-west4)。單一區域模型不受影響。

如要瞭解如何更新模型位置，請參閱「[選擇位置](https://docs.cloud.google.com/vertex-ai/docs/general/locations?hl=zh-tw#choosing_your_location)」。

## 在 Vertex AI 中部署模型

您可以使用各種方法，將模型部署至 Vertex AI 中的端點。詳情請參閱「[將模型部署至端點](https://docs.cloud.google.com/vertex-ai/docs/general/deployment?hl=zh-tw)」。

## 從 Model Registry 刪除 BigQuery ML 模型

如要從 Model Registry 刪除 BigQuery ML 模型，請在 BigQuery ML 中刪除該模型。模型會自動從 Model Registry 中移除。

您可以透過多種方式刪除 BigQuery ML 模型。詳情請參閱「[刪除模型](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw)」一文。

如要刪除已在模型登錄服務中註冊，並部署至端點的 BigQuery ML 模型，請先使用模型登錄服務取消部署模型。接著返回 BigQuery ML，刪除模型。如要進一步瞭解如何取消部署模型，請參閱「[刪除端點](https://docs.cloud.google.com/vertex-ai/docs/samples/aiplatform-delete-endpoint-sample?hl=zh-tw)」。

## 限制

* 你無法註冊[遙控器型號](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw#remote_models)。
* 下列模型可在 Model Registry 中註冊，但無法在 Vertex AI 中部署：

  + [匯入的 XGBoost 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-xgboost?hl=zh-tw)
  + [`ARIMA_PLUS` 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)
  + [`ARIMA_PLUS_XREG` 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]