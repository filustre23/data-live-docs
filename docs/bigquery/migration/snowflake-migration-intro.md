Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Snowflake 遷移至 BigQuery

本文簡要介紹如何從 Snowflake 遷移至 BigQuery。以下各節將介紹遷移工具，協助您執行 BigQuery 遷移作業，並列出 Snowflake 和 BigQuery 的差異，協助您規劃遷移作業。

## 將工作流程從 Snowflake 遷移至 BigQuery

規劃 BigQuery 遷移作業時，請考量 Snowflake 上的不同工作流程，以及如何個別遷移這些工作流程。為盡量減少對現有作業的影響，建議您先將 SQL 查詢遷移至 BigQuery，然後再遷移結構定義和程式碼。

### 遷移 SQL 查詢

如要遷移 SQL 查詢，BigQuery 遷移服務提供各種 SQL 翻譯功能，可自動將 Snowflake SQL 查詢轉換為 GoogleSQL SQL，例如[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)可大量翻譯查詢、[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)可翻譯個別查詢，以及 [SQL 翻譯 API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw)。這些翻譯服務也包含 Gemini 強化功能，可進一步簡化 SQL 查詢遷移程序。

翻譯 SQL 查詢時，請仔細檢查翻譯後的查詢，確認資料型別和表格結構處理正確無誤。為此，我們建議建立各種情境和資料的測試案例。接著在 BigQuery 中執行這些測試案例，比較結果與原始 Snowflake 結果。如有任何差異，請分析並修正轉換後的查詢。

### 遷移結構定義和程式碼

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要從 Snowflake 遷移結構定義和資料，請使用 BigQuery 資料移轉服務中的 Snowflake 連接器設定資料移轉作業。設定資料移轉時，您可以指定要納入的特定 Snowflake 資料表，也可以讓連結器在移轉期間自動偵測資料表結構定義和資料類型。

如要進一步瞭解如何設定 Snowflake 資料移轉，請參閱[排定 Snowflake 移轉作業](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer?hl=zh-tw)。

#### 增量移轉

使用 Snowflake 連接器進行 Snowflake 資料移轉時，您可以設定遞增移轉，只移轉自上次資料移轉後變更的資料，不必在每次資料移轉時載入整個資料集。詳情請參閱「[排定 Snowflake 轉移作業](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer?hl=zh-tw)」。

## 遷移其他 Snowflake 功能

規劃遷移至 BigQuery 時，請考量下列 Snowflake 功能。

| 用途 | Snowflake 功能 | BigQuery 功能 |
| --- | --- | --- |
| 暫存要載入及匯出的原始資料檔案 | 您可以使用 `GET` 和 `PUT` 指令，將資料上傳及下載至[暫存](https://docs.snowflake.com/en/user-guide/data-load-considerations-stage)。查詢和 `COPY` 指令可以讀取及寫入階段。 | BigQuery 會使用 Cloud Storage 暫存檔案資料，並支援從其他來源和服務讀取及寫入資料。 Google Cloud 使用 Cloud Storage 上傳及下載原始資料檔案。    如要進一步瞭解如何從 Cloud Storage 和其他來源載入資料，請參閱「[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」；如要進一步瞭解如何匯出至 Cloud Storage 和其他來源，請參閱「[資料匯出簡介](https://docs.cloud.google.com/bigquery/docs/export-intro?hl=zh-tw)」。 |
| 預先計算常見查詢的結果 | [動態資料表](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)可透過查詢定義，並依排程重新整理。 | [具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)可設為保留並自動重新整理 SQL 查詢運算。 |
| 小型 DML 作業 | Snowflake [混合式資料表](https://docs.snowflake.com/en/user-guide/tables-hybrid)允許小型 DML 寫入。 | 您可以在 BigQuery 中使用[細微 DML](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#fine-grained_dml)，改善小型寫入作業的延遲和輸送量。    如需進階混合型交易/分析處理 (HTAP) 使用案例，請考慮使用 [Spanner 外部資料集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)。 |
| 筆記本和視覺化 | Snowflake [Streamlit](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit) 應用程式可透過 Python 程式碼將資料視覺化。 | 您可以使用 BigQuery [筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)和 [BigFrames](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw) Python 程式庫，在 Python 中探索及以視覺化方式呈現資料。如要瞭解如何與 Looker 及其他分析和資料視覺化工具整合，請參閱「[分析和商業智慧工具簡介](https://docs.cloud.google.com/bigquery/docs/data-analysis-tools-intro?hl=zh-tw)」。 |
| 實體資料版面配置 | Snowflake 支援叢集和微分割，可整理磁碟上的資料。 | BigQuery 支援明確的[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)，讓使用者精確控管資料的分配和整理方式，進而提升成本和執行階段效能。    SQL 翻譯服務會自動處理資料表叢集翻譯作業，並可[設定](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#set_partition_expiration)在遷移 DDL 時自訂分區和叢集。 |
| 外部函式和程序 | Snowflake 支援以多種外部語言實作的函式和預存程序。 | BigQuery 支援透過 Cloud Run 函式呼叫外部函式。您也可以使用 [使用者定義函式](/bigquery/docs/user-defined-functions) (UDF)，例如在 BigQuery 中執行的 SQL UDF。    BigQuery 支援預存程序的 SQL。如要使用其他語言，建議使用外部函式或用戶端應用程式邏輯。 |

## BigQuery 安全性功能

從 Snowflake 遷移至 BigQuery 時，請考量 BigQuery 處理安全性的方式與 Snowflake 的差異。Google Cloud

BigQuery 的安全性與 Google Cloud中的[身分與存取權管理 (IAM)](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw) 息息相關。IAM 權限定義資源允許的作業，並在 Google Cloud 層級強制執行，提供集中且一致的安全管理方法。以下列舉 Google Cloud的部分重要安全性功能：

* **整合式安全性**：BigQuery 會運用 Google Cloud的安全性功能。包括 IAM，可精細控管存取權，確保安全整合流程順暢無虞。
* **資源層級安全性**：IAM 著重於資源層級的存取控管，可授予使用者和群組各種 BigQuery 資源和服務的權限。這種做法可有效管理存取權，確保使用者只具備執行工作所需的權限。
* **網路安全**：BigQuery 享有 Google Cloud的完善網路安全功能，例如[虛擬私有雲](https://docs.cloud.google.com/vpc/docs/overview?hl=zh-tw)和[私人連線](https://docs.cloud.google.com/vpc/docs/private-service-connect?hl=zh-tw)。

從 Snowflake 遷移至 BigQuery 時，請考量下列安全性相關的遷移需求：

* **IAM 設定**：您必須在 BigQuery 中設定 IAM 角色和權限，以符合現有的 Snowflake 存取控管政策。這包括將 Snowflake 角色對應至適當的 [BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。
* **精細的存取控管**：如果您在 Snowflake 中使用資料列或資料欄層級的安全防護機制，則需要在 BigQuery 中使用[已授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)或[政策標記](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)，實作同等控管措施。
* **檢視區塊和 UDF 遷移**：遷移檢視區塊和 UDF 時，請確認相關聯的安全控制措施已正確轉換為 BigQuery 中的[已授權檢視區塊](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)和[已授權 UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#authorize_routines)。

### 加密

BigQuery 預設會[加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)靜態資料和傳輸中的資料。如需進一步控管加密金鑰，BigQuery 支援 [Cloud Key Management Service](https://docs.cloud.google.com/kms/docs?hl=zh-tw) 中的[客戶管理加密金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。您也可以使用[資料欄層級加密](https://docs.cloud.google.com/bigquery/docs/column-key-encrypt?hl=zh-tw)。

為確保資料在遷移至 BigQuery 期間和之後的資料安全性，請考慮下列事項：

* **金鑰管理**：如果您需要客戶管理的金鑰，請在 Cloud Key Management Service 中建立金鑰管理策略，並將 BigQuery 設為使用這些金鑰。
* **資料遮蓋/代碼化**：如果涉及機密資料，請評估是否需要資料遮蓋或代碼化來保護資料。
* **資料列層級安全性**：使用授權檢視畫面、資料列層級安全性篩選器或其他適當方法，導入資料列層級安全性。
* **安全漏洞掃描和滲透測試**：定期執行安全漏洞掃描和滲透測試，檢查 BigQuery 環境的安全狀態。

### 角色

角色是可授予和撤銷可保護物件權限的實體。

在身分與存取權管理中，權限會納入角色群組。IAM 提供三種角色：

* **[基本角色](https://docs.cloud.google.com/bigquery/docs/access-control-primitive-roles?hl=zh-tw)：**
  包括擁有者、編輯者和檢視者角色。您可以使用Google Cloud 主控台、Identity and Access Management API 或 `gcloud CLI`，在專案或服務資源層級套用這些角色。一般而言，為確保最高安全性，我們建議您使用預先定義的角色，遵循最低權限原則。
* **[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)：**這類角色可提供更精細的產品功能存取權 (例如 BigQuery)，適用於常見用途和存取控管模式。
* **[自訂角色](https://docs.cloud.google.com/iam/docs/understanding-custom-roles?hl=zh-tw)：**
  這類角色是由使用者指定的權限組成。

### 存取權控管

Snowflake 可讓您將角色授予其他角色，建立角色階層。IAM 不支援角色階層，但會實作資源階層。[IAM 階層](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control?hl=zh-tw)包含機構層級、資料夾層級、專案層級和資源層級。您可以在階層的任何層級設定 IAM 角色，資源會繼承父項資源的所有政策。

BigQuery 支援[資料表層級的存取控管](https://docs.cloud.google.com/bigquery/docs/table-access-controls-intro?hl=zh-tw)。資料表層級權限可以決定要允許哪些使用者、群組和服務帳戶存取資料表或檢視表。您可以授予使用者特定資料表或檢視區塊的存取權，而不必授予完整資料集的存取權。

如要更精細地控管存取權，也可以使用[資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)或[資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)。這類控管機制會使用政策標記或依據類型的資料分類方式，對機密資料欄提供精細的存取權限。

您也可以建立[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)，進一步限制資料存取權，以便更精細地進行存取控管，讓指定使用者查詢檢視表，但無法讀取基礎資料表。

## 支援的資料類型、屬性和檔案格式

Snowflake 和 BigQuery 支援的資料類型大多相同，但有時會使用不同名稱。如需 Snowflake 和 BigQuery 支援的完整資料類型清單，請參閱「[資料類型](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-sql?hl=zh-tw#data-types)」。您也可以使用 SQL 翻譯工具，例如[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)、[SQL 翻譯 API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw) 或[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)，將不同的 SQL 方言翻譯成 GoogleSQL。

如要進一步瞭解 BigQuery 支援的資料類型，請參閱「[GoogleSQL 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)」。

Snowflake 可以匯出下列檔案格式的資料。您可以將下列格式的資料直接載入 BigQuery：

* [從 Cloud Storage 載入 CSV 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw)。
* [從 Cloud Storage 載入 Parquet 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw)。
* [從 Cloud Storage 載入 JSON 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw)。
* [查詢 Apache Iceberg 中的資料](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw)。

## 遷移工具

下表列出可將資料從 Snowflake 遷移至 BigQuery 的工具。如要瞭解如何在 Snowflake 遷移管道中一併使用這些工具，請參閱 [Snowflake 遷移管道範例](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-tutorials?hl=zh-tw#pipeline-examples)。

* **[`COPY INTO <location>` 指令](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html)：**
  在 Snowflake 中使用這項指令，將資料從 Snowflake 資料表直接擷取至指定的 Cloud Storage bucket。如需端對端範例，請參閱 GitHub 上的「[Snowflake to BigQuery (snowflake2bq)](https://github.com/GoogleCloudPlatform/professional-services/tree/master/tools/snowflake2bq)」。
* **[Apache Sqoop](https://sqoop.apache.org/)：**
  如要將資料從 Snowflake 擷取至 HDFS 或 Cloud Storage，請使用 Sqoop 和 Snowflake 的 JDBC 驅動程式提交 Hadoop 工作。Sqoop 會在 [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc/docs?hl=zh-tw) 環境中執行。
* **[Snowflake JDBC](https://docs.snowflake.com/en/user-guide/jdbc.html)：**
  搭配支援 JDBC 的大多數用戶端工具或應用程式使用這個驅動程式。

您可以使用下列一般工具，將資料從 Snowflake 遷移至 BigQuery：

* **[Snowflake 連接器的 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer?hl=zh-tw)** ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：
  自動將 Cloud Storage 資料批次移轉至 BigQuery。
* **[Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)：**
  使用這個指令列工具，將下載的 Snowflake 檔案複製到 Cloud Storage。
* **[bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)：**使用這個指令列工具與 BigQuery 互動。
  常見用途包括建立 BigQuery 資料表結構定義、將 Cloud Storage 資料載入資料表，以及執行查詢。
* **[Cloud Storage 用戶端程式庫](https://docs.cloud.google.com/storage/docs/reference/libraries?hl=zh-tw)：**
  使用自訂工具 (採用 Cloud Storage 用戶端程式庫)，將下載的 Snowflake 檔案複製到 Cloud Storage。
* **[BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)：**
  使用以 BigQuery 用戶端程式庫為基礎建構的自訂工具，與 BigQuery 互動。
* **[BigQuery 查詢排程器](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)：**
  使用這項 BigQuery 內建功能，排定週期性 SQL 查詢。
* **[Managed Service for Apache Airflow](https://docs.cloud.google.com/composer/docs?hl=zh-tw)：**
  使用這個全代管 Apache Airflow 環境，自動化調度管理 BigQuery 載入工作和轉換。

如要進一步瞭解如何將資料載入 BigQuery，請參閱[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw#loading_the_data_into_bigquery)。

## 定價

規劃 Snowflake 遷移作業時，請考量在 BigQuery 中轉移資料、儲存資料及使用服務的成本。詳情請參閱「[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」。

將資料移出 Snowflake 或 AWS 時，可能會產生輸出費用。跨區域移轉資料或跨不同雲端服務供應商移轉資料時，也可能產生額外費用。

## 開始使用

以下各節將摘要說明從 Snowflake 遷移至 BigQuery 的程序：

### 執行遷移評估

在從 Snowflake 遷移至 BigQuery 的過程中，建議您先執行 [BigQuery 遷移評估工具](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)，評估將資料倉儲從 Snowflake 遷移至 BigQuery 的可行性和潛在效益。這項工具提供結構化方法，協助您瞭解目前的 Snowflake 環境，並估算順利遷移所需的作業量。

執行 BigQuery 遷移評估工具後，會產生評估報告，其中包含下列章節：

* 現有系統報表：現有 Snowflake 系統和用量的快照，包括資料庫、結構定義、資料表數量，以及總大小 (以 TB 為單位)。此外，這項工具也會依大小列出結構定義，並指出可能導致資源使用率偏低的因素，例如沒有寫入作業或讀取次數很少的資料表。
* BigQuery 穩定狀態轉換建議：顯示遷移後 BigQuery 的系統樣貌。包括如何最佳化 BigQuery 工作負載，以及避免浪費資源的建議。
* 遷移計畫：提供遷移作業本身的相關資訊。舉例來說，從現有系統遷移至 BigQuery 穩定狀態。這個部分會顯示自動翻譯的查詢數量，以及將每個資料表移至 BigQuery 的預估時間。

如要進一步瞭解遷移評估結果，請參閱「[查看數據分析報表](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw#review_the_data_studio_report)」。

### 驗證遷移作業

將 Snowflake 資料遷移至 BigQuery 後，請執行[資料驗證工具 (DVT)](https://github.com/GoogleCloudPlatform/professional-services-data-validator)，對新遷移的 BigQuery 資料進行資料驗證。DVT 會驗證各種函式 (從資料表層級到資料列層級)，確認遷移的資料是否如預期運作。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]