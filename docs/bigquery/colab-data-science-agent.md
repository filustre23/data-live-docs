Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 搭配 BigQuery 使用 Colab Enterprise 資料科學代理

Colab Enterprise 和 BigQuery 的資料科學代理 (DSA) 可在 Colab Enterprise 筆記本中，自動執行探索性資料分析、機器學習工作，以及提供洞察資訊。

## 事前準備

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
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

1. 啟用 BigQuery、Gemini for Google Cloud、Dataform 和 Compute Engine API (如有尚未啟用的 API)。

   **啟用 API 所需的角色**

   您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「Service Usage 管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Ccloudaicompanion.googleapis.com%2Cdataform.googleapis.com%2Ccompute.googleapis.com&hl=zh-tw)

   如果是新專案，系統會自動啟用 BigQuery API。

如果您是第一次在 BigQuery 使用 Colab Enterprise，請參閱「[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#required_permissions)」頁面的設定步驟。

## 限制

* DSA 僅適用於 Colab Enterprise 環境。
* DSA 支援下列資料來源：
  + CSV 檔案
  + BigQuery 資料表
* DSA 產生的程式碼只會在筆記本的執行階段中執行。
* 使用 `@mention` 函式搜尋 BigQuery 資料表時，僅限於目前專案。使用資料表選取器，跨專案搜尋。
* `@mention` 函式只會搜尋 BigQuery 資料表。如要搜尋可上傳的資料檔案，請使用 `+` 符號。
* DSA 中的 PySpark 只會生成 Managed Service for Apache Spark 4.0 程式碼。DSA 可協助您升級至 Managed Service for Apache Spark 4.0。如需舊版，請改為[直接在筆記本中編寫及執行 PySpark 程式碼](https://docs.cloud.google.com/bigquery/docs/use-spark?hl=zh-tw)。
* 不支援[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/kms/docs/cmek?hl=zh-tw)。

## 在 BigQuery 使用資料科學代理

下列步驟說明如何在 BigQuery 中使用 DSA。

1. 建立或開啟 Colab Enterprise 筆記本。
2. 選用：透過下列任一方式參照資料：

   * 上傳 CSV 檔案，或在提示中使用 `+` 符號搜尋可用檔案。
   * 在資料表選取器中，從目前專案或您有權存取的其他專案，選擇一或多個 BigQuery 資料表。
   * 在提示中參照 BigQuery 資料表名稱，格式如下：`project_id:dataset.table`。
   * 輸入 `@` 符號，使用 `@mention` 函式搜尋 BigQuery 資料表名稱。
3. 輸入[提示詞](#sample-prompts)，說明要執行的資料分析或要建構的原型。預設行為是使用 sklearn 等開放原始碼程式庫生成 Python 程式碼，以完成複雜的機器學習工作。如要使用特定工具，請在提示中加入下列關鍵字：

   * 如要使用 BigQuery ML，請加入「SQL」關鍵字。
   * 如要使用「BigQuery DataFrames」，請指定「BigFrames」或「BigQuery DataFrames」關鍵字。
   * 如要使用 PySpark，請加入「Apache Spark」或「PySpark」關鍵字。
4. 選擇模型。預設模型為 Gemini 3.0 Flash。
5. 傳送提示並查看結果。

### 分析 CSV 檔案

如要在 BigQuery 中使用 DSA 分析 CSV，請按照下列步驟操作。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中展開專案，然後按一下「Notebooks」。
3. 依序點選**「新增筆記本」 > 「空白筆記本」**。

   或者，在分頁列中，按一下 arrow\_drop\_down「Add」圖示旁的 arrow\_drop\_down 下拉式箭頭，然後依序點選「Notebook」>「Empty notebook」。
4. 按一下「spark」「Toggle Gemini in Colab」(在 Colab 中切換 Gemini) 按鈕，開啟對話方塊。

   **注意：** 點選 collapse\_content「Move」(移動) 圖示，即可切換對話方塊的顯示方式，選擇在獨立面板或筆記本中顯示。
5. 上傳 CSV 檔案。

   1. 在對話方塊中，依序點選「新增至 Gemini」圖示 add\_circle\_outline**「上傳」**。
   2. 視需要授權 Google 帳戶。
   3. 找到 CSV 檔案的位置，然後按一下「開啟」。
6. 或者，在提示中輸入 `+` 符號，搜尋可上傳的檔案。
7. 在對話視窗中輸入提示詞。例如：`Identify trends and
   anomalies in this file.`
8. 選擇模型。預設模型為 Gemini 3.0 Flash。
9. 按一下「傳送」send。結果會顯示在對話視窗中。
10. 您可以要求代理變更計畫，也可以點選「Accept & run」(接受並執行) 執行計畫。執行計畫時，生成的程式碼和文字會顯示在筆記本中。按一下「取消」即可停止。

### 分析 BigQuery 資料表

如要分析 BigQuery 資料表，請在資料表選取器中選擇一或多個資料表、在提示中提供資料表參照，或使用 `@` 符號搜尋資料表。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中展開專案，然後按一下「Notebooks」。
3. 依序點選**「新增筆記本」 > 「空白筆記本」**。

   或者，在分頁列中，按一下 arrow\_drop\_down「Add」圖示旁的 arrow\_drop\_down 下拉式箭頭，然後依序點選「Notebook」>「Empty notebook」。
4. 按一下「spark」「Toggle Gemini in Colab」(在 Colab 中切換 Gemini) 按鈕，開啟對話方塊。

   **注意：** 點選 collapse\_content「Move」(移動) 圖示，即可切換對話方塊的顯示方式，選擇在獨立面板或筆記本中顯示。
5. 在對話視窗中輸入提示詞。
6. 請透過下列其中一種方式參照資料：

   1. 使用表格選取器選擇一或多個表格：

      1. 按一下 add\_circle\_outline
         **新增至 Gemini > BigQuery 資料表**。
      2. 在「BigQuery tables」(BigQuery 資料表) 視窗中，選取專案中的一或多個資料表。您可以使用搜尋列，跨專案搜尋資料表，並篩選資料表。
   2. 直接在提示中加入 BigQuery 資料表名稱。例如：「幫我執行探索性資料分析，並取得這個資料表中資料的深入分析：`project_id:dataset.table`。」

      更改下列內容：

      * `project_id`：專案 ID
      * `dataset`：資料集名稱，其中包含您要分析的資料表
      * `table`：要分析的資料表名稱
   3. 輸入 `@`，在目前專案中搜尋 BigQuery 資料表。
7. 選擇模型。預設模型為 Gemini 3.0 Flash。
8. 按一下「傳送」send。

   結果會顯示在對話視窗中。
9. 您可以要求代理變更計畫，也可以點選「Accept & run」(接受並執行) 執行計畫。執行計畫時，生成的程式碼和文字會顯示在筆記本中。如要執行計畫中的其他步驟，您可能需要再次按一下「Accept & run」(接受並執行)。按一下「取消」即可停止。

## 提示範例

無論提示有多複雜，DSA 都會生成計畫，您可以根據需求調整。

以下範例說明可與 DSA 搭配使用的提示類型。

### Python 提示

除非您在提示中使用特定關鍵字 (例如「BigQuery ML」或「SQL」)，否則系統預設會生成 Python 程式碼。

* 「使用 K 近鄰 (KNN) 機器學習演算法，調查並填補遺漏值。」
* 「依經驗等級繪製薪資圖表。使用 `experience_level` 欄將薪資分組，並為每個群組建立盒鬚圖，顯示 `salary_in_usd` 欄的值。」
* 「使用 XGBoost 演算法建立模型，判斷特定水果的 `class` 變數。將資料分割為訓練和測試資料集，以便產生模型並判斷模型準確度。建立混淆矩陣，顯示每個類別的預測結果，包括所有正確和不正確的預測結果。
* 「預測 `filename.csv` 的 `target_variable` 在未來六個月的表現。」

### SQL 和 BigQuery ML 提示

* 「使用 BigQuery SQL，在 `bigquery-public-data.ml_datasets.census_adult_income` 上建立及評估分類模型。」
* 「使用 SQL，根據 `bigquery-public-data.google_analytics_sample.ga_sessions_*` 預測我網站下個月的流量，然後繪製過往記錄和預測值。」
* 「使用 KMeans 模型和 BigQuery ML SQL 函式，將相似的客戶分組，建立指定目標的行銷廣告活動。使用三個特徵進行分群。接著，建立一系列 2D 散布圖，以圖表呈現結果。使用表格
  `bigquery-public-data.ml_datasets.census_adult_income`。」
* 「使用 `bigquery-public-data.imdb.reviews` 中的評論內容，在 BigQuery ML 生成文字嵌入。」

如需支援的模型和機器學習工作清單，請參閱 [BigQuery ML 說明文件](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。

### DataFrame 提示

* 「針對 `project_id:dataset.table` 中的資料，建立 pandas DataFrame。分析資料中的空值，然後使用圖表類型繪製每個資料欄的分布情形。測量值用小提琴圖呈現，類別則用長條圖。」
* 「讀取 `filename.csv` 並建構 DataFrame。對 DataFrame 執行分析，判斷如何處理值。例如，是否有需要替換或移除的遺漏值，或需要處理的重複資料列。請使用資料檔案，判斷每個城市位置投資金額 (美元) 的分布情形。Graph the top 20 results using a bar graph that shows the results
  in descending order as Location versus Avg Amount Invested (USD)."
* 「使用 BigQuery DataFrames，在 `project_id:dataset.table` 建立及評估分類模型。」
* 「使用 BigQuery DataFrames 建立 `project_id:dataset.table` 的時間序列預測模型，並以圖表呈現模型評估結果。」
* 「使用 BigQuery DataFrames，以圖表呈現 BigQuery 資料表 `project_id:dataset.table` 過去一年的銷售數據。」
* 「使用 BigQuery DataFrames，找出最能預測資料表 `bigquery-public_data.ml_datasets.penguins` 中企鵝物種的特徵。」

### PySpark 提示

* 「使用 Managed Service for Apache Spark，在 `project_id:dataset.table` 建立及評估分類模型。」
* 「將類似的客戶分組，建立指定行銷廣告活動，但首先要使用 PCA 模型進行降維。請使用 PySpark 對資料表 `project_id:dataset.table` 執行這項操作。」

## 關閉 Gemini in BigQuery

如要為 Google Cloud 專案停用 Gemini in BigQuery，管理員必須停用 Gemini for Google Cloud API。詳情請參閱[停用服務](https://docs.cloud.google.com/service-usage/docs/enable-disable?hl=zh-tw#disabling)的相關說明。

如要為特定使用者停用 Gemini in BigQuery，管理員必須撤銷該名使用者的「Gemini for Google Cloud 使用者」 (`roles/cloudaicompanion.user`) 角色。請參閱「[撤銷單一 IAM 角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#revoke-single-role)」一節。

**附註：** 如要選擇不採用資料科學代理，但保留其他 Gemini 功能，請傳送電子郵件至 [vertex-notebooks-previews-external@google.com](mailto:vertex-notebooks-previews-external@google.com)，或填寫[資料科學代理選擇不採用表單](https://forms.gle/KuTAunuLT2YmFAcs8)。如要進一步瞭解如何停用資料科學代理，請參閱「[停用 Gemini in Colab Enterprise](https://docs.cloud.google.com/colab/docs/use-data-science-agent?hl=zh-tw#turn-off)」。

## 定價

資料科學代理的定價取決於輸入和輸出資料。詳情請參閱「[BigQuery 定價模式](https://cloud.google.com/bigquery?hl=zh-tw#pricing)」中的代理程式定價。

## 支援的地區

如要查看 Colab Enterprise 資料科學代理支援的地區，請參閱「[位置](https://docs.cloud.google.com/colab/docs/locations?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]