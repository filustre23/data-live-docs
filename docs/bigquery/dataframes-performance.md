* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 提升 BigQuery DataFrames 效能

BigQuery DataFrames 可讓您使用與 pandas 相容的 API，分析及轉換 BigQuery 中的資料。如要加快資料處理速度並提高成本效益，可以運用多種技巧來提升效能。

本文將說明下列最佳化效能的方法：

* [使用部分排序模式](#partial-ordering-mode)。
* [在耗用大量資源的作業後快取結果](#cache)。
* [使用 `peek()` 方法預覽資料](#preview-peek)。
* [延後 `repr()` 資料擷取作業](#defer)。

## 使用部分排序模式

BigQuery DataFrames 具有排序模式功能，可針對視窗函式和聯結等作業強制執行特定資料列順序。您可以將 `ordering_mode` 屬性設為 `strict` (稱為*嚴格排序模式*，這是預設值) 或 `partial` (稱為*部分排序模式*)，藉此指定排序模式。使用 `partial` 設定可提高查詢效率。

部分排序模式與嚴格排序模式不同。嚴格排序模式會依特定順序排列所有資料列。這個總排序可讓 BigQuery DataFrame 更適合搭配 pandas 使用，讓您使用 `DataFrame.iloc` 屬性依序存取資料列。不過，總排序及其預設的循序索引會導致欄或列的篩選器無法減少掃描的資料量。除非您將這些篩選器套用為 `read_gbq` 和 `read_gbq_table` 函式的參數，否則系統會防止這類情況發生。如要排序 DataFrame 中的所有資料列，BigQuery DataFrames 會建立所有資料列的雜湊。這項作業可能會導致系統忽略資料列和資料欄篩選器，全面掃描資料。

部分排序模式會停止為所有資料列建立總排序，並關閉需要總排序的功能，例如 `DataFrame.iloc` 屬性。部分排序模式也會將 [`DefaultIndexKind` 類別](https://dataframes.bigquery.dev/reference/api/bigframes.enums.DefaultIndexKind.html)設為空值索引，而非連續索引。

使用部分排序模式篩選 `DataFrame` 物件時，BigQuery DataFrames 不會計算連續索引中缺少的資料列。部分排序模式也不會根據索引自動合併資料。這些方法可提高查詢效率。
不過，無論您使用預設的嚴格排序模式或部分排序模式，BigQuery DataFrames API 的運作方式都與您熟悉的 pandas API 相同。

無論是部分排序模式或嚴格排序模式，您都須支付所用 BigQuery 資源的費用。不過，使用部分排序模式處理大型叢集和分區資料表時，可以降低成本。這是因為叢集和分區欄的列篩選條件會減少處理的資料量，進而降低成本。

**注意：** 部分排序模式不適用於 BigQuery API、bq 指令列工具或 Terraform，因為 BigQuery DataFrames 是用戶端程式庫。

### 啟用部分排序模式

如要使用部分排序，請在對 BigQuery DataFrames 執行任何其他作業前，將 `ordering_mode` 屬性設為 `partial`，如下列程式碼範例所示：

```
import bigframes.pandas as bpd

bpd.options.bigquery.ordering_mode = "partial"
```

部分排序模式缺少連續索引，因此可防止不相關的 BigQuery DataFrame 物件隱含聯結。您必須明確呼叫 `DataFrame.merge` 方法，才能聯結衍生自不同資料表運算式的兩個 BigQuery DataFrame 物件。

「`Series.unique()`」和「`Series.drop_duplicates()`」功能不支援部分排序模式。請改用 `groupby` 方法尋找不重複的值，如下列範例所示：

```
# Avoid order dependency by using groupby instead of drop_duplicates.
unique_col = df.groupby(["column"], as_index=False).size().drop(columns="size")
```

在部分排序模式下，每次執行 `DataFrame.head(n)` 和 `Series.head(n)` 函式時，輸出內容可能不盡相同。如要下載隨機的小型資料樣本，請使用 [`DataFrame.peek()` 或 `Series.peek()` 方法](#preview-peek)。

如需使用 `ordering_mode = "partial"` 屬性的詳細教學課程，請參閱「[使用 BigQuery DataFrames 分析 PyPI 的套件下載次數](https://github.com/googleapis/python-bigquery-dataframes/blob/main/notebooks/dataframes/pypi.ipynb)」。

### 疑難排解

由於處於部分排序模式的 BigQuery DataFrames 有時會缺少排序或索引，因此使用某些與 pandas 相容的方法時，可能會遇到下列問題。

#### 需要訂單錯誤

部分功能 (例如 `DataFrame.head()` 和 `DataFrame.iloc` 函式) 需要排序。如需需要排序的特徵清單，請參閱「[支援的 pandas API](https://dataframes.bigquery.dev/supported_pandas_apis.html)」中的「需要排序」欄。

如果物件沒有排序，作業會失敗，並顯示類似以下的 `OrderRequiredError` 訊息：`OrderRequiredError: Op iloc
requires an ordering. Use .sort_values or .sort_index to provide an ordering.`

如錯誤訊息所述，您可以使用 [`DataFrame.sort_values()` 方法](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.DataFrame.sort_values.html)提供排序，依一或多個資料欄排序。其他方法 (例如 [`DataFrame.groupby()`](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.DataFrame.groupby.html)) 會根據分組依據鍵隱含提供總排序。

與 pandas 不同，如果您處於部分排序模式，每次執行相同程式碼時，可能會產生不同的結果。為確保結果一致，請為所有資料列使用穩定的總排序。

#### 空值索引錯誤

部分屬性 (例如 `DataFrame.unstack()` 和 `Series.interpolate()`) 需要索引。如需索引的必要功能清單，請參閱「[支援的 pandas API](https://dataframes.bigquery.dev/supported_pandas_apis.html)」中的「需要索引」資料欄。

使用需要部分排序模式索引的作業時，作業會引發類似下列內容的 `NullIndexError` 訊息：
`NullIndexError: DataFrame cannot perform interpolate as it has no index.
Set an index using set_index.`

如錯誤訊息所述，您可以使用 [`DataFrame.set_index()` 方法](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.DataFrame.reset_index.html)提供索引，依一或多個資料欄排序。其他方法 (例如 [`DataFrame.groupby()`](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.DataFrame.groupby.html)) 會根據群組依據鍵隱含提供索引，除非設定 `as_index=False` 參數。

## 在昂貴的作業後快取結果

BigQuery DataFrames 會在本機儲存作業，並延後執行查詢，直到符合特定條件為止。這可能會導致相同作業在不同查詢中執行多次。

為避免重複執行耗費資源的作業，請使用 `cache()` 方法儲存中繼結果，如以下範例所示：

```
# Assume you have 3 large dataframes "users", "group" and "transactions"

# Expensive join operations
final_df = users.join(groups).join(transactions)
final_df.cache()
# Subsequent derived results will reuse the cached join
print(final_df.peek())
print(len(final_df[final_df["completed"]]))
print(final_df.groupby("group_id")["amount"].mean().peek(30))
```

這個方法會建立臨時 BigQuery 資料表，用於儲存結果。系統會向您收取 BigQuery 中這個臨時資料表的儲存費用。

## 使用 `peek()` 方法預覽資料

BigQuery DataFrames 提供兩種 API 方法來預覽資料：

* `peek(n)` 會傳回 `n` 列資料，其中 `n` 是列數。
* `head(n)` 會根據內容傳回前 `n` 個資料列，其中 `n` 是資料列數。

只有在資料順序很重要時，才使用 `head()` 方法，例如要取得資料欄中五個最大值時。在其他情況下，請使用 `peek()` 方法，更有效率地擷取資料，如下列程式碼範例所示：

```
import bigframes.pandas as bpd

# Read the "Penguins" table into a dataframe
df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

# Preview 3 random rows
df.peek(3)
```

使用[部分排序模式](#partial-enable)時，您也可以使用 `peek()` 方法下載隨機的小型資料樣本。

## 延後 `repr()` 資料擷取作業

您可以在 BigQuery DataFrames 中使用 `repr()` 方法，搭配[筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)或 IDE 偵錯工具。這項呼叫會觸發 `head()` 呼叫，以擷取實際資料。這項擷取作業可能會拖慢反覆編碼和偵錯程序，還會產生費用。

如要防止 `repr()` 方法擷取資料，請將 `repr_mode` 屬性設為 `"deferred"`，如以下範例所示：

```
import bigframes.pandas as bpd

bpd.options.display.repr_mode = "deferred"
```

在延遲模式中，您只能透過明確的 [`peek()` 和 `head()` 呼叫預覽資料](#preview-peek)。

## 後續步驟

* 瞭解 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)。
* 瞭解如何[將 BigQuery DataFrame 視覺化](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw)。
* 請參閱 [BigQuery DataFrames API 參考資料](https://dataframes.bigquery.dev/reference/index.html)。
* 在 GitHub 上查看 BigQuery DataFrames 的[原始碼](https://github.com/googleapis/python-bigquery-dataframes)、[範例筆記本](https://github.com/googleapis/python-bigquery-dataframes/tree/main/notebooks)和[範例](https://github.com/googleapis/python-bigquery-dataframes/tree/main/samples/snippets)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]