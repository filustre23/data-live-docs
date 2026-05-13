Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用查詢範本

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**附註：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-data-sharing-feedback@google.com](mailto:bq-data-sharing-feedback@google.com)。

BigQuery 資料無塵室查詢範本可加速取得洞察資料，並提供額外的安全防護和控管機制，盡量減少資料外洩疑慮。預先定義並限制可在資料無塵室執行的查詢，有助於：

* **防範機密資料外洩**。資料無塵室訂閱者在無塵室中執行查詢時，探索資料的彈性越大，資料擁有者就越可能意外或有意洩漏機密資訊。
* **簡化新手上路流程，方便不熟悉技術的使用者採用**。許多資料供應商認為資料無塵室訂閱者的技術能力較弱，尤其是在編寫以隱私權為重的 SQL 查詢和分配隱私權預算方面。
* **確保資料無塵室訂閱者獲得一致的分析結果**。
  如果無法控管在資料無塵室中執行的查詢，就更難強制執行特定資料分析規則，以及驗證是否符合隱私權法規。

資料擁有者和貢獻者可使用查詢範本，建立預先定義且經過核准的查詢，以配合資料無塵室的用途。他們也可以發布這些查詢，供訂閱者使用。預先定義的查詢會使用 BigQuery 中的[資料表值函式 (TVF)](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)，將整個資料表或特定欄位做為輸入參數傳遞，並傳回資料表做為輸出內容。

## 限制

* 查詢範本最多只支援兩個資料參照，也就是用來定義 TVF 查詢的資料，以及 TVF 接受的資料參數輸入內容。
  + 您可以在 TVF 的查詢定義中參照多個資料表或檢視區塊，但這些項目必須屬於同一資料擁有者或當事人。
* 查詢範本 TVF 僅支援 `TABLE` 和 `VIEW` 固定類型。
* 查詢範本定義[與 TVF 遵循相同的限制](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw#limitations)。

## 事前準備

按照下列步驟，為 Google Cloud 專案啟用 Analytics Hub API：

### 控制台

1. 前往 **Analytics Hub API** 頁面。

   [前往 Analytics Hub API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)
2. 在 Google Cloud 控制台工具列中選取專案。
3. 如果 API 尚未啟用，請點選「啟用」。

### bq

執行 [`gcloud services enable` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw)：

```
gcloud services enable analyticshub.googleapis.com
```

### 必要的角色

如要取得執行本文中工作所需的權限，請要求管理員授予下列 IAM 角色：

* 在資料無塵室中建立或刪除 TVF：
  + [Analytics Hub 發布者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.publisher)  (`roles/analyticshub.publisher`)
    專案
  + 專案的 [Analytics Hub 訂閱者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriber)  (`roles/analyticshub.subscriber`)
* 授權 TVF：
  專案的 [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)
* 在資料無塵室中新增、更新或刪除 TVF 刊登項目：
  + [Analytics Hub 發布者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.publisher)  (`roles/analyticshub.publisher`)
    專案
  + 專案的 [Analytics Hub 訂閱者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriber)  (`roles/analyticshub.subscriber`)
* 建立查詢範本：
  + [Analytics Hub 發布者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.publisher)  (`roles/analyticshub.publisher`)
    專案
  + 專案的 [Analytics Hub 訂閱者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriber)  (`roles/analyticshub.subscriber`)
* 核准查詢範本：
  + [Analytics Hub 發布者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.publisher)  (`roles/analyticshub.publisher`)
    專案
  + 專案的 [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)
* 訂閱含有查詢範本的資料無塵室：
  + 專案的 [Analytics Hub 訂閱者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriber)  (`roles/analyticshub.subscriber`)
  + [Analytics Hub 訂閱項目擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriptionOwner)  (`roles/analyticshub.subscriptionOwner`)
    在要訂閱資料無塵室的專案中
* 執行查詢範本中定義的查詢：
  + 專案的 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
  + 專案的 [BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user)  (`roles/bigquery.user`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行本文中工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行本文中的工作，必須具備下列權限：

* 在資料無塵室中建立或刪除 TVF：
  + 專案的 `bigquery.routines.create`
  + 專案的 `bigquery.routines.update`
  + 專案的 `bigquery.routines.delete`
* 授權 TVF：
  `bigquery.datasets.update`
  處理常式存取的資料集
* 建立查詢範本：
  + 專案的 `analyticshub.listings.subscribe`
  + 專案的 `analyticshub.queryTemplates.create`
* 核准查詢範本：
  + 專案的 `bigquery.routines.create`
  + `bigquery.datasets.update`
    處理常式存取的資料集
  + 專案的 `analyticshub.listings.create`
  + 專案的 `analyticshub.queryTemplates.approve`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 將現有 TVF 新增至資料無塵室

您可以使用 Analytics Hub API，將現有 TVF 新增至資料無塵室。

請使用 [`projects.locations.dataExchanges.listings.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/create?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.listings.create` 方法：

```
    curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X POST https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/listings?listingId=LISTING_ID -d
    '{"bigqueryDataset":{"dataset":"projects/PROJECT_ID/datasets/DATASET_ID","selectedResources":[{"routine":"projects/PROJECT_ID/datasets/DATASET_ID/tables/ROUTINE_ID"}],},"displayName":LISTING_NAME"}'
```

更改下列內容：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `PROJECT_ID`：來源資料集所屬專案的專案 ID。
* `DATASET_ID`：來源資料集 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：資料無塵室 ID。
* `LISTING_ID`：房源 ID。
* `LISTING_NAME`：房源名稱。
* `ROUTINE_ID`：日常安排 ID。

## 查詢範本角色

使用資料無塵室查詢範本時，主要有三種角色。每個角色都有特定的工作流程，本文稍後會說明。

* **範本建立者**：定義要在資料無塵室中執行的查詢。這個角色等同於下列任一 IAM 角色：
  [Analytics Hub 管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-admin-role)、
  [Analytics Hub 發布者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role)
  或 [Analytics Hub 清單管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role)。詳情請參閱「[範本建立者工作流程](#template-creator-workflows)」。
* **範本核准者**：資料擁有者，必須核准查詢範本的參照，範本才能供人使用。這個角色等同於下列任一 IAM 角色：[Analytics Hub 管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-admin-role)、[Analytics Hub 發布者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role)或 [Analytics Hub 清單管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role)。詳情請參閱「[範本核准者工作流程](#template-approver-workflows)」。
* **範本訂閱者**：訂閱資料無塵室的使用者，只能執行範本中核准的查詢。這個角色等同於 [Analytics Hub 訂閱者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) IAM 角色。詳情請參閱「[範本訂閱者工作流程](#template-subscriber-workflows)」。

## 範本建立者工作流程

查詢範本建立者可以執行下列操作：

* [建立查詢範本](#create-query-template)。
* [更新查詢範本](#update-query-template)。
* [將查詢範本送審](#submit-query-template)。
* [刪除查詢範本](#delete-query-template)。

### 將房源新增至資料無塵室

建立查詢範本前，請務必先將資料新增至資料無塵室。如要在資料無塵室中建立產品資訊，請按照下列步驟操作：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要在其中建立查詢範本的資料無塵室顯示名稱。
3. 按一下「新增資料」，然後按照步驟建立已設定分析規則的檢視畫面。如需詳細操作說明，請參閱「[建立產品資訊 (新增資料)](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw#add-data)」一文。

   1. 如要新增其他方的資料，請與其他[信任的貢獻者](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw#data_contributor_workflows)共用資料無塵室。此外，資料貢獻者也必須將資料新增至資料無塵室，才能在查詢範本中使用。
4. 為房源設定[資料外流](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)控管機制。
5. 設定房源的元資料控制選項。如果只想分享上一個步驟中新增資料的結構定義和說明 (而非分享資料本身)，請選取「排除連結資料集的商家資訊存取權」。

   **注意：** 您必須在資料無塵室交換庫層級擁有 Analytics Hub 訂閱者 (`roles/analyticshub.subscriber`) 角色，才能建立查詢範本。Analytics Hub 訂閱者角色可讓您查看新增至資料無塵室的資料結構定義。**注意：** 您無法更新產品資訊來啟用中繼資料控制項，因此建議您在新產品資訊中建立查詢範本。這項設定可確保範本訂閱者無法存取共用資料，包括需要 Analytics Hub 訂閱者角色才能查看中繼資料的資料貢獻者。
6. 查看房源詳細資料。
7. 按一下「新增資料」。現在，為資料建立的檢視區塊中繼資料已新增至資料無塵室。

### 建立查詢範本

選取下列選項之一：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要建立查詢範本的資料無塵室顯示名稱。
3. 在資料無塵室中，前往「範本」分頁。
4. 按一下「建立範本」。
5. 輸入範本名稱和說明。

   **注意：** 建立查詢範本後，就無法編輯範本名稱。
6. 點選「下一步」。
7. 您可以查看新增至資料無塵室的檢視表架構，並提議查詢定義。

   1. 請務必使用支援的[`CREATE TABLE FUNCTION` 語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_function_statement)定義查詢。
   2. 傳遞整個資料表或檢視區塊，並使用固定定義。您必須定義完整的資料表路徑參照，包括專案 ID 和資料集 ID，這些資料來自新增至資料無塵室的資料。例如：

      ```
      query_template1(t1 TABLE<year INT64>) AS (SELECT * FROM `project_id.dataset_id.table_id` WHERE year = table_id.year)
      ```
   3. 如果您已對資料套用隱私權分析規則，請務必確認這個 TVF 包含隱私權專用的 SQL 語法，例如 [`SELECT WITH AGGREGATION_THRESHOLD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_clause)。**注意：** 日常安排定義一律會隱藏，絕不會與範本訂閱者共用。訂閱者只會看到 TVF 預期的表格輸入參數。
8. 查看範本詳細資料。
9. 如要儲存範本但不送審，請按一下「儲存」。
   查詢範本的狀態現在為「草稿」。

您可以[更新查詢範本](#update-query-template)或[將查詢範本送交審查](#submit-query-template)。

**注意：** 你必須[授權 TVF 或常式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw#authorize_routines)，範本訂閱者才能查詢常式。如果透過執行 `CREATE OR REPLACE` 陳述式 (例如 `CREATE OR REPLACE FUNCTION`、`CREATE OR REPLACE PROCEDURE` 或 `CREATE OR REPLACE TABLE FUNCTION`) 修改日常安排，則必須重新授權日常安排。

### API

下列範例說明如何使用 `curl` 指令建立查詢範本：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X POST https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/queryTemplates?queryTemplateId=QUERY_TEMPLATE_ID -d
  'query_template {
  display_name: "DISPLAY_NAME",
  routine {
    definition_body: "QUERY_TEMPLATE_ID(TVF arguments) AS (TVF_DEFINITION)"
  }
}'
```

更改下列內容：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：資料無塵室 ID。
* `DISPLAY_NAME`：查詢範本的顯示名稱。建立查詢範本後，就無法編輯顯示名稱。
* `QUERY_TEMPLATE_ID`：查詢範本 ID。
* `TVF_DEFINITION`：TVF 定義。

下列程式碼範例顯示 API 呼叫的 `definition_body` 範例。
您必須定義完整的資料表路徑參照，包括專案 ID 和資料集 ID，這些資料來自新增至資料無塵室的資料。

```
  query_template1(t1 TABLE<year INT64>) AS (SELECT * FROM `project_id.dataset_id.table_id` WHERE year = table_id.year)
```

`definition_body` 類似於常式的定義。上述 `definition_body` 會轉譯為下列常式：

```
  CREATE OR REPLACE TABLE FUNCTION <approvers_dataset>.query_template1(t1 TABLE, y INT64)
  AS (SELECT * FROM t1 WHERE year > y)
```

您可以[更新查詢範本](#update-query-template)或[將查詢範本送交審查](#submit-query-template)。

### 更新查詢範本

只有在查詢範本處於「草稿」狀態時，您才能更新查詢範本。如果查詢範本已送審，就無法再修改。

如要更新查詢範本，請選取下列其中一個選項：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有查詢範本的資料無塵室顯示名稱。
3. 在資料無塵室中，前往「範本」分頁。
4. 找出要更新的範本所在的列，然後依序點選「動作」**>「編輯範本」**。
5. 視需要更新說明和主要聯絡人。

**注意：** 查詢範本顯示名稱無法更新。

1. 點選「下一步」。
2. 檢查查詢範本，然後按一下「儲存」，即可儲存變更，不必將範本送審。

**注意：** 你必須[授權 TVF 或常式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw#authorize_routines)，範本訂閱者才能查詢常式。如果您透過執行 `CREATE OR REPLACE` 陳述式 (例如 `CREATE OR REPLACE
FUNCTION`、`CREATE OR REPLACE PROCEDURE` 或 `CREATE OR REPLACE TABLE
FUNCTION`) 修改日常安排，則必須重新授權日常安排。

### API

以下範例說明如何使用 `curl` 指令更新查詢範本：

```
 curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
 -H "Content-Type: application/json" \
 -H 'x-goog-user-project:DCR_PROJECT_ID' \
 -X PATCH "https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/queryTemplates/QUERY_TEMPLATE_ID?updateMask=description" \
 -d '{
   "query_template": {
     "description": "New query template"
   }
 }'
```

更改下列內容：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：資料無塵室 ID。
* `QUERY_TEMPLATE_ID`：查詢範本 ID。

**注意：** 查詢範本顯示名稱無法更新。

### 將查詢範本送交審查

選取下列選項之一：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有查詢範本的資料無塵室顯示名稱。
3. 在資料無塵室中，前往「範本」分頁。
4. 在要送審的範本資料列中，依序按一下「動作」**>「送審」**。範本的狀態現在為「需要審查」。

**注意：**查詢範本送交審查後，就無法再修改。**注意：**您必須[授權 TVF 或常式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw#authorize_routines)，範本訂閱者才能查詢常式。如果透過執行 `CREATE OR REPLACE` 陳述式 (例如 `CREATE OR
REPLACE FUNCTION`、`CREATE OR REPLACE PROCEDURE` 或 `CREATE OR REPLACE TABLE
FUNCTION`) 修改日常安排，則必須重新授權日常安排。

### API

以下範例說明如何使用 `curl` 指令，提交查詢範本以供審查：

```
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X POST https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/queryTemplates/QUERY_TEMPLATE_ID:submit
```

更改下列內容：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：資料無塵室 ID。
* `QUERY_TEMPLATE_ID`：查詢範本 ID。

### 刪除查詢範本

只有在查詢範本處於「草稿」狀態時，才能刪除。如果查詢範本已送交審查，就無法再刪除。

選取下列選項之一：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有查詢範本的資料無塵室顯示名稱。
3. 在資料無塵室中，前往「範本」分頁。
4. 在要刪除的範本所在資料列中，依序點選「動作」**>「刪除範本」**。

### API

以下範例說明如何使用 `curl` 指令刪除查詢範本：

```
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X DELETE https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/queryTemplates?queryTemplateId=QUERY_TEMPLATE_ID
```

更改下列內容：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：資料無塵室 ID。
* `QUERY_TEMPLATE_ID`：查詢範本 ID。

## 範本核准者工作流程

查詢範本核准者可以[核准查詢範本](#approve-query-template)。

**重要事項：** 提交查詢範本以供審查後，資料無塵室的所有[資料貢獻者](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw#roles)都能查看查詢範本，但只有可存取查詢所參照資料的資料貢獻者，才能核准範本。

如果 TVF 參照的資料不屬於您 (例如其他投稿者的資料)，只有該資料的擁有者可以核准查詢範本。如果您要建立的 TVF 只會參照您的資料 (用於單向分享)，可以自行核准查詢範本。

### 核准查詢範本

選取下列選項之一：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有查詢範本的資料無塵室顯示名稱。
3. 在資料無塵室中，前往「範本」分頁。
4. 找出需要審查的範本所在的列，然後依序點選「核准狀態」**>「需要審查」**。
5. 按一下「核准」。
6. 選取範本位置。這個位置是建立 TVF 以供分享的位置。
7. 查看建議的查詢範本。
8. 如果查詢範本已核准在資料無塵室中使用，請按一下「核准」。

### API

1. 使用 `jobserver.query` 呼叫，從查詢範本建立常式：

   ```
   curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://bigquery.googleapis.com/bigquery/v2/projects/ROUTINE_PROJECT_ID/queries --data '{"query":"ROUTINE_CREATION_QUERY","useLegacySql":false}'
   ```

   更改下列內容：

   * `ROUTINE_PROJECT_ID`：建立常式的專案 ID。
   * `ROUTINE_CREATION_QUERY`：建立常式的查詢。
2. 將建立的例行程序新增至資料無塵室：

   ```
   curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X POST https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/listings?listingId=LISTING_ID -d
   '{"bigqueryDataset":{"dataset":"projects/PROJECT_ID/datasets/DATASET_ID","selectedResources":[{"routine":"projects/PROJECT_ID/datasets/DATASET_ID/tables/ROUTINE_ID"}],},"displayName":"LISTING_NAME"}'
   ```

   更改下列內容：

   * `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
   * `LOCATION`：資料無塵室的位置。
   * `CLEAN_ROOM_ID`：資料無塵室 ID。
   * `LISTING_ID`：房源 ID。
   * `PROJECT_ID`：來源資料集所屬專案的專案 ID。
   * `DATASET_ID`：來源資料集 ID。
   * `ROUTINE_ID`：日常安排 ID。
   * `LISTING_NAME`：房源名稱。
3. 將查詢範本狀態更新為「`APPROVED`」：

   ```
   curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/queryTemplates/QUERY_TEMPLATE_ID:approve  --data '{}'
   ```

   更改下列內容：

   * `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
   * `LOCATION`：資料無塵室的位置。
   * `CLEAN_ROOM_ID`：資料無塵室 ID。
   * `QUERY_TEMPLATE_ID`：查詢範本 ID。

### 拒絕查詢範本

在 Google Cloud 控制台中，只要不核准提交的審核中查詢範本，即可拒絕查詢範本。

## 範本訂閱者工作流程

查詢範本訂閱者可以查看及訂閱資料無塵室。如果只將查詢範本新增至資料無塵室，訂閱資料無塵室只會授予對應的 TVF 存取權，不會授予基礎共用資料的存取權。

### 訂閱查詢範本

選取下列選項之一：

### 控制台

如要訂閱查詢範本，請[訂閱資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw#subscribe_to_a_data_clean_room)。系統會授予所有已停用「排除連結資料集中的清單存取權」[設定的清單存取權](#add-listing-to-dcr)。

如要訂閱查詢範本，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 前往您在訂閱資料無塵室時建立的連結資料集。
3. 開啟已連結資料集中共用的常式或 TVF。
4. 按一下「叫用資料表函式」。
5. 將參數替換為可接受的輸入內容，也就是資料表名稱或欄位。
6. 按一下「執行」。

如果無法在「Explorer」面板中，將 TVF 巢狀結構視為連結資料集的子項元素，可以直接在連結資料集上查詢 TVF：

```
SELECT * FROM `myproject.dcr_linked_dataset.mytvf`(TABLE myTable);
```

### API

請使用 [`projects.locations.dataExchanges.subscribe` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/subscribe?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.subscribe` 方法：

```
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID:subscribe  --data '{"destination":"projects/SUBSCRIBER_PROJECT_ID/locations/LOCATION","subscription":"SUBSCRIPTION"}'
```

更改下列內容：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：資料無塵室 ID。
* `SUBSCRIBER_PROJECT_ID`：範本訂閱者專案的專案 ID。
* `SUBSCRIPTION`：訂閱方案名稱。

訂閱查詢範本後，您就能直接在連結的資料集上查詢 TVF：

```
SELECT * FROM `myproject.dcr_linked_dataset.mytvf`(TABLE myTable);
```

## 範例情境

查詢範本可協助在資料無塵室中進行不同形式的資料協作。以下各節說明範例情境。

### 單向分享情境

資料發布者會建立查詢範本，確認訂閱合作夥伴只能執行發布者定義的查詢。查詢範本建立者最終會自行核准查詢範本，因為沒有其他參與者加入資料無塵室。

在這個情境中，使用者 A 是資料無塵室擁有者，他建立名為 `campaign_analysis` 的資料無塵室，並新增名為 `my_campaign` 的資料集，其中包含 `campaigns` 資料表。使用者 A 設定匯總門檻政策和中繼資料控制項，確認只有中繼資料結構定義可見，範本訂閱者無法存取來源資料。使用者 A 接著從 `campaigns` 資料表定義資料表值函式，建立查詢範本，並限制連結資料集的訂閱者只能執行 TVF。

TVF 語法如下：

```
campaigns_template(t1 TABLE campaign_ID <STRING> ) AS (
SELECT WITH AGGREGATION_THRESHOLD company_id, company, sum(impressions) FROM myproject.my_campaign.campaigns
group by company_id, company
);
```

由於使用者 A 具有適當的廣告活動資料表權限 (BigQuery 資料擁有者角色)，因此提交查詢範本以供審查後，使用者 A 就能立即自行核准。

### 與多方協作共用

資料無塵室擁有者邀請信任的參與者，提議要對彼此的資料執行哪些查詢。雙方只能查看中繼資料結構定義，無法存取基礎共用資料，因此可安全地提出查詢。如果查詢定義參照的資料不屬於範本提案者，只有該資料的擁有者可以核准範本。

在此情境中，使用者 A 邀請資料無塵室貢獻者使用者 B 加入`campaign_analysis`無塵室。使用者 B 想要查看資料表的中繼資料結構定義，藉此提議查詢範本，將自己的資料與 `campaigns` 資料表彙整。

TVF 語法如下：

```
campaigns_template(t1 TABLE campaign_ID <STRING> ) AS (
SELECT WITH AGGREGATION_THRESHOLD company_id, company, sum(impressions) FROM my_project.my_campaign.campaigns
group by company_id, company
);
```

由於使用者 B 未新增或不擁有 `campaigns` 資料表，因此只有使用者 A 可以在查詢範本提交核准後核准。如要使用查詢範本，使用者 B 必須訂閱資料無塵室並叫用 TVF。使用者 B 會將自己的資料表 (其中包含名為 `campaign_ID` 的欄位) 做為資料表參數傳遞，並執行查詢範本中定義的私有 SQL。使用者 B 不必將自己的資料新增至資料無塵室。

使用者 B 也將名為 `my_transactions` 的資料集新增至資料無塵室，其中包含 `transactions` 和 `products` 資料表。使用者 B 設定匯總門檻政策和中繼資料控制項，確認只有中繼資料結構定義可見，範本訂閱者無法存取來源資料。

使用者 A 現在可以查看資料表的中繼資料結構定義，提出各種查詢範本，將自己的資料加入交易資料表。以下是 TVF 語法的範例：

```
transactions_template(t1 TABLE user_ID  <STRING> ) AS (
SELECT WITH AGGREGATION_THRESHOLD company_id, company, campaign_id, sku, category, date, sum(amount) FROM my_project.my_transactions.transactions
group by company_id, company, campaign_id, sku, category, date
);
```

```
transactions_template_with_join(t1 TABLE user_ID  <STRING> ) AS (
SELECT WITH AGGREGATION_THRESHOLD t.company_id, t.company, t.campaign_id, t.sku, t.date, p.product_name, p.product_category, sum(t.amount) FROM myproject.my_transactions.transactions t
left join my_project.my_transactions.products p
on t.product_id = p.product_id
group by t.company_id, t.company, t.campaign_id, t.sku, t.date, p.product_name, p.product_category
);
```

**注意：** 在 TVF 查詢語法中，只能參照同一方擁有的資料表。詳情請參閱「[限制](#limitations)」一節。

由於使用者 A 未新增或不擁有 `transactions` 和 `products` 資料表，因此只有使用者 B 可以在查詢範本提交核准後核准該範本。如要使用查詢範本，使用者 A 必須訂閱資料無塵室並叫用 TVF。使用者 A 傳遞自己的資料表 (欄位名稱為 `user_ID`) 做為資料表參數，並執行查詢範本中定義的隱私權 SQL。使用者 A 不必將自己的資料新增至資料無塵室。

## 定價

使用查詢範本的資料貢獻者只需支付[資料儲存](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)費用。

使用查詢範本的範本訂閱者只會在執行查詢時，支付[運算 (分析)](https://cloud.google.com/bigquery/pricing?hl=zh-tw#overview_of_pricing) 費用。

## 後續步驟

* 如要進一步瞭解資料無塵室，請參閱「[使用資料無塵室分享機密資料](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)」。
* 如要進一步瞭解訂閱方案，請參閱「[訂閱資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw#subscribe_to_a_data_clean_room)」。
* 如要進一步瞭解 TVF，請參閱[資料表函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)。
* 如要進一步瞭解資料輸出，請參閱「[資料輸出選項 (僅限 BigQuery 共用資料集)](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]