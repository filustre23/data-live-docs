Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Search Ads 360 報表轉換

本文說明如何轉換 Search Ads 360 的報表。

如要查看使用舊版 Search Ads 360 Reporting API 的 Search Ads 360 報表轉換，請參閱「[Search Ads 360 報表轉換 (已淘汰)](https://docs.cloud.google.com/bigquery/docs/sa360-transformation?hl=zh-tw)」。

## Search Ads 360 報表的表格對應

當您的 Search Ads 360 報表移轉至 BigQuery 時，報表會轉換成下列 BigQuery 資料表和檢視表。在 BigQuery 中檢視資料表和檢視表時，customer\_id 的值是您的 Search Ads 360 客戶 ID。

### ad\_group

[ad\_group](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group?hl=zh-tw)

表格：
:   p\_sa\_AdGroup\_customer\_id  
    p\_sa\_AdGroupConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_AdGroupDeviceStats\_customer\_id  
    p\_sa\_AdGroupStats\_customer\_id

觀看次數：
:   sa\_AdGroup\_customer\_id  
    sa\_AdGroupConversionActionAndDeviceStats\_customer\_id  
    sa\_AdGroupDeviceStats\_customer\_id  
    sa\_AdGroupStats\_customer\_id

### ad\_group\_ad

[ad\_group\_ad](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_ad?hl=zh-tw)

表格：
:   p\_sa\_Ad\_customer\_id  
    p\_sa\_AdConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_AdDeviceStats\_customer\_id

觀看次數：
:   a\_Ad\_customer\_id  
    sa\_AdConversionActionAndDeviceStats\_customer\_id  
    sa\_AdDeviceStats\_customer\_id

### ad\_group\_asset

[ad\_group\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_asset?hl=zh-tw)

表格：
:   p\_sa\_AdGroupAssetStats\_customer\_id  
    p\_sa\_AdGroupConversionActionAndAssetStats\_customer\_id

觀看次數：
:   sa\_AdGroupAssetStats\_customer\_id  
    sa\_AdGroupConversionActionAndAssetStats\_customer\_id

### ad\_group\_audience\_view

[ad\_group\_audience\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_audience_view?hl=zh-tw)

表格：
:   p\_sa\_AdGroupAudienceConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_AdGroupAudienceDeviceStats\_customer\_id

觀看次數：
:   sa\_AdGroupAudienceConversionActionAndDeviceStats\_customer\_id  
    sa\_AdGroupAudienceDeviceStats\_customer\_id

### ad\_group\_criterion

[ad\_group\_criterion](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_criterion?hl=zh-tw)

表格：
:   p\_sa\_AdGroupCriterion\_customer\_id  
    p\_sa\_NegativeAdGroupCriterion\_customer\_id  
    p\_sa\_NegativeAdGroupKeyword\_customer\_id

觀看次數：
:   sa\_AdGroupCriterion\_customer\_id  
    sa\_NegativeAdGroupCriterion\_customer\_id  
    sa\_NegativeAdGroupKeyword\_customer\_id

### ad\_group\_label

[ad\_group\_label](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_label?hl=zh-tw)

表格：
:   p\_sa\_AdGroupLabel\_customer\_id

觀看次數：
:   sa\_AdGroupLabel\_customer\_id

### age\_range\_view

[age\_range\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/age_range_view?hl=zh-tw)

表格：
:   p\_sa\_AgeRangeConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_AgeRangeDeviceStats\_customer\_id

觀看次數：
:   sa\_AgeRangeConversionActionAndDeviceStats\_customer\_id  
    sa\_AgeRangeDeviceStats\_customer\_id

### 資產

[asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/asset?hl=zh-tw)

表格：
:   p\_sa\_Asset\_customer\_id

觀看次數：
:   sa\_Asset\_customer\_id

### asset\_set\_asset

[asset\_set\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/asset_set_asset?hl=zh-tw)

表格：
:   p\_sa\_AccountConversionActionAndAssetStats\_customer\_id  
    p\_sa\_AssetSetStats\_customer\_id

觀看次數：
:   sa\_AccountConversionActionAndAssetStats\_customer\_id  
    sa\_AssetSetStats\_customer\_id

### bidding\_strategy

[bidding\_strategy](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/bidding_strategy?hl=zh-tw)

表格：
:   p\_sa\_BidStrategy\_customer\_id  
    p\_sa\_BidStrategyStats\_customer\_id

觀看次數：
:   sa\_BidStrategy\_customer\_id  
    sa\_BidStrategyStats\_customer\_id

### 廣告活動

[廣告活動](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign?hl=zh-tw)

表格：
:   p\_sa\_Campaign\_customer\_id  
    p\_sa\_CampaignConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_CampaignDeviceStats\_customer\_id  
    p\_sa\_CampaignStats\_customer\_id

觀看次數：
:   sa\_Campaign\_customer\_id  
    sa\_CampaignConversionActionAndDeviceStats\_customer\_id  
    sa\_CampaignDeviceStats\_customer\_id  
    sa\_CampaignStats\_customer\_id

### campaign\_asset

[campaign\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign_asset?hl=zh-tw)

表格：
:   p\_sa\_CampaignAssetStats\_customer\_id  
    p\_sa\_CampaignConversionActionAndAssetStats\_customer\_id

觀看次數：
:   sa\_CampaignAssetStats\_customer\_id  
    sa\_CampaignConversionActionAndAssetStats\_customer\_id

### campaign\_audience\_view

[campaign\_audience\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign_audience_view?hl=zh-tw)

表格：
:   p\_sa\_CampaignAudienceConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_CampaignAudienceDeviceStats\_customer\_id

觀看次數：
:   sa\_CampaignAudienceConversionActionAndDeviceStats\_customer\_id  
    sa\_CampaignAudienceDeviceStats\_customer\_id

### campaign\_criterion

[campaign\_criterion](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign_criterion?hl=zh-tw)

表格：
:   p\_sa\_CampaignCriterion\_customer\_id  
    p\_sa\_NegativeCampaignCriterion\_customer\_id  
    p\_sa\_NegativeCampaignKeyword\_customer\_id

觀看次數：
:   sa\_CampaignCriterion\_customer\_id  
    sa\_NegativeCampaignCriterion\_customer\_id  
    sa\_NegativeCampaignKeyword\_customer\_id

### campaign\_label

[campaign\_label](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign_label?hl=zh-tw)

表格：
:   p\_sa\_CampaignLabel\_customer\_id

觀看次數：
:   sa\_CampaignLabel\_customer\_id

### cart\_data\_sales\_view

[cart\_data\_sales\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/cart_data_sales_view?hl=zh-tw)

表格：
:   p\_sa\_CartDataSalesStats\_customer\_id

觀看次數：
:   sa\_CartDataSalesStats\_customer\_id

### 轉換

[轉換](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/conversion?hl=zh-tw)

表格：
:   p\_sa\_Conversion\_customer\_id

觀看次數：
:   sa\_Conversion\_customer\_id

### conversion\_action

[conversion\_action](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/conversion_action?hl=zh-tw)

表格：
:   p\_sa\_ConversionAction\_customer\_id

觀看次數：
:   sa\_ConversionAction\_customer\_id

### 客戶

[顧客](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/customer?hl=zh-tw)

表格：
:   p\_sa\_Account\_customer\_id  
    p\_sa\_AccountConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_AccountDeviceStats\_customer\_id  
    p\_sa\_AccountStats\_customer\_id

觀看次數：
:   sa\_Account\_customer\_id  
    sa\_AccountConversionActionAndDeviceStats\_customer\_id  
    sa\_AccountDeviceStats\_customer\_id  
    sa\_AccountStats\_customer\_id

### customer\_asset

[customer\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/customer_asset?hl=zh-tw)

表格：
:   p\_sa\_AccountAssetStats\_customer\_id

觀看次數：
:   sa\_AccountAssetStats\_customer\_id

### gender\_view

[gender\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/gender_view?hl=zh-tw)

表格：
:   p\_sa\_GenderConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_GenderDeviceStats\_customer\_id

觀看次數：
:   sa\_GenderConversionActionAndDeviceStats\_customer\_id  
    sa\_GenderDeviceStats\_customer\_id

### keyword\_view

[keyword\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/keyword_view?hl=zh-tw)

表格：
:   p\_sa\_Keyword\_customer\_id  
    p\_sa\_KeywordConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_KeywordDeviceStats\_customer\_id  
    p\_sa\_KeywordStats\_customer\_id

觀看次數：
:   sa\_Keyword\_customer\_id  
    sa\_KeywordConversionActionAndDeviceStats\_customer\_id  
    sa\_KeywordDeviceStats\_customer\_id  
    sa\_KeywordStats\_customer\_id

### location\_view

[location\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/location_view?hl=zh-tw)

表格：
:   p\_sa\_LocationConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_LocationDeviceStats\_customer\_id

觀看次數：
:   sa\_LocationConversionActionAndDeviceStats\_customer\_id  
    sa\_LocationDeviceStats\_customer\_id

### product\_group\_view

[product\_group\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/product_group_view?hl=zh-tw)

表格：
:   p\_sa\_ProductGroup\_customer\_id  
    p\_sa\_ProductGroupStats\_customer\_id

觀看次數：
:   sa\_ProductGroup\_customer\_id  
    sa\_ProductGroupStats\_customer\_id

### shopping\_performance\_view

[shopping\_performance\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/shopping_performance_view?hl=zh-tw)

表格：
:   p\_sa\_ProductAdvertised\_customer\_id  
    p\_sa\_ProductAdvertisedConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_ProductAdvertisedDeviceStats\_customer\_id

觀看次數：
:   sa\_ProductAdvertised\_customer\_id  
    sa\_ProductAdvertisedConversionActionAndDeviceStats\_customer\_id  
    sa\_ProductAdvertisedDeviceStats\_customer\_id

### 拜訪

[造訪](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/visit?hl=zh-tw)

表格：
:   p\_sa\_Visit\_customer\_id

觀看次數：
:   sa\_Visit\_customer\_id

### webpage\_view

[webpage\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/webpage_view?hl=zh-tw)

表格：
:   p\_sa\_WebpageConversionActionAndDeviceStats\_customer\_id  
    p\_sa\_WebpageDeviceStats\_customer\_id

觀看次數：
:   sa\_WebpageConversionActionAndDeviceStats\_customer\_id  
    sa\_WebpageDeviceStats\_customer\_id

## Search Ads 360 報表的資料欄詳細資料

Search Ads 360 移轉作業建立的 BigQuery 資料表是由下列資料欄 (欄位) 組成：

Search Ads 360 表格名稱：帳戶

Search Ads 360 API 資源：[customer](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/customer?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| customer\_account\_level | 客戶的帳戶層級：管理員、副管理員、助理管理員或服務帳戶。 |
| customer\_account\_type | 引擎帳戶類型。例如：Google Ads、Microsoft Advertising、Yahoo Japan、百度、Facebook、Engine Track。 |
| customer\_creation\_time | 建立這個顧客的時間戳記。時間戳記採用客戶時區，格式為「yyyy-MM-dd HH:mm:ss」。 |
| customer\_currency\_code | 帳戶使用的幣別。系統支援 ISO 4217 標準的部分貨幣代碼。 |
| customer\_descriptive\_name | 選填，客戶的說明名稱 (可重複)。 |
| customer\_manager\_descriptive\_name | 管理員的描述性名稱。 |
| customer\_sub\_manager\_descriptive\_name | 副管理員的描述性名稱。 |
| customer\_associate\_manager\_descriptive\_name | 關聯管理員的描述性名稱。 |
| customer\_engine\_id | 外部引擎帳戶中的帳戶 ID。 |
| customer\_id | 顧客 ID。 |
| customer\_manager\_id | 管理員的客戶 ID。 |
| customer\_sub\_manager\_id | 副管理員的客戶 ID。 |
| customer\_associate\_manager\_id | 助理管理員的客戶 ID。 |
| customer\_last\_modified\_time | 上次修改這個客戶的日期和時間。日期時間採用客戶時區，格式為「yyyy-MM-dd HH:mm:ss.ssssss」。 |
| customer\_status | 顧客狀態。 |
| customer\_time\_zone | 顧客的當地時區 ID。 |

Search Ads 360 表格名稱：AccountAssetStats

Search Ads 360 API 資源：[customer\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/customer_asset?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| customer\_asset\_asset | 這是必要旗標，不可變動。與客戶連結的資產。 |
| customer\_id | 顧客 ID。 |
| metrics\_average\_cpc | 所有點擊的總費用除以獲得的點擊總次數。 |
| metrics\_average\_cpm | 平均千次曝光出價。 |
| metrics\_clicks | 點擊次數。 |
| metrics\_client\_account\_conversions | 客戶帳戶轉換次數。只有 include\_in\_client\_account\_conversions\_metric 屬性設為 true 的轉換動作，才會納入這項指標。如果您使用以轉換為主的出價策略，系統會調整出價策略來爭取這些轉換。 |
| metrics\_client\_account\_conversions\_value | 客戶帳戶轉換的價值。只有 include\_in\_client\_account\_conversions\_metric 屬性設為 true 的轉換動作，才會納入這項指標。如果您使用以轉換為主的出價策略，系統會調整出價策略來爭取這些轉換。 |
| metrics\_cost\_micros | 這段期間的單次點擊出價和千次曝光出價費用總和。 |
| metrics\_ctr | 廣告獲得的點擊次數 (點擊次數) 除以廣告顯示次數 (曝光次數)。 |
| metrics\_impressions | 廣告顯示在搜尋結果網頁或 Google 聯播網網站上的次數。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17 |

Search Ads 360 表格名稱：AccountConversionActionAndAssetStats

Search Ads 360 API 資源：[asset\_set\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/asset_set_asset?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| asset\_set\_asset\_asset | 不可變動。這個素材資源組合素材資源連結的素材資源。 |
| asset\_set\_asset\_asset\_set | 不可變動。這個素材資源組合素材資源連結的素材資源組合。 |
| customer\_id | 顧客 ID。 |
| metrics\_all\_conversions | 轉換總次數。包括所有轉換，不論 include\_in\_conversions\_metric 的值為何。 |
| metrics\_all\_conversions\_value | 所有轉換的價值。 |
| metrics\_cross\_device\_conversions | 顧客在某裝置上點按廣告，然後使用其他裝置或瀏覽器完成轉換。所有轉換次數中已納入跨裝置轉換。 |
| metrics\_cross\_device\_conversions\_value | 跨裝置轉換價值的總和。 |
| segments.conversion\_action\_name | 轉換動作名稱。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17 |

Search Ads 360 表格名稱：AccountConversionActionAndDeviceStats

Search Ads 360 API 資源：[customer](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/customer?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| customer\_engine\_id | 外部引擎帳戶中的帳戶 ID。 |
| customer\_id | 顧客 ID。 |
| metrics\_all\_conversions | 轉換總次數。包括所有轉換，不論 include\_in\_conversions\_metric 的值為何。 |
| metrics\_all\_conversions\_value | 所有轉換的價值。 |
| metrics\_cross\_device\_conversions | 顧客在某裝置上點按廣告，然後使用其他裝置或瀏覽器完成轉換。所有轉換次數中已納入跨裝置轉換。 |
| metrics\_cross\_device\_conversions\_value | 跨裝置轉換價值的總和。 |
| segments.conversion\_action\_name | 轉換動作名稱。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17 |
| segments\_device | 指標適用的裝置。 |

Search Ads 360 表格名稱：AccountDeviceStats

Search Ads 360 API 資源：[customer](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/customer?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| customer\_engine\_id | 外部引擎帳戶中的帳戶 ID。 |
| customer\_id | 顧客 ID。 |
| metrics\_average\_cpc | 所有點擊的總費用除以獲得的點擊總次數。 |
| metrics\_average\_cpm | 平均千次曝光出價。 |
| metrics\_clicks | 點擊次數。 |
| metrics\_client\_account\_conversions | 客戶帳戶轉換次數。只有 include\_in\_client\_account\_conversions\_metric 屬性設為 true 的轉換動作，才會納入這項指標。如果您使用以轉換為主的出價策略，系統會調整出價策略來爭取這些轉換。 |
| metrics\_client\_account\_conversions\_value | 客戶帳戶轉換的價值。只有 include\_in\_client\_account\_conversions\_metric 屬性設為 true 的轉換動作，才會納入這項指標。如果您使用以轉換為主的出價策略，系統會調整出價策略來爭取這些轉換。 |
| metrics\_client\_account\_view\_through\_conversions | 瀏覽後轉換總次數。如果顧客看到圖片或多媒體廣告，但未與其他廣告互動 (例如點擊)，之後在您的網站上完成轉換，就會計為瀏覽後轉換。 |
| metrics\_cost\_micros | 這段期間的單次點擊出價和千次曝光出價費用總和。 |
| metrics\_ctr | 廣告獲得的點擊次數 (點擊次數) 除以廣告顯示次數 (曝光次數)。 |
| metrics\_impressions | 廣告顯示在搜尋結果網頁或 Google 聯播網網站上的次數。 |
| metrics\_visits | Search Ads 360 成功記錄並轉送至廣告主到達網頁的點擊次數。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17 |
| segments\_device | 指標適用的裝置。 |

Search Ads 360 表格名稱：AccountStats

Search Ads 360 API 資源：[customer](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/customer?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| customer\_engine\_id | 外部引擎帳戶中的帳戶 ID。 |
| customer\_id | 顧客 ID。 |
| metrics\_content\_budget\_lost\_impression\_share | 廣告符合在搜尋聯播網上顯示的資格，但因預算過低而未顯示的次數百分比 (估計值)。注意：搜尋預算錯失的曝光比重會以 0 到 0.9 的範圍回報。任何大於 0.9 的值都會回報為 0.9001。 |
| metrics\_content\_impression\_share | 將您在多媒體廣告聯播網上獲得的曝光次數，除以預估可獲得的曝光次數後所得出的百分比。注意：內容曝光比重的範圍為 0.1 到 1。低於 0.1 的值會回報為 0.0999。 |
| metrics\_content\_rank\_lost\_impression\_share | 廣告因為廣告評級偏低，而錯失多媒體廣告聯播網曝光次數的預估百分比。注意：內容排名錯失的曝光比重會回報在 0 到 0.9 的範圍內。任何大於 0.9 的值都會回報為 0.9001。 |
| metrics\_historical\_quality\_score | 歷來品質分數。 |
| metrics\_search\_budget\_lost\_impression\_share | 廣告符合在搜尋聯播網上顯示的資格，但因預算過低而未顯示的次數百分比 (估計值)。注意：搜尋預算錯失的曝光比重會以 0 到 0.9 的範圍回報。任何大於 0.9 的值都會回報為 0.9001。 |
| metrics\_search\_impression\_share | 此欄是將您在搜尋聯播網上獲得的曝光次數，除以預估可獲得的曝光次數後，所得到的百分比。注意：搜尋曝光比重的報表範圍為 0.1 至 1。低於 0.1 的值會回報為 0.0999。 |
| metrics\_search\_rank\_lost\_impression\_share | 廣告因為廣告評級偏低，而無法在搜尋聯播網上獲得的預估曝光次數百分比。注意：搜尋聯播網錯失的曝光比重 (排名) 範圍為 0 至 0.9。任何大於 0.9 的值都會回報為 0.9001。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17 |

Search Ads 360 表格名稱：廣告

Search Ads 360 API 資源：[ad\_group\_ad](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_ad?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| ad\_group\_ad\_ad\_display\_url | 部分廣告格式的廣告說明中顯示的網址。 |
| ad\_group\_ad\_ad\_expanded\_dynamic\_search\_ad\_description1 | 廣告內容描述的第一行。 |
| ad\_group\_ad\_ad\_expanded\_dynamic\_search\_ad\_description2 | 廣告說明的第二行。 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_description1 | 廣告內容描述的第一行。 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_description2 | 廣告說明的第二行。 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_headline | 廣告標題。 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_headline2 | 廣告的第二個標題。 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_headline3 | 廣告的第三個標題。 |
| ad\_group\_ad\_ad\_final\_urls | 廣告完成所有跨網域重新導向後，可能連到的最終到達網址清單。 |
| ad\_group\_ad\_ad\_id | 廣告的 ID。 |
| ad\_group\_ad\_ad\_name | 廣告的名稱。這項資訊僅用於識別廣告。這個值不必是專屬值，也不會影響放送的廣告。名稱欄位僅支援 DisplayUploadAd、ImageAd、ShoppingComparisonListingAd 和 VideoAd。 |
| ad\_group\_ad\_ad\_text\_ad\_description1 | 廣告內容描述的第一行。 |
| ad\_group\_ad\_ad\_text\_ad\_description2 | 廣告說明的第二行。 |
| ad\_group\_ad\_ad\_text\_ad\_headline | 廣告標題。 |
| ad\_group\_ad\_ad\_type | 廣告類型。 |
| ad\_group\_ad\_creation\_time | 建立這個廣告群組廣告的時間戳記。日期時間採用客戶時區，格式為「yyyy-MM-dd HH:mm:ss.ssssss」。 |
| ad\_group\_ad\_engine\_id | 外部引擎帳戶中的廣告 ID。這個欄位僅適用於 Search Ads 360 帳戶。例如：Yahoo Japan、Microsoft、百度。如為非 Search Ads 360 實體，請改用「ad\_group\_ad.ad.id」。 |
| ad\_group\_ad\_engine\_status | 外部引擎帳戶中廣告的額外狀態。可能狀態 (視外部帳戶類型而定) 包括有效、符合資格、待審查。 |
| ad\_group\_ad\_labels | 附加至這個廣告群組廣告的標籤資源名稱。 |
| ad\_group\_ad\_last\_modified\_time | 上次修改這個廣告群組廣告的日期時間。日期時間採用客戶時區，格式為「yyyy-MM-dd HH:mm:ss.ssssss」。 |
| ad\_group\_ad\_status | 廣告的狀態。 |
| ad\_group\_id | 廣告群組 ID。 |
| campaign\_id | 廣告活動的 ID。 |
| customer\_id | 顧客 ID。 |

Search Ads 360 表格名稱：AdConversionActionAndDeviceStats

Search Ads 360 API 資源：[ad\_group\_ad](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_ad?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| ad\_group\_ad\_ad\_id | 廣告的 ID。 |
| ad\_group\_ad\_engine\_id | 外部引擎帳戶中的廣告 ID。這個欄位僅適用於 Search Ads 360 帳戶。例如：Yahoo Japan、Microsoft、百度。如為非 Search Ads 360 實體，請改用「ad\_group\_ad.ad.id」。 |
| ad\_group\_id | 廣告群組 ID。 |
| campaign\_id | 廣告活動的 ID。 |
| customer\_id | 顧客 ID。 |
| metrics\_all\_conversions | 轉換總次數。包括所有轉換，不論 include\_in\_conversions\_metric 的值為何。 |
| metrics\_all\_conversions\_by\_conversion\_date | 轉換總次數。包括所有轉換，不論 include\_in\_conversions\_metric 的值為何。如果選取這個資料欄和日期，日期資料欄中的值就是轉換日期。如要進一步瞭解 `by_conversion_date` 欄，請參閱[關於「所有轉換」欄](https://support.google.com/sa360/answer/9250611?hl=zh-tw)。 |
| metrics\_all\_conversions\_value | 所有轉換的價值。 |
| metrics\_all\_conversions\_value\_by\_conversion\_date | 所有轉換的價值。如果選取這個資料欄和日期，日期資料欄中的值就是轉換日期。如要進一步瞭解 `by_conversion_date` 欄，請參閱[關於「所有轉換」欄](https://support.google.com/sa360/answer/9250611?hl=zh-tw)。 |
| metrics\_cross\_device\_conversions | 顧客在某裝置上點按廣告，然後使用其他裝置或瀏覽器完成轉換。所有轉換次數中已納入跨裝置轉換。 |
| metrics\_cross\_device\_conversions\_by\_conversion\_date | 依轉換日期計算的跨裝置轉換次數。如要進一步瞭解 `by_conversion_date` 欄，請參閱[關於「所有轉換」欄](https://support.google.com/sa360/answer/9250611?hl=zh-tw)。 |
| metrics\_cross\_device\_conversions\_value | 跨裝置轉換價值的總和。 |
| metrics\_cross\_device\_conversions\_value\_by\_conversion\_date | 依轉換日期計算的跨裝置轉換價值總和。如要進一步瞭解 `by_conversion_date` 欄，請參閱[關於「所有轉換」欄](https://support.google.com/sa360/answer/9250611?hl=zh-tw)。 |
| segments.conversion\_action\_name | 轉換動作名稱。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17 |
| segments\_device | 指標適用的裝置。 |

Search Ads 360 表格名稱：AdDeviceStats

Search Ads 360 API 資源：[ad\_group\_ad](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_ad?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| ad\_group\_ad\_ad\_id | 廣告的 ID。 |
| ad\_group\_ad\_engine\_id | 外部引擎帳戶中的廣告 ID。這個欄位僅適用於 Search Ads 360 帳戶。例如：Yahoo Japan、Microsoft、百度。如為非 Search Ads 360 實體，請改用「ad\_group\_ad.ad.id」。 |
| ad\_group\_id | 廣告群組 ID。 |
| campaign\_id | 廣告活動的 ID。 |
| customer\_id | 顧客 ID。 |
| metrics\_average\_cpc | 所有點擊的總費用除以獲得的點擊總次數。 |
| metrics\_average\_cpm | 平均千次曝光出價。 |
| metrics\_clicks | 點擊次數。 |
| metrics\_client\_account\_conversions | 客戶帳戶轉換次數。只有 include\_in\_client\_account\_conversions\_metric 屬性設為 true 的轉換動作，才會納入這項指標。如果您使用以轉換為主的出價策略，系統會調整出價策略來爭取這些轉換。 |
| metrics\_client\_account\_conversions\_value | 客戶帳戶轉換的價值。只有 include\_in\_client\_account\_conversions\_metric 屬性設為 true 的轉換動作，才會納入這項指標。如果您使用以轉換為主的出價策略，系統會調整出價策略來爭取這些轉換。 |
| metrics\_client\_account\_view\_through\_conversions | 瀏覽後轉換總次數。如果顧客看到圖片或多媒體廣告，但未與其他廣告互動 (例如點擊)，之後在您的網站上完成轉換，就會計為瀏覽後轉換。 |
| metrics\_cost\_micros | 這段期間的單次點擊出價和千次曝光出價費用總和。 |
| metrics\_ctr | 廣告獲得的點擊次數 (點擊次數) 除以廣告顯示次數 (曝光次數)。 |
| metrics\_impressions | 廣告顯示在搜尋結果網頁或 Google 聯播網網站上的次數。 |
| metrics\_visits | Search Ads 360 成功記錄並轉送至廣告主到達網頁的點擊次數。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17 |
| segments\_device | 指標適用的裝置。 |

Search Ads 360 表格名稱：AdGroup

Search Ads 360 API 資源：[ad\_group](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| ad\_group\_bid\_modifier\_bid\_modifier | 條件相符時的出價調節係數。修飾符必須介於 0.1 到 10.0 之間。PreferredContent 的範圍為 1.0 至 6.0。使用 0 選擇不採用裝置類型。 |
| ad\_group\_bid\_modifier\_device\_type | 裝置的類型。 |
| ad\_group\_cpc\_bid\_micros | 最高單次點擊出價。 |
| ad\_group\_creation\_time | 這個廣告群組的建立時間戳記。時間戳記採用客戶時區，格式為「yyyy-MM-dd HH:mm:ss」。 |
| ad\_group\_end\_date | 廣告群組停止放送廣告的日期。根據預設，廣告群組會在廣告群組結束日期結束。如果設定這個欄位，廣告群組會在客戶時區的指定日期結束時停止放送。這個欄位僅適用於 Microsoft Advertising 和 Facebook 閘道帳戶。格式：YYYY-MM-DD 範例：2019-03-14 |
| ad\_group\_engine\_id | 外部引擎帳戶中的廣告群組 ID。這個欄位僅適用於非 Google Ads 帳戶。例如：Yahoo Japan、Microsoft、百度。如果是 Google Ads 實體，請改用「ad\_group.id」。 |
| ad\_group\_engine\_status | 廣告群組的引擎狀態。 |
| ad\_group\_id | 廣告群組 ID。 |
| ad\_group\_labels | 附加至這個廣告群組的標籤資源名稱。 |
| ad\_group\_language\_code | 廣告群組中廣告和關鍵字的語言。這個欄位僅適用於 Microsoft Advertising 帳戶。 |
| ad\_group\_last\_modified\_time | 這個廣告群組上次修改的日期時間。日期時間採用客戶時區，格式為「yyyy-MM-dd HH:mm:ss.ssssss」。 |
| ad\_group\_name | 廣告群組的名稱。建立新廣告群組時，這個欄位為必填，且不得為空白。長度不得超過 255 個 UTF-8 全形字元。不得包含任何空值 (代碼點 0x0)、NL 換行 (代碼點 0xA) 或回車字元 (代碼點 0xD)。 |
| ad\_group\_start\_date | 這個廣告群組開始放送廣告的日期。預設情況下，廣告群組會立即開始放送，或從廣告群組的開始日期開始放送，以較晚者為準。如果設定這個欄位，廣告群組會在客戶時區的指定日期開始時啟動。這個欄位僅適用於 Microsoft Advertising 和 Facebook 閘道帳戶。格式：YYYY-MM-DD 範例：2019-03-14 |
| ad\_group\_status | 廣告群組的狀態。 |
| ad\_group\_targeting\_setting\_target\_restrictions | 限制廣告活動或廣告群組觸及範圍的指定維度設定。 |
| bidding\_strategy\_id | 出價策略的 ID。 |
| campaign\_id | 廣告活動的 ID。 |
| customer\_id | 顧客 ID。 |

Search Ads 360 表格名稱：AdGroupAssetStats

Search Ads 360 API 資源：[ad\_group\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_asset?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| ad\_group\_asset\_ad\_group | 這是必要旗標，不可變動。素材資源連結的廣告群組。 |
| ad\_group\_asset\_asset | 這是必要旗標，不可變動。連結至廣告群組的素材資源。 |
| ad\_group\_engine\_id | 外部引擎帳戶中的廣告群組 ID。這個欄位僅適用於非 Google Ads 帳戶。例如：Yahoo Japan、Microsoft、百度。如果是 Google Ads 實體，請改用「ad\_group.id」。 |
| ad\_group\_id | 廣告群組 ID。 |
| campaign\_id | 廣告活動的 ID。 |
| customer\_id | 顧客 ID。 |
| metrics\_average\_cpc | 所有點擊的總費用除以獲得的點擊總次數。 |
| metrics\_average\_cpm | 平均千次曝光出價。 |
| metrics\_clicks | 點擊次數。 |
| metrics\_client\_account\_conversions | 客戶帳戶轉換次數。只有 include\_in\_client\_account\_conversions\_metric 屬性設為 true 的轉換動作，才會納入這項指標。如果您使用以轉換為主的出價策略，系統會調整出價策略來爭取這些轉換。 |
| metrics\_client\_account\_conversions\_value | 客戶帳戶轉換的價值。只有 include\_in\_client\_account\_conversions\_metric 屬性設為 true 的轉換動作，才會納入這項指標。如果您使用以轉換為主的出價策略，系統會調整出價策略來爭取這些轉換。 |
| metrics\_cost\_micros | 這段期間的單次點擊出價和千次曝光出價費用總和。 |
| metrics\_ctr | 廣告獲得的點擊次數 (點擊次數) 除以廣告顯示次數 (曝光次數)。 |
| metrics\_impressions | 廣告顯示在搜尋結果網頁或 Google 聯播網網站上的次數。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17 |

Search Ads 360 表格名稱：AdGroupAudienceConversionActionAndDeviceStats

Search Ads 360 API 資源：[ad\_group\_audience\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_audience_view?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| ad\_group\_criterion\_age\_range\_type | 年齡層類型。 |
| ad\_group\_criterion\_bid\_modifier | 條件相符時的出價調節係數。修飾符必須介於 0.1 到 10.0 之間。大多數可指定條件類型都支援調節係數。 |
| ad\_group\_criterion\_cpc\_bid\_micros | 單次點擊出價。 |
| ad\_group\_criterion\_criterion\_id | 指定條件的 ID。 |
| ad\_group\_criterion\_gender\_type | 性別類型。 |
| ad\_group\_criterion\_location\_geo\_target\_constant | 地理目標常數資源名稱。 |
| ad\_group\_criterion\_user\_list\_user\_list | 使用者名單資源名稱。 |
| ad\_group\_criterion\_webpage\_conditions | 指定網頁的條件或邏輯運算式。評估網頁指定目標時，系統會將網頁指定目標條件清單以 AND 運算子連結。如果條件清單為空白，表示廣告活動網站的所有網頁都是指定目標。建立作業必須填寫這個欄位，更新作業則不得填寫。 |
| ad\_group\_criterion\_webpage\_coverage\_percentage | 網站條件涵蓋率百分比。這是根據廣告群組和廣告活動中的網站目標、排除網站目標和排除關鍵字，計算出的網站涵蓋率百分比。舉例來說，如果涵蓋範圍傳回 1，表示涵蓋範圍為 100%。 |
| ad\_group\_id | 廣告群組 ID。 |
| campaign\_id | 廣告活動的 ID。 |
| customer\_id | 顧客 ID。 |
| metrics\_cross\_device\_conversions | 顧客在某裝置上點按廣告，然後使用其他裝置或瀏覽器完成轉換。所有轉換次數中已納入跨裝置轉換。 |
| metrics\_cross\_device\_conversions\_value | 跨裝置轉換價值的總和。 |
| segments.conversion\_action\_name | 轉換動作名稱。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17。 |
| segments\_device | 指標適用的裝置。 |

Search Ads 360 表格名稱：AdGroupAudienceDeviceStats

Search Ads 360 API 資源：[ad\_group\_audience\_view](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_audience_view?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| ad\_group\_criterion\_age\_range\_type | 年齡層類型。 |
| ad\_group\_criterion\_bid\_modifier | 條件相符時的出價調節係數。修飾符必須介於 0.1 到 10.0 之間。大多數可指定條件類型都支援調節係數。 |
| ad\_group\_criterion\_cpc\_bid\_micros | 單次點擊出價。 |
| ad\_group\_criterion\_criterion\_id | 指定條件的 ID。 |
| ad\_group\_criterion\_gender\_type | 性別類型。 |
| ad\_group\_criterion\_location\_geo\_target\_constant | 地理目標常數資源名稱。 |
| ad\_group\_criterion\_user\_list\_user\_list | 使用者名單資源名稱。 |
| ad\_group\_criterion\_webpage\_conditions | 指定網頁的條件或邏輯運算式。評估網頁指定目標時，系統會將網頁指定目標條件清單以 AND 運算子連結。如果條件清單為空白，表示廣告活動網站的所有網頁都是指定目標。建立作業必須填寫這個欄位，更新作業則不得填寫。 |
| ad\_group\_criterion\_webpage\_coverage\_percentage | 網站條件涵蓋率百分比。這是根據廣告群組和廣告活動中的網站目標、排除網站目標和排除關鍵字，計算出的網站涵蓋率百分比。舉例來說，如果涵蓋範圍傳回 1，表示涵蓋範圍為 100%。 |
| ad\_group\_id | 廣告群組 ID。 |
| campaign\_id | 廣告活動的 ID。 |
| customer\_id | 顧客 ID。 |
| metrics\_average\_cpc | 所有點擊的總費用除以獲得的點擊總次數。 |
| metrics\_average\_cpm | 平均千次曝光出價。 |
| metrics\_clicks | 點擊次數。 |
| metrics\_client\_account\_conversions | 客戶帳戶轉換次數。只有 include\_in\_client\_account\_conversions\_metric 屬性設為 true 的轉換動作，才會納入這項指標。如果您使用以轉換為主的出價策略，系統會調整出價策略來爭取這些轉換。 |
| metrics\_client\_account\_conversions\_value | 客戶帳戶轉換的價值。只有 include\_in\_client\_account\_conversions\_metric 屬性設為 true 的轉換動作，才會納入這項指標。如果您使用以轉換為主的出價策略，系統會調整出價策略來爭取這些轉換。 |
| metrics\_client\_account\_view\_through\_conversions | 瀏覽後轉換總次數。如果顧客看到圖片或多媒體廣告，但未與其他廣告互動 (例如點擊)，之後在您的網站上完成轉換，就會計為瀏覽後轉換。 |
| metrics\_cost\_micros | 這段期間的單次點擊出價和千次曝光出價費用總和。 |
| metrics\_ctr | 廣告獲得的點擊次數 (點擊次數) 除以廣告顯示次數 (曝光次數)。 |
| metrics\_impressions | 廣告顯示在搜尋結果網頁或 Google 聯播網網站上的次數。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17 |
| segments\_device | 指標適用的裝置。 |

Search Ads 360 表格名稱：AdGroupConversionActionAndAssetStats

Search Ads 360 API 資源：[ad\_group\_asset](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_asset?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| ad\_group\_asset\_ad\_group | 這是必要旗標，不可變動。素材資源連結的廣告群組。 |
| ad\_group\_asset\_asset | 這是必要旗標，不可變動。連結至廣告群組的素材資源。 |
| ad\_group\_engine\_id | 外部引擎帳戶中的廣告群組 ID。這個欄位僅適用於非 Google Ads 帳戶。例如：Yahoo Japan、Microsoft、百度。如果是 Google Ads 實體，請改用「ad\_group.id」。 |
| ad\_group\_id | 廣告群組 ID。 |
| campaign\_id | 廣告活動的 ID。 |
| customer\_id | 顧客 ID。 |
| metrics\_all\_conversions | 轉換總次數。包括所有轉換，不論 include\_in\_conversions\_metric 的值為何。 |
| metrics\_all\_conversions\_value | 所有轉換的價值。 |
| metrics\_cross\_device\_conversions | 顧客在某裝置上點按廣告，然後使用其他裝置或瀏覽器完成轉換。所有轉換次數中已納入跨裝置轉換。 |
| metrics\_cross\_device\_conversions\_value | 跨裝置轉換價值的總和。 |
| segments.conversion\_action\_name | 轉換動作名稱。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2018-04-17 |

Search Ads 360 表格名稱：AdGroupConversionActionAndDeviceStats

Search Ads 360 API 資源：[ad\_group](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| ad\_group\_engine\_id | 僅供輸出。外部引擎帳戶中的廣告群組 ID。這個欄位僅適用於非 Google Ads 帳戶。例如：Yahoo Japan、Microsoft、百度。如果是 Google Ads 實體，請改用「ad\_group.id」。 |
| ad\_group\_id | 僅供輸出。廣告群組 ID。 |
| bidding\_strategy\_id | 僅供輸出。出價策略的 ID。 |
| campaign\_id | 僅供輸出。廣告活動的 ID。 |
| customer\_id | 僅供輸出。顧客 ID。 |
| metrics\_all\_conversions | 轉換總次數。包括所有轉換，不論 include\_in\_conversions\_metric 的值為何。 |
| metrics\_all\_conversions\_value | 所有轉換的價值。 |
| metrics\_cross\_device\_conversions | 顧客在某裝置上點按廣告，然後使用其他裝置或瀏覽器完成轉換。所有轉換次數中已納入跨裝置轉換。 |
| metrics\_cross\_device\_conversions\_value | 跨裝置轉換價值的總和。 |
| segments.conversion\_action\_name | 轉換動作名稱。 |
| segments\_date | 指標適用的日期，格式為 yyyy-MM-dd。例如：2024-04-17 |
| segments\_device | 指標適用的裝置。 |

Search Ads 360 表格名稱：AdGroupCriterion

Search Ads 360 API 資源：[ad\_group\_criterion](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/ad_group_criterion?hl=zh-tw)

| Search Ads 360 欄位名稱 | 說明 |
| --- | --- |
| ad\_group\_criterion\_age\_range\_type | 年齡層類型。 |
| ad\_group\_criterion\_bid\_modifier | 條件相符時的出價調節係數。修飾符必須介於 0.1 到 10.0 之間。大多數可指定條件類型都支援調節係數。 |
| ad\_group\_criterion\_cpc\_bid\_micros | 單次點擊出價。 |
| ad\_group\_criterion\_creation\_time | 這個廣告群組條件的建立時間戳記。時間戳記採用客戶時區，格式為「yyyy-MM-dd HH:mm:ss」。 |
| ad\_group\_criterion\_criterion\_id | 指定條件的 ID。 |
| ad\_group\_criterion\_gender\_type | 性別類型。 |
| ad\_group\_criterion\_last\_modified\_time | 這個廣告群組條件上次修改的日期時間。日期時間採用客戶時區，格式為「yyyy-MM-dd HH:mm:ss.ssssss」。 |
| ad\_group\_criterion\_location\_geo\_target\_constant | 地理目標常數資源名稱。 |
| ad\_group\_criterion\_status | 條件的狀態。這是由用戶端設定的廣告群組條件實體狀態。注意：使用者介面報表可能會納入其他資訊，影響條件是否符合放送資格。在某些情況下，即使透過 API 移除條件，該條件在使用者介面中仍可能顯示為已啟用。舉例來說，除非排除，否則廣告活動預設會向所有年齡層的使用者顯示。由於這些年齡層符合廣告放送資格，使用者介面會將每個年齡範圍顯示為「已啟用」，但 AdGroupCriterion.status 會顯示「已移除」，因為沒有新增任何正向條件。 |
| ad\_group\_criterion\_type | 條件類型。 |
| ad\_group\_criterion\_user\_list\_user\_list | 使用者名單資源名稱。 |
| ad\_group\_criterion\_webpage\_conditions | 指定網頁的條件或邏輯運算式。評估網頁指定目標時，系統會將網頁指定目標條件清單以 AND 運算子連結。如果條件清單為空白，表示廣告活動網站的所有網頁都是指定目標。建立作業必須填寫這個欄位，更新作業則不得填寫。 |
| ad\_group\_criterion\_webpage\_coverage\_percentage | 網站條件涵蓋率百分比。這是根據廣告群組和廣告活動中的網站目標、排除網站目標和排除關鍵字，計算出的網站涵蓋率百分比。舉例來說，如果涵蓋範圍傳回 1，表示涵蓋範圍為 100%。 |
| ad\_group\_id | 廣告群組 ID。 |
| ad\_group\_name | 廣告群組的名稱。建立新廣告群組時，這個欄位為必填，且不得為空白。長度不得超過 255 個 UTF-8 全形字元。不得包含任何空值 (代碼點 0x0)、NL 換行 (代碼點 0xA) 或回車字元 (代碼點 0xD)。 |
| ad\_group\_status | 廣告群組的狀態。 |
| campaign\_id | 廣告活動的 ID。 |
| campaign\_name | 廣告活動名稱。建立新廣告活動時，這個欄位為必填，且不得為空白。不得包含任何空值 (代碼點 0x0)、NL 換行 (代碼點 0xA) 或回車字元 (代碼點 0xD)。 |
| campaign\_status | 廣告活動的狀態。 |
| customer\_account\_type | 引擎帳戶類型。例如：Google Ads、Microsoft Advertising、Yahoo Japan、百度、Facebook、Engine Track。 |
| customer\_descriptive\_name | 選填 |