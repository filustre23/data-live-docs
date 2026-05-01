* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# TABLE\_SNAPSHOTS 檢視畫面

`INFORMATION_SCHEMA.TABLE_SNAPSHOTS` 檢視畫面包含資料表快照的中繼資料。詳情請參閱「[資料表快照簡介](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)」。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.TABLE_SNAPSHOTS` 檢視區塊，您需要資料集的 `bigquery.tables.list` Identity and Access Management (IAM) 權限。`roles/bigquery.metadataViewer` 預先定義的角色具備必要權限。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.TABLE_SNAPSHOTS` 資料表時，結果會針對指定資料集或區域中的每個資料表快照，分別列出一個相對應的資料列。

`INFORMATION_SCHEMA.TABLE_SNAPSHOTS` 資料表具有下列結構定義：擷取資料表快照的標準資料表稱為「基本資料表」。

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `table_catalog` | `STRING` | 包含資料表快照的專案名稱 |
| `table_schema` | `STRING` | 包含資料表快照的資料集名稱 |
| `table_name` | `STRING` | 資料表快照的名稱 |
| `base_table_catalog` | `STRING` | 包含基礎資料表的專案名稱 |
| `base_table_schema` | `STRING` | 包含基礎資料表的資料集名稱 |
| `base_table_name` | `STRING` | 基本資料表的名稱 |
| `snapshot_time` | `TIMESTAMP` | 建立資料表快照的時間 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含資料集或區域限定詞。如果是含有資料集限定符的查詢，您必須具備該資料集的權限。如要查詢含有區域限定符的資料，您必須具備專案權限。詳情請參閱「[語法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)」。下表說明這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [`PROJECT_ID`.]`region-REGION`.INFORMATION_SCHEMA.TABLE_SNAPSHOTS `` | 專案層級 | `REGION` |
| `` [`PROJECT_ID`.]DATASET_ID.INFORMATION_SCHEMA.TABLE_SNAPSHOTS `` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**示例**

```
-- Returns metadata for the table snapshots in the specified dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.TABLE_SNAPSHOTS;

-- Returns metadata for the table snapshots in the specified region.
SELECT * FROM `region-us`.INFORMATION_SCHEMA.TABLE_SNAPSHOTS;
```

## 範例

下列查詢會擷取 `mydataset` 資料集中的資料表快照中繼資料。在這個範例中，系統會顯示資料表快照 `myproject.mydataset.mytablesnapshot`，這是 2021 年 5 月 14 日世界標準時間中午 12 點從基本資料表 `myproject.mydataset.mytable` 擷取的快照。

```
SELECT *
FROM
  `myproject`.mydataset.INFORMATION_SCHEMA.TABLE_SNAPSHOTS;
```

結果大致如下：

```
+----------------+---------------+-----------------+--------------------+-------------------+-----------------+-----------------------------+
| table_catalog  | table_schema  | table_name      | base_table_catalog | base_table_schema | base_table_name | snapshot_time               |
+----------------+---------------+-----------------+----------------------------------------------------------------------------------------+
| myproject      | mydataset     | mytablesnapshot | myProject          | mydataset         | mytable         | 2021-05-14 12:00:00.000 UTC |
+----------------+---------------+-----------------+--------------------+-------------------+-----------------+-----------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]