Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用遠端函式分析物件資料表

本文說明如何使用[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)分析[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)中的非結構化資料。

## 總覽

您可以使用遠端函式，分析物件資料表代表的非結構化資料。透過遠端函式，您可以呼叫在 Cloud Run functions 或 Cloud Run 上執行的函式，並將其程式化，以存取下列資源：

* Google 預先訓練的 AI 模型，包括 Cloud Vision API 和 Document AI。
* 開放原始碼程式庫，例如 [Apache Tika](https://tika.apache.org/)。
* 您自己的自訂模型。

如要使用遠端函式分析物件資料表資料，您必須在呼叫遠端函式時，為物件資料表中的物件產生並傳入[簽署網址](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#signed_urls)。這些簽署網址會授予遠端函式物件存取權。

## 所需權限

* 如要建立遠端函式使用的連線資源，您必須具備下列權限：

  + `bigquery.connections.create`
  + `bigquery.connections.get`
  + `bigquery.connections.list`
  + `bigquery.connections.update`
  + `bigquery.connections.use`
  + `bigquery.connections.delete`
* 如要建立遠端函式，您需要「Cloud Functions 開發人員」或「Cloud Run 開發人員」角色相關聯的權限。
* 如要叫用遠端函式，您需要[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#grant_permission_on_function)一文所述的權限。
* 如要使用遠端函式分析物件資料表，您必須具備物件資料表的 `bigquery.tables.getData` 權限。

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
- Enable the BigQuery, BigQuery Connection API, Cloud Run functions APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Ccloudfunctions.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery, BigQuery Connection API, Cloud Run functions APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Ccloudfunctions.googleapis.com&hl=zh-tw)

1. 確認 BigQuery 管理員已[建立連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)，並[設定 Cloud Storage 的存取權](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#access-storage)。

## 建立遠端函式

如需建立遠端函式的一般操作說明，請參閱「[使用遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)」。

建立遠端函式來分析物件資料表資料時，您必須傳入為物件資料表中的物件產生的[經簽署的網址](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#signed_urls)。如要這麼做，請使用 `STRING` 資料型別的輸入參數。簽署網址會以 HTTP `POST` 要求的 [`calls` 欄位中的輸入資料形式，提供給遠端函式。要求範例如下：](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#input_format)

```
{
  // Other fields omitted.
  "calls": [
    ["https://storage.googleapis.com/mybucket/1.pdf?X-Goog-SignedHeaders=abcd"],
    ["https://storage.googleapis.com/mybucket/2.pdf?X-Goog-SignedHeaders=wxyz"]
  ]
}
```

您可以使用方法，對已簽署的網址發出 HTTP `GET` 要求，藉此讀取遠端函式中的物件。遠端函式可以存取物件，因為簽署的網址會在查詢字串中包含驗證資訊。

為遠端函式指定 [`CREATE FUNCTION` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_function_statement)時，建議將 `max_batching_rows` 選項設為 1，以[避免 Cloud Run functions 超時](https://docs.cloud.google.com/functions/docs/concepts/exec?hl=zh-tw#timeout)，並提高處理作業的平行程度。

### 範例

下列 Cloud Run functions Python 程式碼範例會讀取儲存空間物件，並將內容長度傳回 BigQuery：

```
import functions_framework
import json
import urllib.request

@functions_framework.http
def object_length(request):
  calls = request.get_json()['calls']
  replies = []
  for call in calls:
    object_content = urllib.request.urlopen(call[0]).read()
    replies.append(len(object_content))
  return json.dumps({'replies': replies})
```

部署後，這個函式會有類似 `https://us-central1-myproject.cloudfunctions.net/object_length` 的端點。

以下範例說明如何根據這個 Cloud Run functions 函式建立 BigQuery 遠端函式：

```
CREATE FUNCTION mydataset.object_length(signed_url STRING) RETURNS INT64
REMOTE WITH CONNECTION `us.myconnection`
OPTIONS(
  endpoint = "https://us-central1-myproject.cloudfunctions.net/object_length",
  max_batching_rows = 1
);
```

如需逐步操作說明，請參閱[教學課程：使用遠端函式分析物件資料表](https://docs.cloud.google.com/bigquery/docs/remote-function-tutorial?hl=zh-tw)。

## 呼叫遠端函式

如要呼叫物件資料表資料的遠端函式，請在查詢的 [`select_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#select_list) 中參照遠端函式，然後在 [`FROM` 子句中呼叫 [`EXTERNAL_OBJECT_TRANSFORM` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/table-functions-built-in?hl=zh-tw#external_object_transform)，為物件產生已簽署的網址。](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#from_clause)

**注意：** 使用任一 [AI API](https://cloud.google.com/products/ai?hl=zh-tw) 時，請留意目標 API 的相關配額。如有必要，請使用 `LIMIT` 子句限制傳回的結果，以符合配額限制。

以下範例顯示典型的陳述式語法：

```
SELECT uri, function_name(signed_url) AS function_output
FROM EXTERNAL_OBJECT_TRANSFORM(TABLE my_dataset.object_table, ["SIGNED_URL"])
LIMIT 10000;
```

以下範例說明如何使用遠端函式，只處理物件表格內容的子集：

```
SELECT uri, function_name(signed_url) AS function_output
FROM EXTERNAL_OBJECT_TRANSFORM(TABLE my_dataset.object_table, ["SIGNED_URL"])
WHERE content_type = "application/pdf";
```

## 後續步驟

瞭解如何[對圖片物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/object-table-inference?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]