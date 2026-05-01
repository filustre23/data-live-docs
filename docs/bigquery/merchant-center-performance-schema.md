* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 成效資料表

## 總覽

成效表包含可用來瞭解下列指標分布情況的資料欄：

* **點擊次數：**產品在 Google 上的點擊總數。系統只會計算產品詳細資料頁面的造訪次數。
* **曝光次數：**產品在 Google 服務中顯示的總次數。
  只有在消費者可以選擇是否前往你的產品詳細資料頁面時，系統才會計算曝光次數。如果產品沒有任何曝光次數，請確認該項產品是否已通過核准並等候數日，曝光次數可能就會出現。不過，如果曝光次數低於某個類別的最低門檻，則系統可能不會顯示這項資料，因此總數可能會與其他 Google 途徑中回報的數字不同。

請注意，系統最多可能會更新過去 3 天的成效資料，以便修正資料。差異通常不大。

選取 `Performance` 做為與轉移作業相關的報表之一時，系統會建立下列表格：

* `ProductPerformance_MERCHANT_ID`

## 結構定義

`ProductPerformance_` 資料表具有下列結構定義：

| **欄** | **BigQuery 資料類型** | **說明** | **資料範例** |
| --- | --- | --- | --- |
| `merchant_id` | `INTEGER` | Google Merchant Center 帳戶 ID。這個欄位是主鍵 | 1234 |
| `aggregator_id` | `INTEGER` | 如果 Merchant Center 帳戶 ID 由 MCA 管理，則為 [多重客戶帳戶 (MCA)](https://support.google.com/merchants/answer/188487?hl=zh-tw) 的 ID。否則為空值。 | 12345 |
| `offer_id` | `STRING` | 商家在互動發生時提供的[產品 ID](https://support.google.com/merchants/answer/6324405?hl=zh-tw)。這個欄位是主鍵。 | tddy123uk |
| `title` | `STRING` | 互動發生時的產品名稱。 | TN2351 黑色 USB |
| `brand` | `STRING` | 互動發生時的產品品牌。 | 品牌名稱 |
| `category_l1` | `STRING` | 互動發生時，產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。如未指定類別，請設為空白字串。 | 動物與寵物用品 |
| `category_l2` | `STRING` | 互動發生時，產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。如未指定類別，請設為空白字串。 | 寵物用品 |
| `category_l3` | `STRING` | 互動發生時，產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。如未指定類別，請設為空白字串。 | 狗用品 |
| `category_l4` | `STRING` | 互動發生時，產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。如未指定類別，請設為空白字串。 | 狗床墊 |
| `category_l5` | `STRING` | 互動發生時，產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。如未指定類別，請設為空白字串。 |  |
| `product_type_l1` | `STRING` | 發生互動時的產品[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l2` | `STRING` | 發生互動時的產品[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l3` | `STRING` | 發生互動時的產品[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l4` | `STRING` | 發生互動時的產品[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l5` | `STRING` | 發生互動時的產品[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `custom_label0` | `STRING` | 互動發生時，產品的[自訂標籤屬性](https://support.google.com/merchants/answer/6324473?hl=zh-tw)。 |  |
| `custom_label1` | `STRING` | 互動發生時，產品的[自訂標籤屬性](https://support.google.com/merchants/answer/6324473?hl=zh-tw)。 |  |
| `custom_label2` | `STRING` | 互動發生時，產品的[自訂標籤屬性](https://support.google.com/merchants/answer/6324473?hl=zh-tw)。 |  |
| `custom_label3` | `STRING` | 互動發生時，產品的[自訂標籤屬性](https://support.google.com/merchants/answer/6324473?hl=zh-tw)。 |  |
| `custom_label4` | `STRING` | 互動發生時，產品的[自訂標籤屬性](https://support.google.com/merchants/answer/6324473?hl=zh-tw)。 |  |
| `customer_country_code` | `STRING` | 點選或看到產品的客戶所在國家/地區。 | CH |
| `clicks` | `INTEGER` | 使用者在 Google 上點選你的產品，並前往產品詳細資料頁面的總點擊次數。 | 17 |
| `impressions` | `INTEGER` | 產品在 Google 服務中顯示的總次數。 只有在消費者可以選擇是否前往你的產品詳細資料頁面時，系統才會計算曝光次數。如果產品沒有任何曝光次數，請確認該項產品是否已通過核准並等候數日，曝光次數可能就會出現。 不過，如果曝光次數低於某個類別的最低門檻，則系統可能不會顯示這項資料，因此總數可能會與其他 Google 途徑中回報的數字不同。 | 601 |
| `destination` | `STRING` | 互動是否發生在購物廣告或免費產品資訊。 | 免費，廣告 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]