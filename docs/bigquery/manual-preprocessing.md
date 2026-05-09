Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 手動預先處理特徵

您可以搭配使用 `CREATE MODEL` 陳述式的 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#transform)和手動前處理函式，定義自訂資料前處理作業。您也可以在 `TRANSFORM` 子句以外的地方使用這些手動前處理函式。

如要將資料預先處理作業與模型訓練作業分離，可以使用 `TRANSFORM` 子句建立[僅轉換模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-transform?hl=zh-tw)，只執行資料轉換作業。

您可以使用 [`ML.TRANSFORM` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-transform?hl=zh-tw)，提高特徵前處理的透明度。這個函式可讓您從模型的 `TRANSFORM` 子句傳回預先處理的資料，以便查看模型訓練的實際訓練資料，以及提供模型的實際預測資料。

如要瞭解 BigQuery ML 的特徵預先處理支援，請參閱[特徵預先處理總覽](https://docs.cloud.google.com/bigquery/docs/preprocess-overview?hl=zh-tw)。

## 預先處理函式類型

手動預先處理函式分為幾種類型：

* 純量函式會對單一資料列執行運算。例如：[`ML.BUCKETIZE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-bucketize?hl=zh-tw)。
* 資料表值函式會處理所有資料列，並輸出資料表。例如：[`ML.FEATURES_AT_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-feature-time?hl=zh-tw)。
* 分析函式會對所有資料列執行運算，並根據所有資料列收集的統計資料，輸出每個資料列的結果。例如：[`ML.QUANTILE_BUCKETIZE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-quantile-bucketize?hl=zh-tw)。

  使用 ML 分析函式時，一律須搭配空白的 `OVER()` 子句。

  在訓練期間，如果您在 `TRANSFORM` 子句中使用 ML 分析函式，系統會自動將相同的統計資料套用至預測中的輸入內容。

以下各節說明可用的前處理函式。

### 一般函式

在字串或數值運算式上使用下列函式，即可清除資料：

* [`ML.IMPUTER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-imputer?hl=zh-tw)

### 數值函式

您可以在數值運算式中使用下列函式，將資料正規化：

* [`ML.BUCKETIZE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-bucketize?hl=zh-tw)
* [`ML.MAX_ABS_SCALER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-max-abs-scaler?hl=zh-tw)
* [`ML.MIN_MAX_SCALER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-min-max-scaler?hl=zh-tw)
* [`ML.NORMALIZER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-normalizer?hl=zh-tw)
* [`ML.POLYNOMIAL_EXPAND`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-polynomial-expand?hl=zh-tw)
* [`ML.QUANTILE_BUCKETIZE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-quantile-bucketize?hl=zh-tw)
* [`ML.ROBUST_SCALER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-robust-scaler?hl=zh-tw)
* [`ML.STANDARD_SCALER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-standard-scaler?hl=zh-tw)

### 類別函式

您可以在類別型資料上使用下列函式：

* [`ML.FEATURE_CROSS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-feature-cross?hl=zh-tw)
* [`ML.HASH_BUCKETIZE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-hash-bucketize?hl=zh-tw)
* [`ML.LABEL_ENCODER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-label-encoder?hl=zh-tw)
* [`ML.MULTI_HOT_ENCODER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-multi-hot-encoder?hl=zh-tw)
* [`ML.ONE_HOT_ENCODER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-one-hot-encoder?hl=zh-tw)

### 文字函式

您可以在文字字串運算式中使用下列函式：

* [`ML.NGRAMS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ngrams?hl=zh-tw)
* [`ML.BAG_OF_WORDS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-bag-of-words?hl=zh-tw)
* [`ML.TF_IDF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-tf-idf?hl=zh-tw)

### 圖片功能

在圖片資料上使用下列函式：

* [`ML.CONVERT_COLOR_SPACE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-convert-color-space?hl=zh-tw)
* [`ML.CONVERT_IMAGE_TYPE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-convert-image-type?hl=zh-tw)
* [`ML.DECODE_IMAGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-decode-image?hl=zh-tw)
* [`ML.RESIZE_IMAGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-resize-image?hl=zh-tw)

## 已知限制

* BigQuery ML 支援[模型匯出](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw)中的自動前處理和手動前處理。如要匯出使用 [BigQuery ML `TRANSFORM` 子句訓練的模型，請參閱[支援的資料類型](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw#export-transform-types)和[函式](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw#export-transform-functions)。](https://docs.cloud.google.com/bigquery/docs/bigqueryml-transform?hl=zh-tw)

## 後續步驟

如要進一步瞭解支援手動特徵前處理的模型適用的 SQL 陳述式和函式，請參閱下列文件：

* [機器學習模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)
* [貢獻分析使用者歷程](https://docs.cloud.google.com/bigquery/docs/contribution-analysis?hl=zh-tw#contribution_analysis_user_journey)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]