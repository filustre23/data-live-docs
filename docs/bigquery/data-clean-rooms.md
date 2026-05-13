Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過資料無塵室共用機密資料

資料無塵室提供安全強化環境，多方可共用、彙整及分析資料資產，不必移動或揭露基礎資料。

BigQuery 資料無塵室使用 BigQuery sharing (舊稱 Analytics Hub) 平台。標準的 [BigQuery sharing 資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)可讓您大規模跨機構共用資料，而資料無塵室則可解決共用機密和受保護資料的使用案例。資料無塵室提供額外的安全控管措施，可保護基礎資料，並強制執行資料擁有者定義的[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)。

主要用途包括：

* **廣告活動規劃和目標對象洞察。**讓兩方 (例如賣家和買家) 混合第一方資料，並以注重隱私權的方式改善資料擴充功能。
* **評估和歸因分析。**比對顧客和媒體成效資料，進一步瞭解行銷活動的成效，並做出更明智的業務決策。
* **啟用。**結合顧客資料和其他方的資料，深入瞭解顧客，進而提升區隔功能和媒體啟用成效。

資料無塵室也支援行銷產業以外的用途：

* **零售和民生消費用品業 (CPG)。**整合零售商的銷售點資料和 CPG 公司的行銷資料，進一步提升行銷和宣傳活動成效。
* **金融服務**。結合其他金融和政府機構的機密資料，提升詐欺偵測成效。彙整多間銀行的顧客資料，建立信用風險評分。
* **醫療照護。**與醫生和藥物研究人員分享資料，瞭解患者對治療的反應。
* **供應鏈、物流和運輸。**結合供應商和行銷人的資料，全面瞭解產品在整個生命週期的表現。

## 角色

BigQuery 資料無塵室有三種主要角色：

* **資料無塵室擁有者**：管理 Google Cloud 專案中一或多個資料無塵室的權限、可見度和成員資格。資料無塵室擁有者可以將資料貢獻者和資料無塵室訂閱者角色指派給使用者。這個角色類似於 [Analytics Hub 管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-admin-role) IAM 角色。
* **資料貢獻者**：將資料發布至資料無塵室。在許多情況下，資料無塵室擁有者也是資料貢獻者。這個角色類似於 [Analytics Hub 發布者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role)身分與存取權管理角色。
* **資料無塵室訂閱者**：訂閱資料無塵室中發布的資料，並對資料執行查詢。這個角色類似於[Analytics Hub 訂閱者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role)和 [Analytics Hub 訂閱項目擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriptionOwner) IAM 角色的組合。

## 架構

BigQuery 資料無塵室採用 BigQuery 資料的發布及訂閱模型。BigQuery 架構會區隔運算和儲存空間，因此資料貢獻者可以共用資料，不必建立多個資料副本。下圖顯示 BigQuery 資料無塵室架構：

#### 資料無塵室

資料無塵室是共用機密資料的環境，可防止原始存取並強制執行查詢限制。只有新增為資料無塵室訂閱者的使用者或群組，才能訂閱共用資料。資料無塵室擁有者可以在 BigQuery sharing 中建立任意數量的資料無塵室。

#### 共用資源

共用資源是資料無塵室中的資料共用單位。資源必須是 BigQuery 資料表、檢視表或常式 (資料表值函式)。資料提供者可以在專案中建立或使用現有的 BigQuery 資源，並與資料無塵室訂閱者共用。

#### 清單

資料提供者將資料新增至資料無塵室時，系統會建立資料集。當中包含資料提供者共用資源的參照，以及有助於訂閱者使用資料的說明資訊。資料貢獻者可以建立資料集，並加入說明、範例查詢和文件連結等資訊，供訂閱者參考。

#### 連結的資料集

連結的資料集是唯讀 BigQuery 資料集，做為資料無塵室中所有資料的符號連結。資料無塵室訂閱者查詢連結資料集中的資源時，系統會傳回共用資源中的資料，並符合資料提供者設定的分析規則。訂閱資料無塵室後，系統會在專案中建立連結的資料集，系統不會建立資料副本，訂閱者也無法查看特定中繼資料，例如檢視定義。

#### 分析規則

資料提供者可在資料無塵室中，對共用的資源設定分析規則。[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)可防止未經授權存取基礎資料，並強制執行查詢限制。舉例來說，資料無塵室支援[匯總門檻分析規則](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_clause)，資料無塵室訂閱者只能透過匯總查詢分析資料。

#### 資料輸出控制項

[資料輸出](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)控制項
可自動防止資料無塵室訂閱者從資料無塵室複製及匯出原始資料。資料貢獻者可以設定其他控制項，防止訂閱者複製及匯出查詢結果。

#### 查詢範本

[查詢範本](https://docs.cloud.google.com/bigquery/docs/query-templates?hl=zh-tw)
[(預覽)](https://cloud.google.com/products?hl=zh-tw#product-launch-stages) 可讓資料無塵室擁有者和 BigQuery sharing 發布者共用預先定義的查詢，不必共用資料表和檢視區塊的基礎資源。

預先定義的查詢會使用 BigQuery 中的[資料表值函式 (TVF)](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)，允許將整個資料表或特定欄位做為輸入參數傳遞，並傳回資料表做為輸出。

**警告：** 允許資料無塵室訂閱者在資料無塵室中執行任意查詢，可能會造成安全漏洞。為降低這些風險並提升資料安全性，請使用查詢範本。

## 限制

BigQuery 資料無塵室有下列限制：

* 您只能在檢視區塊中設定[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)，無法在資料表或具體化檢視區塊中設定。因此，如果資料貢獻者直接將資料表、具體化檢視表或沒有分析規則的檢視表分享到資料無塵室，資料無塵室訂閱者就能以原始格式存取這些資源中的資料。
* 由於資料無塵室使用 BigQuery 共用平台，因此適用所有 [BigQuery 共用限制](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#limitations)。
* 資料無塵室僅適用於 [BigQuery sharing 區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)。
* 資料無塵室訂閱者無法在 Knowledge Catalog 或 Data Catalog 中搜尋共用資源。
* 資料無塵室訂閱者無法在連結的資料集上查詢[`INFORMATION_SCHEMA`檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)。
* 資料提供者無法直接將整個資料集發布至資料淨室。
* 資料貢獻者無法將模型或常式 (查詢範本除外) 發布至資料無塵室。
* 資料無塵室最多可新增 100 項共用資源。如要提高這項上限，請傳送電子郵件至 [bq-dcr-feedback@google.com](mailto:bq-dcr-feedback@google.com)。
* 資料無塵室不支援多個區域的房源資訊。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者具備執行本文各項工作所需的權限、啟用 Analytics Hub API，並將 Analytics Hub 管理員角色指派給資料無塵室擁有者。

### 所需權限

如要取得使用資料無塵室所需的權限，請要求管理員授予您「[BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor) 」(`roles/bigquery.dataEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備使用資料無塵室所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用資料無塵室，必須具備下列權限：

* `serviceUsage.services.get`
* `serviceUsage.services.list`
* `serviceUsage.services.enable`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 啟用 Analytics Hub API

如要啟用 Analytics Hub API，請選取下列其中一個選項：

### 控制台

前往 **Analytics Hub API** 頁面，然後為專案啟用 API。 Google Cloud

[啟用 Analytics Hub API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### bq

執行 [`gcloud services enable` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw)：

```
gcloud services enable analyticshub.googleapis.com
```

啟用 Analytics Hub API 後，您就能存取「共用 (Analytics Hub)」頁面。

### 指派 Analytics Hub 管理員角色

資料無塵室擁有者 (也就是建立資料無塵室的使用者) 必須具備[Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-admin-role) (`roles/analyticshub.admin`)。如要瞭解如何將這個角色授予其他使用者，請參閱「[建立 BigQuery 共用管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#create-exchange-administrator)」。

## 資料無塵室擁有者工作流程

資料無塵室擁有者可以執行下列操作：

* 建立資料無塵室。
* 更新資料無塵室屬性。
* 刪除資料無塵室。
* 管理資料貢獻者。
* 管理資料無塵室訂閱者。
* 共用資料無塵室。

### 其他資料無塵室擁有者權限

您必須在專案中具備 Analytics Hub 管理員角色 (`roles/analyticshub.admin`)，才能執行資料無塵室擁有者工作。您也可以在資料夾或機構層級指派這個角色 (如適用)。

### 建立資料無塵室

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「建立資料無塵室」。
3. 在「Project」(專案) 部分，選取資料無塵室的專案。您必須為專案啟用 Analytics Hub API。
4. 指定資料無塵室的位置、名稱、主要聯絡人、圖示 (選用) 和說明。您只能列出與資料無塵室位於相同區域的資料無塵室資源。
5. 選用：如要記錄在連結資料集上執行工作和查詢的所有使用者的[主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)，請按一下「訂閱端電子郵件記錄」切換鈕。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄位中。

   **注意：** 啟用並儲存電子郵件記錄功能後，就無法編輯這項設定。如要停用電子郵件記錄功能，請刪除資料無塵室，然後重新建立，但不要點選「訂閱者電子郵件記錄」切換鈕。
6. 按一下「建立資料無塵室」。
7. 選用：在「資料無塵室權限」部分，新增其他資料無塵室擁有者、資料貢獻者或資料無塵室訂閱者。

### API

使用 [`projects.locations.dataExchanges.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/create?hl=zh-tw)，並將[共用環境](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#sharingenvironmentconfig)設為 `dcrExchangeConfig`。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.create` 方法：

```
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges?data_exchange_id=CLEAN_ROOM_ID -d
  '{
    display_name: "CLEAN_ROOM_NAME",
    sharing_environment_config: {dcr_exchange_config: {}}
  }'
```

請替換下列項目：

* `PROJECT_ID`：專案 ID
* `LOCATION`：資料無塵室的位置
* `CLEAN_ROOM_ID`：您的資料無塵室 ID
* `CLEAN_ROOM_NAME`：資料無塵室的顯示名稱

在要求主體中，提供[資料交換詳細資料](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#resource:-dataexchange)。

如果要求成功，回應主體會包含資料無塵室的詳細資料。

如果您使用 `logLinkedDatasetQueryUserEmail` 欄位啟用訂閱者電子郵件記錄功能，資料交換庫回應會包含 `log_linked_dataset_query_user_email: true`。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄位中。

### 更新資料無塵室

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要更新的資料無塵室顯示名稱。
3. 在「詳細資料」分頁中，按一下「編輯資料無塵室詳細資料」。
4. 視需要更新資料無塵室名稱、主要聯絡人、圖示、說明或訂閱者電子郵件記錄設定。

   **注意：** 啟用並儲存電子郵件記錄功能後，就無法編輯這項設定。如要停用電子郵件記錄功能，請刪除資料無塵室，然後重新建立，但不要點選「訂閱者電子郵件記錄」切換鈕。
5. 按一下 [儲存]。

### API

使用 [`projects.locations.dataExchanges.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/patch?hl=zh-tw)，並將[共用環境](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#sharingenvironmentconfig)設為 `dcrExchangeConfig`。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.patch` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X PATCH https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID?updateMask=UPDATEMASK -d
'{
  display_name: "CLEAN_ROOM_NAME",
  sharing_environment_config: {dcr_exchange_config: {}}
}'
```

請替換下列項目：

* `PROJECT_ID`：專案 ID
* `LOCATION`：資料無塵室的位置
* `CLEAN_ROOM_ID`：您的資料無塵室 ID
* `CLEAN_ROOM_NAME`：資料無塵室的顯示名稱

將 `UPDATEMASK` 替換為要更新的欄位清單。如要更新多個值，請使用以半形逗號分隔的清單。舉例來說，如要更新資料交換的顯示名稱和主要聯絡人，請輸入 `displayName,primaryContact`。

在要求主體中，為下列欄位指定更新的值：

* `displayName`
* `description`
* `primaryContact`
* `documentation`
* `icon`
* `discoveryType`
* `logLinkedDatasetQueryUserEmail`

如要瞭解這些欄位的詳細資料，請參閱「[資源：DataExchange](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#resource:-dataexchange)」。

### 刪除資料無塵室

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 在要刪除的資料無塵室資料列中，依序點按more\_vert「更多動作」>「刪除」。
3. 如要確認，請輸入 `delete`，然後按一下「刪除」。這項操作無法復原。

### API

使用 [`projects.locations.dataExchanges.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/delete?hl=zh-tw)，並將[共用環境](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#sharingenvironmentconfig)設為 `dcrExchangeConfig`。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.delete` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X DELETE https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges?data_exchange_id=CLEAN_ROOM_ID
```

請替換下列項目：

* `PROJECT_ID`：專案 ID
* `LOCATION`：資料無塵室的位置
* `CLEAN_ROOM_ID`：您的資料無塵室 ID
* `CLEAN_ROOM_NAME`：資料無塵室的顯示名稱

刪除資料無塵室後，當中的所有房源都會一併刪除。
但共用資源和連結資料集不會刪除。連結的資料集會與來源資料集取消連結，因此資料無塵室訂閱者開始無法查詢資料無塵室中的資源。

### 管理資料貢獻者

資料無塵室擁有者可以管理哪些使用者能將資料新增至資料無塵室 (即資料貢獻者)。如要允許使用者在資料無塵室中新增資料，請在特定資料無塵室中授予他們 [Analytics Hub 發布商角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) (`roles/analyticshub.publisher`)：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要授予權限的資料無塵室顯示名稱。
3. 在「詳細資料」分頁中，按一下「設定權限」。
4. 按一下「Add principal」(新增主體)。
5. 在「New principals」(新增主體) 中，輸入要新增的資料貢獻者使用者名稱或電子郵件地址。
6. 在「選取角色」部分，依序選取「Analytics Hub」>「Analytics Hub 發布者」。
7. 按一下 [儲存]。

您隨時可以點選「設定權限」，刪除及更新資料貢獻者。

### API

請使用 [`projects.locations.dataExchanges.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/setIamPolicy?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.setIamPolicy` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID:setIamPolicy -d
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

要求主體中的政策應符合 [Policy](https://docs.cloud.google.com/iam/reference/rest/v1/Policy?hl=zh-tw) 的結構。

您可以從 [IAM 頁面](https://console.cloud.google.com/iam-admin?hl=zh-tw)授予整個專案的 Analytics Hub 發布者角色 (`roles/analyticshub.publisher`)，讓使用者有權在專案中將資料新增至任何資料無塵室。不過，我們不建議這麼做，因為這可能會導致使用者擁有過於寬鬆的存取權。

### 管理資料無塵室訂閱者

資料無塵室擁有者可以管理哪些使用者能訂閱資料無塵室 (即訂閱者)。如要允許使用者訂閱資料無塵室，請在特定資料無塵室中，授予使用者「Analytics Hub 訂閱者」角色 (`roles/analyticshub.subscriber`) 和「Analytics Hub 訂閱擁有者」角色 (`roles/analyticshub.subscriptionOwner`)：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要授予權限的資料無塵室顯示名稱。
3. 在「詳細資料」分頁中，按一下「設定權限」。
4. 按一下「Add principal」(新增主體)。
5. 在「New principals」(新增主體) 中，輸入要新增的資料無塵室訂閱者使用者名稱或電子郵件地址。
6. 在「選取角色」部分，依序選取「Analytics Hub」>「Analytics Hub 訂閱者」。
7. 按一下
   add\_box
   「Add another role」(新增其他角色)。
8. 在「選取角色」部分，依序選取「Analytics Hub」>「Analytics Hub 訂閱項目擁有者」。
9. 按一下 [儲存]。

如要隨時刪除及更新訂閱者，請按一下「設定權限」。

### API

請使用 [`projects.locations.dataExchanges.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/setIamPolicy?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.setIamPolicy` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID:setIamPolicy -d
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

要求主體中的政策應符合 [Policy](https://docs.cloud.google.com/iam/reference/rest/v1/Policy?hl=zh-tw) 的結構。

您可以透過[「IAM」頁面](https://console.cloud.google.com/iam-admin?hl=zh-tw)，授予整個專案的 Analytics Hub 訂閱者角色 (`roles/analyticshub.subscriber`) 和 Analytics Hub 訂閱擁有者角色 (`roles/analyticshub.subscriptionOwner`)，讓使用者有權訂閱專案中的任何資料無塵室。不過，我們不建議這麼做，因為這可能會導致使用者擁有過於寬鬆的存取權。

### 共用資料無塵室

您可以直接與訂閱者共用資料無塵室：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 在要共用的資料無塵室資料列中，依序點選 more\_vert「更多動作」**>「複製共用連結」**。
3. 將複製的連結分享給資料無塵室訂閱者，讓他們查看及訂閱資料無塵室。

## 資料貢獻者工作流程

資料貢獻者可以執行下列操作：

* 建立房源，將資料新增至資料無塵室。
* 更新產品資訊。
* 刪除房源資訊。
* 共用資料無塵室。
* 監控商家資訊。

### 其他資料貢獻者權限

如要執行資料貢獻者工作，您必須在資料無塵室中具備 [Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) (`roles/analyticshub.publisher`)。

如要執行資料貢獻者工作，您也需要來源資料集和資料表的 `bigquery.datasets.get`、`bigquery.datasets.update` 和 `bigquery.tables.get` 權限。這些權限屬於 [BigQuery 資料擁有者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner) (`roles/bigquery.dataOwner`)。

如要查看機構中不屬於目前專案的資料無塵室，您需要具備 `resourcemanager.organization.get` 權限。

如要使用資料無塵室建立程序，透過[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)建立 [BigQuery 檢視畫面](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw#creating_a_view)，您需要 `bigquery.tables.setPrivacyPolicy` 和 `bigquery.tables.create` 權限。如果直接參照檢視區塊，則不需要這項權限。

### 建立商家資訊 (新增資料)

**注意：** 如果協作環境需要通用 ID，才能在資料貢獻者和資料無塵室訂閱者資料集之間聯結資料，請先設定[實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-setup?hl=zh-tw)，再按照下列步驟操作。

如要使用[數據分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)準備資料，並以清單形式發布至資料無塵室，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要建立商家資訊的資料無塵室顯示名稱。

   如果您的機構與資料無塵室擁有者不同，且您看不到資料無塵室，請向資料無塵室擁有者索取直接連結。
3. 按一下「新增資料」。
4. 在「選取資料集」和「資料表/檢視表名稱」部分，輸入要在資料無塵室中列出的資料表或檢視表，以及對應的資料集。您將新增分析規則，防止以原始形式存取這項基礎資料，步驟如下：
5. 選取要發布的資源資料欄。
6. 設定房源的檢視畫面名稱、主要聯絡人和說明 (選填)。
7. 點選「下一步」。
8. 為房源選擇分析規則，並設定詳細資料。
9. 為房源設定[資料外流](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)控管機制。
10. 點選「下一步」。
11. 請檢查要新增至資料無塵室的資料和分析規則。
12. 按一下「新增資料」。系統會為您的資料建立檢視區塊，並新增為資料無塵室的項目。系統不會新增來源資料表或檢視表本身。

### API

請使用 [`projects.locations.dataExchanges.listings.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/create?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.listings.create` 方法：

```
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X POST https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/listings?listingId=LISTING_ID -d
  '{"bigqueryDataset":{"dataset":"projects/PROJECT_ID/datasets/DATASET_ID","selectedResources":[{"table":"projects/PROJECT_ID/datasets/DATASET_ID/tables/VIEW_ID"}],},"displayName":LISTING_NAME"}'
```

請替換下列項目：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `PROJECT_ID`：來源資料集所屬專案的專案 ID。
* `DATASET_ID`：來源資料集 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：您的資料無塵室 ID。
* `LISTING_ID`：您的房源 ID。
* `LISTING_NAME`：商家檔案名稱。
* `VIEW_ID`：您的檢視區塊 ID。新增至資料無塵室的檢視區塊必須是已設定[分析規則](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)的[授權檢視區塊](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。

在資料無塵室中列出資源，即表示您授予所有現有和未來的資料無塵室訂閱者，存取共用資源中資料的權限。

如果您嘗試使用沒有分析規則的共用資源建立項目，系統會顯示警告，提醒訂閱者可以存取該資源的原始資料。如果您確認要發布這類資源，且不使用分析規則，仍可建立商家資訊。

如果收到 `Failed to save listing` 錯誤訊息，請確認您[具備執行資料貢獻者工作的必要權限](#additional_data_contributor_permissions)。

### 更新產品資訊

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有房源的資料無塵室顯示名稱。
3. 在要更新的房源所在列中，依序點選 more\_vert「更多動作」>「編輯房源」。
4. 視需要更新主要聯絡人或說明。
5. 點選「下一步」。
6. 視需要更新分析規則。您只能更新所選規則的參數。你無法切換至其他規則。
7. 點選「下一步」。
8. 查看商家資訊，然後按一下**新增資料**。

### API

請使用 [`projects.locations.dataExchanges.listings.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/patch?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.listings.patch` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X PATCH https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/listings/listingId=LISTING_ID?updateMask=displayName -d
'{"displayName":LISTING_NAME"}'
```

請替換下列項目：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：您的資料無塵室 ID。
* `LISTING_ID`：您的房源 ID。
* `LISTING_NAME`：商家檔案名稱。

建立項目後，就無法變更來源資源或資料輸出控管設定。

### 刪除產品資訊

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有房源的資料無塵室顯示名稱。
3. 在要刪除的房源資料列中，依序點選more\_vert「更多動作」**>「刪除房源」**。
4. 如要確認，請輸入 `delete`，然後按一下「刪除」。這項操作無法復原。

### API

請使用 [`projects.locations.dataExchanges.listings.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/delete?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.listings.delete` 方法：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -H 'x-goog-user-project:DCR_PROJECT_ID' -X DELETE https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID/listings?listingId=LISTING_ID
```

請替換下列項目：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：您的資料無塵室 ID。
* `LISTING_ID`：您的房源 ID。

刪除房源資訊時，系統不會刪除共用資源和連結的資料集。連結的資料集會與來源資料集取消連結，因此資料無塵室訂閱者開始無法查詢該清單中的資料。

### 共用資料無塵室

您可以直接與資料無塵室訂閱者共用資料無塵室：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 在要共用的資料無塵室資料列中，依序點選 more\_vert「更多動作」**>「複製共用連結」**。
3. 將複製的連結分享給訂閱者，讓他們查看及訂閱資料無塵室。

### 監控房源

如要查看您在資料無塵室中分享的資源，其來源資料集的用量指標，請查詢 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)。

如要查看產品資訊資料無塵室訂閱者，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下資料無塵室的顯示名稱。
3. 在要查看的商品資訊列中，依序點選 more\_vert「更多動作」>「查看訂閱項目」。

## 資料無塵室訂閱者工作流程

訂閱者可以查看及訂閱資料無塵室。訂閱資料無塵室後，系統會在訂閱者的專案中建立一個連結的資料集。每個連結的資料集都與資料無塵室同名。

您無法訂閱資料無塵室中的特定資料清單。您只能訂閱資料無塵室本身。

### 其他訂閱者權限

您必須在資料無塵室中具備 [Analytics Hub 訂閱者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`) 角色，且在訂閱專案中具備 [Analytics Hub 訂閱項目擁有者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscription-owner-role) (`roles/analyticshub.subscriptionOwner`) 角色，才能執行訂閱者工作。

此外，訂閱資料無塵室時，您必須在專案中具備 `bigquery.datasets.create` 權限，才能建立連結的資料集。

### 訂閱資料無塵室

訂閱資料無塵室後，您就能在專案中建立連結的資料集，並查詢商家資訊中的資料。如要訂閱資料淨室，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下
   add\_box
   「新增資料」。
3. 選取「Sharing (Analytics Hub)」。系統隨即會開啟探索頁面。
4. 如要顯示您有權存取的資料無塵室，請在篩選器清單中選取「資料無塵室」。
5. 按一下要訂閱的資料無塵室。系統會開啟資料無塵室的說明頁面。這個頁面也會顯示供應商是否已啟用訂閱者電子郵件記錄功能。
6. 按一下「訂閱」。
7. 選取訂閱項目的目標專案，然後按一下「訂閱」。

### API

請使用 [`projects.locations.dataExchanges.subscribe` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/subscribe?hl=zh-tw)。

以下範例說明如何使用 `curl` 指令呼叫 `projects.locations.dataExchanges.subscribe` 方法：

```
  curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X POST https://analyticshub.googleapis.com/v1/projects/DCR_PROJECT_ID/locations/LOCATION/dataExchanges/CLEAN_ROOM_ID:subscribe  --data '{"destination":"projects/SUBSCRIBER_PROJECT_ID/locations/LOCATION","subscription":"SUBSCRIPTION"}'
```

請替換下列項目：

* `DCR_PROJECT_ID`：建立資料無塵室的專案 ID。
* `SUBSCRIBER_PROJECT_ID`：訂閱者專案的專案 ID。
* `LOCATION`：資料無塵室的位置。
* `CLEAN_ROOM_ID`：您的資料無塵室 ID。
* `SUBSCRIPTION`：訂閱方案名稱。

在要求主體中，指定要建立[連結資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)的資料集。
如果要求成功，回應主體會包含[訂閱物件](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/subscribe?hl=zh-tw#response-body)。

如果您使用 `logLinkedDatasetQueryUserEmail` 欄位為資料無塵室啟用訂閱者電子郵件記錄功能，訂閱回應會包含 `log_linked_dataset_query_user_email: true`。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面的 `job_principal_subject` 欄位中](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)。

連結的資料集現已新增至您指定的專案，可供查詢。

資料無塵室訂閱者可以編輯連結資料集的某些中繼資料，例如說明和標籤。您也可以為連結的資料集設定權限。不過，連結資料集的變更不會影響來源資料集。您也無法查看檢視畫面定義。

連結資料集中包含的資源為唯讀。訂閱者無法編輯連結資料集中資源的資料或中繼資料。您也無法為連結資料集中的個別資源指定權限。

如要取消訂閱資料無塵室，請刪除連結的資料集。

#### 查詢已連結資料集中的資料

如要查詢連結資料集中的資料，請使用 [`SELECT WITH AGGREGATION_THRESHOLD` 語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_clause)，以便對強制執行分析規則的檢視區塊執行查詢。如需這類語法的範例，請參閱「[查詢匯總門檻分析規則 - 強制執行的檢視畫面](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw#view_in_privacy_query)」。

## 情境範例：廣告主和發布商歸因分析

某廣告主想追蹤行銷廣告活動的成效，廣告主擁有顧客的第一方資料，包括購買記錄、受眾特徵和興趣。發布商擁有網站資料，包括向訪客顯示的廣告和轉換。

廣告主和發布商同意使用資料無塵室合併資料，並評估廣告活動成效。在本例中，發布商會建立資料無塵室，並開放廣告主使用資料進行分析。歸因報表會顯示哪些廣告最能有效提高銷售量，廣告主可以運用這項資訊，改善日後的行銷廣告活動。

廣告主和發布商會透過下列各節所述程序，協調 BigQuery 資料無塵室。

### 建立資料無塵室 (發布商)

1. 發布商機構的資料無塵室擁有者會在 BigQuery 專案中啟用 Analytics Hub API，並將使用者 A 指派為資料無塵室擁有者 (Analytics Hub 管理員 (`roles/analyticshub.admin`))。
2. 使用者 A 建立名為「`Campaign Analysis`」的資料無塵室，並指派下列權限：
   * 資料貢獻者 (Analytics Hub 發布者 (`roles/analyticshub.publisher`))：
     使用者 B，發布者機構的資料工程師。
   * 資料無塵室訂閱者 (Analytics Hub 訂閱者 (`roles/analyticshub.subscriber`) 和訂閱項目擁有者 (`roles/analyticshub.subscriptionOwner`))：
     使用者 C，廣告主機構的行銷分析師。

### 將資料新增至資料無塵室 (發布商)

1. 使用者 B 在名為 `Publisher Conversion Data` 的資料無塵室中建立新項目。建立商家資訊時，系統會建立含有分析規則的新檢視畫面。

### 訂閱資料無塵室 (廣告主)

1. 使用者 C 訂閱資料無塵室，系統會為資料無塵室中的所有房源建立連結的資料集，包括「`Publisher Conversion Data`」房源。
2. 使用者 C 現在可以執行匯總查詢，將這個已連結資料集的資料與第一方資料合併，評估廣告活動成效。

## 實體解析

資料無塵室的應用實例通常需要連結資料貢獻者和資料無塵室訂閱者資料集中的實體，但這些資料集不包含通用 ID。訂閱者和資料貢獻者可能會在多個資料集中以不同方式表示相同記錄，原因可能是資料集來自不同資料來源，或是資料集使用不同命名空間的 ID。

在[資料準備](#add-data)過程中，BigQuery 中的實體解析功能會執行下列操作：

* 對於資料提供者，系統會使用所選通用供應商的 ID，在共用資源中重複資料並解決記錄。這個程序可讓不同貢獻者加入。
* 對於資料無塵室訂閱者，這項功能會將第一方資料集中的記錄去重並解析，然後連結至資料貢獻者資料集中的實體。這個程序可讓訂閱者和資料提供者資料之間進行聯結。

如要使用所選的識別資訊提供者設定實體解析，請參閱[在 BigQuery 中設定及使用實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-setup?hl=zh-tw)。

## 探索資料無塵室資產

如要找出您有權存取的所有資料無塵室，請按照下列步驟操作：

* 資料無塵室擁有者和資料貢獻者可以在Google Cloud 控制台前往「Sharing (Analytics Hub)」頁面。

  [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

  系統會列出您可存取的所有資料無塵室。
* 資料無塵室訂閱者請按照下列步驟操作：

  1. 前往 Google Cloud 控制台的「BigQuery」頁面。

     [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
  2. 在「Explorer」窗格中，按一下
     add\_box
     「新增資料」。
  3. 選取「Sharing (Analytics Hub)」。系統隨即會開啟探索頁面。
  4. 如要顯示您有權存取的資料無塵室，請在篩選器清單中選取「資料無塵室」。

如要找出專案中由資料無塵室建立的所有連結資料集，請在指令列環境中執行下列指令：

```
PROJECT=PROJECT_ID \
for dataset in $(bq ls --project_id $PROJECT | tail +3); \
do [ "$(bq show -d --project_id $PROJECT $dataset | egrep LINKED)" ] \
&& echo $dataset; done
```

請將 `PROJECT_ID` 替換為包含連結資料集的專案。

**注意：** 在「Explorer」窗格中，連結的資料集也會顯示與標準資料集不同的圖示。

## 定價

資料貢獻者只需支付[資料儲存](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)費用。資料無塵室訂閱者只有在執行查詢時，才需要支付[運算 (分析)](https://cloud.google.com/bigquery/pricing?hl=zh-tw#overview_of_pricing)費用。

## 後續步驟

* 瞭解如何[使用查詢範本](https://docs.cloud.google.com/bigquery/docs/query-templates?hl=zh-tw)。
* 瞭解如何[使用分析規則限制資料存取權](https://docs.cloud.google.com/bigquery/docs/analysis-rules?hl=zh-tw)。
* 瞭解如何[使用 VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#vpc-service)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]