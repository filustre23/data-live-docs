Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理具體化檢視表

本文說明如何在 BigQuery 中管理具體化檢視表。

BigQuery 具體化檢視表管理作業包括：

* [修改具體化檢視表](#alter)
* [列出具體化檢視表](#list)
* [取得具體化檢視表相關資訊](#get-info)
* [刪除具體化檢視表](#delete)
* [重新整理具體化檢視表](#refresh)

如要進一步瞭解具體化檢視區塊，請參閱下列資源：

* [具體化檢視表簡介](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)
* [建立具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)
* [使用具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw)
* [監控具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-monitor?hl=zh-tw)

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。如要執行工作，必須具備的權限 (如有) 會列在工作的「必要權限」部分。

## 修改具體化檢視表

您可以使用資料定義語言 (DDL) 和 `ALTER MATERIALIZED
VIEW` 和 `SET OPTIONS`，透過 Google Cloud 控制台或 bq 指令列工具變更具體化檢視區塊。如需具體化檢視表選項清單，請參閱 [`materialized_view_set_options_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#materialized_view_set_options_list)。

以下範例會將 `enable_refresh` 設為 `true`。視您的用途需求調整。

### 所需權限

如要變更具體化檢視表，您需要 `bigquery.tables.get` 和 `bigquery.tables.update` IAM 權限。

下列預先定義的 IAM 角色都包含變更具體化檢視區塊所需的權限：

* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.admin`

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### SQL

如要變更具體化檢視表，請使用 [`ALTER MATERIALIZED VIEW SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_materialized_view_set_options_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER MATERIALIZED VIEW PROJECT.DATASET.MATERIALIZED_VIEW
   SET OPTIONS (enable_refresh = true);
   ```

   請替換下列項目：

   * `PROJECT`：包含具體化檢視區塊的專案名稱
   * `DATASET`：包含具體化檢視區的資料集名稱
   * `MATERIALIZED_VIEW`：要變更的具體化檢視名稱
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

執行 `bq update` 指令：

```
bq update \
--enable_refresh=true \
--refresh_interval_ms= \
PROJECT.DATASET.MATERIALIZED_VIEW
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.MaterializedViewDefinition;
import com.google.cloud.bigquery.Table;
import com.google.cloud.bigquery.TableId;

// Sample to update materialized view
public class UpdateMaterializedView {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String materializedViewName = "MY_MATERIALIZED_VIEW_NAME";
    updateMaterializedView(datasetName, materializedViewName);
  }

  public static void updateMaterializedView(String datasetName, String materializedViewName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, materializedViewName);

      // Get existing materialized view
      Table table = bigquery.getTable(tableId);
      MaterializedViewDefinition materializedViewDefinition = table.getDefinition();
      // Update materialized view
      materializedViewDefinition
          .toBuilder()
          .setEnableRefresh(true)
          .setRefreshIntervalMs(1000L)
          .build();
      table.toBuilder().setDefinition(materializedViewDefinition).build().update();
      System.out.println("Materialized view updated successfully");
    } catch (BigQueryException e) {
      System.out.println("Materialized view was not updated. \n" + e.toString());
    }
  }
}
```

## 列出具體化檢視表

您可以透過 Google Cloud 主控台、bq 指令列工具或 BigQuery API 列出具體化檢視區塊。

### 所需權限

如要列出資料集中的具體化檢視表，您需要 `bigquery.tables.list` IAM 權限。

下列每個預先定義的 IAM 角色都包含必要權限，可列出資料集中的具體化檢視區塊：

* `roles/bigquery.user`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.admin`

如要進一步瞭解 IAM 中的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

列出具體化檢視區的程序與列出資料表的程序相同。如要列出資料集中的具體化檢視表：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
3. 依序點選「總覽」**>「表格」**。捲動清單來檢視該資料集中的資料表，資料表、檢視表和具體化檢視表會分別以「類型」欄中的不同值呈現。具體化檢視表副本的值與具體化檢視表相同。

### bq

請發出 `bq ls` 指令。`--format` 旗標可用來控制輸出內容。如要列出非預設專案中的具體化檢視表，請使用下列格式將專案 ID 新增至資料集：`project_id:dataset`。

```
bq ls --format=pretty project_id:dataset
```

其中：

* project\_id 是您的專案 ID。
* dataset 是資料集名稱。

執行指令時，`Type` 欄位會顯示資料表類型。
例如：

```
+-------------------------+--------------------+----------------------+-------------------+
|         tableId         | Type               |        Labels        | Time Partitioning |
+-------------------------+--------------------+----------------------+-------------------+
| mytable                 | TABLE              | department:shipping  |                   |
| mymatview               | MATERIALIZED_VIEW  |                      |                   |
+-------------------------+--------------------+----------------------+-------------------+
```

範例：

輸入下列指令，列出預設專案中 `mydataset` 資料集的具體化檢視表。

```
bq ls --format=pretty mydataset
```

輸入下列指令，列出 `myotherproject` 中資料集 `mydataset` 的具體化檢視表。

```
bq ls --format=pretty myotherproject:mydataset
```

### API

如要使用 API 列出具體化檢視表，請呼叫 [`tables.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/list?hl=zh-tw) 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// listTables demonstrates iterating through the collection of tables in a given dataset.
func listTables(w io.Writer, projectID, datasetID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	ts := client.Dataset(datasetID).Tables(ctx)
	for {
		t, err := ts.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintf(w, "Table: %q\n", t.TableID)
	}
	return nil
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset that contains
#                  the tables you are listing.
# dataset_id = 'your-project.your_dataset'

tables = client.list_tables(dataset_id)  # Make an API request.

print("Tables contained in '{}':".format(dataset_id))
for table in tables:
    print("{}.{}.{}".format(table.project, table.dataset_id, table.table_id))
```

## 取得具體化檢視表的相關資訊

您可以使用 SQL、bq 指令列工具或 BigQuery API，取得具體化檢視區塊的相關資訊。

### 所需權限

如要查詢具體化檢視區塊的相關資訊，您需要下列 Identity and Access Management (IAM) 權限：

* `bigquery.tables.get`
* `bigquery.tables.list`
* `bigquery.routines.get`
* `bigquery.routines.list`

下列每個預先定義的 IAM 角色都包含上述權限：

* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.admin`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要取得具體化檢視表的相關資訊，包括任何依附的[具體化檢視表副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)，請按照下列步驟操作：

### SQL

如要取得具體化檢視表的相關資訊，請查詢 [`INFORMATION_SCHEMA.TABLES` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT * FROM PROJECT_ID.DATASET_ID.INFORMATION_SCHEMA.TABLES
   WHERE table_type = 'MATERIALIZED VIEW';
   ```

   請替換下列項目：

   * `PROJECT_ID`：包含具體化檢視區塊的專案名稱
   * `DATASET_ID`：包含具體化檢視區塊的資料集名稱
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令：

```
bq show --project=project_id --format=prettyjson dataset.materialized_view
```

更改下列內容：

* project\_id：專案 ID。如要取得預設專案以外的專案具體化檢視表相關資訊，只需加入這個旗標即可。
* dataset：包含具體化檢視區塊的資料集名稱。
* materialized\_view：您想取得資訊的具體化檢視區塊名稱。

範例：

輸入下列指令，顯示 `myproject` 專案中 `report_views` 資料集的實體化檢視表 `my_mv` 相關資訊。

```
bq show --project=myproject --format=prettyjson report_views.my_mv
```

### API

如要使用 API 取得具體化檢視表資訊，請呼叫 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) 方法。

## 刪除具體化檢視表

您可以透過 Google Cloud 主控台、bq 指令列工具或 API 刪除具體化檢視區塊。

**注意：** 一經刪除具體化檢視表即無法復原。

刪除具體化檢視表時，系統也會一併刪除與該檢視表相關聯的權限。重新建立已刪除的具體化檢視區塊時，您也必須手動[重新設定先前與該檢視區塊相關聯的存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)。

### 所需權限

如要刪除具體化檢視，您需要 `bigquery.tables.delete`
IAM 權限。

下列每個預先定義的 IAM 角色都包含刪除具體化檢視區塊所需的權限：

* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.admin`

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### SQL

如要刪除具體化檢視表，請使用 [`DROP MATERIALIZED VIEW` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_materialized_view_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   DROP MATERIALIZED VIEW PROJECT.DATASET.MATERIALIZED_VIEW;
   ```

   請替換下列項目：

   * `PROJECT`：包含具體化檢視區塊的專案名稱
   * `DATASET`：包含具體化檢視區的資料集名稱
   * `MATERIALIZED_VIEW`：要刪除的具體化檢視名稱
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq rm` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_rm)刪除具體化檢視區塊。

### API

呼叫 [`tables.delete`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete?hl=zh-tw) 方法，並為 `projectId`、`datasetId` 和 `tableId`
[參數](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete?hl=zh-tw#path-parameters)指定值：

* 將 `projectId` 參數指派給您的專案 ID。
* 將 `datasetId` 參數指派給資料集 ID。
* 將 `tableId` 參數指派給要刪除的具體化檢視表資料表 ID。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.TableId;

// Sample to delete materialized view
public class DeleteMaterializedView {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String materializedViewName = "MY_MATERIALIZED_VIEW_NAME";
    deleteMaterializedView(datasetName, materializedViewName);
  }

  public static void deleteMaterializedView(String datasetName, String materializedViewName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, materializedViewName);

      boolean success = bigquery.delete(tableId);
      if (success) {
        System.out.println("Materialized view deleted successfully");
      } else {
        System.out.println("Materialized view was not found");
      }
    } catch (BigQueryException e) {
      System.out.println("Materialized view was not found. \n" + e.toString());
    }
  }
}
```

**注意：** 如果未先刪除具體化檢視表，就刪除該檢視表的基礎資料表，則任何重新整理或查詢具體化檢視表的作業都會失敗。如果您決定重新建立基礎資料表，也必須重新建立具體化檢視區塊。

## 重新整理具體化檢視表

重新整理具體化檢視區塊會更新檢視區塊的快取資料，以反映基礎資料表的目前狀態。

查詢具體化檢視表時，BigQuery 會傳回快取具體化檢視表資料和從基本資料表擷取的資料。如果可以，BigQuery 只會讀取上次重新整理檢視區塊後發生的變更。雖然具體化檢視表重新整理時可能不會納入最近串流的資料，但無論是否使用具體化檢視表，查詢一律會讀取串流資料。

直接從主資料表傳回查詢結果，會比從快取具體化檢視表資料傳回結果，產生更高的運算費用。定期重新整理具體化檢視區塊快取資料，可減少直接從基礎資料表傳回的資料量，進而降低運算成本。

本節將說明如何執行下列操作：

* [設定自動重新整理](#automatic-refresh)
* [手動重新整理具體化檢視表](#manual-refresh)

**注意：** 如果未先刪除具體化檢視表就刪除基礎資料表，具體化檢視表就會無法重新整理。如要重新建立基本資料表，也必須重新建立具體化檢視區塊。

### 自動重新整理

你隨時可以啟用或停用自動重新整理功能。自動重新整理工作是由 `bigquery-adminbot@system.gserviceaccount.com` 服務帳戶執行，並顯示在具體化檢視專案的工作記錄中。

根據預設，實體化檢視中的快取資料會在基本資料表變更後 5 到 30 分鐘內，自動從基本資料表重新整理，例如插入或刪除資料列。

您可以設定[重新整理頻率上限](#frequency_cap)，管理快取資料的自動重新整理頻率，進而管理具體化檢視區塊的成本和查詢效能。

#### 啟用及停用自動重新整理

如要在建立具體化檢視表時關閉自動重新整理功能，請將 `enable_refresh` 設為 `false`。

```
CREATE MATERIALIZED VIEW PROJECT.DATASET.MATERIALIZED_VIEW
PARTITION BY RANGE_BUCKET(column_name, buckets)
OPTIONS (enable_refresh = false)
AS SELECT ...
```

如為現有的具體化檢視區塊，您可以使用 `ALTER MATERIALIZED VIEW` 修改 `enable_refresh` 值。

```
ALTER MATERIALIZED VIEW PROJECT.DATASET.MATERIALIZED_VIEW
SET OPTIONS (enable_refresh = true);
```

**注意：** 啟用自動重新整理功能後，系統會立即自動重新整理具體化檢視區塊。

#### 設定展示頻率上限

您可以設定自動重新整理的頻率上限。根據預設，具體化檢視區塊的重新整理頻率不會超過每 30 分鐘一次。

您隨時可以變更重新整理頻率上限。

如要在建立具體化檢視表時設定重新整理頻率上限，請在 DDL 中將 `refresh_interval_minutes` (或在 API 和 bq 指令列工具中將 `refresh_interval_ms`) 設為所需值。

```
CREATE MATERIALIZED VIEW PROJECT.DATASET.MATERIALIZED_VIEW
OPTIONS (enable_refresh = true, refresh_interval_minutes = 60)
AS SELECT ...
```

同樣地，您可以在修改具體化檢視區塊時設定展示頻率上限。
這個範例假設您已啟用自動重新整理功能，現在只想變更展示頻率上限：

```
ALTER MATERIALIZED VIEW PROJECT.DATASET.MATERIALIZED_VIEW
SET OPTIONS (refresh_interval_minutes = 60);
```

重新整理頻率上限下限為 1 分鐘。重新整理頻率上限最多為 7 天。

您可以隨時手動重新整理具體化檢視表，且時間不受頻率上限限制。

#### 盡可能提供最佳服務

系統會盡可能自動重新整理。
如果基礎資料表在 30 分鐘內發生變更，BigQuery 會嘗試在 5 分鐘內啟動重新整理作業，但無法保證會在該時間啟動，也無法保證何時完成。

**注意：** 查詢具體化檢視區塊時，會反映基礎資料表的最新狀態，但如果檢視區塊最近未重新整理，查詢費用或延遲時間可能會高於預期。

自動重新整理的處理方式與[批次](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)優先順序的查詢類似。如果具體化檢視區塊的專案目前沒有容量，系統會延後重新整理。如果專案包含許多重新整理成本很高的檢視區塊，每個檢視區塊相對於其基本資料表，可能會大幅延遲。

### 手動重新整理

您隨時可以手動重新整理具體化檢視區塊。

#### 所需權限

如要手動重新整理具體化檢視表，您需要 `bigquery.tables.getData`、`bigquery.tables.update` 和 `bigquery.tables.updateData` IAM 權限。

下列預先定義的 IAM 角色都包含手動重新整理具體化檢視區塊所需的權限：

* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.admin`

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要更新具體化檢視表中的資料，請呼叫 [`BQ.REFRESH_MATERIALIZED_VIEW`](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_materialized_view) 系統程序。呼叫這個程序時，BigQuery 會找出基底資料表中的變更，並將這些變更套用至具體化檢視區塊。查詢會在重新整理完成時結束。`BQ.REFRESH_MATERIALIZED_VIEW`

```
CALL BQ.REFRESH_MATERIALIZED_VIEW('PROJECT.DATASET.MATERIALIZED_VIEW');
```

**注意：** 請勿一次執行多項重新整理作業。如果對同一個具體化檢視區塊同時執行多項重新整理作業，只有第一個完成的重新整理作業會成功。

## 監控具體化檢視表

您可以使用 BigQuery API 取得具體化檢視表和具體化檢視表重新整理工作的相關資訊。詳情請參閱「[監控具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-monitor?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]