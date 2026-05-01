* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 建立 materialized view 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

建立 materialized view。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [建立具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// createMaterializedView demonstrates generated a materialized view based on an existing
// base table.
func createMaterializedView(projectID, datasetID, baseTableID, viewID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydatasetid"
	// baseTableID := "mytableid"
	// viewID := "myviewid"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	// Get an appropriately escaped table identifier suitable for use in a standard SQL query.
	tableStr, err := client.Dataset(datasetID).Table(baseTableID).Identifier(bigquery.StandardSQLID)
	if err != nil {
		return fmt.Errorf("couldn't construct identifier: %w", err)
	}

	metaData := &bigquery.TableMetadata{
		MaterializedView: &bigquery.MaterializedViewDefinition{
			Query: fmt.Sprintf(`SELECT MAX(TimestampField) AS TimestampField, StringField, 
					  MAX(BooleanField) AS BooleanField FROM %s GROUP BY StringField`, tableStr),
		}}

	viewRef := client.Dataset(datasetID).Table(viewID)
	if err := viewRef.Create(ctx, metaData); err != nil {
		return err
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
import com.google.cloud.bigquery.MaterializedViewDefinition;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;

// Sample to create materialized view
public class CreateMaterializedView {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String materializedViewName = "MY_MATERIALIZED_VIEW_NAME";
    String query =
        String.format(
            "SELECT MAX(TimestampField) AS TimestampField, StringField, "
                + "MAX(BooleanField) AS BooleanField "
                + "FROM %s.%s GROUP BY StringField",
            datasetName, tableName);
    createMaterializedView(datasetName, materializedViewName, query);
  }

  public static void createMaterializedView(
      String datasetName, String materializedViewName, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, materializedViewName);

      MaterializedViewDefinition materializedViewDefinition =
          MaterializedViewDefinition.newBuilder(query).build();

      bigquery.create(TableInfo.of(tableId, materializedViewDefinition));
      System.out.println("Materialized view created successfully");
    } catch (BigQueryException e) {
      System.out.println("Materialized view was not created. \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

bigquery_client = bigquery.Client()

view_id = "my-project.my_dataset.my_materialized_view"
base_table_id = "my-project.my_dataset.my_base_table"
view = bigquery.Table(view_id)
view.mview_query = f"""
SELECT product_id, SUM(clicks) AS sum_clicks
FROM  `{base_table_id}`
GROUP BY 1
"""

# Make an API request to create the materialized view.
view = bigquery_client.create_table(view)
print(f"Created {view.table_type}: {str(view.reference)}")
```

### Terraform

如要瞭解如何套用或移除 Terraform 設定，請參閱「[基本 Terraform 指令](https://docs.cloud.google.com/docs/terraform/basic-commands?hl=zh-tw)」。詳情請參閱 [Terraform 供應商參考文件](https://registry.terraform.io/providers/hashicorp/google/latest/docs)。

```
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "mydataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

  labels = {
    billing_group = "accounting",
    pii           = "sensitive"
  }
}

resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = "my_materialized_view"

  materialized_view {
    query                            = "SELECT ID, description, date_created FROM `myproject.orders.items`"
    enable_refresh                   = "true"
    refresh_interval_ms              = 172800000 # 2 days
    allow_non_incremental_definition = "false"
  }

}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]