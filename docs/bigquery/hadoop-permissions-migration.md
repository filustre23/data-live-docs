* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 从 Hadoop 迁移权限

**预览版**

此功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版功能“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**如需就此功能获得支持或提供反馈，请发送邮件至 [bigquery-permission-migration-support@google.com](mailto:bigquery-permission-migration-support@google.com)。

本文档介绍了如何将 Apache Hadoop 分布式文件系统 (HDFS)、Ranger HDFS 和 Apache Hive 中的权限迁移到 Cloud Storage 或 BigQuery 中的 Identity and Access Management (IAM) 角色。

此权限迁移过程包括以下步骤：

1. 先创建主账号规则集 YAML 配置文件，以[生成主账号映射文件](#generate_a_principals_mapping_file)。然后，使用主账号规则集 YAML 文件以及 HDFS 或 Ranger 元数据文件运行权限迁移工具，以生成主账号映射文件。
2. 先创建权限规则集 YAML 文件，以[生成目标权限映射文件](#generate_target_permissions_file)。然后，使用权限规则集 YAML 文件、表映射配置文件和 HDFS 或 Ranger 元数据文件运行权限迁移工具，以生成目标权限映射文件。
3. 使用目标权限文件运行权限迁移工具，以[将权限应用于 Cloud Storage 或 BigQuery](#apply_permissions)。您还可以使用提供的 Python 脚本生成一个 Terraform 文件，您可以使用该文件自行应用权限。

## 准备工作

在迁移权限之前，请确认您已完成以下操作：

* 安装 [`dwh-migration-dumper` 工具](https://docs.cloud.google.com/bigquery/docs/hadoop-metadata?hl=zh-cn#install-dumper)。
* [运行 `dwh-migration-dumper` 工具](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-cn#extract-metadata-logs)，为数据源生成必要的元数据。

您还可以在发布软件包中的 `terraform.zip` 文件内找到 Terraform 生成器脚本。

## 生成主账号映射文件

主账号映射文件定义了将来源中的主账号映射到 Google Cloud IAM 主账号的映射规则。

如需生成主账号映射文件，您必须先手动创建主账号规则集 YAML 文件，以定义如何将来源中的主账号映射到 Google Cloud IAM 主账号。在主账号规则集 YAML 文件中，为每个来源（`ranger`、`HDFS` 或两者）定义映射规则。

以下示例展示了一个主账号规则集 YAML 文件，该文件将 Apache Ranger 群组映射到 Google Cloud中的服务账号：

```
  ranger:
    user_rules:
      - skip: true
    group_rules:
      # Skip internal Ranger groups.
      - skip: true
        when: "group.groupSource == 0"

      # Map all roles to Google Cloud Platform service accounts.
      - map:
          type:
            value: serviceAccount
          email_address:
            expression: "group.name + 'my-service-account@my-project.iam.gserviceaccount.com'"

    role_rules:
      - skip: true

  hdfs:
    user_rules:
      - skip: true
    group_rules:
      - skip: true
    other_rules:
      - skip: true
```

以下示例展示了一个主账号规则集 YAML 文件，该文件将 HDFS 用户映射到特定的 Google Cloud 用户：

```
  ranger:
    user_rules:
      - skip: true
    group_rules:
      - skip: true
    role_rules:
      - skip: true

  hdfs:
    user_rules:
      # Skip user named 'example'
      - when: "user.name == 'example'"
        skip: true
      # Map all other users to their name at google.com
      - when: "true"
        map:
          type:
            value: user
          email_address:
            expression: "user.name + '@google.com'"

    group_rules:
      - skip: true
    other_rules:
      - skip: true
```

如需详细了解用于创建主账号规则集 YAML 文件的语法，请参阅[规则集 YAML 文件](#ruleset_yaml_files)。

创建主账号规则集 YAML 文件后，将其上传到 Cloud Storage 存储桶。您还必须添加由 `dwh-migration-dumper` 工具生成的 HDFS 文件、Apache Ranger 文件或同时添加这两者，具体取决于您要从哪个来源迁移权限。然后，您可以运行权限迁移工具来生成主账号映射文件。

以下示例展示了如何运行权限迁移工具来同时从 HDFS 和 Apache Ranger 这两者进行迁移，并生成名为 `principals.yaml` 的主账号映射文件。

```
./dwh-permissions-migration expand \
    --principal-ruleset gs://MIGRATION_BUCKET/principals-ruleset.yaml \
    --hdfs-dumper-output gs://MIGRATION_BUCKET/hdfs-dumper-output.zip \
    --ranger-dumper-output gs://MIGRATION_BUCKET/ranger-dumper-output.zip \
    --output-principals gs://MIGRATION_BUCKET/principals.yaml
```

将 `MIGRATION_BUCKET` 替换为包含迁移文件的 Cloud Storage 存储桶的名称。

运行该工具后，检查生成的 `principals.yaml` 文件，验证其中是否包含从来源映射到 Google CloudIAM 主账号的主账号。您可以在执行后续步骤之前手动修改该文件。

## 生成目标权限文件

目标权限文件包含有关 Hadoop 集群中的来源权限集与 BigQuery 或 Cloud Storage 托管文件夹的 IAM 角色之间映射关系的信息。如需生成目标权限文件，您必须先手动创建权限规则集 YAML 文件，以指定 Ranger 或 HDFS 中的权限如何映射到 Cloud Storage 或 BigQuery。

以下示例接受将所有 Ranger 权限映射到 Cloud Storage：

```
gcs:
  ranger_hive_rules:
    - map: {}
      log: true
```

以下示例接受除 `hadoop` 主账号以外的所有 HDFS 权限：

```
gcs:
  hdfs_rules:
    - when:
        source_principal.name == 'hadoop'
      skip: true
    - map: {}
```

以下示例替换了表 `tab0` 的默认角色映射，并对所有其他权限使用默认设置

```
gcs:
  ranger_hive_rules:
    ranger_hive_rules:
      - when: table.name == 'tab0'
        map:
          role:
            value: "roles/customRole"
      - map: {}
```

如需详细了解用于创建权限规则集 YAML 文件的语法，请参阅[规则集 YAML 文件](#ruleset_yaml_files)。

创建权限规则集 YAML 文件后，将其上传到 Cloud Storage 存储桶。您还必须添加由 `dwh-migration-dumper` 工具生成的 HDFS 文件、Apache Ranger 文件或同时添加这两者，具体取决于您要从哪个来源迁移权限。您还必须添加[表配置 YAML 文件](https://docs.cloud.google.com/bigquery/docs/hadoop-transfer?hl=zh-cn#generate_tables_mapping_yaml_files)和[主账号映射文件](#generate_a_principals_mapping_file)。

然后，您可以运行权限迁移工具来生成目标权限文件。

以下示例展示了如何使用表映射配置文件和名为 `principals.yaml` 的主账号映射文件运行权限迁移工具来同时从 HDFS 和 Apache Ranger 这两者进行迁移，并生成名为 `permissions.yaml` 的主账号映射文件。

```
./dwh-permissions-migration build \
    --permissions-ruleset gs://MIGRATION_BUCKET/permissions-config.yaml \
    --tables gs://MIGRATION_BUCKET/tables/ \
    --principals gs://MIGRATION_BUCKET/principals.yaml \
    --ranger-dumper-output gs://MIGRATION_BUCKET/ranger-dumper-output.zip \
    --hdfs-dumper-output gs://MIGRATION_BUCKET/hdfs-dumper-output.zip \
    --output-permissions gs://MIGRATION_BUCKET/permissions.yaml
```

将 `MIGRATION_BUCKET` 替换为包含迁移文件的 Cloud Storage 存储桶的名称。

运行该工具后，检查生成的 `permissions.yaml` 文件，验证其中是否包含从来源映射到 Cloud Storage 或 BigQuery IAM 绑定的权限。您可以在执行后续步骤之前手动进行修改。

## 应用权限

生成目标权限文件后，您便可以运行权限迁移工具，将 IAM 权限应用于 Cloud Storage 或 BigQuery。

在运行权限迁移工具之前，请验证您是否已满足以下前提条件：

* 您已在Google Cloud中创建了所需的主账号（用户、群组、服务账号）。
* 您已创建将用来托管所迁移数据的 Cloud Storage 托管文件夹或表。
* 运行该工具的用户有权管理 Cloud Storage 托管文件夹或表的角色。

您可以通过运行以下命令来应用权限：

```
./dwh-permissions-migration apply \
--permissions gs://MIGRATION_BUCKET/permissions.yaml
```

其中，`MIGRATION_BUCKET` 是包含迁移文件的 Cloud Storage 存储桶的名称。

### 以 Terraform 配置的形式应用权限

如需应用迁移的权限，您还可以将目标权限文件转换为 Terraform 基础设施即代码 (IaC) 配置，并将其应用于 Cloud Storage。

1. 验证您是否安装了 Python 3.7 或更高版本。
2. [创建新的虚拟环境](http://docs.python.org/3/library/venv.html)并将其激活。
3. 在 `permissions-migration/terraform` 目录中，使用以下命令通过 `requirements.txt` 文件安装依赖项：

   ```
   python -m pip install -r requirements.txt
   ```
4. 运行生成器命令：

   ```
   python tf_generator PATH LOCATION OUTPUT
   ```

   替换以下内容：

   * `PATH`：生成的 `permissions.yaml` 文件的路径。
   * `LOCATION`：脚本将在其中根据权限配置检查和创建文件夹的 [Cloud Storage 存储桶的位置](https://docs.cloud.google.com/storage/docs/locations?hl=zh-cn)。
   * `OUTPUT`：输出文件 `main.tf` 的路径。

## 规则集 YAML 文件

在将权限从 HDFS 或 Apache Ranger 迁移到Google Cloud时，规则集 YAML 文件将用于映射主账号和角色。规则集 YAML 文件使用通用表达式语言 (CEL) 来指定谓词（结果为布尔值）和表达式（结果为字符串）。

规则集 YAML 文件具有以下特点：

* 每种类型的映射规则会针对每个输入对象按顺序从上到下执行。
* CEL 表达式可以访问上下文变量，而上下文变量取决于规则集部分。例如，您可以使用 `user` 变量映射到源用户对象，并使用 `group` 变量映射到群组。
* 您可以使用 CEL 表达式或静态值来更改默认值。例如，在映射群组时，您可以将输出值 `type` 从默认值 `group` 替换为另一个值（例如 `serviceAccount`）。
* 必须至少有一条规则与每个输入对象匹配。

在 HDFS 或 Apache Ranger 权限迁移中，可以使用规则集 YAML 文件来定义主账号映射文件或角色映射文件。

### 规则集 YAML 文件中的映射规则

规则集 YAML 文件包含映射规则，用于指定在权限迁移期间如何将来源中的对象与目标中的对象进行匹配。映射规则可以包含以下部分或子句：

* `when`：用于限制规则适用性的谓词子句
  + 一个字符串，表示一个布尔值 CEL 表达式。值可以是 `true` 或 `false`
  + 仅当 `when` 子句的计算结果为 `true` 时，该规则才适用
  + 默认值为 `true`
* `map`：用于指定结果字段内容的子句。此子句的值取决于所处理对象的类型，可以定义为：
  + `expression`：用于以字符串形式进行计算
  + `value`：用于常量字符串
* `skip`：指定不应映射输入对象
  + 可以是 `true` 或 `false`
* `log`：有助于调试或开发规则的谓词子句
  + 一个字符串，表示一个布尔值 CEL 表达式。值可以是 `true` 或 `false`
  + 默认值为 `false`
  + 如果设置为 `true`，输出将包含一个执行日志，可用于监控或诊断执行中的问题

### 创建主账号规则集 YAML 文件

通过为 `email_address` 和 `type` 提供值，可以使用主账号映射文件生成[主账号标识符](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-cn)。

* 使用 `email_address` 指定 Google Cloud 主账号的邮箱。
* 使用 `type` 指定 Google Cloud中主账号的性质。`type` 的值可以是 `user`、`group` 或 `serviceAccount`。

规则中使用的任何 CEL 表达式都可以访问表示所处理对象的变量。变量中的字段基于 HDFS 或 Apache Ranger 元数据文件的内容。可用变量取决于规则集部分：

* 对于 `user_rules`，请使用变量 `user`
* 对于 `group_rules`，请使用变量 `group`
* 对于 `other_rules`，请使用变量 `other`
* 对于 `role_rules`，请使用变量 `role`

以下示例将 HDFS 中的用户映射到 Google Cloud中的用户，以用户名后跟 `@google.com` 作为其邮箱：

```
hdfs:
  user_rules:
    # Skip user named 'example'
    - when: "user.name == 'example'"
      skip: true
    # Map all other users to their name at google.com
    - when: "true"
      map:
        type:
          value: user
        email_address:
          expression: "user.name + '@google.com'"
```

#### 替换默认角色映射

如需使用非默认主账号，您可以使用规则集文件跳过或修改默认角色映射。

以下示例展示了如何跳过规则部分：

```
hdfs:
  user_rules:
    - skip: true
  group_rules:
    - skip: true
  other_rules:
    - skip: true
```

### 创建权限规则集 YAML 文件

权限规则集 YAML 文件用于生成目标权限映射文件。如需创建权限规则集 YAML 文件，请在权限规则集 YAML 中使用 CEL 表达式，将 HDFS 或 Apache Ranger 权限映射到 Cloud Storage 或 BigQuery 角色。

#### 默认角色映射

HDFS 文件角色由源文件权限决定：

* 如果设置了 `w` 位，则默认角色为 `writer`
* 如果设置了 `r` 位，则默认角色为 `reader`
* 如果未设置任何位，则角色为空

Ranger HDFS：

* 如果访问权限集包含 `write`，则默认角色为 `writer`
* 如果访问权限集包含 `read`，则默认角色为 `reader`
* 如果访问集不包含这两者，则角色为空

Ranger：

* 如果访问权限集包含 `update`、`create`、`drop`、`alter`、`index`、`lock`、`all`、`write` 或 `refresh`，则默认角色为 `writer`
* 如果访问权限集包含 `select` 或 `read`，则默认角色为 `reader`
* 如果访问权限集不包含上述任何权限，则角色为空

Cloud Storage：

* `roles/storage.objectUser` - 写入者
* `roles/storage.objectViewer` - 读取者

BigQuery：

* `roles/bigquery.dataOwner` - 写入者
* `roles/bigquery.dataViewer` - 读取者

以下示例展示了如何接受默认映射，而不在规则集 YAML 文件中进行任何更改：

```
ranger_hdfs_rules:
  - map: {}
```

#### 替换默认角色映射

如需使用非默认角色，您可以使用规则集文件跳过或修改默认角色映射。

以下示例展示了如何使用带有角色字段的 map 子句（使用值子句）替换默认角色映射：

```
ranger_hdfs_rules:
  - map:
    role:
      value: "roles/customRole"
```

### 合并权限映射

如果为同一目标资源生成了多个权限映射，则使用具有最广泛访问权限的映射。例如，如果 HDFS 规则向 HDFS 位置的主账号 `pa1` 授予读取者角色，而 Ranger 规则向同一位置的同一主账号授予写入者角色，则系统会分配写入者角色。

### CEL 表达式中的字符串引用

在 YAML 中，使用英文引号 `""` 封装整个 CEL 表达式。在 CEL 表达式中，使用英文单引号 `''` 来引用字符串。例如：

```
"'permissions-migration-' + group.name + '@google.com'"
```




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-02-12。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-02-12。"],[],[]]