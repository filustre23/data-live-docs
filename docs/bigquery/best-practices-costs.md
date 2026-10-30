Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 預估及控管費用

本頁面說明在 BigQuery 估算及控管成本的最佳做法。

BigQuery 的主要費用包括運算 (用於查詢處理) 和儲存 (用於儲存在 BigQuery 中的資料)。BigQuery 提供兩種查詢處理計價模式：[隨選](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)和[以運算資源計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。每種模式都有不同的成本控管最佳做法。如果是[儲存在 BigQuery 的資料](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)，費用取決於為各資料集設定的[儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)。

## 瞭解 BigQuery 的運算定價

BigQuery 的運算定價有些微差異，會影響容量規劃和費用控管。

### 計費模式

如果是 BigQuery 的隨選運算，則會按照 TiB 數收取 BigQuery 查詢費用。

或者，如果是 BigQuery 的運算資源，則會依據用於處理查詢的運算資源 (*[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)*) 收費。如要使用這個模式，請設定運算單元的*[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)*。

預留項目具有下列功能：

* 運算單元會分配到運算單元集區，讓您以適合貴組織的方式管理容量及隔離工作負載。
* 這些資源必須位於一個管理專案中，且受[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#reservations)規範。

運算資源定價模式提供多種[*版本*](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)，所有版本都提供即付即用選項，並以運算單元時數計費。Enterprise 和 Enterprise Plus 版本也提供一或三年期的運算單元承諾使用合約，可節省即付即用費率。

您也可以使用即付即用選項設定[自動調度資源預留項目](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#slot-autoscaling)。詳情請參閱下列資源：

* 如要比較定價模式，請參閱「[選擇模式](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#choosing_a_model)」。
* 如要瞭解定價詳情，請參閱「[隨選運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)」和「[容量運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)」。

### 限制各模型的費用

使用隨選計價模式時，限制費用的唯一方法是設定專案層級或使用者層級的每日配額。不過，這些配額會強制執行硬性上限，防止使用者執行超出配額限制的查詢。如要設定配額，請參閱「[建立自訂查詢配額](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#create-custom-cost-controls)」。

使用運算單元預留項目的運算資源定價模式時，您必須指定預留項目可用的運算單元數量上限。您也可以購買運算單元承諾使用合約，在承諾期享有折扣。

只要將預留項目的基準設為 0，並將上限設為符合工作負載需求的設定，即可完全隨需使用版本。BigQuery 會自動擴充至工作負載所需的運算單元數量，但不會超過您設定的上限。詳情請參閱「[使用預留項目管理工作負載](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)」。

## 控管查詢費用

如要控管個別查詢的費用，建議您先按照最佳做法[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)和[最佳化儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)。

以下各節概述其他最佳做法，可進一步控管查詢費用。

### 建立自訂查詢配額

**最佳做法：**使用自訂每日查詢配額，限制每日處理的資料量。

您可以設定[自訂配額](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw)，指定每項專案或每位使用者每天處理的資料量上限，藉此管理費用。達到配額後，使用者就無法執行查詢。

如要設定自訂配額，您必須具備[特定角色或權限](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw#required_role)。如要瞭解可設定的配額，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

詳情請參閱「[限制各定價模式的費用](#restrict-compute-costs)」。

### 執行查詢前先查看預估費用

**最佳做法：**在執行查詢之前，請先檢查並估算需要支付多少費用。

使用隨選定價模式時，系統會根據讀取的位元組數，向查詢收取費用。如要在執行查詢前估算費用，請按照下列步驟操作：

* [使用控制台中的查詢驗證工具](#use-query-validator) Google Cloud 。
* [對查詢執行模擬測試](#perform-dry-run)，除非目標資料表已使用資料列層級安全性遮蓋，在這種情況下，模擬測試一律會傳回 0 個位元組，以防止旁路攻擊。

**注意：** 查詢的預估計費位元組數是上限，可能會高於執行查詢後的實際計費位元組數。

#### 使用查詢驗證工具

在 Google Cloud 控制台輸入查詢時，查詢驗證工具會驗證查詢語法，並提供讀取位元組數的預估值。您可以使用這項預估值，在 Pricing Calculator 中計算查詢費用。

* 如果查詢無效，查詢驗證工具會顯示錯誤訊息。例如：

  `Not found: Table myProject:myDataset.myTable was not found in location US`
* 如果查詢有效，查詢驗證工具會提供處理查詢所需的預估位元組數。例如：

  `This query will process 623.1 KiB when run.`

#### 執行模擬測試

如要執行模擬測試，請按照下列步驟操作：

### 控制台

1. 前往 BigQuery 頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入查詢。

   如果查詢有效，系統會自動顯示勾號和查詢將處理的資料量。如果查詢無效，則會顯示驚嘆號和錯誤訊息。

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

如果查詢有效，指令會產生下列回應：

```
Query successfully validated. Assuming the tables are not modified,
running this query will process 10918 bytes of data.
```

**注意：** 如果查詢處理的資料量較小，您可能需要將處理的位元組從 KB 轉換為 MB。MB 是 Pricing Calculator 使用的最小單位。

### API

如要使用 API 執行模擬測試，請提交查詢工作，並在 [JobConfiguration](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfiguration) 類型中將 `dryRun` 設為 `true`。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定操作說明進行操作。詳情請參閱 [BigQuery PHP API 參考文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

視運算定價模式而定，估算查詢費用的方法會有所不同。

#### 隨選查詢費用估算

使用[隨選定價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)時，您可以計算處理的位元組數量，藉此估算執行查詢的費用。

#### 依據運算資源估算查詢費用

使用[依運算資源計價](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)時，無法在執行前準確估算個別查詢的確切費用。運算資源費用是根據預留項目佈建或自動調度的整體運算資源運算單元容量計算，而非特定查詢掃描的資料量。

由於動態執行階段因素，在執行前預估個別查詢費用相當困難，這些因素包括：

* **動態運算單元分配**：分配給查詢的運算單元數量取決於查詢複雜度、執行階段最佳化和資源可用性。
* **並行**：多項查詢會動態共用預留項目中的可用運算單元。
* **自動調度資源行為**：如果啟用[運算單元自動調度資源](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#slot-autoscaling)功能，預留項目會根據匯總工作負載需求 (而非單一查詢執行作業) 向上和向下調度資源。

查詢執行完畢後，您可以檢查查詢執行詳細資料，或查詢 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，查看查詢實際消耗的運算資源 (以運算單元毫秒為單位，`total_slot_ms`)。

#### 依容量歸因成本

成本歸因是指在工作負載執行後，將預留運算成本拆分並歸因至各專案、團隊或查詢。

如要瞭解及分配整體費用，您可以使用 Cloud Billing 資料中的[預留項目費用歸因](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw#reservation_cost_attribution)，將預留項目費用歸因於特定查詢和專案。在 Cloud Billing 資料和報表中，尋找「Analysis Slots Attribution」(分析運算單元歸因) 委刊項，即可追蹤每項專案使用的運算單元時數，不會產生額外費用，也不會影響應付憑據總額。

詳情請參閱「[預留項目費用歸因](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw#reservation_cost_attribution)」。

#### 隨選查詢大小計算

如要計算各類查詢處理的位元組數，請參閱下列各節：

* [DML 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#on-demand-query-size-calculation)
* [DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#on-demand-query-size-calculation)
* [分群資料表](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#block-pruning)

**注意：** 所選[資料集儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)不會影響隨選查詢費用計算。BigQuery 一律會使用邏輯 (未壓縮) 位元組來計算隨選查詢費用。**注意：** 如果您查詢的[外部資料表資料](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)儲存在 [ORC](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-orc?hl=zh-tw#orc_conversions) 或 [Parquet](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#parquet_conversions) 中，則計費位元組數僅限於 BigQuery 讀取的資料欄。由於查詢會將外部資料來源的資料類型轉換為 BigQuery 資料類型，因此系統會根據 BigQuery 資料類型的大小計算讀取的位元組數。

### 避免執行查詢來探索資料表資料

**最佳做法：**如果您只是想大致查看或預覽資料表中的資料，請勿使用查詢功能。

如果您正在實驗或探索資料，可以使用資料表預覽選項免費查看資料，且不會影響配額。

BigQuery 支援下列資料預覽選項：

* 在 Google Cloud 控制台的資料表詳細資料頁面中，按一下「Preview」(預覽) 分頁標籤，即可查看資料樣本。
* 在 bq 指令列工具中，使用 [`bq head`](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw#browse-table) 指令並指定要預覽的資料列數量。
* 在 API 中，使用 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 從一組指定的資料列擷取資料表資料。
* 請避免在非分群資料表中使用 `LIMIT`。對於非分群資料表，`LIMIT` 子句不會降低運算費用。

### 限制每項查詢的計費位元組數

**最佳做法：**使用隨選定價模式時，請設定計費位元組數上限，限制查詢費用。

您可以使用計費位元組上限設定，限制針對查詢計費的位元組數。設定計費位元組數上限後，系統會在執行查詢前，預估查詢讀取的位元組數。如果預估的位元組數超過限制，查詢就會失敗，不會產生費用。

如果是分群資料表，查詢的計費位元組數預估值是上限，可能會高於執行查詢後實際計費的位元組數。因此在某些情況下，如果您設定了計費位元組數上限，即使實際計費位元組數不會超過計費位元組數上限設定，分群資料表上的查詢仍可能失敗。

如果查詢因計費位元組上限設定而失敗，系統會傳回類似下列的錯誤：

`Error: Query exceeded limit for bytes billed: 1000000. 10485760 or higher
required.`

設定資料量計費上限：

### 控制台

1. 在「查詢編輯器」中，依序點選「編輯」>「查詢設定」>「進階選項」。
2. 在「Maximum bytes billed」(計費位元組數上限) 欄位中輸入整數。
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

### 避免在非分群資料表中使用 `LIMIT`

**最佳做法：**對於非分群資料表，請勿使用 `LIMIT` 子句做為成本控管方法。

對於非分群資料表，在查詢中套用 `LIMIT` 子句不會影響讀取的資料量。即使查詢只傳回一部分，您仍須支付讀取整個資料表中所有位元組的費用。如果是分群資料表，`LIMIT` 子句可以減少掃描的位元組數，因為掃描到足夠的區塊來取得結果時，掃描就會停止。系統只會依據掃描的位元組數收費。

### 分階段具體化查詢結果

**最佳做法：**如有可能，請分階段具體化查詢結果。

如果您要建立大型、多階段的查詢，每次執行查詢時，BigQuery 都會讀取查詢要求的所有資料。系統會針對您每次執行查詢時讀取的所有資料收取相關費用。

因此，請改為分階段查詢，每個階段都會將查詢結果寫入[目的地資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#permanent-table)來具體化查詢結果。查詢較小的目的地資料表會減少讀取的資料量並降低費用。儲存具體化結果的費用比處理大量資料的費用低很多。

### 使用 Rapid Cache 透過外部資料表查詢 Cloud Storage

**最佳做法：**使用外部資料表查詢 Cloud Storage 資料時，建議啟用 Rapid Cache。

Rapid Cache 為 Cloud Storage bucket 提供採用 SSD 的可用區讀取快取，可提升查詢效能，並降低查詢外部資料表的費用。詳情請參閱「[最佳化 Cloud Storage 外部資料表查詢](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#cloud-storage-query-optimization)」。

## 控管工作負載費用

本節說明控管工作負載成本的最佳做法。**工作負載是一組相關查詢**。例如，工作負載可以是每日執行的資料轉換管道、一組由業務分析師執行的資訊主頁，或由一組資料科學家執行的多個臨時查詢。

### 使用 Google Cloud Pricing Calculator

**最佳做法：**使用 [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw)，根據預測用量建立 BigQuery 的每月總費用估算。接著，您可以將這項預估值與實際費用進行比較，找出可最佳化的部分。

### 隨選

如要使用 [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw) 估算隨選定價模式的費用，請按照下列步驟操作：

1. 開啟 [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw)。
2. 按一下「新增至估算項目」。
3. 選取「BigQuery」。
4. 在「Service type」(服務類型) 部分選取「On-demand」(隨選)。
5. 選擇要執行查詢的位置。
6. 在「Amount of data queried」(查詢的資料量) 部分，輸入模擬測試或查詢驗證工具預估讀取的位元組數。
7. 輸入「Active storage」(使用中儲存空間)、「Long-term storage」(長期儲存空間)、「Streaming inserts」(串流資料即時插入)和「Streaming reads」(串流讀取) 的預估儲存空間用量。您只需根據[資料集儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)，估算實體儲存空間或邏輯儲存空間。
8. 預估費用會顯示在「Cost details」(費用詳細資料) 面板中。如要進一步瞭解預估費用，請按一下「開啟詳細檢視畫面」。您也可以下載及分享費用估算結果。

詳情請參閱[以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)一文。

### 版本

如要使用 [BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的運算資源定價模式，並透過 [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw) 估算費用，請按照下列步驟操作：

1. 開啟 [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw)。
2. 按一下「新增至估算項目」。
3. 選取「BigQuery」。
4. 在「服務類型」部分選取「版本」。
5. 選擇使用運算單元的位置。
6. 選擇**版本**。
7. 選擇「運算單元數量上限」、「基準運算單元數量」、「承諾使用合約」(選用) 和「自動調度資源預估使用率」。
8. 選擇資料的儲存位置。
9. 輸入「Active storage」(使用中儲存空間)、「Long-term storage」(長期儲存空間)、「Streaming inserts」(串流資料即時插入)和「Streaming reads」(串流讀取)的預估儲存空間用量。您只需根據[資料集儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)，估算實體儲存空間或邏輯儲存空間。
10. 預估費用會顯示在「Cost details」(費用詳細資料) 面板中。如要進一步瞭解預估費用，請按一下「開啟詳細檢視畫面」。您也可以下載及分享費用估算結果。

詳情請參閱「[依運算資源用量計費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)」。

### 使用預留項目和承諾使用合約

**最佳做法：**使用 BigQuery 預留項目和承諾使用合約來控管費用。

詳情請參閱「[限制各定價模式的費用](#restrict-compute-costs)」。

### 使用運算單元估算工具

**最佳做法：**使用運算單元估算工具，估算工作負載所需的運算單元數量。

[BigQuery 運算單元估算工具](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)可根據歷來成效指標，協助您管理運算單元容量。

此外，如果客戶採用隨選定價模式，在改用依用量計費模式時，可以查看承諾使用合約和自動調度資源預留項目的規模建議，並享有類似的效能。

### 取消不必要的長時間執行工作

如要釋出容量，請檢查長時間執行的工作，確認是否應繼續執行。如果沒有，請[取消](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#cancel_jobs)。

### 使用資訊主頁查看費用

**最佳做法：**建立資訊主頁來分析 Cloud Billing 資料，以便監控及調整 BigQuery 用量。

您可以將[帳單資料匯出](https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=zh-tw)至 BigQuery，並在數據分析等工具中以圖表呈現。 如需建立帳單資訊主頁的教學課程，請參閱「[使用 BigQuery 和數據分析以圖表呈現 Google Cloud 帳單](https://medium.com/google-cloud/visualize-gcp-billing-using-bigquery-and-data-studio-d3e695f90c08)」。

### 使用帳單預算和快訊

**最佳做法：**使用 [Cloud Billing 預算](https://docs.cloud.google.com/billing/docs/how-to/budgets?hl=zh-tw)，集中監控 BigQuery 費用。

Cloud Billing 預算可讓您追蹤實際費用，並與預估費用比較。設定預算金額後，您可以設定預算快訊門檻規則，用來觸發電子郵件通知。預算快訊電子郵件可協助您掌握 BigQuery 支出與預算的對比情況。

## 控管儲存費用

請按照下列最佳做法，盡可能提高 BigQuery 儲存空間的成本效益。您也可以[將儲存空間調整至最佳狀態，藉此提高查詢效能](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)。

### 使用長期儲存空間

**最佳做法：**使用[長期儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)，降低舊資料的成本。

將資料載入 BigQuery 儲存空間時，資料須依 BigQuery [儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)計費。如果是較舊的資料，您可以自動享有 BigQuery 長期儲存空間定價。

如果資料表連續 90 天未經修改，該資料表的儲存空間價格會自動降低 50%。如果您有分區資料表，系統會分別考量每個分區是否符合長期定價資格，並適用與非分區資料表相同的規則。

請注意，資料表和資料表分區進入長期儲存空間後，如果對資料、中繼資料或分區進行任何修改，可能會導致這些資源移回使用中的 BigQuery 儲存空間。以下列舉可能導致這項異動的行為：

* 插入、更新、截斷、合併或刪除會變更資料表資料的陳述式
* 將資料載入、串流或附加至資料表
* 變更資料表結構定義的 `ALTER` 陳述式
* 新增或修改資料表屬性，例如說明、標籤或到期時間
* 修改資料表中繼資料

### 設定儲存空間計費模式

**最佳做法：**根據使用模式，選擇最合適的儲存空間計費模式。

BigQuery 支援使用邏輯 (未壓縮) 或實體 (壓縮) 位元組，或兩者並用的方式計算儲存空間費用。每個資料集設定的[儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)會決定儲存空間定價，但不會影響查詢效能。

您可以[根據用量模式](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw#forecast_storage_billing)，使用 `INFORMATION_SCHEMA` 檢視畫面判斷最合適的儲存空間計費模式。

### 避免覆寫資料表

**最佳做法：**使用實體儲存空間計費模式時，請避免重複覆寫資料表。

覆寫資料表時 (例如在[批次載入工作](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#appending_to_or_overwriting_a_table)中使用 `--replace` 參數，或使用 [`TRUNCATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#truncate_table_statement) SQL 陳述式)，系統會在時間旅行和安全防護期間保留遭替換的資料。如果頻繁覆寫資料表，會產生額外的儲存空間費用。

您可以使用載入工作中的 `WRITE_APPEND` 參數、`MERGE` SQL 陳述式，或使用 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api-grpc?hl=zh-tw)，將資料逐步載入資料表。

### 縮短時間回溯期

**最佳做法：**您可以根據需求縮短時間旅行保留期限。

如果將[時間回溯](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)期限從預設值 (七天) 縮短，資料表中刪除或變更的資料保留期限也會縮短。只有在使用實體 (壓縮) [儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)時，系統才會收取時間旅行儲存空間費用。

時間回溯期是在資料集層級設定。您也可以使用[配置設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)，為新資料集設定預設時間旅行視窗。

### 為目的地資料表設定到期時間

**最佳做法：**如果您將大型查詢結果寫入目的地資料表，請使用預設資料表到期時間，等到您不再需要這些資料時，系統便會依照設定的時間來刪除資料。

在 BigQuery 儲存空間中保留大型結果集會產生費用。如果不需要永久存取結果，請使用[預設資料表到期時間](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#table-expiration)，讓系統自動刪除資料。

### 將資料封存至 Cloud Storage

**最佳做法：**建議您將資料封存在 Cloud Storage。

您可以根據業務封存需求，將資料從 BigQuery 移至 Cloud Storage。最佳做法是先考量[長期儲存空間定價](#store-data-bigquery)和[實體儲存空間計費模式](#storage-billing-model)，再[從 BigQuery 匯出資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)。

## 排解 BigQuery 費用不一致和意外收費的問題

如要排解非預期的 BigQuery 費用或費用差異問題，請按照下列步驟操作：

1. 查看 Cloud Billing 帳單報表時，如要瞭解 BigQuery 費用的來源，建議先依 SKU 將費用分組，以便觀察對應 BigQuery 服務的用量和費用。
2. 接著，請在 [SKU 說明文件頁面](https://cloud.google.com/skus?hl=zh-tw)或 Cloud Billing UI 的 `Pricing`頁面，查看對應 SKU 的定價，瞭解這是哪項功能，例如 BigQuery Storage Read API、長期儲存空間、隨選定價、Standard 版本。
3. 找出對應的 SKU 後，請使用 `INFORMATION_SCHEMA` 檢視畫面，找出與這些費用相關聯的特定資源，例如：

   * 如果系統向您收取隨選分析費用，請查看 [`INFORMATION_SCHEMA.JOBS` 檢視範例](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#examples)，判斷哪些工作產生費用，以及哪些使用者啟動了這些工作。
   * 如果系統向您收取預留項目或承諾使用合約 SKU 的費用，請查看對應的 [`INFORMATION_SCHEMA.RESERVATIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw) 和 [`INFORMATION_SCHEMA.CAPACITY_COMMITMENTS`](https://docs.cloud.google.com/bigquery/docs/information-schema-capacity-commitments?hl=zh-tw#example) 檢視畫面，找出產生費用的預留項目和承諾使用合約。
   * 如果費用來自儲存空間 SKU，請查看 [`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表範例](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw#example_2)，瞭解哪些資料集和資料表會產生更多費用。

疑難排解重要注意事項：

* 請注意，Cloud Billing 帳單報表中的「每日」時間範圍是從美國和加拿大太平洋時間 (UTC-8) 午夜開始，並會根據美國日光節約時間調整，因此請調整計算和資料匯總方式，以符合相同的時間範圍。
* 將 Cloud Billing UI 與[匯出至 BigQuery 的 Cloud Billing 資料](https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=zh-tw)進行比較時，請務必根據 `usage_start_time` 和 `usage_end_time` 匯總，而非 `export_time`。
* 如果帳單帳戶連結多項專案，而您想查看特定專案的費用，請依專案篩選。
* 執行調查時，請務必選取正確的區域。

### 專案超過免費查詢位元組掃描配額

在免費使用層級執行查詢時，如果帳戶達到每月查詢上限，BigQuery 就會傳回這項錯誤。如要進一步瞭解查詢定價，請參閱「[免費使用層級](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-usage-tier)」。

**錯誤訊息**

```
Your project exceeded quota for free query bytes scanned
```

#### 解析度

如要繼續使用 BigQuery，請[將帳戶升級為 Cloud Billing 付費帳戶](https://docs.cloud.google.com/free/docs/gcp-free-tier?hl=zh-tw#how-to-upgrade)。

### 查詢、預留項目和承諾使用合約相關的非預期費用

如要排解與工作執行相關的非預期費用問題，請根據費用來源採取相應措施：

* 如果隨選分析費用增加，可能是因為啟動的工作數量增加，或工作需要處理的資料量有所變動。請使用 [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 檢視畫面調查。
* 如果承諾使用運算單元的費用增加，請查詢 [`INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES`](https://docs.cloud.google.com/bigquery/docs/information-schema-capacity-commitment-changes?hl=zh-tw)，確認是否購買或修改了新的承諾使用合約。
* 如要瞭解預留項目用量增加的原因，請查看 [`INFORMATION_SCHEMA.RESERVATION_CHANGES`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservation-changes?hl=zh-tw) 中記錄的預留項目變更。如要將自動調度資源預留項目用量與帳單資料進行比對，請按照[自動調度資源範例](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#slot-autoscaling)操作。

#### 計費運算單元時數大於 INFORMATION\_SCHEMA.JOBS 檢視表計算的運算單元時數

使用自動調度資源預留項目時，系統會根據調度後的運算單元數量計算費用，而非使用的運算單元數量。BigQuery 會以 50 個運算單元為單位自動調度資源，因此即使實際用量低於自動調度資源的數量，仍會按最接近的倍數計費。根據預設，自動配置器在縮減資源前至少會等待 1 分鐘，因此即使查詢使用運算單元的時間較短 (例如 1 分鐘內只用了 10 秒)，系統仍會收取至少 1 分鐘的費用。如要避免這些費用，您可以在預留項目層級選擇加入 BigQuery 流暢擴充功能，按秒計費，且沒有最短時間限制。如要瞭解如何正確估算自動調度資源預留項目的費用，請參閱「[Slots Autoscaling](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#slot-autoscaling)」(運算單元自動調度資源) 頁面。如要進一步瞭解如何有效率地使用自動調度資源功能，請參閱[自動調度資源最佳做法](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#slot-autoscaling)。

非自動調度資源的預留項目也會有類似情況，計費方式是根據佈建的運算單元數量，而非使用的運算單元數量。如要預估非自動調度資源預留項目的費用，可以直接查詢 [`RESERVATIONS_TIMELINE` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-reservation-timeline?hl=zh-tw#examples)。

#### 專案執行隨選查詢時，帳單費用低於透過 INFORMATION\_SCHEMA.JOBS 計算的計費位元組總數

實際帳單費用低於計算出的已處理位元組數，可能原因如下：

* 每項專案每月可享有 1 TB 的免費方案查詢配額，不需額外付費。
* 計算時未排除`SCRIPT`類型工作，因此部分值可能重複計算。
* Cloud Billing 帳戶適用的各種節省費用，例如議定折扣、促銷抵免額等。 請查看 [Cloud Billing 帳單報表](https://docs.cloud.google.com/billing/docs/how-to/cost-breakdown?hl=zh-tw#credits)的「節省費用」部分。免費方案每月可處理 1 TB 的查詢量也包含在內。

#### 專案執行隨選查詢時，計費位元組數大於透過 INFORMATION\_SCHEMA.JOBS 計算的處理位元組數

如果帳單金額大於您透過查詢 `INFORMATION_SCHEMA.JOBS` 檢視表計算出的值，可能是下列情況所致：

* 查詢資料列層級安全性資料表

  + 如果資料表設有資料列層級安全性，查詢不會在 `INFORMATION_SCHEMA.JOBS` 檢視中產生 `total_bytes_billed` 值，因此使用 `INFORMATION_SCHEMA.JOBS` 檢視中的 `total_bytes_billed` 計算出的帳單費用會低於實際帳單費用。如要進一步瞭解為何無法查看這項資訊，請參閱「[資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw#limit-side-channel-attacks)」頁面。
* 在 BigQuery 執行機器學習作業

  + BigQuery ML 的隨選查詢計費方式取決於建立的模型類型。部分模型作業的費率高於非機器學習查詢。因此，如果只是將專案的所有 `total_billed_bytes` 相加，並使用標準隨選定價的每 TB 費率，這並不是正確的定價匯總，您必須考量每 TB 的定價差異。
* 價格金額不正確

  + 確認計算時使用的每 TB 定價值正確無誤，並務必選擇正確的區域，因為價格會因位置而異。請參閱[定價說明文件](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#bigquery-pricing)。

一般建議是按照[公開說明文件](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#compare_on-demand_job_usage_to_billing_data)中的建議方式，計算計費隨選工作用量。

#### 即使已停用 API，且未使用預留項目或承諾使用合約，仍須支付 BigQuery Reservations API 費用

檢查 SKU，進一步瞭解哪些服務會產生費用。如果計費 SKU 是 `BigQuery Governance SKU`，則費用來自 Knowledge Catalog。部分 Knowledge Catalog 功能會使用 BigQuery 觸發工作執行作業。這些費用現在會依據對應的 BigQuery Reservations API SKU 處理。 詳情請參閱 [Knowledge Catalog 定價](https://cloud.google.com/dataplex/pricing?e=48754805&hl=zh-tw#dataplex-universal-catalog-pricing)說明文件。

#### 專案已指派給預留項目，但仍會產生 BigQuery Analysis 隨選費用

請詳閱「[排解預訂問題](https://docs.cloud.google.com/bigquery/docs/troubleshoot-workload-management?hl=zh-tw#troubleshoot_issues_with_reservations)」一節，找出 `Analysis` 費用的可能來源。

#### BigQuery Standard 版本的即付即用 (PAYG) 運算單元產生不明費用

在 Cloud Billing 帳單報表中，套用標籤為 `goog-bq-feature-type`、值為 `BQ_STUDIO_NOTEBOOK` 的篩選器。您看到的使用量，是 [BigQuery Standard 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)中，以即付即用運算單元計量的用量。這是使用 [BigQuery Studio 筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw#monitor)的費用。進一步瞭解 [BigQuery Studio 筆記本定價](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#notebook-runtime-pricing)。

#### BigQuery Enterprise 版本的即付即用 (PAYG) 運算單元產生不明費用

在 Cloud Billing 帳單報表中，套用標籤為 `goog-bq-feature-type`、值為 `SPARK_PROCEDURE` 的篩選器。您看到的使用量，是 [BigQuery Enterprise 版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)中以即付即用運算單元計量。這是使用 [BigQuery Apache Spark 程序](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw#pricing)的費用，無論專案使用哪種運算模型，都會以此方式計費。

#### 停用 Reservation API 後，仍產生 BigQuery Reservations API 費用

停用 BigQuery 不會停止收取承諾使用合約費用。如要停止支付使用承諾費用，您必須刪除使用承諾。將續約方案設為「`NONE`」，合約到期時就會自動刪除。

#### 查詢極小的資料表時，隨選計費的成本會不成比例地高

無論資料表的實際大小為何，BigQuery 查詢的「每個參照資料表處理的資料量」最低計費標準為 10 MiB。同樣地，每項查詢處理的資料量最低計費標準為 10 MiB。查詢小型資料表 (即使是 KB 大小的資料表) 時，每次查詢至少會產生 10 MiB 的費用。這可能導致費用遠高於隨選計費預估值，尤其是隨選運算定價。

### 未預期的儲存空間費用

可能導致儲存空間費用增加的情況：

* 資料表中儲存的資料量增加：使用 [`INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-usage?hl=zh-tw) 檢視畫面，監控資料表的位元組變化
* 變更[資料集計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)
* 增加實體計費模式資料集的[時間旅行視窗](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)
* 修改[長期儲存空間](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#storage-pricing)中的資料表，使其成為[近期內容儲存空間](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#storage-pricing)

#### 刪除資料表或資料集後，BigQuery 儲存空間費用增加

[BigQuery 時光旅行功能](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)會保留已刪除的資料，保留時間為設定的時光旅行時間範圍，外加 7 天的安全復原期。在保留期間，實體儲存空間計費模式資料集內已刪除的資料，仍會計入使用中的實體儲存空間費用，即使資料表不再顯示於 `INFORMATION_SCHEMA.TABLE_STORAGE` 或控制台也一樣。如果資料表資料位於長期儲存空間，刪除後會移至使用中的實體儲存空間。根據 [BigQuery 儲存空間定價頁面](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#storage-pricing)，使用中實體位元組的費用約為長期實體位元組的 2 倍，因此相應費用會增加。如要盡量降低實體儲存空間計費模式資料集因刪除資料而產生的費用，建議將時間旅行回溯期縮短為 2 天。

#### 不需修改資料，即可降低儲存空間成本

在 BigQuery 中，使用者須支付近期內容和長期存放內容的儲存空間費用。近期內容儲存空間費用包含連續 90 天未經修改的資料表或資料表分區，而長期儲存空間費用則包含連續 90 天未經修改的資料表和分區。資料轉換至長期儲存空間後，整體儲存空間費用會降低，比使用中儲存空間便宜約 50%。詳情請參閱[儲存空間定價](https://cloud.google.com/bigquery/pricing?e=48754805&hl=zh-tw#storage-pricing)。

#### 儲存空間費用增加，但資料量並未顯著增加

如果對資料表資料、中繼資料或分區執行特定動作，導致長期儲存空間中的資料移至 BigQuery 作用中儲存空間，儲存費用可能會增加。詳情請參閱「[使用長期儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#store-data-bigquery)」。

#### INFORMATION\_SCHEMA 儲存空間計算結果與帳單不符

* 使用 [`INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-usage?hl=zh-tw)，而非 `INFORMATION_SCHEMA.TABLE_STORAGE` - `TABLE_STORAGE_USAGE_TIMELINE` 提供更準確、更精細的資料，可正確計算儲存空間費用
* 在 `INFORMATION_SCHEMA` 檢視表上執行的查詢不含稅金、調整項和四捨五入誤差，比較資料時請考量這些因素。如要進一步瞭解 Cloud Billing 報表，請參閱[這個頁面](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw)。
* `INFORMATION_SCHEMA` 檢視畫面中的資料以世界標準時間 (UTC) 為準，而帳單報表資料則以美國和加拿大太平洋時間 (UTC-8) 為準。

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

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]