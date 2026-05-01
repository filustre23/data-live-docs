* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立邏輯檢視畫面

本文說明如何在 BigQuery 中建立邏輯檢視表。

您可以透過下列方式建立邏輯檢視區塊：

* 使用 Google Cloud 控制台。
* 使用 bq 指令列工具的 `bq mk` 指令。
* 呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables/insert?hl=zh-tw) API 方法
* 使用用戶端程式庫。
* 提交 [`CREATE VIEW`](https://docs.cloud.google.com/bigquery/docs/data-definition-language?hl=zh-tw#create_view_statement) 資料定義語言 (DDL) 陳述式。

## 資料檢視限制

BigQuery 資料檢視有下列幾項限制：

* 檢視畫面為唯讀。舉例來說，您無法執行插入、更新或刪除資料的查詢。
* 如果檢視區塊參照遠端[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)的資料表，您必須先啟用[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)，才能建立檢視區塊。
* 檢視表內的參照必須符合資料集資格。預設資料集不會影響檢視區塊主體。
* 您無法使用 `TableDataList` JSON API 方法從檢視表擷取資料。詳情請參閱 [Tabledata：list](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 的相關說明。
* 使用檢視表時，不能混用 GoogleSQL 和舊版 SQL 查詢。GoogleSQL 查詢無法參照使用舊版 SQL 語法定義的檢視表。
* 您無法在檢視表中參照[查詢參數](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw)。
* 建立檢視表時，系統會將基礎資料表的結構定義和檢視表一併儲存。如果在檢視表建立後新增、刪除或修改資料欄，檢視表不會自動更新，且回報的結構定義會維持不正確，直到變更檢視表 SQL 定義或重新建立檢視表為止。不過即使回報的結構定義不正確，所有提交的查詢還是會產生正確的結果。
* 您無法將舊版 SQL 檢視表自動更新為 GoogleSQL 語法。如要修改用來定義檢視表的查詢，可以使用下列項目：
  + Google Cloud 控制台中的「編輯查詢」選項
  + bq 指令列工具中的 [`bq update --view`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令
  + [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)
  + [update](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/update?hl=zh-tw) 或 [patch](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API 方法。
* 您無法在定義檢視表的 SQL 查詢中加入暫時性使用者定義函式或暫時性資料表。
* 您無法在[萬用字元資料表](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)查詢中參照資料檢視。
* 邏輯檢視區塊無法繼承或明確定義[參數化資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_data_types)，例如 `STRING(n)`，因為參數化資料類型僅支援基本資料表資料欄和指令碼變數。

如要瞭解檢視表適用的配額及限制，請參閱「[檢視表限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#view_limits)」。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文件各項工作所需的權限。

### 所需權限

BigQuery 會將檢視表視為資料表資源，因此建立檢視表需要的權限和建立資料表相同。您還需擁有檢視表 SQL 查詢所參照的資料表查詢權限。

如要建立資料檢視，您需要 `bigquery.tables.create` IAM 權限。`roles/bigquery.dataEditor` 預先定義的 IAM 角色包含建立檢視區塊所需的權限。

此外，如果您具備 `bigquery.datasets.create` 權限，可以在您建立的資料集中建立檢視區塊。如要為不屬於您的資料建立檢視區塊，您必須具備該資料表的 `bigquery.tables.getData` 權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

**注意：** 如要建立或更新[授權 view](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)，或是[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw#create_or_update_view)中的檢視表，您需要額外權限。詳情請參閱「[授權檢視表的必要權限](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw#required_permissions)」和「[授權資料集檢視表的必要權限](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw#permissions_datasets)」。

## 檢視表命名

在 BigQuery 中建立檢視表時，檢視表名稱在同一資料集中不得重複。以下是檢視表的命名規則：

* 包含的字元總計最多 1,024 個 UTF-8 位元組。
* 包含類別 L (字母)、M (標記)、N (數字)、Pc (連接符，包括底線)、Pd (破折號)、Zs (空格) 的 Unicode 字元。詳情請參閱「[一般類別](https://wikipedia.org/wiki/Unicode_character_property#General_Category)」。

以下是有效檢視畫面名稱的範例：`view 01`、`ग्राहक`、`00_お客様`、`étudiant-01`。

注意事項：

* 根據預設，資料表名稱會區分大小寫。`mytable` 和 `MyTable` 可以共存在同一個資料集中，除非是[已關閉大小寫區分功能的資料集](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_case-insensitive_dataset)。
* 我們已保留特定檢視區塊名稱和檢視區塊名稱前置字元，如果收到錯誤訊息，指出檢視區塊名稱或前置字元已保留，請選取其他名稱，然後再試一次。
* 如果您在序列中加入多個點運算子 (`.`)，系統會自動移除重複的運算子。

  例如：
  `project_name....dataset_name..table_name`

  變成這樣：
  `project_name.dataset_name.table_name`

## 建立檢視表

您可以撰寫用來定義檢視表可存取之資料的 SQL 查詢，藉此建立檢視表。SQL 查詢必須包含 `SELECT` 陳述式。
檢視表查詢不允許使用其他陳述式類型 (例如 DML 陳述式) 和[多個陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)，但 `@@session_id`
[系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)除外。

如何建立資料檢視：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「SQL 查詢」add\_box。
3. 在查詢編輯器中輸入有效的 SQL 查詢。

   或者，您也可以[開啟已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#open_a_saved_query_version_as_a_new_query)。
4. 依序點選
5. 在「Save view」(儲存檢視表) 對話方塊中：

   * 在「Project」選單中，選取要儲存檢視表的專案。
   * 在「資料集」選單中，選取資料集或建立新資料集來儲存檢視區塊。已儲存檢視表的目的地資料集必須與來源位於相同[區域](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。
   * 在「Table」(資料表) 欄位中，輸入檢視表的名稱。
   * 按一下 [儲存]。

**注意：** 使用 Google Cloud console 建立檢視表時，您無法加入標籤、說明或到期時間；您可以在使用 API 或 bq 指令列工具建立檢視區時，新增這些選用屬性。使用 Google Cloud 控制台建立檢視表後，即可新增到期時間、說明和標籤。詳情請參閱[更新檢視表](https://docs.cloud.google.com/bigquery/docs/updating-views?hl=zh-tw)的相關說明。

### SQL

使用 [`CREATE VIEW` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_view_statement)。下列範例會從美國人名公開資料集建立名為 `usa_male_names` 的檢視區塊：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE VIEW mydataset.usa_male_names(name, number) AS (
     SELECT
       name,
       number
     FROM
       `bigquery-public-data.usa_names.usa_1910_current`
     WHERE
       gender = 'M'
     ORDER BY
       number DESC
   );
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)並加上 `--view` 旗標。如果是 GoogleSQL 查詢，請加入 `--use_legacy_sql` 旗標，並將旗標設定為 `false`。可選用的參數包括 `--add_tags`、`--expiration`、`--description` 和 `--label`。如需完整參數清單，請參閱 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)參考資料。

如果查詢參照儲存在 Cloud Storage 或本機檔案中的外部使用者定義函式 (UDF) 資源，請使用 `--view_udf_resource` 旗標指定這些資源。本文不示範 `--view_udf_resource` 旗標。如要進一步瞭解如何使用 UDF，請參閱「[UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)」一文。

如果要在預設專案以外的專案中建立檢視表，請使用 `--project_id` 旗標來指定專案 ID。

**注意：**包含檢視表的資料集，以及包含檢視表參照之資料表的資料集，必須位於同一個[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

```
bq mk \
--use_legacy_sql=false \
--view_udf_resource=PATH_TO_FILE \
--expiration=INTEGER \
--description="DESCRIPTION" \
--label=KEY_1:VALUE_1 \
--add_tags=KEY_2:VALUE_2[,...] \
--view='QUERY' \
--project_id=PROJECT_ID \
DATASET.VIEW
```

更改下列內容：

* `PATH_TO_FILE` 是程式碼檔案的 URI 或本機檔案系統路徑，該檔案會做為檢視表使用的使用者定義函式資源，而立即載入並進行評估。請重複該標記以指定多個檔案。
* `INTEGER` 會設定檢視區塊的生命週期 (以秒為單位)。如果 `INTEGER` 為 `0`，檢視畫面就不會過期。如果未加入 `--expiration` 旗標，BigQuery 會使用資料集的預設資料表生命週期建立檢視區塊。
* `DESCRIPTION` 是資料檢視的說明，會用引號括住。
* `KEY_1:VALUE_1` 是代表[標籤](https://docs.cloud.google.com/bigquery/docs/labels?hl=zh-tw)的鍵/值組合。重複使用 `--label` 旗標即可指定多個標籤。
* `KEY_2:VALUE_2` 是代表[標記](https://docs.cloud.google.com/bigquery/docs/labels?hl=zh-tw)的鍵/值組合。在相同旗標下新增多個標記，並在鍵/值組合之間加上半形逗號。
* `QUERY` 是有效的查詢。
* `PROJECT_ID` 是您的專案 ID (若未設定預設專案)。
* `DATASET` 是專案中的資料集。
* `VIEW` 是您要建立的檢視區塊名稱。

範例：

輸入下列指令，在預設專案的 `mydataset` 中建立名為 `myview` 的檢視表。到期時間設為 3600 秒 (1 小時)、說明設為 `This is my view`，標籤則設為 `organization:development`。用於建立檢視區塊的查詢會查詢來自[美國人名資料公開資料集](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=usa_names&%3Bpage=dataset&hl=zh-tw)的資料。

```
bq mk \
--use_legacy_sql=false \
--expiration 3600 \
--description "This is my view" \
--label organization:development \
--view \
'SELECT
  name,
  number
FROM
  `bigquery-public-data.usa_names.usa_1910_current`
WHERE
  gender = "M"
ORDER BY
  number DESC' \
mydataset.myview
```

輸入下列指令，在 `myotherproject` 中的 `mydataset` 建立名為 `myview` 的檢視表。說明設為 `This is my view`、標籤設為 `organization:development`，而檢視的到期時間則設為資料集的預設資料表到期時間。用於建立檢視區塊的查詢會查詢來自[美國人名資料公開資料集](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=usa_names&%3Bpage=dataset&hl=zh-tw)的資料。

```
bq mk \
--use_legacy_sql=false \
--description "This is my view" \
--label organization:development \
--project_id myotherproject \
--view \
'SELECT
  name,
  number
FROM
  `bigquery-public-data.usa_names.usa_1910_current`
WHERE
  gender = "M"
ORDER BY
  number DESC' \
mydataset.myview
```

建立檢視表後，您可以更新檢視表的到期時間、說明和標籤。詳情請參閱[更新檢視表](https://docs.cloud.google.com/bigquery/docs/updating-views?hl=zh-tw)的相關說明。

### Terraform

請使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會建立名為 `myview` 的檢視區塊：

```
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "mydataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

  labels = {
    billing_group = "accounting",
    pii           = "sensitive"
  }
}

resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = "myview"

  view {
    query          = "SELECT global_id, faa_identifier, name, latitude, longitude FROM `bigquery-public-data.faa.us_airports`"
    use_legacy_sql = false
  }

}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   每項專案只需要執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 檢查設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

使用含有 `view` 屬性的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables?hl=zh-tw)呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables/insert?hl=zh-tw) 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// createView demonstrates creation of a BigQuery logical view.
func createView(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydatasetid"
	// tableID := "mytableid"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	meta := &bigquery.TableMetadata{
		// This example shows how to create a view of the shakespeare sample dataset, which
		// provides word frequency information.  This view restricts the results to only contain
		// results for works that contain the "king" in the title, e.g. King Lear, King Henry V, etc.
		ViewQuery: "SELECT word, word_count, corpus, corpus_date FROM `bigquery-public-data.samples.shakespeare` WHERE corpus LIKE '%king%'",
	}
	if err := client.Dataset(datasetID).Table(tableID).Create(ctx, meta); err != nil {
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;
import com.google.cloud.bigquery.ViewDefinition;

// Sample to create a view
public class CreateView {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String viewName = "MY_VIEW_NAME";
    String query =
        String.format(
            "SELECT TimestampField, StringField, BooleanField FROM %s.%s", datasetName, tableName);
    createView(datasetName, viewName, query);
  }

  public static void createView(String datasetName, String viewName, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, viewName);

      ViewDefinition viewDefinition =
          ViewDefinition.newBuilder(query).setUseLegacySql(false).build();

      bigquery.create(TableInfo.of(tableId, viewDefinition));
      System.out.println("View created successfully");
    } catch (BigQueryException e) {
      System.out.println("View was not created. \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library and create a client
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function createView() {
  // Creates a new view named "my_shared_view" in "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const myDatasetId = "my_table"
  // const myTableId = "my_table"
  // const projectId = "bigquery-public-data";
  // const sourceDatasetId = "usa_names"
  // const sourceTableId = "usa_1910_current";
  const myDataset = await bigquery.dataset(myDatasetId);

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
  const options = {
    view: `SELECT name 
    FROM \`${projectId}.${sourceDatasetId}.${sourceTableId}\`
    LIMIT 10`,
  };

  // Create a new view in the dataset
  const [view] = await myDataset.createTable(myTableId, options);

  console.log(`View ${view.id} created.`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

view_id = "my-project.my_dataset.my_view"
source_id = "my-project.my_dataset.my_table"
view = bigquery.Table(view_id)

# The source table in this example is created from a CSV file in Google
# Cloud Storage located at
# `gs://cloud-samples-data/bigquery/us-states/us-states.csv`. It contains
# 50 US states, while the view returns only those states with names
# starting with the letter 'W'.
view.view_query = f"SELECT name, post_abbr FROM `{source_id}` WHERE name LIKE 'W%'"

# Make an API request to create the view.
view = client.create_table(view)
print(f"Created {view.table_type}: {str(view.reference)}")
```

建立檢視區塊後，即可像查詢資料表一樣[查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)該檢視區塊。

## 查看安全性

如要控管 BigQuery 中檢視區塊的存取權，請參閱「[授權檢視區塊](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

## 後續步驟

* 如要瞭解如何建立授權檢視表，請參閱[建立授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。
* 如要瞭解如何取得檢視表中繼資料，請參閱[取得檢視表相關資訊](https://docs.cloud.google.com/bigquery/docs/view-metadata?hl=zh-tw)一文。
* 如要進一步瞭解如何管理檢視區塊，請參閱「[管理檢視區塊](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]