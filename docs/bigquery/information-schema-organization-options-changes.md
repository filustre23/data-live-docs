Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# ORGANIZATION\_OPTIONS\_CHANGES 檢視畫面

您可以查詢 `INFORMATION_SCHEMA.ORGANIZATION_OPTIONS_CHANGES` 檢視區塊，擷取機構中 BigQuery 設定變更的即時中繼資料。這個檢視畫面會顯示 2024 年 1 月 31 日後，組織和專案層級的設定變更。

## 所需權限

如要取得擷取設定變更所需的權限，請要求系統管理員授予您機構的「[BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) 」(`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備  `bigquery.config.update` 權限，可取得設定變更。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

## 結構定義

查詢 `INFORMATION_SCHEMA.ORGANIZATION_OPTIONS_CHANGES` 檢視表時，查詢結果會為機構中的每項設定變更包含一個資料列。

`INFORMATION_SCHEMA.ORGANIZATION_OPTIONS_CHANGES` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `update_time` | `TIMESTAMP` | 設定變更發生的時間。 |
| `username` | `STRING` | 如果是第一方使用者，則為使用者電子郵件。如果是第三方使用者，這是使用者在第三方識別資訊提供者中設定的名稱。 |
| `updated_options` | `JSON` | 使用者在變更中更新的設定選項 JSON 物件，內含更新欄位的新舊值。 |
| `project_id` | `STRING` | 專案 ID。如果是組織層級的設定變更，這個欄位會留空。 |
| `project_number` | `INTEGER` | 專案編號。如果是機構層級的設定變更，這個欄位會留空。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 資料保留

這個檢視畫面會顯示正在進行的工作階段，以及過去 180 天內完成的工作階段記錄。

## 範圍和語法

對這個檢視表執行的查詢必須具有[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` `region-REGION`.INFORMATION_SCHEMA.ORGANIZATION_OPTIONS_CHANGES `` | 指定機構內的設定變更。 | `REGION` |

請替換下列項目：

* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如 `US` 或 `us-west2`。

## 範例

以下範例會擷取 `default_query_job_timeout_ms option` 選項的所有變更：

```
SELECT
  *
FROM
  `region-REGION`.INFORMATION_SCHEMA.ORGANIZATION_OPTIONS_CHANGES
WHERE
  updated_options.default_query_job_timeout_ms is not null;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+----------------+------------+-------------------------+-----------------+------------------------------------------------------------------------------------------------------------------+
| project_number | project_id | update_time             | username        | updated_options                                                                                                  |
|----------------|------------|-------------------------|-----------------|------------------------------------------------------------------------------------------------------------------|
| 4471534625     | myproject1 | 2023-08-22 06:57:49 UTC | user1@gmail.com | {"default_query_job_timeout_ms":{"new":0,"old":1860369},"default_time_zone":{"new":"America/New_York","old":""}} |
|----------------|------------|-------------------------|-----------------|------------------------------------------------------------------------------------------------------------------|
| 5027725474     | myproject2 | 2022-08-01 00:00:00 UTC | user2@gmail.com | {"default_query_job_timeout_ms":{"new":1860369,"old":1860008}}                                                   |
+----------------+------------+-------------------------+-----------------+------------------------------------------------------------------------------------------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]