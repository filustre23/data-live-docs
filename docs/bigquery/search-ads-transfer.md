Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Search Ads 360 資料載入 BigQuery

您可以使用 Search Ads 360 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 Search Ads 360 載入 BigQuery。您可以使用 BigQuery 資料移轉服務，安排週期性移轉工作，將 Search Ads 360 的最新資料新增至 BigQuery。

## 連接器總覽

Search Ads 360 連接器的 BigQuery 資料移轉服務支援下列資料移轉選項。

| 資料移轉選項 | 支援 |
| --- | --- |
| 受支援的報表 | Search Ads 360 連接器支援從 [Search Ads 360 第 0 版報表](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/overview?hl=zh-tw)中的報表移轉資料。 如要瞭解 Search Ads 360 報表如何轉換為 BigQuery 資料表和檢視表，請參閱「[Search Ads 360 報表轉換](https://docs.cloud.google.com/bigquery/docs/search-ads-transformation?hl=zh-tw)」。 |
| 重複頻率 | Search Ads 360 連接器支援每日資料移轉。    根據預設，資料移轉作業會排定在建立資料移轉作業時執行。您可以在[設定資料移轉作業](#setup-data-transfer)時，設定資料移轉時間。 |
| 重新整理時間範圍 | 您可以排定資料移轉作業，在執行時擷取最多 30 天前的 Search Ads 360 資料。[設定資料移轉作業](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#setup-data-transfer)時，您可以設定重新整理回溯期的時間長度。    根據預設，Search Ads 360 連接器的重新整理回溯期為 7 天。    詳情請參閱「[重新整理時間範圍](#refresh)」。 系統每天會擷取一次[比對表格](https://docs.cloud.google.com/bigquery/docs/search-ads-transformation?hl=zh-tw#search_ads_match_tables)的快照，並儲存在上次執行日期的分區中。 比對表快照不會因回填或使用重新整理時間範圍載入的天數而更新。 |
| 補充資料可用性 | [執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，擷取排定資料移轉作業以外的資料。只要在資料來源的資料保留政策允許範圍內，即可擷取歷來資料。    如要瞭解 Search Ads 360 的資料保留政策，請參閱「[報表資料保留政策](https://support.google.com/sa360/answer/13292701?hl=zh-tw)」一文。 |
| 每個管理員帳戶的客戶 ID 數 | BigQuery 資料移轉服務最多支援每個 Search Ads 360 [管理員帳戶](https://support.google.com/sa360/answer/9158072?hl=zh-tw)有 **8,000 個客戶 ID**。 |

如要查看使用舊版 Search Ads 360 Reporting API 的 Search Ads 360 移轉指南，請參閱「[Search Ads 360 移轉作業 (已淘汰)](https://docs.cloud.google.com/bigquery/docs/sa360-transfer?hl=zh-tw)」。

## 從 Search Ads 360 移轉作業擷取資料

將資料從 Search Ads 360 移轉至 BigQuery 時，資料會載入依日期分區的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果您在同一天安排多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該日期的分區。在同一天進行多次移轉或執行補充作業，不會產生重複資料，其他日期的分區也不會受到影響。

### 重新整理時間範圍

「更新回溯期」是指資料移轉時，資料移轉作業擷取資料的天數。舉例來說，如果更新時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務會從來源資料表擷取過去三天的所有資料。在本例中，每日移轉作業執行時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分區，並複製當天的來源資料表資料，然後自動觸發補充執行作業，使用過去兩天的來源資料表資料更新 BigQuery 目的地資料表分區。自動觸發的回填執行作業會覆寫或增量更新 BigQuery 目的地資料表，具體取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉作業時，系統會擷取重新整理期間內的所有可用來源資料。舉例來說，如果更新時間範圍為三天，且您首次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

如要擷取更新時間範圍以外的資料 (例如歷來資料)，或從任何移轉中斷或缺漏中復原資料，您可以啟動或排定[補充執行作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 限制

* Search Ads 360 資料移轉作業的頻率上限為每 24 小時一次。根據預設，移轉作業會在您建立移轉作業時開始。不過，您可以在[建立移轉作業](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#setup-data-transfer)時，設定資料移轉開始時間。
* BigQuery 資料移轉服務不支援在 Search Ads 360 移轉期間進行增量資料移轉。指定資料移轉日期後，系統會移轉該日期可用的所有資料。

## 事前準備

建立 Search Ads 360 資料移轉作業前，請先完成下列事項：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)所需的所有動作。
* [建立 BigQuery 資料移轉服務資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，用於儲存 Search Ads 360 報表資料。
* 如要設定 Pub/Sub 的移轉作業執行通知，您必須具備 `pubsub.topics.setIamPolicy` 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱「[BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)」。
* 在專案中[啟用 Search Ads 360 Reporting API 存取權](https://console.developers.google.com/apis/api/searchads360.googleapis.com/?hl=zh-tw)。

## 所需權限

請確認您已授予下列權限。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能建立 BigQuery 資料移轉服務資料移轉作業：

* BigQuery 資料移轉服務權限：
  + `bigquery.transfers.update`
  + `bigquery.transfers.get`
* BigQuery 權限：
  + `bigquery.datasets.get`
  + `bigquery.datasets.getIamPolicy`
  + `bigquery.datasets.update`
  + `bigquery.datasets.setIamPolicy`
  + `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

詳情請參閱「[授予 `bigquery.admin` 存取權](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#grant_bigqueryadmin_access)」。

### 必要 Google Cloud 角色

您必須具備 `serviceusage.services.use` 權限，才能從 Search Ads 360 下載資料。預先定義的 IAM 角色「[服務使用情形消費者](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer)」(`roles/serviceusage.serviceUsageConsumer`) 包含這項權限。

### 必要的 Search Ads 360 角色

授予讀取權限給移轉設定中使用的 Search Ads 360 客戶 ID 或[管理員帳戶](https://support.google.com/sa360/answer/9158072?hl=zh-tw)。如要設定服務帳戶的讀取權限，請[聯絡 Search Ads 360 支援團隊](https://support.google.com/sa360/gethelp?hl=zh-tw)尋求協助。

## 建立 Search Ads 360 資料移轉作業

如要建立 Search Ads 360 報表的資料移轉作業，您需要 Search Ads 360 客戶 ID 或[管理員帳戶](https://support.google.com/sa360/answer/9158072?hl=zh-tw)。選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料移轉」](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「add 建立移轉作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Search Ads 360」。
4. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
5. 在「Schedule options」(排程選項) 專區：

   * 在「Repeat frequency」(重複頻率) 部分選取選項，指定資料移轉作業的執行頻率。如果選取「Days」(天)，請按照世界標準時間提供有效的值。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
6. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
7. 在「Data source details」(資料來源詳細資料) 區段：

   1. 在「Customer ID」(客戶 ID)，輸入 Search Ads 360 客戶 ID。
   2. 選用步驟：輸入**代理商 ID** 和**廣告主 ID**，即可擷取 [ID 對應表格](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#id-mapping)。
   3. 選用步驟：在「Custom Floodlight Variables」(自訂 Floodlight 變數) 部分，輸入要加進資料移轉的[自訂 Floodlight 變數](https://support.google.com/sa360/answer/13567857?hl=zh-tw)。自訂 Floodlight 變數的擁有者須為 Search Ads 360 帳戶 (由移轉作業設定中的客戶 ID 指定)。這個參數會以 JSON 陣列格式接收輸入字串，並支援多個自訂 Floodlight 變數。在 JSON 陣列的個別項目，您必須提供下列參數：

      * `id`：自訂 Floodlight 變數的數值 ID。您[在 Search Ads 360 建立自訂 Floodlight 變數](https://support.google.com/sa360/answer/14316155?hl=zh-tw)時，系統會指派這組 ID。
        如果已指定 `id`，就不需要指定 `name`。
      * `name`：使用者在 Search Ads 360 定義的自訂 Floodlight 變數名稱。如果已指定 `name`，就不需要指定 `id`。
      * `cfv_field_name`：自訂 Floodlight 變數欄位的確切名稱 (視用途而定)，支援的值為 `conversion_custom_metrics`、`conversion_custom_dimensions`、`raw_event_conversion_metrics` 和 `raw_event_conversion_dimensions`。
      * `destination_table_name`：BigQuery 資料表清單，自訂 Floodlight 變數會新增至這份清單。BigQuery 資料移轉服務擷取這些資料表的內容時，移轉作業會在查詢加入自訂 Floodlight 變數。
      * `bigquery_column_name_suffix`：使用者定義、簡單易懂的資料欄名稱。BigQuery 資料移轉服務會在標準欄位名稱加上後置字串，藉此區分不同的自訂 Floodlight 變數。視用途而定，BigQuery 資料移轉服務會產生如下的 BigQuery 資料欄名稱：

      |  | 自訂 Floodlight 變數做為指標和區隔 | 自訂 Floodlight 變數做為轉換作業資源中的原始事件屬性 |
      | --- | --- | --- |
      | `metrics` | `metrics_conversion_custom_metrics_bigquery_column_name_suffix` | `metrics_raw_event_conversion_metrics_bigquery_column_name_suffix` |
      | `dimension` | `segments_conversion_custom_dimensions_bigquery_column_name_suffix` | `segments_raw_event_conversion_dimensions_bigquery_column_name_suffix` |

      以下是「Custom Floodlight Variables」(自訂 Floodlight 變數) 的項目示例，當中指定兩項自訂 Floodlight 變數：

      ```
      [{
      "id": "1234",
      "cfv_field_name": "raw_event_conversion_metrics",
      "destination_table_name": ["Conversion"],
      "bigquery_column_name_suffix": "suffix1"
      },{
      "name": "example name",
      "cfv_field_name": "conversion_custom_metrics",
      "destination_table_name": ["AdGroupConversionActionAndDeviceStats","CampaignConversionActionAndDeviceStats"],
      "bigquery_column_name_suffix": "suffix2"
      }]
      ```
   4. 選用步驟：在「Custom Columns」(自訂欄) 欄位，輸入要包含在資料移轉中的[自訂欄](https://developers.google.com/search-ads/reporting/concepts/custom-columns?hl=zh-tw)。自訂資料欄的擁有者須為 Search Ads 360 帳戶 (由移轉作業設定中的客戶 ID 指定)。這個欄位會以 JSON 陣列格式接收輸入字串，並支援多個資料欄。在 JSON 陣列的個別項目，您必須提供下列參數：

      * `id`：自訂資料欄的數值 ID。[建立自訂資料欄](https://support.google.com/sa360/answer/9633916?amp%3Bref_topic=14138984&%3Bsjid=5858325799664893372-NC&hl=zh-tw)時，系統會指派這組 ID。如果已指定 `id`，就不需要指定 `name`。
      * `name`：使用者在 Search Ads 360 定義的自訂資料欄名稱。如果已指定 `name`，就不需要指定 `id`。
      * `destination_table_name`：要涵蓋自訂資料欄的 BigQuery 資料表清單。BigQuery 資料移轉服務擷取這些資料表的內容時，移轉作業會在查詢加入自訂資料欄。
      * `bigquery_column_name`：使用者定義、簡單易懂的資料欄名稱。在 `destination_table_name` 指定的目的地資料表，這是自訂資料欄的名稱。資料欄名稱必須[符合 BigQuery 資料欄名稱的格式規定](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_names)，而且不得與其他自訂資料欄或[資料表標準結構定義](https://docs.cloud.google.com/bigquery/docs/search-ads-transformation?hl=zh-tw)中的其他欄位重複。

      以下是「Custom Columns」(自訂資料欄) 項目示例，當中指定兩個自訂資料欄：

      ```
      [{
        "id": "1234",
        "destination_table_name": ["Conversion"],
        "bigquery_column_name": "column1"
      },{
        "name": "example name",
        "destination_table_name": ["AdGroupStats","CampaignStats"],
        "bigquery_column_name": "column2"
      }]
      ```
   5. 選用：在「Table Filter」(資料表篩選器) 欄位，輸入要納入的資料表清單 (以半形逗號分隔)，例如 `Campaign, AdGroup`。您可以為這份清單加上 `-` 前置字元，藉此排除特定資料表，例如 `-Campaign, AdGroup`。預設會加入所有資料表。
   6. 選用步驟：選取「Include PMax Campaign Data」(納入最高成效廣告活動資料)，藉此加入最高成效廣告活動資料，並從特定資料表中排除 `ad_group` 欄位。詳情請參閱[最高成效廣告活動](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#pmax-support)
   7. 選用步驟：選取「Use Client Account Currency」(使用客戶帳戶幣別)，以客戶帳戶的幣別載入費用資料，而非這次資料移轉作業所用帳戶的幣別。
   8. 選用步驟：在「Refresh window」(重新整理時間範圍) 部分，輸入介於 1 至 30 之間的值。如未設定，重新整理時間範圍預設為 7 天。詳情請參閱「[重新整理時間範圍](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#refresh)」
8. 在「Service Account」(服務帳戶) 選單，選取與貴組織 Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與移轉作業建立關聯，這樣就不需要使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。

   如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立移轉作業。服務帳戶必須具備[必要權限](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#required_permissions)。
9. (選用) 在「Notification options」(通知選項) 區段中：

   * 點選切換按鈕，啟用電子郵件通知。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   * 點選切換按鈕，啟用 Pub/Sub 通知。在「Select a Cloud Pub/Sub topic」(選取 Cloud Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
10. 按一下「儲存」。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。還需加上以下旗標：

* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

以下為選用旗標：

* `--project_id`：指定要使用的專案。如未指定旗標，則會使用預設專案。
* `--service_account_name`：指定要用於 Search Ads 360 移轉驗證的服務帳戶，而非使用者帳戶。

```
bq mk \
--transfer_config \
--project_id=PROJECT_ID \
--target_dataset=DATASET \
--display_name=NAME \
--data_source=DATA_SOURCE \
--service_account_name=SERVICE_ACCOUNT_NAME \
--params='{PARAMETERS,"custom_columns":"[{\"id\": \"CC_ID\",\"destination_table_name\": [\"CC_DESTINATION_TABLE\"],\"bigquery_column_name\": \"CC_COLUMN\"}]","custom_floodlight_variables":"[{\"id\": \"CFV_ID\",\"cfv_field_name\": [\"CFV_FIELD_NAME\"],\"destination_table_name\": [\"CFV_DESTINATION_TABLE\"],\"bigquery_column_name_suffix\": \"CFV_COLUMN_SUFFIX\"}]"}'
```

其中：

* PROJECT\_ID (選用)：指定要使用的專案。如未指定旗標，則會使用預設專案。
* DATASET：移轉設定的目標資料集。
* NAME：移轉設定的顯示名稱。資料移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATA\_SOURCE：資料來源 - `search_ads`。
* SERVICE\_ACCOUNT\_NAME (選用)：用於驗證資料移轉作業的服務帳戶名稱。服務帳戶應由用於建立移轉作業的 `project_id` 擁有，且應具備所有[必要權限](#required_permissions)。
* PARAMETERS：JSON 格式的已建立移轉設定參數。例如：`--params='{"param":"param_value"}'`。您必須提供 `customer_id` 參數。