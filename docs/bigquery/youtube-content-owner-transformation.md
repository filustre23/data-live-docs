Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# YouTube 內容擁有者報表轉換

當您的 YouTube 內容擁有者或系統管理報表移轉至 BigQuery 時，報表會轉換成下列 BigQuery 資料表和檢視表。

當您在 BigQuery 中查看資料表和檢視表時，suffix 的值是您在建立移轉時設定的資料表尾碼。

| **YouTube 內容擁有者報告** | **BigQuery 資料表** | **BigQuery 檢視區塊** |
| --- | --- | --- |
| **影片報表** |  |  |
| [使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-user-activity) | p\_content\_owner\_basic\_a4\_suffix | content\_owner\_basic\_a4\_suffix |
| [依省份劃分的使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-province) | p\_content\_owner\_province\_a3\_suffix | content\_owner\_province\_3\_suffix |
| [播放位置](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-playback-locations) | p\_content\_owner\_playback\_location\_a3\_suffix | content\_owner\_playback\_location\_a3\_suffix |
| [流量來源](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-traffic-sources) | p\_content\_owner\_traffic\_source\_a3\_suffix | content\_owner\_traffic\_source\_a3\_suffix |
| [裝置類型和作業系統](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-device-type-and-operating-system) | p\_content\_owner\_device\_os\_a3\_suffix | content\_owner\_device\_os\_a3\_suffix |
| [觀眾客層](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-viewer-demographics) | p\_content\_owner\_demographics\_a1\_suffix | content\_owner\_demographics\_a1\_suffix |
| [內容共享 (依平台分組)](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-content-sharing) | p\_content\_owner\_sharing\_service\_a1\_suffix | content\_owner\_sharing\_service\_a1\_suffix |
| [註解](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-annotations) | p\_content\_owner\_annotations\_a1\_suffix | content\_owner\_annotations\_a1\_suffix |
| [資訊卡](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-cards) | p\_content\_owner\_cards\_a1\_suffix | content\_owner\_cards\_a1\_suffix |
| [片尾](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-end-screens) | p\_content\_owner\_end\_screens\_a1\_suffix | content\_owner\_end\_screens\_a1\_suffix |
| [字幕](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-subtitles) | p\_content\_owner\_subtitles\_a3\_suffix | content\_owner\_subtitles\_a3\_suffix |
| [合併](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-combined) | p\_content\_owner\_combined\_a3\_suffix | content\_owner\_combined\_a3\_suffix |
| **播放清單報表** |  |  |
| [使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-user-activity) | p\_content\_owner\_playlist\_basic\_a2\_suffix | content\_owner\_playlist\_basic\_a2\_suffix |
| [依省份劃分的使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-province) | p\_content\_owner\_playlist\_province\_a2\_suffix | content\_owner\_playlist\_province\_a2\_suffix |
| [播放位置](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-playback-locations) | p\_content\_owner\_playlist\_playback\_location\_a2\_suffix | content\_owner\_playlist\_playback\_location\_a2 |
| [流量來源](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-traffic-sources) | p\_content\_owner\_playlist\_traffic\_source\_a2 | content\_owner\_playlist\_traffic\_source\_a2\_suffix |
| [裝置類型和作業系統](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-device-type-and-operating-system) | p\_content\_owner\_playlist\_device\_os\_a2\_suffix | content\_owner\_playlist\_device\_os\_a2\_suffix |
| [合併](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-combined) | p\_content\_owner\_playlist\_combined\_a2\_suffix | content\_owner\_playlist\_combined\_a2\_suffix |
| **廣告費率報表** |  |  |
| [廣告費率報表](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#ad-rate-reports) | p\_content\_owner\_ad\_rates\_a1\_suffix | content\_owner\_ad\_rates\_a1\_suffix |
| **預估收益報表** |  |  |
| [預估影片收益](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#estimated-revenue-videos) | p\_content\_owner\_estimated\_revenue\_a1\_suffix | content\_owner\_estimated\_revenue\_a1\_suffix |
| [預估資產收益](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#estimated-revenue-assets) | p\_content\_owner\_asset\_estimated\_revenue\_a1\_suffix | content\_owner\_asset\_estimated\_revenue\_a1\_suffix |
| **素材資源報表** |  |  |
| [使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-user-activity) | p\_content\_owner\_asset\_basic\_a3\_suffix | content\_owner\_asset\_basic\_a3\_suffix |
| [依省份劃分的使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-province) | p\_content\_owner\_asset\_province\_a3\_suffix | content\_owner\_asset\_province\_a3\_suffix |
| [影片播放位置](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-playback-locations) | p\_content\_owner\_asset\_playback\_location\_a3\_suffix | content\_owner\_asset\_playback\_location\_a3\_suffix |
| [流量來源](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-traffic-sources) | p\_content\_owner\_asset\_traffic\_source\_a3\_suffix | content\_owner\_asset\_traffic\_source\_a3\_suffix |
| [裝置類型和作業系統](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-device-type-and-operating-system) | p\_content\_owner\_asset\_device\_os\_a3\_suffix | content\_owner\_asset\_device\_os\_a3\_suffix |
| [觀眾客層](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-viewer-demographics) | p\_content\_owner\_asset\_demographics\_a1\_suffix | content\_owner\_asset\_demographics\_a1\_suffix |
| [內容共享 (依平台分組)](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-content-sharing) | p\_content\_owner\_asset\_sharing\_service\_a1\_suffix | content\_owner\_asset\_sharing\_service\_a1\_suffix |
| [註解](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-annotations) | p\_content\_owner\_asset\_annotations\_a1\_suffix | content\_owner\_asset\_annotations\_a1\_suffix |
| [資訊卡](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-cards) | p\_content\_owner\_asset\_cards\_a1\_suffix | content\_owner\_asset\_cards\_a1\_suffix |
| [片尾](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-end-screens) | p\_content\_owner\_asset\_end\_screens\_a1\_suffix | content\_owner\_asset\_end\_screens\_a1\_suffix |
| [合併](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-combined) | p\_content\_owner\_asset\_combined\_a3\_suffix | content\_owner\_asset\_combined\_a3\_suffix |
| **觸及報表** |  |  |
| [觸及基本](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#reach-reports) | p\_content\_owner\_reach\_basic\_a1\_suffix | content\_owner\_reach\_basic\_a1\_suffix |
| [合併觸及](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#reach-reports) | p\_content\_owner\_reach\_combined\_a1\_suffix | content\_owner\_reach\_combined\_a1\_suffix |

| **YouTube 系統管理報表** | **BigQuery 資料表** | **BigQuery 檢視區塊** |
| --- | --- | --- |
| **財務摘要報表** |  |  |
| [每月付款摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/financial-summaries?hl=zh-tw#monthly-payments-summary) | p\_content\_owner\_payments\_summary\_a1\_suffix | content\_owner\_payments\_summary\_a1\_suffix |
| **廣告收益報表** |  |  |
| [每月全球廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-global-ad-revenue-summary) | p\_content\_owner\_global\_ad\_revenue\_summary\_a1\_suffix | content\_owner\_global\_ad\_revenue\_summary\_a1\_suffix |
| [每月國家/地區廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-country-ad-revenue-summary) | p\_content\_owner\_country\_ad\_revenue\_summary\_a1\_suffix | content\_owner\_country\_ad\_revenue\_summary\_a1\_suffix |
| [每月每日廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-day-ad-revenue-summary) | p\_content\_owner\_day\_ad\_revenue\_summary\_a1\_suffix | content\_owner\_day\_ad\_revenue\_summary\_a1\_suffix |
| [每週全球廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-global-ad-revenue-summary) | p\_content\_owner\_global\_ad\_revenue\_summary\_weekly\_a1\_suffix | content\_owner\_global\_ad\_revenue\_summary\_weekly\_a1\_suffix |
| [每週國家/地區廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-country-ad-revenue-summary) | p\_content\_owner\_country\_ad\_revenue\_summary\_weekly\_a1\_suffix | content\_owner\_country\_ad\_revenue\_summary\_weekly\_a1\_suffix |
| [每週每日廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-day-ad-revenue-summary) | p\_content\_owner\_day\_ad\_revenue\_summary\_weekly\_a1\_suffix | content\_owner\_day\_ad\_revenue\_summary\_weekly\_a1\_suffix |
| [每部影片的匯總廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#aggregate-ad-revenue-per-video) | p\_content\_owner\_ad\_revenue\_summary\_a1\_suffix | content\_owner\_ad\_revenue\_summary\_a1\_suffix |
| [每週影片廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-video-ad-revenue-summary) | p\_content\_owner\_ad\_revenue\_summary\_weekly\_a1\_suffix | content\_owner\_ad\_revenue\_summary\_weekly\_a1\_suffix |
| [每週影片廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-video-ad-revenue) | p\_content\_owner\_ad\_revenue\_raw\_weekly\_a1\_suffix | content\_owner\_ad\_revenue\_raw\_weekly\_a1\_suffix |
| [每部影片的每日廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#daily-ad-revenue-per-video) | p\_content\_owner\_ad\_revenue\_raw\_a1\_suffix | content\_owner\_ad\_revenue\_raw\_a1\_suffix |
| [每項資產的廣告收益總額](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#aggregate-ad-revenue-per-asset) | p\_content\_owner\_asset\_ad\_revenue\_summary\_a1\_suffix | content\_owner\_asset\_ad\_revenue\_summary\_a1\_suffix |
| [每日每項資產的廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#daily-ad-revenue-per-asset) | p\_content\_owner\_asset\_ad\_revenue\_raw\_a1\_suffix | content\_owner\_asset\_ad\_revenue\_raw\_a1\_suffix |
| [每月聲明廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-claim-ad-revenue-summary) | p\_content\_owner\_claim\_ad\_revenue\_summary\_a1\_suffix | content\_owner\_claim\_ad\_revenue\_summary\_a1\_suffix |
| [每週著作權聲明廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-claim-ad-revenue-summary) | p\_content\_owner\_claim\_ad\_revenue\_summary\_weekly\_a1\_suffix | content\_owner\_claim\_ad\_revenue\_summary\_weekly\_a1\_suffix |
| [每月聲明廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-claim-ad-revenue) | p\_content\_owner\_claim\_ad\_revenue\_raw\_a1\_suffix | content\_owner\_claim\_ad\_revenue\_raw\_a1\_suffix |
| [每週聲明廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-claim-ad-revenue) | p\_content\_owner\_claim\_ad\_revenue\_raw\_weekly\_a1\_suffix | content\_owner\_claim\_ad\_revenue\_raw\_weekly\_a1\_suffix |
| [每月全球廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-global-ad-adjustment-revenue-summary) | p\_content\_owner\_global\_ad\_adjustment\_revenue\_summary\_a1\_suffix | content\_owner\_global\_ad\_adjustment\_revenue\_summary\_a1\_suffix |
| [每月素材資源廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-asset-ad-adjustment-revenue-summary) | p\_content\_owner\_asset\_ad\_adjustment\_revenue\_summary\_a1\_suffix | content\_owner\_asset\_ad\_adjustment\_revenue\_summary\_a1\_suffix |
| [每月素材資源廣告調整項收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-asset-ad-adjustment-revenue) | p\_content\_owner\_asset\_ad\_adjustment\_revenue\_raw\_a1\_suffix | content\_owner\_asset\_ad\_adjustment\_revenue\_raw\_a1\_suffix |
| [每月影片廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-video-ad-adjustment-revenue-summary) | p\_content\_owner\_ad\_adjustment\_revenue\_summary\_a1\_suffix | content\_owner\_ad\_adjustment\_revenue\_summary\_a1\_suffix |
| [每月影片廣告調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-video-ad-adjustment-revenue-raw) | p\_content\_owner\_ad\_adjustment\_revenue\_raw\_a1\_suffix | content\_owner\_ad\_adjustment\_revenue\_raw\_a1\_suffix |
| [每月聲明廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-claim-ad-adjustment-revenue-summary) | p\_content\_owner\_claim\_ad\_adjustment\_revenue\_summary\_a1\_suffix | content\_owner\_claim\_ad\_adjustment\_revenue\_summary\_a1\_suffix |
| [每月著作權聲明廣告調整項收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-claim-ad-adjustment-revenue) | p\_content\_owner\_claim\_ad\_adjustment\_revenue\_raw\_a1\_suffix | content\_owner\_claim\_ad\_adjustment\_revenue\_raw\_a1\_suffix |
| [每月國家/地區廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-country-ad-adjustment-revenue-summary) | p\_content\_owner\_country\_ad\_adjustment\_revenue\_summary\_a1\_suffix | content\_owner\_country\_ad\_adjustment\_revenue\_summary\_a1\_suffix |
| [每月每日廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-day-ad-adjustment-revenue-summary) | p\_content\_owner\_day\_ad\_adjustment\_revenue\_summary\_a1\_suffix | content\_owner\_day\_ad\_adjustment\_revenue\_summary\_a1\_suffix |
| **訂閱收益報表** |  |  |
| [每月音樂收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-revenue-summary) | p\_content\_owner\_country\_music\_red\_revenue\_summary\_a1\_suffix | content\_owner\_country\_music\_red\_revenue\_summary\_a1\_suffix |
| [每月音樂唱片公司影片收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-video-revenue) | p\_music\_content\_owner\_red\_revenue\_raw\_a1\_suffix | music\_content\_owner\_red\_revenue\_raw\_a1\_suffix |
| [每月音樂唱片公司資產收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-assets-revenue) | p\_music\_content\_owner\_asset\_red\_revenue\_raw\_a1\_suffix | music\_content\_owner\_asset\_red\_revenue\_raw\_a1\_suffix |
| [每月音樂唱片公司訂閱者收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-subscriber-revenue-summary) | p\_music\_content\_owner\_subscriber\_red\_revenue\_summary\_a1\_suffix | music\_content\_owner\_subscriber\_red\_revenue\_summary\_a1\_suffix |
| [每月詞曲出版社收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-revenue-summary) | p\_publisher\_content\_owner\_music\_red\_revenue\_summary\_a1\_suffix | publisher\_content\_owner\_music\_red\_revenue\_summary\_a1\_suffix |
| [每月詞曲出版社訂閱收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-subscription-revenue-summary) | p\_publisher\_content\_owner\_subscriber\_red\_revenue\_summary\_a1\_suffix | publisher\_content\_owner\_subscriber\_red\_revenue\_summary\_a1\_suffix |
| [每月詞曲出版社非音樂訂閱收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-non-music-subscription-revenue-summary) | p\_publisher\_content\_owner\_non\_music\_red\_revenue\_summary\_a1\_suffix | publisher\_content\_owner\_non\_music\_red\_revenue\_summary\_a1\_suffix |
| [每月音樂唱片公司音樂收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-music-revenue-summary) | p\_music\_content\_owner\_country\_music\_red\_revenue\_summary\_a1\_suffix | music\_content\_owner\_country\_music\_red\_revenue\_summary\_a1\_suffix |
| [月費方案音樂影片收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-subscriptions-music-video-revenue) | p\_content\_owner\_music\_red\_revenue\_raw\_a1\_suffix | content\_owner\_music\_red\_revenue\_raw\_a1\_suffix |
| [月繳方案音樂資產收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-subscriptions-music-assets-revenue) | p\_content\_owner\_music\_asset\_red\_revenue\_raw\_a1\_suffix | content\_owner\_music\_asset\_red\_revenue\_raw\_a1\_suffix |
| [每週音樂收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#weekly-music-revenue-summary) | p\_music\_content\_owner\_country\_music\_red\_revenue\_summary\_weekly\_a1\_suffix | music\_content\_owner\_country\_music\_red\_revenue\_summary\_weekly\_a1\_suffix |
| [音樂唱片公司每週影片收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#weekly-music-label-videos-revenue) | p\_music\_content\_owner\_red\_revenue\_raw\_weekly\_a1\_suffix | music\_content\_owner\_red\_revenue\_raw\_weekly\_a1\_suffix |
| [每週音樂唱片公司資產收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#weekly-music-label-assets-revenue) | p\_music\_content\_owner\_asset\_red\_revenue\_raw\_weekly\_a1\_suffix | music\_content\_owner\_asset\_red\_revenue\_raw\_weekly\_a1\_suffix |
| [每月非音樂摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-non-music-summary) | p\_content\_owner\_country\_non\_music\_red\_revenue\_summary\_a1\_suffix | content\_owner\_country\_non\_music\_red\_revenue\_summary\_a1\_suffix |
| [每月音樂唱片公司非音樂收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-non-music-revenue-summary) | p\_music\_content\_owner\_country\_non\_music\_red\_revenue\_summary\_a1\_suffix | music\_content\_owner\_country\_non\_music\_red\_revenue\_summary\_a1\_suffix |
| [非音樂影片的每月訂閱收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-subscriptions-non-music-videos-revenue) | p\_content\_owner\_non\_music\_red\_revenue\_raw\_a1\_suffix | content\_owner\_non\_music\_red\_revenue\_raw\_a1\_suffix |
| [每月訂閱非音樂資產收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-subscriptions-non-music-assets-revenuee) | p\_content\_owner\_non\_music\_asset\_red\_revenue\_raw\_a1\_suffix | content\_owner\_non\_music\_asset\_red\_revenue\_raw\_a1\_suffix |
| [每週非音樂收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#weekly-non-music-revenue-summary) | p\_music\_content\_owner\_country\_non\_music\_red\_revenue\_summary\_weekly\_a1\_suffix | music\_content\_owner\_country\_non\_music\_red\_revenue\_summary\_weekly\_a1\_suffix |
| [每月音樂唱片公司資產訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-asset-subscription-adjustment-revenue-raw) | p\_music\_content\_owner\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix | music\_content\_owner\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix |
| [月費方案調整項音樂影片原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-subscriptions-adjustment-music-video-raw) | p\_music\_content\_owner\_red\_adjustment\_revenue\_raw\_a1\_suffix | music\_content\_owner\_red\_adjustment\_revenue\_raw\_a1\_suffix |
| [每月音樂唱片公司國家/地區音樂訂閱調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-country-music-subscription-adjustment-revenue-summary) | p\_music\_content\_owner\_country\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix | music\_content\_owner\_country\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix |
| [每月音樂唱片公司國家/地區非音樂訂閱調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-country-non-music-subscription-adjustment-revenue-summary) | p\_music\_content\_owner\_country\_non\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix | music\_content\_owner\_country\_non\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix |
| [每月非音樂資產訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-non-music-asset-subscription-adjustment-revenue-raw) | p\_content\_owner\_non\_music\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix | content\_owner\_non\_music\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix |
| [每月非音樂訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-non-music-subscription-adjustment-revenue-raw) | p\_content\_owner\_non\_music\_red\_adjustment\_revenue\_raw\_a1\_suffix | content\_owner\_non\_music\_red\_adjustment\_revenue\_raw\_a1\_suffix |
| [每月音樂影片訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-video-subscription-adjustment-revenue-raw) | p\_content\_owner\_music\_video\_red\_adjustment\_revenue\_raw\_a1\_suffix | content\_owner\_music\_video\_red\_adjustment\_revenue\_raw\_a1\_suffix |
| [每月音樂資產訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-asset-subscription-adjustment-revenue-raw) | p\_content\_owner\_music\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix | content\_owner\_music\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix |
| [每月詞曲出版社資產訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-asset-subscription-adjustment-revenue-raw) | p\_publisher\_content\_owner\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix | publisher\_content\_owner\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix |
| [每月詞曲出版社國家/地區非音樂訂閱調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-country-non-music-subscription-adjustment-revenue-summary) | p\_publisher\_content\_owner\_country\_non\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix | publisher\_content\_owner\_country\_non\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix |
| [每月詞曲出版社國家/地區音樂訂閱調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-country-music-subscription-adjustment-revenue-summary) | p\_publisher\_content\_owner\_country\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix | publisher\_content\_owner\_country\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix |
| **Shorts 收益報表** |  |  |
| [每月 YouTube Shorts 唱片公司內容擁有者收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/shorts?hl=zh-tw#monthly-youtube-shorts-music-label-content-owner-revenue-summary) | p\_music\_content\_owner\_shorts\_revenue\_summary\_a1\_suffix | music\_content\_owner\_shorts\_revenue\_summary\_a1\_suffix |
| [每月 YouTube Shorts 詞曲出版社內容擁有者收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/shorts?hl=zh-tw#monthly-youtube-shorts-music-publisher-content-owner-revenue-summary) | p\_publisher\_content\_owner\_shorts\_revenue\_summary\_a1\_suffix | publisher\_content\_owner\_shorts\_revenue\_summary\_a1\_suffix |
| [每月 YouTube Shorts 全球廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/shorts?hl=zh-tw#monthly-youtube-shorts-global-ad-revenue-summary) | p\_content\_owner\_shorts\_global\_ad\_revenue\_summary\_a2\_suffix | content\_owner\_shorts\_global\_ad\_revenue\_summary\_a2\_suffix |
| [每日 YouTube Shorts 廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/shorts?hl=zh-tw#daily-youtube-shorts-ad-revenue-summary) | p\_content\_owner\_shorts\_day\_ad\_revenue\_summary\_a2\_suffix | content\_owner\_shorts\_day\_ad\_revenue\_summary\_a2\_suffix |
| [每月 YouTube Shorts 國家/地區廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/shorts?hl=zh-tw#monthly-youtube-shorts-country-ad-revenue-summary) | p\_content\_owner\_shorts\_country\_ad\_revenue\_summary\_a2\_suffix | content\_owner\_shorts\_country\_ad\_revenue\_summary\_a2\_suffix |
| [每月 YouTube Shorts 廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/shorts?hl=zh-tw#monthly-youtube-shorts-ad-revenue-summary) | p\_content\_owner\_shorts\_ad\_revenue\_summary\_a2\_suffix | content\_owner\_shorts\_ad\_revenue\_summary\_a2\_suffix |
| [每月 YouTube Shorts 訂閱收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/shorts?hl=zh-tw#monthly-youtube-shorts-subscriptions-revenue-summary) | p\_content\_owner\_shorts\_red\_revenue\_summary\_a1\_suffix | content\_owner\_shorts\_red\_revenue\_summary\_a1\_suffix |
| [每月 YouTube Shorts 訂閱收益影片摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/shorts?hl=zh-tw#monthly-youtube-shorts-subscriptions-revenue-video-summary) | p\_content\_owner\_shorts\_red\_revenue\_video\_summary\_a1\_suffix | content\_owner\_shorts\_red\_revenue\_video\_summary\_a1\_suffix |
| **扣繳稅額報表** |  |  |
| [預扣稅額](https://developers.google.com/youtube/reporting/v1/reports/system_managed/taxes?hl=zh-tw#tax-withholding) | p\_content\_owner\_tax\_withholding\_a1\_suffix | content\_owner\_tax\_withholding\_a1\_suffix |
| **影片報表** |  |  |
| [每日影片中繼資料 (1.4 版)](https://developers.google.com/youtube/reporting/v1/reports/system_managed/videos?hl=zh-tw#daily-video-metadata-version-1.4) | p\_content\_owner\_video\_metadata\_a4\_suffix | content\_owner\_video\_metadata\_a4\_suffix |
| **素材資源報表** |  |  |
| [每日資產報表](https://developers.google.com/youtube/reporting/v1/reports/system_managed/assets?hl=zh-tw#daily-asset-report-version-1.3) | p\_content\_owner\_asset\_a3\_suffix | content\_owner\_asset\_a3\_suffix |
| [每日資產衝突](https://developers.google.com/youtube/reporting/v1/reports/system_managed/assets?hl=zh-tw#daily-asset-conflicts-version-1.3) | p\_content\_owner\_asset\_conflict\_a3\_suffix | content\_owner\_asset\_conflict\_a3\_suffix |
| **參考檔案報表** |  |  |
| [每週參考資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/references?hl=zh-tw#weekly-references) | p\_content\_owner\_active\_references\_a1\_suffix | content\_owner\_active\_references\_a1\_suffix |
| **著作權聲明報表** |  |  |
| [每日兌換次數 (1.2 版)](https://developers.google.com/youtube/reporting/v1/reports/system_managed/claims?hl=zh-tw#daily-claims-version-1.2) | p\_content\_owner\_active\_claims\_a3\_suffix | content\_owner\_active\_claims\_a3\_suffix |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]