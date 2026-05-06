Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 避免過度配適

訓練 BigQuery ML 模型時，常見的陷阱是[過度擬合](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#overfitting)。如果模型過度符合訓練資料，就會發生過度配適情形，導致模型無法準確預測新資料。BigQuery ML 支援兩種避免過度訓練的方法：[提早中止訓練](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#early_stopping)和[正規化](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#regularization)。

如要瞭解如何修改下列選項，請參閱[`CREATE MODEL`陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#model_option_list)。

## 提早中止訓練

在 BigQuery ML 中，防止過度訓練的預設選項是提早中止訓練。啟用提早中止訓練功能後，系統會在訓練期間監控[保留資料](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#holdout_data)的[損失](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#loss)，一旦最新疊代的損失改善幅度低於門檻，就會停止訓練。由於訓練期間不會使用保留資料，因此這類資料可做為模型在新資料上的損失估計值。`early_stop`、`min_rel_progress`、`data_split_method` 和 `data_split_eval_fraction` 選項可控制提早中止訓練的行為。

## 正則化

正則化可避免[模型權重](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#weight)過大，防止模型過度配適訓練資料。BigQuery ML 支援兩種方法來控制模型權重的大小：[L1 正規化](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#L1_regularization)和 [L2 正規化](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#L2_regularization)。

根據預設，`l1_reg` 和 `l2_reg` 的值為零，這會停用正規化。在某些資料集中，為 `l1_reg` 和 `l2_reg` 設定正值，可提升訓練模型在新資料上的成效。通常需要透過試誤法，才能找出最佳的正規化參數值，而且一般會實驗幾個數量級的值 (例如 0.01、0.1、1、10 和 100)。

以下提供使用正規化的通用建議：

* 如果您正在實驗正規化參數，請嘗試停用提早中止訓練功能，清楚瞭解正規化的效果。
* 如果特徵數量相較於訓練集大小較多，請嘗試使用較大的正規化參數值。如果每個特徵的觀察結果很少，過度擬合的風險就會更高。
* 如果您擔心許多特徵可能與預測標籤無關，請嘗試將 `l1_reg` 設為大於 `l2_reg` 的值，反之亦然。有[理論證據](http://www.robotics.stanford.edu/%7Eang/papers/icml04-l1l2.ps)顯示，當許多特徵不相關時，L1 正則化效果較佳。

L1 正則化的另一項優點是，它會將許多模型權重設為零，有助於找出最相關的特徵，並訓練精簡模型。

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要開始使用 BigQuery ML，請參閱[在 BigQuery ML 中建立機器學習模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model?hl=zh-tw)。
* 如要進一步瞭解模型的使用方式，請參閱以下說明：
  + [取得模型中繼資料](https://docs.cloud.google.com/bigquery/docs/getting-model-metadata?hl=zh-tw)
  + [列出模型](https://docs.cloud.google.com/bigquery/docs/listing-models?hl=zh-tw)
  + [更新模型中繼資料](https://docs.cloud.google.com/bigquery/docs/updating-model-metadata?hl=zh-tw)
  + [管理模型](https://docs.cloud.google.com/bigquery/docs/managing-models?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]