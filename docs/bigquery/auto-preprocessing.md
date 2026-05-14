Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 自動預先處理特徵

BigQuery ML 會在訓練期間使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)，自動執行前處理作業。自動前處理包含[遺漏值插補](https://docs.cloud.google.com/bigquery/docs/auto-preprocessing?hl=zh-tw#imputation)和[特徵轉換](https://docs.cloud.google.com/bigquery/docs/auto-preprocessing?hl=zh-tw#feature-transform)。

如要瞭解 BigQuery ML 的特徵前處理支援功能，請參閱「[特徵前處理總覽](https://docs.cloud.google.com/bigquery/docs/preprocess-overview?hl=zh-tw)」。

## 遺漏資料插補

在統計學中，插補法是指以替代值取代遺漏資料的一種機制。當您使用 BigQuery ML 訓練模型時，系統會將 `NULL` 值視為遺漏資料。當您透過 BigQuery ML 預測結果時，如果 BigQuery ML 發現 `NULL` 值或從未出現的值，結果中就可能會出現遺漏值。BigQuery ML 會根據資料欄中的資料類型，以不同方式處理遺漏資料。

| 資料欄類型 | 插補方法 |
| --- | --- |
| 數字 | 在訓練和預測中，數值資料欄的 `NULL` 值會替換為原始輸入資料中的特徵欄所計算出的平均值。 |
| one-hot/multi-hot 編碼 | 在訓練和預測中，編碼資料欄的 `NULL` 值會對應至新增至資料的額外類別。在預測期間，如果有之前沒出現過的資料，系統指派的權重值會是 0。 |
| `TIMESTAMP` | `TIMESTAMP` 資料欄混用經過標準化和 one-hot 編碼資料欄的插補方法。針對產生的 Unix 時間資料欄，BigQuery ML 會將值替換為原始資料欄的平均 Unix 時間。針對其他產生的值，BigQuery ML 會為每個擷取的特徵指派相應的 `NULL` 類別。 |
| `STRUCT` | 在訓練和預測期間，系統會根據 `STRUCT` 的類型，推斷每個欄位的值。 |

## 特徵轉換

根據預設，BigQuery ML 會將輸入特徵轉換成下列格式：

| 輸入資料類型 | 轉換方法 | 說明 |
| --- | --- | --- |
| [`INT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types)  [`NUMERIC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_type)  [`BIGNUMERIC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#bignumeric_type)  [`FLOAT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#floating_point_types) | [標準化](https://en.wikipedia.org/wiki/Feature_scaling#Standardization) | 對於大多數模型，BigQuery ML 會將數值資料欄標準化，並將零值的資料欄置中後再傳送至訓練。但有例外情況，即提升樹狀結構和隨機森林模型，這兩種模型不會進行任何標準化，而 k-means 模型則會根據 `STANDARDIZE_FEATURES` 選項，決定是否要標準化數值特徵。 |
| [`BOOL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#boolean_type)  [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#string_type)  [`BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#bytes_type)  [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type)  [`DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#datetime_type)  [`TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_type) | [經過 one-hot 編碼](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#one-hot_encoding) | 針對 `TIMESTAMP` 以外的所有非數值、非陣列資料欄，BigQuery ML 會對所有模型執行 one-hot 編碼轉換，但提升樹狀結構和隨機森林模型除外。這種轉換方式會為資料欄中的每個不重複值產生一個獨立特徵。標籤編碼轉換作業會用於訓練提升樹狀結構和隨機森林模型，將每個不重複值轉換為數值。 |
| [`ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type) | 經過 multi-hot 編碼 | 針對所有非數值 `ARRAY` 資料欄，BigQuery ML 會執行 multi-hot 編碼轉換。這種轉換方式會為 `ARRAY` 中的每個不重複元素產生一個獨立特徵。 |
| [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type) | 時間戳記轉換 | 當線性或邏輯迴歸模型遇到 `TIMESTAMP` 資料欄時，會從 `TIMESTAMP` 擷取一組元件，並對擷取的元件執行標準化和 one-hot 編碼。針對 Unix 紀元時間 (秒) 元件，BigQuery ML 會使用標準化。所有其他元件則使用 one-hot 編碼。   詳情請參閱下列[時間戳記特徵轉換表](https://docs.cloud.google.com/bigquery/docs/auto-preprocessing?hl=zh-tw#timestamp-transform)。 |
| [`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type) | 結構擴充 | 當 BigQuery ML 遇到 `STRUCT` 資料欄時，會展開 `STRUCT` 內的欄位，建立單一資料欄。這項功能需要為 `STRUCT` 的所有欄位命名。不允許巢狀結構的 `STRUCT`。展開後的資料欄名稱格式為 `{struct_name}_{field_name}`。 |
| 第 [`ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type) 列，共 [`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type) 列 | 沒有轉換 |  |
| 第 [`ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type) 列，共 [`NUMERIC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_types) 列 | 沒有轉換 |  |

### `TIMESTAMP` 特徵轉換

下表顯示從 `TIMESTAMP` 欄擷取的元件，以及對應的轉換方法。

| `TIMESTAMP` 元件 | `processed_input` 筆結果 | 轉換方法 |
| --- | --- | --- |
| 以秒為單位的 Unix Epoch 紀元時間 | `[COLUMN_NAME]` | 標準化 |
| 當月第幾日 | `_TS_DOM_[COLUMN_NAME]` | one-hot 編碼 |
| 星期幾 | `_TS_DOW_[COLUMN_NAME]` | one-hot 編碼 |
| 月份 | `_TS_MOY_[COLUMN_NAME]` | one-hot 編碼 |
| 時段 | `_TS_HOD_[COLUMN_NAME]` | one-hot 編碼 |
| 每小時中的某分鐘 | `_TS_MOH_[COLUMN_NAME]` | one-hot 編碼 |
| 年度第幾週 (週日是一週的開始) | `_TS_WOY_[COLUMN_NAME]` | one-hot 編碼 |
| 年份 | `_TS_YEAR_[COLUMN_NAME]` | one-hot 編碼 |

## 類別特徵編碼

如要為經過單熱編碼的特徵指定其他預設編碼方法，請使用模型選項 `CATEGORY_ENCODING_METHOD`。對於廣義線性模型 (GLM) 模型，您可以將 `CATEGORY_ENCODING_METHOD` 設為下列其中一個值：

* [`ONE_HOT_ENCODING`](#one_hot_encoding)
* [`DUMMY_ENCODING`](#dummy_encoding)
* [`LABEL_ENCODING`](#label_encoding)
* [`TARGET_ENCODING`](#dummy_encoding)

### one-hot 編碼

One-hot 編碼會將特徵的每個類別對應至各自的二進位特徵，其中 `0` 代表特徵不存在，`1` 代表特徵存在 (稱為*虛擬變數*)。這項對應會建立 `N` 個新的特徵資料欄，其中 `N` 是訓練資料表中特徵的不重複類別數量。

舉例來說，假設訓練資料表有名為 `fruit` 的特徵資料欄，且包含 `Apple`、`Banana` 和 `Cranberry` 類別，如下所示：

| 列 | 水果 |
| --- | --- |
| 1 | Apple |
| 2 | 香蕉黃 |
| 3 | 蔓越莓 |

在此情況下，`CATEGORY_ENCODING_METHOD='ONE_HOT_ENCODING'` 選項會將資料表轉換為下列內部表示法：

| 列 | fruit\_Apple | fruit\_Banana | fruit\_Cranberry |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 0 |
| 2 | 0 | 1 | 0 |
| 3 | 0 | 0 | 1 |

[線性迴歸和邏輯迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)以及[提升樹狀結構](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)模型支援 one-hot 編碼。

### 虛擬編碼

[虛擬編碼](https://en.wikiversity.org/wiki/Dummy_variable_(statistics))與 one-hot 編碼類似，都是將類別特徵轉換為一組預留位置變數。虛擬編碼會使用 `N-1` 預留位置變數，而不是 `N` 預留位置變數，代表某項功能的 `N` 類別。舉例來說，如果您將 `CATEGORY_ENCODING_METHOD` 設為 `'DUMMY_ENCODING'`，用於前一個熱編碼範例中顯示的相同 `fruit` 特徵資料欄，則資料表會轉換為下列內部表示法：

| 列 | fruit\_Apple | fruit\_Banana |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 0 | 1 |
| 3 | 0 | 0 |

系統會捨棄訓練資料集中出現次數最多的類別。如果多個類別的出現次數最多，系統會從該組類別中隨機捨棄一個。

最終權重集 ([`ML.WEIGHTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-weights?hl=zh-tw)) 仍會包含已捨棄的類別，但其權重一律為 `0.0`。對於 [`ML.ADVANCED_WEIGHTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-advanced-weights?hl=zh-tw)，已捨棄變數的標準誤差和 p 值為 `NaN`。

如果對最初使用 `'DUMMY_ENCODING'` 訓練的模型使用 `warm_start`，系統會從第一次訓練執行中捨棄相同的預留位置變數。模型無法在訓練期間變更編碼方法。

[線性迴歸和邏輯迴歸模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)支援虛擬編碼。

### 標籤編碼

標籤編碼會將類別特徵的值轉換為 `INT64` 值 (以 `[0, <number of categories>]` 為單位)。

舉例來說，假設您有下列書籍資料集：

| 標題 | 類型 |
| --- | --- |
| 書籍 1 | 奇幻 |
| 書籍 2 | 烹飪 |
| 書籍 3 | 記錄 |
| Book 4 | 烹飪 |

編碼後的標籤值可能如下所示：

| 標題 | 類型 (文字) | 類型 (數字) |
| --- | --- | --- |
| 書籍 1 | 奇幻 | 1 |
| 書籍 2 | 烹飪 | 2 |
| 書籍 3 | 記錄 | 3 |
| Book 4 | 烹飪 | 2 |

編碼字彙會依字母順序排序。不在詞彙中的 `NULL` 值和類別會編碼為 `0`。

[升級樹狀結構模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)支援標籤編碼。

### 目標編碼

目標編碼會將類別特徵值替換為分類模型的目標機率，或是迴歸模型的目標期望值。

經過目標編碼的特徵可能類似下列範例：

```
# Classification model
+------------------------+----------------------+
| original value         | target encoded value |
+------------------------+----------------------+
| (category_1, target_1) |     0.5              |
| (category_1, target_2) |     0.5              |
| (category_2, target_1) |     0.0              |
+------------------------+----------------------+

# Regression model
+------------------------+----------------------+
| original value         | target encoded value |
+------------------------+----------------------+
| (category_1, 2)        |     2.5              |
| (category_1, 3)        |     2.5              |
| (category_2, 1)        |     1.5              |
| (category_2, 2)        |     1.5              |
+------------------------+----------------------+
```

目標編碼適用於[提升樹狀結構模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)。

## 後續步驟

如要進一步瞭解支援自動特徵前處理的模型的支援 SQL 陳述式和函式，請參閱下列文件：

* [機器學習模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)
* [時間序列預測模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-forecast?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]