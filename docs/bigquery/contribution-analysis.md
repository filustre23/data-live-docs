Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 貢獻分析總覽

請參閱本文，瞭解貢獻度分析的用途，以及在 BigQuery ML 中執行貢獻度分析的選項。

## 什麼是貢獻分析？

貢獻度分析 (又稱主要驅動因素分析) 是一種方法，可產生多維度資料中主要指標變更的洞察資料。舉例來說，您可以透過貢獻度分析，瞭解哪些資料導致兩個季度的收益數字出現變化，或是比較兩組訓練資料，瞭解機器學習模型效能的變化。

貢獻度分析是[強化分析](https://en.wikipedia.org/wiki/Augmented_Analytics)的一種形式，也就是運用人工智慧 (AI) 強化及自動化資料分析和解讀作業。貢獻分析可達成擴增分析的主要目標之一，也就是協助使用者找出資料中的模式。

## 使用 BigQuery ML 進行貢獻度分析

貢獻度分析會比較測試集和控制資料集，偵測特定指標出現變化的資料區隔。舉例來說，您可以將 2023 年底的銷售資料表快照做為測試資料，並將 2022 年底的銷售資料表快照做為控制資料，然後比較兩者，瞭解銷售額隨時間的變化。貢獻度分析可顯示哪些資料區隔 (例如特定區域的線上顧客) 帶動銷售額在一年內出現最大變化。

*指標*是貢獻度分析模型用來評估及比較測試和控制資料之間變化的數值。您可以使用貢獻度分析模型指定下列類型的指標：

* [*可加總*](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw#use_a_summable_metric)：
  加總您指定的指標資料欄值，然後為每個資料區隔計算總計。
* [*可加總比率*](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw#use_a_summable_ratio_metric)：
  加總您指定的兩個數值資料欄的值，並判斷每個資料區段之間的比率。
* [*可依類別加總*](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw#use_a_summable_by_category_metric)：
  加總數值資料欄的值，然後除以類別資料欄中的不重複值數量。

*區隔*是資料的切片，由特定維度值組合所識別。舉例來說，如果貢獻度分析模型是以`store_number`、`customer_id` 和 `day` 維度為依據，則這些維度值的每個不重複組合都代表一個區隔。下表中的每一列代表不同區隔：

| **`store_number`** | **`customer_id`** | **`day`** |
| --- | --- | --- |
| 商店 1 |  |  |
| 商店 1 | 顧客 1 |  |
| 商店 1 | 顧客 1 | 星期一 |
| 商店 1 | 顧客 1 | 星期二 |
| 商店 1 | 顧客 2 |  |
| 商店 2 |  |  |

### 使用貢獻度分析模型

您可以使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw)建立貢獻度分析模型。

如要縮短模型建立時間，請指定[先驗支援度門檻](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw#use_an_apriori_support_threshold)。先驗支援度門檻可讓您修剪較小且較不相關的區隔，模型只會使用最大且最相關的區隔。

建立貢獻度分析模型後，您可以使用 [`ML.GET_INSIGHTS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-get-insights?hl=zh-tw)，擷取模型計算的指標資訊。函式輸出內容包含多個洞察資料列，每個洞察資料列對應一個區隔，並提供該區隔的相應指標。

## 貢獻分析使用者歷程

下表說明可與貢獻度分析搭配使用的陳述式和函式：

| 陳述式或函式 | [預先處理特徵](https://docs.cloud.google.com/bigquery/docs/preprocess-overview?hl=zh-tw) | 分析結果生成功能 | 教學課程 |
| --- | --- | --- | --- |
| [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw) | [手動預先處理](https://docs.cloud.google.com/bigquery/docs/manual-preprocessing?hl=zh-tw) | [`ML.GET_INSIGHTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-get-insights?hl=zh-tw) | * [使用可相加的指標，從貢獻度分析模型取得資料洞察](https://docs.cloud.google.com/bigquery/docs/get-contribution-analysis-insights?hl=zh-tw) * [使用可相加的比率指標，從貢獻度分析模型取得資料洞察](https://docs.cloud.google.com/bigquery/docs/get-contribution-analysis-insights-sum-ratio?hl=zh-tw) |

## 後續步驟

* [建立貢獻度分析模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw)
* [從貢獻度分析模型取得資料洞察](https://docs.cloud.google.com/bigquery/docs/get-contribution-analysis-insights?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-17 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-17 (世界標準時間)。"],[],[]]