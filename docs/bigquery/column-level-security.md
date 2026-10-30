Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用資料欄層級存取控管機制限制存取權

本頁說明如何使用 BigQuery 資料欄層級存取控管機制，限制存取資料欄層級的 BigQuery 資料。如需資料欄層級存取控管的一般資訊，請參閱「[BigQuery 資料欄層級存取控管簡介](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)」。

本頁的操作說明會同時使用 BigQuery 和 Data Catalog。

您必須更新資料表結構定義，才能為資料欄設定政策標記。您可以使用 Google Cloud 控制台、bq 指令列工具和 BigQuery API，在資料欄設定政策標記。此外，您也可以使用下列技術，在單一作業中建立資料表、指定結構定義和政策標記：

* bq 指令列工具的 `bq mk` 和 `bq load` 指令。
* `tables.insert` API 方法。
* Google Cloud 控制台中的「Create table」(建立資料表) 頁面。如果使用Google Cloud 控制台，則必須在新增或編輯結構定義時，選取「Edit as text」(以文字形式編輯)。

**注意：** 您無法使用 DDL `CREATE TABLE` 陳述式指定政策標記。

如要強化資料欄層級存取控管，您可以選擇使用[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。資料遮蓋功能可讓您遮蓋機密資料，方法是以空值、預設值或雜湊內容取代資料欄的實際值。

## 事前準備

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

**注意：** 您必須保持啟用 `datacatalog.googleapis.com` API，才能建立及管理用於資料遮蓋和資料欄層級安全性的 Data Catalog 政策標記和分類。雖然 Data Catalog 的中繼資料搜尋和目錄功能已淘汰，並轉換至 Knowledge Catalog，但政策標記專用的 Data Catalog API 功能並未淘汰。

## 角色和權限

使用者和服務帳戶有多種與政策標記相關的角色。

* 管理政策標記的使用者或服務帳戶，必須具備 Data Catalog 政策標記管理員角色。政策標記管理員角色可以管理分類和政策標記，以及授予或移除與政策標記相關聯的 IAM 角色。
* 使用者或服務帳戶如要[強制執行資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#enforce_access_control)，必須具備 BigQuery 管理員角色或 BigQuery 資料擁有者角色。BigQuery 角色可以管理資料政策，用於強制執行分類的存取控管。
* 如要在Google Cloud 控制台中查看組織內所有專案的分類和政策標記，使用者必須具備組織檢視者角色。否則，控制台只會顯示與所選專案相關聯的分類和政策標記。
* 使用者或服務帳戶如要查詢受資料欄層級存取控管機制保護的資料，必須具備 Data Catalog 精細讀取者角色，才能存取該資料。

如要進一步瞭解所有政策標記相關角色，請參閱「[與資料欄層級存取控管搭配使用的角色](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw#roles)」。

### Data Catalog 政策標記管理員角色

Data Catalog 政策標記管理員角色可以建立及管理資料政策標記。

如要授予政策標記管理員角色，您必須具備要授予角色的專案 `resourcemanager.projects.setIamPolicy` 權限。如果您沒有 `resourcemanager.projects.setIamPolicy` 權限，請要求專案擁有者授予權限，或為您執行下列步驟。

1. 前往 Google Cloud 控制台的「IAM」頁面。

   [前往「IAM」](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
2. 如果清單中包含要授予角色的使用者電子郵件地址，請選取該電子郵件地址，然後按一下 edit「Edit」(編輯)。「Edit access」(編輯權限) 窗格隨即開啟。按一下「Add another role」(新增其他角色)。

   如果清單中沒有使用者電子郵件地址，請按一下 person\_add「Add」(新增)，然後在「New principals」(新增主體) 方塊中輸入電子郵件地址。
3. 按一下「Select a role」(選取角色) 下拉式選單。
4. 在「依產品或服務」中，按一下「Data Catalog」。在「Roles」(角色) 中，按一下「Policy Tag Admin」(政策標記管理員)。
5. 按一下 [儲存]。

### BigQuery 資料政策管理員、BigQuery 管理員和 BigQuery 資料擁有者角色

BigQuery 資料政策管理員、BigQuery 管理員和 BigQuery 資料擁有者角色可以管理資料政策。

如要授予上述任一角色，您必須具備要授予角色的專案 `resourcemanager.projects.setIamPolicy` 權限。如果您沒有 `resourcemanager.projects.setIamPolicy` 權限，請要求專案擁有者授予權限，或為您執行下列步驟。

1. 前往 Google Cloud 控制台的「IAM」頁面。

   [前往「IAM」頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
2. 如果清單中列出要授予角色的使用者電子郵件地址，請選取該電子郵件地址，然後按一下 edit「Edit」(編輯)。然後點選「新增其他角色」。

   如果清單中沒有使用者電子郵件地址，請按一下 person\_add「Add」(新增)，然後在「New principals」(新增主體) 方塊中輸入電子郵件地址。
3. 按一下「Select a role」(選取角色) 下拉式清單。
4. 依序點選「BigQuery」>「BigQuery 資料政策管理員」或「BigQuery 管理員」或「BigQuery 資料擁有者」。
5. 按一下 [儲存]。

### 組織檢視者角色

「組織檢視者」角色可讓使用者查看組織資源的詳細資料。如要授予這個角色，您必須具備組織的 `resourcemanager.organizations.setIamPolicy` 權限。

### Data Catalog 精細讀取者角色

如要存取受資料欄層級存取控管機制保護的資料，使用者必須具備 Data Catalog 精細讀取者角色，或任何其他已授予 [`datacatalog.categories.fineGrainedGet` 權限](https://docs.cloud.google.com/iam/docs/roles-permissions/datacatalog?hl=zh-tw#datacatalog.categories.fineGrainedGet)的角色。設定政策標記時，系統會將這個角色指派給主體。

如要為使用者授予政策標記的「精細讀取者」角色，您必須具備專案的 `datacatalog.taxonomies.setIamPolicy` 權限，且該專案含有政策標記的分類。如果您沒有 `datacatalog.taxonomies.setIamPolicy` 權限，請要求專案擁有者授予權限，或代為執行操作。

如需操作說明，請參閱「[設定政策標記的權限](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_permissions_on_policy_tags)」。

## 設定資料欄層級存取控管

完成下列工作，設定資料欄層級存取控管機制：

* 建立政策標記分類。
* 將主體與政策標記建立關聯，並授予主體 Data Catalog 精細讀取者角色。
* 將政策標記與 BigQuery 資料表資料欄建立關聯。
* 對含有政策標記的分類強制執行存取控管。

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
   8. 視分類需求，繼續新增政策標記和子政策標記。
   9. 為階層建立政策標記後，按一下「Create」(建立)。

### API

如要使用現有的分類，請呼叫 [`taxonomies.import`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies/import?hl=zh-tw)，取代下列程序的前兩個步驟。

1. 呼叫 [`taxonomies.create`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies/create?hl=zh-tw) 建立分類。
2. 呼叫 [`taxonomies.policyTags.create`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies.policyTags/create?hl=zh-tw) 建立政策標記。

### 設定政策標記的權限

建立分類的使用者或服務帳戶，必須具備 Data Catalog 政策標記管理員角色。

### 控制台

1. 前往 Google Cloud 控制台的「Policy tag taxonomies」(政策標記分類) 頁面。

   [前往「Policy tag taxonomies」(政策標記分類)](https://console.cloud.google.com/bigquery/security/secure/policy-tags?hl=zh-tw)
2. 按一下包含相關政策標記的分類名稱。
3. 選取一或多個政策標記。
4. 如果「資訊面板」處於隱藏狀態，請按一下「顯示資訊面板」。
5. 在「Info panel」(資訊面板) 中，您可以查看所選政策標記的角色和主體。為建立及管理政策標記的帳戶新增「Policy Tags Admin」(政策標記管理員) 角色。將「Fine-Grained Reader」(精細讀取者) 角色新增至應可存取受資料欄層級存取控管保護資料的帳戶。您也可以使用這個面板，從帳戶中移除角色或修改其他權限。
6. 按一下 [儲存]。

### API

呼叫 [`taxonomies.policytag.setIamPolicy`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies.policyTags/setIamPolicy?hl=zh-tw)，將主體指派給適當的角色，藉此授予政策標記的存取權。

### 在資料欄上設定政策標記

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

#### 其他為資料欄設定政策標記的方法

您也可以在下列情況設定政策標記：

* 使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 建立資料表。傳入用於建立資料表的結構定義。
* 使用 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 將資料載入資料表。載入資料表時，請傳入要使用的結構定義。

如需一般結構定義資訊，請參閱「[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)」。

### 強制執行存取控管

請按照下列操作說明，開啟或關閉存取控管強制執行功能。

如要強制執行存取控管，必須建立資料政策。如果您使用Google Cloud 控制台強制執行存取控管，系統會為您執行這項操作。如要使用 BigQuery Data Policy API 強制執行存取控管，則必須明確建立資料政策。

強制執行存取控管的主體必須具備 BigQuery 管理員角色或 BigQuery 資料擁有者角色。主體也必須具備 Data Catalog 管理員角色或 Data Catalog 檢視者角色。

如要停止強制執行存取控管，請按一下「Enforce access control」(強制執行存取控管) 切換控制項。

如果資料政策與分類中的任何政策標記相關聯，您必須先刪除分類中的所有資料政策，才能停止強制執行存取控管。如果使用 BigQuery Data Policy API 刪除資料政策，則必須刪除 `dataPolicyType` 為 `DATA_MASKING_POLICY` 的所有資料政策。詳情請參閱「[刪除資料政策](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw#delete_data_policies)」。

#### 建立資料政策

請按照下列步驟建立資料政策：

### 控制台

如要強制執行存取控管，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Policy tag taxonomies」(政策標記分類) 頁面。

   [前往「Policy tag taxonomies」(政策標記分類) 頁面](https://console.cloud.google.com/bigquery/security/secure/policy-tags?hl=zh-tw)
2. 按一下要強制執行資料欄層級存取控管的分類。
3. 如果尚未啟用「Enforce access control」(強制執行存取控管)，請按一下「Enforce access control」(強制執行存取控管) 啟用。

### API

使用 [`create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies/create?hl=zh-tw)，並傳入 `dataPolicyType` 欄位設為 `COLUMN_LEVEL_SECURITY_POLICY` 的 [`DataPolicy` 資源](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies?hl=zh-tw#resource:-datapolicy)。

#### 取得資料政策

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

#### 取得資料政策的身分與存取權管理 (IAM) 政策

如要取得資料政策的 IAM 政策，請按照下列步驟操作：

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

    try (DataPolicyServiceClient client = DataPolicyServiceClient.create()) {
      Policy policy = client.getIamPolicy(request);

      System.out.printf("Successfully retrieved IAM policy for data policy: %s%n", resourceName);
      System.out.printf("Policy Version: %d%n", policy.getVersion());
      if (policy.getBindingsCount() > 0) {
        System.out.println("Policy Bindings:");
        for (Binding binding : policy.getBindingsList()) {
          System.out.printf("  Role: %s%n", binding.getRole());
          System.out.printf("  Members: %s%n", String.join(", ", binding.getMembersList()));
          if (binding.hasCondition() && !binding.getCondition().getExpression().isEmpty()) {
            System.out.printf("  Condition: %s%n", binding.getCondition().getExpression());
          }
        }
      } else {
        System.out.println("No bindings found in the policy.");
      }
    } catch (NotFoundException err) {
      System.err.printf("error: data policy '%s' not found: %s%n", resourceName, err.getMessage());
    } catch (ApiException | IOException err) {
      System.err.printf(
          "error: failed to get IAM policy for data policy '%s': %s%n",
          resourceName, err.getMessage());
    }
  }
```

#### 列出資料政策

請按照下列步驟列出資料政策：

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.api.gax.rpc.NotFoundException;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicy;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicyServiceClient;
import com.google.cloud.bigquery.datapolicies.v2.DataPolicyServiceClient.ListDataPoliciesPagedResponse;
import com.google.cloud.bigquery.datapolicies.v2.ListDataPoliciesRequest;
import com.google.cloud.bigquery.datapolicies.v2.LocationName;
import java.io.IOException;

public class ListDataPolicies {

  /**
   * Lists all data policies in a specified project and location.
   *
   * @param projectId The Google Cloud project ID (for example, "example-project-id").
   * @param location The geographic location of the data policies (for example, "us-central1").
   */
  public static void listDataPolicies(String projectId, String location) {
    LocationName parent = LocationName.of(projectId, location);

    ListDataPoliciesRequest request =
        ListDataPoliciesRequest.newBuilder().setParent(parent.toString()).build();

    try (DataPolicyServiceClient client =
```