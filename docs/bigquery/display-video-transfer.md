Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Display & Video 360 資料載入 BigQuery

您可以使用 Display & Video 360 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 Display & Video 360 載入至 BigQuery。您可以使用 BigQuery 資料移轉服務，安排週期性移轉工作，將 Display & Video 360 的最新資料新增至 BigQuery。

## 連接器總覽

Display & Video 360 連接器的 BigQuery 資料移轉服務支援下列資料移轉選項。

| 資料轉移方式 | 支援 |
| --- | --- |
| 受支援的報表 | Display & Video 360 連接器支援從[資料移轉第 2 版 (Display & Video DTv2) 檔案](https://developers.google.com/bid-manager/dtv2/reference/file-format?hl=zh-tw)移轉資料。 如要瞭解 Display & Video 360 報表如何轉換成 BigQuery 表格和檢視表，請參閱「[Display & Video 360 報表轉換](https://docs.cloud.google.com/bigquery/docs/display-video-transformation?hl=zh-tw)」一文。 |
| 重複頻率 | Display & Video 360 連接器支援每日資料轉移。    根據預設，資料移轉作業會在建立時排定時間。[設定資料移轉作業](#set_up_dv_360_transfer)時，你可以設定資料移轉時間。 |
| 重新整理時間範圍 | 資料移轉作業執行時，Display & Video 360 連接器會擷取最多 2 天前的 Display & Video 360 資料。您無法設定這個連結器的重新整理時間範圍。   詳情請參閱「[重新整理時間範圍](#refresh)」。 |
| 資料補充作業的可用性 | [執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，擷取排定資料移轉時間以外的資料。您可以擷取資料來源資料保留政策允許的最早資料。    如要瞭解 Display & Video 360 的資料保留政策，請參閱「[報表資料更新間隔和可用性](https://support.google.com/displayvideo/answer/6110224?hl=zh-tw)」。 |

## 支援的設定資料

除了報表資料，BigQuery 資料移轉服務也會從 Display & Video 360 移轉下列設定資料。設定資料會從 [Display & Video 360 API v3](https://developers.google.com/display-video/api/reference/rest/v3?hl=zh-tw) 擷取。

* [合作夥伴](https://developers.google.com/display-video/api/reference/rest/v3/partners?hl=zh-tw#resource:-partner)
* [廣告主](https://developers.google.com/display-video/api/reference/rest/v3/advertisers?hl=zh-tw#resource:-advertiser)
* [LineItem](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.lineItems?hl=zh-tw#LineItem)
* [LineItemTargeting](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.lineItems/bulkListAssignedTargetingOptions?hl=zh-tw#LineItemAssignedTargetingOption)
* [Campaign](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.campaigns?hl=zh-tw#Campaign)
* [CampaignTargeting](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.campaigns.targetingTypes.assignedTargetingOptions?hl=zh-tw#AssignedTargetingOption)
* [InsertionOrder](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.insertionOrders?hl=zh-tw#InsertionOrder)
* [InsertionOrderTargeting](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.insertionOrders.targetingTypes.assignedTargetingOptions?hl=zh-tw#AssignedTargetingOption)
* [AdGroup](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.adGroups?hl=zh-tw#AdGroup)
* [AdGroupTargeting](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.adGroups/bulkListAdGroupAssignedTargetingOptions?hl=zh-tw#AdGroupAssignedTargetingOption)
* [AdGroupAd](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.adGroupAds?hl=zh-tw#AdGroupAd)
* [廣告素材](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.creatives?hl=zh-tw#resource:-creative)

如要進一步瞭解各類設定資料，請參閱下列連結：

* [關於合作夥伴](https://support.google.com/displayvideo/answer/7622449?hl=zh-tw)
* [建立廣告主](https://support.google.com/displayvideo/answer/3424070?hl=zh-tw)
* [建立委刊項](https://support.google.com/displayvideo/answer/2891312?hl=zh-tw)
* [建立廣告活動](https://support.google.com/displayvideo/answer/7205081?hl=zh-tw)
* [建立廣告訂單](https://support.google.com/displayvideo/answer/2696705?hl=zh-tw)
* [關於 YouTube 與合作夥伴委刊項](https://support.google.com/displayvideo/answer/6274216?hl=zh-tw)
* [管理廣告素材](https://support.google.com/displayvideo/answer/7530472?hl=zh-tw)

## 從 Display & Video 360 轉移作業擷取資料

從 Display & Video 360 將資料移轉至 BigQuery 時，系統會將資料載入以日期為分區依據的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果為同一天排定多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該特定日期的資料分割。同一天內進行多次轉移或執行回填作業，不會導致資料重複，也不會影響其他日期的分區。

### 重新整理視窗

*更新期*是指資料移轉作業在進行時，擷取資料的天數。舉例來說，如果重新整理時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務就會從來源資料表擷取過去三天的所有資料。在這個範例中，每天進行移轉時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分割區，並複製當天的來源資料表資料，然後自動觸發補充作業執行作業，以更新過去兩天的來源資料表資料。系統自動觸發的回填作業會覆寫或增量更新 BigQuery 目的地資料表，具體做法取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。舉例來說，如果重新整理時間範圍為三天，而您是第一次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

如要擷取重新整理時間範圍外的資料 (例如歷來資料)，或從任何轉移中斷或缺漏中復原資料，可以啟動或排定[補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 事前準備

建立 Display & Video 360 資料轉移作業前，請先查看下列必要條件和資訊。

### 必要條件

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，儲存 Display & Video 360 資料。
* 請確認您擁有 Display & Video 360 [合作夥伴 ID](https://support.google.com/displayvideo/answer/7622449?hl=zh-tw) 或[廣告主 ID](https://support.google.com/displayvideo/answer/11415707?hl=zh-tw)。
  合作夥伴 ID 是階層中的父項。
* 確認您擁有[讀取權限](https://support.google.com/displayvideo/answer/2723011?hl=zh-tw)，可透過 Display & Video API 存取夥伴或廣告主資料。
* 確認貴機構可存取 Display & Video 360 資料移轉 v2 (Display & Video 360 DTv2) 檔案。這些檔案會由 Display & Video 360 團隊傳送至 Cloud Storage bucket。如要要求存取 Display & Video 360 DTv2 檔案，請視您是否與 Display & Video 360 簽訂直接合約而定。無論是哪種情況，都可能需要支付額外費用。

  + 如果您與 Display & Video 360 簽訂合約，請[與 Display & Video 360 支援團隊聯絡](https://support.google.com/displayvideo/answer/9026876?hl=zh-tw)，設定 Display & Video 360 DTv2 檔案。
  + 如果您沒有 Display & Video 360 合約，請與代理商聯絡，取得 Display & Video 360 DTv2 檔案的存取權。
  + 完成上述步驟後，您會收到下列任一 Cloud Storage bucket 名稱，視設定是為合作夥伴或廣告主而定：
    - `gs://dcdt_-dbm_partnerPARTNER_ID`
    - `gs://dcdt_-dbm_advertiserADVERTISER_ID`**注意：** 團隊無法代表您產生或授予 Display & Video 360 DTv2 檔案的存取權。 Google Cloud 如要存取 Display & Video 360 DTv2 檔案，請與 Display & Video 360 [支援團隊](https://support.google.com/displayvideo/answer/9026876?hl=zh-tw)或您的代理商聯絡。
* 如要為 Pub/Sub 設定移轉作業執行通知，您必須擁有 `pubsub.topics.setIamPolicy` 權限。詳情請參閱「[BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)」。

### 查看 Display & Video 360 ID

如要擷取 Display & Video 360 ID，請前往 Google Cloud 主控台的 Cloud Storage「Buckets」頁面，並檢查 Display & Video 360 資料移轉 Cloud Storage bucket 中的檔案。Display & Video 360 ID 可用來在您提供的 Cloud Storage bucket 中比對檔案，這個 ID 會嵌入檔案名稱，而非 Cloud Storage 值區名稱。例如：

* 在名為 `dbm_partner123_activity_*` 的檔案中，ID 為 `123`。
* 在名為 `dbm_advertiser567_activity_*` 的檔案中，ID 為 `567`。

### 尋找檔案名稱前置字串

在某些情況下，您 Cloud Storage bucket 中的檔案可能包含由 Google Marketing Platform 服務團隊為您設定的非標準自訂檔案名稱。例如：

在名為 `dbm_partner123456custom_activity_*` 的檔案中，前置字串為 `dbm_partner123456custom`。

如需檔案名前置字元相關協助，請與 [Display & Video 360 支援團隊](https://support.google.com/displayvideo/answer/9026876?hl=zh-tw)聯絡。

## 設定 Display & Video 360 資料移轉

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Create transfer」(建立轉移作業)頁面執行下列操作：

   * 在「Source type」(來源類型) 專區，「Source」(來源) 請選擇「Display & Video 360」。
   * 在「Transfer config name」(轉移設定名稱) 專區，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱。移轉作業名稱可以是任何值，能讓您辨識移轉作業，方便您日後在必要時進行修改。
4. 在「Schedule options」(排程選項) 專區：

   * 選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
   * 「Repeats」請選擇您要多久移轉一次。如果選取「Days」(天)，請按照世界標準時間提供有效的值。
5. 在「Destination settings」(目的地設定) 部分的「Destination dataset」(目的地資料集) 選單，請選取您為了儲存資料而建立的資料集。
6. 在「Data source details」(資料來源詳細資料) 區段：

   * 在「DV360 DTV2 Cloud Storage bucket」欄位中，輸入含有 Display & Video 360 DTv2 檔案的 Cloud Storage bucket。如果您需要設定這個 bucket，請與 Display & Video 360 [支援團隊](https://support.google.com/displayvideo/answer/9026876?hl=zh-tw)聯絡。
   * 在「DV360 Partner/Advertiser ID」(DV360 合作夥伴/廣告主 ID) 欄位中，輸入[合作夥伴 ID](https://support.google.com/displayvideo/answer/7622449?hl=zh-tw) 或[廣告主 ID](https://support.google.com/displayvideo/answer/11415707?hl=zh-tw)。
   * (選用) 在「Notification options」(通知選項) 專區：
     + 按一下啟用電子郵件通知的切換開關。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
     + 點選切換按鈕，啟用 Pub/Sub 通知。在「Select a Cloud Pub/Sub topic」(選取 Cloud Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
7. 按一下 [儲存]。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。必須加上以下旗標：

* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

```
  bq mk --transfer_config \
  --project_id=PROJECT_ID \
  --target_dataset=DATASET \
  --display_name=NAME \
  --params='PARAMETERS' \
  --data_source=DATA_SOURCE
```

其中：

* PROJECT\_ID：您的專案 ID。
* DATASET：資料移轉設定的目標資料集。
* NAME：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* PARAMETERS：已建立資料移轉設定的 JSON 格式參數。舉例來說，`--params='{"param":"param_value"}'`。如果是 Display & Video 360 轉移作業，則必須提供 `bucket` 和 `displayvideo_id` 參數。`file_name_prefix` 參數為選用，僅適用於罕見的自訂檔案名稱。
* DATA\_SOURCE：資料來源 - `displayvideo`。

舉例來說，下列指令會使用 Display & Video 360 ID `123456`、Cloud Storage 值區 `dcdt_-dbm_partner123456` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 Display & Video 360 資料移轉作業。

資料移轉作業會在預設專案中建立：

```
  bq mk --transfer_config \
  --target_dataset=mydataset \
  --display_name='My Transfer' \
  --params='{"bucket":"dcdt_-dbm_partner123456","displayvideo_id": "123456","file_name_prefix":"YYY"}' \
  --data_source=displayvideo
```

執行指令後，您會收到如下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照訊息中的操作說明進行，在指令列中貼上驗證碼。

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

## 查詢資料

資料移轉至 BigQuery 時，系統會將資料寫入擷取時間分區資料表。詳情請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。

建議您查詢自動產生的檢視表，而非直接查詢資料表。不過，如要直接查詢資料表，您必須在查詢中使用 `_PARTITIONTIME` 虛擬資料欄。詳情請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]