Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 搭配 BigQuery 使用 Colab Enterprise 資料科學代理

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋、提出問題或要求停用這項預先發布版功能，請傳送電子郵件至 [vertex-notebooks-previews-external@google.com](mailto:vertex-notebooks-previews-external@google.com)，或填寫 [資料科學代理公開預先發布版停用表單](https://forms.gle/KuTAunuLT2YmFAcs8)。

Colab Enterprise 和 BigQuery 的資料科學代理 (DSA) 可在 Colab Enterprise 筆記本中，自動執行探索性資料分析、機器學習工作，以及提供洞察資訊。

## 事前準備

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).

1. 啟用 BigQuery、Vertex AI、Dataform 和 Compute Engine API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Caiplatform.googleapis.com%2Cdataform.googleapis.com%2Ccompute.googleapis.com&hl=zh-tw)

   新專案會自動啟用 BigQuery API。

如果您剛開始使用 BigQuery 中的 Colab Enterprise，請參閱「[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#required_permissions)」頁面的設定步驟。

## 限制

* 資料科學代理僅適用於 Colab Enterprise 環境。
* 資料科學代理支援下列資料來源：
  + CSV 檔案
  + BigQuery 資料表
* 資料科學代理產生的程式碼只會在筆記本的執行階段中執行。
* 如果專案已啟用 VPC Service Controls，則不支援資料科學代理。
* 使用 `@mention` 函式搜尋 BigQuery 資料表時，只能搜尋目前專案。使用資料表選取器在專案中搜尋。
* `@mention` 函式只會搜尋 BigQuery 資料表。
  如要搜尋可上傳的資料檔案，請使用 `+` 符號。
* 資料科學代理中的 PySpark 只會生成 Managed Service for Apache Spark 4.0 程式碼。DSA 可協助您升級至 Managed Service for Apache Spark 4.0，但如果需要使用舊版，則不應使用資料科學代理。

## 何時使用資料科學代理

資料科學代理可協助您處理各種工作，包括探索性資料分析，以及生成機器學習預測和預報。動態搜尋廣告的用途如下：

* **大規模資料處理**：使用 BigQuery ML、BigQuery DataFrames 或 Managed Service for Apache Spark，對大型資料集執行分散式資料處理作業。這樣您就能有效率地清除、轉換及分析資料，即使資料過大，無法放入單一機器的記憶體也沒問題。
* **生成計畫**：生成及修改計畫，使用 Python、SQL、Managed Service for Apache Spark 和 BigQuery DataFrames 等常見工具完成特定工作。
* **資料探索**：探索資料集以瞭解其結構、找出潛在問題 (例如遺漏值和離群值)，並使用 Python 或 SQL 檢查重要變數的分布情形。
* **資料清理**：清理資料。舉例來說，您可以移除離群值資料點。
* **資料整理**：使用單一熱編碼或標籤編碼等技術，或使用 BigQuery ML [特徵轉換工具](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-transform?hl=zh-tw)，將類別特徵轉換為數值表示法。建立新的分析功能。
* **資料分析**：分析不同變數之間的關係。計算數值特徵之間的關聯性，並探索類別特徵的分布情形。找出資料中的模式和趨勢。
* **資料視覺化**：建立直方圖、箱形圖、散布圖和長條圖等視覺化內容，呈現個別變數的分布情形和變數之間的關係。您也可以使用 Python，為儲存在 BigQuery 中的資料表建立視覺化效果。
* **特徵工程**：從經過清理的資料集設計新特徵。
* **資料分割**：將經過工程處理的資料集分割為訓練、驗證和測試資料集。
* **模型訓練**：使用 pandas DataFrame (`X_train`、`y_train`)、[BigQuery DataFrame](https://docs.cloud.google.com/bigquery/docs/dataframes-ml-ai?hl=zh-tw#train-models)、[PySpark DataFrame](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html) 中的訓練資料，或使用 BigQuery ML [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)和 BigQuery 資料表，訓練模型。
* **模型最佳化**：使用驗證集將模型最佳化。
  探索 `DecisionTreeRegressor` 和 `RandomForestRegressor` 等替代模型，並比較其效能。
* **模型評估**：使用 pandas DataFrame、BigQuery DataFrames 或 PySpark DataFrame，評估測試資料集的模型效能。您也可以使用 BigQuery ML [模型評估函式](https://docs.cloud.google.com/bigquery/docs/evaluate-overview?hl=zh-tw)，評估模型品質並比較模型，適用於使用 BigQuery ML 訓練的模型。
* **模型推論**：使用 BigQuery ML [推論函式](https://docs.cloud.google.com/bigquery/docs/inference-overview?hl=zh-tw)，對 BigQuery ML 訓練的模型、匯入的模型和遠端模型執行推論作業。您也可以使用 BigFrames `model.predict()` 方法或 PySpark [轉換器](https://spark.apache.org/docs/latest/ml-pipeline.html#transformers)進行預測。

## 在 BigQuery 中使用資料科學代理

下列步驟說明如何在 BigQuery 中使用資料科學代理。

1. 建立或開啟 Colab Enterprise 筆記本。
2. 選用：透過下列任一方式參照資料：

   * 上傳 CSV 檔案，或在提示中使用 `+` 符號搜尋可用檔案。
   * 在資料表選取器中，從目前專案或您有權存取的其他專案，選擇一或多個 BigQuery 資料表。
   * 在提示中參照 BigQuery 資料表名稱，格式如下：`project_id:dataset.table`。
   * 輸入 `@` 符號，使用 `@mention` 函式搜尋 BigQuery 資料表名稱。
3. 輸入提示，說明要執行的資料分析或要建構的原型。Data Science Agent 的預設行為是使用 sklearn 等開放原始碼程式庫生成 Python 程式碼，以完成複雜的機器學習工作。如要使用特定工具，請在提示中加入下列關鍵字：

   * 如要使用 BigQuery ML，請加入「SQL」關鍵字。
   * 如要使用「BigQuery DataFrames」，請指定「BigFrames」或「BigQuery DataFrames」關鍵字。
   * 如要使用 PySpark，請加入「Apache Spark」或「PySpark」關鍵字。

   如需協助，請參閱[提示範例](#sample-prompts)。
4. 查看結果。

### 分析 CSV 檔案

如要在 BigQuery 中使用資料科學代理程式分析 CSV 檔案，請按照下列步驟操作。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 BigQuery Studio 歡迎頁面中，按一下「建立新項目」下方的「筆記本」。

   或者，在分頁列中，按一下 **+** 圖示旁的下拉式箭頭，然後依序點選「筆記本」**> 空白筆記本**。arrow\_drop\_down
3. 按一下「Toggle Gemini in Colab」按鈕，開啟即時通訊對話方塊。

   **注意：** 按一下「移至面板」圖示，即可將即時通訊對話方塊移至筆記本外的獨立面板。
4. 上傳 CSV 檔案。

   1. 在即時通訊對話方塊中，依序點選「新增至 Gemini」**> 上傳**。add\_circle\_outline
   2. 視需要授權 Google 帳戶。
   3. 瀏覽至 CSV 檔案所在位置，然後按一下「開啟」。
5. 或者，在提示中輸入 `+` 符號，搜尋可上傳的檔案。
6. 在對話視窗中輸入提示詞。例如：`Identify trends and
   anomalies in this file.`
7. 按一下「傳送」send。結果會顯示在聊天視窗中。
8. 你可以要求服務專員變更計畫，也可以按一下「接受並執行」來運作執行。計畫執行時，筆記本中會顯示生成的程式碼和文字。按一下「取消」即可停止。

### 分析 BigQuery 資料表

如要分析 BigQuery 資料表，請在資料表選取器中選擇一或多個資料表，在提示中提供資料表參照，或使用 `@` 符號搜尋資料表。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 BigQuery Studio 歡迎頁面中，按一下「建立新項目」下方的「筆記本」。

   或者，在分頁列中，按一下 **+** 圖示旁的下拉式箭頭，然後依序點選「筆記本」**> 空白筆記本**。arrow\_drop\_down
3. 按一下「Toggle Gemini in Colab」按鈕，開啟即時通訊對話方塊。

   **注意：** 按一下「移至面板」圖示，即可將即時通訊對話方塊移至筆記本外的獨立面板。
4. 在對話視窗中輸入提示。
5. 請透過下列任一方式參照資料：

   1. 使用表格選取器選擇一或多個表格：

      1. 依序點選 add\_circle\_outline「新增至 Gemini」**> BigQuery 資料表**。
      2. 在「BigQuery tables」(BigQuery 資料表) 視窗中，選取專案中的一或多個資料表。您可以在專案中搜尋表格，並使用搜尋列篩選表格。
   2. 直接在提示中加入 BigQuery 資料表名稱。
      例如：「請協助我對這個表格中的資料執行探索性資料分析，並取得相關洞察：`project_id:dataset.table`。」

      更改下列內容：

      * `project_id`：專案 ID
      * `dataset`：含有您要分析之資料表的資料集名稱
      * `table`：要分析的資料表名稱
   3. 輸入 `@`，在目前專案中搜尋 BigQuery 資料表。
6. 按一下 send「傳送」。

   結果會顯示在聊天視窗中。
7. 你可以要求服務專員變更計畫，也可以按一下「接受並執行」來運作執行。計畫執行時，筆記本中會顯示生成的程式碼和文字。如要執行方案中的其他步驟，您可能需要再次按一下「接受並執行」。按一下「取消」即可停止。

## 提示範例

無論提示詞有多複雜，資料科學代理都會生成計畫，您可以根據需求調整。

以下範例說明動態搜尋廣告可使用的提示類型。

### Python 提示

除非在提示中使用「BigQuery ML」或「SQL」等特定關鍵字，否則系統預設會生成 Python 程式碼。

* 使用 k-Nearest Neighbors (KNN) 機器學習演算法，調查並填補遺漏值。
* 根據經驗程度繪製薪資圖。使用 `experience_level` 欄分組薪資，並為每個群組建立盒鬚圖，顯示 `salary_in_usd` 欄中的值。
* 使用 XGBoost 演算法建立模型，判斷特定水果的 `class` 變數。將資料分成訓練和測試資料集，以生成模型並判斷模型的準確度。建立混淆矩陣，顯示每個類別的預測結果，包括所有正確和不正確的預測。
* 未來六個月的預測 `target_variable` (`filename.csv`)。

### SQL 和 BigQuery ML 提示

* 使用 BigQuery SQL 建立及評估分類模型。`bigquery-public-data.ml_datasets.census_adult_income`
* 使用 SQL，根據 `bigquery-public-data.google_analytics_sample.ga_sessions_*` 預測下個月的網站流量。
  接著，繪製歷史值和預測值。
* 使用 KMeans 模型和 BigQuery ML SQL 函式，將類似的顧客歸為一組，以便建立目標市場廣告活動。使用三項特徵進行分群。接著建立一系列 2D 散佈圖，以視覺化呈現結果。使用表格 `bigquery-public-data.ml_datasets.census_adult_income`。
* 使用 `bigquery-public-data.imdb.reviews` 中的評論內容，在 BigQuery ML 中生成文字嵌入。

如需支援的模型和機器學習工作清單，請參閱 [BigQuery ML 說明文件](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。

### DataFrame 提示

* 為 `project_id:dataset.table` 中的資料建立 pandas DataFrame。
  分析資料中的空值，然後使用圖表類型繪製每個資料欄的分布圖。使用小提琴圖表示測量值，並使用長條圖表示類別。
* 讀取 `filename.csv` 並建構 DataFrame。對 DataFrame 執行分析，判斷如何處理值。舉例來說，是否有需要替換或移除的遺漏值，
  或是需要處理的重複資料列。使用資料檔案，判斷每個城市地點的美元投資金額分布。使用長條圖繪製前 20 項結果，並以「地點」與「平均投資金額 (美元)」的降序顯示結果。
* 使用 BigQuery DataFrame 建立及評估分類模型。`project_id:dataset.table`
* 使用 BigQuery DataFrame 在 `project_id:dataset.table` 建立時間序列預測模型，並以視覺化方式呈現模型評估結果。
* 使用 BigQuery DataFrames，以圖表呈現 BigQuery 資料表 `project_id:dataset.table` 中過去一年的銷售數據。
* 使用 BigQuery DataFrames，從 `bigquery-public_data.ml_datasets.penguins` 資料表找出最能預測企鵝物種的特徵。

### PySpark 提示

* 使用 Managed Service for Apache Spark，在 `project_id:dataset.table` 上建立及評估分類模型。
* 將類似的顧客分組，建立指定目標市場廣告活動，但請先使用 PCA 模型進行降維。請使用 PySpark 在資料表 `project_id:dataset.table` 上執行這項操作。

## 關閉 Gemini in BigQuery

如要為 Google Cloud 專案停用 Gemini in BigQuery，管理員必須停用 Gemini for Google Cloud API。請參閱「[停用服務](https://docs.cloud.google.com/service-usage/docs/enable-disable?hl=zh-tw#disabling)」。

如要為特定使用者停用 Gemini in BigQuery，管理員必須撤銷該名使用者的「Gemini for Google Cloud 使用者」 (`roles/cloudaicompanion.user`) 角色。詳情請參閱[撤銷單一 IAM 角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#revoke-single-role)。

**注意：** 如要選擇不採用「資料科學代理」預先發布版，但繼續使用其他 Gemini 功能，請傳送電子郵件至 [vertex-notebooks-previews-external@google.com](mailto:vertex-notebooks-previews-external@google.com)。

## 定價

在預先發布期間，您需要為在筆記本執行階段中執行的程式碼，以及使用的任何 BigQuery [運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)付費。詳情請參閱 [Colab Enterprise 定價](https://cloud.google.com/colab/pricing?hl=zh-tw)。

## 支援的地區

如要查看 Colab Enterprise 資料科學代理支援的地區，請參閱「[位置](https://docs.cloud.google.com/colab/docs/locations?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]