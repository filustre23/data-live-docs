Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用組織政策，對 BigQuery 資源套用自訂限制

**預覽
— 資料表、資料存取權政策、資料列存取政策和常式的限制**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

本頁面說明如何使用「組織政策服務」自訂限制條件，限制對下列 Google Cloud 資源執行的特定作業：

* `bigquery.googleapis.com/Dataset`
* `bigquery.googleapis.com/Routine`
* `bigquery.googleapis.com/Table`
* `bigquery.googleapis.com/RowAccessPolicy`
* `bigquerydatapolicy.googleapis.com/DataPolicy`

如要進一步瞭解組織政策，請參閱「[自訂組織政策](https://docs.cloud.google.com/organization-policy/overview?hl=zh-tw#custom-organization-policies)」。

## 關於組織政策和限制

Google Cloud 組織政策服務可讓您透過程式輔助，集中控管組織的資源。[組織政策管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/orgpolicy?hl=zh-tw#orgpolicy.policyAdmin)可以定義組織政策，也就是一組稱為「限制」的限制條件，適用於Google Cloud 資源和這些資源在[Google Cloud 資源階層](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw)中的子系。您可以在組織、資料夾或專案層級，強制執行組織政策。

組織政策提供各種 Google Cloud 服務的內建[代管限制](https://docs.cloud.google.com/organization-policy/reference/org-policy-constraints?hl=zh-tw)。不過，如要更精細地自訂組織政策中受限的特定欄位，您也可以建立「自訂限制」，並用於組織政策。

### 政策繼承

根據預設，您強制執行政策的資源子系會繼承組織政策。舉例來說，如果您對資料夾強制執行政策， Google Cloud 會對該資料夾中的所有專案強制執行政策。如要進一步瞭解這項行為及變更方式，請參閱「[階層評估規則](https://docs.cloud.google.com/organization-policy/hierarchy-evaluation?hl=zh-tw#disallow_inheritance)」。

### 優點

您可以使用自訂機構政策，允許或拒絕對 BigQuery 資源 (例如資料集、資料表、資料存取權政策、資料列存取政策和常式) 執行特定作業。您可以藉此控管成本及管理資源存取權，以符合貴機構的法規遵循和安全性要求。 Google Cloud 資源限制非常細緻。這些政策可套用至專案、資料夾或機構層級。

## 限制

* 如果資源 (資料集除外) 的自訂限制導致存取遭拒，[`PolicyViolationInfo`](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.Audit/latest/Google.Cloud.Audit.PolicyViolationInfo?hl=zh-tw)不會發布到 [BigQuery 稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)。錯誤訊息會提供拒絕作業的 `constraintId`。

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
- [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
- 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
- 執行下列指令，[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) gcloud CLI：

  ```
  gcloud init
  ```

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
- [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
- 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
- 執行下列指令，[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) gcloud CLI：

  ```
  gcloud init
  ```

1. 請確認您知道[組織 ID](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw#retrieving_your_organization_id)。

### 必要的角色

如要取得管理組織政策所需的權限，請要求管理員授予組織資源的[組織政策管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/orgpolicy?hl=zh-tw#orgpolicy.policyAdmin)  (`roles/orgpolicy.policyAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `orgpolicy.*` 權限，可管理組織政策。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

您必須具備其他權限，才能建立及管理 BigQuery 資源。詳情請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## BigQuery 支援的資源

下表列出可在自訂限制中參照的 BigQuery 資源。

| 資源 | 欄位 |
| --- | --- |
| bigquery.googleapis.com/Dataset | `resource.datasetReference.datasetId` |
| `resource.defaultCollation` |
| `resource.defaultEncryptionConfiguration.kmsKeyName` |
| `resource.defaultPartitionExpirationMs` |
| `resource.defaultRoundingMode` |
| `resource.defaultTableExpirationMs` |
| `resource.description` |
| `resource.externalCatalogDatasetOptions.defaultStorageLocationUri` |
| `resource.externalCatalogDatasetOptions.parameters` |
| `resource.externalDatasetReference.connection` |
| `resource.externalDatasetReference.externalSource` |
| `resource.friendlyName` |
| `resource.isCaseInsensitive` |
| `resource.linkedDatasetSource.sourceDataset.datasetId` |
| `resource.location` |
| `resource.maxTimeTravelHours` |
| `resource.storageBillingModel` |
| bigquery.googleapis.com/Routine | `resource.routineReference.datasetId` |
| `resource.routineReference.projectId` |
| `resource.routineReference.routineId` |
| bigquery.googleapis.com/RowAccessPolicy | `resource.rowAccessPolicyReference.datasetId` |
| `resource.rowAccessPolicyReference.policyId` |
| `resource.rowAccessPolicyReference.projectId` |
| `resource.rowAccessPolicyReference.tableId` |
| bigquery.googleapis.com/Table | `resource.tableReference.datasetId` |
| `resource.tableReference.projectId` |
| `resource.tableReference.tableId` |
| bigquerydatapolicy.googleapis.com/DataPolicy | `resource.dataMaskingPolicy.predefinedExpression` |
| `resource.dataPolicyType` |

## 設定自訂限制

自訂限制是在 YAML 檔案中定義，其中包含您要強制執行組織政策的服務所支援的資源、方法、條件和動作。自訂限制的條件是使用[一般運算語言 (CEL)](https://github.com/google/cel-spec/blob/master/doc/intro.md) 來定義。如要進一步瞭解如何使用 CEL 在自訂限制中建構條件，請參閱「[建立及管理自訂限制](https://docs.cloud.google.com/organization-policy/create-custom-constraints?hl=zh-tw#common_expression_language)」的 CEL 相關章節。

### 控制台

如要建立自訂限制，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Organization policies」(組織政策) 頁面。

   [前往「Organization policies」(組織政策)](https://console.cloud.google.com/iam-admin/orgpolicies?hl=zh-tw)
2. 在專案選擇工具中，選取要設定組織政策的專案。
3. 按一下「自訂限制」add。
4. 在「顯示名稱」方塊中，輸入容易理解的限制名稱。這個名稱會顯示在錯誤訊息中，可用於識別和偵錯。請勿在顯示名稱中使用個人識別資訊 (PII) 或私密資料，因為錯誤訊息可能會顯示這類名稱。這個欄位最多可包含 200 個半形字元。
5. 在「Constraint ID」(限制 ID) 方塊中，輸入新自訂限制的 ID。自訂限制只能包含字母 (包括大寫和小寫) 或數字，例如 `custom.enforceDatasetId`。這個欄位最多可包含 70 個字元，不含前置字元 (`custom.`)，例如 `organizations/123456789/customConstraints/custom`。請勿在限制 ID 中輸入 PII 或機密資料，因為錯誤訊息可能會顯示上述資訊。
6. 在「說明」方塊中，輸入使用者可理解的限制說明。違反政策時，系統會顯示這項說明做為錯誤訊息。請提供違反政策的詳細原因，以及如何解決問題。請勿在說明中輸入 PII 或機密資料，因為錯誤訊息可能會顯示上述資訊。這個欄位最多可輸入 2000 個字元。
7. 在「Resource type」方塊中，選取包含要限制物件和欄位的 Google Cloud REST 資源名稱，例如 `container.googleapis.com/NodePool`。大多數資源類型最多支援 20 項自訂限制。如果您嘗試建立更多自訂限制，作業會失敗。
8. 在「強制執行方式」下方，選取要對 REST `CREATE` 方法強制執行限制，還是同時對 `CREATE` 和 `UPDATE` 方法強制執行限制。如果您在違反限制的資源上，使用 `UPDATE` 方法強制執行限制，除非變更可解決違規問題，否則組織政策會封鎖對該資源的變更。

如要查看各項服務支援的方法，請在「[支援自訂限制的服務](https://docs.cloud.google.com/organization-policy/reference/custom-constraint-supported-services?hl=zh-tw)」中找出該服務。

9. 如要定義條件，請按一下「編輯條件」edit。

1. 在「Add condition」(新增條件) 面板中，建立參照支援服務資源的 CEL 條件，例如 `resource.management.autoUpgrade == false`。這個欄位最多可輸入 1000 個字元。如要進一步瞭解如何使用 CEL，請參閱「[一般運算語言](https://docs.cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints?hl=zh-tw#common_expression_language)」。如要進一步瞭解自訂限制中可使用的服務資源，請參閱「[自訂限制支援的服務](https://docs.cloud.google.com/resource-manager/docs/organization-policy/custom-constraint-supported-services?hl=zh-tw)」。
2. 按一下 [儲存]。

10. 在「動作」下方，選取符合條件時要允許或拒絕評估方法。

如果條件評估結果為 true，系統會禁止建立或更新資源。

允許動作是指只有在條件評估為 true 時，才允許建立或更新資源的作業。除了條件中明確列出的情況外，其他所有情況都會遭到封鎖。

11. 按一下「建立限制」。

在每個欄位中輸入值後，右側會顯示這個自訂限制的對等 YAML 設定。

### gcloud

1. 如要建立自訂限制，請使用下列格式建立 YAML 檔案：

```
name: organizations/ORGANIZATION_ID/customConstraints/CONSTRAINT_NAME
resourceTypes: RESOURCE_NAME
methodTypes:
  - CREATE  
  - UPDATE 
condition: "CONDITION"
actionType: ACTION
displayName: DISPLAY_NAME
description: DESCRIPTION
```

請替換下列項目：

* `ORGANIZATION_ID`：您的機構 ID，例如 `123456789`。
* `CONSTRAINT_NAME`：新自訂限制的名稱。自訂限制只能包含字母 (包括大寫和小寫) 或數字，例如 `custom.enforceDatasetId`。這個欄位最多可包含 70 個字元，不含前置字元 (`custom.`)，例如 `organizations/123456789/customConstraints/custom`。請勿在限制 ID 中輸入 PII 或機密資料，因為錯誤訊息可能會顯示上述資訊。
* `RESOURCE_NAME`：內含要限制的物件和欄位的 Google Cloud資源完整名稱，例如：`bigquery.googleapis.com/Dataset`。大多數資源類型最多支援 20 項自訂限制。如果您嘗試建立更多自訂限制，作業會失敗。
* `methodTypes`：強制執行限制的 REST 方法。可以是 `CREATE`，也可以是 `CREATE` 和 `UPDATE`。如果您在違反限制的資源上使用 `UPDATE` 方法強制執行限制，除非變更可解決違規問題，否則組織政策會封鎖對該資源的變更。

如要查看各項服務支援的方法，請在「[支援自訂限制的服務](https://docs.cloud.google.com/organization-policy/reference/custom-constraint-supported-services?hl=zh-tw)」中找出該服務。

* `CONDITION`：針對支援服務資源表示法所撰寫的 [CEL 條件](https://docs.cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints?hl=zh-tw#common_expression_language)。這個欄位最多可輸入 1000 個字元。例如：
  `"datasetReference.datasetId.startsWith('test')"`。

如要進一步瞭解可編寫條件的資源，請參閱「[支援的資源](#supported_resources)」。

* `ACTION`：符合 `condition` 時採取的動作。可能的值為 `ALLOW` 和 `DENY`。

允許動作是指如果條件評估結果為 true，系統就會允許建立或更新資源的作業。這也表示系統會封鎖條件中明確列出的情況以外的所有其他情況。

拒絕動作表示如果條件評估結果為 true，系統會封鎖建立或更新資源的作業。

* `DISPLAY_NAME`：人類可讀的限制條件名稱。這個名稱會顯示在錯誤訊息中，可用於識別和偵錯。請勿在顯示名稱中使用 PII 或機密資料，因為錯誤訊息可能會顯示這類名稱。這個欄位最多可輸入 200 個半形字元。
* `DESCRIPTION`：違反政策時，會以錯誤訊息形式顯示且易於理解的限制說明。這個欄位最多可輸入 2000 個字元。

2. 為新的自訂限制建立 YAML 檔案後，您必須加以設定，才能用於組織的組織政策。如要設定自訂限制條件，請使用 [`gcloud org-policies set-custom-constraint`](https://docs.cloud.google.com/sdk/gcloud/reference/org-policies/set-custom-constraint?hl=zh-tw) 指令：

```
gcloud org-policies set-custom-constraint CONSTRAINT_PATH
```

請將 `CONSTRAINT_PATH` 替換成自訂限制檔案的完整路徑。例如：`/home/user/customconstraint.yaml`。

這項作業完成後，自訂限制會顯示在 Google Cloud 組織政策清單中，供組織政策使用。

3. 如要驗證是否存在自訂限制條件，請使用 [`gcloud org-policies list-custom-constraints`](https://docs.cloud.google.com/sdk/gcloud/reference/org-policies/list-custom-constraints?hl=zh-tw) 指令：

```
gcloud org-policies list-custom-constraints --organization=ORGANIZATION_ID
```

請將 `ORGANIZATION_ID` 替換成組織資源的 ID。

詳情請參閱「[查看組織政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/creating-managing-policies?hl=zh-tw#viewing_organization_policies)」。

## 強制執行自訂組織政策

如要強制執行限制，請建立參照該限制的組織政策，然後將組織政策套用至 Google Cloud 資源。

### 控制台

1. 前往 Google Cloud 控制台的「Organization policies」(組織政策) 頁面。

   [前往「Organization policies」(組織政策)](https://console.cloud.google.com/iam-admin/orgpolicies?hl=zh-tw)
2. 在專案選擇工具中，選取要設定組織政策的專案。
3. 在「Organization policies」(組織政策) 頁面的清單中選取限制，即可查看該限制的「Policy details」(政策詳細資料) 頁面。
4. 如要為這項資源設定組織政策，請按一下「Manage policy」(管理政策)。
5. 在「Edit policy」(編輯政策) 頁面，選取「Override parent's policy」(覆寫上層政策)。
6. 按一下「Add a rule」(新增規則)。
7. 在「強制執行」部分，選取是否要強制執行這項機構政策。
8. 選用：如要根據標記設定組織政策的條件，請按一下「Add condition」(新增條件)。請注意，如果為組織政策新增條件式規則，您必須至少新增一項無條件規則，否則無法儲存政策。詳情請參閱「[使用標記設定組織政策範圍](https://docs.cloud.google.com/organization-policy/scope-policies?hl=zh-tw)」。
9. 按一下「Test changes」(測試變更)，模擬組織政策的影響。詳情請參閱「[使用 Policy Simulator 測試組織政策變更](https://docs.cloud.google.com/policy-intelligence/docs/test-organization-policies?hl=zh-tw)」。
10. 如要在模擬測試模式下強制執行組織政策，請按一下「設定模擬測試政策」。詳情請參閱「[測試組織政策](https://docs.cloud.google.com/organization-policy/test-policies?hl=zh-tw)」。
11. 確認試營運模式中的機構政策運作正常後，請按一下「設定政策」，設定正式政策。

### gcloud

1. 如要建立含有布林規則的組織政策，請建立參照限制的政策 YAML 檔案：

```
name: projects/PROJECT_ID/policies/CONSTRAINT_NAME
spec:
  rules:
  - enforce: true

dryRunSpec:
  rules:
  - enforce: true
```

請替換下列項目：

* `PROJECT_ID`：要強制執行限制的專案。
* `CONSTRAINT_NAME`：要為自訂限制定義的名稱，例如：`custom.enforceDatasetId`。

2. 如要以[模擬測試模式](https://docs.cloud.google.com/organization-policy/test-policies?hl=zh-tw)強制執行組織政策，請執行下列指令並加上 `dryRunSpec` 旗標：

```
gcloud org-policies set-policy POLICY_PATH --update-mask=dryRunSpec
```

請將 `POLICY_PATH` 替換為組織政策 YAML 檔案的完整路徑。政策最多需要 15 分鐘才會生效。

3. 確認模擬測試模式中的機構政策能發揮預期效果後，請使用 `org-policies set-policy` 指令和 `spec` 旗標設定正式政策：

```
gcloud org-policies set-policy POLICY_PATH --update-mask=spec
```

請將 `POLICY_PATH` 替換為組織政策 YAML 檔案的完整路徑。政策最多需要 15 分鐘才會生效。

## 測試自訂組織政策

下列範例會建立自訂限制和政策，禁止特定專案中的所有新資料集 ID 以 `test` 開頭。

開始之前，請務必備妥以下項目：

* 組織 ID
* 專案 ID

### 建立限制條件

如要建立自訂限制，請按照下列步驟操作：

1. 建立下列 YAML 檔案，並儲存為 `constraint-enforce-datasetId.yaml`：

   ```
   name: organizations/ORGANIZATION_ID/customConstraints/custom.enforceDatasetId
   resourceTypes:
   - bigquery.googleapis.com/Dataset
   methodTypes:
   - CREATE
   condition: "datasetReference.datasetId.startsWith('test')"
   actionType: DENY
   displayName: Reject test datasets.
   description: Deny new dataset names that begin with 'test'.
   ```

   請將 `ORGANIZATION_ID` 替換成組織 ID。

   這項限制會禁止建立名稱開頭為「test」的資料集。
2. 套用限制：

   ```
   gcloud org-policies set-custom-constraint ~/constraint-enforce-datasetId
   ```
3. 確認限制是否存在：

   ```
   gcloud org-policies list-custom-constraints --organization=ORGANIZATION_ID
   ```

   輸出結果會與下列內容相似：

   ```
   CUSTOM_CONSTRAINT                       ACTION_TYPE  METHOD_TYPES   RESOURCE_TYPES                     DISPLAY_NAME
   custom.enforceDatasetId                 DENY         CREATE         bigquery.googleapis.com/Dataset    Reject test datasets
   ...
   ```

### 建立政策

現在請建立政策，並套用至您建立的自訂限制。

1. 將下列檔案儲存為 `policy-enforce-datasetId.yaml`：

   ```
   name: projects/PROJECT_ID/policies/custom.enforceDatasetId
   spec:
     rules:
     - enforce: true
   ```

   將 `PROJECT_ID` 替換為專案 ID。
2. 套用政策：

   ```
   gcloud org-policies set-policy ~/policy-enforce-datasetId.yaml
   ```
3. 確認政策是否存在：

   ```
   gcloud org-policies list --project=PROJECT_ID
   ```

   輸出結果會與下列內容相似：

   ```
   CONSTRAINT                  LIST_POLICY    BOOLEAN_POLICY    ETAG
   custom.enforceDatasetId     -              SET               COCsm5QGENiXi2E=
   ```

套用政策後， Google Cloud最多可能需要兩分鐘才會開始強制執行。

### 測試政策

嘗試在專案中建立 BigQuery 資料集：

```
bq --location=US mk -d \
    --default_table_expiration 3600 \
    --description "This is my dataset." \
    testdataset
```

輸出內容如下：

```
Operation denied by custom org policies: ["customConstraints/custom.enforceDatasetId": "All new datasets can't begin with 'test'."]
```

## 常見用途的自訂組織政策範例

下表提供一些常見自訂限制的語法範例。

| 說明 | 限制語法 |
| --- | --- |
| 拒絕名稱開頭為「test」的新資料表。 | ```     name: organizations/ORGANIZATION_ID/customConstraints/custom.enforceTableId     resourceTypes:     - bigquery.googleapis.com/Table     methodTypes:     - CREATE     condition: "resource.tableReference.tableId.startsWith('test')"     actionType: DENY     displayName: Reject test tables.     description: Deny new table names that begin with 'test'. ``` |
| 拒絕名稱開頭為「test」的新資料列存取政策。 | ```     name: organizations/ORGANIZATION_ID/customConstraints/custom.enforceRowAccessPolicyId     resourceTypes:     - bigquery.googleapis.com/RowAccessPolicies     methodTypes:     - CREATE     condition: "resource.rowAccessPolicyReference.policyId.startsWith('test')"     actionType: DENY     displayName: Reject 'test' row access policies.     description: Deny new row access policies with names that begin with 'test'. ``` |
| 使用以「SHA256」(安全雜湊演算法 256 位元) 開頭的預先定義運算式，拒絕新的資料存取權政策。 | ```     name: organizations/ORGANIZATION_ID/customConstraints/custom.enforcePredefinedExpression     resourceTypes:     - bigquerydatapolicy.googleapis.com/DataPolicy     methodTypes:     - CREATE     condition: "resource.dataMaskingPolicy.predefinedExpression.startsWith('SHA256')"     actionType: DENY     displayName: Reject SHA256 data policies.     description: Deny new data access policies with predefined expressions that     begin with 'SHA256'.     expression. ``` |
| 拒絕名稱開頭為「test」的新常式。 | ```     name: organizations/ORGANIZATION_ID/customConstraints/custom.enforceRoutineId     resourceTypes:     - bigquery.googleapis.com/Routine     methodTypes:     - CREATE     condition: "resource.routineReference.routineId.startsWith('test')"     actionType: DENY     displayName: Reject test routines.     description: Deny new routines with names that begin with 'test'. ``` |

## 後續步驟

* 進一步瞭解[組織政策服務](https://docs.cloud.google.com/organization-policy/overview?hl=zh-tw)。
* 進一步瞭解如何[建立及管理組織政策](https://docs.cloud.google.com/organization-policy/create-organization-policies?hl=zh-tw)。
* 查看代管[組織政策限制](https://docs.cloud.google.com/organization-policy/reference/org-policy-constraints?hl=zh-tw)的完整清單。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-15 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-15 (世界標準時間)。"],[],[]]