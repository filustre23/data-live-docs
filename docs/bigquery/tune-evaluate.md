Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用微調和評估功能提升模型效能

本文說明如何建立參照 [Vertex AI `gemini-2.0-flash-001` 模型的 BigQuery ML [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw#gemini-models)接著，您可以使用[監督式微調](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw#supervised_tuning)，以新訓練資料微調模型，然後使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估模型。

如果您需要自訂代管的 Vertex AI 模型，例如難以在提示中簡潔定義模型的預期行為，或是提示無法持續產生預期結果，即可使用調整功能。監督式微調也會透過下列方式影響模型：

* 引導模型以特定風格回覆，例如更簡潔或更詳細。
* 教導模型新的行為，例如以特定角色回應提示。
* 讓模型使用新資訊更新自己。

在本教學課程中，目標是讓模型生成的文字風格和內容，盡可能符合提供的基準真相內容。

## 必要的角色

如要執行本教學課程，您需要下列 Identity and Access Management (IAM) 角色：

* 建立及使用 BigQuery 資料集、連線和模型：BigQuery 管理員 (`roles/bigquery.admin`)。
* 將權限授予連線的服務帳戶：專案 IAM 管理員 (`roles/resourcemanager.projectIamAdmin`)。

這些預先定義的角色具備執行本文所述工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 建立資料集：`bigquery.datasets.create`
* 建立表格：`bigquery.tables.create`
* 建立、委派及使用連線：
  `bigquery.connections.*`
* 設定預設連線：`bigquery.config.*`
* 設定服務帳戶權限：
  `resourcemanager.projects.getIamPolicy` 和
  `resourcemanager.projects.setIamPolicy`
* 建立模型並執行推論：
  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
  + `bigquery.models.updateMetadata`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery、BigQuery Connection、Vertex AI 和 Compute Engine API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com%2Ccompute.googleapis.com&hl=zh-tw)

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* **BigQuery:** You incur costs for the queries that you run in
  BigQuery.
* **BigQuery ML:** You incur costs for the model that you
  create and the processing that you perform in BigQuery ML.
* **Vertex AI:** You incur costs for calls to and
  supervised tuning of the `gemini-2.0-flash-001` model.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

詳情請參閱下列資源：

* [BigQuery 儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)
* [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)
* [Vertex AI 定價](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw)

# 建立資料集

建立 BigQuery 資料集來儲存機器學習模型。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下專案名稱。
3. 依序點按 more\_vert「View actions」(查看動作) >「Create dataset」(建立資料集)
4. 在「建立資料集」頁面中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 針對「位置類型」選取「多區域」，然後選取「美國」。
   * 其餘設定請保留預設狀態，然後按一下「建立資料集」。

### bq

如要建立新的資料集，請使用 [`bq mk --dataset` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)。

1. 建立名為 `bqml_tutorial` 的資料集，並將資料位置設為 `US`。

   ```
   bq mk --dataset \
     --location=US \
     --description "BigQuery ML tutorial dataset." \
     bqml_tutorial
   ```
2. 確認資料集已建立完成：

   ```
   bq ls
   ```

### API

請呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法，搭配已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)。

```
{
  "datasetReference": {
     "datasetId": "bqml_tutorial"
  }
}
```

## 建立測試資料表

根據 Hugging Face 的公開 [task955\_wiki\_auto\_style\_transfer](https://huggingface.co/datasets/Lots-of-LoRAs/task955_wiki_auto_style_transfer) 資料集，建立訓練和評估資料表。

1. 開啟 [Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)。
2. 在 Cloud Shell 中執行下列指令，建立測試和評估資料表：

   ```
   python3 -m pip install pandas pyarrow fsspec huggingface_hub

   python3 -c "import pandas as pd; df_train = pd.read_parquet('hf://datasets/Lots-of-LoRAs/task955_wiki_auto_style_transfer/data/train-00000-of-00001.parquet').drop('id', axis=1); df_train['output'] = [x[0] for x in df_train['output']]; df_train.to_json('wiki_auto_style_transfer_train.jsonl', orient='records', lines=True);"

   python3 -c "import pandas as pd; df_valid = pd.read_parquet('hf://datasets/Lots-of-LoRAs/task955_wiki_auto_style_transfer/data/valid-00000-of-00001.parquet').drop('id', axis=1); df_valid['output'] = [x[0] for x in df_valid['output']]; df_valid.to_json('wiki_auto_style_transfer_valid.jsonl', orient='records', lines=True);"

   bq rm -t bqml_tutorial.wiki_auto_style_transfer_train

   bq rm -t bqml_tutorial.wiki_auto_style_transfer_valid

   bq load --source_format=NEWLINE_DELIMITED_JSON bqml_tutorial.wiki_auto_style_transfer_train wiki_auto_style_transfer_train.jsonl input:STRING,output:STRING

   bq load --source_format=NEWLINE_DELIMITED_JSON bqml_tutorial.wiki_auto_style_transfer_valid wiki_auto_style_transfer_valid.jsonl input:STRING,output:STRING
   ```

## 建立基準模型

透過 Vertex AI `gemini-2.0-flash-001` 模型建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式，建立遠端模型：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.gemini_baseline`
   REMOTE WITH CONNECTION DEFAULT
   OPTIONS (ENDPOINT ='gemini-2.0-flash-001');
   ```

   查詢作業會在幾秒內完成，完成後，`gemini_baseline` 模型會顯示在「Explorer」窗格的 `bqml_tutorial` 資料集中。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 查看基準模型成效

使用遠端模型執行 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)，查看模型在評估資料上的成效，無需進行任何調整。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   SELECT result, ground_truth
   FROM
     AI.GENERATE_TEXT(
       MODEL `bqml_tutorial.gemini_baseline`,
       (
         SELECT
           input AS prompt, output AS ground_truth
         FROM `bqml_tutorial.wiki_auto_style_transfer_valid`
         LIMIT 10
       ));
   ```

   如果您檢查輸出資料並比較 `result` 和 `ground_truth` 值，會發現基準模型產生的文字雖然準確反映了基準真相內容中提供的資訊，但風格卻大相逕庭。

## 評估基準模型

如要更詳細地評估模型效能，請使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)。這項函式會計算模型指標，用來評估生成文字的準確率和品質，藉此比較模型回覆與理想回覆的差異。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   SELECT *
   FROM
     ML.EVALUATE(
       MODEL `bqml_tutorial.gemini_baseline`,
       (
         SELECT
           input AS input_text, output AS output_text
         FROM `bqml_tutorial.wiki_auto_style_transfer_valid`
       ),
       STRUCT('text_generation' AS task_type));
   ```

輸出看起來類似以下內容：

```
   +---------------------+---------------------+-------------------------------------------+--------------------------------------------+
   | bleu4_score         | rouge-l_precision   | rouge-l_recall      | rouge-l_f1_score    | evaluation_status                          |
   +---------------------+---------------------+---------------------+---------------------+--------------------------------------------+
   | 0.23317359667074181 | 0.37809145226740043 | 0.45902937167791508 | 0.40956844061733139 | {                                          |
   |                     |                     |                     |                     |  "num_successful_rows": 176,               |
   |                     |                     |                     |                     |  "num_total_rows": 176                     |
   |                     |                     |                     |                     | }                                          |
   +---------------------+---------------------+ --------------------+---------------------+--------------------------------------------+
```

從評估指標來看，基準模型的效能還不錯，但生成的文字與基準真相的相似度偏低。這表示值得執行監督式調整，看看是否能改善這個用途的模型效能。

## 建立調整後模型

建立的遠端模型與「[建立模型](#create_a_baseline_model)」中建立的模型非常相似，但這次要指定 [`AS SELECT` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw#as_select)，提供訓練資料來調整模型。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式，建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw)：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.gemini_tuned`
     REMOTE
       WITH CONNECTION DEFAULT
     OPTIONS (
       endpoint = 'gemini-2.0-flash-001',
       max_iterations = 500,
       data_split_method = 'no_split')
   AS
   SELECT
     input AS prompt, output AS label
   FROM `bqml_tutorial.wiki_auto_style_transfer_train`;
   ```

   查詢作業需要幾分鐘才會完成，完成後，`gemini_tuned` 模型就會顯示在「Explorer」(探索工具) 窗格的 `bqml_tutorial` 資料集中。由於查詢是使用 `CREATE MODEL` 建立模型，因此不會有查詢結果。

## 查看微調模型的成效

執行 `AI.GENERATE_TEXT` 函式，查看微調模型在評估資料上的成效。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   SELECT result, ground_truth
   FROM
     AI.GENERATE_TEXT(
       MODEL `bqml_tutorial.gemini_tuned`,
       (
         SELECT
           input AS prompt, output AS ground_truth
         FROM `bqml_tutorial.wiki_auto_style_transfer_valid`
         LIMIT 10
       ));
   ```

   如果檢查輸出資料，會發現微調模型產生的文字風格與基準真相內容更為相似。

## 評估微調模型

使用 `ML.EVALUATE` 函式，比較微調模型的回覆與理想回覆。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   SELECT *
   FROM
     ML.EVALUATE(
       MODEL `bqml_tutorial.gemini_tuned`,
       (
         SELECT
           input AS prompt, output AS label
         FROM `bqml_tutorial.wiki_auto_style_transfer_valid`
       ),
       STRUCT('text_generation' AS task_type));
   ```

輸出看起來類似以下內容：

```
   +---------------------+---------------------+-------------------------------------------+--------------------------------------------+
   | bleu4_score         | rouge-l_precision   | rouge-l_recall      | rouge-l_f1_score    | evaluation_status                          |
   +---------------------+---------------------+---------------------+---------------------+--------------------------------------------+
   | 0.416868792119966   | 0.642001000843349   | 0.55910008048151372 | 0.5907226262084847  | {                                          |
   |                     |                     |                     |                     |  "num_successful_rows": 176,               |
   |                     |                     |                     |                     |  "num_total_rows": 176                     |
   |                     |                     |                     |                     | }                                          |
   +---------------------+---------------------+ --------------------+---------------------+--------------------------------------------+
```

您可以看到，即使訓練資料集只使用了 1,408 個範例，但評估指標較高，表示效能顯著提升。

## 清除所用資源

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]