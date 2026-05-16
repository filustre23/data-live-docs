Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 刪除資料表快照

本文說明如何使用Google Cloud 主控台、[`DROP SNAPSHOT TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_snapshot_table_statement) GoogleSQL 陳述式、[`bq rm`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_rm) 指令或 BigQuery API [`tables.delete`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete?hl=zh-tw) 呼叫，刪除資料表快照。此外，本文也提供相關資訊，說明如何復原過去七天內刪除或過期的資料表快照。適合熟悉[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)的使用者。

## 權限與角色

本節說明刪除資料表快照所需的[身分與存取權管理 (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，以及授予這些權限的[預先定義 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。

### 權限

如要刪除資料表快照，您必須具備下列權限：

| **權限** | **資源** |
| --- | --- |
| `bigquery.tables.deleteSnapshot` | 要刪除的表格快照 |

### 角色

提供必要權限的預先定義 BigQuery 角色如下：

| **角色** | **資源** |
| --- | --- |
| 下列任一項：   `bigquery.dataOwner`  `bigquery.admin` | 要刪除的表格快照。 |

## 刪除資料表快照

刪除資料表快照的方式與刪除標準資料表相同。您不需要刪除過期的資料表快照。

您可以透過下列任一方式刪除資料表快照：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

[前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下含有資料表快照的資料集。
3. 依序點選「總覽」**>「資料表」**，然後按一下資料表快照的名稱。
4. 在隨即顯示的詳細資料窗格中，按一下「刪除」。
5. 在隨即顯示的對話方塊中輸入 `delete`，然後再次按一下「刪除」。

### SQL

使用 [`DROP SNAPSHOT TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_snapshot_table_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   DROP SNAPSHOT TABLE PROJECT_ID.DATASET_NAME.SNAPSHOT_NAME;
   ```

   請替換下列項目：

   * `PROJECT_ID`：包含快照的專案 ID。
   * `DATASET_NAME`：包含快照的資料集名稱。
   * `SNAPSHOT_NAME`：快照名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

在 Cloud Shell 中輸入下列指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq rm \
PROJECT_ID:DATASET_NAME.SNAPSHOT_NAME
```

請替換下列項目：

* `PROJECT_ID`：包含快照的專案 ID。
* `DATASET_NAME`：包含快照的資料集名稱。
* `SNAPSHOT_NAME`：快照名稱。

### API

使用下列參數呼叫 [`tables.delete`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 含有快照的專案 ID。 |
| `datasetId` | 包含快照的資料集名稱。 |
| `tableId` | 快照名稱。 |

## 還原已刪除或過期的資料表快照

您可以還原過去七天內刪除或過期的資料表快照，方法與還原標準資料表相同。詳情請參閱「[還原資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-restore?hl=zh-tw)」。

## 後續步驟

* [使用服務帳戶執行排程查詢，每月建立資料表的快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-scheduled?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]