* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# Google Ads report transformation

This document describes how you can transform your reports for
Google Ads (formerly known as Google AdWords).

## Table mapping for Google Ads reports

When your Google Ads reports are transferred
to BigQuery, the reports are transformed into the following
BigQuery tables and views.

When you view the tables and views in BigQuery, the value for
customer\_id is your Google Ads customer ID.

| AdWords reports (deprecated) | BigQuery AdWords tables | Google Ads tables | Google Ads API resources (v22.0.0) | BigQuery views |
| --- | --- | --- | --- | --- |
| [Account Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/account-performance-report) | p\_Customer\_customer\_id  p\_HourlyAccountConversionStats\_customer\_id  p\_AccountConversionStats\_customer\_id  p\_HourlyAccountStats\_customer\_id  p\_AccountNonClickStats\_customer\_id  p\_AccountBasicStats\_customer\_id  p\_AccountStats\_customer\_id | p\_ads\_Customer\_customer\_id  p\_ads\_HourlyAccountConversionStats\_customer\_id  p\_ads\_AccountConversionStats\_customer\_id  p\_ads\_HourlyAccountStats\_customer\_id  p\_ads\_AccountNonClickStats\_customer\_id  p\_ads\_AccountBasicStats\_customer\_id  p\_ads\_AccountStats\_customer\_id | [Customer](https://developers.google.com/google-ads/api/fields/v22/customer) | Customer\_customer\_id  HourlyAccountConversionStats\_customer\_id  AccountConversionStats\_customer\_id  HourlyAccountStats\_customer\_id  AccountNonClickStats\_customer\_id  AccountBasicStats\_customer\_id  AccountStats\_customer\_id |
| [Ad Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/ad-performance-report) | p\_AdBasicStats\_customer\_id  p\_AdCrossDeviceStats\_customer\_id  p\_AdConversionStats\_customer\_id  p\_AdStats\_customer\_id  p\_AdCrossDeviceConversionStats\_customer\_id  p\_Ad\_customer\_id | p\_ads\_AdBasicStats\_customer\_id  p\_ads\_AdCrossDeviceStats\_customer\_id  p\_ads\_AdConversionStats\_customer\_id  p\_ads\_AdStats\_customer\_id  p\_ads\_AdCrossDeviceConversionStats\_customer\_id  p\_ads\_Ad\_customer\_id | [Ad Group Ad](https://developers.google.com/google-ads/api/fields/v22/ad_group_ad) | AdBasicStats\_customer\_id  AdCrossDeviceStats\_customer\_id  AdConversionStats\_customer\_id  AdStats\_customer\_id  AdCrossDeviceConversionStats\_customer\_id  Ad\_customer\_id |
| [Adgroup Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/adgroup-performance-report) | p\_AdGroupStats\_customer\_id  p\_AdGroupBasicStats\_customer\_id  p\_AdGroupCrossDeviceStats\_customer\_id  p\_HourlyAdGroupConversionStats\_customer\_id  p\_HourlyAdGroupStats\_customer\_id  p\_AdGroupConversionStats\_customer\_id  p\_AdGroupCrossDeviceConversionStats\_customer\_id  p\_AdGroup\_customer\_id | p\_ads\_AdGroupStats\_customer\_id  p\_ads\_AdGroupBasicStats\_customer\_id  p\_ads\_AdGroupCrossDeviceStats\_customer\_id  p\_ads\_HourlyAdGroupConversionStats\_customer\_id  p\_ads\_HourlyAdGroupStats\_customer\_id  p\_ads\_AdGroupConversionStats\_customer\_id  p\_ads\_AdGroupCrossDeviceConversionStats\_customer\_id  p\_ads\_AdGroup\_customer\_id | [Ad Group](https://developers.google.com/google-ads/api/fields/v22/ad_group) | AdGroupStats\_customer\_id  AdGroupBasicStats\_customer\_id  AdGroupCrossDeviceStats\_customer\_id  HourlyAdGroupConversionStats\_customer\_id  HourlyAdGroupStats\_customer\_id  AdGroupConversionStats\_customer\_id  AdGroupCrossDeviceConversionStats\_customer\_id  AdGroup\_customer\_id |
| [Age Range Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/age-range-performance-report) | p\_AgeRange\_customer\_id  p\_AgeRangeBasicStats\_customer\_id  p\_AgeRangeStats\_customer\_id  p\_AgeRangeConversionStats\_customer\_id  p\_AgeRangeNonClickStats\_customer\_id | p\_ads\_AgeRange\_customer\_id  p\_ads\_AgeRangeBasicStats\_customer\_id  p\_ads\_AgeRangeStats\_customer\_id  p\_ads\_AgeRangeConversionStats\_customer\_id  p\_ads\_AgeRangeNonClickStats\_customer\_id | [Age Range View](https://developers.google.com/google-ads/api/fields/v22/age_range_view) | AgeRange\_customer\_id  AgeRangeBasicStats\_customer\_id  AgeRangeStats\_customer\_id  AgeRangeConversionStats\_customer\_id  AgeRangeNonClickStats\_customer\_id |
| [Audience Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/audience-performance-report) | p\_Audience\_customer\_id  p\_AudienceConversionStats\_customer\_id  p\_AudienceNonClickStats\_customer\_id  p\_AudienceBasicStats\_customer\_id  p\_AudienceStats\_customer\_id | `NULL`  `NULL`  `NULL`  `NULL`  `NULL` | [Ad Group Audience View](https://developers.google.com/google-ads/api/fields/v22/ad_group_audience_view)  [Campaign Audience View](https://developers.google.com/google-ads/api/fields/v22/campaign_audience_view) | Audience\_customer\_id  AudienceConversionStats\_customer\_id  AudienceNonClickStats\_customer\_id  AudienceBasicStats\_customer\_id  AudienceStats\_customer\_id |
| [Bid Goal Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/bid-goal-performance-report) | p\_BidGoal\_customer\_id  p\_BidGoalStats\_customer\_id  p\_HourlyBidGoalStats\_customer\_id  p\_BidGoalConversionStats\_customer\_id | p\_ads\_BidGoal\_customer\_id  p\_ads\_BidGoalStats\_customer\_id  p\_ads\_HourlyBidGoalStats\_customer\_id  p\_ads\_BidGoalConversionStats\_customer\_id | [Bidding Strategy](https://developers.google.com/google-ads/api/fields/v22/bidding_strategy) | BidGoal\_customer\_id  BidGoalStats\_customer\_id  HourlyBidGoalStats\_customer\_id  BidGoalConversionStats\_customer\_id |
| [Budget Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/budget-performance-report) | p\_Budget\_customer\_id  p\_BudgetStats\_customer\_id | p\_ads\_Budget\_customer\_id  p\_ads\_BudgetStats\_customer\_id | [Campaign Budget](https://developers.google.com/google-ads/api/fields/v22/campaign_budget) | Budget\_customer\_id  BudgetStats\_customer\_id |
| [Campaign Location Target Report](https://developers.google.com/adwords/api/docs/appendix/reports/campaign-location-target-report) | p\_CampaignLocationTargetStats\_customer\_id  p\_LocationBasedCampaignCriterion\_customer\_id | p\_ads\_CampaignLocationTargetStats\_customer\_id  p\_ads\_LocationBasedCampaignCriterion\_customer\_id | [Location View](https://developers.google.com/google-ads/api/fields/v22/location_view) | CampaignLocationTargetStats\_customer\_id  LocationBasedCampaignCriterion\_customer\_id |
| [Campaign Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/campaign-performance-report) | p\_Campaign\_customer\_id  p\_CampaignBasicStats\_customer\_id  p\_CampaignConversionStats\_customer\_id  p\_CampaignCrossDeviceStats\_customer\_id  p\_HourlyCampaignConversionStats\_customer\_id  p\_CampaignStats\_customer\_id  p\_HourlyCampaignStats\_customer\_id  p\_CampaignCrossDeviceConversionStats\_customer\_id  p\_CampaignCookieStats\_customer\_id | p\_ads\_Campaign\_customer\_id  p\_ads\_CampaignBasicStats\_customer\_id  p\_ads\_CampaignConversionStats\_customer\_id  p\_ads\_CampaignCrossDeviceStats\_customer\_id  p\_ads\_HourlyCampaignConversionStats\_customer\_id  p\_ads\_CampaignStats\_customer\_id  p\_ads\_HourlyCampaignStats\_customer\_id  p\_ads\_CampaignCrossDeviceConversionStats\_customer\_id  p\_ads\_CampaignCookieStats\_customer\_id | [Campaign](https://developers.google.com/google-ads/api/fields/v22/campaign) | Campaign\_customer\_id  CampaignBasicStats\_customer\_id  CampaignConversionStats\_customer\_id  CampaignCrossDeviceStats\_customer\_id  HourlyCampaignConversionStats\_customer\_id  CampaignStats\_customer\_id  HourlyCampaignStats\_customer\_id  CampaignCrossDeviceConversionStats\_customer\_id  CampaignCookieStats\_customer\_id |
| [Click Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/click-performance-report) | p\_ClickStats\_customer\_id | p\_ads\_ClickStats\_customer\_id | [Click View](https://developers.google.com/google-ads/api/fields/v22/click_view) | ClickStats\_customer\_id |
| [Criteria Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/criteria-performance-report) | p\_Criteria\_customer\_id  p\_CriteriaBasicStats\_customer\_id  p\_CriteriaStats\_customer\_id  p\_CriteriaConversionStats\_customer\_id  p\_CriteriaNonClickStats\_customer\_id | `NULL`  `NULL`  `NULL`  `NULL`  `NULL` |  | Criteria\_customer\_id  CriteriaBasicStats\_customer\_id  CriteriaStats\_customer\_id  CriteriaConversionStats\_customer\_id  CriteriaNonClickStats\_customer\_id |
| [Gender Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/gender-performance-report) | p\_Gender\_customer\_id  p\_GenderBasicStats\_customer\_id  p\_GenderStats\_customer\_id  p\_GenderConversionStats\_customer\_id  p\_GenderNonClickStats\_customer\_id | p\_ads\_Gender\_customer\_id  p\_ads\_GenderBasicStats\_customer\_id  p\_ads\_GenderStats\_customer\_id  p\_ads\_GenderConversionStats\_customer\_id  p\_ads\_GenderNonClickStats\_customer\_id | [Gender View](https://developers.google.com/google-ads/api/fields/v22/gender_view) | Gender\_customer\_id  GenderBasicStats\_customer\_id  GenderStats\_customer\_id  GenderConversionStats\_customer\_id  GenderNonClickStats\_customer\_id |
| [Geo Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/geo-performance-report) | p\_GeoConversionStats\_customer\_id  p\_GeoStats\_customer\_id | p\_ads\_GeoConversionStats\_customer\_id  p\_ads\_GeoStats\_customer\_id | [Geographic View](https://developers.google.com/google-ads/api/fields/v22/geographic_view) | GeoConversionStats\_customer\_id  GeoStats\_customer\_id |
| [Keywords Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/keywords-performance-report) | p\_Keyword\_customer\_id  p\_KeywordBasicStats\_customer\_id  p\_KeywordCrossDeviceStats\_customer\_id  p\_KeywordStats\_customer\_id  p\_KeywordCrossDeviceConversionStats\_customer\_id  p\_KeywordConversionStats\_customer\_id | p\_ads\_Keyword\_customer\_id  p\_ads\_KeywordBasicStats\_customer\_id  p\_ads\_KeywordCrossDeviceStats\_customer\_id  p\_ads\_KeywordStats\_customer\_id  p\_ads\_KeywordCrossDeviceConversionStats\_customer\_id  p\_ads\_KeywordConversionStats\_customer\_id | [Keyword View](https://developers.google.com/google-ads/api/fields/v22/keyword_view) | Keyword\_customer\_id  KeywordBasicStats\_customer\_id  KeywordCrossDeviceStats\_customer\_id  KeywordStats\_customer\_id  KeywordCrossDeviceConversionStats\_customer\_id  KeywordConversionStats\_customer\_id |
| [Paid Organic Query Report](https://developers.google.com/adwords/api/docs/appendix/reports/paid-organic-query-report) | p\_PaidOrganicStats\_customer\_id | p\_ads\_PaidOrganicStats\_customer\_id | [Paid Organic Search Term View](https://developers.google.com/google-ads/api/fields/v22/paid_organic_search_term_view) | PaidOrganicStats\_customer\_id |
| [Parental Status Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/parental-status-performance-report) | p\_ParentalStatus\_customer\_id  p\_ParentalStatusBasicStats\_customer\_id  p\_ParentalStatusStats\_customer\_id  p\_ParentalStatusConversionStats\_customer\_id  p\_ParentalStatusNonClickStats\_customer\_id | p\_ads\_ParentalStatus\_customer\_id  p\_ads\_ParentalStatusBasicStats\_customer\_id  p\_ads\_ParentalStatusStats\_customer\_id  p\_ads\_ParentalStatusConversionStats\_customer\_id  p\_ads\_ParentalStatusNonClickStats\_customer\_id | [Parental Status View](https://developers.google.com/google-ads/api/fields/v22/parental_status_view) | ParentalStatus\_customer\_id  ParentalStatusBasicStats\_customer\_id  ParentalStatusStats\_customer\_id  ParentalStatusConversionStats\_customer\_id  ParentalStatusNonClickStats\_customer\_id |
| [Placement Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/placement-performance-report) | p\_PlacementBasicStats\_customer\_id  p\_PlacementNonClickStats\_customer\_id  p\_PlacementStats\_customer\_id  p\_Placement\_customer\_id  p\_PlacementConversionStats\_customer\_id | p\_ads\_PlacementBasicStats\_customer\_id  p\_ads\_PlacementNonClickStats\_customer\_id  p\_ads\_PlacementStats\_customer\_id  p\_ads\_Placement\_customer\_id  p\_ads\_PlacementConversionStats\_customer\_id | [Managed Placement View](https://developers.google.com/google-ads/api/fields/v22/managed_placement_view) | PlacementBasicStats\_customer\_id  PlacementNonClickStats\_customer\_id  PlacementStats\_customer\_id  Placement\_customer\_id  PlacementConversionStats\_customer\_id |
| [Search Query Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/search-query-performance-report) | p\_SearchQueryStats\_customer\_id  p\_SearchQueryConversionStats\_customer\_id | p\_ads\_SearchQueryStats\_customer\_id  p\_ads\_SearchQueryConversionStats\_customer\_id | [Search Term View](https://developers.google.com/google-ads/api/fields/v22/search_term_view) | SearchQueryStats\_customer\_id  SearchQueryConversionStats\_customer\_id |
| [Shopping Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/shopping-performance-report) | p\_ShoppingProductConversionStats\_customer\_id  p\_ShoppingProductStats\_customer\_id | p\_ads\_ShoppingProductConversionStats\_customer\_id  p\_ads\_ShoppingProductStats\_customer\_id | [Shopping Performance View](https://developers.google.com/google-ads/api/fields/v22/shopping_performance_view) | ShoppingProductConversionStats\_customer\_id  ShoppingProductStats\_customer\_id |
| [Video Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/video-performance-report) | p\_VideoBasicStats\_customer\_id  p\_VideoConversionStats\_customer\_id  p\_VideoStats\_customer\_id  p\_Video\_customer\_id  p\_VideoNonClickStats\_customer\_id | p\_ads\_VideoBasicStats\_customer\_id  p\_ads\_VideoConversionStats\_customer\_id  p\_ads\_VideoStats\_customer\_id  p\_ads\_Video\_customer\_id  p\_ads\_VideoNonClickStats\_customer\_id | [Video](https://developers.google.com/google-ads/api/fields/v22/video) | VideoBasicStats\_customer\_id  VideoConversionStats\_customer\_id  VideoStats\_customer\_id  Video\_customer\_id  VideoNonClickStats\_customer\_id |
|  |  | AdGroupBidModifier | [Ad Group Bid Modifier](https://developers.google.com/google-ads/api/fields/v22/ad_group_bid_modifier) |  |
|  |  | AdGroupAdLabel | [Ad Group Ad Label](https://developers.google.com/google-ads/api/fields/v22/ad_group_ad_label) |  |
|  |  | CampaignLabel | [Campaign Label](https://developers.google.com/google-ads/api/fields/v22/campaign_label) |  |
|  |  | CampaignCriterion | [Campaign Criterion](https://developers.google.com/google-ads/api/fields/v22/campaign_criterion) |  |
|  |  | AdGroupLabel | [Ad Group Label](https://developers.google.com/google-ads/api/fields/v22/ad_group_label) |  |
|  |  | AdGroupAudience  AdGroupAudienceStats  AdGroupAudienceConversionStats  AdGroupAudienceNonClickStats  AdGroupAudienceBasicStats | [Ad Group Audience View](https://developers.google.com/google-ads/api/fields/v22/ad_group_audience_view) |  |
|  |  | Assets (available if [Pmax](https://developers.google.com/google-ads/api/docs/performance-max/overview) data is enabled) | [Assets](https://developers.google.com/google-ads/api/fields/v22/asset) |  |
|  |  | AssetGroup (available if [Pmax](https://developers.google.com/google-ads/api/docs/performance-max/overview) data is enabled) | [Asset Groups](https://developers.google.com/google-ads/api/fields/v22/asset_group) |  |
|  |  | AssetGroupAsset (available if [Pmax](https://developers.google.com/google-ads/api/docs/performance-max/overview) data is enabled) | [Asset Group Assets](https://developers.google.com/google-ads/api/fields/v22/asset_group_asset) |  |
|  |  | AssetGroupSignal (available if [Pmax](https://developers.google.com/google-ads/api/docs/performance-max/overview) data is enabled) | [Asset Group Signal](https://developers.google.com/google-ads/api/fields/v22/asset_group_signal) |  |
|  |  | AssetGroupProductGroupStats (available if [Pmax](https://developers.google.com/google-ads/api/docs/performance-max/overview) data is enabled) | [AssetGroupProductGroupStats](https://developers.google.com/google-ads/api/fields/v22/asset_group_product_group_view) |  |
|  |  | CampaignAssetStats (available if [Pmax](https://developers.google.com/google-ads/api/docs/performance-max/overview) data is enabled) | [CampaignAssetStats](https://developers.google.com/google-ads/api/fields/v22/campaign_asset) |  |

## Column mapping for Google Ads reports

The BigQuery tables created by a Google Ads
transfer consist of the following columns (fields):

Google Ads Table Name: AccountBasicStats

Google Ads API Resource:
[customer](https://developers.google.com/google-ads/api/fields/v22/customer)

| Google Ads Field Name | Description | Adwords Mapped Field Name |
| --- | --- | --- |
| customer\_id | The ID of the customer. | ExternalCustomerId |
| metrics\_clicks | The number of clicks. | Clicks |
| metrics\_conversions | The number of conversions. This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | Conversions |
| metrics\_conversions\_value | The total value of conversions. This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | ConversionValue |
| metrics\_cost\_micros | The sum of your cost-per-click (CPC) and cost-per-thousand impressions (CPM) costs during this period. | Cost |
| metrics\_impressions | Count of how often your ad has appeared on a search results page or website on the Google Network. | Impressions |
| metrics\_interaction\_event\_types | The types of payable and free interactions. | InteractionTypes |
| metrics\_interactions | The number of interactions. An interaction is the main user action associated with an ad format, such as clicks for text and shopping ads or views for video ads. | Interactions |
| metrics\_view\_through\_conversions | The total number of view-through conversions. These happen when a customer sees an image or rich media ad, then later completes a conversion on your site without interacting with (for example, clicking on) another ad. | ViewThroughConversions |
| segments\_ad\_network\_type | Ad network type. | AdNetworkType2 |
| segments\_date | Date to which metrics apply. yyyy-MM-dd format. For example, 2018-04-17. | Date |
| segments\_device | Device to which metrics apply. | Device |
| segments\_slot | Position of the ad. | Slot |

Google Ads Table Name: AccountConversionStats

Google Ads API Resource:
[customer](https://developers.google.com/google-ads/api/fields/v22/customer)

| Google Ads Field Name | Description | Adwords Mapped Field Name |
| --- | --- | --- |
| customer\_id | The ID of the customer. | ExternalCustomerId |
| metrics\_conversions | The number of conversions. This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | Conversions |
| metrics\_conversions\_value | The total value of conversions. This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | ConversionValue |
| metrics\_value\_per\_conversion | The value of conversions divided by the number of conversions. This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | ValuePerConversion |
| segments\_ad\_network\_type | Ad network type. | AdNetworkType2 |
| segments\_click\_type | Click type. | ClickType |
| segments\_conversion\_action | Resource name of the conversion action. | ConversionTrackerId |
| segments\_conversion\_action\_category | Conversion action category. | ConversionCategoryName |
| segments\_conversion\_action\_name | Conversion action name. | ConversionTypeName |
| segments\_date | Date to which metrics apply. yyyy-MM-dd format. For example, 2018-04-17. | Date |
| segments\_day\_of\_week | Day of the week. For example, MONDAY. | DayOfWeek |
| segments\_device | Device to which metrics apply. | Device |
| segments\_month | Month as represented by the date of the first day of a month. Formatted as yyyy-MM-dd. | Month |
| segments\_quarter | Quarter as represented by the date of the first day of a quarter. Uses the calendar year for quarters. For example, the second quarter of 2018 starts on 2018-04-01. Formatted as yyyy-MM-dd. | Quarter |
| segments\_slot | Position of the ad. | Slot |
| segments\_week | Week as defined as Monday through Sunday, and represented by the date of Monday. Formatted as yyyy-MM-dd. | Week |
| segments\_year | Year, formatted as yyyy. | Year |

Google Ads Table Name: AccountNonClickStats

Google Ads API Resource:
[customer](https://developers.google.com/google-ads/api/fields/v22/customer)

| Google Ads Field Name | Description | Adwords Mapped Field Name |
| --- | --- | --- |
| customer\_id | The ID of the customer. | ExternalCustomerId |
| metrics\_all\_conversions | The total number of conversions. This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | AllConversions |
| metrics\_all\_conversions\_from\_interactions\_rate | All conversions from interactions (as oppose to view through conversions) divided by the number of ad interactions. | AllConversionRate |
| metrics\_all\_conversions\_value | The total value of all conversions. | AllConversionValue |
| metrics\_average\_cpe | The average amount that you've been charged for an ad engagement. This amount is the total cost of all ad engagements divided by the total number of ad engagements. | AverageCpe |
| metrics\_trueview\_average\_cpv | The average amount you pay each time someone views your ad. The average CPV is defined by the total cost of all ad views divided by the number of views. | AverageCpv |
| metrics\_content\_budget\_lost\_impression\_share | The estimated percent of times that your ad was eligible to show on the Display Network but didn't because your budget was too low. Note: Content budget lost impression share is reported in the range of 0 to 0.9. Any value above 0.9 is reported as 0.9001. | ContentBudgetLostImpressionShare |
| metrics\_content\_impression\_share | The impressions you've received on the Display Network divided by the estimated number of impressions you were eligible to receive. Note: Content impression share is reported in the range of 0.1 to 1. Any value below 0.1 is reported as 0.0999. | ContentImpressionShare |
| metrics\_content\_rank\_lost\_impression\_share | The estimated percentage of impressions on the Display Network that your ads didn't receive due to poor Ad Rank. Note: Content rank lost impression share is reported in the range of 0 to 0.9. Any value above 0.9 is reported as 0.9001. | ContentRankLostImpressionShare |
| metrics\_cost\_per\_all\_conversions | The cost of ad interactions divided by all conversions. | CostPerAllConversion |
| metrics\_cross\_device\_conversions | Conversions from when a customer clicks on a Google Ads ad on one device, then converts on a different device or browser. Cross-device conversions are already included in all\_conversions. | CrossDeviceConversions |
| metrics\_engagement\_rate | How often people engage with your ad after it's shown to them. This is the number of ad expansions divided by the number of times your ad is shown. | EngagementRate |
| metrics\_engagements | The number of engagements. An engagement occurs when a viewer expands your Lightbox ad. Also, in the future, other ad types may support engagement metrics. | Engagements |
| metrics\_invalid\_click\_rate | The percentage of clicks filtered out of your total number of clicks (filtered + non-filtered clicks) during the reporting period. | InvalidClickRate |
| metrics\_invalid\_clicks | Number of clicks Google considers illegitimate and doesn't charge you for. | InvalidClicks |
| metrics\_search\_budget\_lost\_impression\_share | The estimated percent of times that your ad was eligible to show on the Search Network but didn't because your budget was too low. Note: Search budget lost impression share is reported in the range of 0 to 0.9. Any value above 0.9 is reported as 0.9001. | SearchBudgetLostImpressionShare |
| metrics\_search\_exact\_match\_impression\_share | The impressions you've received divided by the estimated number of impressions you were eligible to receive on the Search Network for search terms that matched your keywords exactly (or were close variants of your keyword), regardless of your keyword match types. Note: Search exact match impression share is reported in the range of 0.1 to 1. Any value below 0.1 is reported as 0.0999. | SearchExactMatchImpressionShare |
| metrics\_search\_impression\_share | The impressions you've received on the Search Network divided by the estimated number of impressions you were eligible to receive. Note: Search impression share is reported in the range of 0.1 to 1. Any value below 0.1 is reported as 0.0999. | SearchImpressionShare |
| metrics\_search\_rank\_lost\_impression\_share | The estimated percentage of impressions on the Search Network that your ads didn't receive due to poor Ad Rank. Note: Search rank lost impression share is reported in the range of 0 to 0.9. Any value above 0.9 is reported as 0.9001. | SearchRankLostImpressionShare |
| metrics\_value\_per\_all\_conversions | The value of all conversions divided by the number of all conversions. | ValuePerAllConversion |
| metrics\_video\_trueview\_view\_rate | The number of views your TrueView video ad receives divided by its number of impressions, including thumbnail impressions for TrueView in-display ads. | VideoViewRate |
| metrics\_video\_trueview\_views | The number of times your video ads were viewed. | VideoViews |
| segments\_ad\_network\_type | Ad network type. | AdNetworkType2 |
| segments\_date | Date to which metrics apply. yyyy-MM-dd format. For example, 2018-04-17. | Date |
| segments\_day\_of\_week | Day of the week. For example, MONDAY. | DayOfWeek |
| segments\_month | Month as represented by the date of the first day of a month. Formatted as yyyy-MM-dd. | Month |
| segments\_quarter | Quarter as represented by the date of the first day of a quarter. Uses the calendar year for quarters. For example, the second quarter of 2018 starts on 2018-04-01. Formatted as yyyy-MM-dd. | Quarter |
| segments\_week | Week as defined as Monday through Sunday, and represented by the date of Monday. Formatted as yyyy-MM-dd. | Week |
| segments\_year | Year, formatted as yyyy. | Year |

Google Ads Table Name: AccountStats

Google Ads API Resource:
[customer](https://developers.google.com/google-ads/api/fields/v22/customer)

| Google Ads Field Name | Description | Adwords Mapped Field Name |
| --- | --- | --- |
| customer\_id | The ID of the customer. | ExternalCustomerId |
| metrics\_active\_view\_cpm | Average cost of viewable impressions (`active\_view\_impressions`). | ActiveViewCpm |
| metrics\_active\_view\_ctr | Active view measurable clicks divided by active view viewable impressions. This metric is reported only for display network. | ActiveViewCtr |
| metrics\_active\_view\_impressions | A measurement of how often your ad has become viewable on a Display Network site. | ActiveViewImpressions |
| metrics\_active\_view\_measurability | The ratio of impressions that could be measured by Active View over the number of served impressions. | ActiveViewMeasurability |
| metrics\_active\_view\_measurable\_cost\_micros | The cost of the impressions you received that were measurable by Active View. | ActiveViewMeasurableCost |
| metrics\_active\_view\_measurable\_impressions | The number of times your ads are appearing on placements in positions where they can be seen. | ActiveViewMeasurableImpressions |
| metrics\_active\_view\_viewability | The percentage of time when your ad appeared on an Active View enabled site (measurable impressions) and was viewable (viewable impressions). | ActiveViewViewability |
| metrics\_average\_cost | The average amount you pay per interaction. This amount is the total cost of your ads divided by the total number of interactions. | AverageCost |
| metrics\_average\_cpc | The total cost of all clicks divided by the total number of clicks received. | AverageCpc |
| metrics\_average\_cpm | Average cost-per-thousand impressions (CPM). | AverageCpm |
| metrics\_clicks | The number of clicks. | Clicks |
| metrics\_conversions | The number of conversions. This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | Conversions |
| metrics\_conversions\_from\_interactions\_rate | Conversions from interactions divided by the number of ad interactions (such as clicks for text ads or views for video ads). This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | ConversionRate |
| metrics\_conversions\_value | The total value of conversions. This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | ConversionValue |
| metrics\_cost\_micros | The sum of your cost-per-click (CPC) and cost-per-thousand impressions (CPM) costs during this period. | Cost |
| metrics\_cost\_per\_conversion | The cost of ad interactions divided by conversions. This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | CostPerConversion |
| metrics\_ctr | The number of clicks your ad receives (Clicks) divided by the number of times your ad is shown (Impressions). | Ctr |
| metrics\_impressions | Count of how often your ad has appeared on a search results page or website on the Google Network. | Impressions |
| metrics\_interaction\_event\_types | The types of payable and free interactions. | InteractionTypes |
| metrics\_interaction\_rate | How often people interact with your ad after it is shown to them. This is the number of interactions divided by the number of times your ad is shown. | InteractionRate |
| metrics\_interactions | The number of interactions. An interaction is the main user action associated with an ad format, such as clicks for text and shopping ads or views for video ads. | Interactions |
| metrics\_value\_per\_conversion | The value of conversions divided by the number of conversions. This only includes conversion actions which include\_in\_conversions\_metric attribute is set to true. | ValuePerConversion |
| segments\_ad\_network\_type | Ad network type. | AdNetworkType2 |
| segments\_click\_type | Click type. | ClickType |
| segments\_date | Date to which metrics apply. yyyy-MM-dd format. For example, 2018-04-17. | Date |
| segments\_day\_of\_week | Day of the week. For example, MONDAY. | DayOfWeek |
| segments\_device | Device to which metrics apply. | Device |
| segments\_month | Month as represented by the date of the first day of a month. Formatted as yyyy-MM-dd. | Month |
| segments\_quarter | Quarter as represented by the date of the first day of a quarter. Uses the calendar year for quarters. For example, the second quarter of 2018 starts on 2018-04-01. Formatted as yyyy-MM-dd. | Quarter |
| segments\_week | Week as defined as Monday through Sunday, and represented by the date of Monday. Formatted as yyyy-MM-dd. | Week |
| segments\_year | Year, formatted as yyyy. | Year |

Google Ads Table Name: Ad

Google Ads API Resource:
[ad\_group\_ad](https://developers.google.com/google-ads/api/fields/v22/ad_group_ad)

| Google Ads Field Name | Description | Adwords Mapped Field Name |
| --- | --- | --- |
| ad\_group\_ad\_ad\_added\_by\_google\_ads | Indicates if this ad was automatically added by Google Ads and not by a user. For example, this could happen when ads are automatically created as suggestions for new ads based on knowledge of how existing ads are performing. | Automated |
| ad\_group\_ad\_ad\_app\_ad\_descriptions | List of text assets for descriptions. When the ad serves the descriptions, they are selected from this list. | UniversalAppAdDescriptions |
| ad\_group\_ad\_ad\_app\_ad\_headlines | List of text assets for headlines. When the ad serves the headlines is selected from this list. | UniversalAppAdHeadlines |
| ad\_group\_ad\_ad\_app\_ad\_html5\_media\_bundles | List of media bundle assets that may be used with the ad. | UniversalAppAdHtml5MediaBundles |
| ad\_group\_ad\_ad\_app\_ad\_images | List of image assets that may be displayed with the ad. | UniversalAppAdImages |
| ad\_group\_ad\_ad\_app\_ad\_mandatory\_ad\_text | An optional text asset that, if specified, must always be displayed when the ad is served. | UniversalAppAdMandatoryAdText |
| ad\_group\_ad\_ad\_app\_ad\_youtube\_videos | List of YouTube video assets that may be displayed with the ad. | UniversalAppAdYouTubeVideos |
| ad\_group\_ad\_ad\_call\_ad\_phone\_number | The phone number in the ad. | CallOnlyPhoneNumber |
| ad\_group\_ad\_ad\_device\_preference | The device preference for the ad. You can only specify a preference for mobile devices. When this preference is set, the ad is preferred over other ads when being displayed on a mobile device. The ad can still be displayed on other device types. For example, if no other ads are available. If unspecified (no device preference), all devices are targeted. This is only supported by some ad types. |  |
| ad\_group\_ad\_ad\_display\_url | The URL that appears in the ad description for some ad formats. | DisplayUrl |
| ad\_group\_ad\_ad\_expanded\_dynamic\_search\_ad\_description | The description of the ad. |  |
| ad\_group\_ad\_ad\_expanded\_dynamic\_search\_ad\_description2 | The second description of the ad. | ExpandedDynamicSearchCreativeDescription2 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_description | The description of the ad. |  |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_description2 | The second description of the ad. | ExpandedTextAdDescription2 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_headline\_part1 | The first part of the ad's headline. | HeadlinePart1 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_headline\_part2 | The second part of the ad's headline. | HeadlinePart2 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_headline\_part3 | The third part of the ad's headline. | ExpandedTextAdHeadlinePart3 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_path1 | The text that can appear alongside the ad's displayed URL. | Path1 |
| ad\_group\_ad\_ad\_expanded\_text\_ad\_path2 | Additional text that can appear alongside the ad's displayed URL. | Path2 |
| ad\_group\_ad\_ad\_final\_app\_urls | A list of final app URLs that are used on mobile if the user has the specific app installed. | CreativeFinalAppUrls |
| ad\_group\_ad\_ad\_final\_mobile\_urls | The list of possible final mobile URLs after all cross-domain redirects for the ad. | CreativeFinalMobileUrls |
| ad\_group\_ad\_ad\_final\_urls | The list of possible final URLs after all cross-domain redirects for the ad. | CreativeFinalUrls |
| ad\_group\_ad\_ad\_group | The ad group to which the ad belongs. |  |
| ad\_group\_ad\_ad\_id | The ID of the ad. | CreativeId |
| ad\_group\_ad\_ad\_image\_ad\_image\_url | URL of the full size image. | ImageAdUrl |
| ad\_group\_ad\_ad\_image\_ad\_mime\_type | The mime type of the image. | ImageCreativeMimeType |
| ad\_group\_ad\_ad\_image\_ad\_name | The name of the image. If the image was created from a MediaFile, this is the MediaFile's name. If the image was created from bytes, this is empty. | ImageCreativeName |
| ad\_group\_ad\_ad\_image\_ad\_pixel\_height | Height in pixels of the full size image. | ImageCreativeImageHeight |
| ad\_group\_ad\_ad\_image\_ad\_pixel\_width | Width in pixels of the full size image. | ImageCreativeImageWidth |
| ad\_group\_ad\_ad\_legacy\_responsive\_display\_ad\_accent\_color | The accent color of the ad in hexadecimal. For example, #ffffff for white. If one of main\_color and accent\_color is set, the other is required as well. | AccentColor |
| ad\_group\_ad\_ad\_legacy\_responsive\_display\_ad\_allow\_flexible\_color | Advertiser's consent to allow flexible color. When true, the ad may be served with different colors if necessary. When false, the ad is served with the specified colors or a neutral color. The default value is true. Must be true if main\_color and accent\_color are not set. | AllowFlexibleColor |
| ad\_group\_ad\_ad\_legacy\_responsive\_display\_ad\_business\_name | The business name in the ad. | BusinessName |
| ad\_group\_ad\_ad\_legacy\_responsive\_display\_ad\_call\_to\_action\_text | The call-to-action text for the ad. | CallToActionText |
| ad\_group\_ad\_ad\_legacy\_responsive\_display\_ad\_description | The description of the ad. | Description |
| ad\_group\_ad\_ad\_legacy\_responsive\_display\_ad\_format\_setting | Specifies which format the ad is served in. Default is ALL\_FORMATS. | FormatSetting |
| ad\_group\_ad\_ad\_legacy\_responsive\_display\_ad\_logo\_image | The MediaFile resource name of the logo image used in the ad. | EnhancedDisplayCreativeLandscapeLogoImageMediaId |
| ad\_group\_ad\_ad\_legacy\_responsive\_display\_ad\_long\_headline | The long version of the ad's headline. | LongHeadline |
| ad\_group\_ad\_ad\_legacy\_responsive\_display\_ad\_main\_color | The main color of the ad in hexadecimal. For example, #ffffff for white. If one of main\_color and accent\_color is set, the other is required as well. | MainColor |
| ad\_group\_ad\_ad\_legacy\_responsive\_display\_ad\_market |