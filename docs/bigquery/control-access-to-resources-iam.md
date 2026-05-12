Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 IAM 控管資源的存取權

本文說明如何查看、授予及撤銷 BigQuery 資料集和資料集內資源 (資料表、檢視區塊和常式) 的存取控管。雖然模型也是資料集層級的資源，但您無法使用 IAM 角色授予個別模型的存取權。

您可以透過 Google Cloud *允許政策*，授予資源的存取權。這類政策又稱為 *Identity and Access Management (IAM) 政策*，會附加於資源。每項資源只能附加一項允許政策。
允許政策可控管資源本身的存取權，以及[沿用允許政策](https://docs.cloud.google.com/iam/docs/allow-policies?hl=zh-tw#inheritance)的資源後代。

如要進一步瞭解允許政策，請參閱 IAM 說明文件中的「[政策結構](https://docs.cloud.google.com/iam/docs/allow-policies?hl=zh-tw#structure)」。

本文假設您已熟悉 [Identity and Access Management (IAM)](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw)。 Google Cloud

## 限制

* [複製的日常安排](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)不會包含日常安排存取控制清單 (ACL)。
* 外部或連結資料集中的常式不支援存取控制項。
* 外部或連結資料集中的資料表不支援存取控制項。
* 您無法使用 Terraform 設定日常安排存取權控管機制。
* 您無法使用 Google Cloud SDK 設定例行存取控管機制。
* 無法使用 [BigQuery 資料控管語言 (DCL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw) 設定例行存取權控管。
* Data Catalog 不支援例行存取控管。如果使用者獲得的例行程序層級存取權設有條件，他們就不會在 BigQuery 側邊面板中看到自己的例行程序。解決方法是改為授予資料集層級的存取權。
* 「[`INFORMATION_SCHEMA.OBJECT_PRIVILEGES`」檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-object-privileges?hl=zh-tw)不會顯示日常作業的存取權控管。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。

### 必要的角色

如要取得修改資源 IAM 政策所需的權限，請要求管理員授予專案的 [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備修改資源 IAM 政策所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要修改資源的 IAM 政策，必須具備下列權限：

* 如要取得資料集的存取權政策：
  `bigquery.datasets.get`
* 如要設定資料集的存取權政策，請按照下列步驟操作：
  `bigquery.datasets.update`
* 如要取得資料集的存取權政策 (僅限Google Cloud 控制台)：
  `bigquery.datasets.getIamPolicy`
* 如何設定資料集的存取權政策 (僅限控制台)：
  `bigquery.datasets.setIamPolicy`
* 如要取得資料表或檢視表的政策：
  `bigquery.tables.getIamPolicy`
* 如要設定資料表或檢視的政策：
  `bigquery.tables.setIamPolicy`
* 如要取得日常安排的存取權政策：
  `bigquery.routines.getIamPolicy`
* 如要設定日常安排的存取權政策：
  `bigquery.routines.setIamPolicy`
* 如要建立 bq 工具或 [SQL BigQuery 作業](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw) (選用)：
  `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 使用資料集存取權控制

您可以授予 [IAM 主體](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw#allow)預先定義或自訂角色，決定主體在資料集中的權限，藉此提供資料集存取權。這也稱為將「允許政策」附加至資源。授予存取權後，您就能查看資料集的存取權控管設定，並撤銷資料集的存取權。

### 授予資料集存取權

使用 BigQuery 網頁版 UI 或 bq 指令列工具建立資料集時，無法授予資料集存取權。您必須先建立資料集，再授予存取權。API 可讓您在建立資料集時，透過呼叫 [`datasets.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw)，搭配已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)，授予存取權。

專案是資料集的父項資源，而資料集則是資料表、檢視表、常式和模型的父項資源。在專案層級授予角色時，資料集和資料集資源會繼承該角色及其權限。同樣地，在資料集層級授予角色時，資料集內的資源會繼承該角色及其權限。

您可以授予 IAM 角色，提供資料集存取權，或使用 IAM 條件有條件地授予存取權。如要進一步瞭解如何授予條件式存取權，請參閱「[使用 IAM 條件控管存取權](https://docs.cloud.google.com/bigquery/docs/conditions?hl=zh-tw#add-conditions-to-datasets)」。

**注意：** 授予資料集存取權後，系統不會自動在「Explorer」窗格中列出該資料集。

如要授予 IAM 角色資料集存取權，但不想使用條件，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 依序點選 person\_add「共用」>「權限」。
5. 按一下「新增主體」person\_add。
6. 在「New principals」(新增主體) 欄位中輸入主體。
7. 在「Select a role」(選取角色) 清單中，選取預先定義的角色或自訂角色。
8. 按一下 [儲存]。
9. 如要返回資料集資訊，請按一下「關閉」。

### SQL

如要授予主體資料集存取權，請使用 [`GRANT` DCL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw#grant_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   GRANT `ROLE_LIST`
   ON SCHEMA RESOURCE_NAME
   TO "USER_LIST"
   ```

   請替換下列項目：

   * `ROLE_LIST`：要授予的角色或以半形逗號分隔的角色清單
   * `RESOURCE_NAME`：您要授予存取權的資料集名稱
   * `USER_LIST`：以逗號分隔的使用者清單，這些使用者會獲得角色

     如需有效格式的清單，請參閱 [`user_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw#user_list)。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

下列範例會將 BigQuery 資料檢視者角色授予 `myDataset`：

```
GRANT `roles/bigquery.dataViewer`
ON SCHEMA `myProject`.myDataset
TO "user:user@example.com", "user:user2@example.com"
```

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 如要將現有資料集的資訊 (包括存取權控管設定) 寫入 JSON 檔案，請使用 [`bq show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show)：

   ```
   bq show \
       --format=prettyjson \
       PROJECT_ID:DATASET > PATH_TO_FILE
   ```

   更改下列內容：

   * PROJECT\_ID：專案 ID
   * DATASET：資料集名稱
   * PATH\_TO\_FILE：本機上 JSON 檔案的路徑
3. 變更 JSON 檔案的 `access` 區段。您可以新增任何 `specialGroup` 項目：`projectOwners`、`projectWriters`、`projectReaders` 和 `allAuthenticatedUsers`。您也可以新增下列任何項目：`userByEmail`、`groupByEmail` 和 `domain`。

   舉例來說，資料集 JSON 檔案中的 `access` 區段應會與以下內容類似：

   ```
   {
    "access": [
     {
      "role": "READER",
      "specialGroup": "projectReaders"
     },
     {
      "role": "WRITER",
      "specialGroup": "projectWriters"
     },
     {
      "role": "OWNER",
      "specialGroup": "projectOwners"
     },
     {
      "role": "READER",
      "specialGroup": "allAuthenticatedUsers"
     },
     {
      "role": "READER",
      "domain": "domain_name"
     },
     {
      "role": "WRITER",
      "userByEmail": "user_email"
     },
     {
      "role": "READER",
      "groupByEmail": "group_email"
     }
    ],
    ...
   }
   ```
4. 完成編輯後，請使用 `bq update` 指令並利用 `--source` 旗標來納入 JSON 檔案。如果資料集位於預設專案以外的專案中，請使用下列格式將專案 ID 新增至資料集名稱：`PROJECT_ID:DATASET`。

   **注意：**如果您套用了含有存取權控管設定的 JSON 檔案，現有的存取權控管設定會遭到覆寫。

   ```
     bq update   

     --source PATH_TO_FILE   

     PROJECT_ID:DATASET
   ```
5. 如要驗證存取控管設定變更，請再次使用 `bq show` 指令，但不要將資訊寫入檔案：

   ```
   bq show --format=prettyjson PROJECT_ID:DATASET
   ```

### Terraform

使用 [`google_bigquery_dataset_iam`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_iam) 資源更新資料集的存取權。

**重要事項：** `google_bigquery_dataset_iam` 提供的不同資源可能會彼此衝突，也可能與
[google\_bigquery\_dataset\_access](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_access) 資源衝突。使用 Terraform 變更存取權控管設定前，請先詳閱[`google_bigquery_dataset_iam`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_iam)說明文件。

**設定資料集的存取權政策**

以下範例說明如何使用 [`google_bigquery_dataset_iam_policy` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_iam#google_bigquery_dataset_iam_policy)，為 `mydataset` 資料集設定 IAM 政策。這會取代已附加至資料集的現有政策：

```
# This file sets the IAM policy for the dataset created by
# https://github.com/terraform-google-modules/terraform-docs-samples/blob/main/bigquery/bigquery_create_dataset/main.tf.
# You must place it in the same local directory as that main.tf file,
# and you must have already applied that main.tf file to create
# the "default" dataset resource with a dataset_id of "mydataset".

data "google_iam_policy" "iam_policy" {
  binding {
    role = "roles/bigquery.admin"
    members = [
      "user:user@example.com",
    ]
  }
  binding {
    role = "roles/bigquery.dataOwner"
    members = [
      "group:data.admin@example.com",
    ]
  }
  binding {
    role = "roles/bigquery.dataEditor"
    members = [
      "serviceAccount:bqcx-1234567891011-12a3@gcp-sa-bigquery-condel.iam.gserviceaccount.com",
    ]
  }
}

resource "google_bigquery_dataset_iam_policy" "dataset_iam_policy" {
  dataset_id  = google_bigquery_dataset.default.dataset_id
  policy_data = data.google_iam_policy.iam_policy.policy_data
}
```

**設定資料集的角色成員資格**

以下範例說明如何使用[`google_bigquery_dataset_iam_binding`資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_iam#google_bigquery_dataset_iam_binding)，為`mydataset`資料集設定特定角色的成員資格。這會取代該角色現有的任何成員。
資料集 IAM 政策中的其他角色會保留：

```
# This file sets membership in an IAM role for the dataset created by
# https://github.com/terraform-google-modules/terraform-docs-samples/blob/main/bigquery/bigquery_create_dataset/main.tf.
# You must place it in the same local directory as that main.tf file,
# and you must have already applied that main.tf file to create
# the "default" dataset resource with a dataset_id of "mydataset".

resource "google_bigquery_dataset_iam_binding" "dataset_iam_binding" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  role       = "roles/bigquery.jobUser"

  members = [
    "user:user@example.com",
    "group:group@example.com"
  ]
}
```

**為單一主體設定角色成員資格**

以下範例說明如何使用 [`google_bigquery_dataset_iam_member` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_iam#google_bigquery_dataset_iam_member)更新 `mydataset` 資料集的 IAM 政策，將角色授予一個主體。更新這項 IAM 政策不會影響已獲資料集角色授權的其他主體存取權。

```
# This file adds a member to an IAM role for the dataset created by
# https://github.com/terraform-google-modules/terraform-docs-samples/blob/main/bigquery/bigquery_create_dataset/main.tf.
# You must place it in the same local directory as that main.tf file,
# and you must have already applied that main.tf file to create
# the "default" dataset resource with a dataset_id of "mydataset".

resource "google_bigquery_dataset_iam_member" "dataset_iam_member" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  role       = "roles/bigquery.user"
  member     = "user:user@example.com"
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

如要在建立資料集時套用存取權控管設定，請使用定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)呼叫 [`datasets.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw)。如要更新存取權控管設定，請呼叫 [`datasets.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw)，並使用 `Dataset` 資源中的 `access` 屬性。

由於 `datasets.update` 方法會取代整個資料集的資源，因此建議您使用 `datasets.patch` 方法來更新存取權控管設定。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

將新項目附加至現有清單，藉此設定新的存取清單 ([`DatasetMetadataToUpdate` 類型](https://pkg.go.dev/cloud.google.com/go/bigquery#DatasetMetadataToUpdate))。然後呼叫 [`dataset.Update()` 函式](https://pkg.go.dev/cloud.google.com/go/bigquery#Dataset.Update)來更新屬性。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
)

// grantAccessToDataset creates a new ACL conceding the READER role to the group "example-analyst-group@google.com"
// For more information on the types of ACLs available see:
// https://cloud.google.com/storage/docs/access-control/lists
func grantAccessToDataset(w io.Writer, projectID, datasetID string) error {
	// TODO(developer): uncomment and update the following lines:
	// projectID := "my-project-id"
	// datasetID := "mydataset"

	ctx := context.Background()

	// Create BigQuery handler.
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	// Create dataset handler
	dataset := client.Dataset(datasetID)

	// Get metadata
	meta, err := dataset.Metadata(ctx)
	if err != nil {
		return fmt.Errorf("bigquery.Dataset.Metadata: %w", err)
	}

	// Find more details about BigQuery Entity Types here:
	// https://pkg.go.dev/cloud.google.com/go/bigquery#EntityType
	//
	// Find more details about BigQuery Access Roles here:
	// https://pkg.go.dev/cloud.google.com/go/bigquery#AccessRole

	entityType := bigquery.GroupEmailEntity
	entityID := "example-analyst-group@google.com"
	roleType := bigquery.ReaderRole

	// Append a new access control entry to the existing access list.
	update := bigquery.DatasetMetadataToUpdate{
		Access: append(meta.Access, &bigquery.AccessEntry{
			Role:       roleType,
			EntityType: entityType,
			Entity:     entityID,
		}),
	}

	// Leverage the ETag for the update to assert there's been no modifications to the
	// dataset since the metadata was originally read.
	meta, err = dataset.Update(ctx, update, meta.ETag)
	if err != nil {
		return err
	}

	fmt.Fprintf(w, "Details for Access entries in dataset %v.\n", datasetID)
	for _, access := range meta.Access {
		fmt.Fprintln(w)
		fmt.Fprintf(w, "Role: %s\n", access.Role)
		fmt.Fprintf(w, "Entities: %v\n", access.Entity)
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
import com.google.cloud.bigquery.Acl.Role;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import com.google.cloud.bigquery.DatasetId;
import java.util.ArrayList;
import java.util.List;

public class GrantAccessToDataset {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    // Project and dataset from which to get the access policy
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    // Group to add to the ACL
    String entityEmail = "group-to-add@example.com";

    grantAccessToDataset(projectId, datasetName, entityEmail);
  }

  public static void grantAccessToDataset(
      String projectId, String datasetName, String entityEmail) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Create datasetId with the projectId and the datasetName.
      DatasetId datasetId = DatasetId.of(projectId, datasetName);
      Dataset dataset = bigquery.getDataset(datasetId);

      // Create a new Entity with the corresponding type and email
      // "user-or-group-to-add@example.com"
      // For more information on the types of Entities available see:
      // https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Acl.Entity
      // and
      // https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Acl.Entity.Type
      Entity entity = new Group(entityEmail);

      // Create a new ACL granting the READER role to the group with the entity email
      // "user-or-group-to-add@example.com"
      // For more information on the types of ACLs available see:
      // https://cloud.google.com/storage/docs/access-control/lists
      Acl newEntry = Acl.of(entity, Role.READER);

      // Get a copy of the ACLs list from the dataset and append the new entry.
      List<Acl> acls = new ArrayList<>(dataset.getAcl());
      acls.add(newEntry);

      // Update the ACLs by setting the new list.
      Dataset updatedDataset = bigquery.update(dataset.toBuilder().setAcl(acls).build());
      System.out.println(
          "ACLs of dataset \""
              + updatedDataset.getDatasetId().getDataset()
              + "\" updated successfully");
    } catch (BigQueryException e) {
      System.out.println("ACLs were not updated \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 [Dataset#metadata](https://googleapis.dev/nodejs/bigquery/latest/Dataset.html#metadata) 方法，將新項目附加至現有清單，藉此設定新的存取清單。然後呼叫 [Dataset#setMetadata()](https://googleapis.dev/nodejs/bigquery/latest/Dataset.html#setMetadata) 函式來更新屬性。

```
/**
 * TODO(developer): Update and un-comment below lines.
 */

// const datasetId = "my_project_id.my_dataset_name";

// ID of the user or group from whom you are adding access.
// const entityId = "user-or-group-to-add@example.com";

// One of the "Basic roles for datasets" described here:
// https://cloud.google.com/bigquery/docs/access-control-basic-roles#dataset-basic-roles
// const role = "READER";

const {BigQuery} = require('@google-cloud/bigquery');

// Instantiate a client.
const client = new BigQuery();

// Type of entity you are granting access to.
// Find allowed allowed entity type names here:
// https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets#resource:-dataset
const entityType = 'groupByEmail';

async function grantAccessToDataset() {
  const [dataset] = await client.dataset(datasetId).get();

  // The 'access entries' array is immutable. Create a copy for modifications.
  const entries = [...dataset.metadata.access];

  // Append an AccessEntry to grant the role to a dataset.
  // Find more details about the AccessEntry object in the BigQuery documentation:
  // https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.AccessEntry
  entries.push({
    role,
    [entityType]: entityId,
  });

  // Assign the array of AccessEntries back to the dataset.
  const metadata = {
    access: entries,
  };

  // Update will only succeed if the dataset
  // has not been modified externally since retrieval.
  //
  // See the BigQuery client library documentation for more details on metadata updates:
  // https://cloud.google.com/nodejs/docs/reference/bigquery/latest

  // Update just the 'access entries' property of the dataset.
  await client.dataset(datasetId).setMetadata(metadata);

  console.log(
    `Role '${role}' granted for entity '${entityId}' in '${datasetId}'.`
  );
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

利用資料集的存取權控管設定 [`dataset.access_entries` 屬性](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.Dataset?hl=zh-tw#google_cloud_bigquery_dataset_Dataset_access_entries)。然後呼叫 [`client.update_dataset()` 函式](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_update_dataset)來更新屬性。

```
from google.api_core.exceptions import PreconditionFailed
from google.cloud import bigquery
from google.cloud.bigquery.enums import EntityTypes

# TODO(developer): Update and uncomment the lines below.

# ID of the dataset to grant access to.
# dataset_id = "my_project_id.my_dataset"

# ID of the user or group receiving access to the dataset.
# Alternatively, the JSON REST API representation of the entity,
# such as the view's table reference.
# entity_id = "user-or-group-to-add@example.com"

# One of the "Basic roles for datasets" described here:
# https://cloud.google.com/bigquery/docs/access-control-basic-roles#dataset-basic-roles
# role = "READER"

# Type of entity you are granting access to.
# Find allowed allowed entity type names here:
# https://cloud.google.com/python/docs/reference/bigquery/latest/enums#class-googlecloudbigqueryenumsentitytypesvalue
entity_type = EntityTypes.GROUP_BY_EMAIL

# Instantiate a client.
client = bigquery.Client()

# Get a reference to the dataset.
dataset = client.get_dataset(dataset_id)

# The `access_entries` list is immutable. Create a copy for modifications.
entries = list(dataset.access_entries)

# Append an AccessEntry to grant the role to a dataset.
# Find more details about the AccessEntry object here:
# https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.AccessEntry
entries.append(
    bigquery.AccessEntry(
        role=role,
        entity_type=entity_type,
        entity_id=entity_id,
    )
)

# Assign the list of AccessEntries back to the dataset.
dataset.access_entries = entries

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

    # Show a success message.
    full_dataset_id = f"{dataset.project}.{dataset.dataset_id}"
    print(
        f"Role '{role}' granted for entity '{entity_id}'"
        f" in dataset '{full_dataset_id}'."
    )
except PreconditionFailed:  # A read-modify-write error
    print(
        f"Dataset '{dataset.dataset_id}' was modified remotely before this update. "
        "Fetch the latest version and retry."
    )
```

### 授予資料集存取權的預先定義角色

您可以授予下列 IAM 預先定義的角色資料集存取權。

**注意：** 雖然可以授予資料集的 BigQuery 管理員或 BigQuery Studio 管理員權限，但請勿在資料集層級授予這些角色。BigQuery 資料擁有者也會授予資料集的所有權限，且權限較低。BigQuery 管理員和 BigQuery Studio 管理員通常是在專案層級授予。

| 角色 | 說明 |
| --- | --- |
| [BigQuery 資料擁有者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner) (`roles/bigquery.dataOwner`) | 如果授予資料集，這個角色會提供下列權限：   * 資料集和資料集內所有資源 (資料表、檢視表、模型和常式) 的所有權限。  **注意：**在專案層級獲派「資料擁有者」角色的主體，也可以建立新資料集，並列出他們有權存取的專案資料集。 |
| [BigQuery 資料編輯者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor) (`roles/bigquery.dataEditor`) | 如果授予資料集，這個角色會提供下列權限：   * 取得資料集的中繼資料和權限。 * 資料表和檢視畫面：  + 建立、更新、取得、列出及刪除資料集的資料表和檢視區塊。 + 讀取 (查詢)、匯出、複製及更新資料表資料。 + 建立、更新及刪除索引。 + 建立及還原快照。  * 具備資料集常式和模型的所有權限。  **注意：**在專案層級獲派資料編輯者角色的主體，也可以在有權存取的專案中建立新資料集，並列出資料集。 |
| [BigQuery 資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer) (`roles/bigquery.dataViewer`) | 如果授予資料集，這個角色會提供下列權限：   * 取得資料集的中繼資料和權限。 * 列出資料集的資料表、檢視區塊和模型。 * 取得資料集資料表和檢視區塊的中繼資料和存取權控管。 * 讀取 (查詢)、複製及匯出資料表資料，並建立快照。 * 列出及叫用資料集的處理常式。 |
| [BigQuery 中繼資料檢視器](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.metadataViewer) (`roles/bigquery.metadataViewer`) | 如果授予資料集，這個角色會提供下列權限：   * 取得資料集的中繼資料和存取權控制。 * 取得資料表和檢視區塊的中繼資料和存取權控制。 * 從資料集的模型和常式取得中繼資料。 * 列出資料集中的資料表、檢視區塊、模型和常式。 |

### 資料集權限

開頭為 `bigquery.datasets` 的權限大多適用於資料集層級。
`bigquery.datasets.create` 不會。如要建立資料集，必須將 `bigquery.datasets.create` 權限授予父項容器 (專案) 的角色。

下表列出資料集的所有權限，以及可套用權限的最低層級資源。

| 權限 | 資源 | 動作 |
| --- | --- | --- |
| `bigquery.datasets.create` | 專案 | 在專案中建立新資料集。 |
| `bigquery.datasets.get` | 資料集 | 取得資料集的中繼資料和存取權控制。如要在控制台中查看權限，也必須具備 `bigquery.datasets.getIamPolicy` 權限。 |
| `bigquery.datasets.getIamPolicy` | 資料集 | 控制台必須具備這項權限，才能授予使用者權限，取得資料集的存取控制項。失敗時維持開放狀態。此外，控制台也需要 `bigquery.datasets.get` 權限才能查看資料集。 |
| `bigquery.datasets.update` | 資料集 | 更新資料集的中繼資料和存取權控管設定。在控制台中更新存取權控管時，也需要 `bigquery.datasets.setIamPolicy` 權限。 |
| `bigquery.datasets.setIamPolicy` | 資料集 | 控制台需要這項權限，才能授予使用者設定資料集存取控管的權限。失敗時維持開放狀態。控制台也需要 `bigquery.datasets.update` 權限才能更新資料集。 |
| `bigquery.datasets.delete` | 資料集 | 刪除資料集。 |
| `bigquery.datasets.createTagBinding` | 資料集 | 將標記附加至資料集。 |
| `bigquery.datasets.deleteTagBinding` | 資料集 | 從資料集卸離標記。 |
| `bigquery.datasets.listTagBindings` | 資料集 | 列出資料集的標記。 |
| `bigquery.datasets.listEffectiveTags` | 資料集 | 列出資料集的有效標記 (已套用和已沿用)。 |
| `bigquery.datasets.link` | 資料集 | 建立 [連結的資料集](https://docs.cloud.google.com/logging/docs/analyze/query-linked-dataset?hl=zh-tw)。 |
| `bigquery.datasets.listSharedDatasetUsage` | 專案 | 列出您在專案中可存取資料集的共用資料集使用統計資料。您必須要有這個權限，才能查詢 `INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面。 |

### 查看資料集的存取權控制

您可以選擇下列任一選項，查看資料集的明確設定存取權控管。如要[查看繼承的角色](#inherited-roles)，請使用 BigQuery 網頁版 UI 存取資料集。

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 依序點選 person\_add「共用」**>「權限」**。

   資料集的存取權控管會顯示在「資料集權限」窗格中。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 如要取得現有政策並以 JSON 格式輸出至本機檔案，請在 Cloud Shell 中使用 [`bq show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show)：

   ```
   bq show \
      --format=prettyjson \
      PROJECT_ID:DATASET > PATH_TO_FILE
   ```

   更改下列內容：

   * PROJECT\_ID：專案 ID
   * DATASET：資料集名稱
   * PATH\_TO\_FILE：本機上 JSON 檔案的路徑

### SQL

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

查詢 [`INFORMATION_SCHEMA.OBJECT_PRIVILEGES` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-object-privileges?hl=zh-tw)。
如要查詢資料集的存取權控管，必須指定 `object_name`。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
   COLUMN_LIST
   FROM
     PROJECT_ID.`region-REGION`.INFORMATION_SCHEMA.OBJECT_PRIVILEGES
   WHERE
   object_name = "DATASET";
   ```

   請替換下列項目：

   * COLUMN\_LIST：以半形逗號分隔的清單，列出[`INFORMATION_SCHEMA.OBJECT_PRIVILEGES` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-object-privileges?hl=zh-tw)中的資料欄
   * PROJECT\_ID：專案 ID
   * REGION：[區域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)
   * DATASET：換成您專案中資料集的名稱
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

範例：

這項查詢會取得 `mydataset` 的存取權控管。

```
SELECT
object_name, privilege_type, grantee
FROM
my_project.`region-us`.INFORMATION_SCHEMA.OBJECT_PRIVILEGES
WHERE
object_name = "mydataset";
```

輸出內容應如下所示：

```
+------------------+-----------------------------+-------------------------+
|   object_name    |  privilege_type             | grantee                 |
+------------------+-----------------------------+-------------------------+
| mydataset        | roles/bigquery.dataOwner    | projectOwner:myproject  |
| mydataset        | roles/bigquery.dataViwer    | user:user@example.com   |
+------------------+-----------------------------+-------------------------+
```

### API

如要查看資料集的存取權控管設定，請呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法，搭配已定義的[`dataset` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)。

存取權控管會顯示在 `dataset` 資源的 `access` 屬性中。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

呼叫 [`client.Dataset().Metadata()` 函式](https://pkg.go.dev/cloud.google.com/go/bigquery#Dataset.Metadata)。存取權政策位於 [`Access`](https://pkg.go.dev/cloud.google.com/go/bigquery@v1.66.0#DatasetMetadata.Access) 屬性中。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
)

// viewDatasetAccessPolicies retrieves the ACL for the given dataset
// For more information on the types of ACLs available see:
// https://cloud.google.com/storage/docs/access-control/lists
func viewDatasetAccessPolicies(w io.Writer, projectID, datasetID string) error {
	// TODO(developer): uncomment and update the following lines:
	// projectID := "my-project-id"
	// datasetID := "mydataset"

	ctx := context.Background()

	// Create new client.
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	// Get dataset's metadata.
	meta, err := client.Dataset(datasetID).Metadata(ctx)
	if err != nil {
		return fmt.Errorf("bigquery.Client.Dataset.Metadata: %w", err)
	}

	fmt.Fprintf(w, "Details for Access entries in dataset %v.\n", datasetID)

	// Iterate over access permissions.
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
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import com.google.cloud.bigquery.DatasetId;
import java.util.List;

public class GetDatasetAccessPolicy {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    // Project and dataset from which to get the access policy.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    getDatasetAccessPolicy(projectId, datasetName);
  }

  public static void getDatasetAccessPolicy(String projectId, String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Create datasetId with the projectId and the datasetName.
      DatasetId datasetId = DatasetId.of(projectId, datasetName);
      Dataset dataset = bigquery.getDataset(datasetId);

      // Show ACL details.
      // Find more information about ACL and the Acl Class here:
      // https://cloud.google.com/storage/docs/access-control/lists
      // https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Acl
      List<Acl> acls = dataset.getAcl();
      System.out.println("ACLs in dataset \"" + dataset.getDatasetId().getDataset() + "\":");
      System.out.println(acls.toString());
      for (Acl acl : acls) {
        System.out.println();
        System.out.println("Role: " + acl.getRole());
        System.out.println("Entity: " + acl.getEntity());
      }
    } catch (BigQueryException e) {
      System.out.println("ACLs info not retrieved. \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 [`Dataset#getMetadata()` 函式擷取資料集中繼資料](https://googleapis.dev/nodejs/bigquery/latest/Dataset.html#getMetadata)。
存取權政策位於產生的中繼資料物件的存取權屬性中。

```
/**
 * TODO(developer): Update and un-comment below lines
 */
// const datasetId = "my_project_id.my_dataset";

const {BigQuery} = require('@google-cloud/bigquery');

// Instantiate a client.
const bigquery = new BigQuery();

async function viewDatasetAccessPolicy() {
  const dataset = bigquery.dataset(datasetId);

  const [metadata] = await dataset.getMetadata();
  const accessEntries = metadata.access || [];

  // Show the list of AccessEntry objects.
  // More details about the AccessEntry object in the BigQuery documentation:
  // https://cloud.google.com/nodejs/docs/reference/bigquery/latest
  console.log(
    `${accessEntries.length} Access entries in dataset '${datasetId}':`
  );
  for (const accessEntry of accessEntries) {
    console.log(`Role: ${accessEntry.role || 'null'}`);
    console.log(`Special group: ${accessEntry.specialGroup || 'null'}`);
    console.log(`User by Email: ${accessEntry.userByEmail || 'null'}`);
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

呼叫 [`client.get_dataset()` 函式](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_get_dataset)。存取政策位於 [`dataset.access_entries` 屬性](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.Dataset?hl=zh-tw#google_cloud_bigquery_dataset_Dataset_access_entries)。

```
from google.cloud import bigquery

# Instantiate a client.
client = bigquery.Client()

# TODO(developer): Update and uncomment the lines below.

# Dataset from which to get the access policy.
# dataset_id = "my_dataset"

# Get a reference to the dataset.
dataset = client.get_dataset(dataset_id)

# Show the list of AccessEntry objects.
# More details about the AccessEntry object here:
# https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.AccessEntry
print(
    f"{len(dataset.access_entries)} Access entries found "
    f"in dataset '{dataset_id}':"
)

for access_entry in dataset.access_entries:
    print()
    print(f"Role: {access_entry.role}")
    print(f"Special group: {access_entry.special_group}")
    print(f"User by Email: {access_entry.user_by_email}")
```

### 撤銷資料集存取權

如要撤銷資料集的存取權，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在詳細資料面板中，依序點選「共用」**>「權限」**。
5. 在「資料集權限」對話方塊中，展開要撤銷存取權的主體。
6. 按一下 delete「移除主體」。
7. 在「要移除主體的角色嗎？」對話方塊中，按一下「移除」。
8. 如要返回資料集詳細資料，請按一下「關閉」。

**注意：** 如果無法撤銷資料集的存取權，主體可能是從[資源階層](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw#resource-hierarchy)中較高的層級[繼承存取權](#inherited-roles)。

### SQL

如要移除主體的資料集存取權，請使用 [`REVOKE` DCL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw#revoke_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   REVOKE `ROLE_LIST`
   ON SCHEMA RESOURCE_NAME
   FROM "USER_LIST"
   ```

   請替換下列項目：

   * `ROLE_LIST`：要撤銷的角色或以半形逗號分隔的角色清單
   * `RESOURCE_NAME`：要撤銷權限的資源名稱
   * `USER_LIST`：以逗號分隔的使用者清單，這些使用者的角色將遭到撤銷

     如需有效格式的清單，請參閱 [`user_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw#user_list)。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

以下範例會撤銷 `myDataset` 的 BigQuery 資料擁有者角色：

```
REVOKE `roles/bigquery.dataOwner`
ON SCHEMA `myProject`.myDataset
FROM "group:group@example.com", "serviceAccount:user@test-project.iam.gserviceaccount.com"
```

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 如要將現有資料集的資訊 (包括存取權控管設定) 寫入 JSON 檔案，請使用 [`bq show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show)：

   ```
   bq show \
       --format=prettyjson \
       PROJECT_ID:DATASET > PATH_TO_FILE
   ```

   更改下列內容：

   * PROJECT\_ID：專案 ID
   * DATASET：資料集名稱
   * PATH\_TO\_FILE：本機上 JSON 檔案的路徑
3. 變更 JSON 檔案的 `access` 區段。您可以移除任何 `specialGroup` 項目：`projectOwners`、`projectWriters`、`projectReaders` 和 `allAuthenticatedUsers`。您也可以移除下列任何項目：`userByEmail`、`groupByEmail` 和 `domain`。

   舉例來說，資料集 JSON 檔案中的 `access` 區段應會與以下內容類似：

   ```
   {
    "access": [
     {
      "role": "READER",
      "specialGroup": "projectReaders"
     },
     {
      "role": "WRITER",
      "specialGroup": "projectWriters"
     },
     {
      "role": "OWNER",
      "specialGroup": "projectOwners"
     },
     {
      "role": "READER",
      "specialGroup": "allAuthenticatedUsers"
     },
     {
      "role": "READER",
      "domain": "domain_name"
     },
     {
      "role": "WRITER",
      "userByEmail": "user_email"
     },
     {
      "role": "READER",
      "groupByEmail": "group_email"
     }
    ],
    ...
   }
   ```
4. 完成編輯後，請使用 `bq update` 指令並利用 `--source` 旗標來納入 JSON 檔案。如果資料集位於預設專案以外的專案中，請使用下列格式將專案 ID 新增至資料集名稱：`PROJECT_ID:DATASET`。

   **注意：**如果您套用了含有存取權控管設定的 JSON 檔案，現有的存取權控管設定會遭到覆寫。

   ```
     bq update   

         --source PATH_TO_FILE   

         PROJECT_ID:DATASET
   ```
5. 如要驗證存取控管變更，請使用 `show` 指令，但不要將資訊寫入檔案：

   ```
   bq show --format=prettyjson PROJECT_ID:DATASET
   ```

### API

呼叫 [`datasets.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw)，並使用 `Dataset` 資源中的 `access` 屬性更新存取權控管設定。

由於 `datasets.update` 方法會取代整個資料集的資源，因此建議您使用 `datasets.patch` 方法來更新存取權控管設定。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

從現有清單中移除項目，藉此設定新的存取清單 (使用 [`DatasetMetadataToUpdate` 類型](https://pkg.go.dev/cloud.google.com/go/bigquery#DatasetMetadataToUpdate))。然後呼叫 [`dataset.Update()` 函式](https://pkg.go.dev/cloud.google.com/go/bigquery#Dataset.Update)來更新屬性。

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

使用 [`Dataset#get()`](https://googleapis.dev/nodejs/bigquery/latest/Dataset.html#get) 方法擷取目前的中繼資料，然後從現有清單中移除指定項目，即可更新資料集存取清單。修改存取權屬性，排除所需實體，然後呼叫 [`Dataset#setMetadata()`](https://googleapis.dev/nodejs/bigquery/latest/Dataset.html#setMetadata) 函式，套用更新後的存取清單。

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

利用資料集的存取權控管設定 [`dataset.access_entries` 屬性](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.Dataset?hl=zh-tw#google_cloud_bigquery_dataset_Dataset_access_entries)。然後呼叫 [`client.update_dataset()` 函式](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_update_dataset)來更新屬性。

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

## 使用資料表和檢視權限控管

BigQuery 會將檢視表視為資料表資源。您可以授予 [IAM 主體](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw#allow)預先定義或自訂的角色，藉此提供資料表或檢視區塊的存取權，並決定主體可對資料表或檢視區塊執行的操作。這也稱為將「允許政策」附加至資源。授予存取權後，您可以查看資料表或檢視表的存取權控管機制，也可以撤銷資料表或檢視表的存取權。

### 授予資料表或檢視表的存取權

如要進行精細的存取控管，您可以對特定資料表或檢視區塊授予預先定義或自訂的 IAM 角色。資料表或檢視區塊也會沿用在資料集層級和更高層級指定的存取權控管。舉例來說，如果您將資料集的 BigQuery 資料擁有者角色授予主體，該主體也會取得資料集中資料表和檢視區塊的 BigQuery 資料擁有者權限。

如要授予資料表或檢視區塊的存取權，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 依序點選「總覽」**>「表格」**，然後點選表格或檢視畫面。
5. 依序點選「共用」person\_add**>「管理權限」**。
6. 按一下「新增主體」person\_add。
7. 在「New principals」(新增主體) 欄位中輸入主體。
8. 在「Select a role」(選取角色) 清單中，選取預先定義的角色或自訂角色。
9. 按一下 [儲存]。
10. 如要返回表格或查看詳細資料，請按一下「關閉」。

### SQL

如要授予主體資料表或檢視表的存取權，請使用 [`GRANT` DCL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw#grant_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   GRANT `ROLE_LIST`
   ON RESOURCE_TYPE RESOURCE_NAME
   TO "USER_LIST"
   ```

   請替換下列項目：

   * `ROLE_LIST`：要授予的角色或以半形逗號分隔的角色清單
   * `RESOURCE_TYPE`：角色適用的資源類型

     支援的值包括 `TABLE`、`VIEW`、`MATERIALIZED
     VIEW` 和 `EXTERNAL TABLE`。
   * `RESOURCE_NAME`：要授予權限的資源名稱
   * `USER_LIST`：以逗號分隔的使用者清單，這些使用者會獲得角色授權

     如需有效格式的清單，請參閱 [`user_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw#user_list)。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

以下範例會授予 `myTable` 的 BigQuery 資料檢視者角色：

```
GRANT `roles/bigquery.dataViewer`
ON TABLE `myProject`.myDataset.myTable
TO "user:user@example.com", "user:user2@example.com"
```

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 如要授予資料表或檢視表的存取權，請使用 [`bq add-iam-policy-binding` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_add-iam-policy-binding)：

   ```
   bq add-iam-policy-binding --member=MEMBER_TYPE:MEMBER --role=ROLE
     --table=true RESOURCE
   ```

   更改下列內容：

   * MEMBER\_TYPE：成員類型，例如 `user`、`group`、`serviceAccount` 或 `domain`。
   * MEMBER：成員的電子郵件地址或網域名稱。
   * ROLE：要授予成員的角色。
   * RESOURCE：要更新政策的資料表或檢視區塊名稱。

### Terraform

使用 [`google_bigquery_table_iam`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table_iam) 資源更新資料表的存取權。

**重要事項：** `google_bigquery_table_iam` 提供的不同資源可能會互相衝突。建議您先詳閱
[`google_bigquery_table_iam`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table_iam)
說明文件，再使用 Terraform 變更存取控管設定。

**設定資料表的存取權政策**

以下範例說明如何使用 [`google_bigquery_table_iam_policy` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table_iam#google_bigquery_table_iam_policy)，為 `mytable` 資料表設定 IAM 政策。這會取代已附加至資料表的任何現有政策：

```
# This file sets the IAM policy for the table created by
# https://github.com/terraform-google-modules/terraform-docs-samples/blob/main/bigquery/bigquery_create_table/main.tf.
# You must place it in the same local directory as that main.tf file,
# and you must have already applied that main.tf file to create
# the "default" table resource with a table_id of "mytable".

data "google_iam_policy" "iam_policy" {
  binding {
    role = "roles/bigquery.dataOwner"
    members = [
      "user:user@example.com",
    ]
  }
}

resource "google_bigquery_table_iam_policy" "table_iam_policy" {
  dataset_id  = google_bigquery_table.default.dataset_id
  table_id    = google_bigquery_table.default.table_id
  policy_data = data.google_iam_policy.iam_policy.policy_data
}
```

**設定表格的角色成員資格**

以下範例說明如何使用 [`google_bigquery_table_iam_binding` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table_iam#google_bigquery_table_iam_binding)，為 `mytable` 資料表設定特定角色的成員資格。這會取代該角色現有的任何成員。
系統會保留資料表 IAM 政策中的其他角色。

```
# This file sets membership in an IAM role for the table created by
# https://github.com/terraform-google-modules/terraform-docs-samples/blob/main/bigquery/bigquery_create_table/main.tf.
# You must place it in the same local directory as that main.tf file,
# and you must have already applied that main.tf file to create
# the "default" table resource with a table_id of "mytable".

resource "google_bigquery_table_iam_binding" "table_iam_binding" {
  dataset_id = google_bigquery_table.default.dataset_id
  table_id   = google_bigquery_table.default.table_id
  role       = "roles/bigquery.dataOwner"

  members = [
    "group:group@example.com",
  ]
}
```

**為單一主體設定角色成員資格**

以下範例說明如何使用 [`google_bigquery_table_iam_member` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table_iam#google_bigquery_table_iam_member)，更新 `mytable` 資料表的 IAM 政策，將角色授予一個主體。更新這項 IAM 政策不會影響已獲資料集角色授權的其他主體存取權。

```
# This file adds a member to an IAM role for the table created by
# https://github.com/terraform-google-modules/terraform-docs-samples/blob/main/bigquery/bigquery_create_table/main.tf.
# You must place it in the same local directory as that main.tf file,
# and you must have already applied that main.tf file to create
# the "default" table resource with a table_id of "mytable".

resource "google_bigquery_table_iam_member" "table_iam_member" {
  dataset_id = google_bigquery_table.default.dataset_id
  table_id   = google_bigquery_table.default.table_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:bqcx-1234567891011-12a3@gcp-sa-bigquery-condel.iam.gserviceaccount.com"
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息