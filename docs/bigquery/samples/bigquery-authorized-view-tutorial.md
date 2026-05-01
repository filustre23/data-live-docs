* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 建立授權檢視表 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用 GitHub 公開資料建立授權 view。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [授權 view](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)
* [建立授權檢視](https://docs.cloud.google.com/bigquery/docs/create-authorized-views?hl=zh-tw)

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Create a source dataset to store your table.
final Dataset sourceDataset = bigquery.create(DatasetInfo.of(sourceDatasetId));
// Populate a source table
String tableQuery =
    "SELECT commit, author, committer, repo_name"
        + " FROM `bigquery-public-data.github_repos.commits`"
        + " LIMIT 1000";
QueryJobConfiguration queryConfig =
    QueryJobConfiguration.newBuilder(tableQuery)
        .setDestinationTable(TableId.of(sourceDatasetId, sourceTableId))
        .build();
bigquery.query(queryConfig);
// Create a separate dataset to store your view
Dataset sharedDataset = bigquery.create(DatasetInfo.of(sharedDatasetId));
// Create the view in the new dataset
String viewQuery =
    String.format(
        "SELECT commit, author.name as author, "
            + "committer.name as committer, repo_name FROM %s.%s.%s",
        projectId, sourceDatasetId, sourceTableId);
ViewDefinition viewDefinition = ViewDefinition.of(viewQuery);
Table view =
    bigquery.create(TableInfo.of(TableId.of(sharedDatasetId, sharedViewId), viewDefinition));
// Assign access controls to the dataset containing the view
List<Acl> viewAcl = new ArrayList<>(sharedDataset.getAcl());
viewAcl.add(Acl.of(new Acl.Group("example-analyst-group@google.com"), Acl.Role.READER));
sharedDataset.toBuilder().setAcl(viewAcl).build().update();
// Authorize the view to access the source dataset
List<Acl> srcAcl = new ArrayList<>(sourceDataset.getAcl());
srcAcl.add(Acl.of(new Acl.View(view.getTableId())));
sourceDataset.toBuilder().setAcl(srcAcl).build().update();
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
async function authorizedViewTutorial() {
  const {BigQuery} = require('@google-cloud/bigquery');
  const bigquery = new BigQuery();

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const projectId = "my_project_id";
  // const sourceDatasetId = "my_source_dataset";
  // const sourceTableId = "my_source_table";
  // const sharedDatasetId = "shared_views";
  // const sharedViewId = "my_view";

  // Make API request to create dataset
  const [sourceDataset] = await bigquery.createDataset(sourceDatasetId);
  console.log(`Source dataset ${sourceDataset.id} created.`);

  const destinationTable = sourceDataset.table(sourceTableId);

  const query = `SELECT commit, author, committer, repo_name
    FROM \`bigquery-public-data.github_repos.commits\`
    LIMIT 1000`;

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
  const options = {
    query: query,
    destination: destinationTable,
  };

  // Make API request to populate a source table
  await bigquery.query(options);
  // Create a separate dataset to store your view

  // Make API request to create a new dataset
  const [sharedDataset] = await bigquery.createDataset(sharedDatasetId);

  console.log(`Dataset ${sharedDataset.id} created.`);
  // Create the view in the new dataset

  const viewQuery = `SELECT
  commit, author.name as author,
  committer.name as committer, repo_name
  FROM
  \`${projectId}.${sourceDatasetId}.${sourceTableId}\``;

  const viewOptions = {
    view: {query: viewQuery, useLegacySql: false},
  };

  // Make API request to create the view
  const [view] = await sharedDataset.createTable(sharedViewId, viewOptions);

  const viewId = view.metadata.id;
  console.log(`View ${viewId} created.`);
  // Assign access controls to the dataset containing the view

  // Note to user: This is a group email for testing purposes. Replace with
  // your own group email address when running this code.
  const analyst_group_email = 'example-analyst-group@google.com';

  const analystAccessEntry = {
    role: 'READER',
    groupByEmail: analyst_group_email,
  };

  // Make API request to retrieve dataset metadata
  const [sharedMetadata] = await sharedDataset.getMetadata();

  const sharedAccessEntries = sharedMetadata.access;
  sharedAccessEntries.push(analystAccessEntry);

  sharedMetadata.access = sharedAccessEntries;

  // Make API request to update dataset metadata
  const [updatedSharedMetadata] =
    await sharedDataset.setMetadata(sharedMetadata);

  console.log(`Dataset ${updatedSharedMetadata.id} updated.`);
  // Authorize the view to access the source dataset

  const viewReference = {
    projectId: projectId,
    datasetId: sharedDatasetId,
    tableId: sharedViewId,
  };

  const datasetAccessEntry = {view: viewReference};

  // Make API request to retrieve source dataset metadata
  const [sourceMetadata] = await sourceDataset.getMetadata();

  const sourceAccessEntries = sourceMetadata.access;
  sourceAccessEntries.push(datasetAccessEntry);

  sourceMetadata.access = sourceAccessEntries;

  // Make API request to update source dataset metadata
  const [updatedSourceMetadata] =
    await sourceDataset.setMetadata(sourceMetadata);

  console.log(`Dataset ${updatedSourceMetadata.id} updated.`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# Create a source dataset
from google.cloud import bigquery
from google.cloud.bigquery.enums import EntityTypes

client = bigquery.Client()
source_dataset_id = "github_source_data"
source_dataset_id_full = "{}.{}".format(client.project, source_dataset_id)


source_dataset = bigquery.Dataset(source_dataset_id_full)
# Specify the geographic location where the dataset should reside.
source_dataset.location = "US"
source_dataset = client.create_dataset(source_dataset)  # API request

# Populate a source table
source_table_id = "github_contributors"
job_config = bigquery.QueryJobConfig()
job_config.destination = source_dataset.table(source_table_id)
sql = """
    SELECT commit, author, committer, repo_name
    FROM `bigquery-public-data.github_repos.commits`
    LIMIT 1000
"""
client.query_and_wait(
    sql,
    # Location must match that of the dataset(s) referenced in the query
    # and of the destination table.
    location="US",
    job_config=job_config,
)  # API request - starts the query and waits for query to finish

# Create a separate dataset to store your view
shared_dataset_id = "shared_views"
shared_dataset_id_full = "{}.{}".format(client.project, shared_dataset_id)


shared_dataset = bigquery.Dataset(shared_dataset_id_full)
shared_dataset.location = "US"
shared_dataset = client.create_dataset(shared_dataset)  # API request

# Create the view in the new dataset
shared_view_id = "github_analyst_view"
view = bigquery.Table(shared_dataset.table(shared_view_id))
sql_template = """
    SELECT
        commit, author.name as author,
        committer.name as committer, repo_name
    FROM
        `{}.{}.{}`
"""
view.view_query = sql_template.format(
    client.project, source_dataset_id, source_table_id
)
view = client.create_table(view)  # API request

# Assign access controls to the dataset containing the view
# analyst_group_email = 'data_analysts@example.com'
access_entries = shared_dataset.access_entries
access_entries.append(
    bigquery.AccessEntry("READER", EntityTypes.GROUP_BY_EMAIL, analyst_group_email)
)
shared_dataset.access_entries = access_entries
shared_dataset = client.update_dataset(
    shared_dataset, ["access_entries"]
)  # API request

# Authorize the view to access the source dataset
access_entries = source_dataset.access_entries
access_entries.append(
    bigquery.AccessEntry(None, EntityTypes.VIEW, view.reference.to_api_repr())
)
source_dataset.access_entries = access_entries
source_dataset = client.update_dataset(
    source_dataset, ["access_entries"]
)  # API request
```

### Terraform

如要瞭解如何套用或移除 Terraform 設定，請參閱「[基本 Terraform 指令](https://docs.cloud.google.com/docs/terraform/basic-commands?hl=zh-tw)」。詳情請參閱 [Terraform 供應商參考文件](https://registry.terraform.io/providers/hashicorp/google/latest/docs)。

```
# Creates an authorized view.

# Create a dataset to contain the view.
resource "google_bigquery_dataset" "view_dataset" {
  dataset_id  = "view_dataset"
  description = "Dataset that contains the view"
  location    = "us-west1"
}

# Create the view to authorize.
resource "google_bigquery_table" "movie_view" {
  project     = google_bigquery_dataset.view_dataset.project
  dataset_id  = google_bigquery_dataset.view_dataset.dataset_id
  table_id    = "movie_view"
  description = "View to authorize"

  view {
    query          = "SELECT item_id, avg(rating) FROM `movie_project.movie_dataset.movie_ratings` GROUP BY item_id ORDER BY item_id;"
    use_legacy_sql = false
  }
}


# Authorize the view to access the dataset
# that the query data originates from.
resource "google_bigquery_dataset_access" "view_authorization" {
  project    = "movie_project"
  dataset_id = "movie_dataset"

  view {
    project_id = google_bigquery_table.movie_view.project
    dataset_id = google_bigquery_table.movie_view.dataset_id
    table_id   = google_bigquery_table.movie_view.table_id
  }
}

# Specify the IAM policy for principals that can access
# the authorized view. These users should already
# have the roles/bigqueryUser role at the project level.
data "google_iam_policy" "principals_policy" {
  binding {
    role = "roles/bigquery.dataViewer"
    members = [
      "group:example-group@example.com",
    ]
  }
}

# Set the IAM policy on the authorized  view.
resource "google_bigquery_table_iam_policy" "authorized_view_policy" {
  project     = google_bigquery_table.movie_view.project
  dataset_id  = google_bigquery_table.movie_view.dataset_id
  table_id    = google_bigquery_table.movie_view.table_id
  policy_data = data.google_iam_policy.principals_policy.policy_data
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]