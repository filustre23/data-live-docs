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

本文說明如何使用 [`CREATE TABLE CLONE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_clone_statement) SQL 陳述式、[`bq cp`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 指令或 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 呼叫，將資料表複製到[資料表複本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)。本文件適用於熟悉[資料表複本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)的使用者。

## 權限與角色

本節說明建立資料表複本時所需的[身分與存取權管理 (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，以及授予這些權限的[預先定義 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。

### 權限

如要建立資料表複本，您必須具備下列權限：

| **權限** | **資源** |
| --- | --- |
| 以下所有項目：   `bigquery.tables.get`  `bigquery.tables.getData` | 要複製的表格。 |
| `bigquery.tables.create`  `bigquery.tables.updateData` | 包含資料表複本的資料集。 |

### 角色

提供必要權限的預先定義 BigQuery 角色如下：

| **角色** | **資源** |
| --- | --- |
| 下列任一項：   `bigquery.dataViewer`  `bigquery.dataEditor`  `bigquery.dataOwner`  `bigquery.admin` | 要複製的表格。 |
| 下列任一項：   `bigquery.dataEditor`  `bigquery.dataOwner`  `bigquery.admin` | 包含新表格複本的資料集。 |

## 建立表格複本

使用 GoogleSQL、bq 指令列工具或 BigQuery API 建立資料表複本。

### SQL

如要複製資料表，請使用 [CREATE TABLE CLONE](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_clone_statement) 陳述式。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入以下陳述式：

   ```
   CREATE TABLE
   myproject.myDataset_backup.myTableClone
   CLONE myproject.myDataset.myTable;
   ```
3. 按一下 play\_circle「Run」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」一文。

更改下列內容：

* `PROJECT` 是目標專案的專案 ID。這個專案必須與包含要複製的資料表的專案位於相同機構。
* `DATASET` 是目標資料集的名稱。這個資料集必須與包含要複製資料表的資料集位於同一個地區。
* `CLONE_NAME` 是您要建立的資料表複本名稱。

### bq

使用加上 `--clone` 旗標的 [`bq cp`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq cp --clone --no_clobber project1:myDataset.myTable PROJECT:DATASET.CLONE_NAME
```

更改下列內容：

* `PROJECT` 是目標專案的專案 ID。這個專案必須與包含要複製的資料表的專案位於相同機構。
* `DATASET` 是目標資料集的名稱。這個資料集必須與包含要複製資料表的資料集位於同一個地區。如果資料集與包含要複製資料表的資料集位於不同地區，系統會複製完整資料表。
* `CLONE_NAME` 是您要建立的資料表複本名稱。

必須使用 `--no_clobber` 旗標。

如果您要在與基礎資料表相同的專案中建立複本，可以略過指定專案，如下所示：

```
bq cp --clone --no_clobber myDataset.myTable DATASET.CLONE_NAME
```

### API

呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法，並將 `operationType` 欄位設為 `CLONE`：

| **參數** | **值** |
| --- | --- |
| `projectId` | 執行工作的專案專案 ID。 |
| 要求主體 | ``` {   "configuration": {     "copy": {       "sourceTables": [         {           "projectId": "myProject",           "datasetId": "myDataset",           "tableId": "myTable"         }       ],       "destinationTable": {         "projectId": "PROJECT",         "datasetId": "DATASET",         "tableId": "CLONE_NAME"       },       "operationType": "CLONE",       "writeDisposition": "WRITE_EMPTY",     }   } } ``` |

更改下列內容：

* `PROJECT` 是目標專案的專案 ID。這個專案必須與包含要複製的資料表的專案位於相同機構。
* `DATASET` 是目標資料集的名稱。這個資料集必須與包含要複製資料表的資料集位於同一個地區。如果資料集與包含要複製資料表的資料集位於不同地區，系統會複製完整的資料表。
* `CLONE_NAME` 是您要建立的資料表複本名稱。

## 存取權控管

建立表格複本時，系統會將表格複本的存取權設為以下方式：

* 將[資料列層級存取權政策](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)從基礎資料表複製到資料表複本。
* 系統會將[資料欄層級存取權政策](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)從基礎資料表複製到資料表複本。
* [資料表層級存取權](https://docs.cloud.google.com/bigquery/docs/table-access-controls-intro?hl=zh-tw)的判斷方式如下：

  + 如果資料表複本覆寫現有資料表，則現有資料表的資料表層級存取權會保留。系統不會從基本資料表複製[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)。
  + 如果資料表複本是新的資源，則資料表複本的資料表層級存取權，取決於建立資料表複本的資料集的存取權政策。此外，[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)會從基本資料表複製到資料表本機副本。

## 後續步驟

* 建立表格複本後，您可以像使用標準表格一樣使用該複本。詳情請參閱「[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]