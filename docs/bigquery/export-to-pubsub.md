Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將資料匯出至 Pub/Sub (反向 ETL)

如要將資料匯出至 Pub/Sub，必須使用 BigQuery [持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)。

本文說明如何從 BigQuery 設定反向擷取、轉換及載入 (RETL) 至 [Pub/Sub](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw)。您可以在[持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)中使用 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)，將資料從 BigQuery 匯出至 [Pub/Sub 主題](https://docs.cloud.google.com/pubsub/docs/create-topic?hl=zh-tw)。

您可以透過 RETL 工作流程將資料發布至 Pub/Sub，結合 BigQuery 的分析功能與 Pub/Sub 的非同步可擴充全域訊息服務。這項工作流程可讓您以事件驅動的方式，將資料提供給下游應用程式和服務。

## 必要條件

您必須[建立服務帳戶](https://docs.cloud.google.com/iam/docs/service-accounts-create?hl=zh-tw)。如要執行持續查詢，並將結果匯出至 Pub/Sub 主題，必須使用[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。

您必須建立 [Pub/Sub 主題](https://docs.cloud.google.com/pubsub/docs/publish-message-overview?hl=zh-tw#about_topics)，才能以訊息形式接收持續查詢結果，並建立 [Pub/Sub 訂閱項目](https://docs.cloud.google.com/pubsub/docs/subscription-overview?hl=zh-tw)，供目標應用程式接收這些訊息。

## 必要的角色

本節說明建立持續查詢的使用者帳戶，以及執行持續查詢的服務帳戶，分別需要哪些角色和權限。

### 使用者帳戶權限

如要在 BigQuery 中建立工作，使用者帳戶必須具備 `bigquery.jobs.create` IAM 權限。下列 IAM 角色都會授予 `bigquery.jobs.create` 權限：

* [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user)
* [BigQuery 作業使用者 (`roles/bigquery.jobUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)
* [BigQuery 管理員 (`roles/bigquery.admin`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)

如要提交使用服務帳戶執行的工作，使用者帳戶必須具備「服務帳戶使用者」(`roles/iam.serviceAccountUser`)角色。如果您使用同一個使用者帳戶建立服務帳戶，則該使用者帳戶必須具備[服務帳戶管理員 (`roles/iam.serviceAccountAdmin`)](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) 角色。如要瞭解如何限制使用者存取單一服務帳戶，而非專案中的所有服務帳戶，請參閱「[授予單一角色](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw#grant-single-role)」。

如果使用者帳戶必須啟用持續查詢用途所需的 API，則該帳戶必須具備「服務使用情形管理員」角色 ([`roles/serviceusage.serviceUsageAdmin`](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageAdmin))。

### 服務帳戶權限

如要從 BigQuery 資料表匯出資料，服務帳戶必須具備 `bigquery.tables.export` IAM 權限。下列每個 IAM 角色都會授予 `bigquery.tables.export` 權限：

* [BigQuery 資料檢視器 (`roles/bigquery.dataViewer`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer)
* [BigQuery 資料編輯器 (`roles/bigquery.dataEditor`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor)
* [BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner)
* [BigQuery 管理員 (`roles/bigquery.admin`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)

如要讓服務帳戶存取 Pub/Sub，您必須授予服務帳戶下列兩個 IAM 角色：

* [Pub/Sub 檢視器 (`roles/pubsub.viewer`)](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.viewer)
* [Pub/Sub 發布者 (`roles/pubsub.publisher`)](https://docs.cloud.google.com/iam/docs/roles-permissions/pubsub?hl=zh-tw#pubsub.publisher)

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)取得必要權限。

## 事前準備

啟用 BigQuery 和 Pub/Sub API。

**啟用 API 時所需的角色**

如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

[啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cpubsub.googleapis.com&hl=zh-tw)

## 匯出至 Pub/Sub

使用 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)將資料匯出至 Pub/Sub 主題：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，依序點選「更多」>「查詢設定」。
3. 在「持續查詢」部分，勾選「使用持續查詢模式」核取方塊。
4. 在「Service account」(服務帳戶) 方塊中，選取您建立的服務帳戶。
5. 按一下 [儲存]。
6. 在查詢編輯器中輸入下列陳述式：

   ```
   EXPORT DATA
   OPTIONS (
   format = 'CLOUD_PUBSUB',
   uri = 'https://pubsub.googleapis.com/projects/PROJECT_ID/topics/TOPIC_ID'
   ) AS
   (
   QUERY
   );
   ```

   更改下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `TOPIC_ID`：Pub/Sub 主題 ID。您可以前往 Google Cloud 控制台的「主題」[頁面](https://console.cloud.google.com/cloudpubsub/topic/list?hl=zh-tw)取得主題 ID。
   * `QUERY`：用於選取要匯出資料的 SQL 陳述式。SQL 陳述式只能包含[支援的作業](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_functionality)。您必須在持續查詢的 `FROM` 子句中使用 [`APPENDS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#appends)，指定開始處理資料的時間點。
7. 按一下「執行」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 在指令列中，使用 [`bq query` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query)和下列旗標執行持續查詢：

   * 將 `--continuous` 旗標設為 `true`，即可持續查詢。
   * 使用 `--connection_property` 旗標指定要使用的服務帳戶。

   ```
   bq query --project_id=PROJECT_ID --use_legacy_sql=false \
   --continuous=true --connection_property=service_account=SERVICE_ACCOUNT_EMAIL \
   'EXPORT DATA OPTIONS (format = "CLOUD_PUBSUB", uri = "https://pubsub.googleapis.com/projects/PROJECT_ID/topics/TOPIC_ID") AS (QUERY);'
   ```

   更改下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `SERVICE_ACCOUNT_EMAIL`：服務帳戶電子郵件地址。您可以在 Google Cloud 控制台的「服務帳戶」[頁面](https://console.cloud.google.com/iam-admin/serviceaccounts?hl=zh-tw)取得服務帳戶電子郵件地址。
   * `QUERY`：用於選取要匯出資料的 SQL 陳述式。SQL 陳述式只能包含[支援的作業](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_functionality)。您必須在持續查詢的 `FROM` 子句中使用 [`APPENDS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#appends)，指定開始處理資料的時間點。

### API

1. 呼叫 [`jobs.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)，執行持續查詢。在您傳遞的 [`Job` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw)的 [`JobConfigurationQuery` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationQuery)中設定下列欄位：

   * 將 `continuous` 欄位設為 `true`，即可讓查詢持續執行。
   * 使用 `connection_property` 欄位指定要使用的服務帳戶。

   ```
   curl --request POST \
     'https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT_ID/jobs'
     --header 'Authorization: Bearer $(gcloud auth print-access-token) \
     --header 'Accept: application/json' \
     --header 'Content-Type: application/json' \
     --data '("configuration":("query":"EXPORT DATA OPTIONS (format = 'CLOUD_PUBSUB', uri = 'https://pubsub.googleapis.com/projects/PROJECT_ID/topics/TOPIC_ID') AS (QUERY);","useLegacySql":false,"continuous":true,"connectionProperties":["key": "service_account","value":"SERVICE_ACCOUNT_EMAIL"]))' \
     --compressed
   ```

   更改下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `QUERY`：用於選取要匯出資料的 SQL 陳述式。SQL 陳述式只能包含[支援的作業](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_functionality)。您必須在持續查詢的 `FROM` 子句中使用 [`APPENDS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#appends)，指定開始處理資料的時間點。
   * `SERVICE_ACCOUNT_EMAIL`：服務帳戶電子郵件地址。您可以在 Google Cloud 控制台的「服務帳戶」[頁面](https://console.cloud.google.com/iam-admin/serviceaccounts?hl=zh-tw)取得服務帳戶電子郵件地址。

## 將多個資料欄匯出至 Pub/Sub

如要在輸出內容中加入多個資料欄，可以建立包含資料欄值的 struct 資料欄，然後使用 [`TO_JSON_STRING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#to_json_string)將 struct 值轉換為 JSON 字串。
以下範例會匯出四個資料欄的資料，並以 JSON 字串格式呈現：

```
EXPORT DATA
  OPTIONS (
    format = 'CLOUD_PUBSUB',
    uri = 'https://pubsub.googleapis.com/projects/myproject/topics/taxi-real-time-rides')
AS (
  SELECT
    TO_JSON_STRING(
      STRUCT(
        ride_id,
        timestamp,
        latitude,
        longitude)) AS message
  FROM
    APPENDS(TABLE `myproject.real_time_taxi_streaming.taxi_rides`,
      -- Configure the APPENDS TVF start_timestamp to specify when you want to
      -- start processing data using your continuous query.
      -- This example starts processing at 10 minutes before the current time.
      CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE)
  WHERE ride_status = 'enroute'
);
```

## 匯出最佳化

如果持續查詢工作效能似乎受到[可用運算資源](https://docs.cloud.google.com/bigquery/docs/continuous-queries-monitor?hl=zh-tw#view_slot_consumption_information)限制，請嘗試增加 BigQuery [`CONTINUOUS` 運算單元預留指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)的大小。

## 限制

* 匯出的資料必須包含單一
  [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#string_type) 或
  [`BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#bytes_type) 欄。
  資料欄名稱可自行選擇。
* 您必須使用[持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)，才能匯出至 Pub/Sub。
* 您無法在持續查詢中將結構定義傳遞至 Pub/Sub 主題。
* 您無法將資料匯出至使用結構定義的 Pub/Sub 主題。
* 匯出至 Pub/Sub 時，您可以匯出 JSON 格式的記錄，其中部分值為 `NULL`，但無法匯出僅包含 `NULL` 值的記錄。在持續查詢中加入 `WHERE message IS NOT NULL` 篩選器，即可從查詢結果中排除 `NULL` 記錄。
* 將資料匯出至已設定[位置端點的 Pub/Sub 主題時，端點必須與包含所查詢資料表的 BigQuery 資料集位於相同的 Google Cloud 區域](https://docs.cloud.google.com/pubsub/docs/reference/service_apis_overview?hl=zh-tw#pubsub_endpoints)界線內。
* 匯出的資料不得超過 [Pub/Sub 配額](https://docs.cloud.google.com/pubsub/quotas?hl=zh-tw)。

## 定價

匯出持續查詢中的資料時，系統會按照 [BigQuery 容量運算價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)計費。如要執行連續查詢，您必須擁有使用 [Enterprise 或 Enterprise Plus 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的[預留位置](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)，以及使用 `CONTINUOUS` 工作類型的[預留位置指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。

匯出資料後，系統會向您收取 Pub/Sub 使用費。
詳情請參閱「[Pub/Sub 定價](https://cloud.google.com/pubsub/pricing?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]