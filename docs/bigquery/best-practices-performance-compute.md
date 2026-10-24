Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 最佳化調整查詢運算

本文提供最佳做法，協助您提升查詢效能。

執行查詢時，您可以在 Google Cloud 控制台[查看查詢計畫](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)。您也可以使用 [`INFORMATION_SCHEMA.JOBS*` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)或 [`jobs.get` REST API 方法](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw#api_sample_representation)要求執行詳細資料。

查詢計畫包含查詢階段和步驟的詳細資料。這些詳細資料可協助您找出提高查詢效能的方法。舉例來說，如果發現某個階段寫入的輸出內容遠多於其他階段，可能代表您需要在查詢中提早篩選。

如要進一步瞭解查詢計畫，並查看查詢計畫資訊如何協助您提升查詢效能的範例，請參閱「[取得查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)」。解決查詢效能深入分析的問題後，您可以執行下列工作，進一步最佳化查詢：

* [減少待處理的資料](#reduce-data-processed)
* [最佳化查詢作業](#optimize-query-operations)
* [減少查詢輸出內容](#reduce-query-output)
* [避免反 SQL 模式](#avoid-anti-sql-patterns)

## 減少處理的資料量

您可以使用下列各節所述的選項，減少需要處理的資料。

### 建議不要使用 `SELECT *`

**最佳做法：**只查詢需要的資料欄，藉此控制投影。

投影是指查詢讀取的資料欄數量。投影過多資料欄會導致額外的 (浪費) I/O 和具體化 (寫入結果)。

* **使用資料預覽選項。**如果您正在實驗或探索資料，請使用其中一個[資料預覽選項](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#preview-data)，而非 `SELECT *`。
* **查詢特定資料欄。**對 `SELECT *` 查詢套用 `LIMIT` 子句不會影響讀取的資料量。系統會根據讀取整個資料表中的所有位元組向您收費，且查詢會計入免費方案配額。相反地，只要查詢需要的資料欄即可。例如，使用 `SELECT * EXCEPT` 從結果中排除一或多個資料欄。
* **使用分區資料表。**如果您確實需要查詢資料表中的每個資料欄，但只需要查詢部分資料，請考慮：
  + 將結果具體化至目的地資料表，並改為查詢該資料表。
  + [將資料表分區](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)，並[查詢相關分區](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)。例如，使用 `WHERE _PARTITIONDATE="2017-01-01"` 僅查詢 2017 年 1 月 1 日的分區。

* **使用 `SELECT * EXCEPT`**。查詢部分資料或使用 `SELECT * EXCEPT`，可大幅減少查詢讀取的資料量。除了節省成本外，減少資料 I/O 量和查詢結果所需的具體化量，也能提升效能。

  ```
  SELECT * EXCEPT (col1, col2, col5)
  FROM mydataset.newtable
  ```

### 避免使用過多 Wildcard 資料表

**最佳做法：**查詢[Wildcard 資料表](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)時，必須使用最精確的前置字串。

透過精簡的 SQL 陳述式使用萬用字元查詢多個資料表。萬用字元資料表是指符合萬用字元運算式的資料表集合。如果資料集包含下列資源，Wildcard 資料表就非常實用：

* 多個具備相容結構定義且命名類似的資料表
* 資料分區資料表

**注意：** 如果資料允許，請使用分區資料表，而非資料分割資料表。詳情請參閱「[避免過度分割資料表](#avoid-oversharding-tables)」。

查詢 Wildcard 資料表時，請在通用資料表前置字串後方指定萬用字元 (`*`)。例如，`FROM bigquery-public-data.noaa_gsod.gsod194*` 會查詢 1940 年代的所有資料表。

相較於較短的前置字串，較詳細的前置字串查詢效果較好。舉例來說，`FROM bigquery-public-data.noaa_gsod.gsod194*` 的效能優於 `FROM bigquery-public-data.noaa_gsod.*`，因為與萬用字元相符的資料表較少。

### 避免使用依日期進行資料分割的資料表

**最佳做法：**請勿使用依日期分區的資料表 (也稱為日期命名資料表) 來取代時間分區資料表。

[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)的執行效果比以日期命名的資料表好。當您建立依日期進行資料分割的資料表時，BigQuery 必須為每個以日期命名的資料表保留一份結構定義與中繼資料的複本。同時，當使用以日期命名的資料表時，BigQuery 可能需要驗證每個查詢資料表的權限。這個做法也會增加查詢的負擔，並影響查詢效能。

### 避免使用資料分割資料表

**最佳做法：**避免建立太多資料表資料分割。如果您要依日期對資料表進行資料分割，請改為使用時間分區資料表。

資料表 sharding 是指將大型資料集分割成多個資料表，並在每個資料表名稱中加入後置字串。如果您要依日期對資料表進行資料分割，請改為使用[時間分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)。

BigQuery 儲存空間的費用低廉，因此您不必像在關聯式資料庫系統中一樣，為了降低成本而最佳化資料表。建立大量資料表 shard 會影響效能，且影響程度大於任何成本效益。

資料分割資料表需要 BigQuery 為每個資料分割維持結構定義、中繼資料與權限。由於維持每個資料分割的資訊會增加額外負擔，因此對資料表進行資料分割會影響查詢效能。

查詢讀取的資料量和來源可能會影響查詢效能和費用。

### 修整分區查詢

**最佳做法：**查詢[分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)時，如要使用分區資料表上的分區進行篩選，請使用下列資料欄：

* 如果是擷取時間分區資料表，請使用虛擬資料欄 `_PARTITIONTIME`
* 如果是分區資料表 (例如以時間單位資料欄和整數範圍為基礎)，請使用*分區資料欄*。

如果是時間單位分區資料表，使用 `_PARTITIONTIME` 或*分區資料欄*篩選資料，即可指定日期或日期範圍。舉例來說，下列 `WHERE` 子句使用 `_PARTITIONTIME` 虛擬資料欄，指定 2016 年 1 月 1 日至 2016 年 1 月 31 日之間的分區：

```
WHERE _PARTITIONTIME
BETWEEN TIMESTAMP("20160101")
AND TIMESTAMP("20160131")
```

查詢只會處理該日期範圍指定的分區中資料。篩選分區可以提高查詢成效並降低成本。

### 使用 `JOIN` 之前減少資料

**最佳做法：**執行匯總，減少 `JOIN` 子句前處理的資料量。

搭配使用 [`GROUP BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#group_by_clause)和[匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw)會耗用大量運算資源，因為這類查詢會使用[重組](https://cloud.google.com/blog/products/bigquery/in-memory-query-execution-in-google-bigquery?hl=zh-tw)。由於這些查詢需要大量運算，因此請務必只在必要時使用 `GROUP BY` 子句。

對於包含 `GROUP BY` 和 `JOIN` 的查詢，請在查詢中提早執行匯總，減少處理的資料量。舉例來說，下列查詢會對兩個大型資料表執行 `JOIN`，且不事先篩選：

```
WITH
  users_posts AS (
  SELECT *
  FROM
    `bigquery-public-data`.stackoverflow.comments AS c
  JOIN
    `bigquery-public-data`.stackoverflow.users AS u
  ON
    c.user_id = u.id
  )
SELECT
  user_id,
  ANY_VALUE(display_name) AS display_name,
  ANY_VALUE(reputation) AS reputation,
  COUNT(text) AS comments_count
FROM users_posts
GROUP BY user_id
ORDER BY comments_count DESC
LIMIT 20;
```

這項查詢會預先匯總留言數量，減少 `JOIN` 讀取的資料量：

```
WITH
  comments AS (
  SELECT
    user_id,
    COUNT(text) AS comments_count
  FROM
    `bigquery-public-data`.stackoverflow.comments
  WHERE
    user_id IS NOT NULL
  GROUP BY user_id
  ORDER BY comments_count DESC
  LIMIT 20
  )
SELECT
  user_id,
  display_name,
  reputation,
  comments_count
FROM comments
JOIN
  `bigquery-public-data`.stackoverflow.users AS u
ON
  user_id = u.id
ORDER BY comments_count DESC;
```

**注意：** 使用 `WITH` 子句搭配一般資料表運算式 (CTE) 的目的是提高查詢可讀性，而非提升效能。新增 `WITH` 子句不保證 BigQuery 會具體化臨時中繼資料表，並重複使用臨時結果進行多項參照。視查詢最佳化工具的決策而定，系統可能會在查詢中多次評估 `WITH` 子句。

### 使用 `WHERE` 子句

**最佳做法：**使用 [`WHERE` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#where_clause)限制查詢傳回的資料量。請盡可能在 `WHERE` 子句中使用 `BOOL`、`INT64`、`FLOAT64` 或 `DATE` 欄。

對 `BOOL`、`INT64`、`FLOAT64` 和 `DATE` 欄執行作業的速度，通常比對 `STRING` 或 `BYTE` 欄執行作業快。請盡可能在 `WHERE` 子句中使用採用上述資料類型的資料欄，減少查詢傳回的資料量。

### 使用 materialized view

**最佳做法：**使用 materialized view 預先計算查詢結果，提升效能和效率。

[materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw) 是預先運算的檢視表，會定期快取查詢結果，提高效能和效率。BigQuery 會運用 materialized view 的預先運算結果，並[盡可能](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#incremental_updates)只讀取基礎資料表的變更，以計算最新結果。您可以直接查詢 materialized view，也可以透過 BigQuery 最佳化工具，使用 materialized view 處理基礎資料表的查詢。

### 使用 BI Engine

**最佳做法：**使用 BigQuery BI Engine 快取最常用的資料，加快查詢速度。

建議您在運算查詢的專案中，新增 [BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 預留項目。BigQuery BI Engine 使用向量化查詢引擎，加快 `SELECT` 查詢效能。

### 使用搜尋索引

**最佳做法：**如需在大型資料表中尋找個別資料列，請使用搜尋索引，有效率地查詢資料列。

[搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-tw)是一種資料結構，可讓您使用 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#search)進行高效率搜尋，但也能使用[其他運算子和函式](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw#operator_and_function_optimization)加速查詢，例如等號 (`=`)、`IN` 或 `LIKE` 運算子，以及特定字串和 JSON 函式。

## 最佳化查詢作業

您可以使用下列各節所述的選項，最佳化查詢作業。

### 避免重複轉換資料

**最佳做法：**如果您使用 SQL 執行 ETL 作業，請避免重複轉換相同資料。

例如，如果您是使用 SQL 來刪減字串或使用規則運算式擷取資料，則在目標資料表中將轉換的結果具體化的效能更高。規則運算式之類的函式需要額外的計算。在不增加轉換負擔的情況下查詢目的地資料表會更有效率。

### 避免對相同 CTE 進行多次評估

**最佳做法**：使用[程序語言](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)、變數、[暫存資料表](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#temporary_tables)和自動過期的資料表，保留計算結果，以便稍後在查詢中使用。

如果查詢包含在多個位置使用的[通用資料表運算式 (CTE)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#with_clause)，則每次參照時，系統可能都會評估這些運算式。查詢最佳化工具會嘗試偵測查詢中只能執行一次的部分，但這不一定可行。因此，使用 CTE 可能無法降低內部查詢複雜度和資源消耗。

您可以將 CTE 的結果儲存在純量變數或臨時資料表中，具體取決於 CTE 傳回的資料。

### 避免重複的資料彙整與子查詢

**最佳做法：**避免重複彙整相同的資料表及使用相同的子查詢。

與其重複彙整資料，不如使用巢狀重複資料來表示關係，這樣可能更有效率。巢狀重複資料可避免 join 作業所需的通訊頻寬影響效能。此外，您也不必重複讀取及寫入相同資料，因此可節省 I/O 費用。詳情請參閱「[使用巢狀和重複欄位](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-nested?hl=zh-tw)」。

同樣地，重複執行相同的子查詢會導致重複處理查詢，進而影響效能。如果您要在多個查詢中使用相同的子查詢，請考慮具體化資料表中的子查詢結果，然後在查詢中使用經過具體化的資料。

具體化子查詢結果可提升效能，並減少 BigQuery 讀取和寫入的資料總量。雖然儲存具體化資料會產生少量費用，不過比起重複 I/O 與查詢處理作業的效能影響，仍是利大於弊。

### 將結合模式最佳化

**最佳做法：**如要彙整多個資料表的資料，請先從最大的資料表開始，最佳化彙整模式。

使用 `JOIN` 子句建立查詢時，請考量合併資料的順序。GoogleSQL 查詢最佳化工具會決定資料表應位於 join 的哪一側。最佳做法是先放置資料列最多的資料表，接著放置資料列最少的資料表，然後依大小遞減順序放置其餘資料表。

將大型資料表放在 `JOIN`
的左邊，並將小型資料表放在
`JOIN` 的右邊時，便建立了傳播結合。傳播結合會將較小資料表中的所有資料傳送至處理較大資料表的每個運算單元。建議您先執行傳播結合。

如要查看 `JOIN` 中資料表的大小，請參閱「[取得資料表相關資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_information_about_tables)」。

### 指定主鍵和外鍵限制

**最佳做法：**如果資料表資料符合[主鍵或外鍵限制](https://docs.cloud.google.com/bigquery/docs/primary-foreign-keys?hl=zh-tw)的資料完整性規定，請在資料表結構定義中指定鍵限制。查詢引擎可使用鍵限制來最佳化查詢計畫。

BigQuery 不會自動檢查資料完整性，因此您必須確保資料符合資料表結構定義中指定的限制。如果未在具有指定限制的資料表中維護資料完整性，查詢結果可能會不準確。

### 最佳化 `ORDER BY` 子句

**最佳做法：**使用 `ORDER BY` 子句時，請務必遵循下列最佳做法：

* **在最外層查詢或[視窗子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls?hl=zh-tw)中使用 `ORDER BY`。**
  將複雜作業移至查詢結尾。除非是在視窗函式中使用，否則在查詢中間放置 `ORDER BY` 子句會大幅影響效能。

  另一種排序查詢的方法，是將複雜的運算 (例如規則運算式和數學函式) 推到查詢結尾。這項技術可在執行複雜作業前減少要處理的資料。
* **使用 `LIMIT` 子句。**如果您要排序大量值，但不需要傳回所有值，請使用 `LIMIT` 子句。舉例來說，下列查詢會排序非常大的結果集，並擲回 `Resources exceeded` 錯誤。查詢會依 `mytable` 中的 `title` 欄排序。`title` 欄包含數百萬個值。

  ```
  SELECT
  title
  FROM
  `my-project.mydataset.mytable`
  ORDER BY
  title;
  ```

  如要移除錯誤，請使用類似下方內容的查詢：

  ```
  SELECT
  title
  FROM
  `my-project.mydataset.mytable`
  ORDER BY
  title DESC
  LIMIT
  1000;
  ```
* **使用視窗函式。**如要排序大量值，請使用視窗函式，並在呼叫視窗函式前限制資料。舉例來說，下列查詢會列出十位最年長的 Stack Overflow 使用者及其排名，其中最年長的帳戶排名最低：

  ```
  SELECT
  id,
  reputation,
  creation_date,
  DENSE_RANK() OVER (ORDER BY creation_date) AS user_rank
  FROM bigquery-public-data.stackoverflow.users
  ORDER BY user_rank ASC
  LIMIT 10;
  ```

  這項查詢大約需要 15 秒才能執行完畢。這項查詢在結尾使用 `LIMIT`，但未在 `DENSE_RANK() OVER` 視窗函式中使用。因此，查詢會要求在單一 worker 節點上排序所有資料。

  您應該在計算視窗函式前限制資料集，以提升效能：

  ```
  WITH users AS (
  SELECT
  id,
  reputation,
  creation_date,
  FROM bigquery-public-data.stackoverflow.users
  ORDER BY creation_date ASC
  LIMIT 10)
  SELECT
  id,
  reputation,
  creation_date,
  DENSE_RANK() OVER (ORDER BY creation_date) AS user_rank
  FROM users
  ORDER BY user_rank;
  ```

  這項查詢約需 2 秒才能執行完畢，傳回的結果與前一項查詢相同。

  請注意，`DENSE_RANK()` 函式會依年份排序資料，因此如果排序資料跨越多個年份，這些查詢不會產生相同的結果。

### 將複雜的查詢拆分為較小的查詢

**最佳做法**：運用[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)功能和[儲存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)，將原本設計為單一複雜查詢的運算，改為多個較小且較簡單的查詢。

複雜的查詢、`REGEX` 函式，以及分層子查詢或 join，執行速度可能較慢，且會耗用大量資源。嘗試將所有運算作業納入一個大型 `SELECT` 陳述式 (例如將其設為檢視表)，有時會成為反模式，並可能導致查詢速度緩慢、耗用大量資源。在極端情況下，內部查詢計畫會變得非常複雜，導致 BigQuery 無法執行。

拆分複雜的查詢，即可將中繼結果具體化為變數或[暫存資料表](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#temporary_tables)。接著，您可以在查詢的其他部分使用這些中繼結果。如果查詢中有多個地方需要這些結果，這個函式就更實用。

這通常能讓您更清楚表達查詢中部分內容的真正意圖，並將暫存資料表做為資料具體化點。

### 使用巢狀和重複欄位

如要瞭解如何使用巢狀和重複欄位反正規化資料儲存庫，請參閱「[使用巢狀和重複欄位](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-nested?hl=zh-tw)」。

### 在彙整程序中使用 `INT64` 資料類型

**最佳做法：**在彙整作業中使用 `INT64` 資料類型，而非 `STRING` 資料類型，以降低成本並提升比較效能。

BigQuery 不會為主鍵建立索引，因此彙整欄越寬，比較所需的時間就越長。因此，在 join 中使用 `INT64` 資料類型，會比使用 `STRING` 資料類型更便宜、更有效率。

## 減少查詢輸出內容

您可以使用下列各節所述的選項，減少查詢輸出內容。

### 具體化大型結果集

**最佳做法：**建議您將[大型結果集具體化](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#large-results)至目的地資料表。寫入大型結果集會對效能與成本造成影響。

BigQuery 將快取結果限制在壓縮後約 10 GB。如果查詢傳回的結果較大，就會超過這項限制，並經常導致下列錯誤：[`Response too large`](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw#responseTooLarge)。

如果您從含有可觀資料量的資料表中選取大量欄位，就很可能產生這個錯誤。若執行將資料正規化而未進行縮減或匯總的 ETL 查詢，則寫入快取結果時也可能會發生問題。

您可以透過下列選項，克服快取結果大小的限制：

* 使用篩選器限制結果集
* 使用 `LIMIT` 子句縮減結果集，尤其是在使用 `ORDER BY` 子句時
* 將輸出資料寫入目的地資料表

您可以使用 BigQuery REST API 翻閱結果。詳情請參閱「[分頁瀏覽資料表資料](https://docs.cloud.google.com/bigquery/docs/paging-results?hl=zh-tw)」。

**注意：** 將極大型結果集寫入目的地資料表會影響查詢效能 (I/O)。此外，儲存目的地資料表也會產生小額費用。您可以使用資料集的[預設資料表到期時間](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#create-dataset)，自動刪除大型目的地資料表。詳情請參閱儲存空間最佳做法中的「[使用到期設定](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw#use-expiration-settings)」一節。

## 避免反 SQL 模式

以下最佳做法將說明如何避免會影響 BigQuery 效能的查詢反模式。

### 避免 self-join

**最佳做法：**請勿使用 self-join，改用[視窗 (分析) 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/analytic-function-concepts?hl=zh-tw)或 [`PIVOT` 運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#pivot_operator)。

self-join 通常用於計算資料列之間的關係。使用 self-join 的結果是，輸出資料列數量可能會平方。此輸出量增加可能會導致效能低落。

### 避免 cross join

**最佳做法：**避免使用產生之輸出多於輸入的彙整。需要使用 `CROSS JOIN` 時，請預先匯總資料。

cross join 是指查詢中第一個資料表的每個資料列，都會與第二個資料表的每個資料列彙整，且兩側都有非不重複索引鍵。最壞的輸出情況是左邊表格的列數乘以右邊表格的列數。在極端情況下，查詢可能無法完成。

如果查詢工作完成，查詢計畫說明會顯示輸出資料列與輸入資料列。如要確認[笛卡爾乘積](https://en.wikipedia.org/wiki/Relational_algebra#Selection_and_cross_product)，請修改查詢，依 join 鍵分組依據，列印 `JOIN` 子句兩側的資料列數量。您也可以在查詢執行圖中，查看[高基數彙整](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#high_cardinality_join)的成效深入分析。

如何避免聯結產生的輸出多於輸入造成的效能問題：

* 使用 `GROUP BY` 子句[預先匯總資料](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#reduce_data_before_using_a_join)。
* 使用窗型函式。Window 函式通常比使用 cross join 更有效率。詳情請參閱[視窗函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls?hl=zh-tw)。

### 避免使用更新或插入單一資料列的 DML 陳述式

**最佳做法：**避免使用更新或插入單一資料列的 [DML](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw) 陳述式。請採批次處理方式，集中進行更新和插入作業。

使用單點 DML 陳述式代表您想將 BigQuery 當成線上交易處理 (OLTP) 系統。BigQuery 著重於使用資料表掃描進行線上分析處理 (OLAP) 上，而不是點查詢。如果您需要與 OLTP 類似的功能 (單列更新或插入)，請考慮使用專為支援 OLTP 用途設計的資料庫，例如 [Cloud SQL](https://docs.cloud.google.com/sql/docs?hl=zh-tw)。

BigQuery DML 陳述式適用於批次更新。BigQuery 中的 `UPDATE` 和 `DELETE` DML 陳述式較適合定期重寫資料，而非單列異動。`INSERT` DML 陳述式適合少量使用。插入作業使用的修改[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#data-manipulation-language-statements)與載入工作相同。如果您的使用案例涉及頻繁的單列插入，請考慮改為[串流](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw)資料。

如果批次處理 `UPDATE` 陳述式在非常長的查詢中產生許多值組，則可能會達到 256 KB 的查詢長度限制。如果想要避開查詢長度限制的問題，請考慮是否可以依據邏輯準則而非使用一連串的直接值組取代來處理更新作業。

例如，您可以將一組取代記錄載入到另一個資料表中，然後編寫 DML 陳述式，使其在未更新的資料欄相符時，更新原始資料表中的所有值。例如，如果原始資料是在資料表 `t` 中，而更新是暫存在資料表 `u` 中，則查詢會與以下內容類似：

```
UPDATE
  dataset.t t
SET
  my_column = u.my_column
FROM
  dataset.u u
WHERE
  t.my_key = u.my_key
```

### 避免交易鎖定衝突

**最佳做法：**[多陳述式交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)應保持簡短，避免將單一 DML 陳述式包裝在交易區塊中，並在重試失敗的交易時使用指數輪詢。

多陳述式交易中的變更 DML 陳述式會取得資料表層級鎖定，且每個資料表的並行限制為 1。相較之下，BigQuery 會自動為每個資料表排入最多 20 個獨立變動 DML 陳述式。如果並行多陳述式交易嘗試修改鎖定的資料表，則不會排入佇列，而是會立即失敗，並顯示錯誤訊息：`Transaction is aborted due to concurrent update against table`。

為盡可能減少鎖定爭用和交易失敗，請採用下列做法：

* **請勿將單一 DML 陳述式包裝在交易中**：單一 DML 陳述式 (例如預存程序中的 `MERGE` 陳述式) 本身就具有不可分割性。執行陳述式時，如果不使用 `BEGIN TRANSACTION` 和 `COMMIT TRANSACTION` 陳述式，BigQuery 就能使用 [DML 佇列](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#update_delete_merge_dml_concurrency)。
* **盡量縮短指令碼和工作階段中的交易時間**：在多陳述式查詢或有效[工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)中，當您在交易中執行變動 DML 陳述式時，BigQuery 會取得目標資料表的資料表層級鎖定。BigQuery 會保留這項寫入鎖定，直到交易提交或復原，或父項指令碼或工作階段 (例如 ODBC 或 JDBC 連線) 結束為止。在開始交易前，請先執行長時間執行的運算或暫存查詢，以免資料表持續鎖定。
* **使用指數輪詢重試**：如果交易因並行更新而失敗，BigQuery 可能需要幾秒鐘才能釋放中繼資料層中的交易鎖定。重試失敗的交易時，請使用指數輪詢策略，並在首次重試前等待至少 60 秒。如要找出重疊的父項指令碼或保留資料表鎖定的工作階段，請參閱「[找出失敗交易的重疊工作](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw#find-overlapping-jobs)」。

### 為名稱相似的資料欄使用別名

**最佳做法：**在查詢 (包括子查詢) 中處理名稱相似的資料欄時，請使用資料欄和資料表別名。

別名有助於識別除了初始參照的資料欄外，還參照了哪些資料欄和資料表。使用別名有助於瞭解及解決 SQL 查詢中的問題，包括找出子查詢中使用的資料欄。

## 後續步驟

* 瞭解如何[最佳化成本](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)。
* 瞭解如何[最佳化儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)。
* 瞭解如何[最佳化函式](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-functions?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]