Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Cloud Storage 載入 CSV 資料

從 Cloud Storage 載入 CSV 資料時，可將資料載入至新的資料表或分區、將資料附加到現有資料表或分區或覆寫現有資料表或分區。將資料載入 BigQuery 時，資料會轉換為 [Capacitor](https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw) 資料欄格式 (BigQuery 的儲存格式)。

如需從本機檔案載入 CSV 資料的相關資訊，請參閱[將資料從本機資料來源載入至 BigQuery](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#loading_data_from_local_files)。

## 歡迎試用

如果您未曾使用過 Google Cloud，歡迎建立帳戶，親自體驗實際使用 BigQuery 的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。

[免費試用 BigQuery](https://console.cloud.google.com/freetrial?hl=zh-tw)

## 限制

從 Cloud Storage bucket 將資料載入 BigQuery 時，須遵守下列限制：

* BigQuery 不保證外部資料來源的資料一致性。如果基礎資料在查詢執行期間遭到變更，可能會導致非預期的行為。
* BigQuery 不支援 [Cloud Storage 物件版本管理](https://docs.cloud.google.com/storage/docs/object-versioning?hl=zh-tw)。如果您在 Cloud Storage URI 中加入世代編號，載入工作就會失敗。

將 CSV 檔案載入 BigQuery 時，請注意下列事項：

* CSV 檔案不支援巢狀或重複資料。
* 移除位元組順序標示 (BOM) 字元。否則可能會發生未預期的問題。
* 如果使用 gzip 壓縮，BigQuery 就無法平行讀取資料。將壓縮的 CSV 資料載入 BigQuery 的速度，比載入未壓縮資料慢。請參閱「[載入壓縮和未壓縮的資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#loading_compressed_and_uncompressed_data)」。
* 您無法在同一個載入工作中同時包含壓縮和未壓縮的檔案。
* gzip 檔案的大小上限為 4 GB。
* 如果所有資料欄都是字串類型，[使用結構定義自動偵測功能](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)載入 CSV 資料時，不會自動偵測標頭。在這種情況下，請在輸入內容中新增數值欄，或明確宣告結構定義。
* 載入 CSV 或 JSON 資料時，`DATE` 資料欄中的值必須使用連字號 (`-`) 分隔符，且必須採用下列日期格式：`YYYY-MM-DD` (年-月-日)。
* 載入 JSON 或 CSV 資料時，`TIMESTAMP` 欄中的值必須使用破折號 (`-`) 或斜線 (`/`) 分隔符號來分隔時間戳記的日期部分，且日期必須採用下列其中一種格式：`YYYY-MM-DD` (年-月-日) 或 `YYYY/MM/DD` (年/月/日)。時間戳記的 `hh:mm:ss` (時-分-秒) 部分必須使用半形冒號 (`:`) 分隔符。
* 檔案必須符合[載入工作限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)中說明的 CSV 檔案大小限制。

## 事前準備

授予 Identity and Access Management (IAM) 角色，讓使用者具備必要權限，可執行本文件中的各項工作，並建立資料集來儲存資料。

### 所需權限

如要將資料載入 BigQuery，您必須具備 IAM 權限，才能執行載入工作，並將資料載入 BigQuery 資料表和分區。如果您是從 Cloud Storage 載入資料，也需要 IAM 權限，才能存取含有資料的 bucket。

#### 將資料載入 BigQuery 的權限

如要將資料載入新的 BigQuery 資料表或分區，或附加或覆寫現有資料表或分區，您必須具備下列 IAM 權限：

* `bigquery.tables.create`
* `bigquery.tables.updateData`
* `bigquery.tables.update`
* `bigquery.jobs.create`

下列各項預先定義的 IAM 角色，都包含將資料載入 BigQuery 資料表或分區所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin` (包含 `bigquery.jobs.create` 權限)
* `bigquery.user` (包含 `bigquery.jobs.create` 權限)
* `bigquery.jobUser` (包含 `bigquery.jobs.create` 權限)

此外，如果您具備 `bigquery.datasets.create` 權限，則可在建立的資料集中，使用載入工作建立及更新資料表。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)」。

### 從 Cloud Storage 載入資料的權限

如要取得從 Cloud Storage bucket 載入資料所需的權限，請要求管理員授予您 bucket 的[儲存空間管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin)  (`roles/storage.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備從 Cloud Storage bucket 載入資料所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能從 Cloud Storage bucket 載入資料：

* `storage.buckets.get`
* `storage.objects.get`
* `storage.objects.list (required if you are using a URI wildcard)`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 建立資料集

建立 [BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存資料。

## CSV 壓縮

您可以使用 `gzip` 公用程式壓縮 CSV 檔案。請注意，`gzip` 會執行完整的檔案壓縮，這與其他檔案格式 (例如 Avro) 的壓縮轉碼器執行的檔案內容壓縮不同。使用 `gzip` 壓縮 CSV 檔案可能會影響效能。如要進一步瞭解相關取捨，請參閱「[載入壓縮和未壓縮的資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#loading_compressed_and_uncompressed_data)」。

## 將 CSV 資料載入資料表

如要將 Cloud Storage 中的 CSV 資料載入新的 BigQuery 資料表，請選取下列其中一個選項：

### 控制台

---

如要直接在 Cloud Shell 編輯器中按照逐步指南操作，請按一下「Guide me」(逐步引導)：

[逐步引導](https://console.cloud.google.com/?tutorial=bigquery_import_data_from_cloud_storage&hl=zh-tw)

---

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，點選「資料集」，然後選取資料集。
4. 在「資料集資訊」部分，點選 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「Source」(來源) 部分，從「Create table from」(建立資料表來源) 清單中選取「Google Cloud Storage」。接著，按照下列步驟操作：
   1. 從 Cloud Storage bucket 選取檔案，或輸入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。您無法在 Google Cloud 控制台中加入多個 URI，但可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage bucket 必須與資料集位於相同位置，且該資料集包含您要建立、附加或覆寫的資料表。
   2. 「檔案格式」請選取「CSV」。
2. 在「Destination」(目的地) 部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要在其中建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位設為「原生資料表」。
3. 在「Schema」(結構定義) 部分，輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。如要啟用結構定義[自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，請選取「自動偵測」。
   您可以透過下列任一方法手動輸入結構定義資訊：
   * 方法 1：按一下「Edit as text」(以文字形式編輯)，然後以 JSON 陣列的形式貼上結構定義。使用 JSON 陣列時，您會按照[建立 JSON 結構定義檔案](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的相同程序產生結構定義。輸入下列指令，即可查看現有資料表的 JSON 格式結構定義：

     ```
         bq show --format=prettyjson dataset.table
     ```
   * 方法 2：按一下「Add field」(新增欄位)add\_box，然後輸入資料表結構定義。指定每個欄位的「Name」(名稱)、「Type」(類型) 和「Mode」(模式)。
4. 選用：指定**分區和叢集設定**。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。
5. 按一下「進階選項」，然後執行下列操作：
   * 讓「Write preference」(寫入偏好設定) 的 [Write if empty] (空白時寫入) 選項維持在已選取狀態。這個選項會建立新資料表，並將資料載入其中。
   * 在「Number of errors allowed」(允許的錯誤數量) 部分，接受預設值 `0`，或輸入可忽略的含錯誤列數上限。如果含錯誤的列數超過這個值，工作就會顯示 `invalid` 訊息並停止執行。這個選項僅適用於 CSV 和 JSON 檔案。
   * 在「Time zone」(時區) 部分，輸入預設時區。如果剖析的時間戳記值未指定時區，就會採用這個預設時區。如要查看更多有效的時區名稱，請按[這裡](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_zone_name)。如果沒有這個值，系統會使用預設時區 (世界標準時間) 剖析沒有特定時區的時間戳記值。
   * 在「Date Format」(日期格式) 中，輸入[格式元素](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/format-elements?hl=zh-tw#format_string_as_datetime)，定義輸入檔案中的 DATE 值格式。這個欄位應採用 SQL 樣式，例如 `MM/DD/YYYY`。如果這個值存在，則這個格式是唯一相容的 DATE 格式。[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw#date_and_time_values)也會根據這個格式 (而非現有格式) 決定 DATE 資料欄類型。如果沒有這個值，系統會使用[預設格式](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#data_types)剖析 DATE 欄位。
   * 在「Datetime Format」(日期時間格式) 中，輸入[格式元素](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/format-elements?hl=zh-tw#format_string_as_datetime)，定義輸入檔案中的 DATETIME 值格式。這個欄位應採用 SQL 樣式，例如 `MM/DD/YYYY HH24:MI:SS.FF3`。如果這個值存在，則這個格式是唯一相容的 DATETIME 格式。[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw#date_and_time_values)也會根據這個格式 (而非現有格式) 決定 DATETIME 資料欄類型。如果沒有這個值，系統會使用[預設格式](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#data_types)剖析 DATETIME 欄位。
   * 在「Time Format」(時間格式) 中，輸入[格式元素](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/format-elements?hl=zh-tw#format_string_as_datetime)，定義輸入檔案中的 TIME 值格式。這個欄位應採用 SQL 樣式，例如 `HH24:MI:SS.FF3`。如果這個值存在，這個格式就是唯一相容的時間格式。[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw#date_and_time_values)也會根據這個格式 (而非現有格式) 決定 TIME 資料欄類型。如果沒有這個值，系統會使用[預設格式](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#data_types)剖析 TIME 欄位。
   * 在「Timestamp Format」(時間戳記格式) 中，輸入[格式元素](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/format-elements?hl=zh-tw#format_string_as_datetime)，定義輸入檔案中的 TIMESTAMP 值格式。這個欄位應採用 SQL 樣式，例如 `MM/DD/YYYY HH24:MI:SS.FF3`。如果提供這個值，則只有這個格式與 TIMESTAMP 相容。[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw#date_and_time_values)也會根據這個格式 (而非現有格式) 決定 TIMESTAMP 資料欄類型。如果沒有這個值，系統會使用[預設格式](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#data_types)剖析 TIMESTAMP 欄位。
   * 如要忽略資料列中未出現在資料表結構定義的值，請選取「Unknown values」(不明的值)。
   * 在「欄位分隔符號」部分，選擇用於分隔 CSV 檔案中儲存格的字元：「逗號」、「定位點」、「直線符號」或「自訂」。如果選擇「自訂」，請在「自訂欄位分隔符號」方塊中輸入分隔符號。預設值為 [Comma] (半形逗號)。
   * 在「Source column match」(來源資料欄比對) 部分，選擇下列其中一項策略，用於比對載入的資料欄與結構定義。
   + `Default`：系統會根據結構定義的提供方式，選擇預設行為。
     如果啟用自動偵測功能，預設行為是依名稱比對資料欄。
     否則，系統預設會依位置比對資料欄。這樣做是為了讓行為回溯相容。
   + `Position`：假設資料欄的排序方式與結構定義相同，則依位置比對資料欄。
   + `Name`：將標題列視為資料欄名稱，並重新排序資料欄，使其與結構定義中的欄位名稱相符，藉此依名稱進行比對。系統會根據「Header rows to skip」(要略過的標題列)，從最後一個略過的資料列讀取資料欄名稱。* 在「Header rows to skip」(要略過的標題列數) 部分，輸入要從 CSV 檔案開頭略過的標題列數。預設值為 `0`。
   * 在「Quoted newlines」(引用換行符號) 部分，勾選「Allow quoted newlines」(允許引用換行符號)，允許 CSV 檔案中含有換行符號的引用資料區段。預設值為 `false`。
   * 在「Jagged rows」(鋸齒狀資料列) 部分，勾選「Allow jagged rows」(允許鋸齒狀資料列)，接受 CSV 檔案中缺少結尾選用資料欄的資料列。缺少的值會視為空值。如未勾選，缺少結尾資料欄的記錄會視為損壞記錄，如果損壞記錄過多，工作結果會傳回無效錯誤。預設值為 `false`。
   * 在「Null markers」(空值標記) 輸入自訂字串清單，代表 CSV 資料中的空值。
   * 在「Encryption」(加密) 部分，按一下「Customer-managed key」(客戶自行管理的金鑰)，即可使用 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
6. 點選「建立資料表」。

**注意：** 使用Google Cloud 控制台將資料載入空白資料表時，您無法新增標籤、說明、資料表到期時間或分區到期時間。  
  
資料表建立後，您可以更新資料表的到期時間、說明和標籤，但無法在使用 Google Cloud 控制台建立資料表後新增分區到期時間。詳情請參閱「[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)」。

### SQL

使用 [`LOAD DATA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)。以下範例會將 CSV 檔案載入新資料表 `mytable`：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   LOAD DATA OVERWRITE mydataset.mytable
   (x INT64,y STRING)
   FROM FILES (
     format = 'CSV',
     uris = ['gs://bucket/path/file.csv']);
   ```
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

請使用 `bq load` 指令，然後使用 `--source_format` 旗標指定 `CSV`，並加入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。您可以加入單一 URI、以逗號分隔的 URI 清單，或包含[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)的 URI。您可以在結構定義定義檔案中內嵌提供結構定義，或使用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能。如未指定結構定義，且 `--autodetect` 為 `false`，且目的地資料表存在，則會使用目的地資料表的結構定義。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

其他選用標記包括：

* `--allow_jagged_rows`：如果有指定，系統會接受在 CSV 檔案中缺少結尾自選欄的資料列。系統會將缺少的值視為空值。如果取消勾選，系統會將缺少結尾資料欄的記錄視為損壞記錄；如果損壞記錄過多，工作結果中就會出現無效錯誤。預設值為 `false`。
* `--allow_quoted_newlines`：如果有指定，系統會允許在 CSV 檔案中使用包含換行符號字元的引用資料區段。預設值為 `false`。
* `--field_delimiter`：用來表示資料中資料欄間界線的字元，`\t` 和 `tab` 都可用來表示 Tab 字元分隔。預設值為 `,`。
* `--null_marker`：選用的自訂字串，代表 CSV 資料中的 NULL 值。
* `--null_markers`：選用逗號分隔的清單，代表 CSV 資料中的空值。這個選項無法與 `--null_marker` 旗標搭配使用。
* `--source_column_match`：指定策略，以便比對載入的資料欄與結構定義。您可以指定 `POSITION`，依位置比對載入的資料欄，前提是資料欄的排序方式與結構定義相同。您也可以指定 `NAME`，將標頭列視為資料欄名稱，並重新排序資料欄，使其與結構定義中的欄位名稱相符，藉此依名稱比對。如未指定這個值，則預設值會依據結構定義的提供方式而定。如果啟用 `--autodetect`，預設行為是依名稱比對資料欄。否則，預設會依位置比對資料欄。
* `--skip_leading_rows`：指定在 CSV 檔案頂端要略過的標題列數。預設值為 `0`。
* `--quote`：用來括住記錄的引號字元。預設值為 `"`。如要表示沒有引號字元，請使用空白字串。
* `--max_bad_records`：這是一個整數，用來指定整個工作失敗前可允許的錯誤記錄數量上限。預設值為 `0`。無論 `--max_bad_records` 的值為何，系統最多只會傳回五個任何類型的錯誤。
* `--ignore_unknown_values`：如果指定，CSV 或 JSON 資料中就可以含有其他無法辨識的值 (但系統會予以忽略)。
* `--time_zone`：選用的預設時區，如果剖析的時間戳記值在 CSV 或 JSON 資料中未指定時區，就會採用這個時區。
* `--date_format`：選用的自訂字串，定義 CSV 或 JSON 資料中 DATE 值的格式。
* `--datetime_format`：選用的自訂字串，定義 CSV 或 JSON 資料中的 DATETIME 值格式。
* `--time_format`：選用的自訂字串，定義 CSV 或 JSON 資料中 TIME 值的格式。
* `--timestamp_format`：選用的自訂字串，定義 CSV 或 JSON 資料中的 TIMESTAMP 值格式。
* `--autodetect`：如果指定，系統就會針對 CSV 和 JSON 資料啟用結構定義自動偵測功能。
* `--time_partitioning_type`：針對資料表啟用時間分區並設定分區類型。可能的值為 `HOUR`、`DAY`、`MONTH` 和 `YEAR`。建立依 `DATE`、`DATETIME` 或 `TIMESTAMP` 資料欄分區的資料表時，可以選擇是否使用這個旗標。時間分區的預設分區類型為 `DAY`。您無法變更現有資料表的分區規格。
* `--time_partitioning_expiration`：這是一個整數，用來指定系統應在何時刪除時間分區 (以秒為單位)。到期時間為分區的世界標準時間日期加上整數值。
* `--time_partitioning_field`：用於建立分區資料表的 `DATE` 或 `TIMESTAMP` 欄。如果啟用時間分區，但未提供這個值，系統會建立擷取時間分區資料表。
* `--require_partition_filter`：這個選項啟用後，系統會要求使用者加入 `WHERE` 子句，以指定要查詢的分區。使用分區篩選器可以降低成本並提升效能。詳情請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)一文。
* `--clustering_fields`：以半形逗號分隔的清單，最多列出四個用於建立[分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)的資料欄名稱。
* `--destination_kms_key`：用於加密資料表資料的 Cloud KMS 金鑰。
* `--column_name_character_map`：定義資料欄名稱字元的範圍和處理方式，並可選擇啟用[彈性資料欄名稱](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#flexible-column-names)。CSV 檔案需要 `--autodetect` 選項。詳情請參閱「[`load_option_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_option_list)」。

  如要進一步瞭解 `bq load` 指令，請參閱：

  + [指令列參考資料](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load)

  如要進一步瞭解分區資料表，請參閱：

  + [建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)

  如要進一步瞭解分群資料表，請參閱：

  + [建立及使用分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)

  如要進一步瞭解資料表加密作業，請參閱下列說明文章：

  + [使用 Cloud KMS 金鑰保護資料](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)

如要將 CSV 資料載入 BigQuery，請輸入下列指令：

```
bq --location=location load \
--source_format=format \
dataset.table \
path_to_source \
schema
```

其中：

* location 是您的位置。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)來設定位置的預設值。
* format為 `CSV`。
* dataset 是現有資料集。
* table 是您正在載入資料的資料表名稱。
* path\_to\_source 是完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或以半形逗號分隔的 URI 清單。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。
* schema 是有效的結構定義。結構定義可以是本機 JSON 檔案，或以內嵌的方式在指令中輸入。您也可以改用 `--autodetect` 旗標，而非提供結構定義。

範例：

下列指令會將 `gs://mybucket/mydata.csv` 中的資料載入 `mydataset` 中名為 `mytable` 的資料表。結構定義是在名為 `myschema.json` 的本機結構定義檔中定義。

```
    bq load \
    --source_format=CSV \
    mydataset.mytable \
    gs://mybucket/mydata.csv \
    ./myschema.json
```

下列指令會將 `gs://mybucket/mydata.csv` 中的資料載入 `mydataset` 中名為 `mytable` 的資料表。結構定義是在名為 `myschema.json` 的本機結構定義檔中定義。CSV 檔案中包含兩個標頭列。如果未指定 `--skip_leading_rows`，則預設行為會假設檔案中不含標頭。

```
    bq load \
    --source_format=CSV \
    --skip_leading_rows=2
    mydataset.mytable \
    gs://mybucket/mydata.csv \
    ./myschema.json
```

下列指令會將 `gs://mybucket/mydata.csv` 中的資料載入 `mydataset` 中名為 `mytable` 的擷取時間分區資料表。結構定義是在名為 `myschema.json` 的本機結構定義檔中定義。

```
    bq load \
    --source_format=CSV \
    --time_partitioning_type=DAY \
    mydataset.mytable \
    gs://mybucket/mydata.csv \
    ./myschema.json
```

下列指令會將 `gs://mybucket/mydata.csv` 中的資料載入 `mydataset` 中名為 `mytable` 的新分區資料表。資料表會依 `mytimestamp` 資料欄進行分區。結構定義是在名為 `myschema.json` 的本機結構定義檔中定義。

```
    bq load \
    --source_format=CSV \
    --time_partitioning_field mytimestamp \
    mydataset.mytable \
    gs://mybucket/mydata.csv \
    ./myschema.json
```

下列指令會將 `gs://mybucket/mydata.csv` 中的資料載入 `mydataset` 中名為 `mytable` 的資料表。結構定義由系統自動偵測。

```
    bq load \
    --autodetect \
    --source_format=CSV \
    mydataset.mytable \
    gs://mybucket/mydata.csv
```

下列指令會將 `gs://mybucket/mydata.csv` 中的資料載入 `mydataset` 中名為 `mytable` 的資料表。結構定義是以內嵌的方式定義，格式為 `field:data_type,field:data_type`。

```
    bq load \
    --source_format=CSV \
    mydataset.mytable \
    gs://mybucket/mydata.csv \
    qtr:STRING,sales:FLOAT,year:STRING
```

**注意：** 使用 bq 指令列工具指定結構定義時，您無法加入 `RECORD` ([`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)) 類型、欄位說明，也無法指定欄位模式。所有欄位模式預設為 `NULLABLE`。如要加入欄位說明、模式和 `RECORD` 類型，請改為提供 [JSON 結構定義檔案](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)。

下列指令會將 `gs://mybucket/` 中多個檔案的資料載入 `mydataset` 中名為 `mytable` 的資料表。Cloud Storage URI 使用萬用字元。結構定義由系統自動偵測。

```
    bq load \
    --autodetect \
    --source_format=CSV \
    mydataset.mytable \
    gs://mybucket/mydata*.csv
```

下列指令會將 `gs://mybucket/` 中多個檔案的資料載入到 `mydataset` 中名為 `mytable` 的資料表。指令包含以半形逗號分隔的 Cloud Storage URI 清單，其中含有萬用字元。結構定義是在名為 `myschema.json` 的本機結構定義檔中定義。

```
    bq load \
    --source_format=CSV \
    mydataset.mytable \
    "gs://mybucket/00/*.csv","gs://mybucket/01/*.csv" \
    ./myschema.json
```

### API

1. 建立指向 Cloud Storage 中來源資料的 `load` 工作。
2. (選擇性操作) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。
3. `source URIs` 屬性必須是完整的，且必須符合下列格式：`gs://bucket/object`。每個 URI 可包含一個「\*」[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。
4. 藉由將 `sourceFormat` 屬性設為 `CSV`，以指定 CSV 資料格式。
5. 如要檢查工作狀態，請呼叫 [`jobs.get(job_id*)`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/get?hl=zh-tw)，其中 job\_id 是初始要求傳回的工作 ID。

   * 如果是 `status.state = DONE`，代表工作已順利完成。
   * 如果出現 `status.errorResult` 屬性，代表要求執行失敗，且該物件會包含描述問題的相關資訊。如果要求執行失敗，系統就不會建立任何資料表，也不會載入任何資料。
   * 如果沒有 `status.errorResult`，代表工作已順利完成，但可能發生一些非致命錯誤，例如匯入幾列資料時發生問題。非嚴重錯誤會列在傳回的工作物件 `status.errors` 屬性中。

**API 附註：**

* 載入工作不可部分完成，且資料狀態具一致性。如果載入工作失敗，所有資料都無法使用；如果載入工作成功，則所有資料都可以使用。
* 最佳做法是產生專屬 ID，並在呼叫 `jobs.insert` 建立載入工作時，將該 ID 做為 `jobReference.jobId` 傳遞。這個方法較不受網路故障問題的影響，因為用戶端可使用已知的工作 ID 進行輪詢或重試。
* 對指定的工作 ID 呼叫 `jobs.insert` 是一種冪等作業。也就是說，您可以對同一個工作 ID 重試無數次，最多會有一個作業成功。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定操作說明進行操作。詳情請參閱 [BigQuery C# API 參考文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryLoadTableGcsCsv
{
    public void LoadTableGcsCsv(
        string projectId = "your-project-id",
        string datasetId = "your_dataset_id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        var gcsURI = "gs://cloud-samples-data/bigquery/us-states/us-states.csv";
        var dataset = client.GetDataset(datasetId);
        var schema = new TableSchemaBuilder {
            { "name", BigQueryDbType.String },
            { "post_abbr", BigQueryDbType.String }
        }.Build();
        var destinationTableRef = dataset.GetTableReference(
            tableId: "us_states");
        // Create job configuration
        var jobOptions = new CreateLoadJobOptions()
        {
            // The source format defaults to CSV; line below is optional.
            SourceFormat = FileFormat.Csv,
            SkipLeadingRows = 1
        };
        // Create and run job
        var loadJob = client.CreateLoadJob(
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

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// importCSVExplicitSchema demonstrates loading CSV data from Cloud Storage into a BigQuery
// table and providing an explicit schema for the data.
func importCSVExplicitSchema(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states.csv")
	gcsRef.SkipLeadingRows = 1
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

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.CsvOptions;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.TableId;

// Sample to load CSV data from Cloud Storage into a new BigQuery table
public class LoadCsvFromGcs {

  public static void runLoadCsvFromGcs() throws Exception {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv";
    Schema schema =
        Schema.of(
            Field.of("name", StandardSQLTypeName.STRING),
            Field.of("post_abbr", StandardSQLTypeName.STRING));
    loadCsvFromGcs(datasetName, tableName, sourceUri, schema);
  }

  public static void loadCsvFromGcs(
      String datasetName, String tableName, String sourceUri, Schema schema) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Skip header row in the file.
      CsvOptions csvOptions = CsvOptions.newBuilder().setSkipLeadingRows(1).build();

      TableId tableId = TableId.of(datasetName, tableName);
      LoadJobConfiguration loadConfig =
          LoadJobConfiguration.newBuilder(tableId, sourceUri, csvOptions).setSchema(schema).build();

      // Load data from a GCS CSV file into the table
      Job job = bigquery.create(JobInfo.of(loadConfig));
      // Blocks until this load table job completes its execution, either failing or succeeding.
      job = job.waitFor();
      if (job.isDone()) {
        System.out.println("CSV from GCS successfully added during load append job");
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

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client libraries
const {BigQuery} = require('@google-cloud/bigquery');
const {Storage} = require('@google-cloud/storage');

// Instantiate clients
const bigquery = new BigQuery();
const storage = new Storage();

/**
 * This sample loads the CSV file at
 * https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.csv
 *
 * TODO(developer): Replace the following lines with the path to your file.
 */
const bucketName = 'cloud-samples-data';
const filename = 'bigquery/us-states/us-states.csv';

async function loadCSVFromGCS() {
  // Imports a GCS file into a table with manually defined schema.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  // Configure the load job. For full list of options, see:
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationLoad
  const metadata = {
    sourceFormat: 'CSV',
    skipLeadingRows: 1,
    schema: {
      fields: [
        {name: 'name', type: 'STRING'},
        {name: 'post_abbr', type: 'STRING'},
      ],
    },
    location: 'US',
  };

  // Load data from a Google Cloud Storage file into the table
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .load(storage.bucket(bucketName).file(filename), metadata);

  // load() waits for the job to finish
  console.log(`Job ${job.id} completed.`);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定操作說明進行操作。詳情請參閱 [BigQuery PHP API 參考文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;
use Google\Cloud\Core\ExponentialBackoff;

/** Uncomment and populate these variables in your code */
// $projectId  = 'The Google project ID';
// $datasetId  = 'The BigQuery dataset ID';

// instantiate the bigquery table service
$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$dataset = $bigQuery->dataset($datasetId);
$table = $dataset->table('us_states');

// create the import job
$gcsUri = 'gs://cloud-samples-data/bigquery/us-states/us-states.csv';
$schema = [
    'fields' => [
        ['name' => 'name', 'type' => 'string'],
        ['name' => 'post_abbr', 'type' => 'string']
    ]
];
$loadConfig = $table->loadFromStorage($gcsUri)->schema($schema)->skipLeadingRows(1);
$job = $table->runJob($loadConfig);
// poll the job until it is complete
$backoff = new ExponentialBackoff(10);
$backoff->execute(function () use ($job) {
    print('Waiting for job to complete' . PHP_EOL);
    $job->reload();
    if (!$job->isComplete()) {
        throw new Exception('Job has not yet completed', 500);
    }
});
// check if the job has errors
if (isset($job->info()['status']['errorResult'])) {
    $error = $job->info()['status']['errorResult']['message'];
    printf('Error running job: %s' . PHP_EOL, $error);
} else {
    print('Data imported successfully' . PHP_EOL);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 [Client.load\_table\_from\_uri()](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_load_table_from_uri) 方法，從 Cloud Storage 的 CSV 檔案載入資料。將 [LoadJobConfig.schema](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_schema) 屬性設為 [SchemaField](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.schema.SchemaField?hl=zh-tw#google_cloud_bigquery_schema_SchemaField) 物件清單，以提供明確的結構定義。

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
    skip_leading_rows=1,
    # The source format defaults to CSV, so the line below is optional.
    source_format=bigquery.SourceFormat.CSV,
)
uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
print("Loaded {} rows.".format(destination_table.num_rows))
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定操作說明進行操作。詳情請參閱 [BigQuery Ruby API 參考文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def load_table_gcs_csv dataset_id = "your_dataset_id"
  bigquery = Google::Cloud::Bigquery.new
  dataset  = bigquery.dataset dataset_id
  gcs_uri  = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
  table_id = "us_states"

  load_job = dataset.load_job table_id, gcs_uri, skip_leading: 1 do |schema|
    schema.string "name"
    schema.string "post_abbr"
  end
  puts "Starting job #{load_job.job_id}"

  load_job.wait_until_done! # Waits for table load to complete.
  puts "Job finished."

  table = dataset.table table_id
  puts "Loaded #{table.rows_count} rows to table #{table.id}"
end
```

## 將 CSV 資料載入使用資料欄時間分區的資料表

如要將 Cloud Storage 中的 CSV 資料載入使用資料欄時間分區的 BigQuery 資料表，請按照下列步驟操作：

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
)

// importPartitionedTable demonstrates specifing time partitioning for a BigQuery table when loading
// CSV data from Cloud Storage.
func importPartitionedTable(projectID, destDatasetID, destTableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states-by-date.csv")
	gcsRef.SkipLeadingRows = 1
	gcsRef.Schema = bigquery.Schema{
		{Name: "name", Type: bigquery.StringFieldType},
		{Name: "post_abbr", Type: bigquery.StringFieldType},
		{Name: "date", Type: bigquery.DateFieldType},
	}
	loader := client.Dataset(destDatasetID).Table(destTableID).LoaderFrom(gcsRef)
	loader.TimePartitioning = &bigquery.TimePartitioning{
		Field:      "date",
		Expiration: 90 * 24 * time.Hour,
	}
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

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobId;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TimePartitioning;
import java.time.Duration;
import java.time.temporal.ChronoUnit;
import java.util.UUID;

public class LoadPartitionedTable {

  public static void runLoadPartitionedTable() throws Exception {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "/path/to/file.csv";
    loadPartitionedTable(datasetName, tableName, sourceUri);
  }

  public static void loadPartitionedTable(String datasetName, String tableName, String sourceUri)
      throws Exception {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
```