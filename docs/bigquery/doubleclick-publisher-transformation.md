Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Google Ad Manager 報表轉換

當您的 Google Ad Manager (原名為 DoubleClick for Publishers) 資料移轉檔案移轉到 BigQuery 時，檔案會轉換成本文所述的 BigQuery 表格和視圖。

當您在 BigQuery 中檢視資料表和視圖時，network\_code 的值是您的 Ad Manager 聯播網代碼。

## 資料移轉檔案

下列各節中的報表會詳細說明 Ad Manager 聯播網活動。

### 網路要求

Ad Manager 檔案：
[NetworkRequests](https://support.google.com/admanager/answer/1733124?hl=zh-tw)
和
[NetworkBackfillRequests](https://support.google.com/admanager/answer/1733124?hl=zh-tw)

BigQuery 資料表：
:   p\_NetworkRequests\_network\_code  
    p\_NetworkBackfillRequests\_network\_code

BigQuery 檢視畫面：
:   NetworkRequests\_network\_code  
    NetworkBackfillRequests\_network\_code

### 聯播網代碼調用次數

Ad Manager 檔案：
[NetworkCodeServes](https://support.google.com/admanager/answer/1733124?hl=zh-tw)
和
[NetworkBackfillCodeServes](https://support.google.com/admanager/answer/1733124?hl=zh-tw)

BigQuery 資料表：
:   p\_NetworkCodeServes  
    p\_NetworkBackfillCodeServes\_network\_code

BigQuery 檢視畫面：
:   NetworkCodeServes  
    NetworkBackfillCodeServes\_network\_code

### 聯播網曝光次數

Ad Manager 檔案：
[NetworkImpressions](https://support.google.com/admanager/answer/1733124?hl=zh-tw)
和
[NetworkBackfillImpressions](https://support.google.com/admanager/answer/1733124?hl=zh-tw)

BigQuery 資料表：
:   p\_NetworkImpressions\_network\_code  
    p\_NetworkBackfillImpressions\_network\_code

BigQuery 檢視畫面：
:   NetworkImpressions\_network\_code  
    NetworkBackfillImpressions\_network\_code

### 聯播網點擊次數

Ad Manager 檔案：
[NetworkClicks](https://support.google.com/admanager/answer/1733124?hl=zh-tw)
和
[NetworkBackfillClicks](https://support.google.com/admanager/answer/1733124?hl=zh-tw)

BigQuery 資料表：
:   p\_NetworkClicks\_network\_code  
    p\_NetworkBackfillClicks\_network\_code

BigQuery 檢視畫面：
:   NetworkClicks\_network\_code  
    NetworkBackfillClicks\_network\_code

### 網路 Active View

Ad Manager 檔案：
[NetworkActiveViews](https://support.google.com/admanager/answer/1733124?hl=zh-tw)
和
[NetworkBackfillActiveViews](https://support.google.com/admanager/answer/1733124?hl=zh-tw)

BigQuery 資料表：
:   p\_NetworkActiveViews\_network\_code  
    p\_NetworkBackfillActiveViews\_network\_code

BigQuery 檢視畫面：
:   NetworkActiveViews\_network\_code  
    NetworkBackfillActiveViews\_network\_code

### 聯播網候補廣告出價

Ad Manager 檔案：
[NetworkBackfillBids](https://support.google.com/admanager/answer/1733124?hl=zh-tw)

BigQuery 資料表：
:   p\_NetworkBackfillBids\_network\_code

BigQuery 檢視畫面：
:   NetworkBackfillBids\_network\_code

### 聯播網影片轉換

Ad Manager 檔案：
[NetworkVideoConversions](https://support.google.com/admanager/answer/1733124?hl=zh-tw)
和
[NetworkBackfillVideoConversions](https://support.google.com/admanager/answer/1733124?hl=zh-tw)

BigQuery 資料表：
:   p\_NetworkVideoConversions\_network\_code  
    p\_NetworkBackfillVideoConversions\_network\_code

BigQuery 檢視畫面：
:   NetworkVideoConversions\_network\_code  
    NetworkBackfillVideoConversions\_network\_code

### 聯播網互動式多媒體轉換

Ad Manager 檔案：
[NetworkRichMediaConversions](https://support.google.com/admanager/answer/1733124?hl=zh-tw)
和
[NetworkBackfillRichMediaConversions](https://support.google.com/admanager/answer/1733124?hl=zh-tw)

BigQuery 資料表：
:   p\_NetworkRichMediaConversions\_network\_code  
    p\_NetworkBackfillRichMediaConversions\_network\_code

BigQuery 檢視畫面：
:   NetworkRichMediaConversions\_network\_code  
    NetworkBackfillRichMediaConversions\_network\_code

### 網路活動

Ad Manager 檔案：
[NetworkActivities](https://support.google.com/admanager/answer/1733124?hl=zh-tw)

BigQuery 資料表：
:   p\_NetworkActivities\_network\_code

BigQuery 檢視畫面：
:   NetworkActivities\_network\_code

## 對照表

下列各節的表格包含帳戶的屬性欄位和中繼資料。

### 廣告類別

Ad Manager 檔案：
[AdCategory](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableAdCategory\_network\_code

BigQuery 檢視畫面：
:   MatchTableAdCategory\_network\_code

### 廣告單元

Ad Manager 檔案：
[AdUnit](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableAdUnit\_network\_code

BigQuery 檢視畫面：
:   MatchTableAdUnit\_network\_code

### 目標對象區隔

Ad Manager 檔案：
[AudienceSegment](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableAudienceSegment\_network\_code

BigQuery 檢視畫面：
:   MatchTableAudienceSegment\_network\_code

### 目標對象區隔類別

Ad Manager 檔案：
[AudienceSegmentCategory](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableAudienceSegmentCategory\_network\_code

BigQuery 檢視畫面：
:   MatchTableAudienceSegmentCategory\_network\_code

### 頻寬群組

Ad Manager 檔案：
[BandwidthGroup](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableBandwidthGroup\_network\_code

BigQuery 檢視畫面：
:   MatchTableBandwidthGroup\_network\_code

### 瀏覽器

Ad Manager 檔案：
[瀏覽器](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableBrowser\_network\_code

BigQuery 檢視畫面：
:   MatchTableBrowser\_network\_code

### 瀏覽器語言

Ad Manager 檔案：
[BrowserLanguage](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableBrowserLanguage\_network\_code

BigQuery 檢視畫面：
:   MatchTableBrowserLanguage\_network\_code

### 公司

Ad Manager 檔案：
[公司](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableCompany\_network\_code

BigQuery 檢視畫面：
:   MatchTableCompany\_network\_code

### 裝置功能

Ad Manager 檔案：
[DeviceCapability](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableDeviceCapability\_network\_code

BigQuery 檢視畫面：
:   MatchTableDeviceCapability\_network\_code

### 裝置類別

Ad Manager 檔案：
[DeviceCategory](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableDeviceCategory\_network\_code

BigQuery 檢視畫面：
:   MatchTableDeviceCategory\_network\_code

### 裝置製造商

Ad Manager 檔案：
[DeviceManufacturer](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableDeviceManufacturer\_network\_code

BigQuery 檢視畫面：
:   MatchTableDeviceManufacturer\_network\_code

### 匯率 (已淘汰)

Ad Manager 檔案：
[ExchangeRate](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   無

BigQuery 檢視畫面：
:   無

### 指定地理區域

Ad Manager 檔案：
[GeoTarget](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableGeoTarget\_network\_code

BigQuery 檢視畫面：
:   MatchTableGeoTarget\_network\_code

### 委刊項

Ad Manager 檔案：
[LineItem](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableLineItem\_network\_code

BigQuery 檢視畫面：
:   MatchTableLineItem\_network\_code

### 行動電信業者

Ad Manager 檔案：
[MobileCarrier](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableMobileCarrier\_network\_code

BigQuery 檢視畫面：
:   MatchTableMobileCarrier\_network\_code

### 行動裝置

Ad Manager 檔案：
[MobileDevice](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableMobileDevice\_network\_code

BigQuery 檢視畫面：
:   MatchTableMobileDevice\_network\_code

### 行動裝置子型號

Ad Manager 檔案：
[MobileDeviceSubmodel](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableMobileDeviceSubmodel\_network\_code

BigQuery 檢視畫面：
:   MatchTableMobileDeviceSubmodel\_network\_code

### 作業系統

Ad Manager 檔案：
[OperatingSystem](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableOperatingSystem\_network\_code

BigQuery 檢視畫面：
:   MatchTableOperatingSystem\_network\_code

### 作業系統版本

Ad Manager 檔案：
[OperatingSystemVersion](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableOperatingSystemVersion\_network\_code

BigQuery 檢視畫面：
:   MatchTableOperatingSystemVersion\_network\_code

### 訂單

Ad Manager 檔案：
[訂單](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableOrder\_network\_code

BigQuery 檢視畫面：
:   MatchTableOrder\_network\_code

### 存放位置

Ad Manager 檔案：
[刊登位置](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTablePlacement\_network\_code

BigQuery 檢視畫面：
:   MatchTablePlacement\_network\_code

### 程式輔助買方

Ad Manager 檔案：
[ProgrammaticBuyer](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableProgrammaticBuyer\_network\_code

BigQuery 檢視畫面：
:   MatchTableProgrammaticBuyer\_network\_code

### 提案撤銷原因

Ad Manager 檔案：
[ProposalRetractionReason](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableProposalRetractionReason\_network\_code

BigQuery 檢視畫面：
:   MatchTableProposalRetractionReason\_network\_code

### 第三方公司

Ad Manager 檔案：
[ThirdPartyCompany](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableThirdPartyCompany\_network\_code

BigQuery 檢視畫面：
:   MatchTableThirdPartyCompany\_network\_code

### 時區

Ad Manager 檔案：
[TimeZone](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableTimeZone\_network\_code

BigQuery 檢視畫面：
:   MatchTableTimeZone\_network\_code

### 使用者

Ad Manager 檔案：
[使用者](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables)

BigQuery 資料表：
:   p\_MatchTableUser\_network\_code

BigQuery 檢視畫面：
:   MatchTableUser\_network\_code




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-06-18 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-06-18 (世界標準時間)。"],[],[]]