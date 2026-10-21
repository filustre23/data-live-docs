Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 商品目錄資料表

## 總覽

**注意：** 自 2025 年 9 月 1 日起，BigQuery 將不再支援匯出產品目錄資料表的報表。建議改用[新版暢銷商品報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-tw)。

暢銷商品資料可協助商家瞭解購物廣告和無付費產品資訊中最熱銷的品牌和產品。如要進一步瞭解暢銷商品，請參閱「[支援的報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-tw#supported_reports)」中的說明。

資料會寫入名為 `BestSellers_TopProducts_Inventory_MERCHANT_ID` 的資料表。

## 結構定義

`BestSellers_TopProducts_Inventory_` 資料表具有下列結構定義：

| **資料欄** | **BigQuery 資料類型** | **說明** |
| --- | --- | --- |
| `rank_id` | `STRING` | 要與「熱門產品」表格聯結的排名 ID |
| `product_id` | `STRING` | 內容 API 的產品 REST ID，格式為 `channel:content_language:feed_label:offer_id`。 |
| `merchant_Id` | `INTEGER` | 商家帳戶 ID。 |
| `aggregator_id` | `INTEGER` | 多重客戶帳戶的 Aggregator 帳戶 ID。 |

## 範例

下例說明 `BestSellers_TopProducts_Inventory_` 資料表如何為 `Products_` 資料表中的所有指定國家/地區提供產品對應。

**熱門產品**

| **product\_title** | **rank\_id:** | **ranking\_country** | **ranking\_category** | **rank** |
| --- | --- | --- | --- | --- |
| 後背包範例 | 2020-03-14:AU:5181:40:product | AU | 5181 | 40 |

**商品目錄資料表**

| **rank\_id** | **product\_id** |
| --- | --- |
| 2020-03-14:AU:5181:40:product | online:en:AU:666840730 |
| 2020-03-14:AU:5181:40:product | online:en:AU:666840730 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-15 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-15 (世界標準時間)。"],[],[]]