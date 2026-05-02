* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立資料表快照

本文說明如何使用Google Cloud 控制台、[`CREATE SNAPSHOT TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_snapshot_table_statement) SQL 陳述式、[`bq cp --snapshot`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 指令或 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API，建立資料表的快照。本文適用於熟悉 BigQuery [資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)的使用者。

## 權限與角色

本節說明建立資料表快照所需的[身分與存取權管理 (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，以及授予這些權限的[預先定義 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。

### 權限

如要建立資料表快照，您必須具備下列權限：

| **權限** | **資源** | **注意事項** |
| --- | --- | --- |
| 符合下列所有條件：   `bigquery.tables.get`  `bigquery.tables.getData`  `bigquery.tables.createSnapshot`  `bigquery.datasets.get`  `bigquery.jobs.create` | 要建立快照的表格。 | 由於快照到期後會遭到刪除，因此如要建立設有到期時間的快照，您必須具備 `bigquery.tables.deleteSnapshot` 權限。 |
| `bigquery.tables.create`  `bigquery.tables.updateData` | 包含資料表快照的資料集。 |  |

### 角色

提供必要權限的預先定義 BigQuery 角色如下：

| **角色** | **資源** | **注意事項** |
| --- | --- | --- |
| 至少下列其中一項：   `bigquery.dataViewer`  `bigquery.dataEditor`  `bigquery.dataOwner`   至少下列其中一項：   `bigquery.jobUser`  `bigquery.studioUser`  `bigquery.user`  `bigquery.studioAdmin`  `bigquery.admin` | 要建立快照的表格。 | 只有 `bigquery.dataOwner`、`bigquery.admin` 和 `bigquery.studioAdmin` 可用於建立設有到期時間的快照。 |
| 至少以下其中一項：   `bigquery.dataEditor`  `bigquery.dataOwner`  `bigquery.studioAdmin`  `bigquery.admin` | 包含新資料表快照的資料集。 |  |

## 限制

如要瞭解資料表快照的限制，請參閱[資料表快照限制](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw#limitations)。

此外，建立資料表快照時有下列限制，適用於所有[資料表複製工作](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#limitations_on_copying_tables)：

* 建立資料表快照時，名稱必須遵循與建立資料表時相同的[命名規則](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#table_naming)。
* 建立資料表快照時，必須遵守 BigQuery 對複製工作的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)。
* 資料表快照資料集必須與要建立快照的資料表所屬資料集位於相同[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，且屬於相同[機構](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw)。舉例來說，您無法在位於美國的資料集中，為位於歐盟資料集的資料表建立資料表快照。您必須改為複製表格。
* BigQuery 建立資料表快照所需的時間可能會因執行作業而有顯著差異，因為基礎儲存空間是動態管理。
* 使用 BigQuery CLI 建立資料表快照時，快照會採用目的地資料集的預設加密金鑰。使用 SQL 建立資料表快照時，快照會與來源資料表使用相同的加密金鑰。

## 建立資料表快照

最佳做法是在與基本資料表不同的資料集內建立資料表快照。採用這種做法後，即使意外刪除基礎資料表的資料集，仍可從資料表快照還原基礎資料表。

建立資料表快照時，請指定要建立快照的資料表，以及資料表快照的專屬名稱。您可以視需要指定快照的[時間](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)和資料表快照的[到期時間](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#updating_a_tables_expiration_time)。

### 建立設有有效期限的資料表快照

您可以透過下列任一選項，建立 24 小時後過期的資料表快照：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
4. 依序點選「總覽」**>「表格」**，然後點選要建立快照的表格名稱。
5. 在隨即顯示的詳細資料窗格中，按一下「快照」。
6. 在隨即顯示的「建立資料表快照」窗格中，輸入新資料表快照的「專案」、「資料集」和「資料表」資訊。
7. 在「Expiration time」(到期時間) 欄位中，輸入從現在起 24 小時後的日期和時間。
8. 按一下 [儲存]。

### SQL

使用 [`CREATE SNAPSHOT TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_snapshot_table_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE SNAPSHOT TABLE SNAPSHOT_PROJECT_ID.SNAPSHOT_DATASET_NAME.SNAPSHOT_NAME
   CLONE TABLE_PROJECT_ID.TABLE_DATASET_NAME.TABLE_NAME
     OPTIONS (
       expiration_timestamp = TIMESTAMP 'TIMESTAMP_VALUE');
   ```

   請替換下列項目：

   * `SNAPSHOT_PROJECT_ID`：要在其中建立快照的專案 ID。
   * `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
   * `SNAPSHOT_NAME`：您要建立的快照名稱。
   * `TABLE_PROJECT_ID`：包含您要建立快照的表格的專案 ID。
   * `TABLE_DATASET_NAME`：包含要建立快照的資料表之資料集名稱。
   * `TABLE_NAME`：要建立快照的資料表名稱。
   * `TIMESTAMP_VALUE`：[時間戳記值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type)，代表 24 小時後的日期和時間。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

**注意：** 快照會沿用來源資料表的加密金鑰。

### bq

在 Cloud Shell 中輸入下列指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq cp \
--snapshot \
--no_clobber \
--expiration=86400 \
TABLE_PROJECT_ID:TABLE_DATASET_NAME.TABLE_NAME \
SNAPSHOT_PROJECT_ID:SNAPSHOT_DATASET_NAME.SNAPSHOT_NAME
```

請替換下列項目：

* `TABLE_PROJECT_ID`：包含您要建立快照的表格的專案 ID。
* `TABLE_DATASET_NAME`：包含要建立快照的資料表之資料集名稱。
* `TABLE_NAME`：要建立快照的資料表名稱。
* `SNAPSHOT_PROJECT_ID`：要在其中建立快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
* `SNAPSHOT_NAME`：您要建立的快照名稱。

`--no_clobber` 旗標為必要項目。

**注意：** 快照會沿用目標資料集的預設加密金鑰。

### API

使用下列參數呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 要為這項作業計費的專案 ID。 |
| 要求主體 | ``` {   "configuration": {     "copy": {       "sourceTables": [         {           "projectId": "TABLE_PROJECT_ID",           "datasetId": "TABLE_DATASET_NAME",           "tableId": "TABLE_NAME"         }       ],       "destinationTable": {         "projectId": "SNAPSHOT_PROJECT_ID",         "datasetId": "SNAPSHOT_DATASET_NAME",         "tableId": "SNAPSHOT_NAME"       },       "operationType": "SNAPSHOT",       "writeDisposition": "WRITE_EMPTY",       "destinationExpirationTime":"TIMESTAMP_VALUE"     }   } } ``` |

請替換下列項目：

* `TABLE_PROJECT_ID`：包含您要建立快照的表格的專案 ID。
* `TABLE_DATASET_NAME`：包含要建立快照的資料表之資料集名稱。
* `TABLE_NAME`：要建立快照的資料表名稱。
* `SNAPSHOT_PROJECT_ID`：要在其中建立快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
* `SNAPSHOT_NAME`：您要建立的快照名稱。
* `TIMESTAMP_VALUE`：[時間戳記值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type)，代表 24 小時後的日期和時間。

與資料表相同，如果未指定到期時間，資料表快照會在[預設資料表到期時間](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#updating_a_tables_expiration_time)或包含資料表快照的資料集到期後過期。

**注意：** 由於快照到期與稍後刪除快照相同，因此建立設有到期時間的快照需要 `bigquery.tables.deleteSnapshot` 權限。

### 使用時空旅行功能建立資料表快照

如要建立一小時前的資料表快照，請使用下列任一選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
4. 依序點選「總覽」**>「表格」**，然後點選要建立快照的表格名稱。
5. 在隨即顯示的詳細資料窗格中，按一下「快照」。
6. 在隨即顯示的「建立資料表快照」窗格中，輸入新資料表快照的「專案」、「資料集」和「資料表」資訊。
7. 在「Snapshot time」(快照時間) 欄位中，輸入 1 小時前的日期和時間。
8. 按一下 [儲存]。

### SQL

使用 [`FOR SYSTEM_TIME AS OF` 子句搭配 [`CREATE SNAPSHOT TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_snapshot_table_statement)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE SNAPSHOT TABLE SNAPSHOT_PROJECT_ID.SNAPSHOT_DATASET_NAME.SNAPSHOT_NAME
   CLONE TABLE_PROJECT_ID.TABLE_DATASET_NAME.TABLE_NAME
   FOR SYSTEM_TIME AS OF
     TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);
   ```

   請替換下列項目：

   * `SNAPSHOT_PROJECT_ID`：要在其中建立快照的專案 ID。
   * `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
   * `SNAPSHOT_NAME`：您要建立的快照名稱。
   * `TABLE_PROJECT_ID`：包含您要建立快照的表格的專案 ID。
   * `TABLE_DATASET_NAME`：包含要建立快照的資料表之資料集名稱。
   * `TABLE_NAME`：要建立快照的資料表名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

在 Cloud Shell 中輸入下列指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq cp \
--no_clobber \
--snapshot \
TABLE_PROJECT_ID:TABLE_DATASET_NAME.TABLE_NAME@-3600000 \
SNAPSHOT_PROJECT_ID:SNAPSHOT_DATASET_NAME.SNAPSHOT_NAME
```

請替換下列項目：

* `TABLE_PROJECT_ID`：包含您要建立快照的表格的專案 ID。
* `TABLE_DATASET_NAME`：包含要建立快照的資料表之資料集名稱。
* `TABLE_NAME`：要建立快照的資料表名稱。
* `SNAPSHOT_PROJECT_ID`：要在其中建立快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
* `SNAPSHOT_NAME`：您要建立的快照名稱。

`--no_clobber` 旗標為必要項目。

### API

使用下列參數呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 要為這項作業計費的專案 ID。 |
| 要求主體 | ``` {   "configuration": {     "copy": {       "sourceTables": [         {           "projectId": "TABLE_PROJECT_ID",           "datasetId": "TABLE_DATASET_NAME",           "tableId": "TABLE_NAME@-360000"         }       ],       "destinationTable": {         "projectId": "SNAPSHOT_PROJECT_ID",         "datasetId": "SNAPSHOT_DATASET_NAME",         "tableId": "SNAPSHOT_NAME"       },       "operationType": "SNAPSHOT",       "writeDisposition": "WRITE_EMPTY"     }   } } ``` |

請替換下列項目：

* `TABLE_PROJECT_ID`：包含您要建立快照的表格的專案 ID。
* `TABLE_DATASET_NAME`：包含要建立快照的資料表之資料集名稱。
* `TABLE_NAME`：要建立快照的資料表名稱。
* `SNAPSHOT_PROJECT_ID`：要在其中建立快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
* `SNAPSHOT_NAME`：您要建立的快照名稱。

如要進一步瞭解如何指定資料表的舊版本，請參閱「[使用時空旅行功能存取歷來資料](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)」。

## 資料表存取控管

如要控管 BigQuery 資料表的存取權，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

建立資料表快照時，系統會按照下列方式設定資料表快照的[資料表層級存取權](https://docs.cloud.google.com/bigquery/docs/table-access-controls-intro?hl=zh-tw)：

* 如果資料表快照覆寫現有資料表，系統會保留現有資料表的資料表層級存取權。系統不會從基本資料表複製[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)。
* 如果資料表快照是新資源，則資料表快照的資料表層級存取權，取決於建立資料表快照的資料集存取權政策。此外，[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)也會從基礎資料表複製到資料表快照。

## 後續步驟

* [更新資料表快照的說明、到期日或存取政策](https://docs.cloud.google.com/bigquery/docs/table-snapshots-update?hl=zh-tw)。
* [還原資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-restore?hl=zh-tw)。
* [使用服務帳戶執行排程查詢，每月建立資料表的快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-scheduled?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]