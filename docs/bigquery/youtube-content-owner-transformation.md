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

## YouTube 內容擁有者報告

以下各節說明 YouTube 內容擁有者報表的轉換。

### 影片報表

下列報表著重於影片層級的使用者活動、播放位置、流量來源和客層。

#### 使用者活動

YouTube 報表：
[使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-user-activity)

BigQuery 資料表：
:   p\_content\_owner\_basic\_a4\_suffix

BigQuery 檢視畫面：
:   content\_owner\_basic\_a4\_suffix

#### 使用者活動 (依省分組)

YouTube 報表：
[依省份劃分的使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-province)

BigQuery 資料表：
:   p\_content\_owner\_province\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_province\_3\_suffix

#### 播放位置

YouTube 報表：
[播放位置](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-playback-locations)

BigQuery 資料表：
:   p\_content\_owner\_playback\_location\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_playback\_location\_a3\_suffix

#### 流量來源

YouTube 報表：
[流量來源](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-traffic-sources)

BigQuery 資料表：
:   p\_content\_owner\_traffic\_source\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_traffic\_source\_a3\_suffix

#### 裝置類型和作業系統

YouTube 報表：
[裝置類型和作業系統](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-device-type-and-operating-system)

BigQuery 資料表：
:   p\_content\_owner\_device\_os\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_device\_os\_a3\_suffix

#### 觀眾客層

YouTube 報表：
[觀眾客層](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-viewer-demographics)

BigQuery 資料表：
:   p\_content\_owner\_demographics\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_demographics\_a1\_suffix

#### 內容共享 (依平台分組)

YouTube 報表：
[依平台分享內容](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-content-sharing)

BigQuery 資料表：
:   p\_content\_owner\_sharing\_service\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_sharing\_service\_a1\_suffix

#### 註解

YouTube 報表：
[註解](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-annotations)

BigQuery 資料表：
:   p\_content\_owner\_annotations\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_annotations\_a1\_suffix

#### 資訊卡

YouTube 報表：
[資訊卡](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-cards)

BigQuery 資料表：
:   p\_content\_owner\_cards\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_cards\_a1\_suffix

#### 結束畫面

YouTube 報表：
[結束畫面](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-end-screens)

BigQuery 資料表：
:   p\_content\_owner\_end\_screens\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_end\_screens\_a1\_suffix

#### 字幕

YouTube 報表：
[字幕](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-subtitles)

BigQuery 資料表：
:   p\_content\_owner\_subtitles\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_subtitles\_a3\_suffix

#### 合併

YouTube 報表：
[合併](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#video-combined)

BigQuery 資料表：
:   p\_content\_owner\_combined\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_combined\_a3\_suffix

### 播放清單報表

下列報表包含播放清單的成效指標和使用者活動。

#### 使用者活動

YouTube 報表：
[使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-user-activity)

BigQuery 資料表：
:   p\_content\_owner\_playlist\_basic\_a2\_suffix

BigQuery 檢視畫面：
:   content\_owner\_playlist\_basic\_a2\_suffix

#### 使用者活動 (依省分組)

YouTube 報表：
[依省份劃分的使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-province)

BigQuery 資料表：
:   p\_content\_owner\_playlist\_province\_a2\_suffix

BigQuery 檢視畫面：
:   content\_owner\_playlist\_province\_a2\_suffix

#### 播放位置

YouTube 報表：
[播放位置](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-playback-locations)

BigQuery 資料表：
:   p\_content\_owner\_playlist\_playback\_location\_a2\_suffix

BigQuery 檢視畫面：
:   content\_owner\_playlist\_playback\_location\_a2

#### 流量來源

YouTube 報表：
[流量來源](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-traffic-sources)

BigQuery 資料表：
:   p\_content\_owner\_playlist\_traffic\_source\_a2

BigQuery 檢視畫面：
:   content\_owner\_playlist\_traffic\_source\_a2\_suffix

#### 裝置類型和作業系統

YouTube 報表：
[裝置類型和作業系統](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-device-type-and-operating-system)

BigQuery 資料表：
:   p\_content\_owner\_playlist\_device\_os\_a2\_suffix

BigQuery 檢視畫面：
:   content\_owner\_playlist\_device\_os\_a2\_suffix

#### 合併

YouTube 報表：
[合併](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#playlist-combined)

BigQuery 資料表：
:   p\_content\_owner\_playlist\_combined\_a2\_suffix

BigQuery 檢視畫面：
:   content\_owner\_playlist\_combined\_a2\_suffix

### 廣告費率報表

下列報表會顯示主要廣告指標和交易率。

#### 廣告費率報表

YouTube 報表：
[廣告費率報表](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#ad-rate-reports)

BigQuery 資料表：
:   p\_content\_owner\_ad\_rates\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_ad\_rates\_a1\_suffix

### 預估收益報表

下列報表會預估影片和資產層級的收益。

#### 估算的影片收益

YouTube 報表：
[影片預估收益](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#estimated-revenue-videos)

BigQuery 資料表：
:   p\_content\_owner\_estimated\_revenue\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_estimated\_revenue\_a1\_suffix

#### 估算的資產收益

YouTube 報表：
[預估資產收益](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#estimated-revenue-assets)

BigQuery 資料表：
:   p\_content\_owner\_asset\_estimated\_revenue\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_estimated\_revenue\_a1\_suffix

### 資產報表

下列報表著重於素材資源成效、使用者參與度和中繼資料。

#### 使用者活動

YouTube 報表：
[使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-user-activity)

BigQuery 資料表：
:   p\_content\_owner\_asset\_basic\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_basic\_a3\_suffix

#### 使用者活動 (依省分組)

YouTube 報表：
[依省份劃分的使用者活動](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-province)

BigQuery 資料表：
:   p\_content\_owner\_asset\_province\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_province\_a3\_suffix

#### 影片播放位置

YouTube 報表：
[影片播放位置](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-playback-locations)

BigQuery 資料表：
:   p\_content\_owner\_asset\_playback\_location\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_playback\_location\_a3\_suffix

#### 流量來源

YouTube 報表：
[流量來源](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-traffic-sources)

BigQuery 資料表：
:   p\_content\_owner\_asset\_traffic\_source\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_traffic\_source\_a3\_suffix

#### 裝置類型和作業系統

YouTube 報表：
[裝置類型和作業系統](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-device-type-and-operating-system)

BigQuery 資料表：
:   p\_content\_owner\_asset\_device\_os\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_device\_os\_a3\_suffix

#### 觀眾客層

YouTube 報表：
[觀眾客層](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-viewer-demographics)

BigQuery 資料表：
:   p\_content\_owner\_asset\_demographics\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_demographics\_a1\_suffix

#### 內容共享 (依平台分組)

YouTube 報表：
[依平台分享內容](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-content-sharing)

BigQuery 資料表：
:   p\_content\_owner\_asset\_sharing\_service\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_sharing\_service\_a1\_suffix

#### 註解

YouTube 報表：
[註解](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-annotations)

BigQuery 資料表：
:   p\_content\_owner\_asset\_annotations\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_annotations\_a1\_suffix

#### 資訊卡

YouTube 報表：
[資訊卡](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-cards)

BigQuery 資料表：
:   p\_content\_owner\_asset\_cards\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_cards\_a1\_suffix

#### 結束畫面

YouTube 報表：
[結束畫面](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-end-screens)

BigQuery 資料表：
:   p\_content\_owner\_asset\_end\_screens\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_end\_screens\_a1\_suffix

#### 合併

YouTube 報表：
[合併](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#asset-combined)

BigQuery 資料表：
:   p\_content\_owner\_asset\_combined\_a3\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_combined\_a3\_suffix

### 觸及報表

下列報表涵蓋頻道內容的觀眾觸及率指標。

#### 觸及基本版

YouTube 報表：
[觸及基本](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#reach-reports)

BigQuery 資料表：
:   p\_content\_owner\_reach\_basic\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_reach\_basic\_a1\_suffix

#### 綜合觸及

YouTube 報表：
[合併觸及](https://developers.google.com/youtube/reporting/v1/reports/content_owner_reports?hl=zh-tw#reach-reports)

BigQuery 資料表：
:   p\_content\_owner\_reach\_combined\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_reach\_combined\_a1\_suffix

## YouTube 系統代管報表

以下各節說明 YouTube 系統管理的報表轉換。

### 財務摘要報表

下列報表會彙整聯播網的付款和帳單資料。

#### 每月付款摘要

YouTube 報表：
[每月付款摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/financial-summaries?hl=zh-tw#monthly-payments-summary)

BigQuery 資料表：
:   p\_content\_owner\_payments\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_payments\_summary\_a1\_suffix

### 廣告收益報表

下列報表提供不同維度的廣告收益摘要，例如國家/地區、影片和資產。

#### 每月全球廣告收益摘要

YouTube 報表：
[每月全球廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-global-ad-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_global\_ad\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_global\_ad\_revenue\_summary\_a1\_suffix

#### 每月國家/地區廣告收益摘要

YouTube 報表：
[每月國家/地區廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-country-ad-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_country\_ad\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_country\_ad\_revenue\_summary\_a1\_suffix

#### 每月每日廣告收益摘要

YouTube 報表：
[每月每日廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-day-ad-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_day\_ad\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_day\_ad\_revenue\_summary\_a1\_suffix

#### 每週全球廣告收益摘要

YouTube 報表：
[每週全球廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-global-ad-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_global\_ad\_revenue\_summary\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_global\_ad\_revenue\_summary\_weekly\_a1\_suffix

#### 每週國家/地區廣告收益摘要

YouTube 報表：
[每週國家/地區廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-country-ad-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_country\_ad\_revenue\_summary\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_country\_ad\_revenue\_summary\_weekly\_a1\_suffix

#### 每週每日廣告收益摘要

YouTube 報表：
[每週每日廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-day-ad-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_day\_ad\_revenue\_summary\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_day\_ad\_revenue\_summary\_weekly\_a1\_suffix

#### 每部影片的匯總廣告收益

YouTube 報表：
[每部影片的匯總廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#aggregate-ad-revenue-per-video)

BigQuery 資料表：
:   p\_content\_owner\_ad\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_ad\_revenue\_summary\_a1\_suffix

#### 每週影片廣告收益摘要

YouTube 報表：
[每週影片廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-video-ad-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_ad\_revenue\_summary\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_ad\_revenue\_summary\_weekly\_a1\_suffix

#### 每週影片廣告收益

YouTube 報表：
[每週影片廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-video-ad-revenue)

BigQuery 資料表：
:   p\_content\_owner\_ad\_revenue\_raw\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_ad\_revenue\_raw\_weekly\_a1\_suffix

#### 每部影片的每日廣告收益

YouTube 報表：
[每部影片的每日廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#daily-ad-revenue-per-video)

BigQuery 資料表：
:   p\_content\_owner\_ad\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_ad\_revenue\_raw\_a1\_suffix

#### 每項資產的匯總廣告收益

YouTube 報表：
[每項資產的廣告收益總計](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#aggregate-ad-revenue-per-asset)

BigQuery 資料表：
:   p\_content\_owner\_asset\_ad\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_ad\_revenue\_summary\_a1\_suffix

#### 每項資產的每日廣告收益

YouTube 報表：
[每日每項資產的廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#daily-ad-revenue-per-asset)

BigQuery 資料表：
:   p\_content\_owner\_asset\_ad\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_ad\_revenue\_raw\_a1\_suffix

#### 每月聲明廣告收益摘要

YouTube 報表：
[每月著作權聲明廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-claim-ad-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_claim\_ad\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_claim\_ad\_revenue\_summary\_a1\_suffix

#### 每週著作權聲明廣告收益摘要

YouTube 報表：
[每週著作權聲明廣告收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-claim-ad-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_claim\_ad\_revenue\_summary\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_claim\_ad\_revenue\_summary\_weekly\_a1\_suffix

#### 每月著作權聲明廣告收益

YouTube 報表：
[每月著作權聲明廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-claim-ad-revenue)

BigQuery 資料表：
:   p\_content\_owner\_claim\_ad\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_claim\_ad\_revenue\_raw\_a1\_suffix

#### 每週著作權聲明廣告收益

YouTube 報表：
[每週著作權聲明廣告收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#weekly-claim-ad-revenue)

BigQuery 資料表：
:   p\_content\_owner\_claim\_ad\_revenue\_raw\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_claim\_ad\_revenue\_raw\_weekly\_a1\_suffix

#### 每月全球廣告調整項收益摘要

YouTube 報表：
[每月全球廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-global-ad-adjustment-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_global\_ad\_adjustment\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_global\_ad\_adjustment\_revenue\_summary\_a1\_suffix

#### 每月素材資源廣告調整項收益摘要

YouTube 報表：
[每月素材資源廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-asset-ad-adjustment-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_asset\_ad\_adjustment\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_ad\_adjustment\_revenue\_summary\_a1\_suffix

#### 每月素材資源廣告調整項收益

YouTube 報表：
[每月素材資源廣告調整項收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-asset-ad-adjustment-revenue)

BigQuery 資料表：
:   p\_content\_owner\_asset\_ad\_adjustment\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_asset\_ad\_adjustment\_revenue\_raw\_a1\_suffix

#### 每月影片廣告調整項收益摘要

YouTube 報表：
[每月影片廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-video-ad-adjustment-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_ad\_adjustment\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_ad\_adjustment\_revenue\_summary\_a1\_suffix

#### 每月影片廣告調整項收益原始資料

YouTube 報表：
[每月影片廣告調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-video-ad-adjustment-revenue-raw)

BigQuery 資料表：
:   p\_content\_owner\_ad\_adjustment\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_ad\_adjustment\_revenue\_raw\_a1\_suffix

#### 每月著作權聲明廣告調整項收益摘要

YouTube 報表：
[每月聲明廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-claim-ad-adjustment-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_claim\_ad\_adjustment\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_claim\_ad\_adjustment\_revenue\_summary\_a1\_suffix

#### 每月著作權聲明廣告調整項收益

YouTube 報表：
[每月著作權聲明廣告調整項收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-claim-ad-adjustment-revenue)

BigQuery 資料表：
:   p\_content\_owner\_claim\_ad\_adjustment\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_claim\_ad\_adjustment\_revenue\_raw\_a1\_suffix

#### 每月國家/地區廣告調整項收益摘要

YouTube 報表：
[每月國家/地區廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-country-ad-adjustment-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_country\_ad\_adjustment\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_country\_ad\_adjustment\_revenue\_summary\_a1\_suffix

#### 每月每日廣告調整項收益摘要

YouTube 報表：
[每月每日廣告調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/ads?hl=zh-tw#monthly-day-ad-adjustment-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_day\_ad\_adjustment\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_day\_ad\_adjustment\_revenue\_summary\_a1\_suffix

### 訂閱收益報表

下列報表會彙整影片和資產的音樂與非音樂訂閱收益。

#### 每月音樂收益摘要

YouTube 報表：
[每月音樂收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-revenue-summary)

BigQuery 資料表：
:   p\_content\_owner\_country\_music\_red\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_country\_music\_red\_revenue\_summary\_a1\_suffix

#### 每月音樂唱片公司影片收益

YouTube 報表：
[每月唱片公司影片收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-video-revenue)

BigQuery 資料表：
:   p\_music\_content\_owner\_red\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_red\_revenue\_raw\_a1\_suffix

#### 每月音樂唱片公司資產收益

YouTube 報表：
[每月唱片公司資產收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-assets-revenue)

BigQuery 資料表：
:   p\_music\_content\_owner\_asset\_red\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_asset\_red\_revenue\_raw\_a1\_suffix

#### 每月音樂唱片公司訂閱者收益摘要

YouTube 報表：
[每月唱片公司訂閱者收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-subscriber-revenue-summary)

BigQuery 資料表：
:   p\_music\_content\_owner\_subscriber\_red\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_subscriber\_red\_revenue\_summary\_a1\_suffix

#### 每月詞曲出版社收益摘要

YouTube 報表：
[每月詞曲出版社收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-revenue-summary)

BigQuery 資料表：
:   p\_publisher\_content\_owner\_music\_red\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   publisher\_content\_owner\_music\_red\_revenue\_summary\_a1\_suffix

#### 每月詞曲出版社訂閱收益摘要

YouTube 報表：
[每月詞曲出版社訂閱收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-subscription-revenue-summary)

BigQuery 資料表：
:   p\_publisher\_content\_owner\_subscriber\_red\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   publisher\_content\_owner\_subscriber\_red\_revenue\_summary\_a1\_suffix

#### 每月詞曲出版社非音樂訂閱收益摘要

YouTube 報表：
[每月詞曲出版社非音樂訂閱收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-non-music-subscription-revenue-summary)

BigQuery 資料表：
:   p\_publisher\_content\_owner\_non\_music\_red\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   publisher\_content\_owner\_non\_music\_red\_revenue\_summary\_a1\_suffix

#### 每月唱片公司音樂收益摘要

YouTube 報表：
[每月唱片公司音樂收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-music-revenue-summary)

BigQuery 資料表：
:   p\_music\_content\_owner\_country\_music\_red\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_country\_music\_red\_revenue\_summary\_a1\_suffix

#### 按月訂閱音樂影片收益

YouTube 報表：
[每月訂閱音樂影片收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-subscriptions-music-video-revenue)

BigQuery 資料表：
:   p\_content\_owner\_music\_red\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_music\_red\_revenue\_raw\_a1\_suffix

#### 每月訂閱音樂資產收益

YouTube 報表：
[每月訂閱音樂資產收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-subscriptions-music-assets-revenue)

BigQuery 資料表：
:   p\_content\_owner\_music\_asset\_red\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_music\_asset\_red\_revenue\_raw\_a1\_suffix

#### 每週音樂收益摘要

YouTube 報表：
[每週音樂收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#weekly-music-revenue-summary)

BigQuery 資料表：
:   p\_music\_content\_owner\_country\_music\_red\_revenue\_summary\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_country\_music\_red\_revenue\_summary\_weekly\_a1\_suffix

#### 音樂唱片公司每週影片收益

YouTube 報表：
[每週唱片公司影片收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#weekly-music-label-videos-revenue)

BigQuery 資料表：
:   p\_music\_content\_owner\_red\_revenue\_raw\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_red\_revenue\_raw\_weekly\_a1\_suffix

#### 每週音樂唱片公司資產收益

YouTube 報表：
[每週唱片公司資產收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#weekly-music-label-assets-revenue)

BigQuery 資料表：
:   p\_music\_content\_owner\_asset\_red\_revenue\_raw\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_asset\_red\_revenue\_raw\_weekly\_a1\_suffix

#### 每月非音樂摘要

YouTube 報表：
[每月非音樂摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-non-music-summary)

BigQuery 資料表：
:   p\_content\_owner\_country\_non\_music\_red\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_country\_non\_music\_red\_revenue\_summary\_a1\_suffix

#### 每月音樂唱片公司非音樂收益摘要

YouTube 報表：
[每月唱片公司非音樂收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-non-music-revenue-summary)

BigQuery 資料表：
:   p\_music\_content\_owner\_country\_non\_music\_red\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_country\_non\_music\_red\_revenue\_summary\_a1\_suffix

#### 非音樂影片的每月訂閱收益

YouTube 報表：
[每月訂閱非音樂影片收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-subscriptions-non-music-videos-revenue)

BigQuery 資料表：
:   p\_content\_owner\_non\_music\_red\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_non\_music\_red\_revenue\_raw\_a1\_suffix

#### 非音樂資產的每月訂閱收益

YouTube 報表：
[每月訂閱非音樂素材資源收益](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-subscriptions-non-music-assets-revenue)

BigQuery 資料表：
:   p\_content\_owner\_non\_music\_asset\_red\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_non\_music\_asset\_red\_revenue\_raw\_a1\_suffix

#### 每週非音樂收益摘要

YouTube 報表：
[每週非音樂收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#weekly-non-music-revenue-summary)

BigQuery 資料表：
:   p\_music\_content\_owner\_country\_non\_music\_red\_revenue\_summary\_weekly\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_country\_non\_music\_red\_revenue\_summary\_weekly\_a1\_suffix

#### 每月音樂唱片公司資產訂閱調整項收益原始資料

YouTube 報表：
[每月唱片公司資產訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-asset-subscription-adjustment-revenue-raw)

BigQuery 資料表：
:   p\_music\_content\_owner\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix

#### 按月訂閱調整音樂影片原始

YouTube 報表：
[每月訂閱調整音樂影片原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-subscriptions-adjustment-music-video-raw)

BigQuery 資料表：
:   p\_music\_content\_owner\_red\_adjustment\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_red\_adjustment\_revenue\_raw\_a1\_suffix

#### 每月唱片公司鄉村音樂訂閱調整項收益摘要

YouTube 報表：
[每月唱片公司國家/地區音樂訂閱調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-country-music-subscription-adjustment-revenue-summary)

BigQuery 資料表：
:   p\_music\_content\_owner\_country\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_country\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix

#### 每月音樂唱片公司國家/地區非音樂訂閱調整收益摘要

YouTube 報表：
[每月唱片公司國家/地區非音樂訂閱調整項收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-label-country-non-music-subscription-adjustment-revenue-summary)

BigQuery 資料表：
:   p\_music\_content\_owner\_country\_non\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   music\_content\_owner\_country\_non\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix

#### 每月非音樂資產訂閱調整項收益原始資料

YouTube 報表：
[每月非音樂資產訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-non-music-asset-subscription-adjustment-revenue-raw)

BigQuery 資料表：
:   p\_content\_owner\_non\_music\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_non\_music\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix

#### 每月非音樂訂閱調整項收益原始資料

YouTube 報表：
[每月非音樂訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-non-music-subscription-adjustment-revenue-raw)

BigQuery 資料表：
:   p\_content\_owner\_non\_music\_red\_adjustment\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_non\_music\_red\_adjustment\_revenue\_raw\_a1\_suffix

#### 每月音樂影片訂閱調整項收益原始資料

YouTube 報表：
[每月音樂影片訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-video-subscription-adjustment-revenue-raw)

BigQuery 資料表：
:   p\_content\_owner\_music\_video\_red\_adjustment\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_music\_video\_red\_adjustment\_revenue\_raw\_a1\_suffix

#### 每月音樂資產訂閱調整項收益原始資料

YouTube 報表：
[每月音樂資產訂閱調整項收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-asset-subscription-adjustment-revenue-raw)

BigQuery 資料表：
:   p\_content\_owner\_music\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   content\_owner\_music\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix

#### 每月詞曲出版社素材訂閱調整項收益原始資料

YouTube 報表：
[每月詞曲出版社資產訂閱調整收益原始資料](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-asset-subscription-adjustment-revenue-raw)

BigQuery 資料表：
:   p\_publisher\_content\_owner\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix

BigQuery 檢視畫面：
:   publisher\_content\_owner\_asset\_red\_adjustment\_revenue\_raw\_a1\_suffix

#### 每月詞曲出版社國家/地區非音樂訂閱調整收益摘要

YouTube 報表：
[每月詞曲出版社國家/地區非音樂訂閱調整收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-country-non-music-subscription-adjustment-revenue-summary)

BigQuery 資料表：
:   p\_publisher\_content\_owner\_country\_non\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   publisher\_content\_owner\_country\_non\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix

#### 每月詞曲出版社鄉村音樂訂閱調整項收益摘要

YouTube 報表：
[每月詞曲出版社國家/地區音樂訂閱調整收益摘要](https://developers.google.com/youtube/reporting/v1/reports/system_managed/subscriptions?hl=zh-tw#monthly-music-publisher-country-music-subscription-adjustment-revenue-summary)

BigQuery 資料表：
:   p\_publisher\_content\_owner\_country\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix

BigQuery 檢視畫面：
:   publisher\_content\_owner\_country\_music\_red\_adjustment\_revenue\_summary\_a1\_suffix

### YouTube Shorts 收益報表

下列報表會匯總 YouTube Shorts 的收益和參與度指標。