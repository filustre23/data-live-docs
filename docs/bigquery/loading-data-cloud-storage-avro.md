Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Cloud Storage 載入 Avro 資料

[Avro](https://avro.apache.org) 是將序列化資料與資料結構定義結合於相同檔案的開放原始碼資料格式。

從 Cloud Storage 載入 Avro 資料時，可將資料載入至新的資料表或分區，或將資料附加到現有資料表或分區，或覆寫現有資料表或分區。將資料載入至 BigQuery 時，資料會轉換為 [Capacitor 列表型格式](https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw)
(BigQuery 的儲存格式)。

將資料從 Cloud Storage 載入 BigQuery 資料表時，該資料表所屬的資料集必須位於和 Cloud Storage bucket 相同的地區或多地區位置。

如需從本機檔案載入 Avro 資料的相關資訊，請參閱[將資料從本機資料來源載入至 BigQuery](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#loading_data_from_local_files)。

## 限制

將資料從 Cloud Storage 值區載入 BigQuery 時有下列限制：

* BigQuery 不保證外部資料來源的資料一致性。如果基礎資料在查詢執行期間遭到變更，可能會導致非預期的行為。
* BigQuery 不支援 [Cloud Storage 物件版本控管](https://docs.cloud.google.com/storage/docs/object-versioning?hl=zh-tw)。如果 Cloud Storage URI 中包含版本編號，載入作業就會失敗。

將 Avro 檔案載入 BigQuery 時，也適用下列限制：

* BigQuery 不支援載入獨立的 Avro 結構定義 (.avsc) 檔案。
* BigQuery 不支援巢狀陣列格式。使用這種格式的 Avro 檔案必須先經過轉換，才能匯入。
* 在 Avro 檔案中，全名名稱和命名空間只能包含英數字元和底線字元 `_`。以下是允許的字元：`[A-Za-z_][A-Za-z0-9_]*`。

如要瞭解 BigQuery 載入工作限制，請參閱[載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)。

## 輸入檔案規定

如要避免將 Avro 檔案載入 BigQuery 時發生 `resourcesExceeded` 錯誤，請遵守下列規範：

* 資料列大小不得超過 50 MB。
* 如果資料列包含許多陣列欄位，或任何非常長的陣列欄位，請將陣列值分成多個欄位。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文中各項工作所需的權限，並建立資料集和資料表來儲存資料。

### 所需權限

如要將資料載入 BigQuery，您需要具備執行載入工作，以及將資料載入 BigQuery 資料表和分區的 IAM 權限。如要從 Cloud Storage 載入資料，您也需要 IAM 權限，才能存取包含資料的值區。

#### 將資料載入 BigQuery 的權限

如要將資料載入新的 BigQuery 資料表或分區，或是附加或覆寫現有的資料表或分區，您需要下列 IAM 權限：

* `bigquery.tables.create`
* `bigquery.tables.updateData`
* `bigquery.tables.update`
* `bigquery.jobs.create`

以下每個預先定義的 IAM 角色都包含將資料載入 BigQuery 資料表或分區所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin` (包括 `bigquery.jobs.create` 權限)
* `bigquery.user` (包括 `bigquery.jobs.create` 權限)
* `bigquery.jobUser` (包括 `bigquery.jobs.create` 權限)

此外，如果您具備 `bigquery.datasets.create` 權限，就能在您建立的資料集中，使用載入工作建立及更新資料表。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

### 從 Cloud Storage 載入資料的權限

如要取得從 Cloud Storage bucket 載入資料所需的權限，請要求管理員授予您 bucket 的「[Storage 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin) 」(`roles/storage.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備從 Cloud Storage 值區載入資料所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要從 Cloud Storage 值區載入資料，您必須具備下列權限：

* `storage.buckets.get`
* `storage.objects.get`
* `storage.objects.list (required if you are using a URI wildcard)`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 建立資料集和資料表

如要儲存資料，您必須建立 [BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，然後在該資料集中建立 [BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)。

## Avro 的優勢

如要將資料載入 BigQuery，建議您使用 Avro 格式。相較於 CSV 與 JSON (以換行符號分隔)，載入 Avro 檔案有以下優勢：

* Avro 二進位格式：
  + 載入較快。即便資料區塊[經過壓縮](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#loading_compressed_and_uncompressed_data)，還是能夠平行讀取。
  + 無需任何輸入或序列化作業。
  + 沒有 ASCII 等其他格式會有的編碼問題，所以剖析較容易。
* 將 Avro 檔案載入 BigQuery 時，會從自述式來源資料自動擷取資料表結構定義。

## Avro 結構定義

將 Avro 檔案載入新的 BigQuery 資料表時，系統會使用來源資料自動擷取資料表結構定義。當 BigQuery 從來源資料擷取結構定義時，會按字母順序使用最後一個檔案。

舉例來說，Cloud Storage 中有下列 Avro 檔案：

```
gs://mybucket/00/
  a.avro
  z.avro
gs://mybucket/01/
  b.avro
```

在 bq 指令列工具中執行這項指令，即可載入所有檔案 (以逗號分隔的清單)，且結構定義衍生自 `mybucket/01/b.avro`：

```
bq load \
--source_format=AVRO \
dataset.table \
"gs://mybucket/00/*.avro","gs://mybucket/01/*.avro"
```

匯入擁有不同 Avro 結構定義的多個 Avro 檔案時，所有結構定義都必須與 [Avro 的結構定義解析](https://avro.apache.org/docs/1.8.1/spec.html#Schema+Resolution)相容。

當 BigQuery 偵測到結構定義時，部分 Avro 資料類型會轉換為 BigQuery 資料類型，確保與 GoogleSQL 語法相容。如需更多資訊，請參閱 [Avro 轉換](#avro_conversions)。

如要提供資料表結構定義來建立外部資料表，請在 BigQuery API 中設定 `referenceFileSchemaUri` 屬性，或在 bq 指令列工具中設定   
`--reference_file_schema_uri` 參數，指向參照檔案的網址。

例如 `--reference_file_schema_uri="gs://mybucket/schema.avro"`。

您也可以[指定 JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)，將結構定義匯入 BigQuery。

## Avro 壓縮

BigQuery 支援下列 Avro 檔案內容的壓縮轉碼器：

* `Snappy`
* `DEFLATE`
* `ZSTD`

## 將 Avro 資料載入至新的資料表

如要將 Avro 資料從 Cloud Storage 載入至新的 BigQuery 資料表，請選取下列任一選項：

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後點選資料集名稱。
4. 在詳細資料窗格中，按一下「建立資料表」
   add\_box。
5. 在「Create table」(建立資料表) 頁面的「Source」(來源) 區段中：

   * 在「Create table from」(使用下列資料建立資料表) 部分，選取「Google Cloud Storage」。
   * 在來源欄位中，瀏覽至或輸入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。請注意，Google Cloud console 中不可加入多個 URI，但支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage 值區的位置必須與要建立之資料表所屬的資料集位置相同。
   * 在「File format」(檔案格式) 中，選取 [Avro]。
6. 在「Create table」(建立資料表) 頁面的「Destination」(目的地) 區段中：

   * 針對「Dataset name」(資料集名稱)，選擇適當的資料集。
   * 確認「Table type」(資料表類型) 已設為「Native table」(原生資料表)。
   * 在「Table name」(資料表名稱) 欄位中，輸入您在 BigQuery 中建立資料表時使用的資料表名稱。
7. 在「Schema」(結構定義) 區段中，不必執行任何操作。結構定義自述於 Avro 檔案中。
8. (選用) 如要對資料表進行分區，請在「Partition and cluster settings」(分區與叢集設定) 區段中選擇您要使用的選項。詳情請參閱[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)。
9. (選擇性操作) 針對「Partitioning filter」(分區篩選器)，請勾選「Require partition filter」(需要分區篩選器) 的方塊，藉此要求使用者加入 `WHERE` 子句來指定要查詢的分區。使用分區篩選器可以降低成本並提升效能。詳情請參閱[在查詢中加入必要的分區篩選器](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#require_a_partition_filter_in_queries)。如果選取 [No partitioning] (無分區)，就無法使用這個選項。
10. (選用) 如要將資料表[分群](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)，請在「Clustering order」(分群順序) 方塊中輸入一到四個欄位名稱。
11. (選擇性操作) 按一下 [Advanced options] (進階選項)。

    * 讓「Write preference」(寫入偏好設定) 的 [Write if empty] (空白時寫入) 選項維持在已選取狀態。這個選項能建立新的資料表，並將您的資料載入其中。
    * 針對「Unknown values」(不明的值)，請讓「Ignore unknown values」(略過不明的值) 保持未勾選狀態。這個選項僅適用於 CSV 和 JSON 檔案。
    * 針對「Encryption」(加密)，請按一下「Customer-managed key」(客戶管理的金鑰)，以使用 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果您保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
12. 點選「建立資料表」。

**注意：** 使用Google Cloud 控制台 將資料載入空白資料表時，您無法新增標籤、說明、資料表到期時間或分區到期時間。  
  
資料表建立完成之後，您就能更新資料表的到期時間、說明和標籤，但您無法在使用 Google Cloud 控制台建立資料表之後，新增分區到期時間。詳情請參閱[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)。

### SQL

使用 [`LOAD DATA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)。以下範例會將 Avro 檔案載入至新資料表 `mytable`：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   LOAD DATA OVERWRITE mydataset.mytable
   FROM FILES (
     format = 'avro',
     uris = ['gs://bucket/path/file.avro']);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

請使用 `bq load` 指令，然後使用 `--source_format` 旗標指定 `AVRO`，並加入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。您可以加入單一 URI、以逗號分隔的 URI 清單，或包含[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)的 URI。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

其他選用標記包括：

* `--time_partitioning_type`：針對資料表啟用時間分區並設定分區類型。可能的值為 `HOUR`、`DAY`、`MONTH` 和 `YEAR`。如果您在 `DATE`、`DATETIME` 或 `TIMESTAMP` 資料欄建立分區資料表，則不一定要使用這個旗標。時間分區的預設分區類型為 `DAY`。您無法變更現有資料表的分區規格。
* `--time_partitioning_expiration`：這是一個整數，用來指定系統應在何時刪除時間分區 (以秒為單位)。到期時間為分區的世界標準時間日期加上整數值。
* `--time_partitioning_field`：用於建立分區資料表的 `DATE` 或 `TIMESTAMP` 資料欄。如果啟用時間分區時沒有這個值，系統就會建立擷取時間分區資料表。
* `--require_partition_filter`：這個選項啟用後，系統會要求使用者加入 `WHERE` 子句，以指定要查詢的分區。使用分區篩選器可以降低成本並提升效能。詳情請參閱「[在查詢中要求使用分區篩選器](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#require_a_partition_filter_in_queries)」。
* `--clustering_fields`：以半形逗號分隔的資料欄名稱清單 (最多四個名稱)，可用來建立[分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)。
* `--destination_kms_key`：用來加密資料表資料的 Cloud KMS 金鑰。

  如要進一步瞭解分區資料表，請參閱：

  + [建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)

  如要進一步瞭解叢集資料表，請參閱下列說明：

  + [建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)

  如要進一步瞭解資料表加密作業，請參閱下列說明文章：

  + [使用 Cloud KMS 金鑰保護資料](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)

如要將 Avro 資料載入 BigQuery，請輸入下列指令：

```
bq --location=location load \
--source_format=format \
dataset.table \
path_to_source
```

更改下列內容：

* location 是您的位置。`--location` 是選用旗標。舉例來說，如果您在東京區域使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)來設定位置的預設值。
* format為 `AVRO`。
* dataset 是現有資料集。
* table 是您正在載入資料的資料表名稱。
* path\_to\_source 是完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或是以逗號分隔的 URI 清單。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。

範例：

下列指令會將資料從 `gs://mybucket/mydata.avro` 載入到 `mydataset` 中名為 `mytable` 的資料表。

```
    bq load \
    --source_format=AVRO \
    mydataset.mytable \
    gs://mybucket/mydata.avro
```

下列指令會將資料從 `gs://mybucket/mydata.avro` 載入到 `mydataset` 中名為 `mytable` 的擷取時間分區資料表。

```
    bq load \
    --source_format=AVRO \
    --time_partitioning_type=DAY \
    mydataset.mytable \
    gs://mybucket/mydata.avro
```

下列指令會將資料從 `gs://mybucket/mydata.avro` 載入到 `mydataset` 中名為 `mytable` 的新分區資料表。資料表會依 `mytimestamp` 資料欄進行分區。

```
    bq load \
    --source_format=AVRO \
    --time_partitioning_field mytimestamp \
    mydataset.mytable \
    gs://mybucket/mydata.avro
```

下列指令會將 `gs://mybucket/` 中多個檔案的資料載入到 `mydataset` 中名為 `mytable` 的資料表。指令中的 Cloud Storage URI 使用萬用字元。

```
    bq load \
    --source_format=AVRO \
    mydataset.mytable \
    gs://mybucket/mydata*.avro
```

下列指令會將 `gs://mybucket/` 中多個檔案的資料載入到 `mydataset` 中名為 `mytable` 的資料表。指令包含以逗號分隔且帶有萬用字元的 Cloud Storage URI 清單。

```
    bq load \
    --source_format=AVRO \
    mydataset.mytable \
    "gs://mybucket/00/*.avro","gs://mybucket/01/*.avro"
```

### API

1. 建立指向 Cloud Storage 中來源資料的 `load` 工作。
2. (選擇性操作) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。
3. `source URIs` 屬性必須是完整的，且必須符合下列格式：`gs://bucket/object`。每個 URI 可包含一個「\*」[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。
4. 藉由將 `sourceFormat` 屬性設為 `AVRO`，以指定 Avro 資料格式。
5. 如要檢查工作狀態，請呼叫 [`jobs.get(job_id)`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/get?hl=zh-tw)，其中 job\_id 是初始要求傳回的工作 ID。

   * 如果是 `status.state = DONE`，代表工作已順利完成。
   * 如果出現 `status.errorResult` 屬性，代表要求執行失敗，且該物件會包含描述問題的相關資訊。如果要求執行失敗，系統就不會建立任何資料表，也不會載入任何資料。
   * 如果未出現 `status.errorResult`，代表工作順利完成，但可能有一些非致命錯誤，例如少數資料列在匯入時發生問題。不嚴重的錯誤都會列在已傳回工作物件的 `status.errors` 屬性中。

**API 附註：**

* 載入工作不可部分完成，且資料狀態具一致性。如果載入工作失敗，所有資料都無法使用；如果載入工作成功，則所有資料都可以使用。
* 最佳做法是產生唯一 ID，並在呼叫 `jobs.insert` 建立載入工作時，將該 ID 當做 `jobReference.jobId` 傳送。這個方法較不受網路故障問題的影響，因為用戶端可使用已知的工作 ID 進行輪詢或重試。
* 對指定的工作 ID 呼叫 `jobs.insert` 是一種冪等作業。也就是說，您可以對同一個工作 ID 重試無數次，最多會有一個作業成功。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// importAvro demonstrates loading Apache Avro data from Cloud Storage into a table.
func importAvro(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states.avro")
	gcsRef.SourceFormat = bigquery.Avro
	loader := client.Dataset(datasetID).Table(tableID).LoaderFrom(gcsRef)

	job, err := loader.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}

	if status.Err() != nil {
		return fmt.Errorf("job completed with error: %v", status.Err())
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.TableId;

// Sample to load Avro data from Cloud Storage into a new BigQuery table
public class LoadAvroFromGCS {

  public static void runLoadAvroFromGCS() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.avro";
    loadAvroFromGCS(datasetName, tableName, sourceUri);
  }

  public static void loadAvroFromGCS(String datasetName, String tableName, String sourceUri) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      LoadJobConfiguration loadConfig =
          LoadJobConfiguration.of(tableId, sourceUri, FormatOptions.avro());

      // Load data from a GCS Avro file into the table
      Job job = bigquery.create(JobInfo.of(loadConfig));
      // Blocks until this load table job completes its execution, either failing or succeeding.
      job = job.waitFor();
      if (job.isDone()) {
        System.out.println("Avro from GCS successfully loaded in a table");
      } else {
        System.out.println(
            "BigQuery was unable to load into the table due to an error:"
                + job.getStatus().getError());
      }
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Column not added during load append \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client libraries
const {BigQuery} = require('@google-cloud/bigquery');
const {Storage} = require('@google-cloud/storage');

// Instantiate clients
const bigquery = new BigQuery();
const storage = new Storage();

/**
 * This sample loads the Avro file at
 * https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.avro
 *
 * TODO(developer): Replace the following lines with the path to your file.
 */
const bucketName = 'cloud-samples-data';
const filename = 'bigquery/us-states/us-states.avro';

async function loadTableGCSAvro() {
  // Imports a GCS file into a table with Avro source format.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'us_states';

  // Configure the load job. For full list of options, see:
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationLoad
  const jobConfigurationLoad = {
    load: {sourceFormat: 'AVRO'},
  };

  // Load data from a Google Cloud Storage file into the table
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .load(storage.bucket(bucketName).file(filename), jobConfigurationLoad);

  // load() waits for the job to finish
  console.log(`Job ${job.id} completed.`);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name

job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.AVRO)
uri = "gs://cloud-samples-data/bigquery/us-states/us-states.avro"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
```

### 從 Avro 資料擷取 JSON 資料

如要確保 Avro 資料以 [`JSON` 資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#json_type)的形式載入 BigQuery，有兩種方法：

1. 將 Avro 結構定義的 `sqlType` 設為 `JSON`，舉例來說，如果您載入的資料具有下列 Avro 結構定義，系統會將 `json_field` 資料欄讀取為 `JSON` 類型：

   ```
   {
       "type": {"type": "string", "sqlType": "JSON"},
       "name": "json_field"
   }
   ```
2. 明確指定 BigQuery 目的地資料表結構定義，並將資料欄類型設為 `JSON`。詳情請參閱[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。

如果您未在 Avro 結構定義或 BigQuery 資料表結構定義中將類型指定為 JSON，系統就會將資料讀取為 `STRING`。

## 將 Avro 資料附加到資料表或使用 Avro 資料覆寫資料表

如要將其他資料載入資料表，您可以指定來源檔案或附加查詢結果。

在 Google Cloud 主控台中，使用「寫入偏好設定」選項，指定從來源檔案或查詢結果載入資料時採取的動作。

將額外資料載入資料表時，可以選擇下列選項：

| 主控台選項 | bq 工具旗標 | BigQuery API 屬性 | 說明 |
| --- | --- | --- | --- |
| 空白時寫入 | 不支援 | `WRITE_EMPTY` | 資料表空白時才會寫入資料。 |
| 附加到資料表中 | `--noreplace` 或 `--replace=false`；如果未指定 `--[no]replace`，則預設動作為附加 | `WRITE_APPEND` | ([預設](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.write_disposition)) 將資料附加至資料表尾端。 |
| 覆寫資料表 | `--replace`或`--replace=true` | `WRITE_TRUNCATE` | 先清除資料表中所有現有資料，再寫入新的資料。 這項操作也會刪除資料表結構定義、資料列層級安全性，並移除所有 Cloud KMS 金鑰。 |

如果您將資料載入現有資料表，該載入工作可附加資料，或覆寫資料表。

**注意：** 本頁面未說明如何對分區資料表進行附加或覆寫。如要瞭解如何對分區資料表進行附加或覆寫，請參閱[對分區資料表中的資料執行附加或覆寫操作](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#append-overwrite)一節。

如要使用 Avro 資料附加或覆寫資料表：

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後點選資料集名稱。
4. 在詳細資料窗格中，按一下「建立資料表」
   add\_box。
5. 在「Create table」(建立資料表) 頁面的「Source」(來源) 區段中：

   * 針對「Create table from」(使用下列資料建立資料表)，選取 [Cloud Storage]。
   * 在來源欄位中，瀏覽至或輸入 [Cloud Storage URI](#gcs-uri)。請注意， Google Cloud 控制台中無法加入多個 URI，但支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage 值區的位置必須與要附加或覆寫之資料表所屬的資料集位置相同。
   * 在「File format」(檔案格式) 中，選取 [Avro]。
6. 在「Create table」(建立資料表) 頁面的「Destination」(目的地) 區段中：

   * 在「Dataset name」(資料集名稱) 部分選擇適當的資料集。
   * 在「Table name」(資料表名稱) 欄位中，輸入要在 BigQuery 中進行附加或覆寫作業的資料表。
   * 確認「Table type」(資料表類型) 已設為「Native table」(原生資料表)。
7. 在「Schema」(結構定義) 區段中，不必執行任何操作。結構定義自述於 Avro 檔案中。

   **注意：**您可以在對資料表進行附加或覆寫作業時修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)一文。
8. 保留「Partition and cluster settings」(分區與叢集設定) 的預設值。您無法藉由附加或覆寫的方式，將資料表轉換為分區資料表或分群資料表； Google Cloud 主控台不支援在載入工作中對分區或分群資料表執行附加或覆寫作業。
9. 點選「進階選項」。

   * 針對「Write preference」(寫入偏好設定)，選擇 [Append to table] (附加到資料表中) 或 [Overwrite table] (覆寫資料表)。
   * 針對「Unknown values」(不明的值)，請讓「Ignore unknown values」(略過不明的值) 保持未勾選狀態。這個選項僅適用於 CSV 和 JSON 檔案。
   * 針對「Encryption」(加密)，請按一下「Customer-managed key」(客戶管理的金鑰)，以使用 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果您保留 **Google-owned and managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
10. 點選「建立資料表」。

### SQL

使用 [`LOAD DATA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)。以下範例會將 Avro 檔案附加至 `mytable` 資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   LOAD DATA INTO mydataset.mytable
   FROM FILES (
     format = 'avro',
     uris = ['gs://bucket/path/file.avro']);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要覆寫資料表，請輸入 `bq load` 指令並加上 `--replace` 旗標。如要附加資料至資料表，使用 `--noreplace` 旗標。若未指定任何旗標，預設動作為附加資料。提供 `--source_format` 旗標，並將其設為 `AVRO`。由於系統會自動從自述來源資料中擷取 Avro 結構定義，所以您不需要提供結構定義。

**注意：**您可以在對資料表進行附加或覆寫作業時修改資料表的結構定義。如要進一步瞭解載入作業期間可進行的結構定義變更，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)一文。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

其他選用標記包括：

* `--destination_kms_key`：用來加密資料表資料的 Cloud KMS 金鑰。

```
bq --location=location load \
--[no]replace \
--source_format=format \
dataset.table \
path_to_source
```

更改下列內容：

* location 是您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。`--location` 是選用旗標。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)來設定位置的預設值。
* format為 `AVRO`。
* dataset 是現有資料集。
* table 是您正在載入資料的資料表名稱。
* path\_to\_source 是完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或是以逗號分隔的 URI 清單。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。

範例：

下列指令會從 `gs://mybucket/mydata.avro` 載入資料，並覆寫 `mydataset` 中名為 `mytable` 的資料表。

```
    bq load \
    --replace \
    --source_format=AVRO \
    mydataset.mytable \
    gs://mybucket/mydata.avro
```

下列指令會從 `gs://mybucket/mydata.avro` 載入資料，並將資料附加至 `mydataset` 中名為 `mytable` 的資料表。

```
    bq load \
    --noreplace \
    --source_format=AVRO \
    mydataset.mytable \
    gs://mybucket/mydata.avro
```

如要瞭解如何使用 bq 指令列工具附加和覆寫分區資料表，請參閱[對分區資料表中的資料執行附加或覆寫操作](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#append-overwrite)。

### API

1. 建立指向 Cloud Storage 中來源資料的 `load` 工作。
2. (選擇性操作) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。
3. `source URIs` 屬性必須是完整的，且必須符合下列格式：`gs://bucket/object`。您可以使用逗號分隔清單的形式加入多個 URI。請注意，系統也支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。
4. 藉由將 `configuration.load.sourceFormat` 屬性設為 `AVRO`，以指定資料格式。
5. 藉由將 `configuration.load.writeDisposition` 屬性設為 `WRITE_TRUNCATE` 或 `WRITE_APPEND`，以指定寫入偏好設定。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// importAvroTruncate demonstrates loading Apache Avro data from Cloud Storage into a table
// and overwriting/truncating existing data in the table.
func importAvroTruncate(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states.avro")
	gcsRef.SourceFormat = bigquery.Avro
	loader := client.Dataset(datasetID).Table(tableID).LoaderFrom(gcsRef)
	// Default for import jobs is to append data to a table.  WriteTruncate
	// specifies that existing data should instead be replaced/overwritten.
	loader.WriteDisposition = bigquery.WriteTruncate

	job, err := loader.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}

	if status.Err() != nil {
		return fmt.Errorf("job completed with error: %v", status.Err())
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.TableId;

// Sample to overwrite the BigQuery table data by loading a AVRO file from GCS
public class LoadAvroFromGCSTruncate {

  public static void runLoadAvroFromGCSTruncate() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.avro";
    loadAvroFromGCSTruncate(datasetName, tableName, sourceUri);
  }

  public static void loadAvroFromGCSTruncate(
      String datasetName, String tableName, String sourceUri) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      LoadJobConfiguration loadConfig =
          LoadJobConfiguration.newBuilder(tableId, sourceUri)
              .setFormatOptions(FormatOptions.avro())
              // Set the write disposition to overwrite existing table data
              .setWriteDisposition(JobInfo.WriteDisposition.WRITE_TRUNCATE)
              .build();

      // Load data from a GCS Avro file into the table
      Job job = bigquery.create(JobInfo.of(loadConfig));
      // Blocks until this load table job completes its execution, either failing or succeeding.
      job = job.waitFor();
      if (job.isDone()) {
        System.out.println("Table is successfully overwritten by AVRO file loaded from GCS");
      } else {
        System.out.println(
            "BigQuery was unable to load into the table due to an error:"
                + job.getStatus().getError());
      }
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Column not added during load append \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client libraries
const {BigQuery} = require('@google-cloud/bigquery');
const {Storage} = require('@google-cloud/storage');

// Instantiate clients
const bigquery = new BigQuery();
const storage = new Storage();

/**
 * This sample loads the Avro file at
 * https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.avro
 *
 * TODO(developer): Replace the following lines with the path to your file.
 */
const bucketName = 'cloud-samples-data';
const filename = 'bigquery/us-states/us-states.avro';

async function loadTableGCSAvroTruncate() {
  /**
   * Imports a GCS file into a table and overwrites
   * table data if table already exists.
   */

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'us_states';

  // Configure the load job. For full list of options, see:
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationLoad
  const jobConfigurationLoad = {
    load: {
      sourceFormat: 'AVRO',
      writeDisposition: 'WRITE_TRUNCATE',
    },
  };

  // Load data from a Google Cloud Storage file into the table
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .load(storage.bucket(bucketName).file(filename), jobConfigurationLoad);

  // load() waits for the job to finish
  console.log(`Job ${job.id} completed.`);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import io

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ],
)

body = io.BytesIO(b"Washington,WA")
client.load_table_from_file(body, table_id, job_config=job_config).result()
previous_rows = client.get_table(table_id).num_rows
assert previous_rows > 0

job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.AVRO,
)

uri = "gs://cloud-samples-data/bigquery/us-states/us-states.avro"
load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
```

## 正在載入 Hive 分區的 Avro 資料

BigQuery 支援載入儲存在 Cloud Storage 的 Hive 分區 Avro 資料，並且將會在目的地 BigQuery 代管資料表中的資料欄，填入 Hive 分區的資料欄。詳情請參閱[從 Cloud Storage 載入外部分區資料](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw)。

## Avro 轉換

BigQuery 會將 Avro 資料類型轉換為下列 BigQuery 資料類型：

### 原始類型

| 沒有 [logicalType 屬性](#logical-types)的 Avro 資料類型 | BigQuery 資料類型 | 附註 |
| --- | --- | --- |
| null | BigQuery 會略過這些值 |  |
| boolean | BOOLEAN |  |
| int | INTEGER |  |
| long | INTEGER |  |
| float | FLOAT |  |
| double | FLOAT |  |
| bytes | BYTES |  |
| string | STRING | 僅限 UTF-8 |

### 邏輯類型

預設情況下，BigQuery 會忽略多數類型的 `logicalType` 屬性，並改用基本 Avro 類型。如要將 Avro 邏輯型別轉換為對應的 BigQuery 資料型別，請使用 bq 指令列工具將 `--use_avro_logical_types` 旗標設為 `true`，或在呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法以建立載入工作時，於[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)中設定 `useAvroLogicalTypes` 屬性。

下表顯示 Avro 邏輯類型到 BigQuery 資料類型的轉換。

| Avro 邏輯類型 | BigQuery 資料類型：已停用邏輯類型 | BigQuery 資料類型：已啟用邏輯類型 |
| --- | --- | --- |
| 日期 | INTEGER | DATE |
| time-millis | INTEGER | 時間 |
| time-micros | INTEGER (從 LONG 轉換) | 時間 |
| timestamp-millis | INTEGER (從 LONG 轉換) | TIMESTAMP |
| timestamp-micros | INTEGER (從 LONG 轉換) | TIMESTAMP |
| local-timestamp-millis | INTEGER (從 LONG 轉換) | DATETIME |
| local-timestamp-micros | INTEGER (從 LONG 轉換) | DATETIME |
| 持續時間 | BYTES (從大小為 12 的 `fixed` 類型轉換) | BYTES (從大小為 12 的 `fixed` 類型轉換) |
| decimal | NUMERIC、BIGNUMERIC 或 STRING (請參閱「[Decimal 邏輯類型](#decimal_logical_type)」) | NUMERIC、BIGNUMERIC 或 STRING (請參閱「[Decimal 邏輯類型](#decimal_logical_type)」) |

如需進一步瞭解 Avro 資料類型，請參閱 [Apache Avro™ 1.8.2 規格](https://avro.apache.org/docs/1.8.2/spec.html)。

**注意：** 從 BigQuery 匯出至 Avro 時，`DATETIME` 會匯出為 `STRING`，並使用自訂邏輯時間，因此匯入回 BigQuery 時不會識別為 `DATETIME`。

#### Date 邏輯類型

在您打算載入的任何 Avro 檔案中，您必須以以下格式指定日期邏輯類型：

```
{
       "type": {"logicalType": "date", "type": "int"},
       "name": "date_field"
}
```

#### Decimal 邏輯類型

`Decimal` 邏輯型別可以轉換為 `NUMERIC`、`BIGNUMERIC` 或 `STRING` 型別。轉換後的型別取決於 `decimal` 邏輯型別的精確度和比例參數，以及指定的小數目標型別。請按照下列方式指定十進位目標類型：

* 如要使用 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 進行[載入作業](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，請使用 [`JobConfigurationLoad.decimalTargetTypes`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.decimal_target_types) 欄位。
* 如要使用 bq 指令列工具中的 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令執行[載入工作](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，請使用 [`--decimal_target_types`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#flags_and_arguments_9) 旗標。
* 如要查詢[含有外部來源的資料表](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)：
  請使用 [`ExternalDataConfiguration.decimalTargetTypes`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#ExternalDataConfiguration.FIELDS.decimal_target_types) 欄位。
* 如果是[使用 DDL 建立的永久外部資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)：
  請使用 [`decimal_target_types`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#external_table_option_list) 選項。

為確保向後相容性，如果未指定十進位目標類型，您可以將含有 `bytes` 資料欄 (具有 `decimal` 邏輯類型) 的 Avro 檔案載入現有資料表的 `BYTES` 資料欄。在這種情況下，系統會忽略 Avro 檔案中資料欄的 `decimal` 邏輯類型。這項轉換模式已淘汰，日後可能會移除。

如要進一步瞭解 Avro `decimal`邏輯類型，請參閱 [Apache Avro™ 1.8.2 規格](https://avro.apache.org/docs/1.8.2/spec.html#Decimal)。

#### 時間邏輯類型

在您要載入的任何 Avro 檔案中，都必須以下列其中一種格式指定時間邏輯類型。

如要精確到毫秒：

```
{
       "type": {"logicalType": "time-millis", "type": "int"},
       "name": "time_millis_field"
}
```

微秒精確度：

```
{
       "type": {"logicalType": "time-micros", "type": "int"},
       "name": "time_micros_field"
}
```

#### 時間戳記邏輯類型

在您要載入的任何 Avro 檔案中，都必須以下列其中一種格式指定時間戳記邏輯類型。

如要精確到毫秒：

```
{
       "type": {"logicalType": "timestamp-millis", "type": "long"},
       "name": "timestamp_millis_field"
}
```

微秒精確度：

```
{
       "type": {"logicalType": "timestamp-micros", "type": "long"},
       "name": "timestamp_micros_field"
}
```

#### Local-Timestamp 邏輯類型

在您打算載入的任何 Avro 檔案中，您必須以下列其中一種格式指定本機時間戳記邏輯型別。

如要精確到毫秒：

```
{
       "type": {"logicalType": "local-timestamp-millis", "type": "long"},
       "name": "local_timestamp_millis_field"
}
```

微秒精確度：

```
{
       "type": {"logicalType": "local-timestamp-micros", "type": "long"},
       "name": "local_timestamp_micros_field"
}
```

### 複合類型

| Avro 資料類型 | BigQuery 資料類型 | 附註 |
| --- | --- | --- |
| record | RECORD | * 別名會被略過 * Doc 會轉換為[欄位說明](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_descriptions) * 在讀取時間設定預設值 * 順序會被略過 * 會捨棄遞迴欄位 — 僅為遞迴欄位保留第一個巢狀層級 |
| enum | STRING | * 字串為 enum 的符號值 * 別名會被略過 * Doc 會轉換為[欄位說明](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_descriptions) |
| array | 重複欄位 | 不支援陣列的陣列。只包含 NULL 類型的陣列會被略過。 |
| map<T> | RECORD | BigQuery 會將 Avro map<T> 欄位轉換為包含兩個欄位 (鍵與值) 的重複 RECORD。BigQuery 會將鍵儲存為 STRING，並將其值轉換為 BigQuery 中相對應的資料類型。 |
| 聯集 | * 可為 null 的欄位 * 清單欄位可為 null 的 RECORD | * 當 union 僅有一個非 null 類型時，會轉換為可為 null 的欄位。 * 否則會轉換為清單欄位可為 null 的 RECORD。這些欄位只有其中一個會在讀取時間設定。 |
| fixed | BYTES | * 別名會被略過 * 系統會忽略大小 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]