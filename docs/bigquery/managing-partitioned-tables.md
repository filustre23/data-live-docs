Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理分區資料表

本文說明如何在 BigQuery 中管理分區資料表。

**注意：** 「[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)」中的資訊也適用於分區資料表。

## 取得分區中繼資料

您可以透過下列方式取得分區資料表的相關資訊：

* 使用 [`INFORMATION_SCHEMA.PARTITIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-partitions?hl=zh-tw) 檢視畫面 (「預覽」)。
* 使用 `__PARTITIONS_SUMMARY__` 中繼資料表 (僅限舊版 SQL)。

### 使用 `INFORMATION_SCHEMA` 檢視表取得分區中繼資料

查詢 `INFORMATION_SCHEMA.PARTITIONS` 檢視表時，查詢結果會為每個分區包含一個資料列。舉例來說，下列查詢會列出資料集中特定資料表的所有分區：

```
#standardSQL
SELECT
  partition_id
FROM
  `DATASET_ID.INFORMATION_SCHEMA.PARTITIONS`
WHERE
  table_name = 'TABLE_NAME'
  AND partition_id IS NOT NULL --filter out non-partitioned tables
```

詳情請參閱「[`INFORMATION_SCHEMA.PARTITIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-partitions?hl=zh-tw)」。

### 使用中繼資料表取得分區中繼資料

在舊版 SQL 中，您可以查詢 `__PARTITIONS_SUMMARY__` 中繼資料表，取得資料表分區的中繼資料。*中繼資料表*是唯讀資料表，內含中繼資料。

查詢 `__PARTITIONS_SUMMARY__` 中繼資料表，如下所示：

```
#legacySQL
SELECT
  partition_id
FROM
  [DATASET_ID.TABLE_NAME$__PARTITIONS_SUMMARY__]
```

**注意：** 如要遷移至 GoogleSQL，請參閱[舊版 SQL 遷移說明文件](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-tw#migrating_partition_meta_table_decorator)。

`__PARTITIONS_SUMMARY__` 中繼資料表包含下列資料欄：

| 值 | 說明 |
| --- | --- |
| `project_id` | 專案名稱。 |
| `dataset_id` | 資料集名稱。 |
| `table_id` | 時間分區資料表的名稱。 |
| `partition_id` | 分區名稱 (日期)。 |
| `creation_time` | 分區的建立時間，從世界標準時間 1970 年 1 月 1 日開始計算，並以毫秒為單位。 |
| `last_modified_time` | 分區的前次修改時間，從世界標準時間 1970 年 1 月 1 日開始計算，並以毫秒為單位。 |

如要執行使用 `__PARTITIONS_SUMMARY__` 中繼資料表的查詢工作，您至少必須具備 `bigquery.jobs.create` 權限和 `bigquery.tables.getData` 權限。

如要進一步瞭解 BigQuery 中的身分與存取權管理角色，請參閱[存取權控管](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)。

## 設定分區到期時間

建立以擷取時間或時間單位資料欄分區的資料表時，您可以指定分區到期時間。這項設定會指定 BigQuery 保留各分區資料的時間長度。這項設定會套用至資料表中的所有分區，但系統會根據分區時間，為每個分區獨立計算。

分區的到期時間是根據世界標準時間的分區界線計算。舉例來說，如果採用每日分區，分區界線就是午夜 (世界標準時間 00:00:00)。如果資料表的分區到期時間為 6 小時，則每個分區會在隔天的世界標準時間 06:00:00 到期。分區過期時，BigQuery 會刪除該分區中的資料。

您也可以在資料集層級指定[預設分區到期時間](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#partition-expiration)。如果您為資料表設定分區到期時間，該值會覆寫預設分區到期時間。如果您未指定任何分區到期時間 (在資料表或資料集上)，分區就永遠不會過期。

**注意：** 整數範圍分區資料表不支援分區到期時間。

如果您設定資料表到期時間，該值會優先於分區到期時間。舉例來說，如果資料表到期時間設為 5 天，分區到期時間設為 7 天，則資料表和其中的所有分區會在 5 天後刪除。

建立資料表後，您可以隨時更新資料表的分區到期時間。無論分區何時建立，新設定都會套用到該資料表中的所有分區。如果現有分區的建立時間早於新的有效期限，就會立即過期。同樣地，如果資料要複製或插入按時間單位資料欄分區的資料表，系統會立即讓任何早於資料表設定分區到期時間的分區過期。

分區到期時，BigQuery 會刪除該分區。
系統會依據[時間旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)和[安全防護](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#fail-safe)政策保留分割區資料，並視您的帳單模式而定，可能需要支付相關費用。在此之前，資料表配額的[分區計數](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#partitioned_tables)仍會維持不變。如要立即刪除分區，可以[手動刪除分區](#delete_a_partition)。

**注意：** BigQuery 稽核記錄不會記錄過期分區的自動刪除作業。

### 更新分區到期時間

更新分區資料表的分區到期時間：

### 控制台

您無法在 Google Cloud 控制台中更新分區到期時間。

### SQL

使用 [`ALTER TABLE SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)。以下範例會將效期更新為 5 天。如要移除資料表的分區到期時間，請將 `partition_expiration_days` 設為 `NULL`。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mytable
     SET OPTIONS (
       -- Sets partition expiration to 5 days
       partition_expiration_days = 5);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

發出含有 `--time_partitioning_expiration` 旗標的 `bq update` 指令。如果您要更新非預設專案中的分區資料表，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

```
bq update \
--time_partitioning_expiration integer_in_seconds \
--time_partitioning_type unit_time \
project_id:dataset.table
```

其中：

* integer 是資料表分區的預設生命週期 (以秒為單位)，這個值沒有下限。到期時間為分區日期加整數值。如果您指定 `0`，就會移除分區到期時間，分區將永遠不會過期。沒有到期時間的分區必須手動刪除。
* unit\_time 為 `DAY`、`HOUR`、`MONTH` 或 `YEAR`，取決於資料表的分區切分單位。這個值必須與您建立資料表時設定的精細程度相符。
* project\_id 是您的專案 ID。
* dataset 是含有您要更新資料表的資料集名稱。
* table 是您要更新之資料表的名稱。

範例：

輸入下列指令，將 `mydataset.mytable` 中的分區到期時間更新為 5 天 (432000 秒)。`mydataset` 在您的預設專案中。

```
bq update --time_partitioning_expiration 432000 mydataset.mytable
```

輸入下列指令，將 `mydataset.mytable` 中的分區到期時間更新為 5 天 (432000 秒)。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq update \
--time_partitioning_expiration 432000 \
myotherproject:mydataset.mytable
```

### API

呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法，並使用 `timePartitioning.expirationMs` 屬性來更新分區到期時間 (以毫秒為單位)。由於 `tables.update` 方法會取代整個資料表資源，因此建議使用 `tables.patch` 方法。

## 設定分區篩選器必要條件

建立分區資料表時，您可以要求對該資料表的所有查詢，都必須包含根據分區資料欄篩選的述詞篩選器 (`WHERE` 子句)。這項設定可以提升效能並降低成本，因為 BigQuery 可以使用篩選器，修剪不符合述詞的分區。這項規定也適用於參照分區資料表的檢視區和具體化檢視區查詢。

如要瞭解如何在建立分區資料表時新增「Require partition filter」(需要分區篩選器) 選項，請參閱[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)一節。

如果分區資料表設有「需要分區篩選器」，則對該資料表執行的每項查詢都必須至少包含一個述詞，且該述詞只能參照分區欄。如果查詢沒有這類述詞，就會傳回下列錯誤：

`Cannot query over table 'project_id.dataset.table' without a
filter that can be used for partition elimination`。

詳情請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)一文。

### 更新分區篩選器必要條件

如果您在建立分區資料表時未啟用「Require partition filter」(需要分區篩選器) 選項，可以更新資料表以新增選項。

### 控制台

建立分區資料表後，您無法使用 Google Cloud 控制台要求啟用分區篩選器。

### SQL

使用 [`ALTER TABLE SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)更新分區篩選器必要條件。以下範例會將需求更新為 `true`：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mypartitionedtable
     SET OPTIONS (
       require_partition_filter = true);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要使用 bq 指令列工具更新分區資料表，以要求使用分區篩選器，請輸入 `bq update` 指令並加上 `--require_partition_filter` 旗標。

如要更新非預設專案中的分區資料表，請使用下列格式將專案 ID 新增到資料集：project\_id:dataset。

例如：

如要在預設專案中更新 `mydataset` 中的 `mypartitionedtable`，請輸入：

```
bq update --require_partition_filter mydataset.mytable
```

如要在 `myotherproject` 中更新 `mydataset` 中的 `mypartitionedtable`，請輸入：

```
bq update --require_partition_filter myotherproject:mydataset.mytable
```

### API

呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法並將 `requirePartitionFilter` 屬性設定為 `true` 以要求使用分區篩選器。由於 `tables.update` 方法會取代整個資料表資源，因此建議使用 `tables.patch` 方法。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Table;

// Sample to update require partition filter on a table.
public class UpdateTableRequirePartitionFilter {

  public static void runUpdateTableRequirePartitionFilter() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    updateTableRequirePartitionFilter(datasetName, tableName);
  }

  public static void updateTableRequirePartitionFilter(String datasetName, String tableName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Table table = bigquery.getTable(datasetName, tableName);
      table.toBuilder().setRequirePartitionFilter(true).build().update();

      System.out.println("Table require partition filter updated successfully");
    } catch (BigQueryException e) {
      System.out.println("Table require partition filter was not updated \n" + e.toString());
    }
  }
}
```

## 複製分區資料表

複製分區資料表的程序，與複製標準資料表的程序相同。詳情請參閱[複製資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)一節。

複製分區資料表時，請注意以下幾點：

* 將分區資料表複製到新的目的地資料表
  :   所有分區資訊都會隨資料表一起複製。新資料表與舊資料表的分區相同。
* 將非分區資料表複製到現有的分區資料表
  :   這項操作僅支援擷取時間分區。BigQuery 會將來源資料複製到代表目前日期的分區。這項作業不支援依時間單位資料欄分區或整數範圍分區的資料表。
* 將分區資料表複製到其他分區資料表
  :   來源與目的地資料表的分區設定必須相符。
* 將分區資料表複製到非分區資料表
  :   目的地資料表會保持不分區。
* 複製多個分區資料表
  :   如果您將多個來源資料表複製到相同工作中的分區資料表，來源資料表不能同時包含分區與非分區資料表。

      如果所有來源資料表都是分區資料表，則所有來源資料表的分區設定都必須符合目的地資料表的分區設定。
* 複製具有[分群規格](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)的分區資料表
  :   如果您複製到新資料表，所有分群資訊都會隨資料表一起複製。新資料表與舊資料表的叢集相同。

      如果複製到現有資料表，來源和目的地資料表的叢集規格必須相符。

複製到現有資料表時，您可以指定要附加還是覆寫目的地資料表。

## 複製個別分區

您可以將一或多個分區的資料複製到其他資料表。

**注意：** 所需權限與[複製表格](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)相同。

### 控制台

Google Cloud 主控台不支援複製分區。

### bq

如要複製分區，請使用 bq 指令列工具的 `bq cp` (複製) 指令與分區修飾符 (`$date`)，例如 `$20160201`。

選用標記可用來控管目的地分區的寫入配置：

* `-a` 或 `--append_table`：把來源分區的資料附加到目的地資料集中的現有資料表或分區。
* `-f` 或 `--force`：覆寫目的地資料集中的現有資料表或分區，此作業不會有確認提示。
* 如果目的地資料集中已有資料表或分區，`-n` 或 `--no_clobber` 會傳回下列錯誤訊息：`Table '<var>project_id:dataset.table</var> or <var>table$date</var>'
  already exists, skipping.`。如未指定 `-n`，預設行為是提示您選擇是否要取代目的地資料表或分區。
* `--destination_kms_key`：客戶管理的 Cloud KMS 金鑰，可用來加密目的地資料表或分區。

`cp` 指令不支援 `--time_partitioning_field` 或 `--time_partitioning_type` 旗標。您無法使用複製工作將擷取時間分區資料表轉換為分區資料表。

本文不示範 `--destination_kms_key`。詳情請參閱[使用 Cloud KMS 金鑰保護資料](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)一文。

如果來源或目的地資料集位於非預設專案中，請採用下列格式將專案 ID 新增至該資料集名稱：`project_id:dataset`。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

```
bq --location=location cp \
-a -f -n \
project_id:dataset.source_table$source_partition \
project_id:dataset.destination_table$destination_partition
```

其中：

* location 是您的位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)，設定該位置的預設值。
* project\_id 是您的專案 ID。
* dataset 是來源或目的地資料集的名稱。
* source\_table 是您要複製的資料表。
* source\_partition 是來源分區的分區修飾符。
* destination\_table 是目的地資料集中的資料表名稱。
* destination\_partition 是目的地分區的分區修飾符。

範例：

**附註：**分區修飾符的分隔符 ($) 是 Unix Shell 中的一種特殊變數。使用指令列工具時，您可能需要逸出修飾符。以下為逸出分區修飾符的範例：`mydataset.table\$20160519`、`'mydataset.table$20160519'`。

**將分區複製到新資料表**

輸入下列指令，將 2018 年 1 月 30 日的分區從 `mydataset.mytable` 複製到新資料表：`mydataset.mytable2`。`mydataset` 在您的預設專案中。

```
bq cp -a 'mydataset.mytable$20180130' mydataset.mytable2
```

**將分區複製到非分區資料表**

輸入下列指令，將 2018 年 1 月 30 日的分區從 `mydataset.mytable` 複製到非分區資料表：`mydataset2.mytable2`。`-a` 捷徑可用來將分區的資料附加至非分區目的地資料表。兩個資料集都在您的預設專案中。

```
bq cp -a 'mydataset.mytable$20180130' mydataset2.mytable2
```

輸入下列指令，將 2018 年 1 月 30 日的分區從 `mydataset.mytable` 複製到非分區資料表：`mydataset2.mytable2`。`-f` 捷徑可用來在無提示的情況下覆寫非分區目的地資料表。

```
bq --location=US cp -f 'mydataset.mytable$20180130' mydataset2.mytable2
```

**將分區複製到其他分區資料表**

輸入下列指令，將 2018 年 1 月 30 日的分區從 `mydataset.mytable` 複製到其他分區資料表：`mydataset2.mytable2`。`-a` 捷徑可用來將分區的資料附加至目的地資料表。由於目的地資料表上未指定分區修飾符，因此會保留來源分區索引鍵，並將資料複製到目的地資料表中 2018 年 1 月 30 日的分區。您也可以在目的地資料表上指定分區修飾符，將資料複製到指定的分區。`mydataset` 在您的預設專案中。`mydataset2` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq --location=US cp \
-a \
'mydataset.mytable$20180130' \
myotherproject:mydataset2.mytable2
```

輸入下列指令，將 2018 年 1 月 30 日的分區從 `mydataset.mytable` 複製到另一個分區資料表 `mydataset2.mytable2` 的 2018 年 1 月 30 日分區。`-f` 捷徑可用來在無提示的情況下覆寫目的地資料表中 2018 年 1 月 30 日的分區。如未使用分區修飾符，則會覆寫目的地資料表中的所有資料。`mydataset` 在您的預設專案中。`mydataset2` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq cp \
-f \
'mydataset.mytable$20180130' \
'myotherproject:mydataset2.mytable2$20180130'
```

輸入下列指令，將 2018 年 1 月 30 日的分區從 `mydataset.mytable` 複製到其他分區資料表：`mydataset2.mytable2`。`mydataset` 在您的預設專案中。`mydataset2` 在 `myotherproject` 中，而不是您的預設專案中。如果目的地資料表中有資料，則預設行為是提示您進行覆寫。

```
bq cp \
'mydataset.mytable$20180130' \
myotherproject:mydataset2.mytable2
```

**注意：** 含分區修飾符的 `bq cp` 指令適用於以資料欄為基礎的分區，其中來源分區和目的地分區相同。`bq cp` 指令也適用於以擷取時間為準的分區，其中分區代表相同的時間單位，或包含來源分區的較粗略時間單位。舉例來說，如果 `$20180130` 是來源分區修飾符，有效目的地分區修飾符包括 `$20180130`、`$201801` 和 `$2018`。如要將以資料欄為準的分區複製到完全不同的分區修飾符，或複製到更精細的時間單位分區，請使用 [`INSERT SELECT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)。

如要複製多個分區，請以逗號分隔的清單形式指定分區：

```
bq cp \
'mydataset.mytable$20180130,mydataset.mytable$20180131' \
myotherproject:mydataset.mytable2
```

### API

呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法，並設定 `copy` 工作。(選用) 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定您的位置。

在工作設定中指定下列屬性：

* 在 `sourceTables` 屬性中輸入來源資料集、資料表和分區。
* 在 `destinationTable` 屬性中輸入目的地資料集和資料表。
* 使用 `writeDisposition` 屬性指定要附加或覆寫目的地資料表或分區。

如要複製多個分區，請在 `sourceTables` 屬性中輸入來源分區 (包括資料集和資料表名稱)。

## 刪除分區

您可以從分區資料表刪除個別分區。不過，您無法刪除特殊 `__NULL__` 或 `__UNPARTITIONED__` 分區。

一次只能刪除一個分區。

**注意：** 所需權限與[刪除資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#deleting_tables)相同。

您可以藉由指定分區的修飾符來刪除分區，但有兩個[特殊分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)是例外。

刪除分區資料表中的分區：

### 控制台

Google Cloud 主控台不支援刪除分區。

### SQL

如果[符合條件的 `DELETE` 陳述式](https://docs.cloud.google.com/bigquery/docs/using-dml-with-partitioned-tables?hl=zh-tw#using_dml_delete_to_delete_partitions)涵蓋分區中的所有資料列，BigQuery 就會移除整個分區。系統會移除這些檔案，不會掃描位元組或耗用配額。以下 `DELETE` 陳述式範例涵蓋 `_PARTITIONDATE` 虛擬資料欄篩選器的整個分區：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   DELETE mydataset.mytable
   WHERE _PARTITIONDATE IN ('2076-10-07', '2076-03-06');
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 `bq rm` 指令並搭配使用 `--table` 旗標 (或 `-t` 捷徑)，以及指定分區修飾符來刪除特定分區。

```
bq rm --table project_id:dataset.table$partition
```

其中：

* project\_id 是您的專案 ID。如果省略此參數，系統會使用預設專案。
* dataset 是包含該資料表之資料集的名稱。
* table 是資料表名稱。
* partition 是您要刪除分區的分區修飾符。

分區裝飾器格式如下，視分區類型而定：

* 每小時分割：`yyyymmddhh`。範例：`$2016030100`。
* 每日分割：`yyyymmdd`。範例：`$20160301`。
* 每月分割：`yyyymm`。範例：`$201603`。
* 年度分區：`yyyy`。範例：`$2016`。
* 整數範圍分區：分區範圍的起始值。範例：`$20`。

bq 指令列工具會提示您確認這項動作。如要略過確認程序，請使用 `--force` 旗標 (或 `-f` 捷徑)。

**附註：**分區修飾符的分隔符 ($) 是 Unix Shell 中的一種特殊變數。使用指令列工具時，您可能需要逸出修飾符。以下為逸出分區修飾符的範例：`mydataset.table\$20160519`、`'mydataset.table$20160519'`。

範例：

在預設專案中，刪除名為 `mydataset.mytable` 的每日分區資料表中的 2016 年 3 月 1 日分區：

```
bq rm --table 'mydataset.mytable$20160301'
```

在按月分區的資料表中，刪除 2016 年 3 月的分區：

```
bq rm --table 'mydataset.mytable$201603'
```

在名為 `mydataset.mytable` 的整數範圍分區資料表中，刪除從 20 開始的整數範圍：

```
bq rm --table 'mydataset.mytable$20'
```

### API

呼叫 [`tables.delete`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete?hl=zh-tw) 方法，並使用 `tableId` 參數來指定資料表和分區修飾符。

## 分區資料表安全性

分區資料表的存取控管方式與標準資料表相同。詳情請參閱[資料表存取權控管簡介](https://docs.cloud.google.com/bigquery/docs/table-access-controls-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]