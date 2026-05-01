* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 遠端函式和 Translation API 教學課程

本教學課程說明如何建立 [BigQuery 遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)、叫用 [Cloud Translation API](https://docs.cloud.google.com/translate/docs/reference/api-overview?hl=zh-tw)，以及使用 SQL 和 Python 將任何語言的內容翻譯成西班牙文。

這項功能的用途包括：

* 將網站上的使用者留言翻譯成當地語言
* 將多種語言的支援要求翻譯成客服案件工作人員可理解的語言

## 目標

* 將必要角色指派給帳戶。
* 建立 Cloud Run 函式。
* 建立 BigQuery 資料集。
* 建立 BigQuery 連線和服務帳戶。
* 將權限授予 BigQuery 服務帳戶。
* 建立 BigQuery 遠端函式。
* 呼叫 BigQuery 遠端函式。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Cloud Run functions](https://cloud.google.com/functions/pricing?hl=zh-tw)
* [Cloud Translation](https://cloud.google.com/translate/pricing?hl=zh-tw)

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

## 事前準備

建議您為本教學課程建立 Google Cloud 專案。此外，請確認您具備完成本教學課程的必要角色。

### 設定 Google Cloud 專案

如要為本教學課程設定 Google Cloud 專案，請完成下列步驟：

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
- Enable the BigQuery, BigQuery Connection,
  Cloud Translation, Cloud Run functions, Cloud Build, Cloud Logging,
  Cloud Pub/Sub, Artifact Registry, and Cloud Run Admin APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery%2Cbigqueryconnection.googleapis.com%2Ctranslate.googleapis.com%2Ccloudfunctions%2Ccloudbuild.googleapis.com%2Clogging.googleapis.com%2Cpubsub.googleapis.com%2Cartifactregistry.googleapis.com%2Crun.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery, BigQuery Connection,
  Cloud Translation, Cloud Run functions, Cloud Build, Cloud Logging,
  Cloud Pub/Sub, Artifact Registry, and Cloud Run Admin APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery%2Cbigqueryconnection.googleapis.com%2Ctranslate.googleapis.com%2Ccloudfunctions%2Ccloudbuild.googleapis.com%2Clogging.googleapis.com%2Cpubsub.googleapis.com%2Cartifactregistry.googleapis.com%2Crun.googleapis.com&hl=zh-tw)

### 帳戶的必要角色

如要取得執行本教學課程中工作所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)
* [BigQuery Connection 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)
* [Cloud Functions 開發人員](https://docs.cloud.google.com/iam/docs/roles-permissions/cloudfunctions?hl=zh-tw#cloudfunctions.developer)  (`roles/cloudfunctions.developer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行本教學課程中工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行本教學課程中的工作，必須具備下列權限：

* `bigquery.datasets.create`
* `bigquery.connections.create`
* `bigquery.connections.get`
* `cloudfunctions.functions.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### Compute Engine 預設服務帳戶的必要角色

啟用 Cloud Run functions 的 API 時，系統會建立[預設 Compute Engine 服務帳戶](https://docs.cloud.google.com/compute/docs/access/service-accounts?hl=zh-tw#default_service_account)。如要完成本教學課程，您必須將 Cloud Translation API 使用者角色授予這個預設服務帳戶。

1. [取得指派給專案的 ID](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw#identifying_projects)。
2. 複製 Compute Engine 預設服務帳戶。預設服務帳戶如下所示：

   ```
   PROJECT_NUMBER-compute@developer.gserviceaccount.com
   ```

   將 `PROJECT_NUMBER` 替換為專案 ID。
3. 前往 Google Cloud 控制台的「IAM」(身分與存取權管理) 頁面。

   [前往 IAM](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project%2Cfolder%2CorganizationId&hl=zh-tw)
4. 選取專案。
5. 按一下「授予存取權」person\_add，然後在「新增主體」欄位中，貼上先前複製的 Compute Engine 預設服務帳戶。
6. 在「指派角色」清單中，搜尋並選取「Cloud Translation API User」。
7. 按一下 [儲存]。

## 建立 Cloud Run 函式

使用 Cloud Run 函式建立函式，將輸入文字翻譯成西班牙文。

1. [建立 Cloud Run 函式](https://docs.cloud.google.com/functions/docs/console-quickstart?hl=zh-tw#create_a_function)，並符合下列規格：

   * 在「Environment」(環境) 中選取「2nd gen」(第 2 代)。
   * 在「Function name」(函式名稱) 中輸入 `translation-handler`。
   * 在「Region」(區域) 中，選取「us-central1」。
   * 在「Maximum number of instances」(執行個體數量上限) 中輸入 `10`。

     這項設定位於「執行階段、建構作業、連線和安全性設定」專區。

     在本教學課程中，我們會使用低於預設值的值，控制傳送至 Translation 的要求比率。
   * 選取「Runtime」(執行階段) 底下的「Python 3.10」。
   * 在「Entry point」(進入點) 中輸入 `handle_translation`。
2. 在檔案清單中選取 **main.py**，然後貼上下列程式碼。

   在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

   ```
   from __future__ import annotations


   import flask
   import functions_framework
   from google.api_core.retry import Retry
   from google.cloud import translate

   # Construct a Translation Client object
   translate_client = translate.TranslationServiceClient()


   # Register an HTTP function with the Functions Framework
   @functions_framework.http
   def handle_translation(request: flask.Request) -> flask.Response:
       """BigQuery remote function to translate input text.

       Args:
           request: HTTP request from BigQuery
           https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#input_format

       Returns:
           HTTP response to BigQuery
           https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#output_format
       """
       try:
           # Parse request data as JSON
           request_json = request.get_json()
           # Get the project of the query
           caller = request_json["caller"]
           project = extract_project_from_caller(caller)
           if project is None:
               return flask.make_response(
                   flask.jsonify(
                       {
                           "errorMessage": (
                               'project can\'t be extracted from "caller":' f" {caller}."
                           )
                       }
                   ),
                   400,
               )
           # Get the target language code, default is Spanish ("es")
           context = request_json.get("userDefinedContext", {})
           target = context.get("target_language", "es")

           calls = request_json["calls"]
           translated = translate_text([call[0] for call in calls], project, target)

           return flask.jsonify({"replies": translated})
       except Exception as err:
           return flask.make_response(
               flask.jsonify({"errorMessage": f"Unexpected error {type(err)}:{err}"}),
               400,
           )


   def extract_project_from_caller(job: str) -> str:
       """Extract project id from full resource name of a BigQuery job.

       Args:
           job: full resource name of a BigQuery job, like
             "//bigquery.googleapi.com/projects/<project>/jobs/<job_id>"

       Returns:
           project id which is contained in the full resource name of the job.
       """
       path = job.split("/")
       return path[4] if len(path) > 4 else None


   def translate_text(
       calls: list[str], project: str, target_language_code: str
   ) -> list[str]:
       """Translates the input text to specified language using Translation API.

       Args:
           calls: a list of input text to translate.
           project: the project where the translate service will be used.
           target_language_code: The ISO-639 language code to use for translation
             of the input text. See
             https://cloud.google.com/translate/docs/advanced/discovering-supported-languages-v3#supported-target
               for the supported language list.

       Returns:
           a list of translated text.
       """
       location = "<your location>"
       parent = f"projects/{project}/locations/{location}"
       # Call the Translation API, passing a list of values and the target language
       response = translate_client.translate_text(
           request={
               "parent": parent,
               "contents": calls,
               "target_language_code": target_language_code,
               "mime_type": "text/plain",
           },
           retry=Retry(),
       )
       # Convert the translated value to a list and return it
       return [translation.translated_text for translation in response.translations]
   ```

   使用 `us-central1` 更新 `<your location>`。
3. 在檔案清單中選取 **requirements.txt**，然後貼上下列文字：

   ```
   Flask==2.2.2
   functions-framework==3.9.2
   google-cloud-translate==3.18.0
   Werkzeug==2.3.8
   ```
4. 按一下「部署」，然後等待函式部署完成。
5. 按一下「觸發條件」分頁標籤。
6. 複製「觸發網址」值並儲存，稍後會用到。建立 BigQuery 遠端函式時，請務必使用這個網址。

## 建立 BigQuery 資料集

[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#create-dataset)，其中會包含遠端函式。建立資料集時，請加入下列規格：

* 在「Dataset ID」(資料集 ID) 中輸入 `remote_function_test`。
* 「位置類型」請選取「多區域」。
* 在「多區域」部分，選取「美國 (多個美國地區)」。

## 建立 BigQuery 連線和服務帳戶

建立 BigQuery 連線，以便在 Cloud Run functions 和 Cloud Run 中，使用任何支援的語言實作遠端函式。建立連線時，系統會為該連線建立服務帳戶。

1. [建立 Google Cloud 資源連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)，並符合下列規格：

   * 在「連線類型」中，選取「BigLake 與遠端函式 (Cloud 資源)」
   * 在「Connection ID」(連線 ID) 中輸入 `remote-function-connection`。
   * 「位置類型」請選取「多區域」。
   * 在「多區域」部分，選取「美國 (多個美國地區)」。
2. [開啟「連線」清單](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#list-connections)，然後選取 **`us.remote-function-connection`**。
3. 複製服務帳戶 ID 並儲存，以供日後使用。您必須在下一個步驟中授予這個 ID 權限。

## 將權限授予 BigQuery 服務帳戶

您在上一個步驟中建立的服務帳戶必須具備使用 Cloud Run 的權限，BigQuery 遠端函式才能使用 Cloud Run 函式。如要授予服務帳戶權限，請完成下列步驟：

1. 前往「Cloud Run」頁面。

   [前往 Cloud Run](https://console.cloud.google.com/project/_/run?hl=zh-tw)。
2. 選取專案。
3. 勾選「`translation-handler`」旁的核取方塊。
4. 在「Permissions」(權限) 面板中，按一下「Add principal」(新增主體)。
5. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
6. 在「指派角色」清單中，搜尋並選取「Cloud Run Invoker」。
7. 按一下 [儲存]。

**注意：** 新權限最多可能需要一分鐘才會生效。

## 建立 BigQuery 遠端函式

如要使用 Cloud Run functions 函式，透過 BigQuery 遠端函式將文字翻譯成西班牙文，請完成下列步驟。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列查詢：

   ```
   CREATE OR REPLACE FUNCTION `remote_function_test.translate_text`(x STRING)
   RETURNS
   STRING
       REMOTE WITH CONNECTION `us.remote-function-connection`
   OPTIONS (
       endpoint = 'TRIGGER_URL',
       max_batching_rows = 10);
   ```

   將 `TRIGGER_URL` 替換為您先前建立 Cloud Run functions 函式時儲存的觸發條件網址。
3. 按一下「執行」。系統會顯示類似以下內容的訊息：

   ```
   This statement created a new function named
   your_project.remote_function_test.translate_text.
   ```

**注意：** 如要限制 HTTP 要求中包含的資料列數量，請將 `max_batching_rows` 選項設為 `10`。如果未指定 `max_batching_rows` 選項，BigQuery 會決定 HTTP 要求中包含的資料列數量。

## 呼叫 BigQuery 遠端函式

建立遠端函式後，請進行測試，確認函式已連結至 Cloud Run 函式，並以西班牙文產生預期結果。

1. 在 BigQuery 查詢編輯器中輸入下列查詢，然後點選「Run」(執行)。

   ```
   SELECT
     remote_function_test.translate_text('This new feature is fantastic!')
       AS translated_text;
   ```

   結果類似下列畫面：

   ```
   +-------------------------------------------+
   | translated_text                           |
   +-------------------------------------------+
   | ¡Esta nueva característica es fantástica! |
   +-------------------------------------------+
   ```
2. 選用：如要測試公開資料集的遠端函式，請輸入下列查詢，然後按一下「執行」。如要限制傳回的結果，請使用 `LIMIT` 子句。

   ```
   SELECT
       text,
       remote_function_test.translate_text(text) AS translated_text
   FROM
       (SELECT text FROM `bigquery-public-data.hacker_news.full` LIMIT 3);
   ```

   結果類似於下列內容：

   ```
   +---------------------------------------------------------------------------+
   | text                            | translated_text                         |
   +---------------------------------------------------------------------------+
   | These benchmarks look good.     | Estos puntos de referencia se ven bien. |
   | Who is using Java?              | ¿Quién está usando Java?                |
   | You need more database storage. | Necesitas más almacenamiento.           |
   +---------------------------------------------------------------------------+
   ```

## 刪除資源

如果您不打算在這個專案中使用這些函式，可以刪除專案，以免產生額外費用。這項操作會永久刪除與專案相關的所有資源。

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

## 後續步驟

* 瞭解如何在 BigQuery 中使用[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)。
* 瞭解[翻譯](https://docs.cloud.google.com/translate/docs/overview?hl=zh-tw)。
* 瞭解 [Cloud Run functions](https://docs.cloud.google.com/functions/docs/concepts/overview?hl=zh-tw)。
* 瞭解 [Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]