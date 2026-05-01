* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 更新資料集存取權限 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

更新資料集的存取權控管設定。

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

// updateDatasetAccessControl demonstrates how the access control policy of a dataset
// can be amended by adding an additional entry corresponding to a specific user identity.
func updateDatasetAccessControl(projectID, datasetID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	ds := client.Dataset(datasetID)
	meta, err := ds.Metadata(ctx)
	if err != nil {
		return err
	}
	// Append a new access control entry to the existing access list.
	update := bigquery.DatasetMetadataToUpdate{
		Access: append(meta.Access, &bigquery.AccessEntry{
			Role:       bigquery.ReaderRole,
			EntityType: bigquery.UserEmailEntity,
			Entity:     "sample.bigquery.dev@gmail.com"},
		),
	}

	// Leverage the ETag for the update to assert there's been no modifications to the
	// dataset since the metadata was originally read.
	if _, err := ds.Update(ctx, update, meta.ETag); err != nil {
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.Acl;
import com.google.cloud.bigquery.Acl.Role;
import com.google.cloud.bigquery.Acl.User;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import java.util.ArrayList;

public class UpdateDatasetAccess {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    // Create a new ACL granting the READER role to "sample.bigquery.dev@gmail.com"
    // For more information on the types of ACLs available see:
    // https://cloud.google.com/storage/docs/access-control/lists
    Acl newEntry = Acl.of(new User("sample.bigquery.dev@gmail.com"), Role.READER);

    updateDatasetAccess(datasetName, newEntry);
  }

  public static void updateDatasetAccess(String datasetName, Acl newEntry) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Dataset dataset = bigquery.getDataset(datasetName);

      // Get a copy of the ACLs list from the dataset and append the new entry
      ArrayList<Acl> acls = new ArrayList<>(dataset.getAcl());
      acls.add(newEntry);

      bigquery.update(dataset.toBuilder().setAcl(acls).build());
      System.out.println("Dataset Access Control updated successfully");
    } catch (BigQueryException e) {
      System.out.println("Dataset Access control was not updated \n" + e.toString());
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

async function updateDatasetAccess() {
  // Update a datasets's access controls.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";

  // Create new role metadata
  const newRole = {
    role: 'READER',
    entity_type: 'userByEmail',
    userByEmail: 'sample.bigquery.dev@gmail.com',
  };

  // Retreive current dataset metadata
  const dataset = bigquery.dataset(datasetId);
  const [metadata] = await dataset.getMetadata();

  // Add new role to role acess array
  metadata.access.push(newRole);
  const [apiResponse] = await dataset.setMetadata(metadata);
  const newAccessRoles = apiResponse.access;
  newAccessRoles.forEach(role => console.log(role));
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# TODO(developer): Set dataset_id to the ID of the dataset to fetch.
dataset_id = "your-project.your_dataset"

# TODO(developer): Set entity_id to the ID of the email or group from whom
# you are adding access. Alternatively, to the JSON REST API representation
# of the entity, such as a view's table reference.
entity_id = "user-or-group-to-add@example.com"

from google.cloud.bigquery.enums import EntityTypes

# TODO(developer): Set entity_type to the type of entity you are granting access to.
# Common types include:
#
# * "userByEmail" -- A single user or service account. For example "fred@example.com"
# * "groupByEmail" -- A group of users. For example "example@googlegroups.com"
# * "view" -- An authorized view. For example
#       {"projectId": "p", "datasetId": "d", "tableId": "v"}
#
# For a complete reference, see the REST API reference documentation:
# https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets#Dataset.FIELDS.access
entity_type = EntityTypes.GROUP_BY_EMAIL

# TODO(developer): Set role to a one of the "Basic roles for datasets"
# described here:
# https://cloud.google.com/bigquery/docs/access-control-basic-roles#dataset-basic-roles
role = "READER"

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

dataset = client.get_dataset(dataset_id)  # Make an API request.

entries = list(dataset.access_entries)
entries.append(
    bigquery.AccessEntry(
        role=role,
        entity_type=entity_type,
        entity_id=entity_id,
    )
)
dataset.access_entries = entries

dataset = client.update_dataset(dataset, ["access_entries"])  # Make an API request.

full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
print(
    "Updated dataset '{}' with modified user permissions.".format(full_dataset_id)
)
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]