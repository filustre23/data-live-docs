Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Search Ads 360 資料載入 BigQuery

您可以使用 Search Ads 360 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 Search Ads 360 載入至 BigQuery。透過 BigQuery 資料移轉服務，您可以安排週期性移轉工作，將 Search Ads 360 的最新資料新增至 BigQuery。

## 連接器總覽

Search Ads 360 連接器的 BigQuery 資料移轉服務支援下列資料移轉選項。

| 資料轉移方式 | 支援 |
| --- | --- |
| 受支援的報表 | Search Ads 360 連接器支援從 [Search Ads 360 v0 報表](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/overview?hl=zh-tw)傳輸資料。 如要瞭解 Search Ads 360 報表如何轉換成 BigQuery 表格和檢視畫面，請參閱「[Search Ads 360 報表轉換](https://docs.cloud.google.com/bigquery/docs/search-ads-transformation?hl=zh-tw)」一文。 |
| 重複頻率 | Search Ads 360 連接器支援每日資料轉移。    根據預設，資料移轉作業會在建立時排定時間。[設定資料移轉作業](#setup-data-transfer)時，你可以設定資料移轉時間。 |
| 重新整理時間範圍 | 您可以排定資料轉移時間，在資料轉移作業執行時，擷取最多 30 天的 Search Ads 360 資料。[設定資料移轉時，您可以設定重新整理視窗的持續時間。](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#setup-data-transfer)    根據預設，Search Ads 360 連接器的更新期為 7 天。    詳情請參閱「[重新整理時間範圍](#refresh)」。 系統每天會為[比對資料表](https://docs.cloud.google.com/bigquery/docs/search-ads-transformation?hl=zh-tw#search_ads_match_tables)建立快照，並儲存在上次執行日期的分區中。系統不會更新回填或使用重新整理視窗載入的日期，因此相符資料表快照不會更新。 |
| 資料補充作業的可用性 | [執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，擷取排定資料移轉時間以外的資料。您可以擷取資料來源資料保留政策允許的最早資料。    如要瞭解 Search Ads 360 的資料保留政策，請參閱「[報表資料保留政策](https://support.google.com/sa360/answer/13292701?hl=zh-tw)」。 |
| 每個管理員帳戶的客戶 ID 數 | BigQuery 資料移轉服務對每個 Search Ads 360 [管理員帳戶](https://support.google.com/sa360/answer/9158072?hl=zh-tw)最多支援 **8000 個客戶 ID**。 |

如要查看使用舊版 Search Ads 360 Reporting API 的 Search Ads 360 移轉指南，請參閱「[Search Ads 360 移轉作業 (已淘汰)](https://docs.cloud.google.com/bigquery/docs/sa360-transfer?hl=zh-tw)」。

## 從 Search Ads 360 轉移作業擷取資料

將資料從 Search Ads 360 移轉至 BigQuery 時，系統會將資料載入至按日期分區的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果為同一天排定多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該特定日期的資料分割。同一天內進行多次轉移或執行回填作業，不會導致資料重複，也不會影響其他日期的分區。

### 重新整理視窗

*更新期*是指資料移轉作業在進行時，擷取資料的天數。舉例來說，如果重新整理時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務就會從來源資料表擷取過去三天的所有資料。在這個範例中，每天進行移轉時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分割區，並複製當天的來源資料表資料，然後自動觸發補充作業執行作業，以更新過去兩天的來源資料表資料。系統自動觸發的回填作業會覆寫或增量更新 BigQuery 目的地資料表，具體做法取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。舉例來說，如果重新整理時間範圍為三天，而您是第一次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

如要擷取重新整理時間範圍外的資料 (例如歷來資料)，或從任何轉移中斷或缺漏中復原資料，可以啟動或排定[補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 限制

* 您最多可以每 24 小時設定一次 Search Ads 360 資料轉移作業。預設情況下，移轉作業會在您建立移轉作業時啟動。不過，您可以在[建立移轉作業](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#setup-data-transfer)時設定資料移轉開始時間。
* 在 Search Ads 360 移轉期間，BigQuery 資料移轉服務不支援增量資料移轉。指定資料移轉日期後，系統會移轉該日期可用的所有資料。

## 事前準備

建立 Search Ads 360 資料移轉作業前的準備事項如下：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料移轉服務資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，儲存 Search Ads 360 報表資料。
* 如要為 Pub/Sub 設定移轉作業執行通知，您必須擁有 `pubsub.topics.setIamPolicy` 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱「[BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)」一文。
* 在專案中[啟用 Search Ads 360 報表 API 的存取權](https://console.developers.google.com/apis/api/searchads360.googleapis.com/?hl=zh-tw)。

## 所需權限

確認您已授予下列權限。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求系統管理員在專案中授予您 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立 BigQuery 資料移轉服務資料移轉作業，您必須具備下列權限：

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

如要從 Search Ads 360 下載資料，您必須具備 `serviceusage.services.use` 權限。[服務使用情形消費者](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer) (`roles/serviceusage.serviceUsageConsumer`) 預先定義的 IAM 角色包含這項權限。

### 必要 Search Ads 360 角色

授予移轉設定所用 Search Ads 360 客戶 ID 或[管理員帳戶](https://support.google.com/sa360/answer/9158072?hl=zh-tw)的讀取權限。如要為服務帳戶設定讀取權限，請[與 Search Ads 360 支援團隊聯絡](https://support.google.com/sa360/gethelp?hl=zh-tw)，尋求協助。

## 建立 Search Ads 360 資料轉移作業

如要建立 Search Ads 360 報表資料轉移作業，您需要 Search Ads 360 客戶 ID 或[管理員帳戶](https://support.google.com/sa360/answer/9158072?hl=zh-tw)。選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「來源類型」部分，針對「來源」，選擇「Search Ads 360」。
4. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
5. 在「Schedule options」(排程選項) 專區：

   * 在「Repeat frequency」(重複頻率) 部分選取選項，指定資料移轉作業的執行頻率。如果選取「Days」(天)，請按照世界標準時間提供有效的值。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
6. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
7. 在「Data source details」(資料來源詳細資料) 區段：

   1. 在「Customer ID」(客戶 ID)，輸入 Search Ads 360 客戶 ID。
   2. 選用步驟：輸入**代理商 ID** 和**廣告主 ID**，即可擷取 [ID 對應表格](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#id-mapping)。
   3. 選用步驟：在「Custom Floodlight Variables」(自訂 Floodlight 變數) 部分，輸入要加進移轉資料的[自訂 Floodlight 變數](https://support.google.com/sa360/answer/13567857?hl=zh-tw)。自訂 Floodlight 變數的擁有者須為 Search Ads 360 帳戶 (由移轉作業設定中的客戶 ID 指定)。這項參數會以 JSON 陣列格式接收輸入字串，並支援多項自訂 Floodlight 變數。在 JSON 陣列的個別項目，您必須提供下列參數：

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
   4. 選用步驟：在「Custom Columns」(自訂資料欄) 欄位，輸入要移轉資料的[自訂資料欄](https://developers.google.com/search-ads/reporting/concepts/custom-columns?hl=zh-tw)。自訂資料欄的擁有者須為 Search Ads 360 帳戶 (由移轉作業設定中的客戶 ID 指定)。這個欄位會以 JSON 陣列格式接收輸入字串，並支援多個資料欄。在 JSON 陣列的個別項目，您必須提供下列參數：

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
   5. 選用步驟：在「Table Filter」(資料表篩選器) 欄位，輸入要涵蓋的資料表清單 (以逗號分隔)，例如 `Campaign, AdGroup`。您可以在這份清單加上 `-` 前置字元，藉此排除特定資料表，例如 `-Campaign, AdGroup`。預設會加入所有資料表。
   6. 選用步驟：選取「Include PMax Campaign Data」(納入最高成效廣告活動資料)，藉此加入最高成效廣告活動資料，並從特定資料表中排除 `ad_group` 欄位。詳情請參閱[最高成效廣告活動](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#pmax-support)
   7. 選用步驟：選取「Use Client Account Currency」(使用客戶帳戶幣別)，以客戶帳戶的幣別載入費用資料，而非這次資料移轉作業所用帳戶的幣別。
   8. 選用步驟：在「Refresh window」(重新整理時間範圍) 部分，輸入介於 1 至 30 之間的值。如未設定，重新整理時間範圍預設為 7 天。詳情請參閱「[重新整理時間範圍](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#refresh)」
8. 在「Service Account」(服務帳戶) 選單，選取與貴組織 Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與移轉作業建立關聯，而非使用使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。

   如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立移轉作業。如果以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立移轉作業。服務帳戶必須具備[必要權限](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#required_permissions)。
9. (選用) 在「Notification options」(通知選項) 區段中：

   * 點選切換按鈕，啟用電子郵件通知。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   * 點選切換按鈕，啟用 Pub/Sub 通知。在「Select a Cloud Pub/Sub topic」(選取 Cloud Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
10. 按一下 [儲存]。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。還需加上以下旗標：

* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

以下旗標為選用項目：

* `--project_id`：指定要使用的專案。如果未指定旗標，系統會使用預設專案。
* `--service_account_name`：指定要用於 Search Ads 360 轉移驗證的服務帳戶，而非使用者帳戶。

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

* PROJECT\_ID (選用)：指定要使用的專案。如果未指定旗標，系統會使用預設專案。
* DATASET：移轉設定的目標資料集。
* NAME：移轉設定的顯示名稱。資料移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATA\_SOURCE：資料來源 - `search_ads`。
* SERVICE\_ACCOUNT\_NAME (選用)：用於驗證資料移轉的服務帳戶名稱。服務帳戶應由用於建立轉移作業的 `project_id` 擁有，且應具備所有[必要權限](#required_permissions)。
* PARAMETERS：已建立移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。您必須提供 `customer_id` 參數。

  + `table_filter`：指定要納入資料轉移作業的資料表。如果未指定旗標，系統會納入所有資料表。如要只納入特定資料表，請使用以半形逗號分隔的值清單 (例如 `Ad, Campaign, AdGroup`)。如要排除特定資料表，請在排除的值前面加上連字號 (`-`) (例如使用 `-Ad, Campaign, AdGroup` 會排除所有三個值)。
  + `custom_columns`：指定報表的自訂欄。這項參數會以 JSON 陣列格式接收輸入字串，並支援多個資料欄。在 JSON 陣列的個別項目，您必須提供下列參數：
    - CC\_ID：自訂資料欄的數值 ID。[建立自訂欄](https://support.google.com/sa360/answer/9633916?amp%3Bref_topic=14138984&%3Bsjid=5858325799664893372-NC&hl=zh-tw)時，系統會指派這組 ID。
    - CC\_DESTINATION\_TABLE：要涵蓋自訂欄的 BigQuery 資料表清單。BigQuery 資料移轉服務擷取這些資料表的內容時，資料移轉作業會在查詢加入自訂欄。
    - CC\_COLUMN：使用者定義、簡單易懂的資料欄名稱。在 `destination_table_name` 指定的目的地資料表，這是自訂欄的欄位名稱。資料欄名稱必須[符合 BigQuery 資料欄名稱的格式規定](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_names)，而且不得與其他自訂資料欄或[資料表標準結構定義](https://docs.cloud.google.com/bigquery/docs/search-ads-transformation?hl=zh-tw)中的其他欄位重複。
  + `custom_floodlight_variables`：指定要納入移轉的[自訂 Floodlight 變數](https://support.google.com/campaignmanager/answer/2823222?sjid=11547437748727448706-NA&hl=zh-tw)。這項參數會以 JSON 陣列格式接收輸入字串，並支援多項自訂 Floodlight 變數。在 JSON 陣列的個別項目，您必須提供下列參數：
    - CFV\_ID：自訂 Floodlight 變數的數值 ID。您[在 Search Ads 360 建立自訂 Floodlight 變數](https://support.google.com/searchads/answer/6024747?hl=zh-tw#set-up)時，系統會指派這組 ID。
    - CFV\_FIELD\_NAME：自訂 Floodlight 變數欄位的確切名稱 (視用途而定)，支援的值為 `conversion_custom_metrics`、`conversion_custom_dimensions`、`raw_event_conversion_metrics` 和 `raw_event_conversion_dimensions`。詳情請參閱「[自訂 Floodlight 指標](https://developers.google.com/search-ads/reporting/concepts/custom-floodlight-variables?hl=zh-tw)」。
    - CFV\_DESTINATION\_TABLE：BigQuery 資料表清單，自訂 Floodlight 變數會新增至這份清單。BigQuery 資料移轉服務擷取這些資料表的內容時，資料移轉作業會在查詢加入自訂 Floodlight 變數。
    - CFV\_COLUMN\_SUFFIX：使用者定義、簡單易懂的資料欄名稱。BigQuery 資料移轉服務會在標準欄位名稱加上後置字串，藉此區分不同的自訂 Floodlight 變數。視用途而定，BigQuery 資料移轉服務會產生如下的 BigQuery 資料欄名稱：
  + `use_client_account_currency`：指定 `TRUE`，以客戶帳戶的幣別載入費用資料，而非這次資料移轉作業所用帳戶的幣別。

  |  | 自訂 Floodlight 變數做為指標和區隔 | 自訂 Floodlight 變數做為轉換作業資源中的原始事件屬性 |
  | --- | --- | --- |
  | `metrics` | `metrics_conversion_custom_metrics_bigquery_column_name_suffix` | `metrics_raw_event_conversion_metrics_bigquery_column_name_suffix` |
  | `dimension` | `segments_conversion_custom_dimensions_bigquery_column_name_suffix` | `segments_raw_event_conversion_dimensions_bigquery_column_name_suffix` |

**注意：** 您無法使用指令列工具設定通知。

舉例來說，下列指令會使用客戶 ID `6828088731` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 Search Ads 360 資料移轉作業。轉移作業也會指定自訂 Floodlight 變數。資料移轉作業會在預設專案中建立：

```
bq mk \
--transfer_config \
--target_dataset=mydataset \
--display_name='My Transfer' \
--data_source=search_ads \
--params='{"customer_id":"6828088731", "custom_floodlight_variables":"[{\"id\": \"9876\", \"cfv_field_name\": \"raw_event_conversion_metrics\", \"destination_table_name\": [\"Conversion\"],\"bigquery_column_name_suffix\": \"suffix1\" }]"}'
```

首次執行指令時，您會收到類似以下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照訊息中的操作說明進行，在指令列中貼上驗證碼。

**注意：** 使用指令列工具建立 Search Ads 360 資料移轉作業時，系統會採用「Schedule」(排程) 的預設值 (移轉作業的建立時間，每 24 小時執行一次) 和「Refresh window」(更新期) 的預設值 (0 - 將更新期設為預設的 7 天) 來設定移轉作業。

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

## 手動觸發 Search Ads 360 轉移作業

如果您[手動觸發轉移](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer) Search Ads 360 資料，系統每天會擷取比對表格的快照，並儲存在上次執行日期的分割區中。手動觸發轉移時，系統不會更新下列資料表的 Match Table 快照：

* 帳戶
* 廣告
* 廣告群組
* AdGroupCriterion
* 任何[ID 對應資料表](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#id-mapping)
* 資產
* BidStrategy
* 廣告活動
* CampaignCriterion
* ConversionAction
* 關鍵字
* NegativeAdGroupKeyword
* NegativeAdGroupCriterion
* NegativeCampaignKeyword
* NegativeCampaignCriterion
* ProductGroup

## 最高成效廣告活動

Search Ads 360 連接器可匯出[最高成效廣告活動](https://support.google.com/google-ads/answer/10724817?hl=zh-tw)資料。[建立資料移轉](#setup-data-transfer)時，請務必選取「納入最高成效廣告活動資料」核取方塊，因為系統預設不會匯出最高成效廣告活動資料。

納入最高成效資料會從特定資料表中移除 `ad_group` 欄位，並加入新資料表。您無法納入 `ad_group` 欄位，因為 Search Ads 360 API 會篩選最高成效資料。

選取「納入最高成效廣告活動資料表」核取方塊後，下列資料表會排除 `ad_group` 相關資料欄：

* CartDataSalesStats
* ProductAdvertised
* ProductAdvertisedDeviceStats
* ProductAdvertisedConversionActionAndDeviceStats

## 支援 Search Ads 360 管理員帳戶

使用 Search Ads 360 管理員帳戶比使用個別客戶 ID 多了幾項優點：

* 不必再針對多個客戶 ID 管理要報告的多項資料移轉作業。
* 由於所有客戶 ID 都儲存在同一份資料表中，因此更容易寫入跨客戶查詢。
* 使用管理員帳戶可減少 BigQuery 資料移轉服務載入配額問題，因為多個客戶 ID 會在同一項工作中載入。

如果現有客戶有多項特定客戶 ID 的 Search Ads 360 資料移轉作業，建議改用 Search Ads 360 管理員帳戶。如要這麼做，請按照下列步驟操作：

1. 在管理員或副管理員帳戶層級設定單一 Search Ads 360 資料移轉。
2. [排定補充作業時間。](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)
3. [停用](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#disable_a_transfer)特定客戶 ID 的 Search Ads 360 轉移作業。

如要進一步瞭解 Search Ads 360 管理員帳戶，請參閱「[關於新版 Search Ads 360 中的管理員帳戶](https://support.google.com/sa360/answer/9158072?hl=zh-tw)」和「[查看帳戶與管理員帳戶的連結方式](https://support.google.com/sa360/answer/9227233?hl=zh-tw)」。

**注意：** BigQuery 資料移轉服務會針對所有列出的客戶 ID 提取報表，但如果客戶 ID 沒有回報指定日期的活動，您可能不會在報表中看到客戶 ID。

### 範例

下列清單顯示與特定 Search Ads 360 管理員帳戶連結的客戶 ID：

* 1234567890 - 根管理員帳戶
  + 1234 — 副管理員帳戶
    - 1111 — 客戶 ID
    - 2222 — 客戶 ID
    - 3333 — 客戶 ID
    - 4444 — 客戶 ID
    - 567 — 副管理員帳戶
      * 5555 — 客戶 ID
      * 6666 — 客戶 ID
      * 7777 — 客戶 ID
  + 89 — 副管理員帳戶
    - 8888 — 客戶 ID
    - 9999 — 客戶 ID
  + 0000 — 客戶 ID

每個連結至管理員帳戶的客戶 ID 都會顯示在每份報表中。如要進一步瞭解 BigQuery 資料移轉服務中的 Search Ads 360 報表結構，請參閱「[Search Ads 360 報表轉換](https://docs.cloud.google.com/bigquery/docs/search-ads-transformation?hl=zh-tw)」。

#### 客戶 ID 1234567890 的移轉設定

根管理員帳戶 (客戶 ID 1234567890) 的移轉設定
會產生資料移轉執行作業，其中包含下列客戶 ID：

* 1111 (透過子管理員帳戶 1234)
* 2222 (透過子管理員帳戶 1234)
* 3333 (透過子管理員帳戶 1234)
* 4444 (透過子管理員帳戶 1234)
* 5555 (透過子管理員帳戶 567 和子管理員帳戶 1234)
* 6666 (透過子管理員帳戶 567 和子管理員帳戶 1234)
* 7777 (透過子管理員帳戶 567 和子管理員帳戶 1234)
* 8888 (透過子管理員帳戶 89)
* 9999 (透過子管理員帳戶 89)
* 0000 (個別客戶 ID)

#### 客戶 ID 1234 的移轉設定

副管理員帳戶 123 (客戶 ID 1234) 的移轉設定會產生資料移轉作業，其中包含下列客戶 ID：

* 1111
* 2222
* 3333
* 4444
* 5555 (透過子管理員帳戶 567)
* 6666 (透過子管理員帳戶 567)
* 7777 (透過子管理員帳戶 567)

#### 客戶 ID 567 的移轉設定

副管理員帳戶 567 (客戶 ID 567) 的移轉設定會產生資料移轉作業，其中包含下列客戶 ID：

* 5555
* 6666
* 7777

#### 客戶 ID 89 的移轉設定

副管理員帳戶 89 (客戶 ID 89) 的轉移設定會產生資料移轉作業，其中包含下列客戶 ID：

* 8888
* 9999

#### 客戶 ID 0000 的移轉設定

客戶 ID 0000 的移轉設定會產生資料移轉執行作業，其中只包含個別客戶 ID：

* 0000

## 查詢資料

資料移轉至 BigQuery 資料移轉服務時，系統會將資料寫入擷取時間分區資料表。詳情請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。

如果您要直接查詢資料表，而不要使用自動產生的檢視表，您必須在查詢中使用 `_PARTITIONTIME` 虛擬資料欄。詳情請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)一文。

## Search Ads 360 查詢範例

您可以使用下列 Search Ads 360 查詢範例來分析已移轉的資料。您也可以在 [數據分析](https://cloud.google.com/looker-studio?hl=zh-tw) 等視覺化工具中查看查詢。

以下查詢範例可協助您開始使用 BigQuery 資料移轉服務，查詢 Search Ads 360 資料。如果您對於這些報表的功能有其他問題，請洽詢您的 Search Ads 360 技術代表。

如果您要直接查詢資料表，而不要使用自動產生的檢視表，您必須在查詢中使用 `_PARTITIONTIME` 虛擬資料欄。詳情請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)一文。

### 廣告活動成效

下列查詢範例分析了最近 30 天的 Search Ads 360 廣告活動成效。

```
SELECT
  c.customer_id,
  c.campaign_name,
  c.campaign_status,
  SUM(cs.metrics_clicks) AS Clicks,
  (SUM(cs.metrics_cost_micros) / 1000000) AS Cost,
  SUM(cs.metrics_impressions) AS Impressions
FROM
  `DATASET.sa_Campaign_CUSTOMER_ID` c
LEFT JOIN
  `DATASET.sa_CampaignStats_CUSTOMER_ID` cs
ON
  (c.campaign_id = cs.campaign_id
  AND cs._DATA_DATE BETWEEN
  DATE_ADD(CURRENT_DATE(), INTERVAL -31 DAY) AND DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY))
WHERE
  c._DATA_DATE = c._LATEST_DATE
GROUP BY
  1, 2, 3
ORDER BY
  Impressions DESC
```

更改下列內容：

* `DATASET`：資料集名稱
* `CUSTOMER_ID`：Search Ads 360 客戶 ID

### 關鍵字數量

下列範例查詢會依廣告活動、廣告群組和關鍵字狀態分析關鍵字。

```
  SELECT
    c.campaign_status AS CampaignStatus,
    a.ad_group_status AS AdGroupStatus,
    k.ad_group_criterion_status AS KeywordStatus,
    k.ad_group_criterion_keyword_match_type AS KeywordMatchType,
    COUNT(*) AS count
  FROM
    `DATASET.sa_Keyword_CUSTOMER_ID` k
    JOIN
    `DATASET.sa_Campaign_CUSTOMER_ID` c
  ON
    (k.campaign_id = c.campaign_id AND k._DATA_DATE = c._DATA_DATE)
  JOIN
    `DATASET.sa_AdGroup_CUSTOMER_ID` a
  ON
    (k.ad_group_id = a.ad_group_id AND k._DATA_DATE = a._DATA_DATE)
  WHERE
    k._DATA_DATE = k._LATEST_DATE
  GROUP BY
    1, 2, 3, 4
```

更改下列內容：

* `DATASET`：資料集名稱
* `CUSTOMER_ID`：Search Ads 360 客戶 ID

## ID 對應表

新版 Search Ads 360 中的實體 (例如客戶、廣告活動和廣告群組) 具有與舊版 Search Ads 360 不同的 [ID 空間](https://developers.google.com/search-ads/v2/how-tos/reporting/id-mapping?hl=zh-tw)。如果現有的 Search Ads 360 移轉使用者想將舊版 Search Ads 360 的資料與新版 Search Ads 360 API 的資料合併，只要在移轉設定中提供有效的代理商 ID 和廣告主 ID，即可使用 BigQuery 資料移轉服務移轉 ID 對應表。

[支援的實體](https://developers.google.com/search-ads/v2/how-tos/reporting/id-mapping?hl=zh-tw)
包含 `legacy_id` 和 `new_id` 兩欄，分別指定舊版和新版 Search Ads 360 中實體的 ID 對應。
對於 AD、CAMPAIGN\_CRITERION 和 CRITERION 實體，系統也會提供 `new_secondary_id`，因為這些實體[在新版 Search Ads 360 中沒有全域專屬 ID](https://developers.google.com/search-ads/v2/how-tos/reporting/id-mapping?hl=zh-tw#object-id-uniqueness)。
以下是 ID 對應表清單。

* IdMapping\_AD
* IdMapping\_AD\_GROUP
* IdMapping\_CAMPAIGN
* IdMapping\_CAMPAIGN\_CRITERION
* IdMapping\_CAMPAIGN\_GROUP
* IdMapping\_CAMPAIGN\_GROUP\_PERFORMANCE\_TARGET
* IdMapping\_CRITERION
* IdMapping\_CUSTOMER
* IdMapping\_FEED\_ITEM
* IdMapping\_FEED\_TABLE

**注意：** 與對照表