Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

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

管道由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 提供支援。

管線包含下列一或多個程式碼資產：

* [筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)
* [SQL 查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)
* [準備資料](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw)

您可以使用管道排定程式碼資產的執行時間。舉例來說，您可以安排每天執行 SQL 查詢，並使用最新的來源資料更新資料表，然後將資料表用於資訊主頁。

在含有多個程式碼資產的管道中，您可以定義執行順序。舉例來說，如要訓練機器學習模型，您可以建立工作流程，其中 SQL 查詢會準備資料，然後後續的筆記本會使用該資料訓練模型。

## 功能

您可以在管道中執行下列操作：

* [建立新的或匯入現有的](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw#add_a_pipeline_task)
  SQL 查詢或 Notebooks 到管道中。
* [排定 pipeline 時間](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)，在指定時間和頻率自動執行。
* 與指定使用者或群組[共用管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw#share_a_pipeline)。
* [分享管道連結](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw#share_a_link_to_a_pipeline)。

## 限制

管道有下列限制：

* 管道僅適用於 Google Cloud 控制台。
* 管線建立後，就無法變更儲存管線的區域。
* 您可以授予使用者或群組所選管道的存取權，但無法授予管道中個別工作的存取權。
* 如果排定的管道執行作業未在下一次排定的執行作業開始前完成，系統會略過下一次排定的執行作業，並標示為錯誤。

## 設定程式碼資產的預設區域

Google Cloud 專案中的所有新程式碼資產都會使用預設區域。資產建立後，就無法變更區域。

**重要事項：** 如果在建立程式碼資產時變更區域，該區域會成為後續所有程式碼資產的預設區域。現有的程式碼資產不會受到影響。

如要設定新程式碼資產的預設區域，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 folder「檔案」，開啟檔案瀏覽器：
3. 在專案名稱旁，按一下
   more\_vert
   「View files panel actions」(查看檔案面板動作) >「Switch code region」(切換程式碼區域)。
4. 選取要設為預設的程式碼區域。
5. 按一下 [儲存]。

如需支援的區域清單，請參閱「[BigQuery Studio 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqstudio-loc)」。

## 支援的地區

所有程式碼資產都會儲存在[程式碼資產的預設區域](#set_the_default_region_for_code_assets)中。更新預設區域後，系統會變更該時間點之後建立的所有程式碼資產區域。

下表列出管道適用的區域：

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

## 配額與限制

BigQuery 管道須遵守 [Dataform 配額和限制](https://docs.cloud.google.com/dataform/docs/quotas?hl=zh-tw)。

## 定價

執行 BigQuery 管道工作時，BigQuery 會收取運算和儲存空間費用。詳情請參閱 [BigQuery 計價方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw)一文。

含有筆記本的管道會根據[預設機型](https://docs.cloud.google.com/colab/docs/runtimes?hl=zh-tw#default_runtime_specifications)產生 Colab Enterprise 執行階段費用。如需定價詳細資料，請參閱 [Colab Enterprise 定價](https://cloud.google.com/colab/pricing?hl=zh-tw)。

系統會使用 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw) 記錄每次 BigQuery 管道執行作業。系統會自動為 BigQuery 管道執行啟用記錄功能，這可能會產生 Cloud Logging 帳單費用。詳情請參閱 [Cloud Logging 定價](https://cloud.google.com/logging/pricing?hl=zh-tw)。

## 後續步驟

* 瞭解如何[建立管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。
* 瞭解如何[管理管道](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw)。
* 瞭解如何[排定管道](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]