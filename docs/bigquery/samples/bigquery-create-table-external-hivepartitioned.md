Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用 Hive 分區建立外部資料表 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用 Hive 分區建立外部資料表。

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

// createTableExternalHivePartitioned demonstrates creating an external table with hive partitioning.
func createTableExternalHivePartitioned(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydatasetid"
	// tableID := "mytableid"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	// First, we'll define table metadata to represent a table that's backed by parquet files held in
	// Cloud Storage.
	//
	// Example file:
	// gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/dt=2020-11-15/file1.parquet
	metadata := &bigquery.TableMetadata{
		Description: "An example table that demonstrates hive partitioning against external parquet files",
		ExternalDataConfig: &bigquery.ExternalDataConfig{
			SourceFormat: bigquery.Parquet,
			SourceURIs:   []string{"gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/*"},
			AutoDetect:   true,
		},
	}

	// The layout of the files in here is compatible with the layout requirements for hive partitioning,
	// so we can add an optional Hive partitioning configuration to leverage the object paths for deriving
	// partitioning column information.
	//
	// For more information on how partitions are extracted, see:
	// https://cloud.google.com/bigquery/docs/hive-partitioned-queries-gcs
	//
	// We have a "/dt=YYYY-MM-DD/" path component in our example files as documented above.  Autolayout will
	// expose this as a column named "dt" of type DATE.
	metadata.ExternalDataConfig.HivePartitioningOptions = &bigquery.HivePartitioningOptions{
		Mode:                   bigquery.AutoHivePartitioningMode,
		SourceURIPrefix:        "gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/",
		RequirePartitionFilter: true,
	}

	// Create the external table.
	tableRef := client.Dataset(datasetID).Table(tableID)
	if err := tableRef.Create(ctx, metadata); err != nil {
		return fmt.Errorf("table creation failure: %w", err)
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
import com.google.cloud.bigquery.ExternalTableDefinition;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.HivePartitioningOptions;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;

// Sample to create external table using hive partitioning
public class CreateTableExternalHivePartitioned {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/hive-partitioning-samples/customlayout/*";
    String sourceUriPrefix =
        "gs://cloud-samples-data/bigquery/hive-partitioning-samples/customlayout/{pkey:STRING}/";
    createTableExternalHivePartitioned(datasetName, tableName, sourceUriPrefix, sourceUri);
  }

  public static void createTableExternalHivePartitioned(
      String datasetName, String tableName, String sourceUriPrefix, String sourceUri) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Configuring partitioning options
      HivePartitioningOptions hivePartitioningOptions =
          HivePartitioningOptions.newBuilder()
              .setMode("CUSTOM")
              .setRequirePartitionFilter(true)
              .setSourceUriPrefix(sourceUriPrefix)
              .build();

      TableId tableId = TableId.of(datasetName, tableName);
      ExternalTableDefinition customTable =
          ExternalTableDefinition.newBuilder(sourceUri, FormatOptions.parquet())
              .setAutodetect(true)
              .setHivePartitioningOptions(hivePartitioningOptions)
              .build();
      bigquery.create(TableInfo.of(tableId, customTable));
      System.out.println("External table created using hivepartitioningoptions");
    } catch (BigQueryException e) {
      System.out.println("External table was not created" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# Demonstrates creating an external table with hive partitioning.

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "your-project.your_dataset.your_table_name"

# TODO(developer): Set source uri.
# Example file:
# gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/dt=2020-11-15/file1.parquet
uri = "gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/*"

# TODO(developer): Set source uri prefix.
source_uri_prefix = (
    "gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/"
)

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# Configure the external data source.
external_config = bigquery.ExternalConfig("PARQUET")
external_config.source_uris = [uri]
external_config.autodetect = True

# Configure partitioning options.
hive_partitioning_opts = bigquery.HivePartitioningOptions()

# The layout of the files in here is compatible with the layout requirements for hive partitioning,
# so we can add an optional Hive partitioning configuration to leverage the object paths for deriving
# partitioning column information.

# For more information on how partitions are extracted, see:
# https://cloud.google.com/bigquery/docs/hive-partitioned-queries-gcs

# We have a "/dt=YYYY-MM-DD/" path component in our example files as documented above.
# Autolayout will expose this as a column named "dt" of type DATE.
hive_partitioning_opts.mode = "AUTO"
hive_partitioning_opts.require_partition_filter = True
hive_partitioning_opts.source_uri_prefix = source_uri_prefix

external_config.hive_partitioning = hive_partitioning_opts

table = bigquery.Table(table_id)
table.external_data_configuration = external_config

table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]