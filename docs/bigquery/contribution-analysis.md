Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 貢獻分析總覽

您可以在 BigQuery ML 中使用貢獻分析，比較測試和控制資料集，並找出哪些資料區隔促成主要指標的變化。視指標類型和維度數量而定，您可以使用 [`AI.KEY_DRIVERS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-key-drivers?hl=zh-tw)直接分析主要驅動因素，或使用 [`ML.GET_INSIGHTS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-get-insights?hl=zh-tw)建立模型並擷取洞察資料。

## 關於貢獻分析

貢獻分析 (又稱主要驅動因素分析) 是一種方法，可用來產生多維度資料中重要指標變化的洞察資料。舉例來說，您可以使用貢獻分析，瞭解哪些資料導致兩個季度的收益數字發生變化，或比較兩組訓練資料，瞭解機器學習模型效能的變化。

貢獻分析是一種[增強型數據分析](https://en.wikipedia.org/wiki/Augmented_Analytics)，也就是運用人工智慧 (AI) 強化及自動化資料分析和理解。貢獻分析可達成增強型數據分析的主要目標之一，也就是協助使用者找出資料中的模式。

## 使用 BigQuery ML 進行貢獻分析

貢獻分析會比較測試資料集和控制資料集，偵測特定指標出現變化的資料區隔。舉例來說，您可以使用 2023 年底擷取的銷售資料[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)做為測試資料，並使用 2022 年底擷取的資料表快照做為控制資料，然後比較兩者，瞭解銷售額隨時間變化的情況。貢獻分析可顯示哪一個資料區隔 (例如特定區域的線上顧客) 對年度銷售額變化的影響最大。

「指標」是貢獻分析模型用來評估及比較測試資料和控制資料之間變化的數值。您可以使用貢獻分析模型指定下列類型的指標：

* [*Summable*](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw#use_a_summable_metric)：加總指定指標欄的值，然後決定每個資料區隔的總計。
* [*可加總比率*](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw#use_a_summable_ratio_metric)：加總您指定的兩個數值欄，並判斷每個資料區隔中這兩個值的比率。
* [*Summable by category*](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw#use_a_summable_by_category_metric)：加總數值資料欄的值，然後除以類別資料欄中不重複值的數量。

「區隔」是指由特定維度值組合識別出的資料片段。舉例來說，如果貢獻分析模型是以 `store_number`、`customer_id` 和 `day` 維度為基礎，則這些維度值的每個不重複組合都代表一個區隔。在下表中，每一列代表不同的區隔：

| **`store_number`** | **`customer_id`** | **`day`** |
| --- | --- | --- |
| 商店 1 |  |  |
| 商店 1 | 客戶 1 |  |
| 商店 1 | 客戶 1 | 星期一 |
| 商店 1 | 客戶 1 | 星期二 |
| 商店 1 | 客戶 2 |  |
| store 2 |  |  |

### 不使用模型分析資料

如果維度少於 12 個，且使用可加總指標，則可透過 [`AI.KEY_DRIVERS` TVF](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-key-drivers?hl=zh-tw) 執行貢獻分析。對於大多數應用程式，我們建議使用 `AI.KEY_DRIVERS` 函式，而非建立模型，因為該函式提供簡化的語法、更快的結果和自動剪枝功能。函式輸出內容包含多列洞察資料，每列洞察資料對應一個區隔，並提供該區隔的對應指標。

### 使用貢獻分析模型

如果需要超過 12 個維度或其他類型的指標，可以使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw)建立貢獻分析模型。

如要縮短模型建立時間，請指定[先驗支援門檻](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw#use_an_apriori_support_threshold)。先驗支援門檻可讓您刪除小型和關聯性較低的區隔，讓模型只使用最大和關聯性最高的區隔。

建立貢獻分析模型後，您可以使用 [`ML.GET_INSIGHTS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-get-insights?hl=zh-tw)擷取模型計算的指標資訊。函式輸出內容包含多列洞察資料，每列洞察資料對應一個區隔，並提供該區隔的對應指標。

## 貢獻分析使用者歷程

下表說明可與貢獻分析搭配使用的陳述式和函式：

| 陳述式或函式 | [預先處理特徵](https://docs.cloud.google.com/bigquery/docs/preprocess-overview?hl=zh-tw) | 分析結果生成功能 | 教學課程 |
| --- | --- | --- | --- |
| [`AI.KEY_DRIVERS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-key-drivers?hl=zh-tw) | [手動預先處理](https://docs.cloud.google.com/bigquery/docs/manual-preprocessing?hl=zh-tw) | 不適用 | [愛荷華州酒類銷售資料的貢獻分析範例](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-key-drivers?hl=zh-tw#example) |
| [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw) | [手動預先處理](https://docs.cloud.google.com/bigquery/docs/manual-preprocessing?hl=zh-tw) | [`ML.GET_INSIGHTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-get-insights?hl=zh-tw) | * [使用可相加的指標，從貢獻分析模型取得資料洞察](https://docs.cloud.google.com/bigquery/docs/get-contribution-analysis-insights?hl=zh-tw) * [使用可相加的比率指標，從貢獻分析模型取得資料洞察](https://docs.cloud.google.com/bigquery/docs/get-contribution-analysis-insights-sum-ratio?hl=zh-tw) |

## 後續步驟

* [進一步瞭解`AI.KEY_DRIVES` TVF](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-key-drivers?hl=zh-tw)
* [建立貢獻分析模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw)
* [從貢獻分析模型取得資料洞察](https://docs.cloud.google.com/bigquery/docs/get-contribution-analysis-insights?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-23 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-23 (世界標準時間)。"],[],[]]