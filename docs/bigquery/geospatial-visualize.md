Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 視覺化呈現地理空間資料

地理空間分析功能可讓您使用下列項目，以視覺化方式呈現地理位置資料：

* [BigQuery Studio](#bigquery_studio)
* [數據分析](#data_studio)
* [BigQuery Geo Viz](#geo_viz)
* [Colab 筆記本](#colab)
* [Google Earth Engine](#google_earth)

## BigQuery Studio

BigQuery Studio 提供整合式地理區域資料檢視器。如果查詢結果包含一或多個 `GEOGRAPHY` 類型資料欄，您可以在互動式地圖中查看結果。如要查看地圖，請在「查詢結果」窗格中，按一下「視覺化」分頁標籤。

BigQuery 的視覺化功能非常適合快速檢查及反覆開發查詢。您可以透過視覺化方式確認資料是否符合預期、找出離群值，以及評估空間資料的正確性。此外，您也可以透過臨時分析探索結果，並從地理空間查詢中立即得出結論。

如要查看如何使用整合式地理檢視器的範例，請參閱「[開始使用地理空間分析功能](https://docs.cloud.google.com/bigquery/docs/geospatial-get-started?hl=zh-tw)」。

### BigQuery Studio 限制

* 一次只能呈現一個 `GEOGRAPHY` 資料欄。
* 效能取決於瀏覽器功能，不適用於算繪極大型或複雜的資料集。BigQuery 最多可算繪約一百萬個頂點、20,000 列或 128 MB 的結果。

## 數據分析

Data Studio 是 Google Marketing Platform 提供的免費自助式報表和資料視覺化服務，可連結至 BigQuery 和數百個其他資料來源。這項服務支援各種[地理欄位類型](https://support.google.com/looker-studio/answer/9843174?hl=zh-tw)，以及 BigQuery `GEOGRAPHY` 多邊形的[等值線圖](https://en.wikipedia.org/wiki/Choropleth_map)。透過[以 Google 地圖為基礎的視覺化功能](https://support.google.com/looker-studio/answer/9713352?hl=zh-tw)，您可以像使用 Google 地圖一樣，平移、縮放及進入街景服務，以視覺化方式呈現地理資料並與之互動。

如需在 Data Studio 中逐步瞭解地理空間分析，請參閱「[透過 Data Studio 將 BigQuery 多邊形資料視覺化](https://support.google.com/looker-studio/answer/10502383?hl=zh-tw)」。`GEOGRAPHY`

## BigQuery Geo Viz

BigQuery Geo Viz 是一個網頁工具，使用 Google Maps API 在 BigQuery 中顯示地理空間資料。您可以執行 SQL 查詢，並在互動式地圖上顯示結果。具備彈性的樣式功能，可用於分析及探索資料。

BigQuery Geo Viz 不是功能齊全的地理空間分析視覺化工具。Geo Viz 是一套簡便的工具，能夠以視覺化方式在地圖上呈現地理空間分析查詢結果 (每次顯示一筆查詢)。

如要查看使用 Geo Viz 呈現地理空間資料的範例，請參閱「[開始使用地理空間分析](https://docs.cloud.google.com/bigquery/docs/geospatial-get-started?hl=zh-tw)」。

如要探索 Geo Viz，請前往 Geo Viz 網頁版工具：

[前往 Geo Viz](https://bigquerygeoviz.appspot.com/?hl=zh-tw)

### Geo Viz 限制

* Geo Viz 支援以 `GEOGRAPHY` 資料欄形式擷取的幾何圖形輸入資料 (亦即點、線、多邊形)。您可以使用 BigQuery 的地理位置函式，將經緯度轉換為 `GEOGRAPHY`。
* Geo Viz 在地圖上顯示的結果數量會受到瀏覽器記憶體限制。您可以使用 `ST_Simplify` 函式降低解析度，並縮減查詢傳回的地理空間資料大小。
* 即時互動分析是由您的瀏覽器在本機環境中處理，實際的運作方式將視瀏覽器的功能而定。
* Geo Viz 僅支援與有權在相同 BigQuery 專案中執行查詢的使用者共用視覺化效果。
* Geo Viz 不支援下載視覺化資料供離線編輯用。

## Colab 筆記本

您也可以在 Colab 筆記本中執行地理空間視覺化。如需有關如何建構 Colab 筆記本來呈現資料圖表的教學課程，請參閱「[在 Colab 中以視覺化方式呈現 BigQuery 地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize-colab?hl=zh-tw)」。

如要查看及執行預先建構的筆記本，請參閱 GitHub 上的「[BigQuery geospatial visualization in Colab](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/notebooks/bigquery_geospatial_visualization.ipynb)」。

## Google Earth Engine

您也可以使用 Google Earth Engine 呈現地理空間資料。如要使用 Google Earth Engine，請將 BigQuery 資料匯出至 Cloud Storage，然後匯入 Google Earth Engine。您可以使用 Google Earth Engine 工具，將資料視覺化。

如要進一步瞭解使用 Google Earth Engine 的方法，請參閱：

* [Google Earth Engine 開發人員指南](https://developers.google.com/earth-engine/?hl=zh-tw)
* [Google Earth Engine API 教學課程](https://developers.google.com/earth-engine/tutorials?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]