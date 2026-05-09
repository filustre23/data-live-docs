Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Apache Spark 預存程序

本文適用於資料工程師、資料科學家和資料分析師，說明如何在 BigQuery 中建立及呼叫 Spark 的預存程序。

您可以使用 BigQuery 建立及執行以 Python、Java 和 Scala 編寫的 [Spark](https://spark.apache.org/) 儲存程序。接著，您可以使用 GoogleSQL 查詢，在 BigQuery 中執行這些預存程序，原理類似執行 [SQL 預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)。

## 事前準備

如要為 Spark 建立預存程序，請要求管理員建立 [Spark 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw)並與您共用。管理員也必須授予與連線相關聯的服務帳戶[必要的 Identity and Access Management (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw#grant-access)。

### 必要的角色

如要取得執行本文中工作所需的權限，請要求管理員授予下列 IAM 角色：

* [建立 Spark 預存程序](#create-spark-procedure)：
  + [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
    在您建立預存程序的資料集上
  + [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)
    在預存程序使用的連線上
  + 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* [呼叫 Spark 預存程序](#call-spark-procedure)：
  + 儲存預存程序的資料集具有 [BigQuery 中繼資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.metadataViewer)  (`roles/bigquery.metadataViewer`) 權限
  + 連線的「BigQuery Connection User」 (`roles/bigquery.connectionUser`)
  + 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行本文中工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行本文中的工作，必須具備下列權限：

* 建立連線：
  + `bigquery.connections.create`
  + `bigquery.connections.list`
* 建立 Spark 預存程序：
  + `bigquery.routines.create`
  + `bigquery.connections.delegate`
  + `bigquery.jobs.create`
* 呼叫 Spark 的預存程序：
  + `bigquery.routines.get`
  + `bigquery.connections.use`
  + `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 位置注意事項

您必須在與[連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw)相同的位置[為 Spark 建立預存程序](#create-spark-procedure)，因為預存程序會在與連線相同的位置執行。舉例來說，如要在美國多區域建立預存程序，請使用位於美國多區域的連線。

### 定價

* 在 BigQuery 上執行 Spark 程序時，收費方式與在 Managed Service for Apache Spark 上執行 Spark 程序時類似。詳情請參閱「[Managed Service for Apache Spark 定價](https://cloud.google.com/dataproc-serverless/pricing?hl=zh-tw)」。
* Spark 預存程序可搭配[隨選計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)使用，也能搭配任何 [BigQuery 版本](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)使用。無論專案使用的[運算定價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#overview_of_pricing)為何，系統一律會按照 [BigQuery Enterprise 版的即付即用模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#enterprise_edition)，收取 Spark 程序費用。
* BigQuery 的 Spark 預存程序不支援使用預留項目或承諾。現有的預訂和承諾仍會用於其他支援的查詢和程序。使用 Spark 預存程序的費用會以 Enterprise 版的即付即用費用計費，並加進帳單。系統會套用貴機構的折扣 (如適用)。
* 雖然 Spark 預存程序會使用 Spark 執行引擎，但您不會看到 Spark 執行的個別費用。如前所述，相應費用會以 [BigQuery Enterprise 版即付即用 SKU](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing) 形式列出。
* Spark 預存程序不提供免費方案。

## 建立 Spark 預存程序

您必須在與所用連線相同的位置建立預存程序。

如果預存程序的本文超過 1 MB，建議您將預存程序放在 Cloud Storage bucket 的檔案中，而不是使用內嵌程式碼。BigQuery 提供兩種方法，可使用 Python 為 Spark 建立預存程序：

* 如要使用 `CREATE PROCEDURE` 陳述式，請[使用 SQL 查詢編輯器](#use-sql-query-editor)。
* 如要直接輸入 Python 程式碼，請[使用 PySpark 編輯器](#use-python-pyspark-editor)。
  您可以[將程式碼儲存為預存程序](#save-stored-procedure)。

### 使用 SQL 查詢編輯器

如要在 SQL 查詢編輯器中建立 Spark 預存程序，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，新增顯示的 [`CREATE PROCEDURE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_procedure)程式碼範例。

   或者，在「Explorer」窗格中，按一下您用來建立連線資源的專案中的連線。接著，如要建立 Spark 的預存程序，請按一下「建立預存程序」search。

   **Python**

   如要在 Python 中建立 Spark 的預存程序，請使用下列程式碼範例：

   ```
   CREATE OR REPLACE PROCEDURE `PROJECT_ID`.DATASET.PROCEDURE_NAME(PROCEDURE_ARGUMENT)
    WITH CONNECTION `CONNECTION_PROJECT_ID.CONNECTION_REGION.CONNECTION_ID`
    OPTIONS (
        engine="SPARK", runtime_version="RUNTIME_VERSION",
        main_file_uri=["MAIN_PYTHON_FILE_URI"]);
    LANGUAGE PYTHON [AS PYSPARK_CODE]
   ```

   **Java 或 Scala**

   如要使用 `main_file_uri` 選項，在 Java 或 Scala 中為 Spark 建立預存程序，請使用下列程式碼範例：

   ```
   CREATE [OR REPLACE] PROCEDURE `PROJECT_ID`.DATASET.PROCEDURE_NAME(PROCEDURE_ARGUMENT)
    WITH CONNECTION `CONNECTION_PROJECT_ID.CONNECTION_REGION.CONNECTION_ID`
    OPTIONS (
        engine="SPARK", runtime_version="RUNTIME_VERSION",
        main_file_uri=["MAIN_JAR_URI"]);
    LANGUAGE JAVA|SCALA
   ```

   如要使用 `main_class` 和 `jar_uris` 選項，在 Java 或 Scala 中為 Spark 建立預存程序，請使用下列程式碼範例：

   ```
   CREATE [OR REPLACE] PROCEDURE `PROJECT_ID`.DATASET.PROCEDURE_NAME(PROCEDURE_ARGUMENT)
    WITH CONNECTION `CONNECTION_PROJECT_ID.CONNECTION_REGION.CONNECTION_ID`
    OPTIONS (
        engine="SPARK", runtime_version="RUNTIME_VERSION",
        main_class=["CLASS_NAME"],
        jar_uris=["URI"]);
    LANGUAGE JAVA|SCALA
   ```

   請替換下列項目：

   * `PROJECT_ID`：您要在其中建立預存程序的專案，例如 `myproject`。
   * `DATASET`：要建立預存程序的資料集，例如 `mydataset`。
   * `PROCEDURE_NAME`：要在 BigQuery 中執行的預存程序名稱，例如 `mysparkprocedure`。
   * `PROCEDURE_ARGUMENT`：輸入引數的參數。

     在這個參數中，請指定下列欄位：

     + `ARGUMENT_MODE`：引數模式。

       有效值包括 `IN`、`OUT` 和 `INOUT`。預設值為 `IN`。
     + `ARGUMENT_NAME`：引數的名稱。
     + `ARGUMENT_TYPE`：引數類型。

     例如：`myproject.mydataset.mysparkproc(num INT64)`。

     詳情請參閱本文中的「[以 `IN` 參數形式傳遞值](#pass-input-parameter)」或「[`OUT` 和 `INOUT` 參數](#pass-input-output-parameter)」。
   * `CONNECTION_PROJECT_ID`：包含要執行 Spark 程序之[連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw)的專案。
   * `CONNECTION_REGION`：包含要執行 Spark 程序之連線的區域，例如 `us`。
   * `CONNECTION_ID`：連線 ID，例如 `myconnection`。

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個部分的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
   * `RUNTIME_VERSION`：Spark 的執行階段版本，例如 `2.2`。
   * `MAIN_PYTHON_FILE_URI`：PySpark 檔案的路徑，例如 `gs://mybucket/mypysparkmain.py`。

     或者，如要在 `CREATE PROCEDURE` 陳述式中加入預存程序的本文，請在 `LANGUAGE PYTHON AS` 後方加入 `PYSPARK_CODE`，如本文「[使用內嵌程式碼](#use-inline-code)」一節的範例所示。
   * `PYSPARK_CODE`：如果您想內嵌傳遞程序主體，請在 `CREATE
     PROCEDURE` 陳述式中定義 PySpark 應用程式。

     此值為字串常值。如果程式碼包含引號和反斜線，必須逸出或以原始字串表示。舉例來說，程式碼傳回的 `"\n";` 可以表示為下列其中一種：

     + 引述的字串：`"return \"\\n\";"`。引號和反斜線都會逸出。
     + 加三引號的字串：`"""return "\\n";"""`。反斜線會逸出，但引號不會。
     + 原始字串：`r"""return "\n";"""`。不需要逸出。如要瞭解如何新增內嵌 PySpark 程式碼，請參閱「[使用內嵌程式碼](#use-inline-code)」。
   * `MAIN_JAR_URI`：包含 `main` 類別的 JAR 檔案路徑，例如 `gs://mybucket/my_main.jar`。
   * `CLASS_NAME`：以 `jar_uris` 選項設定的 JAR 中的類別完整名稱，例如 `com.example.wordcount`。
   * `URI`：包含 `main` 類別中指定類別的 JAR 檔案路徑，例如 `gs://mybucket/mypysparkmain.jar`。

   如要瞭解可在 `OPTIONS` 中指定的其他選項，請參閱[程序選項清單](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#procedure_option_list)。

### 使用 PySpark 編輯器

使用 PySpark 編輯器建立程序時，不需要使用 `CREATE PROCEDURE` 陳述式。請直接在 PySpark 編輯器中新增 Python 程式碼，然後儲存或執行程式碼。

如要在 PySpark 編輯器中建立 Spark 預存程序，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如要直接輸入 PySpark 程式碼，請開啟 PySpark 編輯器。如要開啟 PySpark 編輯器，請點選「建立 SQL 查詢」add\_box旁的 arrow\_drop\_down 選單，然後選取「建立 PySpark 程序」。
3. 如要設定選項，請依序按一下「更多」**>「PySpark 選項」**，然後執行下列操作：

   1. 指定要執行 PySpark 程式碼的位置。
   2. 在「連線」欄位中，指定 Spark 連線。
   3. 在「Stored procedure invocation」(預存程序叫用) 部分，指定要儲存所產生暫時預存程序的資料集。您可以設定特定資料集，或允許使用臨時資料集來叫用 PySpark 程式碼。

      系統會根據上一個步驟中指定的位置產生臨時資料集。如果指定資料集名稱，請確保資料集和 Spark 連線位於相同位置。
   4. 在「Parameters」部分中，定義預存程序的參數。參數值只會在 PySpark 程式碼的工作階段執行期間使用，但宣告本身會儲存在程序中。
   5. 在「Advanced options」(進階選項) 部分，指定程序選項。
      如需程序選項的詳細清單，請參閱[程序選項清單](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#procedure_option_list)。

   1. 在「屬性」部分中，新增鍵/值組合來設定工作。您可以使用「[Managed Service for Apache Spark 支援的 Spark 屬性](https://docs.cloud.google.com/dataproc-serverless/docs/concepts/properties?hl=zh-tw#supported_spark_properties)」中的任何鍵/值組合。

   1. 在「服務帳戶設定」中，指定 PySpark 程式碼在工作階段執行期間要使用的自訂服務帳戶、CMEK、暫存資料集和暫存 Cloud Storage 資料夾。
   2. 按一下 [儲存]。

#### 儲存 Spark 預存程序

使用 PySpark 編輯器[建立預存程序](#use-python-pyspark-editor)後，即可儲存該程序。步驟如下：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，[使用 PySpark 編輯器以 Python 建立 Spark 的預存程序](#use-python-pyspark-editor)。
3. 依序點按
4. 在「儲存預存程序」對話方塊中，指定要儲存預存程序的資料集名稱，以及預存程序的名稱。
5. 按一下 [儲存]。

   如果只想執行 PySpark 程式碼，不想儲存為預存程序，可以點選「執行」，而非「儲存」。

### 使用自訂容器

[自訂容器](https://docs.cloud.google.com/dataproc-serverless/docs/guides/custom-containers?hl=zh-tw)會為工作負載的驅動程式和執行器程序提供執行階段環境。如要使用自訂容器，請使用下列程式碼範例：

```
CREATE OR REPLACE PROCEDURE `PROJECT_ID`.DATASET.PROCEDURE_NAME(PROCEDURE_ARGUMENT)
  WITH CONNECTION `CONNECTION_PROJECT_ID.CONNECTION_REGION.CONNECTION_ID`
  OPTIONS (
      engine="SPARK", runtime_version="RUNTIME_VERSION",
      container_image="CONTAINER_IMAGE", main_file_uri=["MAIN_PYTHON_FILE_URI"]);
  LANGUAGE PYTHON [AS PYSPARK_CODE]
```

請替換下列項目：

* `PROJECT_ID`：您要在其中建立預存程序的專案，例如 `myproject`。
* `DATASET`：要建立預存程序的資料集，例如 `mydataset`。
* `PROCEDURE_NAME`：要在 BigQuery 中執行的預存程序名稱，例如 `mysparkprocedure`。
* `PROCEDURE_ARGUMENT`：輸入引數的參數。

  在這個參數中，請指定下列欄位：

  + `ARGUMENT_MODE`：引數模式。

    有效值包括 `IN`、`OUT` 和 `INOUT`。預設值為 `IN`。
  + `ARGUMENT_NAME`：引數的名稱。
  + `ARGUMENT_TYPE`：引數類型。

  例如：`myproject.mydataset.mysparkproc(num INT64)`。

  詳情請參閱本文中的「[將值做為 `IN` 參數傳遞](#pass-input-parameter)」一節，或「[`OUT` 和 `INOUT` 參數](#pass-input-output-parameter)」一節。
* `CONNECTION_PROJECT_ID`：包含要執行 Spark 程序之[連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw)的專案。
* `CONNECTION_REGION`：包含要執行 Spark 程序之連線的區域，例如 `us`。
* `CONNECTION_ID`：連線 ID，例如 `myconnection`。

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
* `RUNTIME_VERSION`：Spark 的執行階段版本，例如 `2.2`。
* `MAIN_PYTHON_FILE_URI`：PySpark 檔案的路徑，例如 `gs://mybucket/mypysparkmain.py`。

  或者，如要在 `CREATE PROCEDURE` 陳述式中加入預存程序的本文，請在 `LANGUAGE PYTHON AS` 後方加入 `PYSPARK_CODE`，如本文「[使用內嵌程式碼](#use-inline-code)」一節中的範例所示。
* `PYSPARK_CODE`：如果您想內嵌傳遞程序主體，請在 `CREATE
  PROCEDURE` 陳述式中定義 PySpark 應用程式。

  此值為字串常值。如果程式碼包含引號和反斜線，必須逸出這些字元，或以原始字串表示。舉例來說，程式碼傳回的 `"\n";` 可以表示為下列其中一種：

  + 引述的字串：`"return \"\\n\";"`。引號和反斜線都會逸出。
  + 加三引號的字串：`"""return "\\n";"""`。反斜線會逸出，但引號不會。
  + 原始字串：`r"""return "\n";"""`。不需要逸出。如要瞭解如何新增內嵌 PySpark 程式碼，請參閱「[使用內嵌程式碼](#use-inline-code)」。
* [`CONTAINER_IMAGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#procedure_option_list)：[Artifact Registry](https://docs.cloud.google.com/artifact-registry?hl=zh-tw) 中的圖片路徑。其中只能包含程序中使用的程式庫。如未指定，系統會使用與執行階段版本相關聯的預設容器映像檔。

如要進一步瞭解如何使用 Spark 建構自訂容器映像檔，請參閱「[建構自訂容器映像檔](https://docs.cloud.google.com/dataproc-serverless/docs/guides/custom-containers?hl=zh-tw#build_a_custom_container_image)」。

## 呼叫 Spark 預存程序

[建立預存程序](#create-spark-procedure)後，您可以使用下列任一選項呼叫該程序：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的「類別」「傳統版 Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「傳統版 Explorer」窗格中展開專案，然後選取要執行的 Spark 預存程序。
4. 在「預存程序資訊」視窗中，按一下「叫用預存程序」。
   或者，您也可以展開「查看動作」選項，然後點按「叫用」。
5. 按一下「執行」。
6. 在「所有結果」部分中，按一下「查看結果」。
7. 選用步驟：在「查詢結果」部分，按照下列步驟操作：

   * 如要查看 Spark 驅動程式記錄，請按一下「執行詳細資料」。
   * 如要在 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw) 中查看記錄，請按一下「Job information」(工作資訊)，然後在「Log」(記錄) 欄位中點選「log」(記錄)。
   * 如要取得 Spark 記錄伺服器端點，請按一下「Job information」(工作資訊)，然後按一下「Spark history server」(Spark 記錄伺服器)。

### SQL

如要呼叫預存程序，請使用 [`CALL PROCEDURE`陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#call)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CALL `PROJECT_ID`.DATASET.PROCEDURE_NAME()
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

**注意：** 您也可以使用 [`bq show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show)，取得 Cloud Logging 篩選器資訊和 Spark 歷來叢集端點。如要瞭解如何取得記錄篩選器，請參閱本文的「[查看記錄篩選器](#view-log-filters)」一節。

## 使用自訂服務帳戶

您可以使用自訂服務帳戶，在 Spark 程式碼中存取資料，而不必使用 Spark 連線的服務身分來存取資料。

如要使用自訂服務帳戶，請在建立 Spark 預存程序時指定 `INVOKER` 安全模式 (使用 `EXTERNAL SECURITY INVOKER` 陳述式)，並在叫用預存程序時指定服務帳戶。

首次使用自訂服務帳戶執行 Spark 預存程序時，BigQuery 會建立 Spark 服務代理人，並授予該代理人必要權限。請務必在叫用 Spark 預存程序前，不要修改這項授權。詳情請參閱「[BigQuery Spark 服務代理程式](https://docs.cloud.google.com/iam/docs/service-agents?hl=zh-tw#bigquery-spark-service-agent)」。

如要從 Cloud Storage 存取及使用 Spark 程式碼，請務必將必要權限授予 Spark 連線的服務身分。您需要授予連線的服務帳戶 `storage.objects.get` IAM 權限或 `storage.objectViewer` IAM 角色。

如果已在連線中指定 Dataproc Metastore 和 Managed Service for Apache Spark 持續性記錄伺服器，則可選擇授予連線的服務帳戶存取權。詳情請參閱「[授予服務帳戶存取權](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw#grant-access)」。

```
CREATE OR REPLACE PROCEDURE `PROJECT_ID`.DATASET.PROCEDURE_NAME(PROCEDURE_ARGUMENT)
  EXTERNAL SECURITY INVOKER
  WITH CONNECTION `CONNECTION_PROJECT_ID.CONNECTION_REGION.CONNECTION_ID`
  OPTIONS (
      engine="SPARK", runtime_version="RUNTIME_VERSION",
      main_file_uri=["MAIN_PYTHON_FILE_URI"]);
  LANGUAGE PYTHON [AS PYSPARK_CODE]

SET @@spark_proc_properties.service_account='CUSTOM_SERVICE_ACCOUNT';
CALL PROJECT_ID.DATASET_ID.PROCEDURE_NAME();
```

您也可以在上述程式碼中加入下列引數：

```
SET @@spark_proc_properties.staging_bucket='BUCKET_NAME';
SET @@spark_proc_properties.staging_dataset_id='DATASET';
```

更改下列內容：

* `CUSTOM_SERVICE_ACCOUNT`：必填，您提供的自訂服務帳戶。
* `BUCKET_NAME`：選用。做為預設 Spark 應用程式檔案系統的 Cloud Storage bucket。如未提供，系統會在專案中建立預設的 Cloud Storage bucket，且該 bucket 會由在同一專案下執行的所有工作共用。
* `DATASET`：選用。用於儲存叫用程序所產生臨時資料的資料集。工作完成後，系統會清除資料。如未提供，系統會為工作建立預設的暫時性資料集。

自訂服務帳戶必須具備下列權限：

* 如要讀取及寫入做為預設 Spark 應用程式檔案系統的暫存 bucket，請按照下列步驟操作：

  + `storage.objects.*` 權限，或指定暫存值區的 `roles/storage.objectAdmin` IAM 角色。
  + 此外，如果未指定暫存值區，則專案必須具備 `storage.buckets.*` 權限或 `roles/storage.Admin` IAM 角色。
* (選用) 如要從 BigQuery 讀取資料，以及將資料寫入 BigQuery，請按照下列步驟操作：

  + BigQuery 資料表上的 `bigquery.tables.*`。
  + 專案的 `bigquery.readsessions.*`。
  + `roles/bigquery.admin` IAM 角色包含先前的權限。**注意：** 如果預存程序會將資料寫入暫時的 Cloud Storage 值區，然後[將 Cloud Storage 資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，則自訂服務帳戶必須具備專案的 `bigquery.jobs.create` 權限。如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」一文。
* (選用) 如要從 Cloud Storage 讀取資料及寫入資料：

  + `storage.objects.*` 權限，或 Cloud Storage 物件的 `roles/storage.objectAdmin` IAM 角色。
* (選用) 如要讀取及寫入用於 `INOUT/OUT` 參數的暫存資料集：

  + `bigquery.tables.*` 或 `roles/bigquery.dataEditor` IAM 角色。
  + 此外，如果未指定暫存資料集，則需要專案的 `bigquery.datasets.create` 權限或 `roles/bigquery.dataEditor` IAM 角色。

## Spark 預存程序範例

本節將舉例說明如何為 Apache Spark 建立預存程序。

### 使用 Cloud Storage 中的 PySpark 或 JAR 檔案

下列範例說明如何使用 `my-project-id.us.my-connection` 連線，以及儲存在 Cloud Storage 值區中的 PySpark 或 JAR 檔案，為 Spark 建立預存程序：

### Python

```
CREATE PROCEDURE my_bq_project.my_dataset.spark_proc()
WITH CONNECTION `my-project-id.us.my-connection`
OPTIONS(engine="SPARK", runtime_version="2.2", main_file_uri="gs://my-bucket/my-pyspark-main.py")
LANGUAGE PYTHON
```

### Java 或 Scala

使用 `main_file_uri` 建立預存程序：

```
CREATE PROCEDURE my_bq_project.my_dataset.scala_proc_wtih_main_jar()
WITH CONNECTION `my-project-id.us.my-connection`
OPTIONS(engine="SPARK", runtime_version="2.2", main_file_uri="gs://my-bucket/my-scala-main.jar")
LANGUAGE SCALA
```

使用 `main_class` 建立預存程序：

```
CREATE PROCEDURE my_bq_project.my_dataset.scala_proc_with_main_class()
WITH CONNECTION `my-project-id.us.my-connection`
OPTIONS(engine="SPARK", runtime_version="2.2",
main_class="com.example.wordcount", jar_uris=["gs://my-bucket/wordcount.jar"])
LANGUAGE SCALA
```

### 使用內嵌程式碼

以下範例說明如何使用連線 `my-project-id.us.my-connection` 和內嵌 PySpark 程式碼，為 Spark 建立預存程序：

```
CREATE OR REPLACE PROCEDURE my_bq_project.my_dataset.spark_proc()
WITH CONNECTION `my-project-id.us.my-connection`
OPTIONS(engine="SPARK", runtime_version="2.2")
LANGUAGE PYTHON AS R"""
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("spark-bigquery-demo").getOrCreate()

# Load data from BigQuery.
words = spark.read.format("bigquery") \
  .option("table", "bigquery-public-data:samples.shakespeare") \
  .load()
words.createOrReplaceTempView("words")

# Perform word count.
word_count = words.select('word', 'word_count').groupBy('word').sum('word_count').withColumnRenamed("sum(word_count)", "sum_word_count")
word_count.show()
word_count.printSchema()

# Saving the data to BigQuery
word_count.write.format("bigquery") \
  .option("writeMethod", "direct") \
  .save("wordcount_dataset.wordcount_output")
"""
```

### 將值做為輸入參數傳遞

下列範例顯示在 Python 中，將值做為輸入參數傳遞的兩種方法：

#### 方法 1：使用環境變數

在 PySpark 程式碼中，您可以透過 Spark 驅動程式和執行器中的環境變數，取得 Spark 儲存程序的輸入參數。環境變數名稱的格式為 `BIGQUERY_PROC_PARAM.PARAMETER_NAME`，其中 `PARAMETER_NAME` 是輸入參數的名稱。舉例來說，如果輸入參數的名稱是 `var`，對應的環境變數名稱就是 `BIGQUERY_PROC_PARAM.var`。輸入參數採用 [JSON 編碼](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_encodings)。在 PySpark 程式碼中，您可以從環境變數取得 JSON 字串格式的輸入參數值，並將其解碼為 Python 變數。

以下範例說明如何在 PySpark 程式碼中取得 `INT64` 類型的輸入參數值：

```
CREATE OR REPLACE PROCEDURE my_bq_project.my_dataset.spark_proc(num INT64)
WITH CONNECTION `my-project-id.us.my-connection`
OPTIONS(engine="SPARK", runtime_version="2.2")
LANGUAGE PYTHON AS R"""
from pyspark.sql import SparkSession
import os
import json

spark = SparkSession.builder.appName("spark-bigquery-demo").getOrCreate()
sc = spark.sparkContext

# Get the input parameter num in JSON string and convert to a Python variable
num = int(json.loads(os.environ["BIGQUERY_PROC_PARAM.num"]))

"""
```

#### 方法 2：使用內建程式庫

在 PySpark 程式碼中，您只要匯入內建程式庫，即可用來填入所有類型的參數。如要將參數傳遞至執行器，請在 Spark 驅動程式中以 Python 變數的形式填入參數，然後將值傳遞至執行器。內建程式庫支援大多數 BigQuery 資料類型，但 `INTERVAL`、`GEOGRAPHY`、`NUMERIC` 和 `BIGNUMERIC` 除外。

| BigQuery 資料類型 | Python 資料型別 |
| --- | --- |
| `BOOL` | `bool` |
| `STRING` | `str` |
| `FLOAT64` | `float` |
| `INT64` | `int` |
| `BYTES` | `bytes` |
| `DATE` | `datetime.date` |
| `TIMESTAMP` | `datetime.datetime` |
| `TIME` | `datetime.time` |
| `DATETIME` | `datetime.datetime` |
| `Array` | `Array` |
| `Struct` | `Struct` |
| `JSON` | `Object` |
| `NUMERIC` | 不支援 |
| `BIGNUMERIC` | 不支援 |
| `INTERVAL` | 不支援 |
| `GEOGRAPHY` | 不支援 |

以下範例說明如何匯入內建程式庫，並使用該程式庫在 PySpark 程式碼中填入 INT64 類型的輸入參數，以及 ARRAY<STRUCT<a INT64, b STRING>> 類型的輸入參數：

```
CREATE OR REPLACE PROCEDURE my_bq_project.my_dataset.spark_proc(num INT64, info ARRAY<STRUCT<a INT64, b STRING>>)
WITH CONNECTION `my-project-id.us.my-connection`
OPTIONS(engine="SPARK", runtime_version="2.2")
LANGUAGE PYTHON AS R"""
from pyspark.sql import SparkSession
from bigquery.spark.procedure import SparkProcParamContext

def check_in_param(x, num):
  return x['a'] + num

def main():
  spark = SparkSession.builder.appName("spark-bigquery-demo").getOrCreate()
  sc=spark.sparkContext
  spark_proc_param_context = SparkProcParamContext.getOrCreate(spark)

  # Get the input parameter num of type INT64
  num = spark_proc_param_context.num

  # Get the input parameter info of type ARRAY<STRUCT<a INT64, b STRING>>
  info = spark_proc_param_context.info

  # Pass the parameter to executors
  df = sc.parallelize(info)
  value = df.map(lambda x : check_in_param(x, num)).sum()

main()
"""
```

在 Java 或 Scala 程式碼中，您可以透過 Spark 驅動程式和執行器的環境變數，取得 Spark 預存程序的輸入參數。環境變數名稱的格式為 `BIGQUERY_PROC_PARAM.PARAMETER_NAME`，其中 `PARAMETER_NAME` 是輸入參數的名稱。舉例來說，如果輸入參數的名稱是 var，對應的環境變數名稱就是 `BIGQUERY_PROC_PARAM.var`。在 Java 或 Scala 程式碼中，您可以從環境變數取得輸入參數值。

以下範例說明如何從環境變數取得輸入參數的值，並傳送至 Scala 程式碼：

```
val input_param = sys.env.get("BIGQUERY_PROC_PARAM.input_param").get
```

下列範例說明如何從環境變數取得輸入參數，並傳送至 Java 程式碼：

```
String input_param = System.getenv("BIGQUERY_PROC_PARAM.input_param");
```

### 以 `OUT` 和 `INOUT` 參數形式傳遞值

輸出參數會從 Spark 程序傳回值，而 `INOUT` 參數會接受程序的值，並從程序傳回值。如要使用 `OUT` 和 `INOUT` 參數，請在建立 Spark 程序時，於參數名稱前加入 `OUT` 或 `INOUT` 關鍵字。在 PySpark 程式碼中，您可以使用內建程式庫，將值做為 `OUT` 或 `INOUT` 參數傳回。與輸入參數相同，內建程式庫支援大多數 BigQuery 資料類型，但 `INTERVAL`、`GEOGRAPHY`、`NUMERIC` 和 `BIGNUMERIC` 除外。以 `OUT` 或 `INOUT` 參數形式傳回時，`TIME` 和 `DATETIME` 型別值會轉換為世界標準時間時區。

```
CREATE OR REPLACE PROCEDURE my_bq_project.my_dataset.pyspark_proc(IN int INT64, INOUT datetime DATETIME,OUT b BOOL, OUT info ARRAY<STRUCT<a INT64, b STRING>>, OUT time TIME, OUT f FLOAT64, OUT bs BYTES, OUT date DATE, OUT ts TIMESTAMP, OUT js JSON)
WITH CONNECTION `my_bq_project.my_dataset.my_connection`
OPTIONS(engine="SPARK", runtime_version="2.2") LANGUAGE PYTHON AS
R"""
from pyspark.sql.session import SparkSession
import datetime
from bigquery.spark.procedure import SparkProcParamContext

spark = SparkSession.builder.appName("bigquery-pyspark-demo").getOrCreate()
spark_proc_param_context = SparkProcParamContext.getOrCreate(spark)

# Reading the IN and INOUT parameter values.
int = spark_proc_param_context.int
dt = spark_proc_param_context.datetime
print("IN parameter value: ", int, ", INOUT parameter value: ", dt)

# Returning the value of the OUT and INOUT parameters.
spark_proc_param_context.datetime = datetime.datetime(1970, 1, 1, 0, 20, 0, 2, tzinfo=datetime.timezone.utc)
spark_proc_param_context.b = True
spark_proc_param_context.info = [{"a":2, "b":"dd"}, {"a":2, "b":"dd"}]
spark_proc_param_context.time = datetime.time(23, 20, 50, 520000)
spark_proc_param_context.f = 20.23
spark_proc_param_context.bs = b"hello"
spark_proc_param_context.date = datetime.date(1985, 4, 12)
spark_proc_param_context.ts = datetime.datetime(1970, 1, 1, 0, 20, 0, 2, tzinfo=datetime.timezone.utc)
spark_proc_param_context.js = {"name": "Alice", "age": 30}
""";
```

### 從 Hive Metastore 資料表讀取資料，並將結果寫入 BigQuery

以下範例說明如何轉換 Hive Metastore 資料表，並將結果寫入 BigQuery：

```
CREATE OR REPLACE PROCEDURE my_bq_project.my_dataset.spark_proc()
WITH CONNECTION `my-project-id.us.my-connection`
OPTIONS(engine="SPARK", runtime_version="2.2")
LANGUAGE PYTHON AS R"""
from pyspark.sql import SparkSession

spark = SparkSession \
   .builder \
   .appName("Python Spark SQL Managed Service for Apache Spark Hive Metastore integration test example") \
   .enableHiveSupport() \
   .getOrCreate()

spark.sql("CREATE DATABASE IF NOT EXISTS records")

spark.sql("CREATE TABLE IF NOT EXISTS records.student (eid int, name String, score int)")

spark.sql("INSERT INTO records.student VALUES (1000000, 'AlicesChen', 10000)")

df = spark.sql("SELECT * FROM records.student")

df.write.format("bigquery") \
  .option("writeMethod", "direct") \
  .save("records_dataset.student")
"""
```

## 查看記錄檔篩選器

[呼叫 Spark 預存程序](#call-spark-procedure)後，您就能查看記錄資訊。如要取得 Cloud Logging 篩選器資訊和 Spark 歷來叢集端點，請使用 [`bq
show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show)。篩選器資訊位於子項工作的 `SparkStatistics` 欄位下方。如要取得記錄篩選器，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，列出預存程序指令碼工作的子項工作：

   ```
   bq ls -j --parent_job_id=$parent_job_id
   ```

   如要瞭解如何取得工作 ID，請參閱「[查看工作詳細資料](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)」。

   輸出結果會與下列內容相似：

   ```
                   jobId                         Job Type     State       Start Time         Duration
   ---------------------------------------------- ---------   ---------  ---------------  ----------------
   script_job_90fb26c32329679c139befcc638a7e71_0   query      SUCCESS   07 Sep 18:00:27   0:05:15.052000
   ```
3. 找出預存程序的 `jobId`，然後使用 `bq
   show` 指令查看工作詳細資料：

   ```
   bq show --format=prettyjson --job $child_job_id
   ```

   複製 `sparkStatistics` 欄位，因為後續步驟會用到。

   輸出結果會與下列內容相似：

   ```
   {
   "configuration": {...}
   …
   "statistics": {
    …
     "query": {
       "sparkStatistics": {
         "loggingInfo": {
           "projectId": "myproject",
           "resourceType": "myresource"
         },
         "sparkJobId": "script-job-90f0",
         "sparkJobLocation": "us-central1"
       },
       …
     }
   }
   }
   ```
4. 如要記錄，請使用 `SparkStatistics` 欄位[產生記錄篩選器](https://docs.cloud.google.com/logging/docs/view/building-queries?hl=zh-tw)：

   ```
   resource.type = sparkStatistics.loggingInfo.resourceType
   resource.labels.resource_container=sparkStatistics.loggingInfo.projectId
   resource.labels.spark_job_id=sparkStatistics.sparkJobId
   resource.labels.location=sparkStatistics.sparkJobLocation
   ```

   記錄會寫入受監控的 `bigquery.googleapis.com/SparkJob` 資源。記錄檔會標示 `INFO`、`DRIVER` 和 `EXECUTOR` 元件。如要篩選 Spark 驅動程式的記錄，請將 `labels.component = "DRIVER"` 元件新增至記錄篩選器。如要篩選 Spark 執行器的記錄，請將 `labels.component = "EXECUTOR"` 元件新增至記錄篩選器。

## 使用客戶自行管理的加密金鑰

BigQuery Spark 程序會使用客戶管理的加密金鑰 (CMEK) 保護您的內容，並搭配 BigQuery 提供的預設加密功能。如要在 Spark 程序中使用 CMEK，請先觸發 BigQuery [加密服務帳戶的建立作業，並授予必要權限](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#grant_permission)。如果專案套用了 [CMEK 組織政策](https://docs.cloud.google.com/kms/docs/cmek-org-policy?hl=zh-tw)，Spark 程序也會支援這些政策。

如果預存程序使用 `INVOKER` 安全模式，則呼叫程序時，應透過 SQL 系統變數指定 CMEK。否則，您可透過與預存程序相關聯的連線指定 CMEK。

建立 Spark 預存程序時，如要透過連線指定 CMEK，請使用下列程式碼範例：

```
bq mk --connection --connection_type='SPARK' \
 --properties='{"kms_key_name"="projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING_NAME/cryptoKeys/KMS_KEY_NAME"}' \
 --project_id=PROJECT_ID \
 --location=LOCATION \
 CONNECTION_NAME
```

如要在呼叫程序時透過 SQL 系統變數指定 CMEK，請使用下列程式碼範例：

```
SET @@spark_proc_properties.service_account='CUSTOM_SERVICE_ACCOUNT';
SET @@spark_proc_properties.kms_key_name='projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING_NAME/cryptoKeys/KMS_KEY_NAME;
CALL PROJECT_ID.DATASET_ID.PROCEDURE_NAME();
```

## 使用 VPC Service Controls

VPC Service Controls 可用來設定安全 perimeter，以防範資料遭竊。如要搭配 Spark 程序使用 VPC Service Controls，進一步提升安全性，請先[建立服務周圍區域](https://docs.cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=zh-tw)。

如要全面保護 Spark 程序作業，請將下列 API 新增至服務周圍區域：

* BigQuery API (`bigquery.googleapis.com`)
* Cloud Logging API (`logging.googleapis.com`)
* Cloud Storage API (`storage.googleapis.com`)，如果您使用 Cloud Storage
* Artifact Registry API (`artifactregistry.googleapis.com`) 或 Container Registry API (`containerregistry.googleapis.com`)，如果您使用自訂容器
* Dataproc Metastore API (`metastore.googleapis.com`) 和 Cloud Run Admin API (`run.googleapis.com`)，前提是您使用 Dataproc Metastore

將 Spark 程序查詢專案新增至範圍。將代管 Spark 程式碼或資料的其他專案新增至範圍。

## 最佳做法

* 首次在專案中使用連線時，系統會額外花費約一分鐘的時間佈建。如要節省時間，建立 Spark 預存程序時，可以重複使用現有的 Spark 連線。
* 為實際工作環境建立 Spark 程序時，Google 建議指定執行階段版本。如要查看支援的執行階段版本清單，請參閱「[Managed Service for Apache Spark 執行階段版本](https://docs.cloud.google.com/dataproc-serverless/docs/concepts/versions/dataproc-serverless-versions?hl=zh-tw)」。建議使用長期支援 (LTS) 版本。
* 在 Spark 程序中指定自訂容器時，建議使用 Artifact Registry 和[映像檔串流](https://docs.cloud.google.com/dataproc-serverless/docs/guides/custom-containers?hl=zh-tw#image_streaming)。
* 如要提升效能，您可以在 Spark 程序中指定[資源分配屬性](https://docs.cloud.google.com/dataproc-serverless/docs/concepts/properties?hl=zh-tw#resource_allocation_properties)。Spark 預存程序支援的資源分配屬性清單，與 Managed Service for Apache Spark 相同。

## 限制

* 您只能使用 [gRPC 端點通訊協定](https://docs.cloud.google.com/dataproc-metastore/docs/about-endpoint-protocols?hl=zh-tw#grpc)連線至 [Dataproc Metastore](https://docs.cloud.google.com/dataproc-metastore/docs/overview?hl=zh-tw)。系統不支援其他類型的 Hive Metastore。
* [客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/kms/docs/cmek?hl=zh-tw) 僅適用於客戶建立單一區域 Spark 程序時。系統不支援全域區域 CMEK 金鑰和多區域 CMEK 金鑰，例如 `EU` 或 `US`。
* 只有 PySpark 支援傳遞輸出參數。
* 如果透過[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)，將與 Spark 預存程序相關聯的資料集複製到目的地區域，則只能在建立預存程序的區域中查詢該程序。
* Spark 不支援存取私有 VPC Service Controls 網路中的 HTTP 端點。

## 配額與限制

如要瞭解配額和限制，請參閱 [Spark 預存程序配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#spark-procedure)。

## 後續步驟

* 瞭解如何[查看預存程序](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw#view_the_body_of_a_routine)。
* 瞭解如何[刪除預存程序](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw#delete_a_routine)。
* 瞭解如何[使用 SQL 預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]