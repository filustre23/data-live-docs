Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 建立授權檢視表 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在本教學課程中，您會在 BigQuery 中建立授權檢視表，供資料分析師使用。[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)可讓您與特定使用者和群組分享查詢結果，無須授予他們基礎來源資料的存取權。檢視畫面會取得來源資料的存取權，而非使用者或群組。您也可以使用檢視表的 SQL 查詢，從查詢結果中排除資料欄和欄位。

除了使用已授權檢視表，您也可以在來源資料中設定資料欄層級的存取權控管，然後讓使用者存取查詢受控資料的檢視表。如要進一步瞭解資料欄層級存取權控管，請參閱「[資料欄層級存取控管機制簡介](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)」。

如果您有多個授權檢視表存取同一個來源資料集，可以[授權包含檢視表的資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)，不必授權個別檢視表。

## 目標

* 建立資料集，以便加入來源資料。
* 執行查詢，將資料載入來源資料集中的目的地資料表。
* 建立資料集，以便加入授權檢視表。
* 從 SQL 查詢建立授權檢視表，限制資料分析師可在查詢結果中查看的資料欄。
* 授予資料分析師執行查詢工作的權限。
* 授予資料分析師對內含已授權檢視表的資料集存取權。
* 將來源資料集的存取權授予已授權的檢視表。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

完成本文所述工作後，您可以刪除建立的資源，避免繼續計費，詳情請參閱「[清除所用資源](#clean-up)」。

## 事前準備

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)

1. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
2. 啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com&hl=zh-tw)
3. 請確認您具備[必要權限](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw#required_permissions)，可執行本文件中的工作。

## 建立資料集來儲存來源資料

您一開始可以建立儲存來源資料的資料集。

如要建立來源資料集，請選擇下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中，找到要建立資料集的專案，然後依序點選旁邊的 more\_vert「View actions」(查看動作)>「Create dataset」(建立資料集)。
4. 在「建立資料集」頁面中，執行下列操作：

   1. 在「Dataset ID」(資料集 ID) 中輸入 `github_source_data`。
   2. 確認「位置類型」已選取「多區域」。
   3. 如果是「多區域」，請選擇「美國」或「歐盟」。在本教學課程中建立的所有資源都應位於同一個多區域位置。
   4. 點選「建立資料集」。

### SQL

使用 [`CREATE SCHEMA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_schema_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE SCHEMA github_source_data;
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Create a source dataset to store your table.
Dataset sourceDataset = bigquery.create(DatasetInfo.of(sourceDatasetId));
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery
from google.cloud.bigquery.enums import EntityTypes

client = bigquery.Client()
source_dataset_id = "github_source_data"
source_dataset_id_full = "{}.{}".format(client.project, source_dataset_id)


source_dataset = bigquery.Dataset(source_dataset_id_full)
# Specify the geographic location where the dataset should reside.
source_dataset.location = "US"
source_dataset = client.create_dataset(source_dataset)  # API request
```

## 建立資料表並載入來源資料

建立來源資料集後，請將 SQL 查詢結果儲存至目的地資料表，藉此填入資料表。查詢會從 [GitHub 公開資料集](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=github_repos&%3Bpage=dataset&hl=zh-tw)擷取資料。

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列查詢：

   ```
   SELECT
     commit,
     author,
     committer,
     repo_name
   FROM
     `bigquery-public-data.github_repos.commits`
   LIMIT
     1000;
   ```
3. 按一下 [More] (更多) 並選取 [Query settings] (查詢設定)。
4. 在「Destination」(目的地) 部分，選取「Set a destination table for query results」(為查詢結果設定目的地資料表)。
5. 在「Dataset」(資料集) 中輸入 `PROJECT_ID.github_source_data`。

   將 `PROJECT_ID` 替換為專案 ID。
6. 在「Table Id」(資料表 ID) 中輸入 `github_contributors`。
7. 按一下 [儲存]。
8. 按一下「執行」。
9. 查詢完成後，在「Explorer」窗格中，依序點選「Datasets」(資料集) 和 **`github_source_data`** 資料集。
10. 依序點選「總覽」**>「資料表」**，然後點選 **`github_contributors`** 資料表。
11. 如要確認資料已寫入資料表，請按一下「預覽」分頁標籤。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
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
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
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
```

## 建立資料集來儲存授權檢視表

建立來源資料集之後，您會建立新的獨立資料集，儲存將與資料分析師分享的已授權檢視表。在後續步驟中，您會授權檢視表存取來源資料集中的資料。資料分析師可以存取授權 view，但無法直接存取來源資料。

授權檢視區塊應在與來源資料不同的資料集中建立。
這樣一來，資料擁有者就能授權使用者存取授權 view，不必同時授予基礎資料的存取權。來源資料集和授權 view 資料集必須位於同一個區域[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

如要建立儲存檢視表的資料集，請選擇下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，選取要建立資料集的專案。
4. 展開「查看動作」more\_vert選項，然後點選「建立資料集」。
5. 在「建立資料集」頁面中，執行下列操作：

   1. 在「Dataset ID」(資料集 ID) 中輸入 `shared_views`。
   2. 確認「位置類型」已選取「多區域」。
   3. 如果是「多區域」，請選擇「美國」或「歐盟」。在本教學課程中建立的所有資源都應位於同一個多區域位置。
   4. 點選「建立資料集」。

### SQL

使用 [`CREATE SCHEMA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_schema_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE SCHEMA shared_views;
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Create a separate dataset to store your view
Dataset sharedDataset = bigquery.create(DatasetInfo.of(sharedDatasetId));
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
shared_dataset_id = "shared_views"
shared_dataset_id_full = "{}.{}".format(client.project, shared_dataset_id)


shared_dataset = bigquery.Dataset(shared_dataset_id_full)
shared_dataset.location = "US"
shared_dataset = client.create_dataset(shared_dataset)  # API request
```

## 在新資料集中建立授權 view

您可在新資料集中建立您想要授權的視圖。這是您與資料分析師分享的視圖。這個檢視表是使用 SQL 查詢建立，可排除您不希望資料分析師看到的資料欄。

`github_contributors` 來源資料表包含兩個 [`RECORD`](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw#define_nested_and_repeated_columns) 類型的欄位：`author` 和 `committer`。在本教學課程中，您的授權 view 會排除所有作者資料 (作者姓名除外)，以及所有修訂者資料 (修訂者姓名除外)。

如要在新資料集中建立檢視表，請選擇下列任一選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列查詢。

   ```
   SELECT
   commit,
   author.name AS author,
   committer.name AS committer,
   repo_name
   FROM
   `PROJECT_ID.github_source_data.github_contributors`;
   ```

   將 `PROJECT_ID` 替換為專案 ID。
3. 依序點選「儲存」>「儲存檢視畫面」。
4. 在「Save view」(儲存檢視表) 對話方塊中，執行下列操作：

   1. 在「Project」(專案) 部分，確認已選取專案。
   2. 在「Dataset」(資料集) 中輸入 `shared_views`。
   3. 在「Table」(資料表) 中輸入 `github_analyst_view`。
   4. 按一下 [儲存]。

### SQL

使用 [`CREATE VIEW` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_view_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE VIEW shared_views.github_analyst_view
   AS (
     SELECT
       commit,
       author.name AS author,
       committer.name AS committer,
       repo_name
     FROM
       `PROJECT_ID.github_source_data.github_contributors`
   );
   ```

   將 `PROJECT_ID` 替換為您的專案 ID。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Create the view in the new dataset
String viewQuery =
    String.format(
        "SELECT commit, author.name as author, committer.name as committer, repo_name FROM %s.%s.%s",
        projectId, sourceDatasetId, sourceTableId);

ViewDefinition viewDefinition = ViewDefinition.of(viewQuery);

Table view =
    bigquery.create(TableInfo.of(TableId.of(sharedDatasetId, sharedViewId), viewDefinition));
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
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
```

## 授予資料分析師執行查詢工作的權限

資料分析師需要 `bigquery.jobs.create` 權限才能執行查詢工作，且必須獲得檢視表的存取權，才能查詢檢視表。在本節中，您會將 `bigquery.user` 角色授予資料分析師。`bigquery.user` 角色包含 `bigquery.jobs.create` 權限。在後續步驟中，您會授予資料分析師存取檢視表的權限。

如要將資料分析師群組指派給專案層級的 `bigquery.user` 角色，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「IAM」(身分與存取權管理) 頁面。

   [前往「IAM」(身分與存取權管理) 頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
2. 確認已在專案選取器中選取專案。
3. 按一下person\_add「授予存取權」。
4. 在「授予存取權」對話方塊中，執行下列操作：

   1. 在「New principals」(新增主體) 欄位中，輸入包含資料分析師的群組。例如：`data_analysts@example.com`。
   2. 在「請選擇角色」欄位中，搜尋並選取「BigQuery 使用者」角色。
   3. 按一下 [儲存]。

## 授予資料分析師查詢已授權檢視表的權限

如要讓資料分析師查詢檢視表，您必須在資料集層級或檢視表層級授予 `bigquery.dataViewer` 角色。在資料集層級授予這個角色，分析師就能存取資料集中的所有資料表和檢視表。由於本教學課程中建立的資料集只包含一個已授權檢視表，因此您會在資料集層級授予存取權。如果您需要授予存取權給一系列授權檢視表，建議改用[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)。

您先前授予資料分析師的 `bigquery.user` 角色，可提供建立查詢工作所需的權限。不過，他們必須同時具備已授權檢視表或內有該檢視表資料集的 `bigquery.dataViewer` 存取權，才能成功查詢檢視表。

如要授予資料分析師對內含授權檢視表的資料集 `bigquery.dataViewer` 存取權，請按照下列步驟操作：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，按一下「Datasets」(資料集)，然後選取「`shared_views`」資料集，開啟「Details」(詳細資料) 分頁。
4. 依序點選「共用」person\_add「權限」。
5. 在「共用權限」窗格中，按一下「新增主體」。
6. 在「New principals」(新增主體) 部分，輸入包含資料分析師的群組，例如 `data_analysts@example.com`。
7. 按一下「選取角色」，然後依序選取「BigQuery」>「BigQuery 資料檢視者」。
8. 按一下 [儲存]。
9. 按一下 [關閉]。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Assign access controls to the dataset containing the view
List<Acl> viewAcl = new ArrayList<>(sharedDataset.getAcl());
viewAcl.add(Acl.of(new Acl.Group("example-analyst-group@google.com"), Acl.Role.READER));
sharedDataset.toBuilder().setAcl(viewAcl).build().update();
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# analyst_group_email = 'data_analysts@example.com'
access_entries = shared_dataset.access_entries
access_entries.append(
    bigquery.AccessEntry("READER", EntityTypes.GROUP_BY_EMAIL, analyst_group_email)
)
shared_dataset.access_entries = access_entries
shared_dataset = client.update_dataset(
    shared_dataset, ["access_entries"]
)  # API request
```

## 授權視圖存取來源資料集

為內含授權 view 的資料集建立存取控管後，您可授予授權 view 來源資料集的檢視權限。這項授權會授予該檢視表對來源資料的存取權，而非授予資料分析師群組存取權。

如要授權檢視表存取來源資料，請選擇下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，按一下「Datasets」(資料集)，然後選取「`github_source_data`」資料集，開啟「Details」(詳細資料) 分頁。
4. 依序點選「共用」>「授權檢視」。
5. 在「Authorized views」(授權檢視表) 窗格中，輸入「Authorized view」(授權檢視表) `PROJECT_ID.shared_views.github_analyst_view`。

   將 PROJECT\_ID 替換為專案 ID。
6. 按一下「新增授權」。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Authorize the view to access the source dataset
List<Acl> srcAcl = new ArrayList<>(sourceDataset.getAcl());
srcAcl.add(Acl.of(new Acl.View(view.getTableId())));
sourceDataset.toBuilder().setAcl(srcAcl).build().update();
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
access_entries = source_dataset.access_entries
access_entries.append(
    bigquery.AccessEntry(None, EntityTypes.VIEW, view.reference.to_api_repr())
)
source_dataset.access_entries = access_entries
source_dataset = client.update_dataset(
    source_dataset, ["access_entries"]
)  # API request
```

## 驗證設定

設定完成時，資料分析師群組 (例如 `data_analysts`) 的成員可以透過查詢檢視表來驗證設定。

如要驗證設定，資料分析師應執行下列查詢：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     *
   FROM
     `PROJECT_ID.shared_views.github_analyst_view`;
   ```

   將 `PROJECT_ID` 替換為專案 ID。
3. 按一下「執行」play\_circle。

查詢結果類似下方。結果中只會顯示作者名稱和提交者名稱。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

## 完整原始碼

以下是供您參考的完整教學課程原始碼。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Create a source dataset to store your table.
Dataset sourceDataset = bigquery.create(DatasetInfo.of(sourceDatasetId));

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
        "SELECT commit, author.name as author, committer.name as committer, repo_name FROM %s.%s.%s",
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

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

### 控制台

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### gcloud

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

刪除 Google Cloud 專案：

```
gcloud projects delete PROJECT_ID
```

### 刪除個別資源

或者，如要移除本教學課程中使用的個別資源，請執行下列操作：

1. [刪除授權 view](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw#delete_views)。
2. [刪除包含已授權檢視區塊的資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#delete-datasets)。
3. [刪除來源資料集中的資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#deleting_a_table)。
4. [刪除來源資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#delete-datasets)。

您建立了本教學課程中使用的資源，因此不需要其他權限即可刪除這些資源。

## 後續步驟

* 如要瞭解 BigQuery 中的存取權控管，請參閱 [BigQuery 身分與存取權管理角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。
* 如要瞭解 BigQuery 檢視表，請參閱「[邏輯檢視表簡介](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)」。
* 如要進一步瞭解授權檢視表，請參閱[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。
* 如要瞭解存取權控管的基本概念，請參閱 [IAM 總覽](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw)。
* 如要瞭解如何管理存取權控管，請參閱「[管理政策](https://docs.cloud.google.com/iam/docs/managing-policies?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]