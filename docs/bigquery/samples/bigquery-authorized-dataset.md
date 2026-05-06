Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 授權 BigQuery 資料集 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

授權 BigQuery 資料集

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.Acl;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import com.google.cloud.bigquery.DatasetId;
import com.google.common.collect.ImmutableList;
import java.util.ArrayList;
import java.util.List;

public class AuthorizeDataset {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "PROJECT_ID";
    String sourceDatasetName = "BIGQUERY_SOURCE_DATASET_NAME";
    String userDatasetName = "BIGQUERY_USER_DATASET_NAME";
    authorizeDataset(
        DatasetId.of(projectId, sourceDatasetName), DatasetId.of(projectId, userDatasetName));
  }

  // This method will update sourceDataset's ACL with userDataset's ACL
  public static void authorizeDataset(DatasetId sourceDatasetId, DatasetId userDatasetId) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Get both source and user dataset's references
      Dataset sourceDataset = bigquery.getDataset(sourceDatasetId);
      Dataset userDataset = bigquery.getDataset(userDatasetId);

      // Get the source dataset's ACL
      List<Acl> sourceDatasetAcl = new ArrayList<>(sourceDataset.getAcl());

      // Add the user dataset's DatasetAccessEntry object to the existing sourceDatasetAcl
      List<String> targetTypes = ImmutableList.of("VIEWS");
      Acl.DatasetAclEntity userDatasetAclEntity =
          new Acl.DatasetAclEntity(userDatasetId, targetTypes);
      sourceDatasetAcl.add(Acl.of(userDatasetAclEntity));

      // update the source dataset with user dataset's ACL
      Dataset updatedSourceDataset =
          sourceDataset.toBuilder().setAcl(sourceDatasetAcl).build().update();

      System.out.printf(
          "Dataset %s updated with the added authorization\n", updatedSourceDataset.getDatasetId());

    } catch (BigQueryException e) {
      System.out.println("Dataset Authorization failed due to error: \n" + e);
    }
  }
}
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

##
# This is a snippet for showcasing how to authorize a dataset.
#
# Note: Only views target types are supported for now.
#
# @param source_project_id [String] The ID of the source Google Cloud project.
# @param source_database_id [String] The ID of the source database.
# @param user_project_id [String] The ID of the user Google Cloud project.
# @param user_database_id [String] The ID of the user database.
# @param target_types [Array<String>] List of target types for authorization.
#
def authorized_dataset source_project_id:, source_database_id:, user_project_id:, user_database_id:, target_types:
  # Initialize client and get source dataset's references
  source_bigquery = Google::Cloud::Bigquery.new project_id: source_project_id
  source_dataset  = source_bigquery.dataset source_database_id

  # Initialize client and get user dataset's references
  user_bigquery = Google::Cloud::Bigquery.new project_id: user_project_id
  user_dataset  = user_bigquery.dataset user_database_id

  # Add the user dataset's DatasetAccessEntry object to the existing source dataset rules
  source_dataset.access do |access|
    access.add_reader_dataset user_dataset.build_access_entry(target_types: target_types)
  end

  puts "Dataset #{user_dataset.dataset_id} added as authorized dataset in dataset #{source_dataset.dataset_id}"
end
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]