Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將資料匯出至 Bigtable (反向 ETL)

從 BigQuery 到 Bigtable 的反向擷取、轉換及載入 (RETL) 功能，可讓您將 BigQuery 的數據分析功能，與 Bigtable 的低延遲和高處理量結合。您可以將資料提供給應用程式使用者，同時避免耗盡 BigQuery 的配額和限制。

如要設定這項工作流程，請使用 [`EXPORT
DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)，將 BigQuery 資料表的資料匯出至 [Bigtable](https://docs.cloud.google.com/bigtable/docs/overview?hl=zh-tw) 資料表。

## Bigtable 資料表的特性

[Bigtable 資料表](https://docs.cloud.google.com/bigtable/docs/overview?hl=zh-tw#storage-model)與 BigQuery 資料表有幾項差異：

* Bigtable 和 BigQuery 資料表都是由資料列組成，但 Bigtable 資料列是由資料列索引鍵和資料欄系列組成，其中資料欄系列包含任意數量的資料欄，且這些資料欄屬於同一個資料欄系列。
* 特定資料表的資料欄系列會在建立資料表時建立，但也可以在之後新增或移除。建立資料欄系列時，不需指定屬於該系列的資料欄。
* Bigtable 資料欄不需要事先定義，只要在[資料表資料大小限制](https://docs.cloud.google.com/bigtable/quotas?hl=zh-tw#limits-data-size)內，就能以名稱 (也稱為「限定詞」) 儲存資料。
* Bigtable 資料欄可以包含[資料表資料大小限制](https://docs.cloud.google.com/bigtable/quotas?hl=zh-tw#limits-data-size)內的任何二進位值。
* Bigtable 資料欄一律具有時間維度 (也稱為「版本」)。只要時間戳記不相同，任何資料列的同一資料欄中都可以儲存任意數量的資料。
* Bigtable 時間戳記是以 [Unix 紀元時間](https://en.wikipedia.org/wiki/Unix_time)起算的微秒數為單位，例如 0 代表 1970-01-01T00:00:00 UTC。時間戳記必須是非負數的微秒值，精細程度為毫秒 (僅接受 1000 微秒的倍數)。預設 Bigtable 時間戳記為 0。
* Bigtable 中的資料是[依資料列索引鍵、多個資料列索引鍵、資料列索引鍵範圍或使用篩選器讀取](https://docs.cloud.google.com/bigtable/docs/reads?hl=zh-tw)。除了完整資料表掃描外，所有類型的讀取要求都至少須有一個資料列索引鍵或資料列索引鍵範圍。

如要瞭解如何準備 BigQuery 結果，以便匯出至 Bigtable，請參閱「[準備要匯出的查詢結果](#prepare_results)」。

## 事前準備

* 如要接收匯出的資料，您必須建立 [Bigtable 執行個體](https://docs.cloud.google.com/bigtable/docs/creating-instance?hl=zh-tw)和 [Bigtable 資料表](https://docs.cloud.google.com/bigtable/docs/managing-tables?hl=zh-tw#create-table)
* 如要使用這項功能，請建立 [BigQuery Enterprise 或 Enterprise Plus 級預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_reservations)。批次匯出需要 [`QUERY` 指派](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)，[持續匯出](#export_continuously)則需要 [`CONTINUOUS` 指派](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)。
* 授予 [Identity and Access Management (IAM) 角色](#required_roles)，讓使用者具備執行本文件中各項工作所需的權限。

### 必要的角色

如要取得將 BigQuery 資料匯出至 Bigtable 所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* 從 BigQuery 資料表匯出資料：[BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 執行擷取工作：[BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user)  (`roles/bigquery.user`)
* 將資料寫入 Bigtable 資料表：[Bigtable 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigtable?hl=zh-tw#bigtable.user)  (`roles/bigtable.user`)
* 自動為 Bigtable 資料表建立新的資料欄系列：[Bigtable 系統管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigtable?hl=zh-tw#bigtable.admin)  (`roles/bigtable.admin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 限制

* 編碼僅限 `BINARY` 和 `TEXT`。
* 目的地 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)必須設定[單一叢集轉送](https://docs.cloud.google.com/bigtable/docs/routing?hl=zh-tw#single-cluster)和[低要求優先等級](https://docs.cloud.google.com/bigtable/docs/request-priorities?hl=zh-tw)。
* Bigtable 應用程式設定檔必須設為將資料轉送至與 BigQuery 資料集位於相同位置的 Bigtable 叢集。詳情請參閱[位置考量事項](#data-locations)。
* 只有 [BigQuery Enterprise 或 Enterprise Plus 版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)支援匯出至 Bigtable。不支援 BigQuery Standard 版本和[隨選運算](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。

## 位置注意事項

* 如果 BigQuery 資料集位於多區域，則必須設定 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)，將資料轉送至該多區域內的 Bigtable 叢集。舉例來說，如果 BigQuery 資料集位於 `US` 多區域，Bigtable 叢集可以位於 `us-west1` (奧勒岡州) 區域，該區域位於美國境內。
* 如果 BigQuery 資料集位於單一區域，則必須設定 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)，將資料轉送至同一區域的 Bigtable 叢集。舉例來說，如果 BigQuery 資料集位於 `asia-northeast1` (東京) 區域，Bigtable 叢集也必須位於 `asia-northeast1` (東京) 區域。

詳情請參閱「[Bigtable 位置](https://docs.cloud.google.com/bigtable/docs/locations?hl=zh-tw)」。

## 支援的 BigQuery 類型

寫入 Bigtable 時，支援下列資料類型：

| BigQuery 類型 | 寫入的 Bigtable 值 |
| --- | --- |
| `BYTES` | 匯出時不變更。 |
| `STRING` | 已轉換為`BYTES`。 |
| `INTEGER` | 如果將 `bigtable_options.column_families.encoding` 設為 `BINARY`，系統會以 8 位元組、大端序格式 (最高有效位元組優先) 寫入值。如果 `bigtable_options.column_families.encoding` 設為 `TEXT`，則值會寫入為代表數字的人類可讀字串。 |
| `FLOAT` | 以 IEEE 754 8 位元組輸出格式寫入值。 |
| `BOOLEAN` | 如果 `bigtable_options.column_families.encoding` 設為 `BINARY`，則值會寫入為 1 位元組值 (`false` = 0x00 或 `true` = 0x01)。如果 `bigtable_options.column_families.encoding` 設為 `TEXT`，則值會寫入為文字 (`"true"` 或 `"false"`)。 |
| `JSON` | `JSON` 類型的匯出資料欄會解讀為屬於特定 Bigtable 資料欄系列的一組資料欄。JSON 物件的成員會解讀為資料欄，其值會寫入 Bigtable。您可以使用 [`bigtable_options`](#bigtable_options) 設定，調整要寫入的資料欄名稱。   例如：     ```     JSON '{"FIELD1": "VALUE1", "FIELD2": "VALUE2"}' as MY_COLUMN_FAMILY ```   其中值 VALUE1 和 VALUE2 會寫入 Bigtable，做為資料欄系列 MY\_COLUMN\_FAMILY 的資料欄 FIELD1 和 FIELD2。  **注意：**如果 JSON 文件以巢狀結構嵌入其他 `JSON` 或 `STRUCT` 類型，則會以字串形式寫入 Bigtable。匯出巢狀結構於其他結構中的 `STRUCT` 值時，須遵守「[使用 `bigtable_options` 設定匯出作業](#bigtable_options)」一節說明的限制。 |
| `STRUCT` | `STRUCT` 類型的匯出資料欄會解讀為屬於特定 Bigtable 資料欄系列的一組資料欄。struct 的成員會解讀為資料欄，其值則會寫入 Bigtable。您可以使用 [`bigtable_options`](#bigtable_options) 設定，調整要寫入的資料欄名稱。   例如：     ```     STRUCT<FIELD1  STRING, FIELD2 INTEGER> as MY_COLUMN_FAMILY ```   其中 FIELD1 和 FIELD2 值會寫入 Bigtable，做為資料欄系列 MY\_COLUMN\_FAMILY 的資料欄 FIELD1 和 FIELD2。 |

這些支援的資料類型與從 BigQuery 的[外部 Bigtable 資料表](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#bigtablecolumnfamily)讀取資料類似。

## Bigtable 中的`NULL`值

Bigtable 中的 `NULL` 值有下列限制：

* Bigtable 沒有 `NULL` 值的類似項目。在 Bigtable 中，匯出特定資料欄系列和資料欄的 `NULL` 值，會刪除 Bigtable 資料列中的現有值。
* 如果匯出前，Bigtable 值不具備指定的資料列索引鍵、資料欄系列、資料欄限定詞和時間戳記，則匯出的 `NULL` 值不會對 Bigtable 資料列產生任何影響。
* 匯出 `STRUCT` 或 `JSON` 類型的 `NULL` 值時，受影響資料列中對應資料欄系列的所有資料欄值都會刪除。您應將 `NULL` 值轉換為 `STRUCT` 或 `JSON` 類型，以便 SQL 引擎為其附加正確的類型。下列查詢會使用一組指定的資料列索引鍵，刪除資料欄系列 `column_family1` 中的所有資料：

  ```
  EXPORT DATA OPTIONS (...) AS
  SELECT
    rowkey,
  CAST(NULL as STRUCT<INT64>) AS column_family1 FROM T
  ```
* 匯出期間，系統會略過含有 `NULL` 資料列索引鍵的資料列。略過的資料列數量會傳回給呼叫端，並顯示在匯出統計資料中。

## 使用 `bigtable_options` 設定匯出作業

您可以在匯出期間使用 `bigtable_options` 設定，彌合 BigQuery 和 Bigtable 儲存模型之間的差異。設定會以 JSON 字串的形式表示，如以下範例所示：

```
EXPORT DATA OPTIONS(
   uri="https://bigtable.googleapis.com/projects/PROJECT_ID/instances/INSTANCE_ID/appProfiles/APP_PROFILE_ID/tables/TABLE",
   bigtable_options = """{
     "columnFamilies": [{
       "familyId": "COLUMN_FAMILY_NAME",
       "encoding": "ENCODING_VALUE",
       "columns": [
         {
           "qualifierString": "BIGTABLE_COLUMN_QUALIFIER",
           ["qualifierEncoded": "BASE_64_ENCODED_VALUE",]
           "fieldName": "BIGQUERY_RESULT_FIELD_NAME"
         }
       ]
    }]
   }"""
)
```

下表說明 `bigtable_options` 設定中可能使用的欄位：

| 欄位名稱 | 說明 |
| --- | --- |
| `columnFamilies` | 資料欄系列描述元的陣列。 |
| `columnFamilies.familyId` | Bigtable 資料欄系列的 ID。 |
| `columnFamilies.encoding` | 值可設為 `BINARY` 或 `TEXT`。如要瞭解類型的編碼方式，請參閱「[支援的 BigQuery 類型](#bigquery_types)」。 |
| `columnFamilies.columns` | Bigtable 資料欄對應關係陣列。 |
| `columnFamilies.columns.qualifierString` | 選用：Bigtable 資料欄限定詞。如果資料欄限定詞不含非 UTF-8 程式碼，請指定這個值。`qualifierString` 和 `qualifierEncoding` 欄位互斥。如果未指定 `qualifierString` 和 `qualifierEncoded`，系統會使用 `fieldName` 做為資料欄限定詞。 |
| `columnFamilies.columns.qualifierEncoded` | 選用：Base64 編碼的資料欄限定詞。與 `qualifierString` 類似，適用於資料欄限定詞必須包含非 UTF-8 程式碼的情況。 |
| `columnFamilies.columns.fieldName` | 必要：BigQuery 結果集欄位名稱。在某些情況下，可以為空字串。如要瞭解如何將空白 `fieldName` 值與簡單類型的欄位搭配使用，請參閱「[準備匯出查詢結果](#prepare_results)」。 |

## 準備匯出查詢結果

如要將查詢結果匯出至 Bigtable，結果必須符合下列規定：

* 結果集必須包含 `STRING` 或 `BYTES` 類型的 `rowkey` 資料欄。
* 資料列索引鍵、資料欄限定詞、值和時間戳記不得超過 Bigtable [資料表內的資料大小限制](https://docs.cloud.google.com/bigtable/quotas?hl=zh-tw#limits-data-size)。
* 結果集中至少須有一個 `rowkey` 以外的資料欄。
* 每個結果集資料欄都必須是[支援的 BigQuery 類型](#bigquery_types)之一。匯出至 Bigtable 前，請務必將所有不支援的資料欄類型轉換為支援的類型。

Bigtable 不要求資料欄限定詞必須是有效的 BigQuery 資料欄名稱，且支援使用任何位元組。如要瞭解如何覆寫匯出作業的目標資料欄限定詞，請參閱「[使用 `bigtable_options` 設定匯出作業](#bigtable_options)」。

如果您將匯出的值與 Bigtable API (例如 [`ReadModifyWriteRow`](https://docs.cloud.google.com/bigtable/docs/reference/data/rpc/google.bigtable.v2?hl=zh-tw#google.bigtable.v2.Bigtable.ReadModifyWriteRow)) 搭配使用，任何數值都必須使用正確的[二進位編碼](#bigtable_options)。

根據預設，系統會將類型不屬於 `STRUCT` 或 `JSON` 的獨立結果資料欄，解讀為目的地資料欄系列的值 (等於結果資料欄名稱)，且資料欄限定詞等於空白字串。

為示範如何寫入這些資料類型，請參考以下 SQL 範例，其中 `column` 和 `column2` 是獨立的結果資料欄：

```
SELECT
  x as column1, y as column2
FROM table
```

在這個查詢範例中，`SELECT x as column1` 會在處理 `JSON` 或 `STRUCT` 以外的類型時，將值寫入 Bigtable 的 `column1` 資料欄系列和 `''` (空字串) 資料欄限定詞。

您可以使用 [`bigtable_options`](#bigtable_options) 設定，變更這些類型在匯出作業中的寫入方式，如以下範例所示：

```
EXPORT DATA OPTIONS (
  …
  bigtable_options="""{
   "columnFamilies" : [
      {
        "familyId": "ordered_at",
        "columns": [
           {"qualifierString": "order_time", "fieldName": ""}
        ]
      }
   ]
}"""
) AS
SELECT
  order_id as rowkey,
  STRUCT(product, amount) AS sales_info,
  EXTRACT (MILLISECOND FROM order_timestamp AT TIME ZONE "UTC") AS ordered_at
FROM T
```

在本範例中，BigQuery 資料表 `T` 包含下列資料列：

| `order_id` | `order_timestamp` | `product` | `amount` |
| --- | --- | --- | --- |
| 101 | 2023-03-28T10:40:54Z | 搖桿 | 2 |

如果您將上述 `bigtable_options` 設定與資料表 `T` 搭配使用，系統會將下列資料寫入 Bigtable：

| `rowkey` | `sales_info` (資料欄系列) | | | | `ordered_at` (資料欄系列) |
| --- | --- | --- | --- | --- | --- |
| 101 | 產品 | | amount | | order\_time |
| 1970-01-01T00:00:00Z | 搖桿 | 1970-01-01T00:00:00Z | 2 | 1680000054000 |

`1680000054000` 代表 `2023-03-28T10:40:54Z`，以世界標準時間時區的 Unix 紀元時間起算，單位為毫秒。

## 自動建立新的資料欄系列

如要在 Bigtable 資料表中自動建立新的資料欄系列，請將 `EXPORT DATA` 陳述式中的 [`auto_create_column_families` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw#bigtable_export_option)設為 `true`。這個選項需要 `bigtable.tables.update` 權限，Bigtable 系統管理員 (`roles/bigtable.admin`) 等角色具備這項權限。

```
EXPORT DATA OPTIONS (
uri="https://bigtable.googleapis.com/projects/PROJECT-ID/instances/INSTANCE-ID/appProfiles/APP_PROFILE_ID/tables/TABLE",
format="CLOUD_BIGTABLE",
auto_create_column_families = true
) AS
SELECT
  order_id as rowkey,
  STRUCT(product, amount) AS sales_info
FROM T
```

### 使用 `_CHANGE_TIMESTAMP` 設定資料列中所有儲存格的時間戳記

您可以在匯出結果中新增 `TIMESTAMP` 類型的 `_CHANGE_TIMESTAMP` 資料欄。寫入 Bigtable 的每個儲存格都會使用匯出結果列 `_CHANGE_TIMESTAMP` 的時間戳記值。

Bigtable 不支援早於 Unix 紀元 (1970-01-01T00:00:00Z) 的時間戳記。如果 `_CHANGE_TIMESTAMP` 值為 `NULL`，系統會使用 `0` 的 Unix 紀元時間做為預設時間戳記值。

下列查詢會寫入 `product` 和 `amount` 資料欄的儲存格，並使用資料表 `T` 的 `order_timestamp` 資料欄中指定的時間戳記。

```
EXPORT DATA OPTIONS (...) AS
SELECT
  rowkey,
  STRUCT(product, amount) AS sales_info,
  order_timestamp as _CHANGE_TIMESTAMP
FROM T
```

## 持續匯出

如要持續處理匯出查詢，可以將其設為[持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)。

## 匯出多個具有相同 `rowkey` 值的結果

如果匯出的結果包含多個具有相同 `rowkey` 值的資料列，寫入 Bigtable 的值最終會位於同一個 Bigtable 資料列。

您可以使用這個方法，在同一列中產生多個版本的資料欄值。在這個範例中，BigQuery 中的 `orders` 資料表包含下列資料：

| `id` | `customer` | `order_timestamp` | `amount_spent` |
| --- | --- | --- | --- |
| 100 | Bob | 2023-01-01T10:10:54Z | 10.99 |
| 101 | Alice | 2023-01-02T12:10:50Z | 102.7 |
| 102 | Bob | 2023-01-04T15:17:01Z | 11.1 |

接著，使用者執行下列 `EXPORT DATA` 陳述式：

```
EXPORT DATA OPTIONS (
uri="https://bigtable.googleapis.com/projects/PROJECT-ID/instances/INSTANCE-ID/appProfiles/APP_PROFILE_ID/tables/TABLE",
format="CLOUD_BIGTABLE"
) AS
SELECT customer as rowkey, STRUCT(amount_spent) as orders_column_family, order_timestamp as _CHANGE_TIMESTAMP
FROM orders
```

對 BigQuery `orders` 資料表使用這個陳述式，會將下列資料寫入 Bigtable：

|  | orders\_column\_family | |
| --- | --- | --- |
| 資料列索引鍵 | amount\_spent | |
| Alice | 2023-01-02T12:10:50Z | 102.7 |
| Bob | 2023-01-01T10:10:54Z | 10.99 |
| 2023-01-04T15:17:01Z | 11.1 |

匯出至 Bigtable 時，系統會將新值合併至資料表，而非取代整個資料列。如果 Bigtable 中已有資料列索引鍵的值，則新值可能會部分或完全覆寫先前的值，具體取決於資料欄系列、資料欄名稱和寫入儲存格的時間戳記。

**注意：** 請避免匯出有多個資料列的結果，其中相同資料列索引鍵、資料欄系列、資料欄限定詞和時間戳記的值不同。這類匯出作業的結果不確定，取決於 BigQuery 內部的查詢計畫和排程。BigQuery 無法判斷匯出期間覆寫的值，在匯出前是否已存在於 Bigtable，或先前是否由相同的匯出程序插入。

## 將多個資料欄匯出為通訊協定緩衝區 (Protobuf) 值

[通訊協定緩衝區](https://protobuf.dev/)提供靈活有效率的機制，可將結構化資料序列化。考量到 BigQuery 和 Bigtable 處理不同類型的方式，匯出為 Protobuf 可能會很有幫助。您可以使用 BigQuery user-defined function (UDF)，將資料匯出為 Protobuf 二進位值，並傳送至 Bigtable。詳情請參閱「[將資料匯出為 Protobuf 資料欄](https://docs.cloud.google.com/bigquery/docs/protobuf-export?hl=zh-tw)」。

## 匯出最佳化

如要變更從 BigQuery 匯出記錄至 Bigtable 的處理量，請修改 [Bigtable 目的地叢集](https://docs.cloud.google.com/bigtable/docs/instances-clusters-nodes?hl=zh-tw)中的節點數量。處理量 (每秒寫入的資料列數) 會隨著目的地叢集中的節點數量線性擴充。舉例來說，如果將目的地叢集的節點數量增加一倍，匯出處理量也會增加約一倍。

## 定價

在標準查詢中匯出資料時，系統會依[資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing)計費。在持續查詢中匯出資料時，系統會依據 [BigQuery 運算資源定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)計費。如要執行持續查詢，您必須具備使用 [Enterprise 或 Enterprise Plus 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)，以及使用 `CONTINUOUS` 工作類型的[預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。

資料匯出後，系統會向您收取在 Bigtable 儲存資料的費用。詳情請參閱「[Bigtable 定價](https://cloud.google.com/bigtable/pricing?hl=zh-tw#storage)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-21 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-21 (世界標準時間)。"],[],[]]