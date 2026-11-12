Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用分析規則限制資料存取權

GoogleSQL for BigQuery 的分析規則可讓您在共用機密資料時，強制執行隱私權政策和條件。您可以直接或在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，對檢視表套用分析規則，根據匯總門檻、差異化隱私公開程度上限或彙整需求限制查詢。

## 什麼是分析規則？

分析規則會強制執行[共用資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)政策。政策代表執行查詢前必須符合的條件。在 BigQuery 中，您可以使用[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)，或直接將分析規則套用至檢視表，對檢視表強制執行分析規則。強制執行分析規則時，所有查詢該檢視表的使用者都必須遵守該檢視表的分析規則。如果符合分析規則，查詢就會產生符合分析規則的輸出內容。如果查詢不符合分析規則，就會產生錯誤。

## 支援的分析規則

支援下列分析規則：

* [匯總門檻分析規則](#agg_analysis_rules)：強制執行資料集須有的不重複實體數量下限。您可以使用 DDL 陳述式或資料無塵室，對檢視表強制執行這項規則。這項規則支援匯總門檻政策和彙整限制政策。
* [差異化隱私分析規則](#dp_analysis_rules)：強制執行隱私公開程度上限，如果資料套用了[差異化隱私](https://docs.cloud.google.com/bigquery/docs/differential-privacy?hl=zh-tw)防護機制，訂閱者看見的資料就會受限。您可以使用 DDL 陳述式或資料無塵室，對檢視表強制執行這項規則。這項規則支援差異化隱私權政策和彙整限制政策。
* [清單重疊分析規則](#list_overlap_rules)：重疊的資料列只能在彙整作業後查詢，這符合規則。您可以使用 DDL 陳述式或資料無塵室，對檢視表強制執行這項規則。這項規則支援加入限制政策。

## 匯總門檻分析規則

匯總門檻分析規則會強制執行一組資料須有的不重複實體數量下限，必須達到這個門檻，查詢結果才會包含該組資料的統計數據。

強制執行時，匯總門檻分析規則會跨維度將資料分組，同時確保符合匯總門檻。系統會計算每個群組的不重複隱私權單位數量 (由隱私權單位欄表示)，且只會輸出不重複隱私權單位數量符合匯總門檻的群組。

包含這項分析規則的檢視表必須包含[匯總門檻政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)，並可視需要加入[彙整限制政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)。

### 定義檢視表的匯總門檻分析規則

您可以在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，或使用 `CREATE VIEW` 陳述式，為檢視表定義匯總門檻分析規則：

```
CREATE OR REPLACE VIEW VIEW_NAME
  OPTIONS (
    privacy_policy= '''{
      "aggregation_threshold_policy": {
        "threshold" : THRESHOLD,
        "privacy_unit_column": "PRIVACY_UNIT_COLUMN"
      },
      "join_restriction_policy": {
        "join_condition": "JOIN_CONDITION",
        "join_allowed_columns": JOIN_ALLOWED_COLUMNS
      }
    }'''
  )
  AS QUERY;
```

定義：

* `aggregation_threshold_policy`：匯總門檻分析規則的匯總門檻政策。

  + VIEW\_NAME：：檢視表的路徑和名稱。
  + THRESHOLD：查詢結果中，每列資料須由多少個不重複隱私權單位提供。如果潛在資料列不符合這個門檻，就會從查詢結果中省略。
  + PRIVACY\_UNIT\_COLUMN：代表隱私權單位欄。*隱私權單位欄*是隱私權單位的專屬 ID。「隱私權單位」是隱私權單位欄中的值，代表一組資料中受保護的實體。

    您只能使用一個隱私權單位欄，且隱私權單位欄的資料類型必須[可分組](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#groupable_data_types)。

    隱私權單位欄中的值無法透過查詢直接投影，且您只能使用[分析規則支援的匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_policy_functions)匯總這個資料欄中的資料。
* `join_restriction_policy` (選用)：匯總門檻分析規則的選用 join 限制政策。

  + JOIN\_CONDITION：要
    對檢視表強制執行的 join 限制類型。可為下列其中一個值：

    - `JOIN_ALL`：`join_allowed_columns` 中的所有資料欄都必須進行內部彙整，才能查詢這個檢視表。
    - `JOIN_ANY`：必須至少彙整 `join_allowed_columns` 中的一個資料欄，才能查詢這個檢視表。
    - `JOIN_BLOCKED`：這個檢視表無法沿著任何資料欄彙整。在這種情況下，請勿設定 `join_allowed_columns`。
    - `JOIN_NOT_REQUIRED`：不需彙整即可查詢這個檢視表。如果使用 join，則只能使用 `join_allowed_columns` 中的資料欄。
  + JOIN\_ALLOWED\_COLUMNS：可做為 join 作業一部分的資料欄。
* QUERY：檢視表的查詢。

範例：

在以下範例中，系統會在名為 `ExamView` 的檢視表上建立匯總門檻分析規則。`ExamView` 參照名為 [`ExamTable`](#example-tables) 的資料表：

```
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"aggregation_threshold_policy": {"threshold": 3, "privacy_unit_column": "last_name"}}'
)
AS ( SELECT * FROM mydataset.ExamTable );
```

如要查看 `CREATE VIEW` 的 `privacy_policy` 語法，請參閱 [`CREATE VIEW`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_view_statement) 中的 `OPTIONS` 清單。

### 更新檢視表的匯總門檻分析規則

您可以在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，或使用 `ALTER VIEW` 陳述式，變更檢視表的匯總門檻分析規則：

```
ALTER VIEW VIEW_NAME
SET OPTIONS (
  privacy_policy= '''{
    "aggregation_threshold_policy": {
      "threshold" : THRESHOLD,
      "privacy_unit_column": "PRIVACY_UNIT_COLUMN"
    }
  }'''
)
```

如要進一步瞭解上述語法中可為隱私權政策設定的值，請參閱「[定義檢視表的匯總門檻分析規則](#define_privacy_view)」。

範例：

在以下範例中，系統會更新名為 [`ExamView`](#define_privacy_view) 的檢視表匯總門檻分析規則。

```
ALTER VIEW mydataset.ExamView
SET OPTIONS (
  privacy_policy= '{"aggregation_threshold_policy": {"threshold": 50, "privacy_unit_column": "last_name"}}'
);
```

如要查看 `ALTER VIEW` 的 `privacy_policy` 語法，請參閱 [`ALTER VIEW SET OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement) 中的 `OPTIONS` 清單。

### 查詢強制執行匯總門檻分析規則的檢視表

您可以使用 [`AGGREGATION_THRESHOLD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_clause) 子句，查詢具有匯總門檻分析規則的檢視表。查詢必須包含匯總函式，且只能使用[支援匯總門檻的匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_policy_functions)。

範例：

在以下範例中，系統會對名為 [`ExamView`](#define_privacy_view) 的檢視表查詢匯總門檻分析規則：

```
SELECT WITH AGGREGATION_THRESHOLD
  test_id, COUNT(DISTINCT last_name) AS student_count
FROM mydataset.ExamView
GROUP BY test_id;

/*---------+---------------*
 | test_id | student_count |
 +---------+---------------+
 | P91     | 3             |
 | U25     | 4             |
 *---------+---------------*/
```

匯總門檻分析規則也可以視需要加入彙整限制政策。如要瞭解如何搭配使用加入限制政策和分析規則，請參閱「[分析規則中的加入限制政策](#join-restriction-policy)」。

如要查看 `AGGREGATION_THRESHOLD` 子句的其他範例，請參閱「[`AGGREGATION_THRESHOLD` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_clause)」。

## 差異化隱私分析規則

差異化隱私分析規則會強制執行隱私公開程度上限，如果資料套用了[差異化隱私](https://docs.cloud.google.com/bigquery/docs/differential-privacy?hl=zh-tw)防護機制，訂閱者看見的資料就會受限。套用隱私公開程度上限之後，如果所有查詢的 Epsilon 或 Delta 總和達到 Epsilon 總值或 Delta 總值，所有訂閱者都無法查詢共用資料。您可以在檢視表中使用這項分析規則。

包含這項分析規則的檢視表必須包含[差異化隱私政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)，並可視需要加入[彙整限制政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)。

**預覽**

差異化隱私的參數導向隱私公開程度上限功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)，而 BigQuery 資料無塵室的差異化隱私強制執行功能現已[正式發布](https://cloud.google.com/products?hl=zh-tw#product-launch-stages) (GA)。

這項預先發布版產品或功能適用《[服務專屬條款](https://cloud.google.com/terms/service-terms?hl=zh-tw)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。詳情請參閱[推出階段說明](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。

如要針對預先發布版功能提供意見或尋求支援，請傳送電子郵件至 [bq-dcr-feedback@google.com](mailto:bq-dcr-feedback@google.com)。

### 定義檢視表的差異化隱私分析規則

**注意：**本節範例中的隱私權參數並非建議值。請與隱私或資安人員合作，決定資料集和組織最適合的隱私參數。

您可以在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，或使用 `CREATE VIEW` 陳述式，為檢視表定義差異化隱私分析規則：

```
CREATE OR REPLACE VIEW VIEW_NAME
  OPTIONS (
    privacy_policy= '''{
      "differential_privacy_policy": {
        "privacy_unit_column": "PRIVACY_UNIT_COLUMN",
        "max_epsilon_per_query": MAX_EPSILON_PER_QUERY,
        "epsilon_budget": EPSILON_BUDGET,
        "delta_per_query": DELTA_PER_QUERY,
        "delta_budget": DELTA_BUDGET,
        "max_groups_contributed": MAX_GROUPS_CONTRIBUTED
      },
      "join_restriction_policy": {
        "join_condition": "JOIN_CONDITION",
        "join_allowed_columns": JOIN_ALLOWED_COLUMNS
      }
    }'''
  )
  AS QUERY;
```

定義：

* `differential_privacy_policy`：差異化隱私分析規則的差異化隱私政策。

  + PRIVACY\_UNIT\_COLUMN：[資料欄](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_privacy_unit_id)，用於識別使用隱私權分析規則保護的資料集中的實體。這個值是 JSON 字串。
  + MAX\_EPSILON\_PER\_QUERY：決定每項查詢結果中加入的雜訊量，並防止單一查詢達到總 Epsilon。這個值是 JSON 數字，介於 `0.001` 到 `1e+15` 之間。
  + EPSILON\_BUDGET：[Epsilon](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_epsilon) 預算，代表檢視表上所有差異化私人查詢可使用的 Epsilon 總量。這個值必須大於 `MAX_EPSILON_PER_QUERY`，且為 `0.001` 到 `1e+15` 之間的 JSON 數字。
  + DELTA\_PER\_QUERY：結果中任何資料列不符合 Epsilon 差異化隱私條件的機率。這個值是 JSON 數字，介於 `1e-15` 到 `1` 之間。
  + DELTA\_BUDGET：[delta](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_delta) 預算，代表檢視表上所有差異化私人查詢可使用的總 delta。這個值必須大於 `DELTA_PER_QUERY`，且為 `1e-15` 到 `1000` 的 JSON 數字。
  + MAX\_GROUPS\_CONTRIBUTED (選用)：限制隱私權單位欄中的實體可貢獻的[群組數量](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_max_groups)。這個值必須是非負 JSON 整數。
* `join_restriction_policy` (選用)：差異化隱私分析規則的選用 join 限制政策。

  + JOIN\_CONDITION：：要對檢視表
    強制執行的 join 限制類型。可為下列其中一個值：

    - `JOIN_ALL`：`join_allowed_columns` 中的所有資料欄都必須進行內部彙整，才能查詢這個檢視表。
    - `JOIN_ANY`：必須至少彙整 `join_allowed_columns` 中的一個資料欄，才能查詢這個檢視表。
    - `JOIN_BLOCKED`：這個檢視表無法沿著任何資料欄彙整。在這種情況下，請勿設定 `join_allowed_columns`。
    - `JOIN_NOT_REQUIRED`：不需彙整即可查詢這個檢視表。如果使用 join，則只能使用 `join_allowed_columns` 中的資料欄。
  + JOIN\_ALLOWED\_COLUMNS：可做為 join 作業一部分的資料欄。
* QUERY：檢視表的查詢。

範例：

在以下範例中，系統會對名為 `ExamView` 的檢視表建立差異化隱私分析規則。`ExamView` 參照名為 [`ExamTable`](#example-tables) 的資料表：

```
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"differential_privacy_policy": {"privacy_unit_column": "last_name", "max_epsilon_per_query": 1000.0, "epsilon_budget": 10000.1, "delta_per_query": 0.01, "delta_budget": 0.1, "max_groups_contributed": 2}}'
)
AS ( SELECT * FROM mydataset.ExamTable );

-- NOTE: Delta and epsilon parameters are set very high due to the small
-- dataset. In practice, these should be much smaller.
```

如要查看 `CREATE VIEW` 的 `privacy_policy` 語法，請參閱 [`CREATE VIEW`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_view_statement) 中的 `OPTIONS` 清單。

### 更新檢視表的差異化隱私分析規則

**注意：**本節範例中的隱私權參數並非建議值。請與隱私或資安人員合作，決定資料集和組織最適合的隱私參數。

您可以在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，或使用 `ALTER VIEW` 陳述式，變更檢視表的差異化隱私數據分析規則：

```
ALTER VIEW VIEW_NAME
SET OPTIONS (
  privacy_policy= '''{
    "differential_privacy_policy": {
      "privacy_unit_column": "PRIVACY_UNIT_COLUMN",
      "max_epsilon_per_query": MAX_EPSILON_PER_QUERY,
      "epsilon_budget": EPSILON_BUDGET,
      "delta_per_query": DELTA_PER_QUERY,
      "delta_budget": DELTA_BUDGET,
      "max_groups_contributed": MAX_GROUPS_CONTRIBUTED
    }
  }'''
)
```

如要進一步瞭解上述語法中可為隱私權政策設定的值，請參閱「[定義檢視表的差異化隱私分析規則](#dp_analysis_rules)」。

**注意：**更新差異化隱私分析規則時，隱私公開程度上限會重設。

範例：

在以下範例中，名為 [`ExamView`](#dp_define_privacy_view) 的檢視表更新了差異化隱私分析規則。

```
ALTER VIEW mydataset.ExamView
SET OPTIONS(
  privacy_policy= '{"differential_privacy_policy": {"privacy_unit_column": "last_name", "max_epsilon_per_query": 0.01, "epsilon_budget": 1000.0, "delta_per_query": 0.05, "delta_budget": 0.1, "max_groups_contributed": 2}}'
);

-- NOTE: Delta and epsilon parameters are set very high due to the small
-- dataset. In practice, these should be much smaller.
```

如要查看 `ALTER VIEW` 的 `privacy_policy` 語法，請參閱 [`ALTER VIEW SET OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement) 中的 `OPTIONS` 清單。

### 查詢強制執行差異化隱私分析規則的檢視表

**注意：**本節範例中的隱私權參數並非建議值。請與隱私或資安人員合作，決定資料集和組織最適合的隱私參數。

您可以使用 `DIFFERENTIAL_PRIVACY` 子句，查詢具有差異化隱私數據分析規則的檢視表。如要查看 `DIFFERENTIAL_PRIVACY` 子句的語法和其他範例，請參閱「[`DIFFERENTIAL_PRIVACY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_clause)」。

**注意：**如果您剛建立含有差異化隱私分析規則的檢視表，請稍候片刻，再對檢視表執行查詢。

範例：

在以下範例中，系統會對名為 [`ExamView`](#define_privacy_view) 的檢視表查詢差異化隱私分析規則。`ExamView` 應會成功傳回差異化隱私資料，因為 `epsilon`、`delta` 和 `max_groups_contributed` 都符合 `ExamView` 中差異化分析規則的條件。

```
-- Query an analysis rule enforced view called ExamView.
SELECT
  WITH DIFFERENTIAL_PRIVACY
    test_id,
    AVG(test_score) AS average_test_score
FROM mydataset.ExamView
GROUP BY test_id;

-- Results will vary.
/*---------+--------------------*
 | test_id | average_test_score |
 +---------+--------------------+
 | P91     | 512.627693163311   |
 | C83     | 506.01565971561649 |
 | U25     | 524.81202728847893 |
 *---------+--------------------*/
```

**警告：**如果隱私公開程度上限在一或多項查詢中用盡，就無法再查詢檢視表，必須更新或重新建立。

#### 封鎖 epsilon 超出範圍的查詢

Epsilon 可用於新增或移除雜訊。Epsilon 越大，加入的雜訊越少。如要確保差異化隱私查詢的雜訊量最少，請密切注意差異化隱私分析規則中的 `max_epsilon_per_query` 值。

範例：

在下列查詢中，`DIFFERENTIAL_PRIVACY` 子句中的 `epsilon` 高於 [`ExamView`](#define_privacy_view) 中的 `max_epsilon_per_query`，因此查詢會遭到封鎖並顯示錯誤：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"differential_privacy_policy": {"privacy_unit_column": "last_name", "max_epsilon_per_query": 10.01, "epsilon_budget": 1000.0, "delta_per_query": 0.01, "delta_budget": 0.1, "max_groups_contributed": 2}}'
)
AS ( SELECT * FROM mydataset.ExamTable );

-- NOTE: Delta and epsilon parameters are set very high due to the small
-- dataset. In practice, these should be much smaller.
```

建立檢視表後，請稍候片刻，然後執行下列查詢：

```
-- Error: Epsilon is too high: 1e+20, policy for table mydataset.
-- ExamView allows max 10.01
SELECT
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=1e20)
    test_id,
    AVG(test_score) AS average_test_score
FROM mydataset.ExamView
GROUP BY test_id;
```

**警告：**如果隱私公開程度上限在一或多項查詢中用盡，就無法再查詢檢視表，必須更新或重新建立。

#### 封鎖超出 Epsilon 預算的查詢

Epsilon 可用於新增或移除雜訊。Epsilon 值越低，雜訊越多；Epsilon 值越高，雜訊越少。即使雜訊很高，對同一資料進行多次查詢，最終仍可能揭露未加入雜訊的資料版本。為避免這種情況，您可以建立 Epsilon 預算。如要新增 epsilon 預算，請查看檢視表差異化隱私分析規則中的 `epsilon_budget` 值。

範例：

執行下列查詢三次。第三次查詢時，由於使用的總 Epsilon 為 `30`，但 [`ExamView`](#define_privacy_view) 中的 `epsilon_budget` 僅允許 `25.6`，因此查詢會遭到封鎖：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"differential_privacy_policy": {"privacy_unit_column": "last_name", "max_epsilon_per_query": 10.01, "epsilon_budget": 25.6, "delta_per_query": 0.01, "delta_budget": 0.1, "max_groups_contributed": 2}}'
)
AS ( SELECT * FROM mydataset.ExamTable );

-- NOTE: Delta and epsilon parameters are set very high due to the small
-- dataset. In practice, these should be much smaller.
```

建立檢視表後，請稍候片刻，然後執行下列查詢三次：

```
-- Error after three query runs: Privacy budget is not sufficient for
-- table 'mydataset.ExamView' in this query.

SELECT
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=10)
    test_id,
    AVG(test_score) AS average_test_score
FROM mydataset.ExamView
GROUP BY test_id;
```

**警告：**如果隱私公開程度上限在一或多項查詢中用盡，就無法再查詢檢視表，必須更新或重新建立。

## 清單重疊分析規則

彙整作業完成後，只有重疊的資料列可供查詢，這符合清單重疊規則。您可以使用 DDL 陳述式或資料無塵室，對檢視表強制執行這項規則。

包含這項分析規則的檢視表，只能包含[彙整限制政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)。

### 為檢視表定義名單重疊分析規則

您可以在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，或使用 `CREATE VIEW` 陳述式，為檢視表定義名單重疊分析規則：

```
CREATE OR REPLACE VIEW VIEW_NAME
  OPTIONS (
    privacy_policy= '''{
      "join_restriction_policy": {
        "join_condition": "JOIN_CONDITION",
        "join_allowed_columns": JOIN_ALLOWED_COLUMNS
      }
    }'''
  )
  AS QUERY;
```

定義：

* `join_restriction_policy`：名單重疊分析規則的彙整限制政策。

  + JOIN\_CONDITION：要對檢視畫面強制執行的清單重疊類型。可為下列其中一個值：

    - `JOIN_ALL`：`join_allowed_columns` 中的所有資料欄都必須進行內部彙整，才能查詢這個檢視表。
    - `JOIN_ANY`：必須至少彙整 `join_allowed_columns` 中的一個資料欄，才能查詢這個檢視表。
  + JOIN\_ALLOWED\_COLUMNS：可做為 join 作業一部分的資料欄。
* QUERY：檢視表的查詢。

範例：

在以下範例中，系統會在名為 `ExamView` 的檢視表上建立名單重疊分析規則。`ExamView` 參照名為 [`ExamTable`](#example-tables) 的資料表：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"join_restriction_policy": {"join_condition": "JOIN_ANY", "join_allowed_columns": ["test_id", "test_score"]}}'
)
AS ( SELECT * FROM mydataset.ExamTable );
```

### 更新資料檢視的名單重疊分析規則

您可以使用[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)或 `ALTER VIEW` 陳述式，變更檢視畫面的名單重疊分析規則：

```
ALTER VIEW VIEW_NAME
SET OPTIONS (
  privacy_policy= '''{
    "join_restriction_policy": {
      "join_condition": "JOIN_CONDITION",
      "join_allowed_columns": JOIN_ALLOWED_COLUMNS
    }
  }'''
)
```

如要進一步瞭解上述語法中可為隱私權政策設定的值，請參閱「[為檢視定義名單重疊分析規則](#define_list_overlap_view)」。

範例：

在以下範例中，系統會更新名為 [`ExamView`](#define_list_overlap_view) 的檢視表中的名單重疊分析規則。

```
ALTER VIEW mydataset.ExamView
SET OPTIONS(
  privacy_policy= '{"join_restriction_policy": {"join_condition": "JOIN_ALL", "join_allowed_columns": ["test_id", "test_score"]}}'
);
```

如要查看 `ALTER VIEW` 的 `privacy_policy` 語法，請參閱 [`ALTER VIEW SET OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement) 中的 `OPTIONS` 清單。

### 查詢已強制執行名單重疊分析規則的檢視表

您可以對具有名單重疊分析規則的檢視表執行彙整作業。如要查看 `JOIN` 作業的語法，請參閱「[Join 作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)」。

#### 封鎖沒有重疊的彙整作業

如果彙整作業與必要資料欄沒有至少一個重疊，您可以封鎖該作業。

範例：

在下列查詢中，名為 [`ExamView`](#define_list_overlap_view) 的檢視表會與名為 [`StudentTable`](#example-tables) 的資料表彙整。由於檢視表包含`JOIN_ANY`清單重疊分析規則，因此 `ExamView` 和 `StudentTable` 至少須有一個重疊的資料列。由於至少有一個重疊，因此查詢會成功執行。

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"join_restriction_policy": {"join_condition": "JOIN_ANY", "join_allowed_columns": ["test_score", "last_name"]}}'
)
AS ( SELECT * FROM mydataset.ExamTable );

-- Query a view called ExamView and a table called StudentTable.
SELECT *
FROM mydataset.ExamView INNER JOIN mydataset.StudentTable USING (test_score);

/*------------+-----------+---------+-------------*
 | test_score | last_name | test_id | last_name_1 |
 +------------+-----------+---------+-------------+
 | 490        | Ivanov    | U25     | Ivanov      |
 | 500        | Wang      | U25     | Wang        |
 | 510        | Hansen    | P91     | Hansen      |
 | 550        | Silva     | U25     | Silva       |
 | 580        | Devi      | U25     | Devi        |
 *------------+-----------+---------+-------------*/
```

#### 封鎖未完全重疊的內部彙整作業

如果彙整作業未與所有必要資料欄重疊，您可以封鎖該作業。

範例：

在以下範例中，系統嘗試對名為 [`ExamView`](#define_list_overlap_view) 的檢視表和名為 [`StudentTable`](#example-tables) 的資料表執行彙整作業，但查詢失敗。失敗的原因是 `ExamView` 清單重疊分析規則要求彙整彙整限制政策中的所有資料欄。由於名為 [`StudentTable`](#example-tables) 的資料表不含這些資料欄，因此並非所有資料列都會重疊，並會產生錯誤。

```
-- Create a view that includes ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"join_restriction_policy": {"join_condition": "JOIN_ALL", "join_allowed_columns": ["test_score", "last_name"]}}'
)
AS ( SELECT * FROM mydataset.ExamTable );

-- Query error: Joining must occur on all of the following columns
-- [test_score, last_name] on table mydataset.ExamView.
SELECT *
FROM mydataset.ExamView INNER JOIN mydataset.StudentTable USING (last_name);
```

## 搭配使用加入限制政策與其他政策

加入限制政策可與匯總門檻和差異化隱私分析規則中的其他政策搭配使用。不過，一旦將加入限制政策與其他政策搭配使用，就無法再變更其他政策。

範例：

在以下範例中，匯總門檻分析規則使用了彙整限制政策：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"aggregation_threshold_policy":{"threshold": 3, "privacy_unit_column": "last_name"}, "join_restriction_policy": {"join_condition": "JOIN_ANY", "join_allowed_columns": ["test_id", "test_score"]}}'
)
AS ( SELECT * FROM mydataset.ExamTable );
```

### 封鎖沒有必要資料欄的彙整作業

如果彙整作業未包含至少一個必要資料欄，您可以封鎖該作業。方法是在名單重疊分析規則中加入下列部分：

```
"join_restriction_policy": {
  "join_condition": "JOIN_ANY",
  "join_allowed_columns": ["column_name", ...]
}
```

範例：

在下列查詢中，查詢不包含 [`ExamView`](#define_privacy_view) 和 [`StudentTable`](#example-tables) 中 `test_score` 或 `test_id` 資料欄的任何彙整作業，因此查詢會遭到封鎖並顯示錯誤：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"aggregation_threshold_policy": {"threshold": 3, "privacy_unit_column": "last_name"}, "join_restriction_policy": {"join_condition": "JOIN_ANY", "join_allowed_columns": ["test_score", "test_id"]}}'
)
AS ( SELECT * FROM mydataset.ExamTable );

-- Query error: Joining must occur on at least one of the following columns
-- [test_score, test_id] on table mydataset.ExamView.
SELECT *
FROM mydataset.ExamView INNER JOIN mydataset.StudentTable USING (last_name);
```

如要執行上述查詢，請將 `USING` 子句中的 `last_name` 替換為 `test_score`。

### 封鎖沒有彙整作業的查詢

如果查詢必須有彙整作業，您可以使用下列其中一項清單重疊分析規則，在沒有彙整作業時封鎖查詢：

```
"join_restriction_policy": {
  "join_condition": "JOIN_NOT_REQUIRED"
}
```

```
"join_restriction_policy": {
  "join_condition": "JOIN_NOT_REQUIRED",
  "join_allowed_columns": []
}
```

範例：

在下列查詢中，由於查詢中沒有與 [`ExamView`](#define_privacy_view) 的彙整作業，因此查詢會遭到封鎖：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"aggregation_threshold_policy": {"threshold": 3, "privacy_unit_column": "last_name"}, "join_restriction_policy": {"join_condition": "JOIN_NOT_REQUIRED"}}'
)
AS ( SELECT * FROM mydataset.ExamTable );

-- Query error: At least one allowed column must be specified with
-- join_condition = 'JOIN_NOT_REQUIRED'.
SELECT *
FROM mydataset.ExamView;
```

### 封鎖沒有 join 作業和必要資料欄的查詢

如果查詢必須有彙整作業，且彙整作業必須至少有一個必要資料欄，請在清單重疊分析規則中加入下列部分：

```
"join_restriction_policy": {
  "join_condition": "JOIN_NOT_REQUIRED",
  "join_allowed_columns": ["column_name", ...]
}
```

範例：

在下列查詢中，由於彙整作業不包含 [`ExamView`](#define_privacy_view) `join_allowed_columns` 陣列中的資料欄，因此查詢遭到封鎖：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"aggregation_threshold_policy": {"threshold": 3, "privacy_unit_column": "last_name"}, "join_restriction_policy": {"join_condition": "JOIN_NOT_REQUIRED", "join_allowed_columns": ["test_score"]}}'
)
AS ( SELECT * FROM mydataset.ExamTable );

-- Query error: Join occurring on a restricted column.
SELECT *
FROM mydataset.ExamView INNER JOIN mydataset.StudentTable USING (last_name);
```

如要執行上述查詢，請將 `USING` 子句中的 `last_name` 替換為 `test_score`。

### 封鎖所有彙整作業

您可以封鎖所有加入作業。方法是在名單重疊分析規則中，只加入下列部分：

```
"join_restriction_policy": {
  "join_condition": "JOIN_BLOCKED",
}
```

範例：

在下列查詢中，由於與名為 [`ExamView`](#define_privacy_view) 的檢視表有彙整作業，因此查詢遭到封鎖：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"aggregation_threshold_policy": {"threshold": 3, "privacy_unit_column": "last_name"}, "join_restriction_policy": {"join_condition": "JOIN_BLOCKED"}}'
)
AS ( SELECT * FROM mydataset.ExamTable );

-- Query error: Join occurring on a restricted column.
SELECT *
FROM mydataset.ExamView INNER JOIN mydataset.StudentTable USING (last_name);
```

如要執行上述查詢，請移除 `INNER JOIN` 作業。

### 封鎖未包含所有必要資料欄的內部彙整作業

如果內部 JOIN 作業未包含所有必要資料欄，您可以封鎖該作業。方法是在名單重疊分析規則中加入下列部分：

```
"join_restriction_policy": {
  "join_condition": "JOIN_ALL",
  "join_allowed_columns": ["column_name", ...]
}
```

範例：

在下列查詢中，查詢會因錯誤而遭到封鎖，因為查詢在與名為 [`ExamView`](#define_privacy_view) 的檢視表進行彙整作業時，未包含 `test_score`：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"aggregation_threshold_policy": {"threshold": 3, "privacy_unit_column": "last_name"}, "join_restriction_policy": {"join_condition": "JOIN_ALL", "join_allowed_columns": ["test_score", "last_name"]}}'
)
AS ( SELECT * FROM mydataset.ExamTable );

-- Query error: Joining must occur on all of the following columns
-- [test_score, last_name] on table mydataset.ExamView.
SELECT *
FROM mydataset.ExamView INNER JOIN mydataset.StudentTable USING (last_name);
```

如要執行上述查詢，請將 `USING (last_name)` 替換為 `USING (last_name, test_score)`。

## 範例資料表

本文件中的幾個範例會參照 `ExamTable` 和 `StudentTable` 這兩個資料表。`ExamTable` 包含學生測驗分數清單，`StudentTable` 則包含學生及其測驗分數清單。

如要測試本文件中的範例，請先將下列範例資料表新增至專案：

```
-- Create a table called ExamTable.
CREATE OR REPLACE TABLE mydataset.ExamTable AS (
  SELECT "Hansen" AS last_name, "P91" AS test_id, 510 AS test_score UNION ALL
  SELECT "Wang", "U25", 500 UNION ALL
  SELECT "Wang", "C83", 520 UNION ALL
  SELECT "Wang", "U25", 460 UNION ALL
  SELECT "Hansen", "C83", 420 UNION ALL
  SELECT "Hansen", "C83", 560 UNION ALL
  SELECT "Devi", "U25", 580 UNION ALL
  SELECT "Devi", "P91", 480 UNION ALL
  SELECT "Ivanov", "U25", 490 UNION ALL
  SELECT "Ivanov", "P91", 540 UNION ALL
  SELECT "Silva", "U25", 550);

-- Create a table called StudentTable.
CREATE OR REPLACE TABLE mydataset.StudentTable AS (
  SELECT "Hansen" AS last_name, 510 AS test_score UNION ALL
  SELECT "Wang", 500 UNION ALL
  SELECT "Devi", 580 UNION ALL
  SELECT "Ivanov", 490 UNION ALL
  SELECT "Silva", 550);
```

## 限制

分析規則有下列限制：

* 如果已在檢視表中新增分析規則，則無法在匯總門檻分析規則和差異化隱私分析規則之間切換。

匯總門檻分析規則有下列限制：

* 在[強制執行匯總門檻分析規則的檢視表](#view_in_privacy_query)中，您只能在查詢中使用[支援的匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_policy_functions)。
* 您無法在 materialized view 中新增匯總門檻分析規則。
* 如果在匯總門檻查詢中，使用強制執行匯總門檻分析規則的檢視表，兩者的隱私權單位欄必須具有相同的值。
* 如果在匯總門檻查詢中，使用強制執行匯總門檻分析規則的檢視表，則查詢中的門檻必須大於或等於檢視表中的門檻。
* 如果檢視表設有匯總門檻分析規則，則無法使用[時間旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel)功能。

差異化隱私分析規則有下列限制：

* 檢視表的隱私權預算用盡後，該檢視表就無法使用，您必須建立新的檢視表。

名單重疊分析規則有下列限制：

* 如果您將匯總門檻分析規則或差異化隱私分析規則與名單重疊分析規則合併，且未將 `privacy_unit_column` 設為名單重疊分析規則中的 `join_allowed_column`，在某些情況下可能無法彙整任何資料欄。

## 定價

* 將分析規則附加至檢視表不會產生額外費用。
* 分析作業適用標準 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]