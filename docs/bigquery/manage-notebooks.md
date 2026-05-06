Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理筆記本

本文說明如何管理 [BigQuery 中的 Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)，包括如何查看、比較、還原及刪除筆記本。

本文也說明如何在 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/introduction?hl=zh-tw) 中查看及管理筆記本中繼資料。

筆記本是 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 的程式碼資產，由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 提供支援。

## 事前準備

1. [建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。
2. 如要在 Knowledge Catalog 中管理 Notebook 中繼資料，請確保專案已啟用 [Dataplex API](https://docs.cloud.google.com/dataplex/docs/enable-api?hl=zh-tw)。 Google Cloud

### 所需權限

如要共用筆記本，您需要下列 Identity and Access Management (IAM) 角色：

* [BigQuery 作業使用者 (`roles/bigquery.jobUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)
* [BigQuery Read Session User (`roles/bigquery.readSessionUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser)
* [資源層級的程式碼擁有者 (`roles/dataform.codeOwner`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner)。

如要儲存及刪除筆記本，您必須具備下列 IAM 角色：

* [BigQuery 作業使用者 (`roles/bigquery.jobUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)
* [BigQuery Read Session User (`roles/bigquery.readSessionUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser)
* [程式碼擁有者 (`roles/dataform.codeOwner`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner)
  或[程式碼編輯者 (`roles/dataform.codeEditor`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor)

如要使用筆記本修訂版本，您需要下列 IAM 角色：

* [BigQuery 作業使用者 (`roles/bigquery.jobUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)
* [BigQuery Read Session User (`roles/bigquery.readSessionUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser)
* 下列任一角色：

  + [程式碼擁有者 (`roles/dataform.codeOwner`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner)
  + [程式碼編輯器 (`roles/dataform.codeEditor`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor)
  + [程式碼檢視器 (`roles/dataform.codeViewer`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer)

如要進一步瞭解 BigQuery IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」一文。

如要在 Knowledge Catalog 中管理筆記本中繼資料，請確認您具備必要的 [Knowledge Catalog 角色](https://docs.cloud.google.com/dataplex/docs/iam-roles?hl=zh-tw)。

## 授予筆記本存取權

如要授權其他使用者存取筆記本，請將這些使用者新增至適當的 IAM 角色。

**重要事項：** 只要使用者具備筆記本存取權，即可查看筆記本中程式碼產生的所有輸出內容，即便內含使用者無權存取的資料表內容也一樣。如要避免共用已儲存的輸出內容，請[停用筆記本輸出內容儲存功能](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#disable_output_saving)。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
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

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 找出要共用的記事本。你可以使用搜尋功能或篩選器尋找筆記本。
5. 按一下筆記本旁邊的「查看動作」more\_vert，然後依序點選「分享」>「複製連結」。
6. 將連結分享給其他使用者。

## 查看所有筆記本

如要查看專案中的所有筆記本清單，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中，點選「Notebooks」旁邊的「View actions」圖示 more\_vert，然後執行下列其中一項操作：

* 如要在目前的分頁中開啟清單，請按一下「顯示全部」。
* 如要在新分頁中開啟清單，請依序點選「顯示全部」 >「新分頁」。
* 如要在分割分頁中開啟清單，請依序點選「顯示所有項目」 >「分割分頁」。

## 查看筆記本中繼資料

如要查看筆記本中繼資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下要查看中繼資料的筆記本名稱。
5. 查看摘要詳細資料，瞭解筆記本的相關資訊，例如用於資料的[區域](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw#supported_regions)，以及上次修改的日期。

## 使用筆記本版本

您可以選擇在[存放區](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw)內或外部建立筆記本。筆記本的版本控管方式會因筆記本所在位置而異。

### 存放區中的筆記本版本管理

存放區是位於 BigQuery 或第三方供應商的 Git 存放區。您可以在存放區中使用[工作區](https://docs.cloud.google.com/bigquery/docs/workspaces-intro?hl=zh-tw)，對筆記本執行版本控管。詳情請參閱「[使用檔案的版本管控功能](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw#use_version_control_with_a_file)」。

### 在存放區外部管理筆記本版本

請參閱下列各節，瞭解如何查看、比較及還原筆記本版本。

#### 查看筆記本版本

如要查看筆記本版本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。按一下要查看版本記錄的記事本名稱。
4. 如要查看依日期降序排列的筆記本版本清單，請按一下 schedule「版本記錄」。

#### 比較筆記本版本

如要比較筆記本版本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下要比較版本資訊的筆記本名稱。
5. 按一下 schedule「版本記錄」。
6. 按一下筆記本版本旁的 more\_vert「查看動作」，然後按一下「比較」。
   比較窗格隨即開啟，比較您選取的記事本版本與目前的記事本版本。
7. 選用：如要改為在同一窗格中比較版本，請依序點按「比較」和「內嵌」。
8. 選用：如要比較版本原始碼，請按一下「比較」，然後按一下「顯示原始碼」。
9. 選用：如要隱藏筆記本中的指令輸出，請按一下 **比較**，然後取消選取 **顯示輸出**。

#### 還原筆記本版本

從比較窗格還原記事本版本時，您可以先比較記事本的目前版本和先前版本，再選擇是否要還原先前版本。還原筆記本時，系統會建立新版本的筆記本，而不是覆寫目前版本。不會遺失任何版本記錄。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下要還原先前版本的記事本名稱。
5. 按一下 schedule「版本記錄」。
6. 按一下版本旁的 more\_vert「查看動作」，然後點選「比較」。
   比較窗格隨即開啟，比較您選取的筆記本版本與最新版本。
7. 比較後如要還原先前的記事本版本，請按一下「還原」。
8. 按一下「確認」。

## 下載筆記本

如要下載筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下要下載的筆記本名稱。你可以使用搜尋功能或篩選器尋找筆記本。
5. 展開選單列，然後前往「檔案」選單：
6. 選取「下載」，然後選取要下載檔案的檔案類型。

## 刪除筆記本

如要刪除筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 找出要刪除的記事本。
5. 按一下筆記本旁的 more\_vert「查看動作」，然後按一下「刪除」。
6. 如要確認刪除，請在對話方塊中輸入 `delete`。
7. 按一下「Delete」(刪除)。

## 在 Knowledge Catalog 中管理中繼資料

[知識目錄](https://docs.cloud.google.com/dataplex/docs/introduction?hl=zh-tw)可讓您儲存及管理筆記本的中繼資料。根據預設，筆記本會顯示在知識目錄中，不需額外設定。

您可以使用 Knowledge Catalog 管理所有 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)的筆記本。在 Knowledge Catalog 中管理 Notebooks 時，須遵守 [Knowledge Catalog 配額與限制](https://docs.cloud.google.com/dataplex/docs/quotas?hl=zh-tw)，以及 [Knowledge Catalog 定價](https://cloud.google.com/dataplex/pricing?hl=zh-tw)。

Knowledge Catalog 會自動從筆記本擷取下列中繼資料：

* 資料資產名稱
* 資料資產父項
* 資料資產位置
* 資料資產類型
* 對應 Google Cloud 專案

知識目錄會將筆記本記錄為[項目](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entries)，並提供下列項目值：

系統項目群組
:   筆記本的[系統項目群組](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-groups)為 `@dataform`。如要查看知識目錄中的筆記本項目詳細資料，請查看 `dataform` 系統項目群組。如需查看項目群組中所有項目的清單，請參閱知識目錄說明文件中的「[查看項目群組的詳細資料](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-group-details)」一節。

系統項目類型
:   筆記本的[系統項目類型](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-types)為 `dataform-code-asset`。如要查看筆記本詳細資料，您需要查看 `dataform-code-asset` 系統項目類型、使用切面篩選器篩選結果，並[將 `dataform-code-asset` 切面內的 `type` 欄位設為 `NOTEBOOK`](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)。然後選取所選筆記本的項目。
    如要瞭解如何查看所選項目類型的詳細資料，請參閱知識目錄說明文件中的「[查看項目類型的詳細資料](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-type-details)」。如需查看所選項目詳細資料的操作說明，請參閱知識目錄說明文件中的「[查看項目的詳細資料](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-tw#view-entry-details)」一節。

系統切面類型
:   筆記本的[系統切面類型](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw#aspect-types)為 `dataform-code-asset`。如要透過標註[切面](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw#aspects)，為知識型錄中的筆記本提供額外背景資訊，請查看 `dataform-code-asset` 切面類型、使用以切面為準的篩選器篩選結果，然後將 `dataform-code-asset` 切面內的 `type` 欄位設為 `NOTEBOOK`。[如需如何使用層面註解項目，請參閱 Knowledge Catalog 說明文件中的「[管理層面及豐富中繼資料](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw)」一文。](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)

類型
:   資料畫布的類型為 `NOTEBOOK`。
    您可以使用`aspect:dataplex-types.global.dataform-code-asset.type=NOTEBOOK`[以切面為準的篩選器](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)，在`dataform-code-asset`系統項目類型和`dataform-code-asset`切面類型中，透過查詢篩選筆記本。

如需在 Knowledge Catalog 中搜尋資產的操作說明，請參閱 Knowledge Catalog 說明文件中的「[在 Knowledge Catalog 中搜尋資料資產](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-tw)」。

## 疑難排解

詳情請參閱「[排解 Colab Enterprise 問題](https://docs.cloud.google.com/colab/docs/troubleshooting?hl=zh-tw)」。

## 後續步驟

* 進一步瞭解 [BigQuery 中的 Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)。
* 瞭解如何[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。
* 瞭解如何[排定筆記本執行時間](https://docs.cloud.google.com/bigquery/docs/orchestrate-notebooks?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]