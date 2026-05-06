Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# ASSIGNMENT\_CHANGES 檢視畫面

`INFORMATION_SCHEMA.ASSIGNMENT_CHANGES` 檢視畫面會列出管理專案中所有指派項目的變更，且近乎即時。每一列代表對單一指派項目的單一變更。如要進一步瞭解預留項目，請參閱「[預留項目簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。

**注意：** 「檢視區塊名稱」`INFORMATION_SCHEMA.ASSIGNMENT_CHANGES`和`INFORMATION_SCHEMA.ASSIGNMENT_CHANGES_BY_PROJECT`是同義詞，可互換使用。

## 必要權限

如要查詢 `INFORMATION_SCHEMA.ASSIGNMENT_CHANGES` 檢視畫面，您需要專案的 `bigquery.reservationAssignments.list` Identity and Access Management (IAM) 權限。下列預先定義的 IAM 角色都包含必要權限：

* `roles/bigquery.resourceAdmin`
* `roles/bigquery.resourceEditor`
* `roles/bigquery.resourceViewer`
* `roles/bigquery.user`
* `roles/bigquery.admin`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

`INFORMATION_SCHEMA.ASSIGNMENT_CHANGES` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `change_timestamp` | `TIMESTAMP` | 變更發生的時間。 |
| `project_id` | `STRING` | 管理專案的 ID。 |
| `project_number` | `INTEGER` | 管理專案的編號。 |
| `assignment_id` | `STRING` | 可明確識別作業的 ID。 |
| `reservation_name` | `STRING` | 指派項目使用的預留項目名稱。 |
| `job_type` | `STRING` | 可使用保留項目的工作類型。可以是 `PIPELINE` 或 `QUERY`。 |
| `assignee_id` | `STRING` | 唯一識別指派對象資源的 ID。 |
| `assignee_number` | `INTEGER` | 可明確識別指派對象資源的號碼。 |
| `assignee_type` | `STRING` | 指派對象資源的類型。可以是 `organization`、`folder` 或 `project`。 |
| `action` | `STRING` | 指派作業發生的事件類型。可以是 `CREATE`、`UPDATE` 或 `DELETE`。 |
| `user_email` | `STRING` | 進行變更的使用者電子郵件地址或[員工身分聯盟](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)主體。`google`，瞭解 Google 進行的變更。`NULL`：如果電子郵件地址不明。 |
| `state` | `STRING` | 指派狀態。可以是 `PENDING` 或 `ACTIVE`。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 資料保留

這個檢視畫面會顯示目前的指派項目和已刪除的指派項目，這些項目最多會保留 41 天，之後就會從檢視畫面中移除。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定符，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.ASSIGNMENT_CHANGES[_BY_PROJECT] `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 範例

### 查看作業的最新變更

以下範例會顯示在指定日期內，對特定作業進行最新指派更新的使用者。

```
SELECT
  user_email,
  change_timestamp,
  reservation_name,
  assignment_id
FROM
  `region-us`.INFORMATION_SCHEMA.ASSIGNMENT_CHANGES
WHERE
  change_timestamp BETWEEN '2021-09-30' AND '2021-10-01'
  AND assignment_id = 'assignment_01'
ORDER BY
  change_timestamp DESC
LIMIT 1;
```

結果大致如下：

```
+--------------------------------+-----------------------+--------------------+-----------------+
|           user_email           |    change_timestamp   |  reservation_name  |  assignment_id  |
+--------------------------------+-----------------------+--------------------+-----------------+
|  cloudysanfrancisco@gmail.com  |2021-09-30 09:30:00 UTC|   my_reservation   |  assignment_01  |
+--------------------------------+-----------------------+--------------------+-----------------+
```

### 找出特定時間點的預訂指派狀態

以下範例會顯示特定時間點的預訂項目所有有效指派項目。

```
SELECT
    reservation_name,
    assignee_id,
    assignee_type,
    job_type
FROM
    `region-REGION`.INFORMATION_SCHEMA.ASSIGNMENT_CHANGES
WHERE
    reservation_name = RESERVATION_NAME
    AND change_timestamp < TIMESTAMP
QUALIFY ROW_NUMBER() OVER(PARTITION BY assignee_id, job_type ORDER BY change_timestamp DESC) = 1
AND action != 'DELETE';
```

更改下列內容：

* `REGION`：預留項目所在的區域
* `RESERVATION_NAME`：指派作業使用的預訂名稱
* `TIMESTAMP`：代表檢查指派清單的特定時間點的時間戳記

結果大致如下：

```
+-------------------------+---------------------------+---------------+----------+
|    reservation_name     |        assignee_id        | assignee_type | job_type |
+-------------------------+---------------------------+---------------+----------+
| test-reservation        | project_1                 | PROJECT       | QUERY    |
| test-reservation        | project_2                 | PROJECT       | QUERY    |
+-------------------------+---------------------------+---------------+----------+
```

### 找出執行特定工作時的預訂指派狀態

如要顯示特定工作執行時的有效指派項目，請使用下列範例。

```
SELECT
    reservation_name,
    assignee_id,
    assignee_type,
    job_type
FROM
    `region-REGION`.INFORMATION_SCHEMA.ASSIGNMENT_CHANGES
WHERE
    reservation_name = RESERVATION_NAME
    AND change_timestamp < (SELECT creation_time FROM PROJECT_ID.`region-REGION`.INFORMATION_SCHEMA.JOBS WHERE job_id = JOB_ID)
QUALIFY ROW_NUMBER() OVER(PARTITION BY assignee_id, job_type ORDER BY change_timestamp DESC) = 1
AND action != 'DELETE';
```

更改下列內容：

* `REGION`：預留項目所在的區域
* `RESERVATION_NAME`：指派作業使用的預訂名稱
* `PROJECT_ID`： Google Cloud 執行工作所在專案的 ID
* `JOB_ID`：用來檢查指派狀態的工作 ID




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]