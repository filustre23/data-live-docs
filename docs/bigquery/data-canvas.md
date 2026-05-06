Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過 BigQuery 資料畫布分析資料

本文說明如何使用資料畫布進行資料分析。您也可以使用 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/introduction?hl=zh-tw) 管理資料畫布中繼資料。

BigQuery 資料畫布是 [Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-overview?hl=zh-tw) 的功能，可讓您透過自然語言提示詞和圖形介面進行分析工作流程，進而尋找、轉換、查詢資料並以圖表呈現。

在分析工作流程中，BigQuery 資料畫布會使用[有向無環圖](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (DAG)，以圖形檢視工作流程。在 BigQuery 資料畫布中，您可以疊代查詢結果，並在單一位置處理多個查詢分支。

BigQuery 資料畫布旨在加速分析工作，協助資料專業人員 (例如資料分析師、資料工程師等) 進行資料到洞察的歷程。您不必具備特定工具的技術知識，只要熟悉如何讀取及撰寫 SQL 即可。BigQuery 資料畫布會搭配 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/introduction?hl=zh-tw) 中繼資料，根據自然語言找出合適的資料表。

BigQuery 資料畫布不適合由業務使用者直接使用。

BigQuery 資料畫布會使用 Gemini in BigQuery 尋找資料、建立 SQL、生成圖表及建立資料摘要。

瞭解 [Gemini for Google Cloud 如何使用您的資料](https://docs.cloud.google.com/gemini/docs/discover/data-governance?hl=zh-tw)。

## 功能

BigQuery 資料畫布可讓您執行下列操作：

* 使用自然語言查詢或[關鍵字搜尋語法](https://docs.cloud.google.com/data-catalog/docs/how-to/search-reference?hl=zh-tw)，搭配 Knowledge Catalog 中繼資料，找出資料表、檢視區塊或具體化檢視區塊等資產。
* 使用自然語言進行基本 SQL 查詢，例如：

  + 包含 `FROM` 子句、數學函式、陣列和結構體的查詢。
  + 兩個資料表的 `JOIN` 作業。
* 使用自然語言描述所需內容，即可建立自訂視覺化效果。
* 自動取得資料洞察。

## 限制

* 自然語言指令可能無法順利執行下列操作：

  + BigQuery ML
  + Apache Spark
  + 物件資料表
  + BigLake
  + `INFORMATION_SCHEMA` 個檢視表
  + JSON
  + 巢狀和重複欄位
  + 複雜函式和資料類型，例如 `DATETIME` 和 `TIMEZONE`
* 資料視覺化功能不適用於地域圖表。

## 提示最佳做法

只要使用適當的提示技巧，就能生成複雜的 SQL 查詢。以下建議有助於 BigQuery 資料畫布修正自然語言提示詞，提高查詢準確率：

* **清楚撰寫。**清楚說明要求，避免含糊不清。
* **直接提問。**如要獲得最精確的答案，請一次只問一個問題，並簡潔明瞭地提供提示。如果一開始的提示包含多個問題，請將問題的各個部分列出來，讓 Gemini 清楚瞭解。
* **提供明確的指示。**在提示中強調關鍵字詞。
* **指定作業順序。**以清楚且有條理的方式提供操作說明。將任務分成專注的小步驟。
* **反覆修正測試。**嘗試使用不同詞組和方法，找出最佳結果。

詳情請參閱 [BigQuery 資料畫布的提示最佳做法](https://cloud.google.com/blog/products/data-analytics/how-to-write-prompts-for-bigquery-data-canvas?hl=zh-tw)。

## 事前準備

1. [確認已為 Google Cloud 專案啟用 Gemini in BigQuery。](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)管理員通常會執行這個步驟。
2. 請確認您具備[必要的身分與存取權管理 (IAM) 權限](#required-roles)，可使用 BigQuery 資料畫布。
3. 如要在 Knowledge Catalog 中管理資料畫布中繼資料，請確保專案已啟用 [Dataplex API](https://docs.cloud.google.com/dataplex/docs/enable-api?hl=zh-tw)。 Google Cloud

### 必要的角色

如要取得使用 BigQuery 資料畫布所需的權限，請要求系統管理員在專案中授予您下列 IAM 角色：

* [BigQuery Studio 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.studioUser)  (`roles/bigquery.studioUser`)
* [Gemini 版 Google Cloud 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/cloudaicompanion?hl=zh-tw#cloudaicompanion.user)  (`roles/cloudaicompanion.user`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要在 Knowledge Catalog 中管理資料畫布中繼資料，請確認您具備必要的 [Knowledge Catalog 角色](https://docs.cloud.google.com/dataplex/docs/iam-roles?hl=zh-tw)和 [`dataform.repositories.get`](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#predefined-roles) 權限。

**注意：** 建立資料畫布時，BigQuery 會授予您該資料畫布的[Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。如果使用者在 Google Cloud 專案中獲派 Dataform 管理員角色，就能以擁有者身分存取專案中建立的所有資料畫布。如要覆寫這項行為，請參閱[在建立資源時授予特定角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-specific-role)。

## 節點類型

畫布是節點的集合，節點可按任意順序連接。BigQuery 資料畫布包含下列節點類型：

* 文字
* 搜尋
* 資料表
* SQL
* 目的地節點
* 視覺化
* 深入分析

### 文字節點

在 BigQuery 資料畫布中，文字節點可讓您在畫布中新增 RTF 格式內容。您可以在畫布中加入說明、附註或指示，方便自己和其他人瞭解分析的脈絡和目的。您可以在文字節點編輯器中輸入任何文字內容，包括用於設定格式的 Markdown。這項功能可讓您建立吸睛且資訊豐富的文字區塊。

您可以在文字節點中執行下列操作：

* 刪除節點。
* 偵錯節點。
* 複製節點。

### 搜尋節點

在 BigQuery 資料畫布中，搜尋節點可讓您尋找資料資產並納入畫布。這項功能就像橋樑，可連結自然語言查詢或關鍵字搜尋，以及您想使用的實際資料。

您可以使用自然語言或關鍵字提供搜尋查詢。搜尋節點會搜尋資料資產。這項功能會運用 Knowledge Catalog 中繼資料，強化內容認知能力。BigQuery 資料畫布也會建議最近使用的資料表、查詢和已儲存的查詢。

搜尋節點會傳回符合查詢條件的相關資料資產清單。並考量資料欄名稱和資料表說明。接著，您可以選取要新增至資料畫布的資產做為表格節點，進一步分析及視覺化呈現資料。

您可以在搜尋節點中執行下列操作：

* 刪除節點。
* 偵錯節點。
* 複製節點。

### 資料表節點

在 BigQuery 資料畫布中，資料表節點代表您已納入分析工作流程的特定資料表。代表您正在處理的資料，並可直接與資料互動。

資料表節點會顯示資料表相關資訊，例如名稱、結構定義和資料預覽畫面。您可以查看資料表結構定義、詳細資料和預覽畫面等詳細資料，與資料表互動。

在表格節點中，您可以執行下列操作：

* 刪除節點。
* 偵錯節點。
* 複製節點。
* 執行節點。
* 執行節點和下一個節點。

在資料畫布中，您可以執行下列操作：

* 在新 SQL 節點中查詢結果。
* 將結果聯結至其他資料表。

### SQL 節點

在 BigQuery 資料畫布中，SQL 節點可讓您直接在畫布中執行自訂 SQL 查詢。您可以直接在 SQL 節點編輯器中撰寫 SQL 程式碼，也可以使用自然語言提示生成 SQL。

SQL 節點會針對指定資料來源執行提供的 SQL 查詢。
SQL 節點會產生結果表格，然後可連線至畫布中的其他節點，以進行進一步分析或視覺化。SQL 節點執行作業的輸出內容 (又稱「查詢結果」) 也可以透過*目的地節點*保留在自己的資料表中。

查詢執行完畢後，您可以將查詢匯出為[排程查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)、[匯出查詢結果](https://docs.cloud.google.com/bigquery/docs/export-file?hl=zh-tw)，或[共用](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#share-saved-query)畫布，與[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)類似。

您可以在 SQL 節點執行下列操作：

* 將 SQL 陳述式匯出為排定的查詢。
* 刪除節點。
* 偵錯節點。
* 複製節點。
* 執行節點。
* 執行節點和下一個節點。

在資料畫布中，您可以執行下列操作：

* 在新 SQL 節點中查詢結果。
* 將結果儲存至資料表。
* 在視覺化節點中以視覺化方式呈現結果。
* 在洞察節點中生成結果的洞察資料。
* 將結果聯結至其他資料表。

### 目的地節點

在 BigQuery 資料畫布中，目的地節點是 SQL 節點的子項，可將 SQL 執行結果保留在專用資料表中。您可以將資料表儲存至新的或現有資料集，也可以儲存為資料集中的新資料表或現有資料表。建立目的地資料表後，使用 SQL 切換按鈕，在重新執行父項 SQL 節點時，即時更新資料表。

如果目的地節點與父項節點分離，且資料表內容不受父項 SQL 節點的任何上游變更影響，目的地節點就會變成資料表節點。

在目的地節點中，您可以執行下列操作：

* 將節點從父項節點分離，使其成為獨立的資料表節點。
* 在新 SQL 節點中查詢資料表。
* 將結果聯結至其他資料表。

### 圖表節點

在 BigQuery 資料畫布中，您可以透過視覺化節點以圖像方式呈現資料，輕鬆瞭解趨勢、模式和洞察資訊。並提供多種圖表類型供您選擇，讓您選取及自訂最適合資料的圖表。

視覺化節點會將表格做為輸入內容，這可能是 SQL 查詢或表格節點的結果。根據所選圖表類型和輸入表格中的資料，視覺化節點會產生圖表。您可以選取「自動圖表」，讓 BigQuery 為您的資料選取最佳圖表類型。視覺化節點隨即會顯示產生的圖表。

您可以透過視覺化節點自訂圖表，包括變更顏色、標籤和資料來源。您也可以將圖表匯出為 PNG 檔案。

使用下列圖表類型將資料視覺化：

* 長條圖
* 熱視圖
* 折線圖
* 圓餅圖
* 散布圖

在視覺化節點中，您可以執行下列操作：

* 將圖表匯出為 PNG 檔案。
* 偵錯節點。
* 複製節點。
* 執行節點。
* 執行節點和下一個節點。

在資料畫布中，您可以執行下列操作：

* 在洞察節點中生成結果的洞察資料。
* 編輯視覺化圖表。

### 洞察節點

在 BigQuery 資料畫布中，洞察節點可讓您從資料畫布中的資料生成洞察和摘要。協助您發掘模式、評估資料品質，以及在畫布上執行統計分析。這項工具可找出資料中的趨勢、模式、異常狀況和關聯性，並生成簡潔明瞭的資料分析結果摘要。

如要進一步瞭解資料洞察，請參閱「[在 BigQuery 中產生資料洞察](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)」一文。

您可以在洞察節點執行下列操作：

* 刪除節點。
* 複製節點。
* 執行節點。

## 使用 BigQuery 資料畫布

您可以在 Google Cloud 控制台、查詢或資料表中使用 BigQuery 資料畫布。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，按一下「SQL 查詢」add\_box旁邊的「建立新查詢」arrow\_drop\_down，然後點選「資料畫布」。
3. 在「自然語言」提示欄位中，輸入自然語言提示。

   舉例來說，如果您輸入 `Find me tables related to trees`，BigQuery 資料畫布會傳回可能的資料表清單，包括 `bigquery-public-data.usfs_fia.plot_tree` 或 `bigquery-public-data.new_york_trees.tree_species` 等公開資料集。
4. 請選取資料表。

   所選資料表的資料表節點會新增至 BigQuery 資料畫布。如要查看結構定義資訊、資料表詳細資料，或是預覽資料，請選取資料表節點中的相應分頁。
5. 選用：儲存資料畫布後，您可以使用下列工具列查看資料畫布詳細資料或[版本記錄](#view_and_compare_data_canvas_versions)、新增註解、回覆現有註解或取得註解連結：

   「註解」工具列功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。如要提供意見回饋或尋求這項功能的支援，請傳送電子郵件至 [bqui-workspace-pod@google.com](mailto:bqui-workspace-pod@google.com)。

### 畫布控制項

資料畫布工具列提供下列控制項，可新增節點及管理畫布檢視畫面：

* **搜尋**：在畫布中新增搜尋節點。
* **SQL**：在畫布上新增 SQL 節點。
* **文字**：為註解新增 Markdown 或文字節點。
* **縮放控制項**：可設定特定縮放等級。
* **縮放以符合畫面大小**：自動調整縮放比例，在畫布上顯示所有內容。
* **縮放至選取項目**：自動調整縮放比例，聚焦於所選節點。
* **放大**：放大畫布檢視畫面。你也可以按住 `Control` 鍵，並使用滑鼠滾輪捲動來放大畫面。
* **縮小**：縮小畫布檢視畫面。按住 `Control` 鍵並使用滑鼠滾輪捲動，即可縮小畫面。
* **全螢幕**：進入畫布的全螢幕模式。
* **整理畫布**：自動排列畫布上的節點。
* **重新整理畫布**：按一下按鈕即可執行所有可執行的節點。
* **更多動作**：開啟其他選項，例如清除畫布。

下列範例說明如何在分析工作流程中使用 BigQuery 資料畫布。

### 工作流程範例：尋找、查詢及視覺化呈現資料

在這個範例中，您會在 BigQuery 資料畫布中使用自然語言提示尋找資料、生成查詢，並編輯查詢。接著建立圖表。

#### 提示 1：尋找資料

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，按一下「SQL 查詢」add\_box旁邊的「建立新查詢」arrow\_drop\_down，然後點選「資料畫布」。
3. 按一下「搜尋資料」。
4. 按一下 filter\_list「編輯搜尋篩選器」，然後在「篩選搜尋結果」窗格中，將「BigQuery 公開資料集」切換鈕設為開啟。
5. 在「自然語言」提示欄位中，輸入下列自然語言提示：

   ```
   Chicago taxi trips
   ```

   BigQuery 資料畫布會根據 Knowledge Catalog 中繼資料，產生潛在資料表清單。您可以選取多個表格。
6. 選取「`bigquery-public-data.chicago_taxi_trips.taxi_trips`」表格，然後按一下「新增至畫布」。

   BigQuery 資料畫布會新增 `taxi_trips` 的資料表節點。如要查看結構定義資訊、資料表詳細資料，或是預覽資料，請選取資料表節點中的相應分頁。

#### 提示 2：在所選資料表中生成 SQL 查詢

Gemini for Google Cloud產品仍處於早期技術階段，因此可能會生成看似合理卻與事實不符的輸出內容。使用輸出內容前，請一律確認 Gemini for Google Cloud 產品輸出內容是否屬實。詳情請參閱「[Gemini for Google Cloud 和負責任的 AI 技術](https://docs.cloud.google.com/gemini/docs/discover/responsible-ai?hl=zh-tw)」。

如要為 `bigquery-public-data.chicago_taxi_trips.taxi_trips` 資料表生成 SQL 查詢，請按照下列步驟操作：

1. 在資料畫布中，按一下「查詢」。
2. 在「自然語言」提示欄位中輸入下列內容：

   ```
   Get me the 100 longest trips
   ```

   BigQuery 資料畫布會產生類似下列的 SQL 查詢：

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

如要編輯生成的查詢，可以手動編輯查詢，也可以變更自然語言提示並重新生成查詢。在本範例中，您使用自然語言提示編輯查詢，只選取顧客以現金付款的行程。

1. 在「自然語言」提示欄位中輸入下列內容：

   ```
   Get me the 100 longest trips where the payment type is cash
   ```

   BigQuery 資料畫布會產生類似下列的 SQL 查詢：

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
2. 如要查看查詢結果，請按一下「執行」。

#### 建立圖表

1. 在資料畫布中，按一下「視覺化」。
2. 按一下「建立長條圖」。

   BigQuery 資料畫布會建立長條圖，顯示各趟行程的里程數。除了提供圖表，BigQuery 資料畫布也會摘要顯示支援視覺化資料的一些重要詳細資料。
3. 選用：執行下列一或多項操作：

   * 如要修改圖表，請按一下「編輯」，然後在「編輯圖表」窗格中編輯圖表。
   * 如要共用資料畫布，請按一下「共用」，然後按一下「共用連結」，複製 BigQuery 資料畫布連結。
   * 如要清除資料畫布，請選取more\_vert **更多動作**，然後選取gavel **清除畫布**。這個步驟會產生空白畫布。

### 工作流程範例：聯結資料表

在本範例中，您要在 BigQuery 資料畫布中使用自然語言提示尋找資料並聯結資料表。然後將查詢匯出為筆記本。

#### 提示 1：尋找資料

1. 在「自然語言」提示欄位中，輸入下列提示：

   ```
   Information about trees
   ```

   BigQuery 資料畫布會建議多個含有樹木資訊的資料表。
2. 在本範例中，請選取 `bigquery-public-data.new_york_trees.tree_census_1995` 表格，然後按一下「新增至畫布」。

   畫布上會顯示表格。

#### 提示 2：根據地址聯結表格

1. 在資料畫布上，按一下「聯結」。

   BigQuery 資料畫布會建議要聯結的資料表。
2. 如要開啟新的**自然語言**提示欄位，請按一下「搜尋表格」。
3. 在「自然語言」提示欄位中，輸入下列提示：

   ```
   Information about trees
   ```
4. 選取 `bigquery-public-data.new_york_trees.tree_census_2005` 表格，然後按一下「新增至畫布」。

   畫布上會顯示表格。
5. 在資料畫布上，按一下「聯結」。
6. 在「On this canvas」(在這個畫布上) 區段中，選取「Table cell」(表格儲存格) 核取方塊，然後按一下「OK」(確定)。
7. 在「自然語言」提示欄位中，輸入下列提示：

   ```
   Join on address
   ```

   BigQuery 資料畫布會建議 SQL 查詢，根據地址聯結這兩個資料表：

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
8. 如要執行查詢並查看結果，請按一下「執行」。

#### 將查詢匯出為筆記本

BigQuery 資料畫布能將查詢匯出為筆記本。

1. 在資料畫布中，點選「匯出為筆記本」。
2. 在「儲存筆記本」窗格中，輸入筆記本名稱和要儲存的區域。
3. 按一下 [儲存]。筆記本已建立成功。
4. 選用：如要查看建立的筆記本，請按一下「開啟」。

### 工作流程範例：使用提示編輯圖表

在這個範例中，您會在 BigQuery 資料畫布中使用自然語言提示，尋找、查詢及篩選資料，然後編輯視覺化詳細資料。

#### 提示 1：尋找資料

1. 如要尋找美國名字的相關資料，請輸入下列提示：

   ```
   Find data about USA names
   ```

   BigQuery 資料畫布會產生資料表清單。
2. 在本範例中，請選取 `bigquery-public-data.usa_names.usa_1910_current` 表格，然後按一下「新增至畫布」。

#### 提示 2：查詢資料

1. 如要查詢資料，請在資料畫布中按一下「查詢」，然後輸入下列提示：

   ```
   Summarize this data
   ```

   BigQuery 資料畫布會產生類似下列的查詢：

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
2. 按一下「執行」。查詢結果隨即顯示。

#### 提示 3：篩選資料

1. 在資料畫布中，按一下「查詢這些結果」。
2. 如要篩選資料，請在「SQL」提示欄位中輸入下列提示：

   ```
   Get me the top 10 most popular names in 1980
   ```

   BigQuery 資料畫布會產生類似下列的查詢：

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

   執行查詢後，您會看到 1980 年出生的兒童最常見的十個名字。

#### 建立及編輯圖表

1. 在資料畫布中，按一下「視覺化」。

   BigQuery 資料畫布會建議多種視覺化選項，包括長條圖、圓餅圖、折線圖和自訂視覺化。
2. 在本範例中，請按一下「建立長條圖」。

   BigQuery 資料畫布會建立類似下方的長條圖：

除了提供圖表外，BigQuery 資料畫布還會摘要顯示支援視覺化效果的資料重要詳細資料。如要修改圖表，請按一下「視覺化詳細資料」，然後在側邊面板中編輯圖表。

#### 提示 4：編輯視覺化詳細資料

1. 在「視覺呈現」提示詞欄位中輸入下列內容：

   ```
   Create a bar chart sorted high to low, with a gradient
   ```

   BigQuery 資料畫布會建立類似下方的長條圖：
2. 選用：如要進一步變更，請按一下「編輯」。

   系統會顯示「編輯視覺化」窗格。你可以編輯詳細資料，例如圖表標題、X 軸名稱和 Y 軸名稱。此外，如果您按一下「JSON 編輯器」分頁，可以直接根據 JSON 值編輯圖表。

## 與 Gemini 助理合作

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或尋求這項功能支援，請傳送電子郵件至 [datacanvas-feedback@google.com](mailto:datacanvas-feedback@google.com)。

您可以使用 Gemini 支援的對話體驗，處理 BigQuery 資料畫布。對話式助理可根據您的要求建立節點、執行查詢及建立視覺化內容。您可以選擇要讓助理處理的表格，並新增指示來引導助理的行為。助理可處理新的或現有的資料畫布。

如要使用 Gemini 助理，請按照下列步驟操作：

1. 如要開啟助理，請在資料畫布上依序點選 spark「開啟資料畫布助理」。
2. 在「詢問資料問題」欄位中，輸入自然語言提示，例如下列任一項：

   * `Show me interesting statistics of my data.`
   * `Make a chart based on my data, sorted high to low.`
   * `I want to see sample data from my table.`

   回覆會根據要求包含一或多個節點。舉例來說，如果您要求助理建立資料圖表，助理會在資料畫布上建立視覺化節點。

   按一下「詢問資料問題」欄位時，您也可以執行下列操作：

   * 如要新增資料，請按一下「設定」。
   * 如要新增指示，請按一下「設定」。
3. 如要繼續使用助理，請新增其他自然語言提示。

在處理資料畫布時，您可以繼續使用自然語言提示。

### 新增資料

使用 Gemini 對話介面時，您可以新增資料，讓助理知道要參照哪個資料集。助理會要求你選取資料表，然後再執行任何提示。在助理中搜尋資料時，您可以將可搜尋的資料範圍限制為所有專案、已加星號的專案或目前專案。您也可以決定是否要在搜尋中納入公開資料集。

如要將資料新增至 Gemini 助理，請按照下列步驟操作：

1. 如要開啟助理，請在資料畫布上依序點選 spark「開啟資料畫布助理」。
2. 依序點選「設定」和「新增資料」。
3. 選用：如要擴大搜尋範圍，納入公開資料集，請點選「公開資料集」切換按鈕，將其設為開啟。
4. 選用：如要將搜尋結果的範圍變更為其他專案，請從「範圍」選單中選取適當的專案選項。
5. 勾選要新增至助理的每個表格。
   1. 如要搜尋助理未建議的表格，請按一下「搜尋表格」。
   2. 在「自然語言」提示欄位中，輸入說明您要尋找哪個資料表的提示，然後按 `Enter` 鍵。
   3. 找出要新增至助理的各個表格，勾選對應的核取方塊，然後按一下「確定」。
6. 關閉「畫布助理設定」窗格。

助理會根據您選擇的資料進行分析。

### 新增指示

使用 Gemini 對話介面時，你可以新增指令，讓助理瞭解該如何運作。這些指示會套用至資料畫布中的所有提示。潛在指令的例子包括：

* `Visualize trends over time.`
* `Chart colors: Red (negative), Green (positive)`
* `Domain: USA`

如要為助理新增指令，請按照下列步驟操作：

1. 如要開啟助理，請在資料畫布上依序點選 spark「開啟資料畫布助理」。
2. 按一下「設定」。
3. 在「Instructions」(指令) 欄位中，新增給助理的指令清單，然後關閉「Canvas assistant settings」(Canvas 助理設定) 窗格。

助理會記住這些指示，並套用至日後的提示。

### Gemini 助理最佳做法

使用 BigQuery 資料畫布助理時，請遵循下列最佳做法，以獲得最佳結果：

* **具體明確。**清楚說明要計算、分析或以視覺化方式呈現的內容。例如，說出 `Calculate the average trip duration for trips starting in council district
  eight`，而不是 `Analyze trip data`。
* **確保資料脈絡正確無誤。**助理只能使用您提供的資料。確認所有相關資料表和資料欄都已新增至畫布。
* **先從簡單的提示開始，然後逐步調整。**請先提出簡單的問題，確保助理瞭解基本結構和資料。舉例來說，先說「Ok Google」`Show total trips by subscriber_type`，再說「播放 YouTube TV」`Show total trips by subscriber_type and break down the result by
  council_district`。
* **拆解複雜問題。**如果是多步驟程序，請考慮清楚地撰寫提示，並將提示分成不同部分，或為每個主要步驟使用個別提示。例如說出「`First, find the top five busiest stations by
  trip count. Second, calculate the average trip duration for trips starting
  from only those top five stations`」。
* **清楚說明計算方式。**指定所選的計算方式，例如 `SUM`、
  `MAX` 或 `AVERAGE`。例如說出「`Find the MAX trip duration per
  bike_id`」。
* **使用系統指令，保留背景資訊和偏好設定。**使用[系統指令](#add_instructions)陳述適用於所有提示的資訊規則和偏好設定。
* **查看畫布。**請務必檢查生成的節點，確認邏輯符合要求，且結果準確無誤。
* **實驗。**嘗試使用不同的措辭、詳細程度和提示結構，瞭解助理如何回應您的特定資料和分析需求。
* **參照資料欄名稱。**請盡可能使用所選資料的實際欄名。例如，說「`Show the count of trips grouped by
  subscriber_type and start_station_name`」而不是「`Show trips by
  subscriber type`」。

### 工作流程範例：與 Gemini 助理合作

在本範例中，您會使用自然語言提示和 Gemini 助理，尋找、查詢及以圖表呈現資料。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，按一下「SQL 查詢」add\_box旁邊的「建立新查詢」arrow\_drop\_down，然後點選「資料畫布」。
3. 按一下「搜尋資料」。
4. 按一下 filter\_list「編輯搜尋篩選器」，然後在「篩選搜尋結果」窗格中，將「BigQuery 公開資料集」切換鈕設為開啟。
5. 在「自然語言」提示欄位中，輸入下列自然語言提示：

   ```
   bikeshare
   ```

   BigQuery 資料畫布會根據 Knowledge Catalog 中繼資料，產生潛在資料表清單。您可以選取多個表格。
6. 選取「`bigquery-public-data.austin_bikeshare.bikeshare_stations` 表格」和「`bigquery-public-data.austin_bikeshare.bikeshare_trips`」，然後按一下「新增至畫布」。

   系統會將所選資料表的資料表節點新增至 BigQuery 資料畫布。如要查看結構定義資訊、資料表詳細資料，或是預覽資料，請選取資料表節點中的相應分頁。
7. 如要開啟助理，請在資料畫布上依序點選 spark「開啟資料畫布助理」。
8. 按一下「設定」。
9. 在「Instructions」(指令) 欄位中，為助理新增下列指令：

   ```
   Tasks:
     - Visualize findings with charts
     - Show many charts per question
     - Make sure to cover each part via a separate line of reasoning
   ```
10. 關閉「畫布助理設定」窗格。
11. 在「詢問資料問題」欄位中，輸入下列自然語言提示：

    ```
    Show the number of trips by council district and subscriber type
    ```
12. 你可以在「詢問資料問題」欄位中繼續輸入提示。輸入下列自然語言提示：

    ```
    What are most popular stations among the top 5 subscriber types
    ```
13. 輸入最終提示：

    ```
    What station is least used to start and end a trip
    ```

    輸入所有相關提示後，畫布會根據你提供給助理的提示和指令，填入相關查詢和視覺化節點。繼續輸入提示或修改現有提示，取得所需結果。

## 查看所有資料畫布

如要查看專案中的所有資料畫布清單，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，點選「資料畫布」旁邊的「查看動作」圖示 more\_vert，然後執行下列其中一項操作：

* 如要在目前的分頁中開啟清單，請按一下「顯示全部」。
* 如要在新分頁中開啟清單，請依序點選 **「顯示全部」>「新分頁」**。
* 如要在分割分頁中開啟清單，請按一下「在『<』分割分頁中顯示全部」**>**。

## 查看資料畫布中繼資料

如要查看資料畫布中繼資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「資料畫布」。
4. 按一下要查看中繼資料的資料畫布名稱。
5. 按一下「詳細資料」info\_outline，即可查看資料畫布的相關資訊，例如使用的[區域](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#supported_regions)和上次修改日期。

## 使用資料畫布版本

您可以選擇在[存放區](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw)內或外部建立資料畫布。資料畫布的版本控管方式會因資料畫布所在位置而異。

### 存放區中的資料畫布版本管理

存放區是位於 BigQuery 或第三方供應商的 Git 存放區。您可以在存放區中使用[工作區](https://docs.cloud.google.com/bigquery/docs/workspaces-intro?hl=zh-tw)，對資料畫布執行版本控管。詳情請參閱「[使用檔案的版本管控功能](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw#use_version_control_with_a_file)」。

### 存放區外的資料畫布版本控管

您可以查看、比較及還原資料畫布版本。

#### 查看及比較資料畫布版本

如要查看資料畫布的不同版本，並與目前版本比較，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「資料畫布」。
4. 按一下要查看版本記錄的資料畫布名稱。
5. 按一下「版本記錄」schedule，即可查看資料畫布版本清單，並依日期降序排列。
6. 依序點選資料畫布版本旁的 more\_vert「查看動作」和「比較」。
   比較窗格隨即開啟，比較您選取的資料畫布版本與目前的資料畫布版本。
7. 選用：如要改為在同一窗格中比較版本，請依序點按「比較」和「內嵌」。

#### 還原資料畫布版本

從比較窗格還原資料畫布時，您可以先比較先前版本與目前版本，再選擇是否要還原。

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，然後按一下「資料畫布」。
3. 按一下要還原先前版本的資料畫布名稱。
4. 按一下 schedule「版本記錄」。
5. 找到要還原的資料畫布版本，然後依序點選旁邊的 more\_vert「查看動作」和「比較」。

   比較窗格隨即開啟，比較您選取的資料畫布版本與最新版本。
6. 如要在比較後還原先前的資料畫布版本，請按一下「還原」。
7. 按一下「確認」。

## 管理 Knowledge Catalog 中的中繼資料

[Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/introduction?hl=zh-tw) 可讓您查看及管理資料畫布的中繼資料。根據預設，Knowledge Catalog 會提供資料畫布，不需額外設定。

您可以使用 Knowledge Catalog 管理所有 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)的資料畫布。
在 Knowledge Catalog 中管理資料畫布時，須遵守 [Knowledge Catalog 配額和限制](https://docs.cloud.google.com/dataplex/docs/quotas?hl=zh-tw)，以及 [Knowledge Catalog 定價](https://cloud.google.com/dataplex/pricing?hl=zh-tw)。

Knowledge Catalog 會自動從資料畫布擷取下列中繼資料：

* 資料資產名稱
* 資料資產父項
* 資料資產位置
* 資料資產類型
* 對應 Google Cloud 專案

Knowledge Catalog 會將資料畫布記錄為[項目](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entries)，並提供下列項目值：

系統項目群組
:   資料畫布的[系統項目群組](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-groups)為 `@dataform`。如要在 Knowledge Catalog 中查看資料畫布項目的詳細資料，請查看 `dataform` 系統項目群組。如需查看項目群組中所有項目的清單，請參閱 Knowledge Catalog 說明文件中的「[查看項目群組的詳細資料](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-group-details)」。�

系統項目類型
:   資料畫布的[系統項目類型](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-types)為 `dataform-code-asset`。[如要查看資料畫布的詳細資料，請查看 `dataform-code-asset` 系統項目類型、使用切面篩選器篩選結果，並將 `dataform-code-asset` 切面內的 `type` 欄位設為 `DATA_CANVAS`](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)。然後選取所選資料畫布的項目。
    如要瞭解如何查看所選項目類型的詳細資料，請參閱 Knowledge Catalog 說明文件中的「[查看項目類型的詳細資料](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-tw#entry-type-details)」。如需查看所選項目詳細資料的操作說明，請參閱 Knowledge Catalog 說明文件中的「[查看項目的詳細資料](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-tw#view-entry-details)」一節。

系統切面類型
:   資料畫布的[系統切面類型](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw#aspect-types)為 `dataform-code-asset`。如要透過[切面](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw#aspects)註解資料畫布項目，為 Knowledge Catalog 中的資料畫布提供額外背景資訊，請查看 `dataform-code-asset` 切面類型、使用以切面為準的篩選器篩選結果，並[將 `dataform-code-asset` 切面內的 `type` 欄位設為 `DATA_CANVAS`](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)。如需如何使用切面註解項目的操作說明，請參閱 Knowledge Catalog 說明文件中的「[管理切面及豐富中繼資料](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw)」一文。

類型
:   資料畫布的類型為 `DATA_CANVAS`。
    您可以使用`aspect:dataplex-types.global.dataform-code-asset.type=DATA_CANVAS`
    [以切面為準的篩選器](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw#aspect-search)中的查詢，依`dataform-code-asset`
    系統項目類型和`dataform-code-asset`切面類型篩選資料畫布。

如需在 Knowledge Catalog 中搜尋資產的操作說明，請參閱 Knowledge Catalog 說明文件中的「[在 Knowledge Catalog 中搜尋資料資產](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-tw)」。

## 定價

如要瞭解這項功能的定價詳情，請參閱 [Gemini in BigQuery 定價總覽](https://cloud.google.com/products/gemini/pricing?hl=zh-tw#gemini-in-bigquery-pricing)。

## 位置

您可以在所有 [BigQuery 地理位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)使用 BigQuery 資料畫布。如要瞭解 Gemini in BigQuery 在何處處理資料，請參閱「[Gemini in BigQuery 在何處處理資料](https://docs.cloud.google.com/bigquery/docs/gemini-locations?hl=zh-tw)」。

## 提供意見回饋

您可以向 Google 提交意見回饋，協助我們提升 BigQuery 資料畫布建議的品質。如要提供意見，請按照下列步驟操作：

1. 在 BigQuery 資料畫布工具列中，依序點按「更多動作」more\_vert和「提交意見回饋」。
2. 按一下意見回饋適用的類別。
3. 在「請提供詳細意見 (必填)」欄位中輸入意見。
4. 選用：如要提供資料畫布的螢幕截圖給 BigQuery，請按一下「screenshot\_monitor」圖示 screenshot\_monitor「擷取螢幕截圖」。
5. 選用：如要提供生成記錄，請選取「允許 Google 收集我的生成記錄，並與意見回饋一同提交」。
6. 按一下 [傳送]。

資料共用設定會套用至整個專案，而且只有具備 `serviceusage.services.enable` 和 `serviceusage.services.list` IAM 權限的專案管理員能夠設定。

如要直接提供這項功能的意見回饋，也可以傳送電子郵件至 [datacanvas-feedback@google.com](mailto:datacanvas-feedback@google.com)。

## 後續步驟

* 瞭解如何[使用 Gemini 輔助功能撰寫查詢](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw)。
* 瞭解如何[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。
* 瞭解如何使用[資料洞察](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)，生成有關資料的自然語言查詢。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]