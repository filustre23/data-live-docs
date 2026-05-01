* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 安排查詢

本頁面說明如何在 BigQuery 中排定週期性的查詢。

您可以為查詢進行排程，讓查詢週期性執行。排定的查詢必須以 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 編寫，其中可包含 [資料定義語言 (DDL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw) 和 [資料操作語言 (DML)](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw) 陳述式。您可以將查詢字串和目的地資料表參數化，依日期和時間整理查詢結果。

建立或更新查詢的排程時，查詢的排定時間會從當地時間轉換為世界標準時間。世界標準時間不受日光節約時間影響。

## 事前準備

* 排程查詢會使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)的功能。請確認您已完成「[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)」一文中的所有必要動作。
* 授予 Identity and Access Management (IAM) 角色，讓使用者擁有執行本文中各項工作所需的權限。
* 如果您打算指定客戶自行管理的加密金鑰 (CMEK)，請確保[服務帳戶具有加密和解密權限](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#grant_permission)，且您擁有使用 CMEK 時所需的 [Cloud KMS 金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱[指定排定查詢的加密金鑰](#CMEK)。

## 限制

* 如果排程查詢在整點執行 (例如 09:00)，可能會多次觸發，導致資料重複等非預期結果。`INSERT`為避免發生這類非預期的結果，請使用非整點的排程 (例如 08:58 或 09:03)。

### 所需權限

如要排定查詢時間，您必須具備下列 IAM 權限：

* 如要建立轉移作業，您必須具備 `bigquery.transfers.update` 和 `bigquery.datasets.get` 權限，或是 `bigquery.jobs.create`、`bigquery.transfers.get` 和 `bigquery.datasets.get` 權限。

  **注意：** 如果您使用 Google Cloud 控制台或 bq 指令列工具排定查詢時間，則必須具備 `bigquery.transfers.get` 權限。
* 如要執行排程查詢，必須具備下列條件：

  + 目標資料集的 `bigquery.datasets.get` 權限
  + `bigquery.jobs.create`

如要修改或刪除已排定的查詢，您必須具備 `bigquery.transfers.update` 和 `bigquery.transfers.get` 權限，或是 `bigquery.jobs.create` 權限和已排定查詢的擁有權。

預先定義的 [BigQuery 管理員 (`roles/bigquery.admin`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin) IAM 角色包含排定或修改查詢所需的權限。

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

如要建立或更新由服務帳戶執行的排程查詢，您必須有該服務帳戶的存取權。如要進一步瞭解如何授予使用者服務帳戶角色，請參閱[服務帳戶使用者角色](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#user-role)。如要在Google Cloud 主控台的排程查詢使用者介面中選取服務帳戶，您需要下列 IAM 權限：

* `iam.serviceAccounts.list` 列出服務帳戶。
* `iam.serviceAccountUser`，將服務帳戶指派給排程查詢。

**注意：** 如果您使用 bq 指令列工具，請使用 `--service_account_name` 旗標，而非以服務帳戶身分驗證。

## 設定選項

以下各節說明設定選項。

### 查詢字串

查詢字串必須有效，且必須以 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 編寫。排定的查詢每次執行時，都會收到下列[查詢參數](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw#parameterized-timestamps)。

如要在為查詢進行排程之前，手動以 `@run_time` 和 `@run_date` 參數測試查詢字串，請使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)。

#### 可用的參數

| 參數 | GoogleSQL 類型 | 值 |
| --- | --- | --- |
| `@run_time` | [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type) | 以世界標準時間表示。對於具有定期執行排程的查詢，`run_time` 用以表示預定的執行時間。舉例來說，如果排程查詢的時程設定為「every 24 hours」(每 24 小時)，則連續兩次查詢之間的 `run_time` 差異就是 24 小時整 (雖然實際執行時間可能會略有不同)。 |
| `@run_date` | [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type) | 代表邏輯日曆日期。 |

#### 範例

在以下範例中，系統會查詢名為 [`hacker_news.stories`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=hacker_news&%3Bpage=dataset&hl=zh-tw) 的公開資料集，而 `@run_time` 參數是該查詢字串的一部分。

```
SELECT @run_time AS time,
  title,
  author,
  text
FROM `bigquery-public-data.hacker_news.stories`
LIMIT
  1000
```

### 目標資料表

設定排程查詢時，如果查詢結果的目的地資料表不存在，BigQuery 會嘗試建立目的地資料表。

如使用 DDL 或 DML 查詢，請在 Google Cloud 控制台中選擇「Processing location」(處理位置) 或區域。DDL 或 DML 查詢需有處理位置，才能建立目的地資料表。

如果目的地資料表存在，且您使用 `WRITE_APPEND`
[寫入偏好設定](#write_preference)，BigQuery 會將資料附加至目的地資料表，並嘗試對應結構定義。BigQuery 會自動允許新增及重新排序欄位，並容許缺少選填欄位。如果資料表結構定義在執行期間的變更幅度過大，導致 BigQuery 無法自動處理變更，已排定時程的查詢就會失敗。

查詢可參照來自不同專案和不同資料集的資料表。設定排程查詢時，資料表名稱不需要包含目的地資料集。目的地資料集會另外指定。

排程查詢的目的地資料集和資料表必須與排程查詢位於同一個專案。

#### 寫入偏好設定

您選取的寫入偏好設定，會決定查詢結果寫入現有目的地資料表的方式。

* `WRITE_TRUNCATE`：如果資料表存在，BigQuery 會覆寫資料表資料。
* `WRITE_APPEND`：如果資料表存在，BigQuery 會將資料附加至資料表。

如果您使用 DDL 或 DML 查詢，就無法使用寫入偏好設定選項。

唯有 BigQuery 成功完成查詢，才能建立、截斷或附加目的地資料表。建立、截斷或附加的動作是在工作完成時，以一次完整更新的形式進行。

#### 分群

如果資料表是使用 DDL 陳述式 `CREATE TABLE AS SELECT` 建立，排程查詢只能在新資料表上建立叢集。請參閱「[使用資料定義語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)」頁面中的「[從查詢結果建立分群資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_clustered_table_from_the_result_of_a_query)」一節。

#### 分區選項

排程查詢可建立分區或非分區的目的地資料表。分區功能適用於 Google Cloud 主控台、bq 指令列工具和 API 設定方法。如要使用具有分區功能的 DDL 或 DML 查詢，請將「目的地資料表分區欄位」留白。

您可以在 BigQuery 中使用下列類型的資料表分區：

* [整數範圍分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#integer_range)：根據特定 `INTEGER` 資料欄中的值範圍分區的資料表。
* [時間單位資料欄分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)：根據 [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type)、[`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type) 或 [`DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#datetime_type) 資料欄分區的資料表。
* [擷取時間分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#ingestion_time)：依擷取時間分區的資料表。BigQuery 會根據擷取資料的時間，自動將資料列指派給分區。

如要在Google Cloud 控制台使用排程查詢建立分區資料表，請使用下列選項：

* 如要使用整數範圍分區，請將「目的地資料表分區欄位」留空。
* 如要使用時間單位資料欄分區，請在[設定排定的查詢](#set_up_scheduled_queries)時，於「目的地資料表分區欄位」中指定資料欄名稱。
* 如要使用擷取時間分區，請將「Destination table partitioning field」(目的地資料表分區欄位) 留空，並在目的地資料表的名稱中指定日期分區。例如：`mytable${run_date}`。詳情請參閱「[參數範本語法](#param-templating-syntax)」。

#### 可用的參數

設定排定的查詢時，可使用執行階段參數，指定要以何種方式對目的地資料表進行分區。

| 參數 | 範本類型 | 值 |
| --- | --- | --- |
| `run_time` | 格式化的時間戳記 | 採用世界標準時間，依排程而定。對於具有定期執行排程的查詢，`run_time` 用以表示預定的執行時間。舉例來說，如果排程查詢的時程設定為「every 24 hours」(每 24 小時)，則連續兩次查詢之間的 `run_time` 差異就是 24 小時整 (雖然實際執行時間可能會略有不同)。  請參閱 [`TransferRun.runTime`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs.runs?hl=zh-tw) 的說明。 |
| `run_date` | 日期字串 | `run_time` 參數的日期，採用以下格式：`%Y-%m-%d`；例如 `2018-01-01`。這個格式與擷取時間分區資料表相容。 |

#### 範本系統

可使用範本語法讓排定的查詢支援目的地資料表名稱中的執行階段參數。

#### 參數範本語法

範本語法支援基本字串範本和時區設定。參數會以下列格式參照：

* `{run_date}`
* `{run_time[+\-offset]|"time_format"}`

| **參數** | **Purpose** |
| --- | --- |
| `run_date` | 這個參數會由格式為 `YYYYMMDD` 的日期取代。 |
| `run_time` | 這個參數支援下列屬性： `offset` 時區設定，依小時 (h)、分鐘 (m)、秒鐘 (s) 的順序表示。 不支援天 (d)。 可使用小數，例如：`1.5h`。  `time_format` 格式設定字串。最常見的格式參數是年 (%Y)、月 (%m)、日 (%d)。 就分區資料表而言，YYYYMMDD 是必要的後置字串，相當於「%Y%m%d」。  進一步瞭解 [datetime 元素的格式設定](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators?hl=zh-tw#supported-format-elements-for-datetime)。 |

**使用須知：**

* run\_time、offset 和 time\_format 之間不得有空格字元。
* 如果字串要包含大括號，可以按以下方式加以逸出：`'\{' and '\}'`。
* 如果 time\_format 要包含引號或分隔號，例如 `"YYYY|MM|DD"`，可以在格式字串按以下方式加以逸出：`'\"'` 或 `'\|'`。

#### 參數範本範例

以下範例說明如何以不同的時間格式指定目的地資料表名稱，以及如何設定執行時間時區。

| **執行時間 (世界標準時間)** | **範本參數** | **輸出目的地資料表名稱** |
| --- | --- | --- |
| 2018-02-15 00:00:00 | `mytable` | `mytable` |
| 2018-02-15 00:00:00 | `mytable_{run_time|"%Y%m%d"}` | `mytable_20180215` |
| 2018-02-15 00:00:00 | `mytable_{run_time+25h|"%Y%m%d"}` | `mytable_20180216` |
| 2018-02-15 00:00:00 | `mytable_{run_time-1h|"%Y%m%d"}` | `mytable_20180214` |
| 2018-02-15 00:00:00 | `mytable_{run_time+1.5h|"%Y%m%d%H"}` 或 `mytable_{run_time+90m|"%Y%m%d%H"}` | `mytable_2018021501` |
| 2018-02-15 00:00:00 | `{run_time+97s|"%Y%m%d"}_mytable_{run_time+97s|"%H%M%S"}` | `20180215_mytable_000137` |

**注意：**使用日期或時間參數建立資料表時，如果資料表名稱結尾為日期格式 (例如 `YYYYMMDD`)，BigQuery 會[將這些資料表歸為一組](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)。在 Google Cloud 控制台中，這些分組表格可能會顯示類似 `mytable_(1)` 的名稱，代表分片表格的集合。

### 使用服務帳戶

您可以將排程查詢設定為以服務帳戶身分進行驗證。服務帳戶是與您 Google Cloud 專案相關聯的特殊帳戶。服務帳戶可以執行工作 (例如排程查詢或批次處理管道)，使用的憑證是服務帳戶本身的憑證，而非使用者憑證。

如要進一步瞭解如何透過服務帳戶進行驗證，請參閱[驗證功能簡介](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#sa-impersonation)一文。

* 您可以[設定排程查詢](#set_up_scheduled_queries)，透過服務帳戶進行驗證。如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立移轉作業。如果以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立移轉作業。
* 您可以使用 bq 指令列工具或 Google Cloud 控制台，透過服務帳戶的憑證來更新現有排程查詢。詳情請參閱「[更新排程查詢憑證](#update_scheduled_query_credentials)」。

### 使用排定的查詢指定加密金鑰

您可以指定[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/kms/docs/cmek?hl=zh-tw)，加密轉移作業的資料。您可以使用 CMEK 支援從[已排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)進行轉移。

指定移轉作業的 CMEK 後，BigQuery 資料移轉服務會將 CMEK 套用至所有已擷取資料的中間磁碟快取，確保整個資料移轉工作流程符合 CMEK 規定。

如果轉移作業最初並非使用 CMEK 建立，您就無法更新現有轉移作業來新增 CMEK。舉例來說，您無法將原本預設加密的目的地資料表，變更為使用 CMEK 加密。反之，您也無法將 CMEK 加密的目的地資料表變更為其他類型的加密。

如果移轉設定最初是使用 CMEK 加密功能建立，您可以更新移轉的 CMEK。更新移轉作業設定的 CMEK 時，BigQuery 資料移轉服務會在下次執行移轉作業時，將 CMEK 傳播至目的地資料表。屆時，BigQuery 資料移轉服務會在移轉作業執行期間，以新的 CMEK 取代任何過時的 CMEK。詳情請參閱「[更新轉移作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#update_a_transfer)」。

您也可以使用[專案預設金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#project_default_key)。
使用移轉作業指定專案預設金鑰時，BigQuery 資料移轉服務會將專案預設金鑰做為任何新移轉作業設定的預設金鑰。

## 透過服務帳戶設定排程查詢

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.CreateTransferConfigRequest;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ProjectName;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.protobuf.Struct;
import com.google.protobuf.Value;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

// Sample to create a scheduled query with service account
public class CreateScheduledQueryWithServiceAccount {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    final String datasetId = "MY_DATASET_ID";
    final String serviceAccount = "MY_SERVICE_ACCOUNT";
    final String query =
        "SELECT CURRENT_TIMESTAMP() as current_time, @run_time as intended_run_time, "
            + "@run_date as intended_run_date, 17 as some_integer";
    Map<String, Value> params = new HashMap<>();
    params.put("query", Value.newBuilder().setStringValue(query).build());
    params.put(
        "destination_table_name_template",
        Value.newBuilder().setStringValue("my_destination_table_{run_date}").build());
    params.put("write_disposition", Value.newBuilder().setStringValue("WRITE_TRUNCATE").build());
    params.put("partitioning_field", Value.newBuilder().build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Scheduled Query Name")
            .setDataSourceId("scheduled_query")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .setSchedule("every 24 hours")
            .build();
    createScheduledQueryWithServiceAccount(projectId, transferConfig, serviceAccount);
  }

  public static void createScheduledQueryWithServiceAccount(
      String projectId, TransferConfig transferConfig, String serviceAccount) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .setServiceAccountName(serviceAccount)
              .build();
      TransferConfig config = dataTransferServiceClient.createTransferConfig(request);
      System.out.println(
          "\nScheduled query with service account created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("\nScheduled query with service account was not created." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery_datatransfer

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

# The project where the query job runs is the same as the project
# containing the destination dataset.
project_id = "your-project-id"
dataset_id = "your_dataset_id"

# This service account will be used to execute the scheduled queries. Omit
# this request parameter to run the query as the user with the credentials
# associated with this client.
service_account_name = "abcdef-test-sa@abcdef-test.iam.gserviceaccount.com"

# Use standard SQL syntax for the query.
query_string = """
SELECT
  CURRENT_TIMESTAMP() as current_time,
  @run_time as intended_run_time,
  @run_date as intended_run_date,
  17 as some_integer
"""

parent = transfer_client.common_project_path(project_id)

transfer_config = bigquery_datatransfer.TransferConfig(
    destination_dataset_id=dataset_id,
    display_name="Your Scheduled Query Name",
    data_source_id="scheduled_query",
    params={
        "query": query_string,
        "destination_table_name_template": "your_table_{run_date}",
        "write_disposition": "WRITE_TRUNCATE",
        "partitioning_field": "",
    },
    schedule="every 24 hours",
)

transfer_config = transfer_client.create_transfer_config(
    bigquery_datatransfer.CreateTransferConfigRequest(
        parent=parent,
        transfer_config=transfer_config,
        service_account_name=service_account_name,
    )
)

print("Created scheduled query '{}'".format(transfer_config.name))
```

## 查看排程查詢狀態

### 控制台

如要查看排定查詢的狀態，請在導覽選單中按一下「排程」，然後篩選「排定查詢」。按一下排程查詢，即可查看詳細資料。

### bq

排程查詢是一種移轉作業。如要顯示排程查詢的詳細資料，您可以先使用 bq 指令列工具列出移轉作業設定。

輸入 `bq ls` 指令並加上移轉旗標 `--transfer_config`。還需加上以下旗標：

* `--transfer_location`

例如：

```
bq ls \
--transfer_config \
--transfer_location=us
```

如要顯示單一排程查詢的詳細資料，請輸入 `bq show` 指令，並提供`transfer_path`該排程查詢或移轉作業設定的移轉路徑。

例如：

```
bq show \
--transfer_config \
projects/862514376110/locations/us/transferConfigs/5dd12f26-0000-262f-bc38-089e0820fe38
```

### API

請使用 [`projects.locations.transferConfigs.list`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/list?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ListTransferConfigsRequest;
import com.google.cloud.bigquery.datatransfer.v1.ProjectName;
import java.io.IOException;

// Sample to get list of transfer config
public class ListTransferConfigs {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    listTransferConfigs(projectId);
  }

  public static void listTransferConfigs(String projectId) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      ListTransferConfigsRequest request =
          ListTransferConfigsRequest.newBuilder().setParent(parent.toString()).build();
      dataTransferServiceClient
          .listTransferConfigs(request)
          .iterateAll()
          .forEach(config -> System.out.print("Success! Config ID :" + config.getName() + "\n"));
    } catch (ApiException ex) {
      System.out.println("Config list not found due to error." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_datatransfer_v1

client = bigquery_datatransfer_v1.DataTransferServiceClient()


def list_transfer_configs(project_id: str, location: str) -> None:
    """Lists transfer configurations in a given project.

    This sample demonstrates how to list all transfer configurations in a project.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the transfer config, for example "us-central1"
    """

    parent = client.common_location_path(project_id, location)

    try:
        for config in client.list_transfer_configs(parent=parent):
            print(f"Name: {config.name}")
            print(f"Display Name: {config.display_name}")
            print(f"Data source: {config.data_source_id}")
            print(f"Destination dataset: {config.destination_dataset_id}")
            if "time_based_schedule" in config.schedule_options_v2:
                print(
                    f"Schedule: {config.schedule_options_v2.time_based_schedule.schedule}"
                )
            else:
                print("Schedule: None")
            print("---")
    except google.api_core.exceptions.NotFound:
        print(
            f"Error: Project '{project_id}' not found or contains no transfer configs."
        )
    except google.api_core.exceptions.PermissionDenied:
        print(
            f"Error: Permission denied for project '{project_id}'. Please ensure you have the correct permissions."
        )
```

## 更新排程查詢

### 控制台

如要更新排定的查詢，請按照下列步驟操作：

1. 在導覽選單中，按一下「排程查詢」或「排程」。
2. 在排定查詢清單中，按一下要變更的查詢名稱。
3. 在開啟的「已排定查詢詳細資料」頁面中，按一下「編輯」。
4. 選用：在查詢編輯窗格中變更查詢文字。
5. 按一下「排程查詢」，然後選取「更新排程查詢」。
6. 選用：變更查詢的其他排程選項。
7. 按一下「Update」。

### bq

排程查詢是一種移轉作業。如要更新排程查詢，可使用 bq 指令列工具建立移轉作業設定。

輸入 `bq update` 指令，並加上必要的 `--transfer_config` 旗標。

選用標記：

* `--project_id` 是您的專案 ID。如果未指定 `--project_id`，系統會使用預設專案。
* `--schedule` 是您希望查詢執行的頻率。如未指定 `--schedule`，預設設定為依建立時間計算「every 24 hours」(每 24 小時)。
* `--service_account_name` 必須配合 `--update_credentials` 才會生效。詳情請參閱「[更新排程查詢憑證](#update_scheduled_query_credentials)」。
* 與 DDL 和 DML 查詢搭配使用時，`--target_dataset` (DDL 和 DML 查詢為選用) 是命名查詢結果目標資料集的另一種方式。
* `--display_name` 是排定查詢的名稱。
* `--params`：已建立移轉設定的 JSON 格式參數。例如：--params='{"param":"param\_value"}'。
* `--destination_kms_key`：指定 Cloud KMS 金鑰的[金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id) (如果您使用客戶自行管理的加密金鑰 (CMEK) 進行這項轉移作業)。如要瞭解客戶管理的加密金鑰 (CMEK) 如何與 BigQuery 資料移轉服務搭配運作，請參閱「[指定排定查詢的加密金鑰](#CMEK)」。

```
bq update \
--target_dataset=dataset \
--display_name=name \
--params='parameters'
--transfer_config \
RESOURCE_NAME
```

更改下列內容：

* `dataset`。移轉設定的目標資料集。此參數對 DDL 和 DML 查詢而言為選用，但為其他所有查詢的必要參數。
* `name`. 移轉設定的顯示名稱。顯示名稱可以是任何值，方便您日後在必要時修改查詢。
* `parameters`。含有已建立移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。
  + 針對排程查詢，您必須提供 `query` 參數。
  + `destination_table_name_template` 參數是目的地資料表的名稱。此參數對 DDL 和 DML 查詢而言為選用，但為其他所有查詢的必要參數。
  + 針對 `write_disposition` 參數，您可以選擇 `WRITE_TRUNCATE` 來截斷 (覆寫) 目的地資料表，或選擇 `WRITE_APPEND` 將查詢結果附加到目的地資料表。此參數對 DDL 和 DML 查詢而言為選用，但為其他所有查詢的必要參數。
* 選用：`--destination_kms_key` 指定 Cloud KMS 金鑰的[金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)，例如 `projects/project_name/locations/us/keyRings/key_ring_name/cryptoKeys/key_name`。
* `RESOURCE_NAME`：移轉的資源名稱 (也稱為移轉設定)。如果您不知道移轉的資源名稱，請使用 [`bq ls --transfer_config --transfer_location=location`](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#list_transfer_configurations) 找出資源名稱。

**注意：**如要將結果寫入擷取時間分區資料表，請參閱[目的地資料表](#destination_table)一節的操作說明。如使用 `destination_table_name_template` 參數建立移轉設定，且此參數設定為擷取時間分區資料表，排定的查詢將會失敗；如果設定為擷取時間分區的 `partitioning_field` 參數，亦會產生錯誤。**注意：** 您無法使用指令列工具設定通知。

舉例來說，下列指令會使用查詢 `SELECT 1
from mydataset.test`，更新名為 `My Scheduled Query` 的排程查詢移轉作業設定。目的地資料表 `mytable` 每次寫入時皆會截斷，而目標資料集為 `mydataset`：

```
bq update \
--target_dataset=mydataset \
--display_name='My Scheduled Query' \
--params='{"query":"SELECT 1 from mydataset.test","destination_table_name_template":"mytable","write_disposition":"WRITE_TRUNCATE"}'
--transfer_config \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7
```

### API

請使用 [`projects.transferConfigs.patch`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.transferConfigs/patch?hl=zh-tw) 方法，並使用 `transferConfig.name` 參數提供轉移作業的資源名稱。如果您不知道移轉的資源名稱，請使用 [`bq ls --transfer_config --transfer_location=location`](#viewing_a_scheduled_query) 指令列出所有移轉，或呼叫 [`projects.locations.transferConfigs.list`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/list?hl=zh-tw) 方法，並使用 `parent` 參數提供專案 ID。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.cloud.bigquery.datatransfer.v1.UpdateTransferConfigRequest;
import com.google.protobuf.FieldMask;
import com.google.protobuf.util.FieldMaskUtil;
import java.io.IOException;

// Sample to update transfer config.
public class UpdateTransferConfig {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setName(configId)
            .setDisplayName("UPDATED_DISPLAY_NAME")
            .build();
    FieldMask updateMask = FieldMaskUtil.fromString("display_name");
    updateTransferConfig(transferConfig, updateMask);
  }

  public static void updateTransferConfig(TransferConfig transferConfig, FieldMask updateMask)
      throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      UpdateTransferConfigRequest request =
          UpdateTransferConfigRequest.newBuilder()
              .setTransferConfig(transferConfig)
              .setUpdateMask(updateMask)
              .build();
      TransferConfig updateConfig = dataTransferServiceClient.updateTransferConfig(request);
      System.out.println("Transfer config updated successfully :" + updateConfig.getDisplayName());
    } catch (ApiException ex) {
      System.out.print("Transfer config was not updated." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_datatransfer_v1
from google.protobuf import field_mask_pb2


client = bigquery_datatransfer_v1.DataTransferServiceClient()


def update_transfer_config(
    project_id: str,
    location: str,
    transfer_config_id: str,
) -> None:
    """Updates a data transfer configuration.

    This sample shows how to update the display name for a transfer
    configuration.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the transfer config, for example "us-central1"
        transfer_config_id: The transfer configuration ID
    """
    transfer_config_name = client.transfer_config_path(
        project=f"{project_id}/locations/{location}",
        transfer_config=transfer_config_id,
    )

    transfer_config = bigquery_datatransfer_v1.types.TransferConfig(
        name=transfer_config_name,
        display_name="My New Transfer Config display name",
    )
    update_mask = field_mask_pb2.FieldMask(paths=["display_name"])

    try:
        response = client.update_transfer_config(
            transfer_config=transfer_config,
            update_mask=update_mask,
        )

        print(f"Updated transfer config: {response.name}")
        print(f"New display name: {response.display_name}")
    except google.api_core.exceptions.NotFound:
        print(f"Error: Transfer config '{transfer_config_name}' not found.")
```

**注意：** 您無法更新排程查詢的位置。如果移動排程查詢中使用的來源或目的地資料集，則必須在新位置建立新的排程查詢。

### 更新設有擁有權限制的排程查詢

如果嘗試更新不屬於自己的排程查詢，更新可能會失敗，並顯示以下錯誤訊息：

`Cannot modify restricted parameters without taking ownership of the transfer configuration.`

排程查詢的擁有者是與排程查詢相關聯的使用者，或是可存取與排程查詢相關聯服務帳戶的使用者。您可以在排定查詢的設定詳細資料中查看相關聯的使用者。如要瞭解如何更新排程查詢，以便取得擁有權，請參閱「[更新排程查詢憑證](#update_scheduled_query_credentials)」。如要授予使用者服務帳戶存取權，您必須具備[服務帳戶使用者角色](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#user-role)。

排定查詢的擁有者受限參數如下：

* 查詢文字
* 目的地資料集
* 目的地資料表名稱範本

## 更新排定查詢的憑證

如果您是為既有的查詢進行排程，可能需要更新查詢中的使用者憑證。系統會自動為新的排程查詢更新憑證。

**注意：**更新憑證後，系統會以您的身分和權限執行查詢。確認查詢未遭他人修改，以存取只有您能查看的資源，否則可能導致未經授權存取私密資料。

其他可能需要更新憑證的情況包括：

* 您想在排定的查詢中[查詢 Google 雲端硬碟資料](https://docs.cloud.google.com/bigquery/external-data-drive?hl=zh-tw)。
* 嘗試排定查詢時，您會收到 **INVALID\_USER** 錯誤：

  `Error code 5 : Authentication failure: User Id not found. Error code: INVALID_USERID`
* 嘗試更新查詢時，您會收到下列受限參數錯誤：

  `Cannot modify restricted parameters without taking ownership of the transfer configuration.`

**注意：** 如果您不是排程查詢的擁有者，必須在 Google Cloud 專案中擁有 `bigquery.transfers.update` 權限，才能更新排程查詢的憑證。詳情請參閱「[必要權限](#required_permissions)」。

### 控制台

如要重新整理排程查詢上的現有憑證，請進行以下操作：

1. 找出並[查看排程查詢的狀態](#viewing_a_scheduled_query)。
2. 按一下 [MORE] (更多) 按鈕，然後選取 [Update credentials] (更新憑證)。
3. 變更需要 10 至 20 分鐘才會生效。你可能需要清除瀏覽器的快取。

**注意：** Google Cloud 控制台不支援將排程查詢從使用原有憑證變更使用服務帳戶。

### bq

排程查詢是一種移轉作業。如要更新排程查詢的憑證，您可以使用 bq 指令列工具更新移轉作業設定。

輸入 `bq update` 指令並加上移轉旗標 `--transfer_config`。還需加上以下旗標：

* `--update_credentials`

選用旗標：

* `--service_account_name` 是用於透過服務帳戶 (而非個別使用者帳戶) 來驗證排程查詢。

舉例來說，下列指令會更新排程查詢的移轉作業設定，並以服務帳戶身分進行驗證：

```
bq update \
--update_credentials \
--service_account_name=abcdef-test-sa@abcdef-test.iam.gserviceaccount.com \
--transfer_config \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.cloud.bigquery.datatransfer.v1.UpdateTransferConfigRequest;
import com.google.protobuf.FieldMask;
import com.google.protobuf.util.FieldMaskUtil;
import java.io.IOException;

// Sample to update credentials in transfer config.
public class UpdateCredentials {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    String serviceAccount = "MY_SERVICE_ACCOUNT";
    TransferConfig transferConfig = TransferConfig.newBuilder().setName(configId).build();
    FieldMask updateMask = FieldMaskUtil.fromString("service_account_name");
    updateCredentials(transferConfig, serviceAccount, updateMask);
  }

  public static void updateCredentials(
      TransferConfig transferConfig, String serviceAccount, FieldMask updateMask)
      throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      UpdateTransferConfigRequest request =
          UpdateTransferConfigRequest.newBuilder()
              .setTransferConfig(transferConfig)
              .setUpdateMask(updateMask)
              .setServiceAccountName(serviceAccount)
              .build();
      dataTransferServiceClient.updateTransferConfig(request);
      System.out.println("Credentials updated successfully");
    } catch (ApiException ex) {
      System.out.print("Credentials was not updated." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery_datatransfer
from google.protobuf import field_mask_pb2

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

service_account_name = "abcdef-test-sa@abcdef-test.iam.gserviceaccount.com"
transfer_config_name = "projects/1234/locations/us/transferConfigs/abcd"

transfer_config = bigquery_datatransfer.TransferConfig(name=transfer_config_name)

transfer_config = transfer_client.update_transfer_config(
    {
        "transfer_config": transfer_config,
        "update_mask": field_mask_pb2.FieldMask(paths=["service_account_name"]),
        "service_account_name": service_account_name,
    }
)

print("Updated config: '{}'".format(transfer_config.name))
```

## 設定過去日期的手動執行作業

除了排定查詢於日後執行，您也可以手動觸發立即執行作業。如果您的查詢使用 `run_date` 參數，且在先前執行期間發生問題，則可能需要觸發立即執行作業。

舉例來說，每天 09:00 您會在來源資料表中查詢符合目前日期的資料列。然而您發現系統在過去三天內，並未將這項資料加進來源資料表。在這種情況下，您可以將查詢設定為在指定日期範圍的歷史資料中執行。您的查詢在執行時，使用的 `run_date` 和 `run_time` 參數組合會對應到您排程查詢中所設的日期。

[設定排程查詢](#set_up_scheduled_queries)後，可按照以下步驟使用過去的日期範圍來執行查詢：

### 控制台

按一下「排程」儲存排程查詢後，您可以按一下「已排定的查詢」按鈕，查看排程查詢清單。按一下任何顯示名稱可查看該查詢的排程詳細資料。在頁面右上方，按一下 [Schedule Backfill] (排程補充作業)，即可指定過去的日期範圍。

所選的執行時間皆於您所選的範圍之內，這個範圍包含初次執行日期，並排除最後一次的日期。

**警告：** 您提供的日期範圍是以世界標準時間顯示，但是查詢的排程將以您的當地時區顯示 (如要避開此問題，請參考**範例 2**)。

**範例 1**

排程查詢設定在太平洋時間的 `every day 09:00` 執行，而您缺少 1 月 1 日、1 月 2 日和 1 月 3 日的資料。請選擇下列過去的日期範圍：

`Start Time = 1/1/19`  
`End Time = 1/4/19`

您的查詢會使用對應至下列時間的 `run_date` 和 `run_time` 參數執行：

* 1/1/19 09:00 太平洋時間
* 1/2/19 09:00 太平洋時間
* 1/3/19 09:00 太平洋時間

**示例 2**

排程查詢設定在太平洋時間的 `every day 23:00` 執行，而您缺少 1 月 1 日、1 月 2 日和 1 月 3 日的資料。請選擇下列過去的日期範圍 (由於太平洋時間的 23:00 與世界標準時間的日期不同，因此要選擇較晚的日期)：

`Start Time = 1/2/19`  
`End Time = 1/5/19`

您的查詢會使用對應至下列時間的 `run_date` 和 `run_time` 參數執行：

* 1/2/19 06:00 世界標準時間，或 1/1/2019 23:00 太平洋時間
* 1/3/19 06:00 世界標準時間，或 1/2/2019 23:00 太平洋時間
* 1/4/19 06:00 世界標準時間，或 1/3/2019 23:00 太平洋時間

設定手動執行作業後，請重新整理頁面，這些執行作業便會顯示在執行作業清單中。

### bq

如要針對過去的日期範圍手動執行查詢：

輸入 `bq mk` 指令並加上移轉執行作業旗標 `--transfer_run`。還需加上以下旗標：

* `--start_time`
* `--end_time`

```
bq mk \
--transfer_run \
--start_time='start_time' \
--end_time='end_time' \
resource_name
```

更改下列內容：

* `start_time`和`end_time`。
  以 Z 結尾或包含有效時區偏移的時間戳記。範例：
  + 2017-08-19T12:11:35.00Z
  + 2017-05-25T00:00:00+00:00
* `resource_name`。排程查詢 (或移轉作業) 的資源名稱。資源名稱也稱為移轉設定。

例如，下列指令會為排程查詢資源 (又稱為移轉作業設定) 排定補充作業：`projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7`。

```
  bq mk \
  --transfer_run \
  --start_time 2017-05-25T00:00:00Z \
  --end_time 2017-05-25T00:00:00Z \
  projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7
```

詳情請參閱「[`bq mk --transfer_run`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-transfer-run)」。

### API

使用 [projects.locations.transferConfigs.scheduleRun](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/scheduleRuns?hl=zh-tw) 方法並提供 [TransferConfig](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的路徑。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ScheduleTransferRunsRequest;
import com.google.cloud.bigquery.datatransfer.v1.ScheduleTransferRunsResponse;
import com.google.protobuf.Timestamp;
import java.io.IOException;
import org.threeten.bp.Clock;
import org.threeten.bp.Instant;
import org.threeten.bp.temporal.ChronoUnit;

// Sample to run schedule back fill for transfer config
public class ScheduleBackFill {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    Clock clock = Clock.systemDefaultZone();
    Instant instant = clock.instant();
    Timestamp startTime =
        Timestamp.newBuilder()
            .setSeconds(instant.minus(5, ChronoUnit.DAYS).getEpochSecond())
            .setNanos(instant.minus(5, ChronoUnit.DAYS).getNano())
            .build();
    Timestamp endTime =
        Timestamp.newBuilder()
            .setSeconds(instant.minus(2, ChronoUnit.DAYS).getEpochSecond())
            .setNanos(instant.minus(2, ChronoUnit.DAYS).getNano())
            .build();
    scheduleBackFill(configId, startTime, endTime);
  }

  public static void scheduleBackFill(String configId, Timestamp startTime, Timestamp endTime)
      throws IOException {
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
      ScheduleTransferRunsRequest request =
          ScheduleTransferRunsRequest.newBuilder()
              .setParent(configId)
              .setStartTime(startTime)
              .setEndTime(endTime)
              .build();
      ScheduleTransferRunsResponse response = client.scheduleTransferRuns(request);
      System.out.println("Schedule backfill run successfully :" + response.getRunsCount());
    } catch (ApiException ex) {
      System.out.print("Schedule backfill was not run." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import datetime

from google.cloud.bigquery_datatransfer_v1 import (
    DataTransferServiceClient,
    StartManualTransferRunsRequest,
)

# Create a client object
client = DataTransferServiceClient()

# Replace with your transfer configuration name
transfer_config_name = "projects/1234/locations/us/transferConfigs/abcd"
now = datetime.datetime.now(datetime.timezone.utc)
start_time = now - datetime.timedelta(days=5)
end_time = now - datetime.timedelta(days=2)

# Some data sources, such as scheduled_query only support daily run.
# Truncate start_time and end_time to midnight time (00:00AM UTC).
start_time = datetime.datetime(
    start_time.year, start_time.month, start_time.day, tzinfo=datetime.timezone.utc
)
end_time = datetime.datetime(
    end_time.year, end_time.month, end_time.day, tzinfo=datetime.timezone.utc
)

requested_time_range = StartManualTransferRunsRequest.TimeRange(
    start_time=start_time,
    end_time=end_time,
)

# Initialize request argument(s)
request = StartManualTransferRunsRequest(
    parent=transfer_config_name,
    requested_time_range=requested_time_range,
)

# Make the request
response = client.start_manual_transfer_runs(request=request)

# Handle the response
print("Started manual transfer runs:")
for run in response.runs:
    print(f"backfill: {run.run_time} run: {run.name}")
```

## 設定排程查詢的快訊

您可以根據資料列計數指標，為排程查詢設定警報政策。詳情請參閱「[使用排定查詢設定快訊](https://docs.cloud.google.com/bigquery/docs/create-alert-scheduled-query?hl=zh-tw)」。

## 刪除預定查詢

### 控制台

如要透過 Google Cloud 控制台的「Scheduled queries」(已排定的查詢) 頁面刪除排程查詢，請按照下列步驟操作：

1. 在導覽選單中，按一下「已排程的查詢」。
2. 在排定查詢清單中，按一下要刪除的排定查詢名稱。
3. 在「Scheduled query details」(已排定查詢詳細資料) 頁面，按一下「Delete」(刪除)。

或者，您也可以在 Google Cloud 控制台的「Scheduling」(排程) 頁面中刪除排程查詢：

1. 在導覽選單中，按一下「排程」。
2. 在排程查詢清單中，點選要刪除的排程查詢的「動作」選單 more\_vert。
3. 選取 [刪除]。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。