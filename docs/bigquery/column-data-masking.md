Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 遮蓋資料欄資料

本文說明如何實作資料遮蓋，選擇性遮蓋機密資料。只要實作資料遮罩，就能為不同使用者群組提供不同層級的瀏覽權限。如需一般資訊，請參閱「[資料遮蓋簡介](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)」。

如要實作資料遮蓋，請在資料欄中新增資料政策。如要為資料欄新增資料遮蓋政策，請完成下列步驟：

1. 建立分類，並加入至少一個政策標記。
2. 選用：針對您建立的一或多個政策標記，將 Data Catalog 精細讀取者角色授予一或多個主體。
3. 為政策標記建立最多三項資料政策，將遮蓋規則和主體 (代表使用者或群組) 對應至該標記。
4. 在資料欄上設定政策標記。這會將與政策標記相關聯的資料政策對應至所選資料欄。
5. 將 BigQuery Masked Reader 角色指派給應有遮蓋資料存取權的使用者。最佳做法是在資料政策層級指派 BigQuery 遮蓋讀取者角色。在專案層級或更高層級指派角色，會授予使用者專案下所有資料政策的權限，這可能會導致權限過多而引發問題。

您可以使用 Google Cloud 控制台或 BigQuery Data Policy API 處理資料政策。

完成這些步驟後，使用者對資料欄執行查詢時，會根據所屬群組和獲派角色，取得未遮蓋資料、遮蓋資料，或收到存取遭拒錯誤。詳情請參閱「[遮蓋讀取者和精細讀取者角色的互動方式](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#role-interaction)」。

或者，您也可以直接對資料欄套用資料政策。詳情請參閱「[直接在資料欄上使用資料政策遮蓋資料](#data-policies-on-column)」。

## 使用政策標記遮蓋資料

使用政策標記，選擇性遮蓋機密資料。

### 事前準備

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the Data Catalog and BigQuery Data Policy APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=datacatalog.googleapis.com%2Cbigquerydatapolicy.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com&hl=zh-tw)

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the Data Catalog and BigQuery Data Policy APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=datacatalog.googleapis.com%2Cbigquerydatapolicy.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com&hl=zh-tw)

1. 新專案會自動啟用 BigQuery，但您可能需要在現有專案中啟用。

   啟用 BigQuery API (如果尚未啟用)。

   **啟用 API 所需的角色**

   您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「Service Usage 管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com&hl=zh-tw)
2. 如果您建立的資料政策參照[自訂遮蓋常式](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#custom_mask)，請建立相關聯的遮蓋 UDF，以便在後續步驟中使用。

**注意：** 您必須保持啟用 `datacatalog.googleapis.com` API，才能建立及管理用於資料遮蓋和資料欄層級安全性的 Data Catalog 政策標記和分類。雖然 Data Catalog 的中繼資料搜尋和目錄功能已淘汰，並轉換至 Knowledge Catalog，但政策標記專用的 Data Catalog API 功能並未淘汰。

### 可建立分類

建立分類的使用者或服務帳戶，必須具備 Data Catalog 政策標記管理員角色。

### 控制台

1. 前往 Google Cloud 控制台的「Policy tag taxonomies」(政策標記分類) 頁面。

   [前往「Policy tag taxonomies」(政策標記分類)](https://console.cloud.google.com/bigquery/security/secure/policy-tags?hl=zh-tw)
2. 按一下「Create taxonomy」(建立分類)。
3. 在「New taxonomy」(新增分類) 頁面中：

   1. 在「Taxonomy name」(分類名稱) 中，輸入要建立的分類名稱。
   2. 在「Description」(說明) 部分輸入說明。
   3. 如有需要，請變更「Project」(專案) 下方列出的專案。
   4. 如有需要，請變更「位置」下方列出的位置。
   5. 在「政策標記」下方，輸入政策標記名稱和說明。
   6. 如要為政策標記新增子政策標記，請按一下「Add subtag」(新增子標記)。
   7. 如要新增與其他政策標記同層級的新政策標記，請按一下「+ Add policy tag」(+ 新增政策標記)。
   8. 視分類需要，繼續新增政策標記和子政策標記。
   9. 為階層建立政策標記後，按一下「Create」(建立)。

### API

如要使用現有的分類，請呼叫 [`taxonomies.import`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies/import?hl=zh-tw)，取代下列程序的前兩個步驟。

1. 呼叫 [`taxonomies.create`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies/create?hl=zh-tw) 建立分類。
2. 呼叫 [`taxonomies.policyTags.create`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies.policyTags/create?hl=zh-tw) 建立政策標記。

### 使用政策標記

如要進一步瞭解如何使用政策標記，例如如何查看或更新政策標記，請參閱「[使用政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#work_with_policy_tags)」。如需最佳做法，請參閱「[在 BigQuery 中使用政策標記的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)」。

### 建立資料政策

建立資料政策的使用者或服務帳戶必須具備 `bigquery.dataPolicies.create`、`bigquery.dataPolicies.setIamPolicy` 和 `datacatalog.taxonomies.get` 權限。

`bigquery.dataPolicies.create` 和 `bigquery.dataPolicies.setIamPolicy` 權限包含在 BigQuery 資料政策管理員、BigQuery 管理員和 BigQuery 資料擁有者角色中。Data Catalog 管理員和 Data Catalog 檢視者角色具備 `datacatalog.taxonomies.get` 權限。

如果您建立的資料政策參照[自訂遮蓋常式](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#custom_mask)，則也需要[常式權限](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw#permissions)。

如要自訂遮蓋，請授予使用者 BigQuery 管理員或 BigQuery 資料擁有者角色，確保他們具備常式和資料政策的必要權限。

一項政策標記最多可建立九項資料政策。其中一項政策會保留給[資料欄層級存取控管設定](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_up_column-level_access_control)。

### 控制台

1. 前往 Google Cloud 控制台的「Policy tag taxonomies」(政策標記分類) 頁面。

   [前往「Policy tag taxonomies」(政策標記分類)](https://console.cloud.google.com/bigquery/security/secure/policy-tags?hl=zh-tw)
2. 按一下要開啟的分類名稱。
3. 選取政策標記。
4. 點按「管理資料政策」。
5. 在「Data Policy Name」(資料政策名稱) 中，輸入資料政策的名稱。資料政策名稱在資料政策所在的專案中不得重複。
6. 在「Masking Rule」(遮蓋規則)，選擇預先定義的遮蓋規則或自訂遮蓋常式。如要選取自訂遮蓋常式，請確認您在專案層級具備 `bigquery.routines.get` 和 `bigquery.routines.list` 權限。
7. 在「Principal」(主體) 部分，輸入一或多個使用者或群組的名稱，您要授予這些使用者或群組對資料欄的遮蓋存取權。請注意，您在此輸入的所有使用者和群組都會獲得 BigQuery 遮蓋讀取者角色。
8. 按一下「提交」。

### API

1. 呼叫 [`create`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/create?hl=zh-tw) 方法。傳入符合下列規定的 [`DataPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies?hl=zh-tw#resource:-datapolicy) 資源：

   * `dataPolicyType` 欄位設為 `DATA_MASKING_POLICY`。
   * `dataMaskingPolicy` 欄位會識別要使用的資料遮蓋規則或常式。
   * `dataPolicyId` 欄位會提供資料政策的名稱，該名稱在資料政策所在的專案中不得重複。
2. 呼叫 [`setIamPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/setIamPolicy?hl=zh-tw) 方法，並傳入 [`Policy`](https://docs.cloud.google.com/iam/docs/reference/rest/v1/Policy?hl=zh-tw)。`Policy` 必須識別有權存取遮蓋資料的主體，並為 `role` 欄位指定 `roles/bigquerydatapolicy.maskedReader`。

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const datapolicy = require('@google-cloud/bigquery-datapolicies');
const {DataPolicyServiceClient} = datapolicy.v2;
const protos = datapolicy.protos.google.cloud.bigquery.datapolicies.v2;
const {status} = require('@grpc/grpc-js');

const dataPolicyServiceClient = new DataPolicyServiceClient();

/**
 * Creates a data policy to apply a data masking rule to a specific BigQuery table column.
 * This is a primary mechanism for implementing column-level security in BigQuery.
 *
 * @param {string} projectId The Google Cloud project ID (for example, 'example-project-id')
 * @param {string} location The Google Cloud location. Example: 'us'
 * @param {string} dataPolicyId The user-assigned ID of the data policy. Example: 'example-data-policy-id'
 */
async function createDataPolicy(projectId, location, dataPolicyId) {
  const parent = `projects/${projectId}/locations/${location}`;

  const dataPolicy = {
    dataPolicyType: protos.DataPolicy.DataPolicyType.DATA_MASKING_POLICY,
    dataMaskingPolicy: {
      predefinedExpression:
        protos.DataMaskingPolicy.PredefinedExpression.SHA256,
    },
  };

  const request = {
    parent,
    dataPolicyId,
    dataPolicy,
  };

  try {
    const [response] = await dataPolicyServiceClient.createDataPolicy(request);
    console.log(`Successfully created data policy: ${response.name}`);
    console.log(`Data policy ID: ${response.dataPolicyId}`);
    console.log(`Data policy type: ${response.dataPolicyType}`);
    if (response.dataMaskingPolicy) {
      console.log(
        `Data masking expression: ${response.dataMaskingPolicy.predefinedExpression}`,
      );
    }
  } catch (err) {
    if (err.code === status.ALREADY_EXISTS) {
      console.log(
        `Data policy '${dataPolicyId}' already exists in location '${location}' of project '${projectId}'.`,
      );
      console.log(
        'Consider updating the existing data policy or using a different dataPolicyId.',
      );
    } else {
      console.error('Error creating data policy:', err.message);
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.api_core import exceptions
from google.cloud import bigquery_datapolicies_v2

client = bigquery_datapolicies_v2.DataPolicyServiceClient()


def create_data_policy(project_id: str, location: str, data_policy_id: str) -> None:
    """Creates a data policy to apply a data masking rule to a specific BigQuery table column.
    This is a primary mechanism for implementing column-level security in BigQuery.

    Args:
        project_id (str): The Google Cloud project ID.
        location (str): The geographic location of the data policy (for example, "us-central1").
        data_policy_id (str): The ID for the new data policy.
    """

    parent = f"projects/{project_id}/locations/{location}"

    # Define the data masking policy.
    # Here, we specify a SHA-256 predefined expression for data masking.
    data_masking_policy = bigquery_datapolicies_v2.DataMaskingPolicy(
        predefined_expression=bigquery_datapolicies_v2.DataMaskingPolicy.PredefinedExpression.SHA256
    )

    # Create the DataPolicy object.
    # We set the type to DATA_MASKING_POLICY and assign the defined masking policy.
    data_policy = bigquery_datapolicies_v2.DataPolicy(
        data_policy_type=bigquery_datapolicies_v2.DataPolicy.DataPolicyType.DATA_MASKING_POLICY,
        data_masking_policy=data_masking_policy,
    )

    request = bigquery_datapolicies_v2.CreateDataPolicyRequest(
        parent=parent,
        data_policy_id=data_policy_id,
        data_policy=data_policy,
    )

    try:
        response = client.create_data_policy(request=request)
        print(f"Successfully created data policy: {response.name}")
        print(f"Data Policy ID: {response.data_policy_id}")
        print(f"Data Policy Type: {response.data_policy_type.name}")
        print(
            "Data Masking Predefined Expression:"
            f" {response.data_masking_policy.predefined_expression.name}"
        )
    except exceptions.AlreadyExists as e:
        print(
            f"Error: Data policy '{data_policy_id}' already exists in project"
            f" '{project_id}' in location '{location}'. Use a unique ID or"
            " update the existing policy if needed."
        )

    except exceptions.NotFound as e:
        print(
            f"Error: The specified project '{project_id}' or location '{location}'"
            " was not found or is inaccessible. Make sure the project ID and"
            " location are correct and you have the necessary permissions."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.AlreadyExistsException;
import com.google.api.gax.rpc.ApiException;
import com.google.api.gax.rpc.NotFoundException;
import com.google.cloud.bigquery.datapolicies.v2.CreateDataPolicyRequest;
import com.google.cloud.bigquery.datapolicies.v2.DataMaskingPolicy;
import com.google.cloud.bigquery.datapolicies.v2.DataMaskingPolicy.PredefinedExpression;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicy;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicy.DataPolicyType;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicyServiceClient;
import com.google.cloud.bigquery.datapolicies.v2.LocationName;
import java.io.IOException;

public class CreateDataPolicy {

  /**
   * Creates a data policy to apply a data masking rule to a specific BigQuery table column.
   *
   * @param projectId The Google Cloud project ID (for example, "example-project-id").
   * @param location The geographic location of the data policy (for example, "us-central1").
   * @param dataPolicyId The user-assigned ID for the new data policy (for example,
   *     "example_data_policy").
   */
  public static void createDataPolicy(String projectId, String location, String dataPolicyId) {
    LocationName parent = LocationName.of(projectId, location);

    DataMaskingPolicy dataMaskingPolicy =
        DataMaskingPolicy.newBuilder()
            .setPredefinedExpression(PredefinedExpression.SHA256)
            .build();

    DataPolicy dataPolicy =
        DataPolicy.newBuilder()
            .setDataPolicyType(DataPolicyType.DATA_MASKING_POLICY)
            .setDataMaskingPolicy(dataMaskingPolicy)
            .build();

    CreateDataPolicyRequest request =
        CreateDataPolicyRequest.newBuilder()
            .setParent(parent.toString())
            .setDataPolicyId(dataPolicyId)
            .setDataPolicy(dataPolicy)
            .build();

    try (DataPolicyServiceClient client = DataPolicyServiceClient.create()) {
      DataPolicy response = client.createDataPolicy(request);

      System.out.printf("Successfully created data policy: %s%n", response.getName());
      System.out.printf("Data Policy ID: %s%n", response.getDataPolicyId());
      System.out.printf("Data Policy Type: %s%n", response.getDataPolicyType());
      if (response.hasDataMaskingPolicy()) {
        System.out.printf(
            "Data Masking Predefined Expression: %s%n",
            response.getDataMaskingPolicy().getPredefinedExpression());
      }
    } catch (AlreadyExistsException err) {
      System.err.printf(
          "error: data policy '%s' already exists in location '%s' for project '%s': %s%n",
          dataPolicyId, location, projectId, err.getMessage());
    } catch (NotFoundException err) {
      System.err.printf(
          "error: project '%s' or location '%s' was not found: %s%n",
          projectId, location, err.getMessage());
    } catch (ApiException | IOException err) {
      System.err.printf(
          "error: failed to create data policy '%s' in location '%s' for project '%s': %s%n",
          dataPolicyId, location, projectId, err.getMessage());
    }
  }
```

### 在資料欄上設定政策標記

如要為資料欄設定資料政策，請將與資料政策相關聯的政策標記附加至資料欄。

設定政策標記的使用者或服務帳戶必須具備 `datacatalog.taxonomies.get` 和 `bigquery.tables.setCategory` 權限。Data Catalog 政策標記管理員和專案檢視者角色具備 `datacatalog.taxonomies.get`。BigQuery 管理員 (`roles/bigquery.admin`) 和 BigQuery 資料擁有者 (`roles/bigquery.dataOwner`) 角色包含 `bigquery.tables.setCategory`。

如要在Google Cloud 控制台中查看組織內所有專案的分類和政策標記，使用者必須具備 `resourcemanager.organizations.get` 權限，該權限包含在組織檢視者角色中。使用 API 或 `bq` 指令列工具時，則「不」需要這項權限。

**注意：** 每個資料欄只能指派一個政策標記。

### 控制台

使用Google Cloud 控制台[修改結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)，設定政策標記。

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 BigQuery Explorer 中，找出並選取要更新的資料表。系統會開啟該資料表的結構定義。
3. 點選「編輯結構定義」。
4. 在「Current schema」(目前結構定義) 畫面中，選取目標資料欄，然後按一下「Add policy tag」(新增政策標記)。
5. 在「Add a policy tag」(新增政策標記) 畫面中，找出並選取要套用至資料欄的政策標記。
6. 按一下「選取」。畫面應會出現如下所示的內容：
7. 按一下 [儲存]。

### bq

1. 將結構定義寫入本機檔案。

   ```
   bq show --schema --format=prettyjson \
      project-id:dataset.table > schema.json
   ```

   其中：

   * project-id 是您的專案 ID。
   * dataset 是資料集的名稱，其中包含您要更新的資料表。
   * table 是您要更新之資料表的名稱。
2. 修改 schema.json，在資料欄上設定政策標記。針對 `policyTags` 的 `names` 欄位值，請使用[政策標記資源名稱](#retrieve_policy_tag_name)。

   ```
   [
    ...
    {
      "name": "ssn",
      "type": "STRING",
      "mode": "REQUIRED",
      "policyTags": {
        "names": ["projects/project-id/locations/location/taxonomies/taxonomy-id/policyTags/policytag-id"]
      }
    },
    ...
   ]
   ```
3. 更新結構定義。

   ```
   bq update \
      project-id:dataset.table schema.json
   ```

### API

如果是現有資料表，請呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw)；如果是新資料表，請呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)。使用傳入的 `Table` 物件 `schema` 屬性，在結構定義定義中設定政策標記。請參閱指令列範例結構定義，瞭解如何設定政策標記。

使用現有資料表時，建議使用 `tables.patch` 方法，因為 `tables.update` 方法會取代整個資料表資源。

### 強制執行存取控管

為政策標記建立資料政策時，系統會自動強制執行存取控管。如果使用者具備「遮蓋讀取者」角色，則套用該政策標記的所有資料欄都會傳回遮蓋資料，以回應使用者的查詢。

如要停止強制執行存取控管，您必須先刪除與分類中政策標記相關聯的所有資料政策。詳情請參閱「[強制執行存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#enforce_access_control)」。

### 取得資料政策

如要取得資料政策的相關資訊，請按照下列步驟操作：

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {DataPolicyServiceClient} =
  require('@google-cloud/bigquery-datapolicies').v2;
const {status} = require('@grpc/grpc-js');

const client = new DataPolicyServiceClient();

/**
 * Gets a specific data policy from the BigQuery Data Policy API by its name.
 *
 * This sample demonstrates how to fetch the details of an existing data policy.
 * Data policies are used to define rules for data masking or row-level security
 * on BigQuery tables.
 *
 * @param {string} projectId The Google Cloud project ID (for example, 'example-project-id')
 * @param {string} [location='us'] The Google Cloud location of the data policy (For example, 'us', 'europe-west2').
 * @param {string} [dataPolicyId='example-data-policy'] The ID of the data policy to retrieve.
 */
async function getDataPolicy(
  projectId,
  location = 'us',
  dataPolicyId = 'example-data-policy',
) {
  const name = client.dataPolicyPath(projectId, location, dataPolicyId);

  const request = {
    name,
  };

  try {
    const [dataPolicy] = await client.getDataPolicy(request);
    console.log('Successfully retrieved data policy:');
    console.log(`  Name: ${dataPolicy.name}`);
    console.log(`  Type: ${dataPolicy.dataPolicyType}`);
    if (dataPolicy.dataMaskingPolicy) {
      console.log(
        `  Data Masking Policy: ${dataPolicy.dataMaskingPolicy.predefinedExpression || dataPolicy.dataMaskingPolicy.routine}`,
      );
    }
    if (dataPolicy.grantees && dataPolicy.grantees.length > 0) {
      console.log(`  Grantees: ${dataPolicy.grantees.join(', ')}`);
    }
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(
        `Error: Data policy '${dataPolicyId}' not found in location '${location}' for project '${projectId}'.`,
      );
      console.error(
        'Make sure the data policy ID, project ID, and location are correct.',
      );
    } else {
      console.error('Error retrieving data policy:', err.message);
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.api_core import exceptions
from google.cloud import bigquery_datapolicies_v2

client = bigquery_datapolicies_v2.DataPolicyServiceClient()


def get_data_policy(
    project_id: str,
    location: str,
    data_policy_id: str,
) -> None:
    """Gets a specific data policy from the BigQuery Data Policy API by its name.


    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the data policy (for example, "us", "eu").
        data_policy_id: The user-assigned ID of the data policy.
    """
    client = bigquery_datapolicies_v2.DataPolicyServiceClient()

    data_policy_name = client.data_policy_path(
        project=project_id,
        location=location,
        data_policy=data_policy_id,
    )

    try:
        response = client.get_data_policy(name=data_policy_name)

        print(f"Successfully retrieved data policy: {response.name}")
        print(f"  Data Policy ID: {response.data_policy_id}")
        print(f"  Data Policy Type: {response.data_policy_type.name}")
        if response.policy_tag:
            print(f"  Policy Tag: {response.policy_tag}")
        if response.grantees:
            print(f"  Grantees: {', '.join(response.grantees)}")
        if response.data_masking_policy:
            masking_policy = response.data_masking_policy
            if masking_policy.predefined_expression:
                print(
                    f"  Data Masking Predefined Expression: {masking_policy.predefined_expression.name}"
                )
            elif masking_policy.routine:
                print(f"  Data Masking Routine: {masking_policy.routine}")

    except exceptions.NotFound:
        print(f"Error: Data policy '{data_policy_name}' not found.")
        print("Make sure the data policy ID, project ID, and location are correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.api.gax.rpc.NotFoundException;
import com.google.cloud.bigquery.datapolicies.v2.DataMaskingPolicy;
import com.google.cloud.bigquery.datapolicies.v2.DataMaskingPolicy.PredefinedExpression;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicy;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicyName;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicyServiceClient;
import java.io.IOException;

public class GetDataPolicy {

  /**
   * Gets a specific data policy from the BigQuery Data Policy API by its name.
   *
   * @param projectId The Google Cloud project ID (for example, "example-project-id").
   * @param location The geographic location of the data policy (for example, "us-central1").
   * @param dataPolicyId The user-assigned ID of the data policy (for example,
   *     "example_data_policy").
   */
  public static void getDataPolicy(String projectId, String location, String dataPolicyId) {
    DataPolicyName dataPolicyName = DataPolicyName.of(projectId, location, dataPolicyId);

    try (DataPolicyServiceClient client = DataPolicyServiceClient.create()) {
      DataPolicy response = client.getDataPolicy(dataPolicyName);

      System.out.printf("Successfully retrieved data policy: %s%n", response.getName());
      System.out.printf("  Data Policy ID: %s%n", response.getDataPolicyId());
      System.out.printf("  Data Policy Type: %s%n", response.getDataPolicyType());
      if (!response.getPolicyTag().isEmpty()) {
        System.out.printf("  Policy Tag: %s%n", response.getPolicyTag());
      }
      if (!response.getGranteesList().isEmpty()) {
        System.out.printf("  Grantees: %s%n", String.join(", ", response.getGranteesList()));
      }
      if (response.hasDataMaskingPolicy()) {
        DataMaskingPolicy maskingPolicy = response.getDataMaskingPolicy();
        if (maskingPolicy.getPredefinedExpression()
            != PredefinedExpression.PREDEFINED_EXPRESSION_UNSPECIFIED) {
          System.out.printf(
              "  Data Masking Predefined Expression: %s%n",
              maskingPolicy.getPredefinedExpression());
        } else if (!maskingPolicy.getRoutine().isEmpty()) {
          System.out.printf("  Data Masking Routine: %s%n", maskingPolicy.getRoutine());
        }
      }
    } catch (NotFoundException err) {
      System.err.printf(
          "error: data policy '%s' not found: %s%n", dataPolicyName, err.getMessage());
    } catch (ApiException | IOException err) {
      System.err.printf(
          "error: failed to get data policy '%s': %s%n", dataPolicyName, err.getMessage());
    }
  }
```

### 檢查資料政策的身分與存取權管理權限

如要取得資料政策的 IAM 政策，請按照下列步驟操作：

### API

呼叫 [`testIamPermissions` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/testIamPermissions?hl=zh-tw)。

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {DataPolicyServiceClient} =
  require('@google-cloud/bigquery-datapolicies').v2;
const {status} = require('@grpc/grpc-js');

const client = new DataPolicyServiceClient();

/**
 * Get the IAM policy for a specified data policy resource from the BigQuery Data Policy API.
 * This is useful for auditing which members have which roles on the policy.
 *
 *
 * @param {string} projectId Google Cloud Project ID (For example, 'example-project-id')
 * @param {string} location Google Cloud Location (For example, 'us-central1')
 * @param {string} dataPolicyId The ID of the data policy (For example, 'example-data-policy-id')
 */
async function getIamPolicy(projectId, location, dataPolicyId) {
  const resourceName = client.dataPolicyPath(projectId, location, dataPolicyId);

  const request = {
    resource: resourceName,
  };

  try {
    const [policy] = await client.getIamPolicy(request);
    console.log(
      'Successfully retrieved IAM policy for data policy %s:',
      resourceName,
    );
    console.log(JSON.stringify(policy, null, 2));
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(
        `Error: Data Policy '${dataPolicyId}' not found in location '${location}' of project '${projectId}'. ` +
          'Make sure the data policy exists and the resource name is correct.',
      );
    } else {
      console.error(
        `Error getting IAM policy for data policy '${dataPolicyId}':`,
        err,
      );
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.api_core import exceptions
from google.cloud import bigquery_datapolicies_v2
from google.iam.v1 import iam_policy_pb2

client = bigquery_datapolicies_v2.DataPolicyServiceClient()


def get_data_policy_iam_policy(
    project_id: str,
    location: str,
    data_policy_id: str,
) -> None:
    """Get the IAM policy for a specified data policy resource from the BigQuery Data Policy API.
    This is useful for auditing which members have which roles on the policy.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the data policy (for example, "us").
        data_policy_id: The ID of the data policy.
    """

    resource_name = client.data_policy_path(
        project=project_id,
        location=location,
        data_policy=data_policy_id,
    )

    request = iam_policy_pb2.GetIamPolicyRequest(resource=resource_name)

    try:
        policy = client.get_iam_policy(request=request)

        print(f"Successfully retrieved IAM policy for data policy: {resource_name}")
        print("Policy Version:", policy.version)
        if policy.bindings:
            print("Policy Bindings:")
            for binding in policy.bindings:
                print(f"  Role: {binding.role}")
                print(f"  Members: {', '.join(binding.members)}")
                if binding.condition.expression:
                    print(f"  Condition: {binding.condition.expression}")
        else:
            print("No bindings found in the policy.")

    except exceptions.NotFound:
        print(f"Error: Data policy '{resource_name}' not found.")
        print("Make sure the project ID, location, and data policy ID are correct.")
    except exceptions.GoogleAPIError as e:
        print(f"An API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.api.gax.rpc.NotFoundException;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicyName;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicyServiceClient;
import com.google.iam.v1.Binding;
import com.google.iam.v1.GetIamPolicyRequest;
import com.google.iam.v1.Policy;
import java.io.IOException;

public class GetIamPolicy {

  /**
   * Gets the IAM policy for a specified data policy resource from the BigQuery Data Policy API.
   *
   * @param projectId The Google Cloud project ID (for example, "example-project-id").
   * @param location The geographic location of the data policy (for example, "us-central1").
   * @param dataPolicyId The ID of the data policy (for example, "example_data_policy").
   */
  public static void getIamPolicy(String projectId, String location, String dataPolicyId) {
    DataPolicyName resourceName = DataPolicyName.of(projectId, location, dataPolicyId);

    GetIamPolicyRequest request =
        GetIamPolicyRequest.newBuilder().setResource(resourceName.toString()).build();

    try (
```