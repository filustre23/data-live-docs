Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Facebook 廣告資料載入 BigQuery

如要排定從 Facebook Ads 到 BigQuery 的週期性資料移轉作業，請建立移轉設定，指定要移轉的資料物件，以及排定資料移轉作業的頻率。您可以使用 Google Cloud 控制台、`bq` 指令列工具或 BigQuery 資料移轉服務 API，建立資料移轉設定。設定完移轉設定後，[BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)就會按照指定時間表，將最新資料移轉至 BigQuery 資料表。

如要瞭解 Facebook 廣告移轉作業的運作方式，請參閱「[Facebook 廣告資料移轉簡介](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer-intro?hl=zh-tw)」。

## 限制

Facebook 廣告資料移轉作業會受到下列限制：

* 自 2026 年 7 月 6 日起，系統將暫時停用`AdInsightsMMM`報表。詳情請參閱「[2026 年 7 月 6 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Jul06-fb-ads)」一節。
* 定期轉移 Facebook 廣告資料的最短時間間隔為 24 小時。週期性資料移轉的預設間隔為 24 小時。
* Facebook 廣告專用的 BigQuery 資料移轉服務僅支援一組固定的資料表。不支援自訂報表。
* Facebook 廣告資料轉移作業最多需要六小時。如果轉移作業超過這個時間上限，就會失敗。
* 增量轉移作業不支援 `AdInsights`、`AdInsightsActions`、`Ads`、`Campaigns` 和 `AdSets` 資料表。建立資料轉移作業時，如果包含 `AdInsights`、`AdInsightsActions`、`Ads`、`Campaigns` 和 `AdSets` 資料表，且您在「排程選項」中指定日期，系統會轉移該日期可用的所有資料。
* BigQuery 資料移轉服務支援最多 30 天的重新整理時間範圍，可重新整理 `AdInsights`、`AdInsightsActions`、`Ads`、`Campaigns` 和 `AdSets` 資料表。更新期是指資料移轉作業從來源資料擷取資料的天數。首次執行資料移轉作業時，資料移轉作業會擷取重新整理視窗內的所有可用來源資料。
* Facebook 廣告轉移作業需要長期有效的使用者存取權杖，但這類權杖會在 60 天後失效。

  如果長期有效的使用者存取權權杖已過期，請前往資料轉移詳細資料頁面，然後按一下「編輯」，即可取得新的權杖。在編輯轉移頁面中，按照「[Facebook 廣告事前準備](#fb_ads_prereqs)」中的步驟，產生新的長期有效使用者存取權杖。
* 如要透過網路連結進行資料移轉，請務必先[定義靜態 IP 位址，再建立網路連結](https://docs.cloud.google.com/bigquery/docs/connect-to-sap-datasphere?hl=zh-tw#create-network-attachment)。
* 如果設定的網路連結和虛擬機器 (VM) 執行個體位於不同區域，從 Facebook Ads 轉移資料時，可能會發生跨區域資料移動。

## 事前準備

下列各節說明建立 Facebook 廣告資料轉移作業前，您需要採取的步驟。

### Facebook 廣告的必要條件

建立 Facebook 廣告資料轉移作業時，請確認您擁有下列 Facebook 廣告資訊。

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
4. 在「Settings」頁面的「Valid OAuth Redirect URIs」欄位中輸入重新導向網址，然後按一下「Save」。
5. 返回 Google Cloud 控制台。在「資料來源詳細資料」部分，按一下「授權」。系統會將您重新導向至 Facebook 驗證頁面。
6. 選取 Facebook 開發人員應用程式，授權與 BigQuery 資料移轉服務連結的帳戶。
7. 完成後，按一下「我知道了」返回 Google Cloud 控制台。系統現在會在移轉設定中填入長期有效的使用者存取權杖。

長期使用者存取權杖的有效期限為 60 天。如要瞭解如何取得新的長期有效使用者存取權杖，請參閱「[限制](#limitations)」。

#### 更新權杖替代方案

或者，如果您已透過下列任一方法取得更新權杖，也可以在[建立資料移轉](#fb_ads_transfer_setup)時提供：

* [使用 Graph API 產生長期有效的使用者存取權杖](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived)。
  您必須具備 `ads_management`、`ads_read` 和 `business_management` 權限，才能取得資料移轉作業的有效權杖。
* [產生系統使用者權杖](https://developers.facebook.com/docs/facebook-login/guides/access-tokens)。
  系統使用者權杖可讓您手動新增資產 (例如廣告帳戶)，以便納入資料轉移作業。如果系統使用者權杖過期，您必須手動使用新憑證更新移轉設定。建立系統使用者權杖時，您也可以選擇建立不會過期的權杖。詳情請參閱「[支援的存取權杖](https://developers.facebook.com/docs/facebook-login/facebook-login-for-business#supported-access-tokens)」。

### BigQuery 必要條件

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* 如要為 Pub/Sub 設定移轉作業執行通知，請確認您擁有 `pubsub.topics.setIamPolicy` 身分與存取權管理 (IAM) 權限。如果您只設定電子郵件通知，則不需要 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員在專案中授予您 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

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
2. 按一下「建立轉移作業」add。
3. 在「Source type」(來源類型) 專區中，針對「Source」(來源)，選取「Facebook Ads」(Facebook 廣告)。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「Network attachment」(網路連結) 部分，從選單中選取網路連結。如要透過網路連結進行資料移轉，請務必先[定義靜態 IP 位址，再建立網路連結](https://docs.cloud.google.com/bigquery/docs/connect-to-sap-datasphere?hl=zh-tw#create-network-attachment)。
   * 在「Client ID」(用戶端 ID) 中輸入應用程式 ID。
   * 在「Client secret」(用戶端密鑰) 部分，輸入應用程式密鑰。
   * 在「Refresh token」(更新權杖) 部分，按一下「Authorize」(授權)，然後輸入長期有效的使用者存取權杖 ID。如果[已有更新權杖或系統使用者權杖](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#refresh_token_alternatives)，也可以直接在這個欄位輸入更新權杖。如要瞭解如何擷取長期有效的使用者存取權杖，請參閱 [Facebook 廣告事前準備](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#fb_ads_prereqs)的相關說明。
   * 如要**移轉 Facebook 廣告物件**：請指定要納入這次移轉作業的 Facebook 廣告報表或物件。
   * 選取「Fetch Data for Authorized Ad Accounts Only」(僅擷取授權廣告帳戶的資料)，只從授權給您 Facebook 應用程式的廣告帳戶擷取資料。您可以在「App Settings」(應用程式設定) >「Advanced」(進階) 的「Advertising accounts」(廣告帳戶) 部分中，找到授權的廣告帳戶。
   * 如為「ActionsCollections」，請指定一或多個[動作集合](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#action_collections)。
   * 在「Generic Breakdowns」(一般細目) 部分，選取洞察資料的一般細目。這些細目會決定移轉的資料在 `AdInsights` 和 `AdInsightsActions` 資料表中的整理方式。Facebook 廣告只允許特定細目組合。如要進一步瞭解允許的細目組合，請參閱「[合併細分](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#combining_breakdowns)」
   * 在「Action Breakdowns」(動作細目) 部分，選取洞察資料的動作細目。這些細目決定了移轉的資料在 `AdInsightsActions` 資料表中的整理方式。如要瞭解如何合併細目，請參閱「[合併細目](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#combining_breakdowns)」。
   * 在「Refresh window」(重新整理時間範圍) 部分，指定[重新整理時間範圍](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer-intro?hl=zh-tw#refresh)的持續時間。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業名稱。
7. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 在「Repeat frequency」(重複頻率) 清單選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請點選「Email notification」(電子郵件通知) 切換按鈕。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
   * 如要針對這項資料移轉作業啟用 [Pub/Sub 移轉作業執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請點選「Pub/Sub notifications」(Pub/Sub 通知) 切換按鈕。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/publish-message-overview?hl=zh-tw#about-topics)名稱，也可以點選「Create a topic」(建立主題) 來建立主題。
9. 按一下「儲存」。

執行這項資料移轉作業時，BigQuery 資料移轉服務會自動填入下列資料表。

| 資料表名稱 | 說明 |
| --- | --- |
| `AdAccounts` | 使用者可用的廣告帳戶。 |
| `AdInsights` | 所有廣告帳戶的廣告洞察報表。 |
| `AdInsightsActions` | 所有廣告帳戶的廣告洞察動作報表。 |
| `AdInsightsMMM`  **注意：**這份報表暫時無法使用。詳情請參閱「[2026 年 7 月 6 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Jul06-fb-ads)」 | 所有廣告帳戶的廣告洞察行銷組合模式分析 (MMM) 報表。 |
| `Ads` | 所有廣告帳戶的廣告報表。 |
| `AdCreatives` | 所有廣告帳戶的廣告素材報表。 |
| `AdSets` | 所有廣告帳戶的廣告組合報表。 |
| `Campaigns` | 所有廣告帳戶的廣告活動報表。 |
| `AdImages` | 所有廣告帳戶的廣告圖片報表。 |
| `AdLabels` | 所有廣告帳戶的廣告標籤報表。 |
| `Businesses` | 與使用者相關聯的 Meta 企業帳戶。 |
| `CustomAudiences` | 所有廣告帳戶的自訂目標對象報表。 |

### bq

輸入 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)並加上移轉建立標記 `--transfer_config`：

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
  + `connector.authentication.oauth.refreshToken`：長期有效的詞元 ID。
  + `connector.authorizedAdAccountsOnly`：如果設為 `true`，連結器只會從授權給您 Facebook 應用程式的廣告帳戶擷取資料。您可以在「App Settings」(應用程式設定) >「Advanced」(進階) 的「Advanced accounts」(進階帳戶) 部分中，找到授權的廣告帳戶。
  + `connector.actionCollections`：動作集合是物件，可指定使用者對廣告採取的不同動作類型。如需 `actionCollections` 值的完整清單，請參閱「[動作集合](#action_collections)」。
    - 詳情請參閱「[廣告洞察](https://developers.facebook.com/docs/marketing-api/reference/adgroup/insights)」一文。
  + `connector.genericBreakdowns`：指定洞察資料的一般細目。這些細目會決定移轉的資料在 `AdInsights` 和 `AdInsightsActions` 資料表中的整理方式。Facebook 廣告只允許特定細目組合。如要進一步瞭解允許的細目組合，請參閱「[合併細分](#combining_breakdowns)」。
  + `actionBreakdowns`：指定洞察資料的動作細目。這些細目會決定移轉的資料在 `AdInsights` 和 `AdInsightsActions` 資料表中的整理方式。如要瞭解如何合併細目，請參閱「[合併細目](#combining_breakdowns)」。
  + `connector.insightsLevel`：擷取洞察資料的匯總層級 (例如廣告、廣告組合、廣告活動、帳戶)。
  + `connector.insightsTimeIncrement`：匯總洞察資料的分組天數 (介於 1 到 7 之間)。
  + **注意：**所選時間範圍不僅適用於洞察資料表 (`AdInsights` 和 `AdInsightsActions`)，也會使用 Facebook 的 `time_range` 參數篩選 `Ads`、`Campaigns` 和 `AdSets` 資料表。

舉例來說，下列指令會在預設專案中建立 Facebook 廣告資料移轉作業，並提供所有必要參數：

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

儲存移轉設定後，Facebook Ads 連接器會根據排程選項自動觸發移轉作業。每次執行移轉作業時，Facebook 廣告連接器都會將 Facebook 廣告中的所有可用資料移轉至 BigQuery。

如要手動執行資料轉移 (不在排程內)，可以啟動[回填作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

如要瞭解轉移的資料如何對應至 Meta API 欄位，請參閱「[Facebook 廣告報表轉換](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transformation?hl=zh-tw)」。

## 動作集合

動作集合是物件，可指定使用者對廣告採取的不同動作類型。[設定移轉設定](#fb_ads_transfer_setup)時，您可以指定動作集合。

動作集合代表
[`Ad Account, Insights` 端點回應中存在的 [`list<AdsActionStats>` 類型](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/)欄位](https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/)
。

轉移完成後，這些動作集合會填入[`AdInsightsActions`表格](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transformation?hl=zh-tw#adinsightsactions_report)。

**注意：** 為移轉作業指定的動作集合越多，就越有可能[達到 Facebook Ads 設下的頻率限制](https://developers.facebook.com/docs/marketing-api/overview/rate-limiting)。

以下列出 Facebook 廣告資料轉移作業支援的動作集合：

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
<