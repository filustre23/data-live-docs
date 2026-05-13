Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Amazon S3 資料載入 BigQuery

您可以使用 Amazon S3 專用的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)連接器，將資料從 Amazon S3 載入至 BigQuery。透過 BigQuery 資料移轉服務，您可以安排週期性移轉工作，將 Amazon S3 的最新資料新增至 BigQuery。

## 事前準備

建立 Amazon S3 資料移轉作業前的準備事項如下：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* [建立資料移轉作業的目的地資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create_an_empty_table_with_a_schema_definition)，並指定結構定義。目的地資料表必須遵循[資料表命名規則](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#table_naming)。目的地資料表名稱也支援[參數](https://docs.cloud.google.com/bigquery/docs/s3-transfer-parameters?hl=zh-tw)。您可以建立 BigQuery 資料表或[建立 Iceberg 受管理資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw#create-iceberg-tables)。
* 擷取您的 Amazon S3 URI、存取金鑰 ID，以及私密存取金鑰。如需存取金鑰管理方面的資訊，請參閱 [AWS 說明文件](https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html)。
* 如要為 Pub/Sub 設定移轉作業執行通知，您必須擁有 `pubsub.topics.setIamPolicy` 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

## 限制

Amazon S3 資料移轉作業有下列限制：

* Amazon S3 URI 的值區部分無法參數化。
* 如果從 Amazon S3 移轉資料時，將「寫入處置」參數設為 `WRITE_TRUNCATE`，系統會在每次執行作業時，將所有相符的檔案移轉至 Google Cloud 。這可能會導致額外的 Amazon S3 輸出資料移轉費用。如要進一步瞭解執行期間會轉移哪些檔案，請參閱「[前置字元比對與萬用字元比對的影響](#matching)」。
* 不支援從 AWS GovCloud (`us-gov`) 區域移轉資料。
* 不支援將資料移轉至 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)。
* 視 Amazon S3 來源資料的格式而定，可能還有其他的限制。詳情請參閱：

  + [CSV 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#limitations)
  + [JSON 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#limitations)
  + [巢狀與重複資料的限制](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw#limitations)
* 週期性資料移轉作業之間的最短時間間隔為 1 小時。週期性資料移轉的預設間隔為 24 小時。

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

### 必要的 Amazon S3 角色

參閱 Amazon S3 的說明文件，以確保您已設定啟用資料移轉所需的任何權限。Amazon S3 來源資料至少必須套用 AWS 代管政策 [`AmazonS3ReadOnlyAccess`](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html#attach-managed-policy-console)。

## 設定 Amazon S3 資料移轉作業

如何建立 Amazon S3 資料移轉作業：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Create Transfer」(建立轉移作業) 頁面：

   * 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Amazon S3」。
   * 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
   * 在「Schedule options」(排程選項) 專區：

     + 選取**重複頻率**。如果選取「Hours」(小時)、「Days」(天)、「Weeks」(週)或「Months」(月)，必須一併指定頻率。您也可以選取「Custom」(自訂)，建立專屬的重複頻率。如果選取「On-demand」(隨選)，這項資料移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
     + 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
   * 在「Destination settings」(目的地設定) 部分：

     + 在「Dataset」(資料集) 部分，選取您為了儲存資料而建立的資料集。
     + 如要移轉至 BigQuery 資料表，請選取「Native table」(原生資料表)。
     + 如要移轉至 Iceberg 代管資料表，請選取「Apache Iceberg」。
   * 在「Data source details」(資料來源詳細資料) 區段：

     + 在「Destination table」(目的地資料表)，輸入您為了在 BigQuery 儲存資料而建立的資料表名稱。目的地資料表的名稱支援[參數](https://docs.cloud.google.com/bigquery/docs/s3-transfer-parameters?hl=zh-tw)。
     + 在「Amazon S3 URI」以 `s3://mybucket/myfolder/...` 的格式輸入 URI (支援[參數](https://docs.cloud.google.com/bigquery/docs/s3-transfer-parameters?hl=zh-tw))。
     + 在「Access key ID」(存取金鑰 ID) 輸入您的存取金鑰 ID。
     + 在「Secret access key」(私密存取金鑰) 輸入您的私密存取金鑰。
     + 在「File format」(檔案格式) 選取資料格式：JSON (以換行符號分隔)、CSV、Avro、Parquet 或 ORC。
     + 在「Write Disposition」(寫入配置) 選取下列其中一個選項：
       - 「`WRITE_APPEND`」：逐步將新的資料附加至現有目的地資料表。「Write preference」(寫入偏好設定) 的預設值為 **`WRITE_APPEND`**。
       - 「`WRITE_TRUNCATE`」：每次移轉資料時，覆寫目的地資料表資料。

     如要進一步瞭解 BigQuery 資料移轉服務如何使用 **`WRITE_APPEND`** 或 **`WRITE_TRUNCATE`** 擷取資料，請參閱 [Amazon S3 移轉作業資料擷取](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw#data-ingestion)的相關說明。如要進一步瞭解 `writeDisposition` 欄位，請參閱 [`JobConfigurationLoad`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationload)。
   * 在「Transfer Options - All Formats」(移轉選項 - 所有格式) 部分執行下列操作：

     + 在「Number of errors allowed」(允許的錯誤數量) 部分，輸入可以忽略的損壞記錄數量上限 (整數值)。
     + (選用步驟) 在「Decimal target types」(小數目標類型) 部分，輸入以半形逗號分隔的清單，內含來源小數值可能轉換成的 SQL 資料類型。系統會依據下列條件，選取要轉換的 SQL 資料類型：
       - 系統會按照 NUMERIC、[BIGNUMERIC](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_types) 和 STRING 的順序，選取下列清單中第一個支援來源資料有效位數和小數位數的資料類型，做為要轉換的資料類型。
       - 如果清單中的資料類型都不支援有效位數和小數位數，則會選取指定清單中支援範圍最廣的資料類型。如果讀取來源資料時，值超過支援的範圍，就會擲回錯誤。
       - 資料類型 STRING 支援所有有效位數和小數位數值。
       - 如果將這個欄位留空，ORC 的預設資料類型為「NUMERIC, STRING」(NUMERIC、STRING)，其他檔案格式則為「NUMERIC」。
       - 這個欄位不得含有重複的資料類型。
       - 您在這個欄位提供資料類型時採用的順序不會有影響。
   * 如果您選取的檔案格式為 CSV 或 JSON，請在「JSON, CSV」(JSON、CSV) 部分勾選「Ignore unknown values」(略過不明的值)，接受所含值不符合結構定義的資料列。系統會忽略不明的值。對於 CSV 檔案，此選項會忽略每行結尾處額外的值。
   * 如果您選取的檔案格式為 CSV，請在「CSV」部分針對要載入的資料輸入額外的 [CSV 選項](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#csv-options)。
   * 在「Service Account」(服務帳戶) 選單，選取與您的Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與資料移轉作業建立關聯，這樣就不需要使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。

     + 如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立資料移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立資料移轉作業。
     + 服務帳戶必須具備[必要權限](https://docs.cloud.google.com/bigquery/docs/s3-transfer?hl=zh-tw#required_permissions)。
   * (選用步驟) 在「Notification options」(通知選項) 部分執行下列操作：

     + 點選切換按鈕，啟用電子郵件通知。啟用這個選項之後，若資料移轉失敗，移轉作業管理員就會收到電子郵件通知。
     + 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對資料移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
4. 按一下 [儲存]。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。

```
bq mk \
--transfer_config \
--project_id=project_id \
--data_source=data_source \
--display_name=name \
--target_dataset=dataset \
--service_account_name=service_account \
--params='parameters'
```

其中：

* project\_id：選用。您的 Google Cloud 專案 ID。
  如未提供 `--project_id` 指定特定專案，系統會使用預設專案。
* data\_source：必填，資料來源：`amazon_s3`。
* display\_name：必填，資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* dataset：必填，資料移轉設定的目標資料集。
* service\_account：用於驗證資料移轉的服務帳戶名稱。服務帳戶應由用於建立資料移轉的 `project_id` 擁有，且應具備所有[必要權限](#required_permissions)。
* parameters：必填，已建立移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。以下是 Amazon S3 移轉作業的參數：

  + destination\_table\_name\_template：必填，目的地資料表的名稱。
  + data\_path：必填，Amazon S3 URI，格式如下：

    `s3://mybucket/myfolder/...`

    URI 也支援[參數](https://docs.cloud.google.com/bigquery/docs/s3-transfer-parameters?hl=zh-tw)。
  + access\_key\_id：必填，存取金鑰 ID。
  + secret\_access\_key：必填，您的存取金鑰。
  + file\_format：選用。指出要轉移的檔案類型：`CSV`、`JSON`、`AVRO`、`PARQUET` 或 `ORC`。預設值為 `CSV`。
  + write\_disposition：選用。`WRITE_APPEND` 只會轉移上次成功執行後修改的檔案。`WRITE_TRUNCATE` 會轉移所有相符的檔案，包括先前轉移的檔案。預設值為 `WRITE_APPEND`。
  + max\_bad\_records：選用。允許的損壞記錄數量。預設值為 `0`。
  + decimal\_target\_types：選用。以半形逗號分隔的清單，內含來源小數值可能轉換成的 SQL 資料類型。如果未提供這個欄位，ORC 的預設資料類型為「NUMERIC,STRING」(NUMERIC、STRING)，其他檔案格式則為「NUMERIC」。
  + ignore\_unknown\_values：選用屬性，如果 file\_format 不是 `JSON` 或 `CSV`，系統會忽略這個屬性。是否要忽略資料中的不明值。
  + field\_delimiter：選用，僅適用於 `file_format` 為 `CSV` 的情況。分隔欄位的字元。預設值為逗號。
  + skip\_leading\_rows：選用，僅適用於 file\_format 為 `CSV` 的情況。指出您不想匯入的標題列數。預設值為 `0`。
  + allow\_quoted\_newlines：選用，僅適用於 file\_format 為 `CSV` 的情況。指出是否允許在引用欄位中使用換行符號。
  + allow\_jagged\_rows：選用，僅適用於 file\_format 為 `CSV` 的情況。指出是否接受缺少結尾選用欄的資料列。缺少的值將以 NULL 填入。

**注意：** 您無法使用指令列工具設定通知。

舉例來說，下列指令會使用 `s3://mybucket/myfile/*.csv` 的 `data_path` 值、目標資料集 `mydataset` 以及 `file_format`
`CSV`，建立名為 `My Transfer` 的 Amazon S3 資料移轉作業。本範例包含有關 `CSV` file\_format 的選用參數非預設值。

資料移轉作業會在預設專案中建立：

```
bq mk --transfer_config \
--target_dataset=mydataset \
--display_name='My Transfer' \
--params='{"data_path":"s3://mybucket/myfile/*.csv",
"destination_table_name_template":"MyTable",
"file_format":"CSV",
"write_disposition":"WRITE_APPEND",
"max_bad_records":"1",
"ignore_unknown_values":"true",
"field_delimiter":"|",
"skip_leading_rows":"1",
"allow_quoted_newlines":"true",
"allow_jagged_rows":"false"}' \
--data_source=amazon_s3
```

執行指令後，您會收到如下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照指示進行操作，並在指令列中貼上驗證碼。

**注意：** 使用指令列工具建立 Amazon S3 資料移轉作業時，系統會採用「Schedule」(排程) 的預設值 (每 24 小時) 進行移轉設定。

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

// Sample to create amazon s3 transfer config.
public class CreateAmazonS3Transfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    String tableId = "MY_TABLE_ID";
    // Amazon S3 Bucket Uri with read role permission
    String sourceUri = "s3://your-bucket-name/*";
    String awsAccessKeyId = "MY_AWS_ACCESS_KEY_ID";
    String awsSecretAccessId = "AWS_SECRET_ACCESS_ID";
    String sourceFormat = "CSV";
    String fieldDelimiter = ",";
    String skipLeadingRows = "1";
    Map<String, Value> params = new HashMap<>();
    params.put(
        "destination_table_name_template", Value.newBuilder().setStringValue(tableId).build());
    params.put("data_path", Value.newBuilder().setStringValue(sourceUri).build());
    params.put("access_key_id", Value.newBuilder().setStringValue(awsAccessKeyId).build());
    params.put("secret_access_key", Value.newBuilder().setStringValue(awsSecretAccessId).build());
    params.put("source_format", Value.newBuilder().setStringValue(sourceFormat).build());
    params.put("field_delimiter", Value.newBuilder().setStringValue(fieldDelimiter).build());
    params.put("skip_leading_rows", Value.newBuilder().setStringValue(skipLeadingRows).build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Aws S3 Config Name")
            .setDataSourceId("amazon_s3")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .setSchedule("every 24 hours")
            .build();
    createAmazonS3Transfer(projectId, transferConfig);
  }

  public static void createAmazonS3Transfer(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
```