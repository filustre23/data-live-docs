Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# SCHEMATA\_OPTIONS 檢視區塊

`INFORMATION_SCHEMA.SCHEMATA_OPTIONS` 檢視表包含專案中每個資料集所設定的每個選項，各佔一個資料列。

## 事前準備

如要查詢資料集的中繼資料檢視畫面 `SCHEMATA_OPTIONS`，您需要專案層級的「身分與存取權管理」(IAM) 權限 `bigquery.datasets.get`。

下列預先定義的 IAM 角色都包含必要權限，可取得 `SCHEMATA_OPTIONS` 檢視畫面：

* `roles/bigquery.admin`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataViewer`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.SCHEMATA_OPTIONS` 檢視表時，專案中每個資料集設定的每個選項在查詢結果中都會有一個資料列。

`INFORMATION_SCHEMA.SCHEMATA_OPTIONS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `catalog_name` | `STRING` | 包含資料集的專案名稱 |
| `schema_name` | `STRING` | 資料集的名稱，又稱為 `datasetId` |
| `option_name` | `STRING` | 選項名稱。如需支援的選項清單，請參閱[結構定義選項清單](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#schema_option_list)。 只有在 2022 年 12 月 1 日後更新的資料集，才會顯示「`storage_billing_model`」選項。如果資料集上次更新時間早於該日期，則儲存空間計費模型為 `LOGICAL`。 |
| `option_type` | `STRING` | 選項的資料類型 |
| `option_value` | `STRING` | 選項值 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定地區限定符，系統會從美國地區擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]INFORMATION_SCHEMA.SCHEMATA_OPTIONS` | 專案層級 | 美國區域 |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.SCHEMATA_OPTIONS `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**示例**

```
-- Returns metadata for datasets in a region.
SELECT * FROM region-us.INFORMATION_SCHEMA.SCHEMATA_OPTIONS;
```

## 範例

#### 擷取專案中所有資料集的預設資料表到期時間

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：

```
`PROJECT_ID`.INFORMATION_SCHEMA.SCHEMATA_OPTIONS
```

例如：`` `myproject`.INFORMATION_SCHEMA.SCHEMATA_OPTIONS ``。

```
SELECT
  *
FROM
  INFORMATION_SCHEMA.SCHEMATA_OPTIONS
WHERE
  option_name = 'default_table_expiration_days';
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
  +----------------+---------------+-------------------------------+-------------+---------------------+
  |  catalog_name  |  schema_name  |          option_name          | option_type |    option_value     |
  +----------------+---------------+-------------------------------+-------------+---------------------+
  | myproject      | mydataset3    | default_table_expiration_days | FLOAT64     | 0.08333333333333333 |
  | myproject      | mydataset2    | default_table_expiration_days | FLOAT64     | 90.0                |
  | myproject      | mydataset1    | default_table_expiration_days | FLOAT64     | 30.0                |
  +----------------+---------------+-------------------------------+-------------+---------------------+
```

**注意事項：**`0.08333333333333333` 是 2 小時的浮點表示法。

#### 擷取專案中所有資料集的標籤

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：

```
`PROJECT_ID`.INFORMATION_SCHEMA.SCHEMATA_OPTIONS
```

，例如 `` `myproject`.INFORMATION_SCHEMA.SCHEMATA_OPTIONS ``。

```
SELECT
  *
FROM
  INFORMATION_SCHEMA.SCHEMATA_OPTIONS
WHERE
  option_name = 'labels';
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
  +----------------+---------------+-------------+---------------------------------+------------------------+
  |  catalog_name  |  schema_name  | option_name |          option_type            |      option_value      |
  +----------------+---------------+-------------+---------------------------------+------------------------+
  | myproject      | mydataset1    | labels      | ARRAY<STRUCT<STRING, STRING>>   | [STRUCT("org", "dev")] |
  | myproject      | mydataset2    | labels      | ARRAY<STRUCT<STRING, STRING>>   | [STRUCT("org", "dev")] |
  +----------------+---------------+-------------+---------------------------------+------------------------+
```

**注意：** 查詢結果會排除沒有標籤的資料集。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]