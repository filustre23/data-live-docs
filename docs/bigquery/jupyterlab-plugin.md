* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 使用 BigQuery JupyterLab 插件

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

如需针对此功能请求反馈或支持，请发送邮件至 [bigquery-ide-plugin@google.com](mailto:bigquery-ide-plugin@google.com)。

本文档介绍了如何安装和使用 BigQuery JupyterLab 插件来执行以下操作：

* 探索 BigQuery 数据。
* 使用 BigQuery DataFrames API。
* 将 BigQuery DataFrames 笔记本部署到 [Cloud Composer](https://docs.cloud.google.com/composer/docs/concepts/overview?hl=zh-cn)。

BigQuery JupyterLab 插件包含 [Dataproc JupyterLab 插件](https://docs.cloud.google.com/dataproc-serverless/docs/quickstarts/jupyterlab-sessions?hl=zh-cn)的所有功能，例如创建 Dataproc Serverless 运行时模板、启动和管理笔记本、使用 Apache Spark 进行开发、部署代码以及管理资源。

## 安装 BigQuery JupyterLab 插件

如需安装和使用 BigQuery JupyterLab 插件，请按照以下步骤操作：

1. 在本地终端中，检查以确保您的系统上安装了 Python 3.8 或更高版本：

   ```
   python3 --version
   ```
2. [安装 gcloud CLI。](https://docs.cloud.google.com/sdk/docs/install?hl=zh-cn)
3. 在本地终端中，[初始化 gcloud CLI](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-cn)：

   ```
   gcloud init
   ```
4. 安装 Pipenv（一种 Python 虚拟环境工具）：

   ```
   pip3 install pipenv
   ```
5. 创建新的虚拟环境：

   ```
   pipenv shell
   ```
6. 在新虚拟环境中安装 JupyterLab：

   ```
   pipenv install jupyterlab
   ```
7. 安装 BigQuery JupyterLab 插件：

   ```
   pipenv install bigquery-jupyter-plugin
   ```
8. 如果安装的 JupyterLab 版本低于 4.0.0，则启用插件扩展程序：

   ```
   jupyter server extension enable bigquery_jupyter_plugin
   ```
9. 启动 JupyterLab：

   ```
   jupyter lab
   ```

   JupyterLab 会在浏览器中打开。

**注意**：在 macOS 上，如果在启动 JupyterLab 时在终端中收到 `SSL: CERTIFICATE_VERIFY_FAILED` 错误，请通过执行 `/Applications/Python 3.11/Install Certificates.command` 来更新您的 Python SSL 证书。
此文件位于 Python 主目录中。

## 更新项目和区域设置

默认情况下，您的会话会在您运行 `gcloud init` 时设置的项目和区域中运行。如需更改会话的项目和区域设置，请执行以下操作：

* 在 JupyterLab 菜单中，依次点击**设置 > Google BigQuery 设置**。

您必须重启插件，所做的更改才会生效。

## 探索数据

如需在 JupyterLab 中处理 BigQuery 数据，请执行以下操作：

1. 在 JupyterLab 边栏中，打开**数据集资源管理器**窗格：点击
2. 如需展开项目，请在**数据集资源管理器**窗格中点击项目名称旁边的 arrow\_right 展开箭头。

   **数据集资源管理器**窗格会显示项目中位于您为会话配置的 BigQuery 区域中的所有数据集。您可以通过多种方式与项目和数据集互动：

   * 如需查看数据集的相关信息，请点击相应数据集的名称。
   * 要显示数据集中的所有表，请点击数据集旁边的 arrow\_right 展开箭头。
   * 如需查看表的相关信息，请点击表的名称。
   * 如需更改项目或 BigQuery 区域，请[更新您的设置](#configure)。

## 执行笔记本

如需从 JupyterLab 查询 BigQuery 数据，请执行以下操作：

1. 如需打开启动器页面，请依次点击**文件 > 新启动器**。
2. 在 **BigQuery 笔记本**部分中，点击 **BigQuery DataFrames** 卡片。系统会打开一个新笔记本，其中介绍了如何开始使用 BigQuery DataFrames。

BigQuery DataFrames 笔记本支持在本地 Python 内核中进行 Python 开发。BigQuery DataFrames 操作在 BigQuery 上远程执行，但其余代码在本地计算机上执行。在 BigQuery 中执行操作时，查询作业 ID 和作业链接会显示在代码单元下方。

* 如需在 Google Cloud 控制台中查看作业，请点击**打开作业**。

## 部署 BigQuery DataFrames 笔记本

您可以使用 [Dataproc Serverless 运行时模板](https://docs.cloud.google.com/dataproc-serverless/docs/quickstarts/jupyterlab-sessions?hl=zh-cn#create_a_serverless_runtime_template)将 BigQuery DataFrames Notebook 部署到 Cloud Composer。您必须使用运行时版本 2.1 或更高版本。

1. 在 JupyterLab 笔记本中，点击 calendar\_month**作业调度器**。
2. 对于**作业名称**，为作业输入一个唯一的名称。
3. 在**环境**部分，输入要部署作业的 Cloud Composer 环境的名称。
4. 如果您的笔记本已参数化，请添加参数。
5. 输入[无服务器运行时模板](https://docs.cloud.google.com/dataproc-serverless/docs/quickstarts/jupyterlab-sessions?hl=zh-cn#create_a_serverless_runtime_template)的名称。
6. 如需处理笔记本执行故障，请为**重试计数**输入一个整数，为**重试延迟**输入一个值（以分钟为单位）。
7. 选择要发送哪些执行通知，然后输入收件人。

   系统会使用 Airflow SMTP 配置发送通知。
8. 为笔记本选择时间表。
9. 点击**创建**。

成功安排笔记本后，它会显示在所选 Cloud Composer 环境的预定作业列表中。

## 后续步骤

* 尝试学习 [BigQuery DataFrames 快速入门](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-cn)。
* 详细了解 [BigQuery DataFrames Python API](https://docs.cloud.google.com/bigquery/docs/reference/bigquery-dataframes?hl=zh-cn)。
* 使用 JupyterLab 进行 Dataproc 的[无服务器批处理和笔记本会话](https://docs.cloud.google.com/dataproc-serverless/docs/quickstarts/jupyterlab-sessions?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]