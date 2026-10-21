Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理清單

在 BigQuery sharing (舊稱 Analytics Hub) 中，資料發布者可以建立及管理清單，安全地與跨機構的訂閱者共用資料集，不必複製資料。

管理房源時，你可以執行下列工作：

* 在具備發布存取權的任何資料交換中，建立、更新、共用及刪除商家資訊。
* 將 BigQuery sharing 角色指派給管理員、訂閱者和檢視者，藉此管理存取權。
* 查看、監控及移除訂閱者。
* [監控訂閱方案用量指標](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw#use-analytics-hub)。

清單是發布者在[資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)中列出的共用資料集參照資訊。視為目錄設定的身分與存取權管理 (IAM) 政策，以及包含目錄的資料交換類型而定，目錄可分為下列兩種：

* **公開產品資訊。**[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 可以[探索](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)公開清單，並[訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)公開清單。公開資料交換中的清單就是公開清單。這些產品資訊可以參照*免費公開資料集*或*商業資料集*。如果清單參照商業資料集，訂閱者可以直接向資料供應商要求存取清單，也可以瀏覽及購買[與 Google Cloud Marketplace 整合的商業清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)。
* **私人房源資訊**。私人房源資訊會直接分享給個人或群組。舉例來說，私人產品資訊可以參照您與貴機構內部團隊共用的行銷指標資料集。即使你
  [允許所有 Google Cloud 使用者 (`allAuthenticatedUsers`)](#give_users_access_to_a_listing)
  訂閱私人房源，房源仍會維持私人狀態。[不會在 BigQuery 共用頁面顯示為公開清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。如要與使用者分享私人房源，請將房源網址傳送給對方。如要讓私人清單公開顯示，請[公開資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)。

**注意：** 單一 BigQuery 共用項目同時支援要求存取權和 Cloud Marketplace 整合流程。因此，您可以從現有的 (離線) 商業商家資訊建立整合 Cloud Marketplace 的商家資訊，現有訂閱項目不會受到任何影響。

## 事前準備

如要開始使用 BigQuery sharing (舊稱 Analytics Hub)，請在專案中啟用 Analytics Hub API Google Cloud 。

如要啟用 Analytics Hub API，您必須具備下列 Identity and Access Management (IAM) 權限：

* `serviceUsage.services.get`
* `serviceUsage.services.list`
* `serviceUsage.services.enable`

下列預先定義的 IAM 角色包含啟用 Analytics Hub API 所需的權限：

* [服務使用情形管理員](https://docs.cloud.google.com/service-usage/docs/access-control?hl=zh-tw#serviceusage.serviceUsageAdmin) (`roles/serviceusage.serviceUsageAdmin`)

如要啟用 Analytics Hub API，請選取下列其中一個選項：

### 控制台

前往 **Analytics Hub API** 頁面，為 Google Cloud 專案啟用 Analytics Hub API。

[啟用 Analytics Hub API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### gcloud

執行 [gcloud services enable](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw) 指令：

```
gcloud services enable analyticshub.googleapis.com
```

### 必要的角色

如要管理項目和訂閱項目，您必須具備下列任一 BigQuery sharing Identity and Access Management (IAM) 角色：

* [Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.publisher)
  (`roles/analyticshub.publisher`)，可讓您建立、更新、刪除及設定項目 IAM 政策。
* [Analytics Hub 項目管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.listingAdmin) (`roles/analyticshub.listingAdmin`)，可讓您更新、刪除項目，以及設定項目的 IAM 政策。
* [Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.admin)
  (`roles/analyticshub.admin`)，可讓您建立、更新、刪除資料交換庫中的所有產品資訊，以及設定 IAM 政策。

詳情請參閱「[BigQuery 共用 IAM 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#user_roles)」。如要瞭解如何將這些角色授予其他使用者，請參閱「[建立房源管理員](#create-listing-administrator)」。

如要建立項目或更新項目的副本區域，您必須具備來源資料集的 `bigquery.datasets.get` 和 `bigquery.datasets.update` 權限。下列 [BigQuery 預先定義的角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)包含 `bigquery.datasets.update` 權限：

* [BigQuery 資料擁有者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner)
  (`roles/bigquery.dataOwner`)
* [BigQuery 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)
  (`roles/bigquery.admin`)

如要查看您有權存取的機構中所有專案的資料交換，您必須具備 `resourcemanager.organizations.get` 權限。沒有包含這項權限的 BigQuery 預先定義角色，因此您必須使用 [IAM 自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。

## 查看資料交換庫

如要查看貴機構中可存取的資料交換庫清單，請參閱「[查看資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#view_data_exchanges)」。如果資料交換庫位於其他機構，BigQuery sharing 管理員必須[與您共用資料交換庫連結](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#share_a_data_exchange)。

## 建立產品資訊

清單是 BigQuery 共用發布端在資料交換庫中列出的[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)參照資訊。

**注意：** 建議您不要在Google Cloud 使用 VPC Service Controls 服務範圍的專案中建立共用資料集。如必須使用 service perimeter，請務必設定必要的[輸入和輸出規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw#create_a_listing)。

如要建立房源資訊，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

   頁面隨即會列出您可存取的所有資料交換。
2. 按一下要建立刊登資訊的資料交易所名稱。
3. 按一下 add\_box「建立商店資訊」。
4. 在「設定資料」部分的「資源類型」選單中，選取「BigQuery 資料集」或「Pub/Sub 主題」。

   * 如果選取「BigQuery 資料集」，請執行下列操作：

     1. 在「共用資料集」選單中，選取現有資料集，或按一下「建立資料集」建立資料集。資料集必須與資料交易位於相同區域。建立商店資訊後，就無法變更共用資料集。訂閱者[查看連結資料集的繼資料](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#view-table-metadata)時，BigQuery sharing 功能會傳回來源資料集名稱，以及包含該資料集的專案 ID。
     2. 選用：如要讓訂閱者[在多個房源之間共用 SQL 預存程序](#share-stored-procedure-in-listing)，請選取「允許共用預存程序」([預覽版](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages))。
     3. 如要在其他區域提供共用資料集，請展開「區域資料可用性」選單。選單會顯示標示為「可供使用」的現有資料集副本區域。為多個區域設定項目之前，請先確認您已在共用資料集上啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)。您只能選取已啟用跨區域資料集複製功能的區域；其他區域都會標示為「無法使用」。如未選取其他區域，項目會預設為共用資料集的主要區域，標示為「供應商主要區域」。
     4. 在「資料輸出控制項」中，選取適當的資料輸出選項：

        + 如要限制共用資料集的資料複製和匯出作業，但允許匯出查詢結果，請選取「停用共用資料複製與匯出功能」。
        + 如要限制共用資料集和查詢結果的資料複製及匯出作業，請選取「停用查詢結果複製與匯出功能」。這個選項也會選取「停用共用資料複製與匯出功能」。
        + 如要限制透過 API 複製及匯出共用資料集中的資料表，請選取「停用透過 API 複製及匯出資料表的功能」。這個選項也會選取「停用共用資料複製與匯出功能」。

        如要進一步瞭解資料輸出控制項 (包括限制)，請參閱「[資料輸出選項 (僅限 BigQuery 共用資料集)](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)」。
   * 如果選取「Pub/Sub 主題」，請在「共用主題」選單中選取現有的 Pub/Sub 主題，或點選「建立主題」來建立主題。
5. 在「產品資訊詳細資料」部分的「顯示名稱」欄位中，輸入產品資訊的名稱。
6. 輸入下列選填詳細資料：

   * **類別**：選取最多兩個最能代表房源的類別。訂閱者可以根據你選取的類別[篩選商品](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * **資料相依性**：指定用於發布資料的區域。
     訂閱者可透過這項位置設定，從相同區域讀取資料，盡量減少或避免 Pub/Sub 網路輸出費用。如要進一步瞭解輸出費用，請參閱「[資料移轉費用](https://cloud.google.com/pubsub/pricing?hl=zh-tw#egress_costs)」。
   * **圖示**：上傳商店資訊的圖示。支援 PNG 和 JPEG 檔案格式。圖示大小不得超過 512 KiB，最大尺寸為 512 x 512 像素。
   * **說明**：輸入房源的簡短說明。訂閱者可以[依說明文字搜尋房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * **公開探索**：開啟這項設定，即可在 BigQuery 共用目錄中公開探索您的項目。啟用這個選項後，請將 [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`) 授予 `allUsers` 或 `allAuthenticatedUsers`。詳情請參閱「[授予房源角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。如果交易所已[公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)，項目會沿用這些權限，因此無須採取進一步行動。

     由於權限繼承，公開可探索的交易平台無法有私人刊登項目，但私人交易平台可以有公開刊登項目。如要建立公開產品資訊，包含該產品資訊的專案必須有相關聯的機構和帳單帳戶。如果您建立[與 Cloud Marketplace 整合的商業產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，建議開啟公開曝光度。
   * **記錄訂閱端電子郵件**：開啟這項設定，即可記錄在連結資料集上執行工作和查詢的所有使用者的[主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。如果啟用這個選項，日後透過這個清單建立的所有訂閱項目都會啟用訂閱者電子郵件記錄功能。記錄的資料會顯示在[`INFORMATION_SCHEMA.SHARED_DATASET_USAGE`檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的「`job_principal_subject`」欄中。

     **注意：** 啟用並儲存訂閱端電子郵件記錄功能後，就無法編輯這項設定。如要關閉電子郵件記錄功能，請刪除清單項目，然後重新建立清單項目，但不要選取「訂閱者電子郵件記錄」。
   * **說明文件 > Markdown**：以 Markdown 格式輸入支援文件、連結或說明，協助訂閱者使用資料集。
7. 在「商家資訊聯絡資料」部分，輸入下列選填詳細資料：

   * **主要聯絡人**：輸入商家資訊主要聯絡人的電子郵件地址或網址。
   * **要求存取權聯絡人**：輸入你的申請表單電子郵件地址或網址，方便訂閱者與你聯絡，要求存取權。
   * **供應商**：展開「供應商」部分，並在下列欄位中輸入詳細資料：

     + **供應商名稱**：資料供應商的名稱。
     + **供應商主要聯絡人**：資料供應商主要聯絡人的電子郵件地址或網址。

     訂閱者可以依資料供應商篩選清單。
   * **發布商**：展開「發布商」部分，並在下列欄位中輸入詳細資料：

     + **發布商名稱**：建立商家資訊的發布商名稱。
     + **發布商主要聯絡人**：發布商主要聯絡人的電子郵件地址或網址。
8. 查看「商家資訊預覽」部分。
9. 如要發布房源資訊，請按一下「發布」。

### API

請使用 [`projects.locations.dataExchanges.listings.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/create?hl=zh-tw)：

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings?listingId=LISTING_ID
```

更改下列內容：

* `PROJECT_ID`：包含資料交換的專案 ID，您要在其中建立商家資訊。
* `LOCATION`：資料交換庫的位置。如要進一步瞭解支援 BigQuery sharing 的位置，請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
* `DATAEXCHANGE_ID`：資料交換 ID。
* `LISTING_ID`：房源 ID。

在要求主體中，提供[房源詳細資料](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#resource:-listing)。

如要在多個區域建立產品資訊，請在要求主體的 `bigqueryDataset.replicaLocations` 欄位中指定這些區域。為多個區域設定項目之前，請先確認您已在共用資料集上啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)。您只能選取已啟用跨區域資料集複製功能的區域。如果省略這個選填欄位，房源資訊會使用共用資料集的主要區域。

如果要求成功，回應主體會傳回房源詳細資料。如果將 `logLinkedDatasetQueryUserEmail` 欄位設為 `true`，開啟訂閱端電子郵件記錄功能，清單回應會傳回 `log_linked_dataset_query_user_email: true`。記錄的資料會顯示在[`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄中。

如要進一步瞭解如何使用 API 對商家資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

### 從資料集建立房源資訊

如要直接從現有資料集建立房源資訊，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如要查看資料集詳細資料，請按一下資料集名稱。
3. 依序點選「共用」person\_add>「發布為房源資訊」。

   「建立商家資訊」對話方塊隨即開啟。
4. 選取要發布清單的資料交易所。資料交換庫必須與資料集位於相同區域。如要進一步瞭解如何建立資料交換庫，請參閱「[建立交換庫並設定權限](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)」。
5. 在「共用資料集」選單中，選取現有資料集，或按一下「建立資料集」建立資料集。資料集必須與資料交易所位於相同區域。建立產品資訊後，就無法變更這項設定。

   訂閱者[查看連結資料集的繼資料](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#view-table-metadata)時，BigQuery sharing 會傳回來源資料集名稱，以及包含該資料集的專案 ID。
6. 選用：如要讓訂閱者[在多個房源之間共用 SQL 預存程序](#share-stored-procedure-in-listing)，請選取「允許共用預存程序」([預覽版](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages))。
7. 如要在其他區域提供共用資料集，請展開「區域資料可用性」選單。選單會顯示標示為「可供使用」的區域，這些區域有資料集副本。為多個區域設定項目之前，請先確認您已在共用資料集上啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)。您只能選取已啟用跨區域資料集複寫功能的區域，其他區域則會標示為「無法使用」。如未選取其他區域，產品資訊會預設為共用資料集的主要區域，標示為「供應商主要區域」。
8. 在「資料輸出控制項」中，選取適當的資料輸出選項：

   * 如要限制共用資料集的複製和匯出作業，但允許匯出查詢結果，請選取「停用共用資料複製與匯出功能」。
   * 如要限制共用資料集和查詢結果的複製及匯出作業，請選取「停用查詢結果複製與匯出功能」。這個選項也會選取「停用共用資料複製與匯出功能」。
   * 如要限制透過 API 複製及匯出共用資料集中的資料表，請選取「停用透過 API 複製及匯出資料表的功能」。這個選項也會選取「停用共用資料複製與匯出功能」。

   如要瞭解資料輸出控制項和限制，請參閱「[資料輸出選項 (僅限 BigQuery 共用資料集)](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)」。
9. 在「應用程式詳細資訊」部分的「顯示名稱」欄位，輸入應用程式的名稱。
10. 輸入下列選填詳細資料：

    * **類別**：選取最多兩個最能代表房源的類別。訂閱者可以根據你選取的類別[篩選商品](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
    * **資料相依性**：指定用於發布資料的區域。
      訂閱者可透過這項位置設定，從相同區域讀取資料，盡量減少或避免產生 Pub/Sub 網路輸出費用。如要進一步瞭解輸出費用，請參閱「[資料移轉費用](https://cloud.google.com/pubsub/pricing?hl=zh-tw#egress_costs)」。
    * **圖示**：上傳商店資訊的圖示。支援 PNG 和 JPEG 檔案格式。圖示大小不得超過 512 KiB，最大尺寸為 512 x 512 像素。
    * **說明**：輸入房源的簡短說明。訂閱者可以根據說明文字[搜尋房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
    * **公開探索**：開啟這項設定，即可在 BigQuery 共用目錄中公開探索您的項目。啟用這個選項後，請授予 `allUsers` 或 `allAuthenticatedUsers` Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。詳情請參閱「[授予商家檔案角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。如果交易所已[公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)，項目會沿用這些權限，因此無須採取進一步行動。

      由於權限繼承的關係，公開可探索的交易平台無法有私人刊登項目，但私人交易平台可以有公開刊登項目。如要建立公開項目，包含該項目的專案必須有相關聯的機構和帳單帳戶。如果您建立[整合 Cloud Marketplace 的商業產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，建議開啟公開可探索性。
    * **記錄訂閱端電子郵件**：開啟這項功能後，系統會記錄訂閱者 (在清單項目的連結資料集上執行工作和查詢) 的[主要 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)，以供日後所有訂閱項目使用。開啟這個選項後，只有新建立的訂閱項目會記錄主體 ID。記錄的資料會顯示在[`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄中。

      **注意：** 啟用並儲存訂閱端電子郵件記錄功能後，就無法編輯這項設定。如要關閉電子郵件記錄功能，請刪除清單項目，然後重新建立清單項目，但不要選取「訂閱者電子郵件記錄」。
    * **說明文件 > Markdown**：輸入輔助說明文件、連結或操作說明，協助訂閱者使用資料集。
11. 在「商家資訊聯絡資料」部分，輸入下列選填詳細資料：

    * **主要聯絡人**：輸入商家資訊主要聯絡人的電子郵件地址或網址。
    * **要求存取權聯絡人**：輸入收件表單的電子郵件地址或網址，方便訂閱者與您聯絡，要求存取權。
    * **供應商**：展開「供應商」部分，並在下列欄位中輸入詳細資料：

      + **供應商名稱**：資料供應商的名稱。
      + **供應商主要聯絡人**：資料供應商主要聯絡人的電子郵件地址或網址。

      訂閱者可以依資料供應商篩選清單。
    * **發布商**：展開「發布商」部分，並在下列欄位中輸入詳細資料：

      + **發布商名稱**：建立商家資訊的發布商名稱。
      + **發布商主要聯絡人**：發布商主要聯絡人的電子郵件地址或網址。
12. 查看「商家資訊預覽」部分。
13. 如要發布房源資訊，請按一下「發布」。

## 在多個房源之間共用 SQL 預存程序

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**附註：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-data-sharing-feedback@google.com](mailto:bq-data-sharing-feedback@google.com)。

使用 BigQuery 資料集建立清單時，您可以共用 [SQL 預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)。由於預存程序可以建立、捨棄及操控表格，並叫用其他預存程序，因此共用預存程序需要額外授權。

### 訂閱者授權

訂閱者訂閱項目後，連結的預存程序可能不會立即執行。為確保連結的預存程序可以執行，訂閱者必須將連結的資料集名稱傳送給供應商，[供應商才能授權在供應商的資源上執行連結的預存程序](#provider-authorization)。此外，訂閱者必須[授權連結的共用預存程序，並將 IAM 角色附加](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw#bq-attach-role)至訂閱者的資源，允許從這些資源讀取及寫入資料。

### 供應商授權

供應商使用預存程序建立項目時，必須允許訂閱者透過連結的預存程序，讀取及寫入供應商的資料表。為確保存取權，供應商必須採取下列行動：

* 如果是非讀取作業，請授權連結的共用預存程序，並[將 IAM 角色附加](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw#bq-attach-role)至連結預存程序存取的任何供應商資源。
* 如要執行讀取作業，請授權連結的共用預存程序 (位於訂閱者的連結資料集中) 或原始共用預存程序 (位於供應商的資料集中)，並將 IAM 角色附加至程序存取的任何供應商資源。

## 授予使用者存取商家資訊的權限

如要提供私人資訊的存取權，請為該資訊設定 IAM 政策，加入特定個人或群組。如果是商業資訊，[資料交換必須公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)。公開資料交易所中的項目會顯示在所有[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 的 BigQuery 分享中。如要讓使用者瀏覽及要求存取商業項目，請授予這些使用者「Analytics Hub 檢視者」角色 (`roles/analyticshub.viewer`)。如要讓使用者訂閱商業項目，請授予這些使用者「Analytics Hub 訂閱者」角色 (`roles/analyticshub.subscriber`)。如果是[整合 Cloud Marketplace 的商業項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，BigQuery 分享會根據 Cloud Marketplace 訂單，自動授予「Analytics Hub 訂閱者」角色。

如要讓所有人 (包括沒有Google Cloud 帳戶的使用者) 都能存取房源資訊，請授予 `allUsers` Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。

如要授予使用者查看或訂閱商家資訊的權限，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有商家資訊的資料交換名稱。
3. 按一下要分享的房源資訊。
4. 按一下「設定權限」person。
5. 如要新增主體，請按一下「新增主體」person\_add
   。
6. 在「New principals」(新增主體) 欄位中，根據房源類型輸入主體：

   * 如果是私人房源，請輸入要授予存取權的身分電子郵件地址。
   * 如果是公開房源，請輸入 `allAuthenticatedUsers`。
   * 如要讓所有人 (包括非Google Cloud使用者) 都能找到公開清單，請輸入 `allUsers`。
7. 在「選取角色」選單中，指向「Analytics Hub」，然後根據您的房源類型選取角色：

   * 如果是商業產品資訊 (包括與 Cloud Marketplace 整合的產品資訊)，請選取「Analytics Hub 檢視者」。這個角色可讓使用者[查看商家資訊並要求存取權](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * 如果是私人或非商業用途的公開項目，請選取「Analytics Hub 訂閱者」。這個角色可讓使用者[訂閱你的產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)。
   * 如果是整合 Cloud Marketplace 的項目，您不需要授予 Analytics Hub 訂閱者角色 (`roles/analyticshub.subscriber`)。系統會根據 Cloud Marketplace 訂單自動管理訂閱項目。**注意：** 授予授權後，使用者就能存取未整合 Cloud Marketplace 的商業項目。您可以為這些使用者[建立私人項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)，也可以在商業項目中授予這些使用者 [Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`)。

   詳情請參閱「[Analytics Hub 訂閱者和檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role)」。
8. 如要儲存權限，請按一下「儲存」。

### API

1. 呼叫 [`projects.locations.dataExchanges.listings.getIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/getIamPolicy?hl=zh-tw)，讀取現有政策：

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:getIamPolicy
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID，例如 `my-project-1`。
   * `LOCATION`：包含房源資訊的資料交易所位置。
   * `DATAEXCHANGE_ID`：資料交換 ID。
   * `LISTING_ID`：房源 ID。

   共用會傳回回應中的現行政策。
2. 如要新增或移除成員及其相關聯的角色，請使用文字編輯器編輯政策 JSON。請使用下列格式指定成員：

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
3. 呼叫 [`projects.locations.dataExchanges.listings.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/setIamPolicy?hl=zh-tw)，更新政策。
   在要求主體中，傳遞上一個步驟中的更新版 IAM 政策。

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:setIamPolicy
   ```

   在要求主體中，傳遞房源詳細資料。如果要求成功，回應主體會傳回更新政策的房源詳細資料。

如要進一步瞭解如何使用 API 對商家資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

**注意：** 授權使用者存取商業資訊後，你可以為這些使用者[建立私人資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)，或在商業資訊中授予這些使用者 Analytics Hub 訂閱者角色 (`roles/analyticshub.subscriber`)。

### 為公開房源建立未經驗證的網址

如要建立未經驗證的 BigQuery 共用清單網址，供沒有 Google Cloud 帳戶的使用者查看，請按照下列步驟操作：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

   頁面隨即會列出您可存取的所有資料交換。
2. 按一下含有商家資訊的資料交換名稱。
3. 如要查看房源詳細資料，請按一下房源顯示名稱。清單必須開啟[開放搜尋](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)功能。
4. 按一下「複製公開連結」。為確保外部使用者可以查看房源資訊，請確認房源資訊已授予 `allUsers` Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。

### 建立商店資訊管理員

如要讓使用者管理商家資訊，請授予使用者商家資訊的[Analytics Hub 發布者或 Analytics Hub 商家資訊管理員角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role)，建立商家資訊管理員。如需授予商家資訊角色的操作說明，請參閱「[授予商家資訊角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。

## 查看所有訂閱項目

如要查看目前所有訂閱項目，請選取下列任一選項：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有要管理訂閱項目的商家資訊的資料交易平台名稱。
3. 按一下要列出所有訂閱者的房源。
4. 如要查看所有訂閱者，請按一下「管理訂閱項目」：
5. 選用：您可以依訂閱者詳細資料篩選結果。

或者，如果您有權存取[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)，可以按照下列步驟列出訂閱者：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案名稱，點選「Datasets」(資料集)，然後點選共用資料集的名稱。
4. 在「共用」person\_add清單中，選取「管理訂閱項目」。

### SQL

以下範例使用 [`INFORMATION_SCHEMA.SCHEMATA_LINKS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata-links?hl=zh-tw)，列出 `myproject` 中連結至共用資料集的所有連結資料集，這些資料集位於 `us` 區域：

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

如要查看多個區域的訂閱項目，請將 `us` 區域替換為預期的副本位置。舉例來說，如要查看 `myproject` 中連結至共用資料集且位於 `eu` 區域的連結資料集，請使用下列查詢：

```
SELECT * FROM `myproject`.`region-eu`.INFORMATION_SCHEMA.SCHEMATA_LINKS;
```

### API

請使用 [projects.locations.dataExchanges.listings.listSubscriptions 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/listSubscriptions?hl=zh-tw)。

```
GET https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:listSubscriptions
```

更改下列內容：

* `PROJECT_ID`：要訂閱的房源專案 ID。
* `LOCATION`：要訂閱的商家資訊位置。
* `DATAEXCHANGE_ID`：包含要訂閱的房源資訊的資料交易 ID。
* `LISTING_ID`：要訂閱的房源 ID。

## 移除訂閱項目

從房源移除 2023 年 7 月 25 日前建立的訂閱項目時，[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)會與[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)取消連結。訂閱者仍可在專案中查看資料集，但資料集不再連結至共用資料集。

**注意：** 撤銷[與 Cloud Marketplace 整合的商業訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)可能會影響客戶，並違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。

如要從房源資訊中移除 2023 年 7 月 25 日前建立的訂閱項目，請按照下列步驟操作：

1. 如要列出房源的訂閱者，請按照[查看所有訂閱項目](#view_all_subscriptions)的 Google Cloud 控制台操作說明進行。
2. 如要從清單中移除訂閱者，請按一下「刪除」delete。如要移除所有訂閱項目，請按一下「移除所有訂閱項目」。
3. 在「Remove subscription?」(要移除訂閱項目嗎？) 對話方塊中，輸入 `remove` 確認刪除。
4. 按一下 [移除]。

如要移除 2023 年 7 月 25 日後建立的訂閱項目，請按照下列步驟操作：

### 控制台

1. 如要列出房源的訂閱者，請按照[查看所有訂閱項目](#view_all_subscriptions)的 Google Cloud 控制台操作說明進行。
2. 按一下「訂閱項目」。
3. 如要選取要移除的訂閱項目，請勾選這些訂閱項目旁邊的核取方塊，然後按一下「移除訂閱項目」delete。
4. 在「要移除訂閱項目嗎？」對話方塊中輸入 `remove`，確認移除。
5. 按一下 [移除]。

### API

呼叫 [`projects.locations.subscriptions.revoke` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/revoke?hl=zh-tw)：

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/subscriptions/SUBSCRIPTION_ID:revoke
```

更改下列內容：

* `PROJECT_ID`：要移除的訂閱項目專案 ID。
* `LOCATION`：要移除的訂閱項目位置。
* `SUBSCRIPTION`：要移除的[訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#list_subscriptions) ID。

## 更新產品資訊

隨著資料交換需求演變，您可以更新房源的後設資料、類別、可探索性設定和區域供應情形，而不必修改基礎共用資料集。

如果 Google Cloud 專案使用 VPC Service Controls 服務範圍，您可能需要設定額外的[輸入和輸出規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw#update-listing)，允許背景同步更新相關聯的連結資料集。

如要更新房源資訊，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有商家資訊的資料交換名稱。
3. 按一下要更新的房源。
4. 按一下「編輯商家資訊」mode\_edit。
5. 修改欄位中的值。除了房源的共用資料集，你都可以修改所有值。
6. 選用：更新房源設定和供應情形：

   * 如要啟用公開探索功能，請將 [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`) 授予 `allUsers` 或 `allAuthenticatedUsers`。如需授予商家資訊角色的操作說明，請參閱「[授予商家資訊角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。
   * 如要停用私有交換庫中的產品資訊公開探索功能，請從 `roles/analyticshub.viewer``allUsers` 和 `allAuthenticatedUsers` 移除 Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。如果交易平台已[公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)，則會自動沿用刊登權限，無須採取進一步行動。
   * 啟用並儲存訂閱端電子郵件記錄功能後，就無法編輯這項設定。如要關閉電子郵件記錄功能，請刪除清單項目，然後重新建立清單項目，但不要選取「訂閱者電子郵件記錄」。
   * 如要新增或移除區域，請更新區域選取項目。新增多個區域前，請確認您已在共用資料集上啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)。移除區域前，請先刪除該區域中的共用資料集副本。
7. 查看預覽畫面。
8. 如要儲存變更，請按一下「儲存」。如果更新整合 Cloud Marketplace 的產品資訊，系統會顯示通知，提示你一併更新 Cloud Marketplace 資料產品資訊。

   **注意：** 更新 Cloud Marketplace 資料產品資訊時，必須經過 Marketplace 營運團隊審查並核准。

### API

呼叫 [`projects.locations.dataExchanges.listings.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/patch?hl=zh-tw)：

```
PATCH https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID?updateMask=UPDATEMASK
```

更改下列內容：

* `PROJECT_ID`：專案 ID，用於存放您要建立資源的資料交易所。
* `LOCATION`：資料交易所的位置。
* `DATAEXCHANGE_ID`：資料交換 ID。
* `LISTING_ID`：要更新的房源 ID。
* `UPDATEMASK`：要更新的欄位清單。如要更新多個值，請使用以半形逗號分隔的清單。舉例來說，如要更新資料交換的顯示名稱和主要聯絡人，請輸入 `displayName,primaryContact`。

在要求主體中，為更新遮罩中的欄位指定更新的值：

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

更新房源的副本區域時，請指定所有適用區域。更新房源前，請先確認已在共用資料集上啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)。您只能新增共用資料集有副本的區域。從項目中移除區域前，請先刪除該區域的共用資料集副本。你也可以將單一區域房源資訊轉換為多區域房源資訊。

如要進一步瞭解如何使用 API 對商家資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

## 在精選專區中顯示房源資訊

如要提高 BigQuery 共用目錄中項目的曝光度，可以在「精選」部分顯示項目。精選房源受《 Google Cloud 合作夥伴計畫協議》規範。

如要讓房源顯示在「精選」部分，必須符合下列條件：

* 共用資料必須位於 BigQuery 中。
* 您必須在 Google Cloud 技術合作夥伴路徑中，註冊[Google Cloud 合作夥伴網路計畫](https://partners.cloud.google.com/?hl=zh-tw)。
* 你必須建立商店資訊，並開啟[公開探索功能](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)。

如要申請將商家資訊新增至「精選」部分，或申請從該部分移除商家資訊，請提交[精選商家資訊登記表單](https://docs.google.com/forms/d/e/1FAIpQLSe9nLw7kmvU2AEUgaWn5vvPQMFs1Q7XwqKBy7TD5xR1DLX4bQ/viewform?resourcekey=0-zRsM2reDM3QjxegIUluHJA&%3Bpli=1&hl=zh-tw)。

## 刪除產品資訊

刪除商品後，訂閱者就無法再[查看商品](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。刪除房源也會[刪除所有連結的資料集](#remove_a_subscription)，並從訂閱者專案中移除所有訂閱項目。如果資料集仍處於連結狀態，請依序點選 person\_add「共用」**> 管理訂閱**，手動移除資料集。在「訂閱項目」頁面中，
一次移除特定訂閱者資料集或所有訂閱者資料集。

您無法刪除有有效商業訂閱項目的[與 Cloud Marketplace 整合的產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)。您必須先[撤銷所有商業訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#revoke-subscription)，才能刪除商家資訊。

**注意：** 撤銷[與 Cloud Marketplace 整合的商業訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)可能會影響客戶，並違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。

刪除多區域項目不會一併刪除共用資料集副本。刪除多區域房源後，訂閱者就無法再查看房源或查詢連結的資料集。如果沒有其他房源參照共用資料集副本，您可以[刪除這些副本](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#remove_a_dataset_replica)。

刪除多區域房源資訊前，請先確認房源資訊沒有有效訂閱項目。如有有效訂閱項目，請呼叫 [`projects.locations.subscriptions.revoke` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/revoke?hl=zh-tw)來撤銷訂閱。移除所有有效訂閱項目後，即可刪除多區域上架資訊。

**注意：** 商家資訊一經刪除即無法復原。

如要刪除房源資訊，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有商家資訊的資料交換名稱。
3. 按一下要刪除的房源資訊。
4. 按一下「刪除」圖示 delete。
5. 在「Delete listing?」(刪除房源？) 對話方塊中，輸入 `delete` 確認刪除。
6. 點選「刪除」。

### API

呼叫 [`projects.locations.dataExchanges.listings.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/delete?hl=zh-tw)：

```
DELETE https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID
```

更改下列內容：

* `PROJECT_ID`：包含資料交換的專案 ID。
* `LOCATION`：資料交易所的位置。
* `DATAEXCHANGE_ID`：資料交換 ID。
* `LISTING_ID`：要刪除的房源 ID。

如要進一步瞭解如何使用 API 對商家資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

## 後續步驟

* 瞭解 [BigQuery sharing 架構](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#architecture)。
* 瞭解如何[查看及訂閱房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。
* 瞭解 [BigQuery 共用 IAM 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#user_roles)。
* 瞭解如何[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。
* 瞭解 [BigQuery sharing 稽核記錄](https://docs.cloud.google.com/bigquery/docs/analytics-hub-audit-logging?hl=zh-tw)。
* 瞭解如何[監控商家資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-20 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-20 (世界標準時間)。"],[],[]]