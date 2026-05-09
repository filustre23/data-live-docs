Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Google Ad Manager 資料載入 BigQuery

您可以使用 Google Ad Manager 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 Google Ad Manager 載入 BigQuery。透過 BigQuery 資料移轉服務，您可以排定週期性移轉工作，將 Google Ad Manager 的最新資料新增至 BigQuery。

## 連接器總覽

Google Ad Manager 連接器的 BigQuery 資料移轉服務支援下列資料移轉選項。

| 資料轉移方式 | 支援 |
| --- | --- |
| 受支援的報表 | Google Ad Manager 連接器支援從下列報表轉移資料：    * [資料移轉 (Google Ad Manager DT) 檔案](https://support.google.com/admanager/answer/1733124?hl=zh-tw) * [資料移轉欄位](https://support.google.com/admanager/table/7401123?hl=zh-tw) * [比對 BigQuery 資料移轉服務提供的資料表](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transformation?hl=zh-tw)。系統會自動建立及更新這些素材資源。 * [比對以 PQL 擷取的資料表](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) * [來自 CompanyService (v201908) 的對照表](https://developers.google.com/doubleclick-publishers/docs/reference/v201908/CompanyService?hl=zh-tw) * [來自 OrderService (v201908) 的對照表](https://developers.google.com/doubleclick-publishers/docs/reference/v201908/OrderService?hl=zh-tw) * [來自 PlacementService (v201908) 的對照表](https://developers.google.com/doubleclick-publishers/docs/reference/v201908/PlacementService?hl=zh-tw)   如要瞭解 Google Ad Manager 報表如何轉換成 BigQuery 資料表和檢視表，請參閱「[Google Ad Manager 報表轉換](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transformation?hl=zh-tw)」一文。 |
| 重複頻率 | Google Ad Manager 連接器每 4 小時會轉移一次資料。根據預設，Google Ad Manager 資料移轉作業每 8 小時會重複執行一次。    [設定資料移轉](#set_up_a_google_ad_manager_transfer)時，可以設定資料移轉時間。 |
| 重新整理時間範圍 | Google Ad Manager 連接器會在執行資料移轉時，擷取最多 2 天的 Google Ad Manager 資料。您無法設定這個連結器的重新整理時間範圍。   詳情請參閱「[重新整理時間範圍](#refresh)」。 |
| 資料補充作業的可用性 | [執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，擷取排定資料移轉時間以外的資料。您可以擷取資料來源資料保留政策允許的最早資料。    如要瞭解 Google Ad Manager 的資料保留政策，請參閱「[Google Ad Manager 資料移轉報表](https://support.google.com/admanager/answer/1733124?hl=zh-tw)」。 |

**注意：** BigQuery 資料移轉服務支援 Google Ad Manager DT 檔案使用下列分隔符號：定位點分隔符號 ( \t )、直立線符號 ( | )、脫字符號 ( ^ ) 和逗號 ( , )。

## 從 Google Ad Manager 移轉作業擷取資料

從 Google Ad Manager 將資料移轉至 BigQuery 時，系統會將資料載入以日期為分區的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果為同一天排定多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該特定日期的資料分割。同一天內進行多次轉移或執行回填作業，不會導致資料重複，也不會影響其他日期的分區。

### 重新整理視窗

*更新期*是指資料移轉作業在進行時，擷取資料的天數。舉例來說，如果重新整理時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務就會從來源資料表擷取過去三天的所有資料。在這個範例中，每天進行移轉時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分割區，並複製當天的來源資料表資料，然後自動觸發補充作業執行作業，以更新過去兩天的來源資料表資料。系統自動觸發的回填作業會覆寫或增量更新 BigQuery 目的地資料表，具體做法取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。舉例來說，如果重新整理時間範圍為三天，而您是第一次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

如要擷取重新整理時間範圍外的資料 (例如歷來資料)，或從任何轉移中斷或缺漏中復原資料，可以啟動或排定[補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

### 資料移轉 (DT) 檔案更新

從 Google Ad Manager 資料移轉 (Google Ad Manager DT) 檔案建立的資料表可以遞增更新。Google Ad Manager 會將 Google Ad Manager DT 檔案新增至 Cloud Storage bucket。接著，移轉作業會將 Cloud Storage bucket 中的新 Google Ad Manager DT 檔案，以遞增方式載入 BigQuery 資料表，不會重新載入已移轉至 BigQuery 資料表的檔案。

舉例來說，Google Ad Manager 會在凌晨 1 點將 `file1` 新增至值區，並在凌晨 2 點新增 `file2`。移轉作業會在凌晨 3 點 30 分開始，並將 `file1` 和 `file2` 載入至 BigQuery。Google Ad Manager 接著會在上午 5 點新增 `file3`，並在上午 6 點新增 `file4`。第二次移轉作業會在上午 7 點 30 分開始，並將 `file3` 和 `file4` 附加到 BigQuery，而不是載入所有四個檔案來覆寫資料表。

### 更新對照表

對照表可為資料移轉檔案中的原始值提供查詢機制。如需對照表清單，請參閱「[Google Ad Manager 報表轉換](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transformation?hl=zh-tw)」。
不同的比對資料表會以不同的擷取方法更新。下表列出比對表及其擷取方法：

| 擷取方式 | 說明 | 對照表 |
| --- | --- | --- |
| 分批更新 | 每次執行時，都會附加增量更新。舉例來說，當天第一次執行轉移作業時，系統會載入轉移作業前修改的所有資料；當天第二次執行轉移作業時，系統會載入前一次轉移作業後，以及本次轉移作業前修改的資料。 | `Company`、`Order`、`Placement`、`LineItem`、`AdUnit` |
| 更新整個表格 | 全表更新每天會載入整個表格一次。舉例來說，當天第一次執行轉移作業時，系統會載入資料表的所有可用資料。當天第二次執行轉移作業時，系統會略過載入這些資料表。 | `AdCategory`、`AudienceSegmentCategory`、`BandwidthGroup`、`Browser`、`BrowserLanguage`、 `DeviceCapability`、`DeviceCategory`、`DeviceManufacturer`、`GeoTarget`、`MobileCarrier`、 `MobileDevice`、`MobileDeviceSubmodel`、`OperatingSystem`、`OperatingSystemVersion`、 `ThirdPartyCompany`、`TimeZone`、`User`、`ProgrammaticBuyer` |
| 覆寫整個資料表 | 每次執行移轉作業時，系統都會覆寫整個資料表。 | `AudienceSegment` |

## 事前準備

建立 Google Ad Manager 資料移轉作業前的準備事項如下：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)以儲存 Google Ad Manager 資料。
* **確認貴機構可存取 Google Ad Manager 資料移轉 (Google Ad Manager DT) 檔案。**這些檔案會由 Google Ad Manager 團隊傳送至 Cloud Storage bucket。如要取得 Google Ad Manager DT 檔案的存取權，請參閱「[Ad Manager 資料移轉報表](https://support.google.com/admanager/answer/1733124?hl=zh-tw)」。Google Ad Manager 小組可能會向您收取額外費用。

  完成上述步驟後，您會獲得類似下列字串的 Cloud Storage 值區：

  ```
      gdfp-12345678
  ```

  該 Google Cloud 團隊「無法」代表您產生或授予 Google Ad Manager DT 檔案的存取權。請與 Google Ad Manager [支援小組](https://support.google.com/admanager/answer/3059042?ref_topic=7519191&hl=zh-tw)聯絡，詢問有關 Google Ad Manager DT 檔案存取權的事宜。
* 為 Google Ad Manager 網路[啟用 API 存取權](https://support.google.com/admanager/answer/3088588?hl=zh-tw)。
* 如要設定資料移轉通知，您必須擁有 Pub/Sub 的 `pubsub.topics.setIamPolicy` 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。

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

### 必要的 Google Ad Manager 角色

授予儲存在 Cloud Storage 中 Google Ad Manager DT 檔案的讀取權限。Google Ad Manager DT 檔案的權限是由 Google Ad Manager 團隊管理。除了 Google Ad Manager 資料移轉檔案，建立資料移轉作業的人員也必須加入 Google Ad Manager 聯播網，並擁有建立各種[對照表](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transformation?hl=zh-tw) (委刊項、訂單、廣告單元等) 所需的所有實體讀取權限。如要完成這項操作，請將驗證資料移轉的 Ad Manager 使用者新增至 Ad Manager 中的「所有實體」團隊。

## 設定 Google Ad Manager 移轉作業

針對 Google Ad Manager 設定 BigQuery 資料移轉作業需要下列項目：

* **Cloud Storage bucket**：Google Ad Manager DT 檔案的 Cloud Storage bucket URI，如「[事前準備](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transfer?hl=zh-tw#before_you_begin)」一節所述。
  值區名稱應如下所示：

  ```
  gdfp-12345678
  ```
* **網路代碼**：您可以在登入網路時的網址中找出 Google Ad Manager 網路代碼。舉例來說，在網址 `https://admanager.google.com/2032576#delivery` 中，`2032576` 是您的網路代碼。詳情請參閱「[開始使用 Google Ad Manager](https://developers.google.com/doubleclick-publishers/docs/start?hl=zh-tw)」一文。

如要為 Google Ad Manager 建立 BigQuery 資料移轉服務資料移轉作業，請進行下列操作：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「建立轉移作業」add。
3. 在「Create Transfer」(建立轉移作業) 頁面：

   * 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Google Ad Manager (formerly DFP)」(Google Ad Manager (原名為 DFP))。
   * 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
   * 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
   * 在「Data source details」(資料來源詳細資料) 專區：
     + 在「Cloud Storage bucket」 輸入用來儲存資料移轉檔案的 Cloud Storage bucket 名稱。輸入 bucket 名稱時，請勿加入 `gs://`。
     + 針對「Network code」(網路代碼)，輸入您的網路代碼。
   * 在「Service Account」(服務帳戶) 選單，選取與貴組織 Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與移轉作業建立關聯，而非使用使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。
       
       
     如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立移轉作業。如果是以 Google 帳戶登入，則不一定要透過服務帳戶建立移轉作業。服務帳戶必須具備[必要權限](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transfer?hl=zh-tw#required_permissions)。
   * (選用步驟) 在「Notification options」(通知選項) 部分執行下列操作：

     + 按一下啟用電子郵件通知的切換開關。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
     + 點選切換按鈕，啟用 Pub/Sub 執行通知。在「Select a Cloud Pub/Sub topic」(選取 Cloud Pub/Sub 主題) 選取主題名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
4. 按一下 [儲存]。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。還需加上以下旗標：

* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

選用標記：

* `--service_account_name`：指定用於 Google Ad Manager 轉移驗證的服務帳戶，而非使用者帳戶。

```
bq mk --transfer_config \
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
* name 是資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改資料移轉作業時，能夠據此識別即可。
* parameters 含有已建立移轉設定的 JSON 格式參數，例如：`--params='{"param":"param_value"}'`。針對 Google Ad Manager，您必須提供 `bucket` 和 `network_code` 參數。
  + `bucket`：包含 Google Ad Manager DT 檔案的 Cloud Storage bucket。
  + `network_code`：聯播網代碼
  + `load_match_tables`：是否要載入比對資料表。預設為 `True`
* data\_source 是資料來源：`dfp_dt` (Google Ad Manager)。
* service\_account\_name 是用於驗證資料移轉作業的服務帳戶名稱。服務帳戶應由用於建立轉移作業的 `project_id` 擁有，且應具備所有[必要權限](#required_permissions)。

**注意：** 您無法使用指令列工具設定通知。

您還可以提供 `--project_id` 標記來指定特定專案。如果未指定 `--project_id`，系統會採用預設專案。

舉例來說，下列指令會使用聯播網代碼 `12345678`、Cloud Storage 值區 `gdfp-12345678` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 Google Ad Manager 資料移轉作業。資料移轉作業會在預設專案中建立：

```
bq mk --transfer_config \
--target_dataset=mydataset \
--display_name='My Transfer' \
--params='{"bucket": "gdfp-12345678","network_code": "12345678"}' \
--data_source=dfp_dt
```

執行指令後，您會收到如下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照指示進行操作，並在指令列中貼上驗證碼。

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

// Sample to create a ad manager(formerly DFP) transfer config
public class CreateAdManagerTransfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    String bucket = "gs://cloud-sample-data";
    // the network_code can only be digits with length 1 to 15
    String networkCode = "12345678";
    Map<String, Value> params = new HashMap<>();
    params.put("bucket", Value.newBuilder().setStringValue(bucket).build());
    params.put("network_code", Value.newBuilder().setStringValue(networkCode).build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Ad Manager Config Name")
            .setDataSourceId("dfp_dt")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .build();
    createAdManagerTransfer(projectId, transferConfig);
  }

  public static void createAdManagerTransfer(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = client.createTransferConfig(request);
      System.out.println("Ad manager transfer created successfully :" + config.getName());
    } catch (
```