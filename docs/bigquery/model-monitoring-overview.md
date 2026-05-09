Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 模型監控總覽

本文說明 BigQuery ML 如何透過評估及比較模型使用的資料，支援監控機器學習 (ML) 模型。包括比較模型的提供資料與訓練資料，以及比較新的提供資料與先前使用的提供資料。

瞭解模型使用的資料是機器學習的重要環節，因為這些資料會影響模型效能。瞭解訓練和服務資料之間的差異，對於確保模型長期維持準確度特別重要。模型在與訓練資料相似的服務資料上，表現最佳。如果服務資料與模型訓練資料不同，就算模型本身沒有變動，效能也可能會降低。

BigQuery ML 提供多項函式，可協助您分析訓練和服務資料的*資料偏斜*和*資料漂移*：

* 當訓練資料的特徵值分布與正式環境中的服務資料顯著不同時，就會發生*資料偏移*。模型訓練期間會儲存模型訓練統計資料，因此您不需要原始訓練資料，就能使用偏差偵測功能。
* *資料偏移*：當正式環境的特徵資料分布情況隨時間大幅變動時，就會發生資料偏移。系統支援偵測連續資料跨度之間的變異，例如不同服務資料日期之間的變異。這樣一來，如果服務資料隨時間變化，您就能在資料集差異過大而需要重新訓練模型前收到通知。

使用下列函式監控 BigQuery ML 中的模型：

* [`ML.DESCRIBE_DATA`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-describe-data?hl=zh-tw)：計算一組訓練或服務資料的描述性統計資料。
* [`ML.VALIDATE_DATA_SKEW`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-validate-data-skew?hl=zh-tw)：計算一組服務資料的統計資料，然後與訓練 BigQuery ML 模型時計算的訓練資料統計資料進行比較，找出這兩組資料之間的異常差異。系統只會計算服務資料中與訓練資料特徵資料欄相符的特徵資料欄統計資料，以提升效能並降低成本。
* [`ML.VALIDATE_DATA_DRIFT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-validate-data-drift?hl=zh-tw)：計算及比較兩組應用資料的統計資料，找出兩組資料之間的異常差異。
* [`ML.TFDV_DESCRIBE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-tfdv-describe?hl=zh-tw)：計算一組訓練或服務資料的精細描述性統計資料。這個函式的行為與 [TensorFlow `tfdv.generate_statistics_from_csv` API](https://www.tensorflow.org/tfx/data_validation/api_docs/python/tfdv/generate_statistics_from_csv?hl=zh-tw) 相同。
* [`ML.TFDV_VALIDATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-tfdv-validate?hl=zh-tw)：比較訓練和應用資料的統計資料，或兩組應用資料的統計資料，找出兩組資料之間的異常差異。這個函式的行為與 [TensorFlow `validate_statistics` API](https://www.tensorflow.org/tfx/data_validation/api_docs/python/tfdv/validate_statistics?hl=zh-tw) 相同。

## 監控用途

本節說明如何在常見的監控用途中，使用 BigQuery ML 模型監控函式。

### 基本資料偏差監控

如果您想快速開發及監控資料偏斜模型，且不需要精細的偏斜統計資料來整合現有的監控解決方案，就適合使用這個應用實例。

這個用途的典型步驟如下：

1. 在訓練和服務資料上執行 `ML.DESCRIBE_DATA` 函式，確保兩個資料集可適當比較，且在預期參數範圍內。
2. [建立 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)，並使用訓練資料訓練模型。
3. 執行 `ML.VALIDATE_DATA_SKEW` 函式，比較服務資料統計資料與模型建立期間計算出的訓練資料統計資料，查看是否有任何資料偏差。
4. 如果出現資料偏差，請調查根本原因、適當調整訓練資料，然後重新訓練模型。

### 基本資料偏移監控

如果您想快速開發及監控資料偏移模型，且不需要精細的偏移統計資料來整合現有的監控解決方案，就適合使用這個應用實例。

這個用途的典型步驟如下：

1. 在訓練和服務資料上執行 `ML.DESCRIBE_DATA` 函式，確保兩個資料集彼此適當比較，且在預期參數範圍內。
2. [建立 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)，並使用訓練資料訓練模型。
3. 執行 `ML.VALIDATE_DATA_DRIFT` 函式，比較兩個不同服務資料集的統計資料，查看是否有任何資料漂移。舉例來說，您可能想比較目前的放送資料與[表格快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)中的歷史放送資料，或是與特定時間點放送的功能，這可透過 [`ML.FEATURES_AT_TIME` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-feature-time?hl=zh-tw)取得。
4. 如果發生資料偏移，請調查根本原因、適當調整訓練資料，然後重新訓練模型。

### 進階資料偏差或偏移監控

如果您想取得精細的偏斜或漂移統計資料，以便與現有的監控解決方案整合，或用於其他用途，就適合採用這個應用實例。

這個用途的典型步驟如下：

1. 在訓練和服務資料上，以適合監控解決方案的間隔執行 `ML.TFDV_DESCRIBE` 函式，並[儲存查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw)。這個步驟可讓您比較未來的服務資料與過去時間點的訓練和服務資料。
2. 在訓練和提供資料的統計資料，或兩組提供資料的統計資料上執行 `ML.TFDV_VALIDATE` 函式，分別評估資料偏斜或特徵漂移。訓練和服務資料必須以 JSON 格式提供，並採用 TensorFlow [`DatasetFeatureStatisticsList` Protocol Buffers](https://www.tensorflow.org/tfx/tf_metadata/api_docs/python/tfmd/proto/statistics_pb2/DatasetFeatureStatisticsList?hl=zh-tw)。您可以執行 `ML.TFDV_DESCRIBE` 函式，以正確格式產生通訊協定緩衝區，也可以從 BigQuery 外部載入。以下範例說明如何評估特徵偏斜：

   ```
   DECLARE stats1 JSON;
   DECLARE stats2 JSON;

   SET stats1 = (
     SELECT * FROM ML.TFDV_DESCRIBE(TABLE `myproject.mydataset.training`)
   );
   SET stats2 = (
     SELECT * FROM ML.TFDV_DESCRIBE(TABLE `myproject.mydataset.serving`)
   );

   SELECT ML.TFDV_VALIDATE(stats1, stats2, 'SKEW');

   INSERT `myproject.mydataset.serve_stats`
     (t, dataset_feature_statistics_list)
   SELECT CURRENT_TIMESTAMP() AS t, stats1;
   ```
3. 如有資料偏斜或資料漂移，請調查根本原因、適當調整訓練資料，然後重新訓練模型。

## 監控資料視覺化

部分監控功能可與 [Vertex AI 模型監控](https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview?hl=zh-tw)整合，方便您使用圖表[分析模型監控功能輸出內容](https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/run-monitoring-job?hl=zh-tw#analyze_monitoring_job_results)。

使用 Vertex AI 視覺化功能有以下好處：

* **互動式視覺化**：在 Vertex AI 控制台使用圖表，探索資料分布、偏斜指標和漂移指標。
* **歷史分析**：使用 Vertex AI 視覺化功能，追蹤一段時間內的模型監控結果。這有助於找出資料變更的趨勢和模式，以便主動更新及維護模型。
* **集中管理**：在統一的 Vertex AI 資訊主頁中，管理所有 BigQuery ML 和 Vertex AI 模型的監控作業。

您可以使用 `ML.VALIDATE_DATA_DRIFT` 函式的 `MODEL` 引數，啟用該函式輸出的視覺化功能。您可以使用 `ML.VALIDATE_DATA_SKEW` 函式的 `enable_visualization_link` 引數，啟用該函式輸出的視覺化功能。

只有[註冊](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw#register_models)至 Vertex AI 的模型，才能使用監控視覺化功能。您可以使用 [`ALTER MODEL` 陳述式註冊現有模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-alter-model?hl=zh-tw)。

## 監控自動化

您可以使用[排程查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)執行監控函式、評估輸出內容，並在偵測到異常情形時重新訓練模型，自動執行監控作業。您必須在[設定排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#set_up_scheduled_queries)時啟用電子郵件通知。

如需自動執行 `ML.VALIDATE_DATA_SKEW` 函式的範例，請參閱「[自動偵測偏斜](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-validate-data-skew?hl=zh-tw#automate_skew_detection)」。

## 後續步驟

如要進一步瞭解 ML 模型支援的 SQL 陳述式和函式，請參閱[ML 模型端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]