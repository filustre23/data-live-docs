* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將資料表資料匯出至 Cloud Storage

本頁面說明如何將 BigQuery 資料表中的資料匯出或擷取至 Cloud Storage。

[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw) 後，您就可以匯出數種格式的資料。BigQuery 對每個檔案最多可匯出 1 GB 的邏輯資料大小。如果要匯出的資料超過 1 GB，就必須將資料分別匯出成[多個檔案](#exporting_data_into_one_or_more_files)。將資料匯出至多個檔案時，各檔案的大小會有所差異。

您也可以使用 [`EXPORT DATA`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw#export_data_statement) 陳述式匯出查詢結果。您可以使用 [`EXPORT DATA OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw#gcs_s3_export_option) 指定匯出資料的格式。

最後，您可以使用 [Dataflow](https://docs.cloud.google.com/dataflow/what-is-google-cloud-dataflow?hl=zh-tw) 等服務來讀取 BigQuery 中的資料，不必從 BigLake 匯出資料。如要進一步瞭解如何使用 Dataflow 讀取 BigQuery 的資料及將資料寫入 BigQuery，請參閱 [BigQuery I/O 說明文件](https://beam.apache.org/documentation/io/built-in/google-bigquery)。

## 匯出限制

當您從 BigQuery 匯出資料時，請注意以下幾點：

**注意：** 如果將資料匯出至 Cloud Storage bucket，強烈建議您停用值區的「值區鎖定」和「軟刪除」保留政策。如果匯出至設有這類資料保留政策的 bucket，BigQuery 會嘗試將檔案重新寫入 bucket，但如果 bucket 的資料保留政策禁止覆寫檔案，這項作業就會失敗，導致產生額外費用。匯出完成後，即可重新啟用這些政策。

* 您無法將資料表資料匯出至本機檔案、Google 試算表或 Google 雲端硬碟。唯一支援的匯出位置是 Cloud Storage。如需儲存查詢結果的相關資訊，請查看[下載並儲存查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#downloading-saving-results-console)一節。
* 您最多可將 1 GB 的邏輯資料表資料匯出至單一檔案。如果您匯出的資料超過 1 GB，請使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw#exporting_data_into_one_or_more_files)將資料匯出到多個檔案。當您將資料匯出成多個檔案時，各個檔案的大小會有所差異。如要[限制匯出檔案大小](#limit_the_exported_file_size)，可以分割資料並匯出每個分割區。
* 使用 `EXPORT DATA` 陳述式時，系統不保證產生的檔案大小。
* 擷取作業產生的檔案數量可能有所不同。
* 您無法將巢狀與重複資料匯出成 CSV 格式。巢狀與重複資料適用於 Avro、JSON 和 Parquet 匯出。
* 匯出 [JSON](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#json_type) 格式的資料時，系統會將 [INT64](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types) (整數) 資料類型編碼為 JSON 字串，以便該資料讓其他系統讀取時能保留 64 位元精確度。
* 您無法在單一擷取工作中，從多個資料表匯出資料。
* 使用 Google Cloud 控制台匯出資料時，無法選擇 `GZIP` 以外的其他壓縮類型。
* 以 JSON 格式匯出表格時，系統會使用 Unicode 標記 `\uNNNN` 轉換符號 `<`、`>` 和 `&`，其中 `N` 是十六進位數字。舉例來說，`profit&loss` 會變為 `profit\u0026loss`。進行這項 Unicode 轉換是為了避免安全漏洞。
* 除非使用 [`EXPORT DATA`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw#export_data_statement) 陳述式，並在 `query_statement` 中指定 `ORDER BY` 子句，否則無法保證匯出資料表的資料順序。
* BigQuery 不支援 Cloud Storage 資源路徑在初始雙斜線後還有多個連續斜線。Cloud Storage 物件名稱可以包含多個連續的斜線 (「/」) 字元，但 BigQuery 會將多個連續斜線轉換為一個斜線。舉例來說，下列資源路徑在 Cloud Storage 中有效，但在 BigQuery 中則無效：`gs://bucket/my//object//name`。
* 如果擷取工作正在執行，期間載入 BigQuery 的任何新資料都不會納入該擷取工作。您必須建立新的擷取工作，才能匯出新資料。

## 事前準備

授予 [Identity and Access Management (IAM)](https://docs.cloud.google.com/iam/docs?hl=zh-tw) 角色，讓使用者擁有執行本文各項工作所需的權限。

### 所需權限

如要執行本文中的工作，您需要下列權限。

#### 從 BigQuery 資料表匯出資料的權限

如要從 BigQuery 資料表匯出資料，您需要 `bigquery.tables.export`IAM 權限。

下列預先定義的 IAM 角色都具備 `bigquery.tables.export` 權限：

* `roles/bigquery.dataViewer`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.admin`

#### 執行擷取工作的權限

如要執行擷取[工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)，您需要 `bigquery.jobs.create` IAM 權限。

下列每個預先定義的 IAM 角色都包含執行擷取作業所需的權限：

* `roles/bigquery.user`
* `roles/bigquery.jobUser`
* `roles/bigquery.admin`

#### 將資料寫入 Cloud Storage bucket 的權限

如要將資料寫入現有的 Cloud Storage 值區，您需要下列 IAM 權限：

* `storage.objects.create`
* `storage.objects.delete`

下列每個預先定義的 IAM 角色都包含將資料寫入現有 Cloud Storage 值區所需的權限：

* `roles/storage.objectAdmin`
* `roles/storage.admin`

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 匯出格式與壓縮類型

BigQuery 支援下列匯出資料用的資料格式與壓縮類型：

| 資料格式 | 支援的壓縮類型 | 說明 |
| --- | --- | --- |
| CSV | GZIP | 您可以控制已匯出資料中的 CSV 分隔符號，方法是使用 [`--field_delimiter`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_extract) bq 指令列工具旗標，或是使用 [`configuration.extract.fieldDelimiter`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationextract) 解壓縮工作屬性。  不支援巢狀與重複資料。 |
| JSON | GZIP | 支援巢狀與重複資料。 |
| Avro | DEFLATE、SNAPPY | Avro 不支援以 GZIP 格式匯出項目。  支援巢狀和重複資料。請參閱「[Avro 匯出詳細資料](#avro_export_details)」。 |
| Parquet | SNAPPY、GZIP、ZSTD | 支援巢狀和重複資料。詳情請參閱 [Parquet 匯出詳細資料](#parquet_export_details)。 |

## 匯出資料

以下各節說明如何將資料表資料、資料表的中繼資料和查詢結果匯出至 Cloud Storage。

### 匯出資料表資料

請透過下列方式匯出資料表的資料：

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具中的 [`bq extract`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_extract) 指令
* 使用 API 或用戶端程式庫提交 `extract` 工作

請選取下列其中一個選項：

### 控制台

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
4. 依序點選「總覽」**>「表格」**，然後選取所需表格。
5. 在詳細資料窗格中，按一下「上傳」「匯出」。
6. 在「Export to Google Storage」(匯出至 Google Cloud Storage) 對話方塊中：

   * 針對「GCS Location」(GCS 位置)，請瀏覽至您要匯出資料的值區、資料夾或檔案。
   * 為「Export format」(匯出格式) 選擇以下其中一種匯出資料格式：[CSV]、[JSON (Newline Delimited)] (JSON (以換行符號分隔))、[Avro] 或 [Parquet]。
   * 針對「Compression」(壓縮選項)，請選取壓縮格式，或選取 `None` 表示不壓縮。
7. 按一下「儲存」即可匯出資料表。

如要查看工作進度，請在「Explorer」窗格中按一下「Job history」，然後尋找「EXTRACT」類型的工作。

如要將檢視區塊匯出至 Cloud Storage，請使用 [`EXPORT DATA OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)。

### SQL

使用 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw#export_data_statement)。以下範例會從名為 `mydataset.table1` 的資料表匯出所選欄位：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   EXPORT DATA
     OPTIONS (
       uri = 'gs://bucket/folder/*.csv',
       format = 'CSV',
       overwrite = true,
       header = true,
       field_delimiter = ';')
   AS (
     SELECT field1, field2
     FROM mydataset.table1
     ORDER BY field1
   );
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

**注意：** `EXPORT DATA` 陳述式中的 `LIMIT` 子句通常會導致匯出工作執行緩慢。因此，我們不建議在 `EXPORT DATA` 陳述式中使用 `LIMIT` 子句。

### bq

使用加上 `--destination_format` 旗標的 [`bq extract`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_extract) 指令。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

其他選用標記包括：

* `--compression`：匯出檔案所用的壓縮類型。
* `--field_delimiter`：匯出作業在採用 CSV 格式的輸出檔案中，用來表示不同資料欄之間界線的字元。`\t` 和 `tab` 都可用來表示 Tab 字元分隔。
* `--print_header`：如果有指定該旗標，系統在列印有標頭的格式 (例如 CSV) 時，就會列印標頭列。

```
bq extract --location=location \
--destination_format format \
--compression compression_type \
--field_delimiter delimiter \
--print_header=boolean \
project_id:dataset.table \
gs://bucket/filename.ext
```

其中：

* location 是您的位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* format 是資料匯出格式：`CSV`、`NEWLINE_DELIMITED_JSON`、`AVRO` 或 `PARQUET`。
* compression\_type：所選擇資料格式支援的壓縮類型。請參閱「[匯出格式與壓縮類型](#export_formats_and_compression_types)」。
* delimiter：在 CSV 格式的匯出檔案中，用來指定不同資料欄之間界線的字元。`\t` 和 `tab` 都是可接受的 Tab 分隔名稱。
* boolean 為 `true` 或 `false`。設定為 `true` 時，如果資料格式支援標頭，系統在列印匯出的資料時就會列印標頭列。預設值為 `true`。
* project\_id 是您的專案 ID。
* dataset 是來源資料集的名稱。
* table 是您要匯出的資料表。如果您使用[分區裝飾器](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#partition_decorators)，則必須在資料表路徑前後加上半形單引號，或逸出 `$` 字元。
* bucket 是匯出資料的目標 Cloud Storage 值區名稱。BigQuery 資料集與 Cloud Storage 值區必須位於相同的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
* filename.ext 是匯出的資料檔案名稱和副檔名。您可以使用[萬用字元](#exporting_data_into_one_or_more_files)，將資料匯出至多個檔案。

範例：

舉例來說，下列指令會把 `mydataset.mytable` 匯出成名為 `myfile.csv` 的 gzip 壓縮檔，而 `myfile.csv` 會儲存在名為 `example-bucket` 的 Cloud Storage 值區中。

```
bq extract \
--compression GZIP \
'mydataset.mytable' \
gs://example-bucket/myfile.csv
```

預設目的地格式為 CSV。如要匯出為 JSON 或 Avro 格式，請使用 `destination_format` 旗標並將其設為 `NEWLINE_DELIMITED_JSON` 或 `AVRO`。例如：

```
bq extract \
--destination_format NEWLINE_DELIMITED_JSON \
'mydataset.mytable' \
gs://example-bucket/myfile.json
```

下列指令會把 `mydataset.mytable` 匯出成採用 Snappy 壓縮類型的 Avro 格式檔案，檔案名稱為 `myfile.avro`。而系統會把 `myfile.avro` 匯出到名為 `example-bucket` 的 Cloud Storage 值區。

```
bq extract \
--destination_format AVRO \
--compression SNAPPY \
'mydataset.mytable' \
gs://example-bucket/myfile.avro
```

下列指令會將 `mydataset.my_partitioned_table` 的單一分區匯出至 Cloud Storage 中的 CSV 檔案：

```
bq extract \
--destination_format CSV \
'mydataset.my_partitioned_table$0' \
gs://example-bucket/single_partition.csv
```

### API

如要匯出資料，請建立 `extract` 工作，並填入工作設定。

**注意：** 如要將資料匯出為 Parquet 格式，建議使用 [BigQuery Export to Parquet (透過 BigQuery Storage API) 範本](https://docs.cloud.google.com/dataflow/docs/guides/templates/provided/bigquery-to-parquet?hl=zh-tw)，而非自行編寫解決方案，這樣可能更快。

(選擇性操作) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性內指定您的位置。

1. 建立指向 BigQuery 來源資料與 Cloud Storage 目的地的擷取工作。
2. 指定來源資料表，方法是使用包含專案 ID、資料集 ID 和資料表 ID 的 `sourceTable` 設定物件。
3. `destination URI(s)` 屬性必須是完整的，且必須符合下列格式：`gs://bucket/filename.ext`。每個 URI 都可以包含一個「\*」萬用字元，而且它必須出現在值區名稱之後。
4. 設定 `configuration.extract.destinationFormat` 屬性以指定資料格式。舉例來說，如要匯出 JSON 檔案，請將此屬性值設為 `NEWLINE_DELIMITED_JSON`。
5. 如要查看工作狀態，請利用初始要求所傳回的工作 ID 來呼叫 [jobs.get(job\_id)](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/get?hl=zh-tw)。

   * 如果是 `status.state = DONE`，代表工作已順利完成。
   * 如果出現 `status.errorResult` 屬性，代表要求執行失敗，且該物件將包含所發生錯誤的相關訊息。
   * 如果沒有出現 `status.errorResult`，代表工作已順利完成，但過程中可能發生了幾個不嚴重的錯誤。不嚴重的錯誤都會列在已傳回工作物件的 `status.errors` 屬性中。

**API 附註：**

* 最佳做法就是產生唯一識別碼，並在呼叫 `jobs.insert` 來建立工作時，將該唯一識別碼當做 `jobReference.jobId` 傳送。這個方法較不受網路故障問題的影響，因為用戶端可對已知的工作 ID 進行輪詢或重試。
* 針對指定的工作 ID 呼叫 `jobs.insert` 算是種冪等運算；換句話說，您可以針對同一個工作 ID 重試作業無數次，但在這些作業中最多只會有一個成功。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryExtractTable
{
    public void ExtractTable(
        string projectId = "your-project-id",
        string bucketName = "your-bucket-name")
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        // Define a destination URI. Use a single wildcard URI if you think
        // your exported data will be larger than the 1 GB maximum value.
        string destinationUri = $"gs://{bucketName}/shakespeare-*.csv";
        BigQueryJob job = client.CreateExtractJob(
            projectId: "bigquery-public-data",
            datasetId: "samples",
            tableId: "shakespeare",
            destinationUri: destinationUri
        );
        job = job.PollUntilCompleted().ThrowOnAnyError();  // Waits for the job to complete.
        Console.Write($"Exported table to {destinationUri}.");
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// exportTableAsCompressedCSV demonstrates using an export job to
// write the contents of a table into Cloud Storage as CSV.
func exportTableAsCSV(projectID, gcsURI string) error {
	// projectID := "my-project-id"
	// gcsUri := "gs://mybucket/shakespeare.csv"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	srcProject := "bigquery-public-data"
	srcDataset := "samples"
	srcTable := "shakespeare"

	gcsRef := bigquery.NewGCSReference(gcsURI)
	gcsRef.FieldDelimiter = ","

	extractor := client.DatasetInProject(srcProject, srcDataset).Table(srcTable).ExtractorTo(gcsRef)
	extractor.DisableHeader = true
	// You can choose to run the job in a specific location for more complex data locality scenarios.
	// Ex: In this example, source dataset and GCS bucket are in the US.
	extractor.Location = "US"

	job, err := extractor.Run(ctx)
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
import com.google.cloud.RetryOption;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.Table;
import com.google.cloud.bigquery.TableId;
import org.threeten.bp.Duration;

public class ExtractTableToCsv {

  public static void runExtractTableToCsv() {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "bigquery-public-data";
    String datasetName = "samples";
    String tableName = "shakespeare";
    String bucketName = "my-bucket";
    String destinationUri = "gs://" + bucketName + "/path/to/file";
    // For more information on export formats available see:
    // https://cloud.google.com/bigquery/docs/exporting-data#export_formats_and_compression_types
    // For more information on Job see:
    // https://googleapis.dev/java/google-cloud-clients/latest/index.html?com/google/cloud/bigquery/package-summary.html

    String dataFormat = "CSV";
    extractTableToCsv(projectId, datasetName, tableName, destinationUri, dataFormat);
  }

  // Exports datasetName:tableName to destinationUri as raw CSV
  public static void extractTableToCsv(
      String projectId,
      String datasetName,
      String tableName,
      String destinationUri,
      String dataFormat) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(projectId, datasetName, tableName);
      Table table = bigquery.getTable(tableId);

      Job job = table.extract(dataFormat, destinationUri);

      // Blocks until this job completes its execution, either failing or succeeding.
      Job completedJob =
          job.waitFor(
              RetryOption.initialRetryDelay(Duration.ofSeconds(1)),
              RetryOption.totalTimeout(Duration.ofMinutes(3)));
      if (completedJob == null) {
        System.out.println("Job not executed since it no longer exists.");
        return;
      } else if (completedJob.getStatus().getError() != null) {
        System.out.println(
            "BigQuery was unable to extract due to an error: \n" + job.getStatus().getError());
        return;
      }
      System.out.println(
          "Table export successful. Check in GCS bucket for the " + dataFormat + " file.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Table extraction job was interrupted. \n" + e.toString());
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
const {Storage} = require('@google-cloud/storage');

const bigquery = new BigQuery();
const storage = new Storage();

async function extractTableToGCS() {
  // Exports my_dataset:my_table to gcs://my-bucket/my-file as raw CSV.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";
  // const bucketName = "my-bucket";
  // const filename = "file.csv";

  // Location must match that of the source table.
  const options = {
    location: 'US',
  };

  // Export data from the table into a Google Cloud Storage file
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .extract(storage.bucket(bucketName).file(filename), options);

  console.log(`Job ${job.id} created.`);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/**
 * Extracts the given table as json to given GCS bucket.
 *
 * @param string $projectId The project Id of your Google Cloud Project.
 * @param string $datasetId The BigQuery dataset ID.
 * @param string $tableId The BigQuery table ID.
 * @param string $bucketName Bucket name in Google Cloud Storage
 */
function extract_table(
    string $projectId,
    string $datasetId,
    string $tableId,
    string $bucketName
): void {
    $bigQuery = new BigQueryClient([
      'projectId' => $projectId,
    ]);
    $dataset = $bigQuery->dataset($datasetId);
    $table = $dataset->table($tableId);
    $destinationUri = "gs://{$bucketName}/{$tableId}.json";
    // Define the format to use. If the format is not specified, 'CSV' will be used.
    $format = 'NEWLINE_DELIMITED_JSON';
    // Create the extract job
    $extractConfig = $table->extract($destinationUri)->destinationFormat($format);
    // Run the job
    $job = $table->runJob($extractConfig);  // Waits for the job to complete
    printf('Exported %s to %s' . PHP_EOL, $table->id(), $destinationUri);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# from google.cloud import bigquery
# client = bigquery.Client()
# bucket_name = 'my-bucket'
project = "bigquery-public-data"
dataset_id = "samples"
table_id = "shakespeare"

destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.csv")
dataset_ref = bigquery.DatasetReference(project, dataset_id)
table_ref = dataset_ref.table(table_id)

extract_job = client.extract_table(
    table_ref,
    destination_uri,
    # Location must match that of the source table.
    location="US",
)  # API request
extract_job.result()  # Waits for job to complete.

print(
    "Exported {}:{}.{} to {}".format(project, dataset_id, table_id, destination_uri)
)
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def extract_table bucket_name = "my-bucket",
                  dataset_id  = "my_dataset_id",
                  table_id    = "my_table_id"
  bigquery = Google::Cloud::Bigquery.new
  dataset  = bigquery.dataset dataset_id
  table    = dataset.table    table_id

  # Define a destination URI. Use a single wildcard URI if you think
  # your exported data will be larger than the 1 GB maximum value.
  destination_uri = "gs://#{bucket_name}/output-*.csv"

  extract_job = table.extract_job destination_uri do |config|
    # Location must match that of the source table.
    config.location = "US"
  end
  extract_job.wait_until_done! # Waits for the job to complete

  puts "Exported #{table.id} to #{destination_uri}"
end
```

### 匯出資料表中繼資料

如要從 [Iceberg 資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw)匯出資料表的中繼資料，請使用下列 SQL 陳述式：

```
EXPORT TABLE METADATA FROM `[[PROJECT_NAME.]DATASET_NAME.]TABLE_NAME`;
```

更改下列內容：

* PROJECT\_NAME：資料表的專案名稱。預設值為執行這項查詢的專案。
* DATASET\_NAME：資料表的資料集名稱。
* TABLE\_NAME：資料表名稱。

匯出的中繼資料位於 STORAGE\_URI`/metadata` 資料夾中，其中 STORAGE\_URI 是在選項中設定的表格儲存位置。

### 匯出查詢結果

如要將查詢結果匯出至 Cloud Storage，請按照下列步驟操作： Google Cloud

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「SQL 查詢」add\_box。
3. 在「Query editor」(查詢編輯器) 文字區域中輸入有效的 GoogleSQL 查詢。
4. 按一下「執行」。
5. 傳回結果時，依序點按「儲存結果」>「Cloud Storage」。
6. 在「Export to Google Storage」(匯出至 Google Cloud Storage) 對話方塊中：

   * 針對「GCS Location」(GCS 位置)，請瀏覽至您要匯出資料的值區、資料夾或檔案。
   * 為「Export format」(匯出格式) 選擇以下其中一種匯出資料格式：[CSV]、[JSON (Newline Delimited)] (JSON (以換行符號分隔))、[Avro] 或 [Parquet]。
   * 針對「Compression」(壓縮選項)，請選取壓縮格式，或選取 `None` 表示不壓縮。
7. 按一下「儲存」即可匯出查詢結果。

如要查看工作進度，請展開「Job history」(工作記錄) 窗格，然後尋找 `EXTRACT` 類型的工作。

## Avro 匯出詳細資料

BigQuery 可以透過以下方式表示 Avro 格式的資料：

* 結果匯出檔案是 Avro 容器檔案。
* 每個 BigQuery 資料列都會表示為一筆 Avro 記錄。巢狀資料會以巢狀記錄物件來表示。
* `REQUIRED` 欄位會表示為對應 Avro 類型。舉例來說，BigQuery 的 `INTEGER` 類型就會對應到 Avro 的 `LONG` 類型。
* `NULLABLE` 欄位會表示為對應類型的 Avro Union 與「空值」。
* `REPEATED` 欄位會表示為 Avro 陣列。
* 在「擷取工作」和「匯出資料 SQL」中，`TIMESTAMP` 資料類型預設會表示為 `timestamp-micros` 邏輯類型 (會註解 Avro `LONG` 類型)。(注意：您可以將 `use_avro_logical_types=False` 新增至 `Export Data Options`，停用邏輯型別，改為在時間戳記資料欄上使用 `string` 型別，但在擷取工作中，系統一律會使用 Avro 邏輯型別)。
* 在「匯出資料 SQL」中，`DATE` 資料類型預設會表示為 `date` 邏輯類型 (會註解 Avro `INT` 類型)，但在「擷取工作」中，預設會表示為 `string` 類型。(注意：您可以在 `Export Data Options` 中加入 `use_avro_logical_types=False`，停用邏輯型別，或使用 `--use_avro_logical_types=True` 旗標，在擷取工作中啟用邏輯型別)。
* 在「匯出資料 SQL」中，`TIME` 資料類型預設會表示為 `timestamp-micro` 邏輯類型 (會註解 Avro `LONG` 類型)，但在「擷取工作」中，預設會表示為 `string` 類型。(注意：您可以在 `Export Data Options` 中加入 `use_avro_logical_types=False` 來停用邏輯型別，或使用 `--use_avro_logical_types=True` 旗標在擷取工作中啟用邏輯型別)。
* 在「匯出資料」SQL 中，`DATETIME` 資料類型預設會表示為 Avro `STRING` 類型 (具有自訂命名邏輯類型 `datetime` 的字串類型)，但在「擷取」工作中，預設會表示為 `string` 類型。(注意：您可以在 `Export Data Options` 中新增 `use_avro_logical_types=False`，停用邏輯型別，或使用 `--use_avro_logical_types=True` 旗標在擷取工作中啟用邏輯型別)。
* Avro 匯出作業不支援 [RANGE 類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#range_type)。

**注意：** 字串類型編碼遵循網際網路工程任務組 (IETF) 的 [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) 規格。

參數化 `NUMERIC(P[, S])` 和 `BIGNUMERIC(P[, S])` 資料類型會將精確度和比例類型參數移轉至 Avro 十進位邏輯類型。

**注意：**

* 如果將 `DATETIME` 類型匯出為 Avro，您無法直接將 Avro 檔案載入回相同的資料表結構定義，因為轉換後的 `STRING` 不符合結構定義。如要解決這個問題，請將檔案載入暫存資料表。
  然後使用 SQL 查詢將欄位轉換為 `DATETIME` 型別，並將結果儲存至新資料表。詳情請參閱「[變更資料欄的資料類型](https://docs.cloud.google.com/bigquery/docs/manually-changing-schemas?hl=zh-tw#changing_a_columns_data_type) 」。
* 指定「匯出資料選項」`use_avro_logical_types`和「擷取工作」旗標 `--use_avro_logical_types`後，系統會同時將這些選項套用至所有邏輯類型。

Avro 格式無法與 GZIP 壓縮搭配使用。如要壓縮 Avro 資料，請使用 bq 指令列工具或 API，然後指定支援壓縮 Avro 資料的類型之一：`DEFLATE` 或 `SNAPPY`。

## Parquet 匯出詳細資料

BigQuery 會將 GoogleSQL 資料類型轉換為下列 Parquet 資料類型：

| BigQuery 資料類型 | Parquet 原始類型 | Parquet 邏輯類型 |
| --- | --- | --- |
| 整數 | `INT64` | `NONE` |
| 數字 | `FIXED_LEN_BYTE_ARRAY` | `DECIMAL (precision = 38, scale = 9)` |
| Numeric(P[, S]) | `FIXED_LEN_BYTE_ARRAY` | `DECIMAL (precision = P, scale = S)` |
| 大數值 | `FIXED_LEN_BYTE_ARRAY` | `DECIMAL (precision = 76, scale = 38)` |
| BigNumeric(P[, S]) | `FIXED_LEN_BYTE_ARRAY` | `DECIMAL (precision = P, scale = S)` |
| 浮點 | `FLOAT` | `NONE` |
| 布林值 | `BOOLEAN` | `NONE` |
| 字串 | `BYTE_ARRAY` | `STRING` `(UTF8)` |
| 位元組 | `BYTE_ARRAY` | `NONE` |
| 日期 | `INT32` | `DATE` |
| 日期時間 | `INT64` | `TIMESTAMP (isAdjustedToUTC = false, unit = MICROS)` |
| 時間 | `INT64` | `TIME (isAdjustedToUTC = true, unit = MICROS)` |
| 時間戳記 | `INT64` | `TIMESTAMP (isAdjustedToUTC = false, unit = MICROS)` |
| 地理位置 | `BYTE_ARRAY` | `GEOGRAPHY (edges = spherical)` |

Parquet 結構定義會將巢狀資料表示為群組，並將重複記錄表示為重複群組。如要進一步瞭解如何在 BigQuery 中使用巢狀和重複資料，請參閱[指定巢狀和重複欄](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw)。

**注意：** 如果將 `DATETIME` 類型匯出為 Parquet，您無法直接將 Parquet 檔案載回相同的資料表結構定義，因為轉換後的值與結構定義不符。

您可以對 `DATETIME` 類型使用下列解決方法：

* 將檔案載入暫存資料表。然後使用 SQL 查詢將欄位轉換為 `DATETIME`，並將結果儲存至新資料表。詳情請參閱「[變更資料欄的資料類型](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw#change_a_columns_data_type)」。
* 在載入工作中，使用 `--schema` 旗標提供資料表結構定義。將日期時間資料欄定義為 `col:DATETIME`。

`GEOGRAPHY` 邏輯型別會以新增至匯出檔案的 [GeoParquet](https://geoparquet.org) 中繼資料表示。

## 將資料匯出為一或多個檔案

`destinationUris` 屬性會指出 BigQuery 所匯出檔案的一或多個目標位置和檔案名稱。

BigQuery 支援在每個 URI 中使用一個萬用字元運算子 (\*)。該萬用字元可出現在檔案名稱元件中的任何位置，使用萬用字元運算子就會指示 BigQuery 根據提供的模式建立多個資料分割檔案。萬用字元運算子會以數字取代 (從 0 開始)，向左填補到到 12 位數。例如，在檔案名稱結尾處使用萬用字元的 URI 建立的檔案，會在第一個檔案結尾附加 `000000000000`，在第二個檔案結尾附加 `000000000001`，依此類推。

下表說明 `destinationUris` 屬性的幾個可能選項：

| `destinationUris` 選項 | |
| --- | --- |
| 單一 URI | 如果要匯出的資料表資料大小沒有超過 1 GB，請使用單一 URI。這個選項是最常用的情況，因為匯出的資料一般會小於 1 GB 的上限值。[`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw#export_data_statement)不支援這個選項，您必須使用單一萬用字元 URI。  **屬性定義：**  `['gs://my-bucket/file-name.json']`  **建立：**     ``` gs://my-bucket/file-name.json ``` |
| 單一萬用字元 URI | 單一萬用字元只能用於 URI 的檔案名稱元件。  如果您認為要匯出的資料會超過 1 GB 的上限值，請使用單一萬用字元 URI。BigQuery 會根據您提供的模式，將資料分割為多個檔案。匯出檔案的大小會有所差異。  **屬性定義：**  `['gs://my-bucket/file-name-*.json']`  **建立：**     ``` gs://my-bucket/file-name-000000000000.json gs://my-bucket/file-name-000000000001.json gs://my-bucket/file-name-000000000002.json ... ```   `['gs://my-bucket/*']`  **建立：**     ``` gs://my-bucket/000000000000 gs://my-bucket/000000000001 gs://my-bucket/000000000002 ... ``` |

### 限制匯出檔案大小

如果單次匯出的資料超過 1 GB，請使用萬用字元將資料匯出到多個檔案，各個檔案的大小會有所差異。如要限制每個匯出檔案的大小上限，其中一個方法是隨機分割資料，然後將每個分割區匯出至檔案：

1. 決定所需的分區數量，這等於資料總大小除以所選匯出檔案大小。舉例來說，如果您有 8,000 MB 的資料，且希望每個匯出檔案約為 20 MB，則需要 400 個分割區。
2. 建立新的資料表，並依據名為 `export_id` 的新隨機產生資料欄進行分區和叢集處理。以下範例說明如何從現有資料表 (名為 `source_table`) 建立新的 `processed_table`，這需要 `n` 個分區才能達到所選檔案大小：

   ```
   CREATE TABLE my_dataset.processed_table
   PARTITION BY RANGE_BUCKET(export_id, GENERATE_ARRAY(0, n, 1))
   CLUSTER BY export_id
   AS (
     SELECT *, CAST(FLOOR(n*RAND()) AS INT64) AS export_id
     FROM my_dataset.source_table
   );
   ```
3. 針對介於 0 和 `n-1` 之間的每個整數 `i`，對下列查詢執行 `EXPORT DATA` 陳述式：

   ```
   SELECT * EXCEPT(export_id)
   FROM my_dataset.processed_table
   WHERE export_id = i;
   ```

### 擷取壓縮資料表

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// exportTableAsCompressedCSV demonstrates using an export job to
// write the contents of a table into Cloud Storage as compressed CSV.
func exportTableAsCompressedCSV(projectID, gcsURI string) error {
	// projectID := "my-project-id"
	// gcsURI := "gs://mybucket/shakespeare.csv"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	srcProject := "bigquery-public-data"
	srcDataset := "samples"
	srcTable := "shakespeare"

	gcsRef := bigquery.NewGCSReference(gcsURI)
	gcsRef.Compression = bigquery.Gzip

	extractor := client.DatasetInProject(srcProject, srcDataset).Table(srcTable).ExtractorTo(gcsRef)
	extractor.DisableHeader = true
	// You can choose to run the job in a specific location for more complex data locality scenarios.
	// Ex: In this example, source dataset and GCS bucket are in the US.
	extractor.Location = "US"

	job, err := extractor.Run(ctx)
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
import com.google.cloud.bigquery.ExtractJobConfiguration;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.TableId;

// Sample to extract a compressed table
public class ExtractTableCompressed {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String projectName = "MY_PROJECT_NAME";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String bucketName = "MY-BUCKET-NAME";
    String destinationUri = "gs://" + bucketName + "/path/to/file";
    // For more information on export formats available see:
    // https://cloud.google.com/bigquery/docs/exporting-data#export_formats_and_compression_types
    String compressed = "gzip";
    // For more information on Job see:
    // https://googleapis.dev/java/google-cloud-clients/latest/index.html?com/google/cloud/bigquery/package-summary.html
    String dataFormat = "CSV";

    extractTableCompressed(
        projectName, datasetName, tableName, destinationUri, dataFormat, compressed);
  }

  public static void extractTableCompressed(
      String projectName,
      String datasetName,
      String tableName,
      String destinationUri,
      String dataFormat,
      String compressed) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(projectName, datasetName, tableName);

      ExtractJobConfiguration extractConfig =
          ExtractJobConfiguration.newBuilder(tableId, destinationUri)
              .setCompression(compressed)
              .setFormat(dataFormat)
              .build();

      Job job = bigquery.create(JobInfo.of(extractConfig));

      // Blocks until this job completes its execution, either failing or succeeding.
      Job completedJob = job.waitFor();
      if (completedJob == null) {
        System.out.println("Job not executed since it no longer exists.");
        return;
      } else if (completedJob.getStatus().getError() != null) {
        System.out.println(
            "BigQuery was unable to extract due to an error: \n" + job.getStatus().getError());
        return;
      }
      System.out.println("Table extract compressed successful");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Table extraction job was interrupted. \n" + e.toString());
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
const {Storage} = require('@google-cloud/storage');

const bigquery = new BigQuery();
const storage = new Storage();

async function extractTableCompressed() {
  // Exports my_dataset:my_table to gcs://my-bucket/my-file as a compressed file.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";
  // const bucketName = "my-bucket";
  // const filename = "file.csv";

  // Location must match that of the source table.
  const options = {
    location: 'US',
    gzip: true,
  };

  // Export data from the table into a Google Cloud Storage file
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .extract(storage.bucket(bucketName).file(filename), options);

  console.log(`Job ${job.id} created.`);

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
# bucket_name = 'my-bucket'

destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.csv.gz")
dataset_ref = bigquery.DatasetReference(project, dataset_id)
table_ref = dataset_ref.table("shakespeare")
job_config = bigquery.job.ExtractJobConfig()
job_config.compression = bigquery.Compression.GZIP

extract_job = client.extract_table(
    table_ref,
    destination_uri,
    # Location must match that of the source table.
    location="US",
    job_config=job_config,
)  # API request
extract_job.result()  # Waits for job to complete.
```

## 用途範例

這個範例說明如何將資料匯出至 Cloud Storage。

假設您要從端點記錄檔持續將資料串流至 Cloud Storage，每天匯出快照到 Cloud Storage，以進行備份和封存。最佳選擇是[擷取作業](#export-data-in-bigquery)，但須遵守特定[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)和[限制](#export_limitations)。

使用 [API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 或[用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)提交擷取工作，並將專屬 ID 做為 **`jobReference.jobId`** 傳遞。擷取工作是
非同步。
[檢查工作狀態](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/get?hl=zh-tw)：使用建立工作時的專屬工作 ID。如果 **`status.status`** 為 **`DONE`**，代表工作已順利完成。如果存在 **`status.errorResult`**，表示工作失敗，需要重試。

**批次資料處理**

假設您使用夜間批次工作，在固定期限前載入資料。這項載入工作完成後，系統會如上一節所述，從查詢具體化統計資料表。系統會從這個資料表擷取資料，並彙整成 PDF 報表，然後傳送給監管機構。

由於需要讀取的資料量不大，請使用 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) API，以 JSON 字典格式擷取資料表的所有資料列。如果資料超過一頁，結果會設定 **`pageToken`** 屬性。如要擷取下一頁的結果，請再次發出 `tabledata.list` 呼叫，並透過 **`pageToken`** 參數提供代碼值。如果 API 呼叫失敗並顯示 [5xx 錯誤](https://docs.cloud.google.com/bigquery/docs/error-messages?hl=zh-tw)，請使用指數輪詢重試。大多數 4xx 錯誤都無法重試。為進一步分離 BigQuery 匯出作業和報表產生作業，結果應保留在磁碟中。

## 配額政策

如要瞭解擷取工作配額，請參閱「配額與限制」頁面的[擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)一節。

擷取工作的使用量可在 `INFORMATION_SCHEMA` 中查看。
擷取工作的 `JOBS_BY_*` 系統資料表中的工作項目包含 `total_bytes_processed` 值，可用於監控總用量，確保每天用量低於 50 TiB。如要瞭解如何查詢 `INFORMATION_SCHEMA.JOBS` 檢視畫面以取得 `total_bytes_processed` 值，請參閱 [`INFORMATION_SCHEMA.JOBS` 結構定義](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#schema)

### 查看目前的配額用量

您可以執行 `INFORMATION_SCHEMA` 查詢，查看特定時間範圍內執行的工作相關中繼資料，瞭解目前查詢、載入、擷取或複製工作的使用情形。您可以將目前用量與[配額限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)進行比較，判斷特定類型工作的配額用量。下列查詢範例會使用 `INFORMATION_SCHEMA.JOBS` 檢視表，依專案列出查詢、載入、擷取和複製工作的數量：

```
SELECT
  sum(case  when job_type="QUERY" then 1 else 0 end) as QRY_CNT,
  sum(case  when job_type="LOAD" then 1 else 0 end) as LOAD_CNT,
  sum(case  when job_type="EXTRACT" then 1 else 0 end) as EXT_CNT,
  sum(case  when job_type="COPY" then 1 else 0 end) as CPY_CNT
FROM `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE date(creation_time)= CURRENT_DATE()
```

您可以設定 [Cloud Monitoring](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw) 快訊政策，監控匯出的位元組數。

1. 前往 Google Cloud 控制台的 *notifications*「Alerting」(警告) 頁面：

   [前往「Alerting」(警告)](https://console.cloud.google.com/monitoring/alerting?hl=zh-tw)

   如果您是使用搜尋列尋找這個頁面，請選取子標題為「Monitoring」的結果。
2. 在「快訊」頁面中，按一下「建立政策」。
3. 在「政策設定模式」下方，選取「程式碼編輯器 (MQL 或 PromQL)」。
4. 在 **PromQL** 查詢編輯器中，輸入下列查詢：

   ```
   (
     sum by (project_id, quota_metric, location) (increase({"serviceruntime.googleapis.com/quota/rate/net_usage", monitored_resource="consumer_quota", service="bigquery.googleapis.com"}[1m]))
     /
     max by (project_id, quota_metric, location) ({"serviceruntime.googleapis.com/quota/limit", monitored_resource="consumer_quota", service="bigquery.googleapis.com", limit_name="ExtractBytesPerDay"})
   ) > 0.01
   ```

   如果「自動執行」未啟用，請點選「執行查詢」。
5. 設定其餘快訊，然後按一下「建立政策」。

如要瞭解如何建立以 PromQL 為基礎的快訊政策，請參閱「[建立以 PromQL 為基礎的快訊政策 (主控台)](https://docs.cloud.google.com/monitoring/promql/create-promql-alerts-console?hl=zh-tw)」。

## 疑難排解

診斷及排解擷取工作問題。

### 使用 Logs Explorer 診斷問題

如要診斷擷取作業的問題，可以使用 [Logs Explorer](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw) 查看特定擷取作業的記錄，並找出可能的錯誤。下列 Logs Explorer 篩選器會傳回擷取工作的相關資訊：

```
resource.type="bigquery_resource"
protoPayload.methodName="jobservice.insert"
(protoPayload.serviceData.jobInsertRequest.resource.jobConfiguration.query.query=~"EXPORT" OR
protoPayload.serviceData.jobCompletedEvent.eventName="extract_job_completed" OR
protoPayload.serviceData.jobCompletedEvent.job.jobConfiguration.query.query=~"EXPORT")
```

### 超出每日擷取位元組配額錯誤

如果專案的擷取作業超出預設的 50 TiB 每日上限，BigQuery 就會傳回這項錯誤。如要進一步瞭解擷取工作限制，請參閱「[擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)」。

**錯誤訊息**

```
Your usage exceeded quota for ExtractBytesPerDay
```

#### 診斷

如果匯出的資料表超過 50 TiB，匯出作業會失敗，因為[超過擷取限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)。如要[匯出特定資料表分區的資料表資料](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#export_table_data)，可以使用[分區修飾符](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#partition_decorators)來識別要匯出的分區。

如要收集最近幾天的匯出資料用量，可以嘗試下列做法：

* [查看專案配額](https://docs.cloud.google.com/docs/quotas/view-manage?hl=zh-tw#view_project_quotas)：使用 `Name: Extract bytes per day` 或 `Metric: bigquery.googleapis.com/quota/extract/bytes` 等篩選條件，並顯示用量圖表，即可查看幾天內的用量趨勢。
* 或者，您也可以查詢 [`INFORMATION_SCHEMA.JOBS_BY_PROJECT`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，查看幾天內的總擷取位元組。舉例來說，下列查詢會傳回過去七天內，`EXTRACT` 工作每天處理的位元組總數。

  ```
  SELECT
  TIMESTAMP_TRUNC(creation_time, DAY) AS day,
  SUM ( total_bytes_processed ) / POW(1024, 3) AS total_gibibytes_processed
  FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE
  creation_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY) AND CURRENT_TIMESTAMP()
  AND job_type = "EXTRACT"
  GROUP BY 1
  ORDER BY 2 DESC
  ```
* 然後找出耗用位元組數超出預期的特定工作，進一步縮小搜尋結果範圍。以下範例會傳回前 100 個 `EXTRACT` 工作，這些工作在過去七天內處理的資料量超過 100 GB。

  ```
  SELECT
  creation_time,
  job_id,
  total_bytes_processed/POW(1024, 3) AS total_gigabytes_processed
  FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE
  creation_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY) AND CURRENT_TIMESTAMP()
  AND job_type="EXTRACT"
  AND total_bytes_processed > (POW(1024, 3) * 100)
  ORDER BY
  total_bytes_processed DESC
  LIMIT 100
  ```

您也可以使用[工作探索器](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)，並搭配 `Bytes processed more than` 等篩選器，篩選出特定時間範圍內的高處理量工作。

#### 解析度

如要解決這項配額錯誤，其中一種方法是建立運算單元[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations)，然後將專案[指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)給具有 `PIPELINE` 工作類型的預留項目。由於這個方法使用專屬預留項目，而非免費的共用運算單元集區，因此可以略過限制檢查。如有需要，您可以刪除預留項目，以便日後使用共用運算單元集區。

如要瞭解如何匯出超過 50 TiB 的資料，請參閱「[擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)」的附註部分。

## 定價

如要瞭解資料匯出定價，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing)頁面。

匯出資料之後，系統會因您在 Cloud Storage 中儲存資料而向您收取費用。詳情請參閱 [Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)。

## 資料表安全性

如要控管 BigQuery 資料表的存取權，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

## 後續步驟

* 如要進一步瞭解 Google Cloud 控制台，請參閱「[使用 Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)」。
* 如要進一步瞭解 bq 指令列工具，請參閱「[使用 bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)」。
* 如要瞭解如何使用 Google BigQuery API 用戶端程式庫來建立應用程式，請參閱[用戶端程式庫快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]