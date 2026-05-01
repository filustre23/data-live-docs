* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用分析規則限制資料存取權

本文提供 GoogleSQL for BigQuery 中分析規則的一般資訊。

## 什麼是分析規則？

分析規則會強制執行資料共用[政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)。政策代表查詢執行前必須符合的條件。在 BigQuery 中，您可以使用[資料淨室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)，或直接將分析規則套用至檢視區塊，對檢視區塊強制執行分析規則。強制執行分析規則後，所有查詢該檢視區塊的使用者都必須遵守該檢視區塊的分析規則。如果符合分析規則，查詢會產生符合分析規則的輸出內容。如果查詢不符合分析規則，就會產生錯誤。

## 支援的分析規則

系統支援下列分析規則：

* [匯總門檻分析規則](#agg_analysis_rules)：強制執行資料集須有的不重複實體數量下限。您可以使用 DDL 陳述式或資料無塵室，在檢視表上強制執行這項規則。這項規則支援匯總門檻政策和聯結限制政策。
* [差異化隱私分析規則](#dp_analysis_rules)：強制執行隱私公開程度上限，如果資料套用了[差異化隱私](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/differential-privacy?hl=zh-tw)防護機制，訂閱者看見的資料就會受限。您可以使用 DDL 陳述式或資料無塵室，在檢視表上強制執行這項規則。這項規則支援差異化隱私權政策和聯結限制政策。
* [清單重疊分析規則](#list_overlap_rules)：重疊的資料列只能在聯結作業後查詢，這符合規則。您可以使用 DDL 陳述式或資料無塵室，在檢視畫面中強制執行這項規則。這項規則支援加入限制政策。

## 匯總門檻分析規則

匯總門檻分析規則會強制執行查詢輸出資料列須有的不重複實體數量下限，必須達到這個門檻，查詢結果才會包含輸出資料列。

強制執行時，匯總門檻分析規則會將資料依維度分組，同時確保達到匯總門檻。這項函式會計算每個群組中不重複隱私單位的數量 (以隱私單位欄表示)，並只輸出不重複隱私單位數量符合匯總門檻的群組。

包含這項分析規則的檢視畫面必須包含[匯總門檻政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)，且可選擇性包含[聯結限制政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)。

### 為檢視區塊定義匯總門檻分析規則

您可以在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，或使用 `CREATE VIEW` 陳述式，為檢視畫面定義匯總門檻分析規則：

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

  + VIEW\_NAME：檢視區塊的路徑和名稱。
  + THRESHOLD：每個查詢結果資料列必須提供的相異隱私權單位數量下限。如果潛在資料列未達到這個門檻，查詢結果就會省略該資料列。
  + PRIVACY\_UNIT\_COLUMN：代表隱私權單位欄。*隱私權單位欄*是隱私權單位的專屬 ID。*隱私權單位*是隱私權單位欄中的值，代表受保護資料集中的實體。

    您只能使用一個隱私權單位欄，且隱私權單位欄的資料類型必須為[可分組](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#groupable_data_types)。

    您無法透過查詢直接預測隱私權單元資料欄中的值，只能使用[分析規則支援的匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_policy_functions)，匯總這個資料欄中的資料。
* `join_restriction_policy` (選用)：匯總門檻分析規則的選用加入限制政策。

  + JOIN\_CONDITION：要對檢視畫面強制執行的聯結限制類型。可為下列其中一個值：

    - `JOIN_ALL`：必須先對 `join_allowed_columns` 中的所有資料欄進行內部聯結，才能查詢這個檢視區塊。
    - `JOIN_ANY`：`join_allowed_columns` 中至少要有一個資料欄加入這個檢視區塊，才能查詢。
    - `JOIN_BLOCKED`：這個檢視畫面無法沿著任何資料欄合併。
      在這種情況下，請勿設定 `join_allowed_columns`。
    - `JOIN_NOT_REQUIRED`：查詢這個檢視區塊時，不需要聯結。如果使用聯結，則只能使用 `join_allowed_columns` 中的資料欄。
  + JOIN\_ALLOWED\_COLUMNS：可做為聯結作業一部分的資料欄。
* QUERY：檢視區塊的查詢。

範例：

在以下範例中，系統會在名為 `ExamView` 的檢視表上建立匯總門檻分析規則。`ExamView` 參照名為「[`ExamTable`](#example-tables)」的資料表：

```
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"aggregation_threshold_policy": {"threshold": 3, "privacy_unit_column": "last_name"}}'
)
AS ( SELECT * FROM mydataset.ExamTable );
```

如要查看 `CREATE VIEW` 的 `privacy_policy` 語法，請參閱 [`CREATE VIEW`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_view_statement) 中的 `OPTIONS` 清單。

### 更新資料檢視的匯總門檻分析規則

您可以在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，或使用 `ALTER VIEW` 陳述式，變更資料檢視的匯總門檻分析規則：

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

如要進一步瞭解您可以在上述語法中為隱私權政策設定的值，請參閱[為檢視畫面定義匯總門檻分析規則](#define_privacy_view)。

範例：

在下列範例中，系統會更新名為 [`ExamView`](#define_privacy_view) 的檢視區塊，

```
ALTER VIEW mydataset.ExamView
SET OPTIONS (
  privacy_policy= '{"aggregation_threshold_policy": {"threshold": 50, "privacy_unit_column": "last_name"}}'
);
```

如要查看 `ALTER VIEW` 的 `privacy_policy` 語法，請參閱`OPTIONS` 清單 [`ALTER VIEW SET OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement)。

### 查詢匯總門檻分析規則強制執行的檢視畫面

您可以使用 [`AGGREGATION_THRESHOLD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_clause) 子句，查詢具有匯總門檻分析規則的檢視區塊。查詢必須包含匯總函式，且只能使用[支援匯總門檻的匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_policy_functions)。

範例：

在下列範例中，系統會對名為 [`ExamView`](#define_privacy_view) 的檢視區塊查詢匯總門檻分析規則：

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

匯總門檻分析規則也可以視需要包含聯結限制政策。如要瞭解如何搭配使用聯結限制政策與分析規則，請參閱「[分析規則中的聯結限制政策](#join-restriction-policy)」。

如要查看`AGGREGATION_THRESHOLD`子句的其他範例，請參閱[`AGGREGATION_THRESHOLD`子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_clause)。

## 差異化隱私分析規則

差異化隱私分析規則會強制執行隱私公開程度上限，如果資料套用了[差異化隱私](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/differential-privacy?hl=zh-tw)防護機制，訂閱者看見的資料就會受限。
套用隱私公開程度上限之後，如果所有查詢的 Epsilon 或 Delta 總和達到 Epsilon 總值或 Delta 總值，所有訂閱者都無法查詢共用資料。您可以在檢視畫面中使用這項分析規則。

包含這項分析規則的檢視區塊必須包含[差異隱私權政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)，且可選擇性包含[聯結限制政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)。

**預覽**

以參數為準的差異隱私權隱私預算功能為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)，而 BigQuery 資料無塵室的差異隱私權強制執行功能現已[正式發布](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。

這項搶先體驗產品或功能適用《[服務專屬條款](https://cloud.google.com/terms/service-terms?hl=zh-tw)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。詳情請參閱[推出階段說明](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。

如要提供意見回饋或尋求預先發布版功能支援，請傳送電子郵件至 [bq-dcr-feedback@google.com](mailto:bq-dcr-feedback@google.com)。

### 為檢視畫面定義差異化隱私權分析規則

**注意：** 本節範例中的隱私權參數僅供參考，您應與隱私或資安人員合作，為資料集和機構決定最合適的隱私參數。

您可以在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，或使用 `CREATE VIEW` 陳述式，為檢視畫面定義差異隱私權分析規則：

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

* `differential_privacy_policy`：差異化隱私權分析規則的差異化隱私權政策。

  + PRIVACY\_UNIT\_COLUMN：資料集中用隱私權分析規則保護實體的[資料欄](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_privacy_unit_id)。這個值是 JSON 字串。
  + MAX\_EPSILON\_PER\_QUERY：決定各查詢結果中加入的雜訊量，並防止單一查詢達到 [epsilon](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_epsilon) 總值。這個值是介於 `0.001` 到 `1e+15` 的 JSON 數字。
  + [EPSILON\_BUDGET：代表檢視畫面中所有差異隱私權查詢可用的 Epsilon 總數。](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_epsilon)這個值必須大於 `MAX_EPSILON_PER_QUERY`，且是介於 `0.001` 到 `1e+15` 的 JSON 數字。
  + DELTA\_PER\_QUERY：結果中任何資料列未通過 epsilon 差異隱私權檢查的機率。這個值是介於 `1e-15` 到 `1` 的 JSON 數字。
  + DELTA\_BUDGET：[差異](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_delta)預算，代表檢視畫面中所有差異隱私權查詢可用的總差異。這個值必須大於 `DELTA_PER_QUERY`，且是介於 `1e-15` 到 `1000` 的 JSON 數字。
  + MAX\_GROUPS\_CONTRIBUTED (選用)：限制隱私單位資料欄中的實體可貢獻的[群組數量](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_max_groups)。這個值必須為非負 JSON 整數。
* `join_restriction_policy` (選用)：差異化隱私權分析規則的選用聯結限制政策。

  + JOIN\_CONDITION：要對檢視畫面強制執行的聯結限制類型。可為下列其中一個值：

    - `JOIN_ALL`：必須先對 `join_allowed_columns` 中的所有資料欄進行內部聯結，才能查詢這個檢視區塊。
    - `JOIN_ANY`：`join_allowed_columns` 中至少要有一個資料欄加入這個檢視區塊，才能查詢。
    - `JOIN_BLOCKED`：這個檢視畫面無法沿著任何資料欄合併。
      在這種情況下，請勿設定 `join_allowed_columns`。
    - `JOIN_NOT_REQUIRED`：查詢這個檢視區塊時，不需要聯結。如果使用聯結，則只能使用 `join_allowed_columns` 中的資料欄。
  + JOIN\_ALLOWED\_COLUMNS：可做為聯結作業一部分的資料欄。
* QUERY：檢視區塊的查詢。

範例：

在以下範例中，系統會在名為 `ExamView` 的檢視表上建立差異化隱私權分析規則。`ExamView` 參照名為「[`ExamTable`](#example-tables)」的資料表：

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

### 更新檢視區塊的差異化隱私權分析規則

**注意：** 本節範例中的隱私權參數僅供參考，您應與隱私或資安人員合作，為資料集和機構決定最合適的隱私參數。

您可以在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，或使用 `ALTER VIEW` 陳述式，變更檢視的差異化隱私權分析規則：

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

如要進一步瞭解您可以在上述語法中設定的隱私權政策值，請參閱[為檢視畫面定義差異隱私權分析規則](#dp_analysis_rules)。

**注意：** 更新差異化隱私權分析規則時，隱私權預算會重設。

範例：

在下列範例中，系統會更新名為 [`ExamView`](#dp_define_privacy_view) 的檢視區塊差異化隱私分析規則。

```
ALTER VIEW mydataset.ExamView
SET OPTIONS(
  privacy_policy= '{"differential_privacy_policy": {"privacy_unit_column": "last_name", "max_epsilon_per_query": 0.01, "epsilon_budget": 1000.0, "delta_per_query": 0.05, "delta_budget": 0.1, "max_groups_contributed": 2}}'
);

-- NOTE: Delta and epsilon parameters are set very high due to the small
-- dataset. In practice, these should be much smaller.
```

如要查看 `ALTER VIEW` 的 `privacy_policy` 語法，請參閱`OPTIONS` 清單 [`ALTER VIEW SET OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement)。

### 查詢強制執行差異化隱私權分析規則的檢視畫面

**注意：** 本節範例中的隱私權參數僅供參考，您應與隱私或資安人員合作，為資料集和機構決定最合適的隱私參數。

您可以使用 `DIFFERENTIAL_PRIVACY` 子句，查詢具有差異化隱私權分析規則的檢視區塊。如要查看 `DIFFERENTIAL_PRIVACY` 子句的語法和其他範例，請參閱[`DIFFERENTIAL_PRIVACY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_clause)。

**注意：** 如果您剛建立含有差異隱私權分析規則的檢視區塊，請稍候片刻再對該檢視區塊執行任何查詢。

範例：

在下列範例中，系統會對名為 [`ExamView`](#define_privacy_view) 的檢視區塊查詢差異化隱私權分析規則。由於 `epsilon`、`delta` 和 `max_groups_contributed` 都符合 `ExamView` 中差異分析規則的條件，因此差異隱私權資料應會從 `ExamView` 順利傳回。

```
-- Query an analysis–rule enforced view called ExamView.
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

**警告：** 當隱私權預算在一或多個查詢中用盡時，檢視畫面就無法再查詢，必須更新或重新建立。

#### 使用超出範圍的 epsilon 封鎖查詢

Epsilon 可用於新增或移除雜訊。Epsilon 值越大，加入的雜訊就越少。如要確保差異隱私權查詢的干擾量最少，請密切注意差異隱私權分析規則中的 `max_epsilon_per_query` 值。

範例：

在下列查詢中，由於 `DIFFERENTIAL_PRIVACY` 子句中的 `epsilon` 高於 [`ExamView`](#define_privacy_view) 中的 `max_epsilon_per_query`，因此查詢遭到封鎖並顯示錯誤：

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

建立檢視區塊後，請稍候片刻，然後執行下列查詢：

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

**警告：** 當隱私權預算在一或多個查詢中用盡時，檢視畫面就無法再查詢，必須更新或重新建立。

#### 封鎖超出 epsilon 預算的查詢

Epsilon 可用於新增或移除雜訊。較小的 epsilon 會增加雜訊，較大的 epsilon 則會減少雜訊。即使雜訊很高，對相同資料進行多次查詢，最終仍可找出未經雜訊處理的資料版本。如要避免這種情況，可以建立 epsilon 預算。如要新增 epsilon 預算，請查看檢視區的差異隱私權分析規則中 `epsilon_budget` 的值。

範例：

執行下列查詢三次。第三次查詢時，系統會封鎖查詢，因為使用的總 Epsilon 為 `30`，但 [`ExamView`](#define_privacy_view) 只允許 `25.6`：`epsilon_budget`

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

建立檢視區塊後，請稍待片刻，然後執行下列查詢三次：

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

**警告：** 當隱私權預算在一或多個查詢中用盡時，檢視畫面就無法再查詢，必須更新或重新建立。

## 清單重疊分析規則

聯結作業後，只能查詢重疊的資料列，這符合清單重疊規則。您可以使用 DDL 陳述式或資料無塵室，對檢視區強制執行這項規則。

包含這項分析規則的檢視區塊只能包含[聯結限制政策](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#privacy_policy)。

### 為檢視畫面定義名單重疊分析規則

您可以在[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)中，或使用 `CREATE VIEW` 陳述式，為檢視畫面定義清單重疊分析規則：

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

* `join_restriction_policy`：清單重疊分析規則的聯結限制政策。

  + JOIN\_CONDITION：要在檢視區塊上強制執行的清單重疊類型。可為下列其中一個值：

    - `JOIN_ALL`：必須先對 `join_allowed_columns` 中的所有資料欄進行內部聯結，才能查詢這個檢視區塊。
    - `JOIN_ANY`：`join_allowed_columns` 中至少要有一個資料欄加入這個檢視區塊，才能查詢。
  + JOIN\_ALLOWED\_COLUMNS：可做為聯結作業一部分的資料欄。
* QUERY：檢視區塊的查詢。

範例：

在下列範例中，系統會在名為 `ExamView` 的檢視區塊上建立清單重疊分析規則。`ExamView` 參照名為「[`ExamTable`](#example-tables)」的資料表：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"join_restriction_policy": {"join_condition": "JOIN_ANY", "join_allowed_columns": ["test_id", "test_score"]}}'
)
AS ( SELECT * FROM mydataset.ExamTable );
```

### 更新檢視區塊的清單重疊分析規則

您可以透過[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)或 `ALTER VIEW` 陳述式，變更檢視的目標對象重疊分析規則：

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

如要進一步瞭解您可以在上述語法中為隱私權政策設定的值，請參閱「[為資料檢視定義名單重疊分析規則](#define_list_overlap_view)」。

範例：

在下列範例中，系統會更新名為 [`ExamView`](#define_list_overlap_view) 的檢視區塊中，清單重疊分析規則。

```
ALTER VIEW mydataset.ExamView
SET OPTIONS(
  privacy_policy= '{"join_restriction_policy": {"join_condition": "JOIN_ALL", "join_allowed_columns": ["test_id", "test_score"]}}'
);
```

如要查看 `ALTER VIEW` 的 `privacy_policy` 語法，請參閱`OPTIONS` 清單 [`ALTER VIEW SET OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement)。

### 查詢名單重疊分析規則 - 強制執行檢視畫面

您可以對具有清單重疊分析規則的檢視區執行聯結作業。如要查看 `JOIN` 作業的語法，請參閱「[加入作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)」。

#### 封鎖沒有重疊的聯結作業

如果聯結作業未與必要資料欄重疊，您可以封鎖該作業。

範例：

在下列查詢中，名為 [`ExamView`](#define_list_overlap_view) 的檢視區塊會與名為 [`StudentTable`](#example-tables) 的資料表聯結。由於檢視畫面包含 `JOIN_ANY` 清單重疊分析規則，因此至少需要 `ExamView` 和 `StudentTable` 的一個重疊資料列。由於至少有一個重疊部分，因此查詢作業會順利執行。

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

#### 封鎖沒有完全重疊的內部聯結作業

如果聯結作業未包含所有必要資料欄的重疊部分，您可以封鎖該作業。

範例：

在下列範例中，系統嘗試對名為 [`ExamView`](#define_list_overlap_view) 的檢視區塊和名為 [`StudentTable`](#example-tables) 的資料表執行聯結作業，但查詢失敗。由於「`ExamView` 清單重疊分析」規則需要根據聯結限制政策中的所有資料欄進行聯結，因此發生失敗。由於名為 [`StudentTable`](#example-tables) 的資料表不含這些資料欄，因此並非所有資料列都會重疊，且會產生錯誤。

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

## 將加入限制政策與其他政策搭配使用

您可以將加入限制政策與其他政策搭配使用，例如匯總門檻和差異化隱私權分析規則。不過，一旦將加入限制政策與其他政策搭配使用，之後就無法變更該其他政策。

範例：

在以下範例中，匯總門檻分析規則會使用聯結限制政策：

```
-- Create a view that includes a table called ExamTable.
CREATE OR REPLACE VIEW mydataset.ExamView
OPTIONS(
  privacy_policy= '{"aggregation_threshold_policy":{"threshold": 3, "privacy_unit_column": "last_name"}, "join_restriction_policy": {"join_condition": "JOIN_ANY", "join_allowed_columns": ["test_id", "test_score"]}}'
)
AS ( SELECT * FROM mydataset.ExamTable );
```

### 封鎖沒有必要資料欄的聯結作業

如果聯結作業未包含至少一個必要資料欄，您可以封鎖該作業。如要執行這項操作，請在清單重疊分析規則中加入下列部分：

```
"join_restriction_policy": {
  "join_condition": "JOIN_ANY",
  "join_allowed_columns": ["column_name", ...]
}
```

範例：

在下列查詢中，查詢會因錯誤而遭到封鎖，因為查詢在 [`ExamView`](#define_privacy_view) 和 [`StudentTable`](#example-tables) 中，未對 `test_score` 或 `test_id` 資料欄執行任何聯結作業：

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

如要執行上述查詢，請在 `USING` 子句中，將 `last_name` 換成 `test_score`。

### 封鎖沒有聯結作業的查詢

如果查詢必須有聯結作業，您可以使用下列其中一項清單重疊分析規則，在沒有聯結作業時封鎖查詢：

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

在下列查詢中，由於查詢中沒有與 [`ExamView`](#define_privacy_view) 的聯結作業，因此查詢遭到封鎖：

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

### 封鎖沒有聯結作業和必要資料欄的查詢

如果查詢必須有聯結作業，且聯結作業必須至少有一個必要資料欄，請在清單重疊分析規則中加入下列部分：

```
"join_restriction_policy": {
  "join_condition": "JOIN_NOT_REQUIRED",
  "join_allowed_columns": ["column_name", ...]
}
```

範例：

在下列查詢中，由於聯結作業未在 [`ExamView`](#define_privacy_view) `join_allowed_columns` 陣列中加入資料欄，因此查詢遭到封鎖：

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

如要執行上述查詢，請在 `USING` 子句中，將 `last_name` 換成 `test_score`。

### 封鎖所有加入作業

你可以封鎖所有加入作業。如要這麼做，請在名單重疊分析規則中只加入下列部分：

```
"join_restriction_policy": {
  "join_condition": "JOIN_BLOCKED",
}
```

範例：

在下列查詢中，由於有與名為 [`ExamView`](#define_privacy_view) 的檢視區塊的聯結作業，因此查詢遭到封鎖：

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

### 封鎖沒有所有必要資料欄的內部聯結作業

如果內部聯結作業未包含所有必要資料欄，您可以封鎖該作業。如要執行這項操作，請在清單重疊分析規則中加入下列部分：

```
"join_restriction_policy": {
  "join_condition": "JOIN_ALL",
  "join_allowed_columns": ["column_name", ...]
}
```

範例：

在下列查詢中，查詢會遭到封鎖並顯示錯誤，因為查詢未在與名為 [`ExamView`](#define_privacy_view) 的檢視區塊進行的聯結作業中加入 `test_score`：

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

如要執行先前的查詢，請將 `USING (last_name)` 換成 `USING (last_name, test_score)`。

## 範例資料表

本文中的幾個範例會參照名為 `ExamTable` 和 `StudentTable` 的兩個資料表。`ExamTable` 包含學生產生的測驗分數清單，`StudentTable` 則包含學生及其測驗分數清單。

如要測試本文中的範例，請先將下列範例表格加入專案：

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

* 如果已在檢視畫面中新增分析規則，就無法在匯總門檻分析規則和差異隱私權分析規則之間切換。

聚合閾值分析規則有下列限制：

* 您只能在[匯總門檻分析規則強制執行的檢視區塊](#view_in_privacy_query)查詢中，使用[支援的匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#agg_threshold_policy_functions)。
* 您無法在具體化檢視中新增匯總門檻分析規則。
* 如果您在匯總門檻查詢中使用匯總門檻分析規則強制執行的檢視畫面，兩者必須具有相同的隱私權單元資料欄值。
* 如果您在匯總門檻查詢中使用匯總門檻分析規則強制執行的資料檢視，查詢中的門檻必須大於或等於資料檢視中的門檻。
* 如果檢視畫面有匯總門檻分析規則，系統會停用[時間回溯](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel)功能。

差異化隱私分析規則有下列限制：

* 檢視表的隱私權預算用盡後，就無法再使用該檢視表，您必須建立新的檢視表。

名單重疊分析規則有下列限制：

* 如果您將匯總門檻分析規則或差異隱私權分析規則，與名單重疊分析規則合併使用，且未將 `privacy_unit_column` 放在名單重疊分析規則的 `join_allowed_column` 中，在某些情況下可能無法加入任何資料欄。

## 定價

* 將分析規則附加至檢視畫面不會產生額外費用。
* 分析作業適用標準 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]