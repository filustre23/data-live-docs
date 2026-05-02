* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 區域性商品目錄資料表

## 總覽

區域商品目錄表會向商家顯示產品的區域供應情形和價格覆寫值。區域商品目錄資料的格式主要對應至 Content API [`regionalinventory`](https://developers.google.com/shopping-content/reference/rest/v2.1/regionalinventory?hl=zh-tw) 資源的相關欄位格式。

如果您使用個別商家 ID，資料會寫入名為 `RegionalInventories_MERCHANT_ID` 的資料表；如果您使用 MCA 帳戶，資料會寫入 `RegionalInventories_AGGREGATOR_ID`。

## 結構定義

`RegionalInventories_` 資料表具有下列結構定義：

| **欄** | **BigQuery 資料類型** | **說明** | **資料範例** |
| --- | --- | --- | --- |
| `product_id` | `STRING` | 產品的 Content API REST ID，格式為：`channel:content_language:feed_label:offer_id`。這個欄位是主鍵。 | online:en:AU:666840730 |
| `merchant_id` | `INTEGER` | 商家帳戶 ID。這個欄位是主鍵。 |  |
| `aggregator_id` | `INTEGER` | 多重客戶帳戶的 Aggregator 帳戶 ID。 |  |
| `region_id` | `STRING` | 商品目錄的區域 ID。 |  |
| `price` | `RECORD` | 商品的區域價格。 |  |
| `price.value` | `NUMERIC` | 商品的區域價格。 | 99 |
| `price.currency` | `STRING` | 商品區域價格的幣別。 | 瑞士法郎 |
| `sale_price` | `RECORD` | 商品的區域特價。 |  |
| `sale_price.value` | `NUMERIC` | 商品的區域特價。 | 49 |
| `sale_price.currency` | `STRING` | 商品區域特價的幣別。 | 瑞士法郎 |
| `sale_price_effective_start_date` | `TIMESTAMP` | 商品在該地區特價的開始日期和時間。 | 2021-03-30 00:00:00 (世界標準時間) |
| `sale_price_effective_end_date` | `TIMESTAMP` | 商品在該地區特價的結束日期和時間。 | 2021-04-14 00:00:00 (世界標準時間) |
| `availability` | `STRING` | 商品的地區供應情形狀態。 | 缺貨 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]