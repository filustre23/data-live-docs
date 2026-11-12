Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用快取查詢結果

除非您指定永久目的地資料表，否則 BigQuery 會自動將查詢結果寫入暫時的快取結果資料表。再次執行相同查詢時，BigQuery 可以直接從快取資料表傳回結果，加快查詢執行速度，並避免產生額外的運算費用。

系統會為每位使用者和每個專案維護暫時快取結果資料表，[互動式和批次查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)的快取時間約為 24 小時，但有部分[例外狀況](#cache-exceptions)。視版本而定，您可能也可以存取同一專案中[其他使用者的快取結果](#cross-user-caching)。儲存快取結果資料表不會產生費用，但永久資料表會產生[儲存空間費用](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。

## 限制

使用查詢快取會受到下列限制：

* 當您執行重複的查詢時，BigQuery 會嘗試重複使用快取查詢結果。如要從快取擷取資料，重複的查詢文字必須與原始查詢相同。
* 如要將查詢結果保留在快取結果資料表中，結果集必須小於回應大小上限。如要進一步瞭解如何管理大型結果集，請參閱[傳回大量查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#large-results)。
* 您無法使用 [DML](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw) 陳述式指定快取結果資料表。
* 雖然目前的語意允許，但不建議將快取結果做為依附工作的輸入內容。舉例來說，您不應提交從快取資料表擷取結果的查詢工作。而是改將您的結果寫入已命名的目標資料表。為簡化清理作業，您可以使用資料集層級的 `defaultTableExpirationMs` 屬性等功能，在指定時間後自動刪除資料。

## 定價與配額

快取的查詢結果會儲存為臨時資料表。將快取查詢結果儲存在臨時資料表，不需支付儲存費用。從快取結果資料表擷取查詢結果時，工作統計資料屬性 `statistics.query.cacheHit` 會傳回 `true`，且您不需支付查詢費用。雖然使用快取結果的查詢不會產生費用，但查詢仍須遵守 BigQuery [配額政策](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。

除了降低成本外，使用快取結果的查詢速度也明顯較快，因為 BigQuery 不需要計算結果集。

## 查詢快取的例外狀況

在下列情況下，系統無法快取查詢結果：

* 在工作設定、 Google Cloud 控制台、 bq 指令列工具或 API 中指定目的地資料表時。
* 自上次快取結果後，任何參照的資料表或邏輯檢視表有所變更。
* 查詢參照的任何資料表最近收到串流資料即時插入 (資料表在寫入最佳化儲存空間中有資料)，即使沒有新資料列也一樣。
* 如果查詢使用非確定性函式，例如 `CURRENT_TIMESTAMP()` 和 `CURRENT_DATE` 等日期和時間函式，以及 `SESSION_USER()` 等其他函式，則會根據查詢執行時間傳回不同的值。
* 使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)查詢多個資料表。
* 快取結果已過期。快取生命週期通常為 24 小時，但快取結果會盡可能保留，也可能提早失效。
* 如果查詢是針對 Cloud Storage 以外的[外部資料來源](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw)執行。(Cloud Storage 上的 GoogleSQL 查詢支援快取查詢結果)。
* 如果查詢是針對受[資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)保護的資料表執行，系統就不會快取結果。
* 如果查詢執行的資料表受到[資料欄層級安全性](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)保護 (包括資料遮蓋)，系統可能不會快取結果。
* 查詢文字有任何變更，包括修改空白字元或註解。

## 快取結果的儲存方式

執行查詢時，系統會在特殊類型的[隱藏資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#hidden_datasets) (稱為*匿名資料集*) 中，建立暫時的快取結果資料表。一般資料集會沿用 IAM 資源階層模型 (專案和組織權限) 的權限，但匿名資料集只有擁有者可以存取。匿名資料集的擁有者是執行查詢並產生快取結果的使用者。此外，系統也會檢查專案的 `bigquery.jobs.create` 權限，確認使用者是否能存取專案。

BigQuery 不支援共用匿名資料集。如果您打算共用查詢結果，請勿使用儲存在匿名資料集中的快取結果。而是改將結果寫入已命名的目標資料表。

雖然執行查詢的使用者具備資料集和快取結果資料表的完整存取權，但我們不建議將這些資料表做為依附工作的輸入內容。

匿名資料集的名稱開頭為底線。
這樣一來， Google Cloud 控制台的資料集清單就不會顯示這些資料集。
您可以使用 bq 指令列工具或 API，列出匿名資料集，並稽核匿名資料集的存取控管機制。

如要進一步瞭解如何列出及取得資料集 (包括匿名資料集) 的相關資訊，請參閱「[列出資料集](https://docs.cloud.google.com/bigquery/docs/listing-datasets?hl=zh-tw)」。

## 跨使用者快取

如果您具備執行查詢所需的權限，且查詢結果已在專案中為其他使用者快取，BigQuery 就會傳回快取中的結果。快取結果會複製到您的個人匿名資料集，並在您執行查詢後保留 24 小時。

如果您使用的是 Enterprise 或 Enterprise Plus [版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)，則可使用跨使用者快取功能。單一使用者快取的[限制和例外狀況](#cache-exceptions)也適用於跨使用者快取。

## 停用快取結果擷取作業

如果您選擇 [Use cached results] (使用快取的結果) 選項，系統會重複使用先前執行相同查詢時的結果，除非所查詢的資料表曾有異動。快取結果只在重複相同查詢時會發揮效用；雖然新查詢的 [Use cached results] (使用快取的結果) 選項預設為啟用，但不會有任何效果。

當您重複相同查詢時，如果 [Use cached results] (使用快取的結果) 選項已停用，系統會覆寫現有的快取結果。在這種情況下，BigQuery 必須計算查詢結果，因此您必須支付這項查詢的費用。這特別適合用來處理基準化作業。

如要停用快取結果擷取功能，並強制執行查詢工作的即時評估作業，您可以將查詢工作的 `configuration.query.useQueryCache` 屬性設定為 `false`。

如要停用 [Use cached results] (使用快取的結果) 選項：

### 控制台

1. 開啟 Google Cloud 控制台。  
   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 [Compose new query] (撰寫新查詢)。
3. 在「Query editor」(查詢編輯器) 文字區域中輸入有效的 SQL 查詢。
4. 依序點選「編輯」>「查詢設定」。
5. 在「快取偏好設定」部分，清除「使用快取結果」。

### bq

使用 `nouse_cache` 旗標覆寫查詢快取。下列範例會強制 BigQuery 處理查詢，而不使用現有的快取結果：

```
 bq query \
 --nouse_cache \
 --batch \
 'SELECT
    name,
    count
  FROM
    `my-project`.mydataset.names_2013
  WHERE
    gender = "M"
  ORDER BY
    count DESC
  LIMIT
    6'
```

### API

如要在不使用現有快取結果的情況下處理查詢，請在 `query` 工作設定中將 `useQueryCache` 屬性設為 `false`。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// queryDisableCache demonstrates issuing a query and requesting that the query cache is bypassed.
func queryDisableCache(w io.Writer, projectID string) error {
	// projectID := "my-project-id"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	q := client.Query(
		"SELECT corpus FROM `bigquery-public-data.samples.shakespeare` GROUP BY corpus;")
	q.DisableQueryCache = true
	// Location must match that of the dataset(s) referenced in the query.
	q.Location = "US"

	// Run the query and print results when the query job is completed.
	job, err := q.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}
	if err := status.Err(); err != nil {
		return err
	}
	it, err := job.Read(ctx)
	for {
		var row []bigquery.Value
		err := it.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintln(w, row)
	}
	return nil
}
```

### Java

如要在不使用現有快取結果的情況下處理查詢，請在建立 [QueryJobConfiguration](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration?hl=zh-tw) 時，將[使用查詢快取](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration.Builder?hl=zh-tw#com_google_cloud_bigquery_QueryJobConfiguration_Builder_setUseQueryCache_java_lang_Boolean_)設為 `false`。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;

// Sample to running a query with the cache disabled.
public class QueryDisableCache {

  public static void runQueryDisableCache() {
    String query = "SELECT corpus FROM `bigquery-public-data.samples.shakespeare` GROUP BY corpus;";
    queryDisableCache(query);
  }

  public static void queryDisableCache(String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              // Disable the query cache to force live query evaluation.
              .setUseQueryCache(false)
              .build();

      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query disable cache performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
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

async function queryDisableCache() {
  // Queries the Shakespeare dataset with the cache disabled.

  // Create a client
  const bigquery = new BigQuery();

  const query = `SELECT corpus
    FROM \`bigquery-public-data.samples.shakespeare\`
    GROUP BY corpus`;
  const options = {
    query: query,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
    useQueryCache: false,
  };

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(options);
  console.log(`Job ${job.id} started.`);

  // Wait for the query to finish
  const [rows] = await job.getQueryResults();

  // Print the results
  console.log('Rows:');
  rows.forEach(row => console.log(row));
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

// Extract query results
$queryResults = $bigQuery->runQuery($jobConfig);

$i = 0;
foreach ($queryResults as $row) {
    printf('--- Row %s ---' . PHP_EOL, ++$i);
    foreach ($row as $column => $value) {
        printf('%s: %s' . PHP_EOL, $column, json_encode($value));
    }
}
printf('Found %s row(s)' . PHP_EOL, $i);
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

job_config = bigquery.QueryJobConfig(use_query_cache=False)
sql = """
    SELECT corpus
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus;
"""
query_job = client.query(sql, job_config=job_config)  # Make an API request.

for row in query_job:
    print(row)
```

## 確保使用快取

如果使用 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/insert?hl=zh-tw) 方法執行查詢，您可以將 `query` 工作設定的 `createDisposition` 屬性設為 `CREATE_NEVER`，強制查詢工作失敗，除非可以使用快取結果。

如果快取中沒有查詢結果，系統會傳回 `NOT_FOUND` 錯誤。

### bq

使用 `--require_cache` 旗標，要求從查詢快取取得結果。下列範例會強制 BigQuery 處理查詢，即使快取中已有結果：

```
 bq query \
 --require_cache \
 --batch \
 'SELECT
    name,
    count
  FROM
    `my-project`.mydataset.names_2013
  WHERE
    gender = "M"
  ORDER BY
    count DESC
  LIMIT
    6'
```

### API

如要使用現有的快取結果處理查詢，請在 `query` 工作設定中，將 [`createDisposition` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationQuery.FIELDS.create_disposition)設為 `CREATE_NEVER`。

## 驗證是否使用快取

請使用下列任一方法，判斷 BigQuery 是否使用快取傳回結果：

* **使用 Google Cloud 控制台**。前往「Query results」(查詢結果)，然後按一下「Job Information」(工作資訊)。「處理的位元組數」顯示「0 B (已快取結果)」。
* **使用 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/v2?hl=zh-tw)。**
  查詢結果中的 `cacheHit` 屬性已設為 `true`。

## 資料欄層級安全防護機制的影響

根據預設，BigQuery 會將查詢結果快取 24 小時，但有先前所述的[例外狀況](#cache-exceptions)。如果查詢的資料表受[資料欄層級安全性](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)保護，系統可能不會快取查詢。如果 BigQuery 快取結果，則適用 24 小時的快取生命週期。

如果變更政策標記使用的 Data Catalog 精細讀取者角色 (例如移除群組或使用者)，24 小時快取不會失效。對 Data Catalog 精細讀取者存取控管群組本身的變更會立即傳播，但變更不會使快取失效。

這代表如果使用者執行查詢，仍可查看查詢結果。即使使用者在過去 24 小時內失去資料存取權，仍可從快取擷取這些結果。

使用者從政策標記的 Data Catalog 精細讀取者角色中移除後，在 24 小時內，只能存取先前允許查看的快取資料。如果資料表新增了資料列，即使結果已快取，使用者也無法查看新增的資料列。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]