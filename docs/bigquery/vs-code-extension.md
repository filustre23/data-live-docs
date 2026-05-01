* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 使用 Google Cloud for Visual Studio Code 扩展程序

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需就此预览版功能提供反馈或提出问题，请联系 [bigquery-ide-plugin@google.com](mailto:bigquery-ide-plugin@google.com)。

借助 Google Cloud [Visual Studio Code (VS Code)](https://code.visualstudio.com/) 扩展程序，您可以在 VS Code 中执行以下操作：

* 开发和执行 BigQuery 笔记本。
* 浏览、检查和预览 BigQuery 数据集。

## 准备工作

1. 在本地终端中，检查以确保您的系统上安装了 [Python 3.11](https://www.python.org/downloads/) 或更高版本：

   ```
   python3 --version
   ```
2. [安装 Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install?hl=zh-cn)。
3. 在本地终端中，[初始化 gcloud CLI](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-cn)：

   ```
   gcloud init
   ```
4. 配置默认项目：

   ```
   gcloud config set project PROJECT_ID
   ```

   将 `PROJECT_ID` 替换为您的默认项目。
5. 设置[应用默认凭证](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-cn)：

   ```
   gcloud auth application-default login
   ```
6. [下载并安装 VS Code](https://code.visualstudio.com/download)。
7. 打开 VS Code，然后在活动栏中点击**扩展程序**。
8. 使用搜索栏找到 **Jupyter** 扩展程序，然后点击**安装**。VS Code 中的 BigQuery 功能需要 Microsoft 的 Jupyter 扩展程序作为依赖项。

## 安装 Google Cloud 扩展程序

1. 打开 VS Code，然后在活动栏中点击**扩展程序**。
2. 使用搜索栏找到 **Google Cloud Code** 扩展程序，然后点击**安装**。
3. 如果出现提示，请重启 VS Code。

**Google Cloud Code** 图标现在会显示在活动栏中。

## 配置扩展程序

1. 打开 VS Code，然后在活动栏中点击 **Google Cloud Code**。
2. 打开 **BigQuery 笔记本**部分。
3. 点击**登录 Google Cloud**。系统会将您重定向，您可使用您的凭证登录。
4. 使用顶层应用任务栏，依次前往**代码 > 设置 > 设置 > 扩展程序**。
5. 找到 **Google Cloud Code**，然后点击**管理**图标以打开菜单。
6. 选择**设置**。
7. 对于 **Cloud Code：项目**设置，请输入您要用于执行笔记本和显示 BigQuery 数据集的Google Cloud 项目的名称。
8. 对于 **Cloud Code > Beta 版：BigQuery 区域**设置，输入 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn#supported_locations)。
   该扩展程序会显示来自此位置的数据集。

## 开发 BigQuery 笔记本

1. 打开 VS Code，然后在活动栏中点击 **Google Cloud Code**。
2. 打开 **BigQuery 笔记本**部分，然后点击 **BigQuery 笔记本**。系统会创建一个包含示例代码的新 `.ipynb` 文件，并在编辑器中打开该文件。
3. 在新笔记本中，点击**选择内核**，然后选择 Python 内核。
   BigQuery 笔记本需要本地 Python 内核才能执行。您可以创建新的虚拟环境，也可以使用现有虚拟环境。
4. 如果该库尚未安装在您的虚拟环境中，请安装 `bigframes` 客户端库：

   1. 打开**终端**窗口。
   2. 运行 `pip install bigframes` 命令。

您现在可以在 BigQuery 笔记本中编写和执行代码。

## 探索和预览 BigQuery 数据集

1. 打开 VS Code，然后在活动栏中点击 **Google Cloud Code**。
2. 如需查看指定项目和区域中的数据集和表，请打开 **BigQuery 数据集**部分。BigQuery 公共数据集也会显示。
3. 如需在编辑器中打开新标签页，请点击任意表名称。此标签页包含表详细信息、架构和预览。

## 价格

Visual Studio Code 扩展程序是免费的，但您需要为使用的任何Google Cloud 服务（BigQuery、Dataproc、Cloud Storage）付费。

## 后续步骤

* 详细了解 [BigQuery 中的笔记本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-cn)。
* 详细了解 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]