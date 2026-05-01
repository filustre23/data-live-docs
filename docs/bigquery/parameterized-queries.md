* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 執行參數化查詢

使用 GoogleSQL 語法查詢 BigQuery 資料時，您可以運用參數保護查詢，避免使用者輸入內容遭到 [SQL 注入](https://en.wikipedia.org/wiki/SQL_injection)。參數會取代 GoogleSQL 查詢中的任意運算式。

您可以傳遞各種資料類型的查詢參數，包括：

* 陣列
* 時間戳記
* 結構體
* 範圍

## 在查詢中傳遞參數

查詢參數僅支援 [GoogleSQL 語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql?hl=zh-tw)。參數不可取代 ID、資料欄名稱、資料表名稱，或是查詢的其他部分。

如要指定具名參數，請使用 `@` 字元，後面加上 [ID](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#identifiers)，例如 `@param_name`。或者，您可以使用預留位置值 `?` 來指定位置參數。查詢可以使用位置或已命名參數，但不得同時使用這兩者。

**注意：** 為保護可能含有私密資訊的資料，當您使用參數執行查詢時，BigQuery [記錄](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw#logs)不會記錄參數值。

您可以在 BigQuery 中透過下列方式執行參數化查詢：

* Google Cloud 控制台中的 BigQuery Studio 查詢編輯器
* bq 指令列工具的 `bq query` 指令
* API
* 用戶端程式庫

以下範例說明如何將參數值傳遞至參數化查詢：

### 控制台

如要在 Google Cloud 控制台中執行參數化查詢，請在「查詢設定」中設定參數，然後在 SQL 查詢中參照這些參數，方法是在每個參數名稱前面加上 `@` 字元。

**支援的資料類型**： Google Cloud 控制台僅支援原始資料類型的參數化查詢，例如 `BIGNUMERIC`、`BOOL`、`BYTES`、`DATE`、`DATETIME`、`FLOAT64`、`GEOGRAPHY`、`INT64`、`INTERVAL`、`NUMERIC`、`STRING`、`TIME` 或 `TIMESTAMP`。 Google Cloud 控制台不支援複雜的資料類型，例如 `ARRAY` 和 `STRUCT`。

## 在 Google Cloud 控制台中新增參數

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器工具列中，按一下 settings「更多」，然後選取「查詢設定」。
3. 在「查詢設定」窗格中，找到「查詢參數」部分，然後按一下「新增參數」。
4. 請為查詢中的每個參數提供下列資訊：

   * **名稱**：輸入參數名稱 (請勿加入 `@` 字元)。
   * **類型**：選取參數的資料類型。
   * **值**：輸入要用於這次執行的值。
5. 按一下 [儲存]。

## 在 Google Cloud 控制台中將參數值傳遞至查詢

1. 在查詢編輯器中，使用您在上一步設定的參數輸入 SQL 查詢。如要參照這些變數，請在名稱前加上 `@` 字元，如範例所示。

   **範例**：

   ```
   SELECT
       word,
       word_count
     FROM
       `bigquery-public-data.samples.shakespeare`
     WHERE
       corpus = @corpus
     AND
       word_count >= @min_word_count
     ORDER BY
       word_count DESC;
   ```

   在這個範例中，您會將 `corpus` 參數新增為 `STRING`，並將值設為 `romeoandjuliet`，然後將 `min_word_count` 參數新增為 `INT64`，並將值設為 `250`。

   如果查詢缺少參數或參數無效，系統會顯示錯誤訊息。按一下錯誤訊息中的「設定參數」，即可調整參數設定。
2. 如要在查詢編輯器中執行參數化查詢，請按一下「執行」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 請使用 `--parameter`，以 `name:type:value` 的格式來提供參數的值。如果名稱留白，會產生位置參數。如果您省略類型，系統會假設類型是 `STRING`。

   `--parameter` 標記必須與標記 `--use_legacy_sql=false` 一起使用，以便指定 GoogleSQL 語法。

   (選用) 使用 `--location` 標記指定您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

   ```
   bq query \
      --use_legacy_sql=false \
      --parameter=corpus::romeoandjuliet \
      --parameter=min_word_count:INT64:250 \
      'SELECT
        word,
        word_count
      FROM
        `bigquery-public-data.samples.shakespeare`
      WHERE
        corpus = @corpus
      AND
        word_count >= @min_word_count
      ORDER BY
        word_count DESC;'
   ```

### API

如要使用已命名參數，請將 `query` 工作設定中的 `parameterMode` 設定為 `NAMED`。

請利用 `query` 工作設定中的參數清單填入 `queryParameters`。請利用查詢中所用的 `@param_name` 來設定每個參數的 `name`。

請將 `useLegacySql` 設定為 `false` 來[啟用 GoogleSQL 語法](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。

```
{
  "query": "SELECT word, word_count FROM `bigquery-public-data.samples.shakespeare` WHERE corpus = @corpus AND word_count >= @min_word_count ORDER BY word_count DESC;",
  "queryParameters": [
    {
      "parameterType": {
        "type": "STRING"
      },
      "parameterValue": {
        "value": "romeoandjuliet"
      },
      "name": "corpus"
    },
    {
      "parameterType": {
        "type": "INT64"
      },
      "parameterValue": {
        "value": "250"
      },
      "name": "min_word_count"
    }
  ],
  "useLegacySql": false,
  "parameterMode": "NAMED"
}
```

[在 Google APIs Explorer 中嘗試這個範例](https://developers.google.com/apis-explorer/?hl=zh-tw#p/bigquery/v2/bigquery.jobs.query?projectId=my-project-id&_h=1&resource=%257B%250A++%2522query%2522%253A+%2522SELECT+word%252C+word_count%255CnFROM+%2560bigquery-public-data.samples.shakespeare%2560%255CnWHERE+corpus+%253D+%2540corpus%255CnAND+word_count+%253E%253D+%2540min_word_count%255CnORDER+BY+word_count+DESC%253B%2522%252C%250A++%2522queryParameters%2522%253A+%250A++%255B%250A++++%257B%250A++++++%2522parameterType%2522%253A+%250A++++++%257B%250A++++++++%2522type%2522%253A+%2522STRING%2522%250A++++++%257D%252C%250A++++++%2522parameterValue%2522%253A+%250A++++++%257B%250A++++++++%2522value%2522%253A+%2522romeoandjuliet%2522%250A++++++%257D%252C%250A++++++%2522name%2522%253A+%2522corpus%2522%250A++++%257D%252C%250A++++%257B%250A++++++%2522parameterType%2522%253A+%250A++++++%257B%250A++++++++%2522type%2522%253A+%2522INT64%2522%250A++++++%257D%252C%250A++++++%2522parameterValue%2522%253A+%250A++++++%257B%250A++++++++%2522value%2522%253A+%2522250%2522%250A++++++%257D%252C%250A++++++%2522name%2522%253A+%2522min_word_count%2522%250A++++%257D%250A++%255D%252C%250A++%2522useLegacySql%2522%253A+false%252C%250A++%2522parameterMode%2522%253A+%2522NAMED%2522%250A%257D&)。

如要使用位置參數，請將 `query` 工作設定中的 `parameterMode` 設定為 `POSITIONAL`。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要使用已命名參數：

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryQueryWithNamedParameters
{
    public void QueryWithNamedParameters(string projectId = "your-project-id")
    {
        var corpus = "romeoandjuliet";
        var minWordCount = 250;

        // Note: Standard SQL is required to use query parameters.
        var query = @"
            SELECT word, word_count
            FROM `bigquery-public-data.samples.shakespeare`
            WHERE corpus = @corpus
            AND word_count >= @min_word_count
            ORDER BY word_count DESC";

        // Initialize client that will be used to send requests.
        var client = BigQueryClient.Create(projectId);

        var parameters = new BigQueryParameter[]
        {
            new BigQueryParameter("corpus", BigQueryDbType.String, corpus),
            new BigQueryParameter("min_word_count", BigQueryDbType.Int64, minWordCount)
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
            Console.WriteLine($"{row["word"]}: {row["word_count"]}");
        }
    }
}
```

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要使用位置參數：

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryQueryWithPositionalParameters
{
    public void QueryWithPositionalParameters(string projectId = "project-id")
    {
        var corpus = "romeoandjuliet";
        var minWordCount = 250;

        // Note: Standard SQL is required to use query parameters.
        var query = @"
                SELECT word, word_count
                FROM `bigquery-public-data.samples.shakespeare`
                WHERE corpus = ?
                AND word_count >= ?
                ORDER BY word_count DESC;";

        // Initialize client that will be used to send requests.
        var client = BigQueryClient.Create(projectId);

        // Set the name to None to use positional parameters.
        // Note that you cannot mix named and positional parameters.
        var parameters = new BigQueryParameter[]
        {
            new BigQueryParameter(null, BigQueryDbType.String, corpus),
            new BigQueryParameter(null, BigQueryDbType.Int64, minWordCount)
        };

        var job = client.CreateQueryJob(
            sql: query,
            parameters: parameters,
            options: new QueryOptions
            {
                UseQueryCache = false,
                ParameterMode = BigQueryParameterMode.Positional
            });
        // Wait for the job to complete.
        job = job.PollUntilCompleted().ThrowOnAnyError();
        // Display the results
        foreach (BigQueryRow row in client.GetQueryResults(job.Reference))
        {
            Console.WriteLine($"{row["word"]}: {row["word_count"]}");
        }
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要使用已命名參數：

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// queryWithNamedParams demonstrate issuing a query using named query parameters.
func queryWithNamedParams(w io.Writer, projectID string) error {
	// projectID := "my-project-id"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	q := client.Query(
		`SELECT word, word_count
        FROM ` + "`bigquery-public-data.samples.shakespeare`" + `
        WHERE corpus = @corpus
        AND word_count >= @min_word_count
        ORDER BY word_count DESC;`)
	q.Parameters = []bigquery.QueryParameter{
		{
			Name:  "corpus",
			Value: "romeoandjuliet",
		},
		{
			Name:  "min_word_count",
			Value: 250,
		},
	}
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

如要使用位置參數：

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// queryWithPostionalParams demonstrate issuing a query using positional query parameters.
func queryWithPositionalParams(w io.Writer, projectID string) error {
	// projectID := "my-project-id"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	q := client.Query(
		`SELECT word, word_count
        FROM ` + "`bigquery-public-data.samples.shakespeare`" + `
        WHERE corpus = ?
        AND word_count >= ?
        ORDER BY word_count DESC;`)
	q.Parameters = []bigquery.QueryParameter{
		{
			Value: "romeoandjuliet",
		},
		{
			Value: 250,
		},
	}
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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要使用已命名參數：

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.QueryParameterValue;
import com.google.cloud.bigquery.TableResult;

public class QueryWithNamedParameters {

  public static void queryWithNamedParameters() {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      String corpus = "romeoandjuliet";
      long minWordCount = 250;
      String query =
          "SELECT word, word_count\n"
              + "FROM `bigquery-public-data.samples.shakespeare`\n"
              + "WHERE corpus = @corpus\n"
              + "AND word_count >= @min_word_count\n"
              + "ORDER BY word_count DESC";

      // Note: Standard SQL is required to use query parameters.
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              .addNamedParameter("corpus", QueryParameterValue.string(corpus))
              .addNamedParameter("min_word_count", QueryParameterValue.int64(minWordCount))
              .build();

      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query with named parameters performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

如要使用位置參數：

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.QueryParameterValue;
import com.google.cloud.bigquery.TableResult;

public class QueryWithPositionalParameters {
  public static void queryWithPositionalParameters() {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      String corpus = "romeoandjuliet";
      long minWordCount = 250;
      String query =
          "SELECT word, word_count\n"
              + "FROM `bigquery-public-data.samples.shakespeare`\n"
              + "WHERE corpus = ?\n"
              + "AND word_count >= ?\n"
              + "ORDER BY word_count DESC";

      // Note: Standard SQL is required to use query parameters.
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              .addPositionalParameter(QueryParameterValue.string(corpus))
              .addPositionalParameter(QueryParameterValue.int64(minWordCount))
              .build();

      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query with positional parameters performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要使用已命名參數：

```
// Run a query using named query parameters

// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function queryParamsNamed() {
  // The SQL query to run
  const sqlQuery = `SELECT word, word_count
        FROM \`bigquery-public-data.samples.shakespeare\`
        WHERE corpus = @corpus
        AND word_count >= @min_word_count
        ORDER BY word_count DESC`;

  const options = {
    query: sqlQuery,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
    params: {corpus: 'romeoandjuliet', min_word_count: 250},
  };

  // Run the query
  const [rows] = await bigquery.query(options);

  console.log('Rows:');
  rows.forEach(row => console.log(row));
}
```

如要使用位置參數：

```
// Run a query using positional query parameters

// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function queryParamsPositional() {
  // The SQL query to run
  const sqlQuery = `SELECT word, word_count
        FROM \`bigquery-public-data.samples.shakespeare\`
        WHERE corpus = ?
        AND word_count >= ?
        ORDER BY word_count DESC`;

  const options = {
    query: sqlQuery,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
    params: ['romeoandjuliet', 250],
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

如要使用已命名參數：

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

query = """
    SELECT word, word_count
    FROM `bigquery-public-data.samples.shakespeare`
    WHERE corpus = @corpus
    AND word_count >= @min_word_count
    ORDER BY word_count DESC;
"""
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("corpus", "STRING", "romeoandjuliet"),
        bigquery.ScalarQueryParameter("min_word_count", "INT64", 250),
    ]
)
results = client.query_and_wait(
    query, job_config=job_config
)  # Make an API request.

for row in results:
    print("{}: \t{}".format(row.word, row.word_count))
```

如要使用位置參數：

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

query = """
    SELECT word, word_count
    FROM `bigquery-public-data.samples.shakespeare`
    WHERE corpus = ?
    AND word_count >= ?
    ORDER BY word_count DESC;
"""
# Set the name to None to use positional parameters.
# Note that you cannot mix named and positional parameters.
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter(None, "STRING", "romeoandjuliet"),
        bigquery.ScalarQueryParameter(None, "INT64", 250),
    ]
)
results = client.query_and_wait(
    query, job_config=job_config
)  # Make an API request.

for row in results:
    print("{}: \t{}".format(row.word, row.word_count))
```

## 在參數化查詢中使用陣列

如要在查詢參數中使用陣列類型，請將類型設定為 `ARRAY<T>`，其中 `T` 是陣列中元素的類型。請將值建構為以方括號括住的元素清單，其中的元素以逗號分隔，例如 `[1, 2,
3]`。

如要進一步瞭解陣列類型，請參閱[資料類型參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type)。

### 控制台

Google Cloud 控制台不支援參數化查詢中的陣列。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 這項查詢會針對在美國出生的男嬰，挑出開頭為英文字母 W 的姓名中最受歡迎的：

   **注意：**這個範例查詢的是以美國為基礎的公開資料集。由於該公開資料集儲存在美國的多地區位置，因此您目的地資料表所屬的資料集也必須位於美國。您無法查詢位於某個位置的資料集，然後將結果寫入位於另一個位置的目的地資料表。 

   ```
   bq query \
      --use_legacy_sql=false \
      --parameter='gender::M' \
      --parameter='states:ARRAY<STRING>:["WA", "WI", "WV", "WY"]' \
      'SELECT
        name,
        SUM(number) AS count
      FROM
        `bigquery-public-data.usa_names.usa_1910_2013`
      WHERE
        gender = @gender
        AND state IN UNNEST(@states)
      GROUP BY
        name
      ORDER BY
        count DESC
      LIMIT
        10;'
   ```

   請小心地用單引號括住陣列類型宣告，以免 `>` 字元意外地將指令輸出重新導向至某個檔案。

### API

如要使用陣列值參數，請將 `query` 工作設定中的 [`parameterType`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/QueryParameter?hl=zh-tw) 設定為 `ARRAY`。

如果陣列值是純量，請將 [`parameterType`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/QueryParameter?hl=zh-tw) 設定為值的類型，例如 `STRING`。如果陣列值是結構，請將參數類型設定為 `STRUCT`，並將所需的欄位定義新增至 `structTypes`。

舉例來說，下列查詢會針對在美國出生的男嬰，挑出開頭為英文字母 W 的姓名中最受歡迎的。

```
{
 "query": "SELECT name, sum(number) as count\nFROM `bigquery-public-data.usa_names.usa_1910_2013`\nWHERE gender = @gender\nAND state IN UNNEST(@states)\nGROUP BY name\nORDER BY count DESC\nLIMIT 10;",
 "queryParameters": [
  {
   "parameterType": {
    "type": "STRING"
   },
   "parameterValue": {
    "value": "M"
   },
   "name": "gender"
  },
  {
   "parameterType": {
    "type": "ARRAY",
    "arrayType": {
     "type": "STRING"
    }
   },
   "parameterValue": {
    "arrayValues": [
     {
      "value": "WA"
     },
     {
      "value": "WI"
     },
     {
      "value": "WV"
     },
     {
      "value": "WY"
     }
    ]
   },
   "name": "states"
  }
 ],
 "useLegacySql": false,
 "parameterMode": "NAMED"
}
```

[在 Google APIs Explorer 中嘗試這個範例](https://developers.google.com/apis-explorer/?hl=zh-tw#p/bigquery/v2/bigquery.jobs.query?projectId=my-project-id&_h=1&resource=%257B%250A++%2522query%2522%253A+%2522SELECT+name%252C+sum(number)+as+count%255CnFROM+%2560bigquery-public-data.usa_names.usa_1910_2013%2560%255CnWHERE+gender+%253D+%2540gender%255CnAND+state+IN+UNNEST(%2540states)%255CnGROUP+BY+name%255CnORDER+BY+count+DESC%255CnLIMIT+10%253B%2522%252C%250A++%2522queryParameters%2522%253A+%250A++%255B%250A++++%257B%250A++++++%2522parameterType%2522%253A+%250A++++++%257B%250A++++++++%2522type%2522%253A+%2522STRING%2522%250A++++++%257D%252C%250A++++++%2522parameterValue%2522%253A+%250A++++++%257B%250A++++++++%2522value%2522%253A+%2522M%2522%250A++++++%257D%252C%250A++++++%2522name%2522%253A+%2522gender%2522%250A++++%257D%252C%250A++++%257B%250A++++++%2522parameterType%2522%253A+%250A++++++%257B%250A++++++++%2522type%2522%253A+%2522ARRAY%2522%252C%250A++++++++%2522arrayType%2522%253A+%250A++++++++%257B%250A++++++++++%2522type%2522%253A+%2522STRING%2522%250A++++++++%257D%250A++++++%257D%252C%250A++++++%2522parameterValue%2522%253A+%250A++++++%257B%250A++++++++%2522arrayValues%2522%253A+%250A++++++++%255B%250A++++++++++%257B%250A++++++++++++%2522value%2522%253A+%2522WA%2522%250A++++++++++%257D%252C%250A++++++++++%257B%250A++++++++++++%2522value%2522%253A+%2522WI%2522%250A++++++++++%257D%252C%250A++++++++++%257B%250A++++++++++++%2522value%2522%253A+%2522WV%2522%250A++++++++++%257D%252C%250A++++++++++%257B%250A++++++++++++%2522value%2522%253A+%2522WY%2522%250A++++++++++%257D%250A++++++++%255D%250A++++++%257D%252C%250A++++++%2522name%2522%253A+%2522states%2522%250A++++%257D%250A++%255D%252C%250A++%2522useLegacySql%2522%253A+false%252C%250A++%2522parameterMode%2522%253A+%2522NAMED%2522%250A%257D&)。

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
		return fmt.Errorf("bigquery.NewClient: %v", err)
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

  public static void runQueryWithArrayParameters() {
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
              .addNamedParameter("states", QueryParameterValue.
```