* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 跨區域資料集複製

透過 BigQuery 資料集複製功能，您可以在兩個不同的區域或多區域之間，設定自動複製資料集。

## 總覽

在 BigQuery 中建立資料集時，您會選取資料儲存的區域或多區域。「區域」是指地理區域內的資料中心集合，「多區域」是指包含兩個以上地理區域的大型地理區域。您的資料會儲存在其中一個所含區域，且不會在多區域內複製。如要進一步瞭解單一地區與多地區，請參閱 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

BigQuery 一律會將資料副本儲存在資料集位置內的兩個不同Google Cloud 可用區。「可用區」是區域內 Google Cloud 資源的部署範圍。在所有區域中，區域間的複製作業都會使用同步雙重寫入。選取多區域位置不會提供跨區域複製或區域備援功能，因此如果發生區域服務中斷，資料集可用性不會提高。資料會儲存在地理位置內的單一區域。

如要提高異地備援能力，可以複製任何資料集。
BigQuery 會在您指定的另一個區域建立資料集的次要副本。然後，這項副本會以非同步方式在兩個區域之間複製，總共會有四個區域副本。

### 資料集複製

如果複製資料集，BigQuery 會將資料儲存在您指定的區域。

* **主要區域**。首次建立資料集時，BigQuery 會將資料集放在主要區域。
* **次要區域**。新增資料集副本時，BigQuery 會將副本放在次要區域。

一開始，主要地區的副本是*主要副本*，次要地區的副本則是*次要副本*。

主要副本可寫入，次要副本則為唯讀。寫入主要備用資源的資料會非同步複製到次要備用資源。在每個區域內，資料會備援儲存在兩個可用區。網路流量絕不會離開 Google Cloud 網路。

下圖顯示複製資料集時發生的複製作業：

如果主要區域處於連線狀態，您可以手動切換至次要副本。詳情請參閱「[升級次要副本](#promote_the_secondary_replica)」。

### 定價

系統會針對複製的資料集收取下列費用：

* **儲存空間。**次要區域的儲存空間位元組會以次要區域的個別副本計費。次要副本中的資料表和分區不會重設為[長期儲存空間](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)中的動態儲存空間。
* **資料複製。**如要進一步瞭解資料複製的計費方式，請參閱[資料複製定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_replication)。

資料複製作業由 BigQuery 管理，不會使用您的[時段資源](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)。資料複製費用會另外計費。

### 次要區域的運算資源

如要針對次要區域中的副本執行工作和查詢，您必須在次要區域內購買[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)，或執行隨選查詢。

您可以使用這些位置，從次要副本執行唯讀查詢。如果將次要副本升級為主要副本，您也可以使用這些時段寫入副本。

您可以購買與主要區域相同或不同數量的運算單元。如果購買的運算單元較少，可能會影響查詢效能。

## 位置注意事項

如要新增資料集副本，請先在 BigQuery 中建立要複製的初始資料集 (如果尚未建立)。新增副本的位置會設為您新增副本時指定的位置。新增副本的位置必須與初始資料集的位置不同。也就是說，資料集中的資料會持續在資料集建立位置和副本位置之間複製。對於需要共置的副本 (例如檢視區塊、具體化檢視區塊或非 BigLake 外部資料表)，如果副本的位置與來源資料的位置不同或不相容，可能會導致工作發生錯誤。

當客戶跨區域複製資料集時，BigQuery 會確保資料只位於建立副本的位置。

### 主機代管規定

使用資料集複製功能時，必須符合下列共置需求。

#### Cloud Storage

如要查詢 Cloud Storage 中的資料，Cloud Storage 值區必須與副本位於同一位置。決定副本的放置位置時，請考量[外部資料表位置](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#data-locations)。

## 限制

BigQuery 資料集複製作業有下列限制：

* 透過 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) 或 [`tabledata.insertAll`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll?hl=zh-tw) 方法寫入主要副本的串流資料會複製到次要副本，但這項作業是盡力而為，因此複製作業可能會延遲。
* 從 [Datastream](https://cloud.google.com/datastream-for-bigquery?hl=zh-tw) 或 [BigQuery 變更資料擷取擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)寫入主要副本的串流 upsert 作業，會盡可能複製到次要副本，但可能會有較長的複製延遲時間。複製完成後，次要副本中的 upsert 會根據表格設定的[`max_staleness`](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw#manage_table_staleness)值，合併至次要副本的表格基準。
* 您無法在已複製資料集的資料表上啟用[精細 DML](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#fine-grained_dml)，也無法複製含有已啟用精細 DML 資料表的資料集。
* 您可以使用 Google Cloud 控制台
  或 SQL [資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)管理複製作業和切換作業。
* 每個區域或多區域最多只能有一個資料集副本。您無法在同一個目的地區域中，為同一個資料集建立兩個次要副本。
* 副本中的資源會受到「[資源行為](#resource-behavior)」一節所述的限制。
* [政策標記](https://docs.cloud.google.com/bigquery/docs/managing-policy-tags-across-locations?hl=zh-tw)和相關聯的資料政策不會複製到次要副本。如果使用者沒有專案、資料夾或機構層級的 `roles/datacatalog.categoryFineGrainedReader` 角色，即使升級複本，在原始區域以外的區域中，凡是參照含有政策標記資料欄的查詢都會失敗。
* 次要副本建立完成後，才能在次要副本中使用[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)功能。
* 如要在資料集上啟用跨區域複製功能，目的地區域的大小上限 (以邏輯位元組為單位) 預設為：`us` 和 `eu`
  [多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions) 10 PB，其他[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions) 500 TB。這些限制可設定。如需更多資訊，請與[Google Cloud 支援團隊](https://cloud.google.com/support-hub?hl=zh-tw)聯絡。
* 這項配額適用於邏輯資源。
* 您只能複製資料表少於 10 萬個的資料集。
* 每個資料集每天最多只能在同一區域新增 (然後捨棄) 4 個副本。
* 您受到[頻寬](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#bandwidth_limits)限制。
* 如果未設定 `replica_kms_key` 值，則無法在次要區域查詢套用[客戶管理的加密金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) (CMEK) 的資料表。
* 不支援 BigLake 資料表。
* 您無法複製外部或聯邦資料集。
* 不支援 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)。
* 如果您要為[災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)設定資料複製功能，則無法設定下列區域配對：
  + `us-central1` - `us` 多區域
  + `us-west1` - `us` 多區域
  + `eu-west1` - `eu` 多區域
  + `eu-west4` - `eu` 多區域
* 無法複製常式層級的存取權控管，但可以複製常式的資料集層級存取權控管。
* 搜尋索引的運作方式如下：
  + 只有搜尋索引中繼資料會複製到次要區域，索引資料本身不會複製。
  + 如果切換至副本，系統會從先前的主要區域刪除索引，並在升級的區域中重新產生索引。
  + 如果在 8 小時內來回切換，索引產生作業就會延遲 8 小時。
* 您無法複製隱藏的資料集。

### 資源行為

次要副本中的資源不支援下列作業：

* [建立資料表副本](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_clone_statement)
* [建立資料表快照](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_snapshot_table_statement)

次要副本為唯讀狀態。如要在次要副本中建立資源副本，您必須先複製或查詢資源，然後在次要副本外部實現結果。舉例來說，您可以使用 [CREATE TABLE AS SELECT](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，從次要副本資源建立新資源。

主要和次要副本有以下差異：

| 區域 1 主要副本 | 區域 2 次要副本 | 附註 |
| --- | --- | --- |
| BigLake 資料表 | BigLake 資料表 | 不支援。 |
| BigLake Apache Iceberg 資料表 | BigLake Apache Iceberg 資料表 | 請參閱「[Lakehouse 執行階段目錄跨區域複製和災難復原](https://docs.cloud.google.com/biglake/docs/about-managed-disaster-recovery?hl=zh-tw)」。 |
| 外部資料表 | 外部資料表 | 系統只會複製外部資料表定義。如果 Cloud Storage bucket 與副本不在同一個位置，查詢就會失敗。 |
| 邏輯檢視畫面 | 邏輯檢視畫面 | 如果邏輯檢視區塊參照的資料集或資源與邏輯檢視區塊不在相同位置，查詢時就會失敗。 |
| 受管理資料表 | 代管資料表 | 沒有差別。 |
| 具體化檢視表 | 具體化檢視表 | 如果參照的資料表與具體化檢視表不在同一區域，查詢就會失敗。如果複製的具體化檢視表過時，系統會在檢視表「最大過時」上方顯示過時狀態。 |
| 型號 | 型號 | 儲存為代管資料表。 |
| 遠端功能 | 遠端功能 | 連線是區域資源。如果參照的資料集或資源 (連線) 與遠端函式不在相同位置，遠端函式在執行時就會失敗。 |
| 處理常式 | 使用者定義函式 (UDF) 或預存程序 | 如果常式參照的資料集或資源與常式不在相同位置，執行時就會失敗。任何參照連線的常式 (例如遠端函式) 都無法在來源區域外運作。 |
| 資料列存取政策 | 資料列存取政策 | 沒有差別。 |
| 搜尋索引 | 搜尋索引 | 只會複製索引中繼資料。索引資料只會存在於主要區域。 |
| 預存程序 | 預存程序 | 如果儲存的程序參照的資料集或資源與儲存的程序不在同一位置，執行時就會失敗。 |
| 資料表副本 | 代管資料表 | 在次要副本中以深層副本計費。 |
| 資料表快照 | 資料表快照 | 在次要副本中以深層副本計費。 |
| 資料表值函式 (TVF) | TVF | 如果 TVF 參照的資料集或資源與 TVF 位於不同位置，執行時就會失敗。 |
| UDF | UDF | 如果 UDF 參照的資料集或資源與 UDF 位於不同位置，執行時就會失敗。 |
| 資料欄的資料政策 | 資料欄的資料政策 | 如果自訂資料政策參照的 UDF 與政策不在相同位置，查詢附加政策的資料表時就會失敗。 |

## 服務中斷情境

跨區域複製功能不適合在整個區域服務中斷時，做為災難復原計畫使用。如果主要副本所在區域全面中斷服務，您就無法升級次要副本。由於次要備用資源是唯讀資源，因此您無法在次要備用資源上執行任何寫入工作，也無法升級次要區域，直到主要備用資源的區域還原為止。如要進一步瞭解如何準備災難復原，請參閱「[受管理災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)」。

下表說明區域全面中斷對複寫資料的影響：

| 區域 1 | 區域 2 | 服務中斷區域 | 影響 |
| --- | --- | --- | --- |
| 主要副本 | 次要副本 | 區域 2 | 在區域 2 中針對次要副本執行的唯讀工作會失敗。 |
| 主要副本 | 次要副本 | 區域 1 | 在區域 1 中執行的所有工作都會失敗。唯讀工作會繼續在區域 2 執行，也就是次要副本所在的區域。在成功與區域 1 同步前，區域 2 的內容會過時。 |

## 使用資料集複製功能

本節說明如何複製資料集、升級次要副本，以及在次要區域執行 BigQuery 讀取工作。

### 所需權限

如要取得管理副本所需的權限，請要求管理員授予您 `bigquery.datasets.update` 權限。

### 複製資料集

如要複製資料集，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下要複製的資料集。
3. 點按「Details」(詳細資料) 分頁標籤。
4. 在「副本」部分，按一下「建立副本」。
5. 在「建立資料集副本」窗格中，執行下列操作：

   1. 在「位置類型」部分，選取副本的位置類型。
   2. 在「Region」(區域) 清單中，選取副本所在的區域。
   3. 選用步驟：如要使用客戶管理的加密金鑰 (CMEK)，請展開「Advanced options」(進階選項) 部分，然後選取「Customer-managed encryption key (CMEK)」(客戶管理的加密金鑰 (CMEK)) 選項。
6. 按一下「建立備用資源」。

### SQL

如要複製資料集，請使用 [`ALTER SCHEMA ADD REPLICA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_add_replica_statement)。

您可以為位於區域或多區域的任何資料集新增副本，但該區域或多區域中不得已有該資料集的副本。新增副本後，初始複製作業需要一段時間才能完成。資料複製期間，您仍可執行參照主要副本的查詢，查詢處理容量不會減少。您無法在多區域內複製地理位置的資料。

下列範例會在 `us-central1` 區域中建立名為 `my_dataset` 的資料集，然後在 `us-east4` 區域中新增副本：

```
-- Create the primary replica in the us-central1 region.
CREATE SCHEMA my_dataset OPTIONS(location='us-central1');

-- Create a replica in the secondary region.
ALTER SCHEMA my_dataset
ADD REPLICA `my_replica`
OPTIONS(location='us-east4');
```

如要確認何時成功建立次要副本，可以查詢 [`INFORMATION_SCHEMA.SCHEMATA_REPLICAS`](https://docs.cloud.google.com/bigquery/docs/information-schema-schemata-replicas?hl=zh-tw) 檢視中的 `creation_complete` 欄。

建立次要副本後，您可以明確[設定查詢位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)為次要區域，藉此查詢次要副本。如果未明確設定位置，BigQuery 會使用資料集主要副本的區域。

### 升級次要副本

如果主要區域處於連線狀態，您可以升級次要副本。
升級後，次要副本就會成為可寫入的主要副本。如果次要備用資源與主要備用資源同步，這項作業會在幾秒內完成。如果次要副本未趕上進度，升級作業就無法完成，直到次要副本趕上進度為止。如果主要區域發生服務中斷情形，次要備用資源就無法升級為主要資源。

注意事項：

* 升級程序進行期間，所有寫入資料表的作業都會傳回錯誤。升級作業開始後，舊的主要副本會立即變成不可寫入。
* 促銷活動啟動時未完全複製的資料表會傳回過時的讀取內容。

如要將副本升級為主要副本，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下要升級的資料集。
3. 點按「Details」(詳細資料) 分頁標籤。
4. 在「副本」部分中，找出要升級的副本，然後按一下「設為主要」。
5. 在「Promote replica」對話方塊的文字欄位中輸入 `confirm`，然後按一下「Confirm」。

### SQL

如要將備用資源升級為主要備用資源，請使用 [`ALTER SCHEMA SET
OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)，並設定 `primary_replica` 選項。

注意事項：

* 您必須在查詢設定中，明確將工作位置設為次要區域。詳情請參閱「[BigQuery 指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)」一文。

以下範例會將 `us-east4` 副本升級為主要副本：

```
ALTER SCHEMA my_dataset SET OPTIONS(primary_replica = 'us-east4');
```

如要確認次要副本何時升級成功，可以查詢 [`INFORMATION_SCHEMA.SCHEMATA_REPLICAS`](https://docs.cloud.google.com/bigquery/docs/information-schema-schemata-replicas?hl=zh-tw) 檢視中的 `replica_primary_assignment_complete` 欄。

### 移除資料集副本

如要移除副本並停止複製資料集，請選取下列任一選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下要移除副本的資料集。
3. 點按「Details」(詳細資料) 分頁標籤。
4. 在「副本」部分中，找出要移除的副本，然後依序按一下「更多動作」more\_vert 和「刪除」。
5. 在「Delete dataset replica?」(要刪除資料集副本嗎？) 對話方塊中，在文字欄位輸入 `delete`，然後按一下「Delete」(刪除)。

### SQL

如要移除副本並停止複製資料集，請使用 [`ALTER SCHEMA DROP REPLICA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_drop_replica_statement)。

以下範例會移除 `us` 副本：

```
ALTER SCHEMA my_dataset
DROP REPLICA IF EXISTS `us`;
```

如要刪除整個資料集，必須先捨棄所有次要副本。如果您刪除整個資料集 (例如使用 [`DROP
SCHEMA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_schema_statement))，但未捨棄所有次要副本，系統會顯示下列錯誤訊息：

```
The dataset replica of the cross region dataset 'project_id:dataset_id' in region 'REGION' is not yet writable because the primary assignment is not yet complete.
```

詳情請參閱「[升級次要副本](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#promote_the_secondary_replica)」。

## 監控備用資源

您可以透過 BigQuery、Cloud Monitoring 或 `INFORMATION_SCHEMA` 檢視畫面，監控資料集副本的狀態。

如要瞭解如何針對這些指標建立快訊，請參閱「[建立資訊主頁、圖表和快訊](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw)」。

### 使用 BigQuery 查看複製狀態

如要在Google Cloud 控制台中查看資料集的複製狀態和延遲時間，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中展開專案。
3. 按一下要監控的資料集。
4. 在資料集詳細資料窗格中，按一下「詳細資料」分頁標籤。
5. 在「副本」部分中，查看「複寫延遲」和「狀態」。如要查看更多詳細資料，包括複寫延遲圖表，請按一下「查看詳細資料」。

### 使用 Cloud Monitoring 查看複製狀態

BigQuery 會在 Monitoring 中提供下列指標，協助您監控複製狀態：

* **複製延遲時間**：次要區域內資料的過時程度，這些資料是透過跨區域複製或代管災難復原作業複製。這項指標可做為復原點目標 (RPO) 的替代指標。
* **網路輸出位元組**：從主要區域複製到次要區域的資料量 (以位元組為單位)，會據此計費。這項指標有助於監控頻寬配額用量。

如要在 Monitoring 中查看這些指標，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Monitoring」頁面。

   [前往「Monitoring」](https://console.cloud.google.com/monitoring?hl=zh-tw)
2. 按一下「指標探索工具」。
3. 在「選取指標」欄位中，搜尋並選取「BigQuery 資料集」。
4. 選取「複寫延遲時間」 (`bigquery.googleapis.com/storage/replication/dataset_staleness`) 或「網路輸出位元組」 (`bigquery.googleapis.com/storage/replication/network_egress_bytes_count`)。
5. 按一下「套用」。
6. 在「匯總」部分，選取匯總方法。對於複寫延遲指標，建議選取「第 99 個百分位數」。相較於平均值或其他匯總資料，這項匯總資料更能顯示最差的成效。
7. 選用：如要查看特定資料集或次要區域的指標，請按一下「新增篩選條件」，選取「dataset\_id」或「location」選項，然後輸入值。如果將資料複製到多個次要區域，可以依位置分組，查看每個區域的指標。

### 使用 `INFORMATION_SCHEMA` 查看複製狀態

如要列出專案中的資料集副本，請查詢 [`INFORMATION_SCHEMA.SCHEMATA_REPLICAS`](https://docs.cloud.google.com/bigquery/docs/information-schema-schemata-replicas?hl=zh-tw) 檢視區塊。

## 遷移資料集

您可以使用跨區域資料集複製功能，將資料集從一個區域遷移至另一個區域。以下範例說明如何使用跨區域複製功能，將現有的 `my_migration` 資料集從 `US` 多區域遷移至 `EU` 多區域。

### 複製資料集

如要開始遷移程序，請先在要遷移資料的區域中複製資料集。在這個情境中，您要將 `my_migration` 資料集遷移至 `EU` 多區域。

```
-- Create a replica in the secondary region.
ALTER SCHEMA my_migration
ADD REPLICA `eu`
OPTIONS(location='eu');
```

這項操作會在 `EU` 多區域中建立名為 `eu` 的次要副本。主要副本是`US`多區域中的`my_migration`資料集。

### 升級次要副本

如要繼續將資料集遷移至 `EU` 多區域，請升級次要副本：

```
ALTER SCHEMA my_migration SET OPTIONS(primary_replica = 'eu')
```

升級完成後，`eu` 即為主要副本。這是可寫入的副本。

### 完成遷移作業

如要完成從 `US` 多區域到 `EU` 多區域的遷移作業，請刪除 `us` 副本。這個步驟並非必要，但如果您不需要遷移作業以外的資料集副本，這個步驟就很有用。

```
ALTER SCHEMA my_migration
DROP REPLICA IF EXISTS us;
```

您的資料集位於 `EU` 多區域，且沒有 `my_migration` 資料集的副本。您已成功將資料集遷移至 `EU` 多區域。如要查看遷移的完整資源清單，請參閱「[資源行為](#resource-behavior)」。

## 由客戶管理的加密金鑰 (CMEK)

建立次要副本時，系統不會自動複製[客戶代管的 Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如要維持複製資料集的加密狀態，您必須為新增副本的位置設定 `replica_kms_key`。您可以使用 [`ALTER SCHEMA ADD REPLICA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_add_replica_statement)設定 `replica_kms_key`。

使用 CMEK 複製資料集時，行為如下列情境所述：

* 如果來源資料集有 `default_kms_key`，使用 `ALTER SCHEMA ADD REPLICA` DDL 陳述式時，您必須提供在副本資料集區域中建立的 `replica_kms_key`。
* 如果來源資料集未設定 `default_kms_key` 的值，您就無法設定 `replica_kms_key`。
* 如果您在 `default_kms_key` 或 `replica_kms_key` 上使用[Cloud KMS 金鑰輪替](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_rotation)，金鑰輪替後，您仍可查詢複製的資料集。

  + 主要區域的金鑰輪替只會更新輪替後建立的資料表金鑰版本，輪替前建立的資料表仍會使用輪替前設定的金鑰版本。
  + 次要區域的金鑰輪替作業會將次要副本中的所有資料表更新為新金鑰版本。
  + 將主要備用資源切換為次要備用資源後，次要備用資源 (原為主要備用資源) 中的所有資料表都會更新為新金鑰版本。
  + 如果刪除金鑰輪替前在主要副本資料表上設定的金鑰版本，則在更新金鑰版本前，仍使用金鑰輪替前設定的金鑰版本的資料表都無法查詢。如要更新金鑰版本，舊金鑰版本必須處於啟用狀態 (不得停用或刪除)。
* 如果來源資料集未設定 `default_kms_key` 的值，但來源資料集中的個別資料表已套用 CMEK，則無法在複製的資料集中查詢這些資料表。如要查詢資料表，請按照下列步驟操作：

  + 為來源資料集新增 `default_kms_key` 值。
  + 使用 `ALTER SCHEMA ADD REPLICA` DDL 陳述式建立新副本時，請為 `replica_kms_key` 選項設定值。您可以在目的地區域查詢 CMEK 資料表。

  無論來源區域使用的金鑰為何，目的地區域中的所有 CMEK 資料表都會使用相同的 `replica_kms_key`。

### 使用 CMEK 建立副本

以下範例會在 `us-west1` 區域建立副本，並設定 `replica_kms_key` 值。如果是 CMEK 金鑰，請[授予 BigQuery 服務帳戶加密和解密權限](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#grant_permission)。

```
-- Create a replica in the secondary region.
ALTER SCHEMA my_dataset
ADD REPLICA `us-west1`
OPTIONS(location='us-west1',
  replica_kms_key='my_us_west1_kms_key_name');
```

### CMEK 限制

複製已套用 CMEK 的資料集時，會受到下列限制：

* 建立副本後，您就無法更新複製的 Cloud KMS 金鑰。
* 建立資料集副本後，就無法更新來源資料集的「`default_kms_key`」值。
* 如果提供的 `replica_kms_key` 在目的地區域無效，系統就不會複製資料集。

## 指派給資料欄的資料政策

以下各節說明[直接指派給資料欄的資料政策](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw#data-policies-on-column)
[(預覽版)](https://cloud.google.com/products?hl=zh-tw#product-launch-stages) 如何與跨區域複寫互動。

指派給資料欄的資料政策是區域資源。也就是說，資料政策和附加的資料表必須位於相同區域。建立次要副本時，系統會自動複製資料政策。如果資料政策附加至複製資料集中的任何資料表，BigQuery 會在次要區域建立或更新資料政策及其對應的 IAM 政策。

### 可變動性

複製的資料政策在次要區域中為唯讀。您無法在次要區域[更新資料政策](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw#update-data-policies-on-column)。主要區域中資料表附加的原始資料政策仍可變更。只有在資料地區政策未附加至任何次要資料表時，才能變更。如果附加至次要區域的資料表，就會變成不可變動。如果資料政策不可變更，BigQuery 會拒絕更新或設定 IAM 政策的任何作業。

### 命名衝突

主要和次要區域的資料政策資源相同，但位置除外。對於資料政策及其在次要區域的副本，格式為 `projects/PROJECT_NUMBER/locations/LOCATION_ID/dataPolicies/DATA_POLICY_ID` 的 ID 完全相同，但 `LOCATION_ID` 的值除外。如果次要區域中已有 ID 衝突的資料政策，複製作業就會失敗。您必須先解決主要或次要區域的命名衝突，才能繼續複製作業。

### 自訂遮蓋政策

如果您使用[自訂遮蓋常式](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#masking_options)，請務必複製自訂 UDF。您可以將這些 UDF 納入要複製的資料集。

### 將資料政策附加至資料表欄、從資料表欄卸離或刪除資料政策

在主要區域中，將資料政策附加至資料欄或從資料欄卸離/刪除，都屬於資料表結構定義變更。所有次要區域的資料表結構定義都會更新，以反映這項變更。不過，如果從主要區域的所有資料表欄卸離資料政策，資料政策就會在次要區域中成為孤立政策，您必須手動清理。不建議在次要區域手動附加複製的資料政策，因為這可能會導致複雜的情況，例如無法新增或移除 FGAC 授權。

如果刪除已卸離的資料政策，背景工作會將其從資料表結構描述中移除。發生這種情況時，資料表結構定義變更會傳播至目的地區域。與卸離政策一樣，您必須手動刪除次要區域中的資料政策。

### 捨棄副本

如果捨棄副本，系統不會自動刪除附加的資料政策。與卸離政策一樣，您必須手動刪除次要區域中的資料政策。

## 後續步驟

* 瞭解如何使用 [BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)。
* 瞭解 [BigQuery 可靠性功能](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]