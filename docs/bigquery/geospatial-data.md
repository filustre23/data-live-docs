Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用地理空間資料

地理空間分析功能可讓您在 BigQuery 中分析地理資料，地理資料也稱為*地理空間資料*。

使用地理空間資料時的常見物件類型包括以下項目：

* *幾何*代表地球上的表面積，通常使用點、線、多邊形或點、線與多邊形的集合描述。*幾何集合*是一種幾何，代表集合中所有形狀的空間聯集。
* *空間特徵*代表邏輯空間物件，結合幾何圖形與應用程式專用屬性。
* *空間特徵集合*是一組空間特徵。

在 BigQuery 中，[`GEOGRAPHY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#geography_type)
資料類型代表幾何值或幾何集合。如要表示空間特徵，請建立資料表，其中包含幾何體的 `GEOGRAPHY` 資料欄，以及屬性的額外資料欄。表格中的每一列都是空間特徵，整個表格則代表空間特徵集合。

`GEOGRAPHY` 資料類型描述地球表面上的*點集合*。地理資訊點集合是指 [WGS84](https://earth-info.nga.mil/GandG/update/index.php?action=home#tab_wgs84-data) 參考橢球體上的點、線與多邊形集合，含測地線。您可以透過呼叫其中一個 GoogleSQL [地理位置函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)來使用 `GEOGRAPHY` 資料類型。

## 正在載入地理空間資料

地球上的單一點可以只用經緯度配對來描述。
舉例來說，您可以載入含有經緯度值的 CSV 檔案，然後使用 [`ST_GEOGPOINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogpoint) 函式將這些值轉換為 `GEOGRAPHY` 值。

如要載入更複雜的地理區域，請將下列地理空間資料格式載入 `GEOGRAPHY` 欄：

* Well-known text (WKT)
* 熟知的二進位 (WKB)
* GeoJSON
* GeoParquet

### 載入 WKT 或 WKB 資料

[WKT](https://en.wikipedia.org/wiki/Well-known_text) 是一種文字格式，用來描述個別的幾何形狀，通常使用點、線、含選用孔的多邊形，或點、線或多邊形的集合描述。WKB 是 WKT 格式的二進位版本。WKB 可以進行十六進位編碼，適用於不支援二進位資料的格式，例如 JSON。

舉例來說，下列程式碼會定義 WKT 中的點：

```
POINT(-121 41)
```

如要描述空間特徵，WKT 通常會嵌入容器檔案格式 (例如 CSV 檔案) 或資料庫資料表中。檔案資料列或資料表資料列通常會對應於空間特徵。整個檔案或資料表會對應至特徵集合。如要將 WKT 資料載入 BigQuery，請提供[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)，指定地理空間資料的 `GEOGRAPHY` 資料欄。

**注意：** 您無法使用結構定義自動偵測功能，將 WKT 資料載入為 `GEOGRAPHY` 值。如果啟用自動偵測功能，BigQuery 會將資料載入為 `STRING` 值。

舉例來說，您可能有一個 CSV 檔案，內含下列資料：

```
"POLYGON((-124.49 47.35,-124.49 40.73,-116.49 40.73,-116.49 47.35,-124.49 47.35))",poly1
"POLYGON((-85.6 31.66,-85.6 24.29,-78.22 24.29,-78.22 31.66,-85.6 31.66))",poly2
"POINT(1 2)",point1
```

您可以執行 bq 指令列工具 `load` 指令來載入這個檔案：

```
bq load --source_format=CSV \
  --schema="geography:GEOGRAPHY,name:STRING" \
  mydataset.mytable filename1.csv
```

如要進一步瞭解如何在 BigQuery 中載入資料，請參閱「[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」。

如要將 WKT 資料串流至現有的 BigQuery 資料表 (含有 `GEOGRAPHY` 欄)，請在 API 要求中將資料序列化為字串。

### bq

執行 bq 指令列工具 `insert` 指令：

```
echo '{"geo": "LINESTRING (-118.4085 33.9416, -73.7781 40.6413)"}' \
    | bq insert my_dataset.geo_table
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery
import shapely.geometry
import shapely.wkt

bigquery_client = bigquery.Client()

# This example uses a table containing a column named "geo" with the
# GEOGRAPHY data type.
table_id = "my-project.my_dataset.my_table"

# Use the Shapely library to generate WKT of a line from LAX to
# JFK airports. Alternatively, you may define WKT data directly.
my_geography = shapely.geometry.LineString(
    [(-118.4085, 33.9416), (-73.7781, 40.6413)]
)
rows = [
    # Convert data into a WKT string.
    {"geo": shapely.wkt.dumps(my_geography)},
]

#  table already exists and has a column
# named "geo" with data type GEOGRAPHY.
errors = bigquery_client.insert_rows_json(table_id, rows)
if errors:
    raise RuntimeError(f"row insert failed: {errors}")
else:
    print(f"wrote 1 row to {table_id}")
```

如要進一步瞭解 BigQuery 中的串流資料，請參閱[以串流方式將資料傳入 BigQuery](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw) 一文。

您也可以使用 [`ST_GEOGFROMTEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogfromtext) 函式，將 WKT 文字字串轉換為 `GEOGRAPHY` 值。

### 載入 GeoJSON 資料

[GeoJSON](https://geojson.org/) 是以 JSON 為基礎的幾何和空間特徵格式。舉例來說，下列程式碼會定義 GeoJSON 中的點：

```
{ "type": "Point", "coordinates": [-121,41] }
```

GeoJSON 資料可包含下列任一物件類型：

* *幾何圖形物件*：這種空間形狀是由一組點、線及含有自選孔洞的多邊形所組成。
* *地圖項目物件*：包含幾何圖形，以及額外的名稱/值組 (依個別應用程式而不同)。
* *地圖項目集合*：特徵集合是一組特徵物件。

將 GeoJSON 資料載入 BigQuery 的方法有兩種：

* [載入以換行符號分隔的 GeoJSON 檔案](#geojson-files)。
* [載入內嵌於其他檔案類型中的個別 GeoJSON 幾何物件](#geojson-data)。

#### 載入以換行符號分隔的 GeoJSON 檔案

以換行符號分隔的 GeoJSON 檔案包含 GeoJSON 地圖項目物件清單，檔案中的每一行代表一個物件。GeoJSON 地圖項目物件是具有下列成員的 JSON 物件：

* `type`。如果是地圖項目物件，值必須為 `Feature`。BigQuery 會驗證值，但不會將其納入資料表結構定義。
* `geometry`。值為 GeoJSON `Geometry` 物件或 `null`。
  BigQuery 會將這個成員轉換為 `GEOGRAPHY` 值。
* `properties`。值可以是任何 JSON 物件或空值。如果值不是 `null`，BigQuery 會將 JSON 物件的每個成員載入為個別資料表欄。如要進一步瞭解 BigQuery 如何剖析 JSON 資料類型，請參閱[載入 JSON 資料的詳細資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#details_of_loading_json_data)。
* `id`。選用。如有提供，值可以是字串或數字。
  BigQuery 會將這個值載入名為 `id` 的資料欄。

如果特徵物件包含未列於此的其他成員，BigQuery 會直接將這些成員轉換為資料表欄。

您可以使用 bq 指令列工具的 `bq
load` 指令，載入以換行符分隔的 GeoJSON 檔案，如下所示：

```
bq load \
 --source_format=NEWLINE_DELIMITED_JSON \
 --json_extension=GEOJSON \
 --autodetect \
 DATASET.TABLE \
 FILE_PATH_OR_URI
```

更改下列內容：

* `DATASET` 是您的資料集名稱。
* `TABLE` 是目標資料表的名稱。
* `FILE_PATH_OR_URI` 是本機檔案的路徑或 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。

上一個範例會啟用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能。如要進一步控管 BigQuery 如何轉換 `properties` 物件內的值，可以改為提供明確的結構定義。詳情請參閱「[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specify_schemas)」。如果您提供明確的結構定義，請勿在結構定義中加入頂層 `type` 資料欄。針對 `properties` 成員的每個成員，定義個別資料欄，而非單一巢狀資料欄。

如 [RFC 7946](https://tools.ietf.org/html/rfc7946) 所定義，完整的 GeoJSON 資料結構是單一 JSON 物件。許多系統會將 GeoJSON 資料匯出為單一 `FeatureCollection` 物件，其中包含所有幾何圖形。如要將這個格式載入 BigQuery，您必須先轉換檔案，方法是移除根層級的 `FeatureCollection` 物件，並將個別特徵物件分割成不同的行。舉例來說，下列指令會使用 `jq` 指令列工具，將 GeoJSON 檔案分割為以換行符號分隔的格式：

```
cat ~/file1.json | jq -c '.features[]' > converted.json
```

#### 從以換行符號分隔的 GeoJSON 檔案建立外部資料表

您可以建立[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)，查詢儲存在 Cloud Storage 中以換行符號分隔的 GeoJSON 檔案。如要建立外部資料表，請使用 [`CREATE EXTERNAL TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement) DDL 陳述式。在 `OPTIONS` 子句中，將 `format` 選項設為 `NEWLINE_DELIMITED_JSON`，並將 `json_extension` 選項設為 `GEOJSON`。

範例：

```
CREATE EXTERNAL TABLE mydataset.table1 OPTIONS (
  format="NEWLINE_DELIMITED_JSON",
  json_extension = 'GEOJSON',
  uris = ['gs://mybucket/geofile.json']
);
```

#### 載入 GeoJSON 幾何圖形資料

地理空間分析支援載入以文字字串形式內嵌於其他檔案類型中的個別 GeoJSON 幾何物件。舉例來說，您可以載入 CSV 檔案，其中一個資料欄包含 GeoJSON 幾何圖形物件。

如要將這類 GeoJSON 資料載入 BigQuery，請提供[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)，指定 GeoJSON 資料的 `GEOGRAPHY` 資料欄。您必須手動提供結構定義。否則，如果啟用自動偵測功能，BigQuery 會將資料載入為 `STRING` 值。

地理空間分析不支援使用這種方法載入 GeoJSON 特徵物件或特徵集合。如要載入地圖項目物件，請考慮使用以換行符號分隔的 GeoJSON 檔案。

如要將 GeoJSON 資料串流至現有的 BigQuery 資料表 (含有 `GEOGRAPHY` 資料欄)，請在 API 要求中將資料序列化為字串。

### bq

執行 bq 指令列工具 `insert` 指令：

```
echo '{"geo": "{\"type\": \"LineString\", \"coordinates\": [[-118.4085, 33.9416], [-73.7781, 40.6413]]}"}' \
  | bq insert my_dataset.geo_table
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import geojson
from google.cloud import bigquery

bigquery_client = bigquery.Client()

# This example uses a table containing a column named "geo" with the
# GEOGRAPHY data type.
table_id = "my-project.my_dataset.my_table"

# Use the python-geojson library to generate GeoJSON of a line from LAX to
# JFK airports. Alternatively, you may define GeoJSON data directly, but it
# must be converted to a string before loading it into BigQuery.
my_geography = geojson.LineString([(-118.4085, 33.9416), (-73.7781, 40.6413)])
rows = [
    # Convert GeoJSON data into a string.
    {"geo": geojson.dumps(my_geography)}
]

#  table already exists and has a column
# named "geo" with data type GEOGRAPHY.
errors = bigquery_client.insert_rows_json(table_id, rows)
if errors:
    raise RuntimeError(f"row insert failed: {errors}")
else:
    print(f"wrote 1 row to {table_id}")
```

您也可以使用 [`ST_GEOGFROMGEOJSON`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogfromgeojson) 函式，將 GeoJSON 幾何物件轉換為 `GEOGRAPHY` 值。舉例來說，您可以將幾何圖形儲存為 `STRING` 值，然後執行呼叫 `ST_GEOGFROMGEOJSON` 的查詢。

### 載入 GeoParquet 檔案

[GeoParquet](https://geoparquet.org) 規格會在 [Parquet](https://parquet.apache.org/) 檔案格式中新增地理空間類型。GeoParquet 包含中繼資料，可為所含的地理空間資料提供明確語意，避免其他地理空間資料格式發生[解讀問題](#coordinate_systems_and_edges)。

載入 Parquet 檔案時，BigQuery 會檢查 GeoParquet 中繼資料。如果存在 GeoParquet 中繼資料，BigQuery 預設會將中繼資料描述的所有資料欄載入對應的 `GEOGRAPHY` 資料欄。如要進一步瞭解如何載入 Parquet 檔案，請參閱「[載入 Parquet 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw)」。

**注意：** 為避免中斷現有工作流程，部分專案已停用 GeoParquet 支援。如果 GeoParquet 檔案未直接載入 `GEOGRAPHY` 欄，請[與支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

#### 從 GeoParquet 資料建立外部資料表

參照 GeoParquet 檔案的[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw)會將相關資料欄對應至 `GEOGRAPHY` 型別。

GeoParquet 檔案 (`bbox`、`covering`) 中的統計資料不會用於加速外部資料表的查詢。

### 座標系與邊緣

在地理空間分析中，點是指一個 WGS84 球體的表面位置，以經度和大地緯度的方式表示。至於邊緣 (edge) 則是指兩端點之間的球面測地線，(也就是說，邊緣是球體表面上的最短路徑)。

WKT 格式並不提供座標系，載入 WKT 資料時，地理空間分析會假設資料使用 WGS84 座標和球形邊緣。除非地理區域夠小，可忽略球面和平面邊緣之間的差異，否則請確保來源資料符合該座標系統。

GeoJSON 會明確使用 WGS84 座標和平面邊緣。載入 GeoJSON 資料時，地理空間分析會將平面邊緣轉換為球面邊緣。地理空間分析會在必要時為線條加上額外的點，以便讓轉換後的邊緣序列維持在原始線條的 10 公尺範圍之內。這項程序稱為「細分」或「非均勻密集化」。您無法直接控制細分程序。

如要載入具有球形邊緣的地理位置，請使用 WKT。如要載入具有平面邊緣的地理位置 (通常稱為「幾何圖形」)，最簡單的方法就是使用 GeoJSON。不過，如果幾何資料已採用 WKT 格式，您也可以選擇將資料載入為 `STRING` 類型，然後使用 [`ST_GEOGFROMTEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogfromtext_signature2) 函式轉換為 `GEOGRAPHY` 值。將 `planar` 參數設為 `TRUE`，將資料解讀為平面。

GeoParquet 檔案包含用於建立資料的座標系統和邊緣相關中繼資料。讀取具有平面邊緣的 GeoParquet 檔案時，地理空間分析會將平面邊緣轉換為球面邊緣。如果 GeoParquet 檔案的座標系統不是 WGS84，系統會拒絕上傳。

選擇交換格式時，請務必瞭解來源資料使用的座標系統。多數系統會明確支援從 WKT 解析地理資訊 (而非幾何圖形)，或是採用平面邊緣。

您的座標應該先列出經度，再列出緯度。如果地理位置具有任何長線段或邊緣，則它們必須經過曲面細分處理，否則地理空間分析會將其詮釋為球形測地線，因此可能會無法對應至原始資料來源的座標系。

### 多邊形方向

在球體上，每個多邊形都有一個互補的多邊形。舉例來說，描述地球各大洲的多邊形會有一個描述地球海洋的多邊形。由於兩個多邊形都使用相同的界線環形描述，因此需要規則來解決在兩個多邊形中的模糊性 (兩個多邊形中，哪一個由指定的 WKT 字串描述)。

從檔案載入 WKT 和 WKB 字串，或使用串流擷取功能時，地理空間分析會假設輸入中的多邊形方向如下：如果按照輸入頂點的順序沿著多邊形界線前進，多邊形的內部會在左側。地理空間分析功能在將地理位置物件匯出至 WKT 和 WKB 字串時，會使用相同的規則。

如果您使用 [`ST_GEOGFROMTEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogfromtext) 函式將 WKT 字串轉換為 `GEOGRAPHY` 值，`oriented` 參數會指定函式判斷多邊形的方式：

* `FALSE`：將輸入內容解譯為具有較小面積的多邊形。這是預設行為。
* `TRUE`：使用先前說明的左側方向規則。這個選項可讓您載入面積大於半球的多邊形。

由於 GeoJSON 字串是在平面地圖上定義，因此即使輸入內容未遵照 GeoJSON 格式規格 [RFC 7946](https://tools.ietf.org/html/rfc7946) 中定義的方向規則，也可以明確地判定方向。

### 處理格式不正確的空間資料

從其他工具將空間資料載入 BigQuery 時，您可能會因為 WKT 或 GeoJSON 資料無效而發生轉換錯誤。舉例來說，`Edge K has duplicate vertex with edge N` 錯誤表示多邊形具有重複的頂點 (除第一個與最後一個以外)。

為避免格式化問題，您可以建立一個函式讓輸出結果符合標準。舉例來說，從 PostGIS 匯出資料時，您可以使用 PostGIS `ST_MakeValid` 函式來標準化輸出內容。或者，您也可以匯入文字格式的資料，然後呼叫 [`ST_GEOGFROMTEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogfromtext_signature2) 或 [`ST_GEOGFROMGEOJSON`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogfromgeojson) 並搭配 `make_valid` 參數，將資料轉換為所需格式。如果 `make_valid` 為 `TRUE`，這些函式會嘗試修復無效的多邊形。

如要查找或忽略格式不正確的資料，請使用 `SAFE` 前綴函式輸出有問題的資料。例如，下列查詢使用 `SAFE` 前置字元來擷取格式不正確的空間資料。

```
SELECT
  geojson AS bad_geojson
FROM
  mytable
WHERE
  geojson IS NOT NULL
  AND SAFE.ST_GEOGFROMGEOJSON(geojson) IS NULL
```

### 限制

地理空間分析不支援地理空間格式的下列功能：

* 3D 幾何圖形。包括 WKT 格式的「Z」字尾，以及 GeoJSON 格式的高度座標。
* 線性參考系統。包括 WKT 格式的「M」字尾。
* 幾何圖元或多部分幾何圖形以外的 WKT 幾何圖形物件。
  具體來說，地理空間分析僅支援 Point、MultiPoint、LineString、MultiLineString、Polygon、MultiPolygon 和 GeometryCollection。

如要瞭解 GeoJSON 和 WKT 輸入格式的特定限制，請參閱 [`ST_GEOGFROMGEOJSON`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogfromgeojson) 和 [`ST_GEOGFROMTEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogfromtext)。

## 整合地理空間光柵資料與 Google Earth Engine

地理空間洞察資料通常會以格線或*點陣*資料的形式呈現。點陣資料會將區域連續資料 (例如衛星圖像、天氣預報和土地覆蓋物) 整理成像素格線。雖然 BigQuery 主要專門處理表格向量資料，代表具有界線和點的特徵，但您可以使用 [`ST_REGIONSTATS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_regionstats)，將點陣資料整合到 BigQuery 分析中。這項函式會使用 Google 的光柵分析平台 Earth Engine，對光柵資料執行運算和彙整作業，以強化地理空間分析。詳情請參閱「[處理點陣資料](https://docs.cloud.google.com/bigquery/docs/raster-data?hl=zh-tw)」。

如要瞭解如何將 Earth Engine 資料匯出至 BigQuery，請參閱「[匯出至 BigQuery](https://developers.google.com/earth-engine/guides/exporting_to_bigquery?hl=zh-tw)」。如要進一步瞭解 Earth Engine 和 BigQuery 的整合功能，請參閱 Earth Engine 說明文件中的「[BigQuery 整合](https://developers.google.com/earth-engine/guides/bigquery_integrations?hl=zh-tw)」。

## 轉換地理空間資料

如果資料表包含獨立的經度和緯度資料欄，則可以透過 GoogleSQL [地理位置函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw) (例如 [`ST_GEOGPOINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogpoint))，將這些值轉換為地理位置。舉例來說，如果您有兩個 `DOUBLE` 欄位分別存放經度與緯度，則可以使用下列查詢建立一個地理位置欄位：

```
SELECT
  *,
  ST_GEOGPOINT(longitude, latitude) AS g
FROM
  mytable
```

BigQuery 可以將 WKT 和 GeoJSON 字串轉換為地理位置類型。如果資料採用其他格式 (例如 Shapefile)，請使用外部工具將資料轉換為支援的輸入檔案格式，例如 CSV 檔案，並以 WKT 或 GeoJSON 字串編碼 `GEOGRAPHY` 欄。

## 將地理空間資料分區及分群

您可以[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)包含 `GEOGRAPHY` 資料欄的資料表。`GEOGRAPHY` 資料欄可做為分群資料欄使用，但 `GEOGRAPHY` 資料欄無法當成分區資料欄。

將 `GEOGRAPHY` 資料儲存至資料表時，如果您的查詢使用空間述詞篩選資料，請確認資料表是依 `GEOGRAPHY` 欄分群。這通常可提升查詢效能，並可能降低成本。空間述詞會呼叫布林地理位置函式，並且會將 `GEOGRAPHY` 欄做為引數使用。以下範例顯示使用 `ST_DWITHIN` 函式的空間述詞：

```
WHERE ST_DWITHIN(geo, ST_GeogPoint(longitude, latitude), 100)
```

## 將 JOIN 應用於空間資料

空間 JOIN 是指在 `WHERE` 子句中，將兩份具有述詞地理位置函式的資料表予以合併。例如：

```
-- how many stations within 1 mile range of each zip code?
SELECT
    zip_code AS zip,
    ANY_VALUE(zip_code_geom) AS polygon,
    COUNT(*) AS bike_stations
FROM
    `bigquery-public-data.new_york.citibike_stations` AS bike_stations,
    `bigquery-public-data.geo_us_boundaries.zip_codes` AS zip_codes
WHERE ST_DWITHIN(
         zip_codes.zip_code_geom,
         ST_GEOGPOINT(bike_stations.longitude, bike_stations.latitude),
         1609.34)
GROUP BY zip
ORDER BY bike_stations DESC
```

當您的地理位置資料保持不變時，空間合併的效果會更好。上述範例在查詢中建立了地理位置值，但若將地理位置值存入 BigQuery 資料表的話將會有更加的效能表現。

舉例來說，下列查詢會擷取經度與緯度組合，並且將它們轉換成地理資料點。執行這項查詢時，您可以指定新的目的地資料表來儲存查詢結果。

```
SELECT
  *,
  ST_GEOGPOINT(pLongitude, pLatitude) AS p
FROM
  mytable
```

BigQuery 可透過下列 GoogleSQL 述詞函式對 INNER JOIN 和 CROSS JOIN 運算子實作最佳化空間 JOIN：

* [`ST_DWITHIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_dwithin)
* [`ST_INTERSECTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_intersects)
* [`ST_CONTAINS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_contains)
* [`ST_WITHIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_within)
* [`ST_COVERS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_covers)
* [`ST_COVEREDBY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_coveredby)
* [`ST_EQUALS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_equals)
* [`ST_TOUCHES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_touches)

下列項目的空間合併並未進行最佳化：

* 適用於 `LEFT`、`RIGHT` 或 `FULL OUTER` 聯結
* 如果涉及反向聯結
* 當空間述詞為否定時

使用 `ST_DWITHIN` 述詞的 `JOIN` 只會在距離參數為常數運算式時最佳化。

## 匯出空間資料

當您從 BigQuery 匯出空間資料時，`GEOGRAPHY` 欄值將一律格式化成 WKT 字串。如要以 GeoJSON 格式匯出資料，請使用 [`ST_ASGEOJSON`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_asgeojson) 函式。

如果您用來分析匯出資料的工具無法解讀 `GEOGRAPHY` 資料類型，可以使用地理函式 (例如 [`ST_ASTEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_astext) 或 [`ST_ASGEOJSON`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_asgeojson)) 將資料欄值轉換為字串。地理空間分析會在必要時為線條加上額外的資料點，以便讓轉換後的邊緣序列維持在原始測地線的 10 公尺範圍之內。

例如，下列查詢使用 `ST_ASGEOJSON` 將 GeoJSON 值轉換為字串。

```
SELECT
  ST_ASGEOJSON(ST_MAKELINE(ST_GEOGPOINT(1,1), ST_GEOGPOINT(3,2)))
```

結果資料會如下所示：

```
{ "type": "LineString", "coordinates": [ [1, 1], [1.99977145571783, 1.50022838764041], [2.49981908082299, 1.75018082434274], [3, 2] ] }
```

GeoJSON 線條擁有兩個額外的資料點。地理空間分析會新增這些資料點，這樣 GeoJSON 線條會和原始線條一樣貼近地面上的相同路徑。

## 後續步驟

* 如要開始使用地理空間分析，請參閱[資料分析師專用的地理空間分析入門指南](https://docs.cloud.google.com/bigquery/docs/geospatial-get-started?hl=zh-tw)。
* 如要進一步瞭解地理空間分析的視覺化選項，請參閱「[視覺化地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize?hl=zh-tw)」。
* 如要查看地理空間分析的 GoogleSQL 函式說明文件，請參閱[GoogleSQL 中的地理函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]