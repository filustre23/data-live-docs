* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查看及訂閱清單和資料交換

本文說明如何在 BigQuery sharing (舊稱 Analytics Hub) 中查看及訂閱項目和資料交換。BigQuery 共用訂閱者可以查看並訂閱自己有權存取的清單和資料交換。在 BigQuery sharing 中訂閱清單或資料交換，會在 Google Cloud 專案中建立連結的資料集。

## 必要的角色

如要取得使用目錄所需的權限，請要求 BigQuery 共用管理員在 BigQuery 共用訂閱者專案中，授予您下列身分與存取權管理 (IAM) 角色：

* [探索房源](#discover-listings)：
  [Analytics Hub 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`)
* [探索資料交換](#discover-data-exchanges)：
  [Analytics Hub 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.viewer) (`roles/analyticshub.viewer`)
* [訂閱項目](#subscribe-listings)：
  [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user) (`roles/bigquery.user`)

  + 如要訂閱項目，您也必須請 BigQuery sharing 項目發布端授予您項目、交換庫或專案的 [Analytics Hub 訂閱者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#analyticshub.subscriber) (`roles/analyticshub.subscriber`)，視您的用途最適合的範圍而定。
* [訂閱資料交易所](#subscribe-data-exchanges)：
  [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user) (`roles/bigquery.user`)

  + 如要在資料無塵室交換庫的環境中訂閱資料交換服務，您也必須請 BigQuery sharing 發布端，在特定資料無塵室中授予您 Analytics Hub 訂閱端角色 (`roles/analyticshub.subscriber`)。此外，您必須請 BigQuery sharing 訂閱者機構中的目標專案擁有者，在目標專案中授予您「Analytics Hub 訂閱擁有者」角色 (`roles/analyticshub.subscriptionOwner`)。
* [查看已連結的資料集](#view-linked-datasets)：
  [BigQuery 資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer)
  (`roles/bigquery.dataViewer`)
* [查詢已連結的資料集](#query-linked-datasets)：
  [BigQuery 資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer)
  (`roles/bigquery.dataViewer`)
* [更新已連結的資料集](#update-linked-datasets)：
  [BigQuery 資料擁有者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner)
  (`roles/bigquery.dataOwner`)
* [查看資料表的中繼資料](#view-table-metadata)：
  [BigQuery 資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer)
  (`roles/bigquery.dataViewer`)
* [刪除已連結的資料集](#delete-linked-datasets)：
  [BigQuery 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)
  (`roles/bigquery.admin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行本文所述工作所需的權限。如要查看建立及查詢資料集所需的確切權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 建立新資料集：按一下 `bigquery.datasets.create` 或 `bigquery.datasets.*`，對資料集執行其他動作。
* 查詢資料集：按一下 `bigquery.jobs.create` 或 `bigquery.jobs.*`，對工作執行其他動作。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 探索商家資訊

如要探索公開和私人房源，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「搜尋房源」。系統會顯示對話方塊，內含可存取的房源。
3. 如要依名稱或說明篩選房源，請在「搜尋房源」欄位中輸入房源名稱或說明。
4. 在「篩選器」部分，你可以根據下列欄位篩選房源：

   * **產品資訊**：選取要查看私人產品資訊、公開產品資訊，還是貴機構內的[產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)。
   * **類別**：選取一或多個類別。
   * **位置**：選取位置。你只能依資料交換位置搜尋。詳情請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
   * 「供應商」：選取資料供應商。部分資料供應商會要求你申請存取他們的商業資料集。要求存取權後，資料供應商會與您聯絡，分享他們的資料集。
5. 瀏覽篩選後的商家資訊。

## 探索資料交換庫

如要探索資料交換庫，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「搜尋房源」。系統會顯示對話方塊，內含可訂閱的清單和資料交換。
3. 如要依名稱或說明篩選資料無塵室交換，請在「搜尋清單」欄位中輸入資料無塵室交換的名稱或說明。
4. 在「篩選器」部分，您可以根據下列欄位篩選資料無塵室交換：

   * **清單**：選取「資料無塵室」核取方塊，即可查看與您共用的資料無塵室。
   * **類別**：選取一或多個類別。
   * **位置**：選取位置。您只能依資料交換位置搜尋。詳情請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
5. 瀏覽篩選後的資料無塵室。

## 訂閱產品資訊

訂閱[產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)後，您就能在專案中建立[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)，*以唯讀模式存取*產品資訊中的資料。

**注意：** 建議您避免將資料放在 VPC Service Controls 範圍內的專案。如果這麼做，就必須新增適當的[輸入和輸出規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw#subscribe_to_a_listing)。

如要訂閱房源，請按照下列步驟操作：

### 控制台

1. 如要查看可存取的房源清單，請按照「[探索房源](#discover-listings)」一文中的步驟操作。
2. 瀏覽清單，然後按一下要訂閱的清單。系統會顯示含有房源詳細資料的對話方塊。如果供應商已啟用訂閱者電子郵件記錄功能，系統就會顯示對話方塊。在「其他詳細資料」部分，你可以查看供應商提供房源資訊的區域。
3. 如果無法訂閱參照*商業資料集*的項目等，請按一下「要求存取權」或「透過 Marketplace 購買」。如果點選可訂閱的資料集，請按一下「訂閱」，開啟「建立連結資料集」對話方塊。
4. 如果專案未啟用 Analytics Hub API，系統會顯示錯誤訊息，並提供啟用 API 的連結。按一下「啟用 Analytics Hub API」。
5. 在「建立連結的資料集」對話方塊中，指定下列詳細資料：

   * **專案**：指定要新增資料集的專案名稱。
   * **連結的資料集名稱**：指定連結的資料集名稱。
   * **主要區域**：選取要建立連結資料集的區域。

     **注意：** 選取的主要區域不必與供應商的主要區域相同。您可能會選擇將連結的資料集與供應商放在同一區域，以盡量減少資料複製延遲。
   * 選用：**副本區域**
     ([預覽版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：
     選取要建立其他連結資料集次要副本的區域。您可以選擇將連結的資料集與其他資料放在同一區域，以盡量減少輸出資料，並簡化跨資料集聯結。如要建立連結的資料集副本，您必須具備連結資料集的 `bigquery.datasets.update` 權限。**注意：** 系統會盡力建立連結資料集副本。如果缺少權限，系統就不會建立副本。
6. 如要儲存變更，請按一下「儲存」。連結的資料集會列在專案中。

### API

請使用 [`projects.locations.dataExchanges.listings.subscribe` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/subscribe?hl=zh-tw)。

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:subscribe
```

更改下列內容：

* `PROJECT_ID`：您要訂閱的房源專案 ID。
* `LOCATION`：要訂閱的商家資訊位置。
* `DATAEXCHANGE_ID`：要訂閱的房源資料廣告交易平台 ID。
* `LISTING_ID`：要訂閱的房源 ID。

在要求主體中，指定要建立[連結資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)的資料集。

如要建立訂閱項目，並在多個區域提供連結資料集副本 ([預覽版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請使用要求主體中的 `location` 欄位，指定連結資料集的主要區域。如要在次要區域建立連結資料集副本，可以視需要使用要求主體中的 `destinationDataset.replica_locations` 欄位，列出所有選取的次要副本區域。確認 `location` 屬性和 `destinationDataset.replica_locations` 欄位中指定的區域，是相關聯產品資訊可用的區域。

**附註：** 系統會盡可能建立連結資料集副本。如果連結的資料集缺少 `bigquery.datasets.update` 權限，系統就不會建立副本。

如果要求成功，回應主體會包含[訂閱物件](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/subscribe?hl=zh-tw#response-body)。

如果您使用 `logLinkedDatasetQueryUserEmail` 欄位為資料交換庫或刊登啟用訂閱者電子郵件記錄功能，訂閱回應會包含 `log_linked_dataset_query_user_email: true`。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄位中。

如果啟用預存程序共用功能 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，清單回應會包含 `stored_procedure_config: true`。

**注意：** BigQuery sharing 訂閱者必須[授權共用預存程序](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)，才能在連結的資料集中讀取及寫入訂閱者擁有的特定資源。

## 訂閱資料交換

訂閱[資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)後，您可以在專案中建立[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)，取得資料無塵室交換庫中的資料唯讀存取權。

如要訂閱資料無塵室交換庫，請按照下列步驟操作：

### 控制台

1. 如要查看您有權存取的資料無塵室交換庫清單，請按照「[探索資料交換庫](#discover-data-exchanges)」一文中的步驟操作。
2. 瀏覽資料無塵室交換庫，然後按一下要訂閱的資料無塵室交換庫。系統會顯示含有資料無塵室交易詳細資料的對話方塊。
3. 如果點選可訂閱的資料無塵室交換庫，請按一下**訂閱**，開啟**將資料無塵室新增至專案**對話方塊。
4. 如果專案未啟用 Analytics Hub API，系統會顯示錯誤訊息，並提供啟用 API 的連結。按一下「啟用 Analytics Hub API」。
5. 在「將資料無塵室新增至專案」對話方塊中，指定下列詳細資料：

   * **目的地**：指定要新增資料集的專案名稱。
6. 如要儲存變更，請按一下「儲存」。連結的資料集會列在專案中。

### API

請使用 [`projects.locations.dataExchanges.subscribe` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/subscribe?hl=zh-tw)。

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/location/LOCATION/dataExchanges/DATAEXCHANGE_ID:subscribe
```

更改下列內容：

* `PROJECT_ID`：您要訂閱的資料交換庫專案 ID。
* `LOCATION`：要訂閱的資料交換庫位置。
* `DATAEXCHANGE_ID`：要訂閱的資料交易所 ID。

在要求主體中，指定要建立[連結資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)的資料集。

如果要求成功，回應主體會包含[訂閱物件](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/subscribe?hl=zh-tw#response-body)。如果您已為資料交換庫啟用訂閱者電子郵件記錄功能 ([預覽版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，訂閱回應會包含 `log_linked_dataset_query_user_email: true`。

## 查看連結的資料集

連結的資料集會與其他資料集一起顯示在Google Cloud 控制台中。

如要查看專案中已連結的資料集，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「傳統版 Explorer」窗格中，點選「category」：

   **如果沒有看到「傳統版 Explorer」窗格，請按一下「展開左窗格」圖示 last\_page 開啟窗格。**
3. 在「傳統版 Explorer」窗格中，按一下包含已連結資料集的專案名稱。

或者，您也可以使用[Data Catalog (已淘汰)](https://docs.cloud.google.com/data-catalog/docs/how-to/search?hl=zh-tw#how_to_search_for_data_assets) 或 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-tw) 搜尋及查看連結的資料集。如要比對所有 BigQuery sharing 連結資料集，請使用 `type=dataset.linked` 述詞。詳情請參閱 [Data Catalog 搜尋語法](https://docs.cloud.google.com/data-catalog/docs/how-to/search-reference?hl=zh-tw)或 [Knowledge Catalog 搜尋語法](https://docs.cloud.google.com/dataplex/docs/search-syntax?hl=zh-tw)。

### Cloud Shell

執行下列指令：

```
PROJECT=PROJECT_ID \
for dataset in $(bq ls --project_id $PROJECT | tail +3); do [ "$(bq show -d --project_id $PROJECT $dataset | egrep LINKED)" ] && echo $dataset; done
```

將 `PROJECT_ID` 替換為 Google Cloud 專案 ID。

**注意：** 如果 BigQuery sharing 發布端[移除訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#remove_a_subscription)，連結的資料集詳細資料頁面就會顯示資料集已取消連結。您可以刪除[未連結的資料集](#delete-linked-datasets)，因為您無法查詢未連結的資料集。

## 查詢連結的資料集

您可以[查詢任何其他 BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw#querying_table_data)，方法與查詢連結資料集中的資料表和檢視相同。

## 更新連結的資料集

連結資料集中的資源為*唯讀*。您無法編輯連結資料集中資源的資料或中繼資料，也無法為個別資源指定權限。

您只能更新連結資料集的說明和標籤。
連結資料集的變更不會影響來源或共用資料集。

如要更新已連結資料集的說明和標籤，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下 explore「Explorer」：
3. 在「Explorer」窗格中展開專案名稱，點選「Datasets」(資料集)，然後點選連結資料集的名稱開啟該資料集。
4. 在詳細資料窗格中，按一下「編輯詳細資料」mode\_edit
   ，然後指定下列詳細資料：

   1. 如要新增標籤，請參閱[在資料集中加入標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#adding_a_label_to_a_dataset)。
   2. 如要啟用[校對](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)，請展開「進階選項」部分，然後按照下列步驟操作：

      1. 選取「啟用預設定序」。
      2. 從「預設排序」清單中選取所需選項。
5. 按一下 [儲存]。

## 查看資料表中繼資料

如要查看基礎資料表中繼資料，請查詢 [`INFORMATION_SCHEMA.TABLES`](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw) 檢視區塊：

```
SELECT * FROM `LINKED-DATASET.INFORMATION_SCHEMA.TABLES`
```

將 LINKED-DATASET 替換為已連結資料集的名稱。

**注意：** [以區域為準的 `INFORMATION_SCHEMA` 查詢](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)不會傳回連結資料表的中繼資料。如要瞭解不支援連結資料集資料集限定符的`INFORMATION_SCHEMA`檢視畫面，請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#limitations)」一文。

## 取消訂閱或刪除連結的資料集

如要取消訂閱資料集，請刪除連結的資料集。刪除連結的資料集不會刪除來源資料集。

連結的資料集一經刪除即無法復原。不過，您可以[再次訂閱產品資訊](#subscribe-listings)，並將資料集和從 Google Cloud Marketplace 整合式產品資訊建立的連結資料集新增至專案，重新建立已刪除的連結資料集。

如果 BigQuery sharing 發布者[移除您的訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#remove_a_subscription)，則[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)會與[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)取消連結。由於這是發布者對訂閱者擁有的資源發起的動作，因此連結的資料集會保留在 BigQuery sharing 訂閱者的專案中，但處於未連結狀態。如要移除未連結的資料集，請將其刪除。

如要刪除連結的資料集，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下 explore「Explorer」：
3. 在「Explorer」窗格中展開專案名稱，點選「Datasets」(資料集)，然後點選連結資料集的名稱開啟該資料集。
4. 按一下「Delete」(刪除)。
5. 在「Delete linked dataset?」(要刪除已連結的資料集嗎？) 對話方塊中輸入「delete」(刪除)，確認要刪除。
6. 按一下「Delete」(刪除)。

## 後續步驟

* 瞭解 [BigQuery 共用](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)。
* 瞭解如何[管理房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)。
* 瞭解如何[管理資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)。
* 瞭解 [BigQuery sharing 稽核記錄](https://docs.cloud.google.com/bigquery/docs/analytics-hub-audit-logging?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]