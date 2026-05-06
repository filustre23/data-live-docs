Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立筆記本

本文說明如何[在 BigQuery 中建立 Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)。筆記本是 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 的程式碼資產，由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 提供技術支援。

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
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery, Dataform APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cdataform.googleapis.com&hl=zh-tw)

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
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery, Dataform APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cdataform.googleapis.com&hl=zh-tw)

### 所需權限

設定適當權限，即可建立、編輯或查看記事本。

所有具備 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`) 的使用者，都擁有專案中建立的所有筆記本存取權。

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[使用身分與存取權管理功能控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

#### 建立筆記本的權限

如要取得建立及執行筆記本所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.readSessionUser)  (`roles/bigquery.readSessionUser`)
* [BigQuery Studio 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.studioUser)  (`roles/bigquery.studioUser`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

**警告：** 程式碼資產的顯示設定受專案層級的 Dataform 權限控管。具備 `dataform.repositories.list` 權限的使用者 (這項權限包含在標準 BigQuery 角色中，例如「BigQuery Job User」、「BigQuery Studio User」和「BigQuery User」)，可以在專案的「Explorer」面板中查看所有程式碼資產，無論這些資產是由他們建立，還是與他們共用。 Google Cloud 如要限制可見度，您可以建立排除 `dataform.repositories.list` 權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。**注意：** 在專案中獲派「程式碼建立者」角色的使用者，可以透過 Dataform API 或 Dataform 指令列介面 (CLI)，列出該專案中的程式碼資產名稱。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。如要查看建立及執行筆記本所需的確切權限，請展開「必要權限」部分：

#### 所需權限

* `bigquery.config.get`
* `bigquery.jobs.create`
* `bigquery.readsessions.create`
* `bigquery.readsessions.getData`
* `bigquery.readsessions.update`
* `resourcemanager.projects.get`
* `resourcemanager.projects.list`
* `dataform.locations.get`
* `dataform.locations.list`
* `dataform.repositories.create`
**注意：**擁有 `dataform.repositories.create` 權限的使用者，可以使用預設的 Dataform 服務帳戶執行程式碼，並取得授予該服務帳戶的所有權限。詳情請參閱「[Dataform 權限的安全考量](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#security-considerations-permissions)」。* `dataform.repositories.list`
* `dataform.collections.create`
* `dataform.collections.list`
* `aiplatform.notebookRuntimeTemplates.apply`
* `aiplatform.notebookRuntimeTemplates.get`
* `aiplatform.notebookRuntimeTemplates.list`
* `aiplatform.notebookRuntimeTemplates.getIamPolicy`
* `aiplatform.notebookRuntimes.assign`
* `aiplatform.notebookRuntimes.get`
* `aiplatform.notebookRuntimes.list`
* `aiplatform.operations.list`

**注意：** 建立筆記本時，BigQuery 會授予該筆記本的[Dataform 管理員角色](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。在 Google Cloud 專案中獲派 Dataform 管理員角色的所有使用者，都擁有專案中建立的所有筆記本的擁有者存取權。如要覆寫這項行為，請參閱[在建立資源時授予特定角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-specific-role)。

#### 可編輯筆記本的角色

如要編輯及執行筆記本，您必須具備下列 IAM 角色：

* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
* [筆記本執行階段使用者](https://docs.cloud.google.com/vertex-ai/docs/general/access-control?hl=zh-tw#aiplatform.notebookRuntimeUser) (`roles/aiplatform.notebookRuntimeUser`)
* [程式碼編輯器](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor) (`roles/dataform.codeEditor`)

#### 可查看筆記本的角色

如要查看及執行筆記本，您必須具備下列 IAM 角色：

* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
* [筆記本執行階段使用者](https://docs.cloud.google.com/vertex-ai/docs/general/access-control?hl=zh-tw#aiplatform.notebookRuntimeUser) (`roles/aiplatform.notebookRuntimeUser`)
* [程式碼檢視者](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer) (`roles/dataform.codeViewer`)

## 建立筆記本

請參閱下列各節，瞭解如何建立筆記本。

### 設定程式碼資產的預設區域

Google Cloud 專案中的所有新程式碼資產都會使用預設區域。資產建立後，就無法變更區域。

**重要事項：** 如果在建立程式碼資產時變更區域，該區域會成為後續所有程式碼資產的預設區域。現有的程式碼資產不會受到影響。

如要設定新程式碼資產的預設區域，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 folder「檔案」，開啟檔案瀏覽器：
3. 在專案名稱旁，按一下
   more\_vert
   「View files panel actions」(查看檔案面板動作) >「Switch code region」(切換程式碼區域)。
4. 選取要設為預設的程式碼區域。
5. 按一下 [儲存]。

如需支援的區域清單，請參閱「[BigQuery Studio 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqstudio-loc)」。

### 使用筆記本庫建立筆記本

BigQuery 的 Google Cloud 控制台筆記本庫是探索及使用預先建構筆記本範本的中心。

如要從筆記本庫中的範本建立筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如要開啟筆記本庫，請在編輯器面板的分頁列中，按一下「SQL 查詢」旁的箭頭 arrow\_drop\_downadd\_box，然後依序點選「筆記本」**> 所有範本**。
3. 在筆記本範本庫中選取範本。例如，您可以選取「開始使用 BigQuery DataFrames」。

   新的筆記本隨即開啟，內含的儲存格會顯示針對 `bigquery-public-data.ml_datasets.penguins` 公開資料集執行的範例查詢。
4. 或者，您也可以按一下「SQL 查詢」**旁的箭頭 arrow\_drop\_downadd\_box，然後依序點選「筆記本」**>「空白筆記本」**、「筆記本」>「BigQuery 範本」**或「筆記本」**>「Spark 範本」**，開啟這些特定範本。
5. 如要從範本建立可執行的筆記本，請按一下「使用這個範本」。
6. 選用：如要查看筆記本詳細資料或[版本記錄](#create_a_notebook_from_an_existing_notebook)、新增註解、回覆或取得現有註解的連結，請使用下列工具列：

   「註解」工具列功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。如要提供意見回饋或尋求這項功能的支援，請傳送電子郵件至 [bqui-workspace-pod@google.com](mailto:bqui-workspace-pod@google.com)。
7. 選用：在工具列中，您可以使用「參考」面板預覽資料表、快照、檢視區塊或具體化檢視區塊的結構定義詳細資料，或是在新分頁中開啟這些項目。面板也會列出最近和已加星號的資源。

### 從表格建立筆記本

如要建立含有特定資料表預設查詢的筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下資料集。
4. 依序點選「總覽」**>「表格」**，然後找出要查詢的表格。
5. 依序點選資料表旁的 more\_vert「動作」和「在 Python 筆記本中開啟」>。

   系統會開啟新筆記本，其中包含的儲存格會顯示針對所選資料表的範例查詢。

### 建立筆記本，探索查詢結果集

如要建立筆記本來探索查詢結果集，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在編輯器窗格中，執行會產生查詢結果的查詢。
3. **在「查詢結果」窗格中，依序點選「開啟方式」>「Notebook」**。

   系統會開啟新的筆記本，其中包含可傳回查詢 SQL 和查詢結果的程式碼儲存格。

### 從現有筆記本建立筆記本

如要將現有筆記本的任何版本開啟為新筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 選取筆記本。
5. 按一下 schedule「版本記錄」。
6. 依序點選筆記本版本旁的 more\_vert「查看動作」和「開啟為新的 Python 筆記本」。

   筆記本副本會以新筆記本的形式開啟。

## 上傳筆記本

您可以上傳本機筆記本，在 BigQuery Studio 中使用。上傳的筆記本隨後會顯示在 Google Cloud 控制台的 BigQuery 頁面中。

如要上傳筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後執行下列其中一個步驟：

   * 在「筆記本」旁，依序點選 more\_vert「查看動作」>「上傳至筆記本」。
   * 在 Google Cloud 專案名稱旁，依序點選 more\_vert「查看動作」>「上傳至專案」>「筆記本」。
4. 在「Upload Notebook」(上傳筆記本) 對話方塊的「Notebook」(筆記本) 欄位中，按一下「Browse」(瀏覽)，然後選取要上傳的筆記本。
5. 選用：在「筆記本名稱」欄位中編輯筆記本名稱。
6. 在「Region」(地區) 欄位中，選取要上傳筆記本的地區。
7. 按一下「上傳」。

您可以透過「Explorer」窗格存取筆記本。

## 連線至執行階段

請參閱下列各節，瞭解如何將筆記本連線至 [Vertex AI 執行階段](https://docs.cloud.google.com/colab/docs/create-runtime?hl=zh-tw)。執行階段是運算資源，可執行筆記本中的程式碼。執行階段必須與筆記本位於相同區域。

如要進一步瞭解執行階段，請參閱[執行階段和執行階段範本](https://docs.cloud.google.com/colab/docs/runtimes?hl=zh-tw)。

**注意：** 如果您使用 [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/overview?hl=zh-tw)，請務必先[設定 Private Google Access 搭配 VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/private-connectivity?hl=zh-tw)，再連線至執行階段。否則，服務會傳回錯誤 `Failed to connect to Runtime Network
projects/projectid/global/networks/default' was not found.`

### 連線至預設執行階段

預設執行階段是預先設定的執行階段，只需要進行最少的設定。

如要連線至預設執行階段，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下筆記本名稱即可開啟。
5. 在筆記本中，按一下「連線」，或執行筆記本中的任何儲存格。

   如果沒有啟用的執行階段，連線至預設執行階段可能需要幾分鐘的時間。

### 連線至非預設執行階段

如要使用預設執行階段以外的執行階段，請先在 Vertex AI 中[建立該額外執行階段](https://docs.cloud.google.com/vertex-ai/docs/colab/create-runtime?hl=zh-tw)。

如要連線至非預設的執行階段，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下筆記本名稱即可開啟。
5. 在筆記本中，按一下「連線」旁的下拉式選單 arrow\_drop\_down，然後按一下「連線到執行階段」。
6. 按一下「連線至現有的執行階段」。
7. 在「Runtimes」(執行階段) 中，選取要使用的執行階段。執行階段必須與筆記本位於相同位置。
8. 按一下「連線」。

### 連線至新的執行階段

如要連線至新的執行階段，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下筆記本名稱即可開啟。
5. 在筆記本中，按一下「連線」旁的下拉式選單 arrow\_drop\_down，然後按一下「連線到執行階段」。
6. 按一下「建立新的執行階段」。
7. 在「執行階段範本」中，選取要使用的 [Vertex AI 執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)。
8. 在「執行階段名稱」中，輸入執行階段的名稱。
9. 按一下「連線」。

## 瞭解儲存格

筆記本是由可編輯的儲存格組成。系統支援下列類型的儲存格：

* **文字儲存格**：使用文字儲存格，以 Markdown 格式在筆記本中加入說明和圖片。
* **程式碼儲存格**：使用程式碼儲存格將 Python 新增至筆記本。您可以個別執行每個程式碼儲存格。程式碼儲存格可以參照您已執行的其他儲存格中建立的任何變數。
* **SQL 儲存格**：使用 [SQL 儲存格](https://docs.cloud.google.com/colab/docs/sql-cells?hl=zh-tw)執行 GoogleSQL 查詢。查詢輸出內容會自動儲存為 DataFrame，名稱與儲存格標題相同。您可以在單一 SQL 儲存格中執行多個 SQL 陳述式，但只有最後一個陳述式的結果會儲存至 DataFrame。

  您可以在運算式中參照 Python 變數，或將 BigQuery DataFrames 做為查詢中的資料表，方法是將變數名稱放在大括號 (`{ }`) 中：

  ```
  # Refer to the Python variable my_threshold in a SQL expression.
  SELECT * FROM my_dataset.my_table WHERE x > {my_threshold};

  # Reference previous query results to iterate on your queries.
  SELECT * FROM {df};
  ```
* **圖表儲存格**：使用[圖表儲存格](https://docs.cloud.google.com/colab/docs/visualization-cells?hl=zh-tw)，自動生成筆記本中任何 DataFrame 的圖表。您可以修改要顯示的資料欄，並從各種圖表類型和匯總中選取。您也可以選擇自訂顏色、資料標籤和標題。

## 授予筆記本存取權

如要授權其他使用者存取筆記本，請將這些使用者新增至適當的 IAM 角色。

**重要事項：** 只要使用者具備筆記本存取權，即可查看筆記本中程式碼產生的所有輸出內容，即便內含使用者無權存取的資料表內容也一樣。如要避免共用已儲存的輸出內容，請[停用筆記本輸出內容儲存功能](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#disable_output_saving)。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 找出要授予存取權的記事本。
5. 按一下筆記本旁的「開啟動作」more\_vert，然後按一下「共用」。
6. 在「分享權限」窗格中，按一下「新增使用者/群組」。
7. 在「New principals」(新增主體) 欄位中輸入主體。
8. 在「Role」(角色) 清單中，選取下列其中一個角色：

   * [**程式碼擁有者**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner)：可以對筆記本執行任何動作，包括刪除或共用筆記本。
   * [**程式碼編輯器**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor)：可編輯筆記本。
   * [**程式碼檢視者**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer)：可以查看筆記本。**注意：** 主體也必須具備[Notebook 執行階段使用者 (`roles/aiplatform.notebookRuntimeUser`)](https://docs.cloud.google.com/vertex-ai/docs/general/access-control?hl=zh-tw#aiplatform.notebookRuntimeUser) 和 [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user)角色，才能執行筆記本。
9. 選用：如要查看完整的角色清單和進階共用設定，請按一下「進階共用設定」。
10. 按一下 [儲存]。
11. 如要返回筆記本資訊頁面，請按一下「關閉」。

## 共用筆記本

如要與其他使用者共用筆記本，可以產生並分享筆記本連結。如要讓其他使用者查看您共用的筆記本，請先[授予筆記本存取權](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#grant_access_to_notebooks)。

如要執行 Notebook，使用者必須能存取 Notebook 所存取的資料。詳情請參閱「[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)」。

**重要事項：** 只要使用者具備筆記本存取權，即可查看筆記本中程式碼產生的所有輸出內容，即便內含使用者無權存取的資料表內容也一樣。如要避免共用已儲存的輸出內容，請[停用筆記本輸出內容儲存功能](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#disable_output_saving)。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 找出要共用的記事本。你可以使用搜尋功能或篩選器尋找筆記本。
5. 按一下筆記本旁邊的「查看動作」more\_vert，然後依序點選「分享」>「複製連結」。
6. 將連結分享給其他使用者。

## 停用筆記本輸出內容儲存功能

如要禁止與有權存取筆記本檔案的其他使用者共用儲存的筆記本輸出內容，請停用筆記本輸出內容儲存功能。

停用所選筆記本的輸出內容儲存功能後，BigQuery 會刪除筆記本檔案中儲存的所有輸出內容，且不會儲存後續執行的輸出內容。

不過，[有權存取筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#grant_access_to_notebooks)的使用者仍可透過下列方式查看輸出內容：

* 執行筆記本，查看目前的輸出內容。系統不會儲存這項輸出內容。
* 在修訂版本記錄中查看筆記本的封存版本和輸出內容。

如要停用所選筆記本的輸出內容儲存功能，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下要停用儲存輸出的筆記本。
5. 如要展開選單列，請依序點選 keyboard\_arrow\_down **切換標題顯示設定**。
6. 依序點選「編輯」**>「筆記本設定」**。
7. 在「筆記本設定」視窗中，選取「儲存這個筆記本時，忽略程式碼儲存格輸出內容」。
8. 按一下 [儲存]。
9. 按一下「重新載入」。

## 解決衝突

如果您和其他使用者在筆記本中進行衝突的變更，服務會引發 `Automatic saving failed. This file was updated remotely or
in another tab.` 錯誤，並提供 `Show diff` 連結。如要解決衝突，請按照下列步驟操作：

1. 按一下 `Show diff` 連結。系統會開啟「查看遠端變更」對話方塊。
2. 選用：如要比較筆記本原始碼，請勾選「原始碼」核取方塊。
3. 選用步驟：如要直接比較版本，而非在個別窗格中比較，請勾選「Inline diff」核取方塊。
4. 查看變更並決定要保留哪些變更，必要時請修訂輸入內容。
5. 按一下「儲存變更」。

## 重新命名筆記本

如要重新命名筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下要重新命名的記事本。
5. 按一下 keyboard\_arrow\_down「切換標題顯示設定」
   即可展開選單列。
6. 依序點選「檔案」**>「重新命名」**。
7. 在「Rename notebook」(重新命名筆記本) 對話方塊中輸入筆記本名稱，然後按一下「Rename」(重新命名)。

## 疑難排解

詳情請參閱「[排解 Colab Enterprise 問題](https://docs.cloud.google.com/colab/docs/troubleshooting?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[管理記事本](https://docs.cloud.google.com/bigquery/docs/manage-notebooks?hl=zh-tw)。
* 瞭解如何[排定筆記本](https://docs.cloud.google.com/bigquery/docs/orchestrate-notebooks?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]