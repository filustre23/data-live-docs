Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用巢狀和重複欄位

您可以在 BigQuery 中使用巢狀 `STRUCT` 和重複 `ARRAY` 欄位，對關聯資料進行去正規化，並在保留父項與子項關係的同時，提升查詢效能。將階層式資料內嵌儲存在單一資料表中，可減少或消除昂貴的資料表彙整和網路重組。

## 資料去正規化

去正規化是提升正規化關聯資料集讀取效能的常見策略。在 BigQuery 中，建議使用巢狀和重複欄位來反正規化資料。如果資料集之間為階層關係且經常同時查詢 (例如上下層關係)，最適合使用這項策略。

使用正規化資料節省儲存空間的效果，在現代系統中較不明顯。使用去標準化資料雖會提高儲存空間成本，但用來換取效能的提升絕對划算。Join 作業需要資料協調 (通訊頻寬)，去標準化作業則可將資料本地化至個別[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)，因此兩者可平行執行。

如要在將資料去標準化的同時維持資料的關係，您可以使用巢狀和重複的欄位，而非完全整併資料。將關聯資料完全整併後，網路通訊 (重組) 可能會對查詢效能造成負面影響。

舉例來說，如果您在進行訂單結構定義的去標準化作業時未使用巢狀與重複的欄位，就可能須按照 `order_id` 等的欄位將資料分組 (如果存在一對多關係)。將資料分組涉及重組作業，因此成效不如使用巢狀與重複的欄位將資料去標準化。

在某些情況下，將資料去標準化及使用巢狀與重複的欄位並無法提升效能。舉例來說，星形結構定義通常是經過最佳化的數據分析結構定義，因此如果您嘗試進一步去正規化，成效可能不會有顯著差異。

## 使用巢狀和重複的欄位

BigQuery 不需要完全整平的去標準化作業。您可以使用巢狀與重複欄位來保留關聯性。

* 巢狀資料 (`STRUCT`)

  + 巢狀結構資料可讓您以內嵌方式呈現外部實體。
  + 查詢巢狀資料時使用 dot 語法參照 Leaf 欄位，這與使用 Join 的語法類似。
  + 在 GoogleSQL 中，巢狀資料會以 [`STRUCT` 類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)表示。
* 重複資料 (`ARRAY`)

  + 建立 `RECORD` 類型的欄位，並將模式設為 `REPEATED`，即可在內嵌中保留一對多關係 (只要關係不是高基數)。
  + 如果使用重複資料，資料重組就非必要。
  + 重複資料會以 `ARRAY` 表示。查詢重複資料時，您可以在 GoogleSQL 中使用 [`ARRAY` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/array_functions?hl=zh-tw)。
* 巢狀和重複的資料 (`STRUCT` 的 `ARRAY`)。

  + 巢狀和重複資料彼此互補。
  + 例如，在交易記錄資料表中，您可以納入明細項目 `STRUCT` 的陣列。

詳情請參閱「[在資料表結構定義中指定巢狀與重複的資料欄](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw)」。

如要進一步瞭解如何反正規化資料，請參閱「[反正規化](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw#denormalization)」。

## 範例

假設有一個 `Orders` 資料表，其中每一列代表一項售出的明細項目：

| **Order\_Id** | **Item\_Name** |
| --- | --- |
| 001 | A1 |
| 001 | B1 |
| 002 | A1 |
| 002 | C1 |

如要分析這個資料表的資料，您必須使用 `GROUP BY` 子句，如下所示：

```
SELECT COUNT (Item_Name)
FROM Orders
GROUP BY Order_Id;
```

`GROUP BY` 子句會產生額外的運算負擔，但您可以透過巢狀結構重複資料來避免這種情況。您可以建立資料表，每列包含一筆訂單，並將訂單委刊項放在巢狀欄位中，這樣就不必使用 `GROUP BY` 子句：

| **Order\_Id** | **Item\_Name** |
| --- | --- |
| 001 | A1    B1 |
| 002 | A1    C1 |

在 BigQuery 中，您通常會將巢狀結構定義指定為 `STRUCT` 物件的 `ARRAY`。您可以使用 [`UNNEST` 運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#unnest_operator)[展開巢狀資料](https://docs.cloud.google.com/bigquery/docs/arrays?hl=zh-tw#flattening_arrays)，如以下查詢所示：

```
SELECT *
FROM UNNEST(
  [
    STRUCT('001' AS Order_Id, ['A1', 'B1'] AS Item_Name),
    STRUCT('002' AS Order_Id, ['A1', 'C1'] AS Item_Name)
  ]
);
```

這項查詢會產生類似下方的結果：

如果這項資料未經巢狀結構處理，每筆訂單可能會有數個資料列，每個資料列代表該訂單中售出的每項商品，這會導致資料表過大，且 `GROUP BY` 作業費用高昂。

## 運動

您可以按照本節中的步驟，查看使用巢狀欄位的查詢與未使用巢狀欄位的查詢之間的成效差異。

1. 根據 `bigquery-public-data.stackoverflow.comments` 公開資料集建立資料表：

   ```
   CREATE OR REPLACE TABLE `PROJECT.DATASET.stackoverflow`
   AS (
   SELECT
     user_id,
     post_id,
     creation_date
   FROM
     `bigquery-public-data.stackoverflow.comments`
   );
   ```
2. 使用 `stackoverflow` 資料表，執行下列查詢，查看每位使用者的最早留言：

   ```
   SELECT
     user_id,
     ARRAY_AGG(STRUCT(post_id, creation_date AS earliest_comment) ORDER BY creation_date ASC LIMIT 1)[OFFSET(0)].*
   FROM
     `PROJECT.DATASET.stackoverflow`
   GROUP BY user_id
   ORDER BY user_id ASC;
   ```

   這項查詢需要約 25 秒才能執行，並處理 1.88 GB 的資料。
3. 建立第二個資料表，其中包含相同資料，並使用 `STRUCT` 類型建立 `comments` 欄位，用來儲存 `post_id` 和 `creation_date` 資料，而不是兩個個別欄位：

   ```
   CREATE OR REPLACE TABLE `PROJECT.DATASET.stackoverflow_nested`
   AS (
   SELECT
     user_id,
     ARRAY_AGG(STRUCT(post_id, creation_date) ORDER BY creation_date ASC) AS comments
   FROM
     `bigquery-public-data.stackoverflow.comments`
   GROUP BY user_id
   );
   ```
4. 使用 `stackoverflow_nested` 資料表，執行下列查詢，查看每位使用者的最早留言：

   ```
   SELECT
     user_id,
     (SELECT AS STRUCT post_id, creation_date as earliest_comment FROM UNNEST(comments) ORDER BY creation_date ASC LIMIT 1).*
   FROM
     `PROJECT.DATASET.stackoverflow_nested`
   ORDER BY user_id ASC;
   ```

   這項查詢需要約 10 秒才能執行完畢，並會處理 1.28 GB 的資料。
5. 完成後，請[刪除](https://docs.cloud.google.com/bigquery/docs/samples/bigquery-delete-table?hl=zh-tw) `stackoverflow` 和 `stackoverflow_nested` 資料表。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-23 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-23 (世界標準時間)。"],[],[]]