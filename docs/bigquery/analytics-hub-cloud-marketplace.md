Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 Google Cloud Marketplace 上將清單商業化

BigQuery sharing 發布者可以透過 BigQuery sharing (舊稱 Analytics Hub) 與 [Google Cloud Marketplace](https://docs.cloud.google.com/marketplace?hl=zh-tw) 的整合功能，在 Cloud Marketplace 上列出自己的資料產品，藉此創造收益。使用發布者/訂閱者模式，您就能大規模與顧客分享資料產品，不必管理每筆交易和訂閱。您可以設定資料產品的各個層面，例如提供的資料類型 (例如 BigQuery 資料集)、訂閱價格 (付費、免費或試用) 和訂閱時間長度。

身為 BigQuery sharing 訂閱者，您可以使用這項整合功能，探索及使用各種 Google 和第三方資料產品與商業資料集。

繼續操作前，請先熟悉 [BigQuery sharing 資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)。

## 事前準備

1. [授予身分與存取權管理 (IAM) 角色](#required-roles)，讓使用者擁有執行本文件各項工作所需的權限。
2. [啟用 Analytics Hub API](#enable-api)。

### 必要的角色

如要取得使用 Cloud Marketplace 整合式產品資訊所需的權限，請要求管理員授予下列 IAM 角色：

* 建立及管理 BigQuery sharing 項目：
  + [Analytics Hub 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.admin)  (`roles/analyticshub.admin`)
  + [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)
  + [Service Management 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/servicemanagement?hl=zh-tw#servicemanagement.admin)  (`roles/servicemanagement.admin`)
* 在 Cloud Marketplace 建立及管理資料產品資訊：
  [Commerce Producer 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/commerceproducer?hl=zh-tw#commerceproducer.admin)  (`roles/commerceproducer.admin`)
* 在 Cloud Marketplace 訂閱付費的 BigQuery sharing 資訊：
  + [帳單帳戶管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/billing?hl=zh-tw#billing.admin)  (`roles/billing.admin`)
  + [Analytics Hub 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.viewer)  (`roles/analyticshub.viewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

### 啟用 Analytics Hub API

如要啟用 Analytics Hub API，請選取下列其中一個選項：

### 控制台

前往 **Analytics Hub API** 頁面，為專案啟用 Analytics Hub API。 Google Cloud

[啟用 API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### gcloud

執行 [`gcloud services enable` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw)：

```
gcloud services enable analyticshub.googleapis.com
```

啟用 Analytics Hub API 後，您可以在Google Cloud 控制台中存取「Sharing (Analytics Hub)」[頁面](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)。

## 限制

整合 Cloud Marketplace 的產品資訊有下列限制：

* 適用所有 [BigQuery 共用限制](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#limitations)。
* BigQuery sharing 發布者和訂閱者必須位於[支援的 Cloud Marketplace 機構管轄範圍](https://cloud.google.com/terms/marketplace-agency-jurisdictions?hl=zh-tw)。
* Cloud Marketplace 整合式產品資訊會編入 [Data Catalog](https://docs.cloud.google.com/bigquery/docs/data-catalog?hl=zh-tw) (已淘汰) 和 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/catalog-overview?hl=zh-tw) 的索引，但您無法特別篩選其資源類型。
* 系統不會在供應商用量指標或[`INFORMATION_SCHEMA`檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)中，擷取 Cloud Marketplace 整合式產品的帳單用量指標。
* Cloud Marketplace 整合不支援資料無塵室和 Pub/Sub 主題。

## 架構與術語

下圖顯示 Cloud Marketplace 與 BigQuery sharing 之間的互動，適用於商業項目：

#### Cloud Marketplace 上的資料產品

如要建立 Cloud Marketplace 資料產品資訊，請選取 BigQuery sharing 項目、選擇定價模式，然後將產品提交至 Cloud Marketplace 進行審查。

#### 在 BigQuery sharing 中整合 Cloud Marketplace 項目

Cloud Marketplace 資料產品項目獲得核准並發布後，BigQuery sharing 項目就會成為整合 Cloud Marketplace 的項目，在共用項目和 Cloud Marketplace 之間建立整合連結，並讓項目符合購買資格。這類 BigQuery 共用項目支援共用資料集。

#### 連結的資源

訂閱整合 Cloud Marketplace 的項目時，系統會在 BigQuery sharing 訂閱端專案中建立連結的資源。連結資源的存取權由有效的 Cloud Marketplace 訂單管理。整合 Cloud Marketplace 的產品資訊支援連結資料集。

## 建立與 Cloud Marketplace 整合的商店資訊

如要建立 BigQuery sharing 項目並發布至 Cloud Marketplace，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 建立新的[分享資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#create-exchange)。或者，選擇現有的資料交換，保留現有訂閱項目。
3. 在資料交換庫中建立[房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)。或者，選擇現有商店資訊，保留現有訂閱項目。

   **注意：** 單一 BigQuery sharing 項目同時支援要求存取權和 Cloud Marketplace 整合流程。也就是說，您可以從現有的 (離線) 商業產品資訊建立整合 Cloud Marketplace 的產品資訊，現有訂閱項目不會受到任何影響。
4. 在資料交易的資料列中，依序按一下 more\_vert「更多動作」>「在 Marketplace 上架」。系統會將您重新導向至 Cloud Marketplace Producer Portal。
5. 按照 Cloud Marketplace Producer Portal 上的操作說明，將 BigQuery sharing 清單加入為[資料產品](https://docs.cloud.google.com/marketplace/docs/partners/data?hl=zh-tw)。
6. 返回「Sharing (Analytics Hub)」頁面。在資料交換的資料列中，「Marketplace」欄會顯示「未發布」，表示資料產品已建立並提交核准。點選「未發布」，系統會將你重新導向至 Cloud Marketplace Producer Portal，方便你查看狀態。
7. 通過核准後，「Marketplace」欄會顯示「已發布」字樣。
   按一下「已發布」一詞，系統會將你重新導向至 Cloud Marketplace 中的產品資訊。

如需其他規定，請參閱「[在 Google Cloud Marketplace 上提供軟體](https://docs.cloud.google.com/marketplace/docs/partners/offer-products?hl=zh-tw)」。

## 更新整合 Cloud Marketplace 的商店資訊

更新 Cloud Marketplace 整合式資訊的程序，與[更新資料交換庫標準產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#update_a_listing)的程序相同。您可能也需要在 Cloud Marketplace Producer Portal 中更新資料產品資訊，這可能需要再次審查和核准。

## 管理 Cloud Marketplace 整合式產品資訊的訂閱項目

Cloud Marketplace 訂單會管理已整合 Cloud Marketplace 的產品資訊商業訂閱項目。您仍可按照[標準產品資訊的相同程序](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#give_users_access_to_a_data_exchange)，手動新增及更新 BigQuery sharing 訂閱者，但不會發生相關的 Cloud Marketplace 交易。

您也可以手動撤銷訂閱，方法是[按照標準產品資訊的相同程序](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#revoke-subscription)，輸入 Marketplace 服務 ID 來接受警告通知。不過請注意，撤銷商業訂閱可能會影響客戶，並違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。此外，撤銷訂閱不會從 BigQuery sharing 或 Cloud Marketplace 移除項目。

## 停用與 Cloud Marketplace 整合的產品資訊

如要停用已整合商業版 Cloud Marketplace 的產品資訊，請在 [Google Cloud Marketplace Producer Portal](https://docs.cloud.google.com/marketplace/docs/partners?hl=zh-tw) 中管理相關聯產品的生命週期。

下架會從房源移除商業特徵，並轉換為標準的非商業用途房源。這個程序可確保在商業化結束前，履行對訂閱者的現有合約義務。

如要停用與 Cloud Marketplace 整合的產品資訊，請按照下列步驟操作：

1. 在 Producer Portal 中[要求停用產品資訊](https://docs.cloud.google.com/marketplace/docs/partners/deprecate-product?hl=zh-tw#product-deprecation)。

   **注意：** 標準產品淘汰必須至少提前 180 天通知現有客戶。
2. 等待淘汰日期到來。淘汰日期過後，Cloud Marketplace 資訊就會永久刪除。
3. 從 Producer Portal 刪除產品。

BigQuery sharing 項目完全下架後，就會成為標準的非商業用途項目。你可以選擇保留產品資訊供內部或免費分享，或[刪除產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#delete_a_listing)。

### 刪除與 Cloud Marketplace 整合的產品

**警告：** 強烈建議您[停用與 Cloud Marketplace 整合的產品資訊](#offboard-listing)，而不是刪除這類產品資訊。刪除整合 Cloud Marketplace 的產品資訊後，就無法復原。刪除與 Cloud Marketplace 整合的產品可能會影響客戶，並違反《[Cloud Marketplace 服務條款](https://cloud.google.com/terms/marketplace/launcher?hl=zh-tw)》。

如要從 BigQuery sharing 和 Cloud Marketplace 刪除與 Cloud Marketplace 整合的產品資訊，請按照下列步驟操作：

1. 按照[與資料交換相同的程序](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw#revoke-subscription)，撤銷 Cloud Marketplace 整合式產品的所有商業訂閱項目。如果 Cloud Marketplace 整合式產品資訊有有效的商業訂閱項目，就無法刪除。
2. 按照標準程序[刪除資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#delete_a_data_exchange)。
3. 系統顯示警告通知時，請輸入 Marketplace 服務 ID 以接受，然後按一下「確認」。

## 訂閱整合 Cloud Marketplace 的產品資訊

如要在 Cloud Marketplace 上訂閱 BigQuery sharing 項目，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「搜尋房源」search。
3. 搜尋要訂閱的商家資訊。
4. 按一下房源。
5. 如果貴機構已購買房源資訊，也就是顯示「訂閱」按鈕和購買日期，請按照下列步驟操作：

   1. 按一下「訂閱」。
   2. 指定專案和連結的資料集名稱。
   3. 按一下 [儲存]。

   如果沒有訂閱房源的權限，請按一下「要求存取權」並提交要求表單。
6. 如果貴機構尚未購買該產品資訊 (顯示「透過 Marketplace 購買」按鈕)，請按照下列步驟操作：

   1. 按一下「透過 Marketplace 購買」。
   2. 按一下「訂閱」。
   3. 在「訂單摘要」頁面中，指定訂閱方案、購買詳細資料，並接受條款 (如同意)。
   4. 按一下「訂閱」，然後按一下「前往產品頁面」。
   5. 請稍候片刻。啟用訂單後，按一下「前往 BigQuery sharing (Analytics Hub) 管理」。系統會將您重新導向回「Sharing (Analytics Hub)」頁面。
   6. 在 BigQuery sharing 資源的資訊頁面中，按一下「訂閱」。
   7. 指定專案和連結的資料集名稱。
   8. 按一下 [儲存]。

   如要取得部分房源的報價，可能需要提交表單，與銷售團隊聯絡。

只要專案使用相同的帳單帳戶，就能訂閱該項目。

## 定價

適用標準的 [BigQuery 共享定價](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#pricing)。此外，整合 Cloud Marketplace 的產品資訊也須遵守[Cloud Marketplace 收益分潤規定](https://docs.cloud.google.com/marketplace/docs/partners/get-started?hl=zh-tw)。如要進一步瞭解 BigQuery sharing 訂閱者如何支付發布者費用，以使用資料產品，請參閱「[管理 Cloud Marketplace 產品的帳單](https://docs.cloud.google.com/marketplace/docs/manage-billing?hl=zh-tw)」。

## 後續步驟

* 進一步瞭解 [Cloud Marketplace](https://docs.cloud.google.com/marketplace/docs?hl=zh-tw)。
* 如果您是 VPC Service Controls 使用者，請參閱「[VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#vpc-service)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]