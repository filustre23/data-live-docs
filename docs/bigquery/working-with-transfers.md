Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理轉移作業

本文說明如何管理現有的資料移轉設定。

您也可以[手動觸發現有轉移作業](#manually_trigger_a_transfer)，也就是啟動*補充執行*。

## 查看轉移作業

查看現有的移轉設定，方法是查看每項移轉作業的相關資訊、列出所有現有的移轉作業，以及查看移轉作業的執行記錄或記錄訊息。

### 必要的角色

如要取得查看移轉詳細資料所需的權限，請要求管理員授予您專案的「[BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user) 」(`roles/bigquery.user`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

此外，如要透過 Google Cloud 控制台查看記錄訊息，您必須具備查看 Cloud Logging 資料的權限。「記錄檢視者」角色 (`roles/logging.viewer`) 可讓您以唯讀存取 Logging 的所有功能。如要進一步瞭解適用於 Cloud 記錄資料的 Identity and Access Management (IAM) 權限和角色，請參閱 Cloud Logging [存取權控管指南](https://docs.cloud.google.com/logging/docs/access-control?hl=zh-tw)。

如要進一步瞭解 BigQuery 資料移轉服務中的 IAM 角色，請參閱[存取權控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

### 取得轉移詳細資料

您可以在建立移轉後，取得移轉設定的相關資訊。這些設定包括您在建立移轉時提供的值，以及其他重要資訊，例如資源名稱。

如何取得移轉設定的相關資訊：

### 控制台

1. 前往「資料轉移」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 選取要查看詳細資料的轉移作業。
3. 如要查看移轉設定和資料來源詳細資料，請在「Transfer details」(移轉作業詳細資料) 頁面中，按一下「Configuration」(設定)。以下範例顯示 Google Ads 移轉的設定屬性：

### bq

輸入 `bq show` 指令並提供移轉設定的資源名稱。`--format` 標記可用來控管輸出格式。

```
bq show \
--format=prettyjson \
--transfer_config resource_name
```

將 `resource_name` 替換為移轉的資源名稱 (也稱為移轉設定)。如果您不知道移轉的資源名稱，請使用以下指令找出資源名稱：
[`bq ls --transfer_config --transfer_location=location`](#list_transfer_configurations)。

例如，輸入下列指令來顯示 `projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7` 的移轉設定。

```
bq show \
--format=prettyjson \
--transfer_config projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7
```

### API

使用 [`projects.locations.transferConfigs.get`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/get?hl=zh-tw) 方法，並使用 `name` 參數提供轉移設定。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.GetTransferConfigRequest;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import java.io.IOException;

// Sample to get config info.
public class GetTransferConfigInfo {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    // i.e projects/{project_id}/transferConfigs/{config_id}` or
    // `projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}`
    getTransferConfigInfo(configId);
  }

  public static void getTransferConfigInfo(String configId) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      GetTransferConfigRequest request =
          GetTransferConfigRequest.newBuilder().setName(configId).build();
      TransferConfig info = dataTransferServiceClient.getTransferConfig(request);
      System.out.print("Config info retrieved successfully." + info.getName() + "\n");
    } catch (ApiException ex) {
      System.out.print("config not found." + ex.toString());
    }
  }
}
```

### 列出移轉設定

如要列出專案中所有現有的移轉設定：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 如果專案中有任何移轉設定，資料移轉清單會顯示移轉設定清單。

### bq

如要按照位置列出專案的所有移轉設定，請輸入 `bq ls` 指令並提供 `--transfer_location` 和 `--transfer_config` 標記。您還可以提供 `--project_id` 標記來指定特定專案。如果未指定 `--project_id`，系統會使用預設專案。`--format` 標記可用來控管輸出格式。

如要列出特定資料來源的移轉設定，請提供 `--filter` 標記。

如要以分頁格式查看特定數量的移轉設定，請提供 `--max_results` 標記來指定移轉次數。這個指令會傳回您使用 `--page_token` 旗標提供的頁面符記，以便查看下 n 個設定。如果省略 `--max_results`，系統最多會傳回 1000 項設定，且 `--max_results` 不會接受大於 1000 的值。如果專案有超過 1000 個設定，請使用 `--max_results` 和 `--page_token` 逐一查看所有設定。

```
bq ls \
--transfer_config \
--transfer_location=location \
--project_id=project_id \
--max_results=integer \
--filter=dataSourceIds:data_sources
```

更改下列內容：

* `location` 是移轉設定的位置。此[位置](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw#supported_regions)是您在建立移轉時指定的位置。
* `project_id` 是您的專案 ID。
* `integer` 是每頁顯示的結果數。
* `data_sources` 是下列一或多項：
  + `amazon_s3` - [Amazon S3 資料移轉](https://docs.cloud.google.com/bigquery/docs/s3-transfer?hl=zh-tw#bq)
  + `azure_blob_storage` - [Azure Blob 儲存體資料移轉](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer?hl=zh-tw#bq)
  + `dcm_dt` - [Campaign Manager 資料移轉](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw#set_up_a_campaign_manager_transfer)
  + `google_cloud_storage` - [Cloud Storage 資料移轉](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw#set_up_a_cloud_storage_transfer)
  + `cross_region_copy` - [資料集副本](https://docs.cloud.google.com/bigquery/docs/copying-datasets?hl=zh-tw)
  + `dfp_dt`- [Google Ad Manager 資料移轉](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transfer?hl=zh-tw#set_up_a_google_ad_manager_transfer)
  + `displayvideo`- [Display & Video 360 資料移轉](https://docs.cloud.google.com/bigquery/docs/display-video-transfer?hl=zh-tw)
  + `google_ads` - [Google Ads 資料移轉](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)
  + `merchant_center` - [Google Merchant Center 資料移轉](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer-schedule-transfers?hl=zh-tw)
  + `mysql` - [MySQL 資料移轉](https://docs.cloud.google.com/bigquery/docs/mysql-transfer?hl=zh-tw#set-up-a-mysql-data-transfer)
  + `play` - [Google Play 資料移轉](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw#setup-transfer)
  + `scheduled_query` - [已排定查詢的資料移轉](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)
  + `search_ads`- [Search Ads 360 資料移轉](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw)
  + `youtube_channel` - [YouTube 頻道資料移轉](https://docs.cloud.google.com/bigquery/docs/youtube-channel-transfer?hl=zh-tw#set_up_a_youtube_channel_transfer)
  + `youtube_content_owner` - [YouTube 內容擁有者資料移轉](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw#set_up_a_youtube_content_owner_transfer)
  + `redshift` - [Amazon Redshift 遷移](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw#set-up-transfer)
  + `on_premises` - [Teradata 遷移](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw)

範例：

輸入下列指令，顯示您預設專案中所有位於美國的移轉設定。使用 `--format` 標記控制輸出。

```
bq ls \
--format=prettyjson \
--transfer_config \
--transfer_location=us
```

輸入下列指令，顯示專案 ID `myproject` 在美國的所有移轉設定。

```
bq ls \
--transfer_config \
--transfer_location=us \
--project_id=myproject
```

輸入下列指令，列出 3 個最近的移轉設定。

```
bq ls \
--transfer_config \
--transfer_location=us \
--project_id=myproject \
--max_results=3
```

這個指令會傳回下一頁憑證。複製頁面權杖並在 `bq ls` 指令中提供，即可查看下 3 個結果。

```
bq ls \
--transfer_config \
--transfer_location=us \
--project_id=myproject \
--max_results=3 \
--page_token=AB1CdEfg_hIJKL
```

輸入下列指令，列出專案 ID `myproject` 的 Google Ads 和 Campaign Manager 移轉設定。

```
bq ls \
--transfer_config \
--transfer_location=us \
--project_id=myproject \
--filter=dataSourceIds:dcm_dt,google_ads
```

### API

請使用 [`projects.locations.transferConfigs.list`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/list?hl=zh-tw) 方法，並透過 `parent` 參數提供專案 ID。

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

### 查看移轉執行記錄

在執行排定的移轉作業時，系統會為每個移轉設定都保留一個執行紀錄，當中包含成功的移轉執行和失敗的移轉執行。已超過 90 天的移轉執行作業會自動從執行記錄中刪除。

如何查看移轉設定的執行記錄：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 在資料移轉清單中，按一下要查看的移轉作業。
3. 系統會將您帶往所選移轉作業的「執行記錄」頁面。

### bq

如要列出特定移轉設定的移轉執行作業，請輸入 `bq
ls` 指令並提供 `--transfer_run` 標記。您還可以提供 `--project_id` 標記來指定特定專案。如果 resource\_name 不含專案資訊，系統會使用 `--project_id` 值。如未指定 `--project_id`，系統會使用預設專案。`--format` 標記可用來控管輸出格式。

如要查看特定數量的移轉執行作業，請提供 `--max_results` 標記。這個指令會傳回您使用 `--page_token` 旗標提供的頁面符記，以便查看下 n 個設定。

如要根據執行狀態列出移轉執行作業，請提供 `--filter` 標記。

```
bq ls \
--transfer_run \
--max_results=integer \
--transfer_location=location \
--project_id=project_id \
--filter=states:state, ... \
resource_name
```

更改下列內容：

* `integer` 是要傳回的結果數。
* `location` 是移轉設定的位置。此[位置](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw#supported_regions)是您在建立移轉時指定的位置。
* `project_id` 是您的專案 ID。
* `state, ...` 是下列其中一種或逗號分隔的清單：
  + `SUCCEEDED`
  + `FAILED`
  + `PENDING`
  + `RUNNING`
  + `CANCELLED`
* `resource_name` 是移轉的資源名稱，也稱為移轉設定。如果您不知道移轉的資源名稱，請使用 [`bq ls --transfer_config --transfer_location=location`](#list_transfer_configurations) 找出資源名稱。

範例：

輸入下列指令，顯示移轉設定 `projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7` 最近 3 次的執行作業。使用 `--format` 標記控制輸出。

```
bq ls \
--format=prettyjson \
--transfer_run \
--max_results=3 \
--transfer_location=us \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7
```

這個指令會傳回下一頁憑證。複製頁面權杖並在 `bq ls` 指令中提供，即可查看下 3 個結果。

```
bq ls \
--format=prettyjson \
--transfer_run \
--max_results=3 \
--page_token=AB1CdEfg_hIJKL \
--transfer_location=us \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7
```

輸入下列指令，顯示移轉設定 `projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7` 所有失敗的執行作業。

```
bq ls \
--format=prettyjson \
--transfer_run \
--filter=states:FAILED \
--transfer_location=us \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7
```

### API

使用 [`projects.locations.transferConfigs.runs.list`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs.runs/list?hl=zh-tw) 方法，並使用 `parent` 參數指定專案 ID。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ListTransferRunsRequest;
import java.io.IOException;

// Sample to get run history from transfer config.
public class RunHistory {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    // i.e projects/{project_id}/transferConfigs/{config_id}` or
    // `projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}`
    runHistory(configId);
  }

  public static void runHistory(String configId) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      ListTransferRunsRequest request =
          ListTransferRunsRequest.newBuilder().setParent(configId).build();
      dataTransferServiceClient
          .listTransferRuns(request)
          .iterateAll()
          .forEach(run -> System.out.print("Success! Run ID :" + run.getName() + "\n"));
    } catch (ApiException ex) {
      System.out.println("Run history not found due to error." + ex.toString());
    }
  }
}
```

### 查看移轉執行作業的詳細資料與記錄訊息

當移轉執行作業出現在執行記錄中時，即可查看執行作業的詳細資料，包括記錄訊息、警告和錯誤、執行作業名稱及開始和結束時間等。

如何查看移轉執行詳細資料：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 在資料移轉清單中，按一下要查看的移轉作業。
3. 系統會將您帶往所選移轉作業的「執行記錄」頁面。
4. 按一下個別移轉作業，即可開啟該移轉作業的「執行詳細資料」面板。
5. 在「執行詳細資料」中，記下任何錯誤訊息。與 Cloud Customer Care 團隊聯絡時必須提供這些資訊。執行作業詳細資料還包括記錄訊息和警告。

### bq

如要查看移轉執行作業的詳細資料，請輸入 `bq show` 指令並使用 `--transfer_run` 標記提供移轉執行作業的執行作業名稱。`--format` 標記可用來控管輸出格式。

```
bq show \
--format=prettyjson \
--transfer_run run_name
```

將 `run_name` 替換為移轉執行的執行名稱。
您可以使用 [`bq ls`](#view_the_run_history) 指令來擷取執行作業名稱。

範例：

輸入下列指令，顯示移轉執行作業 `projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7/runs/1a2b345c-0000-1234-5a67-89de1f12345g` 的詳細資料。

```
bq show \
--format=prettyjson \
--transfer_run \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7/runs/1a2b345c-0000-1234-5a67-89de1f12345g
```

如要查看移轉執行作業的移轉記錄訊息，請輸入 `bq ls` 指令並搭配使用 `--transfer_log` 標記。您可以使用 `--message_type` 旗標，依類型篩選記錄訊息。

如要查看特定數量的記錄訊息，請提供 `--max_results` 旗標。這個指令會傳回您使用 `--page_token` 旗標提供的頁面符記，以便查看下 n 則訊息。

```
bq ls \
--transfer_log \
--max_results=integer \
--message_type=messageTypes:message_type \
run_name
```

更改下列內容：

* `integer` 是要傳回的記錄訊息數。
* `message_type` 是要查看的記錄訊息類型 (單一值或逗號分隔的清單)：
  + `INFO`
  + `WARNING`
  + `ERROR`
* `run_name` 是移轉執行的執行名稱。您可以使用 [`bq ls`](#view_the_run_history) 指令來擷取執行作業名稱。

範例：

輸入下列指令來查看以下移轉執行作業的前 2 個記錄訊息：`projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7/runs/1a2b345c-0000-1234-5a67-89de1f12345g`。

```
bq ls \
--transfer_log \
--max_results=2 \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7/runs/1a2b345c-0000-1234-5a67-89de1f12345g
```

這個指令會傳回下一頁憑證。複製頁面權杖並在 `bq ls` 指令中提供，即可查看下 2 個結果。

```
bq ls \
--transfer_log \
--max_results=2 \
--page_token=AB1CdEfg_hIJKL \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7/runs/1a2b345c-0000-1234-5a67-89de1f12345g
```

輸入下列指令，即可只查看轉移作業 `projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7/runs/1a2b345c-0000-1234-5a67-89de1f12345g` 的錯誤訊息。

```
bq ls \
--transfer_log \
--message_type=messageTypes:ERROR \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7/runs/1a2b345c-0000-1234-5a67-89de1f12345g
```

### API

使用 [`projects.transferConfigs.runs.transferLogs.list`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.transferConfigs.runs.transferLogs/list?hl=zh-tw) 方法，並使用 `parent` 參數提供移轉執行的執行名稱。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.GetTransferRunRequest;
import com.google.cloud.bigquery.datatransfer.v1.TransferRun;
import java.io.IOException;

// Sample to get run details from transfer config.
public class RunDetails {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    // runId examples:
    // `projects/{project_id}/transferConfigs/{config_id}/runs/{run_id}` or
    // `projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}/runs/{run_id}`
    String runId = "MY_RUN_ID";
    runDetails(runId);
  }

  public static void runDetails(String runId) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      GetTransferRunRequest request = GetTransferRunRequest.newBuilder().setName(runId).build();
      TransferRun run = dataTransferServiceClient.getTransferRun(request);
      System.out.print("Run details retrieved successfully :" + run.getName() + "\n");
    } catch (ApiException ex) {
      System.out.print("Run details not found." + ex.toString());
    }
  }
}
```

## 修改轉移作業

您可以編輯轉移設定中的資訊、更新附加至轉移設定的使用者憑證，以及停用或刪除轉移作業，藉此修改現有的轉移作業。

### 必要的角色

如要取得修改移轉作業所需的權限，請要求管理員授予您專案的「[BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) 」(`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

### 更新移轉

建立移轉設定後，您可以編輯下列欄位：

* 目的地資料集
* 顯示名稱
* 任何為特定移轉類型指定的參數
* 執行作業通知設定
* 服務帳戶

移轉作業建立後，就無法編輯來源。

如何更新移轉：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 在資料移轉清單中，按一下要查看的移轉作業。
3. 按一下「編輯」即可更新移轉設定。

### bq

輸入 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)，使用 `--transfer_config` 標記提供移轉設定的資源名稱，並提供 `--display_name`、`--params`、`--refresh_window_days`、`--schedule` 或 `--target_dataset` 標記。您可以選擇性地為[排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)或 [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw) 移轉作業提供 `--destination_kms_key` 旗標。

```
bq update \
--display_name='NAME' \
--params='PARAMETERS' \
--refresh_window_days=INTEGER \
--schedule='SCHEDULE'
--target_dataset=DATASET_ID \
--destination_kms_key="DESTINATION_KEY" \
--transfer_config \
--service_account_name=SERVICE_ACCOUNT \
RESOURCE_NAME
```

更改下列內容：

* `NAME`：移轉設定的顯示名稱。
* `PARAMETERS`：移轉設定的 JSON 格式參數。例如：`--params='{"param1":"param_value1"}'`。如要瞭解支援的參數，請參閱資料來源的轉移指南。
* `INTEGER`：0 到 30 之間的值。如要瞭解如何設定重新整理視窗，請參閱相關移轉類型的說明文件。
* `SCHEDULE`：週期性排程，例如 `--schedule="every 3 hours"`。如要瞭解 `schedule` 語法，請參閱「[設定 `schedule` 格式](https://docs.cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml?hl=zh-tw#formatting_the_schedule)」。
* DATASET\_ID：移轉設定的目標資料集。
* DESTINATION\_KEY：[Cloud KMS 金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)，例如 `projects/project_name/locations/us/keyRings/key_ring_name/cryptoKeys/key_name`。
  CMEK 僅適用於[排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)或 [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw) 移轉作業。
* SERVICE\_ACCOUNT：指定要用於這項轉移作業的服務帳戶。
* RESOURCE\_NAME：移轉的資源名稱，也稱為移轉設定。如果您不知道移轉的資源名稱，請使用 [`bq ls --transfer_config --transfer_location=location`](#list_transfer_configurations) 找出資源名稱。

**注意：** 您無法使用 bq 工具更新通知設定。

範例：

下列指令會更新 Google Ads 移轉作業 `projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7` 的顯示名稱、目標資料集、重新整理時間範圍和參數：

```
bq update \
--display_name='My changed transfer' \
--params='{"customer_id":"123-123-5678"}' \
--refresh_window_days=3 \
--target_dataset=mydataset2 \
--transfer_config \
 projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7
```

下列指令會更新排程查詢移轉作業 `projects/myproject/locations/us/transferConfigs/5678z567-5678-5z67-5yx9-56zy3c866vw9` 的參數和排程：

```
bq update \
--params='{"destination_table_name_template":"test", "write_disposition":"APPEND"}' \
--schedule="every 24 hours" \
--transfer_config \
projects/myproject/locations/us/transferConfigs/5678z567-5678-5z67-5yx9-56zy3c866vw9
```

### API

請使用 [`projects.transferConfigs.patch`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.transferConfigs/patch?hl=zh-tw) 方法，並使用 `transferConfig.name` 參數提供轉移作業的資源名稱。如果您不知道移轉的資源名稱，請使用以下指令找出資源名稱：
[`bq ls --transfer_config --transfer_location=location`](#list_transfer_configurations)。
您也可以呼叫下列方法，並使用 `parent` 參數提供專案 ID，列出所有轉移作業：[`projects.locations.transferConfigs.list`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/list?hl=zh-tw)。

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

### 更新憑證

移轉使用的憑證為建立該移轉的使用者的憑證。如您需要變更移轉設定所連結的使用者，您可以更新移轉的憑證。當建立移轉的使用者已不在您的組織時，這個方法十分實用。

如何更新移轉的憑證：

### 控制台

1. 在 Google Cloud 控制台中，以要轉移擁有權的使用者身分登入。
2. 前往「資料轉移」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
3. 在資料移轉清單中，按一下要查看的移轉作業。
4. 按一下「更多」選單，然後選取「重新整理憑證」。
5. 按一下「允許」，讓 BigQuery 資料移轉服務有權查看您的報表資料，以及存取並管理 BigQuery 中的資料。

### bq

輸入 `bq update` 指令並用 `--transfer_config` 標記提供移轉設定的資源名稱，以及提供 `--update_credentials` 標記。

```
bq update \
--update_credentials=boolean \
--transfer_config \
resource_name
```

更改下列內容：

* `boolean` 是一個表示是否應為移轉設定更新憑證的布林值。
* `resource_name` 是移轉的資源名稱，也稱為移轉設定。如果您不知道移轉的資源名稱，請使用 [`bq ls --transfer_config --transfer_location=location`](#list_transfer_configurations) 找出資源名稱。

範例：

輸入下列指令來更新以下 Google Ads 移轉的憑證：`projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7`。

```
bq update \
--update_credentials=true \
--transfer_config \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7
```

### API

請使用 [`projects.transferConfigs.patch`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.transferConfigs/patch?hl=zh-tw) 方法，並提供 `authorizationCode` 和 `updateMask` 參數。

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

### 停用移轉

停用轉移作業後，系統會在轉移作業名稱中加入 disabled。
停用轉移功能後，系統不會再排定新的轉移作業，也不允許新的回填作業。正在進行中的移轉執行將會如常完成。

停用移轉並**不會**移除任何已經移轉至 BigQuery 的資料。先前已移轉的資料會產生標準的 BigQuery [儲存空間費用](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)，直到您[刪除資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#delete_a_dataset)或[刪除資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#deleting_tables)為止。

如何停用移轉：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 [Transfers] (傳輸作業)。
3. 在「Transfers」(傳輸作業) 頁面中，按一下要停用的移轉項目。
4. 按一下「停用」。如要重新啟用轉移功能，請按一下「啟用」。

### bq

CLI 不支援停用移轉。

### API

使用 [`projects.locations.transferConfigs.patch`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/patch?hl=zh-tw) 方法，並在 `projects.locations.transferConfig` 資源中將 `disabled` 設為 `true`。

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

// Sample to disable transfer config.
public class DisableTransferConfig {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    TransferConfig transferConfig =
        TransferConfig.newBuilder().setName(configId).setDisabled(true).build();
    FieldMask updateMask = FieldMaskUtil.fromString("disabled");
    disableTransferConfig(transferConfig, updateMask);
  }

  public static void disableTransferConfig(TransferConfig transferConfig, FieldMask updateMask)
      throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      UpdateTransferConfigRequest request =
          UpdateTransferConfigRequest.newBuilder()
              .setTransferConfig(transferConfig)
              .setUpdateMask(updateMask)
              .build();
      TransferConfig updateConfig = dataTransferServiceClient.updateTransferConfig(request);
      System.out.println("Transfer config disabled successfully :" + updateConfig.getDisplayName());
    } catch (ApiException ex) {
      System.out.print("Transfer config was not disabled." + ex.toString());
    }
  }
}
```

如要重新啟用轉移功能，請按照下列步驟操作：

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
/*
 * Copyright 2020 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.example.bigquerydatatransfer;

import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.cloud.bigquery.datatransfer.v1.UpdateTransferConfigRequest;
import com.google.protobuf.FieldMask;
import com.google.protobuf.util.FieldMaskUtil;
import java.io.IOException;

// Sample to disable transfer config.
public class DisableTransferConfig {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    TransferConfig transferConfig =
        TransferConfig.newBuilder().setName(configId).setDisabled(true).build();
    FieldMask updateMask = FieldMaskUtil.fromString("disabled");
    disableTransferConfig(transferConfig, updateMask);
  }

  public static void disableTransferConfig(
```