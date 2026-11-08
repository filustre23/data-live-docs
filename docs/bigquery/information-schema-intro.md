Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# INFORMATION\_SCHEMA 簡介

BigQuery `INFORMATION_SCHEMA` 檢視表可讓您擷取 BigQuery 物件的中繼資料。您可以查詢這些唯讀、系統定義的檢視表，分析資料集、工作和存取控管等資源。

在 BigQuery 中，您可以使用 GoogleSQL 查詢 `INFORMATION_SCHEMA` 檢視表，方法是指定範圍和檢視表。例如，如要取得資料集中資料表的中繼資料，請指定 `myDataset.INFORMATION_SCHEMA.TABLES`。

下表列出可用的檢視畫面：

| 資源類型 | INFORMATION\_SCHEMA 檢視表 |
| --- | --- |
| 存取控管 | `OBJECT_PRIVILEGESscience` |
| BI Engine | `BI_CAPACITIES`  `BI_CAPACITY_CHANGES` |
| 設定 | `EFFECTIVE_PROJECT_OPTIONS`  `ORGANIZATION_OPTIONS`  `ORGANIZATION_OPTIONS_CHANGES`  `PROJECT_OPTIONS`  `PROJECT_OPTIONS_CHANGES` |
| 資料集 | `SCHEMATA  SCHEMATA_LINKS  SCHEMATA_OPTIONS  SHARED_DATASET_USAGE  SCHEMATA_REPLICAS  SCHEMATA_REPLICAS_BY_FAILOVER_RESERVATION` |
| 圖表 | `PROPERTY_GRAPHS` |
| 工作 | `JOBS_BY_PROJECT†`  `JOBS_BY_USER`  `JOBS_BY_FOLDER`  `JOBS_BY_ORGANIZATION` |
| 依時間片段劃分的工作 | `JOBS_TIMELINE_BY_PROJECT†`  `JOBS_TIMELINE_BY_USER`  `JOBS_TIMELINE_BY_FOLDER`  `JOBS_TIMELINE_BY_ORGANIZATION` |
| 最佳化建議和洞察 | `INSIGHTSscience`  `RECOMMENDATIONSscience`  `RECOMMENDATIONS_BY_ORGANIZATIONscience` |
| 預留項目 | `ASSIGNMENTS_BY_PROJECT†`  `ASSIGNMENT_CHANGES_BY_PROJECT†`  `CAPACITY_COMMITMENTS_BY_PROJECT†`  `CAPACITY_COMMITMENT_CHANGES_BY_PROJECT†`  `FAILOVER_HISTORY_BY_PROJECT†science`  `RESERVATIONS_BY_PROJECT†`  `RESERVATION_CHANGES_BY_PROJECT†`  `RESERVATIONS_TIMELINE_BY_PROJECT†` |
| 處理常式 | `PARAMETERS`  `ROUTINES`  `ROUTINE_OPTIONS` |
| 搜尋索引 | `SEARCH_INDEXES`  `SEARCH_INDEX_COLUMNS`  `SEARCH_INDEX_COLUMN_OPTIONSscience`  `SEARCH_INDEX_OPTIONS`  `SEARCH_INDEXES_BY_ORGANIZATION` |
| 工作階段 | `SESSIONS_BY_PROJECT†`  `SESSIONS_BY_USER` |
| 串流 | `STREAMING_TIMELINE_BY_PROJECT†`  `STREAMING_TIMELINE_BY_FOLDER`  `STREAMING_TIMELINE_BY_ORGANIZATION` |
| Tables | `COLUMNS`  `COLUMN_FIELD_PATHS`  `CONSTRAINT_COLUMN_USAGE`  `KEY_COLUMN_USAGE`  `PARTITIONSscience`  `TABLES`  `TABLE_OPTIONS`  `TABLE_CONSTRAINTS`  `TABLE_SNAPSHOTS`  `TABLE_STORAGE_BY_PROJECT†`  `TABLE_STORAGE_BY_FOLDER`  `TABLE_STORAGE_BY_ORGANIZATION`  `TABLE_STORAGE_USAGE_TIMELINEscience`  `TABLE_STORAGE_USAGE_TIMELINE_BY_FOLDERscience`  `TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATIONscience` |
| 向量索引 | `VECTOR_INDEXES`  `VECTOR_INDEX_COLUMNS`  `VECTOR_INDEX_OPTIONS` |
| 瀏覽次數 | `VIEWS`  `MATERIALIZED_VIEWS` |
| Write API | `WRITE_API_TIMELINE_BY_PROJECT†`  `WRITE_API_TIMELINE_BY_FOLDER`  `WRITE_API_TIMELINE_BY_ORGANIZATION` |

† 對於 `*BY_PROJECT` 檢視畫面，`BY_PROJECT` 後置字元為選用。例如，查詢 `INFORMATION_SCHEMA.JOBS_BY_PROJECT` 和 `INFORMATION_SCHEMA.JOBS` 會傳回相同的結果。

**注意：**[BigQuery Omni 系統資料表](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#limitations)不支援部分 `INFORMATION_SCHEMA` 檢視表。您可以使用 `INFORMATION_SCHEMA` 查看 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw#view_resource_metadata) 和 [Azure Storage](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw#view_resource_metadata_with_information_schema) 的資源中繼資料。

## 定價

如果專案採用隨選定價，即使查詢處理的位元組少於 10 MB，對 `INFORMATION_SCHEMA` 檢視表執行查詢仍會產生至少 10 MB 的資料處理費用。10 MB 是隨選查詢的最低計費量。詳情請參閱「[隨選定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)」。

如果專案採用以運算資源為基礎的定價模式，對`INFORMATION_SCHEMA`檢視表和資料表執行查詢時，會耗用您購買的 BigQuery 運算單元。詳情請參閱「[依用量計費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)」。

由於系統不會快取 `INFORMATION_SCHEMA` 查詢，因此每次執行 `INFORMATION_SCHEMA` 查詢時，即使查詢文字相同，您仍須付費。

系統不會收取 `INFORMATION_SCHEMA` 資料檢視的儲存費用。

## 語法

`INFORMATION_SCHEMA` 檢視表必須符合資料集或區域條件。

**注意：**您必須[指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)，才能查詢 `INFORMATION_SCHEMA` 檢視表。如果查詢執行位置與資料集或所用區域限定詞的位置不符，查詢 `INFORMATION_SCHEMA` 檢視表會失敗，並顯示下列錯誤：  

```
Table myproject: region-us.INFORMATION_SCHEMA.[VIEW] not found in location US
```

### 資料集限定詞

如果使用資料集限定詞，結果會限制在指定的資料集。例如：

```
-- Returns metadata for tables in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.TABLES;
```

下列 `INFORMATION_SCHEMA` 檢視表支援資料集限定詞：

* `COLUMNS`
* `COLUMN_FIELD_PATHS`
* `MATERIALIZED_VIEWS`
* `PARAMETERS`
* `PARTITIONS`
* `ROUTINES`
* `ROUTINE_OPTIONS`
* `TABLES`
* `TABLE_OPTIONS`
* `VIEWS`

### 區域限定詞

區域限定詞會以 `region-REGION` 語法表示。任何[資料集位置名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)都可用於 `REGION`。例如，下列區域限定詞有效：

* `region-us`
* `region-asia-east2`
* `region-europe-north1`

如有區域限定詞，結果會限制在指定位置。[區域限定詞](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#locations_and_regions)沒有階層關係，也就是說，歐盟多區域不包含 `europe-*` 區域，美國多區域也不包含 `us-*` 區域。舉例來說，下列查詢會傳回執行查詢的專案中，`US` 多區域內所有資料集的中繼資料，但不包含 `us-west1` 區域中的資料集：

```
-- Returns metadata for all datasets in the US multi-region.
SELECT * FROM region-us.INFORMATION_SCHEMA.SCHEMATA;
```

下列 `INFORMATION_SCHEMA` 檢視表不支援區域限定詞：

* [`INFORMATION_SCHEMA.PARTITIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-partitions?hl=zh-tw#scope_and_syntax)
* [`INFORMATION_SCHEMA.SEARCH_INDEXES`](https://docs.cloud.google.com/bigquery/docs/information-schema-indexes?hl=zh-tw#scope_and_syntax)
* [`INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS`](https://docs.cloud.google.com/bigquery/docs/information-schema-index-columns?hl=zh-tw)
* [`INFORMATION_SCHEMA.SEARCH_INDEX_OPTIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-index-options?hl=zh-tw)

如果未指定區域限定詞或資料集限定詞，系統會傳回錯誤。

針對限定區域的 `INFORMATION_SCHEMA` 檢視表執行查詢時，查詢會在您指定的區域中執行，也就是說，您無法透過單一查詢彙整不同區域檢視表的資料。如要合併多個區域的 `INFORMATION_SCHEMA` 檢視表，請在本機讀取並合併查詢結果，或將結果資料表[複製](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy_tables_across_regions)到共同區域。

### 專案限定詞

如果使用專案限定詞，結果會限制在指定專案。例如：

```
-- Returns metadata for the specified project and region.
SELECT * FROM myProject.`region-us`.INFORMATION_SCHEMA.TABLES;

-- Returns metadata for the specified project and dataset.
SELECT * FROM myProject.myDataset.INFORMATION_SCHEMA.TABLES;
```

所有 `INFORMATION_SCHEMA` 檢視畫面都支援專案限定詞。如未指定專案限定詞，檢視表會預設為執行查詢的專案。

為組織層級檢視畫面指定專案限定詞 (例如 `STREAMING_TIMELINE_BY_ORGANIZATION`) 不會影響結果。

## 限制

* BigQuery `INFORMATION_SCHEMA` 查詢必須採用 GoogleSQL 語法。`INFORMATION_SCHEMA` 並不支援舊版 SQL。
* `INFORMATION_SCHEMA` 查詢結果不會快取。
* `INFORMATION_SCHEMA` 檢視表無法用於 DDL 陳述式。
* `INFORMATION_SCHEMA` 檢視表不含[隱藏資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#hidden_datasets)的資訊。
* `INFORMATION_SCHEMA` 查詢若含有區域限定詞，可能會包含[在時間旅行期間內刪除的資料集](https://docs.cloud.google.com/bigquery/docs/restore-deleted-datasets?hl=zh-tw)中，該區域資源的中繼資料。
* 從 `INFORMATION_SCHEMA` 檢視表列出資源時，系統只會在上層檢查權限，不會在個別資料列層級檢查。因此，任何使用標記有條件指定個別資料列的[拒絕政策](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#deny_access_to_a_resource)都會遭到忽略。

## 後續步驟

* [取得資料表資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_table_information_using_information_schema)。
* [查看 Iceberg 代管資料表中繼資料](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw#view-iceberg-table-metadata-snapshot)。
* [查看圖表結構定義](https://docs.cloud.google.com/bigquery/docs/graph-schema-overview?hl=zh-tw#view_graph_schemas)。
* [監控工作](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)。
* [使用資訊結構定義排解問題](https://docs.cloud.google.com/bigquery/docs/info-schema-troubleshoot?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-04 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-04 (世界標準時間)。"],[],[]]