Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理 materialized view 副本

本文說明如何在 BigQuery 管理 materialized view 副本。

BigQuery 對 materialized view 副本的管理作業包括：

* [列出 materialized view 副本](#list)
* [取得 materialized view 副本的相關資訊](#get-info)
* [刪除 materialized view 副本](#delete)

如要進一步瞭解 materialized view 副本，請參閱下列資源：

* [materialized view 副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)
* [建立 materialized view 副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#create)

## 事前準備

授予 Identity and Access Management (IAM) 角色，讓使用者具備執行本文件中各項工作所需的權限。執行工作所需的權限 (如有) 會列在工作的「必要權限」部分。

## 列出 materialized view 副本

您可以透過 Google Cloud 控制台列出 materialized view 副本。

### 所需權限

如要列出資料集中的 materialized view 副本，您必須具備 `bigquery.tables.list` IAM 權限。

下列各項預先定義的 IAM 角色，都包含列出資料集中 materialized view 副本所需的權限：

* `roles/bigquery.user`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.admin`

如要進一步瞭解 IAM 中的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要列出資料集中的 materialized view 副本，請按照下列步驟操作：

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
3. 依序點選**「總覽」>「表格」**。捲動清單，查看資料集中的資料表。資料表、檢視表和 materialized view 是透過「Type」(類型) 欄中的不同值來識別。materialized view 副本與 materialized view 具有相同價值。

## 取得 materialized view 副本的相關資訊

您可以使用 SQL、bq 指令列工具或 BigQuery API，取得 materialized view 副本的相關資訊。

### 所需權限

如要查詢 materialized view 副本的相關資訊，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.tables.get`
* `bigquery.tables.list`
* `bigquery.routines.get`
* `bigquery.routines.list`

下列各項預先定義的 IAM 角色均包含上述權限：

* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.admin`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要取得 materialized view 副本的資訊，包括來源 [materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)：

### SQL

如要取得 materialized view 副本的相關資訊，請查詢 [`INFORMATION_SCHEMA.TABLES` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT * FROM PROJECT_ID.DATASET_ID.INFORMATION_SCHEMA.TABLES
   WHERE table_type = 'MATERIALIZED VIEW';
   ```

   替換下列內容：

   * `PROJECT_ID`：materialized view 副本所在專案的名稱
   * `DATASET_ID`：包含 materialized view 副本的資料集名稱
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令：

```
bq show --project=project_id --format=prettyjson dataset.materialized_view_replica
```

更改下列內容：

* project\_id：專案 ID。只有在 materialized view 副本位於預設專案以外的專案時，才需要加入這個旗標，以取得副本資訊。
* dataset：包含
  具體化檢視副本的資料集名稱。
* materialized\_view\_replica：要查詢資訊的 materialized view 副本名稱。

範例：

輸入下列指令，顯示 `myproject` 專案中 `report_views` 資料集內 materialized view 副本 `my_mv_replica` 的資訊。

```
bq show --project=myproject --format=prettyjson report_views.my_mv_replica
```

### API

如要使用 API 取得 materialized view 副本資訊，請呼叫 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) 方法。

## 刪除 materialized view 副本

您可以透過 Google Cloud 控制台刪除 materialized view 副本。

**注意：** 刪除 materialized view 副本後即無法復原。

### 所需權限

如要刪除 materialized view 副本，您必須具備 `bigquery.tables.delete` IAM 權限。

下列各項預先定義的 IAM 角色，都包含刪除 materialized view 副本所需的權限：

* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.admin`

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
3. 依序點選**「總覽」>「資料表」**，然後點選具體化檢視表副本。
4. 在詳細資料窗格中，依序按一下**「更多」>「刪除」**。
5. 在「Delete materialized view?」(要刪除 materialized view 嗎？) 對話方塊中，在欄位輸入 `delete`，然後按一下「Delete」(刪除)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-01 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-01 (世界標準時間)。"],[],[]]