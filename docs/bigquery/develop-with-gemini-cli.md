Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Gemini CLI 分析資料

搭配使用 [Gemini CLI](https://docs.cloud.google.com/gemini/docs/codeassist/gemini-cli?hl=zh-tw) 和專屬 BigQuery [擴充功能](#about-bigquery-extensions)，即可在終端機中使用自然語言提示與資料互動。直接在指令列使用 AI 輔助功能，即可分析個人和公開資料表，並擷取洞察資訊，不必切換至其他環境。

這些第一方擴充功能提供一些常見的資料分析和洞察工具。如要自行建構工具，請參閱「[搭配使用 BigQuery 與 MCP、Gemini CLI 和其他代理](https://docs.cloud.google.com/bigquery/docs/pre-built-tools-with-mcp-toolbox?hl=zh-tw)」。

## 關於 Gemini CLI 和擴充功能

Gemini CLI 是 Google 的開放原始碼對話式 AI 代理，可加速開發工作流程，並協助編寫程式碼、偵錯、探索資料和創作內容。這項服務提供代理驅動體驗，可與 Data Cloud 服務 (例如 BigQuery) 和其他熱門 Google Cloud 資料庫及開放原始碼資料庫互動。

如要進一步瞭解 Gemini CLI，請參閱 [Gemini CLI 說明文件](https://github.com/google-gemini/gemini-cli/blob/main/README.md)。

### 擴充功能的運作方式

擴充功能可拓展 Gemini CLI 的能力，讓其連結及控制特定 Google Cloud 服務和其他工具。擴充功能可讓 Gemini 瞭解脈絡和 API，進而進行對話式互動。您可以從 GitHub 網址、本機目錄或註冊資料庫載入擴充功能。這些擴充功能提供工具、斜線指令和提示。這些與 IDE 擴充功能 (例如 Gemini Code Assist) 不同，後者是使用 MCP Toolbox 整合。

## 關於 BigQuery 擴充功能

BigQuery 提供下列擴充功能，可透過 Gemini CLI 處理 BigQuery 資料：

BigQuery 資料分析擴充功能
:   使用這項擴充功能，即可探索資料、進一步瞭解 BigQuery 資料表和資料集，以及用自然語言提出有關資料集的問題。您也可以使用內建的進階工具生成預測結果，或執行貢獻分析。這項擴充功能中的工具可協助 Gemini CLI 根據您的自然語言問題編寫 SQL 查詢，然後執行查詢來提供問題答案。

BigQuery 對話式數據分析擴充功能
:   使用這項擴充功能，即可透過預先託管的伺服器端數據分析代理，從 BigQuery 資料取得進階深入分析。這項擴充功能中的工具可協助 Gemini CLI 將自然語言問題傳送至內建的託管代理，並根據資料提供更深入的洞察。

### BigQuery 資料分析工具

[BigQuery 資料分析擴充功能](https://github.com/gemini-cli-extensions/bigquery-data-analytics)提供下列工具：

| 類別 | 工具 | 自然語言提示詞範例 |
| --- | --- | --- |
| 資料集和資料表資訊 | `get_dataset_info` | 取得資料集 bigquery-public-data.pypi 的資訊 |
| `get_table_info` | 取得資料表 bigquery-public-data.pypi.file\_downloads 的資訊 |
| `list_dataset_ids` | 列出 bigquery-public-data 專案中的所有機器學習資料集 |
| `list_table_ids` | 列出資料集 bigquery-public-data.pypi 中的所有資料表 |
| 搜尋 | `search_catalog` | 尋找與 PyPi 下載相關的資料表 |
| SQL 執行 | `execute_sql` | 使用 bigquery-public-data.pypi.file\_downloads，顯示本月下載次數最多的前 10 個 pypi 套件 |
| 時間序列預測 | `forecast` | 使用 bigquery-public-data.pypi.file\_downloads，預測 urllib3 套件在 2025 年最後四個月的下載量 |
| 貢獻分析 | `analyze_contribution` | 分析 bigquery-public-data.google\_analytics\_sample.ga\_sessions\_20170801 資料表中，國家/地區對收益的貢獻 |

### 對話式數據分析工具

[對話式數據分析擴充功能](https://github.com/gemini-cli-extensions/bigquery-conversational-analytics)提供下列工具：

| 類別 | 工具 | 自然語言提示詞範例 |
| --- | --- | --- |
| 搜尋 | `search_catalog` | 尋找與 PyPi 下載相關的資料表 |
| 對話式數據分析 | `ask_data_insights` | 使用 ask\_data\_insights 工具和 bigquery-public-data.google\_analytics\_sample 下的資料表，告訴我應該著重哪些管道，以及原因 |

## 事前準備

開始前，請先備妥下列項目：

* 至少一個 Google Cloud 專案的存取權。
* 如要使用資料分析擴充功能，請啟用下列 API：

  + BigQuery
  + 如要使用 `search_catalog` 工具：Knowledge Catalog
* 如要使用對話式數據分析擴充功能，請啟用下列 API：

  + BigQuery
  + Knowledge Catalog
  + 如要使用 `ask_data_insights` 工具，請啟用 Gemini for Google Cloud API、Gemini 和 Data Analytics API with Gemini

### 必要的角色

如要取得透過 Gemini CLI 使用 BigQuery 擴充功能所需的權限，請要求管理員授予您 Resource Manager 資源 (專案、資料夾和組織) 或較低層級資源 (例如資料集) 的下列 IAM 角色：

* 在 Google Cloud 專案中執行 BigQuery 查詢：[BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user) (`roles/bigquery.user`)
* 使用基礎中繼資料工具取得 BigQuery 資料集和資料表中繼資料：[BigQuery 中繼資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.metadataViewer) (`roles/bigquery.metadataViewer`)
* 使用對話式數據分析擴充功能：[Gemini for Google Cloud 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/cloudaicompanion?hl=zh-tw#cloudaicompanion.user) (`roles/cloudaicompanion.user`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 安裝 BigQuery 擴充功能

安裝 BigQuery 擴充功能，然後使用這些功能探索及分析資料。

1. [安裝 Gemini CLI](https://github.com/google-gemini/gemini-cli?tab=readme-ov-file#quickstart)。
2. 設定環境變數，連線至 BigQuery 專案：

   ```
   export BIGQUERY_PROJECT="PROJECT_ID"
   ```

   將 `PROJECT_ID` 替換為您的 Google Cloud專案 ID。

   您也可以設定下列選用環境變數：

   * `BIGQUERY_LOCATION`：資料集位置，例如 `export
     BIGQUERY_LOCATION="us"`
   * `BIGQUERY_USE_CLIENT_OAUTH`：是否使用用戶端 OAuth，例如：`export BIGQUERY_USE_CLIENT_OAUTH=true`
3. 使用 `gemini extension install` 指令安裝 BigQuery 資料分析或對話式數據分析擴充功能：

   * 選用：安裝 BigQuery 資料分析擴充功能：

     ```
     gemini extensions install https://github.com/gemini-cli-extensions/bigquery-data-analytics
     ```
   * 選用：安裝 BigQuery 對話式數據分析擴充功能：

     ```
     gemini extensions install https://github.com/gemini-cli-extensions/bigquery-conversational-analytics
     ```
4. 以互動模式啟動 Gemini CLI，探索及分析資料：

   ```
   gemini
   ```

   CLI 會自動載入 BigQuery 擴充功能和相關工具，方便您與資料互動。

**注意：**如果同時安裝兩個 BigQuery 擴充功能，Gemini CLI 可能會使用任一擴充功能的工具來回答問題。這可能會影響計費，因為使用對話式數據分析工具會產生額外費用。詳情請參閱[定價](#pricing)。

## 探索及分析資料的提示詞範例

在 Gemini CLI 輸入提示詞。您可以參考下列範例。

### 探索及分析資料表

下列提示範例可讓您探索及分析資料表。

* **提示詞範例**：尋找與 PyPi 下載相關的資料表

  ```
  Find tables related to PyPi downloads
  ```

  **回應範例**

  Gemini CLI 會傳回相關資料表清單：

  ```
  ✦ I found the following tables related to PyPi downloads:

      *   file_downloads: projects/bigquery-public-data/datasets/pypi/tables/file_downloads
      *   distribution_metadata: projects/bigquery-public-data/datasets/pypi/tables/distribution_metadata
  ```
* **提示範例**：顯示本月下載次數前十名的 PyPI 套件：

  ```
  Using bigquery-public-data.pypi.file_downloads, show me the top 10
  downloaded pypi packages this month
  ```

  **回應範例**

  Gemini CLI 會傳回前 10 個套件：

  ```
  ✦ Here are the top 10 most downloaded PyPI packages this month:

      1.  boto3: 685,007,866 downloads
      2.  botocore: 531,034,851 downloads
      3.  urllib3: 512,611,825 downloads
      4.  requests: 464,595,806 downloads
      5.  typing-extensions: 459,505,780 downloads
      6.  certifi: 451,929,759 downloads
      7.  charset-normalizer: 428,716,731 downloads
      8.  idna: 409,262,986 downloads
      9.  grpcio-status: 402,535,938 downloads
      10. aiobotocore: 399,650,559 downloads
  ```

### 使用 `ask_data_insights` 工具取得更深入的洞察資訊

`ask_data_insights` 工具會觸發 BigQuery Conversational Analytics API 上的代理，回答您的問題。伺服器端代理會收集資料的其他背景資訊，並提供更多深入分析。

* **提示詞範例**：取得洞察資料，瞭解應著重哪些管道

  ```
  Using ask_data_insights and using the tables under
  bigquery-public-data.google_analytics_sample, tell me the channels I should
  focus on and why
  ```

  **回應範例**

  Gemini CLI 會根據分析結果傳回建議：

  ```
  Based on the analysis of the Google Analytics sample data, here are the
  channels you should focus on and why:

  |     Channel      | Total Visits | Total Pageviews | Total Transactions | Total Revenue |
  | ---------------- | ------------ | --------------- | ------------------ | ------------- |
  | Referral         |      104,838 |         707,597 |              5,543 |   $651,429.91 |
  | Direct           |      143,026 |         584,840 |              2,219 |   $434,840.55 |
  | Organic Search   |      381,561 |       1,569,218 |              3,581 |   $326,380.51 |
  | Display          |        6,262 |          34,202 |                152 |    $78,337.46 |
  | Paid Search      |       25,326 |         136,060 |                479 |    $43,558.90 |
  | Social           |      226,117 |         398,690 |                131 |     $4,916.54 |
  | Affiliates       |       16,403 |          47,417 |                  9 |       $597.38 |
  | (Other)          |          120 |             442 |                  1 |         $9.99 |

    Recommendations:

      1.  Prioritize referral traffic:
          *   Why: This is a highly valuable channel. It brings in the most
              revenue and has a high number of transactions, despite not
              having the highest number of visits. This indicates that
              traffic from referrals is highly qualified and converts
              well.
          *   Action: Identify your top referring websites and build
              stronger relationships with them. Look for similar websites
              to partner with.

      2.  Nurture your direct traffic:
          *   Why: Direct traffic is your second-highest revenue source.
              These are likely returning customers or people who know your
              brand well.
  ```

### 定價

使用中繼資料工具 (例如 `get_dataset_info`、`get_table_info`、`list_dataset_ids` 和 `list_table_ids`) 或 `search_catalog` 工具，不需額外付費。

執行查詢的工具 (包括 `execute_sql`、`forecast` 和 `analyze_contribution`) 會根據專案設定，按照 [BigQuery 隨選定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)或 [BigQuery 容量定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)計費。

在 Beta 版 (v1.0 之前) 期間，`ask_data_insights` 工具不需額外付費，但這項工具觸發的任何 BigQuery 查詢，都會按照標準 BigQuery 定價計費。

## 後續步驟

* 進一步瞭解如何[搭配使用 BigQuery 與 MCP、Gemini CLI 和其他代理](https://docs.cloud.google.com/bigquery/docs/pre-built-tools-with-mcp-toolbox?hl=zh-tw)。
* 進一步瞭解 [Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-overview?hl=zh-tw)。
* 請參閱 GitHub 上的[資料分析擴充功能](https://github.com/gemini-cli-extensions/bigquery-data-analytics)。
* 請參閱 GitHub 上的[對話式數據分析擴充功能](https://github.com/gemini-cli-extensions/bigquery-conversational-analytics)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-03 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-03 (世界標準時間)。"],[],[]]