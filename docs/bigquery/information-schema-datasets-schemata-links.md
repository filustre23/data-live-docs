* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# SCHEMATA\_LINKS 檢視畫面

`INFORMATION_SCHEMA.SCHEMATA_LINKS` 檢視畫面會為每個透過 BigQuery 共用的[連結資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)提供一列資料。這個檢視畫面也會顯示透過[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)共用的專案中，個別的資源 (例如資料表或檢視區塊)。這個檢視畫面會為連結資料集中的每個資源顯示一行。

## 必要權限

如要查詢 `INFORMATION_SCHEMA.SCHEMATA_LINKS` 檢視畫面，您必須具備專案層級的 `bigquery.datasets.get` Identity and Access Management (IAM) 權限。

下列預先定義的 IAM 角色都包含查詢 `INFORMATION_SCHEMA.SCHEMATA_LINKS` 檢視畫面所需的權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataViewer`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

`INFORMATION_SCHEMA.SCHEMATA_LINKS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `catalog_name` | `STRING` | 來源資料集所屬專案的名稱。 |
| `schema_name` | `STRING` | 來源資料集的名稱。資料集名稱也稱為 `datasetId`。 |
| `linked_schema_catalog_number` | `STRING` | 含有連結資料集的專案編號。 |
| `linked_schema_catalog_name` | `STRING` | 包含連結資料集的專案名稱。 |
| `linked_schema_name` | `STRING` | 連結資料集的名稱。資料集名稱也稱為 `datasetId`。 |
| `linked_schema_creation_time` | `TIMESTAMP` | 連結資料集的建立時間。 |
| `linked_schema_org_display_name` | `STRING` | 建立連結資料集的機構顯示名稱。 |
| `shared_asset_id` | `STRING` | 透過資料無塵室共用的資產 ID。如果 `link_type` 為 `REGULAR`，這個值為 `null`。 |
| `link_type` | `STRING` | 連結資料集的類型。可能的值為 `REGULAR` 或 `DCR` (資料無塵室)。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如果未指定區域限定符，系統會從美國地區擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]INFORMATION_SCHEMA.SCHEMATA_LINKS` | 專案層級 | 美國區域 |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.SCHEMATA_LINKS `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 範例

本節列出查詢 `INFORMATION_SCHEMA.SCHEMATA_LINKS` 檢視區塊的範例。

**範例：列出與其他專案連結的所有資料集**

以下範例會列出 `EU` 多地區中，與名為 `otherproject` 的其他專案連結的所有資料集：

```
SELECT * FROM `otherproject`.`region-eu`.INFORMATION_SCHEMA.SCHEMATA_LINKS;
```

輸出結果大致如下。系統會省略某些資料欄，以便簡化輸出結果。

```
+---------------------+----------------+----------------------------+------------------------------+--------------------+--------------------------------+-----------------------------+-----------------+-----------+
|    catalog_name    |  schema_name    | linked_schema_catalog_name | linked_schema_catalog_number | linked_schema_name | linked_schema_org_display_name | linked_schema_creation_time | shared_asset_id | link_type |
+---------------------+----------------+----------------------------+------------------------------+--------------------+--------------------------------+-----------------------------+-----------------+-----------+
|  otherproject      | source_dataset  | subscriptioproject1        |                974999999291  | linked_dataset     |  subscriptionorg1              |         2025-08-07 05:02:27 | NULL            | REGULAR   |
|  otherproject      | source_dataset1 | subscriptionproject2       |                974999999292  | test_dcr           |  subscriptionorg2              |         2025-08-07 10:08:50 | test_table      | DCR       |
+---------------------+----------------+----------------------------+------------------------------+--------------------+--------------------------------+-----------------------------+-----------------+-----------+
```

**範例：列出共用資料集的所有連結資料集**

以下範例會列出 `US` 多地區中，名為 `sharedataset` 的共用資料集連結的所有資料集：

```
SELECT * FROM INFORMATION_SCHEMA.SCHEMATA_LINKS WHERE schema_name = 'sharedataset';
```

輸出結果大致如下。系統會省略某些資料欄，以便簡化輸出結果。

```
+---------------------+----------------+----------------------------+------------------------------+--------------------+--------------------------------+-----------------------------+-----------------+-----------+
|    catalog_name     |  schema_name   | linked_schema_catalog_name | linked_schema_catalog_number | linked_schema_name | linked_schema_org_display_name | linked_schema_creation_time | shared_asset_id | link_type |
+---------------------+----------------+----------------------------+------------------------------+--------------------+--------------------------------+-----------------------------+-----------------+-----------+
|  myproject          | sharedataset   | subscriptionproject1       |                974999999291  | linked_dataset     |  subscriptionorg1              |         2025-08-07 05:02:27 | NULL            | REGULAR   |
|  myproject          | sharedataset   | subscriptionproject2       |                974999999292  | test_dcr           |  subscriptionorg2              |         2025-08-07 10:08:50 | test_table      | DCR       |
+---------------------+----------------+----------------------------+------------------------------+--------------------+--------------------------------+-----------------------------+-----------------+-----------+
```

**範例：列出使用資料無塵室共用的所有資源**

以下範例列出所有個別資源 (例如資料表或檢視區塊)，這些資源是使用資料淨室從 `EU` 多區域中的另一個專案 (名為 `otherproject`) 共用：

```
SELECT * FROM `otherproject`.`region-eu`.INFORMATION_SCHEMA.SCHEMATA_LINKS where link_type='DCR';
```

輸出結果大致如下。系統會省略某些資料欄，以便簡化輸出結果。

```
+---------------------+----------------+----------------------------+------------------------------+--------------------+--------------------------------+-----------------------------+-----------------+-----------+
|    catalog_name     |  schema_name   | linked_schema_catalog_name | linked_schema_catalog_number | linked_schema_name | linked_schema_org_display_name | linked_schema_creation_time | shared_asset_id | link_type |
+---------------------+----------------+----------------------------+------------------------------+--------------------+--------------------------------+-----------------------------+-----------------+-----------+
|  otherproject       | sharedataset1  | subscriptionproject1       |                 974999999291 | test_dcr1          |  subscriptionorg1              |         2025-08-07 05:02:27 | test_view       | DCR       |
|  otherproject       | sharedataset2  | subscriptionproject2       |                 974999999292 | test_dcr2          |  subscriptionorg2              |         2025-08-07 10:08:50 | test_table      | DCR       |
+---------------------+----------------+----------------------------+------------------------------+--------------------+--------------------------------+-----------------------------+-----------------+-----------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]