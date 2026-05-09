Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Google Ads 廣告資料載入 BigQuery

您可以使用 Google Ads 適用的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)連接器，將 Google Ads (舊稱 Google AdWords) 的資料載入至 BigQuery。您可以使用 BigQuery 資料移轉服務，安排週期性移轉工作，將 Google Ads 的最新資料新增至 BigQuery。

如要瞭解最近的資料來源變更，請參閱 [BigQuery 資料移轉服務資料來源變更記錄](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw)。

## 連接器總覽

Google Ads 連接器的 BigQuery 資料移轉服務支援下列資料移轉選項。

| 資料轉移方式 | 支援 |
| --- | --- |
| 受支援的報表 | Google Ads 連接器支援從 [Google Ads API v22](https://developers.google.com/google-ads/api/fields/v22/overview?hl=zh-tw) 的報表傳輸資料。 如要瞭解 Google Ads 報表如何轉換成 BigQuery 表格和視圖，請參閱「[Google Ads 報表轉換](https://docs.cloud.google.com/bigquery/docs/google-ads-transformation?hl=zh-tw)」一文。 |
| 重複頻率 | Google Ads 連接器支援每日資料轉移。    根據預設，資料移轉作業會在建立時排定時間。[設定資料移轉作業](#setup-data-transfer)時，你可以設定資料移轉時間。 |
| 重新整理時間範圍 | 您可以排定資料移轉作業，在執行作業時擷取最多 30 天的 Google Ads 廣告資料。[設定資料移轉時，您可以設定重新整理視窗的持續時間。](#setup-data-transfer)    根據預設，Google Ads 連接器的更新期為 7 天。    詳情請參閱「[重新整理時間範圍](#refresh)」。 系統每天會為[比對資料表](https://docs.cloud.google.com/bigquery/docs/google-ads-transformation?hl=zh-tw#google_ads_match_tables)建立快照，並儲存在上次執行日期的分區中。系統不會更新回填或使用重新整理視窗載入的日期，因此相符資料表快照不會更新。 |
| 資料補充作業的可用性 | [執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，擷取排定資料移轉時間以外的資料。您可以擷取資料來源資料保留政策允許的最早資料。    如要瞭解 Google Ads 的資料保留政策，請參閱「[Google Ads 資料保留政策](https://support.google.com/google-ads/answer/15188209?hl=zh-tw)」。 |
| 每個管理員帳戶的客戶 ID 數 | 8,000  BigQuery 資料移轉服務對每個 Google Ads [管理員帳戶](https://support.google.com/adwords/answer/6139186?hl=zh-tw) (MCC) 最多支援 **8000 個客戶 ID**。 |

如要將 Google Ads 報表對應到 Google Ads UI 中顯示的項目，請參閱[將報表對應至 Google Ads UI](https://developers.google.com/google-ads/api/docs/conversions/ui-mapping?hl=zh-tw) 一文。

## 從 Google Ads 轉移作業擷取資料

將 Google Ads 資料移轉至 BigQuery 時，系統會將資料載入以日期為分區的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果為同一天排定多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該特定日期的資料分割。同一天內進行多次轉移或執行回填作業，不會導致資料重複，也不會影響其他日期的分區。

### 重新整理視窗

*更新期*是指資料移轉作業在進行時，擷取資料的天數。舉例來說，如果重新整理時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務就會從來源資料表擷取過去三天的所有資料。在這個範例中，每天進行移轉時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分割區，並複製當天的來源資料表資料，然後自動觸發補充作業執行作業，以更新過去兩天的來源資料表資料。系統自動觸發的回填作業會覆寫或增量更新 BigQuery 目的地資料表，具體做法取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。舉例來說，如果重新整理時間範圍為三天，而您是第一次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

如要擷取重新整理時間範圍外的資料 (例如歷來資料)，或從任何轉移中斷或缺漏中復原資料，可以啟動或排定[補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 限制

* Google Ads 資料轉移的最高頻率為每 24 小時一次。預設情況下，移轉作業會在您建立移轉作業時啟動。不過，您可以在[建立轉移作業](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#setup-data-transfer)時設定轉移開始時間。
* BigQuery 資料移轉服務在 Google Ads 移轉期間，不支援增量資料移轉。指定資料移轉日期後，系統會移轉該日期可用的所有資料。

## 事前準備

建立 Google Ads 資料移轉作業前，請先完成下列事項：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料移轉服務資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，以儲存 Google Ads 廣告資料。
* 如要為 Pub/Sub 設定移轉作業執行通知，請確認您擁有 `pubsub.topics.setIamPolicy` 權限。如果您設定電子郵件通知，就不需要 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。

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

### 必要的 Google Ads 角色

您必須授予移轉設定所使用的 Google Ads 客戶 ID 或[管理員帳戶](https://support.google.com/google-ads/answer/6139186?hl=zh-tw) (MCC) 讀取權限。建立新的轉移設定時，如果授權方式是使用個別使用者憑證，則必須[啟用兩步驟驗證](https://support.google.com/accounts/answer/185839?hl=zh-tw)。

如要授權服務帳戶移轉 Google Ads 資料，建議您授予服務帳戶 Google Ads 的直接帳戶存取權。詳情請參閱「[使用直接帳戶存取權授權](https://developers.google.com/google-ads/api/docs/oauth/service-accounts?hl=zh-tw#direct)」。如果轉移設定是透過服務帳戶授權，則不需要多重驗證 (MFA) 規定，例如兩步驟驗證。

## 建立 Google Ads 廣告資料移轉作業

如要為 Google Ads 報表建立資料移轉作業，您需要 Google Ads 客戶 ID 或管理員帳戶 (我的客戶中心)。如要瞭解如何擷取 Google Ads 客戶 ID，請參閱[尋找客戶 ID](https://support.google.com/google-ads/answer/1704344?hl=zh-tw) 一文。

如要為 Google Ads 報表建立資料移轉作業，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Source type」(來源類型) 區段中，針對「Source」(來源)，選擇 [Google Ads]。
4. 在「Data source details」(資料來源詳細資料) 區段：

   1. 在「Customer ID」(客戶 ID) 中，輸入您的 Google Ads 客戶 ID。
   2. 在「Report type」(報表類型) 選取「Standard」(標準) 或「Custom」(自訂)。
      * 如果選取「Standard」(標準)，移轉作業就會涵蓋一組標準報表和欄位，詳情請參閱 [Google Ads 報表轉換](https://docs.cloud.google.com/bigquery/docs/google-ads-transformation?hl=zh-tw)的相關說明。
        + 選用步驟：選取選項來排除已移除或停用的項目，以及加入 Google Ads 中沒有的資料表。
        + 選用步驟：輸入要加入的資料表清單 (以半形逗號分隔)，例如 `Campaign, AdGroup`。您可以為這份清單加上 `-` 前置字元來排除特定資料表，例如 `-Campaign, AdGroup`。預設會加入所有資料表。
        + 選用步驟：選取這個選項，加入最高成效廣告報表專屬的資料表。如要進一步瞭解最高成效廣告的支援情形，請參閱[最高成效廣告支援情形](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#pmax-support)的相關說明。
        + 選用：在「Refresh window」(重新整理時間範圍) 中，輸入介於 1 至 30 的值。
      * 如果選取「Custom」(自訂)，請針對要納入這項移轉作業的個別[自訂報表](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#custom_reports)，提供輸出資料表和 Google Ads 查詢。
        + 選用步驟：點選「Add query」(新增查詢) 來新增自訂報表。
        + 選用：在「Refresh window」(重新整理時間範圍) 中，輸入介於 1 至 30 的值。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
7. 在「Schedule options」(排程選項) 專區：

   * 在「Repeat frequency」(重複頻率) 部分選取選項，指定資料移轉作業的執行頻率。如果選取「Days」(天)，請按照世界標準時間提供有效的值。
     + 小時
     + 天
     + 隨選
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
8. 在「Service Account」(服務帳戶) 選單，選取與貴機構 Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與資料移轉作業建立關聯，這樣就不需要使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)。

   * 如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，就必須有服務帳戶才能建立移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立移轉作業。
   * 服務帳戶必須具備[必要權限](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#required_permissions)。
9. (選用) 在「Notification options」(通知選項) 區段中：

   * 按一下啟用電子郵件通知的切換開關。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   * 點選切換按鈕，啟用 Pub/Sub 通知。在「Select a Cloud Pub/Sub topic」(選取 Cloud Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
10. 按一下 [儲存]。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。還需加上以下旗標：

* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

以下旗標為選用項目：

* `--project_id`：指定要使用的專案。如果未指定旗標，系統會使用預設專案。
* `--table_filter`：指定要納入資料轉移作業的資料表。如果未指定旗標，系統會納入所有資料表。如要只納入特定資料表，請使用以半形逗號分隔的值清單 (例如 `Ad`、`Campaign`、`AdGroup`)。如要排除特定資料表，請在值前面加上連字號 (`-`) (例如 `-Ad`、`Campaign`、`AdGroup`)。
* `--schedule`：指定查詢的執行頻率。如未指定 `--schedule`，預設值會設為 `every 24 hours`。如要瞭解排程語法，請參閱「[設定排程格式](https://docs.cloud.google.com/appengine/docs/flexible/scheduling-jobs-with-cron-yaml?hl=zh-tw#formatting_the_schedule)」。
* `--refresh_window_days`：指定移轉設定的更新期 (以天為單位)。預設值為 `7`。
* `--service_account_name`：指定要用於 Google Ads 轉移驗證的服務帳戶，而非使用者帳戶。
* `--include_pmax`：指定 `true`，加入最高成效廣告報表專屬的資料表。預設值為 `false`。如要進一步瞭解最高成效廣告的支援情形，請參閱[最高成效廣告支援情形](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#pmax-support)

```
bq mk \
--transfer_config \
--project_id=PROJECT_ID \
--target_dataset=DATASET \
--display_name=NAME \
--params='PARAMETERS' \
--data_source=DATA_SOURCE \
--table_filter=TABLES \
--schedule=SCHEDULE \
--refresh_window_days=REFRESH_DAYS \
--service_account_name=SERVICE_ACCOUNT_NAME \
--include_pmax=PMAX_ENABLE
```

其中：

* PROJECT\_ID 是您的專案 ID。
* DATASET 是資料移轉設定的目標資料集。
* NAME 是資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* PARAMETERS 包含移轉設定的下列 JSON 參數：`--params='{"param":"param_value"}'`。
  + `customer_id`：輸入您的 Google Ads 客戶 ID。這是必填欄位。
  + `custom_report_table_names`：這項轉移作業中包含的[自訂報表](#custom_reports)資料表名稱清單。這份清單對應至 `custom_report_queries` 中的查詢。這個清單的長度必須與 `custom_report_queries` 中的清單長度相符。
  + `custom_report_queries`：這項轉移作業中包含的自訂報表清單，以及[Google Ads 查詢語言 (GAQL) 查詢](#custom_reports)。這份清單對應至 `custom_report_table_names` 中的名稱。這個清單的長度必須與 `custom_report_table_names` 中的清單長度相符。
  + 選用：將 `exclude_removed_items` 參數設為 `true`，以免移轉遭到移除或停用的實體和指標。
* DATA\_SOURCE 是資料來源：`google_ads`。
* TABLES 是逗號分隔的清單，可指定要納入或排除在資料移轉作業之外的資料表。
* SCHEDULE 是您希望查詢執行的頻率。如未指定 `--schedule`，預設為每 24 小時執行一次，時間從建立移轉作業時開始計算。
* REFRESH\_DAYS 是一個整數，用來指定移轉設定的更新期 (以天為單位)。預設值為 `7`。
* SERVICE\_ACCOUNT\_NAME 是用於驗證移轉作業的服務帳戶名稱。服務帳戶必須由用於建立轉移作業的 `project_id` 所擁有，且必須具備所有[必要權限](#required_permissions)。
* PMAX\_ENABLE：指定 `true`，加入最高成效廣告報表專屬的資料表。預設值為 `false`。如要進一步瞭解最高成效廣告的支援情形，請參閱[最高成效廣告支援情形](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#pmax-support)

**注意：** 您無法使用指令列工具設定通知。

舉例來說，下列指令會使用客戶 ID `123-123-1234` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 Google Ads 資料移轉作業。資料移轉作業會在預設專案中建立：

```
bq mk \
--transfer_config \
--target_dataset=mydataset \
--display_name='My Transfer' \
--params='{"customer_id":"123-123-1234","exclude_removed_items":"true"}' \
--data_source=google_ads
```

首次執行指令時，您會收到類似以下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照訊息中的操作說明進行，在指令列中貼上驗證碼。

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

// Sample to create ads(formerly AdWords) transfer config
public class CreateAdsTransfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    // the customer_id only allows digits and hyphen ('-').
    String customerId = "012-345-6789";
    String refreshWindow = "100";
    Map<String, Value> params = new HashMap<>();
    params.put("customer_id", Value.newBuilder().setStringValue(customerId).build());
    params.put("refreshWindow", Value.newBuilder().setStringValue(refreshWindow).build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Ads Transfer Config Name")
            .setDataSourceId("adwords")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .build();
    createAdsTransfer(projectId, transferConfig);
  }

  public static void createAdsTransfer(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = client.createTransferConfig(request);
      System.out.println("Ads transfer created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out
```