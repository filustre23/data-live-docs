Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 價格基準資料表

## 總覽

**注意：** 自 2025 年 9 月 1 日起，BigQuery 將不再支援價格基準報告。建議您改用[價格競爭力報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-price-competitiveness-schema?hl=zh-tw)。如要進一步瞭解如何遷移至新報表，請參閱「[遷移價格競爭力報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-price-competitiveness-migration?hl=zh-tw)」。

BigQuery 中的價格基準資料可協助商家瞭解其他商家如何為相同產品定價。將 Google Merchant Center 報表資料轉移至 BigQuery 時，`Products_PriceBenchmarks_` 資料表的格式會提供每個國家/地區和每項產品的每日價格基準。

如果您使用個別商家 ID，資料會寫入名為 `Products_PriceBenchmarks_MERCHANT_ID` 的表格；如果您使用 MCA 帳戶，資料會寫入名為 `Products_PriceBenchmarks_AGGREGATOR_ID` 的表格。

## 結構定義

`Products_PriceBenchmarks` 資料表具有下列結構定義：

| 欄 | BigQuery 資料類型 | 說明 |
| --- | --- | --- |
| `product_id` | `STRING` | 產品的 Content API REST ID，格式為：`channel:content_language:feed_label:offer_id`，類似於[產品資料表結構定義](https://docs.cloud.google.com/bigquery/docs/merchant-center-products-schema?hl=zh-tw)中定義的方式。這個欄位是主鍵。 |
| `merchant_id` | `INTEGER` | 商家帳戶 ID。 |
| `aggregator_id` | `INTEGER` | 多重客戶帳戶的 Aggregator 帳戶 ID。 |
| `country_of_sale` | `STRING` | 使用者在 Google 上執行查詢的國家/地區。 |
| `price_benchmark_value` | `FLOAT` | 對於透過購物廣告宣傳特定產品的所有商家而言，該項產品的平均點擊加權價格。系統會依照全球交易品項識別碼比對產品。詳情請參閱[這篇說明中心文章](https://support.google.com/merchants/answer/9626903?hl=zh-tw)。 |
| `price_benchmark_currency` | `STRING` | 基準值的幣別。 |
| `price_benchmark_timestamp` | `DATETIME` | 基準測試的時間戳記。 |

## 範例：比較產品價格與基準價格

以下 SQL 查詢會彙整 `Products` 和 `Price Benchmarks` 資料，傳回產品清單和相關基準。

```
WITH products AS
(
  SELECT
    _PARTITIONDATE AS date,
    *
  FROM
    dataset.Products_merchant_id
  WHERE
   _PARTITIONDATE >= 'YYYY-MM-DD'
),
benchmarks AS
(
  SELECT
    _PARTITIONDATE AS date,
    *
  FROM
    dataset.Products_PriceBenchmarks_merchant_id
  WHERE
    _PARTITIONDATE >= 'YYYY-MM-DD'
)
SELECT
  products.date,
  products.product_id,
  products.merchant_id,
  products.aggregator_id,
  products.price,
  products.sale_price,
  benchmarks.price_benchmark_value,
  benchmarks.price_benchmark_currency,
  benchmarks.country_of_sale
FROM
  products
INNER JOIN
  benchmarks
ON products.product_id = benchmarks.product_id AND
   products.merchant_id = benchmarks.merchant_id AND
   products.date = benchmarks.date
```

彙整資料的注意事項：
  
1. 並非所有產品都有基準，因此請視情況使用 INNER JOIN 或 LEFT JOIN。  
2. 每項產品可能會有多個基準 (每個國家/地區一個)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]