Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 中的 SQL 簡介

BigQuery 中的 GoogleSQL 可讓您分析大量資料集、管理資料庫物件，以及控管整個資料倉儲的存取權。支援的 SQL 方言和陳述式類型可讓您有效建構複雜查詢，並使用 BigQuery 的全套資料操縱和管理功能。

GoogleSQL 是符合 ANSI 標準的[結構化查詢語言 (SQL)](https://en.wikipedia.org/wiki/SQL)，支援下列類型的陳述式：

* [查詢陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)也稱為資料查詢語言 (DQL) 陳述式，是在 BigQuery 中分析資料的主要方法。這類運算子會掃描一或多個資料表或運算式，並傳回運算結果資料列。查詢陳述式可包含 [pipe 語法](https://docs.cloud.google.com/bigquery/docs/pipe-syntax?hl=zh-tw)。
* [程序語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)是 GoogleSQL 的程序擴充功能，可讓您在單一要求中執行多個 SQL 陳述式。程序陳述式可使用變數和控制流程陳述式，且可能產生副作用。
* [資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)可讓您建立及修改下列物件：

  + 資料集
  + 資料表，包括結構定義和資料欄類型
  + 資料表本機副本和快照
  + 瀏覽次數
  + 函式
  + 索引
  + 承諾使用容量、預留項目和指派作業
  + 資料列層級存取政策
* [資料操縱語言 (DML) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw)可讓您在 BigQuery 資料表中更新、插入及刪除資料。
* [資料控管語言 (DCL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw)可讓您控管 BigQuery 系統資源，例如存取權和容量。
* [交易控制語言 (TCL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#transactions)可讓您管理資料修改交易。
* [載入陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)和[匯出陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)可讓您管理進出 BigQuery 的資料。

## BigQuery SQL 方言

BigQuery 支援 GoogleSQL 語法，建議所有新專案都使用這種語法。此外，我們也提供舊版 SQL 方言，但有[一些限制](https://docs.cloud.google.com/bigquery/docs/legacy-sql-feature-availability?hl=zh-tw)。建議您[從舊版 SQL 遷移至 GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-tw)。

### 變更為使用非預設方言

您用來查詢資料的介面會決定預設的查詢方言。如要切換至其他方言，請執行下列操作：

### 控制台

Google Cloud 控制台的預設方言為 GoogleSQL。如要將方言變更為舊版 SQL，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，依序點選「編輯」>「查詢設定」。
3. 在「Advanced options」(進階選項) 區段中，按一下「SQL dialect」(SQL 方言) 的「Legacy」(舊版)，然後點選「Save」(儲存)。這會為這項查詢設定舊版 SQL 選項。點選「add\_box SQL Query」(add\_box SQL 查詢)add\_box 建立新查詢時，必須再次選取舊版 SQL 選項。

### SQL

預設 SQL 方言為 GoogleSQL。您可以在查詢中加入 `#standardSQL` 或 `#legacySQL` 前置字元，設定 SQL 方言。這些查詢前置字元不區分大小寫，必須位於查詢之前，且必須以換行字元與查詢分隔。以下範例將方言設為舊版 SQL，並查詢 natality 資料集：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   #legacySQL
   SELECT
     weight_pounds, state, year, gestation_weeks
   FROM
     [bigquery-public-data:samples.natality]
   ORDER BY
     weight_pounds DESC
   LIMIT
     10;
   ```
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

`bq` 指令列工具中的預設查詢方言為舊版 SQL。如要切換至 GoogleSQL 方言，請在指令列陳述式中加入 `--use_legacy_sql=false` 或 `--nouse_legacy_sql` 旗標。

**切換至 GoogleSQL 方言**

如要在查詢工作中使用 GoogleSQL 語法，請將 `use_legacy_sql` 參數設為 `false`。

```
  bq query \
  --use_legacy_sql=false \
  'SELECT
    word
  FROM
    `bigquery-public-data.samples.shakespeare`'
```

**將 GoogleSQL 設為預設方言**

您可以編輯指令列工具的設定檔 `.bigqueryrc`，將 GoogleSQL 設為指令列工具和互動式殼層的預設方言。

如要進一步瞭解 `.bigqueryrc`，請參閱[設定指令專屬旗標預設值](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)的相關說明。

如要在 `.bigqueryrc` 中設定 `--use_legacy_sql=false`，請執行下列操作：

1. 在文字編輯器中開啟 `.bigqueryrc`。根據預設，`.bigqueryrc` 應位於您的使用者目錄中，例如 `$HOME/.bigqueryrc`。
2. 在檔案中加入以下文字。這個範例會將 GoogleSQL 設為查詢和 `mk` 指令 (建立檢視表時使用) 的預設語法。如果您已為 `query` 或 `mk` 指令旗標設定了預設值，則不必重新加入 `[query]` 或 `[mk]`。

   ```
   [query]
   --use_legacy_sql=false
   [mk]
   --use_legacy_sql=false
   ```
3. 儲存並關閉檔案。
4. 如果您使用的是互動式殼層，則必須結束並重新啟動，才能套用變更。

如要瞭解可用的指令列旗標，請參閱 [bq 指令列工具參考資料](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw)。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定操作說明進行操作。詳情請參閱 [BigQuery C# API 參考文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

根據預設，C# 程式庫會使用 GoogleSQL。

**切換至舊版 SQL 方言**

如要在查詢工作中使用舊版 SQL 語法，請將 `UseLegacySql` 參數設為 `true`。

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryQueryLegacy
{
    public void QueryLegacy(
        string projectId = "your-project-id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        string query = @"
            SELECT name FROM [bigquery-public-data:usa_names.usa_1910_2013]
            WHERE state = 'TX'
            LIMIT 100";
        BigQueryJob job = client.CreateQueryJob(
            sql: query,
            parameters: null,
            options: new QueryOptions { UseLegacySql = true });
        // Wait for the job to complete.
        job = job.PollUntilCompleted().ThrowOnAnyError();
        // Display the results
        foreach (BigQueryRow row in client.GetQueryResults(job.Reference))
        {
            Console.WriteLine($"{row["name"]}");
        }
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

根據預設，Go 用戶端程式庫會使用 GoogleSQL。

**切換至舊版 SQL 方言**

如要在查詢工作中使用舊版 SQL 語法，請將查詢設定中的 `UseLegacySQL` 屬性設為 `true`。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// queryLegacy demonstrates running a query using Legacy SQL.
func queryLegacy(w io.Writer, projectID, sqlString string) error {
	// projectID := "my-project-id"
	// sqlString = "SELECT 3 as somenum"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	q := client.Query(sqlString)
	q.UseLegacySQL = true

	// Run the query and process the returned row iterator.
	it, err := q.Read(ctx)
	if err != nil {
		return fmt.Errorf("query.Read(): %w", err)
	}
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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

根據預設，Java 用戶端程式庫會使用 GoogleSQL。

**切換至舊版 SQL 方言**

如要在查詢工作中使用舊版 SQL 語法，請將 `useLegacySql` 參數設為 `true`。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;

public class RunLegacyQuery {

  public static void main(String[] args) {
    runLegacyQuery();
  }

  public static void runLegacyQuery() {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // To use legacy SQL syntax, set useLegacySql to true.
      String query =
          "SELECT corpus FROM [bigquery-public-data:samples.shakespeare] GROUP BY corpus;";
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query).setUseLegacySql(true).build();

      // Execute the query.
      TableResult result = bigquery.query(queryConfig);

      // Print the results.
      result.iterateAll().forEach(rows -> rows.forEach(row -> System.out.println(row.getValue())));

      System.out.println("Legacy query ran successfully");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Legacy query did not run \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

根據預設，Node.js 用戶端程式庫會使用 GoogleSQL。

**切換至舊版 SQL 方言**

如要在查詢工作中使用舊版 SQL 語法，請將 `useLegacySql` 參數設為 `true`。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function queryLegacy() {
  // Queries the U.S. given names dataset for the state of Texas using legacy SQL.

  const query =
    'SELECT word FROM [bigquery-public-data:samples.shakespeare] LIMIT 10;';

  // For all options, see https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
  const options = {
    query: query,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
    useLegacySql: true,
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

根據預設，PHP 用戶端程式庫會使用 GoogleSQL。

**切換至舊版 SQL 方言**

如要在查詢工作中使用舊版 SQL 語法，請將 `useLegacySql` 參數設為 `true`。

```
use Google\Cloud\BigQuery\BigQueryClient;

/**
 * Query using legacy sql
 *
 * @param string $projectId The project Id of your Google Cloud Project.
 */
function query_legacy(string $projectId): void
{
    $query = 'SELECT corpus FROM [bigquery-public-data:samples.shakespeare] GROUP BY corpus';

    $bigQuery = new BigQueryClient([
      'projectId' => $projectId,
    ]);
    $jobConfig = $bigQuery->query($query)->useLegacySql(true);

    $queryResults = $bigQuery->runQuery($jobConfig);

    $i = 0;
    foreach ($queryResults as $row) {
        printf('--- Row %s ---' . PHP_EOL, ++$i);
        foreach ($row as $column => $value) {
            printf('%s: %s' . PHP_EOL, $column, json_encode($value));
        }
    }
    printf('Found %s row(s)' . PHP_EOL, $i);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

根據預設，Python 用戶端程式庫會使用 GoogleSQL。

**切換至舊版 SQL 方言**

如要在查詢工作中使用舊版 SQL 語法，請將 `use_legacy_sql` 參數設為 `True`。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

query = (
    "SELECT name FROM [bigquery-public-data:usa_names.usa_1910_2013] "
    'WHERE state = "TX" '
    "LIMIT 100"
)

# Set use_legacy_sql to True to use legacy SQL syntax.
job_config = bigquery.QueryJobConfig(use_legacy_sql=True)

# Start the query and waits for query job to complete, passing in the extra configuration.
results = client.query_and_wait(
    query, job_config=job_config
)  # Make an API request.

print("The query data:")
for row in results:
    print(row)
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定操作說明進行操作。詳情請參閱 [BigQuery Ruby API 參考文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

根據預設，Ruby 用戶端程式庫會使用 GoogleSQL。

**切換至舊版 SQL 方言**

如要在查詢工作中使用舊版 SQL 語法，請在查詢中傳遞 `legacy_sql: true` 選項。

```
require "google/cloud/bigquery"

def query_legacy
  bigquery = Google::Cloud::Bigquery.new
  sql = "SELECT name FROM [bigquery-public-data:usa_names.usa_1910_2013] " \
        "WHERE state = 'TX' " \
        "LIMIT 100"

  results = bigquery.query sql, legacy_sql: true do |config|
    # Location must match that of the dataset(s) referenced in the query.
    config.location = "US"
  end

  results.each do |row|
    puts row.inspect
  end
end
```

## 排解查詢相關問題

如要瞭解如何解決執行查詢時發生的問題，請參閱「[排解查詢問題](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw)」。

## 後續步驟

* 如要瞭解如何在 BigQuery 中執行 SQL 查詢，請參閱「[執行互動式和批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)」。
* 如要進一步瞭解查詢最佳化的一般資訊，請參閱「[查詢效能最佳化簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」。
* 如要瞭解在 BigQuery 中查詢資料時使用的 GoogleSQL 語法，請參閱「[查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)」。
* 如要進一步瞭解如何在查詢中使用管道語法，請參閱「[管道語法](https://docs.cloud.google.com/bigquery/docs/pipe-syntax?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]