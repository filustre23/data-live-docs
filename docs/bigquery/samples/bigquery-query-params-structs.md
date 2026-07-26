Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 結構參數 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用結構體參數執行查詢。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [執行參數化查詢](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw)

## 程式碼範例

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

// queryWithStructParam demonstrates running a query and providing query parameters that include struct
// types.
func queryWithStructParam(w io.Writer, projectID string) error {
	// projectID := "my-project-id"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	type MyStruct struct {
		X int64
		Y string
	}
	q := client.Query(
		`SELECT @struct_value as s;`)
	q.Parameters = []bigquery.QueryParameter{
		{
			Name:  "struct_value",
			Value: MyStruct{X: 1, Y: "foo"},
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
import java.util.HashMap;
import java.util.Map;

public class QueryWithStructsParameters {

  public static void main(String[] args) {
    queryWithStructsParameters();
  }

  public static void queryWithStructsParameters() {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Create struct
      Map<String, QueryParameterValue> struct = new HashMap<>();
      struct.put("x", QueryParameterValue.int64(1));
      struct.put("y", QueryParameterValue.string("foo"));
      QueryParameterValue recordValue = QueryParameterValue.struct(struct);

      String query = "SELECT STRUCT(@recordField) AS s";
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              .addNamedParameter("recordField", recordValue)
              .build();

      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s", val.toString())));

      System.out.println("Query with struct parameter performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

### Rust

```
use google_cloud_bigquery::FromRow;
use google_cloud_bigquery::client::BigQuery;
use google_cloud_bigquery::model::{
    QueryParameter, QueryParameterStructType, QueryParameterType, QueryParameterValue,
};

#[derive(FromRow, Debug)]
struct NameCount {
    name: String,
    number: i64,
}

pub async fn sample(project_id: &str) -> anyhow::Result<()> {
    let client = BigQuery::builder().build().await?;

    let mut rows = client
        .query(
            "SELECT name, number \
        FROM `bigquery-public-data.usa_names.usa_1910_2013` \
        WHERE state = @record.state AND gender = @record.gender \
        LIMIT 10",
        )
        .with_project_id(project_id)
        .set_parameter_mode("NAMED")
        .set_query_parameters([QueryParameter::new()
            .set_name("record")
            .set_parameter_type(
                QueryParameterType::new()
                    .set_type("STRUCT")
                    .set_struct_types([
                        QueryParameterStructType::new()
                            .set_name("state")
                            .set_type(QueryParameterType::new().set_type("STRING")),
                        QueryParameterStructType::new()
                            .set_name("gender")
                            .set_type(QueryParameterType::new().set_type("STRING")),
                    ]),
            )
            .set_parameter_value(QueryParameterValue::new().set_struct_values([
                ("state", QueryParameterValue::new().set_value("TX")),
                ("gender", QueryParameterValue::new().set_value("F")),
            ]))])
        .set_location("US")
        .run()
        .await?
        .until_done()
        .await?
        .read();

    while let Some(row) = rows.next().await.transpose()? {
        let name_count: NameCount = row.try_into()?;
        println!("Name: {}, Number: {}", name_count.name, name_count.number);
    }
    Ok(())
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]