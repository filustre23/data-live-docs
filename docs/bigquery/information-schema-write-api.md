Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# WRITE\_API\_TIMELINE 檢視畫面

`INFORMATION_SCHEMA.WRITE_API_TIMELINE` 檢視畫面會顯示目前專案每分鐘的 BigQuery Storage Write API 擷取統計資料匯總。

您可以查詢 `INFORMATION_SCHEMA`Write API 檢視畫面，擷取使用 BigQuery Storage Write API 將資料擷取至 BigQuery 的歷來和即時資訊。詳情請參閱 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)。

**注意：** 檢視區塊名稱 `INFORMATION_SCHEMA.WRITE_API_TIMELINE` 和 `INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_PROJECT` 是同義詞，可以互換使用。

## 必要權限

如要查詢 `INFORMATION_SCHEMA.WRITE_API_TIMELINE` 檢視畫面，您需要專案的 `bigquery.tables.list` Identity and Access Management (IAM) 權限。

下列預先定義的 IAM 角色都包含必要權限：

* `roles/bigquery.user`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.resourceAdmin`
* `roles/bigquery.admin`

**注意：**「擁有者」或「編輯者」這些[基本角色](https://docs.cloud.google.com/bigquery/docs/access-control-basic-roles?hl=zh-tw)*不*包含必要的 `bigquery.tables.list` 權限。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA` BigQuery Storage Write API 檢視區塊時，查詢結果會包含使用 BigQuery Storage Write API 將資料擷取至 BigQuery 的歷史和即時資訊。下列檢視區塊中的每個資料列，都代表匯總後特定資料表的擷取統計資料，匯總間隔為一分鐘，起始時間為 `start_timestamp`。統計資料會依串流類型和錯誤代碼分組，因此每個時間戳記和資料表組合的每一分鐘間隔，都會有一列資料，代表每個串流類型和每個遇到的錯誤代碼。如果要求成功，錯誤代碼會設為 `OK`。如果特定時間範圍內沒有資料擷取至資料表，則該資料表不會顯示對應時間戳記的資料列。`INFORMATION_SCHEMA.WRITE_API_TIMELINE` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `start_timestamp` | `TIMESTAMP` | *(分區資料欄)* 匯總統計資料的 1 分鐘間隔開始時間戳記。 |
| `project_id` | `STRING` | *(叢集資料欄)* 專案 ID。 |
| `project_number` | `INTEGER` | 專案編號。 |
| `dataset_id` | `STRING` | *(叢集資料欄)* 資料集 ID。 |
| `table_id` | `STRING` | *(叢集欄)* 資料表的 ID。 |
| `stream_type` | `STRING` | 使用 BigQuery Storage Write API 擷取資料時所用的[串流類型](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#overview)。應為「DEFAULT」、「COMMITTED」、「BUFFERED」或「PENDING」其中之一。 |
| `error_code` | `STRING` | 這個資料列指定的要求傳回的錯誤代碼。「OK」表示要求成功。 |
| `total_requests` | `INTEGER` | 1 分鐘間隔內的要求總數。 |
| `total_rows` | `INTEGER` | 1 分鐘間隔內所有要求的總列數。 |
| `total_input_bytes` | `INTEGER` | 1 分鐘間隔內所有資料列的位元組總數。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 資料保留

這個檢視區塊包含過去 180 天的 BigQuery Storage Write API 擷取記錄。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定符，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.WRITE_API_TIMELINE[_BY_PROJECT] `` | 專案層級 | REGION |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**示例**

* 如要查詢美國多區域的資料，請使用
  `` `region-us`.INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_PROJECT ``
* 如要查詢歐盟多區域的資料，請使用 `` `region-eu`.INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_PROJECT ``
* 如要查詢 asia-northeast1 地區的資料，請使用
  `` `region-asia-northeast1`.INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_PROJECT ``

如需可用地區清單，請參閱「[資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)」。

## 範例

##### 範例 1：近期 BigQuery Storage Write API 擷取作業失敗

以下範例會計算過去 30 分鐘內，專案中所有資料表每分鐘的失敗要求總數，並依資料流類型和錯誤代碼細分：

```
SELECT
  start_timestamp,
  stream_type,
  error_code,
  SUM(total_requests) AS num_failed_requests
FROM
  `region-us`.INFORMATION_SCHEMA.WRITE_API_TIMELINE
WHERE
  error_code != 'OK'
  AND start_timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 30 MINUTE)
GROUP BY
  start_timestamp,
  stream_type,
  error_code
ORDER BY
  start_timestamp DESC;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+---------------------+-------------+------------------+---------------------+
|   start_timestamp   | stream_type |    error_code    | num_failed_requests |
+---------------------+-------------+------------------+---------------------+
| 2023-02-24 00:25:00 | PENDING     | NOT_FOUND        |                   5 |
| 2023-02-24 00:25:00 | DEFAULT     | INVALID_ARGUMENT |                   1 |
| 2023-02-24 00:25:00 | DEFAULT     | DEADLINE_EXCEEDED|                   4 |
| 2023-02-24 00:24:00 | PENDING     | INTERNAL         |                   3 |
| 2023-02-24 00:24:00 | DEFAULT     | INVALID_ARGUMENT |                   1 |
| 2023-02-24 00:24:00 | DEFAULT     | DEADLINE_EXCEEDED|                   2 |
+---------------------+-------------+------------------+---------------------+
```

##### 範例 2：每分鐘所有要求 (含錯誤代碼) 的明細

以下範例會計算每分鐘成功和失敗的附加要求，並依錯誤代碼類別劃分。這項查詢可用於填入資訊主頁。

```
SELECT
  start_timestamp,
  SUM(total_requests) AS total_requests,
  SUM(total_rows) AS total_rows,
  SUM(total_input_bytes) AS total_input_bytes,
  SUM(
    IF(
      error_code IN (
        'INVALID_ARGUMENT', 'NOT_FOUND', 'CANCELLED', 'RESOURCE_EXHAUSTED',
        'ALREADY_EXISTS', 'PERMISSION_DENIED', 'UNAUTHENTICATED',
        'FAILED_PRECONDITION', 'OUT_OF_RANGE'),
      total_requests,
      0)) AS user_error,
  SUM(
    IF(
      error_code IN (
        'DEADLINE_EXCEEDED','ABORTED', 'INTERNAL', 'UNAVAILABLE',
        'DATA_LOSS', 'UNKNOWN'),
      total_requests,
      0)) AS server_error,
  SUM(IF(error_code = 'OK', 0, total_requests)) AS total_error,
FROM
  `region-us`.INFORMATION_SCHEMA.WRITE_API_TIMELINE
GROUP BY
  start_timestamp
ORDER BY
  start_timestamp DESC;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+---------------------+----------------+------------+-------------------+------------+--------------+-------------+
|   start_timestamp   | total_requests | total_rows | total_input_bytes | user_error | server_error | total_error |
+---------------------+----------------+------------+-------------------+------------+--------------+-------------+
| 2020-04-15 22:00:00 |         441854 |     441854 |       23784853118 |          0 |           17 |          17 |
| 2020-04-15 21:59:00 |         355627 |     355627 |       26101982742 |          8 |            0 |          13 |
| 2020-04-15 21:58:00 |         354603 |     354603 |       26160565341 |          0 |            0 |           0 |
| 2020-04-15 21:57:00 |         298823 |     298823 |       23877821442 |          2 |            0 |           2 |
+---------------------+----------------+------------+-------------------+------------+--------------+-------------+
```

##### 範例 3：傳入流量最高的資料表

以下範例會傳回傳入流量最多的 10 個資料表的 BigQuery Storage Write API 擷取統計資料：

```
SELECT
  project_id,
  dataset_id,
  table_id,
  SUM(total_rows) AS num_rows,
  SUM(total_input_bytes) AS num_bytes,
  SUM(total_requests) AS num_requests
FROM
  `region-us`.INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_PROJECT
GROUP BY
  project_id,
  dataset_id,
  table_id
ORDER BY
  num_bytes DESC
LIMIT 10;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+----------------------+------------+-------------------------------+------------+----------------+--------------+
|      project_id      | dataset_id |           table_id            |  num_rows  |   num_bytes    | num_requests |
+----------------------+------------+-------------------------------+------------+----------------+--------------+
| my-project           | dataset1   | table1                        | 8016725532 | 73787301876979 |   8016725532 |
| my-project           | dataset1   | table2                        |   26319580 | 34199853725409 |     26319580 |
| my-project           | dataset2   | table1                        |   38355294 | 22879180658120 |     38355294 |
| my-project           | dataset1   | table3                        |  270126906 | 17594235226765 |    270126906 |
| my-project           | dataset2   | table2                        |   95511309 | 17376036299631 |     95511309 |
| my-project           | dataset2   | table3                        |   46500443 | 12834920497777 |     46500443 |
| my-project           | dataset2   | table4                        |   25846270 |  7487917957360 |     25846270 |
| my-project           | dataset1   | table4                        |   18318404 |  5665113765882 |     18318404 |
| my-project           | dataset1   | table5                        |   42829431 |  5343969665771 |     42829431 |
| my-project           | dataset1   | table6                        |    8771021 |  5119004622353 |      8771021 |
+----------------------+------------+-------------------------------+------------+----------------+--------------+
```

##### 範例 4：資料表的 BigQuery Storage Write API 擷取錯誤率

以下範例會計算特定資料表的每日錯誤明細，並依錯誤代碼分類：

```
SELECT
  TIMESTAMP_TRUNC(start_timestamp, DAY) as day,
  project_id,
  dataset_id,
  table_id,
  error_code,
  SUM(total_rows) AS num_rows,
  SUM(total_input_bytes) AS num_bytes,
  SUM(total_requests) AS num_requests
FROM
  `region-us`.INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_PROJECT
WHERE
  table_id LIKE 'my_table'
GROUP BY
  project_id, dataset_id, table_id, error_code, day
ORDER BY
  day, project_id, dataset_id DESC;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+---------------------+-------------+------------+----------+----------------+----------+-----------+--------------+
|         day         |  project_id | dataset_id | table_id |   error_code   | num_rows | num_bytes | num_requests |
+---------------------+-------------+------------+----------+----------------+----------+-----------+--------------+
| 2020-04-21 00:00:00 | my_project  | my_dataset | my_table | OK             |       41 |    252893 |           41 |
| 2020-04-20 00:00:00 | my_project  | my_dataset | my_table | OK             |     2798 |  10688286 |         2798 |
| 2020-04-19 00:00:00 | my_project  | my_dataset | my_table | OK             |     2005 |   7979495 |         2005 |
| 2020-04-18 00:00:00 | my_project  | my_dataset | my_table | OK             |     2054 |   7972378 |         2054 |
| 2020-04-17 00:00:00 | my_project  | my_dataset | my_table | OK             |     2056 |   6978079 |         2056 |
| 2020-04-17 00:00:00 | my_project  | my_dataset | my_table | INTERNAL       |        4 |     10825 |            4 |
+---------------------+-------------+------------+----------+----------------+----------+-----------+--------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]