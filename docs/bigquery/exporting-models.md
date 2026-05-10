Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 可匯出模型

本頁說明如何匯出 BigQuery ML 模型。您可以將 BigQuery ML 模型匯出至 Cloud Storage，並用於線上預測，或在 Python 中編輯模型。您可以透過下列方式匯出 BigQuery ML 模型：

* 使用[Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw)。
* 使用 [`EXPORT MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-export-model?hl=zh-tw) 陳述式。
* 在 bq 指令列工具中使用 `bq extract` 指令。
* 透過 API 或用戶端程式庫提交 [`extract`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfiguration) 工作。

您可以匯出下列模型類型：

* `AUTOENCODER`
* `AUTOML_CLASSIFIER`
* `AUTOML_REGRESSOR`
* `BOOSTED_TREE_CLASSIFIER`
* `BOOSTED_TREE_REGRESSOR`
* `DNN_CLASSIFIER`
* `DNN_REGRESSOR`
* `DNN_LINEAR_COMBINED_CLASSIFIER`
* `DNN_LINEAR_COMBINED_REGRESSOR`
* `KMEANS`
* `LINEAR_REG`
* `LOGISTIC_REG`
* `MATRIX_FACTORIZATION`
* `RANDOM_FOREST_CLASSIFIER`
* `RANDOM_FOREST_REGRESSOR`
* `TENSORFLOW` (匯入的 TensorFlow 模型)
* `PCA`
* `TRANSFORM_ONLY`

## 匯出模型格式和範例

下表列出各 BigQuery ML 模型類型的匯出目的地格式，並提供寫入 Cloud Storage bucket 的檔案範例。

| 模型類型 | 匯出模型格式 | 匯出檔案範例 |
| --- | --- | --- |
| AUTOML\_CLASSIFIER | [TensorFlow SavedModel](https://www.tensorflow.org/guide/saved_model?hl=zh-tw) (TF 2.1.0) | `gcs_bucket/    assets/      f1.txt      f2.txt    saved_model.pb    variables/      variables.data-00-of-01      variables.index` |
| AUTOML\_REGRESSOR |
| 自動編碼器 | [TensorFlow SavedModel](https://www.tensorflow.org/guide/saved_model?hl=zh-tw) (TF 1.15 以上版本) |
| DNN\_CLASSIFIER |
| DNN\_REGRESSOR |
| DNN\_LINEAR\_COMBINED\_CLASSIFIER |
| DNN\_LINEAR\_COMBINED\_REGRESSOR |
| KMEANS |
| LINEAR\_REGRESSOR |
| LOGISTIC\_REG |
| MATRIX\_FACTORIZATION |
| PCA |
| TRANSFORM\_ONLY |
| BOOSTED\_TREE\_CLASSIFIER | 追加劑 (XGBoost 0.82) | `gcs_bucket/    assets/      0.txt      1.txt      model_metadata.json    main.py    model.bst    xgboost_predictor-0.1.tar.gz      ....       predictor.py      ....`    `main.py` 適用於在本機執行。詳情請參閱「[模型部署](#model-deployment)」。 |
| BOOSTED\_TREE\_REGRESSOR |
| RANDOM\_FOREST\_REGRESSOR |
| RANDOM\_FOREST\_REGRESSOR |
| TENSORFLOW (已匯入) | [TensorFlow SavedModel](https://www.tensorflow.org/guide/saved_model?hl=zh-tw) | 與匯入模型時完全相同的檔案 |

**注意：** 模型建立期間執行的[自動資料前處理](https://docs.cloud.google.com/bigquery/docs/auto-preprocessing?hl=zh-tw) (例如標準化和標籤編碼)，會儲存在匯出檔案中，做為 TensorFlow SavedModel 圖的一部分，並儲存在 Booster 的外部檔案中。將資料傳遞給模型進行預測前，不需要進行明確的預先處理。輸入內容通常應與 BigQuery ML [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw) 使用的內容相符。匯出模型簽章中的所有數值都會轉換為 `FLOAT64` 資料型別。此外，所有 `STRUCT` 欄位都必須展開為個別欄位。舉例來說，`STRUCT f2` 中的 `f1` 欄位應重新命名為 `f2_f1`，並以獨立資料欄的形式傳遞。

## 匯出使用「`TRANSFORM`」訓練的模型

如果模型是使用 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)訓練，則額外的預先處理模型會執行 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)中的相同邏輯，並以 TensorFlow SavedModel 格式儲存於 `transform` 子目錄下。您也可以將使用 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)訓練的模型部署至 Vertex AI 和本機。詳情請參閱[模型部署](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw#model-deployment)。

| 匯出模型格式 | 匯出檔案範例 |
| --- | --- |
| 預測模型：[TensorFlow SavedModel](https://www.tensorflow.org/guide/saved_model?hl=zh-tw) 或 Booster (XGBoost 0.82)。  TRANSFORM 子句的預先處理模型：[TensorFlow SavedModel](https://www.tensorflow.org/guide/saved_model?hl=zh-tw) (TF 2.5 以上版本) | `gcs_bucket/    ....(model files)    transform/      assets/          f1.txt/          f2.txt/      saved_model.pb      variables/          variables.data-00-of-01          variables.index` |

模型不包含在訓練期間於 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)外執行的特徵工程相關資訊。例如 `SELECT` 陳述式中的任何內容。因此，您需要先手動轉換輸入資料，再提供給預先處理模型。

### 支援的資料類型

匯出以 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)訓練的模型時，系統支援下列資料類型，可饋送至 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)。

| TRANSFORM 輸入類型 | TRANSFORM 輸入內容範例 | 匯出的前處理模型輸入樣本 |
| --- | --- | --- |
| INT64 | `10,  11` | `tf.constant(    [10, 11],    dtype=tf.int64)` |
| NUMERIC | `NUMERIC 10,  NUMERIC 11` | `tf.constant(    [10, 11],    dtype=tf.float64)` |
| BIGNUMERIC | `BIGNUMERIC 10,  BIGNUMERIC 11` | `tf.constant(    [10, 11],    dtype=tf.float64)` |
| FLOAT64 | `10.0,  11.0` | `tf.constant(    [10, 11],    dtype=tf.float64)` |
| BOOL | `TRUE,  FALSE` | `tf.constant(    [True, False],    dtype=tf.bool)` |
| STRING | `'abc',  'def'` | `tf.constant(    ['abc', 'def'],    dtype=tf.string)` |
| 位元組 | `b'abc',  b'def'` | `tf.constant(    ['abc', 'def'],    dtype=tf.string)` |
| 日期 | `DATE '2020-09-27',  DATE '2020-09-28'` | `tf.constant(    [      '2020-09-27',      '2020-09-28'    ],    dtype=tf.string)    "%F" format` |
| DATETIME | `DATETIME '2023-02-02 02:02:01.152903',  DATETIME '2023-02-03 02:02:01.152903'` | `tf.constant(    [      '2023-02-02 02:02:01.152903',      '2023-02-03 02:02:01.152903'    ],    dtype=tf.string)    "%F %H:%M:%E6S" format` |
| 時間 | `TIME '16:32:36.152903',  TIME '17:32:36.152903'` | `tf.constant(    [      '16:32:36.152903',      '17:32:36.152903'    ],    dtype=tf.string)    "%H:%M:%E6S" format` |
| 時間戳記 | `TIMESTAMP '2017-02-28 12:30:30.45-08',  TIMESTAMP '2018-02-28 12:30:30.45-08'` | `tf.constant(    [      '2017-02-28 20:30:30.4 +0000',      '2018-02-28 20:30:30.4 +0000'    ],    dtype=tf.string)    "%F %H:%M:%E1S %z" format` |
| ARRAY | `['a', 'b'],  ['c', 'd']` | `tf.constant(    [['a', 'b'], ['c', 'd']],    dtype=tf.string)` |
| ARRAY< STRUCT< INT64, FLOAT64>> | `[(1, 1.0), (2, 1.0)],  [(2, 1.0), (3, 1.0)]` | `tf.sparse.from_dense(    tf.constant(      [        [0, 1.0, 1.0, 0],        [0, 0, 1.0, 1.0]      ],      dtype=tf.float64))` |
| NULL | `NULL,  NULL` | `tf.constant(    [123456789.0e10, 123456789.0e10],    dtype=tf.float64)    tf.constant(    [1234567890000000000, 1234567890000000000],    dtype=tf.int64)    tf.constant(    [' __MISSING__ ', ' __MISSING__ '],    dtype=tf.string)` |

### 支援的 SQL 函式

匯出使用 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)訓練的模型時，可以在 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)中使用下列 SQL 函式。

* [運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw)
  + `+`、`-`、`*`、`/`、`=`、`<`、`>`、`<=`、`>=`、`!=`、`<>`、
    `[NOT] BETWEEN`、`[NOT] IN`、`IS [NOT] NULL`、`IS [NOT] TRUE`、
    `IS [NOT] FALSE`、`NOT`、`AND`、`OR`。
* [條件運算式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw)
  + `CASE expr`、`CASE`、`COALESCE`、`IF`、`IFNULL`、`NULLIF`。
* [數學函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw)
  + `ABS`、`ACOS`、`ACOSH`、`ASINH`、`ATAN`、`ATAN2`、`ATANH`、`CBRT`、`CEIL`、
    `CEILING`、`COS`、`COSH`、`COT`、`COTH`、`CSC`、`CSCH`、`EXP`、`FLOOR`、
    `IS_INF`、`IS_NAN`、`LN`、`LOG`、`LOG10`、`MOD`、`POW`、`POWER`、`SEC`、
    `SECH`、`SIGN`、`SIN`、`SINH`、`SQRT`、`TAN`、`TANH`。
* [轉換函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions?hl=zh-tw)
  + `CAST AS INT64`、`CAST AS FLOAT64`、`CAST AS NUMERIC`、
    `CAST AS BIGNUMERIC`、`CAST AS STRING`、`SAFE_CAST AS INT64`、
    `SAFE_CAST AS FLOAT64`
* [字串函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw)
  + `CONCAT`、`LEFT`、`LENGTH`、`LOWER`、`REGEXP_REPLACE`、`RIGHT`、`SPLIT`、`SUBSTR`、`SUBSTRING`、`TRIM`、`UPPER`。
* [日期函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw)
  + `Date`、`DATE_ADD`、`DATE_SUB`、`DATE_DIFF`、`DATE_TRUNC`、`EXTRACT`、`FORMAT_DATE`、`PARSE_DATE`、`SAFE.PARSE_DATE`。
* [日期時間函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw)
  + `DATETIME`、`DATETIME_ADD`、`DATETIME_SUB`、`DATETIME_DIFF`、`DATETIME_TRUNC`、`EXTRACT`、`PARSE_DATETIME`、`SAFE.PARSE_DATETIME`。
* [時間函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw)
  + `TIME`、`TIME_ADD`、`TIME_SUB`、`TIME_DIFF`、`TIME_TRUNC`、`EXTRACT`、`FORMAT_TIME`、`PARSE_TIME`、`SAFE.PARSE_TIME`。
* [時間戳記函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw)
  + `TIMESTAMP`、`TIMESTAMP_ADD`、`TIMESTAMP_SUB`、`TIMESTAMP_DIFF`、
    `TIMESTAMP_TRUNC`、`FORMAT_TIMESTAMP`、`PARSE_TIMESTAMP`、
    `SAFE.PARSE_TIMESTAMP`、`TIMESTAMP_MICROS`、`TIMESTAMP_MILLIS`、
    `TIMESTAMP_SECONDS`、`EXTRACT`、`STRING`、`UNIX_MICROS`、`UNIX_MILLIS`、
    `UNIX_SECONDS`。
* [手動預先處理函式](https://docs.cloud.google.com/bigquery/docs/manual-preprocessing?hl=zh-tw)
  + `ML.IMPUTER`、`ML.HASH_BUCKETIZE`、`ML.LABEL_ENCODER`、
    `ML.MULTI_HOT_ENCODER`、`ML.NGRAMS`、`ML.ONE_HOT_ENCODER`、`ML.BUCKETIZE`、
    `ML.MAX_ABS_SCALER`、`ML.MIN_MAX_SCALER`、`ML.NORMALIZER`、
    `ML.QUANTILE_BUCKETIZE`、`ML.ROBUST_SCALER`、`ML.STANDARD_SCALER`。

## 限制

匯出模型時，請注意下列限制：

* 如果訓練期間使用下列任何功能，系統就不支援匯出模型：

  + 輸入資料中含有 `ARRAY`、`TIMESTAMP` 或 `GEOGRAPHY` 特徵類型。
* 匯出的 `AUTOML_REGRESSOR` 和 `AUTOML_CLASSIFIER` 類型模型不支援 Vertex AI 部署，無法用於線上預測。
* 匯出矩陣分解模型時，模型大小上限為 1 GB。
  模型大小與 `num_factors` 大致成正比，因此如果達到上限，可以在訓練期間減少 `num_factors`，縮減模型大小。
* 如要瞭解使用 [BigQuery ML `TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)訓練的模型 (用於[手動前處理特徵](https://docs.cloud.google.com/bigquery/docs/manual-preprocessing?hl=zh-tw))，請參閱支援匯出的[資料類型](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw#export-transform-types)和[函式](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw#export-transform-functions)。
* 使用 [BigQuery ML `TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)在 2023 年 9 月 18 日前訓練的模型，必須重新訓練，才能[透過 Model Registry 部署](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw)，以進行線上預測。
* 匯出模型時，系統支援 `ARRAY<STRUCT<INT64, FLOAT64>>`、`ARRAY` 和 `TIMESTAMP` 做為預先轉換的資料，但不支援做為轉換後的資料。

## 匯出 BigQuery ML 模型

如要匯出模型，請選取下列其中一個選項：

### 控制台

1. 在 Google Cloud 控制台開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
4. 依序點選「總覽」**>「模型」**，然後點選要匯出的模型名稱。
5. 依序按一下「更多」**>「匯出」**：
6. 在「Export model to Google Cloud Storage」(將模型匯出至 Google Cloud Storage) 對話方塊中：

   * 在「選取 GCS 位置」中，瀏覽至要匯出模型的值區或資料夾位置，然後按一下「選取」。
   * 按一下「提交」即可匯出模型。

如要查看工作進度，請在「Explorer」窗格中按一下「Job history」，然後尋找「EXTRACT」類型的工作。

### SQL

您可以使用 `EXPORT MODEL` 陳述式，透過 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql?hl=zh-tw) 查詢語法，將 BigQuery ML 模型匯出至 [Cloud Storage](https://docs.cloud.google.com/storage/docs?hl=zh-tw)。

如要在 Google Cloud 控制台中使用 `EXPORT MODEL` 陳述式匯出 BigQuery ML 模型，請按照下列步驟操作：

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 [Compose new query] (撰寫新查詢)。
3. 在「Query editor」(查詢編輯器) 欄位中，輸入 [`EXPORT MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-export-model?hl=zh-tw) 陳述式。

   [URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri) 為 `gs://bucket/path/to/saved_model/` 的 Cloud Storage 值區。

   ```
    EXPORT MODEL `myproject.mydataset.mymodel`
    OPTIONS(URI = 'gs://bucket/path/to/saved_model/')
   ```
4. 按一下「執行」。查詢完成時，「查詢結果」窗格會顯示 `Successfully exported model`。

### bq

**注意：** 如要使用 bq 指令列工具匯出模型，您必須具備 bq 指令列工具 2.0.56 以上版本，該工具隨附於 gcloud CLI [287.0.0 以上版本](https://docs.cloud.google.com/sdk/docs/release-notes?hl=zh-tw#28700_2020-04-01)。如要查看已安裝的 bq 工具版本，請使用 [`bq version`](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#getting_help)，並視需要使用 [`gcloud components update`](https://docs.cloud.google.com/sdk/gcloud/reference/components/update?hl=zh-tw) 更新 gcloud CLI。

請使用 `bq extract` 指令，並加上 `--model` 旗標。

(選用) 提供 `--destination_format` 旗標，並選擇匯出模型的格式。(選用) 加上 `--location` 旗標，並將該旗標值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

```
bq --location=location extract \
--destination_format format \
--model project_id:dataset.model \
gs://bucket/model_folder
```

其中：

* location 是您的位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)，設定該位置的預設值。
* destination\_format 是匯出模型的格式：`ML_TF_SAVED_MODEL` (預設) 或 `ML_XGBOOST_BOOSTER`。
* project\_id 是您的專案 ID。
* dataset 是來源資料集的名稱。
* model 是您要匯出的模型。
* bucket 是匯出資料的目標 Cloud Storage 值區名稱。BigQuery 資料集與 Cloud Storage 值區必須位於相同的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
* model\_folder 是要寫入匯出模型檔案的資料夾名稱。

範例：

舉例來說，下列指令會將 TensorFlow SavedModel 格式的 `mydataset.mymodel` 匯出至名為 `mymodel_folder` 的 Cloud Storage bucket。

```
bq extract --model \
'mydataset.mymodel' \
gs://example-bucket/mymodel_folder
```

destination\_format 的預設值為 `ML_TF_SAVED_MODEL`。

下列指令會以 XGBoost Booster 格式將 `mydataset.mymodel` 匯出至名為 `mymodel_folder` 的 Cloud Storage bucket。

```
bq extract --model \
--destination_format ML_XGBOOST_BOOSTER \
'mydataset.mytable' \
gs://example-bucket/mymodel_folder
```

### API

如要匯出模型，請建立 `extract` 工作，並填入工作設定。

(選用) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性內指定您的位置。

1. 建立指向 BigQuery ML 模型和 Cloud Storage 目的地的擷取工作。
2. 指定來源模型，方法是使用包含專案 ID、資料集 ID 和模型 ID 的 `sourceModel` 設定物件。
3. `destination URI(s)` 屬性必須是完整的，且必須符合下列格式：gs://bucket/model\_folder。
4. 設定 `configuration.extract.destinationFormat` 屬性以指定目的地格式。舉例來說，如要匯出升級樹狀結構模型，請將此屬性值設為 `ML_XGBOOST_BOOSTER`。
5. 如要查看工作狀態，請利用初始要求所傳回的工作 ID 來呼叫 [jobs.get(job\_id)](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/get?hl=zh-tw)。

   * 如果是 `status.state = DONE`，代表工作已順利完成。
   * 如果出現 `status.errorResult` 屬性，代表要求執行失敗，且該物件將包含所發生錯誤的相關訊息。
   * 如果沒有出現 `status.errorResult`，代表工作已順利完成，但過程中可能發生了幾個不嚴重的錯誤。非致命錯誤都會列在已傳回工作物件的 `status.errors` 屬性中。

**API 附註：**

* 最佳做法就是產生唯一識別碼，並在呼叫 `jobs.insert` 來建立工作時，將該唯一識別碼當做 `jobReference.jobId` 傳送。這個方法較不受網路故障問題的影響，因為用戶端可使用已知的工作 ID 進行輪詢或重試。
* 針對指定的工作 ID 呼叫 `jobs.insert` 算是種冪等運算；換句話說，您可以針對同一個工作 ID 重試作業無數次，但在這些作業中最多只會有一個成功。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.ExtractJobConfiguration;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.ModelId;

// Sample to extract model to GCS bucket
public class ExtractModel {

  public static void main(String[] args) throws InterruptedException {
    // TODO(developer): Replace these variables before running the sample.
    String projectName = "bigquery-public-data";
    String datasetName = "samples";
    String modelName = "model";
    String bucketName = "MY-BUCKET-NAME";
    String destinationUri = "gs://" + bucketName + "/path/to/file";
    extractModel(projectName, datasetName, modelName, destinationUri);
  }

  public static void extractModel(
      String projectName, String datasetName, String modelName, String destinationUri)
      throws InterruptedException {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      ModelId modelId = ModelId.of(projectName, datasetName, modelName);

      ExtractJobConfiguration extractConfig =
          ExtractJobConfiguration.newBuilder(modelId, destinationUri).build();

      Job job = bigquery.create(JobInfo.of(extractConfig));

      // Blocks until this job completes its execution, either failing or succeeding.
      Job completedJob = job.waitFor();
      if (completedJob == null) {
        System.out.println("Job not executed since it no longer exists.");
        return;
      } else if (completedJob.getStatus().getError() != null) {
        System.out.println(
            "BigQuery was unable to extract due to an error: \n" + job.getStatus().getError());
        return;
      }
      System.out.println("Model extract successful");
    } catch (BigQueryException ex) {
      System.out.println("Model extraction job was interrupted. \n" + ex.toString());
    }
  }
}
```

## 模型部署

您可以將匯出的模型部署至 Vertex AI 和本機。如果模型的 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)包含日期函式、日期時間函式、時間函式或時間戳記函式，您必須在容器中使用 [bigquery-ml-utils 程式庫](https://pypi.org/project/bigquery-ml-utils/)。但如果您是[透過 Model Registry 部署](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw)，則不需要匯出模型或提供模型的容器。

### Vertex AI 部署作業

| 匯出模型格式 | 部署 |
| --- | --- |
| TensorFlow SavedModel (非 AutoML 模型) | [部署 TensorFlow SavedModel](https://docs.cloud.google.com/vertex-ai/docs/general/deployment?hl=zh-tw)。 您必須使用 [支援的 TensorFlow 版本](https://docs.cloud.google.com/vertex-ai/docs/supported-frameworks-list?hl=zh-tw#tensorflow)建立 SavedModel 檔案。 |
| TensorFlow SavedModel (AutoML 模型) | 不支援。 |
| XGBoost Booster | 使用[自訂預測處理常式](https://docs.cloud.google.com/vertex-ai/docs/predictions/custom-prediction-routines?hl=zh-tw)。如果是 XGBoost Booster 模型，預先處理和事後處理資訊會儲存在匯出的檔案中，而自訂預測處理常式可讓您部署模型和額外匯出的檔案。   您必須使用[支援的 XGBoost 版本](https://docs.cloud.google.com/vertex-ai/docs/supported-frameworks-list?hl=zh-tw#xgboost_2)建立模型檔案。 |

### 地端部署作業

| 匯出模型格式 | 部署 |
| --- | --- |
| TensorFlow SavedModel (非 AutoML 模型) | SavedModel 是標準格式，您可以在 [TensorFlow Serving Docker 容器](https://www.tensorflow.org/tfx/serving/serving_basic?hl=zh-tw)中部署模型。  您也可以運用 Vertex AI Online Prediction 的[本機執行](https://docs.cloud.google.com/vertex-ai/docs/training/containerize-run-code-local?hl=zh-tw)功能。 |
| TensorFlow SavedModel (AutoML 模型) | [將模型容器化並執行](https://docs.cloud.google.com/vertex-ai/docs/training/containerize-run-code-local?hl=zh-tw)。 |
| XGBoost Booster | 如要在本機執行 XGBoost Booster 模型，可以使用匯出的 `main.py` 檔案：  1. 將 Cloud Storage 中的所有檔案下載至本機目錄。 2. 將 `xgboost_predictor-0.1.tar.gz` 中的 `predictor.py` 檔案解壓縮至本機目錄。 3. 執行 `main.py` (請參閱 `main.py` 中的操作說明)。 |

## 預測輸出格式

本節提供各模型類型的預測輸出格式。所有匯出的模型都支援批次預測，可一次處理多個輸入資料列。舉例來說，在下列輸出格式範例中，每個範例都有兩個輸入列。

### 自動編碼器

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +------------------------+------------------------+------------------------+ |      LATENT_COL_1      |      LATENT_COL_2      |           ...          | +------------------------+------------------------+------------------------+ |       [FLOAT]          |         [FLOAT]        |           ...          | +------------------------+------------------------+------------------------+ ``` | ``` +------------------+------------------+------------------+------------------+ |   LATENT_COL_1   |   LATENT_COL_2   |   LATENT_COL_3   |   LATENT_COL_4   | +------------------------+------------+------------------+------------------+ |    0.21384512    |    0.93457112    |    0.64978097    |    0.00480489    | +------------------+------------------+------------------+------------------+ ``` |

### AUTOML\_CLASSIFIER

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +------------------------------------------+ | predictions                              | +------------------------------------------+ | [{"scores":[FLOAT], "classes":[STRING]}] | +------------------------------------------+ ``` | ``` +---------------------------------------------+ | predictions                                 | +---------------------------------------------+ | [{"scores":[1, 2], "classes":['a', 'b']},   | |  {"scores":[3, 0.2], "classes":['a', 'b']}] | +---------------------------------------------+ ``` |
|

### AUTOML\_REGRESSOR

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +-----------------+ | predictions     | +-----------------+ | [FLOAT]         | +-----------------+ ``` | ``` +-----------------+ | predictions     | +-----------------+ | [1.8, 2.46]     | +-----------------+ ``` |

### BOOSTED\_TREE\_CLASSIFIER 和 RANDOM\_FOREST\_CLASSIFIER

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +-------------+--------------+-----------------+ | LABEL_PROBS | LABEL_VALUES | PREDICTED_LABEL | +-------------+--------------+-----------------+ | [FLOAT]     | [STRING]     | STRING          | +-------------+--------------+-----------------+ ``` | ``` +-------------+--------------+-----------------+ | LABEL_PROBS | LABEL_VALUES | PREDICTED_LABEL | +-------------+--------------+-----------------+ | [0.1, 0.9]  | ['a', 'b']   | ['b']           | +-------------+--------------+-----------------+ | [0.8, 0.2]  | ['a', 'b']   | ['a']           | +-------------+--------------+-----------------+ ``` |

### BOOSTED\_TREE\_REGRESSOR 和 RANDOM\_FOREST\_REGRESSOR

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +-----------------+ | predicted_label | +-----------------+ | FLOAT           | +-----------------+ ``` | ``` +-----------------+ | predicted_label | +-----------------+ | [1.8]           | +-----------------+ | [2.46]          | +-----------------+ ``` |

### DNN\_CLASSIFIER

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +---------------+-------------+-----------+---------+------------------------+--------+---------------+ | ALL_CLASS_IDS | ALL_CLASSES | CLASS_IDS | CLASSES | LOGISTIC (binary only) | LOGITS | PROBABILITIES | +---------------+-------------+-----------+---------+------------------------+--------+---------------+ | [INT64]       | [STRING]    | INT64     | STRING  | FLOAT                  | [FLOAT]| [FLOAT]       | +---------------+-------------+-----------+---------+------------------------+--------+---------------+ ``` | ``` +---------------+-------------+-----------+---------+------------------------+--------+---------------+ | ALL_CLASS_IDS | ALL_CLASSES | CLASS_IDS | CLASSES | LOGISTIC (binary only) | LOGITS | PROBABILITIES | +---------------+-------------+-----------+---------+------------------------+--------+---------------+ | [0, 1]        | ['a', 'b']  | [0]       | ['a']   | [0.36]                 | [-0.53]| [0.64, 0.36]  | +---------------+-------------+-----------+---------+------------------------+--------+---------------+ | [0, 1]        | ['a', 'b']  | [0]       | ['a']   | [0.2]                  | [-1.38]| [0.8, 0.2]    | +---------------+-------------+-----------+---------+------------------------+--------+---------------+ ``` |

### DNN\_REGRESSOR

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +-----------------+ | PREDICTED_LABEL | +-----------------+ | FLOAT           | +-----------------+ ``` | ``` +-----------------+ | PREDICTED_LABEL | +-----------------+ | [1.8]           | +-----------------+ | [2.46]          | +-----------------+ ``` |

### DNN\_LINEAR\_COMBINED\_CLASSIFIER

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +---------------+-------------+-----------+---------+------------------------+--------+---------------+ | ALL_CLASS_IDS | ALL_CLASSES | CLASS_IDS | CLASSES | LOGISTIC (binary only) | LOGITS | PROBABILITIES | +---------------+-------------+-----------+---------+------------------------+--------+---------------+ | [INT64]       | [STRING]    | INT64     | STRING  | FLOAT                  | [FLOAT]| [FLOAT]       | +---------------+-------------+-----------+---------+------------------------+--------+---------------+ ``` | ``` +---------------+-------------+-----------+---------+------------------------+--------+---------------+ | ALL_CLASS_IDS | ALL_CLASSES | CLASS_IDS | CLASSES | LOGISTIC (binary only) | LOGITS | PROBABILITIES | +---------------+-------------+-----------+---------+------------------------+--------+---------------+ | [0, 1]        | ['a', 'b']  | [0]       | ['a']   | [0.36]                 | [-0.53]| [0.64, 0.36]  | +---------------+-------------+-----------+---------+------------------------+--------+---------------+ | [0, 1]        | ['a', 'b']  | [0]       | ['a']   | [0.2]                  | [-1.38]| [0.8, 0.2]    | +---------------+-------------+-----------+---------+------------------------+--------+---------------+ ``` |

### DNN\_LINEAR\_COMBINED\_REGRESSOR

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +-----------------+ | PREDICTED_LABEL | +-----------------+ | FLOAT           | +-----------------+ ``` | ``` +-----------------+ | PREDICTED_LABEL | +-----------------+ | [1.8]           | +-----------------+ | [2.46]          | +-----------------+ ``` |

### KMEANS

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +--------------------+--------------+---------------------+ | CENTROID_DISTANCES | CENTROID_IDS | NEAREST_CENTROID_ID | +--------------------+--------------+---------------------+ | [FLOAT]            | [INT64]      | INT64               | +--------------------+--------------+---------------------+ ``` | ``` +--------------------+--------------+---------------------+ | CENTROID_DISTANCES | CENTROID_IDS | NEAREST_CENTROID_ID | +--------------------+--------------+---------------------+ | [1.2, 1.3]         | [1, 2]       | [1]                 | +--------------------+--------------+---------------------+ | [0.4, 0.1]         | [1, 2]       | [2]                 | +--------------------+--------------+---------------------+ ``` |

### LINEAR\_REG

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +-----------------+ | PREDICTED_LABEL | +-----------------+ | FLOAT           | +-----------------+ ``` | ``` +-----------------+ | PREDICTED_LABEL | +-----------------+ | [1.8]           | +-----------------+ | [2.46]          | +-----------------+ ``` |

### LOGISTIC\_REG

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +-------------+--------------+-----------------+ | LABEL_PROBS | LABEL_VALUES | PREDICTED_LABEL | +-------------+--------------+-----------------+ | [FLOAT]     | [STRING]     | STRING          | +-------------+--------------+-----------------+ ``` | ``` +-------------+--------------+-----------------+ | LABEL_PROBS | LABEL_VALUES | PREDICTED_LABEL | +-------------+--------------+-----------------+ | [0.1, 0.9]  | ['a', 'b']   | ['b']           | +-------------+--------------+-----------------+ | [0.8, 0.2]  | ['a', 'b']   | ['a']           | +-------------+--------------+-----------------+ ``` |

### MATRIX\_FACTORIZATION

**注意：**我們僅支援輸入使用者，並輸出前 50 個 (predicted\_rating、predicted\_item) 配對，並依 predicted\_rating 降序排序。

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +--------------------+--------------+ | PREDICTED_RATING | PREDICTED_ITEM | +------------------+----------------+ | [FLOAT]          | [STRING]       | +------------------+----------------+ ``` | ``` +--------------------+--------------+ | PREDICTED_RATING | PREDICTED_ITEM | +------------------+----------------+ | [5.5, 1.7]       | ['A', 'B']     | +------------------+----------------+ | [7.2, 2.7]       | ['B', 'A']     | +------------------+----------------+ ``` |

### TENSORFLOW (已匯入)

| 預測輸出格式 |
| --- |
| 與匯入的模型相同 |

### PCA

| 預測輸出格式 | 輸出範例 |
| --- | --- |
| ``` +-------------------------+---------------------------------+ | PRINCIPAL_COMPONENT_IDS | PRINCIPAL_COMPONENT_PROJECTIONS | +-------------------------+---------------------------------+ |       [INT64]           |             [FLOAT]             | +-------------------------+---------------------------------+ ``` | ``` +-------------------------+---------------------------------+ | PRINCIPAL_COMPONENT_IDS | PRINCIPAL_COMPONENT_PROJECTIONS | +-------------------------+---------------------------------+ |       [1, 2]            |             [1.2, 5.0]          | +-------------------------+---------------------------------+ ``` |

### TRANSFORM\_ONLY

| 預測輸出格式 |
| --- |
| 與模型 `TRANSFORM` 子句中指定的資料欄相同 |

## XGBoost 模型視覺化

模型匯出後，您可以使用 [plot\_tree](https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.plot_tree) Python API，以視覺化方式呈現提升樹狀結構。舉例來說，您可以在不安裝依附元件的情況下使用 [Colab](https://colab.research.google.com/?hl=zh-tw)：

1. 將升級樹狀結構模型匯出至 Cloud Storage bucket。
2. 從 Cloud Storage bucket 下載 `model.bst` 檔案。
3. 在 [Colab 筆記本](https://colab.sandbox.google.com/notebooks/welcome.ipynb?hl=zh-tw)中，將 `model.bst` 檔案上傳至 `Files`。
4. 在筆記本中執行下列程式碼：

   ```
   import xgboost as xgb
   import matplotlib.pyplot as plt

   model = xgb.Booster(model_file="model.bst")
   num_iterations = <iteration_number>
   for tree_num in range(num_iterations):
     xgb.plot_tree(model, num_trees=tree_num)
   plt.show
   ```

這個範例會繪製多個樹狀結構 (每次疊代一個樹狀結構)：

**注意：** 我們會使用標籤編碼器編碼類別特徵，因此您可以從模型匯出 Cloud Storage bucket 內「assets/」目錄中的詞彙檔案，取得分割值的對應類別。舉例來說，如果節點中顯示「f0 < 2.95」，您可以尋找第 3 個項目，在詞彙檔案中找出對應的類別。

我們不會在模型中儲存特徵名稱，因此您會看到「f0」、「f1」等名稱。您可以使用這些名稱 (例如「f0」) 做為索引，在`assets/model_metadata.json`匯出檔案中找到對應的特徵名稱。

## 所需權限

如要將 BigQuery ML 模型匯出至 Cloud Storage，您必須擁有存取 BigQuery ML 模型的權限、執行擷取工作的權限，以及將資料寫入 Cloud Storage bucket 的權限。

**BigQuery 權限**

* 您至少必須擁有 `bigquery.models.export` 權限，才能匯出模型。以下是擁有 `bigquery.models.export` 權限的預先定義 Identity and Access Management (IAM) 角色：

  + `bigquery.dataViewer`
  + `bigquery.dataOwner`
  + `bigquery.dataEditor`
  + `bigquery.admin`
* 您至少必須擁有 `bigquery.jobs.create` 權限，才能執行匯出[工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)。以下是擁有 `bigquery.jobs.create` 權限的預先定義 IAM 角色：

  + `bigquery.user`
  + `bigquery.jobUser`
  + `bigquery.admin`

**Cloud Storage 權限**

* 如要將資料寫入現有的 Cloud Storage 值區，您必須擁有 `storage.objects.create` 權限。以下是擁有 `storage.objects.create` 權限的預先定義 IAM 角色：

  + `storage.objectCreator`
  + `storage.objectAdmin`
  + `storage.admin`

如要進一步瞭解 BigQuery ML 中的 IAM 角色和權限，請參閱[存取權控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

## 在不同位置之間移動 BigQuery 資料

資料集建立之後，即無法更改位置，但您可以[建立資料集副本](https://docs.cloud.google.com/bigquery/docs/copying-datasets?hl=zh-tw)。

## 配額政策

如要瞭解擷取工作配額，請參閱「配額與限制」頁面的[擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)一節。

## 定價

匯出 BigQuery ML 模型不需付費，但匯出作業會受限於 BigQuery 的[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。如要進一步瞭解 BigQuery 定價，請參閱[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面。

匯出資料之後，系統會因您在 Cloud Storage 中儲存資料而向您收取費用。如要進一步瞭解 Cloud Storage 的計價方式，請參閱 Cloud Storage [定價](https://cloud.google.com/storage/pricing?hl=zh-tw)頁面。

## 後續步驟

* 逐步完成「[匯出 BigQuery ML 模型以進行線上預測](https://docs.cloud.google.com/bigquery/docs/export-model-tutorial?hl=zh-tw)」教學課程。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]