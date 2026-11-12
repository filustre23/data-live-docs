Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立資料表快照

本文說明如何使用Google Cloud 控制台、[`CREATE SNAPSHOT TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_snapshot_table_statement) SQL 陳述式、[`bq cp --snapshot`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 指令或 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 建立資料表快照。本文適用於熟悉 BigQuery [資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)的使用者。

## 權限與角色

本節說明建立資料表快照所需的 [Identity and Access Management (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，以及授予這些權限的[預先定義 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。

### 權限

如要建立資料表快照，您必須具備下列權限：

| **權限** | **資源** | **注意事項** |
| --- | --- | --- |
| 符合下列所有條件：   `bigquery.tables.get`  `bigquery.tables.getData`  `bigquery.tables.createSnapshot`  `bigquery.datasets.get`  `bigquery.jobs.create` | 要建立快照的資料表。 | 由於快照到期後會刪除快照，因此您必須具備 `bigquery.tables.deleteSnapshot` 權限，才能建立有到期時間的快照。 |
| `bigquery.tables.create`  `bigquery.tables.updateData` | 包含資料表快照的資料集。 |  |

### 角色

提供必要權限的預先定義 BigQuery 角色如下：

| **角色** | **資源** | **注意事項** |
| --- | --- | --- |
| 至少以下其中一項：   `bigquery.dataViewer`  `bigquery.dataEditor`  `bigquery.dataOwner`   另須滿足下列其中一項條件：   `bigquery.jobUser`  `bigquery.studioUser`  `bigquery.user`  `bigquery.studioAdmin`  `bigquery.admin` | 要建立快照的資料表。 | 只有 `bigquery.dataOwner`、`bigquery.admin` 和 `bigquery.studioAdmin` 可用於建立具有到期時間的快照。 |
| 至少符合下列其中一項條件：   `bigquery.dataEditor`  `bigquery.dataOwner`  `bigquery.studioAdmin`  `bigquery.admin` | 包含新資料表快照的資料集。 |  |

## 限制

如要瞭解資料表快照限制，請參閱「[資料表快照限制](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw#limitations)」。

此外，建立資料表快照時須遵守下列限制，這些限制適用於所有[資料表複製工作](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#limitations_on_copying_tables)：

* 建立資料表快照時，名稱必須遵守與建立資料表時相同的[命名規則](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#table_naming)。
* 建立資料表快照時，須遵守 BigQuery 對複製工作的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)。
* 資料表快照資料集必須與要建立快照的資料表資料集位於相同的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)和[組織](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw)。舉例來說，如果資料表位於歐盟境內的資料集，您就無法在美國境內的資料集建立資料表快照。請改為建立資料表副本。
* BigQuery 建立資料表快照所需的時間，可能會因基礎儲存空間是動態管理，而有顯著差異。
* 使用 BigQuery CLI 建立資料表快照時，快照會採用目的地資料集的預設加密金鑰。使用 SQL 建立資料表快照時，快照會與來源資料表使用相同的加密金鑰。

## 建立資料表快照

最佳做法是在與基礎資料表不同的資料集中建立資料表快照。這樣一來，即使基礎資料表的資料集不小心遭到刪除，也能從資料表快照還原基礎資料表。

建立資料表快照時，您必須指定要建立快照的資料表，以及資料表快照的專屬名稱。您可以視需要指定快照的[時間](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)和資料表快照的[到期時間](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#updating_a_tables_expiration_time)。

### 建立有到期時間的資料表快照

您可以透過下列任一選項，建立 24 小時後到期的資料表快照：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
4. 依序點選**「Overview」(總覽) >「Tables」(資料表)**，然後點選要建立快照的
   資料表名稱。
5. 在詳細資料窗格中，依序點選**「更多」>「建立快照」**。
6. 在隨即顯示的「Create table snapshot」(建立資料表快照) 窗格中，輸入新資料表快照的「Project」(專案)、「Dataset」(資料集) 和「Table」(資料表) 資訊。
7. 在「Expiration time」(到期時間) 欄位中，輸入從現在起 24 小時後的日期和時間。
8. 按一下「儲存」。

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

   替換下列內容：

   * `SNAPSHOT_PROJECT_ID`：要建立快照的專案 ID。
   * `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
   * `SNAPSHOT_NAME`：要建立的快照名稱。
   * `TABLE_PROJECT_ID`：專案 ID，用於存放您要建立快照的資料表。
   * `TABLE_DATASET_NAME`：資料集名稱，其中包含您要建立快照的資料表。
   * `TABLE_NAME`：要建立快照的資料表名稱。
   * `TIMESTAMP_VALUE`：[時間戳記值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type)，代表 24 小時後的日期和時間。
3. 按一下「play\_circle 執行」。

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

替換下列內容：

* `TABLE_PROJECT_ID`：專案 ID，用於存放您要建立快照的資料表。
* `TABLE_DATASET_NAME`：資料集名稱，其中包含您要建立快照的資料表。
* `TABLE_NAME`：要建立快照的資料表名稱。
* `SNAPSHOT_PROJECT_ID`：要建立快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
* `SNAPSHOT_NAME`：要建立的快照名稱。

必須使用 `--no_clobber` 旗標。

**注意：** 快照會沿用目的地資料集的預設加密金鑰。

### API

使用下列參數呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 這項作業的計費專案 ID。 |
| 要求主體 | ``` {   "configuration": {     "copy": {       "sourceTables": [         {           "projectId": "TABLE_PROJECT_ID",           "datasetId": "TABLE_DATASET_NAME",           "tableId": "TABLE_NAME"         }       ],       "destinationTable": {         "projectId": "SNAPSHOT_PROJECT_ID",         "datasetId": "SNAPSHOT_DATASET_NAME",         "tableId": "SNAPSHOT_NAME"       },       "operationType": "SNAPSHOT",       "writeDisposition": "WRITE_EMPTY",       "destinationExpirationTime":"TIMESTAMP_VALUE"     }   } } ``` |

替換下列內容：

* `TABLE_PROJECT_ID`：專案 ID，用於存放您要建立快照的資料表。
* `TABLE_DATASET_NAME`：資料集名稱，其中包含您要建立快照的資料表。
* `TABLE_NAME`：要建立快照的資料表名稱。
* `SNAPSHOT_PROJECT_ID`：要建立快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
* `SNAPSHOT_NAME`：要建立的快照名稱。
* `TIMESTAMP_VALUE`：[時間戳記值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type)，代表 24 小時後的日期和時間。

與資料表一樣，如果未指定到期時間，資料表快照會在[預設資料表到期時間](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#updating_a_tables_expiration_time)或包含資料表快照的資料集到期後失效。

**注意：** 由於快照到期等同於在稍後刪除快照，因此建立具有到期時間的快照需要 `bigquery.tables.deleteSnapshot` 權限。

### 使用時間旅行功能建立資料表快照

您可以使用下列任一選項，建立一小時前的資料表快照：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
4. 依序點選**「Overview」(總覽) >「Tables」(資料表)**，然後點選
   要建立快照的資料表名稱。
5. 在詳細資料窗格中，依序點選**「更多」>「建立快照」**。
6. 在隨即顯示的「Create table snapshot」(建立資料表快照) 窗格中，輸入新資料表快照的「Project」(專案)、「Dataset」(資料集) 和「Table」(資料表) 資訊。
7. 在「Snapshot time」(快照時間) 欄位中，輸入 1 小時前的日期和時間。
8. 按一下「儲存」。

### SQL

使用 [`CREATE SNAPSHOT TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_snapshot_table_statement)和 [`FOR SYSTEM_TIME AS OF` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE SNAPSHOT TABLE SNAPSHOT_PROJECT_ID.SNAPSHOT_DATASET_NAME.SNAPSHOT_NAME
   CLONE TABLE_PROJECT_ID.TABLE_DATASET_NAME.TABLE_NAME
   FOR SYSTEM_TIME AS OF
     TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);
   ```

   替換下列內容：

   * `SNAPSHOT_PROJECT_ID`：要建立快照的專案 ID。
   * `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
   * `SNAPSHOT_NAME`：要建立的快照名稱。
   * `TABLE_PROJECT_ID`：專案 ID，用於存放您要建立快照的資料表。
   * `TABLE_DATASET_NAME`：資料集名稱，其中包含您要建立快照的資料表。
   * `TABLE_NAME`：要建立快照的資料表名稱。
3. 按一下「play\_circle 執行」。

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

替換下列內容：

* `TABLE_PROJECT_ID`：專案 ID，用於存放您要建立快照的資料表。
* `TABLE_DATASET_NAME`：資料集名稱，其中包含您要建立快照的資料表。
* `TABLE_NAME`：要建立快照的資料表名稱。
* `SNAPSHOT_PROJECT_ID`：要建立快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
* `SNAPSHOT_NAME`：要建立的快照名稱。

必須使用 `--no_clobber` 旗標。

### API

使用下列參數呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 這項作業的計費專案 ID。 |
| 要求主體 | ``` {   "configuration": {     "copy": {       "sourceTables": [         {           "projectId": "TABLE_PROJECT_ID",           "datasetId": "TABLE_DATASET_NAME",           "tableId": "TABLE_NAME@-360000"         }       ],       "destinationTable": {         "projectId": "SNAPSHOT_PROJECT_ID",         "datasetId": "SNAPSHOT_DATASET_NAME",         "tableId": "SNAPSHOT_NAME"       },       "operationType": "SNAPSHOT",       "writeDisposition": "WRITE_EMPTY"     }   } } ``` |

替換下列內容：

* `TABLE_PROJECT_ID`：專案 ID，用於存放您要建立快照的資料表。
* `TABLE_DATASET_NAME`：資料集名稱，其中包含您要建立快照的資料表。
* `TABLE_NAME`：要建立快照的資料表名稱。
* `SNAPSHOT_PROJECT_ID`：要建立快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：要在其中建立快照的資料集名稱。
* `SNAPSHOT_NAME`：要建立的快照名稱。

如要進一步瞭解如何指定資料表的過往版本，請參閱「[使用時間旅行功能存取歷來資料](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)」。

## 資料表存取控管

如要控管 BigQuery 資料表的存取權，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

建立資料表快照時，資料表快照的[資料表層級存取權](https://docs.cloud.google.com/bigquery/docs/table-access-controls-intro?hl=zh-tw)設定如下：

* 如果資料表快照覆寫現有資料表，則會保留現有資料表的資料表層級存取權。[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)不會從基礎資料表複製。
* 如果資料表快照是新資源，則資料表快照的資料表層級存取權，取決於建立資料表快照的資料集存取權政策。此外，[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)會從基礎資料表複製到資料表快照。

## 後續步驟

* [更新資料表快照的說明、到期日或存取權政策](https://docs.cloud.google.com/bigquery/docs/table-snapshots-update?hl=zh-tw)。
* [還原資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-restore?hl=zh-tw)。
* [使用執行排定查詢的服務帳戶，建立資料表的每月快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-scheduled?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]