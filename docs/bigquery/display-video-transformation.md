Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Display & Video 360 資料轉換

將 Display & Video 360 資料移轉至 BigQuery 時，系統會將資料轉換成下列 BigQuery 表格和檢視表。

當您在 BigQuery 中檢視資料表和檢視表時，displayvideo\_id 的值即為您的 Display & Video 360 合作夥伴或廣告客戶 ID。

| **Display & Video 360 資源** | **BigQuery 資料表** | **BigQuery 檢視表** |
| --- | --- | --- |
| **資料移轉檔案** | | |
| [曝光](https://developers.google.com/bid-manager/dtv2/reference/file-format?hl=zh-tw) | p\_Impression\_displayvideo\_id | Impression\_displayvideo\_id |
| [點擊](https://developers.google.com/bid-manager/dtv2/reference/file-format?hl=zh-tw) | p\_Click\_displayvideo\_id | Click\_displayvideo\_id |
| [活動](https://developers.google.com/bid-manager/dtv2/reference/file-format?hl=zh-tw) | p\_Activity\_displayvideo\_id | Activity\_displayvideo\_id |
| **DV360 API 資源 (v3)** | | |
| [合作夥伴](https://developers.google.com/display-video/api/reference/rest/v3/partners?hl=zh-tw#resource:-partner) | p\_Partner\_displayvideo\_id | Partner\_displayvideo\_id |
| [廣告主](https://developers.google.com/display-video/api/reference/rest/v3/advertisers?hl=zh-tw#resource:-advertiser) | p\_Advertiser\_displayvideo\_id | Advertiser\_displayvideo\_id |
| [LineItem](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.lineItems?hl=zh-tw#LineItem) | p\_LineItem\_displayvideo\_id | LineItem\_displayvideo\_id |
| [LineItemTargeting](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.lineItems/bulkListAssignedTargetingOptions?hl=zh-tw#LineItemAssignedTargetingOption) | p\_LineItemTargeting\_displayvideo\_id | LineItemTargeting\_displayvideo\_id |
| [Campaign](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.campaigns?hl=zh-tw#Campaign) | p\_Campaign\_displayvideo\_id | Campaign\_displayvideo\_id |
| [CampaignTargeting](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.campaigns.targetingTypes.assignedTargetingOptions?hl=zh-tw#AssignedTargetingOption) | p\_CampaignTargeting\_displayvideo\_id | CampaignTargeting\_displayvideo\_id |
| [InsertionOrder](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.insertionOrders?hl=zh-tw#InsertionOrder) | p\_InsertionOrder\_displayvideo\_id | InsertionOrder\_displayvideo\_id |
| [InsertionOrderTargeting](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.insertionOrders.targetingTypes.assignedTargetingOptions?hl=zh-tw#AssignedTargetingOption) | p\_InsertionOrderTargeting\_displayvideo\_id | InsertionOrderTargeting\_displayvideo\_id |
| [AdGroup](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.adGroups?hl=zh-tw#AdGroup) | p\_AdGroup\_displayvideo\_id | AdGroup\_displayvideo\_id |
| [AdGroupTargeting](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.adGroups/bulkListAdGroupAssignedTargetingOptions?hl=zh-tw#AdGroupAssignedTargetingOption) | p\_AdGroupTargeting\_displayvideo\_id | AdGroupTargeting\_displayvideo\_id |
| [AdGroupAd](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.adGroupAds?hl=zh-tw#AdGroupAd) | p\_AdGroupAd\_displayvideo\_id | AdGroupAd\_displayvideo\_id |
| [廣告素材](https://developers.google.com/display-video/api/reference/rest/v3/advertisers.creatives?hl=zh-tw#resource:-creative) | p\_Creative\_displayvideo\_id | Creative\_displayvideo\_id |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]