Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Facebook 廣告報表轉換

本文說明[將 Facebook Ads 資料移轉至 BigQuery](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw) 時，Facebook Ads 報表的轉換方式。

## Facebook 廣告報表的表格對應

當您的 Facebook 廣告報表移轉至 BigQuery 時，報表會轉換成下列 BigQuery 資料表和檢視表。

### 「`AdAccounts`」報表

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
| `id` | ID [KEY] | *字串* | 廣告帳戶 ID。 |
|  | 目標 | *字串* | 用來取得廣告帳戶的目標。這個值為 `null`，可取得所有廣告帳戶。 |
| `account_id` | AccountId | *字串* | 直接在 Facebook 中查看廣告帳戶時的 ID。 |
| `account_status` | AccountStatus | *整數* | 帳戶狀態。1 = 有效、2 = 已停用、3 = 未結算、7 = 待審核、9 = 寬限期內、101 = 暫時無法使用、100 = 待關閉。 |
| `age` | 年齡 | *Double* | 廣告帳戶的開立時間 (以天為單位)。 |
| `amount_spent` | AmountSpent | *整數* | 帳戶目前的支出總額。這項設定可以重設。 |
| `balance` | 餘額 | *整數* | 應付帳單金額。 |
| `business_city` | BusinessCity | *字串* | 商家地址所在的城市。 |
| `business_country_code` | BusinessCountryCode | *字串* | 商家地址的國家/地區代碼。 |
| `business_name` | BusinessName | *字串* | 帳戶的商家名稱。 |
| `business_state` | BusinessState | *字串* | 公司地址的州別縮寫。 |
| `business_street` | BusinessStreet | *字串* | 帳戶的商家街道地址第一行。 |
| `business_street2` | BusinessStreet2 | *字串* | 帳戶的商家街道地址第二行。 |
| `business_zip` | BusinessZip | *字串* | 商家地址的郵遞區號。 |
| `capabilities` | 功能 | *字串* | 這個廣告帳戶可使用的功能。 |
| `created_time` | CreatedTime | *日期時間* | 帳戶建立時間。 |
| `currency` | 幣別 | *字串* | 帳戶使用的幣別，以帳戶設定中的相應值為準。 |
| `min_campaign_group_spend_cap` | MinCampaignGroupSpendCap | *字串* | 廣告活動群組的最低支出上限。 |
| `name` | 名稱 | *字串* | 帳戶名稱。請注意，許多帳戶沒有名稱，因此這個欄位可能會空白。 |
| `offsite_pixels_tos_accepted` | OffsitePixelsTosAccepted | *字串* | 指出是否已簽署站外像素服務條款合約。 |
| `owner` | OwnerId | *字串* | 廣告帳戶擁有者的 Facebook ID。 |
| `spend_cap` | SpendCap | *整數* | 這個帳戶可支出的最高金額，超過這個金額後，廣告活動就會暫停。如果值為 0，表示沒有支出上限。 |
| `timezone_id` | TimezoneId | *字串* | 時區 ID。 |
| `timezone_name` | TimezoneName | *字串* | 時區名稱。 |
| `timezone_offset_hours_utc` | TimezoneOffsetHoursUTC | *Double* | 與世界標準時間的時差。 |

### 「`AdInsights`」報表

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
|  | 目標 | *字串* | 要取得洞察資料的帳戶 ID。 |
| `date_start` | DateStart | *日期* | 擷取洞察資料的開始日期。在 Facebook 使用者介面中，這是「報表開始」欄位。 |
| `date_stop` | DateEnd | *日期* | 擷取洞察資料的結束日期。在 Facebook 使用者介面中，這是「報表結束」欄位。 |
|  | TimeIncrement | *字串* | 資料匯總的天數。這個值會設為 1。 |
|  | 等級 | *字串* | 代表結果的層級。這個值會設為 `ad`。 |
| `account_currency` | AccountCurrency | *字串* | 廣告帳戶使用的幣別。 |
| `action_attribution_windows` | ActionAttributionWindows | *字串* | 以半形逗號分隔的清單，用於決定動作的歸因回溯期。舉例來說，28d\_click 表示 API 會傳回使用者點按廣告後 28 天內發生的所有動作。這個選項設為 [1d\_view,28d\_click]。 |
| `account_id` | AdAccountId | *字串* | 與報表列相關聯的廣告帳戶 ID。 |
| `account_name` | AdAccountName | *字串* | 與報表列相關聯的廣告帳戶名稱。 |
| `campaign_id` | CampaignId | *字串* | 與報表列相關聯的廣告活動 ID。 |
| `campaign_name` | CampaignName | *字串* | 與報表列相關聯的廣告活動名稱。 |
| `adset_id` | AdSetId | *字串* | 與報表列相關聯的廣告組合 ID。 |
| `adset_name` | AdSetName | *字串* | 與報表列相關聯的廣告組合名稱。 |
| `ad_id` | AdId | *字串* | 與報表列相關聯的廣告 ID。 |
| `ad_name` | AdName | *字串* | 與報表列相關聯的廣告名稱。 |
| `buying_type` | BuyingType | *字串* | 廣告活動中指定廣告的付費方式。 |
| `clicks` | 點擊次數 | *長* | 廣告獲得的總點擊次數。視宣傳內容而定，這類互動可能包括粉絲專頁按讚、活動回應或應用程式安裝。在 Facebook 使用者介面中，這是「點擊次數 (全部)」欄位。 |
| `conversion_rate_ranking` | ConversionRateRanking | *字串* | 轉換率排名。 |
| `cost_per_estimated_ad_recallers` | CostPerEstimatedAdRecallers | *十進位* | 我們預估在 2 天內詢問時，每位額外使用者回憶起看過您廣告的平均費用。 |
| `cost_per_inline_link_click` | CostPerInlineLinkClick | *十進位* | 廣告中連結的平均單次點擊出價。 |
| `cost_per_inline_post_engagement` | CostPerInlinePostEngagement | *十進位* | 貼文的平均單次參與出價。 |
| `cost_per_unique_click` | CostPerUniqueClick | *十進位* | 這些廣告的單次不重複點擊平均費用，計算方式為支出金額除以獲得的不重複點擊次數。 |
| `cost_per_unique_inline_link_click` | CostPerUniqueInlineLinkClick | *十進位* | 您為每次不重複的內嵌連結點擊支付的平均費用。 |
| `cpc` | 單次點擊出價 | *十進位* | 這些廣告的平均單次點擊出價，計算方式為支出金額除以獲得的點擊次數。 |
| `cpm` | 千次曝光出價 | *十進位* | 您為廣告每獲得 1,000 次曝光所支付的平均費用。 |
| `cpp` | 單次通話成本 | *十進位* | 廣告每觸及 1,000 位不重複使用者，您支付的平均費用。 |
| `ctr` | 點閱率 | *Double* | 獲得的點擊次數除以曝光次數。在 Facebook 使用者介面中，這是「點閱率 (全部)」% 欄位。 |
| `estimated_ad_recall_rate` | EstimatedAdRecallRate | *Double* | 預估記得廣告的人數除以廣告觸及人數。 |
| `estimated_ad_recallers` | EstimatedAdRecallers | *Double* | 我們預估在 2 天內，會記得看過您廣告的人數。 |
| `frequency` | 頻率 | *Double* | 廣告向每位使用者放送的平均次數。 |
| `impressions` | 曝光次數 | *長* | 廣告放送次數。在行動應用程式中，廣告首次顯示時，系統就會計算為一次放送。在所有其他 Facebook 介面中，廣告會在首次顯示於使用者的動態消息時放送，或每次顯示於右欄時放送。 |
| `inline_link_clicks` | InlineLinkClicks | *長* | 廣告中連結的總點擊次數。 |
| `inline_link_click_ctr` | InlineLinkClicksCounter | *Double* | 連結的內嵌點擊點閱率。 |
| `inline_post_engagement` | InlinePostEngagement | *長* | 貼文的參與總次數。 |
| `instant_experience_clicks_to_open` | InstantExperienceClicksToOpen | *長* | 對應至 META API 中的 instant\_experience\_clicks\_to\_open 欄位。 |
| `instant_experience_clicks_to_start` | InstantExperienceClicksToStart | *長* | 對應於 META API 中的 instant\_experience\_clicks\_to\_start 欄位。 |
| `instant_experience_outbound_clicks` | InstantExperienceOutboundClicks | *長* | 對應至 META API 中的 instant\_experience\_outbound\_clicks 欄位。 |
| `objective` | 目標 | *字串* | 您為廣告活動選取的目標。目標反映您希望透過廣告達成的目標。 |
| `quality_ranking` | QualityRanking | *字串* | 品質排名。 |
| `reach` | 觸及率 | *長* | 廣告的放送對象人數。 |
| `spend` | 支出 | *十進位* | 到目前為止的總支出金額。 |
|  | UniqueClicks | *長* | 點擊廣告的不重複使用者總數。舉例來說，如果 3 位使用者點按同一則廣告 5 次，系統會計為 3 次不重複點擊。 |
|  | UniqueCTR | *Double* | 點按廣告的人數除以觸及人數。舉例來說，如果您獲得 20 次不重複點擊，且廣告放送對象為 1,000 位不重複使用者，則不重複點閱率為 2%。 |
| `inline_link_clicks` | UniqueInlineLinkClicks | *長* | 廣告獲得的不重複內嵌連結點擊次數。在 Facebook 使用者介面中，這是「不重複連結點擊次數」欄位。 |
|  | UniqueInlineLinkClickCounter | *Double* | 不重複內嵌連結點擊的點閱率。 |
|  | UniqueLinkClicksCounter | *Double* | 連結點擊的不重複點閱率。點擊廣告中導向 Facebook 以外連結的人數，除以觸及人數。舉例來說，如果連結獲得 20 次不重複點擊，且廣告向 1,000 位不重複使用者顯示，則不重複點閱率為 2%。 |
|  | 入住 | *Int* | 歸因於廣告的入住次數。 |
|  | EventResponses | *Int* | 歸因於廣告的事件回應次數。 |
| `inline_link_clicks` | LinkClicks | *Int* | 歸因於廣告的連結點擊次數。 |
|  | OfferSaves | *Int* | 歸因於廣告的收到優惠數量。 |
| `outbound_clicks` | OutboundClicks | *Int* | 歸因於廣告的出站點擊次數。 |
|  | PageEngagements | *Int* | 歸因於廣告的網頁參與度次數。 |
|  | PageLikes | *Int* | 歸因於廣告的粉絲專頁按讚次數。 |
|  | PageMentions | *Int* | 歸因於廣告的網頁提及次數。 |
|  | PagePhotoViews | *Int* | 歸因於廣告的相片瀏覽次數。 |
|  | PostComments | *Int* | 歸因於廣告的貼文留言數。 |
|  | PostEngagements | *Int* | 歸因於廣告的貼文參與次數。 |
|  | PostShares | *Int* | 歸因於廣告的貼文分享次數。 |
|  | PostReactions | *Int* | 歸因於廣告的貼文回應次數。 |
|  | PageTabViews | *Int* | 歸因於廣告的索引標籤瀏覽次數。 |
|  | 區域 | *字串* | 使用者觀看廣告的區域。這是細分欄位。 |
|  | Video3SecondViews | *Int* | 歸因於廣告的影片觀看次數。只要影片播放至少 3 秒，或播放完整部影片 (如果影片長度不到 3 秒)，就會計為一次觀看。 |
| **一般細目** | | | |
|  | 年齡 | *字串* | 這列指標的年齡範圍。 |
|  | 性別 | *字串* | 這列指標的性別。 |
|  | 國家/地區 | *字串* | 這個資料列中指標的國家/地區。 |
|  | 區域 | *字串* | 使用者觀看廣告的區域。 |
|  | FrequencyValue | *字串* | 觸及和頻率廣告活動中的廣告向每位使用者放送的次數。 |
|  | HStatsByAdvertiserTZ | *字串* | 廣告主取得統計資料的時間範圍。 |
|  | HStatsByAudienceTZ | *字串* | 目標對象的統計資料時間範圍。 |
|  | ImpressionDevice | *字串* | 用來觀看廣告的裝置。 |
|  | PlatformPosition | *字串* | 平台上的位置。 |
|  | PublisherPlatform | *字串* | 廣告發布的平台。 |
|  | ProductId | *字串* | 廣告中宣傳的產品 ID。 |

### 「`AdInsightsActions`」報表

`ACTION_COLLECTION`是指使用者對廣告採取的行動類型。如需動作集合的完整清單，請參閱「[動作集合](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw#action_collections)」。

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
|  | 目標 | *字串* | 要取得洞察資料的帳戶 ID。 |
| `date_start` | DateStart | *日期* | 要擷取洞察資料的起始日期。在 Facebook 使用者介面中，這是「報表開始」欄位。 |
| `date_stop` | DateEnd | *日期* | 要擷取洞察資料的結束日期。在 Facebook 使用者介面中，這是「報表結束」欄位。 |
|  | TimeIncrement | *字串* | 資料匯總的天數。這個值設為 1。 |
|  | 等級 | *字串* | 代表結果的層級。值是在 `ad` 設定。 |
| `action_attribution_windows` | ActionAttributionWindows | *字串* | 以半形逗號分隔的清單，用於決定動作的歸因回溯期。舉例來說，28d\_click 表示 API 會傳回使用者點按廣告後 28 天內發生的所有動作。預設選項為 [1d\_view,7d\_click]。可能的值包括 1d\_view、7d\_view、28d\_view、1d\_click、7d\_click、28d\_click、default。 |
|  | ActionCollection | *字串* | 這項資訊來自您在轉移期間選擇的動作集合。 |
| `account_id` | AdAccountId | *字串* | 與報表列相關聯的廣告帳戶 ID。 |
| `account_name` | AdAccountName | *字串* | 與報表列相關聯的廣告帳戶名稱。 |
| `campaign_id` | CampaignId | *字串* | 與報表列相關聯的廣告活動 ID。 |
| `campaign_name` | CampaignName | *字串* | 與報表列相關聯的廣告活動名稱。 |
| `adset_id` | AdSetId | *字串* | 與報表列相關聯的廣告組合 ID。 |
| `adset_name` | AdSetName | *字串* | 與報表列相關聯的廣告組合名稱。 |
| `ad_id` | AdId | *字串* | 與報表列相關聯的廣告 ID。 |
| `ad_name` | AdName | *字串* | 與報表列相關聯的廣告名稱。 |
| `ACTION_COLLECTION.value` | ActionValue | *整數* | 預設歸因期間的指標值。  Facebook 廣告計畫更新這個資料類型對應。詳情請參閱 [2026 年 7 月 25 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Jul25-fb-ads)。 |
| `ACTION_COLLECTION.1d_click` | Action1dClick | *字串* | 廣告獲得點擊後 1 天的歸因期指標值。 |
| `ACTION_COLLECTION.1d_view` | Action1dView | *字串* | 廣告觀看後 1 天的歸因回溯期指標值。 |
| `ACTION_COLLECTION.7d_click` | Action7dClick | *字串* | 歸因期為點擊廣告後 7 天的指標值。 |
| `ACTION_COLLECTION.7d_view` | Action7dView | *字串* | 廣告觀看後 7 天的歸因回溯期指標值。 |
| `ACTION_COLLECTION.28d_click` | Action28dClick | *字串* | 廣告獲得點擊後 28 天的歸因期指標值。 |
| `ACTION_COLLECTION.28d_view` | Action28dView | *字串* | 歸因期為觀看廣告後 28 天的指標值。 |
| `ACTION_COLLECTION.dda` | ActionDDA | *字串* | 歸因期間的指標值，由以數據為準歸因模式提供。 |
| **一般細目** | | | |
|  | 年齡 | *字串* | 這列指標的年齡範圍。 |
|  | 性別 | *字串* | 這列指標的性別。 |
|  | 國家/地區 | *字串* | 這個資料列中指標的國家/地區。 |
|  | 區域 | *字串* | 使用者觀看廣告的區域。 |
|  | FrequencyValue | *字串* | 觸及和頻率廣告活動中的廣告向每位使用者放送的次數。 |
|  | HStatsByAdvertiserTZ | *字串* | 廣告主取得統計資料的時間範圍。 |
|  | HStatsByAudienceTZ | *字串* | 目標對象的統計資料時間範圍。 |
|  | ImpressionDevice | *字串* | 用來觀看廣告的裝置。 |
|  | PlatformPosition | *字串* | 平台上的位置。 |
|  | PublisherPlatform | *字串* | 廣告發布的平台。 |
|  | ProductId | *字串* | 廣告中宣傳的產品 ID。 |
| **動作細目** | | | |
|  | ActionType | *字串* | 使用者看到廣告後，即使沒有點擊，也會對廣告採取動作。 |
|  | ActionCanvasComponentName | *字串* | 畫布廣告中的元件名稱。 |
|  | ActionCarouselCardId | *字串* | 使用者看到廣告時互動的特定輪播資訊卡 ID。 |
|  | ActionCarouselCardName | *字串* | 使用者看到廣告時與之互動的特定輪播資訊卡。資訊卡會依標題分類。 |
|  | ActionDestination | *字串* | 使用者點按廣告後前往的到達網頁。 |
|  | ActionDevice | *字串* | 您追蹤的轉換事件發生所在的裝置。 |
|  | ActionReaction | *字串* | 廣告或加強推廣貼文的表情符號回應次數。 |
|  | ActionTargetId | *字串* | 使用者點按廣告後前往的到達網頁 ID。 |
|  | ActionVideoSound | *字串* | 使用者觀看影片廣告時的音效狀態 (開啟/關閉)。 |
|  | ActionVideoType | *字串* | 影片指標細目。 |
|  | ActionConvertedProductId | *字串* | 已轉換的產品 ID - 適用於協作廣告。 |

### 「`AdInsightsMMM`」報表

**注意：** 自 2026 年 7 月 6 日起，系統將暫時停用 `AdInsightsMMM` 報表。詳情請參閱 [2026 年 7 月 6 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Jul06-fb-ads)。

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
|  | 目標 | *字串* | 要取得洞察資料的帳戶 ID。 |
|  | TimeIncrement | *字串* | 資料匯總的天數。 |
| `account_id` | AccountId | *字串* | 與資料列相關聯的廣告帳戶 ID。 |
| `campaign_id` | CampaignId | *字串* | 與資料列相關聯的廣告活動 ID。 |
| `adset_id` | AdSetId | *字串* | 與資料列相關聯的廣告組合 ID。 |
| `date_start` | DateStart | *日期* | 擷取洞察資料的開始日期。 |
| `date_stop` | DateEnd | *日期* | 擷取洞察資料的結束日期。 |
| `impressions` | 曝光次數 | *長* | 廣告放送次數。 |
| `spend` | 支出 | *十進位* | 支出總金額。 |
| `country` | 國家/地區 | *字串* | 指標的國家/地區。 |
| `region` | 區域 | *字串* | 廣告的觀看區域。 |
| `dma` | DMA | *字串* | 指標的指定行銷區域。 |
| `device_platform` | DevicePlatform | *字串* | 使用的裝置平台。 |
| `platform_position` | PlatformPosition | *字串* | 平台上的位置。 |
| `publisher_platform` | PublisherPlatform | *字串* | 發布商平台。 |
| `creative_media_type` | CreativeMediaType | *字串* | 廣告素材中使用的媒體類型。 |

### 「`Ads`」報表

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
| `id` | ID | *字串* | 廣告的 ID。 |
|  | 目標 | *字串* | 用於擷取廣告的目標欄位。 |
| `name` | 名稱 | *字串* | 廣告的名稱。 |
| `status` | AdStatus | *字串* | 廣告的狀態。 |
| `bid_info` | BidInfo | *字串* | 與廣告相關聯的出價資訊。 |
| `bid_type` | BidType | *字串* | 與廣告相關聯的出價類型。 |
| `campaign_id` | CampaignId | *字串* | 廣告活動的 ID。 |
| `adset_id` | AdSetId | *字串* | 廣告組合的 ID。 |
| `creative` | AdCreativeId | *字串* | 廣告素材的 ID。 |
| `configured_status` | ConfiguredStatus | *字串* | 廣告的設定狀態。 |
| `created_time` | CreatedTime | *日期時間* | 廣告的建立時間。 |
| `updated_time` | UpdatedTime | *日期時間* | 廣告的上次更新時間。 |
| `conversion_specs` | ConversionSpecs | *字串* | 轉換規格。 |
| `failed_delivery_checks` | FailedDeliveryChecks | *字串* | 有關遞送檢查失敗的資訊。 |
| `recommendations` | 建議 | *字串* | 廣告建議。 |
| `tracking_specs` | TrackingSpecs | *JSON* | 追蹤規格。 |
| `ad_active_time` | AdActiveTime | *字串* | 有效時間參數。 |
| `ad_schedule_end_time` | AdScheduleEndTime | *日期時間* | 排定的結束時間。 |
| `ad_schedule_start_time` | AdScheduleStartTime | *日期時間* | 排定的開始時間。 |
| `bid_amount` | BidAmount | *整數* | 出價金額。 |
| `last_updated_by_app_id` | LastUpdatedByAppId | *字串* | 最後更新廣告的應用程式 ID。 |
| `preview_shareable_link` | PreviewShareableLink | *字串* | 可共用的預覽連結。 |
| `source_ad_id` | SourceAdId | *字串* | 來源廣告 ID。 |

### 「`AdCreatives`」報表

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
| `id` | ID | *字串* | 廣告素材的 ID。 |
|  | 目標 | *字串* | 目標欄位。 |
| `name` | 名稱 | *字串* | 廣告素材名稱。 |
| `applink_treatment` | ApplinkTreatment | *字串* | 廣告素材的深層連結處理方式。 |
| `body` | 內文 | *字串* | 廣告區塊的內文。 |
| `call_to_action_type` | CallToActionType | *字串* | 行動號召類型。 |
| `effective_instagram_media_id` | EffectiveInstagramMediaId | *字串* | Instagram 媒體的有效 ID。 |
| `image_hash` | ImageHash | *字串* | 相關聯圖片的雜湊值。 |
| `image_url` | ImageUrl | *字串* | 廣告素材圖片的網址。 |
| `instagram_permalink_url` | InstagramPermalinkUrl | *字串* | Instagram 永久連結。 |
| `instagram_user_id` | InstagramUserId | *字串* | Instagram 使用者 ID。 |
| `link_og_id` | LinkOgId | *字串* | 連結的 Open Graph ID。 |
| `link_url` | LinkUrl | *字串* | 到達網頁網址。 |
| `object_id` | ObjectId | *字串* | 相關聯的物件 ID。 |
| `object_story_id` | ObjectStoryId | *字串* | 物件故事 ID。 |
| `object_type` | ObjectType | *字串* | 物件的類型。 |
| `object_url` | ObjectUrl | *字串* | 物件的網址。 |
| `page_id` | PageId | *字串* | 相關聯的 Facebook 粉絲專頁 ID。 |
| `product_set_id` | ProductSetId | *字串* | 產品組合 ID。 |
| `run_status` | RunStatus | *字串* | 廣告素材的執行狀態。 |
| `source_instagram_media_id` | SourceInstagramMediaId | *字串* | 來源 Instagram 媒體 ID。 |
| `template_url` | TemplateUrl | *字串* | 範本網址。 |
| `thumbnail_url` | ThumbnailUrl | *字串* | 縮圖網址。 |
| `title` | 標題 | *字串* | 廣告素材的標題文字。 |
| `url_tags` | UrlTags | *字串* | 網址代碼參數。 |
| `adlabels` | AdLabels | *字串* | 與廣告素材相關聯的標籤。 |
| `object_story_spec.link_data` | ObjectStorySpecLinkData | *JSON* | 連結資料規格。 |
| `object_story_spec.photo_data` | ObjectStorySpecPhotoData | *JSON* | 相片資料規格。 |
| `object_story_spec.video_data` | ObjectStorySpecVideoData | *JSON* | 影片資料規格。 |
| `object_story_spec.text_data` | ObjectStorySpecTextData | *JSON* | 文字資料規格。 |
| `object_story_spec.template_data` | ObjectStorySpecTemplateData | *JSON* | 範本資料規格。 |

### 「`AdSets`」報表

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
| `id` | ID | *字串* | 廣告組合的 ID。 |
|  | 目標 | *字串* | 目標欄位。 |
| `name` | 名稱 | *字串* | 廣告組合的名稱。 |
| `budget_remaining` | BudgetRemaining | *整數* | 剩餘預算。 |
| `campaign_id` | CampaignId | *字串* | 相關聯的廣告活動 ID。 |
| `status` | AdSetStatus | *字串* | 廣告組合狀態。 |
| `billing_event` | BillingEvent | *字串* | 帳單事件條件。 |
| `created_time` | CreatedTime | *日期時間* | 廣告組合建立時間。 |
| `daily_budget` | DailyBudget | *整數* | 每日預算上限。 |
| `lifetime_budget` | LifetimeBudget | *整數* | 整個生命週期的預算上限。 |
| `end_time` | EndTime | *日期時間* | 排定的結束時間。 |
| `start_time` | StartTime | *日期時間* | 排定的開始時間。 |
| `updated_time` | UpdatedTime | *日期時間* | 上次更新廣告組合的時間。 |
| `recommendations` | 建議 | *字串* | 廣告組合的建議。 |
| `targeting.genders` | TargetingGenders | *字串* | 指定性別。 |
| `targeting.age_max` | TargetingAgeMax | *整數* | 目標年齡上限。 |
| `targeting.age_min` | TargetingAgeMin | *整數* | 目標最低年齡。 |
| `targeting.countries` | TargetingCountries | *字串* | 指定國家/地區。 |
| `targeting.location_types` | TargetingLocationTypes | *字串* | 指定地區類型。 |
| `targeting.regions` | TargetingRegions | *字串* | 目標區域或州。 |
| `targeting.cities` | TargetingCities | *字串* | 指定城市。 |
| `targeting.zips` | TargetingZips | *字串* | 指定目標郵遞區號。 |
| `targeting.custom_locations` | TargetingCustomLocations | *字串* | 指定自訂地區。 |
| `targeting.geo_markets` | TargetingGeoMarkets | *字串* | 目標地理市場。 |
| `targeting.interests` | TargetingInterests | *字串* | 指定個人興趣。 |
| `targeting.behaviors` | TargetingBehaviors | *字串* | 指定使用者行為。 |
| `targeting.device_platforms` | TargetingDevicePlatforms | *字串* | 指定平台。 |
| `targeting.publisher_platforms` | TargetingPublisherPlatforms | *字串* | 指定發布商平台。 |
| `targeting.instagram_positions` | TargetingInstagramPositions | *字串* | 指定 Instagram 刊登位置。 |
| `targeting.page_types` | TargetingPageTypes | *字串* | 目標網頁類型。 |
| `learning_stage_info.status` | LearningStageInfoStatus | *字串* | 學習階段的狀態。 |
| `learning_stage_info.conversions` | LearningStageInfoConversions | *整數* | 學習階段的轉換次數。 |
| `learning_stage_info.attribution_windows` | LearningStageInfoAttributionWindows | *字串* | 學習階段的歸屬期。 |
| `learning_stage_info.last_sig_edit_time` | LearningStageInfoLastSigEditTime | *日期時間* | 學習階段的最後一次重大編輯時間。 |

### 「`Campaigns`」報表

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
| `id` | ID | *字串* | 廣告活動的 ID。 |
|  | 目標 | *字串* | 目標欄位。 |
| `name` | 名稱 | *字串* | 廣告活動名稱。 |
| `buying_type` | BuyingType | *字串* | 購買類型。 |
| `configured_status` | ConfiguredStatus | *字串* | 設定的狀態。 |
| `effective_status` | EffectiveStatus | *字串* | 有效狀態。 |
| `status` | 狀態 | *字串* | 廣告活動的目前狀態。 |
| `created_time` | CreatedTime | *日期時間* | 建立時間。 |
| `objective` | 目標 | *字串* | 選取的廣告活動目標。 |
| `spend_cap` | SpendCap | *整數* | 生命週期支出上限。 |
| `daily_budget` | DailyBudget | *整數* | 每日預算。 |
| `budget_remaining` | BudgetRemaining | *整數* | 廣告活動的剩餘預算。 |
| `lifetime_budget` | LifetimeBudget | *整數* | 整個生命週期的預算總額。 |
| `bid_strategy` | BidStrategy | *字串* | 用於出價的策略。 |
| `start_time` | StartTime | *日期時間* | 排定的開始時間。 |
| `stop_time` | StopTime | *日期時間* | 排定的停止/結束時間。 |
| `updated_time` | UpdatedTime | *日期時間* | 上次更新時間。 |
| `boosted_object_id` | BoostedObjectId | *字串* | 任何加成物件的 ID。 |

### 「`AdImages`」報表

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
| `id` | ID | *字串* | 圖片的 ID。 |
|  | 目標 | *字串* | 目標欄位。 |
| `account_id` | AccountId | *字串* | 擁有圖片的廣告帳戶 ID。 |
| `created_time` | CreatedTime | *日期時間* | 圖片的建立時間。 |
| `hash` | hash | *字串* | 圖片內容的專屬雜湊值。 |
| `height` | 高度 | *整數* | 圖片高度 (以像素為單位)。 |
| `width` | 寬度 | *整數* | 圖片寬度 (以像素為單位)。 |
| `creatives` | AssociatedWithCreatives | *字串* | 關聯廣告素材資訊。 |
| `name` | 名稱 | *字串* | 圖片的名稱 ID。 |
| `original_height` | OriginalHeight | *整數* | 上傳時的原始高度。 |
| `original_width` | OriginalWidth | *整數* | 上傳時的原始寬度。 |
| `status` | 狀態 | *字串* | 圖片的驗證狀態。 |
| `permalink_url` | PermalinkUrl | *字串* | 指向圖片永久連結的網址。 |

### 「`AdLabels`」報表

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
| `id` | ID | *字串* | 廣告標籤的 ID。 |
|  | 目標 | *字串* | 目標欄位。 |
| `name` | 名稱 | *字串* | 標籤的顯示名稱。 |
| `created_time` | CreatedTime | *日期時間* | 標籤建立時間。 |
| `updated_time` | UpdatedTime | *日期時間* | 標籤上次更新時間。 |

### 「`Businesses`」報表

| **Meta API 欄位名稱** | **對應的 BigQuery 欄位名稱** | **類型** | **說明** |
| --- | --- | --- | --- |
| `id` | ID | *字串* | 商家 ID。 |
| `name` | 名稱 | *字* |