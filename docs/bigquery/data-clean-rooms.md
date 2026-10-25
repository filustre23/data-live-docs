Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過資料無塵室共用機密資料

您可以運用資料無塵室，建立安全性更高的環境。在這個環境中，多方可以共用、彙整及分析資料資產。這項協作作業不會移動或揭露基礎資料。

BigQuery 資料無塵室與 BigQuery sharing (舊稱 Analytics Hub) 平台整合。標準 [BigQuery 共用資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)支援大規模跨組織資料共用。不過，資料無塵室專門用於處理機密和受保護的資料。資料無塵室提供額外的安全控管機制，可保護基礎資料，並強制執行資料擁有者定義的[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)。

**注意：** 資料無塵室中的分析規則提供隱私權控制項，但可能無法完全防止複雜的查詢擷取未經授權的資料。如要控管並限制只能執行核准的查詢，請使用[查詢範本](#query_templates)。

## 用途

主要用途包括：

* **廣告活動規劃和目標對象洞察**讓兩方 (例如賣家和買家) 混合第一方資料，並以注重隱私權的方式充實資料。
* **評估和歸因。**比對顧客和媒體成效資料，進一步瞭解行銷成效，並決定日後的廣告活動。
* **啟用：**將顧客數位資料與其他方的資料結合，進一步瞭解顧客，提升區隔能力和媒體啟用成效。

資料無塵室也支援行銷業以外的多種用途：

* **零售和民生消費用品業 (CPG)。**整合零售商的銷售點資料和 CPG 公司的行銷資料，最佳化行銷和促銷活動。
* **金融服務**。結合其他金融和政府機關的機密資料，提升詐欺偵測能力。匯總多間銀行的客戶資料，建立信用風險評分。
* **醫療照護：**在醫生和藥物研究人員之間分享資料，瞭解病患對治療的反應。
* **供應鏈、物流和運輸：**結合供應商和行銷人員的資料，全面瞭解產品在整個生命週期中的成效。

## 角色

BigQuery 資料無塵室有三種主要角色：

* **資料無塵室擁有者**：管理 Google Cloud 專案中一或多個資料無塵室的權限、瀏覽權限和成員資格。資料無塵室擁有者可以將資料貢獻者和資料無塵室訂閱者角色指派給使用者。這個角色類似於 [Analytics Hub 管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-admin-role) Identity and Access Management (IAM) 角色。
* **資料提供者**：將資料發布至資料無塵室。在許多情況下，資料無塵室擁有者也是資料提供者。這個角色類似於 [Analytics Hub 發布者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) IAM 角色。
* **資料無塵室訂閱者**：訂閱資料無塵室中發布的資料，並對資料執行查詢。這個角色類似於 [Analytics Hub 訂閱者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role)和 [Analytics Hub 訂閱項目擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriptionOwner) IAM 角色的組合。

## 架構

BigQuery 資料無塵室採用 BigQuery 資料的發布和訂閱模式。BigQuery 架構會區分運算和儲存空間，讓資料提供者不必建立多份資料副本，就能共用資料。下圖顯示 BigQuery 資料無塵室架構：

### 資料無塵室

資料無塵室是共用機密資料的環境，可防止原始存取，並強制執行查詢限制。只有新增為資料無塵室訂閱者的使用者或群組，才能訂閱共用資料。資料無塵室擁有者可以在 BigQuery 共用中建立任意數量的資料無塵室。

### 共用資源

共用資源是資料無塵室中的資料共用單位。資源必須是 BigQuery 資料表、檢視表或常式 (資料表值函式)。資料提供者會在專案中建立或使用現有的 BigQuery 資源，與資料無塵室訂閱者共用。

### 清單

以資料提供者身分將資料新增至資料無塵室時，您會建立一筆資訊。清單包含共用資源的參照資訊，以及可協助訂閱者使用資料的說明資訊。您可以加入說明、查詢範例和說明文件連結等資訊，供訂閱者參考。

### 連結的資料集

連結的資料集是唯讀 BigQuery 資料集，做為資料無塵室中所有資料的符號連結。資料無塵室訂閱者查詢連結資料集中的資源時，系統會傳回共用資源中的資料，並滿足資料提供者設定的分析規則集。訂閱資料無塵室後，BigQuery 會在專案中建立連結資料集。系統不會建立資料副本，訂閱者也無法查看特定中繼資料，例如檢視表定義。

### 分析規則

資料提供者可針對在資料無塵室共用的資源，設定分析規則。[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)有助於防止原始存取基礎資料，並強制執行查詢限制。舉例來說，資料無塵室支援[匯總門檻分析規則](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_clause)，資料無塵室訂閱者只能透過匯總查詢分析資料。

### 資料輸出控制項

[資料輸出](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)控制項會自動防止資料無塵室訂閱者複製及匯出資料無塵室中的原始資料。資料提供者可以設定其他控制項，防止訂閱者複製及匯出查詢結果。

### 查詢範本

[查詢範本](https://docs.cloud.google.com/bigquery/docs/query-templates?hl=zh-tw)可讓資料無塵室擁有者和 BigQuery sharing 發布者共用預先定義的查詢，而不必共用資料表和檢視表的基礎資源。

預先定義的查詢會使用 BigQuery 中的[資料表值函式 (TVF)](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)，可將整個資料表或特定欄位做為輸入參數傳遞，並傳回資料表做為輸出內容。

## 限制

BigQuery 資料無塵室有下列限制：

* 您只能在檢視表上設定[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)，無法在資料表或 materialized view 上設定。由於這項限制，如果資料提供者直接將資料表、materialized view 或不含分析規則的檢視表，共用至資料無塵室，訂閱者就能存取原始資料。
* 雖然[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)提供隱私權控制項，但無法保證能封鎖所有未經授權、旨在擷取原始資料的查詢。為保護資訊安全，請在資料無塵室中使用[查詢範本](https://docs.cloud.google.com/bigquery/docs/query-templates?hl=zh-tw)審查及核准查詢，藉此封鎖未經授權的嘗試。
* 由於資料無塵室使用 BigQuery 共用平台，因此所有 [BigQuery 共用限制](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#limitations)皆適用。
* 資料無塵室僅適用於 [BigQuery 共用區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)。
* 資料無塵室訂閱者無法在 Knowledge Catalog 搜尋共用資源。
* 資料無塵室訂閱者無法查詢連結資料集上的 [`INFORMATION_SCHEMA` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)。
* 資料提供者無法直接將整個資料集發布至資料無塵室。
* 資料提供者無法將模型或常式 (查詢範本除外) 發布至資料無塵室。
* 資料無塵室最多可新增 100 項共用資源。如要提高上限，請傳送電子郵件至 [bq-dcr-feedback@google.com](mailto:bq-dcr-feedback@google.com)。
* 資料無塵室不支援多個區域的產品資訊。

## 事前準備

授予 IAM 角色，確保您具備完成本文件所述工作所需的權限、啟用 Analytics Hub API，並將 Analytics Hub 管理員角色指派給資料無塵室擁有者。

### 所需權限

如要取得使用資料無塵室所需的權限，請要求管理員授予您 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備使用資料無塵室所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

必須具備下列權限，才能使用資料無塵室：

* `serviceUsage.services.get`
* `serviceUsage.services.list`
* `serviceUsage.services.enable`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 啟用 Analytics Hub API

如要啟用 Analytics Hub API，請選取下列其中一個選項：

### 控制台

前往「**Analytics Hub API**」頁面，為 Google Cloud 專案啟用 API。

[啟用 Analytics Hub API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### gcloud

執行 [`gcloud services enable` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw)：

```
gcloud services enable analyticshub.googleapis.com
```

啟用 Analytics Hub API 後，即可存取[「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)。

### 授予 Analytics Hub 管理員角色

如要以擁有者身分建立資料無塵室，您必須具備 [Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-admin-role) (`roles/analyticshub.admin`)。如要進一步瞭解如何將這個角色授予其他使用者，請參閱「[建立 BigQuery sharing 管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#create-exchange-administrator)」。

## 資料無塵室擁有者工作流程

資料無塵室擁有者可以執行下列操作：

* 建立資料無塵室。
* 更新資料無塵室屬性。
* 刪除資料無塵室。
* 管理資料提供者。
* 管理資料無塵室訂閱者。
* 共用資料無塵室。

### 其他資料無塵室擁有者權限

如要完成資料無塵室擁有者工作，您必須具備專案的 Analytics Hub 管理員角色 (`roles/analyticshub.admin`)。您也可以在資料夾或組織層級指派這個角色 (如適用)。

### 建立資料無塵室

如要建立資料無塵室，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「建立資料無塵室」。
3. 在「Project」(專案) 部分，選取資料無塵室的專案。您必須為專案啟用 Analytics Hub API。
4. 指定資料無塵室的位置、名稱、主要聯絡人、圖示 (選用) 和說明。您只能列出與資料無塵室位於相同區域的資料無塵室資源。
5. 選用：如要記錄所有在連結資料集上執行工作和查詢的使用者[主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)，請按一下「Subscriber Email Logging」(訂閱者電子郵件記錄) 切換鈕。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄位中。

   **注意：** 啟用並儲存電子郵件記錄功能後，就無法編輯這項設定。
   如要停用電子郵件記錄功能，請刪除資料無塵室，然後重新建立，但不要點選「Subscriber Email Logging」(訂閱者電子郵件記錄) 切換鈕。
6. 按一下「建立資料無塵室」。
7. 選用：在「Clean Room Permissions」(資料無塵室權限) 部分，新增其他資料無塵室擁有者、資料貢獻者或資料無塵室訂閱者。

### API

請使用 [`projects.locations.dataExchanges.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/create?hl=zh-tw)，並將[共用環境](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#sharingenvironmentconfig)設為 `dcrExchangeConfig`。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.create` 方法：

```
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges?dataExchangeId=CLEAN_ROOM_ID -d \
  '{
    "displayName": "CLEAN_ROOM_NAME",
    "sharingEnvironmentConfig": {"dcrExchangeConfig": {}}
  }'
```

替換下列內容：

* `PROJECT_ID`：專案 ID
* `LOCATION`：資料無塵室的位置
* `CLEAN_ROOM_ID`：資料無塵室 ID
* `CLEAN_ROOM_NAME`：資料無塵室的顯示名稱

在要求主體中，提供[資料交換詳細資料](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#resource:-dataexchange)。

如果要求成功，回應主體會包含資料無塵室的詳細資料。

如果使用 `logLinkedDatasetQueryUserEmail` 欄位啟用訂閱者電子郵件記錄功能，資料交換回應會包含 `log_linked_dataset_query_user_email: true`。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄位中。

### 更新資料無塵室

如要更新資料無塵室屬性，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要更新的資料無塵室顯示名稱。
3. 在「詳細資料」分頁中，按一下「編輯資料無塵室詳細資料」。
4. 視需要更新資料無塵室名稱、主要聯絡人、圖示、說明或訂閱者電子郵件記錄設定。

   **注意：** 啟用並儲存電子郵件記錄功能後，就無法編輯這項設定。如要停用電子郵件記錄功能，請刪除資料無塵室，然後重新建立，但不要點選「Subscriber Email Logging」(訂閱者電子郵件記錄) 切換鈕。
5. 按一下 [儲存]。

### API

請使用 [`projects.locations.dataExchanges.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/patch?hl=zh-tw)，並將[共用環境](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#sharingenvironmentconfig)設為 `dcrExchangeConfig`。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.patch` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X PATCH https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID?updateMask=UPDATEMASK -d \
'{
  "displayName": "CLEAN_ROOM_NAME",
  "sharingEnvironmentConfig": {"dcrExchangeConfig": {}}
}'
```

替換下列內容：

* `PROJECT_ID`：專案 ID
* `LOCATION`：資料無塵室的位置
* `CLEAN_ROOM_ID`：資料無塵室 ID
* `UPDATEMASK`：以半形逗號分隔的欄位清單，列出要更新的欄位，例如 `displayName,primaryContact`
* `CLEAN_ROOM_NAME`：資料無塵室的顯示名稱

在要求主體中，指定下列欄位的更新值：

* `displayName`
* `description`
* `primaryContact`
* `documentation`
* `icon`
* `discoveryType`
* `logLinkedDatasetQueryUserEmail`

如要進一步瞭解這些欄位，請參閱「[資源：DataExchange](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#resource:-dataexchange)」。

### 刪除資料無塵室

如要刪除資料無塵室，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 在要刪除的資料無塵室資料列中，依序按一下
   more\_vert
   **「More actions」(更多動作) > 「Delete」(刪除)**。
3. 如要確認，請輸入 `delete`，然後按一下「Delete」(刪除)。這項操作無法復原。

### API

請使用 [`projects.locations.dataExchanges.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/delete?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.delete` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X DELETE https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID
```

替換下列內容：

* `PROJECT_ID`：專案 ID
* `LOCATION`：資料無塵室的位置
* `CLEAN_ROOM_ID`：資料無塵室 ID

刪除資料無塵室後，當中的所有產品資訊都會刪除。共用資源和連結的資料集不會刪除。連結的資料集會與來源資料集取消連結，因此資料無塵室訂閱者無法再查詢資料無塵室中的資源。

### 管理資料提供者

資料無塵室擁有者可以管理哪些人能將資料新增至資料無塵室 (資料提供者)。如要允許資料提供者將資料新增至資料無塵室，請在該資料無塵室中授予[Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) (`roles/analyticshub.publisher`)：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要授予權限的資料無塵室顯示名稱。
3. 在「詳細資料」分頁中，按一下「設定權限」。
4. 按一下「Add principal」(新增主體)。
5. 在「New principals」(新增主體) 中，輸入要新增的資料提供者使用者名稱或電子郵件。
6. 在「**選取角色**」部分，依序選取
   「**Analytics Hub > Analytics Hub 發布者**」。
7. 按一下 [儲存]。

您隨時可以點選「Set permissions」(設定權限)，刪除及更新資料提供者。

### API

請使用 [`projects.locations.dataExchanges.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/setIamPolicy?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.setIamPolicy` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID:setIamPolicy -d \
'{
  "policy": {
    "bindings": [
      {
        "members": [
          "my-service-account@my-project.iam.gserviceaccount.com"
        ],
        "role": "roles/analyticshub.publisher"
      }
    ]
  }
}'
```

要求主體中的政策必須符合[政策](https://docs.cloud.google.com/iam/docs/reference/rest/v1/Policy?hl=zh-tw)的結構。

您可以在[「IAM」頁面](https://console.cloud.google.com/iam-admin?hl=zh-tw)，為整個專案授予 Analytics Hub 發布者角色 (`roles/analyticshub.publisher`)。這項權限可讓您將資料新增至該專案中的任何資料無塵室。不建議在專案層級授予這個角色，因為這可能會導致存取權限過於寬鬆。

### 管理資料無塵室訂閱者

資料無塵室擁有者可以管理哪些人能訂閱資料無塵室 (即訂閱者)。如要允許訂閱者訂閱資料無塵室，請在該資料無塵室中，授予他們 [Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`) 和 [Analytics Hub 訂閱項目擁有者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscription-owner-role) (`roles/analyticshub.subscriptionOwner`)：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要授予權限的資料無塵室顯示名稱。
3. 在「詳細資料」分頁中，按一下「設定權限」。
4. 按一下「Add principal」(新增主體)。
5. 在「New principals」(新增主體) 中，輸入要新增的資料無塵室訂閱者使用者名稱或電子郵件地址。
6. 在「**請選擇角色**」部分，依序選取
   「**Analytics Hub > Analytics Hub 訂閱者**」
7. 按一下 add\_box「Add another role」(新增其他角色)。
8. 在**「選取角色」**部分，依序選取
   **「Analytics Hub」>「Analytics Hub 訂閱項目擁有者」**。
9. 按一下 [儲存]。

您隨時可以點選「Set permissions」(設定權限)，刪除及更新資料無塵室訂閱者。

### API

請使用 [`projects.locations.dataExchanges.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/setIamPolicy?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.setIamPolicy` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID:setIamPolicy -d \
'{
  "policy": {
    "bindings": [
      {
        "members": [
          "user:mike@example.com"
        ],
        "role": "roles/analyticshub.subscriptionOwner"
      },
      {
        "members": [
          "user:mike@example.com"
        ],
        "role": "roles/analyticshub.subscriber"
      }
    ]
  }
}'
```

要求主體中的政策必須符合[政策](https://docs.cloud.google.com/iam/docs/reference/rest/v1/Policy?hl=zh-tw)的結構。

您可以在[「IAM」頁面](https://console.cloud.google.com/iam-admin?hl=zh-tw)，為整個專案授予 Analytics Hub 訂閱者角色 (`roles/analyticshub.subscriber`) 和 Analytics Hub 訂閱項目擁有者角色 (`roles/analyticshub.subscriptionOwner`)。這些角色可授予訂閱該專案中任何資料無塵室的權限。請避免在專案層級授予這些角色，以免存取權限過於寬鬆。

### 共用資料無塵室

您可以直接與資料無塵室訂閱者共用資料無塵室：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 在要共用的資料無塵室資料列中，依序按一下
   more\_vert
   **「More actions」(更多動作) >「Copy share link」(複製共用連結)**。
3. 如要讓訂閱者查看及訂閱資料無塵室，請與他們分享複製的連結。

## 資料貢獻者工作流程

資料提供者可以執行下列操作：

* 建立清單，將資料新增至資料無塵室。
* 更新商店資訊。
* 刪除產品資訊。
* 共用資料無塵室。
* 監控產品資訊。

### 其他資料提供者權限

如要完成資料提供者工作，您必須具備資料無塵室的 [Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) (`roles/analyticshub.publisher`)。

此外，您還需要來源資料集和資料表的 `bigquery.datasets.get`、`bigquery.datasets.update` 和 `bigquery.tables.get` 權限。[BigQuery 資料擁有者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner) (`roles/bigquery.dataOwner`) 具備這些權限。

如要查看貴組織中不屬於目前專案的資料無塵室，您必須具備 `resourcemanager.organizations.get` 權限。

如要使用資料無塵室建立程序，建立具有[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)的 [BigQuery 檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw#creating_a_view)，您必須具備 `bigquery.tables.setPrivacyPolicy` 和 `bigquery.tables.create` 權限。如果直接參照檢視表，則不需要這項權限。

### 建立產品資訊 (新增資料)

**注意：** 如果協作環境需要通用 ID，才能彙整資料提供者和資料無塵室訂閱者資料集的資料，請先設定[實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-setup?hl=zh-tw)，再按照下列步驟操作。

如要使用[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)準備資料，並以清單形式發布至資料無塵室，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要建立產品資訊的資料無塵室顯示名稱。

   如果您與資料無塵室擁有者不屬於同一個組織，且無法查看資料無塵室，請向資料無塵室擁有者索取直接連結。
3. 點選「新增資料」。
4. 在「Select dataset」(選取資料集) 和「Table/view name」(資料表/檢視表名稱)，輸入要在資料無塵室列出的資料表或檢視表，以及對應的資料集。您將新增分析規則，防止原始存取這個基礎資料，只需幾個步驟即可完成。
5. 選取要發布的資源資料欄。
6. 設定清單的檢視名稱、主要聯絡人和說明 (選用)。
7. 點選「下一步」。
8. 為清單選擇分析規則，並設定詳細資料。
9. 設定清單的[資料輸出](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)控制項。
10. 點選「下一步」。
11. 查看要新增至資料無塵室的資料和分析規則。
12. 按一下「新增資料」。系統會為資料建立檢視表，並將其新增為資料無塵室的項目。來源資料表或檢視表本身不會新增。

### API

請使用 [`projects.locations.dataExchanges.listings.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/create?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.listings.create` 方法：

```
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X POST https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/listings?listingId=LISTING_ID -d \
  '{"bigqueryDataset":{"dataset":"projects/PROJECT_ID/datasets/DATASET_ID","selectedResources":[{"table":"projects/PROJECT_ID/datasets/DATASET_ID/tables/VIEW_ID"}]},"displayName":"LISTING_NAME"}'
```

替換下列內容：

* `DCR_PROJECT_ID`：資料無塵室建立所在專案的專案 ID。
* `PROJECT_ID`：來源資料集所在專案的專案 ID。
* `DATASET_ID`：來源資料集 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：資料無塵室 ID。
* `LISTING_ID`：您的產品資訊 ID。
* `LISTING_NAME`：您的產品資訊名稱。
* `VIEW_ID`：檢視表 ID。您新增至資料無塵室的檢視表，必須是已設定[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)的[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。

在資料無塵室中列出資源，即代表您授予所有目前和未來的資料無塵室訂閱者存取共用資源中資料的權限。

如果您建立的清單包含缺少分析規則的共用資源，系統會顯示警告，指出訂閱者可以存取該資源的原始資料。確認警告後，仍可建立產品資訊。

如果收到 `Failed to save listing` 錯誤，請確認您具備[完成資料提供者工作所需的權限](#additional_data_contributor_permissions)。

### 更新商店資訊

如要更新商店資訊，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下資料無塵室的顯示名稱，其中包含該產品資訊。
3. 在要更新的產品資訊列中，依序按一下
   more\_vert
   **「More actions」(更多動作) >「Edit listing」(編輯產品資訊)**。
4. 視需要更新主要聯絡人或說明。
5. 點選「下一步」。
6. 視需要更新分析規則。您只能更新所選規則的參數。無法切換至其他規則。
7. 點選「下一步」。
8. 檢查商店資訊，然後按一下「儲存」。

### API

請使用 [`projects.locations.dataExchanges.listings.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/patch?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.listings.patch` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X PATCH https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/listings/LISTING_ID?updateMask=displayName -d \
'{"displayName":"LISTING_NAME"}'
```

替換下列內容：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：資料無塵室 ID。
* `LISTING_ID`：您的產品資訊 ID。
* `LISTING_NAME`：您的產品資訊名稱。

建立清單後，就無法變更來源資源或資料輸出控管。

### 刪除商家資訊

如要刪除商店資訊，請選擇下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下資料無塵室的顯示名稱，其中包含該產品資訊。
3. 在要刪除的產品資訊列中，依序按一下
   more\_vert
   **「More actions」(更多動作) >「Delete listing」(刪除產品資訊)**。
4. 如要確認，請輸入 `delete`，然後按一下「Delete」(刪除)。這項操作無法復原。

### API

請使用 [`projects.locations.dataExchanges.listings.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/delete?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.listings.delete` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X DELETE https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/listings/LISTING_ID
```

替換下列內容：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：資料無塵室 ID。
* `LISTING_ID`：您的產品資訊 ID。

刪除項目時，共用資源和連結的資料集不會一併刪除。連結的資料集會與來源資料集取消連結，因此資料無塵室訂閱者無法再查詢該清單中的資源。

### 共用資料無塵室

您可以直接與資料無塵室訂閱者共用資料無塵室：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 在要共用的資料無塵室資料列中，依序按一下
   more\_vert
   **「More actions」(更多動作) >「Copy share link」(複製共用連結)**。
3. 如要讓訂閱者查看及訂閱資料無塵室，請與他們分享複製的連結。

### 監控產品資訊

如要查看資料無塵室中共用資源的來源資料集用量指標，請查詢 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)。

如要查看資料無塵室訂閱者，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下資料無塵室的顯示名稱。
3. 在要查看的產品資訊列中，依序按一下
   more\_vert
   **「More actions」(更多動作) >「View subscriptions」(查看訂閱項目)**。

## 資料無塵室訂閱者工作流程

資料無塵室訂閱者可以執行下列操作：

* 訂閱資料無塵室。
* 查詢連結資料集中的資料。

訂閱資料無塵室後，系統會在專案中建立一個連結的資料集。每個連結資料集的名稱都與資料無塵室相同。

您無法訂閱資料無塵室中的特定清單，您只能訂閱資料無塵室本身。

### 其他資料無塵室訂閱者權限

如要完成資料無塵室訂閱者工作，您必須具備資料無塵室的 [Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`)，以及訂閱專案的 [Analytics Hub 訂閱項目擁有者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscription-owner-role) (`roles/analyticshub.subscriptionOwner`)。

訂閱資料無塵室時，您也需要專案中的 `bigquery.datasets.create` 權限，才能建立連結的資料集。

### 訂閱資料無塵室

訂閱資料無塵室後，系統會在您的專案中建立連結資料集，讓您查詢清單中的資料。如要訂閱資料無塵室，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，點選 add\_box「Add data」(新增資料)。
3. 選取「Sharing (Analytics Hub)」。探索頁面隨即開啟。
4. 如要顯示您有權存取的資料無塵室，請在篩選器清單中選取「Clean rooms」(資料無塵室)。
5. 按一下要訂閱的資料無塵室。資料無塵室的說明頁面隨即開啟。在這個頁面中，您也可以查看供應商是否已啟用訂閱者電子郵件記錄功能。
6. 點選「訂閱」。
7. 選取訂閱項目的目的地專案，然後按一下「Subscribe」(訂閱)。

### API

請使用 [`projects.locations.dataExchanges.subscribe` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/subscribe?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.subscribe` 方法：

```
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID:subscribe  --data '{"destination":"projects/SUBSCRIBER_PROJECT_ID/locations/LOCATION","subscription":"SUBSCRIPTION"}'
```

替換下列內容：

* `DCR_PROJECT_ID`：資料無塵室建立所在專案的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：資料無塵室 ID。
* `SUBSCRIBER_PROJECT_ID`：訂閱者專案的專案 ID。
* `SUBSCRIPTION`：訂閱項目的名稱。
* `LINKED_DATASET_ID`：您要為連結資料集指定的 ID。
* `PRIMARY_REGION`：要建立連結資料集的主要地理區域。

在要求主體中，指定目的地位置、訂閱項目名稱，以及要建立[連結資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)的資料集：

```
{
  "destination": "projects/SUBSCRIBER_PROJECT_ID/locations/LOCATION",
  "subscription": "SUBSCRIPTION",
  "destinationDataset": {
    "datasetReference": {
      "projectId": "SUBSCRIBER_PROJECT_ID",
      "datasetId": "LINKED_DATASET_ID"
    },
    "location": "PRIMARY_REGION"
  }
}
```

如果要求成功，回應主體會包含 [`Operation` 物件](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/subscribe?hl=zh-tw#body.response_body)。

如果您使用 `logLinkedDatasetQueryUserEmail` 欄位，為資料無塵室啟用訂閱者電子郵件記錄功能，訂閱回應會包含 `log_linked_dataset_query_user_email: true`。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄位中。

連結的資料集現已新增至您指定的專案，可供查詢。

資料無塵室訂閱者存取連結資料集時，須遵守下列條件：

* **中繼資料和權限**：您可以編輯連結資料集的部分中繼資料 (例如說明和標籤)，也可以設定連結資料集的權限。變更連結的資料集不會影響來源資料集。您無法查看檢視表定義。
* **唯讀資源**：連結資料集中的資源為唯讀。訂閱者無法編輯連結資料集中資源的資料或中繼資料，也無法指定連結資料集中個別資源的權限。
* **取消訂閱**：如要取消訂閱資料無塵室，請刪除連結的資料集。

### 查詢連結資料集中的資料

如要查詢已連結資料集中的資料，請使用 [`SELECT WITH AGGREGATION_THRESHOLD` 語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_clause)，對強制執行分析規則的檢視表執行查詢。如需這個語法的範例，請參閱「[查詢強制執行匯總門檻分析規則的檢視表](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw#view_in_privacy_query)」。

## 情境範例：廣告主和發布商歸因分析

某廣告主想追蹤行銷廣告活動的成效，廣告主擁有顧客的第一方資料，包括購買記錄、客層和興趣。發布商擁有網站資料，包括向訪客顯示的廣告和轉換。

廣告主和發布商同意使用資料無塵室合併資料，並評估廣告活動成效。在此情況下，發布商會建立資料無塵室，並提供資料供廣告主分析。產生的歸因報表會向廣告主顯示哪些廣告最能有效提升銷售量。廣告主會運用這項資訊，最佳化日後的行銷廣告活動。

廣告主和發布商會透過下列各節所述的程序，協調 BigQuery 資料無塵室。

### 建立資料無塵室 (發布商)

1. 發布商組織中的資料無塵室擁有者，在 BigQuery 專案中啟用 Analytics Hub API，並指派使用者 A 為資料無塵室擁有者 (Analytics Hub 管理員 (`roles/analyticshub.admin`))。
2. 使用者 A 建立名為 `Campaign Analysis` 的資料無塵室，並指派下列權限：
   * 資料提供者 (Analytics Hub 發布者 (`roles/analyticshub.publisher`))：使用者 B，發布者組織中的資料工程師。
   * 資料無塵室訂閱者 (Analytics Hub 訂閱者 (`roles/analyticshub.subscriber`) 和訂閱項目擁有者 (`roles/analyticshub.subscriptionOwner`))：使用者 C，廣告主機構的行銷分析師。

### 將資料新增至資料無塵室 (發布商)

使用者 B 在資料無塵室中建立名為 `Publisher Conversion Data` 的新清單。建立產品資訊時，系統會建立含有分析規則的新檢視表。

### 訂閱資料無塵室 (廣告主)

1. 使用者 C 訂閱資料無塵室，系統會為資料無塵室中的所有產品資訊 (包括 `Publisher Conversion Data` 產品資訊) 建立連結資料集。
2. 使用者 C 現在可以執行匯總查詢，將這個連結資料集的資料與第一方資料合併，評估廣告活動成效。

## 實體解析

資料無塵室用途通常需要連結資料提供者和資料無塵室訂閱者資料集中的實體，而這些資料集不含共同 ID。訂閱者和資料提供者可能會在多個資料集中以不同方式表示相同的記錄，原因可能是資料集來自不同的資料來源，或資料集使用來自不同命名空間的 ID。

BigQuery 的實體解析功能是[資料準備](#add-data)的一部分，可執行下列操作：

* 對於資料提供者，系統會使用他們選擇的一般供應商 ID，簡化及解析共用資源中的記錄。這項程序可讓跨貢獻者加入。
* 對於資料無塵室訂閱者，這項服務會簡化及解析第一方資料集中的記錄，並連結至資料貢獻者資料集中的實體。這項程序可彙整訂閱者和資料提供者的資料。

如要進一步瞭解如何設定實體解析，請參閱「[在 BigQuery 中設定及使用實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-setup?hl=zh-tw)」。

## 探索資料無塵室資產

如要找出您有權存取的所有資料無塵室，請按照下列步驟操作：

* 如果是資料無塵室擁有者和資料提供者，請前往Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

  [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

  系統會列出您可存取的所有資料無塵室。
* 資料無塵室訂閱者請按照下列步驟操作：

  1. 前往 Google Cloud 控制台的「BigQuery」頁面。

     [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
  2. 在「Explorer」窗格中，點選 add\_box「Add data」(新增資料)。
  3. 選取「Sharing (Analytics Hub)」。探索頁面隨即開啟。
  4. 如要顯示您有權存取的資料無塵室，請在篩選器清單中選取「Clean rooms」(資料無塵室)。

如要找出專案中由資料無塵室建立的所有連結資料集，請在指令列環境中執行下列指令：

```
PROJECT=PROJECT_ID; \
for dataset in $(bq ls --project_id $PROJECT | tail +3); \
do [ "$(bq show -d --project_id $PROJECT $dataset | grep -E LINKED)" ] \
&& echo $dataset; done
```

將 `PROJECT_ID` 替換為包含連結資料集的專案。

**注意：** 在「Explorer」窗格中，連結資料集的圖示也與標準資料集不同。

## 定價

下表提供 BigQuery 資料無塵室的定價摘要：

| 角色 | 定價詳細資料 |
| --- | --- |
| 資料提供者 | 僅收取[資料儲存](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)費用。 |
| 資料無塵室訂閱者 | 執行查詢時，只需支付[運算 (分析)](https://cloud.google.com/bigquery/pricing?hl=zh-tw#overview_of_pricing) 費用。 |

## 後續步驟

* 瞭解如何[使用查詢範本](https://docs.cloud.google.com/bigquery/docs/query-templates?hl=zh-tw)。
* 瞭解如何[使用分析規則限制資料存取權](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)。
* 瞭解如何[使用 VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#vpc-service-controls)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]