Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 共用功能簡介

BigQuery sharing (舊稱 Analytics Hub) 是一個資料交換平台，可讓您透過完善的安全和隱私權架構，大規模地跨機構共用資料和洞察資訊。您可以使用 BigQuery sharing 探索並存取不同資料供應商收錄的資料庫。這個資料庫也包含 Google 提供的資料集。

舉例來說，您可以透過共用功能，使用第三方和 Google 資料集，擴增您的 Analytics 和 ML 計畫。

Analytics Hub Identity and Access Management (IAM) 角色可讓您執行下列共用工作：

* Analytics Hub 發布者可以與合作夥伴聯播網或自家機構即時共用資料。[資訊](#listings)可讓您分享資料，不必複製共用資料，並在 [Google Cloud Marketplace](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw) 或透過自有管道營利。您可以建立可供分析的資料來源目錄，並設定精細的權限，將資料交付給正確的目標對象。您也可以管理訂閱項目，並查看清單的使用指標。
* Analytics Hub 訂閱者可以探索所需資料、將共用資料與現有資料合併，以及使用 [BigQuery 的內建功能](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw#explore-bigquery)。訂閱房源後，系統會在 Google Cloud 專案中建立[連結資料集](#linked_datasets)或連結的 Pub/Sub 訂閱項目。您可以使用[訂閱資源](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions?hl=zh-tw)管理訂閱項目，該資源會儲存訂閱者的相關資訊，並代表發布者和訂閱者之間的連結。
* Analytics Hub 檢視者可以瀏覽 BigQuery sharing 中您有權存取的共用資源，並向發布者要求存取共用資料。您可以在 BigQuery sharing 和 Cloud Marketplace 上，探索整合 Cloud Marketplace 的商業清單。
* Analytics Hub 管理員可以建立[資料交換庫](#data_exchanges)，啟用資料共用功能，然後授權資料發布者和訂閱者存取這些資料交換庫。

詳情請參閱「[設定 Analytics Hub 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw)」。

## 架構

BigQuery 共用功能是根據資料資源的發布和訂閱模型建構而成，可讓您在原地進行零複製共用。Google Cloud BigQuery sharing 支援下列 Google Cloud 資源：

* BigQuery 資料集
* Pub/Sub 主題

### 發布者工作流程

下圖說明發布者如何共用資產：

以下各節說明這個工作流程中的功能。

#### 共用資源

共用資源是發布端在 BigQuery sharing 中分享的單位。

##### 共用的資料集

共用資料集是 BigQuery 資料集，也是 BigQuery sharing 中的資料共用單位。BigQuery 架構將運算和儲存空間分開，因此資料發布者可以與任意數量的訂閱者共用資料集，不必反覆複製資料。發布者可以在專案中建立或使用現有的 BigQuery 資料集，並加入下列支援的物件，然後傳送給訂閱者：

* [授權 view](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)
* [已授權的資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)
* [BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)
* [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)
* [具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)
* [日常安排](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw)
  + [使用者定義的函式 (UDF)](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)
  + [資料表函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)
  + [SQL 預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)
* [Tables](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)
* [表格快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)
* [觀看次數](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)

共用資料集支援[資料欄層級安全性](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)。

請注意 VPC Service Controls 和共用功能有下列限制：

* 請勿在 VPC Service Controls 範圍內的專案中發布共用資料。如果專案中的共用資料集位於 VPC Service Controls 服務範圍內，您需要為交換庫專案 (代管的項目) 和所有訂閱端專案設定適當的[輸入和輸出規則](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw)，才能順利訂閱發布端提供的項目。
* 請勿將交換庫專案放在 VPC Service Controls perimeter 中，否則可能會中斷發布工作流程，且需要為發布端專案和所有訂閱端專案設定[輸入和輸出規則](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw)，才能順利訂閱商家資訊。

##### 共用主題

共用主題是 [Pub/Sub 主題](https://docs.cloud.google.com/pubsub/docs/create-topic?hl=zh-tw)，也是 [BigQuery 中串流資料共用的單位](https://docs.cloud.google.com/bigquery/docs/analytics-hub-stream-sharing?hl=zh-tw)。發布者可以在專案中建立或使用現有的 Pub/Sub 主題，並將主題發布給訂閱者。

#### 資料交換庫

資料交換是容器，可讓您透過自助服務共用資料。其中包含參照共用資源的項目。發布者和管理員可以在交易平台和商家資訊層級授予訂閱者存取權。這有助於您避免明確授予基礎共用資源的存取權。您可以瀏覽資料交換，探索可存取的資料，並訂閱共用資源。[建立資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#create-exchange)時，您可以指派主要聯絡人的電子郵件地址。使用者可以透過這個電子郵件地址，向資料交換擁有者提出問題或疑慮。

資料交換庫可以是下列其中一種類型：

* **私人資料交換。**根據預設，資料交換是私人的，只有可存取該交換庫的使用者或群組，才能查看或訂閱清單。
* **公開資料交換。**根據預設，資料交換是私人的，只有可存取該交換的使用者或群組，才能查看或訂閱其清單。不過，您可以選擇公開資料交換。[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 可以[探索](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#discover-listings)及[訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)公開資料交換庫中的清單。如要進一步瞭解公開資料交換庫，請參閱「[將資料交換庫設為公開](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#make-data-exchange-public)」。

Analytics Hub 管理員角色可讓您建立多個資料交換，並管理執行共用工作的使用者。

#### 清單

清單是發布者在資料交換庫中列出的共用資源參照資訊。發布者可以建立資源清單，並指定資源說明、要執行的範例查詢或範例訊息資料、任何相關文件連結，以及有助於訂閱者使用共用資源的任何其他資訊。建立房源時，你可以指派主要聯絡電子郵件地址、供應商名稱和聯絡人，以及發布者名稱和聯絡人。

使用者可以透過主要聯絡人電子郵件地址，向商家資訊擁有者詢問資料交換相關問題或提出疑慮。供應商名稱和聯絡人是最初提供項目資料的機構。這項資訊為選填。發布者名稱和聯絡人是發布資料的機構，這些資料會用於 BigQuery sharing。您可以選擇是否提供這項資訊，詳情請參閱「[管理房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)」。

根據為目錄設定的 IAM 政策，以及包含目錄的資料交換類型，目錄可分為下列兩種：

* **公開產品資訊。**公開清單會與所有[Google Cloud 使用者 (`allAuthenticatedUsers`)](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 共用。公開資料交換庫中的清單就是公開清單。這些資訊可以是*免費公開資源*或*商業資源*的參考資料。如果清單是商業資源，訂閱者可以直接向資料供應商要求存取清單，也可以瀏覽及購買[整合 Google Cloud Marketplace 的商業清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)。
* **私人房源**。私人房源資訊會直接分享給個人或群組。舉例來說，私人產品資訊可以參照您與機構內其他團隊共用的行銷指標資料集。

### 訂閱者工作流程

下圖說明 Analytics Hub 訂閱者如何與共用資源互動：

以下各節說明訂閱者工作流程中的功能。

#### 已連結的資源

訂閱 BigQuery sharing 項目時，系統會建立連結的資源，將訂閱者連結至基礎共用資源。

##### 連結的資料集

連結的資料集是*唯讀* BigQuery 資料集，做為共用資料集的指標或參照。訂閱項目會在專案中建立連結的資料集，而非資料集副本，因此訂閱者可以讀取資料，但無法在其中新增或更新物件。透過連結的資料集查詢資料表和檢視表等物件時，系統會傳回共用資料集內的資料。如要進一步瞭解連結的資料集，請參閱[查看及訂閱商家資訊和資料交易平台](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。

連結的資料集有權存取共用資料集的資料表和檢視表。
訂閱者連結資料集後，即可存取共用資料表的資料表和檢視畫面，不必再進行任何身分與存取權管理授權。

連結的資料集支援下列物件：

* [授權 view](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)
* [已授權的資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)
* [獲得授權的處理常式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)

##### 已連結的 Pub/Sub 訂閱項目

訂閱共用主題的房源資訊時，系統會在訂閱端專案中建立連結的 Pub/Sub 訂閱項目。系統不會建立共用主題或訊息資料的副本。連結的 [Pub/Sub 訂閱項目](https://docs.cloud.google.com/pubsub/docs/subscription-overview?hl=zh-tw)訂閱者可以存取發布至共用主題的訊息。訂閱者可存取共用主題的訊息資料，不需額外 IAM 授權。發布者可以直接在 Pub/Sub 中管理訂閱項目，也可以透過 BigQuery sharing 共用訂閱項目管理功能。如要進一步瞭解連結的 Pub/Sub 訂閱項目，請參閱「[透過 Pub/Sub 串流分享](https://docs.cloud.google.com/bigquery/docs/analytics-hub-stream-sharing?hl=zh-tw)」。

## 資料輸出選項 (僅限 BigQuery 共用資料集)

發布商可透過資料輸出選項，限制訂閱者從已連結的 BigQuery 資料集匯出資料。

發布商可以對目錄、查詢結果或兩者啟用資料輸出限制。限制資料輸出時，適用下列限制：

* 無法使用複製、複製、匯出及快照 API。
* 您無法在 Google Cloud 控制台中複製、複製、匯出及建立快照。
* 您無法將受限資料集連結至資料表探索工具。
* 受限資料集無法使用 BigQuery 資料移轉服務。
* [`CREATE TABLE AS SELECT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)和[寫入目的地資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw)的功能無法使用。
* [`CREATE VIEW AS SELECT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_view_statement)，且無法寫入目的地檢視區塊。

[建立產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)時，你可以設定適當的資料輸出選項。

## 限制

BigQuery 共用功能有下列限制：

* 一個共用資料集最多可連結 1,000 個資料集。
* 一個共用主題最多可有 10,000 個 Pub/Sub 訂閱項目。這項限制包括連結的 Pub/Sub 訂閱項目，以及在 BigQuery sharing 功能以外建立的 Pub/Sub 訂閱項目 (例如直接從 Pub/Sub 建立)。
* [建立清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)時，無法選取包含不支援資源的資料集做為共用資料集。如要進一步瞭解 BigQuery sharing 支援的 BigQuery 物件，請參閱[共用資料集](#shared_datasets)。
* 您無法在連結資料集中的個別表格上設定 [IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)或 [IAM 政策](https://docs.cloud.google.com/config-connector/docs/reference/resource-docs/iam/iampolicy?hl=zh-tw)。請改為在連結的資料集層級套用。
* 您無法在連結資料集中的資料表上附加 [IAM 標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)。請改為在連結的資料集層級套用。
* 2023 年 7 月 25 日前建立的連結資料集，不會由[訂閱資源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw)回填。
  只有在 2023 年 7 月 25 日後建立的訂閱項目，才能搭配 API 方法使用。
* 如果您是發布商，則適用下列 BigQuery 互通性限制：

  + 您必須授予訂閱者明確的權限，才能讀取來源資料集，並查詢連結資料集中的檢視表。如要授予檢視表的存取權，最佳做法是建立[授權檢視表](https://docs.cloud.google.com/bigquery/docs/share-access-views?hl=zh-tw)。授權檢視表可授予訂閱者檢視表資料的存取權，但不會授予基礎來源資料的存取權。
  + [查詢計畫](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)會顯示共用檢視區塊查詢和常式查詢，包括專案 ID，以及授權檢視區塊中涉及的其他資料集。請勿在共用檢視區塊或例行查詢中加入任何您認為是機密資訊的內容，例如加密金鑰。
  + 系統會在 [Data Catalog](https://docs.cloud.google.com/data-catalog/docs/concepts/overview?hl=zh-tw) (已淘汰) 和 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/catalog-overview?hl=zh-tw) 中為共用資料集建立索引。訂閱者可以立即查看共用資料集的更新內容，例如新增資料表或檢視區塊。不過，在某些情況下，例如共用資料集中有超過 100 個訂閱者或資料表時，這些服務可能需要最多 18 小時才能為更新內容建立索引。由於索引作業延遲，訂閱者無法立即在 Google Cloud 控制台中搜尋這些更新的資源。
  + 系統會在 Data Catalog (已淘汰) 和 Knowledge Catalog 中為共用主題建立索引，但您無法依資源類型進行篩選。
  + 如果您已在列出的資料表上設定[資料列層級安全防護](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)或[資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)政策，訂閱者必須是 Enterprise 或 Enterprise Plus 客戶，才能在連結的資料集上執行查詢作業。如要瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
* 如果您是訂閱者，則適用下列 BigQuery 互通性限制：

  + 系統不支援參照連結資料集中資料表的具體化檢視表。
  + 系統不支援對連結資料集資料表建立[快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。
  + 如果查詢的連結資料集和 `JOIN` 陳述式大於 1 TB (實際儲存空間)，查詢可能會失敗。如要解決這個問題，請[與支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。
  + 您無法搭配 `INFORMATION_SCHEMA` 檢視使用[區域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)，[查看連結資料集的中繼資料](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#view-table-metadata)。
  + 多個地區的商家資訊有以下限制：
  + 只有共用資料集和連結的資料集副本支援多個區域的項目。共用 Pub/Sub 主題和訂閱項目不支援多個區域的刊登。
  + 資料無塵室不支援多個區域的房源資訊。
  + [BigQuery Omni 地區](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)不支援多個地區的房源資訊。
* 使用指標有以下限制：

  + 如果是在 2023 年 7 月 20 日前訂閱，就無法取得房源的使用指標。
  + [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)
    `num_rows_processed` 和 `total_bytes_processed` 欄位的使用指標
    可能含有不準確的資料。
  + 用量指標僅支援 [BigQuery 作業](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)的用量。下列資源不支援消耗量：

    - [BigQuery Storage Read API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw#read_from_a_session_stream)
    - [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw)
    - [BigQuery BI Engine 查詢](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)
  + 只有 2024 年 4 月 22 日之後的查詢，才會填入[檢視](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)的用量指標。
  + 系統不會擷取 BigQuery 中已連結的 Pub/Sub 訂閱項目用量指標。您可以繼續直接在 Pub/Sub 中查看用量。
  + BigQuery sharing 用量指標資訊主頁不提供 SQL 預存程序。您可以在 `INFORMATION_SCHEMA.ROUTINES` 檢視畫面中查看詳細資料，但無法在 `INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面中查看。詳情請參閱「[使用 `INFORMATION_SCHEMA` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw#use-information-schema)」。
* 訂閱 Salesforce Data Cloud 資料時，有下列限制：

  + 系統會以檢視畫面形式分享 Data Cloud 資料。訂閱者無法存取檢視畫面參照的基礎資料表。

## 支援的地區

BigQuery sharing 功能支援下列區域和多重區域。

#### 區域

下表列出美洲地區中可分享的區域。

| 地區說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- |
| 俄亥俄州哥倫布 | `us-east5` |  |
| 達拉斯 | `us-south1` |  |
| 愛荷華州 | `us-central1` |  |
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

下表列出亞太地區可分享的區域。

| 地區說明 | 區域名稱 | 詳細資料 |
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

下表列出歐洲地區中可分享的區域。

| 地區說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- |
| 比利時 | `europe-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 柏林 | `europe-west10` |  |
| 芬蘭 | `europe-north1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 法蘭克福 | `europe-west3` |  |
| 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 米蘭 | `europe-west8` |  |
| 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 巴黎 | `europe-west9` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 杜林 | `europe-west12` |  |
| 華沙 | `europe-central2` |  |
| 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |

下表列出可共用位置資訊的中東地區。

| **地區說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 達曼 | `me-central2` |  |
| 杜哈 | `me-central1` |  |
| 特拉維夫市 | `me-west1` |  |

下表列出非洲可分享位置資訊的地區。

| **地區說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 約翰尼斯堡 | `africa-south1` |  |

#### 多區域

下表列出可共用的多重區域。

| 多地區說明 | 多地區名稱 |
| --- | --- |
| 歐盟1[成員國](https://europa.eu/european-union/about-eu/countries_en)境內的資料中心 | `EU` |
| 美國資料中心 | `US` |

1 位於 `EU` 多地區的資料，不會存放在 `europe-west2` (倫敦) 或 `europe-west6` (蘇黎世) 資料中心。

#### Omni 區域

下表列出可分享的 Omni。

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

## 用途範例

本節提供如何使用 BigQuery 共用的範例。

假設您是零售商，而貴機構在名為「預測」的 Google Cloud 專案中，有即時需求預測資料。您想與供應鏈系統中的數百家供應商分享這項需求預測資料。以下各節說明如何透過 BigQuery sharing 功能，與供應商共用資料。

### 管理員

身為預測專案的擁有者，您必須先啟用 API，然後將[Analytics Hub 管理員角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#ah-admin-role) (`roles/analyticshub.admin`) 指派給專案中的資料交換管理員。具有 Analytics Hub 管理員角色的使用者稱為 *BigQuery sharing 管理員*。

BigQuery sharing 管理員可以執行下列工作：

* 在貴機構的預測專案中，建立、更新、刪除及共用資料交換。
* 使用 Analytics Hub 管理員角色，管理其他 *BigQuery sharing 管理員*。
* 授予貴機構員工 [Analytics Hub 發布者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.publisher) (`roles/analyticshub.publisher`)，即可管理 *BigQuery sharing 發布者*。如要讓員工只能更新、刪除及分享商家檔案，但無法建立商家檔案，請授予他們「Analytics Hub 清單管理員」角色 (`roles/analyticshub.listingAdmin`)。
* 授予由所有供應商組成的 Google 群組「Analytics Hub 訂閱者」角色 (`roles/analyticshub.subscriber`)，即可管理 *BigQuery sharing 訂閱者*。如要讓供應商只能查看可用的交換庫和刊登項目，請授予他們[Analytics Hub 檢視者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`)。這些供應商無法訂閱刊登項目。

詳情請參閱「[BigQuery sharing IAM 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw#user_roles)」和「[管理資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)」。

### 發布端

發布商會在「預測」專案或其他專案中，為資料集建立下列項目：

* 清單 A：需求預測資料集 1
* 項目 B：需求預測資料集 2
* 清單 C：需求預測資料集 3

資料供應商可以[追蹤共用資料集的用量指標](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw#use-analytics-hub)。用量指標包括下列詳細資料：

* 針對共用資料集執行的工作。
* 訂閱者專案和機構使用共用資料集的詳細資料。
* 工作處理的資料列和位元組數量。

詳情請參閱「[管理房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)」。

### 訂閱人數

訂閱者可以瀏覽資料交換中可存取的項目。他們也可以訂閱這些資訊，並建立連結的資料集，將這些資料集新增至專案。供應商接著就能對這些連結的資料集執行查詢，並即時擷取結果。

詳情請參閱「[查看及訂閱商家資訊和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)」。

## 定價

管理資料交易或資料集清單不會產生額外費用。

如果是 BigQuery 資料集，發布者需支付資料儲存費用，而訂閱者則需根據以量計價或容量計價模式，支付對共用資料執行的查詢費用。如要瞭解價格，請參閱「[BigQuery 計價方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」一文。

如果是 Pub/Sub，主題發布者須支付寫入共用主題的位元組總數 (發布總處理量) 和網路輸出 (如適用)。訂閱者須支付從連結訂閱項目讀取的位元組總數 (訂閱吞吐量)，以及網路輸出量 (如適用)。詳情請參閱「[Pub/Sub 定價](https://cloud.google.com/pubsub/pricing?hl=zh-tw#pubsub)」。

## 配額

如要瞭解 BigQuery sharing 配額，請參閱[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#analytics-hub)。

## 法規遵循

BigQuery sharing 是 BigQuery 的一部分，符合下列法規遵循計畫：

* [ISO 27001](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [ISO 27017](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [ISO 27018](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [SOC 1](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [SOC 2](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [SOC 3](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [PCI](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [滲透測試](https://cloud.google.com/security/compliance/services-in-scope?hl=zh-tw)
* [健康保險流通與責任法案](https://cloud.google.com/security/compliance/hipaa?hl=zh-tw)
* [HITRUST](https://cloud.google.com/security/compliance/hitrust?hl=zh-tw)

## VPC Service Controls

您可以設定必要的輸入和輸出規則，允許發布者和訂閱者從設有 VPC Service Controls 範圍的專案存取資料。詳情請參閱「[共用 VPC Service Controls 規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[查看及訂閱清單和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)。
* 瞭解如何授予 [Analytics Hub 角色](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]