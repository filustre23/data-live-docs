Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 BigQuery 中使用 Salesforce Data 360 資料

本文說明如何使用 BigQuery Omni，在 BigQuery 中存取及分析 Salesforce Data 360 資料。這份文件說明如何在 BigQuery 中連結 Data 360 資料集，以便執行查詢、將資料與 Google Cloud中的資料表彙整，以及使用 BigQuery Omni 具體化檢視表複製資料。

本文適用於 Data 360 使用者，他們希望使用 BigQuery 深入分析 Data 360 資料，或將資料與 Google Cloud 中的資料結合，進行跨雲端分析，且不需建構及維護擷取、轉換和載入 (ETL) 管道。

## 事前準備

您必須是 Data 360 使用者，才能使用 Data 360 資料。如果專案已啟用 VPC Service Controls，則需要額外權限。

### 必要的角色

您需要下列角色和權限：

* Analytics Hub 訂閱者 (`roles/analyticshub.subscriber`)
* BigQuery 管理員 (`roles/bigquery.admin`)

## 分享 Data 360 的資料

這份文件說明如何將資料從 Data 360 共用至 BigQuery：[BYOL 資料共用 - 與 BigQuery 進行無 ETL 整合](https://help.salesforce.com/s/articleView?id=sf.c360_a_access_data_from_google_bigquery.htm&type=5)。

## 將 Data 360 資料集連結至 BigQuery

如要在 BigQuery 中存取 Data 360 資料集，請先按照下列步驟將資料集連結至 BigQuery：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「Salesforce Data Cloud」

   系統會顯示 Data 360 資料集。您可以使用下列命名模式，依名稱尋找資料集：

   ```
   listing_DATA_SHARE_NAME_TARGET_NAME
   ```

   更改下列內容：
   * `DATA_SHARE_NAME`：Data 360 中的資料共用名稱。
   * `TARGET_NAME`：Data 360 中的 BigQuery 目標名稱。
3. 點選要新增至 BigQuery 的資料集。
4. 按一下「將資料集新增至專案」。
5. 指定連結資料集的名稱。

建立連結資料集後，即可探索資料集和其中的資料表。所有資料表的中繼資料都是從 Data 360 動態擷取。資料集內的所有物件都是對應至 Data 360 物件的檢視表。BigQuery 支援三種 Data 360 物件：

* 資料湖泊物件 (DLO)
* 資料模型物件 (DMO)
* 計算洞察物件 (CIO)

所有這些物件在 BigQuery 中都會以檢視表呈現。這些檢視表會指向儲存在 Amazon S3 的隱藏資料表。

**注意：** 如果您使用 VPC Service Controls，且 Analytics Hub API 受到限制，則必須在 VPC Service Controls perimeter 建立[輸出規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)，納入 Data 360 Sharing 供應商專案。

## 使用 Data 360 資料

下列範例使用名為 Northwest Trail Outfitters (NTO) 的資料集，該資料集託管於 Data 360。這個資料集包含三個資料表，代表 NTO 組織的線上銷售資料：

* `linked_nto_john.nto_customers__dll`
* `linked_nto_john.nto_products__dll`
* `linked_nto_john.nto_orders__dll`

這些範例中使用的另一個資料集是離線銷售點資料。這涵蓋離線銷售，由三個資料表組成：

* `nto_pos.customers`
* `nto_pos.products`
* `nto_pos.orders`

下列資料集會儲存其他物件：

* `aws_data`
* `us_data`

### 執行臨時查詢

您可以使用 BigQuery Omni 執行臨時查詢，透過訂閱的資料集分析 Data 360 資料。以下範例顯示一項簡單的查詢，可查詢 Data 360 的客戶資料表。

```
SELECT name__c, age__c
  FROM `listing_nto_john.nto_customers__dll`
  WHERE age > 40
  LIMIT 1000;
```

### 執行 BigQuery Omni 查詢

BigQuery Omni 查詢可讓您彙整 BigQuery Omni 區域中的任何資料表，以及 BigQuery 區域中的資料表。如要進一步瞭解 BigQuery Omni 查詢，請參閱這篇[網誌文章](https://cloud.google.com/blog/products/data-analytics/announcing-bigquery-omni-cross-cloud-joins?hl=zh-tw)。在這個範例中，我們擷取了名為 `john` 的客戶總銷售額。

```
-- Get combined sales for a customer from both offline and online sales
USING (
  SELECT total_price FROM `listing_nto_john.nto_orders__dll`
       WHERE customer_name = 'john'
  UNION ALL
  SELECT total_price FROM `listing_nto_john.nto_orders__dll`
       WHERE customer_name = 'john'
) a SELECT SUM(total_price);
```

### 透過 CTAS 執行 BigQuery Omni 資料移轉

您可以使用 Create Table As Select (CTAS)，將資料從 BigQuery Omni 區域中的 Data 360 資料表移至 `US` 區域。

```
-- Move all the orders for March to the US region
CREATE OR REPLACE TABLE us_data.online_orders_march
  AS SELECT * FROM listing_nto_john.nto_orders__dll
    WHERE EXTRACT(MONTH FROM order_time) = 3
```

目的地資料表是 `US` 區域中的 BigQuery 代管資料表。這個資料表可以與其他資料表彙整。這項作業會根據轉移的資料量產生 AWS egress 費用。

資料移動後，您就不必再為 `online_orders_march` 資料表中執行的任何查詢支付輸出費用。

### BigQuery Omni materialized view

BigQuery Omni materialized view ([CCMV](https://cloud.google.com/blog/products/data-analytics/introducing-bigquery-omni-cross-cloud-materialized-views?hl=zh-tw)) 會以遞增方式，將資料從 BigQuery Omni 區域移轉至非 BigQuery Omni BigQuery 區域。設定新的 CCMV，轉移線上交易的總銷售額摘要，並將資料複製到 `US` 區域。

您可以從廣告資料中心存取 CCMV，並與其他廣告資料中心資料彙整。CCMV 的運作方式大致與一般 BigQuery 代管資料表相同。

#### 建立本機 materialized view

如要建立本機 materialized view，請按照下列步驟操作：

```
-- Create a local materialized view that keeps track of total sales by day

CREATE MATERIALIZED VIEW `aws_data.total_sales`
  OPTIONS (enable_refresh = true, refresh_interval_minutes = 60)
  AS SELECT EXTRACT(DAY FROM order_time) AS date, SUM(order_total) as sales
    FROM `listing_nto_john.nto_orders__dll`
    GROUP BY 1;
```

#### 授權 materialized view

您必須授權 materialized view，才能建立 CCMV。您可以授權檢視表 (`aws_data.total_sales`) 或資料集 (`aws_data`)。如要授權 materialized view，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 開啟來源資料集 `listing_nto_john`。
3. 依序點選「共用」和「授權資料集」。
4. 輸入資料集名稱 (在本例中為 `listing_nto_john`)，然後按一下「確定」。

#### 建立 materialized view 副本

在 `US` 區域建立新的 materialized view 副本。每當來源資料變更時，materialized view 就會定期複製，確保副本保持最新狀態。

```
-- Create a replica MV in the us region.
CREATE MATERIALIZED VIEW `us_data.total_sales_replica`
  AS REPLICA OF `aws_data.total_sales`;
```

#### 對副本 materialized view 執行查詢

以下範例會對副本 materialized view 執行查詢：

```
-- Find total sales for the current month for the dashboard

SELECT EXTRACT(MONTH FROM CURRENT_DATE()) as month, SUM(sales)
  FROM us_data.total_sales_replica
  WHERE month = EXTRACT(MONTH FROM date)
  GROUP BY 1
```

## 搭配`INFORMATION_SCHEMA`使用 Data 360 資料

Data 360 資料集支援 BigQuery `INFORMATION_SCHEMA` 檢視表。`INFORMATION_SCHEMA` 檢視表中的資料會定期從 Data 360 同步，因此可能不是最新資料。[`TABLES`](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw) 和 [`SCHEMATA`](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata?hl=zh-tw) 檢視表中的 `SYNC_STATUS` 欄會顯示上次完成同步處理的時間、導致 BigQuery 無法提供最新資料的錯誤，以及修正錯誤所需的步驟。

`INFORMATION_SCHEMA` 查詢不會反映在初始同步處理前，最近建立的資料集。

Data 360 資料集與其他連結資料集一樣，須遵守相同的[限制](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#limitations)，例如只能在資料集範圍查詢中，透過 `INFORMATION_SCHEMA` 存取。

## 後續步驟

* 瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 瞭解 [BigQuery Omni join](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_joins)。
* 瞭解 [materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]