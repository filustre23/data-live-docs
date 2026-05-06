Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查詢叢集資料表

在 BigQuery 中建立叢集資料表時，資料表資料會依照資料表結構定義中的一或多個資料欄內容進行自動編排。您指定的資料欄會用來將相關資料放在相同位置。使用多個資料欄對資料表進行叢集處理時，您指定的資料欄排列順序非常重要。指定的資料欄順序決定了資料的排列順序。

對叢集資料表執行查詢時，如要達到最佳效能，使用的運算式要能依照指定的叢集資料欄順序，針對一個叢集資料欄或多個叢集資料欄進行篩選。就效能而言，叢集資料欄的篩選查詢通常勝過於非叢集資料欄的篩選查詢。

BigQuery 根據叢集資料欄的值在叢集資料表中進行資料排序，並將資料組織成區塊。

若您提交叢集資料欄含有篩選器的查詢，BigQuery 會使用叢集資訊有效確定區塊是否包含任何與查詢相關的資料，因而只掃描相關區塊，這樣的過程就稱為[區塊修剪](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#block-pruning)。

您可以透過以下方式查詢叢集資料表：

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具的 `bq query` 指令
* 呼叫 [`jobs.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)並設定[查詢工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationQuery)
* 使用用戶端程式庫

您只能對叢集資料表使用 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql?hl=zh-tw)。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// queryClusteredTable demonstrates querying a table that has a clustering specification.
func queryClusteredTable(w io.Writer, projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	q := client.Query(fmt.Sprintf(`
	SELECT
	  COUNT(1) as transactions,
	  SUM(amount) as total_paid,
	  COUNT(DISTINCT destination) as distinct_recipients
    FROM
	  `+"`%s.%s`"+`
	 WHERE
	    timestamp > TIMESTAMP('2015-01-01')
		AND origin = @wallet`, datasetID, tableID))
	q.Parameters = []bigquery.QueryParameter{
		{
			Name:  "wallet",
			Value: "wallet00001866cb7e0f09a890",
		},
	}
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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;

public class QueryClusteredTable {

  public static void runQueryClusteredTable() throws Exception {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    queryClusteredTable(projectId, datasetName, tableName);
  }

  public static void queryClusteredTable(String projectId, String datasetName, String tableName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      String sourceTable = "`" + projectId + "." + datasetName + "." + tableName + "`";
      String query =
          "SELECT word, word_count\n"
              + "FROM "
              + sourceTable
              + "\n"
              // Optimize query performance by filtering the clustered columns in sort order
              + "WHERE corpus = 'romeoandjuliet'\n"
              + "AND word_count >= 1";

      QueryJobConfiguration queryConfig = QueryJobConfiguration.newBuilder(query).build();

      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query clustered table performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the destination table.
# table_id = "your-project.your_dataset.your_table_name"

sql = "SELECT * FROM `bigquery-public-data.samples.shakespeare`"
cluster_fields = ["corpus"]

job_config = bigquery.QueryJobConfig(
    clustering_fields=cluster_fields, destination=table_id
)

# Start the query, passing in the extra configuration.
client.query_and_wait(
    sql, job_config=job_config
)  # Make an API request and wait for job to complete.

table = client.get_table(table_id)  # Make an API request.
if table.clustering_fields == cluster_fields:
    print(
        "The destination table is written using the cluster_fields configuration."
    )
```

## 所需權限

如要執行查詢[作業](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)，您需要對執行查詢作業的專案具備 `bigquery.jobs.create` 身分與存取權管理 (IAM) 權限。

下列每個預先定義的 IAM 角色都包含執行查詢作業所需的權限：

* `roles/bigquery.admin`
* `roles/bigquery.jobUser`
* `roles/bigquery.user`

此外，您還需要查詢參照的所有資料表和檢視區塊的 `bigquery.tables.getData` 權限。此外，查詢檢視區塊時，您需要所有基礎資料表和檢視區塊的這項權限。不過，如果您使用[授權檢視畫面](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)或[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)，就不需要存取基礎來源資料。

下列每個預先定義的 IAM 角色都包含查詢參照的所有資料表和檢視區塊所需權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataViewer`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 最佳做法

如要讓叢集資料表的查詢達到最佳效能，請使用下列最佳做法。

為提供背景資訊，最佳做法範例中使用的資料表樣本是使用 DDL 陳述式建立的叢集資料表。DDL 陳述式會建立名為 `ClusteredSalesData` 的資料表。資料表會依照下列資料欄的排序順序進行叢集處理：`customer_id`、`product_id`、`order_id`。

```
CREATE TABLE
  `mydataset.ClusteredSalesData`
PARTITION BY
  DATE(timestamp)
CLUSTER BY
  customer_id,
  product_id,
  order_id AS
SELECT
  *
FROM
  `mydataset.SalesData`
```

### 依排序順序篩選叢集資料欄

指定篩選條件時，使用的運算式要能依照排序順序，對叢集資料欄進行篩選。排序順序是 `CLUSTER BY` 子句中指定的資料欄順序。
如要享有叢集功能帶來的優勢，請在從左到右的排序順序中，納入一或多個叢集資料欄，並從第一個資料欄開始。在大多數情況下，第一個分群資料欄在區塊修剪方面最有效，其次是第二個資料欄，然後是第三個。您仍可在查詢中單獨使用第二或第三個資料欄，但區塊修剪可能不會那麼有效。篩選器運算式中的資料欄名稱順序不會影響效能。

下列範例會查詢在上一個範例中建立的 `ClusteredSalesData` 叢集資料表。查詢內含的篩選運算式可先依 `customer_id` 進行篩選，再依 `product_id` 進行篩選。這項查詢會依照*排序順序* (`CLUSTER BY` 子句中指定的資料欄順序)，對叢集資料欄進行篩選，因此可達到最佳效能。

```
SELECT
  SUM(totalSale)
FROM
  `mydataset.ClusteredSalesData`
WHERE
  customer_id = 10000
  AND product_id LIKE 'gcp_analytics%'
```

下列查詢並未依照排序順序對叢集資料欄進行篩選，因此無法達到最佳查詢效能。這項查詢先依 `product_id` 進行篩選，再依 `order_id` 進行篩選 (略過 `customer_id`)。

```
SELECT
  SUM(totalSale)
FROM
  `mydataset.ClusteredSalesData`
WHERE
  product_id LIKE 'gcp_analytics%'
  AND order_id = 20000
```

### 請勿在複合篩選運算式中使用叢集資料欄

如果在複合篩選運算式中使用叢集資料欄，就無法套用區塊修剪，從而無法達到最佳查詢效能。

舉例來說，下列查詢不會修剪區塊，原因在於篩選運算式當中的一個函式使用了叢集資料欄 `customer_id`。

```
SELECT
  SUM(totalSale)
FROM
  `mydataset.ClusteredSalesData`
WHERE
  CAST(customer_id AS STRING) = "10000"
```

如要修剪區塊以達到最佳查詢效能，請使用如下所示的簡易篩選運算式。在本例中，叢集資料欄 `customer_id` 會套用簡易篩選器。

```
SELECT
  SUM(totalSale)
FROM
  `mydataset.ClusteredSalesData`
WHERE
  customer_id = 10000
```

### 不要比對叢集資料欄和其他資料欄

如果篩選運算式把叢集資料欄跟另一個資料欄 (叢集資料欄或非叢集資料欄) 進行比對，就無法套用區塊修剪，因此無法達到最佳查詢效能。

下列查詢沒有修剪區塊的原因是，篩選運算式把 `customer_id` 叢集資料欄跟另一個 `order_id` 資料欄進行比對。

```
SELECT
  SUM(totalSale)
FROM
  `mydataset.ClusteredSalesData`
WHERE
  customer_id = order_id
```

## 表格安全性

如要控管 BigQuery 資料表的存取權，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

## 後續步驟

* 如需執行查詢的詳細資訊，請參閱[執行互動式與批次查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)一文。
* 如要瞭解如何建立及使用叢集資料表，請參閱[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)。
* 如需 BigQuery 中的分區資料表支援總覽，請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。
* 如要瞭解如何建立分區資料表，請參閱[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]