Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Notebook 和程式輔助分析工具

雖然 SQL 是強大的查詢語言，但 Python、Java 或 R 等程式設計語言提供的語法和統計函式，在資料分析工作中可能更具表現力。Notebook 環境提供高度彈性的替代方案，可取代試算表，用於複雜的資料探索和機器學習 (ML) 工作流程。

BigQuery 提供內建的筆記本整合功能，並支援其他多種程式輔助分析解決方案。

## Colab Enterprise 筆記本

您可以在 BigQuery 中使用 Colab Enterprise 筆記本，在單一整合式介面中執行端對端資料科學和機器學習工作流程。與標準 SQL 編輯器不同，筆記本可讓您結合 SQL 查詢與 Python 程式碼、RTF 格式和圖表，完整呈現資料。Colab Enterprise 筆記本適合下列用途：

* **端對端機器學習工作流程：**在單一介面中建構、評估及部署 BigQuery ML 模型。
* **資料探索：**使用 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw) 清理及分析大型資料集。
* **協作研究：**追蹤版本記錄，並透過 Identity and Access Management (IAM) 與同事共用筆記本。

Colab Enterprise 筆記本具有下列優點：

* **AI 輔助開發：**運用 Gemini Enterprise Agent Platform 輔助程式碼開發。
* **完美整合 Python：**不需額外設定，即可使用 BigQuery DataFrames API。
* **熟悉的編輯器功能：**享有與 BigQuery SQL 編輯器類似的 SQL 自動完成功能。
* **整合式視覺化：**直接在工作流程中使用互動式 DataFrame 視覺化或 `matplotlib` 和 `seaborn` 等程式庫。
* **SQL-Python 互通性：**在參照 Python 變數的儲存格中執行 SQL。

### 資料科學代理

[Colab Enterprise 資料科學代理 (DSA)](https://docs.cloud.google.com/bigquery/docs/colab-data-science-agent?hl=zh-tw) 可在 Colab Enterprise 筆記本中，自動執行探索性資料分析、機器學習工作，以及提供洞察資訊。DSA 的用途包括：

* **機器學習工作流程：**設計新特徵、將資料分割為訓練、驗證和測試資料集，並處理模型訓練、最佳化、評估和推論的完整生命週期。
* **大規模資料處理：**使用 BigQuery ML、BigQuery DataFrames 或 Managed Service for Apache Spark，對大型資料集執行分散式資料處理。
* **生成計畫：**使用 Python、SQL、Managed Service for Apache Spark 和 BigQuery DataFrames 等常見工具，生成及修改計畫，完成特定工作。
* **資料探索、清理和整頓：**探索資料集，瞭解其結構、找出潛在問題 (例如缺少值和離群值)，並檢查重要變數的分佈情形。您也可以使用 one-hot 編碼等技術，將類別特徵轉換為數值表示法。
* **資料分析和視覺化：**分析不同變數之間的關係、計算關聯性，以及建立直方圖、箱形圖、散布圖和長條圖等圖表。

### 瞭解儲存格

筆記本是由可編輯的儲存格組成。Colab Enterprise 筆記本支援下列類型的儲存格：

* **文字儲存格**：使用文字儲存格，以 Markdown 格式在筆記本中加入說明和圖片。
* **程式碼儲存格**：使用程式碼儲存格，在筆記本中加入 Python。您可以個別執行每個程式碼儲存格。程式碼儲存格可以參照在其他已執行儲存格中建立的任何變數。
* **SQL 儲存格**：使用 [SQL 儲存格](https://docs.cloud.google.com/colab/docs/sql-cells?hl=zh-tw)執行 GoogleSQL 查詢。查詢輸出內容會自動儲存為 DataFrame，名稱與儲存格標題相同。您可以在單一 SQL 儲存格中執行多個 SQL 陳述式，但只有最後一個陳述式的結果會儲存至 DataFrame。

  您可以在運算式中參照 Python 變數，或將 BigQuery DataFrames 做為查詢中的資料表，只要將變數名稱括在大括號 (`{ }`) 中即可：

  ```
  # Refer to the Python variable my_threshold in a SQL expression.
  SELECT * FROM my_dataset.my_table WHERE x > {my_threshold};

  # Reference previous query results to iterate on your queries.
  SELECT * FROM {df};
  ```
* **圖表儲存格**：使用[圖表儲存格](https://docs.cloud.google.com/colab/docs/visualization-cells?hl=zh-tw)，自動生成筆記本中任何 DataFrame 的圖表。您可以修改要顯示的資料欄，並從各種圖表類型和匯總方式中選取。您也可以選擇自訂顏色、資料標籤和標題。

### 筆記本庫

筆記本庫是探索及使用預先建構筆記本範本的中心。其中包含 SQL、Python、Apache Spark 和 DataFrames 的基本範本，可協助您執行資料準備、分析和視覺化等常見工作。

### 執行階段管理和安全性

Notebooks 使用 Colab Enterprise 執行階段，這是分配給特定使用者的 Compute Engine 虛擬機器，可執行程式碼。筆記本存取權則由 IAM 角色控管。如要偵測筆記本所用 Python 套件中的安全漏洞，可以安裝並使用 [Notebook Security Scanner](https://docs.cloud.google.com/security-command-center/docs/enable-notebook-security-scanner?hl=zh-tw)。

### 監控和區域

BigQuery Studio 中的所有程式碼資產都會儲存在預設區域，更新這項設定會變更新建立程式碼資產的區域。凡是提供 BigQuery Studio 的區域，皆可使用 Colab Enterprise 筆記本。

如要監控 Notebook 的運算單元用量，可以查看 Cloud Billing 帳單報表，並篩選 `goog-bq-feature-type` 標籤，值為 `BQ_STUDIO_NOTEBOOK`。

Notebook 功能僅適用於 Google Cloud 控制台。

### 定價

如要瞭解 Colab Enterprise 筆記本的定價資訊，請參閱「[筆記本執行階段定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#external_services)」。

## BigQuery DataFrames

[BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw) 是一組開放原始碼 Python 程式庫，可讓您使用熟悉的 Python API，充分運用 BigQuery 資料處理功能。BigQuery DataFrames 透過 SQL 轉換將處理作業推送至 BigQuery，藉此實作 pandas 和 scikit-learn API。這項設計可讓您使用 BigQuery 探索及處理數 TB 的資料，並訓練機器學習模型，全部都透過 Python API 完成。

BigQuery DataFrames 具有下列優點：

* 超過 750 個 pandas 和 scikit-learn API，透過透明的 SQL 轉換，實作至 BigQuery 和 BigQuery ML API。
* 延遲執行查詢，提升效能。
* 使用使用者定義的 Python 函式擴充資料轉換功能，以便在雲端處理資料。這些函式會自動部署為 BigQuery [遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)。
* 與 Gemini Enterprise Agent Platform 整合，讓您使用 Gemini 模型生成文字。

## 其他程式輔助分析解決方案

除了 Colab Enterprise 和 BigQuery DataFrames 之外，BigQuery 還與其他幾項程式輔助解決方案整合：

* **Jupyter Notebooks 和 JupyterLab：**您可以使用 [BigQuery 的 IPython Magics](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/magics?hl=zh-tw) 或 [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)，直接從 Jupyter Notebooks 與 BigQuery 互動。您可以使用 [Vertex AI Workbench 執行個體](https://docs.cloud.google.com/gemini-enterprise-agent-platform/notebooks/workbench/introduction?hl=zh-tw)或 [Managed Service for Apache Spark](https://cloud.google.com/products/managed-service-for-apache-spark?hl=zh-tw)，在 Google Cloud 上部署環境。
* **Apache Zeppelin：**在 Managed Service for Apache Spark 上安裝 [Zeppelin 選用元件](https://docs.cloud.google.com/dataproc/docs/concepts/components/zeppelin?hl=zh-tw)，即可部署網頁式 Apache Zeppelin 筆記本，用於資料分析。
* **Apache Hadoop、Spark 和 Hive：**
  [Managed Service for Apache Spark](https://cloud.google.com/products/managed-service-for-apache-spark?hl=zh-tw) 與開放原始碼 BigQuery 連接器整合。這些連接器會使用 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)，透過 gRPC 直接從 BigQuery 平行串流資料。
* **Apache Beam 和 Dataflow：**Apache Beam 是開放原始碼架構，提供多項時間區間設定和工作階段分析基元，以及連接器生態系統，包括 BigQuery 連接器。[Dataflow](https://docs.cloud.google.com/dataflow/docs/overview?hl=zh-tw) 是全代管服務，可讓您大規模執行這些 Apache Beam 工作。

### 其他資源

BigQuery 提供多種語言的[用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)，例如 Java、Go、Python、JavaScript、PHP 和 Ruby。某些資料分析架構 (例如 [pandas](https://pandas.pydata.org/)) 提供[外掛程式](https://pandas-gbq.readthedocs.io/en/latest/)，可直接與 BigQuery 互動。如果您偏好殼層環境，則可使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-20 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-20 (世界標準時間)。"],[],[]]