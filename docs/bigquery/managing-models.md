Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理模型

管理 BigQuery ML 模型，有助於整理、保護及發布機器學習資產。您可以複製模型並重新命名，以便在不同環境之間升級模型，或更新命名慣例，而不必重新訓練資料。您也可以使用客戶自行管理的加密金鑰 (CMEK) 保護模型。

## 必要的角色

如要取得讀取及建立 BigQuery 模型所需的權限，請要求管理員授予您專案的 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor) (`roles/bigquery.dataEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備讀取及建立 BigQuery 模型所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能讀取及建立 BigQuery 模型：

* 如要讀取模型中的資訊，請按照下列步驟操作：
  `bigquery.models.getData`
* 建立模型：
  `bigquery.models.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 重新命名模型

您無法變更現有模型的名稱。如您需要變更模型的名稱，請遵循相關步驟[複製模型](#copy-model)。當您在複製操作中指定目的地時，請使用新模型名稱。

## 複製模型

您可透過以下方式，將某個來源資料集的一或多個模型複製至目的地資料集：

* 使用 Google Cloud 控制台。
* 使用 bq 指令列工具的 `bq cp` 指令。
* 直接呼叫 [jobs.insert](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 方法，並設定[複製工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationTableCopy)，或使用用戶端程式庫。

### 複製模型的限制

模型複製工作有下列限制：

* 複製模型時，目的地模型的名稱必須遵循與您[建立模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#model_name)時相同的命名慣例。
* 模型副本須遵守 BigQuery 對複製工作的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)。
* Google Cloud 控制台不支援複製模型。
* 不支援使用單一指令複製多個來源模型。
* 使用 CLI 複製模型時，不支援 `--destination_kms_key` 旗標。

### 複製模型

您可透過以下方式複製模型：

* 使用指令列工具的 `bq cp` 指令
* 呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 方法並設定[複製工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationTableCopy)，或使用用戶端程式庫

如要複製模型：

### 控制台

Google Cloud 控制台不支援複製模型。

### bq

請發出 `bq cp` 指令。選用標記：

* `-f` 或 `--force` 會覆寫目的地資料集中的現有模型，且不會提示您確認。
* 如果目的地資料集中已有模型，`-n` 或 `--no_clobber` 會傳回下列錯誤訊息：`'[PROJECT_ID]:[DATASET].[MODEL]'
  already exists, skipping`。

  如未指定 `-n`，預設行為是提示您選擇是否要取代目的地模型。

**注意：**複製模型時，不支援 `--destination_kms_key` 旗標。

如果來源或目的地資料集位於非預設專案中，請採用下列格式將專案 ID 新增至該資料集名稱：`PROJECT_ID:DATASET`。

提供 `--location` 旗標，並將值設為[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

```
bq --location=LOCATION cp -f -n PROJECT_ID:DATASET.SOURCE_MODEL PROJECT_ID:DATASET.DESTINATION_MODEL
```

更改下列內容：

* LOCATION：位置名稱。`--location` 旗標為選用。舉例來說，如果您在東京區域使用 BigQuery，可以將旗標值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#set_default_values_for_command-line_flags)設定位置的預設值。如需完整位置清單，請參閱「[BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)」。
* PROJECT\_ID：您的專案 ID。
* DATASET：來源或目的地資料集的名稱。
* SOURCE\_MODEL：要複製的模型。
* DESTINATION\_MODEL：目的地資料集中的模型名稱。

範例：

輸入下列指令，將 `mydataset.mymodel` 複製到 `mydataset2`。
這兩個資料集都位於預設專案中，且是在 `US` 多區域位置建立。

```
bq --location=US cp mydataset.mymodel mydataset2.mymodel
```

輸入下列指令，複製 `mydataset.mymodel` 並覆寫同名的目的地模型。來源資料集位於預設專案中。目的地資料集位於 `myotherproject` 中。`-f` 捷徑可用來在無提示的情況下覆寫目的地模型。`mydataset` 和 `myotherdataset` 是在 `US` 多區域位置建立。

```
bq --location=US cp -f mydataset.mymodel myotherproject:myotherdataset.mymodel
```

輸入下列指令，複製 `mydataset.mymodel`。如果目的地資料集包含同名模型，則會傳回錯誤。來源資料集位於預設專案中。目的地資料集位於 `myotherproject` 中。`-n` 捷徑可用來防止覆寫同名模型。這兩個資料集都是在 `US` 多區域位置建立。

```
bq --location=US cp -n mydataset.mymodel myotherproject:myotherdataset.mymodel
```

輸入下列指令，將 `mydataset.mymodel` 複製到 `mydataset2`，並將模型重新命名為 `mymodel2`。這兩個資料集都位於預設專案中。這兩個資料集都是在 `asia-northeast1` 區域建立。

```
bq --location=asia-northeast1 cp mydataset.mymodel mydataset2.mymodel2
```

### API

如要使用 API 複製模型，請呼叫 [`bigquery.jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法，並設定 `copy` 工作。在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定位置。

您必須在工作設定中指定下列值：

```
"copy": {
      "sourceTable": {       // Required
        "projectId": string, // Required
        "datasetId": string, // Required
        "tableId": string    // Required
      },
      "destinationTable": {  // Required
        "projectId": string, // Required
        "datasetId": string, // Required
        "tableId": string    // Required
      },
      "createDisposition": string,  // Optional
      "writeDisposition": string,   // Optional
    },
```

其中：

* `sourceTable`：提供要複製的模型相關資訊。
* `destinationTable`：提供新模型的相關資訊。
* `createDisposition`：指定是否要在模型不存在時建立模型。
* `writeDisposition`：指定是否要覆寫現有模型。

## 加密模型

如要進一步瞭解如何使用 CMEK 加密模型，請參閱「[使用 CMEK 保護 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#cmek-bqml)」。

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要開始使用 BigQuery ML，請參閱「[在 BigQuery ML 中建立機器學習模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model?hl=zh-tw)」。
* 如要進一步瞭解如何使用模型，請參閱：
  + [取得模型中繼資料](https://docs.cloud.google.com/bigquery/docs/getting-model-metadata?hl=zh-tw)
  + [列出模型](https://docs.cloud.google.com/bigquery/docs/listing-models?hl=zh-tw)
  + [更新模型中繼資料](https://docs.cloud.google.com/bigquery/docs/updating-model-metadata?hl=zh-tw)
  + [刪除模型](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw)
  + [使用 Gemini Enterprise Agent Platform 管理模型](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-17 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-17 (世界標準時間)。"],[],[]]