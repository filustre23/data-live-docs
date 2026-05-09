Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# CAPACITY\_COMMITMENT\_CHANGES 檢視畫面

`INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES`檢視畫面會列出管理專案中容量使用承諾的所有變更，且近乎即時。每一列代表對單一容量承諾的單一變更。
詳情請參閱「[預留配額承諾](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)」。

**注意：** 檢視區塊名稱 `INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES` 和 `INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES_BY_PROJECT` 是同義詞，可以互換使用。

## 必要權限

如要查詢 `INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES` 檢視畫面，您必須具備專案的 `bigquery.capacityCommitments.list` Identity and Access Management (IAM) 權限。下列預先定義的 IAM 角色都包含必要權限：

* `roles/bigquery.resourceAdmin`
* `roles/bigquery.resourceEditor`
* `roles/bigquery.resourceViewer`
* `roles/bigquery.user`
* `roles/bigquery.admin`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

`INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `change_timestamp` | `TIMESTAMP` | 變更發生的時間。 |
| `project_id` | `STRING` | 管理專案的 ID。 |
| `project_number` | `INTEGER` | 管理專案的編號。 |
| `capacity_commitment_id` | `STRING` | 可明確識別容量承諾的 ID。 |
| `commitment_plan` | `STRING` | 容量使用承諾的合約方案。 |
| `state` | `STRING` | 容量使用承諾的狀態。可以是 `PENDING` 或 `ACTIVE`。 |
| `slot_count` | `INTEGER` | 與容量使用承諾相關聯的運算單元數量。 |
| `action` | `STRING` | 容量承諾發生的事件類型。可以是 `CREATE`、`UPDATE` 或 `DELETE`。 |
| `user_email` | `STRING` | 進行變更的使用者電子郵件地址或[員工身分聯盟](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)主體。`google`，瞭解 Google 進行的變更。`NULL`：如果電子郵件地址不明。 |
| `commitment_start_time` | `TIMESTAMP` | 目前使用承諾期間的開始時間。僅適用於`ACTIVE`容量承諾，否則為`NULL`。 |
| `commitment_end_time` | `TIMESTAMP` | 目前使用承諾期間的結束時間。僅適用於`ACTIVE`容量承諾，否則為`NULL`。 |
| `failure_status` | `RECORD` | 如果是 `FAILED` 承諾方案，則提供失敗原因，否則為 `NULL`。`RECORD` 由 `code` 和 `message` 組成。 |
| `renewal_plan` | `STRING` | 容量使用承諾在 `commitment_end_time` 通過後轉換的方案。方案變更後，承諾期會根據承諾方案延長。僅適用於 `ANNUAL` 和 `TRIAL` 承諾，否則為 `NULL`。 |
| `edition` | `STRING` | 與這項預訂相關聯的版本。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。 |
| `is_flat_rate` | `BOOL` | 承諾是否與舊版固定費率容量模式或版本相關聯。如果 `FALSE`，則目前的約期與版本相關聯。如果為 `TRUE`，則承諾是舊版固定費率容量模式。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 資料保留

這個檢視畫面會顯示目前的容量使用承諾，以及最多保留 41 天的已刪除容量使用承諾，之後這些承諾就會從檢視畫面中移除。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定符，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES[_BY_PROJECT] `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 範例

下列查詢會顯示在指定日期內，對目前專案進行最新容量承諾更新的使用者。

```
SELECT
  user_email,
  change_timestamp
FROM
  `region-us`.INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES
WHERE
  change_timestamp BETWEEN '2021-09-30' AND '2021-10-01'
ORDER BY
  change_timestamp DESC
LIMIT 1;
```

結果大致如下：

```
+--------------------------------+-------------------------+
|           user_email           |     change_timestamp    |
+--------------------------------+-------------------------+
|     222larabrown@gmail.com     | 2021-09-30 09:30:00 UTC |
+--------------------------------+-------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]