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

在 BigQuery sharing (舊稱 Analytics Hub) 中，資料發布者可以建立及管理清單，安全地與各組織的訂閱者共用資料集，不必複製資料。

管理產品資訊時，您可以執行下列工作：

* 在您具備發布權限的任何資料交換中，建立、更新、共用及刪除清單。
* 將 BigQuery sharing 角色指派給管理員、訂閱者和檢視者，藉此管理存取權。
* 查看、監控及移除訂閱者。
* [監控訂閱項目用量指標](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw#use-analytics-hub)。

清單是發布端在[資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)中列出的共用資料集參照資訊。視為清單設定的身分與存取權管理 (IAM) 政策，以及包含清單的資料交換類型而定，清單可能屬於下列兩種類型之一：

* **公開資訊：**[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 可以[探索](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)及[訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)公開清單。公開資料交換中的清單即為公開清單。這些項目可以參照*免費公開資料集*或*商業資料集*。如果清單參照商業資料集，訂閱者可以直接向資料提供者要求存取清單，也可以瀏覽及購買[與 Google Cloud Marketplace 整合的商業清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)。
* **私人產品資訊。**私人產品資訊會直接與個人或群組共用。舉例來說，私人產品資訊可以參照您與組織內部團隊共用的行銷指標資料集。即使您[允許所有 Google Cloud 使用者 (`allAuthenticatedUsers`)](#give_users_access_to_a_listing) 訂閱私人產品，該產品仍會保持私人狀態。[BigQuery 共用頁面](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)不會公開顯示。如要與使用者分享私人產品資訊，請將產品資訊網址傳送給他們。如要公開私人清單，請[將資料交換設為公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)。

**注意：** 單一 BigQuery sharing 項目同時支援要求存取權和 Cloud Marketplace 整合流程。因此，您可以從現有的 (離線) 商業產品資訊建立與 Cloud Marketplace 整合的產品資訊，而不會中斷現有的訂閱項目。

## 事前準備

如要開始使用 BigQuery sharing (舊稱 Analytics Hub)，請在 Google Cloud 專案中啟用 Analytics Hub API。

如要啟用 Analytics Hub API，您必須具備下列 Identity and Access Management (IAM) 權限：

* `serviceUsage.services.get`
* `serviceUsage.services.list`
* `serviceUsage.services.enable`

下列預先定義的 IAM 角色包含啟用 Analytics Hub API 所需的權限：

* [服務使用情形管理員](https://docs.cloud.google.com/service-usage/docs/access-control?hl=zh-tw#serviceusage.serviceUsageAdmin) (`roles/serviceusage.serviceUsageAdmin`)

如要啟用 Analytics Hub API，請選取下列其中一個選項：

### 控制台

前往「**Analytics Hub API**」頁面，為 Google Cloud 專案啟用 Analytics Hub API。

[啟用 Analytics Hub API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### gcloud

執行 [gcloud services enable](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw) 指令：

```
gcloud services enable analyticshub.googleapis.com
```

### 必要的角色

如要管理清單和訂閱項目，您必須具備下列其中一個 BigQuery 共用 Identity and Access Management (IAM) 角色：

* [Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.publisher) (`roles/analyticshub.publisher`)：可建立、更新、刪除項目，以及設定項目的 IAM 政策。
* [Analytics Hub 清單管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.listingAdmin) (`roles/analyticshub.listingAdmin`)：可更新、刪除及設定清單的 IAM 政策。
* [Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.admin) (`roles/analyticshub.admin`)：可建立、更新、刪除資料交換中的所有產品資訊，以及設定相關 IAM 政策。

詳情請參閱「[BigQuery 共用 IAM 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#user_roles)」。如要瞭解如何將這些角色授予其他使用者，請參閱「[建立產品資訊管理員](#create-listing-administrator)」。

如要建立項目或更新項目的副本區域，您必須具備來源資料集的 `bigquery.datasets.get` 和 `bigquery.datasets.update` 權限。下列 [BigQuery 預先定義的角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)包含 `bigquery.datasets.update` 權限：

* [BigQuery 資料擁有者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner) (`roles/bigquery.dataOwner`)
* [BigQuery 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin) (`roles/bigquery.admin`)

如要查看您有權存取的組織中，所有專案的資料交換，您必須具備 `resourcemanager.organizations.get` 權限。BigQuery 預先定義的角色不含這項權限，因此您必須使用 [IAM 自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。

## 查看資料交換

如要查看貴組織中可存取的資料交換清單，請參閱「[查看資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#view_data_exchanges)」。如果資料交換庫位於其他組織，BigQuery 共用管理員必須與您[共用資料交換庫連結](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#share_a_data_exchange)。

## 建立產品資訊

「清單」是 BigQuery 共用發布者在資料交換中列出的[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)參照資訊。

**注意：** 建議您不要在Google Cloud 使用 VPC Service Controls service perimeter 的專案中建立共用資料集。如果必須使用 service perimeter，則須設定必要的[輸入和輸出規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw#create_a_listing)。

如要建立產品資訊，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

   頁面會列出您可存取的所有資料交換。
2. 按一下要建立產品資訊的資料交換作業名稱。
3. 按一下「add\_box 建立商店資訊」。
4. 在「Configure data」(設定資料) 區段的「Resource type」(資源類型) 選單中，選取「BigQuery dataset」(BigQuery 資料集) 或「Pub/Sub Topic」(Pub/Sub 主題)。

   * 如果選取「BigQuery dataset」(BigQuery 資料集)，請執行下列操作：

     1. 在「Shared dataset」(共用資料集) 選單中，選取現有資料集，或按一下「Create a dataset」(建立資料集) 建立資料集。資料集必須與資料交換位於相同區域。建立清單後，即無法變更共用資料集。訂閱者[查看連結資料集的中繼資料](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#view-table-metadata)時，BigQuery sharing 功能會傳回來源資料集名稱，以及包含該資料集的專案 ID。
     2. 選用：如要允許訂閱者[在不同清單中共用 SQL 預存程序](#share-stored-procedure-in-listing)，請選取「Allow stored procedure sharing」(允許共用預存程序) ([預先發布版](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages))。
     3. 如要在其他區域提供共用資料集，請展開「Region data availability」(區域資料可用性) 選單。選單會顯示已有資料集副本的區域，並標示為「可供使用」。為多個區域設定項目之前，請確認您已在共用資料集啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)功能。您只能選取已啟用跨區域資料集複製功能的區域，其他區域都會標示為「無法使用」。如未選取其他區域，產品預設會使用共用資料集的主要區域，並標示為「Provider primary」(供應商主要區域)。
     4. 在「Data Egress controls」(資料輸出控制項) 中，選取適當的資料輸出選項：

        + 如要限制共用資料集的資料複製和匯出功能，但允許匯出查詢結果，請選取「Disable copy and export of shared data」(停用共用資料複製與匯出功能)。
        + 如要限制共用資料集和查詢結果的資料複製和匯出功能，請選取「Disable copy and export of query results」(停用查詢結果複製與匯出功能)。選取這個選項後，系統也會選取「停用共用資料複製與匯出功能」。
        + 如要限制透過 API 複製及匯出共用資料集中的資料表，請選取「Disable copy and export of tables through APIs」(停用透過 API 複製及匯出資料表的功能)。選取這個選項後，系統也會選取「停用共用資料複製與匯出功能」。

        如要進一步瞭解資料輸出控制項 (包括限制)，請參閱「[資料輸出選項 (僅限 BigQuery 共用資料集)](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)」。
   * 如果選取「Pub/Sub Topic」(Pub/Sub 主題)，請在「Shared topic」(共用主題) 選單中選取現有的 Pub/Sub 主題，或按一下「Create a topic」(建立主題) 建立主題。
5. 在「Listing details」(產品資訊詳細資料) 部分的「Display name」(顯示名稱) 中，輸入產品資訊的名稱。
6. 輸入下列選填詳細資料：

   * **類別**：最多可選取五個最能代表產品資訊的類別。訂閱者可以使用您選取的類別[篩選產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * **資料相依性**：指定用於發布資料的區域。這項位置設定可讓訂閱者從相同區域讀取資料，盡可能降低或避免 Pub/Sub 網路輸出費用。如要進一步瞭解輸出費用，請參閱「[資料移轉費用](https://cloud.google.com/pubsub/pricing?hl=zh-tw#egress_costs)」。
   * **圖示**：上傳產品資訊的圖示。支援 PNG 和 JPEG 檔案格式。圖示大小必須小於 512 KiB，尺寸上限為 512 x 512 像素。
   * **說明**：輸入產品資訊的簡短說明。訂閱者可以依說明文字[搜尋產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * **公開曝光度**：開啟這項設定，即可在 BigQuery 共用目錄中公開顯示清單。如果啟用這個選項，請將 [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`) 授予 `allUsers` 或 `allAuthenticatedUsers`。詳情請參閱「[授予產品資訊的角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。如果交換作業已設為[公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)，清單會沿用這些權限，您不需採取進一步行動。

     由於權限繼承，公開可搜尋的交換庫無法包含私人清單項目，但私人交換庫可以包含公開清單項目。如要建立公開產品資訊，含有該產品資訊的專案必須有相關聯的組織和帳單帳戶。如果您建立[與 Cloud Marketplace 整合的商業產品](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，建議您開啟公開曝光功能。
   * **訂閱端電子郵件記錄**：開啟這項設定，即可記錄所有在連結資料集執行工作和查詢的使用者[主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。如果啟用這個選項，日後透過這個清單建立的所有訂閱項目，都會啟用訂閱者電子郵件記錄功能。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄中。

     **注意：** 啟用並儲存訂閱端電子郵件記錄功能後，就無法編輯這項設定。如要關閉電子郵件記錄功能，請刪除清單項目，然後重新建立清單項目，但不要選取「Subscriber email logging」(訂閱者電子郵件記錄)。
   * **Documentation > Markdown**：以 Markdown 格式輸入支援文件、連結或操作說明，協助訂閱者使用資料集。
7. 在「Listing contact information」(產品資訊聯絡資訊) 部分，輸入下列選填詳細資料：

   * **主要聯絡人**：輸入產品資訊主要聯絡人的電子郵件地址或網址。
   * **要求存取權聯絡資訊**：輸入電子郵件地址或受理表單網址，方便訂閱者與您聯絡，要求存取權。
   * **供應商**：展開「供應商」部分，並在下列欄位中輸入詳細資料：

     + **供應商名稱**：資料供應商的名稱。
     + **供應商主要聯絡人**：資料供應商主要聯絡人的電子郵件地址或網址。

     訂閱者可以依資料供應商篩選清單。
   * **Publisher**：展開「Publisher」部分，並在下列欄位中輸入詳細資料：

     + **發布商名稱**：建立產品資訊的發布商名稱。
     + **發布商主要聯絡人**：發布商主要聯絡人的電子郵件地址或網址。
8. 查看「商店資訊預覽」部分。
9. 如要發布產品資訊，請按一下「發布」。

### API

請使用 [`projects.locations.dataExchanges.listings.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/create?hl=zh-tw)：

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings?listingId=LISTING_ID
```

更改下列內容：

* `PROJECT_ID`：專案 ID，該專案含有您要建立清單的資料交換。
* `LOCATION`：資料交換的位置。如要進一步瞭解支援 BigQuery 共用的位置，請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
* `DATAEXCHANGE_ID`：資料交換作業 ID。
* `LISTING_ID`：：產品資訊 ID。

在要求主體中提供[產品資訊詳細資料](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#resource:-listing)。

如要在多個區域建立產品資訊，請在要求主體的 `bigqueryDataset.replicaLocations` 欄位中指定這些區域。為多個區域設定產品資訊前，請確認您已在共用資料集啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)功能。您只能選取已啟用跨區域資料集複製功能的區域。如果省略這個選填欄位，清單會使用共用資料集的主要區域。

如果要求成功，回應主體會傳回產品資訊詳細資料。如果將 `logLinkedDatasetQueryUserEmail` 欄位設為 `true`，啟用訂閱端電子郵件記錄功能，清單項目回應會傳回 `log_linked_dataset_query_user_email: true`。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄中。

如要進一步瞭解如何使用 API 對產品資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

### 從資料集建立產品資訊

如要直接從現有資料集建立產品資訊，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如要查看資料集詳細資料，請按一下資料集名稱。
3. 依序點選「person\_add 共用」「發布為清單」。

   「建立產品資訊」對話方塊隨即開啟。
4. 選取要發布清單項目的資料交換。資料交換必須與資料集位於相同區域。如要進一步瞭解如何建立資料交換，請參閱「[建立交換作業並設定權限](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)」。
5. 在「Shared dataset」(共用資料集) 選單中，選取現有資料集，或按一下「Create a dataset」(建立資料集) 建立資料集。資料集必須與資料交換作業位於相同區域。建立商店資訊後，就無法變更這項設定。

   訂閱者[查看連結資料集的中繼資料](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#view-table-metadata)時，BigQuery sharing 功能會傳回來源資料集名稱，以及包含該資料集的專案 ID。
6. 選用：如要允許訂閱者[在不同清單中共用 SQL 預存程序](#share-stored-procedure-in-listing)，請選取「Allow stored procedure sharing」(允許共用預存程序) ([預先發布版](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages))。
7. 如要在其他區域提供共用資料集，請展開「Region data availability」(區域資料可用性) 選單。選單會顯示含有資料集副本的區域，並標示為「Ready to use」(可供使用)。為多個區域設定產品資訊前，請確認您已在共用資料集啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)功能。您只能選取已啟用跨區域資料集複製功能的區域，其他區域都會標示為「無法使用」。如未選取其他區域，產品預設會設為共用資料集的主要區域，並標示為「Provider primary」(供應商主要區域)。
8. 在「Data egress controls」(資料輸出控制項) 中，選取適當的資料輸出選項：

   * 如要限制共用資料集的複製和匯出功能，但允許匯出查詢結果，請選取「Disable copy and export of shared data」(停用共用資料複製與匯出功能)。
   * 如要限制共用資料集和查詢結果的複製與匯出功能，請選取「Disable copy and export of query results」(停用查詢結果複製與匯出功能)。這個選項也會選取「停用共用資料複製與匯出功能」。
   * 如要限制透過 API 複製及匯出共用資料集中的資料表，請選取「Disable copy and export of tables through APIs」(停用透過 API 複製及匯出資料表的功能)。選取這個選項後，系統也會選取「停用共用資料複製與匯出功能」。

   如要瞭解資料輸出控管和限制，請參閱「[資料輸出選項 (僅限 BigQuery 共用資料集)](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_egress)」。
9. 在「Listing details」(產品資訊詳細資料) 區段的「Display name」(顯示名稱) 中，輸入產品資訊的名稱。
10. 輸入下列選填詳細資料：

    * **類別**：最多可選取五個最能代表產品資訊的類別。訂閱者可以使用您選取的類別[篩選產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
    * **資料相依性**：指定用於發布資料的區域。這項位置設定可讓訂閱者從相同區域讀取資料，盡可能降低或避免 Pub/Sub 網路輸出費用。如要進一步瞭解輸出費用，請參閱「[資料移轉費用](https://cloud.google.com/pubsub/pricing?hl=zh-tw#egress_costs)」。
    * **圖示**：上傳產品資訊的圖示。支援 PNG 和 JPEG 檔案格式。圖示必須小於 512 KiB，最大尺寸為 512 x 512 像素。
    * **說明**：輸入產品資訊的簡短說明。訂閱者可以透過說明文字[搜尋清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
    * **公開曝光度**：開啟這項設定，即可在 BigQuery 共用目錄中公開顯示產品資訊。如果啟用這個選項，請將 Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`) 授予 `allUsers` 或 `allAuthenticatedUsers`。詳情請參閱「[授予清單角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。如果交換作業已設為[公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)，清單會沿用這些權限，您不需採取進一步行動。

      由於權限繼承，公開可搜尋的交換庫不能有私人清單項目，但私人交換庫可以有公開清單項目。如要建立公開產品資訊，含有該產品資訊的專案必須有相關聯的組織和帳單帳戶。如果您建立[與 Cloud Marketplace 整合的商業產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，建議開啟公開曝光度。
    * **訂閱端電子郵件記錄**：開啟這項功能，即可記錄訂閱端[主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)，以便掌握日後所有訂閱項目對此清單項目連結資料集執行的工作和查詢。啟用這個選項後，只有新建立的訂閱項目會記錄主體 ID。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄中。

      **注意：** 啟用並儲存訂閱端電子郵件記錄功能後，就無法編輯這項設定。如要關閉電子郵件記錄功能，請刪除清單項目，然後重新建立清單項目，但不要選取「Subscriber email logging」(訂閱者電子郵件記錄)。
    * **說明文件 > Markdown**：輸入支援文件、連結或操作說明，協助訂閱者使用資料集。
11. 在「Listing contact information」(產品資訊聯絡資訊) 部分，輸入下列選填詳細資料：

    * **主要聯絡人**：輸入產品資訊主要聯絡人的電子郵件地址或網址。
    * **要求存取權聯絡資訊**：輸入電子郵件地址或受理表單網址，方便訂閱者與您聯絡並要求存取權。
    * **供應商**：展開「供應商」部分，並在下列欄位中輸入詳細資料：

      + **供應商名稱**：資料供應商的名稱。
      + **供應商主要聯絡人**：資料供應商主要聯絡人的電子郵件地址或網址。

      訂閱者可以依資料供應商篩選清單。
    * **發布商**：展開「發布商」部分，並在下列欄位中輸入詳細資料：

      + **發布商名稱**：建立產品資訊的發布商名稱。
      + **發布商主要聯絡人**：發布商主要聯絡人的電子郵件地址或網址。
12. 查看「商店資訊預覽」部分。
13. 如要發布產品資訊，請按一下「發布」。

## 在不同產品資訊之間共用 SQL 預存程序

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-data-sharing-feedback@google.com](mailto:bq-data-sharing-feedback@google.com)。

使用 BigQuery 資料集建立清單時，您可以共用 [SQL 預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)。由於預存程序可以建立、刪除及操控資料表，並叫用其他預存程序，因此共用預存程序需要額外授權。

### 訂閱者授權

訂閱者訂閱項目後，連結的預存程序可能不會立即執行。為確保連結的預存程序可以執行，訂閱者必須將連結的資料集名稱傳送給提供者，以便[提供者授權提供者資源上連結的預存程序](#provider-authorization)。此外，訂閱者必須[授權連結的共用預存程序，並將 IAM 角色附加](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw#bq-attach-role)至訂閱者的資源，才能讀取及寫入這些資源。

### 供應商授權

提供者使用預存程序建立清單時，必須允許訂閱者透過連結的預存程序，讀取及寫入提供者的資料表。為確保能順利存取，供應商必須執行下列操作：

* 如要執行非讀取作業，請授權連結的共用預存程序，並將 [IAM 角色附加](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw#bq-attach-role)至連結預存程序存取的任何提供者資源。
* 如要執行讀取作業，請授權連結的共用預存程序 (位於訂閱者的連結資料集)，或原始共用預存程序 (位於供應商的資料集)，並將 IAM 角色附加至程序存取的任何供應商資源。

## 授予使用者清單存取權

如要提供私人產品資訊的存取權，您必須設定該產品資訊的 IAM 政策，納入特定個人或群組。如果是商業產品資訊，[資料交換必須公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)。公開資料交換中的項目會顯示在所有[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 的 BigQuery sharing 中。如要允許使用者瀏覽及要求存取商業項目，請授予[Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.viewer`)。如要允許使用者訂閱商業項目，請授予 [Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`)。如果是[與 Cloud Marketplace 整合的商業項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，BigQuery sharing 會根據 Cloud Marketplace 訂單自動授予 Analytics Hub 訂閱者角色。

如要讓所有人 (包括沒有Google Cloud 帳戶的使用者) 都能存取您的資訊，請將 Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`) 授予`allUsers`。

如要授予使用者檢視或訂閱產品資訊的權限，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有該項目的資料交換作業名稱。
3. 按一下要分享的產品資訊。
4. 按一下「person 設定權限」。
5. 如要新增主體，請按一下「person\_add 新增主體」。
6. 在「New principals」(新增主體) 欄位中，根據產品資訊類型輸入主體：

   * 如果是私人產品，請輸入要授予存取權的身分電子郵件地址。
   * 如果是公開產品資訊，請輸入 `allAuthenticatedUsers`。
   * 如要讓所有人 (包括非Google Cloud使用者) 都能找到公開產品資訊，請輸入 `allUsers`。
7. 在「Select a role」(選取角色) 選單中，指向「Analytics Hub」，然後根據清單類型選取角色：

   * 如果是商業產品資訊 (包括與 Cloud Marketplace 整合的產品資訊)，請選取「Analytics Hub Viewer」(Analytics Hub 檢視者)。具備這個角色的使用者可以[查看清單並要求存取權](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * 如果是私人或非商業用途的公開項目，請選取「Analytics Hub Subscriber」(Analytics Hub 訂閱者)。具備這個角色的使用者可以[訂閱您的產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)。
   * 如果是與 Cloud Marketplace 整合的項目，您不需要授予 Analytics Hub 訂閱者角色 (`roles/analyticshub.subscriber`)。系統會根據 Cloud Marketplace 訂單自動管理訂閱項目。**注意：** 授予授權，讓使用者存取非 Cloud Marketplace 整合的商業產品後，您可以為這些使用者[建立私人產品](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)，或在商業產品上授予[Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`)。

   詳情請參閱「[Analytics Hub 訂閱者和檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role)」。
8. 如要儲存權限，請按一下「儲存」。

### API

1. 呼叫 [`projects.locations.dataExchanges.listings.getIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/getIamPolicy?hl=zh-tw)，讀取現有政策：

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:getIamPolicy
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID，例如 `my-project-1`。
   * `LOCATION`：
     含有清單的資料交換位置。
   * `DATAEXCHANGE_ID`：資料交換作業 ID。
   * `LISTING_ID`：：產品資訊 ID。

   共用設定會在回應中傳回目前的政策。
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
3. 呼叫 [`projects.locations.dataExchanges.listings.setIamPolicy` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/setIamPolicy?hl=zh-tw)來更新政策。在要求主體中，傳遞上一個步驟中更新的 IAM 政策。

   ```
   POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:setIamPolicy
   ```

   在要求主體中傳遞產品資訊詳細資料。如果要求成功，回應主體會傳回含有更新政策的產品資訊詳細資料。

如要進一步瞭解如何使用 API 對產品資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

**注意：** 將商業產品資訊的存取權授權給使用者後，您可以為這些使用者[建立私人產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)，或授予他們商業產品資訊的 Analytics Hub 訂閱者角色 (`roles/analyticshub.subscriber`)。

### 為公開產品資訊建立未經驗證的網址

如要建立未經驗證的 BigQuery 共用資訊清單網址，讓沒有 Google Cloud 帳戶的使用者查看，請按照下列步驟操作：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

   頁面會列出您可存取的所有資料交換。
2. 按一下含有該項目的資料交換作業名稱。
3. 如要查看清單詳細資料，請按一下清單顯示名稱。清單項目必須啟用[公開搜尋](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)功能。
4. 點按「複製公開連結」。為確保外部使用者可以查看清單，請確認清單已授予 `allUsers` Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。

### 建立產品資訊管理員

如要讓使用者管理清單，您可以建立清單管理員，方法是將清單的 [Analytics Hub 發布者或 Analytics Hub 清單管理員角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role)授予這些使用者。如需授予產品資訊角色的操作說明，請參閱「[授予產品資訊角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。

## 查看所有訂閱項目

如要查看目前所有訂閱項目，請選取下列其中一個選項：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下資料交換名稱，其中包含您要管理訂閱項目的清單。
3. 按一下要列出所有訂閱者的產品資訊。
4. 如要查看產品資訊的所有訂閱者，請按一下「Manage subscriptions」(管理訂閱項目)：
5. 選用：您可以依訂閱者詳細資料篩選結果。

或者，如果您有[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)的存取權，可以按照下列步驟列出訂閱者：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案名稱，依序點選「Datasets」(資料集) 和共用資料集的名稱。
4. 在 person\_add「Sharing」(共用) 清單中，選取「Manage subscriptions」(管理訂閱項目)。

### SQL

下列範例使用 [`INFORMATION_SCHEMA.SCHEMATA_LINKS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata-links?hl=zh-tw)，列出 `us` 區域中 `myproject` 內連結至共用資料集的所有連結資料集：

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

如果清單包含多個區域，您可以將 `us` 區域替換為預期的副本位置，查看不同區域的訂閱項目。舉例來說，如要查看 `eu` 區域中 `myproject` 內共用資料集的連結資料集，請使用下列查詢：

```
SELECT * FROM `myproject`.`region-eu`.INFORMATION_SCHEMA.SCHEMATA_LINKS;
```

### API

請使用 [`projects.locations.dataExchanges.listings.listSubscriptions` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/listSubscriptions?hl=zh-tw)。

```
GET https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:listSubscriptions
```

更改下列內容：

* `PROJECT_ID`：要訂閱的清單專案 ID。
* `LOCATION`：要訂閱的產品資訊位置。
* `DATAEXCHANGE_ID`：資料交換 ID，其中包含您要訂閱的清單。
* `LISTING_ID`：要訂閱的清單 ID。

## 移除訂閱項目

如果從清單中移除 2023 年 7 月 25 日前建立的訂閱項目，[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)會與[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)取消連結。訂閱者仍可在專案中查看資料集，但資料集不會再連結至共用資料集。

**注意：** 撤銷[與 Cloud Marketplace 整合的商業訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，可能會影響客戶，且可能違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。

如要從商店資訊中移除 2023 年 7 月 25 日前建立的訂閱項目，請按照下列步驟操作：

1. 如要列出產品資訊的訂閱者，請按照 Google Cloud 控制台的[查看所有訂閱項目](#view_all_subscriptions)操作說明進行。
2. 如要從清單中移除訂閱者，請按一下 delete「Delete」(刪除)。如要移除所有訂閱項目，請按一下「Remove all subscriptions」(移除所有訂閱項目)。
3. 在「Remove subscription?」(要移除訂閱項目嗎？) 對話方塊中，輸入 `remove` 確認刪除。
4. 按一下 [移除]。

如要移除 2023 年 7 月 25 日後建立的訂閱項目，請按照下列步驟操作：

### 控制台

1. 如要列出產品資訊的訂閱者，請按照 Google Cloud 控制台的[查看所有訂閱項目](#view_all_subscriptions)操作說明進行。
2. 按一下「訂閱項目」。
3. 如要選取要移除的訂閱項目，請勾選這些訂閱項目旁的核取方塊，然後按一下「delete Remove Subscriptions」(移除訂閱項目)。
4. 在「Remove subscription?」(要移除訂閱項目嗎？) 對話方塊中，輸入 `remove` 確認移除。
5. 按一下 [移除]。

### API

呼叫 [`projects.locations.subscriptions.revoke` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/revoke?hl=zh-tw)：

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/subscriptions/SUBSCRIPTION_ID:revoke
```

更改下列內容：

* `PROJECT_ID`：要移除的訂閱項目專案 ID。
* `LOCATION`：要移除的訂閱項目位置。
* `SUBSCRIPTION_ID`：要移除的[訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#list_subscriptions) ID。

## 更新商店資訊

隨著資料交換需求演變，您可以更新清單的中繼資料、類別、可搜尋性設定和區域可用性，而不必修改基礎共用資料集。

如果 Google Cloud 專案使用 VPC Service Controls service perimeter，您可能需要設定額外的[輸入和輸出規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw#update-listing)，允許背景同步處理作業更新相關聯的連結資料集。

如要更新商店資訊，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有該項目的資料交換作業名稱。
3. 按一下要更新的商店資訊。
4. 按一下「mode\_edit 編輯商店資訊」。
5. 修改欄位中的值。除了清單的共用資料集外，您可以修改所有值。
6. 選用：更新商店資訊設定和供應情形：

   * 如要啟用公開探索功能，請將 [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`) 授予 `allUsers` 或 `allAuthenticatedUsers`。如需授予產品資訊角色的操作說明，請參閱「[授予產品資訊角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#grant-role-listing)」。
   * 如要停用私人交換所中產品資訊的公開搜尋功能，請從 `allUsers` 和 `allAuthenticatedUsers` 移除 Analytics Hub 檢視者角色 (`roles/analyticshub.viewer`)。如果 Exchange 已設為[公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)，則會沿用清單權限，您無須採取進一步行動。
   * 啟用並儲存訂閱端電子郵件記錄功能後，就無法編輯這項設定。如要關閉電子郵件記錄功能，請刪除清單項目，然後重新建立清單項目，但不要選取「Subscriber email logging」(訂閱者電子郵件記錄)。
   * 如要新增或移除區域，請更新區域選項。新增多個區域前，請確認您已在共用資料集啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)功能。移除區域前，請先刪除該區域中的共用資料集副本。
7. 查看商店資訊預覽。
8. 按一下「儲存」即可儲存變更。如果您更新與 Cloud Marketplace 整合的產品資訊，系統會提示您一併更新 Cloud Marketplace 資料產品資訊。

   **注意：** 更新 Cloud Marketplace 資料產品資訊，必須經過 Marketplace 營運團隊審查及核准。

### API

呼叫 [`projects.locations.dataExchanges.listings.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/patch?hl=zh-tw)：

```
PATCH https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID?updateMask=UPDATEMASK
```

更改下列內容：

* `PROJECT_ID`：專案 ID，該專案包含您要建立清單的資料交換。
* `LOCATION`：資料交換作業的位置。
* `DATAEXCHANGE_ID`：資料交換作業的 ID。
* `LISTING_ID`：要更新的產品資訊 ID。
* `UPDATEMASK`：要更新的欄位清單。如要更新多個值，請使用以半形逗號分隔的清單。舉例來說，如要更新資料交換作業的顯示名稱和主要聯絡人，請輸入 `displayName,primaryContact`。

在要求主體中，為更新遮罩中的欄位指定更新值：

* `displayName`
* `description`
* `primaryContact`
* `documentation`
* `icon`
* `categories[]`
* `discoveryType`
* `logLinkedDatasetQueryUserEmail`
* `bigqueryDataset.replicaLocations`

如要進一步瞭解這些欄位，請參閱「[資源：清單](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#resource:-listing)」。

更新產品資訊的副本區域時，請指定所有適用區域。更新產品資訊前，請確認您已在共用資料集啟用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#use_dataset_replication)功能。您只能新增共用資料集副本所在的區域。從清單中移除區域前，請先刪除該區域中的共用資料集副本。您也可以將單一區域產品轉換為多區域產品。

如要進一步瞭解如何使用 API 對產品資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

## 在「精選內容」專區顯示商店資訊

如要提高產品資訊在 BigQuery sharing 目錄中的曝光度，可以在「Featured」(精選) 專區中顯示產品資訊。精選產品資訊受 Google Cloud 《合作夥伴計畫協議》規範。

如要申請在「精選」部分顯示產品資訊，必須符合下列條件：

* 共用資料必須位於 BigQuery。
* 您必須加入 Google Cloud 技術合作夥伴計畫中的 [Google Cloud Partner Network 計畫](https://partners.cloud.google.com/?hl=zh-tw)。
* 您必須建立商店資訊，並開啟[公開曝光度](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)。

如要申請將產品資訊加入「精選」專區，或從該專區移除產品資訊，請提交[精選產品資訊登記表單](https://docs.google.com/forms/d/e/1FAIpQLSe9nLw7kmvU2AEUgaWn5vvPQMFs1Q7XwqKBy7TD5xR1DLX4bQ/viewform?resourcekey=0-zRsM2reDM3QjxegIUluHJA&%3Bpli=1&hl=zh-tw)。

## 刪除商家資訊

刪除產品資訊後，訂閱者就無法再[查看產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。刪除清單也會[刪除所有連結的資料集](#remove_a_subscription)，並從訂閱者專案中移除所有訂閱項目。如果資料集仍處於連結狀態，請依序點選
person\_add
**「Sharing」(共用) >「Manage Subscription」(管理訂閱項目)**，手動移除資料集。在「Subscriptions」(訂閱項目) 頁面中，移除特定訂閱者資料集，或一次移除所有訂閱者資料集。

您無法刪除具有有效商業訂閱項目的[與 Cloud Marketplace 整合的產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)。您必須先[撤銷所有商業訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#revoke-subscription)，才能刪除產品資訊。

**注意：** 撤銷[與 Cloud Marketplace 整合的商業訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)，可能會影響客戶，且可能違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。

刪除多區域產品資訊不會刪除共用資料集副本。
刪除多區域清單後，訂閱者就無法再查看清單或查詢連結的資料集。如果沒有其他產品資訊參照共用資料集副本，您可以[刪除這些副本](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#remove_a_dataset_replica)。

刪除多區域產品資訊前，請先確認該產品資訊沒有任何有效訂閱項目。如果存在有效訂閱項目，請呼叫 [`projects.locations.subscriptions.revoke` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/revoke?hl=zh-tw)撤銷。移除所有有效訂閱項目後，請刪除多區域產品資訊。

**注意：** 商家資訊一經刪除即無法復原。

如要刪除商店資訊，請按照下列步驟操作：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有該項目的資料交換作業名稱。
3. 按一下要刪除的商店資訊。
4. 按一下「刪除」圖示 delete。
5. 在「Delete listing?」(要刪除產品資訊嗎？) 對話方塊中，輸入 `delete` 確認刪除。
6. 點選「刪除」。

### API

呼叫 [`projects.locations.dataExchanges.listings.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/delete?hl=zh-tw)：

```
DELETE https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID
```

更改下列內容：

* `PROJECT_ID`：資料交換所在專案的 ID。
* `LOCATION`：資料交換作業的位置。
* `DATAEXCHANGE_ID`：資料交換作業的 ID。
* `LISTING_ID`：要刪除的產品資訊 ID。

如要進一步瞭解如何使用 API 對產品資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

## 後續步驟

* 瞭解 [BigQuery 共用架構](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#architecture)。
* 瞭解如何[查看及訂閱產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。
* 瞭解 [BigQuery 共用 IAM 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#user_roles)。
* 瞭解如何[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。
* 瞭解 [BigQuery 共用稽核記錄](https://docs.cloud.google.com/bigquery/docs/analytics-hub-audit-logging?hl=zh-tw)。
* 瞭解如何[監控商店資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]