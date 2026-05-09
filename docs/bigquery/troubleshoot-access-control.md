Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排解 BigQuery 的 IAM 權限問題

本文說明如何排解 BigQuery 中身分與存取權管理 (IAM) 權限的問題。IAM 權限問題通常會導致 `Access Denied` 錯誤，例如：

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

* 如要排解主體存取 BigQuery 資源的問題，請確認您具備[必要 IAM 權限](https://docs.cloud.google.com/policy-intelligence/docs/troubleshoot-access?hl=zh-tw#required-permissions)。

## 收集問題相關資訊

如要排解資源存取問題，第一步是判斷缺少的權限、遭拒存取權的 IAM 主體，以及主體嘗試存取的資源。

### 從錯誤或工作記錄取得資訊

如要取得主體、資源和權限的相關資訊，請檢查 bq 指令列工具的輸出內容、API 回應或 Google Cloud 控制台中的 BigQuery。

舉例來說，如果您嘗試執行權限不足的查詢， Google Cloud 控制台的「Query results」(查詢結果) 專區中，「Job information」(工作資訊) 分頁會顯示類似以下的錯誤。

檢查錯誤，判斷主體、資源和權限。

**注意：** 您也可以使用[工作記錄](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)查看工作詳細資料。

在某些情況下，您可以直接從錯誤訊息要求缺少的權限。詳情請參閱 IAM 說明文件中的「[權限錯誤訊息](https://docs.cloud.google.com/iam/docs/permission-error-messages?hl=zh-tw)」。

### 從 Cloud 稽核記錄取得資訊

如果錯誤訊息是通用訊息、缺少資訊，或動作在背景程序中失敗，請使用 Cloud 稽核記錄記錄檔瀏覽器取得錯誤相關資訊。

1. 前往 Google Cloud 控制台的「Logs Explorer」頁面。

   [前往 Logs Explorer](https://console.cloud.google.com/logs/query?hl=zh-tw)

   或者，從導覽選單中選擇「監控」**>「記錄檔探索工具」**。
2. 在記錄檢視器中，選擇「專案記錄」做為記錄範圍。
3. 在查詢視窗中輸入下列查詢，從 BigQuery 資料存取記錄取得權限相關錯誤：

   ```
   resource.type="bigquery_resource" AND
   logName="projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Fdata_access" AND
   protoPayload.status.message:"Access Denied" OR
   protoPayload.status.message:"Permission denied" OR
   protoPayload.status.code=7
   ```

   將 PROJECT\_ID 替換為專案 ID。
4. 在查詢結果中，展開與失敗作業對應的記錄項目。
5. 在 `protoPayload` 區段中，展開 `authorizationInfo` 陣列，然後展開 `authorizationInfo` 陣列中的每個節點。

   `authorizationInfo` 陣列會顯示 API 呼叫期間執行的每項權限檢查。
6. 如要查看錯誤原因，請尋找 `granted: false` 項目。「`granted: false`」項目會顯示下列資訊：

   * `permission`：已檢查的 IAM 權限字串。
     例如：`bigquery.tables.getData`。
   * `resource`：主體嘗試存取的資源完整名稱。例如：`projects/myproject/datasets/mydataset/tables/mytable`。
   * `principalEmail` (如有)：在「參照」`protoPayload.authenticationInfo`中，這是嘗試執行動作的主體。

**注意：** 您可以在 Google Cloud Observability 的「[**範例查詢**」頁面](https://docs.cloud.google.com/logging/docs/view/query-library?hl=zh-tw#bigquery-filters)找到其他 BigQuery 稽核記錄範例查詢。

## 使用政策分析工具檢查允許政策

您可以使用允許政策的政策分析工具，根據 [IAM 允許政策](https://docs.cloud.google.com/iam/docs/policies?hl=zh-tw)，瞭解哪些 [IAM 主體](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw)具備哪些 BigQuery 資源的存取權。

**注意：** 政策智慧功能也提供[身分與存取權管理政策疑難排解工具](https://docs.cloud.google.com/policy-intelligence/docs/troubleshoot-access?hl=zh-tw)，可協助您排解特定主體的存取權問題。

收集權限錯誤的相關資訊後，您可以使用政策分析器，瞭解主體缺少必要存取權的原因。這項工具會分析所有相關政策、Google 群組成員資格，以及專案、資料夾和機構等上層資源的繼承項目。

如要使用政策分析工具分析允許政策，請建立分析查詢、指定分析範圍，然後執行查詢。

1. 前往 Google Cloud 控制台的「Policy Analyzer」頁面。

   [前往 Policy Analyzer](https://console.cloud.google.com/iam-admin/analyzer?hl=zh-tw)

   或者，從導覽選單中依序選擇「IAM 與管理」**>「政策分析器」**。
2. 按一下「建立自訂查詢」。
3. 在「設定查詢」頁面中，輸入先前收集的資訊：

   1. 在「選取範圍」部分，確認「選取查詢範圍」欄位中顯示的是目前專案，或按一下「瀏覽」選擇其他資源。
   2. 在「設定查詢參數」部分，為「參數 1」選擇「主體」，然後在「主體」欄位中，輸入使用者、群組或服務帳戶的電子郵件地址。
   3. 按一下 add「新增參數」。
   4. 針對「參數 2」，選擇「權限」，然後在「權限」欄位中，依序點選「選取」、選擇 BigQuery 權限和「新增」。例如選取 **`bigquery.tables.getData`**。
   5. 按一下 add「新增參數」。
   6. 在「參數 3」中選擇「資源」，並在「資源」欄位中輸入資源的完整名稱。資源名稱必須包含服務前置字串，如以下範例所示：

      * **BigQuery 專案**：
        `//cloudresourcemanager.googleapis.com/projects/PROJECT_ID`
      * **BigQuery 資料集**：
        `//bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET`
      * **BigQuery 資料表**：
        `//bigquery.googleapis.com/projects/PROJECT/datasets/DATASET/tables/TABLE`
4. 在「自訂查詢」窗格中，依序點選「分析」>「執行查詢」。
5. 查看查詢結果。結果可能是下列其中一項：

   * **空白清單**。如果沒有結果，表示主體沒有必要權限。您需要[授予主體角色](#find-role)，提供適當的權限。
   * **一或多個結果**。如果分析器找到允許政策，表示存在某種形式的存取權。按一下每個結果的「查看繫結」，即可查看提供資源存取權的角色，主體是這些資源的成員。政策繫結會顯示存取權是透過群組成員資格或繼承方式授予，還是因 [IAM 條件](https://docs.cloud.google.com/bigquery/docs/conditions?hl=zh-tw)或 [IAM 拒絕政策](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#deny_access_to_a_resource)而遭拒。

## 找出可授予必要權限的正確 IAM 角色

確認主體沒有足夠的存取權後，下一步是找出適當的預先定義或自訂 IAM 角色，授予必要權限。您選擇的角色應遵循最小權限原則。

如果貴機構使用自訂角色，您可以[列出專案或機構中建立的所有自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw#roles-list)，找出正確的角色。舉例來說，在 Google Cloud 控制台的「Roles」(角色) 頁面，您可以依「Type:Custom」(類型：自訂) 篩選清單，只查看自訂角色。

如要找出正確的預先定義 IAM 角色，請按照下列步驟操作。

1. 開啟 BigQuery IAM 角色和權限頁面的「BigQuery 權限」部分。
2. 在「Enter a permission」(輸入權限) 搜尋列中，輸入您從錯誤訊息、工作記錄或稽核記錄中擷取的權限。例如：`bigquery.tables.getData`。

   搜尋結果會顯示授予該權限的所有預先定義 BigQuery 角色。
3. 運用最低權限原則：在角色清單中，選擇授予必要權限的最嚴格角色。舉例來說，如果您搜尋「`bigquery.tables.getData`」來授予查詢表格資料的權限，則 [BigQuery 資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer)是授予該權限的最低權限角色。
4. 將適當角色授予主體。如要瞭解如何將 IAM 角色授予 BigQuery 資源，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

## 後續步驟

* 如需所有 BigQuery IAM 角色和權限的清單，請參閱「[BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。
* 如要進一步瞭解如何排解身分與存取權管理中的允許和拒絕政策問題，請參閱「[排解政策問題](https://docs.cloud.google.com/iam/docs/troubleshoot-policies?hl=zh-tw)」。
* 如要進一步瞭解政策智慧政策分析工具，請參閱[允許政策的政策分析工具](https://docs.cloud.google.com/policy-intelligence/docs/policy-analyzer-overview?hl=zh-tw)。
* 如要進一步瞭解政策疑難排解工具，請參閱「[使用政策疑難排解工具](https://docs.cloud.google.com/iam/docs/troubleshoot-policies?hl=zh-tw#troubleshooter)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]