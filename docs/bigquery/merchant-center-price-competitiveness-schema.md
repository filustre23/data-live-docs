Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 價格競爭力表

## 總覽

BigQuery 中的價格競爭力資料可協助商家瞭解其他商家如何為相同產品定價。當您將 Google Merchant Center 報表資料移轉至 BigQuery 時，`PriceCompetitiveness_` 資料表的格式會提供每個國家/地區和每項產品的每日價格基準。價格競爭力表格也包含產品的其他屬性，協助你瞭解某個類別或品牌的價格競爭力。

如果您使用個別商家 ID，資料會寫入名為 `PriceCompetitiveness_MERCHANT_ID` 的資料表；如果您使用 MCA 帳戶，資料會寫入名為 `PriceCompetitiveness_AGGREGATOR_ID` 的資料表。

**注意：** 如要存取價格競爭力資料，你必須符合[市場洞察的資格規定](https://support.google.com/merchants/answer/9712881?hl=zh-tw)。

## 結構定義

`PriceCompetitiveness_` 資料表具有下列結構定義：

| 欄 | BigQuery 資料類型 | 說明 | 資料範例 |
| --- | --- | --- | --- |
| `aggregator_id` | `INTEGER` | 如果商家屬於 MCA，則為[多重客戶帳戶 (MCA)](https://support.google.com/merchants/answer/188487?hl=zh-tw) ID。否則為空值。 | 12345 |
| `merchant_id` | `INTEGER` | Google Merchant Center 帳戶 ID。這個欄位是主鍵。 | 1234 |
| `id` | `STRING` | 產品的 [Content API REST ID](https://developers.google.com/shopping-content/guides/products/product-id?hl=zh-tw)，格式為：`channel:content_language:feed_label:offer_id`，類似於在 [產品資料表結構定義](https://docs.cloud.google.com/bigquery/docs/merchant-center-products-schema?hl=zh-tw)中定義的方式。這個欄位是主鍵。 | online:en:AU:666840730 |
| `title` | `STRING` | 產品名稱。 | TN2351 黑色 USB |
| `brand` | `STRING` | 產品品牌。 | 品牌名稱 |
| `offer_id` | `STRING` | 商家提供的[產品 ID](https://support.google.com/merchants/answer/6324405?hl=zh-tw)。 | tddy123uk |
| `benchmark_price` | `RECORD` | 對於透過購物廣告宣傳特定產品的所有商家而言，該項產品的平均點擊加權價格。系統會依照[GTIN](https://support.google.com/merchants/answer/6324461?hl=zh-tw)比對產品。詳情請參閱[這篇說明中心文章，瞭解價格競爭力報表](https://support.google.com/merchants/answer/9626903?hl=zh-tw)。 |  |
| `benchmark_price.amount_micros` | `INTEGER` | 以微量單位表示的商品價格 (1 代表 1000000)。 | 1000000 |
| `benchmark_price.currency_code` | `STRING` | 商品價格的幣別。 | 美元 |
| `price` | `RECORD` | 產品價格。 |  |
| `price.amount_micros` | `STRING` | 以微量單位表示的商品價格 (1 代表 1000000)。 | 1000000 |
| `price.currency_code` | `INTEGER` | 商品價格的幣別。 | 美元 |
| `report_country_code` | `STRING` | 使用者在 Google 上執行查詢的國家/地區代碼。 | 瑞士、美國 |
| `product_type_l1` | `STRING` | 產品的[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l2` | `STRING` | 產品的[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l3` | `STRING` | 產品的[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l4` | `STRING` | 產品的[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l5` | `STRING` | 產品的[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `category_l1` | `STRING` | 產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。 | 動物與寵物用品 |
| `category_l2` | `STRING` | 產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。 | 寵物用品 |
| `category_l3` | `STRING` | 產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。 | 狗用品 |
| `category_l4` | `STRING` | 產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。 | 狗床墊 |
| `category_l5` | `STRING` | 產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。 |  |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]