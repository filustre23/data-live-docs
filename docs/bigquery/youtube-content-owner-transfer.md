Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 YouTube 內容擁有者資料載入 BigQuery

您可以使用 YouTube 內容擁有者連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將 YouTube 內容擁有者資料載入 BigQuery。您可以使用 BigQuery 資料移轉服務，排定週期性移轉工作，將 YouTube 內容擁有者的最新資料新增至 BigQuery。

## 連接器總覽

YouTube 內容擁有者連結器的 BigQuery 資料移轉服務支援下列資料移轉選項。

| 資料轉移方式 | 支援 |
| --- | --- |
| 受支援的報表 | YouTube 內容擁有者連結器支援從下列報表移轉資料：    * [內容擁有者報告](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw) * 系統代管報表：   + [總覽](https://developers.google.com/youtube/reporting/v1/reports/system_managed/reports?hl=zh-tw)   + [報告](https://developers.google.com/youtube/reporting/v1/reports/system_managed/reports?hl=zh-tw)   + [欄位](https://developers.google.com/youtube/reporting/v1/reports/system_managed/fields?hl=zh-tw)   YouTube 內容擁有者連接器支援 [2018 年 6 月 18 日](https://developers.google.com/youtube/reporting/revision_history?hl=zh-tw#june-18,-2018)的 API 版本。  如要瞭解 YouTube 內容擁有者報表如何轉換成 BigQuery 資料表和檢視表，請參閱「[YouTube 內容擁有者報表轉換](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transformation?hl=zh-tw)」。 |
| 重複頻率 | YouTube 內容擁有者連接器支援每日資料轉移。    根據預設，資料移轉作業會在建立時排定時間。[設定資料移轉作業](#set_up_a_youtube_content_owner_transfer)時，你可以設定資料移轉時間。 |
| 重新整理時間範圍 | YouTube 內容擁有者連接器會在資料移轉作業執行時，擷取最多 1 天的 YouTube 內容擁有者資料。   詳情請參閱「[重新整理時間範圍](#refresh)」。 |
| 資料補充作業的可用性 | [執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，擷取排定資料移轉時間以外的資料。您可以擷取資料來源資料保留政策允許的最早資料。    包含歷來資料的 YouTube 報表在產生後可保留 30 天 (不含歷來資料的報表可保留 60 天)。詳情請參閱「[歷來資料](https://developers.google.com/youtube/reporting/v1/reports/?hl=zh-tw#historical-data)」。 |

## 從 YouTube 內容擁有者轉移作業擷取資料

將 YouTube 內容擁有者報表中的資料移轉至 BigQuery 時，資料會載入按日期分區的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果為同一天排定多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該特定日期的資料分割。同一天內進行多次轉移或執行回填作業，不會導致資料重複，也不會影響其他日期的分區。

### 重新整理視窗

*更新期*是指資料移轉作業在進行時，擷取資料的天數。舉例來說，如果重新整理時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務就會從來源資料表擷取過去三天的所有資料。在這個範例中，每天進行移轉時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分割區，並複製當天的來源資料表資料，然後自動觸發補充作業執行作業，以更新過去兩天的來源資料表資料。系統自動觸發的回填作業會覆寫或增量更新 BigQuery 目的地資料表，具體做法取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。舉例來說，如果重新整理時間範圍為三天，而您是第一次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

如要擷取重新整理時間範圍外的資料 (例如歷來資料)，或從任何轉移中斷或缺漏中復原資料，可以啟動或排定[補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 限制

* 資料移轉作業的最低排程頻率為每 24 小時一次。根據預設，資料移轉作業會在您建立資料移轉作業時啟動。不過，您可以在[設定轉移作業](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw#set_up_a_youtube_content_owner_transfer)時，設定轉移開始時間。
* 在 YouTube 內容擁有者移轉期間，BigQuery 資料移轉服務不支援增量資料移轉。指定資料移轉日期後，系統會移轉該日期可用的所有資料。

## 事前準備

建立 YouTube 內容擁有者資料移轉作業前，請先完成下列事項：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存 YouTube 資料。
* 確認您擁有 [YouTube 內容擁有者](https://support.google.com/youtube/answer/6301188?hl=zh-tw)帳戶。YouTube 內容擁有者與 YouTube 頻道並不相同。
  一般來說，只有在必須管理多個不同的頻道時，您才需要擁有 YouTube 內容擁有者帳戶。
* 如果您想要為 Pub/Sub 設定移轉作業執行通知，您必須擁有`pubsub.topics.setIamPolicy` 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

## 所需權限

確認您已授予下列權限。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求系統管理員在專案中授予您 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立 BigQuery 資料移轉服務資料移轉作業，您必須具備下列權限：

* BigQuery 資料移轉服務權限：
  + `bigquery.transfers.update`
  + `bigquery.transfers.get`
* BigQuery 權限：
  + `bigquery.datasets.get`
  + `bigquery.datasets.getIamPolicy`
  + `bigquery.datasets.update`
  + `bigquery.datasets.setIamPolicy`
  + `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

詳情請參閱「[授予 `bigquery.admin` 存取權](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#grant_bigqueryadmin_access)」。

### 必要的 YouTube 角色

* YouTube 內容管理員或 YouTube 內容擁有者。

  內容管理員具有為內容擁有者管理 YouTube 內容的權限。內容擁有者是一種綜合帳戶，這個帳戶擁有一個或多個 YouTube 頻道，以及這些頻道中的影片。
* YouTube 內容擁有者報表設定中的 `Hide revenue data` 已取消勾選。

  如要移轉收益相關報表，您必須為建立移轉作業的使用者取消勾選 YouTube 報表權限設定中的 `Hide revenue data`。

## 設定 YouTube 內容擁有者轉移作業

如要設定 YouTube 內容擁有者資料移轉作業，您需要下列項目：

* **內容擁有者 ID**：由 YouTube 提供。以內容擁有者或管理員身分登入 YouTube 時，您的 ID 會顯示在網址的 `o=` 後方。舉例來說，如果網址為 `https://studio.youtube.com/owner/AbCDE_8FghIjK?o=AbCDE_8FghIjK`，則內容擁有者 ID 為 `AbCDE_8FghIjK`。如要選取其他內容管理工具帳戶，請參閱「[登入內容管理工具帳戶](https://support.google.com/youtube/answer/6301172?hl=zh-tw)」或「[YouTube 頻道切換器](https://www.youtube.com/channel_switcher?hl=zh-tw)」。如要進一步瞭解如何建立及管理內容管理工具帳戶，請參閱「[設定內容管理工具帳戶設定](https://support.google.com/youtube/topic/6032636?hl=zh-tw)」。
* **資料表後置字串**：您在設定移轉作業時為頻道提供的易記名稱。後置字串會附加在工作 ID 後方，形成資料表名稱，例如 reportTypeId\_suffix。後置字串可用於防止不同的資料移轉作業寫入同一個資料表。所有將資料載入同個資料集的移轉工作，其資料表後置字串都不能重複，且後置字串應盡量簡短，避免產生過於冗長的資料表名稱。

如果您使用 [YouTube Reporting API](https://developers.google.com/youtube/reporting/v1/reference/rest/?hl=zh-tw)，並且已經有一些報表工作，BigQuery 資料移轉服務會載入您的報表資料。如果沒有現有的報表工作，設定資料移轉時，系統會自動啟用 YouTube 報表工作。

如要設定 YouTube 內容擁有者資料移轉作業：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。確認你已登入帳戶，且身分是內容擁有者或內容管理員。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 [Transfers] (傳輸作業)。
3. 按一下 [Create Transfer] (建立移轉作業)。
4. 在「Create Transfer」(建立轉移作業) 頁面：

   * 在「Source type」(來源類型) 區段中，針對「Source」(來源)，選擇 [YouTube Content Owner] (YouTube 內容擁有者)。
   * 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
   * 在「Schedule options」(排程選項) 專區：

     + 在「Repeat frequency」(重複頻率) 部分選取選項，指定資料移轉作業的執行頻率。如果選取「Days」(天)，請按照世界標準時間提供有效的值。
     + 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
   * 在「Destination settings」(目的地設定) 部分，「Destination dataset」(目的地資料集) 請選取您為了儲存資料而建立的資料集。
   * 在「Data source details」(資料來源詳細資料) 區段：

     + 於「Content Owner ID」(內容擁有者 ID) 部分輸入您的內容擁有者 ID。
     + 在「Table Suffix」(資料表後置字串) 部分，輸入後置字串，例如 `MT`。
   * 在「Service Account」(服務帳戶) 選單，選取與貴組織 Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與資料移轉作業建立關聯，這樣就不需要使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。

     如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立資料移轉作業。如果以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立資料移轉作業。服務帳戶必須具備[必要權限](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw#required_permissions)。
   * (選用) 在「Notification options」(通知選項) 區段中：

     + 點選切換按鈕，啟用電子郵件通知。啟用這個選項之後，若資料移轉失敗，移轉作業管理員就會收到電子郵件通知。
     + 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
5. 按一下 [儲存]。
6. 如果您是第一次登入帳戶，請選取帳戶並點選「Allow」(允許)。請選取您是內容擁有者或內容管理員的帳戶。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。還需加上以下旗標：

* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

選用標記：

* `--service_account_name`：指定要用於內容擁有者轉移驗證的服務帳戶，而非使用者帳戶。

```
bq mk \
--transfer_config \
--project_id=project_id \
--target_dataset=dataset \
--display_name=name \
--params='parameters' \
--data_source=data_source \
--service_account_name=service_account_name
```

其中：

* project\_id 是您的專案 ID。
* dataset 是移轉設定的目標資料集。
* name 是移轉設定的顯示名稱。資料移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* parameters 含有已建立移轉設定的 JSON 格式參數，例如：`--params='{"param":"param_value"}'`。進行 YouTube 內容擁有者資料移轉時，您必須提供 `content_owner_id` 和 `table_suffix` 參數。您可以選擇將 `configure_jobs` 參數設為 `true`，讓 BigQuery 資料移轉服務為您管理 YouTube 報表工作。如果有些 YouTube 報告不存在您的帳戶中，您必須建立新的報告工作才能啟用移轉功能。
* data\_source 是資料來源：`youtube_content_owner`。
* service\_account\_name 是用於驗證資料移轉作業的服務帳戶名稱。服務帳戶應由用於建立轉移作業的 `project_id` 擁有，且應具備所有[必要權限](#required_permissions)。

**注意：** 您無法使用指令列工具設定通知。

您還可以提供 `--project_id` 標記來指定特定專案。如果未指定 `--project_id`，系統會採用預設專案。

舉例來說，下列指令會使用內容擁有者 ID `AbCDE_8FghIjK`、資料表後置字串 `MT` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 YouTube 內容擁有者資料移轉作業。資料移轉作業會在預設專案中建立：

```
bq mk \
--transfer_config \
--target_dataset=mydataset \
--display_name='My Transfer' \
--params='{"content_owner_id":"abCDE_8FghIjK","table_suffix":"MT","configure_jobs":"true"}' \
--data_source=youtube_content_owner
```

**注意：** 使用指令列工具建立 YouTube 內容擁有者資料移轉作業時，系統會採用「Schedule」(排程) 的[預設值](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw#connector_overview)進行移轉設定。

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

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

// Sample to create youtube content owner channel transfer config
public class CreateYoutubeContentOwnerTransfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    String contentOwnerId = "MY_CONTENT_OWNER_ID";
    String tableSuffix = "_test";
    Map<String, Value> params = new HashMap<>();
    params.put("content_owner_id", Value.newBuilder().setStringValue(contentOwnerId).build());
    params.put("table_suffix", Value.newBuilder().setStringValue(tableSuffix).build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Youtube Owner Channel Config Name")
            .setDataSourceId("youtube_content_owner")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .build();
    createYoutubeContentOwnerTransfer(projectId, transferConfig);
  }

  public static void createYoutubeContentOwnerTransfer(
      String projectId, TransferConfig transferConfig) throws IOException {
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = client.createTransferConfig(request);
      System.out.println(
          "Youtube content owner channel transfer created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("Youtube content owner channel transfer was not created." + ex.toString());
    }
  }
}
```

**附註：**如果您是第一次設定 YouTube 報表工作，在首批報表備妥前，最多必須等候 48 小時。詳情請參閱 YouTube Reporting API 說明文件中的[建立報表工作](https://developers.google.com/youtube/reporting/v1/reports/?hl=zh-tw#step-3-create-a-reporting-job)一節。

## 查詢資料