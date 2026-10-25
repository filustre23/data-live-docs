Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 執行查詢

BigQuery 可讓您根據用途，立即 (互動式)、批次或持續執行查詢。如要驗證 SQL 語法，並估算查詢處理的資料量，以便進一步控管成本，您可以執行[模擬測試](#dry-run)。

## 查詢作業的類型

您可以使用下列其中一種查詢工作類型[查詢 BigQuery 資料](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)：

* **[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)**。根據預設，BigQuery 會以互動式查詢工作的形式執行查詢，並盡快開始執行。
* **[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)**。批次查詢的優先順序低於互動式查詢。如果專案或預留項目已用盡所有可用的運算資源，批次查詢就更有可能排入佇列，並留在佇列中。批次查詢開始執行後，執行方式與互動式查詢相同。詳情請參閱「[查詢佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)」。
* **[持續查詢工作](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)**。這類工作會持續執行查詢，即時分析傳入 BigQuery 的資料，然後將結果寫入 BigQuery 資料表，或匯出至 Bigtable 或 Pub/Sub。您可以使用這項功能執行具時效性的工作，例如建立深入分析並立即採取行動、套用即時機器學習 (ML) 推論，以及建構事件導向的資料管道。

您可以透過下列方法執行查詢工作：

* 在 [Google Cloud 控制台](https://docs.cloud.google.com/bigquery/bigquery-web-ui?hl=zh-tw#overview)中編寫及執行查詢。
* 在 [bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)中執行 `bq query` 指令。
* 透過程式輔助方式呼叫 BigQuery [REST API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2?hl=zh-tw) 中的 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/query?hl=zh-tw) 或 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/insert?hl=zh-tw) 方法。
* 使用 BigQuery [用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)。

BigQuery 會將查詢結果儲存至[臨時資料表 (預設) 或永久資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#temporary_and_permanent_tables)。將永久資料表指定為結果的目的地資料表時，您可以選擇要附加或覆寫現有資料表，或建立名稱不重複的新資料表。

**注意：** 如果您從某項專案查詢儲存在其他專案的資料，系統會向執行查詢的專案收取查詢工作費用，並向儲存資料的專案收取 BigQuery 資料儲存量費用。

## 必要的角色

如要取得執行查詢工作所需的權限，請要求管理員授予您下列 IAM 角色：

* 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)。
* 對查詢參照的所有資料表和檢視表，具備 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`) 角色。如要查詢檢視表，您也必須具備所有基礎資料表和檢視表的這項角色。如果您使用[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)或[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)，則不需要存取基礎來源資料。

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行查詢工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

必須具備下列權限，才能執行查詢工作：

* `bigquery.jobs.create`
  ，無論資料儲存於何處。
* `bigquery.tables.getData`
  。如要查詢檢視表，您也必須具備所有基礎資料表和檢視表的這項權限。如果您使用[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)或[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)，則不需要存取基礎來源資料。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 疑難排解

```
Access Denied: Project [project_id]: User does not have bigquery.jobs.create
permission in project [project_id].
```

如果主體不具備在專案中建立查詢工作的權限，就會發生這項錯誤。

**解決方法**：管理員必須授予您查詢專案的 `bigquery.jobs.create` 權限。除了存取查詢資料所需的權限外，您還必須具備這項權限。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 執行互動式查詢

如要執行互動式查詢，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「add\_box SQL 查詢」。
3. 在查詢編輯器中，輸入有效的 GoogleSQL 查詢。

   舉例來說，您可以查詢 [BigQuery 公開資料集 `usa_names`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=usa_names&%3Bpage=dataset&hl=zh-tw)，找出 1910 年到 2013 年之間美國最常見的姓名：

   ```
   SELECT
     name, gender,
     SUM(number) AS total
   FROM
     `bigquery-public-data.usa_names.usa_1910_2013`
   GROUP BY
     name, gender
   ORDER BY
     total DESC
   LIMIT
     10;
   ```

   或者，您也可以使用[「Reference」(參考資料) 面板](#use-reference-panel)建構新查詢。
4. 選用：如要在輸入查詢時自動顯示程式碼建議，請依序點選「Tools」(工具) >「Parser-based auto-completion」(剖析器型自動補全)。如果不需要自動完成建議，請取消選取「Parser-based auto-completion」。這也會關閉專案名稱自動填入建議。
5. 選用：如要選取其他[查詢設定](#query-settings)，請依序點選「Edit」(編輯) >「Query settings」(查詢設定)。
6. 按一下「play\_circle 執行」。

   如未指定目的地資料表，查詢工作會將輸出內容寫入暫存 (快取) 資料表。

   現在，您可以在「Query results」(查詢結果) 窗格的「Results」(結果) 分頁中，探索查詢結果。
7. 選用步驟：如要按照資料欄排序查詢結果，請點選資料名稱欄旁的 arrow\_drop\_down「Open sort menu」(開啟排序選單)，然後選取排列順序。如果排序作業的預估處理位元組數大於 0，選單頂端就會顯示位元組數。
8. 選用：如要查看查詢結果的圖表，請前往「Visualization」(圖表) 分頁。您可以放大或縮小圖表、將圖表下載為 PNG 檔案，或切換圖例顯示設定。

   在「Visualization configuration」(圖表設定) 窗格中，您可以變更圖表類型，並設定圖表的測量指標和維度。這個窗格中的欄位會預先填入初始設定，這些設定是根據查詢的目的地資料表結構定義推論而來。在同一個查詢編輯器中，後續執行查詢時會保留這項設定。

   如果是「折線圖」、「長條圖」或「散布圖」圖表，支援的維度為 `INT64`、`FLOAT64`、`NUMERIC`、`BIGNUMERIC`、`TIMESTAMP`、`DATE`、`DATETIME`、`TIME` 和 `STRING` 資料類型，支援的測量指標則為 `INT64`、`FLOAT64`、`NUMERIC` 和 `BIGNUMERIC` 資料類型。

   如果查詢結果包含 `GEOGRAPHY` 類型，則預設圖表類型為「地圖」，可讓您在[互動式地圖](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize?hl=zh-tw#bigquery_studio)上以圖表呈現結果。
9. 選用：在「JSON」分頁中，您可以查看 JSON 格式的查詢結果，其中鍵是資料欄名稱，值則是該資料欄的結果。

### bq

1. 在 Google Cloud 控制台啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 控制台底部會開啟 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已設定適用於您目前專案的值。工作階段可能要幾秒鐘的時間才能初始化。
2. 使用 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令。在以下範例中，`--use_legacy_sql=false` 旗標可讓您使用 GoogleSQL 語法。

   ```
   bq query \
       --use_legacy_sql=false \
       'QUERY'
   ```

   將 QUERY 替換為有效的 GoogleSQL 查詢。例如，查詢 [BigQuery 公開資料集 `usa_names`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=usa_names&%3Bpage=dataset&hl=zh-tw)，找出 1910 年到 2013 年之間美國最常見的姓名：

   ```
   bq query \
       --use_legacy_sql=false \
       'SELECT
         name, gender,
         SUM(number) AS total
       FROM
         `bigquery-public-data.usa_names.usa_1910_2013`
       GROUP BY
         name, gender
       ORDER BY
         total DESC
       LIMIT
         10;'
   ```

   查詢工作會將輸出內容寫入臨時 (快取) 資料表。

   您也可以指定查詢結果的目的地資料表和[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如要將結果寫入現有資料表，請加入適當的旗標，以便附加 (`--append_table=true`) 或覆寫 (`--replace=true`) 資料表。

   ```
   bq query \
       --location=LOCATION \
       --destination_table=TABLE \
       --use_legacy_sql=false \
       'QUERY'
   ```

   更改下列內容：

   * LOCATION：目的地資料表的區域或多區域，例如 `US`

     在本範例中，`usa_names` 資料集儲存在美國多區域位置。如果您為這項查詢指定目的地資料表，則包含目的地資料表的資料集也必須位於美國多區域。您無法在某個位置查詢資料集，並將結果寫入其他位置的資料表。

     您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
   * TABLE：目的地資料表的名稱，例如 `myDataset.myTable`

     如果目的地資料表是新資料表，BigQuery 會在您執行查詢時建立資料表。不過，您必須指定現有的資料集。

     如果資料表不在目前的專案中，請使用 `PROJECT_ID:DATASET.TABLE` 格式新增Google Cloud 專案 ID，例如 `myProject:myDataset.myTable`。如未指定 `--destination_table`，系統會產生查詢工作，將輸出內容寫入臨時資料表。

### Terraform

使用 [`google_bigquery_job` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_job)。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會執行查詢。您可以[查看工作詳細資料](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)，擷取查詢結果：

```
# Generate a unique job ID.
resource "random_string" "job_id" {
  lower   = true
  length  = 16
  special = false

  keepers = {
    uuid = uuid()
  }
}

# Create a query using the generated job ID.
resource "google_bigquery_job" "my_query_job" {
  job_id = random_string.job_id.id

  query {
    query = "SELECT name, SUM(number) AS total FROM `bigquery-public-data.usa_names.usa_1910_2013` GROUP BY name ORDER BY total DESC LIMIT 100;"
  }
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   每個專案只需執行這個指令一次，而且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確的值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱必須有 `.tf` 副檔名，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在進行教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   您也可以從 GitHub 複製程式碼。如果 Terraform 程式碼片段是端對端解決方案的一部分，建議您採用這種做法。
3. 請查看並修改範例參數，以便套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請視需要加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 要建立或更新的資源符合預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台的使用者介面中，前往資源頁面，確認 Terraform 已建立或更新資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

如要使用 API 執行查詢，請[插入新工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)並填入 `query` 工作設定屬性。您也可以在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，透過 `location` 屬性指定位置。

呼叫 [`getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 來輪詢結果。持續輪詢，直到 `jobComplete` 等於 `true` 為止。檢查 `errors` 清單中的錯誤與警告。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定操作說明進行操作。詳情請參閱 [BigQuery C# API 參考文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryQuery
{
    public void Query(
        string projectId = "your-project-id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        string query = @"
            SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013`
            WHERE state = 'TX'
            LIMIT 100";
        BigQueryJob job = client.CreateQueryJob(
            sql: query,
            parameters: null,
            options: new QueryOptions { UseQueryCache = false });
        // Wait for the job to complete.
        job = job.PollUntilCompleted().ThrowOnAnyError();
        // Display the results
        foreach (BigQueryRow row in client.GetQueryResults(job.Reference))
        {
            Console.WriteLine($"{row["name"]}");
        }
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
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// queryBasic demonstrates issuing a query and reading results.
func queryBasic(w io.Writer, projectID string) error {
	// projectID := "my-project-id"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	q := client.Query(
		"SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` " +
			"WHERE state = \"TX\" " +
			"LIMIT 100")
	// Location must match that of the dataset(s) referenced in the query.
	q.Location = "US"
	// Run the query and print results when the query job is completed.
	job, err := q.Run(ctx)
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
	it, err := job.Read(ctx)
	for {
		var row []bigquery.Value
		err := it.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintln(w, row)
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
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;

public class SimpleQuery {

  public static void main(String[] args) {
    // TODO(developer): Replace this query before running the sample.
    String query =
        "SELECT name, SUM(number) as total_people "
            + "FROM `bigquery-public-data.usa_names.usa_1910_2013` "
            + "WHERE state = 'TX' "
            + "GROUP BY name, state "
            + "ORDER BY total_people DESC "
            + "LIMIT 100;";
    simpleQuery(query);
  }

  public static void simpleQuery(String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Create the query job.
      QueryJobConfiguration queryConfig = QueryJobConfiguration.newBuilder(query).build();

      // Execute the query.
      TableResult result = bigquery.query(queryConfig);

      // Print the results.
      result
          .iterateAll()
          .forEach(
              row -> {
                System.out.print("name:" + row.get("name").getStringValue());
                System.out.print(", count:" + row.get("total_people").getLongValue());
                System.out.println();
              });

      System.out.println("Query ran successfully");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query did not run \n" + e.toString());
    }
  }
}
```

如要使用 Proxy 執行查詢，請參閱「[設定 Proxy](https://github.com/googleapis/google-cloud-java#configuring-a-proxy)」。

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library using default credentials
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();
async function query() {
  // Queries the U.S. given names dataset for the state of Texas.

  const query = `SELECT name
    FROM \`bigquery-public-data.usa_names.usa_1910_2013\`
    WHERE state = 'TX'
    LIMIT 100`;

  // For all options, see https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
  const options = {
    query: query,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
  };

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(options);
  console.log(`Job ${job.id} started.`);

  // Wait for the query to finish
  const [rows] = await job.getQueryResults();

  // Print the results
  console.log('Rows:');
  rows.forEach(row => console.log(row));
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定操作說明進行操作。詳情請參閱 [BigQuery PHP API 參考文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;
use Google\Cloud\Core\ExponentialBackoff;

/** Uncomment and populate these variables in your code */
// $projectId = 'The Google project ID';
// $query = 'SELECT id, view_count FROM `bigquery-public-data.stackoverflow.posts_questions`';

$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$jobConfig = $bigQuery->query($query);
$job = $bigQuery->startQuery($jobConfig);

$backoff = new ExponentialBackoff(10);
$backoff->execute(function () use ($job) {
    print('Waiting for job to complete' . PHP_EOL);
    $job->reload();
    if (!$job->isComplete()) {
        throw new Exception('Job has not yet completed', 500);
    }
});
$queryResults = $job->queryResults();

$i = 0;
foreach ($queryResults as $row) {
    printf('--- Row %s ---' . PHP_EOL, ++$i);
    foreach ($row as $column => $value) {
        printf('%s: %s' . PHP_EOL, $column, json_encode($value));
    }
}
printf('Found %s row(s)' . PHP_EOL, $i);
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

query = """
    SELECT name, SUM(number) as total_people
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE state = 'TX'
    GROUP BY name, state
    ORDER BY total_people DESC
    LIMIT 20
"""
rows = client.query_and_wait(query)  # Make an API request.

print("The query data:")
for row in rows:
    # Row values can be accessed by field name or index.
    print("name={}, count={}".format(row[0], row["total_people"]))
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定操作說明進行操作。詳情請參閱 [BigQuery Ruby API 參考文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def query
  bigquery = Google::Cloud::Bigquery.new
  sql = "SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` " \
        "WHERE state = 'TX' " \
        "LIMIT 100"

  # Location must match that of the dataset(s) referenced in the query.
  results = bigquery.query sql do |config|
    config.location = "US"
  end

  results.each do |row|
    puts row.inspect
  end
end
```

## 模擬測試

BigQuery 模擬測試會提供下列資訊：

* [隨選模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)的預估費用
* 驗證查詢
* 查詢在[運算資源模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)中處理的大約位元組數

模擬測試不會使用查詢運算單元，也不會產生費用。您可以使用模擬測試傳回的預估值，在[Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw)中計算查詢費用。

**注意：** 如果聯合查詢使用外部資料來源，即使傳回資料列，模擬測試仍可能回報資料下限為 0 位元組。這是因為從外部資料表處理的資料量，要等到實際查詢完成後才能確定。執行聯合查詢仍會產生處理這項資料的費用。**注意：** 對受資料列層級安全性遮罩的資料表進行模擬測試時，一律會傳回 0 個位元組，以防範旁路攻擊。因此無法透過模擬測試估算查詢費用。

### 執行模擬測試

如要執行模擬測試，請按照下列步驟操作：

### 控制台

1. 前往 BigQuery 頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入查詢。

   如果查詢有效，系統會自動顯示勾號和查詢將處理的資料量。如果查詢無效，則會顯示驚嘆號和錯誤訊息。

### bq

使用 `--dry_run` 旗標輸入如下的查詢。

```
bq query \
--use_legacy_sql=false \
--dry_run \
'SELECT
   COUNTRY,
   AIRPORT,
   IATA
 FROM
   `project_id`.dataset.airports
 LIMIT
   1000'
```

如果查詢有效，指令會產生下列回應：

```
Query successfully validated. Assuming the tables are not modified,
running this query will process 10918 bytes of data.
```

**注意：** 如果查詢處理的資料量較小，您可能需要將處理的位元組從 KB 轉換為 MB。MB 是 Pricing Calculator 使用的最小單位。

### API

如要使用 API 執行模擬測試，請提交查詢工作，並在 [JobConfiguration](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfiguration) 類型中將 `dryRun` 設為 `true`。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
)

// queryDryRun demonstrates issuing a dry run query to validate query structure and
// provide an estimate of the bytes scanned.
func queryDryRun(w io.Writer, projectID string) error {
	// projectID := "my-project-id"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	q := client.Query(`
	SELECT
		name,
		COUNT(*) as name_count
	FROM ` + "`bigquery-public-data.usa_names.usa_1910_2013`" + `
	WHERE state = 'WA'
	GROUP BY name`)
	q.DryRun = true
	// Location must match that of the dataset(s) referenced in the query.
	q.Location = "US"

	job, err := q.Run(ctx)
	if err != nil {
		return err
	}
	// Dry run is not asynchronous, so get the latest status and statistics.
	status := job.LastStatus()
	if err := status.Err(); err != nil {
		return err
	}
	fmt.Fprintf(w, "This query will process %d bytes\n", status.Statistics.TotalBytesProcessed)
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
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.JobStatistics;
import com.google.cloud.bigquery.QueryJobConfiguration;

// Sample to run dry query on the table
public class QueryDryRun {

  public static void runQueryDryRun() {
    String query =
        "SELECT name, COUNT(*) as name_count "
            + "FROM `bigquery-public-data.usa_names.usa_1910_2013` "
            + "WHERE state = 'WA' "
            + "GROUP BY name";
    queryDryRun(query);
  }

  public static void queryDryRun(String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query).setDryRun(true).setUseQueryCache(false).build();

      Job job = bigquery.create(JobInfo.of(queryConfig));
      JobStatistics.QueryStatistics statistics = job.getStatistics();

      System.out.println(
          "Query dry run performed successfully." + statistics.getTotalBytesProcessed());
    } catch (BigQueryException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function queryDryRun() {
  // Runs a dry query of the U.S. given names dataset for the state of Texas.

  const query = `SELECT name
    FROM \`bigquery-public-data.usa_names.usa_1910_2013\`
    WHERE state = 'TX'
    LIMIT 100`;

  // For all options, see https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
  const options = {
    query: query,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
    dryRun: true,
  };

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(options);

  // Print the status and statistics
  console.log('Status:');
  console.log(job.metadata.status);
  console.log('\nJob Statistics:');
  console.log(job.metadata.statistics);
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定操作說明進行操作。詳情請參閱 [BigQuery PHP API 參考文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/** Uncomment and populate these variables in your code */
// $projectId = 'The Google project ID';
// $query = 'SELECT id, view_count FROM `bigquery-public-data.stackoverflow.posts_questions`';

// Construct a BigQuery client object.
$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);

// Set job configs
$jobConfig = $bigQuery->query($query);
$jobConfig->useQueryCache(false);
$jobConfig->dryRun(true);

// Extract query results
$queryJob = $bigQuery->startJob($jobConfig);
$info = $queryJob->info();

printf('This query will process %s bytes' . PHP_EOL, $info['statistics']['totalBytesProcessed']);
```

### Python

將 [QueryJobConfig.dry\_run](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob_dry_run) 屬性設為 `True`。如果有提供模擬測試的查詢設定，則 [Client.query()](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_query) 一律會傳回已完成的 [QueryJob](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob)。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

# Start the query, passing in the extra configuration.
query_job = client.query(
    (
        "SELECT name, COUNT(*) as name_count "
        "FROM `bigquery-public-data.usa_names.usa_1910_2013` "
        "WHERE state = 'WA' "
        "GROUP BY name"
    ),
    job_config=job_config,
)  # Make an API request.

# A dry run query completes immediately.
print("This query will process {} bytes.".format(query_job.total_bytes_processed))
```

## 排解查詢相關問題

如要瞭解如何解決執行查詢時發生的問題，請參閱「[排解查詢問題](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw)」。

## 執行批次查詢

如要執行批次查詢，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「add\_box SQL 查詢」。
3. 在查詢編輯器中，輸入有效的 GoogleSQL 查詢。

   舉例來說，您可以查詢 [BigQuery 公開資料集 `usa_names`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=usa_names&%3Bpage=dataset&hl=zh-tw)，找出 1910 年到 2013 年之間美國最常見的姓名：

   ```
   SELECT
     name, gender,
     SUM(number) AS total
   FROM
     `bigquery-public-data.usa_names.usa_1910_2013`
   GROUP BY
     name, gender
   ORDER BY
     total DESC
   LIMIT
     10;
   ```
4. 依序點選「編輯」>「查詢設定」。
5. 在「資源管理」部分，選取「Batch」。
6. 選用：調整[查詢設定](#query-settings)。
7. 按一下 [儲存]。
8. 按一下「play\_circle 執行」。

   如未指定目的地資料表，查詢工作會將輸出內容寫入暫存 (快取) 資料表。

### bq

1. 在 Google Cloud 控制台啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 控制台底部會開啟 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已設定適用於您目前專案的值。工作階段可能要幾秒鐘的時間才能初始化。
2. 使用 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並指定 `--batch` 旗標。在以下範例中，`--use_legacy_sql=false` 旗標可讓您使用 GoogleSQL 語法。

   ```
   bq query \
       --batch \
       --use_legacy_sql=false \
       'QUERY'
   ```

   將 QUERY 替換為有效的 GoogleSQL 查詢。例如，查詢 [BigQuery 公開資料集 `usa_names`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=usa_names&%3Bpage=dataset&hl=zh-tw)，找出 1910 年到 2013 年之間美國最常見的姓名：

   ```
   bq query \
       --batch \
       --use_legacy_sql=false \
       'SELECT
         name, gender,
         SUM(number) AS total
       FROM
         `bigquery-public-data.usa_names.usa_1910_2013`
       GROUP BY
         name, gender
       ORDER BY
         total DESC
       LIMIT
         10;'
   ```

   查詢工作會將輸出內容寫入臨時 (快取) 資料表。

   您也可以指定查詢結果的目的地資料表和[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如要將結果寫入現有資料表，請加入適當的旗標，以便附加 (`--append_table=true`) 或覆寫 (`--replace=true`) 資料表。

   ```
   bq query \
       --batch \
       --location=LOCATION \
       --destination_table=TABLE \
       --use_legacy_sql=false \
       'QUERY'
   ```

   更改下列內容：

   * LOCATION：目的地資料表的區域或多區域，例如 `US`

     在本範例中，`usa_names` 資料集儲存在美國多區域位置。如果您為這項查詢指定目的地資料表，則包含目的地資料表的資料集也必須位於美國多區域。您無法在某個位置查詢資料集，並將結果寫入其他位置的資料表。

     您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
   * TABLE：目的地資料表的名稱，例如 `myDataset.myTable`

     如果目的地資料表是新資料表，BigQuery 會在您執行查詢時建立資料表。不過，您必須指定現有的資料集。

     如果資料表不在目前的專案中，請使用 `PROJECT_ID:DATASET.TABLE` 格式新增Google Cloud 專案 ID，例如 `myProject:myDataset.myTable`。如未指定 `--destination_table`，系統會產生查詢工作，將輸出內容寫入臨時資料表。

### API

如要使用 API 執行查詢，請[插入新工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)並填入 `query` 工作設定屬性。您也可以在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，透過 `location` 屬性指定位置。

填入查詢工作屬性時，請加入 `configuration.query.priority` 屬性，並將值設為 `BATCH`。

呼叫 [`getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 來輪詢結果。持續輪詢，直到 `jobComplete` 等於 `true` 為止。檢查 `errors` 清單中的錯誤與警告。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"
	"time"

	"cloud.google.com/go/bigquery"
)

// queryBatch demonstrates issuing a query job using batch priority.
func queryBatch(w io.Writer, projectID, dstDatasetID, dstTableID string) error {
	// projectID := "my-project-id"
	// dstDatasetID := "mydataset"
	// dstTableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	// Build an aggregate table.
	q := client.Query(`
		SELECT
  			corpus,
  			SUM(word_count) as total_words,
  			COUNT(1) as unique_words
		FROM ` + "`bigquery-public-data.samples.shakespeare`" + `
		GROUP BY corpus;`)
	q.Priority = bigquery.BatchPriority
	q.QueryConfig.Dst = client.Dataset(dstDatasetID).Table(dstTableID)

	// Start the job.
	job, err := q.Run(ctx)
	if err != nil {
		return err
	}
	// Job is started and will progress without interaction.
	// To simulate other work being done, sleep a few seconds.
	time.Sleep(5 * time.Second)
	status, err := job.Status(ctx)
	if err != nil {
		return err
	}

	state := "Unknown"
	switch status.State {
	case bigquery.Pending:
		state = "Pending"
	case bigquery.Running:
		state = "Running"
	case bigquery.Done:
		state = "Done"
	}
	// You can continue to monitor job progress until it reaches
	// the Done state by polling periodically.  In this example,
	// we print the latest status.
	fmt.Fprintf(w, "Job %s in Location %s currently in state: %s\n", job.ID(), job.Location(), state)

	return nil

}
```

### Java

如要執行批次查詢，請[將查詢優先順序設定](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration.Builder?hl=zh-tw#com_google_cloud_bigquery_QueryJobConfiguration_Builder_setPriority_com_google_cloud_bigquery_QueryJobConfiguration_Priority_)為 [QueryJobConfiguration.Priority.BATCH](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration.Priority?hl=zh-tw#staticFields) (當建立 [QueryJobConfiguration](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration?hl=zh-tw) 時)。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;

// Sample to query batch in a table
public class QueryBatch {

  public static void runQueryBatch() {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String query =
        "SELECT corpus"
            + " FROM `"
            + projectId
            + "."
            + datasetName
            + "."
            + tableName
            + " GROUP BY corpus;";
    queryBatch(query);
  }

  public static void queryBatch(String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              // Run at batch priority, which won't count toward concurrent rate limit.
              .setPriority(QueryJobConfiguration.Priority.BATCH)
              .build();

      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query batch performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query batch not performed \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library and create a client
const
```