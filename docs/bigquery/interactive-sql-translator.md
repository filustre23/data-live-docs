* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用互動式 SQL 翻譯器翻譯查詢

本文說明如何使用 BigQuery 互動式 SQL 翻譯器，將查詢從不同的 SQL 方言翻譯成 GoogleSQL 查詢。互動式 SQL 翻譯器能讓您用更少的時間和心力，將工作負載遷移至 BigQuery。本文適用於熟悉[Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)的使用者。

您可以使用[翻譯規則功能](#customize)，自訂互動式 SQL 翻譯器翻譯 SQL 的方式。

## 事前準備

如果您的 Google Cloud CLI 專案是在 2022 年 2 月 15 日前建立，請按照下列步驟啟用 BigQuery Migration API：

1. 前往 Google Cloud 控制台的「BigQuery Migration API」頁面。

   [前往 BigQuery Migration API](https://console.cloud.google.com/apis/api/bigquerymigration.googleapis.com/overview?hl=zh-tw)
2. 按一下「啟用」。

**注意：** 2022 年 2 月 15 日後建立的專案會自動啟用這項 API。

### 權限與角色

本節說明使用互動式 SQL 翻譯工具所需的[身分與存取權管理 (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，包括授予這些權限的[預先定義 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。本節也會說明設定其他翻譯設定所需的權限。

#### 使用互動式 SQL 翻譯器的權限

如要取得使用互動式翻譯工具所需的權限，請要求管理員授予 `parent` 資源的「[MigrationWorkflow 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquerymigration?hl=zh-tw#bigquerymigration.editor) 」(`roles/bigquerymigration.editor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備使用互動式翻譯工具所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用互動式翻譯工具，必須具備下列權限：

* `bigquerymigration.workflows.create`
* `bigquerymigration.workflows.get`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

#### 設定其他翻譯設定的權限

您可以使用轉譯設定中的「轉譯設定 ID」和「轉譯設定來源位置」欄位，設定其他轉譯設定。如要設定這些翻譯設定，您必須具備下列權限：

* `bigquerymigration.workflows.get`
* `bigquerymigration.workflows.list`

下列預先定義的 IAM 角色提供必要權限，讓您設定其他翻譯設定：

* `roles/bigquerymigration.viewer`

如要進一步瞭解 BigQuery IAM，請參閱「[使用身分與存取權管理功能控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」一文。

## 支援的 SQL 方言

BigQuery 互動式 SQL 翻譯器可將下列 SQL 方言翻譯成 GoogleSQL：

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

### 使用輔助 UDF 處理不支援的 SQL 函式

將來源 SQL 語法翻譯為 BigQuery 時，部分函式可能沒有直接對應的函式。為解決這個問題，BigQuery 遷移服務 (和更廣泛的 BigQuery 社群) 提供輔助使用者定義函式 (UDF)，可複製這些不支援的來源方言函式行為。

這些 UDF 通常位於 `bqutil` 公開資料集中，因此翻譯後的查詢一開始可以採用 `bqutil.<dataset>.<function>()` 格式參照這些 UDF。例如：`bqutil.fn.cw_count()`。

#### 正式環境的重要注意事項：

雖然 `bqutil` 可方便存取這些輔助 UDF，進行初始轉譯和測試，但基於下列原因，不建議直接依賴 `bqutil` 處理正式版工作負載：

1. 版本管控：`bqutil` 專案會代管這些 UDF 的最新版本，因此定義可能會隨時間變更。如果 UDF 的邏輯更新，直接依賴 `bqutil` 可能會導致生產查詢發生非預期行為或重大變更。
2. 依附元件隔離：將 UDF 部署至自己的專案，可避免外部變更影響正式環境。
3. 自訂：您可能需要修改或最佳化這些 UDF，進一步符合特定商業邏輯或效能需求。只有在這些資源位於您的專案中時，才能執行這項操作。
4. 安全性和治理：貴機構的安全政策可能會限制直接存取 `bqutil` 等公開資料集，以處理正式環境資料。將 UDF 複製到受控環境，符合這類政策規定。

#### 將輔助 UDF 部署至專案：

如要穩定可靠地在實際工作環境中使用，請將這些輔助 UDF 部署到自己的專案和資料集。您可以全面掌控這些應用程式的版本、自訂項目和存取權。
如需部署這些 UDF 的詳細操作說明，請參閱 [GitHub 上的 UDF 部署指南](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/udfs#deploying-the-udfs)。本指南提供必要的指令碼和步驟，協助您將 UDF 複製到環境中。

## 位置

互動式 SQL 翻譯器適用於下列處理位置：

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

[以 Gemini 為基礎的翻譯設定](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#ai_yaml_guidelines)僅適用於特定處理位置。詳情請參閱「[Google 模型端點位置](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#google_model_endpoint_locations)」。

## 將查詢翻譯為 GoogleSQL

請按照下列步驟將查詢翻譯成 GoogleSQL：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「編輯器」窗格中，按一下「更多」，然後選取「翻譯設定」。
3. 在「來源方言」部分，選取要翻譯的 SQL 方言。
4. 選用。在「Processing location」(處理位置) 中，選取要執行翻譯工作的地點。舉例來說，如果您位於歐洲，且不希望資料跨越任何位置限制範圍，請選取「eu」`eu`區域。
5. 按一下 [儲存]。
6. 在「編輯器」窗格中，按一下「更多」，然後選取「啟用 SQL 翻譯」。

   「編輯器」窗格會分成兩個窗格。
7. 在左側窗格中，輸入要翻譯的查詢。
8. 按一下「Translate」(翻譯)。

   BigQuery 會將查詢翻譯為 GoogleSQL，並顯示在右側窗格中。舉例來說，以下螢幕截圖顯示翻譯後的 Teradata SQL：
9. 選用步驟：如要執行翻譯後的 GoogleSQL 查詢，請按一下「執行」。
10. 選用：如要返回 SQL 編輯器，請點選「更多」，然後選取「停用 SQL 翻譯」。

    「編輯器」窗格會恢復為單一窗格。

## 搭配互動式 SQL 翻譯器使用 Gemini

您可以設定互動式 SQL 翻譯器，調整翻譯來源 SQL 的方式。方法是在 YAML 設定檔中提供要搭配 Gemini 使用的規則，或是提供含有 SQL 物件中繼資料或物件對應資訊的設定 YAML 檔案。

### 建立及套用已啟用 Gemini 的翻譯規則

**注意：** 如要取得預先發布版功能的支援，或提供意見回饋，請傳送電子郵件至 [ai-sql-translation-help@google.com](mailto:ai-sql-translation-help@google.com)。

您可以建立翻譯規則，自訂互動式 SQL 翻譯器翻譯 SQL 的方式。互動式 SQL 轉譯器會根據您指派的任何 Gemini 強化 SQL 轉譯規則調整轉譯內容，讓您根據遷移需求自訂轉譯結果。

如要建立已啟用 Gemini 的 SQL 轉譯規則，您可以在控制台中建立，也可以建立設定 YAML 檔案並上傳至 Cloud Storage。

### 控制台

如要為輸入的 SQL 建立 Gemini 輔助的 SQL 翻譯規則，請在查詢編輯器中編寫輸入的 SQL 查詢，然後依序點選「ASSIST」(輔助) >「Customize」(自訂)。([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))

同樣地，如要為輸出的 SQL 建立 Gemini 輔助 SQL 翻譯規則，請執行互動式翻譯，然後依序點選「輔助」>「自訂這項翻譯」。

「自訂」選單出現後，請繼續執行下列步驟。

1. 使用下列一或多個提示建立翻譯規則：

   * 在「Find and replace a pattern」(尋找並取代模式) 提示中，於「Replace」(取代) 欄位指定要取代的 SQL 模式，並在「With」(取代為) 欄位指定取代的 SQL 模式。

     SQL 模式可包含 SQL 指令碼中的任意數量陳述式、子句或函式。使用這項提示詞建立規則後，Gemini 強化版 SQL 轉譯功能會找出 SQL 查詢中該 SQL 模式的所有執行個體，並動態替換為其他 SQL 模式。舉例來說，您可以使用這個提示建立規則，將所有 `months_between (X,Y)` 換成 `date_diff(X,Y,MONTH)`。
   * 在「說明輸出內容的變更」欄位中，以自然語言輸入 SQL 翻譯輸出內容的變更。

     使用這項提示建立規則後，Gemini 輔助的 SQL 轉譯功能會識別要求，並對 SQL 查詢進行指定變更。
2. 按一下「預覽」。
3. 在「Gemini 生成的建議」對話方塊中，根據規則檢查 Gemini 強化版 SQL 轉譯功能對 SQL 查詢所做的變更。
4. 選用：如要新增這項規則，以便用於日後的翻譯作業，請勾選「儲存這個提示...」核取方塊。

   規則會儲存在預設設定 YAML 檔案或 `__default.ai_config.yaml` 中。
   這個 YAML 設定檔會儲存到 Cloud Storage 資料夾，如[翻譯設定](#translate-with-additional-configs)中的「Translation Configuration Source Location」欄位所指定。如果尚未設定「Translation Configuration Source Location」(翻譯設定來源位置)，系統會顯示資料夾瀏覽器，供您選取位置。設定 YAML 檔案須遵守[設定檔大小限制](#config-limitations)。
5. 如要將建議的變更套用至 SQL 查詢，請按一下「套用」。

### YAML

如要建立 Gemini 強化的 SQL 轉譯規則，請建立以 Gemini 為基礎的設定 YAML 檔案，並上傳至 Cloud Storage。詳情請參閱「[建立以 Gemini 為基礎的設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#ai_yaml_guidelines)」。

將 Gemini 強化版 SQL 轉譯規則上傳至 Cloud Storage 後，即可套用該規則，方法如下：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，依序點選「更多」**>「翻譯設定」**。
3. 在「Translation Configuration Source Location」(翻譯設定來源位置) 欄位中，指定儲存在 Cloud Storage 資料夾中的 Gemini 基礎 YAML 檔案路徑。
4. 按一下 [儲存]。

   儲存後，請執行互動式翻譯。如果提供設定 YAML 檔案，互動式翻譯工具會根據檔案中的規則，建議變更翻譯內容。

如果 Gemini 根據規則為輸入內容提供建議，系統會顯示「預覽建議的變更」對話方塊，並顯示翻譯輸入內容的可能變更。([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))

如果 Gemini 根據規則提供輸出內容建議，程式碼編輯器中會顯示通知橫幅。如要查看及套用這些建議，請按照下列步驟操作：

1. 在程式碼編輯器兩側，依序點選「輔助」>「查看建議」，即可重新查看對應查詢的建議變更。
2. 在「Gemini 生成的建議」對話方塊中，查看 Gemini 根據轉譯規則對 SQL 查詢所做的變更。
3. 如要將建議的變更套用至翻譯輸出內容，請按一下「套用」。

#### 更新以 Gemini 為基礎的設定 YAML 檔案

如要更新現有的設定 YAML 檔案，請按照下列步驟操作：

1. 在「Gemini 生成的建議」對話方塊中，按一下「查看 Gemini 規則設定檔」。
2. 設定編輯器隨即顯示，請選取要編輯的設定 YAML 檔案。
3. 進行變更，然後按一下「儲存」。
4. 按一下「完成」，關閉 YAML 編輯器。
5. 執行互動式翻譯，套用更新後的規則。

### 說明翻譯內容

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 透過 Gemini 強化版 SQL 轉譯功能，你可以使用 Gemini 模型為指令碼生成文字說明。已啟用 Gemini 的 SQL 翻譯功能可免費使用 Gemini，但有用量限制。這項用量足以應付大多數遷移專案。如要要求提高這項限制，或取得這項預先發布版功能的支援並提供意見回饋，請傳送電子郵件至 [ai-sql-translation-help@google.com](mailto:ai-sql-translation-help@google.com)。

執行互動式翻譯後，你可以要求 Gemini 生成文字說明。生成的文字包含翻譯後 SQL 查詢的摘要。Gemini 也會找出來源 SQL 查詢與轉譯的 GoogleSQL 查詢之間的轉譯差異和不一致之處。

如要取得 Gemini 生成的 SQL 翻譯說明，請按照下列步驟操作：

1. 如要建立 Gemini 生成的 SQL 翻譯說明，請依序點選「輔助」和「說明這項翻譯」。

### 使用批次翻譯設定 ID 翻譯

提供批次翻譯設定 ID，即可執行與批次翻譯工作相同翻譯設定的互動式查詢。

1. 在查詢編輯器中，依序點選「更多」**>「翻譯設定」**。
2. 在「Translation Configuration ID」(翻譯設定 ID) 欄位中，提供批次翻譯設定 ID，套用已完成的 BigQuery 批次遷移工作中的相同翻譯設定。

   如要找出工作的批次轉譯設定 ID，請從「SQL 轉譯」頁面選取批次轉譯工作，然後按一下「轉譯設定」分頁標籤。批次翻譯設定 ID 會列為「資源名稱」。
3. 按一下 [儲存]。

### 使用其他設定翻譯

您可以指定儲存在 Cloud Storage 資料夾中的設定 YAML 檔案，執行含有其他翻譯設定的互動式查詢。翻譯設定可能包含來源資料庫的 SQL 物件中繼資料或物件對應資訊，有助於提升翻譯品質。舉例來說，您可以加入來源資料庫的 DDL 資訊或結構定義，提升互動式 SQL 翻譯品質。

如要指定轉譯設定，請提供轉譯設定來源檔案的位置，然後按照下列步驟操作：

1. 在查詢編輯器中，依序點選「更多」**>「翻譯設定」**。
2. 在「轉譯設定來源位置」欄位中，指定儲存在 Cloud Storage 資料夾中的轉譯設定檔路徑。

   BigQuery 互動式 SQL 翻譯器支援包含[翻譯中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)和[物件名稱對應](https://docs.cloud.google.com/bigquery/docs/output-name-mapping?hl=zh-tw#json_file_format)的中繼資料 ZIP 檔案。如要瞭解如何將檔案上傳至 Cloud Storage，請參閱「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。
3. 按一下 [儲存]。

### 設定檔大小限制

使用 BigQuery 互動式 SQL 翻譯工具時，壓縮的後設資料檔案或 YAML 設定檔必須小於 50 MB。如果檔案大小超過 50 MB，互動式翻譯工具會在翻譯期間略過該設定檔，並產生類似下列內容的錯誤訊息：

`CONFIG ERROR: Skip reading file "gs://metadata-file.zip". File size (150,000,000 bytes)
exceeds limit (50 MB).`

如要縮減中繼資料檔案大小，可以使用 `--database` 或 `--schema` 旗標，只擷取與翻譯輸入查詢相關的資料庫或結構定義中繼資料。如要進一步瞭解如何使用這些旗標[產生中繼資料檔案](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)，請參閱「[全域旗標](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw#global_flags)」。

## 排解翻譯錯誤

使用互動式 SQL 翻譯器時，可能會遇到下列常見錯誤。

### `RelationNotFound` 或 `AttributeNotFound` 翻譯問題

使用[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw#translate_a_query_into_standard_sql)翻譯查詢後，您可能會遇到翻譯失敗的情況，並收到 `RelationNotFound` 或 `AttributeNotFound` 錯誤。

如要找出翻譯失敗的內容，請前往「翻譯詳細資料」頁面，然後開啟「記錄訊息」分頁。

為確保翻譯結果最準確，您可以在查詢本身之前，輸入查詢中使用的任何資料表資料定義語言 (DDL) 陳述式。舉例來說，如要翻譯 Amazon Redshift 查詢 `select table1.field1, table2.field1
from table1, table2 where table1.id = table2.id;`，請在互動式 SQL 翻譯器中輸入下列 SQL 陳述式：

```
create table schema1.table1 (id int, field1 int, field2 varchar(16));
create table schema1.table2 (id int, field1 varchar(30), field2 date);

select table1.field1, table2.field1
from table1, table2
where table1.id = table2.id;
```

#### 使用 Gemini 修正翻譯問題

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

如要修正 `RelationNotFound` 或 `AttributeNotFound` 錯誤導致的翻譯工作失敗問題，你也可以按照下列步驟使用 Gemini 嘗試解決這些問題。

1. 前往「Translation details」(翻譯詳細資料) 頁面，然後開啟「Log Messages」(記錄訊息) 分頁。
2. 在「類別」欄中，按一下含有 `RelationNotFound` 或 `AttributeNotFound` 訊息的查詢。
3. 按一下「建議修正方式」。
4. 按一下「套用」。
5. 按一下「翻譯」重新翻譯查詢。

## 定價

使用互動式 SQL 翻譯器不需付費。不過，儲存輸入和輸出檔案所用的儲存空間仍須支付一般費用。詳情請參閱「[儲存空間價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

## 後續步驟

進一步瞭解資料倉儲遷移作業的下列步驟：

* [遷移作業總覽](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw)
* [遷移評估](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)
* [結構定義與資料移轉總覽](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw)
* [批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)
* [資料管道](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw)
* [資安與資管](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)
* [資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator#data-validation-tool)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]