Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

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

[Parquet](http://parquet.apache.org) 是 Apache Hadoop 生態系統廣泛使用的開放原始碼資料欄導向資料格式。

從 Cloud Storage 載入 Parquet 資料時，可將資料載入新的資料表或分區、或對現有資料表或分區進行附加或覆寫作業。將資料載入 BigQuery 時，資料會轉換為 [Capacitor](https://cloud.google.com/blog/products/gcp/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw) 資料欄格式 (BigQuery 的儲存格式)。

將資料從 Cloud Storage 載入 BigQuery 資料表時，該資料表所屬的資料集必須位於和 Cloud Storage 值區相同的地區或多地區位置。

如要瞭解如何從本機檔案載入 Parquet 資料，請參閱[從本機檔案載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)。

## 限制

將資料從 Cloud Storage 值區載入 BigQuery 時有下列限制：

* BigQuery 不保證外部資料來源的資料一致性。如果基礎資料在查詢執行期間遭到變更，可能會導致非預期的行為。
* BigQuery 不支援 [Cloud Storage 物件版本控管](https://docs.cloud.google.com/storage/docs/object-versioning?hl=zh-tw)。如果 Cloud Storage URI 中包含版本編號，載入作業就會失敗。
* 如果載入的檔案有不同的結構定義，您就無法在 Cloud Storage URI 中使用萬用字元。只要欄位位置不同，即為不同的結構定義。

## 輸入檔案規定

如要避免將 Parquet 檔案載入 BigQuery 時發生 `resourcesExceeded` 錯誤，請遵守下列規範：

* 資料列大小不得超過 50 MB。
* 如果輸入資料包含超過 100 欄，請考慮將頁面大小縮減為小於預設頁面大小 (1 \* 1024 \* 1024 位元組)。如果您使用大量壓縮，這項功能就特別實用。
* 為獲得最佳效能，請將資料列群組大小設為至少 16 MiB。
  如果列群組大小較小，I/O 會增加，載入和查詢速度也會變慢。

## 事前準備

授予 Identity and Access Management (IAM) 角色，讓使用者具備執行本文中各項工作所需的權限，並建立資料集來儲存資料。

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

在 bq 指令列工具中執行這項指令，即可載入所有檔案 (以逗號分隔的清單)，且結構定義衍生自 `mybucket/01/b.parquet`：

```
bq load \
--source_format=PARQUET \
dataset.table \
"gs://mybucket/00/*.parquet","gs://mybucket/01/*.parquet"
```

載入具有不同結構定義的多個 Parquet 檔案時，不同結構定義中指定的相同資料欄必須在各個結構定義中採用相同的[模式](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#modes)。

BigQuery 偵測結構定義時，部分 Parquet 資料類型會轉換為 BigQuery 資料類型，使其與 GoogleSQL 語法相容。詳情請參閱 [Parquet 轉換](#parquet_conversions)。

如要提供資料表結構定義來建立外部資料表，請在 BigQuery API 中設定 `referenceFileSchemaUri` 屬性，或在 bq 指令列工具中設定   
`--reference_file_schema_uri` 參數，指向參照檔案的網址。

例如 `--reference_file_schema_uri="gs://mybucket/schema.parquet"`。

## Parquet 壓縮

BigQuery 支援下列 Parquet 檔案內容的壓縮轉碼器：

* `GZip`
* `LZO_1C`
* `LZO_1X`
* `LZ4_RAW`
* `Snappy`
* `ZSTD`

## 將 Parquet 資料載入至新的資料表

您可以透過下列方式將 Parquet 資料載入新的資料表：

* Google Cloud 控制台
* bq 指令列工具的 `bq load` 指令
* `jobs.insert` API 方法並設定 `load` 工作
* 用戶端程式庫

如要將 Parquet 資料從 Cloud Storage 載入新的 BigQuery 資料表，請執行下列操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「來源」部分中，從「建立資料表來源」清單中選取「Google Cloud Storage」。
   接著，按照下列步驟操作：
   1. 從 Cloud Storage bucket 選取檔案，或輸入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。
      您無法在 Google Cloud 控制台中加入多個 URI，但支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage 值區的位置必須與要建立、附加或覆寫的表格所在的資料集位置相同。
   2. 在「File format」(檔案格式) 部分，選取「Parquet」。
2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。Parquet 檔案的結構定義為自述式。
4. 選用：指定「分區與叢集設定」。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。
5. 按一下「進階選項」，然後執行下列操作：
   * 讓「Write preference」(寫入偏好設定) 的 [Write if empty] (空白時寫入) 選項維持在已選取狀態。這個選項能建立新的資料表，並將您的資料載入其中。
   * 如要忽略不在資料表結構定義中的資料列值，請選取「Unknown values」(不明的值)。
   * 針對 **Encryption**，請按一下 **Customer-managed key**，以使用 [Cloud Key Management Service key](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果您保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
6. 點選「建立資料表」。

**注意：** 使用Google Cloud 控制台 將資料載入空白資料表時，您無法新增標籤、說明、資料表到期時間或分區到期時間。  
  
資料表建立完成之後，您就能更新資料表的到期時間、說明和標籤，但您無法在使用 Google Cloud 控制台建立資料表之後，新增分區到期時間。詳情請參閱[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)。

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

* `--time_partitioning_type`：針對資料表啟用時間分區並設定分區類型。可能的值為 `HOUR`、`DAY`、`MONTH` 和 `YEAR`。如果您在 `DATE`、`DATETIME` 或 `TIMESTAMP` 資料欄建立分區資料表，則不一定要使用這個旗標。時間分區的預設分區類型為 `DAY`。您無法變更現有資料表的分區規格。
* `--time_partitioning_expiration`：這是一個整數，用來指定系統應在何時刪除時間分區 (以秒為單位)。到期時間為分區的世界標準時間日期加整數值。
* `--time_partitioning_field`：用於建立分區資料表的 `DATE` 或 `TIMESTAMP` 資料欄。如果啟用時間分區時沒有這個值，系統就會建立擷取時間分區資料表。
* `--require_partition_filter`：這個選項啟用後，系統會要求使用者加入 `WHERE` 子句，以指定要查詢的分區。使用分區篩選器可以降低成本並提升效能。詳情請參閱[在查詢中要求使用分區篩選器](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)。
* `--clustering_fields`：以半形逗號分隔的資料欄名稱清單 (最多四個名稱)，可用來建立[分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)。
* `--destination_kms_key`：用來加密資料表資料的 Cloud KMS 金鑰。
* `--column_name_character_map`：定義資料欄名稱字元的範圍和處理方式，並可選擇啟用[彈性資料欄名稱](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#flexible-column-names)。詳情請參閱「[`load_option_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_option_list)」。如要進一步瞭解支援和不支援的字元，請參閱「[更靈活的資料欄名稱](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#flexible-column-names)」。

  如要進一步瞭解分區資料表，請參閱：

  + [建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)

  如要進一步瞭解叢集資料表，請參閱下列說明：

  + [建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)

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

* `LOCATION`：您的位置。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)，設定該位置的預設值。
* `FORMAT`: `PARQUET`.
* `DATASET`：現有資料集。
* `TABLE`：您要載入資料的資料表名稱。
* `PATH_TO_SOURCE`：完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或是以逗號分隔的清單 URI。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。

範例：

下列指令會將資料從 `gs://mybucket/mydata.parquet` 載入到 `mydataset` 中名為 `mytable` 的資料表。

```
    bq load \
    --source_format=PARQUET \
    mydataset.mytable \
    gs://mybucket/mydata.parquet
```

下列指令會將資料從 `gs://mybucket/mydata.parquet` 載入到 `mydataset` 中名為 `mytable` 的新擷取時間分區資料表。

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
3. `source URIs` 屬性必須是完整的，且必須符合下列格式：`gs://BUCKET/OBJECT`。每個 URI 可包含一個「\*」[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。
4. 將 `sourceFormat` 屬性設為 `PARQUET`，以指定 Parquet 資料格式。
5. 如要檢查工作狀態，請呼叫 [`jobs.get(JOB_ID*)`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/get?hl=zh-tw)，並將 JOB\_ID 替換為初始要求傳回的工作 ID。

   * 如果是 `status.state = DONE`，代表工作已順利完成。
   * 如果出現 `status.errorResult` 屬性，代表要求執行失敗，且該物件會包含描述問題的相關資訊。如果要求執行失敗，系統就不會建立任何資料表，也不會載入任何資料。
   * 如果未出現 `status.errorResult`，代表工作順利完成，但可能有一些不嚴重的錯誤，例如少數資料列在匯入時發生問題。不嚴重的錯誤都會列在已傳回工作物件的 `status.errors` 屬性中。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 [Client.load\_table\_from\_uri()](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_load_table_from_uri) 方法，從 Cloud Storage 啟動載入工作。如要使用 Parquet，請將 [LoadJobConfig.source\_format 屬性](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_source_format)設為 `PARQUET` 字串，並將工作設定當做 `job_config` 引數傳送至 `load_table_from_uri()` 方法。

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

在 Google Cloud 主控台中，使用「寫入偏好設定」選項，指定從來源檔案或查詢結果載入資料時採取的動作。

將額外資料載入資料表時，可以選擇下列選項：

| 主控台選項 | bq 工具旗標 | BigQuery API 屬性 | 說明 |
| --- | --- | --- | --- |
| 空白時寫入 | 不支援 | `WRITE_EMPTY` | 資料表空白時才會寫入資料。 |
| 附加到資料表中 | `--noreplace` 或 `--replace=false`；如果未指定 `--[no]replace`，則預設動作為附加 | `WRITE_APPEND` | ([預設](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.write_disposition)) 將資料附加至資料表尾端。 |
| 覆寫資料表 | `--replace`或`--replace=true` | `WRITE_TRUNCATE` | 先清除資料表中所有現有資料，再寫入新的資料。 這項操作也會刪除資料表結構定義、資料列層級安全性，並移除所有 Cloud KMS 金鑰。 |

如果您將資料載入現有資料表，該載入工作可附加資料，或覆寫資料表。

您可以透過下列方式來對資料表進行附加或覆寫作業：

* Google Cloud 控制台
* bq 指令列工具的 `bq load` 指令
* `jobs.insert` API 方法並設定 `load` 工作
* 用戶端程式庫

**注意：**本頁面未說明如何對分區資料表進行附加或覆寫。如要瞭解如何對分區資料表進行附加或覆寫，請參閱[對分區資料表中的資料執行附加或覆寫操作](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#append-overwrite)一節。

如要使用 Parquet 資料對資料表進行附加或覆寫，請執行下列操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「來源」部分中，從「建立資料表來源」清單中選取「Google Cloud Storage」。
   接著，按照下列步驟操作：
   1. 從 Cloud Storage bucket 選取檔案，或輸入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。
      您無法在 Google Cloud 控制台中加入多個 URI，但支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage 值區的位置必須與要建立、附加或覆寫的表格所在的資料集位置相同。
   2. 在「File format」(檔案格式) 部分，選取「Parquet」。
**注意：**您可以在附加或覆寫資料表時修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱「[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)」一文。
2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。Parquet 檔案的結構定義為自述式。
**注意：**您可以在附加或覆寫資料表時修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。4. 選用：指定「分區與叢集設定」。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。您無法藉由附加或覆寫的方式，將資料表轉換為分區資料表或分群資料表。 Google Cloud 控制台不支援在載入工作中附加資料到分區或叢集資料表，也不支援覆寫分區或叢集資料表。
5. 按一下「進階選項」，然後執行下列操作：
   * 針對「Write preference」(寫入偏好設定)，請選擇「Append to table」(附加到資料表中) 或「Overwrite table」(覆寫資料表)。
   * 如要忽略不在資料表結構定義中的資料列值，請選取「Unknown values」(不明的值)。
   * 針對 **Encryption**，請按一下 **Customer-managed key**，以使用 [Cloud Key Management Service key](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果您保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
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

如要覆寫資料表，請輸入 `bq load` 指令並加上 `--replace` 旗標。如要附加資料至資料表，使用 `--noreplace` 旗標。若未指定任何旗標，預設動作為附加資料。提供 `--source_format` 旗標，並將其設為 `PARQUET`。由於系統會自動從自述來源資料中擷取 Parquet 結構定義，所以您不需要提供結構定義。

**注意：**您可以在對資料表進行附加或覆寫作業時修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)一文。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

其他選用標記包括：

* `--destination_kms_key`：用來加密資料表資料的 Cloud KMS 金鑰。

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
* `table`：您要載入資料的資料表名稱。
* `path_to_source`：完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或是以逗號分隔的清單 URI。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。

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

如要瞭解如何使用 bq 指令列工具附加和覆寫分區資料表，請參閱[對分區資料表中的資料執行附加或覆寫操作](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#append-overwrite)。

### API

1. 建立指向 Cloud Storage 中來源資料的 `load` 工作。
2. (選擇性操作) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。
3. `source URIs` 屬性必須是完整的，且必須符合下列格式：`gs://BUCKET/OBJECT`。您可以使用以逗號分隔清單的形式包含多個 URI。請注意，系統也支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。
4. 藉由將 `configuration.load.sourceFormat` 屬性設為 `PARQUET`，以指定資料格式。
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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要將資料列附加到現有資料表，請將 [`LoadJobConfig.write_disposition` 屬性](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_write_disposition)設為 [`WRITE_APPEND`](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.enums.WriteDisposition?hl=zh-tw#google.cloud.bigquery.enums.WriteDisposition.WRITE_APPEND)。

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

BigQuery 支援載入儲存在 Cloud Storage 的 Hive 分區 Parquet 資料，並且會將目標 BigQuery 代管資料表中的資料欄，填入 Hive 分區的資料欄。詳情請參閱[載入外部分區資料](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw)。

## Parquet 轉換

本節說明 BigQuery 在載入 Parquet 資料時，如何剖析各種資料類型。

部分 Parquet 資料類型 (例如 `INT32`、`INT64`、`BYTE_ARRAY` 和 `FIXED_LEN_BYTE_ARRAY`) 可以轉換為多種 BigQuery 資料類型。為確保 BigQuery 正確轉換 Parquet 資料類型，請在 Parquet 檔案中指定適當的資料類型。

舉例來說，如要將 Parquet `INT32` 資料類型轉換為 BigQuery `DATE` 資料類型，請指定下列項目：

```
optional int32 date_col (DATE);
```

BigQuery 會將 Parquet 資料類型轉換為下列各節所述的 BigQuery 資料類型。

### 類型轉換

| Parquet 類型 | Parquet 邏輯類型 | BigQuery 資料類型 |
| --- | --- | --- |
| `BOOLEAN` | 無 | BOOLEAN |
| INT32 | 無，`INTEGER` (`UINT_8`、`UINT_16`、 `UINT_32`、`INT_8`、`INT_16`、 `INT_32`) | INT64 |
| INT32 | [DECIMAL](#decimal_logical_type) | NUMERIC、BIGNUMERIC 或 STRING |
| `INT32` | `DATE` | DATE |
| `INT64` | 無，`INTEGER` (`UINT_64`、`INT_64`) | INT64 |
| INT64 | [DECIMAL](#decimal_logical_type) | NUMERIC、BIGNUMERIC 或 STRING |
| `INT64` | `TIMESTAMP`，`precision=MILLIS` (`TIMESTAMP_MILLIS`) | TIMESTAMP |
| `INT64` | `TIMESTAMP`，`precision=MICROS` (`TIMESTAMP_MICROS`) | TIMESTAMP |
| `INT96` | 無 | TIMESTAMP |
| `FLOAT` | 無 | FLOAT64 |
| `DOUBLE` | 無 | FLOAT64 |
| `BYTE_ARRAY` | 無 | BYTES |
| `BYTE_ARRAY` | `STRING` (`UTF8`) | STRING |
| FIXED\_LEN\_BYTE\_ARRAY | [DECIMAL](#decimal_logical_type) | NUMERIC、BIGNUMERIC 或 STRING |
| `FIXED_LEN_BYTE_ARRAY` | 無 | BYTES |

巢狀群組會轉換為 [`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type) 類型。系統不支援其他 Parquet 類型與轉換類型的組合。

### 不帶正負號的邏輯類型

Parquet `UINT_8`、`UINT_16`、`UINT_32` 和 `UINT_64` 類型為不帶正負號。
載入 BigQuery 帶正負號的 `INTEGER` 欄時，BigQuery 會將這些類型的值視為不帶正負號。如果是 `UINT_64`，如果無符號值超過 9,223,372,036,854,775,807 的最大 `INTEGER` 值，就會傳回錯誤。

### Decimal 邏輯類型

`Decimal` 邏輯型別可以轉換為 `NUMERIC`、`BIGNUMERIC` 或 `STRING` 型別。轉換後的型別取決於 `decimal` 邏輯型別的精確度和比例參數，以及指定的小數目標型別。請按照下列方式指定十進位目標類型：

* 如要使用 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 進行[載入作業](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，請使用 [`JobConfigurationLoad.decimalTargetTypes`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.decimal_target_types) 欄位。
* 如要使用 bq 指令列工具中的 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令執行[載入工作](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，請使用 [`--decimal_target_types`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#flags_and_arguments_9) 旗標。
* 如要查詢[含有外部來源的資料表](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)：
  請使用 [`ExternalDataConfiguration.decimalTargetTypes`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#ExternalDataConfiguration.FIELDS.decimal_target_types) 欄位。
* 如果是[使用 DDL 建立的永久外部資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)：
  請使用 [`decimal_target_types`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#external_table_option_list) 選項。

### 列舉邏輯類型

`Enum` 邏輯型別可以轉換為 `STRING` 或 `BYTES`。請依下列方式指定轉換後的目標類型：

* 如要使用 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 進行[載入作業](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，請使用 [`JobConfigurationLoad.parquetOptions`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.parquet_options) 欄位。
* 如要使用 bq 指令列工具中的 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令執行[載入工作](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，請使用 [`--parquet_enum_as_string`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#parquet_enum_as_string_flag) 旗標。
* 如要使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 建立永久外部資料表：
  請使用 [`--parquet_enum_as_string`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) 旗標。

### 清單邏輯類型

您可以為 Parquet `LIST` 邏輯型別啟用結構定義推論功能。BigQuery 會檢查 `LIST` 節點是否為[標準形式](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#lists)，或是[回溯相容規則](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#backward-compatibility-rules)所述的形式之一：

```
// standard form
<optional | required> group <name> (LIST) {
  repeated group list {
    <optional | required> <element-type> element;
  }
}
```

如果是，轉換後結構定義中 `LIST` 節點的對應欄位會視為具有下列結構定義：

```
repeated <element-type> <name>
```

省略「list」和「element」節點。

* 如要使用 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 進行[載入工作](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，請使用 [`JobConfigurationLoad.parquetOptions` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.parquet_options)。
* 如要使用 bq 指令列工具中的 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令執行[載入工作](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，請使用 [`--parquet_enable_list_inference` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#parquet_enable_list_inference_flag)。
* 如果是使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 建立的永久外部資料表，請使用 [`--parquet_enable_list_inference` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)。
* 如要使用 [`CREATE EXTERNAL TABLE` 陳述式建立永久外部資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)，請使用 [`enable_list_inference` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#external_table_option_list)。

### 地理空間資料

您可以載入 Parquet 檔案，其中包含 `STRING` 資料欄中的 [WKT](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)、十六進位編碼的 [WKB](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) 或 [GeoJSON](https://geojson.org/)，或是 `BYTE_ARRAY` 資料欄中的 [WKB](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)，方法是指定類型為 `GEOGRAPHY` 的 BigQuery 結構定義。詳情請參閱「[載入地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw#loading_geospatial_data)」。

您也可以載入 [GeoParquet](https://geoparquet.org) 檔案。在此情況下，GeoParquet 中繼資料描述的資料欄預設會解譯為 `GEOGRAPHY` 型別。您也可以提供明確的結構定義，將原始 WKB 資料載入 `BYTES` 資料欄。詳情請參閱「[載入 GeoParquet 檔案](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw#loading_geoparquet_files)」。

### 資料欄名稱轉換

欄名可包含英文字母 (a-z、A-Z)、數字 (0-9) 或底線 (\_)，且開頭必須是英文字母或底線。如果您使用彈性資料欄名稱，BigQuery 支援以數字開頭的資料欄名稱。請謹慎使用數字開頭的資料欄，因為使用 BigQuery Storage Read API 或 BigQuery Storage Write API 時，如果資料欄名稱開頭是數字，需要特別處理。如要進一步瞭解彈性資料欄名稱支援功能，請參閱「[彈性資料欄名稱](#flexible-column-names)」。

欄名的長度上限為 300 個字元。資料欄名稱不得使用以下任何一個前置字串：

* `_TABLE_`
* `_FILE_`
* `_PARTITION`
* `_ROW_TIMESTAMP`
* `__ROOT__`
* `_COLIDENTIFIER`
* `_CHANGE_SEQUENCE_NUMBER`
* `_CHANGE_TYPE`
* `_CHANGE_TIMESTAMP`

資料欄名稱不得重複，即使大小寫不同也是如此。舉例來說，系統會將 `Column1` 和 `column1` 這兩個資料欄名稱視為相同。如要進一步瞭解資料欄命名規則，請參閱 GoogleSQL 參考資料中的「[資料欄名稱](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#column_names)」。

如果資料表名稱 (例如 `test`) 與其中一個資料欄名稱 (例如 `test`) 相同，`SELECT` 運算式會將 `test` 資料欄解讀為包含所有其他資料表資料欄的 `STRUCT`。如要避免發生這種衝突，請使用下列其中一種方法：

* 請勿為表格及其資料欄使用相同名稱。
* 請避免使用 `_field_` 做為資料欄名稱前置字串。系統保留的前置字元會導致查詢期間自動重新命名。舉例來說，`SELECT _field_ FROM project1.dataset.test` 查詢會傳回名為 `_field_1` 的資料欄。如要查詢具有這個名稱的資料欄，請使用別名控制輸出內容。
* 為表格指派其他別名。舉例來說，下列查詢會將資料表別名 `t` 指派給資料表 `project1.dataset.test`：

  ```
  SELECT test FROM project1.dataset.test AS t;
  ```
* 參照資料欄時，請一併提供資料表名稱。例如：

  ```
  SELECT test.test FROM project1.dataset.test;
  ```

### 彈性設定資料欄名稱

資料欄名稱的命名方式更靈活，包括擴大支援非英文語言的字元，以及其他符號。如果彈性資料欄名稱是[加上引號的 ID](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#quoted_identifiers)，請務必使用倒引號 (`` ` ``) 字元括住。

彈性資料欄名稱支援下列字元：

* 任何語言的任何字母，以 Unicode 規則運算式 [`\p{L}`](https://www.unicode.org/reports/tr44/#General_Category_Values) 表示。
* 任何語言的任何數字字元，以 Unicode 正規運算式 [`\p{N}`](https://www.unicode.org/reports/tr44/#General_Category_Values) 表示。
* 任何連接符號字元，包括底線，以 Unicode 規則運算式 [`\p{Pc}`](https://www.unicode.org/reports/tr44/#General_Category_Values) 表示。
* 連字號或破折號，以 Unicode 規則運算式 [`\p{Pd}`](https://www.unicode.org/reports/tr44/#General_Category_Values) 表示。
* 任何預期會與另一個字元搭配使用的標記，以 Unicode 規則運算式 [`\p{M}`](https://www.unicode.org/reports/tr44/#General_Category_Values) 表示。例如重音符號、母音變音或外框。
* 下列特殊字元：
  + 以 Unicode 規則運算式 `\u0026` 表示的連接符號 (`&`)。
  + 百分比符號 (`%`)，以 Unicode 規則運算式 `\u0025` 表示。
  + 等號 (`=`)，以 Unicode 規則運算式 `\u003D` 表示。
  + 加號 (`+`)，以 Unicode 規則運算式 `\u002B` 表示。
  + 冒號 (`:`)，以 Unicode 規則運算式 `\u003A` 表示。
  + 以 Unicode 規則運算式 `\u0027` 表示的單引號 (`'`)。
  + 小於符號 (`<`)，以 Unicode 正規運算式 `\u003C` 表示。
  + 大於符號 (`>`)，以 Unicode 規則運算式 `\u003E` 表示。
  + 井號 (`#`)，以 Unicode 正則運算式 `\u0023` 表示。
  + 垂直線 (`|`)，以 Unicode 規則運算式 `\u007c` 表示。
  + 空格字元。

彈性資料欄名稱不支援下列特殊字元：

* 驚嘆號 (`!`)，以 Unicode 規則運算式 `\u0021` 表示。
* 半形雙引號 (`"`)，以 Unicode 規則運算式 `\u0022` 表示。
* 以 Unicode 規則運算式 `\u0024` 表示的錢幣符號 (`$`)。
* 左括號 (`(`)，以 Unicode 規則運算式 `\u0028` 表示。
* 右括號 (`)`)，以 Unicode 規則運算式 `\u0029` 表示。
* 星號 (`*`)，以 Unicode 規則運算式 `\u002A` 表示。
* 以 Unicode 規則運算式 `\u002C` 表示的逗號 (`,`)。
* 句號 (`.`)，以 Unicode 規則運算式 `\u002E` 表示。使用資料欄名稱字元對應時，Parquet 檔案資料欄名稱中的句號*不會*替換為底線。詳情請參閱[彈性資料欄限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#limitations_2)。
* 斜線 (`/`)，以 Unicode 規則運算式 `\u002F` 表示。
* 以 Unicode 規則運算式 `\u003B` 表示的分號 (`;`)。
* 問號 (`?`)，以 Unicode 規則運算式 `\u003F` 表示。
* 以 Unicode 規則運算式 `\u0040` 表示的 at 符號 (`@`)。
* 左方括號 (`[`)，以 Unicode 規則運算式 `\u005B` 表示。
* 反斜線 (`\`)，以 Unicode 規則運算式 `\u005C` 表示。
* 右方括號 (`]`)，以 Unicode 正則運算式 `\u005D` 表示。
* Unicode 規則運算式 `\u005E` 代表的揚抑符號 (`^`)。
* Unicode 規則運算式 `\u0060` 代表的重音符 (`` ` ``)。
* 左大括號 {`{`)，以 Unicode 規則運算式 `\u007B` 表示。
* 右大括號 (`}`)，以 Unicode 正則運算式 `\u007D` 表示。
* 波浪號 (`~`)，以 Unicode 規則運算式 `\u007E` 表示。

如需其他規範，請參閱「[資料欄名稱](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#column_names)」。

BigQuery Storage Read API 和 BigQuery Storage Write API 都支援擴充的欄字元。如要透過 BigQuery Storage Read API 使用擴充的 Unicode 字元清單，必須設定旗標。您可以使用 `displayName` 屬性擷取資料欄名稱。以下範例說明如何使用 Python 用戶端設定旗標：

```
from google.cloud.bigquery_storage import types
requested_session = types.ReadSession()

#set avro serialization options for flexible column.
options = types.AvroSerializationOptions()
options.enable_display_name_attribute = True
requested_session.read_options.avro_serialization_options = options
```

如要透過 BigQuery Storage Write API 使用擴充的 Unicode 字元清單，您必須提供含有 `column_name` 標記的結構定義，除非您使用 `JsonStreamWriter` 寫入器物件。以下範例說明如何提供結構定義：

```
syntax = "proto2";
package mypackage;
// Source protos located in github.com/googleapis/googleapis
import "google/cloud/bigquery/storage/v1/annotations.proto";

message
```