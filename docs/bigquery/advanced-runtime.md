Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BigQuery 進階執行階段

BigQuery 進階執行階段是一組效能強化功能，可自動加速分析工作負載，使用者不必採取任何動作或變更程式碼。本文將說明這些效能提升功能，包括強化向量化和簡短查詢最佳化。

## 角色和權限

如要取得指定配置設定所需的權限，請要求管理員在專案或機構中授予您「[BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) 」(`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 強化向量化

向量化執行是查詢處理模型，可處理與 CPU 快取大小一致的資料區塊，並使用單指令多資料 (SIMD) 指令。強化向量化功能可將 BigQuery 中的向量化查詢執行作業，擴展至查詢處理的下列層面：

* 透過運用 Capacitor 儲存格式中的專用資料編碼，即可對編碼資料執行篩選器評估作業。
* 專用編碼會透過查詢計畫傳播，因此在資料仍處於編碼狀態時，即可處理更多資料。
* BigQuery 實作運算式摺疊功能來評估決定性函式和常數運算式，可將複雜述詞簡化為常數值。

## 短查詢最佳化

BigQuery 通常會在分散式環境中執行查詢，並使用隨機中間層。短查詢最佳化
動態識別可做為單一階段執行的查詢，減少延遲時間和運算單元用量。如果查詢是在單一階段執行，就能更有效地使用專用編碼。搭配[「選擇性建立工作」模式](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#optional-job-creation)使用時，這些最佳化措施最有效，可盡量減少工作啟動、維護和結果擷取延遲。

短查詢最佳化功能的適用資格不固定，會受到下列因素影響：

* 預測的資料掃描大小。
* 所需資料移動量。
* 查詢篩選器的選擇性。
* 儲存空間中資料的類型和實體配置。
* 整體查詢結構。
* 過去查詢執行的[歷史統計資料](https://docs.cloud.google.com/bigquery/docs/history-based-optimizations?hl=zh-tw)。

## 預估進階執行階段的影響

如要估算進階執行階段的影響，可以使用下列 SQL 查詢，找出預計執行時間改善幅度最大的專案查詢：

```
WITH
  jobs AS (
    SELECT
      *,
      query_info.query_hashes.normalized_literals AS query_hash,
      TIMESTAMP_DIFF(end_time, start_time, MILLISECOND) AS elapsed_ms,
      EXISTS(
        SELECT 1
        FROM UNNEST(JSON_QUERY_ARRAY(query_info.optimization_details.optimizations)) AS o
        WHERE JSON_VALUE(o, '$.enhanced_vectorization') = 'applied'
      ) AS has_advanced_runtime
    FROM region-LOCATION.INFORMATION_SCHEMA.JOBS_BY_PROJECT
    WHERE EXTRACT(DATE FROM creation_time) > DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
      AND creation_time >= TIMESTAMP "2026-01-30"
  ),
  most_recent_jobs_without_advanced_runtime AS (
    SELECT *
    FROM jobs
    WHERE NOT has_advanced_runtime
    QUALIFY ROW_NUMBER() OVER (PARTITION BY query_hash ORDER BY end_time DESC) = 1
  )
SELECT
  job.job_id,
  100 * SAFE_DIVIDE(
    original_job.elapsed_ms - job.elapsed_ms,
    original_job.elapsed_ms) AS percent_execution_time_saved,
  job.elapsed_ms AS new_elapsed_ms,
  original_job.elapsed_ms AS original_elapsed_ms,
FROM jobs AS job
INNER JOIN most_recent_jobs_without_advanced_runtime AS original_job
  USING (query_hash)
WHERE
  job.has_advanced_runtime
  AND original_job.end_time < job.start_time
ORDER BY percent_execution_time_saved DESC
LIMIT 10;
```

**注意：** 您只能比較 2026 年 1 月 30 日當天或之後建立的查詢，因為自該日起，`INFORMATION_SCHEMA.JOBS` 檢視畫面中會持續顯示進階執行階段最佳化指標 (`enhanced_vectorization` 和 `short_query_optimization`)。先前的查詢會限制查詢時間範圍，確保這一點。

更改下列內容：

* `LOCATION`：應評估工作成效的地點

如果已套用進階執行階段，這項查詢的結果可能類似於下列內容：

```
/*--------------+----------------------------+----------------+---------------------*
 |    job_id    | percent_elapsed_time_saved | new_elapsed_ms | original_elapsed_ms |
 +--------------+----------------------------+----------------+---------------------+
 | sample_job1  |         45.38834951456311  |            225 |                 412 |
 | sample_job2  |         45.19480519480519  |            211 |                 385 |
 | sample_job3  |         33.246753246753244 |            257 |                 385 |
 | sample_job4  |         29.28802588996764  |           1311 |                1854 |
 | sample_job5  |         28.18181818181818  |           1027 |                1430 |
 | sample_job6  |         25.804195804195807 |           1061 |                1430 |
 | sample_job7  |         25.734265734265733 |           1062 |                1430 |
 | sample_job8  |         25.454545454545453 |           1066 |                1430 |
 | sample_job9  |         25.384615384615383 |           1067 |                1430 |
 | sample_job10 |         25.034965034965033 |           1072 |                1430 |
 *--------------+----------------------------+----------------+---------------------*/
```

這項查詢的結果僅為進階執行階段影響的預估值。
影響查詢效能的因素有很多，包括但不限於可用時段、資料隨時間的變化、檢視區塊或 UDF 定義，以及查詢參數值的差異。

如果這項查詢的結果為空白，表示沒有任何工作使用進階執行階段，或是所有工作都在 30 天前完成最佳化。

這項查詢可套用至其他查詢效能指標，例如 `total_slot_ms` 和 `total_bytes_billed`。詳情請參閱 [`INFORMATION_SCHEMA.JOBS_BY_PROJECT`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#schema) 的結構定義。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]