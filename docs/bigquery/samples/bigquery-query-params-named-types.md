Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 已命名參數和指定類型 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用具名參數和指定參數類型執行查詢。

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

// Sample to run query with named types parameters.
public class QueryWithNamedTypesParameters {

  public static void main(String[] args) {
    String[] words = {"and", "is", "the", "moon"};
    String corpus = "romeoandjuliet";
    Integer wordsCount = 250;
    String query =
        "SELECT word, word_count"
            + " FROM `bigquery-public-data.samples.shakespeare`"
            + " WHERE word IN UNNEST(@wordList)"
            + " AND corpus = @corpus"
            + " AND word_count >= @minWordCount"
            + " ORDER BY word_count DESC";
    queryWithNamedTypesParameters(query, words, corpus, wordsCount);
  }

  public static void queryWithNamedTypesParameters(
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
              .addNamedParameter("wordList", wordList)
              .addNamedParameter("corpus", corpusParam)
              .addNamedParameter("minWordCount", minWordCount)
              .build();

      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query with named types parameters performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

### Rust

```
use google_cloud_bigquery::client::BigQuery;
use google_cloud_bigquery::model::{QueryParameter, QueryParameterType, QueryParameterValue};

pub async fn sample(project_id: &str) -> anyhow::Result<()> {
    let client = BigQuery::builder().build().await?;

    let mut rows = client
        .query(
            "SELECT \
        @date_param AS date_col, \
        @numeric_param AS num_col, \
        @bool_param AS bool_col;",
        )
        .with_project_id(project_id)
        .set_parameter_mode("NAMED")
        .set_query_parameters([
            QueryParameter::new()
                .set_name("date_param")
                .set_parameter_type(QueryParameterType::new().set_type("DATE"))
                .set_parameter_value(QueryParameterValue::new().set_value("2026-01-15")),
            QueryParameter::new()
                .set_name("numeric_param")
                .set_parameter_type(QueryParameterType::new().set_type("NUMERIC"))
                .set_parameter_value(QueryParameterValue::new().set_value("12345.67")),
            QueryParameter::new()
                .set_name("bool_param")
                .set_parameter_type(QueryParameterType::new().set_type("BOOL"))
                .set_parameter_value(QueryParameterValue::new().set_value("true")),
        ])
        .set_location("US")
        .run()
        .await?
        .until_done()
        .await?
        .read();

    while let Some(row) = rows.next().await.transpose()? {
        let date_col: String = row.get("date_col");
        let num_col: String = row.get("num_col");
        let bool_col: bool = row.get("bool_col");
        println!("Date: {date_col}, Numeric: {num_col}, Bool: {bool_col}");
    }
    Ok(())
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]