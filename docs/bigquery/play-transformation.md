* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Play 報表轉換

當您的 Google Play 報表移轉至 BigQuery 時，報表會轉換成下列 BigQuery 表格和檢視表。

當您在 BigQuery 中查看資料表和檢視表時，suffix 的值是您在建立移轉時設定的資料表尾碼。

| Google Play 報表 | BigQuery 表格 | BigQuery 視圖 |
| --- | --- | --- |
| **詳細報表** |  |  |
| ***評論*** |  |  |
| [評論](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#reviews) | p\_Reviews\_suffix | Reviews\_suffix |
| ***財務報表*** |  |  |
| [預估銷售額](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#financial) | p\_Sales\_suffix | Sales\_suffix |
| [收益](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#financial) | p\_Earnings\_suffix | Earnings\_suffix |
| [韓國 Play 餘額付款](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#financial) | p\_Korean\_Play\_balance\_funded\_suffix | Korean\_Play\_balance\_funded\_suffix |
| **匯總報表** |  |  |
| ***統計資料*** |  |  |
| [安裝次數](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#statistics) | p\_Installs\_app\_version\_suffix  p\_Installs\_carrier\_suffix  p\_Installs\_country\_suffix  p\_Installs\_device\_suffix  p\_Installs\_language\_suffix  p\_Installs\_os\_version\_suffix | Installs\_app\_version\_suffix  Installs\_carrier\_suffix  Installs\_country\_suffix  Installs\_device\_suffix  Installs\_language\_suffix  Installs\_os\_version\_suffix |
| [當機](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#statistics) | p\_Crashes\_app\_version\_suffix  p\_Crashes\_device\_suffix  p\_Crashes\_os\_version\_suffix | Crashes\_app\_version\_suffix  Crashes\_device\_suffix  Crashes\_os\_version\_suffix |
| [評分](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#statistics) | p\_Ratings\_app\_version\_suffix  p\_Ratings\_carrier\_suffix  p\_Ratings\_country\_suffix  p\_Ratings\_device\_suffix  p\_Ratings\_language\_suffix  p\_Ratings\_os\_version\_suffix | Ratings\_app\_version\_suffix  Ratings\_carrier\_suffix  Ratings\_country\_suffix  Ratings\_device\_suffix  Ratings\_language\_suffix  Ratings\_os\_version\_suffix |
| [訂閱人數](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#statistics) | p\_Stats\_Subscribers\_country\_suffix  p\_Stats\_Subscribers\_device\_suffix | Stats\_Subscribers\_country\_suffix  Stats\_Subscribers\_device\_suffix |
| ***獲取新客*** |  |  |
| [商店成效](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#acquisition) | p\_Store\_Performance\_country\_suffix  p\_Store\_Performance\_traffic\_source\_suffix | Store\_Performance\_country\_suffix  Store\_Performance\_traffic\_source\_suffix |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]