Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理清單

本文說明如何在 BigQuery sharing (舊稱 Analytics Hub) 中管理清單。身為 BigQuery 共用發布者，您可以執行下列操作：

* 在您有發布權限的資料交換庫中建立房源資訊。
* 更新、刪除、分享及查看房源的使用指標。
* 管理清單的不同 BigQuery sharing 角色，例如清單管理員、訂閱者和檢視者。
* 查看所有訂閱你房源的使用者。
* [監控商家資訊的使用情況](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw)。
* 從房源資訊中移除訂閱者。

清單是發布者在[資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)中列出的共用資料集參照資訊。根據為房源設定的 Identity and Access Management (IAM) 政策，以及包含房源的資料交換庫類型，房源可分為下列兩種：

* **公開產品資訊。**[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 可以[探索](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)及[訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)公開清單。公開資料交換中的清單就是公開清單。這些清單可以是*免費公開資料集*或*商業資料集*的參照。如果資訊是商業資料集，BigQuery sharing 訂閱者可以直接向資料供應商要求存取資訊，也可以瀏覽及購買[整合 Google Cloud Marketplace 的商業資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)。
* **私人房源**。私人房源資訊會直接分享給個人或群組。舉例來說，私人房源資訊可以參照您與機構內其他內部團隊共用的行銷指標資料集。即使您可以
  [允許 Google Cloud 使用者 (`allAuthenticatedUsers`)](#give_users_access_to_a_listing) 訂閱您的項目，該項目仍會維持私密狀態，且
  [不會顯示在 BigQuery sharing 頁面上的公開項目清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。如要與使用者分享這類房源資訊，請將房源網址提供給他們。如要讓私人產品資訊可供搜尋，請[公開交易所](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)。

**注意：** 單一 BigQuery 共用項目同時支援要求存取權和 Cloud Marketplace 整合流程。也就是說，您可以從現有的 (離線) 商業產品資訊建立與 Cloud Marketplace 整合的產品資訊，現有訂閱項目不會受到任何影響。

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

如要管理項目和訂閱項目，您必須具備下列任一 BigQuery sharing Identity and Access Management (IAM) 角色：

* [Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.publisher) (`roles/analyticshub.publisher`)，可讓您建立、更新、刪除及設定項目 IAM 政策。
* [Analytics Hub 清單管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.listingAdmin) (`roles/analyticshub.listingAdmin`)，可讓您更新、刪除及設定清單的 IAM 政策。
* [Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.admin) (`roles/analyticshub.admin`)，可讓您在資料交換庫中建立、更新、刪除及設定所有資源的 IAM 政策。

詳情請參閱「[BigQuery sharing IAM 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#user_roles)」。如要瞭解如何將這些角色授予其他使用者，請參閱「[建立房源管理員](#create-listing-administrator)」。

如要建立產品資訊或更新產品資訊的副本區域，您必須擁有要建立或更新產品資訊之資料集的 `bigquery.datasets.get` 和 `bigquery.datasets.update` 權限。下列 [BigQuery 預先定義角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)包含 `bigquery.datasets.update` 權限：

* [BigQuery 資料擁有者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner)
  (`roles/bigquery.dataOwner`)
* [BigQuery 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)
  (`roles/bigquery.admin`)

如要查看您有權存取的機構中所有專案的資料交換，您必須具備 `resourcemanager.organizations.get` 權限。沒有包含這項權限的 [BigQuery 預先定義角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)，因此您需要使用 [IAM 自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。

## 查看資料交換庫

如要查看您有權存取的機構資料交換清單，請參閱「[查看資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#view_data_exchanges)」。如果資料交換庫位於其他機構，BigQuery sharing 管理員必須[與您分享該資料交換庫的連結](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#share_a_data_exchange)。

## 建立產品資訊

清單是 BigQuery sharing 發布端在資料交換庫中列出的[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)參照資訊。

**注意：** 建議您不要在具有 VPC Service Controls perimeter 的Google Cloud 專案中新增共用資料集。如果這麼做，您就必須新增適當的[輸入和輸出規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw#create_a_listing)。

如要建立房源資訊，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

   畫面上會顯示您可存取的所有資料交換。
2. 按一下要建立刊登的資料交易所名稱。
3. 按一下 add\_box「建立商店資訊」。
4. 在「設定資料」部分，選取「資源類型」選單中的「BigQuery 資料集」或「Pub/Sub 主題」。

   * 如果選取「BigQuery 資料集」，請執行下列操作：

     1. 在「共用資料集」選單中，選取現有資料集，或按一下「建立資料集」建立新資料集。選取要在資料交換中列出的資料集。資料集必須與資料交易所處的區域相同。建立產品資訊後，就無法更新這個欄位。當 BigQuery sharing 訂閱者[查看連結資料集的中繼資料](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#view-table-metadata)時，系統會傳回來源資料集名稱和包含該資料集的專案 ID。
     2. 選用：如要讓訂閱者[在資訊中分享 SQL 預存程序](#share-stored-procedure-in-listing)，請選取「允許共用預存程序」([預先發布版](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages))。
     3. 展開「區域資料可用性」選單，在其他區域提供共用資料集。選單會顯示有資料集副本的區域，並標示「可供使用」。設定多個區域的房源資訊前，請先確認已在共用資料集上啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)功能，因為您只能選取已啟用這項功能的區域。其他地區則標示為「不適用」。如未選取其他區域，項目會預設使用共用資料集的主要區域，標示為「供應商主要區域」。
     4. 在「資料輸出控制項」中，選取適當的資料輸出選項。

        + 如要對共用資料集套用資料輸出限制，但不要對共用資料集的查詢結果套用限制，請選取「停用共用資料的複製和匯出功能」。
        + 如要對共用資料集和共用資料集的查詢結果套用資料輸出限制，請選取「禁止複製及匯出查詢結果」，系統也會自動設定「禁止複製及匯出共用資料」。
        + 如要對共用資料集套用資料 API 複製及匯出輸出限制，請選取「停用透過 API 複製及匯出資料表的功能」，系統會自動一併設定「停用共用資料複製與匯出功能」。

        如要進一步瞭解資料輸出控管 (包括限制)，請參閱「[資料輸出選項 (僅限 BigQuery 共用資料集)](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)」。
   * 如果選取「Pub/Sub Topic」(Pub/Sub 主題)，則可以在「Shared topic」(共用主題) 選單中選取現有的 Pub/Sub 主題，或按一下「Create a topic」(建立主題)建立新主題。
5. 在「產品資訊詳細資料」部分的「顯示名稱」中，輸入產品資訊名稱。
6. 輸入下列選填詳細資料：

   * **類別**：選取最多兩個最能代表商家檔案的類別。BigQuery sharing 訂閱者可以根據這些類別[篩選商家資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * **資料親和性**：如果您使用 Pub/Sub 主題，BigQuery sharing 發布端會使用這些區域發布資料。BigQuery sharing 訂閱端可利用這項資訊，從相同區域讀取資料，盡量減少或避免 Pub/Sub 網路輸出費用。如要進一步瞭解輸出費用，請參閱「[資料移轉費用](https://cloud.google.com/pubsub/pricing?hl=zh-tw#egress_costs)」。
   * **圖示**：產品資訊的圖示。支援 PNG 和 JPEG 檔案格式。圖示的檔案大小不得超過 512 KiB，尺寸不得超過 512 x 512 像素。
   * **說明**：簡要說明房源。訂閱者可以根據說明[搜尋房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * **公開探索**：在 BigQuery sharing 目錄中啟用公開探索功能，啟用這個選項後，請授予 `allUsers` 或 `allAuthenticatedUsers` [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`)。詳情請參閱「[授予商家資訊角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。如果交易所已[公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)，則會自動沿用上架權限，因此不需要採取任何行動。

     由於權限繼承的關係，可公開探索的交易平台無法提供私人清單項目，但私人交易平台可以提供公開清單項目。如要建立公開資料集，資料集所在的專案必須有相關聯的機構和帳單帳戶。如果您要建立[整合 Cloud Marketplace 的商業產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，建議將產品資訊設為公開，方便使用者搜尋。
   * **訂閱端電子郵件記錄**：啟用記錄功能，以便掌握所有在連結資料集上執行工作和查詢的使用者[主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。啟用這項選項後，這項產品資訊日後的所有訂閱項目都會啟用訂閱者電子郵件記錄功能。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視區塊的 `job_principal_subject` 欄位中。](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)

     **注意：** 啟用並儲存電子郵件記錄功能後，就無法再編輯這項設定。如要停用電子郵件記錄功能，請刪除清單項目並重新建立，但不要點擊「訂閱者電子郵件記錄」切換按鈕。
   * **說明文件 > Markdown**：其他資訊，例如任何相關說明文件的連結，以及可協助 BigQuery 分享訂閱端使用主題的任何其他資訊。
7. 在「商店資訊聯絡資料」部分，輸入下列選填詳細資料：

   * **主要聯絡人**：輸入商家資訊主要聯絡人的電子郵件 ID 或網址。
   * **要求存取權聯絡人**：輸入電子郵件 ID 或 BigQuery sharing 訂閱者的聯絡表單網址。
   * **供應商**：展開「供應商」部分，並在下列欄位中指定詳細資料：

     + **供應商名稱**：主題供應商的名稱。
     + **供應商主要聯絡人**：主題供應商主要聯絡人的電子郵件 ID 或網址。

     訂閱者可以根據資料供應商篩選清單。
   * **發布商**：展開「發布商」部分，並在下列欄位中指定詳細資料：

     + **發布者名稱**：建立清單的 BigQuery sharing 發布者名稱。
     + **發布者主要聯絡人**：主題發布者主要聯絡人的電子郵件 ID 或網址。
8. 查看「商家資訊預覽」部分。
9. 按一下「發布」。

### API

請使用 [`projects.locations.dataExchanges.listings.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/create?hl=zh-tw)。

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings?listingId=LISTING_ID
```

更改下列內容：

* `PROJECT_ID`：包含資料交換庫的專案 ID，您要在該交換庫中建立商家資訊。
* `LOCATION`：資料交換庫的位置。如要進一步瞭解支援 BigQuery sharing 的位置，請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
* `DATAEXCHANGE_ID`：資料交換 ID。
* `LISTING_ID`：房源 ID。

在要求主體中，提供[房源詳細資料](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#resource:-listing)。

如要為多個區域建立房源資訊，請在要求主體的 `bigqueryDataset.replicaLocations` 欄位中指定其他區域。為多個區域設定項目之前，請先確認已在共用資料集上啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)。您只能選取已啟用跨區域資料集複製功能的區域。如果未填寫這個選填欄位，系統會使用共用資料集的主要區域建立產品資訊。

如果要求成功，回應主體會包含房源詳細資料。如果使用 `logLinkedDatasetQueryUserEmail` 欄位啟用訂閱者電子郵件記錄功能，清單回應會包含 `log_linked_dataset_query_user_email: true`。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視區塊的 `job_principal_subject` 欄位中](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)。

如要進一步瞭解如何使用 API 對房源執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

### 從資料集建立房源資訊

你也可以透過下列方式，從資料集建立產品資訊：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下資料集即可查看詳細資料。
3. 依序點選「分享」person\_add>「發布為房源資訊」。

   「建立房源資訊」對話方塊隨即開啟。
4. 選取要發布這項清單的資料交換庫。資料交換必須與資料集位於相同區域。如要進一步瞭解如何建立資料交換，請參閱「[建立交換並設定權限](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)」。
5. 在「共用資料集」選單中，選取現有資料集，或按一下「建立資料集」建立新資料集。選取要在資料交換中列出的資料集。資料集必須與資料交換位於相同區域。房源建立後，就無法更新這個欄位。

   當 BigQuery sharing 訂閱端[查看連結資料集的中繼資料](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#view-table-metadata)時，系統會傳回來源資料集名稱和包含該資料集的專案 ID。
6. 選用：如要讓訂閱者[在資訊中分享 SQL 預存程序](#share-stored-procedure-in-listing)，請選取「允許共用預存程序」([預先發布版](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages))。
7. 展開「區域資料可用性」選單，即可在其他區域提供共用資料集。選單會顯示有資料集副本的區域，並標示「可供使用」。為多個區域設定房源資訊前，請先確認已在共用資料集上啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)，因為您只能選取已啟用跨區域資料集複製的區域。其他地區則標示為「不適用」。如未選取其他區域，預設會使用共用資料集區域，標示為「供應商主要區域」。
8. 在「資料輸出控制項」中，選取適當的資料輸出選項。

   * 如要對共用資料集套用資料輸出限制，但不要對共用資料集的查詢結果套用限制，請選取「停用共用資料複製與匯出功能」。
   * 如要對共用資料集和共用資料集的查詢結果套用資料輸出限制，請選取「停用查詢結果複製與匯出功能」，系統也會自動設定「停用共用資料複製與匯出功能」。
   * 如要對共用資料集套用資料 API 複製和匯出輸出限制，請選取「停用透過 API 複製及匯出資料表的功能」，系統也會自動設定「停用共用資料複製與匯出功能」。

   如要進一步瞭解資料輸出控制項 (包括限制)，請參閱「[資料輸出選項 (僅限 BigQuery 共用資料集)](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)」。
9. 在「產品資訊詳細資料」部分的「顯示名稱」中，輸入產品資訊名稱。
10. 輸入下列選填詳細資料：

    * **類別**：選取最多兩個最能代表商家檔案的類別。BigQuery sharing 訂閱者可以根據這些類別[篩選商家資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
    * **資料親和性**：BigQuery sharing 發布者用來發布資料的區域。BigQuery sharing 訂閱端可利用這項資訊，從相同區域讀取資料，盡量減少或避免 Pub/Sub 網路輸出費用。如要進一步瞭解輸出費用，請參閱「[資料移轉費用](https://cloud.google.com/pubsub/pricing?hl=zh-tw#egress_costs)」。
    * **圖示**：產品資訊的圖示。支援 PNG 和 JPEG 檔案格式。圖示的檔案大小不得超過 512 KiB，尺寸不得超過 512 x 512 像素。
    * **說明**：簡要說明商家資訊。BigQuery sharing 訂閱者可以根據說明[搜尋清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
    * **公開可探索性**：在 BigQuery 共用目錄中啟用您的刊登資訊的公開可探索性。啟用這個選項後，請授予 `allUsers` 或 `allAuthenticatedUsers`「Analytics Hub 檢視者」角色 `roles/analyticshub.viewer`。詳情請參閱「[授予房源角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。如果交易所已[公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)，則會自動沿用刊登權限，因此不需要採取任何行動。

      由於權限繼承的關係，公開可探索的交易平台無法提供私人刊登，但私人交易平台可以提供公開刊登。如要建立公開資料，資料目錄所在的專案必須有相關聯的機構和帳單帳戶。如果您要建立[整合 Cloud Marketplace 的商業產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，建議將產品資訊設為公開，方便使用者搜尋。
    * **記錄訂閱端電子郵件**：開啟這項功能後，系統會記錄訂閱者[主要 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)，以便掌握日後所有訂閱者在清單項目連結資料集上執行的工作和查詢。啟用這個選項後，只有新建立的訂閱項目會記錄主體 ID。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視區塊的 `job_principal_subject` 欄位中](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)。

      **注意：** 啟用並儲存電子郵件記錄功能後，就無法再編輯這項設定。如要停用電子郵件記錄功能，請刪除清單項目並重新建立，但不要點擊「訂閱者電子郵件記錄」切換按鈕。
    * **說明文件 > Markdown**：其他資訊，例如任何相關說明文件的連結，以及有助於訂閱者使用主題的任何其他資訊。
11. 在「商店資訊聯絡資料」部分，輸入下列選填詳細資料：

    * **主要聯絡人**：輸入商家資訊主要聯絡人的電子郵件 ID 或網址。
    * **要求存取聯絡人**：輸入電子郵件 ID 或申請表單網址，供訂閱者與你聯絡。
    * **供應商**：展開「供應商」部分，並在下列欄位中指定詳細資料：

      + **供應商名稱**：主題供應商的名稱。
      + **供應商主要聯絡人**：主題供應商主要聯絡人的電子郵件 ID 或網址。

      訂閱者可以根據資料供應商篩選清單。
    * **發布商**：展開「發布商」部分，並在下列欄位中指定詳細資料：

      + **發布者名稱**：建立清單的 BigQuery sharing 發布者名稱。
      + **發布者主要聯絡人**：主題發布者主要聯絡人的電子郵件 ID 或網址。
12. 查看「商家資訊預覽」部分。
13. 按一下「發布」。

### 在房源資訊中分享 SQL 預存程序

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

注意：如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-data-sharing-feedback@google.com](mailto:bq-data-sharing-feedback@google.com)。

使用 BigQuery 資料集建立清單時，可以共用 [SQL 儲存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)。由於預存程序可以建立、捨棄及操控表格，也可以叫用其他預存程序，因此需要額外授權。

#### 訂閱者授權

訂閱項目後，系統可能不會直接執行連結的預存程序。為確保可存取連結的預存程序，訂閱者必須將連結的資料集名稱告知供應商，[供應商才能授權存取供應商資源中的連結預存程序](#provider-authorization)。此外，訂閱端必須[授權連結的共用預存程序，並將 IAM 角色連接至擁有的資源](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw#bq-attach-role)，才能讀取及寫入這些資源。

#### 提供者授權

供應商使用預存程序建立項目時，必須允許訂閱者透過連結的預存程序讀取及寫入資料表。如要確保這點，請按照下列步驟操作：

* 對於非讀取作業，供應商必須授權連結的共用預存程序，並[將 IAM 角色附加](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw#bq-attach-role)至連結預存程序存取的任何供應商資源。
* 如要執行讀取作業，供應商可以授權連結的共用預存程序 (位於訂閱端的連結資料集中)，或授權原始共用預存程序 (位於供應商的資料集中)，並[將 IAM 角色附加至](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw#bq-attach-role)連結預存程序存取的任何供應商資源。

## 授予使用者商家資訊存取權

如要授予使用者私人應用程式存取權，請為該應用程式設定個別使用者或群組的 IAM 政策。如果是商業房源，[資料交換必須公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)。公開資料交換庫中的項目會顯示在所有使用者的 BigQuery sharing ([Google Cloud `allAuthenticatedUsers`](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users))。如要讓使用者瀏覽及要求存取商業項目，您必須授予使用者 [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.viewer`)。如要讓使用者訂閱商業項目，您必須明確授予使用者 [Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`)。如果是[整合 Cloud Marketplace 的商業項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，系統會根據 Cloud Marketplace 訂單自動佈建 Analytics Hub 訂閱者角色。

如要讓所有人 (包括未使用 Google Cloud的使用者) 都能存取您的產品資訊，請授予 `allUsers` Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。

如要授予使用者查看或訂閱房源的權限，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下包含房源資訊的資料交換名稱。
3. 按一下要新增訂閱者的房源資訊。
4. 按一下「設定權限」person。
5. 如要新增主體，請按一下「新增主體」person\_add
   。
6. 在「New principals」(新增主體) 欄位中，根據房源類型新增下列詳細資料：

   * 如果是私人房源，請輸入要授予存取權的身分識別電子郵件 ID。
   * 如果是公開產品資訊，請新增 `allAuthenticatedUsers`。
   * 如要讓所有人 (包括非Google Cloud使用者) 都能找到公開的產品資訊，請新增 `allUsers`。
7. 將指標懸停在「Select a role」(選取角色) 的「Analytics Hub」(Analytics Hub) 上，然後根據商家資訊類型選取下列其中一個角色：

   * 如果是商業產品資訊 (包括整合 Cloud Marketplace 的產品資訊)，請選取「Analytics Hub Viewer」角色。這個角色可讓使用者[查看商家資訊並要求存取權](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * 如果是私人或非商業用途的公開清單，請選取「Analytics Hub 訂閱者」角色。使用者可透過這個角色[訂閱你的商家資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)。
   * 如果是整合 Cloud Marketplace 的產品資訊，系統會根據 Cloud Marketplace 訂單自動控管及管理訂閱項目，因此不需要授予 Analytics Hub 訂閱者角色 (`roles/analyticshub.subscriber`)。**注意：** 授予使用者存取非 Cloud Marketplace 整合式商業項目的授權後，您可以為這些使用者建立私人項目，或授予這些使用者商業項目的 Analytics Hub 訂閱者 (`roles/analyticshub.subscriber`) 角色。

   詳情請參閱「[Analytics Hub 訂閱者和檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role)」。
8. 按一下 [儲存]。

### API

1. 使用 [`projects.locations.dataExchanges.listings.getIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/getIamPolicy?hl=zh-tw)，透過清單 `getIamPolicy` 方法讀取現有政策。

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:getIamPolicy
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID，例如 `my-project-1`。
   * `LOCATION`：包含房源資訊的資料交換庫位置。
   * `DATAEXCHANGE_ID`：資料交換 ID。
   * `LISTING_ID`：房源 ID。

   分享會在回應中傳回目前的政策。
2. 如要新增或移除成員及其相關聯的角色，請使用文字編輯器編輯政策。請使用下列格式新增成員：

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
3. 使用 [`projects.locations.dataExchanges.listings.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/setIamPolicy?hl=zh-tw)寫入更新後的政策。在要求主體中，提供上一個步驟中更新的 IAM 政策。

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:setIamPolicy
   ```

   在要求主體中提供房源詳細資料。如果要求成功，回應主體會包含房源詳細資料。

如要進一步瞭解如何使用 API 對房源執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

**注意：** 授權使用者存取商業檔案後，你可以為這些使用者[建立私人檔案](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)，或授予商業檔案的[Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`)。

### 為公開房源建立未經驗證的網址

如要建立未經驗證的 BigQuery 共用清單網址，讓非Google Cloud 使用者也能查看，請按照下列步驟操作：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

   畫面上會顯示您可存取的所有資料交換。
2. 按一下包含房源資訊的資料交換名稱。
3. 按一下顯示名稱即可查看房源詳細資料。商店資訊必須啟用[公開探索功能](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)。
4. 按一下「複製公開連結」，即可產生未經驗證的產品資訊網址。請確認這份清單授予 `allUsers` Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。

### 建立商店資訊管理員

如要讓使用者管理商家資訊，必須建立商家資訊管理員。如要建立清單管理員，您必須在清單層級授予使用者 [Analytics Hub 發布者或 Analytics Hub 清單管理員 IAM 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role)。如要進一步瞭解如何授予這些角色，請參閱「[授予角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。

## 查看所有訂閱項目

如要查看目前所有商店資訊的訂閱項目，請選取下列其中一個選項：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下包含要管理訂閱項目商家資訊的資料交換庫名稱。
3. 按一下要列出所有訂閱者的商家資訊。
4. 如要查看您產品資訊的所有訂閱者，請按一下「管理訂閱」。
5. 選用：您可以依訂閱者詳細資料篩選結果。

或者，如果您有權存取[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)，可以按照下列步驟列出訂閱者：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案名稱，點選「Datasets」(資料集)，然後點選共用資料集的名稱。
4. 在「共用」person\_add清單中，選取「管理訂閱項目」。

### SQL

以下範例使用 [`INFORMATION_SCHEMA.SCHEMATA_LINKS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata-links?hl=zh-tw)，列出 `myproject` 中與共用資料集連結的所有連結資料集，這些資料集位於 `us` 區域：

```
SELECT * FROM `myproject`.`region-us`.INFORMATION_SCHEMA.SCHEMATA_LINKS;
```

輸出結果大致如下。某些資料欄會省略，用以簡化輸出內容。

```
+----------------+-------------+----------------------------+------------------------------+--------------------+--------------------------------+
|  catalog_name  | schema_name | linked_schema_catalog_name | linked_schema_catalog_number | linked_schema_name | linked_schema_org_display_name |
+----------------+-------------+----------------------------+------------------------------+--------------------+--------------------------------+
| myproject      | myschema1   | subscriptionproject1       |                 974999999291 | subscriptionld1    | subscriptionorg                |
| myproject      | myschema2   | subscriptionproject2       |                 974999999292 | subscriptionld2    | subscriptionorg                |
| myproject      | myschema3   | subscriptionproject3       |                 974999999293 | subscriptionld3    | subscriptionorg                |
+----------------+-------------+----------------------------+------------------------------+--------------------+--------------------------------+
```

如要查看多個區域的訂閱項目，請將 `us` 區域替換為預期副本位置。舉例來說，如要查看 `myproject` 中與共用資料集連結，且位於 `eu` 區域的連結資料集，請使用下列查詢：

```
SELECT * FROM `myproject`.`region-eu`.INFORMATION_SCHEMA.SCHEMATA_LINKS;
```

### API

使用 [projects.locations.dataExchanges.listings.listSubscriptions 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/listSubscriptions?hl=zh-tw)。

```
GET https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:listSubscriptions
```

更改下列內容：

* `PROJECT_ID`：您要訂閱的房源專案 ID。
* `LOCATION`：要訂閱的商家資訊位置。
* `DATAEXCHANGE_ID`：包含您要訂閱的房源資訊的資料交易 ID。
* `LISTING_ID`：要訂閱的房源 ID。

## 移除訂閱項目

如果移除 2023 年 7 月 25 日前建立的產品資訊訂閱項目，
[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)會與[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)取消連結。
訂閱者仍可在專案中查看資料集，但這些資料集已不再與共用資料集連結。

**注意：** 撤銷[與 Cloud Marketplace 整合的商業訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，可能會影響客戶並違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。

如要從商店資訊中移除 2023 年 7 月 25 日前建立的訂閱項目，請按照下列步驟操作：

1. 如要列出所有產品資訊的訂閱者，請按照「[查看所有訂閱項目](#view_all_subscriptions)」一文中的 Google Cloud 控制台操作說明進行操作。
2. 如要從清單中移除訂閱者，請按一下「刪除」delete。如要移除所有訂閱項目，請按一下「移除所有訂閱項目」。
3. 在「要移除訂閱項目嗎？」對話方塊中輸入 `remove` 以確認。
4. 按一下 [移除]。

如要移除 2023 年 7 月 25 日後建立的訂閱項目，請按照下列步驟操作：

### 控制台

1. 如要列出所有產品資訊的訂閱者，請按照「[查看所有訂閱項目](#view_all_subscriptions)」一文中的 Google Cloud 控制台操作說明進行操作。
2. 按一下「Subscriptions」(訂閱項目) 分頁標籤。
3. 如要從房源資訊中移除訂閱者，請選取要移除的訂閱項目，然後按一下 delete「移除訂閱」。
4. 在「要移除訂閱項目嗎？」對話方塊中輸入 `remove` 以確認。
5. 按一下 [移除]。

### API

使用 [projects.locations.subscriptions.revoke 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/revoke?hl=zh-tw)。

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/subscriptions/SUBSCRIPTION_ID:revoke
```

更改下列內容：

* `PROJECT_ID`：要移除的訂閱項目專案 ID。
* `LOCATION`：要移除的訂閱項目位置。
* `SUBSCRIPTION`：要移除的[訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#list_subscriptions) ID。

## 更新產品資訊

如要更新房源資訊，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下包含房源資訊的資料交換名稱。
3. 按一下要更新的商家資訊。
4. 按一下「編輯商家資訊」mode\_edit。
5. 修改欄位中的值。除了房源的共用資料集，您可修改所有值。
6. 選用：

   * 如要啟用公開探索功能，請將 Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`) 授予 `allUsers` 或 `allAuthenticatedUsers`。詳情請參閱「[授予房源角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。
   * 如果停用公開探索功能，請從 `allUsers` 和 `allAuthenticatedUsers` 移除 Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。公開交易平台無法提供私人房源，但私人交易平台可以提供公開房源。
   * 啟用並儲存訂閱端電子郵件記錄功能後，就無法編輯這項設定。如要停用電子郵件記錄功能，請刪除清單項目，然後重新建立，但不要點擊「訂閱者電子郵件記錄」切換按鈕。
   * 在房源資訊中新增或移除區域。新增多個區域前，請先確認您已在共用資料集上啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)。移除區域時，請先刪除該區域中的共用資料集副本。
7. 預覽房源資訊。
8. 如要儲存變更，請按一下「儲存」。為避免與整合 Cloud Marketplace 的產品資訊發生差異，系統會顯示通知，提示更新 Cloud Marketplace 資料產品資訊。

   **注意：** 更新 Cloud Marketplace 資料產品資訊時，必須經過 Marketplace 營運團隊審查並核准。

### API

請使用 [`projects.locations.dataExchanges.listings.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/patch?hl=zh-tw)。

```
PATCH https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID?updateMask=UPDATEMASK
```

將 `UPDATEMASK` 替換為要更新的欄位清單。如要更新多個值，請使用以半形逗號分隔的清單。舉例來說，如要更新資料交換的顯示名稱和主要聯絡人，請輸入 `displayName,primaryContact`。

在要求主體中，為下列欄位指定更新的值：

* `displayName`
* `description`
* `primaryContact`
* `documentation`
* `icon`
* `categories[]`
* `discoveryType`
* `logLinkedDatasetQueryUserEmail`
* `bigqueryDataset.replicaLocations`

如要瞭解這些欄位的詳細資料，請參閱「[資源：房源](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#resource:-listing)」。

更新商家資訊的副本區域時，請務必指定所有適用區域。更新商家資訊前，請確認已在共用資料集上啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)。您只能新增共用資料集複製的區域。如要移除區域，請先刪除該區域的共用資料集副本，再從項目中移除。您也可以將現有房源資訊轉換為多個地區的房源資訊。

如要進一步瞭解如何使用 API 對房源執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

## 刪除產品資訊

刪除商品後，訂閱者就無法再[查看商品](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。刪除房源資訊也會[刪除所有連結的資料集](#remove_a_subscription)，並從訂閱者專案中移除所有訂閱項目。如果資料集仍處於連結狀態，請依序點選 person\_add「共用」**>「管理訂閱」**，手動移除資料集。系統會開啟「訂閱項目」頁面，您可以在這裡移除特定訂閱者資料集，或一次移除所有訂閱者資料集。

您無法刪除含有有效商業訂閱項目的[整合 Cloud Marketplace 的產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)。刪除房源前，請[撤銷所有商業訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#revoke-subscription)。

**注意：** 請注意，撤銷與 Cloud Marketplace 整合的商業訂閱項目，可能會影響客戶並違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。

刪除多個區域的產品資訊不會一併刪除共用資料集副本。刪除多個區域的項目後，訂閱者就無法再查看項目或查詢連結的資料集。如果其他項目未參照共用資料集副本，您可以[選擇刪除副本](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#remove_a_dataset_replica)。

刪除多個區域的產品資訊前，請確認沒有與其相關聯的有效訂閱項目。如有有效訂閱項目，您必須先使用 [`projects.locations.subscriptions.revoke` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/revoke?hl=zh-tw)撤銷訂閱。移除所有有效訂閱後，即可繼續刪除多個區域的商家資訊。

**注意：** 一旦刪除房源，就無法復原。

如要刪除商家資訊，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下包含房源資訊的資料交換名稱。
3. 按一下要刪除的商家資訊。
4. 按一下「刪除」圖示 delete。
5. 在「Delete listing?」(刪除房源？) 對話方塊中輸入「delete」(刪除)，確認要刪除房源。
6. 點選「刪除」。

### API

請使用 [`projects.locations.dataExchanges.listings.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/delete?hl=zh-tw)。

```
DELETE https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID
```

如要進一步瞭解如何使用 API 對房源執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

## 在精選專區中顯示房源資訊

如要提高 BigQuery 共用目錄中資源的曝光率和知名度，資源可以顯示在「精選」部分。精選房源受《 Google CloudPartner Advantage 協議》規範。

如要讓合作夥伴的清單顯示在 BigQuery sharing 目錄的「精選」部分，必須符合下列條件：

* 共用資料必須位於 BigQuery 中。
* 他們必須註冊[Partner Advantage 計畫](https://partners.cloud.google.com/?hl=zh-tw)，並取得「建構」資格。
* 清單必須已建立，且已啟用[公開探索](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)功能。

如要將商家資訊加入「精選」專區，請填寫並提交[申請表單](https://docs.google.com/forms/d/e/1FAIpQLSe9nLw7kmvU2AEUgaWn5vvPQMFs1Q7XwqKBy7TD5xR1DLX4bQ/viewform?resourcekey=0-zRsM2reDM3QjxegIUluHJA&%3Bpli=1&hl=zh-tw)。如要要求從該專區移除商家資訊，請提交相同的[申請表單](https://docs.google.com/forms/d/e/1FAIpQLSe9nLw7kmvU2AEUgaWn5vvPQMFs1Q7XwqKBy7TD5xR1DLX4bQ/viewform?resourcekey=0-zRsM2reDM3QjxegIUluHJA&%3Bpli=1&hl=zh-tw)。

## 後續步驟

* 瞭解 [BigQuery 共用架構](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#architecture)。
* 瞭解如何[查看及訂閱房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。
* 瞭解 [BigQuery sharing IAM 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#user_roles)。
* 瞭解如何[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。
* 瞭解 [BigQuery sharing 稽核記錄](https://docs.cloud.google.com/bigquery/docs/analytics-hub-audit-logging?hl=zh-tw)。
* 瞭解如何[監控商家資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]