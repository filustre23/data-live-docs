Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Cloud Storage 載入 Parquet 資料

本頁概要說明如何將 Parquet 資料從 Cloud Storage 載入 BigQuery。

[Parquet](http://parquet.apache.org) 是開放原始碼的欄導向資料格式，廣泛用於 Apache Hadoop 生態系統。

從 Cloud Storage 載入 Parquet 資料時，可將資料載入新的資料表或分區、或對現有資料表或分區進行附加或覆寫作業。將資料載入 BigQuery 時，資料會轉換為 [Capacitor](https://cloud.google.com/blog/products/gcp/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw) 資料欄格式 (BigQuery 的儲存格式)。

如要瞭解如何從本機檔案載入 Parquet 資料，請參閱「[從本機檔案載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)」。

## 限制

從 Cloud Storage bucket 將資料載入 BigQuery 時，您必須遵守下列限制：

* BigQuery 不保證外部資料來源的資料一致性。如果基礎資料在查詢執行期間遭到變更，可能會導致非預期的行為。
* BigQuery 不支援 [Cloud Storage 物件版本控管](https://docs.cloud.google.com/storage/docs/object-versioning?hl=zh-tw)。如果 Cloud Storage URI 中包含版本編號，載入工作就會失敗。
* 如果載入的檔案有不同的結構定義，您就無法在 Cloud Storage URI 中使用萬用字元。只要欄位位置不同，即為不同的結構定義。

## 輸入檔案規定

如要避免將 Parquet 檔案載入 BigQuery 時發生 `resourcesExceeded` 錯誤，請遵守下列規範：

* 資料列大小不得超過 50 MB。
* 如果輸入資料包含超過 100 欄，請考慮縮小頁面大小，使其小於預設頁面大小 (1 \* 1024 \* 1024 位元組)。如果您使用大量壓縮，這項功能就特別實用。
* 為獲得最佳效能，請將列群組大小設為至少 16 MiB。
  如果列群組大小較小，I/O 會增加，載入和查詢速度也會變慢。

## 事前準備

授予 Identity and Access Management (IAM) 角色，讓使用者具備執行本文件各項工作所需的權限，並建立資料集來儲存資料。

### 所需權限

如要將資料載入 BigQuery，您需要 IAM 權限才能執行載入工作，並將資料載入 BigQuery 資料表和資料分割。如要從 Cloud Storage 載入資料，您也需要 IAM 權限，才能存取含有資料的 bucket。

#### 將資料載入 BigQuery 的權限

如要將資料載入新的 BigQuery 資料表或資料分割區，或是附加或覆寫現有資料表或資料分割區，您需要下列 IAM 權限：

* `bigquery.tables.create`
* `bigquery.tables.updateData`
* `bigquery.tables.update`
* `bigquery.jobs.create`

下列每個預先定義的 IAM 角色都包含將資料載入 BigQuery 資料表或資料分割區所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin` (包括 `bigquery.jobs.create` 權限)
* `bigquery.user` (包括 `bigquery.jobs.create` 權限)
* `bigquery.jobUser` (包括 `bigquery.jobs.create` 權限)

此外，如果您有 `bigquery.datasets.create` 權限，可以使用您建立的資料集中的載入作業，建立及更新資料表。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)」。

### 從 Cloud Storage 載入資料的權限

如要取得從 Cloud Storage bucket 載入資料所需的權限，請要求管理員授予 bucket 的「[Storage 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin) 」(`roles/storage.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備從 Cloud Storage bucket 載入資料所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要從 Cloud Storage bucket 載入資料，必須具備下列權限：

* `storage.buckets.get`
* `storage.objects.get`
* `storage.objects.list (required if you are using a URI wildcard)`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 建立資料集

建立 [BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存資料。

## Parquet 結構定義

將 Parquet 檔案載入 BigQuery 時，系統會從自述式來源資料自動擷取資料表結構定義。從來源資料擷取結構定義時，BigQuery 會按照字母順序使用最後一個檔案。

舉例來說，Cloud Storage 中有下列 Parquet 檔案：

```
gs://mybucket/00/
  a.parquet
  z.parquet
gs://mybucket/01/
  b.parquet
```

在 bq 指令列工具中執行這項指令，會載入所有檔案 (以半形逗號分隔的清單)，並從 `mybucket/01/b.parquet` 衍生結構定義：

```
bq load \
--source_format=PARQUET \
dataset.table \
"gs://mybucket/00/*.parquet","gs://mybucket/01/*.parquet"
```

載入具有不同結構定義的多個 Parquet 檔案時，不同結構定義中指定的相同資料欄必須在各個結構定義中採用相同的[模式](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#modes)。

BigQuery 偵測到結構定義時，會將部分 Parquet 資料類型轉換為 BigQuery 資料類型，使其與 GoogleSQL 語法相容。詳情請參閱 [Parquet 轉換](#parquet_conversions)。

如要提供資料表結構定義來建立外部資料表，請在 BigQuery API 中設定 `referenceFileSchemaUri` 屬性，或在 bq 指令列工具中設定   
`--reference_file_schema_uri` 參數，指向參考檔案的網址。

例如 `--reference_file_schema_uri="gs://mybucket/schema.parquet"`。

## Parquet 壓縮

BigQuery 支援下列 Parquet 檔案內容的壓縮編解碼器：

* `GZip`
* `LZO_1C`
* `LZO_1X`
* `LZ4_RAW`
* `Snappy`
* `ZSTD`

## 將 Parquet 資料載入至新的資料表

您可以透過下列任一方式，將 Parquet 資料載入新資料表：

* Google Cloud 控制台
* bq 指令列工具的 `bq load` 指令
* `jobs.insert` API 方法和設定 `load` 工作
* 用戶端程式庫

如要將 Parquet 資料從 Cloud Storage 載入新的 BigQuery 資料表，請執行下列操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，點選「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「來源」部分中，從「建立資料表來源」清單中選取「Google Cloud Storage」。
   接著，按照下列步驟操作：
   1. 從 Cloud Storage bucket 選取檔案，或輸入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。
      您無法在 Google Cloud 控制台中加入多個 URI，但支援[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage bucket 必須與包含要建立、附加或覆寫資料表的資料集位於相同位置。
   2. 在「檔案格式」中選取「Parquet」。
2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。結構定義會自行描述 Parquet 檔案。
4. 選用：指定「分區與叢集設定」。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。
5. 按一下「進階選項」，然後執行下列操作：
   * 讓「Write preference」(寫入偏好設定) 的 [Write if empty] (空白時寫入) 選項維持在已選取狀態。這個選項會建立新資料表，並將資料載入其中。
   * 如要忽略資料列中不屬於資料表結構定義的值，請選取「Unknown values」(不明的值)。
   * 如要**加密**，請點選「客戶管理的金鑰」，使用 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
6. 點選「建立資料表」。

**注意：** 使用Google Cloud 控制台將資料載入空白資料表時，無法新增標籤、說明、資料表到期日或分區到期日。  
  
資料表建立完成後，您可以更新資料表的到期時間、說明和標籤，但使用 Google Cloud 控制台建立資料表後，就無法新增分區到期時間。詳情請參閱「[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)」。

### SQL

使用 [`LOAD DATA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)。以下範例會將 Parquet 檔案載入新資料表 `mytable`：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   LOAD DATA OVERWRITE mydataset.mytable
   FROM FILES (
     format = 'PARQUET',
     uris = ['gs://bucket/path/file.parquet']);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

請使用 `bq load` 指令，然後使用 `--source_format` 旗標指定 `PARQUET`，並加入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。您可以加入單一 URI、以逗號分隔的 URI 清單，或包含[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)的 URI。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

其他選用標記包括：

* `--time_partitioning_type`：在資料表上啟用時間分區，並設定分區類型。可能的值為 `HOUR`、`DAY`、`MONTH` 和 `YEAR`。建立以 `DATE`、`DATETIME` 或 `TIMESTAMP` 欄為依據的資料表時，這個旗標為選用項目。時間分區的預設分區類型為 `DAY`。您無法變更現有資料表的分割規格。
* `--time_partitioning_expiration`：這是一個整數，用來指定系統應在何時刪除時間分區 (以秒為單位)。到期時間會評估為分區的世界標準時間日期加上整數值。
* `--time_partitioning_field`：用於建立分區資料表的 `DATE` 或 `TIMESTAMP` 資料欄。如果啟用時間分區功能，但未提供這個值，系統會建立擷取時間分區資料表。
* `--require_partition_filter`：這個選項啟用後，系統會要求使用者加入 `WHERE` 子句，以指定要查詢的分區。規定必須使用分區篩選器，有助於降低費用及提高成效。
  詳情請參閱「[在查詢中要求使用分割區篩選器](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)」。
* `--clustering_fields`：以半形逗號分隔的清單，最多可列出四個用於建立[分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)的欄名。
* `--destination_kms_key`：用於加密表格資料的 Cloud KMS 金鑰。
* `--column_name_character_map`：定義資料欄名稱字元的範圍和處理方式，並可選擇啟用[彈性資料欄名稱](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#flexible-column-names)。詳情請參閱「[`load_option_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_option_list)」。如要進一步瞭解支援和不支援的字元，請參閱「[彈性資料欄名稱](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#flexible-column-names)」。

  如要進一步瞭解分區資料表，請參閱：

  + [建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)

  如要進一步瞭解分群資料表，請參閱：

  + [建立及使用分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)

  如要進一步瞭解資料表加密作業，請參閱下列說明文章：

  + [使用 Cloud KMS 金鑰保護資料](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)

如要將 Parquet 資料載入 BigQuery，請輸入下列指令：

```
bq --location=LOCATION load \
--source_format=FORMAT \
DATASET.TABLE \
PATH_TO_SOURCE
```

更改下列內容：

* `LOCATION`：您的位置。`--location` 是選用旗標。舉例來說，如果您在東京區域使用 BigQuery，可以將旗標值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)，設定該位置的預設值。
* `FORMAT`: `PARQUET`.
* `DATASET`：現有資料集。
* `TABLE`：要載入資料的資料表名稱。
* `PATH_TO_SOURCE`：完整 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri) 或以逗號分隔的清單 URI。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。

範例：

下列指令會將資料從 `gs://mybucket/mydata.parquet` 載入到 `mydataset` 中名為 `mytable` 的資料表。

```
    bq load \
    --source_format=PARQUET \
    mydataset.mytable \
    gs://mybucket/mydata.parquet
```

下列指令會將 `gs://mybucket/mydata.parquet` 中的資料載入 `mydataset` 中名為 `mytable` 的新擷取時間分區資料表。

```
    bq load \
    --source_format=PARQUET \
    --time_partitioning_type=DAY \
    mydataset.mytable \
    gs://mybucket/mydata.parquet
```

下列指令會將資料從 `gs://mybucket/mydata.parquet` 載入到 `mydataset` 中名為 `mytable` 的分區資料表。資料表會依 `mytimestamp` 資料欄進行分區。

```
    bq load \
    --source_format=PARQUET \
    --time_partitioning_field mytimestamp \
    mydataset.mytable \
    gs://mybucket/mydata.parquet
```

下列指令會將 `gs://mybucket/` 中多個檔案的資料載入到 `mydataset` 中名為 `mytable` 的資料表。指令中的 Cloud Storage URI 使用萬用字元。

```
    bq load \
    --source_format=PARQUET \
    mydataset.mytable \
    gs://mybucket/mydata*.parquet
```

下列指令會將 `gs://mybucket/` 中多個檔案的資料載入到 `mydataset` 中名為 `mytable` 的資料表。指令包含以逗號分隔且帶有萬用字元的 Cloud Storage URI 清單。

```
    bq load \
    --source_format=PARQUET \
    mydataset.mytable \
    "gs://mybucket/00/*.parquet","gs://mybucket/01/*.parquet"
```

### API

1. 建立指向 Cloud Storage 中來源資料的 `load` 工作。
2. (選擇性操作) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。
3. `source URIs` 屬性必須是完整名稱，格式為 `gs://BUCKET/OBJECT`。每個 URI 最多可包含一個「\*」[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。
4. 將 `sourceFormat` 屬性設為 `PARQUET`，以指定 Parquet 資料格式。
5. 如要檢查工作狀態，請呼叫 [`jobs.get(JOB_ID*)`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/get?hl=zh-tw)，並將 JOB\_ID 替換為初始要求傳回的工作 ID。

   * 如果是 `status.state = DONE`，代表工作已順利完成。
   * 如果存在 `status.errorResult` 屬性，表示要求失敗，且該物件包含說明錯誤原因的資訊。如果要求執行失敗，系統就不會建立任何資料表，也不會載入任何資料。
   * 如果沒有 `status.errorResult`，表示工作順利完成，但可能發生一些非致命錯誤，例如匯入部分資料列時發生問題。系統會在傳回的工作物件的 `status.errors` 屬性中列出非致命錯誤。

**API 附註：**

* 載入工作具有原子性和一致性：如果載入工作失敗，所有資料都無法使用；如果載入工作成功，所有資料都能使用。
* 最佳做法是產生專屬 ID，並在呼叫 `jobs.insert` 建立載入工作時，將該 ID 做為 `jobReference.jobId` 傳遞。這個方法較不受網路故障問題的影響，因為用戶端可使用已知的工作 ID 進行輪詢或重試。
* 對指定的工作 ID 呼叫 `jobs.insert` 是一種冪等作業。也就是說，您可以對同一個工作 ID 重試無數次，最多會有一個作業成功。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// importParquet demonstrates loading Apache Parquet data from Cloud Storage into a table.
func importParquet(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states.parquet")
	gcsRef.SourceFormat = bigquery.Parquet
	gcsRef.AutoDetect = true
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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.TableId;
import java.math.BigInteger;

public class LoadParquet {

  public static void runLoadParquet() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    loadParquet(datasetName);
  }

  public static void loadParquet(String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.parquet";
      TableId tableId = TableId.of(datasetName, "us_states");

      LoadJobConfiguration configuration =
          LoadJobConfiguration.builder(tableId, sourceUri)
              .setFormatOptions(FormatOptions.parquet())
              .build();

      // For more information on Job see:
      // https://googleapis.dev/java/google-cloud-clients/latest/index.html?com/google/cloud/bigquery/package-summary.html
      // Load the table
      Job job = bigquery.create(JobInfo.of(configuration));

      // Blocks until this load table job completes its execution, either failing or succeeding.
      Job completedJob = job.waitFor();
      if (completedJob == null) {
        System.out.println("Job not executed since it no longer exists.");
        return;
      } else if (completedJob.getStatus().getError() != null) {
        System.out.println(
            "BigQuery was unable to load the table due to an error: \n"
                + job.getStatus().getError());
        return;
      }

      // Check number of rows loaded into the table
      BigInteger numRows = bigquery.getTable(tableId).getNumRows();
      System.out.printf("Loaded %d rows. \n", numRows);

      System.out.println("GCS parquet loaded successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("GCS Parquet was not loaded. \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client libraries
const {BigQuery} = require('@google-cloud/bigquery');
const {Storage} = require('@google-cloud/storage');

// Instantiate clients
const bigquery = new BigQuery();
const storage = new Storage();

/**
 * This sample loads the Parquet file at
 * https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.parquet
 *
 * TODO(developer): Replace the following lines with the path to your file.
 */
const bucketName = 'cloud-samples-data';
const filename = 'bigquery/us-states/us-states.parquet';

async function loadTableGCSParquet() {
  // Imports a GCS file into a table with Parquet source format.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  // Configure the load job. For full list of options, see:
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationLoad
  const metadata = {
    sourceFormat: 'PARQUET',
    location: 'US',
  };

  // Load data from a Google Cloud Storage file into the table
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .load(storage.bucket(bucketName).file(filename), metadata);

  // load() waits for the job to finish
  console.log(`Job ${job.id} completed.`);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;
use Google\Cloud\Core\ExponentialBackoff;

/** Uncomment and populate these variables in your code */
// $projectId  = 'The Google project ID';
// $datasetId  = 'The BigQuery dataset ID';

// instantiate the bigquery table service
$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$dataset = $bigQuery->dataset($datasetId);
$table = $dataset->table('us_states');

// create the import job
$gcsUri = 'gs://cloud-samples-data/bigquery/us-states/us-states.parquet';
$loadConfig = $table->loadFromStorage($gcsUri)->sourceFormat('PARQUET');
$job = $table->runJob($loadConfig);
// poll the job until it is complete
$backoff = new ExponentialBackoff(10);
$backoff->execute(function () use ($job) {
    print('Waiting for job to complete' . PHP_EOL);
    $job->reload();
    if (!$job->isComplete()) {
        throw new Exception('Job has not yet completed', 500);
    }
});
// check if the job has errors
if (isset($job->info()['status']['errorResult'])) {
    $error = $job->info()['status']['errorResult']['message'];
    printf('Error running job: %s' . PHP_EOL, $error);
} else {
    print('Data imported successfully' . PHP_EOL);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 [Client.load\_table\_from\_uri()](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_load_table_from_uri) 方法，從 Cloud Storage 啟動載入工作。如要使用 Parquet，請將 [LoadJobConfig.source\_format 屬性](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_source_format)設為 `PARQUET` 字串，並將工作設定做為 `job_config` 引數傳遞至 `load_table_from_uri()` 方法。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
)
uri = "gs://cloud-samples-data/bigquery/us-states/us-states.parquet"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
```

## 使用 Parquet 資料附加到資料表或覆寫資料表

如要將其他資料載入資料表，您可以指定來源檔案或附加查詢結果。

在 Google Cloud 控制台中，使用「寫入偏好設定」選項，指定從來源檔案或查詢結果載入資料時要採取的動作。

將額外資料載入資料表時，可以選擇下列選項：

| 主控台選項 | bq 工具旗標 | BigQuery API 屬性 | 說明 |
| --- | --- | --- | --- |
| 空白時寫入 | 不支援 | `WRITE_EMPTY` | 資料表空白時才會寫入資料。 |
| 附加到資料表 | `--noreplace` 或 `--replace=false`；如果未指定 `--[no]replace`，則預設動作為附加 | `WRITE_APPEND` | ([預設](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.write_disposition)) 將資料附加至資料表結尾。 |
| 覆寫資料表 | `--replace`或`--replace=true` | `WRITE_TRUNCATE` | 在寫入新資料前，清除資料表中的所有現有資料。 這項操作也會刪除資料表結構定義、資料列層級安全性，並移除所有 Cloud KMS 金鑰。 |

如果您將資料載入現有資料表，該載入工作可附加資料，或覆寫資料表。

您可以使用下列任一方式附加或覆寫表格：

* Google Cloud 控制台
* bq 指令列工具的 `bq load` 指令
* `jobs.insert` API 方法和設定 `load` 工作
* 用戶端程式庫

**注意：**本頁面未說明如何對分區資料表進行附加或覆寫。如要瞭解如何對分區資料表進行附加或覆寫，請參閱[對分區資料表中的資料執行附加或覆寫操作](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#append-overwrite)一節。

如要使用 Parquet 資料對資料表進行附加或覆寫，請執行下列操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，點選「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「來源」部分中，從「建立資料表來源」清單中選取「Google Cloud Storage」。
   接著，按照下列步驟操作：
   1. 從 Cloud Storage bucket 選取檔案，或輸入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。
      您無法在 Google Cloud 控制台中加入多個 URI，但支援[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage bucket 必須與包含要建立、附加或覆寫資料表的資料集位於相同位置。
   2. 在「檔案格式」中選取「Parquet」。
**注意：**附加或覆寫表格時，可以修改表格的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱「[修改表格結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)」。2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。結構定義會自行描述 Parquet 檔案。
**注意：**附加或覆寫表格時，可以修改表格的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱「[修改表格結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)」。4. 選用：指定「分區與叢集設定」。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。您無法透過附加或覆寫資料表，將資料表轉換為已分區或分群資料表。 Google Cloud 控制台不支援在載入工作中，附加至或覆寫已分割或叢集化的資料表。
5. 按一下「進階選項」，然後執行下列操作：
   * 在「寫入偏好設定」部分，選擇「附加到資料表」或「覆寫資料表」。
   * 如要忽略資料列中不屬於資料表結構定義的值，請選取「Unknown values」(不明的值)。
   * 如要**加密**，請點選「客戶管理的金鑰」，使用 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
6. 點選「建立資料表」。

### SQL

使用 [`LOAD DATA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)。以下範例會將 Parquet 檔案附加至 `mytable` 資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   LOAD DATA INTO mydataset.mytable
   FROM FILES (
     format = 'PARQUET',
     uris = ['gs://bucket/path/file.parquet']);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要覆寫資料表，請輸入 `bq load` 指令並加上 `--replace` 旗標。如要附加資料至資料表，使用 `--noreplace` 旗標。若未指定任何旗標，預設動作為附加資料。提供 `--source_format` 旗標，並將其設為 `PARQUET`。由於系統會從自述式來源資料自動擷取 Parquet 結構定義，因此您不需要提供結構定義。

**注意：**您可以在對資料表進行附加或覆寫作業時修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)一文。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

其他選用標記包括：

* `--destination_kms_key`：用於加密表格資料的 Cloud KMS 金鑰。

```
bq --location=LOCATION load \
--[no]replace \
--source_format=FORMAT \
DATASET.TABLE \
PATH_TO_SOURCE
```

更改下列內容：

* `location`：您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。`--location` 是選用旗標。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)來設定位置的預設值。
* `format`: `PARQUET`.
* `dataset`：現有資料集。
* `table`：要載入資料的資料表名稱。
* `path_to_source`：完整 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri) 或以逗號分隔的清單 URI。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。

範例：

下列指令會從 `gs://mybucket/mydata.parquet` 載入資料，並覆寫 `mydataset` 中名為 `mytable` 的資料表。

```
    bq load \
    --replace \
    --source_format=PARQUET \
    mydataset.mytable \
    gs://mybucket/mydata.parquet
```

下列指令會從 `gs://mybucket/mydata.parquet` 載入資料，並將資料附加至 `mydataset` 中名為 `mytable` 的資料表。

```
    bq load \
    --noreplace \
    --source_format=PARQUET \
    mydataset.mytable \
    gs://mybucket/mydata.parquet
```

如要瞭解如何使用 bq 指令列工具附加及覆寫已分割資料表的資料，請參閱「[附加及覆寫已分割資料表的資料](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#append-overwrite)」。

### API

1. 建立指向 Cloud Storage 中來源資料的 `load` 工作。
2. (選擇性操作) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。
3. `source URIs` 屬性必須是完整名稱，格式為 `gs://BUCKET/OBJECT`。您可以使用以逗號分隔清單的形式包含多個 URI。請注意，系統也支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。
4. 藉由將 `configuration.load.sourceFormat` 屬性設為 `PARQUET`，以指定資料格式。
5. 藉由將 `configuration.load.writeDisposition` 屬性設為 `WRITE_TRUNCATE` 或 `WRITE_APPEND`，以指定寫入偏好設定。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// importParquetTruncate demonstrates loading Apache Parquet data from Cloud Storage into a table
// and overwriting/truncating existing data in the table.
func importParquetTruncate(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states.parquet")
	gcsRef.SourceFormat = bigquery.Parquet
	gcsRef.AutoDetect = true
	loader := client.Dataset(datasetID).Table(tableID).LoaderFrom(gcsRef)
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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.JobInfo.WriteDisposition;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.TableId;
import java.math.BigInteger;

public class LoadParquetReplaceTable {

  public static void runLoadParquetReplaceTable() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    loadParquetReplaceTable(datasetName);
  }

  public static void loadParquetReplaceTable(String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Imports a GCS file into a table and overwrites table data if table already exists.
      // This sample loads CSV file at:
      // https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.csv
      String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.parquet";
      TableId tableId = TableId.of(datasetName, "us_states");

      // For more information on LoadJobConfiguration see:
      // https://googleapis.dev/java/google-cloud-clients/latest/com/google/cloud/bigquery/LoadJobConfiguration.Builder.html
      LoadJobConfiguration configuration =
          LoadJobConfiguration.builder(tableId, sourceUri)
              .setFormatOptions(FormatOptions.parquet())
              // Set the write disposition to overwrite existing table data.
              .setWriteDisposition(WriteDisposition.WRITE_TRUNCATE)
              .build();

      // For more information on Job see:
      // https://googleapis.dev/java/google-cloud-clients/latest/index.html?com/google/cloud/bigquery/package-summary.html
      // Load the table
      Job job = bigquery.create(JobInfo.of(configuration));

      // Load data from a GCS parquet file into the table
      // Blocks until this load table job completes its execution, either failing or succeeding.
      Job completedJob = job.waitFor();
      if (completedJob == null) {
        System.out.println("Job not executed since it no longer exists.");
        return;
      } else if (completedJob.getStatus().getError() != null) {
        System.out.println(
            "BigQuery was unable to load into the table due to an error: \n"
                + job.getStatus().getError());
        return;
      }

      // Check number of rows loaded into the table
      BigInteger numRows = bigquery.getTable(tableId).getNumRows();
      System.out.printf("Loaded %d rows. \n", numRows);

      System.out.println("GCS parquet overwrote existing table successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Table extraction job was interrupted. \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client libraries
const {BigQuery} = require('@google-cloud/bigquery');
const {Storage} = require('@google-cloud/storage');

// Instantiate clients
const bigquery = new BigQuery();
const storage = new Storage();

/**
 * This sample loads the CSV file at
 * https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.csv
 *
 * TODO(developer): Replace the following lines with the path to your file.
 */
const bucketName = 'cloud-samples-data';
const filename = 'bigquery/us-states/us-states.parquet';

async function loadParquetFromGCSTruncate() {
  /**
   * Imports a GCS file into a table and overwrites
   * table data if table already exists.
   */

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";

  // Configure the load job. For full list of options, see:
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationLoad
  const metadata = {
    sourceFormat: 'PARQUET',
    // Set the write disposition to overwrite existing table data.
    writeDisposition: 'WRITE_TRUNCATE',
    location: 'US',
  };

  // Load data from a Google Cloud Storage file into the table
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .load(storage.bucket(bucketName).file(filename), metadata);
  // load() waits for the job to finish
  console.log(`Job ${job.id} completed.`);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;
use Google\Cloud\Core\ExponentialBackoff;

/** Uncomment and populate these variables in your code */
// $projectId = 'The Google project ID';
// $datasetId = 'The BigQuery dataset ID';
// $tableID = 'The BigQuery table ID';

// instantiate the bigquery table service
$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$table = $bigQuery->dataset($datasetId)->table($tableId);

// create the import job
$gcsUri = 'gs://cloud-samples-data/bigquery/us-states/us-states.parquet';
$loadConfig = $table->loadFromStorage($gcsUri)->sourceFormat('PARQUET')->writeDisposition('WRITE_TRUNCATE');
$job = $table->runJob($loadConfig);

// poll the job until it is complete
$backoff = new ExponentialBackoff(10);
$backoff->execute(function () use ($job) {
    print('Waiting for job to complete' . PHP_EOL);
    $job->reload();
    if (!$job->isComplete()) {
        throw new Exception('Job has not yet completed', 500);
    }
});

// check if the job has errors
if (isset($job->info()['status']['errorResult'])) {
    $error = $job->info()['status']['errorResult']['message'];
    printf('Error running job: %s' . PHP_EOL, $error);
} else {
    print('Data imported successfully' . PHP_EOL);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要將資料列附加至現有資料表，請將 [`LoadJobConfig.write_disposition` 屬性](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_write_disposition)設為 [`WRITE_APPEND`](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.enums.WriteDisposition?hl=zh-tw#google.cloud.bigquery.enums.WriteDisposition.WRITE_APPEND)。

如要取代現有資料表中的資料列，請將 [`LoadJobConfig.write_disposition` 屬性](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_write_disposition)設為 [`WRITE_TRUNCATE`](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.enums.WriteDisposition?hl=zh-tw#google.cloud.bigquery.enums.WriteDisposition.WRITE_TRUNCATE)。

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
    source_format=bigquery.SourceFormat.PARQUET,
)

uri = "gs://cloud-samples-data/bigquery/us-states/us-states.parquet"
load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
```

## 載入 Hive 分區的 Parquet 資料

BigQuery 支援載入儲存在 Cloud Storage 的 Hive 分區 Parquet 資料，並將 Hive 分區資料欄填入目的地 BigQuery 代管資料表。詳情請參閱「[載入外部分區資料](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw)」。

## Parquet 轉換

本節說明載入 Parquet 資料時，BigQuery 如何剖析各種資料類型。

部分 Parquet 資料型別 (例如 `INT32`、`INT64`、`BYTE_ARRAY` 和 `FIXED_LEN_BYTE_ARRAY`) 可以轉換為多個 BigQuery 資料型別。為確保 BigQuery 正確轉換 Parquet 資料類型，請在 Parquet 檔案中指定適當的資料類型。

舉例來說，如要將 Parquet `INT32` 資料類型轉換為 BigQuery `DATE` 資料類型，請指定下列項目：

```
optional int32 date_col (DATE);
```

BigQuery 會將 Parquet 資料類型轉換為下列章節所述的 BigQuery 資料類型。

### 類型轉換

| Parquet 類型 | Parquet 邏輯型別 | BigQuery 資料類型 |
| --- | --- | --- |
| `BOOLEAN` | 無 | BOOLEAN |
| INT32 | 無，`INTEGER` (`UINT_8`、`UINT_16`、 `UINT_32`、`INT_8`、`INT_16`、 `INT_32`) | INT64 |
| INT32 | [DECIMAL](#decimal_logical_type) | NUMERIC、BIGNUMERIC 或 STRING |
| `INT32` | `DATE` | DATE |
| `INT32` | `TIME`、`precision=MILLIS` (`TIME_MILLIS`) | 時間 |
| `INT64` | 無，`INTEGER` (`UINT_64`、`INT_64`) | INT64 |
| INT64 | [DECIMAL](#decimal_logical_type) | NUMERIC、BIGNUMERIC 或 STRING |
| `INT64` | `TIME`、`precision=MICROS` (`TIME_MICROS`) | 時間 |
| `INT64` | `TIMESTAMP`、`precision=MILLIS` (`TIMESTAMP_MILLIS`) | TIMESTAMP |
| `INT64` | `TIMESTAMP`、`precision=MICROS` (`TIMESTAMP_MICROS`) | TIMESTAMP |
| `INT96` | 無 | TIMESTAMP |
| `FLOAT` | 無 | FLOAT64 |
| `DOUBLE` | 無 | FLOAT64 |
| `BYTE_ARRAY` | 無 | BYTES |
| `BYTE_ARRAY` | `STRING` (`UTF8`) | STRING |
| FIXED\_LEN\_BYTE\_ARRAY | [DECIMAL](#decimal_logical_type) | NUMERIC、BIGNUMERIC 或 STRING |
| `FIXED_LEN_BYTE_ARRAY` | 無 | BYTES |

巢狀群組會轉換為 [`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type) 型別。系統不支援其他 Parquet 類型與轉換類型的組合。

### 未簽署的邏輯型別

Parquet `UINT_8`、`UINT_16`、`UINT_32` 和 `UINT_64` 類型為無符號。
將這些類型的值載入 BigQuery 已簽署的 `INTEGER` 資料欄時，BigQuery 會將這些值視為未簽署。如果是 `UINT_64`，如果無符號值超過 9,223,372,036,854,775,807 的最大 `INTEGER` 值，就會傳回錯誤。

### Decimal 邏輯類型

`Decimal` 邏輯型別可轉換為 `NUMERIC`、`BIGNUMERIC` 或 `STRING` 型別。轉換後的型別取決於 `decimal` 邏輯型別的有效位數和小數位數參數，以及指定的小數目標型別。請依下列方式指定十進位目標類型：

* 如要使用 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 進行[載入作業](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，請使用 [`JobConfigurationLoad.decimalTargetTypes`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.decimal_target_types) 欄位。
* 如要使用 bq 指令列工具中的 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令執行[載入工作](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，請使用 [`--decimal_target_types`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#flags_and_arguments_9) 旗標。
* 如要查詢[具有外部來源的資料表](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)：
  請使用 [`ExternalDataCon`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#ExternalDataConfiguration.FIELDS.decimal_target_types)