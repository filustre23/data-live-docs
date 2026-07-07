Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 筆記本簡介

您可以在 BigQuery 中使用 [Colab Enterprise 筆記本](https://docs.cloud.google.com/colab/docs/introduction?hl=zh-tw)，在單一整合式介面中執行端對端資料科學和機器學習工作流程。與標準 SQL 編輯器不同，筆記本可讓您結合 SQL 查詢、Python 程式碼、RTF 和視覺化內容，以資料呈現完整的故事。筆記本非常適合下列用途：

* **端對端機器學習工作流程**：在單一筆記本介面中建構、評估及部署 BigQuery ML 模型。
* **資料探索**：使用 BigQuery DataFrames 清理及分析大型資料集。
* **協同研究**：使用 IAM 與同事共用筆記本，並追蹤版本記錄。

筆記本是 BigQuery Studio 中的程式碼資產，與已儲存的查詢並列，並由 Dataform 提供支援。這些功能僅適用於 Google Cloud 控制台。

## 優點

BigQuery 中的 Notebook 具有下列優點：

* **與 Python 完美整合**：使用 BigQuery DataFrames API 時，不必進行任何額外設定。
* **AI 輔助開發**：使用 [Gemini 生成式 AI](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw) 輔助開發程式碼。
* **熟悉的編輯器功能**：使用 SQL 自動完成功能，與 BigQuery SQL 編輯器類似。
* **整合式視覺化**：使用互動式 [DataFrame 視覺化](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#cells)，或 [matplotlib](https://matplotlib.org/) 和 [seaborn](https://seaborn.pydata.org/) 等程式庫，直接在工作流程中將資料視覺化。
* **SQL-Python 互通性**：在參照 Python 變數的儲存格中[執行 SQL](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#cells)。

## 筆記本庫

筆記本庫是中心樞紐，可供探索及使用預先建構的筆記本範本。這些範本可讓您執行資料準備、資料分析和視覺化等常見工作。筆記本範本也有助於探索 BigQuery Studio 功能、管理工作流程，以及推廣最佳做法。

您可以使用筆記本範本庫，簡化整個意圖到洞察工作流程，包括資料生命週期的各個階段，從擷取和探索到進階分析和 BigQuery ML。

筆記本庫提供各種技能程度適用的範本。範本庫包含 SQL、Python、Apache Spark 和 DataFrame 的基本範本。您也可以探索 BigQuery 中的生成式 AI 和多模態資料分析等主題。

如要開始使用筆記本庫，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「Explorer」選單中的「Notebooks」。
3. 按一下「新記事本」下拉式選單，然後選取「所有範本」。

如要進一步瞭解如何使用筆記本範本庫中的範本，請參閱「[使用筆記本範本庫建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#create-notebook-console)」。

## 執行階段管理

BigQuery 會使用 [Colab Enterprise 執行階段](https://docs.cloud.google.com/colab/docs/create-runtime?hl=zh-tw)執行筆記本。

筆記本執行階段是分配給特定使用者的 Compute Engine 虛擬機器，可讓使用者在筆記本中執行程式碼。多個筆記本可以共用同一個執行階段。不過，每個執行階段都只屬於一位使用者，其他人無法使用。筆記本執行階段是根據範本建立，通常由具備管理員權限的使用者定義。您隨時可以改用不同範本類型的執行階段。

## 筆記本安全性

您可以使用 Identity and Access Management (IAM) 角色控管筆記本存取權。詳情請參閱「[授予筆記本存取權](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#grant_access_to_notebooks)」和「[筆記本的安全性考量](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#notebooks-security)」。

如要偵測筆記本中使用的 Python 套件是否有安全漏洞，請安裝並使用 [Notebook Security Scanner](https://docs.cloud.google.com/security-command-center/docs/enable-notebook-security-scanner?hl=zh-tw) ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

## 支援的地區

BigQuery Studio 可讓您儲存、共用及管理筆記本版本。下表列出 BigQuery Studio 的適用地區：

|  | 區域說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- | --- |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` |  |
| **美洲** | | | |
|  | 哥倫布 | `us-east5` |  |
|  | 達拉斯 | `us-south1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 洛杉磯 | `us-west2` |  |
|  | 拉斯維加斯 | `us-west4` |  |
|  | 蒙特婁 | `northamerica-northeast1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 北維吉尼亞州 | `us-east4` |  |
|  | 俄勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 南卡羅來納州 | `us-east1` |  |
| **亞太地區** | | | |
|  | 香港 | `asia-east2` |  |
|  | 雅加達 | `asia-southeast2` |  |
|  | 孟買 | `asia-south1` |  |
|  | 首爾 | `asia-northeast3` |  |
|  | 新加坡 | `asia-southeast1` |  |
|  | 雪梨 | `australia-southeast1` |  |
|  | 台灣 | `asia-east1` |  |
|  | 東京 | `asia-northeast1` |  |
| **歐洲** | | | |
|  | 比利時 | `europe-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 芬蘭 | `europe-north1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 米蘭 | `europe-west8` |  |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 杜林 | `europe-west12` |  |
|  | 華沙 | `europe-central2` |  |
|  | 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **中東地區** | | | |
|  | 達曼 | `me-central2` |  |
|  | 杜哈 | `me-central1` |  |
|  | 特拉維夫市 | `me-west1` |  |

**注意：** 所有程式碼資產都會儲存在預設區域。更新預設區域後，之後建立的所有程式碼資產都會使用新的區域。

## 定價

如要瞭解 BigQuery Studio 筆記本的價格資訊，請參閱「[筆記本執行階段價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#external_services)」。

## 監控運算單元用量

如要監控 BigQuery Studio 筆記本的配額用量，請在 Google Cloud 控制台中查看 [Cloud Billing 報表](https://docs.cloud.google.com/billing/docs/reports?hl=zh-tw)。在 Cloud Billing 帳單報表中，套用標籤為 **goog-bq-feature-type** 且值為 **BQ\_STUDIO\_NOTEBOOK** 的篩選條件，即可查看 BigQuery Studio 筆記本的運算單元用量和費用。

## 疑難排解

詳情請參閱「[排解 Colab Enterprise 問題](https://docs.cloud.google.com/colab/docs/troubleshooting?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。
* 瞭解如何[管理記事本](https://docs.cloud.google.com/bigquery/docs/manage-notebooks?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-07-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-07-05 (世界標準時間)。"],[],[]]