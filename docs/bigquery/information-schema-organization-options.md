Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# ORGANIZATION\_OPTIONS 檢視表

您可以查詢 `INFORMATION_SCHEMA.ORGANIZATION_OPTIONS` 檢視區塊，擷取 BigQuery 機構選項的即時中繼資料。這個檢視畫面包含在機構層級設定的設定選項。如要查看設定選項的預設值，請參閱[設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#configuration-settings)。

## 所需權限

如要取得組織選項中繼資料，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.config.get`

下列預先定義的 IAM 角色包含取得組織選項中繼資料所需的權限：

* `roles/bigquery.jobUser`

如要進一步瞭解精細的 BigQuery 權限，請參閱[角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

## 結構定義

查詢 `INFORMATION_SCHEMA.ORGANIZATION_OPTIONS` 檢視區塊時，如果專案中的設定選項與機構層級的預設值不同，查詢結果會為每個設定選項包含一個資料列。

`INFORMATION_SCHEMA.ORGANIZATION_OPTIONS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `option_name` | `STRING` | [選項表格](#options_table)中的其中一個名稱值。 |
| `option_description` | `STRING` | 選項說明。 |
| `option_type` | `STRING` | `option_value` 的資料類型。 |
| `option_value` | `STRING` | 選項的目前值。 |

##### 選項表格

| `option_name` | `option_type` | `option_value` |
| --- | --- | --- |
| `default_time_zone` | `STRING` | 這個機構的預設時區。 |
| `default_kms_key_name` | `STRING` | 這個組織的預設金鑰名稱。 |
| `default_query_job_timeout_ms` | `STRING` | 這個組織的預設查詢逾時時間 (以毫秒為單位)。 |
| `default_interactive_query_queue_timeout_ms` | `STRING` | 這個組織的互動式查詢佇列預設逾時時間 (以毫秒為單位)。 |
| `default_batch_query_queue_timeout_ms` | `STRING` | 這個機構的佇列批次查詢預設逾時時間 (毫秒)。 |
| `reusable_column_aliases_mode` | `STRING` | 這個機構是否已啟用可重複使用的資料欄別名。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免查詢因基礎結構定義變更而中斷。

## 資料保留

這個檢視畫面會顯示目前執行的工作階段，以及過去 180 天內完成的工作階段記錄。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` `region-REGION`.INFORMATION_SCHEMA.ORGANIZATION_OPTIONS `` | 指定組織內的設定選項。 | `REGION` |

請替換下列項目：

* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`region-us`。

## 範例

以下範例會從 `INFORMATION_SCHEMA.ORGANIZATION_OPTIONS` 擷取 `OPTION_NAME`、`OPTION_TYPE` 和 `OPTION_VALUE` 欄。

```
SELECT
  option_name, option_type, option_value
FROM
  `region-us`.INFORMATION_SCHEMA.ORGANIZATION_OPTIONS;
```

**注意：** `INFORMATION_SCHEMA` 檢視名稱會區分大小寫。

結果大致如下：

```
  +--------------------------------------------+-------------+---------------------+
  | option_name                                | option_type | option_value        |
  +--------------------------------------------+-------------+---------------------+
  | default_time_zone                          | STRING      | America/Los_Angeles |
  +--------------------------------------------+-------------+---------------------+
  | default_kms_key_name                       | STRING      | test/testkey1       |
  +--------------------------------------------+-------------+---------------------+
  | default_query_job_timeout_ms               | INT64       | 18000000            |
  +--------------------------------------------+-------------+---------------------+
  | default_interactive_query_queue_timeout_ms | INT64       | 600000              |
  +--------------------------------------------+-------------+---------------------+
  | default_batch_query_queue_timeout_ms       | INT64       | 1200000             |
  +--------------------------------------------+-------------+---------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-15 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-15 (世界標準時間)。"],[],[]]