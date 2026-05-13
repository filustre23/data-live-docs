Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 預留 BI Engine 容量

建立預留項目即可購買 BI Engine 容量。
BI Engine 僅適用於支援版本的專案。
預留量以記憶體容量 (GiB) 為單位。保留項目會附加至您在建立保留項目時指定的專案和區域。BI Engine 會使用這項容量快取資料。如要瞭解 BI Engine 的預留空間大小上限，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#biengine-limits)」。

使用 BI Engine 時，系統會依據您為專案購買的 BI Engine 容量收費。系統會根據區域定價，以每 GiB/小時為單位收取 BI Engine 預留項目費用，詳情請參閱 [BI Engine 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bi_engine_pricing)。

**預留專案：** BI Engine 預留項目是由帳單專案的 ID 管理。購買預訂時，請務必指定報帳專案 ID 和用於查詢資料的區域。這不一定是包含資料集的專案。

## 必要的角色

如要取得建立及刪除預留項目所需的權限，請要求管理員授予專案的 [BigQuery 資源管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceAdmin)  (`roles/bigquery.resourceAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立預留項目

如要預留 BI Engine 的以量計價容量，請按照下列步驟操作：

### 控制台

1. 在 BigQuery 頁面的「管理」中，前往「BI Engine」頁面。

   [前往 BI Engine](https://console.cloud.google.com/bigquery/admin/bi-engine?hl=zh-tw)

   **注意：** 如果系統提示您啟用 **BigQuery Reservation API**，請點選「啟用」。
2. 按一下 add「建立預留項目」。
3. 在「建立預訂」頁面中，針對「步驟 1」執行下列操作：

   * 確認專案名稱。
   * 選擇你的所在位置。位置應與您要查詢的[資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)相符。
   * 調整滑桿，設定要保留的記憶體容量。
     以下範例將容量設為 2 GiB。目前上限為 250 GiB。您可以[要求提高](https://docs.google.com/forms/d/e/1FAIpQLSdkGV6kwVN_Wz34sjWF4wPofmGkTsPofRKGEth0M9JLpeZcUA/viewform?hl=zh-tw)專案的預留容量上限。大多數地區都可提高預訂上限，處理時間為 3 天到 1 週。
4. 點選「下一步」。
5. **偏好資料表** (選用)。[偏好資料表](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw#preferred_tables)：可將 BI Engine 加速功能限制在特定資料表。其他資料表則使用一般 BigQuery 運算單元。

   在「Table Id」欄位中，使用以下模式指定要加速的資料表：`PROJECT.DATASET.TABLE`。

   更改下列內容：

   * `PROJECT`：您的 Google Cloud 專案 ID
   * `DATASET`：資料集
   * `TABLE`：要加速的資料表
6. 點選「下一步」。
7. 在**步驟 3** 中，請檢查預訂詳細資料，然後按一下「建立」。

確認預訂後，詳細資料會顯示在「預訂」頁面。

### SQL

使用 [`ALTER BI_CAPACITY SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_bi_capacity_set_options_statement)建立或修改 BI Engine 預留項目。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER BI_CAPACITY `PROJECT_ID.LOCATION_ID.default`
   SET OPTIONS (
     size_gb = VALUE,
     preferred_tables =
       ['TABLE_PROJECT_ID.DATASET.TABLE1',
       'TABLE_PROJECT_ID.DATASET.TABLE2']);
   ```

   請替換下列項目：

   * `PROJECT_ID`：可選用的專案 ID，該專案將受益於 BI Engine 加速。如果省略此參數，系統會使用預設專案。
   * `LOCATION_ID`：需要快取資料的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)，並加上 `region-` 前置字元。例如：`region-us`、`region-us-central1`。
   * `VALUE`：BI Engine 容量預留大小 (以 GiB 為單位)，範圍為 1 到 250 GiB。`INT64`您可以[要求增加](https://docs.google.com/forms/d/e/1FAIpQLSdkGV6kwVN_Wz34sjWF4wPofmGkTsPofRKGEth0M9JLpeZcUA/viewform?hl=zh-tw)專案的預留容量上限。大多數地區都可提高預訂量，處理時間為 3 天到 1 週。設定 `VALUE` 會取代現有值 (如果有的話)，設為 `NULL` 則會清除該選項的值。
   * `TABLE_PROJECT_ID.DATASET.TABLE`：
     要套用加速功能的[偏好資料表](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw#preferred_tables)選用清單。格式：
     `TABLE_PROJECT_ID.DATASET.TABLE or
     DATASET.TABLE`. 如果省略專案，系統會使用預設專案。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)，並提供資料定義語言 (DDL) 陳述式做為查詢參數：

```
bq --project_id=PROJECT_ID update \
    --bi_reservation_size=SIZE \
    --location=LOCATION \
    --reservation
```

更改下列內容：

* `PROJECT_ID`：專案 ID
* `SIZE`：預留記憶體容量 (以 GiB 為單位)，範圍為 1 到 250 GiB。您可以[要求提高](https://docs.google.com/forms/d/e/1FAIpQLSdkGV6kwVN_Wz34sjWF4wPofmGkTsPofRKGEth0M9JLpeZcUA/viewform?hl=zh-tw)專案的預留容量上限。大多數地區都可提高預訂上限，處理時間為 3 天到 1 週。
* `LOCATION`：您要查詢的資料集位置

### 預估及評估容量

如要估算 BI Engine 預留容量的需求，請按照下列步驟操作：

1. 查看 [`TOTAL_LOGICAL_BYTES` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)，判斷資料表的邏輯大小，並將該大小用於初始 BI Engine 預留空間。例如：

   ```
   SELECT
     SUM(TOTAL_LOGICAL_BYTES) / 1024.0 / 1024.0 / 1024.0 AS logical_size_gb
   FROM
     `region-us.INFORMATION_SCHEMA.TABLE_STORAGE`
   WHERE
     TABLE_NAME IN UNNEST(["Table1", "Table2"]);
   ```

   舉例來說，如果查詢一組資料表，這些資料表總共含有 200 GiB 的資料，最佳做法是先預留 200 GiB 的 BI Engine 容量。如果查詢的選擇性較高，只會使用可用欄位或分區的子集，則可從較小的預留大小開始。
2. 執行所有需要最佳化的查詢，這些查詢必須與 BI Engine 預留項目位於相同專案和區域。目標是估算需要最佳化的工作負載。負載增加會導致處理查詢時需要更多記憶體。收到查詢後，資料會載入 BI Engine。
3. 比較 BI Engine RAM 保留項目與使用的位元組數，`reservation/used_bytes` 位於 [Cloud Monitoring `bigquerybiengine` 指標](https://docs.cloud.google.com/monitoring/api/metrics_gcp_a_b?hl=zh-tw#gcp-bigquerybiengine)中。
4. 根據結果調整預訂容量。在許多情況下，較小的預留項目可加快大多數查詢的速度，進而節省金錢和資源。如要進一步瞭解如何監控 BI Engine，請參閱「[BI Engine 監控](https://docs.cloud.google.com/bigquery/docs/bi-engine-monitor?hl=zh-tw)」。

下列因素會影響 BI Engine 預留項目大小：

* BI Engine 只會快取處理查詢時所需的常用資料欄和資料列。
* 預留容量用盡時，BI Engine 會嘗試卸載最久沒使用的資料，為新查詢釋出容量。
* 如果多個需要大量運算資源的查詢使用相同資料集，BI Engine 會載入額外的資料副本，重新分配資源並縮短回應時間。

## 修改預留項目

如要修改現有預訂，請完成下列步驟：

### 控制台

如要在現有預留項目中指定一組加速資料表，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 BigQuery 導覽選單中，點選「BI Engine」。

   如果專案已設定偏好資料表，系統會在「偏好資料表」欄中顯示一組資料表。
3. 在要編輯的預訂項目列中，按一下「動作」欄中的圖示，然後選取「編輯」。
4. 將「容量 (GiB)」滑桿調整至要預留的記憶體容量。點選「下一步」。
5. 偏好的資料表：如要在現有預留項目中指定一組要加速的資料表，請在「資料表 ID」欄位中，使用以下模式指定要加速的資料表：`PROJECT.DATASET.TABLE`。

   更改下列內容：

   * `PROJECT`：您的 Google Cloud 專案 ID
   * `DATASET`：資料集
   * `TABLE`：要加速的資料表

   變更最多可能需要十秒才會生效。只有偏好資料表清單中的資料表可以使用 BI Engine 加速功能。

   點選「下一步」。
6. 確認修改後的預訂內容。如果同意，請按一下「更新」。

### SQL

您可以使用 [`ALTER BI_CAPACITY SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_bi_capacity_set_options_statement)建立或修改 BI Engine 預留項目。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER BI_CAPACITY `PROJECT_ID.LOCATION_ID.default`
   SET OPTIONS (
     size_gb = VALUE,
     preferred_tables =
       [`TABLE_PROJECT_ID.DATASET.TABLE1`,
       `TABLE_PROJECT_ID.DATASET.TABLE2`]);
   ```

   請替換下列項目：

   * `PROJECT_ID`：可選用的專案 ID，該專案將受益於 BI Engine 加速。如果省略此參數，系統會使用預設專案。
   * `LOCATION_ID`：需要快取資料的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)，並加上 `region-` 前置字元。例如：`region-us`、`region-us-central1`。
   * `VALUE`：以 GiB 為單位的 BI Engine 容量預留大小，範圍為 1 到 250 GiB。`INT64`您可以[要求增加](https://docs.google.com/forms/d/e/1FAIpQLSdkGV6kwVN_Wz34sjWF4wPofmGkTsPofRKGEth0M9JLpeZcUA/viewform?hl=zh-tw)專案的預留容量上限。大多數地區都可提高預訂量，處理時間為 3 天到 1 週。設定 `VALUE` 會取代現有值 (如果有的話)，設為 `NULL` 則會清除該選項的值。
   * `TABLE_PROJECT_ID.DATASET.TABLE`：
     要套用加速功能的[偏好資料表](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw#preferred_tables)清單 (選用)。格式：
     `TABLE_PROJECT_ID.DATASET.TABLE or
     DATASET.TABLE`. 如果省略專案，系統會使用預設專案。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

## 刪除預留項目

如要刪除容量預留項目，請按照下列步驟操作：

### 控制台

1. 在 BigQuery 頁面的「管理」中，前往「BI Engine」頁面。

   [前往 BI Engine](https://console.cloud.google.com/bigquery/admin/bi-engine?hl=zh-tw)
2. 在「預訂」部分，找出您的預訂。
3. 在「動作」欄中，按一下預訂項目右側的 more\_vert 圖示，然後選擇「刪除」。
4. 在「Delete reservation?」(要刪除預訂項目嗎？) 對話方塊中輸入「Delete」(刪除)，然後按一下「DELETE」(刪除)。

### SQL

設定 BI Engine 容量的選項。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER BI_CAPACITY `PROJECT_ID.LOCATION_ID.default`
   SET OPTIONS (
     size_gb = 0);
   ```

   請替換下列項目：

   * `PROJECT_ID`：可選用的專案 ID，該專案將受益於 BI Engine 加速。如果省略此參數，系統會使用預設專案。
   * `LOCATION_ID`：需要快取資料的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)，並加上 `region-` 前置字元。例如：`region-us`、`region-us-central1`。

   刪除專案中的所有預留容量後，該專案的 BI Engine 就會停用。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)，並提供 DDL 陳述式做為查詢參數。

```
bq --project_id="PROJECT_ID" \
update --reservation
    --bi_reservation_size=0 \
    --location=LOCATION
```

更改下列內容：

* `PROJECT_ID`：專案 ID
* `LOCATION`：您要查詢的資料集位置

## 驗證 BI Engine 資訊

您可以查詢 [`INFORMATION_SCHEMA` 資料表](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)，取得 BI Engine 容量的相關資訊。

### 確認預訂狀態

如要驗證預訂狀態 (包括一組偏好的資料表)，請使用 SQL 查詢查看 `INFORMATION_SCHEMA.BI_CAPACITIES` 檢視畫面。例如：

```
SELECT
  *
FROM
  `<PROJECT_ID>.region-<REGION>.INFORMATION_SCHEMA.BI_CAPACITIES`;
```

在 Google Cloud 控制台中，這項 SQL 查詢的結果大致如下：

### 查看預訂變更

如要查看特定預訂的變更記錄，請使用 `INFORMATION_SCHEMA.BI_CAPACITY_CHANGES` 檢視畫面 (透過 SQL 查詢)。例如：

```
SELECT
  *
FROM
  `<PROJECT_ID>.region-<REGION>.INFORMATION_SCHEMA.BI_CAPACITY_CHANGES`
ORDER BY
  change_timestamp DESC
LIMIT 3;
```

在 Google Cloud 控制台中，這項 SQL 查詢的結果大致如下：

## 後續步驟

* 進一步瞭解 [BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)。
* 瞭解 [BI Engine 定價](https://cloud.google.com/bi-engine/pricing?hl=zh-tw)。
* [使用數據分析分析資料](https://docs.cloud.google.com/bigquery/docs/visualize-looker-studio?hl=zh-tw)。
* [監控 BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-monitor?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]