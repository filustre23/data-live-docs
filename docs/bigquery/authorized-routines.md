Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 獲得授權的處理常式

授權常式可讓您與特定使用者或群組分享查詢結果，而不授予他們產生結果的基礎資料表存取權。舉例來說，授權常式可以計算資料的匯總值，或查閱資料表值並用於計算。

在預設情況下，使用者必須有權讀取資料表中的資料，才能叫用常式。或者，您也可以*授權*處理常式存取包含參照資料表的資料集。即使呼叫處理常式的使用者無法直接查詢資料表，獲授權的處理常式仍可查詢資料集中的資料表。

你可以授權下列類型的日常安排：

* [資料表函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)
* [使用者定義的函式 (UDF)](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)
* [預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)

**注意：** 授權為常式的預存程序具有 DDL 和 DML 存取權。
這些程序可以建立、修改及刪除資料庫物件。有權存取授權預存程序的主體可以略過 Identity and Access Management (IAM) 權限，並執行通常會遭到拒絕的動作。請只將授權的預存程序存取權授予您信任的主體，讓他們完整執行程序。

## 授權處理常式

如要授權常式，請使用 Google Cloud 控制台、bq 指令列工具或 REST API：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後選取資料集。
4. 在詳細資料窗格中，依序點選「共用」**>「授權常式」**。
5. 在「Authorized routines」(授權的處理常式) 頁面的「Authorize routine」(授權處理常式) 部分，選取要授權的處理常式所屬的「Project」(專案)、「Dataset」(資料集) 和「Routine」(處理常式)。
6. 按一下「新增授權」。

### bq

1. 使用 `bq show` 指令，取得您要讓常式存取的資料集 JSON 表示法。指令輸出內容是 [`Dataset`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw#Dataset) 資源的 JSON 表示法。將結果儲存至本機檔案。

   ```
   bq show --format=prettyjson TARGET_DATASET > dataset.json
   ```

   將 `TARGET_DATASET` 替換為常式可存取的資料集名稱。
2. 編輯檔案，將下列 JSON 物件新增至 `Dataset` 資源中的 `access` 陣列：

   ```
   {
    "routine": {
      "datasetId": "DATASET_NAME",
      "projectId": "PROJECT_ID",
      "routineId": "ROUTINE_NAME"
    }
   }
   ```

   更改下列內容：

   * `DATASET_NAME`：包含常式的資料集名稱。
   * `PROJECT_ID`：包含常式的專案的專案 ID。
   * `ROUTINE_NAME`：日常安排的名稱。
3. 選用：如要授權預存程序，請附加 IAM 角色。這個角色會根據權限，限制對授權程序的存取權。如要這麼做，請在 JSON 物件中加入 `"role"`：

   ```
   {
    "role": "ROLE_NAME",
    "routine": {
      "datasetId": "DATASET_NAME",
      "projectId": "PROJECT_ID",
      "routineId": "ROUTINE_NAME"
    }
   }
   ```

   將 `ROLE_NAME` 替換為要附加的角色名稱。您可以將下列角色附加至預存程序：

   * [BigQuery 常式中繼資料檢視器](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.routineMetadataViewer) (`roles/bigquery.routineMetadataViewer`)
   * [BigQuery 常式資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.routineDataViewer) (`roles/bigquery.routineDataViewer`)
   * [BigQuery 常式資料編輯者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.routineDataEditor) (`roles/bigquery.routineDataEditor`)
   * [BigQuery Routine Admin](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.routineAdmin) (`roles/bigquery.routineAdmin`)**注意：** 您只能將這些角色附加至預存程序。其他類型的日常安排不支援角色。
4. 使用 `bq update` 指令更新資料集：

   ```
   bq update --source dataset.json TARGET_DATASET
   ```

### API

1. 呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法，擷取要讓處理常式存取的資料集。回應內容包含 [`Dataset`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw#Dataset) 資源的表示法。
2. 在 `Dataset` 資源的 `access` 陣列中新增下列 JSON 物件：

   ```
   {
    "routine": {
      "datasetId": "DATASET_NAME",
      "projectId": "PROJECT_ID",
      "routineId": "ROUTINE_NAME"
    }
   }
   ```

   更改下列內容：

   * `DATASET_NAME`：含有 UDF 的資料集名稱。
   * `PROJECT_ID`：含有 UDF 的專案 ID。
   * `ROUTINE_NAME`：日常安排的名稱。
3. 選用：如要授權已儲存程序，請附加 IAM 角色。這個角色會根據權限限制對授權程序的存取權。如要這麼做，請將 `"role"` 新增至 JSON 物件：

   ```
   {
    "role": "ROLE_NAME",
    "routine": {
      "datasetId": "DATASET_NAME",
      "projectId": "PROJECT_ID",
      "routineId": "ROUTINE_NAME"
    }
   }
   ```

   將 `ROLE_NAME` 替換為要附加的角色名稱。您可以將下列角色附加至預存程序：

   * [BigQuery 常式中繼資料檢視器](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.routineMetadataViewer) (`roles/bigquery.routineMetadataViewer`)
   * [BigQuery 常式資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.routineDataViewer) (`roles/bigquery.routineDataViewer`)
   * [BigQuery 常式資料編輯者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.routineDataEditor) (`roles/bigquery.routineDataEditor`)
   * [BigQuery Routine Admin](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.routineAdmin) (`roles/bigquery.routineAdmin`)**注意：** 您只能將這些角色附加至預存程序。其他類型的日常安排不支援角色。
4. 使用修改後的 `Dataset` 表示法呼叫 [`dataset.update`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/update?hl=zh-tw) 方法。

**注意：** 如果透過執行 `CREATE OR REPLACE` 陳述式 ([`CREATE OR REPLACE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_function_statement)、[`CREATE OR REPLACE PROCEDURE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_procedure)、[`CREATE OR REPLACE TABLE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_function_statement)) 或呼叫 [`routines.update`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/routines/update?hl=zh-tw) 方法修改常式，則必須重新授權常式。

## 配額與限制

獲得授權的處理常式會受到資料集限制。詳情請參閱「[資料集限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#dataset_limits)」。

更新處理常式後，現有授權處理常式的授權就會過期。BigQuery 會在 24 小時內自動移除過時的授權常式授權項目。如要立即更新項目，請先從「目前已授權的常式」清單中手動刪除項目，然後重新授權。

## 獲得授權的處理常式範例

以下是建立及使用授權 UDF 的端對端範例。

1. 建立名為 `private_dataset` 和 `public_dataset` 的兩個資料集。如要進一步瞭解如何建立資料集，請參閱「[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#create-dataset)」。
2. 執行下列陳述式，在 `private_dataset` 中建立名為 `private_table` 的資料表：

   ```
   CREATE OR REPLACE TABLE private_dataset.private_table
   AS SELECT key FROM UNNEST(['key1', 'key1','key2','key3']) key;
   ```
3. 執行下列陳述式，在 `public_dataset` 中建立名為 `count_key` 的 UDF。UDF 包含 `private_table` 的 `SELECT` 陳述式。

   ```
   CREATE OR REPLACE FUNCTION public_dataset.count_key(input_key STRING)
   RETURNS INT64
   AS
   ((SELECT COUNT(1) FROM private_dataset.private_table t WHERE t.key = input_key));
   ```
4. 在`public_dataset`資料集上，將 `bigquery.dataViewer` 角色授予使用者。這個角色包含 `bigquery.routines.get` 權限，可讓使用者呼叫常式。如要瞭解如何指派資料集的存取權控管，請參閱[控管資料集存取權](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-tw)。

   **注意：** 建議您建立具有最低權限的自訂角色，而非使用內建角色。詳情請參閱[建立及管理自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。
5. 此時，使用者有權呼叫 `count_key` 常式，但無法存取 `private_dataset` 中的資料表。如果使用者嘗試呼叫常式，會收到類似以下的錯誤訊息：

   ```
   Access Denied: Table myproject:private_dataset.private_table: User does
   not have permission to query table myproject:private_dataset.private_table.
   ```
6. 使用 bq 指令列工具，執行 `show` 指令，如下所示：

   ```
   bq show --format=prettyjson private_dataset > dataset.json
   ```

   輸出內容會儲存至名為 `dataset.json` 的本機檔案。
7. 編輯 `dataset.json`，將下列 JSON 物件新增至 `access` 陣列：

   ```
   {
    "routine": {
      "datasetId": "public_dataset",
      "projectId": "PROJECT_ID",
      "routineId": "count_key"
    }
   }
   ```

   將 `PROJECT_ID` 替換為 `public_dataset` 的專案 ID。
8. 使用 bq 指令列工具，執行 `update` 指令，如下所示：

   ```
   bq update --source dataset.json private_dataset
   ```
9. 如要確認 UDF 是否有權存取 `private_dataset`，使用者可以執行下列查詢：

   ```
   SELECT public_dataset.count_key('key1');
   ```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]