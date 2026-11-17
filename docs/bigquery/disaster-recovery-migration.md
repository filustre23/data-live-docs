Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 遷移至代管災難復原

本頁面說明如何從 BigQuery 跨區域複製功能，遷移至 BigQuery 代管災難復原。

## 總覽

BigQuery [跨區域複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw) (CRR) 和[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw) (DR) 功能，旨在提升資料可用性和災難復原能力。不過，兩者處理區域性服務中斷的方式不同。如果主要區域無法使用，CRR 不允許升級次要副本。相較之下，DR 則提供更全面的保護，即使主要區域無法使用，也能容錯移轉至次要副本。CRR 只會複製儲存空間，而 DR 則會複製儲存空間和運算能力。

下表說明 CRR 和 DR 的功能：

| 功能 | CRR | DR |
| --- | --- | --- |
| 初始複製程序 | 一開始使用 CRR 複製資料集。 | 在將 CRR 資料集遷移至 DR 資料集之前，初始載入作業已透過 CRR 複製。 |
| 促銷活動複製 | 使用標準複製功能。 | 使用[強化型複製功能](https://docs.cloud.google.com/storage/docs/availability-durability?hl=zh-tw#turbo-replication)。 |
| 升級程序 | 在資料集層級升級。 | 在預留項目層級升級 (預留項目容錯移轉和資料集升級)。一個容錯移轉預留項目可附加多個資料集。 DR 不支援資料集層級升級。 |
| 促銷活動執行 | 透過使用者介面或 SQL 式 DDL 指令，為每個資料集設定。不支援 CLI、用戶端程式庫、API 或 Terraform。 | 透過使用者介面或 SQL 式 DDL 指令，為每個 EPE 預留項目設定。不支援 CLI、用戶端程式庫、API 或 Terraform。 |
| 容錯移轉模式 | 軟式容錯移轉。 | 硬式容錯移轉。 |
| 版本需求 | 任何運算能力模式。 | Enterprise Plus 版。 |
| 限制 | [CRR 限制](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#limitations)。 | 包括 [CRR 限制](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#limitations)和 [DR 限制](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw#limitations)。 |
| 寫入權限 | 在任何運算資源模式下執行的工作，都可以寫入主要區域中的複製資料集。次要節點一律為唯讀。 | 只有在 Enterprise Plus 預留項目下執行的工作，才能寫入主要區域中的複製資料集。次要資料集和預留項目副本一律為唯讀。 |
| 讀取權限 | 在任何運算資源模式下執行的工作，都可以讀取複製的資料集。 | 在任何運算資源模式下執行的工作，都可以讀取複製的資料集。 |

## 遷移影響

以下各節將概略說明遷移至 DR 時，費用和功能會有哪些變化。

### 費用影響

從 CRR 遷移至 DR 時，請考量下列成本影響：

* DR 僅支援 Enterprise Plus 版本的寫入權限，這會產生較高的運算費用。您可以從任何運算資源模型讀取資料，因此現有工作的讀取費用不會改變。
* DR 會使用 [Turbo 複製](https://docs.cloud.google.com/storage/docs/availability-durability?hl=zh-tw#turbo-replication)功能，這項功能會依據區域組合產生額外費用。
* CRR 和 DR 的儲存空間價格相同。

如要進一步瞭解定價，請參閱「[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」。

### 功能影響

從 CRR 遷移至 DR 時，請考量下列功能影響：

* DR 僅支援預留項目層級的容錯移轉。任何仰賴資料集層級容錯移轉的現有工作都會失敗。
* 資料集附加至 DR 預留項目後，只有 Enterprise Plus 版本的查詢可以寫入資料集。如果現有的寫入工作未採用 Enterprise Plus 版本的運算能力，就會失敗。

## 事前準備

開始遷移前，請先熟悉[跨區域複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)和[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)的概念。

如要遷移至 DR，必須符合下列必要條件：

* 您有已啟用 BigQuery 的有效 Google Cloud 專案。
* 您已使用 CRR 建立及複製資料集。
* 資料集的主要和次要位置與您要用於 DR 的位置相同。
* 您具備使用 DR 的必要權限。如要進一步瞭解權限，請參閱「[事前準備](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw#before_you_begin)」。

## 從 CRR 遷移至 DR

以下各節說明如何將資料集從 CRR 遷移至 DR。假設您已為 CRR 設定資料集。

### 建立容錯移轉預留項目

如要啟用災難復原功能，您必須在主要區域建立容錯移轉預留項目。設定預留項目時，請選擇適當的主要和次要區域。主要和次要區域應與您要遷移至 DR 的所有 CRR 資料集區域相符。如要建立容錯移轉預留項目，請選擇下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，依序點選「Workload management」(工作負載管理) 和 playlist\_add「Create reservation」(建立預留項目)。
3. 在「Reservation name」(預留項目名稱) 欄位中，輸入預留項目名稱。
4. 在「Location」(位置) 清單中選取位置。
5. 在「Edition」清單中，選取 Enterprise Plus 版本。
6. 在「Max reservation size selector」(預留項目大小選取器) 清單中，選取預留項目大小上限。
7. 選用：在「Baseline slots」(基準運算單元) 欄位中，輸入預留項目的基準運算單元數量。

   可用的自動調度資源運算單元數量，是從「Max reservation size」(預留項目大小上限) 值減去「Baseline slots」(基準運算單元) 值而得。舉例來說，如果您建立的預留項目有 100 個基準運算單元，且預留項目大小上限為 400，則預留項目會有 300 個自動調度資源運算單元。如要進一步瞭解基準運算單元，請參閱「[使用預留項目搭配基準和自動調度資源運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw#using_reservations_with_baseline_and_autoscaling_slots)」。
8. 在「Secondary location」(次要位置) 清單中，選取次要位置。
9. 如要停用[閒置的運算單元共用](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)功能，並僅使用指定的運算單元容量，請按一下「Ignore idle slots」(忽略閒置運算單元) 切換鈕。
10. 如要展開「Advanced settings」(進階設定) 部分，請按一下 expand\_more 展開箭頭。
11. 選用：如要設定目標工作並行，請將「Override automatic target job concurrency」(覆寫自動目標工作並行設定) 切換鈕設為開啟，然後輸入「Target Job Concurrency」(目標工作並行) 的值。「Cost estimate」(費用預估) 表格會顯示運算單元明細。「Capacity summary」(容量摘要) 表格會顯示預留項目的摘要。
12. 按一下「儲存」。

新的預留項目會顯示在「Slot reservations」(運算單元預留項目) 分頁中。

### SQL

如要建立預留項目，請使用 [`CREATE RESERVATION` 資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_reservation_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE RESERVATION
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME`
   OPTIONS (
     slot_capacity = NUMBER_OF_BASELINE_SLOTS,
     edition = ENTERPRISE_PLUS,
     secondary_location = SECONDARY_LOCATION);
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID。
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，則只能選擇 Enterprise 版本。
   * `RESERVATION_NAME`：預留項目的名稱。

     名稱開頭和結尾必須是小寫英文字母或數字，且只能包含小寫英文字母、數字和破折號。
   * `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量。您無法在同一項預留項目中設定 `slot_capacity` 選項和 `edition` 選項。
   * `SECONDARY_LOCATION`：預留項目的次要[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果服務中斷，附加至這個預留項目的任何資料集都會容錯移轉至這個位置。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### 將資料集附加至預留項目

建立容錯移轉預留項目後，請將跨區域資料集附加至預留項目。這會為所有附加資料集啟用容錯移轉功能。如要將資料集附加至預留項目，請選擇下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 點選「Slot reservations」(運算單元預留項目) 分頁標籤。
4. 按一下要附加資料集的預留項目。
5. 按一下「連結的容錯移轉資料集」分頁標籤。
6. 按一下「連結容錯移轉資料集」。
7. 輸入要與預留項目建立關聯的資料集名稱。
8. 按一下「新增」。

### SQL

如要將資料集附加至預留項目，請使用 [`ALTER SCHEMA SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER SCHEMA
     `DATASET_NAME`
   SET OPTIONS (
     failover_reservation = ADMIN_PROJECT_ID.RESERVATION_NAME);
   ```

   替換下列內容：

   * `DATASET_NAME`：資料集名稱。
   * `ADMIN_PROJECT_ID.RESERVATION_NAME`：要與資料集建立關聯的預留項目名稱。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### 驗證設定

如要驗證設定狀態，請查詢 [`INFORMATION_SCHEMA.SCHEMATA_REPLICAS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-schemata-replicas?hl=zh-tw)。

```
PROJECT_ID.`region-REGION`.INFORMATION_SCHEMA.SCHEMATA_REPLICAS[_BY_PROJECT]
```

確認資料集已附加至正確區域中的正確預留項目。

請更改下列內容：

* 選用：`PROJECT_ID`： Google Cloud 專案的 ID。如未指定，則會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)，才能查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

## 範例

以下範例將逐步說明如何從 CRR 遷移至 DR，並提供使用 GoogleSQL 的實際範例。在本例中，假設如下：

* 您目前使用的專案名為 `myproject`。
* 您已建立名為 `mydataset` 的資料集，並設定 CRR。
* `mydataset` 的主要區域為 `us-central1`，次要區域為 `us-west1`。

如要開始將資料集遷移至 DR，請先使用 Enterprise Plus 版本建立預留項目。在本範例中，預留項目名稱為 `myreservation`。

```
CREATE RESERVATION `myproject.region-us-central1.myreservation`
OPTIONS (
  slot_capacity = 0,
  edition = ENTERPRISE_PLUS,
  autoscale_max_slots = 50,
  secondary_location = 'us-west-1');
```

建立預留項目後，即可將資料集附加至預留項目。下列範例會將資料集附加至預留項目：

```
ALTER SCHEMA
  `myproject.mydataset`
SET OPTIONS (
  failover_reservation = 'myproject.myreservation');
```

接著，確認資料集已成功附加。

```
SELECT
  failover_reservation_project_id,failover_reservation_name,
FROM
 `myproject`.`region-us-west1`.INFORMATION_SCHEMA.SCHEMATA_REPLICAS
WHERE
 schema_name='mydataset';
```

這項查詢的結果應與下方類似：

```
+---------------------------------+---------------------------+
| failover_reservation_project_id | failover_reservation_name |
+---------------------------------+---------------------------+
| myproject                       | myreservation             |
| myproject                       | myreservation             |
+---------------------------------+---------------------------+
```

## 後續步驟

* 如要進一步瞭解跨區域複製功能，請參閱「[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)」。
* 如要進一步瞭解代管災難復原，請參閱「[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-16 (世界標準時間)。"],[],[]]