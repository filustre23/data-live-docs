* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 價格深入分析資料表

## 總覽

價格分析報表會顯示產品的建議特價，並預測產品價格更新後的預期成效。你可以使用價格分析報表，更有效地設定產品價格。這份報表與 [Google Merchant Center 的價格分析報表](https://support.google.com/merchants/answer/11916926?hl=zh-tw)類似。

如果您使用個別商家 ID，資料會寫入名為 `PriceInsights_MERCHANT_ID` 的資料表；如果您使用 MCA 帳戶，資料會寫入名為 `PriceInsights_AGGREGATOR_ID` 的資料表。

## 結構定義

`PriceInsights_` 資料表具有下列結構定義：

| 欄 | BigQuery 資料類型 | 說明 | 資料範例 |
| --- | --- | --- | --- |
| `aggregator_id` | `INTEGER` | 如果商家屬於 MCA，請提供多重客戶帳戶 (MCA) ID。否則為空值。 | 12345 |
| `merchant_id` | `INTEGER` | Google Merchant Center 帳戶 ID。這個欄位是主鍵。 | 1234 |
| `id` | `STRING` | 產品的 Content API REST ID，格式為：`channel:content_language:feed_label:offer_id`，類似於[產品資料表結構定義](https://docs.cloud.google.com/bigquery/docs/merchant-center-products-schema?hl=zh-tw)中定義的方式。這個欄位是主鍵。 | online:en:AU:666840730 |
| `title` | `STRING` | 產品名稱。 | TN2351 黑色 USB |
| `brand` | `STRING` | 產品品牌。 | 品牌名稱 |
| `offer_id` | `STRING` | 商家提供的[產品 ID](https://support.google.com/merchants/answer/6324405?hl=zh-tw)。 | tddy123uk |
| `price` | `RECORD` | 產品目前的價格。 | 1 美元 = `amount_micros: 1000000 currency_code: USD` |
| `suggested_price` | `RECORD` | Google 預估的特價或折扣價格，可為貴商家賺取最高毛利。系統會透過複雜的模型，模擬產品在過去 7 天內採用不同價格點的成效，推估出建議特價。  為了計算建議價格，我們會將你目前的價格，與類似商家銷售的相同產品價格做比較。此外，這個模型也會考量產品需求、販售類似產品的賣方數量，以及類似商家的預估利潤率等，並在分析過後，推算出採用建議價格後的預期曝光次數、點擊次數、轉換次數和毛利。  雖然建議價格可提供寶貴的深入分析資料，但不保證未來成效。 | 1 美元 = `amount_micros: 1000000 currency_code: USD` |
| `predicted_impressions_change_fraction` | `FLOAT` | 套用建議特價後，預估曝光次數會有所增加。系統的模型會使用過去 7 天的成效資料來產生預測結果。 |  |
| `predicted_clicks_change_fraction` | `FLOAT` | 套用建議特價後，點擊次數預計將有所增加。系統的模型會使用過去 7 天的成效資料來產生預測結果。 |  |
| `predicted_conversions_change_fraction` | `FLOAT` | 套用建議特價後，轉換次數預計將有所增加。系統的模型會使用過去 7 天的成效資料來產生預測結果。 |  |
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

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]