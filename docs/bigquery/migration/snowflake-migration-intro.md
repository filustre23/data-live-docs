Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Snowflake 遷移至 BigQuery

本文將介紹如何從 Snowflake 遷移至 BigQuery。以下各節將介紹遷移工具，協助您執行 BigQuery 遷移作業，並概述 Snowflake 和 BigQuery 之間的一些差異，協助您規劃遷移作業。

## 將工作流程從 Snowflake 遷移至 BigQuery

規劃 BigQuery 遷移作業時，請考量 Snowflake 上的不同工作流程，以及如何個別遷移。為盡可能降低對現有作業的影響，建議您先將 SQL 查詢遷移至 BigQuery，然後再遷移結構定義和程式碼。

### 遷移 SQL 查詢

如要遷移 SQL 查詢，BigQuery 遷移服務提供多種 SQL 翻譯功能，可自動將 Snowflake SQL 查詢轉換為 GoogleSQL SQL，例如[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)可大量翻譯查詢、[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)可翻譯個別查詢，以及 [SQL 翻譯 API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw)。這些翻譯服務也包含 Gemini 強化功能，可進一步簡化 SQL 查詢遷移程序。

翻譯 SQL 查詢時，請仔細檢查翻譯後的查詢，確認資料類型和資料表結構是否正確處理。為此，建議您建立各種測試案例，涵蓋不同情境和資料。接著在 BigQuery 執行這些測試案例，並與原始 Snowflake 結果比較。如有任何差異，請分析並修正轉換後的查詢。

### 遷移結構定義和程式碼

如要從 Snowflake 遷移結構定義和資料，請使用 BigQuery 資料移轉服務中的 Snowflake 連接器設定資料移轉作業。設定資料移轉作業時，您可以指定要納入的特定 Snowflake 資料表，並讓連接器在移轉期間自動偵測資料表結構定義和資料類型。

如要進一步瞭解如何設定 Snowflake 資料移轉作業，請參閱「[排定 Snowflake 移轉作業](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer?hl=zh-tw)」。

#### 增量移轉作業

使用 Snowflake 連接器移轉 Snowflake 資料時，您可以設定遞增移轉，只移轉上次資料移轉後變更的資料，而不是每次都載入整個資料集。詳情請參閱「[排定 Snowflake 移轉作業](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer?hl=zh-tw)」。

## 遷移其他 Snowflake 功能

規劃遷移至 BigQuery 時，請考量下列 Snowflake 功能。

| 用途 | Snowflake 功能 | BigQuery 功能 |
| --- | --- | --- |
| 暫存原始資料檔案，以便載入和匯出 | 您可以使用 `GET` 和 `PUT` 指令，將資料上傳及下載至[暫存區](https://docs.snowflake.com/en/user-guide/data-load-considerations-stage)。查詢和「COPY」指令可以讀取及寫入暫存區。 | BigQuery 仰賴 Cloud Storage 暫存檔案資料，並支援從其他多個來源和服務讀取及寫入資料。 Google Cloud 使用 Cloud Storage 上傳及下載原始資料檔案。    如要進一步瞭解從 Cloud Storage 和其他來源載入資料的多種方式，請參閱「[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」；如要進一步瞭解如何匯出至 Cloud Storage 和其他來源，請參閱「[資料匯出簡介](https://docs.cloud.google.com/bigquery/docs/export-intro?hl=zh-tw)」。 |
| 預先運算常見查詢結果 | [動態資料表](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)可透過查詢定義，並依排程重新整理。 | 您可以設定[具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)，保留並自動重新整理 SQL 查詢運算。 |
| 小型 DML 作業 | Snowflake [混合資料表](https://docs.snowflake.com/en/user-guide/tables-hybrid)允許小型 DML 寫入。 | 您可以在 BigQuery 中使用[精細 DML](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#fine-grained_dml)，縮短延遲時間並提高小型寫入作業的處理量。    如需進階混合型交易/數據分析處理 (HTAP) 用途，建議使用 [Spanner 外部資料集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)。 |
| Notebook 和視覺化 | Snowflake [Streamlit](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit) 應用程式可透過 Python 程式碼，以圖表呈現資料。 | BigQuery [筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)和 [BigFrames](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw) Python 程式庫可用於探索及視覺化 Python 資料。如要瞭解如何與 Looker 和其他分析及視覺化工具整合，請參閱「[分析和商業智慧工具簡介](https://docs.cloud.google.com/bigquery/docs/data-analysis-tools-intro?hl=zh-tw)」。 |
| 實體資料配置 | Snowflake 支援叢集和微資料分割，可整理磁碟上的資料。 | BigQuery 支援明確[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)，讓使用者精確控管資料分布和整理方式，進而提升成本效益和執行階段效能。    SQL 翻譯服務會自動處理資料表分群翻譯，您也可以[設定](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#set_partition_expiration)在遷移 DDL 時自訂分區和分群。 |
| 外部函式和程序 | Snowflake 支援以多種外部語言實作的函式和預存程序。 | BigQuery 支援透過 Cloud Run functions 呼叫外部函式。您也可以使用 [user-defined function](/bigquery/docs/user-defined-functions) (UDF)，例如在 BigQuery 中執行的 SQL UDF。    BigQuery 支援 SQL 儲存程序。如要使用其他語言，建議您使用外部函式或用戶端應用程式邏輯。 |

## BigQuery 安全防護功能

從 Snowflake 遷移至 BigQuery 時，請考量Google Cloud 與 Snowflake 處理安全性的方式有何不同。

BigQuery 的安全性與 Google Cloud中的 [Identity and Access Management (IAM)](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw) 密不可分。IAM 權限定義了資源允許的操作，並在 Google Cloud 層級強制執行，提供集中且一致的安全管理方法。以下是 Google Cloud的主要安全防護功能：

* **整合式安全性**：BigQuery 運用 Google Cloud的安全防護功能，包括 IAM，可精細控管存取權，提供強大且流暢的安全整合。
* **資源層級安全性**：IAM 著重於資源層級的存取控管，可為使用者和群組授予各種 BigQuery 資源和服務的權限。這種做法可有效管理存取權，確保使用者只具備執行工作所需的權限。
* **網路安全**：BigQuery 受益於 Google Cloud強大的網路安全防護功能，例如[虛擬私有雲](https://docs.cloud.google.com/vpc/docs/overview?hl=zh-tw)和[私人連線](https://docs.cloud.google.com/vpc/docs/private-service-connect?hl=zh-tw)。

從 Snowflake 遷移至 BigQuery 時，請考量下列安全性相關遷移需求：

* **IAM 設定**：您必須在 BigQuery 中設定 IAM 角色和權限，以符合現有的 Snowflake 存取控管政策。這包括將 Snowflake 角色對應至適當的 [BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。
* **精細的存取控管**：如果您在 Snowflake 中使用資料列層級或資料欄層級安全性，則必須使用[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)或[政策標記](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)，在 BigQuery 中實作對等控管機制。
* **檢視表和 UDF 遷移**：遷移檢視表和 UDF 時，請確認相關聯的安全控管機制已正確轉譯為 BigQuery 中的[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)和[授權 UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#authorize_routines)。

### 加密

BigQuery 預設會[加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)靜態和傳輸中的資料。如需進一步控管加密金鑰，BigQuery 支援 [Cloud Key Management Service](https://docs.cloud.google.com/kms/docs?hl=zh-tw) 中的[客戶自行管理的加密金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。您也可以使用[資料欄層級加密](https://docs.cloud.google.com/bigquery/docs/column-key-encrypt?hl=zh-tw)。

為確保在遷移至 BigQuery 期間和之後的資料安全性，請考量下列事項：

* **金鑰管理**：如需客戶自行管理的金鑰，請在 Cloud Key Management Service 制定金鑰管理策略，並設定 BigQuery 使用這些金鑰。
* **資料遮蓋/代碼化**：如果涉及機密資料，請評估是否需要遮蓋或代碼化資料，以保護資料。
* **資料列層級安全性**：使用授權檢視表、資料列層級安全性篩選器或其他適當方法，實施資料列層級安全性。
* **安全漏洞掃描和滲透測試**：定期執行安全漏洞掃描和滲透測試，檢查 BigQuery 環境的資安態勢。

### 角色

角色是可授予及撤銷安全物件權限的實體。

在身分與存取權管理中，權限會納入角色群組。IAM 提供三種角色：

* **[基本角色](https://docs.cloud.google.com/bigquery/docs/access-control-basic-roles?hl=zh-tw)：**
  包括擁有者、編輯者和檢視者角色。您可以使用Google Cloud 控制台、Identity and Access Management API 或 `gcloud CLI`，在專案或服務資源層級套用這些角色。一般來說，為確保最高安全性，建議您使用預先定義的角色，遵循最小權限原則。
* **[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)：**這類角色可讓您更精細地控管產品 (例如 BigQuery) 功能的存取權，適用於常見用途和存取控管模式。
* **[自訂角色](https://docs.cloud.google.com/iam/docs/understanding-custom-roles?hl=zh-tw)：**這類角色是由使用者指定的權限組成。

### 存取控管

Snowflake 可讓您將角色授予其他角色，建立角色階層。IAM 不支援角色階層，但會實作資源階層。[IAM 階層](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control?hl=zh-tw)包含組織層級、資料夾層級、專案層級和資源層級。您可以在階層中的任何層級設定 IAM 角色，資源會繼承父項資源的所有政策。

BigQuery 支援[資料表層級存取控管](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)。資料表層級權限會決定哪些使用者、群組和服務帳戶可以存取資料表或檢視表。您可以授予使用者特定資料表或檢視表的存取權，而不必授予完整資料集的存取權。

如要更精細地控管存取權，也可以使用[資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)或[資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)。這類控管機制會使用政策標記或依據類型的資料分類，對機密資料欄提供精細的存取權限。

您也可以建立[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)，限制資料存取權，以便進行更精細的存取控管，讓指定使用者可以查詢檢視表，而不需要基礎資料表的讀取權限。

## 支援的資料類型、屬性和檔案格式

Snowflake 和 BigQuery 支援大部分相同的資料類型，但有時會使用不同的名稱。如需 Snowflake 和 BigQuery 支援的資料類型完整清單，請參閱「[資料類型](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-sql?hl=zh-tw#data-types)」。您也可以使用 SQL 翻譯工具，例如[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)、[SQL 翻譯 API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw) 或[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)，將不同的 SQL 方言翻譯成 GoogleSQL。

如要進一步瞭解 BigQuery 支援的資料類型，請參閱「[GoogleSQL 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)」。

Snowflake 可匯出下列檔案格式的資料。您可以直接將下列格式載入 BigQuery：

* [從 Cloud Storage 載入 CSV 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw)。
* [從 Cloud Storage 載入 Parquet 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw)。
* [從 Cloud Storage 載入 JSON 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw)。
* [查詢 Apache Iceberg 中的資料](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)。

## 遷移工具

下列清單說明可用於將資料從 Snowflake 遷移至 BigQuery 的工具。如要瞭解如何在 Snowflake 遷移管道中搭配使用這些工具，請參閱「[Snowflake 遷移管道範例](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-tutorials?hl=zh-tw#pipeline-examples)」。

* **[`COPY INTO <location>` 指令](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html)：**
  在 Snowflake 中使用這個指令，將 Snowflake 資料表中的資料直接擷取至指定的 Cloud Storage bucket。如需端對端範例，請參閱 GitHub 上的 [Snowflake 至 BigQuery (snowflake2bq)](https://github.com/GoogleCloudPlatform/professional-services/tree/master/tools/snowflake2bq)。
* **[Apache Sqoop](https://sqoop.apache.org/)：**如要將 Snowflake 的資料擷取至 HDFS 或 Cloud Storage，請使用 Sqoop 和 Snowflake 的 JDBC 驅動程式提交 Hadoop 工作。Sqoop 會在 [Managed Service for Apache Spark](https://docs.cloud.google.com/managed-spark/docs?hl=zh-tw) 環境中執行。
* **[Snowflake JDBC](https://docs.snowflake.com/en/user-guide/jdbc.html)：**
  這個驅動程式適用於大多數支援 JDBC 的用戶端工具或應用程式。

您可以使用下列一般工具，將資料從 Snowflake 遷移至 BigQuery：

* **[Snowflake 專用 BigQuery 資料移轉服務連接器](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer?hl=zh-tw)**：自動將 Cloud Storage 資料批次移轉至 BigQuery。
* **[Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)：**使用這項指令列工具，將下載的 Snowflake 檔案複製到 Cloud Storage。
* **[bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)：**使用這項指令列工具與 BigQuery 互動。常見用途包括建立 BigQuery 資料表結構定義、將 Cloud Storage 資料載入資料表，以及執行查詢。
* **[Cloud Storage 用戶端程式庫](https://docs.cloud.google.com/storage/docs/reference/libraries?hl=zh-tw)：**
  使用採用 Cloud Storage 用戶端程式庫的自訂工具，將下載的 Snowflake 檔案複製到 Cloud Storage。
* **[BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)：**使用以 BigQuery 用戶端程式庫為基礎建構的自訂工具，與 BigQuery 互動。
* **[BigQuery 查詢排程器](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)：**使用這項內建 BigQuery 功能，排定週期性 SQL 查詢。
* **[Managed Service for Apache Airflow](https://docs.cloud.google.com/composer/docs?hl=zh-tw)：**使用這個全代管 Apache Airflow 環境，自動調度管理 BigQuery 載入工作和轉換作業。

如要進一步瞭解如何將資料載入 BigQuery，請參閱「[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw#loading_the_data_into_bigquery)」。

## 定價

規劃 Snowflake 遷移作業時，請考量在 BigQuery 中移轉資料、儲存資料和使用服務的費用。詳情請參閱「[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」。

將資料移出 Snowflake 或 AWS 可能會產生 egress 費用。跨區域或跨雲端服務供應商移轉資料時，也可能產生額外費用。

## 開始使用

以下各節將概略說明從 Snowflake 遷移至 BigQuery 的程序：

### 執行遷移評估

從 Snowflake 遷移至 BigQuery 時，建議您先執行 [BigQuery 遷移評估工具](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)，評估將資料倉儲從 Snowflake 遷移至 BigQuery 的可行性和潛在效益。這項工具提供結構化方法，可協助您瞭解目前的 Snowflake 環境，並預估順利遷移所需的工作。

執行 BigQuery 遷移評估工具後，會產生評估報告，其中包含下列部分：

* 現有系統報表：現有 Snowflake 系統和用量的數據匯報，包括資料庫、結構定義、資料表的數量，以及總大小 (以 TB 為單位)。此外，這項工具也會依大小列出結構定義，並指出可能未充分利用資源的情況，例如沒有寫入作業或讀取作業很少的資料表。
* BigQuery 穩定狀態轉換建議：顯示遷移後系統在 BigQuery 中的樣貌。其中包含在 BigQuery 最佳化工作負載和避免浪費的建議。
* 遷移計畫：提供遷移作業本身的相關資訊。例如從現有系統轉換至 BigQuery 穩定狀態。這個部分包含自動翻譯的查詢數量，以及將各個資料表移至 BigQuery 的預計時間。

如要進一步瞭解遷移評估結果，請參閱「[查看數據分析報表](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw#review_the_data_studio_report)」。

### 驗證遷移作業

將 Snowflake 資料遷移至 BigQuery 後，請執行 [Data Validation Tool (DVT)](https://github.com/GoogleCloudPlatform/professional-services-data-validator)，對新遷移的 BigQuery 資料執行資料驗證。DVT 會驗證從資料表層級到資料列層級的各種函式，確認遷移的資料能正常運作。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-08 (世界標準時間)。"],[],[]]