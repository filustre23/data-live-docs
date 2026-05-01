* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 从 Teradata 迁移到 BigQuery：概览

本文档提供了更多信息，可帮助您了解在使用 BigQuery Data Transfer Service 将架构和数据从 Teradata 迁移到 [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn) 时需要做出的决策。
如需了解 Teradata 迁移过程，请参阅[从 Teradata 迁移到 BigQuery 简介](https://docs.cloud.google.com/bigquery/docs/migration/teradata-migration-intro?hl=zh-cn)。

迁移架构和数据通常是将数据仓库从其他平台迁移到 BigQuery 时所需执行的多个步骤之一。如需了解一般迁移过程，请参阅[概览：将数据仓库迁移到 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-cn)。

您还可以使用[批量 SQL 转换](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-cn)来批量迁移 SQL 脚本，或使用[交互式 SQL 转换](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-cn)来转换临时查询。这两种 SQL 转换服务都全面支持 Teradata SQL。

## 概览

您可以结合使用 BigQuery Data Transfer Service 和特殊的迁移代理，将架构和数据从 Teradata 复制到 BigQuery。连接到本地数据仓库的迁移代理会与 BigQuery Data Transfer Service 通信，以便将表从数据仓库复制到 BigQuery。

以下步骤描述了迁移过程的工作流：

1. 下载迁移代理。
2. 在 BigQuery Data Transfer Service 中配置转移作业。
3. 运行转移作业，将表架构和数据从数据仓库复制到 BigQuery。
4. 可选。使用 Google Cloud 控制台监控转移作业。

## 转移作业配置

您可以配置转移作业，以最大限度满足您的需求。在设置从 Teradata 到 BigQuery 的数据转移作业之前，请考虑以下部分中介绍的配置选项并确定要使用的设置。根据您选择的设置，您可能需要满足一些前提条件才能开始执行转移作业。

对于大多数系统，尤其是那些具有大型表的系统，您可以按照以下步骤获得最佳性能：

1. 对 Teradata 表进行分区。
2. 使用 [Teradata Parallel Transporter (TPT)](https://docs.teradata.com/r/Teradata-Parallel-Transporter-User-Guide/February-2022/Introduction-to-Teradata-PT/High-Level-Description) 执行[提取](#extraction_method)操作。
3. 创建[自定义架构文件](#custom_schema_file)并配置目标 BigQuery 聚簇和分区列。

这样，迁移代理就可以逐个分区执行提取操作，这是最高效的做法。

### 提取方法

BigQuery Data Transfer Service 支持两种提取方法，使用这两种方法都可将数据从 Teradata 转移到 BigQuery：

* **使用 [Teradata Parallel Transporter (TPT)](https://docs.teradata.com/r/Teradata-Parallel-Transporter-User-Guide/February-2022/Introduction-to-Teradata-PT/High-Level-Description) *tbuild* 实用程序**。这是推荐的方法。使用 TPT 通常可以加快数据提取过程。

  在此模式下，迁移代理会尝试使用按分区分布的数据行计算提取批次。对于每个批次，代理都会发出并执行一个 TPT 提取脚本，从而生成一组以竖线分隔的文件。代理会将这些文件上传到 Cloud Storage 存储桶，之后转移作业会用到这些文件。将文件上传到 Cloud Storage 后，迁移代理便会从本地文件系统中删除这些文件。

  如果您在**没有**分区列的情况下使用 TPT 提取方法，系统会提取整个表。如果您在**具有**分区列的情况下使用 TPT 提取方法，代理会提取分区集。

  在此模式下，迁移代理不会限制提取的文件在本地文件系统上占用的空间量。确保本地文件系统的空间大于最大分区或最大表的大小，具体取决于您是否指定了分区列。

  **使用 [Cloud Storage 的访问模块](https://docs.teradata.com/r/Enterprise_IntelliFlex_Lake_VMware/Teradata-Tools-and-Utilities-Access-Module-Reference-20.00/Teradata-Access-Module-for-GCS/Overview-of-the-Teradata-Access-Module-for-GCS)**。此方法无需在本地文件系统上使用中间存储空间，从而提高了运行代理的虚拟机的性能并降低了资源利用率。此方法使用适用于 Cloud Storage 的 Teradata 访问模块将数据直接导出到 Cloud Storage。如需使用此功能，虚拟机上运行的 Teradata 工具必须是 17.20 以上的版本。Teradata 工具可以单独升级，而无需更改 Teradata 实例版本。
* **搭配使用 JDBC 驱动程序和 FastExport 连接进行提取。**如果提取的文件可用的本地存储空间存在限制，或者由于某种原因您无法使用 TPT，那么请使用该提取方法。

  在此模式下，迁移代理会将表提取到本地文件系统上的 AVRO 文件集合中。代理会将这些文件上传到 Cloud Storage 存储桶，之后转移作业会用到这些文件。将文件上传到 Cloud Storage 后，迁移代理便会从本地文件系统中删除这些文件。

  在此模式下，您可以限制本地文件系统上的 AVRO 文件所占用的空间量。如果超出此限制，系统会暂停提取，直到迁移代理上传和删除现有 AVRO 文件来释放空间。

### 架构标识

您可以通过多种方式定义架构。在从 Teradata 到 BigQuery 的数据转移期间，BigQuery Data Transfer Service 提供自动架构检测和[数据类型映射](https://docs.cloud.google.com/bigquery/docs/migration/teradata-sql?hl=zh-cn#data_types)。您还可以使用转换引擎获取数据类型映射，也可以选择指定自定义架构文件。

#### 默认架构检测

**预览版**

此功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版功能“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需就此功能获得支持或提供反馈，请发送邮件至 [bq-dts-migration@google.com](mailto:bq-dts-migration@google.com)。

如果您未指定任何架构配置，BigQuery Data Transfer Service 会在数据转移期间自动检测 Teradata 源表的架构，并将数据类型映射到相应的 BigQuery 数据类型。如需详细了解默认数据类型映射，请参阅[数据类型](https://docs.cloud.google.com/bigquery/docs/migration/teradata-sql?hl=zh-cn#data_types)。

#### 将转换引擎输出用于架构

**预览版**

此功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版功能“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需就此功能获得支持或提供反馈，请发送邮件至 [bq-dts-migration@google.com](mailto:bq-dts-migration@google.com)。

在将 Teradata 表迁移到 BigQuery 期间，BigQuery Data Transfer Service 会使用 BigQuery 转换引擎的输出进行架构映射。如需使用此选项，请确保满足以下前提条件：

1. 生成要转换的元数据。执行转储工具以生成用于转换的元数据，并遵循 Teradata 源指南。如需了解详情，请参阅[生成元数据以进行转换和评估](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-cn)。
2. 将生成的元数据文件（例如 `metadata.zip`）上传到 Cloud Storage 存储桶。此存储桶用作转换引擎的输入位置。
3. 启动批量转换作业，以创建 BigQuery Data Transfer Service 映射，该映射定义了目标 BigQuery 表的架构。如需了解如何执行此操作，请参阅[创建批量转换](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-cn#create_a_batch_translation)。
   以下示例通过指定 `target_types = "dts_mapping"` 生成 BigQuery Data Transfer Service 映射：

   ```
   curl -d "{
   \"name\": \"teradata_2_bq_translation\",
    \"displayName\": \"Teradata to BigQuery Translation\",
    \"tasks\": {
        string: {
          \"type\": \"Teradata2BigQuery_Translation\",
          \"translation_details\": {
              \"target_base_uri\": \"gs://your_translation_output_bucket/output\",
              \"source_target_mapping\": {
                \"source_spec\": {
                    \"base_uri\": \"gs://your_metadata_bucket/input\"
                }
              },
              \"target_types\": \"metadata\",
          }
        }
    },
    }" \
    -H "Content-Type:application/json" \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -X POST https://bigquerymigration.googleapis.com/v2alpha/projects/your_project_id/locations/your_location/workflows
   ```

   您可以在 Google Cloud 控制台中查看批量转换作业的状态，方法是依次前往 **BigQuery** -> **SQL 转换**。完成后，映射文件会存储在 `target_base_uri` 标志中指定的 Cloud Storage 位置。

   如需生成令牌，请使用 `gcloud auth print-access-token` 命令或范围为 `https://www.googleapis.com/auth/cloud-platform` 的 [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/?hl=zh-cn)。
4. 在 Teradata 数据转移配置中，指定在其中存储上一步中的映射文件的 Cloud Storage 文件夹的路径。BigQuery Data Transfer Service 会使用此映射来定义目标 BigQuery 表的架构。

#### 自定义架构文件

我们建议在以下情况下指定自定义架构：

* 如果您需要捕获表的重要信息（如分区），则此类信息可能会在迁移过程中丢失。

  例如，[增量转移](#incremental)应指定架构文件，以便后续转移中的数据在加载到 BigQuery 时得到正确分区。如果没有架构文件，每次运行转移作业时，BigQuery Data Transfer Service 都会使用要转移的源数据自动应用表架构，并且有关分区、聚簇、主键和更改跟踪的所有信息都将丢失。
* 如果您需要在数据转移期间更改列名称或数据类型。

自定义架构文件是一个描述数据库对象的 JSON 文件。架构包含一组数据库，每个数据库包含一组表，每个表包含一组列。每个对象都有一个 `originalName` 字段，指示 Teradata 中的对象名称；以及一个 `name` 字段，指示 BigQuery 中该对象的目标名称。

列具有以下字段：

* `originalType`：指示 Teradata 中的列数据类型
* `type`：指示 BigQuery 中相应列的目标数据类型。
* `usageType`：有关系统使用列的方式的信息。支持以下使用类型：

  + `DEFAULT`：一个目标表中可以有多列标注此使用类型。此 `usageType` 表示该列在源系统中没有特殊用途。这是默认值。
  + `CLUSTERING`：您可以使用此使用类型在每个目标表中最多注释四列。聚簇的列顺序根据其在自定义架构中的显示顺序确定。您选择的列必须满足[限制条件](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-cn#create_an_empty_clustered_table_with_a_schema_definition)才能在 BigQuery 中进行聚簇。如果为同一表指定了 `PARTITIONING` 字段，BigQuery 将使用这些列创建聚簇表。
  + `PARTITIONING`：您只能使用此使用类型注释每个目标表中的一列。此列在用于包含 `tables` 对象的[分区](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-cn)表定义中使用。您只能将此使用类型用在具有 `TIMESTAMP` 或 `DATE` 数据类型的列。
  + `COMMIT_TIMESTAMP`：您只能使用此使用类型注释每个目标表中的一列。使用此 `usageType` 来标识[增量更新](#incremental)的更新时间戳列。此列将用于提取自上次转移作业运行后创建或更新的行。您只能将此使用类型用在具有 `TIMESTAMP` 或 `DATE` 数据类型的列。
  + `PRIMARY_KEY`：您可以使用此使用类型在每个目标表中为列添加注解。使用此使用类型可只将一个列标识为主键，或者在复合键的情况下，对多个列使用相同的使用类型可标识表的唯一实体。这些列与 `COMMIT_TIMESTAMP` 搭配使用，可提取自上次转移作业运行后创建或更新的行。

您可以手动创建一个自定义架构文件，如以下示例所示，也可以让迁移代理在您初始化代理时为您生成一个自定义架构文件。

在此示例中，用户要迁移 `tpch` 数据库中称为 `orders` 且具有以下表定义的 Teradata 表：

```
  CREATE SET TABLE TPCH.orders ,FALLBACK ,
      NO BEFORE JOURNAL,
      NO AFTER JOURNAL,
      CHECKSUM = DEFAULT,
      DEFAULT MERGEBLOCKRATIO,
      MAP = TD_MAP1
      (
        O_ORDERKEY INTEGER NOT NULL,
        O_CUSTKEY INTEGER NOT NULL,
        O_ORDERSTATUS CHAR(1) CHARACTER SET LATIN CASESPECIFIC NOT NULL,
        O_TOTALPRICE DECIMAL(15,2) NOT NULL,
        O_ORDERDATE DATE FORMAT 'yyyy-mm-dd' NOT NULL,
        O_ORDERPRIORITY CHAR(15) CHARACTER SET LATIN CASESPECIFIC NOT NULL,
        O_CLERK CHAR(15) CHARACTER SET LATIN CASESPECIFIC NOT NULL,
        O_SHIPPRIORITY INTEGER NOT NULL,
        O_COMMENT VARCHAR(79) CHARACTER SET LATIN CASESPECIFIC NOT NULL)
  UNIQUE PRIMARY INDEX ( O_ORDERKEY );
```

迁移到 BigQuery 时，用户希望使用以下更改配置架构：

* 将 `O_CUSTKEY` 列重命名为 `O_CUSTOMERKEY`
* 将 `O_ORDERDATE` 标识为分区列

以下示例是一个用于配置这些设置的自定义架构：

```
{
  "databases": [
    {
      "name": "tpch",
      "originalName": "e2e_db",
      "tables": [
        {
          "name": "orders",
          "originalName": "orders",
          "columns": [
            {
              "name": "O_ORDERKEY",
              "originalName": "O_ORDERKEY",
              "type": "INT64",
              "originalType": "integer",
              "usageType": [
                "DEFAULT"
              ],
              "isRequired": true,
              "originalColumnLength": 4
            },
            {
              "name": "O_CUSTOMERKEY",
              "originalName": "O_CUSTKEY",
              "type": "INT64",
              "originalType": "integer",
              "usageType": [
                "DEFAULT"
              ],
              "isRequired": true,
              "originalColumnLength": 4
            },
            {
              "name": "O_ORDERSTATUS",
              "originalName": "O_ORDERSTATUS",
              "type": "STRING",
              "originalType": "character",
              "usageType": [
                "DEFAULT"
              ],
              "isRequired": true,
              "originalColumnLength": 1
            },
            {
              "name": "O_TOTALPRICE",
              "originalName": "O_TOTALPRICE",
              "type": "NUMERIC",
              "originalType": "decimal",
              "usageType": [
                "DEFAULT"
              ],
              "isRequired": true,
              "originalColumnLength": 8
            },
            {
              "name": "O_ORDERDATE",
              "originalName": "O_ORDERDATE",
              "type": "DATE",
              "originalType": "date",
              "usageType": [
                "PARTITIONING"
              ],
              "isRequired": true,
              "originalColumnLength": 4
            },
            {
              "name": "O_ORDERPRIORITY",
              "originalName": "O_ORDERPRIORITY",
              "type": "STRING",
              "originalType": "character",
              "usageType": [
                "DEFAULT"
              ],
              "isRequired": true,
              "originalColumnLength": 15
            },
            {
              "name": "O_CLERK",
              "originalName": "O_CLERK",
              "type": "STRING",
              "originalType": "character",
              "usageType": [
                "DEFAULT"
              ],
              "isRequired": true,
              "originalColumnLength": 15
            },
            {
              "name": "O_SHIPPRIORITY",
              "originalName": "O_SHIPPRIORITY",
              "type": "INT64",
              "originalType": "integer",
              "usageType": [
                "DEFAULT"
              ],
              "isRequired": true,
              "originalColumnLength": 4
            },
            {
              "name": "O_COMMENT",
              "originalName": "O_COMMENT",
              "type": "STRING",
              "originalType": "varchar",
              "usageType": [
                "DEFAULT"
              ],
              "isRequired": true,
              "originalColumnLength": 79
            }
          ]
        }
      ]
    }
  ]
}
```

### 按需转移或增量转移

将数据从 Teradata 数据库实例迁移到 BigQuery 时，BigQuery Data Transfer Service 既支持完整转移（按需转移），也支持周期性转移（增量转移）。您可以在[设置转移作业](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-cn#set_up_a_transfer)时，在时间安排选项中将转移指定为按需转移或增量转移。

* 按需转移：使用此模式可对架构和数据执行从 Teradata 到 BigQuery 的完整快照迁移。
* 计划转移：使用此模式可执行完整快照，并定期将新数据和修改后的数据（增量数据）从 Teradata 迁移到 BigQuery。增量转移需要自定义架构，以便在以下任一应用场景中为列添加注解：

  + 仅使用 `COMMIT_TIMESTAMP` 使用类型为列添加注解：在此转移中，Teradata 中的新行或修改后的行会附加到 BigQuery 中的数据。BigQuery 表中更新后的行可能包含具有旧值和新值的重复行。
  + 使用 `COMMIT_TIMESTAMP` 和 `PRIMARY_KEY` 使用类型为列添加注解：在此转移中，新行会进行附加，修改后的行会更新到 BigQuery 中的相应行。在 `PRIMARY_KEY` 中定义的列用于在 BigQuery 中保持数据的唯一性。
  + 架构中定义的 `PRIMARY_KEY` 列不必是 Teradata 表中的 `PRIMARY_KEY`。它可以是任意列，但必须包含唯一的数据。

#### 增量转移

在增量转移中，首次转移始终在 BigQuery 中创建表快照。所有后续增量转移都将遵循如下所述的自定义架构文件中定义的注解。

对于每次转移作业运行，系统都会保存转移作业运行的时间戳。对于每次后续转移作业运行，代理会收到上次转移作业运行的时间戳 (T1) 和当前转移作业运行开始的时间戳 (T2)。

对于初始运行后的转移，迁移代理将使用以下每个表逻辑提取数据：

* 如果架构文件中的表对象没有使用类型为 `COMMIT_TIMESTAMP` 的列，则跳过该表。
* 如果表中有使用类型为 `COMMIT_TIMESTAMP` 的列，系统会提取时间戳介于 T1 和 T2 之间的所有行并将其附加到 BigQuery 中的现有表。
* 如果表中有使用类型为 `COMMIT_TIMESTAMP` 的列和使用类型为 `PRIMARY_KEY` 的列，系统会提取时间戳介于 T1 和 T2 之间的所有行。在 BigQuery 中的现有表中，所有新行会进行附加，而修改后的行会进行更新。

**注意**：从 Teradata 进行增量迁移不支持将已删除的行与 BigQuery 同步。

以下是用于增量转移的示例架构文件。

仅包含 `COMMIT_TIMESTAMP` 的架构

```
{
  "databases": [
    {
      "name": "abc_db",
      "originalName": "abc_db",
      "tables": [
        {
          "name": "abc_table",
          "originalName": "abc_table",
          "columns": [
            {
              "name": "Id",
              "originalName": "Id",
              "type": "INT64",
              "originalType": "integer",
              "originalColumnLength": 4,
              "usageType": [
                "DEFAULT"
              ],
              "isRequired": true
            },
            {
              "name": "timestamp",
              "originalName": "timestamp",
              "type": "TIMESTAMP",
              "originalType": "timestamp",
              "originalColumnLength": 26,
              "usageType": [
                "COMMIT_TIMESTAMP"
              ],
              "isRequired": false
            }
          ]
        }
      ]
    }
  ]
}
```

包含 `COMMIT_TIMESTAMP` 且将一个列 (Id) 作为 `PRIMARY_KEY` 的架构

```
{
  "databases": [
    {
      "name": "abc_db",
      "originalName": "abc_db",
      "tables": [
        {
          "name": "abc_table",
          "originalName": "abc_table",
          "columns": [
            {
              "name": "Id",
              "originalName": "Id",
              "type": "INT64",
              "originalType": "integer",
              "originalColumnLength": 4,
              "usageType": [
                "PRIMARY_KEY"
              ],
              "isRequired": true
            },
            {
              "name": "timestamp",
              "originalName": "timestamp",
              "type": "TIMESTAMP",
              "originalType": "timestamp",
              "originalColumnLength": 26,
              "usageType": [
                "COMMIT_TIMESTAMP"
              ],
              "isRequired": false
            }
          ]
        }
      ]
    }
  ]
}
```

包含 `COMMIT_TIMESTAMP` 且将复合键 (Id + Name) 作为 `PRIMARY_KEY` 的架构

```
{
  "databases": [
    {
      "name": "abc_db",
      "originalName": "abc_db",
      "tables": [
        {
          "name": "abc_table",
          "originalName": "abc_table",
          "columns": [
            {
              "name": "Id",
              "originalName": "Id",
              "type": "INT64",
              "originalType": "integer",
              "originalColumnLength": 4,
              "usageType": [
                "PRIMARY_KEY"
              ],
              "isRequired": true
            },
            {
              "name": "Name",
              "originalName": "Name",
              "type": "STRING",
              "originalType": "character",
              "originalColumnLength": 30,
              "usageType": [
                "PRIMARY_KEY"
              ],
              "isRequired": false
            },
            {
              "name": "timestamp",
              "originalName": "timestamp",
              "type": "TIMESTAMP",
              "originalType": "timestamp",
              "originalColumnLength": 26,
              "usageType": [
                "COMMIT_TIMESTAMP"
              ],
              "isRequired": false
            }
          ]
        }
      ]
    }
  ]
}
```

下表介绍了迁移代理如何处理增量转移中的数据定义语言 (DDL) 和数据操纵语言 (DML) 操作。

| Teradata 操作 | 类型 | Teradata 到 BigQuery 的支持 |
| --- | --- | --- |
| `CREATE` | DDL | 系统会在 BigQuery 中创建表的新完整快照。 |
| `DROP` | DDL | 不支持 |
| `ALTER` (`RENAME`) | DDL | 系统会在 BigQuery 中为重命名的表创建新的完整快照。上一个快照不会从 BigQuery 中删除。用户不会收到重命名表的通知。 |
| `INSERT` | DML | 新的行会添加到 BigQuery 表中。 |
| `UPDATE` | DML | 如果仅使用 `COMMIT_TIMESTAMP`，相应行会作为新行附加到 BigQuery 表，类似于 `INSERT` 操作。如果同时使用 `COMMIT_TIMESTAMP` 和 `PRIMARY_KEY`，相应行会进行更新，类似于 `UPDATE` 操作。 |
| `MERGE` | DML | 不受支持。请参阅 `INSERT`、`UPDATE` 和 `DELETE`。 |
| `DELETE` | DML | 不支持 |

## 位置注意事项

您的 Cloud Storage 存储桶必须位于与 BigQuery 中目标数据集的区域或多区域兼容的区域或多区域中。

* 如果您的 BigQuery 数据集位于多区域，则包含您要转移的数据的 Cloud Storage 存储桶必须位于同一多区域或该多区域内的位置。例如，如果您的 BigQuery 数据集位于 `EU` 多区域，则 Cloud Storage 存储桶可以位于欧盟内的 `europe-west1` 比利时区域。
* 如果您的数据集位于单个区域，则 Cloud Storage 存储桶必须位于同一区域。例如，如果您的数据集位于 `asia-northeast1` 东京区域，则您的 Cloud Storage 存储桶不能位于 `ASIA` 多区域。

如需详细了解转移和区域，请参阅[数据集位置和转移](https://docs.cloud.google.com/bigquery/docs/dts-locations?hl=zh-cn)。

## 价格

使用 BigQuery 进行数据转移是免费的。但是，使用此服务可能会产生 Google 之外的费用，如平台出站数据传输费用。

* 提取数据、将数据上传到 Cloud Storage 存储桶然后将数据加载到 BigQuery 都是免费的。
* 数据上传到 BigQuery 后，系统**不会**自动将其从您的 Cloud Storage 存储桶中删除。请考虑手动删除 Cloud Storage 存储桶中的数据，以避免额外的存储开销。请参阅 [Cloud Storage 价格](https://cloud.google.com/storage/pricing?hl=zh-cn)。
* 您必须遵循加载作业适用的标准 BigQuery [配额和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn#load_jobs)。
* 系统会对增量注入 upsert 操作应用标准 DML BigQuery [配额和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn#data-manipulation-language-statements)。
* 数据转移到 BigQuery 后，您需要按标准 BigQuery [存储](https://cloud.google.com/bigquery/pricing?hl=zh-cn#storage)和[计算](https://cloud.google.com/bigquery/pricing?hl=zh-cn#analysis_pricing_models)价格付费。
* 如需了解详情，请参阅我们的转移作业[价格页面](https://cloud.google.com/bigquery/pricing?hl=zh-cn#data-transfer-service-pricing)。

## 限制

* 系统完全支持一次性按需转移。
  仅支持部分[增量转移中的 DDL/DML 操作](#ddldml_operations_in_incremental_transfers)。
* 在数据转移期间，数据将被提取到本地文件系统上的目录中。因此，请确保本地文件系统有足够的可用空间。
  + 使用 FastExport 提取模式时，您可以设置要使用的最大存储空间以及由迁移代理强制施加的严格限制。[设置从 Teradata 到 BigQuery 的转移作业](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-cn#set_up_a_transfer)时，请在[迁移代理的配置文件](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-cn#initialize_the_migration_agent)中设定 `max-local-storage` 设置。
  + 使用 TPT 提取方法时，请确保文件系统有足够的可用空间 - 大于 Teradata 实例中的最大表分区。
* BigQuery Data Transfer Service 会自动转换架构（如果您不提供自定义架构文件）并将 Teradata 数据转移到 BigQuery。
  数据会[从 Teradata 映射到 BigQuery 类型](#teradata_mapping)。
* 文件加载到 BigQuery 后，系统**不会**自动从您的 Cloud Storage 存储桶中删除文件。将数据加载到 BigQuery 后，请考虑手动从您的 Cloud Storage 存储桶中删除这些数据，以免产生额外的存储费用。请参阅[价格](#pricing)。
* 提取的速度受 JDBC 连接的限制。
* 从 Teradata 中提取的数据**不会**加密。请采取适当的措施来限制对本地文件系统中的提取文件的访问，并确保 Cloud Storage 存储桶受到妥善保护。
* 其他数据库资源（例如存储过程、已保存的查询、视图和用户定义的函数）**不会**转移，不在此服务范围之内。
* 增量转移不支持硬删除。增量转移不会将 Teradata 中已删除的任何行与 BigQuery 同步。

## 后续步骤

* 查看[将 Teradata 迁移到 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-cn) 的分步说明。
* 尝试 Teradata 到 BigQuery 的[测试迁移](https://docs.cloud.google.com/bigquery/docs/migration/teradata-tutorial?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]