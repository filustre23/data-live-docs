* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 BigQuery 中使用 Salesforce Data Cloud 資料

本文說明如何使用 BigQuery Omni，在 BigQuery 中存取及分析 Salesforce Data Cloud 資料。本文說明如何連結 BigQuery 中的 Data Cloud 資料集，以便執行查詢、將資料與 Google Cloud中的資料表聯結，以及使用跨雲端具體化檢視表複製資料。

本文適用於想要使用 BigQuery 深入分析 Data Cloud 資料，或將資料與 Google Cloud 中的資料合併，以進行跨雲端分析的 Data Cloud 使用者，而且不必建構及維護「擷取、轉換及載入」(ETL) 管道。

## 事前準備

您必須是 Data Cloud 使用者，才能使用 Data Cloud 資料。如果專案已啟用 VPC Service Controls，您需要額外權限。

### 必要的角色

必須具備下列角色和權限：

* Analytics Hub 訂閱者 (`roles/analyticshub.subscriber`)
* BigQuery 管理員 (`roles/bigquery.admin`)

## 從 Data Cloud 共用資料

本文件說明如何將 Data Cloud 中的資料共用至 BigQuery - [自備授權資料共用 - 無須 ETL 即可與 BigQuery 整合](https://help.salesforce.com/s/articleView?id=sf.c360_a_access_data_from_google_bigquery.htm&type=5)。

## 將 Data Cloud 資料集連結至 BigQuery

如要在 BigQuery 中存取 Data Cloud 資料集，請先按照下列步驟將資料集連結至 BigQuery：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「Salesforce Data Cloud」

   系統會顯示 Data Cloud 資料集。您可以使用下列命名模式依名稱尋找資料集：

   ```
   listing_DATA_SHARE_NAME_TARGET_NAME
   ```

   更改下列內容：
   * `DATA_SHARE_NAME`：Data Cloud 中的資料共用名稱。
   * `TARGET_NAME`：Data Cloud 中 BigQuery 目標的名稱。
3. 按一下要新增至 BigQuery 的資料集。
4. 按一下「將資料集新增至專案」。
5. 指定連結的資料集名稱。

建立連結的資料集後，即可探索資料集和其中的資料表。系統會動態從 Data Cloud 擷取所有資料表的中繼資料。資料集內的所有物件都是對應至 Data Cloud 物件的檢視區塊。BigQuery 支援三種 Data Cloud 物件：

* 資料湖泊物件 (DLO)
* 資料模型物件 (DMO)
* 計算洞察物件 (CIO)

所有這些物件都會以 BigQuery 中的檢視表表示。
這些檢視區塊指向儲存在 Amazon S3 中的隱藏資料表。

**注意：** 如果您使用 VPC Service Controls，且 Analytics Hub API 受到限制，則需要在 VPC Service Controls perimeter 中建立[輸出規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)，納入 Data Cloud Sharing 生產者專案。

## 使用 Data Cloud 資料

下列範例使用名為 Northwest Trail Outfitters (NTO) 的資料集，該資料集託管於 Data Cloud。這個資料集包含三個資料表，代表 NTO 機構的線上銷售資料：

* `linked_nto_john.nto_customers__dll`
* `linked_nto_john.nto_products__dll`
* `linked_nto_john.nto_orders__dll`

這些範例使用的另一個資料集是離線銷售點資料。這涵蓋離線銷售，並包含三個資料表：

* `nto_pos.customers`
* `nto_pos.products`
* `nto_pos.orders`

下列資料集會儲存其他物件：

* `aws_data`
* `us_data`

### 執行臨時查詢

您可以使用 BigQuery Omni 執行臨時查詢，透過訂閱的資料集分析 Data Cloud 資料。以下範例顯示簡單的查詢，可從 Data Cloud 查詢 customers 資料表。

```
SELECT name__c, age__c
  FROM `listing_nto_john.nto_customers__dll`
  WHERE age > 40
  LIMIT 1000;
```

### 執行跨雲端查詢

透過跨雲端查詢，您可以彙整 BigQuery Omni 區域中的任何資料表，以及 BigQuery 區域中的資料表。如要進一步瞭解跨雲端查詢，請參閱這篇[網誌文章](https://cloud.google.com/blog/products/data-analytics/announcing-bigquery-omni-cross-cloud-joins?hl=zh-tw)。在本例中，我們擷取名為 `john` 的顧客的總銷售額。

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

### 透過 CTAS 進行跨雲端資料移轉

您可以使用「Create Table As Select (CTAS)」將資料從 BigQuery Omni 區域的 Data Cloud 資料表移至 `US` 區域。

```
-- Move all the orders for March to the US region
CREATE OR REPLACE TABLE us_data.online_orders_march
  AS SELECT * FROM listing_nto_john.nto_orders__dll
    WHERE EXTRACT(MONTH FROM order_time) = 3
```

目的地資料表是 `US`
區域中的 BigQuery 代管資料表。這個資料表可以與其他資料表彙整。這項作業會產生 AWS 輸出費用，費用金額取決於傳輸的資料量。

資料轉移後，在 `online_orders_march` 資料表中執行的任何查詢都不會產生輸出費用。

### 跨雲端具體化檢視表

跨雲端具體化檢視區塊 ([CCMV](https://cloud.google.com/blog/products/data-analytics/introducing-bigquery-omni-cross-cloud-materialized-views?hl=zh-tw)) 可將資料從 BigQuery Omni 區域，以遞增方式移轉至非 BigQuery Omni 的 BigQuery 區域。設定新的 CCMV，從線上交易移轉總銷售額摘要，並將該資料複製到 `US` 區域。

您可以從廣告資料中心存取 CCMV，並與其他廣告資料中心資料合併。在大多數情況下，CCMV 的運作方式與一般 BigQuery 代管資料表相同。

#### 建立本機具體化檢視表

如要建立本機具體化檢視表，請按照下列步驟操作：

```
-- Create a local materialized view that keeps track of total sales by day

CREATE MATERIALIZED VIEW `aws_data.total_sales`
  OPTIONS (enable_refresh = true, refresh_interval_minutes = 60)
  AS SELECT EXTRACT(DAY FROM order_time) AS date, SUM(order_total) as sales
    FROM `listing_nto_john.nto_orders__dll`
    GROUP BY 1;
```

#### 授權具體化檢視表

您必須授權具體化檢視區塊，才能建立 CCMV。您可以授權檢視表 (`aws_data.total_sales`) 或資料集 (`aws_data`)。如要授權具體化檢視表，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 開啟來源資料集 `listing_nto_john`。
3. 按一下「共用」，然後點選「授權資料集」。
4. 輸入資料集名稱 (本例為 `listing_nto_john`)，然後按一下「確定」。

#### 建立具體化檢視表副本

在 `US` 區域建立新的副本具體化檢視區。只要來源資料有變更，具體化檢視區就會定期複製資料，確保副本資料保持最新狀態。

```
-- Create a replica MV in the us region.
CREATE MATERIALIZED VIEW `us_data.total_sales_replica`
  AS REPLICA OF `aws_data.total_sales`;
```

#### 在副本具體化檢視表中執行查詢

以下範例會在備用資源 materialized view 上執行查詢：

```
-- Find total sales for the current month for the dashboard

SELECT EXTRACT(MONTH FROM CURRENT_DATE()) as month, SUM(sales)
  FROM us_data.total_sales_replica
  WHERE month = EXTRACT(MONTH FROM date)
  GROUP BY 1
```

## 搭配 `INFORMATION_SCHEMA` 使用 Data Cloud 資料

Data Cloud 資料集支援 BigQuery `INFORMATION_SCHEMA` 檢視區塊。`INFORMATION_SCHEMA` 檢視畫面中的資料會定期從 Data Cloud 同步處理，因此可能過時。[`TABLES`](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw) 和 [`SCHEMATA`](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata?hl=zh-tw) 檢視畫面中的「`SYNC_STATUS`」欄會顯示上次完成同步處理的時間、導致 BigQuery 無法提供最新資料的錯誤，以及修正錯誤所需的步驟。

`INFORMATION_SCHEMA` 查詢不會反映在初始同步前建立的資料集。

Data Cloud 資料集與其他連結資料集一樣，受到[限制](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#limitations)，例如只能在資料集範圍查詢中以 `INFORMATION_SCHEMA` 存取。

## 後續步驟

* 瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 瞭解[跨雲端聯結](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_joins)。
* 瞭解[具體化檢視](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]