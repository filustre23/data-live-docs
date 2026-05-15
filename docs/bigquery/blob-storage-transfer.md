Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Blob 儲存體資料載入 BigQuery

您可以使用 Blob Storage 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 Blob Storage 載入 BigQuery。您可以使用 BigQuery 資料移轉服務，安排週期性移轉工作，將 Blob 儲存空間中的最新資料新增至 BigQuery。

## 事前準備

建立 Blob Storage 資料移轉作業前，請完成下列事項：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* 選擇現有的 BigQuery 資料集，或[建立新的資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存資料。
* 選擇現有的 BigQuery 資料表，或[建立新的資料移轉目的地資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create_an_empty_table_with_a_schema_definition)，並指定結構定義。目的地資料表必須遵循[資料表命名規則](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#table_naming)。目的地資料表名稱也支援[參數](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-parameters?hl=zh-tw)。您可以建立 BigQuery 資料表或[建立 Iceberg 受管理資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw#create-iceberg-tables)。
* 擷取 Blob 儲存體帳戶名稱、容器名稱、資料路徑 (選用) 和 SAS 權杖。如要瞭解如何使用共用存取簽章 (SAS) 授予 Blob 儲存空間存取權，請參閱「[共用存取簽章 (SAS)](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#shared-access-signature)」。
* 如果使用 Azure Storage 防火牆限制 Azure 資源的存取權，請[將 BigQuery 資料移轉服務工作人員新增至允許的 IP 清單](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#ip_restrictions)。
* 如果您打算指定客戶自行管理的加密金鑰 (CMEK)，請確保[服務帳戶具有加密和解密權限](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#grant_permission)，且您擁有使用 CMEK 時所需的 [Cloud KMS 金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱[指定移轉作業加密金鑰](#CMEK)。

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

### 必要的 Blob Storage 角色

如要瞭解在 Blob 儲存空間中啟用資料移轉所需的權限，請參閱「[共用存取簽章 (SAS)](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#shared-access-signature)」。

## 限制

Blob 儲存空間資料移轉作業有下列限制：

* 週期性資料移轉作業之間的最短時間間隔為 1 小時。預設間隔為 24 小時。
* 視 Blob 儲存體來源資料的格式而定，可能還有其他的限制：
  + [CSV 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#limitations)
  + [JSON 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#limitations)
  + [巢狀與重複資料的限制](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw#limitations)
* 不支援將資料移轉至 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)。

## 設定 Blob 儲存體資料移轉作業

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Create transfer」(建立轉移作業)頁面執行下列操作：

   * 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Azure Blob Storage & ADLS」(Azure Blob 儲存體和 ADLS)：
   * 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業名稱。
   * 在「Schedule options」(排程選項) 部分，請執行下列操作：

     + 選取**重複頻率**。如果選取「Hours」(小時)、「Days」(天)、「Weeks」(週)或「Months」(月)，必須一併指定頻率。您也可以選取「Custom」(自訂)，指定重複頻率。如果選取「On-demand」(隨選)，這項資料移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
     + 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
   * 在「Destination settings」(目的地設定) 部分：

     + 在「Dataset」(資料集) 部分，選取您為了儲存資料而建立的資料集。
     + 如要移轉至 BigQuery 資料表，請選取「Native table」(原生資料表)。
     + 如要移轉至 Iceberg 代管資料表，請選取「Apache Iceberg」。
   * 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

     + 在「Destination table」(目的地資料表)，輸入您為了在 BigQuery 儲存資料而建立的資料表名稱。目的地資料表名稱支援[參數](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-parameters?hl=zh-tw)。
     + 在「Azure storage account name」(Azure 儲存體帳戶名稱)，輸入 Blob 儲存體帳戶名稱。
     + 在「Container name」(容器名稱)，輸入 Blob 儲存體容器名稱。
     + 在「Data path」(資料路徑) 部分輸入路徑，篩選出要移轉的檔案。
       [查看示例](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#azure_blob_storage_data_path_examples)。
     + 在「SAS token」(SAS 權杖) 部分輸入 Azure SAS 權杖。
     + 在「File format」(檔案格式) 選取來源資料格式。
     + 在「Write disposition」(寫入配置) 部分，選取 **`WRITE_APPEND`** 可以陸續將新的資料附加至目的地資料表；選取 **`WRITE_TRUNCATE`** 則可在每次移轉資料時覆寫目的地資料表資料。「Write disposition」(寫入配置) 的預設值為 **`WRITE_APPEND`**。

     如要進一步瞭解 BigQuery 資料移轉服務如何使用 **`WRITE_APPEND`** 或 **`WRITE_TRUNCATE`** 擷取資料，請參閱 [Azure Blob 移轉作業資料擷取](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#data-ingestion)的相關說明。如要進一步瞭解 `writeDisposition` 欄位，請參閱 [`JobConfigurationLoad`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationload)。
   * 在「Transfer options」(移轉作業選項) 部分執行下列操作：

     + 在「Number of errors allowed」(允許的錯誤數量) 部分，輸入可以忽略的損壞記錄數量上限 (整數值)，預設值為 0。
     + (選用步驟) 在「Decimal target types」(小數目標類型) 部分，輸入以半形逗號分隔的清單，內含來源資料內小數值可能轉換成的 SQL 資料類型。系統會依據下列條件，選取要轉換的 SQL 資料類型：
       - 系統會按照 `NUMERIC`、`BIGNUMERIC` 和 `STRING` 的順序，選取指定清單中支援的有效位數和小數位數類型。
       - 如果清單中的資料類型都不支援有效位數和小數位數，則會選取指定清單中支援範圍最廣的資料類型。如果讀取來源資料時，值超過支援的範圍，就會擲回錯誤。
       - 資料類型 `STRING` 支援所有有效位數和小數位數值。
       - 如果將這個欄位留空，ORC 的預設資料類型為 `NUMERIC,STRING`，其他檔案格式則為 `NUMERIC`。
       - 這個欄位不得含有重複的資料類型。
       - 您提供資料類型時採用的順序不會有影響。
   * 如果您選取的檔案格式為 CSV 或 JSON，請在「JSON, CSV」(JSON、CSV) 部分勾選「Ignore unknown values」(略過不明的值)，接受所含值不符合結構定義的資料列。
   * 如果您選取的檔案格式為 CSV，請在「CSV」部分針對要載入的資料輸入[額外的 CSV 選項](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#csv-options)。
   * 在「Notification options」(通知選項) 部分，您可以選擇啟用電子郵件通知和 Pub/Sub 通知。

     + 啟用電子郵件通知之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
     + 啟用 [Pub/Sub 通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw#notifications)時，請選取要發布的[主題](https://docs.cloud.google.com/pubsub/docs/admin?hl=zh-tw)名稱，或是點選「Create a topic」(建立主題) 來建立主題。
   * 如果使用 [CMEK](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)，請在「Advanced options」(進階選項) 部分選取「Customer-managed key」(客戶管理的金鑰)。畫面隨即會列出可用的 CMEK 供您選擇。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱[指定移轉作業加密金鑰](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer?hl=zh-tw#CMEK)的相關說明。
4. 按一下 [儲存]。

### bq

使用 [`bq mk --transfer_config` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-transfer-config)建立 Blob 儲存體移轉作業：

```
bq mk \
  --transfer_config \
  --project_id=PROJECT_ID \
  --data_source=DATA_SOURCE \
  --display_name=DISPLAY_NAME \
  --target_dataset=DATASET \
  --destination_kms_key=DESTINATION_KEY \
  --params=PARAMETERS
```

更改下列內容：

* `PROJECT_ID`：(選用) 包含目標資料集的專案 ID。如未指定，系統會使用預設專案。
* `DATA_SOURCE`: `azure_blob_storage`.
* `DISPLAY_NAME`：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* `DATASET`：資料移轉設定的目標資料集。
* `DESTINATION_KEY`：(選用) [Cloud KMS 金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)，例如 `projects/project_name/locations/us/keyRings/key_ring_name/cryptoKeys/key_name`。
* `PARAMETERS`：資料移轉設定的參數，以 JSON 格式列出。例如：`--params={"param1":"value1", "param2":"value2"}`。以下是 Blob 儲存體資料移轉作業的參數：
  + `destination_table_name_template`：必填，目的地資料表的名稱。
  + `storage_account`：必填，Blob 儲存體帳戶名稱。
  + `container`：必填，Blob 儲存體容器名稱。
  + `data_path`：選用。篩選出要移轉的檔案路徑。請參閱[範例](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw#azure_blob_storage_data_path_examples)。
  + `sas_token`：必填，Azure SAS 權杖。
  + `file_format`：選用。要移轉的檔案類型：`CSV`、`JSON`、`AVRO`、`PARQUET` 或 `ORC`。預設值為 `CSV`。
  + `write_disposition`：選用。選取 `WRITE_APPEND` 可將資料附加至目的地資料表，選取 `WRITE_TRUNCATE` 則可覆寫目的地資料表中的資料。預設值為 `WRITE_APPEND`。
  + `max_bad_records`：選用。允許的損壞記錄數量。預設值為 0。
  + `decimal_target_types`：選用。以半形逗號分隔的清單，內含來源資料內小數值可能轉換成的 SQL 資料類型。如果未提供這個欄位，ORC 的預設資料類型為 `NUMERIC,STRING`，其他檔案格式則為 `NUMERIC`。
  + `ignore_unknown_values`：選用，如果 `file_format` 不是 `JSON` 或 `CSV`，系統會忽略這個值。設為 `true` 即可接受含有與結構定義不符值的資料列。
  + `field_delimiter`：選用，僅適用於 `file_format` 為 `CSV` 的情況。分隔欄位的字元。預設值為 `,`。
  + `skip_leading_rows`：選用，僅適用於 `file_format` 為 `CSV` 的情況。指出您不想匯入的標題列數。預設值為 0。
  + `allow_quoted_newlines`：選用，僅適用於 `file_format` 為 `CSV` 的情況。指出是否允許在引用欄位中使用換行符號。
  + `allow_jagged_rows`：選用，僅適用於 `file_format` 為 `CSV` 的情況。指出是否接受缺少結尾自選欄的資料列。缺少的值會填入 `NULL`。

舉例來說，下列指令會建立名為 `mytransfer` 的 Blob 儲存體資料移轉作業：

```
bq mk \
  --transfer_config \
  --data_source=azure_blob_storage \
  --display_name=mytransfer \
  --target_dataset=mydataset \
  --destination_kms_key=projects/myproject/locations/us/keyRings/mykeyring/cryptoKeys/key1
  --params={"destination_table_name_template":"mytable",
      "storage_account":"myaccount",
      "container":"mycontainer",
      "data_path":"myfolder/*.csv",
      "sas_token":"my_sas_token_value",
      "file_format":"CSV",
      "max_bad_records":"1",
      "ignore_unknown_values":"true",
      "field_delimiter":"|",
      "skip_leading_rows":"1",
      "allow_quoted_newlines":"true",
      "allow_jagged_rows":"false"}
```

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

// Sample to create azure blob storage transfer config.
public class CreateAzureBlobStorageTransfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    final String displayName = "MY_TRANSFER_DISPLAY_NAME";
    final String datasetId = "MY_DATASET_ID";
    String tableId = "MY_TABLE_ID";
    String storageAccount = "MY_AZURE_STORAGE_ACCOUNT_NAME";
    String containerName = "MY_AZURE_CONTAINER_NAME";
    String dataPath = "MY_AZURE_FILE_NAME_OR_PREFIX";
    String sasToken = "MY_AZURE_SAS_TOKEN";
    String fileFormat = "CSV";
    String fieldDelimiter = ",";
    String skipLeadingRows = "1";
    Map<String, Value> params = new HashMap<>();
    params.put(
        "destination_table_name_template", Value.newBuilder().setStringValue(tableId).build());
    params.put("storage_account", Value.newBuilder().setStringValue(storageAccount).build());
    params.put("container", Value.newBuilder().setStringValue(containerName).build());
    params.put("data_path", Value.newBuilder().setStringValue(dataPath).build());
    params.put("sas_token", Value.newBuilder().setStringValue(sasToken).build());
    params.put("file_format", Value.newBuilder().setStringValue(fileFormat).build());
    params.put("field_delimiter", Value.newBuilder().setStringValue(fieldDelimiter).build());
    params.put("skip_leading_rows", Value.newBuilder().setStringValue(skipLeadingRows).build());
    createAzureBlobStorageTransfer(projectId, displayName, datasetId, params);
  }

  public static void createAzureBlobStorageTransfer(
      String projectId, String displayName, String datasetId, Map<String, Value> params)
      throws IOException {
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName(displayName)
            .setDataSourceId("azure_blob_storage")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .setSchedule("every 24 hours")
            .build();
    // Initialize client that will be used to send requests. This client only needs to be created
    // once, and can be reused for multiple requests.
    try (
```