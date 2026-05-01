* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 複製使用客戶自行管理的加密金鑰 (CMEK) 的資料表 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

複製使用客戶自行管理的加密金鑰 (CMEK) 的資料表。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [客戶管理的 Cloud KMS 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)

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

// copyTableWithCMEK demonstrates creating a copy of a table and ensuring the copied data is
// protected with a customer managed encryption key.
func copyTableWithCMEK(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	srcTable := client.DatasetInProject("bigquery-public-data", "samples").Table("shakespeare")
	copier := client.Dataset(datasetID).Table(tableID).CopierFrom(srcTable)
	copier.DestinationEncryptionConfig = &bigquery.EncryptionConfig{
		// TODO: Replace this key with a key you have created in Cloud KMS.
		KMSKeyName: "projects/cloud-samples-tests/locations/us-central1/keyRings/test/cryptoKeys/test",
	}
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
import com.google.cloud.bigquery.EncryptionConfiguration;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.TableId;

// Sample to copy a cmek table
public class CopyTableCmek {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String destinationDatasetName = "MY_DESTINATION_DATASET_NAME";
    String destinationTableId = "MY_DESTINATION_TABLE_NAME";
    String sourceDatasetName = "MY_SOURCE_DATASET_NAME";
    String sourceTableId = "MY_SOURCE_TABLE_NAME";
    String kmsKeyName = "MY_KMS_KEY_NAME";
    EncryptionConfiguration encryption =
        EncryptionConfiguration.newBuilder().setKmsKeyName(kmsKeyName).build();
    copyTableCmek(
        sourceDatasetName, sourceTableId, destinationDatasetName, destinationTableId, encryption);
  }

  public static void copyTableCmek(
      String sourceDatasetName,
      String sourceTableId,
      String destinationDatasetName,
      String destinationTableId,
      EncryptionConfiguration encryption) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId sourceTable = TableId.of(sourceDatasetName, sourceTableId);
      TableId destinationTable = TableId.of(destinationDatasetName, destinationTableId);

      // For more information on CopyJobConfiguration see:
      // https://googleapis.dev/java/google-cloud-clients/latest/com/google/cloud/bigquery/JobConfiguration.html
      CopyJobConfiguration configuration =
          CopyJobConfiguration.newBuilder(destinationTable, sourceTable)
              .setDestinationEncryptionConfiguration(encryption)
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
            "BigQuery was unable to copy table due to an error: \n" + job.getStatus().getError());
        return;
      }
      System.out.println("Table cmek copied successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Table cmek copying job was interrupted. \n" + e.toString());
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

# TODO(developer): Set dest_table_id to the ID of the destination table.
# dest_table_id = "your-project.your_dataset.your_table_name"

# TODO(developer): Set orig_table_id to the ID of the original table.
# orig_table_id = "your-project.your_dataset.your_table_name"

# Set the encryption key to use for the destination.
# TODO(developer): Replace this key with a key you have created in KMS.
# kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
#     your-project, location, your-ring, your-key
# )

job_config = bigquery.CopyJobConfig(
    destination_encryption_configuration=bigquery.EncryptionConfiguration(
        kms_key_name=kms_key_name
    )
)
job = client.copy_table(orig_table_id, dest_table_id, job_config=job_config)
job.result()  # Wait for the job to complete.

dest_table = client.get_table(dest_table_id)  # Make an API request.
if dest_table.encryption_configuration.kms_key_name == kms_key_name:
    print("A copy of the table created")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]