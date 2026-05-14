Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過時空旅行和安全防護功能保留資料

本文說明資料集的*時空旅行*和*安全防護*資料保留期限。在時間回溯和安全期內，系統會繼續儲存您在資料集任何資料表中變更或刪除的資料，以備不時之需。

## 時空旅行和資料保留

您可以在時間旅行視窗的任何時間點存取變更或刪除的資料，該視窗預設涵蓋過去七天。時間旅行功能可讓您[查詢已更新或刪除的資料](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw)、還原已刪除的[資料表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw)或[資料集](https://docs.cloud.google.com/bigquery/docs/restore-deleted-datasets?hl=zh-tw)、還原[已過期的資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#updating_a_tables_expiration_time)，或[將資料表還原至特定時間點](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw#restore-a-table)。

你可以設定時間回溯視窗的持續時間，最短為兩天，最長為七天。如果需要復原更新或刪除的資料，較長的時間旅行視窗就很有用。使用[實體儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)時，縮短時間範圍可節省儲存空間費用。使用邏輯儲存空間計費模式時，不適用這些折扣。如要進一步瞭解儲存空間計費模式對費用的影響，請參閱「[計費方式](#billing)」。時間旅行功能的時間長度不得少於 2 天。

## 設定時間回溯期

您可以在資料集或專案層級設定時間回溯期。這些設定隨後會套用至與資料集或專案相關聯的所有資料表。

### 設定專案層級的時間回溯期

如要指定專案層級的預設時間回溯期，可以使用資料定義語言 (DDL) 陳述式。如要瞭解如何設定專案層級的時間旅行視窗，請參閱「[管理設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)」。

### 設定資料集層級的時間回溯期

如要指定或修改資料集的時空旅行時間範圍，可以使用Google Cloud console、bq 指令列工具或 BigQuery API。

* 如要為新資料集指定預設時間回溯期，請參閱「[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#create-dataset)」。
* 如要修改或更新現有資料集的時空旅行視窗，請參閱「[更新時空旅行視窗](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#update_time_travel_windows)」。

修改時間旅行時間範圍時，如果時間戳記指定的時間超出時間旅行時間範圍，或是在資料表建立之前，查詢就會失敗並傳回類似下列的錯誤：

```
Table ID was created at time which is
before its allowed time travel interval timestamp. Creation
time: timestamp
```

## 時間回溯功能的運作方式

BigQuery 採用欄位式儲存格式。也就是說，資料是依資料欄而非資料列整理及儲存。如果資料表有多個資料欄，所有資料列中每個資料欄的值會一起儲存在儲存區塊中。

修改 BigQuery 資料表中的儲存格時，您會變更特定資料列和資料欄中的特定值。由於 BigQuery 會將資料欄儲存在一起，因此即使只修改資料欄中的單一儲存格，通常也需要讀取包含該資料欄資料的整個儲存區塊 (適用於受影響的資料列)、套用變更，然後寫入該儲存區塊的新版本。

時間旅行功能會追蹤組成資料表的儲存區塊版本，更新資料時，BigQuery 不會直接修改現有的儲存區塊，而是會建立受影響儲存區塊的新版本，並納入更新後的資料。然後保留舊版，以供時間旅行之用。

BigQuery 會使用適應性檔案大小和儲存區塊。儲存區塊的大小不固定，而是取決於資料表大小和資料分配等因素。即使只變更儲存區塊中的一個儲存格，也會變更該資料欄的資料，可能影響多個資料列。因此，版本化並傳送至時空旅行的資料單位，通常是包含該資料欄修改資料的整個儲存區塊，而不只是單一儲存格。

因此，變更一個儲存格可能會導致傳送至時間旅行的資料量，超出變更大小。

### 時間旅行視窗對資料表和資料集復原的影響

刪除資料表或資料集時，系統會使用刪除時生效的時間回溯期。

舉例來說，如果時間回溯視窗的持續時間為兩天，然後將持續時間增加至七天，則在變更前刪除的資料表仍只能復原兩天。同樣地，如果時間回溯期為五天，而您將其縮短為三天，則在變更前刪除的任何資料表仍可復原五天。

由於時間回溯期是在資料集層級設定，因此您必須先還原已刪除的資料集，才能變更其時間回溯期。

如果您縮短時間旅行視窗的持續時間、刪除資料表，然後發現需要更長的時間才能復原該資料，可以從刪除資料表之前的時間點建立資料表快照。您必須在刪除的資料表仍可復原時執行這項操作。
詳情請參閱「[使用時空旅行功能建立資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-create?hl=zh-tw#create_a_table_snapshot_using_time_travel)」。

### 時間回溯和資料列層級存取權

如果資料表有或曾有[資料列層級存取權政策](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)，只有獲授下列 [Identity and Access Management (IAM)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw) 權限的主體，才能存取資料表的歷來資料：

| **權限** | **資源** |
| --- | --- |
| [`bigquery.rowAccessPolicies.overrideTimeTravelRestrictions`](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.rowAccessPolicies.overrideTimeTravelRestrictions) | 要存取歷來資料的資料表 |

以下是提供 `bigquery.rowAccessPolicies.overrideTimeTravelRestrictions` 權限的預先定義 IAM 角色：

| **角色** | **資源** |
| --- | --- |
| [`roles/bigquery.admin`](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin) | 要存取歷來資料的資料表 |
| [`roles/bigquery.studioAdmin`](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioAdmin) | 要存取歷來資料的資料表 |
| [`roles/iam.databasesAdmin`](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.databasesAdmin) | 要存取歷來資料的資料表 |

您也可以使用[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)授予權限。`bigquery.rowAccessPolicies.overrideTimeTravelRestrictions`

**注意：** **`roles/owner`** 角色不具備資料表管理員角色中的所有權限，因此您必須將其中一個資料表管理員角色授予任何還原資料表的使用者，這些資料表已套用或曾套用列層級存取權政策。

* 執行下列指令，傳遞 UTC 時間戳記，取得對應的 Unix 紀元時間：

  ```
  date -d '2023-08-04 16:00:34.456789Z' +%s000
  ```
* 在 bq 指令列工具中，將上一個指令傳回的 UNIX 紀元時間 `1691164834000` 取代為 執行下列指令，在相同資料集 `myDatasetID` 的另一個資料表 `restoredTable` 中，還原已刪除資料表 `deletedTableID` 的副本：

  ```
  bq cp myProjectID:myDatasetID.deletedTableID@1691164834000 myProjectID:myDatasetID.restoredTable
  ```

## 故障保全

BigQuery 提供安全期。在安全期內，系統會在時間旅行視窗後自動保留刪除的資料額外七天，以供緊急復原。資料可在資料表層級復原。系統會從資料表刪除時的時間戳記所代表的時間點，還原資料表資料。安全期無法設定，也無法延長。

執行下列作業時，遭取代或移除的資料可在時間回溯期內復原。時間旅行時間範圍結束後，這項資料就會進入保全期，以延長復原時間：

* **刪除或取代資料表：**刪除資料表或完全取代資料表資料時 (例如在載入工作中使用 [`WRITE_TRUNCATE`](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata.WriteDisposition?hl=zh-tw) 寫入處置，或使用 [`CREATE OR REPLACE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)
  陳述式)，系統會保留資料表先前的內容。
* **刪除分區：**如果從[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)中刪除特定分區，系統會保留該分區的資料。資料表中的其他分區不受影響。

您無法查詢或直接復原安全儲存空間中的資料。如要從安全儲存空間復原資料，請與 [Cloud Customer Care](https://cloud.google.com/support-hub?hl=zh-tw) 團隊聯絡。

**警告：** 安全期過後，Cloud Customer Care 就無法復原任何已刪除的資料。

## 帳單

如果將[儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)設為依實體位元組計費，系統會另外收取時間旅行和安全儲存空間所用位元組的費用。時間回溯和容錯移轉儲存空間的費用，會以實際使用中的儲存空間費率計算。您可以[設定時間範圍](#configure_the_time_travel_window)，在儲存空間成本與資料保留需求之間取得平衡。

如果將儲存空間計費模式設為依邏輯位元組計費，系統會將時間旅行和容錯移轉儲存空間的總儲存空間費用，計入您支付的基本費率。

下表比較實體和邏輯儲存空間的費用：

| **計費模式** | **你支付的費用為何？** |
| --- | --- |
| 實體 (壓縮) 儲存空間 | * 您需要支付有效位元組的費用 * 長期儲存費用 * 您需要支付 Time Travel 儲存空間費用 * 您需要支付容錯儲存空間的費用 |
| 邏輯 (未壓縮) 儲存空間 (預設設定) | * 您只需要為動態儲存付費 * 長期儲存費用 * 您不必支付時間旅行儲存空間費用 * 您不需要支付安全儲存空間費用 |

如果您使用實體儲存空間，可以查看 [`TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw) 和 [`TABLE_STORAGE_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-by-organization?hl=zh-tw) 檢視畫面中的 `TIME_TRAVEL_PHYSICAL_BYTES` 和 `FAIL_SAFE_PHYSICAL_BYTES` 欄，瞭解時間旅行和安全模式使用的位元組。如需如何使用其中一個檢視畫面估算費用的範例，請參閱「[預測儲存空間帳單](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw#forecast_storage_billing)」。

[儲存費用](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)適用於時空旅行和容錯資料，但只有在 BigQuery 其他地方不適用資料儲存費用時，您才需要付費。詳情如下：

* 建立資料表時，不會產生時空旅行或容錯儲存空間費用。
* 如果資料遭到變更或刪除，您必須支付時間回溯期間和安全期內，時間回溯功能儲存的變更或刪除資料費用。這與表格快照和副本的儲存空間定價類似。
* 臨時資料表不會產生安全儲存空間費用。

## 資料保留範例

下表說明已刪除或變更的資料在儲存空間保留時間範圍之間的移動方式。以下範例顯示總有效儲存空間為 200 GiB，且在 7 天的時間旅行視窗中刪除了 50 GiB 的情況：

|  | 第 0 天 | 第 1 天 | 第 2 天 | 第 3 天 | 第 4 天 | 第 5 天 | 第 6 天 | Day 7 | 第 8 天 | 第 9 天 | 第 10 天 | 第 11 天 | 第 12 天 | 第 13 天 | Day 14 | 第 15 天 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 動態儲存空間 | 200 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 |
| 時間回溯儲存空間 |  | 50 | 50 | 50 | 50 | 50 | 50 | 50 |  |  |  |  |  |  |  |  |
| 安全儲存空間 |  |  |  |  |  |  |  |  | 50 | 50 | 50 | 50 | 50 | 50 | 50 |  |

從長期實體儲存裝置刪除資料的運作方式也相同。

## 限制

使用時間旅行功能擷取資料時，會受到以下限制：

* 時空旅行功能只會在時空旅行時間範圍內提供歷來資料。如要將資料表資料保留時間延長至時空旅行時間範圍以外，以供非緊急用途使用，請使用[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。
* 如果資料表有或曾有資料列層級存取權政策，則只有資料表管理員可以使用時間旅行。詳情請參閱「[時間旅行和資料列層級存取權](#time_travel_and_row-level_access)」。
* 時間旅行功能不會還原資料表中繼資料。
* 下列表格類型不支援時空旅行：
  + [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)。不過，如果是 Apache Iceberg 外部資料表，您可以使用 [`FOR SYSTEM_TIME AS OF` 子句](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw#query_data_at_a_point_in_time)，存取 Iceberg 中繼資料保留的快照。
  + [暫時快取的查詢結果資料表](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)。
  + [暫時性工作階段表格](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)。
  + [暫時性多重陳述式表格](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)。
  + 外部資料集下方列出的資料表。

## 後續步驟

* 瞭解如何[查詢及復原時間旅行資料](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw)。
* 進一步瞭解[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]