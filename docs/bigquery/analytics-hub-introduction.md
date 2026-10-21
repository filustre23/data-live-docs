Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 共用功能簡介

BigQuery sharing (舊稱 Analytics Hub) 是資料交換平台，可讓您安全地共用、探索及存取資料，不受機構藩籬的限制，也不必複製資料。

您可以使用 BigQuery sharing 功能，探索精選的第三方和 Google 資料集，並與內部資料結合，強化數據分析和機器學習計畫。

BigQuery sharing Identity and Access Management (IAM) 角色可讓您執行下列 BigQuery sharing 工作：

* [Analytics Hub 發布者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-publisher-role) (`roles/analyticshub.publisher`)：與合作夥伴網路或貴組織內部即時共用資料。[清單](#listings)可讓您共用資料，而不必複製資料，您也可以在 [Google Cloud Marketplace](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw) 或透過自己的管道，利用清單營利。您可以建立可供分析的資料來源目錄，並設定精細的權限，將資料提供給授權的訂閱者。您也可以管理訂閱項目，並查看清單的使用指標。
* [Analytics Hub 訂閱者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role)
  (`roles/analyticshub.subscriber`)：探索資料、將共用資料與現有資料合併，以及使用 [BigQuery 的內建功能](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw#explore-bigquery)。
  訂閱產品時，系統會在 Google Cloud 專案中建立[連結資料集](#linked_datasets)或連結的 Pub/Sub 訂閱項目。如要管理訂閱項目，請使用[訂閱資源](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions?hl=zh-tw)，其中會儲存訂閱者的資訊，並代表發布者與訂閱者之間的連結。
* [Analytics Hub 檢視者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-subscriber-role) (`roles/analyticshub.viewer`)：瀏覽您有權在 BigQuery sharing 中查看的資料交換庫和資訊。如果您沒有清單的訂閱權限，可以向發布者要求存取共用資料的權限。您可以在 BigQuery sharing 和 Cloud Marketplace 中，探索與 Cloud Marketplace 整合的商業產品資訊。
* [Analytics Hub 管理員](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-admin-role) (`roles/analyticshub.admin`)：建立[資料交換](#data_exchanges)，讓發布者共用資料，並授予資料發布者和訂閱者存取這些資料交換的權限。

詳情請參閱「[設定 Analytics Hub 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw)」。

## 架構

BigQuery sharing 功能是以Google Cloud 資料資源的發布和訂閱模型為基礎，可讓您直接共用資料，無須複製。BigQuery sharing 支援下列資源：

* BigQuery 資料集
* Pub/Sub 主題

### 發布商工作流程

在發布者工作流程中，您會在專案中建立共用資源，將資源整理成資料交換中的清單，並授予訂閱者存取權：

以下各節說明發布者工作流程中的元件。

#### 共用的資料集

共用資料集是 BigQuery 資料集，做為 BigQuery sharing 功能中的資料共用單位。BigQuery 架構將運算和儲存作業分開，因此資料發布者可以與多個訂閱者共用資料集，而不必複製資料。發布者可在專案中建立或使用現有的 BigQuery 資料集，並包含下列支援的物件：

* [授權 view](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)
* [已獲授權的資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)
* [BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)
* [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)
* [具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)
* [日常安排](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw)

  + [使用者定義函式 (UDF)](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)
  + [資料表函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)
  + [SQL 預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)
* [Tables](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)
* [資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)
* [觀看次數](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)

共用資料集支援[資料欄層級安全性](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)。

#### 共用主題

共用主題是 [Pub/Sub 主題](https://docs.cloud.google.com/pubsub/docs/create-topic?hl=zh-tw)，也是 [BigQuery 串流資料共用](https://docs.cloud.google.com/bigquery/docs/analytics-hub-stream-sharing?hl=zh-tw)的單位。發布者會在專案中建立或使用現有的 Pub/Sub 主題，並將主題發布給訂閱者。

#### 資料交換庫

資料交換是容器，可讓發布者共用資料清單，並讓訂閱者直接瀏覽及要求存取權。其中包含參照共用資源的項目。發布商和管理員可以在交易平台和刊登層級授予訂閱者存取權，避免在基礎共用資源上明確授予存取權。[建立資料交換作業](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#create-exchange)時，您可以指派主要聯絡電子郵件地址，方便訂閱者與資料交換作業擁有者聯絡。

資料交換可以是下列其中一種：

* **私人資料交換**：資料交換預設為私人。只有具備該資料交換存取權的使用者或群組，才能查看或訂閱其清單。
* **公開資料交換**：所有[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 都能[探索](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)及[訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)公開資料交換的清單。詳情請參閱「[公開資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)」。

Analytics Hub 管理員角色可讓您建立多個資料交換庫，並管理執行 BigQuery sharing 工作的團隊成員。

#### 清單

清單是發布者在資料交換庫中列出的共用資源參照資訊。發布者可以建立項目，並指定資源說明、範例查詢、範例訊息資料、說明文件連結，以及訂閱者適用的相關操作說明。建立房源資訊時，你可以指派主要聯絡電子郵件地址、供應商詳細資料和發布者詳細資料。詳情請參閱「[管理房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)」。

根據為清單及其父項資料交換設定的 IAM 政策，清單可以是下列其中一種類型：

* **不公開產品資訊**：根據預設，產品資訊為不公開，且直接與特定使用者或群組共用。舉例來說，私人房源資訊可以參照您與貴機構特定團隊共用的內部指標資料集。
* **公開清單**：與所有[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 共用。公開資料交換中的清單即為公開清單。這些項目可能參照免費的公開資源或商業資源。如果資訊是商業資源，訂閱者可以直接向資料供應商要求存取權，或購買[與 Cloud Marketplace 整合的商業資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)。

#### 資料輸出選項

如果是 BigQuery 共用資料集，發布者可透過資料輸出選項，限制訂閱者從連結的資料集匯出資料。

發布商可以對目錄、查詢結果或兩者啟用資料輸出限制。資料輸出受限時，會受到下列限制：

* 無法使用複製、複製、匯出和快照 API。
* 控制台不提供複製、複製、匯出及快照選項。 Google Cloud
* 受限資料集無法使用 BigQuery 資料移轉服務。
* [`CREATE TABLE AS SELECT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)和[寫入目的地資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw)功能無法使用。
* [`CREATE VIEW AS SELECT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_view_statement)，以及寫入目的地檢視區塊的功能。

[建立房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)時，你可以設定適當的資料輸出選項。

### 訂閱者工作流程

在訂閱者工作流程中，您可以瀏覽資料交換庫來探索、訂閱項目，並查詢專案中的連結資源：

以下各節說明訂閱者工作流程中的元件。

#### 連結的資料集

連結資料集是唯讀 BigQuery 資料集，做為共用資料集的指標或參照。訂閱項目會在專案中建立連結的資料集，不會複製資料。訂閱者可以即時查詢標準資料表和檢視畫面，但無法在資料集中新增或更新物件。

連結的資料集有權存取共用資料集中的資料表和檢視表，不需對基礎來源資料集進行額外的 IAM 授權。除了標準資料表和檢視表外，連結的資料集也支援下列授權資源：

* [授權 view](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)
* [已授權的資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)
* [獲得授權的處理常式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)

如要進一步瞭解連結的資料集，請參閱「[查看及訂閱商家資訊和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)」。

#### 連結的 Pub/Sub 訂閱項目

訂閱含有共用主題的清單，會在訂閱者專案中建立連結的 Pub/Sub 訂閱項目，不會複製共用主題或訊息資料。[連結的 Pub/Sub 訂閱項目](https://docs.cloud.google.com/pubsub/docs/subscription-overview?hl=zh-tw)訂閱者可以存取發布至共用主題的訊息，不需在來源主題上取得額外的 IAM 授權。發布商可以直接在 Pub/Sub 中管理訂閱項目，也可以透過 BigQuery sharing 共用訂閱項目管理功能。

如要進一步瞭解連結的 Pub/Sub 訂閱項目，請參閱「[透過 Pub/Sub 共用串流](https://docs.cloud.google.com/bigquery/docs/analytics-hub-stream-sharing?hl=zh-tw)」。

## 應用實例

本節提供範例，說明如何使用 BigQuery sharing 進行合作夥伴協作和資料營利。

### 合作夥伴協作

假設您是零售商，貴組織在名為 `Forecasting` 的 Google Cloud 專案中，維護即時需求預測資料。您想與供應鏈網路中的數百家供應商分享這項需求預測資料。以下各節說明如何在角色之間共用資料。

#### 管理員

身為 `Forecasting` 專案的擁有者，您啟用了 Analytics Hub API，並將 Analytics Hub 管理員角色 (`roles/analyticshub.admin`) 授予管理資料交換作業的團隊成員。具備這個角色的主體是 *BigQuery sharing administrators*。

BigQuery 共用管理員可以執行下列工作：

* 建立、更新、刪除及共用貴組織 `Forecasting` 專案中的資料交換作業。
* 透過 Analytics Hub 管理員角色，管理其他 BigQuery sharing 管理員。
* 授予員工 [Analytics Hub Publisher 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.publisher) (`roles/analyticshub.publisher`)，即可管理 BigQuery sharing 發布者。如果員工只需要更新、刪除及共用項目，而不必建立項目，請授予 [Analytics Hub 項目管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.listingAdmin) (`roles/analyticshub.listingAdmin`)。
* 如要管理 BigQuery sharing 訂閱者，請將 [Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.subscriber) (`roles/analyticshub.subscriber`) 授予由所有供應商組成的 Google 群組。如果供應商只需要查看可用的交易平台和刊登資訊，不需要訂閱，請授予[Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`)。

詳情請參閱「[BigQuery sharing IAM 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#user_roles)」和「[管理資料交換作業](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)」。

#### 發布者

在這種情況下，資料發布者會將供應鏈資料集打包成個別的商品資訊，以滿足供應商需求。發布者在 `Forecasting` 專案中建立下列清單：

* 商品資訊 A：需求預測資料集 1
* 項目 B：需求預測資料集 2
* 清單 C：需求預測資料集 3

發布者可以[追蹤共用資料集的使用指標](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw#use-analytics-hub)，包括下列詳細資料：

* 針對共用資料集執行的工作。
* 訂閱者專案和組織的用量詳細資料。
* 處理的資料列和位元組總數。

詳情請參閱「[管理商店資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)」。

#### 訂閱者

訂閱者可以在資料交換中瀏覽可存取的清單。供應商訂閱這些資訊後，即可將資料集新增至專案做為連結資料集。供應商接著就能對這些連結的資料集執行查詢，並即時擷取預測結果。

詳情請參閱「[查看及訂閱房源和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)」。

### 資料營利

假設您是金融資料供應商，在名為 `MarketDataSource` 的 Google Cloud 專案中，有精選的歷來股票定價資料集。您想將這項資料提供給外部金融機構和交易商，藉此營利。以下各節說明如何透過 BigQuery sharing，將資料轉化為收益。

#### 管理員

身為 `MarketDataSource` 專案的擁有者，您會啟用 Analytics Hub API 和 Cloud Marketplace API，然後將 Analytics Hub 管理員角色 (`roles/analyticshub.admin`) 授予管理商業資料交換作業的團隊。擁有這個角色的主體是 *BigQuery sharing 管理員*。

BigQuery 共用管理員可以執行下列工作：

* 建立公開資料交易所，並[與 Cloud Marketplace 整合](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)。
* 如要管理 BigQuery sharing 發布者，請將 Analytics Hub 發布者角色 (`roles/analyticshub.publisher`) 授予負責建立商業項目的資料工程師。如果員工只需要更新、刪除及共用產品資訊，不需要建立產品資訊，請授予 Analytics Hub 產品資訊管理員角色 (`roles/analyticshub.listingAdmin`)。
* 在 Cloud Marketplace 中管理商業條款和定價模式。

詳情請參閱「[管理資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)」和「[與 Cloud Marketplace 整合的商業產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)」。

#### 發布者

在這個情境中，發布者會根據訂閱模式，將金融資料產品包裝成不同層級的資訊。發布者會建立下列項目：

* 項目 A：全球股價 (按月訂閱)
* 項目 B：即時市場信號 (按年訂閱)
* 項目 C：歷史經濟指標 (免費試用)

發布者可以[追蹤共用資料集的使用指標](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw#use-analytics-hub)，包括下列詳細資料：

* 針對共用資料集執行的工作。
* 訂閱者專案和組織的用量詳細資料。
* 處理的總列數和位元組數。

詳情請參閱「[管理房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)」。

#### 訂閱者

訂閱者可以在 BigQuery sharing 或直接在 Cloud Marketplace 瀏覽清單。購買訂閱方案後，訂閱者會在 Google Cloud 專案中建立連結的資料集，並搭配專屬交易模型查詢歷來資料，不必手動擷取資料或複製檔案。

詳情請參閱「[查看及訂閱房源和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)」。

## 定價

在 BigQuery 共用中管理資料交換或資訊清單，不會產生額外費用。

下表列出支援資源的定價模式：

| 資源 | 發布商費用 | 訂閱者費用 | 更多資訊 |
| --- | --- | --- | --- |
| **BigQuery 資料集** | 資料儲存 | 對共用資料執行的查詢 (隨選或容量計價) | [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw) |
| **Pub/Sub 主題** | 寫入的資料 (發布處理量) 和網路輸出 (如適用) | 資料讀取 (訂閱處理量) 和網路輸出 (如適用) | [Pub/Sub 定價](https://cloud.google.com/pubsub/pricing?hl=zh-tw#pubsub) |

## 支援的地區

下列區域和多區域支援 BigQuery sharing 功能：

#### 區域

下表列出美洲地區可共用裝置的區域。

| 區域說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- |
| 俄亥俄州哥倫布 | `us-east5` |  |
| 達拉斯 | `us-south1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 拉斯維加斯 | `us-west4` |  |
| 洛杉磯 | `us-west2` |  |
| 墨西哥 | `northamerica-south1` |  |
| 蒙特婁 | `northamerica-northeast1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 北維吉尼亞州 | `us-east4` |  |
| 奧克拉荷馬州 | `us-central2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 奧勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 鹽湖城 | `us-west3` |  |
| 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 聖地亞哥 | `southamerica-west1` |  |
| 南卡羅來納州 | `us-east1` |  |
| 多倫多 | `northamerica-northeast2` |  |
|

下表列出可使用共用功能的亞太地區。

| 區域說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- |
| 德里 | `asia-south2` |  |
| 香港 | `asia-east2` |  |
| 雅加達 | `asia-southeast2` |  |
| 墨爾本 | `australia-southeast2` |  |
| 孟買 | `asia-south1` |  |
| 大阪 | `asia-northeast2` |  |
| 首爾 | `asia-northeast3` |  |
| 新加坡 | `asia-southeast1` |  |
| 雪梨 | `australia-southeast1` |  |
| 台灣 | `asia-east1` |  |
| 東京 | `asia-northeast1` |  |

下表列出可使用分享功能的歐洲地區。

| 區域說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- |
| 比利時 | `europe-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 柏林 | `europe-west10` |  |
| 芬蘭 | `europe-north1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 法蘭克福 | `europe-west3` |  |
| 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 米蘭 | `europe-west8` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 巴黎 | `europe-west9` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 杜林 | `europe-west12` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 華沙 | `europe-central2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |

下表列出中東地區可使用分享功能的區域。

| **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 達曼 | `me-central2` |  |
| 杜哈 | `me-central1` |  |
| 特拉維夫 | `me-west1` |  |

下表列出可分享位置資訊的非洲地區。

| **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 約翰尼斯堡 | `africa-south1` |  |

#### 多區域

下表列出可共用的多區域。

| 多地區說明 | 多地區名稱 |
| --- | --- |
| 歐盟[會員國](https://europa.eu/european-union/about-eu/countries_en)境內的資料中心1 | `EU` |
| 美國資料中心 | `US` |

1 位於 `EU` 多區域的資料不會儲存在 `europe-west2` (倫敦) 或 `europe-west6` (蘇黎世) 資料中心。

#### Omni 區域

下表列出可分享的 Omni 裝置。

|  | Omni 區域說明 | Omni 區域名稱 |
| --- | --- | --- |
| **AWS** | | |
|  | AWS - 美國東部 (北維吉尼亞州) | `aws-us-east-1` |
|  | AWS - 美國西部 (奧勒岡州) | `aws-us-west-2` |
|  | AWS - 亞太地區 (首爾) | `aws-ap-northeast-2` |
|  | AWS - 亞太地區 (雪梨) | `aws-ap-southeast-2` |
|  | AWS - 歐洲 (愛爾蘭) | `aws-eu-west-1` |
|  | AWS - 歐洲 (法蘭克福) | `aws-eu-central-1` |
| **Azure** | | |
|  | Azure - 美國東部 2 | `azure-eastus2` |

## 配額

如要瞭解 BigQuery sharing 資源配額和限制，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#analytics-hub)」。

## 法規遵循

BigQuery sharing 是 BigQuery 的一部分，符合下列法規遵循計畫：

* [ISO 27001](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [ISO 27017](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [ISO 27018](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [SOC 1](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [SOC 2](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [SOC 3](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [PCI DSS](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [滲透測試](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [HIPAA](https://cloud.google.com/security/compliance/hipaa?hl=zh-tw)
* [HITRUST](https://cloud.google.com/security/compliance/hitrust?hl=zh-tw)

## 限制

以下各節說明 BigQuery 共用的作業和互通性限制。

### 一般資源限制

BigQuery 共用功能適用下列一般資源限制：

* 一個共用資料集最多可連結 1,000 個資料集。
* 一個共用主題最多可有 10,000 個 Pub/Sub 訂閱項目。這項限制包含連結的 Pub/Sub 訂閱項目，以及直接在 Pub/Sub 建立的訂閱項目。
* 含有不支援資源的資料集無法選為共用資料集。如要瞭解支援的物件，請參閱「[共用資料集](#shared_datasets)」。
* 您無法在連結資料集中的個別表格上設定 [IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)或 [IAM 政策](https://docs.cloud.google.com/config-connector/docs/reference/resource-docs/iam/iampolicy?hl=zh-tw)。請改為在連結的資料集層級套用。
* 您無法將 [IAM 標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)附加至連結資料集內的資料表。請改為在連結的資料集層級套用。
* 2023 年 7 月 25 日前建立的連結資料集不會由[訂閱資源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw)回填。
  只有 2023 年 7 月 25 日後建立的訂閱項目，才能與 API 方法搭配使用。

### 發布商限制

如果您是發布商，則適用下列 BigQuery 互通性限制：

* 您必須明確授予訂閱者讀取來源資料集的權限，才能查詢連結資料集中的檢視表。最佳做法是建立[授權 view](https://docs.cloud.google.com/bigquery/docs/share-access-views?hl=zh-tw)，授予訂閱者查看資料的權限，但不授予基礎來源資料的存取權。
* [查詢計畫](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)會顯示共用 view 查詢和常式查詢定義，包括專案 ID 和授權 view 涉及的其他資料集。請勿在共用檢視表或例行查詢中加入加密金鑰等機密資訊。
* 共用資料集會編入 [Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/catalog-overview?hl=zh-tw) 索引。訂閱者可立即取得共用資料集的結構定義更新。不過，如果共用資料集中的訂閱者或資料表超過 100 個，更新作業可能需要最多 18 小時才能建立索引。由於索引作業延遲，訂閱者無法立即在 Google Cloud 控制台搜尋更新後的資源。
* 共用主題會編入 Knowledge Catalog 索引，但您無法依資源類型進行篩選。
* 如果您在列出的資料表上設定[資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)或[資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)政策，訂閱者必須使用 Enterprise 或 Enterprise Plus 版本，才能在連結的資料集上執行查詢工作。如要瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

### 訂閱者限制

如果您是訂閱者，則適用下列 BigQuery 互通性限制：

* 不支援參照連結資料集中資料表的 materialized view。
* 不支援擷取連結資料集資料表的[快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。
* 如果查詢含有連結的資料集和 `JOIN` 陳述式，且超過 1 TB (實體儲存空間)，可能會失敗。如果遇到這個問題，請[聯絡支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。
* 您無法搭配使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)和 `INFORMATION_SCHEMA` 檢視表，[查看連結資料集的中繼資料](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#view-table-metadata)。

### 多區域商店資訊限制

跨多個區域的產品資訊有以下限制：

* 只有共用資料集和連結的資料集副本，才支援多個區域的項目。共用 Pub/Sub 主題或訂閱項目不支援多個區域的房源資訊。
* 資料無塵室不支援多個區域的產品資訊。
* [BigQuery Omni 區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)不支援多個區域的房源資訊。

### 用量指標限制

用量指標有以下限制：

* 2023 年 7 月 20 日前訂閱的產品資訊無法取得用量指標。
* [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)的 `num_rows_processed` 和 `total_bytes_processed` 欄位使用量指標可能含有不準確的資料。
* 只有[BigQuery 工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)的使用量，才支援用量指標。下列資源不支援用量指標：

  + [BigQuery Storage Read API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw#read_from_a_session_stream)
  + [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw)
  + [BigQuery BI Engine 查詢](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)
* [檢視表](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)的用量指標只會填入 2024 年 4 月 22 日之後的查詢。
* 系統不會擷取 BigQuery 中已連結的 Pub/Sub 訂閱項目用量指標。您可以直接在 Pub/Sub 中查看用量。
* BigQuery 共用情形指標資訊主頁不提供 SQL 預存程序。您可以在「`INFORMATION_SCHEMA.ROUTINES`」檢視畫面中查看詳細資料，但無法在「`INFORMATION_SCHEMA.SHARED_DATASET_USAGE`」檢視畫面中查看。詳情請參閱「[使用 `INFORMATION_SCHEMA` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw#use-information-schema)」。

### VPC Service Controls 和 Salesforce Data 360 限制

VPC Service Controls 和 Salesforce Data 360 適用下列限制：

* 除非您為發布者專案、交換專案和訂閱者專案設定適當的[輸入和輸出規則](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw)，否則請勿在 VPC Service Controls perimeter 內的專案中發布共用資料或託管資料交換作業。詳情請參閱「[共用 VPC Service Controls 規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)」。
* Data 360 資料會以檢視畫面形式共用。訂閱者無法存取檢視表參照的基礎資料表。

## 後續步驟

* 瞭解如何[查看及訂閱清單和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。
* 瞭解如何[授予 BigQuery 共用角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw)。
* 瞭解如何[管理資料交換作業](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)和[管理清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-20 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-20 (世界標準時間)。"],[],[]]