Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理筆記本

本文說明如何管理 [BigQuery 中的 Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)，包括如何查看、比較、還原及刪除筆記本。

本文也說明如何在 [Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/introduction?hl=zh-tw) 查看及管理筆記本中繼資料。

Notebooks 是 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 程式碼資產，採用 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 技術。

## 事前準備

1. [建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。
2. 如要在 Knowledge Catalog 中管理筆記本中繼資料，請確認 Google Cloud 專案已啟用 [Dataplex API](https://docs.cloud.google.com/knowledge-catalog/docs/enable-api?hl=zh-tw)。

### 所需權限

如要共用筆記本，您必須具備下列 Identity and Access Management (IAM) 角色：

* [BigQuery 工作使用者 (`roles/bigquery.jobUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)
* [BigQuery 讀取工作階段使用者 (`roles/bigquery.readSessionUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser)
* 資源層級的[程式碼擁有者 (`roles/dataform.codeOwner`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner)。

如要儲存及刪除筆記本，您必須具備下列 IAM 角色：

* [BigQuery 工作使用者 (`roles/bigquery.jobUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)
* [BigQuery 讀取工作階段使用者 (`roles/bigquery.readSessionUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser)
* [程式碼擁有者 (`roles/dataform.codeOwner`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner) 或[程式碼編輯器 (`roles/dataform.codeEditor`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor)

如要使用筆記本修訂版本，您必須具備下列 IAM 角色：

* [BigQuery 工作使用者 (`roles/bigquery.jobUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)
* [BigQuery 讀取工作階段使用者 (`roles/bigquery.readSessionUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser)
* 下列任一角色：

  + [程式碼擁有者 (`roles/dataform.codeOwner`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner)
  + [程式碼編輯器 (`roles/dataform.codeEditor`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor)
  + [程式碼檢視者 (`roles/dataform.codeViewer`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer)

如要進一步瞭解 BigQuery IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要在 Knowledge Catalog 中管理筆記本中繼資料，請確認您具備必要的 [Knowledge Catalog 角色](https://docs.cloud.google.com/knowledge-catalog/docs/iam-roles?hl=zh-tw)。

## 授予筆記本存取權

如要授予其他使用者筆記本存取權，請將這些使用者新增至適當的 IAM 角色。

**重要事項：** 只要使用者具備筆記本存取權，即可查看筆記本中程式碼產生的所有輸出內容，即便內含使用者無權存取的資料表內容也一樣。如要避免共用已儲存的輸出內容，請[停用筆記本輸出內容儲存功能](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#disable_output_saving)。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 找出要授予存取權的筆記本。
5. 按一下筆記本旁的「Open actions」(開啟動作) 圖示 more\_vert，然後點選「Share」(共用)。
6. 在「共用權限」窗格中，按一下「新增使用者/群組」。
7. 在「New principals」(新增主體) 欄位中輸入主體。
8. 在「Role」(角色) 清單中，選取下列其中一個角色：

   * [**程式碼擁有者**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner)：可對筆記本執行任何動作，包括刪除或共用。
   * [**程式碼編輯器**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor)：可編輯筆記本。
   * [**程式碼檢視者**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer)：可以查看筆記本。**注意：** 主體也必須具備[Notebook 執行階段使用者 (`roles/aiplatform.notebookRuntimeUser`)](https://docs.cloud.google.com/vertex-ai/docs/general/access-control?hl=zh-tw#aiplatform.notebookRuntimeUser) 和 [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user) 角色，才能執行筆記本。
9. 選用：如要查看完整的角色清單和進階共用設定，請按一下「Advanced sharing」(進階共用)。
10. 按一下 [儲存]。
11. 如要返回筆記本資訊頁面，請按一下「Close」(關閉)。

## 共用筆記本

如要與其他使用者共用筆記本，可以生成並分享筆記本連結。如要讓其他使用者查看您共用的筆記本，您必須先[授予筆記本存取權](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#grant_access_to_notebooks)。

如要執行筆記本，使用者必須有權存取筆記本存取的資料。詳情請參閱「[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)」。

**重要事項：** 只要使用者具備筆記本存取權，即可查看筆記本中程式碼產生的所有輸出內容，即便內含使用者無權存取的資料表內容也一樣。如要避免共用已儲存的輸出內容，請[停用筆記本輸出內容儲存功能](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#disable_output_saving)。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 找出要共用的筆記本。您可以使用搜尋功能或篩選器尋找筆記本。
5. 按一下筆記本旁的「查看動作」圖示 more\_vert，然後依序點選「共用」>「複製連結」。
6. 與其他使用者分享連結。

## 停用筆記本輸出內容儲存功能

您可以停用筆記本輸出內容儲存功能，防止與其他有權存取筆記本檔案的使用者共用已儲存的筆記本輸出內容。

如果停用所選筆記本的輸出內容儲存功能，BigQuery 會刪除筆記本檔案中儲存的所有輸出內容，且不會儲存後續執行的輸出內容。

不過，[有權存取筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#grant_access_to_notebooks)的使用者仍可透過下列方式查看輸出內容：

* 執行筆記本，查看目前的輸出內容。系統不會儲存這項輸出內容。
* 在修訂版本記錄中，查看筆記本的封存版本和輸出內容。

如要停用所選筆記本的輸出內容儲存功能，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 按一下要停用輸出內容儲存功能的筆記本。
5. 如要展開選單列，請按一下 keyboard\_arrow\_down「切換標頭顯示設定」。
6. 依序點選**「編輯」 > 「筆記本設定」**。
7. 在「Notebook settings」(筆記本設定) 視窗中，選取「Omit code cell output when saving this notebook」(儲存這個筆記本時，忽略程式碼儲存格輸出內容)。
8. 按一下 [儲存]。
9. 按一下「重新載入」。

## 解決衝突

如果您和其他使用者在筆記本中進行了不一致的變更，服務會引發 `Automatic saving failed. This file was updated remotely or
in another tab.` 錯誤，並提供 `Show diff` 連結。如要解決衝突，請按照下列步驟操作：

1. 按一下「`Show diff`」連結。「Review remote changes」對話方塊隨即開啟。
2. 選用：如要比較筆記本原始碼，請勾選「Raw source」(原始碼) 核取方塊。
3. 選用：如要比較內嵌版本，而非在不同窗格中比較，請勾選「Inline diff」(內嵌差異) 核取方塊。
4. 查看變更並決定要保留哪些內容，必要時可修改輸入內容。
5. 按一下「儲存變更」。

## 查看所有筆記本

如要查看專案中所有筆記本的清單，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，按一下「Notebooks」旁邊的 more\_vert「View actions」(查看動作)，然後執行下列任一操作：

* 如要在目前的分頁中開啟清單，請按一下「顯示全部」。
* 如要在新分頁中開啟清單，請依序點選「全部顯示」 >「新分頁」。
* 如要在分割分頁中開啟清單，請依序按一下「全部顯示」 >「分割分頁」。

## 查看筆記本中繼資料

如要查看筆記本中繼資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 按一下要查看中繼資料的筆記本名稱。
5. 查看摘要詳細資料，瞭解筆記本的相關資訊，例如用於資料的[區域](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw#supported_regions)和上次修改日期。

## 使用筆記本版本

您可以選擇在[存放區](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw)內或外建立筆記本。Notebook 的版本管理方式會因 Notebook 的位置而異。

### 存放區中的 Notebook 版本管理

存放區是位於 BigQuery 或第三方供應商的 Git 存放區。您可以使用存放區中的[工作區](https://docs.cloud.google.com/bigquery/docs/workspaces-intro?hl=zh-tw)，對筆記本執行版本管控。詳情請參閱「[使用檔案版本管控功能](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw#use_version_control_with_a_file)」。

### 在存放區外管理 Notebook 版本

請參閱下列各節，瞭解如何查看、比較及還原筆記本版本。

#### 查看筆記本版本

如要查看筆記本版本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。按一下要查看版本記錄的筆記本名稱。
4. 如要依日期遞減順序查看筆記本版本清單，請按一下「Version history」(版本記錄) 圖示 schedule。

#### 比較筆記本版本

如要比較筆記本版本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 按一下要比較版本資訊的筆記本名稱。
5. 按一下 schedule「版本記錄」。
6. 按一下筆記本版本旁的 more\_vert「View actions」(查看動作)，然後點選「Compare」(比較)。比較窗格隨即開啟，比較您選取的筆記本版本與目前的筆記本版本。
7. 選用：如要並排比較版本，而非在不同窗格中比較，請依序按一下「Compare」(比較) 和「Inline」(並排)。
8. 選用：如要比較版本的原始碼，請依序按一下「Compare」(比較) 和「Show raw source」(顯示原始碼)。
9. 選用：如要在筆記本中隱藏指令輸出內容，請按一下「Compare」(比較)，然後取消選取「Show output」(顯示輸出內容)。

#### 還原筆記本版本

從比較窗格還原筆記本版本，可讓您比較筆記本的目前和先前版本，再選擇還原先前版本。還原筆記本會建立新版本，而非覆寫目前版本。不會遺失任何版本記錄。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 按一下要還原先前版本的筆記本名稱。
5. 按一下 schedule「版本記錄」。
6. 按一下版本旁的 more\_vert「View actions」(查看動作)，然後點選「Compare」(比較)。比較窗格隨即開啟，比較您選取的筆記本版本與最新筆記本版本。
7. 如要在比較後還原先前的筆記本版本，請按一下「Restore」(還原)。
8. 按一下「確認」。

## 重新命名筆記本

如要重新命名筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 點選要重新命名的筆記本。
5. 按一下 keyboard\_arrow\_down「Toggle header visibility」(切換標頭顯示設定)，展開選單列。
6. 依序點選**「檔案」 > 「重新命名」**。
7. 在「Rename notebook」(重新命名筆記本) 對話方塊中，輸入筆記本名稱，然後按一下「Rename」(重新命名)。

## 下載筆記本

如要下載筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 按一下要下載的筆記本名稱。您可以使用搜尋功能或篩選器尋找筆記本。
5. 展開選單列，然後前往「檔案」選單：
6. 選取「下載」，然後選取要下載的檔案類型。

## 刪除筆記本

如要刪除筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Notebooks」。
4. 找出要刪除的筆記本。
5. 按一下筆記本旁的 more\_vert「View actions」(查看動作)，然後點選「Delete」(刪除)。
6. 在對話方塊中輸入 `delete`，確認刪除。
7. 點選「刪除」。

## 在 Knowledge Catalog 管理中繼資料

[Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/introduction?hl=zh-tw) 可讓您儲存及管理 Notebook 的中繼資料。Notebooks 預設在 Knowledge Catalog 中提供，不需額外設定。

您可以使用 Knowledge Catalog，管理所有 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)中的筆記本。在 Knowledge Catalog 中管理筆記本時，須遵守 [Knowledge Catalog 配額和限制](https://docs.cloud.google.com/knowledge-catalog/docs/quotas?hl=zh-tw)，以及 [Knowledge Catalog 定價](https://cloud.google.com/dataplex/pricing?hl=zh-tw)。

Knowledge Catalog 會自動從筆記本擷取下列中繼資料：

* 資料資產名稱
* 資料資產父項
* 資料資產位置
* 資料資產類型
* 對應的 Google Cloud 專案

Knowledge Catalog 會將筆記本記錄為[項目](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entries)，並包含下列項目值：

系統項目群組
:   筆記本的[系統項目群組](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-groups)為 `@dataform`。如要在 Knowledge Catalog 中查看筆記本項目的詳細資料，您必須查看 `dataform` 系統項目群組。如要瞭解如何查看項目群組中所有項目的清單，請參閱 Knowledge Catalog 說明文件中的「[查看項目群組的詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-group-details)」。

系統項目類型
:   筆記本的[系統項目類型](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-types)為 `dataform-code-asset`。如要查看筆記本詳細資料，請查看 `dataform-code-asset` 系統項目類型，使用切面篩選器篩選結果，並[將 `dataform-code-asset` 切面中的 `type` 欄位設為 `NOTEBOOK`](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)。然後選取該筆記本中的項目。
    如要瞭解如何查看所選項目類型的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目類型的詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-type-details)」。如要瞭解如何查看所選項目的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw#view-entry-details)」一節。

系統切面類型
:   筆記本的[系統切面類型](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#aspect-types)為 `dataform-code-asset`。如要使用[切面](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#aspects)為筆記本項目加上註解，為 Knowledge Catalog 中的筆記本提供額外背景資訊，請查看 `dataform-code-asset` 切面類型，使用切面篩選器篩選結果，並[將 `dataform-code-asset` 切面中的 `type` 欄位設為 `NOTEBOOK`](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)。如要瞭解如何使用切面為項目加上註解，請參閱 Knowledge Catalog 說明文件中的「[管理切面並充實中繼資料](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw)」。

類型
:   資料畫布的類型為 `NOTEBOOK`。這種類型可讓您在[切面篩選器](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)中使用 `aspect:dataplex-types.global.dataform-code-asset.type=NOTEBOOK` 查詢，篩選 `dataform-code-asset` 系統項目類型和 `dataform-code-asset` 切面類型中的筆記本。

如要瞭解如何在 Knowledge Catalog 搜尋資產，請參閱 Knowledge Catalog 說明文件中的「[在 Knowledge Catalog 搜尋資料資產](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw)」。

## 疑難排解

詳情請參閱「[排解 Colab Enterprise 問題](https://docs.cloud.google.com/colab/docs/troubleshooting?hl=zh-tw)」。

## 後續步驟

* 進一步瞭解 [BigQuery 中的 Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)。
* 瞭解如何[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。
* 瞭解如何[排定筆記本執行作業](https://docs.cloud.google.com/bigquery/docs/orchestrate-notebooks?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]