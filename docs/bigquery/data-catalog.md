Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 搭配使用 Knowledge Catalog 與 BigQuery

Knowledge Catalog (舊稱 Dataplex Universal Catalog) 與 BigQuery 互動，做為 BigQuery 中繼資料的中央資料治理和代理存取層。詳情請參閱「[Knowledge Catalog 總覽](https://docs.cloud.google.com/knowledge-catalog/docs/introduction?hl=zh-tw)」。

## 如何搭配使用 Knowledge Catalog 和 BigQuery？

Knowledge Catalog 與 BigQuery 的互動方式如下。

### 自動擷取中繼資料

Knowledge Catalog 會自動探索 BigQuery 資產的技術中繼資料，並建立索引。包含下列項目：

* **資產類型**：[資料集、資料表、檢視表、模型、常式、連線、連結的資料集](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw)和[圖表](https://docs.cloud.google.com/bigquery/docs/graph-overview?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。
* **BigQuery sharing**：BigQuery sharing (舊稱 Analytics Hub) 的[交換和清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)。
* **即時更新**：系統支援近乎即時的擷取作業，並使用 Pub/Sub 提供[*中繼資料變更動態饋給*](https://docs.cloud.google.com/knowledge-catalog/docs/metadata-change-feeds-overview?hl=zh-tw)，通知下游系統 BigQuery 中的結構定義變更或刪除。
* **探索暗資料**：Knowledge Catalog 可[掃描非結構化檔案](https://docs.cloud.google.com/knowledge-catalog/docs/data-insights-unstructured-data?hl=zh-tw) (例如 Cloud Storage 中的 PDF)，擷取實體，並轉換為 BigQuery 中可查詢的資產。這項功能可讓先前無法存取的「暗資料」用於 BigQuery 數據分析和 AI 基準化。

### 中繼資料表示法和擴充

* **項目**：每個 BigQuery 資料表或資產在目錄中都以[*項目*](https://docs.cloud.google.com/knowledge-catalog/docs/ingest-custom-sources?hl=zh-tw)表示，而非整個資料表，例如 `project.dataset.table`。
* **資料品質評量表整合**：Knowledge Catalog 為目錄中的每個項目提供[資料品質評量表](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#data-quality-scorecard)。除了內建的 Knowledge Catalog 資料掃描作業，Dataform 的斷言結果也是這份評量表的資料來源。
* **自動擴充中繼資料**：使用 Dataform 建立資料表和檢視表時，可以直接在程式碼中定義語意中繼資料。管道動作順利完成後，這項中繼資料會自動同步至 Knowledge Catalog。支援的切面類型如下：

  + 總覽：項目的說明文件和摘要文字。
  + 一般切面：技術詳細資料的語義中繼資料標記，例如資料表系統和類型資訊。

  如要查看中繼資料更新狀態，請按照「[查看過去的手動執行作業](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw#view-manual-runs)」中的操作說明進行。

  中繼資料同步後，您可以在 Knowledge Catalog 搜尋及查看項目。詳情請參閱「[搜尋資源](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw#search-data-assets)」。
* **資料欄層級中繼資料**：個別資料欄或欄位會以*[路徑](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw)*表示，可讓您將特定中繼資料 (例如 PII 標記或資料品質分數) 附加至 BigQuery 資料表中的個別欄位，而非僅限於資料表本身。
* **切面**：技術中繼資料會以[*切面*](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata?hl=zh-tw#aspects)充實，為資料新增業務情境，例如擁有權、資料品質和說明文件。
* **資料產品**：您可以將相關的 BigQuery 資產封裝成[資料產品](https://docs.cloud.google.com/knowledge-catalog/docs/data-products-overview?hl=zh-tw) (例如電子商務業務資料)，並設定共用存取權和控管限制。

### 資料探索與搜尋

* **語意搜尋**：使用者可以透過自然語言[搜尋](https://docs.cloud.google.com/knowledge-catalog/docs/semantic-search?hl=zh-tw) BigQuery 資料，這對資料科學家和 AI 代理特別有用，能使用冗長或複雜的查詢，找出可靠的資料產品。
* **名稱翻譯**：為方便透過程式查詢，系統允許將 BigQuery SQL 名稱或完整名稱[翻譯](https://docs.cloud.google.com/knowledge-catalog/docs/samples/dataplex-lookup-entry?hl=zh-tw#code-sample)為 Knowledge Catalog 項目名稱。

### 代理存取權和建立基準

* **代理存取權**：AI 代理可透過[本機或遠端 MCP 伺服器](https://docs.cloud.google.com/knowledge-catalog/docs/mcp-overview?hl=zh-tw)，探索並彈性使用 Knowledge Catalog 工具。
* **AI 代理的背景資訊**：Knowledge Catalog 會建立[背景資訊圖](https://docs.cloud.google.com/knowledge-catalog/docs/introduction?hl=zh-tw#sample-workflows)，將 BigQuery 資料集與業務語意連結，確保模型使用企業核准的資料，減少 AI 幻覺。

### 管理與法規遵循

* **資料歷程**：Knowledge Catalog 會自動[追蹤](https://docs.cloud.google.com/knowledge-catalog/docs/about-data-lineage?hl=zh-tw)資料如何流入/流出 BigQuery 資料表，以及如何轉換。這項功能對於稽核整個資料資產中的私密資訊 (例如 PII) 至關重要。
* **存取控管：**中繼資料管理功能與 [Identity and Access Management (IAM)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw) 和 [VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/vpc-sc?hl=zh-tw) 整合，確保探索及存取 BigQuery 中繼資料時，遵循組織的安全政策。

## 後續步驟

進一步瞭解 Knowledge Catalog：

* [Knowledge Catalog 應用實例](https://docs.cloud.google.com/knowledge-catalog/docs/use-cases?hl=zh-tw)
* [Knowledge Catalog 常見問題](https://docs.cloud.google.com/knowledge-catalog/docs/faq?hl=zh-tw)
* [關於 Knowledge Catalog 的中繼資料管理功能](https://docs.cloud.google.com/knowledge-catalog/docs/metadata-overview?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-19 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-19 (世界標準時間)。"],[],[]]