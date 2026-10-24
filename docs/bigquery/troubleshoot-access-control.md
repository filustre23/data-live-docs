Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排解存取控管問題

本文說明如何排解 BigQuery 中 Identity and Access Management (IAM) 權限、資料欄層級存取控管和客戶自行管理的加密金鑰 (CMEK) 的安全性問題。IAM 權限問題通常會導致 `Access Denied` 錯誤，如下所示：

* `Access Denied: Project PROJECT_ID:
  User does not have bigquery.jobs.create permission in project
  PROJECT_ID.`
* `Access Denied: Project PROJECT_ID:
  User does not have bigquery.datasets.get permission on dataset
  DATASET.`
* `User does not have permission to query table
  PROJECT_ID:DATASET.TABLE.`
* `Access Denied: Table PROJECT_ID:DATASET.TABLE:
  User does not have permission to query table
  PROJECT_ID:DATASET.TABLE, or perhaps it
  does not exist.`
* `Access Denied: User PRINCIPAL does
  not have permission to perform bigquery.tables.getData on resource
  'projects/PROJECT_ID/datasets/DATASET/tables/TABLE'.`

## 事前準備

* 如要排解主體存取 BigQuery 資源的問題，請確認您具備[必要的 IAM 權限](https://docs.cloud.google.com/policy-intelligence/docs/troubleshoot-access?hl=zh-tw#required-permissions)。

## 收集問題相關資訊

排解資源存取問題的第一步，是判斷缺少的權限、存取遭拒的 IAM 主體，以及主體嘗試存取的資源。

### 從錯誤或工作記錄中取得資訊

如要取得主體、資源和權限的相關資訊，請查看 bq 指令列工具的輸出內容、API 回應，或 Google Cloud 控制台中的 BigQuery。

舉例來說，如果您嘗試在權限不足的情況下執行查詢， Google Cloud 控制台「Query results」(查詢結果) 專區的「Job information」(工作資訊) 分頁會顯示類似下方的錯誤。

檢查錯誤，判斷主體、資源和權限。

**注意：** 您也可以使用[工作記錄](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)查看工作詳細資料。

在某些情況下，您可以直接透過錯誤訊息要求缺少的權限。詳情請參閱 IAM 說明文件中的「[權限錯誤訊息](https://docs.cloud.google.com/iam/docs/permission-error-messages?hl=zh-tw)」。

### 從 Cloud 稽核記錄取得資訊

如果錯誤訊息是一般訊息、缺少資訊，或是在背景程序中執行動作失敗，請使用 Cloud 稽核記錄的 Logs Explorer，取得錯誤相關資訊。

1. 前往 Google Cloud 控制台的「Logs Explorer」頁面。

   [前往 Logs Explorer](https://console.cloud.google.com/logs/query?hl=zh-tw)

   或者，您也可以從導覽選單中依序選擇**「Monitoring」 >
   「Logs Explorer」**。
2. 在 Logs Explorer 中，選取「專案記錄」做為記錄範圍。
3. 在查詢視窗中輸入下列查詢，從 BigQuery 資料存取記錄取得權限相關錯誤：

   ```
   resource.type="bigquery_resource" AND
   logName="projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Fdata_access" AND
   protoPayload.status.message:"Access Denied" OR
   protoPayload.status.message:"Permission denied" OR
   protoPayload.status.code=7
   ```

   將 PROJECT\_ID 替換為專案 ID。
4. 在查詢結果中，展開失敗作業對應的記錄項目。
5. 在 `protoPayload` 區段中，展開 `authorizationInfo` 陣列，然後展開 `authorizationInfo` 陣列中的每個節點。

   `authorizationInfo` 陣列會顯示 API 呼叫期間執行的每項權限檢查。
6. 如要查看錯誤原因，請找出 `granted: false` 項目。`granted: false` 項目會顯示下列資訊：

   * `permission`：檢查的 IAM 權限字串。例如：`bigquery.tables.getData`。
   * `resource`：主體嘗試存取的資源完整名稱。例如：`projects/myproject/datasets/mydataset/tables/mytable`。
   * `principalEmail` (如有)：`protoPayload.authenticationInfo` 中參照的主體，即嘗試執行動作的主體。

**注意：** 如需其他 BigQuery 稽核記錄範例查詢，請前往 Google Cloud Observability 的 [**範例查詢** 頁面](https://docs.cloud.google.com/logging/docs/view/query-library?hl=zh-tw#bigquery-filters)。

## 使用允許政策的政策分析工具

允許政策的政策分析工具可讓您根據 [IAM 允許政策](https://docs.cloud.google.com/iam/docs/policies?hl=zh-tw)，找出哪些 [IAM 主體](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw)具備哪些 BigQuery 資源的哪些存取權。

**注意：** Policy Intelligence 也提供 [IAM 政策疑難排解工具](https://docs.cloud.google.com/policy-intelligence/docs/troubleshoot-access?hl=zh-tw)，可協助您排解特定主體的存取權問題。

收集權限錯誤的相關資訊後，您可以使用政策分析工具，瞭解主體為何缺少必要存取權。這項工具會分析所有相關政策、Google 群組成員資格，以及從上層資源 (例如專案、資料夾和組織) 繼承的權限。

如要使用政策分析工具分析允許政策，請建立分析查詢、指定分析範圍，然後執行查詢。

1. 前往 Google Cloud 控制台的「政策分析工具」頁面。

   [前往政策分析工具](https://console.cloud.google.com/iam-admin/analyzer?hl=zh-tw)

   或者，您也可以從導覽選單中，依序選擇**「IAM & Admin」(IAM 與管理) >
   「Policy Analyzer」(政策分析工具)**。
2. 按一下「建立自訂查詢」。
3. 在「Configure your query」(設定查詢) 頁面中，輸入先前收集的資訊：

   1. 在「Select the scope」(選取範圍) 區段的「Select query scope」(選取查詢範圍) 欄位中，確認目前專案是否顯示，或按一下「Browse」(瀏覽) 選擇其他資源。
   2. 在「Set the query parameters」(設定查詢參數) 專區中，針對「Parameter 1」(參數 1) 選擇「Principal」(主體)，然後在「Principal」(主體) 欄位中輸入使用者、群組或服務帳戶的電子郵件地址。
   3. 按一下「add 新增參數」。
   4. 在「Parameter 2」(參數 2) 中選擇「Permission」(權限)，然後在「Permission」(權限) 欄位中按一下「Select」(選取)，選擇 BigQuery 權限，然後按一下「Add」(新增)。例如，選取 **`bigquery.tables.getData`**。
   5. 按一下「add 新增參數」。
   6. 在「Parameter 3」(參數 3) 中，選擇「Resource」(資源)，然後在「Resource」(資源) 欄位中輸入完整資源名稱。資源名稱必須包含服務前置字串，如以下範例所示：

      * **BigQuery 專案**：
        `//cloudresourcemanager.googleapis.com/projects/PROJECT_ID`
      * **BigQuery 資料集**：`//bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET`
      * **BigQuery 資料表**：
        `//bigquery.googleapis.com/projects/PROJECT/datasets/DATASET/tables/TABLE`
4. 在「**自訂查詢**」窗格中，依序點選**「分析」>「執行查詢」**。
5. 查看查詢結果。結果可能是下列其中一項：

   * **空白清單**。如果沒有結果，代表主體不具備必要權限。您必須[授予主體角色](#find-role)，提供正確權限。
   * **一或多個結果**。如果分析工具找到允許政策，代表存在某種形式的存取權。按一下每項結果的「View Binding」(查看繫結)，即可查看提供主體所屬資源存取權的角色。政策繫結會顯示存取權是透過群組成員資格或繼承授予，還是遭到 [IAM 條件](https://docs.cloud.google.com/bigquery/docs/conditions?hl=zh-tw)或 [IAM 拒絕政策](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#deny_access_to_a_resource)拒絕。

## 找出可授予必要權限的正確 IAM 角色

確認主體沒有足夠的存取權後，下一步是找出適當的預先定義或自訂 IAM 角色，授予必要權限。選擇角色時，應遵循最小權限原則。

如果貴組織使用自訂角色，您可以[列出在專案或組織中建立的所有自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw#roles-list)，找出正確的角色。舉例來說，在 Google Cloud 控制台的「Roles」(角色) 頁面中，您可以依「Type:Custom」(類型：自訂) 篩選清單，只查看自訂角色。

如要找出正確的預先定義 IAM 角色，請按照下列步驟操作。

1. 開啟 BigQuery IAM 角色和權限頁面的「[BigQuery 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)」部分。
2. 在「Enter a permission」(輸入權限) 搜尋列中，輸入從錯誤訊息、工作記錄或稽核記錄中擷取的權限。例如：`bigquery.tables.getData`。

   搜尋結果會顯示所有預先定義的 BigQuery 角色，這些角色會授予該權限。
3. 套用最小權限原則：在角色清單中，選擇可授予必要權限的最嚴格角色。舉例來說，如果您搜尋 `bigquery.tables.getData`，想授予查詢資料表資料的能力，則「BigQuery 資料檢視者」就是授予該權限的最低權限角色。
4. 為該主體授予適當角色。如要瞭解如何將 IAM 角色授予 BigQuery 資源，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

## 未接受《BigQuery 服務條款》

錯誤字串：`BigQuery Terms of Service have not been accepted`

如果未接受《BigQuery 服務條款》，就會發生這個 HTTP `403 Forbidden` 錯誤 (`reason: termsOfServiceNotAccepted`)。這個錯誤並非缺少 IAM 權限所致。建立資料集或載入資料等要求可能會傳回這項錯誤。

請按照下列步驟解決這個問題：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如果出現歡迎頁面，請選取國家/地區，勾選「Terms of Service」(服務條款) 核取方塊，然後按一下「Agree and continue」(同意並繼續)。詳情請參閱「[啟用 BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw#setup)」。

接受《服務條款》後，請重試要求。

## 排解違反政策錯誤

在 BigQuery 中收到 HTTP `403 PERMISSION_DENIED` 錯誤，且錯誤原因為 `policyViolation` 時，表示失敗是由組織政策、資料 perimeter 或 VPC Service Controls 造成。

以下各節說明與這項錯誤原因相關的最常見錯誤訊息、原因和解決方法。

### 依據機構政策的規定，您無法提出要求

錯誤字串：
`VPC Service Controls: Request is prohibited by organization's policy.
vpcServiceControlsUniqueIdentifier:
VPC_SERVICE_CONTROLS_UNIQUE_IDENTIFIER`

#### 診斷

您的要求來自指定 VPC Service Controls perimeter 以外的網路位址或用戶端，或違反工作區定義的輸入和輸出規則。如果查詢橫跨多項專案，就經常會發生這種情況。例如，查詢計費專案位於資料專案的安全 perimeter 之外。

#### 解析度

1. **找出專屬 ID。**擷取錯誤訊息中的 `vpcServiceControlsUniqueIdentifier`。使用這個 ID 篩選 Google CloudLogs Explorer，找出對應的 VPC Service Controls 記錄，查看詳細原因：

   ```
   protoPayload.metadata.@type="type.googleapis.com/google.cloud.audit.VpcServiceControlAuditMetadata"
   protoPayload.metadata.vpcServiceControlsUniqueId="VPC_SERVICE_CONTROLS_UNIQUE_IDENTIFIER"
   ```

   在 `protoPayload.metadata.violationReason` 下方尋找 `violationReason` 值。找出問題後，請研究記錄項目中的其他詳細資料，並按照現有的 [VPC Service Controls 疑難排解指南](https://docs.cloud.google.com/vpc-service-controls/docs/troubleshooting?hl=zh-tw#debugging)操作。此外，建議您使用[違規分析工具](https://docs.cloud.google.com/vpc-service-controls/docs/violation-analyzer?hl=zh-tw)。
2. **修正跨專案計費問題。**如果是跨專案查詢，請確保執行查詢的計費專案與查詢的資料位於 perimeter 內的相同 perimeter。如有需要，請使用 Google Cloud 控制台專案挑選器、bq 指令列工具中的 [`--project_id` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#project_id_flag)，或 [API 或用戶端程式庫要求](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)，手動指定符合規定的計費專案。
3. **驗證存取層級。**請使用 [Access Context Manager](https://docs.cloud.google.com/access-context-manager/docs/overview?hl=zh-tw)，確認用戶端網路、IP 或使用者帳戶已獲准使用。Google Cloud 控制台需要特別設定輸入規則，允許使用者存取受保護的環境。

### 如果專案已啟用 VPC Service Controls，就無法匯出至 Google 雲端硬碟

錯誤字串：
`Export to Google Drive is blocked for projects with VPC-SC enabled`

#### 診斷

Google 雲端硬碟不支援 VPC Service Controls。由於 Google 雲端硬碟無法強制執行安全範圍，BigQuery 會自動停用將 API 擷取內容匯出至 Google 雲端硬碟的功能，適用於源自 VPC Service Controls 邊界內的所有要求，以防止資料遭竊。

#### 解析度

請勿直接匯出至 Google 雲端硬碟，而是將查詢結果擷取至位於相同 VPC Service Controls perimeter 內的 Cloud Storage bucket，或將結果儲存為本機檔案。

### 如果專案已啟用 VPC Service Controls，Google 雲端硬碟外部資料表會遭到封鎖

錯誤字串：
`Google Drive external tables are blocked for projects with VPC-SC enabled`

#### 診斷

根據預設，VPC Service Controls 不會封鎖 Google 雲端硬碟外部資料表 (例如連結試算表) 的查詢。不過， Google Cloud 貴組織明確要求 Google Cloud對專案強制執行嚴格的封鎖設定，覆寫預設的允許行為，防止任何從 VPC Service Controls 範圍內傳入 Google 雲端硬碟資料的查詢，因此會出現這項錯誤。

#### 解析度

將 Google 試算表或 Google 雲端硬碟檔案中的資料，直接匯入 VPC Service Controls 範圍內的標準 BigQuery 資料表，而非以外部聯合資料表的形式動態查詢。或者，您也可以與內部 Cloud 管理員聯絡，討論貴組織的資料匯出界限。

### 專案無法匯出至 Google 雲端硬碟

錯誤字串：
`Export to Google Drive is blocked for your project.`

#### 診斷

即使沒有 VPC Service Controls perimeter， Google Cloud 管理員也已要求對專案套用特定嚴格組織設定，拒絕所有 Google 雲端硬碟資料擷取功能。

#### 解析度

請選擇其他擷取目的地，例如 Cloud Storage bucket 或本機檔案，或與內部 Cloud 管理員聯絡，討論貴組織的資料匯出界限。

### 位置違反組織政策限制

錯誤字串：
`LOCATION violates constraint CONSTRAINT_NAME on the
resource projects/PROJECT_ID` 或
`LOCATION violates constraint CONSTRAINT_NAME on the
resource projects/PROJECT_ID/datasets/DATASET_ID`

#### 診斷

Cloud 管理員已設定[組織政策限制](https://docs.cloud.google.com/organization-policy/reference/org-policy-constraints?hl=zh-tw)，明確限制可建立或分析資源的位置。這項錯誤通常會在下列情況出現：

* 在未經授權的地理區域建立資料集 (例如受 `constraints/gcp.resourceLocations` 限制)。
* 嘗試在不允許的情況下，跨外部雲端使用 BigQuery Omni (例如，遭到 `constraints/bigquery.disableBQOmniAWS` 或 `constraints/bigquery.disableBQOmniAzure` 封鎖)。

#### 解析度

1. 請查看錯誤訊息中提供的確切 `CONSTRAINT_NAME`，瞭解哪些動作遭到封鎖。
2. 請為資料選取其他未封鎖的區域，或與Google Cloud 組織管理員合作，在資料夾或組織層級查看組織政策。詳情請參閱「[建構及定義資源位置](https://docs.cloud.google.com/organization-policy/restrict-locations?hl=zh-tw)」。

## 排解未經驗證錯誤

當您在 BigQuery 中收到 HTTP `401 Unauthorized` (gRPC `UNAUTHENTICATED`) 錯誤，且錯誤原因為 `unauthenticated` 時，表示要求缺少有效的驗證憑證、OAuth 2.0 存取權杖已過期，或呼叫端無法以指定身分進行驗證。

以下各節說明最常見的 `unauthenticated` 情境、原因和解決方法。

### 憑證無效或已過期

錯誤字串：

* `Invalid credential`
* `User credential was invalid.`
* `Credentials expired`
* `Credentials missing required scope.`
* `Request had invalid authentication credentials. Expected OAuth 2 access
  token, login cookie or other valid authentication credential.`

#### 診斷

要求提供的存取權杖、服務帳戶金鑰或應用程式預設憑證 (ADC) 已過期、撤銷或缺少必要的 OAuth 2.0 範圍。如果要求的簽署系統時鐘與網路時間通訊協定 (NTP) 時間不一致，也會發生這個錯誤。

#### 解析度

* **重新整理憑證。**如果您是從本機開發環境進行驗證，請執行 `gcloud auth application-default login` (適用於 ADC) 或 `gcloud auth login`，取得新的權杖。
* **驗證服務帳戶金鑰和 OAuth 範圍。**如果應用程式使用 `GOOGLE_APPLICATION_CREDENTIALS`，請確認變數指向有效且未撤銷的 JSON 金鑰檔案、服務帳戶已在Google Cloud 控制台啟用，且憑證包含必要的 `https://www.googleapis.com/auth/bigquery` 或 `https://www.googleapis.com/auth/cloud-platform` 範圍。
* **使用目前的用戶端程式庫，並同步處理系統時鐘。**請將 [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)或 [ODBC](https://docs.cloud.google.com/bigquery/docs/odbc-for-bigquery?hl=zh-tw) 或 [JDBC](https://docs.cloud.google.com/bigquery/docs/jdbc-for-bigquery?hl=zh-tw) 驅動程式更新至最新版本，以便自動處理 OAuth 2.0 權杖更新和聯合憑證。此外，請確認主機的系統時鐘已使用 NTP 同步。

### 缺少使用者憑證或服務帳戶模擬權限

錯誤字串：

* `Current user can not act as user for service account
  SERVICE_ACCOUNT_EMAIL`
* `No end user credentials found when accessing
  PROJECT_ID:DATASET_ID.TABLE_ID. Please use
  end user credentials to call BigQuery APIs.`

#### 診斷

工作或持續查詢設為以自訂服務帳戶的身分執行，但呼叫端沒有權限以該帳戶的身分執行，或者目標資料表或安全性政策需要使用者憑證 (EUC)，BigQuery 才能根據互動式使用者身分評估存取權。

#### 解析度

* **授予服務帳戶模擬權限。**執行[持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw)或設定了自訂服務帳戶的工作時，請將該服務帳戶的服務帳戶使用者角色 (`roles/iam.serviceAccountUser`，包含 `iam.serviceAccounts.actAs` 權限) 授予呼叫端。模擬服務帳戶或將聯合憑證換成短期權杖時，請將目標服務帳戶的服務帳戶權杖建立者角色 (`roles/iam.serviceAccountTokenCreator`) 授予呼叫端。
* **使用使用者憑證進行驗證。**如果目標資源需要使用者憑證，請使用互動式使用者的 OAuth 2.0 憑證 (例如執行 `gcloud auth application-default login`，或在商業智慧工具中設定使用者 OAuth)，而非獨立服務帳戶憑證，驗證要求。
* **驗證 VPC Service Controls 輸入和輸出規則。**如果要求跨越 VPC Service Controls 邊界，請確認 perimeter 的輸入和輸出規則允許呼叫端身分和目標資源。

### 帳戶受限、停權或刪除

錯誤字串：

* `The account was restricted due to REASON`
* `Account deleted`

#### 診斷

發出要求的 Google 帳戶或 Google Workspace 帳戶，已遭管理員或帳戶安全性政策停權、停用、限制或刪除。

#### 解析度

請與 Google Workspace 或 Cloud Identity 管理員聯絡，在 Google 管理控制台中查看帳戶狀態，並還原或取消停權使用者帳戶，或更新工作負載，以便使用有效的服務帳戶進行驗證。

## 排解資料欄層級存取控管問題

以下各節說明如何排解[資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)和 Data Catalog 政策標記的問題。

### 我看不到 Data Catalog 角色

如果找不到「Data Catalog Fine-Grained Reader」等角色，可能是因為您尚未在專案中啟用 Data Catalog API。如要瞭解如何啟用 Data Catalog API，請參閱「[事前準備](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#before_you_begin)」。啟用 Data Catalog API 後，Data Catalog 角色會在幾分鐘後顯示。

### 我無法查看「Taxonomies」(分類) 頁面

您需要額外權限，才能在Google Cloud 控制台查看「Policy tag taxonomies」(政策標記分類) 頁面。舉例來說，Data Catalog [政策標記管理員](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#policy_tags_admin)角色可以存取「Taxonomies」(分類) 頁面。

### 我已強制執行政策標記，但似乎沒有作用

如果仍收到不應存取帳戶的查詢結果，可能是帳戶收到快取結果。具體來說，如果您先前成功執行查詢，然後強制執行政策標記，則可能會從[查詢結果快取](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)取得結果。根據預設，查詢結果會快取 24 小時。如果[停用結果快取](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw#disabling_retrieval_of_cached_results)，查詢會立即失敗。如要進一步瞭解快取，請參閱「[資料欄層級存取控管的影響](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw#security)」。

一般來說，IAM 更新作業約需 30 秒才會生效。政策標記階層的變更最多可能需要 30 分鐘才會生效。

### 我沒有權限讀取設有資料欄層級安全性的資料表

您必須在不同層級 (例如組織、資料夾、專案和政策標記) 具備[精細讀取者角色](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#fine_grained_reader)或[遮蓋讀取者角色](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#roles_for_querying_masked_data)。「精細讀取者」角色可授予原始資料存取權，而「經過遮蓋的讀取者」角色則可授予[遮蓋資料](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)的存取權。您可以使用 [IAM 政策疑難排解工具](https://docs.cloud.google.com/policy-intelligence/docs/troubleshoot-access?hl=zh-tw)，在專案層級檢查這項權限。

### 我在政策標記分類中設定精細的存取控管，但使用者仍能看到受保護的資料

如要排解這個問題，請確認下列事項：

* 在 BigQuery **安全中心**的[「Policy tag taxonomies」(政策標記分類) 頁面](https://console.cloud.google.com/bigquery/security/secure/policy-tags?hl=zh-tw)中，確認「Enforce access control」(強制執行存取控管) 切換鈕已設為「On」(啟用)。
* 確認查詢並未使用[快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)。如果您使用 bq 指令列工具測試查詢，請使用 `--nouse_cache` 旗標停用查詢快取。例如：

  ```
  bq query --nouse_cache --use_legacy_sql=false "SELECT * EXCEPT (customer_pii) FROM my_table;"
  ```

### 專案遷移注意事項

政策標記和分類會歸屬於特定 Google Cloud 組織，當專案遷移至新組織時，不會自動重新建立關聯。如果將使用政策標記進行資料欄層級存取控管的專案遷移至其他組織，會發生下列問題：

* 在已遷移的專案中，您無法再透過 Google Cloud 控制台管理政策標記。
* 您無法將這些政策標記套用至已遷移專案中的新資料欄。
* 現有的資料欄層級存取控管機制可能仍會顯示，但基於管理目的，原始組織中來源分類的連結已中斷。

如要解決這個問題， Google Cloud 支援團隊必須手動介入，將分類與新組織重新建立關聯。如果您遷移了含有政策標記的專案，並遇到這些問題，請[與 Cloud Customer Care 聯絡](https://docs.cloud.google.com/support?hl=zh-tw)。

## 排解客戶自行管理的加密金鑰問題

下列清單說明搭配使用 Cloud Key Management Service 和客戶自行管理的加密金鑰 (CMEK) 時，常見的錯誤和建議解決方法：

錯誤：`Please grant Cloud KMS CryptoKey Encrypter/Decrypter role`
:   **解決方法：**與專案相關聯的 BigQuery 服務帳戶沒有足夠的 IAM 權限，無法對指定的 Cloud KMS 金鑰執行操作。如要授予必要的 IAM 權限，請按照錯誤訊息或「[授予加密和解密權限](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#grant_permission)」中的指示操作。

錯誤：`Existing table encryption settings don't match encryption settings specified in the request`
:   **解決方法：**如果目的地資料表的加密設定與要求中的加密設定不符，就可能發生這項錯誤。如要解決這個問題，請使用 `TRUNCATE` 寫入配置來取代資料表，或指定其他目的地資料表。

錯誤：`This region is not supported`
:   **解決方法：**Cloud KMS 金鑰的區域與目的地資料表的 BigQuery 資料集區域不符。如要解決這個問題，請選取與資料集所在區域相符的金鑰，或將資料載入與金鑰區域相符的資料集。

錯誤：`Your administrator requires that you specify an encryption key for queries in project PROJECT_ID.`
:   **解決方法：**組織政策禁止建立資源或執行查詢。如要進一步瞭解這項政策，請參閱「[要求所有資源使用 CMEK](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#services_constraint)」一文。

錯誤：`Your administrator prevents using KMS keys from project KMS_PROJECT_ID to protect resources in project PROJECT_ID.`
:   **解決方法：**組織政策禁止建立資源或執行查詢。如要進一步瞭解這項政策，請參閱「[限制 BigQuery 專案的 Cloud KMS 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#projects_constraint)」。

## 後續步驟

* 如要查看所有 BigQuery IAM 角色和權限的清單，請參閱「[BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。
* 如要進一步瞭解資料欄層級安全性，請參閱「[使用資料欄層級存取控管功能限制存取權](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)」。
* 如要進一步瞭解客戶自行管理的加密金鑰，請參閱「[使用 Cloud KMS 金鑰保護資料](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)」。
* 如要進一步瞭解如何排解 IAM 允許和拒絕政策的問題，請參閱「[排解政策問題](https://docs.cloud.google.com/iam/docs/troubleshoot-policies?hl=zh-tw)」。
* 如要進一步瞭解 Policy Intelligence 政策分析工具，請參閱「[允許政策的政策分析工具](https://docs.cloud.google.com/policy-intelligence/docs/policy-analyzer-overview?hl=zh-tw)」。
* 如要進一步瞭解政策疑難排解工具，請參閱「[使用政策疑難排解工具](https://docs.cloud.google.com/iam/docs/troubleshoot-policies?hl=zh-tw#troubleshooter)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]