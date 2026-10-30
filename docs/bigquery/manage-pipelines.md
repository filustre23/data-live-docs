Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理管道

[BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)可讓您檢查執行記錄、設定失敗警示，以及控管由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 支援的程式碼資產。您也可以在 [Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/introduction?hl=zh-tw) 中充實工作流程中繼資料，追蹤資料品質，並刪除過時的工作流程，讓專案井然有序。視團隊儲存程式碼的位置而定，您可以在「Files and Folders」(檔案和資料夾) (包括使用者資料夾和團隊資料夾) 或「BigQuery Studio Git repositories (Git Folders)」(BigQuery Studio Git 存放區 (Git 資料夾)) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 中存取管道。

## 事前準備

1. [建立 BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。
2. 如要在 Knowledge Catalog 中管理管道中繼資料，請確認 Google Cloud 專案已啟用 [Dataplex API](https://docs.cloud.google.com/knowledge-catalog/docs/enable-api?hl=zh-tw)。

### 必要的角色

如要取得管理管道所需的權限，請要求管理員授予您下列 IAM 角色：

* 如要查看及執行管道，請按照下列步驟操作：
  + 專案的 [Dataform 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Viewer)  (`roles/dataform.Viewer`)
  + 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 如要使用 Google 帳戶的使用者憑證執行管道：專案或特定 BigQuery 資料集的 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
* 如要刪除管道：管道的 [Dataform 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Admin)  (`roles/dataform.Admin`)
* 如要管理使用者資料夾中的管道，請按照下列步驟操作：
  + 資料夾的[程式碼擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeOwner)  (`roles/dataform.codeOwner`)
  + 資料夾上的「Code Editor」(程式碼編輯器) (`roles/dataform.codeEditor`)
  + 資料夾的[程式碼檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeViewer)  (`roles/dataform.codeViewer`)
* 如要管理團隊資料夾中的管道，請按照下列步驟操作：
  + 團隊資料夾的[團隊資料夾擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.teamFolderOwner)  (`roles/dataform.teamFolderOwner`)
  + 團隊資料夾的[團隊資料夾協作者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.teamFolderContributor)  (`roles/dataform.teamFolderContributor`)
  + 團隊資料夾的[團隊資料夾檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.teamFolderViewer)  (`roles/dataform.teamFolderViewer`)
* 如要管理 Git 存放區中的管道：專案的 [Developer Connect OAuth 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/developerconnect?hl=zh-tw#developerconnect.oauthUser)  (`roles/developerconnect.oauthUser`)
* 如要在 Knowledge Catalog 查看及管理中繼資料：專案或 `@bigquery` 項目群組的 [Dataplex Catalog 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.catalogEditor)  (`roles/dataplex.catalogEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如要進一步瞭解 Dataform IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw)」。如要進一步瞭解資料夾的角色，請參閱「[建立及管理資料夾](https://docs.cloud.google.com/bigquery/docs/create-manage-folders?hl=zh-tw#required_roles)」。如要進一步瞭解 Git 存放區的角色，請參閱「[使用 BigQuery Studio Git 存放區管理程式碼](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw#required_roles)」。

**注意：** 建立管道時，BigQuery 會授予您該管道的 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。凡是具備 Google Cloud 專案 Dataform 管理員角色的使用者，都擁有專案中所有管道的擁有者存取權。

如果您使用自訂服務帳戶執行管道，則必須將下列角色授予該服務帳戶：

* 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* 專案或特定 BigQuery 資料集的 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor) (`roles/bigquery.dataEditor`)
* 專案或 `@bigquery` 項目群組的 [Dataplex Catalog 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.catalogEditor) (`roles/dataplex.catalogEditor`)

## 查看管道

您可以在「Files」(檔案) 窗格中，查看及檢查儲存在資料夾或 Git 資料夾中的管道。您可以在「Explorer」窗格中，查看獨立管道和儲存在資料夾中的管道。儲存在 Git 資料夾中的管道不會顯示在「Explorer」窗格中。

### 在「Files」(檔案) 窗格中查看管道

儲存在資料夾或 Git 資料夾中的管道會直接顯示在「Files」(檔案) 窗格中。

如要查看儲存在資料夾或 Git 資料夾中的管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「檔案」圖示 folder，開啟檔案瀏覽器。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 展開「User」資料夾、「Team folder」或已連結的 Git 存放區資料夾。

   管道會以「管道」圖示顯示，而非標準資料夾圖示。
4. 按一下管道資料夾，開啟**管道檢視器**。

   **Pipeline Viewer** 會顯示管道工作的編譯有向無環圖 (DAG)、執行狀態和設定分頁。
5. 在檔案瀏覽器中展開管道目錄，即可瀏覽巢狀目錄 (例如 `definitions/`) 和個別工作檔案。

**注意：** 如果連結的 Git 存放區根目錄中含有 `workflow_settings.yaml`，BigQuery Studio 會將其視為根層級管道。Git 存放區資料夾本身會顯示「Pipeline」圖示。點選 Git 存放區資料夾後，**Pipeline Viewer** 會開啟，並顯示整個存放區的已編譯 DAG。

### 在「Explorer」窗格中查看管道

如要查看獨立管道和儲存在資料夾中的管道清單，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後點選「Pipelines」。
4. 選取管道，在**管道檢視器**中開啟。

## 查看過往手動執行作業

如要查看所選管道過去的手動執行記錄，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下「Executions」(執行作業)。
5. 選用：如要重新整理過去執行作業的清單，請按一下「Refresh」(重新整理)。

## 設定快訊，掌握失敗的管道執行作業

每個管道都有對應的 Dataform 存放區 ID。
每次執行 BigQuery 管道時，系統都會使用對應的 Dataform 存放區 ID，將執行作業記錄在 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw) 中。您可以使用 Cloud Monitoring 觀察 BigQuery 管道執行的 Cloud Logging 記錄趨勢，並在發生指定情況時通知您。

如要在 BigQuery 管道執行失敗時收到快訊，可以為對應的 Dataform 存放區 ID 建立記錄警告政策。如需操作說明，請參閱「[設定工作流程叫用失敗的警告](https://docs.cloud.google.com/dataform/docs/monitor-runs?hl=zh-tw#configure-alerts-failed-workflow-invocations)」。

如要找出管道的 Dataform 存放區 ID，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下「設定」。

   管道的 Dataform 存放區 ID 會顯示在「Settings」(設定) 分頁底部。

## 刪除管道

如要永久刪除管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。[前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)

* 如要刪除儲存在資料夾或 Git 資料夾中的管道，請按照下列步驟操作：

  1. 在左側窗格中，按一下「folder 檔案」。
  2. 在檔案樹狀結構中，找出要刪除的管道資料夾。
  3. 按一下管道資料夾旁的 more\_vert「View actions」(查看動作)，然後點選「Delete」(刪除)。
  4. 在確認對話方塊中點按「刪除」。

     管道資料夾和其中包含的所有工作和檔案，都會從工作區中刪除。
* 如要刪除「Explorer」窗格中列出的管道，請按照下列步驟操作：

  1. 點選左側窗格中的 explore「Explorer」。
  2. 在「Explorer」窗格中展開專案，然後點選「Pipelines」。
  3. 找出要刪除的管道。
  4. 按一下管道旁的 more\_vert「View actions」(查看動作)，然後點選「Delete」(刪除)。
  5. 點選「刪除」。

## 在 Knowledge Catalog 管理中繼資料

Knowledge Catalog 可讓您儲存及管理 pipeline 的中繼資料。Knowledge Catalog 預設提供管道，不需額外設定。

您可以使用 Knowledge Catalog 管理所有[管道位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)中的管道。在 Knowledge Catalog 中管理管道時，須遵守 [Knowledge Catalog 配額和限制](https://docs.cloud.google.com/knowledge-catalog/docs/quotas?hl=zh-tw)，以及 [Knowledge Catalog 定價](https://cloud.google.com/dataplex/pricing?hl=zh-tw)。

Knowledge Catalog 會自動從管道擷取下列中繼資料：

* 資料資產名稱
* 資料資產父項
* 資料資產位置
* 資料資產類型
* 對應的 Google Cloud 專案

Knowledge Catalog 會將管道記錄為[項目](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entries)，並包含下列項目值：

系統項目群組
:   管道的[系統項目群組](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-groups)為 `@dataform`。如要在 Knowledge Catalog 中查看管道項目的詳細資料，您必須查看 `dataform` 系統項目群組。如要瞭解如何查看項目群組中所有項目的清單，請參閱 Knowledge Catalog 說明文件中的「[查看項目群組的詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-group-details)」。

系統項目類型
:   管道的[系統項目類型](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-types)為 `dataform-code-asset`。如要查看管道詳細資料，您必須查看 `dataform-code-asset` 系統項目類型、使用切面篩選器篩選結果，並[將 `dataform-code-asset` 切面中的 `type` 欄位設為 `WORKFLOW`](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)。接著，選取所選管道的項目。如要瞭解如何查看所選項目類型的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目類型的詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-type-details)」。如要瞭解如何查看所選項目的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw#view-entry-details)」一節。

系統切面類型
:   管道的[系統切面類型](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#aspect-types)為 `dataform-code-asset`。如要使用[切面](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#aspects)為資料管道項目加上註解，為 Knowledge Catalog 中的管道提供額外背景資訊，請查看 `dataform-code-asset` 切面類型，使用切面篩選器篩選結果，並[將 `dataform-code-asset` 切面中的 `type` 欄位設為 `WORKFLOW`](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)。如要瞭解如何使用切面為項目加上註解，請參閱 Knowledge Catalog 說明文件中的「[管理切面並充實中繼資料](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw)」。

類型
:   資料畫布的類型為 `WORKFLOW`。這個類型可讓您在[切面篩選器](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)中使用 `aspect:dataplex-types.global.dataform-code-asset.type=WORKFLOW` 查詢，篩選 `dataform-code-asset` 系統項目類型和 `dataform-code-asset` 切面類型中的管道。

如要瞭解如何在 Knowledge Catalog 搜尋資產，請參閱 Knowledge Catalog 說明文件中的「[在 Knowledge Catalog 搜尋資料資產](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw)」。

### 中繼資料擴充和資料品質評量表整合

Dataform 可將下列中繼資料發布至 Knowledge Catalog：

* 總覽切面類型
* 一般切面類型
* 資料品質評量表切面類型

Dataform 斷言會自動與 [Knowledge Catalog 資料品質評量表](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#data-quality-scorecard)整合。在管道執行期間，任何 Dataform 斷言的結果都會自動發布至 Knowledge Catalog。這些結果會填入 Knowledge Catalog 資料品質評量表，並顯示通過或失敗狀態。

**注意：** 每次執行都會覆寫先前 Dataform 執行作業發布的現有資料品質評量表，但不會影響 Knowledge Catalog 資料掃描建立的評量表。

如要查看中繼資料更新狀態，請按照「[查看過去的手動執行作業](#view-manual-runs)」中的操作說明進行。

中繼資料同步後，您可以在 Knowledge Catalog 搜尋及查看項目。詳情請參閱「[搜尋資源](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw#search-data-assets)」。

## 後續步驟

* 進一步瞭解 [BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)。
* 瞭解如何[建立管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。
* 瞭解如何[排定管道](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)。
* 瞭解如何[使用 BigQuery Studio Git 存放區管理程式碼](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw)。
* 瞭解如何[使用資料夾整理程式碼資產](https://docs.cloud.google.com/bigquery/docs/code-asset-folders?hl=zh-tw)。
* 進一步瞭解 [Dataform 部署作業](https://docs.cloud.google.com/dataform/docs/deployments?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]