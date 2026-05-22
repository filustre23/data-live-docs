Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 執行查詢

本文說明如何在 BigQuery 中執行查詢，以及如何透過[模擬測試](#dry-run)，瞭解查詢執行前會處理多少資料。

## 查詢作業的類型

您可以使用下列其中一種查詢工作類型[查詢 BigQuery 資料](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)：

* **[互動式查詢作業](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)**。根據預設，BigQuery 會以互動式查詢工作執行查詢，這類工作會盡快開始執行。
* **[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)**。批次查詢的優先順序低於互動式查詢。如果專案或預訂項目已用盡所有可用的運算資源，批次查詢就更有可能排入佇列，並留在佇列中。批次查詢開始執行後，運作方式與互動式查詢相同。詳情請參閱「[查詢佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)」。
* **[持續查詢工作](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)**。
  有了這些工作，查詢就會持續執行，讓您即時分析 BigQuery 中的輸入資料，然後將結果寫入 BigQuery 資料表，或將結果匯出至 Bigtable 或 Pub/Sub。您可以使用這項功能執行具時效性的工作，例如建立洞察資料並立即採取行動、套用即時機器學習 (ML) 推論，以及建構事件導向資料管道。

您可以使用下列方法執行查詢工作：

* 在[Google Cloud 控制台](https://docs.cloud.google.com/bigquery/bigquery-web-ui?hl=zh-tw#overview)中編寫及執行查詢。
* 在 [bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)中執行 `bq query` 指令。
* 透過程式呼叫 BigQuery [REST API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2?hl=zh-tw) 中的 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/query?hl=zh-tw) 或 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/insert?hl=zh-tw) 方法。
* 使用 BigQuery [用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)。

BigQuery 會將查詢結果儲存至[臨時資料表 (預設) 或永久資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#temporary_and_permanent_tables)。
將永久資料表指定為結果的目的地資料表時，您可以選擇附加或覆寫現有資料表，也可以建立名稱不重複的新資料表。

**注意：** 如果您從某個專案查詢儲存在其他專案中的資料，系統會向查詢專案收取查詢工作的費用，並向儲存資料的專案收取 BigQuery 中儲存的資料量費用。

## 必要的角色

如要取得執行查詢作業所需的權限，請要求管理員授予您下列 IAM 角色：

* 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)。
* 查詢參照的所有資料表和檢視區塊的 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)。如要查詢檢視區塊，您也必須具備所有基礎資料表和檢視區塊的這項角色。如果您使用[授權檢視畫面](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)或[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)，就不需要存取基礎來源資料。

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行查詢工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行查詢工作，必須具備下列權限：

* `bigquery.jobs.create`
  無論資料儲存於何處，都會在執行查詢的專案中顯示。
* `bigquery.tables.getData`
  查詢參照的所有資料表和檢視表。如要查詢檢視表，您也需要所有基礎資料表和檢視表的這項權限。如果您使用[授權檢視畫面](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)或[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)，就不需要存取基礎來源資料。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 疑難排解

```
Access Denied: Project [project_id]: User does not have bigquery.jobs.create
permission in project [project_id].
```

如果主體沒有在專案中建立查詢工作的權限，就會發生這個錯誤。

**解決方法**：系統管理員必須授予您所查詢專案的 `bigquery.jobs.create` 權限。除了存取所查詢資料所需的權限外，您還必須具備這項權限。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 執行互動式查詢

如要執行互動式查詢，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「SQL 查詢」add\_box。
3. 在查詢編輯器中輸入有效的 GoogleSQL 查詢。

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

   或者，您也可以使用「參考」[面板](#use-reference-panel)建構新查詢。
4. 選用步驟：如要在輸入查詢時自動顯示程式碼建議，請按一下「更多」settings，然後選取「SQL 自動完成」。如果不需要自動完成建議，請取消選取「SQL 自動完成」。這也會關閉專案名稱自動填入建議。
5. 選用：如要選取其他[查詢設定](#query-settings)，請按一下「更多」settings，然後按一下「查詢設定」。
6. 按一下「執行」play\_circle。

   如未指定目的地資料表，查詢工作會將輸出寫入臨時 (快取) 資料表。

   現在可以在「查詢結果」窗格的「結果」分頁中，探索查詢結果。
7. 選用步驟：如要按照資料欄排序查詢結果，請點選資料名稱欄旁的 arrow\_drop\_down「Open sort menu」(開啟排序選單)，然後選取排列順序。如果排序作業的預估處理位元組數大於 0，選單頂端就會顯示位元組數。
8. 選用：如要查看查詢結果的視覺化資料，請前往「Visualization」(視覺化) 分頁標籤。你可以放大或縮小圖表、將圖表下載為 PNG 檔案，或切換圖例的顯示狀態。

   在「視覺化設定」窗格中，您可以變更視覺化類型，並設定視覺化的指標和維度。這個窗格中的欄位會預先填入從查詢目的地資料表結構定義推論出的初始設定。在同一個查詢編輯器中，後續執行查詢時會保留設定。

   如果是「折線圖」、「長條圖」或「散布圖」**，支援的維度資料類型為 `INT64`、`FLOAT64`、`NUMERIC`、`BIGNUMERIC`、`TIMESTAMP`、`DATE`、`DATETIME`、`TIME` 和 `STRING`，支援的指標資料類型則為 `INT64`、`FLOAT64`、`NUMERIC` 和 `BIGNUMERIC`。**

   如果查詢結果包含 `GEOGRAPHY` 類型，則預設的視覺化類型為「地圖」，可讓您在[互動式地圖](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize?hl=zh-tw#bigquery_studio)上查看結果。
9. 選用：在「JSON」分頁中，您可以 JSON 格式查看查詢結果，其中鍵是欄名，值是該欄的結果。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 使用 [`bq query` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query)。在下列範例中，`--use_legacy_sql=false` 旗標可讓您使用 GoogleSQL 語法。

   ```
   bq query \
       --use_legacy_sql=false \
       'QUERY'
   ```

   請將 QUERY 替換成有效的 GoogleSQL 查詢。舉例來說，您可以查詢 [BigQuery 公開資料集 `usa_names`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=usa_names&%3Bpage=dataset&hl=zh-tw)，找出 1910 年到 2013 年之間美國最常見的姓名：

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

   查詢工作會將輸出內容寫入暫時性 (快取) 資料表。

   您可以選擇指定查詢結果的目的地資料表和[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如要將結果寫入現有資料表，請加入適當的標記來附加 (`--append_table=true`) 或覆寫 (`--replace=true`) 資料表。

   ```
   bq query \
       --location=LOCATION \
       --destination_table=TABLE \
       --use_legacy_sql=false \
       'QUERY'
   ```

   更改下列內容：

   * LOCATION：目的地資料表所在的區域或多區域，例如 `US`

     在本範例中，`usa_names` 資料集儲存在美國多區域位置。如果您為這項查詢指定目的地資料表，則包含目的地資料表的資料集也必須位於美國多區域。您無法查詢位於某個位置的資料集，然後將結果寫入位於另一個位置的資料表。

     您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
   * TABLE：目的地資料表的名稱，例如 `myDataset.myTable`

     如果目的地資料表是新資料表，BigQuery 會在您執行查詢時建立該資料表。不過，您必須指定現有資料集。

     如果資料表不在目前的專案中，請使用 `PROJECT_ID:DATASET.TABLE` 格式新增Google Cloud 專案 ID，例如 `myProject:myDataset.myTable`。如未指定 `--destination_table`，系統會產生將輸出寫入臨時資料表的查詢工作。

### Terraform

使用 [`google_bigquery_job` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_job)。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會執行查詢。您可以[查看工作詳細資料](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)，擷取查詢結果：

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

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

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

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

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

如要使用 API 執行查詢，請[插入新工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)並填入 `query` 工作設定屬性。(選用) 請前往[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段，並在 `location` 屬性中指定您的位置。

呼叫 [`getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 來輪詢結果。持續輪詢，直到 `jobComplete` 等於 `true` 為止。檢查 `errors` 清單中的錯誤與警告。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;

public class SimpleQuery {

  public static void runSimpleQuery() {
    // TODO(developer): Replace this query before running the sample.
    String query = "SELECT corpus FROM `bigquery-public-data.samples.shakespeare` GROUP BY corpus;";
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
      result.iterateAll().forEach(rows -> rows.forEach(row -> System.out.println(row.getValue())));

      System.out.println("Query ran successfully");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query did not run \n" + e.toString());
    }
  }
}
```

如要透過 Proxy 執行查詢，請參閱[設定 Proxy](https://github.com/googleapis/google-cloud-java#configuring-a-proxy)。

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

## 執行批次查詢

如要執行批次查詢，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「SQL 查詢」add\_box。
3. 在查詢編輯器中輸入有效的 GoogleSQL 查詢。

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
4. 按一下「更多」settings，然後按一下「查詢設定」。
5. 在「資源管理」部分，選取「批次」。
6. 選用：調整[查詢設定](#query-settings)。
7. 按一下 [儲存]。
8. 按一下「執行」play\_circle。

   如未指定目的地資料表，查詢工作會將輸出寫入臨時 (快取) 資料表。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 使用 [`bq query` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query)並指定 `--batch` 旗標。在下列範例中，`--use_legacy_sql=false` 旗標可讓您使用 GoogleSQL 語法。

   ```
   bq query \
       --batch \
       --use_legacy_sql=false \
       'QUERY'
   ```

   請將 QUERY 替換成有效的 GoogleSQL 查詢。舉例來說，您可以查詢 [BigQuery 公開資料集 `usa_names`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=usa_names&%3Bpage=dataset&hl=zh-tw)，找出 1910 年到 2013 年之間美國最常見的姓名：

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

   查詢工作會將輸出內容寫入暫時性 (快取) 資料表。

   您可以選擇指定查詢結果的目的地資料表和[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如要將結果寫入現有資料表，請加入適當的標記來附加 (`--append_table=true`) 或覆寫 (`--replace=true`) 資料表。

   ```
   bq query \
       --batch \
       --location=LOCATION \
       --destination_table=TABLE \
       --use_legacy_sql=false \
       'QUERY'
   ```

   更改下列內容：

   * LOCATION：目的地資料表所在的區域或多區域，例如 `US`

     在本範例中，`usa_names` 資料集儲存在美國多區域位置。如果您為這項查詢指定目的地資料表，則包含目的地資料表的資料集也必須位於美國多區域。您無法查詢位於某個位置的資料集，然後將結果寫入位於另一個位置的資料表。

     您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
   * TABLE：目的地資料表的名稱，例如 `myDataset.myTable`

     如果目的地資料表是新資料表，BigQuery 會在您執行查詢時建立該資料表。不過，您必須指定現有資料集。

     如果資料表不在目前的專案中，請使用 `PROJECT_ID:DATASET.TABLE` 格式新增Google Cloud 專案 ID，例如 `myProject:myDataset.myTable`。如未指定 `--destination_table`，系統會產生將輸出寫入臨時資料表的查詢工作。

### API

如要使用 API 執行查詢，請[插入新工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)並填入 `query` 工作設定屬性。(選用) 請前往[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段，並在 `location` 屬性中指定您的位置。

填入查詢工作屬性時，請加入 `configuration.query.priority` 屬性，並將值設為 `BATCH`。

呼叫 [`getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 來輪詢結果。持續輪詢，直到 `jobComplete` 等於 `true` 為止。檢查 `errors` 清單中的錯誤與警告。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library and create a client
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function queryBatch() {
  // Runs a query at batch priority.

  // Create query job configuration. For all options, see
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#jobconfigurationquery
  const queryJobConfig = {
    query: `SELECT corpus
            FROM \`bigquery-public-data.samples.shakespeare\` 
            LIMIT 10`,
    useLegacySql: false,
    priority: 'BATCH',
  };

  // Create job configuration. For all options, see
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#jobconfiguration
  const jobConfig = {
    // Specify a job configuration to set optional job resource properties.
    configuration: {
      query: queryJobConfig,
    },
  };

  // Make API request.
  const [job] = await bigquery.createJob(jobConfig);

  const jobId = job.metadata.id;
  const state = job.metadata.status.state;
  console.log(`Job ${jobId} is currently in state ${state}`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

job_config = bigquery.QueryJobConfig(
    # Run at batch priority, which won't count toward concurrent rate limit.
    priority=bigquery.QueryPriority.BATCH
)

sql = """
    SELECT corpus
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus;
"""

# Start the query, passing in the extra configuration.
query_job = client.query(sql, job_config=job_config)  # Make an API request.

# Check on the progress by getting the job's updated state. Once the state
# is `DONE`, the results are ready.
query_job = client.get_job(
    query_job.job_id, location=query_job.location
)  # Make an API request.

print("Job {} is currently in state {}".format(query_job.job_id, query_job.state))
```

## 執行持續查詢

執行持續查詢工作需要額外設定。詳情請參閱「[建立連續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw)」。

## 使用「參考資料」面板

在查詢編輯器中，「參考資料」面板會動態顯示資料表、快照、檢視區塊和具體化檢視區塊的情境感知資訊。您可以在面板中預覽這些資源的結構定義詳細資料，或在新分頁中開啟。您也可以使用「Reference」面板，插入查詢程式碼片段或欄位名稱，建構新查詢或編輯現有查詢。

如要使用「Reference」(參考) 面板建構新查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「SQL 查詢」add\_box。
3. 按一下「quick\_reference\_all」quick\_reference\_all**參考資料**。
4. 按一下最近或已加星號的資料表或檢視畫面。您也可以使用搜尋列尋找資料表和檢視區塊。
5. 依序點選 more\_vert「View actions」(查看動作) 和「Insert query snippet」(插入查詢程式碼片段)。
6. 選用：您可以預覽資料表的結構定義詳細資料，或在新分頁中查看/開啟這些資料。
7. 現在您可以手動編輯查詢，或直接在查詢中插入欄位名稱。如要插入欄位名稱，請在查詢編輯器中指向要插入欄位名稱的位置，然後按一下「參照」面板中的欄位名稱。

## 查詢設定

執行查詢時，您可以指定下列設定：

* 查詢結果的[目的地資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#permanent-table)。
* 這項工作的優先順序。
* 是否要使用[快取的查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)。
* 工作逾時時間 (以毫秒為單位)。
* 是否使用[工作階段模式](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)。
* 要使用的[加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)類型。
* 查詢的計費位元組數上限。
* 要使用的 [SQL 方言](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。
* 執行查詢的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。查詢必須在與查詢中參照的任何資料表相同的位置執行。
* 要執行查詢的[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)。

## 「選擇性建立工作」模式

「選擇性建立工作」模式可縮短執行時間較短的查詢整體延遲時間，例如資訊主頁或資料探索工作負載的查詢。這個模式會執行查詢，並針對 `SELECT` 陳述式傳回內嵌結果，不需要使用 [`jobs.getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 擷取結果。使用「選擇性建立工作」模式的查詢在執行時不會建立工作，除非 BigQuery 判斷必須建立工作才能完成查詢。

如要啟用「選擇性建立工作」模式，請在 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 要求主體中，將 [QueryRequest](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw#QueryRequest) 執行個體的 `jobCreationMode` 欄位設為 `JOB_CREATION_OPTIONAL`。

如果這個欄位的值設為 `JOB_CREATION_OPTIONAL`，BigQuery 會判斷查詢是否可以使用選用的工作建立模式。如果是，BigQuery 會執行查詢，並在回應的 `rows` 欄位中傳回所有結果。由於系統不會為這項查詢建立工作，因此 BigQuery 不會在回應主體中傳回 `jobReference`。而是傳回 `queryId` 欄位，您可以使用 [`INFORMATION_SCHEMA.JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#optional-job-creation)，取得查詢洞察資料。由於系統未建立任何工作，因此沒有可傳遞至 [`jobs.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw) 和 [`jobs.getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) API 的 `jobReference`，無法查詢這些查詢。

如果 BigQuery 判斷完成查詢需要工作，就會傳回 `jobReference`。您可以檢查 [`INFORMATION_SCHEMA.JOBS` 檢視中的 `job_creation_reason` 欄位](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#optional-job-creation)，判斷系統為查詢建立工作的原因。在這種情況下，查詢完成時，您應使用 [`jobs.getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 擷取結果。

使用 `JOB_CREATION_OPTIONAL` 值時，回應中可能不會出現 `jobReference` 欄位。存取欄位前，請先檢查該欄位是否存在。

為多重陳述式查詢 (指令碼) 指定 `JOB_CREATION_OPTIONAL` 時，BigQuery 可能會最佳化執行程序。在最佳化過程中，BigQuery 可能會判斷出，建立的工作資源數量少於個別陳述式數量，就能完成指令碼，甚至可能完全不建立任何工作，就執行整個指令碼。這項最佳化作業取決於 BigQuery 對指令碼的評估結果，因此不一定適用於所有情況。系統會全自動執行最佳化作業。使用者無須採取任何行動或進行任何控制。

如要使用「選擇性建立工作」模式執行查詢，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「SQL 查詢」add\_box。
3. 在查詢編輯器中輸入有效的 GoogleSQL 查詢。

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
4. 按一下「更多」settings，然後選擇「選擇性建立工作」查詢模式。如要確認這項選擇，請按一下「確認」。
5. 按一下「執行」play\_circle。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 使用 [`bq query` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query)並指定 `--job_creation_mode=JOB_CREATION_OPTIONAL` 旗標。在下列範例中，`--use_legacy_sql=false` 旗標可讓您使用 GoogleSQL 語法。

   ```
   bq query \
       --rpc=true \
       --use_legacy_sql=false \
       --job_creation_mode=JOB_CREATION_OPTIONAL \
       --location=LOCATION \
       'QUERY'
   ```

   請將 QUERY 替換為有效的 GoogleSQL 查詢，並將 LOCATION 替換為資料集所在的有效區域。舉例來說，您可以查詢 [BigQuery 公開資料集 `usa_names`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=usa_names&%3Bpage=dataset&hl=zh-tw)，找出 1910 年到 2013 年之間美國最常見的姓名：

   ```
   bq query \
       --rpc=true \
       --use_legacy_sql=false \
       --job_creation_mode=JOB_CREATION_OPTIONAL \
       --location=us \
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

   查詢作業會在回應中內嵌傳回輸出內容。

   **附註：** 您可以視需要使用 `--apilog=stdout` 記錄 API 要求和回應，以便擷取 `queryId`。

### API

如要使用 API 在「選擇性建立工作」模式中執行查詢，請[同步執行查詢](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw)，並填入 [`QueryRequest`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw#QueryRequest) 屬性。加入 `jobCreationMode` 屬性，並將值設為 `JOB_CREATION_OPTIONAL`。

查看回覆。如果 `jobComplete` 等於 `true` 且 `jobReference` 為空，請從 `rows` 欄位讀取結果。您也可以從回覆中取得 `queryId`。

如果存在 `jobReference`，您可以檢查 `jobCreationReason`，瞭解 BigQuery 建立工作的原因。呼叫 [`getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 來輪詢結果。持續輪詢，直到 `jobComplete` 等於 `true` 為止。檢查 `errors` 清單中的錯誤與警告。

### Java

適用版本：2.51.0 以上

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.JobId;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.QueryJobConfiguration.JobCreationMode;
import com.google.cloud.bigquery.TableResult;

// Sample demonstrating short mode query execution.
//
// This feature is controlled by setting the defaultJobCreationMode
// field in the BigQueryOptions used for the client. JOB_CREATION_OPTIONAL
// allows for the execution of queries without creating a job.
public class QueryJobOptional {

  public static void main(String[] args) {
    String query =
        "SELECT name, gender, SUM(number) AS total FROM "
            + "bigquery-public-data.usa_names.usa_1910_2013 GROUP BY "
            + "name, gender ORDER BY total DESC LIMIT 10";
    queryJobOptional(query);
  }

  public static void queryJobOptional(String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs
      // to be created once, and can be reused for multiple requests.
      BigQueryOptions options = BigQueryOptions.getDefaultInstance();
      options.setDefaultJobCreationMode(JobCreationMode.JOB_CREATION_OPTIONAL);
      BigQuery bigquery = options.getService();

      // Execute the query. The returned TableResult provides access information
      // about the query execution as well as query results.
      TableResult results = bigquery.query(QueryJobConfiguration.of(query));

      JobId jobId = results.getJobId();
      if (jobId != null) {
        System.out.println("Query was run with job state.  Job ID: " + jobId.toString());
      } else {
        System.out.println("Query was run in short mode.  Query ID: " + results.getQueryId());
      }

      // Print the results.
      results
          .iterateAll()
          .forEach(
              row -> {
                System.out.print("name:" + row.get("name").getStringValue());
                System.out.print(", gender: " + row.get("gender").getStringValue());
                System.out.print(", total: " + row.get("total").getLongValue());
                System.out.println();
              });

    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

如要透過 Proxy 執行查詢，請參閱[設定 Proxy](https://github.com/googleapis/google-cloud-java#configuring-a-proxy)。

### Python

適用版本：3.34.0 以上

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# This example demonstrates executing a query without requiring an associated
# job.
from google.cloud import bigquery
from google.cloud.bigquery.enums import JobCreationMode

# Construct a BigQuery client object, specifying that the library should
# avoid creating jobs when possible.
client = bigquery.Client(
    default_job_creation_mode=JobCreationMode.JOB_CREATION_OPTIONAL
)

query = """
    SELECT
        name,
        gender,
        SUM(number) AS total
    FROM
        bigquery-public-data.usa_names.usa_1910_2013
    GROUP BY
        name, gender
    ORDER BY
        total DESC
    LIMIT 10
"""
# Run the query.  The returned `rows` iterator can return information about
# how the query was executed as well as the result data.
rows = client.query_and_wait(query)

if rows.job_id is not None:
    print("Query was run with job state.  Job ID: {}".format(rows.job_id))
else:
    print(
        "Query was run without creating a job.  Query ID: {}".format(rows.query_id)
    )

print("The query data:")
for row in rows:
    # Row values can be accessed by field name or index.
    print("name={}, gender={}, total={}".format(row[0], row[1], row["total"]))
```

### 節點

適用版本：8.1.0 以上

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Demonstrates issuing a query that may be run in short query mode.

// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new
```