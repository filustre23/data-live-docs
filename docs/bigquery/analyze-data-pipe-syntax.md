Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用管道語法分析資料

GoogleSQL 的管道語法可讓您以線性方式建構查詢，讓複雜的資料分析更容易讀取、編寫及維護。在本教學課程中，您將使用公開的 [`bigquery-public-data.austin_bikeshare.bikeshare_trips` 資料表](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=austin_bikeshare&%3Bt=bikeshare_trips&%3Bpage=table&hl=zh-tw)建立查詢，篩選、匯總及分析單車行程資料。如需概念背景和運算子規格，請參閱「[使用管道查詢語法](https://docs.cloud.google.com/bigquery/docs/pipe-syntax-guide?hl=zh-tw)」和「[管道查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw)」。

## 目標

* 使用 [`FROM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#from_queries)開始查詢，即可查看資料表資料。
* 使用 [`EXTEND` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#extend_pipe_operator)新增資料欄。
* 使用 [`AGGREGATE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#extend_pipe_operator)，按日和週匯總資料。
* 使用 [`CROSS JOIN` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#join_pipe_operator)，匯總滑動時間範圍內的資料。
* 使用 [`WHERE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#where_pipe_operator)篩選資料。
* 執行多層級匯總時，比較管道語法的線性查詢結構與標準語法的巢狀查詢結構。

## 事前準備

您必須先建立或選取專案，才能開始使用 BigQuery 公開資料集。我們免費為您提供每月 1 TB 的資料處理量，讓您無需啟用計費功能就能開始查詢公開資料集。如果您想要進行的運用會超出[免費方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)的範圍，則必須啟用計費功能。

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).

1. 新專案會自動啟用 BigQuery。如要在現有專案中啟用 BigQuery，請按照下列步驟操作：

   啟用 BigQuery API (如果尚未啟用)。

   **啟用 API 所需的角色**

   如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「Service Usage 管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

如要進一步瞭解執行查詢的不同方式，請參閱「[執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)」。

## 查看資料表資料

如要從 `bikeshare_trips` 資料表擷取所有資料，請執行下列查詢：

### Pipe 語法

```
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`;
```

### 標準語法

```
SELECT *
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`;
```

在管道語法中，查詢可以從 [`FROM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#from_queries)開始，不需使用 `SELECT` 子句即可傳回資料表結果。

結果大致如下：

```
+----------+-----------------+---------+-----------+-------------------------+-----+
| trip_id  | subscriber_type | bike_id | bike_type | start_time              | ... |
+----------+-----------------+---------+-----------+-------------------------+-----+
| 28875008 | Pay-as-you-ride | 18181   | electric  | 2023-02-12 12:46:32 UTC | ... |
| 28735401 | Explorer        | 214     | classic   | 2023-01-13 12:01:45 UTC | ... |
| 29381980 | Local365        | 21803   | electric  | 2023-04-20 08:43:46 UTC | ... |
| ...      | ...             | ...     | ...       | ...                     | ... |
+----------+-----------------+---------+-----------+-------------------------+-----+
```

## 新增欄

在 `bikeshare_trips` 資料表中，`start_time` 欄是時間戳記，但您可能想新增只顯示行程日期的資料欄。如要在管道語法中新增資料欄，請使用 [`EXTEND` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#extend_pipe_operator)：

### Pipe 語法

```
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
|> EXTEND CAST(start_time AS DATE) AS date;
```

### 標準語法

```
SELECT *, CAST(start_time AS DATE) AS date
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`;
```

結果大致如下：

```
+----------+-----------------+---------+-----------+-------------------------+------------+-----+
| trip_id  | subscriber_type | bike_id | bike_type | start_time              | date       | ... |
+----------+-----------------+---------+-----------+-------------------------+------------+-----+
| 28875008 | Pay-as-you-ride | 18181   | electric  | 2023-02-12 12:46:32 UTC | 2023-02-12 | ... |
| 28735401 | Explorer        | 214     | classic   | 2023-01-13 12:01:45 UTC | 2023-01-13 | ... |
| 29381980 | Local365        | 21803   | electric  | 2023-04-20 08:43:46 UTC | 2023-04-20 | ... |
| ...      | ...             | ...     | ...       | ...                     | ...        | ... |
+----------+-----------------+---------+-----------+-------------------------+------------+-----+
```

## 匯總每日資料

您可以依日期分組，找出每天的總行程數和使用的單車數。

* 使用[`AGGREGATE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#aggregate_pipe_operator)和 `COUNT` 函式，找出行程總數和使用的單車數量。
* 使用 `GROUP BY` 子句，依日期將結果分組。

### Pipe 語法

```
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
|> EXTEND CAST(start_time AS DATE) AS date
|> AGGREGATE
     COUNT(*) AS trips,
     COUNT(DISTINCT bike_id) AS distinct_bikes
   GROUP BY date;
```

### 標準語法

```
SELECT
  CAST(start_time AS DATE) AS date,
  COUNT(*) AS trips,
  COUNT(DISTINCT bike_id) AS distinct_bikes
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY date;
```

結果大致如下：

```
+------------+-------+----------------+
| date       | trips | distinct_bikes |
+------------+-------+----------------+
| 2023-04-20 | 841   | 197            |
| 2023-01-27 | 763   | 148            |
| 2023-06-12 | 562   | 202            |
| ...        | ...   | ...            |
+------------+-------+----------------+
```

## 排序結果

如要依 `date` 欄遞減排序結果，請在 `GROUP BY` 子句中加入 [`DESC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#shorthand_order_pipe_syntax) 後置字串：

### Pipe 語法

```
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
|> EXTEND CAST(start_time AS DATE) AS date
|> AGGREGATE
     COUNT(*) AS trips,
     COUNT(DISTINCT bike_id) AS distinct_bikes
   GROUP BY date DESC;
```

### 標準語法

```
SELECT
  CAST(start_time AS DATE) AS date,
  COUNT(*) AS trips,
  COUNT(DISTINCT bike_id) AS distinct_bikes
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY date
ORDER BY date DESC;
```

結果大致如下：

```
+------------+-------+----------------+
| date       | trips | distinct_bikes |
+------------+-------+----------------+
| 2024-06-30 | 331   | 90             |
| 2024-06-29 | 395   | 123            |
| 2024-06-28 | 437   | 137            |
| ...        | ...   | ...            |
+------------+-------+----------------+
```

在管道語法中，您可以直接將排序後置字串新增至 `GROUP BY` 子句，而不必使用 [`ORDER BY` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#order_by_pipe_operator)。在 `GROUP BY` 子句中加入後置字串，是管道語法支援的幾種選用[簡寫排序功能 (搭配 `AGGREGATE`)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#shorthand_order_pipe_syntax) 之一。在標準語法中，這是不可能的，您必須使用 `ORDER BY` 子句進行排序。

## 匯總每週資料

現在您已取得每天使用的單車數量資料，可以進一步查詢每七天使用的不重複單車數量。

如要更新資料表中的資料列，以顯示週數而非天數，請在 `GROUP BY` 子句中使用 [`DATE_TRUNC` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_trunc)，並將精細程度設為 `WEEK`：

### Pipe 語法

```
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
|> EXTEND CAST(start_time AS DATE) AS date
|> AGGREGATE
    COUNT(*) AS trips,
    COUNT(DISTINCT bike_id) AS distinct_bikes,
GROUP BY DATE_TRUNC(date, WEEK) AS date DESC;
```

### 標準語法

```
SELECT
  DATE_TRUNC(CAST(start_time AS DATE), WEEK) AS date,
  COUNT(*) AS trips,
  COUNT(DISTINCT bike_id) AS distinct_bikes,
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY date
ORDER BY date DESC;
```

結果大致如下：

```
+------------+-------+----------------+
| date       | trips | distinct_bikes |
+------------+-------+----------------+
| 2024-06-30 | 331   | 90             |
| 2024-06-23 | 3206  | 213            |
| 2024-06-16 | 3441  | 212            |
| ...        | ...   | ...            |
+------------+-------+----------------+
```

## 在滑動視窗中匯總

上一節的結果顯示開始和結束日期之間的「固定時間範圍」內的行程，例如 `2024-06-23` 到 `2024-06-29`。您可能想在*滑動時間範圍*內查看行程，也就是隨著新的一天到來，時間範圍也會向前移動。換句話說，您可能想知道任何指定日期後一週內的行程數和單車使用量。

如要對資料套用滑動時間範圍，請先將每趟行程從開始日期起，往後複製六個額外的「有效」天數。接著，使用 `DATE_ADD` 函式計算活躍天數的日期。最後，匯總每個活動日的行程和單車 ID。

1. 如要向前複製資料，請使用 `GENERATE_ARRAY` 函式和 cross join：

   ### Pipe 語法

   ```
   FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
   |> EXTEND CAST(start_time AS DATE) AS date
   |> CROSS JOIN UNNEST(GENERATE_ARRAY(0, 6)) AS diff_days;
   ```

   ### 標準語法

   ```
   SELECT *, CAST(start_time AS DATE) AS date
   FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
   CROSS JOIN UNNEST(GENERATE_ARRAY(0, 6)) AS diff_days;
   ```

   `GENERATE_ARRAY` 函式會建立包含七個元素的陣列，從 `0` 到 `6`。`CROSS JOIN UNNEST` 作業會為每個資料列建立七個副本，並新增 `diff_days` 資料欄，其中包含每個資料列從 `0` 到 `6` 的其中一個陣列元素值。您可以使用 `diff_days` 值做為原始日期的調整值，將時間範圍向前滑動指定天數，最多可比原始日期早七天。
2. 如要查看行程的計算有效日期，請使用 `EXTEND` 管道運算子和 `DATE_ADD` 函式，建立名為 `active_date` 的資料欄，其中包含開始日期加上 `diff_days` 資料欄中的值：

   ### Pipe 語法

   ```
   FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
   |> EXTEND CAST(start_time AS DATE) AS date
   |> CROSS JOIN UNNEST(GENERATE_ARRAY(0, 6)) AS diff_days
   |> EXTEND DATE_ADD(date, INTERVAL diff_days DAY) AS active_date;
   ```

   ### 標準語法

   ```
   SELECT *, DATE_ADD(date, INTERVAL diff_days DAY) AS active_date
   FROM (
     SELECT *, CAST(start_time AS DATE) AS date
     FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
     CROSS JOIN UNNEST(GENERATE_ARRAY(0, 6)) AS diff_days)
   ```

   舉例來說，如果行程從 `2024-05-20` 開始，則到 `2024-05-26` 為止的每一天，行程都會視為有效。
3. 最後，匯總行程 ID 和單車 ID，並依 `active_date` 分組：

   ### Pipe 語法

   ```
   FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
   |> EXTEND CAST(start_time AS DATE) AS date
   |> CROSS JOIN UNNEST(GENERATE_ARRAY(0, 6)) AS diff_days
   |> EXTEND DATE_ADD(date, INTERVAL diff_days DAY) AS active_date
   |> AGGREGATE COUNT(DISTINCT bike_id) AS active_7d_bikes,
               COUNT(trip_id) AS active_7d_trips
   GROUP BY active_date DESC;
   ```

   ### 標準語法

   ```
   SELECT
     DATE_ADD(date, INTERVAL diff_days DAY) AS active_date,
     COUNT(DISTINCT bike_id) AS active_7d_bikes,
     COUNT(trip_id) AS active_7d_trips
   FROM (
     SELECT *, CAST(start_time AS DATE) AS date
     FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
     CROSS JOIN UNNEST(GENERATE_ARRAY(0, 6)) AS diff_days)
   GROUP BY active_date
   ORDER BY active_date DESC;
   ```

   結果大致如下：

   ```
   +-------------+-----------------+-----------------+
   | active_date | active_7d_bikes | active_7d_trips |
   +-------------+-----------------+-----------------+
   | 2024-07-06  | 90              | 331             |
   | 2024-07-05  | 142             | 726             |
   | 2024-07-04  | 186             | 1163            |
   | ...         | ...             | ...             |
   +-------------+-----------------+-----------------+
   ```

## 篩除未來日期

在上述查詢中，日期會延伸至未來，最多可超過資料中最後一個日期六天。如要篩除超出資料結束日期的日期，請在查詢中設定日期上限：

1. 新增另一個 `EXTEND` 管道運算子，使用含有 `OVER` 子句的視窗函式，計算資料表中的最大日期。
2. 使用 `WHERE` 管道運算子，篩除超過最大日期的生成資料列。

### Pipe 語法

```
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
|> EXTEND CAST(start_time AS DATE) AS date
|> EXTEND MAX(date) OVER () AS max_date
|> CROSS JOIN UNNEST(GENERATE_ARRAY(0, 6)) AS diff_days
|> EXTEND DATE_ADD(date, INTERVAL diff_days DAY) AS active_date
|> WHERE active_date <= max_date
|> AGGREGATE COUNT(DISTINCT bike_id) AS active_7d_bikes,
             COUNT(trip_id) AS active_7d_trips
   GROUP BY active_date DESC;
```

### 標準語法

```
SELECT
  DATE_ADD(date, INTERVAL diff_days DAY) AS active_date,
  COUNT(DISTINCT bike_id) AS active_7d_bikes,
  COUNT(trip_id) AS active_7d_trips
FROM(
  SELECT *
  FROM (
    SELECT *,
      DATE_ADD(date, INTERVAL diff_days DAY) AS active_date,
      MAX(date) OVER () AS max_date
    FROM(
      SELECT *, CAST(start_time AS DATE) AS date,
      FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
      CROSS JOIN UNNEST(GENERATE_ARRAY(0, 6)) AS diff_days))
  WHERE active_date <= max_date)
GROUP BY active_date
ORDER BY active_date DESC;
```

結果大致如下：

```
+-------------+-----------------+-----------------+
| active_date | active_7d_bikes | active_7d_trips |
+-------------+-----------------+-----------------+
| 2024-06-30  | 212             | 3031            |
| 2024-06-29  | 213             | 3206            |
| 2024-06-28  | 219             | 3476            |
| ...         | ...             | ...             |
+-------------+-----------------+-----------------+
```

## 後續步驟

* 如要進一步瞭解管道語法的運作方式，請參閱「[使用管道查詢語法](https://docs.cloud.google.com/bigquery/docs/pipe-syntax-guide?hl=zh-tw)」。
* 如需更多技術資訊，請參閱[管道查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw)參考文件。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]