Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立資料表本機副本

本文說明如何使用 [`CREATE TABLE CLONE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_clone_statement) SQL 陳述式、[`bq cp`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 指令或 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 呼叫，將資料表複製到[資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)。本文適用於熟悉[表格副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)的使用者。

## 權限與角色

本節說明建立資料表副本時所需的[Identity and Access Management (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，以及授予這些權限的[預先定義 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。

### 權限

如要建立資料表副本，您必須具備下列權限：

| **權限** | **資源** |
| --- | --- |
| 符合下列所有條件：   `bigquery.tables.get`  `bigquery.tables.getData` | 要複製的表格。 |
| `bigquery.tables.create`  `bigquery.tables.updateData` | 包含資料表副本的資料集。 |

### 角色

提供必要權限的預先定義 BigQuery 角色如下：

| **角色** | **資源** |
| --- | --- |
| 下列任一項：   `bigquery.dataViewer`  `bigquery.dataEditor`  `bigquery.dataOwner`  `bigquery.admin` | 要複製的表格。 |
| 下列任一項：   `bigquery.dataEditor`  `bigquery.dataOwner`  `bigquery.admin` | 包含新資料表副本的資料集。 |

## 建立資料表副本

使用 GoogleSQL、bq 指令列工具或 BigQuery API 建立資料表副本。

### SQL

如要複製資料表，請使用 [CREATE TABLE CLONE](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_clone_statement) 陳述式。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE
   myproject.myDataset_backup.myTableClone
   CLONE myproject.myDataset.myTable;
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

更改下列內容：

* `PROJECT` 是目標專案的專案 ID。
  這個專案必須與包含要複製資料表的專案位於同一個機構。
* `DATASET` 是目標資料集的名稱。
  這個資料集必須與包含要複製資料表的資料集位於同一個地區。
* `CLONE_NAME` 是您要建立的資料表副本名稱。

### bq

使用加上 `--clone` 旗標的 [`bq cp`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq cp --clone --no_clobber project1:myDataset.myTable PROJECT:DATASET.CLONE_NAME
```

更改下列內容：

* `PROJECT` 是目標專案的專案 ID。
  這個專案必須與包含要複製資料表的專案位於同一個機構。
* `DATASET` 是目標資料集的名稱。
  這個資料集必須與包含要複製資料表的資料集位於同一個地區。如果資料集與包含要複製資料表的資料集不在同一區域，系統會複製整個資料表。
* `CLONE_NAME` 是您要建立的資料表副本名稱。

`--no_clobber` 旗標為必要項目。

如要在與基礎資料表相同的專案中建立副本，可以略過指定專案，如下所示：

```
bq cp --clone --no_clobber myDataset.myTable DATASET.CLONE_NAME
```

### API

呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法，並將 `operationType` 欄位設為 `CLONE`：

| **參數** | **值** |
| --- | --- |
| `projectId` | 執行工作的專案 ID。 |
| 要求主體 | ``` {   "configuration": {     "copy": {       "sourceTables": [         {           "projectId": "myProject",           "datasetId": "myDataset",           "tableId": "myTable"         }       ],       "destinationTable": {         "projectId": "PROJECT",         "datasetId": "DATASET",         "tableId": "CLONE_NAME"       },       "operationType": "CLONE",       "writeDisposition": "WRITE_EMPTY",     }   } } ``` |

更改下列內容：

* `PROJECT` 是目標專案的專案 ID。
  這個專案必須與包含要複製資料表的專案位於同一個機構。
* `DATASET` 是目標資料集的名稱。
  這個資料集必須與包含要複製資料表的資料集位於同一個地區。如果資料集與包含要複製資料表的資料集不在同一區域，系統會複製整個資料表。
* `CLONE_NAME` 是您要建立的資料表副本名稱。

## 存取控管

建立資料表副本時，系統會依下列方式設定資料表副本的存取權：

* [資料列層級存取政策](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)會從基礎資料表複製到資料表副本。
* [資料欄層級存取權政策](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)
  會從基礎資料表複製到資料表副本。
* [資料表層級的存取權](https://docs.cloud.google.com/bigquery/docs/table-access-controls-intro?hl=zh-tw)取決於下列因素：

  + 如果資料表副本覆寫現有資料表，系統會保留現有資料表的資料表層級存取權。系統不會從基本資料表複製[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)。
  + 如果資料表副本是新資源，則資料表副本的資料表層級存取權，取決於建立資料表副本的資料集存取權政策。此外，[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)也會從基本資料表複製到資料表本機副本。

## 後續步驟

* 建立資料表副本後，您就可以像使用標準資料表一樣使用副本。
  詳情請參閱「[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]