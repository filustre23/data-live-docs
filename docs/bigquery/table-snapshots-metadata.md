* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查看資料表快照中繼資料

本文說明如何透過 Google Cloud 控制台、查詢`INFORMATION_SCHEMA` 資料表的 [`TABLE_SNAPSHOTS`](https://docs.cloud.google.com/bigquery/docs/information-schema-snapshots?hl=zh-tw) 檢視畫面、使用 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令，或呼叫 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) API，查看 BigQuery 資料表快照的中繼資料。適合熟悉 BigQuery[資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)和[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)的使用者。

## 權限與角色

本節說明查看資料表快照中繼資料所需的[身分與存取權管理 (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，以及授予這些權限的[預先定義 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。

### 權限

如要查看資料表快照的中繼資料，您必須具備下列權限：

| **權限** | **資源** |
| --- | --- |
| `bigquery.tables.get` | 資料表快照 |

### 角色

提供必要權限的預先定義 BigQuery 角色如下：

| **角色** | **資源** |
| --- | --- |
| 下列任一項：   `bigquery.metadataViewer`  `bigquery.dataViewer`  `bigquery.dataEditor`  `bigquery.dataOwner`  `bigquery.admin` | 資料表快照 |

## 取得資料表快照的中繼資料

資料表快照的中繼資料與標準資料表的中繼資料類似，但有以下差異：

* 額外的 `baseTableReference` 欄位會識別快照的來源基本資料表。
* `type` 欄位的值為 `SNAPSHOT`。

您可以透過下列任一方式查看資料表快照的中繼資料：

### 主控台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「Explorer」explore：

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下含有資料表快照的資料集。
4. 依序點選「總覽」**>「資料表」**，然後按一下資料表快照的名稱。
5. 在隨即顯示的快照窗格中，您可以執行下列操作：

   * 按一下「結構定義」分頁標籤，查看資料表快照的結構定義和政策標記。
   * 按一下「詳細資料」表格，查看表格快照的大小、到期時間、基本表格、快照時間和其他資訊。

### SQL

如要查看資料表快照的中繼資料，請查詢 [`INFORMATION_SCHEMA.TABLE_SNAPSHOTS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-snapshots?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     *
   FROM
     PROJECT_ID.DATASET_NAME.INFORMATION_SCHEMA.TABLE_SNAPSHOTS
   WHERE
     table_name = 'SNAPSHOT_NAME';
   ```

   請替換下列項目：

   * `PROJECT_ID`：包含快照的專案 ID。
   * `DATASET_NAME`：包含快照的資料集名稱。
   * `SNAPSHOT_NAME`：快照的名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

在 Cloud Shell 中輸入下列指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq show \
--format=prettyjson \
PROJECT_ID:DATASET_NAME.SNAPSHOT_NAME
```

請替換下列項目：

* `PROJECT_ID`：包含快照的專案 ID。
* `DATASET_NAME`：包含快照的資料集名稱。
* `SNAPSHOT_NAME`：快照的名稱。

輸出結果會與下列內容相似：

```
{
  "creationTime": "1593194331936",
   ...
  "snapshotDefinition": {
    "baseTableReference": {
      "datasetId": "myDataset",
      "projectId": "myProject",
      "tableId": "mytable"
    },
    "snapshotTime": "2020-06-26T17:58:50.815Z"
  },
  "tableReference": {
    "datasetId": "otherDataset",
    "projectId": "myProject",
    "tableId": "mySnapshot"
  },
  "type": "SNAPSHOT"
}
```

### API

使用下列參數呼叫 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 包含快照的專案 ID。 |
| `datasetId` | 包含快照的資料集名稱。 |
| `tableId` | 快照名稱。 |

回應主體類似於下列內容：

```
{
  "kind": "bigquery#table",
  "etag": "...",
  "id": "myProject:myDataset.mySnapshot",
  "selfLink": "https://content-bigquery.googleapis.com/bigquery/v2/projects/myProject/datasets/myDataset/tables/mySnapshot",
  "tableReference": {
    "projectId": "myProject",
    "datasetId": "myDataset",
    "tableId": "mySnapshot"
  },
  "description": "...",
  "schema": {
    "fields": [
      ...
    ]
  },
  "numBytes": "637931",
  "numLongTermBytes": "0",
  "numRows": "33266",
  "creationTime": "1593194331936",
  "lastModifiedTime": "1593194331936",
  "type": "SNAPSHOT",
  "location": "US",
  "snapshotDefinition": {
    "baseTableReference": {
      "projectId": "myProject",
      "datasetId": "otherDataset",
      "tableId": "myTable"
    },
    "snapshotTime": "2020-06-26T17:58:50.815Z"
  }
}
```

## 後續步驟

* [更新資料表快照的說明、到期日或存取政策](https://docs.cloud.google.com/bigquery/docs/table-snapshots-update?hl=zh-tw)。
* [刪除資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-delete?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]