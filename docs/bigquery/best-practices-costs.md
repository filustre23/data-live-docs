* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 預估及控管費用

這個頁面說明在 BigQuery 中估算及控管費用的最佳做法。

BigQuery 的主要費用是運算 (用於查詢處理) 和儲存空間 (用於儲存在 BigQuery 中的資料)。BigQuery 提供兩種查詢處理計費模式：[以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)和[以容量為準](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)的計費模式。每種模式都有不同的費用控管最佳做法。[儲存在 BigQuery 的資料](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)費用取決於為每個資料集設定的[儲存空間帳單模型](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)。

## 瞭解 BigQuery 的運算定價

BigQuery 的運算價格略有不同，會影響容量規劃和成本控管。

### 計費模式

在 BigQuery 中，隨選運算資源的費用是按照 BigQuery 查詢處理的資料量 (以 TiB 為單位) 計算。

或者，如果使用 BigQuery 的容量運算，系統會根據處理查詢時使用的運算資源 (*[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)*) 收取費用。如要使用這個模型，請設定*[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)*。

預留功能具有下列特色：

* 運算單元會分配到運算單元集區，方便您管理容量，並以適合貴機構的方式隔離工作負載。
* 這些資源必須位於一個管理專案中，且受[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#reservations)規範。

容量定價模式提供多種[*版本*](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)，
所有版本都提供即付即用選項，以運算單元時數為單位收費。Enterprise 和 Enterprise Plus 版本也提供可選用的一年或三年期運算單元承諾，與即付即用費率相比，可節省費用。

您也可以使用即付即用選項設定[自動調度預留項目](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)。詳情請參閱下列文章：

* 如要比較定價模式，請參閱[選擇模式](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#choosing_a_model)。
* 如需定價詳細資料，請參閱[以量計價的運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)和[容量運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。

### 限制每個模型的費用

使用隨選價格模式時，如要限制費用，唯一方法是設定專案層級或使用者層級的每日配額。不過，這些配額會強制設下上限，防止使用者執行超出配額限制的查詢。如要設定配額，請參閱「[建立自訂查詢配額](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#create-custom-cost-controls)」。

使用運算單元預留項目時，您會指定預留項目可用的運算單元數量上限。您也可以購買運算單元承諾使用合約，在承諾使用期間享有折扣價。

您可以將預訂的基準設為 0，並將上限設為符合工作負載需求的設定，完全依需求使用版本。BigQuery 會自動將配額擴充至工作負載所需的配額數量，但絕不會超過您設定的上限。詳情請參閱[使用預留項目進行工作負載管理](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)。

## 控管查詢費用

如要控管個別查詢的費用，建議您先遵循[查詢運算最佳化](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)和[儲存空間最佳化](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)的最佳做法。

以下各節將說明其他最佳做法，協助您進一步控管查詢費用。

### 建立自訂查詢配額

**最佳做法：**使用自訂每日查詢配額，限制每日處理的資料量。

您可以設定[自訂配額](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw)，指定每個專案或使用者每天處理的資料量上限，藉此管理費用。達到配額後，使用者就無法執行查詢。

如要設定自訂配額，您需要[特定角色或權限](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw#required_role)。
如要瞭解可設定的配額，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

詳情請參閱「[為各個定價模式設下費用限制](#restrict-compute-costs)」。

### 執行查詢前先查看預估費用

**最佳做法：**在執行查詢之前，請先檢查並估算需要支付多少費用。

如果採用隨選定價模式，系統會根據查詢讀取的位元組數計費。如要在執行查詢之前估算費用，請使用：

* 在 Google Cloud 控制台[使用查詢驗證工具](#use-query-validator)。
* [對查詢執行模擬測試](#perform-dry-run)。

**注意：** 查詢的預估計費位元組數是上限，可能高於查詢執行後實際計費的位元組數。

#### 使用查詢驗證工具

在 Google Cloud 控制台中輸入查詢時，查詢驗證工具會驗證查詢語法，並估算讀取的位元組數。您可以在 Pricing Calculator 中使用這項估算值來計算查詢費用。

* 如果查詢無效，查詢驗證工具會顯示錯誤訊息。例如：

  `Not found: Table myProject:myDataset.myTable was not found in location US`
* 如果查詢有效，查詢驗證工具會預估處理查詢所需的位元組數。例如：

  `This query will process 623.1 KiB when run.`

#### 執行模擬測試

如要執行模擬測試，請按照下列步驟操作：

### 控制台

1. 前往 BigQuery 頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入查詢。

   如果查詢有效，系統就會自動顯示勾號和查詢處理的資料量。如果查詢無效，則會顯示驚嘆號和錯誤訊息。

### bq

使用 `--dry_run` 旗標輸入如下的查詢。

```
bq query \
--use_legacy_sql=false \
--dry_run \
'SELECT
   COUNTRY,
   AIRPORT,
   IATA
 FROM
   `project_id`.dataset.airports
 LIMIT
   1000'
```

如果查詢有效，這項指令會產生下列回應：

```
Query successfully validated. Assuming the tables are not modified,
running this query will process 10918 bytes of data.
```

**注意：** 如果您的查詢僅處理少量資料，則可能需要將處理的位元組數從 KB 轉換為 MB。MB 是 Pricing Calculator 使用的最小度量單位。

### API

如要使用 API 執行模擬測試，請在 [JobConfiguration](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfiguration) 型別中，將 `dryRun` 設定為 `true`，然後提交查詢工作。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
)

// queryDryRun demonstrates issuing a dry run query to validate query structure and
// provide an estimate of the bytes scanned.
func queryDryRun(w io.Writer, projectID string) error {
	// projectID := "my-project-id"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	q := client.Query(`
	SELECT
		name,
		COUNT(*) as name_count
	FROM ` + "`bigquery-public-data.usa_names.usa_1910_2013`" + `
	WHERE state = 'WA'
	GROUP BY name`)
	q.DryRun = true
	// Location must match that of the dataset(s) referenced in the query.
	q.Location = "US"

	job, err := q.Run(ctx)
	if err != nil {
		return err
	}
	// Dry run is not asynchronous, so get the latest status and statistics.
	status := job.LastStatus()
	if err := status.Err(); err != nil {
		return err
	}
	fmt.Fprintf(w, "This query will process %d bytes\n", status.Statistics.TotalBytesProcessed)
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
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.JobStatistics;
import com.google.cloud.bigquery.QueryJobConfiguration;

// Sample to run dry query on the table
public class QueryDryRun {

  public static void runQueryDryRun() {
    String query =
        "SELECT name, COUNT(*) as name_count "
            + "FROM `bigquery-public-data.usa_names.usa_1910_2013` "
            + "WHERE state = 'WA' "
            + "GROUP BY name";
    queryDryRun(query);
  }

  public static void queryDryRun(String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query).setDryRun(true).setUseQueryCache(false).build();

      Job job = bigquery.create(JobInfo.of(queryConfig));
      JobStatistics.QueryStatistics statistics = job.getStatistics();

      System.out.println(
          "Query dry run performed successfully." + statistics.getTotalBytesProcessed());
    } catch (BigQueryException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function queryDryRun() {
  // Runs a dry query of the U.S. given names dataset for the state of Texas.

  const query = `SELECT name
    FROM \`bigquery-public-data.usa_names.usa_1910_2013\`
    WHERE state = 'TX'
    LIMIT 100`;

  // For all options, see https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
  const options = {
    query: query,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
    dryRun: true,
  };

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(options);

  // Print the status and statistics
  console.log('Status:');
  console.log(job.metadata.status);
  console.log('\nJob Statistics:');
  console.log(job.metadata.statistics);
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/** Uncomment and populate these variables in your code */
// $projectId = 'The Google project ID';
// $query = 'SELECT id, view_count FROM `bigquery-public-data.stackoverflow.posts_questions`';

// Construct a BigQuery client object.
$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);

// Set job configs
$jobConfig = $bigQuery->query($query);
$jobConfig->useQueryCache(false);
$jobConfig->dryRun(true);

// Extract query results
$queryJob = $bigQuery->startJob($jobConfig);
$info = $queryJob->info();

printf('This query will process %s bytes' . PHP_EOL, $info['statistics']['totalBytesProcessed']);
```

### Python

將 [QueryJobConfig.dry\_run](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob_dry_run) 屬性設為 `True`。如果有提供模擬測試的查詢設定，則 [Client.query()](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_query) 一律會傳回已完成的 [QueryJob](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob)。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

# Start the query, passing in the extra configuration.
query_job = client.query(
    (
        "SELECT name, COUNT(*) as name_count "
        "FROM `bigquery-public-data.usa_names.usa_1910_2013` "
        "WHERE state = 'WA' "
        "GROUP BY name"
    ),
    job_config=job_config,
)  # Make an API request.

# A dry run query completes immediately.
print("This query will process {} bytes.".format(query_job.total_bytes_processed))
```

### 估算查詢費用

使用[隨選定價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)時，您可以計算處理的位元組數，估算執行查詢的費用。

#### 以量計價查詢大小計算

如要計算各類查詢處理的位元組數，請參閱下列章節：

* [DML 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#on-demand-query-size-calculation)
* [DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#on-demand-query-size-calculation)
* [叢集資料表](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#block-pruning)

**注意：** 選取的[資料集儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)不會影響隨選查詢費用計算。BigQuery 一律會使用邏輯 (未壓縮) 位元組計算隨選查詢費用。**注意：** 如果您查詢的[外部資料表資料](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)是以 [ORC](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-orc?hl=zh-tw#orc_conversions) 或 [Parquet](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#parquet_conversions) 格式儲存，計費的位元組數僅限於 BigQuery 讀取的資料欄。由於外部資料來源的資料類型是經由查詢轉換為 BigQuery 資料類型，因此系統會根據 BigQuery 資料類型大小計算讀取的位元組數。

### 避免執行查詢來探索資料表資料

**最佳做法：**如果您只是想大致查看或預覽資料表中的資料，請勿使用查詢功能。

如要進行資料實驗或探索資料，可以使用資料表預覽選項免費查看資料，且不會影響配額。

BigQuery 支援下列資料預覽選項：

* 在 Google Cloud 控制台的資料表詳細資料頁面中，按一下「預覽」分頁標籤，即可對資料進行取樣。
* 在 bq 指令列工具中，使用 [`bq head`](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw#browse-table) 指令並指定要預覽的資料列數。
* 在 API 中，使用 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 從一組指定的資料列擷取資料表資料。
* 請避免在非叢集資料表中使用 `LIMIT`。如果是非叢集資料表，`LIMIT` 子句不會降低運算費用。

### 限制每項查詢的計費位元組數

**最佳做法：**使用以量計價的定價模式時，請設定資料量計費上限，以限制查詢費用。

您可以使用計費位元組上限設定，限制針對查詢計費的位元組數。設定資料量計費上限後，系統會在查詢執行前預估查詢讀取的位元組數。如果預估的位元組數超過限制，查詢就會失敗，不會產生費用。

如果是叢集資料表，查詢的計費位元組數預估值是上限，可能高於查詢執行後實際計費的位元組數。因此在某些情況下，即使實際計費位元組不會超過計費位元組上限設定，您在分群資料表上執行的查詢仍可能失敗。

如果查詢因計費位元組上限設定而失敗，會傳回類似以下的錯誤：

`Error: Query exceeded limit for bytes billed: 1000000. 10485760 or higher
required.`

設定資料量計費上限：

### 控制台

1. 在「查詢編輯器」中，依序點選「更多」**>「查詢設定」>「進階選項」**。
2. 在「計費位元組上限」欄位中輸入整數。
3. 按一下 [儲存]。

### bq

請使用 `bq query` 指令，並加上 `--maximum_bytes_billed` 旗標。

```
  bq query --maximum_bytes_billed=1000000 \
  --use_legacy_sql=false \
  'SELECT
     word
   FROM
     `bigquery-public-data`.samples.shakespeare'
```

### API

在 [`JobConfigurationQuery`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationquery) 或 [`QueryRequest`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw#queryrequest) 中設定 `maximumBytesBilled` 屬性。

### 避免在非叢集資料表中使用 `LIMIT`

**最佳做法：**對於非叢集資料表，請勿使用 `LIMIT` 子句做為費用控管的方法。

對於非叢集資料表，將 `LIMIT` 子句套用至查詢不會影響讀取的資料量。即使查詢只傳回子集，系統仍會收取您如查詢所指示，在完整資料表中讀取所有位元組的費用。使用分群資料表時，`LIMIT` 子句可以減少掃描的位元組數，因為掃描作業會在掃描足夠的區塊以取得結果後停止。系統只會根據掃描的位元組數計費。

### 分階段具體化查詢結果

**最佳做法：**如有可能，請分階段具體化查詢結果。

如果您要建立大型、多階段的查詢，每次執行查詢時，BigQuery 都會讀取查詢要求的所有資料。系統會針對您每次執行查詢時讀取的所有資料收取相關費用。

因此，請改為分階段查詢，每個階段都會將查詢結果寫入[目的地資料表](https://docs.cloud.google.com/bigquery/querying-data?hl=zh-tw#permanent-table)來具體化查詢結果。查詢較小的目的地資料表會減少讀取的資料量並降低費用。儲存具體化結果的費用比處理大量資料的費用低很多。

### 使用 Rapid Cache 透過外部資料表查詢 Cloud Storage

**最佳做法：**使用外部資料表查詢 Cloud Storage 資料時，請考慮啟用 Rapid Cache。

Rapid Cache 為 Cloud Storage 值區提供以 SSD 為基礎的可用區讀取快取，查詢外部資料表時，可望提升查詢效能並降低查詢費用。詳情請參閱「[最佳化 Cloud Storage 外部資料表查詢](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#cloud-storage-query-optimization)」。

## 控管工作負載費用

本節說明控管工作負載費用的最佳做法。**工作負載是一組相關查詢**。舉例來說，工作負載可以是每日執行的資料轉換管道、一組由一群業務分析師執行的資訊主頁，或一組由一群資料科學家執行的臨時查詢。

### 使用 Google Cloud 價格計算工具

**最佳做法：**使用 [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw)，根據預測用量估算 BigQuery 的每月總費用。然後將這項預估值與實際費用進行比較，找出可最佳化的部分。

### 隨選

如要使用隨選計費模式，請按照下列步驟，在[Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw) 中估算費用：

1. 開啟[Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw)。
2. 按一下「新增至估算值」。
3. 選取 BigQuery。
4. 選取「隨選」做為**服務類型**。
5. 選擇要執行查詢的位置。
6. 針對「Amount of data queried」(查詢的資料量)，輸入來自模擬測試或查詢驗證工具的估算的讀取位元組數。
7. 輸入「動態儲存」、「長期儲存」、「串流資料插入」和「串流讀取」的預估儲存空間用量。
   您只需要根據[資料集儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)，估算實體儲存空間或邏輯儲存空間。
8. 預估費用會顯示在「費用詳細資料」面板中。如要進一步瞭解預估費用，請按一下「開啟詳細檢視畫面」。你也可以下載及分享費用估算結果。

詳情請參閱[以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)一文。

### 版本

如要使用[Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw)，估算搭配[BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)使用容量計費模式的費用，請按照下列步驟操作：

1. 開啟[Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw)。
2. 按一下「新增至估算值」。
3. 選取 BigQuery。
4. 在「服務類型」中選取「版本」。
5. 選擇使用名額的位置。
6. 選擇所需「版本」。
7. 選擇「運算單元數量上限」、「基準運算單元數量」、選用的「承諾」，以及「自動調度資源的預估使用率」。
8. 選擇資料的儲存位置。
9. 輸入「動態儲存」、「長期儲存」、「串流資料插入」和「串流讀取」的預估儲存空間用量。
   您只需要根據[資料集儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)，估算實體儲存空間或邏輯儲存空間。
10. 預估費用會顯示在「費用詳細資料」面板中。如要進一步瞭解預估費用，請按一下「開啟詳細檢視畫面」。你也可以下載及分享費用估算結果。

詳情請參閱「[以容量為準的定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)」。

### 使用預留項目和承諾

**最佳做法：**使用 BigQuery 預留項目和承諾方案控管費用。

詳情請參閱「[為各個定價模式設下費用限制](#restrict-compute-costs)」。

### 使用預估值計算工具

**最佳做法：**使用運算單元估算器，估算工作負載所需的運算單元數量。

[BigQuery 運算單元估算工具](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)可根據歷來成效指標管理運算單元容量。

此外，如果客戶使用隨選計費模式，在改用以容量為準的計費模式時，可以查看承諾使用和自動調度資源預留項目的規模建議，確保效能與先前相近。

### 取消不必要的長時間執行工作

如要釋出容量，請檢查長時間執行的工作，確認是否應繼續執行。如果沒有，請[取消](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#cancel_jobs)。

### 使用資訊主頁查看費用

**最佳做法：**建立資訊主頁來分析 Cloud Billing 資料，以便監控及調整 BigQuery 用量。

您可以將[帳單資料匯出](https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=zh-tw)至 BigQuery，並在 Data Studio 等工具中以視覺化方式呈現。 如需有關建立計費資訊主頁的教學課程，請參閱「[使用 BigQuery 與數據分析視覺化計費](https://medium.com/google-cloud/visualize-gcp-billing-using-bigquery-and-data-studio-d3e695f90c08)」一文。 Google Cloud

### 使用帳單預算和快訊

**最佳做法：**使用 [Cloud Billing 預算](https://docs.cloud.google.com/billing/docs/how-to/budgets?hl=zh-tw)集中監控 BigQuery 費用。

Cloud Billing 預算可讓您追蹤實際費用與預估費用的差異。設定預算金額後，您可以設定預算快訊門檻規則，用來觸發電子郵件通知。預算快訊電子郵件可協助您根據預算，掌握 BigQuery 支出追蹤情形。

## 控管儲存空間費用

請按照這些最佳做法，盡可能提高 BigQuery 儲存空間的成本效益。您也可以[將儲存空間調整至最佳狀態，藉此提高查詢效能](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)。

### 使用長期儲存空間

**最佳做法：**使用[長期儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)，降低舊資料的費用。

將資料載入 BigQuery 儲存空間後，將適用 BigQuery 的[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。對於較舊的資料，您可以自動享有 BigQuery 長期儲存空間定價。

如果資料表連續 90 天未經修改，系統會自動將其儲存價格調降 50%。如果您有分區資料表，系統會將每個分區視為獨立的單位，判斷是否適用長期儲存價格，並遵守與非分區資料表相同的規則。

請注意，資料表和資料表分區一旦進入長期儲存空間，對資料、中繼資料或分區的任何修改，都可能導致這些資源移回 BigQuery 作用中儲存空間。以下列舉幾個可能導致這項異動的動作：

* 插入、更新、截斷、合併或刪除會變更資料表資料的陳述式
* 將資料載入、串流或附加至資料表
* 變更資料表結構定義的 `ALTER` 陳述式
* 新增或修改資料表屬性，例如說明、標籤或到期時間
* 修改資料表中繼資料

### 設定儲存空間計費模式

**最佳做法：**根據使用模式調整儲存空間計費模式。

BigQuery 支援使用邏輯 (未壓縮) 或實體 (已壓縮) 位元組，或兩者組合來計算儲存空間費用。為每個資料集設定的[儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)會決定儲存空間價格，但不會影響查詢效能。

您可以透過 `INFORMATION_SCHEMA` 檢視畫面，根據[用量模式](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw#forecast_storage_billing)判斷最適合的儲存空間計費模式。

### 避免覆寫資料表

**最佳做法：**使用實體儲存空間計費模式時，請避免重複覆寫資料表。

覆寫資料表時 (例如在[批次載入工作](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#appending_to_or_overwriting_a_table)中使用 `--replace` 參數，或使用 [`TRUNCATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#truncate_table_statement) SQL 陳述式)，系統會在時空旅行和安全防護時間範圍內保留取代的資料。如果經常覆寫資料表，就會產生額外的儲存費用。

您可以改為在載入工作中，使用 `WRITE_APPEND` 參數、`MERGE` SQL 陳述式或 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)，將資料逐步載入資料表。

### 縮短時間回溯期

**最佳做法：**您可以根據需求縮短時間回溯視窗。

如果將[時間回溯](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)期從預設的七天縮短，系統就會減少保留從資料表刪除或變更的資料。只有在使用實體 (壓縮) [儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)時，系統才會收取時空旅行儲存空間費用。

時間回溯期是在資料集層級設定。您也可以使用[設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)，為新資料集設定預設時間回溯期。

### 為目的地資料表設定到期時間

**最佳做法：**如果您將大型查詢結果寫入目的地資料表，請使用預設資料表到期時間，等到您不再需要這些資料時，系統便會依照設定的時間來刪除資料。

在 BigQuery 儲存空間中保留大型結果集會產生費用。如果您不需要結果的擁有存取權，請使用[預設資料表到期時間](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#table-expiration)為您自動刪除資料。

### 將資料封存至 Cloud Storage

**最佳做法：**考慮將資料封存至 Cloud Storage。

您可以根據業務需求，將資料從 BigQuery 移至 Cloud Storage 進行封存。最佳做法是先考量[長期儲存價格](#store-data-bigquery)和[實體儲存空間計費模式](#storage-billing-model)，再[從 BigQuery 匯出資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)。

## 排解 BigQuery 費用差異和意外費用

請按照下列步驟排解 BigQuery 費用超出預期或費用差異的問題：

1. 查看 Cloud Billing 帳單報表時，如要瞭解 BigQuery 的費用來源，建議先依 SKU 分組費用，方便觀察對應 BigQuery 服務的使用量和費用。
2. 接著，請參閱 [SKU 說明文件頁面](https://cloud.google.com/skus?hl=zh-tw)或 Cloud Billing 使用者介面的 `Pricing`頁面，瞭解對應 SKU 的定價，判斷是哪項功能，例如 BigQuery Storage Read API、長期儲存空間、以量計價、標準版。
3. 找出對應的 SKU 後，請使用 `INFORMATION_SCHEMA` 檢視畫面找出與這些費用相關的特定資源，例如：

   * 如果系統向您收取隨選分析費用，請查看[`INFORMATION_SCHEMA.JOBS`檢視範例](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#examples)，找出導致費用的工作和啟動這些工作的使用者。
   * 如果系統向您收取預留項目或承諾使用合約 SKU 的費用，請查看對應的 [`INFORMATION_SCHEMA.RESERVATIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw) 和 [`INFORMATION_SCHEMA.CAPACITY_COMMITMENTS`](https://docs.cloud.google.com/bigquery/docs/information-schema-capacity-commitments?hl=zh-tw#example) 檢視畫面，找出需要付費的預留項目和承諾使用合約。
   * 如果費用來自儲存空間 SKU，請查看[`INFORMATION_SCHEMA.TABLE_STORAGE`檢視範例](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw#example_2)，瞭解哪些資料集和資料表會產生較多費用。

排解問題時的重要注意事項：

* 請注意，Cloud Billing 帳單報表中的「每日」時間範圍是以美國和加拿大太平洋時間 (UTC-8) 午夜為準，且會隨美國日光節約時間進行調整，因此請調整計算和資料匯總作業，以符合相同的時間範圍。
* 將 Cloud Billing 使用者介面與[匯出至 BigQuery 的 Cloud Billing 資料](https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=zh-tw)進行比較時，請務必根據 `usage_start_time` 和 `usage_end_time` 進行彙整，而非 `export_time`。
* 如果帳單帳戶連結多個專案，且您想查看特定專案的費用，請依專案篩選。
* 進行調查時，請務必選取正確的區域。

### 專案掃描的免費查詢位元組數超出配額

在免費用量方案中執行查詢時，如果帳戶達到每月查詢上限，BigQuery 就會傳回這個錯誤。如要進一步瞭解查詢定價，請參閱[免費用量層級](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-usage-tier)。

**錯誤訊息**

```
Your project exceeded quota for free query bytes scanned
```

#### 解析度

如要繼續使用 BigQuery，請[將帳戶升級為 Cloud Billing 付費帳戶](https://docs.cloud.google.com/free/docs/gcp-free-tier?hl=zh-tw#how-to-upgrade)。

### 與查詢、預訂和承諾相關的預期外費用

如要排解與工作執行相關的意外費用，請根據這些費用的來源採取行動：

* 如果隨選分析費用增加，可能是因為啟動的工作數量增加，或是工作需要處理的資料量有所變更。使用 [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 檢視畫面調查這個問題。
* 如果承諾運算單元的費用增加，請查詢 [`INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES`](https://docs.cloud.google.com/bigquery/docs/information-schema-capacity-commitment-changes?hl=zh-tw)，確認是否購買或修改了新的承諾。
* 如要瞭解因預留項目用量而增加的費用，請查看 [`INFORMATION_SCHEMA.RESERVATION_CHANGES`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservation-changes?hl=zh-tw) 中記錄的預留項目異動。如要比對自動調度資源保留項目用量與帳單資料，請參閱[自動調度資源範例](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw#monitor_autoscaling_with_information_schema)。

#### 帳單上的運算單元小時數大於 INFORMATION\_SCHEMA.JOBS 檢視畫面計算出的運算單元小時數

使用自動調度資源預留項目時，系統會根據調度的運算單元數量計算費用，而非根據使用的運算單元數量。BigQuery 會以 50 個運算單元為倍數自動調整規模，因此即使實際用量少於自動調整的數量，系統仍會以最接近的倍數計費。
自動調度器縮減資源前，最短等待時間為 1 分鐘，因此即使查詢使用配額的時間少於 1 分鐘 (例如 1 分鐘內只用了 10 秒)，系統仍會收取至少 1 分鐘的費用。如要正確估算自動調度資源預留的費用，請參閱「[自動調度資源預留配額](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw#monitor_autoscaling_with_information_schema)」頁面。如要進一步瞭解如何有效使用自動調度資源功能，請參閱[自動調度資源最佳做法](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw#autoscaling_best_practices)。

非自動調度預留項目也會出現類似情況，系統會根據佈建的運算單元數量計算費用，而非使用的運算單元數量。如要估算非自動調整規模預訂的費用，可以直接查詢 [`RESERVATIONS_TIMELINE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-reservation-timeline?hl=zh-tw#examples)。

#### 透過 INFORMATION\_SCHEMA.JOBS 計算，以量計價查詢專案的計費位元組總數，但實際帳單金額較低

實際帳單費用低於計算出的處理位元組數，可能有多種原因：

* 每個專案每月可免費查詢 1 TB 的資料，不需額外付費。
* `SCRIPT` 類型的工作未從計算中排除，可能導致部分值重複計算。
* 套用至 Cloud Billing 帳戶的各種節省金額，例如議定折扣、促銷抵免額等。 請查看 [Cloud Billing 帳單報表](https://docs.cloud.google.com/billing/docs/how-to/cost-breakdown?hl=zh-tw#credits)的「節省」部分。免費方案的每月 1 TB 查詢量也包含在內。

#### 透過 INFORMATION\_SCHEMA.JOBS 計算的處理位元組數，大於以隨選查詢執行的專案帳單

如果帳單金額大於您查詢 `INFORMATION_SCHEMA.JOBS` 檢視畫面後計算出的值，可能是因為下列情況：

* 查詢資料列層級安全性資料表

  + 查詢採用資料列層級安全防護機制的資料表時，`INFORMATION_SCHEMA.JOBS` 檢視畫面不會產生 `total_bytes_billed` 的值，因此使用 `INFORMATION_SCHEMA.JOBS` 檢視畫面中的 `total_bytes_billed` 計算的帳單金額會低於實際帳單金額。如要進一步瞭解為何無法查看這項資訊，請參閱「[資料列層級安全防護最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw#limit-side-channel-attacks)」頁面。
* 在 BigQuery 中執行 ML 作業

  + BigQuery ML 以量計價的查詢會根據建立的模型類型計費。部分模型作業的收費費率高於非機器學習查詢。因此，如果只是將專案的所有 `total_billed_bytes` 加總，並使用每 TB 的標準隨選價格費率，這不會是正確的價格匯總結果，您需要考量每 TB 的價格差異。
* 價格金額有誤

  + 確認計算時使用的每 TB 價格值正確無誤，並務必選擇正確的區域，因為價格會因地點而異。請參閱[定價說明文件](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#bigquery-pricing)。

一般建議是按照[公開說明文件](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#compare_on-demand_job_usage_to_billing_data)中建議的方式，計算帳單的隨選工作用量。

#### 即使 API 已停用，且未使用預留容量或約定，仍需支付 BigQuery Reservations API 使用費

檢查 SKU，進一步瞭解哪些服務會產生費用。如果帳單上的 SKU 為 `BigQuery Governance SKU`，表示這筆費用來自 Knowledge Catalog。
部分 Knowledge Catalog 功能會使用 BigQuery 觸發工作執行作業。這些費用現在會透過對應的 BigQuery Reservations API SKU 處理。 詳情請參閱 [Knowledge Catalog 定價](https://cloud.google.com/dataplex/pricing?e=48754805&hl=zh-tw#dataplex-universal-catalog-pricing)說明文件。

#### 專案已指派給預留項目，但仍看到 BigQuery 分析以量計價費用

請詳閱「[排解預訂問題](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#troubleshoot_issues_with_reservations)」一節，找出 `Analysis` 費用的可能來源。

#### BigQuery Standard 版的隨用隨付運算單元產生預期外的費用

在 Cloud Billing 報表中，套用標籤為 `goog-bq-feature-type` 且值為 `BQ_STUDIO_NOTEBOOK` 的篩選器。您看到的用量會以「BigQuery Standard 版」的隨用隨付運算單元計算。這是使用 [BigQuery Studio 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw#monitor_slot_usage)的費用。進一步瞭解 [BigQuery Studio 筆記本定價](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#notebook-runtime-pricing)。

#### BigQuery Enterprise 版的隨用隨付運算單元產生預期外的費用

在 Cloud Billing 報表中，套用標籤為 `goog-bq-feature-type` 且值為 `SPARK_PROCEDURE` 的篩選器。您看到的用量會以「BigQuery Enterprise 版」的隨用隨付運算單元計費。這是使用 [BigQuery Apache Spark 程序](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw#pricing)的費用，無論專案使用的運算模型為何，都會以這種方式計費。

#### 停用 Reservation API 後，仍產生 BigQuery Reservations API 費用

停用 BigQuery 不會停止收取使用承諾費用。如要停止收取使用承諾費用，請刪除使用承諾。將續約方案設為 `NONE`，承諾使用合約到期時就會自動刪除。

#### 查詢非常小的資料表時，隨選查詢的費用會不成比例地偏高

無論資料表實際大小為何，BigQuery 查詢的「每個參照資料表處理的資料量」最低計費額度為 10 MiB。同樣地，每項查詢「處理的資料量」最低收費額度為 10 MiB。查詢小型資料表時，即使資料表大小只有 KB，每項查詢也會產生至少 10 MiB 的費用。這可能會導致費用遠高於隨選計費預估值，且隨選運算價格特別昂貴。

### 非預期的儲存空間費用

可能導致儲存空間費用增加的情況：

* 資料表儲存的資料量增加 - 使用 [`INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-usage?hl=zh-tw) 檢視畫面監控資料表位元組的變化
* 變更[資料集計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)
* 增加實體帳單模型資料集的[時間回溯期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)
* 修改含有[長期儲存空間](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#storage-pricing)資料的表格，導致表格變成[近期內容儲存空間](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#storage-pricing)

#### 刪除資料表或資料集後，BigQuery 儲存空間費用增加

[BigQuery 時間旅行功能](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)會保留已刪除的資料，保留時間為設定的時間旅行視窗，外加 7 天的容錯復原時間。在保留期限內，實體儲存空間計費模式資料集中的已刪除資料仍會計入有效實體儲存空間費用，即使資料表不再顯示於 `INFORMATION_SCHEMA.TABLE_STORAGE` 或控制台也是如此。如果資料表資料位於長期儲存空間，刪除作業會將資料移至有效實體儲存空間。這會導致相應費用增加，因為根據 [BigQuery 儲存空間定價頁面](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#storage-pricing)，系統對使用中的實際位元組收取的費用，大約是長期實際位元組的 2 倍。建議您將時移視窗縮短為 2 天，盡量減少實體儲存空間計費模式資料集因刪除資料而產生的費用。

#### 無需修改資料，即可降低儲存空間費用

在 BigQuery 中，使用者需要支付動態和長期儲存空間的費用。動態儲存費用包含連續 90 天未經修改的任何資料表或資料表分區，而長期儲存費用則包含連續 90 天未經修改的資料表和分區。資料移轉至長期儲存空間後，整體儲存空間費用會降低，因為長期儲存空間的費用比活躍儲存空間便宜約 50%。如需更多詳細資料，請參閱[儲存空間定價](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#storage-pricing)。

#### 儲存空間費用增加，但資料量並未顯著增加

如果對資料表資料、中繼資料或分區執行特定動作，導致長期儲存空間中的資料移至 BigQuery 作用中儲存空間，儲存空間費用可能會增加。詳情請參閱「[使用長期儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#store-data-bigquery)」。

#### INFORMATION\_SCHEMA 儲存空間計算結果與帳單不符

* 請使用 [`INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-usage?hl=zh-tw)，而非 `INFORMATION_SCHEMA.TABLE_STORAGE` - `TABLE_STORAGE_USAGE_TIMELINE`，因為前者提供的資料更準確且更精細，可正確計算儲存空間費用
* 在 `INFORMATION_SCHEMA` 檢視畫面中執行的查詢不會納入稅金、調整項和捨入錯誤，因此比較資料時請將這些因素納入考量。如要進一步瞭解 Cloud Billing 報表，請參閱[這個頁面](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw)。
* `INFORMATION_SCHEMA` 檢視畫面中顯示的資料以世界標準時間為準，而帳單報表資料則以美國和加拿大太平洋時間 (UTC-8) 為準。

## 後續步驟

* 瞭解 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。
* 瞭解如何[最佳化查詢](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)。
* 瞭解如何[最佳化儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)。
* 如要瞭解帳單、快訊和資料視覺化，請參閱下列主題：

  + [建立、編輯或刪除預算和預算快訊](https://docs.cloud.google.com/billing/docs/how-to/budgets?hl=zh-tw)
  + [將 Cloud Billing 資料匯出至 BigQuery](https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=zh-tw)
  + [透過數據分析以圖表呈現費用](https://docs.cloud.google.com/billing/docs/how-to/visualize-data?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]