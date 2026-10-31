Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 視覺化呈現地理空間資料

在 BigQuery 中以視覺化方式呈現地理空間資料，可確認資料是否一致、找出離群值，以及評估空間資訊的正確性。您可以使用下列工具，根據地理位置資料進行檢查並得出結論：

* [BigQuery Studio](#bigquery_studio)
* [數據分析](#data_studio)
* [BigQuery Geo Viz](#geo_viz)
* [Colab 筆記本](#colab)
* [Google Earth Engine](#google_earth)

## BigQuery Studio

BigQuery Studio 提供整合式地理資料檢視器。如果查詢結果包含一或多個 `GEOGRAPHY` 已指定類型和格式的欄，您可以在互動式地圖中查看結果。如要查看地圖，請在「查詢結果」窗格中，點選「圖表」分頁標籤。

BigQuery 的圖表功能非常適合用於快速檢查和反覆開發查詢。您可以透過視覺化方式確認資料是否符合預期、找出離群值，以及評估空間資料的正確性。此外，這項功能也適用於臨時分析，可探索結果並從地理空間查詢中立即得出結論。

如要查看如何使用整合式地理檢視器的範例，請參閱「[開始使用地理空間分析](https://docs.cloud.google.com/bigquery/docs/geospatial-get-started?hl=zh-tw)」。

### BigQuery Studio 限制

* 一次只能以圖表呈現一個`GEOGRAPHY`資料欄。
* 效能取決於瀏覽器功能，不適合用於算繪極大或複雜的資料集。BigQuery 最多可算繪約 100 萬個頂點、20,000 列或 128 MB 的結果。

## 數據分析

數據分析是 Google Marketing Platform 提供的免付費自助式報表和資料視覺化服務，可連結至 BigQuery 和其他數百個資料來源。這項服務支援多種[地理欄位類型](https://support.google.com/looker-studio/answer/9843174?hl=zh-tw)，以及 BigQuery `GEOGRAPHY` 多邊形的 [choropleth 地圖](https://en.wikipedia.org/wiki/Choropleth_map)。透過[以 Google 地圖為基礎的視覺化功能](https://support.google.com/looker-studio/answer/9713352?hl=zh-tw)，您可以像使用 Google 地圖一樣，以視覺化方式呈現地理資料並與其互動：平移、放大及切換至街景服務。

如需數據分析中地理空間分析的逐步操作說明，請參閱「[使用數據分析以圖表呈現 BigQuery `GEOGRAPHY` 多邊形](https://support.google.com/looker-studio/answer/10502383?hl=zh-tw)」。

## BigQuery Geo Viz

BigQuery Geo Viz 是一項網頁工具，可使用 Google Maps API 視覺化呈現 BigQuery 中的地理空間資料。您可以執行 SQL 查詢，並在互動式地圖上顯示結果。靈活的樣式功能可讓您分析及探索資料。

BigQuery Geo Viz 並非功能完整的地理空間數據分析視覺化工具。Geo Viz 是一種輕量級工具，可一次在地圖上以視覺化方式呈現一項地理空間分析查詢的結果。

如要查看使用 Geo Viz 視覺化地理空間資料的範例，請參閱「[開始使用地理空間分析](https://docs.cloud.google.com/bigquery/docs/geospatial-get-started?hl=zh-tw)」。

如要探索 Geo Viz，請前往 Geo Viz 網頁工具：

[前往 Geo Viz](https://bigquerygeoviz.appspot.com/?hl=zh-tw)

### Geo Viz 限制

* Geo Viz 支援以 `GEOGRAPHY` 資料欄形式擷取的幾何圖形輸入內容 (點、線和多邊形)。您可以使用 BigQuery 的地理函式，將經緯度轉換為 `GEOGRAPHY`。
* Geo Viz 可在地圖上顯示的結果數量受限於瀏覽器記憶體。您可以使用 `ST_Simplify` 函式，降低查詢傳回的地理空間資料解析度和大小。
* 即時互動分析是由您的瀏覽器在本機環境中處理，實際的運作方式將視瀏覽器的功能而定。
* Geo Viz 僅支援與有權在相同 BigQuery 專案中執行查詢的使用者共用圖表。
* Geo Viz 不支援下載圖表進行離線編輯。

## Colab 筆記本

您也可以在 Colab 筆記本中執行地理空間視覺化。如需建構 Colab 筆記本以視覺化呈現資料的教學課程，請參閱「[在 Colab 中以視覺化方式呈現 BigQuery 地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize-colab?hl=zh-tw)」。

如要查看及執行預先建構的筆記本，請參閱 GitHub 中的 [Colab 中的 BigQuery 地理空間視覺化](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/notebooks/bigquery_geospatial_visualization.ipynb)。

## Google Earth Engine

您也可以使用 Google Earth Engine，以視覺化方式呈現地理空間資料。如要使用 Google Earth Engine，請將 BigQuery 資料匯出至 Cloud Storage，然後匯入 Google Earth Engine。您可以使用 Google Earth Engine 工具，以圖表呈現資料。

如要進一步瞭解使用 Google Earth Engine 的方法，請參閱：

* [Google Earth Engine 開發人員指南](https://developers.google.com/earth-engine/?hl=zh-tw)
* [Google Earth Engine API 教學課程](https://developers.google.com/earth-engine/tutorials?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-30 (世界標準時間)。"],[],[]]