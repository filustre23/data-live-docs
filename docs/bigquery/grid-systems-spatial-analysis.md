Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 空間分析格線系統

[S2](http://s2geometry.io/) 和 [H3](https://h3geo.org/) 等地理空間網格系統可將空間資料整理成標準化地理區域，以便進行分析。選擇合適的多解析度格線系統，即可可靠地匯總資料、比較局部區域，並追蹤一段時間內的變化，不必依賴不一致的行政邊界。

## 空間分析總覽和使用難題

空間分析有助於呈現實體空間中實體 (商店或房屋) 與事件之間的關係。以地球表面做為實體空間的空間分析，稱為[地理空間分析](https://docs.cloud.google.com/bigquery/docs/geospatial-intro?hl=zh-tw)。BigQuery 包含地理空間功能和函式，可讓您大規模執行地理空間分析。

許多地理空間用途涉及匯總局部區域內的資料，並比較這些區域的統計匯總資料。這些本地化區域在[空間資料庫資料表](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw)中以多邊形表示。在某些情況下，這種方法稱為「統計地理」。為了改善報表、分析和[空間索引](https://cloud.google.com/blog/products/data-analytics/best-practices-for-spatial-clustering-in-bigquery?hl=zh-tw)，必須標準化地理區域範圍的判斷方法。舉例來說，零售商可能想分析店面所在區域或考慮開設新店的區域，瞭解人口特徵隨時間的變化。或者，保險公司可能想分析特定區域的常見天然災害風險，進一步瞭解財產風險。

許多地區都有嚴格的資料隱私權法規，因此包含位置資訊的資料集必須[去識別化或部分匿名化](https://docs.cloud.google.com/sensitive-data-protection/docs/deidentify-sensitive-data?hl=zh-tw)，以保護資料中個人的隱私。舉例來說，您可能需要對包含未償房貸資料的資料集，進行地理信用集中風險分析。如要對資料集進行去識別化，使其符合法規遵循分析，您需要保留房地產位置的相關資訊，但避免使用特定地址或經緯度座標。

在上述範例中，這些分析的設計人員面臨下列挑戰：

* 如何繪製區域邊界，分析該區域隨時間的變化？
* 如何使用現有的行政界線，例如人口普查區或多解析度格線系統？

本文將說明各個選項、介紹最佳做法，並協助您避免常見錯誤，藉此解答這些問題。

## 選擇統計區域時常犯的錯誤

房地產銷售、行銷廣告活動、電子商務出貨和保險單等業務資料集，都適合進行空間分析。這些資料集通常包含看似方便的空間彙整鍵，例如普查區、郵遞區號或城市名稱。包含人口普查區、郵遞區號和城市表示法的公開資料集隨手可得，因此很適合用做統計匯總的行政界線。

雖然這些和其他行政邊界名義上很方便，但也有缺點。此外，這些界線在數據分析專案的早期階段可能運作良好，但在後期階段可能會出現缺點。

### 郵遞區號

世界各國都使用郵遞區號來轉送郵件，因此在空間和非空間資料集中，郵遞區號通常用於參照位置和區域。以上述房貸範例來說，資料集通常需要去識別化，才能進行下游分析。由於每個房產地址都包含郵遞區號，因此可以存取郵遞區號參考資料表，方便您選擇空間分析的彙整鍵。

使用郵遞區號的缺點是，郵遞區號並非以多邊形表示，而且沒有單一正確的郵遞區號區域資料來源。此外，郵遞區號[無法準確反映實際的人類行為](https://carto.com/blog/zip-codes-spatial-analysis)。美國最常用的郵遞區號資料來自[美國人口普查局 TIGER/Line Shapefile](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)，其中包含名為 [ZCTA5 (郵遞區號統計區)](https://catalog.data.gov/dataset/tiger-line-shapefile-2019-2010-nation-u-s-2010-census-5-digit-zip-code-tabulation-area-zcta5-na) 的資料集。這個資料集代表根據郵件遞送路線得出的郵遞區號邊界近似值。不過，有些代表個別建築物的郵遞區號完全沒有邊界。其他國家/地區也存在這個問題，因此難以形成單一全球事實資料表，其中包含一組權威性的郵遞區號邊界，可用於跨系統和跨資料集。

此外，全球各地使用的郵遞區號格式不盡相同。
有些是三到十位數的數字，有些則是英數字元。
此外，國家/地區之間也有重疊，因此必須將原產地與郵遞區號儲存在不同的資料欄中。有些國家/地區不使用郵遞區號，這會使分析更加複雜。

### 人口普查區、城市和郡

有些行政單位 (例如人口普查區、城市和郡) 不會受到缺乏權威邊界的影響。舉例來說，城市邊界在大多數情況下都是由政府機關明確界定。美國人口普查局和大多數其他國家/地區的類似機構，都對人口普查區有明確定義。

使用這些和其他行政邊界的缺點是，它們會隨著時間變化，且彼此在地理上不一致。縣市會合併或拆分，有時也會重新命名。美國每十年會更新一次普查區，其他國家/地區則會在不同時間更新。令人困惑的是，在某些情況下，地理邊界可能會改變，但其專屬 ID 仍保持不變，因此難以分析及瞭解一段時間內的變化。

某些行政區界線的另一個常見缺點，是這些區域各自獨立，沒有地理階層。除了比較個別區域外，常見的需求是比較區域本身的匯總資料與其他匯總資料。舉例來說，零售商在實作[赫夫模型](https://en.wikipedia.org/wiki/Huff_model)時，可能會想使用多個距離執行這項分析，而這些距離可能與業務其他部分使用的行政區不對應。

## 單一和多解析度格線

單一解析度格線由離散單位組成，與包含這些單位的較大區域沒有地理關係。舉例來說，郵遞區號與較大行政單位 (例如可能包含郵遞區號的城市或郡) 的邊界，地理關係不一致。進行空間分析時，必須瞭解不同區域之間的關係，但不需要深入瞭解定義區域多邊形的歷史和法規。

多解析度格線有時稱為階層式格線，因為每個縮放等級的儲存格都會在較高的縮放等級細分為較小的儲存格。多解析度格線是由定義明確的單位階層組成，這些單位包含在較大的單位中。舉例來說，普查區包含區塊群組，而區塊群組又包含區塊。這種一致的階層關係有助於統計匯總。舉例來說，您可以計算普查區內所有區塊群組的平均收入，藉此顯示該普查區的平均收入。郵遞區號無法做到這一點，因為所有郵遞區號區域都位於單一解析度。由於沒有標準化的方式來定義鄰近性，或比較不同國家/地區的收入，因此很難比較某個區域與周圍區域的收入。

## S2 和 H3 格線系統

本節將概略介紹 S2 和 H3 格線系統。

### S2

[S2 幾何圖形](http://s2geometry.io/)是 Google 開發的開放原始碼階層式格線系統，於 2011 年公開發布。您可以使用 S2 格線系統，為每個儲存格指派不重複的 64 位元整數，藉此整理及建立空間資料索引。解析度分為 31 個等級。每個儲存格都以正方形表示，專為球形幾何圖形 (有時稱為[*地理區域*](https://postgis.net/workshops/postgis-intro/geography.html)) 的作業而設計。每個正方形會再細分為四個較小的正方形。鄰近遍歷是指識別鄰近 S2 儲存格的能力，但由於正方形可能會有四個或八個相關鄰近儲存格 (視分析類型而定)，因此定義較不明確。以下是多解析度 S2 網格儲存格的範例：

BigQuery 使用 S2 儲存格為空間資料建立索引，並提供多項函式。例如，[`S2_CELLIDFROMPOINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#s2_cellidfrompoint) 會傳回 S2 儲存格 ID，其中包含地球表面上指定層級的點。

### H3

[H3](https://www.uber.com/en-IN/blog/h3/) 是 Uber 開發的開放原始碼階層式格線系統，由 Overture Maps 使用。解析度共有 16 個等級。每個儲存格都以六邊形表示，且與 S2 一樣，每個儲存格都會指派不重複的 64 位元整數。在[墨西哥灣 H3 單元視覺化](https://h3geo.org/docs/core-library/restable/)範例中，較小的 H3 單元並未完全包含在較大的單元中。

每個儲存格會再細分為七個較小的六邊形。雖然細分結果不完全精確，但足以應付許多用途。每個儲存格都與六個相鄰儲存格共用一條邊，因此更容易遍歷相鄰儲存格。舉例來說，每個層級都有 [12 個五邊形](https://h3geo.org/docs/api/inspection/#h3ispentagon)，這些五邊形與五個相鄰的五邊形共用一條邊，而不是六個。雖然 BigQuery 不支援 H3，但您可以使用 [Carto Analytics Toolbox for BigQuery](https://carto.com/blog/spatial-functions-bigquery-uber)，在 BigQuery 中新增 H3 支援。

雖然 S2 和 H3 程式庫都是開放原始碼，並依據[Apache 2 授權](https://www.apache.org/licenses/LICENSE-2.0)提供，但 H3 程式庫的文件更為詳細。

## HEALPix

另一種將球體網格化的配置，通常用於天文學領域，稱為階層式等面積等緯度像素化 (HEALPix)。[HEALPix](https://healpix.jpl.nasa.gov/index.shtml) 與階層式像素深度無關，但運算時間維持不變。

HEALPix 是球體的階層式等面積像素化配置。用於呈現及分析天球 (或其他球體) 上的資料。除了運算時間固定外，HEALPix 格線還具有下列特性：

* 網格儲存格具有階層結構，會維持上下層關係。
* 在特定階層中，儲存格的面積相等。
* 這些單元格遵循[*等緯度*](https://healpix.jpl.nasa.gov/html/intronode4.htm)分布，可提高光譜法的效能。

BigQuery 不支援 HEALPix，但有許多語言 (包括 [JavaScript](https://github.com/michitaro/healpix)) 都有多種實作方式，因此可以方便地在 BigQuery user-defined function (UDF) 中使用。

## 各項索引策略的應用實例

本節提供一些範例，協助您評估最適合您用途的格線系統。

許多數據分析和報表用途都涉及視覺化，無論是分析本身的一部分，還是向業務利害關係人製作報表。這些視覺化圖表通常會以[網路麥卡托](https://en.wikipedia.org/wiki/Web_Mercator_projection)呈現，這是 Google 地圖和許多其他網路地圖應用程式使用的平面投影。在視覺化扮演重要角色的情況下，H3 儲存格可提供主觀上更佳的視覺化體驗。S2 儲存格 (尤其是在較高緯度) 往往比 H3 儲存格更扭曲，且在平面投影中呈現時，與較低緯度的儲存格不一致。

在分析中，鄰近比較扮演重要角色，而 H3 儲存格可簡化實作。舉例來說，比較城市各區域的分析結果，有助於決定適合開設新零售商店或配送中心的地點。分析時，必須對指定儲存格的屬性執行統計計算，並與相鄰儲存格比較。

S2 儲存格在全域性質的分析中效果較佳，例如涉及距離和角度測量的分析。Niantic 的《Pokémon GO》利用 S2 儲存格決定遊戲資產的放置位置和分布方式。S2 儲存格的精確細分屬性可確保遊戲資產能平均分布在全球各地。

## 後續步驟

* 如需空間分群的最佳做法，請參閱「[BigQuery 空間分群：最佳做法](https://cloud.google.com/blog/products/data-analytics/best-practices-for-spatial-clustering-in-bigquery?hl=zh-tw)」。
* 瞭解如何[根據不完整的資料建立空間階層](https://mentin.medium.com/creating-spatial-hierarchy-2ba5488eac0a)。
* 瞭解 [GitHub 上的 S2 幾何圖形](https://github.com/google/s2geometry)。
* 瞭解 [GitHub 上的 H3 幾何圖形](https://github.com/uber/h3)。
* 查看[使用 H3、BigQuery 和 Earth Engine 的範例](https://github.com/Prindle19/ee_python_esg_intro/blob/main/01%20-%20Dataframes%20and%20Zonal%20Statistics.ipynb)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-30 (世界標準時間)。"],[],[]]