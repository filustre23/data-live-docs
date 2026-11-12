Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 Google Cloud Marketplace 銷售產品

BigQuery sharing (舊稱 Analytics Hub) 可讓您透過 [Google Cloud Marketplace](https://docs.cloud.google.com/marketplace?hl=zh-tw) 提供及購買資料產品。發布者可以透過 Cloud Marketplace 大規模共用 BigQuery 資料集，並設定付費、免費或試用會員方案和效期，不必管理個別交易。

訂閱者可以透過 Cloud Marketplace 探索及使用 Google 和第三方商業資料集。繼續操作前，請先熟悉 [BigQuery 共用資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)。

## 事前準備

1. [授予 Identity and Access Management (IAM) 角色](#required-roles)，讓使用者具備執行本文件各項工作所需的權限。
2. [啟用 Analytics Hub API](#enable-api)。

### 必要的角色

如要取得使用 Cloud Marketplace 整合式產品資訊所需的權限，請要求管理員授予您下列 IAM 角色：

* 建立及管理 BigQuery sharing 項目：
  + [Analytics Hub 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.admin) (`roles/analyticshub.admin`)
  + [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner) (`roles/bigquery.dataOwner`)
  + [服務管理管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/servicemanagement?hl=zh-tw#servicemanagement.admin) (`roles/servicemanagement.admin`)
* 在 Cloud Marketplace 建立及管理資料產品資訊：[Commerce 供應商管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/commerceproducer?hl=zh-tw#commerceproducer.admin) (`roles/commerceproducer.admin`)
* 在 Cloud Marketplace 訂閱付費 BigQuery 共用項目：
  + [帳單帳戶管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/billing?hl=zh-tw#billing.admin) (`roles/billing.admin`)
  + [Analytics Hub 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

### 啟用 Analytics Hub API

如要啟用 Analytics Hub API，請選取下列其中一個選項：

### 控制台

前往「**Analytics Hub API**」頁面，為 Google Cloud 專案啟用 Analytics Hub API。

[啟用 API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### gcloud

使用 [`gcloud services enable` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw)啟用 Analytics Hub API：

```
gcloud services enable analyticshub.googleapis.com
```

啟用 Analytics Hub API 後，您可以在Google Cloud 控制台查看[「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)。

## 限制

與 Cloud Marketplace 整合的產品資訊有下列限制：

* 所有 [BigQuery 共用限制](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#limitations)皆適用。
* BigQuery sharing 發布者和訂閱者必須位於支援的 [Cloud Marketplace 代理商管轄區](https://cloud.google.com/terms/marketplace-agency-jurisdictions?hl=zh-tw)。
* 與 Cloud Marketplace 整合的產品資訊會編入 [Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/metadata-overview?hl=zh-tw) 索引，但您無法專門篩選這類資源類型。
* Cloud Marketplace 整合式產品資訊的計費使用指標，不會記錄在供應商使用指標或 [`INFORMATION_SCHEMA` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)中。
* Cloud Marketplace 整合不支援資料無塵室和 Pub/Sub 主題。

## 架構和術語

下圖顯示 Cloud Marketplace 與 BigQuery sharing 之間的互動，用於商業項目：

### Cloud Marketplace 中的資料產品

如要建立 Cloud Marketplace 資料產品項目，請選取 BigQuery 共用項目、選擇定價模式，然後將產品提交至 Cloud Marketplace 審查。

### BigQuery 共用平台上的 Cloud Marketplace 整合式項目

Cloud Marketplace 核准並發布資料產品項目後，您的 BigQuery sharing 項目就會變成 Cloud Marketplace 整合項目。核准後，系統會在 BigQuery sharing 和 Cloud Marketplace 之間建立整合連結，並將產品資訊設為可供購買。這類 BigQuery 共用項目支援共用資料集。

### 連結的資源

訂閱與 Cloud Marketplace 整合的清單時，BigQuery sharing 功能會在訂閱者專案中建立連結資源。有效的 Cloud Marketplace 訂單會管理連結資源的存取權。與 Cloud Marketplace 整合的產品資訊支援連結資料集。

## 建立與 Cloud Marketplace 整合的產品資訊

如要建立 BigQuery sharing 刊登資訊，並在 Cloud Marketplace 發布，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 建立 [BigQuery 共用資料交換作業](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#create-exchange)。或者，如要保留現有訂閱項目，請選取現有的資料交換。
3. [在資料交換中建立清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)。或者，如要保留現有訂閱項目，請選取現有商店資訊。

   **注意：**單一 BigQuery sharing 項目可同時支援存取要求和 Cloud Marketplace 整合流程。由於這兩種流程都支援，您可以從現有的離線商業產品資訊建立 Cloud Marketplace 整合產品資訊，而不會中斷現有訂閱。
4. 在產品資訊列中，依序按一下
   more\_vert
   **「More actions」(更多動作)>「List on Marketplace」(在 Marketplace 上架)**。
   系統會將您重新導向至 Cloud Marketplace 供應商入口網站。
5. 如要將 BigQuery sharing 刊登項目設為[資料產品](https://docs.cloud.google.com/marketplace/docs/partners/data?hl=zh-tw)，請按照 Cloud Marketplace Producer Portal 中的操作說明操作。
6. 返回「Sharing (Analytics Hub)」頁面。在產品資訊列中，「Marketplace」欄會顯示「Not Published」，表示您已建立並提交資料產品以供核准。如要在 Cloud Marketplace Producer Portal 中查看核准狀態，請按一下「Not Published」(未發布)。
7. 資料產品通過核准後，「Marketplace」欄會顯示「已發布」。如要在 Cloud Marketplace 查看產品資訊，請按一下「Published」(已發布)。

如需其他規定，請參閱「[在 Cloud Marketplace 提供軟體](https://docs.cloud.google.com/marketplace/docs/partners/offer-products?hl=zh-tw)」。

## 更新與 Cloud Marketplace 整合的產品資訊

更新與 Cloud Marketplace 整合的產品資訊時，程序與[更新資料交換中的標準產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#update_a_listing)相同。您可能也需要在 Cloud Marketplace Producer Portal 更新資料產品資訊，這可能需要再次審查和核准。

## 管理與 Cloud Marketplace 整合的產品訂閱項目

Cloud Marketplace 訂單會管理與 Cloud Marketplace 整合的商業訂閱項目。您仍可按照標準程序，[授予使用者資料交換存取權](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#give_users_access_to_a_data_exchange)，手動新增及更新 BigQuery sharing 訂閱者。但不會進行相關聯的 Cloud Marketplace 交易。

您也可以手動撤銷訂閱項目，方法是按照標準程序[撤銷訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#revoke-subscription)，並輸入 Cloud Marketplace 服務 ID 來接受警告通知。不過，撤銷商業訂閱項目可能會影響客戶，並違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。此外，撤銷訂閱項目並不會從 BigQuery sharing 或 Cloud Marketplace 移除產品資訊。

## 停用與 Cloud Marketplace 整合的產品

如要下架與 Cloud Marketplace 整合的商業產品資訊，您必須在 [Cloud Marketplace Producer Portal](https://docs.cloud.google.com/marketplace/docs/partners?hl=zh-tw)中管理相關產品的生命週期。

下架作業會移除產品資訊的商業特性，並將其轉換為標準的非商業用途產品資訊。這項程序可確保您在商業化結束前，履行對訂閱者的現有合約義務。

如要將與 Cloud Marketplace 整合的產品資訊下架，請按照下列步驟操作：

1. 在 Producer Portal 中，[要求淘汰產品資訊](https://docs.cloud.google.com/marketplace/docs/partners/deprecate-product?hl=zh-tw#product-deprecation)。

   **注意：**標準產品淘汰作業必須至少提前 180 天通知現有客戶。
2. 等待淘汰日期過去。淘汰日期過後，Cloud Marketplace 產品資訊就會永久刪除。
3. 從 Producer Portal 刪除產品。

BigQuery sharing 項目完全停用後，會做為標準非商業用途項目運作。您可以保留產品資訊，用於內部或免費共用，也可以[刪除產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#delete_a_listing)。

### 刪除與 Cloud Marketplace 整合的產品資訊

**警告：**強烈建議您[停用與 Cloud Marketplace 整合的產品資訊](#offboard-listing)，而非刪除。刪除與 Cloud Marketplace 整合的產品資訊後，即無法復原。刪除與 Cloud Marketplace 整合的產品，可能會影響客戶，並違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。

如要從 BigQuery sharing 和 Cloud Marketplace 刪除與 Cloud Marketplace 整合的產品資訊，請按照下列步驟操作：

1. 按照[撤銷訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#revoke-subscription)的標準程序，撤銷與 Cloud Marketplace 整合的產品資訊的所有商業訂閱項目。如果與 Cloud Marketplace 整合的產品資訊有有效的商業訂閱項目，則無法刪除。
2. 按照標準程序[刪除商家資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#delete_a_listing)。
3. 看到警告通知時，請輸入 Cloud Marketplace 服務 ID 表示接受，然後按一下「Confirm」(確認)。

## 訂閱與 Cloud Marketplace 整合的產品

如要在 Cloud Marketplace 訂閱 BigQuery sharing 項目，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「search 搜尋產品資訊」。
3. 搜尋要訂閱的產品。如要探索 Cloud Marketplace 上的商業
   產品，請套用
   **「Listings」(產品)>「Marketplace」**篩選器。
4. 按一下該產品資訊。
5. 如果貴組織已購買產品，也就是說，您可以看到「Subscribe」(訂閱) 按鈕和購買日期，請執行下列操作：

   1. 點選「訂閱」。
   2. 指定專案和連結的資料集名稱。
   3. 按一下「儲存」。

   如果您沒有訂閱清單的權限，請按一下「Request access」(要求存取權)，然後提交要求表單。
6. 如果貴組織尚未購買產品，也就是畫面上顯示「Purchase via Marketplace」(透過 Marketplace 購買) 按鈕，請按照下列步驟操作：

   1. 按一下「透過 Marketplace 購買」。
   2. 點選「訂閱」。
   3. 在「Order summary」(訂單摘要) 頁面中，指定會員方案和購買詳細資料，並接受條款 (如果您同意)。
   4. 依序點選「訂閱」和「前往產品頁面」。
   5. 請稍候片刻。訂單啟用後，請按一下「Manage on BigQuery sharing (Analytics Hub)」(前往 BigQuery sharing (Analytics Hub) 管理)。系統會將您重新導向回「Sharing (Analytics Hub)」頁面。
   6. 在 BigQuery sharing 資訊頁面，按一下「Subscribe」(訂閱)。
   7. 指定專案和連結的資料集名稱。
   8. 按一下「儲存」。

   如要取得某些產品的報價，您可能需要提交表單，與銷售團隊聯絡。

凡是使用相同帳單帳戶的專案，也都能訂閱該清單。

## 定價

適用標準 [BigQuery 共用定價](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#pricing)。此外，Cloud Marketplace 整合式產品資訊也須遵守 [Cloud Marketplace 收益分潤規定](https://docs.cloud.google.com/marketplace/docs/partners/get-started?hl=zh-tw)。如要進一步瞭解發布者如何向 BigQuery sharing 訂閱者收取資料產品使用費，請參閱「[管理 Cloud Marketplace 產品的帳單](https://docs.cloud.google.com/marketplace/docs/manage-billing?hl=zh-tw)」。

## 後續步驟

* 進一步瞭解 [Cloud Marketplace](https://docs.cloud.google.com/marketplace/docs?hl=zh-tw)。
* 如果您是 VPC Service Controls 使用者，請參閱「[VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#vpc-service-controls)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]