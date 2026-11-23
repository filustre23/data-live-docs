Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用主鍵和外鍵

在 BigQuery 資料表宣告主鍵和外鍵限制，有助於查詢最佳化工具排除不必要的 join，並重新排序 join，加快執行速度。建立及管理這些資料表限制，即可加快查詢速度 (尤其是複雜檢視表)，不必手動重寫 SQL。

BigQuery 支援下列鍵限制：

* **主鍵**：資料表的主鍵是一或多個資料欄的組合，每個資料列的主鍵都不重複，且不為 `NULL`。
* **外鍵**：資料表的外鍵是一或多個資料欄的組合，這些資料欄會出現在參照資料表的主鍵資料欄中，或為 `NULL`。

主鍵和外鍵通常用於確保資料完整性，以及最佳化查詢。BigQuery 不會強制執行主鍵和外鍵限制。在資料表上宣告限制時，必須確保資料符合限制。如要確保資料欄中的值不重複，建議使用[識別欄](https://docs.cloud.google.com/bigquery/docs/identity-columns?hl=zh-tw)。BigQuery 可使用資料表限制來最佳化查詢。

## 管理限制

您可以透過下列 DDL 陳述式，建立及管理主鍵和外鍵關係：

* 使用 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)建立資料表時，建立主鍵和外鍵限制。
* 使用 [`ALTER TABLE ADD PRIMARY KEY` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_add_primary_key_statement)，為現有資料表新增主鍵限制。
* 使用 [`ALTER TABLE ADD FOREIGN KEY` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_add_foreign_key_statement)，將外鍵限制新增至現有資料表。
* 使用 [`ALTER TABLE DROP PRIMARY KEY` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_drop_primary_key_statement)，從資料表捨棄主鍵限制。
* 使用 [`ALTER TABLE DROP CONSTRAINT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_drop_constraint_statement)，從資料表捨棄外鍵限制。

您也可以透過 BigQuery API 更新 [`TableConstraints` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#TableConstraints)，管理資料表限制。

## 查看限制

下列檢視畫面會提供資料表限制的相關資訊：

* [`INFORMATION_SCHEMA.TABLE_CONSTRAINTS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-table-constraints?hl=zh-tw)包含資料集內資料表的所有主鍵和外鍵限制資訊。
* [`INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-constraint-column-usage?hl=zh-tw)包含各資料表主鍵欄的資訊，以及資料集內其他資料表外鍵參照的欄。
* [`INFORMATION_SCHEMA.KEY_COLUMN_USAGE` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-key-column-usage?hl=zh-tw)包含每個資料表的資料欄資訊，這些資料欄受限為主鍵或外鍵。

## 最佳化查詢

在資料表上建立並強制執行主鍵和外鍵時，BigQuery 可以使用這項資訊，排除或最佳化特定查詢彙整。雖然可以透過重寫查詢來模擬這些最佳化作業，但這類重寫作業不一定實用。

在正式環境中，您可能會建立檢視表，彙整多個事實和維度資料表。開發人員可以查詢檢視表，而不必查詢基礎資料表，並在每次手動重寫彙整。只要定義適當的限制，系統就會自動對任何適用的查詢執行 join 最佳化。

**注意：**BigQuery 不會強制執行鍵限制。您必須隨時維護限制。如果查詢的資料表違反限制，可能會傳回不正確的結果。

以下各節的範例會參照 `store_sales` 和 `customer` 資料表，並加上限制：

```
CREATE TABLE mydataset.customer (customer_name STRING PRIMARY KEY NOT ENFORCED);

CREATE TABLE mydataset.store_sales (
    item STRING PRIMARY KEY NOT ENFORCED,
    sales_customer STRING REFERENCES mydataset.customer(customer_name) NOT ENFORCED,
    category STRING);
```

### 消除內部彙整

請參考下列包含 `INNER JOIN` 的查詢：

```
SELECT ss.*
FROM mydataset.store_sales AS ss
    INNER JOIN mydataset.customer AS c
    ON ss.sales_customer = c.customer_name;
```

`customer_name` 資料欄是 `customer` 資料表的主鍵，因此 `store_sales` 資料表的每個資料列都只有一個相符項目，如果 `sales_customer` 為 `NULL`，則沒有相符項目。由於查詢只會從 `store_sales` 資料表選取資料欄，因此查詢最佳化工具可以消除 join，並將查詢重寫為下列內容：

```
SELECT *
FROM mydataset.store_sales
WHERE sales_customer IS NOT NULL;
```

### 消除外部彙整

如要移除`LEFT OUTER JOIN`，右側的彙整索引鍵必須不重複，且只能選取左側的資料欄。請參考下列查詢：

```
SELECT ss.*
FROM mydataset.store_sales ss
    LEFT OUTER JOIN mydataset.customer c
    ON ss.category = c.customer_name;
```

在這個範例中，`category` 和 `customer_name` 之間沒有任何關係。所選資料欄僅來自 `store_sales` 資料表，且彙整索引鍵 `customer_name` 是 `customer` 資料表的主鍵，因此每個值都是不重複的。這表示 `customer` 資料表中，`store_sales` 資料表的每個資料列都只有一個 (可能是 `NULL`) 相符項目，且可以排除 `LEFT OUTER JOIN`：

```
SELECT ss.*
FROM mydataset.store_sales;
```

### 重新排序彙整

如果 BigQuery 無法排除 join，則可使用資料表限制取得 join 數量資訊，並最佳化執行 join 的順序。

## 限制

主鍵和外鍵有下列限制：

* BigQuery 不會強制執行鍵限制。您必須隨時維護限制。如果資料表違反限制，查詢可能會傳回不正確的結果。
* 主鍵不得超過 16 個資料欄。
* 外鍵的值必須存在於參照的資料表資料欄中。這些值可以是 `NULL`。
* 主鍵和外鍵必須是下列其中一種：`BIGNUMERIC`、`BOOLEAN`、`BYTES`、`DATE`、`DATETIME`、`INT64`、`NUMERIC`、`STRING` 或 `TIMESTAMP`。
* 主鍵和外鍵只能在頂層資料欄設定。
* 無法命名主鍵。
* 無法重新命名設有主鍵限制的資料表。
* 一個資料表最多可有 64 個外鍵。
* 外鍵無法參照同一資料表中的資料欄。
* 無法重新命名或變更主鍵限制或外鍵限制中的欄位類型。
* 如果您[複製](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)、[複製](https://docs.cloud.google.com/bigquery/docs/table-clones-create?hl=zh-tw)、[還原](https://docs.cloud.google.com/bigquery/docs/table-snapshots-restore?hl=zh-tw)或[建立](https://docs.cloud.google.com/bigquery/docs/table-snapshots-create?hl=zh-tw)資料表快照，但未使用 `-a` 或 `--append_table` 選項，來源資料表的限制會複製並覆寫至目的地資料表。如果使用 `-a` 或 `--append_table` 選項，系統只會將來源資料表記錄新增至目的地資料表，不會套用資料表限制。

## 後續步驟

* 進一步瞭解如何[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-23 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-23 (世界標準時間)。"],[],[]]