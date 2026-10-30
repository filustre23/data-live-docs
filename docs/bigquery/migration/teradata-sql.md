Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Teradata SQL 翻譯指南

本文詳細說明 Teradata 和 BigQuery 在 SQL 語法方面的異同，協助您規劃遷移作業。使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。

## 資料類型

本節說明 Teradata 和 BigQuery 資料類型的對應關係。

**注意：** Teradata 支援 [`DEFAULT`](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Definition-Language-Syntax-and-Examples/Table-Statements/CREATE-TABLE-and-CREATE-TABLE-AS/Syntax-Elements/column_partition_definition/column_data_type_attribute/DEFAULT?tocId=FGX%7EnkdqLciLCOJTJMvFnA) 和其他[限制](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Definition-Language-Syntax-and-Examples/Table-Statements/CREATE-TABLE-and-CREATE-TABLE-AS/Syntax-Elements/column_partition_definition/table_constraint)，但 BigQuery 不會使用這些限制。



| Teradata | BigQuery | 附註 |
| --- | --- | --- |
| `INTEGER` | `INT64` |  |
| `SMALLINT` | `INT64` |  |
| `BYTEINT` | `INT64` |  |
| `BIGINT` | `INT64` |  |
| `DECIMAL` | `NUMERIC, DECIMAL`  `BIGNUMERIC, BIGDECIMAL` | 如果小數位數 (小數點後的位數) <= 9，請使用 BigQuery 的 `NUMERIC` (別名 `DECIMAL`)。  如果小數位數大於 9，請使用 BigQuery 的 `BIGNUMERIC` (別名 `BIGDECIMAL`)。  如需強制執行自訂數字或小數位數界限 (限制)，請使用 BigQuery 的[參數化](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_decimal_type)十進位資料類型。  Teradata 允許您透過四捨五入儲存的值來插入更高精確度的值，但會保留計算中的高精確度。與 ANSI 標準相比，這可能會導致[非預期的四捨五入行為](https://docs.teradata.com/r/SQL-Data-Types-and-Literals/July-2021/Numeric-Data-Types/Rounding)。 |
| `FLOAT` | `FLOAT64` |  |
| `NUMERIC` | `NUMERIC, DECIMAL`  `BIGNUMERIC, BIGDECIMAL` | 如果小數位數 (小數點後的位數) <= 9，請使用 BigQuery 的 `NUMERIC` (別名 `DECIMAL`)。  如果小數位數大於 9，請使用 BigQuery 的 `BIGNUMERIC` (別名 `BIGDECIMAL`)。  如需強制執行自訂數字或小數位數界限 (限制)，請使用 BigQuery 的[參數化](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_decimal_type)十進位資料類型。  Teradata 允許您透過四捨五入儲存的值來插入更高精確度的值，但會保留計算中的高精確度。與 ANSI 標準相比，這可能會導致[非預期的四捨五入行為](https://docs.teradata.com/r/SQL-Data-Types-and-Literals/July-2021/Numeric-Data-Types/Rounding)。 |
| `NUMBER` | `NUMERIC, DECIMAL`  `BIGNUMERIC, BIGDECIMAL` | 如果小數位數 (小數點後的位數) <= 9，請使用 BigQuery 的 `NUMERIC` (別名 `DECIMAL`)。  如果小數位數大於 9，請使用 BigQuery 的 `BIGNUMERIC` (別名 `BIGDECIMAL`)。  如需強制執行自訂數字或小數位數界限 (限制)，請使用 BigQuery 的[參數化](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_decimal_type)十進位資料類型。  Teradata 允許您透過四捨五入儲存的值來插入更高精確度的值，但會保留計算中的高精確度。與 ANSI 標準相比，這可能會導致[非預期的四捨五入行為](https://docs.teradata.com/r/SQL-Data-Types-and-Literals/July-2021/Numeric-Data-Types/Rounding)。 |
| `REAL` | `FLOAT64` |  |
| `CHAR/CHARACTER` | `STRING` | 如需強制規定字元長度上限，請使用 BigQuery 的[參數化](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_string_type) `STRING`資料類型。 |
| `VARCHAR` | `STRING` | 如需強制規定字元長度上限，請使用 BigQuery 的[參數化](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_string_type) `STRING`資料類型。 |
| `CLOB` | `STRING` |  |
| `JSON` | `JSON` |  |
| `BLOB` | `BYTES` |  |
| `BYTE` | `BYTES` |  |
| `VARBYTE` | `BYTES` |  |
| `DATE` | `DATE` | BigQuery 不支援自訂格式，這與 Teradata 搭配 DataForm 在 SDF 中支援的格式類似。 |
| `TIME` | `TIME` |  |
| `TIME WITH TIME ZONE` | `TIME` | Teradata 會以世界標準時間 (UTC) 儲存 `TIME` 資料類型，並允許您使用 `WITH TIME ZONE` 語法傳遞與 UTC 的時差。BigQuery 中的 `TIME` 資料類型代表與任何日期或時區無關的時間。 |
| `TIMESTAMP` | `TIMESTAMP` | Teradata 和 BigQuery `TIMESTAMP` 資料類型都具有微秒精確度 (但 Teradata 支援閏秒，BigQuery 則不支援)。    Teradata 和 BigQuery 資料類型通常與世界標準時間時區相關聯 ([詳細資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_zones))。 |
| `TIMESTAMP WITH TIME ZONE` | `TIMESTAMP` | Teradata `TIMESTAMP` 可在整個系統、個別使用者或個別資料欄 (使用 `WITH TIME ZONE`) 設定不同的時區。    如果您未明確指定時區，BigQuery `TIMESTAMP` 類型會假設為世界標準時間。請務必正確匯出時區資訊 (請勿在沒有時區資訊的情況下串連 `DATE` 和 `TIME` 值)，以便 BigQuery 在匯入時轉換。或是在匯出前，務必將時區資訊轉換為世界標準時間。    BigQuery 具有 `DATETIME`，可做為民用時間 (輸出時不會顯示時區) 和 `TIMESTAMP` (精確的時間點，一律顯示世界標準時間時區) 之間的抽象概念。 |
| `ARRAY` | `ARRAY` |  |
| `MULTI-DIMENSIONAL ARRAY` | `ARRAY` | 在 BigQuery 中，使用 struct 陣列，每個 struct 包含 `ARRAY` 類型的欄位 (詳情請參閱 BigQuery [說明文件](https://docs.cloud.google.com/bigquery/docs/arrays?hl=zh-tw#building_arrays_of_arrays))。 |
| `INTERVAL HOUR` | `INT64` |  |
| `INTERVAL MINUTE` | `INT64` |  |
| `INTERVAL SECOND` | `INT64` |  |
| `INTERVAL DAY` | `INT64` |  |
| `INTERVAL MONTH` | `INT64` |  |
| `INTERVAL YEAR` | `INT64` |  |
| `PERIOD(DATE)` | `DATE`，`DATE` | `PERIOD(DATE)` 應轉換為兩個包含開始日期和結束日期的 `DATE` 欄，以便與視窗函式搭配使用。 |
| `PERIOD(TIMESTAMP WITH TIME ZONE)` | `TIMESTAMP`，`TIMESTAMP` |  |
| `PERIOD(TIMESTAMP)` | `TIMESTAMP`，`TIMESTAMP` |  |
| `PERIOD(TIME)` | `TIME`，`TIME` |  |
| `PERIOD(TIME WITH TIME ZONE)` | `TIME`，`TIME` |  |
| `UDT` | `STRING` |  |
| `XML` |  |