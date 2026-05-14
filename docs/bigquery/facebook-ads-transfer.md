Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Facebook 廣告資料載入 BigQuery

你可以使用 Facebook Ads 連接器專用的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將 Facebook Ads 的資料載入 BigQuery。您可以使用 BigQuery 資料移轉服務，安排週期性移轉工作，將 Facebook 廣告的最新資料新增至 BigQuery。

## 連接器總覽

Facebook 廣告連結器的 BigQuery 資料移轉服務支援下列資料移轉選項。

| 資料轉移方式 | 支援 |
| --- | --- |
| 受支援的報表 | Facebook 廣告適用的 BigQuery 資料移轉服務支援移轉下列 Facebook 廣告報表：  * `AdAccounts` * `AdInsights` * `AdInsightsActions`   如要瞭解 Facebook Ads 報表如何轉換成 BigQuery 表格和視圖，請參閱「[Facebook Ads 報表轉換](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transformation?hl=zh-tw)」一文。 |
| 重複頻率 | Facebook 廣告連接器支援每日資料移轉。    根據預設，資料移轉作業會在建立時排定時間。[設定資料移轉作業](#fb_ads_transfer_setup)時，你可以設定資料移轉時間。 |
| 重新整理時間範圍 | Facebook 廣告連接器會在執行資料移轉時，擷取最多 30 天的 Facebook 廣告資料。您無法設定這個連結器的重新整理時間範圍。   詳情請參閱「[重新整理時間範圍](#refresh)」。 |
| 資料補充作業的可用性 | [執行資料補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)，擷取排定資料移轉時間以外的資料。您可以擷取資料來源資料保留政策允許的最早資料。 |

## 限制

Facebook 廣告資料移轉作業會受到下列限制：

* Facebook 廣告資料轉移作業之間的最短時間間隔為 24 小時。週期性資料移轉的預設間隔為 24 小時。
* Facebook 廣告專用的 BigQuery 資料移轉服務僅支援一組固定的資料表。不支援自訂報表。
* Facebook 廣告資料轉移作業最多需要六小時。如果轉移作業超過這個時間上限，就會失敗。
* `AdInsights` 和 `AdInsightsActions` 表格不支援增量轉移。建立包含 `AdInsights` 和 `AdInsightsActions` 資料表的資料移轉作業，並在「排程選項」中指定日期時，系統會移轉該日期可用的所有資料。
* BigQuery 資料移轉服務支援最多 30 天的重新整理時間範圍，可重新整理 `AdInsights` 和 `AdInsightsActions` 資料表。更新期是指資料移轉作業從來源資料擷取資料的天數。首次執行資料移轉時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。
* Facebook 廣告轉移作業需要長期有效的存取權杖，但這類權杖會在 60 天後失效。

  如果長期有效的使用者存取權杖已過期，請前往資料移轉詳細資料頁面，然後按一下「編輯」，即可取得新的權杖。在編輯轉移頁面中，按照「[Facebook 廣告事前準備](#fb_ads_prereqs)」中的步驟產生新的長期有效使用者存取權杖。
* 如要透過網路連結進行資料移轉，請務必先[定義靜態 IP 位址，再建立網路連結](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw)。
* 如果設定的網路連結和虛擬機器 (VM) 執行個體位於不同區域，從 Facebook Ads 轉移資料時，可能會發生跨區域資料移動。

## 從 Facebook 廣告轉移作業擷取資料

從 Facebook 廣告將資料移轉至 BigQuery 時，系統會將資料載入依日期分區的 BigQuery 資料表。資料載入的資料表分區會對應至資料來源的日期。如果為同一天排定多項移轉作業，BigQuery 資料移轉服務會以最新資料覆寫該特定日期的資料分割。同一天內進行多次轉移或執行回填作業，不會導致資料重複，也不會影響其他日期的分區。

如果是 `AdInsights` 和 `AdInsightsActions` 資料表，資料載入的資料表分區會對應至資料來源的日期。

對於 `AdAccounts` 表格，系統每天會擷取一次快照，並儲存在上次移轉執行日期的分區中。重新整理視窗不適用於 `AdAccounts` 資料表。

### 重新整理視窗

*更新期*是指資料移轉作業在進行時，擷取資料的天數。舉例來說，如果重新整理時間範圍為三天，且每天都會進行移轉，BigQuery 資料移轉服務就會從來源資料表擷取過去三天的所有資料。在這個範例中，每天進行移轉時，BigQuery 資料移轉服務會建立新的 BigQuery 目的地資料表分割區，並複製當天的來源資料表資料，然後自動觸發補充作業執行作業，以更新過去兩天的來源資料表資料。系統自動觸發的回填作業會覆寫或增量更新 BigQuery 目的地資料表，具體做法取決於 BigQuery 資料移轉服務連接器是否支援增量更新。

首次執行資料移轉時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。舉例來說，如果重新整理時間範圍為三天，而您是第一次執行資料移轉作業，BigQuery 資料移轉服務會擷取三天內的所有來源資料。

如要擷取重新整理時間範圍外的資料 (例如歷來資料)，或從任何轉移中斷或缺漏中復原資料，可以啟動或排定[補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 事前準備

下列各節將說明建立 Facebook 廣告資料移轉作業前，您需要採取的步驟。

### Facebook 廣告的必要條件

建立 Facebook 廣告資料移轉作業時，請確認您擁有下列 Facebook 廣告資訊。

| Facebook 廣告參數 | 說明 |
| --- | --- |
| `clientID` | OAuth 2.0 用戶端的應用程式 ID 名稱。 |
| `clientSecret` | OAuth 2.0 用戶端的應用程式密鑰。 |
| `refreshToken` | 長期有效的使用者存取權杖，也稱為「更新」權杖。 |

如要取得 `clientID` 和 `clientSecret`，請執行下列步驟：

1. [建立 Facebook 開發人員應用程式](https://developers.facebook.com/docs/development/create-an-app/other-app-types)，應用程式類型為 `Business`。
2. 在 [Facebook 應用程式資訊主頁](https://developers.facebook.com/apps)中，依序點選「應用程式設定」>「基本」，然後找出與應用程式對應的應用程式 ID 和應用程式密鑰。

如要取得長期有效的使用者存取權杖 (又稱「更新」權杖)，請按照下列步驟操作：

1. 在 Google Cloud 控制台中，按照步驟[建立 Facebook 廣告轉移作業](#fb_ads_transfer_setup)。
2. 在「資料來源詳細資料」部分，複製「重新整理權杖」欄位後列出的重新導向 URI。
3. 按一下「Facebook 應用程式資訊主頁」，然後按一下「Facebook 企業登入」部分中的「設定」。
4. 在「Settings」頁面中，於「Valid OAuth Redirect URIs」欄位輸入重新導向網址，然後按一下「Save」。
5. 返回 Google Cloud 控制台。在「資料來源詳細資料」部分，按一下「授權」。系統會將您重新導向至 Facebook 驗證頁面。
6. 選取 Facebook 開發人員應用程式，授權與 BigQuery 資料移轉服務連結的帳戶。
7. 完成後，按一下「我知道了」返回 Google Cloud 控制台。移轉設定中現在會填入長期有效的使用者存取權杖。

長期有效的使用者存取權杖會在 60 天後失效。如要瞭解如何取得新的長期有效使用者存取權杖，請參閱「[限制](#limitations)」。

#### 更新權杖替代方案

或者，如果您已透過下列任一方法取得更新權杖，也可以在[建立資料移轉作業](#fb_ads_transfer_setup)時提供該權杖：

* [使用 Graph API 產生長期有效的使用者存取權杖](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived)。
  您必須具備 `ads_management`、`ads_read` 和 `business_management` 權限，才能取得資料移轉作業的有效權杖。
* [產生系統使用者權杖](https://developers.facebook.com/docs/facebook-login/guides/access-tokens)。
  系統使用者權杖可讓您手動新增資產 (例如廣告帳戶)，以便納入資料移轉作業。如果系統使用者權杖過期，您必須手動使用新憑證更新轉移設定。建立系統使用者權杖時，您也可以選擇建立不會過期的權杖。詳情請參閱「[支援的存取權杖](https://developers.facebook.com/docs/facebook-login/facebook-login-for-business#supported-access-tokens)」。

### BigQuery 必要條件

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* 如要為 Pub/Sub 設定移轉作業執行通知，請確認您擁有 `pubsub.topics.setIamPolicy` 身分與存取權管理 (IAM) 權限。如果您只設定電子郵件通知，則不需要 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

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

## 建立 Facebook 廣告資料移轉作業

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Source type」(來源類型) 專區中，針對「Source」(來源)，選取「Facebook Ads」(Facebook 廣告)。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「Network attachment」(網路連結) 部分，從選單中選取網路連結。如要透過網路連結進行資料移轉，請務必先[定義靜態 IP 位址，再建立網路連結](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw)。
   * 在「Client ID」(用戶端 ID) 中輸入應用程式 ID。
   * 在「Client secret」(用戶端密鑰) 部分，輸入應用程式密鑰。
   * 在「Refresh token」(更新權杖) 部分，按一下「Authorize」(授權)，然後輸入長期有效的使用者存取權杖 ID。如果[已有更新權杖或系統使用者權杖](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#refresh_token_alternatives)，也可以直接在這個欄位輸入更新權杖。如要瞭解如何擷取長期有效的使用者存取權杖，請參閱 [Facebook 廣告事前準備](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#fb_ads_prereqs)的相關說明。
   * 如要**移轉 Facebook 廣告物件**：請指定要納入這次移轉作業的 Facebook 廣告報表或物件。
   * 選取「Fetch Data for Authorized Ad Accounts Only」(僅擷取授權廣告帳戶的資料)，只從授權給您 Facebook 應用程式的廣告帳戶擷取資料。您可以在「App Settings」(應用程式設定) >「Advanced」(進階) 的「Advertising accounts」(廣告帳戶) 部分中，找到授權的廣告帳戶。
   * 如為「ActionsCollections」，請指定一或多個[動作集合](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#action_collections)。
   * 在「Generic Breakdowns」(一般細目) 部分，選取洞察資料的一般細目。這些細目會決定移轉的資料在 `AdInsights` 和 `AdInsightsActions` 資料表中的整理方式。Facebook 廣告只允許特定細目組合。如要進一步瞭解允許的細目組合，請參閱「[合併細分](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#combining_breakdowns)」
   * 在「Action Breakdowns」(動作細目) 部分，選取洞察資料的動作細目。這些細目決定了移轉的資料在 `AdInsightsActions` 資料表中的整理方式。如要瞭解如何合併細目，請參閱「[合併細目](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#combining_breakdowns)」。
   * 在「Refresh window」(重新整理時間範圍) 部分，指定[重新整理時間範圍](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#refresh)的持續時間。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業名稱。
7. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 在「Repeat frequency」(重複頻率) 清單選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請點選「Email notification」(電子郵件通知) 切換按鈕。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
   * 如要針對這項資料移轉作業啟用 [Pub/Sub 移轉作業執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請點選「Pub/Sub notifications」(Pub/Sub 通知) 切換按鈕。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，也可以點選「Create a topic」(建立主題) 來建立主題。
9. 按一下「儲存」。

執行這項資料移轉作業時，BigQuery 資料移轉服務會自動填入下列資料表。

| 資料表名稱 | 說明 |
| --- | --- |
| `AdAccounts` | 使用者可用的廣告帳戶。 |
| `AdInsights` | 所有廣告帳戶的廣告洞察報表。 |
| `AdInsightsActions` | 所有廣告帳戶的廣告洞察動作報表。 |

### bq

輸入 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)
並加上移轉建立標記
`--transfer_config`：

```
bq mk
    --transfer_config
    --project_id=PROJECT_ID
    --data_source=DATA_SOURCE
    --display_name=DISPLAY_NAME
    --target_dataset=DATASET
    --params='PARAMETERS'
```

其中：

* PROJECT\_ID (選用)：您的 Google Cloud 專案 ID。
  如未提供 `--project_id` 指定特定專案，系統會使用預設專案。
* DATA\_SOURCE：資料來源 (例如 `facebook-ads`)。
* DISPLAY\_NAME：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATASET：資料移轉設定的目標資料集。
* PARAMETERS：已建立資料移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。以下是 Facebook 廣告轉移作業的參數：
  + `connector.authentication.oauth.clientId`：OAuth 2.0 用戶端的應用程式 ID 名稱。
  + `connector.authentication.oauth.clientSecret`：OAuth 2.0 用戶端的應用程式密鑰。
  + `connector.authentication.oauth.refreshToken`：長期有效權杖 ID。
  + `connector.authorizedAdAccountsOnly`：如果設為 `true`，連結器只會從授權給您 Facebook 應用程式的廣告帳戶擷取資料。您可以在「App Settings」(應用程式設定) >「Advanced」(進階) 的「Advanced accounts」(進階帳戶) 部分中，找到授權的廣告帳戶。
  + `connector.actionCollections`：動作集合是物件，可指定使用者對廣告採取的不同動作類型。如需 `actionCollections` 值的完整清單，請參閱「[動作集合](#action_collections)」。
    - 詳情請參閱「[廣告洞察](https://developers.facebook.com/docs/marketing-api/reference/adgroup/insights)」一文。
  + `connector.genericBreakdowns`：指定洞察資料的一般細目。這些細目會決定移轉的資料在 `AdInsights` 和 `AdInsightsActions` 資料表中的整理方式。Facebook 廣告只允許特定細目組合。如要進一步瞭解允許的細目組合，請參閱「[合併細分](#combining_breakdowns)」。
  + `actionBreakdowns`：指定洞察資料的動作細目。這些細目會決定移轉的資料在 `AdInsights` 和 `AdInsightsActions` 資料表中的整理方式。如要瞭解如何合併細目，請參閱「[合併細目](#combining_breakdowns)」。

舉例來說，下列指令會在預設專案中建立 Facebook Ads 資料移轉作業，並提供所有必要參數：

```
bq mk
--transfer_config
--target_dataset=mydataset
--data_source=facebook_ads
--display_name='My Transfer'
--params='{"connector.authentication.oauth.clientId": "1650000000",
    "connector.authentication.oauth.clientSecret":"TBA99550",
    "connector.authentication.oauth.refreshToken":"abcdef",
    "connector.authorizedAdAccountsOnly":true,
    "connector.actionCollections":["Actions", "Conversions"],
    "connector.genericBreakdowns":["PublisherPlatform", "PlatformPosition"],
    "connector.actionBreakdowns":["ActionDevice", "ActionType"]}'
```

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

儲存移轉設定後，Facebook Ads 連接器會根據排程選項，自動觸發移轉作業。每次執行移轉作業時，Facebook 廣告連接器都會將 Facebook 廣告中的所有可用資料移轉至 BigQuery。

如要在正常排程以外手動執行資料移轉作業，可以啟動[回填作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

如要瞭解轉移的資料如何對應至 Meta API 欄位，請參閱「[Facebook 廣告報表轉換](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transformation?hl=zh-tw)」。

## 動作集合

動作集合是物件，可指定使用者對廣告採取的不同動作類型。您可以在[設定轉移設定](#fb_ads_transfer_setup)時指定動作集合。

動作集合代表 [`Ad Account, Insights` 端點回應中存在的 [`list<AdsActionStats>` 類型](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/)欄位](https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/)。

轉移完成後，這些動作集合會填入[`AdInsightsActions`表格](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transformation?hl=zh-tw#adinsightsactions_report)。

**注意：** 為移轉指定越多動作集合，就越有可能[達到 Facebook Ads 設下的頻率限制](https://developers.facebook.com/docs/marketing-api/overview/rate-limiting)。

以下列出 Facebook 廣告資料移轉支援的動作集合：

* `ActionValues`
* `Actions`
* `AdClickActions`
* `AdImpressionActions`
* `CatalogSegmentActions`
* `CatalogSegmentValue`
* `CatalogSegmentValueMobilePurchaseRoas`
* `CatalogSegmentValueOmniPurchaseRoas`
* `CatalogSegmentValueWebsitePurchaseRoas`
* `ConversionValues`
* `Conversions`
* `ConvertedProductQuantity`
* `ConvertedProductValue`
* `CostPer15_secVideoView`
* `CostPer2SecContinuousVideoView`
* `CostPerActionType`
* `CostPerAdClick`
* `CostPerConversion`
* `CostPerOneThousandAdImpression`
* `CostPerOutboundClick`
* `CostPerThruplay`
* `CostPerUniqueActionType`
* `CostPerUniqueConversion`
* `CostPerUniqueOutboundClick`
* `InteractiveComponentTap`
* `MobileAppPurchaseRoas`
* `OutboundClicks`
* `OutboundClicksCtr`
* `PurchaseRoas`
* `UniqueActions`
* `UniqueConversions`
* `UniqueOutboundClicks`
* `UniqueOutboundClicksCtr`
* `UniqueVideoView15_sec`
* `Video15_secWatchedActions`
* `Video30_secWatchedActions`
* `VideoAvgTimeWatchedActions`
* `VideoContinuous2SecWatchedActions`
* `VideoP100_watchedActions`
* `VideoP25WatchedActions`
* `VideoP50WatchedActions`
* `VideoP75WatchedActions`
* `VideoP95WatchedActions`
* `VideoPlayActions`
* `VideoPlayCurveActions`
* `VideoPlayRetentionGraphActions`
* `VideoTimeWatchedActions`
* `WebsiteCtr`
* `WebsitePurchaseRoas`

## 合併細分

Facebook Ads 對可一起選取的欄設有限制。使用這些受限組合會導致資料移轉失敗。

如要進一步瞭解可合併的細目，請參閱「[合併細目](https://developers.facebook.com/docs/marketing-api/insights/breakdowns/#combiningbreakdowns)」。

## 排解轉移設定問題

如果無法順利設定 Facebook 廣告資料移轉作業，請嘗試下列疑難排解步驟：

* 使用 [Facebook 存取權杖偵錯工具](https://developers.facebook.com/tools/debug/accesstoken/)，檢查使用者存取權杖是否已過期。長期有效的使用者存取權權杖會在 60 天後失效。如果長期有效的使用者存取權杖已過期，請前往轉移詳細資料，然後按一下「編輯」修改轉移設定。在編輯轉移頁面中，按照「[Facebook 廣告先決條件](#fb_ads_prereqs)」一文中的步驟產生新的代碼。
* 確認長期有效的使用者存取權杖是使用必要權限 (`ads_management`、`ads_read` 和 `business_management`) 產生。如要檢查長期使用者存取權杖的權限，請在瀏覽器中輸入下列連結：

  ```
  https://graph.facebook.com/me/permissions?access_token=TOKEN
  ```

  其中 TOKEN 是長期使用者存取權杖的值。

  如果沒有必要權限，請按照「[Facebook 廣告事前準備](#fb_ads_prereqs)」一文中的步驟，產生新的長期有效使用者存取權杖。
* 在 [Facebook 應用程式資訊主頁](https://developers.facebook.com/apps)的「必要行動」分頁中，查看是否有需要處理的項目。

您可能會看到下列與 Meta API 速率限制錯誤相關的錯誤訊息：

發生錯誤：`There have been too many calls from this ad-account. Wait a bit and try again.`
:   **解決方法**：確認沒有平行工作流程使用相同的應用程式或憑證。如果這些錯誤仍未解決，請嘗試將權限升級為**進階存取權**，取得更多頻率限制配額。詳情請參閱「[行銷 API 使用頻率限制](https://developers.facebook.com/docs/marketing-apis/rate-limiting/)」。

### 常見的監控指標訊息

您也可以查看 [BigQuery 資料移轉服務監控指標](https://docs.cloud.google.com/bigquery/docs/dts-monitor?hl=zh-tw#monitor)，判斷資料移轉失敗的原因。下表列出 Facebook 廣告資料轉移的一些常見 `ERROR_CODE` 訊息。

| 錯誤 | 說明 |
| --- | --- |
| `INVALID_ARGUMENT` | 提供的設定無效。您也可能會遇到這個錯誤，並看到「如要瞭解有效的細目組合，請參閱『[合併細目](#combining_breakdowns)』」訊息。`This combination of action and generic breakdowns is not allowed.` |
| `PERMISSION_DENIED` | 憑證無效 |
| `UNAUTHENTICATED` | 必須驗證 |
| `SERVICE_UNAVAILABLE` | 這項服務暫時無法處理這項資料移轉作業 |
| `DEADLINE_EXCEEDED` | 資料移轉未在六小時內完成 |
| `NOT_FOUND` | 找不到要求的資源 |
| `INTERNAL` | 其他原因導致連接器失敗 |
| `FAILED_PRECONDITION` | 這個錯誤可能會連帶顯示「This error can occur when you include a network attachment with your transfer but have not configured your public network address translation (NAT) correctly.」訊息。如果傳輸內容包含網路附件，但您未正確設定公用網路位址轉譯 (NAT)，就可能發生這個錯誤。`There was an issue connecting to Facebook Ads API.`如要解決這項錯誤，請按照[定義靜態 IP 位址來建立網路連結](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw#create_a_network_attachment)的步驟操作。 |
| `RESOURCE_EXHAUSTED` | 資料來源配額或限制已用盡 |

## 定價

如要瞭解 Facebook 廣告移轉作業的定價資訊，請參閱[資料移轉服務定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#bqdts)。

## 後續步驟

* 進一步瞭解 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。
* 進一步瞭解如何[處理移轉作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)，例如查看設定和執行記錄。
* 瞭解如何[透過跨雲端作業載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]