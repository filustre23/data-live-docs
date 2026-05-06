Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 陣列參數 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用陣列參數執行查詢。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [執行參數化查詢](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw)

## 程式碼範例

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryQueryWithArrayParameters
{
    public void QueryWithArrayParameters(string projectId = "your-project-id")
    {
        var gender = "M";
        string[] states = { "WA", "WI", "WV", "WY" };

        // Note: Standard SQL is required to use query parameters.
        var query = @"
            SELECT name, sum(number) as count
            FROM `bigquery-public-data.usa_names.usa_1910_2013`
            WHERE gender = @gender
            AND state IN UNNEST(@states)
            GROUP BY name
            ORDER BY count DESC
            LIMIT 10;";

        // Initialize client that will be used to send requests.
        var client = BigQueryClient.Create(projectId);

        var parameters = new BigQueryParameter[]
        {
            new BigQueryParameter("gender", BigQueryDbType.String, gender),
            new BigQueryParameter("states", BigQueryDbType.Array, states)
        };

        var job = client.CreateQueryJob(
            sql: query,
            parameters: parameters,
            options: new QueryOptions { UseQueryCache = false });
        // Wait for the job to complete.
        job = job.PollUntilCompleted().ThrowOnAnyError();
        // Display the results
        foreach (BigQueryRow row in client.GetQueryResults(job.Reference))
        {
            Console.WriteLine($"{row["name"]}: {row["count"]}");
        }
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
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// queryWithArrayParams demonstrates issuing a query and specifying query parameters that include an
// array of strings.
func queryWithArrayParams(w io.Writer, projectID string) error {
	// projectID := "my-project-id"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	q := client.Query(
		`SELECT
			name,
			sum(number) as count 
        FROM ` + "`bigquery-public-data.usa_names.usa_1910_2013`" + `
		WHERE
			gender = @gender
        	AND state IN UNNEST(@states)
		GROUP BY
			name
		ORDER BY
			count DESC
		LIMIT 10;`)
	q.Parameters = []bigquery.QueryParameter{
		{
			Name:  "gender",
			Value: "M",
		},
		{
			Name:  "states",
			Value: []string{"WA", "WI", "WV", "WY"},
		},
	}
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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.QueryParameterValue;
import com.google.cloud.bigquery.TableResult;

// Sample to running a query with array query parameters.
public class QueryWithArrayParameters {

  public static void main(String[] args) {
    String gender = "M";
    String[] states = {"WA", "WI", "WV", "WY"};
    String query =
        "SELECT name, sum(number) as count\n"
            + "FROM `bigquery-public-data.usa_names.usa_1910_2013`\n"
            + "WHERE gender = @gender\n"
            + "AND state IN UNNEST(@states)\n"
            + "GROUP BY name\n"
            + "ORDER BY count DESC\n"
            + "LIMIT 10;";
    queryWithArrayParameters(query, gender, states);
  }

  public static void queryWithArrayParameters(String query, String gender, String[] states) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Note: Standard SQL is required to use query parameters.
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              .addNamedParameter("gender", QueryParameterValue.string(gender))
              .addNamedParameter("states", QueryParameterValue.array(states, String.class))
              .build();

      TableResult results = bigquery.query(queryConfig);

      // Print the results.
      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));
      System.out.println("Query with arrays parameters performed successfully");
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
// Run a query using array query parameters

// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function queryParamsArrays() {
  // The SQL query to run
  const sqlQuery = `SELECT name, sum(number) as count
  FROM \`bigquery-public-data.usa_names.usa_1910_2013\`
  WHERE gender = @gender
  AND state IN UNNEST(@states)
  GROUP BY name
  ORDER BY count DESC
  LIMIT 10;`;

  const options = {
    query: sqlQuery,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
    params: {gender: 'M', states: ['WA', 'WI', 'WV', 'WY']},
  };

  // Run the query
  const [rows] = await bigquery.query(options);

  console.log('Rows:');
  rows.forEach(row => console.log(row));
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

query = """
    SELECT name, sum(number) as count
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE gender = @gender
    AND state IN UNNEST(@states)
    GROUP BY name
    ORDER BY count DESC
    LIMIT 10;
"""
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("gender", "STRING", "M"),
        bigquery.ArrayQueryParameter("states", "STRING", ["WA", "WI", "WV", "WY"]),
    ]
)
rows = client.query_and_wait(query, job_config=job_config)  # Make an API request.

for row in rows:
    print("{}: \t{}".format(row.name, row.count))
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]