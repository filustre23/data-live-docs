Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 掃描資料品質問題

本文說明如何搭配使用 BigQuery 和 Knowledge Catalog，確保資料符合品質期望。Knowledge Catalog 自動資料品質功能可協助您定義及衡量 BigQuery 資料表中的資料品質。您可以自動掃描資料、根據定義的規則驗證資料，並在資料不符合品質規定時記錄警告。

如要進一步瞭解自動資料品質，請參閱「[自動資料品質總覽](https://docs.cloud.google.com/dataplex/docs/auto-data-quality-overview?hl=zh-tw)」。

**提示：** 本文中的步驟說明如何管理專案中的資料品質掃描作業。您也可以在處理特定資料表時，建立及管理資料品質掃描作業。詳情請參閱本文的「[管理特定資料表的資料品質掃描](#start-from-table)」一節。

## 事前準備

1. 啟用 Dataplex API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=dataplex.googleapis.com&hl=zh-tw)
2. 選用：如要讓 Knowledge Catalog 根據資料剖析掃描結果，產生資料品質規則建議，請[建立並執行資料剖析掃描作業](https://docs.cloud.google.com/bigquery/docs/data-profile-scan?hl=zh-tw)。

## 必要的角色

本節說明使用 Knowledge Catalog 資料品質掃描作業所需的 IAM 角色和權限。

### 使用者角色和權限

如要取得執行及管理資料品質掃描作業所需的權限，請要求管理員授予下列 IAM 角色：

* 對 BigQuery 資料表執行資料品質掃描：
  + 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
    ，可執行掃描工作
  + 在要掃描的 BigQuery 資料表上，按一下 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 將資料品質掃描結果發布至 Knowledge Catalog：
  + 掃描資料表的「BigQuery 資料編輯者」 (`roles/bigquery.dataEditor`)
  + [Dataplex Catalog 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.catalogEditor)  (`roles/dataplex.catalogEditor`)：在與表格相同位置的`@bigquery`項目群組上
* 對 `DataScan` 資源執行特定工作：
  + 專案的 [Dataplex DataScan 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.dataScanAdmin)  (`roles/dataplex.dataScanAdmin`)，可取得完整存取權
  + 專案的 [Dataplex DataScan 建立者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.dataScanCreator)  (`roles/dataplex.dataScanCreator`)，可建立掃描作業
  + 專案的「Dataplex DataScan 編輯者」 (`roles/dataplex.dataScanEditor`) 寫入存取權
  + 專案的 [Dataplex DataScan 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.dataScanViewer)  (`roles/dataplex.dataScanViewer`)，可讀取掃描中繼資料
  + 專案的 [Dataplex DataScan 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.dataScanDataViewer)  (`roles/dataplex.dataScanDataViewer`)，可讀取掃描資料，包括規則和結果

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行及管理資料品質掃描作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行及管理資料品質掃描作業，必須具備下列權限：

* 對 BigQuery 資料表執行資料品質掃描：
  + 專案的 `bigquery.jobs.create` 權限，以便執行掃描工作
  + `bigquery.tables.get`
    要掃描的 BigQuery 資料表
  + `bigquery.tables.getData`
    要掃描的 BigQuery 資料表
* 將資料品質掃描結果發布至 Knowledge Catalog：
  + `bigquery.tables.update`
    掃描的資料表
  + `dataplex.entryGroups.useDataQualityScorecardAspect`
    位於與資料表相同位置的 `@bigquery` 項目群組
* 建立 `DataScan`：
  `dataplex.datascans.create`
  在專案中
* 刪除 `DataScan`：
  `dataplex.datascans.delete`
  專案
* 查看 `DataScan` 中繼資料：
  `dataplex.datascans.get`
  在專案上
* 查看 `DataScan` 詳細資料，包括規則和結果：
  `dataplex.datascans.getData`
  在專案上
* 列出專案的 `DataScan`：
  `dataplex.datascans.list`
* 執行 `DataScan`：
  `dataplex.datascans.run`
  專案
* 更新專案中的 `DataScan`：
  `dataplex.datascans.update`
* 取得或設定 `DataScan` 的 IAM 政策：
  + 專案的 `dataplex.datascans.getIamPolicy`
  + 專案的 `dataplex.datascans.setIamPolicy`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要存取受 BigQuery 資料欄層級存取政策保護的資料欄，您也需要這些資料欄的權限。

**注意：** Knowledge Catalog 不會在專案中建立 BigQuery 工作，進行資料品質掃描。不過，您需要 `bigquery.jobs.create` 權限才能建立 `DryRun` 工作，以檢查資料表的權限。

### Knowledge Catalog 服務帳戶角色和權限

如果您尚未建立任何資料品質或資料剖析掃描作業，或是在這個專案中沒有 Knowledge Catalog 湖泊，請執行下列指令建立服務 ID：
`gcloud beta services identity create --service=dataplex.googleapis.com`。
如果存在，這項指令會傳回 Knowledge Catalog 服務 ID。

為確保含有資料品質掃描作業的專案，其 Knowledge Catalog 服務帳戶具備從各種來源讀取資料及匯出結果的必要權限，請要求管理員將下列 IAM 角色授予含有資料品質掃描作業的專案，其 Knowledge Catalog 服務帳戶：

**重要事項：**您必須將這些角色授予含有資料品質掃描的專案的 Knowledge Catalog 服務帳戶，*而非*使用者帳戶。如果未將角色授予正確的主體，可能會導致權限錯誤。

* 讀取 BigQuery 資料表資料：
  掃描的 BigQuery 資料表和規則中參照的任何其他資料表，都必須具備 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`) 權限。
* 讀取 Iceberg REST 目錄資料表資料：
  [BigLake 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-tw#biglake.viewer)  (`roles/biglake.viewer`)
  掃描 Iceberg REST 目錄資料表，以及規則中參照的任何其他資料表
* 將掃描結果匯出至 BigQuery 資料表：
  結果資料集和資料表的「BigQuery 資料編輯者」 (`roles/bigquery.dataEditor`)
* 掃描 Knowledge Catalog lake 中整理的 BigQuery 資料：
  + [Dataplex 中繼資料讀取者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.metadataReader)  (`roles/dataplex.metadataReader`)
    Dataplex 資源
  + [Dataplex 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.viewer)  (`roles/dataplex.viewer`)
    Dataplex 資源
* 從 Cloud Storage 掃描 BigQuery 外部資料表：
  Cloud Storage bucket 的「Storage Object Viewer」 (`roles/storage.objectViewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備從各種來源讀取資料及匯出結果所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要從各種來源讀取資料及匯出結果，必須具備下列權限：

* 讀取 BigQuery 資料表資料：
  + `bigquery.tables.get`
    BigQuery 資料表
  + `bigquery.tables.getData`
    BigQuery 資料表
* 將掃描結果匯出至 BigQuery 資料表：
  + `bigquery.datasets.get`
    結果資料集和資料表
  + `bigquery.tables.create`
    結果資料集和資料表
  + `bigquery.tables.get`
    結果資料集和資料表
  + `bigquery.tables.getData`
    結果資料集和資料表
  + `bigquery.tables.update`
    結果資料集和資料表
  + `bigquery.tables.updateData`
    結果資料集和資料表
* 掃描 Knowledge Catalog lake 中整理的 BigQuery 資料：
  + `dataplex.lakes.list`
    Dataplex 資源
  + `dataplex.lakes.get`
    Dataplex 資源
  + `dataplex.zones.list`
    Dataplex 資源
  + `dataplex.zones.get`
    Dataplex 資源
  + `dataplex.entities.list`
    Dataplex 資源
  + `dataplex.entities.get`
    Dataplex 資源
  + `dataplex.operations.get`
    Dataplex 資源
* 從 Cloud Storage 掃描 BigQuery 外部資料表：
  + `storage.buckets.get`
    Cloud Storage bucket
  + `storage.objects.get`
    Cloud Storage bucket

管理員或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，將這些權限授予包含資料品質掃描的專案 Knowledge Catalog 服務帳戶。

如要存取受 BigQuery 資料欄層級存取權政策保護的資料欄，請為這些資料欄指派 Knowledge Catalog 服務帳戶權限。

如果資料表已啟用 BigQuery 資料列層級存取權政策，您只能掃描 Knowledge Catalog 服務帳戶可見的資料列。請注意，系統不會評估個別使用者的存取權限是否符合資料列層級政策。

## 建立資料品質掃描作業

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下「建立資料品質掃描作業」。
3. 在「定義掃描」視窗中，填入下列欄位：

   1. (選用) 輸入「Display name」(顯示名稱)。
   2. 輸入 ID。請參閱[資源命名慣例](https://docs.cloud.google.com/compute/docs/naming-resources?hl=zh-tw#resource-name-format)。
   3. 選用：輸入**說明**。
   4. 在「Table」(資料表) 欄位中，按一下「Browse」(瀏覽)。選擇要掃描的資料表，然後按一下「選取」。系統僅支援標準 BigQuery 和 Iceberg REST 目錄資料表。

      如為多區域資料集內的資料表，請選擇要建立資料掃描的區域。

      如要瀏覽 Knowledge Catalog 湖泊中的資料表，請按一下「Browse within Knowledge Catalog Lakes」(在 Knowledge Catalog 湖泊中瀏覽)。
   5. 在「範圍」欄位中，選擇「增量」或「完整資料」。

      * 如果選擇「增量」：在「時間戳記欄」欄位中，從 BigQuery 資料表選取 `DATE` 或 `TIMESTAMP` 類型的資料欄，這類資料欄的值只會增加，可用於識別新的記錄。另外，這類資料欄也可用來將資料表分區。
   6. 如要篩選資料，請選取「篩選列」核取方塊。提供由有效 SQL 運算式組成的資料列篩選器，該運算式可用於 GoogleSQL 語法的 [`WHERE` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#where_clause)。例如：`col1 >= 0`。篩選器可由多個資料欄條件組合而成。例如：`col1 >= 0 AND col2 < 10`。
   7. 如要對資料取樣，請在「取樣大小」清單中選取取樣百分比。請選擇介於 0.0% 和 100.0% 之間的百分比值，最多可有 3 位小數。如果是較大的資料集，請選擇較低的取樣百分比。舉例來說，如果資料表大小為 1 PB，且您輸入的值介於 0.1% 到 1.0% 之間，資料品質掃描就會取樣 1 到 10 TB 的資料。如果是增量資料掃描，資料品質掃描會對最新增量套用取樣。
   8. 如要將資料品質掃描結果發布為 Knowledge Catalog 中繼資料，請選取「將結果發布至 Knowledge Catalog」核取方塊。

      您可以在來源資料表的 BigQuery 和 Knowledge Catalog 頁面中，查看「資料品質」分頁標籤上的最新掃描結果。如要讓使用者存取已發布的掃描結果，請參閱本文的「[授予資料品質掃描結果的存取權](#share-results)」一節。
   9. 在「時間表」部分，選擇下列其中一個選項：

      * **重複**：按照排程執行資料品質掃描作業，排程可設為每小時、每天、每週、每月或自訂。指定掃描的執行頻率和時間。如果選擇自訂，請使用 [cron](https://en.wikipedia.org/wiki/Cron) 格式指定時間表。
      * **隨選**：按需求執行資料品質掃描作業。
      * **單次執行**：立即執行一次資料品質掃描，並在自動刪除時間過後移除掃描作業。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

        + **設定掃描後結果自動刪除時間**：自動刪除時間是指掃描執行到刪除之間的時間間隔。如果資料品質掃描作業未指定自動刪除時間，系統會在執行作業 24 小時後自動刪除。自動刪除時間範圍從 0 秒 (立即刪除) 到 365 天。
   10. 按一下「繼續」。
4. 在「資料品質規則」視窗中，定義要為這項資料品質掃描設定的規則。

   1. 按一下「新增規則」，然後選擇下列任一做法。

      * **以資料概況為基礎的建議**：根據現有的資料剖析掃描結果，從建議中建立規則。

        1. **選擇資料欄**：選取要取得建議規則的資料欄。
        2. **選擇掃描專案**：如果資料剖析掃描作業所在的專案，與您要建立資料品質掃描作業的專案不同，請選取要從哪個專案提取剖析掃描作業。
        3. **選擇資料概況結果**：選取一或多個資料概況結果，然後按一下「確定」。系統會根據這些資訊產生建議規則清單，供您做為起點。
        4. 找出要新增的規則，勾選對應的核取方塊，然後按一下「選取」。選取後，規則會新增至目前的規則清單。接著即可編輯規則。
      * **內建規則類型**：根據預先定義的規則建立規則。
        請參閱[預先定義的規則](https://docs.cloud.google.com/dataplex/docs/auto-data-quality-overview?hl=zh-tw#predefined-rules)清單。

        1. **選擇資料欄**：選取要套用規則的資料欄。
        2. **選擇規則類型**：選取要選擇的規則類型，然後按一下「確定」。顯示的規則類型取決於您選取的資料欄。
        3. 找出要新增的規則，勾選對應的核取方塊，然後按一下「選取」。選取後，規則會新增至目前的規則清單。接著即可編輯規則。
      * **SQL 資料列檢查規則**：建立要套用至每個資料列的自訂 SQL 規則。

        1. 在「維度」中，選擇一個維度。
        2. 在「通過門檻」中，選擇必須通過檢查的記錄百分比。
        3. 在「欄名稱」中選擇資料欄。
        4. 在「提供 SQL 運算式」欄位中，輸入評估結果為布林值 `true` (通過) 或 `false` (失敗) 的 SQL 運算式。詳情請參閱「[支援的自訂 SQL 規則類型](https://docs.cloud.google.com/dataplex/docs/auto-data-quality-overview?hl=zh-tw#supported-custom-sql-rule-types)」和「[定義資料品質規則](https://docs.cloud.google.com/dataplex/docs/use-auto-data-quality?hl=zh-tw#sample-rules)」中的範例。
        5. 按一下「新增」。
      * **SQL 匯總檢查規則**：建立自訂 SQL 資料表條件規則。

        1. 在「維度」中，選擇一個維度。
        2. 在「欄名稱」中選擇資料欄。
        3. 在「提供 SQL 運算式」欄位中，輸入評估結果為布林值 `true` (通過) 或 `false` (失敗) 的 SQL 運算式。詳情請參閱「[支援的自訂 SQL 規則類型](https://docs.cloud.google.com/dataplex/docs/auto-data-quality-overview?hl=zh-tw#supported-custom-sql-rule-types)」和「[定義資料品質規則](https://docs.cloud.google.com/dataplex/docs/use-auto-data-quality?hl=zh-tw#sample-rules)」中的範例。
        4. 按一下「新增」。
      * **SQL 斷言規則**：建立自訂 SQL 斷言規則，檢查資料是否處於無效狀態。

        1. 在「維度」中，選擇一個維度。
        2. 選用：在「欄名稱」中選擇欄。
        3. 在「Provide a SQL statement」(提供 SQL 陳述式) 欄位中，輸入會傳回符合無效狀態資料列的 SQL 陳述式。如果傳回任何資料列，即代表這項規則失敗。請省略 SQL 陳述式結尾的分號。詳情請參閱「[支援的自訂 SQL 規則類型](https://docs.cloud.google.com/dataplex/docs/auto-data-quality-overview?hl=zh-tw#supported-custom-sql-rule-types)」和「[定義資料品質規則](https://docs.cloud.google.com/dataplex/docs/use-auto-data-quality?hl=zh-tw#sample-rules)」中的範例。
        4. 按一下「新增」。
   2. 選用：您可以為任何資料品質規則指派自訂規則名稱，用於監控和快訊，以及說明。如要這麼做，請編輯規則並指定下列詳細資料：

      * **規則名稱**：輸入自訂規則名稱，長度上限為 63 個半形字元。
        規則名稱可包含英文字母 (a-z、A-Z)、數字 (0-9) 和連字號 (-)，且開頭須為英文字母，結尾須為數字或英文字母。
      * **說明**：輸入規則說明，長度上限為 1,024 個字元。
   3. 重複上述步驟，在資料品質掃描中新增其他規則。完成後，按一下「繼續」。
5. 選用步驟：將掃描結果匯出至 BigQuery 標準資料表。在「將掃描結果匯出至 BigQuery 資料表」部分，執行下列操作：

   1. 在「選取 BigQuery 資料集」欄位中，按一下「瀏覽」。選取用來儲存資料品質掃描結果的 BigQuery 資料集。
   2. 在「BigQuery table」(BigQuery 資料表) 欄位中，指定要儲存資料品質掃描結果的資料表。如果使用現有資料表，請確認該資料表與[匯出資料表結構定義](https://docs.cloud.google.com/dataplex/docs/use-auto-data-quality?hl=zh-tw#table-schema)相容。如果指定的資料表不存在，Knowledge Catalog 會為您建立。

      **注意：** 您可以為多項資料品質掃描作業使用同一個結果資料表。
6. 選用：新增標籤。標籤是鍵/值組合，可用來將相關物件分組，或與其他 Google Cloud 資源組合。
7. 選用：設定電子郵件通知報告，在資料品質掃描工作完成時通知使用者。在「通知報表」部分，按一下「新增電子郵件 ID」add，然後輸入最多五個電子郵件地址。然後選取要傳送報表的狀況：

   * **品質分數 (<=)**：如果作業成功，但資料品質分數低於指定目標分數，系統就會傳送報表。輸入介於 0 到 100 之間的目標品質分數。
   * **工作失敗**：無論資料品質結果如何，只要工作本身失敗，就會傳送報表。
   * **工作完成 (成功或失敗)**：工作結束時傳送報表，無論資料品質結果為何。
8. 點選「建立」。

   掃描作業建立完成後，只要按一下「立即執行」，即可隨時執行掃描。

### gcloud

如要建立資料品質掃描作業，請使用 [`gcloud dataplex datascans create data-quality` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/create/data-quality?hl=zh-tw)。

如果來源資料是儲存在 Knowledge Catalog lake 中，請加入 `--data-source-entity` 旗標：

```
gcloud dataplex datascans create data-quality DATASCAN \
    --location=LOCATION \
    --data-quality-spec-file=DATA_QUALITY_SPEC_FILE \
    --data-source-entity=DATA_SOURCE_ENTITY
```

如果來源資料並非在 Knowledge Catalog 湖泊中整理，請加入 `--data-source-resource` 旗標：

```
gcloud dataplex datascans create data-quality DATASCAN \
    --location=LOCATION \
    --data-quality-spec-file=DATA_QUALITY_SPEC_FILE \
    --data-source-resource=DATA_SOURCE_RESOURCE
```

請替換下列變數：

* `DATASCAN`：資料品質掃描的名稱。
* `LOCATION`：要建立資料品質掃描的 Google Cloud 區域。
* `DATA_QUALITY_SPEC_FILE`：含有資料品質掃描規格的 JSON 或 YAML 檔案路徑。檔案可以是本機檔案，也可以是前置字串為 `gs://` 的 Cloud Storage 路徑。使用這個檔案指定掃描的資料品質規則。您也可以在這個檔案中指定其他詳細資料，例如篩選器、取樣百分比，以及掃描後動作，像是匯出至 BigQuery 或傳送電子郵件通知報告。請參閱 [JSON 表示法的說明文件](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/DataQualitySpec?hl=zh-tw)和[YAML 表示法範例](https://docs.cloud.google.com/dataplex/docs/use-auto-data-quality?hl=zh-tw#create-scan-using-gcloud)。
* `DATA_SOURCE_ENTITY`：包含資料品質掃描資料的 Knowledge Catalog 實體。例如：`projects/test-project/locations/test-location/lakes/test-lake/zones/test-zone/entities/test-entity`。
* `DATA_SOURCE_RESOURCE`：包含資料品質掃描資料的資源名稱。例如：`//bigquery.googleapis.com/projects/test-project/datasets/test-dataset/tables/test-table`。

### C#

### C#

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

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
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

### Node.js

### Node.js

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
// Copyright 2026 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// ** This file is automatically generated by gapic-generator-typescript. **
// ** https://github.com/googleapis/gapic-generator-typescript **
// ** All changes to this file may be overwritten. **



'use strict';

function main(parent, dataScan, dataScanId) {
  /**
   * This snippet has been automatically generated and should be regarded as a code template only.
   * It will require modifications to work.
   * It may require correct/in-range values for request initialization.
   * TODO(developer): Uncomment these variables before running the sample.
   */
  /**
   *  Required. The resource name of the parent location:
   *  `projects/{project}/locations/{location_id}`
   *  where `project` refers to a *project_id* or *project_number* and
   *  `location_id` refers to a Google Cloud region.
   */
  // const parent = 'abc123'
  /**
   *  Required. DataScan resource.
   */
  // const dataScan = {}
  /**
   *  Required. DataScan identifier.
   *  * Must contain only lowercase letters, numbers and hyphens.
   *  * Must start with a letter.
   *  * Must end with a number or a letter.
   *  * Must be between 1-63 characters.
   *  * Must be unique within the customer project / location.
   */
  // const dataScanId = 'abc123'
  /**
   *  Optional. Only validate the request, but do not perform mutations.
   *  The default is `false`.
   */
  // const validateOnly = true

  // Imports the Dataplex library
  const {DataScanServiceClient} = require('@google-cloud/dataplex').v1;

  // Instantiates a client
  const dataplexClient = new DataScanServiceClient();

  async function callCreateDataScan() {
    // Construct request
    const request = {
      parent,
      dataScan,
      dataScanId,
    };

    // Run request
    const [operation] = await dataplexClient.createDataScan(request);
    const [response] = await operation.promise();
    console.log(response);
  }

  callCreateDataScan();
}

process.on('unhandledRejection', err => {
  console.error(err.message);
  process.exitCode = 1;
});
main(...process.argv.slice(2));
```

### Python

### Python

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


def sample_create_data_scan():
    # Create a client
    client = dataplex_v1.DataScanServiceClient()

    # Initialize request argument(s)
    data_scan = dataplex_v1.DataScan()
    data_scan.data.entity = "entity_value"

    request = dataplex_v1.CreateDataScanRequest(
        parent="parent_value",
        data_scan=data_scan,
        data_scan_id="data_scan_id_value",
    )

    # Make the request
    operation = client.create_data_scan(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)
```

### Ruby

### Ruby

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

如要建立資料品質掃描作業，請使用 [`dataScans.create` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/create?hl=zh-tw)。

下列要求會建立單次資料品質掃描作業：

```
POST https://dataplex.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataScans?data_scan_id=DATASCAN_ID

{
"data": {
  "resource": "//bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID"
},
"type": "DATA_QUALITY",
"executionSpec": {
  "trigger": {
    "oneTime": {
      "ttl_after_scan_completion": "120s"
    }
  }
},
"dataQualitySpec": {
  "rules": [
    {
      "nonNullExpectation": {},
      "column": "COLUMN_NAME",
      "dimension": "DIMENSION",
      "threshold": 1
    }
  ],
  "filter": "FILTER_CONDITION"
}
}
```

更改下列內容：

* `PROJECT_ID`：專案 ID。
* `LOCATION`：要建立資料品質掃描作業的區域。
* `DATASCAN_ID`：資料品質掃描的 ID。
* `DATASET_ID`：BigQuery 資料集的 ID。
* `TABLE_ID`：BigQuery 資料表的 ID。
* `COLUMN_NAME`：規則的資料欄名稱。
* `DIMENSION`：規則的維度，例如 `VALIDITY`。
* `FILTER_CONDITION`：選用的 [AIP-160 篩選器字串](https://docs.cloud.google.com/dataplex/docs/auto-data-quality-overview?hl=zh-tw#rule-filtering)，可選擇性地執行規則 (例如 `name = \"RULE_NAME\"`)。

如要根據資料剖析掃描結果，使用規則建議建立資料品質掃描規則，請對資料剖析掃描呼叫 [`dataScans.jobs.generateDataQualityRules` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans.jobs/generateDataQualityRules?hl=zh-tw)，取得建議。

**注意：**如果 BigQuery 資料表已將「需要分區篩選器」設為 `true`，請使用 BigQuery 分區資料欄做為資料品質掃描的資料列篩選器或時間戳記資料欄。

## 執行資料品質掃描

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下要執行的資料品質掃描作業。
3. 按一下「立即執行」。

### gcloud

如要執行資料品質掃描，請使用 [`gcloud dataplex datascans run` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/run?hl=zh-tw)：

```
gcloud dataplex datascans run DATASCAN \
--location=LOCATION \
```

請替換下列變數：

* `LOCATION`：建立資料品質掃描作業的 Google Cloud 區域。
* `DATASCAN`：資料品質掃描的名稱。

### C#

### C#

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

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
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

如要執行資料品質掃描，請使用 [`dataScans.run` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/run?hl=zh-tw)。

**注意：** 單次排程的資料品質掃描作業不支援執行。

## 查看資料品質掃描結果

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下資料品質掃描作業的名稱。

   * 「總覽」部分會顯示最近一次工作的相關資訊，包括掃描執行時間、每項工作掃描的記錄數量、所有資料品質檢查是否通過，以及失敗的資料品質檢查數量 (如有)。
   * 「資料品質掃描設定」部分會顯示掃描的詳細資料。
3. 如要查看工作的詳細資訊，例如指出通過規則百分比的資料品質分數、失敗的規則和工作記錄，請按一下「工作記錄」分頁標籤。然後按一下工作 ID。

**注意：** 如果您已將掃描結果匯出至 BigQuery 資料表，也可以從該資料表存取掃描結果。如果將掃描結果發布為 Knowledge Catalog 中繼資料，即可查看資料品質分數。

### gcloud

如要查看資料品質掃描工作的結果，請使用 [`gcloud dataplex datascans jobs describe` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/jobs/describe?hl=zh-tw)：

```
gcloud dataplex datascans jobs describe JOB \
--location=LOCATION \
--datascan=DATASCAN \
--view=FULL
```

請替換下列變數：

* `JOB`：資料品質掃描工作的 ID。
* `LOCATION`：建立資料品質掃描的 Google Cloud 區域。
* `DATASCAN`：工作所屬的資料品質掃描名稱。
* `--view=FULL`：如要查看掃描工作結果，請指定 `FULL`。

### C#

### C#

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

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
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

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import com.google.cloud.dataplex.v1.DataScan;
import com.google.cloud.dataplex.v1.DataScanName;
import com.google.cloud.dataplex.v1.DataScanServiceClient;
import com.google.cloud.dataplex.v1.GetDataScanRequest;

public class SyncGetDataScan {

  public static void main(String[] args) throws Exception {
    syncGetDataScan();
  }

  public static void syncGetDataScan() throws Exception {
    // This snippet has been automatically generated and should be regarded as a code template only.
    // It will require modifications to work:
    // - It may require correct/in-range values for request initialization.
    // - It may require specifying regional endpoints when creating the service client as shown in
    // https://cloud.google.com/java/docs/setup#configure_endpoints_for_the_client_library
    try (DataScanServiceClient dataScanServiceClient = DataScanServiceClient.create()) {
      GetDataScanRequest request =
          GetDataScanRequest.newBuilder()
              .setName(DataScanName.of("[PROJECT]", "[LOCATION]", "[DATASCAN]").toString())
              .build();
      DataScan response = dataScanServiceClient.getDataScan(request);
    }
  }
}
```

### Python

### Python

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


def sample_get_data_scan():
    # Create a client
    client = dataplex_v1.DataScanServiceClient()

    # Initialize request argument(s)
    request = dataplex_v1.GetDataScanRequest(
        name="name_value",
    )

    # Make the request
    response = client.get_data_scan(request=request)

    # Handle the response
    print(response)
```

### Ruby

### Ruby

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
require "google/cloud/dataplex/v1"

##
# Snippet for the get_data_scan call in the DataScanService service
#
# This snippet has been automatically generated and should be regarded as a code
# template only. It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
# client as shown in https://cloud.google.com/ruby/docs/reference.
#
# This is an auto-generated example demonstrating basic usage of
# Google::Cloud::Dataplex::V1::DataScanService::Client#get_data_scan.
#
def get_data_scan
  # Create a client object. The client can be reused for multiple calls.
  client = Google::Cloud::Dataplex::V1::DataScanService::Client.new

  # Create a request. To set request fields, pass in keyword arguments.
  request = Google::Cloud::Dataplex::V1::GetDataScanRequest.new

  # Call the get_data_scan method.
  result = client.get_data_scan request

  # The returned object is of type Google::Cloud::Dataplex::V1::DataScan.
  p result
end
```

### REST

如要查看資料品質掃描結果，請使用 [`dataScans.get` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/get?hl=zh-tw)。

### 查看已發布的結果

如果資料品質掃描結果發布為 Knowledge Catalog 中繼資料，您可以在Google Cloud 控制台的 BigQuery 和 Knowledge Catalog 頁面，以及來源資料表的「資料品質」分頁中，查看最新的掃描結果。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，按一下「Datasets」(資料集)，然後點選您的資料集。
4. 依序點按「總覽」**>「資料表」**，然後選取要查看資料品質掃描結果的資料表。
5. 按一下「資料品質」分頁標籤。

   系統會顯示最近發布的結果。

   **注意：** 如果這是首次執行掃描，可能無法查看已發布的結果。

### 查看歷來掃描結果

Knowledge Catalog 會儲存最近 300 項工作或過去一年的資料品質掃描記錄，以先到者為準。

### 控制台

1. 在 Google Cloud 控制台的 BigQuery「Metadata curation」(中繼資料管理) 頁面，前往「Data profiling & quality」(資料剖析與品質) 分頁。

   [前往「Data profiling & quality」(資料剖析與品質) 頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/data-profiling-and-quality?hl=zh-tw)
2. 按一下資料品質掃描作業的名稱。
3. 按一下「工作記錄」分頁標籤。

   「工作記錄」分頁提供過去工作相關資訊，例如每項工作掃描的記錄數量、工作狀態、工作執行時間，以及每項規則是否通過。
4. 如要查看工作的詳細資訊，請按一下「工作 ID」欄中的任何工作。

### gcloud

如要查看歷來資料品質掃描工作，請使用 [`gcloud dataplex datascans jobs list` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/jobs/list?hl=zh-tw)：

```
gcloud dataplex datascans jobs list \
--location=LOCATION \
--datascan=DATASCAN \
```

請替換下列變數：

* `LOCATION`：建立資料品質掃描的 Google Cloud 區域。
* `DATASCAN`：要查看歷史記錄作業的資料品質掃描名稱。

### C#

### C#

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[為本機開發環境設定驗證機制](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
using Google.Api.Gax;
using Google.Cloud.Dataplex.V1;
using System;

public sealed partial class GeneratedDataScanServiceClientSnippets
{
    /// <summary>Snippet for ListDataScanJobs</summary>
    /// <remarks>
    /// This snippet has been automatically generated and should be regarded as a code template only.
    /// It will require modifications to work:
    /// - It may require correct/in-range values for request initialization.
    /// - It may require specifying regional endpoints when creati
```