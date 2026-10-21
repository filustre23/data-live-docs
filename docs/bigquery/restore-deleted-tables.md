Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 還原已刪除的資料表

本文說明如何在 BigQuery 中還原 (或*取消刪除*) 已刪除的資料表。您可以在資料集指定的時間回溯期內還原已刪除的資料表，包括明確刪除的資料表，以及因資料表到期而隱含刪除的資料表。您也可以[設定時空旅行視窗](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#configure_the_time_travel_window)。

如要瞭解如何還原整個已刪除的資料集或快照，請參閱下列資源：

* [還原已刪除的資料集](https://docs.cloud.google.com/bigquery/docs/restore-deleted-datasets?hl=zh-tw)
* [還原資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-restore?hl=zh-tw)

時間回溯期可設定為 2 到 7 天。時間回溯期限過後，BigQuery 會提供[安全期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#fail-safe)，自動保留已刪除的資料七天。安全期過後，就無法使用任何方法還原資料表，包括提交支援單。

## 事前準備

確認您具備必要的 Identity and Access Management (IAM) 權限，可以還原已刪除的資料表。

如要從已刪除的資料集還原資料表，必須在原本儲存資料集的區域重新建立資料集。在不同區域重新建立資料集會導致時間旅行資料表還原作業失敗。

### 必要的角色

如要取得還原已刪除資料表所需的權限，請要求管理員授予您專案的 [BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user)  (`roles/bigquery.user`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 還原資料表

您可以將歷來資料複製到新資料表，藉此還原資料表。即使資料表已刪除或過期，只要在時間回溯期內還原資料表，就能複製歷來資料。

從歷來資料還原資料表時，來源資料表的[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)不會複製到目的地資料表。資料表分區資訊也不會複製到目的地資料表。如要重新建立原始資料表的分區架構，您可以在 [Cloud Logging](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw) 中查看初始資料表建立要求，並使用該資訊為還原的資料表建立分區。

您只能還原整個資料表，無法還原個別分區。舉例來說，不支援使用分區裝飾器 (例如 `bq cp mydataset.mytable$20260712@1418864998000 mydataset.mytable_restored`) 複製分區。

您可以使用 `@<time>` 時間修飾符，將資料表複製到新資料表，還原已刪除但仍在時間旅行期間內的資料表。即使使用時間修飾符，您也無法查詢已刪除的資料表。必須先還原。

請使用下列語法搭配 `@<time>` 時間修飾符：

* `tableid@TIME`，其中 `TIME` 是自 Unix Epoch 紀元時間起算的毫秒數。
* `tableid@-TIME_OFFSET`，其中 `TIME_OFFSET` 是與目前時間的相對偏移量，以毫秒為單位。
* `tableid@0`：指定可用的最早歷來資料。

如要還原表格，請選取下列任一選項：

### 控制台

您無法使用 Google Cloud 控制台取消刪除資料表。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 控制台底部會開啟 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已設定適用於您目前專案的值。工作階段可能要幾秒鐘的時間才能初始化。
2. 如要還原表格，請先判斷表格存在時的 UNIX 時間戳記 (以毫秒為單位)。您可以使用 Linux `date` 指令，從一般時間戳記值產生 Unix 時間戳記：

   ```
   date -d '2023-08-04 16:00:34.456789Z' +%s000
   ```
3. 接著，使用 `bq copy` 指令和 `@<time>` 時間旅行裝飾器，執行表格複製作業。

   例如，輸入下列指令，將 `1418864998000` 時間點的 `mydataset.mytable` 資料表複製到新資料表 `mydataset.newtable`。

   ```
   bq cp mydataset.mytable@1418864998000 mydataset.newtable
   ```

   (選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

   您也可以指定相對偏移。以下範例會複製一小時前的資料表版本：

   ```
   bq cp mydataset.mytable@-3600000 mydataset.newtable
   ```

   **注意：** 如果嘗試復原時間旅行視窗之前的資料，或是復原資料表建立前的資料，系統會顯示 `Invalid time travel timestamp` 錯誤。詳情請參閱「[排解資料表復原問題](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw#troubleshoot_table_recovery)」。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

如果您預期可能需要在時光旅行時間範圍允許的時間之後還原資料表，請建立資料表的資料表快照。詳情請參閱「[資料表快照簡介](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)」。

您無法直接還原邏輯檢視畫面。詳情請參閱「[還原檢視表](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw#restore_a_view)」。

**注意：** 如果刪除資料表後，又建立同名的新資料表，您可以使用[時間點復原](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw#bq)功能，還原原始已刪除資料表中的資料。時間戳記必須指定原始資料表存在的時間。

### 找出資料表的刪除時間

在 Google Cloud 控制台的 Logs Explorer 中使用下列篩選條件，找出顯示特定資料表到期或刪除的稽核項目：

```
resource.type="bigquery_resource"
protoPayload.resourceName="projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID"
(protoPayload.methodName="google.cloud.bigquery.v2.TableService.DeleteTable" OR protoPayload.methodName="tableservice.delete" OR protoPayload.serviceData.jobCompletedEvent.job.jobConfiguration.query.statementType="DROP_TABLE" OR protoPayload.methodName="InternalTableExpired")
```

更改下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：包含資料表的資料集 ID。
* `TABLE_ID`：已刪除資料表的 ID。

或者，您也可以使用下列篩選器，找出包含資料表的資料集到期或刪除時間：

```
resource.type="bigquery_dataset"
protoPayload.resourceName="projects/PROJECT_ID/datasets/DATASET_ID"
(protoPayload.methodName="google.cloud.bigquery.v2.DatasetService.DeleteDataset" OR protoPayload.methodName="datasetservice.delete")
```

更改下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：包含資料表的資料集 ID。

## 找出資料表刪除的原因

您可以使用 [`INFORMATION_SCHEMA.TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw) 檢視畫面，判斷資料表的刪除方式。

`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面會顯示目前資料表和時間回溯期內刪除的資料表相關資訊。如果資料表已刪除，`table_deletion_time` 欄會包含刪除時間戳記，`table_deletion_reason` 欄則會包含刪除方法。

如要判斷表格遭刪除的原因，請查詢 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面：

```
SELECT
  table_name,
  deleted,
  table_deletion_time,
  table_deletion_reason
FROM
  `PROJECT_ID`.`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE
WHERE
  table_schema = "DATASET_ID"
  AND table_name = "TABLE_ID"
```

請替換下列變數：

* `PROJECT_ID`：您的專案 ID。
* `REGION`：包含資料表的資料集所在區域。
* `DATASET_ID`：包含資料表的資料集 ID。
* `TABLE_ID`：已刪除資料表的 ID。

「`table_deletion_reason`」欄會說明資料表刪除的原因：

* `TABLE_EXPIRATION`：表格在設定的到期時間過後遭到刪除。
* `DATASET_DELETION`：使用者刪除了資料表所屬的資料集。
* `USER_DELETED`：使用者刪除了資料表。

## 疑難排解資料表復原問題

### 使用過去的時間戳記查詢已刪除的資料表

您無法使用時間戳記裝飾符查詢過去已刪除的資料表，或使用 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 將結果儲存至目的地資料表，藉此還原資料表資料。使用上述任一方法都會產生下列錯誤：

```
Not found: Table myproject:mydataset.table was not found in location LOCATION
```

如要複製資料表，請按照「[還原資料表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw#restore_a_table)」中的步驟操作。

### 錯誤：`VPC Service Controls: Request is prohibited by organization's policy`

嘗試從 Google Cloud Shell 執行複製指令時，可能會遇到類似下列的錯誤：

```
BigQuery error in cp operation: VPC Service Controls: Request is prohibited by organization's policy
```

Google Cloud 不支援透過 VPC SC 從控制台使用 Cloud Shell，因為系統會將這類要求視為來自服務周邊以外，並拒絕存取 VPC Service Controls 保護的資料。如要解決這個問題，請使用 Google Cloud CLI 啟動並[在本機連線至 Cloud Shell](https://docs.cloud.google.com/shell/docs/launching-cloud-shell?hl=zh-tw#launch_and_connect_locally_to_with_the)。

### 錯誤：`Latest categories are incompatible with schema`

如果您從 Google Cloud Shell 執行複製指令，可能會收到類似下列的錯誤訊息：

```
Latest categories are incompatible with schema at TIMESTAMP
```

造成這項錯誤的原因可能有很多種：

* 目的地資料表結構定義與原始資料表結構定義不同 (只要沒有附加任何[資料欄層級政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)，即可新增資料欄)。
* 目的地資料表的[資料欄層級政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)設定與來源資料表不同。

如要解決這項錯誤，請按照下列步驟操作：

1. 請確認目的地資料表的結構定義與原始資料表相同，且原始資料表中的所有資料欄都存在於目的地資料表中，且兩份資料表中的資料欄順序相同。
2. 從目的地資料表移除所有不在原始資料表結構定義中的資料欄層級政策標記。

### 錯誤：`BigQuery error in cp operation: Invalid time travel timestamp`

如果您從 Google Cloud Shell 執行 `bq copy` 指令，可能會收到類似下列的錯誤訊息：

```
BigQuery error in cp operation: Invalid time travel timestamp 1744343690000 for
table PROJECT_ID:DATASET_ID.TABLE_ID@1744343690000.
Cannot read before 1744843691075
```

這項錯誤表示您嘗試從時間旅行視窗之前或資料表建立之前的資料表狀態復原資料。系統不支援這項操作。錯誤訊息會包含可用於讀取表格資料的最新時間戳記。在 `bq copy` 指令中使用錯誤中的時間戳記。

如果提供負數的時間戳記值 (例如 `TABLE@-1744963620000`)，也可能發生這個錯誤。請改用可搭配 `-` 符號使用的時間偏移。

```
BigQuery error in cp operation: Invalid time travel timestamp 584878816 for
table PROJECT_ID:DATASET_ID.TABLE_ID@584878816.
Cannot read before 1744843691075
```

這則錯誤訊息表示 `bq cp` 指令含有負的時間戳記值做為偏移量，且您嘗試在 `CURRENT_TIMESTAMP - PROVIDED TIMESTAMP` 讀取資料表。這個值通常是 1970 年的時間戳記。如要解決這個問題，請在設定表格裝飾符值時，驗證位移或時間戳記值，並適當使用 `-` 符號。

### 分區

您只能還原整個資料表，您無法還原個別磁碟分割區。
舉例來說，系統不支援使用分區裝飾器 (例如 `bq cp mydataset.mytable$20260712@1418864998000 mydataset.mytable_restored`) 複製分區。

### 具體化檢視表

您無法直接還原已刪除的 materialized view，如果刪除具體化檢視區塊，就必須[重新建立](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)。

如果刪除作為 materialized view 基礎資料表的資料表，該 materialized view 就無法再查詢或重新整理。如果按照「[還原資料表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw#restore_a_table)」中的步驟還原基礎資料表，您也必須[重新建立](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)使用該資料表的任何 materialized view。

### 外部資料表

您無法直接還原已刪除的外部資料表。如果刪除外部資料表，必須[重新建立](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw#external_tables)。重新建立程序需要知道原始資料表的定義，最重要的是：

* 資料表的結構定義
* 指向外部資料的來源 URI
* 外部資料的格式

您可以從 [Cloud Logging](https://cloud.google.com/logging?hl=zh-tw) 取得這項資訊，方法是尋找資料表建立記錄項目。如果資料表剛刪除，您也可以嘗試查詢 [`INFORMATION_SCHEMA.TABLE_OPTIONS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-table-options?hl=zh-tw)來取得 URI。

刪除外部資料表不會刪除基礎資料。

## 後續步驟

* 瞭解如何[建立及使用表格](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)。
* 瞭解如何[管理表格](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)。
* 瞭解如何[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。
* 瞭解如何[處理表格資料](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-15 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-15 (世界標準時間)。"],[],[]]