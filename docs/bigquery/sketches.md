Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 草圖 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

BigQuery 的 GoogleSQL 支援資料草圖。
資料草圖是資料匯總的簡要摘要。這項功能會擷取所有必要資訊，以便擷取匯總結果、繼續匯總資料，或與其他草稿合併，進而重新匯總。

使用草圖計算指標的成本，遠低於計算確切值。如果運算速度太慢或需要過多暫時儲存空間，請使用草圖來減少查詢時間和資源。

此外，如果沒有 Sketch，通常只能對原始資料執行作業，才能計算[基數](https://en.wikipedia.org/wiki/Cardinality) (例如不重複使用者人數) 或[分位數](https://en.wikipedia.org/wiki/Quantile) (例如中位數造訪時間)，因為已匯總的資料無法再合併。

假設資料表含有下列資料：

| 產品 | 使用者人數 | 造訪時間中位數 |
| --- | --- | --- |
| 產品 A | 5 億 | 10 分鐘 |
| 產品 B | 2,000 萬 | 2 分鐘 |

由於我們不知道表格中有多少使用者同時使用這兩項產品，因此無法計算這兩項產品的使用者總數。同樣地，由於系統已遺失造訪時間長度的分布情形，因此無法計算造訪時間長度的中位數。

解決方法是改為將草圖儲存在表格中。每個草圖都是特定輸入屬性 (例如基數) 的近似精簡表示法，您可以儲存、合併 (或重新彙整) 及查詢，取得接近確切的結果。在先前的範例中，您可以建立並合併 (重新彙整) 各產品的草圖，估算產品 A 和產品 B 的不重複使用者人數。您也可以使用同樣可合併及查詢的分位數草圖，估算中位數造訪時間。

舉例來說，下列查詢會使用 [HLL++](#sketches_hll) 和 [KLL](#sketches_kll) 草圖，估算 YouTube (產品 A) 和 Google 地圖 (產品 B) 的不重複使用者和中位數造訪時間：

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

由於草圖會對原始資料進行有損壓縮，因此會產生統計錯誤，並以誤差範圍或信賴區間 (CI) 表示。對大多數應用程式而言，這項不確定性很小。舉例來說，在 95% 的情況下，一般基數計數草圖的相對誤差約為 1%。草圖會犧牲部分準確度或*精確度*，換取更快速、更便宜的運算作業，以及更少的儲存空間。

總而言之，草圖具有下列主要屬性：

* 代表特定指標的近似匯總值
* 外型小巧
* 是記憶體內次線性資料結構的序列化形式
* 通常是固定大小，且漸近小於輸入內容
* 可能會產生統計錯誤，您可以透過精確度層級判斷
* 可與其他草圖合併，以匯總基礎資料集的聯集

## 使用草圖合併重新匯總

草圖可讓您儲存及合併資料，以便有效率地重新彙整。因此，草圖特別適合用於資料集的具體化檢視畫面。您可以合併草圖，根據為每個資料串流建立的部分草圖，建構多個資料串流的摘要。

舉例來說，如果您每天建立不重複使用者人數的預估草圖，就能合併每日草圖，取得過去七天的預估不重複使用者人數。重新彙整合併的每日草圖，有助於避免讀取資料集的完整輸入內容。

草圖重新彙整也適用於線上分析處理 (OLAP)。您可以合併草圖，建立[OLAP 立方體](https://en.wikipedia.org/wiki/OLAP_cube)的綜覽，其中草圖會沿著立方體的一或多個特定維度匯總資料。使用實際不重複計數時，無法進行 OLAP 匯總。

## 我該使用哪種草圖？

不同的草圖演算法是為不同類型的指標設計，例如用於個別計數的 [HLL++](#sketches_hll)，以及用於分位數的 [KLL](#sketches_kll)。GoogleSQL 也提供[近似匯總函式](#approx_functions)，您可以使用這些函式查詢這類資料，不必指定精確度等級等查詢詳細資料。

使用的草圖取決於需要估算的資料類型。

### 估算基數

如需估算[基數](https://en.wikipedia.org/wiki/Cardinality)，請使用 [HLL++ 草圖](#sketches_hll)。

舉例來說，如要取得特定月份積極使用產品的不重複使用者人數 (MAU 或 28DAU 指標)，請使用 HLL++ 草圖。

### 計算分位數

如要取得資料集的[分位數](https://en.wikipedia.org/wiki/Quantile)，請使用 [KLL 略圖](#sketches_kll)。

舉例來說，如要取得商店中顧客的造訪時間中位數，或是追蹤支援單在佇列中等待處理的第 95 個百分位數延遲，請使用 KLL 略圖。

## HLL++ 草圖

HyperLogLog++ (HLL++) 是一種草圖演算法，用於估算基數。HLL++ 是以「[HyperLogLog in Practice](https://research.google.com/pubs/archive/40671.pdf?hl=zh-tw)」一文為基礎，其中 *++* 表示對 HyperLogLog 演算法所做的增強功能。

「基數」是草圖輸入內容中不重複元素的數量。舉例來說，您可以使用 HLL++ 略圖，取得開啟應用程式的不重複使用者人數。

HLL++ 可預估極小和極大的基數。HLL++ 包含 64 位元雜湊函式、可減少小型基數估計值記憶體需求的稀疏表示法，以及小型基數估計值的實證偏差修正。

**精確度**

HLL++ 草圖支援自訂精確度。下表顯示支援的精確度值、最大儲存空間大小，以及典型精確度層級的信賴區間 (CI)：

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

您無法從 HLL++ 略圖中刪除值。

**其他詳細資料**

如需可搭配 HLL++ 草圖使用的函式清單，請參閱 [HLL++ 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hll_functions?hl=zh-tw)。

### Sketch 整合

您可以將 HLL++ 草圖與其他系統整合。舉例來說，您可以在 [Dataflow](https://cloud.google.com/dataflow?hl=zh-tw)、[Apache Spark](https://spark.apache.org) 和 [ZetaSketch](https://github.com/google/zetasketch) 等外部應用程式中建立草圖，然後在 GoogleSQL 中使用這些草圖，反之亦然。

除了 GoogleSQL，您也可以搭配 [Java](https://github.com/google/zetasketch/blob/master/java/com/google/zetasketch/HyperLogLogPlusPlus.java) 使用 HLL++ 草圖。

## KLL 草圖

KLL (Karnin-Lang-Liberty 的縮寫) 是一種串流演算法，可計算近似[分位數](#quantiles)的草圖。相較於精確計算，這項函式可更有效率地計算任意分位數，但會產生些微的近似誤差。

**精確度**

KLL 草圖支援自訂精確度。精確度會定義傳回的近似分位數 *q* 的準確度。

根據預設，概略分位數的等級最多可與 `⌈Φ * n⌉` 相差 `±1/1000 * n`，其中 `n` 是輸入中的列數，`⌈Φ * n⌉` 則是確切分位數的等級。

如果您提供自訂精確度，概略分位數的等級最多可能與確切分位數的等級相差 `±1/precision * n`。在 99.999% 的情況下，誤差會落在這個誤差範圍內。這項錯誤保證僅適用於確切排名和近似排名之間的差異。分位數的確切值和近似值之間的數值差異可能非常大。

舉例來說，假設您想找出中位數值 `Φ = 0.5`，並使用 `1000` 的預設精確度。在 99.999% 的情況下，`KLL_QUANTILES.EXTRACT_POINT` 函式傳回的值與實際排名最多相差 `n/1000`。換句話說，傳回的值幾乎一律介於第 49.9 個和第 50.1 個百分位數之間。如果草圖中有 1,000,000 個項目，傳回中位數的排名幾乎一律介於 499,000 和 501,000 之間。

如果您使用 `100` 的自訂精確度尋找中位數值，則在 99.999% 的情況下，`KLL_QUANTILES.EXTRACT_POINT` 函式傳回的值的排名與實際排名最多相差 `n/100`。換句話說，傳回的值幾乎一律介於第 49 和第 51 個百分位數之間。如果草圖中有 1,000,000 個項目，傳回中位數的等級幾乎一律介於 490,000 和 510,000 之間。

使用 [`KLL_QUANTILES.INIT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/kll_functions?hl=zh-tw#kll_quantilesinit_int64) 函式初始化 KLL 草圖時，可以定義精確度。

**大小**

KLL 略圖大小取決於精確度參數和輸入類型。
如果輸入類型為 `INT64`，草圖可使用額外的最佳化功能，如果輸入值來自小型宇宙，這項功能就特別實用。下表包含 `INT64` 的兩欄。其中一欄提供大小上限，適用於大小為 10 億的有限宇宙中的項目；另一欄則提供任意輸入值的上限。

| 精確度 | FLOAT64 | INT64 (<10 億) | INT64 (任何) |
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

Phi (Φ) 代表要產生的分位數，以草圖輸入中總列數的分數表示，並標準化為介於 0 和 1 之間。如果函式支援 phi，函式會傳回值 *v*，使得大約 Φ \* *n* 個輸入值小於或等於 *v*，且 (1-Φ) \* *n* 個輸入值大於或等於 *v*。

**其他詳細資料**

如需可搭配 KLL 摘要使用的函式清單，請參閱 [KLL 量化函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/kll_functions?hl=zh-tw#kll_functions)。

KLL 演算法定義於「[Optimal Quantile Approximation in Streams](https://arxiv.org/pdf/1603.05346v2.pdf)」一文中，並以作者 Karnin、Lang 和 Liberty 的名字命名，他們於 2016 年發表了這篇論文。KLL 演算法使用可變大小的緩衝區，改善舊版 [MP80 演算法](https://polylogblog.files.wordpress.com/2009/08/80munro-median.pdf)，減少大型資料集的記憶體用量，並將草圖大小從 `O(log n)` 縮減為 `O(1)`。由於演算法具有不確定性，因此以相同精確度對同一組資料建立的草圖可能不盡相同。

## 分位數

[分位數](https://en.wikipedia.org/wiki/Quantile)是切點，可將機率分布範圍劃分為機率相等的連續間隔，或以相同方式劃分樣本中的觀察值。支援分位數的草圖可讓您估算分位數，方法是將這些間隔和機率匯總為近乎準確的分位數結果。

分位數通常有兩種定義方式：

* 對於正整數 `q`，`q` 分位數是一組值，可將輸入集分割成 `q` 個大小幾乎相等的子集。其中有些有特定名稱：單一 2 分位數是中位數，4 分位數是四分位數，100 分位數是百分位數等。此外，KLL 函式會傳回輸入的 (確切) 最小值和最大值，因此查詢 2 分位數時會傳回三個值。

  **提示：** 如要擷取一組 `q` 分位數，其中 `q` 是 `number` 引數，請在 `KLL_QUANTILES.*` 函式中使用 `MERGE` 和 `EXTRACT` 函式。
* 或者，分位數也可以視為個別的 `Φ` 分位數，其中 `Φ` 是實數，且 `0 <= Φ <= 1`。`Φ` 分位數 `x` 是輸入內容的元素，其中 `Φ` 分數的輸入內容小於或等於 `x`，而 `(1-Φ)` 分數的輸入內容大於或等於 `x`。在這種表示法中，中位數是 0.5 分位數，第 95 百分位數則是 0.95 分位數。

  **提示：** 如要擷取個別 `Φ` 分位數，請使用支援分位數的 `MERGE_POINT` 和 `EXTRACT_POINT` 函式，其中 `Φ` 是 `phi` 引數。

舉例來說，您可以使用支援分位數的草圖，取得使用者開啟應用程式次數的中位數。

## 概略匯總函式

除了以草圖為基礎的特定近似函式，GoogleSQL 也提供預先定義的近似匯總函式。這些近似匯總函式支援草圖，可進行常見的估算，例如不重複計數、分位數和最高計數，但不允許自訂精確度。此外，這類草圖也不會像其他類型的草圖一樣，公開及儲存草圖以供重新彙整。近似匯總函式的設計宗旨，是執行以草圖為基礎的快速查詢，不必進行詳細設定。

如需可搭配以草圖為基礎的近似值使用的近似匯總函式清單，請參閱「[近似匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]