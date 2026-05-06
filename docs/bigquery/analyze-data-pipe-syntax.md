Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 pipe 語法分析資料

本教學課程說明如何使用管道語法編寫查詢，以分析資料。

管道語法是 GoogleSQL 的擴充功能，支援線性查詢結構，可讓您更輕鬆地讀取、撰寫及維護查詢。管道語法包含管道符號 `|>`、[管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#pipe_operators)名稱和任何引數。詳情請參閱下列資源：

* 如要瞭解 pipe 語法，請參閱「[使用 pipe 查詢語法](https://docs.cloud.google.com/bigquery/docs/pipe-syntax-guide?hl=zh-tw)」。
* 如需完整的語法詳細資料，請參閱「[管道查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw)」參考文件。

在本教學課程中，您將使用公開的[`bigquery-public-data.austin_bikeshare.bikeshare_trips`資料表](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=austin_bikeshare&%3Bt=bikeshare_trips&%3Bpage=table&hl=zh-tw)，以管道語法建構複雜查詢，該資料表包含自行車行程資料。

## 目標

* 使用 [`FROM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#from_queries)啟動查詢，即可查看資料表資料。
* 使用 [`EXTEND` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#extend_pipe_operator)新增資料欄。
* 使用 [`AGGREGATE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#extend_pipe_operator)，按日和週匯總資料。
* 使用 [`CROSS JOIN` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#join_pipe_operator)，匯總滑動時間區間的資料。
* 使用 [`WHERE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#where_pipe_operator)篩選資料。
* 執行多層匯總時，請比較管道語法的線性查詢結構與標準語法的巢狀查詢結構。

## 事前準備

您必須先建立或選取專案，才能開始使用 BigQuery 公開資料集。我們免費為您提供每月 1 TB 的資料處理量，讓您無需啟用計費功能就能開始查詢公開資料集。如果您想要進行的運用會超出[免費方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)的範圍，則必須啟用計費功能。

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
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

1. 新專案會自動啟用 BigQuery。如要在現有專案中啟用 BigQuery，

   啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery&hl=zh-tw)

如要進一步瞭解執行查詢的不同方式，請參閱[執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)。

## 查看資料表資料

如要從 `bikeshare_trips` 資料表擷取所有資料，請執行下列查詢：

### 管道語法

```
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`;
```

### 標準語法

```
SELECT *
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`;
```

在管道語法中，查詢可以從 [`FROM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#from_queries)開始，不必使用 `SELECT` 子句，即可傳回表格結果。

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

在 `bikeshare_trips` 資料表中，`start_time` 資料欄是時間戳記，但您可能只想新增顯示行程日期的資料欄。如要以管道語法新增資料欄，請使用 [`EXTEND` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#extend_pipe_operator)：

### 管道語法

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

您可以依日期分組，找出每天的行程總數和使用單車數。

* 使用[`AGGREGATE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#aggregate_pipe_operator)搭配 `COUNT` 函式，找出行程總數和使用的自行車數量。
* 使用 `GROUP BY` 子句，依日期將結果分組。

### 管道語法

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

## 訂單結果

如要依 `date` 欄遞減排序結果，請在 `GROUP BY` 子句中加入
[`DESC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#shorthand_order_pipe_syntax)
後置字元：

### 管道語法

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

在管道語法中，您可以直接將排序後置字元新增至 `GROUP BY` 子句，而不必使用 [`ORDER BY` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#order_by_pipe_operator)。在 `GROUP BY` 子句中加入後置字串，是 `AGGREGATE` 管道語法支援的其中一項選用[簡短排序功能。在標準語法中，這是不可能的，您必須使用 `ORDER BY` 子句進行排序。](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#shorthand_order_pipe_syntax)

## 匯總每週資料

現在您已取得每天使用的單車數量資料，可以根據查詢結果，找出每個七天時間範圍內使用的不重複單車數量。

如要更新資料表中的資料列，改為顯示週而非天數，請在 `GROUP BY` 子句中使用 [`DATE_TRUNC` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_trunc)，並將精細度設為 `WEEK`：

### 管道語法

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

前一節的結果顯示開始和結束日期之間的*固定時間範圍*內的行程，例如 `2024-06-23` 到 `2024-06-29`。您可能想查看*滑動時間範圍*內的行程，也就是七天內每天都會更新的行程。換句話說，您可能想知道特定日期後一週的行程次數和單車使用次數。

如要將滑動視窗套用至資料，請先將每趟行程從開始日期起，往前複製六個額外的*有效*天。接著，使用 `DATE_ADD` 函式計算有效天數的日期。最後，匯總每個有效日期的行程和單車 ID。

1. 如要將資料向前複製，請使用 `GENERATE_ARRAY` 函式和交叉聯結：

   ### 管道語法

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

   `GENERATE_ARRAY` 函式會建立含有七個元素的陣列，分別是 `0` 到 `6`。`CROSS JOIN UNNEST` 運算會建立每個資料列的七個副本，並新增 `diff_days` 資料欄，其中包含 `0` 到 `6` 的陣列元素值。您可以將 `diff_days` 值做為原始日期的調整值，將時間範圍往前推移該天數，最多可推移至原始日期後七天。
2. 如要查看行程的計算結果，請使用 `EXTEND` 管道運算子搭配 `DATE_ADD` 函式，建立名為 `active_date` 的資料欄，其中包含開始日期加上 `diff_days` 資料欄中的值：

   ### 管道語法

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

   舉例來說，如果旅程從 `2024-05-20`開始，則在 `2024-05-26`之前每天都算有效。
3. 最後，匯總行程 ID 和單車 ID，並依 `active_date` 分組：

   ### 管道語法

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

## 篩選未來日期

在上述查詢中，日期會延伸到未來，最多可超出資料中的最後一個日期六天。如要篩除超出資料結束日期的日期，請在查詢中設定最晚日期：

1. 新增另一個 `EXTEND` 管道運算子，使用含 `OVER` 子句的 window 函式，計算資料表中的最大日期。
2. 使用 `WHERE` 管道運算子，篩除超過最晚日期的產生資料列。

### 管道語法

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
* 如需更多技術資訊，請參閱 [Pipe 查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw)參考說明文件。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]