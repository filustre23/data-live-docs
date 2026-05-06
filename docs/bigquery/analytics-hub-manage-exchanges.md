Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理資料交換

本文說明如何在 BigQuery sharing (舊稱 Analytics Hub) 中管理資料交易所。身為 BigQuery sharing 管理員，您可以執行下列操作：

* 建立、更新、查看、分享及刪除[資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)。
* 建立、更新、刪除及共用房源資訊。
* 管理 BigQuery sharing 管理員、清單管理員、發布者、訂閱者和檢視者。

資料交換預設為私密。只有具備交易所存取權的使用者或群組，才能查看或訂閱交易所的資料。您可以要求[公開資料交換](#make-data-exchange-public)。將資料交換作業設為公開，[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 就能[探索](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)及[訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)清單。

## 事前準備

如要開始使用 BigQuery sharing (舊稱 Analytics Hub)，請在專案中啟用 Analytics Hub API。 Google Cloud

如要啟用 Analytics Hub API，您需要下列 Identity and Access Management (IAM) 權限：

* `serviceUsage.services.get`
* `serviceUsage.services.list`
* `serviceUsage.services.enable`

以下是具有啟用 Analytics Hub API 所需權限的預先定義 IAM 角色：

* [服務使用情形管理員](https://docs.cloud.google.com/service-usage/docs/access-control?hl=zh-tw#serviceusage.serviceUsageAdmin) (`roles/serviceusage.serviceUsageAdmin`)

如要啟用 Analytics Hub API，請選取下列其中一個選項：

### 控制台

前往 **Analytics Hub API** 頁面，為專案啟用 Analytics Hub API。 Google Cloud

[啟用 Analytics Hub API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### gcloud

執行 [gcloud services enable](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw) 指令：

```
gcloud services enable analyticshub.googleapis.com
```

### 必要的角色

如要取得管理資料交換庫所需的權限，請要求系統管理員授予您專案的 [Analytics Hub 管理員角色](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.admin)  (`roles/analyticshub.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立資料交換庫

**注意：** 請勿在具有 VPC Service Controls perimeter 的 Google Cloud 專案中建立資料交換。如果這麼做，您必須新增適當的[輸入和輸出規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw#create_a_data_exchange)。

如要建立資料交換庫，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下 add\_box「建立兌換」。
3. 在「建立交換庫」對話方塊中，選取資料交換庫的「專案」和「區域」。建立資料交換後，就無法更新專案和區域。
4. 在「顯示名稱」欄位中，輸入資料交易所的名稱。
5. 選用：在下列欄位中輸入值：

   * **主要聯絡人**：輸入資料交換的主要聯絡人網址或電子郵件地址。
   * **說明**：輸入資料交易的說明。
6. 如要記錄在連結資料集上執行工作和查詢的所有使用者[主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)，請按一下「訂閱端電子郵件記錄」切換鈕。啟用這個選項後，資料交換庫中所有未來的清單項目都會啟用訂閱者電子郵件記錄功能。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視區塊的 `job_principal_subject` 欄位中。](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)

   **注意：** 啟用並儲存電子郵件記錄功能後，就無法編輯這項設定。如要停用電子郵件記錄功能，請刪除資料交換庫，然後重新建立，但不要點選「訂閱端電子郵件記錄」切換鈕。
7. 如要啟用公開可偵測性，請點選「公開可偵測性」切換按鈕。如果交換庫可供公開搜尋，目錄中就會顯示交換庫中的所有項目，且可供搜尋。啟用公開探索功能後，請設定交換權限。根據預設，所有清單都會沿用資料交換的開放搜尋設定。這表示公開交易平台無法有私人清單項目，但私人交易平台可以有公開清單項目。您可以在個別房源資訊層級設定公開探索類型。建立資料交換的專案必須有相關聯的機構和帳單帳戶。
8. 按一下「建立交易」。
9. 選用步驟：在「Exchange Permissions」(Exchange 權限) 部分，完成下列步驟：

   1. 在下列欄位中輸入電子郵件地址，即可授予 Identity and Access Management (IAM) 角色：

      * **管理員**：為這些使用者指派 [Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-admin-role) (`roles/analyticshub.admin`)。
      * **發布者**：將 [Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) (`roles/analyticshub.publisher`) 指派給這些使用者。如要瞭解 BigQuery sharing 發布端可執行的工作，請參閱「[管理清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)」。
      * **訂閱者**：將 [Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`) 指派給這些使用者。如要瞭解 BigQuery sharing 訂閱者可以執行的工作，請參閱「[查看及訂閱清單和資料交易所](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)」。
      * **檢視者**：為這些使用者指派 [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.viewer`)。BigQuery 分享檢視者可以[查看房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。

        如果啟用公開探索功能，請將 Analytics Hub 檢視者角色授予 `allUsers` 或 `allAuthenticatedUsers`。
   2. 如要儲存權限，請按一下「設定權限」。
10. 如果未設定資料交換的權限，請按一下「略過」。

### API

請使用 [`projects.locations.dataExchanges.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/create?hl=zh-tw)。

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges?dataExchangeId=DATAEXCHANGE_ID
```

更改下列內容：

* `PROJECT_ID`：您要在當中建立資料交換的專案 ID。
* `LOCATION`：資料交換庫的位置。如要進一步瞭解支援 BigQuery sharing 的位置，請參閱[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)。
* `DATAEXCHANGE_ID`：資料交換庫的 ID。

在要求主體中，提供[資料交換詳細資料](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#resource:-dataexchange)。

如果要求成功，回應主體會包含資料交換的詳細資料。

如果您使用 `logLinkedDatasetQueryUserEmail` 欄位啟用訂閱者電子郵件記錄功能，資料交換回應會包含 `log_linked_dataset_query_user_email: true`。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視區塊的 `job_principal_subject` 欄位中](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)。

如要進一步瞭解如何使用 API 對資料交易所執行工作，請參閱 [`projects.locations.dataExchanges` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#methods)。

## 更新資料交換

如要更新資料交換庫，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 從資料交換清單中，選取要更新的資料交換。
3. 前往「詳細資料」分頁。
4. 按一下「編輯兌換」mode\_edit。
5. 在「編輯交易所」對話方塊中，更新下列欄位：

   * **顯示名稱**
   * **主要聯絡人**
   * **說明**
   * **開放搜尋**
     + 如要啟用公開探索功能，請將 Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`) 授予 `allUsers` 或 `allAuthenticatedUsers`。
     + 如要停用公開探索功能，請從 `allUsers` 或 `allAuthenticatedUsers` 移除 Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。公開交易平台無法提供私人房源，但私人交易平台可以提供公開房源。
   * **訂閱端電子郵件記錄**

     **注意：** 啟用並儲存電子郵件記錄功能後，就無法編輯這項設定。如要停用電子郵件記錄功能，請刪除資料交換庫，然後重新建立，但不要點選「訂閱端電子郵件記錄」切換鈕。
6. 按一下 [儲存]。

### API

請使用 [`projects.locations.dataExchanges.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/patch?hl=zh-tw)。

```
PATCH https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID?updateMask=UPDATEMASK
```

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

如要進一步瞭解如何使用 API 對資料交易所執行工作，請參閱 [`projects.locations.dataExchanges` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#methods)。

## 查看資料交換庫

如要查看您有權存取的專案或機構資料交換庫，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 這個頁面會顯示 Google Cloud 專案中的資料交換。如果您擁有 `resourcemanager.organizations.get` 權限，也可以查看 Google Cloud 機構中的資料交換。

### API

如要查看專案中的資料交換，請使用 [`projects.locations.dataExchanges.list` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/list?hl=zh-tw)：

```
GET https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges
```

更改下列內容：

* PROJECT\_ID：專案 ID。
* LOCATION：要列出現有資料交易所的位置。

如要查看貴機構的資料交換活動，請使用 [`organizations.locations.dataExchanges.list` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/organizations.locations.dataExchanges/list?hl=zh-tw)：

```
GET https://analyticshub.googleapis.com/v1/organizations/ORGANIZATION_ID/location/LOCATION/dataExchanges
```

更改下列內容：

* `ORGANIZATION_ID`：機構 ID。詳情請參閱「[取得機構 ID](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw#retrieving_your_organization_id)」。
* `LOCATION`：要列出現有資料交易所的位置。

## 共用資料交換庫

如果 BigQuery sharing 發布者所屬的機構與資料交換庫所屬的機構不同，發布者就無法在 BigQuery sharing 中[查看您的資料交換庫](#view_data_exchanges)。與發布商共用資料交換連結。

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 在資料交換清單中，按一下「更多選項」more\_vert。
3. 按一下「複製共用連結」content\_copy。

## 授予使用者資料交換存取權

如要授予使用者資料交換存取權，您必須為該資料交換設定 IAM 政策。如要瞭解預先定義的 IAM 使用者角色，請參閱「[BigQuery sharing IAM 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#user_roles)」。

**注意：**
管理[外部身分識別資訊提供者](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)中使用者存取權時，請將 Google 帳戶主體 ID (例如 `user:kiran@example.com`、`group:support@example.com` 和 `domain:example.com`) 替換為適當的[員工身分聯盟主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。

### 控制台

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下要設定權限的資料交換名稱。
3. 前往「詳細資料」分頁。
4. 按一下「設定權限」person。
5. 如要新增主體，請按一下「新增主體」person\_add。
6. 在「New principals」(新增主體) 欄位中，新增要授予存取權的電子郵件 ID。您也可以使用 `allUsers` 將資源設為公開，讓網際網路上的所有人都能存取，或使用 `allAuthenticatedUsers` 將資源設為僅供登入 Google 的使用者存取。
7. 在「Select a role」(請選擇角色) 選單中選取「Analytics Hub」(資料分析中心)，然後選取下列任一 Identity and Access Management (IAM) 角色：

   * **Analytics Hub 管理員**
   * **Analytics Hub 清單管理員**
   * **Analytics Hub 發布者**
   * **Analytics Hub 訂閱者**
   * **Analytics Hub 訂閱項目擁有者**
   * **Analytics Hub 檢視者**
8. 按一下 [儲存]。

### API

1. 使用 [`projects.locations.dataExchanges.getIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/getIamPolicy?hl=zh-tw)，透過清單 `getIamPolicy` 方法讀取現有政策：

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID:getIamPolicy
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID，例如 `my-project-1`。
   * `LOCATION`：資料交換的位置。使用小寫英文字母。
   * `DATAEXCHANGE_ID`：資料交換 ID。

   BigQuery sharing (舊稱 Analytics Hub) 會傳回目前的政策。
2. 如要新增或移除成員及其相關聯的身分與存取權管理 (IAM) 角色，請使用文字編輯器編輯政策。請使用下列格式新增成員：

   * `user:test-user@gmail.com`
   * `group:admins@example.com`
   * `serviceAccount:test123@example.domain.com`
   * `domain:example.domain.com`

   舉例來說，如要將 `roles/analyticshub.subscriber` 角色授予 `group:subscribers@example.com`，請在政策中新增下列繫結：

   ```
   {
    "members": [
      "group:subscribers@example.com"
    ],
    "role":"roles/analyticshub.subscriber"
   }
   ```
3. 使用 [`projects.locations.dataExchanges.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/setIamPolicy?hl=zh-tw)寫入更新後的政策。在要求主體中，提供上一個步驟中更新的 IAM 政策。

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID:setIamPolicy
   ```

   在要求主體中提供房源詳細資料。如果要求成功，回應主體會包含房源詳細資料。

### 建立 BigQuery 共用管理員

如要管理資料交換，請授予使用者「Analytics Hub 管理員」角色 (`roles/analyticshub.admin`)，在專案或資料交換層級建立資料交換管理員。

如要允許管理員管理專案中的所有資料交換，請[為該專案授予 Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-project)。

如要允許管理員管理特定資料交換，請[授予他們該資料交換的 Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-data-exchange)。

## 公開資料交換庫

資料交換預設為私密。只有具備交換庫存取權的使用者或群組，才能查看或訂閱交換庫的刊登內容。您可以將資料交換設為公開，讓[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 探索及訂閱其中的清單。

如要公開資料交換庫，請按照下列步驟操作：

1. 如要允許 `allAuthenticatedUsers`[查看產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)，請在資料交換庫層級授予 Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。
2. 如要允許 `allAuthenticatedUsers`[訂閱商家資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)，請在資料交換庫層級授予 Analytics Hub 訂閱者角色 (`roles/analyticshub.subscriber`)。
3. [建立](#create-exchange)或[更新](#update-exchange)資料交換庫時，啟用公開探索功能。公開資料交換時，請指定適當的權限。

**注意：** 你也可以將公開資料交換轉換為私人資料交換。如要這麼做，請從資料交換庫的權限清單中移除 `allAuthenticatedUsers`。

## 刪除資料交換

刪除資料交換庫也會一併刪除所有產品資訊。不過，共用和連結的資料集不會刪除。刪除專案時，系統不會刪除資料交換。請先刪除這些資料交換，再[刪除專案](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw#shutting_down_projects)。
資料交換刪除後即無法復原。

刪除資料交換前，請根據資料交換的設定完成下列步驟：

* 如要進行資料交換，請[停用與 Cloud Marketplace 整合的商用產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw#offboard-listing)。
* 如要與多個地區的房源進行資料交換，請[使用 `projects.locations.subscriptions.revoke` 方法移除所有有效訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#revoke-subscription)。

如要刪除資料交換庫，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 從資料交換庫清單中，選取要刪除的資料交換庫。
3. 前往「詳細資料」分頁。
4. 按一下 delete「刪除兌換項目」。
5. 在「要刪除對話嗎？」對話方塊中輸入「刪除」，確認要刪除對話。
6. 點選「刪除」。

### API

請使用 [`projects.locations.dataExchanges.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/delete?hl=zh-tw)。

```
DELETE https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID
```

更改下列內容：

* `PROJECT_ID`：您要在當中建立資料交換的專案 ID。
* `LOCATION`：資料交換庫的位置。如要進一步瞭解支援 BigQuery sharing 的位置，請參閱[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)。
* `DATAEXCHANGE_ID`：資料交換庫的 ID。

如要進一步瞭解如何使用 API 對資料交易所執行工作，請參閱 [`projects.locations.dataExchanges` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges?hl=zh-tw#methods)。

## 後續步驟

* 瞭解如何[管理房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)。
* 瞭解如何[授予 Analytics Hub 使用者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw)。
* 瞭解如何[查看及訂閱清單和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。
* 瞭解[共用稽核記錄](https://docs.cloud.google.com/bigquery/docs/analytics-hub-audit-logging?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]