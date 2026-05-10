Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用主鍵和外鍵

主鍵和外鍵是資料表限制，有助於查詢最佳化。本文說明如何建立、查看及管理限制，並運用這些限制來最佳化查詢。

BigQuery 支援下列鍵限制：

* **主鍵**：資料表的主鍵是由一或多個資料欄組合而成，每個資料列都有專屬主鍵，且不得為 `NULL`。
* **外鍵**：資料表的外鍵是出現在參照資料表主鍵欄中的一或多個資料欄組合，或是 `NULL`。

主鍵和外鍵通常用於確保資料完整性，並啟用查詢最佳化。BigQuery 不會強制執行主鍵和外鍵限制。在資料表上宣告限制時，請務必確保資料符合限制。BigQuery 可使用資料表限制來最佳化查詢。

## 管理限制

您可以使用下列 DDL 陳述式建立及管理主鍵和外鍵關係：

* 使用 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)建立資料表時，請建立主鍵和外鍵限制。
* 使用 [`ALTER TABLE ADD PRIMARY KEY` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_add_primary_key_statement)，在現有資料表中加入主鍵限制。
* 使用 [`ALTER TABLE ADD FOREIGN KEY` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_add_foreign_key_statement)，在現有資料表中加入外鍵限制。
* 使用 [`ALTER TABLE DROP PRIMARY KEY` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_drop_primary_key_statement)，從資料表捨棄主鍵限制。
* 使用 [`ALTER TABLE DROP CONSTRAINT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_drop_constraint_statement)，從資料表捨棄外鍵限制。

您也可以透過 BigQuery API 更新 [`TableConstraints` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#TableConstraints)，管理資料表限制。

## 查看限制

下列檢視畫面會提供表格限制的相關資訊：

* [`INFORMATION_SCHEMA.TABLE_CONSTRAINTS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-table-constraints?hl=zh-tw)包含資料集中資料表的所有主鍵和外鍵限制資訊。
* 「[`INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE`」檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-constraint-column-usage?hl=zh-tw)
  包含每個資料表主鍵欄的相關資訊，以及資料集中其他資料表的外鍵所參照的欄。
* [`INFORMATION_SCHEMA.KEY_COLUMN_USAGE` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-key-column-usage?hl=zh-tw)包含各資料表資料欄的相關資訊，這些資料欄會受限於主鍵或外鍵。

## 最佳化查詢

在資料表上建立及強制執行主鍵和外鍵時，BigQuery 可以使用該資訊來排除或最佳化特定查詢聯結。雖然可以透過重新編寫查詢來模擬這些最佳化作業，但這類重新編寫並不一定實用。

在實際工作環境中，您可能會建立檢視區塊，彙整許多事實和維度資料表。開發人員可以查詢檢視區塊，不必查詢基礎資料表，也不必每次都手動重寫聯結。只要定義適當的限制，系統就會自動針對任何適用查詢進行聯結最佳化。

**注意：** BigQuery 不會強制執行鍵限制。您有責任隨時維持限制。如果查詢的資料表違反限制，可能會傳回不正確的結果。

以下各節的範例會參照設有限制的 `store_sales` 和 `customer` 資料表：

```
CREATE TABLE mydataset.customer (customer_name STRING PRIMARY KEY NOT ENFORCED);

CREATE TABLE mydataset.store_sales (
    item STRING PRIMARY KEY NOT ENFORCED,
    sales_customer STRING REFERENCES mydataset.customer(customer_name) NOT ENFORCED,
    category STRING);
```

### 消除內部聯結

請考量下列含有 `INNER JOIN` 的查詢：

```
SELECT ss.*
FROM mydataset.store_sales AS ss
    INNER JOIN mydataset.customer AS c
    ON ss.sales_customer = c.customer_name;
```

`customer_name` 資料欄是 `customer` 資料表的主鍵，因此 `store_sales` 資料表中的每個資料列都只有一個相符項目，如果 `sales_customer` 是 `NULL`，則沒有相符項目。由於查詢只會從 `store_sales` 資料表選取資料欄，查詢最佳化工具可以排除聯結，並將查詢重新編寫為下列內容：

```
SELECT *
FROM mydataset.store_sales
WHERE sales_customer IS NOT NULL;
```

### 消除外部聯結

如要移除 `LEFT OUTER JOIN`，右側的聯結鍵必須是唯一的，且只能選取左側的資料欄。請參考以下查詢：

```
SELECT ss.*
FROM mydataset.store_sales ss
    LEFT OUTER JOIN mydataset.customer c
    ON ss.category = c.customer_name;
```

在本例中，`category` 和 `customer_name` 之間沒有關係。所選資料欄只來自 `store_sales` 資料表，且聯結鍵 `customer_name` 是 `customer` 資料表的主鍵，因此每個值都是唯一的。也就是說，`customer` 資料表中每個資料列都恰好有一個 (可能為 `NULL`) 相符項目，因此 `LEFT OUTER JOIN` 可以刪除：`store_sales`

```
SELECT ss.*
FROM mydataset.store_sales;
```

### 重新排序彙整

如果 BigQuery 無法排除聯結，可以使用資料表限制取得聯結基數的相關資訊，並最佳化執行聯結的順序。

## 限制

主鍵和外鍵必須遵守下列限制：

* BigQuery 不會強制執行鍵限制。您有責任隨時維持限制。如果查詢的資料表違反限制，可能會傳回不正確的結果。
* 主鍵不得超過 16 個資料欄。
* 外鍵的值必須存在於參照的資料表欄中。這些值可以是 `NULL`。
* 主鍵和外鍵必須是下列其中一種型別：`BIGNUMERIC`、`BOOLEAN`、`BYTES`、`DATE`、`DATETIME`、`INT64`、`NUMERIC`、`STRING` 或 `TIMESTAMP`。
* 主鍵和外鍵只能在頂層資料欄中設定。
* 主鍵無法命名。
* 如果資料表有主鍵限制，就無法重新命名。
* 每個資料表最多可有 64 個外鍵。
* 外鍵無法參照同一資料表中的資料欄。
* 屬於主鍵限制或外鍵限制的欄位無法重新命名，也無法變更類型。
* 如果您[複製](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)、[複製](https://docs.cloud.google.com/bigquery/docs/table-clones-create?hl=zh-tw)、[還原](https://docs.cloud.google.com/bigquery/docs/table-snapshots-restore?hl=zh-tw)或[快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-create?hl=zh-tw)資料表時未選取 `-a` 或 `--append_table` 選項，來源資料表限制會複製並覆寫至目的地資料表。如果使用 `-a` 或 `--append_table` 選項，系統只會將來源資料表記錄新增至目的地資料表，不會新增資料表限制。

## 後續步驟

* 進一步瞭解如何[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]