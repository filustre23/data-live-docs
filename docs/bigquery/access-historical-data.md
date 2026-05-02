* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 存取歷來資料

BigQuery 可讓您查詢及還原儲存在 BigQuery 中的資料，這些資料是在[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)時間範圍內變更或刪除。

## 查詢特定時間點的資料

您可以使用 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 子句，在時間旅行視窗內，查詢資料表在任何時間點的歷史資料。這個子句會採用常數時間戳記運算式，並參照該時間戳記當前的資料表版本。資料表必須儲存在 BigQuery 中，不得為外部資料表。使用 `SYSTEM_TIME AS OF` 時，資料表大小沒有限制。

舉例來說，下列查詢會傳回一小時前的資料表歷史版本：

```
SELECT *
FROM `mydataset.mytable`
  FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);
```

**注意：** GoogleSQL 支援 `FOR SYSTEM_TIME AS OF` 子句。
在舊版 SQL 中，[時間修飾符](https://docs.cloud.google.com/bigquery/docs/table-decorators?hl=zh-tw#time_decorators)提供對等功能。

如果時間戳記指定的時間早於時間回溯期，或早於資料表建立時間，查詢就會失敗並傳回類似下列的錯誤：

```
Invalid snapshot time 1601168925462 for table
myproject:mydataset.table1@1601168925462. Cannot read before 1601573410026.
```

使用 `CREATE OR REPLACE TABLE` 陳述式替換現有資料表後，您可以使用 `FOR SYSTEM_TIME AS OF` 查詢資料表的先前版本。

如果資料表已刪除，查詢就會失敗，並傳回類似下列的錯誤：

```
Not found: Table myproject:mydataset.table was not found in location LOCATION
```

## 從特定時間點還原資料表

如要從歷來資料還原資料表，請將歷來資料複製到新資料表。只要在時間回溯期內還原資料表，即使資料表已遭刪除或過期，您仍可複製歷來資料。

從歷史資料還原資料表時，來源資料表的[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)不會複製到目的地資料表。資料表分區資訊也不會複製到目的地資料表。如要重新建立原始資料表的分區架構，請在 [Cloud Logging](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw) 中查看初始資料表建立要求，並使用該資訊將還原的資料表分區。

如果資料表已刪除，但仍在時間旅行視窗內，您可以將資料表複製到新資料表，並使用 `@<time>` 時間修飾符，藉此還原資料表。即使使用時間修飾符，您也無法查詢已刪除的資料表。你必須先還原。

請搭配 `@<time>` 時間裝飾器使用下列語法：

* `tableid@TIME`，其中 `TIME` 是自 Unix 紀元起經過的毫秒數。
* `tableid@-TIME_OFFSET`，其中 `TIME_OFFSET` 是相對於目前時間的偏移量 (以毫秒為單位)。
* `tableid@0`：指定可用的最舊歷來資料。

如要還原資料表，請選取下列其中一個選項：

### 控制台

您無法使用 Google Cloud 控制台還原已刪除的資料表。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 如要還原資料表，請先確定資料表存在時間的 UNIX 時間戳記 (以毫秒為單位)。您可以使用 Linux `date` 指令，從一般時間戳記值產生 Unix 時間戳記：

   ```
   date -d '2023-08-04 16:00:34.456789Z' +%s000
   ```
3. 接著，使用 `bq copy` 指令搭配 `@<time>` 時空旅行修飾符，執行資料表複製作業。

   舉例來說，請輸入下列指令，將時間為 `1418864998000` 的 `mydataset.mytable` 資料表複製到新的資料表 `mydataset.newtable` 中。

   ```
   bq cp mydataset.mytable@1418864998000 mydataset.newtable
   ```

   (選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

   您也可以指定相對偏移量。以下範例會複製一小時前的資料表版本：

   ```
   bq cp mydataset.mytable@-3600000 mydataset.newtable
   ```

   **注意：** 如果嘗試復原時間旅行視窗之前的資料，或是復原資料表建立之前的資料，系統會傳回 `Invalid time travel timestamp` 錯誤。詳情請參閱「[排解資料表復原問題](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw#troubleshoot_table_recovery)」。

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
		return fmt.Errorf("bigquery.NewClient: %v", err)
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
import com.google.cloud.bigquery.TableId;

// Sample to undeleting a table
public class UndeleteTable {

  public static void runUndeleteTable() {
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

      // "Accidentally" delete the table.
      bigquery.delete(TableId.of(datasetName, tableName));

      // Record the current time.  We'll use this as the snapshot time
      // for recovering the table.
      long snapTime = System.currentTimeMillis();

      // Construct the restore-from tableID using a snapshot decorator.
      String snapshotTableId = String.format("%s@%d", tableName, snapTime);

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
  await bigquery
    .dataset(datasetId)
    .table(tableId)
    .delete();

  console.log(`Table ${tableId} deleted.`);

  // Construct the restore-from table ID using a snapshot decorator.
  const snapshotTableId = `${tableId}@${snapshotEpoch}`;

  // Construct and run a copy job.
  await bigquery
    .dataset(datasetId)
    .table(snapshotTableId)
    .copy(bigquery.dataset(datasetId).table(recoveredTableId));

  console.log(
    `Copied data from deleted table ${tableId} to ${recoveredTableId}`
  );
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

如果您預期之後可能會還原資料表，但時間超出時空旅行時間範圍，請建立資料表的快照。詳情請參閱「[資料表快照簡介](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)」。

您無法直接還原邏輯檢視區塊。詳情請參閱「[還原檢視畫面](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw#restore_a_view)」。

## 後續步驟

* 進一步瞭解[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。
* 進一步瞭解[時間旅行和容錯安全機制中的資料保留](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)。
* 進一步瞭解如何[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]