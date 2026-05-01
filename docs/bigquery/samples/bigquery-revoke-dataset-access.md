* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 撤銷資料集存取權 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

移除使用者或群組存取 BigQuery 資料集的權限。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [使用 IAM 控管資源的存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
)

// revokeAccessToDataset creates a new ACL removing the dataset access to "example-analyst-group@google.com" entity
// For more information on the types of ACLs available see:
// https://cloud.google.com/storage/docs/access-control/lists
func revokeAccessToDataset(w io.Writer, projectID, datasetID, entity string) error {
	// TODO(developer): uncomment and update the following lines:
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// entity := "user@mydomain.com"

	ctx := context.Background()

	// Create BigQuery client.
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	// Get dataset handler
	dataset := client.Dataset(datasetID)

	// Get dataset metadata
	meta, err := dataset.Metadata(ctx)
	if err != nil {
		return err
	}

	// Create new access entry list by copying the existing and omiting the access entry entity value
	var newAccessList []*bigquery.AccessEntry
	for _, entry := range meta.Access {
		if entry.Entity != entity {
			newAccessList = append(newAccessList, entry)
		}
	}

	// Only proceed with update if something in the access list was removed.
	// Additionally, we use the ETag from the initial metadata to ensure no
	// other changes were made to the access list in the interim.
	if len(newAccessList) < len(meta.Access) {
		update := bigquery.DatasetMetadataToUpdate{
			Access: newAccessList,
		}
		meta, err = dataset.Update(ctx, update, meta.ETag)
		if err != nil {
			return err
		}
	} else {
		return fmt.Errorf("any access entry was revoked")
	}

	fmt.Fprintf(w, "Details for Access entries in dataset %v.\n", datasetID)

	for _, access := range meta.Access {
		fmt.Fprintln(w)
		fmt.Fprintf(w, "Role: %s\n", access.Role)
		fmt.Fprintf(w, "Entity: %v\n", access.Entity)
	}

	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.Acl;
import com.google.cloud.bigquery.Acl.Entity;
import com.google.cloud.bigquery.Acl.Group;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import com.google.cloud.bigquery.DatasetId;
import java.util.List;

public class RevokeDatasetAccess {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    // Project and dataset from which to get the access policy.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    // Group to remove from the ACL
    String entityEmail = "group-to-remove@example.com";

    revokeDatasetAccess(projectId, datasetName, entityEmail);
  }

  public static void revokeDatasetAccess(String projectId, String datasetName, String entityEmail) {
    try {
      // Initialize client that will be used to send requests. This client only needs
      // to be created once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Create datasetId with the projectId and the datasetName.
      DatasetId datasetId = DatasetId.of(projectId, datasetName);
      Dataset dataset = bigquery.getDataset(datasetId);

      // Create a new Entity with the corresponding type and email
      // "user-or-group-to-remove@example.com"
      // For more information on the types of Entities available see:
      // https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Acl.Entity
      // and
      // https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Acl.Entity.Type
      Entity entity = new Group(entityEmail);

      // To revoke access to a dataset, remove elements from the Acl list.
      // Find more information about ACL and the Acl Class here:
      // https://cloud.google.com/storage/docs/access-control/lists
      // https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Acl
      // Remove the entity from the ACLs list.
      List<Acl> acls =
          dataset.getAcl().stream().filter(acl -> !acl.getEntity().equals(entity)).toList();

      // Update the ACLs by setting the new list.
      bigquery.update(dataset.toBuilder().setAcl(acls).build());
      System.out.println("ACLs of \"" + datasetName + "\" updated successfully");
    } catch (BigQueryException e) {
      System.out.println("ACLs were not updated \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
/**
 * TODO(developer): Update and un-comment below lines
 */

// const datasetId = "my_project_id.my_dataset"

// ID of the user or group from whom you are revoking access.
// const entityId = "user-or-group-to-remove@example.com"

const {BigQuery} = require('@google-cloud/bigquery');

// Instantiate a client.
const bigquery = new BigQuery();

async function revokeDatasetAccess() {
  const [dataset] = await bigquery.dataset(datasetId).get();

  // To revoke access to a dataset, remove elements from the access list.
  //
  // See the BigQuery client library documentation for more details on access entries:
  // https://cloud.google.com/nodejs/docs/reference/bigquery/latest

  // Filter access entries to exclude entries matching the specified entity_id
  // and assign a new list back to the access list.
  dataset.metadata.access = dataset.metadata.access.filter(entry => {
    return !(
      entry.entity_id === entityId ||
      entry.userByEmail === entityId ||
      entry.groupByEmail === entityId
    );
  });

  // Update will only succeed if the dataset
  // has not been modified externally since retrieval.
  //
  // See the BigQuery client library documentation for more details on metadata updates:
  // https://cloud.google.com/bigquery/docs/updating-datasets

  // Update just the 'access entries' property of the dataset.
  await dataset.setMetadata(dataset.metadata);

  console.log(`Revoked access to '${entityId}' from '${datasetId}'.`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery
from google.api_core.exceptions import PreconditionFailed

# TODO(developer): Update and uncomment the lines below.

# ID of the dataset to revoke access to.
# dataset_id = "my-project.my_dataset"

# ID of the user or group from whom you are revoking access.
# Alternatively, the JSON REST API representation of the entity,
# such as a view's table reference.
# entity_id = "user-or-group-to-remove@example.com"

# Instantiate a client.
client = bigquery.Client()

# Get a reference to the dataset.
dataset = client.get_dataset(dataset_id)

# To revoke access to a dataset, remove elements from the AccessEntry list.
#
# See the BigQuery client library documentation for more details on `access_entries`:
# https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.Dataset#google_cloud_bigquery_dataset_Dataset_access_entries

# Filter `access_entries` to exclude entries matching the specified entity_id
# and assign a new list back to the AccessEntry list.
dataset.access_entries = [
    entry for entry in dataset.access_entries
    if entry.entity_id != entity_id
]

# Update will only succeed if the dataset
# has not been modified externally since retrieval.
#
# See the BigQuery client library documentation for more details on `update_dataset`:
# https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_update_dataset
try:
    # Update just the `access_entries` property of the dataset.
    dataset = client.update_dataset(
        dataset,
        ["access_entries"],
    )

    # Notify user that the API call was successful.
    full_dataset_id = f"{dataset.project}.{dataset.dataset_id}"
    print(f"Revoked dataset access for '{entity_id}' to ' dataset '{full_dataset_id}.'")
except PreconditionFailed:  # A read-modify-write error.
    print(
        f"Dataset '{dataset.dataset_id}' was modified remotely before this update. "
        "Fetch the latest version and retry."
    )
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]