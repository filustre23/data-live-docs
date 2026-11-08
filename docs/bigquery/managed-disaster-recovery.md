Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 代管災難復原

為保護資料，並在區域服務中斷期間維持業務營運，您可以設定及使用 BigQuery 代管的災難復原功能，保護 BigQuery 資料和工作負載。

## 總覽

BigQuery 支援災難復原，即使整個區域的服務全面中斷，也能正常營運。BigQuery 災難復原功能會透過[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)管理儲存空間容錯移轉。在次要區域建立資料集副本後，您可以控管運算和儲存空間的容錯移轉行為，在服務中斷期間維持業務不中斷。容錯移轉後，您可以在升級後的區域存取運算資源 (運算單元) 和複製的資料集。災難復原功能僅適用於 [Enterprise Plus 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。

代管災難復原功能提供兩種容錯移轉選項：硬容錯移轉和軟容錯移轉。硬容錯移轉會立即將次要區域的預留項目和資料集副本升級為主要項目。即使目前的主要區域處於離線狀態，這項操作仍會繼續執行，不會等待任何未複製的資料完成複製。因此，硬性容錯移轉期間可能會遺失資料。如果任何工作在副本的 [`replication_time`](https://docs.cloud.google.com/bigquery/docs/information-schema-schemata-replicas?hl=zh-tw#schema) 值之後，於來源區域提交資料，則可能需要在硬容錯移轉後，於目的地區域重新執行。在硬容錯移轉期間，尚未複製的資料集存取控管機制 (ACL)，包括授權檢視表和使用者存取權授予，也可能遺失。為避免下游中斷，請在容錯移轉應對手冊中加入 ACL 重新建立步驟 (例如使用 `terraform apply`)。與硬性容錯移轉不同，軟性容錯移轉會等到主要區域中提交的所有預留項目和資料集變更都複製到次要區域後，才會完成容錯移轉程序。軟性容錯移轉需要主要和次要區域都可用。啟動軟性容錯移轉會設定預留項目的 [`softFailoverStartTime`](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rest/v1/projects.locations.reservations?hl=zh-tw#replicationstatus)。軟容錯移轉完成後，系統會清除 [`softFailoverStartTime`](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rest/v1/projects.locations.reservations?hl=zh-tw#replicationstatus)。

如要啟用災難復原功能，您必須在主要區域 (即容錯移轉前資料集所在的區域) 建立 Enterprise Plus 版預留項目。Enterprise Plus 預留項目包含配對區域中的待命運算資源。接著，您需要將資料集附加至這個預留項目，才能為該資料集啟用容錯移轉功能。只有在資料集已回填，且主要和次要位置與預留項目相同時，才能將資料集附加至預留項目。將資料集附加至容錯移轉預留項目後，只有 Enterprise Plus 預留項目可以寫入這些資料集，而且您無法對資料集執行[跨區域複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)升級。您可以使用任何容量模式，讀取附加至容錯移轉預留項目的資料集。如要進一步瞭解預留項目，請參閱「[工作負載管理簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。

容錯移轉後，次要區域會立即提供主要區域的運算能力。無論是否使用，這項可用性都適用於預留基準。

您必須主動選擇容錯移轉，做為測試的一部分或因應實際災難。10 分鐘內不應容錯移轉超過一次。在資料複製情境中，補充作業是指在資料集副本建立或啟用前，使用現有的歷來資料填入副本。資料集必須完成回填，才能容錯移轉至資料集。

下圖顯示代管災難復原的架構：

## 限制

BigQuery 災難復原功能有以下限制：

* BigQuery 災難復原功能與[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#limitations)功能有相同的限制。
* 容錯移轉預留項目最多可附加 1,000 個資料集。
* 如果現有預留項目有超過 1,000 個[預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，則無法轉換為容錯移轉預留項目。
* 如果查詢參照的資料集附加至同一管理專案中的多個容錯移轉預留項目，則所有預留項目都必須使用相同的次要位置。
* 資料集附加至容錯移轉預留項目後，只有 Enterprise Plus 預留項目可以寫入該資料集。您可以使用任何容量模式，從附加的資料集讀取資料。
* 如果資料集使用災難復原功能，載入和擷取工作就無法使用免費的共用運算單元集區。您必須建立 `PIPELINE` 類型的預留項目指派作業，因為只有 Enterprise Plus 版本支援寫入已設定災難復原的資料集。
* 容錯移轉後，自動調度資源功能會依據次要區域的可用運算資源而定。次要區域僅提供預留基準。
* 如果在初始建立資源期間複製失敗，系統就不會在次要區域建立預留項目，也無法進行硬式或軟式容錯移轉。
* 如要使用軟容錯移轉，主要和次要區域都必須可用。
* 如果預留項目設定變更尚未複製到次要區域，就無法啟動軟容錯移轉。如果發生任何複製錯誤，例如次要區域的運算單元配額不足或暫時性問題，軟性容錯移轉作業就無法啟動。
* 在軟性容錯移轉期間，您無法更新預留項目或附加資料集，但仍可讀取。
* 在容錯移轉作業期間，由於暫時性轉送變更，在有效軟性容錯移轉期間，在容錯移轉預留項目上執行的工作可能不會使用預留項目運算單元。這些工作會在軟式容錯移轉開始前和完成後使用預留項目運算單元。
* 容錯移轉後，[排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)不會自動重新導向至新的主要位置，因為這些查詢會繫結至建立時指定的位置。如要繼續執行排定的查詢，請在新的主要位置重新建立查詢。
* [`INFORMATION_SCHEMA.RESERVATIONS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw)不含容錯移轉詳細資料。如要列出預留項目的容錯移轉事件，請查詢 [`INFORMATION_SCHEMA.FAILOVER_HISTORY` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-failover-history?hl=zh-tw)。
* [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)只會顯示工作執行區域的工作記錄。主要區域工作記錄不會複製到次要區域。容錯移轉後，次要區域不會顯示主要區域的工作記錄。

## 位置

建立容錯移轉預留項目時，可使用下列區域：

| 位置代碼 | 地區名稱 | 地區說明 |
| --- | --- | --- |
| `AU` |  |  |
|  | `AUSTRALIA-SOUTHEAST1` | 雪梨 |
|  | `AUSTRALIA-SOUTHEAST2` | 墨爾本 |
| `CA` |  |  |
|  | `NORTHAMERICA-NORTHEAST1` | 蒙特婁 |
|  | `NORTHAMERICA-NORTHEAST2` | 多倫多 |
| `DE` |  |  |
|  | `EUROPE-WEST3` | 法蘭克福 |
|  | `EUROPE-WEST10` | 柏林 |
| `EU` |  |  |
|  | `EU` | 歐洲 (多區域) |
|  | `EUROPE-CENTRAL2` | 華沙 |
|  | `EUROPE-NORTH1` | 芬蘭 |
|  | `EUROPE-SOUTHWEST1` | 馬德里 |
|  | `EUROPE-WEST1` | 比利時 |
|  | `EUROPE-WEST3` | 法蘭克福 |
|  | `EUROPE-WEST4` | 荷蘭 |
|  | `EUROPE-WEST8` | 米蘭 |
|  | `EUROPE-WEST9` | 巴黎 |
| `IN` |  |  |
|  | `ASIA-SOUTH1` | 孟買 |
|  | `ASIA-SOUTH2` | 德里 |
| `US` |  |  |
|  | `US` | 美國 (多區域) |
|  | `US-CENTRAL1` | 愛荷華州 |
|  | `US-EAST1` | 南卡羅來納州 |
|  | `US-EAST4` | 北維吉尼亞州 |
|  | `US-EAST5` | 哥倫布 |
|  | `US-SOUTH1` | 達拉斯 |
|  | `US-WEST1` | 奧勒岡州 |
|  | `US-WEST2` | 洛杉磯 |
|  | `US-WEST3` | 鹽湖城 |
|  | `US-WEST4` | 拉斯維加斯 |

必須在`AU`、`CA`、`DE`、`EU`、`IN`或`US`內選取區域配對。舉例來說，`US` 內的區域無法與 `EU` 內的區域配對。

如果 BigQuery 資料集位於多區域位置，則無法使用下列區域組合。這項限制是為了確保容錯移轉預留項目和資料在複製後，會位於不同的地理位置。如要進一步瞭解多區域中的區域，請參閱「[多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)」。

* `us-central1` - `us` 多區域
* `us-west1` - `us` 多區域
* `eu-west1` - `eu` 多區域
* `eu-west4` - `eu` 多區域

## 事前準備

1. 確認您具備`bigquery.reservations.update` Identity and Access Management (IAM) 權限，可更新預留項目。
2. 確認您有已設定複製作業的現有資料集。詳情請參閱「[複製資料集](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#replicate_a_dataset)」。

## 強化型複製

災難復原功能會使用[強化型複製](https://docs.cloud.google.com/storage/docs/availability-durability?hl=zh-tw#turbo-replication)，加快跨區域資料複製速度，[降低資料遺失風險](https://docs.cloud.google.com/architecture/disaster-recovery?hl=zh-tw#step_1_gather_existing_requirements)、盡可能縮短服務停機時間，並在區域服務中斷後[協助支援不中斷的服務](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw#disaster_planning)。

強化型複製功能不適用於初始回填作業。初始補充作業完成後，只要未超過[頻寬配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#bandwidth_limits)且沒有使用者錯誤，強化型複製功能就會在 15 分鐘內，將資料集複製到具有次要副本的單一容錯移轉區域配對。

### 復原時間目標

復原時間目標 (RTO) 是指發生災難時，BigQuery 復原的目標時間。如要進一步瞭解 RTO，請參閱「[DR 規劃基本概念](https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide?hl=zh-tw)」。啟動容錯移轉後，代管災難復原的 RTO 為五分鐘。由於 RTO 的關係，在容錯移轉程序啟動後的五分鐘內，次要區域就會提供容量。

### 復原點目標

復原點目標 (RPO) 是指必須能還原資料的最近時間點。如要進一步瞭解 RPO，請參閱「[災難復原規劃基本概念](https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide?hl=zh-tw)」。代管災難復原的 RPO 是依資料集定義。RPO 的目標是讓次要副本與主要副本的資料差距保持在 15 分鐘內。如要達到這個 RPO，您不得超過[頻寬配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#bandwidth_limits)，且不得發生任何使用者錯誤。

## 配額

您必須先在次要區域中具備所選運算能力，才能設定容錯移轉預留項目。如果次要區域沒有可用配額，您就無法設定或更新預留項目。詳情請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#reservations)」。

### 容錯移轉預留項目的配額注意事項

設定代管災難復原時，容錯移轉預留項目的基準運算單元，會是次要區域中分配到的運算單元。即使預留項目處於閒置狀態，且未啟動容錯移轉，這些分配到的運算單元仍會在次要區域的「**Quotas & System Limits**」(配額與系統限制) 頁面中顯示為「已使用」。請確保管理專案在次要區域有足夠的運算單元配額，可容納容錯移轉預留項目的基準容量。如要進一步瞭解分配到的運算單元和配額用量，請參閱「[瞭解運算單元指標](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw#understand_slot_metrics)」。

強化型複製功能的頻寬有配額限制。詳情請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#bandwidth_limits)」。

## 定價

如要設定代管災難復原功能，必須採用下列定價方案：

* 運算容量：必須購買 [Enterprise Plus 版本](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。
* 強化型複製：災難復原功能在複製期間會使用強化型複製。系統會依據實體位元組數和複製的實體 GiB 計費。詳情請參閱「[強化型複製功能的資料複製資料移轉定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_replication)」。
* 儲存空間：次要區域的儲存空間位元組計費方式與主要區域相同。詳情請參閱「[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

客戶只需支付主要區域的運算容量費用。次要運算容量 (依據預留基準) 位於次要區域，不需額外付費。除非預留項目已容錯移轉，否則[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)無法使用次要運算資源。

如要在次要區域執行過時讀取作業，則必須[購買](https://cloud.google.com/bigquery/pricing?hl=zh-tw#overview_of_pricing)額外的運算資源。

代管災難復原功能支援 [BigQuery 流暢擴充](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fluid-scaling)。如要確保容錯移轉後，系統會按秒計費且不設最低時間長度，請務必在主要和次要區域啟用 BigQuery 流暢擴充功能。

## 建立或修改 Enterprise Plus 預留項目

**注意：**建立容錯移轉預留項目之前，請確認次要區域中沒有同名的預留項目。同樣地，請確保指派新的容錯移轉預留項目時，不會在次要位置重新指派相同工作類型的相同資源。這類衝突可能會導致複製失敗，造成主要和次要位置不一致。這可能會導致後續的容錯移轉作業失敗。

將資料集附加至預留項目之前，您必須先建立 Enterprise Plus 預留項目，或修改現有預留項目，並設定災難復原。

### 建立預留項目

請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 點選「Create reservation」(建立預留項目)。
4. 在「Reservation name」(預留項目名稱) 欄位中，輸入預留項目名稱。
5. 在「Location」(位置) 清單中選取位置。
6. 在「Edition」清單中，選取 Enterprise Plus 版本。
7. 在「Max reservation size selector」(預留項目大小上限選取器) 清單中，選取預留項目大小上限。
8. 選用：在「Baseline slots」(基準運算單元) 欄位中，輸入預留項目的基準運算單元數量。

   可用的自動調度資源運算單元數量，是從「Max reservation size」(預留項目大小上限) 值減去「Baseline slots」(基準運算單元) 值而得。舉例來說，如果您建立的預留項目有 100 個基準運算單元，且預留項目大小上限為 400，則預留項目會有 300 個自動調度資源運算單元。如要進一步瞭解基準運算單元，請參閱「[使用預留項目搭配基準和自動調度資源運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw#using_reservations_with_baseline_and_autoscaling_slots)」。
9. 在「Secondary location」(次要位置) 清單中，選取次要位置。
10. 如要停用[閒置運算單元共用](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)功能，並僅使用指定的運算單元容量，請按一下「Ignore idle slots」(忽略閒置運算單元) 切換鈕。
11. 如要展開「Advanced settings」(進階設定) 部分，請按一下 expand\_more 展開箭頭。
12. 選用：如要設定目標工作並行，請將「Override automatic target job concurrency」(覆寫自動目標工作並行) 切換鈕設為開啟，然後在「Target Job Concurrency」(目標工作並行) 中輸入值。「Cost estimate」(費用預估) 表格會顯示運算單元的細目。「Capacity summary」(容量摘要) 表格會顯示預留項目的摘要。
13. 按一下「儲存」。

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
   * `RESERVATION_NAME`：預留項目名稱。

     名稱開頭和結尾必須是小寫英文字母或數字，且只能包含小寫英文字母、數字和破折號。
   * `NUMBER_OF_BASELINE_SLOTS`：要
     分配給預留項目的基準運算單元數量。您無法在同一項預留項目中設定 `slot_capacity` 選項和 `edition` 選項。
   * `SECONDARY_LOCATION`：預留項目的次要[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果發生服務中斷，附加至這個預留項目的任何資料集都會容錯移轉至這個位置。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### 修改現有預留項目

請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 點選「Slot reservations」(運算單元預留項目) 分頁標籤。
4. 找出要更新的預訂。
5. 按一下 more\_vert「Reservations actions」(預留項目動作)，然後點選「Edit」(編輯)。
6. 在「Secondary location」(次要位置) 欄位中輸入次要位置。
7. 按一下「儲存」。

### SQL

如要新增或變更預留項目的次要位置，請使用 [`ALTER RESERVATION SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_reservation_set_options_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER RESERVATION
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME`
   SET OPTIONS (
     secondary_location = SECONDARY_LOCATION);
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID。
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，例如 `europe-west9`。
   * `RESERVATION_NAME`：預留項目的名稱。名稱開頭和結尾必須是小寫英文字母或數字，且只能包含小寫英文字母、數字和破折號。
   * `SECONDARY_LOCATION`：預留項目的次要[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果發生服務中斷，附加至這個預留項目的任何資料集都會容錯移轉至這個位置。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

## 將資料集附加至預留項目

如要為先前建立的預留項目啟用災難復原功能，請完成下列步驟。資料集必須已設定為在與預留項目相同的主要和次要區域中複製。詳情請參閱「[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#replicate_a_dataset)」。

**注意：**將資料集附加至容錯移轉預留項目後，只有 Enterprise Plus 預留項目可以寫入該資料集。您可以使用任何容量模式，讀取附加至容錯移轉預留項目的資料集。詳情請參閱「[限制](#limitations)」一節。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 點選「Slot reservations」(運算單元預留項目) 分頁標籤。
4. 按一下要附加資料集的預留項目。
5. 按一下「災難復原」分頁標籤。
6. 按一下「新增容錯移轉資料集」。
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

## 將資料集與預留項目取消連結

如要停止透過預留項目管理資料集的容錯移轉行為，請將資料集與預留項目取消連結。這項操作不會變更資料集目前的主要副本，也不會移除任何現有的資料集副本。如要進一步瞭解如何在卸載資料集後移除資料集副本，請參閱「[移除資料集副本](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#remove_a_dataset_replica)」。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，依序點選「Workload management」(工作負載管理) 和「Slot reservations」(運算單元預留項目) 分頁標籤。
3. 按一下要取消連結資料集的預留項目。
4. 按一下「災難復原」分頁標籤。
5. 展開資料集主要副本的 more\_vert「Actions」(動作) 選項。
6. 按一下 [移除]。

### SQL

如要將資料集與預留項目解除連結，請使用 [`ALTER SCHEMA SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER SCHEMA
     `DATASET_NAME`
   SET OPTIONS (
     failover_reservation = NULL);
   ```

   替換下列內容：

   * `DATASET_NAME`：資料集名稱。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

## 啟動容錯移轉

如果發生區域性服務中斷，您必須手動將預留項目容錯移轉至副本使用的位置。預留項目容錯移轉時，也會一併移轉任何相關聯的資料集。如要手動容錯移轉預留項目，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Disaster recovery」(災難復原)。
3. 按一下要容錯移轉至的預留項目名稱。
4. 選取「硬式容錯移轉模式 (預設)」或「軟式容錯移轉模式」。
5. 按一下「容錯移轉」。

### SQL

如要為預留項目新增或變更次要位置，請使用 [`ALTER RESERVATION SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_reservation_set_options_statement)，並將 `is_primary` 設為 `TRUE`。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER RESERVATION
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME`
   SET OPTIONS (
     is_primary = TRUE, failover_mode=FAILOVER_MODE);
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID。
   * `LOCATION`：預留項目的新主要[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，也就是容錯移轉前的目前次要位置，例如 `europe-west9`。
   * `RESERVATION_NAME`：預留項目的名稱。名稱開頭和結尾必須是小寫英文字母或數字，且只能包含小寫英文字母、數字和破折號。
   * `PRIMARY_STATUS`：布林值狀態，宣告預留項目是否為主要副本。
   * `FAILOVER_MODE`：選用參數，用於說明容錯移轉模式。可設為 `HARD` 或 `SOFT`。如未指定這個參數，系統預設會使用 `HARD`。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

## 監控備用資源

您可以透過 BigQuery、Cloud Monitoring 或 `INFORMATION_SCHEMA` 檢視畫面，監控資料集副本的狀態。

如要瞭解如何為這些指標建立警告，請參閱「[建立資訊主頁、圖表和警告](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw)」。

### 使用 BigQuery 查看複製狀態

如要在Google Cloud 控制台查看資料集的複製狀態和延遲時間，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中展開專案。
3. 按一下要監控的資料集。
4. 在資料集詳細資料窗格中，按一下「Details」(詳細資料) 分頁標籤。
5. 在「副本」部分，查看「複製延遲時間」和「狀態」。如要查看更多詳細資料 (包括複製延遲時間圖表)，請按一下「View details」(查看詳細資料)。

### 使用 Cloud Monitoring 查看複製狀態

BigQuery 在 Monitoring 中提供下列指標，協助您監控複製狀態：

* **複製延遲時間**：次要區域內資料的過時程度，這些資料是透過跨區域複製或代管災難復原作業複製。這項指標可做為復原點目標 (RPO) 的代理指標。
* **網路輸出位元組數**：從主要區域複製到次要區域的計費資料量 (以位元組為單位)。這項指標可協助您監控頻寬配額使用率。

如要在 Monitoring 中查看這些指標，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Monitoring」頁面。

   [前往「Monitoring」](https://console.cloud.google.com/monitoring?hl=zh-tw)
2. 按一下「Metrics Explorer」。
3. 在「選取指標」欄位中，搜尋並選取「BigQuery 資料集」。
4. 選取「Replication latency」(複製延遲時間) (`bigquery.googleapis.com/storage/replication/dataset_staleness`) 或「Network egress bytes」(網路輸出位元組) (`bigquery.googleapis.com/storage/replication/network_egress_bytes_count`)。
5. 按一下「套用」。
6. 在「Aggregation」(匯總) 部分，選取匯總方法。針對複製延遲時間指標，建議選取「99th percentile」(第 99 個百分位數)。與平均值或其他匯總值相比，這項匯總值更能反映最差的成效。
7. 選用：如要查看特定資料集或次要區域的指標，請按一下「Add filter」(新增篩選器)，選取「dataset\_id」或「location」選項，然後輸入值。如果將資料複製到多個次要區域，可以依位置分組，查看各區域的指標。

### 使用 `INFORMATION_SCHEMA` 查看複製狀態

如要判斷副本狀態，請查詢 [`INFORMATION_SCHEMA.SCHEMATA_REPLICAS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-schemata-replicas?hl=zh-tw)。例如：

```
SELECT
  schema_name,
  replica_name,
  creation_complete,
  replica_primary_assigned,
  replica_primary_assignment_complete
FROM
  `region-LOCATION`.INFORMATION_SCHEMA.SCHEMATA_REPLICAS
WHERE
  schema_name="my_dataset"
```

下列查詢會傳回過去七天內，如果資料集是容錯移轉資料集，就會失敗的工作。如要查詢整個組織的工作，請將 `INFORMATION_SCHEMA.JOBS` 替換為 [`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-organization?hl=zh-tw)，並省略 `jobs.query`，因為 `INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視畫面不含查詢文字：

```
SELECT
  jobs.project_id AS job_project_id,
  jobs.job_id,
  jobs.job_type,
  jobs.statement_type,
  jobs.reservation_id,
  jobs.edition,
  jobs.destination_table.project_id AS dataset_project_id,
  jobs.destination_table.dataset_id,
  jobs.destination_table.table_id,
  jobs.query
FROM
  `PROJECT_ID.region-LOCATION`.INFORMATION_SCHEMA.JOBS AS jobs
WHERE
  jobs.creation_time
    BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
    AND CURRENT_TIMESTAMP()
  AND jobs.destination_table.project_id = 'DATASET_PROJECT_ID'
  AND jobs.destination_table.dataset_id = 'DATASET_ID'
  AND (jobs.edition IS NULL OR jobs.edition != 'ENTERPRISE_PLUS');
```

更改下列內容：

* `PROJECT_ID`：執行工作的專案 ID。
* `LOCATION`：[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
* `DATASET_PROJECT_ID`：目的地資料集所在的專案 ID。
* `DATASET_ID`：您打算附加至容錯移轉預留項目的資料集 ID。

## 後續步驟

* 查詢 [`INFORMATION_SCHEMA.FAILOVER_HISTORY`](https://docs.cloud.google.com/bigquery/docs/information-schema-failover-history?hl=zh-tw)，查看預留項目的容錯移轉事件。
* 進一步瞭解[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)。
* 進一步瞭解[可靠性](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-08 (世界標準時間)。"],[],[]]