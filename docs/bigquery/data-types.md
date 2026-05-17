Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 舊版 SQL 資料類型

這份文件將詳細說明 BigQuery 的舊版 SQL 查詢語法支援的資料類型。建議使用的 BigQuery 查詢語法是 GoogleSQL。如要瞭解 GoogleSQL 中的資料類型，請參閱 [GoogleSQL 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)。

## 舊版 SQL 資料類型

您的資料可以包含下列資料類型：

| 資料類型 | 可能的值 |
| --- | --- |
| STRING | 變數長度字元 (UTF-8) 資料。 |
| BYTES | 變數長度二進位資料。  * 匯入的 BYTES 資料必須採用 base64 編碼，但 BigQuery 可讀取及轉換 Avro BYTES 資料。 * 從 BigQuery 資料表讀取的位元組資料會進行 base64 編碼，除非您匯出為 Avro 格式，否則會套用 Avro 位元組資料類型。 |
| INTEGER | 64 位元帶正負號整數。  如果您使用 BigQuery API 將不在 [-253+1, 253-1] 範圍內的整數 (在大多數情況下，這表示大於 9,007,199,254,740,991) 載入至整數 (INT64) 資料欄，則必須以字串形式傳遞，以免資料毀損。這個問題是由於 JSON/ECMAScript 中的整數大小有限制。詳情請參閱 [RFC 7159 的「Numbers」一節](https://www.rfc-editor.org/rfc/rfc7159.html#section-6)。 |
| FLOAT | 雙精確度浮點數格式。 |
| NUMERIC | 舊版 SQL 僅支援部分 NUMERIC 功能。詳情請參閱「[舊版 SQL 中的確切數值](#numeric-type-support)」。 |
| BIGNUMERIC | 舊版 SQL 僅支援 BIGNUMERIC 的部分功能。詳情請參閱「[舊版 SQL 中的確切數值](#numeric-type-support)」。 |
| BOOLEAN | * **CSV 格式：** `1` 或 `0`、`true` 或 `false`、`t` 或 `f`、`yes` 或 `no`、`y` 或 `n` (全部不區分大小寫)。 * **JSON 格式：** `true` 或 `false` (不區分大小寫)。 |
| RECORD | 一或多個其他欄位的集合。 |
| TIMESTAMP | 您可將 TIMESTAMP 資料類型描述為 UNIX 時間戳記或日曆日期時間。BigQuery 會在內部將 TIMESTAMP 資料儲存為 UNIX 時間戳記，精確度高達毫秒。  **UNIX 時間戳記**  正或負小數。正數指定了紀元 (1970-01-01 00:00:00 UTC) 後秒數，負數指定了紀元前秒數。最高保留 6 位小數 (精確度達到毫秒)。  **日期和時間字串**  日期和時間字串，格式為 `YYYY-MM-DD HH:MM:SS`。支援 `UTC` 和 `Z` 指定碼。  您可在日期與時間字串中提供時區偏移量，但 BigQuery 不在將值轉換為它的內部格式之後保留偏移量。如果您需要保留原始時區資料，請將時區偏移量儲存在另一個資料欄中。當您指定個位數時區偏移量時，開頭必須是零。  使用 JSON 格式時，日期與時間字串都必須加上引號。  **範例**  以下範例顯示以 UNIX 時間戳記與日期和時間字串格式描述特定日期的相同方法。   | 事件 | UNIX 時間戳記格式 | 日期/時間字串格式 | | --- | --- | --- | | 奧克拉荷馬市附近的輕微 (M4.2) 地震 | ``` 1408452095.220 1408452095.220000 ``` | ``` 2014-08-19 07:41:35.220 -05:00 2014-08-19 12:41:35.220 UTC 2014-08-19 12:41:35.220 2014-08-19 12:41:35.220000 2014-08-19T12:41:35.220Z ``` | | 尼爾‧阿姆斯壯在月球上踏上第一步 | ``` -14182916 ``` | ``` 1969-07-20 20:18:04 1969-07-20 20:18:04 UTC 1969-07-20T20:18:04 ``` | | 修正 [Y10k 錯誤](https://en.wikipedia.org/wiki/Year_10,000_problem)的期限 | ``` 253402300800 2.53402300800e11 ``` | ``` 10000-01-01 00:00 ``` | |
| DATE | 舊版 SQL 對於 DATE 的支援有限。詳情請參閱[舊版 SQL 中的民用時](#civil-time)。 |
| 時間 | 舊版 SQL 對於 TIME 的支援有限。詳情請參閱[舊版 SQL 中的民用時](#civil-time)。 |
| DATETIME | 舊版 SQL 對於 DATETIME 的支援有限。詳情請參閱[舊版 SQL 中的民用時](#civil-time)。 |

## 舊版 SQL 中的精確數值

您可以在 `SELECT list (with aliases)`、`GROUP BY keys` 和視窗函式中的傳遞欄位等非修改子句中讀取 NUMERIC 或 BIGNUMERIC 值。不過，任何涉及 NUMERIC 或 BIGNUMERIC 值的運算 (包括比較) 都會產生未定義的結果。

舊版 SQL 支援以下 cast 和 conversion 函數：

* `CAST(<numeric> AS STRING)`
* `CAST(<bignumeric> AS STRING)`
* `CAST(<string> AS NUMERIC)`
* `CAST(<string> AS BIGNUMERIC)`

## 舊版 SQL 中的民用時

您可以讀取民用時間資料類型 (DATE、TIME 和 DATETIME)，並使用 `SELECT list (with aliases)`、`GROUP BY keys` 和視窗函式中的傳遞欄位等非修改運算子加以處理。不過，任何針對民用時間值 (包括比較) 的其他運算，都會產生未定義的結果。

舊版 SQL 支援下列 casts 與 conversion 函式：

* `CAST(<date> AS STRING)`
* `CAST(<time> AS STRING)`
* `CAST(<datetime> AS STRING)`
* `CAST(<string> AS DATE)`
* `CAST(<string> AS TIME)`
* `CAST(<string> AS DATETIME)`

實際上，舊版 SQL 會將民用時值解讀為整數，您以為對整數的運算是民用時值的結果，其實是產生非預期的結果。

如要使用民用時間資料類型計算值，請考慮使用 [GoogleSQL](https://docs.cloud.google.com/bigquery/sql-reference?hl=zh-tw)。GoogleSQL 支援對 [DATE](https://docs.cloud.google.com/bigquery/sql-reference/data-types?hl=zh-tw#date-type)、[DATETIME](https://docs.cloud.google.com/bigquery/sql-reference/data-types?hl=zh-tw#datetime-type) 和 [TIME](https://docs.cloud.google.com/bigquery/sql-reference/data-types?hl=zh-tw#time-type) 資料類型的所有 SQL 作業。

## 後續步驟

* 如要使用 API 設定欄位的資料類型，請參閱 [`schema.fields.type`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#TableFieldSchema.FIELDS.type)。
* 如需 GoogleSQL 資料類型，請參閱「[資料類型](https://docs.cloud.google.com/bigquery/sql-reference/data-types?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]