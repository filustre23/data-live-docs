Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用微調和評估功能提升模型效能 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何調整模型，讓模型在不改變整體意思的情況下，提供更精確的用詞或加入修飾語，使指定句子更豐富。您將建立參照 [Gemini Enterprise Agent Platform 模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw#gemini-models)的[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)，使用[監督式調整](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw#supervised_tuning)，然後透過 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估調整後的模型。

調整功能可協助您自訂託管的 Agent Platform 模型，例如難以在提示中定義預期行為，或提示無法持續產生預期結果時。監督式調整也會以下列方式影響模型：

* 引導模型傳回特定回覆風格，例如更簡潔或更詳細。
* 教導模型新行為，例如以特定角色回應提示。
* 讓模型根據新資訊更新。

在本教學課程中，目標是讓模型生成風格和內容盡可能接近所提供基準真相內容的文字。

## 目標

* 建立資料集。
* 將訓練和評估資料匯入資料表。
* 建立基準模型。
* 評估基準模型成效。
* 建立調整後的模型。
* 評估調整後模型的效能。

## 費用

在本文件中，您將使用下列 Google Cloud計費元件：

* **BigQuery.** You incur costs for the queries that you run in
  BigQuery.
* **BigQuery ML.** You incur costs for the model that you
  create and the processing that you perform in BigQuery ML.
* **Gemini Enterprise Agent Platform.** You incur costs for
  calls to and supervised tuning of the Gemini
  model.

您可以使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)，根據預測用量估算費用。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

詳情請參閱下列資源：

* [BigQuery 儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)
* [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)
* [Agent Platform 定價](https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing?hl=zh-tw)

## 事前準備

如要執行本教學課程，您必須具備下列 Identity and Access Management (IAM) 角色：

* 建立及使用 BigQuery 資料集、連結和模型：BigQuery 管理員 (`roles/bigquery.admin`)。
* 將權限授予連線的服務帳戶：專案 IAM 管理員 (`roles/resourcemanager.projectIamAdmin`)。

這些預先定義的角色具備執行本文件所述工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 建立資料集：`bigquery.datasets.create`
* 建立表格：`bigquery.tables.create`
* 建立、委派及使用連線：
  `bigquery.connections.*`
* 設定預設連線：`bigquery.config.*`
* 設定服務帳戶權限：`resourcemanager.projects.getIamPolicy`和`resourcemanager.projects.setIamPolicy`
* 建立模型並執行推論：
  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
  + `bigquery.models.updateMetadata`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

1. 在 Google Cloud 控制台的專案選取器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需具備特定 IAM 角色，只要您已獲派某個專案的角色，即可選取該專案。
   * **建立專案**：如要建立專案，您必須具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。如果採用這種做法，當您完成這些步驟後，就可以直接刪除該專案，並移除相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認 Google Cloud 專案已啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project)。
3. 啟用 BigQuery、BigQuery Connection、Agent Platform API 和 Compute Engine API (如有尚未啟用的 API)。

   **啟用 API 所需的角色**

   您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過擁有者角色 (`roles/owner`) 取得這項權限。否則，您可以透過 Service Usage 管理員角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com%2Ccompute.googleapis.com&hl=zh-tw)

## 建立資料集

如要建立 BigQuery 資料集，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」中展開專案，然後按一下「資料集」。
4. 在「Datasets」(資料集) 頁面，按一下add「Create dataset」(建立資料集)。
5. 在「建立資料集」窗格中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 在「資料位置」部分，選取「US」。

   其餘預設設定則保持不變。
6. 點選「建立資料集」。

### bq

如要建立新的資料集，請使用 [`bq mk --dataset` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)。

1. 建立名為 `bqml_tutorial` 的資料集，並將資料位置設為 `US`：

   ```
   bq mk --dataset \
     --location=US \
     --description "BigQuery ML tutorial dataset." \
     bqml_tutorial
   ```
2. 確認資料集已建立：

   ```
   bq ls
   ```

### API

使用定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法：

```
{
  "datasetReference": {
     "datasetId": "bqml_tutorial"
  }
}
```

## 建立測試資料表

根據 Hugging Face 的公開 [`task955_wiki_auto_style_transfer` 資料集](https://huggingface.co/datasets/Lots-of-LoRAs/task955_wiki_auto_style_transfer)，建立訓練和評估資料表。

1. 開啟 [Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)。
2. 在 Cloud Shell 建立測試和評估資料表：

   ```
   python3 -m pip install pandas pyarrow fsspec huggingface_hub

   python3 -c "import pandas as pd; df_train = pd.read_parquet('hf://datasets/Lots-of-LoRAs/task955_wiki_auto_style_transfer/data/train-00000-of-00001.parquet').drop('id', axis=1); df_train['output'] = [x[0] for x in df_train['output']]; df_train.to_json('wiki_auto_style_transfer_train.jsonl', orient='records', lines=True);"

   python3 -c "import pandas as pd; df_valid = pd.read_parquet('hf://datasets/Lots-of-LoRAs/task955_wiki_auto_style_transfer/data/valid-00000-of-00001.parquet').drop('id', axis=1); df_valid['output'] = [x[0] for x in df_valid['output']]; df_valid.to_json('wiki_auto_style_transfer_valid.jsonl', orient='records', lines=True);"

   bq load --replace=true --source_format=NEWLINE_DELIMITED_JSON bqml_tutorial.wiki_auto_style_transfer_train wiki_auto_style_transfer_train.jsonl input:STRING,output:STRING

   bq load --replace=true --source_format=NEWLINE_DELIMITED_JSON bqml_tutorial.wiki_auto_style_transfer_valid wiki_auto_style_transfer_valid.jsonl input:STRING,output:STRING
   ```

## 查看訓練資料

輸入的訓練資料是提示，要求模型在不改變句子大意的情況下，詳細說明句子。每個提示都包含一組相同的兩個正面範例和兩個負面範例，以及要改寫的句子。輸出內容則是模型產生的詳細句子。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式，查看輸入和輸出資料範例：

   ```
   SELECT * FROM bqml_tutorial.wiki_auto_style_transfer_train LIMIT 1;
   ```

   結果大致如下：

   ```
   +-----------------------------------------------+-------------------------------------------------+
   | input                                         | output                                          |
   +-----------------------------------------------+-------------------------------------------------+
   | Definition: In this task, we ask you to       | Merton College ( in full : The House or College |
   | elaborate the sentence without changing its   | of Scholars of Merton in the University of      |
   | general meaning. You can do so by explaining  | Oxford ) is one of the constituent colleges of  |
   | further the input sentence, using more        | the University of Oxford in England .           |
   | precise wording, adding qualifiers and        |                                                 |
   | auxiliary information etc.                    |                                                 |
   |                                               |                                                 |
   | Positive Example 1 -                          |                                                 |
   | Input: The Inheritance Cycle is a series of   |                                                 |
   | fantasy books written by Christopher Paolini. |                                                 |
   | Output: The Inheritance Cycle is a tetralogy  |                                                 |
   | of young adult high fantasy novels written by |                                                 |
   | American author Christopher Paolini.          |                                                 |
   |                                               |                                                 |
   | Positive Example 2 -                          |                                                 |
   | Input: The Greco-Roman or Graeco-Roman world, |                                                 |
   | refers to geographical regions and countries  |                                                 |
   | who had the language , culture , government   |                                                 |
   | or religion of the ancient Greeks and Romans. |                                                 |
   | Output: The Greco-Roman world , Greco-Roman   |                                                 |
   | culture , or the term Greco-Roman (spelled    |                                                 |
   | Graeco-Roman in the United Kingdom and the    |                                                 |
   | Commonwealth), when used as an adjective , as |                                                 |
   | understood by modern scholars and writers ,   |                                                 |
   | refers to those geographical regions and      |                                                 |
   | countries that culturally ( and so            |                                                 |
   |  historically ) were directly , long-term ,   |                                                 |
   | and intimately influenced by the language ,   |                                                 |
   | culture , government and religion of the      |                                                 |
   | ancient Greeks and Romans.                    |                                                 |
   |                                               |                                                 |
   | Negative Example 1 -                          |                                                 |
   | Input: Boryla, an American football           |                                                 |
   | quarterback, did not participate in the 1952  |                                                 |
   | playoffs.                                     |                                                 |
   | Output: Boryla was not in the 1952 playoffs.  |                                                 |
   |                                               |                                                 |
   | Negative Example 2 -                          |                                                 |
   | Input: The wild population in China decreased |                                                 |
   | to around 2,000 in 2005.                      |                                                 |
   | Output: By 2005, the wild population          |                                                 |
   | decreased to about 2,000.                     |                                                 |
   |                                               |                                                 |
   | Now complete the following example -          |                                                 |
   | Input: Merton College is one of the colleges  |                                                 |
   | of the University of Oxford .                 |                                                 |
   | Output:                                       |                                                 |
   +-----------------------------------------------+-------------------------------------------------+
   ```

## 建立基準模型

在 Gemini 模型上建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式，建立遠端模型：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.gemini_baseline`
   REMOTE WITH CONNECTION DEFAULT
   OPTIONS (ENDPOINT = 'gemini-2.5-pro');
   ```

   查詢會在幾秒內完成，接著 `gemini_baseline` 模型會顯示在「Explorer」窗格的 `bqml_tutorial` 資料集中。由於查詢使用 `CREATE MODEL` 陳述式建立模型，因此沒有查詢結果。

## 查看基準模型效能

如要查看遠端模型在未經調整的情況下，對評估資料的成效，請執行 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)：

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

   結果大致如下：

   ```
   +-------------------------------------------------+-------------------------------------------------+
   | result                                          | ground_truth                                    |
   +-------------------------------------------------+-------------------------------------------------+
   | In mathematics, and more specifically in graph  | In mathematics , and more specifically in graph |
   | theory, a graph is an abstract structure that   | theory , a graph is a structure amounting to a  |
   | is used to model pairwise relationships between | set of objects in which some pairs of the       |
   | objects. A graph in this context is made up of  | objects are in some sense " related " .         |
   | vertices (also called nodes or points) and      |                                                 |
   | edges (also called links or lines) that connect |                                                 |
   | pairs of vertices.                              |                                                 |
   | ...                                             | ...                                             |
   +-------------------------------------------------+-------------------------------------------------+
   ```

   雖然基準模型生成的文字能準確反映基準真相內容中提供的事實，但文字風格有時會有所不同。基準模型產生的詳細說明，往往比所需的基準真相更長。

## 評估基準模型

如要更詳細地評估模型效能，請使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)。這項函式會計算模型指標，評估生成的文字的準確度和品質，以便比較模型回覆與理想回覆。

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

   結果大致如下：

   ```
   +---------------------+---------------------+-------------------------------------------+--------------------------------------------+
   | bleu4_score         | rouge-l_precision   | rouge-l_recall      | rouge-l_f1_score    | evaluation_status                          |
   +---------------------+---------------------+---------------------+---------------------+--------------------------------------------+
   | 0.32571814014498979 | 0.45752569962901607 | 0.557224161991254   | 0.49205029983307907 | {                                          |
   |                     |                     |                     |                     |  "num_successful_rows": 176,               |
   |                     |                     |                     |                     |  "num_total_rows": 176                     |
   |                     |                     |                     |                     | }                                          |
   +---------------------+---------------------+ --------------------+---------------------+--------------------------------------------+
   ```

這些分數可量化評估成效。接下來幾節將說明如何建立調整後的模型，並與基準模型比較效能。

## 建立調整後模型

建立遠端模型，與您在「[建立模型](#create_a_baseline_model)」中建立的模型非常相似，但這次請指定 [`AS SELECT` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw#as_select)，提供訓練資料來調整模型。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式，建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw)：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.gemini_tuned`
     REMOTE
       WITH CONNECTION DEFAULT
     OPTIONS (
       endpoint = 'gemini-2.5-pro',
       max_iterations = 500,
       data_split_method = 'no_split')
   AS
   SELECT
     input AS prompt, output AS label
   FROM `bqml_tutorial.wiki_auto_style_transfer_train`;
   ```

   查詢應該會在幾分鐘內完成，完成後，`gemini_tuned` 模型會顯示在「Explorer」窗格的 `bqml_tutorial` 資料集中。由於查詢使用 `CREATE MODEL` 陳述式建立模型，因此不會產生查詢結果。

## 檢查調整後模型的效能

如要查看調整後的模型在評估資料上的成效，請執行 `AI.GENERATE_TEXT` 函式：

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

   調整後的模型生成的文字，在風格上與基準真相內容更相似。

## 評估調整後的模型

如要比較調整後模型的回覆與理想回覆，請使用 `ML.EVALUATE` 函式：

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

   結果大致如下：

   ```
   +---------------------+---------------------+-------------------------------------------+--------------------------------------------+
   | bleu4_score         | rouge-l_precision   | rouge-l_recall      | rouge-l_f1_score    | evaluation_status                          |
   +---------------------+---------------------+---------------------+---------------------+--------------------------------------------+
   | 0.44878025403825506 | 0.57236062510796448 | 0.638794269320597   | 0.59591519400141835 | {                                          |
   |                     |                     |                     |                     |  "num_successful_rows": 176,               |
   |                     |                     |                     |                     |  "num_total_rows": 176                     |
   |                     |                     |                     |                     | }                                          |
   +---------------------+---------------------+ --------------------+---------------------+--------------------------------------------+
   ```

調整後的模型效能顯著提升，在所有評估指標上都優於基準模型。

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

**警告**：刪除專案會出現以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

刪除 Google Cloud 專案：

```
gcloud projects delete PROJECT_ID
```

### 刪除個別資源

如要重複使用專案，請刪除您為本教學課程建立的資源。

1. 前往「BigQuery」頁面

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 刪除 `bqml_tutorial` 資料集。刪除資料集也會一併刪除模型和資料表。

   1. 在「Explorer」窗格中展開專案，然後點選「資料集」。
   2. 在「Datasets」(資料集) 清單中，點選 `bqml_tutorial` 資料集。
   3. 在詳細資料窗格中，按一下「delete 刪除」。
   4. 在「Delete dataset」(刪除資料集) 對話方塊中，按一下「Delete」(刪除)。

## 後續步驟

* 進一步瞭解 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)。
* 進一步瞭解 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)。
* 查看遠端模型的[監督式調整選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw#supervised_tuning)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-03 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-03 (世界標準時間)。"],[],[]]