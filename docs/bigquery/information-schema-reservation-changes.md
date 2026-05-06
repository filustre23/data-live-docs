Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# RESERVATION\_CHANGES 檢視畫面

`INFORMATION_SCHEMA.RESERVATION_CHANGES` 檢視畫面會列出管理專案中所有預留項目的變更，且近乎即時。每一列代表單一預訂的變更。詳情請參閱「[預留項目簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。

**注意：** 檢視區塊名稱 `INFORMATION_SCHEMA.RESERVATION_CHANGES` 和 `INFORMATION_SCHEMA.RESERVATION_CHANGES_BY_PROJECT` 是同義詞，可以互換使用。

## 必要權限

如要查詢 `INFORMATION_SCHEMA.RESERVATION_CHANGES` 檢視畫面，您需要專案的 `bigquery.reservations.list` Identity and Access Management (IAM) 權限。下列預先定義的 IAM 角色都包含必要權限：

* BigQuery 資源管理員 (`roles/bigquery.resourceAdmin`)
* BigQuery 資源編輯者 (`roles/bigquery.resourceEditor`)
* BigQuery 資源檢視者 (`roles/bigquery.resourceViewer`)
* BigQuery 使用者 (`roles/bigquery.user`)
* BigQuery 管理員 (`roles/bigquery.admin`)

如要進一步瞭解 BigQuery 權限，請參閱 [BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

## 結構定義

`INFORMATION_SCHEMA.RESERVATION_CHANGES` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `change_timestamp` | `TIMESTAMP` | 變更發生的時間。 |
| `project_id` | `STRING` | 管理專案的 ID。 |
| `project_number` | `INTEGER` | 管理專案的編號。 |
| `reservation_name` | `STRING` | 使用者提供的預留項目名稱。 |
| `ignore_idle_slots` | `BOOL` | 如為 false，使用這個預留項目的任何查詢都可以使用其他容量承諾的閒置運算單元。 |
| `action` | `STRING` | 預訂發生的事件類型。可以是 `CREATE`、`UPDATE` 或 `DELETE`。 |
| `slot_capacity` | `INTEGER` | 預留項目的基準。 |
| `user_email` | `STRING` | 進行變更的使用者電子郵件地址或[員工身分聯盟](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)主體。`google`，瞭解 Google 進行的變更。`NULL`：如果電子郵件地址不明。 |
| `target_job_concurrency` | `INTEGER` | 可同時執行的查詢目標數量，這會受到可用資源的限制。如果為零，系統會根據可用資源自動計算這個值。 |
| `autoscale` | `STRUCT` | 保留項目的自動調度容量相關資訊。欄位包括：   * `current_slots`：自動調度資源功能為預訂項目新增的時段數量。   **注意：**使用者減少 `max_slots` 後，可能需要一段時間才能傳播，因此 `current_slots` 可能會維持原始值，且在短時間內 (不到一分鐘) 大於 `max_slots`。 * `max_slots`：自動調度資源可為預留項目新增的運算單元數量上限。 |
| `edition` | `STRING` | 與這項預訂相關聯的版本。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。 |
| `primary_location` | `STRING` | 預訂項目主要副本的目前位置。這個欄位僅適用於使用[代管災難復原功能](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)的預訂。 |
| `secondary_location` | `STRING` | 預留項目次要副本的目前位置。這個欄位只會為使用[代管災難復原功能](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)的預訂設定。 |
| `original_primary_location` | `STRING` | 最初建立預訂的位置。 |
| `labels` | `RECORD` | 與預訂項目相關聯的標籤陣列。 |
| `reservation_group_path` | `STRING` | 預訂連結的階層式群組結構。 舉例來說，如果群組結構包含上層群組和子項群組，則 `reservation_group_path` 欄位會包含類似 `[parent group, child group]` 的清單。這個欄位目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。 |
| `max_slots` | `INTEGER` | 這個預留項目可使用的運算單元數量上限，包括基準運算單元 (`slot_capacity`)、閒置運算單元 (如果 `ignore_idle_slots` 為 false) 和自動調度運算單元。使用者會指定這個欄位，以使用[預訂預測功能](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)。 |
| `scaling_mode` | `STRING` | 預留項目的縮放模式，決定預留項目如何從基準縮放至 `max_slots`。使用者會指定這個欄位，以使用[預訂預測功能](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 資料保留

這個檢視畫面會顯示目前的預訂和已刪除的預訂，後者最多保留 41 天，之後就會從檢視畫面中移除。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定符，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID].`region-REGION`.INFORMATION_SCHEMA.RESERVATION_CHANGES[_BY_PROJECT] `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 範例

以下範例會取得特定預訂的變更記錄。您可以使用這項資訊查看特定預訂項目的變更清單，例如建立或刪除預訂項目。

```
SELECT
  *
FROM
  reservation-admin-project.`region-us`.
  INFORMATION_SCHEMA.RESERVATION_CHANGES
WHERE
  reservation_name = "my-reservation"
ORDER BY
  change_timestamp DESC;
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]