* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Comparison Shopping Service Center 資料表結構定義

當你將 Comparison Shopping Service (CSS) Center 報表資料移轉至 BigQuery 時，產品與產品問題資料的格式主要可對應至 Content API 中 [`ProductView`](https://developers.google.com/shopping-content/reference/rest/v2.1/reports/search?hl=zh-tw#productview) 和 [`Productstatuses`](https://developers.google.com/shopping-content/v2/reference/v2.1/productstatuses?hl=zh-tw) 資源的相關欄位格式。

## CSS Center 產品結構定義

下表列出 `Products_` 資料表的結構定義。部分欄位會以其他欄位的子集方式納入。例如，`Price` 欄位同時包含 `Value` 和 `Currency` 欄位。

| 欄位名稱 | 類型 | 說明 |
| --- | --- | --- |
| CSS ID | `INTEGER` | CSS ID |
| 商家 ID | `INTEGER` | 優惠擁有者的商家帳戶 ID |
| 產品 ID | `STRING` | 商品的專屬 ID |
| 動態饋給標籤 | `STRING` | 商品的動態饋給標籤，如果未提供則為「-」 |
| 語言代碼 | `STRING` | 商品的雙字母格式 ISO 639-1 語言編碼 |
| 管道 | `STRING` | 商品的通路，`online` 或 `local` |
| 標題 | `STRING` | 商品的標題 |
| 品牌 | `STRING` | 商品的品牌 |
| 類別 l{1-5} | `INTEGER` | 商品的 Google 產品類別 |
| 產品類型 l{1-5} | `STRING` | 商品的產品類型 |
| 價格 | `RECORD` | 商品未折扣前的全額價格 |
| 值 | `INTEGER` | 商品的價格 |
| 貨幣 | `STRING` | 價格的幣別 |
| 特價 | `RECORD` | 商品的特價 (如適用) |
| 值 | `INTEGER` | 商品的特價 |
| 貨幣 | `STRING` | 特價的幣別 |
| 條件 | `STRING` | 商品的狀況 |
| 可用性 | `STRING` | 商品的供應狀態 |
| 運送標籤 | `STRING` | 動態饋給中指定的運送標籤 |
| 全球交易品項識別碼 | `STRING` | 商品的[全球交易品項識別碼](https://support.google.com/merchants/answer/188494?hl=zh-tw#gtin) (GTIN) |
| 商品群組 ID | `STRING` | 同一產品所有型號的共用 ID |
| 建立時間 | `INTEGER` | 供應商建立此項目的時間，以微秒為單位的時間戳記 |
| 到期日 | `DATE` | 商品到期的日期 (於插播時指定) |
| 匯總報表內容狀態 | `STRING` | 所有報表情境匯總的產品狀態。支援的值為 `ELIGIBLE`、`ELIGIBLE_LIMITED`、`PENDING`、`NOT_ELIGIBLE_OR_DISAPPROVED`、`AGGREGATED_STATUS_UNSPECIFIED` |
| 報表內容狀態 | `RECORD`、`REPEATED` | 產品在各報表內容和區域中的狀態 |
| 報表內容 | `STRING` | 報表內容 |
| 區域和狀態 | `RECORD`、`REPEATED` | 各區域的狀態 |
| 區域 | `STRING` | 以 ISO 3166 格式表示的區域代碼 |
| 狀態 | `STRING` | 產品在該地區的狀態，可為 `ELIGIBLE`、`PENDING` 或 `DISAPPROVED` |
| 商品問題 | `RECORD`、`REPEATED` | 與產品相關聯的商品層級問題清單 |
| 類型 | `RECORD` | 問題類型 |
| 代碼 | `STRING` | 問題的錯誤代碼，相當於產品問題的 [`code`](https://developers.google.com/shopping-content/guides/product-issues?hl=zh-tw) |
| Canonical 屬性 | `STRING` | 屬性專屬問題的標準屬性名稱 |
| 嚴重性 | `RECORD` | 這個問題對優惠提供的影響程度 |
| 每個報表內容的嚴重程度 | `RECORD`、`REPEATED` | 每個報表內容的問題嚴重程度 |
| 報表內容 | `STRING` | 問題適用的報表內容 |
| 不通過審查的區域 | `STRING`、`REPEATED` | 報表內容中遭拒登的區域清單，以 ISO 3166 格式表示 |
| 已停售的地區 | `STRING`、`REPEATED` | 報表內容中降級的區域清單，以 ISO 3166 格式表示 |
| 匯總嚴重性 | `STRING` | 針對問題影響的所有報表內容，匯總問題的嚴重程度。其值可以是 `AGGREGATED_ISSUE_SEVERITY_UNSPECIFIED`、`DISAPPROVED`、`DEMOTED` 或 `PENDING` |
| 解析度 | `STRING` | 商家是否可解決這個問題 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]