Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理已儲存的查詢

本文說明如何管理[已儲存的查詢和傳統版已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw)，以及如何在 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/introduction?hl=zh-tw) 中管理已儲存的查詢的中繼資料。

儲存的查詢是 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 支援的 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 程式碼資產。

## 事前準備

您可以在[遷移](#migrate_classic_saved_queries)、[建立](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#create_saved_queries)或選取 BigQuery Studio 已儲存的查詢時，選擇為遷移的公開或專案傳統版已儲存的查詢設定 IAM 權限，並[授予所選 Identity and Access Management (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#share-saved-query)給該已儲存的查詢。

將公開或專案的傳統已儲存查詢遷移至 BigQuery Studio 已儲存查詢時，請選取 BigQuery Studio 已儲存的查詢，將授予該查詢的權限複製到遷移的已儲存的查詢。

### 必要的角色

如要取得管理已儲存的查詢所需的權限，請要求系統管理員在您要管理已儲存的查詢的專案中，授予下列 IAM 角色：

* 如要在 Google Cloud 控制台中管理 BigQuery Studio 已儲存的查詢：
  + [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
  + [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.readSessionUser)  (`roles/bigquery.readSessionUser`)
  + [程式碼擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeOwner)  (`roles/dataform.codeOwner`)
* 如要使用 BigQuery API 管理 BigQuery Studio 儲存的查詢，請按照下列步驟操作：
  [程式碼擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeOwner)  (`roles/dataform.codeOwner`)
* 如要將專案的傳統已儲存查詢遷移至 BigQuery Studio 已儲存查詢，請按照下列步驟操作：
  [BigQuery Studio 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.studioAdmin)  (`roles/bigquery.studioAdmin`)
* 如要允許[已通過驗證的使用者](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users)查看[公開存取查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#grant-public-access)：
  [程式碼檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeViewer)  (`roles/dataform.codeViewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備管理已儲存查詢所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要管理已儲存的查詢，必須具備下列權限：

* 如要在 Google Cloud 控制台中管理 BigQuery Studio 已儲存的查詢：
   `bigquery.config.get, bigquery.jobs.create, dataform.locations., resourcemanager.projects.get, resourcemanager.projects.list, bigquery.readsessions., dataform.repositories., dataform.workspaces.`
* 如要使用 BigQuery API 管理 BigQuery Studio 已儲存的查詢，請按照下列步驟操作：
   `dataform.locations., dataform.repositories., dataform.workspaces.*, resourcemanager.projects.get, resourcemanager.projects.list`
* 如要將專案的傳統版已儲存查詢遷移至 BigQuery Studio 已儲存查詢，請按照下列步驟操作：
   `bigquery.savedqueries.get, bigquery.savedqueries.list, bigquery.savedqueries.update, bigquery.savedqueries.delete, bigquery.savedqueries.create`
* 如要允許[已驗證的使用者](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users)查看[公開存取查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#grant-public-access)：
   `dataform.locations.*, dataform.repositories.computeAccessTokenStatus, dataform.repositories.fetchHistory, dataform.repositories.fetchRemoteBranches, dataform.repositories.get, dataform.repositories.getIamPolicy, dataform.repositories.list, dataform.repositories.queryDirectoryContents, dataform.repositories.readFile, dataform.workspaces.fetchFileDiff, dataform.workspaces.fetchFileGitStatuses, dataform.workspaces.fetchGitAheadBehind. dataform.workspaces.get, dataform.workspaces.getIamPolicy, dataform.workspaces.list, dataform.workspaces.queryDirectoryContents, dataform.workspaces.readFile, dataform.workspaces.searchFiles, resourcemanager.projects.get, resourcemanager.projects.list`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」一文。

如要在 Knowledge Catalog 中管理已儲存的查詢中繼資料，請確認您具備必要的 [Knowledge Catalog 角色](https://docs.cloud.google.com/dataplex/docs/iam-roles?hl=zh-tw)和 [`dataform.repositories.get`](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#predefined-roles) 權限。

## 共用已儲存的查詢

如要與使用者共用已儲存的查詢，請先授予該使用者已儲存查詢的存取權，並將他們新增至適當的 IAM 角色。然後產生已儲存的查詢的連結，並與使用者共用該連結。

與您共用查詢的使用者只會看到最新版本的查詢。
系統不會在共用查詢中顯示自動儲存但您未明確儲存的變更。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
4. 找出並點選要授予存取權的已儲存查詢。您可以使用搜尋功能或篩選器尋找查詢。
5. 依序點按「共用」person\_add和「管理權限」。
6. 在「管理權限」窗格中，按一下「新增使用者/群組」。
7. 在「New principals」(新增主體) 欄位中輸入主體。
8. 在「Role」(角色) 清單中，選取下列其中一個角色：

   * [**程式碼擁有者**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner)：可以對已儲存的查詢執行任何動作，包括刪除或共用查詢。
   * [**程式碼編輯器**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor)：可編輯查詢。
   * [**程式碼檢視者**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer)：可以查看查詢。**注意：** 主體也必須具備 [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user) 角色，才能執行已儲存的查詢。
9. 選用：如要查看完整的角色清單和進階共用設定，請按一下「進階共用設定」。
10. 按一下 [儲存]。
11. 如要返回已儲存的查詢資訊，請按一下「關閉」。
12. 如要產生已儲存的查詢的連結，請按一下「分享」圖示 person\_add，然後按一下「取得連結」。

    連結即會複製到剪貼簿。

## 授予已儲存的查詢公開存取權

如要授予 `allAuthenticatedUsers` 主體已儲存的 BigQuery Studio 查詢公開存取權，請授予該主體已儲存的查詢的程式碼檢視者 ([roles/dataform.codeViewer](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer)) 角色。

將 IAM 角色指派給`allAuthenticatedUsers`主體後，透過 Google 帳戶完成驗證的服務帳戶和所有使用者都會獲得該角色。這包括未連結至 Google Workspace 帳戶或 Cloud Identity 網域的帳戶，例如個人 Gmail 帳戶。未通過驗證的使用者 (如匿名訪客) 不會具有這個識別碼。詳情請參閱「[所有已驗證的使用者](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users)」。

舉例來說，如果您在`sales`已儲存的查詢中，將「程式碼檢視者」角色授予 `allAuthenticatedUsers`，那麼網際網路上所有已透過 Google 帳戶完成驗證的服務帳戶和使用者，都將擁有`sales`已儲存查詢的唯讀存取權。

**注意：** 如果將管理員、編輯或執行層級的權限授予 `allAuthenticatedUsers`，惡意行為者可能會存取您的資料。只授予最低必要權限。

如要授予 BigQuery Studio 已儲存的查詢的公開存取權，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
4. 找出並按一下要授予公開存取權的已儲存的查詢。您可以使用搜尋功能或篩選器來尋找查詢。
5. 按一下已儲存的查詢旁的 more\_vert「查看動作」**，然後依序點選「共用」>「管理權限」**。
6. 在「管理權限」窗格中，按一下「新增使用者/群組」。
7. 在「New principals」(新增主體) 欄位中輸入 `allAuthenticatedUsers`。
8. 在「Role」(角色) 清單中，選取「Code Viewer」(程式碼檢視者) 角色。
9. 按一下 [儲存]。
10. 如要返回已儲存的查詢資訊，請按一下「關閉」。

## 禁止公開存取已儲存的查詢

為確保任何 BigQuery Studio 已儲存的查詢都不會授予公開存取權，請限制專案中的 `allAuthenticatedUsers` 主體。

如要在專案中限制 `allAuthenticatedUsers`，您可以[設定 `iam.allowedPolicyMemberDomains` 政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-domains?hl=zh-tw#setting_the_organization_policy)，並從 `allowed_values` 清單中移除 `allAuthenticatedUsers`。

在`iam.allowedPolicyMemberDomains`政策中限制 `allAuthenticatedUsers` 後，專案中的任何 IAM 政策都無法使用 `allAuthenticatedUsers` 主體，因此無法授予所有資源 (包括 BigQuery Studio 已儲存查詢) 公開存取權。

如要進一步瞭解 `iam.allowedPolicyMemberDomains` 政策及設定方式，請參閱「[依照網域設定身分限制](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-domains?hl=zh-tw)」。

## 設定程式碼資產的預設區域

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

## 查看所有已儲存的查詢

如要查看專案中所有已儲存的查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，點選「Queries」旁邊的「View actions」more\_vert，然後執行下列其中一項操作：

* 如要在目前的分頁中開啟清單，請按一下「顯示全部」。
* 如要在新分頁中開啟清單，請依序點選「顯示全部」 >「新分頁」。
* 如要在分割分頁中開啟清單，請依序點選「顯示所有項目」 >「分割分頁」。

## 查看已儲存的查詢中繼資料

如要查看已儲存的查詢的中繼資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
4. 找出並點選要查看中繼資料的已儲存的查詢。
5. 按一下「資訊」**詳細資料**，即可查看已儲存的查詢的相關資訊，例如使用的[區域](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#supported_regions)和上次修改日期。

## 使用已儲存的查詢版本

您可以選擇在[存放區](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw)內或外部建立已儲存的查詢。系統會根據已儲存查詢的位置，以不同方式處理已儲存查詢的版本管理。

### 存放區中已儲存的查詢版本管理

存放區是位於 BigQuery 或第三方供應商的 Git 存放區。您可以在存放區中使用「工作區」，對儲存的查詢執行版本控管。詳情請參閱「[使用檔案的版本管控功能](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw#use_version_control_with_a_file)」。

### 在存放區外部儲存查詢版本

請參閱下列各節，瞭解如何查看、比較及還原已儲存的查詢版本。

#### 查看已儲存的查詢版本

如要查看已儲存的查詢版本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
4. 按一下要查看版本記錄的已儲存查詢名稱。
5. 按一下「版本記錄」history，即可查看已儲存的查詢版本清單，並依日期降序排列。

#### 比較已儲存的查詢版本

如要比較已儲存的查詢版本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
4. 按一下要比較版本資訊的已儲存的查詢名稱。
5. 按一下 history「版本記錄」。
6. 按一下已儲存的查詢版本旁的 more\_vert「查看動作」，然後點選「比較」。比較窗格隨即開啟，比較您選取的已儲存的查詢版本與目前的查詢。
7. 選用：目前的查詢也會顯示自動儲存的變更。如要明確儲存這些變更，請按一下「覆寫」。
8. 選用：如要改為在同一窗格中比較版本，請依序點按「比較」和「內嵌」。

#### 還原已儲存的查詢版本

從比較窗格還原時，您可以先比較已儲存查詢的先前版本與目前版本，再選擇是否要還原。

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
3. 按一下要還原舊版的已儲存的查詢名稱。
4. 按一下 history「版本記錄」。
5. 按一下要還原的已儲存的查詢版本旁的 more\_vert「查看動作」，然後按一下「比較」。比較窗格隨即開啟，比較您選取的已儲存的查詢版本與最新查詢版本，包括任何自動儲存的變更。
6. 如要在比較後還原先前的已儲存的查詢版本，請按一下 **還原**。
7. 按一下「確認」。

## 在連結試算表中開啟已儲存的查詢

如要在連結試算表開啟已儲存的查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
   找出要在連結試算表開啟的已儲存的查詢。
4. 按一下已儲存的查詢旁的 more\_vert「開啟動作」，然後依序點選「開啟方式」「連結試算表」。

   或者，按一下已儲存的查詢名稱，在詳細資料窗格中開啟查詢，然後按一下「在 **> 已連結的試算表**中開啟」。

## 下載已儲存的查詢

如要下載已儲存的查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
4. 按一下已儲存的查詢名稱即可開啟。
5. 點選 [下載]。

## 刪除已儲存的查詢

如要刪除已儲存的查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
4. 找出要刪除的已儲存的查詢。
5. 按一下已儲存的查詢旁的 more\_vert「開啟動作」，然後按一下「刪除」。
6. 如要確認刪除，請在對話方塊中輸入 `delete`。
7. 點選「刪除」。

## 傳統版已儲存查詢

**已淘汰：** [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/enable-assets?hl=zh-tw) 中的已儲存查詢功能，日後將完全取代傳統的已儲存查詢功能。我們正在審查淘汰時程。詳情請參閱[傳統版已儲存查詢的淘汰事宜](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#classic-saved-queries-deprecation)。
如要瞭解如何遷移至已儲存的查詢，請參閱「[遷移傳統版已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#migrate_classic_saved_queries)」一文。

請參閱下列各節，瞭解如何管理[傳統儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#classic_saved_queries)。

****注意：** 如果尚未啟用 BigQuery Studio，傳統版儲存的查詢會顯示在「傳統版探索器」窗格的「已儲存的查詢」**NUMBER**資料夾中，而不是「(傳統版) 查詢」資料夾。**

### 共用傳統版已儲存的查詢

您可以共用已設為專案或公開瀏覽權限的傳統版已儲存查詢。專案層級瀏覽權限可讓具備[必要權限](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#required_permissions_for_classic_saved_queries)的主體檢視、更新或刪除查詢。公開瀏覽權限可讓擁有查詢連結的任何人查看查詢，但無法更新或刪除查詢。

如要與其他使用者共用傳統版已儲存的查詢，請產生並分享傳統版已儲存查詢的連結。

如要執行傳統共用查詢，使用者必須能存取查詢所存取的資料。詳情請參閱「[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)」。

如果您打算共用傳統版已儲存的查詢，請考慮在查詢中加入說明其用途的註解。

1. 點選左側窗格中的「類別」「傳統版 Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「傳統版 Explorer」窗格中展開專案，按一下「(傳統版) 查詢」，然後找出要共用的傳統版已儲存的查詢。
3. 按一下查詢旁的 more\_vert「查看動作」，然後點選「取得連結」。
4. 將連結分享給要授予查詢存取權的使用者。

### 將傳統版查詢儲存為已儲存的查詢

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的「類別」「傳統版 Explorer」：
3. 在「傳統版 Explorer」窗格中，展開專案和「(傳統版) 查詢」資料夾，以及「專案查詢」資料夾 (如有需要)。
4. 按一下已儲存的傳統查詢名稱即可開啟。
5. 依序點按 「儲存查詢 (舊版)」**>「將查詢另存為...」**。
6. 在「儲存查詢」對話方塊中輸入名稱，然後選擇查詢的位置。
7. 按一下 [儲存]。

### 遷移傳統版已儲存的查詢

如要批次遷移傳統版已儲存查詢，您必須具備[必要角色](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#required_roles)。這些角色授予的權限會決定可遷移的傳統版已儲存查詢類型。

您可以批次遷移下列傳統版已儲存查詢：

個人傳統版已儲存查詢
:   只有建立者才能看到個人傳統版已儲存查詢。這類項目會標示 person 圖示。個人儲存的傳統查詢只能由擁有者遷移。

公開的傳統版已儲存查詢
:   擁有查詢連結的任何人都可看到公開的傳統版已儲存查詢。這類項目會標示 share 圖示。只有擁有者才能遷移傳統版公開已儲存查詢。

    公開傳統儲存查詢的 IAM 權限不會對應至 BigQuery Studio 儲存查詢的權限。也就是說，從公開傳統儲存查詢遷移的 BigQuery Studio 儲存查詢，預設不會公開。您必須在遷移期間或之後，為遷移的 BigQuery Studio 已儲存查詢設定 IAM 權限。

    如要在遷移期間為遷移的 BigQuery Studio 已儲存的查詢設定 IAM 權限，您可以選取現有的 BigQuery Studio 已儲存的查詢，並將其權限套用至遷移的已儲存的查詢。BigQuery 會複製所選 BigQuery Studio 已儲存的查詢的權限，並套用至遷移的已儲存的查詢。您也可以手動新增要共用已遷移儲存查詢的使用者或群組。

    如果您在遷移期間未設定 IAM 權限，只有您能存取遷移的 BigQuery Studio 已儲存查詢。

專案傳統版已儲存查詢
:   凡是擁有[必要權限](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#required_permissions_for_classic_saved_queries)的主體，都能看到專案層級的儲存查詢。這類檔案會以 people 圖示表示。您可以批次遷移專案中的所有傳統版已儲存查詢。

    專案傳統儲存查詢的 IAM 權限，不會直接對應至 BigQuery Studio 儲存查詢的權限。您必須在遷移期間或遷移後，為遷移的 BigQuery Studio 已儲存查詢設定 IAM 權限。

    如要在遷移期間為遷移的 BigQuery Studio 已儲存的查詢設定 IAM 權限，您可以選取現有的 BigQuery Studio 已儲存的查詢，並將其權限套用至遷移的已儲存的查詢。BigQuery 會複製所選 BigQuery Studio 已儲存的查詢的權限，並套用至遷移的已儲存的查詢。您也可以手動新增要共用已遷移儲存查詢的使用者或群組。

    如果您在遷移期間未設定 IAM 權限，只有您能存取遷移的 BigQuery Studio 已儲存查詢。

批次遷移傳統版已儲存查詢時，BigQuery 會執行下列操作：

* 將所有要遷移的傳統版已儲存查詢儲存為 BigQuery Studio 已儲存查詢，並儲存在所選區域中。
* 將所有遷移的傳統版已儲存查詢轉換為唯讀傳統版已儲存查詢。

遷移後，您可將個人、公開和專案的傳統已儲存查詢，做為 BigQuery Studio 已儲存查詢和唯讀傳統已儲存查詢存取。

#### 遷移風險

批次遷移後，您將無法修改遷移的傳統已儲存查詢。遷移後，您儲存的個人、公開和專案傳統版查詢會變成唯讀。

BigQuery 會使用 Dataform API，將遷移的 BigQuery Studio 已儲存查詢新增至您的 Google Cloud 專案。如要還原這些變更，必須手動清理。

**警告：** 遷移作業一旦開始，便無法停止或取消。

#### 批次遷移傳統版已儲存查詢

如要將專案中的傳統已儲存查詢批次遷移至 BigQuery Studio 已儲存查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的「類別」「傳統版 Explorer」：
3. 在「傳統版 Explorer」窗格中，展開專案並依序點選「(傳統版) 查詢」旁的「查看動作」圖示 more\_vert 和「遷移傳統版已儲存的查詢」。
4. 在「傳統版已儲存查詢遷移作業」窗格的「檢查遷移準備狀態」部分，按一下「下一步」，確認您具備[必要角色](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#required_roles)。

   IAM 權限會決定您可以遷移哪種傳統版已儲存查詢，以及**傳統版已儲存查詢遷移作業**窗格中可見的部分。
5. 在「區域」部分中，從「區域」下拉式選單選取區域，BigQuery 會將遷移的已儲存查詢儲存在該區域。

   建議您選取 BigQuery Studio 程式碼資產的預設區域。詳情請參閱「[設定預設區域](#set-default-region)」。
6. 如要遷移所有個人傳統版已儲存的查詢，請在「遷移個人查詢」部分中，選取「遷移所有個人查詢」核取方塊，然後按一下「下一步」。
7. 如要遷移專案中的所有傳統版公開查詢，請在「遷移公開查詢」部分中執行下列操作：

   1. 勾選「遷移所有公開查詢」核取方塊。
   2. 在「SQL」下拉式選單中，選取具有 IAM 政策的 BigQuery Studio 已儲存的查詢，並將這些政策套用至已遷移的已儲存的查詢。
   3. 選用：如要新增要與之共用已遷移儲存查詢的使用者或群組，請按一下「新增使用者/群組」。

      如要公開分享已遷移的已儲存查詢，請將 `allAuthenticatedUsers` 設為主體，並授予程式碼檢視者角色。詳情請參閱「[授予公開存取權](#grant-public-access)」。
   4. 點選「下一步」。
8. 如要遷移專案層級的傳統版儲存查詢，請在「遷移專案查詢」部分中執行下列操作：

   1. 選取「遷移所有專案查詢」核取方塊。
   2. 在「SQL」下拉式選單中，選取 BigQuery Studio 已儲存的查詢，其中含有要套用至已遷移已儲存查詢的 IAM 政策。
   3. 選用：如要新增要與之共用已遷移儲存查詢的使用者或群組，請按一下「新增使用者/群組」。
   4. 點選「下一步」。
9. 如要確認您瞭解[遷移作業的風險](#migration-risks)，並要批次遷移傳統已儲存查詢，請在「Confirm」(確認) 區段的「Confirm」(確認) 欄位中輸入 `confirm`，然後按一下「Next」(下一步)。

   **警告：** 遷移作業一旦開始，便無法停止或取消。
10. 按一下「提交」。

視要遷移的查詢數量而定，遷移作業可能需要超過 15 分鐘。

### 刪除傳統版已儲存的查詢

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的「類別」「傳統版 Explorer」：
3. 在「傳統版 Explorer」窗格中，展開專案和「(傳統版) 查詢」資料夾，以及「專案查詢」資料夾 (如有需要)。
4. 找出要刪除的傳統已儲存的查詢。
5. 按一下查詢旁的 
   more\_vert 「查看動作」，然後按一下「刪除」。
6. 如要確認刪除，請在對話方塊中輸入 `delete`。
7. 點選「刪除」。

## 管理 Knowledge Catalog 中的中繼資料

您可以使用 Knowledge Catalog 儲存及管理已儲存查詢的中繼資料。根據預設，Knowledge Catalog 會提供已儲存的查詢，不需額外設定。

您可以使用 Knowledge Catalog 管理所有[已儲存查詢位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)中的已儲存的查詢。在 Knowledge Catalog 中管理已儲存的查詢時，須遵守 [Knowledge Catalog 配額和限制](https://docs.cloud.google.com/dataplex/docs/quotas?hl=zh-tw)，以及 [Knowledge Catalog 定價](https://cloud.google.com/dataplex/pricing?hl=zh-tw)。

Knowledge Catalog 會自動從已儲存的查詢中擷取下列中繼資料：

* 資料資產名稱
* 資料資產父項
* 資料資產位置
* 資料資產類型
* 對應 Google Cloud 專案

Knowledge Catalog 會將儲存的查詢記錄為[項目](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entries)，並包含下列項目值：

系統項目群組
:   已儲存查詢的[系統項目群組](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-groups)為 `@dataform`。如要查看 Knowledge Catalog 中已儲存的查詢項目的詳細資料，請查看 `dataform` 系統項目群組。如需查看項目群組中所有項目的清單，請參閱 Knowledge Catalog 說明文件中的「[查看項目群組的詳細資料](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-group-details)」。�

系統項目類型
:   已儲存查詢的[系統項目類型](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-types)為 `dataform-code-asset`。[如要查看已儲存查詢的詳細資料，您需要查看 `dataform-code-asset` 系統項目類型、使用切面式篩選器篩選結果，並將 `dataform-code-asset` 切面內的 `type` 欄位設為 `SQL_QUERY`](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)。
    然後選取所選已儲存查詢的項目。如要瞭解如何查看所選項目類型的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目類型的詳細資料](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-type-details)」。如需查看所選項目詳細資料的操作說明，請參閱 Knowledge Catalog 說明文件中的「[查看項目的詳細資料](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-tw#view-entry-details)」一節。

系統切面類型
:   已儲存查詢的[系統切面類型](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw#aspect-types)為 `dataform-code-asset`。如要透過註解資料儲存的查詢項目[切面](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw#aspects)，在 Knowledge Catalog 中為已儲存的查詢提供額外背景資訊，請查看 `dataform-code-asset` 切面類型、使用以切面為準的篩選器篩選結果，並[將 `dataform-code-asset` 切面內的 `type` 欄位設為 `SQL_QUERY`](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)。如需如何使用切面註解項目的操作說明，請參閱 Knowledge Catalog 說明文件中的「[管理切面及豐富中繼資料](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw)」一文。

類型
:   已儲存查詢的類型為 `SQL_QUERY`。您可以使用`aspect:dataplex-types.global.dataform-code-asset.type=SQL_QUERY``dataform-code-asset``dataform-code-asset`[以切面為準的篩選器](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)，依系統項目類型和切面類型篩選已儲存的查詢。

如需在 Knowledge Catalog 中搜尋資產的操作說明，請參閱 Knowledge Catalog 說明文件中的「[在 Knowledge Catalog 中搜尋資料資產](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-tw)」。

## 後續步驟

* 如要進一步瞭解 BigQuery Studio 已儲存的查詢，請參閱「[已儲存的查詢簡介](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw) 」。
* 如要瞭解如何建立已儲存的查詢，請參閱[建立已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]