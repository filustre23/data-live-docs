* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 使用自定义限制条件管理共享 Sharing 交换和清单

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**如需提供反馈或请求支持，请联系 [bq-data-sharing-feedback@google.com](mailto:bq-data-sharing-feedback@google.com) 。

本页面介绍了如何使用组织政策服务自定义限制条件来限制对以下 Google Cloud 资源执行的特定操作：

* `analyticshub.googleapis.com/DataExchange`
* `analyticshub.googleapis.com/Listing`

如需详细了解组织政策，请参阅[自定义组织政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview?hl=zh-cn#custom-organization-policies)。

## 组织政策和限制条件简介

借助 Google Cloud 组织政策服务，您可以对组织的资源进行程序化集中控制。作为[组织政策管理员](https://docs.cloud.google.com/iam/docs/understanding-roles?hl=zh-cn#orgpolicy.policyAdmin)，您可以定义组织政策，这是一组称为限制条件的限制，会应用于 [Google Cloud 资源层次结构](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-cn)中的Google Cloud 资源及其后代。您可以在组织、文件夹或项目级强制执行组织政策。

组织政策为各种 Google Cloud 服务提供内置的[托管式限制](https://docs.cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints?hl=zh-cn)。但是，如果您想要更精细地控制和自定义组织政策中受限的特定字段，还可以创建自定义限制条件并在组织政策中使用这些自定义限制条件。

### 政策继承

如果您对资源强制执行政策，默认情况下，该资源的后代会继承组织政策。例如，如果您对某个文件夹强制执行一项政策， Google Cloud 会对该文件夹中的所有项目强制执行该政策。如需详细了解此行为及其更改方式，请参阅[层次结构评估规则](https://docs.cloud.google.com/resource-manager/docs/organization-policy/understanding-hierarchy?hl=zh-cn#disallow_inheritance)。

## 限制

* 您只能使用 Google Cloud 控制台或 Google Cloud CLI 为 BigQuery Sharing 资源设置自定义限制条件。
* 您只能对 BigQuery Sharing 资源的 `CREATE` 或 `UPDATE` 方法强制执行自定义限制条件。
* 新的自定义限制条件不会自动应用于现有资源。您必须更新现有资源才能应用限制条件。如需查找需要更新的现有资源，请强制执行[试运行组织政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/dry-run-policy?hl=zh-cn)。
  在试运行现有资源期间，系统不会检查[发布到数据净室的现有清单](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-cn#add-data)。
* 不支持模拟当前资源的限制条件。
* 您必须以小写字母形式在 `resource.bigqueryDataset.replicaLocations` 字段中设置值。如需了解详情，请参阅[支持的资源](#supported_resources)。

## 准备工作

- Sign in to your Google Cloud account. If you're new to
  Google Cloud, [create an account](https://console.cloud.google.com/freetrial?hl=zh-cn) to evaluate how our products perform in
  real-world scenarios. New customers also get $300 in free credits to
  run, test, and deploy workloads.
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-cn)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-cn#confirm_billing_is_enabled_on_a_project).
- [Install](https://docs.cloud.google.com/sdk/docs/install?hl=zh-cn) the Google Cloud CLI.

  - 如果您使用的是外部身份提供方 (IdP)，则必须先[使用联合身份登录 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-cn)。
  - 如需[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-cn) gcloud CLI，请运行以下命令：

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
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-cn)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-cn#confirm_billing_is_enabled_on_a_project).
- [Install](https://docs.cloud.google.com/sdk/docs/install?hl=zh-cn) the Google Cloud CLI.

  - 如果您使用的是外部身份提供方 (IdP)，则必须先[使用联合身份登录 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-cn)。
  - 如需[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-cn) gcloud CLI，请运行以下命令：

    ```
    gcloud init
    ```

1. 请确保您知道您的[组织 ID](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-cn#retrieving_your_organization_id)。

### 所需的角色

如需获得管理自定义组织政策所需的权限，请让您的管理员为您授予组织资源的 [Organization Policy Administrator](https://docs.cloud.google.com/iam/docs/roles-permissions/orgpolicy?hl=zh-cn#orgpolicy.policyAdmin) (`roles/orgpolicy.policyAdmin`) IAM 角色。
如需详细了解如何授予角色，请参阅[管理对项目、文件夹和组织的访问权限](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn)。

您也可以通过[自定义角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-cn)或其他[预定义角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-cn#predefined)来获取所需的权限。

## 设置自定义限制条件

自定义限制条件是在 YAML 文件中，由实施组织政策的服务所支持的资源、方法、条件和操作定义的。自定义限制条件的条件使用[通用表达式语言 (CEL)](https://github.com/google/cel-spec/blob/master/doc/intro.md) 进行定义。如需详细了解如何使用 CEL 构建自定义限制条件中的条件，请参阅[创建和管理自定义限制条件](https://docs.cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints?hl=zh-cn#common_expression_language)的 CEL 部分。

### 控制台

如需创建自定义限制条件，请执行以下操作：

1. 在 Google Cloud 控制台中，转到**组织政策**页面。

   [转到组织政策](https://console.cloud.google.com/iam-admin/orgpolicies?hl=zh-cn)
2. 在项目选择器中，选择要为其设置组织政策的项目。
3. 点击 add **自定义限制条件**。
4. 在**显示名称**框中，为限制条件输入一个人类可读名称。此名称会在错误消息中使用，并可用于识别和调试用途。请勿在显示名称中使用个人身份信息或敏感数据，因为此名称可能会在错误消息中公开。此字段最多可包含 200 个字符。
5. 在**限制条件 ID** 框中，为新的自定义限制条件输入所需的名称。自定义限制条件只能包含字母（包括大写和小写）或数字，例如 `custom.disableGkeAutoUpgrade`。此字段最多可包含 70 个字符，不计算前缀 (`custom.`)，例如 `organizations/123456789/customConstraints/custom`。请勿在限制条件 ID 中包含个人身份信息或敏感数据，因为该 ID 可能会在错误消息中公开。
6. 在**说明**框中，输入人类可读的限制条件说明。当违反政策时，此说明将用作错误消息。请包含有关发生违规的原因以及如何解决违规问题的详细信息。请勿在说明中包含个人身份信息或敏感数据，因为该说明可能会在错误消息中公开。
   此字段最多可包含 2000 个字符。
7. 在**资源类型**框中，选择包含要限制的对象和字段的 Google Cloud REST 资源的名称，例如 `container.googleapis.com/NodePool`。大多数资源类型最多支持 20 个自定义限制条件。如果您尝试创建更多自定义限制条件，操作将会失败。
8. 在**强制执行方法**下，选择是对 REST **CREATE** 方法强制执行限制条件，还是同时对 **CREATE** 和 **UPDATE** 方法强制执行限制条件。如果您对违反限制条件的资源使用 **UPDATE** 方法强制执行限制条件，除非更改解决了违规问题，否则组织政策会阻止对该资源的更改。

并非所有 Google Cloud 服务都支持这两种方法。如需查看每种服务支持的方法，请在[支持的服务](https://docs.cloud.google.com/resource-manager/docs/organization-policy/custom-constraint-supported-services?hl=zh-cn)中找到相应服务。

9. 如需定义条件，请点击 edit **修改条件**。

1. 在**添加条件**面板中，创建一个引用受支持服务资源的 CEL 条件，例如 `resource.management.autoUpgrade == false`。此字段最多可包含 1,000 个字符。如需详细了解 CEL 用法，请参阅[通用表达式语言](https://docs.cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints?hl=zh-cn#common_expression_language)。
   如需详细了解可在自定义限制条件中使用的服务资源，请参阅[自定义限制条件支持的服务](https://docs.cloud.google.com/resource-manager/docs/organization-policy/custom-constraint-supported-services?hl=zh-cn)。
2. 点击**保存**。

10. 在**操作**下，选择在满足条件时是允许还是拒绝评估的方法。

拒绝操作意味着，如果条件计算结果为 true，则创建或更新资源的操作会被阻止。

允许操作意味着，仅当条件计算结果为 true 时，才允许执行创建或更新资源的操作。除了条件中明确列出的情况之外，其他所有情况都会被阻止。

11. 点击**创建限制条件**。

在每个字段中输入值后，右侧将显示此自定义限制条件的等效 YAML 配置。

### gcloud

1. 如需创建自定义限制条件，请使用以下格式创建 YAML 文件：

```
      name: organizations/ORGANIZATION_ID/customConstraints/CONSTRAINT_NAME
      resourceTypes:
      - RESOURCE_NAME
      methodTypes:
      - CREATE  
- UPDATE 
      condition: "CONDITION"
      actionType: ACTION
      displayName: DISPLAY_NAME
      description: DESCRIPTION
```

请替换以下内容：

* `ORGANIZATION_ID`：您的组织 ID，例如 `123456789`。
* `CONSTRAINT_NAME`：新的自定义限制条件的名称。自定义限制条件只能包含字母（包括大写和小写）或数字，例如 `custom.enforceDataExchangeDiscovery`。此字段最多可包含 70 个字符。
* `RESOURCE_NAME`：包含要限制的对象和字段的 Google Cloud资源的完全限定名称。例如 `analyticshub.googleapis.com/DataExchange`。
* `CONDITION`：针对受支持服务资源的表示形式编写的 [CEL 条件](https://docs.cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints?hl=zh-cn#common_expression_language)。此字段最多可包含 1,000 个字符。例如 `"resource.discoveryType == 'DISCOVERY_TYPE_PUBLIC'"`。

如需详细了解可针对其编写条件的资源，请参阅[支持的资源](#supported_resources)。

* `ACTION`：满足 `condition` 时要执行的操作。
  可能的值包括 `ALLOW` 和 `DENY`。

允许操作意味着，如果条件计算结果为 true，则允许执行创建或更新资源的操作。这也意味着，除了条件中明确列出的情况之外，其他所有情况都会被阻止。

拒绝操作意味着，如果条件计算结果为 true，则创建或更新资源的操作会被阻止。

* `DISPLAY_NAME`：限制条件的直观易记名称。此字段最多可包含 200 个字符。
* `DESCRIPTION`：直观易懂的限制条件说明，当违反政策时会作为错误消息显示。此字段最多可包含 2000 个字符。

2. 为新的自定义限制条件创建 YAML 文件后，您必须对其进行设置，以使其可用于组织中的组织政策。如需设置自定义限制条件，请使用 [`gcloud org-policies set-custom-constraint`](https://docs.cloud.google.com/sdk/gcloud/reference/org-policies/set-custom-constraint?hl=zh-cn) 命令：

```
        gcloud org-policies set-custom-constraint CONSTRAINT_PATH
```

将 `CONSTRAINT_PATH` 替换为自定义限制条件文件的完整路径。例如 `/home/user/customconstraint.yaml`。

此操作完成后，您的自定义限制条件将作为组织政策显示在您的 Google Cloud 组织政策列表中。

3. 如需验证自定义限制条件是否存在，请使用 [`gcloud org-policies list-custom-constraints`](https://docs.cloud.google.com/sdk/gcloud/reference/org-policies/list-custom-constraints?hl=zh-cn) 命令：

```
      gcloud org-policies list-custom-constraints --organization=ORGANIZATION_ID
```

将 `ORGANIZATION_ID` 替换为您的组织资源的 ID。

如需了解详情，请参阅[查看组织政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/creating-managing-policies?hl=zh-cn#viewing_organization_policies)。

## 强制执行自定义组织政策

如需强制执行限制条件，您可以创建引用该限制条件的组织政策，并将该组织政策应用于 Google Cloud 资源。

### 控制台

1. 在 Google Cloud 控制台中，前往**组织政策**页面。

   [转到组织政策](https://console.cloud.google.com/iam-admin/orgpolicies?hl=zh-cn)
2. 在项目选择器中，选择要为其设置组织政策的项目。
3. 从**组织政策**页面上的列表中选择您的限制条件，以查看该限制条件的**政策详情**页面。
4. 如需为该资源配置组织政策，请点击**管理政策**。
5. 在**修改政策**页面，选择**覆盖父级政策**。
6. 点击**添加规则**。
7. 在**强制执行**部分中，选择是否强制执行此组织政策。
8. （可选）如需使组织政策成为基于某个标记的条件性政策，请点击**添加条件**。请注意，如果您向组织政策添加条件规则，则必须至少添加一个无条件规则，否则无法保存政策。如需了解详情，请参阅[设置带有标记的组织政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/tags-organization-policy?hl=zh-cn)。
9. 点击**测试更改**以模拟组织政策的效果。如需了解详情，请参阅[使用 Policy Simulator 测试组织政策更改](https://docs.cloud.google.com/policy-intelligence/docs/test-organization-policies?hl=zh-cn)。
10. 如需在试运行模式下强制执行组织政策，请点击**设置试运行政策**。如需了解详情，请参阅[在试运行模式下创建组织政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/dry-run-policy?hl=zh-cn)。
11. 验证试运行模式下的组织政策按预期运行后，点击**设置政策**来设置现行政策。

### gcloud

1. 如需创建包含布尔值规则的组织政策，请创建引用该限制条件的 YAML 政策文件：

```
        name: projects/PROJECT_ID/policies/CONSTRAINT_NAME
        spec:
          rules:
          - enforce: true
        
        dryRunSpec:
          rules:
          - enforce: true
```

请替换以下内容：

* `PROJECT_ID`：要对其强制执行您的限制条件的项目。
* `CONSTRAINT_NAME`：您为自定义限制条件定义的名称。例如，`custom.enforceDataExchangeDiscovery`。

2. 如需在[试运行模式](https://docs.cloud.google.com/resource-manager/docs/organization-policy/dry-run-policy?hl=zh-cn)下强制执行组织政策，请运行以下带有 `dryRunSpec` 标志的命令：

```
        gcloud org-policies set-policy POLICY_PATH \
          --update-mask=dryRunSpec
```

将 `POLICY_PATH` 替换为组织政策 YAML 文件的完整路径。该政策最长需要 15 分钟才能生效。

3. 验证试运行模式下的组织政策按预期运行后，使用 `org-policies set-policy` 命令和 `spec` 标志设置现行政策：

```
        gcloud org-policies set-policy POLICY_PATH \
          --update-mask=spec
```

将 `POLICY_PATH` 替换为组织政策 YAML 文件的完整路径。该政策最长需要 15 分钟才能生效。

## 测试自定义组织政策

以下示例展示了如何创建自定义限制条件和政策，要求所有 `analyticshub.googleapis.com/DataExchange` 资源都是不公开的。

在开始之前，您必须拥有以下各项：

* 您的组织 ID
* 项目 ID

### 创建限制条件

如需创建自定义限制条件，请按照以下步骤操作：

1. 将以下文件保存为 `constraint-enforce-dataExchangeDiscovery.yaml`：

   ```
   name: organizations/ORGANIZATION_ID/customConstraints/custom.enforceDataExchangeDiscovery
   resourceTypes:
   - analyticshub.googleapis.com/DataExchange
   methodTypes:
   - CREATE
   condition: "resource.discoveryType == 'DISCOVERY_TYPE_PUBLIC'"
   actionType: DENY
   displayName: Reject public DataExchanges.
   description: All DataExchange resources must be private.
   ```

   将 `ORGANIZATION_ID` 替换为您的组织 ID。

   此限制条件会拒绝创建或配置发现类型为公开的新 `analyticshub.googleapis.com/DataExchange` 资源的操作。
2. 应用限制条件：

   ```
   gcloud org-policies set-custom-constraint ~/constraint-enforce-dataExchangeDiscovery.yaml
   ```
3. 验证限制条件存在：

   ```
   gcloud org-policies list-custom-constraints --organization=ORGANIZATION_ID
   ```

   输出类似于以下内容：

   ```
   CUSTOM_CONSTRAINT                       ACTION_TYPE  METHOD_TYPES   RESOURCE_TYPES                           DISPLAY_NAME
   custom.enforceDataExchangeDiscovery     DENY         CREATE,UPDATE  analyticshub.googleapis.com/DataExchange Reject public DataExchanges.
   ...
   ```

### 创建政策

创建政策，并将该政策应用于您创建的自定义限制条件。

1. 将以下文件保存为 `policy-enforce-dataExchangeDiscovery.yaml`：

   ```
   name: projects/PROJECT_ID/policies/custom.enforceDataExchangeDiscovery
   spec:
     rules:
     - enforce: true
   ```

   将 `PROJECT_ID` 替换为您的项目 ID。
2. 应用政策：

   ```
   gcloud org-policies set-policy ~/policy-enforce-dataExchangeDiscovery.yaml
   ```
3. 验证政策存在：

   ```
   gcloud org-policies list --project=PROJECT_ID
   ```

   输出类似于以下内容：

   ```
   CONSTRAINT                           LIST_POLICY    BOOLEAN_POLICY    ETAG
   custom.enforceDataExchangeDiscovery  -              SET               ETAG
   ```

应用政策后，请等待大约两分钟，以便 Google Cloud 开始强制执行政策。

### 测试政策

按照[创建数据交换](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-cn#create-exchange)中的步骤在项目中创建 `analyticshub.googleapis.com/DataExchange` 资源。设为可公开发现。

输出如下所示：

```
Operation failed, please try again. Error Message: Operation denied by org policy on resource 'projects/PROJECT_ID/locations/us':
["customConstraints/custom.enforceDataExchangeDiscovery": "All DataExchange resources must be private."]
```

## 常见用例的自定义组织政策示例

下表提供了一些常见自定义限制条件的语法示例。

| 说明 | 限制条件语法 |
| --- | --- |
| `DataExchange` 资源无法公开发现。 | ```     name: organizations/ORGANIZATION_ID/customConstraints/custom.enforceDataExchangeDiscovery     resource_types: analyticshub.googleapis.com/DataExchange     method_types:       - CREATE       - UPDATE     condition: resource.discoveryType == 'DISCOVERY_TYPE_PUBLIC'     action_type: DENY     display_name: Reject public DataExchanges.     description: All DataExchange resources must be private. ``` |
| 仅允许在数据净室 (DCR) 中创建 `DataExchange` 资源。 | ```     name:       organizations/ORGANIZATION_ID/customConstraints/custom.analyticsHubAllowDCRDataExchange     resource_types: analyticshub.googleapis.com/DataExchange     method_types:       - CREATE     condition: has(resource.sharingEnvironmentConfig.dcrExchangeConfig)     action_type: ALLOW     display_name: Allow a DataExchange in a DCR.     description: Only allow the creation of a DataExchange resource in a DCR. ``` |
| 仅允许启用了订阅方邮件日志记录的 `DataExchange` 资源。 | ```     name: organizations/ORGANIZATION_ID/customConstraints/custom.subscriberEmailLoggingAllowed     resource_types: analyticshub.googleapis.com/DataExchange     method_types:       - CREATE       - UPDATE     condition: resource.logLinkedDatasetQueryUserEmail == true     action_type: ALLOW     display_name: Subscriber email logging must be enabled.     description: Subscriber email logging must be enabled for DataExchange resources. ``` |
| `Listing` 资源无法公开发现。 | ```     name: organizations/ORGANIZATION_ID/customConstraints/custom.noPublicListing     resource_types: analyticshub.googleapis.com/Listing     method_types:       - CREATE       - UPDATE     condition: resource.discoveryType == 'DISCOVERY_TYPE_PUBLIC'     action_type: DENY     display_name: Reject public Listings.     description: All Listing resources must be undiscoverable. ``` |
| `Listing` 资源必须引用 BigQuery 数据集。 | ```     name: organizations/ORGANIZATION_ID/customConstraints/custom.listingWithBQDataset     resource_types: analyticshub.googleapis.com/Listing     method_types:       - CREATE       - UPDATE     condition: has(resource.bigqueryDataset) && resource.bigqueryDataset.dataset.contains('test')     action_type: ALLOW     display_name: Listing must have a BigQuery dataset.     description: Listing must have a BigQuery dataset whose name contains the string "test". ``` |
| `Listing` 资源必须启用 `restrictedExportPolicy` 对象。 | ```     name: organizations/ORGANIZATION_ID/customConstraints/custom.listingWithRestrictedExportPolicy     resource_types: analyticshub.googleapis.com/Listing     method_types:       - CREATE       - UPDATE     condition: has(resource.bigqueryDataset) && has(resource.bigqueryDataset.restrictedExportPolicy) && resource.bigqueryDataset.restrictedExportPolicy.enabled == true     action_type: DENY     display_name: The Listing must have restricted export policy.     description: The Listing resource must have restrictedExportPolicy enabled to allow egress controls. ``` |

## BigQuery Sharing 支持的资源

下表列出了您可以在自定义限制条件中引用的 BigQuery Sharing 资源。

| 资源 | 字段 |
| --- | --- |
| analyticshub.googleapis.com/DataExchange | `resource.description` |
| `resource.discoveryType` |
| `resource.displayName` |
| `resource.documentation` |
| `resource.icon` |
| `resource.logLinkedDatasetQueryUserEmail` |
| `resource.primaryContact` |
| analyticshub.googleapis.com/Listing | `resource.allowOnlyMetadataSharing` |
| `resource.bigqueryDataset.dataset` |
| `resource.bigqueryDataset.replicaLocations` |
| `resource.bigqueryDataset.restrictedExportPolicy.enabled` |
| `resource.bigqueryDataset.restrictedExportPolicy.restrictDirectTableAccess` |
| `resource.bigqueryDataset.restrictedExportPolicy.restrictQueryResult` |
| `resource.bigqueryDataset.selectedResources.routine` |
| `resource.bigqueryDataset.selectedResources.table` |
| `resource.categories` |
| `resource.dataProvider.name` |
| `resource.dataProvider.primaryContact` |
| `resource.description` |
| `resource.discoveryType` |
| `resource.displayName` |
| `resource.documentation` |
| `resource.icon` |
| `resource.logLinkedDatasetQueryUserEmail` |
| `resource.primaryContact` |
| `resource.publisher.name` |
| `resource.publisher.primaryContact` |
| `resource.pubsubTopic.dataAffinityRegions` |
| `resource.pubsubTopic.topic` |
| `resource.requestAccess` |
| `resource.restrictedExportConfig.enabled` |
| `resource.restrictedExportConfig.restrictQueryResult` |

## 后续步骤

* 详细了解[自定义限制条件](https://docs.cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints?hl=zh-cn)。
* 详细了解[组织政策服务](https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview?hl=zh-cn)。
* 详细了解如何[创建和管理组织政策](https://docs.cloud.google.com/resource-manager/docs/organization-policy/using-constraints?hl=zh-cn)。
* 查看托管式[组织政策限制条件](https://docs.cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints?hl=zh-cn)的完整列表。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-01-06。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-01-06。"],[],[]]