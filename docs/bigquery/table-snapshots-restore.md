Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 還原資料表快照

本文說明如何使用 Google Cloud 主控台、`CREATE TABLE CLONE` 查詢、`bq cp` 指令或 `jobs.insert` API，從資料表快照建立可寫入的資料表。適合熟悉[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)的使用者。

## 權限與角色

本節說明從資料表快照建立可寫入資料表時，您需要具備的[身分與存取權管理 (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，以及授予這些權限的[預先定義 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。

### 權限

如要從資料表快照建立可寫入的資料表，您需要下列權限：

| **權限** | **資源** |
| --- | --- |
| 符合下列所有條件：   `bigquery.tables.get`  `bigquery.tables.getData`  `bigquery.tables.restoreSnapshot` | 要複製到可寫入資料表的資料表快照。 |
| `bigquery.tables.create` | 包含目的地資料表的資料集。 |

### 角色

提供必要權限的預先定義 BigQuery 角色如下：

| **角色** | **資源** |
| --- | --- |
| 下列任一項：   `bigquery.dataEditor`  `bigquery.dataOwner`  `bigquery.admin` | 要複製到可寫入資料表的資料表快照。 |
| 下列任一項：   `bigquery.dataEditor`  `bigquery.dataOwner`  `bigquery.admin` | 包含目的地資料表的資料集。 |

## 還原資料表快照

如要從快照建立可寫入的資料表，請指定要複製的資料表快照和目的地資料表。目的地資料表可以是新資料表，也可以用資料表快照覆寫現有資料表。

### 還原至新資料表

您可以透過下列任一方式，將資料表快照還原至新資料表：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後點選包含要還原資料表快照的資料集。
4. 依序點選「總覽」**>「資料表」**，然後按一下資料表快照的名稱。
5. 在隨即顯示的表格快照窗格中，按一下「更新」**還原**。
6. 在隨即顯示的「Restore snapshot」(還原快照) 窗格中，輸入新資料表的「Project」(專案)、「Dataset」(資料集) 和「Table」(資料表) 資訊。
7. 按一下 [儲存]。

### SQL

使用 [`CREATE TABLE CLONE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_clone_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE TABLE_PROJECT_ID.TABLE_DATASET_NAME.NEW_TABLE_NAME
   CLONE SNAPSHOT_PROJECT_ID.SNAPSHOT_DATASET_NAME.SNAPSHOT_NAME;
   ```

   請替換下列項目：

   * `TABLE_PROJECT_ID`：要在其中建立新資料表的專案 ID。
   * `TABLE_DATASET_NAME`：要在其中建立新資料表的資料集名稱。
   * `NEW_TABLE_NAME`：新資料表的名稱。
   * `SNAPSHOT_PROJECT_ID`：包含要還原快照的專案 ID。
   * `SNAPSHOT_DATASET_NAME`：包含要還原快照的資料集名稱。
   * `SNAPSHOT_NAME`：要還原的快照名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

在 Cloud Shell 中輸入下列指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq cp \
--restore \
--no_clobber \
SNAPSHOT_PROJECT_ID:SNAPSHOT_DATASET_NAME.SNAPSHOT_NAME \
TABLE_PROJECT_ID:TABLE_DATASET_NAME.NEW_TABLE_NAME
```

請替換下列項目：

* `SNAPSHOT_PROJECT_ID`：包含要還原快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：包含要還原快照的資料集名稱。
* `SNAPSHOT_NAME`：要還原的快照名稱。
* `TABLE_PROJECT_ID`：要在其中建立新資料表的專案 ID。
* `TABLE_DATASET_NAME`：要在其中建立新資料表的資料集名稱。
* `NEW_TABLE_NAME`：新資料表的名稱。

如果目的地資料表已存在，`--no_clobber` 旗標會指示指令失敗。

### API

使用下列參數呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 要為這項作業計費的專案 ID。 |
| 要求主體 | ``` {   "configuration": {     "copy": {       "sourceTables": [         {           "projectId": "SNAPSHOT_PROJECT_ID",           "datasetId": "SNAPSHOT_DATASET_NAME",           "tableId": "SNAPSHOT_NAME"         }       ],       "destinationTable": {         "projectId": "TABLE_PROJECT_ID",         "datasetId": "TABLE_DATASET_NAME",         "tableId": "NEW_TABLE_NAME"       },       "operationType": "RESTORE",       "writeDisposition": "WRITE_EMPTY"     }   } } ``` |

請替換下列項目：

* `SNAPSHOT_PROJECT_ID`：包含要還原快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：包含要還原快照的資料集名稱。
* `SNAPSHOT_NAME`：要還原的快照名稱。
* `TABLE_PROJECT_ID`：要在其中建立新資料表的專案 ID。
* `TABLE_DATASET_NAME`：要在其中建立新資料表的資料集名稱。
* `NEW_TABLE_NAME`：新資料表的名稱。

如未指定到期時間，目的地資料表會在包含該資料表的資料集預設到期時間過後失效。

### 覆寫現有資料表

您可以使用下列任一選項，以資料表快照覆寫現有資料表：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後點選包含要還原資料表快照的資料集。
4. 依序點選「總覽」**>「資料表」**，然後按一下資料表快照的名稱。
5. 在隨即顯示的表格快照窗格中，按一下「還原」。
6. 在隨即顯示的「還原快照」窗格中，輸入現有資料表的「專案」、「資料集」和「資料表」資訊。
7. 選取「覆寫資料表 (如有)」。
8. 按一下 [儲存]。

### SQL

使用 [`CREATE TABLE CLONE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_clone_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE OR REPLACE TABLE TABLE_PROJECT_ID.TABLE_DATASET_NAME.TABLE_NAME
   CLONE SNAPSHOT_PROJECT_ID.SNAPSHOT_DATASET_NAME.SNAPSHOT_NAME;
   ```

   請替換下列項目：

   * `TABLE_PROJECT_ID`：要在其中建立新資料表的專案 ID。
   * `TABLE_DATASET_NAME`：包含要覆寫資料表的資料集名稱。
   * `TABLE_NAME`：要覆寫的資料表名稱。
   * `SNAPSHOT_PROJECT_ID`：包含要還原快照的專案 ID。
   * `SNAPSHOT_DATASET_NAME`：包含要還原快照的資料集名稱。
   * `SNAPSHOT_NAME`：要還原的快照名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

在 Cloud Shell 中輸入下列指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq cp \
--restore \
--force \
SNAPSHOT_PROJECT_ID:SNAPSHOT_DATASET_NAME.SNAPSHOT_NAME \
TABLE_PROJECT_ID:TABLE_DATASET_NAME.TABLE_NAME
```

請替換下列項目：

* `SNAPSHOT_PROJECT_ID`：包含要還原快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：包含要還原快照的資料集名稱。
* `SNAPSHOT_NAME`：要還原的快照名稱。
* `TABLE_PROJECT_ID`：要在其中建立新資料表的專案 ID。
* `TABLE_DATASET_NAME`：包含要覆寫資料表的資料集名稱。
* `TABLE_NAME`：要覆寫的資料表名稱。

### API

使用下列參數呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 要為這項作業計費的專案 ID。 |
| 要求主體 | ``` {   "configuration": {     "copy": {       "sourceTables": [         {           "projectId": "SNAPSHOT_PROJECT_ID",           "datasetId": "SNAPSHOT_DATASET_NAME",           "tableId": "SNAPSHOT_NAME"         }       ],       "destinationTable": {         "projectId": "TABLE_PROJECT_ID",         "datasetId": "TABLE_DATASET_NAME",         "tableId": "TABLE_NAME"       },       "operationType": "RESTORE",       "writeDisposition": "WRITE_TRUNCATE"     }   } } ``` |

請替換下列項目：

* `SNAPSHOT_PROJECT_ID`：包含要還原快照的專案 ID。
* `SNAPSHOT_DATASET_NAME`：包含要還原快照的資料集名稱。
* `SNAPSHOT_NAME`：要還原的快照名稱。
* `TABLE_PROJECT_ID`：要在其中建立新資料表的專案 ID。
* `TABLE_DATASET_NAME`：包含要覆寫資料表的資料集名稱。
* `TABLE_NAME`：要覆寫的資料表名稱。

如未指定到期時間，目的地資料表會在包含該資料表的資料集預設到期時間過後失效。

## 後續步驟

* [列出指定基礎資料表的資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-list?hl=zh-tw#list_the_table_snapshots_of_a_specified_base_table)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]