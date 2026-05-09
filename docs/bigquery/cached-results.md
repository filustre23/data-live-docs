Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用快取查詢結果

BigQuery 會將所有查詢結果寫入資料表。這份資料表可以由使用者明確指定 (即目標資料表)，也可以是暫時性的快取結果資料表。如果您再次執行完全相同的查詢，BigQuery 會從快取資料表傳回結果 (如有)。暫時性的快取結果資料表是依據不同的使用者和專案個別維護，視版本而定，您可能可以存取在相同專案中執行查詢的[其他使用者快取結果](#cross-user-caching)。系統不會針對快取查詢結果資料表向您收取儲存空間費用。不過，如果您將查詢結果寫入永久性資料表，則須支付資料的[儲存](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)費用。

所有查詢結果 (包括[互動式與批次查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)) 會以快取方式存放在暫時性資料表中約 24 小時，但也有一些[例外狀況](#cache-exceptions)。

## 限制

使用查詢快取會受到下列限制：

* 當您執行重複的查詢時，BigQuery 會嘗試重複使用快取查詢結果。重複的查詢字詞必須與原始查詢完全相同，系統才能從快取中擷取資料。
* 如要將查詢結果保留在快取結果資料表中，結果集必須小於回應大小上限。如要進一步瞭解如何管理大型結果集，請參閱[傳回大量查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#large-results)。
* 您無法使用 [DML](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw) 陳述式指定快取結果資料表。
* 雖然目前的語意允許這類操作，但建議您不要將快取結果做為相依工作的輸入內容。舉例來說，請不要提交會從快取資料表擷取結果的查詢工作，而是改將您的結果寫入已命名的目標資料表。如要簡化清除作業，資料集層級 `defaultTableExpirationMs` 屬性等功能可能會在指定期限過後使資料自動過期。

## 定價與配額

快取的查詢結果會儲存為暫時性資料表。您不需要為儲存在臨時資料表中的快取查詢結果支付費用。如果查詢結果是擷取自快取結果資料表，系統傳回的工作統計資料屬性 `statistics.query.cacheHit` 值為 `true`，您就無須為這項查詢作業支付費用。雖然使用快取結果的查詢作業不收費，但仍適用 BigQuery [配額政策](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw)。

除了降低成本以外，使用快取結果的查詢作業因為 BigQuery 不需計算結果集，可大幅加快執行速度。

## 查詢快取的例外狀況

在下列情況下，系統無法快取查詢結果：

* 當您在工作設定、 Google Cloud 主控台、 bq 指令列工具或 API 中指定目的地資料表時。
* 在系統上次快取結果之後，已有參考資料表或邏輯檢視表經過異動。
* 查詢所參考的任一資料表最近收到串流資料插入，也就是資料表在寫入最佳化儲存空間中含有資料 (即使未新增任何資料列)。
* 如果查詢使用非確定性函式，比方日期和時間函式 (例如 `CURRENT_TIMESTAMP()` 和 `CURRENT_DATE`) 以及其他函式 (像是 `SESSION_USER()`)，系統會根據查詢執行時間傳回不同的值。
* 使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)查詢多個資料表。
* 快取結果已過期。一般快取的生命週期為 24 小時，但系統會盡量擷取快取結果，因此快取可能會更快失效。
* 針對 Cloud Storage 以外的[外部資料來源](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)執行查詢。(快取查詢結果支援在 Cloud Storage 上執行的 GoogleSQL 查詢)。
* 如果查詢是針對受[資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)保護的資料表執行，結果就不會快取。
* 如果查詢是針對受[資料欄層級安全性](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)保護的資料表執行 (包括資料遮蓋)，系統可能不會快取結果。
* 如果查詢文字有任何變更，包括修改空白字元或註解。

## 快取結果的儲存方式

執行查詢時，系統會在稱為「匿名資料集」的特殊[隱藏資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#hidden_datasets)中，建立暫時性的快取結果資料表。一般資料集是從身分與存取權管理資源階層模型繼承權限 (專案與機構權限)，但匿名資料集的存取權僅限於擁有者。匿名資料集的擁有者是執行產生快取結果的查詢使用者。此外，系統也會檢查專案的 `bigquery.jobs.create` 權限，確認使用者有權存取專案。

BigQuery 不支援共用匿名資料集。如果您打算共用查詢結果，請勿使用儲存在匿名資料集裡的快取結果。而是改將結果寫入已命名的目標資料表。

雖然執行查詢的使用者具備資料集和快取結果資料表的完整存取權，但建議您不要將這些資料做為相依工作的輸入內容。

匿名資料集的名稱會以底線開頭。
因此， Google Cloud 控制台中的資料集清單會隱藏這類名稱。
您可以使用 bq 指令列工具或 API 列出匿名資料集，並稽核這類資料集的存取權控制。

如要進一步瞭解如何列出及取得資料集 (包括匿名資料集) 的相關資訊，請參閱[列出資料集](https://docs.cloud.google.com/bigquery/docs/listing-datasets?hl=zh-tw)。

## 跨使用者快取

如果您具備執行查詢的必要權限，且查詢結果已快取在專案中供其他使用者使用，BigQuery 就會從快取傳回結果。快取結果會複製到您的個人匿名資料集中，並在您執行查詢後的 24 小時內保留在該處。

如果您使用 Enterprise 或 Enterprise Plus [版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)，即可使用跨使用者快取功能。單一使用者快取的[限制和例外狀況](#cache-exceptions)，同樣適用於跨使用者快取。

## 停用快取結果擷取作業

如果您選擇 [Use cached results] (使用快取的結果) 選項，系統會重複使用先前執行相同查詢時的結果，除非所查詢的資料表曾有異動。快取結果只在重複相同查詢時會發揮效用；雖然新查詢的 [Use cached results] (使用快取的結果) 選項預設為啟用，但不會有任何效果。

當您重複相同查詢時，如果 [Use cached results] (使用快取的結果) 選項已停用，系統會覆寫現有的快取結果。在這種情況下，BigQuery 必須計算查詢結果，因此您必須支付這項查詢的費用。這特別適合用來處理基準化作業。

如要停用快取結果擷取功能，並強制執行查詢工作的即時評估作業，您可以將查詢工作的 `configuration.query.useQueryCache` 屬性設定為 `false`。

如要停用 [Use cached results] (使用快取的結果) 選項：

### 控制台

1. 開啟 Google Cloud 控制台。  
   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 [Compose new query] (撰寫新查詢)。
3. 在「Query editor」(查詢編輯器) 文字區域中輸入有效的 SQL 查詢。
4. 按一下 [More] (更多) 並選取 [Query settings] (查詢設定)。
5. 在「Cache preference」(快取偏好) 部分，取消勾選「Use cached results」(使用快取的結果)。

### bq

使用 `nouse_cache` 旗標覆寫查詢快取。下列範例顯示如何強制 BigQuery 在不使用現有快取結果的情況下處理查詢：

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

如要在不使用現有快取結果的情況下處理查詢，請在 `query` 工作設定中，將 `useQueryCache` 屬性設為 `false`。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

如要在不使用現有快取結果的情況下處理查詢，請在建立 [QueryJobConfiguration](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration?hl=zh-tw) 時，[將使用查詢快取設為](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration.Builder?hl=zh-tw#com_google_cloud_bigquery_QueryJobConfiguration_Builder_setUseQueryCache_java_lang_Boolean_) `false`。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

如果您使用 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/insert?hl=zh-tw) 方法執行查詢，可以將 `query` 工作設定的 `createDisposition` 屬性設為 `CREATE_NEVER`，強制讓無法使用快取結果的查詢工作失敗。

如果快取中沒有查詢結果，系統會傳回 `NOT_FOUND` 錯誤。

### bq

使用 `--require_cache` 旗標要求查詢快取的結果。下列範例顯示如何強制 BigQuery 在結果存在於快取的情況下處理查詢：

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

如要使用現有快取結果處理查詢，請在 `query` 工作設定中，將 [`createDisposition` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationQuery.FIELDS.create_disposition)設為 `CREATE_NEVER`。

## 驗證是否使用快取

使用下列任一方法，判斷 BigQuery 傳回的結果是否使用快取：

* **使用 Google Cloud 控制台**。前往「查詢結果」，然後按一下「工作資訊」。「處理的位元組數」顯示「0 B (已快取結果)」。
* **使用 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/v2?hl=zh-tw)。**
  查詢結果中的 `cacheHit` 屬性已設為 `true`。

## 資料欄層級安全防護機制的影響

根據預設，BigQuery 會將查詢結果快取 24 小時，但有先前所述的[例外狀況](#cache-exceptions)。針對受[資料欄層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)保護的資料表進行的查詢，可能不會快取。如果 BigQuery 快取了結果，則適用 24 小時的快取生命週期。

如果變更政策標記所用的 Data Catalog 精細讀取者角色，例如從該角色移除群組或使用者，24 小時快取不會失效。對 Data Catalog 細部讀者存取控管群組所做的變更會立即傳播，但不會使快取失效。

影響：使用者執行查詢後，查詢結果仍會顯示給使用者。即使使用者在過去 24 小時內無法存取資料，仍可從快取中擷取這些結果。

從政策標記的 Data Catalog 精細讀取者角色移除使用者後，使用者只能在 24 小時內存取先前獲准查看的快取資料。如果資料表新增了資料列，即使結果已快取，使用者也無法看到新增的資料列。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]