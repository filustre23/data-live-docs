Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過 Pub/Sub 共用串流

您可以透過 BigQuery sharing (舊稱 Analytics Hub) 共用 Pub/Sub 主題，在多個內部和外部組織界限之間，收錄及發布串流資料庫。即時串流資料會透過 BigQuery sharing 交換和資訊清單共用，讓您以邏輯方式分類及分組大量 Pub/Sub 主題，並大規模佈建存取權。

你可以分享串流資料，以便執行下列操作：

* **金融服務**：
  + 即時分享快速變動的工具價格、報價和訂單。
  + 偵測洗錢和付款詐欺行為。
  + 支援交易風險運算。
* **零售和民生消費用品業 (CPG)**：
  + 即時管理商店商品目錄。
  + 提供個人化行銷和客戶服務。
  + 動態調整價格。
  + 監控社群媒體管道。
  + 最佳化實體商店版面配置。
* **醫療照護**：
  + 運用預測演算法，即時監控病患並分析風險。
  + 使用穿戴式醫療器材監控生命徵象。
  + 自動擷取、建構、儲存及處理病患、專業醫護人員和機構管理部門的資料。
* **電信**：
  + 監控網路健康狀態並預測故障。
  + 探索使用者行為模式，更準確地定位裝置和天線。

## 必要的角色

共用 Pub/Sub 主題的角色與共用 BigQuery 資料集類似：

* **管理員**：管理交換作業和清單的權限、瀏覽權限和成員資格。這個角色類似於 [Analytics Hub 管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-admin-role) (`roles/analyticshub.admin`) IAM 角色。
* **共用主題發布者**：建立、管理及授予共用 Pub/Sub 主題清單的存取權。這個角色類似於 [Analytics Hub 發布者或 Analytics Hub 清單管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) IAM 角色。發布者是使用者，而非建立訊息並傳送至主題的[發布者應用程式](https://docs.cloud.google.com/pubsub/docs/publisher?hl=zh-tw)。
* **共用主題訂閱者**：訂閱共用主題清單。共用主題訂閱者可以設定主題訊息的傳送方式。這個角色類似於 [Analytics Hub 訂閱者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role)或 [Analytics Hub 訂閱項目擁有者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscription-owner-role) IAM 角色。視訊息資料的傳送方式而定，可能需要額外權限，例如將訊息寫入 BigQuery 的 [Pub/Sub 服務帳戶權限](https://docs.cloud.google.com/pubsub/docs/bigquery?hl=zh-tw#service_account_permissions)。

## 架構

下圖說明 Pub/Sub 資源的發布者和訂閱者如何與 BigQuery 共用功能互動：

**圖 1：**共用主題發布者和訂閱者工作流程與 Pub/Sub 主題。

共用主題
:   共用主題是 BigQuery sharing 功能中，共用 Pub/Sub 主題的單位。共用主題發布者可以建立或使用現有的 Pub/Sub 主題，將訊息資料發布給訂閱者。BigQuery sharing 不會複製來源 Pub/Sub 主題。

清單
:   發布者將共用主題新增至資料交換庫時，系統會建立清單。它會參照共用主題。

廣告交易平台
:   交換庫是參照共用主題的清單邏輯分組。

連結的 Pub/Sub 訂閱項目
:   訂閱含有共用主題的清單時，系統會在共用主題訂閱者專案中，建立連結的 Pub/Sub 訂閱項目。共用主題發布者的專案也會將 Pub/Sub 訂閱項目，表示為 Pub/Sub 訂閱項目和共用項目訂閱項目。

## 限制

透過 Pub/Sub 共用串流時，有下列限制：

* 共用主題最多支援 10,000 個 Pub/Sub 訂閱項目。這項限制包含連結的 Pub/Sub 訂閱項目，以及在「共用」功能以外建立的 Pub/Sub 訂閱項目，例如直接透過 Pub/Sub 建立的訂閱項目。
* 共用主題會在 Knowledge Catalog 中建立索引，但您無法依資源類型篩選。
* 系統會擷取共用 Pub/Sub 主題和訂閱項目的用量指標，並顯示在「指標」資訊主頁中，但 `INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 不提供這些指標。

  如要監控指標，請參閱「[在 Cloud Monitoring 中監控 Pub/Sub](https://docs.cloud.google.com/pubsub/docs/monitoring?hl=zh-tw)」。

  這些指標包括：

  + 發布訊息數
  + 發布要求
  + 發布處理量 (以位元組為單位)
  + 前 5 名訂閱項目
  + 擷取的位元組數
  + 其他

### 啟用 Analytics Hub API

如要啟用 Analytics Hub API，請按照下列步驟操作：

### 控制台

前往 API 程式庫，為Google Cloud 專案啟用 Analytics Hub API。

[啟用 Analytics Hub API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### gcloud

執行 [`gcloud services enable`](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw) 指令：

```
gcloud services enable analyticshub.googleapis.com
```

### 啟用 Pub/Sub API

前往 API 程式庫，為 Google Cloud 專案啟用 Pub/Sub API。

[啟用 Pub/Sub API](https://console.cloud.google.com/apis/library/pubsub.googleapis.com?hl=zh-tw)

## 共用主題發布者工作流程

共用主題發布者可以執行下列操作：

* 建立清單，將共用主題新增至 Exchange。
* 更新商店資訊。
* 刪除產品資訊。
* 分享商店資訊。
* 管理產品資訊的訂閱項目。
* 從清單中移除訂閱者。

### 其他發布者權限

如要執行共用主題發布者工作，您必須具備交換或項目的 [Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) (`roles/analyticshub.publisher`)。如要查看您有權存取的組織中，所有專案的[資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)，您必須具備 `resourcemanager.organizations.get` 權限。

此外，您還需要具備要列出的 Pub/Sub 主題 `pubsub.topics.setIamPolicy` 權限。如要共用附加結構定義的主題，您必須將主題附加結構定義的 `pubsub.schemas.get` 權限，授予 BigQuery sharing 訂閱端。這項權限可讓 BigQuery sharing 訂閱端正確剖析 Pub/Sub 訂閱項目的訊息。

### 建立產品資訊 (新增共用主題)

如要將共用主題新增至產品資訊，請選取下列其中一個選項：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

   頁面會列出您可存取的所有資料交換。
2. 按一下要建立產品資訊的資料交換作業名稱。
3. 按一下「add\_box 建立商店資訊」。
4. 在「Create listing」(建立產品資訊) 頁面中，從「Resource type」(資源類型) 清單選取「Pub/Sub Topic」(Pub/Sub 主題)。
5. 從「Shared topic」(共用主題) 清單中選取現有的 Pub/Sub 主題，或按一下「Create a topic」(建立主題)。
6. 在「Listing details」(產品資訊詳細資料) 頁面的「Display name」(顯示名稱) 欄位中，輸入產品資訊名稱。
7. 輸入下列選填詳細資料：

   * **類別**：選取最多兩個最能代表產品資訊的類別。共用主題訂閱者可以根據這些類別[篩選清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * **資料相依性**：共用主題發布者用來發布資料的區域。共用主題訂閱者可根據這項資訊，從相同區域讀取資料，盡可能減少或避免 Pub/Sub 網路輸出費用。如要進一步瞭解輸出費用，請參閱「[資料移轉費用](https://cloud.google.com/pubsub/pricing?hl=zh-tw#egress_costs)」。
   * **圖示**：商店資訊的圖示。支援 PNG 和 JPEG 檔案格式。圖示必須小於 512 KiB，尺寸不得超過 512 x 512 像素。
   * **說明**：簡短說明產品資訊。共用主題訂閱者可以根據說明[搜尋清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * **公開曝光度**：在 BigQuery sharing 目錄中，啟用清單的公開曝光度。您也必須設定產品資訊的權限。按一下 Exchange 的「Actions」(動作)，然後按一下「Set permissions」(設定權限)。將 [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.viewer`) 授予 `allUsers` 或 `allAuthenticatedusers`。按一下「Allow Public Access」(允許公開存取)。
   * **說明文件 > Markdown**：其他資訊，例如相關說明文件的連結，以及其他有助於共用主題訂閱者使用主題的詳細資料。
8. 在「Listing contact information」(產品資訊聯絡資訊) 頁面中，輸入下列選填詳細資料：

   * **主要聯絡人**：輸入產品資訊主要聯絡人的電子郵件地址或網址。
   * **要求存取權聯絡資訊**：輸入電子郵件地址或受理表單網址，讓共用主題訂閱者與您聯絡。
   * **Provider**：展開「Provider」部分，並在下列欄位中指定詳細資料：

     + **供應商名稱**：主題供應商的名稱。
     + **Provider primary contact**：主題供應商主要聯絡人的電子郵件地址或網址。

     共用主題訂閱者可以根據資料供應商篩選清單。
   * **Publisher**：展開「Publisher」部分，並在下列欄位中指定詳細資料：

     + **發布者名稱**：建立項目的共用主題發布者名稱。
     + **發布者主要聯絡人**：共用主題發布者主要聯絡人的電子郵件地址或網址。
9. 查看「Listing preview」頁面。
10. 按一下「發布」。

### API

請使用 [`projects.locations.dataExchanges.listings.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/create?hl=zh-tw)。

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings?listingId=LISTING_ID
```

更改下列內容：

* `PROJECT_ID`：專案 ID，包含您要建立清單的資料交換。
* `LOCATION`：資料交換作業的位置。如要進一步瞭解支援共用功能的地區，請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
* `DATAEXCHANGE_ID`：資料交換作業 ID。
* `LISTING_ID`：：產品資訊 ID。

在要求主體中提供[產品資訊詳細資料](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#resource:-listing)。如果要求成功，回應主體會包含商店資訊詳細資料。

如要進一步瞭解如何使用 API 對產品資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

### 更新商店資訊

如要更新商店資訊，請選取下列其中一個選項：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有該項目的資料交換作業名稱。
3. 按一下要更新的商店資訊。
4. 按一下「mode\_edit 編輯商店資訊」。
5. 修改欄位值。除了產品資訊的共用主題外，您可以修改所有值。
6. 按一下「發布」即可儲存變更。

### API

請使用 [`projects.locations.dataExchanges.listings.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/patch?hl=zh-tw)。

```
PATCH https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID?updateMask=UPDATEMASK
```

更改下列內容：

* `PROJECT_ID`：專案 ID，包含您要建立清單的資料交換。
* `LOCATION`：資料交換作業的位置。如要進一步瞭解支援共用功能的地區，請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
* `DATAEXCHANGE_ID`：資料交換作業 ID。
* `LISTING_ID`：：產品資訊 ID。
* `UPDATEMASK`：要更新的欄位清單。如要更新多個值，請使用以半形逗號分隔的清單。

在要求主體中指定更新的值。

如要進一步瞭解如何使用 API 對產品資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

### 刪除商家資訊

如果共用的 Pub/Sub 主題有有效的訂閱項目，則無法刪除該主題的產品資訊。嘗試刪除共用主題資訊前，請先[撤銷所有有效訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-stream-sharing?hl=zh-tw#revoke_a_subscription)。刪除後即無法復原。

如要刪除商店資訊，請選擇下列其中一個選項：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有該項目的資料交換作業名稱。
3. 按一下要刪除的商店資訊。
4. 按一下「刪除」圖示 delete。
5. 在「Delete listing?」(要刪除產品資訊嗎？) 對話方塊中，輸入 `delete` 確認刪除。
6. 點選「刪除」。

### API

請使用 [`projects.locations.dataExchanges.listings.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/delete?hl=zh-tw)。

```
DELETE https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID
```

更改下列內容：

* `PROJECT_ID`：專案 ID，包含您要建立清單的資料交換。
* `LOCATION`：資料交換作業的位置。如要進一步瞭解支援共用功能的地區，請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
* `DATAEXCHANGE_ID`：資料交換作業 ID。
* `LISTING_ID`：：產品資訊 ID。

如要進一步瞭解如何使用 API 對產品資訊執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

### 分享商店資訊

如要授予使用者私人產品資訊的存取權，請為該產品資訊設定個人或群組的 IAM 政策。如果是商業產品資訊，[資料交換作業必須公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)。公開資料交換庫中的項目會顯示在[Google Cloud 所有使用者 (allAuthenticatedUsers)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 的「共用」頁面中。如要允許使用者要求存取商業清單，請授予 [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.viewer`)。

如要授予使用者查看或訂閱產品資訊的權限，請按照下列步驟操作：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有該項目的資料交換作業名稱。
3. 按一下要新增共用主題訂閱者的清單。
4. 按一下「person 設定權限」。
5. 如要新增主體，請按一下「person\_add 新增主體」。
6. 在「新增主體」欄位中，根據產品類型新增詳細資料：

   * 如果是私人產品，請輸入要授予存取權的身分電子郵件地址。
   * 如果是公開產品，請新增 `allAuthenticatedUsers`。
7. 在「Select a role」(選取角色) 選單中，選取「Analytics Hub」，然後根據資訊清單類型選取下列其中一個角色：

   * 如果是商業項目，請選取「Analytics Hub 檢視者」角色。這個角色可讓使用者[查看清單並要求存取權](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * 如果是私人或非商業用途公開清單，請選取「Analytics Hub Subscriber」(Analytics Hub 訂閱者) 角色。具備這個角色的使用者可以[訂閱您的產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)。
8. 按一下 [儲存]。

詳情請參閱「[Analytics Hub 訂閱者和檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role)」。

### 管理訂閱項目

如要允許使用者訂閱含有共用主題的清單，請在特定清單上授予「Analytics Hub 訂閱者」(`roles/analyticshub.subscriber`) 和「Analytics Hub 訂閱項目擁有者」(`roles/analyticshub.subscriptionOwner`) 角色：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下資料交換名稱，其中包含您要管理訂閱項目的清單。
3. 按一下要列出共用主題訂閱者的項目。
4. 按一下「person 設定權限」。
5. 如要新增主體，請按一下「person\_add 新增主體」。
6. 在「New principals」(新增主體) 欄位中，輸入要新增的訂閱者使用者名稱或電子郵件地址。
7. 在「**選取角色**」部分，依序選取「**Analytics Hub > Analytics Hub 訂閱者**」。
8. 按一下 add\_box「Add another role」(新增其他角色)。
9. 在**「選取角色」**部分，依序選取**「Analytics Hub」>「Analytics Hub 訂閱項目擁有者」**。
10. 按一下 [儲存]。

只要按一下「設定權限」，即可隨時刪除及更新訂閱者。

### 撤銷訂閱項目

如要從 BigQuery sharing 中移除共用主題資訊的訂閱項目，請選取下列其中一個選項：

### 控制台

1. 如要列出產品資訊的共用主題訂閱者，請按照[查看所有訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#view_all_subscriptions)中的Google Cloud 控制台操作說明操作。
2. 按一下「Subscriptions」(訂閱項目) 分頁標籤，即可查看資料交換作業的所有訂閱項目。
3. 找出要移除的訂閱項目並勾選旁邊的核取方塊，或選取所有訂閱項目。
4. 在「Revoke subscription?」(要撤銷訂閱項目嗎？) 對話方塊中，輸入 `revoke` 進行確認。
5. 按一下 [撤銷]。

### API

如要移除訂閱項目，請使用 [`projects.locations.subscriptions.revoke`](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/revoke?hl=zh-tw) 方法。

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/subscriptions/SUBSCRIPTION_ID:revoke
```

更改下列內容：

* `PROJECT_ID`：要移除的訂閱項目專案 ID。
* `LOCATION`：訂閱項目的位置。
* `SUBSCRIPTION_ID`：要移除的訂閱項目 ID。

從 BigQuery sharing 撤銷訂閱項目後，共用主題訂閱端就不會再收到共用主題的訊息資料。Pub/Sub 訂閱項目會與共用主題中斷連結。如果直接從 Pub/Sub 刪除訂閱項目，BigQuery sharing 訂閱項目仍會保留，需要手動清除。

## 訂閱者工作流程

BigQuery 共用訂閱者可以查看及訂閱清單。訂閱共用主題的清單，會在訂閱者的專案中建立一個連結的 Pub/Sub 訂閱項目。Pub/Sub 訂閱項目會顯示在共用主題發布者的專案中。

### 其他訂閱者權限

您必須在專案、交換或資訊清單層級，具備 [Analytics Hub 訂閱者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`) 角色，才能執行訂閱者工作。

### 訂閱共用主題清單

如要訂閱含有共用主題的產品資訊，請選取下列其中一個選項：

### 控制台

1. 如要查看可存取的產品資訊清單，請按照「[查看產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)」中的步驟操作。
2. 瀏覽清單，然後按一下要訂閱的項目。系統會顯示含有商店資訊詳細資料的對話方塊。
3. 按一下「訂閱」，開啟「建立訂閱項目」對話方塊。
4. 如果專案尚未啟用 Analytics Hub API，系統會顯示錯誤訊息，並提供啟用 API 的連結。按一下「Enable Analytics Hub API」。
5. 在「Create subscription」(建立訂閱項目) 對話方塊中，指定下列詳細資料：

   * **訂閱項目 ID**：指定要建立的訂閱項目名稱。
   * **傳送類型**：選取訊息資料的傳送方式。
   * **訊息保留時間**：設定訊息保留時間。
   * **到期時間範圍**：設定訂閱項目在閒置多久後到期 (如有)。
   * **確認期限**：設定確認期限。
   * **訂閱項目篩選器**：設定訊息的篩選器語法。
   * **僅傳送一次**：啟用僅傳送一次。
   * **訊息排序**：使用排序鍵啟用訊息排序功能。
   * **Dead lettering**：啟用 dead-letter 功能。
   * **重試政策**：設定重試政策。

   如要進一步瞭解 Pub/Sub 訂閱項目屬性，請參閱「[訂閱項目屬性](https://docs.cloud.google.com/pubsub/docs/subscription-properties?hl=zh-tw)」。
6. 如要儲存變更，請按一下「建立」。系統會在您的專案中建立連結的 Pub/Sub 訂閱項目。

### API

請使用 [`projects.locations.dataExchanges.listings.subscribe` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/subscribe?hl=zh-tw)。

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:subscribe
```

更改下列內容：

* `PROJECT_ID`：要訂閱的清單專案 ID。
* `LOCATION`：要訂閱的產品資訊位置。
* `DATAEXCHANGE_ID`：要訂閱的清單資料交換 ID。
* `LISTING_ID`：要訂閱的產品 ID。

在要求主體中，指定要建立[連結 Pub/Sub 訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_pubsub_subscriptions)的 Pub/Sub 訂閱項目。如果成功，回應主體會是空白。

如要進一步瞭解 Pub/Sub 訂閱項目，請參閱[訂閱項目總覽](https://docs.cloud.google.com/pubsub/docs/subscription-overview?hl=zh-tw)。

## 定價

Pub/Sub 主題發布者透過 BigQuery sharing 列出及共用主題，不需支付額外費用。共用主題發布者須支付寫入共用主題的總位元組數 (發布處理量) 費用，以及網路輸出費用 (如適用)。共用主題訂閱者須支付從連結訂閱項目讀取的總位元組數 (訂閱處理量) 費用，以及網路輸出費用 (如適用)。詳情請參閱 [Pub/Sub 定價](https://cloud.google.com/pubsub/pricing?hl=zh-tw#pubsub)。

## VPC Service Controls

如果共用主題來自設有 VPC Service Controls 範圍的專案，請設定適當的輸入和輸出規則，將存取權授予共用主題的發布者和訂閱者。

## 後續步驟

* 瞭解如何[管理產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)。
* 瞭解如何[訂閱產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。
* 瞭解如何[監控 Pub/Sub 資源](https://docs.cloud.google.com/pubsub/docs/monitoring?hl=zh-tw)。
* 瞭解如何[設定 BigQuery 共用的 VPC Service Controls 規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-21 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-21 (世界標準時間)。"],[],[]]