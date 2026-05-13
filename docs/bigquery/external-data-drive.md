Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立 Google 雲端硬碟外部資料表

本文說明如何針對儲存在 Google 雲端硬碟中的資料建立外部資料表。

BigQuery 支援個人雲端硬碟檔案和共用檔案的外部資料表。如要進一步瞭解雲端硬碟，請參閱「[雲端硬碟訓練課程和相關說明](https://support.google.com/a/users/answer/9282958?hl=zh-tw)」。

您可以針對雲端硬碟中下列格式的檔案建立外部資料表：

* 逗號分隔值 (CSV)
* 換行符號分隔的 JSON
* Avro
* Google 試算表

## 事前準備

建立外部資料表前，請先蒐集一些資訊，並確認您有權建立資料表。

### 擷取雲端硬碟 URI

如要建立 Google 雲端硬碟資料來源的外部資料表，您必須提供[雲端硬碟 URI](#drive-uri)。您可以直接從雲端硬碟資料的網址取得雲端硬碟 URI：

**URI 格式**

* `https://docs.google.com/spreadsheets/d/FILE_ID`

  或
* `https://drive.google.com/open?id=FILE_ID`

其中 `FILE_ID` 是雲端硬碟檔案的英數字元 ID。

### 驗證並啟用雲端硬碟存取權

存取雲端硬碟中代管的資料需要額外的 OAuth 範圍。如要驗證 BigQuery 存取權並啟用雲端硬碟存取權，請執行下列操作：

### 控制台

在 Google Cloud 控制台中建立[外部資料表](#create_external_tables)時，請按照網頁驗證步驟操作。當系統提示時，按一下「允許」，將 Google 雲端硬碟的存取權授予 BigQuery 用戶端工具。

### gcloud

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 輸入以下指令，確認您擁有最新版本的 Google Cloud CLI。

   ```
   gcloud components update
   ```
3. 輸入下列指令，進行 Google 雲端硬碟驗證。

   ```
   gcloud auth login --enable-gdrive-access
   ```

**注意：** 如果您是使用 Cloud Shell 存取雲端硬碟資料，就不需要更新 Google Cloud CLI 或進行雲端硬碟驗證。

### API

除了 BigQuery 的範圍，您還必須要求適當的 [Google 雲端硬碟 OAuth 範圍](https://developers.google.com/identity/protocols/googlescopes?hl=zh-tw#drive)：

1. 執行 [`gcloud auth login --enable-gdrive-access` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/auth/login?hl=zh-tw)登入。
2. 執行 [`gcloud auth print-access-token` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/auth/print-access-token?hl=zh-tw)，取得用於 API 的雲端硬碟範圍 OAuth 存取權杖。

### Python

1. [建立 OAuth 用戶端 ID](https://support.google.com/cloud/answer/6158849?hl=zh-tw)。
2. 在本機環境中設定[應用程式預設憑證 (ADC)](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw)，並執行下列步驟，取得必要範圍：

   1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI，然後執行下列指令[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw)：

      ```
      gcloud init
      ```
   2. 為 Google 帳戶建立本機驗證憑證：

      ```
      gcloud auth application-default login \
          --client-id-file=CLIENT_ID_FILE \
          --scopes=https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/cloud-platform
      ```

      將 `CLIENT_ID_FILE` 替換為包含 OAuth 用戶端 ID 的檔案。

      詳情請參閱「[使用 gcloud CLI 提供的使用者憑證](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw#personal)」。

### Java

1. [建立 OAuth 用戶端 ID](https://support.google.com/cloud/answer/6158849?hl=zh-tw)。
2. 在本機環境中設定[應用程式預設憑證 (ADC)](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw)，並執行下列操作，取得必要範圍：

   1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI，然後執行下列指令[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw)：

      ```
      gcloud init
      ```
   2. 為 Google 帳戶建立本機驗證憑證：

      ```
      gcloud auth application-default login \
          --client-id-file=CLIENT_ID_FILE \
          --scopes=https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/cloud-platform
      ```

      將 `CLIENT_ID_FILE` 替換為包含 OAuth 用戶端 ID 的檔案。

      詳情請參閱「[使用 gcloud CLI 提供的使用者憑證](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw#personal)」。

### 必要的角色

如要建立外部資料表，您需要 `bigquery.tables.create`
BigQuery 身分與存取權管理 (IAM) 權限。

下列預先定義的 Identity and Access Management 角色都具備這項權限：

* BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)
* BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)
* BigQuery 管理員 (`roles/bigquery.admin`)

如果您不具備上述任一角色，請要求管理員授予存取權或為您建立外部資料表。

如要進一步瞭解 BigQuery 中的 Identity and Access Management 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 建立外部資料表

您可以透過下列方式建立已連結至外部資料來源的永久資料表：

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具的 `mk` 指令
* 在使用 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) API 方法時建立 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)
* 使用用戶端程式庫

如要建立外部資料表：

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在詳細資料窗格中，按一下「建立資料表」
   add\_box。
5. 在「Create table」(建立資料表) 頁面的「Source」(來源) 區段中：

   * 在「Create table from」(使用下列資料建立資料表) 部分，選取 [Drive] (雲端硬碟)。
   * 在「Select Drive URI」(選取雲端硬碟 URI) 欄位中，輸入 [Google 雲端硬碟 URI](#drive-uri)。請注意，雲端硬碟 URI 不支援萬用字元。
   * 在「File format」(檔案格式) 部分選取您所使用的資料格式。雲端硬碟資料的有效格式包括：

     + 逗號分隔值 (CSV)
     + 換行符號分隔的 JSON
     + Avro
     + 試算表**注意：** 在 Google Cloud 控制台中，選擇 Avro 或 Datastore 備份，系統就會隱藏「自動偵測」選項，因為這些檔案屬於自述式類型。
6. (選用) 如果選擇 Google 試算表，請在「Sheet range (Optional)」(工作表範圍 (選用)) 方塊中指定要查詢的工作表和儲存格範圍。您可以指定工作表名稱，也可以指定 `sheet_name!top_left_cell_id:bottom_right_cell_id` 當做儲存格範圍；例如「Sheet1！A1：B20」。如果未指定**工作表範圍**，系統則會使用檔案中的第一個工作表。
7. 在「Create table」(建立資料表) 頁面的「Destination」(目的地) 區段中：

   * 針對「Dataset name」(資料集名稱) 選擇適當的資料集，然後在「Table name」(資料表名稱) 欄位中，輸入您在 BigQuery 建立資料表時使用的名稱。
   * 確認「Table type」(資料表類型) 已設為 [External table] (外部資料表)。
8. 在「Schema」(結構定義) 區段中，輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。

   * 如果是 JSON 或 CSV 檔案，您可以勾選 [Auto-detect] (自動偵測) 選項，啟用結構定義[自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能。[Auto-detect] (自動偵測)  不適用於 Datastore 匯出項目、Firestore 匯出項目和 Avro 檔案。系統會自動從自述來源資料中擷取這些檔案類型的結構定義資訊。
   * 透過以下方式，手動輸入結構定義資訊：
     + 啟用 [Edit as text] (以文字形式編輯)，然後以 JSON 陣列的形式輸入資料表結構定義。注意：您可以在 bq 指令列工具中輸入下列指令，查看現有資料表的 JSON 格式結構定義：`bq show --format=prettyjson DATASET.TABLE`。
     + 使用 [Add Field] (新增欄位) 手動輸入結構定義。
9. 點選「建立資料表」。
10. 必要的話，選取帳戶然後按一下「Allow」(允許)，將 Google 雲端硬碟的存取權授予 BigQuery 用戶端工具。

接著，您就可以對資料表執行查詢，就像是標準 BigQuery 資料表一樣，但外部資料來源的[限制](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw#external_data_source_limitations)仍適用。

查詢完成後，可以將結果下載為 CSV 或 JSON、將結果儲存為資料表，或將結果儲存至 Google 試算表。詳情請參閱[下載、儲存及匯出資料](https://docs.cloud.google.com/bigquery/bigquery-web-ui?hl=zh-tw#exportdata)一文。

### bq

您可以使用 `bq mk` 指令在 bq 指令列工具中建立資料表。使用 bq 指令列工具建立連結至外部資料來源的資料表時，可以透過以下項目識別資料表的結構定義：

* [資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw) (儲存在本機)
* 內嵌結構定義
* JSON 結構定義檔 (儲存在本機)

如要使用資料表定義檔建立連結至雲端硬碟資料來源的永久資料表，請輸入以下指令。

```
bq mk \
--external_table_definition=DEFINITION_FILE \
DATASET.TABLE
```

其中：

* `DEFINITION_FILE` 是本機電腦上[資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)的路徑。
* `DATASET` 是包含該資料表之資料集的名稱。
* `TABLE` 是您所建立的資料表名稱。

舉例來說，以下指令會使用名稱為 `mytable_def` 的資料表定義檔，建立名為 `mytable` 的永久資料表。

```
bq mk --external_table_definition=/tmp/mytable_def mydataset.mytable
```

如要使用內嵌結構定義建立連結至外部資料來源的永久資料表，請輸入下列指令。

```
bq mk \
--external_table_definition=SCHEMA@SOURCE_FORMAT=DRIVE_URI \
DATASET.TABLE
```

其中：

* `SCHEMA` 是結構定義，格式為 `FIELD:DATA_TYPE,FIELD:DATA_TYPE`。
* `SOURCE_FORMAT` 為 `CSV`、`NEWLINE_DELIMITED_JSON`、`AVRO` 或 `GOOGLE_SHEETS`。
* `DRIVE_URI` 是您的 [雲端硬碟 URI](#drive-uri)。
* `DATASET` 是包含該資料表之資料集的名稱。
* `TABLE` 是您所建立的資料表名稱。

舉例來說，下列指令會使用 `Region:STRING,Quarter:STRING,Total_sales:INTEGER` 結構定義，建立名為 `sales` 的永久資料表，且此表會連結至儲存在雲端硬碟中的試算表檔案。

```
bq mk \
--external_table_definition=Region:STRING,Quarter:STRING,Total_sales:INTEGER@GOOGLE_SHEETS=https://drive.google.com/open?id=1234_AbCD12abCd \
mydataset.sales
```

如要使用 JSON 結構定義檔來建立已連結至外部資料來源的永久資料表，請輸入下列指令。

```
bq mk \
--external_table_definition=SCHEMA_FILE@SOURCE_FORMAT=DRIVE_URI \
DATASET.TABLE
```

其中：

* `SCHEMA_FILE` 是您本機上的 JSON 結構定義檔路徑。
* `SOURCE_FORMAT` 為 `CSV`、`NEWLINE_DELIMITED_JSON`、`AVRO` 或 `GOOGLE_SHEETS`。
* `DRIVE_URI` 是您的 [雲端硬碟 URI](#drive-uri)。
* `DATASET` 是包含該資料表之資料集的名稱。
* `TABLE` 是您所建立的資料表名稱。

如果您的[表格定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)包含[試算表專屬設定](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#GoogleSheetsOptions)，則可略過開頭的資料列，並指定定義的試算表範圍。

以下範例會使用 `/tmp/sales_schema.json` 結構定義檔，建立名為 `sales` 的資料表，且此表會連結至儲存在雲端硬碟中的 CSV 檔案。

```
bq mk \
--external_table_definition=/tmp/sales_schema.json@CSV=https://drive.google.com/open?id=1234_AbCD12abCd \
mydataset.sales
```

永久資料表建立完成後，您就可以對資料表執行查詢，就像是標準 BigQuery 資料表一樣，但外部資料來源的[限制](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw#external_data_source_limitations)仍適用。

查詢完成後，可以將結果下載為 CSV 或 JSON、將結果儲存為資料表，或將結果儲存至 Google 試算表。詳情請參閱[下載、儲存及匯出資料](https://docs.cloud.google.com/bigquery/bigquery-web-ui?hl=zh-tw#exportdata)一文。

### API

在使用 API 方法 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 時建立 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。指定 `schema` 屬性，或將 `autodetect` 屬性設為 `true`，為支援的資料來源啟用結構定義自動偵測功能。

### Python

```
from google.cloud import bigquery
import google.auth

credentials, project = google.auth.default()

# Construct a BigQuery client object.
client = bigquery.Client(credentials=credentials, project=project)

# TODO(developer): Set dataset_id to the ID of the dataset to fetch.
# dataset_id = "your-project.your_dataset"

# Configure the external data source.
dataset = client.get_dataset(dataset_id)
table_id = "us_states"
schema = [
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("post_abbr", "STRING"),
]
table = bigquery.Table(dataset.table(table_id), schema=schema)
external_config = bigquery.ExternalConfig("GOOGLE_SHEETS")
# Use a shareable link or grant viewing access to the email address you
# used to authenticate with BigQuery (this example Sheet is public).
sheet_url = (
    "https://docs.google.com/spreadsheets"
    "/d/1i_QCL-7HcSyUZmIbP9E6lO_T5u3HnpLe7dnpHaijg_E/edit?usp=sharing"
)
external_config.source_uris = [sheet_url]
options = external_config.google_sheets_options
assert options is not None
options.skip_leading_rows = 1  # Optionally skip header row.
options.range = (
    "us-states!A20:B49"  # Optionally set range of the sheet to query from.
)
table.external_data_configuration = external_config

# Create a permanent table linked to the Sheets file.
table = client.create_table(table)  # Make an API request.

# Example query to find states starting with "W".
sql = 'SELECT * FROM `{}.{}` WHERE name LIKE "W%"'.format(dataset_id, table_id)

results = client.query_and_wait(sql)  # Make an API request.

# Wait for the query to complete.
w_states = list(results)
print(
    "There are {} states with names starting with W in the selected range.".format(
        len(w_states)
    )
)
```

### Java

```
import com.google.auth.oauth2.GoogleCredentials;
import com.google.auth.oauth2.ServiceAccountCredentials;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.ExternalTableDefinition;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.GoogleSheetsOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;
import com.google.cloud.bigquery.TableResult;
import com.google.common.collect.ImmutableSet;
import java.io.IOException;

// Sample to queries an external data source using a permanent table
public class QueryExternalSheetsPerm {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri =
        "https://docs.google.com/spreadsheets/d/1i_QCL-7HcSyUZmIbP9E6lO_T5u3HnpLe7dnpHaijg_E/edit?usp=sharing";
    Schema schema =
        Schema.of(
            Field.of("name", StandardSQLTypeName.STRING),
            Field.of("post_abbr", StandardSQLTypeName.STRING));
    String query =
        String.format("SELECT * FROM %s.%s WHERE name LIKE 'W%%'", datasetName, tableName);
    queryExternalSheetsPerm(datasetName, tableName, sourceUri, schema, query);
  }

  public static void queryExternalSheetsPerm(
      String datasetName, String tableName, String sourceUri, Schema schema, String query) {
    try {

      GoogleCredentials credentials =
          ServiceAccountCredentials.getApplicationDefault();

      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery =
          BigQueryOptions.newBuilder().setCredentials(credentials).build().getService();

      // Skip header row in the file.
      GoogleSheetsOptions sheetsOptions =
          GoogleSheetsOptions.newBuilder()
              .setSkipLeadingRows(1) // Optionally skip header row.
              .setRange("us-states!A20:B49") // Optionally set range of the sheet to query from.
              .build();

      TableId tableId = TableId.of(datasetName, tableName);
      // Create a permanent table linked to the Sheets file.
      ExternalTableDefinition externalTable =
          ExternalTableDefinition.newBuilder(sourceUri, sheetsOptions).setSchema(schema).build();
      bigquery.create(TableInfo.of(tableId, externalTable));

      // Example query to find states starting with 'W'
      TableResult results = bigquery.query(QueryJobConfiguration.of(query));

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query on external permanent table performed successfully.");
    } catch (BigQueryException | InterruptedException | IOException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

## 查詢外部資料表

詳情請參閱「[查詢雲端硬碟資料](https://docs.cloud.google.com/bigquery/docs/query-drive-data?hl=zh-tw)」。

## `_FILE_NAME` 虛擬資料欄

以外部資料來源為基礎的資料表可提供名為 `_FILE_NAME` 的虛擬資料欄。這個資料欄含有該列所屬檔案的完整路徑。此資料欄僅適用於參照儲存在 **Cloud Storage** 和 **Google 雲端硬碟**中的外部資料的資料表。

系統會保留 `_FILE_NAME` 資料欄名稱，這表示您無法在任何資料表中使用該名稱建立資料欄。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]