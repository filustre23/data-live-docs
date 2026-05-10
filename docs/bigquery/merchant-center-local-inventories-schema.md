Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 店面商品目錄資料表

## 總覽

商家可以利用店面商品目錄資料，將產品的店面商品目錄匯出至 BigQuery。這項資料包含產品的價格、供應情形和數量，以及取貨資訊和店內產品地點。

店面商品目錄資料的格式主要對應至 Content API [`localinventory`](https://developers.google.com/shopping-content/reference/rest/v2.1/localinventory?hl=zh-tw) 資源的相關欄位格式。

視您使用的 Merchant Center 帳戶類型而定，資料會寫入下列任一表格：

* 如果您使用的是個別商家 ID，資料會寫入 `LocalInventories_MERCHANT_ID` 表格。
* 如果您使用的是 MCA 帳戶，資料會寫入 `LocalInventories_AGGREGATOR_ID` 資料表。

## 結構定義

`LocalInventories_` 資料表具有下列結構定義：

| **欄** | **BigQuery 資料類型** | **說明** | **資料範例** |
| --- | --- | --- | --- |
| `product_id` | `STRING` | 產品的 Content API REST ID，格式為：`channel:content_language:feed_label:offer_id`。這個欄位是主鍵。 | online:en:AU:666840730 |
| `merchant_id` | `INTEGER` | 商家帳戶 ID。這個欄位是主鍵。 |  |
| `aggregator_id` | `INTEGER` | [多重客戶帳戶 (MCA)](https://support.google.com/merchants/answer/188487?hl=zh-tw) ID。 |  |
| `store_code` | `STRING` | 這個店面商品目錄資源的商店代碼。 |  |
| `price` | `RECORD` | 商品的當地價格。 |  |
| `price.value` | `NUMERIC` | 商品的當地價格。 | 99 |
| `price.currency` | `STRING` | 商品當地價格的幣別。 | 瑞士法郎 |
| `sale_price` | `RECORD` | 商品的當地特價。 |  |
| `sale_price.value` | `NUMERIC` | 商品的當地特價。 | 49 |
| `sale_price.currency` | `STRING` | 商品當地特價的幣別。 | 瑞士法郎 |
| `sale_price_effective_start_date` | `TIMESTAMP` | 商品特價的開始日期和時間。 | 2021-03-30 00:00:00 (世界標準時間) |
| `sale_price_effective_end_date` | `TIMESTAMP` | 商品特價的結束日期和時間。 | 2021-04-14 00:00:00 (世界標準時間) |
| `availability` | `STRING` | 商品在當地的供應情形。 | 缺貨 |
| `quantity` | `INTEGER` | 商品數量。 | 500 |
| `pickup_method` | `STRING` | 商品支援的取貨方式。 | ship\_to\_store [送貨到店] |
| `pickup_sla` | `STRING` | 從下單日期到商品可供取貨日期之間的預估時間。 | 三天 |
| `instore_product_location` | `STRING` | 商品在店內的位置。 |  |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]