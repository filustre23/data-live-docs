* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 位置參數和指定類型 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用位置參數和指定的參數類型執行查詢。

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.QueryParameterValue;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.TableResult;

// Sample to run query with positional types parameters.
public class QueryWithPositionalTypesParameters {

  public static void main(String[] args) {
    String[] words = {"and", "is", "the", "moon"};
    String corpus = "romeoandjuliet";
    Integer wordsCount = 250;
    String query =
        "SELECT word, word_count"
            + " FROM `bigquery-public-data.samples.shakespeare`"
            + " WHERE word IN UNNEST(?)"
            + " AND corpus = ?"
            + " AND word_count >= ?"
            + " ORDER BY word_count DESC";
    queryWithPositionalTypesParameters(query, words, corpus, wordsCount);
  }

  public static void queryWithPositionalTypesParameters(
      String query, String[] words, String corpus, Integer wordsCount) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      QueryParameterValue wordList = QueryParameterValue.array(words, StandardSQLTypeName.STRING);
      QueryParameterValue corpusParam = QueryParameterValue.of(corpus, StandardSQLTypeName.STRING);
      QueryParameterValue minWordCount =
          QueryParameterValue.of(wordsCount, StandardSQLTypeName.INT64);

      // Note: Standard SQL is required to use query parameters.
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              .addPositionalParameter(wordList)
              .addPositionalParameter(corpusParam)
              .addPositionalParameter(minWordCount)
              .build();

      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query with positional types parameters performed successfully.");
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
const bigquery = new BigQuery();

async function queryParamsPositionalTypes() {
  // Run a query using positional query parameters and provided parameter types.

  // The SQL query to run
  const sqlQuery = `SELECT word, word_count
  FROM \`bigquery-public-data.samples.shakespeare\`
  WHERE word IN UNNEST(?)
  AND corpus = ?
  AND word_count >= ?
  ORDER BY word_count DESC`;

  const queryOptions = {
    query: sqlQuery,
    params: [['and', 'is', 'the', 'moon'], 'romeoandjuliet', 250],
    types: [['STRING'], 'STRING', 'INT64'],
  };

  // Run the query
  const [rows] = await bigquery.query(queryOptions);

  console.log('Rows:');
  rows.forEach(row => console.log(row));
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]