Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理資料準備作業

本文說明如何管理 BigQuery 資料準備作業，包括管理存取權、版本管理、效能和中繼資料。本文也說明如何執行基本工作，例如查看及下載資料準備作業。

資料準備作業是由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 驅動的 [BigQuery](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 資源。詳情請參閱「[BigQuery 資料準備總覽](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw)」一文。

## 事前準備

1. 確認已啟用 [Gemini for Google Cloud API](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw#enable-api)。
2. 如要在 Knowledge Catalog 中管理資料準備中繼資料，請確保專案已啟用 [Dataplex API](https://docs.cloud.google.com/knowledge-catalog/docs/enable-api?hl=zh-tw)。 Google Cloud

### 必要的角色

準備資料的使用者和執行工作的 Dataform 服務帳戶，都需要下列 Identity and Access Management (IAM) 角色授予的權限。

#### 取得資料準備功能的使用者存取權

如要取得在 BigQuery 中準備資料所需的權限，請要求管理員授予您下列 IAM 角色：

* 專案的 [BigQuery Studio 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.studioUser)  (`roles/bigquery.studioUser`)
* 專案的 [Gemini for Google Cloud 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/cloudaicompanion?hl=zh-tw#cloudaicompanion.user)  (`roles/cloudaicompanion.user`)
* 存取來源資料表：
  資料表、資料集或專案的 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 分享資料準備作業：
  [Dataform 程式碼擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeOwner)  (`roles/dataform.codeOwner`)
  在表格、資料集或專案上

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

如要進一步瞭解 BigQuery 資料集的 IAM，請參閱「[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)」。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

#### 取得管理中繼資料的權限

如要取得管理 Knowledge Catalog 中資料準備中繼資料所需的權限，請確認您具備必要的 [Knowledge Catalog 角色](https://docs.cloud.google.com/knowledge-catalog/docs/iam-roles?hl=zh-tw)和 [`dataform.repositories.get`](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#predefined-roles) 權限。

#### 授予 Dataform 服務帳戶存取權

為確保 Dataform 服務帳戶具備在 BigQuery 中執行資料準備作業的必要權限，請要求管理員將下列 IAM 角色授予 Dataform 服務帳戶：

* 存取來源資料表：
  資料表、資料集或專案的 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 存取目的地資料表：
  資料表、資料集或專案的「BigQuery 資料編輯者」 (`roles/bigquery.dataEditor`)

視資料準備管道而定，Dataform 服務帳戶可能需要額外權限。詳情請參閱「[授予 Dataform 必要存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-dataform-required-access)」。

#### 準備資料時應考量的安全事項

由於 BigQuery 中的程式碼資產是由 Dataform 支援，因此請考慮以下安全影響，以確保使用者能存取這些資產：

* 程式碼資產的可見度取決於專案層級的 Dataform 權限。具備 `dataform.repositories.list` 權限的使用者 (包括 [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)、[BigQuery Studio 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser)和 [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user)等標準 BigQuery 角色)，可以在 Google Cloud 專案的「Explorer」面板中查看所有程式碼資產，無論這些資產是由他們建立，還是與他們共用。如要限制瀏覽權限，可以建立排除 `dataform.repositories.list` 權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。
* 與 Dataform 服務代理程式共用的任何密鑰，都可能遭到可編輯這些資產的使用者存取。為確保憑證安全，請限制只有信任的使用者可以建立及編輯憑證，並限制 Dataform 服務代理程式可存取的密鑰。詳情請參閱「[在套件安裝期間存取密鑰](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#secret-access-risk)」。

詳情請參閱「[Dataform 權限的安全性考量](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#security-considerations-permissions)」。

## 查看現有資料準備作業

如要查看現有資料準備作業的清單，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案。
4. 按一下「資料準備」。

## 透過增量處理資料，最佳化資料準備作業

如要設定將準備好的資料寫入目的地資料表的方式，請按照下列步驟操作。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，按一下「資料準備」，然後選取資料準備作業。
4. 在資料準備工具列中，依序選取「更多」**>「寫入模式」**。
5. 選取任一選項。詳情請參閱「[寫入模式](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw#write-mode)」。
6. 按一下 [儲存]。

## 資料準備版本

您可以選擇在[存放區](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw)內或外部建立資料準備作業。系統會根據資料準備作業所在位置，以不同方式處理版本控管。

### 存放區中的資料準備版本管理

存放區是位於 BigQuery 或第三方供應商的 Git 存放區。您可以在存放區中使用[工作區](https://docs.cloud.google.com/bigquery/docs/workspaces-intro?hl=zh-tw)，對資料準備作業執行版本控管。詳情請參閱「[使用檔案的版本管控功能](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw#use_version_control_with_a_file)」。

### 在存放區外部進行資料準備版本管理

如果 BigQuery 資料準備作業不在存放區中，則不支援查看、比較或還原資料準備作業版本。

如要依時間順序查看資料準備版本清單，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，按一下「資料準備」，然後選取資料準備作業。
4. 按一下「版本記錄」schedule。

## 下載資料準備檔案

如要以 SQLX 檔案下載資料準備作業，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「資料準備」。
4. 按一下要下載的資料準備作業名稱。
5. 按一下「下載」。資料準備作業會以 [SQLX 檔案格式](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw#dataform-core)儲存，例如 `NAME data preparation.dp.sqlx`。

**注意：**2025 年 7 月前建立的資料準備檔案會自動遷移至 SQLX 格式，這會改變檔案的儲存和執行方式。在下列情況中，系統會觸發這項一次性遷移作業：

* 開啟現有資料準備時，系統會遷移該資料準備。
* 儲存或更新資料準備工作時，管道中的資料準備工作就會遷移。

## 上傳資料準備檔案

如要從 SQLX 檔案上傳資料準備作業，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案。
4. 按一下**「資料準備」**，然後依序點按 more\_vert
   **「查看動作」 >「上傳至資料準備」**。
5. 在「上傳資料準備」對話方塊中，選取要上傳的檔案，或輸入資料準備的網址。
6. 輸入資料準備作業的名稱。
7. 選取管理及儲存資源的資料準備位置。
8. 按一下「上傳」。

## 管理 Knowledge Catalog 中的中繼資料

您可以使用 Knowledge Catalog 儲存及管理資料準備作業的中繼資料。預設情況下，Knowledge Catalog 會提供資料準備功能，不需額外設定。

您可以使用 Knowledge Catalog 管理所有 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)的資料準備作業。在 Knowledge Catalog 中管理資料準備作業時，須遵守 [Knowledge Catalog 配額和限制](https://docs.cloud.google.com/knowledge-catalog/docs/quotas?hl=zh-tw)，並適用 [Knowledge Catalog 定價](https://cloud.google.com/dataplex/pricing?hl=zh-tw)。

Knowledge Catalog 會自動從資料準備作業擷取下列中繼資料：

* 資料資產名稱
* 資料資產父項
* 資料資產位置
* 資料資產類型
* 對應 Google Cloud 專案

Knowledge Catalog 會將資料準備作業記錄為[項目](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entries)，並提供下列項目值：

系統項目群組
:   資料準備的[系統項目群組](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-groups)為 `@dataform`。如要查看 Knowledge Catalog 中資料準備項目的詳細資料，您需要查看 `dataform` 系統項目群組。如要瞭解如何查看項目群組中的所有項目清單，請參閱 Knowledge Catalog 說明文件中的「[查看項目群組的詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-group-details)」
。

系統項目類型
:   資料準備的[系統項目類型](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-types)為 `dataform-code-asset`。如要查看資料準備的詳細資料，您需要查看 `dataform-code-asset` 系統項目類型、使用切面式篩選器篩選結果，並[將 `dataform-code-asset` 切面內的 `type` 欄位設為 `DATA_PREPARATION`](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)。然後選取所選資料準備作業的項目。
    如要瞭解如何查看所選項目類型的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目類型的詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-type-details)」。如要瞭解如何查看所選項目的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目的詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw#view-entry-details)」
。

系統切面類型
:   資料準備的[系統層面類型](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#aspect-types)為 `dataform-code-asset`。如要透過[切面](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#aspects)註解資料準備項目，在 Knowledge Catalog 中為資料準備作業提供額外脈絡，請查看 `dataform-code-asset` 切面類型、使用以切面為準的篩選器篩選結果，並[將 `dataform-code-asset` 切面內的 `type` 欄位設為 `DATA_PREPARATION`](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)。如需如何使用切面註解項目的操作說明，請參閱 Knowledge Catalog 說明文件中的「[管理切面及豐富中繼資料](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw)」一文。

類型
:   資料畫布的類型為 `DATA_PREPARATION`。
    您可以使用`aspect:dataplex-types.global.dataform-code-asset.type=DATA_PREPARATION`[以切面為準的篩選器](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)中的查詢，依`dataform-code-asset`系統項目類型和`dataform-code-asset`切面類型篩選資料準備作業。

如需搜尋資產的操作說明，請參閱 Knowledge Catalog 說明文件中的「[在 Knowledge Catalog 中搜尋資料資產](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw)」。

## 後續步驟

* 進一步瞭解如何[在 BigQuery 中準備資料](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw)。
* 瞭解如何[手動或排程執行資料準備作業](https://docs.cloud.google.com/bigquery/docs/orchestrate-data-preparations?hl=zh-tw)。
* 瞭解如何[建立資料準備作業](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-15 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-15 (世界標準時間)。"],[],[]]