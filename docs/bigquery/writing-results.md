* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 寫入查詢結果

本文說明如何將查詢結果寫入臨時或永久資料表。

## 暫時性與永久性資料表

BigQuery 會將所有查詢結果儲存至永久或臨時資料表：

* BigQuery 會使用臨時資料表[快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)，這些結果不會寫入永久資料表。這些資料表會建立在特殊資料集中，並隨機命名。您也可以在[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#temporary_tables)和[工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw#use_temporary_tables_in_sessions)中建立臨時表，供自己使用。[臨時快取查詢結果資料表](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)不會計費。
  如果臨時資料表不是快取查詢結果，您就需要付費。
* 查詢完成後，暫時性資料表最多會存在 24 小時。如要查看資料表結構和資料，請按照下列步驟操作：

  1. 前往「BigQuery」頁面

     [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
  2. 點選左側窗格中的 explore「Explorer」。

     如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
  3. 在「Explorer」窗格中，按一下「Job history」。
  4. 按一下「個人記錄」。
  5. 選擇建立暫存資料表的查詢。接著，在「目的地資料表」 列中，按一下「暫時性資料表」。
* 只有建立查詢工作的使用者或服務帳戶，才能存取臨時資料表資料。
* 臨時資料表無法共用，也無法透過任何一種標準清單或其他資料表操縱方法來顯示。如要分享查詢結果，請將結果寫入永久資料表、下載結果，或透過 Google 試算表或 Google 雲端硬碟分享結果。
* 系統會在與查詢的資料表相同的區域中建立暫時資料表。
* 永久資料表可以是您有權存取的任何資料集中之新資料表或現有資料表。如果您將查詢結果寫入新資料表，就必須支付資料的[儲存](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)費用。當您將查詢結果寫入永久資料表時，所查詢的資料表必須與包含目標資料表的資料集位於相同位置。
* 啟用[網域限制機構政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-domains?hl=zh-tw)後，您就無法將查詢結果儲存至暫存資料表。暫時停用網域限制機構政策，執行查詢，然後再次啟用政策，即可解決這個問題。或者，您也可以將查詢結果儲存到目的地資料表。

**注意：** 如果您從某個專案查詢儲存在其他專案中的資料，查詢專案會支付查詢工作的費用，而儲存資料的專案則會支付 BigQuery 中儲存的資料量費用。

## 所需權限

如要將查詢結果寫入資料表，您至少必須具備下列權限：

* `bigquery.tables.create`：建立新資料表的權限
* `bigquery.tables.updateData`：將資料寫入新資料表、覆寫資料表或將資料附加至資料表
* `bigquery.jobs.create`：執行查詢工作

您可能還需要其他權限 (例如 `bigquery.tables.getData`)，才能存取您要查詢的資料。

以下是同時具有 `bigquery.tables.create` 和 `bigquery.tables.updateData` 權限的預先定義 IAM 角色：

* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.admin`

以下是具有 `bigquery.jobs.create` 權限的預先定義 IAM 角色：

* `bigquery.user`
* `bigquery.jobUser`
* `bigquery.admin`

此外，當具備 `bigquery.datasets.create` 權限的使用者建立資料集時，會獲得該資料集的 `bigquery.dataOwner` 存取權。`bigquery.dataOwner` 存取權可讓使用者在資料集裡建立及更新資料表。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 將查詢結果寫入永久資料表

將查詢結果寫入永久資料表時，您可以建立新資料表、將結果附加到現有資料表，或覆寫現有資料表。

### 寫入查詢結果

請按照下列程序，將查詢結果寫入永久資料表。為協助控管費用，您可以在執行查詢前[預覽資料](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#preview-data)。

### 控制台

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在查詢編輯器中輸入有效的 SQL 查詢。
5. 按一下「更多」，然後選取「查詢設定」。
6. 選取「為查詢結果設定目標資料表」選項。
7. 在「目的地」部分，選取要建立資料表的「資料集」，然後選擇「資料表 ID」。
8. 在「Destination table write preference」(目標資料表寫入偏好設定) 區段，選擇下列其中一項：

   * [Write if empty] (空白時寫入)：僅在資料表空白時將查詢結果寫入資料表。
   * [Append to table] (附加到資料表中)：將查詢結果附加到現有的資料表。
   * [Overwrite table] (覆寫資料表)：使用查詢結果覆寫名稱相同的現有資料表。
9. 選用：針對「Data location」(資料位置)，選擇您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
10. 如要更新查詢設定，請按一下「儲存」。
11. 按一下「執行」。這會建立一個查詢工作，將查詢結果寫入您指定的資料表。

如果您在執行查詢前忘記指定目的地資料表，也可以按一下編輯器上方的 [[Save Results] (儲存結果)](#save-query-results) 按鈕，將快取結果資料表複製至永久資料表。

### SQL

以下範例使用 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，從公開 `bikeshare_trips` 資料表中的資料建立 `trips` 資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE mydataset.trips AS (
     SELECT
       bike_id,
       start_time,
       duration_minutes
     FROM
       bigquery-public-data.austin_bikeshare.bikeshare_trips
   );
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

詳情請參閱「[從現有資料表建立新資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_new_table_from_an_existing_table)」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令並指定 `--destination_table` 旗標，根據查詢結果建立永久資料表。指定 `use_legacy_sql=false` 旗標以使用 GoogleSQL 語法。如要將查詢結果寫入不在預設專案內的資料表，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

   選用：提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

   如要控管現有目的地資料表的寫入配置，請指定以下其中一種選用旗標：

   * `--append_table`：如果目的地資料表已存在，查詢結果會附加至該資料表。
   * `--replace`：如果目的地資料表已存在，查詢結果會覆寫該資料表。

     ```
     bq --location=location query \
     --destination_table project_id:dataset.table \
     --use_legacy_sql=false 'query'
     ```

     更改下列內容：
   * `location` 是用於處理查詢的位置名稱，`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
   * `project_id` 是您的專案 ID。
   * `dataset` 是包含您要寫入查詢結果之資料表的資料集名稱。
   * `table` 是您要寫入查詢結果的資料表名稱。
   * `query` 是採用 GoogleSQL 語法的查詢。

     如未指定任何寫入配置旗標，預設動作是僅在資料表空白時，才將結果寫入資料表。如果資料表存在但並非空白，系統會傳回下列錯誤：`BigQuery error in query operation: Error processing job
     project_id:bqjob_123abc456789_00000e1234f_1: Already
     Exists: Table project_id:dataset.table`。

     範例：

     **注意：**這些範例會查詢位於美國的公開資料集。由於該公開資料集儲存在美國的多地區位置，因此您目的地資料表所屬的資料集也必須位於美國。您無法查詢位於某個位置的資料集，然後將結果寫入位於另一個位置的目的地資料表。 

     輸入下列指令，將查詢結果寫入 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於預設專案中。由於您未在指令中指定任何寫入配置旗標，因此資料表必須為新資料表或空白資料表。否則，系統會傳回 `Already exists` 錯誤。查詢會從[美國人名資料公開資料集](https://console.cloud.google.com/marketplace/product/social-security-administration/us-names?hl=zh-tw)中擷取資料。

     ```
     bq query \
     --destination_table mydataset.mytable \
     --use_legacy_sql=false \
     'SELECT
     name,
     number
     FROM
     `bigquery-public-data`.usa_names.usa_1910_current
     WHERE
     gender = "M"
     ORDER BY
     number DESC'
     ```

     輸入下列指令，使用查詢結果覆寫 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於預設專案中。該指令使用 `--replace` 旗標來覆寫目標資料表。

     ```
     bq query \
     --destination_table mydataset.mytable \
     --replace \
     --use_legacy_sql=false \
     'SELECT
     name,
     number
     FROM
     `bigquery-public-data`.usa_names.usa_1910_current
     WHERE
     gender = "M"
     ORDER BY
     number DESC'
     ```

     輸入下列指令，將查詢結果附加至 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於 `my-other-project`，而非預設專案。指令使用 `--append_table` 旗標將查詢結果附加至目的地資料表。

     ```
     bq query \
     --append_table \
     --use_legacy_sql=false \
     --destination_table my-other-project:mydataset.mytable \
     'SELECT
     name,
     number
     FROM
     `bigquery-public-data`.usa_names.usa_1910_current
     WHERE
     gender = "M"
     ORDER BY
     number DESC'
     ```

     各範例的輸出內容如下。為了方便閱讀，以下僅顯示部分輸出內容。

     ```
     Waiting on bqjob_r123abc456_000001234567_1 ... (2s) Current status: DONE
     +---------+--------+
     |  name   | number |
     +---------+--------+
     | Robert  |  10021 |
     | John    |   9636 |
     | Robert  |   9297 |
     | ...              |
     +---------+--------+
     ```

### API

如要將查詢結果儲存至永久資料表，請呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法，設定 `query` 工作，然後加入 `destinationTable` 屬性的值。如要控管現有目標資料表的寫入配置，請設定 `writeDisposition` 屬性。

如要控管查詢工作的處理位置，請在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中指定 `location` 屬性。

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

// queryWithDestination demonstrates saving the results of a query to a specific table by setting the destination
// via the API properties.
func queryWithDestination(w io.Writer, projectID, destDatasetID, destTableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	q := client.Query("SELECT 17 as my_col")
	q.Location = "US" // Location must match the dataset(s) referenced in query.
	q.QueryConfig.Dst = client.Dataset(destDatasetID).Table(destTableID)
	// Run the query and print results when the query job is completed.
	job, err := q.Run(ctx)
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
	it, err := job.Read(ctx)
	for {
		var row []bigquery.Value
		err := it.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintln(w, row)
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要將查詢結果儲存至永久資料表，請在 [QueryJobConfiguration](https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration?hl=zh-tw) 中將[目標資料表](https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration.Builder?hl=zh-tw#com_google_cloud_bigquery_QueryJobConfiguration_Builder_setDestinationTable_com_google_cloud_bigquery_TableId_)設為所要的 [TableId](https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.TableId?hl=zh-tw)。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableId;

public class SaveQueryToTable {

  public static void runSaveQueryToTable() {
    // TODO(developer): Replace these variables before running the sample.
    String query = "SELECT corpus FROM `bigquery-public-data.samples.shakespeare` GROUP BY corpus;";
    String destinationTable = "MY_TABLE";
    String destinationDataset = "MY_DATASET";

    saveQueryToTable(destinationDataset, destinationTable, query);
  }

  public static void saveQueryToTable(
      String destinationDataset, String destinationTableId, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Identify the destination table
      TableId destinationTable = TableId.of(destinationDataset, destinationTableId);

      // Build the query job
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query).setDestinationTable(destinationTable).build();

      // Execute the query.
      bigquery.query(queryConfig);

      // The results are now saved in the destination table.

      System.out.println("Saved query ran successfully");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Saved query did not run \n" + e.toString());
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

async function queryDestinationTable() {
  // Queries the U.S. given names dataset for the state of Texas
  // and saves results to permanent table.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  // Create destination table reference
  const dataset = bigquery.dataset(datasetId);
  const destinationTable = dataset.table(tableId);

  const query = `SELECT name
    FROM \`bigquery-public-data.usa_names.usa_1910_2013\`
    WHERE state = 'TX'
    LIMIT 100`;

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
  const options = {
    query: query,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
    destination: destinationTable,
  };

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(options);

  console.log(`Job ${job.id} started.`);
  console.log(`Query results loaded to table ${destinationTable.id}`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要將查詢結果儲存至永久性資料表，請建立 [QueryJobConfig](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob)，並將[目的地](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob_destination)設為所要的 [TableReference](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.TableReference?hl=zh-tw)。接著，將工作設定傳送至[查詢方法](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_query)。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the destination table.
# table_id = "your-project.your_dataset.your_table_name"

job_config = bigquery.QueryJobConfig(destination=table_id)

sql = """
    SELECT corpus
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus;
"""

# Start the query, passing in the extra configuration.
query_job = client.query(sql, job_config=job_config)  # Make an API request.
query_job.result()  # Wait for the job to complete.

print("Query results loaded to the table {}".format(table_id))
```

## 寫入大型查詢結果

通常，查詢都有[回應大小上限](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。如果您打算執行可能會傳回較大結果的查詢，可以執行下列其中一項操作：

* 在 GoogleSQL 中，指定查詢結果的目的地資料表。
* 在舊版 SQL 中，指定目標資料表並設定 `allowLargeResults` 選項。

如果您指定的目標資料表會寫入大型查詢結果，則必須支付資料的[儲存](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)費用。

### 限制

在舊版 SQL 中，寫入大型結果受到下列限制：

* 您必須指定目標資料表。
* 不能指定頂層 `ORDER BY`、`TOP` 或 `LIMIT` 子句。這麼做會抵銷使用 `allowLargeResults` 的好處，因為再也無法平行計算查詢輸出。
* [窗型函式](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw#windowfunctions)只有在合併使用 `PARTITION BY` 子句時才能傳回大型查詢結果。

### 使用舊版 SQL 寫入大型結果

如要使用舊版 SQL 寫入大型結果集：

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 [Compose new query] (撰寫新查詢)。
3. 在「Query editor」(查詢編輯器) 文字區域中輸入有效的 SQL 查詢。請使用 `#legacySQL` 前置字串，或確認您已在查詢設定中勾選 [Use Legacy SQL] (使用舊版 SQL)。
4. 按一下 [More] (更多)，然後選取 [Query settings] (查詢設定)。
5. 在「Destination」(目的地) 部分，勾選 [Set a destination table for query results] (為查詢結果設定目標資料表)。
6. 在「Dataset」(資料集) 部分，選擇要儲存資料表的資料集。
7. 在「Table Id」(資料表 ID) 欄位中，輸入資料表名稱。
8. 如果您要將大型結果集寫入現有資料表，可以使用「Destination table write preference」(目標資料表寫入偏好設定) 選項來控管目標資料表的寫入配置：

   * **Write if empty：**僅在資料表空白時將查詢結果寫入資料表。
   * **附加到資料表中：**將查詢結果附加到現有資料表。
   * **覆寫資料表：**使用查詢結果覆寫名稱相同的現有資料表。
9. 在「Results Size」(結果大小) 部分，勾選「Allow large results (no size limit)」(允許大型結果 (無大小上限))。
10. 選用：針對「Data location」(資料位置)，選擇資料的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
11. 按一下 [Save] (儲存) 以更新查詢設定。
12. 按一下 [Run] (執行)。這會建立一個查詢工作，將大型結果集寫入您指定的資料表。

### bq

使用 `--allow_large_results` 旗標搭配 `--destination_table` 旗標，建立目標資料表來保存大型結果集。因為 `--allow_large_results` 選項只適用於舊版 SQL，所以您也必須指定 `--use_legacy_sql=true` 旗標。如要將查詢結果寫入不在預設專案內的資料表，請使用下列格式將專案 ID 新增至資料集名稱：`PROJECT_ID:DATASET`。
加上 `--location` 旗標，並將旗標的值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

如要控管現有目標資料表的寫入配置，請指定以下其中一種選用旗標：

* `--append_table`：如果目的地資料表已存在，查詢結果會附加至該資料表。
* `--replace`：如果目的地資料表已存在，查詢結果會覆寫該資料表。

```
bq --location=location query \
--destination_table PROJECT_ID:DATASET.TABLE \
--use_legacy_sql=true \
--allow_large_results "QUERY"
```

更改下列內容：

* `LOCATION` 是用於處理查詢的位置名稱，`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `PROJECT_ID` 是您的專案 ID。
* `DATASET` 是包含您要寫入查詢結果之資料表的資料集名稱。
* `TABLE` 是您要寫入查詢結果的資料表名稱。
* `QUERY` 是舊版 SQL 語法中的查詢。

範例：

**附註：**些範例查詢的是公開資料集。由於該資料集儲存在 `US` 多地區位置，因此您的目標資料表也必須位於美國境內。您無法將公開資料查詢結果寫入不同地區的資料表。

輸入下列指令，將大型查詢結果寫入 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於預設專案中。由於您未在指令中指定任何寫入配置旗標，因此資料表必須為新資料表或空白資料表。否則，系統會傳回 `Already exists` 錯誤。查詢會從[美國人名資料公開資料集](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=usa_names&%3Bpage=dataset&hl=zh-tw)擷取資料。此查詢僅做示範之用。傳回的結果集不會超出回應大小上限。

```
bq query \
--destination_table mydataset.mytable \
--use_legacy_sql=true \
--allow_large_results \
"SELECT
  name,
  number
FROM
  [bigquery-public-data:usa_names.usa_1910_current]
WHERE
  gender = 'M'
ORDER BY
  number DESC"
```

輸入下列指令，使用大型查詢結果覆寫 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於 `myotherproject`，而非預設專案中。指令使用 `--replace` 旗標覆寫目標資料表。

```
bq query \
--destination_table mydataset.mytable \
--replace \
--use_legacy_sql=true \
--allow_large_results \
"SELECT
  name,
  number
FROM
  [bigquery-public-data:usa_names.usa_1910_current]
WHERE
  gender = 'M'
ORDER BY
  number DESC"
```

輸入下列指令，將大型查詢結果附加至 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於 `myotherproject`，而非預設專案中。指令使用 `--append_table` 旗標將查詢結果附加至目的地資料表。

```
bq query \
--destination_table myotherproject:mydataset.mytable \
--append_table \
--use_legacy_sql=true \
--allow_large_results \
"SELECT
  name,
  number
FROM
  [bigquery-public-data:usa_names.usa_1910_current]
WHERE
  gender = 'M'
ORDER BY
  number DESC"
```

### API

如要將大型結果寫入目標資料表，請呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法，設定 `query` 工作，並將 `allowLargeResults` 屬性設為 `true`。使用 `destinationTable` 屬性指定目標資料表。如要控管現有目標資料表的寫入配置，請設定 `writeDisposition` 屬性。

在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，利用 `location` 屬性指定您的位置。

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

// queryLegacyLargeResults demonstrates issuing a legacy SQL query and writing a large result set
// into a destination table.
func queryLegacyLargeResults(w io.Writer, projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "destinationdataset"
	// tableID := "destinationtable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	q := client.Query(
		"SELECT corpus FROM [bigquery-public-data:samples.shakespeare] GROUP BY corpus;")
	q.UseLegacySQL = true
	q.AllowLargeResults = true
	q.QueryConfig.Dst = client.Dataset(datasetID).Table(tableID)
	// Run the query and print results when the query job is completed.
	job, err := q.Run(ctx)
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
	it, err := job.Read(ctx)
	for {
		var row []bigquery.Value
		err := it.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintln(w, row)
	}
	return nil
}
```

### Java

如要啟用大型結果，請在 [QueryJobConfiguration](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration?hl=zh-tw) 中將[允許大型結果](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration.Builder?hl=zh-tw#com_google_cloud_bigquery_QueryJobConfiguration_Builder_setAllowLargeResults_java_lang_Boolean_)設為 `true`，並將[目標資料表](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.TableId?hl=zh-tw)設為需要的 [TableId](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.TableId?hl=zh-tw)。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableResult;

// Sample to run query with large results and save the results to a table.
public class QueryLargeResults {

  public static void runQueryLargeResults() {
    // TODO(developer): Replace these variables before running the sample.
    String destinationDataset = "MY_DESTINATION_DATASET_NAME";
    String destinationTable = "MY_DESTINATION_TABLE_NAME";
    String query = "SELECT corpus FROM [bigquery-public-data:samples.shakespeare] GROUP BY corpus;";
    queryLargeResults(destinationDataset, destinationTable, query);
  }

  public static void queryLargeResults(
      String destinationDataset, String destinationTable, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      QueryJobConfiguration queryConfig =
          // To use legacy SQL syntax, set useLegacySql to true.
          QueryJobConfiguration.newBuilder(query)
              .setUseLegacySql(true)
              // Save the results of the query to a permanent table.
              .setDestinationTable(TableId.of(destinationDataset, destinationTable))
              // Allow results larger than the maximum response size.
              // If true, a destination table must be set.
              .setAllowLargeResults(true)
              .build();

      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query large results performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
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

async function queryLegacyLargeResults() {
  // Query enables large result sets.

  /**
   * TODO(developer): Uncomment the following lines before running the sample
   */
  // const projectId = "my_project"
  // const datasetId = "my_dataset";
  // const tableId = "my_table";

  const query = `SELECT word FROM [bigquery-public-data:samples.shakespeare] LIMIT 10;`;

  // For all options, see https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
  const options = {
    query: query,
    // Location must match that of the dataset(s) referenced
    // in the query and of the destination table.
    useLegacySql: true,
    allowLargeResult: true,
    destinationTable: {
      projectId: projectId,
      datasetId: datasetId,
      tableId: tableId,
    },
  };

  const [job] = await bigquery.createQueryJob(options);
  console.log(`Job ${job.id} started.`);

  // Wait for the query to finish
  const [rows] = await job.getQueryResults();

  // Print the results
  console.log('Rows:');
  rows.forEach(row => console.log(row));
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the destination table.
# table_id = "your-project.your_dataset.your_table_name"

# Set the destination table and use_legacy_sql to True to use
# legacy SQL syntax.
job_config = bigquery.QueryJobConfig(
    allow_large_results=True, destination=table_id, use_legacy_sql=True
)

sql = """
    SELECT corpus
    FROM [bigquery-public-data:samples.shakespeare]
    GROUP BY corpus;
"""

# Start the query, passing in the extra configuration.
query_job = client.query(sql, job_config=job_config)  # Make an API request.
query_job.result()  # Wait for the job to complete.

print("Query results loaded to the table {}".format(table_id))
```

## 從 Google Cloud 控制台下載及儲存查詢結果

使用 Google Cloud 控制台執行 SQL 查詢後，您可以將結果儲存到其他位置。您可以使用 Google Cloud 控制台，將查詢結果下載到本機檔案、Google 試算表或 Google 雲端硬碟。如果您先依資料欄排序查詢結果，下載的資料就會保留排序順序。bq 指令列工具或 API 都不支援將結果儲存到本機檔案、Google 試算表或 Google 雲端硬碟。

### 限制

下載並儲存查詢結果受到下列限制：

* 您只能以 CSV 或以換行符號分隔的 JSON 格式將查詢結果下載到本機檔案。
* 您無法將包含巢狀與重複資料的查詢結果儲存到 Google 試算表。
* 如要使用 Google Cloud 主控台將查詢結果儲存到 Google 雲端硬碟，結果集必須為 1 GB 或以下。如果結果較大，您可以改為將結果儲存到資料表。
* 將查詢結果儲存至本機 CSV 檔案時，下載大小上限為 10 MB。最大下載大小取決於 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 方法回應中傳回的每個資料列大小，且可能會因查詢結果的結構而異。因此，下載的 CSV 檔案大小可能不同，且可能小於下載大小上限。
* 您只能以 CSV 或以換行符號分隔的 JSON 格式將查詢結果儲存到 Google 雲端硬碟。

## 後續步驟

* 瞭解如何以程式輔助方式[將資料表匯出為 JSON 檔案](https://docs.cloud.google.com/bigquery/docs/samples/bigquery-extract-table-json?hl=zh-tw)。
* 瞭解[查詢作業的配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。
* 瞭解 [BigQuery 儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]