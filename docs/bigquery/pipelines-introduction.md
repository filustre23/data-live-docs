Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery Pipelines 簡介

您可以使用 BigQuery 管道，自動執行並簡化 BigQuery 資料程序。您可以透過管道依序排定及執行程式碼資產，提高效率並減少人工作業。

## 總覽

管道是由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 驅動。
除了執行程式碼資產，Dataform 還會自動更新 Knowledge Catalog 中管道內建立的資料表的中繼資料。

管道包含下列一或多個程式碼資產：

* [筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)
* [SQL 查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)
* [準備資料](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw)
* SQLX 工作，包括資料表、檢視區塊、來源和資料品質測試

您可以使用管道安排程式碼資產的執行時間。舉例來說，您可以排定每天執行 SQL 查詢，並以最新的來源資料更新資料表，然後將資料表用於資訊主頁。

在含有多個程式碼資產的管道中，您可以定義執行順序。舉例來說，如要訓練機器學習模型，您可以建立工作流程，其中 SQL 查詢會準備資料，後續的筆記本則會使用該資料訓練模型。

觸發管道執行時，BigQuery 會按照依附關係定義的順序執行動作。針對每個動作，BigQuery 會執行下列步驟：

1. 在 BigQuery 中執行編譯後的 SQL。
2. 更新執行記錄中的動作狀態。
3. 動作完成後，Dataform 會自動啟動中繼資料同步作業，將資料同步至 Knowledge Catalog。這項擴充程序會使用 SQLX 設定中定義的語意中繼資料，更新 Knowledge Catalog。這項同步作業會以非同步方式進行，並採用重試機制，確保中繼資料更新不會影響管道延遲，或在 Dataplex API 暫時無法使用時導致工作流程失敗。

## 功能

您可以在管道中執行下列操作：

* [建立新或匯入現有](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw#add_a_pipeline_task)的 SQL 查詢、Notebook、資料準備或 SQLX 工作至管道。
* [排定管道時間表](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)，在指定時間和頻率自動執行。
* 與指定使用者或群組[共用管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw#share_a_pipeline)。
* [分享管道連結](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw#share_a_link_to_a_pipeline)。

## 限制

管道有下列限制：

* 管道僅適用於 Google Cloud 控制台。
* 管道建立後，即無法變更管道的儲存區域。
* 您可以授予使用者或群組所選管道的存取權，但無法授予管道內個別工作的存取權。
* 如果預定 pipeline 執行作業未在下一次預定執行作業開始前完成，系統會略過下一次預定執行作業，並標示為錯誤。

## 設定程式碼資產的預設區域

Google Cloud 專案中的所有新程式碼資產都會使用預設區域。資產建立後，就無法變更區域。

**重要事項：** 建立程式碼資產時，如果變更區域，該區域會成為後續所有程式碼資產的預設區域。現有程式碼資產不受影響。

如要為新的程式碼資產設定預設區域，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 folder「檔案」，開啟檔案瀏覽器：
3. 在專案名稱旁，按一下
   more\_vert
   「查看檔案面板動作」>「切換程式碼區域」。
4. 選取要設為預設的程式碼區域。
5. 按一下 [儲存]。

如要查看支援的區域清單，請參閱「[BigQuery Studio 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqstudio-loc)」。

所有程式碼資產都會儲存在[程式碼資產的預設區域](#set_the_default_region_for_code_assets)中。更新預設區域後，該區域會套用至之後建立的所有程式碼資產。

## 配額與限制

BigQuery 管道須遵守 [Dataform 配額和限制](https://docs.cloud.google.com/dataform/docs/quotas?hl=zh-tw)。

## 定價

執行 BigQuery 管道工作時，BigQuery 會收取運算和儲存空間費用。詳情請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

含有筆記本的管道會產生 Colab Enterprise 執行階段費用，費用依[預設機型](https://docs.cloud.google.com/colab/docs/runtimes?hl=zh-tw#default_runtime_specifications)而定。如需定價詳情，請參閱「[Colab Enterprise 定價](https://cloud.google.com/colab/pricing?hl=zh-tw)」。

系統會使用 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw) 記錄每次 BigQuery 管道執行作業。系統會自動為 BigQuery 管道執行啟用記錄功能，這可能會產生 Cloud Logging 的計費費用。詳情請參閱「[Cloud Logging 定價](https://cloud.google.com/logging/pricing?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[建立管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。
* 瞭解如何[管理管道](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw)。
* 瞭解如何[排定管道](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-15 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-15 (世界標準時間)。"],[],[]]