Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排定管道

本文說明如何排定 [BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)的執行時間，包括如何排定管道執行時間，以及檢查排定的管道執行作業。

管道是由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 支援。
每個管道排程都會使用 Google 帳戶使用者憑證或[自訂服務帳戶](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#about-service-accounts)執行，您可以在設定排程時選取。

您對管道所做的變更會自動儲存，但只有您和專案中獲派 Dataform 管理員角色的使用者可以存取。如要使用新版管道更新排程，請[部署管道](#deploy)。
部署作業會更新排程，改用目前版本的管道。排程一律會執行最新部署的版本。

含有 Notebook 的管道排程會使用[預設執行階段規格](https://docs.cloud.google.com/colab/docs/runtimes?hl=zh-tw#default_runtime_specifications)。在排定執行的管道 (內含筆記本) 期間，BigQuery 會將筆記本輸出內容寫入排程建立期間選取的 [Cloud Storage 值區](https://docs.cloud.google.com/storage/docs/buckets?hl=zh-tw)。

## 事前準備

請先[建立管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。

### 啟用管道排程

如要排定管道執行時間，請將下列角色授予您打算用於管道排程的自訂服務帳戶：

[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)
:   按照「[為服務帳戶授予單一角色](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw#grant-single-role)」一文中的步驟，將服務帳戶新增為自身的主體。換句話說，請將服務帳戶新增為相同服務帳戶的主體。然後將「服務帳戶使用者」角色授予這個主體。

如果管道包含 SQL 查詢，您必須將下列角色授予預計用於管道排程的服務帳戶：

[BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
:   按照「[在專案中授予單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)」一文的說明，在管道讀取資料的專案中，將 BigQuery 工作使用者角色授予服務帳戶。

[BigQuery 資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer) (`roles/bigquery.dataViewer`)
:   按照「[在專案中授予單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)」一文的說明，在管道讀取資料的專案中，將 BigQuery 資料檢視者角色授予服務帳戶。

[BigQuery 資料編輯者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor) (`roles/bigquery.dataEditor`)
:   按照「[在專案中授予單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)」一文的說明，在管道寫入資料的專案中，將 BigQuery 資料編輯者角色授予服務帳戶。

如果管道包含筆記本，您必須將下列角色授予計畫用於管道排程的服務帳戶：

[筆記本執行程式使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.notebookExecutorUser) (`roles/aiplatform.notebookExecutorUser`)
:   按照「[授予專案的單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)」一文的說明，在所選專案中，將 Notebook 執行者使用者角色授予服務帳戶。

[儲存空間管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin) (`roles/storage.admin`)
:   按照「[將主體新增至 bucket 層級政策](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add)」一文的說明，將服務帳戶新增為主體，並指派儲存空間管理員角色。這個主體將用於儲存排定管線執行作業時，所執行筆記本的輸出內容。

此外，您必須將下列角色授予預設的 Dataform 服務代理：

[服務帳戶憑證建立者](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#token-creator-role) (`roles/iam.serviceAccountTokenCreator`)
:   按照「[授予服務帳戶憑證建立存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-token-creation-access)」一文的說明，將預設 Dataform 服務代理新增為服務帳戶的主體，並將「服務帳戶憑證建立者」角色授予這個主體。

[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)
:   按照「[使用 Google Cloud console 授予或撤銷多個 IAM 角色](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw#multiple-roles-console)」一文的說明，在自訂服務帳戶中，將服務帳戶使用者角色授予預設的 Dataform 服務代理程式。

如要進一步瞭解 Dataform 中的服務帳戶，請參閱「[關於 Dataform 中的服務帳戶](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#about-service-accounts)」。

### VPC Service Controls 規定

如果您使用 VPC Service Controls 保護管道，請注意，排定的執行作業是由 Dataform 支援。為排定執行的作業設定 VPC Service Controls 時，請確保符合下列規定：

* 您必須設定[`dataform.restrictGitRemotes`機構政策服務](https://docs.cloud.google.com/dataform/docs/restrict-git-remotes?hl=zh-tw)。
* Dataform 和 BigQuery 必須受限於相同的 VPC Service Controls 服務範圍。
* 如要允許使用者在排定或手動觸發執行作業時，使用 Google 帳戶的使用者憑證進行驗證，請將使用者身分新增至連入規則。詳情請參閱「[更新 service perimeter 的輸入和輸出政策](https://docs.cloud.google.com/vpc-service-controls/docs/configuring-ingress-egress-policies?hl=zh-tw#updating)」和「[輸入規則參考資料](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw#ingress-rules-reference)」。

如需詳細設定步驟和安全性考量事項，請參閱「[為 Dataform 設定 VPC Service Controls](https://docs.cloud.google.com/dataform/docs/vpc-service-controls?hl=zh-tw)」。

### 必要的角色

如要取得管理管道所需的權限，請要求管理員授予您下列 IAM 角色：

* 刪除管道：
  [Dataform 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Admin)  (`roles/dataform.Admin`)
  管道
* 建立、編輯、執行及刪除管道排程：
  + [管道的 Dataform 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Admin)  (`roles/dataform.Admin`)
  + 自訂服務帳戶的[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser)  (`roles/iam.serviceAccountUser`)
* 查看及執行管道：
  專案的 [Dataform 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Viewer)  (`roles/dataform.Viewer`)
* 查看管道排程：專案的 [Dataform 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Editor)  (`roles/dataform.Editor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如要提升排程安全性，請參閱「[實作進階排程權限](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#enhanced-scheduling-permissions)」。

如要進一步瞭解 Dataform IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw)」。

如要在排定管道時使用 Colab 筆記本執行階段範本，您需要「筆記本執行階段使用者」角色 (`roles/aiplatform.notebookRuntimeUser`)。

## 建立管道排程

**提示：** 您也可以使用「管道和連線」頁面，透過[簡化、BigQuery 專屬的工作流程](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw)，排定 Dataform 管道。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要建立管道排程，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「Schedule」(排程)。
5. 在「排定管道」窗格的「排程名稱」欄位中，輸入排程名稱。
6. 在「驗證」部分，使用 Google 帳戶使用者憑證或服務帳戶授權管道。

   * 如要使用 Google 帳戶使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。
7. 如果管道包含筆記本，請在「筆記本選項」部分，選取「執行階段範本」欄位中的 Colaboratory 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。

   **注意：**筆記本執行階段範本必須與管道位於相同區域。**注意：**如果您沒有使用 Colab 筆記本執行階段範本的[必要角色](#required_roles)，仍可使用預設執行階段規格執行及排定管道。
8. 如果管道包含 Notebook，請在「Notebook options」(Notebook 選項) 部分，點選「Cloud Storage bucket」(Cloud Storage bucket) 欄位中的「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket，用於儲存管道中 Notebook 的輸出內容。

   您選取的服務帳戶必須獲得所選 bucket 的 Storage 管理員 IAM 角色。詳情請參閱「[啟用管道排程](#enable-scheduling)」。
9. 在「設定類型」下方，選取「時間表 (以時間為準的週期性)」。
10. 在「排程頻率」下方，執行下列操作：

    1. 在「Repeats」(重複時間間隔) 選單中，選取排定管道執行的頻率。
    2. 在「At time」(時間) 欄位中，輸入排定管道執行的時間。
    3. 在「時區」選單中，選取時間表的時區。
11. 使用「以高優先順序執行互動式工作 (預設)」選項，設定 BigQuery 查詢工作優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果清除這個選項，查詢會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行，優先順序較低。
12. 按一下「建立時間表」。如果選取「使用我的使用者憑證執行」做為驗證方法，您必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

建立排程時，系統會自動部署管道的目前版本。如要使用新版管道更新排程，請[部署管道](#deploy)。

系統會以所選時間和頻率，執行最新部署的管道版本。

**注意：** 如果預定管道執行作業未在下一次預定執行作業開始前完成，系統會略過下一次預定執行作業，並標示為錯誤。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下「建立」，然後從選單中選取「管道時間表」。
3. 在「Schedule pipeline」(排程管道) 窗格中，選取要排程的管道。
4. 在「排程名稱」欄位中，輸入排程名稱。
5. 在「驗證」部分，使用 Google 帳戶使用者憑證或服務帳戶授權管道。

   * 如要使用 Google 帳戶使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。
6. 如果管道包含筆記本，請在「筆記本選項」部分，選取「執行階段範本」欄位中的 Colab 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」一文。

   **注意：**筆記本執行階段範本必須與管道位於相同區域。**注意：**如果您沒有使用 Colab 筆記本執行階段範本的[必要角色](#required_roles)，仍可使用預設執行階段規格執行及排定管道。
7. 如果管道包含筆記本，請在「Cloud Storage bucket」(Cloud Storage bucket) 欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket，用來儲存管道中筆記本的輸出內容。

   您選取的服務帳戶必須獲得所選 bucket 的 Storage 管理員 IAM 角色。詳情請參閱「[啟用管道排程](#enable-scheduling)」。
8. 在「設定類型」下方，選取「時間表 (以時間為準的週期性)」。
9. 在「排程頻率」下方，執行下列操作：

   1. 在「Repeats」(重複時間間隔) 選單中，選取排定管道執行的頻率。
   2. 在「At time」(時間) 欄位中，輸入排定管道執行的時間。
   3. 在「時區」選單中，選取時間表的時區。
10. 使用「以高優先順序執行互動式工作 (預設)」選項，設定 BigQuery 查詢工作優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果清除這個選項，查詢會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行，優先順序較低。
11. 按一下「建立時間表」。如果選取「使用我的使用者憑證執行」做為驗證方法，您必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

**注意：** 如果預定管道執行作業未在下一次預定執行作業開始前完成，系統會略過下一次預定執行作業，並標示為錯誤。

### 授權給您的 Google 帳戶

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [dataform-preview-support@google.com](mailto:dataform-preview-support@google.com)。

如要使用[Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)使用者憑證驗證資源，您必須手動授予 BigQuery 管道權限，才能取得 Google 帳戶的存取權杖，並代表您存取來源資料。您可以使用 OAuth 對話方塊介面手動授予核准。

**注意：** 使用 Google 帳戶的使用者憑證執行或排定 BigQuery 管道時，系統不支援情境感知存取權 (CAA) 政策，包括以 IP 為準、以地理位置為準，以及裝置合規政策，因為權杖要求來自 Google 基礎架構。除非[豁免 Dataform OAuth 用戶端 ID 遵守政策](https://docs.cloud.google.com/dataform/docs/troubleshooting?hl=zh-tw#euc-permission-denied)，否則 CAA 政策會禁止執行這些作業。

您只需要授予 BigQuery 管道一次權限。

如要撤銷授予的權限，請按照下列步驟操作：

1. 前往 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)。
2. 按一下「BigQuery Pipelines」。
3. 按一下 [移除存取權]。

**警告：** 撤銷存取權後，這個 Google 帳戶在所有區域擁有的管道日後都無法執行。

如果新的 Google 帳戶擁有者從未建立過時間表，更新憑證以變更管道時間表擁有者時，也需要手動核准。

如果管道包含筆記本，您也必須手動授予 Colab Enterprise 權限，才能取得 Google 帳戶的存取權杖，並以您的名義存取來源資料。你只需要授予一次權限。你可以在 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)撤銷這項權限。

## 依觸發條件排定時間

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bigquery-event-based-triggers@google.com](mailto:bigquery-event-based-triggers@google.com)。

您可以設定 BigQuery 管道，根據指定 BigQuery 資料表的更新自動觸發執行作業。您可以建立以觸發條件為依據的排程，在 BigQuery 資料變更時自動執行管道，不必採用固定排程。

當管道偵測到指定資料表發生變更時，就會觸發相關聯工作流程的新執行作業。您可以根據單一資料表、一組資料表或一組資料表中的任何資料表的更新來定義條件。

您也可以調整觸發條件式排程的選用設定，控管管道觸發條件之間的最小間隔。舉例來說，您可以調整「最短執行時間」值，確保觸發條件排程的啟動頻率不會超出預期。您也可以調整「最長等待時間」值，確保即使系統未偵測到任何資料表更新，觸發條件式排程也會在該時間內強制啟動一次。

### 限制

觸發條件排程有下列限制：

* 依指定條件觸發的排程不會立即執行。設定以觸發條件為準的排程時，管道大約每 3 分鐘會檢查一次 BigQuery 資料表的狀態。這段時間稱為輪詢間隔，可能會導致表格修改與觸發程序啟動之間出現延遲。
* 在每個輪詢間隔期間，系統會針對每個受監控的資料表，向 BigQuery 發出 API 呼叫。監控大量資料表可能會導致[耗用 BigQuery API 配額](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw#ts-maximum-api-request-limit)。

### 建立觸發條件

如要建立觸發條件，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「觸發條件」。
5. 在「觸發條件」欄位中，輸入觸發條件的名稱。
6. 在「驗證」部分，使用 Google 帳戶使用者憑證或服務帳戶授權管道。

   * 如要使用 Google 帳戶使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。
7. 如果管道包含筆記本，請在「筆記本選項」部分，選取「執行階段範本」欄位中的 Colaboratory 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。

   **注意：**筆記本執行階段範本必須與管道位於相同區域。**注意：**如果您沒有使用 Colab 筆記本執行階段範本的[必要角色](#required_roles)，仍可使用預設執行階段規格執行及排定管道。
8. 如果管道包含 Notebook，請在「Notebook options」(Notebook 選項) 部分，點選「Cloud Storage bucket」(Cloud Storage bucket) 欄位中的「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket，用於儲存管道中 Notebook 的輸出內容。

   您選取的服務帳戶必須獲得所選 bucket 的 Storage 管理員 IAM 角色。詳情請參閱「[啟用管道排程](#enable-scheduling)」。
9. 在「設定類型」下方，選取「觸發條件 (以事件為基礎的執行方式)」。
10. 在「Search tables」(搜尋資料表) 欄位中，新增要監控觸發條件的資料表。
11. 在「觸發條件」下方，選取下列任一選項：

    * **等待「所有」資料表更新**：只有在上次檢查後，所有列出的資料表都已更新時，才會觸發工作流程。
    * **「任意」資料表更新就會觸發**：如果自上次檢查後，清單中的任何資料表有更新，就會觸發這項工作流程。
12. (選用) 輸入「最長等待時間」，如果在這段時間內未偵測到任何資料表更新，系統就會強制啟動觸發程序。支援的值介於 1 秒到 7 天之間。如未指定，工作流程只會在監控的資料表更新時執行，且須符合最短執行時間。
13. (選用) 選取「最短執行時間」，避免觸發條件的啟動頻率高於這個最短時間。支援 3 分鐘到 24 小時之間的值。如未指定，預設值為 3 分鐘。
14. 按一下「建立時間表」。如果選取「使用我的使用者憑證執行」做為驗證方法，您必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

### 排解觸發條件式排程問題

本節說明觸發條件排程的常見問題，以及解決方法。

問題：觸發條件未啟動
:   **解決方法：**請嘗試下列任一步驟：

    * 確認使用者憑證或服務帳戶具備所有[必要權限](#required_roles)。
    * 確認指定的 BigQuery 資料表正在修改中。
    * 確認觸發條件未受到[輪詢間隔](#limitations)影響。
    * 檢查最低執行時間或「最低執行時間」值，是否會導致執行頻率降低。您可以調低這個值，提高觸發條件啟用的頻率。
    * 檢查觸發條件選項 (「全部」或「任一」) 是否會影響觸發條件的啟用。
    * 檢查[稽核記錄](https://docs.cloud.google.com/bigquery/docs/introduction-audit-workloads?hl=zh-tw)，確認 Dataform 嘗試呼叫 BigQuery API 來檢查受監控資料表狀態時是否發生錯誤。

問題：觸發條件的觸發頻率過高
:   **解決方式：**調整執行時間下限，或「執行時間下限」值。您可以增加這個值，降低觸發條件啟用的頻率。

## 部署管道

部署管道時，系統會使用管道的目前版本更新排程。排程會執行最新部署的管道版本。

如要部署管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 點選「Deploy」(部署)。

系統會以目前版本的管道更新對應的排程。
系統會在排定的時間執行最新部署的管道版本。

## 停用時間表

如要暫停所選管道的排定執行作業，但不想刪除排程，可以停用排程。

如要為所選管道停用排程，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「查看時間表」。
5. 在「時間表詳細資料」表格的「時間表狀態」列中，點按「時間表已啟用」切換鈕。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「排程詳細資料」頁面中，按一下「停用」。

## 啟用時間表

如要恢復已停用管道排程的排定執行作業，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「查看時間表」。
5. 在「排程詳細資料」表格的「排程狀態」列中，點選「排程已停用」切換鈕。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「時間表詳細資料」頁面中，按一下「啟用」。

## 手動執行已部署的管道

手動執行已部署的管道時，BigQuery 會執行一次管道，與排定的時間表無關。

如要手動執行已部署的管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道排程的名稱。
3. 在「排程詳細資料」頁面中，按一下「執行」。

## 查看所有管道排程

如要查看專案中的所有管道時間表，請按照下列步驟操作： Google Cloud

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 選用：如要顯示其他資料欄的管道時間表詳細資料，請按一下「資料欄顯示選項」view\_column，然後選取資料欄並按一下「確定」。

## 查看管道排程詳細資料

如要查看所選管道排程的詳細資料，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「查看時間表」。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道排程的名稱。

## 查看過去的排程執行作業

如要查看所選管道排程的過往執行記錄，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「執行」。
5. 選用：如要重新整理過往執行記錄清單，請按一下「重新整理」。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「排程詳細資料」頁面的「過去的執行作業」部分，檢查過去的執行作業。
4. 選用：如要重新整理過往執行記錄清單，請按一下「重新整理」。

## 編輯管道排程

如要編輯管道排程，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「查看時間表」，然後按一下「編輯」。
5. 在「排定管道」對話方塊中編輯排程，然後按一下「更新排程」。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「排程詳細資料」頁面中，按一下「編輯」。
4. 按一下「查看時間表」，然後按一下「編輯」。
5. 在「排定管道」對話方塊中編輯排程，然後按一下「更新排程」。

## 刪除管道排程

如要永久刪除管道排程，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 執行下列任一操作：

   * 按一下所選管道排程的名稱，然後在「排程詳細資料」頁面中，按一下「刪除」。
   * 在包含所選管道排程的資料列中，按一下「Actions」(動作) 欄中的「View actions」(查看動作) more\_vert，然後按一下「Delete」(刪除)。
3. 在隨即出現的對話方塊中，按一下「刪除」。

## 後續步驟

* 進一步瞭解 [BigQuery 中的管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)。
* 瞭解如何[建立管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-06-25 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-06-25 (世界標準時間)。"],[],[]]