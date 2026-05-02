* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 列出資料表快照

本文說明如何透過 Google Cloud 控制台、查詢 [`INFORMATION_SCHEMA.TABLE_SNAPSHOTS`](https://docs.cloud.google.com/bigquery/docs/information-schema-snapshots?hl=zh-tw) 資料表、使用 [`bq ls`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_ls) 指令，或呼叫 [`tables.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/list?hl=zh-tw) API，取得 BigQuery 資料集中的資料表快照清單。本文也會說明如何查詢 `INFORMATION_SCHEMA.TABLE_SNAPSHOTS` 資料表，列出指定主資料表的所有資料表快照。本文適用於熟悉 BigQuery[資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)和[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)的使用者。

## 權限與角色

本節說明在資料集中列出資料表快照所需的[身分與存取權管理 (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，以及授予這些權限的[預先定義 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。列出資料表快照所需的權限和角色，與[列出其他類型資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#list_tables_in_a_dataset)所需的權限和角色相同。

### 權限

如要列出資料集中的資料表快照，您需要下列權限：

| **權限** | **資源** |
| --- | --- |
| `bigquery.tables.list` | 包含資料表快照的資料集。 |

### 角色

提供必要權限的預先定義 BigQuery 角色如下：

| **角色** | **資源** |
| --- | --- |
| 下列任一項：   `bigquery.dataUser`  `bigquery.dataViewer`  `bigquery.dataEditor`  `bigquery.dataOwner`  `bigquery.admin` | 包含資料表快照的資料集。 |

## 列出資料集中的資料表快照

列出資料集中的資料表快照，與列出其他類型的資料表類似。資料表快照的類型為 `SNAPSHOT`。

您可以使用下列任一選項列出資料表快照：

### 主控台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「Explorer」explore：

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取包含要列出資料表快照的資料集。
4. 依序點選「總覽」**>「表格」**。如要從清單中找出快照，請查看「類型」欄中的 **`SNAPSHOT`** 值。

### SQL

查詢
[`INFORMATION_SCHEMA.TABLE_SNAPSHOTS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-snapshots?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     *
   FROM
     PROJECT_ID.DATASET_NAME.INFORMATION_SCHEMA.TABLE_SNAPSHOTS;
   ```

   請替換下列項目：

   * `PROJECT_ID`：專案 ID，用於存放您要列出的快照。
   * `DATASET_NAME`：包含您要列出快照的資料集名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

結果類似下方：

```
+---------------+----------------+------------------+--------------------+-------------------+-----------------+-----------------------------+
| table_catalog | table_schema   | table_name       | base_table_catalog | base_table_schema | base_table_name | snapshot_time               |
+---------------+----------------+------------------+--------------------+-------------------+-----------------+-----------------------------+
| myproject     | mydataset      | mysnapshot       | basetableproject   | basetabledataset           | basetable           | 2021-04-16 14:05:27.519 UTC |
+---------------+----------------+------------------+--------------------+-------------------+-----------------+-----------------------------+
```

### bq

在 Cloud Shell 中輸入下列指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq ls \
PROJECT_ID:DATASET_NAME
```

請替換下列項目：

* `PROJECT_ID`：專案 ID，用於存放您要列出的快照。
* `DATASET_NAME`：包含您要列出快照的資料集名稱。

輸出結果看起來與下列內容相似：

```
+-------------------------+--------+---------------------+-------------------+
|         tableId         |  Type  |       Labels        | Time Partitioning |
+-------------------------+--------+---------------------+-------------------+
| mysnapshot              |SNAPSHOT|                     |                   |
+-------------------------+--------+---------------------+-------------------+
```

### API

使用下列參數呼叫 [`tables.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/list?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 包含您要列出快照的專案 ID。 |
| `datasetId` | 包含您要列出快照的資料集名稱。 |

## 列出指定基本資料表的資料表快照

您可以查詢 `INFORMATION_SCHEMA.TABLE_SNAPSHOTS` 檢視區塊，列出指定基礎資料表的資料表快照：

```
SELECT
  *
FROM
  PROJECT_ID.DATASET_NAME.INFORMATION_SCHEMA.TABLE_SNAPSHOTS
WHERE
  base_table_name = 'books';
```

請替換下列項目：

* `PROJECT_ID`：專案 ID，用於存放您要列出的快照。
* `DATASET_NAME`：包含您要列出快照的資料集名稱。

## 後續步驟

* [取得資料表快照的相關資訊](https://docs.cloud.google.com/bigquery/docs/table-snapshots-metadata?hl=zh-tw)。
* [更新資料表快照的說明、到期日或存取政策](https://docs.cloud.google.com/bigquery/docs/table-snapshots-update?hl=zh-tw)。
* [刪除資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-delete?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]