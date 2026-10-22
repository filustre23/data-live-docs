Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 搭配使用服務帳戶和 BigQuery 資料移轉服務

BigQuery 資料移轉服務可讓您使用[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw) (而非個別使用者憑證)，驗證支援資料來源的資料移轉作業。服務帳戶是與 Google Cloud 專案相關聯的 Google 帳戶，可執行排定的查詢或批次處理管道等工作。您可以透過 Google Cloud 控制台、API 或 `bq` 指令列設定服務帳戶驗證，並在憑證變更時[更新現有移轉作業](#update_data_transfer_credentials)。

下列錯誤代碼表示您必須更新憑證：

* 轉移作業無法授權使用者存取資料來源：

  `Error code 401 : Request is missing required authentication credential. UNAUTHENTICATED`
* 嘗試執行移轉作業時，收到 **INVALID\_USER** 錯誤：

  `Error code 5 : Authentication failure: User Id not found. Error code: INVALID_USERID`

如要進一步瞭解如何使用服務帳戶進行驗證，請參閱「[驗證簡介](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#sa-impersonation)」。

## 支援服務帳戶的資料來源

BigQuery 資料移轉服務可使用服務帳戶憑證，透過下列方式進行移轉：

* [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw)
* [Amazon Redshift](https://docs.cloud.google.com/bigquery/docs/migration/redshift-overview?hl=zh-tw)
* [Amazon S3](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw)
* [Campaign Manager](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw)
* [碳足跡](https://docs.cloud.google.com/carbon-footprint/docs/export?hl=zh-tw)
* [資料集副本](https://docs.cloud.google.com/bigquery/docs/copying-datasets?hl=zh-tw)
* [Display & Video 360](https://docs.cloud.google.com/bigquery/docs/display-video-transfer?hl=zh-tw)
* [Google Ad Manager](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transfer?hl=zh-tw)
* [Google Ads](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)
* [Google Merchant Center](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-tw)
* [Google Play](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw)
* [已排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#using_a_service_account)
* [Search Ads 360](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw)
* [Teradata](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw)
* [YouTube 內容擁有者](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw)

## 事前準備

* 確認您已完成「[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)」中的所有必要動作。
* 授予 Identity and Access Management (IAM) 角色，讓使用者具備執行本文件中各項工作所需的權限。

### 所需權限

如要更新資料移轉作業，改用服務帳戶，您必須具備下列權限：

* 修改移轉作業的 `bigquery.transfers.update` 權限。

  預先定義的 `roles/bigquery.admin` IAM 角色包含這項權限。
* 服務帳戶的存取權。如要進一步瞭解如何授予使用者服務帳戶角色，請參閱「[服務帳戶使用者角色](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#user-role)」。

請確認您選擇執行移轉作業的服務帳戶具備下列權限：

* 目標資料集的 `bigquery.datasets.get` 和 `bigquery.datasets.update` 權限。如果資料表使用[資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)，服務帳戶也必須具備 `bigquery.tables.setCategory` 權限。

  `bigquery.admin` 預先定義的 IAM 角色包含所有這些權限。如要進一步瞭解 BigQuery 資料移轉服務中的 IAM 角色，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。
* 已設定的移轉資料來源存取權。如要進一步瞭解不同資料來源所需的權限，請參閱「[支援服務帳戶的資料來源](#data_sources_with_service_account_support)」。
* 如果是 Google Ads 移轉作業，服務帳戶必須具備全網域授權。詳情請參閱 [Google Ads API 服務帳戶指南](https://developers.google.com/google-ads/api/docs/oauth/service-accounts?hl=zh-tw#service_account_access_setup)。

## 更新資料移轉憑證

您可以使用服務帳戶的憑證，更新現有的資料移轉作業。下列情況需要更新憑證：

* 轉移作業無法授權使用者存取資料來源：

  `Error code 401 : Request is missing required authentication credential. UNAUTHENTICATED`
* 嘗試執行移轉作業時，收到 **INVALID\_USER** 錯誤：

  `Error code 5 : Authentication failure: User Id not found. Error code: INVALID_USERID`

### 控制台

下列程序會更新資料移轉設定，改為以服務帳戶 (而非個人使用者帳戶) 進行驗證。

1. 在 Google Cloud 控制台中，前往「Data transfers」(資料移轉) 頁面。

   [前往「資料移轉」](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 在資料移轉作業清單中，按一下要查看的移轉作業。
3. 按一下「EDIT」(編輯)，更新移轉設定。
4. 在「Service Account」(服務帳戶) 欄位中，輸入服務帳戶名稱。
5. 按一下 [儲存]。

### bq

如要更新資料移轉作業的憑證，可以使用 bq 指令列工具更新移轉設定。

使用 `bq update` 指令，並加上 `--transfer_config`、`--update_credentials` 和 `--service_account_name` 旗標。

舉例來說，下列指令會更新資料移轉設定，以服務帳戶 (而非個別使用者帳戶) 的身分進行驗證：

```
bq update \
--transfer_config \
--update_credentials \
--service_account_name=abcdef-test-sa@abcdef-test.iam.gserviceaccount.com projects/862514376110/locations/us/transferConfigs/5dd12f26-0000-262f-bc38-089e0820fe38
```

**注意：** 如果您使用的是 bq 指令列工具，請使用 `--service_account_name` 旗標，不要以服務帳戶身分驗證。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-21 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-21 (世界標準時間)。"],[],[]]