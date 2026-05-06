Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Google Play 資料載入 BigQuery

您可以使用 Google Play 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 Google Play 載入 BigQuery。透過 BigQuery 資料移轉服務，您可以安排週期性移轉工作，將 Google Play 的最新資料新增至 BigQuery。

## 連接器總覽

Google Play 連接器的 BigQuery 資料移轉服務支援下列資料移轉選項。

| 資料移轉選項 | 支援 |
| --- | --- |
| 受支援的報表 | * 詳細報表：   + [評論](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#reviews)   + [財務報表](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#financial) * 匯總報表：   + [統計資料](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#statistics)   + [獲取新客](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#acquisition)   如要瞭解 Google Play 報表如何轉換成 BigQuery 表格和檢視畫面，請參閱「[Google Play 報表轉換](https://docs.cloud.google.com/bigquery/docs/play-transformation?hl=zh-tw)」一文。 |
| 重複頻率 | Google Play 連接器支援每日資料轉移。    根據預設，資料移轉作業會在建立時排定時間。[設定資料移轉作業](#setup-transfer)時，你可以設定資料移轉時間。 |
| 重新整理時間範圍 | 資料移轉作業執行時，Google Play 連接器會擷取最多 7 天的 Google Play 資料。   詳情請參閱「[重新整理時間範圍](#refresh)」。 |
| 資料補充作業的可用性 | [執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，擷取排定資料移轉時間以外的資料。您可以擷取資料來源資料保留政策允許的最早資料。 |

## 從 Google Play 轉移作業擷取資料

從 Google Play 移轉資料至 BigQuery 時，系統會將資料載入依日期分區的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果為同一天排定多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該特定日期的資料分割。同一天內進行多次轉移或執行回填作業，不會導致資料重複，也不會影響其他日期的分區。

### 重新整理視窗

*更新期*是指資料移轉作業在執行時，擷取資料的天數。舉例來說，如果重新整理時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務就會從來源資料表擷取過去三天的所有資料。在這個範例中，每天進行移轉時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分割區，並複製當天的來源資料表資料，然後自動觸發補充作業執行作業，以更新過去兩天的來源資料表資料。系統自動觸發的回填作業會覆寫或增量更新 BigQuery 目的地資料表，具體做法取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。舉例來說，如果重新整理時間範圍為三天，而您是第一次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

如要擷取重新整理時間範圍外的資料 (例如歷來資料)，或從任何轉移中斷或缺漏中復原資料，可以啟動或排定[補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 限制

* 資料移轉作業的最低排程頻率為每 24 小時一次。預設情況下，移轉作業會在您建立移轉作業時啟動。不過，您可以在[設定轉移作業](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw#setup-transfer)時，設定轉移開始時間。
* 在 Google Play 移轉期間，BigQuery 資料移轉服務不支援增量資料移轉。指定資料移轉日期後，系統會移轉該日期可用的所有資料。

## 事前準備

建立 Google Play 資料移轉作業前，請先：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)以儲存 Google Play 資料。
* 尋找您的 Cloud Storage bucket：
  1. 在 [Google Play 管理中心](https://play.google.com/apps/publish/?hl=zh-tw)，按一下 file\_download「下載報表」，然後選取「評論」、「統計資料」或「財務」。
  2. 如要複製 Cloud Storage bucket 的 ID，請按一下「複製 Cloud Storage URI」content\_copy。您的值區 ID 開頭為 `gs://`。舉例來說，如果是評論報表，您的 ID 類似於以下內容：

     ```
     gs://pubsite_prod_rev_01234567890987654321/reviews
     ```
  3. 如要轉移 Google Play 資料，只需複製 `gs://` 與 `/reviews` 之間的專屬 ID：

     ```
     pubsite_prod_rev_01234567890987654321
     ```
  4. 如果您想要為 Pub/Sub 設定移轉作業執行通知，您必須擁有`pubsub.topics.setIamPolicy` 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

## 所需權限

確認您已授予下列權限。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

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

### 必要的 Google Play 角色

確認您在 Google Play 中具有以下權限：

* 您在 [Google Play 管理中心](https://play.google.com/apps/publish/?hl=zh-tw)中必須具備報告存取權。

  該 Google Cloud 團隊「無法」代表您產生 Google Play 檔案或授予該檔案的存取權。如需存取 Google Play 檔案的說明，請參閱「[聯絡 Google Play 支援服務](https://support.google.com/googleplay/answer/9789798?ref_topic=3364260&visit_id=636444821343154346-869320595&rd=1&hl=zh-tw)」一文。

## 設定 Google Play 轉移作業

如要設定 Google Play 資料移轉作業，您必須擁有：

* **Cloud Storage 值區**。如需找出 Cloud Storage bucket 的步驟，請參閱「[事前準備](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw#before_you_begin)」一節。Cloud Storage 值區的開頭是 `pubsite_prod_rev`。例如：`pubsite_prod_rev_01234567890987654321`。
* **資料表後置字串**：在載入同一資料集的所有資料來源標上易記名稱。後置字串可用於防止不同的移轉作業寫入同一個資料表。所有將資料載入同個資料集的移轉工作，其資料表後置字串都不能重複，並且後置字串應盡量簡短，避免產生過於冗長的資料表名稱。

如要設定 Google Play 資料移轉作業，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「建立轉移作業」add。
3. 在「Create Transfer」(建立轉移作業) 頁面：

   * 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Google Play」。
   * 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
   * 在「Schedule options」(排程選項) 專區：

     + 在「Repeat frequency」(重複頻率) 部分選取選項，指定資料移轉作業的執行頻率。如果選取「Days」(天)，請按照世界標準時間提供有效的值。
     + 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
   * 在「Destination settings」(目的地設定) 部分，「Destination dataset」(目的地資料集) 請選取您為了儲存資料而建立的資料集。
   * 在「Data source details」(資料來源詳細資料) 區段：

     + 在「Cloud Storage bucket」(Cloud Storage bucket) 輸入 Cloud Storage bucket 的 ID。
     + 在「Table suffix」(資料表後置字串) 部分輸入後置字串，例如 `MT` (即 `My Transfer`)。
   * 在「Service Account」(服務帳戶) 選單，選取與貴組織 Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與資料移轉作業建立關聯，這樣就不需要使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。

     + 如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立資料移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立移轉作業。
     + 服務帳戶必須具備[必要權限](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw#required_permissions)。
   * (選用步驟) 在「Notification options」(通知選項) 部分執行下列操作：

     + 按一下啟用電子郵件通知的切換開關。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
     + 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
4. 按一下 [儲存]。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。還需加上以下旗標：

* `--target_dataset`
* `--display_name`
* `--params`
* `--data_source`

```
bq mk \
--transfer_config \
--project_id=project_id \
--target_dataset=dataset \
--display_name=name \
--params='parameters' \
--data_source=data_source
--service_account_name=service_account_name
```

其中：

* project\_id 是您的專案 ID。如果未指定 `--project_id`，系統會使用預設專案。
* dataset 是移轉設定的目標資料集。
* name 是移轉設定的顯示名稱。資料移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* parameters 含有已建立移轉設定的 JSON 格式參數，例如：`--params='{"param":"param_value"}'`。針對 Google Play，您必須提供 `bucket` 和 `table_suffix` 參數。`bucket` 是包含您 Play 報表檔案的 Cloud Storage 值區。
* data\_source 是資料來源：`play`。
* service\_account\_name 是用於驗證資料移轉作業的服務帳戶名稱。服務帳戶應由用於建立轉移作業的相同 `project_id` 所擁有，且應具備所有[必要權限](#required_permissions)。

**注意：** 您無法使用指令列工具設定通知。

舉例來說，下列指令會使用 Cloud Storage 值區 `pubsite_prod_rev_01234567890987654321` 和目標資料集 `mydataset`，建立名為 `My
Transfer` 的 Google Play 資料移轉作業。資料移轉作業會在預設專案中建立：

```
bq mk \
--transfer_config \
--target_dataset=mydataset \
--display_name='My Transfer' \
--params='{"bucket":"pubsite_prod_rev_01234567890987654321","table_suffix":"MT"}' \
--data_source=play
```

首次執行指令時，您會收到如下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照訊息中的操作說明進行，在指令列中貼上驗證碼。

**注意：** 使用指令列工具建立 Google Play 資料移轉作業時，系統會採用「Schedule」(排程) 的預設值 (每 24 小時) 進行移轉設定。

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

// Sample to create a play transfer config.
public class CreatePlayTransfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    String bucket = "gs://cloud-sample-data";
    String tableSuffix = "_test";
    Map<String, Value> params = new HashMap<>();
    params.put("bucket", Value.newBuilder().setStringValue(bucket).build());
    params.put("table_suffix", Value.newBuilder().setStringValue(tableSuffix).build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Play Config Name")
            .setDataSourceId("play")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .build();
    createPlayTransfer(projectId, transferConfig);
  }

  public static void createPlayTransfer(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = client.createTransferConfig(request);
      System.out.println("play transfer created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("play transfer was not created." + ex.toString());
    }
  }
}
```

**警告：** 如果您變更報表的結構定義，則當天所有檔案的結構定義都必須相同，否則當天所有的資料移轉作業都會失敗。

## 排解 Google Play 轉移設定問題

如果您無法順利設定資料移轉作業，請參閱[排解 BigQuery 資料移轉服務移轉設定問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw)。

## 查詢資料

資料移轉至 BigQuery 時，系統會將資料寫入擷取時間分區資料表。詳情請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。

如果您要直接查詢資料表，而不要使用自動產生的檢視表，您必須在查詢中使用 `_PARTITIONTIME` 虛擬資料欄。詳情請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)一文。

## 定價

如要瞭解 Google Play 資料移轉定價，請參閱[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data-transfer-service-pricing)頁面。

資料移轉至 BigQuery 之後，即適用標準的 BigQuery [儲存空間](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)和[查詢](https://cloud.google.com/bigquery/pricing?hl=zh-tw#queries)計價方式。

## 後續步驟

* 如要瞭解 Google Play 報告如何移轉至 BigQuery，請參閱 [Google Play 報告轉換](https://docs.cloud.google.com/bigquery/docs/play-transformation?hl=zh-tw)一文。
* 如需 BigQuery 資料移轉服務的總覽，請參閱
  [BigQuery 資料移轉服務簡介](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。
* 如要瞭解如何使用移轉作業，包括取得移轉設定、列出移轉設定以及查看移轉設定的執行記錄，請參閱[使用移轉功能](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。