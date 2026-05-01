* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 複製多個資料表 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

將多個來源資料表複製到指定目的地。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)

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

// copyMultiTable demonstrates using a copy job to copy multiple source tables into a single destination table.
func copyMultiTable(projectID, srcDatasetID string, srcTableIDs []string, dstDatasetID, dstTableID string) error {
	// projectID := "my-project-id"
	// srcDatasetID := "sourcedataset"
	// srcTableIDs := []string{"table1","table2"}
	// dstDatasetID = "destinationdataset"
	// dstTableID = "destinationtable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	srcDataset := client.Dataset(srcDatasetID)
	dstDataset := client.Dataset(dstDatasetID)
	var tableRefs []*bigquery.Table
	for _, v := range srcTableIDs {
		tableRefs = append(tableRefs, srcDataset.Table(v))
	}
	copier := dstDataset.Table(dstTableID).CopierFrom(tableRefs...)
	copier.WriteDisposition = bigquery.WriteTruncate
	job, err := copier.Run(ctx)
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
import com.google.cloud.bigquery.CopyJobConfiguration;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.TableId;
import java.util.Arrays;

public class CopyMultipleTables {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String destinationDatasetName = "MY_DATASET_NAME";
    String destinationTableId = "MY_TABLE_NAME";
    String sourceTable1Id = "MY_SOURCE_TABLE_1";
    String sourceTable2Id = "MY_SOURCE_TABLE_2";
    copyMultipleTables(destinationDatasetName, destinationTableId, sourceTable1Id, sourceTable2Id);
  }

  public static void copyMultipleTables(
      String destinationDatasetName,
      String destinationTableId,
      String sourceTable1Id,
      String sourceTable2Id) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId destinationTable = TableId.of(destinationDatasetName, destinationTableId);
      TableId sourceTable1 = TableId.of(destinationDatasetName, sourceTable1Id);
      TableId sourceTable2 = TableId.of(destinationDatasetName, sourceTable2Id);

      // For more information on CopyJobConfiguration see:
      // https://googleapis.dev/java/google-cloud-clients/latest/com/google/cloud/bigquery/JobConfiguration.html
      CopyJobConfiguration configuration =
          CopyJobConfiguration.newBuilder(
                  destinationTable, Arrays.asList(sourceTable1, sourceTable2))
              .build();

      // For more information on Job see:
      // https://googleapis.dev/java/google-cloud-clients/latest/index.html?com/google/cloud/bigquery/package-summary.html
      Job job = bigquery.create(JobInfo.of(configuration));

      // Blocks until this job completes its execution, either failing or succeeding.
      Job completedJob = job.waitFor();
      if (completedJob == null) {
        System.out.println("Job not executed since it no longer exists.");
        return;
      } else if (completedJob.getStatus().getError() != null) {
        System.out.println(
            "BigQuery was unable to copy tables due to an error: \n" + job.getStatus().getError());
        return;
      }
      System.out.println("Table copied successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Table copying job was interrupted. \n" + e.toString());
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

async function copyTableMultipleSource() {
  // Copy multiple source tables to a given destination.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // sourceTable = 'my_table';
  // destinationTable = 'testing';

  // Create a client
  const dataset = bigquery.dataset(datasetId);

  const metadata = {
    createDisposition: 'CREATE_NEVER',
    writeDisposition: 'WRITE_TRUNCATE',
  };

  // Create table references
  const table = dataset.table(sourceTable);
  const yourTable = dataset.table(destinationTable);

  // Copy table
  const [apiResponse] = await table.copy(yourTable, metadata);
  console.log(apiResponse.configuration.copy);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dest_table_id to the ID of the destination table.
# dest_table_id = "your-project.your_dataset.your_table_name"

# TODO(developer): Set table_ids to the list of the IDs of the original tables.
# table_ids = ["your-project.your_dataset.your_table_name", ...]

job = client.copy_table(table_ids, dest_table_id)  # Make an API request.
job.result()  # Wait for the job to complete.

print("The tables {} have been appended to {}".format(table_ids, dest_table_id))
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]