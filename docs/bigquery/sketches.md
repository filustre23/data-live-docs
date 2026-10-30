Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 草圖 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

BigQuery 的 GoogleSQL 支援資料草圖。資料草圖是資料匯總的精簡摘要。它會擷取所有必要資訊，以便擷取匯總結果、繼續匯總資料，或與其他草圖合併，以便重新匯總。

使用草圖計算指標的成本，遠低於計算精確值的成本。如果運算速度太慢或需要太多暫存空間，請使用草圖來減少查詢時間和資源。

此外，如果不使用草圖，通常只能透過對原始資料執行工作，來計算[基數](https://en.wikipedia.org/wiki/Cardinality) (例如不重複使用者人數) 或[分位數](https://en.wikipedia.org/wiki/Quantile) (例如造訪時間長度中位數)，因為已匯總的資料無法再合併。

假設資料表包含下列資料：

| 產品 | 使用者人數 | 造訪停留時間中位數 |
| --- | --- | --- |
| 產品 A | 5 億 | 10 分鐘 |
| 產品 B | 2,000 萬 | 2 分鐘 |

由於表格未顯示同時使用這兩項產品的使用者人數，因此無法計算這兩項產品的使用者總數。同樣地，由於造訪時間長度的分布資料已遺失，因此無法計算造訪時間長度的中位數。

解決方法是改為將草圖儲存在資料表中。每個草圖都是特定輸入屬性 (例如基數) 的近似精簡表示法，您可以儲存、合併 (或重新匯總) 及查詢，以取得接近精確的結果。在上述範例中，您可以為產品 A 和產品 B 建立並合併 (重新匯總) 草圖，藉此估算不重複使用者人數。您也可以使用分位數草圖估算造訪時間長度的中位數，並同樣可以合併及查詢。

舉例來說，下列查詢使用 [HLL++](#sketches_hll) 和 [KLL](#sketches_kll) 草圖，估算 YouTube (產品 A) 和 Google 地圖 (產品 B) 的不重複使用者和造訪時間長度中位數：

```
-- Build sketches for YouTube stats.
CREATE TABLE user.YOUTUBE_ACCESS_STATS
AS
SELECT
  HLL_COUNT.INIT(user_id) AS distinct_users_sketch,
  KLL_QUANTILES.INIT_INT64(visit_duration_ms) AS visit_duration_ms_sketch,
  hour_of_day
FROM YOUTUBE_ACCESS_LOG()
GROUP BY hour_of_day;

-- Build sketches for Maps stats.
CREATE TABLE user.MAPS_ACCESS_STATS
AS
SELECT
  HLL_COUNT.INIT(user_id) AS distinct_users_sketch,
  KLL_QUANTILES.INIT_INT64(visit_duration_ms) AS visit_duration_ms_sketch,
  hour_of_day
FROM MAPS_ACCESS_LOG()
GROUP BY hour_of_day;

-- Query YouTube hourly stats.
SELECT
  HLL_COUNT.EXTRACT(distinct_users_sketch) AS distinct_users,
  KLL_QUANTILES.EXTRACT_POINT_INT64(visit_duration_ms_sketch, 0.5)
  AS median_visit_duration, hour_of_day
FROM user.YOUTUBE_ACCESS_STATS;

-- Query YouTube daily stats.
SELECT
  HLL_COUNT.MERGE(distinct_users_sketch),
  KLL_QUANTILES.MERGE_POINT_INT64(visit_duration_ms_sketch, 0.5)
  AS median_visit_duration, date
FROM user.YOUTUBE_ACCESS_STATS
GROUP BY date;

-- Query total stats across YouTube and Maps.
SELECT
  HLL_COUNT.MERGE(distinct_users_sketch) AS unique_users_all_services,
  KLL_QUANTILES.MERGE_POINT_INT64(visit_duration_ms_sketch, 0.5)
    AS median_visit_duration_all_services,
FROM
  (
    SELECT * FROM user.YOUTUBE_ACCESS_STATS
    UNION ALL
    SELECT * FROM user.MAPS_ACCESS_STATS
  );
```

由於草圖會對原始資料進行有損壓縮，因此會產生統計誤差，並以誤差範圍或信賴區間 (CI) 表示。對大多數應用程式來說，這種不確定性很小。舉例來說，在 95% 的情況下，一般基數計數草圖的相對誤差約為 1%。草圖會犧牲部分準確度或*精確度*，以換取更快速、更便宜的運算，以及更少的儲存空間。

總結來說，草圖具有下列主要屬性：

* 代表特定指標的大約匯總值
* 精簡
* 是記憶體內次線性資料結構的序列化形式
* 通常是固定大小，且漸近小於輸入內容
* 可能會產生統計誤差，您可透過精確度等級來判斷
* 可與其他草圖合併，彙整基礎資料集的聯集

## 透過草圖合併重新匯總

草圖可讓您儲存及合併資料，以便有效率地重新匯總。因此，草圖特別適合用來儲存資料集的預先運算摘要，也就是「*materialized view*」。您可以合併草圖，根據為每個串流建立的部分草圖，建構多個資料串流的摘要。

舉例來說，如果您每天建立一個草圖，用於估算不重複使用者人數，則可以合併每日草圖，取得過去七天的不重複使用者人數。重新匯總合併的每日草圖，可避免讀取資料集的完整輸入內容。

Sketch 重新匯總也適用於線上分析處理 (OLAP)。您可以合併草圖，建立 [OLAP 立方體](https://en.wikipedia.org/wiki/OLAP_cube)的匯總，其中草圖會沿著立方體的一或多個特定維度匯總資料。OLAP 匯總無法使用真正的相異計數。

## 我該使用哪種草圖？

不同的草圖演算法適用於不同類型的指標，例如 [HLL++](#sketches_hll) 適用於不重複計數，[KLL](#sketches_kll) 適用於分位數。GoogleSQL 也提供[近似匯總函式](#approx_functions)，可用於查詢這類資料，不必指定精確度等級等查詢詳細資料。

您使用的草圖取決於需要估算的資料類型。

### 估算基數

如需估算[基數](https://en.wikipedia.org/wiki/Cardinality)，請使用 [HLL++ 草圖](#sketches_hll)。

舉例來說，如要取得在指定月份內活躍使用產品的不重複使用者人數 (MAU 或 28DAU 指標)，請使用 HLL++ 草圖。

### 計算分位數

如要取得資料集的[分位數](https://en.wikipedia.org/wiki/Quantile)，請使用 [KLL 草圖](#sketches_kll)。

舉例來說，如要取得商店中顧客的造訪時間長度中位數，或追蹤票證在處理前停留在佇列中的第 95 個百分位數延遲時間，請使用 KLL 草圖。

## HLL++ 草圖

HyperLogLog++ (HLL++) 是用於估算基數的草圖演算法。HLL++ 是以「[HyperLogLog in Practice](https://research.google.com/pubs/archive/40671.pdf?hl=zh-tw)」這篇論文為基礎，其中 *++* 表示對 HyperLogLog 演算法進行的增強。

「基數」是指草圖輸入內容中不重複元素的數量。舉例來說，您可以使用 HLL++ 草圖，取得開啟應用程式的不重複使用者人數。

HLL++ 可估算極小和極大的基數。HLL++ 包含 64 位元雜湊函式、稀疏表示法 (可減少小基數估計值的記憶體需求)，以及小基數估計值的經驗偏差校正。

**精確度**

HLL++ 草圖支援自訂精確度。下表列出支援的精確度值、儲存空間大小上限，以及一般精確度等級的信賴區間 (CI)：

| 精確度 | 儲存空間大小上限 | 65% CI | 95% CI | CI |
| --- | --- | --- | --- | --- |
| 10 | 1 KiB + 28 B | ±3.25% | ±6.50% | ±9.75% |
| 11 | 2 KiB + 28 B | ±2.30% | ±4.60% | ±6.89% |
| 12 | 4 KiB + 28 B | ±1.63% | ±3.25% | ±4.88% |
| 13 | 8 KiB + 28 B | ±1.15% | ±2.30% | ±3.45% |
| 14 | 16 KiB + 30 B | ±0.81% | ±1.63% | ±2.44% |
| 15 (預設) | 32 KiB + 30 B | ±0.57% | ±1.15% | ±1.72% |
| 16 | 64 KiB + 30 B | ±0.41% | ±0.81% | ±1.22% |
| 17 | 128 KiB + 30 B | ±0.29% | ±0.57% | ±0.86% |
| 18 | 256 KiB + 30 B | ±0.20% | ±0.41% | ±0.61% |
| 19 | 512 KiB + 30 B | ±0.14% | ±0.29% | ±0.43% |
| 20 | 1024 KiB + 30 B | ±0.10% | ±0.20% | ±0.30% |
| 21 | 2048 KiB + 32 B | ±0.07% | ±0.14% | ±0.22% |
| 22 | 4096 KiB + 32 B | ±0.05% | ±0.10% | ±0.15% |
| 23 | 8192 KiB + 32 B | ±0.04% | ±0.07% | ±0.11% |
| 24 | 16384 KiB + 32 B | ±0.03% | ±0.05% | ±0.08% |

使用 [`HLL_COUNT.INIT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hll_functions?hl=zh-tw#hll_countinit) 函式初始化 HLL++ 草圖時，可以定義精確度。

**刪除**

您無法從 HLL++ 草圖中刪除值。

**其他詳細資料**

如需可與 HLL++ 草圖搭配使用的函式清單，請參閱「[HLL++ 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hll_functions?hl=zh-tw)」。

### Sketch 整合

您可以將 HLL++ 草圖與其他系統整合。舉例來說，您可以在 [Dataflow](https://cloud.google.com/dataflow?hl=zh-tw)、[Apache Spark](https://spark.apache.org) 和 [ZetaSketch](https://github.com/google/zetasketch) 等外部應用程式中建立草圖，然後在 GoogleSQL 中使用，反之亦然。

除了 GoogleSQL 之外，您也可以搭配使用 HLL++ 草圖和 [Java](https://github.com/google/zetasketch/blob/master/java/com/google/zetasketch/HyperLogLogPlusPlus.java)。

## KLL 草圖

KLL (Karnin-Lang-Liberty 的簡稱) 是一種串流演算法，用於計算近似[分位數](#quantiles)的草圖。它計算任意分位數的效率遠高於精確計算，但會產生微小的近似誤差。

**精確度**

KLL 草圖支援自訂精確度。精確度定義了傳回的近似分位數 *q* 的精確度。

根據預設，近似分位數的排名最多可與 `⌈Φ * n⌉` 相差 `±1/1000 * n`，其中 `n` 是輸入內容中的資料列數，`⌈Φ * n⌉` 則是確切分位數的排名。

如果提供自訂精確度，近似分位數的排名與精確分位數的排名最多可相差 `±1/precision * n`。在 99.999% 的情況下，誤差會在這個誤差範圍內。這項誤差保證僅適用於精確排名和近似排名之間的差異。分位數的精確值和近似值之間的數值差異可能任意大。

舉例來說，假設您想找出中位數 `Φ = 0.5`，並使用預設精確度 `1000`。在 99.999% 的情況下，`KLL_QUANTILES.EXTRACT_POINT` 函式傳回的值與實際排名的差異最多為 `n/1000`。換句話說，傳回的值幾乎一律介於第 49.9 個和第 50.1 個百分位數之間。如果草圖中有 1,000,000 個項目，則傳回的中位數排名幾乎一律介於 499,000 和 501,000 之間。

如果使用自訂精確度 `100` 找出中位數值，則在 99.999% 的情況下，`KLL_QUANTILES.EXTRACT_POINT` 函式傳回的值排名與實際排名最多相差 `n/100`。換句話說，傳回的值幾乎一律介於第 49 個和第 51 個百分位數之間。如果草圖中有 1,000,000 個項目，則傳回的中位數排名幾乎一律介於 490,000 和 510,000 之間。

使用 [`KLL_QUANTILES.INIT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/kll_functions?hl=zh-tw#kll_quantilesinit_int64) 函式初始化 KLL 草圖時，可以定義精確度。

**大小**

KLL 草圖大小取決於精確度參數和輸入類型。如果輸入類型為 `INT64`，草圖可使用額外的最佳化功能，這在輸入值來自小型母體時特別實用。下表包含兩個 `INT64` 欄。其中一欄提供大小為 1B 的有限母體中項目的草圖大小上限，第二欄則提供任意輸入值的上限。

| 精確度 | FLOAT64 | INT64 (<1B) | INT64 (不限) |
| --- | --- | --- | --- |
| 10 | 761 B | 360 B | 717 B |
| 20 | 1.46 KB | 706 B | 1.47 KB |
| 50 | 3.49 KB | 1.72 KB | 3.60 KB |
| 100 | 6.94 KB | 3.44 KB | 7.12 KB |
| 200 | 13.87 KB | 6.33 KB | 13.98 KB |
| 500 | 35.15 KB | 14.47 KB | 35.30 KB |
| 1000 | 71.18 KB | 27.86 KB | 71.28 KB |
| 2000 | 144.51 KB | 55.25 KB | 144.57 KB |
| 5000 | 368.87 KB | 139.54 KB | 368.96 KB |
| 10000 | 749.82 KB | 282.27 KB | 697.80 KB |
| 20000 | 1.52 MB | 573.16 KB | 1.37 MB |
| 50000 | 3.90 MB | 1.12 MB | 3.45 MB |
| 100000 | 7.92 MB | 2.18 MB | 6.97 MB |

**Phi**

Phi (Φ) 代表要產生的分位數，以草圖輸入中資料列總數的分數表示，正規化為 0 到 1 之間。如果函式支援 phi，則會傳回值 *v*，使得大約 Φ \* *n* 個輸入值小於或等於 *v*，且 (1-Φ) \* *n* 個輸入值大於或等於 *v*。

**其他詳細資料**

如要查看可與 KLL 草圖搭配使用的函式清單，請參閱「[KLL 分位數函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/kll_functions?hl=zh-tw#kll_functions)」。

KLL 演算法定義於論文《[Optimal Quantile Approximation in Streams](https://arxiv.org/pdf/1603.05346v2.pdf)》，並以作者 Karnin、Lang 和 Liberty 的名字命名，他們於 2016 年發表了這篇論文。KLL 演算法使用可變大小的緩衝區，減少大型資料集的記憶體用量，將草圖大小從 `O(log n)` 縮減至 `O(1)`，進而改善舊版 [MP80 演算法](https://polylogblog.files.wordpress.com/2009/08/80munro-median.pdf)。由於演算法具有不確定性，因此在同一組資料上以相同精確度建立的草圖可能不盡相同。

## 分位數

[分位數](https://en.wikipedia.org/wiki/Quantile)是切點，可將機率分布範圍劃分為機率相等的連續區間，或以相同方式劃分樣本中的觀測值。支援分位數的草圖可將這些區間和機率匯總為近乎精確的分位數結果，讓您估算分位數。

分位數通常有兩種定義方式：

* 對於正整數 `q`，`q` 分位數是一組值，可將輸入集分割成 `q` 個大小幾乎相等的子集。其中有些有特定名稱：單一 2 分位數是中位數、4 分位數是四分位數、100 分位數是百分位數等。KLL 函式還會傳回輸入內容的 (確切) 最小值和最大值，因此查詢 2 分位數時，會傳回三個值。

  **提示：** 如要擷取一組 `q` 分位數 (其中 `q` 是 `number` 引數)，請使用 `KLL_QUANTILES.*` 函式中的 `MERGE` 和 `EXTRACT` 函式。
* 或者，分位數也可以視為個別的 `Φ` 分位數，其中 `Φ` 是實數，且 `0 <= Φ <= 1`。`Φ` 分位數 `x` 是輸入內容的元素，因此輸入內容的 `Φ` 分數小於或等於 `x`，而 `(1-Φ)` 分數大於或等於 `x`。在這個標記法中，中位數是 0.5 分位數，第 95 個百分位數是 0.95 分位數。

  **提示：** 如要擷取個別 `Φ` 分位數，請使用支援分位數的 `MERGE_POINT` 和 `EXTRACT_POINT` 函式，其中 `Φ` 是 `phi` 引數。

舉例來說，您可以使用支援分位數的草圖，取得使用者開啟應用程式次數的中位數。

## 概略匯總函式

GoogleSQL 提供預先定義的約略匯總函式，可做為特定草圖式近似函式的替代方案。這些近似匯總函式支援不重複計數、分位數和最高計數等常見估計值的草圖，但不允許自訂精確度。此外，這類草圖也不會像其他類型的草圖一樣，公開及儲存草圖以重新匯總。近似匯總函式專為執行快速草圖式查詢而設計，不需詳細設定。

如要查看可與草圖式近似值搭配使用的近似匯總函式清單，請參閱「[近似匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]