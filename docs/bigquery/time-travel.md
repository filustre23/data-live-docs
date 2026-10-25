Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過時間旅行和容錯機制保留資料

本文說明資料集的*時間回溯*和*安全防護*資料保留期限。在時間旅行和安全防護期間，您在資料集任何資料表中變更或刪除的資料會繼續儲存，以備您需要復原。

## 時間旅行和資料保留

您可以在時間旅行視窗的任何時間點存取變更或刪除的資料，預設時間範圍為過去七天。時間旅行功能可讓您[查詢更新或刪除的資料](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw)、還原已刪除的[資料表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw)或[資料集](https://docs.cloud.google.com/bigquery/docs/restore-deleted-datasets?hl=zh-tw)、還原[過期的資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#updating_a_tables_expiration_time)，或[將資料表還原至特定時間點](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw#restore-a-table)。

您可以設定時間旅行回溯期的長度，最短兩天，最長七天。如果需要復原更新或刪除的資料，較長的時間旅行視窗就很有用。使用[實體儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)時，較短的時間旅行窗口可節省儲存費用。如果採用邏輯儲存空間計費模式，則不適用這些節省方案。如要進一步瞭解儲存空間計費模式對費用的影響，請參閱「[計費](#billing)」一文。時間旅行的時長不得少於 2 天。

## 設定時間回溯期

您可以在資料集或專案層級設定時間回溯期。這些設定隨後會套用至與資料集或專案相關聯的所有資料表。

### 設定專案層級的時間回溯期

如要指定專案層級的預設時間回溯期，可以使用資料定義語言 (DDL) 陳述式。如要瞭解如何設定專案層級的時間旅行回溯期，請參閱「[管理配置設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)」。

### 設定資料集層級時間回溯期

如要指定或修改資料集的時光旅行時間範圍，可以使用Google Cloud 控制台、bq 指令列工具或 BigQuery API。

* 如要指定新資料集的預設時間回溯期，請參閱「[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#create-dataset)」。
* 如要修改或更新現有資料集的時間回溯期，請參閱「[更新時間回溯期](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#update_time_travel_windows)」。

修改時光旅行時間範圍時，如果時間戳記指定的時間超出時光旅行時間範圍，或早於資料表建立時間，查詢就會失敗，並傳回類似下列的錯誤：

```
Table ID was created at time which is
before its allowed time travel interval timestamp. Creation
time: timestamp
```

## 時間旅行的運作方式

BigQuery 使用資料欄儲存格式。也就是說，資料是依資料欄而非資料列整理及儲存。如果資料表有多個資料欄，則所有資料列中每個資料欄的值都會一起儲存在儲存區塊中。

修改 BigQuery 資料表中的儲存格，即代表變更特定資料列和資料欄中的特定值。由於 BigQuery 會將資料欄儲存在一起，因此即使只修改資料欄中的單一儲存格，通常也需要讀取整個儲存區塊，其中包含受影響資料列的資料欄資料，套用變更，然後寫入該儲存區塊的新版本。

時間旅行功能會追蹤構成資料表的儲存區塊版本。更新資料時，BigQuery 不會直接修改現有的儲存區塊，而是會建立受影響儲存區塊的新版本，並加入更新後的資料。然後保留先前版本，以便進行時間旅行。

BigQuery 會採用可調整的檔案大小和儲存空間區塊。儲存區塊的大小並非固定，而是會因資料表大小和資料分布等因素而異。即使只變更儲存區塊中的一個儲存格，也會變更該資料欄的資料，可能影響許多資料列。因此，版本化並傳送至時空旅行的資料單位，通常是包含該資料欄修改資料的整個儲存區塊，而不只是單一儲存格。

因此，變更一個儲存格可能會導致傳送至時間旅行的資料量超過變更的大小。

### 時間回溯期對資料表和資料集復原作業的影響

刪除的資料表或資料集會使用刪除時有效的時間回溯期。

舉例來說，如果將時光旅行時間範圍從兩天延長為七天，在變更前刪除的資料表仍只能復原兩天。同樣地，如果將時間旅行回溯期從五天縮短為三天，在變更前刪除的資料表仍可在五天內復原。

由於時間回溯期是在資料集層級設定，因此您必須先取消刪除資料集，才能變更其時間回溯期。

如果縮短時間旅行視窗的持續時間、刪除資料表，然後發現需要更長的時間才能復原該資料，可以從刪除資料表之前的時間點建立資料表快照。請務必在已刪除的資料表仍可復原時執行這項操作。詳情請參閱「[使用時間旅行功能建立資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-create?hl=zh-tw#create_a_table_snapshot_using_time_travel)」。

### 時間回溯和資料列層級存取權

如果資料表有或曾有[資料列層級存取權政策](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)，只有獲授下列 [Identity and Access Management (IAM)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw) 權限的主體，才能存取資料表的歷來資料：

| **權限** | **資源** |
| --- | --- |
| [`bigquery.rowAccessPolicies.overrideTimeTravelRestrictions`](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.rowAccessPolicies.overrideTimeTravelRestrictions) | 正在存取歷來資料的資料表 |

下列預先定義的 IAM 角色提供
`bigquery.rowAccessPolicies.overrideTimeTravelRestrictions`
權限：

| **角色** | **資源** |
| --- | --- |
| [`roles/bigquery.admin`](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin) | 要存取歷來資料的資料表 |
| [`roles/bigquery.studioAdmin`](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioAdmin) | 要存取歷來資料的資料表 |
| [`roles/iam.databasesAdmin`](https://docs.cloud.google.com/iam/docs/roles-permissions/jobfunctions?hl=zh-tw#iam.databasesAdmin) | 正在存取歷來資料的資料表 |

您也可以使用[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)授予 `bigquery.rowAccessPolicies.overrideTimeTravelRestrictions` 權限。

**注意：** **`roles/owner`** 角色不包含資料表管理員角色中的所有權限，因此您必須將其中一個資料表管理員角色授予任何使用者，讓他們還原已套用或曾套用資料列層級存取權政策的資料表。

* 執行下列指令，傳遞世界標準時間時間戳記，取得對應的 Unix 紀元時間：

  ```
  date -d '2023-08-04 16:00:34.456789Z' +%s000
  ```
* 在 bq 指令列工具中，取代前一個指令收到的 UNIX 紀元時間 `1691164834000`。執行下列指令，在相同資料集 `myDatasetID` 的另一個資料表 `restoredTable` 中，還原已刪除資料表 `deletedTableID` 的副本：

  ```
  bq cp myProjectID:myDatasetID.deletedTableID@1691164834000 myProjectID:myDatasetID.restoredTable
  ```

## 安全機制

BigQuery 提供安全防護期。在安全防護期間，刪除的資料會在時光旅行期間結束後自動保留七天，以便用於緊急復原。資料可在資料表層級復原，復原時間點為資料刪除時的時間戳記。

安全期無法設定，也無法延長。您必須在七天安全期結束前，開始並完成資料表復原作業，並根據資料表大小預留足夠時間，讓複製工作完成。

執行下列作業時，您可以在時間回溯期內復原遭取代或移除的資料。時間旅行窗口結束後，這項資料會進入安全防護期，延長復原時間：

* **刪除或取代資料表：**刪除資料表或完全取代資料表資料時 (例如，在載入工作中透過 [`WRITE_TRUNCATE`](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata.WriteDisposition?hl=zh-tw)
  寫入處置，或使用 [`CREATE OR REPLACE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)
  陳述式)，系統會保留資料表先前的內容。
* **分區刪除或到期：**如果[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)中的特定分區遭到刪除或到期，系統會保留屬於該分區的資料。資料表中的其他分區不會受到影響。由於無法還原個別分區，因此您必須從分區遭刪除或過期前的時間戳記還原整個資料表。如果原始資料表設有分區到期時間，該設定會複製到還原的資料表。如要查詢早於分區到期時間的還原分區，請[更新還原資料表的分區到期時間](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#update_the_partition_expiration)。

### 從故障安全儲存空間復原資料

您無法直接查詢安全儲存空間中的資料，也無法從安全儲存空間複製資料表，除非 [Cloud 客戶服務](https://cloud.google.com/support-hub?hl=zh-tw)授予資料集暫時的安全復原存取權。如要從安全儲存空間還原資料表，請與 [Cloud Customer Care](https://cloud.google.com/support-hub?hl=zh-tw) 聯絡，要求取得資料集的安全還原存取權，然後執行含有 `@TIME` 時間戳記裝飾符的資料表複製工作，自行[還原資料表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw#restore_a_table)。

時間旅行復原只會更新中繼資料指標，而安全復原必須在資料表複製工作完成前，實際還原及複製封存的儲存區塊。從安全防護儲存空間還原大型或大量分區的資料表時，請注意下列行為：

* **複製時間較長和逾時：**從安全儲存空間還原多 TB 的資料表或含有多個分區的資料表，所需時間可能比標準資料表複製作業長得多。在所有儲存區塊還原之前，單一複製工作可能會逾時或失敗，並出現暫時性內部錯誤。
* **重試時逐步還原：**系統會逐步儲存安全防護還原進度。在複製工作逾時或失敗前還原的任何儲存空間區塊，都會維持還原狀態。如果 `bq cp` 指令失敗，請使用完全相同的來源資料表和 `@TIME` 時間戳記裝飾符，重試該指令。每次重試都會略過已還原的區塊，並繼續還原剩餘資料，直到複製工作成功為止。
* **時效性復原期：**請在七天安全期內盡早聯絡 [Cloud Customer Care](https://cloud.google.com/support-hub?hl=zh-tw)，尤其是大型資料表，這樣您才有足夠的時間在安全期到期前執行重試。

**警告：** 安全防護期過後，Cloud Customer Care 就無法復原任何已刪除的資料。

## 帳單

如果將[儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)設為使用實體位元組，系統會針對時間旅行和安全防護儲存空間使用的位元組另外計費。時間旅行和安全防護儲存空間，則按使用中實體儲存空間費率計費。您可以[設定時光旅行時間範圍](#configure_the_time_travel_window)，在儲存費用和資料保留需求之間取得平衡。

如果將儲存空間計費模式設為使用邏輯位元組，系統會將時空旅行和安全儲存空間的總儲存空間費用，計入您支付的基本費率。

下表比較實體和邏輯儲存空間費用：

| **結帳模式** | **你支付的項目為何？** |
| --- | --- |
| 實體 (壓縮) 儲存空間 | * 您必須支付有效位元組的費用 * 支付長期儲存費用 * 您需要支付時間旅行儲存空間費用 * 您需要支付故障安全儲存空間的費用 |
| 邏輯 (未壓縮) 儲存空間 (預設設定) | * 您需要支付使用中儲存空間的費用 * 支付長期儲存費用 * 時間旅行儲存空間不需付費 * 您不需為安全儲存空間付費 |

如果您使用實體儲存空間，可以查看 [`TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw) 和 [`TABLE_STORAGE_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-by-organization?hl=zh-tw) 檢視畫面中的 `TIME_TRAVEL_PHYSICAL_BYTES` 和 `FAIL_SAFE_PHYSICAL_BYTES` 欄，瞭解時間旅行和安全模式使用的位元組。如要瞭解如何使用其中一個檢視表來預估費用，請參閱「[預測儲存空間帳單](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw#forecast_storage_billing)」。

時間旅行和容錯移轉資料會產生[儲存空間費用](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)，但只有在 BigQuery 其他地方不適用資料儲存空間費用時，您才需要付費。相關細節如下：

* 建立資料表時，不會產生時間旅行或安全防護儲存空間費用。
* 如果資料遭到變更或刪除，則在時間旅行期間和防故障期間，系統會針對時間旅行儲存的變更或刪除資料收取儲存費用。這與表格快照和副本的儲存空間價格類似。
* 臨時資料表不會產生安全防護儲存空間費用。

## 資料保留範例

下表說明已刪除或變更的資料如何在儲存空間保留期限內移動。以下範例顯示總有效儲存空間為 200 GiB，且在七天的時空旅行時間範圍內刪除了 50 GiB 的情況：

|  | 第 0 天 | 第 1 天 | 第 2 天 | 第 3 天 | 第 4 天 | 第 5 天 | 第 6 天 | Day 7 | 第 8 天 | 第 9 天 | 第 10 天 | 第 11 天 | 第 12 天 | 第 13 天 | Day 14 | 第 15 天 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 使用中的儲存空間 | 200 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 | 150 |
| 時間回溯儲存空間 |  | 50 | 50 | 50 | 50 | 50 | 50 | 50 |  |  |  |  |  |  |  |  |
| 故障安全儲存空間 |  |  |  |  |  |  |  |  | 50 | 50 | 50 | 50 | 50 | 50 | 50 |  |

從長期實體儲存空間刪除資料的方式也相同。

## 限制

使用時空旅行功能擷取資料時，須遵守下列限制：

* 時間回溯功能只會在時間回溯期內提供歷來資料。如要將資料表資料保留超過時空旅行時間範圍，以供非緊急用途使用，請使用[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。
* 如果資料表有或曾有資料列層級存取權政策，則只有資料表管理員可以使用時間回溯功能。詳情請參閱「[時間旅行和資料列層級存取權](#time_travel_and_row-level_access)」。
* 時光旅行不會還原資料表中繼資料。
* 下列資料表類型不支援時間旅行：
  + [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)。不過，如果是 Apache Iceberg 外部資料表，您可以使用 [`FOR SYSTEM_TIME AS OF` 子句](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw#query_data_at_a_point_in_time)，存取 Iceberg 中繼資料中保留的快照。
  + [暫時快取的查詢結果資料表](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)。
  + [臨時工作階段資料表](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)。
  + [臨時多陳述式資料表](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)。
  + 外部資料集下方列出的資料表。

## 後續步驟

* 瞭解如何[查詢及復原時間旅行資料](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw)。
* 進一步瞭解[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]