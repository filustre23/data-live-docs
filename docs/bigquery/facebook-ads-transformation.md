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
| `age` | 年齡 | *Double* | 廣告帳戶的開立天數。 |
| `amount_spent` | AmountSpent | *整數* | 帳戶目前的支出總金額。這項設定可以重設。 |
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
| `name` | 名稱 | *字串* | 帳戶名稱；請注意，許多帳戶沒有名稱，因此這個欄位可能會空白。 |
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
| `action_attribution_windows` | ActionAttributionWindows | *字串* | 以半形逗號分隔的清單，用於決定動作的歸屬期。舉例來說，28d\_click 表示 API 會傳回使用者點按廣告後 28 天內發生的所有動作。這個選項設為 [1d\_view,28d\_click]。 |
| `account_id` | AdAccountId | *字串* | 與報表列相關聯的廣告帳戶 ID。 |
| `account_name` | AdAccountName | *字串* | 與報表列相關聯的廣告帳戶名稱。 |
| `campaign_id` | CampaignId | *字串* | 與報表列相關聯的廣告活動 ID。 |
| `campaign_name` | CampaignName | *字串* | 與報表列相關聯的廣告活動名稱。 |
| `adset_id` | AdSetId | *字串* | 與報表列相關聯的廣告組合 ID。 |
| `adset_name` | AdSetName | *字串* | 與報表列相關聯的廣告組合名稱。 |
| `ad_id` | AdId | *字串* | 與報表列相關聯的廣告 ID。 |
| `ad_name` | AdName | *字串* | 與報表列相關聯的廣告名稱。 |
| `buying_type` | BuyingType | *字串* | 廣告活動中目標廣告的付費方式。 |
| `clicks` | 點擊次數 | *長* | 廣告獲得的總點擊次數。視宣傳內容而定，這類互動可能包括按讚、活動回應或應用程式安裝次數。在 Facebook 使用者介面中，這是「點擊次數 (全部)」欄位。 |
| `conversion_rate_ranking` | ConversionRateRanking | *字串* | 轉換率排名。 |
| `cost_per_estimated_ad_recallers` | CostPerEstimatedAdRecallers | *十進位* | 我們預估，如果詢問使用者是否在 2 天內看過您的廣告，平均每增加一位記得看過廣告的使用者，您需要支付的費用。 |
| `cost_per_inline_link_click` | CostPerInlineLinkClick | *十進位* | 廣告中連結的平均單次點擊出價。 |
| `cost_per_inline_post_engagement` | CostPerInlinePostEngagement | *十進位* | 貼文的平均單次參與出價。 |
| `cost_per_unique_click` | CostPerUniqueClick | *十進位* | 這些廣告的單次不重複點擊平均費用，計算方式為支出金額除以獲得的不重複點擊次數。 |
| `cost_per_unique_inline_link_click` | CostPerUniqueInlineLinkClick | *十進位* | 您為每次不重複的內嵌連結點擊支付的平均費用。 |
| `cpc` | 單次點擊出價 | *十進位* | 這些廣告的平均單次點擊出價，計算方式為支出金額除以獲得的點擊次數。 |
| `cpm` | 千次曝光出價 | *十進位* | 您為廣告每獲得 1,000 次曝光所支付的平均費用。 |
| `cpp` | 單次通話成本 | *十進位* | 您為廣告向 1,000 位不重複使用者放送所支付的平均費用。 |
| `ctr` | 點閱率 | *Double* | 獲得的點擊次數除以曝光次數。在 Facebook 使用者介面中，這是「點閱率 (全部)」% 欄位。 |
| `estimated_ad_recall_rate` | EstimatedAdRecallRate | *Double* | 預估記得廣告的人數除以廣告觸及人數。 |
| `estimated_ad_recallers` | EstimatedAdRecallers | *Double* | 我們預估在 2 天內詢問時，會記得看過您廣告的人數。 |
| `frequency` | 頻率 | *Double* | 每位使用者看到廣告的平均次數。 |
| `impressions` | 曝光次數 | *長* | 廣告放送次數。在行動應用程式中，廣告首次顯示時，系統就會將其計為已放送。在所有其他 Facebook 介面中，廣告會在首次出現在使用者的動態消息時放送，或每次出現在右欄時放送。 |
| `inline_link_clicks` | InlineLinkClicks | *長* | 廣告中連結的總點擊次數。 |
| `inline_link_click_ctr` | InlineLinkClicksCounter | *Double* | 連結的內嵌點擊點閱率。 |
| `inline_post_engagement` | InlinePostEngagement | *長* | 貼文的參與總次數。 |
| `instant_experience_clicks_to_open` | InstantExperienceClicksToOpen | *長* | 對應至 META API 中的 instant\_experience\_clicks\_to\_open 欄位。 |
| `instant_experience_clicks_to_start` | InstantExperienceClicksToStart | *長* | 對應至 META API 中的 instant\_experience\_clicks\_to\_start 欄位。 |
| `instant_experience_outbound_clicks` | InstantExperienceOutboundClicks | *長* | 對應至 META API 中的 instant\_experience\_outbound\_clicks 欄位。 |
| `objective` | 目標 | *字串* | 您為廣告活動選取的目標。目標反映您希望透過廣告達成的目標。 |
| `quality_ranking` | QualityRanking | *字串* | 品質排名。 |
| `reach` | 觸及率 | *長* | 廣告的放送對象人數。 |
| `spend` | 支出 | *十進位* | 到目前為止的支出總額。 |
|  | UniqueClicks | *長* | 點擊廣告的不重複使用者總數。舉例來說，如果 3 位使用者點按同一則廣告 5 次，系統會計為 3 次不重複點擊。 |
|  | UniqueCTR | *Double* | 點按廣告的人數除以觸及人數。舉例來說，如果您獲得 20 次不重複點擊，且廣告向 1,000 位不重複使用者放送，則不重複點閱率為 2%。 |
| `inline_link_clicks` | UniqueInlineLinkClicks | *長* | 廣告獲得的不重複內嵌連結點擊次數。在 Facebook 使用者介面中，這是「不重複連結點擊次數」欄位。 |
|  | UniqueInlineLinkClickCounter | *Double* | 不重複內嵌連結點擊的點閱率。 |
|  | UniqueLinkClicksCounter | *Double* | 連結點擊的不重複點閱率。將點擊廣告中導向 Facebook 以外連結的人數，除以您觸及的人數。舉例來說，如果連結獲得 20 次不重複點擊，且廣告向 1,000 位不重複使用者顯示，則不重複點閱率為 2%。 |
|  | 入住 | *Int* | 歸因於廣告的入住次數。 |
|  | EventResponses | *Int* | 歸因於廣告的事件回應數量。 |
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
|  | HStatsByAdvertiserTZ | *字串* | 廣告主統計資料的計算時間範圍。 |
|  | HStatsByAudienceTZ | *字串* | 目標對象的統計資料所涵蓋的時間範圍。 |
|  | ImpressionDevice | *字串* | 用來觀看廣告的裝置。 |
|  | PlatformPosition | *字串* | 平台上的位置。 |
|  | PublisherPlatform | *字串* | 廣告發布平台。 |
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
| `action_attribution_windows` | ActionAttributionWindows | *字串* | 以半形逗號分隔的清單，用於決定動作的歸屬期。舉例來說，28d\_click 表示 API 會傳回使用者點按廣告後 28 天內發生的所有動作。預設選項為 [1d\_view,7d\_click]。可能的值包括 1d\_view、7d\_view、28d\_view、1d\_click、7d\_click、28d\_click、default。 |
|  | ActionCollection | *字串* | 這項資訊來自您在轉移期間選擇的動作集合。 |
| `account_id` | AdAccountId | *字串* | 與報表列相關聯的廣告帳戶 ID。 |
| `account_name` | AdAccountName | *字串* | 與報表列相關聯的廣告帳戶名稱。 |
| `campaign_id` | CampaignId | *字串* | 與報表列相關聯的廣告活動 ID。 |
| `campaign_name` | CampaignName | *字串* | 與報表列相關聯的廣告活動名稱。 |
| `adset_id` | AdSetId | *字串* | 與報表列相關聯的廣告組合 ID。 |
| `adset_name` | AdSetName | *字串* | 與報表列相關聯的廣告組合名稱。 |
| `ad_id` | AdId | *字串* | 與報表列相關聯的廣告 ID。 |
| `ad_name` | AdName | *字串* | 與報表列相關聯的廣告名稱。 |
| `ACTION_COLLECTION.value` | ActionValue | *整數* | 預設歸屬期的指標值。  Facebook 廣告計畫更新這個資料類型對應。詳情請參閱 [2026 年 7 月 25 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Jul25-fb-ads)。 |
| `ACTION_COLLECTION.1d_click` | Action1dClick | *字串* | 廣告獲得點擊後 1 天的歸屬期指標值。 |
| `ACTION_COLLECTION.1d_view` | Action1dView | *字串* | 廣告觀看後 1 天的歸屬期指標值。 |
| `ACTION_COLLECTION.7d_click` | Action7dClick | *字串* | 廣告獲得點擊後 7 天的歸屬期指標值。 |
| `ACTION_COLLECTION.7d_view` | Action7dView | *字串* | 廣告觀看後 7 天的歸屬期指標值。 |
| `ACTION_COLLECTION.28d_click` | Action28dClick | *字串* | 廣告獲得點擊後 28 天的歸屬期指標值。 |
| `ACTION_COLLECTION.28d_view` | Action28dView | *字串* | 觀看廣告後 28 天的歸屬期指標值。 |
| `ACTION_COLLECTION.dda` | ActionDDA | *字串* | 歸屬期的指標值，由以數據為準模式提供。 |
| **一般細目** | | | |
|  | 年齡 | *字串* | 這列指標的年齡範圍。 |
|  | 性別 | *字串* | 這列指標的性別。 |
|  | 國家/地區 | *字串* | 這個資料列中指標的國家/地區。 |
|  | 區域 | *字串* | 使用者觀看廣告的區域。 |
|  | FrequencyValue | *字串* | 觸及和頻率廣告活動中的廣告向每位使用者放送的次數。 |
|  | HStatsByAdvertiserTZ | *字串* | 廣告主統計資料的計算時間範圍。 |
|  | HStatsByAudienceTZ | *字串* | 目標對象的統計資料所涵蓋的時間範圍。 |
|  | ImpressionDevice | *字串* | 用來觀看廣告的裝置。 |
|  | PlatformPosition | *字串* | 平台上的位置。 |
|  | PublisherPlatform | *字串* | 廣告發布平台。 |
|  | ProductId | *字串* | 廣告中宣傳的產品 ID。 |
| **動作細目** | | | |
|  | ActionType | *字串* | 使用者看到廣告後採取的動作，即使他們沒有點擊廣告也算在內。 |
|  | ActionCanvasComponentName | *字串* | 畫布廣告中的元件名稱。 |
|  | ActionCarouselCardId | *字串* | 使用者看到廣告時互動的特定輪播資訊卡 ID。 |
|  | ActionCarouselCardName | *字串* | 使用者看到廣告時與之互動的特定輪播資訊卡。系統會根據廣告標題識別資訊卡。 |
|  | ActionDestination | *字串* | 使用者點按廣告後前往的到達網頁。 |
|  | ActionDevice | *字串* | 您追蹤的轉換事件發生所在的裝置。 |
|  | ActionReaction | *字串* | 廣告或加強推廣貼文的表情符號回應次數。 |
|  | ActionTargetId | *字串* | 使用者點按廣告後前往的到達網頁 ID。 |
|  | ActionVideoSound | *字串* | 使用者觀看影片廣告時的音效狀態 (開啟/關閉)。 |
|  | ActionVideoType | *字串* | 影片指標細目。 |
|  | ActionConvertedProductId | *字串* | 已轉換的產品 ID - 適用於協作廣告。 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]