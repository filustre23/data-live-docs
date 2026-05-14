Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過 Pub/Sub 串流分享

您可以透過 BigQuery sharing (舊稱 Analytics Hub) 共用 Pub/Sub 主題，在多個內部和外部機構界線之間，管理及發布串流資料庫。即時串流資料會透過 BigQuery 共用交換庫和產品資訊共用，方便您以邏輯方式分類及分組大量 Pub/Sub 主題，並大規模佈建存取權。

分享串流資料可執行下列操作：

* **金融服務**：
  + 即時分享快速變動的工具價格、報價和訂單。
  + 偵測洗錢和付款詐欺行為。
  + 支援交易風險計算。
* **零售和民生消費用品業 (CPG)**：
  + 即時管理店內商品目錄。
  + 提供個人化行銷和客戶服務。
  + 動態調整價格。
  + 監控社群媒體管道。
  + 改善實體商店的版面配置。
* **醫療保健**：
  + 運用預測演算法監控病患，並即時分析風險。
  + 使用穿戴式醫療器材監測健康指標。
  + 自動取得、建構、儲存及處理病患、專業醫護人員和機構管理人員的資料。
* **電信**：
  + 監控網路健康狀態並預測故障。
  + 找出使用者行為模式，以便更準確地定位裝置和天線。

## 必要的角色

共用 Pub/Sub 主題的角色與共用 BigQuery 資料集類似：

* **管理員**：管理交換庫和產品資訊的權限、曝光度和成員資格。這個角色等同於「Analytics Hub 管理員」(`roles/analyticshub.admin`) IAM 角色。
* **共用主題發布者**：建立、管理及授予共用 Pub/Sub 主題清單的存取權。這個角色類似於 [Analytics Hub 發布者或 Analytics Hub 清單管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) IAM 角色。發布者是使用者，而不是建立訊息並傳送至主題的[發布者應用程式](https://docs.cloud.google.com/pubsub/docs/publisher?hl=zh-tw)。
* **共用主題訂閱端**：訂閱共用主題清單。共用主題訂閱者可以設定主題訊息的傳送方式。這個角色類似於 [Analytics Hub 訂閱者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role)或 [Analytics Hub 訂閱項目擁有者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscription-owner-role) IAM 角色。視訊息資料的傳送方式而定，可能需要額外權限，例如[Pub/Sub 服務帳戶權限](https://docs.cloud.google.com/pubsub/docs/bigquery?hl=zh-tw#service_account_permissions)，才能將訊息寫入 BigQuery。

## 架構

下圖說明 Pub/Sub 資源的發布端和訂閱端如何與 BigQuery 共用功能互動：



共用主題
:   共用主題是透過 BigQuery sharing 功能共用 Pub/Sub 主題的單位。身為共用主題發布者，您可以建立或使用現有的 Pub/Sub 主題，將訊息資料發布給訂閱者。BigQuery sharing 不會複製來源 Pub/Sub 主題。

清單
:   發布者將共用主題新增至交換庫時，系統會建立清單。並參照共用主題。

廣告交易平台
:   交換庫是指參照共用主題的產品資訊邏輯分組。

已連結的 Pub/Sub 訂閱項目
:   訂閱共用主題的產品資訊時，系統會在共用主題訂閱端專案中建立連結的 Pub/Sub 訂閱項目。共用主題發布者的專案也會將 Pub/Sub 訂閱項目表示為 Pub/Sub 訂閱項目和共用清單訂閱項目。

## 限制

透過 Pub/Sub 分享串流有下列限制：

* 共用主題最多可支援 10,000 個 Pub/Sub 訂閱項目。這項限制包括連結的 Pub/Sub 訂閱項目，以及在共用功能外建立的 Pub/Sub 訂閱項目 (例如直接從 Pub/Sub 建立的項目)。
* Data Catalog (已淘汰) 和 Knowledge Catalog 會為共用主題建立索引，但您無法依資源類型進行篩選。
* 系統會擷取共用 Pub/Sub 主題和訂閱項目的用量指標，並顯示在指標資訊主頁中，但 `INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 不會顯示這些指標。

  如要監控指標，請參閱「[在 Cloud Monitoring 中監控 Pub/Sub](https://docs.cloud.google.com/pubsub/docs/monitoring?hl=zh-tw)」。

  這些指標包括：

  + 發布訊息數
  + 發布要求
  + 發布處理量 (以位元組為單位)
  + 前 5 大訂閱項目
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

前往 API 程式庫，為您的 Google Cloud 專案啟用 Pub/Sub API。

[啟用 Pub/Sub API](https://console.cloud.google.com/apis/library/pubsub.googleapis.com?hl=zh-tw)

## 共用主題發布商工作流程

身為共用主題發布者，你可以執行下列操作：

* 建立產品資訊，將共用主題新增至交換庫。
* 更新產品資訊。
* 刪除房源資訊。
* 分享商家資訊。
* 管理房源的訂閱項目。
* 從房源資訊中移除訂閱者。

### 其他發布商權限

如要執行共用主題發布者工作，您必須在交換庫或產品資訊中具備[Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) (`roles/analyticshub.publisher`)。如要查看您有權存取的機構中所有專案的[資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)，您必須具備 `resourcemanager.organizations.get` 權限。

此外，您還需要列出 Pub/Sub 主題的 `pubsub.topics.setIamPolicy` 權限。如要共用附加結構定義的主題，您必須授予 BigQuery sharing 訂閱端主題附加結構定義的 `pubsub.schemas.get` 權限。這項權限可讓 BigQuery sharing 訂閱端正確剖析 Pub/Sub 訂閱項目的訊息。

### 建立產品資訊 (新增共用主題)

如要將共用主題新增至房源資訊，請選取下列其中一個選項：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)

   頁面會列出您可存取的所有資料交換。
2. 按一下要建立房源資訊的資料交換庫名稱。
3. 按一下 add\_box「建立商店資訊」。
4. 在「建立項目」頁面中，從「資源類型」清單選取「Pub/Sub 主題」。
5. 從「共用主題」清單中選取現有的 Pub/Sub 主題，或按一下「建立主題」。
6. 在「清單詳細資料」頁面的「顯示名稱」欄位中，輸入產品資訊名稱。
7. 輸入下列選填詳細資料：

   * **類別**：選取最多兩個最能代表商家檔案的類別。共用主題訂閱者可以根據這些類別[篩選房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * **資料相依性**：共用主題發布者用來發布資料的區域。共用主題的訂閱者可透過這項資訊，從相同區域讀取資料，盡量減少或避免 Pub/Sub 網路輸出費用。如要進一步瞭解輸出費用，請參閱「[資料移轉費用](https://cloud.google.com/pubsub/pricing?hl=zh-tw#egress_costs)」。
   * **圖示**：產品資訊的圖示。支援 PNG 和 JPEG 檔案格式。圖示大小不得超過 512 KiB，尺寸不得超過 512 x 512 像素。
   * **說明**：簡要說明房源。共用主題訂閱者可以根據說明[搜尋房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * **公開探索**：在 BigQuery sharing 目錄中，為您的項目啟用公開探索功能。您也必須設定商家資訊的權限。按一下交易所的「動作」，然後點選「設定權限」。授予 `allUsers` 或 `allAuthenticatedusers` [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.viewer`)。按一下「允許公開存取」。
   * **說明文件 > Markdown**：其他資訊，例如相關說明文件的連結，以及有助於共用主題訂閱者使用主題的其他詳細資料。
8. 在「商家資訊聯絡資料」頁面中，輸入下列選填詳細資料：

   * **主要聯絡人**：輸入商家資訊主要聯絡人的電子郵件地址或網址。
   * **要求存取聯絡人**：輸入電子郵件地址或接收表單網址，分享主題訂閱者可透過這些資訊與您聯絡。
   * **供應商**：展開「供應商」部分，並在下列欄位中指定詳細資料：

     + **供應商名稱**：主題供應商的名稱。
     + **供應商主要聯絡人**：主題供應商主要聯絡人的電子郵件地址或網址。

     共用主題訂閱者可以根據資料供應商篩選房源資訊。
   * **發布商**：展開「發布商」部分，並在下列欄位中指定詳細資料：

     + **發布商名稱**：建立商家資訊的共用主題發布商名稱。
     + **發布者主要聯絡人**：共用主題發布者主要聯絡人的電子郵件地址或網址。
9. 查看「商家資訊預覽」頁面。
10. 按一下「發布」。

### API

請使用 [`projects.locations.dataExchanges.listings.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/create?hl=zh-tw)。

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings?listingId=LISTING_ID
```

更改下列內容：

* `PROJECT_ID`：包含資料交換庫的專案 ID，您要在該交換庫中建立商家資訊。
* `LOCATION`：資料交換庫的位置。如要進一步瞭解支援分享功能的地區，請參閱[支援的地區](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)。
* `DATAEXCHANGE_ID`：資料交換 ID。
* `LISTING_ID`：房源 ID。

在要求主體中，提供[房源詳細資料](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#resource:-listing)。如果要求成功，回應主體會包含房源詳細資料。

如要進一步瞭解如何使用 API 對房源執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

### 更新產品資訊

如要更新商家資訊，請選取下列其中一個選項：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下包含房源資訊的資料交換名稱。
3. 按一下要更新的商家資訊。
4. 按一下「編輯商家資訊」mode\_edit。
5. 修改欄位值。除了房源的共用主題，你還可以修改所有值。
6. 按一下「發布」即可儲存變更。

### API

請使用 [`projects.locations.dataExchanges.listings.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/patch?hl=zh-tw)。

```
PATCH https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID?updateMask=UPDATEMASK
```

更改下列內容：

* `PROJECT_ID`：包含資料交換庫的專案 ID，您要在該交換庫中建立商家資訊。
* `LOCATION`：資料交換庫的位置。如要進一步瞭解支援分享功能的地區，請參閱「[支援的地區](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
* `DATAEXCHANGE_ID`：資料交換 ID。
* `LISTING_ID`：房源 ID。
* `UPDATEMASK`：要更新的欄位清單。如要更新多個值，請使用以半形逗號分隔的清單。

在要求主體中指定更新的值。

如要進一步瞭解如何使用 API 對房源執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

### 刪除產品資訊

如果共用的 Pub/Sub 主題有有效訂閱項目，就無法刪除房源資訊。嘗試刪除共用主題資訊前，請[撤銷所有有效訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-stream-sharing?hl=zh-tw#revoke_a_subscription)。刪除商家資訊後無法復原。

如要刪除房源，請選擇下列任一做法：

### 控制台

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下包含房源資訊的資料交換名稱。
3. 按一下要刪除的商家資訊。
4. 按一下「刪除」圖示 delete。
5. 在「要刪除房源嗎？」對話方塊中輸入 `delete`，確認刪除房源。
6. 點選「刪除」。

### API

請使用 [`projects.locations.dataExchanges.listings.delete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/delete?hl=zh-tw)。

```
DELETE https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID
```

更改下列內容：

* `PROJECT_ID`：包含資料交換庫的專案 ID，您要在該交換庫中建立商家資訊。
* `LOCATION`：資料交換庫的位置。如要進一步瞭解支援分享功能的地區，請參閱「[支援的地區](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
* `DATAEXCHANGE_ID`：資料交換 ID。
* `LISTING_ID`：房源 ID。

如要進一步瞭解如何使用 API 對房源執行工作，請參閱 [`projects.locations.dataExchanges.listings` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings?hl=zh-tw#methods)。

### 分享房源資訊

如要授權使用者存取私人應用程式，請為該應用程式的個人或群組設定 IAM 政策。如果是商業用途的商家資訊，[資料交換必須公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)。公開資料交換庫中的清單會顯示在「分享」頁面，供[所有使用者 (allAuthenticatedUsers)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 存取。Google Cloud 如要允許使用者要求存取商業產品資訊，請授予他們 [Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.viewer`)。

如要授予使用者檢視或訂閱清單的權限，請按照下列步驟操作：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下包含房源資訊的資料交換名稱。
3. 按一下要新增共用主題訂閱者的房源資訊。
4. 按一下「設定權限」person。
5. 如要新增主體，請按一下 person\_add「新增主體」。
6. 在「New principals」(新增主體) 欄位中，根據房源類型新增詳細資料：

   * 如果是私人應用程式，請輸入要授予存取權的身分電子郵件地址。
   * 如果是公開產品資訊，請新增 `allAuthenticatedUsers`。
7. 從「Select a role」選單選取「Analytics Hub」，然後根據房源類型選取下列其中一個角色：

   * 如果是商業產品資訊，請選取「Analytics Hub 檢視者」角色。這個角色可讓使用者[查看商家資訊並要求存取權](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)。
   * 如果是私人或非商業用途的公開清單，請選取「Analytics Hub 訂閱者」角色。使用者可透過這個角色[訂閱你的商家資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)。
8. 按一下 [儲存]。

詳情請參閱「[Analytics Hub 訂閱者和檢視者角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role)」。

### 管理訂閱項目

如要讓使用者訂閱含有共用主題的項目，請在特定項目中授予「Analytics Hub 訂閱者」(`roles/analyticshub.subscriber`) 和「Analytics Hub 訂閱項目擁有者」(`roles/analyticshub.subscriptionOwner`) 角色：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下包含要管理訂閱項目之商家資訊的資料交易平台名稱。
3. 按一下要列出共用主題訂閱者的房源。
4. 按一下「設定權限」person。
5. 如要新增主體，請按一下 person\_add「新增主體」。
6. 在「New principals」(新增主體) 欄位中，輸入要新增訂閱者的使用者名稱或電子郵件地址。
7. 在「選取角色」部分，依序選取「Analytics Hub」>「Analytics Hub 訂閱者」。
8. 按一下 add\_box「Add another role」(新增其他角色)。
9. 在「選取角色」部分，依序選取「Analytics Hub」>「Analytics Hub 訂閱項目擁有者」。
10. 按一下 [儲存]。

按一下「設定權限」，即可隨時刪除及更新訂閱者。

### 撤銷訂閱

如要從 BigQuery sharing 移除共用主題清單的訂閱項目，請選取下列其中一個選項：

### 控制台

1. 如要列出房源的共用主題訂閱端，請按照「[查看所有訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#view_all_subscriptions)」中的Google Cloud 控制台操作說明操作。
2. 按一下「Subscriptions」(訂閱項目) 分頁標籤，查看資料交易所的所有訂閱項目。
3. 找出要移除的訂閱項目，然後勾選旁邊的核取方塊，或選取所有訂閱項目。
4. 在「要撤銷訂閱嗎？」對話方塊中輸入 `revoke` 以確認。
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

從 BigQuery sharing 撤銷訂閱項目後，共用主題的訂閱端就不會再收到共用主題的訊息資料。Pub/Sub 訂閱項目會從共用主題卸離。如果直接從 Pub/Sub 刪除訂閱項目，BigQuery 共用訂閱項目會保留，需要清理。

## 訂閱者工作流程

BigQuery sharing 訂閱者可以查看及訂閱清單。訂閱共用主題的清單時，系統會在訂閱者的專案中建立一個連結的 Pub/Sub 訂閱項目。共用主題發布者的專案會顯示 Pub/Sub 訂閱項目。

### 其他訂閱者權限

您必須在專案、交換庫或刊登層級獲派[Analytics Hub 訂閱者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.subscriber`) 角色，才能執行訂閱者工作。

### 訂閱共用主題清單

如要訂閱含有共用主題的房源，請選取下列其中一個選項：

### 控制台

1. 如要查看可存取的房源清單，請按照「[查看房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)」一文中的步驟操作。
2. 瀏覽房源，然後按一下要訂閱的房源。系統會顯示含有房源詳細資料的對話方塊。
3. 按一下「訂閱」，開啟「建立訂閱項目」對話方塊。
4. 如果專案尚未啟用 Analytics Hub API，系統會顯示錯誤訊息，並提供啟用 API 的連結。按一下「啟用 Analytics Hub API」。
5. 在「建立訂閱項目」對話方塊中，指定下列詳細資料：

   * **訂閱 ID**：指定要建立的訂閱名稱。
   * **傳送類型**：選取訊息資料的傳送方式。
   * **訊息保留時間**：設定訊息保留時間。
   * **到期時間範圍**：設定訂閱項目在閒置一段時間後到期的時間，如果會到期。
   * **確認期限**：設定確認期限。
   * **訂閱項目篩選器**：設定郵件的篩選器語法。
   * **僅傳送一次**：啟用「僅傳送一次」選項。
   * **訊息排序**：使用排序鍵啟用訊息排序功能。
   * **無效信件**：啟用無效信件功能。
   * **重試政策**：設定重試政策。

   如要進一步瞭解 Pub/Sub 訂閱項目屬性，請參閱[訂閱項目屬性](https://docs.cloud.google.com/pubsub/docs/subscription-properties?hl=zh-tw)。
6. 如要儲存變更，請按一下「建立」。系統會在專案中建立連結的 Pub/Sub 訂閱項目。

### API

請使用 [`projects.locations.dataExchanges.listings.subscribe` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/subscribe?hl=zh-tw)。

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:subscribe
```

更改下列內容：

* `PROJECT_ID`：您要訂閱的房源專案 ID。
* `LOCATION`：要訂閱的商家資訊位置。
* `DATAEXCHANGE_ID`：要訂閱的房源資料廣告交易平台 ID。
* `LISTING_ID`：要訂閱的房源 ID。

在要求主體中，指定要建立[連結 Pub/Sub 訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_pubsub_subscriptions)的 Pub/Sub 訂閱項目。如果成功，回應主體會留白。

如要進一步瞭解 Pub/Sub 訂閱項目，請參閱[訂閱項目總覽](https://docs.cloud.google.com/pubsub/docs/subscription-overview?hl=zh-tw)。

## 定價

Pub/Sub 主題發布者透過 BigQuery sharing 列出及共用主題時，不會產生額外費用。共用主題發布端須支付寫入共用主題的總位元組數 (發布處理量) 費用，以及網路輸出費用 (如適用)。系統會向共用主題的訂閱端收取從連結訂閱項目讀取的總位元組數 (訂閱處理量)，以及網路輸出費用 (如適用)。詳情請參閱 [Pub/Sub 定價](https://cloud.google.com/pubsub/pricing?hl=zh-tw#pubsub)。

## VPC Service Controls

如要存取設有 VPC Service Controls 範圍的專案中分享的主題，請設定適當的輸入和輸出規則，授予共用主題發布端和訂閱端存取權。

## 後續步驟

* 瞭解如何[管理房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)。
* 瞭解如何[訂閱房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。
* 瞭解如何[監控 Pub/Sub 資源](https://docs.cloud.google.com/pubsub/docs/monitoring?hl=zh-tw)。
* 瞭解如何[為 BigQuery sharing 設定 VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]