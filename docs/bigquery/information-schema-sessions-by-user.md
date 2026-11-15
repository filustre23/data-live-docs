Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# SESSIONS\_BY\_USER 檢視表

`INFORMATION_SCHEMA.SESSIONS_BY_USER` 檢視表包含目前使用者在目前專案中建立的 BigQuery 工作階段即時中繼資料。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.SESSIONS_BY_USER` 檢視表，您必須具備專案的 `bigquery.jobs.list` Identity and Access Management (IAM) 權限。下列各項預先定義的 IAM 角色都包含必要權限：

* 專案檢視者
* BigQuery 使用者

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.SESSIONS_BY_*` 檢視表時，查詢結果會為每個 BigQuery 工作階段顯示一列。

`INFORMATION_SCHEMA.SESSIONS_BY_*` 檢視表具有下列結構定義：

**注意：**基礎資料會依 `creation_time` 欄分區，並依 `project_id` 和 `user_email` 分類。

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `creation_time` | `TIMESTAMP` | (*分區資料欄*) 這個工作階段的建立時間。 分區依據為這個時間戳記的世界標準時間。 |
| `expiration_time` | `TIMESTAMP` | (*分區資料欄*) 這個工作階段的到期時間。 分區依據為這個時間戳記的世界標準時間。 |
| `folder_numbers` | `ARRAY<INT64>` | 階層中包含專案的資料夾 ID，依階層由低到高排序。 |
| `is_active` | `BOOL` | 工作階段是否仍在進行中？如果是，則為 `TRUE`，否則為 `FALSE`。 |
| `last_modified_time` | `TIMESTAMP` | *(分區欄) 工作階段上次修改的時間。*分區依據為這個時間戳記的世界標準時間。 |
| `principal_subject` | `STRING` | 執行工作階段的主體 ID。格式如下：Google 帳戶使用者為 `user:USER_EMAIL`、服務帳戶為 `serviceAccount:SA_EMAIL`，或[員工身分聯盟](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)和 [Workload Identity Federation](https://docs.cloud.google.com/iam/docs/workload-identity-federation?hl=zh-tw) 主體為開頭是 `principal://` 的主體 ID。 |
| `project_id` | `STRING` | (*分群欄*) 專案 ID。 |
| `project_number` | `INTEGER` | 專案編號。 |
| `session_id` | `STRING` | 工作階段 ID。例如 `bquxsession_1234`。 |
| `user_email` | `STRING` | (*分群欄*) 執行工作階段的使用者電子郵件地址或服務帳戶。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免查詢在基礎結構定義變更時中斷。

## 資料保留

這個檢視畫面會顯示目前執行中的工作階段，以及過去 180 天內完成的工作階段記錄。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定詞，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.SESSIONS_BY_USER `` | 目前使用者在指定專案中建立的工作階段。 | `REGION` |

請更改下列內容：

* 選用：`PROJECT_ID`： Google Cloud 專案的 ID。如未指定，則會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)，才能查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

## 範例

如要對預設專案以外的專案執行查詢，請按照下列格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.SESSIONS_BY_USER
```

例如：`` `myproject`.`region-us`.INFORMATION_SCHEMA.SESSIONS_BY_USER ``。

以下範例列出目前使用者建立的工作階段：

```
SELECT
  session_id,
  creation_time
FROM
  `region-us`.INFORMATION_SCHEMA.SESSIONS_BY_USER
WHERE
  creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
ORDER BY
  creation_time DESC;
```

**注意：**`INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果應如下所示：

```
+-------------------------------------------------------------------------+
| session_id                                        | creation_time       |
+-------------------------------------------------------------------------+
| CgwKCmZhbGl1LXRlc3QQARokMGQ5YWWYzZmE0YjhkMDBm     | 2021-06-01 08:04:26 |
| CgwKCmZhbGl1LXRlc3QQARokMDAzYjI0OWQtZTczwZjA1NDc2 | 2021-05-31 22:43:02 |
+-------------------------------------------------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-13 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-13 (世界標準時間)。"],[],[]]