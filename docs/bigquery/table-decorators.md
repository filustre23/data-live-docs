Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 舊版 SQL 中的資料表修飾符

**注意：** 本文說明舊版 SQL 查詢語法中的資料表修飾符。我們建議使用的 BigQuery 查詢語法是 GoogleSQL。標準 SQL 不支援資料表修飾符，但 GoogleSQL 中的 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 子句提供與時間修飾符同等的功能。如果是範圍修飾符，您可以使用時間分區資料表，在 GoogleSQL 中實現類似的語意。詳情請參閱 GoogleSQL 遷移指南中的「[資料表修飾符](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-tw#table_decorators)」和「[舊版 SQL 功能可用性](https://docs.cloud.google.com/bigquery/docs/legacy-sql-feature-availability?hl=zh-tw)」。

通常，BigQuery 會在[執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)時進行完整資料欄掃描。您可以在舊版 SQL 中，使用資料表修飾符執行更符合成本效益的資料子集查詢。無論何時讀取資料表都可以使用資料表修飾符，例如複製資料表、[匯出資料表](https://docs.cloud.google.com/bigquery/docs/export-intro?hl=zh-tw)或使用 `tabledata.list` 列出資料時。

**注意：** GoogleSQL 不支援範圍裝飾符。如要查看這項功能要求的狀態，請參閱 [BigQuery 功能要求追蹤器](https://issuetracker.google.com/issues/35905931?hl=zh-tw)。您可以按一下「Vote for this issue and get email notifications」(針對此問題投票並取得電子郵件通知) 星號圖示，以登錄您對該功能的支持。

資料表修飾符支援相對和絕對 `<time>` 值。相對值由負數表示，絕對值由正數表示。舉例來說，`-3600000` 表示相對於目前時間的一小時前 (以毫秒為單位)；`3600000` 表示 1970 年 1 月 1 日後的一小時 (以毫秒為單位)。

## 時間修飾符

時間修飾符 (舊稱「快照修飾符」) 會參照資料表在特定時間點的歷來資料。

### 語法

```
@<time>
```

* 指 `<time>` 的資料表歷來資料，以紀元後毫秒為單位。
* `<time>` 必須是最近七天內，且大於或等於資料表的建立時間，但小於資料表的刪除或到期時間。
* `@0` 是特殊情況，指資料表可用的最舊資料。

時間修飾符也用於舊版 SQL 以外的環境。您可以在 [`bq cp` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp)中使用這些修飾符，[還原在七天內刪除的資料表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw)。

### 範例

如要取得一小時前資料表的歷來資料：

**相對值範例**

```
#legacySQL
SELECT COUNT(*) FROM [PROJECT_ID:DATASET.TABLE@-3600000]
```

**絕對值範例**

1. 取得一小時前的 `<time>`：

   ```
   #legacySQL
   SELECT INTEGER(DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -1, 'HOUR')/1000)
   ```
2. 然後在以下查詢中替換 `<time>`：

   ```
   #legacySQL
   SELECT COUNT(*) FROM [PROJECT_ID:DATASET.TABLE@time]
   ```

## 範圍修飾符

### 語法

```
@<time1>-<time2>
```

* 指 `<time1>` 和 `<time2>` 之間新增的資料表資料，以紀元後毫秒為單位。
* `<time1>` 和 `<time2>`
  必須在最近七天內。
* `<time2>` 是選用項目，預設為「現在」。

### 範例

**相對值範例**

如要取得前一小時和前半小時間新增的資料表資料：

```
#legacySQL
SELECT COUNT(*) FROM [PROJECT_ID:DATASET.TABLE@-3600000--1800000]
```

如要取得前 10 分鐘的資料：

```
#legacySQL
SELECT COUNT(*) FROM [PROJECT_ID:DATASET.TABLE@-600000-]
```

**絕對值範例**

如要取得前一小時和前半小時間新增的資料表資料：

1. 取得一小時前的 `<time1>`：

   ```
   #legacySQL
   SELECT INTEGER(DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -1, 'HOUR')/1000)
   ```
2. 取得半小時前的 `<time2>`：

   ```
   #legacySQL
   SELECT INTEGER(DATE_ADD(USEC_TO_TIMESTAMP(NOW()), -30, 'MINUTE')/1000)
   ```
3. 在下列查詢中替換 `<time1>` 和
   `<time2>`：

   ```
   #legacySQL
   SELECT COUNT(*) FROM [PROJECT_ID:DATASET.TABLE@time1-time2]
   ```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]