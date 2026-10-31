Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 空間分析的最佳做法

在 BigQuery 分析複雜的地理空間特徵時，資料集可能包含大量多邊形、多邊形集合和 LineString，用來代表複雜特徵，例如道路、地塊和洪水區。每個形狀可包含數千個點。在 BigQuery 的大多數空間運算中 (例如交集和距離計算)，基礎演算法通常會造訪每個形狀中的大部分點，以產生結果。在某些作業中，演算法會造訪所有點。

處理含有數千個點的形狀，可能會大幅增加查詢費用和時間。如要最佳化地理空間查詢效能並縮短延遲時間，您可以對資料集套用特定的空間分析最佳做法。

本文假設您的 BigQuery 地理空間資料表[已依地理資料欄分群](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw#partitioning_and_clustering_geospatial_data)。

## 簡化形狀

**最佳做法：**使用簡化和貼齊格線功能，將原始資料集的簡化版本儲存為 materialized view。

許多具有大量點的複雜形狀都可以簡化，而不會大幅降低精確度。您可以單獨或合併使用 BigQuery [`ST_SIMPLIFY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_simplify) 和 [`ST_SNAPTOGRID`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_snaptogrid) 函式，減少複雜形狀中的點數。將這些函式與 BigQuery [materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw) 結合，即可將原始資料集的簡化版本儲存為 materialized view，並根據基礎資料表自動保持最新狀態。

在下列用途中，簡化形狀最能有效改善資料集的成本和效能：

* 您必須維持與真實形狀的高度相似性。
* 您必須執行高精確度、高準確度的作業。
* 您想加快視覺化速度，同時不影響形狀細節。

下列程式碼範例說明如何對具有 `GEOGRAPHY` 資料欄 (名為 `geom`) 的基礎資料表使用 `ST_SIMPLIFY` 函式。程式碼會簡化形狀並移除點，但不會干擾形狀的任何邊緣，超過 1.0 公尺的容許值。

```
CREATE MATERIALIZED VIEW project.dataset.base_mv
  CLUSTER BY geom
AS (
  SELECT
    * EXCEPT (geom),
    ST_SIMPLIFY(geom, 1.0) AS geom
  FROM base_table
)
```

以下程式碼範例說明如何使用 `ST_SNAPTOGRID` 函式，將點貼齊解析度為 0.00001 度的格線：

```
CREATE MATERIALIZED VIEW project.dataset.base_mv
  CLUSTER BY geom
AS (
  SELECT
    * EXCEPT (geom),
    ST_SNAPTOGRID(geom, -5) AS geom
  FROM base_table
)
```

這個函式中的 `grid_size` 引數是做為指數，也就是 10e-5 = 0.00001。在最糟的情況下 (發生在赤道)，這個解析度相當於約 1 公尺。

建立這些檢視表後，請使用與查詢基礎資料表相同的查詢語意，查詢 `base_mv` 檢視表。您可以運用這項技術，快速找出需要深入分析的一組形狀，然後對基礎資料表執行第二次更深入的分析。測試查詢，看看哪些門檻值最適合您的資料。

**注意：** `ST_SIMPLIFY` 函式會保留輸入形狀的拓撲，避免過度簡化。

如果是評估用途，請判斷用途所需的準確度。使用 `ST_SIMPLIFY` 函式時，請將 `threshold_meters` 參數設為所需的精確度。如要測量城市或更大範圍的距離，請將門檻設為 10 公尺。如果是較小的範圍 (例如測量建築物與最近水域之間的距離)，建議使用較小的門檻 (1 公尺以下)。使用較小的門檻值，會從指定形狀中移除較少的點。

透過網路服務提供地圖圖層時，您可以使用 [bigquery-geotools 專案](https://github.com/GoogleCloudPlatform/bigquery-geotools)，預先計算不同縮放等級的 materialized view。這項專案是 Geoserver 的驅動程式，可讓您透過 BigQuery 提供空間圖層。這個驅動程式會建立多個具有不同 `ST_SIMPLIFY` 門檻參數的 materialized view，以便在較高的縮放等級提供較少細節。

## 使用點和矩形

**最佳做法：**將形狀縮減為點或矩形，代表其位置。

您可以將形狀縮減為單一點或矩形，提高查詢效能。本節中的方法無法準確呈現形狀的細節和比例，但能以最佳方式呈現形狀的位置。

您可以使用形狀的地理中心點 (*群集中心*) 代表整個形狀的位置。使用包含形狀的矩形建立形狀的*範圍*，可用於表示形狀的位置，並保留其相對大小的資訊。

當您需要測量兩點之間的距離 (例如兩個城市之間) 時，使用點和矩形最能有效改善資料集的成本和效能。

舉例來說，假設您將美國土地地塊的資料庫載入 BigQuery 資料表，然後判斷最近的水體。在這種情況下，使用 [`ST_CENTROID`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_centroid) 函式預先計算地塊群集中心，並搭配本文「[簡化形狀](#simplify-shapes)」一節所述的方法，可減少使用 [`ST_DISTANCE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_distance) 或 [`ST_DWITHIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_dwithin) 函式時執行的比較次數。使用 `ST_CENTROID` 函式時，計算時必須考量地塊中心。以這種方式預先計算地塊群集中心，也能減少成效變異，因為不同地塊形狀可能包含不同數量的點。

這個方法的變體是使用 [`ST_BOUNDINGBOX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_boundingbox) 函式，而非 `ST_CENTROID` 函式，來計算輸入形狀周圍的矩形包絡。雖然這種做法不如使用單一錨點有效率，但可以減少特定極端情況的發生。這個變化版本仍可提供良好且一致的效能，因為 `ST_BOUNDINGBOX` 函式的輸出內容一律只包含四個需要考量的點。定界框結果的類型為 [`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)，這表示您必須手動計算距離，或使用本文稍後介紹的[向量索引方法](#use-vector-search-and-vector-indexes)。

## 使用船體

**最佳做法：**使用凸包，以最佳方式呈現形狀的位置。

想像一下，如果將形狀收縮包裝，並計算收縮包裝的邊界，該邊界就稱為「殼層」。在凸包中，所得形狀的所有角度都是凸角。與形狀範圍一樣，凸包會保留一些有關基礎形狀相對大小和比例的資訊。不過，使用凸包的代價是，在後續分析中需要儲存及考量更多點。

您可以使用 [`ST_CONVEXHULL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_convexhull) 函式，以最佳方式表示形狀的位置。使用這個函式可提高準確度，但會降低效能。`ST_CONVEXHULL` 函式與 [`ST_EXTENT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_extent) 函式類似，但輸出形狀包含更多點，且點數會根據輸入形狀的複雜度而有所不同。雖然對於非複雜形狀的小型資料集，效能優勢可能微不足道，但對於具有大型和複雜形狀的大型資料集，`ST_CONVEXHULL` 函式可在成本、效能和準確度之間取得良好平衡。

## 使用格線系統

**最佳做法：**使用地理空間格線系統比較區域。

如果您的用途涉及匯總本地化區域內的資料，並比較這些區域的統計匯總資料，則可利用標準化格線系統比較不同區域。

舉例來說，零售商可能想分析商店所在地或考慮開設新店的地區，人口統計資料隨時間變化的情況。或者，保險公司可能想分析特定區域的常見自然災害風險，進一步瞭解財產風險。

使用 [S2 和 H3 等標準格線系統](https://docs.cloud.google.com/bigquery/docs/grid-systems-spatial-analysis?hl=zh-tw#s2_and_h3_grid_systems)，可加快這類統計匯總和空間分析的速度。使用這些網格系統也能簡化數據分析的開發作業，並提高開發效率。

舉例來說，使用美國[人口普查區](https://en.wikipedia.org/wiki/Census_tract)進行比較時，會因大小不一致而產生問題，因此必須套用校正係數，才能在人口普查區之間進行同類比較。此外，普查區和其他行政邊界會隨著時間而改變，需要花費心力修正這些變更。使用網格系統進行空間分析，可以解決這類問題。

## 使用向量搜尋和向量索引

**最佳做法：**使用向量搜尋和向量索引，進行最鄰近地理空間查詢。

[BigQuery 推出](https://cloud.google.com/blog/products/data-analytics/introducing-new-vector-search-capabilities-in-bigquery?hl=zh-tw)向量搜尋功能，可支援語意搜尋、相似度偵測和檢索增強生成等機器學習用途。要實現這些用途，關鍵在於一種稱為[近似最鄰近搜尋](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximation_methods)的索引方法。您可以使用[向量搜尋](https://docs.cloud.google.com/bigquery/docs/vector-search-intro?hl=zh-tw)，比較代表空間中點的向量，加快及簡化最鄰近地理空間查詢。

您可以使用向量搜尋，依半徑搜尋特徵。首先，請設定搜尋半徑。您可以在最近鄰搜尋的結果集中，找出最佳半徑。設定半徑後，請使用 [`ST_DWITHIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_dwithin) 函式找出附近的地圖項目。

舉例來說，假設您已知某棟建築物的位置，並想找出距離該建築物最近的十棟建築物。您可以將每棟建築物的群集中心儲存為新資料表中的向量，為資料表建立索引，然後使用向量搜尋功能進行搜尋。

在本例中，您也可以使用 BigQuery 中的 Overture Maps 資料，建立與感興趣區域和名為 `geom_vector` 的向量相對應的建築物形狀資料表。本例中的感興趣區域是美國維吉尼亞州諾福克市，以 [FIPS 代碼](https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code) 51710 表示，如以下程式碼範例所示：

```
CREATE TABLE vector_search.norfolk_buildings
AS (
  SELECT
    *,
    [
      ST_X(ST_CENTROID(building.geometry)),
      ST_Y(ST_CENTROID(building.geometry))] AS geom_vector
  FROM `bigquery-public-data.overture_maps.building` AS building
  INNER JOIN `bigquery-public-data.geo_us_boundaries.counties` AS county
    ON (st_intersects(county.county_geom, building.geometry))
  WHERE county.county_fips_code = '51710'
)
```

下列程式碼範例說明如何在資料表建立向量索引：

```
CREATE
  vector index building_vector_index
ON
  vector_search.norfolk_buildings(geom_vector)
  OPTIONS (index_type = 'IVF')
```

這項查詢會找出距離特定錨定建築物最近的 10 棟建築物：

```
SELECT base.*
FROM
  VECTOR_SEARCH(
    TABLE vector_search.norfolk_buildings,
    'geom_vector',
    (
      SELECT
        geom_vector
      FROM
        vector_search.norfolk_buildings
      WHERE id = '56873794-9873-4fe1-871a-5987bb3a0efb'
    ),
    top_k => 10,
    distance_type => 'EUCLIDEAN',
    options => '{"fraction_lists_to_search":0.1}')
```

**注意：** 您可能需要調整部分參數 (例如 `top_k` 和 `fraction_lists_to_search`)，才能處理特定資料。

在「查詢結果」窗格中，點選「圖表」分頁標籤。地圖會顯示最靠近錨定建築物的一組建築物形狀：

在 Google Cloud 控制台執行這項查詢時，請按一下「Job Information」(工作資訊)，確認「Vector Index Usage Mode」(向量索引使用模式) 設為 `FULLY_USED`。這表示查詢使用的是您稍早建立的 `building_vector_index` 向量索引。

**注意：** 由於這項向量搜尋使用歐幾里得距離，因此結果可能與直接使用 `ST_DISTANCE` 函式不同，尤其是在比較長距離時，地球曲率會開始產生較大影響。

## 分割大型圖案

**最佳做法：**使用 `ST_SUBDIVIDE` 函式分割大型形狀。

使用 `ST_SUBDIVIDE` 函式，[將大型形狀或長線字串拆分為較小的形狀](https://mentin.medium.com/subdivide-and-conquer-any-geometry-ca4f0a4b8491)。

## 後續步驟

* 瞭解如何[使用格線系統進行空間分析](https://docs.cloud.google.com/bigquery/docs/grid-systems-spatial-analysis?hl=zh-tw)。
* 進一步瞭解 [BigQuery 地理函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)。
* 瞭解如何[管理向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)。
* 進一步瞭解 [BigQuery 空間索引和分群的最佳做法](https://cloud.google.com/blog/products/data-analytics/best-practices-for-spatial-clustering-in-bigquery?hl=zh-tw)。
* 如要進一步瞭解如何在 BigQuery 中分析地理空間資料並以圖表呈現，請參閱「[開始使用地理空間分析](https://docs.cloud.google.com/bigquery/docs/geospatial-get-started?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-30 (世界標準時間)。"],[],[]]