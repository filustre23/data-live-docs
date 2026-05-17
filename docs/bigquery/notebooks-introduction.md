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

本文將簡介 BigQuery 中的 [Colab Enterprise 筆記本](https://docs.cloud.google.com/colab/docs/introduction?hl=zh-tw)。您可以使用筆記本，透過 SQL、Python 和其他常見的套件和 API，完成分析和機器學習 (ML) 工作流程。筆記本提供下列選項，可提升協作和管理效率：

* 使用 Identity and Access Management (IAM)，與特定使用者和群組共用筆記本。
* 查看筆記本版本記錄。
* 還原或從筆記本的先前版本建立分支。

筆記本是 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 程式碼資產，由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 提供技術支援。[儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw)也是程式碼資產。
所有程式碼資產都會儲存在預設[區域](#supported_regions)。更新預設區域後，之後建立的所有程式碼資產都會使用新的區域。

記事本功能僅適用於 Google Cloud 控制台。

## 優點

BigQuery 中的 Notebook 具有下列優點：

* [BigQuery DataFrames](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw) 已整合至筆記本，無須設定。BigQuery DataFrames 是 Python API，可讓您使用 [pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) 和 [scikit-learn](https://scikit-learn.org/stable/modules/classes.html) API，大規模分析 BigQuery 資料。
* 採用 [Gemini 生成式 AI](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw) 技術輔助開發程式碼。
* 自動完成 SQL 陳述式，與 BigQuery 編輯器相同。
* 可儲存、共用及管理筆記本版本。
* 您可以在工作流程的任何時間點，使用 [matplotlib](https://matplotlib.org/)、
  [seaborn](https://seaborn.pydata.org/) 和其他熱門程式庫將資料視覺化。
* 您可以在儲存格中編寫及[執行 SQL](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#cells)，並參照筆記本中的 Python 變數。
* 支援匯總和自訂功能的互動式 [DataFrame 視覺化](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#cells)。

## 筆記本庫

筆記本庫是探索及使用預先建構筆記本範本的中心。這些範本可讓您執行資料準備、資料分析和視覺化等常見工作。筆記本範本也有助於探索 BigQuery Studio 功能、管理工作流程，以及推廣最佳做法。

您可以使用筆記本範本庫，簡化資料生命週期各階段的意圖到洞察工作流程，包括擷取和探索資料，以及進階分析和 BigQuery ML。

筆記本庫提供各種技能程度適用的範本。這個範本庫提供 SQL、Python、Apache Spark 和 DataFrame 的基本範本。您也可以探索 BigQuery 中的生成式 AI 和多模態資料分析等主題。

如要開始使用筆記本庫，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 BigQuery Studio 首頁，按一下「查看筆記本庫」。

如要進一步瞭解如何使用筆記本庫範本，請參閱「[使用筆記本庫建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#create-notebook-console)」。

## 執行階段管理

BigQuery 會使用 [Colab Enterprise 執行階段](https://docs.cloud.google.com/colab/docs/create-runtime?hl=zh-tw)執行筆記本。

筆記本執行階段是分配給特定使用者的 Compute Engine 虛擬機器，可讓使用者在筆記本中執行程式碼。多個筆記本可以共用同一個執行階段。不過，每個執行階段只屬於一位使用者，其他人無法使用。筆記本執行階段是根據範本建立，通常由具備管理員權限的使用者定義。您隨時可以改用其他範本類型的執行階段。

## 筆記本安全性

您可以使用 Identity and Access Management (IAM) 角色控管筆記本存取權。詳情請參閱「[授予筆記本存取權](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#grant_access_to_notebooks)」一文。

如要偵測筆記本中使用的 Python 套件是否有安全漏洞，請安裝並使用 [Notebook Security Scanner](https://docs.cloud.google.com/security-command-center/docs/enable-notebook-security-scanner?hl=zh-tw) ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

## 支援的地區

BigQuery Studio 可讓您儲存、共用及管理筆記本版本。下表列出 BigQuery Studio 的適用地區：

|  | 地區說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- | --- |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` |  |
| **美洲** | | | |
|  | 哥倫布 | `us-east5` |  |
|  | 達拉斯 | `us-south1` |  |
|  | 愛荷華州 | `us-central1` |  |
|  | 洛杉磯 | `us-west2` |  |
|  | 拉斯維加斯 | `us-west4` |  |
|  | 蒙特婁 | `northamerica-northeast1` |  |
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
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 杜林 | `europe-west12` |  |
|  | 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **中東地區** | | | |
|  | 杜哈 | `me-central1` |  |
|  | 達曼 | `me-central2` |  |

## 定價

如要瞭解 BigQuery Studio 筆記本的價格資訊，請參閱「[筆記本執行階段價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#external_services)」。

## 監控運算單元用量

如要監控 BigQuery Studio 筆記本的時段用量，請在 Google Cloud 控制台中查看 [Cloud Billing 報表](https://docs.cloud.google.com/billing/docs/reports?hl=zh-tw)。在 Cloud Billing 帳單報表中，套用標籤為 **goog-bq-feature-type** 且值為 **BQ\_STUDIO\_NOTEBOOK** 的篩選條件，即可查看 BigQuery Studio 筆記本的運算單元用量和費用。

## 疑難排解

詳情請參閱「[排解 Colab Enterprise 問題](https://docs.cloud.google.com/colab/docs/troubleshooting?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。
* 瞭解如何[管理記事本](https://docs.cloud.google.com/bigquery/docs/manage-notebooks?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]