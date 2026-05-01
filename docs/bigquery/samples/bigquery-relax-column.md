* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 放寬資料欄 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

將必要資料欄變更為可為空值。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)

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

// relaxTableAPI demonstrates modifying the schema of a table to remove the requirement that columns allow
// no NULL values.
func relaxTableAPI(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydatasetid"
	// tableID := "mytableid"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	// Setup: We first create a table with a schema that's restricts NULL values.
	sampleSchema := bigquery.Schema{
		{Name: "full_name", Type: bigquery.StringFieldType, Required: true},
		{Name: "age", Type: bigquery.IntegerFieldType, Required: true},
	}
	original := &bigquery.TableMetadata{
		Schema: sampleSchema,
	}
	if err := client.Dataset(datasetID).Table(tableID).Create(ctx, original); err != nil {
		return err
	}

	tableRef := client.Dataset(datasetID).Table(tableID)
	meta, err := tableRef.Metadata(ctx)
	if err != nil {
		return err
	}
	// Iterate through the schema to set all Required fields to false (nullable).
	var relaxed bigquery.Schema
	for _, v := range meta.Schema {
		v.Required = false
		relaxed = append(relaxed, v)
	}
	newMeta := bigquery.TableMetadataToUpdate{
		Schema: relaxed,
	}
	if _, err := tableRef.Update(ctx, newMeta, meta.ETag); err != nil {
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
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.LegacySQLTypeName;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardTableDefinition;
import com.google.cloud.bigquery.Table;

public class RelaxColumnMode {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableId = "MY_TABLE_NAME";
    relaxColumnMode(datasetName, tableId);
  }

  public static void relaxColumnMode(String datasetName, String tableId) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Table table = bigquery.getTable(datasetName, tableId);

      // Create new relaxed schema based on the existing table schema
      Schema relaxedSchema =
          Schema.of(
              // The only supported modification you can make to a column's mode is changing it from
              // REQUIRED to NULLABLE
              // Changing a column's mode from REQUIRED to NULLABLE is also called column relaxation
              // INFO: LegacySQLTypeName will be updated to StandardSQLTypeName in release 1.103.0
              Field.newBuilder("word", LegacySQLTypeName.STRING)
                  .setMode(Field.Mode.NULLABLE)
                  .build(),
              Field.newBuilder("word_count", LegacySQLTypeName.STRING)
                  .setMode(Field.Mode.NULLABLE)
                  .build(),
              Field.newBuilder("corpus", LegacySQLTypeName.STRING)
                  .setMode(Field.Mode.NULLABLE)
                  .build(),
              Field.newBuilder("corpus_date", LegacySQLTypeName.STRING)
                  .setMode(Field.Mode.NULLABLE)
                  .build());

      // Update the table with the new schema
      Table updatedTable =
          table.toBuilder().setDefinition(StandardTableDefinition.of(relaxedSchema)).build();
      updatedTable.update();
      System.out.println("Table schema successfully relaxed.");
    } catch (BigQueryException e) {
      System.out.println("Table schema not relaxed \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library and create a client
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function relaxColumn() {
  /**
   * Changes columns from required to nullable.
   * Assumes existing table with the following schema:
   * [{name: 'Name', type: 'STRING', mode: 'REQUIRED'},
   * {name: 'Age', type: 'INTEGER'},
   * {name: 'Weight', type: 'FLOAT'},
   * {name: 'IsMagic', type: 'BOOLEAN'}];
   */

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  const newSchema = [
    {name: 'Name', type: 'STRING', mode: 'NULLABLE'},
    {name: 'Age', type: 'INTEGER'},
    {name: 'Weight', type: 'FLOAT'},
    {name: 'IsMagic', type: 'BOOLEAN'},
  ];

  // Retrieve current table metadata
  const table = bigquery.dataset(datasetId).table(tableId);
  const [metadata] = await table.getMetadata();

  // Update schema
  metadata.schema = newSchema;
  const [apiResponse] = await table.setMetadata(metadata);

  console.log(apiResponse.schema.fields);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

# TODO(dev): Change table_id to full name of the table you want to create.
table_id = "your-project.your_dataset.your_table"

table = client.get_table(table_id)
new_schema = []
for field in table.schema:
    if field.mode != "REQUIRED":
        new_schema.append(field)
    else:
        # SchemaField properties cannot be edited after initialization.
        # To make changes, construct new SchemaField objects.
        new_field = field.to_api_repr()
        new_field["mode"] = "NULLABLE"
        relaxed_field = bigquery.SchemaField.from_api_repr(new_field)
        new_schema.append(relaxed_field)

table.schema = new_schema
table = client.update_table(table, ["schema"])

print(f"Updated {table_id} schema: {table.schema}.")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]