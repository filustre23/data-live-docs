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

The following sections categorize report transformations based on report
types and specialized datasets.

### Account reports

The following reports focus on high-level account performance, bidding
strategies, and budget management.

| AdWords reports (deprecated) | BigQuery AdWords tables | Google Ads tables | Google Ads API resources (v25.0.0) | BigQuery views |
| --- | --- | --- | --- | --- |
| [Account Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/account-performance-report) | p\_Customer\_customer\_id  p\_HourlyAccountConversionStats\_customer\_id  p\_AccountConversionStats\_customer\_id  p\_HourlyAccountStats\_customer\_id  p\_AccountNonClickStats\_customer\_id  p\_AccountBasicStats\_customer\_id  p\_AccountStats\_customer\_id | p\_ads\_Customer\_customer\_id  p\_ads\_HourlyAccountConversionStats\_customer\_id  p\_ads\_AccountConversionStats\_customer\_id  p\_ads\_HourlyAccountStats\_customer\_id  p\_ads\_AccountNonClickStats\_customer\_id  p\_ads\_AccountBasicStats\_customer\_id  p\_ads\_AccountStats\_customer\_id | [Customer](https://developers.google.com/google-ads/api/fields/v25/customer) | Customer\_customer\_id  HourlyAccountConversionStats\_customer\_id  AccountConversionStats\_customer\_id  HourlyAccountStats\_customer\_id  AccountNonClickStats\_customer\_id  AccountBasicStats\_customer\_id  AccountStats\_customer\_id |
| [Bid Goal Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/bid-goal-performance-report) | p\_BidGoal\_customer\_id  p\_BidGoalStats\_customer\_id  p\_HourlyBidGoalStats\_customer\_id  p\_BidGoalConversionStats\_customer\_id | p\_ads\_BidGoal\_customer\_id  p\_ads\_BidGoalStats\_customer\_id  p\_ads\_HourlyBidGoalStats\_customer\_id  p\_ads\_BidGoalConversionStats\_customer\_id | [Bidding Strategy](https://developers.google.com/google-ads/api/fields/v25/bidding_strategy) | BidGoal\_customer\_id  BidGoalStats\_customer\_id  HourlyBidGoalStats\_customer\_id  BidGoalConversionStats\_customer\_id |
| [Budget Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/budget-performance-report) | p\_Budget\_customer\_id  p\_BudgetStats\_customer\_id | p\_ads\_Budget\_customer\_id  p\_ads\_BudgetStats\_customer\_id | [Campaign Budget](https://developers.google.com/google-ads/api/fields/v25/campaign_budget) | Budget\_customer\_id  BudgetStats\_customer\_id |

### Campaign reports

The following reports contain metrics for campaign-level performance and
location-based targeting.

| AdWords reports (deprecated) | BigQuery AdWords tables | Google Ads tables | Google Ads API resources (v25.0.0) | BigQuery views |
| --- | --- | --- | --- | --- |
| [Campaign Location Target Report](https://developers.google.com/adwords/api/docs/appendix/reports/campaign-location-target-report) | p\_CampaignLocationTargetStats\_customer\_id  p\_LocationBasedCampaignCriterion\_customer\_id | p\_ads\_CampaignLocationTargetStats\_customer\_id  p\_ads\_LocationBasedCampaignCriterion\_customer\_id | [Location View](https://developers.google.com/google-ads/api/fields/v25/location_view) | CampaignLocationTargetStats\_customer\_id  LocationBasedCampaignCriterion\_customer\_id |
| [Campaign Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/campaign-performance-report) | p\_Campaign\_customer\_id  p\_CampaignBasicStats\_customer\_id  p\_CampaignConversionStats\_customer\_id  p\_CampaignCrossDeviceStats\_customer\_id  p\_HourlyCampaignConversionStats\_customer\_id  p\_CampaignStats\_customer\_id  p\_HourlyCampaignStats\_customer\_id  p\_CampaignCrossDeviceConversionStats\_customer\_id  p\_CampaignCookieStats\_customer\_id | p\_ads\_Campaign\_customer\_id  p\_ads\_CampaignBasicStats\_customer\_id  p\_ads\_CampaignConversionStats\_customer\_id  p\_ads\_CampaignCrossDeviceStats\_customer\_id  p\_ads\_HourlyCampaignConversionStats\_customer\_id  p\_ads\_CampaignStats\_customer\_id  p\_ads\_HourlyCampaignStats\_customer\_id  p\_ads\_CampaignCrossDeviceConversionStats\_customer\_id  p\_ads\_CampaignCookieStats\_customer\_id | [Campaign](https://developers.google.com/google-ads/api/fields/v25/campaign) | Campaign\_customer\_id  CampaignBasicStats\_customer\_id  CampaignConversionStats\_customer\_id  CampaignCrossDeviceStats\_customer\_id  HourlyCampaignConversionStats\_customer\_id  CampaignStats\_customer\_id  HourlyCampaignStats\_customer\_id  CampaignCrossDeviceConversionStats\_customer\_id  CampaignCookieStats\_customer\_id |

### Ad group reports

The following reports focus on metrics at the ad group level.

| AdWords reports (deprecated) | BigQuery AdWords tables | Google Ads tables | Google Ads API resources (v25.0.0) | BigQuery views |
| --- | --- | --- | --- | --- |
| [Adgroup Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/adgroup-performance-report) | p\_AdGroupStats\_customer\_id  p\_AdGroupBasicStats\_customer\_id  p\_AdGroupCrossDeviceStats\_customer\_id  p\_HourlyAdGroupConversionStats\_customer\_id  p\_HourlyAdGroupStats\_customer\_id  p\_AdGroupConversionStats\_customer\_id  p\_AdGroupCrossDeviceConversionStats\_customer\_id  p\_AdGroup\_customer\_id | p\_ads\_AdGroupStats\_customer\_id  p\_ads\_AdGroupBasicStats\_customer\_id  p\_ads\_AdGroupCrossDeviceStats\_customer\_id  p\_ads\_HourlyAdGroupConversionStats\_customer\_id  p\_ads\_HourlyAdGroupStats\_customer\_id  p\_ads\_AdGroupConversionStats\_customer\_id  p\_ads\_AdGroupCrossDeviceConversionStats\_customer\_id  p\_ads\_AdGroup\_customer\_id | [Ad Group](https://developers.google.com/google-ads/api/fields/v25/ad_group) | AdGroupStats\_customer\_id  AdGroupBasicStats\_customer\_id  AdGroupCrossDeviceStats\_customer\_id  HourlyAdGroupConversionStats\_customer\_id  HourlyAdGroupStats\_customer\_id  AdGroupConversionStats\_customer\_id  AdGroupCrossDeviceConversionStats\_customer\_id  AdGroup\_customer\_id |

### Ad reports

The following reports are for individual ad performance.

| AdWords reports (deprecated) | BigQuery AdWords tables | Google Ads tables | Google Ads API resources (v25.0.0) | BigQuery views |
| --- | --- | --- | --- | --- |
| [Ad Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/ad-performance-report) | p\_AdBasicStats\_customer\_id  p\_AdCrossDeviceStats\_customer\_id  p\_AdConversionStats\_customer\_id  p\_AdStats\_customer\_id  p\_AdCrossDeviceConversionStats\_customer\_id  p\_Ad\_customer\_id | p\_ads\_AdBasicStats\_customer\_id  p\_ads\_AdCrossDeviceStats\_customer\_id  p\_ads\_AdConversionStats\_customer\_id  p\_ads\_AdStats\_customer\_id  p\_ads\_AdCrossDeviceConversionStats\_customer\_id  p\_ads\_Ad\_customer\_id | [Ad Group Ad](https://developers.google.com/google-ads/api/fields/v25/ad_group_ad) | AdBasicStats\_customer\_id  AdCrossDeviceStats\_customer\_id  AdConversionStats\_customer\_id  AdStats\_customer\_id  AdCrossDeviceConversionStats\_customer\_id  Ad\_customer\_id |

### Demographics reports

The following reports include performance data broken down by user demographic
characteristics.

| AdWords reports (deprecated) | BigQuery AdWords tables | Google Ads tables | Google Ads API resources (v25.0.0) | BigQuery views |
| --- | --- | --- | --- | --- |
| [Age Range Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/age-range-performance-report) | p\_AgeRange\_customer\_id  p\_AgeRangeBasicStats\_customer\_id  p\_AgeRangeStats\_customer\_id  p\_AgeRangeConversionStats\_customer\_id  p\_AgeRangeNonClickStats\_customer\_id | p\_ads\_AgeRange\_customer\_id  p\_ads\_AgeRangeBasicStats\_customer\_id  p\_ads\_AgeRangeStats\_customer\_id  p\_ads\_AgeRangeConversionStats\_customer\_id  p\_ads\_AgeRangeNonClickStats\_customer\_id | [Age Range View](https://developers.google.com/google-ads/api/fields/v25/age_range_view) | AgeRange\_customer\_id  AgeRangeBasicStats\_customer\_id  AgeRangeStats\_customer\_id  AgeRangeConversionStats\_customer\_id  AgeRangeNonClickStats\_customer\_id |
| [Gender Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/gender-performance-report) | p\_Gender\_customer\_id  p\_GenderBasicStats\_customer\_id  p\_GenderStats\_customer\_id  p\_GenderConversionStats\_customer\_id  p\_GenderNonClickStats\_customer\_id | p\_ads\_Gender\_customer\_id  p\_ads\_GenderBasicStats\_customer\_id  p\_ads\_GenderStats\_customer\_id  p\_ads\_GenderConversionStats\_customer\_id  p\_ads\_GenderNonClickStats\_customer\_id | [Gender View](https://developers.google.com/google-ads/api/fields/v25/gender_view) | Gender\_customer\_id  GenderBasicStats\_customer\_id  GenderStats\_customer\_id  GenderConversionStats\_customer\_id  GenderNonClickStats\_customer\_id |
| [Parental Status Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/parental-status-performance-report) | p\_ParentalStatus\_customer\_id  p\_ParentalStatusBasicStats\_customer\_id  p\_ParentalStatusStats\_customer\_id  p\_ParentalStatusConversionStats\_customer\_id  p\_ParentalStatusNonClickStats\_customer\_id | p\_ads\_ParentalStatus\_customer\_id  p\_ads\_ParentalStatusBasicStats\_customer\_id  p\_ads\_ParentalStatusStats\_customer\_id  p\_ads\_ParentalStatusConversionStats\_customer\_id  p\_ads\_ParentalStatusNonClickStats\_customer\_id | [Parental Status View](https://developers.google.com/google-ads/api/fields/v25/parental_status_view) | ParentalStatus\_customer\_id  ParentalStatusBasicStats\_customer\_id  ParentalStatusStats\_customer\_id  ParentalStatusConversionStats\_customer\_id  ParentalStatusNonClickStats\_customer\_id |

### Keywords and search reports

The following reports cover keyword performance, search terms, and combined
paid and organic query data.

| AdWords reports (deprecated) | BigQuery AdWords tables | Google Ads tables | Google Ads API resources (v25.0.0) | BigQuery views |
| --- | --- | --- | --- | --- |
| [Keywords Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/keywords-performance-report) | p\_Keyword\_customer\_id  p\_KeywordBasicStats\_customer\_id  p\_KeywordCrossDeviceStats\_customer\_id  p\_KeywordStats\_customer\_id  p\_KeywordCrossDeviceConversionStats\_customer\_id  p\_KeywordConversionStats\_customer\_id | p\_ads\_Keyword\_customer\_id  p\_ads\_KeywordBasicStats\_customer\_id  p\_ads\_KeywordCrossDeviceStats\_customer\_id  p\_ads\_KeywordStats\_customer\_id  p\_ads\_KeywordCrossDeviceConversionStats\_customer\_id  p\_ads\_KeywordConversionStats\_customer\_id | [Keyword View](https://developers.google.com/google-ads/api/fields/v25/keyword_view) | Keyword\_customer\_id  KeywordBasicStats\_customer\_id  KeywordCrossDeviceStats\_customer\_id  KeywordStats\_customer\_id  KeywordCrossDeviceConversionStats\_customer\_id  KeywordConversionStats\_customer\_id |
| [Paid Organic Query Report](https://developers.google.com/adwords/api/docs/appendix/reports/paid-organic-query-report) | p\_PaidOrganicStats\_customer\_id | p\_ads\_PaidOrganicStats\_customer\_id | [Paid Organic Search Term View](https://developers.google.com/google-ads/api/fields/v25/paid_organic_search_term_view) | PaidOrganicStats\_customer\_id |
| [Search Query Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/search-query-performance-report) | p\_SearchQueryStats\_customer\_id  p\_SearchQueryConversionStats\_customer\_id | p\_ads\_SearchQueryStats\_customer\_id  p\_ads\_SearchQueryConversionStats\_customer\_id | [Search Term View](https://developers.google.com/google-ads/api/fields/v25/search_term_view) | SearchQueryStats\_customer\_id  SearchQueryConversionStats\_customer\_id |

### Audience and targeting reports

The following reports are related to audience views, criteria, and managed
placements.

| AdWords reports (deprecated) | BigQuery AdWords tables | Google Ads tables | Google Ads API resources (v25.0.0) | BigQuery views |
| --- | --- | --- | --- | --- |
| [Audience Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/audience-performance-report) | p\_Audience\_customer\_id  p\_AudienceConversionStats\_customer\_id  p\_AudienceNonClickStats\_customer\_id  p\_AudienceBasicStats\_customer\_id  p\_AudienceStats\_customer\_id | `NULL`  `NULL`  `NULL`  `NULL`  `NULL` | [Ad Group Audience View](https://developers.google.com/google-ads/api/fields/v25/ad_group_audience_view)  [Campaign Audience View](https://developers.google.com/google-ads/api/fields/v25/campaign_audience_view) | Audience\_customer\_id  AudienceConversionStats\_customer\_id  AudienceNonClickStats\_customer\_id  AudienceBasicStats\_customer\_id  AudienceStats\_customer\_id |
| [Criteria Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/criteria-performance-report) | p\_Criteria\_customer\_id  p\_CriteriaBasicStats\_customer\_id  p\_CriteriaStats\_customer\_id  p\_CriteriaConversionStats\_customer\_id  p\_CriteriaNonClickStats\_customer\_id | `NULL`  `NULL`  `NULL`  `NULL`  `NULL` |  | Criteria\_customer\_id  CriteriaBasicStats\_customer\_id  CriteriaStats\_customer\_id  CriteriaConversionStats\_customer\_id  CriteriaNonClickStats\_customer\_id |
| [Placement Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/placement-performance-report) | p\_PlacementBasicStats\_customer\_id  p\_PlacementNonClickStats\_customer\_id  p\_PlacementStats\_customer\_id  p\_Placement\_customer\_id  p\_PlacementConversionStats\_customer\_id | p\_ads\_PlacementBasicStats\_customer\_id  p\_ads\_PlacementNonClickStats\_customer\_id  p\_ads\_PlacementStats\_customer\_id  p\_ads\_Placement\_customer\_id  p\_ads\_PlacementConversionStats\_customer\_id | [Managed Placement View](https://developers.google.com/google-ads/api/fields/v25/managed_placement_view) | PlacementBasicStats\_customer\_id  PlacementNonClickStats\_customer\_id  PlacementStats\_customer\_id  Placement\_customer\_id  PlacementConversionStats\_customer\_id |

### Shopping and video reports

The following reports focus on specialized campaign channels.

| AdWords reports (deprecated) | BigQuery AdWords tables | Google Ads tables | Google Ads API resources (v25.0.0) | BigQuery views |
| --- | --- | --- | --- | --- |
| [Shopping Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/shopping-performance-report) | p\_ShoppingProductConversionStats\_customer\_id  p\_ShoppingProductStats\_customer\_id | p\_ads\_ShoppingProductConversionStats\_customer\_id  p\_ads\_ShoppingProductStats\_customer\_id | [Shopping Performance View](https://developers.google.com/google-ads/api/fields/v25/shopping_performance_view) | ShoppingProductConversionStats\_customer\_id  ShoppingProductStats\_customer\_id |
| [Video Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/video-performance-report) | p\_VideoBasicStats\_customer\_id  p\_VideoConversionStats\_customer\_id  p\_VideoStats\_customer\_id  p\_Video\_customer\_id  p\_VideoNonClickStats\_customer\_id | p\_ads\_VideoBasicStats\_customer\_id  p\_ads\_VideoConversionStats\_customer\_id  p\_ads\_VideoStats\_customer\_id  p\_ads\_Video\_customer\_id  p\_ads\_VideoNonClickStats\_customer\_id | [Video](https://developers.google.com/google-ads/api/fields/v25/video) | VideoBasicStats\_customer\_id  VideoConversionStats\_customer\_id  VideoStats\_customer\_id  Video\_customer\_id  VideoNonClickStats\_customer\_id |

### Geography and click reports

The following reports present detailed metrics on user geography and
click-level data.

| AdWords reports (deprecated) | BigQuery AdWords tables | Google Ads tables | Google Ads API resources (v25.0.0) | BigQuery views |
| --- | --- | --- | --- | --- |
| [Click Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/click-performance-report) | p\_ClickStats\_customer\_id | p\_ads\_ClickStats\_customer\_id | [Click View](https://developers.google.com/google-ads/api/fields/v25/click_view) | ClickStats\_customer\_id |
| [Geo Performance Report](https://developers.google.com/adwords/api/docs/appendix/reports/geo-performance-report) | p\_GeoConversionStats\_customer\_id  p\_GeoStats\_customer\_id | p\_ads\_GeoConversionStats\_customer\_id  p\_ads\_GeoStats\_customer\_id | [Geographic View](https://developers.google.com/google-ads/api/fields/v25/geographic_view) | GeoConversionStats\_customer\_id  GeoStats\_customer\_id |

### Attribute and label tables

The following tables provide mapping information for attribute settings and
label assignments, such as CampaignLabel, AdGroupLabel, and AdGroupBidModifier.

| Google Ads tables | Google Ads API resources (v25.0.0) |
| --- | --- |
| AdGroupBidModifier | [Ad Group Bid Modifier](https://developers.google.com/google-ads/api/fields/v25/ad_group_bid_modifier) |
| AdGroupAdLabel | [Ad Group Ad Label](https://developers.google.com/google-ads/api/fields/v25/ad_group_ad_label) |
| CampaignLabel | [Campaign Label](https://developers.google.com/google-ads/api/fields/v25/campaign_label) |
| CampaignCriterion | [Campaign Criterion](https://developers.google.com/google-ads/api/fields/v25/campaign_criterion) |
| AdGroupLabel | [Ad Group Label](https://developers.google.com/google-ads/api/fields/v25/ad_group_label) |
| AdGroupAudience  AdGroupAudienceStats  AdGroupAudienceConversionStats  AdGroupAudienceNonClickStats  AdGroupAudienceBasicStats | [Ad Group Audience View](https://developers.google.com/google-ads/api/fields/v25/ad_group_audience_view) |

### Performance Max (PMax) tables

The following tables are dedicated to Performance Max assets and signals, such
as AssetGroup and CampaignAssetStats.

| Google Ads tables | Google Ads API resources (v25.0.0) |
| --- | --- |
| Assets (available if [Pmax](https://developers.google.com/google-ads/api/docs/performance-max/overview) data is enabled) | [Assets](https://developers.google.com/google-ads/api/fields/v25/asset) |
<