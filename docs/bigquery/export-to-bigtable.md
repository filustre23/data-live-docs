* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將資料匯出至 Bigtable (反向 ETL)

本文說明如何從 BigQuery 設定反向 ETL (RETL) 至 Bigtable。如要這麼做，請使用 [`EXPORT
DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)，將資料從 BigQuery 資料表匯出至 [Bigtable](https://docs.cloud.google.com/bigtable/docs/overview?hl=zh-tw) 資料表。

您可以透過 RETL 工作流程將資料匯入 Bigtable，結合 BigQuery 的分析功能與 Bigtable 的低延遲和高處理量。這個工作流程可讓您為應用程式使用者提供資料，同時避免耗盡 BigQuery 的配額和限制。

## Bigtable 資料表的特性

[Bigtable 資料表](https://docs.cloud.google.com/bigtable/docs/overview?hl=zh-tw#storage-model)與 BigQuery 資料表有幾項差異：

* Bigtable 和 BigQuery 資料表都是由資料列組成，但 Bigtable 資料列是由資料列索引鍵和資料欄系列組成，其中包含屬於相同資料欄系列的任意數量的資料欄。
* 特定資料表的資料欄系列是在建立資料表時建立，但之後也可以新增或移除。建立資料欄系列時，不必指定屬於該系列的資料欄。
* Bigtable 資料欄不需要預先定義，可用於在[資料表的大小限制內](https://docs.cloud.google.com/bigtable/quotas?hl=zh-tw#limits-data-size)，以名稱 (也稱為「限定詞」) 儲存資料。
* Bigtable 資料欄可包含[資料大小限制內的任何二進位值](https://docs.cloud.google.com/bigtable/quotas?hl=zh-tw#limits-data-size)。
* Bigtable 資料欄一律具有時間維度 (也稱為「版本」)。只要時間戳記不同，同一欄的任何資料列都可以儲存任意數量的資料。
* Bigtable 時間戳記是以微秒為單位，自 [Unix 紀元時間](https://en.wikipedia.org/wiki/Unix_time)起算，例如 0 代表 1970-01-01T00:00:00 UTC。時間戳記必須為非負數的微秒數，且精確度為毫秒 (僅接受 1000 微秒的倍數)。預設的 Bigtable 時間戳記為 0。
* Bigtable 中的資料[可依資料列索引鍵、多個資料列索引鍵、資料列索引鍵範圍或篩選器讀取](https://docs.cloud.google.com/bigtable/docs/reads?hl=zh-tw)。除了完整資料表掃描之外，所有類型的讀取要求都至少須有一個資料列索引鍵或資料列索引鍵範圍。

如要瞭解如何準備 BigQuery 結果以匯出至 Bigtable，請參閱「[準備匯出的查詢結果](#prepare_results)」。

## 事前準備

您必須建立 [Bigtable 執行個體](https://docs.cloud.google.com/bigtable/docs/creating-instance?hl=zh-tw)和 [Bigtable 資料表](https://docs.cloud.google.com/bigtable/docs/managing-tables?hl=zh-tw#create-table)，才能接收匯出的資料。

授予[身分與存取權管理 (IAM) 角色](#required_roles)，讓使用者擁有執行本文中各項工作所需的權限。

### 必要的角色

如要取得將 BigQuery 資料匯出至 Bigtable 所需的權限，請要求系統管理員在專案中授予您下列 IAM 角色：

* 從 BigQuery 資料表匯出資料：
  [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 執行擷取作業：
  [BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user)  (`roles/bigquery.user`)
* 將資料寫入 Bigtable 資料表：
  [Bigtable 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigtable?hl=zh-tw#bigtable.user)  (`roles/bigtable.user`)
* 為 Bigtable 資料表自動建立新的資料欄系列：
  [Bigtable 系統管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigtable?hl=zh-tw#bigtable.admin)  (`roles/bigtable.admin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 限制

* 編碼僅限 `BINARY` 和 `TEXT`。
* 目的地 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)必須設定[單叢集轉送](https://docs.cloud.google.com/bigtable/docs/routing?hl=zh-tw#single-cluster)和[低要求優先等級](https://docs.cloud.google.com/bigtable/docs/request-priorities?hl=zh-tw)。
* Bigtable 應用程式設定檔必須設定為將資料轉送至與 BigQuery 資料集位於同一位置的 Bigtable 叢集。詳情請參閱[位置注意事項](#data-locations)。
* 只有 [BigQuery Enterprise 或 Enterprise Plus 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)支援匯出至 Bigtable。
  不支援 BigQuery Standard 版和[隨選運算](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。
* 只有[`QUERY`指派](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)的預留項目支援匯出至 Bigtable。

## 位置注意事項

* 如果 BigQuery 資料集位於多個地區，則必須設定 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)，將資料傳送至該多地區內的 Bigtable 叢集。舉例來說，如果您的 BigQuery 資料集位於 `US` 多區域，Bigtable 叢集可以位於美國境內的 `us-west1` (奧勒岡) 區域。
* 如果 BigQuery 資料集位於單一地區，則必須設定 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)，將資料傳送至相同地區的 Bigtable 叢集。舉例來說，如果您的 BigQuery 資料集位於 `asia-northeast1` (東京) 地區，Bigtable 叢集也必須位於 `asia-northeast1` (東京) 地區。

詳情請參閱「[Bigtable 位置](https://docs.cloud.google.com/bigtable/docs/locations?hl=zh-tw)」。

## 支援的 BigQuery 類型

寫入 Bigtable 時，系統支援下列資料類型：

| BigQuery 類型 | 寫入的 Bigtable 值 |
| --- | --- |
| `BYTES` | 匯出時不會進行任何變更。 |
| `STRING` | 已轉換為 `BYTES`。 |
| `INTEGER` | 如果 `bigtable_options.column_families.encoding` 設為 `BINARY`，則值會以 8 位元組的大端序格式 (最重要的位元組在前) 寫入。如果 `bigtable_options.column_families.encoding` 設為 `TEXT`，則值會寫入為代表數字的易讀字串。 |
| `FLOAT` | 以 IEEE 754 8 位元組輸出格式寫入值。 |
| `BOOLEAN` | 如果 `bigtable_options.column_families.encoding` 設為 `BINARY`，則值會寫入為 1 位元組值 (`false` = 0x00 或 `true` = 0x01)。如果 `bigtable_options.column_families.encoding` 設為 `TEXT`，值會以文字形式寫入 (`"true"` 或 `"false"`)。 |
| `JSON` | 系統會將匯出的 `JSON` 類型資料欄解讀為屬於特定 Bigtable 資料欄系列的資料欄群組。JSON 物件的成員會解讀為資料欄，其值會寫入 Bigtable。您可以使用 [`bigtable_options`](#bigtable_options) 設定調整要寫入的資料欄名稱。   例如：     ```     JSON '{"FIELD1": "VALUE1", "FIELD2": "VALUE2"}' as MY_COLUMN_FAMILY ```   其中，值 VALUE1 和 VALUE2 會以資料欄 FIELD1 和 FIELD2 的形式寫入 Bigtable，並屬於資料欄系列 MY\_COLUMN\_FAMILY。  **注意：**如果 JSON 文件巢狀內嵌於其他 `JSON` 或 `STRUCT` 類型，系統會以字串形式寫入 Bigtable。匯出巢狀結構中的 `STRUCT` 值時，會受到「[使用 `bigtable_options` 設定匯出項目](#bigtable_options)」一節所述的限制。 |
| `STRUCT` | 系統會將匯出的 `STRUCT` 類型資料欄解讀為屬於特定 Bigtable 資料欄系列的資料欄群組。結構體的成員會解讀為資料欄，以及要寫入 Bigtable 的值。您可以使用 [`bigtable_options`](#bigtable_options) 設定調整要寫入的資料欄名稱。   例如：     ```     STRUCT<FIELD1  STRING, FIELD2 INTEGER> as MY_COLUMN_FAMILY ```   其中，值 FIELD1 和 FIELD2 會以資料欄 FIELD1 和 FIELD2 的形式寫入 Bigtable，並歸入資料欄系列 MY\_COLUMN\_FAMILY。 |

這些支援的資料類型與從 BigQuery 的[外部 Bigtable 資料表](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#bigtablecolumnfamily)讀取資料類似。

## Bigtable 中的 `NULL` 值

Bigtable 中的 `NULL` 值有下列限制：

* Bigtable 沒有 `NULL` 值的類似項目。匯出 Bigtable 中特定資料欄系列和資料欄的值時，系統會刪除 Bigtable 資料列中的現有值。`NULL`
* 如果匯出前，具有特定資料列索引鍵、資料欄系列、資料欄限定詞和時間戳記的 Bigtable 值不存在，匯出的 `NULL` 值就不會影響 Bigtable 資料列。
* 匯出 `NULL` `STRUCT` 或 `JSON` 類型的值時，系統會刪除受影響資料列中，屬於對應資料欄系列的所有資料欄值。您應將 `NULL` 值轉換為 `STRUCT` 或 `JSON` 型別，SQL 引擎才能為該值附加正確型別。下列查詢會從資料欄系列 `column_family1` 中刪除一組指定資料列鍵的所有資料：

  ```
  EXPORT DATA OPTIONS (...) AS
  SELECT
    rowkey,
  CAST(NULL as STRUCT<INT64>) AS column_family1 FROM T
  ```
* 匯出時，系統會略過含有 `NULL` 列鍵的資料列。系統會將略過的資料列數傳回給呼叫端，做為匯出統計資料。

## 使用 `bigtable_options` 設定匯出作業

匯出時，您可以使用 `bigtable_options` 設定，彌合 BigQuery 和 Bigtable 儲存模型之間的差異。設定會以 JSON 字串的形式表示，如下列範例所示：

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
| `columnFamilies` | 資料欄系列描述元陣列。 |
| `columnFamilies.familyId` | Bigtable 資料欄系列的 ID。 |
| `columnFamilies.encoding` | 值可以設為 `BINARY` 或 `TEXT`。如要瞭解類型如何編碼，請參閱「[支援的 BigQuery 類型](#bigquery_types)」。 |
| `columnFamilies.columns` | Bigtable 資料欄對應陣列。 |
| `columnFamilies.columns.qualifierString` | 選填：Bigtable 資料欄限定詞。如果資料欄限定詞沒有非 UTF-8 編碼，請指定這個值。`qualifierString` 和 `qualifierEncoding` 欄位互斥，如果未指定 `qualifierString` 和 `qualifierEncoded`，則會使用 `fieldName` 做為資料欄限定詞。 |
| `columnFamilies.columns.qualifierEncoded` | 選用：Base64 編碼的資料欄限定詞。與 `qualifierString` 類似，如果資料欄限定詞必須使用非 UTF-8 編碼。 |
| `columnFamilies.columns.fieldName` | 必要：BigQuery 結果集欄位名稱。在某些情況下，可以是空字串。如要瞭解如何將空白 `fieldName` 值與簡單型別的欄位搭配使用，請參閱「[準備匯出查詢結果](#prepare_results)」。 |

## 準備匯出查詢結果

如要將查詢結果匯出至 Bigtable，結果必須符合下列條件：

* 結果集必須包含 `rowkey` 欄，且類型為 `STRING` 或 `BYTES`。
* 資料列鍵、資料欄限定符、值和時間戳記不得超過資料表中的 Bigtable [資料大小限制](https://docs.cloud.google.com/bigtable/quotas?hl=zh-tw#limits-data-size)。
* 結果集中必須至少有一個 `rowkey` 以外的資料欄。
* 每個結果集資料欄都必須是[支援的 BigQuery 類型](#bigquery_types)。匯出至 Bigtable 前，請先將所有不支援的資料欄類型轉換為支援的類型。

Bigtable 不要求資料欄限定符必須是有效的 BigQuery 資料欄名稱，且支援使用任何位元組。如要瞭解如何覆寫匯出作業的目標欄位限定符，請參閱「[使用 `bigtable_options` 設定匯出作業](#bigtable_options)」。

如果您將匯出的值用於 Bigtable API (例如 [`ReadModifyWriteRow`](https://docs.cloud.google.com/bigtable/docs/reference/data/rpc/google.bigtable.v2?hl=zh-tw#google.bigtable.v2.Bigtable.ReadModifyWriteRow))，任何數值都必須使用正確的[二進位編碼](#bigtable_options)。

根據預設，系統會將 `STRUCT` 或 `JSON` 以外類型的獨立結果資料欄，解讀為目的地資料欄系列的值 (等於結果資料欄名稱)，以及等於空白字串的資料欄限定詞。

如要示範如何編寫這些資料類型，請參考下列 SQL 範例，其中 `column` 和 `column2` 是獨立的結果欄：

```
SELECT
  x as column1, y as column2
FROM table
```

在這個查詢範例中，處理 `JSON` 或 `STRUCT` 以外的型別時，`SELECT x as column1` 會將值寫入 Bigtable 的 `column1` 資料欄系列和 `''` (空字串) 資料欄限定詞。

您可以使用 [`bigtable_options`](#bigtable_options) 設定，變更這些型別在匯出時的寫入方式，如下例所示：

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

如果您使用上述 `bigtable_options` 設定和資料表 `T`，下列資料會寫入 Bigtable：

| `rowkey` | `sales_info` (資料欄系列) | | | | `ordered_at` (資料欄系列) |
| --- | --- | --- | --- | --- | --- |
| 101 | 產品 | | amount | | order\_time |
| 1970-01-01T00:00:00Z | 搖桿 | 1970-01-01T00:00:00Z | 2 | 1680000054000 |

`1680000054000` 代表 `2023-03-28T10:40:54Z`，以世界標準時間時區的 Unix Epoch 紀元時間為準，單位為毫秒。

## 自動建立新的資料欄系列

如要在 Bigtable 資料表中自動建立新的資料欄系列，請在 `EXPORT DATA` 陳述式中將 [`auto_create_column_families` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw#bigtable_export_option)設為 `true`。如要使用這個選項，您必須具備 `bigtable.tables.update` 權限，例如 Bigtable 系統管理員 (`roles/bigtable.admin`) 等角色都具備這項權限。

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

### 使用 `_CHANGE_TIMESTAMP` 為資料列中的所有儲存格設定時間戳記

您可以將 `TIMESTAMP` 類型的 `_CHANGE_TIMESTAMP` 資料欄新增至結果，然後匯出。
寫入 Bigtable 的每個儲存格都會使用匯出結果列的 `_CHANGE_TIMESTAMP` 時間戳記值。

Bigtable 不支援早於 Unix 紀元 (1970-01-01T00:00:00Z) 的時間戳記。如果 `_CHANGE_TIMESTAMP` 值為 `NULL`，系統會使用 `0` 的 Unix Epoch 時間做為預設時間戳記值。

下列查詢會使用資料表 `T` 的 `order_timestamp` 資料欄中指定的時間戳記，為 `product` 和 `amount` 資料欄寫入儲存格。

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

## 匯出具有相同 `rowkey` 值的多個結果

匯出結果時，如果有多個資料列具有相同的 `rowkey` 值，寫入 Bigtable 的值會位於同一個 Bigtable 資料列。

您可以使用這個方法，在同一列中產生多個版本的資料欄值。在本範例中，BigQuery 中的 `orders` 資料表包含下列資料：

| `id` | `customer` | `order_timestamp` | `amount_spent` |
| --- | --- | --- | --- |
| 100 | Bob | 2023-01-01T10:10:54Z | 10.99 |
| 101 | Alice | 2023-01-02T12:10:50Z | 102.7 |
| 102 | Bob | 2023-01-04T15:17:01Z | 11.1 |

使用者接著執行下列 `EXPORT DATA` 陳述式：

```
EXPORT DATA OPTIONS (
uri="https://bigtable.googleapis.com/projects/PROJECT-ID/instances/INSTANCE-ID/appProfiles/APP_PROFILE_ID/tables/TABLE",
format="CLOUD_BIGTABLE"
) AS
SELECT customer as rowkey, STRUCT(amount_spent) as orders_column_family, order_timestamp as _CHANGE_TIMESTAMP
FROM orders
```

在 BigQuery `orders` 資料表中使用這項陳述式，會導致下列資料寫入 Bigtable：

|  | orders\_column\_family | |
| --- | --- | --- |
| 資料列索引鍵 | amount\_spent | |
| Alice | 2023-01-02T12:10:50Z | 102.7 |
| Bob | 2023-01-01T10:10:54Z | 10.99 |
| 2023-01-04T15:17:01Z | 11.1 |

匯出至 Bigtable 時，系統會將新值併入資料表，而非取代整列。如果資料列索引鍵在 Bigtable 中已有值，則新值會部分或完全覆寫先前的資料，具體情況取決於要寫入的儲存格的資料欄系列、資料欄名稱和時間戳記。

**注意：** 請避免匯出結果，因為這些結果有多個資料列，且相同資料列索引鍵、資料欄系列、資料欄限定詞和時間戳記的值不同。這類匯出作業的結果不具決定性，取決於 BigQuery 內的查詢計畫和排程。BigQuery 無法判斷匯出期間覆寫的值，是匯出前就存在於 Bigtable 中，還是先前由同一匯出程序插入。

## 將多個資料欄匯出為通訊協定緩衝區 (Protobuf) 值

[通訊協定緩衝區](https://protobuf.dev/)提供彈性且有效率的機制，可將結構化資料序列化。考量到 BigQuery 和 Bigtable 處理不同類型的方式，匯出為 Protobuf 可能會很有幫助。您可以使用 BigQuery 使用者定義函式 (UDF)，將資料匯出為 Protobuf 二進位值至 Bigtable。詳情請參閱「[以 Protobuf 欄匯出資料](https://docs.cloud.google.com/bigquery/docs/protobuf-export?hl=zh-tw)」。

## 匯出最佳化

如要變更從 BigQuery 匯出記錄至 Bigtable 的處理量，請修改 [Bigtable 目的地叢集](https://docs.cloud.google.com/bigtable/docs/instances-clusters-nodes?hl=zh-tw)中的節點數量。處理量 (每秒寫入的列數) 會隨著目的地叢集中的節點數線性調整。
舉例來說，如果將目的端叢集中的節點數量增加一倍，匯出輸送量大約也會增加一倍。

## 定價

匯出標準查詢中的資料時，系統會按照[資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing)計費。
匯出持續查詢中的資料時，系統會按照 [BigQuery 容量運算價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)計費。如要執行連續查詢，您必須擁有使用 [Enterprise 或 Enterprise Plus 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的[預留位置](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)，以及使用 `CONTINUOUS` 工作類型的[預留位置指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。

匯出資料之後，系統會因您在 Bigtable 中儲存資料而向您收取費用。詳情請參閱 [Bigtable 定價](https://cloud.google.com/bigtable/pricing?hl=zh-tw#storage)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]