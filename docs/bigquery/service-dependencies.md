Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理 BigQuery API 依附元件

您可以瞭解各個 API 如何影響依賴這些 API 的 Google Cloud 功能，進而管理 BigQuery 行為。根據預設，您建立的每個 Google Cloud 專案都會啟用部分 API 服務
，而所有使用
BigQuery 的 Google Cloud 專案則會自動啟用其他 API 服務
。您必須明確啟用其餘 API 服務，才能使用其功能。

如果誤停用依附元件，可能會影響 BigQuery 功能。瞭解這些依附元件，在 Google Cloud 專案中啟用或停用服務時，做出明智決策。

## 預設啟用的服務

根據預設，每個新的Google Cloud 專案都會啟用下列服務：

| **服務** | **API 名稱** | **哪些功能需要這項設定** | **停用這項服務的影響** |
| --- | --- | --- | --- |
| BigQuery sharing | `analyticshub.googleapis.com` | * [發布資料交換作業](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw) * [發布產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)和[管理訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-subscriptions?hl=zh-tw) * [資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw) | * 無法建立或管理資料交換、清單、資料無塵室或訂閱項目。 * 您無法搜尋及探索其他供應商建立的交換作業或資訊。 * 建立的訂閱項目會保留，但無法存取。 * 只要啟用 BigQuery API，即可存取已連結的資料集。 * 無法建立新訂閱方案 |
| BigQuery Connection API | `bigqueryconnection.googleapis.com` | * 對儲存在 BigQuery 外部的資料儲存庫執行[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw) * 外部資料表和資料集 * [BigQuery   metastore](https://docs.cloud.google.com/bigquery/docs/about-bqms?hl=zh-tw) | * 無法管理外部連結。 * 無法建立遠端模型。 * 無法建立遠端函式。 * 無法查詢 BigLake 資料表和物件資料表。 |
| BigQuery 遷移服務 | `bigquerymigration.googleapis.com` | * [資料遷移評估](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw) * [SQL 查詢翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw) | * 無法建立遷移任務或評估。 * 無法使用現有工作或評量。   **注意：**完成資料遷移後，通常可以停用這項服務。 |
| BigQuery 資料政策 | `bigquerydatapolicy.googleapis.com` | * [資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw) | * 您無法管理資料遮蓋政策。 * 資料遮蓋政策不會刪除，但查詢套用資料遮蓋的資料表會失敗。 |
| BigQuery 資料移轉服務 | `bigquerydatatransfer.googleapis.com` | * [排定資料移轉作業](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw) | * 無法管理排定的資料移轉作業。 * 現有的資料移轉作業會停止。 |
| BigQuery Reservation API | `bigqueryreservation.googleapis.com` | * [依據容量管理工作負載](https://docs.cloud.google.com/bigquery/docs/reservations-get-started?hl=zh-tw) | * 您無法建立或管理運算資源承諾使用合約、預留項目或指派作業。 * 無法監控運算單元用量。 * 無法使用災難復原容錯移轉功能。 * 運算單元自動調度資源功能會停止。 |
| BigQuery Storage API | `bigquerystorage.googleapis.com` | * [串流資料擷取](https://docs.cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-tw) * [批次載入資料](https://docs.cloud.google.com/bigquery/docs/write-api-batch?hl=zh-tw) * [變更資料擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw) | * 您無法使用 [Storage Read API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 或 [Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) 存取 BigQuery 資料。 |
| Dataform | `dataform.googleapis.com` | * Dataform 提供程式碼存放區，可供下列功能使用：  + [BigQuery 管道](https://docs.cloud.google.com/dataform/docs/quickstart-create-workflow?hl=zh-tw) + [已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw) + [Colab 筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw) + [Dataform](https://docs.cloud.google.com/dataform/docs?hl=zh-tw) + [資料準備](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw) + [資料畫布](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw) | * 您無法建立管道、已儲存的查詢、Colab 筆記本、資料畫布、資料準備或 Dataform 專案。 * 現有的排定管道、筆記本或 Dataform 專案會停止。 * 現有的管道、已儲存的查詢、Colab 筆記本、資料畫布、資料準備或 Dataform 專案都將無法存取。 |
| Knowledge Catalog | `dataplex.googleapis.com` | * Knowledge Catalog 提供 Data Catalog 和管理功能，可供下列項目使用：   + BigQuery Studio 中的資源探索工具   + BigQuery Studio SQL 編輯器的自動完成功能   + [BigQuery sharing (舊稱 Analytics Hub) 搜尋項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)   + [商家檔案洞察](https://docs.cloud.google.com/bigquery/docs/data-profile-scan?hl=zh-tw)   + [資料品質掃描](https://docs.cloud.google.com/bigquery/docs/data-quality-scan?hl=zh-tw)   + 查看[資料歷程](https://docs.cloud.google.com/knowledge-catalog/docs/use-lineage?hl=zh-tw#view-lineage)   + [資料表和資料集深入分析](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)   + [資料畫布](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw) | * 無法搜尋 BigQuery 資料資產。 * 無法搜尋共用清單。 * 您無法建立新的設定檔洞察資料、資料品質掃描或查詢建議，也無法存取先前建立的項目。 * 您無法在歷程圖上查看資料資產詳細資料。 * 您無法在資料畫布中搜尋資料資產。 |

### 停用 BigQuery API 的影響

停用 BigQuery API 也會停用下列依賴 BigQuery API 的服務：

* 二進位授權 (`binaryauthorization.googleapis.com`)
* Google Kubernetes Engine (`container.googleapis.com`)
* Google Cloud API (`cloudapis.googleapis.com`)
* Dataprep by Trifacta (`dataprep.googleapis.com`)
* Open Service Broker for Google Cloud (`servicebroker.googleapis.com`)
* Telecom Data Fabric (`telecomdatafabric.googleapis.com`)

## BigQuery Unified API 啟用的服務

BigQuery Unified API (`bigqueryunified.googleapis.com`) 包含一系列精選服務，可讓各種 BigQuery 功能正常運作。啟用 BigQuery Unified API 後，這些服務會同時啟用。Google 可以更新這個集合中的服務，而這些服務會在啟用這個 API 的專案中自動啟用。您可以停用個別服務和 API。

如要瞭解如何啟用 `bigqueryunified.googleapis.com`，請參閱「[啟用及停用服務](https://docs.cloud.google.com/service-usage/docs/enable-disable?hl=zh-tw)」。

| **服務** | **API 名稱** | **哪些功能需要這項設定** | **停用這項服務的影響** |
| --- | --- | --- | --- |
| Vertex AI | `aiplatform.googleapis.com` | * [Colab 筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw) * [BigQuery ML 遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw) | * 無法執行筆記本。 * 任何現有的 BigQuery ML 遠端模型都會停止運作。 * 現有筆記本仍可編輯。 |
| BigQuery Unified API | `bigqueryunified.googleapis.com` | * 按一下即可啟用本文件列出的 BigQuery 依附服務，但不包括 **cloudaicompanion**、**composer** 和 **datalineage** API。 * 確保專案已啟用新的 BigQuery 依附元件。 | * 系統不會在專案中自動啟用未來的依附元件。 |
| Compute Engine | `compute.googleapis.com` | * Google Compute Engine 為 Managed Service for Apache Spark 和 Gemini Enterprise Agent Platform 提供的所有功能，提供執行階段環境。 | * Colab 筆記本、遠端機器學習模型、Apache Spark、SparkSQL 和 PySpark 工作都會停止。 * 原始碼仍可使用。 * Dataproc API 已停用。 |
| Managed Service for Apache Spark | `dataproc.googleapis.com` | * [使用 Apache Spark 等開放原始碼引擎查詢資料。](https://docs.cloud.google.com/bigquery/docs/bqms-use-dataproc?hl=zh-tw) * [搭配使用 Spark SQL 或 PySpark 與 Managed Service for Apache Spark。](https://docs.cloud.google.com/bigquery/docs/bqms-use-dataproc-serverless?hl=zh-tw) * [使用 Spark 預存程序。](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw) | * 您無法建立 Managed Service for Apache Spark 叢集來執行開放原始碼資料分析。 * 您無法執行 Managed Service for Apache Spark 工作負載。 * 無法執行 Spark in BigQuery 工作負載。 |
| Datastream | `datastream.googleapis.com` | * [提供變更資料擷取功能，並將資料複製到 BigQuery。](https://docs.cloud.google.com/datastream/docs/overview?hl=zh-tw) | * 所有資料串流都會暫停，且無法存取。 |

## 預設停用的服務

您必須手動啟用下列服務，才能使用對應的功能：

| **服務** | **API 名稱** | **哪些功能需要這項設定** | **停用這項服務的影響** |
| --- | --- | --- | --- |
| Gemini for Google Cloud API | `cloudaicompanion.googleapis.com` | * Gemini in BigQuery 功能 | * 程式碼完成、生成和說明功能會停止運作。  進一步瞭解如何[關閉 Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw#turn-off)。 |
| Managed Service for Apache Airflow | `composer.googleapis.com` | * [排定工作負載](https://docs.cloud.google.com/bigquery/docs/orchestrate-workloads?hl=zh-tw) | * 現有的 Managed Service for Apache Airflow DAG 不會列在「排程」頁面，且會停止。 * 現有的 Managed Airflow 環境會停止運作，並傳回錯誤狀態。 |
| Data Lineage API | `datalineage.googleapis.com` | * [資料歷程](https://docs.cloud.google.com/knowledge-catalog/docs/use-lineage?hl=zh-tw#view-lineage)擷取和檢視 | * 系統未擷取專案的資料歷程。 * 您無法查看歷程圖。 |

## 手動啟用 BigQuery 程式碼資產

如要在 BigQuery 管理程式碼資產 (例如筆記本和已儲存的查詢)，必須啟用下列 API：

* Compute Engine API
* Dataform API
* Vertex AI API

2024 年 3 月前，系統預設不會自動啟用這些 API。如果您有 2024 年 3 月前建立的自動化指令碼，且這些指令碼依賴這些 API 的狀態，則可能需要更新。如果已啟用這些 API，BigQuery 的「Explorer」窗格中會顯示新的「Notebooks」和「Queries」資料夾。

### 事前準備

如要手動啟用程式碼資產管理功能，您必須具備 Identity and Access Management (IAM) [擁有者角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#legacy-basic) (`roles/owner`)。

### 手動啟用 BigQuery 程式碼資產

如要為程式碼素材資源啟用必要的 API 依附元件，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 **Studio** 編輯器窗格的分頁列中，按一下 **+** 符號旁的 arrow\_drop\_down 箭頭下拉式選單，將滑鼠游標懸停在「Notebook」上，然後選取「Empty notebook」。
3. 點按「啟用 API」。

   如果找不到這個選項，請確認您是否具備必要的 IAM [擁有者角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#legacy-basic) (`roles/owner`)。如果開啟的是空白筆記本，代表您已啟用必要的 API。
4. 在「Enable core features」(啟用核心功能) 窗格的「Core feature APIs」(核心功能 API) 部分，執行下列操作：

   1. 如要啟用資料串流、排程和筆記本的所有 BigQuery 依附元件，請按一下「BigQuery Unified API」旁的「Enable」(啟用)。
   2. 選用：如要選擇要啟用的 API，請按一下「View and enable individual APIs」(查看及啟用個別 API)，然後在要啟用的各個 API 旁按一下「Enable」(啟用)。
   3. API 啟用後，請點選「Next」(下一步)。
5. 選用：在「權限」部分設定使用者權限：

   * 如要授予主體建立程式碼資產，以及讀取、編輯和設定所建立程式碼資產的權限，請在「BigQuery Studio User」(BigQuery Studio 使用者) 欄位中輸入使用者或群組名稱。
   * 如要授予主體讀取、編輯及設定所有共用程式碼資產權限的能力，請在「BigQuery Studio Admin」(BigQuery Studio 管理員) 欄位中輸入使用者或群組名稱。
6. 點選「下一步」。
7. 選用：在「Additional APIs」(其他 API) 專區，按一下「Enable all」(全部啟用)，啟用使用 [BigQuery DataFrames](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw) 建立 BigQuery 遠端程序所需的 API。
8. 如果選擇不啟用其他 API，請按一下「Close」(關閉)，關閉「Enable core features」(啟用核心功能) 窗格。

### 限制程式碼資產的存取權

您可以設定[限制資源服務用量組織政策限制](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-resources?hl=zh-tw)，防止啟用其他 API。您隨時可以[關閉所選 API](https://docs.cloud.google.com/service-usage/docs/enable-disable?hl=zh-tw#disabling)。

## 後續步驟

* 如要瞭解如何管理 Google Cloud 服務，請參閱「[啟用及停用服務](https://docs.cloud.google.com/service-usage/docs/enable-disable?hl=zh-tw)」。
* 如要瞭解如何使用組織政策限制，精細管理 API 存取權，請參閱「[限制資源用量](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-resources?hl=zh-tw)」。
* 如要瞭解如何透過 BigQuery 的 Identity and Access Management (IAM) 角色和權限控管服務存取權，請參閱「[BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-28 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-28 (世界標準時間)。"],[],[]]