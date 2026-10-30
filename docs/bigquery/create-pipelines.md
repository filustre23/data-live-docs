Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立管道

您可以在 [BigQuery 中建立管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)，自動調度及執行工作流程，例如排定 SQL 查詢、筆記本和資料準備工作的執行順序。

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
- Enable the BigQuery, Dataform, and Vertex AI APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cdataform.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery, Dataform, and Vertex AI APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cdataform.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

### VPC Service Controls 需求

如果您使用 VPC Service Controls 保護管道，請注意，管道執行作業是由 Dataform 提供。為排定執行作業設定 VPC Service Controls 時，請務必符合下列規定：

* 您必須設定 [`dataform.restrictGitRemotes` 組織政策服務](https://docs.cloud.google.com/dataform/docs/restrict-git-remotes?hl=zh-tw)。
* Dataform 和 BigQuery 必須受相同的 VPC Service Controls service perimeter 限制。
* 如要允許使用者在排定或手動觸發執行作業時，使用 Google 帳戶的使用者憑證進行驗證，您必須將他們的使用者身分新增至輸入規則。詳情請參閱「[更新 service perimeter 的輸入和輸出政策](https://docs.cloud.google.com/vpc-service-controls/docs/configuring-ingress-egress-policies?hl=zh-tw#updating)」和「[輸入規則參考資料](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw#ingress-rules-reference)」。

如需詳細設定步驟和安全性考量，請參閱「[設定 Dataform 的 VPC Service Controls](https://docs.cloud.google.com/dataform/docs/vpc-service-controls?hl=zh-tw)」。

### 管道必要角色

如要取得建立管道所需的權限，請要求管理員授予您下列 IAM 角色：

* 如要建立管道：專案的[程式碼建立者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeCreator)  (`roles/dataform.codeCreator`)
* 如要編輯及執行管道：專案的 [Dataform 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.editor)  (`roles/dataform.editor`)
* 如要在使用者資料夾中建立管道，請按照下列步驟操作：
  + 專案的[程式碼建立者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeCreator)  (`roles/dataform.codeCreator`)
  + 資料夾的[程式碼擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeOwner)  (`roles/dataform.codeOwner`)
  + 資料夾上的「Code Editor」(程式碼編輯器) (`roles/dataform.codeEditor`)
* 如要在團隊資料夾中建立管道，請按照下列步驟操作：
  + 團隊資料夾的[團隊資料夾協作者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.teamFolderContributor)  (`roles/dataform.teamFolderContributor`)
  + 團隊資料夾的[團隊資料夾擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.teamFolderOwner)  (`roles/dataform.teamFolderOwner`)
* 如要連結 Git 資料夾的 Git 存放區：專案的 [Developer Connect OAuth 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/developerconnect?hl=zh-tw#developerconnect.oauthUser)  (`roles/developerconnect.oauthUser`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如要進一步瞭解 Dataform IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw)」。

如要進一步瞭解資料夾的角色，請參閱「[建立及管理資料夾](https://docs.cloud.google.com/bigquery/docs/create-manage-folders?hl=zh-tw#required_roles)」。

如要進一步瞭解 Git 存放區的角色，請參閱「[使用 BigQuery Studio Git 存放區管理程式碼](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw#required_roles)」。

**注意：** 建立管道時，BigQuery 會授予您該管道的 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。凡是具備 Google Cloud 專案 Dataform 管理員角色的使用者，都擁有專案中所有管道的擁有者存取權。如要覆寫這項行為，請參閱「[在建立資源時授予特定角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-specific-role)」。

### 筆記本選項的必要角色

如要取得在筆記本選項中選取執行階段範本所需的權限，請要求管理員授予您專案的[Notebook Runtime User](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.notebookRuntimeUser)  (`roles/aiplatform.notebookRuntimeUser`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如果沒有這個角色，可以選取預設的筆記本執行階段規格。

### 管道的安全性考量

BigQuery 中的程式碼資產是由 Dataform 提供，因此請考量下列安全性影響，再授予使用者這些資產的存取權：

* 程式碼資產的瀏覽權限由專案層級的 Dataform 權限控管。使用者只要具備 `dataform.repositories.list` 權限 (包含在標準 BigQuery 角色中，例如 [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)、[BigQuery Studio 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser)和 [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user))，就能在 Google Cloud 專案的「Explorer」面板中查看所有程式碼資產，無論這些資產是否由他們建立或與他們共用。如要限制瀏覽權限，可以建立不含 `dataform.repositories.list` 權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。
* 凡是與 Dataform 服務代理共用的 Secret，都有可能遭到可編輯這些資產的使用者存取。為確保憑證安全，請限制只有信任的使用者才能建立及編輯權限，並限制 Dataform 服務代理可存取的密鑰。詳情請參閱「[在套件安裝期間存取 Secret](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#secret-access-risk)」。

詳情請參閱「[Dataform 權限的安全性考量](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#security-considerations-permissions)」。

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

## 建立管道

您可以透過下列方式建立及儲存管道：

* **在資料夾中**：在 BigQuery Studio 的「檔案」窗格中，將管道整理到個人或團隊資料夾。
* **在 BigQuery Studio Git 資料夾中** ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：使用 Developer Connect 連結 Git 存放區，在資料夾中託管、控管版本及管理多個獨立管道或根層級管道。
* **從編輯器分頁列**：在查詢編輯器的「+」選單中建立管道。
* **透過「Pipelines & Connections」(管道和連線) 頁面** ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：使用簡化的 BigQuery 專屬工作流程建立管道。

### 在資料夾中建立管道

您可以在 BigQuery Studio 的個人使用者資料夾或共用團隊資料夾中，直接建立及管理管道。如要進一步瞭解資料夾，請參閱「[使用資料夾整理程式碼資產](https://docs.cloud.google.com/bigquery/docs/code-asset-folders?hl=zh-tw)」。

如要在資料夾中建立管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下 folder「Files」(檔案)，開啟檔案瀏覽器。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 請執行下列任一操作來建立管道：

   * 選取要放置管道的使用者資料夾或團隊資料夾，按一下工具列上的「+」 (建立) 按鈕，然後選取「管道」。
   * 在檔案樹狀結構中，按一下資料夾名稱旁的「查看動作」圖示 more\_vert，然後依序選取「建立」>「管道」。
   * 開啟資料夾，在主面板中查看內容，然後按一下「Create Pipeline」(建立管道)。
4. 在建立對話方塊中，輸入管道名稱。
5. 點選「建立」。檔案樹狀結構中會出現新的管道資料夾，並顯示「管道」圖示。
6. 按一下管道資料夾，開啟「Pipeline Viewer」，然後調整[管道設定](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw#configure-pipeline-settings)。

### 在 Git 存放區建立管道

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或尋求這項功能的支援，請傳送電子郵件至 [cloud-pipelines-ui@google.com](mailto:cloud-pipelines-ui@google.com)。

您可以在 BigQuery Studio 中，直接在與 Git 整合的資料夾內建立及管理管道。Git 資料夾代表使用 Developer Connect 連結至 BigQuery Studio 的遠端 GitHub 或 GitLab 存放區。您可以在單一 Git 存放區中，託管及管理多個獨立管道。Git 存放區管道支援 Dataform [部署作業](https://docs.cloud.google.com/dataform/docs/deployments?hl=zh-tw)，可用於排程、發布設定和多環境自動化調度管理。

如要在 Git 資料夾中建立管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如果您尚未連結 Git 存放區，請[建立並連結 BigQuery Studio Git 存放區](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw#create-git-repository)。
3. 在左側窗格中，按一下 folder「Files」(檔案)，開啟檔案瀏覽器。
4. 在檔案樹狀結構中，找出已連結的 Git 存放區資料夾，或其中的巢狀目錄。
5. 按一下資料夾名稱旁的 more\_vert「View actions」(查看動作)，然後依序選取「Create」(建立) >「Pipeline」(管道)。
6. 在對話方塊中輸入管道名稱，然後按一下「儲存」。

   系統會建立新的管道目錄，並使用預設檔案進行初始化：

   * `workflow_settings.yaml`：管道設定。
   * `definitions/actions.yaml`：空白工作定義。
7. 在檔案瀏覽器中點選管道目錄，開啟「Pipeline Viewer」。

**注意：** 如果遠端 Git 存放區的根目錄含有管道設定 (`workflow_settings.yaml`)，BigQuery Studio 會自動將該存放區視為**根層級管道**。Git 存放區資料夾本身會顯示「管道」圖示。點選 Git 存放區資料夾後，**Pipeline Viewer** 會開啟，並顯示整個存放區的已編譯 DAG。您不需要建立巢狀管道目錄。

### 從編輯器分頁列建立管道

如要從編輯器分頁列建立管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在編輯器窗格的分頁列中，按一下 **+** 符號旁的 arrow\_drop\_down 箭頭，然後點選「Pipeline」(管道)。
3. 選用：如要重新命名管道，請按一下管道名稱，然後輸入新名稱。
4. 調整[管道設定](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw#configure-pipeline-settings)。

### 透過「管道與連線」頁面建立管道

您可以在 Google Cloud 控制台中使用 BigQuery 的「Pipelines & Connections」(管道和連線) 頁面，建立使用[簡化 BigQuery 專屬工作流程](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw)的 Dataform 管道。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要瞭解如何從 BigQuery 的「Pipelines & Connections」(管道和連線) 頁面建立管道，請參閱「[建立資料整合資產](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw#create_a_data_integration_asset)」。

## 設定管道

如要設定管道，請在**管道檢視器**中開啟管道，按一下「Settings」(設定) 分頁標籤，然後設定下列部分：

1. 在「Authentication」(驗證) 部分，選擇使用 Google 帳戶的使用者憑證或服務帳戶，為管道授權。

   * 如要使用 Google 帳戶的使用者憑證，請選取「Run with my user credentials」(以我的使用者憑證執行)。

     選用：在「Extended access options」(擴充存取權選項) 部分，選取管道所需的其他服務：

     + **Knowledge Catalog**：可更新 Google Cloud Knowledge Catalog 中繼資料。
     + **Google 雲端硬碟**：允許唯讀存取 Google 雲端硬碟檔案。
     + **Bigtable**：可讀取 Google Bigtable 資料 (唯讀)。

       **注意：** 系統不支援使用使用者憑證驗證 API 執行作業。如要使用 Dataform API [執行管道中的所有工作](#run-pipeline-all-tasks)，您必須設定管道，讓其使用服務帳戶。
   * 如要使用服務帳戶，請選取「Run with selected service account」(以所選服務帳戶執行)，然後選取服務帳戶。如需建立服務帳戶，請按一下「New service account」(新增服務帳戶)。
2. 在「Processing location」(處理位置) 部分，選取管道的處理位置。

   * 如要啟用自動選取位置功能，請選取「Automatic location selection」(自動選取位置)。這個選項會根據要求中參照的資料集選取位置。選擇程序如下：

     + 如果查詢參照相同位置的資料集，BigQuery 會使用該位置。
     + 如果查詢參照兩個以上不同位置的資料集，就會發生錯誤。如要進一步瞭解這項限制，請參閱「[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)」。
     + 如果查詢未參照任何資料集，BigQuery 會預設為 `US` 多區域。
   * 如要選擇特定區域，請選取「Region」(區域)，然後在「Region」(區域) 選單中選擇區域。或者，您也可以在查詢中使用 [`@@location` 系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)。詳情請參閱「[指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)」。
   * 如要選擇多區域，請選取「Multi-region」(多區域)，然後在「Multi-region」(多區域) 選單中選擇多區域。

   管道處理位置不一定要與程式碼資產的預設儲存位置相同。

### SQLX 選項

如要設定管道的 SQLX 設定，請在「SQLX options」(SQLX 選項) 專區執行下列操作：

1. 在「Default project」(預設專案) 欄位中，輸入現有Google Cloud 專案的名稱。這個值會用於 `workflow_settings.yaml` 檔案中的 `defaultProject`，以及 `dataform.json` 檔案中的 `defaultDatabase`。管道工作執行期間會使用預設專案。

   **注意：** 系統不會驗證專案名稱，因此您可以輸入任何非空白字串。不過，如果專案不存在，管道執行作業就會失敗。
2. 選用：在「Default dataset」(預設資料集) 欄位中，搜尋並選取現有資料集。系統會根據所選專案和處理位置，篩選可用的資料集清單。這個值會用於 `workflow_settings.yaml` 檔案中的 `defaultDataset`。管道工作執行時會使用預設資料集。

   **注意：** 設定預設資料集後，如果變更管道的區域，資料集選取項目就會失效。變更專案也可能導致資料集選取項目失效。如果所選專案中沒有指定資料集，系統會建立資料集。

### Notebook 選項

如要在管道中新增筆記本，請在「Notebook options」(筆記本選項) 專區執行下列操作：

1. 在「Runtime template」(執行階段範本) 欄位中，接受預設的筆記本執行階段，或搜尋並選取現有的執行階段。

   * 如要查看預設執行階段的規格，請按一下旁邊的箭頭。
   * 如要建立新的執行階段，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。**注意：**筆記本執行階段範本必須與指定該範本的管道位於相同區域。**注意：**在 BigQuery 管道中加入筆記本後，就無法變更 Gemini Enterprise Agent Platform 執行階段執行個體的網路。執行階段僅限用於預設網路，不支援選取其他網路。
2. 在「Cloud Storage bucket」欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket，用於儲存管道中 Notebook 的輸出內容。
3. 按照「[將主體新增至 bucket 層級政策](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add)」中的步驟，將自訂 Dataform 服務帳戶新增為主體，並加入您要用來儲存排定 pipeline 執行作業輸出的 Cloud Storage bucket，然後將 [Storage 管理員角色](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin) (`roles/storage.admin`) 授予這個主體。

   所選自訂 Dataform 服務帳戶必須具備所選 bucket 的 Storage 管理員 IAM 角色。

## 新增管道工作

您可以在管道中新增多項工作，按照特定順序執行程式碼資產。

管道內支援的程式碼資產包括：

* SQL 查詢
* Notebooks
* 資料準備
* 資料表和檢視表 (SQLX 工作)

### 工作命名慣例

為管道任務命名時，請遵循下列命名慣例：

* 任務名稱只能包含英文字母 (a-z、A-Z)、數字 (0-9)、底線 (`_`) 和連字號 (`-`)。
* 工作名稱開頭須為英文字母、數字或底線。
* 工作名稱不得包含半形句號 (`.`)。命名或重新命名工作時，請勿加入 `.sql` 或 `.py` 等副檔名。如果工作名稱含有半形句號，「Run」(執行) 按鈕會停用。
* 任務名稱可包含字元，總長度最多 1,024 個 UTF-8 位元組。
* 管道容器中的任務名稱不得重複。
* 工作名稱須區分大小寫。

### 新增工作

如要將工作新增至管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 如要新增程式碼素材資源，請選取下列其中一個選項：

### SQL 查詢

您可以建立新查詢，也可以匯入現有查詢。

1. 執行下列其中一個步驟：

   * 按一下「Add task」(新增工作)，然後選取「Query」(查詢)。您可以建立新查詢，也可以匯入現有查詢。
   * 在資料夾或 Git 資料夾中處理管道時，請在「Files」(檔案) 窗格中的管道資料夾上按一下滑鼠右鍵，然後選取「Create Query」(建立查詢)。
   * 在資料夾或 Git 資料夾中處理管道時，請按一下「Pipeline Viewer」中的「Add task」按鈕。
2. 選用：在「Query task details」(查詢工作詳細資料) 窗格的「Run after」(執行後) 選單中，選取要在查詢前執行的工作。

**建立新查詢**

1. 按一下「Edit Query」(編輯查詢) 旁邊的 arrow\_drop\_down 箭頭選單，然後選取「In context」(在情境中) 或「In new tab」(在新分頁中)。
2. 搜尋現有查詢。
3. 選取查詢名稱，然後按下 **Enter** 鍵。
4. 按一下 [儲存]。
5. 選用：如要重新命名查詢，請在管道窗格中按一下查詢名稱，然後依序點選「Edit Query」(編輯查詢) 和畫面頂端的現有查詢名稱，接著輸入新名稱。

**匯入現有查詢**

1. 按一下「編輯查詢」旁的arrow\_drop\_down箭頭選單，然後點選「匯入副本」。
2. 搜尋要匯入的現有查詢，或從搜尋窗格中選取現有查詢。匯入查詢時，查詢的來源檔案會複製到管道中，因此原始檔案不會變更。
3. 按一下「編輯」，開啟匯入的查詢。
4. 按一下 [儲存]。

### 筆記本

您可以建立新筆記本，也可以匯入現有筆記本。
如要變更筆記本執行階段範本的設定，請參閱「[筆記本選項](#notebook_options)」。

1. 執行下列其中一個步驟：

   * 按一下「新增工作」，然後選取「筆記本」。
   * 在資料夾或 Git 資料夾中處理管道時，請在「Files」(檔案) 窗格中的管道資料夾上按一下滑鼠右鍵，然後選取「Create Notebook」(建立筆記本)。
   * 在資料夾或 Git 資料夾中處理管道時，請按一下「Pipeline Viewer」中的「Add task」按鈕。
   1. 選用：在「Notebook task details」(Notebook 工作詳細資料) 窗格的「Run after」(執行後) 選單中，選取要在 Notebook 前執行的工作。

   **建立新的筆記本**
2. 按一下「Edit Notebook」(編輯筆記本) 旁邊的 arrow\_drop\_down 箭頭選單，然後選取「In context」(在情境中) 或「In new tab」(在新分頁中)。
3. 搜尋現有筆記本。
4. 選取筆記本名稱，然後按下 **Enter** 鍵。
5. 按一下 [儲存]。
6. 選用：如要重新命名筆記本，請在管道窗格中按一下筆記本名稱，然後依序點選「Edit Notebook」(編輯筆記本) 和畫面頂端的現有筆記本名稱，接著輸入新名稱。

**匯入現有筆記本**

1. 按一下「Edit Notebook」(編輯筆記本) 旁的 arrow\_drop\_down 箭頭選單，然後點選「Import a copy」(匯入副本)。
2. 搜尋要匯入的現有筆記本，或從搜尋窗格選取現有筆記本。匯入筆記本時，筆記本的來源檔案會複製到管道中，因此原始檔案不會變更。
3. 如要開啟匯入的筆記本，請按一下「編輯」。
4. 按一下 [儲存]。

### 準備資料

您可以建立新的資料準備作業，也可以匯入現有作業。

1. 執行下列其中一個步驟：

   * 按一下「新增工作」，然後選取「資料準備」。
   * 在資料夾或 Git 資料夾中處理管道時，請在「Files」(檔案) 窗格中的管道資料夾上按一下滑鼠右鍵，然後選取「Create Data preparation」(建立資料準備)。
   * 在資料夾或 Git 資料夾中處理管道時，請按一下「Pipeline Viewer」中的「Add task」按鈕。
2. 選用：在「Data preparation task details」(資料準備工作詳細資料) 窗格的「Run after」(執行後) 選單中，選取要在資料準備前執行的工作。

**建立新的資料準備作業**

1. 按一下「Edit Data preparation」(編輯資料準備) 旁的arrow\_drop\_down箭頭選單，然後選取「In context」(在內容中) 或「In new tab」(在新分頁中)。
2. 搜尋現有的資料準備作業。
3. 選取資料準備作業名稱，然後按下 **Enter** 鍵。
4. 按一下 [儲存]。
5. 選用：如要重新命名資料準備作業，請在管道窗格中按一下資料準備作業名稱，然後依序點選「Edit Data preparation」(編輯資料準備作業) 和畫面頂端的名稱，再輸入新名稱。

**匯入現有的資料準備**

1. 按一下「Edit Data preparation」(編輯資料準備) 旁的 arrow\_drop\_down 箭頭下拉式選單，然後點選「Import a copy」(匯入副本)。
2. 搜尋要匯入的現有資料準備，或從搜尋窗格中選取現有資料準備。匯入資料準備作業時，原始作業不會變更，因為資料準備作業的來源檔案會複製到管道中。
3. 如要開啟匯入的資料準備，請按一下「編輯」。
4. 按一下 [儲存]。

### 資料表

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或申請支援，請傳送電子郵件至 [dataform-preview-support@google.com](mailto:dataform-preview-support@google.com)。

1. 執行下列其中一個步驟：

* 按一下「新增工作」，然後選取「表格」。
* 在資料夾或 Git 資料夾中處理管道時，請在「Files」(檔案) 窗格中的管道資料夾上按一下滑鼠右鍵，然後選取「Create Table」(建立資料表)。
* 在資料夾或 Git 資料夾中處理管道時，請按一下「Pipeline Viewer」中的「Add task」按鈕。

1. 在「Create new」(新建) 窗格中，選取「Table」(資料表) 或「Incremental table」(遞增資料表)。
2. 確認資料表的預設專案，或選取新專案。
3. 確認資料表的預設資料集，或選取新的資料集。
4. 輸入表格名稱。
5. 在表格工作詳細資料窗格中，按一下「開啟」即可開啟工作。
6. 如要設定工作，請依序前往
   **「Details」(詳細資料) >「Configuration」(設定)**，或在資料表的程式碼編輯器中，使用 `config` 區塊。

如要變更中繼資料，請使用「設定」分頁。這個分頁可讓您在程式碼編輯器中編輯 `config` 區塊中的特定值，例如格式類似 JavaScript 物件的字串或陣列。使用這個分頁可避免語法錯誤，並確認設定正確無誤。

選用：在「Run after」(執行後) 選單中，選取要在資料表之前執行的工作。

您也可以在編輯器的 `config` 區塊中，定義管道任務的中繼資料。詳情請參閱「[建立資料表](https://docs.cloud.google.com/dataform/docs/reference/sample-scripts?hl=zh-tw#creating_tables)」。

編輯器會驗證程式碼，並顯示驗證狀態。

**注意：** 在 `config` 區塊中使用 JavaScript 函式做為值時，無法在「設定」分頁中編輯 JavaScript 函式。

1. 使用 `metadata` 鍵指定 Knowledge Catalog 的資訊。這項擴充程序支援下列中繼資料建構：

* 總覽：項目的說明文件和摘要文字。
* 一般切面：語意詳細資料，例如資料表系統和類型資訊。

下列設定範例說明如何將總覽和一般中繼資料切面，新增至 Knowledge Catalog 的資料表設定：

```
       ```javascript
       config {
       type: "table",
       metadata: {
          overview: "This table provides standardized trip data.",
          extraProperties: {
             generic: {
                   system: "BigQuery",
                   type: "fact table"
             }
             }
       }
       }
       ```
```

1. 在**「Details」(詳細資料) >「Compiled queries」(已編譯的查詢)** 中，查看從 SQLX 程式碼編譯的 SQL。
2. 點選「執行」，在管道中執行 SQL。
3. 在「查詢結果」中，檢查資料預覽。

### 查看

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或申請支援，請傳送電子郵件至 [dataform-preview-support@google.com](mailto:dataform-preview-support@google.com)。

1. 執行下列其中一個步驟：

   * 按一下「新增工作」，然後選取「檢視」。
   * 在資料夾或 Git 資料夾中處理管道時，請在「Files」(檔案) 窗格中的管道資料夾上按一下滑鼠右鍵，然後選取「Create View」(建立檢視畫面)。
   * 在資料夾或 Git 資料夾中處理管道時，請按一下「Pipeline Viewer」中的「Add task」按鈕。
2. 在「Create new」(新建) 窗格中，選取「View」(檢視表) 或「Materialized view」(具體化檢視表)。
3. 確認檢視表的預設專案，或選取新專案。
4. 確認檢視表的預設資料集，或選取新的資料集。
5. 輸入檢視表名稱。
6. 在「查看工作詳細資料」窗格中，按一下「開啟」即可開啟工作。
7. 如要設定工作，請使用
   **「Details」>「Configuration」**中的設定，或在檢視畫面的
   程式碼編輯器 `config` 區塊中設定。

如要變更中繼資料，請使用「設定」分頁。在這個分頁中，您可以編輯程式碼編輯器中 `config` 區塊內的特定值，例如格式類似 JavaScript 物件的字串或陣列。使用這個分頁可避免語法錯誤，並確認設定正確無誤。

選用：在「Run after」(執行後) 選單中，選取要在檢視表之前執行的工作。

您也可以在編輯器的 `config` 區塊中，定義管道任務的中繼資料。詳情請參閱「[使用 Dataform 核心建立檢視表](https://docs.cloud.google.com/dataform/docs/reference/sample-scripts?hl=zh-tw#create-view)」。

編輯器會驗證程式碼，並顯示驗證狀態。

**注意：** 在 `config` 區塊中使用 JavaScript 函式做為值時，無法在「設定」分頁中編輯 JavaScript 函式。

1. 使用 `metadata` 鍵指定 Knowledge Catalog 的資訊。這項擴充程序支援下列中繼資料建構：

* 總覽：項目的說明文件和摘要文字。
* 一般切面：語意詳細資料，例如資料表系統和類型資訊。

下列設定範例說明如何將總覽和一般中繼資料切面，新增至 Knowledge Catalog 的資料表設定：

```
       ```javascript
       config {
       type: "view",
       metadata: {
          overview: "This view provides standardized trip data.",
          extraProperties: {
             generic: {
                   system: "BigQuery",
                   type: "view"
             }
             }
       }
       }
       ```
```

1. 在**「Details」(詳細資料) >「Compiled queries」(已編譯的查詢)** 中，查看從 SQLX 程式碼編譯的 SQL。
2. 點選「執行」，在管道中執行 SQL。
3. 在「查詢結果」中，檢查資料預覽。

### 宣告來源

1. 按一下「新增工作」，然後選取「宣告來源」。
2. 在「Declare source」(宣告來源) 窗格中，驗證資料來源的預設專案，或選取新專案。
3. 確認資料來源的預設資料集，或選取新的資料集。
4. 在「Table / View」(資料表/檢視表) 欄位中，選取要用做資料來源的資料表或檢視表。
5. 點選「建立」。
6. 在宣告來源工作詳細資料窗格中，按一下「Open」(開啟) 即可開啟工作。
7. 在
   **「Details」>「Configuration」**中，或在程式碼編輯器的 `config` 區塊中，使用設定來設定資料來源。

   如要進一步瞭解如何設定資料來源，請參閱「[宣告資料來源](https://docs.cloud.google.com/dataform/docs/declare-source?hl=zh-tw)」。

   編輯器會驗證程式碼，並顯示驗證狀態。

### 斷言資料測試

1. 按一下「新增工作」，然後選取「資料品質測試」。
2. 在「Create new」(新建) 窗格中，確認資料品質測試的預設專案，或選取新專案。
3. 驗證資料品質測試的預設資料集，或選取新的資料集。
4. 在「Table」(資料表) 欄位中，輸入資料品質測試的名稱。
5. 點選「建立」。
6. 在資料品質測試工作詳細資料窗格中，按一下「Open」(開啟) 開啟工作。
7. 如要設定測試的斷言，請依序前往
   **「Details」 >「Configuration」**，或在程式碼編輯器的 `config` 區塊中進行設定。

   如要進一步瞭解如何設定斷言，請參閱「[測試資料品質](https://docs.cloud.google.com/dataform/docs/test-data?hl=zh-tw#assertions)」。

   選用：在「Run after」(執行後) 選單中，選取要在管道序列中先於資料品質測試執行的工作。

   編輯器會驗證程式碼，並顯示驗證狀態。
8. 按一下「Run」(執行)，在管道序列中執行資料品質測試。

### 單元測試

1. 按一下「新增任務」**Add task**，然後選取「單元測試」**Unit test**。
2. 在「Action to test」(要測試的動作) 欄位中，選取要測試的資料表或檢視表。
3. 在「BigQuery Unit test」(BigQuery 單元測試) 欄位中，輸入單元測試的名稱。
4. 點選「建立」。
5. 在工作詳細資料窗格中，按一下「Open」(開啟) 開啟單元測試。
6. 設定單元測試的輸入內容和預期輸出內容資料列。

   如要進一步瞭解如何設定單元測試，請參閱「[測試資料品質](https://docs.cloud.google.com/dataform/docs/test-data?hl=zh-tw#unit-tests)」。
7. 選用：如要確保輸入和輸出內容符合預期，請按一下「Run task」(執行工作)，然後選取預期或實際陳述式。
8. 按一下「Run」(執行)，在管道序列中執行資料品質測試。

## 編輯管道工作

如要編輯管道任務，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下選取的工作。
5. 如要變更前置工作，請在「Run after」(執行後) 選單中，選取要在工作之前執行的工作。
6. 如要編輯所選工作的內容，請按一下「編輯」。
7. 在新開啟的分頁中編輯工作內容，然後儲存變更。

## 刪除管道工作

如要從管道中刪除工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下選取的工作。
5. 在「Task details」(工作詳細資料) 窗格中，依序按一下「Delete」(刪除) 和「Delete」(刪除)。

## 共用管道

**重要事項：** 如果將 [`projects.locations.updateConfig` Dataform API 方法](https://docs.cloud.google.com/dataform/reference/rest/v1beta1/projects.locations/updateConfig?hl=zh-tw)中的 `enable_private_workspace` 欄位[(預先發布版)](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)設為 `true`，藉此強化安全性，則只有管道建立者可以讀取及寫入該管道中的程式碼。詳情請參閱「[啟用私人工作區](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#enable-private-workspaces)」。**注意：** 您可以共用管道，但無法共用管道中的工作。

如要共用管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下「共用」，然後選取「管理權限」。
5. 按一下「新增使用者/群組」。
6. 在「New principals」(新增主體) 欄位中，輸入至少一位使用者或群組的名稱。
7. 在「指派角色」部分選取角色。
8. 按一下 [儲存]。

## 分享管道連結

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下「分享」，然後選取「分享連結」。管道網址會複製到電腦的剪貼簿。

## 執行管道

執行管道時，您可以選擇執行管道中的所有工作、手動選取要執行的特定工作、執行含有指定標記的工作，或執行單元測試。

### 執行管道中的所有工作

如要手動執行目前版本的管道，請選取下列其中一個選項：

### 控制台

如要執行管道中的所有工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 依序點選「play\_circle\_filled 執行」>「執行所有工作」。如果您在[驗證](#create_a_pipeline)時選取「Run with my user credentials」(使用我的使用者憑證執行)，則必須[授權給您的 Google 帳戶](#authorize-google-account)。
5. 選用：如要檢查執行作業，請[查看過去的手動執行作業](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw#view-manual-runs)。

### API

**注意：** Dataform API 不支援管道執行的使用者憑證。您必須在管道設定的「Authentication」(驗證) 部分選取服務帳戶，才能使用 API。

如要手動執行 pipeline，請編譯預設工作區，並使用編譯結果建立工作流程叫用。

1. 如要為預設工作區建立編譯結果，請使用 [`projects.locations.repositories.compilationResults.create` 方法](https://docs.cloud.google.com/dataform/reference/rest/v1/projects.locations.repositories.compilationResults/create?hl=zh-tw)。

   使用下列資訊執行 API 要求：

   ```
   curl -X POST \
      -H "Authorization: Bearer $(gcloud auth print-access-token)" \
      -H "Content-Type: application/json" \
      -d '{
         "workspace": "projects/PROJECT_ID/locations/LOCATION/repositories/REPOSITORY_ID/workspaces/default"
      }' \
      "https://dataform.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/repositories/REPOSITORY_ID/compilationResults"
   ```

   更改下列內容：

   * `LOCATION`：存放區的 Google Cloud 區域，例如 `us-central1`。如要查看存放區位置，請前往 Google Cloud 控制台的「Explorer」窗格，選取管道，開啟「設定」分頁，然後點選「在 Dataform 中開啟管道」。位置位於網址中，格式為 `/locations/LOCATION/`。
   * `PROJECT_ID`：Google Cloud 專案的專屬 ID。
   * `REPOSITORY_ID`：Dataform 存放區的專屬 ID，例如 `my-secure-repo`。如要在 Google Cloud 控制台查看存放區 ID，請前往「Explorer」窗格，選取管道，然後開啟「Settings」(設定) 分頁，查看「Dataform repository ID」(Dataform 存放區 ID) 欄位。
2. 在回應主體中，找出 `name` 欄位並複製其值，例如 `projects/my-project/locations/us-central1/repositories/my-repo/compilationResults/12345-67890`。
3. 使用 [`projects.locations.repositories.workflowInvocations.create` 方法](https://docs.cloud.google.com/dataform/reference/rest/v1/projects.locations.repositories.workflowInvocations/create?hl=zh-tw)觸發管道執行作業。

   使用下列資訊執行 API 要求：

   ```
   curl -X POST \
      -H "Authorization: Bearer $(gcloud auth print-access-token)" \
      -H "Content-Type: application/json" \
      -d '{
         "compilationResult": "COMPILATION_RESULT"
      }' \
      "https://dataform.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/repositories/REPOSITORY_ID/workflowInvocations"
   ```

   更改下列內容：

   * `COMPILATION_RESULT`：在上一個步驟中複製的編譯結果完整資源名稱。
   * `LOCATION`：存放區的 Google Cloud 區域，例如 `us-central1`。
   * `PROJECT_ID`：Google Cloud 專案的專屬 ID。
   * `REPOSITORY_ID`：Dataform 存放區的專屬 ID，例如 `my-secure-repo`。

### 執行管道中選取的工作

如要執行管道中的特定工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 依序點選 play\_circle\_filled「Run」>「Select tasks to run」。
5. 在「Run」(執行) 窗格的「Authentication」(驗證) 部分，使用 Google 帳戶或服務帳戶的使用者憑證，授權執行作業。

   * 如要使用 Google 帳戶的使用者憑證，請選取「Run with user credentials」(以使用者憑證執行)。

     ```
     Optional: In the **Extended access options** section, select the
     additional services that your pipeline requires:

     - **Knowledge Catalog**: Allows Google Cloud Knowledge Catalog metadata updates.
     - **Google Drive**: Allows read-only access to Google Drive files.
     - **Bigtable**: Allows read-only access to Google
       Bigtable data.
     ```
   * 如要使用自訂服務帳戶，請選取「Run with selected service account」(以所選服務帳戶執行)，然後選取自訂服務帳戶。

     **注意：** 如要在選單中查看服務帳戶，您必須具備專案層級的 `iam.serviceAccounts.list` 權限，這項權限可透過[檢視服務帳戶角色](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountViewer) (`roles/iam.serviceAccountViewer`) 取得。如果您沒有這項權限，可以按一下「Enter manually」(手動輸入)，然後輸入服務帳戶 ID 來選取服務帳戶。

     如要建立服務帳戶，請按一下「新增服務帳戶」。
6. 確認已選取「Selection of tasks」。
7. 在「Select tasks to run」(選取要執行的工作) 選單中，搜尋特定工作，然後選取要執行的工作。

   「Tasks」(工作) 表格會列出您選取的工作。按一下工作名稱，即可直接在 SQL 編輯器中開啟。
8. 選用：設定下列執行選項：

   * 「Include dependencies」：選取這個選項，即可執行所選工作及其依附元件。
   * **Include dependents**：選取這個選項，即可執行所選工作及其下游轉換附屬元件。
   * 「Run with full refresh」(以全面重新整理的方式執行)：選取這個選項，即可從頭重建所有資料表。
   * **「Run as interactive job with high priority (default)」(以高優先順序執行互動式工作 (預設))**：選取這個選項，即可設定 BigQuery 查詢工作的優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果取消勾選這個選項，系統會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，優先順序較低。
9. 按一下「執行」。如果驗證方式選取「Run with user credentials」(使用使用者憑證執行)，則必須[授權 Google 帳戶](#authorize-google-account) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。
10. 選用：如要檢查執行作業，請[查看過去的手動執行作業](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw#view-manual-runs)。

### 在管道中執行含有指定標記的工作

如要在管道中執行含有指定標記的工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 依序點選 play\_circle\_filled「Run」>「Run by tag」，然後執行下列任一操作：

   * 按一下要執行的標記。
   * 按一下「checklist 選取要執行的標記」。
5. 在「Run」(執行) 窗格的「Authentication」(驗證) 區段中，使用 Google 帳戶或服務帳戶的使用者憑證，授權執行作業。

   * 如要使用 Google 帳戶的使用者憑證，請選取「Run with user credentials」(以使用者憑證執行)。

     ```
     Optional: In the **Extended access options** section, select the
     additional services that your pipeline requires:

     - **Knowledge Catalog**: Allows Google Cloud Knowledge Catalog metadata updates.
     - **Google Drive**: Allows read-only access to Google Drive files.
     - **Bigtable**: Allows read-only access to Google
       Bigtable data.
     ```
   * 如要使用自訂服務帳戶，請選取「Run with selected service account」(以所選服務帳戶執行)，然後選取自訂服務帳戶。

     **注意：** 如要在選單中查看服務帳戶，您必須具備專案層級的 `iam.serviceAccounts.list` 權限，這項權限可透過[檢視服務帳戶角色](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountViewer) (`roles/iam.serviceAccountViewer`) 取得。如果您沒有這項權限，可以按一下「Enter manually」(手動輸入)，然後輸入服務帳戶 ID 來選取服務帳戶。

     如要建立服務帳戶，請按一下「新增服務帳戶」。
6. 確認已選取「選取代碼」。
7. 在「Select tags to run」(選取要執行的標記) 選單中，搜尋特定標記，然後選取要執行的標記。

   「Tasks」(工作) 表格會列出您選取的工作。按一下工作名稱，即可直接在 SQL 編輯器中開啟。
8. 選用：設定下列執行選項：

   * 「Include dependencies」：選取這個選項，即可執行所選工作及其依附元件。
   * **Include dependents**：選取這個選項，即可執行所選工作及其下游轉換附屬元件。
   * 「Run with full refresh」(以全面重新整理的方式執行)：選取這個選項，即可從頭重建所有資料表。
   * **「Run as interactive job with high priority (default)」(以高優先順序執行互動式工作 (預設))**：選取這個選項，即可設定 BigQuery 查詢工作的優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果取消勾選這個選項，系統會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，優先順序較低。
9. 按一下「執行」。如果驗證方式選取「Run with user credentials」(使用使用者憑證執行)，則必須[授權 Google 帳戶](#authorize-google-account) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。
10. 選用：如要檢查執行作業，請[查看過去的手動執行作業](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw#view-manual-runs)。

### 在管道中執行單元測試

如要[在 Dataform 中定義單元測試](https://docs.cloud.google.com/dataform/docs/test-data?hl=zh-tw#unit-tests)，請在存放區的 `definitions/` 目錄中建立 `.sqlx` 測試檔案。在 Dataform 建立單元測試後，可以直接在 BigQuery 管道中執行，根據模擬資料集驗證 SQL 轉換邏輯。

如要在管道中執行單元測試，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下「play\_circle\_filled 執行」。
5. 在「Run」(執行) 窗格的「Authentication」(驗證) 部分，使用 Google 帳戶的使用者憑證或服務帳戶，授權執行作業：

   * 如要使用 Google 帳戶的使用者憑證 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「Run with user credentials」(使用使用者憑證執行)。

     ```
     Optional: In the **Extended access options** section, select the
     additional services that your pipeline requires:

     - **Knowledge Catalog**: Allows Google Cloud Knowledge Catalog metadata updates.
     - **Google Drive**: Allows read-only access to Google Drive files.
     - **Bigtable**: Allows read-only access to Google
       Bigtable data.
     ```
   * 如要使用自訂服務帳戶，請選取「Run with selected service account」(以所選服務帳戶執行)，然後選取自訂服務帳戶。

     如要在選單中查看服務帳戶，您必須具備專案層級的 `iam.serviceAccounts.list` 權限，這項權限可透過[檢視服務帳戶角色](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountViewer) (`roles/iam.serviceAccountViewer`) 取得。如果您沒有這項權限，可以按一下「Enter manually」(手動輸入)，然後輸入服務帳戶 ID，藉此選取服務帳戶。

     如要建立服務帳戶，請按一下「新增服務帳戶」。
6. 在「Execution mode」(執行模式) 部分，選取「Unit tests」(單元測試)。
7. 選取下列其中一個執行範圍選項：

   * **選取單元測試**：搜尋並選取管道中的特定單元測試。
   * **選取單元測試標記**：篩選並執行指派特定標記的單元測試。
   * **所有單元測試**：執行管道中定義的所有單元測試。
8. 選用：在「Execution options」(執行選項) 部分，選取「Execute as interactive job with high priority」(以高優先順序執行互動式工作) 核取方塊，即可立即執行單元測試，優先考量執行速度。

   如未勾選「Execute as interactive job with high priority」(以高優先順序執行互動式工作) 核取方塊，Dataform 預設會使用批次資源執行單元測試，優先節省運算成本。
9. 按一下「執行」。如果驗證方式選取「Run with user credentials」(使用使用者憑證執行)，則必須[授權 Google 帳戶](#authorize-google-account) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。
10. 選用：如要檢查執行作業，請[查看過去的手動執行作業](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw#view-manual-runs)。

### 授權給您的 Google 帳戶

如要使用 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)使用者憑證驗證資源，您必須手動授予權限，讓 BigQuery 管道取得 Google 帳戶的存取權杖，並代表您存取來源資料。您可以使用 OAuth 對話方塊介面手動授予核准。如果選取任何「Extended access options」，就必須授予這些服務的存取權，例如 Google 雲端硬碟或 Knowledge Catalog。

**注意：** 使用 Google 帳戶的使用者憑證執行或排定 BigQuery 管道時，不支援情境感知存取權 (CAA) 政策，包括 IP、地理位置和裝置法規遵循政策，因為權杖要求來自 Google 基礎架構。除非 Dataform OAuth 用戶端 ID [不受政策限制](https://docs.cloud.google.com/dataform/docs/troubleshooting?hl=zh-tw#euc-permission-denied)，否則 CAA 政策會封鎖這些執行作業。

您只需要授予 BigQuery 管道權限一次。

如要撤銷已授予的權限，請按照下列步驟操作：

1. 前往 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)。
2. 按一下「BigQuery Pipelines」。
3. 按一下 [移除存取權]。

**警告：** 撤銷存取權限後，這個 Google 帳戶擁有者在所有區域擁有的管道，日後都無法執行。

如果管道含有筆記本，您也必須手動授予權限，Colab Enterprise 才能取得 Google 帳戶的存取權杖，並代表您存取來源資料。只需授予權限一次。您可以在 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)撤銷這項權限。

## 後續步驟

* 進一步瞭解 [BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)。
* 瞭解如何[管理管道](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw)。
* 瞭解如何[排定管道](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)。
* 瞭解如何[使用 BigQuery Studio Git 存放區管理程式碼](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw)。
* 瞭解如何[使用資料夾整理程式碼資產](https://docs.cloud.google.com/bigquery/docs/code-asset-folders?hl=zh-tw)。
* 瞭解如何[透過單元測試檢驗資料品質](https://docs.cloud.google.com/dataform/docs/test-data?hl=zh-tw#unit-tests)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-28 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-28 (世界標準時間)。"],[],[]]