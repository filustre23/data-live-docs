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

當您的 Google Ad Manager (原名為 DoubleClick for Publishers) 資料移轉檔案移轉到 BigQuery 時，檔案會轉換成下列 BigQuery 表格和視圖。

在 BigQuery 中查看表格和視圖時，network\_code 的值是 Google Ad Manager 網路代碼。

| **Google Ad Manager 檔案** | **BigQuery 資料表** | **BigQuery 檢視表** |
| --- | --- | --- |
| **資料移轉檔案** |  |  |
| [NetworkRequests NetworkBackfillRequests](https://support.google.com/admanager/answer/1733124?hl=zh-tw) | p\_NetworkRequests\_network\_code p\_NetworkBackfillRequests\_network\_code | NetworkRequests\_network\_code NetworkBackfillRequests\_network\_code |
| [NetworkCodeServes NetworkBackfillCodeServes](https://support.google.com/admanager/answer/1733124?hl=zh-tw) | p\_NetworkCodeServes p\_NetworkBackfillCodeServes\_network\_code | NetworkCodeServes NetworkBackfillCodeServes\_network\_code |
| [NetworkImpressions NetworkBackfillImpressions](https://support.google.com/admanager/answer/1733124?hl=zh-tw) | p\_NetworkImpressions\_network\_code p\_NetworkBackfillImpressions\_network\_code | NetworkImpressions\_network\_code NetworkBackfillImpressions\_network\_code |
| [NetworkClicks NetworkBackfillClicks](https://support.google.com/admanager/answer/1733124?hl=zh-tw) | p\_NetworkClicks\_network\_code p\_NetworkBackfillClicks\_network\_code | NetworkClicks\_network\_code NetworkBackfillClicks\_network\_code |
| [NetworkActiveViews NetworkBackfillActiveViews](https://support.google.com/admanager/answer/1733124?hl=zh-tw) | p\_NetworkActiveViews\_network\_code p\_NetworkBackfillActiveViews\_network\_code | NetworkActiveViews\_network\_code NetworkBackfillActiveViews\_network\_code |
| [NetworkBackfillBids](https://support.google.com/admanager/answer/1733124?hl=zh-tw) | p\_NetworkBackfillBids\_network\_code | NetworkBackfillBids\_network\_code |
| [NetworkVideoConversions NetworkBackfillVideoConversions](https://support.google.com/admanager/answer/1733124?hl=zh-tw) | p\_NetworkVideoConversions\_network\_code p\_NetworkBackfillVideoConversions\_network\_code | NetworkVideoConversions\_network\_code NetworkBackfillVideoConversions\_network\_code |
| [NetworkRichMediaConversions NetworkBackfillRichMediaConversions](https://support.google.com/admanager/answer/1733124?hl=zh-tw) | p\_NetworkRichMediaConversions\_network\_code p\_NetworkBackfillRichMediaConversions\_network\_code | NetworkRichMediaConversions\_network\_code NetworkBackfillRichMediaConversions\_network\_code |
| [NetworkActivities](https://support.google.com/admanager/answer/1733124?hl=zh-tw) | p\_NetworkActivities\_network\_code | NetworkActivities\_network\_code |
| **比對資料表** |  |  |
| [AdCategory](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableAdCategory\_network\_code | MatchTableAdCategory\_network\_code |
| [AdUnit](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableAdUnit\_network\_code | MatchTableAdUnit\_network\_code |
| [AudienceSegment](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableAudienceSegment\_network\_code | MatchTableAudienceSegment\_network\_code |
| [AudienceSegmentCategory](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableAudienceSegmentCategory\_network\_code | MatchTableAudienceSegmentCategory\_network\_code |
| [BandwidthGroup](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableBandwidthGroup\_network\_code | MatchTableBandwidthGroup\_network\_code |
| [瀏覽器](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableBrowser\_network\_code | MatchTableBrowser\_network\_code |
| [BrowserLanguage](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableBrowserLanguage\_network\_code | MatchTableBrowserLanguage\_network\_code |
| [Company](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableCompany\_network\_code | MatchTableCompany\_network\_code |
| [DeviceCapability](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableDeviceCapability\_network\_code | MatchTableDeviceCapability\_network\_code |
| [DeviceCategory](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableDeviceCategory\_network\_code | MatchTableDeviceCategory\_network\_code |
| [DeviceManufacturer](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableDeviceManufacturer\_network\_code | MatchTableDeviceManufacturer\_network\_code |
| [ExchangeRate](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) (已淘汰) | - | - |
| [GeoTarget](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableGeoTarget\_network\_code | MatchTableGeoTarget\_network\_code |
| [LineItem](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableLineItem\_network\_code | MatchTableLineItem\_network\_code |
| [MobileCarrier](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableMobileCarrier\_network\_code | MatchTableMobileCarrier\_network\_code |
| [MobileDevice](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableMobileDevice\_network\_code | MatchTableMobileDevice\_network\_code |
| [MobileDeviceSubmodel](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableMobileDeviceSubmodel\_network\_code | MatchTableMobileDeviceSubmodel\_network\_code |
| [OperatingSystem](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableOperatingSystem\_network\_code | MatchTableOperatingSystem\_network\_code |
| [OperatingSystemVersion](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableOperatingSystemVersion\_network\_code | MatchTableOperatingSystemVersion\_network\_code |
| [訂單](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableOrder\_network\_code | MatchTableOrder\_network\_code |
| [刊登位置](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTablePlacement\_network\_code | MatchTablePlacement\_network\_code |
| [ProgrammaticBuyer](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableProgrammaticBuyer\_network\_code | MatchTableProgrammaticBuyer\_network\_code |
| [ProposalRetractionReason](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableProposalRetractionReason\_network\_code | MatchTableProposalRetractionReason\_network\_code |
| [ThirdPartyCompany](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableThirdPartyCompany\_network\_code | MatchTableThirdPartyCompany\_network\_code |
| [TimeZone](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableTimeZone\_network\_code | MatchTableTimeZone\_network\_code |
| [User](https://developers.google.com/doubleclick-publishers/docs/pqlreference?hl=zh-tw#matchtables) | p\_MatchTableUser\_network\_code | MatchTableUser\_network\_code |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]