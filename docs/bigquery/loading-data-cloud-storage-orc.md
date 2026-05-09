Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Cloud Storage 載入 ORC 資料

本頁面提供將 ORC 資料從 Cloud Storage 載入至 BigQuery 的總覽。

[ORC](http://orc.apache.org) 是一種開放原始碼資料欄導向的資料格式，在 Apache Hadoop 生態系統中被廣泛使用。

從 Cloud Storage 載入 ORC 資料時，可將資料載入至新的資料表或分區，或將資料附加到現有資料表或分區，或覆寫現有資料表或分區。將資料載入 BigQuery 時，資料會轉換為 [Capacitor](https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw) 資料欄格式 (BigQuery 的儲存格式)。

將資料從 Cloud Storage 載入 BigQuery 資料表時，該資料表所屬的資料集必須位於和 Cloud Storage 值區相同的地區或多地區位置。

如需從本機檔案載入 ORC 資料的相關資訊，請參閱
[將資料從本機資料來源載入至 BigQuery](https://docs.cloud.google.com/bigquery/docs/loading-data-local?hl=zh-tw)。

## 限制

將資料從 Cloud Storage 值區載入 BigQuery 時有下列限制：

* BigQuery 不保證外部資料來源的資料一致性。如果基礎資料在查詢執行期間遭到變更，可能會導致非預期的行為。
* BigQuery 不支援 [Cloud Storage 物件版本控管](https://docs.cloud.google.com/storage/docs/object-versioning?hl=zh-tw)。如果 Cloud Storage URI 中包含版本編號，載入作業就會失敗。

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

## ORC 結構定義

您將 ORC 檔案載入至 BigQuery 時，系統會透過自述式來源資料自動擷取資料表結構定義。當 BigQuery 從來源資料擷取結構定義時，會按照字母順序使用最後一個檔案。

舉例來說，Cloud Storage 中有下列 ORC 檔案：

```
gs://mybucket/00/
  a.orc
  z.orc
gs://mybucket/01/
  b.orc
```

在 bq 指令列工具中執行這項指令，即可載入所有檔案 (以逗號分隔的清單)，且結構定義衍生自 `mybucket/01/b.orc`：

```
bq load \
--source_format=ORC \
dataset.table \
"gs://mybucket/00/*.orc","gs://mybucket/01/*.orc"
```

當 BigQuery 偵測到結構定義時，部分 ORC 資料類型會轉換為 BigQuery 資料類型，確保與 GoogleSQL 語法相容。在偵測到的結構定義中，所有欄位均為 [`NULLABLE`](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#modes)。詳情請參閱 [ORC 轉換](#orc_conversions)一節。

載入具有不同結構定義的多個 ORC 檔案時，多個結構定義中所指定的相同欄位 (具有相同名稱與相同巢狀層級) 必須對應至各個結構定義中相同的已轉換 BigQuery 資料類型。

如要提供資料表結構定義來建立外部資料表，請在 BigQuery API 中設定 `referenceFileSchemaUri` 屬性，或在 bq 指令列工具中設定   
`--reference_file_schema_uri` 參數，指向參照檔案的網址。

例如 `--reference_file_schema_uri="gs://mybucket/schema.orc"`。

## ORC 壓縮

BigQuery 支援下列 ORC 檔案內容的壓縮轉碼器：

* `Zlib`
* `Snappy`
* `LZO`
* `LZ4`
* `ZSTD`

上傳至 BigQuery 後，ORC 檔案中的資料不會保持壓縮狀態。系統會根據[資料集儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)，以邏輯位元組或實際位元組回報資料儲存空間。如要取得儲存空間用量資訊，請查詢 [`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)。

## 將 ORC 資料載入至新的資料表

您可以透過以下方式將 ORC 資料載入至新的資料表：

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具的 `bq load` 指令
* 呼叫 `jobs.insert` API 方法並設定 `load` 工作
* 使用用戶端程式庫

如要將 ORC 資料從 Google Cloud Storage 載入至新的 BigQuery 資料表：

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
   2. 在「File format」(檔案格式) 部分選取「ORC」。
2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。結構定義自述於 ORC 檔案中。
4. 選用：指定「分區與叢集設定」。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。
5. 按一下「進階選項」，然後執行下列操作：
   * 讓「Write preference」(寫入偏好設定) 的 [Write if empty] (空白時寫入) 選項維持在已選取狀態。這個選項能建立新的資料表，並將您的資料載入其中。
   * 如要忽略不在資料表結構定義中的資料列值，請選取「Unknown values」(不明的值)。
   * 針對 **Encryption**，請按一下 **Customer-managed key**，以使用 [Cloud Key Management Service key](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果您保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
6. 點選「建立資料表」。

**注意：** 使用Google Cloud 控制台 將資料載入空白資料表時，您無法新增標籤、說明、資料表到期時間或分區到期時間。  
  
資料表建立完成之後，您就能更新資料表的到期時間、說明和標籤，但您無法在使用 Google Cloud 控制台建立資料表之後，新增分區到期時間。詳情請參閱[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)。

### SQL

使用 [`LOAD DATA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)。以下範例會將 ORC 檔案載入至新資料表 `mytable`：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   LOAD DATA OVERWRITE mydataset.mytable
   FROM FILES (
     format = 'ORC',
     uris = ['gs://bucket/path/file.orc']);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 `bq load` 指令將 ORC 指定為 `source_format`，並加入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。
您可以加入單一 URI、以逗號分隔的 URI 清單，或包含[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)的 URI。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

其他選用標記包括：

* `--time_partitioning_type`：針對資料表啟用時間分區並設定分區類型。可能的值為 `HOUR`、`DAY`、`MONTH` 和 `YEAR`。如果您在 `DATE`、`DATETIME` 或 `TIMESTAMP` 資料欄建立分區資料表，則不一定要使用這個旗標。時間分區的預設分區類型為 `DAY`。您無法變更現有資料表的分區規格。
* `--time_partitioning_expiration`：這是一個整數，用來指定系統應在何時刪除時間分區 (以秒為單位)。到期時間為分區的世界標準時間日期加上整數值。
* `--time_partitioning_field`：用於建立分區資料表的 `DATE` 或 `TIMESTAMP` 資料欄。如果啟用時間分區時沒有這個值，系統就會建立擷取時間分區資料表。
* `--require_partition_filter`：這個選項啟用後，系統會要求使用者加入 `WHERE` 子句，以指定要查詢的分區。使用分區篩選器可以降低成本並提升效能。詳情請參閱[在查詢中要求使用分區篩選器](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)。
* `--clustering_fields`：以半形逗號分隔的資料欄名稱清單 (最多四個名稱)，可用來建立[分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)。
* `--destination_kms_key`：用來加密資料表資料的 Cloud KMS 金鑰。

  如要進一步瞭解分區資料表，請參閱：

  + [建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)

  如要進一步瞭解叢集資料表，請參閱：

  + [建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)

  如要進一步瞭解資料表加密作業，請參閱：

  + [使用 Cloud KMS 金鑰保護資料](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)

如要將 ORC 資料載入 BigQuery，請輸入下列指令：

```
bq --location=location load \
--source_format=format \
dataset.table \
path_to_source
```

其中：

* location 是您的位置。`--location` 是選用旗標。舉例來說，如果您在東京區域使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* format為 `ORC`。
* dataset 是現有資料集。
* table 是您正在載入資料的資料表名稱。
* path\_to\_source 是完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或是以逗號分隔的 URI 清單。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。

範例：

下列指令會將資料從 `gs://mybucket/mydata.orc` 載入到 `mydataset` 中名為 `mytable` 的資料表。

```
    bq load \
    --source_format=ORC \
    mydataset.mytable \
    gs://mybucket/mydata.orc
```

下列指令會將 `gs://mybucket/mydata.orc` 中的資料載入至 `mydataset` 中名為 `mytable` 的新擷取時間分區資料表。

```
    bq load \
    --source_format=ORC \
    --time_partitioning_type=DAY \
    mydataset.mytable \
    gs://mybucket/mydata.orc
```

下列指令會將資料從 `gs://mybucket/mydata.orc` 載入到 `mydataset` 中名為 `mytable` 的分區資料表。資料表會依 `mytimestamp` 資料欄進行分區。

```
    bq load \
    --source_format=ORC \
    --time_partitioning_field mytimestamp \
    mydataset.mytable \
    gs://mybucket/mydata.orc
```

下列指令會將 `gs://mybucket/` 中多個檔案的資料載入到 `mydataset` 中名為 `mytable` 的資料表。指令中的 Cloud Storage URI 使用萬用字元。

```
    bq load \
    --source_format=ORC \
    mydataset.mytable \
    gs://mybucket/mydata*.orc
```

下列指令會將 `gs://mybucket/` 中多個檔案的資料載入到 `mydataset` 中名為 `mytable` 的資料表。指令包含以逗號分隔且帶有萬用字元的 Cloud Storage URI 清單。

```
    bq load --autodetect \
    --source_format=ORC \
    mydataset.mytable \
    "gs://mybucket/00/*.orc","gs://mybucket/01/*.orc"
```

### API

1. 建立指向 Cloud Storage 中來源資料的 `load` 工作。
2. (選用) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。
3. `source URIs` 屬性必須是完整的，且必須符合下列格式：`gs://bucket/object`。每個 URI 可包含一個「\*」[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。
4. 將 `sourceFormat` 屬性設為 `ORC`，以指定 ORC 資料格式。
5. 如要檢查工作狀態，請呼叫 [`jobs.get(job_id*)`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/get?hl=zh-tw)，其中 job\_id 是初始要求傳回的工作 ID。

   * 如果是 `status.state = DONE`，代表工作已順利完成。
   * 如果出現 `status.errorResult` 屬性，代表要求執行失敗，且該物件會包含描述問題的相關資訊。如果要求執行失敗，系統就不會建立任何資料表，也不會載入任何資料。
   * 如果未出現 `status.errorResult`，代表工作順利完成，但可能有一些非致命錯誤，例如少數資料列在匯入時發生問題。不嚴重的錯誤都會列在已傳回工作物件的 `status.errors` 屬性中。

**API 附註：**

* 載入工作不可部分完成，且資料狀態具一致性。如果載入工作失敗，所有資料都無法使用；如果載入工作成功，則所有資料都可以使用。
* 最佳做法是產生唯一 ID，並在呼叫 `jobs.insert` 建立載入工作時，將該 ID 當做 `jobReference.jobId` 傳送。這個方法較不受網路故障問題的影響，因為用戶端可使用已知的工作 ID 進行輪詢或重試。
* 對指定的工作 ID 呼叫 `jobs.insert` 是一種冪等作業。也就是說，您可以對同一個工作 ID 重試無數次，最多會有一個作業成功。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Apis.Bigquery.v2.Data;
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryLoadTableGcsOrc
{
    public void LoadTableGcsOrc(
        string projectId = "your-project-id",
        string datasetId = "your_dataset_id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        var gcsURI = "gs://cloud-samples-data/bigquery/us-states/us-states.orc";
        var dataset = client.GetDataset(datasetId);
        TableReference destinationTableRef = dataset.GetTableReference(
            tableId: "us_states");
        // Create job configuration
        var jobOptions = new CreateLoadJobOptions()
        {
            SourceFormat = FileFormat.Orc
        };
        // Create and run job
        var loadJob = client.CreateLoadJob(
            sourceUri: gcsURI,
            destination: destinationTableRef,
            // Pass null as the schema because the schema is inferred when
            // loading Orc data
            schema: null,
            options: jobOptions
        );
        loadJob = loadJob.PollUntilCompleted().ThrowOnAnyError();  // Waits for the job to complete.
        // Display the number of rows uploaded
        BigQueryTable table = client.GetTable(destinationTableRef);
        Console.WriteLine(
            $"Loaded {table.Resource.NumRows} rows to {table.FullyQualifiedId}");
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// importORCTruncate demonstrates loading Apache ORC data from Cloud Storage into a table.
func importORC(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states.orc")
	gcsRef.SourceFormat = bigquery.ORC
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

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.TableId;

// Sample to load ORC data from Cloud Storage into a new BigQuery table
public class LoadOrcFromGCS {

  public static void runLoadOrcFromGCS() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.orc";
    Schema schema =
        Schema.of(
            Field.of("name", StandardSQLTypeName.STRING),
            Field.of("post_abbr", StandardSQLTypeName.STRING));
    loadOrcFromGCS(datasetName, tableName, sourceUri, schema);
  }

  public static void loadOrcFromGCS(
      String datasetName, String tableName, String sourceUri, Schema schema) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      LoadJobConfiguration loadConfig =
          LoadJobConfiguration.newBuilder(tableId, sourceUri, FormatOptions.orc())
              .setSchema(schema)
              .build();

      // Load data from a GCS ORC file into the table
      Job job = bigquery.create(JobInfo.of(loadConfig));
      // Blocks until this load table job completes its execution, either failing or succeeding.
      job = job.waitFor();
      if (job.isDone() && job.getStatus().getError() == null) {
        System.out.println("ORC from GCS successfully added during load append job");
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
 * This sample loads the ORC file at
 * https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.orc
 *
 * TODO(developer): Replace the following lines with the path to your file.
 */
const bucketName = 'cloud-samples-data';
const filename = 'bigquery/us-states/us-states.orc';

async function loadTableGCSORC() {
  // Imports a GCS file into a table with ORC source format.

  /**
   * TODO(developer): Uncomment the following line before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table'

  // Configure the load job. For full list of options, see:
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationLoad
  const metadata = {
    sourceFormat: 'ORC',
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
$gcsUri = 'gs://cloud-samples-data/bigquery/us-states/us-states.orc';
$loadConfig = $table->loadFromStorage($gcsUri)->sourceFormat('ORC');
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

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name

job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.ORC)
uri = "gs://cloud-samples-data/bigquery/us-states/us-states.orc"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def load_table_gcs_orc dataset_id = "your_dataset_id"
  bigquery = Google::Cloud::Bigquery.new
  dataset  = bigquery.dataset dataset_id
  gcs_uri  = "gs://cloud-samples-data/bigquery/us-states/us-states.orc"
  table_id = "us_states"

  load_job = dataset.load_job table_id, gcs_uri, format: "orc"
  puts "Starting job #{load_job.job_id}"

  load_job.wait_until_done! # Waits for table load to complete.
  puts "Job finished."

  table = dataset.table table_id
  puts "Loaded #{table.rows_count} rows to table #{table.id}"
end
```

## 使用 ORC 資料附加到資料表或覆寫資料表

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

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具的 `bq load` 指令
* 呼叫 `jobs.insert` API 方法並設定 `load` 工作
* 使用用戶端程式庫

**注意：**本頁面未說明如何對分區資料表進行附加或覆寫。如要瞭解如何附加和覆寫分區資料表，請參閱[對分區資料表中的資料執行附加或覆寫操作](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#append-overwrite)一節。

使用 ORC 資料附加或覆寫資料表的方式如下：

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
   2. 在「File format」(檔案格式) 部分選取「ORC」。
**注意：**您可以在附加或覆寫資料表時修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱「[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)」一文。
2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。結構定義自述於 ORC 檔案中。
**注意：**您可以在附加或覆寫資料表時修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。4. 選用：指定「分區與叢集設定」。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。您無法藉由附加或覆寫的方式，將資料表轉換為分區資料表或分群資料表。 Google Cloud 控制台不支援在載入工作中附加資料到分區或叢集資料表，也不支援覆寫分區或叢集資料表。
5. 按一下「進階選項」，然後執行下列操作：
   * 針對「Write preference」(寫入偏好設定)，請選擇「Append to table」(附加到資料表中) 或「Overwrite table」(覆寫資料表)。
   * 如要忽略不在資料表結構定義中的資料列值，請選取「Unknown values」(不明的值)。
   * 針對 **Encryption**，請按一下 **Customer-managed key**，以使用 [Cloud Key Management Service key](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果您保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
6. 點選「建立資料表」。

### SQL

使用 [`LOAD DATA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)。以下範例會將 ORC 檔案附加至 `mytable` 資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   LOAD DATA INTO mydataset.mytable
   FROM FILES (
     format = 'ORC',
     uris = ['gs://bucket/path/file.orc']);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要覆寫資料表，請輸入 `bq load` 指令並加上 `--replace` 旗標。如要附加資料至資料表，使用 `--noreplace` 旗標。若未指定任何旗標，預設動作為附加資料。提供 `--source_format` 旗標，並將其設為 `ORC`。由於系統會自動從自述來源資料中擷取 ORC 結構定義，所以您不需要提供結構定義。

**注意：**您可以在對資料表進行附加或覆寫作業時修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)一文。

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

其中：

* location 是您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。`--location` 是選用旗標。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)來設定位置的預設值。
* format為 `ORC`。
* dataset 是現有資料集。
* table 是您正在載入資料的資料表名稱。
* path\_to\_source 是完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或是以逗號分隔的 URI 清單。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。

範例：

下列指令會從 `gs://mybucket/mydata.orc` 載入資料，並覆寫 `mydataset` 中名為 `mytable` 的資料表。

```
    bq load \
    --replace \
    --source_format=ORC \
    mydataset.mytable \
    gs://mybucket/mydata.orc
```

下列指令會從 `gs://mybucket/mydata.orc` 載入資料，並將資料附加至 `mydataset` 中名為 `mytable` 的資料表。

```
    bq load \
    --noreplace \
    --source_format=ORC \
    mydataset.mytable \
    gs://mybucket/mydata.orc
```

如要瞭解如何使用 bq 指令列工具附加和覆寫分區資料表，請參閱[對分區資料表中的資料執行附加或覆寫操作](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#append-overwrite)一節。

### API

1. 建立指向 Cloud Storage 中來源資料的 `load` 工作。
2. (選用) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。
3. `source URIs` 屬性必須是完整的，且必須符合下列格式：`gs://bucket/object`。您可以使用逗號分隔清單的形式加入多個 URI。請注意，系統也支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。
4. 藉由將 `configuration.load.sourceFormat` 屬性設為 `ORC`，以指定資料格式。
5. 藉由將 `configuration.load.writeDisposition` 屬性設為 `WRITE_TRUNCATE` 或 `WRITE_APPEND`，以指定寫入偏好設定。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Apis.Bigquery.v2.Data;
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryLoadTableGcsOrcTruncate
{
    public void LoadTableGcsOrcTruncate(
        string projectId = "your-project-id",
        string datasetId = "your_dataset_id",
        string tableId = "your_table_id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        var gcsURI = "gs://cloud-samples-data/bigquery/us-states/us-states.orc";
        var dataset = client.GetDataset(datasetId);
        TableReference destinationTableRef = dataset.GetTableReference(
            tableId: "us_states");
        // Create job configuration
        var jobOptions = new CreateLoadJobOptions()
        {
            SourceFormat = FileFormat.Orc,
            WriteDisposition = WriteDisposition.WriteTruncate
        };
        // Create and run job
        var loadJob = client.CreateLoadJob(
            sourceUri: gcsURI,
            destination: destinationTableRef,
            // Pass null as the schema because the schema is inferred when
            // loading Orc data
            schema: null, options: jobOptions);
        loadJob = loadJob.PollUntilCompleted().ThrowOnAnyError();  // Waits for the job to complete.
        // Display the number of rows uploaded
        BigQueryTable table = client.GetTable(destinationTableRef);
        Console.WriteLine(
            $"Loaded {table.Resource.NumRows} rows to {table.FullyQualifiedId}");
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// importORCTruncate demonstrates loading Apache ORC data from Cloud Storage into a table
// and overwriting/truncating existing data in the table.
func importORCTruncate(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states.orc")
	gcsRef.SourceFormat = bigquery.ORC
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

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.TableId;

// Sample to overwrite the BigQuery table data by loading a ORC file from GCS
public class LoadOrcFromGcsTruncate {

  public static void runLoadOrcFromGcsTruncate() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.orc";
    loadOrcFromGcsTruncate(datasetName, tableName, sourceUri);
  }

  public static void loadOrcFromGcsTruncate(
      String datasetName, String tableName, String sourceUri) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      LoadJobConfiguration loadConfig =
          LoadJobConfiguration.newBuilder(tableId, sourceUri)
              .setFormatOptions(FormatOptions.orc())
              // Set the write disposition to overwrite existing table data
              .setWriteDisposition(JobInfo.WriteDisposition.WRITE_TRUNCATE)
              .build();

      // Load data from a GCS ORC file into the table
      Job job = bigquery.create(JobInfo.of(loadConfig));
      // Blocks until this load table job completes its execution, either failing or succeeding.
      job = job.waitFor();
      if (job.isDone() && job.getStatus().getError() == null) {
        System.out.println("Table is successfully overwritten by ORC file loaded from GCS");
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

// Instantiate the clients
const bigquery = new BigQuery();
const storage = new Storage();

/**
 * This sample loads the CSV file at
 * https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.csv
 *
 * TODO(developer): Replace the following lines with the path to your file.
 */
const bucketName = 'cloud-samples-data';
const filename = 'bigquery/us-states/us-states.orc';

async function loadORCFromGCSTruncate() {
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
    sourceFormat: 'ORC',
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
$gcsUri = 'gs://cloud-samples-data/bigquery/us-states/us-states.orc';
$loadConfig = $table->loadFromStorage($gcsUri)->sourceFormat('ORC')->writeDisposition('WRITE_TRUNCATE');
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

如要取代現有資料表中的資料列，請將 [LoadJobConfig.write\_disposition 屬性](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_write_disposition)設為 [WRITE\_TRUNCATE](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.enums.WriteDisposition?hl=zh-tw#google.cloud.bigquery.enums.WriteDisposition.WRITE_TRUNCATE)。

```
import io

from google.cloud import
```