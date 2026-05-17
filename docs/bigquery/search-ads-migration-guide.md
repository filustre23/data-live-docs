Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Search Ads 360 遷移指南

Search Ads 360 連接器 (舊稱 *DoubleClick Search*) 會使用新的 [Search Ads 360 reporting API](https://developers.google.com/search-ads/reporting/overview?hl=zh-tw)。[舊版 Search Ads 360 報表 API](https://developers.google.com/search-ads/v2/how-tos/reporting?hl=zh-tw) 已不再支援，因此您應遷移 BigQuery 資料移轉服務工作流程，以便與新版 Search Ads 360 報表 API 相容。本文將說明新版 Search Ads 360 與舊版 Search Ads 360 的差異，並提供對應資訊，協助您將現有資源遷移至新版 Search Ads 360。

## Search Ads 360 的新功能

新版 Search Ads 360 Reporting API 提供多項變更，可能會影響您現有的 BigQuery 資料移轉服務工作流程。

### 帳戶結構

新版 Search Ads 360 報表 API 採用階層式架構，將帳戶區分為管理員帳戶、副管理員帳戶和客戶帳戶。詳情請參閱「[帳戶階層差異](https://support.google.com/sa360/answer/13633455?hl=zh-tw)」和「[關於管理員帳戶](https://support.google.com/sa360/answer/9158072?hl=zh-tw)」。

### ID 空間

新版 Search Ads 360 中的實體與舊版 Search Ads 360 的[ID 空間](https://developers.google.com/search-ads/v2/how-tos/reporting/id-mapping?hl=zh-tw)對應方式不同。如要瞭解舊 ID 和新 ID 之間的對應關係，請參閱「[ID 對應](#id_mapping)」一文。

### 以資源為基礎的報表

新版 Search Ads 360 API 資料模型採用資源導向資料模型，而舊版 Search Ads 360 API 則採用報表導向資料模型。新版 Search Ads 360 API 連接器會查詢 Search Ads 360 中的[資源](https://developers.google.com/search-ads/reporting/concepts/api-structure?hl=zh-tw#resources)，建立 BigQuery 資料表。如要進一步瞭解新版 Search Ads 360 API 中的資源結構，請參閱「[Search Ads 360 Reporting API 結構](https://developers.google.com/search-ads/reporting/concepts/api-structure?hl=zh-tw)」。

## 遷移移轉設定

目前沒有自動化方法可將現有的 Search Ads 360 轉移設定轉換為新版 Search Ads 360 Reporting API。您必須[建立新版 Search Ads 360 資料移轉](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#setup-data-transfer)，並使用新版 Search Ads 360 報表 API 做為資料來源。

## 查看對應資訊

請參閱下列對應資訊，將現有的 Search Ads 360 資源對應至新版 Search Ads 360 Reporting API。

### 報表對應

新版 Search Ads 360 報表以資源為依據，其結構與舊版 Search Ads 360 的報表不同。如需舊報表和新報表的完整對應項目，請參閱「[Search Ads 360 Reporting API 的報表對應項目](https://developers.google.com/search-ads/reporting/migrate/mappings/report-mappings?hl=zh-tw)」。

下表列出 BigQuery 資料移轉服務支援的資料表，以及用於產生資料表的查詢資源。

| 舊版 Search Ads 報表 | 新版搜尋廣告資源 | 新的 BigQuery 資料表名稱 |
| --- | --- | --- |
| [adGroup](https://developers.google.com/search-ads/v2/report-types/adGroup?hl=zh-tw) | [ad\_group](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group?hl=zh-tw) | p\_sa\_AdGroupStats\_customer\_id  p\_sa\_AdGroup\_customer\_id  p\_sa\_AdGroupDeviceStats\_customer\_id  p\_sa\_AdGroupConversionActionAndDeviceStats\_customer\_id |
| [ad](https://developers.google.com/search-ads/v2/report-types/ad?hl=zh-tw) | [ad\_group\_ad](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_ad?hl=zh-tw) | p\_sa\_AdConversionActionAndDeviceStats\_customer\_id  p\_sa\_AdDeviceStats\_customer\_id  p\_sa\_Ad\_customer\_id |
| 不適用 | [ad\_group\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_asset?hl=zh-tw) | p\_sa\_AdGroupAssetStats\_customer\_id  p\_sa\_AdGroupConversionActionAndAssetStats\_customer\_id |
| 不適用 | [ad\_group\_asset\_set](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_asset_set?hl=zh-tw) | p\_sa\_AdGroupAssetSet\_customer\_id |
| [adGroupTarget](https://developers.google.com/search-ads/v2/report-types/adGroupTarget?hl=zh-tw) | [ad\_group\_audience\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_audience_view?hl=zh-tw) | p\_sa\_AdGroupAudienceDeviceStats\_customer\_id  p\_sa\_AdGroupAudienceConversionActionAndDeviceStats\_customer\_id |
| [adGroupTarget](https://developers.google.com/search-ads/v2/report-types/adGroupTarget?hl=zh-tw) | [ad\_group\_criterion](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_criterion?hl=zh-tw) | p\_sa\_NegativeAdGroupCriterion\_customer\_id  p\_sa\_NegativeAdGroupKeyword\_customer\_id  p\_sa\_AdGroupCriterion\_customer\_id |
| [adGroupTarget](https://developers.google.com/search-ads/v2/report-types/adGroupTarget?hl=zh-tw) | [age\_range\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/age_range_view?hl=zh-tw) | p\_sa\_AgeRangeDeviceStats\_customer\_id  p\_sa\_AgeRangeConversionActionAndDeviceStats\_customer\_id |
| 不適用 | [asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/asset?hl=zh-tw) | p\_sa\_Asset\_customer\_id |
| [bidStrategy](https://developers.google.com/search-ads/v2/report-types/bidStrategy?hl=zh-tw) | [bidding\_strategy](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/bidding_strategy?hl=zh-tw) | p\_sa\_BidStrategy\_customer\_id  p\_sa\_BidStrategyStats\_customer\_id |
| [campaign](https://developers.google.com/search-ads/v2/report-types/campaign?hl=zh-tw) | [campaign](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign?hl=zh-tw) | p\_sa\_CampaignConversionActionAndDeviceStats\_customer\_id  p\_sa\_Campaign\_customer\_id  p\_sa\_CampaignDeviceStats\_customer\_id  p\_sa\_CampaignStats\_customer\_id |
| 不適用 | [campaign\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign_asset?hl=zh-tw) | p\_sa\_CampaignAssetStats\_customer\_id  p\_sa\_CampaignConversionActionAndAssetStats\_customer\_id |
| 不適用 | [campaign\_asset\_set](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign_asset_set?hl=zh-tw) | p\_sa\_CampaignAssetSet\_customer\_id |
| [campaignTarget](https://developers.google.com/search-ads/v2/report-types/campaignTarget?hl=zh-tw) | [campaign\_audience\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign_audience_view?hl=zh-tw) | p\_sa\_CampaignAudienceConversionActionAndDeviceStats\_customer\_id  p\_sa\_CampaignAudienceDeviceStats\_customer\_id |
| [campaignTarget](https://developers.google.com/search-ads/v2/report-types/campaignTarget?hl=zh-tw) | [campaign\_criterion](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign_criterion?hl=zh-tw) | p\_sa\_CampaignCriterion\_customer\_id  p\_sa\_NegativeCampaignKeyword\_customer\_id  p\_sa\_NegativeCampaignCriterion\_customer\_id |
| [productLeadAndCrossSell](https://developers.google.com/search-ads/v2/report-types/productLeadAndCrossSell?hl=zh-tw) | [cart\_data\_sales\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/cart_data_sales_view?hl=zh-tw) | p\_sa\_CartDataSalesStats\_customer\_id |
| [轉換](https://developers.google.com/search-ads/v2/report-types/conversion?hl=zh-tw) | [轉換](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/conversion?hl=zh-tw) | p\_sa\_Conversion\_customer\_id |
| [floodlightActivity](https://developers.google.com/search-ads/v2/report-types/floodlightActivity?hl=zh-tw) | [conversion\_action](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/conversion_action?hl=zh-tw) | p\_sa\_ConversionAction\_customer\_id |
| [帳戶](https://developers.google.com/search-ads/v2/report-types/account?hl=zh-tw) | [customer](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/customer?hl=zh-tw) | p\_sa\_Account\_customer\_id  p\_sa\_AccountDeviceStats\_customer\_id  p\_sa\_AccountConversionActionAndDeviceStats\_customer\_id  p\_sa\_AccountStats\_customer\_id |
| 不適用 | [customer\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/customer_asset?hl=zh-tw) | p\_sa\_CustomerAssetStats\_customer\_id  p\_sa\_CustomerConversionActionAndAssetStats\_customer\_id |
| 不適用 | [customer\_asset\_set](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/customer_asset_set?hl=zh-tw) | p\_sa\_CustomerAssetSet\_customer\_id |
| [adGroupTarget](https://developers.google.com/search-ads/v2/report-types/adGroupTarget?hl=zh-tw) | [gender\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/gender_view?hl=zh-tw) | p\_sa\_GenderDeviceStats\_customer\_id  p\_sa\_GenderConversionActionAndDeviceStats\_customer\_id |
| [關鍵字](https://developers.google.com/search-ads/v2/report-types/keyword?hl=zh-tw) | [keyword\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/keyword_view?hl=zh-tw) | p\_sa\_Keyword\_customer\_id  p\_sa\_KeywordDeviceStats\_customer\_id  p\_sa\_KeywordStats\_customer\_id  p\_sa\_KeywordConversionActionAndDeviceStats\_customer\_id |
| [adGroupTarget](https://developers.google.com/search-ads/v2/report-types/adGroupTarget?hl=zh-tw) | [location\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/location_view?hl=zh-tw) | p\_sa\_LocationDeviceStats\_customer\_id  p\_sa\_LocationConversionActionAndDeviceStats\_customer\_id |
| [productAdvertised](https://developers.google.com/search-ads/v2/report-types/productAdvertised?hl=zh-tw) | [shopping\_performance\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/shopping_performance_view?hl=zh-tw) | p\_sa\_ProductAdvertised\_customer\_id  p\_sa\_ProductAdvertisedConversionActionAndDeviceStats\_customer\_id  p\_sa\_ProductAdvertisedDeviceStats\_customer\_id |
| [productGroup](https://developers.google.com/search-ads/v2/report-types/productGroup?hl=zh-tw) | [product\_group\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/product_group_view?hl=zh-tw) | p\_sa\_ProductGroupStats\_customer\_id  p\_sa\_ProductGroup\_customer\_id |
| [訪問](https://developers.google.com/search-ads/v2/report-types/visit?hl=zh-tw) | [訪問](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/visit?hl=zh-tw) | p\_sa\_Visit\_customer\_id |
| [adGroupTarget](https://developers.google.com/search-ads/v2/report-types/adGroupTarget?hl=zh-tw) | [webpage\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/webpage_view?hl=zh-tw) | p\_sa\_WebpageDeviceStats\_customer\_id  p\_sa\_WebpageConversionActionAndDeviceStats\_customer\_id |

### 欄位對應

BigQuery 資料移轉服務支援部分 Search Ads 360 報表欄位，如「[Search Ads 360 報表轉換](https://docs.cloud.google.com/bigquery/docs/search-ads-transformation?hl=zh-tw)」一文所列。BigQuery 不支援資料欄名稱中的 `.`，因此所有轉移的報表都會將 `.` 替換為 `_`。舉例來說，Search Ads 360 資源中的 `ad_group_ad.ad.text_ad.description1` 欄位會以 `ad_group_ad_ad_text_ad_description1` 的形式轉移至 BigQuery。

### ID 對應

新版 Search Ads 360 中的實體 (例如客戶、廣告活動和廣告群組) 的 [ID 空間](https://developers.google.com/search-ads/v2/how-tos/reporting/id-mapping?hl=zh-tw)與舊版 Search Ads 360 不同。如要進一步瞭解新版 Search Ads 360 的 ID 對應表，請參閱「[ID 對應表](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#id-mapping)」。

## 遷移查詢的範例

以下範例說明 BigQuery 查詢在對應至新 Search Ads 360 報表 API 前後的樣貌。

請參考以下查詢範例，瞭解如何使用舊版 Search Ads 360 報表 API 分析過去 30 天的 Search Ads 廣告活動成效。

```
SELECT
  c.accountId,
  c.campaign,
  C.status,
  SUM(cs.impr) AS Impressions,
  SUM(cs.clicks) AS Clicks,
  (SUM(cs.cost) / 1000000) AS Cost
FROM
  `previous_dataset.Campaign_advertiser_id` c
LEFT JOIN
  `previous_dataset.CampaignStats_advertiser_id` cs
ON
  (c.campaignId = cs.campaignId
  AND cs._DATA_DATE BETWEEN
  DATE_ADD(CURRENT_DATE(), INTERVAL -31 DAY) AND DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY))
WHERE
  c._DATA_DATE = c._LATEST_DATE
GROUP BY
  1, 2, 3
ORDER BY
  Impressions DESC
```

當對應項目與新版 Search Ads 360 報表 API 相容時，同一個查詢會轉換為下列內容：

```
SELECT
  c.customer_id,
  c.campaign_name,
  C.campaign_status,
  SUM(cs.metrics_impressions) AS Impressions,
  SUM(cs.metrics_clicks) AS Clicks,
  (SUM(cs.metrics_cost_micros) / 1000000) AS Cost
FROM
  `new_dataset.sa_Campaign_customer_id` c
LEFT JOIN
  `new_dataset.sa_CampaignStats_customer_id` cs
ON
  (c.campaign_id = cs.campaign_id
  AND cs._DATA_DATE BETWEEN
  DATE_ADD(CURRENT_DATE(), INTERVAL -31 DAY) AND DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY))
WHERE
  c._DATA_DATE = c._LATEST_DATE
GROUP BY
  1, 2, 3
ORDER BY
  Impressions DESC
```

如要查看更多與新版 Search Ads 360 相容的查詢示例，請參閱「[查詢示例](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw#example_queries)」。

## 後續步驟

* 如要瞭解如何安排及管理 Search Ads 360 的週期性載入工作，請參閱「[Search Ads 360 移轉作業](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw)」。
* 如要瞭解如何轉換 Search Ads 360 報表，請參閱「[Search Ads 360 報表轉換](https://docs.cloud.google.com/bigquery/docs/search-ads-transformation?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]