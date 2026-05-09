Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 超參數調整總覽

在機器學習中，超參數調整會找出學習演算法的最佳超參數組合。超參數是模型引數，其值是在學習程序開始前設定。反之，其他參數的值 (例如線性模型的係數) 則會經過學習。

超參數調整功能可減少手動疊代超參數的時間，讓您有更多時間專注於探索資料的洞察資訊。

您可以為下列模型類型指定超參數調整選項：

* [線性迴歸和邏輯迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)
* [K-means](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw)
* [矩陣分解](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw)
* [自動編碼器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder?hl=zh-tw)
* [強化型樹狀結構](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
* [隨機森林](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)
* [深層類神經網路 (DNN)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)
* [廣度和深度網路](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)

對於這類模型，只要在 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)中為 [`NUM_TRIALS` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#num_trials)指定值，即可啟用超參數調整功能。

如要試著對線性迴歸模型執行超參數調整，請參閱「[使用 BigQuery ML 超參數調整功能改善模型效能](https://docs.cloud.google.com/bigquery/docs/hyperparameter-tuning-tutorial?hl=zh-tw)」。

下列模型也支援超參數調整，但不允許您指定特定值：

* [AutoML Tables 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw)預設會在模型訓練中嵌入自動超參數調整功能。
* [ARIMA\_PLUS 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)可讓您設定 [`AUTO_ARIMA` 引數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#auto_arima)，使用 auto.ARIMA 演算法執行超參數調整。這項演算法會為趨勢模組執行超參數調整。超參數調整功能不支援整個[模型化管道](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#modeling-pipeline)。

## 位置

如要瞭解哪些地區支援超參數微調，請參閱 [BigQuery ML 地區](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqml-loc)。

## 設定超參數

如要調整超參數，您必須為該超參數指定一系列值，供模型用於一組試驗。如要在 `CREATE MODEL` 陳述式中設定超參數，請使用下列其中一個關鍵字，而非提供單一值：

* `HPARAM_RANGE`：雙元素 `ARRAY(FLOAT64)` 值，用於定義超參數連續值的搜尋空間下限和上限。使用這個選項可為超參數指定值範圍，例如 `LEARN_RATE = HPARAM_RANGE(0.0001, 1.0)`。
* `HPARAM_CANDIDATES`：`ARRAY(STRUCT)` 值，用於指定超參數的離散值集。使用這個選項為超參數指定一組值，例如 `OPTIMIZER = HPARAM_CANDIDATES(['ADAGRAD', 'SGD', 'FTRL'])`。

## 超參數和目標

下表列出支援超參數調整的各模型類型，以及支援的超參數和目標：

| 模型類型 | 超參數目標 | 超參數 | 有效範圍 | 預設範圍 | 縮放類型 |
| --- | --- | --- | --- | --- | --- |
| `LINEAR_REG` | `MEAN_ABSOLUTE_ERROR`   `MEAN_SQUARED_ERROR`   `MEAN_SQUARED_LOG_ERROR`   `MEDIAN_ABSOLUTE_ERROR`   `R2_SCORE` (預設)   `EXPLAINED_VARIANCE` | `L1_REG`   `L2_REG` | `(0, ∞]`   `(0, ∞]` | `(0, 10]`   `(0, 10]` | `LOG`   `LOG` |
| `LOGISTIC_REG` | `PRECISION`   `RECALL`   `ACCURACY`   `F1_SCORE`   `LOG_LOSS`   `ROC_AUC` (預設) | `L1_REG`   `L2_REG` | `(0, ∞]`   `(0, ∞]` | `(0, 10]`   `(0, 10]` | `LOG`   `LOG` |
| `KMEANS` | `DAVIES_BOULDIN_INDEX` | `NUM_CLUSTERS` | `[2, 100]` | `[2, 10]` | `LINEAR` |
| `MATRIX_ FACTORIZATION` (露骨) | `MEAN_SQUARED_ERROR` | `NUM_FACTORS`   `L2_REG` | `[2, 200]`   `(0, ∞)` | `[2, 20]`   `(0, 10]` | `LINEAR`   `LOG` |
| `MATRIX_ FACTORIZATION` (隱含) | `MEAN_AVERAGE_PRECISION` (預設)   `MEAN_SQUARED_ERROR`   `NORMALIZED_DISCOUNTED_CUMULATIVE_GAIN`   `AVERAGE_RANK` | `NUM_FACTORS`   `L2_REG`   `WALS_ALPHA` | `[2, 200]`   `(0, ∞)`   `[0, ∞)` | `[2, 20]`   `(0, 10]`   `[0, 100]` | `LINEAR`   `LOG`   `LINEAR` |
| `AUTOENCODER` | `MEAN_ABSOLUTE_ERROR`   `MEAN_SQUARED_ERROR` (預設)   `MEAN_SQUARED_LOG_ERROR` | `LEARN_RATE`   `BATCH_SIZE`   `L1_REG`   `L2_REG`   `L1_REG_ACTIVATION`   `DROPOUT`   `HIDDEN_UNITS`     `OPTIMIZER`      `ACTIVATION_FN` | `[0, 1]`   `(0, ∞)`   `(0, ∞)`   `(0, ∞)`   `(0, ∞)`     `[0, 1)`   `[1, ∞)` 陣列   {`ADAM`、`ADAGRAD`、`FTRL`、`RMSPROP`、`SGD`}   {`RELU`、`RELU6`、`CRELU`、`ELU`、`SELU`、`SIGMOID`、`TANH`} | `[0, 1]`   `[16, 1024]`   `(0, 10]`   `(0, 10]`   `(0, 10]`     `[0, 0.8]`   不適用   {`ADAM`, `ADAGRAD`, `FTRL`, `RMSPROP`, `SGD`}   不適用 | `LOG`   `LOG`   `LOG`   `LOG`   `LOG`     `LINEAR`   不適用   不適用      不適用 |
| `DNN_CLASSIFIER` | `PRECISION`   `RECALL`   `ACCURACY`   `F1_SCORE`   `LOG_LOSS`   `ROC_AUC` (預設) | `BATCH_SIZE`   `DROPOUT`   `HIDDEN_UNITS`   `LEARN_RATE`   `OPTIMIZER`      `L1_REG`   `L2_REG`   `ACTIVATION_FN` | `(0, ∞)`   `[0, 1)`   `[1, ∞)` 陣列   `[0, 1]`   {`ADAM`、`ADAGRAD`、`FTRL`、`RMSPROP`、`SGD`}   `(0, ∞)`   `(0, ∞)`   {`RELU`、`RELU6`、`CRELU`、`ELU`、`SELU`、`SIGMOID`、`TANH`} | `[16, 1024]`   `[0, 0.8]`   不適用   `[0, 1]`   {`ADAM`, `ADAGRAD`, `FTRL`, `RMSPROP`, `SGD`}   `(0, 10]`   `(0, 10]`   不適用 | `LOG`   `LINEAR`   不適用   `LINEAR`   不適用      `LOG`   `LOG`   不適用 |
| `DNN_REGRESSOR` | `MEAN_ABSOLUTE_ERROR`   `MEAN_SQUARED_ERROR`   `MEAN_SQUARED_LOG_ERROR`   `MEDIAN_ABSOLUTE_ERROR`   `R2_SCORE` (預設)   `EXPLAINED_VARIANCE` |
| `DNN_LINEAR_ COMBINED_ CLASSIFIER` | `PRECISION`   `RECALL`   `ACCURACY`   `F1_SCORE`   `LOG_LOSS`   `ROC_AUC` (預設) | `BATCH_SIZE`   `DROPOUT`   `HIDDEN_UNITS`   `L1_REG`   `L2_REG`   `ACTIVATION_FN` | `(0, ∞)`   `[0, 1)`   `[1, ∞)` 陣列   `(0, ∞)`   `(0, ∞)`   {`RELU`、`RELU6`、`CRELU`、`ELU`、`SELU`、`SIGMOID`、`TANH`} | `[16, 1024]`   `[0, 0.8]`   不適用   `(0, 10]`   `(0, 10]`   不適用 | `LOG`   `LINEAR`   不適用   `LOG`   `LOG`   不適用 |
| `DNN_LINEAR_ COMBINED_ REGRESSOR` | `MEAN_ABSOLUTE_ERROR`   `MEAN_SQUARED_ERROR`   `MEAN_SQUARED_LOG_ERROR`   `MEDIAN_ABSOLUTE_ERROR`   `R2_SCORE` (預設)   `EXPLAINED_VARIANCE` |
| `BOOSTED_TREE_ CLASSIFIER` | `PRECISION`   `RECALL`   `ACCURACY`   `F1_SCORE`   `LOG_LOSS`   `ROC_AUC` (預設) | `LEARN_RATE`   `L1_REG`   `L2_REG`   `DROPOUT`   `MAX_TREE_DEPTHMAX_TREE_DEPTH`   `SUBSAMPLE`   `MIN_SPLIT_LOSS`   `NUM_PARALLEL_TREE`   `MIN_TREE_CHILD_WEIGHT`   `COLSAMPLE_BYTREE`   `COLSAMPLE_BYLEVEL`   `COLSAMPLE_BYNODE`   `BOOSTER_TYPE`   `DART_NORMALIZE_TYPE`   `TREE_METHOD` | `[0, ∞)`   `(0, ∞)`   `(0, ∞)`   `[0, 1]`   `[1, 20]`      `(0, 1]`   `[0, ∞)`   `[1, ∞)`     `[0, ∞)`     `[0, 1]`     `[0, 1]`     `[0, 1]`     {`GBTREE`, `DART`}   {`TREE`, `FOREST`}   {`AUTO`, `EXACT`, `APPROX`, `HIST`} | `[0, 1]`   `(0, 10]`   `(0, 10]`   不適用   `[1, 10]`      `(0, 1]`   不適用   不適用     不適用     不適用     不適用     不適用     不適用   不適用   不適用 | `LINEAR`   `LOG`   `LOG`   `LINEAR`   `LINEAR`      `LINEAR`   `LINEAR`   `LINEAR`     `LINEAR`     `LINEAR`     `LINEAR`     `LINEAR`     不適用   不適用   不適用 |
| `BOOSTED_TREE_ REGRESSOR` | `MEAN_ABSOLUTE_ERROR`   `MEAN_SQUARED_ERROR`   `MEAN_SQUARED_LOG_ERROR`   `MEDIAN_ABSOLUTE_ERROR`   `R2_SCORE` (預設)   `EXPLAINED_VARIANCE` |
| `RANDOM_FOREST_ CLASSIFIER` | `PRECISION`   `RECALL`   `ACCURACY`   `F1_SCORE`   `LOG_LOSS`   `ROC_AUC` (預設) | `L1_REG`   `L2_REG`   `MAX_TREE_DEPTH`   `SUBSAMPLE`   `MIN_SPLIT_LOSS`   `NUM_PARALLEL_TREE`   `MIN_TREE_CHILD_WEIGHT`   `COLSAMPLE_BYTREE`   `COLSAMPLE_BYLEVEL`   `COLSAMPLE_BYNODE`   `TREE_METHOD` | `(0, ∞)`   `(0, ∞)`   `[1, 20]`   `(0, 1)`   `[0, ∞)`   `[2, ∞)`     `[0, ∞)`     `[0, 1]`     `[0, 1]`     `[0, 1]`   {`AUTO`, `EXACT`, `APPROX`, `HIST`} | `(0, 10]`   `(0, 10]`   `[1, 20]`   `(0, 1)`   不適用   `[2, 200]`     不適用     不適用     不適用     不適用     不適用 | `LOG`   `LOG`   `LINEAR`   `LINEAR`   `LINEAR`   `LINEAR`     `LINEAR`     `LINEAR`     `LINEAR`     `LINEAR`     不適用 |
| `RANDOM_FOREST_ REGRESSOR` | `MEAN_ABSOLUTE_ERROR`   `MEAN_SQUARED_ERROR`   `MEAN_SQUARED_LOG_ERROR`   `MEDIAN_ABSOLUTE_ERROR`   `R2_SCORE` (預設)   `EXPLAINED_VARIANCE` |

大多數 `LOG` 比例超參數會使用 `0` 的開放下界。您仍可使用 `HPARAM_RANGE` 關鍵字設定超參數範圍，將 `0` 設為下限。舉例來說，在提升樹狀結構分類器模型中，您可以將 [`L1_REG` 超參數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw#l1_reg)的範圍設為 `L1_REG = HPARAM_RANGE(0, 5)`。`0` 的值會轉換為 `1e-14`。

支援條件超參數。舉例來說，在提升樹狀結構迴歸模型中，只有當 [`BOOSTER_TYPE` 超參數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw#booster_type)的值為 `DART` 時，您才能微調 [`DART_NORMALIZE_TYPE` 超參數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw#dart_normalize_type)。在這種情況下，您會指定搜尋空間，系統會自動處理條件，如下列範例所示：

```
BOOSTER_TYPE = HPARAM_CANDIDATES(['DART', 'GBTREE'])
DART_NORMALIZE_TYPE = HPARAM_CANDIDATES(['TREE', 'FOREST'])
```

另一個例子是升級樹狀結構模型中 `BOOSTER_TYPE` 和 `DROPOUT` 與 之間的互動。只有在 `BOOSTER_TYPE` 包含 `'DART'` 做為候選項目時，才能調整 `DROPOUT` 參數。如果您為 `DROPOUT` 定義搜尋空間，但將 `BOOSTER_TYPE` 限制為僅 `HPARAM_CANDIDATES(['GBTREE'])`，微調工作就會失敗。

## 搜尋起點

如果您未使用 `HPARAM_RANGE` 或 `HPARAM_CANDIDATES` 為超參數指定搜尋空間，系統會從該超參數的預設值開始搜尋，如該模型類型的 `CREATE MODEL` 主題所述。舉例來說，如果您要為[提升樹狀結構模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)執行超參數調整作業，但未指定 [`L1_REG` 超參數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw#l1_reg)的值，搜尋作業就會從預設值 `0` 開始。

如果您使用 `HPARAM_RANGE` 或 `HPARAM_CANDIDATES` 為超參數指定搜尋空間，搜尋起點會取決於指定的搜尋空間是否包含該超參數的預設值，如該模型類型的 `CREATE MODEL` 主題所述：

* 如果指定範圍包含預設值，搜尋會從該處開始。舉例來說，如果您要為隱含[矩陣因式分解模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw)執行超參數調整，並為 [`WALS_ALPHA` 超參數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw#wals_alpha)指定 `[20, 30, 40, 50]` 值，搜尋作業就會從預設值 `40` 開始。
* 如果指定範圍未包含預設值，搜尋作業會從指定範圍中與預設值最接近的點開始。舉例來說，如果您為 `WALS_ALPHA` 超參數指定 `[10, 20, 30]` 值，搜尋作業就會從 `30` 開始，這是最接近 `40` 預設值的值。

## 資料分割

指定 `NUM_TRIALS` 選項的值時，服務會判斷您正在進行超參數調整，並自動對輸入資料執行 3 向分割，將資料分成訓練、評估和測試集。根據預設，系統會隨機處理輸入資料，然後將資料分割為 80% 用於訓練、10% 用於評估，另外 10% 則用於測試。

每次試驗訓練都會使用訓練和評估集，與不使用超參數調整的模型相同。系統會根據該模型類型的[模型評估指標](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw#output)，計算試用超參數建議。每次試驗訓練結束時，系統都會使用測試集測試試驗，並在模型中記錄指標。這樣一來，最終報表評估指標就能使用模型尚未分析的資料，確保客觀性。評估資料用於計算超參數建議的中間指標，而測試資料則用於計算最終的客觀模型指標。

如要只使用訓練集，請為 `CREATE MODEL` 陳述式的 [`DATA_SPLIT_METHOD` 選項指定 `NO_SPLIT`。](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#data_split_method)

如要只使用訓練和評估集，請為 `CREATE MODEL` 陳述式的 [`DATA_SPLIT_TEST_FRACTION` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#data_split_test_fraction)指定 `0`。如果測試集為空白，系統會將評估集做為測試集，用於最終評估指標報表。

只有在資料分割比例相同時，一般訓練工作產生的模型指標，才能與超參數調整訓練工作產生的模型指標進行比較。舉例來說，以下模型可相互比較：

* 非超參數調整：`DATA_SPLIT_METHOD='RANDOM', DATA_SPLIT_EVAL_FRACTION=0.2`
* 超參數調整：`DATA_SPLIT_METHOD='RANDOM', DATA_SPLIT_EVAL_FRACTION=0.2, DATA_SPLIT_TEST_FRACTION=0`

## 效能

使用超參數調整時，模型效能通常不會比使用預設搜尋空間且不使用超參數調整時差。如果模型使用預設搜尋空間，且未使用超參數調整功能，則一律會在第一次試驗時使用預設超參數。

如要確認超參數調整功能是否提升模型效能，請比較超參數調整模型的最合適實驗，以及非超參數調整模型的第一個實驗。

## 遷移學習

如果您在 `CREATE MODEL` 陳述式中將 [`HPARAM_TUNING_ALGORITHM` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#hparam_tuning_algorithm)設為 `VIZIER_DEFAULT`，系統就會預設啟用遷移學習。如果模型符合下列條件，即可從先前調整的模型中學習，進而提升超參數調整效果：

* 與先前微調的模型類型相同。
* 與先前調整過的模型位於同一個專案。
* 這項功能會使用相同的超參數搜尋空間，或是先前調整模型超參數搜尋空間的*子集*。子集使用相同的超參數名稱和類型，但不一定要有相同的範圍。舉例來說，`(a:[0, 10])` 會視為 `(a:[-1, 1], b:[0, 1])` 的子集。

遷移學習不需要輸入資料相同。

遷移學習有助於解決冷啟動問題，也就是系統在第一批試用期間會隨機探索。遷移學習會為系統提供超參數及其目標的初步知識。如要持續提升模型品質，請一律使用相同或部分超參數，訓練新的超參數調整模型。

遷移學習可協助超參數調整更快收斂，而不是協助子模型收斂。

## 處理錯誤

超參數調整功能會以以下方式處理錯誤：

* 取消：如果訓練工作在執行期間取消，所有成功的試驗仍可使用。
* 輸入內容無效：如果使用者輸入內容無效，服務會傳回使用者錯誤。
* 無效的超參數：如果超參數對測試無效，系統會略過測試，並在 `ML.TRIAL_INFO` 函式的輸出內容中標示為 `INFEASIBLE`。
* 試用版內部錯誤：如果 `NUM_TRIALS` 值因 `INTERNAL_ERROR` 而失敗的比例超過 10%，訓練工作就會停止並傳回使用者錯誤。
* 如果因 `INTERNAL_ERROR` 而失敗的 `NUM_TRIALS` 值少於 10%，訓練作業會繼續進行，並在 `ML.TRIAL_INFO` 函式的輸出內容中，將失敗的試驗標示為 `FAILED`。

## 提供模型函式

您可以搭配多個現有提供模型函式，使用超參數調整的輸出模型。如要使用這些函式，請遵守下列規則：

* 如果函式會接收輸入資料，則只會傳回一次試驗的結果。根據預設，這是最佳試用期，但您也可以指定 `TRIAL_ID` 做為指定函式的引數，選擇特定試用期。您可以從 `ML.TRIAL_INFO` 函式的輸出內容取得 `TRIAL_ID`。支援的函式如下：

  + [`ML.CONFUSION_MATRIX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-confusion?hl=zh-tw)
  + [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)
  + [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)
  + [`ML.RECOMMEND`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-recommend?hl=zh-tw)
  + [`ML.ROC_CURVE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-roc?hl=zh-tw)
* 如果函式未採用輸入資料，系統會傳回所有試驗結果，且第一個輸出資料欄為 `TRIAL_ID`。支援的函式如下：

  + [`ML.CENTROIDS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-centroids?hl=zh-tw)
  + [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)
  + [`ML.WEIGHTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-weights?hl=zh-tw)

[`ML.FEATURE_INFO`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-feature?hl=zh-tw) 的輸出內容不會變更，因為所有試驗都會共用相同的輸入資料。

由於輸入資料的分割方式不同，`ML.EVALUATE` 和 `ML.TRIAL_INFO` 的評估指標可能會有所差異。根據預設，`ML.EVALUATE` 會針對測試資料執行，而 `ML.TRIAL_INFO` 則會針對評估資料執行。詳情請參閱[資料分割](#data_split)。

### 不支援的函式

[`ML.TRAINING_INFO` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-train?hl=zh-tw)會傳回每次疊代的資訊，且疊代結果不會儲存在超參數調整模型中。系統會改為儲存試用結果。您可以使用 [`ML.TRIAL_INFO` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-trial-info?hl=zh-tw)取得試驗結果的相關資訊。

## 匯出模型

您可以使用 [`EXPORT MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-export-model?hl=zh-tw)，將透過超參數調整建立的模型匯出至 Cloud Storage 位置。您可以匯出預設最佳試用期，或任何指定的試用期。

## 定價

超參數調整訓練的費用是所有執行試驗的費用總和。試用期間的價格與現有的 [BigQuery ML 定價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)一致。

## 常見問題

本節提供有關超參數調整的常見問題解答。

### 需要多少次試驗才能調整模型？

建議您為每個超參數至少使用 10 次試驗，因此試驗總數應至少為 `10 * num_hyperparameters`。如果您使用預設搜尋空間，請參閱「[超參數和目標](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-hyperparameter-tuning?hl=zh-tw#hyperparameters_and_objectives)」表格中的「超參數」欄，瞭解特定模型類型預設調整的超參數數量。

### 如果使用超參數調整後，成效沒有提升，該怎麼辦？

請務必遵循本文指南，進行公平比較。如果效能仍未提升，可能表示預設超參數已能有效運作。建議您先著重於特徵工程或嘗試其他模型類型，再進行另一輪超參數調整。

### 如果想繼續微調模型，該怎麼做？

使用相同的搜尋空間訓練新的超參數調整模型。內建的遷移學習功能可根據先前微調的模型繼續微調。

### 我是否需要使用所有資料和最佳超參數重新訓練模型？

這取決於下列因素：

* K-means 模型已將所有資料做為訓練資料，因此不需要重新訓練模型。
* 對於矩陣分解模型，您可以選取超參數和所有輸入資料，重新訓練模型，以更全面地涵蓋使用者和項目。
* 如果是其他模型類型，通常不需要重新訓練。在預設的隨機資料分割期間，這項服務已保留 80% 的輸入資料用於訓練。如果資料集很小，您仍可使用更多訓練資料和所選超參數重新訓練模型，但如果留給提早中止訓練的評估資料很少，可能會導致過度配適。

## 後續步驟

* 如要試著執行超參數調整，請參閱「[使用 BigQuery ML 超參數調整來改善模型效能](https://docs.cloud.google.com/bigquery/docs/hyperparameter-tuning-tutorial?hl=zh-tw)」。
* 如要進一步瞭解 ML 模型支援的 SQL 陳述式和函式，請參閱「[ML 模型端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]