Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Campaign Manager 資料載入 BigQuery

您可以使用 Campaign Manager 連接器，透過 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)將資料從 Campaign Manager 載入 BigQuery。透過 BigQuery 資料移轉服務，您可以安排週期性移轉工作，將 Campaign Manager 的最新資料新增至 BigQuery。

## 連接器總覽

Campaign Manager 連接器的 BigQuery 資料移轉服務支援下列資料移轉選項。

如要瞭解 Campaign Manager 報表如何轉換成 BigQuery 資料表和檢視表，請參閱「[Campaign Manager 報表轉換](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transformation?hl=zh-tw)」。

| 資料轉移方式 | 支援 |
| --- | --- |
| 受支援的報表 | Campaign Manager 連接器支援從下列報表移轉資料：   * [資料移轉 v2 (Campaign Manager DTv2) 檔案](https://developers.google.com/doubleclick-advertisers/dtv2/reference/file-format?hl=zh-tw) * [資料移轉 v2 (Campaign Manager DTv2) 對照表](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw) |
| 重複頻率 | Campaign Manager 連接器每 8 小時會傳輸一次資料。    根據預設，系統會在建立資料移轉時排定 Campaign Manager 資料移轉作業。 |
| 重新整理時間範圍 | 資料移轉作業執行時，Campaign Manager 連接器會擷取最多 2 天前的 Campaign Manager 資料。您無法設定這個連結器的重新整理時間範圍。   詳情請參閱「[重新整理時間範圍](#refresh)」。 |
| 資料補充作業的可用性 | [執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，擷取排定資料移轉時間以外的資料。您可以擷取資料來源資料保留政策允許的最早資料。    如要瞭解 Display & Video 360 的資料保留政策，請參閱「[資料刪除和保留控制項](https://support.google.com/campaignmanager/answer/10769131?hl=zh-tw)」。 |

## 從 Campaign Manager 移轉作業擷取資料

從 Campaign Manager 將資料移轉至 BigQuery 時，系統會將資料載入以日期為分區的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果為同一天排定多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該特定日期的資料分割。同一天內進行多次轉移或執行回填作業，不會導致資料重複，也不會影響其他日期的分區。

### 重新整理視窗

*更新期*是指資料移轉作業在進行時，擷取資料的天數。舉例來說，如果重新整理時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務就會從來源資料表擷取過去三天的所有資料。在這個範例中，每天進行移轉時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分割區，並複製當天的來源資料表資料，然後自動觸發補充作業執行作業，以更新過去兩天的來源資料表資料。系統自動觸發的回填作業會覆寫或增量更新 BigQuery 目的地資料表，具體做法取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。舉例來說，如果重新整理時間範圍為三天，而您是第一次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

如要擷取重新整理時間範圍外的資料 (例如歷來資料)，或從任何轉移中斷或缺漏中復原資料，可以啟動或排定[補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 事前準備

建立 Campaign Manager 資料移轉作業前的準備事項如下：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存 Campaign Manager 資料。
* **確認貴機構可存取 Campaign Manager 資料移轉第 2 版 (Campaign Manager DTv2) 檔案。**這些檔案會由 Campaign Manager 團隊傳送至 Cloud Storage bucket。如要取得 Campaign Manager DTv2 檔案的存取權，請視您是否與 Campaign Manager 簽訂直接合約，採取後續步驟。這兩種情況都可能需要額外付費。

  + 如果您與 Campaign Manager 簽訂合約，請與 [Campaign Manager 支援團隊](https://support.google.com/campaignmanager/answer/9026876?amp%3Bref_topic=2834087&%3Bvisit_id=1-636444821343154346-869320595&%3Brd=2&hl=zh-tw)聯絡，設定 Campaign Manager DTv2 檔案。
  + 如果您**沒有** Campaign Manager 合約，您的代理商或 Campaign Manager 經銷商可能可以存取 Campaign Manager DTv2 檔案。請與您的代理商或經銷商聯絡，以便取得這些檔案的存取權。

  完成上述步驟後，您會獲得類似下列字串的 Cloud Storage bucket 名稱：

  `dcdt_-dcm_account123456`

  團隊無法 Google Cloud 代表您產生或授予 Campaign Manager DTv2 檔案的存取權。如要存取 Campaign Manager DTv2 檔案，請與 Campaign Manager [支援團隊](https://support.google.com/campaignmanager/answer/9026876?ref_topic=2834087&visit_id=1-636444821343154346-869320595&rd=2&hl=zh-tw)、代理商或 Campaign Manager 經銷商聯絡。
* 如果您想要為 Pub/Sub 設定移轉作業執行通知，您必須擁有`pubsub.topics.setIamPolicy` 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。

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

### 必要的 Campaign Manager 角色

授予 Campaign Manager DTv2 檔案的讀取權限，這些檔案儲存在 Cloud Storage 中。存取權由提供 Cloud Storage bucket 的實體管理。

## 設定 Campaign Manager 轉移作業

如要設定 Campaign Manager 資料移轉作業，您必須擁有：

* **Cloud Storage 值區**：存放 Campaign Manager DTv2 檔案的 Cloud Storage 值區 URI，如[事前準備](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw#before_you_begin)一節所述。值區名稱應如下所示：

  `dcdt_-dcm_account123456`
* **Campaign Manager ID**：您的 Campaign Manager Network、廣告客戶或 Floodlight ID。Network ID 在階層中是父項。

### 尋找 Campaign Manager ID

如要擷取 Campaign Manager ID，您可以使用 Cloud Storage [主控台](https://console.cloud.google.com/storage?hl=zh-tw)檢查 Campaign Manager 資料移轉 Cloud Storage bucket 中的檔案。Campaign Manager ID 可用來在您提供的 Cloud Storage bucket 中比對檔案，這個 ID 會嵌入**檔案名稱**，而非 Cloud Storage bucket 名稱。

例如：

* 在名為 `dcm_account123456_activity_*` 的檔案中，ID 為 **123456**。
* 在名為 `dcm_floodlight7890_activity_*` 的檔案中，ID 為 **7890**。
* 在名為 `dcm_advertiser567_activity_*` 的檔案中，
  ID 為 **567**。

### 尋找檔案名稱前置字串

在極少數的情況下，在您 Cloud Storage bucket 中的檔案可能包含由 Google Marketing Platform 服務團隊為您設定的非標準自訂檔案名稱。

例如：

* 在名為 `dcm_account123456custom_activity_*` 的檔案中，前置字串為 **dcm\_account123456custom**，也就是 `_activity` 之前的所有內容。

如果您需要協助，請聯絡 [Campaign Manager 支援小組](https://support.google.com/campaignmanager/answer/9026876?amp%3Bref_topic=2834087&%3Bvisit_id=1-636444821343154346-869320595&%3Brd=2&hl=zh-tw)。

### 為 Campaign Manager 建立資料移轉作業

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Create Transfer」(建立轉移作業) 頁面：

   * 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Campaign Manager」。
   * 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
   * 在「Schedule options」(排程選項) 區段中，針對「Schedule」(排程) 保留預設值 ([Start now] (立即開始))，或按一下 [Start at a set time] (於設定的時間開始)。

     + 在「Repeats」(重複頻率) 選擇移轉作業的執行頻率。如果您不是選取「Daily」(每天)，會需要進一步選擇細項。例如，您選了「Weekly」(每週)，接著就要選取星期幾。
     + 在「Start date and run time」(開始日期和執行時間)，輸入開始移轉資料的日期和時間。如果選取「Start now」(立即開始)，這個選項就會停用。
   * 在「Destination settings」(目的地設定) 部分，「Destination dataset」(目的地資料集) 請選取您為了儲存資料而建立的資料集。
   * 在「Data source details」(資料來源詳細資料) 區段：

     + 在「Cloud Storage bucket」輸入或瀏覽用來儲存 Data Transfer V2.0 檔案的 Cloud Storage bucket 名稱。輸入 bucket 名稱時，請勿加入 `gs://`。
     + 在「DoubleClick ID」輸入合適的 Campaign Manager ID。
     + (選用步驟) 如果檔案內含[類似這些範例的標準名稱](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw#find-id)，請將 「File name prefix」(檔案名稱前置字串) 欄位留空。如果 Cloud Storage bucket 中的檔案有自訂檔案名稱，請指定[檔案名稱前置字串](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw#filename-prefix)。
   * (選用) 在「Notification options」(通知選項) 區段中：

     + 按一下啟用電子郵件通知的切換開關。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
     + 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
4. 按一下 [儲存]。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。還需加上以下旗標：

* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

```
bq mk --transfer_config \
--project_id=project_id \
--target_dataset=dataset \
--display_name=name \
--params='parameters' \
--data_source=data_source
```

其中：

* project\_id 是您的專案 ID。
* dataset 是資料移轉設定的目標資料集。
* name 是資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* parameters 含有已建立資料移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。針對 Campaign Manager，您必須提供 `bucket` 和 `network_id` 參數。`bucket` 是內含 Campaign Manager DTv2 檔案的 Cloud Storage bucket。`network_id` 是您的聯播網、Floodlight 或廣告主 ID。
* data\_source 是資料來源：`dcm_dt` (Campaign Manager)。

**注意：** 您無法使用指令列工具設定通知。

您還可以提供 `--project_id` 標記來指定特定專案。如果未指定 `--project_id`，系統會採用預設專案。

舉例來說，下列指令會使用 Campaign Manager ID `123456`、Cloud Storage 值區 `dcdt_-dcm_account123456` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 Campaign Manager 資料移轉作業。參數 `file_name_prefix` 為選填，僅適用於罕見的自訂檔案名稱。

資料移轉作業會在預設專案中建立：

```
bq mk --transfer_config \
--target_dataset=mydataset \
--display_name='My Transfer' \
--params='{"bucket": "dcdt_-dcm_account123456","network_id": "123456","file_name_prefix":"YYY"}' \
--data_source=dcm_dt
```

執行指令後，您會收到如下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照指示進行操作，並在指令列中貼上驗證碼。

**注意：** 當您使用指令列工具建立 Campaign Manager 資料移轉作業時，系統會採用「Schedule」(排程) 的預設值 (每 8 小時) 進行移轉設定。

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

// Sample to create campaign manager transfer config
public class CreateCampaignmanagerTransfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    String bucket = "gs://cloud-sample-data";
    // the network_id only allows digits
    String networkId = "7878";
    String fileNamePrefix = "test_";
    Map<String, Value> params = new HashMap<>();
    params.put("bucket", Value.newBuilder().setStringValue(bucket).build());
    params.put("network_id", Value.newBuilder().setStringValue(networkId).build());
    params.put("file_name_prefix", Value.newBuilder().setStringValue(fileNamePrefix).build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Campaignmanager Config Name")
            .setDataSourceId("dcm_dt")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .build();
    createCampaignmanagerTransfer(projectId, transferConfig);
  }

  public static void createCampaignmanagerTransfer(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = client.createTransferConfig(request);
      System.out.println("Campaignmanager transfer created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("Campaignmanager transfer was not created." + ex.toString());
    }
  }
}
```

**警告：** 如果您變更報表的結構定義，則當天所有檔案的結構定義都必須相同，否則當天所有的資料移轉作業都會失敗。

## 排解 Campaign Manager 移轉設定問題

如果無法順利設定資料移轉，請參閱[排解移轉設定問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw)中的「[Campaign Manager 移轉問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#campaign_manager_transfer_issues)」一節。

## 查詢資料

資料移轉至 BigQuery 時，系統會將資料寫入擷取時間分區資料表。詳情請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。

如果您要直接查詢資料表，而不要使用自動產生的檢視表，您必須在查詢中使用 `_PARTITIONTIME` 虛擬資料欄。詳情請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)一文。

## Campaign Manager 範例查詢

您可以使用下列 Campaign Manager 查詢範例來分析已移轉的資料。您還可以在 [數據分析](https://www.google.com/analytics/data-studio/?hl=zh-tw) 等視覺化工具中使用查詢。這些查詢可協助您開始透過 BigQuery 查詢 Campaign Manager 資料。如果您對於這些報表的功能有其他問題，