* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 从 Apache Hive 提取元数据以进行迁移

**预览版**

此功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版功能“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需就此功能获得支持或提供反馈，请发送邮件至 [bigquery-permission-migration-support@google.com](mailto:bigquery-permission-migration-support@google.com)。

本文档介绍了如何在运行 Apache Hive 数据或权限迁移之前使用 `dwh-migration-dumper` 工具提取必要的元数据。

本文档介绍了从以下数据源提取元数据的相关信息：

* Apache Hive
* Apache Hadoop 分布式文件系统 (HDFS)
* Apache Ranger
* Cloudera Manager
* Apache Hive 查询日志

## 准备工作

在使用 `dwh-migration-dumper` 工具之前，请执行以下操作：

### 安装 Java

您打算运行 `dwh-migration-dumper` 工具的服务器必须安装 Java 8 或更高版本。如果未安装，请从 [Java 下载页面](https://www.java.com/download/)下载并安装 Java。

### 所需权限

您指定用于将 `dwh-migration-dumper` 工具连接到源系统的用户账号必须具有从该系统读取元数据的权限。确认此账号具有适当的角色成员资格，可以查询您的平台可用的元数据资源。例如，`INFORMATION_SCHEMA` 是在多个平台中常见的元数据资源。

## 安装 `dwh-migration-dumper` 工具

如需安装 `dwh-migration-dumper` 工具，请按以下步骤操作：

1. 在要运行 `dwh-migration-dumper` 工具的机器上，从 [`dwh-migration-dumper` 工具 GitHub 代码库](https://github.com/google/dwh-migration-tools/releases/latest)下载 zip 文件。
2. 如需验证 `dwh-migration-dumper` 工具 ZIP 文件，请下载 [`SHA256SUMS.txt` 文件](https://github.com/google/dwh-migration-tools/releases/latest/download/SHA256SUMS.txt)并运行以下命令：

   ### Bash

   ```
   sha256sum --check SHA256SUMS.txt
   ```

   如果验证失败，请参阅[问题排查](#corrupted_zip_file)。

   ### Windows PowerShell

   ```
   (Get-FileHash RELEASE_ZIP_FILENAME).Hash -eq ((Get-Content SHA256SUMS.txt) -Split " ")[0]
   ```

   将 `RELEASE_ZIP_FILENAME` 替换为 `dwh-migration-dumper` 命令行提取工具版本的下载 ZIP 文件名，例如 `dwh-migration-tools-v1.0.52.zip`

   `True` 结果表示校验和验证成功。

   `False` 结果表示验证错误。确保校验和以及 ZIP 文件从同一发布版本下载并放在同一目录中。
3. 提取该 zip 文件。提取工具二进制文件位于通过提取 ZIP 文件创建的文件夹的 `/bin` 子目录中。
4. 更新 `PATH` 环境变量，以包含提取工具的安装路径。

## 提取元数据以进行迁移

选择以下选项之一，了解如何提取数据源的元数据：

### Apache Hive

按照 Apache Hive 部分中的步骤[从数据仓库中提取元数据和查询日志](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-cn#apache-hive)，提取 Apache Hive 元数据。然后，您可以将元数据上传到包含迁移文件的 Cloud Storage 存储桶。

### HDFS

运行以下命令，使用 `dwh-migration-dumper` 工具从 HDFS 中提取元数据。

```
dwh-migration-dumper \
  --connector hdfs \
  --host HDFS-HOST \
  --port HDFS-PORT \
  --output gs://MIGRATION-BUCKET/hdfs-dumper-output.zip \
  --assessment \
```

替换以下内容：

* `HDFS-HOST`：HDFS NameNode 主机名
* `HDFS-PORT`：HDFS NameNode 端口号。如果您使用的是默认 `8020` 端口，则可以跳过此参数。
* `MIGRATION-BUCKET`：您用于存储迁移文件的 Cloud Storage 存储桶。

此命令会将元数据从 HDFS 提取到 `MIGRATION-BUCKET` 目录中名为 `hdfs-dumper-output.zip` 的文件中。

从 HDFS 提取元数据时，存在以下几个已知限制：

* 此连接器中的某些任务是可选的，可能会失败，并在输出中记录全栈轨迹。只要所需任务已成功完成并生成了 `hdfs-dumper-output.zip`，您就可以继续进行 HDFS 迁移。
* 如果配置的线程池大小过大，提取过程可能会失败或运行速度低于预期。如果您遇到这些问题，建议您使用命令行参数 `--thread-pool-size` 减小线程池大小。

### Apache Ranger

运行以下命令，使用 `dwh-migration-dumper` 工具从 Apache Ranger 中提取元数据。

```
dwh-migration-dumper \
  --connector ranger \
  --host RANGER-HOST \
  --port 6080 \
  --user RANGER-USER \
  --password RANGER-PASSWORD \
  --ranger-scheme RANGER-SCHEME \
  --output gs://MIGRATION-BUCKET/ranger-dumper-output.zip \
  --assessment \
```

替换以下内容：

* `RANGER-HOST`：Apache Ranger 实例的主机名
* `RANGER-USER`：Apache Ranger 用户的用户名
* `RANGER-PASSWORD`：Apache Ranger 用户的密码
* `RANGER-SCHEME`：指定 Apache Ranger 使用的是 `http` 还是 `https`。默认值为 `http`。
* `MIGRATION-BUCKET`：您用于存储迁移文件的 Cloud Storage 存储桶。

您还可以包含以下可选标志：

* `--kerberos-auth-for-hadoop`：如果 Apache Ranger 受 Kerberos 保护，而不是受基本身份验证保护，则替换 `--user` 和 `--password`。您必须先运行 `kinit` 命令，然后再运行 `dwh-migration-dumper` 工具，才能使用此标志。
* `--ranger-disable-tls-validation`：如果 API 使用的 HTTPS 证书是自签名证书，请添加此标志。例如，使用 Cloudera 时。

此命令会将元数据从 Apache Ranger 提取到 `MIGRATION-BUCKET` 目录中名为 `ranger-dumper-output.zip` 的文件中。

### Cloudera

运行以下命令，使用 `dwh-migration-dumper` 工具从 Cloudera 提取元数据。

```
dwh-migration-dumper \
  --connector cloudera-manager \
  --url CLOUDERA-URL \
  --user CLOUDERA-USER \
  --password CLOUDERA-PASSWORD \
  --output gs://MIGRATION-BUCKET/cloudera-dumper-output.zip \
  --yarn-application-types APPLICATION-TYPES \
  --pagination-page-size PAGE-SIZE \
  --assessment \
```

替换以下内容：

* `CLOUDERA-URL`：Cloudera Manager 的网址
* `CLOUDERA-USER`：Cloudera 用户的用户名
* `CLOUDERA-PASSWORD`：Cloudera 用户的密码
* `MIGRATION-BUCKET`：您用于存储迁移文件的 Cloud Storage 存储桶。
* `APPLICATION-TYPES`：（可选）Hadoop YARN 中所有现有应用类型的列表。例如 `SPARK, MAPREDUCE`。
* `PAGE-SIZE`：（可选）指定从第三方服务（如 Hadoop YARN API）提取的数据量。默认值为 `1000`，表示每个请求 1,000 个实体。

此命令会将元数据从 Cloudera 提取到 `MIGRATION-BUCKET` 目录中名为 `dwh-migration-cloudera.zip` 的文件中。

### Apache Hive 查询日志

按照 Apache Hive 部分中的步骤[使用 `hadoop-migration-assessment` 日志记录钩子提取查询日志](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-cn#apache-hive)提取 Apache Hive 查询日志。然后，您可以将日志上传到包含迁移文件的 Cloud Storage 存储桶。

## 后续步骤

从 Hadoop 中提取元数据后，您可以使用这些元数据文件执行以下操作：

* [从 Hadoop 迁移权限](https://docs.cloud.google.com/bigquery/docs/hadoop-permissions-migration?hl=zh-cn)
* [安排 Hadoop 转移](https://docs.cloud.google.com/bigquery/docs/hadoop-transfer?hl=zh-cn)




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]