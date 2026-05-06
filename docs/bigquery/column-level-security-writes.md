Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料欄層級存取權控管對寫入作業的影響

本頁說明使用 BigQuery 資料欄層級存取權控管機制，限制存取資料欄層級資料時，對寫入作業的影響。如需資料欄層級存取權控管的一般資訊，請參閱「[BigQuery 資料欄層級存取權控管簡介](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)」。

如要控管資料欄層級的存取權，使用者必須具備受政策標記保護的資料欄讀取權限。部分寫入作業需要先讀取資料欄資料，才能實際寫入資料欄。對於這些作業，BigQuery 會檢查使用者的讀取權限，確保使用者有權存取資料欄。舉例來說，如果使用者要更新的資料包含寫入受保護的欄，使用者必須具備該欄的讀取權限。如果使用者要插入新的資料列，其中包含寫入受保護資料欄的內容，則不需要受保護資料欄的讀取權限。不過，除非使用者擁有受保護資料欄的讀取權限，否則寫入這類資料列的使用者無法讀取新寫入的資料。

以下各節詳細說明不同類型的寫入作業。本主題中的範例使用 `customers` 資料表，結構定義如下：

| 欄位名稱 | 類型 | 模式 | 政策標記 |
| --- | --- | --- | --- |
| `user_id` | STRING | 必填 | `policy-tag-1` |
| `credit_score` | INTEGER | NULLABLE | `policy-tag-2` |
| `ssn` | STRING | NULLABLE | `policy-tag-3` |

## 使用 BigQuery 資料操縱語言 (DML)

### 插入資料

如果是 `INSERT` 陳述式，BigQuery 不會檢查掃描的資料欄或更新的資料欄是否具有政策標記的精細讀取者權限。這是因為 `INSERT` 不需要讀取任何資料欄資料。不過，即使您成功將值插入沒有讀取權限的資料欄，插入後，系統仍會如預期保護這些值。

### 刪除、更新及合併資料

如果是 `DELETE`、`UPDATE` 和 `MERGE` 陳述式，BigQuery 會檢查掃描的資料欄是否具備細部讀取者權限。除非您加入 [`WHERE` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#where_clause)，或需要查詢讀取資料的其他子句或子查詢，否則這些陳述式不會掃描資料欄。

### 正在載入資料

將資料 (例如從 Cloud Storage 或本機檔案) 載入資料表時，BigQuery 不會檢查目的地資料表欄的精細讀取者權限。這是因為載入資料不需要從目的地資料表讀取內容。

串流至 BigQuery 的方式與 `LOAD` 和 `INSERT` 類似。
即使沒有精細讀取者權限，您也可以使用 BigQuery 將資料串流至目標資料表欄。

### 複製資料

如果是複製作業，BigQuery 會檢查使用者是否具備來源資料表的精細讀取者權限。BigQuery 不會檢查使用者是否具備精細讀取者權限，可存取目的地資料表中的資料欄。與 `LOAD`、`INSERT` 和串流類似，複製完成後，您將無法讀取剛寫入的資料，除非您擁有目的地資料表欄的「細部讀取者」權限。

## DML 範例

### `INSERT`

**範例：**

```
INSERT INTO customers VALUES('alice', 85, '123-456-7890');
```

|  | 來源資料欄 | 更新資料欄 |
| --- | --- | --- |
| 是否已檢查政策標記的精細讀取者？ | 不適用 | 否 |
| 已勾選「資料欄」 | 不適用 | `user_id` `credit_score` `ssn` |

### `UPDATE`

**範例：**

```
UPDATE customers SET credit_score = 0
  WHERE user_id LIKE 'alice%' AND credit_score < 30
```

|  | 來源資料欄 | 更新資料欄 |
| --- | --- | --- |
| 是否已檢查政策標記的精細讀取者？ | 是 | 否 |
| 已勾選「資料欄」 | `user_id` `credit_score` | `credit_score` |

### `DELETE`

**範例：**

```
DELETE customers WHERE credit_score = 0
```

|  | 來源資料欄 | 更新資料欄 |
| --- | --- | --- |
| 是否已檢查政策標記的精細讀取者？ | 是 | 否 |
| 已勾選「資料欄」 | `credit_score` | `user_id` `credit_score` `ssn` |

## 載入範例

### 從本機檔案或 Cloud Storage 載入

**範例：**

```
load --source_format=CSV samples.customers \
  ./customers_data.csv \
  ./customers_schema.json
```

|  | 來源資料欄 | 更新資料欄 |
| --- | --- | --- |
| 是否已檢查政策標記的精細讀取者？ | 不適用 | 否 |
| 已勾選「資料欄」 | 不適用 | `user_id` `credit_score` `ssn` |

### 串流

使用舊版 `insertAll` 串流 API 或 Storage Write API 串流時，系統不會檢查政策標記。如果是[擷取 BigQuery 變更資料](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)，系統會檢查主鍵資料欄的政策標記。

## 複製範例

### 將資料附加到現有資料表

**範例：**

```
cp -a samples.customers samples.customers_dest
```

|  | 來源資料欄 | 更新資料欄 |
| --- | --- | --- |
| 是否已檢查政策標記的精細讀取者？ | 是 | 否 |
| 已勾選「資料欄」 | `customers.user_id` `customers.credit_score` `customers.ssn` | `customers_dest.user_id` `customers_dest.credit_score` `customers_dest.ssn` |

### 將查詢結果儲存到目的地資料表

**範例：**

```
query --use_legacy_sql=false \
--max_rows=0 \
--destination_table samples.customers_dest \
--append_table "SELECT * FROM samples.customers LIMIT 10;"
```

|  | 來源資料欄 | 更新資料欄 |
| --- | --- | --- |
| 是否已檢查政策標記的精細讀取者？ | 是 | 否 |
| 已勾選「資料欄」 | `customers.user_id` `customers.credit_score` `customers.ssn` | `customers_dest.user_id` `customers_dest.credit_score` `customers_dest.ssn` |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]