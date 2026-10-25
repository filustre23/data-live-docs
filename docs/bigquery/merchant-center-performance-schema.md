Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 成效表格

## 總覽

成效表格包含多個資料欄，可用來瞭解下列指標的分佈情形：

* **點擊次數：**產品在 Google 獲得的點擊總數。只有產品詳細資料頁面的造訪次數會計入。
* **曝光次數：**產品在 Google 服務中顯示的總次數。
  只有在消費者可以選擇是否前往你的產品詳細資料頁面時，系統才會計算曝光次數。如果產品沒有任何曝光次數，請確認該產品已通過驗證，並等待幾天後再查看，屆時曝光次數應該就會出現。
  此外，如果曝光次數低於類別的最低門檻，系統可能不會顯示，因此總數可能與其他 Google 平台回報的資料不同。

請注意，成效資料最多可能更新至 3 天前，以反映修正後的資料。差異通常不大。

如果選取「`Performance`」做為與移轉作業相關的報表，系統會建立下列資料表：

* `ProductPerformance_MERCHANT_ID`

## 結構定義

`ProductPerformance_` 資料表包含下列結構定義：

| **資料欄** | **BigQuery 資料類型** | **說明** | **範例資料** |
| --- | --- | --- | --- |
| `merchant_id` | `INTEGER` | Google Merchant Center 帳戶 ID。這個欄位是主鍵 | 1234 |
| `aggregator_id` | `INTEGER` | 如果 Merchant Center 帳戶 ID 是由[多重客戶帳戶 (MCA)](https://support.google.com/merchants/answer/188487?hl=zh-tw) 管理，則為 MCA 的 ID。否則為空值。 | 12345 |
| `offer_id` | `STRING` | 互動發生時，商家提供的[產品 ID](https://support.google.com/merchants/answer/6324405?hl=zh-tw)。這個欄位是主鍵。 | tddy123uk |
| `title` | `STRING` | 互動發生時的產品名稱。 | TN2351 黑色 USB |
| `brand` | `STRING` | 互動發生時的產品品牌。 | 品牌名稱 |
| `category_l1` | `STRING` | 互動發生時，產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。如果沒有類別，請設為空白字串。 | 動物與寵物用品 |
| `category_l2` | `STRING` | 互動發生時，產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。如果沒有類別，請設為空白字串。 | 寵物用品 |
| `category_l3` | `STRING` | 互動發生時，產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。如果沒有類別，請設為空白字串。 | 狗用品 |
| `category_l4` | `STRING` | 互動發生時，產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。如果沒有類別，請設為空白字串。 | 狗床 |
| `category_l5` | `STRING` | 互動發生時，產品的 [Google 產品類別](https://support.google.com/merchants/answer/6324436?hl=zh-tw)。如果沒有類別，請設為空白字串。 |  |
| `product_type_l1` | `STRING` | 互動發生時，產品的[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l2` | `STRING` | 互動發生時，產品的[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l3` | `STRING` | 互動發生時，產品的[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l4` | `STRING` | 互動發生時，產品的[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `product_type_l5` | `STRING` | 互動發生時，產品的[產品類型屬性](https://support.google.com/merchants/answer/6324406?hl=zh-tw)。 |  |
| `custom_label0` | `STRING` | 互動發生時，產品的[自訂標籤屬性](https://support.google.com/merchants/answer/6324473?hl=zh-tw)。 |  |
| `custom_label1` | `STRING` | 互動發生時，產品的[自訂標籤屬性](https://support.google.com/merchants/answer/6324473?hl=zh-tw)。 |  |
| `custom_label2` | `STRING` | 互動發生時，產品的[自訂標籤屬性](https://support.google.com/merchants/answer/6324473?hl=zh-tw)。 |  |
| `custom_label3` | `STRING` | 互動發生時，產品的[自訂標籤屬性](https://support.google.com/merchants/answer/6324473?hl=zh-tw)。 |  |
| `custom_label4` | `STRING` | 互動發生時，產品的[自訂標籤屬性](https://support.google.com/merchants/answer/6324473?hl=zh-tw)。 |  |
| `customer_country_code` | `STRING` | 點擊或查看產品的顧客所在國家/地區。 | CH |
| `clicks` | `INTEGER` | 使用者在 Google 服務中點選你的產品，並前往產品詳細資料頁面的總點擊次數。 | 17 |
| `impressions` | `INTEGER` | 你的產品在 Google 服務中顯示的總次數。 只有在消費者可以選擇是否前往你的產品詳細資料頁面時，系統才會計算曝光次數。如果產品沒有任何曝光次數，請確認該產品已通過驗證，並等待幾天後再查看，屆時曝光次數應該就會出現。 此外，如果曝光次數低於類別的最低門檻，系統可能不會顯示，因此總數可能與其他 Google 平台回報的資料不同。 | 601 |
| `destination` | `STRING` | 互動式廣告的目的地，無論是購物廣告、免費產品資訊或 YouTube 聯盟。 | 免費、廣告、聯盟 |
| `network` | `STRING` | 指標適用的網路。 | SEARCH、SEARCH\_PARTNERS、CONTENT、YOUTUBE |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]