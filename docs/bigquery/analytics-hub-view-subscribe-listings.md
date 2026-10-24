Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查看及訂閱清單和資料交換

在 BigQuery 共用 (舊稱 Analytics Hub) 中，您可以探索及訂閱清單和資料交換，直接在 BigQuery 中查詢共用資料，不必複製資料或支付儲存費用。訂閱後，專案中會建立唯讀的連結資料集，方便您分析共用資料表和檢視表，以及現有資源。

## 必要的角色

如要取得使用產品資訊所需的權限，請要求管理員授予您下列 IAM 角色：

* 探索產品資訊和資料交換：訂閱者專案的 [Analytics Hub 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.viewer)  (`roles/analyticshub.viewer`)
* 訂閱產品資訊：
  + 訂閱者專案的 [BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user)  (`roles/bigquery.user`)
  + 發布者清單、交換或專案的 [Analytics Hub 訂閱者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriber)  (`roles/analyticshub.subscriber`)
* 訂閱資料交換作業：
  + 訂閱者專案的 [BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user)  (`roles/bigquery.user`)
  + 資料無塵室的 [Analytics Hub 訂閱者](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriber)  (`roles/analyticshub.subscriber`)
  + 目的地專案的 [Analytics Hub 訂閱項目擁有者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/analyticshub?hl=zh-tw#analyticshub.subscriptionOwner)  (`roles/analyticshub.subscriptionOwner`)
* 查看及查詢連結的資料集：訂閱者專案的 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 查看資料表中繼資料：訂閱者專案的 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 更新連結的資料集：訂閱者專案的 [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)
* 刪除連結的資料集：訂閱者專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備使用產品資訊所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能使用產品資訊：

* 在訂閱者專案建立新資料集：`bigquery.datasets.create`
* 查詢訂閱者專案中的資料集：`bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 探索商店資訊

如要探索公開和私人產品資訊，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「搜尋產品」。畫面上會顯示對話方塊，列出您可以存取的產品資訊。
3. 如要依名稱或說明篩選產品資訊，請在「Search for listings」(搜尋產品資訊) 欄位中輸入文字。
4. 在「Filters」(篩選器) 部分，使用下列欄位篩選產品資訊：

   * **Listings** (清單)：選取要查看私人清單、公開清單，還是貴組織內的[清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)。
   * **類別**：選取一或多個類別。
   * **位置**：選取位置。您只能依據資料交換位置進行搜尋。詳情請參閱「[支援的地區](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
   * **供應商**：選取資料供應商。部分資料供應商會要求您申請商業資料集的存取權。提出存取要求後，資料供應商會與您聯絡，分享資料集。
5. 瀏覽篩選後的商家資訊。

## 探索資料交換庫

如要探索資料交換，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」(共用 (Analytics Hub)) 頁面。

   [前往「共用 (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「搜尋產品」。畫面上會顯示對話方塊，列出可訂閱的清單和資料交換。
3. 如要依名稱或說明篩選資料交換，請在「Search for listings」(搜尋清單) 欄位中輸入文字。
4. 在「Filters」(篩選器) 部分，使用下列欄位篩選資料無塵室交換：

   * 「Listings」(清單)：勾選「Clean rooms」(資料無塵室) 核取方塊，即可查看共用的資料無塵室。
   * **類別**：選取一或多個類別。
   * **位置**：選取位置。您只能依據資料交換位置進行搜尋。詳情請參閱「[支援的地區](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#supported-regions)」。
5. 瀏覽篩選後的資料無塵室。

## 訂閱產品資訊

訂閱[清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)後，系統會在專案中建立[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)，讓您以唯讀方式存取清單中的資料。

**注意：** 請勿將資料放在 VPC Service Controls 範圍內的專案中。如果專案位於 perimeter 內，請新增適當的[輸入和輸出規則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw#subscribe_to_a_listing)。

如要訂閱產品，請按照下列步驟操作：

### 控制台

1. 如要查看您有權存取的清單，請按照「[探索清單](#discover-listings)」中的步驟操作。
2. 在產品資訊清單中，按一下要訂閱的產品資訊。畫面上會顯示含有商店資訊詳細資料的對話方塊。對話方塊會指出供應商是否啟用訂閱者電子郵件記錄功能，並列出產品可用的區域。
3. 如果清單需要核准或購買 (例如商業資料集)，請按一下「Request access」(要求存取權) 或「Purchase via Marketplace」(透過 Marketplace 購買)。否則，請按一下「Subscribe」(訂閱)，開啟「Create linked dataset」(建立連結的資料集) 對話方塊。
4. 如果專案未啟用 Analytics Hub API，請在顯示的訊息中點選「Enable Analytics Hub API」(啟用 Analytics Hub API)。
5. 在「建立連結的資料集」對話方塊中，指定下列詳細資料：

   * 「Project」(專案)：輸入要新增資料集的專案名稱。
   * **連結的資料集名稱**：輸入連結資料集的名稱。
   * 「Primary region」(主要區域)：選取要建立連結資料集的區域。

     **注意：** 主要區域不一定要與供應商的主要區域相同。您可以將連結的資料集放在供應商的區域，盡可能縮短複製延遲時間。
   * 選用：**副本區域**：選取要建立連結資料集副本的區域。將連結的資料集與其他資料放在同一位置，可盡量減少輸出，並方便跨資料集彙整。如要建立副本，您必須具備連結資料集的 `bigquery.datasets.update` 權限。**注意：** 系統會嘗試建立連結資料集副本，但如果連結資料集缺少 `bigquery.datasets.update` 權限，就不會建立副本。
6. 如要建立連結的資料集，請按一下「儲存」。

### API

如要訂閱產品資訊，請呼叫 [`projects.locations.dataExchanges.listings.subscribe` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings/subscribe?hl=zh-tw)：

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID/listings/LISTING_ID:subscribe
```

更改下列內容：

* `PROJECT_ID`： Google Cloud 專案 ID，用於存放您要訂閱的清單。
* `LOCATION`：產品資訊的位置。
* `DATAEXCHANGE_ID`：清單的資料交換 ID。
* `LISTING_ID`：要訂閱的產品 ID。
* `SUBSCRIBER_PROJECT_ID`：要建立連結資料集的訂閱者專案 Google Cloud 專案 ID。
* `LINKED_DATASET_ID`：要指派給連結資料集的 ID。
* `PRIMARY_REGION`：要建立連結資料集的主要地理區域。

在要求主體中，指定要建立[連結資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)的資料集：

```
{
"destinationDataset": {
  "datasetReference": {
    "projectId": "SUBSCRIBER_PROJECT_ID",
    "datasetId": "LINKED_DATASET_ID"
  },
  "location": "PRIMARY_REGION"
}
}
```

如要建立訂閱項目，並在多個區域中連結資料集副本，請在 `location` 欄位中指定主要區域。如要指定次要副本區域，請將區域新增至 `destinationDataset.replica_locations` 欄位。請確認所有指定區域都是可提供產品資訊的區域。

**注意：** 系統會嘗試建立連結資料集副本，但如果連結資料集缺少 `bigquery.datasets.update` 權限，就不會建立副本。

如果要求成功，回應主體會包含[訂閱項目物件](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/Shared.Types/Subscription?hl=zh-tw)。

如果您為資料交換或含有 `logLinkedDatasetQueryUserEmail` 欄位的清單項目啟用訂閱者電子郵件記錄功能，訂閱回應會包含 `log_linked_dataset_query_user_email: true`。記錄的資料會顯示在 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)的 `job_principal_subject` 欄位中。

如果啟用預存程序共用功能 ([預先發布版](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages))，清單回應會包含 `stored_procedure_config: true`。

**注意：** 如要在連結資料集中執行共用預存程序，您必須[授權共用預存程序](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)存取專案中的資源。

## 訂閱資料交換

訂閱[資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)後，您可以在專案中建立[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)，以唯讀方式存取資料交換中的資料。

如要訂閱資料無塵室交換，請按照下列步驟操作：

### 控制台

1. 如要查看您有權存取的資料無塵室交換清單，請按照「[探索資料交換](#discover-data-exchanges)」中的步驟操作。
2. 在資料無塵室清單中，按一下要訂閱的資料無塵室交換。系統會顯示對話方塊，其中包含資料無塵室交換詳細資料。
3. 按一下「訂閱」，開啟「將資料無塵室新增至專案」對話方塊。
4. 如果專案未啟用 Analytics Hub API，請在顯示的訊息中點選「Enable Analytics Hub API」(啟用 Analytics Hub API)。
5. 在「Add data clean room to project」(將資料無塵室新增至專案) 對話方塊中，指定下列詳細資料：

   * 「Destination」(目的地)：輸入要新增資料集的專案名稱。
6. 如要建立連結的資料集，請按一下「儲存」。

### API

如要訂閱資料無塵室交換，請呼叫 [`projects.locations.dataExchanges.subscribe` 方法](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges/subscribe?hl=zh-tw)：

```
POST https://analyticshub.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/dataExchanges/DATAEXCHANGE_ID:subscribe
```

更改下列內容：

* `PROJECT_ID`： Google Cloud 專案 ID，用於存放您要訂閱的資料交換。
* `LOCATION`：資料交換作業的位置。
* `DATAEXCHANGE_ID`：資料交換作業 ID。
* `SUBSCRIBER_PROJECT_ID`：您要建立連結資料集的訂閱者專案 Google Cloud 專案 ID。
* `SUBSCRIPTION_ID`：要建立的訂閱項目名稱。
* `LINKED_DATASET_ID`：您要為連結資料集指定的 ID。
* `PRIMARY_REGION`：要建立連結資料集的主要地理區域。

在要求主體中，指定目的地位置、訂閱項目名稱，以及要建立[連結資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)的資料集：

```
{
"destination": "projects/SUBSCRIBER_PROJECT_ID/locations/LOCATION",
"subscription": "SUBSCRIPTION_ID",
"destinationDataset": {
  "datasetReference": {
    "projectId": "SUBSCRIBER_PROJECT_ID",
    "datasetId": "LINKED_DATASET_ID"
  },
  "location": "PRIMARY_REGION"
}
}
```

如果要求成功，回應主體會包含[作業物件](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/Operation?hl=zh-tw)。如果您已為資料交換啟用訂閱者電子郵件記錄功能，訂閱回應會包含 `log_linked_dataset_query_user_email: true`。

## 查看連結的資料集

連結的資料集會與其他資料集一起顯示在Google Cloud 控制台中。

如要查看專案中的連結資料集，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「傳統版 Explorer」窗格中，點選「類別」：

   如果沒有看到「傳統版 Explorer」窗格，請按一下 last\_page「展開左側窗格」，開啟窗格。
3. 在「傳統版 Explorer」窗格中，點選包含 連結資料集的專案名稱。

或者，您也可以使用 [Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw) 搜尋及查看連結的資料集。如要在搜尋查詢中比對所有 BigQuery sharing 連結資料集，請使用 `type=dataset.linked` 述詞。詳情請參閱「[Knowledge Catalog 搜尋語法](https://docs.cloud.google.com/knowledge-catalog/docs/search-syntax?hl=zh-tw)」。

### Cloud Shell

如要使用 `bq` 指令列工具列出專案中的連結資料集，請在 Cloud Shell 中執行下列指令：

```
PROJECT=PROJECT_ID \
for dataset in $(bq ls --project_id $PROJECT | tail +3); do [ "$(bq show -d --project_id $PROJECT $dataset | egrep LINKED)" ] && echo $dataset; done
```

將 `PROJECT_ID` 替換為 Google Cloud 專案 ID。

**注意：** 如果發布者[移除訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#remove_a_subscription)，連結的資料集詳細資料頁面會指出資料集已取消連結。由於無法查詢未連結的資料集，您可以[刪除未連結的資料集](#delete-linked-datasets)。

## 查詢連結的資料集

您可以[查詢任何其他 BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw#querying_table_data)，並以相同方式查詢已連結資料集中的資料表和檢視表。

如要查詢連結資料集中的資料表，請執行 `SELECT` 查詢，並參照專案 ID、連結資料集 ID 和資料表名稱：

```
SELECT * FROM `PROJECT_ID`.`LINKED_DATASET_ID`.`TABLE_NAME`
LIMIT 10;
```

更改下列內容：

* `PROJECT_ID`：您的 Google Cloud 專案 ID。
* `LINKED_DATASET_ID`：連結資料集的 ID。
* `TABLE_NAME`：要查詢的資料表或檢視表名稱。

詳情請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)」。

## 更新連結的資料集

連結資料集中的資源為*唯讀*。您無法編輯連結資料集中資源的資料或中繼資料，也無法指定個別資源的權限。

您只能更新已連結資料集的說明和標籤。變更連結的資料集不會影響來源或共用資料集。

如要更新已連結資料集的說明和標籤，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，點選 explore「Explorer」：
3. 在「Explorer」窗格中展開專案名稱，點選「Datasets」(資料集)，然後點選連結的資料集名稱，即可開啟資料集。
4. 在詳細資料窗格中，按一下「mode\_edit Edit details」(編輯詳細資料)，然後設定下列選項：

   1. 如要新增標籤，請參閱「[為資料集新增標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#adding_a_label_to_a_dataset)」。
   2. 如要啟用[校對](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)，請展開「Advanced options」(進階選項)，然後按照下列步驟操作：

      1. 選取「Enable default collation」(啟用預設定序)。
      2. 在「Default collation」(預設校對) 清單中選取所需選項。
5. 點按「儲存」，儲存變更。

## 查看資料表中繼資料

如要查看連結資料集的資料表中繼資料，請查詢 [`INFORMATION_SCHEMA.TABLES`](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw) 檢視表：

```
SELECT * FROM `LINKED_DATASET_ID`.INFORMATION_SCHEMA.TABLES;
```

將 `LINKED_DATASET_ID` 替換為連結資料集的 ID。

**注意：** [以區域為基礎的 `INFORMATION_SCHEMA` 查詢](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)不會傳回連結資料表的中繼資料。如要進一步瞭解不支援的檢視表，請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#limitations)」一節。

## 取消訂閱或刪除連結的資料集

如要取消訂閱資料集，請刪除連結的資料集。刪除連結資料集不會刪除來源資料集。

連結的資料集一經刪除即無法復原。不過，您隨時可以再次[訂閱產品資訊](#subscribe-listings)，重新建立已刪除的連結資料集。

如果發布者[移除您的訂閱項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#remove_a_subscription)，[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)會與[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)取消連結。由於這是發布端對訂閱端擁有的資源採取的動作，因此連結的資料集會保留在您的專案中，但處於取消連結狀態。如要移除未連結的資料集，請將其刪除。

如要刪除連結的資料集，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，點選 explore「Explorer」：
3. 在「Explorer」窗格中展開專案名稱，點選「Datasets」(資料集)，然後點選連結的資料集名稱，即可開啟資料集。
4. 點選「刪除」。
5. 在「Delete linked dataset?」(要刪除連結的資料集嗎？) 對話方塊中，輸入 `delete` 確認刪除。
6. 點選「刪除」。

## 後續步驟

* 瞭解 [BigQuery 共用](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)。
* 瞭解如何[管理商家資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)。
* 瞭解如何[管理資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)。
* 瞭解如何[查看 BigQuery 共用稽核記錄](https://docs.cloud.google.com/bigquery/docs/analytics-hub-audit-logging?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]