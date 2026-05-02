* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Campaign Manager 報表轉換

當您的 Campaign Manager (原名為 DoubleClick Campaign Manager) 資料移轉檔案移轉到 BigQuery 時，檔案會轉換成下列 BigQuery 表格和視圖。

當您在 BigQuery 中檢視資料表和視圖時，campaign\_manager\_id 的值是您的 Campaign Manager Network、廣告主或 Floodlight ID。

| **Campaign Manager 檔案** | **BigQuery 資料表** | **BigQuery 檢視區塊** |
| --- | --- | --- |
| **資料移轉檔案** |  |  |
| [曝光](https://developers.google.com/doubleclick-advertisers/dtv2/reference/file-format?hl=zh-tw) | p\_impression\_campaign\_manager\_id | impression\_campaign\_manager\_id |
| [點按](https://developers.google.com/doubleclick-advertisers/dtv2/reference/file-format?hl=zh-tw) | p\_click\_campaign\_manager\_id | click\_campaign\_manager\_id |
| [活動](https://developers.google.com/doubleclick-advertisers/dtv2/reference/file-format?hl=zh-tw) | p\_activity\_campaign\_manager\_id | activity\_campaign\_manager\_id |
| [rich\_media](https://developers.google.com/doubleclick-advertisers/dtv2/reference/file-format?hl=zh-tw) | p\_rich\_media\_campaign\_manager\_id | rich\_media\_campaign\_manager\_id |
| **比對表格** |  |  |
| [activity\_cats](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#activity_cats) | p\_match\_table\_activity\_cats\_campaign\_manager\_id | match\_table\_activity\_cats\_campaign\_manager\_id |
| [activity\_types](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#activity_types) | p\_match\_table\_activity\_types\_campaign\_manager\_id | match\_table\_activity\_types\_campaign\_manager\_id |
| [ads](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#ads) | p\_match\_table\_ads\_campaign\_manager\_id | match\_table\_ads\_campaign\_manager\_id |
| [ad\_placement\_assignments](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#ad_placement_assignments) | p\_match\_table\_ad\_placement\_assignments\_campaign\_manager\_id | match\_table\_ad\_placement\_assignments\_campaign\_manager\_id |
| [廣告主](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#advertisers) | p\_match\_table\_advertisers\_campaign\_manager\_id | match\_table\_advertisers\_campaign\_manager\_id |
| [assets](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#assets) | p\_match\_table\_assets\_campaign\_manager\_id | match\_table\_assets\_campaign\_manager\_id |
| [瀏覽器](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#browsers) | p\_match\_table\_browsers\_campaign\_manager\_id | match\_table\_browsers\_campaign\_manager\_id |
| [廣告活動](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#campaigns) | p\_match\_table\_campaigns\_campaign\_manager\_id | match\_table\_campaigns\_campaign\_manager\_id |
| [城市](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#cities) | p\_match\_table\_cities\_campaign\_manager\_id | match\_table\_cities\_campaign\_manager\_id |
| [廣告素材](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#creatives) | p\_match\_table\_creatives\_campaign\_manager\_id | match\_table\_creatives\_campaign\_manager\_id |
| [creative\_ad\_assignments](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#creative_ad_assignments) | p\_match\_table\_creative\_ad\_assignments\_campaign\_manager\_id | match\_table\_creative\_ad\_assignments\_campaign\_manager\_id |
| [custom\_creative\_fields](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#custom_creative_fields) | p\_match\_table\_custom\_creative\_fields\_campaign\_manager\_id | match\_table\_custom\_creative\_fields\_campaign\_manager\_id |
| [paid\_search](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#paid_search) | p\_match\_table\_paid\_search\_campaign\_manager\_id | match\_table\_paid\_search\_campaign\_manager\_id |
| [designated\_market\_areas](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#designated_market_areas) | p\_match\_table\_designated\_market\_areas\_campaign\_manager\_id | match\_table\_designated\_market\_areas\_campaign\_manager\_id |
| [keyword\_value](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#keyword_value) | p\_match\_table\_keyword\_value\_campaign\_manager\_id | match\_table\_keyword\_value\_campaign\_manager\_id |
| null 使用者 ID 原因類別 | 不支援 | 不支援 |
| 互動式多媒體標準事件和事件類型 ID | 不支援 | 不支援 |
| [custom\_rich\_media](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#custom_rich_media) | p\_match\_table\_custom\_rich\_media\_campaign\_manager\_id | match\_table\_custom\_rich\_media\_campaign\_manager\_id |
| [operating\_systems](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#operating_systems) | p\_match\_table\_operating\_systems\_campaign\_manager\_id | match\_table\_operating\_systems\_campaign\_manager\_id |
| [刊登位置](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#placements) | p\_match\_table\_placements\_campaign\_manager\_id | match\_table\_placements\_campaign\_manager\_id |
| [placement\_cost](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#placement_cost) | p\_match\_table\_placement\_cost\_campaign\_manager\_id | match\_table\_placement\_cost\_campaign\_manager\_id |
| [協作平台](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#sites) | p\_match\_table\_sites\_campaign\_manager\_id | match\_table\_sites\_campaign\_manager\_id |
| [狀態](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#states) | p\_match\_table\_states\_campaign\_manager\_id | match\_table\_states\_campaign\_manager\_id |
| [custom\_floodlight\_variables](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#custom_floodlight_variables) | p\_match\_table\_custom\_floodlight\_variables\_campaign\_manager\_id | match\_table\_custom\_floodlight\_variables\_campaign\_manager\_id |
| [landing\_page\_url](https://developers.google.com/doubleclick-advertisers/dtv2/reference/match-tables?hl=zh-tw#landing_page_url) | p\_match\_table\_landing\_page\_url\_campaign\_manager\_id | match\_table\_landing\_page\_url\_campaign\_manager\_id |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]