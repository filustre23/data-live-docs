Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從其他 Google 和 Google Cloud 服務載入資料

許多 Google 和 Google Cloud 服務都可讓您直接將作業、數據分析和帳單資料匯出至 BigQuery。匯出資料後，您可以彙整各項服務的記錄、執行 SQL 查詢，以及建立自訂報表。視來源服務而定，您可以從該服務的控制台或 API 啟動即時或排定的批次匯出作業。

如要直接在外部資料庫、Google 雲端硬碟或 Google 試算表中查詢資料，而不匯出資料，請參閱「[外部資料來源](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)」。如需本文件未列出的服務，或想直接從 BigQuery 建立載入工作和查詢，請參閱「[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」。

## 支援資料匯出的雲端服務

### 碳足跡

[碳足跡](https://docs.cloud.google.com/carbon-footprint?hl=zh-tw)匯出功能會擷取所選帳單帳戶使用涵蓋 Google Cloud 服務時，產生的預估溫室氣體排放總量。

您可以將碳足跡資料匯出至 BigQuery，以便執行資料分析，或建立自訂資訊主頁和報表。

如要設定匯出碳足跡資料，請參閱「[匯出碳足跡資料](https://docs.cloud.google.com/carbon-footprint/docs/export?hl=zh-tw)」。

### Google Security Operations

您可以將 [Google Security Operations](https://chronicle.security) 安全性記錄匯出至 BigQuery，以便進行其他資料彙整和分析。

如要設定匯出 Google Security Operations 安全性記錄，請與 [Google Security Operations 支援團隊](https://docs.cloud.google.com/chronicle/docs/getting-support?hl=zh-tw)聯絡。

### Cloud Asset Inventory

[Cloud Asset Inventory](https://docs.cloud.google.com/asset-inventory?hl=zh-tw) 可讓您將組織、資料夾或專案的資產中繼資料匯出至 BigQuery 資料表，然後對資產清單執行資料分析。

如要設定匯出 Cloud Asset Inventory 資料，請參閱「[匯出至 BigQuery](https://docs.cloud.google.com/asset-inventory/docs/exporting-to-bigquery?hl=zh-tw)」。

### Cloud Billing

[Cloud Billing](https://docs.cloud.google.com/billing?hl=zh-tw) 匯出至 BigQuery 功能可讓您全天自動匯出詳細的Google Cloud 帳單資料 (例如用量、預估費用和定價資料)。

**時機很重要。**為確保您能存取更全面的帳單資料，滿足分析需求，建議您在建立 Cloud Billing 帳戶時，一併啟用將 Cloud Billing 資料匯出至 BigQuery 的功能。

如要設定匯出 Cloud Billing 資料，請參閱「[將 Cloud Billing 資料匯出至 BigQuery](https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=zh-tw)」。

### Cloud Logging

您可以將 [Cloud Logging](https://docs.cloud.google.com/logging?hl=zh-tw) 的記錄檔轉送至 BigQuery 資料表，以便進行其他分析和彙整。如果是 Google Cloud 服務，記錄資料產生後約 1 分鐘即可查詢。

如要將 BigQuery 做為 Observability Analytics 的一部分，請參閱「[Observability Analytics](https://docs.cloud.google.com/logging/docs/analyze/query-and-view?hl=zh-tw)」。

如要設定匯出 Cloud Logging 資料，請參閱「[將記錄轉送至支援的接收器](https://docs.cloud.google.com/logging/docs/export/configure_export_v2?hl=zh-tw)」。

### Customer Experience Insights

[CX Insights](https://docs.cloud.google.com/solutions/ccai-insights?hl=zh-tw) 可讓您將 CX Insights 對話和分析資料匯出至 BigQuery，以便執行原始查詢。

如要設定 CX Insights 資料匯出作業，請參閱「[將對話匯出至 BigQuery](https://docs.cloud.google.com/contact-center/insights/docs/export?hl=zh-tw)」。

### Dialogflow CX

[Dialogflow CX](https://docs.cloud.google.com/dialogflow?hl=zh-tw) 會生成虛擬服務專員與客戶之間的對話記錄。

如要設定從 Dialogflow CX 匯出對話，請參閱「[將互動記錄匯出至 BigQuery](https://docs.cloud.google.com/dialogflow/cx/docs/concept/export-bq?hl=zh-tw)」。

### Firebase

[Firebase](https://firebase.google.com/?hl=zh-tw) 包含多項可傳送至 BigQuery 的 Analytics 匯出資料。包括：

* 數據分析
* 雲端通訊
* Crashlytics
* Performance Monitoring
* A/B 測試
* 遠端設定個人化

如要設定匯出 Firebase 資料，請參閱「[將專案資料匯出至 BigQuery](https://firebase.google.com/docs/projects/bigquery-export?hl=zh-tw)」。

### Google Analytics 4

如要瞭解如何將工作階段資料從 [Google Analytics 4](https://developers.google.com/analytics/devguides/collection/ga4?hl=zh-tw) 報表資料檢視匯出至 BigQuery，請參閱 Analytics 說明中心的「[BigQuery Export](https://support.google.com/analytics/answer/9358801?hl=zh-tw)」和「[設定 BigQuery Export](https://support.google.com/analytics/answer/3416092?hl=zh-tw)」兩篇文章。Google Analytics 4 資料匯入 BigQuery 後，您可以使用 GoogleSQL 查詢。

如果 Google Analytics 4 匯出作業發生錯誤，請參閱「[連結失敗的原因](https://support.google.com/analytics/answer/9823238?hl=zh-tw#reasons&zippy=,in-this-article)」或「[匯出失敗的原因](https://support.google.com/analytics/answer/9823238?hl=zh-tw#export&zippy=,in-this-article)」。

如果 Google Analytics 4 匯出資料延遲、匯出後缺少 Google Analytics 4 資料，或遇到其他問題，請與 [Analytics 支援團隊](https://support.google.com/analytics/?hl=zh-tw)聯絡。

如有 BigQuery 的相關問題 (例如帳單)，請洽詢 [Google Cloud 支援團隊](https://cloud.google.com/support/?hl=zh-tw)。

### Google Analytics 360

如要瞭解如何將工作階段資料從 [Google Analytics 360](https://marketingplatform.google.com/about/analytics-360/?hl=zh-tw) 報表資料檢視匯出至 BigQuery，請參閱 Analytics 說明中心的「[BigQuery Export](https://support.google.com/analytics/topic/3416089?hl=zh-tw)」一文。Google Analytics 360 資料匯入 BigQuery 後，您可以使用 GoogleSQL 查詢資料。

如需在 BigQuery 中查詢 Analytics 資料的範例，請參閱 Analytics 說明中的「[BigQuery 指南](https://support.google.com/analytics/answer/4419694?hl=zh-tw)」。

如果問題與連結 BigQuery 和 Google Analytics 360、匯出後缺少 Google Analytics 360 資料，或從 Google Analytics 360 匯出時資料延遲有關，請與 [Google Analytics 360 支援團隊](https://support.google.com/analytics/answer/9026876?hl=zh-tw)聯絡。

如有 BigQuery 的相關問題 (例如帳單)，請洽詢 [Google Cloud 支援團隊](https://cloud.google.com/support/?hl=zh-tw)。

### Google Search Console 資料

您可以排定每天將 [Google Search](https://www.google.com/search/about/?hl=zh-tw) Console 成效資料匯出至 BigQuery，以便對資料執行複雜的查詢。

如要設定資料匯出作業，請參閱「[關於匯出 Search Console 大量資料至 BigQuery](https://support.google.com/webmasters/answer/12918484?hl=zh-tw)」。

### 建議工具

您可以使用 BigQuery 資料移轉服務，安排每日[建議](https://docs.cloud.google.com/recommender/docs/whatis-activeassist?hl=zh-tw)快照。建議會提供 Google Cloud 產品和資源使用最佳化建議，以及資源使用模式的深入分析。

如要使用 BigQuery 資料移轉服務設定資料快照，請參閱「[將建議匯出至 BigQuery](https://docs.cloud.google.com/recommender/docs/bq-export/export-recommendations-to-bq?hl=zh-tw)」。

### Gemini Enterprise Agent Platform 批次預測

[Gemini Enterprise Agent Platform](https://docs.cloud.google.com/vertex-ai?hl=zh-tw) 批次預測會根據模型的輸入內容，建立一組預測結果。您可以將這些結果儲存在 BigQuery，以便進行其他分析和彙整。

如要設定批次預測結果的匯出作業，請參閱「[取得批次預測結果和說明](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/tabular-data/classification-regression/get-batch-predictions?hl=zh-tw#make-batch-inference-request)」。

### Gemini Enterprise Agent Platform 預測

您可以使用 Gemini Enterprise Agent Platform Predictions，將線上端點的預測結果儲存在 BigQuery，以便進一步分析。

如要設定模型預測與 BigQuery 的整合，請參閱「[線上預測記錄](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/predictions/online-prediction-logging?hl=zh-tw#enabling-and-disabling)」。

## 後續步驟

* 瞭解如何使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，在 BigQuery 中啟動其他整合。
* 瞭解如何連結至其他[外部資料來源](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]