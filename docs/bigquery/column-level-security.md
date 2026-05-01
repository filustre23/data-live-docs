* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過資料欄層級存取控管機制限制存取權

本頁說明如何使用 BigQuery 資料欄層級存取權控管機制，限制存取資料欄層級的 BigQuery 資料。如需資料欄層級存取權控管的一般資訊，請參閱「[BigQuery 資料欄層級存取權控管簡介](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)」。

本頁的說明會同時使用 BigQuery 和 Data Catalog。

您必須更新資料表結構定義，才能為資料欄設定政策標記。您可以使用 Google Cloud 控制台、bq 指令列工具和 BigQuery API，為資料欄設定政策標記。此外，您也可以使用下列技術，在單一作業中建立資料表、指定結構定義及指定政策標記：

* bq 指令列工具的 `bq mk` 和 `bq load` 指令。
* `tables.insert` API 方法。
* Google Cloud 控制台中的「建立資料表」頁面。如果您使用Google Cloud 控制台，新增或編輯結構定義時，必須選取「以文字形式編輯」。

**注意：** 您無法使用 DDL `CREATE TABLE` 陳述式指定政策標記。

如要強化資料欄層級的存取控管，您可以選擇使用[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。
資料遮蓋功能可將資料欄的實際值替換為空值、預設值或雜湊內容，藉此遮蓋機密資料。

## 事前準備

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

## 角色和權限

使用者和服務帳戶有多種與政策代碼相關的角色。

* 管理政策代碼的使用者或服務帳戶必須具備 Data Catalog 政策代碼管理員角色。政策標記管理員角色可以管理分類和政策標記，以及授予或移除與政策標記相關聯的 IAM 角色。
* 如要[強制執行存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#enforce_access_control)，使用者或服務帳戶必須具備 BigQuery 管理員或 BigQuery 資料擁有者角色，才能進行資料欄層級的存取控管。BigQuery 角色可以管理資料政策，這些政策用於對分類強制執行存取權控管。
* 如要在Google Cloud 控制台中查看機構內所有專案的分類和政策標記，使用者必須具備機構檢視者角色。否則，控制台只會顯示與所選專案相關聯的分類和政策標籤。
* 如要查詢受欄級存取控管保護的資料，使用者或服務帳戶必須具備 Data Catalog Fine-Grained Reader 角色，才能存取該資料。

如要進一步瞭解所有與政策標記相關的角色，請參閱「[搭配資料欄層級存取控管使用的角色](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw#roles)」一文。

### Data Catalog 政策代碼管理員角色

具備 Data Catalog 政策標記管理員角色的使用者可以建立及管理資料政策標記。

如要授予政策標記管理員角色，您必須具備要授予角色的專案 `resourcemanager.projects.setIamPolicy` 權限。如果您沒有 `resourcemanager.projects.setIamPolicy` 權限，請要求專案擁有者授予您權限，或為您執行下列步驟。

1. 前往 Google Cloud 控制台的「IAM」頁面。

   [開啟「IAM」頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
2. 如果清單中列出要授予角色的使用者電子郵件地址，請選取該電子郵件地址，然後按一下「編輯」edit。「編輯權限」窗格隨即開啟。按一下「新增其他角色」。

   如果清單中沒有使用者電子郵件地址，請按一下「新增」person\_add，然後在「New principals」(新的主體) 方塊中輸入電子郵件地址。
3. 按一下「選取角色」下拉式清單。
4. 在「依產品或服務」中，按一下「Data Catalog」。在「角色」中，按一下「政策標記管理員」。
5. 按一下 [儲存]。

### BigQuery 資料政策管理員、BigQuery 管理員和 BigQuery 資料擁有者角色

BigQuery 資料政策管理員、BigQuery 管理員和 BigQuery 資料擁有者角色可以管理資料政策。

如要授予這兩個角色，您必須具備要授予角色的專案的 `resourcemanager.projects.setIamPolicy` 權限。如果您沒有 `resourcemanager.projects.setIamPolicy` 權限，請要求專案擁有者授予您權限，或為您執行下列步驟。

1. 前往 Google Cloud 控制台的「IAM」頁面。

   [開啟「IAM」頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
2. 如果清單中列出要授予角色的使用者電子郵件地址，請選取該電子郵件地址，然後按一下「編輯」edit。然後按一下「新增其他角色」。

   如果清單中沒有使用者電子郵件地址，請按一下「新增」person\_add，然後在「New principals」(新的主體) 方塊中輸入電子郵件地址。
3. 按一下「選取角色」下拉式清單。
4. 按一下「BigQuery」，然後按一下「BigQuery 資料政策管理員」、「BigQuery 管理員」或「BigQuery 資料擁有者」。
5. 按一下 [儲存]。

### 機構檢視者角色

使用者可透過機構檢視者角色，查看機構資源的詳細資料。如要授予這個角色，您必須具備機構的 `resourcemanager.organizations.setIamPolicy` 權限。

### Data Catalog 精細讀取者角色

如要存取受資料欄層級存取控管機制保護的資料，使用者必須具備 Data Catalog 精細讀取者角色，或是任何獲授 [`datacatalog.categories.fineGrainedGet` 權限](https://docs.cloud.google.com/iam/docs/roles-permissions/datacatalog?hl=zh-tw#datacatalog.categories.fineGrainedGet)的其他角色。設定政策標記時，系統會將這個角色指派給主體。

如要授予使用者政策標記的精細讀取者角色，您必須具備含有該政策標記分類的專案 `datacatalog.taxonomies.setIamPolicy` 權限。如果您沒有 `datacatalog.taxonomies.setIamPolicy` 權限，請專案擁有者授予您權限，或代您執行這項操作。

如需操作說明，請參閱「[設定政策標記的權限](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_permissions_on_policy_tags)」。

## 設定資料欄層級存取控管

如要設定資料欄層級存取權控管，請完成下列工作：

* 建立政策標記分類。
* 將主體與政策標記建立關聯，並授予主體「Data Catalog 精細讀取者」角色。
* 將政策標記與 BigQuery 資料表欄建立關聯。
* 對含有政策標記的分類強制執行存取控管。

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
   8. 視需要繼續為分類新增政策標記和子項政策標記。
   9. 為階層建立完政策標記後，請按一下「建立」。

### API

如要使用現有分類，請呼叫
[`taxonomies.import`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies/import?hl=zh-tw)
，取代下列程序的前兩個步驟。

1. 呼叫 [`taxonomies.create`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies/create?hl=zh-tw) 建立分類。
2. 呼叫 [`taxonomies.policytag.create`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies.policyTags/create?hl=zh-tw) 建立政策標記。

### 設定政策標記的權限

建立分類架構的使用者或服務帳戶必須獲派 Data Catalog 政策代碼管理員角色。

### 控制台

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下包含相關政策標記的分類名稱。
3. 選取一或多個政策標記。
4. 如果**資訊面板**已隱藏，請按一下「顯示資訊面板」。
5. 在「資訊面板」中，您可以查看所選政策標記的角色和主體。為建立及管理政策標記的帳戶新增「政策標記管理員」角色。將「精細讀取者」角色新增至要存取受資料欄層級存取控管機制保護資料的帳戶。您也可以使用這個面板從帳戶移除角色，或修改其他權限。
6. 按一下 [儲存]。

### API

呼叫
[`taxonomies.policytag.setIamPolicy`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies.policyTags/setIamPolicy?hl=zh-tw)
，將主體指派給適當的角色，授予政策標記的存取權。

### 在資料欄上設定政策標記

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

#### 在資料欄上設定政策標記的其他方式

您也可以在下列情況設定政策標記：

* 使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 建立資料表。傳遞要用於建立資料表的結構定義。
* 使用 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 將資料載入資料表。載入資料表時，傳入要使用的結構定義。

如需一般結構定義資訊，請參閱「[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)」。

### 強制執行存取控管

請按照這些操作說明開啟或關閉存取控管的強制執行功能。

如要強制執行存取控管，必須建立資料政策。如果您使用Google Cloud 控制台強制執行存取控管，系統會代為完成這項作業。如要使用 BigQuery Data Policy API 強制執行存取權控管，您必須明確建立資料政策。

強制執行存取控管的主體必須具備 BigQuery 管理員角色或 BigQuery 資料擁有者角色。主體也必須具備 Data Catalog 管理員角色或 Data Catalog 檢視者角色。

如要停止強制執行存取控管 (如果已啟用)，請點選「強制執行存取控管」切換控制項。

如果分類中的任何政策標記有相關聯的資料政策，您必須先刪除分類中的所有資料政策，才能停止強制執行存取控管。如果您使用 BigQuery Data Policy API 刪除資料政策，則必須刪除所有具有 `dataPolicyType` 的資料政策。`DATA_MASKING_POLICY`詳情請參閱「[刪除資料政策](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw#delete_data_policies)」。

#### 建立資料政策

如要建立資料政策，請按照下列步驟操作：

### 控制台

如要強制執行存取控管，請按照下列步驟操作：

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下要強制執行資料欄層級存取控管的分類。
3. 如果「強制執行存取控管」尚未開啟，請點選「強制執行存取控管」來啟用。

### API

使用 [`create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/create?hl=zh-tw)，並傳入 [`DataPolicy` 資源](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies?hl=zh-tw#resource:-datapolicy)，其中 `dataPolicyType` 欄位設為 `COLUMN_LEVEL_SECURITY_POLICY`。

#### 取得資料政策

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

#### 取得資料政策的身分與存取權管理 (IAM) 政策

如要取得資料政策的 IAM 政策，請按照下列步驟操作：

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

#### 列出資料政策

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

#### 刪除資料政策

如要刪除資料政策，請按照下列步驟操作：

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

## 使用政策標記

本節說明如何查看、修改及刪除政策代碼。

### 查看政策標記

如要查看您為分類建立的政策標記，請按照下列步驟操作：

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下要查看政策標記的分類。「分類」頁面會顯示分類中的政策標記。

### 在結構定義中查看政策標記

檢查資料表結構定義時，您可以查看套用至資料表的政策標記。您可以使用 Google Cloud 控制台、bq 指令列工具、BigQuery API 和用戶端程式庫查看結構定義。如要瞭解如何查看結構定義，請參閱「[取得資料表資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_information_about_tables)」。

### 查看政策標記的權限

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下包含相關政策標記的分類名稱。
3. 選取一或多個政策標記。
4. 如果**資訊面板**已隱藏，請按一下「顯示資訊面板」。
5. 在「資訊面板」中，您可以查看所選政策標記的角色和主體。

### 更新政策標記的權限

建立分類架構的使用者或服務帳戶必須獲派 Data Catalog 政策代碼管理員角色。

### 控制台

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下包含相關政策標記的分類名稱。
3. 選取一或多個政策標記。
4. 如果**資訊面板**已隱藏，請按一下「顯示資訊面板」。
5. 在「資訊面板」中，您可以查看所選政策標記的角色和主體。為建立及管理政策標記的帳戶新增「政策標記管理員」角色。將「精細讀取者」角色新增至要存取受資料欄層級存取控管機制保護資料的帳戶。您也可以使用這個面板從帳戶移除角色，或修改其他權限。
6. 按一下 [儲存]。

### API

呼叫
[`taxonomies.policytag.setIamPolicy`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies.policyTags/setIamPolicy?hl=zh-tw)
，將主體指派給適當的角色，授予政策標記的存取權。

### 擷取政策標記資源名稱

將政策標記套用至資料欄時，您需要政策標記資源名稱。

如要擷取政策標記資源名稱，請按照下列步驟操作：

1. [查看政策標記](#view_policy_tags)，瞭解含有政策標記的分類。
2. 找出要複製資源名稱的政策標記。
3. 按一下「複製政策標記資源名稱」圖示。

### 清除政策標記

更新資料表結構定義，從資料欄清除政策標記。您可以使用Google Cloud console、bq 指令列工具和 BigQuery API 方法，從資料欄中清除政策標記。

### 控制台

在「Current schema」(目前結構定義) 頁面的「Policy tags」(政策標記) 下方，按一下「X」。

### bq

**注意：** 如要清除政策標記，您必須將 `policyTags` 的 `names` 欄位明確設為空白清單 `[]`。刪除 `policyTags` 欄位不會影響現有的政策標記。這是為了防止誤刪政策標記，導致敏感資料外洩。

1. 擷取結構定義並儲存至本機檔案。

   ```
   bq show --schema --format=prettyjson \
      project-id:dataset.table > schema.json
   ```

   其中：

   * project-id 是您的專案 ID。
   * dataset 是含有您要更新資料表的資料集名稱。
   * table 是您要更新之資料表的名稱。
2. 修改 schema.json，從資料欄中清除政策標記。

   ```
   [
    ...
    {
      "name": "ssn",
      "type": "STRING",
      "mode": "REQUIRED",
      "policyTags": {
        "names": []
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

**注意：** 如要清除政策標記，您必須將 `policyTags` 的 `names` 欄位明確設為空白清單 `[]`。刪除 `policyTags` 欄位不會影響現有的政策標記。這是為了防止誤刪政策標記，導致敏感資料外洩。

呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 並使用 `schema` 屬性，清除結構定義中的政策標記。如要瞭解如何清除政策標記，請參閱指令列範例結構定義。

由於 `tables.update` 方法會取代整個資料表資源，因此建議使用 `tables.patch` 方法。

### 刪除政策標記

您可以刪除分類中的一或多個政策標記，也可以刪除分類和其中包含的所有政策標記。刪除政策標記後，系統會自動移除政策標記與套用該標記的任何資料欄之間的關聯。

如果刪除的政策標記有相關聯的[資料政策](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)，系統最多可能需要 30 分鐘才能刪除該資料政策。如要立即刪除資料政策，可以直接[刪除](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw#delete_data_policies)。

如要刪除分類中的一或多個政策標記，請按照下列步驟操作：

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下含有要刪除標記的分類名稱。
3. 按一下 [編輯]。
4. 按一下要刪除的政策標記旁的 delete。
5. 按一下 [儲存]。
6. 按一下「確認」。

如要刪除整個分類，請按照下列步驟操作：

1. 在Google Cloud 控制台中開啟「Policy tag taxonomies」(政策標記分類) 頁面。

   [開啟「政策標記分類」頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)
2. 按一下含有要刪除標記的分類名稱。
3. 按一下「刪除政策標記分類」。
4. 輸入分類名稱，然後按一下「刪除」。

## 使用資料欄層級存取控管機制查詢資料

如果使用者有資料集存取權，且具備 Data Catalog 細部讀取者角色，即可存取欄資料。使用者照常執行查詢。

如果使用者有資料集存取權，但沒有 Data Catalog 細部讀取者角色，就無法存取資料欄資料。如果這類使用者執行 `SELECT *`，系統會顯示錯誤訊息，列出使用者無法存取的資料欄。如要解決這項錯誤，請採取下列任一做法：

* 修改查詢，排除使用者無法存取的資料欄。舉例來說，如果使用者無法存取「`ssn`」欄，但可以存取其餘欄，則可執行下列查詢：

  ```
  SELECT * EXCEPT (ssn) FROM ...
  ```

  在上述範例中，`EXCEPT` 子句會排除 `ssn` 資料欄。
* 請 Data Catalog 管理員將使用者新增為相關資料類別的 Data Catalog 精細讀取者。錯誤訊息會提供使用者需要存取權的政策標記完整名稱。

## 常見問題

### BigQuery 資料欄層級安全防護機制是否適用於檢視區塊？

可以。檢視表衍生自基礎資料表。透過檢視畫面存取受保護的資料欄時，系統會套用資料表上相同的資料欄層級存取權控管。

BigQuery 中有兩種檢視表：邏輯檢視表和授權檢視表。這兩種檢視畫面都是從來源資料表衍生而來，且都與資料表的資料欄層級存取控管機制一致。

詳情請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

### 資料欄層級存取控管機制是否適用於 `STRUCT` 或 `RECORD` 資料欄？

可以。您只能將政策標記套用至葉節點欄位，且只有這些欄位會受到保護。

### 我可以同時使用舊版 SQL 和 GoogleSQL 嗎？

您可以使用 GoogleSQL 查詢受欄層級存取控管保護的資料表。

如果目標資料表有任何政策標記，系統會拒絕所有舊版 SQL 查詢。

### 查詢會記錄在 Cloud Logging 中嗎？

政策標記檢查結果會記錄在 Logging 中。如要瞭解欄層級存取控管的稽核記錄，請參閱[這篇文章](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw#audit_logging)。

### 複製資料表時，是否會受到資料欄層級存取控管機制影響？

可以。如果沒有存取權，就無法複製欄。

下列作業會驗證資料欄層級權限。

* `SELECT` 查詢 (含目的地資料表)
* [資料表複製工作](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)
* [資料擷取工作](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw) (例如擷取至 Cloud Storage)

### 將資料複製到新表格時，系統會自動傳播政策標記嗎？

在大多數情況下，不會。如果您將查詢結果複製到新資料表，系統不會自動為新資料表指派政策標記。因此新資料表沒有資料欄層級存取控管機制。如果您將資料匯出至 Cloud Storage，也適用相同規定。

但如果您使用[資料表複製工作](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)，則不在此限。由於資料表複製作業不會套用任何資料轉換，因此政策標記會自動傳播至目標資料表。這項例外狀況不適用於跨區域資料表複製工作，因為這類工作不支援複製政策標記。

### 資料欄層級存取控管機制是否與虛擬私有雲相容？

可以，資料欄層級存取控管機制和 VPC 可相容並互補。

虛擬私有雲會運用 IAM 控制服務存取權，例如 BigQuery 和 Cloud Storage。資料欄層級的存取權控管機制可提供 BigQuery 內個別資料欄的精細安全防護。

如要針對政策標記和資料政策強制執行 VPC，以進行資料欄層級存取控管和動態資料遮蓋，您必須在範圍內限制下列 API：

* [Data Catalog API](https://docs.cloud.google.com/data-catalog/docs/reference/rest?hl=zh-tw)
* [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw)
* [BigQuery Data Policy API](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest?hl=zh-tw)

## 疑難排解

### 我無法查看 Data Catalog 角色

如果看不到 Data Catalog 細部讀取者等角色，可能是因為您尚未在專案中啟用 Data Catalog API。如要瞭解如何啟用 Data Catalog API，請參閱「[開始前](#before_you_begin)」一節。啟用 Data Catalog API 後，Data Catalog 角色應會在幾分鐘內顯示。

### 我無法查看「分類」頁面

您需要額外權限，才能查看「分類」頁面。舉例來說，Data Catalog [政策標記管理員](#policy_tags_admin)角色可存取「分類」頁面。

### 我強制執行政策標記，但似乎沒有作用

如果帳戶不應有存取權，但您仍收到該帳戶的查詢結果，可能是因為該帳戶收到快取結果。具體來說，如果您先前已成功執行查詢，然後強制執行政策標記，您可能會從[查詢結果快取](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)取得結果。根據預設，查詢結果會快取 24 小時。如果您[停用結果快取](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw#disabling_retrieval_of_cached_results)，查詢應會立即失敗。如要進一步瞭解快取，請參閱「[欄級存取控管的影響](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw#security)」。

一般來說，IAM 更新作業大約需要 30 秒才能完成。
政策標記階層的變更最多可能需要 30 分鐘才會生效。

### 我沒有權限從設有資料欄層級安全防護機制的資料表讀取資料

您需要[精細讀取者角色](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#fine_grained_reader)或[遮蓋讀取者角色](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#roles_for_querying_masked_data)，才能在不同層級 (例如機構、資料夾、專案和政策標記) 執行這項操作。「精細讀取者」角色可授予原始資料存取權，「經過遮蓋的讀取者」角色則可授予[遮蓋資料](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)存取權。您可以使用 [IAM 疑難排解工具](https://docs.cloud.google.com/policy-intelligence/docs/troubleshoot-access?hl=zh-tw)，在專案層級檢查這項權限。

### 我在政策標記分類中設定了精細的存取權控管，但使用者仍可查看受保護的資料

如要排解這個問題，請確認下列詳細資料：

* 在「政策標記分類」[頁面](https://console.cloud.google.com/bigquery/policy-tags?hl=zh-tw)，確認「強制執行存取控管」切換鈕處於「開啟」位置。
* 確認查詢未使用[快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)。
  如果您使用 `bq` 指令列介面工具測試查詢，則應使用 `--nouse_cache flag` 停用查詢快取。例如：

  ```
  bq query --nouse_cache --use_legacy_sql=false "SELECT * EXCEPT (customer_pii) FROM my_table;"
  ```

### 專案遷移注意事項

政策標記和分類位於特定 Google Cloud 機構
內，專案遷移至新機構時，不會自動重新建立關聯。如果將使用政策標記控管資料欄層級存取權的專案遷移至其他機構，會發生下列問題：

* 遷移的專案中，您將無法再透過 Google Cloud 控制台使用者介面
  管理政策標記。
* 您無法在遷移後的專案中，將這些政策標記套用至新資料欄。
* 現有的資料欄層級存取權控管機制可能仍會顯示為有效，但為了管理目的，系統會中斷與原始機構中來源分類的連結。

如要解決這個問題， Google Cloud 支援團隊
必須手動介入，將分類與新機構重新建立關聯。如果您已遷移含有政策代碼的專案，並遇到這些問題，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/support?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]