* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用批次 SQL 翻譯器遷移程式碼

**注意：** 如要透過 API 翻譯 SQL 指令碼 (包括新的批次翻譯)，建議使用 [BigQuery Migration API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw)。BigQuery Migration API 的運作方式與批次 SQL 翻譯器非常相似，但不需要安裝或使用用戶端程式碼。

本文說明如何使用 BigQuery 的批次 SQL 翻譯器，將以其他 SQL 方言編寫的指令碼翻譯成 GoogleSQL 查詢。本文適用於熟悉[Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)的使用者。

## 事前準備

提交翻譯工作前，請先完成下列步驟：

1. 確認您具備所有必要權限。
2. 啟用 BigQuery Migration API。
3. 收集包含待翻譯 SQL 指令碼和查詢的來源檔案。
4. 選用。建立中繼資料檔案，提升翻譯準確率。
5. 選用。決定是否需要將來源檔案中的 SQL 物件名稱對應至 BigQuery 中的新名稱。如有需要，請決定要使用哪些名稱對應規則。
6. 決定要使用哪種方法提交翻譯工作。
7. 將來源檔案上傳至 Cloud Storage。

### 所需權限

您必須具備專案的下列權限，才能啟用 BigQuery 移轉服務：

* `resourcemanager.projects.get`
* `serviceusage.services.enable`
* `serviceusage.services.get`

如要存取及使用 BigQuery 遷移服務，您必須具備專案的下列權限：

* `bigquerymigration.workflows.create`
* `bigquerymigration.workflows.get`
* `bigquerymigration.workflows.list`
* `bigquerymigration.workflows.delete`
* `bigquerymigration.subtasks.get`
* `bigquerymigration.subtasks.list`

  或者，您也可以使用下列角色取得相同權限：

  + `bigquerymigration.viewer` - 唯讀存取權。
  + `bigquerymigration.editor` - 讀取/寫入權限。

如要存取輸入和輸出檔案的 Cloud Storage bucket，請按照下列步驟操作：

* 來源 Cloud Storage bucket 上的 `storage.objects.get`。
* 來源 Cloud Storage bucket 上的 `storage.objects.list`。
* 目標 Cloud Storage 值區中的 `storage.objects.create`。

您可以透過下列角色取得上述所有必要的 Cloud Storage 權限：

* `roles/storage.objectAdmin`
* `roles/storage.admin`

### 啟用 BigQuery Migration API

如果您的 Google Cloud CLI 專案是在 2022 年 2 月 15 日前建立，請按照下列步驟啟用 BigQuery Migration API：

1. 前往 Google Cloud 控制台的「BigQuery Migration API」頁面。

   [前往 BigQuery Migration API](https://console.cloud.google.com/apis/api/bigquerymigration.googleapis.com/overview?hl=zh-tw)
2. 按一下「啟用」。

**注意：** 2022 年 2 月 15 日後建立的專案會自動啟用這項 API。

### 收集來源檔案

來源檔案必須是文字檔，其中包含來源方言的有效 SQL。來源檔案也可以包含註解。請盡可能確保 SQL 有效，並使用可用的方法。

### 建立中繼資料檔案

為協助服務產生更準確的翻譯結果，建議您提供中繼資料檔案。不過，這並非強制要求。

您可以使用 `dwh-migration-dumper` 指令列擷取工具產生中繼資料資訊，也可以提供自己的中繼資料檔案。準備好中繼資料檔案後，即可將這些檔案與來源檔案一併放入翻譯來源資料夾。翻譯人員會自動偵測並運用這些檔案翻譯來源檔案，您不需要設定任何額外設定來啟用這項功能。

如要使用 `dwh-migration-dumper` 工具產生中繼資料資訊，請參閱「[產生翻譯的中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)」。

如要提供自己的中繼資料，請將來源系統中 SQL 物件的資料定義語言 (DDL) 陳述式收集到個別文字檔中。

### 決定如何提交翻譯工作

提交批次翻譯作業有三種方式：

* **批次翻譯用戶端**：在設定檔中變更設定來設定工作，並使用指令列提交工作。這種方法不需要手動將來源檔案上傳至 Cloud Storage。在翻譯工作處理期間，用戶端仍會使用 Cloud Storage 儲存檔案。

  舊版批次翻譯用戶端是開放原始碼的 Python 用戶端，可讓您翻譯本機上的來源檔案，並將翻譯後的檔案輸出至本機目錄。您可以在用戶端的設定檔中變更幾項設定，設定用戶端以供基本用途。您也可以選擇設定用戶端，處理更複雜的工作，例如巨集取代，以及翻譯輸入和輸出內容的前後處理。詳情請參閱批次翻譯用戶端[readme](https://github.com/google/dwh-migration-tools/blob/main/client/README.md)。
* **Google Cloud 控制台**：使用使用者介面設定及提交工作。這個方法需要將來源檔案上傳至 Cloud Storage。

### 建立設定 YAML 檔案

您可以視需要建立及使用[設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw)，自訂批次翻譯作業。這些檔案可用於以各種方式轉換翻譯輸出內容。舉例來說，您可以[建立設定 YAML 檔案，在翻譯期間變更 SQL 物件的大小寫](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#change_object-name_case)。

如要使用 Google Cloud 控制台或 BigQuery Migration API 執行批次翻譯工作，可以[將設定 YAML 檔案上傳至含有來源檔案的 Cloud Storage bucket](#upload-files)。

如要使用批次翻譯用戶端，請將設定 YAML 檔案放在本機翻譯輸入資料夾中。

### 將輸入檔案上傳至 Cloud Storage

如要使用 Google Cloud 控制台或 BigQuery Migration API 執行翻譯工作，請將包含要翻譯的查詢和指令碼的來源檔案上傳至 Cloud Storage。您也可以將[任何中繼資料檔案](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)或[設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw)上傳至含有來源檔案的相同 Cloud Storage 值區和目錄。如要進一步瞭解如何建立值區，以及將檔案上傳至 Cloud Storage，請參閱「[建立值區](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

## 支援的 SQL 方言

批次 SQL 翻譯器是 BigQuery 遷移服務的一部分。批次 SQL 翻譯器可將下列 SQL 方言翻譯為 GoogleSQL：

* Amazon Redshift SQL
* Apache HiveQL 和 Beeline CLI
* IBM Netezza SQL 和 NZPLSQL
* Teradata 和 Teradata Vantage：
  + SQL
  + Basic Teradata Query (BTEQ)
  + Teradata Parallel Transport (TPT)

此外，[預覽版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)也支援翻譯下列 SQL 方言：

* Apache Impala SQL
* Apache Spark SQL
* Azure Synapse T-SQL
* GoogleSQL (BigQuery)
* Greenplum SQL
* IBM DB2 SQL
* MySQL SQL
* Oracle SQL、PL/SQL、Exadata
* PostgreSQL SQL
* Trino 或 PrestoSQL
* Snowflake SQL
* SQL Server T-SQL
* SQLite
* Vertica SQL

**重要事項：** 我們會盡力完成翻譯作業，翻譯成功率可能因來源指令碼中 SQL 陳述式的獨特性和複雜度而異。你可能需要手動翻譯部分指令碼。
使用[Google Cloud 控制台輸出](#output)中的「動作」分頁，診斷及修正翻譯問題。

### 使用輔助 UDF 處理不支援的 SQL 函式

將來源方言的 SQL 轉換為 BigQuery 時，部分函式可能沒有直接對應的函式。為解決這個問題，BigQuery 遷移服務 (和更廣泛的 BigQuery 社群) 提供輔助使用者定義函式 (UDF)，可複製這些不支援的來源方言函式行為。

這些 UDF 通常位於 `bqutil` 公開資料集中，因此翻譯後的查詢一開始可以採用 `bqutil.<dataset>.<function>()` 格式參照這些 UDF。例如：`bqutil.fn.cw_count()`。

#### 正式環境的重要注意事項：

雖然 `bqutil` 可方便存取這些輔助 UDF，進行初始轉換和測試，但基於下列原因，不建議直接依賴 `bqutil` 處理實際工作環境工作負載：

1. 版本管控：`bqutil` 專案會代管這些 UDF 的最新版本，因此定義可能會隨時間變更。如果 UDF 的邏輯更新，直接依賴 `bqutil` 可能會導致正式版查詢發生非預期行為或破壞性變更。
2. 依附元件隔離：將 UDF 部署至自己的專案，可避免外部變更影響正式環境。
3. 自訂：您可能需要修改或最佳化這些 UDF，進一步滿足特定商業邏輯或效能需求。只有在這些資源位於您的專案中時，才能執行這項操作。
4. 安全性和控管：貴機構的安全政策可能會限制直接存取公開資料集 (例如 `bqutil`)，以處理正式環境資料。將 UDF 複製到受控環境，符合這類政策規定。

#### 將輔助 UDF 部署至專案：

如要穩定可靠地在實際工作環境中使用，請將這些輔助 UDF 部署到自己的專案和資料集。您可以全面掌控這些應用程式的版本、自訂項目和存取權。
如需部署這些 UDF 的詳細操作說明，請參閱 [GitHub 上的 UDF 部署指南](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/udfs#deploying-the-udfs)。本指南提供必要的指令碼和步驟，協助您將 UDF 複製到環境中。

## 位置

批次 SQL 翻譯器可在下列處理位置使用：

|  | **地區說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- | --- |
| **亞太地區** | | | |
|  | 曼谷 | `asia-southeast3` |  |
|  | 德里 | `asia-south2` |  |
|  | 香港 | `asia-east2` |  |
|  | 雅加達 | `asia-southeast2` |  |
|  | 墨爾本 | `australia-southeast2` |  |
|  | 孟買 | `asia-south1` |  |
|  | 大阪 | `asia-northeast2` |  |
|  | 首爾 | `asia-northeast3` |  |
|  | 新加坡 | `asia-southeast1` |  |
|  | 雪梨 | `australia-southeast1` |  |
|  | 台灣 | `asia-east1` |  |
|  | 東京 | `asia-northeast1` |  |
| **歐洲** | | | |
|  | 比利時 | `europe-west1` |  |
|  | 柏林 | `europe-west10` |  |
|  | 歐洲 (多區域) | `eu` |
|  | 芬蘭 | `europe-north1` |  |
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` |  |
|  | 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 米蘭 | `europe-west8` |  |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 巴黎 | `europe-west9` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 斯德哥爾摩 | `europe-north2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 杜林 | `europe-west12` |  |
|  | 華沙 | `europe-central2` |  |
|  | 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **美洲** | | | |
|  | 俄亥俄州哥倫布 | `us-east5` |  |
|  | 達拉斯 | `us-south1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 拉斯維加斯 | `us-west4` |  |
|  | 洛杉磯 | `us-west2` |  |
|  | 墨西哥 | `northamerica-south1` |  |
|  | 北維吉尼亞州 | `us-east4` |  |
|  | 奧勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 魁北克 | `northamerica-northeast1` | [低 CO2](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) 區域 |
|  | 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 鹽湖城 | `us-west3` |  |
|  | 聖地亞哥 | `southamerica-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 南卡羅來納州 | `us-east1` |  |
|  | 多倫多 | `northamerica-northeast2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 美國 (多區域) | `us` |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` |  |
| **MiddleEast** | | | |
|  | 達曼 | `me-central2` |  |
|  | 杜哈 | `me-central1` |  |
|  | 以色列 | `me-west1` |  |

## 提交翻譯工作

請按照下列步驟開始翻譯工作、查看進度，以及查看結果。

### 控制台

這些步驟假設您已將來源檔案上傳至 Cloud Storage bucket。

1. 前往 Google Cloud 控制台的「SQL Translation」頁面。

   [前往 SQL 翻譯](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在「SQL translation」(SQL 翻譯) 面板中，按一下「Start translation」(開始翻譯)。
3. 在「Translation configuration」(翻譯設定) 中輸入下列資訊：

   1. 在「Display name」(顯示名稱) 中，輸入翻譯工作的名稱。名稱可包含英文字母、數字或底線。
   2. 在「Processing location」(處理位置) 中，選取要執行翻譯工作的地點。舉例來說，如果您位於歐洲，且不希望資料跨越任何位置限制範圍，請選取「`eu`」區域。如果選擇與來源檔案 bucket 相同的位置，翻譯工作成效最佳。
   3. 在「來源方言」中，選取要翻譯的 SQL 方言。
   4. 在「目標方言」部分，選取「GoogleSQL」。
4. 點選「下一步」。
5. 在「檔案位置詳細資料」部分，指定要用於翻譯輸入和輸出的 Cloud Storage 路徑。您可以輸入路徑 (格式為
   `bucket_name/folder_name/`)，也可以使用「瀏覽」選項前往資料夾。

   1. 在「輸出目錄位置」部分，指定翻譯檔案的目標 Cloud Storage 資料夾路徑。這是所有翻譯輸出內容的根目錄。
   2. 選擇一或多個**輸入目錄位置**，其中包含要翻譯的 SQL 檔案路徑。
   3. 如有需要，每個輸入目錄都可以選擇在根輸出目錄下方提供**輸出子目錄名稱**。
6. 點選「下一步」。
7. 選取要自訂中繼資料的任何選用設定，以及任何其他翻譯輸出內容。
8. 您可以建立設定 YAML 檔案，並將這些檔案放在輸入 Cloud Storage 值區中，進一步自訂翻譯行為。這些檔案可用於設定重新命名物件、啟用最佳化功能、透過 Gemini 提升翻譯品質等。如要進一步瞭解設定 YAML 檔案，請參閱「[建立設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw)」。
9. 按一下「建立」即可開始翻譯工作。

翻譯工作建立完成後，您可以在翻譯工作清單中查看狀態。

### 批次翻譯用戶端

**注意：** 建議使用 [BigQuery Migration API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw) 進行新的翻譯，而不要使用批次翻譯用戶端。

1. [安裝批次翻譯用戶端和 Google Cloud CLI](https://github.com/google/dwh-migration-tools/blob/main/client/README.md#installation)。
2. [產生 gcloud CLI 憑證檔案](https://github.com/google/dwh-migration-tools/blob/main/client/README.md#optional-gcloud-login-and-authentication)。
3. 在批次翻譯用戶端安裝目錄中，使用您選擇的文字編輯器開啟 `config.yaml` 檔案，並修改下列設定：

   * `project_number`：輸入要用於批次翻譯工作的專案編號。您可以在專案的[Google Cloud 控制台歡迎頁面](https://console.cloud.google.com/welcome?hl=zh-tw)上，找到「專案資訊」窗格。
   * `gcs_bucket`：輸入 Cloud Storage bucket 的名稱，批次翻譯用戶端會在翻譯作業處理期間，使用這個 bucket 儲存檔案。
   * `input_directory`：輸入含有來源檔案和任何中繼資料檔案的目錄絕對或相對路徑。
   * `output_directory`：輸入翻譯檔案目標目錄的絕對或相對路徑。
4. 儲存變更並關閉 `config.yaml` 檔案。
5. 將來源和中繼資料檔案放在輸入目錄中。
6. 使用下列指令執行批次翻譯用戶端：

   ```
   bin/dwh-migration-client
   ```
7. 建立翻譯工作。

   * 以下範例顯示建立翻譯工作的指令。指令會執行工作流程，並在工作流程成功時顯示輸出內容。

     ```
     gcloud bq migration-workflows create --location=us --config-file=CONFIG_FILE_NAME.json
     ```
   * 以下範例顯示使用 `--async` 旗標建立及執行工作流程的指令。這個指令會建立及執行工作流程，並立即傳回工作流程的連結。

     ```
     gcloud bq migration-workflows create --location=LOCATION  --config-file=CONFIG_FILE_NAME.json --async
     ```
   * 以下範例顯示列出翻譯工作的指令：

     ```
     gcloud bq migration-workflows list --location=LOCATION
     ```

   更改下列內容：

   * `LOCATION`：執行這項翻譯工作的 Google Cloud 專案位置。
   * `CONFIG_FILE_NAME`：`config.yaml` 檔案的名稱。
     建立翻譯工作後，您可以在 Google Cloud 控制台的翻譯工作清單中查看工作狀態。
8. 選用。翻譯工作完成後，請刪除工作在指定 Cloud Storage bucket 中建立的檔案，以免產生儲存空間費用。

### BigQuery CLI

如要使用 bq 指令列工具執行批次 SQL 轉譯器，請按照下列步驟操作：

1. 以 YAML 或 JSON 格式建立翻譯設定檔。您必須在這個檔案中定義來源檔案的路徑、輸出目的地，以及翻譯的來源和目標方言。

   以下範例顯示從 Teradata 翻譯為 BigQuery 的翻譯設定 YAML 檔案：

   ```
   tasks:
   translation_task:
     type: Teradata2BigQuery_Translation
     translationDetails:
       sourceTargetMapping:
       - sourceSpec:
           baseUri: gs://bq-translations/input
         targetSpec:
           relativePath: output
       targetBaseUri: gs://bq-translations
       targetTypes:
       - sql
       sourceEnvironment:
         defaultDatabase: default_db
         schemaSearchPath:
         - foo
   ```

   以下範例顯示從 Teradata 翻譯為 BigQuery 的翻譯設定 JSON 檔案：

   ```
   {
   "tasks": {
     "translation_task": {
       "type": "Teradata2BigQuery_Translation",
       "translationDetails": {
         "sourceTargetMapping": [
           {
             "sourceSpec": {
               "literal": {
                 "literalString": "sel 1",
                 "relativePath": "my_input_1"
               },
               "encoding": "UTF-8"
             }
           },
           {
             "sourceSpec": {
               "literal": {
                 "literalString": "sel 2",
                 "relativePath": "my_input_2"
               },
               "encoding": "UTF-8"
             }
           }
         ],
         "targetReturnLiterals": [
           "sql/my_input_1",
           "sql/my_input_2"
         ]
       }
     }
   }
   }
   ```
2. 建立翻譯設定後，請執行下列指令來執行翻譯工作。

   ```
   bq mk --migration_workflow --location=LOCATION --config_file=CONFIG_FILE_NAME.json
   ```

   更改下列內容：

   * `LOCATION`：執行這項翻譯工作的 Google Cloud 專案位置。
   * `CONFIG_FILE_NAME`：`config.yaml` 檔案的名稱。

* 如要查看特定翻譯工作的詳細資料，請執行下列指令：

  ```
  bq show --migration_workflow projects/PROJECT_ID/ locations/us/workflows/WORKFLOW_ID
  ```

  更改下列內容：

  + `PROJECT_ID`：執行這項翻譯工作的 Google Cloud 專案 ID。
  + `WORKFLOW_ID`：翻譯工作 ID。
* 如要查看特定翻譯作業的結果，請執行下列指令：

  ```
  gcloud bq migration-workflows describe projects/PROJECT_ID    /locations/us/workflows/WORKFLOW_ID
  ```
* 如要從清單中移除翻譯工作，請執行下列指令：

  ```
  bq rm --migration_workflow projects/PROJECT_ID/locations/us/workflows/WORKFLOW_ID
  ```
* 如要列出所有翻譯工作，請執行下列指令：

  ```
  bq ls --migration_workflow --location=LOCATION
  ```

## 探索翻譯輸出內容

執行翻譯工作後，您可以在 Google Cloud 控制台中查看工作相關資訊。如果您使用 Google Cloud 控制台執行工作，可以在指定的目的地 Cloud Storage 值區中查看工作結果。如果您使用批次翻譯用戶端執行工作，可以在指定的輸出目錄中查看工作結果。批次 SQL 翻譯器會將下列檔案輸出至指定目的地：

* 翻譯後的檔案。
* CSV 格式的翻譯摘要報告。
* JSON 格式的已取用輸出內容名稱對應。
* AI 建議的檔案。

### Google Cloud 控制台輸出內容

如要查看翻譯工作詳細資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」頁面。

   [前往 SQL 翻譯](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中，找到要查看翻譯詳細資料的工作。然後按一下翻譯工作名稱。
   您可以查看桑基圖，瞭解作業的整體品質、輸入的程式碼行數 (不含空白行和註解)，以及翻譯過程中發生的問題清單。您應優先修正左側的問題，早期階段的問題可能會導致後續階段出現其他問題。
3. 將指標懸停在錯誤或警告列上，然後查看建議，判斷偵錯翻譯工作的後續步驟。
4. 選取「記錄摘要」分頁標籤，即可查看翻譯問題摘要，包括問題類別、建議動作，以及各個問題的發生頻率。你可以點選桑基圖的長條，篩選問題。您也可以選取問題類別，查看與該類別相關的記錄訊息。
5. 選取「記錄訊息」分頁，即可查看各項翻譯問題的詳細資訊，包括問題類別、具體問題訊息，以及發生問題的檔案連結。您可以點選桑基圖的長條，篩選問題。您可以在「Log Message」(記錄訊息) 分頁中選取問題，開啟「Code」(程式碼) 分頁，查看輸入和輸出檔案 (如有)。
6. 按一下「工作詳細資料」分頁標籤，即可查看翻譯工作設定詳細資料。

### 摘要報告

摘要報告是 CSV 檔案，內含翻譯作業期間遇到的所有警告和錯誤訊息表格。

如要在 Google Cloud 控制台中查看摘要檔案，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」頁面。

   [前往 SQL 翻譯](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中找出感興趣的工作，然後按一下工作名稱，或依序點選「更多選項」**>「顯示詳細資料」**。
3. 在「工作詳細資料」分頁的「翻譯報告」部分，按一下「translation\_report.csv」。
4. 在「物件詳細資料」頁面中，按一下「已通過驗證的網址」列中的值，即可在瀏覽器中查看檔案。

下表說明摘要檔案的欄位：

| **欄** | **說明** |
| --- | --- |
| 時間戳記 | 問題發生時的時間戳記。 |
| FilePath | 與問題相關聯的來源檔案路徑。 |
| FileName | 與問題相關聯的來源檔案名稱。 |
| ScriptLine | 發生問題的行號。 |
| ScriptColumn | 發生問題的欄號。 |
| TranspilerComponent | 發生警告或錯誤的翻譯引擎內部元件。這個資料欄可能為空。 |
| 環境 | 與警告或錯誤相關的翻譯方言環境。這個資料欄可能為空。 |
| ObjectName | 來源檔案中與警告或錯誤相關聯的 SQL 物件。這個資料欄可能為空。 |
| 嚴重性 | 問題的嚴重程度，可能是警告或錯誤。 |
| 類別 | 翻譯問題類別。 |
| SourceType | 這個問題的來源。這個資料欄的值可以是 `SQL` (表示輸入 SQL 檔案有問題)，也可以是 `METADATA` (表示中繼資料套件有問題)。 |
| 訊息 | 翻譯問題警告或錯誤訊息。 |
| ScriptContext | 與問題相關聯的來源檔案中的 SQL 程式碼片段。 |
| 動作 | 建議您採取哪些行動來解決問題。 |

### 「程式碼」分頁

您可以在「程式碼」分頁中，查看特定翻譯工作的輸入和輸出檔案詳細資訊。在「程式碼」分頁中，您可以檢查翻譯工作使用的檔案、並排比較輸入檔案和翻譯內容，找出任何不準確之處，以及查看工作中特定檔案的記錄摘要和訊息。

如要存取程式碼分頁，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」頁面。

   [前往 SQL 翻譯](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中找出感興趣的工作，然後按一下工作名稱，或依序點選「更多選項」**>「顯示詳細資料」**。
3. 選取「程式碼」分頁標籤。「程式碼」分頁包含下列面板：

   * 檔案總管：包含用於翻譯的所有 SQL 檔案。按一下檔案即可查看翻譯輸入和輸出內容，以及翻譯時發生的任何問題。
   * **以 Gemini 補強的輸入內容**：由翻譯引擎翻譯的輸入 SQL。如果您已[在 Gemini 設定中](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#ai_yaml_guidelines)指定來源 SQL 的 Gemini 自訂規則，翻譯工具會先轉換原始輸入內容，然後翻譯 Gemini 強化輸入內容。如要查看原始輸入內容，請按一下「查看原始輸入內容」。
   * **翻譯輸出內容**：翻譯結果。如果您已在 [Gemini 設定](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#ai_yaml_guidelines)中指定目標 SQL 的 Gemini 自訂規則，系統會將轉換套用至轉譯結果，做為 Gemini 強化輸出內容。如果系統提供 Gemini 強化輸出內容，你可以點選「Gemini 建議」按鈕，查看這類內容。
4. 選用：如要在 [BigQuery 互動式 SQL 翻譯器](#debug-interactive-translator)中查看輸入檔案和輸出檔案，請按一下「編輯」。您可以編輯檔案，然後將輸出檔案儲存回 Cloud Storage。

**注意：** 您可以在[結果頁面](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw#explore_the_translation_output)查看整體翻譯工作的記錄摘要和訊息。

### 「設定」分頁

您可以在「設定」分頁中新增、重新命名、查看或編輯設定 YAML 檔案。「結構定義探索工具」會顯示支援的設定類型說明文件，協助您編寫設定 YAML 檔案。編輯設定 YAML 檔案後，您可以重新執行工作，使用新的設定。

如要存取設定分頁，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」頁面。

   [前往 SQL 翻譯](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中找出感興趣的工作，然後按一下工作名稱，或依序點選「更多選項」**>「顯示詳細資料」**。
3. 在「Translation details」(翻譯詳細資料) 視窗中，按一下「Configuration」(設定) 分頁標籤。

如要新增設定檔，請按照下列步驟操作：

1. 依序點按 more\_vert「更多選項」>「建立設定 YAML 檔案」。
2. 系統會顯示面板，供您選擇新設定 YAML 檔案的類型、位置和名稱。
3. 點選「建立」。

如要編輯現有的設定檔：

1. 按一下設定 YAML 檔案。
2. 編輯檔案，然後按一下「儲存」。
3. 按一下「重新執行」，使用編輯過的設定 YAML 檔案執行新的翻譯工作。

如要重新命名現有的設定檔，請依序點選「more\_vert」more\_vert「更多選項」>「重新命名」。

### 使用的輸出名稱對應檔案

這個 JSON 檔案包含翻譯工作使用的輸出名稱對應規則。由於名稱對應規則發生衝突，或翻譯期間識別出的 SQL 物件缺少名稱對應規則，這個檔案中的規則可能與您為翻譯工作指定的[輸出名稱對應](https://docs.cloud.google.com/bigquery/docs/output-name-mapping?hl=zh-tw)規則不同。請檢查這個檔案，判斷名稱對應規則是否需要修正。如有，請建立新的輸出名稱對應規則，解決您發現的任何問題，然後執行新的翻譯工作。

### 翻譯後的檔案

系統會為每個來源檔案，在目的地路徑中產生對應的輸出檔案。輸出檔案包含翻譯後的查詢。

**重要事項：** 我們會盡力完成翻譯作業，盡可能驗證翻譯後的查詢。

## 使用互動式 SQL 翻譯器，偵錯批次翻譯的 SQL 查詢

您可以使用 BigQuery 互動式 SQL 翻譯器，透過與來源資料庫相同的中繼資料或物件對應資訊，檢查或偵錯 SQL 查詢。完成批次翻譯作業後，BigQuery 會產生翻譯設定 ID，其中包含作業的中繼資料、物件對應或結構定義搜尋路徑等資訊 (視查詢而定)。您可以使用互動式 SQL 翻譯器搭配批次翻譯設定 ID，執行指定設定的 SQL 查詢。

如要使用批次翻譯設定 ID 啟動互動式 SQL 翻譯，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」頁面。

   [前往 SQL 翻譯](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中，找出您感興趣的工作，然後依序點按 more\_vert「更多選項」**>「開啟互動式翻譯」**。

   BigQuery 互動式 SQL 翻譯器現在會開啟，並顯示對應的批次翻譯設定 ID。如要查看互動式翻譯的翻譯設定 ID，請在互動式 SQL 翻譯器中依序點選「更多」>「翻譯設定」。

如要在互動式 SQL 翻譯器中偵錯批次翻譯檔案，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」頁面。

   [前往 SQL 翻譯](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中找出感興趣的工作，然後按一下工作名稱，或依序點選「更多選項」**>**「顯示詳細資料」。
3. 在「翻譯詳細資料」視窗中，按一下「程式碼」分頁標籤。
4. 在檔案總管中，按一下檔案名稱即可開啟檔案。
5. 按一下輸出檔案名稱旁的「編輯」，在互動式 SQL 轉譯器 ([預覽](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)) 中開啟檔案。

   您會看到輸入和輸出檔案已填入互動式 SQL 翻譯器，該翻譯器現在使用對應的批次翻譯設定 ID。
6. 如要將編輯後的輸出檔案儲存回 Cloud Storage，請在互動式 SQL 轉譯器中依序點選「儲存」**> 儲存至 GCS**。

## 限制

翻譯工具無法翻譯 SQL 以外語言的使用者定義函式 (UDF)，因為無法剖析這些函式，判斷輸入和輸出資料類型。這會導致參照這些 UDF 的 SQL 陳述式翻譯不準確。為確保在轉換期間正確參照非 SQL UDF，請使用有效的 SQL 建立具有相同簽章的預留位置 UDF。

舉例來說，假設您有以 C 語言編寫的 UDF，可計算兩個整數的總和。為確保參照這個 UDF 的 SQL 陳述式能正確轉換，請建立與 C UDF 具有相同簽章的預留位置 SQL UDF，如下列範例所示：

```
CREATE FUNCTION Test.MySum (a INT, b INT)
  RETURNS INT
  LANGUAGE SQL
  RETURN a + b;
```

將這個預留位置 UDF 儲存為文字檔，並將該檔案納入翻譯工作的來源檔案。這有助於翻譯人員瞭解 UDF 定義，並識別預期的輸入和輸出資料類型。

## 配額與限制

* 適用 [BigQuery Migration API 配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#migration-api-limits)。
* 每個專案最多只能有 10 個有效翻譯工作。
* 雖然來源和中繼資料檔案總數沒有硬性限制，但建議檔案數不要超過 1000 個，以提升效能。

## 排解翻譯錯誤

### `RelationNotFound` 或 `AttributeNotFound` 翻譯問題

使用[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw#submit_a_translation_job)翻譯查詢後，您可能會遇到翻譯失敗的情況，並收到 `RelationNotFound` 或 `AttributeNotFound` 錯誤。

如要找出翻譯失敗的內容，請前往「翻譯詳細資料」頁面，然後開啟「記錄訊息」分頁。

翻譯服務最適合搭配中繼資料 DDL 使用。如果找不到 SQL 物件定義，翻譯引擎就會提出 `RelationNotFound` 或 `AttributeNotFound` 問題。建議使用中繼資料擷取工具產生中繼資料套件，確保所有物件定義都存在。建議先新增中繼資料，解決大多數翻譯錯誤，因為中繼資料通常能修正許多其他錯誤，這些錯誤間接起因於缺少中繼資料。

詳情請參閱「[產生翻譯和評估用的中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)」。

#### 使用 Gemini 修正翻譯問題

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

如要修正 `RelationNotFound` 或 `AttributeNotFound` 錯誤導致的翻譯工作失敗問題，你也可以按照下列步驟使用 Gemini 嘗試解決這些問題。

1. 前往「Translation details」(翻譯詳細資料) 頁面，然後開啟「Log Messages」(記錄訊息) 分頁。
2. 在「類別」欄中，按一下含有 `RelationNotFound` 或 `AttributeNotFound` 訊息的查詢。
3. 按一下錯誤訊息，即可前往程式碼分頁中含有錯誤的檔案和行。
4. 在「動作」欄中，按一下「建議修正」。
5. 選取下列其中一個選項：「套用」或「套用並重新執行」：

   * 按一下「套用」，將產生的結構定義檔案從輸出目錄複製到輸入目錄。
   * 按一下「Apply and rerun」，將產生的結構定義檔案從輸出目錄複製到輸入目錄，並開啟重新執行視窗。

## 定價

批次 SQL 翻譯器為免費工具，使用者無須付費。不過，儲存輸入和輸出檔案所用的儲存空間仍須支付一般費用。詳情請參閱「[儲存空間價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

## 後續步驟

進一步瞭解資料倉儲遷移作業的下列步驟：

* [遷移作業總覽](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw)
* [遷移評估](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)
* [結構定義與資料移轉總覽](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw)
* [資料管道](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw)
* [互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)
* [資安與資管](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)
* [資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator#data-validation-tool)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]