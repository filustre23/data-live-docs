Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理資料表

這份文件說明如何在 BigQuery 中管理資料表。
您可透過下列方式管理 BigQuery 資料表：

* [更新資料表屬性](#updating_table_properties)：
  + [到期時間](#updating_a_tables_expiration_time)
  + [說明](#updating_a_tables_description)
  + [結構定義](#updating_a_tables_schema_definition)
  + [標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#adding_table_and_view_labels)
  + [預設捨入模式](#update_rounding_mode)
* [重新命名 (複製) 資料表](#renaming-table)
* [複製表格](#copy-table)
* [刪除表格](#deleting_tables)

如要瞭解如何還原 (或*取消刪除*) 已刪除的資料表，請參閱「[還原已刪除的資料表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw)」。

如要進一步瞭解如何建立及使用資料表，包括取得資料表資訊、列出資料表及控管資料表資料存取權等，請參閱[建立與使用資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。執行工作所需的權限 (如有) 會列在工作的「必要權限」部分。

## 更新資料表屬性

您可以更新資料表的下列元素：

* [說明](#updating_a_tables_description)
* [到期時間](#updating_a_tables_expiration_time)
* [結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)
* [標籤](https://docs.cloud.google.com/bigquery/docs/labels?hl=zh-tw#creating_or_updating_a_table_or_view_label)
* [資料表名稱](#renaming-table)
* [標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)

### 所需權限

如要取得更新資料表屬性所需的權限，請要求管理員授予您資料表的[資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備更新表格屬性所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要更新資料表屬性，您必須具備下列權限：

* `bigquery.tables.update`
* `bigquery.tables.get`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

此外，如果您具備 `bigquery.datasets.create` 權限，可以更新所建立資料集的資料表屬性。

### 更新資料表的說明

您可以透過下列方式更新資料表的說明：

* 使用 Google Cloud 控制台。
* 使用資料定義語言 (DDL) `ALTER TABLE` 陳述式。
* 使用 bq 指令列工具的 `bq update` 指令。
* 呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API 方法
* 使用用戶端程式庫。
* 使用 Gemini in BigQuery 產生說明。

如何更新資料表的說明：

### 控制台

使用Google Cloud 主控台建立資料表時，無法新增說明。資料表建立完畢之後，您就可以在「Details」(詳細資料) 頁面中新增說明。

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
3. 依序點選「總覽」**>「表格」**，然後選取所需表格。
4. 按一下「詳細資料」分頁標籤，然後點選「編輯詳細資料」。
5. 在「說明」部分新增或編輯說明。
6. 按一下 [儲存]。

### SQL

使用 [`ALTER TABLE SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)。以下範例會更新名為 `mytable` 的資料表說明：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mytable
     SET OPTIONS (
       description = 'Description of mytable');
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 發出含有 `--description` 旗標的 `bq update` 指令。如果您要更新非預設專案中的資料表，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

   ```
   bq update \
   --description "description" \
   project_id:dataset.table
   ```

   更改下列內容：

   * `description`：置於引號中的資料表說明
   * `project_id`：專案 ID
   * `dataset`：含有您要更新資料表的資料集名稱
   * `table`：要更新的資料表名稱

   範例：

   如要將 `mydataset` 資料集中的 `mytable` 資料表說明變更為「Description of mytable」，請輸入下列指令。`mydataset` 資料集位於預設專案中。

   ```
   bq update --description "Description of mytable" mydataset.mytable
   ```

   如要將 `mydataset` 資料集中的 `mytable` 資料表說明變更為「Description of mytable」，請輸入下列指令。`mydataset` 資料集位於 `myotherproject` 專案，而非預設專案。

   ```
   bq update \
   --description "Description of mytable" \
   myotherproject:mydataset.mytable
   ```

### API

呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法，並使用[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)中的 `description` 屬性來更新資料表的說明。由於 `tables.update` 方法會取代整個資料表資源，因此建議使用 `tables.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// updateTableDescription demonstrates how to fetch a table's metadata and updates the Description metadata.
func updateTableDescription(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	tableRef := client.Dataset(datasetID).Table(tableID)
	meta, err := tableRef.Metadata(ctx)
	if err != nil {
		return err
	}
	update := bigquery.TableMetadataToUpdate{
		Description: "Updated description.",
	}
	if _, err = tableRef.Update(ctx, update, meta.ETag); err != nil {
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
import com.google.cloud.bigquery.Table;

public class UpdateTableDescription {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String newDescription = "this is the new table description";
    updateTableDescription(datasetName, tableName, newDescription);
  }

  public static void updateTableDescription(
      String datasetName, String tableName, String newDescription) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Table table = bigquery.getTable(datasetName, tableName);
      bigquery.update(table.toBuilder().setDescription(newDescription).build());
      System.out.println("Table description updated successfully to " + newDescription);
    } catch (BigQueryException e) {
      System.out.println("Table description was not updated \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

設定 [Table.description](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.Table?hl=zh-tw#google_cloud_bigquery_table_Table_description) 屬性並呼叫 [Client.update\_table()](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_update_table)，將更新傳送至 API。

```
# from google.cloud import bigquery
# client = bigquery.Client()
# project = client.project
# dataset_ref = bigquery.DatasetReference(project, dataset_id)
# table_ref = dataset_ref.table('my_table')
# table = client.get_table(table_ref)  # API request

assert table.description == "Original description."
table.description = "Updated description."

table = client.update_table(table, ["description"])  # API request

assert table.description == "Updated description."
```

### Gemini

您可以使用資料洞察，透過 Gemini in BigQuery 生成資料表說明。資料洞察功能可自動探索、解讀及管理資料。

如要進一步瞭解資料洞察，包括設定步驟、必要 IAM 角色，以及提升所產生洞察準確度的最佳做法，請參閱「[在 BigQuery 中產生資料洞察](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)」。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，展開專案和資料集，然後選取資料表。
4. 在詳細資料面板中，按一下「結構定義」分頁標籤。
5. 點按「生成」。

   **注意：** 如果沒有看到「產生」按鈕，請點選「描述資料」。你可能需要捲動畫面才能看到這個按鈕。

   Gemini 會生成資料表說明和資料表洞察結果。系統需要幾分鐘才能填入資訊。您可以在表格的「洞察」分頁中查看生成的洞察資料。
6. 如要編輯及儲存系統產生的表格說明，請按照下列步驟操作：

   1. 按一下「查看資料欄說明」。

      系統會顯示目前的資料表說明和生成的說明。
   2. 在「資料表說明」部分，按一下「儲存至詳細資料」。
   3. 如要以生成的說明取代目前的說明，請按一下「複製建議的說明」。
   4. 視需要編輯表格說明，然後按一下「儲存至詳細資料」。

      系統會立即更新資料表說明。
   5. 如要關閉「預覽說明」面板，請按一下「關閉」close。

### 更新資料表的到期時間

您可以設定資料集層級的預設資料表到期時間，也可以在建立資料表時設定資料表的到期時間。資料表的到期時間通常稱為「存留時間」或 TTL。

資料表過期後，系統會一併刪除資料表和其中的所有資料。
如有需要，您可以在資料集指定的時間旅行視窗內取消刪除過期的資料表，詳情請參閱「[還原已刪除的資料表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw)」。

如果您在建立資料表時設定了到期時間，系統將會忽略資料集的資料表預設到期時間。如果您未在資料集層級設定資料表的預設到期時間，也未在建立資料表時設定到期時間，則資料表將永遠不會過期，您必須以手動方式才能[刪除](#deleting_a_table)。

建立資料表後，您可以隨時透過以下方式更新資料表的到期時間：

* 使用 Google Cloud 控制台。
* 使用資料定義語言 (DDL) `ALTER TABLE` 陳述式。
* 使用 bq 指令列工具的 `bq update` 指令。
* 呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API 方法
* 使用用戶端程式庫。

**附註：** 如果設定的到期時間已過，系統會立即刪除該資料表。

如何更新資料表的到期時間：

### 控制台

使用Google Cloud 主控台建立資料表時，您無法新增到期時間。建立資料表後，您可以在「Table Details」(資料表詳細資料) 頁面上新增或更新資料表的到期時間。

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
3. 依序點選「總覽」**>「表格」**，然後選取所需表格。
4. 按一下「詳細資料」分頁標籤，然後按一下「編輯詳細資料」。
5. 針對「Expiration time」(到期時間)，選取「Specify date」(指定日期)。然後使用日曆小工具選取到期日。
6. 按一下 [儲存]。已更新的到期時間會顯示在「Table info」(資料表資訊) 區段。

### SQL

使用 [`ALTER TABLE SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)。以下範例會更新名為 `mytable` 的資料表到期時間：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mytable
     SET OPTIONS (
       -- Sets table expiration to timestamp 2025-02-03 12:34:56
       expiration_timestamp = TIMESTAMP '2025-02-03 12:34:56');
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 發出含有 `--expiration` 旗標的 `bq update` 指令。如果您要更新非預設專案中的資料表，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

   ```
   bq update \
   --expiration integer \
   project_id:dataset.table
   ```

   更改下列內容：

   * `integer`：資料表的預設生命週期 (以秒為單位)，最小值是 3600 秒 (1 小時)。到期時間為目前時間加整數值。如果您指定 `0`，系統就會移除資料表到期時間，讓這個資料表永遠不會過期。沒有到期時間的資料表都必須手動刪除。
   * `project_id`：您的專案 ID。
   * `dataset`：含有您要更新資料表的資料集名稱。
   * `table`：要更新的資料表名稱。

   範例：

   如要將 `mydataset` 資料集中的 `mytable` 資料表到期時間更新為 5 天 (432000 秒)，請輸入下列指令。`mydataset` 資料集位於預設專案中。

   ```
   bq update --expiration 432000 mydataset.mytable
   ```

   如要將 `mydataset` 資料集中的 `mytable` 資料表到期時間更新為 5 天 (432000 秒)，請輸入下列指令。`mydataset` 資料集位於 `myotherproject` 專案，而非預設專案。

   ```
   bq update --expiration 432000 myotherproject:mydataset.mytable
   ```

### API

呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法並使用[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)中的 `expirationTime` 屬性更新資料表的到期時間 (以毫秒為單位)。由於 `tables.update` 方法會取代整個資料表資源，因此建議使用 `tables.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
)

// updateTableExpiration demonstrates setting the table expiration of a table to a specific point in time
// in the future, at which time it will be deleted.
func updateTableExpiration(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	tableRef := client.Dataset(datasetID).Table(tableID)
	meta, err := tableRef.Metadata(ctx)
	if err != nil {
		return err
	}
	update := bigquery.TableMetadataToUpdate{
		ExpirationTime: time.Now().Add(time.Duration(5*24) * time.Hour), // table expiration in 5 days.
	}
	if _, err = tableRef.Update(ctx, update, meta.ETag); err != nil {
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
import com.google.cloud.bigquery.Table;
import java.util.concurrent.TimeUnit;

public class UpdateTableExpiration {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    // Update table expiration to one day.
    Long newExpiration =
        TimeUnit.MILLISECONDS.convert(1, TimeUnit.DAYS) + System.currentTimeMillis();
    updateTableExpiration(datasetName, tableName, newExpiration);
  }

  public static void updateTableExpiration(
      String datasetName, String tableName, Long newExpiration) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Table table = bigquery.getTable(datasetName, tableName);
      bigquery.update(table.toBuilder().setExpirationTime(newExpiration).build());

      System.out.println("Table expiration updated successfully to " + newExpiration);
    } catch (BigQueryException e) {
      System.out.println("Table expiration was not updated \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function updateTableExpiration() {
  // Updates a table's expiration.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset', // Existing dataset
  // const tableId = 'my_table', // Existing table
  // const expirationTime = Date.now() + 1000 * 60 * 60 * 24 * 5 // 5 days from current time in ms

  // Retreive current table metadata
  const table = bigquery.dataset(datasetId).table(tableId);
  const [metadata] = await table.getMetadata();

  // Set new table expiration to 5 days from current time
  metadata.expirationTime = expirationTime.toString();
  const [apiResponse] = await table.setMetadata(metadata);

  const newExpirationTime = apiResponse.expirationTime;
  console.log(`${tableId} expiration: ${newExpirationTime}`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

設定 [Table.expires](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.Table?hl=zh-tw#google_cloud_bigquery_table_Table_expires) 屬性並呼叫 [Client.update\_table()](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_update_table)，將更新傳送至 API。

```
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime


def update_table_expiration(table_id, expiration):
    orig_table_id = table_id
    orig_expiration = expiration

    from google.cloud import bigquery

    client = bigquery.Client()

    # TODO(dev): Change table_id to the full name of the table you want to update.
    table_id = "your-project.your_dataset.your_table_name"

    # TODO(dev): Set table to expire for desired days days from now.
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=5
    )

    table_id = orig_table_id
    expiration = orig_expiration

    table = client.get_table(table_id)  # Make an API request.
    table.expires = expiration
    table = client.update_table(table, ["expires"])  # API request

    print(f"Updated {table_id}, expires {table.expires}.")
```

如要更新資料集的預設分區到期時間：

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import java.util.concurrent.TimeUnit;

// Sample to update partition expiration on a dataset.
public class UpdateDatasetPartitionExpiration {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    // Set the default partition expiration (applies to new tables, only) in
    // milliseconds. This example sets the default expiration to 90 days.
    Long newExpiration = TimeUnit.MILLISECONDS.convert(90, TimeUnit.DAYS);
    updateDatasetPartitionExpiration(datasetName, newExpiration);
  }

  public static void updateDatasetPartitionExpiration(String datasetName, Long newExpiration) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Dataset dataset = bigquery.getDataset(datasetName);
      bigquery.update(dataset.toBuilder().setDefaultPartitionExpirationMs(newExpiration).build());
      System.out.println(
          "Dataset default partition expiration updated successfully to " + newExpiration);
    } catch (BigQueryException e) {
      System.out.println("Dataset partition expiration was not updated \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def update_dataset_default_partition_expiration(dataset_id: str) -> None:

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset to fetch.
    # dataset_id = 'your-project.your_dataset'

    dataset = client.get_dataset(dataset_id)  # Make an API request.

    # Set the default partition expiration (applies to new tables, only) in
    # milliseconds. This example sets the default expiration to 90 days.
    dataset.default_partition_expiration_ms = 90 * 24 * 60 * 60 * 1000

    dataset = client.update_dataset(
        dataset, ["default_partition_expiration_ms"]
    )  # Make an API request.

    print(
        "Updated dataset {}.{} with new default partition expiration {}".format(
            dataset.project, dataset.dataset_id, dataset.default_partition_expiration_ms
        )
    )
```

### 更新資料表的捨入模式

您可以使用 [`ALTER TABLE SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)，更新資料表的[預設捨入模式](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#Table.FIELDS.default_rounding_mode)。以下範例會將 `mytable` 的預設捨去模式更新為 `ROUND_HALF_EVEN`：

```
ALTER TABLE mydataset.mytable
SET OPTIONS (
  default_rounding_mode = "ROUND_HALF_EVEN");
```

在表格中新增 `NUMERIC` 或 `BIGNUMERIC` 欄位時，如果沒有指定[捨入模式](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#rounding_mode)，系統會自動將捨入模式設為表格的預設捨入模式。變更資料表的預設捨入模式不會影響現有欄位的捨入模式。

### 更新資料表的結構定義

如要進一步瞭解如何更新資料表結構定義，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。

### 重新命名資料表

資料表建立後，您可以使用 [`ALTER TABLE RENAME TO` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_rename_to_statement)重新命名。以下範例會將 `mytable` 重新命名為 `mynewtable`：

```
ALTER TABLE mydataset.mytable
RENAME TO mynewtable;
```

`ALTER TABLE RENAME TO` 陳述式會在目的地資料集中重新建立資料表，並使用原始資料表的建立時間戳記。如果您已設定[資料集層級的資料表到期時間](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#table-expiration)，如果重新命名的資料表原始建立時間戳記超出到期時間範圍，系統可能會立即刪除該資料表。

#### 重新命名資料表的限制

* 如要重新命名正在串流資料的表格，請停止串流、提交所有待處理的串流，並等待 BigQuery 指出串流未在使用中。
* 通常在上次串流作業的 5 小時後，即可重新命名表格，但有時可能需要較長時間。
* 系統會保留現有的資料表 ACL 和資料列存取政策，但不會保留在資料表重新命名期間所做的資料表 ACL 和資料列存取政策更新。
* 您無法同時重新命名資料表，並對該資料表執行 DML 陳述式。
* 重新命名資料表會移除資料表中的所有[Data Catalog 標記](https://docs.cloud.google.com/data-catalog/docs/tags-and-tag-templates?hl=zh-tw) (已淘汰) 和[Knowledge Catalog 層面](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw#aspects)。
* 重新命名資料表時，系統會捨棄在該資料表上建立的任何搜尋索引或向量索引。
* 您無法重新命名外部資料表。

## 複製資料表

本節說明如何建立資料表的完整副本。如要瞭解其他類型的資料表副本，請參閱[資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)和[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。

您可以透過下列方式複製資料表：

* 使用 Google Cloud 控制台。
* 使用 [`bq cp`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 指令。
* 使用資料定義語言 (DDL) [`CREATE TABLE COPY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_copy) 陳述式。
* 呼叫 [jobs.insert](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 方法並設定 `copy` 工作。
* 使用用戶端程式庫。

### 複製資料表的限制

資料表複製工作有下列限制：

* 表格複製作業開始後就無法停止。資料表複製作業會非同步執行，即使取消工作也不會停止。跨區域複製資料表時，您也需要支付資料移轉費用，以及目標區域的儲存空間費用。
* 當您複製資料表時，目的地資料表的名稱必須遵循您[建立資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create-table)時所使用的命名慣例。
* 資料表複製必須遵循 BigQuery 有關複製工作的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)。
* Google Cloud 主控台一次只能複製一個資料表。您無法覆寫目的地資料集中的現有資料表。目的地資料集中的資料表名稱不得重複。
* Google Cloud 控制台不支援將多個來源資料表複製到目的地資料表。
* 使用 API、bq 指令列工具或用戶端程式庫複製多個來源資料表到目的地資料表時，所有來源資料表都必須具有相同的結構定義，包括任何分區或分群。

  某些資料表結構定義更新 (例如捨棄或重新命名資料欄)，可能會導致資料表具有看似相同的結構定義，但內部表示法不同。這可能會導致資料表複製工作失敗，並出現 `Maximum limit on diverging physical schemas reached` 錯誤。在這種情況下，您可以使用 [`CREATE TABLE LIKE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_like)，確保來源資料表的結構定義與目的地資料表的結構定義完全一致。
* 由於基礎儲存空間是動態管理，因此 BigQuery 複製資料表所需的時間可能會因不同執行作業而有顯著差異。
* 如果目的地資料表的資料欄數多於來源資料表，且額外資料欄有[預設值](https://docs.cloud.google.com/bigquery/docs/default-values?hl=zh-tw)，您就無法複製來源資料表並附加至目的地資料表。您可以改為執行 `INSERT destination_table SELECT * FROM source_table` 來複製資料。
* 如果複製作業覆寫現有資料表，系統會保留現有資料表的資料表層級存取權。來源資料表的[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)不會複製到覆寫的資料表，但現有資料表的標記會保留。不過，跨區域複製資料表時，現有資料表中的標記會遭到移除。
* 如果複製作業會建立新資料表，新資料表的資料表層級存取權，取決於新資料表所在資料集的存取權政策。此外，系統也會將[標籤](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)從來源資料表複製到新資料表。
* 將多個來源資料表複製到目的地資料表時，所有來源資料表都必須具有相同的標記。

### 必要的角色

如要執行本文中的工作，您需要下列權限。

#### 複製資料表和分區的角色

如要取得複製資料表和分區所需的權限，請要求管理員授予您來源和目的地資料集的[資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備複製資料表和資料分割所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要複製資料表和分區，必須具備下列權限：

* `bigquery.tables.getData`
  來源和目的地資料集
* `bigquery.tables.get`
  來源和目的地資料集
* `bigquery.tables.create`
  目的地資料集
* `bigquery.tables.update`
  目的地資料集

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

#### 執行複製作業的權限

如要取得執行複製工作所需的權限，請要求管理員授予您來源和目的地資料集的「[工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser) 」(`roles/bigquery.jobUser`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.jobs.create` 權限，可執行複製工作。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

### 複製單一來源資料表

您可以透過以下方式複製單一資料表：

* 使用 Google Cloud 控制台。
* 使用 bq 指令列工具的 `bq cp` 指令。
* 使用資料定義語言 (DDL) `CREATE TABLE COPY` 陳述式。
* 呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 方法、設定 `copy` 工作，然後指定 `sourceTable` 屬性。
* 使用用戶端程式庫。

Google Cloud 控制台和 `CREATE TABLE COPY` 陳述式在複製工作中，都只支援一個來源資料表和一個目的地資料表。如要[將多個來源檔案複製](#copying_multiple_source_tables)到目的地資料表，請使用 bq 指令列工具或 API。

如要複製單一來源資料表：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
3. 依序點選「總覽」**>「表格」**，然後選取所需表格。
4. 在詳細資料窗格中，按一下「複製」。
5. 在「Copy table」(複製資料表) 對話方塊中的「Destination」(目的地) 下方：

   * 在「Project」(專案) 部分，選擇將用來儲存複製資料表的專案。
   * 針對「Dataset」(資料集)，選取您要用來儲存複製資料表的資料集。來源與目的地資料集必須位於相同的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * 針對「Table」(資料表)，輸入新資料表的名稱。目標資料集中的資料表名稱不得重複。您無法使用 Google Cloud 控制台覆寫目的地資料集中現有的資料表。如要進一步瞭解資料表名稱規定，請參閱「[資料表命名](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#table_naming)」。
6. 按一下 [Copy] (複製) 即可開始複製工作。

### SQL

使用 [`CREATE TABLE COPY` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_copy)，將名為 `table1` 的資料表複製到名為 `table1copy` 的新資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE myproject.mydataset.table1copy
   COPY myproject.mydataset.table1;
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 請發出 `bq cp` 指令。選用標記可用來控管目的地資料表的寫入配置：

   * `-a` 或 `--append_table`：把來源資料表的資料附加到目的地資料集中現有的資料表上。
   * `-f` 或 `--force`：覆寫目的地資料集中的現有資料表，此作業不會有確認提示。
   * 如果目的地資料集裡已有資料表，`-n` 或 `--no_clobber` 會傳回下列錯誤訊息：`Table 'project_id:dataset.table' already exists, skipping.`。如未指定 `-n`，預設行為是提示您選擇是否要取代目的地資料表。
   * `--destination_kms_key`：由客戶管理的 Cloud KMS 金鑰，可用來為目的地資料表加密。

   本文不示範 `--destination_kms_key`。詳情請參閱[使用 Cloud Key Management Service 金鑰保護資料](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。

   如果來源或目的地資料集位於非預設專案中，請採用下列格式將專案 ID 新增至該資料集名稱：`project_id:dataset`。

   (選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

   ```
   bq --location=location cp \
   -a -f -n \
   project_id:dataset.source_table \
   project_id:dataset.destination_table
   ```

   更改下列內容：

   * `location`：位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)，設定該位置的預設值。
   * `project_id`：您的專案 ID。
   * `dataset`：來源或目的地資料集的名稱。
   * `source_table`：要複製的資料表。
   * `destination_table`：目的地資料集中的資料表名稱。

   範例：

   如要將 `mydataset.mytable` 資料表複製到 `mydataset2.mytable2` 資料表，請輸入下列指令。這兩個資料集都在預設專案中。

   ```
   bq cp mydataset.mytable mydataset2.mytable2
   ```

   如要複製 `mydataset.mytable` 資料表，並覆寫有相同名稱的目的地資料表，請輸入下列指令。來源資料集位於預設專案中。目的地資料集位於 `myotherproject` 專案中。`-f` 捷徑可用來在無提示的情況下覆寫目的地資料表。

   ```
   bq cp -f \
   mydataset.mytable \
   myotherproject:myotherdataset.mytable
   ```

   如要複製 `mydataset.mytable` 資料表，並在目的地資料集有相同名稱的資料表時傳回錯誤，請輸入下列指令。來源資料集位於預設專案中。目的地資料集位於 `myotherproject` 專案中。`-n` 捷徑用於防止名稱相同的資料表遭到覆寫。

   ```
   bq cp -n \
   mydataset.mytable \
   myotherproject:myotherdataset.mytable
   ```

   如要複製 `mydataset.mytable` 資料表，並將資料附加到有相同名稱的目的地資料表，請輸入下列指令。來源資料集位於預設專案中。目的地資料集位於 `myotherproject` 專案中。`- a` 捷徑是用來附加到目的地資料表。

   ```
   bq cp -a mydataset.mytable myotherproject:myotherdataset.mytable
   ```

### API

您可以呼叫 [`bigquery.jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法並設定 `copy` 工作，透過 API 複製現有資料表。在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，於 `location` 屬性指定您的位置。

您必須在工作設定中指定下列值：

```
"copy": {
      "sourceTable": {       // Required
        "projectId": string, // Required
        "datasetId": string, // Required
        "tableId": string    // Required
      },
      "destinationTable": {  // Required
        "projectId": string, // Required
        "datasetId": string, // Required
        "tableId": string    // Required
      },
      "createDisposition": string,  // Optional
      "writeDisposition": string,   // Optional
    },
```

其中 `sourceTable` 提供要複製的資料表相關資訊，`destinationTable` 提供新資料表相關資訊，`createDisposition` 指定資料表不存在時是否建立資料表，而 `writeDisposition` 則指定是否覆寫或附加至現有資料表。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Apis.Bigquery.v2.Data;
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryCopyTable
{
    public void CopyTable(
        string projectId = "your-project-id",
        string destinationDatasetId = "your_dataset_id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        TableReference sourceTableRef = new TableReference()
        {
            TableId = "shakespeare",
            DatasetId = "samples",
            ProjectId = "bigquery-public-data"
        };
        TableReference destinationTableRef = client.GetTableReference(
            destinationDatasetId, "destination_table");
        BigQueryJob job = client.CreateCopyJob(
            sourceTableRef, destinationTableRef)
            .PollUntilCompleted() // Wait for the job to complete.
            .ThrowOnAnyError();

        // Retrieve destination table
        BigQueryTable destinationTable = client.GetTable(destinationTableRef);
        Console.WriteLine(
            $"Copied {destinationTable.Resource.NumRows} rows from table "
            + $"{sourceTableRef.DatasetId}.{sourceTableRef.TableId} "
            + $"to {destinationTable.FullyQualifiedId}."
        );
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// copyTable demonstrates copying a table from a source to a destination, and
// allowing the copy to overwrite existing data by using truncation.
func copyTable(projectID, datasetID, srcID, dstID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// srcID := "sourcetable"
	// dstID := "destinationtable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	dataset := client.Dataset(datasetID)
	copier := dataset.Table(dstID).CopierFrom(dataset.Table(srcID))
	copier.WriteDisposition = bigquery.WriteTruncate
	job, err := copier.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}
	if err := status.Err(); err != nil {
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
import com.google.cloud.bigquery.CopyJobConfiguration;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.TableId;

public class CopyTable {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String destinationDatasetName = "MY_DESTINATION_DATASET_NAME";
    String destinationTableId = "MY_DESTINATION_TABLE_NAME";
    String sourceDatasetName = "MY_SOURCE_DATASET_NAME";
    String sourceTableId = "MY_SOURCE_TABLE_NAME";

    copyTable(sourceDatasetName, sourceTableId, destinationDatasetName, destinationTableId);
  }

  public static void copyTable(
      String sourceDatasetName,
      String sourceTableId,
      String destinationDatasetName,
      String destinationTableId) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId sourceTable = TableId.of(sourceDatasetName, sourceTableId);
      TableId destinationTable = TableId.of(destinationDatasetName, destinationTableId);

      // For more information on CopyJobConfiguration see:
      // https://googleapis.dev/java/google-cloud-clients/latest/com/google/cloud/bigquery/JobConfiguration.html
      CopyJobConfiguration configuration =
          CopyJobConfiguration.newBuilder(destinationTable, sourceTable).build();

      // For more information on Job see:
      // https://googleapis.dev/java/google-cloud-clients/latest/index.html?com/google/cloud/bigquery/package-summary.html
      Job job = bigquery.create(JobInfo.of(configuration));

      // Blocks until this job completes its execution, either failing or succeeding.
      Job completedJob = job.waitFor();
      if (completedJob == null) {
        System.out.println("Job not executed since it no longer exists.");
        return;
      } else if (completedJob.getStatus().getError() != null) {
        System.out.println(
            "BigQuery was unable to copy table due to an error: \n" + job.getStatus().getError());
        return;
      }
      System.out.println("Table copied successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Table copying job was interrupted. \n" + e.toString());
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

async function copyTable() {
  // Copies src_dataset:src_table to dest_dataset:dest_table.

  /**
   * TODO(developer): Uncomment the following lines before running the sample
   */
  // const srcDatasetId = "my_src_dataset";
  // const srcTableId = "my_src_table";
  // const destDatasetId = "my_dest_dataset";
  // const destTableId = "my_dest_table";

  // Copy the table contents into another table
  const [job] = await bigquery
    .dataset(srcDatasetId)
    .table(srcTableId)
    .copy(bigquery.dataset(destDatasetId).table(destTableId));

  console.log(`Job ${job.id} completed.`);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;
use Google\Cloud\Core\ExponentialBackoff;

/** Uncomment and populate these variables in your code */
// $projectId = 'The Google project ID';
// $datasetId = 'The BigQuery dataset ID';
// $sourceTableId   = 'The BigQuery table ID to copy from';
// $destinationTableId = 'The BigQuery table ID to copy to';

$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$dataset = $bigQuery->dataset($datasetId);
$sourceTable = $dataset->table($sourceTableId);
$destinationTable = $dataset->table($destinationTableId);
$copyConfig = $sourceTable->copy($destinationTable);
$job = $sourceTable->runJob($copyConfig);

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
    print('Table copied successfully' . PHP_EOL);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set source_table_id to the ID of the original table.
# source_table_id = "your-project.source_dataset.source_table"

# TODO(developer): Set destination_table_id to the ID of the destination table.
# destination_table_id = "your-project.destination_dataset.destination_table"

job = client.copy_table(source_table_id, destination_table_id)
job.result()  # Wait for the job to complete.

print("A copy of the table created.")
```

### 複製多個來源資料表

您可以透過下列方式，將多個來源資料表複製到目的地資料表：

* 使用 bq 指令列工具的 `bq cp` 指令。
* 呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法、設定 `copy` 工作，然後指定 `sourceTables` 屬性。
* 使用用戶端程式庫。

所有來源資料表都必須擁有相同的結構定義和[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)，且只能有一個目的地資料表。

來源資料表必須指定為逗號分隔的清單。複製多個來源資料表時，無法使用萬用字元。

如要複製多個來源資料表，請選取下列其中一個選項：

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 發出 `bq cp` 指令，並以逗號分隔清單的形式包含多個來源資料表。
   選用標記可用來控管目的地資料