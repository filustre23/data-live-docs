Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 指定結構定義

BigQuery 可讓您在將資料載入資料表，以及建立空白資料表時指定資料表結構定義。此外，您也可以針對支援的資料格式，使用結構定義[自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw#auto-detect)功能。

載入 Avro、Parquet、ORC、Firestore 匯出檔案或 Datastore 匯出檔案時，系統會自動從自述式來源資料擷取結構定義。

您可以透過下列方式指定資料表的結構定義：

* 使用 Google Cloud 控制台。
* 使用 `CREATE TABLE` SQL 陳述式。
* 使用 bq 指令列工具內嵌。
* 以 JSON 格式建立結構定義檔案。
* 呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法，並設定 `load` 工作設定中的 `schema` 屬性。
* 呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法，並使用 `schema` 屬性，設定[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)中的結構定義。

載入資料或建立空白資料表之後，您可以[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。

## 結構定義元件

當您指定資料表結構定義時，您必須提供每個資料欄的名稱和資料類型。您也可以提供資料欄的說明、模式和預設值。

### 欄名稱

欄名可包含英文字母 (a-z、A-Z)、數字 (0-9) 或底線 (\_)，且開頭必須是英文字母或底線。如果您使用彈性資料欄名稱，BigQuery 支援以數字開頭的資料欄名稱。請謹慎使用數字開頭的資料欄，因為使用 BigQuery Storage Read API 或 BigQuery Storage Write API 時，如果資料欄名稱開頭是數字，需要特別處理。如要進一步瞭解彈性資料欄名稱支援功能，請參閱「[彈性資料欄名稱](#flexible-column-names)」。

欄名的長度上限為 300 個字元。資料欄名稱不得使用以下任何一個前置字串：

* `_TABLE_`
* `_FILE_`
* `_PARTITION`
* `_ROW_TIMESTAMP`
* `__ROOT__`
* `_COLIDENTIFIER`
* `_CHANGE_SEQUENCE_NUMBER`
* `_CHANGE_TYPE`
* `_CHANGE_TIMESTAMP`

資料欄名稱不得重複，即使大小寫不同也是如此。舉例來說，系統會將 `Column1` 和 `column1` 這兩個資料欄名稱視為相同。如要進一步瞭解資料欄命名規則，請參閱 GoogleSQL 參考資料中的「[資料欄名稱](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#column_names)」。

如果資料表名稱 (例如 `test`) 與其中一個資料欄名稱 (例如 `test`) 相同，`SELECT` 運算式會將 `test` 資料欄解讀為包含所有其他資料表資料欄的 `STRUCT`。如要避免發生這種衝突，請使用下列其中一種方法：

* 請勿為表格及其資料欄使用相同名稱。
* 請避免使用 `_field_` 做為資料欄名稱前置字串。系統保留的前置字元會導致查詢期間自動重新命名。舉例來說，`SELECT _field_ FROM project1.dataset.test` 查詢會傳回名為 `_field_1` 的資料欄。如要查詢具有這個名稱的資料欄，請使用別名控制輸出內容。
* 為表格指派其他別名。舉例來說，下列查詢會將資料表別名 `t` 指派給資料表 `project1.dataset.test`：

  ```
  SELECT test FROM project1.dataset.test AS t;
  ```
* 參照資料欄時，請一併提供資料表名稱。例如：

  ```
  SELECT test.test FROM project1.dataset.test;
  ```

### 彈性設定資料欄名稱

資料欄名稱的命名方式更靈活，包括擴大支援非英文語言的字元，以及其他符號。如果彈性資料欄名稱是[加上引號的 ID](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#quoted_identifiers)，請務必使用倒引號 (`` ` ``) 字元括住。

彈性資料欄名稱支援下列字元：

* 任何語言的任何字母，以 Unicode 規則運算式 [`\p{L}`](https://www.unicode.org/reports/tr44/#General_Category_Values) 表示。
* 任何語言的任何數字字元，以 Unicode 正規運算式 [`\p{N}`](https://www.unicode.org/reports/tr44/#General_Category_Values) 表示。
* 任何連接符號字元，包括底線，以 Unicode 規則運算式 [`\p{Pc}`](https://www.unicode.org/reports/tr44/#General_Category_Values) 表示。
* 連字號或破折號，以 Unicode 規則運算式 [`\p{Pd}`](https://www.unicode.org/reports/tr44/#General_Category_Values) 表示。
* 任何預期會與另一個字元搭配使用的標記，以 Unicode 規則運算式 [`\p{M}`](https://www.unicode.org/reports/tr44/#General_Category_Values) 表示。例如重音符號、母音變音或外框。
* 下列特殊字元：
  + 以 Unicode 規則運算式 `\u0026` 表示的連接符號 (`&`)。
  + 百分比符號 (`%`)，以 Unicode 規則運算式 `\u0025` 表示。
  + 等號 (`=`)，以 Unicode 規則運算式 `\u003D` 表示。
  + 加號 (`+`)，以 Unicode 規則運算式 `\u002B` 表示。
  + 冒號 (`:`)，以 Unicode 規則運算式 `\u003A` 表示。
  + 以 Unicode 規則運算式 `\u0027` 表示的單引號 (`'`)。
  + 小於符號 (`<`)，以 Unicode 正規運算式 `\u003C` 表示。
  + 大於符號 (`>`)，以 Unicode 規則運算式 `\u003E` 表示。
  + 井號 (`#`)，以 Unicode 正則運算式 `\u0023` 表示。
  + 垂直線 (`|`)，以 Unicode 規則運算式 `\u007c` 表示。
  + 空格字元。

彈性資料欄名稱不支援下列特殊字元：

* 驚嘆號 (`!`)，以 Unicode 規則運算式 `\u0021` 表示。
* 半形雙引號 (`"`)，以 Unicode 規則運算式 `\u0022` 表示。
* 以 Unicode 規則運算式 `\u0024` 表示的錢幣符號 (`$`)。
* 左括號 (`(`)，以 Unicode 規則運算式 `\u0028` 表示。
* 右括號 (`)`)，以 Unicode 規則運算式 `\u0029` 表示。
* 星號 (`*`)，以 Unicode 規則運算式 `\u002A` 表示。
* 以 Unicode 規則運算式 `\u002C` 表示的逗號 (`,`)。
* 句號 (`.`)，以 Unicode 規則運算式 `\u002E` 表示。使用資料欄名稱字元對應時，Parquet 檔案資料欄名稱中的句號*不會*替換為底線。詳情請參閱[彈性資料欄限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#limitations_2)。
* 斜線 (`/`)，以 Unicode 規則運算式 `\u002F` 表示。
* 以 Unicode 規則運算式 `\u003B` 表示的分號 (`;`)。
* 問號 (`?`)，以 Unicode 規則運算式 `\u003F` 表示。
* 以 Unicode 規則運算式 `\u0040` 表示的 at 符號 (`@`)。
* 左方括號 (`[`)，以 Unicode 規則運算式 `\u005B` 表示。
* 反斜線 (`\`)，以 Unicode 規則運算式 `\u005C` 表示。
* 右方括號 (`]`)，以 Unicode 正則運算式 `\u005D` 表示。
* Unicode 規則運算式 `\u005E` 代表的揚抑符號 (`^`)。
* Unicode 規則運算式 `\u0060` 代表的重音符 (`` ` ``)。
* 左大括號 {`{`)，以 Unicode 規則運算式 `\u007B` 表示。
* 右大括號 (`}`)，以 Unicode 正則運算式 `\u007D` 表示。
* 波浪號 (`~`)，以 Unicode 規則運算式 `\u007E` 表示。

如需其他規範，請參閱「[資料欄名稱](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#column_names)」。

BigQuery Storage Read API 和 BigQuery Storage Write API 都支援擴充的欄字元。如要透過 BigQuery Storage Read API 使用擴充的 Unicode 字元清單，必須設定旗標。您可以使用 `displayName` 屬性擷取資料欄名稱。以下範例說明如何使用 Python 用戶端設定旗標：

```
from google.cloud.bigquery_storage import types
requested_session = types.ReadSession()

#set avro serialization options for flexible column.
options = types.AvroSerializationOptions()
options.enable_display_name_attribute = True
requested_session.read_options.avro_serialization_options = options
```

如要透過 BigQuery Storage Write API 使用擴充的 Unicode 字元清單，您必須提供含有 `column_name` 標記的結構定義，除非您使用 `JsonStreamWriter` 寫入器物件。以下範例說明如何提供結構定義：

```
syntax = "proto2";
package mypackage;
// Source protos located in github.com/googleapis/googleapis
import "google/cloud/bigquery/storage/v1/annotations.proto";

message FlexibleSchema {
  optional string item_name_column = 1
  [(.google.cloud.bigquery.storage.v1.column_name) = "name-列"];
  optional string item_description_column = 2
  [(.google.cloud.bigquery.storage.v1.column_name) = "description-列"];
}
```

在本範例中，`item_name_column` 和 `item_description_column` 是預留位置名稱，必須符合[通訊協定緩衝區](https://protobuf.dev/)命名慣例。請注意，`column_name` 註解一律優先於預留位置名稱。

#### 限制

* 系統不支援[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)的彈性資料欄名稱。

### 資料欄說明

每個資料欄可視需要納入說明。說明的長度上限為 1024 個字元。

### 預設值

資料欄的[預設值](https://docs.cloud.google.com/bigquery/docs/default-values?hl=zh-tw)必須是[常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#literals)或下列其中一個函式：

* [`CURRENT_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#current_date)
* [`CURRENT_DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#current_datetime)
* [`CURRENT_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#current_time)
* [`CURRENT_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#current_timestamp)
* [`GENERATE_UUID`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/utility-functions?hl=zh-tw#generate_uuid)
* [`RAND`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw#rand)
* [`SESSION_USER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/security_functions?hl=zh-tw#session_user)
* [`ST_GEOGPOINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogpoint)

### GoogleSQL 資料類型

您可以在結構定義中指定下列 GoogleSQL 資料類型。資料類型為必要項目。

| 名稱 | 資料類型 | 說明 |
| --- | --- | --- |
| [整數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types) | `INT64` | 不包含小數的數值 |
| [浮點](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#floating_point_types) | `FLOAT64` | 具有小數的概略數值 |
| [數字](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_type) | `NUMERIC` | 包含小數的精確數值 |
| [BigNumeric](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#bignumeric_type) | `BIGNUMERIC` | 包含小數的精確數值 |
| [布林](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#boolean_type) | `BOOL` | TRUE 或 FALSE (不區分大小寫) |
| [字串](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#string_type) | `STRING` | 變數長度字元 (Unicode) 資料 |
| [位元組](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#bytes_type) | `BYTES` | 變數長度二進位資料 |
| [日期](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type) | `DATE` | 邏輯日曆日期 |
| [日期/時間](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#datetime_type) | `DATETIME` | 年、月、日、時、分、秒和亞秒 |
| [時間](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_type) | `TIME` | 時間；與特定日期無關 |
| [時間戳記](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type) | `TIMESTAMP` | 絕對時間點 (精確度高達微秒) |
| [結構 (記錄)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type) | `STRUCT` | 已排序欄位的容器，每個容器都有一個類型 (必填) 和欄位名稱 (選填) |
| [地理](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#geography_type) | `GEOGRAPHY` | 地表上的地理資訊點集合 ([WGS84](http://earth-info.nga.mil/GandG/update/index.php) 參考橢球體上的點、線與多邊形集合，含測地線) |
| [JSON](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#json_type) | `JSON` | 代表 JSON，這是一種輕量型資料交換格式 |
| [RANGE](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/range-functions?hl=zh-tw#range) | `RANGE` | `DATE`、`DATETIME` 或 `TIMESTAMP` 值範圍 |

如要進一步瞭解 GoogleSQL 中的資料類型，請參閱「[GoogleSQL 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)」。

查詢資料時，您也可以聲明陣列類型。詳情請參閱「[使用陣列](https://docs.cloud.google.com/bigquery/docs/arrays?hl=zh-tw)」。

### 模式

BigQuery 支援下列資料欄模式；模式為選用項目。假如未指定模式，資料欄會預設為 `NULLABLE`。

| 模式 | 說明 |
| --- | --- |
| 是否可為空值 | 資料欄允許 `NULL` 值 (預設) |
| 必填 | 不得輸入 `NULL` 值 |
| 重複 | 資料欄包含指定類型的值陣列 |

如要進一步瞭解模式，請參閱 [`TableFieldSchema`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#TableFieldSchema) 中的 `mode`。

### 捨入模式

如果資料欄是 `NUMERIC` 或 `BIGNUMERIC` 類型，您可以設定[`rounding_mode` 資料欄選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#column_option_list)，決定將值寫入表格時的捨入方式。您可以在頂層資料欄或 `STRUCT` 欄位中設定 `rounding_mode` 選項。支援的捨入模式如下：

* `"ROUND_HALF_AWAY_FROM_ZERO"`：這個模式 (預設) 會將中間值四捨五入。
* `"ROUND_HALF_EVEN"`：這個模式會將中間值四捨五入至最接近的偶數。

如果資料欄不是 `NUMERIC` 或 `BIGNUMERIC` 類型，就無法設定 `rounding_mode` 選項。如要進一步瞭解這些類型，請參閱[十進位類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#decimal_types)。

下列範例會建立資料表，並根據資料欄的捨入模式插入捨入值：

```
CREATE TABLE mydataset.mytable (
  x NUMERIC(5,2) OPTIONS (rounding_mode='ROUND_HALF_EVEN'),
  y NUMERIC(5,2) OPTIONS (rounding_mode='ROUND_HALF_AWAY_FROM_ZERO')
);
INSERT mydataset.mytable (x, y)
VALUES (NUMERIC "1.025", NUMERIC "1.025"),
       (NUMERIC "1.0251", NUMERIC "1.0251"),
       (NUMERIC "1.035", NUMERIC "1.035"),
       (NUMERIC "-1.025", NUMERIC "-1.025");
```

資料表 `mytable` 如下所示：

```
+-------+-------+
| x     | y     |
+-------+-------+
| 1.02  | 1.03  |
| 1.03  | 1.03  |
| 1.04  | 1.04  |
| -1.02 | -1.03 |
+-------+-------+
```

詳情請參閱 [`TableFieldSchema`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#TableFieldSchema) 中的 `roundingMode`。

## 指定結構定義

載入資料或建立空白資料表時，您可以使用 Google Cloud 控制台或 bq 指令列工具指定資料表的結構定義。載入 CSV 與 JSON (以換行符號分隔) 檔時，系統支援指定結構定義。載入 Avro、Parquet、ORC、Firestore 匯出資料或 Datastore 匯出資料時，系統會自動從自述式來源資料擷取結構定義。

如何指定資料表結構定義：

### 控制台

在 Google Cloud 控制台中，您可以使用「新增欄位」選項或「以文字形式編輯」選項指定結構定義。

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，按一下「Datasets」(資料集)，然後點選您的資料集。
4. 在詳細資料窗格中，按一下「建立資料表」
   add\_box。
5. 在「Create table」(建立資料表) 頁面的「Source」(來源) 區段中，選取 [Empty table] (空白資料表)。
6. 在「Create table」(建立資料表) 頁面的「Destination」(目的地) 區段中：

   * 為「Dataset name」(資料集名稱)，選擇適當的資料集
   * 在「Table name」(資料表名稱) 欄位中，輸入您建立資料表時所使用的名稱。
   * 確認「Table type」(資料表類型) 設為「Native table」(原生資料表)。
7. 在「Schema」(結構定義) 部分輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。

   * 選項 1：使用「新增欄位」，並指定每個欄位的名稱、[類型](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#standard_sql_data_types)和[模式](#modes)。
   * 選項 2：按一下 [Edit as Text] (以文字形式編輯)，然後以 JSON 陣列的形式貼上結構定義。如果您使用 JSON 陣列，可透過與[建立 JSON 結構定義檔](#specifying_a_json_schema_file)一樣的程序產生結構定義。
8. 點選「建立資料表」。

### SQL

使用 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)。使用 [column](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#column_name_and_column_schema) 選項指定結構定義。下列範例會建立名為 `newtable` 的新資料表，其中包含 x、y、z 資料欄，類型分別為整數、字串和布林值：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE IF NOT EXISTS mydataset.newtable (x INT64, y STRING, z BOOL)
     OPTIONS(
       description = 'My example table');
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用下列其中一個指令，以內嵌方式提供 `field:data_type,field:data_type` 格式的結構定義：

* 如果要載入資料，請使用 `bq load` 指令。
* 如要建立空白資料表，請使用 `bq mk` 指令。

在指令列中指定結構定義時，無法加入 `RECORD` ([`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)) 或 [`RANGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/range-functions?hl=zh-tw) 類型，也不能加入資料欄說明，以及指定資料欄模式。所有模式均會使用預設設定 `NULLABLE`。如要加入說明、模式、`RECORD` 類型和 `RANGE` 類型，請改為提供 [JSON 結構定義檔](#specifying_a_json_schema_file)。

如要使用內嵌結構定義將資料載入資料表，請輸入 `load` 指令並使用 `--source_format` 旗標指定資料格式。如要將資料載入預設專案以外的專案中，請使用下列格式加上專案 ID：`project_id:dataset.table_name`。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

```
bq --location=location load \
--source_format=format \
project_id:dataset.table_name \
path_to_source \
schema
```

更改下列內容：

* `location`：位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)，設定該位置的預設值。
* `format`：`NEWLINE_DELIMITED_JSON` 或 `CSV`。
* `project_id`：您的專案 ID。
* `dataset`：包含您要載入資料的資料表。
* `table_name`：您要載入資料的資料表名稱。
* `path_to_source`：您本機或 Cloud Storage 上的 CSV 或 JSON 資料檔案位置。
* `schema`：內嵌結構定義。

範例：

輸入下列指令，將資料從名為 `myfile.csv` 的本機 CSV 檔案載入預設專案中的 `mydataset.mytable`。結構定義是以內嵌方式指定。

```
bq load \
--source_format=CSV \
mydataset.mytable \
./myfile.csv \
qtr:STRING,sales:FLOAT,year:STRING
```

如要進一步瞭解如何將資料載入 BigQuery，請參閱「[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」。

如要在建立空白資料表時指定內嵌結構定義，請搭配 `--table` 或 `-t` 旗標輸入 `bq mk` 指令。如要建立非預設專案中的資料表，請使用下列格式將專案 ID 新增至指令：`project_id:dataset.table`。

```
bq mk --table project_id:dataset.table schema
```

更改下列內容：

* `project_id`：您的專案 ID。
* `dataset`：專案中的資料集。
* `table`：您要建立的資料表名稱。
* `schema`：內嵌結構定義。

舉例來說，下列指令會在預設專案中建立名為 `mytable` 的空白資料表。結構定義是以內嵌方式指定。

```
bq mk --table mydataset.mytable qtr:STRING,sales:FLOAT,year:STRING
```

如要進一步瞭解如何建立空白資料表，請參閱[建立含有結構定義的空白資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create_an_empty_table_with_a_schema_definition)。

### C#

將資料載入資料表時，如何指定資料表的結構定義：

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Apis.Bigquery.v2.Data;
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryLoadTableGcsJson
{
    public void LoadTableGcsJson(
        string projectId = "your-project-id",
        string datasetId = "your_dataset_id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        var gcsURI = "gs://cloud-samples-data/bigquery/us-states/us-states.json";
        var dataset = client.GetDataset(datasetId);
        var schema = new TableSchemaBuilder {
            { "name", BigQueryDbType.String },
            { "post_abbr", BigQueryDbType.String }
        }.Build();
        TableReference destinationTableRef = dataset.GetTableReference(
            tableId: "us_states");
        // Create job configuration
        var jobOptions = new CreateLoadJobOptions()
        {
            SourceFormat = FileFormat.NewlineDelimitedJson
        };
        // Create and run job
        BigQueryJob loadJob = client.CreateLoadJob(
            sourceUri: gcsURI, destination: destinationTableRef,
            schema: schema, options: jobOptions);
        loadJob = loadJob.PollUntilCompleted().ThrowOnAnyError();  // Waits for the job to complete.
        // Display the number of rows uploaded
        BigQueryTable table = client.GetTable(destinationTableRef);
        Console.WriteLine(
            $"Loaded {table.Resource.NumRows} rows to {table.FullyQualifiedId}");
    }
}
```

建立空白資料表時，如何指定結構定義：

```
using Google.Cloud.BigQuery.V2;

public class BigQueryCreateTable
{
    public BigQueryTable CreateTable(
        string projectId = "your-project-id",
        string datasetId = "your_dataset_id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        var dataset = client.GetDataset(datasetId);
        // Create schema for new table.
        var schema = new TableSchemaBuilder
        {
            { "full_name", BigQueryDbType.String },
            { "age", BigQueryDbType.Int64 }
        }.Build();
        // Create the table
        return dataset.CreateTable(tableId: "your_table_id", schema: schema);
    }
}
```

### Go

將資料載入資料表時，如何指定資料表的結構定義：

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// importJSONExplicitSchema demonstrates loading newline-delimited JSON data from Cloud Storage
// into a BigQuery table and providing an explicit schema for the data.
func importJSONExplicitSchema(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states.json")
	gcsRef.SourceFormat = bigquery.JSON
	gcsRef.Schema = bigquery.Schema{
		{Name: "name", Type: bigquery.StringFieldType},
		{Name: "post_abbr", Type: bigquery.StringFieldType},
	}
	loader := client.Dataset(datasetID).Table(tableID).LoaderFrom(gcsRef)
	loader.WriteDisposition = bigquery.WriteEmpty

	job, err := loader.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}

	if status.Err() != nil {
		return fmt.Errorf("job completed with error: %v", status.Err())
	}
	return nil
}
```

建立空白資料表時，如何指定結構定義：

```
import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
)

// createTableExplicitSchema demonstrates creating a new BigQuery table and specifying a schema.
func createTableExplicitSchema(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydatasetid"
	// tableID := "mytableid"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	sampleSchema := bigquery.Schema{
		{Name: "full_name", Type: bigquery.StringFieldType},
		{Name: "age", Type: bigquery.IntegerFieldType},
	}

	metaData := &bigquery.TableMetadata{
		Schema:         sampleSchema,
		ExpirationTime: time.Now().AddDate(1, 0, 0), // Table will be automatically deleted in 1 year.
	}
	tableRef := client.Dataset(datasetID).Table(tableID)
	if err := tableRef.Create(ctx, metaData); err != nil {
		return err
	}
	return nil
}
```

### Java

將資料載入資料表時，如何指定資料表的結構定義：

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.TableId;

// Sample to load JSON data from Cloud Storage into a new BigQuery table
public class LoadJsonFromGCS {

  public static void runLoadJsonFromGCS() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.json";
    Schema schema =
        Schema.of(
            Field.of("name", StandardSQLTypeName.STRING),
            Field.of("post_abbr", StandardSQLTypeName.STRING));
    loadJsonFromGCS(datasetName, tableName, sourceUri, schema);
  }

  public static void loadJsonFromGCS(
      String datasetName, String tableName, String sourceUri, Schema schema) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      LoadJobConfiguration loadConfig =
          LoadJobConfiguration.newBuilder(tableId, sourceUri)
              .setFormatOptions(FormatOptions.json())
              .setSchema(schema)
              .build();

      // Load data from a GCS JSON file into the table
      Job job = bigquery.create(JobInfo.of(loadConfig));
      // Blocks until this load table job completes its execution, either failing or succeeding.
      job = job.waitFor();
      if (job.isDone()) {
        System.out.println("Json from GCS successfully loaded in a table");
      } else {
        System.out.println(
            "BigQuery was unable to load into the table due to an error:"
                + job.getStatus().getError());
      }
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Column not added during load append \n" + e.toString());
    }
  }
}
```

建立空白資料表時，如何指定結構定義：

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.StandardTableDefinition;
import com.google.cloud.bigquery.TableDefinition;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;

public class CreateTable {

  public static void runCreateTable() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    Schema schema =
        Schema.of(
            Field.of("stringField", StandardSQLTypeName.STRING),
            Field.of("booleanField", StandardSQLTypeName.BOOL));
    createTable(datasetName, tableName, schema);
  }

  public static void createTable(String datasetName, String tableName, Schema schema) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      TableDefinition tableDefinition = StandardTableDefinition.of(schema);
      TableInfo tableInfo = TableInfo.newBuilder(tableId, tableDefinition).build();

      bigquery.create(tableInfo);
      System.out.println("Table created successfully");
    } catch (BigQueryException e) {
      System.out.println("Table was not created. \n" + e.toString());
    }
  }
}
```

### Python

將資料載入資料表時，如要指定資料表的結構定義，請設定 [LoadJobConfig.schema](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_schema) 屬性。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ],
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
)
uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"

load_job = client.load_table_from_uri(
    uri,
    table_id,
    location="US",  # Must match the destination dataset location.
    job_config=job_config,
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
```

如要在建立空白資料表時指定結構定義，請設定 [Table.schema](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.Table?hl=zh-tw#google_cloud_bigquery_table_Table_schema) 屬性。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"

schema = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)
```

## 指定 JSON 結構定義檔

如果不想使用內嵌結構定義，也可以改用 JSON 結構定義檔指定結構定義。JSON 結構定義檔是由包含以下項目的 JSON 陣列所組成：

* 資料欄的[名稱](#column_names)
* 資料欄的[資料類型](#standard_sql_data_types)
* 選用：資料欄的[模式](#modes) (如果未指定，模式預設為 `NULLABLE`)
* 選用：資料欄的欄位 (如果是 [`STRUCT` 類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type))
* 選用：資料欄的[說明](#column_descriptions)
* 選用：資料欄的[政策標記](https://docs.cloud.google.com/data-catalog/docs/policy-tags?hl=zh-tw)，用於欄位層級的存取控管
* 選用：`STRING` 或 `BYTES` 類型的資料欄值長度上限
* 選用：`NUMERIC` 或 `BIGNUMERIC` 類型的資料欄[精確度](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#decimal_types)
* 選用：`NUMERIC` 或 `BIGNUMERIC` 類型的資料欄[比例](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#decimal_types)
* 選用：資料欄的[排序規則](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw) (適用於 `STRING` 類型)
* 選用：資料欄的[預設值](https://docs.cloud.google.com/bigquery/docs/default-values?hl=zh-tw)
* 選用：資料欄的[捨入模式](#rounding_mode) (如果資料欄為 `NUMERIC` 或 `BIGNUMERIC` 類型)

**注意：** 您也可以使用 Google Cloud 控制台的「Edit as Text」(以文字形式編輯) 選項，指定在結構定義檔中建立的 JSON 陣列。也可以做為在 API 中設定 [`schema`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#tableschema) 屬性的起點。

### 建立 JSON 結構定義檔

如要建立 JSON 結構定義檔，請為每個資料欄輸入 [`TableFieldSchema`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#TableFieldSchema)。`name` 和 `type` 為必要欄位，其他欄位則為選填。

```
[
  {
    "name": string,
    "type": string,
    "mode": string,
    "fields": [
      {
        object (TableFieldSchema)
      }
    ],
    "description": string,
    "policyTags": {
      "names": [
        string
      ]
    },
    "maxLength": string,
    "precision": string,
    "scale": string,
    "collation": string,
    "defaultValueExpression": string,
    "roundingMode": string
  },
  {
    "name": string,
    "type": string,
    ...
  }
]
```

如果資料欄是 `RANGE<T>` 類型，請使用 `rangeElementType` 欄位描述 `T`，其中 `T` 必須是 `DATE`、`DATETIME` 或 `TIMESTAMP`。

```
[
  {
    "name": "duration",
    "type": "RANGE",
    "mode": "NULLABLE",
    "rangeElementType": {
      "type": "DATE"
    }
  }
]
```

JSON 陣列會包含在括號 `[]` 中。每個資料欄都必須以半形逗號分隔 (`},`)。

如要將現有資料表結構定義寫入本機檔案，請執行下列操作：

### bq

```
bq show \
--schema \
--format=prettyjson \
project_id:dataset.table > path_to_file
```

更改下列內容：

* `project_id`：您的專案 ID。
* `dataset`：專案中的資料集。
* `table`：現有資料表結構定義的名稱。
* `path_to_file`：您要將資料表結構定義寫入的本機檔案位置。

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要使用 Python 用戶端程式庫，從資料表寫入結構定義 JSON 檔案，請呼叫 [Client.schema\_to\_json](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_schema_to_json) 方法。

```
from google.cloud import bigquery

client = bigquery.Client()

# TODO(dev): Change the table_id variable to the full name of the
# table you want to get schema from.
table_id = "your-project.your_dataset.your_table_name"

# TODO(dev): Change schema_path variable to the path
# of your schema file.
schema_path = "path/to/schema.json"
table = client.get_table(table_id)  # Make an API request.

# Write a schema file to schema_path with the schema_to_json method.
client.schema_to_json(table.schema, schema_path)

with open(schema_path, "r", encoding="utf-8") as schema_file:
    schema_contents = schema_file.read()

# View table properties
print(f"Got table '{table.project}.{table.dataset_id}.{table.table_id}'.")
print(f"Table schema: {schema_contents}")
```

您可以使用輸出檔案做為 JSON 結構定義檔的起點。假如您使用此方法，請確定該檔案僅包含代表資料表結構定義的 JSON 陣列。

舉例來說，下列 JSON 陣列代表基本的資料表結構定義。此結構定義有三個資料欄：`qtr` (`REQUIRED` `STRING`)、`rep` (`NULLABLE` `STRING`) 和 `sales` (`NULLABLE` `FLOAT`)。

```
[
  {
    "name": "qtr",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "quarter"
  },
  {
    "name": "rep",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "sales representative"
  },
  {
    "name": "sales",
    "type": "FLOAT",
    "mode": "NULLABLE",
    "defaultValueExpression": "2.55"
  }
]
```

### 使用 JSON 結構定義檔

建立 JSON 結構定義檔後，您可以使用 bq 指令列工具指定結構定義。您無法透過 Google Cloud 控制台或 API 使用結構定義檔。

提供結構定義檔案：

* 如果要載入資料，請使用 `bq load` 指令。
* 如要建立空白資料表，請使用 `bq mk` 指令。

您提供的 JSON 結構定義檔必須儲存在可讀取的本機位置。您無法指定儲存在 Cloud Storage 或 Google 雲端硬碟中的 JSON 結構定義檔。

#### 在載入資料時指定結構定義檔

如要使用 JSON 結構定義將資料載入資料表，請按照下列步驟操作：

### bq

```
bq --location=location load \
--source_format=format \
project_id:dataset.table \
path_to_data_file \
path_to_schema_file
```

更改下列內容：

* `location`：位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)來設定位置的預設值。
* `format`：`NEWLINE_DELIMITED_JSON` 或 `CSV`。
* `project_id`：您的專案 ID。
* `dataset`：包含您要載入資料的資料表。
* `table`：您要載入資料的資料表名稱。
* `path_to_data_file`：您本機或 Cloud Storage 上的 CSV 或 JSON 資料檔案位置。
* `path_to_schema_file`：本機上結構定義檔的路徑。

範例：

輸入下列指令，將資料從名為 `myfile.csv` 的本機 CSV 檔案載入預設專案中的 `mydataset.mytable`。結構定義在目前目錄的 `myschema.json` 中指定。

```
bq load --source_format=CSV mydataset.mytable ./myfile.csv ./myschema.json
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要使用 Python 用戶端程式庫從 JSON 檔案載入資料表結構定義，請呼叫 [schema\_from\_json](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_schema_from_json) 方法。

```
from google.cloud import bigquery

client = bigquery.Client()

# TODO(dev): Change uri variable to the path of your data file.
uri = "gs://your-bucket/path/to/your-file.csv"
# TODO(dev): Change table_id to the full name of the table you want to create.
table_id = "your-project.your_dataset.your_table"
# TODO(dev): Change schema_path variable to the path of your schema file.
schema_path = "path/to/schema.json"
# To load a schema file use the schema_from_json method.
schema = client.schema_from_json(schema_path)

job_config = bigquery.LoadJobConfig(
    # To use the schema you loaded pass it into the
    # LoadJobConfig constructor.
    schema=schema,
    skip_leading_rows=1,
)

# Pass the job_config object to the load_table_from_file,
# load_table_from_json, or load_table_from_uri method
# to use the schema on a new table.
load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
print(f"Loaded {destination_table.num_rows} rows to {table_id}.")
```

#### 在建立資料表時指定結構定義檔

如要使用 JSON 結構定義檔在現有資料集中建立空白資料表，請執行下列操作：

### bq

```
bq mk --table project_id:dataset.table path_to_schema_file
```

更改下列內容：

* `project_id`：您的專案 ID。
* `dataset`：專案中的資料集。
* `table`：您要建立的資料表名稱。
* `path_to_schema_file`：本機上結構定義檔的路徑。

舉例來說，以下指令會在預設專案的 `mydataset` 中建立名為 `mytable` 的資料表。結構定義是在目前目錄的 `myschema.json` 中指定：

```
bq mk --table mydataset.mytable ./myschema.json
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要使用 Python 用戶端程式庫從 JSON 檔案載入資料表結構定義，請呼叫 [schema\_from\_json](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_schema_from_json) 方法。

```
from google.cloud import bigquery

client = bigquery.Client()

# TODO(dev): Change table_id to the
```