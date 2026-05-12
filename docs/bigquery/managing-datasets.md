Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理資料集

本文說明如何在 BigQuery 中複製資料集、在其他位置重建資料集、保護資料集、刪除資料集，以及從已刪除的資料集還原資料表。如要瞭解如何還原 (或*取消刪除*) 已刪除的資料集，請參閱[還原已刪除的資料集](https://docs.cloud.google.com/bigquery/docs/restore-deleted-datasets?hl=zh-tw)。

BigQuery 管理員可以整理分析師使用的[資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)和[檢視區塊](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)，並控管存取權。如要進一步瞭解資料集，請參閱「[資料集簡介](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw)」。

現有資料集的名稱無法變更，資料集建立後也無法搬移。如要變更資料集名稱，可以[複製資料集](#copy-datasets)，然後變更目的地資料集的名稱。如要遷移資料集，請按照下列其中一種方法操作：

* [在其他位置重新建立資料集](#recreate-dataset)。
* [複製資料集](#copy-datasets)。

## 必要的角色

本節說明管理資料集所需的角色和權限。如果來源或目的地資料集與您用於複製的專案位於同一專案，則您不需要該資料集的額外權限或角色。

### 複製資料集

授予這些角色，即可複製資料集。複製資料集的功能目前為 [Beta 版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要取得複製資料集所需的權限，請要求系統管理員授予您下列 IAM 角色：

* BigQuery 管理員 (`roles/bigquery.admin`) - 目的地專案
* BigQuery 資料檢視者 (`roles/bigquery.dataViewer`) - 來源資料集
* BigQuery 資料編輯者 (`roles/bigquery.dataEditor`) - 目的地資料集

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備複製資料集所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要複製資料集，必須具備下列權限：

* `bigquery.transfers.update`
  目標專案
* `bigquery.jobs.create`
  目標專案
* `bigquery.datasets.get`
  來源和目的地資料集
* `bigquery.tables.list`
  來源和目的地資料集
* `bigquery.datasets.update`
  目的地資料集
* `bigquery.tables.create`
  目的地資料集

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 刪除資料集

授予這些角色，即可刪除資料集。

如要取得刪除資料集所需的權限，請要求系統管理員授予您專案的「[BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner) 」(`roles/bigquery.dataOwner`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備刪除資料集所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要刪除資料集，您必須具備下列權限：

* 專案的 `bigquery.datasets.delete`
* `bigquery.tables.delete`
  專案

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 複製資料集

**Beta 版**

這項產品適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

您不需要擷取、移動或重新載入資料到 BigQuery 中，即可複製資料集，包括區域內或跨區域的分區資料。BigQuery 會在後端使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)複製資料集。如要瞭解資料移轉時的位置注意事項，請參閱「[資料位置和移轉作業](https://docs.cloud.google.com/bigquery/docs/dts-locations?hl=zh-tw)」。

針對每一個資料集複製作業設定，一次可以有一個有效副本。其他移轉作業已排入佇列。如果您使用 Google Cloud 控制台，可以透過 BigQuery 資料移轉服務排定週期性複製作業，並設定電子郵件或 Pub/Sub 通知。

### 限制

複製資料集時，請注意以下限制：

* 您無法從來源資料集複製下列資源：

  + 觀看次數。
  + 常式，包括使用者定義函式。
  + 外部資料表。
  + 如果複製工作跨地區，則為[變更資料擷取 (CDC) 資料表](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)。系統支援在同一區域內複製 CDC 資料表。
  + 如果目的地資料集未以 CMEK 加密，且未提供 CMEK，則以[客戶管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) 加密的資料表不支援跨區域資料表複製工作。跨地區複製作業支援複製以預設方式加密的資料表。

    您可以複製同一個區域內的所有加密資料表，包括以 CMEK 加密的資料表。
* 您無法將下列資源做為複製工作的目標資料集：

  + 寫入最佳化儲存空間。
  + 如果複製作業跨越區域，且來源資料表未以 CMEK 加密，則資料集會以 CMEK 加密。

    不過，在同地區複製作業中，允許以 CMEK 加密的資料表做為目的地資料表。
* 複製作業之間的時間間隔下限為 12 小時。
* 不支援將資料附加到目的地資料集中的分區或非分區資料表。如果來源資料表沒有變更，系統會略過該資料表。如果來源資料表更新，目的地資料表會完全截斷並取代。
* 如果來源資料集和目的地資料集中有資料表，且來源資料表上次成功複製後沒有任何變更，就會略過此資料表。即使勾選「覆寫目標資料表」核取方塊，系統仍會略過來源資料表。
* 截斷目的地資料集中的資料表時，資料集複製作業不會偵測對目的地資料集資源所做的任何變更，然後才會開始複製作業。資料集複製作業會覆寫目的地資料集中的所有資料，包括資料表和結構定義。
* 複製作業開始後，目的地資料表可能不會反映來源資料表的變更。
* [BigQuery Omni 區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)不支援複製資料集。
* 如要將資料集複製到另一個 [VPC Service Controls 服務邊界](https://docs.cloud.google.com/vpc-service-controls/docs/service-perimeters?hl=zh-tw)的專案，請設定下列輸出規則：

  + 在目標專案的 VPC Service Controls 服務邊界設定中，IAM 主體必須具備下列方法：

    - `bigquery.datasets.get`
    - `bigquery.tables.list`
    - `bigquery.tables.get`、
    - `bigquery.tables.getData`
  + 在來源專案的 VPC Service Controls 服務範圍設定中，使用的 IAM 主體必須將方法設為 `All Methods`。
* 如果您嘗試更新不屬於自己的資料集副本移轉設定，更新作業可能會失敗，並顯示下列錯誤訊息：

  `Cannot modify restricted parameters without taking ownership of the transfer configuration.`

  資料集副本的擁有者是與資料集副本相關聯的使用者，或是可存取與資料集副本相關聯服務帳戶的使用者。您可以在資料集副本的[設定詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#get_transfer_details)中查看相關聯的使用者。如要瞭解如何更新資料集副本以取得擁有權，請參閱「[更新憑證](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#update_credentials)」。如要授予使用者服務帳戶的存取權，您必須具備[服務帳戶使用者角色](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#user-role)。

  資料集副本的擁有者受限參數如下：

  + 來源專案
  + 來源資料集
  + 目的地資料集
  + 覆寫目的地資料表設定
* 適用所有[跨區域複製資料表的限制](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#limitations)。

### 複製資料集

選取下列選項之一：

### 控制台

1. 為目的地資料集[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)。

   [啟用 BigQuery 資料移轉服務 API](https://console.cloud.google.com/apis/library/bigquerydatatransfer.googleapis.com?hl=zh-tw)
2. 確認您具備[必要角色](#required-roles)。

   如要為 Pub/Sub 設定移轉作業執行通知 (請參閱後續步驟的「**做法 2**」)，您必須擁有 `pubsub.topics.setIamPolicy` 權限。

   如果您只設定電子郵件通知，則不需要 Pub/Sub 權限。詳情請參閱 BigQuery 資料移轉服務的[執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
3. 在與來源資料集相同或不同的地區[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。

**選項 1：使用 BigQuery 複製函式**

如要建立一次性移轉作業，請使用 BigQuery 複製功能：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 content\_copy「複製」，然後執行下列操作：

   1. 在「資料集」欄位中，建立新的資料集，或從清單中選取現有的資料集 ID。

      同一專案中的資料集名稱不得重複。專案和資料集可能位於不同地區，但並非所有地區都支援跨區資料集複製功能。

      「位置」欄位會顯示來源資料集的位置。
   2. 選用：如要覆寫目的地資料表的資料和結構定義，請勾選「覆寫目的地資料表」核取方塊。來源和目的地資料表必須具有相同的分割區結構定義。
   3. 如要複製資料集，請按一下「複製」。

**選項 2：使用 BigQuery 資料移轉服務**

如要排定定期複製作業，並設定電子郵件或 Pub/Sub 通知，請在目的地專案的 Google Cloud 控制台中使用 BigQuery 資料移轉服務：

1. 前往「資料轉移」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「建立轉移作業」。
3. 在「來源」清單中，選取「資料集副本」。
4. 在「顯示名稱」欄位中，輸入移轉作業的名稱。
5. 在「Schedule options」(排程選項) 部分執行下列操作：

   1. 在「Repeat frequency」(重複頻率) 部分，選擇移轉作業的執行頻率：

      如果選取「自訂」，請輸入自訂頻率，例如 `every day 00:00`。詳情請參閱「[設定時間表格式](https://docs.cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml?hl=zh-tw#formatting_the_schedule)」。

      **注意：** 複製工作之間的時間間隔不得少於 12 小時。
   2. 在「Start date and run time」(開始日期和執行時間) 部分，輸入開始移轉的日期與時間。如果您選擇 [Start now] (立即開始)，系統就會停用這個選項。
6. 在「Destination settings」(目的地設定) 部分，選取目的地資料集來儲存移轉資料。您也可以點選「建立新的資料集」，先建立新的資料集，再選取要轉移的資料集。
7. 在「Data source details」(資料來源詳細資料) 區段中，輸入下列資訊：

   1. 針對「Source dataset」(來源資料集)，輸入要複製的資料集 ID。
   2. 針對「Source project」(來源專案)，請輸入來源資料集的專案 ID。
8. 如要使用來源資料表覆寫目的地資料表的資料和結構定義，請選取「覆寫目的地資料表」核取方塊。來源和目的地資料表必須具有相同的分割結構定義。
9. 在「Service Account」(服務帳戶) 選單，選取與貴機構Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與移轉作業建立關聯，這樣就不需要使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。

   * 如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立移轉作業。
   * 服務帳戶必須具備[必要角色](#required-roles)。
10. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

    * 如要啟用電子郵件通知，請點選切換按鈕。啟用這個選項之後，若移轉失敗，移轉設定的擁有者會收到電子郵件通知。
    * 如要啟用 Pub/Sub 通知，請點選切換按鈕，然後從清單中選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「建立主題」。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
11. 按一下 [儲存]。

### bq

1. 為目的地資料集[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)。
2. 確認您具備[必要角色](#required-roles)。
3. 如要[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，請使用 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)，並搭配資料集建立旗標 `--dataset` 和 `location` 旗標：

   ```
   bq mk \
     --dataset \
     --location=LOCATION \
     PROJECT:DATASET
   ```

   更改下列內容：

   * `LOCATION`：要複製資料集的位置
   * `PROJECT`：目標資料集的專案 ID
   * `DATASET`：目標資料集的名稱
4. 如要複製資料集，請使用 `bq mk` 指令，搭配轉移建立旗標 [`--transfer_config`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-transfer-config) 和 `--data_source` 旗標。您必須將 `--data_source` 標記設為 `cross_region_copy`。如需 `--data_source` 旗標的有效值完整清單，請參閱 bq 指令列工具參考資料中的[傳輸設定旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-transfer-config)。

   ```
   bq mk \
     --transfer_config \
     --project_id=PROJECT \
     --data_source=cross_region_copy \
     --target_dataset=DATASET \
     --display_name=NAME \
    --service_account_name=SERCICE_ACCOUNT \
     --params='PARAMETERS'
   ```

   更改下列內容：

   * `NAME`：複製作業或移轉設定的顯示名稱
   * `SERVICE_ACCOUNT`：用於驗證轉移作業的服務帳戶名稱。服務帳戶應由用於建立轉移作業的同一 `project_id` 所擁有，且應具備所有[必要權限](#required-roles)。
   * `PARAMETERS`：JSON 格式的移轉設定參數

     資料集複製作業設定的參數如下：

     + `source_dataset_id`：要複製的來源資料集 ID
     + `source_project_id`：來源資料集所在專案的 ID
     + `overwrite_destination_table`：選用旗標，可截斷前一個副本的資料表並重新整理所有資料

     來源和目的地資料表必須具有相同的分割區結構定義。

   以下範例會根據系統環境，顯示參數的格式：

   * **Linux：**使用單引號括住 JSON 字串，例如：

     ```
     '{"source_dataset_id":"mydataset","source_project_id":"mysourceproject","overwrite_destination_table":"true"}'
     ```
   * **Windows 指令列：**使用雙引號括住 JSON 字串，並以反斜線逸出字串中的雙引號，例如：

     ```
     "{\"source_dataset_id\":\"mydataset\",\"source_project_id\":\"mysourceproject\",\"overwrite_destination_table\":\"true\"}"
     ```
   * **PowerShell：**使用單引號括住 JSON 字串，並以反斜線逸出字串中的雙引號，例如：

     ```
     '{\"source_dataset_id\":\"mydataset\",\"source_project_id\":\"mysourceproject\",\"overwrite_destination_table\":\"true\"}'
     ```

   舉例來說，下列指令會分別建立名為 `My Transfer` 的資料集副本設定、名為 `mydataset` 的目標資料集和 ID 為 `myproject` 的專案。

   ```
   bq mk \
     --transfer_config \
     --project_id=myproject \
     --data_source=cross_region_copy \
     --target_dataset=mydataset \
     --display_name='My Transfer' \
     --params='{
         "source_dataset_id":"123_demo_eu",
         "source_project_id":"mysourceproject",
         "overwrite_destination_table":"true"
         }'
   ```

### API

1. 為目的地資料集[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)。
2. 確認您具備[必要角色](#required-roles)。
3. 如要[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，請使用已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法。
4. 如要複製資料集，請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

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

// Sample to copy dataset from another gcp project
public class CopyDataset {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String destinationProjectId = "MY_DESTINATION_PROJECT_ID";
    final String destinationDatasetId = "MY_DESTINATION_DATASET_ID";
    final String sourceProjectId = "MY_SOURCE_PROJECT_ID";
    final String sourceDatasetId = "MY_SOURCE_DATASET_ID";
    Map<String, Value> params = new HashMap<>();
    params.put("source_project_id", Value.newBuilder().setStringValue(sourceProjectId).build());
    params.put("source_dataset_id", Value.newBuilder().setStringValue(sourceDatasetId).build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(destinationDatasetId)
            .setDisplayName("Your Dataset Copy Name")
            .setDataSourceId("cross_region_copy")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .setSchedule("every 24 hours")
            .build();
    copyDataset(destinationProjectId, transferConfig);
  }

  public static void copyDataset(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = dataTransferServiceClient.createTransferConfig(request);
      System.out.println("Copy dataset created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("Copy dataset was not created." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 `pip install google-cloud-bigquery-datatransfer` 安裝 [BigQuery Data Transfer API 的 Python 用戶端](https://docs.cloud.google.com/python/docs/reference/bigquerydatatransfer/latest?hl=zh-tw)。然後建立移轉設定，複製資料集。

```
from google.cloud import bigquery_datatransfer

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

destination_project_id = "my-destination-project"
destination_dataset_id = "my_destination_dataset"
source_project_id = "my-source-project"
source_dataset_id = "my_source_dataset"
transfer_config = bigquery_datatransfer.TransferConfig(
    destination_dataset_id=destination_dataset_id,
    display_name="Your Dataset Copy Name",
    data_source_id="cross_region_copy",
    params={
        "source_project_id": source_project_id,
        "source_dataset_id": source_dataset_id,
    },
    schedule="every 24 hours",
)
transfer_config = transfer_client.create_transfer_config(
    parent=transfer_client.common_project_path(destination_project_id),
    transfer_config=transfer_config,
)
print(f"Created transfer config: {transfer_config.name}")
```

為避免產生額外的儲存空間費用，建議[刪除先前的資料集](#delete-datasets)。

### 查看資料集複製作業

如要在Google Cloud 控制台中查看資料集副本工作的狀態和詳細資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 選取要查看轉移詳細資料的轉移作業，然後執行下列操作：

   1. 在「Transfer details」(移轉作業詳細資料) 頁面中，選取移轉作業執行。
   2. 如要重新整理，請按一下 refresh「重新整理」。

## 在其他位置重新建立資料集

如要手動將資料集移至其他位置，請按照下列步驟操作：

1. 從 BigQuery 資料表[匯出資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)至 Cloud Storage 值區。

   從 BigQuery 中匯出資料並不需要付費，但是在 Cloud Storage [儲存匯出的資料](https://docs.cloud.google.com/storage/pricing?hl=zh-tw#storage-pricing)則會產生費用。BigQuery 匯出作業會受到[擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)的相關限制。
2. 從匯出 Cloud Storage bucket 中，將資料複製或移動至您在目的地位置建立的新 bucket。舉例來說，如果您要將資料從`US`多區域移到`asia-northeast1`東京區域，則必須把資料移轉到您在東京建立的值區。如要瞭解如何轉移 Cloud Storage 物件，請參閱 Cloud Storage 說明文件中的[複製、重新命名及移動物件](https://docs.cloud.google.com/storage/docs/copying-renaming-moving-objects?hl=zh-tw)一文。

   在不同地區之間轉移資料將導致 Cloud Storage 產生[網路輸出費用](https://docs.cloud.google.com/storage/pricing?hl=zh-tw#network-pricing)。
3. 在新位置建立新的 BigQuery 資料集，然後將資料從 Cloud Storage bucket 載入新資料集。

   將資料載入 BigQuery 無須支付費用，但將資料儲存於 Cloud Storage 則須支付費用，直到您刪除資料或值區為止。載入資料之後，將資料儲存至 BigQuery 亦須支付相關費用。將資料載入 BigQuery 時，必須遵守[載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)的相關限制。

您也可以使用 [Managed Service for Apache Airflow](https://cloud.google.com/blog/products/data-analytics/how-to-transfer-bigquery-tables-between-locations-with-cloud-composer?hl=zh-tw)，以程式輔助方式移動及複製大型資料集。

如要進一步瞭解如何使用 Cloud Storage 儲存及移動大型資料集，請參閱[搭配大數據使用 Cloud Storage](https://docs.cloud.google.com/storage/docs/working-with-big-data?hl=zh-tw)。

## 安全資料集

如要在 BigQuery 中控管資料集存取權，請參閱「[控管資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。如要瞭解資料加密，請參閱「[靜態資料加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)」。

## 刪除資料集

使用 Google Cloud 控制台刪除資料集時，系統會自動刪除資料集中的資料表和檢視表 (包括其中的資料)。不過，使用任何其他方法時，您必須先清空資料集，或指定相應的旗標、參數或關鍵字，強制移除資料集內容。

如果您嘗試刪除非空白資料集，但未提供適當的標記或參數，作業就會失敗並顯示以下錯誤訊息：`Dataset project:dataset is still in use`。

刪除資料集時，系統會為資料集刪除作業建立一筆[稽核記錄](https://docs.cloud.google.com/bigquery/docs/introduction-audit-workloads?hl=zh-tw)項目。不會為資料集內刪除的每個資料表建立個別的記錄檔項目。

如要刪除資料集，請選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下資料集。
4. 在詳細資料窗格中，按一下 delete「刪除」。
5. 在「Delete dataset」(刪除資料集) 對話方塊中，在欄位輸入 `delete`，然後按一下「Delete」(刪除)。

**注意：** 使用 Google Cloud 控制台刪除資料集時，系統會自動移除資料表。

### SQL

如要刪除資料集，請使用 [`DROP SCHEMA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_schema_statement)。

以下範例會刪除名為 `mydataset` 的資料集：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   DROP SCHEMA IF EXISTS mydataset;
   ```

   根據預設，這項功能只能刪除空白資料集。
   如要刪除資料集和所有內容，請使用 `CASCADE` 關鍵字：

   ```
   DROP SCHEMA IF EXISTS mydataset CASCADE;
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq rm` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_rm)，並加上 `--dataset` 或 `-d` 旗標 (選用)。如果資料集中包含資料表，您就必須使用 `-r` 標記來移除資料集中的所有資料表。如果您使用 `-r` 旗標，則可以省略 `--dataset` 或 `-d` 旗標。

執行指令後，系統會要求確認。您可以使用 `-f` 標記略過確認程序。

如要刪除非預設專案中的資料表，請使用下列格式將專案 ID 新增至資料集名稱：`PROJECT_ID:DATASET`。

```
bq rm -r -f -d PROJECT_ID:DATASET
```

更改下列內容：

* `PROJECT_ID`：專案 ID
* `DATASET`：要刪除的資料集名稱

**範例：**

輸入下列指令，從預設專案中移除名為 `mydataset` 的資料集及其所有資料表。這個指令會使用 `-d` 旗標。

```
bq rm -r -d mydataset
```

當系統提示時，請輸入 `y`，然後按下 Enter 鍵。

輸入下列指令，即可從 `myotherproject` 中移除 `mydataset` 及其中的所有資料表。這個指令不會使用選用的 `-d` 旗標。`-f` 標記可用來略過確認程序。

```
bq rm -r -f myotherproject:mydataset
```

您可以使用 `bq ls` 指令確認資料集是否已刪除。

### API

呼叫 [`datasets.delete`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/delete?hl=zh-tw) 方法來刪除資料集，然後將 `deleteContents` 參數設為 `true` 來刪除當中的資料表。

### C#

下列程式碼範例會刪除空白資料集。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 `pip install google-cloud-bigquery-datatransfer` 安裝 [BigQuery Data Transfer API 的 Python 用戶端](https://docs.cloud.google.com/python/docs/reference/bigquerydatatransfer/latest?hl=zh-tw)。然後建立移轉設定，複製資料集。

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryDeleteDataset
{
    public void DeleteDataset(
        string projectId = "your-project-id",
        string datasetId = "your_empty_dataset"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        // Delete a dataset that does not contain any tables
        client.DeleteDataset(datasetId: datasetId);
        Console.WriteLine($"Dataset {datasetId} deleted.");
    }
}
```

下列程式碼範例會刪除資料集及其所有內容：

```
// Copyright(c) 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may not
// use this file except in compliance with the License. You may obtain a copy of
// the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations under
// the License.
//

using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryDeleteDatasetAndContents
{
    public void DeleteDatasetAndContents(
        string projectId = "your-project-id",
        string datasetId = "your_dataset_with_tables"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        // Use the DeleteDatasetOptions to delete a dataset and its contents
        client.DeleteDataset(
            datasetId: datasetId,
            options: new DeleteDatasetOptions() { DeleteContents = true }
        );
        Console.WriteLine($"Dataset {datasetId} and contents deleted.");
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 `pip install google-cloud-bigquery-datatransfer` 安裝 [BigQuery Data Transfer API 的 Python 用戶端](https://docs.cloud.google.com/python/docs/reference/bigquerydatatransfer/latest?hl=zh-tw)。然後建立移轉設定，複製資料集。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// deleteDataset demonstrates the deletion of an empty dataset.
func deleteDataset(projectID, datasetID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	// To recursively delete a dataset and contents, use DeleteWithContents.
	if err := client.Dataset(datasetID).Delete(ctx); err != nil {
		return fmt.Errorf("Delete: %v", err)
	}
	return nil
}
```

### Java

下列程式碼範例會刪除空白資料集。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 `pip install google-cloud-bigquery-datatransfer` 安裝 [BigQuery Data Transfer API 的 Python 用戶端](https://docs.cloud.google.com/python/docs/reference/bigquerydatatransfer/latest?hl=zh-tw)。然後建立移轉設定，複製資料集。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQuery.DatasetDeleteOption;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.DatasetId;

public class DeleteDataset {

  public static void runDeleteDataset() {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    deleteDataset(projectId, datasetName);
  }

  public static void deleteDataset(String projectId, String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      DatasetId datasetId = DatasetId.of(projectId, datasetName);
      boolean success = bigquery.delete(datasetId, DatasetDeleteOption.deleteContents());
      if (success) {
        System.out.println("Dataset deleted successfully");
      } else {
        System.out.println("Dataset was not found");
      }
    } catch (BigQueryException e) {
      System.out.println("Dataset was not deleted. \n" + e.toString());
    }
  }
}
```

下列程式碼範例會刪除資料集及其所有內容：

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

package com.example.bigquery;

import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.DatasetId;

// Sample to delete dataset with contents.
public class DeleteDatasetAndContents {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    deleteDatasetAndContents(projectId, datasetName);
  }

  public static void deleteDatasetAndContents(String projectId, String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      DatasetId datasetId = DatasetId.of(projectId, datasetName);
      // Use the force parameter to delete a dataset and its contents
      boolean success = bigquery.delete(datasetId, BigQuery.DatasetDeleteOption.deleteContents());
      if (success) {
        System.out.println("Dataset deleted with contents successfully");
      } else {
        System.out.println("Dataset was not found");
      }
    } catch (BigQueryException e) {
      System.out.println("Dataset was not deleted with contents. \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 `pip install google-cloud-bigquery-datatransfer` 安裝 [BigQuery Data Transfer API 的 Python 用戶端](https://docs.cloud.google.com/python/docs/reference/bigquerydatatransfer/latest?hl=zh-tw)。然後建立移轉設定，複製資料集。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function deleteDataset() {
  // Deletes a dataset named "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';

  // Create a reference to the existing dataset
  const dataset = bigquery.dataset(datasetId);

  // Delete the dataset and its contents
  await dataset.delete({force: true});
  console.log(`Dataset ${dataset.id} deleted.`);
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 `pip install google-cloud-bigquery-datatransfer` 安裝 [BigQuery Data Transfer API 的 Python 用戶端](https://docs.cloud.google.com/python/docs/reference/bigquerydatatransfer/latest?hl=zh-tw)。然後建立移轉設定，複製資料集。

```
use Google\Cloud\BigQuery\BigQueryClient;

/** Uncomment and populate these variables in your code */
// $projectId = 'The Google project ID';
// $datasetId = 'The BigQuery dataset ID';

$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$dataset = $bigQuery->dataset($datasetId);
$table = $dataset->delete();
printf('Deleted dataset %s' . PHP_EOL, $datasetId);
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 `pip install google-cloud-bigquery-datatransfer` 安裝 [BigQuery Data Transfer API 的 Python 用戶端](https://docs.cloud.google.com/python/docs/reference/bigquerydatatransfer/latest?hl=zh-tw)。然後建立移轉設定，複製資料集。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set model_id to the ID of the model to fetch.
# dataset_id = 'your-project.your_dataset'

# Use the delete_contents parameter to delete a dataset and its contents.
# Use the not_found_ok parameter to not receive an error if the dataset has already been deleted.
client.delete_dataset(
    dataset_id, delete_contents=True, not_found_ok=True
)  # Make an API request.

print("Deleted dataset '{}'.".format(dataset_id))
```

### Ruby

下列程式碼範例會刪除空白資料集。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 `pip install google-cloud-bigquery-datatransfer` 安裝 [BigQuery Data Transfer API 的 Python 用戶端](https://docs.cloud.google.com/python/docs/reference/bigquerydatatransfer/latest?hl=zh-tw)。然後建立移轉設定，複製資料集。

```
require "google/cloud/bigquery"

def delete_dataset dataset_id = "my_empty_dataset"
  bigquery = Google::Cloud::Bigquery.new

  # Delete a dataset that does not contain any tables
  dataset = bigquery.dataset dataset_id
  dataset.delete
  puts "Dataset #{dataset_id} deleted."
end
```

下列程式碼範例會刪除資料集及其所有內容：

```
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
require "google/cloud/bigquery"

def delete_dataset_and_contents dataset_id = "my_dataset_with_tables"
  bigquery = Google::Cloud::Bigquery.new

  # Use the force parameter to delete a dataset and its contents
  dataset = bigquery.dataset dataset_id
  dataset.delete force: true
  puts "Dataset #{dataset_id} and contents deleted."
end
```

## 從已刪除的資料集還原資料表

您可以還原已刪除資料集中的資料表，但必須在資料集的[時間回溯期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)內。如要還原整個資料集，請參閱「[還原已刪除的資料集](https://docs.cloud.google.com/bigquery/docs/restore-deleted-datasets?hl=zh-tw)」。

1. 建立與原始資料集名稱相同且位於相同位置的資料集。
2. 使用自 Epoch 紀元以來的毫秒數格式 (例如 `1418864998000`)，選擇原始資料集刪除前的時間戳記。
3. 將時間為 `1418864998000` 的 `originaldataset.table1` 資料表複製到新資料集：

   ```
   bq cp originaldataset.table1@1418864998000 mydataset.mytable
   ```

   如要找出已刪除資料集中的非空白資料表名稱，請在時間回溯期內查詢資料集的 [`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)。

## 還原已刪除的資料集

如要瞭解如何還原 (或*取消刪除*) 已刪除的資料集，請參閱「[還原已刪除的資料集](https://docs.cloud.google.com/bigquery/docs/restore-deleted-datasets?hl=zh-tw)」。

## 配額

如要瞭解複製配額，請參閱「[複製作業](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)」。
您可以在 `INFORMATION_SCHEMA` 中查看複製工作的用量。如要瞭解如何查詢 `INFORMATION_SCHEMA.JOBS` 檢視區塊，請參閱[`JOBS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)。

## 定價

如需複製資料集的定價資訊，請參閱「[資料複製定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_replication)」。

BigQuery 會傳送壓縮資料以跨地區進行複製，因此計費的資料量可能小於資料集的實際大小。詳情請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」一文。

## 後續步驟

* 瞭解如何[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。
* 瞭解如何[更新資料集](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]