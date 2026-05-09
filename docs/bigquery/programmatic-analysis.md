Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 程式輔助分析工具

本文說明多種寫入及執行程式碼的方式，可用來分析 BigQuery 中所代管的資料。

儘管 SQL 是一種功能強大的查詢語言，但是 Python、Java 或 R 等程式設計語言提供了語法和大量的內建統計功能，資料分析人員可能會認為這對於某些類型的資料分析而言更快速且更易於操作。

同樣地，儘管試算表已廣為使用，但其他程式設計環境 (如筆記本) 有時可提供更靈活的環境來進行複雜的資料分析和探索。

## Colab Enterprise 筆記本

您可以在 BigQuery 中使用 [Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)，透過 SQL、Python 和其他常見套件與 API，完成分析和機器學習 (ML) 工作流程。筆記本提供下列選項，可提升協作和管理效率：

* 使用 Identity and Access Management (IAM)，與特定使用者和群組共用筆記本。
* 查看筆記本版本記錄。
* 還原或從筆記本的先前版本建立分支。

筆記本是 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 程式碼資產，由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 提供支援，但筆記本不會顯示在 Dataform 中。[儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw)也是程式碼資產。
所有程式碼資產都會儲存在預設[區域](#supported_regions)。更新預設區域後，之後建立的所有程式碼資產都會使用新的區域。

記事本功能僅適用於 Google Cloud 控制台。

BigQuery 中的 Notebook 具有下列優點：

* [BigQuery DataFrames](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw) 已整合至筆記本，無須設定。BigQuery DataFrames 是 Python API，可讓您使用 [pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) 和 [scikit-learn](https://scikit-learn.org/stable/modules/classes.html) API，大規模分析 BigQuery 資料。
* 採用 [Gemini 生成式 AI](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw) 技術輔助開發程式碼。
* 自動完成 SQL 陳述式，與 BigQuery 編輯器相同。
* 可儲存、共用及管理筆記本版本。
* 您可以在工作流程的任何時間點，使用 [matplotlib](https://matplotlib.org/)、
  [seaborn](https://seaborn.pydata.org/) 和其他熱門程式庫將資料視覺化。
* 您可以在儲存格中編寫及[執行 SQL](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#cells)，並參照筆記本中的 Python 變數。
* 支援匯總和自訂功能的互動式 [DataFrame 視覺化](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#cells)。

你可以使用筆記本範本庫中的範本，開始使用筆記本。詳情請參閱「[使用筆記本庫建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#create-notebook-console)」。

## BigQuery DataFrames

[BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw) 是一組開放原始碼 Python 程式庫，可讓您使用熟悉的 Python API，充分運用 BigQuery 資料處理功能。BigQuery DataFrames 會透過 SQL 轉換，將處理作業下推至 BigQuery，藉此實作 pandas 和 scikit-learn API。這種設計可讓您使用 BigQuery 探索及處理 TB 級資料，並透過 Python API 訓練機器學習模型。

BigQuery DataFrames 的優點如下：

* 透過透明的 SQL 轉換至 BigQuery 和 BigQuery ML API，實作超過 750 個 pandas 和 scikit-learn API。
* 延後執行查詢，提升效能。
* 使用 Python 使用者定義函式擴充資料轉換作業，以便在雲端處理資料。這些函式會自動部署為 BigQuery [遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)。
* 與 Vertex AI 整合，讓您使用 Gemini 模型生成文字。

## 其他程式輔助分析解決方案

BigQuery 也提供下列程式輔助分析解決方案。

### Jupyter Notebook

[Jupyter](https://jupyter.org/) 是一種開放原始碼的網頁型應用程式，用來發布包含即時程式碼、文字說明和視覺化內容的筆記本。數據資料學家、機器學習專家和學生通常會使用這個平台，執行資料清理與轉換、數值模擬、統計建模、資料視覺化和機器學習等工作。

Jupyter Notebooks 以 [IPython](https://ipython.org/) 核心 (一種功能強大的互動式殼層) 為基礎，可透過 [BigQuery 的 IPython Magics](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/magics?hl=zh-tw) 直接與 BigQuery 互動。或者，您也可以安裝任何可用的 [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)，從 Jupyter Notebooks 執行個體存取 BigQuery。
您可以透過 [GeoJSON 擴充功能](https://github.com/jupyterlab/jupyter-renderers/tree/master/packages/geojson-extension)，使用 Jupyter 筆記本將 [BigQuery GIS](https://docs.cloud.google.com/bigquery/docs/gis-intro?hl=zh-tw) 的資料視覺化。如要進一步瞭解 BigQuery 整合，請參閱[在 Jupyter 筆記本中以視覺化方式呈現 BigQuery 資料](https://docs.cloud.google.com/bigquery/docs/visualize-jupyter?hl=zh-tw)一文的教學課程。

[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) 是網頁式使用者介面，可用於管理文件和活動，例如 Jupyter 筆記本、文字編輯器、終端機和自訂元件。使用 JupyterLab，您可以利用分頁標籤和分割工具，在工作區中同時排列多項文件和活動。

您可以使用下列其中一項產品，在Google Cloud 上部署 Jupyter 筆記本和 JupyterLab 環境：

* [Vertex AI Workbench 執行個體](https://docs.cloud.google.com/vertex-ai/docs/workbench/instances/introduction?hl=zh-tw)：提供整合 JupyterLab 環境的服務，可讓機器學習開發人員和資料科學家使用部分最新的資料科學和機器學習架構。Vertex AI Workbench 已與 BigQuery 等其他 Google Cloud 資料產品整合，使用者可以輕鬆執行多項工作，包括資料擷取、預先處理和探索資料，以及最終的模型訓練和部署作業等。詳情請參閱 [Vertex AI Workbench 執行個體簡介](https://docs.cloud.google.com/vertex-ai/docs/workbench/instances/introduction?hl=zh-tw)。
* [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc?hl=zh-tw) 是一項運作快速又簡單易用的全代管服務，可讓您以更輕鬆且更具成本效益的方式執行 [Apache Spark](https://spark.apache.org/) 和 [Apache Hadoop](https://hadoop.apache.org/) 叢集。您可以使用 [Jupyter 選用元件](https://docs.cloud.google.com/dataproc/docs/concepts/components/jupyter?hl=zh-tw)，在 Managed Service for Apache Spark 叢集上安裝 Jupyter 筆記本和 JupyterLab。
  元件提供 Python 核心，用來執行 [PySpark](https://pypi.org/project/pyspark/) 程式碼。根據預設，Managed Service for Apache Spark 會自動設定將筆記本[儲存在 Cloud Storage 中](https://github.com/src-d/jgscm)，讓其他叢集可以存取相同的筆記本檔案。將現有筆記本遷移至 Managed Service for Apache Spark 時，請檢查系統支援的 [Managed Service for Apache Spark 版本](https://docs.cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions?hl=zh-tw)是否包含筆記本的依附元件。如要安裝自訂軟體，您可以考慮[自行建立 Managed Service for Apache Spark 映像檔](https://docs.cloud.google.com/dataproc/docs/guides/dataproc-images?hl=zh-tw)、編寫自己的[初始化動作](https://docs.cloud.google.com/dataproc/docs/concepts/configuring-clusters/init-actions?hl=zh-tw)或[指定自訂 Python 套件需求](https://docs.cloud.google.com/dataproc/docs/tutorials/python-configuration?hl=zh-tw)。如要開始使用，請參閱[在 Managed Service for Apache Spark 叢集上安裝及執行 Jupyter 筆記本](https://docs.cloud.google.com/dataproc/docs/tutorials/jupyter-notebook?hl=zh-tw)的教學課程。

### Apache Zeppelin

[Apache Zeppelin](https://zeppelin.apache.org/)是一種開放原始碼的專案，提供網頁型的筆記本進行數據分析。您可以藉由安裝 [Zeppelin 選用元件](https://docs.cloud.google.com/dataproc/docs/concepts/components/zeppelin?hl=zh-tw)，在 [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc?hl=zh-tw) 上部署 Apache Zeppelin 執行個體。根據預設，筆記本會儲存在 Cloud Storage 中，即在叢集建立期間由使用者指定或系統自動建立的 Apache Spark 受管理服務暫存值區。建立叢集時，您可以新增 `zeppelin:zeppelin.notebook.gcs.dir` 屬性來變更筆記本位置。如要進一步瞭解如何安裝及設定 Apache Zeppelin，請參閱 [Zeppelin 元件指南](https://docs.cloud.google.com/dataproc/docs/concepts/components/zeppelin?hl=zh-tw)。如需範例，請參閱[使用適用於 Apache Zeppelin 的 BigQuery Interpreter 分析 BigQuery 資料集](https://cloud.google.com/blog/products/gcp/analyzing-bigquery-datasets-using-bigquery-interpreter-for-apache-zeppelin?hl=zh-tw)。

### Apache Hadoop、Apache Spark 和 Apache Hive

在遷移資料分析管道時，您可能需要遷移部分舊版的 [Apache Hadoop](https://hadoop.apache.org/)、[Apache Spark](https://spark.apache.org/) 或 [Apache Hive](https://hive.apache.org/) 工作，這些工作需要直接處理資料倉儲中的資料。例如，您可以擷取用於機器學習工作負載的功能。

有了 Apache Spark 代管服務，您就能以符合成本效益的方式，有效部署全代管 Hadoop 和 Spark 叢集。Managed Service for Apache Spark 整合了開放原始碼 [BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/bigquery?hl=zh-tw)。這些連接器使用 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)，直接從 BigQuery 透過 gRPC 串流資料。

將現有的 Hadoop 和 Spark 工作負載遷移至 Managed Service for Apache Spark 時，您可以確認系統支援的 [Managed Service for Apache Spark 版本](https://docs.cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions?hl=zh-tw)中是否包含工作負載依附元件。如要安裝自訂軟體，您可以考慮[自行建立 Managed Service for Apache Spark 映像檔](https://docs.cloud.google.com/dataproc/docs/guides/dataproc-images?hl=zh-tw)、寫入自己的[初始化動作](https://docs.cloud.google.com/dataproc/docs/concepts/configuring-clusters/init-actions?hl=zh-tw)或[指定自訂 Python 套件需求](https://docs.cloud.google.com/dataproc/docs/tutorials/python-configuration?hl=zh-tw)。

如要開始使用，請參閱「[Managed Service for Apache Spark 快速入門導覽課程指南](https://docs.cloud.google.com/dataproc/docs/quickstarts?hl=zh-tw)」和「[BigQuery 連接器程式碼範例](https://docs.cloud.google.com/dataproc/docs/examples/bigquery-example?hl=zh-tw)」。

### Apache Beam

[Apache Beam](https://beam.apache.org/) 是一個開放原始碼架構，提供豐富的時間區間設定和工作階段分析基元，以及各式來源與接收器連接器的生態系統，包括 [BigQuery 適用的連接器](https://beam.apache.org/documentation/io/built-in/google-bigquery/)。Apache Beam 可讓您在串流 (即時) 與批次 (舊有) 模式下轉換並擴充資料，而且可靠性和明確性完全相同。

[Dataflow](https://docs.cloud.google.com/dataflow?hl=zh-tw) 是一項全代管服務，可大規模執行 Apache Beam 工作。Dataflow 的無伺服器方法能夠自動處理效能、資源調度、可用性、安全性和法規遵循相關作業，因此可以減輕您的營運工作負擔，讓您能專心設計程式，無須費心管理伺服器叢集。

您可以利用不同的方式提交 Dataflow 工作，例如透過[指令列介面](https://docs.cloud.google.com/dataflow/docs/guides/using-command-line-intf?hl=zh-tw)、[Java SDK](https://beam.apache.org/documentation/sdks/java/) 或 [Python SDK](https://beam.apache.org/documentation/sdks/python/)。

如要將資料查詢和資料管道從其他架構遷移至 Apache Beam 和 Dataflow，請參閱 [Apache Beam 的程式設計模型](https://docs.cloud.google.com/dataflow/docs/concepts/beam-programming-model?hl=zh-tw)一文，並瀏覽官方的 [Dataflow 說明文件](https://docs.cloud.google.com/dataflow/docs?hl=zh-tw)。

### 其他資源

BigQuery 提供大量的[用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)，支援多種程式設計語言，例如 Java、Go、Python、JavaScript、PHP 和 Ruby。部分資料分析架構 (例如 [pandas](https://pandas.pydata.org/)) 提供可直接與 BigQuery 互動的[外掛程式](https://pandas-gbq.readthedocs.io/en/latest/)。如需實際範例，請參閱[在 Jupyter 筆記本中以視覺化方式呈現 BigQuery 資料](https://docs.cloud.google.com/bigquery/docs/visualize-jupyter?hl=zh-tw)教學課程。

最後，如果您偏好在殼層環境中編寫程式，可以使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]