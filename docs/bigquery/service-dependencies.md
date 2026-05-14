Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理 BigQuery API 依附元件

本文說明 BigQuery 依附的 Google Cloud 服務和 API。此外，本文也會說明停用這些服務後，對 BigQuery 行為的影響。在專案中啟用或停用服務前，請先詳閱這份文件。

您建立的每個 Google Cloud 專案預設都會啟用部分服務。使用 BigQuery 的所有專案都會自動啟用其他 API。 Google Cloud 如要使用其餘服務的功能，必須先明確啟用這些服務。詳情請參閱下列資源：

* [預設啟用的服務](https://docs.cloud.google.com/service-usage/docs/enabled-service?hl=zh-tw#default)
* [啟用及停用服務](https://docs.cloud.google.com/service-usage/docs/enable-disable?hl=zh-tw)

本文適用對象為管理員。

## 預設啟用的服務

每個新專案預設都會啟用下列服務：Google Cloud

| **服務** | **哪些功能需要這項服務** | **停用這項服務的影響** |
| --- | --- | --- |
| `analyticshub.googleapis.com` | * [發布資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw) * [發布產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)和[管理訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw) * [資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw) | * 您無法建立或管理資料交換、刊登、資料無塵室或訂閱項目。 * 您無法搜尋及探索其他供應商建立的交易平台或房源。 * 已建立的訂閱項目會保留，但無法存取。 * 只要啟用 BigQuery API，即可存取已連結的資料集。 * 無法建立新訂閱項目 |
| `bigqueryconnection.googleapis.com` | * [聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)儲存在 BigQuery 外部的資料 * 外部資料表和資料集 * [BigQuery   中繼資料存放區](https://docs.cloud.google.com/bigquery/docs/about-bqms?hl=zh-tw) | * 你無法管理外部連線。 * 無法建立遠端模型。 * 您無法建立遠端函式。 * 您無法查詢 BigLake 資料表和物件資料表。 |
| `bigquerymigration.googleapis.com` | * [資料遷移評估](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw) * [SQL 查詢翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw) | * 您無法建立遷移工作或評估。 * 無法使用現有作業或評量。   **注意：**通常完成資料遷移後，即可停用這項服務。 |
| `bigquerydatapolicy.googleapis.com` | * [資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw) | * 您無法管理資料遮蓋政策。 * 資料遮蓋政策不會遭到刪除，但對套用資料遮蓋的資料表進行查詢時會失敗。 |
| `bigquerydatatransfer.googleapis.com` | * [排定資料移轉](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw) | * 無法管理排定的資料轉移作業。 * 現有的資料移轉作業會停止。 |
| `bigqueryreservation.googleapis.com` | * [以容量為基準的工作負載管理](https://docs.cloud.google.com/bigquery/docs/reservations-get-started?hl=zh-tw) | * 您無法建立或管理容量承諾、預留項目或指派項目。 * 無法監控運算單元用量。 * 無法進行災難復原容錯移轉。 * 停止自動調度運算單元。 |
| `bigquerystorage.googleapis.com` | * [串流資料擷取](https://docs.cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-tw) * [批次載入資料](https://docs.cloud.google.com/bigquery/docs/write-api-batch?hl=zh-tw) * [變更資料擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw) | * 您無法使用 [Storage Read API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 或 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) 存取 BigQuery 資料。 |
| `dataform.googleapis.com` | * Dataform 提供程式碼存放區，下列功能會運用這些存放區：  + [BigQuery 管道](https://docs.cloud.google.com/dataform/docs/quickstart-create-workflow?hl=zh-tw) + [儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw) + [Colab 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw) + [Dataform](https://docs.cloud.google.com/dataform/docs?hl=zh-tw) + [資料準備](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw) + [資料畫布](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw) | * 您無法建立管道、已儲存的查詢、Colab 筆記本、資料畫布、資料準備或 Dataform 專案。 * 現有的排定管道、筆記本或 Dataform 專案會停止運作。 * 現有的管道、已儲存的查詢、Colab 筆記本、資料畫布、資料準備或 Dataform 專案都將無法存取。 |
| `dataplex.googleapis.com` | * Knowledge Catalog 提供資料編目和管理功能，適用於下列項目：   + BigQuery Studio 中的資源瀏覽器   + BigQuery Studio SQL 編輯器中的自動完成功能   + [BigQuery sharing (舊稱 Analytics Hub) 搜尋項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)   + [商家檔案洞察資料](https://docs.cloud.google.com/bigquery/docs/data-profile-scan?hl=zh-tw)   + [資料品質掃描](https://docs.cloud.google.com/bigquery/docs/data-quality-scan?hl=zh-tw)   + [資料歷程](https://docs.cloud.google.com/dataplex/docs/use-lineage?hl=zh-tw#view-bq-lineage)檢視畫面   + [資料表和資料集洞察](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)   + [資料畫布](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw) | * 無法搜尋 BigQuery 資料資產。 * 無法搜尋共用房源。 * 您無法建立新的設定檔洞察資料、資料品質掃描或查詢建議，也無法存取先前建立的項目。 * 您無法在歷程圖中查看資料資產詳細資料。 * 您無法在資料畫布中搜尋資料資產。 |

### 停用 BigQuery API 的影響

停用 BigQuery API 時，也會停用下列服務，因為這些服務都依附於 BigQuery API：

* binaryauthorization.googleapis.com
* container.googleapis.com
* cloudapis.googleapis.com
* dataprep.googleapis.com
* servicebroker.googleapis.com
* telecomdatafabric.googleapis.com

## BigQuery Unified API 啟用的服務

BigQuery Unified API (`bigqueryunified.googleapis.com`) 包含各種 BigQuery 功能運作所需的精選服務。啟用 BigQuery Unified API 後，所有這些服務都會一併啟用。Google 可以更新這個集合中的服務，且這些服務會在啟用此 API 的專案中自動啟用。您可以停用個別服務和 API。

如要瞭解如何啟用 `bigqueryunified.googleapis.com`，請參閱「[啟用及停用服務](https://docs.cloud.google.com/service-usage/docs/enable-disable?hl=zh-tw)」。

| **服務** | **哪些功能需要這項服務** | **停用這項服務的影響** |
| --- | --- | --- |
| `aiplatform.googleapis.com` | * [Colab 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw) * [BigQuery ML 遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw) | * 您將無法執行筆記本。 * 現有的 BigQuery ML 遠端模型將停止運作。 * 你仍可編輯現有筆記本。 |
| `bigqueryunified.googleapis.com` | * 一鍵啟用本文列出的 BigQuery 相關服務，但不包括 **cloudaicompanion**、**composer** 和 **datalineage** API。 * 確保專案中已啟用新的 BigQuery 依附元件。 | * 專案不會自動啟用日後的依附元件。 |
| `compute.googleapis.com` | * Google Compute Engine 為 Managed Service for Apache Spark 和 Vertex AI 提供的所有功能，提供執行階段環境。 | * Colab 筆記本、遠端機器學習模型、Apache Spark、SparkSQL 和 PySpark 工作會停止。 * 原始碼仍可使用。 * Dataproc API 會停用。 |
| `dataproc.googleapis.com` | * [使用 Apache Spark 等開放原始碼引擎查詢資料。](https://docs.cloud.google.com/bigquery/docs/bqms-use-dataproc?hl=zh-tw) * [搭配 Managed Service for Apache Spark 使用 Spark SQL 或 PySpark。](https://docs.cloud.google.com/bigquery/docs/bqms-use-dataproc-serverless?hl=zh-tw) * [使用 Spark 預存程序。](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw) | * 您無法建立 Managed Service for Apache Spark 叢集，執行開放原始碼資料分析。 * 您無法執行 Managed Service for Apache Spark 工作負載。 * 您無法在 BigQuery 工作負載中執行 Spark。 |
| `datastream.googleapis.com` | * [提供變更資料擷取和複製至 BigQuery 的功能。](https://docs.cloud.google.com/datastream/docs/overview?hl=zh-tw) | * 所有資料串流都會暫停，且無法存取。 |

## 預設停用的服務

您必須手動啟用下列服務，才能使用對應功能：

| **服務** | **哪些功能需要這項服務** | **停用這項服務的影響** |
| --- | --- | --- |
| `cloudaicompanion.googleapis.com` | * Gemini in BigQuery 功能 | * 程式碼完成、生成和說明功能停止運作。  進一步瞭解如何[停用 Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw#turn-off)。 |
| `composer.googleapis.com` | * [排定工作負載](https://docs.cloud.google.com/bigquery/docs/orchestrate-workloads?hl=zh-tw) | * 現有的 Managed Service for Apache Airflow DAG 不會列在「Scheduling」(排程) 頁面上，且會停止。 * 現有的 Managed Airflow 環境會停止運作，並傳回錯誤狀態。 |
| `datalineage.googleapis.com` | * 擷取及查看[資料歷程](https://docs.cloud.google.com/dataplex/docs/use-lineage?hl=zh-tw#view-bq-lineage) | * 系統未擷取專案的資料沿襲。 * 您無法查看歷程圖。 |

## 手動啟用 BigQuery 程式碼資產

如要在 BigQuery 中管理程式碼資產 (例如筆記本和儲存的查詢)，您必須啟用下列 API：

* Compute Engine API
* Dataform API
* Vertex AI API

在 2024 年 3 月前，這些 API 預設不會自動啟用。如果您在 2024 年 3 月前有自動化指令碼，且這些指令碼依賴這些 API 的狀態，則可能需要更新。如果已啟用這些 API，BigQuery 的「Explorer」窗格中會顯示新的「Notebooks」和「Queries」資料夾。

### 事前準備

如要手動啟用程式碼資產管理功能，您必須具備 Identity and Access Management (IAM) 的[擁有者角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#legacy-basic) (`roles/owner`)。

### 手動啟用 BigQuery 程式碼資產

如要為程式碼資產啟用必要的 API 依附元件，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 **Studio** 的編輯器窗格分頁列中，按一下「+」符號旁的向下箭頭 arrow\_drop\_down，將指標懸停在「筆記本」上，然後選取「空白筆記本」。
3. 按一下「Enable APIs」。

   如果沒有看到這個選項，請檢查您是否具備必要的 IAM [擁有者角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#legacy-basic) (`roles/owner`)。如果開啟的是空白筆記本，表示您已啟用必要的 API。
4. 在「啟用核心功能」窗格的「核心功能 API」部分，執行下列操作：

   1. 如要啟用資料串流、排程和筆記本的所有 BigQuery 依附元件，請按一下「BigQuery Unified API」旁的「啟用」。
   2. 選用：如要選擇要啟用的 API，請按一下「查看及啟用個別 API」，然後按一下要啟用 API 旁的「啟用」。
   3. 啟用 API 後，請按一下「下一步」。
5. 選用：在「權限」部分設定使用者權限：

   * 如要授予主體建立程式碼資產的權限，以及讀取、編輯和設定所建立程式碼資產的權限，請在「BigQuery Studio 使用者」欄位中輸入使用者或群組名稱。
   * 如要授予主體讀取、編輯及設定所有共用程式碼資產權限的能力，請在「BigQuery Studio 管理員」欄位中輸入使用者或群組名稱。
6. 點選「下一步」。
7. 選用：在「其他 API」部分，按一下「全部啟用」，啟用使用 [BigQuery DataFrames](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw) 建立 BigQuery 遠端程序的 API。
8. 如果選擇不啟用其他 API，請按一下「關閉」，關閉「啟用核心功能」窗格。

### 限制程式碼資產的存取權

如要避免啟用其他 API，請設定[限制服務使用情形機構政策限制](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-resources?hl=zh-tw)。您隨時可以[關閉選取的 API](https://docs.cloud.google.com/service-usage/docs/enable-disable?hl=zh-tw#disabling)。

## 後續步驟

* 如要瞭解如何管理 Google Cloud 服務，請參閱「[啟用及停用服務](https://docs.cloud.google.com/service-usage/docs/enable-disable?hl=zh-tw)」。
* 如要瞭解如何透過機構政策限制，以精細程度管理 API 存取權，請參閱[限制資源用量](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-resources?hl=zh-tw)。
* 如要瞭解如何透過 BigQuery 的 Identity and Access Management (IAM) 角色和權限控管服務存取權，請參閱「[BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]