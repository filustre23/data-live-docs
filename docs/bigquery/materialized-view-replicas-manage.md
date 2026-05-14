Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理具體化檢視表副本

本文說明如何在 BigQuery 中管理具體化檢視表副本。

BigQuery 管理具體化檢視表副本時，可執行下列作業：

* [列出具體化檢視表副本](#list)
* [取得具體化檢視副本的相關資訊](#get-info)
* [刪除具體化檢視表副本](#delete)

如要進一步瞭解具體化檢視區塊副本，請參閱下列內容：

* [具體化檢視表副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)
* [建立具體化檢視表副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#create)

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。執行工作所需的權限 (如有) 會列在工作的「必要權限」部分。

## 列出具體化檢視表副本

您可以透過 Google Cloud 控制台列出具體化檢視區塊副本。

### 所需權限

如要在資料集中列出具體化檢視表副本，您需要 `bigquery.tables.list` IAM 權限。

下列每個預先定義的 IAM 角色都包含必要權限，可在資料集中列出具體化檢視表副本：

* `roles/bigquery.user`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.admin`

如要進一步瞭解 IAM 中的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要列出資料集中的具體化檢視副本，請執行下列操作：

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
3. 依序點選「總覽」**>「表格」**。捲動清單來檢視該資料集中的資料表，資料表、檢視區塊和具體化檢視區塊在「類型」欄中會以不同值表示。具體化檢視表副本的值與具體化檢視表相同。

## 取得 materialized view 副本的相關資訊

您可以使用 SQL、bq 指令列工具或 BigQuery API，取得具體化檢視副本的相關資訊。

### 所需權限

如要查詢具體化檢視表副本的相關資訊，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.tables.get`
* `bigquery.tables.list`
* `bigquery.routines.get`
* `bigquery.routines.list`

下列每個預先定義的 IAM 角色都包含上述權限：

* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.admin`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要取得 materialized view 副本的相關資訊，包括來源 [materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)：

### SQL

如要取得具體化檢視表副本的相關資訊，請查詢 [`INFORMATION_SCHEMA.TABLES` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT * FROM PROJECT_ID.DATASET_ID.INFORMATION_SCHEMA.TABLES
   WHERE table_type = 'MATERIALIZED VIEW';
   ```

   請替換下列項目：

   * `PROJECT_ID`：包含具體化檢視副本的專案名稱
   * `DATASET_ID`：包含具體化檢視表副本的資料集名稱
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令：

```
bq show --project=project_id --format=prettyjson dataset.materialized_view_replica
```

更改下列內容：

* project\_id：專案 ID。如要取得預設專案以外專案中具體化檢視副本的相關資訊，只需加入這個旗標即可。
* dataset：包含具體化檢視表副本的資料集名稱。
* materialized\_view\_replica：要取得資訊的具體化檢視副本名稱。

範例：

輸入下列指令，即可顯示 `myproject` 專案中 `report_views` 資料集內具體化檢視表副本 `my_mv_replica` 的相關資訊。

```
bq show --project=myproject --format=prettyjson report_views.my_mv_replica
```

### API

如要使用 API 取得具體化檢視表副本資訊，請呼叫 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) 方法。

## 刪除具體化檢視表副本

您可以透過 Google Cloud 控制台刪除具體化檢視表副本。

**注意：** 刪除具體化檢視表副本後，即無法復原。

### 所需權限

如要刪除具體化檢視副本，您需要 `bigquery.tables.delete`IAM 權限。

下列預先定義的 IAM 角色都包含刪除 materialized view 副本所需的權限：

* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.admin`

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
3. 依序點選「Overview」**>「Tables」**，然後按一下 materialized view 副本。
4. 點選「刪除」。
5. 在「Delete materialized view?」(要刪除具體化檢視區塊嗎？) 對話方塊中，在欄位中輸入 `delete`，然後按一下「Delete」(刪除)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]