Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 連線至 Blob 儲存體

BigQuery 管理員可以建立[連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，讓資料分析師存取儲存在 Azure Blob 儲存空間中的資料。

[BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw) 會透過連線存取 Blob 儲存體資料。BigQuery Omni 支援 [Azure 工作負載身分聯合](https://docs.microsoft.com/en-us/azure/active-directory/develop/workload-identity-federation)。BigQuery Omni 支援 Azure 工作負載身分聯盟，可讓您在租戶中授予 Azure 應用程式 Google 服務帳戶的存取權。您或 Google 無須管理任何應用程式用戶端密鑰。

建立 BigQuery Azure 連線後，您可以[查詢 Blob 儲存體資料](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)，也可以[將查詢結果匯出至 Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-export-results-to-azure-storage?hl=zh-tw)。

## 事前準備

* 請確認您已建立下列資源：

  + 已啟用 [BigQuery Connection API](https://console.cloud.google.com/apis/library/bigqueryconnection.googleapis.com?hl=zh-tw) 的[Google Cloud 專案](https://docs.cloud.google.com/docs/overview?hl=zh-tw#projects)。
  + 如果您採用以容量計價的收費模式，請務必為專案啟用 [BigQuery Reservation API](https://console.cloud.google.com/apis/library/bigqueryreservation.googleapis.com?hl=zh-tw)。如要瞭解定價資訊，請參閱 [BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)。
  + 具有 Azure 訂用帳戶的 Azure 租用戶。
  + 符合下列規格的 Azure 儲存體帳戶：

    - 一般用途 V2 帳戶或 Blob 儲存體帳戶。
    - 它使用階層式命名空間。詳情請參閱「[建立要搭配 Azure Data Lake Storage Gen2 使用的儲存空間帳戶](https://docs.microsoft.com/en-us/azure/storage/blobs/create-data-lake-storage-account)」。
    - 資料採用[支援的格式](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw#table-definition)。
    - 資料位於 `azure-eastus2` 區域。

## 必要的角色

* 如要取得建立連線來存取 Azure Blob 儲存空間資料所需的權限，請要求系統管理員授予您專案的 [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

  您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。
* 請確認您在租戶中擁有下列 Azure IAM 權限：
  + `Application.ReadWrite.All`
  + `AppRoleAssignment.ReadWrite.All`

## 配額

如要進一步瞭解配額，請參閱 [BigQuery Connection API](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#connection_api)。

## 建立 Azure 連線

如要建立 Azure 連線，請按照下列步驟操作：

1. [在 Azure 租用戶中建立應用程式](#create-azure-tenant)。
2. [建立 BigQuery Azure 連線](#create-azure-connection)。
3. [新增聯合憑證](#add-a-federated-credential)。
4. [將角色指派給 BigQuery Azure AD 應用程式](#assigning-a-role)。

如要進一步瞭解如何使用聯合身分憑證存取 Azure 中的資料，請參閱「[工作負載身分聯盟](https://docs.microsoft.com/en-us/azure/active-directory/develop/workload-identity-federation)」。

### 在 Azure 租戶中建立應用程式

如要在 Azure 租戶中建立應用程式，請按照下列步驟操作：

### Azure 入口網站

1. 在 Azure 入口網站中，前往「App registrations」，然後點選「New registration」。
2. 在「Name」部分，輸入應用程式名稱。
3. 在「Supported account types」中，選取「Accounts in this organizational directory only」。
4. 如要註冊新應用程式，請按一下「Register」。
5. 記下「應用程式 (用戶端) ID」。您必須在[建立連線](#create-azure-connection)時提供這個 ID。

### Terraform

在 Terraform 設定檔中新增下列內容：

```
  data "azuread_client_config" "current" {}

  resource "azuread_application" "example" {
    display_name = "bigquery-omni-connector"
    owners       = [data.azuread_client_config.current.object_id]
  }

  resource "azuread_service_principal" "example" {
    client_id                    = azuread_application.example.client_id
    app_role_assignment_required = false
    owners                       = [data.azuread_client_config.current.object_id]
  }
```

詳情請參閱如何[註冊 Azure 中的應用程式](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#register-an-application)。

### 建立連線

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，點選「新增資料」add。

   「新增資料」對話方塊隨即開啟。
3. 在「Filter By」(依據篩選) 窗格的「Data Source Type」(資料來源類型) 專區中，選取「Databases」(資料庫)。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `Azure`。
4. 在「精選資料來源」部分，按一下「Azure Blob 儲存體」。
5. 按一下「Azure Blob Storage Omni：BigQuery Federation」解決方案資訊卡。
6. 在「建立表格」對話方塊的「連線 ID」欄位中，選取「建立新的 ABS 連線」。
7. 在「外部資料來源」窗格中，輸入下列資訊：

   * 在「連線類型」中，選取「Azure 中的 BigLake (透過 BigQuery Omni)」。
   * 在「Connection ID」(連線 ID) 專區中輸入連線資源的 ID。可以使用英文字母、數字、破折號和底線。
   * 選取要建立連結的位置。
   * 選用：在「Friendly name」(好記名稱) 中輸入使用者容易記得的連線名稱，例如 `My connection resource`。好記名稱可以是任何資料值，只要您日後需要修改時可以輕鬆識別連線資源即可。
   * 選用：在「Description」(說明) 中輸入連線資源的說明。
   * 輸入 **Azure 租戶 ID**，也就是目錄 (租戶) ID。
   * 勾選「使用聯合身分」核取方塊，然後輸入 Azure 聯盟應用程式 (用戶端) ID。

     如要瞭解如何取得 Azure ID，請參閱[在 Azure 租戶中建立應用程式](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw#create-azure-tenant)。
8. 點選「建立連線」。
9. 點選「前往連線」。
10. 在「連線資訊」部分，記下「BigQuery Google 身分」的值，也就是服務帳戶 ID。這個 ID 是指Google Cloud 您授權存取應用程式的[服務帳戶](#assigning-a-role)。

### Terraform

```
  resource "google_bigquery_connection" "connection" {
    connection_id = "omni-azure-connection"
    location      = "azure-eastus2"
    description   = "created by terraform"

    azure {
      customer_tenant_id              = "TENANT_ID"
      federated_application_client_id = azuread_application.example.client_id
    }
  }
```

請將 `TENANT_ID` 改成包含 Blob 儲存體帳戶的 Azure 目錄的租戶 ID。

### bq

使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令。如要以 JSON 格式取得輸出內容，請使用 `--format=json` 參數。

```
bq mk --connection --connection_type='Azure' \
  --tenant_id=TENANT_ID \
  --location=AZURE_LOCATION \
  --federated_azure=true \
  --federated_app_client_id=APP_ID \
  CONNECTION_ID
```

更改下列內容：

* `TENANT_ID`：Azure 目錄的租用戶 ID，其中包含 Azure 儲存體帳戶。
* `AZURE_LOCATION`：Azure 儲存體資料所在的 Azure 區域。BigQuery Omni 支援 `azure-eastus2` 區域。
* `APP_ID`：Azure 應用程式 (用戶端) ID。如要瞭解如何取得這個 ID，請參閱「[在 Azure 租戶中建立應用程式](#create-azure-tenant)」。
* `CONNECTION_ID`：連線名稱。

輸出結果會與下列內容相似：

```
Connection CONNECTION_ID successfully created
Please add the following identity to your Azure application APP_ID
Identity: SUBJECT_ID
```

這項輸出內容包含下列值：

* `APP_ID`：您建立的應用程式 ID。
* `SUBJECT_ID`：使用者授權存取應用程式的 Google Cloud服務帳戶 ID。在 Azure 中建立聯盟憑證時，這是必填的值。

記下 `APP_ID` 和 `SUBJECT_ID` 值，以供後續步驟使用。

**注意：** 如要覆寫預設專案，請使用 `--project_id=PROJECT_ID` 參數。將 `PROJECT_ID` 替換為Google Cloud 專案 ID。

接著，為應用程式新增聯盟憑證。

### 新增聯合憑證

如要建立同盟憑證，請按照下列步驟操作：

### Azure 入口網站

1. 在 Azure 入口網站中前往「應用程式註冊」，然後按一下您的應用程式。
2. **依序選取「憑證和密鑰」>「聯合憑證」>「新增憑證」**。然後執行下列操作：

   1. 從「聯合憑證情境」清單中，選取「其他核發者」。
   2. 在「Issuer」中輸入 `https://accounts.google.com`。
   3. 在「主體 ID」中，輸入 Google Cloud 您[建立連結](#create-azure-connection)時取得的 **BigQuery Google 身分**。
   4. 在「Name」(名稱) 中輸入憑證名稱。
   5. 按一下「新增」。

### Terraform

在 Terraform 設定檔中新增下列內容：

```
  resource "azuread_application_federated_identity_credential" "example" {
    application_id = azuread_application.example.id
    display_name   = "omni-federated-credential"
    description    = "BigQuery Omni federated credential"
    audiences      = ["api://AzureADTokenExchange"]
    issuer         = "https://accounts.google.com"
    subject        = google_bigquery_connection.connection.azure[0].identity
  }
```

詳情請參閱「[設定應用程式以信任外部識別資訊提供者](https://docs.microsoft.com/en-us/azure/active-directory/develop/workload-identity-federation-create-trust?tabs=azure-portal)」。

### 將角色指派給 BigQuery 的 Azure 應用程式

如要將角色指派給 BigQuery 的 Azure 應用程式，請使用 Azure 入口網站、Azure PowerShell 或 Microsoft Management REST API：

### Azure 入口網站

如要執行角色指派，請以具備 `Microsoft.Authorization/roleAssignments/write` 權限的使用者身分登入 Azure 入口網站。角色指派作業可讓 BigQuery Azure 連線存取角色政策中指定的 Azure 儲存空間資料。

如要使用 Azure 入口網站新增角色指派，請按照下列步驟操作：

1. 在 Azure 儲存體帳戶中，於搜尋列輸入 `IAM`。
2. 按一下「存取權控管 (IAM)」。
3. 按一下「新增」，然後選取「新增角色指派」。
4. 如要提供唯讀存取權，請選取「儲存體 Blob 資料讀取者」角色。如要提供讀寫存取權，請選取「儲存體 Blob 資料參與者」角色。
5. 將「指派存取權給」設為「使用者、群組或服務主體」。
6. 按一下「選取成員」。
7. 在「Select」(選取) 欄位中，輸入[在 Azure 租戶中建立應用程式](#create-azure-tenant)時指定的 Azure 應用程式名稱。
8. 按一下 [儲存]。

詳情請參閱「[使用 Azure 入口網站指派 Azure 角色](https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal)」。

### Terraform

在 Terraform 設定檔中新增下列內容：

```
  resource "azurerm_role_assignment" "data_role" {
    scope                = data.azurerm_storage_account.example.id
    # Read permission for Omni on the storage account
    role_definition_name = "Storage Blob Data Reader"
    principal_id         = azuread_service_principal.example.id
  }
```

### Azure PowerShell

如要在資源範圍為服務主體新增角色指派，可以使用 [`New-AzRoleAssignment` 指令](https://docs.microsoft.com/en-us/powershell/module/az.resources/new-azroleassignment?view=azps-7.5.0)：

```
  New-AzRoleAssignment`
   -SignInName APP_NAME`
   -RoleDefinitionName ROLE_NAME`
   -ResourceName RESOURCE_NAME`
   -ResourceType RESOURCE_TYPE`
   -ParentResource PARENT_RESOURCE`
   -ResourceGroupName RESOURCE_GROUP_NAME
```

更改下列內容：

* `APP_NAME`：應用程式名稱。
* `ROLE_NAME`：要指派的角色名稱。
* `RESOURCE_NAME`：資源名稱。
* `RESOURCE_TYPE`：資源類型。
* `PARENT_RESOURCE`：父項資源。
* `RESOURCE_GROUP_NAME`：資源群組名稱。

如要進一步瞭解如何使用 Azure PowerShell 新增服務主體，請參閱「[使用 Azure PowerShell 指派 Azure 角色](https://docs.microsoft.com/azure/role-based-access-control/role-assignments-powershell#add-a-role-assignment)」。

### Azure CLI

如要在資源範圍為服務主體新增角色指派，可以使用 Azure 指令列工具。您必須具備儲存空間帳戶的 `Microsoft.Authorization/roleAssignments/write` 權限，才能授予角色。

如要將角色 (例如「儲存體 Blob 資料讀取者」角色) 指派給服務主體，請執行 [`az role assignment create` 指令](https://docs.microsoft.com/en-us/cli/azure/role/assignment?view=azure-cli-latest#az-role-assignment-create)：

```
  az role assignment create --role "Storage Blob Data Reader" \
    --assignee-object-id ${SP_ID} \
    --assignee-principal-type ServicePrincipal \
    --scope   subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP_NAME/providers/Microsoft.Storage/storageAccounts/STORAGE_ACCOUNT_NAME
```

更改下列內容：

* `SP_ID`：服務主體 ID。
  這個服務主體適用於[您建立的應用程式](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw#create-azure-tenant)。如要取得聯合連線的服務主體，請參閱[服務主體物件](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals#service-principal-object)。
* `STORAGE_ACCOUNT_NAME`：儲存空間帳戶名稱。
* `RESOURCE_GROUP_NAME`：資源群組名稱。
* `SUBSCRIPTION_ID`：訂閱 ID。

詳情請參閱「[使用 Azure CLI 指派 Azure 角色](https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-cli)」。

### Microsoft REST API

如要為服務主體新增角色指派，可以將 HTTP 要求傳送至 Microsoft Management。

如要呼叫 Microsoft Graph REST API，請先擷取應用程式的 OAuth 權杖。詳情請參閱「[在沒有使用者帳戶的情況下取得存取權](https://docs.microsoft.com/graph/auth-v2-service)」。呼叫 Microsoft Graph REST API 的應用程式必須具備 `Application.ReadWrite.All` 應用程式權限。

如要產生 OAuth 權杖，請執行下列指令：

```
  export TOKEN=$(curl -X POST \
    https://login.microsoftonline.com/TENANT_ID/oauth2/token \
    -H 'cache-control: no-cache' \
    -H 'content-type: application/x-www-form-urlencoded' \
    --data-urlencode "grant_type=client_credentials" \
    --data-urlencode "resource=https://graph.microsoft.com/" \
    --data-urlencode "client_id=CLIENT_ID" \
    --data-urlencode "client_secret=CLIENT_SECRET" \
  | jq --raw-output '.access_token')
```

更改下列內容：

* `TENANT_ID`：與包含 Azure 儲存體帳戶的 Azure 目錄 ID 相符的租戶 ID。
* `CLIENT_ID`：Azure 用戶端 ID。
* `CLIENT_SECRET`：Azure 用戶端密鑰。

取得要指派給服務主體的 [Azure 內建角色](https://docs.microsoft.com/azure/role-based-access-control/built-in-roles) ID。

常見角色包括：

* [Storage Blob Data Contributor](https://docs.microsoft.com/azure/role-based-access-control/built-in-roles#storage-blob-data-contributor)：
  `ba92f5b4-2d11-453d-a403-e96b0029c9fe`
* [儲存空間 Blob 資料讀取者](https://docs.microsoft.com/azure/role-based-access-control/built-in-roles#storage-blob-data-reader)：
  `2a2b9908-6ea1-4ae2-8e65-a410df84e7d1`

如要將角色指派給服務主體，請呼叫 Microsoft Graph REST API 至 Azure Resource Management REST API：

```
  export ROLE_ASSIGNMENT_ID=$(uuidgen)
  curl -X PUT \
'https://management.azure.com/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP_NAME/providers/Microsoft.Storage/storageAccounts/STORAGE_ACCOUNT_NAME/providers/Microsoft.Authorization/roleAssignments/ROLE_ASSIGNMENT_ID?api-version=2018-01-01-preview' \
    -H "authorization: Bearer ${TOKEN?}" \
    -H 'cache-control: no-cache' \
    -H 'content-type: application/json' \
    -d '{
        "properties": {
            "roleDefinitionId": "subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP_NAME/providers/Microsoft.Storage/storageAccounts/STORAGE_ACCOUNT_NAME/providers/Microsoft.Authorization/roleDefinitions/ROLE_ID",
            "principalId": "SP_ID"
        }
    }'
```

更改下列內容：

* `ROLE_ASSIGNMENT_ID`：角色 ID。
* `SP_ID`：服務主體 ID。
  這個服務主體適用於[您建立的應用程式](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw#create-azure-tenant)。如要取得聯邦連線的服務主體，請參閱「[服務主體物件](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals#service-principal-object)」。
* `SUBSCRIPTION_ID`：訂閱 ID。
* `RESOURCE_GROUP_NAME`：資源群組名稱。
* `STORAGE_ACCOUNT_NAME`：儲存空間帳戶名稱。
* `SUBSCRIPTION_ID`：訂閱 ID。

現在可以使用連線了。不過，Azure 中的角色指派可能會有傳播延遲。如果因為權限問題而無法使用連線，請稍後再試。

**注意：** 刪除連結後，用於存取 Azure 應用程式的 Google 身分識別就會遭到刪除。Azure 租戶中的應用程式不會遭到刪除。

## 與使用者共用連線

您可以授予下列角色，讓使用者查詢資料及管理連線：

* `roles/bigquery.connectionUser`：可讓使用者透過連線功能連結外部資料來源，並對其執行查詢。
* `roles/bigquery.connectionAdmin`：允許使用者管理連線。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)

   連線會列在專案中，位於「Connections」(連線) 群組。
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 按一下專案，然後依序點選「連線」和所需連線。
4. 在「詳細資料」窗格中，按一下「共用」即可共用連線。
   接著，按照下列步驟操作：

   1. 在「連線權限」對話方塊中，新增或編輯主體，與其他主體共用連線。
   2. 按一下 [儲存]。

### bq

您無法使用 bq 指令列工具共用連線。
如要共用連線，請使用 Google Cloud 控制台或 BigQuery Connections API 方法共用連線。

### API

請使用 BigQuery Connections REST API 參考資料部分中的 [`projects.locations.connections.setIAM` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest/v1/projects.locations.connections?hl=zh-tw#methods)，並提供 `policy` 資源的執行個體。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.resourcenames.ResourceName;
import com.google.cloud.bigquery.connection.v1.ConnectionName;
import com.google.cloud.bigqueryconnection.v1.ConnectionServiceClient;
import com.google.iam.v1.Binding;
import com.google.iam.v1.Policy;
import com.google.iam.v1.SetIamPolicyRequest;
import java.io.IOException;

// Sample to share connections
public class ShareConnection {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String location = "MY_LOCATION";
    String connectionId = "MY_CONNECTION_ID";
    shareConnection(projectId, location, connectionId);
  }

  static void shareConnection(String projectId, String location, String connectionId)
      throws IOException {
    try (ConnectionServiceClient client = ConnectionServiceClient.create()) {
      ResourceName resource = ConnectionName.of(projectId, location, connectionId);
      Binding binding =
          Binding.newBuilder()
              .addMembers("group:example-analyst-group@google.com")
              .setRole("roles/bigquery.connectionUser")
              .build();
      Policy policy = Policy.newBuilder().addBindings(binding).build();
      SetIamPolicyRequest request =
          SetIamPolicyRequest.newBuilder()
              .setResource(resource.toString())
              .setPolicy(policy)
              .build();
      client.setIamPolicy(request);
      System.out.println("Connection shared successfully");
    }
  }
}
```

## 後續步驟

* 瞭解不同[連線類型](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)。
* 瞭解如何[管理連線](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)。
* 進一步瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 瞭解 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。
* 瞭解如何[查詢 Blob 儲存體資料](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)。
* 瞭解如何[將查詢結果匯出至 Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-export-results-to-azure-storage?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]