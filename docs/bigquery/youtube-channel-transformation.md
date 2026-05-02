* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# YouTube 頻道報表轉換

當您的 YouTube 頻道報表移轉至 BigQuery 時，報表會轉換成下列 BigQuery 資料表和檢視表。

當您在 BigQuery 中查看資料表和檢視表時，suffix 的值是您在建立移轉時設定的資料表尾碼。

| **YouTube 頻道報告** | **BigQuery 資料表** | **BigQuery 檢視區塊** |
| --- | --- | --- |
| **影片報表** |  |  |
| [使用者活動](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-user-activity) | p\_channel\_basic\_a3\_suffix | channel\_basic\_a3\_suffix |
| [依省份劃分的使用者活動](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-province) | p\_channel\_province\_a3\_suffix | channel\_province\_a3\_suffix |
| [播放位置](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-playback-locations) | p\_channel\_playback\_location\_a3\_suffix | channel\_playback\_location\_a3\_suffix |
| [流量來源](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-traffic-sources) | p\_channel\_traffic\_source\_a3\_suffix | channel\_traffic\_source\_a3\_suffix |
| [裝置類型和作業系統](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-device-type-and-operating-system) | p\_channel\_device\_os\_a3\_suffix | channel\_device\_os\_a3\_suffix |
| [觀眾客層](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-viewer-demographics) | p\_channel\_demographics\_a1\_suffix | channel\_demographics\_a1\_suffix |
| [內容共享 (依平台分組)](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-content-sharing) | p\_channel\_sharing\_service\_a1\_suffix | channel\_sharing\_service\_a1\_suffix |
| [註解](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-annotations) | p\_channel\_annotations\_a1\_suffix | channel\_annotations\_a1\_suffix |
| [資訊卡](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-cards) | p\_channel\_cards\_a1\_suffix | channel\_cards\_a1\_suffix |
| [片尾](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-end-screens) | p\_channel\_end\_screens\_a1\_suffix | channel\_end\_screens\_a1\_suffix |
| [字幕](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-subtitles) | p\_channel\_subtitles\_a3\_suffix | channel\_subtitles\_a3\_suffix |
| [合併](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#video-combined) | p\_channel\_combined\_a3\_suffix | channel\_combined\_a3\_suffix |
| **播放清單報表** |  |  |
| [使用者活動](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#playlist-user-activity) | p\_playlist\_basic\_a2\_suffix | playlist\_basic\_a2\_suffix |
| [依省份劃分的使用者活動](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#playlist-province) | p\_playlist\_province\_a2\_suffix | playlist\_province\_a2\_suffix |
| [播放位置](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#playlist-playback-locations) | p\_playlist\_playback\_location\_a2\_suffix | playlist\_playback\_location\_a2\_suffix |
| [流量來源](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#playlist-traffic-sources) | p\_playlist\_traffic\_source\_a2\_suffix | playlist\_traffic\_source\_a2\_suffix |
| [裝置類型和作業系統](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#playlist-device-type-and-operating-system) | p\_playlist\_device\_os\_a2\_suffix | playlist\_device\_os\_a2\_suffix |
| [合併](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#playlist-combined) | p\_playlist\_combined\_a2\_suffix | playlist\_combined\_a2\_suffix |
| **觸及報表** |  |  |
| [觸及基本](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#reach-reports) | p\_channel\_reach\_basic\_a1\_suffix | channel\_reach\_basic\_a1\_suffix |
| [合併觸及](https://developers.google.com/youtube/reporting/v1/reports/channel_reports?hl=zh-tw#reach-reports) | p\_channel\_reach\_combined\_a1\_suffix | channel\_reach\_combined\_a1\_suffix |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]