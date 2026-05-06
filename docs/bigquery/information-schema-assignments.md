Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 「指派項目」檢視畫面

`INFORMATION_SCHEMA.ASSIGNMENTS` 檢視畫面會列出管理專案中所有目前的指派項目，且清單近乎即時更新。每一列代表一項目前指派的作業。目前指派的作業處於待處理或有效狀態，且尚未刪除。如要進一步瞭解預留項目，請參閱「[預留項目簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。

**注意：** 「檢視區塊名稱」`INFORMATION_SCHEMA.ASSIGNMENTS`和`INFORMATION_SCHEMA.ASSIGNMENTS_BY_PROJECT`是同義詞，可互換使用。

## 必要權限

如要查詢 `INFORMATION_SCHEMA.ASSIGNMENTS` 檢視畫面，您需要專案的 `bigquery.reservationAssignments.list` Identity and Access Management (IAM) 權限。下列預先定義的 IAM 角色都包含必要權限：

* `roles/bigquery.resourceAdmin`
* `roles/bigquery.resourceEditor`
* `roles/bigquery.resourceViewer`
* `roles/bigquery.user`
* `roles/bigquery.admin`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

`INFORMATION_SCHEMA.ASSIGNMENTS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `ddl` | `STRING` | 用來建立這項指派作業的 DDL 陳述式。 |
| `project_id` | `STRING` | 管理專案的 ID。 |
| `project_number` | `INTEGER` | 管理專案的編號。 |
| `assignment_id` | `STRING` | 可明確識別作業的 ID。 |
| `reservation_name` | `STRING` | 指派項目使用的預留項目名稱。 |
| `job_type` | `STRING` | 可使用保留項目的工作類型。可能的值為 `PIPELINE`、`QUERY`、`CONTINUOUS`、`ML_EXTERNAL` 或 `BACKGROUND`。 |
| `assignee_id` | `STRING` | 唯一識別指派對象資源的 ID。 |
| `assignee_number` | `INTEGER` | 可明確識別指派對象資源的號碼。 |
| `assignee_type` | `STRING` | 指派對象資源的類型。可以是 `organization`、`folder` 或 `project`。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定符，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.ASSIGNMENTS[_BY_PROJECT] `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 範例

如要對預設專案以外的專案執行查詢，請使用以下格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.ASSIGNMENTS
```

。

更改下列內容：

* PROJECT\_ID：您已指派預留事項的專案 ID。
* REGION\_NAME：區域名稱。

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.ASSIGNMENTS ``。

以下範例會取得專案目前指派的預留項目及其運算單元容量。比較專案的運算單元用量與指派給該專案的預留項目運算單元容量，有助於偵錯工作效能。

```
SELECT
  reservation.reservation_name,
  reservation.slot_capacity
FROM
  `RESERVATION_ADMIN_PROJECT.region-REGION_NAME`.
  INFORMATION_SCHEMA.ASSIGNMENTS_BY_PROJECT assignment
INNER JOIN
  `RESERVATION_ADMIN_PROJECT.region-REGION_NAME`.
  INFORMATION_SCHEMA.RESERVATIONS_BY_PROJECT AS reservation
ON
  (assignment.reservation_name = reservation.reservation_name)
WHERE
   assignment.assignee_id = "PROJECT_ID"
  AND job_type = "QUERY";
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]