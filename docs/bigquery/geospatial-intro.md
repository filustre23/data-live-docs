Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 地理空間分析簡介

在像 BigQuery 這樣的資料倉儲中，位置資訊非常常見，且可能影響重要的業務決策。您可以使用地理空間分析，透過 [`GEOGRAPHY` 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#geography_type)和 [GoogleSQL 地理函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)，分析及視覺化 BigQuery 中的地理空間資料。

舉例來說，您可以記錄一段時間內送貨車輛或包裹的經緯度。您也可以記錄顧客交易，並將資料與含有商店位置資料的其他表格合併。您可以使用這類位置資料執行下列操作：

* 預估包裹的送達時間。
* 判斷哪些顧客應收到特定商店地點的郵件。
* 結合資料與衛星圖像的樹木覆蓋率百分比，判斷是否適合使用空拍機配送。

## 限制

地理空間分析有下列限制：

* [地理位置函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)僅適用於 GoogleSQL。
* 目前只有 Python 專用的 BigQuery 用戶端程式庫支援 `GEOGRAPHY` 資料類型。如要使用其他用戶端程式庫，請透過 `ST_ASTEXT` 或 `ST_ASGEOJSON` 函式將 `GEOGRAPHY` 值轉換為字串。使用 `ST_ASTEXT` 轉換為文字只會儲存一個值，而轉換成 WKT 格式代表將資料標註為 `STRING` 類型，而非 `GEOGRAPHY` 類型。

## 配額

地理空間分析的配額與限制適用於您可對包含地理空間資料的資料表執行的各種工作類型，包括以下項目：

* [載入資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs) (載入工作)
* [匯出資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs) (擷取工作)
* [查詢資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs) (查詢工作)
* [複製資料表](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs) (複製工作)

如要進一步瞭解所有配額和限制，請參閱[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)一文。

## 定價

使用地理空間分析功能時，費用是依據下列要素來決定：

* 含有地理空間資料的資料表中所儲存的資料量
* 對資料執行的查詢作業

如需儲存空間價格的相關資訊，請參閱[儲存空間價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。

如需查詢價格的相關資訊，請參閱「[分析定價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)」。

許多資料表作業都是免費的，包括載入資料、複製資料表及匯出資料。雖然這些作業都是免費的，但仍受限於 BigQuery 的[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。如需所有免費作業的相關資訊，請參閱定價頁面上的「免費作業」一節。

## 後續步驟

* 如要開始使用地理空間分析，請參閱「[開始使用地理空間分析](https://docs.cloud.google.com/bigquery/docs/geospatial-get-started?hl=zh-tw)」。
* 如要進一步瞭解地理空間分析的視覺化選項，請參閱「[視覺化呈現地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize?hl=zh-tw)」。
* 如要進一步瞭解如何使用地理空間資料，請參閱「[使用地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw)」。
* 如要進一步瞭解如何使用光柵資料，請參閱「[使用光柵資料](https://docs.cloud.google.com/bigquery/docs/raster-data?hl=zh-tw)」。
* 如要進一步瞭解如何將 Google Earth Engine 地理空間資料併入 BigQuery，請參閱「[載入 Google Earth Engine 地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw#load-ee)」。
* 如要查看地理空間分析的 GoogleSQL 函式說明文件，請參閱[GoogleSQL 中的地理函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)。
* 如要瞭解不同的格線系統，請參閱「[空間分析的格線系統](https://docs.cloud.google.com/bigquery/docs/grid-systems-spatial-analysis?hl=zh-tw)」。
* 如要進一步瞭解地理空間資料集、地理空間分析和 AI，請參閱「[地理空間分析](https://docs.cloud.google.com/solutions/geospatial?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]