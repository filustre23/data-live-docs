Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立筆記本

本文說明如何[在 BigQuery 中建立 Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)。Notebooks 是 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 程式碼資產，採用 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 技術。

## 事前準備

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
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
- Enable the BigQuery, Dataform, and Compute Engine APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cdataform.googleapis.com%2Ccompute.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery, Dataform, and Compute Engine APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cdataform.googleapis.com%2Ccompute.googleapis.com&hl=zh-tw)

### 所需權限

設定適當權限，以便建立、編輯或查看筆記本。

凡是具備 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`) 的使用者，都擁有專案中所有筆記本的擁有者存取權。

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

#### 建立 Notebook 的權限

如要取得建立及執行筆記本所需的權限，請要求管理員授予您專案的 [BigQuery Studio 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.studioUser)  (`roles/bigquery.studioUser`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

**注意：** 在專案中獲派程式碼建立者角色的使用者，可以使用 Dataform API 或 Dataform 指令列介面 (CLI)，列出該專案中的程式碼資產名稱。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。如要查看建立及執行 Notebook 的確切必要權限，請展開「Required permissions」(必要權限) 部分：

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
* `dataform.repositories.list`
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

**注意：** 建立筆記本時，BigQuery 會授予您該筆記本的 [Dataform 管理員角色](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。凡是具備 Google Cloud 專案 Dataform 管理員角色的使用者，都擁有該專案中所有 Notebook 的擁有者權限。如要覆寫這項行為，請參閱「[在建立資源時授予特定角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-specific-role)」。

#### 編輯 Notebook 的角色

如要編輯及執行 Notebook，您必須具備下列 IAM 角色：

* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
* [Notebook 執行階段使用者](https://docs.cloud.google.com/vertex-ai/docs/general/access-control?hl=zh-tw#aiplatform.notebookRuntimeUser) (`roles/aiplatform.notebookRuntimeUser`)
* [程式碼編輯器](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor) (`roles/dataform.codeEditor`)

#### 查看 Notebook 的角色

如要查看及執行筆記本，您必須具備下列 IAM 角色：

* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
* [Notebook 執行階段使用者](https://docs.cloud.google.com/vertex-ai/docs/general/access-control?hl=zh-tw#aiplatform.notebookRuntimeUser) (`roles/aiplatform.notebookRuntimeUser`)
* [程式碼檢視者](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer) (`roles/dataform.codeViewer`)

#### Notebook 的安全性考量

BigQuery 中的程式碼資產是由 Dataform 提供，因此請考量下列安全性影響，再授予使用者這些資產的存取權：

* 程式碼資產的瀏覽權限由專案層級的 Dataform 權限控管。使用者只要具備 `dataform.repositories.list` 權限 (包含在標準 BigQuery 角色中，例如 [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)、[BigQuery Studio 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser)和 [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user))，就能在 Google Cloud 專案的「Explorer」面板中查看所有程式碼資產，無論這些資產是否由他們建立或與他們共用。如要限制瀏覽權限，可以建立不含 `dataform.repositories.list` 權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。
* 凡是與 Dataform 服務代理共用的 Secret，可編輯這些資產的使用者都有可能存取。為確保憑證安全，請限制只有信任的使用者才能建立及編輯權限，並限制 Dataform 服務代理可存取的密鑰。詳情請參閱「[在套件安裝期間存取 Secret](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#secret-access-risk)」。

詳情請參閱「[Dataform 權限的安全性考量](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#security-considerations-permissions)」。

## 建立筆記本

請參閱下列各節，瞭解如何建立筆記本。

### 設定程式碼資產的預設區域

Google Cloud 專案中的所有新程式碼資產都會使用預設區域。資產建立後，就無法變更區域。

**重要事項：** 如果在建立程式碼資產時變更區域，該區域會成為後續所有程式碼資產的預設區域。現有程式碼資產不受影響。

如要設定新程式碼資產的預設區域，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder Files」(檔案)，開啟檔案瀏覽器：
3. 按一下專案名稱旁的 more\_vert「View files panel actions」(查看檔案面板動作) >「Switch code region」(切換程式碼區域)。
4. 選取要設為預設值的程式碼區域。
5. 按一下 [儲存]。

如要查看支援的地區清單，請參閱「[BigQuery Studio 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqstudio-loc)」。

### 使用筆記本庫建立筆記本

BigQuery Google Cloud 控制台中的筆記本庫是探索及使用預先建構筆記本範本的中心。

如要使用筆記本庫中的範本建立筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如要開啟筆記本庫，請在編輯器窗格的分頁列中，按一下「SQL 查詢」 旁的
   arrow\_drop\_down
   箭頭，然後依序點選「筆記本」>「所有範本」。add\_box
3. 在筆記本庫中選取範本。例如，您可以選取「**開始使用 BigQuery DataFrames**」。

   新的筆記本隨即開啟，其中包含的儲存格會顯示針對 `bigquery-public-data.ml_datasets.penguins` 公開資料集的範例查詢。
4. 或者，您也可以點選「SQL 查詢」 旁邊的
   arrow\_drop\_down
   箭頭，然後依序點選 **「Notebook」>「空白筆記本」**、
   **「Notebook」>「BigQuery 範本」**或
   **「Notebook」>「Spark 範本」**，開啟這些特定範本。add\_box
5. 如要從範本建立可執行的筆記本，請按一下「Use this template」(使用這個範本)。
6. 選用：如要查看筆記本詳細資料或[版本記錄](#create_a_notebook_from_an_existing_notebook)、新增註解、回覆或取得現有註解的連結，請使用下列工具列：

   「Comments」(註解) 工具列功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。如要提供意見或尋求支援，請傳送電子郵件至 [bqui-workspace-pod@google.com](mailto:bqui-workspace-pod@google.com)。
7. 選用：在「Comments」(註解) 工具列中，您可以使用「Reference」(參考資料) 面板預覽資料表、快照、檢視表或 materialized view 的結構定義詳細資料，或在新分頁中開啟。面板也會列出最近和已加星號的資源。

### 從資料表建立筆記本

如要建立含有特定資料表預設查詢的筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
4. 依序點選**「總覽」 > 「資料表」**，然後找出要查詢的資料表。
5. 依序點選資料表旁的 more\_vert **「Actions」(動作)**
   和**「Open in」(開啟方式) >「Python notebook」(Python 筆記本)**。

   新的筆記本隨即開啟，其中包含顯示所選資料表範例查詢的儲存格。

### 建立筆記本，探索查詢結果集

如要建立筆記本來探索查詢結果集，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在編輯器窗格中執行查詢，產生查詢結果。
3. 在「**查詢結果**」窗格中，依序點選**「開啟方式」>「Notebook」**。

   新的筆記本會開啟，其中包含程式碼儲存格，可傳回查詢 SQL 和查詢結果。

### 根據現有筆記本建立筆記本

如要將現有筆記本的任何版本開啟為新筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 選取筆記本。
5. 按一下 schedule「版本記錄」。
6. 按一下筆記本版本旁的 more\_vert「View actions」(查看動作)，然後點選「Open as new Python notebook」(開啟為新的 Python 筆記本)。

   系統會開啟筆記本副本，做為新的筆記本。

## 上傳筆記本

您可以上傳本機筆記本，在 BigQuery Studio 中使用。上傳的筆記本會顯示在 Google Cloud 控制台的 BigQuery 頁面中。

如要上傳筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後執行下列任一操作：

   * 按一下「筆記本」旁的 more\_vert「查看動作」>「上傳筆記本」。
   * 按一下 Google Cloud 專案名稱旁的more\_vert「查看動作」「上傳至專案」「Notebook」。
4. 在「Upload Notebook」(上傳筆記本) 對話方塊的「Notebook」(筆記本) 欄位中，按一下「Browse」(瀏覽)，然後選取要上傳的筆記本。
5. 選用：在「Notebook name」(筆記本名稱) 欄位中，編輯筆記本名稱。
6. 在「Region」(區域) 欄位，選取要上傳筆記本的區域。
7. 按一下「上傳」。

您可以透過「Explorer」窗格存取筆記本。

## 連線到執行階段

請參閱下列各節，瞭解如何將筆記本連結至 [Gemini Enterprise Agent Platform 執行階段](https://docs.cloud.google.com/colab/docs/create-runtime?hl=zh-tw)。執行階段是運算資源，用於執行筆記本中的程式碼。執行階段必須與筆記本位於相同區域。

如要進一步瞭解執行階段，請參閱「[執行階段和執行階段範本](https://docs.cloud.google.com/colab/docs/runtimes?hl=zh-tw)」。

**注意：** 如果您使用 [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/overview?hl=zh-tw)，請務必先[設定 Private Google Access 搭配 VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/private-connectivity?hl=zh-tw)，再連線至執行階段。否則，服務會傳回錯誤 `Failed to connect to Runtime Network
projects/projectid/global/networks/default' was not found.`

### 連線至預設執行階段

預設執行階段是預設的執行階段，只需進行最基本的設定。

如要連線至預設執行階段，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 按一下筆記本名稱即可開啟。
5. 在筆記本中，點選「Connect」，或執行筆記本中的任何儲存格。

   如果沒有啟用的執行階段，可能需要幾分鐘才能連線至預設執行階段。

### 連線至非預設執行階段

如要使用預設以外的執行階段，請先[在 Agent Platform 建立該執行階段](https://docs.cloud.google.com/gemini-enterprise-agent-platform/notebooks/colab/create-runtime?hl=zh-tw)。

如要連線至非預設執行階段，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 按一下筆記本名稱即可開啟。
5. 在筆記本中，按一下「Connect」(連線) 旁邊的 arrow\_drop\_down 下拉式選單，然後點選「Connect to a runtime」(連線至執行階段)。
6. 按一下「連線至現有的執行階段」。
7. 在「Runtimes」(執行階段) 中，選取要使用的執行階段。執行階段必須與 Notebook 位於相同位置。
8. 點選「連線」。

### 連線至新的執行階段

如要連線至新的執行階段，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 按一下筆記本名稱即可開啟。
5. 在筆記本中，按一下「Connect」(連線) 旁邊的 arrow\_drop\_down 下拉式選單，然後點選「Connect to a runtime」(連線至執行階段)。
6. 按一下「建立新的執行階段」。
7. 在「Runtime Template」(執行階段範本) 中，選取要使用的 [Agent Platform 執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)。
8. 在「Runtime name」(執行階段名稱) 中，輸入執行階段的名稱。
9. 點選「連線」。

## 疑難排解

詳情請參閱「[排解 Colab Enterprise 問題](https://docs.cloud.google.com/colab/docs/troubleshooting?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[管理筆記本](https://docs.cloud.google.com/bigquery/docs/manage-notebooks?hl=zh-tw)。
* 瞭解如何[排定筆記本執行作業](https://docs.cloud.google.com/bigquery/docs/orchestrate-notebooks?hl=zh-tw)。
* 瞭解如何[存取 BigQuery Studio Git 存放區掛接中的筆記本檔案](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw#notebook-mount)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-20 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-20 (世界標準時間)。"],[],[]]