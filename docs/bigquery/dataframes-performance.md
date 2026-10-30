Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 最佳化 BigQuery DataFrames 效能

您可以最佳化 BigQuery DataFrames 工作流程，使用與 pandas 相容的 API 分析及轉換資料，同時縮短執行時間並降低成本。套用特定最佳化技術 (例如部分排序模式和結果快取)，可以更快速、更符合成本效益地處理資料。

## 使用部分排序模式

BigQuery DataFrames 具備排序模式功能，可針對視窗函式和 join 等作業強制執行特定資料列順序。您可以將 `ordering_mode` 屬性設為 `strict` (稱為「嚴格排序模式」，這是預設值) 或 `partial` (稱為「部分排序模式」)，藉此指定排序模式。使用 `partial` 設定可提高查詢效率。

部分排序模式與嚴格排序模式不同。嚴格排序模式會依特定順序排列所有資料列。這種總排序可讓 BigQuery DataFrames 與 pandas 搭配運作，讓您使用 `DataFrame.iloc` 屬性依順序存取資料列。不過，由於總排序和預設的依序索引，篩選資料欄或資料列無法減少掃描的資料量。除非您將這些篩選器做為參數套用至 `read_gbq` 和 `read_gbq_table` 函式，否則系統會防止這種情況發生。為排序 DataFrame 中的所有資料列，BigQuery DataFrames 會建立所有資料列的雜湊。這項作業可能會導致系統執行完整資料掃描，並忽略資料列和資料欄篩選器。

部分排序模式會停止 BigQuery DataFrames 為所有資料列建立總排序，並關閉需要總排序的功能，例如 `DataFrame.iloc` 屬性。部分排序模式也會將 [`DefaultIndexKind` 類別](https://dataframes.bigquery.dev/reference/api/bigframes.enums.DefaultIndexKind.html)設為空值索引，而非依序索引。

使用部分排序模式篩選 `DataFrame` 物件時，BigQuery DataFrames 不會計算序列索引中缺少的資料列。部分排序模式也不會根據索引自動合併資料。這些方法可以提高查詢效率。
不過，無論您使用預設的嚴格排序模式或部分排序模式，BigQuery DataFrames API 的運作方式都與熟悉的 pandas API 類似。

無論是部分或嚴格排序模式，您都必須依據使用的 BigQuery 資源付費。不過，處理大型分群和分區資料表時，使用部分排序模式可降低成本。這是因為叢集和分區資料欄的資料列篩選器，會減少處理的資料量。

**注意：** 部分排序模式不適用於 BigQuery API、bq 指令列工具或 Terraform，因為 BigQuery DataFrames 是用戶端程式庫。

### 啟用部分排序模式

如要使用部分排序，請先將 `ordering_mode` 屬性設為 `partial`，再使用 BigQuery DataFrames 執行其他作業，如以下程式碼範例所示：

```
import bigframes.pandas as bpd

bpd.options.bigquery.ordering_mode = "partial"
```

部分排序模式沒有循序索引，因此可避免不相關的 BigQuery DataFrame 物件隱含 join。您必須明確呼叫 `DataFrame.merge` 方法，才能彙整兩個衍生自不同資料表運算式的 BigQuery DataFrame 物件。

`Series.unique()` 和 `Series.drop_duplicates()` 功能不適用於部分排序模式。請改用 `groupby` 方法找出不重複的值，如以下範例所示：

```
# Avoid order dependency by using groupby instead of drop_duplicates.
unique_col = df.groupby(["column"], as_index=False).size().drop(columns="size")
```

在部分排序模式下，每次執行 `DataFrame.head(n)` 和 `Series.head(n)` 函式時，輸出結果可能不盡相同。如要下載隨機的小型資料樣本，請使用 [`DataFrame.peek()` 或 `Series.peek()` 方法](#preview-peek)。

如需使用 `ordering_mode = "partial"` 屬性的詳細教學課程，請參閱「[使用 BigQuery DataFrames 分析 PyPI 的套件下載資料](https://github.com/googleapis/python-bigquery-dataframes/blob/main/notebooks/dataframes/pypi.ipynb)」。

### 疑難排解

由於 BigQuery DataFrames 在部分排序模式下有時會缺少排序或索引，因此在使用某些與 pandas 相容的方法時，可能會遇到下列問題。

#### 「Order required」錯誤

部分功能 (例如 `DataFrame.head()` 和 `DataFrame.iloc` 函式) 需要排序。如需需要排序的功能清單，請參閱「[支援的 pandas API](https://dataframes.bigquery.dev/supported_pandas_apis.html)」中的「Requires ordering」(需要排序) 欄。

如果物件沒有排序，作業就會失敗，並顯示類似下方的 `OrderRequiredError` 訊息：`OrderRequiredError: Op iloc
requires an ordering. Use .sort_values or .sort_index to provide an ordering.`

如錯誤訊息所述，您可以使用 [`DataFrame.sort_values()` 方法](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.DataFrame.sort_values.html)提供排序方式，依一或多個資料欄排序。其他方法 (例如 [`DataFrame.groupby()`](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.DataFrame.groupby.html)) 則會根據分組依據鍵，隱含提供總排序。

與 pandas 不同，在部分排序模式下，每次執行相同的程式碼，都可能產生不同的結果。為確保結果一致，請為所有資料列使用穩定的總排序。

#### 空值索引錯誤

部分功能 (例如 `DataFrame.unstack()` 和 `Series.interpolate()` 屬性) 需要索引。如需需要索引的功能清單，請參閱「[支援的 pandas API](https://dataframes.bigquery.dev/supported_pandas_apis.html)」中的「Requires index」(需要索引) 欄。

如果使用的作業需要採用部分排序模式的索引，該作業會引發 `NullIndexError` 訊息，如下所示：
`NullIndexError: DataFrame cannot perform interpolate as it has no index.
Set an index using set_index.`

如錯誤訊息所述，您可以使用 [`DataFrame.set_index()` 方法](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.DataFrame.reset_index.html)提供索引，依一或多個資料欄排序。其他方法 (例如 [`DataFrame.groupby()`](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.DataFrame.groupby.html)) 會根據分組依據鍵隱含提供索引，除非設定 `as_index=False` 參數。

## 快取高成本作業的結果

BigQuery DataFrames 會在本機儲存作業，並延遲執行查詢，直到符合特定條件為止。這可能會導致相同作業在不同查詢中執行多次。

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

這個方法會建立臨時 BigQuery 資料表來儲存結果。系統會根據這個臨時資料表在 BigQuery 的儲存空間計費。

## 使用 `peek()` 方法預覽資料

BigQuery DataFrames 提供兩種預覽資料的 API 方法：

* `peek(n)` 會傳回 `n` 列資料，其中 `n` 是列數。
* `head(n)` 會根據情境傳回前 `n` 列資料，其中 `n` 是列數。

只有在資料順序很重要時，才使用 `head()` 方法，例如，當您想要資料欄中的五個最大值時。在其他情況下，請使用 `peek()` 方法，提高資料擷取效率，如以下程式碼範例所示：

```
import bigframes.pandas as bpd

# Read the "Penguins" table into a dataframe
df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

# Preview 3 random rows
df.peek(3)
```

您也可以在使用[部分排序模式](#partial-enable)時，透過 `peek()` 方法下載隨機的小型資料樣本。

## 延遲 `repr()` 資料擷取

您可以使用[筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)或 IDE 偵錯工具，在 BigQuery DataFrames 中呼叫 `repr()` 方法。這項呼叫會觸發 `head()` 呼叫，擷取實際資料。這項擷取作業可能會減慢疊代程式設計和偵錯程序，並產生費用。

如要防止 `repr()` 方法擷取資料，請將 `repr_mode` 屬性設為 `"deferred"`，如以下範例所示：

```
import bigframes.pandas as bpd

bpd.options.display.repr_mode = "deferred"
```

在延遲模式下，您只能透過明確的 [`peek()` 和 `head()` 呼叫](#preview-peek)預覽資料。

## 後續步驟

* 瞭解 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)。
* 瞭解如何[以圖表呈現 BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw)。
* 探索 [BigQuery DataFrames API 參考資料](https://dataframes.bigquery.dev/reference/index.html)。
* 在 GitHub 查看 BigQuery DataFrames [原始碼](https://github.com/googleapis/python-bigquery-dataframes)、[筆記本範例](https://github.com/googleapis/python-bigquery-dataframes/tree/main/notebooks)和[範例](https://github.com/googleapis/python-bigquery-dataframes/tree/main/samples/snippets)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]