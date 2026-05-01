* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 修改資料表結構定義

本文說明如何修改現有 BigQuery 資料表的結構定義。

您可以使用 SQL [資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)，進行本文所述的大部分結構定義修改。這些對帳單不會產生費用。

如要以本頁所述的所有方式修改資料表結構，請將資料表資料[匯出](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)至 Cloud Storage，然後將資料[載入](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)至結構定義經過修改的新資料表。BigQuery 載入和擷取工作免費，但您必須付費才能將匯出的資料儲存在 Cloud Storage 中。以下各節說明如何以其他方式執行各種結構定義修改。

BigQuery 中的結構定義更新不會導致資料遺失。

**注意：** 更新結構定義後，變更內容可能不會立即反映在 [`INFORMATION_SCHEMA.TABLES`](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw) 和 [`INFORMATION_SCHEMA.COLUMNS`](https://docs.cloud.google.com/bigquery/docs/information-schema-columns?hl=zh-tw) 檢視畫面中。如要查看立即結構定義異動，請呼叫 [`tables.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw)。

## 新增資料欄

您可以透過下列任一方式，將資料欄新增至現有資料表的結構定義：

* 新增空白資料欄。
* 使用載入或查詢工作覆寫資料表。
* 使用載入或查詢工作將資料附加至資料表。

您新增的任何資料欄都必須遵守 BigQuery 的[資料欄名稱](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_names)規則。如要進一步瞭解如何建立結構定義元件，請參閱[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。

您無法在資料表結構定義中間新增資料欄。系統一律會在表格或欄位的結尾處新增資料欄和巢狀欄位。如要在表格結構定義中間建立新資料欄，唯一方法是使用所選結構定義建立新表格，然後從原始表格複製資料。

### 新增空白資料欄

新增資料欄至現有的資料表結構定義時，資料欄必須為 `NULLABLE` 或 `REPEATED`。您無法將 `REQUIRED` 資料欄新增至現有的資料表結構定義。在 API 或 bq 指令列工具中，將 `REQUIRED` 資料欄新增至現有資料表結構定義會導致錯誤。不過，您可以建立巢狀 `REQUIRED` 欄，做為新 `RECORD` 欄位的一部分。只有在載入資料時建立資料表，或者使用結構定義建立空白資料表時，您才能新增 `REQUIRED` 資料欄。

如何將空白資料欄新增至資料表的結構定義：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 依序點選「總覽」**>「表格」**，然後選取所需表格。
5. 在詳細資料窗格中，按一下「結構定義」分頁標籤。
6. 點選「編輯結構定義」。你可能需要捲動頁面才能看到這個按鈕。
7. 在「目前的結構定義」頁面中，按一下「新欄位」下方的「新增欄位」。

   * 在「Name」(名稱) 部分，輸入資料欄名稱。
   * 針對「Type」(類型)，請選擇[資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)。
   * 針對[「Mode」(模式)](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#TableFieldSchema.FIELDS.mode)，請選擇 `NULLABLE` 或 `REPEATED`。
8. 資料欄新增完畢後，按一下 [Save] (儲存)。

**注意：** 您無法使用 Google Cloud 控制台，在[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)中新增資料欄。

### SQL

使用 [`ALTER TABLE ADD COLUMN` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_add_column_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mytable
   ADD COLUMN new_column STRING;
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

**注意：** 您無法使用 `ALTER TABLE ADD COLUMN` 陳述式，在[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)中新增資料欄。

### bq

發出 `bq update` 指令並提供 JSON 結構定義檔。如果您要更新的資料表位於非預設專案中，請依照下列格式將該專案的 ID 加到資料集名稱中：`PROJECT_ID:DATASET`。

```
bq update PROJECT_ID:DATASET.TABLE SCHEMA
```

更改下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET`：含有您要更新之資料表的資料集名稱。
* `TABLE`：要更新的資料表名稱。
* `SCHEMA`：您本機上的 JSON 結構定義檔路徑。

指定內嵌結構定義時，無法指定資料欄說明、模式和 `RECORD` ([`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)) 類型。所有資料欄模式都會預設為 `NULLABLE`。因此如要新增巢狀資料欄至 `RECORD`，就必須[提供 JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)。

如果您嘗試使用內嵌結構定義新增資料欄，則必須提供包括新資料欄在內的整個結構定義。由於您無法使用內嵌結構定義指定資料欄模式，因此更新作業會將任何現有的 `REPEATED` 資料欄變更為 `NULLABLE`，這會產生下列錯誤：`BigQuery error in update
operation: Provided Schema does not match Table
PROJECT_ID:dataset.table. Field field has changed mode
from REPEATED to NULLABLE.`

使用 bq 指令列工具將資料欄新增至現有資料表的建議方法是[提供 JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)。

如何使用 JSON 結構定義檔案將空白資料欄新增至資料表的結構定義：

1. 首先，請發出 `bq show` 指令並加上 `--schema` 旗標，並將現有的資料表結構定義寫入檔案。如果您要更新的資料表位於非預設專案中，請依照下列格式將該專案的 ID 加到資料集名稱中：`PROJECT_ID:DATASET`。

   ```
   bq show \
   --schema \
   --format=prettyjson \
   PROJECT_ID:DATASET.TABLE > SCHEMA
   ```

   更改下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET`：含有您要更新之資料表的資料集名稱。
   * `TABLE`：要更新的資料表名稱。
   * `SCHEMA`：寫入本機的結構定義檔。

   舉例來說，如要將 `mydataset.mytable` 的結構定義寫入檔案，請輸入下列指令。`mydataset.mytable` 位於您的預設專案中。

   ```
      bq show \
      --schema \
      --format=prettyjson \
      mydataset.mytable > /tmp/myschema.json
   ```
2. 在文字編輯器中開啟結構定義檔。結構定義應如下所示：

   ```
   [
     {
       "mode": "REQUIRED",
       "name": "column1",
       "type": "STRING"
     },
     {
       "mode": "REQUIRED",
       "name": "column2",
       "type": "FLOAT"
     },
     {
       "mode": "REPEATED",
       "name": "column3",
       "type": "STRING"
     }
   ]
   ```
3. 將資料欄新增至結構定義的結尾處。如果您嘗試在陣列的其他地方新增資料欄，系統將會傳回下列錯誤訊息：`BigQuery error in update operation: Precondition
   Failed`。資料表建立完成後，修改結構定義順序不會影響資料欄或巢狀欄位順序。

   您可以使用 JSON 檔案為新資料欄指定說明、`NULLABLE` 或 `REPEATED` 模式以及 `RECORD` 類型。例如，如果使用上一個步驟中的結構定義，新的 JSON 陣列會如下所示。此範例中會新增名為 `column4` 的 `NULLABLE` 資料欄，且 `column4` 包含說明。

   ```
     [
       {
         "mode": "REQUIRED",
         "name": "column1",
         "type": "STRING"
       },
       {
         "mode": "REQUIRED",
         "name": "column2",
         "type": "FLOAT"
       },
       {
         "mode": "REPEATED",
         "name": "column3",
         "type": "STRING"
       },
       {
         "description": "my new column",
         "mode": "NULLABLE",
         "name": "column4",
         "type": "STRING"
       }
     ]
   ```

   如要進一步瞭解如何使用 JSON 結構定義檔，請參閱[指定 JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)一節。
4. 更新結構定義檔後，請發出下列指令來更新資料表的結構定義。如果您要更新的資料表位於預設專案以外的專案中，請依照下列格式將該專案的 ID 加到資料集名稱中：`PROJECT_ID:DATASET`。

   ```
   bq update PROJECT_ID:DATASET.TABLE SCHEMA
   ```

   更改下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET`：含有您要更新之資料表的資料集名稱。
   * `TABLE`：要更新的資料表名稱。
   * `SCHEMA`：寫入本機的結構定義檔。

   例如，輸入以下指令來更新預設專案中 `mydataset.mytable` 的結構定義。您本機機器上的 JSON 結構定義檔路徑為 `/tmp/myschema.json`。

   ```
   bq update mydataset.mytable /tmp/myschema.json
   ```

### API

呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法，並使用 `schema` 屬性將空白資料欄新增至結構定義。由於 `tables.update` 方法會取代整個資料表資源，因此建議使用 `tables.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// updateTableAddColumn demonstrates modifying the schema of a table to append an additional column.
func updateTableAddColumn(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	tableRef := client.Dataset(datasetID).Table(tableID)
	meta, err := tableRef.Metadata(ctx)
	if err != nil {
		return err
	}
	newSchema := append(meta.Schema,
		&bigquery.FieldSchema{Name: "phone", Type: bigquery.StringFieldType},
	)
	update := bigquery.TableMetadataToUpdate{
		Schema: newSchema,
	}
	if _, err := tableRef.Update(ctx, update, meta.ETag); err != nil {
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
import com.google.cloud.bigquery.FieldList;
import com.google.cloud.bigquery.LegacySQLTypeName;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardTableDefinition;
import com.google.cloud.bigquery.Table;
import java.util.ArrayList;
import java.util.List;

public class AddEmptyColumn {

  public static void runAddEmptyColumn() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableId = "MY_TABLE_NAME";
    String newColumnName = "NEW_COLUMN_NAME";
    addEmptyColumn(newColumnName, datasetName, tableId);
  }

  public static void addEmptyColumn(String newColumnName, String datasetName, String tableId) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Table table = bigquery.getTable(datasetName, tableId);
      Schema schema = table.getDefinition().getSchema();
      FieldList fields = schema.getFields();

      // Create the new field/column
      Field newField = Field.of(newColumnName, LegacySQLTypeName.STRING);

      // Create a new schema adding the current fields, plus the new one
      List<Field> fieldList = new ArrayList<Field>();
      fields.forEach(fieldList::add);
      fieldList.add(newField);
      Schema newSchema = Schema.of(fieldList);

      // Update the table with the new schema
      Table updatedTable =
          table.toBuilder().setDefinition(StandardTableDefinition.of(newSchema)).build();
      updatedTable.update();
      System.out.println("Empty column successfully added to table");
    } catch (BigQueryException e) {
      System.out.println("Empty column was not added. \n" + e.toString());
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

async function addEmptyColumn() {
  // Adds an empty column to the schema.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';
  const column = {name: 'size', type: 'STRING'};

  // Retrieve current table metadata
  const table = bigquery.dataset(datasetId).table(tableId);
  const [metadata] = await table.getMetadata();

  // Update table schema
  const schema = metadata.schema;
  const new_schema = schema;
  new_schema.fields.push(column);
  metadata.schema = new_schema;

  const [result] = await table.setMetadata(metadata);
  console.log(result.schema.fields);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

將新的 [SchemaField](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.schema.SchemaField?hl=zh-tw) 物件附加至 [Table.schema](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.Table?hl=zh-tw#google_cloud_bigquery_table_Table_schema) 的副本，然後用已更新的結構定義取代 [Table.schema](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.Table?hl=zh-tw#google_cloud_bigquery_table_Table_schema) 屬性的值。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table
#                  to add an empty column.
# table_id = "your-project.your_dataset.your_table_name"

table = client.get_table(table_id)  # Make an API request.

original_schema = table.schema
new_schema = original_schema[:]  # Creates a copy of the schema.
new_schema.append(bigquery.SchemaField("phone", "STRING"))

table.schema = new_schema
table = client.update_table(table, ["schema"])  # Make an API request.

if len(table.schema) == len(original_schema) + 1 == len(new_schema):
    print("A new column has been added.")
else:
    print("The column has not been added.")
```

### 在 `RECORD` 欄中新增巢狀資料欄

除了新增資料欄至資料表的結構定義外，您也可以將巢狀資料欄新增至 `RECORD` 資料欄。新增巢狀資料欄的程序與新增資料欄的程序類似。

### 控制台

Google Cloud 主控台不支援在現有的 `RECORD` 資料欄新增巢狀欄位。

### SQL

系統不支援使用 SQL DDL 陳述式，在現有的 `RECORD` 資料欄新增巢狀欄位。

### bq

發出 `bq update` 指令並提供 JSON 結構定義檔，該檔案會將巢狀欄位新增至現有 `RECORD` 資料欄的結構定義。如果您要更新的資料表位於非預設專案中，請依照下列格式將該專案的 ID 加到資料集名稱中：`PROJECT_ID:DATASET`。

```
bq update PROJECT_ID:DATASET.TABLE SCHEMA
```

更改下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET`：含有您要更新之資料表的資料集名稱。
* `TABLE`：要更新的資料表名稱。
* `SCHEMA`：您本機上的 JSON 結構定義檔路徑。

指定內嵌結構定義時，無法指定資料欄說明、模式和 `RECORD` ([`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)) 類型。所有資料欄模式都會預設為 `NULLABLE`。因此如要新增巢狀資料欄至 `RECORD`，就必須[提供 JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)。

若要使用 JSON 結構檔案將巢狀欄位新增至 `RECORD`，請進行以下操作：

1. 首先，請發出 `bq show` 指令並加上 `--schema` 旗標，並將現有的資料表結構定義寫入檔案。如果您要更新的資料表位於非預設專案中，請依照下列格式將該專案的 ID 加到資料集名稱中：`PROJECT_ID:DATASET.TABLE`。

   ```
   bq show \
   --schema \
   --format=prettyjson \
   PROJECT_ID:DATASET.TABLE > SCHEMA
   ```

   更改下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET`：含有您要更新之資料表的資料集名稱。
   * `TABLE`：要更新的資料表名稱。
   * `SCHEMA`：寫入本機的結構定義檔。

   舉例來說，如要將 `mydataset.mytable` 的結構定義寫入檔案，請輸入下列指令。`mydataset.mytable` 位於您的預設專案中。

   ```
   bq show \
   --schema \
   --format=prettyjson \
   mydataset.mytable > /tmp/myschema.json
   ```
2. 在文字編輯器中開啟結構定義檔。結構定義應如下所示。在此範例中，`column3` 是巢狀的重複資料欄。巢狀資料欄為 `nested1` 和 `nested2`。`fields` 陣列列出了以巢狀形式嵌套在 `column3` 中的欄位。

   ```
   [
     {
       "mode": "REQUIRED",
       "name": "column1",
       "type": "STRING"
     },
     {
       "mode": "REQUIRED",
       "name": "column2",
       "type": "FLOAT"
     },
     {
       "fields": [
         {
           "mode": "NULLABLE",
           "name": "nested1",
           "type": "STRING"
         },
         {
           "mode": "NULLABLE",
           "name": "nested2",
           "type": "STRING"
         }
       ],
       "mode": "REPEATED",
       "name": "column3",
       "type": "RECORD"
     }
   ]
   ```
3. 在 `fields` 陣列的結尾處新增巢狀資料欄。巢狀欄位一律會加在欄位結尾。在此範例中，`nested3` 是新的巢狀資料欄。

   ```
     [
       {
         "mode": "REQUIRED",
         "name": "column1",
         "type": "STRING"
       },
       {
         "mode": "REQUIRED",
         "name": "column2",
         "type": "FLOAT"
       },
       {
         "fields": [
           {
             "mode": "NULLABLE",
             "name": "nested1",
             "type": "STRING"
           },
           {
             "mode": "NULLABLE",
             "name": "nested2",
             "type": "STRING"
           },
           {
             "mode": "NULLABLE",
             "name": "nested3",
             "type": "STRING"
           }
         ],
         "mode": "REPEATED",
         "name": "column3",
         "type": "RECORD"
       }
     ]
   ```

   如要進一步瞭解如何使用 JSON 結構定義檔，請參閱[指定 JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)一節。
4. 更新結構定義檔後，請發出下列指令來更新資料表的結構定義。如果您要更新的資料表位於預設專案以外的專案中，請依照下列格式將該專案的 ID 加到資料集名稱中：`PROJECT_ID:DATASET`。

   ```
   bq update PROJECT_ID:DATASET.TABLE SCHEMA
   ```

   更改下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET`：含有您要更新之資料表的資料集名稱。
   * `TABLE`：要更新的資料表名稱。
   * `SCHEMA`：您本機上的 JSON 結構定義檔路徑。

   例如，輸入以下指令來更新預設專案中 `mydataset.mytable` 的結構定義。您本機機器上的 JSON 結構定義檔路徑為 `/tmp/myschema.json`。

   ```
   bq update mydataset.mytable /tmp/myschema.json
   ```

### API

呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法，並使用 `schema` 屬性將巢狀資料欄新增至結構定義。由於 `tables.update` 方法會取代整個資料表資源，因此建議使用 `tables.patch` 方法。

### 在覆寫或附加資料時新增資料欄

將資料載入現有資料表並選擇覆寫現有資料表時，可以新增資料欄至現有資料表。覆寫現有的資料表時，系統會使用所載入資料的結構定義來覆寫現有資料表的結構定義。如要瞭解如何使用載入工作覆寫資料表，請參閱資料格式的說明文件：

* [Avro](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw#appending_to_or_overwriting_a_table_with_avro_data)
* [Parquet](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#appending_to_or_overwriting_a_table_with_parquet_data)
* [ORC](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-orc?hl=zh-tw#append_to_or_overwrite_a_table_with_orc_data)
* [CSV](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#appending_to_or_overwriting_a_table_with_csv_data)
* [JSON](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#appending_to_or_overwriting_a_table_with_json_data)

#### 在載入附加工作中新增資料欄

您可以在載入工作期間將資料附加至資料表時一併新增資料欄。新結構定義的決定方式如下：

* 自動偵測 (適用於 CSV 和 JSON 檔案)
* 可在 JSON 結構定義檔中指定 (適用於 CSV 和 JSON 檔)
* Avro、ORC、Parquet 和 Datastore 匯出檔案的自述式來源資料

若您在 JSON 檔中指定結構，則必須在其中定義新的資料欄。如果缺少新資料欄的定義，則嘗試附加資料時，系統將會傳回錯誤訊息。

當您在附加作業期間新增資料欄時，系統將會針對現有資料列將新資料欄中的值設為 `NULL`。

如要在載入工作期間，在將資料附加到資料表時一併新增資料欄，請使用下列任一選項：

### bq

請使用 `bq load` 指令載入資料並指定 `--noreplace` 旗標，以指出您要將資料附加至現有的資料表。

如果您要附加的資料是 CSV 格式，或是以換行符號分隔的 JSON 格式，請指定 `--autodetect` 旗標以使用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，或在 JSON 結構定義檔中提供結構定義。系統可從 Avro 或 Datastore 匯出檔自動推斷新增的資料欄。

將 `--schema_update_option` 旗標設為 `ALLOW_FIELD_ADDITION`，以指出要附加的資料中包含新的資料欄。

如果您要附加的資料表位於非預設專案中的資料集裡，請依照下列格式將該專案的 ID 加到資料集名稱中：`PROJECT_ID:DATASET`。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

輸入 `load` 指令，如下所示：

```
bq --location=LOCATION load \
--noreplace \
--autodetect \
--schema_update_option=ALLOW_FIELD_ADDITION \
--source_format=FORMAT \
PROJECT_ID:DATASET.TABLE \
PATH_TO_SOURCE \
SCHEMA
```

更改下列內容：

* `LOCATION`：位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可將該旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)來設定位置的預設值。
* `FORMAT`：結構定義的格式。`NEWLINE_DELIMITED_JSON`、`CSV`、`AVRO`、`PARQUET`、`ORC` 或 `DATASTORE_BACKUP`。
* `PROJECT_ID`：您的專案 ID。
* `DATASET`：含有您要更新之資料表的資料集名稱。
* `TABLE`：要附加的資料表名稱。
* `PATH_TO_SOURCE`：完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)、以逗號分隔的 URI 清單，或您本機上的資料檔案路徑。
* `SCHEMA`：本機 JSON 結構定義檔的路徑。不指定 `--autodetect` 時，只有 CSV 和 JSON 檔案需要結構定義檔。系統會從來源資料推斷 Avro 和 Datastore 的結構定義。

範例：

輸入下列指令，使用載入工作將本機 Avro 資料檔案 (`/tmp/mydata.avro`) 附加至 `mydataset.mytable`。由於結構定義可從 Avro 資料中自動推斷出來，因此您不需要使用 `--autodetect` 旗標。`mydataset` 位於您的預設專案中。

```
bq load \
--noreplace \
--schema_update_option=ALLOW_FIELD_ADDITION \
--source_format=AVRO \
mydataset.mytable \
/tmp/mydata.avro
```

輸入下列指令，使用載入工作將 Cloud Storage 中採用換行符號分隔格式的 JSON 資料檔案附加至 `mydataset.mytable`。`--autodetect` 旗標可用於偵測新資料欄。`mydataset` 位於您的預設專案中。

```
bq load \
--noreplace \
--autodetect \
--schema_update_option=ALLOW_FIELD_ADDITION \
--source_format=NEWLINE_DELIMITED_JSON \
mydataset.mytable \
gs://mybucket/mydata.json
```

輸入下列指令，使用載入工作將 Cloud Storage 中採用換行符號分隔格式的 JSON 資料檔案附加至 `mydataset.mytable`。包含新資料欄的結構定義是在本機 JSON 結構定義檔 `/tmp/myschema.json` 中指定。`mydataset` 在 `myotherproject` 中，而不在您的預設專案中。

```
bq load \
--noreplace \
--schema_update_option=ALLOW_FIELD_ADDITION \
--source_format=NEWLINE_DELIMITED_JSON \
myotherproject:mydataset.mytable \
gs://mybucket/mydata.json \
/tmp/myschema.json
```

### API

呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法。設定 `load` 工作和下列屬性：

* 使用 `sourceUris` 屬性參照 Cloud Storage 中的資料。
* 設定 `sourceFormat` 屬性來指定資料格式。
* 在 `schema` 屬性中指定結構定義。
* 使用 `schemaUpdateOptions` 屬性指定結構定義更新選項。
* 使用 `writeDisposition` 屬性將目的地資料表的寫入處理方式設為 `WRITE_APPEND`。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"os"

	"cloud.google.com/go/bigquery"
)

// createTableAndWidenLoad demonstrates augmenting a table's schema to add a new column via a load job.
func createTableAndWidenLoad(projectID, datasetID, tableID, filename string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	sampleSchema := bigquery.Schema{
		{Name: "full_name", Type: bigquery.StringFieldType},
	}
	meta := &bigquery.TableMetadata{
		Schema: sampleSchema,
	}
	tableRef := client.Dataset(datasetID).Table(tableID)
	if err := tableRef.Create(ctx, meta); err != nil {
		return err
	}
	// Now, import data from a local file, but specify field additions are allowed.
	// Because the data has a second column (age), the schema is amended as part of
	// the load.
	f, err := os.Open(filename)
	if err != nil {
		return err
	}
	source := bigquery.NewReaderSource(f)
	source.AutoDetect = true   // Allow BigQuery to determine schema.
	source.SkipLeadingRows = 1 // CSV has a single header line.

	loader := client.Dataset(datasetID).Table(tableID).LoaderFrom(source)
	loader.SchemaUpdateOptions = []string{"ALLOW_FIELD_ADDITION"}
	job, err := loader.Run(ctx)
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
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobId;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.JobInfo.SchemaUpdateOption;
import com.google.cloud.bigquery.JobInfo.WriteDisposition;
import com.google.cloud.bigquery.LegacySQLTypeName;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.TableId;
import com.google.common.collect.ImmutableList;
import java.util.UUID;

public class AddColumnLoadAppend {

  public static void runAddColumnLoadAppend() throws Exception {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "/path/to/file.csv";
    addColumnLoadAppend(datasetName, tableName, sourceUri);
  }

  public static void addColumnLoadAppend(String datasetName, String tableName, String sourceUri)
      throws Exception {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);

      // Add a new column to a BigQuery table while appending rows via a load job.
      // 'REQUIRED' fields cannot  be added to an existing schema, so the additional column must be
      // 'NULLABLE'.
      Schema newSchema =
          Schema.of(
              Field.newBuilder("name", LegacySQLTypeName.STRING)
                  .setMode(Field.Mode.REQUIRED)
                  .build(),
              // Adding below additional column during the load job
              Field.newBuilder("post_abbr", LegacySQLTypeName.STRING)
                  .setMode(Field.Mode.NULLABLE)
                  .build());

      LoadJobConfiguration loadJobConfig =
          LoadJobConfiguration.builder(tableId, sourceUri)
              .setFormatOptions(FormatOptions.csv())
              .setWriteDisposition(WriteDisposition.WRITE_APPEND)
              .setSchema(newSchema)
              .setSchemaUpdateOptions(ImmutableList.of(SchemaUpdateOption.ALLOW_FIELD_ADDITION))
              .build();

      // Create a job ID so that we can safely retry.
      JobId jobId = JobId.of(UUID.randomUUID().toString());
      Job loadJob = bigquery.create(JobInfo.newBuilder(loadJobConfig).setJobId(jobId).build());

      // Load data from a GCS parquet file into the table
      // Blocks until this load table job completes its execution, either failing or succeeding.
      Job completedJob = loadJob.waitFor();

      // Check for errors
      if (completedJob == null) {
        throw new Exception("Job not executed since it no longer exists.");
      } else if (completedJob.getStatus().getError() != null) {
        // You can also look at queryJob.getStatus().getExecutionErrors() for all
        // errors, not just the latest one.
        throw new Exception(
            "BigQuery was unable to load into the table due to an error: \n"
                + loadJob.getStatus().getError());
      }
      System.out.println("Column successfully added during load append job");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Column not added during load append \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client libraries
const {BigQuery} = require('@google-cloud/bigquery');

// Instantiate client
const bigquery = new BigQuery();

async function addColumnLoadAppend() {
  // Adds a new column to a BigQuery table while appending rows via a load job.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const fileName = '/path/to/file.csv';
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  // In this example, the existing table contains only the 'Name', 'Age',
  // & 'Weight' columns. 'REQUIRED' fields cannot  be added to an existing
  // schema, so the additional column must be 'NULLABLE'.
  const schema = 'Name:STRING, Age:INTEGER, Weight:FLOAT, IsMagic:BOOLEAN';

  // Retrieve destination table reference
  const [table] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .get();
  const destinationTableRef = table.metadata.tableReference;

  // Set load job options
  const options = {
    schema: schema,
    schemaUpdateOptions: ['ALLOW_FIELD_ADDITION'],
    writeDisposition: 'WRITE_APPEND',
    destinationTable: destinationTableRef,
  };

  // Load data from a local file into the table
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .load(fileName, options);

  console.log(`Job ${job.id} completed.`);
  console.log(`New Schema:`);
  console.log(job.configuration.load.schema.fields);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# from google.cloud import bigquery
# client = bigquery.Client()
# project = client.project
# dataset_ref = bigquery.DatasetReference(project, 'my_dataset')
# filepath = 'path/to/your_file.csv'

# Retrieves the destination table and checks the length of the schema
table_id = "my_table"
table_ref = dataset_ref.table(table_id)
table = client.get_table(table_ref)
print("Table {} contains {} columns.".format(table_id, len(table.schema)))

# Configures the load job to append the data to the destination table,
# allowing field addition
job_config = bigquery.LoadJobConfig()
job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
job_config.schema_update_options = [
    bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
]
# In this example, the existing table contains only the 'full_name' column.
# 'REQUIRED' fields cannot be added to an existing schema, so the
# additional column must be 'NULLABLE'.
job_config.schema = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
]
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1

with open(filepath, "rb") as source_file:
    job = client.load_table_from_file(
        source_file,
        table_ref,
        location="US",  # Must match the destination dataset location.
        job_config=job_config,
    )  # API request

job.result()  # Waits for table load to complete.
print(
    "Loaded {} rows into {}:{}.".format(
        job.output_rows, dataset_id, table_ref.table_id
    )
)

# Checks the updated length of the schema
table = client.get_table(table)
print("Table {} now contains {} columns.".format(table_id, len(table.schema)))
```

#### 在查詢附加工作中新增資料欄

將查詢結果附加至資料表時，可以新增資料欄至資料表。

在查詢工作中使用附加作業新增資料欄時，系統會使用查詢結果的結構定義來更新目的地資料表的結構定義。請注意，您無法在一個位置查詢資料表後，將結果寫入不同位置的資料表。

如要在查詢工作期間，於將資料附加至資料表時一併新增資料欄，請選取下列其中一個選項：

### bq

使用 `bq query` 指令查詢資料，並指定 `--destination_table` 旗標來指出您要附加的資料表。

如要指定將查詢結果附加至現有目的地資料表，請指定 `--append_table` 旗標。

將 `--schema_update_option` 旗標設定為 `ALLOW_FIELD_ADDITION`，以指出要附加的查詢結果中包含新的資料欄。

指定 `use_legacy_sql=false` 旗標，以在查詢中使用 GoogleSQL 語法。

如果您要附加的資料表位於非預設專案中的資料集裡，請依照下列格式將該專案的 ID 加到資料集名稱中：`PROJECT_ID:DATASET`。請注意，您要查詢的資料表和目的地資料表必須位於同一位置。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

```
bq --location=LOCATION query \
--destination_table PROJECT_ID:DATASET.TABLE \
--append_table \
--schema_update_option=ALLOW_FIELD_ADDITION \
--use_legacy_sql=false \
'QUERY'
```

更改下列內容：

* `LOCATION`：位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可將該旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)來設定位置的預設值。請注意，您無法將查詢結果附加至不同位置的資料表。
* `PROJECT_ID`：您的專案 ID。
* `dataset`：含有您要附加之資料表的資料集名稱。
* `TABLE`：要附加的資料表名稱。
* `QUERY`：採用 GoogleSQL 語法的查詢。

範例：

輸入下列指令，以查詢預設專案中的 `mydataset.mytable`，並將查詢結果附加至 `mydataset.mytable2` (也在預設專案中)。

```
bq query \
--destination_table mydataset.mytable2 \
--append_table \
--schema_update_option=ALLOW_FIELD_ADDITION \
--use_legacy_sql=false \
'SELECT
   column1,column2
 FROM
   mydataset.mytable'
```

輸入下列指令，以查詢預設專案中的 `mydataset.mytable`，並將查詢結果附加至位於 `myotherproject` 中的 `mydataset.mytable2`。

```
bq query \
--destination_table myotherproject:mydataset.mytable2 \
--append_table \
--schema_update_option=ALLOW_FIELD_ADDITION \
--use_legacy_sql=false \
'SELECT
   column1,column2
 FROM
   mydataset.mytable'
```

### API

呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法。設定 `query` 工作和下列屬性：

* 使用 `destinationTable` 屬性指定目的地資料表。
* 使用 `writeDisposition` 屬性將目的地資料表的寫入處理方式設為 `WRITE_APPEND`。
* 使用 `schemaUpdateOptions` 屬性指定結構定義更新選項。
* 使用 `query` 屬性指定 GoogleSQL 查詢。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// createTableAndWidenQuery demonstrates how the schema of a table can be modified to add columns by appending
// query results that include the new columns.
func createTableAndWidenQuery(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	// First, we create a sample table.
	sampleSchema := bigquery.Schema{
		{Name: "full_name", Type: bigquery.StringFieldType, Required: true},
		{Name: "age", Type: bigquery.IntegerFieldType, Required: true},
	}
	original := &bigquery.TableMetadata{
		Schema: sampleSchema,
	}
	tableRef := client.Dataset(datasetID).Table(tableID)
	if err := tableRef.Create(ctx, original); err != nil {
		return err
	}
	// Our table has two columns.  We'll introduce a new favorite_color column via
	// a subsequent query that appends to the table.
	q := client.Query("SELECT \"Timmy\" as full_name, 85 as age, \"Blue\" as favorite_color")
	q.SchemaUpdateOptions = []string{"ALLOW_FIELD_ADDITION"}
	q.QueryConfig.Dst = client.Dataset(datasetID).Table(tableID)
	q.WriteDisposition = bigquery.WriteAppend
	q.Location = "US"
	job, err := q.Run(ctx)
	if err != nil {
		return err
	}
	_, err = job.Wait(ctx)
	if err != nil {
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
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.JobInfo.SchemaUpdateOption;
import com.google.cloud.bigquery.JobInfo.WriteDisposition;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableResult;
import com.google.common.collect.ImmutableList;

public class RelaxTableQuery {

  public static void runRelaxTableQuery() throws Exception {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    relaxTableQuery(projectId, datasetName, tableName);
  }

  // To relax all columns in a destination table when you append data to it during a query job
  public static void relaxTableQuery(String projectId, String datasetName, String tableName)
      throws Exception {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);

      String sourceTable = "`" + projectId + "." + datasetName + "."<
```