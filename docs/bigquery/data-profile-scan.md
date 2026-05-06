Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 剖析資料

本文說明如何使用資料剖析掃描作業，進一步瞭解資料。BigQuery 會使用 Knowledge Catalog 分析資料的統計特徵，例如平均值、不重複值和最大值。Knowledge Catalog 也會使用這項資訊[建議資料品質檢查規則](https://docs.cloud.google.com/dataplex/docs/auto-data-quality-overview?hl=zh-tw)。

如要進一步瞭解資料剖析，請參閱「[關於資料剖析](https://docs.cloud.google.com/dataplex/docs/data-profiling-overview?hl=zh-tw)」。

**提示：** 本文中的步驟說明如何管理專案中的資料剖析掃描。您也可以在處理特定資料表時，建立及管理資料剖析掃描作業。詳情請參閱本文件的「[管理特定資料表的資料剖析掃描](#start-from-table)」一節。

## 事前準備

啟用 Dataplex API。

**啟用 API 時所需的角色**

如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

[啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=dataplex.googleapis.com&hl=zh-tw)

## 必要的角色

本節說明使用 Knowledge Catalog 資料剖析掃描作業所需的 IAM 角色和權限。

### 使用者角色和權限

如要取得建立及管理資料剖析掃描作業所需的權限，請要求系統管理員授予您下列 IAM 角色：

* 建立、執行、更新及刪除資料剖析檔掃描作業：
  在包含資料掃描作業的專案中，[Dataplex DataScan 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.dataScanEditor)  (`roles/dataplex.dataScanEditor`)
* 查看資料剖析掃描結果、工作和記錄：
  在包含資料掃描作業的專案中，[Dataplex DataScan 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.dataScanViewer)  (`roles/dataplex.dataScanViewer`)
* 將資料剖析掃描結果發布至 Knowledge Catalog：
  [Dataplex Catalog 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.catalogEditor)  (`roles/dataplex.catalogEditor`)
  在 `@bigquery` 項目群組上
* 在「資料剖析檔」分頁中，查看 BigQuery 中發布的資料剖析掃描結果：
  資料表的「BigQuery 資料檢視者」圖示 (`roles/bigquery.dataViewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備建立及管理資料剖析掃描作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立及管理資料剖析掃描作業，必須具備下列權限：

* 建立、執行、更新及刪除資料剖析掃描作業：
  + 專案的  `dataplex.datascans.create`
  + `dataplex.datascans.update`
    資料掃描
  + `dataplex.datascans.delete`
    資料掃描
  + `dataplex.datascans.run`
    資料掃描
  + `dataplex.datascans.get`
    資料掃描
  + 專案的  `dataplex.datascans.list`
  + `dataplex.dataScanJobs.get`
    資料掃描工作
  + `dataplex.dataScanJobs.list`
    資料掃描
* 查看資料剖析掃描結果、工作和記錄：
  + `dataplex.datascans.getData`
    資料掃描
  + 專案的  `dataplex.datascans.list`
  + `dataplex.dataScanJobs.get`
    資料掃描工作
  + `dataplex.dataScanJobs.list`
    資料掃描
* 將資料剖析掃描結果發布至 Knowledge Catalog：
  + `dataplex.entryGroups.useDataProfileAspect`
    項目群組
  + `bigquery.tables.update`
    在桌上
  + `dataplex.entries.update`
    on entry
* 在 BigQuery 或 Knowledge Catalog 中查看資料表的已發布資料剖析檔結果：
  + `bigquery.tables.get`
    在桌上
  + `bigquery.tables.getData`
    在桌上

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### Knowledge Catalog 服務帳戶角色和權限

為確保 Knowledge Catalog 服務帳戶具備執行資料剖析掃描和匯出結果的必要權限，請要求管理員將下列 IAM 角色授予 Knowledge Catalog 服務帳戶：

**重要事項：**您必須將這些角色授予 Knowledge Catalog 服務帳戶，*而非*使用者帳戶。如果未將角色授予正確的主體，可能會導致權限錯誤。

* 對 BigQuery 資料執行資料剖析掃描：
  + [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
    在執行掃描的專案中
  + [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
    掃描中的資料表
* 針對使用 Cloud Storage 資料的 BigQuery 外部資料表執行資料剖析掃描：
  + [Storage 物件檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectViewer)  (`roles/storage.objectViewer`)
    在 Cloud Storage 值區上
  + [Storage 舊版值區讀取者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.legacyBucketReader)  (`roles/storage.legacyBucketReader`)
    在 Cloud Storage bucket 上
* 在 Lakehouse 上執行 Iceberg REST 目錄資料表的資料剖析掃描作業：
  [BigLake 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-tw#biglake.viewer)  (`roles/biglake.viewer`)
  在掃描的 Iceberg REST 目錄資料表上
  Google Cloud
* 將資料剖析掃描結果匯出至 BigQuery 資料表：
  資料表的「BigQuery 資料編輯者」 (`roles/bigquery.dataEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行資料剖析掃描作業及匯出結果所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行資料剖析掃描作業及匯出結果，您必須具備下列權限：

* 對 BigQuery 資料執行資料剖析掃描：
  + 專案的  `bigquery.jobs.create`
  + `bigquery.tables.get`
    在桌上
  + `bigquery.tables.getData`
    在桌上
* 針對使用 Cloud Storage 資料的 BigQuery 外部資料表執行資料剖析掃描：
  + `storage.buckets.get`
    on bucket
  + `storage.objects.get`
    物件
* 將資料剖析掃描結果匯出至 BigQuery 資料表：
  + `bigquery.tables.create`
    資料集
  + `bigquery.tables.updateData`
    在桌上

管理員或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，授予 Knowledge Catalog 服務帳戶這些權限。

如果資料表使用 BigQuery [資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)，Knowledge Catalog 只能掃描 Knowledge Catalog 服務帳戶可見的資料列。如要允許 Knowledge Catalog 掃描所有資料列，請將其服務帳戶新增至述詞為 `TRUE` 的資料列篩選器。

如果資料表使用 BigQuery [資料欄層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)，Knowledge Catalog 就必須有權掃描受保護的資料欄。如要授予存取權，請將資料表使用的所有政策標記的「Data Catalog 精細讀取者」 (`roles/datacatalog.fineGrainedReader`) 角色，授予 Knowledge Catalog 服務帳戶。建立或更新資料掃描的使用者也需要受保護資料欄的權限。

### 將角色授予 Knowledge Catalog 服務帳戶

如要執行資料剖析掃描，Knowledge Catalog 會使用服務帳戶，該帳戶必須具備執行 BigQuery 工作和讀取 BigQuery 資料表資料的權限。如要授予必要角色，請按照下列步驟操作：

1. 取得 Knowledge Catalog 服務帳戶的電子郵件地址。如果您尚未在這個專案中建立資料剖析檔或資料品質掃描作業，請執行下列 `gcloud` 指令來產生服務身分：

   ```
   gcloud beta services identity create --service=dataplex.googleapis.com
   ```

   指令會傳回服務帳戶電子郵件，格式如下：
   service-PROJECT\_ID@gcp-sa-dataplex.iam.gserviceaccount.com。

   如果服務帳戶已存在，請在 Google Cloud 主控台的「IAM」(身分與存取權管理) 頁面，查看具有「Dataplex」名稱的主體，即可找到服務帳戶的電子郵件地址。
2. 在專案中授予服務帳戶 **BigQuery 工作使用者** (`roles/bigquery.jobUser`) 角色。服務帳戶可透過這個角色執行掃描的 BigQuery 工作。

   ```
   gcloud projects add-iam-policy-binding PROJECT_ID \
       --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-dataplex.iam.gserviceaccount.com" \
       --role="roles/bigquery.jobUser"
   ```

   更改下列內容：

   * `PROJECT_ID`：您的 Google Cloud 專案 ID。
   * `service-PROJECT_NUMBER@gcp-sa-dataplex.iam.gserviceaccount.com`：Knowledge Catalog 服務帳戶的電子郵件地址。
3. 針對要剖析的每個資料表，授予服務帳戶「BigQuery 資料檢視者」(`roles/bigquery.dataViewer`) 角色。這個角色可授予資料表的唯讀存取權。

   ```
   gcloud bigquery tables add-iam-policy-binding DATASET_ID.TABLE_ID \
       --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-dataplex.iam.gserviceaccount.com" \
       --role="roles/bigquery.dataViewer"
   ```

   更改下列內容：

   * `DATASET_ID`：包含表格的資料集 ID。
   * `TABLE_ID`：要分析的資料表 ID。
   * `service-PROJECT_NUMBER@gcp-sa-dataplex.iam.gserviceaccount.com`：Knowledge Catalog 服務帳戶的電子郵件地址。

## 建立資料剖析掃描

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下「建立資料剖析掃描」。
3. (選用) 輸入「Display name」(顯示名稱)。
4. 輸入 ID。請參閱「[資源命名慣例](https://docs.cloud.google.com/compute/docs/naming-resources?hl=zh-tw#resource-name-format)」。
5. 選用：輸入**說明**。
6. 在「Table」(資料表) 欄位中，按一下「Browse」(瀏覽)。選擇要掃描的資料表，然後按一下「選取」。系統僅支援標準 BigQuery 和 Iceberg REST 目錄資料表。

   如為多區域資料集內的資料表，請選擇要建立資料掃描的區域。

   如要瀏覽 Knowledge Catalog 湖泊中的資料表，請按一下「Browse within Knowledge Catalog Lakes」(在 Knowledge Catalog 湖泊中瀏覽)。
7. 在「模式」部分，選取下列任一選項：

   * **標準**：使用可自訂的掃描設定剖析資料。此為預設模式。
   * **輕量級**：提供低延遲、低保真度的掃描，可快速取得洞察資料。
8. 如果選擇「標準」模式，請設定下列選項。選取「輕量」模式時，不會顯示這些選項。

   1. 在「範圍」欄位中，選擇「增量」或「完整資料」。

      如果選擇「增量資料」，請在「時間戳記欄」欄位中，從 BigQuery 資料表選取 `DATE` 或 `TIMESTAMP` 類型的資料欄。Knowledge Catalog 會使用這個資料欄，在新增記錄時識別新記錄。如果資料表是依據 `DATE` 或 `TIMESTAMP` 類型的資料欄分區，建議使用這個資料欄做為分區資料欄。
   2. 選用：如要篩選資料，請執行下列任一操作：

      * 如要依資料列篩選，請選取「篩選資料列」核取方塊。
        輸入有效的 SQL 運算式，該運算式可搭配 GoogleSQL 語法中的 [`WHERE` 子句使用](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#where_clause)。例如：`col1 >= 0`。

        篩選器可以是多個資料欄的 SQL 條件組合。例如：`col1 >= 0 AND col2 < 10`。
      * 如要依資料欄篩選，請選取「篩選資料欄」核取方塊。
      * 如要在剖析掃描中加入資料欄，請在「Include columns」(包含資料欄) 欄位中按一下「Browse」(瀏覽)。選取要納入的資料欄，然後按一下「選取」。
      * 如要從剖析掃描中排除資料欄，請在「排除資料欄」欄位中按一下「瀏覽」。選取要排除的資料欄，然後按一下「選取」。**注意：** 你可以使用「包含資料欄」、「排除資料欄」，或同時使用兩者。如果同時使用這兩個欄位，資料剖析掃描會先根據「Include columns」(納入資料欄) 欄位中的輸入內容選取資料欄，然後根據「Exclude columns」(排除資料欄) 欄位中的輸入內容排除資料欄。
   3. 如要對資料剖析掃描作業套用取樣，請在「取樣大小」清單中選取取樣百分比。請選擇介於 0.0% 至 100.0% 之間的百分比值，最多可有 3 位小數。

      * 如果是較大的資料集，請選擇較低的取樣百分比。舉例來說，如果資料表大小為 1 PB，且您輸入的值介於 0.1% 到 1.0% 之間，資料剖析檔會取樣 1 到 10 TB 的資料。
      * 樣本資料中必須至少有 100 筆記錄，才能傳回結果。
      * 如果是增量資料掃描，資料剖析掃描會對最新增量套用取樣。
9. 選用步驟：在來源資料表的Google Cloud 控制台中，將資料剖析掃描結果發布至 BigQuery 和 Knowledge Catalog 頁面。選取「將結果發布至 Knowledge Catalog」核取方塊。

   您可以在來源資料表的 BigQuery 和 Knowledge Catalog 頁面中，透過「資料剖析檔」分頁標籤查看最新的掃描結果。如要讓使用者存取已發布的掃描結果，請參閱本文的「[授予資料剖析掃描結果的存取權](#share-results)」一節。

   在下列情況下，可能無法使用發布選項：

   * 您沒有資料表的必要權限。
   * 已將另一項資料剖析掃描設為發布結果。
10. 在「時間表」部分，選擇下列其中一個選項：

    * **重複**：排定資料剖析掃描的執行時間，例如每小時、每天、每週、每月或自訂。指定掃描的執行頻率和時間。如果選擇自訂，請使用 [cron](https://en.wikipedia.org/wiki/Cron) 格式指定排程。
    * **依需求**：依需求執行資料剖析掃描。
    * **執行一次**：立即執行一次資料剖析掃描作業，並在自動刪除時間過後移除掃描作業。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

      + **設定掃描後結果自動刪除**：自動刪除時間會定義資料剖析掃描在執行後保持有效的時間長度。如果掃描資料設定檔時未指定自動刪除時間，系統會在 24 小時後自動移除掃描結果。自動刪除時間範圍從 0 秒 (立即刪除) 到 365 天。
11. 按一下「繼續」。
12. 選用步驟：將掃描結果匯出至 BigQuery 標準資料表。在「將掃描結果匯出至 BigQuery 資料表」部分，執行下列操作：

    1. 在「選取 BigQuery 資料集」欄位中，按一下「瀏覽」。選取要用來儲存資料剖析掃描結果的 BigQuery 資料集。
    2. 在「BigQuery table」(BigQuery 資料表) 欄位中，指定要儲存資料設定檔掃描結果的資料表。如果使用現有資料表，請確認該資料表與[匯出資料表結構定義](https://docs.cloud.google.com/dataplex/docs/use-data-profiling?hl=zh-tw#table-schema)相容。如果指定的資料表不存在，Knowledge Catalog 會為您建立。

       **注意：** 您可以為多個資料剖析掃描作業使用同一個結果資料表。
13. 選用：新增標籤。標籤是鍵/值組合，可用來將相關物件分組，或與其他 Google Cloud 資源組合。
14. 如要建立掃描作業，請按一下「建立」。

    如果將排程設為隨選，您也可以按一下「執行掃描」立即執行掃描。

### gcloud

如要建立資料剖析掃描，請使用 [`gcloud dataplex datascans create data-profile` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/create/data-profile?hl=zh-tw)。

如果來源資料是儲存在 Knowledge Catalog lake 中，請加入 `--data-source-entity` 旗標：

```
gcloud dataplex datascans create data-profile DATASCAN \
--location=LOCATION \
--data-source-entity=DATA_SOURCE_ENTITY
```

如果來源資料並非在 Knowledge Catalog 湖泊中整理，請加入 `--data-source-resource` 旗標：

```
gcloud dataplex datascans create data-profile DATASCAN \
--location=LOCATION \
--data-source-resource=DATA_SOURCE_RESOURCE
```

請替換下列變數：

* `DATASCAN`：資料剖析掃描的名稱。
* `LOCATION`：建立資料剖析掃描的 Google Cloud 區域。
* `DATA_SOURCE_ENTITY`：包含資料剖析掃描資料的 Knowledge Catalog 實體。例如：`projects/test-project/locations/test-location/lakes/test-lake/zones/test-zone/entities/test-entity`。
* `DATA_SOURCE_RESOURCE`：資源名稱，其中包含資料剖析掃描的資料。例如：`//bigquery.googleapis.com/projects/test-project/datasets/test-dataset/tables/test-table`。

### C#

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.Dataplex.V1/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
using Google.Api.Gax.ResourceNames;
using Google.Cloud.Dataplex.V1;
using Google.LongRunning;

public sealed partial class GeneratedDataScanServiceClientSnippets
{
    /// <summary>Snippet for CreateDataScan</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void CreateDataScanRequestObject()
    {
        // Create client
        DataScanServiceClient dataScanServiceClient = DataScanServiceClient.Create();
        // Initialize request argument(s)
        CreateDataScanRequest request = new CreateDataScanRequest
        {
            ParentAsLocationName = LocationName.FromProjectLocation("[PROJECT]", "[LOCATION]"),
            DataScan = new DataScan(),
            DataScanId = "",
            ValidateOnly = false,
        };
        // Make the request
        Operation<DataScan, OperationMetadata> response = dataScanServiceClient.CreateDataScan(request);

        // Poll until the returned long-running operation is complete
        Operation<DataScan, OperationMetadata> completedResponse = response.PollUntilCompleted();
        // Retrieve the operation result
        DataScan result = completedResponse.Result;

        // Or get the name of the operation
        string operationName = response.Name;
        // This name can be stored, then the long-running operation retrieved later by name
        Operation<DataScan, OperationMetadata> retrievedResponse = dataScanServiceClient.PollOnceCreateDataScan(operationName);
        // Check if the retrieved long-running operation has completed
        if (retrievedResponse.IsCompleted)
        {
            // If it has completed, then access the result
            DataScan retrievedResult = retrievedResponse.Result;
        }
    }
}
```

### Go

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://pkg.go.dev/cloud.google.com/go/dataplex)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
package main

import (
	"context"

	dataplex "cloud.google.com/go/dataplex/apiv1"
	dataplexpb "cloud.google.com/go/dataplex/apiv1/dataplexpb"
)

func main() {
	ctx := context.Background()
	// This snippet has been automatically generated and should be regarded as a code template only.
	// It will require modifications to work:
	// - It may require correct/in-range values for request initialization.
	// - It may require specifying regional endpoints when creating the service client as shown in:
	//   https://pkg.go.dev/cloud.google.com/go#hdr-Client_Options
	c, err := dataplex.NewDataScanClient(ctx)
	if err != nil {
		// TODO: Handle error.
	}
	defer c.Close()

	req := &dataplexpb.CreateDataScanRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/dataplex/apiv1/dataplexpb#CreateDataScanRequest.
	}
	op, err := c.CreateDataScan(ctx, req)
	if err != nil {
		// TODO: Handle error.
	}

	resp, err := op.Wait(ctx)
	if err != nil {
		// TODO: Handle error.
	}
	// TODO: Use resp.
	_ = resp
}
```

### Java

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-dataplex/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import com.google.cloud.dataplex.v1.CreateDataScanRequest;
import com.google.cloud.dataplex.v1.DataScan;
import com.google.cloud.dataplex.v1.DataScanServiceClient;
import com.google.cloud.dataplex.v1.LocationName;

public class SyncCreateDataScan {

  public static void main(String[] args) throws Exception {
    syncCreateDataScan();
  }

  public static void syncCreateDataScan() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DataScanServiceClient dataScanServiceClient = DataScanServiceClient.create()) {
      CreateDataScanRequest request =
          CreateDataScanRequest.newBuilder()
              .setParent(LocationName.of("[PROJECT]", "[LOCATION]").toString())
              .setDataScan(DataScan.newBuilder().build())
              .setDataScanId("dataScanId1260787906")
              .setValidateOnly(true)
              .build();
      DataScan response = dataScanServiceClient.createDataScanAsync(request).get();
    }
  }
}
```

### Python

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/dataplex/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import dataplex_v1


def sample_create_data_scan():
    # Create a client
    client = dataplex_v1.DataScanServiceClient()

    # Initialize request argument(s)
    data_scan = dataplex_v1.DataScan()
    data_scan.data.entity = "entity_value"

    request = dataplex_v1.CreateDataScanRequest(
        parent="parent_value",
        data_scan=data_scan,
        data_scan_id="data_scan_id_value",
    )

    # Make the request
    operation = client.create_data_scan(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)
```

### Ruby

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-dataplex/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
require "google/cloud/dataplex/v1"

##
# Snippet for the create_data_scan call in the DataScanService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::Dataplex::V1::DataScanService::Client#create_data_scan.
#
def create_data_scan
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::Dataplex::V1::DataScanService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::Dataplex::V1::CreateDataScanRequest.new

  # Call the create_data_scan method.
  result = client.create_data_scan request

  # The returned object is of type Gapic::Operation. You can use it to
  # check the status of an operation, cancel it, or wait for results.
  # Here is how to wait for a response.
  result.wait_until_done! timeout: 60
  if result.response?
    p result.response
  else
    puts "No response received."
  end
end
```

### REST

如要建立資料剖析掃描作業，請使用 [`dataScans.create` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/create?hl=zh-tw)。

**注意：** 如果 BigQuery 資料表的 `Require
partition filter` 設定設為 `true`，請使用資料表的分區資料欄做為資料剖析掃描的資料列篩選器或時間戳記欄。

## 建立多項資料剖析掃描作業

您可以使用 Google Cloud 控制台，同時為 BigQuery 資料集中的多個資料表設定資料剖析掃描作業。

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下「建立資料剖析掃描」。
3. 選取「多項資料剖析掃描作業」選項。
4. 輸入 **ID 前置字串**。Knowledge Catalog 會使用您提供的前置字元和專屬後置字元，自動產生掃描 ID。
5. 為所有資料剖析掃描作業輸入**說明**。
6. 在「Dataset」(資料集) 欄位中，按一下「Browse」(瀏覽)。選取要從中挑選資料表的資料集。按一下「選取」。
7. 如果資料集屬於多區域，請選取要建立資料剖析掃描作業的**區域**。
8. 在「模式」部分，選擇下列任一選項：

   * **標準**：使用可自訂的掃描設定剖析資料。此為預設模式。
   * **輕巧**：提供低延遲、低保真度的掃描，可快速取得洞察資訊。這項功能為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。
9. 如果選擇「標準」模式，請為掃描設定下列項目。選取「輕量」模式時，系統不會顯示這些設定。

   1. 在「範圍」欄位中，選擇「增量」或「完整資料」。

      如果選擇「增量」資料，則只能選取依 `DATE` 或 `TIMESTAMP` 類型資料欄分區的資料表。
   2. 如要對資料剖析掃描套用取樣，請在「取樣大小」清單中選取取樣百分比。

      請選擇介於 0.0% 和 100.0% 之間的百分比值，最多可有 3 位小數。
10. 選用步驟：在來源資料表的Google Cloud 控制台中，將資料剖析掃描結果發布至 BigQuery 和 Knowledge Catalog 頁面。選取「將結果發布至 Knowledge Catalog」核取方塊。

    您可以在來源資料表的 BigQuery 和 Knowledge Catalog 頁面中，透過「資料剖析檔」分頁標籤查看最新的掃描結果。如要讓使用者存取已發布的掃描結果，請參閱本文的「[授予資料剖析掃描結果的存取權](#share-results)」一節。

    **注意：** 您必須選擇尚未發布掃描結果的資料表。
11. 在「時間表」部分，選擇下列其中一個選項：

    * **重複**：排定資料剖析掃描的執行時間，例如每小時、每天、每週、每月或自訂。指定掃描的執行頻率和時間。如果選擇自訂，請使用 [cron](https://en.wikipedia.org/wiki/Cron) 格式指定排程。
    * **隨選**：視需要執行資料剖析掃描。

      + **單次執行**：立即執行一次資料剖析掃描作業，並在自動刪除時間過後移除掃描作業。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

        - **設定掃描後結果自動刪除**：自動刪除時間會定義資料剖析掃描在執行後保持有效的時間長度。如果掃描資料剖析時未指定自動刪除時間，系統會在 24 小時後自動移除掃描結果。自動刪除時間範圍從 0 秒 (立即刪除) 到 365 天。
12. 按一下「繼續」。
13. 在「選擇資料表」欄位中，按一下「瀏覽」。選擇要掃描的一或多個表格，然後按一下「選取」。
14. 按一下「繼續」。
15. 選用步驟：將掃描結果匯出至 BigQuery 標準資料表。在「將掃描結果匯出至 BigQuery 資料表」部分，執行下列操作：

    1. 在「選取 BigQuery 資料集」欄位中，按一下「瀏覽」。選取要用來儲存資料剖析掃描結果的 BigQuery 資料集。
    2. 在「BigQuery table」(BigQuery 資料表) 欄位中，指定要儲存資料設定檔掃描結果的資料表。如果使用現有資料表，請確認該資料表與[匯出資料表結構定義](https://docs.cloud.google.com/dataplex/docs/use-data-profiling?hl=zh-tw#table-schema)相容。如果指定的資料表不存在，Knowledge Catalog 會為您建立。

       Knowledge Catalog 會對所有資料剖析掃描作業使用相同的結果資料表。
16. 選用：新增標籤。標籤是鍵/值組合，可用來將相關物件分組，或與其他 Google Cloud 資源組合。
17. 如要建立掃描作業，請按一下「建立」。

    如果將排程設為「按需求」，您也可以點選「執行掃描」立即執行掃描。

## 執行資料剖析掃描

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下要執行的資料剖析掃描。
3. 點選「立即執行」。

### gcloud

如要執行資料剖析掃描，請使用 [`gcloud dataplex datascans run` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/run?hl=zh-tw)：

```
gcloud dataplex datascans run DATASCAN \
--location=LOCATION
```

請替換下列變數：

* `DATASCAN`：資料剖析掃描的名稱。
* `LOCATION`：建立資料剖析掃描作業的 Google Cloud 區域。

### C#

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.Dataplex.V1/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
using Google.Cloud.Dataplex.V1;

public sealed partial class GeneratedDataScanServiceClientSnippets
{
    /// <summary>Snippet for RunDataScan</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void RunDataScanRequestObject()
    {
        // Create client
        DataScanServiceClient dataScanServiceClient = DataScanServiceClient.Create();
        // Initialize request argument(s)
        RunDataScanRequest request = new RunDataScanRequest
        {
            DataScanName = DataScanName.FromProjectLocationDataScan("[PROJECT]", "[LOCATION]", "[DATASCAN]"),
        };
        // Make the request
        RunDataScanResponse response = dataScanServiceClient.RunDataScan(request);
    }
}
```

### Go

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://pkg.go.dev/cloud.google.com/go/dataplex)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
package main

import (
	"context"

	dataplex "cloud.google.com/go/dataplex/apiv1"
	dataplexpb "cloud.google.com/go/dataplex/apiv1/dataplexpb"
)

func main() {
	ctx := context.Background()
	// This snippet has been automatically generated and should be regarded as a code template only.
	// It will require modifications to work:
	// - It may require correct/in-range values for request initialization.
	// - It may require specifying regional endpoints when creating the service client as shown in:
	//   https://pkg.go.dev/cloud.google.com/go#hdr-Client_Options
	c, err := dataplex.NewDataScanClient(ctx)
	if err != nil {
		// TODO: Handle error.
	}
	defer c.Close()

	req := &dataplexpb.RunDataScanRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/dataplex/apiv1/dataplexpb#RunDataScanRequest.
	}
	resp, err := c.RunDataScan(ctx, req)
	if err != nil {
		// TODO: Handle error.
	}
	// TODO: Use resp.
	_ = resp
}
```

### Java

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-dataplex/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import com.google.cloud.dataplex.v1.DataScanName;
import com.google.cloud.dataplex.v1.DataScanServiceClient;
import com.google.cloud.dataplex.v1.RunDataScanRequest;
import com.google.cloud.dataplex.v1.RunDataScanResponse;

public class SyncRunDataScan {

  public static void main(String[] args) throws Exception {
    syncRunDataScan();
  }

  public static void syncRunDataScan() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DataScanServiceClient dataScanServiceClient = DataScanServiceClient.create()) {
      RunDataScanRequest request =
          RunDataScanRequest.newBuilder()
              .setName(DataScanName.of("[PROJECT]", "[LOCATION]", "[DATASCAN]").toString())
              .build();
      RunDataScanResponse response = dataScanServiceClient.runDataScan(request);
    }
  }
}
```

### Python

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/dataplex/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import dataplex_v1


def sample_run_data_scan():
    # Create a client
    client = dataplex_v1.DataScanServiceClient()

    # Initialize request argument(s)
    request = dataplex_v1.RunDataScanRequest(
        name="name_value",
    )

    # Make the request
    response = client.run_data_scan(request=request)

    # Handle the response
    print(response)
```

### Ruby

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-dataplex/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
require "google/cloud/dataplex/v1"

##
# Snippet for the run_data_scan call in the DataScanService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::Dataplex::V1::DataScanService::Client#run_data_scan.
#
def run_data_scan
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::Dataplex::V1::DataScanService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::Dataplex::V1::RunDataScanRequest.new

  # Call the run_data_scan method.
  result = client.run_data_scan request

  # The returned object is of type Google::Cloud::Dataplex::V1::RunDataScanResponse.
  p result
end
```

### REST

如要執行資料剖析掃描，請使用 [`dataScans.run` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/run?hl=zh-tw)。

**注意：** 單次排程的資料剖析掃描作業不支援執行。

## 查看資料剖析掃描結果

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下資料剖析掃描的名稱。

   * 「總覽」部分會顯示最近一次工作的相關資訊，包括掃描執行時間、掃描的資料表記錄數和工作狀態。
   * 「資料剖析掃描設定」部分會顯示掃描的詳細資料。
3. 如要查看工作的詳細資訊，例如掃描的資料表欄、掃描中找到的欄統計資料和工作記錄，請按一下「工作記錄」分頁標籤。然後按一下工作 ID。

**注意：** 如果已將掃描結果匯出至 BigQuery 資料表，也可以從該資料表存取掃描結果。

### gcloud

如要查看資料剖析掃描工作的結果，請使用 [`gcloud dataplex datascans jobs describe` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/jobs/describe?hl=zh-tw)：

```
gcloud dataplex datascans jobs describe JOB \
--location=LOCATION \
--datascan=DATASCAN \
--view=FULL
```

請替換下列變數：

* `JOB`：資料剖析掃描工作的 ID。
* `LOCATION`：建立資料剖析掃描作業的 Google Cloud 區域。
* `DATASCAN`：作業所屬資料剖析掃描的名稱。
* `--view=FULL`：如要查看掃描工作結果，請指定 `FULL`。

### C#

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.Dataplex.V1/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
using Google.Cloud.Dataplex.V1;

public sealed partial class GeneratedDataScanServiceClientSnippets
{
    /// <summary>Snippet for GetDataScan</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void GetDataScanRequestObject()
    {
        // Create client
        DataScanServiceClient dataScanServiceClient = DataScanServiceClient.Create();
        // Initialize request argument(s)
        GetDataScanRequest request = new GetDataScanRequest
        {
            DataScanName = DataScanName.FromProjectLocationDataScan("[PROJECT]", "[LOCATION]", "[DATASCAN]"),
            View = GetDataScanRequest.Types.DataScanView.Unspecified,
        };
        // Make the request
        DataScan response = dataScanServiceClient.GetDataScan(request);
    }
}
```

### Go

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://pkg.go.dev/cloud.google.com/go/dataplex)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
package main

import (
	"context"

	dataplex "cloud.google.com/go/dataplex/apiv1"
	dataplexpb "cloud.google.com/go/dataplex/apiv1/dataplexpb"
)

func main() {
	ctx := context.Background()
	// This snippet has been automatically generated and should be regarded as a code template only.
	// It will require modifications to work:
	// - It may require correct/in-range values for request initialization.
	// - It may require specifying regional endpoints when creating the service client as shown in:
	//   https://pkg.go.dev/cloud.google.com/go#hdr-Client_Options
	c, err := dataplex.NewDataScanClient(ctx)
	if err != nil {
		// TODO: Handle error.
	}
	defer c.Close()

	req := &dataplexpb.GetDataScanRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/dataplex/apiv1/dataplexpb#GetDataScanRequest.
	}
	resp, err := c.GetDataScan(ctx, req)
	if err != nil {
		// TODO: Handle error.
	}
	// TODO: Use resp.
	_ = resp
}
```

### Java

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-dataplex/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import com.google.cloud.dataplex.v1.DataScan;
import com.google.cloud.dataplex.v1.DataScanName;
import com.google.cloud.dataplex.v1.DataScanServiceClient;
import com.google.cloud.dataplex.v1.GetDataScanRequest;

public class SyncGetDataScan {

  public static void main(String[] args) throws Exception {
    syncGetDataScan();
  }

  public static void syncGetDataScan() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DataScanServiceClient dataScanServiceClient = DataScanServiceClient.create()) {
      GetDataScanRequest request =
          GetDataScanRequest.newBuilder()
              .setName(DataScanName.of("[PROJECT]", "[LOCATION]", "[DATASCAN]").toString())
              .build();
      DataScan response = dataScanServiceClient.getDataScan(request);
    }
  }
}
```

### Python

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/dataplex/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import dataplex_v1


def sample_get_data_scan():
    # Create a client
    client = dataplex_v1.DataScanServiceClient()

    # Initialize request argument(s)
    request = dataplex_v1.GetDataScanRequest(
        name="name_value",
    )

    # Make the request
    response = client.get_data_scan(request=request)

    # Handle the response
    print(response)
```

### Ruby

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-dataplex/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
require "google/cloud/dataplex/v1"

##
# Snippet for the get_data_scan call in the DataScanService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::Dataplex::V1::DataScanService::Client#get_data_scan.
#
def get_data_scan
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::Dataplex::V1::DataScanService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::Dataplex::V1::GetDataScanRequest.new

  # Call the get_data_scan method.
  result = client.get_data_scan request

  # The returned object is of type Google::Cloud::Dataplex::V1::DataScan.
  p result
end
```

### REST

如要查看資料剖析掃描結果，請使用 [`dataScans.get` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/get?hl=zh-tw)。

### 查看已發布的結果

如果資料剖析掃描結果發布至 Google Cloud 控制台的 BigQuery 和 Knowledge Catalog 頁面，您可以在來源資料表的「資料剖析檔」分頁中查看最新的掃描結果。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，按一下「Datasets」(資料集)，然後點選您的資料集。
4. 依序點按「總覽」**>「資料表」**，然後選取要查看資料剖析掃描結果的資料表。
5. 按一下「資料剖析檔」分頁標籤。

   系統會顯示最近發布的結果。

   **注意：** 如果這是第一次執行掃描，可能無法查看發布的結果。

### 查看最近一次的資料剖析掃描工作

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下資料剖析掃描的名稱。
3. 按一下「最近一次的工作結果」分頁標籤。

   如果至少有一項工作順利完成，**最近一次的工作結果**分頁就會提供最近一次工作的相關資訊。並列出掃描的資料表欄，以及掃描時發現的欄統計資料。

### gcloud

如要查看最近一次成功的資料剖析掃描，請使用 [`gcloud dataplex datascans describe` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/describe?hl=zh-tw)：

```
gcloud dataplex datascans describe DATASCAN \
--location=LOCATION \
--view=FULL
```

請替換下列變數：

* `DATASCAN`：要查看最新作業的資料剖析掃描名稱。
* `LOCATION`：建立資料剖析掃描的 Google Cloud 區域。
* `--view=FULL`：如要查看掃描工作結果，請指定 `FULL`。

### REST

如要查看最近的掃描作業，請使用 [`dataScans.get` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/get?hl=zh-tw)。

### 查看歷來掃描結果

Knowledge Catalog 會儲存最近 300 項作業的資料剖析掃描記錄，或過去一年的記錄 (以先到者為準)。

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下資料剖析掃描的名稱。
3. 按一下「工作記錄」分頁標籤。

   「工作記錄」分頁會提供過去工作相關資訊，例如每項工作掃描的記錄數量、工作狀態，以及工作執行時間。
4. 如要查看工作的詳細資訊，請按一下「工作 ID」欄中的任何工作。

### gcloud

如要查看歷來資料剖析掃描工作，請使用 [`gcloud dataplex datascans jobs list` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/jobs/list?hl=zh-tw)：

```
gcloud dataplex datascans jobs list \
--location=LOCATION \
--datascan=DATASCAN
```

請替換下列變數：

* `LOCATION`：建立資料剖析掃描的 Google Cloud 區域。
* `DATASCAN`：要查看作業的資料剖析掃描名稱。

### C#

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/dataplex/docs/reference/libraries?hl=zh-tw)」中的