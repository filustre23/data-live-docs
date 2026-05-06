Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用 BigQuery API 執行查詢 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用 BigQuery 建立簡易應用程式。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [BigQuery API 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)
* [開始進行驗證](https://docs.cloud.google.com/bigquery/docs/authentication/getting-started?hl=zh-tw)
* [使用 BigQuery C# 用戶端程式庫查詢公開資料集](https://docs.cloud.google.com/walkthroughs/bigquery/csharp-client-library?hl=zh-tw)
* [使用 BigQuery 用戶端程式庫查詢公開資料集](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)
* [使用 BigQuery Go 用戶端程式庫查詢公開資料集](https://docs.cloud.google.com/walkthroughs/bigquery/go-client-library?hl=zh-tw)
* [使用 BigQuery Java 用戶端程式庫查詢公開資料集](https://docs.cloud.google.com/walkthroughs/bigquery/java-client-library?hl=zh-tw)
* [使用 BigQuery Node.js 用戶端程式庫查詢公開資料集](https://docs.cloud.google.com/walkthroughs/bigquery/node-client-library?hl=zh-tw)
* [使用 BigQuery PHP 用戶端程式庫查詢公開資料集](https://docs.cloud.google.com/walkthroughs/bigquery/php-client-library?hl=zh-tw)
* [使用 BigQuery Python 用戶端程式庫查詢公開資料集](https://docs.cloud.google.com/walkthroughs/bigquery/python-client-library?hl=zh-tw)
* [使用 BigQuery Ruby 用戶端程式庫查詢公開資料集](https://docs.cloud.google.com/walkthroughs/bigquery/ruby-client-library?hl=zh-tw)

## 程式碼範例

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using System;
using Google.Cloud.BigQuery.V2;

namespace GoogleCloudSamples
{
    public class Program
    {
        public static void Main(string[] args)
        {
            string projectId = Environment.GetEnvironmentVariable("GOOGLE_PROJECT_ID");
            var client = BigQueryClient.Create(projectId);
            string query = @"SELECT
                CONCAT(
                    'https://stackoverflow.com/questions/',
                    CAST(id as STRING)) as url, view_count
                FROM `bigquery-public-data.stackoverflow.posts_questions`
                WHERE tags like '%google-bigquery%'
                ORDER BY view_count DESC
                LIMIT 10";
            var result = client.ExecuteQuery(query, parameters: null);
            Console.Write("\nQuery Results:\n------------\n");
            foreach (var row in result)
            {
                Console.WriteLine($"{row["url"]}: {row["view_count"]} views");
            }
        }
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Command simpleapp queries the Stack Overflow public dataset in Google BigQuery.
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)


func main() {
	projectID := os.Getenv("GOOGLE_CLOUD_PROJECT")
	if projectID == "" {
		fmt.Println("GOOGLE_CLOUD_PROJECT environment variable must be set.")
		os.Exit(1)
	}

	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		log.Fatalf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	rows, err := query(ctx, client)
	if err != nil {
		log.Fatal(err)
	}
	if err := printResults(os.Stdout, rows); err != nil {
		log.Fatal(err)
	}
}

// query returns a row iterator suitable for reading query results.
func query(ctx context.Context, client *bigquery.Client) (*bigquery.RowIterator, error) {

	query := client.Query(
		`SELECT
			CONCAT(
				'https://stackoverflow.com/questions/',
				CAST(id as STRING)) as url,
			view_count
		FROM ` + "`bigquery-public-data.stackoverflow.posts_questions`" + `
		WHERE tags like '%google-bigquery%'
		ORDER BY view_count DESC
		LIMIT 10;`)
	return query.Read(ctx)
}

type StackOverflowRow struct {
	URL       string `bigquery:"url"`
	ViewCount int64  `bigquery:"view_count"`
}

// printResults prints results from a query to the Stack Overflow public dataset.
func printResults(w io.Writer, iter *bigquery.RowIterator) error {
	for {
		var row StackOverflowRow
		err := iter.Next(&row)
		if err == iterator.Done {
			return nil
		}
		if err != nil {
			return fmt.Errorf("error iterating through results: %w", err)
		}

		fmt.Fprintf(w, "url: %s views: %d\n", row.URL, row.ViewCount)
	}
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FieldValueList;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobId;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;


public class SimpleApp {

  public static void main(String... args) throws Exception {
    // TODO(developer): Replace these variables before running the app.
    String projectId = "MY_PROJECT_ID";
    simpleApp(projectId);
  }

  public static void simpleApp(String projectId) {
    try {
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(
                  "SELECT CONCAT('https://stackoverflow.com/questions/', "
                      + "CAST(id as STRING)) as url, view_count "
                      + "FROM `bigquery-public-data.stackoverflow.posts_questions` "
                      + "WHERE tags like '%google-bigquery%' "
                      + "ORDER BY view_count DESC "
                      + "LIMIT 10")
              // Use standard SQL syntax for queries.
              // See: https://cloud.google.com/bigquery/sql-reference/
              .setUseLegacySql(false)
              .build();

      JobId jobId = JobId.newBuilder().setProject(projectId).build();
      Job queryJob = bigquery.create(JobInfo.newBuilder(queryConfig).setJobId(jobId).build());

      // Wait for the query to complete.
      queryJob = queryJob.waitFor();

      // Check for errors
      if (queryJob == null) {
        throw new RuntimeException("Job no longer exists");
      } else if (queryJob.getStatus().getExecutionErrors() != null
          && queryJob.getStatus().getExecutionErrors().size() > 0) {
        // TODO(developer): Handle errors here. An error here do not necessarily mean that the job
        // has completed or was unsuccessful.
        // For more details: https://cloud.google.com/bigquery/troubleshooting-errors
        throw new RuntimeException("An unhandled error has occurred");
      }

      // Get the results.
      TableResult result = queryJob.getQueryResults();

      // Print all pages of the results.
      for (FieldValueList row : result.iterateAll()) {
        // String type
        String url = row.get("url").getStringValue();
        String viewCount = row.get("view_count").getStringValue();
        System.out.printf("%s : %s views\n", url, viewCount);
      }
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Simple App failed due to error: \n" + e.toString());
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

async function queryStackOverflow() {
  // Queries a public Stack Overflow dataset.

  // Create a client
  const bigqueryClient = new BigQuery();

  // The SQL query to run
  const sqlQuery = `SELECT
    CONCAT(
      'https://stackoverflow.com/questions/',
      CAST(id as STRING)) as url,
    view_count
    FROM \`bigquery-public-data.stackoverflow.posts_questions\`
    WHERE tags like '%google-bigquery%'
    ORDER BY view_count DESC
    LIMIT 10`;

  const options = {
    query: sqlQuery,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
  };

  // Run the query
  const [rows] = await bigqueryClient.query(options);

  console.log('Query Results:');
  rows.forEach(row => {
    const url = row['url'];
    const viewCount = row['view_count'];
    console.log(`url: ${url}, ${viewCount} views`);
  });
}
queryStackOverflow();
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
<?php
# ...

require __DIR__ . '/vendor/autoload.php';

use Google\Cloud\BigQuery\BigQueryClient;


$bigQuery = new BigQueryClient();
$query = <<<ENDSQL
SELECT
  CONCAT(
    'https://stackoverflow.com/questions/',
    CAST(id as STRING)) as url,
  view_count
FROM `bigquery-public-data.stackoverflow.posts_questions`
WHERE tags like '%google-bigquery%'
ORDER BY view_count DESC
LIMIT 10;
ENDSQL;
$queryJobConfig = $bigQuery->query($query);
$queryResults = $bigQuery->runQuery($queryJobConfig);

if ($queryResults->isComplete()) {
    $i = 0;
    $rows = $queryResults->rows();
    foreach ($rows as $row) {
        printf('--- Row %s ---' . PHP_EOL, ++$i);
        printf('url: %s, %s views' . PHP_EOL, $row['url'], $row['view_count']);
    }
    printf('Found %s row(s)' . PHP_EOL, $i);
} else {
    throw new Exception('The query failed to complete');
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery



def query_stackoverflow() -> None:
    client = bigquery.Client()
    results = client.query_and_wait(
        """
        SELECT
          CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
          view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
        LIMIT 10"""
    )  # Waits for job to complete.

    for row in results:
        print("{} : {} views".format(row.url, row.view_count))


if __name__ == "__main__":
    query_stackoverflow()
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

# This uses Application Default Credentials to authenticate.
# @see https://cloud.google.com/bigquery/docs/authentication/getting-started
bigquery = Google::Cloud::Bigquery.new

sql     = "SELECT " \
          "CONCAT('https://stackoverflow.com/questions/', CAST(id as STRING)) as url, view_count " \
          "FROM `bigquery-public-data.stackoverflow.posts_questions` " \
          "WHERE tags like '%google-bigquery%' " \
          "ORDER BY view_count DESC LIMIT 10"
results = bigquery.query sql

results.each do |row|
  puts "#{row[:url]}: #{row[:view_count]} views"
end
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]