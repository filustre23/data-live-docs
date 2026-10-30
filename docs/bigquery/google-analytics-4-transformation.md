Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Analytics 4 報表轉換

Google Analytics 4 報表移轉至 BigQuery 時，會轉換成下列 BigQuery 資料表和檢視表。

| **GA4 報表名稱** | **BigQuery 資料表** | **BigQuery 檢視表** |
| --- | --- | --- |
| 目標對象 | p\_ga4\_Audiences | ga4\_Audiences |
| 客層詳情 | p\_ga4\_DemographicDetails | ga4\_DemographicDetails |
| 電子商務購買 | p\_ga4\_EcommercePurchases | ga4\_EcommercePurchases |
| 活動 | p\_ga4\_Events | ga4\_Events |
| 到達網頁 | p\_ga4\_LandingPage | ga4\_LandingPage |
| 網頁和畫面 | p\_ga4\_PagesAndScreens | ga4\_PagesAndScreens |
| 促銷抵免額 | p\_ga4\_Promotions | ga4\_Promotions |
| 技術詳情 | p\_ga4\_TechDetails | ga4\_TechDetails |
| 流量開發 | p\_ga4\_TrafficAcquisition | ga4\_TrafficAcquisition |
| 使用者開發 | p\_ga4\_UserAcquisition | ga4\_UserAcquisition |

## Google Analytics 報表的資料表結構定義

表格名稱：Audiences

| 欄位名稱 | 說明 |
| --- | --- |
| audienceName | 目標對象的名稱。報表會根據使用者在報表日期範圍內所屬的目標對象，將使用者歸入相應的目標對象。目前的使用者行為不會影響報表中的歷來目標對象成員。 |
| averageSessionDuration | 使用者工作階段的平均時間長度 (以秒為單位)。 |
| newUsers | 初次與網站互動或初次啟動應用程式的使用者人數 (觸發事件：first\_open 或 first\_visit)。 |
| screenPageViewsPerSession | 使用者在每個工作階段瀏覽的應用程式畫面或網頁數量。重複瀏覽同一個網頁或畫面也會列入計算。(screen\_view + page\_view 事件數量) / 工作階段數。 |
| 工作階段 | 在網站或應用程式上開始的工作階段數 (觸發事件：session\_start)。 |
| totalRevenue | 來自購買、訂閱及廣告的收益總和 (「購買收益」加上「訂閱收益」加上「廣告收益」)，減去退款交易收益。 |
| totalUsers | 記錄至少一項事件的不重複使用者人數，無論記錄事件時是否正在使用網站或應用程式。 |

資料表名稱：DemographicDetails

| 欄位名稱 | 說明 |
| --- | --- |
| brandingInterest | 購物漏斗上層使用者展現的興趣。使用者可能會歸入多個興趣類別，例如「購物者」、「生活型態與興趣/寵物愛好者」或「旅遊/旅遊愛好者/海灘旅遊愛好者」。 |
| 城市 | 使用者活動的來源城市。 |
| 國家/地區 | 使用者活動的來源國家/地區。 |
| 語言 | 使用者瀏覽器或裝置的語言設定。例如英文。 |
| 區域 | 使用者活動的來源地理區域，根據使用者的 IP 位址推算而得。 |
| userAgeBracket | 使用者年齡層。 |
| userGender | 使用者性別。 |
| activeUsers | 曾造訪網站或應用程式的不重複使用者人數。 |
| engagedSessions | 發生互動事件的工作階段數。 |
| engagementRate | 發生互動事件的工作階段百分比。 |
| eventCount | 事件數量。 |
| keyEvents | 重要事件發生次數。 |
| newUsers | 初次與網站互動或初次啟動應用程式的使用者人數 (觸發事件：first\_open 或 first\_visit)。 |
| totalRevenue | 來自購買、訂閱及廣告的收益總和 (「購買收益」加上「訂閱收益」加上「廣告收益」)，減去退款交易收益。 |
| totalUsers | 記錄至少一項事件的不重複使用者人數，無論記錄事件時是否正在使用網站或應用程式。 |
| userEngagementDuration | 網站或應用程式在使用者裝置前景運作的總時間 (以秒為單位)。 |
| userKeyEventRate | 觸發任何重要事件的使用者百分比。 |

資料表名稱：EcommercePurchases

| 欄位名稱 | 說明 |
| --- | --- |
| itemBrand | 商品品牌名稱。 |
| itemCategory | 商品所屬的階層類別。舉例來說，在「服飾/男性/夏季/上衣/T 恤」中，「服飾」是商品類別。 |
| itemCategory2 | 商品所屬的階層類別。舉例來說，在「服飾/男性/夏季/上衣/T 恤」中，「男性」是商品類別 2。 |
| itemCategory3 | 商品所屬的階層類別。舉例來說，在「服飾/男性/夏季/上衣/T 恤」中，「夏季」是商品類別 3。 |
| itemCategory4 | 商品所屬的階層類別。舉例來說，在「服飾/男性/夏季/上衣/T 恤」中，「上衣」是商品類別 4。 |
| itemCategory5 | 商品所屬的階層類別。舉例來說，在「服飾/男性/夏季/上衣/T 恤」中，「T 恤」是商品類別 5。 |
| itemId | 項目 ID。 |
| itemListPosition | 商品在清單中的位置。例如清單中銷售的產品。在標記中，這項維度會由 items 陣列中的 index 參數填入。 |
| itemName | 商品名稱。 |
| itemVariant | 產品的特定變化版本。例如 XS、S、M、L 等尺寸，或紅色、藍色、綠色、黑色等顏色。由 item\_variant 參數填入。 |
| itemsAddedToCart | 單一商品加入購物車的數量。這項指標會計算 add\_to\_cart 事件中的商品數量。 |
| itemRevenue | 購買總收益減去商品退款交易收益。商品收益是價格和數量的乘積。商品收益不含稅金和運費，這兩項費用是在事件層級指定，而非商品層級。 |
| itemsPurchased | 購買事件中單一商品的單位數。這項指標會計算購買事件中的商品數量。 |
| itemsViewed | 單一商品的瀏覽數量。這項指標會計算 view\_item 事件中的商品數量。 |

資料表名稱：Events

| 欄位名稱 | 說明 |
| --- | --- |
| eventName | 事件名稱。 |
| eventCount | 事件數量。 |
| eventCountPerUser | 每位使用者的平均事件數 (事件計數除以活躍使用者人數)。 |
| totalRevenue | 來自購買、訂閱及廣告的收益總和 (「購買收益」加上「訂閱收益」加上「廣告收益」)，減去退款交易收益。 |
| totalUsers | 記錄至少一項事件的不重複使用者人數，無論記錄事件時是否正在使用網站或應用程式。 |

資料表名稱：LandingPage

| 欄位名稱 | 說明 |
| --- | --- |
| landingPage | 與工作階段中第一次網頁瀏覽相關聯的網頁路徑。 |
| activeUsers | 曾造訪網站或應用程式的不重複使用者人數。 |
| keyEvents | 重要事件發生次數。 |
| newUsers | 初次與網站互動或初次啟動應用程式的使用者人數 (觸發事件：first\_open 或 first\_visit)。 |
| sessionKeyEventRate | 觸發任何重要事件的工作階段百分比。 |
| 工作階段 | 在網站或應用程式上開始的工作階段數 (觸發事件：session\_start)。 |
| totalRevenue | 來自購買、訂閱及廣告的收益總和 (「購買收益」加上「訂閱收益」加上「廣告收益」)，減去退款交易收益。 |
| userEngagementDurationPerSession | 單次工作階段平均參與時間 |

資料表名稱：PagesAndScreens

| 欄位名稱 | 說明 |
| --- | --- |
| contentGroup | 適用於已發布內容項目的類別。由事件參數 content\_group 填入。 |
| unifiedPagePathScreen | 記錄事件的網頁路徑 (網頁) 或畫面類別 (應用程式)。 |
| unifiedScreenClass | 記錄事件的網頁標題 (網站) 或畫面類別 (應用程式)。 |
| unifiedScreenName | 記錄事件的網頁標題 (網站) 或畫面名稱 (應用程式)。 |
| activeUsers | 曾造訪網站或應用程式的不重複使用者人數。 |
| eventCount | 事件數量。 |
| keyEvents | 重要事件發生次數。 |
| screenPageViews | 使用者瀏覽應用程式畫面或網頁的次數。重複瀏覽同一個網頁或畫面也會列入計算。(screen\_view + page\_view 事件)。 |
| screenPageViewsPerUser | 每位活躍使用者瀏覽的應用程式畫面或網頁數量。重複瀏覽同一個網頁或畫面也會列入計算。將 screen\_view 與 page\_view 事件的數量加總，然後除以活躍使用者數。 |
| totalRevenue | 來自購買、訂閱及廣告的收益總和 (「購買收益」加上「訂閱收益」加上「廣告收益」)，減去退款交易收益。 |
| userEngagementDuration | 網站或應用程式在使用者裝置前景運作的總時間 (以秒為單位)。 |

資料表名稱：Promotions

| 欄位名稱 | 說明 |
| --- | --- |
| itemPromotionCreativeName | 商品促銷廣告素材的名稱。 |
| itemPromotionId | 促銷活動 ID。 |
| itemPromotionName | 商品促銷活動的名稱。 |
| itemListPosition | 商品在清單中的位置。例如清單中銷售的產品。在標記中，這項維度會由 items 陣列中的 index 參數填入。 |
| itemsAddedToCart | 單一商品加入購物車的數量。這項指標會計算 add\_to\_cart 事件中的商品數量。 |
| itemsCheckedOut | 單一商品的結帳數量。這項指標會計算 begin\_checkout 事件中的商品數量。 |
| itemPromotionClickThroughRate | 選取促銷活動的使用者人數除以曾瀏覽同一促銷活動的使用者人數。這項指標會以小數形式傳回；舉例來說，0.1382 代表 13.82% 的使用者在瀏覽促銷活動後，也選取了該促銷活動。 |
| itemRevenue | 購買總收益，扣除商品退款交易收益。商品收益是價格和數量的乘積。商品收益不含稅金和運費，這兩項費用是在事件層級指定，而非商品層級。 |
| itemsClickedInPromotion | 單一商品在促銷活動中獲得的點擊次數。這項指標會計算 select\_promotion 事件中的商品數量。 |
| itemsPurchased | 購買事件中單一商品的單位數。這項指標會計算購買事件中的商品數量。 |
| itemsViewedInPromotion | 單一商品在促銷活動中獲得的瀏覽次數。這項指標會計算 view\_promotion 事件中的商品數量。 |

資料表名稱：TechDetails

| 欄位名稱 | 說明 |
| --- | --- |
| appVersion | 應用程式的 versionName (Android) 或簡短版軟體包版本編號 (iOS)。 |
| browser | 用來瀏覽網站的瀏覽器。 |
| deviceCategory | 裝置類型：桌機、平板電腦或行動裝置。 |
| operatingSystem | 應用程式或網站訪客使用的作業系統。包括電腦和行動作業系統，例如 Windows 和 Android。 |
| operatingSystemVersion | 網站或應用程式訪客使用的作業系統版本。舉例來說，Android 10 的版本是 10，iOS 13.5.1 的版本是 13.5.1。 |
| operatingSystemWithVersion | 作業系統和版本。例如 Android 10 或 Windows 7。 |
| platform | 應用程式或網站的運作平台，例如網站、iOS 或 Android。如要在報表中判斷串流類型，請同時使用 platform 和 streamId。 |
| platformDeviceCategory | 網站或行動應用程式的運作平台和裝置類型。(例如：Android/行動裝置) |
| screenResolution | 使用者螢幕的解析度。例如 1920x1080。 |
| activeUsers | 曾造訪網站或應用程式的不重複使用者人數。 |
| engagedSessions | 持續超過 10 秒、曾發生重要事件，或有至少 2 次畫面瀏覽的工作階段數。 |
| engagementRate | 互動工作階段的百分比 (互動工作階段除以工作階段)。這項指標會以小數形式傳回；舉例來說，0.7239 代表 72.39% 的工作階段是互動工作階段。 |
| eventCount | 事件數量。 |
| keyEvents | 重要事件發生次數。 |
| newUsers | 初次與網站互動或初次啟動應用程式的使用者人數 (觸發事件：first\_open 或 first\_visit)。 |
| totalRevenue | 來自購買、訂閱及廣告的收益總和 (「購買收益」加上「訂閱收益」加上「廣告收益」)，減去退款交易收益。 |
| userEngagementDuration | 網站或應用程式在使用者裝置前景運作的總時間 (以秒為單位)。 |

資料表名稱：TrafficAcquisition

| 欄位名稱 | 說明 |
| --- | --- |
| sessionCampaignName | 工作階段的行銷廣告活動名稱。包括 Google Ads 廣告活動、手動廣告活動和其他廣告活動。 |
| sessionDefaultChannelGroup | 工作階段的預設管道群組主要取決於來源和媒介，列舉，包括「直接」、「自然搜尋」、「付費社群活動」、「自然社群活動」、「電子郵件」、「聯盟」、「參照連結網址」、「付費搜尋」、「影片」和「多媒體」。 |
| sessionMedium | 在網站或應用程式上啟動工作階段的媒介。 |
| sessionPrimaryChannelGroup | 促成工作階段的主要管道群組。主要管道群組是 Google Analytics 標準報表使用的管道群組，也是資源資料的有效記錄，會持續與管道分組資料保持一致。 |
| sessionSource | 在網站或應用程式上啟動工作階段的來源。 |
| sessionSourceMedium | 維度 sessionSource 和 sessionMedium 的合併值。 |
| sessionSourcePlatform | 工作階段廣告活動的來源平台。請勿依賴這個欄位傳回使用 Urchin 流量監視器 (UTM) 的流量「手動」值；這個欄位將在近期推出的功能中，從傳回「手動」值更新為傳回「(not set)」值。 |
| eventCount | 事件數量。 |
| eventsPerSession | 每個工作階段的平均事件數 (事件計數除以工作階段數)。 |
| engagementRate | 互動工作階段的百分比 (互動工作階段除以工作階段)。這項指標會以小數形式傳回；舉例來說，0.7239 代表 72.39% 的工作階段是互動工作階段。 |
| engagedSessions | 持續超過 10 秒、曾發生重要事件，或有至少 2 次畫面瀏覽的工作階段數。 |
| keyEvents | 重要事件發生次數。 |
| 工作階段 | 在網站或應用程式上開始的工作階段數 (觸發事件：session\_start)。 |
| sessionKeyEventRate | 觸發任何重要事件的工作階段百分比。 |
| totalRevenue | 來自購買、訂閱及廣告的收益總和 (「購買收益」加上「訂閱收益」加上「廣告收益」)，減去退款交易收益。 |
| userEngagementDurationPerSession | 單次工作階段平均參與時間 |

資料表名稱：UserAcquisition

| 欄位名稱 | 說明 |
| --- | --- |
| firstUserCampaignName | 初次招攬到使用者的行銷廣告活動名稱；包括 Google Ads 廣告活動、手動廣告活動和其他廣告活動。 |
| firstUserDefaultChannelGroup | 最初招攬到使用者的預設管道群組。預設管道群組主要取決於來源和媒介，列舉，包括「直接」、「自然搜尋」、「付費社群活動」、「自然社群活動」、「電子郵件」、「聯盟」、「參照連結網址」、「付費搜尋」、「影片」和「多媒體」。 |
| firstUserMedium | 最初將使用者帶往網站或應用程式的媒介。 |
| firstUserPrimaryChannelGroup | 最初招攬到使用者的主要管道群組。主要管道群組是 Google Analytics 標準報表使用的管道群組，也是資源資料的有效記錄，會持續與管道分組資料保持一致。 |
| firstUserSource | 最初將使用者帶往網站或應用程式的來源。 |
| firstUserSourceMedium | 維度 firstUserSource 和 firstUserMedium 的合併值。 |
| firstUserSourcePlatform | 初次招攬到使用者的來源平台。請勿依賴這個欄位傳回使用 Urchin 流量監視器 (UTM) 的流量「手動」值；這個欄位將在近期推出的功能中，從傳回「手動」值更新為傳回「(not set)」值。 |
| activeUsers | 曾造訪網站或應用程式的不重複使用者人數。 |
| engagedSessions | 持續超過 10 秒、曾發生重要事件，或有至少 2 次畫面瀏覽的工作階段數。 |
| eventCount | 事件數量。 |
| keyEvents | 重要事件發生次數。 |
| newUsers | 初次與網站互動或初次啟動應用程式的使用者人數 (觸發事件：first\_open 或 first\_visit)。 |
| totalRevenue | 來自購買、訂閱及廣告的收益總和 (「購買收益」加上「訂閱收益」加上「廣告收益」)，減去退款交易收益。 |
| totalUsers | 記錄至少一項事件的不重複使用者人數，無論記錄事件時是否正在使用網站或應用程式。 |
| userEngagementDuration | 網站或應用程式在使用者裝置前景運作的總時間 (以秒為單位)。 |
| userKeyEventRate | 觸發任何重要事件的使用者百分比。 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-28 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-28 (世界標準時間)。"],[],[]]