Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 遮蓋資料欄資料

本文說明如何實作資料遮蓋，有選擇性地遮蓋敏感資料。實作資料遮蓋功能後，您就能為不同使用者群組提供不同層級的資料檢視權限。如需一般資訊，請參閱「[資料遮蓋簡介](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)」。

如要導入資料遮蓋功能，請在資料欄中新增資料政策。如要為資料欄新增資料遮蓋政策，請完成下列步驟：

1. 建立分類，並至少包含一個政策標記。
2. 選用：在您建立的一或多個政策標記上，將「Data Catalog 精細讀取者」角色授予一或多個主體。
3. 為政策標記建立最多三項資料政策，將遮蓋規則和主體 (代表使用者或群組) 對應至該標記。
4. 在資料欄上設定政策標記。將與政策標記相關聯的資料政策對應至所選資料欄。
5. 將 BigQuery「經過遮蓋的讀取者」角色指派給應有權存取遮蓋資料的使用者。最佳做法是在資料政策層級指派 BigQuery 遮蓋讀取者角色。在專案層級以上指派角色，會授予使用者專案下所有資料政策的權限，可能導致權限過多而引發問題。

您可以使用 Google Cloud 控制台或 BigQuery Data Policy API 來處理資料政策。

完成上述步驟後，使用者對資料欄執行查詢時，會根據所屬群組和獲授的角色，取得未遮蓋的資料、遮蓋的資料或存取遭拒錯誤。詳情請參閱「[遮蓋讀者和精細讀者角色如何互動](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#role-interaction)」。

或者，您也可以直接在資料欄上套用資料政策。詳情請參閱「[直接在資料欄上使用資料政策遮蓋資料](#data-policies-on-column)」。

## 使用政策標記遮蓋資料

使用政策標記選擇性遮蓋機密資料。

### 事前準備

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
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
- Enable the Data Catalog and BigQuery Data Policy APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=datacatalog.googleapis.com%2Cbigquerydatapolicy.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com&hl=zh-tw)

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
- Enable the Data Catalog and BigQuery Data Policy APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=datacatalog.googleapis.com%2Cbigquerydatapolicy.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com&hl=zh-tw)

1. 新專案會自動啟用 BigQuery，但您可能需要在現有專案中啟用這項服務。

   啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com&hl=zh-tw)
2. 如果您要建立的資料政策參照[自訂遮蓋常式](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#custom_mask)，請建立相關聯的遮蓋 UDF，以便在後續步驟中使用。

### 可建立分類

建立分類架構的使用者或服務帳戶必須獲派 Data Catalog 政策代碼管理員角色。

### 控制台

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下「建立分類」。
3. 在「New taxonomy」(新增分類) 頁面中：

   1. 在「分類名稱」部分，輸入要建立的分類名稱。
   2. 在「說明」中輸入說明。
   3. 如有需要，請變更「Project」下方列出的專案。
   4. 如有需要，請變更「位置」下方列出的位置。
   5. 在「政策標記」下方，輸入政策標記名稱和說明。
   6. 如要為政策標記新增子項政策標記，請按一下「新增子項標記」。
   7. 如要在與其他政策標記相同的層級新增政策標記，請點選「+ 新增政策標記」。
   8. 視需要繼續為分類架構新增政策標記和子項政策標記。
   9. 為階層建立完政策標記後，請按一下「建立」。

### API

如要使用現有分類，請呼叫
[`taxonomies.import`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies/import?hl=zh-tw)
，取代下列程序的前兩個步驟。

1. 呼叫 [`taxonomies.create`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies/create?hl=zh-tw) 建立分類。
2. 呼叫 [`taxonomies.policytag.create`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies.policyTags/create?hl=zh-tw) 建立政策標記。

### 使用政策標記

如要進一步瞭解如何使用政策標記 (例如查看或更新政策標記)，請參閱「[使用政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#work_with_policy_tags)」。如需最佳做法，請參閱「[在 BigQuery 中使用政策標記的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)」。

### 建立資料政策

建立資料政策的使用者或服務帳戶必須具備 `bigquery.dataPolicies.create`、`bigquery.dataPolicies.setIamPolicy` 和 `datacatalog.taxonomies.get` 權限。

「BigQuery 資料政策管理員」、「BigQuery 管理員」和「BigQuery 資料擁有者」角色都具備 `bigquery.dataPolicies.create` 和 `bigquery.dataPolicies.setIamPolicy` 權限。「`datacatalog.taxonomies.get`」權限包含在 Data Catalog 管理員和 Data Catalog 檢視者角色中。

如果您要建立的資料政策參照[自訂遮蓋常式](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#custom_mask)，則也需要[常式權限](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw#permissions)。

如果是自訂遮蓋，請授予使用者 BigQuery 管理員或 BigQuery 資料擁有者角色，確保他們具備常式和資料政策的必要權限。

每個政策標記最多可建立九項資料政策。其中一項政策會保留給[資料欄層級存取控管設定](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_up_column-level_access_control)。

### 控制台

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下分類名稱即可開啟。
3. 選取政策標記。
4. 按一下「管理資料政策」。
5. 在「資料政策名稱」中，輸入資料政策的名稱。資料政策名稱在資料政策所屬專案中不得重複。
6. 在「遮蓋規則」中，選擇預先定義的遮蓋規則或自訂遮蓋常式。如要選取自訂遮蓋常式，請務必在專案層級同時具備 `bigquery.routines.get` 和 `bigquery.routines.list` 權限。
7. 在「主體」中，輸入一或多個使用者或群組的名稱，授予這些對象資料欄的遮蓋存取權。請注意，您在此輸入的所有使用者和群組都會獲派 BigQuery 遮蓋讀取者角色。
8. 按一下「提交」。

### API

1. 呼叫 [`create`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/create?hl=zh-tw) 方法。傳遞符合下列條件的[`DataPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies?hl=zh-tw#resource:-datapolicy)資源：

   * `dataPolicyType` 欄位設為 `DATA_MASKING_POLICY`。
   * `dataMaskingPolicy` 欄位會識別要使用的資料遮蓋規則或常式。
   * `dataPolicyId` 欄位會提供資料政策的名稱，該名稱在資料政策所屬專案中不得重複。
2. 呼叫 [`setIamPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/setIamPolicy?hl=zh-tw) 方法，並傳入 [`Policy`](https://docs.cloud.google.com/iam/docs/reference/rest/v1/Policy?hl=zh-tw)。`Policy`必須識別獲准存取遮蓋資料的主體，並為 `role` 欄位指定 `roles/bigquerydatapolicy.maskedReader`。

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

### 在資料欄上設定政策標記

將與資料政策相關聯的政策標記附加至資料欄，即可在資料欄上設定資料政策。

設定政策標記的使用者或服務帳戶必須具備 `datacatalog.taxonomies.get` 和 `bigquery.tables.setCategory` 權限。`datacatalog.taxonomies.get` 包含在 Data Catalog 政策標記管理員和專案檢視者角色中。`bigquery.tables.setCategory` 包含在 BigQuery 管理員 (`roles/bigquery.admin`) 和 BigQuery 資料擁有者 (`roles/bigquery.dataOwner`) 角色中。

如要在Google Cloud 控制台中查看機構內所有專案的分類和政策標記，使用者必須具備`resourcemanager.organizations.get`權限，這項權限包含在機構檢視者角色中。

**注意：** 每個資料欄只能指派一個政策標記。

### 控制台

使用Google Cloud 控制台[修改結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)，設定政策標記。

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 BigQuery 探索器中，找出並選取要更新的資料表。系統會開啟該資料表的資料表結構定義。
3. 點選「編輯結構定義」。
4. 在「目前的結構定義」畫面上，選取目標資料欄，然後按一下「新增政策標記」。
5. 在「新增政策標記」畫面中，找出並選取要套用至資料欄的政策標記。
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
   * dataset 是含有您要更新資料表的資料集名稱。
   * table 是您要更新之資料表的名稱。
2. 修改 schema.json，為資料欄設定政策標記。如要取得 `policyTags` 的 `names` 欄位值，請使用[政策標記資源名稱](#retrieve_policy_tag_name)。

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

如為現有資料表，請呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw)；如為新資料表，請呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)。使用您傳入的 `Table` 物件的 `schema` 屬性，在結構定義中設定政策標記。請參閱指令列範例結構定義，瞭解如何設定政策標記。

處理現有資料表時，建議使用 `tables.patch` 方法，因為 `tables.update` 方法會取代整個資料表資源。

### 強制執行存取控管

為政策標記建立資料政策時，系統會自動強制執行存取控管。如果使用者具備「經過遮蓋的讀取者」角色，系統會在回應查詢時，針對套用該政策標記的所有資料欄傳回遮蓋資料。

如要停止強制執行存取控管，您必須先刪除分類中與政策標記相關聯的所有資料政策。詳情請參閱[強制執行存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#enforce_access_control)。

### 取得資料政策

如要取得資料政策的相關資訊，請按照下列步驟操作：

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

### 檢查資料政策的 IAM 權限

如要取得資料政策的 IAM 政策，請按照下列步驟操作：

### API

呼叫 [`testIamPermissions` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/testIamPermissions?hl=zh-tw)。

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

### 列出資料政策

如要列出資料政策，請按照下列步驟操作：

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {DataPolicyServiceClient} =
  require('@google-cloud/bigquery-datapolicies').v2;
const {status} = require('@grpc/grpc-js');

const client = new DataPolicyServiceClient();

/**
 * Lists all data policies in a given project and location.
 *
 * Data policies define rules for data masking, row-level security, or column-level security.
 *
 * @param {string} projectId The Google Cloud project ID. (for example, 'example-project-id')
 * @param {string} location The Google Cloud location of the data policies. (For example, 'us')
 */
async function listDataPolicies(projectId, location) {
  const parent = `projects/${projectId}/locations/${location}`;

  const request = {
    parent,
  };

  try {
    console.log(
      `Listing data policies for project: ${projectId} in location: ${location}`,
    );
    const [dataPolicies] = await client.listDataPolicies(request);

    if (dataPolicies.length === 0) {
      console.log(
        `No data policies found in location ${location} for project ${projectId}.`,
      );
      return;
    }

    console.log('Data Policies:');
    for (const dataPolicy of dataPolicies) {
      console.log(`  Data Policy Name: ${dataPolicy.name}`);
      console.log(`    ID: ${dataPolicy.dataPolicyId}`);
      console.log(`    Type: ${dataPolicy.dataPolicyType}`);
      if (dataPolicy.policyTag) {
        console.log(`    Policy Tag: ${dataPolicy.policyTag}`);
      }
      if (dataPolicy.grantees && dataPolicy.grantees.length > 0) {
        console.log(`    Grantees: ${dataPolicy.grantees.join(', ')}`);
      }
      if (dataPolicy.dataMaskingPolicy) {
        if (dataPolicy.dataMaskingPolicy.predefinedExpression) {
          console.log(
            `    Data Masking Predefined Expression: ${dataPolicy.dataMaskingPolicy.predefinedExpression}`,
          );
        } else if (dataPolicy.dataMaskingPolicy.routine) {
          console.log(
            `    Data Masking Routine: ${dataPolicy.dataMaskingPolicy.routine}`,
          );
        }
      }
    }

    console.log(`Successfully listed ${dataPolicies.length} data policies.`);
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(
        `Error: The project or location '${location}' for project '${projectId}' was not found. ` +
          'Make sure the project ID and location are correct and that the BigQuery Data Policy API is enabled.',
      );
    } else if (err.code === status.PERMISSION_DENIED) {
      console.error(
        `Error: Permission denied when listing data policies for project '${projectId}' in location '${location}'. ` +
          'Make sure the authenticated account has the necessary permissions (For example, bigquery.datapolicies.list).',
      );
    } else {
      console.error(`Error listing data policies: ${err.message}`);
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_datapolicies_v2

client = bigquery_datapolicies_v2.DataPolicyServiceClient()


def list_data_policies(project_id: str, location: str) -> None:
    """Lists all data policies in a specified project.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the data policies (for example, "us", "us-central1").
    """

    parent = f"projects/{project_id}/locations/{location}"

    try:
        request = bigquery_datapolicies_v2.ListDataPoliciesRequest(parent=parent)

        print(
            f"Listing data policies for project '{project_id}' in location '{location}':"
        )
        page_result = client.list_data_policies(request=request)

        found_policies = False
        for data_policy in page_result:
            found_policies = True
            print(f"  Data Policy Name: {data_policy.name}")
            print(f"  Data Policy ID: {data_policy.data_policy_id}")
            print(f"  Data Policy Type: {data_policy.data_policy_type.name}")
            if data_policy.policy_tag:
                print(f"  Policy Tag: {data_policy.policy_tag}")
            if data_policy.grantees:
                print(f"  Grantees: {', '.join(data_policy.grantees)}")
            print("-" * 20)

        if not found_policies:
            print("No data policies found.")

    except google.api_core.exceptions.NotFound as e:
        print(f"Error: The specified project or location was not found or accessible.")
        print(f"Details: {e}")
        print(
            "Make sure the project ID and location are correct and you have the necessary permissions."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
```

### 更新資料政策

更新資料政策的使用者或服務帳戶必須具備 `bigquery.dataPolicies.update` 權限。如要更新與資料政策相關聯的政策標記，您也需要 `datacatalog.taxonomies.get` 權限。

如要更新與資料政策相關聯的主體，您必須具備 `bigquery.dataPolicies.setIamPolicy` 權限。

「BigQuery 資料政策管理員」、「BigQuery 管理員」和「BigQuery 資料擁有者」角色都具備 `bigquery.dataPolicies.update` 和 `bigquery.dataPolicies.setIamPolicy` 權限。「`datacatalog.taxonomies.get`」權限包含在 Data Catalog 管理員和 Data Catalog 檢視者角色中。

### 控制台

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下分類名稱即可開啟。
3. 選取政策標記。
4. 按一下「管理資料政策」。
5. 視需要變更遮蓋規則。
6. 選用：新增或移除主體。
7. 按一下「提交」。

### API

如要變更資料遮蓋規則，請呼叫 [`patch`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/patch?hl=zh-tw) 方法，並傳遞具有更新 `dataMaskingPolicy` 欄位的 [`DataPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies?hl=zh-tw#resource:-datapolicy) 資源。

如要變更與資料政策相關聯的主體，請呼叫 [`setIamPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/setIamPolicy?hl=zh-tw) 方法，並傳遞 [`Policy`](https://docs.cloud.google.com/iam/docs/reference/rest/v1/Policy?hl=zh-tw)，更新獲准存取遮蓋資料的主體。

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const datapolicy = require('@google-cloud/bigquery-datapolicies');
const {DataPolicyServiceClient} = datapolicy.v2;
const protos = datapolicy.protos.google.cloud.bigquery.datapolicies.v2;
const {status} = require('@grpc/grpc-js');

const client = new DataPolicyServiceClient();

/**
 * Updates the data masking configuration of an existing data policy.
 * This example demonstrates how to use a FieldMask to selectively update the
 * `data_masking_policy` (for example, changing the masking expression from
 * ALWAYS_NULL to SHA256) without affecting other fields or recreating the policy.
 *
 * @param {string} projectId The Google Cloud project ID (For example, 'example-project-id').
 * @param {string} location The location of the data policy (For example, 'us').
 * @param {string} dataPolicyId The ID of the data policy to update (For example, 'example-data-policy-id').
 */
async function updateDataPolicy(projectId, location, dataPolicyId) {
  const resourceName = client.dataPolicyPath(projectId, location, dataPolicyId);

  const getRequest = {
    name: resourceName,
  };

  try {
    // To prevent race conditions, use the policy's etag in the update.
    const [currentDataPolicy] = await client.getDataPolicy(getRequest);
    const currentETag = currentDataPolicy.etag;

    // This example transitions a masking rule from ALWAYS_NULL to SHA256.
    const dataPolicy = {
      name: resourceName,
      etag: currentETag,
      dataMaskingPolicy: {
        predefinedExpression:
          protos.DataMaskingPolicy.PredefinedExpression.SHA256,
      },
    };

    // Use a field mask to selectively update only the data masking policy.
    const updateMask = {
      paths: ['data_masking_policy'],
    };

    const request = {
      dataPolicy,
      updateMask,
    };

    const [response] = await client.updateDataPolicy(request);
    console.log(`Successfully updated data policy: ${response.name}`);
    console.log(
      `New masking expression: ${response.dataMaskingPolicy.predefinedExpression}`,
    );
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(
        `Error: Data policy '${resourceName}' not found. ` +
          'Make sure the data policy exists and the project, location, and data policy ID are correct.',
      );
    } else {
      console.error('Error updating data policy:', err.message, err);
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.api_core import exceptions
from google.cloud import bigquery_datapolicies_v2
from google.protobuf import field_mask_pb2

client = bigquery_datapolicies_v2.DataPolicyServiceClient()


def update_data_policy(project_id: str, location: str, data_policy_id: str) -> None:
    """Updates the data masking configuration of an existing data policy.

    This example demonstrates how to use a FieldMask to selectively update the
    `data_masking_policy` (for example, changing the masking expression from
    ALWAYS_NULL to SHA256) without affecting other fields or recreating the policy.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location (for example, "us") of the data policy.
        data_policy_id: The ID of the data policy to update.
    """

    data_policy_name = client.data_policy_path(
        project=project_id,
        location=location,
        data_policy=data_policy_id,
    )

    # To prevent race conditions, use the policy's etag in the update.
    existing_policy = client.get_data_policy(name=data_policy_name)

    # This example transitions a masking rule from ALWAYS_NULL to SHA256.
    updated_data_policy = bigquery_datapolicies_v2.DataPolicy(
        name=data_policy_name,
        data_masking_policy=bigquery_datapolicies_v2.DataMaskingPolicy(
            predefined_expression=bigquery_datapolicies_v2.DataMaskingPolicy.PredefinedExpression.SHA256
        ),
        etag=existing_policy.etag,
    )

    # Use a field mask to selectively update only the data masking policy.
    update_mask = field_mask_pb2.FieldMask(paths=["data_masking_policy"])
    request = bigquery_datapolicies_v2.UpdateDataPolicyRequest(
        data_policy=updated_data_policy,
        update_mask=update_mask,
    )

    try:
        response = client.update_data_policy(request=request)
        print(f"Successfully updated data policy: {response.name}")
        print(f"New data policy type: {response.data_policy_type.name}")
        if response.data_masking_policy:
            print(
                f"New masking expression: {response.data_masking_policy.predefined_expression.name}"
            )
    except exceptions.NotFound:
        print(f"Error: Data policy '{data_policy_name}' not found.")
        print("Make sure the data policy ID and location are correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
```

### 刪除資料政策

建立資料政策的使用者或服務帳戶必須具備 `bigquery.dataPolicies.delete` 權限。BigQuery 資料政策管理員、BigQuery 管理員和 BigQuery 資料擁有者角色都具備此權限。

### 控制台

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下分類名稱即可開啟。
3. 選取政策標記。
4. 按一下「管理資料政策」。
5. 按一下要刪除的資料政策旁的 delete。
6. 按一下「提交」。
7. 按一下「確認」。

### API

如要刪除資料政策，請呼叫 [`delete`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/delete?hl=zh-tw) 方法。

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {DataPolicyServiceClient} =
  require('@google-cloud/bigquery-datapolicies').v2;
const {status} = require('@grpc/grpc-js');

const client = new DataPolicyServiceClient();

/**
 * Deletes a data policy from the BigQuery Data Policy API, which is identified by its project ID, location, and data policy ID.
 *
 * @param {string} projectId The Google Cloud project ID.
 * @param {string} location The Google Cloud location (For example, 'us').
 * @param {string} dataPolicyId The ID of the data policy to delete (For example, 'example-data-policy').
 */
async function deleteDataPolicy(projectId, location, dataPolicyId) {
  const name = client.dataPolicyPath(projectId, location, dataPolicyId);

  const request = {
    name,
  };

  try {
    await client.deleteDataPolicy(request);
    console.log(`Successfully deleted data policy: ${name}`);
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(
        `Data policy ${name} not found. Make sure the data policy ID and location are correct.`,
      );
    } else {
      console.error(`Error deleting data policy ${name}:`, err.message);
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.api_core import exceptions as core_exceptions
from google.cloud import bigquery_datapolicies_v2

client = bigquery_datapolicies_v2.DataPolicyServiceClient()


def delete_data_policy(project_id: str, location: str, data_policy_id: str) -> None:
    """Deletes a data policy from the BigQuery Data Policy APIs.

    Args:
        project_id: The Google Cloud project ID.
        location: The location of the data policy (for example, "us").
        data_policy_id: The ID of the data policy to delete.
    """

    name = client.data_policy_path(
        project=project_id, location=location, data_policy=data_policy_id
    )

    try:
        client.delete_data_policy(name=name)
        print(f"Successfully deleted data policy: {name}")
    except core_exceptions.NotFound:
        print(f"Data policy '{name}' not found. It may have already been deleted.")
    except Exception as e:
        print(f"Error deleting data policy '{name}': {e}")
```

## 對資料欄套用資料政策，遮蓋資料

除了建立政策標記，您也可以建立資料政策，並直接套用至資料欄。

### 使用資料政策

您可以使用 [BigQuery Data Policy API](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest?hl=zh-tw) 建立、更新及刪除資料政策。如要直接在資料欄上套用資料政策，請勿使用 Google Cloud 控制台的「政策標記分類」頁面。

如要使用資料政策，請使用 [`v2.projects.locations.datapolicies`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest?hl=zh-tw#rest-resource:-v2.projects.locations.datapolicies) 資源。

#### 建立資料政策

建立資料政策的使用者或服務帳戶必須具備 `bigquery.dataPolicies.create` 權限。

這項 `bigquery.dataPolicies.create` 權限包含在 BigQuery 資料政策管理員、BigQuery 管理員和 BigQuery 資料擁有者角色中。「`datacatalog.taxonomies.get`」權限包含在 Data Catalog 管理員和 Data Catalog 檢視者角色中。

如果您要建立的資料政策參照[自訂遮蓋常式](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#custom_mask)，則也需要[常式權限](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw#permissions)。

如果您使用自訂遮蓋，請授予使用者 BigQuery 資料擁有者角色，確保他們擁有常式和資料政策的必要權限。

### API

如要建立資料政策，請呼叫 [`create`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/create?hl=zh-tw) 方法。傳遞符合下列條件的[`DataPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies?hl=zh-tw#resource:-datapolicy)資源：

* `dataPolicyType` 欄位設為 `DATA_MASKING_POLICY` 或 `RAW_DATA_ACCESS_POLICY`。
* `dataMaskingPolicy` 欄位會識別要使用的資料遮蓋規則或常式。
* `dataPolicyId` 欄位會提供資料政策的名稱，該名稱在資料政策所屬專案中不得重複。

### SQL

如要建立具有遮蓋存取權的資料政策，請使用 `CREATE DATA_POLICY` 陳述式，並將 `data_policy_type` 的值設為 `DATA_MASKING_POLICY`：

```
    CREATE[ OR REPLACE] DATA_POLICY [IF NOT EXISTS] `myproject.region-us.data_policy_name`
    OPTIONS (
      data_policy_type="DATA_MASKING_POLICY",
      masking_expression="ALWAYS_NULL"
    );
```

如要建立具有原始存取權的資料政策，請使用 `CREATE DATA_POLICY` 陳述式，並將 `data_policy_type` 的值設為 `RAW_DATA_ACCESS_POLICY`：

```
    CREATE[ OR REPLACE] DATA_POLICY [IF NOT EXISTS] `myproject.region-us.data_policy_name`
    OPTIONS (data_policy_type="RAW_DATA_ACCESS_POLICY");
```

如未指定 `data_policy_type` 的值，預設值為 `RAW_DATA_ACCESS_POLICY`。

```
    CREATE[ OR REPLACE] DATA_POLICY [IF NOT EXISTS] myproject.region-us.data_policy_name;
```

* `data_policy_type` 欄位設為 `DATA_MASKING_POLICY` 或 `RAW_DATA_ACCESS_POLICY`。資料政策建立後，您就無法更新這個欄位。
* `masking_expression` 欄位會識別要使用的資料遮蓋規則或常式。

#### 更新資料政策

更新資料政策的使用者或服務帳戶必須具備 `bigquery.dataPolicies.update` 權限。

BigQuery 資料政策管理員、BigQuery 管理員和 BigQuery 資料擁有者角色都具備 `bigquery.dataPolicies.update` 權限。

### API

如要變更資料遮蓋規則，請呼叫 [`patch`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/patch?hl=zh-tw) 方法，並傳遞具有更新 `dataMaskingPolicy` 欄位的 [`DataPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies?hl=zh-tw#resource:-datapolicy) 資源。

### SQL

使用 `ALTER DATA_POLICY` 陳述式更新資料遮蓋規則。例如：

```
    ALTER DATA_POLICY `myproject.region-us.data_policy_name`
    SET OPTIONS (
      data_policy_type="DATA_MASKING_POLICY",
      masking_expression="SHA256"
    );
```

您也可以授予資料政策精細的存取控管權。

授予資料政策精細存取權控管權限，以及管理資料政策的權限不同。如要控管精細的存取控管權限，請更新資料政策的 `grantees` 欄位。如要控管資料政策的存取權，請使用 [`setIamPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/setIamPolicy?hl=zh-tw) 方法設定 IAM 角色。

如要在資料政策中設定受讓人，請使用 [v2 `patch`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/patch?hl=zh-tw)
方法。如要管理資料政策權限，請使用 [v1
`setIamPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v1/projects.locations.dataPolicies/setIamPolicy?hl=zh-tw)
方法。

### API

如要授予資料政策精細的存取控管權，請呼叫 [`patch`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/patch?hl=zh-tw) 方法，然後傳遞更新 `grantees` 欄位的 [`DataPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies?hl=zh-tw#resource:-datapolicy) 資源。

### SQL

如要授予資料政策的精細存取控管權限，請使用 `GRANT FINE_GRAINED_READ` 陳述式新增 `grantees`。例如：

```
    GRANT FINE_GRAINED_READ ON DATA_POLICY `myproject.region-us.data_policy_name`
    TO "principal://goog/subject/user1@example.com","principal://goog/subject/user2@example.com"
```

如要從資料政策撤銷精細存取控管存取權，請使用 `REVOKE FINE_GRAINED_READ` 陳述式移除 `grantees`。例如：

```
    REVOKE FINE_GRAINED_READ ON DATA_POLICY `myproject.region-us.data_policy_name`
    FROM "principal://goog/subject/user1@example.com","principal://goog/subject/user2@example.com"
```

#### 刪除資料政策

建立資料政策的使用者或服務帳戶必須具備 `bigquery.dataPolicies.delete` 權限。BigQuery 資料政策管理員、BigQuery 管理員和 BigQuery 資料擁有者角色都具備此權限。

### API

如要刪除資料政策，請呼叫 [`delete`](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/delete?hl=zh-tw) 方法。

### SQL

使用 `DROP DATA_POLICY` 陳述式刪除資料政策：

```
    DROP DATA_POLICY `myproject.region-us.data_policy_name`;
```

### 直接在資料欄上指派資料政策

您可以直接在資料欄上指派資料政策，不必使用政策標記。

#### 事前準備

如要取得直接在資料欄上指派資料政策所需的權限，請要求管理員授予您資料表的「BigQuery 資料政策管理員」 (`roles/bigquerydatapolicy.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備直接在資料欄上指派資料政策所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要直接在資料欄上指派資料政策，必須具備下列權限：

* `bigquery.tables.update`
* `bigquery.tables.setColumnDataPolicy`
* `bigquery.dataPolicies.attach`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

#### 指派資料政策

如要直接在資料欄上指派資料政策，請採取下列任一做法：

### SQL

如要將資料政策附加至資料欄，請使用 [`CREATE
TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)、[`ALTER TABLE ADD
COLUMN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_add_column_statement) 或 [`ALTER COLUMN SET
OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_column_set_options_statement) DDL 陳述式。

以下範例使用 `CREATE TABLE` 陳述式，並在資料欄中設定資料政策：

```
    CREATE TABLE myproject.table1 (
    name INT64 OPTIONS (data_policies=["{'name':'myproject.region-us.data_policy_name1'}",
                                      "{'name':'myproject.region-us.data_policy_name2'}"])
    );
```

以下範例使用 `ALTER COLUMN SET OPTIONS`，在資料表的現有資料欄中新增資料政策：

```
ALTER TABLE myproject.table1
ALTER COLUMN column_name SET OPTIONS (
  data_policies += ["{'name':'myproject.region-us.data_policy_name1'}",
                    "{'name':'myproject.region-us.data_policy_name2'}"]);
```

### API

如要將資料政策指派給資料欄，請對資料表呼叫 [`patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法，並使用適用的資料政策更新資料表結構定義。

### 取消指派資料政策

如要直接在資料欄中取消指派資料政策，請採取下列任一做法：

### SQL

如要將資料政策從資料欄中分離，請使用 [`ALTER COLUMN SET
OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_column_set_options_statement) DDL 陳述式。

以下範例使用 `ALTER COLUMN SET OPTIONS`，從資料表的現有資料欄中移除所有資料政策：

```
ALTER TABLE myproject.table1
ALTER COLUMN column_name SET OPTIONS (
  data_policies = []);
```

下列範例使用 `ALTER COLUMN SET OPTIONS`，替換資料表中現有資料欄的資料政策：

```
ALTER TABLE
```