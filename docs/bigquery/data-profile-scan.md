Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 剖析資料

資料剖析掃描會分析資料的統計特徵 (例如平均值、不重複值和最大值)，協助您進一步瞭解資料。使用這些由 Knowledge Catalog 支援的掃描功能，您可以深入瞭解資料集，並快速建立[資料品質檢查建議規則](https://docs.cloud.google.com/knowledge-catalog/docs/auto-data-quality-overview?hl=zh-tw)。

如要進一步瞭解資料剖析，請參閱「[關於資料剖析](https://docs.cloud.google.com/knowledge-catalog/docs/data-profiling-overview?hl=zh-tw)」。

**提示：** 本文說明如何管理專案中的資料剖析掃描作業。您也可以在處理特定資料表時，建立及管理資料剖析掃描。詳情請參閱「[管理特定資料表的資料剖析掃描作業](#start-from-table)」。

## 事前準備

啟用 Dataplex API (如果尚未啟用)。

**啟用 API 所需的角色**

您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「Service Usage 管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

[啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=dataplex.googleapis.com&hl=zh-tw)

## 必要的角色

本節說明使用 Knowledge Catalog 資料剖析掃描作業所需的 IAM 角色和權限。

### 使用者角色和權限

如要取得建立及管理資料剖析掃描作業所需的權限，請要求管理員授予您下列 IAM 角色：

* 建立、執行、更新及刪除資料剖析掃描：在包含資料掃描作業的專案中，具備 [Dataplex DataScan 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.dataScanEditor)  (`roles/dataplex.dataScanEditor`) 角色
* 查看資料剖析掃描結果、工作和記錄：在包含資料掃描作業的專案中，具備 [Dataplex DataScan 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.dataScanViewer)  (`roles/dataplex.dataScanViewer`) 角色
* 將資料剖析掃描結果發布至 Knowledge Catalog：`@bigquery` 項目群組的 [Dataplex Catalog 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.catalogEditor)  (`roles/dataplex.catalogEditor`)
* 在「資料剖析」分頁中，查看 BigQuery 內已發布的資料剖析掃描結果：
  資料表的 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 執行資料剖析掃描：
  + 在執行掃描作業的專案 (所有資料表類型) 具備 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`) 角色
  + 對要掃描的 BigQuery 資料表，具備 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`) 角色
* 對使用 Cloud Storage 資料的 BigQuery 外部資料表執行資料剖析掃描：
  + Cloud Storage bucket (Cloud Storage、Apache Hive 目錄端點和 Apache Iceberg REST 目錄端點) 的 [Storage 物件檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectViewer)  (`roles/storage.objectViewer`)
  + Cloud Storage bucket 的 [Storage 舊版 bucket 讀取者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.legacyBucketReader)  (`roles/storage.legacyBucketReader`)
* 對 Google Cloud Lakehouse 管理的 Apache Iceberg、Apache Hive 和 SAP BDC Delta Lake 資料表執行資料剖析掃描：
  對要掃描的資料表具備 [BigLake 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-tw#biglake.viewer)  (`roles/biglake.viewer`) 角色
* 將資料剖析掃描結果匯出至 BigQuery 資料表：資料表的 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備建立及管理資料剖析掃描作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能建立及管理資料剖析掃描作業：

* 建立、執行、更新及刪除資料剖析掃描：
  + 專案的 `dataplex.datascans.create`
  + `dataplex.datascans.update`
    資料掃描
  + `dataplex.datascans.delete`
    資料掃描
  + `dataplex.datascans.run`
    資料掃描
  + `dataplex.datascans.get`
    資料掃描
  + 專案的 `dataplex.datascans.list`
  + `dataplex.dataScanJobs.get`
    資料掃描工作
  + `dataplex.dataScanJobs.list`
    資料掃描
* 查看資料剖析掃描結果、工作和記錄：
  + `dataplex.datascans.getData`
    資料掃描
  + 專案的 `dataplex.datascans.list`
  + `dataplex.dataScanJobs.get`
    資料掃描工作
  + `dataplex.dataScanJobs.list`
    資料掃描
* 將資料剖析掃描結果發布至 Knowledge Catalog：
  + 項目群組上的 `dataplex.entryGroups.useDataProfileAspect`
  + `bigquery.tables.update`
    在資料表
  + `dataplex.entries.update`
    (進入時)
* 在 BigQuery 或 Knowledge Catalog 查看資料表的已發布資料剖析結果：
  + `bigquery.tables.get`
    在資料表
  + `bigquery.tables.getData`
    在資料表

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### Knowledge Catalog 服務帳戶角色和權限

無論您選取哪種[執行身分](https://docs.cloud.google.com/knowledge-catalog/docs/data-profiling-overview?hl=zh-tw#execution_identity) (預設 Knowledge Catalog 服務代理、自訂服務帳戶或使用者憑證)，該身分都必須具備下列角色和權限，才能在後端執行資料剖析掃描工作及匯出結果。

**注意：** 如要掃描以 CMEK 加密的 BigQuery 資源，您也必須將 `roles/cloudkms.cryptoKeyEncrypterDecrypter` 角色授予相關服務代理。詳情請參閱「[DataScans CMEK 權限](https://docs.cloud.google.com/knowledge-catalog/docs/cmek?hl=zh-tw#datascans-cmek-permissions)」。

為確保執行身分具備必要權限，可執行資料剖析掃描作業及匯出結果，請要求管理員將下列 IAM 角色授予執行身分：

**重要事項：**請務必將這些角色授予執行身分，*而非*您的使用者帳戶。如果未將角色授予正確的主體，可能會發生權限錯誤。

* 執行資料剖析掃描：
  + 在執行掃描作業的專案 (所有資料表類型) 具備 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`) 角色
  + 對要掃描的 BigQuery 資料表，具備 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`) 角色
* 對使用 Cloud Storage 資料的 BigQuery 外部資料表執行資料剖析掃描：
  + Cloud Storage bucket 的 [Storage 物件檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectViewer)  (`roles/storage.objectViewer`)
  + Cloud Storage bucket 的[儲存空間舊版 bucket 讀取者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.legacyBucketReader)  (`roles/storage.legacyBucketReader`)
* 對 Google Cloud Lakehouse 管理的 Apache Iceberg、Apache Hive 和 SAP BDC Delta Lake 資料表執行資料剖析掃描：
  對要掃描的資料表具備 [BigLake 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-tw#biglake.viewer)  (`roles/biglake.viewer`) 角色
* 將資料剖析掃描結果匯出至 BigQuery 資料表：資料表的 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行資料剖析掃描作業和匯出結果所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行資料剖析掃描作業及匯出結果，必須具備下列權限：

* 對 BigQuery 資料執行資料剖析掃描：
  + 專案的 `bigquery.jobs.create`
  + `bigquery.tables.get`
    在資料表
  + `bigquery.tables.getData`
    在資料表
* 對使用 Cloud Storage 資料的 BigQuery 外部資料表執行資料剖析掃描：
  + `storage.buckets.get`
    (位於值區)
  + `storage.objects.get`
    (物件)
* 將資料剖析掃描結果匯出至 BigQuery 資料表：
  + `bigquery.tables.create`
    資料集
  + `bigquery.tables.updateData`
    在資料表

管理員或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，將這些權限授予執行身分。

如果資料表使用 BigQuery [資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)，Knowledge Catalog 只能掃描 Knowledge Catalog 服務帳戶可查看的資料列。如要讓 Knowledge Catalog 掃描所有資料列，請將其服務帳戶新增至述詞為 `TRUE` 的資料列篩選器。

如果資料表使用 BigQuery [資料欄層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)，Knowledge Catalog 必須具備存取權，才能掃描受保護的資料欄。如要授予存取權，請將資料表使用的所有政策標記，授予 Knowledge Catalog 服務帳戶「Data Catalog 精細讀取者」 (`roles/datacatalog.fineGrainedReader`) 角色。建立或更新資料掃描作業的使用者，也需要受保護資料欄的權限。

### 將角色授予 Knowledge Catalog 服務帳戶

為執行資料剖析掃描，Knowledge Catalog 會使用服務帳戶，該帳戶必須具備執行 BigQuery 工作和讀取 BigQuery 資料表資料的權限。如要授予必要角色，請按照下列步驟操作：

1. 取得 Knowledge Catalog 服務帳戶的電子郵件地址。如果您先前未在這項專案中建立資料剖析或資料品質掃描，請執行下列 `gcloud` 指令，產生服務身分：

   ```
   gcloud beta services identity create --service=dataplex.googleapis.com
   ```

   這個指令會傳回服務帳戶電子郵件地址，格式如下：service-PROJECT\_ID@gcp-sa-dataplex.iam.gserviceaccount.com。

   如果服務帳戶已存在，您可以在
   Google Cloud 控制台的「[**IAM**
   」頁面上](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)，查看名稱為「**Dataplex**」的主體，找出該帳戶的電子郵件地址。
2. 將專案的 **BigQuery 工作使用者** (`roles/bigquery.jobUser`) 角色授予服務帳戶。這個角色可讓服務帳戶執行掃描的 BigQuery 工作。

   ```
   gcloud projects add-iam-policy-binding PROJECT_ID \
       --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-dataplex.iam.gserviceaccount.com" \
       --role="roles/bigquery.jobUser"
   ```

   更改下列內容：

   * `PROJECT_ID`：您的 Google Cloud 專案 ID。
   * `service-PROJECT_NUMBER@gcp-sa-dataplex.iam.gserviceaccount.com`：Knowledge Catalog 服務帳戶的電子郵件地址。
3. 針對要剖析的每個資料表，授予服務帳戶 **BigQuery 資料檢視者** (`roles/bigquery.dataViewer`) 角色。這個角色可授予資料表的唯讀存取權。

   ```
   gcloud bigquery tables add-iam-policy-binding DATASET_ID.TABLE_ID \
       --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-dataplex.iam.gserviceaccount.com" \
       --role="roles/bigquery.dataViewer"
   ```

   更改下列內容：

   * `DATASET_ID`：資料表所在資料集的 ID。
   * `TABLE_ID`：要剖析的資料表 ID。
   * `service-PROJECT_NUMBER@gcp-sa-dataplex.iam.gserviceaccount.com`：Knowledge Catalog 服務帳戶的電子郵件地址。

## 建立資料剖析掃描

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 點按「建立資料剖析掃描」。
3. (選用) 輸入**顯示名稱**。
4. 輸入 ID。請參閱[資源命名慣例](https://docs.cloud.google.com/compute/docs/naming-resources?hl=zh-tw#resource-name-format)。
5. 選用：輸入**說明**。
6. 在「Table」(資料表) 欄位中，按一下「Browse」(瀏覽)。選擇要掃描的資料表，然後按一下「Select」(選取)。僅支援標準 BigQuery 資料表，以及由Google Cloud Lakehouse 管理的 Apache Iceberg、Apache Hive 和 SAP BDC Delta Lake 資料表。

   如果是多區域資料集內的資料表，請選擇要建立資料掃描作業的區域。

   如要瀏覽 Knowledge Catalog 湖泊中的資料表，請按一下「Browse within Knowledge Catalog Lakes」(在 Knowledge Catalog 湖泊中瀏覽)。
7. 在「模式」部分，選取下列其中一個選項：

   * **標準**：使用可自訂的掃描設定剖析資料。此為預設模式。
   * **輕量**：透過低延遲、低精確度的掃描，快速提供洞察資訊。
8. 如果選擇「Standard」模式，請設定下列選項。如果選取「Lightweight」模式，就不會顯示這些選項。

   1. 在「Scope」(範圍) 欄位中，選擇「Incremental」(增量) 或「Entire data」(完整資料)。

      如果選擇「Incremental data」(增量資料)，請在「Timestamp column」(時間戳記欄) 欄位中，從 BigQuery 資料表選取 `DATE` 或 `TIMESTAMP` 類型的資料欄。Knowledge Catalog 會使用這個資料欄，識別新增的記錄。如果資料表是依 `DATE` 或 `TIMESTAMP` 類型的資料欄分區，建議使用該資料欄做為分區資料欄。
   2. 選用：如要篩選資料，請執行下列任一操作：

      * 如要依資料列篩選，請勾選「篩選資料列」核取方塊。請輸入有效的 SQL 運算式，可用於 [GoogleSQL 語法的 `WHERE` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#where_clause)。例如：`col1 >= 0`。

        篩選器可以是多個資料欄的 SQL 條件組合。例如：`col1 >= 0 AND col2 < 10`。
      * 如要依資料欄篩選，請勾選「篩選資料欄」核取方塊。
      * 如要在設定檔掃描中納入資料欄，請在「Include columns」(納入資料欄) 欄位中，按一下「Browse」(瀏覽)。選取要納入的資料欄，然後按一下「Select」(選取)。
      * 如要從設定檔掃描中排除資料欄，請在「Exclude columns」(排除資料欄) 欄位中，按一下「Browse」(瀏覽)。選取要排除的資料欄，然後按一下「Select」(選取)。**注意：** 您可以使用「包含資料欄」、「排除資料欄」，或兩者皆用。如果同時使用這兩個欄位，資料剖析掃描作業會先根據您在「Include columns」(納入資料欄) 欄位中輸入的內容選取資料欄，然後根據您在「Exclude columns」(排除資料欄) 欄位中輸入的內容排除資料欄。
   3. 如要對資料剖析掃描套用取樣，請在「Sampling size」(取樣大小) 清單中選取取樣百分比。請選擇介於 0.0% 至 100.0% 之間的百分比值，最多可到小數點後 3 位。

      * 如果資料集較大，請選擇較低的取樣百分比。舉例來說，如果資料表大小為 1 PB，您輸入的值介於 0.1% 至 1.0% 之間，資料剖析作業會取樣 1 至 10 TB 的資料。
      * 樣本資料中至少要有 100 筆記錄，才能傳回結果。
      * 如果是遞增資料掃描，資料剖析掃描會對最新增量套用取樣。
9. 選用：在Google Cloud 控制台的 BigQuery 和 Knowledge Catalog 頁面中，發布來源資料表的資料剖析掃描結果。勾選「Publish results to Knowledge Catalog」(將結果發布至 Knowledge Catalog) 核取方塊。

   您可以在來源資料表的 BigQuery 和 Knowledge Catalog 頁面中，透過「Data profile」(資料剖析) 分頁查看最新的掃描結果。如要讓使用者存取已發布的掃描結果，請參閱本文的「[授予資料剖析掃描結果的存取權](#share-results)」一節。

   在下列情況下，可能無法使用發布選項：

   * 您沒有資料表的必要權限。
   * 已將另一項資料剖析掃描設為發布結果。
10. 在「Schedule」(時間表) 部分，選擇下列其中一個選項：

    * **重複**：按照排程執行資料剖析掃描，頻率可設為每小時、每天、每週、每月或自訂。指定掃描作業的執行頻率和時間。如果選擇自訂，請使用 [cron](https://en.wikipedia.org/wiki/Cron) 格式指定排程。
    * **依需求**：依需求執行資料剖析掃描。
    * **單次執行**：立即執行資料剖析掃描作業一次，並在自動刪除時間過後移除掃描作業。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

      + **設定掃描後結果自動刪除**：自動刪除時間定義資料剖析掃描執行後，保持有效的時間長度。如果未指定自動刪除時間，資料剖析掃描作業會在 24 小時後自動移除。自動刪除時間可介於 0 秒 (立即刪除) 到 365 天之間。
11. 按一下「繼續」。
12. 選用：將掃描結果匯出至 BigQuery 標準資料表。在「Export scan results to BigQuery table」(將掃描結果匯出至 BigQuery 資料表) 區段中，執行下列操作：

    1. 在「選取 BigQuery 資料集」欄位中，按一下「瀏覽」。選取要儲存資料剖析掃描結果的 BigQuery 資料集。
    2. 在「BigQuery table」(BigQuery 資料表) 欄位中，指定要儲存資料剖析掃描結果的資料表。如果使用現有資料表，請確認該資料表與[匯出資料表結構定義](https://docs.cloud.google.com/knowledge-catalog/docs/use-data-profiling?hl=zh-tw#table-schema)相容。如果指定的資料表不存在，Knowledge Catalog 會為您建立。

       **注意：** 您可以將多項資料剖析掃描作業的結果，儲存至同一個結果資料表。
13. 選用：新增標籤。標籤是鍵/值組合，可用來將相關物件分組，或與其他 Google Cloud 資源組合。
14. 如要建立掃描作業，請按一下「Create」(建立)。

    如果將排程設為「依需求」，也可以點選「執行掃描」，立即執行掃描。

### gcloud

如要建立資料剖析掃描，請使用 [`gcloud dataplex datascans create data-profile` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/create/data-profile?hl=zh-tw)。

如果來源資料是以 Knowledge Catalog 湖泊的形式組織，請加入 `--data-source-entity` 旗標：

```
gcloud dataplex datascans create data-profile DATASCAN \
--location=LOCATION \
--data-source-entity=DATA_SOURCE_ENTITY
```

如果來源資料並非在 Knowledge Catalog 湖泊內管理，請加入 `--data-source-resource` 旗標：

```
gcloud dataplex datascans create data-profile DATASCAN \
--location=LOCATION \
--data-source-resource=DATA_SOURCE_RESOURCE
```

請替換下列變數：

* `DATASCAN`：資料剖析掃描作業的名稱。
* `LOCATION`：要建立資料剖析掃描作業的 Google Cloud 區域。
* `DATA_SOURCE_ENTITY`：Knowledge Catalog 實體，包含資料剖析掃描作業的資料。例如：`projects/test-project/locations/test-location/lakes/test-lake/zones/test-zone/entities/test-entity`。
* `DATA_SOURCE_RESOURCE`：資源名稱，內含資料剖析掃描作業的資料。例如：`//bigquery.googleapis.com/projects/test-project/datasets/test-dataset/tables/test-table`。

### C#

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 C# 設定操作說明進行操作。詳情請參閱 [BigQuery C# API 參考文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.Dataplex.V1/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
using Google.Api.Gax.ResourceNames;
using Google.Cloud.Dataplex.V1;
using Google.LongRunning;

public sealed partial class GeneratedDataScanServiceClientSnippets
{
    /// <summary>Snippet for CreateDataScan</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void CreateDataScanRequestObject()
    {
        // Create client
        DataScanServiceClient dataScanServiceClient = DataScanServiceClient.Create();
        // Initialize request argument(s)
        CreateDataScanRequest request = new CreateDataScanRequest
        {
            ParentAsLocationName = LocationName.FromProjectLocation("[PROJECT]", "[LOCATION]"),
            DataScan = new DataScan(),
            DataScanId = "",
            ValidateOnly = false,
        };
        // Make the request
        Operation<DataScan, OperationMetadata> response = dataScanServiceClient.CreateDataScan(request);

        // Poll until the returned long-running operation is complete
        Operation<DataScan, OperationMetadata> completedResponse = response.PollUntilCompleted();
        // Retrieve the operation result
        DataScan result = completedResponse.Result;

        // Or get the name of the operation
        string operationName = response.Name;
        // This name can be stored, then the long-running operation retrieved later by name
        Operation<DataScan, OperationMetadata> retrievedResponse = dataScanServiceClient.PollOnceCreateDataScan(operationName);
        // Check if the retrieved long-running operation has completed
        if (retrievedResponse.IsCompleted)
        {
            // If it has completed, then access the result
            DataScan retrievedResult = retrievedResponse.Result;
        }
    }
}
```

### Go

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://pkg.go.dev/cloud.google.com/go/dataplex)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
//go:build examples

package main

import (
	"context"

	dataplex "cloud.google.com/go/dataplex/apiv1"
	dataplexpb "cloud.google.com/go/dataplex/apiv1/dataplexpb"
)

func main() {
	ctx := context.Background()
	// This snippet has been automatically generated and should be regarded as a code template only.
	// It will require modifications to work:
	// - It may require correct/in-range values for request initialization.
	// - It may require specifying regional endpoints when creating the service client as shown in:
	//   https://pkg.go.dev/cloud.google.com/go#hdr-Client_Options
	c, err := dataplex.NewDataScanClient(ctx)
	if err != nil {
		// TODO: Handle error.
	}
	defer c.Close()

	req := &dataplexpb.CreateDataScanRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/dataplex/apiv1/dataplexpb#CreateDataScanRequest.
	}
	op, err := c.CreateDataScan(ctx, req)
	if err != nil {
		// TODO: Handle error.
	}

	resp, err := op.Wait(ctx)
	if err != nil {
		// TODO: Handle error.
	}
	// TODO: Use resp.
	_ = resp
}
```

### Java

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-dataplex/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import com.google.cloud.dataplex.v1.CreateDataScanRequest;
import com.google.cloud.dataplex.v1.DataScan;
import com.google.cloud.dataplex.v1.DataScanServiceClient;
import com.google.cloud.dataplex.v1.LocationName;

public class SyncCreateDataScan {

  public static void main(String[] args) throws Exception {
    syncCreateDataScan();
  }

  public static void syncCreateDataScan() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DataScanServiceClient dataScanServiceClient = DataScanServiceClient.create()) {
      CreateDataScanRequest request =
          CreateDataScanRequest.newBuilder()
              .setParent(LocationName.of("[PROJECT]", "[LOCATION]").toString())
              .setDataScan(DataScan.newBuilder().build())
              .setDataScanId("dataScanId1260787906")
              .setValidateOnly(true)
              .build();
      DataScan response = dataScanServiceClient.createDataScanAsync(request).get();
    }
  }
}
```

### Python

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/dataplex/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.api_core.exceptions
from google.cloud import dataplex_v1


def create_data_profile_scan_global(
    project_id: str,
    dataset_id: str,
    table_id: str,
    location: str,
) -> None:
    """Creates a Dataplex Data Profile Scan using global API endpoint routing.

    Args:
        project_id (str): Google Cloud project ID where the scan is created.
        dataset_id (str): Target BigQuery dataset ID.
        table_id (str): Target BigQuery table ID to scan.
        location (str): Google Cloud region where serverless compute runs.
    """
    client = dataplex_v1.DataScanServiceClient()

    parent = client.common_location_path(project=project_id, location=location)

    bigquery_table = (
        f"//bigquery.googleapis.com/projects/{project_id}"
        f"/datasets/{dataset_id}/tables/{table_id}"
    )

    data_profile_spec = dataplex_v1.DataProfileSpec(sampling_percent=100.0)

    data_scan = dataplex_v1.DataScan(
        display_name="Global Data Profile Scan",
        description="Regional data profile scan generating automated table statistics.",
        data=dataplex_v1.DataSource(resource=bigquery_table),
        data_profile_spec=data_profile_spec,
    )

    request = dataplex_v1.CreateDataScanRequest(
        parent=parent,
        data_scan=data_scan,
    )

    try:
        operation = client.create_data_scan(request=request)
        print(operation.result())

    except google.api_core.exceptions.AlreadyExists:
        print("A scan with this ID already exists.")
    except google.api_core.exceptions.InvalidArgument as e:
        print(f"Your scan configuration is invalid: {e}")
    except google.api_core.exceptions.GoogleAPIError as e:
        print(f"Unexpected exception: {e}")
```

### Ruby

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 Ruby 設定操作說明進行操作。詳情請參閱 [BigQuery Ruby API 參考文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-dataplex/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
require "google/cloud/dataplex/v1"

##
# Snippet for the create_data_scan call in the DataScanService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::Dataplex::V1::DataScanService::Client#create_data_scan.
#
def create_data_scan
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::Dataplex::V1::DataScanService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::Dataplex::V1::CreateDataScanRequest.new

  # Call the create_data_scan method.
  result = client.create_data_scan request

  # The returned object is of type Gapic::Operation. You can use it to
  # check the status of an operation, cancel it, or wait for results.
  # Here is how to wait for a response.
  result.wait_until_done! timeout: 60
  if result.response?
    p result.response
  else
    puts "No response received."
  end
end
```

### REST

如要建立資料剖析掃描，請使用 [`dataScans.create` 方法](https://docs.cloud.google.com/knowledge-catalog/docs/reference/rest/v1/projects.locations.dataScans/create?hl=zh-tw)。

**注意：** 如果 BigQuery 資料表的 `Require
partition filter` 設定設為 `true`，請使用資料表的分區欄，做為資料剖析掃描作業的資料列篩選器或時間戳記欄。

## 建立多項資料剖析掃描作業

您可以使用 Google Cloud 控制台，同時為 BigQuery 資料集中的多個資料表設定資料剖析掃描。

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 點按「建立資料剖析掃描」。
3. 選取「Multiple data profile scans」(多項資料剖析掃描作業) 選項。
4. 輸入**ID 前置字串**。Knowledge Catalog 會使用提供的前置字串和不重複的後置字串，自動產生掃描 ID。
5. 輸入所有資料剖析掃描作業的**說明**。
6. 在「Dataset」(資料集) 欄位中，按一下「Browse」(瀏覽)。選取要從中挑選資料表的資料集。按一下「選取」。
7. 如果資料集為多區域，請選取要建立資料剖析掃描作業的「Region」(區域)。
8. 在「模式」部分，選擇下列任一選項：

   * **標準**：使用可自訂的掃描設定剖析資料。此為預設模式。
   * **輕量**：透過低延遲、低精確度的掃描，快速提供洞察資料。這項功能為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。
9. 如果選擇「Standard」(標準) 模式，請為掃描作業進行下列設定。如果選取「輕量」模式，就不會顯示這些設定。

   1. 在「Scope」(範圍) 欄位中，選擇「Incremental」(增量) 或「Entire data」(完整資料)。

      如果選擇「Incremental」(增量) 資料，則只能選取依 `DATE` 或 `TIMESTAMP` 類型資料欄分區的資料表。
   2. 如要對資料剖析掃描套用取樣，請在「Sampling size」(取樣大小) 清單中選取取樣百分比。

      請選擇介於 0.0% 至 100.0% 之間的百分比值，最多可到小數點後 3 位。
10. 選用：在Google Cloud 控制台的 BigQuery 和 Knowledge Catalog 頁面中，發布來源資料表的資料剖析掃描結果。勾選「Publish results to Knowledge Catalog」(將結果發布至 Knowledge Catalog) 核取方塊。

    您可以在來源資料表的 BigQuery 和 Knowledge Catalog 頁面中，透過「Data profile」(資料剖析) 分頁查看最新的掃描結果。如要允許使用者存取已發布的掃描結果，請參閱本文的「[授予資料剖析掃描結果的存取權](#share-results)」一節。

    **注意：** 您必須選擇沒有任何現有掃描作業發布結果的資料表。
11. 在「Schedule」(時間表) 部分，選擇下列其中一個選項：

    * **重複**：按照排程執行資料剖析掃描，頻率可設為每小時、每天、每週、每月或自訂。指定掃描作業的執行頻率和時間。如果選擇自訂，請使用 [cron](https://en.wikipedia.org/wiki/Cron) 格式指定排程。
    * **依需求**：依需求執行資料剖析掃描。

      + **執行一次**：立即執行資料剖析掃描作業一次，並在自動刪除時間後移除掃描作業。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

        - **設定掃描後結果自動刪除**：自動刪除時間定義資料剖析掃描執行後，保持有效的時間長度。如果未指定自動刪除時間，資料剖析掃描作業會在 24 小時後自動移除。自動刪除時間可介於 0 秒 (立即刪除) 到 365 天。
12. 按一下「繼續」。
13. 在「Choose tables」(選擇資料表) 欄位中，按一下「Browse」(瀏覽)。選擇一或多個要掃描的資料表，然後按一下「Select」(選取)。
14. 按一下「繼續」。
15. 選用：將掃描結果匯出至 BigQuery 標準資料表。在「Export scan results to BigQuery table」(將掃描結果匯出至 BigQuery 資料表) 區段中，執行下列操作：

    1. 在「選取 BigQuery 資料集」欄位中，按一下「瀏覽」。選取要儲存資料剖析掃描結果的 BigQuery 資料集。
    2. 在「BigQuery table」(BigQuery 資料表) 欄位中，指定要儲存資料剖析掃描結果的資料表。如果使用現有資料表，請確認該資料表與[匯出資料表結構定義](https://docs.cloud.google.com/knowledge-catalog/docs/use-data-profiling?hl=zh-tw#table-schema)相容。如果指定的資料表不存在，Knowledge Catalog 會為您建立。

       Knowledge Catalog 會針對所有資料剖析掃描作業使用相同的結果資料表。
16. 選用：新增標籤。標籤是鍵/值組合，可用來將相關物件分組，或與其他 Google Cloud 資源組合。
17. 如要建立掃描作業，請按一下「Create」(建立)。

    如果將排程設為「隨選」，也可以立即執行掃描，只要按一下「執行掃描」即可。

## 執行資料剖析掃描

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 點選要執行的資料剖析掃描作業。
3. 點選「立即執行」。

### gcloud

如要執行資料剖析掃描，請使用 [`gcloud dataplex datascans run` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/run?hl=zh-tw)：

```
gcloud dataplex datascans run DATASCAN \
--location=LOCATION
```

請替換下列變數：

* `DATASCAN`：資料剖析掃描作業的名稱。
* `LOCATION`：建立資料剖析掃描作業的 Google Cloud 區域。

### C#

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 C# 設定操作說明進行操作。詳情請參閱 [BigQuery C# API 參考文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.Dataplex.V1/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
using Google.Cloud.Dataplex.V1;

public sealed partial class GeneratedDataScanServiceClientSnippets
{
    /// <summary>Snippet for RunDataScan</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void RunDataScanRequestObject()
    {
        // Create client
        DataScanServiceClient dataScanServiceClient = DataScanServiceClient.Create();
        // Initialize request argument(s)
        RunDataScanRequest request = new RunDataScanRequest
        {
            DataScanName = DataScanName.FromProjectLocationDataScan("[PROJECT]", "[LOCATION]", "[DATASCAN]"),
        };
        // Make the request
        RunDataScanResponse response = dataScanServiceClient.RunDataScan(request);
    }
}
```

### Go

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://pkg.go.dev/cloud.google.com/go/dataplex)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
//go:build examples

package main

import (
	"context"

	dataplex "cloud.google.com/go/dataplex/apiv1"
	dataplexpb "cloud.google.com/go/dataplex/apiv1/dataplexpb"
)

func main() {
	ctx := context.Background()
	// This snippet has been automatically generated and should be regarded as a code template only.
	// It will require modifications to work:
	// - It may require correct/in-range values for request initialization.
	// - It may require specifying regional endpoints when creating the service client as shown in:
	//   https://pkg.go.dev/cloud.google.com/go#hdr-Client_Options
	c, err := dataplex.NewDataScanClient(ctx)
	if err != nil {
		// TODO: Handle error.
	}
	defer c.Close()

	req := &dataplexpb.RunDataScanRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/dataplex/apiv1/dataplexpb#RunDataScanRequest.
	}
	resp, err := c.RunDataScan(ctx, req)
	if err != nil {
		// TODO: Handle error.
	}
	// TODO: Use resp.
	_ = resp
}
```

### Java

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-dataplex/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import com.google.cloud.dataplex.v1.DataScanName;
import com.google.cloud.dataplex.v1.DataScanServiceClient;
import com.google.cloud.dataplex.v1.RunDataScanRequest;
import com.google.cloud.dataplex.v1.RunDataScanResponse;

public class SyncRunDataScan {

  public static void main(String[] args) throws Exception {
    syncRunDataScan();
  }

  public static void syncRunDataScan() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DataScanServiceClient dataScanServiceClient = DataScanServiceClient.create()) {
      RunDataScanRequest request =
          RunDataScanRequest.newBuilder()
              .setName(DataScanName.of("[PROJECT]", "[LOCATION]", "[DATASCAN]").toString())
              .build();
      RunDataScanResponse response = dataScanServiceClient.runDataScan(request);
    }
  }
}
```

### Python

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/dataplex/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import dataplex_v1


def sample_run_data_scan():
    # Create a client
    client = dataplex_v1.DataScanServiceClient()

    # Initialize request argument(s)
    request = dataplex_v1.RunDataScanRequest(
        name="name_value",
    )

    # Make the request
    response = client.run_data_scan(request=request)

    # Handle the response
    print(response)
```

### Ruby

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 Ruby 設定操作說明進行操作。詳情請參閱 [BigQuery Ruby API 參考文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-dataplex/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
require "google/cloud/dataplex/v1"

##
# Snippet for the run_data_scan call in the DataScanService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::Dataplex::V1::DataScanService::Client#run_data_scan.
#
def run_data_scan
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::Dataplex::V1::DataScanService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::Dataplex::V1::RunDataScanRequest.new

  # Call the run_data_scan method.
  result = client.run_data_scan request

  # The returned object is of type Google::Cloud::Dataplex::V1::RunDataScanResponse.
  p result
end
```

### REST

如要執行資料剖析掃描，請使用 [`dataScans.run` 方法](https://docs.cloud.google.com/knowledge-catalog/docs/reference/rest/v1/projects.locations.dataScans/run?hl=zh-tw)。

### Airflow

如要在 [Managed Service for Apache Airflow (Cloud Composer)](https://docs.cloud.google.com/composer/docs?hl=zh-tw) 中，使用有向無環圖 (DAG) 執行資料剖析掃描，請使用 [`DataplexRunDataProfileScanOperator`](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/dataplex/index.html#airflow.providers.google.cloud.operators.dataplex.DataplexRunDataProfileScanOperator)：

```
from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.operators.dataplex import DataplexRunDataProfileScanOperator

with DAG(
  "dataplex_data_profile_scan",
  start_date=datetime(2026, 1, 1),
  schedule_interval="@daily",
  catchup=False,
) as dag:

  run_profile_scan = DataplexRunDataProfileScanOperator(
      task_id="run_dataplex_profile_scan",
      project_id="PROJECT_ID",
      region="REGION",
      data_scan_id="DATASCAN_ID",
  )
```

請替換下列變數：

* `PROJECT_ID`： Google Cloud 專案 ID。
* `REGION`：建立資料剖析掃描作業的 Google Cloud 區域。
* `DATASCAN_ID`：資料剖析掃描作業的 ID。

**注意：** 如果資料剖析掃描作業只執行一次，就無法執行。

## 查看資料剖析掃描結果

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下資料剖析掃描作業的名稱。

   * 「Overview」(總覽) 專區會顯示最近工作的相關資訊，包括掃描執行時間、掃描的資料表記錄數量，以及工作狀態。
   * 「Data profile scan configuration」(資料剖析掃描設定) 專區會顯示掃描作業的詳細資料。
3. 如要查看工作的詳細資訊，例如掃描的資料表欄、掃描中找到的欄統計資料，以及工作記錄，請按一下「Jobs history」(工作記錄) 分頁標籤。然後點選工作 ID。

**注意：** 如果您將掃描結果匯出至 BigQuery 資料表，也可以從資料表存取掃描結果。

### gcloud

如要查看資料剖析掃描工作的結果，請使用 [`gcloud dataplex datascans jobs describe` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/jobs/describe?hl=zh-tw)：

```
gcloud dataplex datascans jobs describe JOB \
--location=LOCATION \
--datascan=DATASCAN \
--view=FULL
```

請替換下列變數：

* `JOB`：資料剖析掃描工作的工作 ID。
* `LOCATION`：建立資料剖析掃描作業的 Google Cloud 區域。
* `DATASCAN`：工作所屬資料剖析掃描作業的名稱。
* `--view=FULL`：如要查看掃描工作結果，請指定 `FULL`。

### C#

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 C# 設定操作說明進行操作。詳情請參閱 [BigQuery C# API 參考文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.Dataplex.V1/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
using Google.Cloud.Dataplex.V1;

public sealed partial class GeneratedDataScanServiceClientSnippets
{
    /// <summary>Snippet for GetDataScan</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creating the service client as shown in
    ///   https://cloud.google.com/dotnet/docs/reference/help/client-configuration#endpoint.
    /// </remarks>
    public void GetDataScanRequestObject()
    {
        // Create client
        DataScanServiceClient dataScanServiceClient = DataScanServiceClient.Create();
        // Initialize request argument(s)
        GetDataScanRequest request = new GetDataScanRequest
        {
            DataScanName = DataScanName.FromProjectLocationDataScan("[PROJECT]", "[LOCATION]", "[DATASCAN]"),
            View = GetDataScanRequest.Types.DataScanView.Unspecified,
        };
        // Make the request
        DataScan response = dataScanServiceClient.GetDataScan(request);
    }
}
```

### Go

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://pkg.go.dev/cloud.google.com/go/dataplex)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
//go:build examples

package main

import (
	"context"

	dataplex "cloud.google.com/go/dataplex/apiv1"
	dataplexpb "cloud.google.com/go/dataplex/apiv1/dataplexpb"
)

func main() {
	ctx := context.Background()
	// This snippet has been automatically generated and should be regarded as a code template only.
	// It will require modifications to work:
	// - It may require correct/in-range values for request initialization.
	// - It may require specifying regional endpoints when creating the service client as shown in:
	//   https://pkg.go.dev/cloud.google.com/go#hdr-Client_Options
	c, err := dataplex.NewDataScanClient(ctx)
	if err != nil {
		// TODO: Handle error.
	}
	defer c.Close()

	req := &dataplexpb.GetDataScanRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/cloud.google.com/go/dataplex/apiv1/dataplexpb#GetDataScanRequest.
	}
	resp, err := c.GetDataScan(ctx, req)
	if err != nil {
		// TODO: Handle error.
	}
	// TODO: Use resp.
	_ = resp
}
```

### Java

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/knowledge-catalog/docs/reference/libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-dataplex/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import com.google.cloud.dataplex.v1.DataScan;
import com.google.cloud.dataplex.v1.
```