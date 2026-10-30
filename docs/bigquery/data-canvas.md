Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過 BigQuery 資料畫布分析資料

在 BigQuery 資料畫布，您可以透過自然語言提示和圖形介面，尋找、轉換、查詢資料，並以圖表呈現。您可以與這項 [Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-overview?hl=zh-tw) 功能互動，在單一位置反覆調整查詢結果，並探索多個查詢分支。

BigQuery 資料畫布會使用[有向無環圖](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (DAG) 呈現工作流程的圖形檢視畫面，BigQuery 資料畫布旨在加速分析工作，並協助資料分析師、資料工程師等資料專業人員，完成從資料到洞察的流程。您不需要具備特定工具的技術知識，只要熟悉 SQL 的基本讀寫操作即可。BigQuery 資料畫布會與 [Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/introduction?hl=zh-tw) 中繼資料搭配使用，根據自然語言找出適當的資料表。

瞭解 [Gemini for Google Cloud 如何使用您的資料](https://docs.cloud.google.com/gemini/docs/discover/data-governance?hl=zh-tw)。

## 功能

BigQuery 資料畫布可讓您執行下列操作：

* 使用[自然語言搜尋](https://docs.cloud.google.com/knowledge-catalog/docs/about-search?hl=zh-tw)功能，搭配 Knowledge Catalog 中繼資料，尋找資料表、檢視表或 materialized view 等資產。
* 使用自然語言執行基本 SQL 查詢，例如：

  + 包含 `FROM` 子句、數學函式、陣列和結構體的查詢。
  + 兩個資料表的 `JOIN` 作業。
* 使用自然語言描述所需內容，建立自訂圖表。
* 自動生成資料洞察。

## 限制

* 自然語言指令可能不適用於下列情況：

  + BigQuery ML
  + Apache Spark
  + 物件資料表
  + BigLake
  + `INFORMATION_SCHEMA` 個檢視表
  + JSON
  + 巢狀和重複欄位
  + 複雜函式和資料類型，例如 `DATETIME` 和 `TIMEZONE`
* 資料視覺化不適用於地理區域圖表。
* BigQuery 資料畫布不適合業務使用者直接使用。

## 提示最佳做法

只要使用適當的提示技術，就能生成複雜的 SQL 查詢。下列建議有助於 BigQuery 資料畫布修正自然語言提示，提高查詢準確度：

* **清楚表達。**清楚說明要求，避免含糊不清。
* **直接提問。**為取得最精確的答案，請一次提出一個問題，並保持提示簡潔。如果一開始的提示包含多個問題，請將問題的各個部分分項列出，讓 Gemini 清楚瞭解。
* **給予明確具體的指示。**在提示中強調關鍵字詞。
* **指定運算順序。**請以清楚且有條理的方式提供操作說明。將任務分成小而專注的步驟。
* **修正及反覆測試。**嘗試不同的詞組和方法，看看哪種效果最好。

詳情請參閱「[BigQuery 資料畫布的提示最佳做法](https://cloud.google.com/blog/products/data-analytics/how-to-write-prompts-for-bigquery-data-canvas?hl=zh-tw)」。

## 事前準備

1. [確認 Google Cloud 專案已啟用 Gemini in BigQuery。](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)這個步驟通常由管理員執行。
2. 確認您具備[必要的 Identity and Access Management (IAM) 權限](#required-roles)，可使用 BigQuery 資料畫布。
3. 如要在 Knowledge Catalog 管理資料畫布中繼資料，請確認 Google Cloud 專案已啟用 [Dataplex API](https://docs.cloud.google.com/knowledge-catalog/docs/enable-api?hl=zh-tw)。

### 必要的角色

如要取得使用 BigQuery 資料畫布所需的權限，請要求管理員授予您下列專案 IAM 角色：

* [BigQuery Studio 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.studioUser)  (`roles/bigquery.studioUser`)
* Gemini for Google Cloud 使用者 (`roles/cloudaicompanion.user`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要在 Knowledge Catalog 中管理資料畫布中繼資料，請確認您具備必要的 [Knowledge Catalog 角色](https://docs.cloud.google.com/knowledge-catalog/docs/iam-roles?hl=zh-tw)和 [`dataform.repositories.get`](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#predefined-roles) 權限。

**注意：** 建立資料畫布時，BigQuery 會授予您該資料畫布的 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。凡是具備 Google Cloud 專案 Dataform 管理員角色的使用者，都擁有該專案中所有資料畫布的擁有者存取權。如要覆寫這項行為，請參閱「[在建立資源時授予特定角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-specific-role)」。

### 資料畫布的安全考量

BigQuery 中的程式碼資產是由 Dataform 提供，因此請考量下列安全性影響，再授予使用者這些資產的存取權：

* 程式碼資產的瀏覽權限由專案層級的 Dataform 權限控管。使用者只要具備 `dataform.repositories.list` 權限 (包含在標準 BigQuery 角色中，例如 [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)、[BigQuery Studio 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser)和 [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user))，就能在 Google Cloud 專案的「Explorer」面板中查看所有程式碼資產，無論這些資產是否由他們建立或與他們共用。如要限制瀏覽權限，可以建立不含 `dataform.repositories.list` 權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。
* 凡是與 Dataform 服務代理共用的 Secret，都有可能遭到可編輯這些資產的使用者存取。為確保憑證安全，請限制只有信任的使用者才能建立及編輯權限，並限制 Dataform 服務代理可存取的密鑰。詳情請參閱「[在套件安裝期間存取 Secret](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#secret-access-risk)」。

詳情請參閱「[Dataform 權限的安全性考量](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#security-considerations-permissions)」。

## 節點類型

畫布內含一或多個節點，節點可以任何順序連接。BigQuery 資料畫布有下列節點類型：

* 文字
* 搜尋
* 資料表
* SQL
* 目的地節點
* 圖表
* 深入分析

### 文字節點

在 BigQuery 資料畫布中，文字節點可讓您在畫布中新增 RTF 格式內容。您可以在畫布中加入說明、附註或指示，方便自己和他人瞭解分析的背景資訊和目的。您可以在文字節點編輯器中輸入任何文字內容，包括用於設定格式的 Markdown。這項功能可讓您建立美觀且資訊豐富的文字區塊。

在文字節點中，您可以執行下列操作：

* 刪除節點。
* 對節點進行偵錯。
* 複製節點。

### 搜尋節點

在 BigQuery 資料畫布中，搜尋節點可讓您尋找資料資產並納入畫布。這項功能可做為橋梁，連結自然語言查詢或關鍵字搜尋，以及您要處理的實際資料。

您可以使用自然語言或關鍵字提供搜尋查詢。搜尋節點會搜尋資料資產。這項功能會運用 Knowledge Catalog 中繼資料，強化內容認知能力。BigQuery 資料畫布也會建議最近使用的資料表、查詢和已儲存的查詢。

搜尋節點會傳回符合查詢條件的相關資料資產清單。並考量資料欄名稱和資料表說明。接著，您可以選取要新增至資料畫布的資產，做為資料表節點，進一步分析資料並以圖表呈現。

在搜尋節點中，您可以執行下列操作：

* 刪除節點。
* 對節點進行偵錯。
* 複製節點。

### 資料表節點

在 BigQuery 資料畫布中，資料表節點代表您已納入分析工作流程的特定資料表。代表您正在處理的資料，並可讓您直接與資料互動。

資料表節點會顯示資料表的相關資訊，例如名稱、結構定義和資料預覽。您可以查看資料表結構定義、資料表詳細資料和資料表預覽等詳細資料，與資料表互動。

在表格節點中，您可以執行下列操作：

* 刪除節點。
* 對節點進行偵錯。
* 複製節點。
* 執行節點。
* 執行該節點和後續節點。

在資料畫布中，您可以執行下列操作：

* 在新的 SQL 節點中查詢結果。
* 將結果與其他資料表彙整。

### SQL 節點

在 BigQuery 資料畫布中，SQL 節點可讓您直接在畫布中執行自訂 SQL 查詢。您可以直接在 SQL 節點編輯器中編寫 SQL 程式碼，或使用自然語言提示詞生成 SQL。

SQL 節點會對指定的資料來源執行提供的 SQL 查詢。SQL 節點會產生結果資料表，可連結至畫布中的其他節點，以便進一步分析或視覺化。執行 SQL 節點的輸出內容稱為「查詢結果」，也可以透過「目的地節點」保留至專屬資料表。

查詢執行完畢後，您可以將其匯出為[排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)、[匯出查詢結果](https://docs.cloud.google.com/bigquery/docs/export-file?hl=zh-tw)，或[共用](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#share-saved-query)畫布，就像[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)一樣。

在 SQL 節點中，您可以執行下列操作：

* 將 SQL 陳述式匯出為排定的查詢。
* 刪除節點。
* 對節點進行偵錯。
* 複製節點。
* 執行節點。
* 執行該節點和後續節點。

在資料畫布中，您可以執行下列操作：

* 在新的 SQL 節點中查詢結果。
* 將結果儲存至資料表。
* 在視覺化節點中以圖表呈現結果。
* 在洞察節點中生成結果的洞察。
* 將結果與其他資料表彙整。

### 目的地節點

在 BigQuery 資料畫布中，目的地節點是 SQL 節點的子項，會將 SQL 執行結果保留至專屬資料表。您可以將資料表儲存在新的或現有資料集中，也可以儲存為資料集中的新資料表或現有資料表。建立目的地資料表後，請使用 SQL 切換鈕，在重新執行父項 SQL 節點時，即時更新資料表。

目的地節點與父項分離後，可成為資料表節點，且資料表的內容不會受到父項 SQL 節點任何上游變更的影響。

在目的地節點，您可以執行下列操作：

* 將節點與父項分離，使其成為獨立的資料表節點。
* 在新的 SQL 節點中查詢資料表。
* 將結果與其他資料表彙整。

### 圖表節點

在 BigQuery 資料畫布中，圖表節點可讓您以視覺化方式呈現資料，更輕鬆地瞭解趨勢、模式和洞察資訊。提供多種圖表類型，方便您選取及自訂最適合資料的圖表。

圖表節點會將資料表做為輸入內容，這可以是 SQL 查詢或資料表節點的結果。視覺化節點會根據所選圖表類型和輸入表格中的資料，生成圖表。您可以選取「Auto-Chart」(自動圖表)，讓 BigQuery 為資料選取最合適的圖表類型。視覺化節點會顯示生成的圖表。

您可以使用視覺化節點自訂圖表，包括變更顏色、標籤和資料來源。也可以將圖表匯出為 PNG 檔案。

使用下列圖表類型呈現資料：

* 長條圖
* 熱視圖
* 折線圖
* 圓餅圖
* 散布圖

在圖表節點中，您可以執行下列操作：

* 將圖表匯出為 PNG 檔案。
* 對節點進行偵錯。
* 複製節點。
* 執行節點。
* 執行該節點和後續節點。

在資料畫布中，您可以執行下列操作：

* 在洞察節點中生成結果的洞察。
* 編輯圖表。

### 洞察節點

在 BigQuery 資料畫布中，洞察節點可讓您根據資料畫布中的資料生成洞察和摘要。這項功能可協助您在畫布上發掘模式、評估資料品質，以及執行統計分析。這項功能可找出資料中的趨勢、模式、異常狀況和關聯，並生成簡潔明瞭的資料分析結果摘要。

如要進一步瞭解資料洞察，請參閱「[在 BigQuery 中生成資料洞察](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)」。

在洞察節點中，您可以執行下列操作：

* 刪除節點。
* 複製節點。
* 執行節點。

## 使用 BigQuery 資料畫布

您可以在 Google Cloud 控制台、查詢或資料表中使用 BigQuery 資料畫布。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，按一下「SQL 查詢」add\_box 旁的「新建」arrow\_drop\_down，選取「AI 與知識」，然後點選「資料畫布」。
3. 在「自然語言」提示詞欄位中，輸入自然語言提示詞。

   舉例來說，如果輸入 `Find me tables related to trees`，BigQuery 資料畫布會傳回可能資料表的清單，包括 `bigquery-public-data.usfs_fia.plot_tree` 或 `bigquery-public-data.new_york_trees.tree_species` 等公開資料集。
4. 請選取資料表。

   所選資料表的資料表節點會新增至 BigQuery 資料畫布。如要查看結構定義資訊、資料表詳細資料，或是預覽資料，請選取資料表節點中的相應分頁。
5. 選用：儲存資料畫布後，您可以使用下列工具列查看資料畫布詳細資料或[版本記錄](#view_and_compare_data_canvas_versions)、新增註解，或回覆/取得現有註解的連結：

   「Comments」(註解) 工具列功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。如要提供意見回饋或尋求支援，請傳送電子郵件至 [bqui-workspace-pod@google.com](mailto:bqui-workspace-pod@google.com)。

### 畫布控制項

資料畫布工具列提供下列控制項，可用於新增節點及管理畫布檢視畫面：

* **搜尋**：在畫布中新增搜尋節點。
* **SQL**：在畫布中新增 SQL 節點。
* **Text**：新增 Markdown 或文字節點，用於註解。
* **縮放控制項**：可設定特定縮放等級。
* **縮放至符合大小**：自動調整縮放比例，在畫布上顯示所有內容。
* 「Zoom to Selection」(縮放至所選項目)：自動調整縮放比例，聚焦於所選節點。
* **放大**：放大畫布檢視畫面。按住 `Control` 鍵並使用滑鼠滾輪，也可以放大畫面。
* **縮小**：縮小畫布檢視畫面。按住 `Control` 鍵並使用滑鼠滾輪捲動，即可縮小畫面。
* **全螢幕**：進入畫布的全螢幕模式。
* **整理畫布**：自動排列畫布上的節點。
* **重新整理畫布**：按一下按鈕，即可執行所有可執行的節點。
* **更多動作**：開啟其他選項，例如清除畫布。

以下範例說明在分析工作流程中，使用 BigQuery 資料畫布的不同方式。

### 畫布設定

「Canvas settings」(畫布設定) 窗格提供下列選項：

* **位置**：資料畫布的處理[位置](#supported-locations)。詳情請參閱「[指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)」。
* **查詢參數**：新增[參數](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw)，用於資料畫布的 SQL 查詢。
* **資源管理**：管理[查詢工作優先順序](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)、[快取](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)和[工作設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#query_and_job_execution_settings)。
* **畫布管理**：控管資料畫布上的查詢輸出內容顯示方式。
* 「Advanced options」(進階選項)：選取 Google-owned and Google-managed encryption key 或[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/kms/docs/cmek?hl=zh-tw)，並設定查詢的[計費位元組數上限](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#restrict-bytes-billed)。

如要變更資料畫布設定，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 展開專案名稱，然後點選「資料畫布」。
4. 在「Data canvases」(資料畫布) 頁面，按一下要更新的畫布連結。
5. 按一下 settings「Canvas settings」(Canvas 設定)。
6. 在「位置」部分，選擇下列其中一個選項：

   1. 選取「Automatic location selection」(自動選取位置)，允許 BigQuery 根據您查詢的資源自動決定處理位置。
   2. 或者，如要手動轉送工作，請按照下列步驟操作：

      1. 取消選取「Automatic location selection」(自動選取位置)，然後選取「Location type」(位置類型)，例如「Region」(區域) 或「Multi-region」(多區域)。
      2. 在「region」(區域) 欄位中指定區域，或在「multi-region」(多區域) 欄位中指定多區域。
      3. (選用) 在「Reservation」(預留項目) 部分，選擇要用於 Canvas 工作的預留項目。
7. 在「Query parameters」(查詢參數) 部分，選擇下列任一選項：

   1. 按一下「Add parameter」(新增參數)，定義要在畫布中 SQL 查詢使用的標準參數。
   2. 輸入參數的名稱、類型和值。**注意：** Google Cloud 控制台中的查詢參數只支援原始類型。
   如果是 `ARRAY`、`STRUCT` 和 `JSON` 等複雜類型，請使用 `bq` 指令列工具或 BigQuery API。
8. 在「資源管理」部分，選擇下列任一選項：

   1. 在「Job priority」(工作優先順序) 部分，選擇要以「Interactive」(互動式) 或「Batch」(批次) 優先順序執行 Canvas 查詢。
   2. 在「Cache preference」(快取偏好設定) 部分，選取「Use cached results」(使用快取結果)，允許 BigQuery 傳回先前快取的查詢結果。使用快取結果可降低成本並提升效能。
   3. 在「Job timeout」(工作逾時) 部分，輸入工作執行時間上限 (以毫秒為單位)。如果超過這個時間限制，BigQuery 會嘗試停止工作。
9. 在「Canvas management」(畫布管理) 區段，取消選取「Omit node output when saving this canvas」(儲存這個畫布時，省略節點輸出內容)，即可快取查詢結果和畫布狀態。這只會儲存畫布結構和查詢。
10. 展開「Advanced options」(進階選項) 區段，然後選擇下列任一選項：

    1. 在「Encryption」(加密) 部分，選擇「Google-managed keys」(Google 代管金鑰) 或「Cloud KMS key」(Cloud KMS 金鑰)，然後輸入客戶自行管理金鑰的類型和值。
    2. 在「Maximum bytes billed」(計費位元組上限) 中，輸入查詢的計費位元組上限。如果查詢超出這個上限，就會失敗，不會產生費用。如未指定這個選項，計費位元組數上限會設為專案預設值。
11. 完成變更後，按一下「Save」(儲存)，將設定套用至資料畫布。

### 工作流程範例：尋找、查詢及視覺化資料

在這個範例中，您會在 BigQuery 資料畫布使用自然語言提示，尋找資料、生成查詢及編輯查詢。接著，您會建立圖表。

#### 提示 1：尋找資料

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，按一下「SQL 查詢」add\_box 旁的「新建」arrow\_drop\_down，選取「AI 與知識」，然後點選「資料畫布」。
3. 按一下「搜尋資料」。
4. 按一下「filter\_list」filter\_list**「Edit search filters」(編輯搜尋篩選器)**，然後在「Filter search」(篩選搜尋) 窗格中，將「BigQuery public datasets」(BigQuery 公開資料集) 切換鈕設為開啟。
5. 在「自然語言」提示詞欄位，輸入下列自然語言提示詞：

   ```
   Chicago taxi trips
   ```

   BigQuery 資料畫布會根據 Knowledge Catalog 中繼資料，生成潛在資料表清單。您可以選取多個資料表。
6. 選取 `bigquery-public-data.chicago_taxi_trips.taxi_trips` 資料表，然後按一下「Add to canvas」(新增至畫布)。

   `taxi_trips` 的資料表節點會新增至 BigQuery 資料畫布。如要查看結構定義資訊、資料表詳細資料，或是預覽資料，請選取資料表節點中的相應分頁。

#### 提示 2：在所選資料表中生成 SQL 查詢

Gemini for Google Cloud產品仍處於早期技術階段，因此可能會生成看似合理卻與事實不符的輸出內容。使用輸出內容前，請一律確認 Gemini for Google Cloud 產品輸出內容是否屬實。詳情請參閱「[Gemini for Google Cloud 和負責任的 AI 技術](https://docs.cloud.google.com/gemini/docs/discover/responsible-ai?hl=zh-tw)」。

如要為 `bigquery-public-data.chicago_taxi_trips.taxi_trips` 資料表生成 SQL 查詢，請按照下列步驟操作：

1. 在資料畫布中，點選「查詢」。
2. 在「自然語言」提示詞欄位輸入下列內容：

   ```
   Get me the 100 longest trips
   ```

   BigQuery 資料畫布會生成類似下列內容的 SQL 查詢：

   ```
   SELECT
     taxi_id,
     trip_start_timestamp,
     trip_end_timestamp,
     trip_miles
   FROM
     `bigquery-public-data.chicago_taxi_trips.taxi_trips`
   ORDER BY
     trip_miles DESC
   LIMIT
     100;
   ```

#### 提示 3：編輯查詢

如要編輯生成的查詢，可以手動編輯，也可以變更自然語言提示，然後重新生成查詢。在這個範例中，您會使用自然語言提示編輯查詢，只選取顧客以現金付款的行程。

1. 在「自然語言」提示詞欄位輸入下列內容：

   ```
   Get me the 100 longest trips where the payment type is cash
   ```

   BigQuery 資料畫布會生成類似下列內容的 SQL 查詢：

   ```
   SELECT
     taxi_id,
     trip_start_timestamp,
     trip_end_timestamp,
     trip_miles
   FROM
     `PROJECT_ID.chicago_taxi_trips_123123.taxi_trips`
   WHERE
     payment_type = 'Cash'
   ORDER BY
     trip_miles DESC
   LIMIT
     100;
   ```

   在上述範例中，`PROJECT_ID` 是 Google Cloud 專案的 ID。
2. 如要查看查詢結果，請點選「執行」。

#### 建立圖表

1. 在資料畫布中，點選「圖表呈現」。
2. 點選「建立長條圖」。

   BigQuery 資料畫布會建立長條圖，依行程 ID 顯示行程里程數。除了提供圖表，BigQuery 資料畫布也會摘要說明視覺化圖表資料的部分重要細節。
3. 選用：執行下列一或多項操作：

   * 如要修改圖表，請按一下「Edit」(編輯)，然後在「Edit visualization」(編輯圖表) 窗格中編輯圖表。
   * 如要共用資料畫布，請依序點選「Share」(共用) 和「Share Link」(共用連結)，複製 BigQuery 資料畫布連結。
   * 如要清理資料畫布，請依序選取 more\_vert「More actions」(更多動作) 和 gavel「Clear canvas」(清除畫布)。這個步驟會產生空白畫布。

### 工作流程範例：彙整資料表

在本範例中，您會在 BigQuery 資料畫布中使用自然語言提示，尋找資料並彙整資料表。接著，您會將查詢匯出為筆記本。

#### 提示 1：尋找資料

1. 在「自然語言」提示詞欄位輸入下列提示詞：

   ```
   Information about trees
   ```

   BigQuery 資料畫布會建議幾個含有樹木資訊的資料表。
2. 在本範例中，請選取 `bigquery-public-data.new_york_trees.tree_census_1995` 資料表，然後按一下「Add to canvas」(新增至畫布)。

   表格會顯示在畫布上。

#### 提示 2：依地址彙整資料表

1. 在資料畫布上，按一下「Join」(彙整)。

   BigQuery 資料畫布會建議要彙整的資料表。
2. 如要開啟新的「Natural language」(自然語言) 提示欄位，請按一下「Search for tables」(搜尋資料表)。
3. 在「自然語言」提示詞欄位輸入下列提示詞：

   ```
   Information about trees
   ```
4. 選取 `bigquery-public-data.new_york_trees.tree_census_2005` 資料表，然後點選「Add to canvas」(新增至畫布)。

   表格會顯示在畫布上。
5. 在資料畫布上，按一下「Join」(彙整)。
6. 在「On this canvas」(在這個畫布上) 區段中，勾選「Table cell」(表格儲存格) 核取方塊，然後按一下「OK」(確定)。
7. 在「自然語言」提示詞欄位輸入下列提示詞：

   ```
   Join on address
   ```

   BigQuery 資料畫布會建議 SQL 查詢，依地址彙整這兩個資料表：

   ```
   SELECT
     *
   FROM
     `bigquery-public-data.new_york_trees.tree_census_2015` AS t2015
   JOIN
     `bigquery-public-data.new_york_trees.tree_census_1995` AS t1995
   ON
     t2015.address = t1995.address;
   ```
8. 如要執行查詢並查看結果，請點選「執行」。

#### 將查詢匯出為筆記本

BigQuery 資料畫布能將查詢匯出為筆記本。

1. 在資料畫布中，點選「匯出為筆記本」。
2. 在「Save Notebook」(儲存筆記本) 窗格中，輸入筆記本名稱和要儲存的區域。
3. 按一下 [儲存]。筆記本已建立成功。
4. 選用：如要查看建立的筆記本，請按一下「開啟」。

### 工作流程範例：使用提示編輯圖表

在這個範例中，您會在 BigQuery 資料畫布使用自然語言提示，尋找、查詢及篩選資料，然後編輯圖表詳細資料。

#### 提示 1：尋找資料

1. 如要尋找美國姓名的資料，請輸入下列提示：

   ```
   Find data about USA names
   ```

   BigQuery 資料畫布會生成資料表清單。
2. 在本範例中，請選取 `bigquery-public-data.usa_names.usa_1910_current` 資料表，然後按一下「Add to canvas」(新增至畫布)。

#### 提示 2：查詢資料

1. 如要查詢資料，請在資料畫布中按一下「Query」(查詢)，然後輸入下列提示：

   ```
   Summarize this data
   ```

   BigQuery 資料畫布會生成類似下列內容的查詢：

   ```
   SELECT
     state,
     gender,
     year,
     name,
     number
   FROM
     `bigquery-public-data.usa_names.usa_1910_current`
   ```
2. 按一下「執行」。系統會顯示查詢結果。

#### 提示 3：篩選資料

1. 在資料畫布中，點選「查詢這些結果」。
2. 如要篩選資料，請在「SQL」提示詞欄位中輸入下列提示詞：

   ```
   Get me the top 10 most popular names in 1980
   ```

   BigQuery 資料畫布會生成類似下列內容的查詢：

   ```
   SELECT
     name,
     SUM(number) AS total_count
   FROM
     `bigquery-public-data`.usa_names.usa_1910_current
   WHERE
     year = 1980
   GROUP BY
     name
   ORDER BY
     total_count DESC
   LIMIT
     10;
   ```

   執行查詢後，您會看到一份資料表，列出 1980 年出生的兒童中最常見的十個名字。

#### 建立及編輯圖表

1. 在資料畫布中，點選「圖表呈現」。

   BigQuery 資料畫布會建議多種圖表選項，包括長條圖、圓餅圖、折線圖和自訂圖表。
2. 在本範例中，請點選「建立長條圖」。

   BigQuery 資料畫布會建立類似下方的長條圖：

除了提供圖表外，BigQuery 資料畫布也會摘要說明圖表資料的一些重要細節。如要修改圖表，請按一下「Visualization details」(圖表詳細資料)，然後在側邊面板中編輯圖表。

#### 提示 4：編輯圖表詳細資料

1. 在「視覺化」提示詞欄位中，輸入下列內容：

   ```
   Create a bar chart sorted high to low, with a gradient
   ```

   BigQuery 資料畫布會建立類似下方的長條圖：
2. 選用：如要進一步變更，請按一下「編輯」。

   「編輯圖表」窗格隨即顯示。您可以編輯圖表標題、x 軸名稱和 y 軸名稱等詳細資料。此外，如果按一下「JSON Editor」(JSON 編輯器) 分頁標籤，即可根據 JSON 值直接編輯圖表。

## 與 Gemini 助理合作

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或尋求這項功能的支援，請傳送電子郵件至 [datacanvas-feedback@google.com](mailto:datacanvas-feedback@google.com)。

您可以使用 Gemini 支援的對話功能，操作 BigQuery 資料畫布。對話助理可根據您的要求建立節點、執行查詢及建立圖表。您可以選擇要讓助理處理哪些資料表，並新增指示來引導助理的行為。助理可與新的或現有的資料畫布搭配使用。

如要使用 Gemini 助理，請按照下列步驟操作：

1. 如要開啟助理，請在資料畫布上按一下「spark」圖示，然後點選「開啟資料畫布助理」。
2. 在「Ask a data question」(提出資料問題) 欄位中，輸入自然語言提示，例如：

   * `Show me interesting statistics of my data.`
   * `Make a chart based on my data, sorted high to low.`
   * `I want to see sample data from my table.`

   回覆會根據要求，包含一或多個節點。舉例來說，如果您要求助理建立資料圖表，助理就會在資料畫布上建立圖表節點。

   按一下「提出資料問題」欄位，也可以執行下列操作：

   * 如要新增資料，請按一下「設定」。
   * 如要新增指令，請按一下「設定」。
3. 如要繼續使用助理，請新增其他自然語言提示。

使用資料畫布時，您可以繼續輸入自然語言提示。

### 新增資料

使用 Gemini 對話介面時，您可以新增資料，讓助理知道要參照哪個資料集。執行任何提示前，助理會要求您選取資料表。在助理中搜尋資料時，您可以將可搜尋資料的範圍限制為所有專案、已加星號的專案或目前專案。您也可以決定是否要在搜尋中加入公開資料集。

如要將資料新增至 Gemini 助理，請按照下列步驟操作：

1. 如要開啟助理，請在資料畫布上按一下「spark」圖示，然後點選「開啟資料畫布助理」。
2. 依序點選「設定」和「新增資料」。
3. 選用：如要展開搜尋結果，納入公開資料集，請將「Public datasets」(公開資料集) 切換鈕設為開啟。
4. 選用：如要將搜尋結果範圍變更為其他專案，請從「Scope」(範圍) 選單中選取適當的專案選項。
5. 找出要新增至助理的資料表，並勾選對應的核取方塊。
   1. 如要搜尋助理未建議的資料表，請按一下「Search for tables」(搜尋資料表)。
   2. 在「Natural language」(自然語言) 提示詞欄位中，輸入提示詞來描述要尋找的資料表，然後按下 `Enter` 鍵。
   3. 勾選要新增至助理的資料表，然後按一下「Ok」(確定)。
6. 關閉「Canvas assistant settings」(畫布助理設定) 窗格。

助理會根據您選擇的資料進行分析。

### 新增指示

使用 Gemini 對話介面時，您可以新增指令，讓助理知道如何運作。這些指示會套用至資料畫布中的所有提示。潛在指令範例如下：

* `Visualize trends over time.`
* `Chart colors: Red (negative), Green (positive)`
* `Domain: USA`

如要新增助理的操作說明，請按照下列步驟操作：

1. 如要開啟助理，請在資料畫布上按一下「spark」圖示，然後點選「開啟資料畫布助理」。
2. 按一下「設定」。
3. 在「Instructions」(操作說明) 欄位中，新增助理的操作說明清單，然後關閉「Canvas assistant settings」(Canvas 助理設定) 窗格。

助理會記住這些指示，並套用到日後的提示。

### Gemini 助理最佳做法

如要充分發揮 BigQuery 資料畫布助理的效用，請遵循下列最佳做法：

* **具體明確。**清楚說明要計算、分析或以視覺化方式呈現的內容。例如，請說 `Calculate the average trip duration for trips starting in council district
  eight`，而不是 `Analyze trip data`。
* **確保資料情境準確無誤。**助理只能處理您提供的資料。確認所有相關資料表和資料欄都已新增至畫布。
* **先從簡單的開始，然後逐步調整。**先提出簡單的問題，確保助理瞭解基本結構和資料。例如，先說 `Show total trips by subscriber_type`，再說 `Show total trips by subscriber_type and break down the result by
  council_district`。
* **拆解複雜問題。**如果流程包含多個步驟，請考慮在提示中清楚區分各個部分，或為每個主要步驟使用不同的提示。例如，說出「`First, find the top five busiest stations by
  trip count. Second, calculate the average trip duration for trips starting
  from only those top five stations`」。
* **清楚說明計算方式。**指定所選計算，例如 `SUM`、`MAX` 或 `AVERAGE`。例如，說出「`Find the MAX trip duration per
  bike_id`」。
* **使用系統指令，設定持續有效的背景資訊和偏好設定。**使用[系統指令](#add_instructions)，說明適用於所有提示的資訊規則和偏好設定。
* **查看畫布。**請務必檢查生成的節點，確認邏輯符合要求，且結果準確無誤。
* **實驗。**嘗試不同的措辭、詳細程度和提示結構，瞭解助理如何回應您的特定資料和分析需求。
* **參照資料欄名稱。**請盡可能使用所選資料的實際資料欄名稱。例如，請說「`Show the count of trips grouped by
  subscriber_type and start_station_name`」，而不是「`Show trips by
  subscriber type`」。

### 工作流程範例：與 Gemini 助理合作

在本範例中，您將使用自然語言提示和 Gemini 助理，尋找、查詢資料並以圖表呈現。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，按一下「SQL 查詢」add\_box 旁的「新建」arrow\_drop\_down，選取「AI 與知識」，然後點選「資料畫布」。
3. 按一下「搜尋資料」。
4. 按一下「filter\_list」filter\_list**「Edit search filters」(編輯搜尋篩選器)**，然後在「Filter search」(篩選搜尋) 窗格中，將「BigQuery public datasets」(BigQuery 公開資料集) 切換鈕設為開啟。
5. 在「自然語言」提示詞欄位，輸入下列自然語言提示詞：

   ```
   bikeshare
   ```

   BigQuery 資料畫布會根據 Knowledge Catalog 中繼資料，生成潛在資料表清單。您可以選取多個資料表。
6. 選取 `bigquery-public-data.austin_bikeshare.bikeshare_stations` 資料表和 `bigquery-public-data.austin_bikeshare.bikeshare_trips`，然後按一下「Add to canvas」(新增至畫布)。

   BigQuery 資料畫布會為每個所選資料表新增資料表節點。如要查看結構定義資訊、資料表詳細資料，或是預覽資料，請選取資料表節點中的相應分頁。
7. 如要開啟助理，請在資料畫布上按一下「spark」圖示，然後點選「開啟資料畫布助理」。
8. 按一下「設定」。
9. 在「Instructions」(操作說明) 欄位中，為助理新增下列操作說明：

   ```
   Tasks:
     - Visualize findings with charts
     - Show many charts per question
     - Make sure to cover each part via a separate line of reasoning
   ```
10. 關閉「Canvas assistant settings」(畫布助理設定) 窗格。
11. 在「Ask a data question」(提出資料問題) 欄位中，輸入下列自然語言提示：

    ```
    Show the number of trips by council district and subscriber type
    ```
12. 您可以繼續在「提出資料問題」欄位中輸入提示。輸入下列自然語言提示：

    ```
    What are most popular stations among the top 5 subscriber types
    ```
13. 輸入最後一個提示詞：

    ```
    What station is least used to start and end a trip
    ```

    提出所有相關提示後，畫布會根據您提供給助理的提示和指示，填入相關查詢和視覺化節點。繼續輸入提示或修改現有提示，取得所需結果。

## 查看所有資料畫布

如要查看專案中所有資料畫布的清單，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，點選「Data canvases」(資料畫布) 旁邊的 more\_vert「View actions」(查看動作)，然後執行下列任一操作：

* 如要在目前的分頁中開啟清單，請按一下「顯示全部」。
* 如要在新分頁中開啟清單，請依序點選「在新分頁中顯示全部」>「新分頁」。
* 如要在分割分頁中開啟清單，請依序點選 **「全部顯示」 > 「分割分頁」**。

## 查看資料畫布中繼資料

如要查看資料畫布中繼資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「資料畫布」。
4. 按一下要查看中繼資料的資料畫布名稱。
5. 按一下「info\_outline Details」(詳細資料)，即可查看資料畫布的相關資訊，例如使用的[區域](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#supported_regions)和上次修改日期。

## 使用資料畫布版本

您可以選擇在[存放區](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw)內或外建立資料畫布。資料畫布版本管理方式會因資料畫布所在位置而異。

### 存放區中的資料畫布版本管理

存放區是位於 BigQuery 或第三方供應商的 Git 存放區。您可以使用存放區中的[工作區](https://docs.cloud.google.com/bigquery/docs/workspaces-intro?hl=zh-tw)，對資料畫布執行版本管控。詳情請參閱「[使用檔案版本管控功能](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw#use_version_control_with_a_file)」。

### 在存放區外建立資料畫布版本

您可以查看、比較及還原資料畫布版本。

#### 查看及比較資料畫布版本

如要查看資料畫布的不同版本，並與目前版本比較，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「資料畫布」。
4. 按一下要查看版本記錄的資料畫布名稱。
5. 按一下「schedule 版本記錄」，即可查看資料畫布版本清單，依日期遞減排序。
6. 按一下資料畫布版本旁的 more\_vert「View actions」(查看動作)，然後點選「Compare」(比較)。比較窗格隨即開啟，比較您選取的資料畫布版本與目前的資料畫布版本。
7. 選用：如要直接在同一頁面比較版本，而非在不同窗格中比較，請依序按一下「Compare」(比較) 和「Inline」(內嵌)。

#### 還原資料畫布版本

從比較窗格還原，可讓您比較資料畫布的先前版本和目前版本，再選擇是否還原。

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，然後點選「資料畫布」。
3. 按一下要還原先前版本的資料畫布名稱。
4. 按一下 schedule「版本記錄」。
5. 按一下要還原的資料畫布版本旁的 more\_vert「View actions」(查看動作)，然後點選「Compare」(比較)。

   比較窗格隨即開啟，比較您選取的資料畫布版本與最新資料畫布版本。
6. 如要在比較後還原先前的資料畫布版本，請按一下「Restore」(還原)。
7. 按一下「確認」。

## 在 Knowledge Catalog 管理中繼資料

[Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/introduction?hl=zh-tw) 可讓您查看及管理資料畫布的中繼資料。Knowledge Catalog 預設提供資料畫布，無須額外設定。

您可以使用 Knowledge Catalog，管理所有 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)中的資料畫布。在 Knowledge Catalog 管理資料畫布時，須遵守 [Knowledge Catalog 配額和限制](https://docs.cloud.google.com/knowledge-catalog/docs/quotas?hl=zh-tw)，以及 [Knowledge Catalog 定價](https://cloud.google.com/dataplex/pricing?hl=zh-tw)。

Knowledge Catalog 會自動從資料畫布擷取下列中繼資料：

* 資料資產名稱
* 資料資產父項
* 資料資產位置
* 資料資產類型
* 對應的 Google Cloud 專案

Knowledge Catalog 會將資料畫布記錄為[項目](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entries)，並使用下列項目值：

系統項目群組
:   資料畫布的[系統項目群組](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-groups)為 `@dataform`。如要在 Knowledge Catalog 查看資料畫布項目的詳細資料，您必須查看 `dataform` 系統項目群組。如要瞭解如何查看項目群組中所有項目的清單，請參閱 Knowledge Catalog 說明文件中的「[查看項目群組的詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-group-details)」。

系統項目類型
:   資料畫布的[系統項目類型](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-types)為 `dataform-code-asset`。如要查看資料畫布的詳細資料，請查看 `dataform-code-asset` 系統項目類型，使用切面篩選器篩選結果，並[將 `dataform-code-asset` 切面中的 `type` 欄位設為 `DATA_CANVAS`](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)。然後選取所選資料畫布的項目。如要瞭解如何查看所選項目類型的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目類型的詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw#entry-type-details)」。如要瞭解如何查看所選項目的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目詳細資料](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw#view-entry-details)」一節。

系統切面類型
:   資料畫布的[系統切面類型](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#aspect-types)為 `dataform-code-asset`。如要使用[切面](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#aspects)為資料畫布項目加上註解，為 Knowledge Catalog 中的資料畫布提供額外背景資訊，請查看 `dataform-code-asset` 切面類型，使用切面篩選器篩選結果，並[將 `dataform-code-asset` 切面中的 `type` 欄位設為 `DATA_CANVAS`](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)。如要瞭解如何使用切面為項目加上註解，請參閱 Knowledge Catalog 說明文件中的「[管理切面並充實中繼資料](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw)」。

類型
:   資料畫布的類型為 `DATA_CANVAS`。這種類型可讓您在`dataform-code-asset`系統項目類型和`dataform-code-asset`切面類型中，使用`aspect:dataplex-types.global.dataform-code-asset.type=DATA_CANVAS`查詢，在[切面篩選器](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw#aspect-search)中篩選資料畫布。

如要瞭解如何在 Knowledge Catalog 搜尋資產，請參閱 Knowledge Catalog 說明文件中的「[在 Knowledge Catalog 搜尋資料資產](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw)」。

## 定價

如要瞭解這項功能的定價，請參閱「[Gemini in BigQuery 定價總覽](https://cloud.google.com/products/gemini/pricing?hl=zh-tw#gemini-in-bigquery-pricing)」。

## 位置

您可以在所有 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)使用 BigQuery 資料畫布。如要瞭解 Gemini in BigQuery 處理資料的位置，請參閱「[Gemini in BigQuery 處理資料的位置](https://docs.cloud.google.com/bigquery/docs/gemini-locations?hl=zh-tw)」。

## 提供意見回饋

您可以向 Google 提交意見回饋，協助我們提升 BigQuery 資料畫布建議的品質。如要提供意見，請按照下列步驟操作：

1. 在 BigQuery 資料畫布工具列中，按一下 more\_vert「More actions」(更多動作)，然後點選「Submit feedback」(提交意見回饋)。
2. 按一下意見回饋適用的類別。
3. 在「請提供詳細意見 (必填)」欄位中輸入意見。
4. 選用：如要提供資料畫布的螢幕截圖給 BigQuery，請按一下「screenshot\_monitor 擷取螢幕截圖」。
5. 選用：如要提供生成記錄，請選取「允許 Google 收集我的生成記錄，並與意見回饋一同提交」。
6. 按一下 [傳送]。

資料共用設定會套用至整個專案，而且只有具備 `serviceusage.services.enable` 和 `serviceusage.services.list` IAM 權限的專案管理員能夠設定。

如要直接提供這項功能的意見回饋，也可以傳送電子郵件至 [datacanvas-feedback@google.com](mailto:datacanvas-feedback@google.com)。

## 後續步驟

* 瞭解如何[在 Gemini 協助下撰寫查詢](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw)。
* 瞭解如何[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。
* 瞭解如何運用[資料洞察](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)，生成關於資料的自然語言查詢。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-28 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-28 (世界標準時間)。"],[],[]]