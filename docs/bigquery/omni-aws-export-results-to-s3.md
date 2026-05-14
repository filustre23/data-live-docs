Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將查詢結果匯出至 Amazon S3

本文說明如何將針對 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)執行的查詢結果，匯出至 Amazon Simple Storage Service (Amazon S3) 值區。

如要瞭解 BigQuery 和 Amazon S3 之間的資料流程，請參閱「[匯出資料時的資料流程](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#export-data)」。

## 限制

如要查看適用於 Amazon S3 和 Blob 儲存體的 BigLake 資料表限制完整清單，請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#limitations)」。

## 事前準備

請確認您已備妥下列資源：

* [存取 Amazon S3 儲存貯體的連線](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-tw)。
* [Amazon S3 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)。
* 正確的 Amazon Web Services (AWS) Identity and Access Management (IAM)
  政策：
  + 您必須具備 `PutObject` 權限，才能將資料寫入 Amazon S3 bucket。
    詳情請參閱「[為 BigQuery 建立 AWS IAM 政策](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-tw#creating-aws-iam-policy)」。

* 如果您採用[以量計價的收費模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，請確保已為專案啟用 [BigQuery Reservation API](https://console.cloud.google.com/apis/library/bigqueryreservation.googleapis.com?hl=zh-tw)。如要瞭解定價資訊，請參閱「[BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)」一文。

## 匯出查詢結果

無論是否有現有內容，BigQuery Omni 都會寫入指定的 Amazon S3 位置。匯出查詢可以覆寫現有資料，或將查詢結果與現有資料混合。建議您將查詢結果匯出至空白的 Amazon S3 儲存空間。

如要執行查詢，請選取下列其中一個選項：

### SQL

在「Query editor」(查詢編輯器) 欄位中，輸入 GoogleSQL 匯出查詢。
GoogleSQL 是 Google Cloud 控制台的預設語法。

**注意：** 如要覆寫預設專案，請使用 `--project_id=PROJECT_ID` 參數。將 `PROJECT_ID` 替換為 Google Cloud 專案 ID。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
      EXPORT DATA WITH CONNECTION `CONNECTION_REGION.CONNECTION_NAME`
      OPTIONS(uri="s3://BUCKET_NAME/PATH", format="FORMAT", ...)
      AS QUERY
   ```

   更改下列內容：

   * `CONNECTION_REGION`：建立連線的區域。
   * `CONNECTION_NAME`：您建立的連線名稱，必須具備寫入 Amazon S3 儲存貯體的必要權限。
   * `BUCKET_NAME`：要寫入資料的 Amazon S3 儲存桶。
   * `PATH`：要寫入匯出檔案的路徑。路徑字串的葉節點目錄中必須剛好包含一個萬用字元 `*`，例如 `../aa/*`、`../aa/b*c`、`../aa/*bc` 和 `../aa/bc*`。BigQuery 會根據匯出的檔案數量，將 `*` 替換為 `0000..N`。BigQuery 會判斷檔案數量和大小。如果 BigQuery 決定匯出兩個檔案，則第一個檔案名稱中的 `*` 會替換為 `000000000000`，第二個檔案名稱中的 `*` 會替換為 `000000000001`。
   * `FORMAT`：支援的格式為 `JSON`、`AVRO`、`CSV` 和 `PARQUET`。
   * `QUERY`：用於分析 BigLake 資料表中儲存資料的查詢。包含查詢所用 BigLake 資料表的資料集，必須與目標 Amazon S3 值區位於相同的 [Amazon S3 區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)。
   * 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;

// Sample to export query results to Amazon S3 bucket
public class ExportQueryResultsToS3 {

  public static void main(String[] args) throws InterruptedException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    String externalTableName = "MY_EXTERNAL_TABLE_NAME";
    // connectionName should be in the format of connection_region.connection_name. e.g.
    // aws-us-east-1.s3-write-conn
    String connectionName = "MY_CONNECTION_REGION.MY_CONNECTION_NAME";
    // destinationUri must contain exactly one * anywhere in the leaf directory of the path string
    // e.g. ../aa/*, ../aa/b*c, ../aa/*bc, and ../aa/bc*
    // BigQuery replaces * with 0000..N depending on the number of files exported.
    // BigQuery determines the file count and sizes.
    String destinationUri = "s3://your-bucket-name/*";
    String format = "EXPORT_FORMAT";
    // Export result of query to find states starting with 'W'
    String query =
        String.format(
            "EXPORT DATA WITH CONNECTION `%s` OPTIONS(uri='%s', format='%s') "
              + "AS SELECT * FROM %s.%s.%s WHERE name LIKE 'W%%'",
            connectionName, destinationUri, format, projectId, datasetName, externalTableName);
    exportQueryResultsToS3(query);
  }

  public static void exportQueryResultsToS3(String query) throws InterruptedException {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableResult results = bigquery.query(QueryJobConfiguration.of(query));

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query results exported to Amazon S3 successfully.");
    } catch (BigQueryException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

## 疑難排解

如果收到與 `quota failure` 相關的錯誤訊息，請檢查是否已為查詢保留容量。如要進一步瞭解預留配額，請參閱本文的「[事前準備](#before_you_begin)」一節。

## 後續步驟

* 瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 瞭解如何[匯出資料表資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)。
* 瞭解如何[查詢儲存在 Amazon S3 中的資料](https://docs.cloud.google.com/bigquery/docs/query-aws-data?hl=zh-tw)。
* 瞭解如何[為 BigQuery Omni 設定 VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/omni-vpc-sc?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]