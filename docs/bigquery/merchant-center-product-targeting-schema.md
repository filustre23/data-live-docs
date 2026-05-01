* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Merchant Center 產品指定目標資料表

## 總覽

產品指定目標資料可協助商家瞭解，在可存取的每個連結廣告主帳戶中，哪些購物和最高成效廣告活動會指定目標產品。

* 系統會考量所有廣告活動指定目標參數，例如[商家資訊群組](https://support.google.com/google-ads/answer/11596074?hl=zh-tw)、[產品群組](https://support.google.com/google-ads/answer/6275317?hl=zh-tw)和[動態饋給標籤](https://support.google.com/merchants/answer/14994087?hl=zh-tw)。
* 系統只會考慮含有有效廣告群組或素材資源群組的有效廣告活動。
* 為了計算 `targeting_status`，我們只會考量擁有 BigQuery 匯出檔案的使用者可存取的廣告客戶帳戶。詳情請參閱「[管理 Google Ads 帳戶存取權](https://support.google.com/google-ads/answer/6372672?hl=zh-tw)」。

## 資料表名稱

如果您在[設定 Google Merchant Center 移轉作業](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer-schedule-transfers?hl=zh-tw#set_up_a_google_merchant_center_transfer)時選擇「產品指定對象」報表選項，BigQuery 會在移轉期間為資料建立資料表。資料表名稱開頭為 `ProductTargeting_` 前置字元：

* 如果您使用個別商家 ID 設定轉移作業，資料表名稱為 `ProductTargeting_MERCHANT_ID`。
* 如果您使用 MCA 帳戶設定轉移作業，表格名稱為 `ProductTargeting_AGGREGATOR_ID`。

## 結構定義

產品指定目標資料表具有下列結構定義：

| 名稱 | 類型 | 說明 | 資料範例 |
| --- | --- | --- | --- |
| `product_id` | `STRING` | 產品的 Content API REST ID 格式為：`channel:content_language:feed_label:offer_id`。這個欄位是主鍵。 | online:en:AU:666840730 |
| `advertiser_id` | `INTEGER` | 廣告活動的廣告主 ID。這個欄位是主鍵。 | 4321 |
| `targeting_status` | `STRING` | 產品是否為廣告活動指定目標。   **注意：**Google Ads 廣告活動指定的產品可能不符合放送資格。如要確認產品是否符合資格，請使用[產品報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-products-schema?hl=zh-tw)的 `destinations.status` 欄位。 | TARGETED、NOT\_TARGETED |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]