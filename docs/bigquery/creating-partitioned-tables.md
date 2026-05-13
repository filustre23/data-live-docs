Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立分區資料表

本頁面說明如何在 BigQuery 中建立分區資料表。如需分區資料表的總覽，請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。

### 所需權限

### 必要的角色

如要取得建立資料表所需的權限，請要求管理員授予您下列 IAM 角色：

* 如果您要透過載入資料或將查詢結果儲存至資料表來建立資料表，請在專案中指派 [BigQuery Job User](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)。
* 資料集的「BigQuery 資料編輯者」 (`roles/bigquery.dataEditor`)，您要在該資料集建立資料表。

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備建立表格所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立資料表，您必須具備下列權限：

* `bigquery.tables.create`
  在要建立資料表的資料集上。
* `bigquery.tables.getData`
  如果您要將查詢結果儲存為資料表，則必須擁有查詢參照的所有資料表和檢視區塊的存取權。
* `bigquery.jobs.create`
  專案，如果您是透過載入資料或將查詢結果儲存至資料表來建立資料表。
* `bigquery.tables.updateData`
  資料表，如果您要使用查詢結果附加或覆寫資料表，就需要這個權限。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 建立空白分區資料表

在 BigQuery 中建立分區資料表的步驟，與建立[標準資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)類似，但您需要指定分區選項，以及任何其他資料表選項。

### 建立時間單位資料欄分區資料表

如何使用結構定義建立空白時間單位資料欄分區資料表：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「來源」部分，從「建立資料表來源」清單中選取「空白資料表」。
2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。結構定義必須包含 `DATE`、`TIMESTAMP` 或 `DATETIME` 資料欄，做為分區資料欄。詳情請參閱[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。
   你可以使用下列任一方法手動輸入結構定義資訊：
   * 選項 1：按一下「以文字形式編輯」，然後以 JSON 陣列的形式貼上結構定義。如果您使用 JSON 陣列，可透過與[建立 JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)一樣的程序產生結構定義。您可以輸入下列指令，查看現有資料表的 JSON 格式結構定義：

     ```
         bq show --format=prettyjson dataset.table
     ```
   * 選項 2：按一下 add\_box
     「新增欄位」，然後輸入表格結構定義。指定每個欄位的「Name」(名稱)、「[Type](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#standard_sql_data_types)」(類型) 和「[Mode](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#modes)」(模式)。
4. 在「Partition and cluster settings」(分區與叢集設定) 區段的「Partitioning」(分區) 清單中，選取「Partition by field」(依欄位分區)，然後選擇分區資料欄。只有在結構定義包含 `DATE`、`TIMESTAMP` 或 `DATETIME` 資料欄時，才能使用這個選項。
5. 選用：如要要求所有查詢都必須使用分區篩選器，請選取「Require partition filter」(需要分區篩選器) 核取方塊。分區篩選器可降低費用並提升效能。詳情請參閱「[設定分區篩選器規定](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)」。
6. 選取「Partitioning type」。
7. 選用步驟：如要使用客戶自行管理的加密金鑰，請在「Advanced options」(進階選項) 部分選取「Use a customer-managed encryption key (CMEK)」(使用客戶自行管理的加密金鑰 (CMEK)) 選項。根據預設，BigQuery 會使用 Google-owned and Google-managed encryption key[加密靜態儲存的客戶內容](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
8. 點選「建立資料表」。

**注意：** 您無法在 Google Cloud 控制台中設定分區到期時間。如要在建立資料表後設定分區，請參閱[更新分區到期時間](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)。

### SQL

如要建立時間單位資料欄分區資料表，請使用 [`CREATE TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，並搭配 [`PARTITION BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#partition_expression)。

下列範例會根據 `transaction_date` 資料欄，建立每日分區的資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE
     mydataset.newtable (transaction_id INT64, transaction_date DATE)
   PARTITION BY
     transaction_date
     OPTIONS (
       partition_expiration_days = 3,
       require_partition_filter = TRUE);
   ```

   使用 [`OPTIONS` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#table_option_list)設定資料表選項，例如[分區到期時間](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)和[分區篩選器要求](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

`DATE` 欄的預設分區類型為每日分區。如要指定其他分割類型，請在 `PARTITION BY` 子句中加入 [`DATE_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_trunc) 函式。舉例來說，下列查詢會建立每月分區的資料表：

```
CREATE TABLE
  mydataset.newtable (transaction_id INT64, transaction_date DATE)
PARTITION BY
  DATE_TRUNC(transaction_date, MONTH)
  OPTIONS (
    partition_expiration_days = 3,
    require_partition_filter = TRUE);
```

您也可以指定 `TIMESTAMP` 或 `DATETIME` 資料欄做為分區資料欄。在這種情況下，請在 `PARTITION BY` 子句中加入 `TIMESTAMP_TRUNC` 或 `DATETIME_TRUNC` 函式，指定分割區類型。舉例來說，下列陳述式會根據 `TIMESTAMP` 資料欄建立每日分區的資料表：

```
CREATE TABLE
  mydataset.newtable (transaction_id INT64, transaction_ts TIMESTAMP)
PARTITION BY
  TIMESTAMP_TRUNC(transaction_ts, DAY)
  OPTIONS (
    partition_expiration_days = 3,
    require_partition_filter = TRUE);
```

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) 指令並加上 `--table` 旗標 (或 `-t` 捷徑)：

   ```
   bq mk \
      --table \
      --schema SCHEMA \
      --time_partitioning_field COLUMN \
      --time_partitioning_type UNIT_TIME \
      --time_partitioning_expiration EXPIRATION_TIME \
      --require_partition_filter=BOOLEAN
      PROJECT_ID:DATASET.TABLE
   ```

   更改下列內容：

   * SCHEMA：格式為 `column:data_type,column:data_type` 的結構定義，或本機電腦上的 JSON 結構定義檔案路徑。詳情請參閱[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。
   * COLUMN：分割資料欄的名稱。在資料表結構定義中，這個資料欄必須是 `TIMESTAMP`、`DATETIME` 或 `DATE` 類型。
   * UNIT\_TIME：分區類型。支援的值包括 `DAY`、`HOUR`、`MONTH` 或 `YEAR`。
   * EXPIRATION\_TIME：資料表分區的到期時間，以秒為單位。`--time_partitioning_expiration` 是選用旗標。詳情請參閱「[設定分區期限](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)」。
   * BOOLEAN：如果 `true`，則對這個資料表執行的查詢必須包含分區篩選器。`--require_partition_filter` 是選用旗標。詳情請參閱「[設定分區篩選器規定](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)」。
   * PROJECT\_ID：專案 ID。如果省略此參數，系統會使用預設專案。
   * DATASET：專案中的資料集名稱。
   * TABLE：要建立的資料表名稱。

   如需其他指令列選項，請參閱 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)。

   下列範例會建立名為 `mytable` 的資料表，並使用每小時分區，依 `ts` 資料欄分區。分區到期時間為 259,200 秒 (3 天)。

   ```
   bq mk \
      -t \
      --schema 'ts:TIMESTAMP,qtr:STRING,sales:FLOAT' \
      --time_partitioning_field ts \
      --time_partitioning_type HOUR \
      --time_partitioning_expiration 259200  \
      mydataset.mytable
   ```

### Terraform

請使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 Cloud Resource Manager API。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會建立名為 `mytable` 的資料表，並按天分區：

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
  table_id   = "mytable"

  time_partitioning {
    type          = "DAY"
    field         = "Created"
    expiration_ms = 432000000 # 5 days
  }
  require_partition_filter = true

  schema = <<EOF
[
  {
    "name": "ID",
    "type": "INT64",
    "mode": "NULLABLE",
    "description": "Item ID"
  },
  {
    "name": "Created",
    "type": "TIMESTAMP",
    "description": "Record creation timestamp"
  },
  {
    "name": "Item",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

使用指定 `timePartitioning` 屬性和 `schema` 屬性的已定義[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
)

// createTablePartitioned demonstrates creating a table and specifying a time partitioning configuration.
func createTablePartitioned(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydatasetid"
	// tableID := "mytableid"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	sampleSchema := bigquery.Schema{
		{Name: "name", Type: bigquery.StringFieldType},
		{Name: "post_abbr", Type: bigquery.IntegerFieldType},
		{Name: "date", Type: bigquery.DateFieldType},
	}
	metadata := &bigquery.TableMetadata{
		TimePartitioning: &bigquery.TimePartitioning{
			Field:      "date",
			Expiration: 90 * 24 * time.Hour,
		},
		Schema: sampleSchema,
	}
	tableRef := client.Dataset(datasetID).Table(tableID)
	if err := tableRef.Create(ctx, metadata); err != nil {
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
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.StandardTableDefinition;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;
import com.google.cloud.bigquery.TimePartitioning;

// Sample to create a partition table
public class CreatePartitionedTable {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    Schema schema =
        Schema.of(
            Field.of("name", StandardSQLTypeName.STRING),
            Field.of("post_abbr", StandardSQLTypeName.STRING),
            Field.of("date", StandardSQLTypeName.DATE));
    createPartitionedTable(datasetName, tableName, schema);
  }

  public static void createPartitionedTable(String datasetName, String tableName, Schema schema) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);

      TimePartitioning partitioning =
          TimePartitioning.newBuilder(TimePartitioning.Type.DAY)
              .setField("date") //  name of column to use for partitioning
              .setExpirationMs(7776000000L) // 90 days
              .build();

      StandardTableDefinition tableDefinition =
          StandardTableDefinition.newBuilder()
              .setSchema(schema)
              .setTimePartitioning(partitioning)
              .build();
      TableInfo tableInfo = TableInfo.newBuilder(tableId, tableDefinition).build();

      bigquery.create(tableInfo);
      System.out.println("Partitioned table created successfully");
    } catch (BigQueryException e) {
      System.out.println("Partitioned table was not created. \n" + e.toString());
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

async function createTablePartitioned() {
  // Creates a new partitioned table named "my_table" in "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";
  const schema = 'Name:string, Post_Abbr:string, Date:date';

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
  const options = {
    schema: schema,
    location: 'US',
    timePartitioning: {
      type: 'DAY',
      expirationMS: '7776000000',
      field: 'date',
    },
  };

  // Create a new table in the dataset
  const [table] = await bigquery
    .dataset(datasetId)
    .createTable(tableId, options);
  console.log(`Table ${table.id} created with partitioning: `);
  console.log(table.metadata.timePartitioning);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

# Use format "your-project.your_dataset.your_table_name" for table_id
table_id = your_fully_qualified_table_id
schema = [
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("post_abbr", "STRING"),
    bigquery.SchemaField("date", "DATE"),
]
table = bigquery.Table(table_id, schema=schema)
table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="date",  # name of column to use for partitioning
    expiration_ms=1000 * 60 * 60 * 24 * 90,
)  # 90 days

table = client.create_table(table)

print(
    f"Created table {table.project}.{table.dataset_id}.{table.table_id}, "
    f"partitioned on column {table.time_partitioning.field}."
)
```

### 建立擷取時間分區資料表

如何使用結構定義建立空白擷取時間分區資料表：

### 控制台

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」面板中展開專案並選取資料集。
3. 展開「動作」選項，然後點按「開啟」。more\_vert
4. 在詳細資料面板中，按一下「建立資料表」
   add\_box。
5. 在「Create table」(建立資料表) 頁面的「Source」(來源) 區段中，選取 [Empty table] (空白資料表)。
6. 在「Destination」(目的地) 區段中：

   * 在「Dataset name」(資料集名稱) 部分選擇適當的資料集。
   * 在「Table name」(資料表名稱) 欄位中，輸入資料表名稱。
   * 確認「Table type」(資料表類型) 設為「Native table」(原生資料表)。
7. 在「Schema」(結構定義) 部分輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。
8. 在「Partition and cluster settings」(分區與叢集設定) 區段的「Partitioning」(分區) 中，按一下「Partition by ingestion time」(依擷取時間分區)。
9. (選用) 如要要求所有查詢都必須使用分區篩選器，請選取「Require partition filter」(需要分區篩選器) 核取方塊。使用分區篩選器可以降低成本並提升效能。詳情請參閱「[設定分區篩選器規定](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)」。
10. 點選「建立資料表」。

**注意：** 您無法在 Google Cloud 控制台中設定分區到期時間。如要在建立資料表後設定分區，請參閱[更新分區到期時間](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)。

### SQL

如要建立擷取時間分區資料表，請使用 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，並搭配 [`PARTITION BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#partition_expression)，依 `_PARTITIONDATE` 分區。

下列範例會建立每日分區的資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE
     mydataset.newtable (transaction_id INT64)
   PARTITION BY
     _PARTITIONDATE
     OPTIONS (
       partition_expiration_days = 3,
       require_partition_filter = TRUE);
   ```

   使用 [`OPTIONS` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#table_option_list)設定資料表選項，例如[分區到期時間](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)和[分區篩選器要求](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

擷取時間分區的預設分區類型為每日分區。如要指定其他分割類型，請在 `PARTITION BY` 子句中加入 [`DATE_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_trunc) 函式。舉例來說，下列查詢會建立每月分區的資料表：

```
CREATE TABLE
  mydataset.newtable (transaction_id INT64)
PARTITION BY
  DATE_TRUNC(_PARTITIONTIME, MONTH)
  OPTIONS (
    partition_expiration_days = 3,
    require_partition_filter = TRUE);
```

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) 指令並加上 `--table` 旗標 (或 `-t` 捷徑)：

   ```
   bq mk \
      --table \
      --schema SCHEMA \
      --time_partitioning_type UNIT_TIME \
      --time_partitioning_expiration EXPIRATION_TIME \
      --require_partition_filter=BOOLEAN  \
      PROJECT_ID:DATASET.TABLE
   ```

   更改下列內容：

   * SCHEMA：格式為 `column:data_type,column:data_type` 的定義，或本機上 JSON 結構定義檔的路徑。詳情請參閱[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。
   * UNIT\_TIME：分區類型。支援的值包括 `DAY`、`HOUR`、`MONTH` 或 `YEAR`。
   * EXPIRATION\_TIME：資料表分區的到期時間，以秒為單位。`--time_partitioning_expiration` 是選用旗標。詳情請參閱「[設定分區期限](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)」。
   * BOOLEAN：如果 `true`，則對這個資料表執行的查詢必須包含分區篩選器。`--require_partition_filter` 是選用旗標。詳情請參閱「[設定分區篩選器規定](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)」。
   * PROJECT\_ID：專案 ID。如果省略此參數，系統會使用預設專案。
   * DATASET：專案中的資料集名稱。
   * TABLE：要建立的資料表名稱。

   如需其他指令列選項，請參閱 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)。

   下列範例會建立名為 `mytable` 的擷取時間分區資料表。資料表採用每日分區，分區到期時間為 259,200 秒 (3 天)。

   ```
   bq mk \
      -t \
      --schema qtr:STRING,sales:FLOAT,year:STRING \
      --time_partitioning_type DAY \
      --time_partitioning_expiration 259200 \
      mydataset.mytable
   ```

### Terraform

請使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 Cloud Resource Manager API。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會建立名為 `mytable` 的資料表，並依擷取時間分區：

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
  table_id   = "mytable"

  time_partitioning {
    type          = "MONTH"
    expiration_ms = 604800000 # 7 days
  }
  require_partition_filter = true

  schema = <<EOF
[
  {
    "name": "ID",
    "type": "INT64",
    "mode": "NULLABLE",
    "description": "Item ID"
  },
  {
    "name": "Item",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

使用指定 `timePartitioning` 屬性和 `schema` 屬性的已定義[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法。

### 建立整數範圍分區資料表

如何使用結構定義建立空白整數範圍分區資料表：

### 控制台

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」面板中展開專案並選取資料集。
3. 展開「動作」選項，然後點按「開啟」。more\_vert
4. 在詳細資料面板中，按一下「建立資料表」
   add\_box。
5. 在「Create table」(建立資料表) 頁面的「Source」(來源) 區段中，選取 [Empty table] (空白資料表)。
6. 在「Destination」(目的地) 區段中：

   * 在「Dataset name」(資料集名稱) 部分選擇適當的資料集。
   * 在「Table name」(資料表名稱) 欄位中，輸入資料表名稱。
   * 確認「Table type」(資料表類型) 設為「Native table」(原生資料表)。
7. 在「Schema」(結構定義) 區段中，輸入結構定義。確認結構定義包含分區資料欄的 `INTEGER` 欄。詳情請參閱「[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)」。
8. 在「Partition and cluster settings」(分區與叢集設定) 區段的「Partitioning」(分區) 下拉式清單中，選取「Partition by field」(依欄位分區)，然後選擇分區資料欄。只有當結構定義包含 `INTEGER` 資料欄時，才能使用這個選項。
9. 提供「開始」、「結束」和「間隔」的值：

   * 「Start」是第一個分區範圍的起始值 (含)。
   * 「End」是最後一個分區範圍的結束值 (不含)。
   * 「Interval」是每個分區範圍的寬度。

   超出這些範圍的值會放入特殊 `__UNPARTITIONED__` 分區。
10. (選用) 如要要求所有查詢都必須使用分區篩選器，請選取「Require partition filter」(需要分區篩選器) 核取方塊。使用分區篩選器可以降低成本並提升效能。詳情請參閱「[設定分區篩選器規定](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)」。
11. 點選「建立資料表」。

**注意：** 您無法在 Google Cloud 控制台中設定分區到期時間。如要在建立資料表後設定分區，請參閱[更新分區到期時間](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)。

### SQL

如要建立整數範圍分區資料表，請使用 [`CREATE TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)搭配 [`PARTITION BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#partition_expression)。

下列範例會建立一個資料表，這個資料表在 `customer_id` 資料欄上含有一個起始值為 0、結束值為 100 且數字間隔為 10 的分區：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE mydataset.newtable (customer_id INT64, date1 DATE)
   PARTITION BY
     RANGE_BUCKET(customer_id, GENERATE_ARRAY(0, 100, 10))
     OPTIONS (
       require_partition_filter = TRUE);
   ```

   使用 [`OPTIONS` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#table_option_list)設定資料表選項，例如[分區篩選器需求](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) 指令並加上 `--table` 旗標 (或 `-t` 捷徑)：

   ```
   bq mk \
      --schema schema \
      --range_partitioning=COLUMN_NAME,START,END,INTERVAL \
      --require_partition_filter=BOOLEAN  \
      PROJECT_ID:DATASET.TABLE
   ```

   更改下列內容：

   * SCHEMA：格式為 `column:data_type,column:data_type` 的內嵌結構定義，或本機電腦上的 JSON 結構定義檔案路徑。詳情請參閱[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。
   * COLUMN\_NAME：分割資料欄的名稱。在資料表結構定義中，這個資料欄必須是 `INTEGER` 類型。
   * START：第一個分區範圍的起始值 (含)。
   * END：最後一個分區範圍的結尾 (不含)。
   * INTERVAL：每個分區範圍的寬度。
   * BOOLEAN：如果 `true`，則對這個資料表執行的查詢必須包含分區篩選器。`--require_partition_filter` 是選用旗標。詳情請參閱「[設定分區篩選器規定](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)」。
   * PROJECT\_ID：專案 ID。如果省略此參數，系統會使用預設專案。
   * DATASET：專案中的資料集名稱。
   * TABLE：要建立的資料表名稱。

   超出分區範圍的值會放入特殊 `__UNPARTITIONED__` 分區。

   如需其他指令列選項，請參閱 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)。

   下列範例會建立名為 `mytable` 的資料表，並依 `customer_id` 資料欄分區。

   ```
   bq mk \
      -t \
      --schema 'customer_id:INTEGER,qtr:STRING,sales:FLOAT' \
      --range_partitioning=customer_id,0,100,10 \
      mydataset.mytable
   ```

### Terraform

請使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 Cloud Resource Manager API。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會建立名為 `mytable` 的資料表，並依整數範圍分區：

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
  table_id   = "mytable"

  range_partitioning {
    field = "ID"
    range {
      start    = 0
      end      = 1000
      interval = 10
    }
  }
  require_partition_filter = true

  schema = <<EOF
[
  {
    "name": "ID",
    "type": "INT64",
    "description": "Item ID"
  },
  {
    "name": "Item",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

使用指定 `rangePartitioning` 屬性和 `schema` 屬性的已定義[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.RangePartitioning;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.StandardTableDefinition;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;

// Sample to create a range partitioned table
public class CreateRangePartitionedTable {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    Schema schema =
        Schema.of(
            Field.of("integerField", StandardSQLTypeName.INT64),
            Field.of("stringField", StandardSQLTypeName.STRING),
            Field.of("booleanField", StandardSQLTypeName.BOOL),
            Field.of("dateField", StandardSQLTypeName.DATE));
    createRangePartitionedTable(datasetName, tableName, schema);
  }

  public static void createRangePartitionedTable(
      String datasetName, String tableName, Schema schema) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);

      // Note: The field must be a top- level, NULLABLE/REQUIRED field.
      // The only supported type is INTEGER/INT64
      RangePartitioning partitioning =
          RangePartitioning.newBuilder()
              .setField("integerField")
              .setRange(
                  RangePartitioning.Range.newBuilder()
                      .setStart(1L)
                      .setInterval(2L)
                      .setEnd(10L)
                      .build())
              .build();

      StandardTableDefinition tableDefinition =
          StandardTableDefinition.newBuilder()
              .setSchema(schema)
              .setRangePartitioning(partitioning)
              .build();
      TableInfo tableInfo = TableInfo.newBuilder(tableId, tableDefinition).build();

      bigquery.create(tableInfo);
      System.out.println("Range partitioned table created successfully");
    } catch (BigQueryException e) {
      System.out.println("Range partitioned table was not created. \n" + e.toString());
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

async function createTableRangePartitioned() {
  // Creates a new integer range partitioned table named "my_table"
  // in "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";

  const schema = [
    {name: 'fullName', type: 'STRING'},
    {name: 'city', type: 'STRING'},
    {name: 'zipcode', type: 'INTEGER'},
  ];

  // To use integer range partitioning, select a top-level REQUIRED or
  // NULLABLE column with INTEGER / INT64 data type. Values that are
  // outside of the range of the table will go into the UNPARTITIONED
  // partition. Null values will be in the NULL partition.
  const rangePartition = {
    field: 'zipcode',
    range: {
      start: 0,
      end: 100000,
      interval: 10,
    },
  };

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
  const options = {
    schema: schema,
    rangePartitioning: rangePartition,
  };

  // Create a new table in the dataset
  const [table] = await bigquery
    .dataset(datasetId)
    .createTable(tableId, options);

  console.log(`Table ${table.id} created with integer range partitioning: `);
  console.log(table.metadata.rangePartitioning);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"

schema = [
    bigquery.SchemaField("full_name", "STRING"),
    bigquery.SchemaField("city", "STRING"),
    bigquery.SchemaField("zipcode", "INTEGER"),
]

table = bigquery.Table(table_id, schema=schema)
table.range_partitioning = bigquery.RangePartitioning(
    # To use integer range partitioning, select a top-level REQUIRED /
    # NULLABLE column with INTEGER / INT64 data type.
    field="zipcode",
    range_=bigquery.PartitionRange(start=0, end=100000, interval=10),
)
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)
```

## 從查詢結果建立分區資料表

您可以透過下列方式，從查詢結果建立分區資料表：

* 在 SQL 中，請使用 `CREATE TABLE ... AS SELECT` 陳述式。您可以使用這種方法，建立以時間單位資料欄或整數範圍分區的資料表，但無法以擷取時間分區。
* 使用 bq 指令列工具或 BigQuery API，為查詢設定目的地資料表。查詢執行時，BigQuery 會將結果寫入目的地資料表。這種做法適用於任何分割類型。
* 呼叫 `jobs.insert` API 方法，並在 `timePartitioning` 屬性或 `rangePartitioning` 屬性中指定分區。

### SQL

使用 [`CREATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) 陳述式。加入 [`PARTITION BY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#partition_expression) 子句來設定分區。

下列範例會建立以 `transaction_date` 資料欄為分區依據的資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE
     mydataset.newtable (transaction_id INT64, transaction_date DATE)
   PARTITION BY
     transaction_date
   AS (
     SELECT
       transaction_id, transaction_date
     FROM
       mydataset.mytable
   );
   ```

   使用 [`OPTIONS` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#table_option_list)設定資料表選項，例如[分區篩選器需求](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 如要從查詢建立分區資料表，請使用 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並加上 `--destination_table` 旗標和 `--time_partitioning_type` 旗標。

   按時間單位資料欄分區：

   ```
   bq query \
      --use_legacy_sql=false \
      --destination_table TABLE_NAME \
      --time_partitioning_field COLUMN \
      --time_partitioning_type UNIT_TIME \
      'QUERY_STATEMENT'
   ```

   擷取時間分區：

   ```
   bq query \
      --use_legacy_sql=false \
      --destination_table TABLE_NAME \
      --time_partitioning_type UNIT_TIME \
      'QUERY_STATEMENT'
   ```

   整數範圍分區：

   ```
   bq query \
      --use_legacy_sql=false \
      --destination_table PROJECT_ID:DATASET.TABLE \
      --range_partitioning COLUMN,START,END,INTERVAL \
      'QUERY_STATEMENT'
   ```

   更改下列內容：

   * PROJECT\_ID：專案 ID。如果省略此參數，系統會使用預設專案。
   * DATASET：專案中的資料集名稱。
   * TABLE：要建立的資料表名稱。
   * COLUMN：分割資料欄的名稱。
   * UNIT\_TIME：分區類型。支援的值包括 `DAY`、`HOUR`、`MONTH` 或 `YEAR`。
   * START：範圍分區的起始值 (含)。
   * END：範圍分區的結束值 (不含)。
   * INTERVAL：分區內每個範圍的寬度。
   * QUERY\_STATEMENT：用於填入資料表的查詢。

   下列範例會建立以 `transaction_date` 資料欄為分區依據的資料表，並使用每月分區。

   ```
   bq query \
      --use_legacy_sql=false \
      --destination_table mydataset.newtable \
      --time_partitioning_field transaction_date \
      --time_partitioning_type MONTH \
      'SELECT transaction_id, transaction_date FROM mydataset.mytable'
   ```

   下列範例會建立按 `customer_id` 資料欄分區的資料表，並使用整數範圍分區。

   ```
   bq query \
      --use_legacy_sql=false \
      --destination_table mydataset.newtable \
      --range_partitioning customer_id,0,100,10 \
      'SELECT * FROM mydataset.ponies'
   ```

   如果是擷取時間分區資料表，您也可以使用[分區修飾符](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#write-to-partition)，將資料載入特定分區。下列範例會建立新的擷取時間分區資料表，並將資料載入 `20180201` (2018 年 2 月 1 日) 分區：

   ```
   bq query \
      --use_legacy_sql=false  \
      --time_partitioning_type=DAY \
      --destination_table='newtable$20180201' \
      'SELECT * FROM mydataset.mytable'
   ```

### API

如要將查詢結果儲存至分區資料表，請呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法。設定 `query` 工作。在 `destinationTable` 中指定目的地資料表。在 `timePartitioning` 屬性或 `rangePartitioning` 屬性中指定分割。

## 將日期資料分割資料表轉換成擷取時間分區資料表

如果您先前建立的是日期資料分割資料表，可以使用 bq 指令列工具中的 [`partition`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_partition) 指令，將整組相關資料表轉換成單一擷取時間分區資料表。

```
bq --location=LOCATION partition \
    --time_partitioning_type=PARTITION_TYPE \
    --time_partitioning_expiration INTEGER \
    PROJECT_ID:SOURCE_DATASET.SOURCE_TABLE \
    PROJECT_ID:DESTINATION_DATASET.DESTINATION_TABLE
```

更改下列內容：

* LOCATION：位置名稱。`--location` 是選用旗標。
* PARTITION\_TYPE：分區類型。可能的值包括 `DAY`、`HOUR`、`MONTH` 或 `YEAR`。
* INTEGER：分區到期時間，以秒為單位。這個值沒有下限。到期時間為分區的世界標準時間日期加上該整數值。`time_partitioning_expiration` 是選用旗標。
* PROJECT\_ID：專案 ID。
* SOURCE\_DATASET：包含日期分片資料表的資料集。
* SOURCE\_TABLE：日期資料分割資料表的前置字串。
* DESTINATION\_DATASET：新分區資料表的資料集。
* DESTINATION\_TABLE：要建立的分區資料表名稱。

`partition` 指令不支援 `--label`、`--expiration`、`--add_tags` 或 `--description` 旗標。您可以在建立資料表後，在其中加入標籤、資料表到期時間、[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)和說明。

執行 `partition` 指令時，BigQuery 會建立複製工作，此工作會從資料分割資料表產生分區。

下列範例會從一組以 `sourcetable_` 為前置字串的日期資料分割資料表，建立名為 `mytable_partitioned` 的擷取時間分區資料表。新資料表會每天分區，分區到期時間為 259,200 秒 (3 天)。

```
bq partition \
    --time_partitioning_type=DAY \
    --time_partitioning_expiration 259200 \
    mydataset.sourcetable_ \
    mydataset.mytable_partitioned
```

如果日期資料分割資料表是 `sourcetable_20180126` 和 `sourcetable_20180127`，這項指令會建立下列分區：`mydataset.mytable_partitioned$20180126` 和 `mydataset.mytable_partitioned$20180127`。

## 分區資料表安全性

分區資料表的存取控管方式與標準資料表相同。詳情請參閱[資料表存取權控管簡介](https://docs.cloud.google.com/bigquery/docs/table-access-controls-intro?hl=zh-tw)。

## 後續步驟

* 如要瞭解如何管理及更新分區資料表，請參閱[管理分區資料表](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw)一文。
* 如要瞭解如何查詢分區資料表，請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]