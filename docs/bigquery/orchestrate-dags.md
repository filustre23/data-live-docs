* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排定 Airflow DAG

本文說明如何透過 BigQuery 的「排程」頁面，從 [Managed Airflow 3](https://docs.cloud.google.com/composer/docs/composer-3/composer-overview?hl=zh-tw) 排程 [Airflow 有向無環圖 (DAG)](https://docs.cloud.google.com/composer/docs/composer-3/composer-overview?hl=zh-tw#about-airflow)，包括如何手動觸發 DAG，以及如何查看過去 DAG 執行的記錄和記錄檔。

## 關於在 BigQuery 中管理 Airflow DAG

BigQuery 的「排程」頁面提供相關工具，可排定在 Managed Airflow 3 環境中執行的 Airflow DAG。

您在 BigQuery 中排定的 Airflow DAG 會在專案中一或多個 Managed Airflow 環境中執行。BigQuery 的「排程」頁面會整合專案中所有 Airflow DAG 的資訊。

在 DAG 執行期間，Airflow 會排定並執行組成 DAG 的個別工作，順序由 DAG 定義。在 BigQuery 的「Scheduling」(排程) 頁面中，您可以查看過去 DAG 執行作業的狀態、瀏覽所有 DAG 執行作業和這些 DAG 執行作業中所有工作的詳細記錄，以及查看 DAG 的詳細資料。

**注意：** 您無法在 BigQuery 中管理 Managed Airflow 環境。如要管理環境 (例如建立環境、為 DAG 檔案安裝依附元件、上傳、刪除或變更個別 DAG)，請使用 Managed Airflow。

如要進一步瞭解 Airflow 的核心概念，例如 Airflow DAG、DAG 執行、任務或運算子，請參閱 Airflow 說明文件的「[核心概念](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html)」頁面。

如要進一步瞭解 Managed Airflow 環境，請參閱 Managed Airflow 說明文件中的「[Managed Airflow 3 總覽](https://docs.cloud.google.com/composer/docs/composer-3/composer-overview?hl=zh-tw)」頁面。

## 事前準備

1. 啟用 Cloud Composer API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=composer.googleapis.com&hl=zh-tw)
2. 確認 Google Cloud 專案至少有一個 Managed Airflow 3 環境，且至少已上傳一個 DAG 檔案：

* 如要開始使用 Airflow DAG，請按照「[在 Managed Airflow 3 中執行 Apache Airflow DAG](https://docs.cloud.google.com/composer/docs/composer-3/run-apache-airflow-dag?hl=zh-tw)」指南中的操作說明進行。在本指南中，您將建立具有預設設定的 Managed Airflow 3 環境、將 DAG 上傳至該環境，並確認 Airflow 是否執行 DAG。
* 如需將 Airflow DAG 上傳至 Managed Airflow 3 環境的詳細操作說明，請參閱「[新增及更新 DAG](https://docs.cloud.google.com/composer/docs/composer-3/manage-dags?hl=zh-tw)」。
* 如需建立 Managed Airflow 第 3 代環境的詳細操作說明，請參閱「[建立 Managed Airflow 環境](https://docs.cloud.google.com/composer/docs/composer-3/create-environments?hl=zh-tw)」。

### 所需權限

如要取得排定 Airflow DAG 時間所需的權限，請要求管理員授予您專案的下列 IAM 角色：

* 如要查看 Airflow DAG 及其詳細資料：
  [環境和 Storage 物件檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/composer?hl=zh-tw#composer.environmentAndStorageObjectViewer)  (`roles/composer.environmentAndStorageObjectViewer`)
* 如要觸發及暫停 Airflow DAG，請執行下列操作：
  「環境與 Storage 物件使用者」 (`roles/composer.environmentAndStorageObjectUser`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備排定 Airflow DAG 時間所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要排定 Airflow DAG 的執行時間，您必須具備下列權限：

* 如要查看 Airflow DAG 及其詳細資料：
   `composers.dags.list, composer.environments.list`
* 如要觸發及暫停 Airflow DAG：
   `composers.dags.list, composer.environments.list, composer.dags.execute`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 Managed Airflow 3 IAM，請參閱 Managed Airflow 說明文件中的「[使用 IAM 控管存取權](https://docs.cloud.google.com/composer/docs/composer-3/access-control?hl=zh-tw)」。

## 手動觸發 Airflow DAG

手動觸發 Airflow DAG 時，Airflow 會執行一次 DAG，不受 DAG 指定排程影響。

如要手動觸發所選的 Airflow DAG，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「Scheduling」(排程) 頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 執行下列其中一項操作：

   * 按一下所選 DAG 的名稱，然後在「DAG details」(DAG 詳細資料) 頁面上，按一下「Trigger DAG」(觸發 DAG)。
   * 在包含所選 DAG 的資料列中，按一下「Actions」欄中的 more\_vert「View actions」，然後按一下「Trigger DAG」。

## 查看 Airflow DAG 執行記錄和詳細資料

如要查看所選 Airflow DAG 的詳細資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「Scheduling」(排程) 頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選 DAG 的名稱。
3. 在「DAG details」(DAG 詳細資料) 頁面上，選取「Details」(詳細資料) 分頁標籤。
4. 如要查看過去的 DAG 執行作業，請選取「Runs」(執行作業) 分頁標籤。

   1. 選用：根據預設，「執行作業」分頁會顯示過去 10 天的 DAG 執行作業。如要依其他時間範圍篩選 DAG 執行作業，請在「10 days」(10 天) 下拉式選單中選取時間範圍，然後按一下「OK」(確定)。
   2. 選用：如要在所有 DAG 執行作業的清單中顯示其他資料欄和 DAG 執行作業詳細資料，請按一下「資料欄顯示選項」view\_column，然後選取資料欄並按一下「確定」。
   3. 如要查看所選 DAG 執行作業的詳細資料和記錄檔，請選取 DAG 執行作業。
5. 如要查看 DAG 的視覺化圖表 (含工作依附元件)，請選取「圖表」分頁標籤。

   1. 如要查看工作詳細資料，請在圖表中選取工作。
6. 如要查看 DAG 的原始碼，請選取「程式碼」分頁標籤。
7. 選用：如要重新整理顯示的資料，請按一下「重新整理」。

## 查看所有 Airflow DAG

如要查看Google Cloud 專案中所有 Managed Airflow 3 環境的 Airflow DAG，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「Scheduling」(排程) 頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 選用：如要顯示含有 DAG 詳細資料的其他資料欄，請按一下「資料欄顯示選項」view\_column，然後選取資料欄並按一下「確定」。

## 暫停 Airflow DAG

如要暫停所選 Airflow DAG，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「Scheduling」(排程) 頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 執行下列其中一項操作：

   * 按一下所選 DAG 的名稱，然後在「DAG details」(DAG 詳細資料) 頁面上，按一下「Pause DAG」(暫停 DAG)。
   * 在包含所選 DAG 的資料列中，按一下「動作」欄中的 more\_vert「查看動作」，然後按一下「暫停 DAG」。

## 疑難排解

如需排解 Airflow DAG 相關問題的操作說明，請參閱 Managed Airflow 說明文件中的「[排解 Airflow DAG 相關問題](https://docs.cloud.google.com/composer/docs/composer-3/troubleshooting-dags?hl=zh-tw)」。

## 後續步驟

* 進一步瞭解如何[編寫 Airflow DAG](https://docs.cloud.google.com/composer/docs/composer-3/write-dags?hl=zh-tw)。
* 進一步瞭解 [Managed Airflow 3 中的 Airflow](https://docs.cloud.google.com/composer/docs/composer-3/composer-overview?hl=zh-tw#about-airflow)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]