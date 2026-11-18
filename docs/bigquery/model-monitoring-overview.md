Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 模型監控總覽

在 BigQuery ML 中監控機器學習 (ML) 模型，即可評估及比較模型用於預測的資料。包括比較模型的提供資料與訓練資料，以及比較新的提供資料與先前使用的提供資料。

瞭解模型使用的資料是機器學習的重要環節，因為這些資料會影響模型效能。瞭解訓練和提供資料之間的差異，對於確保模型長期準確性尤為重要。如果提供資料與訓練資料相似，模型成效會最好。如果提供資料與模型訓練資料不同，就算模型本身沒有變動，效能也可能會降低。

BigQuery ML 提供多項函式，可協助您分析訓練和提供資料，找出*資料偏斜*和*資料偏移*：

* 如果訓練資料的特徵值分布情形與正式環境中的服務資料有顯著差異，就會發生*資料偏斜*。模型的訓練統計資料會在模型訓練期間儲存，因此您不需要原始訓練資料，即可使用偏差偵測功能。
* 當正式環境的特徵資料分布隨時間大幅變動時，就會發生*資料偏移*。系統支援連續資料範圍的偏移偵測，例如不同日期的供應資料。這樣一來，如果提供資料隨時間變化，您就能在資料集差異過大而無法重新訓練模型之前，收到通知。

使用下列函式，在 BigQuery ML 中監控模型：

* [`ML.DESCRIBE_DATA`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-describe-data?hl=zh-tw)：計算一組訓練或服務資料的敘述統計資料。
* [`ML.VALIDATE_DATA_SKEW`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-validate-data-skew?hl=zh-tw)：計算一組服務資料的統計資料，然後與訓練 BigQuery ML 模型時計算的訓練資料統計資料進行比較，找出兩個資料集之間的異常差異。系統只會針對提供資料中與訓練資料特徵欄相符的特徵欄計算統計資料，以提升效能並降低成本。
* [`ML.VALIDATE_DATA_DRIFT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-validate-data-drift?hl=zh-tw)：計算並比較兩組服務資料的統計資料，找出兩組資料集之間的異常差異。
* [`ML.TFDV_DESCRIBE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-tfdv-describe?hl=zh-tw)：針對一組訓練或服務資料，計算精細的敘述統計資料。這個函式的行為與 [TensorFlow `tfdv.generate_statistics_from_csv` API](https://www.tensorflow.org/tfx/data_validation/api_docs/python/tfdv/generate_statistics_from_csv?hl=zh-tw) 相同。
* [`ML.TFDV_VALIDATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-tfdv-validate?hl=zh-tw)：比較訓練和應用資料的統計資料，或兩組應用資料的統計資料，找出兩個資料集之間的異常差異。這項函式的行為與 [TensorFlow `validate_statistics` API](https://www.tensorflow.org/tfx/data_validation/api_docs/python/tfdv/validate_statistics?hl=zh-tw) 相同。

## Monitoring 用途

本節說明如何在常見的監控用途中，使用 BigQuery ML 模型監控函式。

### 基本資料偏斜監控

如果您想快速開發及監控模型，瞭解資料偏斜情形，且不需要精細的偏斜統計資料，來與現有監控解決方案整合，就適合採用這種做法。

這個用途的一般步驟如下：

1. 對訓練和服務資料執行 `ML.DESCRIBE_DATA` 函式，確保兩個資料集能適當比較，且在預期參數範圍內。
2. [建立 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)，並使用訓練資料進行訓練。
3. 執行 `ML.VALIDATE_DATA_SKEW` 函式，比較提供資料統計資料與模型建立期間計算的訓練資料統計資料，確認是否有任何資料偏斜。
4. 如果資料偏斜，請調查根本原因，適當調整訓練資料，然後重新訓練模型。

### 基本資料偏移監控

如果您想快速開發模型並監控資料偏移，且不需要精細的偏移統計資料來整合現有監控解決方案，就適合採用這種做法。

這個用途的一般步驟如下：

1. 對訓練和提供資料執行 `ML.DESCRIBE_DATA` 函式，確保兩個資料集能適當比較，且在預期參數範圍內。
2. [建立 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)，並使用訓練資料進行訓練。
3. 執行 `ML.VALIDATE_DATA_DRIFT` 函式，比較兩個不同服務資料集的統計資料，看看是否有資料偏移。舉例來說，您可能想將目前的特徵供應資料與[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)中的歷來特徵供應資料進行比較，或與特定時間點供應的特徵進行比較，您可以使用 [`ML.FEATURES_AT_TIME` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-feature-time?hl=zh-tw)取得這些資料。
4. 如果發生資料偏移，請調查根本原因、適當調整訓練資料，然後重新訓練模型。

### 進階資料偏斜或偏移監控

如要將精細的偏誤或偏移統計資料與現有監控解決方案整合，或用於其他用途，就適合採用這個做法。

這個用途的一般步驟如下：

1. 請根據監控解決方案，以適當的時間間隔對訓練和服務資料執行 `ML.TFDV_DESCRIBE` 函式，並[儲存查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw)。這個步驟可讓您比較未來的提供資料，以及過去時間點的訓練和提供資料。
2. 對訓練和服務資料統計資料，或兩組服務資料統計資料執行 `ML.TFDV_VALIDATE` 函式，分別評估資料偏斜或特徵偏移。訓練和提供資料必須以 JSON 格式的 TensorFlow [`DatasetFeatureStatisticsList` 通訊協定緩衝區](https://www.tensorflow.org/tfx/tf_metadata/api_docs/python/tfmd/proto/statistics_pb2/DatasetFeatureStatisticsList?hl=zh-tw)提供。您可以執行 `ML.TFDV_DESCRIBE` 函式，以正確格式產生通訊協定緩衝區，也可以從 BigQuery 外部載入。以下範例說明如何評估特徵扭曲：

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
3. 如果發生資料偏斜或資料偏移，請調查根本原因，適當調整訓練資料，然後重新訓練模型。

## 監控圖表

部分監控函式可與 [Gemini Enterprise Agent Platform 模型監控](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/model-monitoring/overview?hl=zh-tw)整合，讓您使用圖表[分析模型監控函式輸出內容](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/model-monitoring/run-monitoring-job?hl=zh-tw#analyze_monitoring_job_results)。

使用 Agent Platform 視覺化功能有以下優點：

* **互動式視覺化**：在 Agent Platform 控制台中使用圖表和圖形，探索資料分布、偏斜指標和偏移指標。
* **歷來分析**：使用 Agent Platform 視覺化圖表，追蹤模型監控結果隨時間的變化。這可讓您找出資料變化的趨勢和模式，以便主動更新及維護模型。
* **集中管理**：在整合式 Agent Platform 資訊主頁中，管理所有 BigQuery ML 和 Agent Platform 模型的監控作業。

您可以使用 `ML.VALIDATE_DATA_DRIFT` 函式的 `MODEL` 引數，啟用該函式輸出的視覺化功能。您可以使用 `ML.VALIDATE_DATA_SKEW` 函式的 `enable_visualization_link` 引數，啟用該函式輸出的視覺化功能。

只有[註冊](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw#register_models)至 Agent Platform 的模型，才能使用監控圖表。您可以使用 [`ALTER MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-alter-model?hl=zh-tw)註冊現有模型。

## 監控自動化

您可以使用[排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)執行監控函式、評估輸出內容，並在偵測到異常狀況時重新訓練模型，藉此自動監控。[設定排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#set_up_scheduled_queries)時，必須啟用電子郵件通知。

如需自動化 `ML.VALIDATE_DATA_SKEW` 函式的範例，請參閱「[自動偵測偏差](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-validate-data-skew?hl=zh-tw#automate_skew_detection)」。

## 後續步驟

如要進一步瞭解機器學習模型支援的 SQL 陳述式和函式，請參閱「[機器學習模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-17 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-17 (世界標準時間)。"],[],[]]