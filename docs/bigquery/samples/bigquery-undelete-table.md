Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 取消刪除 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

取消刪除資料表。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [還原已刪除的資料表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw)

## 程式碼範例

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

// deleteAndUndeleteTable demonstrates how to recover a deleted table by copying it from a point in time
// that predates the deletion event.
func deleteAndUndeleteTable(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	ds := client.Dataset(datasetID)
	if _, err := ds.Table(tableID).Metadata(ctx); err != nil {
		return err
	}
	// Record the current time.  We'll use this as the snapshot time
	// for recovering the table.
	snapTime := time.Now()

	// "Accidentally" delete the table.
	if err := client.Dataset(datasetID).Table(tableID).Delete(ctx); err != nil {
		return err
	}

	// Construct the restore-from tableID using a snapshot decorator.
	snapshotTableID := fmt.Sprintf("%s@%d", tableID, snapTime.UnixNano()/1e6)
	// Choose a new table ID for the recovered table data.
	recoverTableID := fmt.Sprintf("%s_recovered", tableID)

	// Construct and run a copy job.
	copier := ds.Table(recoverTableID).CopierFrom(ds.Table(snapshotTableID))
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

	ds.Table(recoverTableID).Delete(ctx)
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
import com.google.cloud.bigquery.Table;
import com.google.cloud.bigquery.TableId;
import org.threeten.bp.Instant;

// Sample to undeleting a table
public class UndeleteTable {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_TABLE";
    String recoverTableName = "MY_RECOVER_TABLE_TABLE";
    undeleteTable(datasetName, tableName, recoverTableName);
  }

  public static void undeleteTable(String datasetName, String tableName, String recoverTableName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Record the current time.  We'll use this as the snapshot time
      // for recovering the table.
      long snapshotEpoch = Instant.now().toEpochMilli();

      // ...

      // "Accidentally" delete the table.
      bigquery.delete(TableId.of(datasetName, tableName));

      // Construct the restore-from tableID using a snapshot decorator.
      String snapshotTableId = String.format("%s@%d", tableName, snapshotEpoch);

      // Construct and run a copy job.
      CopyJobConfiguration configuration =
          CopyJobConfiguration.newBuilder(
                  // Choose a new table ID for the recovered table data.
                  TableId.of(datasetName, recoverTableName),
                  TableId.of(datasetName, snapshotTableId))
              .build();

      Job job = bigquery.create(JobInfo.of(configuration));
      job = job.waitFor();
      if (job.isDone() && job.getStatus().getError() == null) {
        System.out.println("Undelete table recovered successfully.");
      } else {
        System.out.println(
            "BigQuery was unable to copy the table due to an error: \n"
                + job.getStatus().getError());
        return;
      }
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Table not found. \n" + e.toString());
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

async function undeleteTable() {
  // Undeletes "my_table_to_undelete" from "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table_to_undelete";
  // const recoveredTableId = "my_recovered_table";

  /**
   * TODO(developer): Choose an appropriate snapshot point as epoch milliseconds.
   * For this example, we choose the current time as we're about to delete the
   * table immediately afterwards.
   */
  const snapshotEpoch = Date.now();

  // Delete the table
  await bigquery.dataset(datasetId).table(tableId).delete();

  console.log(`Table ${tableId} deleted.`);

  // Construct the restore-from table ID using a snapshot decorator.
  const snapshotTableId = `${tableId}@${snapshotEpoch}`;

  // Construct and run a copy job.
  await bigquery
    .dataset(datasetId)
    .table(snapshotTableId)
    .copy(bigquery.dataset(datasetId).table(recoveredTableId));

  console.log(
    `Copied data from deleted table ${tableId} to ${recoveredTableId}`,
  );
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/**
 * Restore a deleted table from its snapshot.
 *
 * @param string $projectId The project Id of your Google Cloud Project.
 * @param string $datasetId The BigQuery dataset ID.
 * @param string $tableId Table ID of the table to delete.
 * @param string $restoredTableId Table Id for the restored table.
 */
function undelete_table(
    string $projectId,
    string $datasetId,
    string $tableId,
    string $restoredTableId
): void {
    $bigQuery = new BigQueryClient(['projectId' => $projectId]);
    $dataset = $bigQuery->dataset($datasetId);

    // Choose an appropriate snapshot point as epoch milliseconds.
    // For this example, we choose the current time as we're about to delete the
    // table immediately afterwards
    $snapshotEpoch = date_create()->format('Uv');

    // Delete the table.
    $dataset->table($tableId)->delete();

    // Construct the restore-from table ID using a snapshot decorator.
    $snapshotId = "{$tableId}@{$snapshotEpoch}";

    // Restore the deleted table
    $restoredTable = $dataset->table($restoredTableId);
    $copyConfig = $dataset->table($snapshotId)->copy($restoredTable);
    $job = $bigQuery->runJob($copyConfig);

    // check if the job is complete
    $job->reload();
    if (!$job->isComplete()) {
        throw new \Exception('Job has not yet completed', 500);
    }
    // check if the job has errors
    if (isset($job->info()['status']['errorResult'])) {
        $error = $job->info()['status']['errorResult']['message'];
        printf('Error running job: %s' . PHP_EOL, $error);
    } else {
        print('Snapshot restored successfully' . PHP_EOL);
    }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import time

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Choose a table to recover.
# table_id = "your-project.your_dataset.your_table"

# TODO(developer): Choose a new table ID for the recovered table data.
# recovered_table_id = "your-project.your_dataset.your_table_recovered"

# TODO(developer): Choose an appropriate snapshot point as epoch
# milliseconds. For this example, we choose the current time as we're about
# to delete the table immediately afterwards.
snapshot_epoch = int(time.time() * 1000)

# ...

# "Accidentally" delete the table.
client.delete_table(table_id)  # Make an API request.

# Construct the restore-from table ID using a snapshot decorator.
snapshot_table_id = "{}@{}".format(table_id, snapshot_epoch)

# Construct and run a copy job.
job = client.copy_table(
    snapshot_table_id,
    recovered_table_id,
    # Must match the source and destination tables location.
    location="US",
)  # Make an API request.

job.result()  # Wait for the job to complete.

print(
    "Copied data from deleted table {} to {}".format(table_id, recovered_table_id)
)
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]