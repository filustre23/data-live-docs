Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立叢集資料表

您可以在 BigQuery 中使用叢集資料表，減少查詢處理的資料量。

使用叢集資料表時，系統會根據指定資料欄 (也稱為*叢集資料欄*) 的值整理資料表資料。BigQuery 會依叢集資料欄排序資料，然後將具有相似值的資料列儲存在相同或鄰近的實體區塊中。當查詢依分群資料欄篩選資料時，BigQuery 只會有效率地掃描相關區塊，並略過不符合篩選條件的資料。

如要瞭解詳情，請參考下列資源：

* 如要進一步瞭解 BigQuery 中的叢集資料表，請參閱[叢集資料表簡介](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。
* 如要瞭解如何使用及控管叢集資料表的存取權，請參閱[管理叢集資料表](https://docs.cloud.google.com/bigquery/docs/manage-clustered-tables?hl=zh-tw)。

## 事前準備

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

### 資料表命名規定

在 BigQuery 中建立資料表時，每個資料集裡的資料表名稱不得重複。資料表名稱可以：

* 包含的字元總計最多 1,024 個 UTF-8 位元組。
* 包含類別 L (字母)、M (標記)、N (數字)、Pc (連接符，包括底線)、Pd (破折號)、Zs (空格) 的 Unicode 字元。詳情請參閱「[一般類別](https://wikipedia.org/wiki/Unicode_character_property#General_Category)」。

以下都是有效的資料表名稱範例：`table 01`、`ग्राहक`、`00_お客様`、`étudiant-01`。

注意事項：

* 根據預設，資料表名稱會區分大小寫。`mytable` 和 `MyTable` 可以共存在同一個資料集中，除非是[已關閉大小寫區分功能的資料集](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_case-insensitive_dataset)。
* 部分資料表名稱和資料表名稱前置字串已保留。如果收到錯誤訊息，指出資料表名稱或前置字元已保留，請選取其他名稱，然後再試一次。
* 如果您在序列中加入多個點運算子 (`.`)，系統會自動移除重複的運算子。

  例如：
  `project_name....dataset_name..table_name`

  變成這樣：
  `project_name.dataset_name.table_name`

### 分群資料欄需求

在 BigQuery 中建立資料表時，您可以指定用於建立分群資料表的欄。資料表建立完成後，您可以修改用於建立分群資料表的資料欄。詳情請參閱「[修改叢集規格](https://docs.cloud.google.com/bigquery/docs/manage-clustered-tables?hl=zh-tw#modifying-cluster-spec)」。

叢集欄位必須是高層級、非重複欄位，且屬於下列任一項資料類型：

* `BIGNUMERIC`
* `BOOL`
* `DATE`
* `DATETIME`
* `GEOGRAPHY`
* `INT64`
* `NUMERIC`
* `RANGE`
* `STRING`
* `TIMESTAMP`

您最多可指定四個叢集資料欄，當您指定多個叢集資料欄時，資料欄的順序將決定資料的排序方式。舉例來說，如果資料表是依資料欄 a、b、c 來進行叢集，則資料也會按照相同順序排序，即第一順位是資料欄 a、第二順位是資料欄 b、第三順位是資料欄 c。按照最佳做法，最常用以進行資料篩選或匯總的資料欄應排在第一順位。

叢集資料欄順序亦會影響資料查詢的效能與定價。如要瞭解查詢叢集資料表的最佳做法，請參閱[查詢叢集資料表](https://docs.cloud.google.com/bigquery/docs/querying-clustered-tables?hl=zh-tw)一文。

## 透過結構定義建立空白分群資料表

如何使用結構定義建立空白分群資料表：

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
3. 在「Schema」(結構定義) 區段中，輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。
   你可以使用下列任一方法手動輸入結構定義資訊：
   * 選項 1：按一下「以文字形式編輯」，然後以 JSON 陣列的形式貼上結構定義。如果您使用 JSON 陣列，可透過與[建立 JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)一樣的程序產生結構定義。您可以輸入下列指令，查看現有資料表的 JSON 格式結構定義：

     ```
         bq show --format=prettyjson dataset.table
     ```
   * 選項 2：按一下 add\_box
     「新增欄位」，然後輸入表格結構定義。指定每個欄位的「Name」(名稱)、「[Type](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#standard_sql_data_types)」(類型) 和「[Mode](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#modes)」(模式)。
4. 針對「Clustering order」(叢集處理順序)，輸入一到四個以半形逗號分隔的資料欄名稱。
5. 選用步驟：如要使用客戶自行管理的加密金鑰，請在「Advanced options」(進階選項) 部分選取「Use a customer-managed encryption key (CMEK)」(使用客戶自行管理的加密金鑰 (CMEK)) 選項。根據預設，BigQuery 會使用 Google-owned and Google-managed encryption key[加密靜態儲存的客戶內容](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
6. 點選「建立資料表」。

### SQL

使用 [`CREATE TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)指令，並加上 `CLUSTER BY` 選項。下列範例會在 `mydataset` 中建立名為 `myclusteredtable` 的分群資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE mydataset.myclusteredtable
   (
     customer_id STRING,
     transaction_amount NUMERIC
   )
   CLUSTER BY
     customer_id
     OPTIONS (
       description = 'a table clustered by customer_id');
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用加上以下旗標的 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令：

* `--table` (或 `-t` 捷徑)。
* `--schema`。您可利用內嵌方式或以 JSON 結構定義檔提供資料表結構定義。
* `--clustering_fields`。您最多可指定四個叢集資料欄。

可選用的參數包括 `--expiration`、`--description`、`--time_partitioning_type`、`--time_partitioning_field`、`--time_partitioning_expiration`、`--destination_kms_key` 和 `--label`。

如要建立非預設專案中的資料表，請使用下列格式將專案 ID 新增至資料集：`project_id:dataset`。

本文不示範 `--destination_kms_key`。如要進一步瞭解如何使用 `--destination_kms_key`，請參閱[客戶管理的加密金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)說明。

輸入下列指令，建立含有結構定義的空白分群資料表：

```
bq mk \
    --table \
    --expiration INTEGER1 \
    --schema SCHEMA \
    --clustering_fields CLUSTER_COLUMNS \
    --description "DESCRIPTION" \
    --label KEY:VALUE,KEY:VALUE \
    PROJECT_ID:DATASET.TABLE
```

更改下列內容：

* `INTEGER1`：資料表的預設生命週期 (以秒為單位)。最小值是 3,600 秒 (1 小時)。到期時間為目前世界標準時間加整數值。如果您在建立資料表時設定了資料表到期時間，系統會忽略資料集的預設資料表到期時間設定。設定這個值會在指定時間到期後刪除資料表。
* `SCHEMA`：格式為 `COLUMN:DATA_TYPE,COLUMN:DATA_TYPE` 的內嵌結構定義，或您本機電腦上的 JSON 結構定義檔案路徑。
* `CLUSTER_COLUMNS`：以半形逗號分隔的清單，最多包含四個叢集資料欄。清單不得包含任何空格。
* `DESCRIPTION`：置於括號中的資料表說明。
* `KEY:VALUE`：代表[標籤](https://docs.cloud.google.com/bigquery/docs/labels?hl=zh-tw)的鍵/值組合。您可以用逗號分隔的清單輸入多個標籤。
* `PROJECT_ID`：您的專案 ID。
* `DATASET`：專案中的資料集。
* `TABLE`：您要建立的資料表名稱。

您在指令列中指定結構定義時，無法加入 `RECORD` ([`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)) 類型和資料欄說明，也不能指定資料欄模式。所有模式均預設為 `NULLABLE`。如要加入說明、模式和 `RECORD` 類型，請改為[提供 JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)。

範例：

輸入下列指令，在預設專案中的 `mydataset` 內建立名為 `myclusteredtable` 的分群資料表。資料表到期時間設為 2,592,000 秒 (1 個月 30 天)、說明設為 `This is my clustered table`，而標籤則設為 `organization:development`。此指令使用 `-t` 捷徑，而非 `--table`。

結構定義以內嵌方式指定為：`timestamp:timestamp,customer_id:string,transaction_amount:float`。所指定的叢集欄位 `customer_id` 用於叢集資料表。

```
bq mk \
    -t \
    --expiration 2592000 \
    --schema 'timestamp:timestamp,customer_id:string,transaction_amount:float' \
    --clustering_fields customer_id \
    --description "This is my clustered table" \
    --label org:dev \
    mydataset.myclusteredtable
```

輸入下列指令，在 `myotherproject` (而非預設專案) 中建立名為 `myclusteredtable` 的分群資料表，說明設為 `This is my clustered table`，標籤則設為 `organization:development`。此指令使用 `-t` 捷徑，而非 `--table`。這個指令不會指定資料表到期時間。如果資料集有預設資料表到期時間，系統會直接套用這個時間。如果資料集沒有預設資料表到期時間，資料表將永不過期。

結構定義在本機 JSON 檔案 `/tmp/myschema.json` 中指定。`customer_id` 欄位用於叢集資料表。

```
bq mk \
    -t \
    --expiration 2592000 \
    --schema /tmp/myschema.json \
    --clustering_fields=customer_id \
    --description "This is my clustered table" \
    --label org:dev \
    myotherproject:mydataset.myclusteredtable
```

建立資料表後，您可以更新資料表的[說明](https://docs.cloud.google.com/bigquery/docs/samples/bigquery-update-table-description?hl=zh-tw)和[標籤](https://docs.cloud.google.com/bigquery/docs/labels?hl=zh-tw#creating_and_updating_table_and_view_labels)。

### Terraform

請使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 Cloud Resource Manager API。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會建立名為 `mytable` 的資料表，並以 `ID` 和 `Created` 資料欄做為叢集依據：

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

  clustering = ["ID", "Created"]

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
  },
 {
   "name": "Created",
   "type": "TIMESTAMP"
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

使用指定 `clustering.fields` 屬性和 `schema` 屬性的已定義[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法。

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
table.clustering_fields = ["city", "zipcode"]
table = client.create_table(table)  # Make an API request.
print(
    "Created clustered table {}.{}.{}".format(
        table.project, table.dataset_id, table.table_id
    )
)
```

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

// createTableClustered demonstrates creating a BigQuery table with advanced properties like
// partitioning and clustering features.
func createTableClustered(projectID, datasetID, tableID string) error {
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
		{Name: "timestamp", Type: bigquery.TimestampFieldType},
		{Name: "origin", Type: bigquery.StringFieldType},
		{Name: "destination", Type: bigquery.StringFieldType},
		{Name: "amount", Type: bigquery.NumericFieldType},
	}
	metaData := &bigquery.TableMetadata{
		Schema: sampleSchema,
		TimePartitioning: &bigquery.TimePartitioning{
			Field:      "timestamp",
			Expiration: 90 * 24 * time.Hour,
		},
		Clustering: &bigquery.Clustering{
			Fields: []string{"origin", "destination"},
		},
	}
	tableRef := client.Dataset(datasetID).Table(tableID)
	if err := tableRef.Create(ctx, metaData); err != nil {
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
import com.google.cloud.bigquery.Clustering;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.StandardTableDefinition;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;
import com.google.cloud.bigquery.TimePartitioning;
import com.google.common.collect.ImmutableList;

public class CreateClusteredTable {
  public static void runCreateClusteredTable() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    createClusteredTable(datasetName, tableName);
  }

  public static void createClusteredTable(String datasetName, String tableName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);

      TimePartitioning partitioning = TimePartitioning.of(TimePartitioning.Type.DAY);

      Schema schema =
          Schema.of(
              Field.of("name", StandardSQLTypeName.STRING),
              Field.of("post_abbr", StandardSQLTypeName.STRING),
              Field.of("date", StandardSQLTypeName.DATE));

      Clustering clustering =
          Clustering.newBuilder().setFields(ImmutableList.of("name", "post_abbr")).build();

      StandardTableDefinition tableDefinition =
          StandardTableDefinition.newBuilder()
              .setSchema(schema)
              .setTimePartitioning(partitioning)
              .setClustering(clustering)
              .build();
      TableInfo tableInfo = TableInfo.newBuilder(tableId, tableDefinition).build();

      bigquery.create(tableInfo);
      System.out.println("Clustered table created successfully");
    } catch (BigQueryException e) {
      System.out.println("Clustered table was not created. \n" + e.toString());
    }
  }
}
```

## 從查詢結果建立分群資料表

從查詢結果建立分群資料表的作法有兩種：

* 將結果寫入新的目的地資料表並指定叢集資料欄，
* 使用 DDL `CREATE TABLE AS SELECT` 陳述式。如要進一步瞭解此做法，請參閱「使用資料定義語言陳述式」頁面中的[從查詢結果建立分群資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_clustered_table_from_the_result_of_a_query)一節。

您可以藉由查詢分區資料表或非分區資料表的方式建立分群資料表。但不能利用查詢結果將現有的資料表變更為叢集資料表。

從查詢結果建立分群資料表時，必須使用標準 SQL。系統不支援使用舊版 SQL 查詢叢集資料表，或將查詢結果寫入叢集資料表。

### SQL

如要從查詢結果建立分群資料表，請使用 [`CREATE TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)搭配 `CLUSTER BY` 選項。下列範例會查詢現有的非叢集資料表，建立依 `customer_id` 叢集的新資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE mydataset.clustered_table
   (
     customer_id STRING,
     transaction_amount NUMERIC
   )
   CLUSTER BY
     customer_id
   AS (
     SELECT * FROM mydataset.unclustered_table
   );
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

輸入下列指令，從查詢結果中建立新的叢集目的地資料表：

```
bq --location=LOCATION query \
    --use_legacy_sql=false 'QUERY'
```

更改下列內容：

* `LOCATION`：位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `QUERY`：採用 GoogleSQL 語法的查詢。您無法使用舊版 SQL 查詢叢集資料表，或將查詢結果寫入叢集資料表。該查詢可包含 `CREATE TABLE`
  [DDL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw) 陳述式，以指定建立分群資料表的選項。您可以使用 DDL 取代指定個別指令列旗標的做法。

範例：

輸入下列指令，將查詢結果寫入 `mydataset` 中名為 `myclusteredtable` 的叢集目的地資料表。`mydataset` 在您的預設專案中。查詢會從非分區資料表 mytable 中擷取資料，資料表的 `customer_id` 資料欄用於叢集資料表。資料表的 `timestamp` 資料欄用於建立分區資料表。

```
bq query --use_legacy_sql=false \
    'CREATE TABLE
       mydataset.myclusteredtable
     PARTITION BY
       DATE(timestamp)
     CLUSTER BY
       customer_id
     AS (
       SELECT
         *
       FROM
         `mydataset.mytable`
     );'
```

### API

如要將查詢結果儲存到分群資料表，請呼叫 [`jobs.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)、設定 [`query` 工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationQuery)，然後加入可建立分群資料表的 `CREATE TABLE` [DDL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw) 陳述式。

在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，利用 `location` 屬性指定您的位置。

## 在載入資料時建立叢集資料表

載入資料到新資料表時，您可以指定分群資料欄來建立分群資料表。您不必在資料載入資料表之前，事先建立空白的資料表，因為您可以同時建立分群資料表並載入資料。

有關如何載入資料的詳情，請參閱[將資料載入 BigQuery 的簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)。

如要在定義載入工作時定義叢集，請進行以下操作：

### SQL

使用 [`LOAD DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)。以下範例會載入 AVRO 資料，建立依 `transaction_date` 欄位分區，並依 `customer_id` 欄位分群的資料表。同時設定分區在三天後過期。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   LOAD DATA INTO mydataset.mytable
   PARTITION BY transaction_date
   CLUSTER BY customer_id
     OPTIONS (
       partition_expiration_days = 3)
   FROM FILES(
     format = 'AVRO',
     uris = ['gs://bucket/path/file.avro']);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### API

如要在透過載入工作建立資料表時定義叢集設定，您可以填入資料表的 [`Clustering`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#clustering) 屬性。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// importClusteredTable demonstrates creating a table from a load job and defining partitioning and clustering
// properties.
func importClusteredTable(projectID, destDatasetID, destTableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/sample-transactions/transactions.csv")
	gcsRef.SkipLeadingRows = 1
	gcsRef.Schema = bigquery.Schema{
		{Name: "timestamp", Type: bigquery.TimestampFieldType},
		{Name: "origin", Type: bigquery.StringFieldType},
		{Name: "destination", Type: bigquery.StringFieldType},
		{Name: "amount", Type: bigquery.NumericFieldType},
	}
	loader := client.Dataset(destDatasetID).Table(destTableID).LoaderFrom(gcsRef)
	loader.TimePartitioning = &bigquery.TimePartitioning{
		Field: "timestamp",
	}
	loader.Clustering = &bigquery.Clustering{
		Fields: []string{"origin", "destination"},
	}
	loader.WriteDisposition = bigquery.WriteEmpty

	job, err := loader.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}

	if status.Err() != nil {
		return fmt.Errorf("job completed with error: %v", status.Err())
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
import com.google.cloud.bigquery.Clustering;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TimePartitioning;
import com.google.common.collect.ImmutableList;

public class LoadTableClustered {

  public static void runLoadTableClustered() throws Exception {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "/path/to/file.csv";
    loadTableClustered(datasetName, tableName, sourceUri);
  }

  public static void loadTableClustered(String datasetName, String tableName, String sourceUri)
      throws Exception {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);

      Schema schema =
          Schema.of(
              Field.of("name", StandardSQLTypeName.STRING),
              Field.of("post_abbr", StandardSQLTypeName.STRING),
              Field.of("date", StandardSQLTypeName.DATE));

      TimePartitioning partitioning = TimePartitioning.of(TimePartitioning.Type.DAY);

      Clustering clustering =
          Clustering.newBuilder().setFields(ImmutableList.of("name", "post_abbr")).build();

      LoadJobConfiguration loadJobConfig =
          LoadJobConfiguration.builder(tableId, sourceUri)
              .setFormatOptions(FormatOptions.csv())
              .setSchema(schema)
              .setTimePartitioning(partitioning)
              .setClustering(clustering)
              .build();

      Job loadJob = bigquery.create(JobInfo.newBuilder(loadJobConfig).build());

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
      System.out.println("Data successfully loaded into clustered table during load job");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Data not loaded into clustered table during load job \n" + e.toString());
    }
  }
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

job_config = bigquery.LoadJobConfig(
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
    schema=[
        bigquery.SchemaField("timestamp", bigquery.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("origin", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("destination", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("amount", bigquery.SqlTypeNames.NUMERIC),
    ],
    time_partitioning=bigquery.TimePartitioning(field="timestamp"),
    clustering_fields=["origin", "destination"],
)

job = client.load_table_from_uri(
    ["gs://cloud-samples-data/bigquery/sample-transactions/transactions.csv"],
    table_id,
    job_config=job_config,
)

job.result()  # Waits for the job to complete.

table = client.get_table(table_id)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
)
```

## 後續步驟

* 如要瞭解如何使用叢集資料表，請參閱[管理叢集資料表](https://docs.cloud.google.com/bigquery/docs/manage-clustered-tables?hl=zh-tw)。
* 關於如何查詢叢集資料表，請參閱[查詢叢集資料表](https://docs.cloud.google.com/bigquery/docs/querying-clustered-tables?hl=zh-tw)一文。
* 如需 BigQuery 中的分區資料表支援總覽，請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。
* 如要瞭解如何建立分區資料表，請參閱[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)。
* 如要查看 `INFORMATION_SCHEMA` 的總覽，請參閱「[BigQuery `INFORMATION_SCHEMA` 簡介](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]