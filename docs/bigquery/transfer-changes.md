Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料移轉服務資料來源變更記錄

本頁詳細說明 BigQuery 資料移轉服務資料來源結構定義和結構定義對應的變更。如要瞭解 BigQuery 資料移轉服務連接器即將推出的異動，請在本頁搜尋資料來源 (例如 `Google Ads API` 或 `Display & Video 360 API`)，或搜尋特定資料表名稱或值。

## Campaign Manager 360

Campaign Manager 360 連接器的 BigQuery 資料移轉服務會定期更新，支援新增、淘汰或遷移的資料欄。Campaign Manager 360 連接器的 BigQuery 資料移轉服務會從 Campaign Manager 360 [資料移轉檔案](https://developers.google.com/doubleclick-advertisers/dtv2/reference/release-notes?hl=zh-tw)擷取資料。

以下各節將概略說明異動內容。異動項目會依發布日期排序，每個項目都會提供相關資訊，說明您需要進行哪些變更，才能繼續接收 Campaign Manager 360 的資料。

### 2025 年 7 月 7 日

Campaign Manager 360 [宣布](https://support.google.com/campaignmanager/answer/16320235?hl=zh-tw#111)，將更新瀏覽器、作業系統、行動裝置廠商和型號，以及 ISP 資料的條件 ID，符合跨平台資料標準。遷移完成後，Campaign Manager 360 將停止填入已淘汰資料欄的值，並開始填入新資料欄。受影響的資料欄如下：

| 已淘汰的資料欄 | 新的資料欄 |
| --- | --- |
| `DBM_Browser_Platform_ID` | `DV360_Browser_Platform_Reportable_ID` |
| `DBM_ISP_ID` | `DV360_ISP_Reportable_ID` |
| `DBM_Operating_System_ID` | `DV360_Operating_System_Reportable_ID` |
| `DBM_Mobile_Make_ID` | `DV360_Mobile_Make_Reportable_ID` |
| `DBM_Mobile_Model_ID` | `DV360_Mobile_Model_Reportable_ID` |

## Display & Video 360 API

Display & Video 360 連接器的 BigQuery 資料移轉服務會定期更新，以支援新資料欄，並因應新版 [Display & Video 360 API](https://developers.google.com/display-video/api/release-notes?hl=zh-tw) 帶來的異動。Display & Video 360 連接器的 BigQuery 資料移轉服務會使用支援的 API 版本擷取[設定資料](https://docs.cloud.google.com/bigquery/docs/display-video-transfer?hl=zh-tw#supported_configuration_data)。

以下各節將說明更新至新版 Display & Video 360 API 時的異動。異動項目會依發布日期排序，每個項目都會提供相關資訊，說明您需要進行哪些變更，才能繼續接收 Display & Video 360 的資料。

### 2025 年 8 月 26 日

[Display & Video 360 連接器](https://docs.cloud.google.com/bigquery/docs/display-video-transfer?hl=zh-tw)計畫將用於擷取設定資料的 [Display & Video 360 API 版本](https://developers.google.com/display-video/api/release-notes?hl=zh-tw)從 [v3](https://developers.google.com/display-video/api/reference/rest/v3?hl=zh-tw) 更新為 [v4](https://developers.google.com/display-video/api/reference/rest/v4?hl=zh-tw)。API 升級帶來的異動列於下方。詳情請參閱「[Display & Video 360 API 第 3 版至第 4 版遷移指南](https://developers.google.com/display-video/api/v4-migration-guide?hl=zh-tw)」。

Display & Video 360 連接器預計於 2025 年 8 月 26 日更新。

#### 已淘汰的資料表

下列資料表將停止接收新資料。現有資料會保留，但不會再更新。

* `CampaignTargeting`
* `InsertionOrderTargeting`

#### 資料欄已重新命名的資料表

| 受影響的資料表 | 已淘汰的資料欄 | 新的資料欄 |
| --- | --- | --- |
| * `AdGroupTargeting` * `LineItemTargeting` | `audienceGroupDetails.includedFirstAndThirdPartyAudienceGroups` | `audienceGroupDetails.includedFirstPartyAndPartnerAudienceGroups` |
| `audienceGroupDetails.includedFirstAndThirdPartyAudienceGroups.settings` | `audienceGroupDetails.includedFirstPartyAndPartnerAudienceGroups.settings` |
| `audienceGroupDetails.includedFirstAndThirdPartyAudienceGroups.settings.firstAndThirdPartyAudienceId` | `audienceGroupDetails.includedFirstPartyAndPartnerAudienceGroups.settings.firstPartyAndPartnerAudienceId` |
| `audienceGroupDetails.includedFirstAndThirdPartyAudienceGroups.settings.recency` | `audienceGroupDetails.includedFirstPartyAndPartnerAudienceGroups.settings.recency` |
| `audienceGroupDetails.excludedFirstAndThirdPartyAudienceGroup` | `audienceGroupDetails.excludedFirstPartyAndPartnerAudienceGroup` |
| `audienceGroupDetails.excludedFirstAndThirdPartyAudienceGroup.settings` | `audienceGroupDetails.excludedFirstPartyAndPartnerAudienceGroup.settings` |
| `audienceGroupDetails.excludedFirstAndThirdPartyAudienceGroup.settings.firstAndThirdPartyAudienceId` | `audienceGroupDetails.excludedFirstPartyAndPartnerAudienceGroup.settings.firstPartyAndPartnerAudienceId` |
| `audienceGroupDetails.excludedFirstAndThirdPartyAudienceGroup.settings.recency` | `audienceGroupDetails.excludedFirstPartyAndPartnerAudienceGroup.settings.recency` |

#### 含有已淘汰資料欄的資料表

| 受影響的資料表 | 已淘汰的資料欄 |
| --- | --- |
| `Creative` | `reviewStatus.publisherReviewStatuses` |

## Facebook 廣告

Facebook Ads 連接器的 BigQuery 資料移轉服務會定期更新，以因應 Facebook Ads 導入的新異動。

以下各節將按照發布日期列出異動。

### 2026 年 7 月 6 日

2026 年 7 月 6 日起，[Facebook Ads 連接器](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw)會暫時停用 Facebook Ads 廣告資料移轉作業的 `AdInsightsMMM` 報表。Facebook Ads API 最近有所異動，指定行銷區域 (DMA) 欄已淘汰，因此查詢這項細目時會傳回空白結果。為避免資料移轉失敗，我們做出這項調整。

包含 `AdInsightsMMM` 報表的 Facebook Ads 現有資料移轉作業會繼續執行，但移轉作業不會包含 `AdInsightsMMM` 報表的資料。

### 2026 年 7 月 25 日

2026 年 7 月 25 日，[Facebook Ads 連接器](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer?hl=zh-tw)預計將 `AdInsightsActions` 報表中 `ActionValue` 欄位的資料類型對應，從 `INT` 更新為 `FLOAT`。這項變更旨在更準確地反映來源資料，並確保資料完整性。

## Google Ads API

Google Ads 適用的 BigQuery 資料移轉服務會定期更新，以支援新資料欄，並因應 [Google Ads API](https://developers.google.com/google-ads/api/docs/release-notes?hl=zh-tw) 帶來的異動。Google Ads 適用的 BigQuery 資料移轉服務連接器，會使用 Google Ads 連接器中[支援的 API 版本](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#connector_overview)。

以下各節將概略說明 Google Ads API 帶來的異動。變更項目會依發布日期排序，每個項目都會提供相關資訊，說明您需要進行哪些變更，才能繼續接收 Google Ads 資料。

如要進一步瞭解 Google Ads API 發布時間表，請參閱[時間表](https://developers.google.com/google-ads/api/docs/sunset-dates?hl=zh-tw#timetable)。

### 2026 年 6 月 15 日

[Google Ads 連接器](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)預計將 [Google Ads API 版本](https://developers.google.com/google-ads/api/docs/release-notes?hl=zh-tw)從 [v22](https://developers.google.com/google-ads/api/fields/v22/overview?hl=zh-tw) 更新至 [v23](https://developers.google.com/google-ads/api/fields/v23/overview?hl=zh-tw)。API 升級後，受影響資料表中新移轉資料的資料欄值會變更。詳情請參閱「[Google Ads API 升級](https://developers.google.com/google-ads/api/docs/upgrade?hl=zh-tw#v22-v23)」。

| 已淘汰的資料欄 | 新的資料欄 | 受影響的資料表 |
| --- | --- | --- |
| `campaign_start_date` | `campaign_start_date_time` | `Campaign` |
| `campaign_end_date` | `campaign_end_date_time` |

2026 年 4 月 3 日前，Google Ads 連接器會在資料表架構中新增 `campaign_start_date_time` 和 `campaign_end_date_time` 欄，並填入 `null`。2026 年 6 月 15 日，Google Ads API 更新至第 23 版後，這些新資料欄將填入新值和新資料類型 [datetime](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#datetime_type)。`campaign_start_date` 和 `campaign_end_date` 將會淘汰，並填入 `null`，但仍會保留在資料表架構中。

每組資料欄中，只有一欄會填入 Google Ads API 的值，另一欄則會填入 `null`。為因應 Google Ads API v23 更新，請更新查詢，指定其中一欄。如果 SQL 查詢選取了已淘汰的資料欄，請更新查詢，指定正確的資料欄，例如：

```
IFNULL(DATE(campaign_start_date_time), campaign_start_date)
```

### 2026 年 6 月 8 日

下列資料欄將於 2026 年 6 月 8 日淘汰。新移轉的資料會填入 `null`。

| 已淘汰的資料欄 | 受影響的資料表 |
| --- | --- |
| `ad_group_ad_ad_call_ad_phone_number` | `Ad` |

### 2026 年 6 月 1 日

2026 年 6 月 1 日起，Google Ads 連接器將限制每日資料補充作業，僅限最近 37 個月。如果嘗試回填 37 個月前的資料，系統會傳回錯誤。這項異動是為了因應 [2026 年 6 月 1 日起實施的 Google Ads 新版資料保留政策](https://ads-developers.googleblog.com/2026/05/new-data-retention-policy-for-google.html)。

已移轉並儲存在 BigQuery 資料表中的資料則不受影響。

### 2026 年 5 月 7 日

2026 年 5 月 7 日起，Google Ads 將要求[使用者必須通過多重驗證 (MFA)](https://ads-developers.googleblog.com/2026/04/multi-factor-authentication-requirement.html)。
現有的移轉設定和移轉作業不會受到影響。如要建立新的移轉設定，並以個別使用者憑證授權，則必須啟用[兩步驟驗證](https://support.google.com/accounts/answer/185839?hl=zh-tw)。使用服務帳戶授權的新移轉設定，不需要兩步驟驗證。

### 2026 年 3 月 2 日

[Google Ads 連接器](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)預計將 [Google Ads API 版本](https://developers.google.com/google-ads/api/docs/release-notes?hl=zh-tw)從 [v21](https://developers.google.com/google-ads/api/fields/v21/overview?hl=zh-tw) 更新至 [v22](https://developers.google.com/google-ads/api/fields/v22/overview?hl=zh-tw)。API 升級後，受影響資料表中新移轉資料的資料欄值會變更。詳情請參閱「[Google Ads API 升級](https://developers.google.com/google-ads/api/docs/upgrade?hl=zh-tw#v21-v22)」。

| 已淘汰的資料欄 | 新的資料欄 | 受影響的資料表 |
| --- | --- | --- |
| `metrics_average_cpv` | `metrics_trueview_average_cpv` | * `AccountNonClickStats` * `AdCrossDeviceStats` * `AdGroupAudienceNonClickStats` * `AdGroupCrossDeviceStats` * `AgeRangeNonClickStats` * `BudgetStats` * `CampaignAssetStats` * `CampaignAudienceNonClickStats` * `CampaignCrossDeviceStats` * `CampaignLocationTargetStats` * `DisplayVideoAutomaticPlacementsStats` * `DisplayVideoKeywordStats` * `GenderNonClickStats` * `GeoStats` * `KeywordCrossDeviceStats` * `ParentalStatusNonClickStats` * `PlacementNonClickStats` * `SearchQueryStats` * `VideoNonClickStats` |
| `metrics_video_view_rate` | `metrics_video_trueview_view_rate` | * `AccountNonClickStats` * `AdCrossDeviceStats` * `AdGroupAudienceNonClickStats` * `AdGroupCrossDeviceStats` * `AgeRangeNonClickStats` * `BudgetStats` * `CampaignAudienceNonClickStats` * `CampaignCrossDeviceStats` * `CampaignLocationTargetStats` * `DisplayVideoAutomaticPlacementsStats` * `GenderNonClickStats` * `GeoStats` * `KeywordCrossDeviceStats` * `ParentalStatusNonClickStats` * `PlacementNonClickStats` * `SearchQueryStats` * `VideoNonClickStats` |
| `metrics_video_views` | `metrics_video_trueview_views` | * `AccountNonClickStats` * `AdCrossDeviceStats` * `AdGroupAudienceNonClickStats` * `AdGroupCrossDeviceStats` * `AgeRangeNonClickStats` * `BudgetStats` * `CampaignAudienceNonClickStats` * `CampaignCrossDeviceStats` * `CampaignLocationTargetStats` * `DisplayVideoAutomaticPlacementsStats` * `GenderNonClickStats` * `GeoStats` * `KeywordCrossDeviceStats` * `ParentalStatusNonClickStats` * `PlacementNonClickStats` * `SearchQueryStats` * `VideoNonClickStats` |

2026 年 1 月 16 日前，Google Ads 連接器會將 `metrics_trueview_average_cpv`、`metrics_video_trueview_view_rate` 和 `metrics_video_trueview_views` 資料欄新增至資料表結構定義，並填入 `null`。2026 年 3 月 2 日 Google Ads API 更新至第 22 版後，這些新資料欄將填入新值。部分資料欄現已淘汰，例如 `metrics_average_cpv`、`metrics_video_view_rate` 和 `metrics_video_views`。已淘汰的資料欄現在會填入 `null`，但仍會保留在資料表結構定義中。

每組資料欄中，只有一欄會填入 Google Ads API 的值，另一欄則會填入 `null`。為因應 Google Ads API v22 更新，請更新查詢，指定其中一個資料欄。舉例來說，如果 SQL 查詢選取 `metrics_average_cpv` 欄，請更新查詢，指定正確的欄：

```
IFNULL(metrics_average_cpv, metrics_trueview_average_cpv)
```

如果您使用[自訂報表](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#custom_reports)，請參閱 [Google Ads API 第 22 版參考頁面](https://developers.google.com/google-ads/api/fields/v22/overview?hl=zh-tw)和 [Google Ads API 版本資訊](https://developers.google.com/google-ads/api/docs/release-notes?hl=zh-tw)，在 [Google Ads 連接器](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)升級至 Google Ads API 第 22 版後，更新受影響的 GAQL 查詢。
如果您使用[自訂報表](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw#custom_reports)，請參閱 [Google Ads API 第 22 版參考頁面](https://developers.google.com/google-ads/api/fields/v22/overview?hl=zh-tw)和 [Google Ads API 版本資訊](https://developers.google.com/google-ads/api/docs/release-notes?hl=zh-tw)，在 [Google Ads 連接器](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)升級至 Google Ads API 第 22 版後，更新受影響的 GAQL 查詢。

### 2025 年 8 月 1 日

[Google Ads 移轉作業](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)預計將 [Google Ads API 版本](https://developers.google.com/google-ads/api/docs/release-notes?hl=zh-tw)從 [v18](https://developers.google.com/google-ads/api/reference/rpc/v18/overview?hl=zh-tw) 更新至 [v20](https://developers.google.com/google-ads/api/reference/rpc/v20/overview?hl=zh-tw)。API 升級後，受影響資料表中新移轉資料的資料欄值會變更。詳情請參閱「[Google Ads API 升級](https://developers.google.com/google-ads/api/docs/upgrade?hl=zh-tw#v18-v19)」。

#### 資料表：`p_ads_Ad_customer_id`

| 受影響的資料欄 | 已淘汰的資料類型 |
| --- | --- |
| ad\_group\_type | VIDEO\_OUTSTREAM |
| ad\_group\_ad\_ad\_type | VIDEO\_OUTSTREAM |

#### 資料表：`p_ads_Campaign_customer_id`

| 受影響的資料欄 | 已淘汰的資料類型 |
| --- | --- |
| campaign\_advertising\_channel\_sub\_type | VIDEO\_OUTSTREAM |

#### 資料表：`p_ads_DisplayVideoKeywordStats_customer_id`

| 受影響的資料欄 | 已淘汰的資料類型 |
| --- | --- |
| campaign\_advertising\_channel\_sub\_type | VIDEO\_OUTSTREAM |

### 2025 年 1 月 20 日

[Google Ads 移轉作業](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)計畫將 [Google Ads API 版本](https://developers.google.com/google-ads/api/docs/release-notes?hl=zh-tw)從 [v16](https://developers.google.com/google-ads/api/reference/rpc/v16/overview?hl=zh-tw) 更新至 [v18](https://developers.google.com/google-ads/api/reference/rpc/v18/overview?hl=zh-tw)。API 升級後，受影響資料表中新移轉資料的資料欄值會變更。詳情請參閱「[Google Ads API 升級](https://developers.google.com/google-ads/api/docs/upgrade?hl=zh-tw#v17-v18)」。

Google Ads 連接器更新作業已於 2025 年 1 月 20 日開始，並於 2025 年 2 月 4 日完成。

#### 資料表：`p_ads_Campaign_customer_id`

| 受影響的資料欄 | 舊值 (v16) | 新值 (v18) |
| --- | --- | --- |
| campaign\_advertising\_channel\_type | DISCOVERY | DEMAND\_GEN |

#### 資料表：`p_ads_Ad_customer_id`

| 受影響的資料欄 | 舊值 (v16) | 新值 (v18) |
| --- | --- | --- |
| ad\_type | DISCOVERY\_MULTI\_ASSET\_AD  DISCOVERY\_CAROUSEL\_AD  DISCOVERY\_VIDEO\_RESPONSIVE\_AD | DEMAND\_GEN\_MULTI\_ASSET\_AD  DEMAND\_GEN\_CAROUSEL\_AD  DEMAND\_GEN\_VIDEO\_RESPONSIVE\_AD |

#### 資料表：`Asset`

| 受影響的資料欄 | 舊值 (v16) | 新值 (v18) |
| --- | --- | --- |
| asset\_type | DISCOVERY\_CAROUSEL\_CARD | DEMAND\_GEN\_CAROUSEL\_CARD |

為確保查詢在更新後仍可運作，請變更查詢，同時選取新舊值。舉例來說，如果 SQL 查詢中有下列 `WHERE` 條件：

```
WHERE asset_type='DISCOVERY_CAROUSEL_CARD'
```

替換為下列陳述式：

```
WHERE
  asset_type='DISCOVERY_CAROUSEL_CARD'
  OR asset_type='DEMAND_GEN_CAROUSEL_CARD'
```

### 2024 年 6 月 24 日

[Google Ads 移轉作業](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw)計畫將 [Google Ads API 版本](https://developers.google.com/google-ads/api/docs/release-notes?hl=zh-tw)從 v14 更新至 [v16](https://developers.google.com/google-ads/api/reference/rpc/v16/overview?hl=zh-tw)。在這次 API 升級中，受影響資料表中新移轉資料的資料欄名稱會變更。此外，部分資料欄已淘汰。詳情請參閱「[Google Ads API 升級](https://developers.google.com/google-ads/api/docs/upgrade?hl=zh-tw#v17-v18)」。

Google Ads 連接器更新作業已於 2024 年 6 月 17 日開始，並於 2024 年 6 月 23 日完成。

| 受影響的資料表 | 已淘汰的資料欄 | 新的資料欄 |
| --- | --- | --- |
| * `ShoppingProductStats` * `ShoppingProductConversionStats` | `segments_product_bidding_category_level1` | `segments_product_category_level1` |
| `segments_product_bidding_category_level2` | `segments_product_category_level2` |
| `segments_product_bidding_category_level3` | `segments_product_category_level3` |
| `segments_product_bidding_category_level4` | `segments_product_category_level4` |
| `segments_product_bidding_category_level5` | `segments_product_category_level5` |
| * `ProductGroupStats` | `ad_group_criterion_listing_group_case_value_product_bidding_category_id` | `ad_group_criterion_listing_group_case_value_product_category_category_id` |
| `ad_group_criterion_listing_group_case_value_product_bidding_category_level` | `ad_group_criterion_listing_group_case_value_product_category_level` |
| * `AssetGroupListingFilter` | `asset_group_listing_group_filter_case_value_product_bidding_category_id` | `asset_group_listing_group_filter_case_value_product_category_category_id` |
| `asset_group_listing_group_filter_case_value_product_bidding_category_level` | `asset_group_listing_group_filter_case_value_product_category_level` |
| `asset_group_listing_group_filter_vertical` | `asset_group_listing_group_filter_listing_source` |

Google Ads API 14 版在 BigQuery 資料表結構定義中新增了 `segments_product_category_level1` 和 `segments_product_category_level2` 等資料欄，但填入的是 `null`。Google Ads API 更新至第 16 版後，這些新資料欄會填入新值。`segments_product_bidding_category_level1` 和 `segments_product_bidding_category_level2` 等已淘汰的資料欄會填入 `null`，但仍會保留在資料表結構定義中。

每組資料欄中，只有一欄會填入 Google Ads API 的值，另一欄則會填入 `null`。為確保現有查詢在更新後仍能正常運作，請更新查詢，選擇其中一欄。舉例來說，如果 SQL 查詢中包含下列陳述式：

```
segments_product_bidding_category_level1
```

請改用下列陳述式，指定正確的資料欄：

```
IFNULL(segments_product_category_level1, segments_product_bidding_category_level1)
```

2024 年 6 月 24 日後建立的移轉設定，一律會使用新資料欄。已淘汰的資料欄仍會保留在資料表結構定義中，但會填入 `null`。

## Google Analytics API

Google Analytics 連接器的 BigQuery 資料移轉服務會定期更新，以支援新資料欄，並因應 [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1/changelog?hl=zh-tw) 帶來的異動。Google Analytics 適用的 BigQuery 資料移轉服務連接器，會使用最新支援的 API 版本擷取報表資料。

以下各節將概略說明 Google Analytics Data API 導入的變更。異動項目會依發布日期排序，每個項目都會提供相關資訊，說明您需要進行哪些變更，才能繼續接收 Google Analytics 的資料。

### 2026 年 6 月 1 日

自 2026 年 6 月 1 日起，使用 BigQuery 資料移轉服務回填 Google Analytics 資料時，最多只能回填最近 37 個月的資料。這項異動是為了因應 [2026 年 6 月 1 日起實施的 Google Ads 新版資料保留政策](https://ads-developers.googleblog.com/2026/05/new-data-retention-policy-for-google.html)。

#### 資料遺失風險

**警告：** 下列操作可能會導致資料遺失。

* 2026 年 6 月 1 日後，如果嘗試補充超過 37 個月以前的 Google Analytics 資料，可能會導致資料遺失。
* 如果日期超出 37 個月的保留期限，Google Analytics Data API 可能會傳回部分或空白資料。
* 如果觸發 37 個月前的補登作業，移轉作業會以 API 的不完整結果，覆寫 BigQuery 分區中的現有資料，可能導致完整的歷來資料被空白或部分資料取代。

為避免資料遺失，請確認 Google Analytics 的所有手動或自動回填程序，都不會指定排定日期前 37 個月以上的日期。

在這項異動前，已移轉並儲存在 BigQuery 資料表中的資料不受影響。Google 不會刪除現有資料。

請在 2026 年 6 月 1 日前，檢查 Google Analytics 資料移轉設定和補充資料指令碼，確保符合新的 37 個月保留期限。

### 2025 年 9 月 22 日

**注意：** 這些異動只會影響在 2025 年 4 月 25 日前使用 Google Analytics 連接器的使用者。

[Google Analytics 連接器](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transfer?hl=zh-tw)計畫淘汰表格並更新結構定義，以反映 [Google Analytics Data API v1](https://developers.google.com/analytics/devguides/reporting/data/v1/changelog?hl=zh-tw) 的異動。以下各節將列出這些變更。

Google Analytics 連接器預計於 2025 年 9 月 22 日開始更新。

#### 已淘汰的資料表

下表列出即將淘汰的資料表，以及採用更新結構定義的新資料表。請注意，本次更新後，`p_ga4_conversions` 和 `p_ga4_inAppPurchases` 資料表將停止使用。在 2025 年 9 月 22 日前，系統會同時填入已淘汰和新的資料表，讓您有時間遷移。您可以在移轉設定中使用「Table Filter」(資料表篩選器) 選項，篩除已淘汰的資料表。

| 已淘汰的表格 | 新資料表 |
| --- | --- |
| `p_ga4_audiences` | `p_ga4_Audiences` |
| `p_ga4_conversions` | `Deprecated` |
| `p_ga4_demographicDetails` | `p_ga4_DemographicDetails` |
| `p_ga4_ecommercePurchase` | `p_ga4_EcommercePurchase` |
| `p_ga4_events` | `p_ga4_Events` |
| `p_ga4_inAppPurchases` | `Deprecated` |
| `p_ga4_landingPage` | `p_ga4_LandingPage` |
| `p_ga4_pagesAndScreens` | `p_ga4_PagesAndScreens` |
| `p_ga4_promotions` | `p_ga4_Promotions` |
| `p_ga4_techDetails` | `p_ga4_TechDetails` |
| `p_ga4_trafficAcquisition` | `p_ga4_TrafficAcquisition` |
| `p_ga4_userAcquisition` | `p_ga4_UserAcquisition` |

#### 更新後的資料表結構定義

如要查看新的資料表架構，請前往「[Google Analytics 報表轉換](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transformation?hl=zh-tw)」頁面。

結構定義變更摘要如下：

* **修正結構定義：**修正流量開發、獲取新客和到達網頁報表的結構定義。舉例來說，流量開發和獲客報表結構定義先前曾互換，且到達網頁報表缺少 `landingPage` 維度。
* **欄位重新命名和停用：**為配合目前的 Google Analytics 術語，所有報表中的轉換欄位都已重新命名為 `keyEvents`。因此，「轉換」報表本身也已停用。
* **資料類型變更：**BigQuery 中的收益欄位從 `INTEGER` 變更為 `FLOAT`，以準確呈現 API 傳回的浮點微值。
* **新表格和欄位命名慣例：**為與 Google Analytics API 保持一致，新表格中的欄位名稱會使用 `camelCase` (例如 `eventCount`)，取代先前的 `snake_case` (例如 `event_count`)。

## Google Merchant Center

Google Merchant Center 連接器的 BigQuery 資料移轉服務會定期更新，以支援新資料欄，並因應 Google Merchant Center 報表帶來的變更。

以下各節將按照發布日期列出異動。

### 2026 年 10 月 28 日

2026 年 10 月 28 日，[Google Merchant Center 連接器](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-tw)將更新[產品成效表格](https://docs.cloud.google.com/bigquery/docs/merchant-center-performance-schema?hl=zh-tw)，以配合 Google Merchant Center 成效報表更新：

* **新增「`network`」欄：**「`network`」欄現在會依適用的聯播網 (例如 `SEARCH`、`SEARCH_PARTNERS`、`CONTENT` 和 `YOUTUBE`)，區隔產品成效指標。
* **新的 `destination` 值：**YouTube Shopping 聯盟計畫中精選產品的成效事件，現在會單獨列在 `destination` 值 `AFFILIATE` 下方，而非包含在 `FREE` 中。

現有的資料移轉作業會繼續執行。在這個日期之後移轉的新資料列，將包含新的 `network` 資料欄和 `AFFILIATE` 目的地值。詳情請參閱商家說明中心文章「[Google Merchant Center 成效報表更新](https://support.google.com/merchants/answer/17103877?hl=zh-tw)」。

## Microsoft SQL Server

Microsoft SQL Server 連接器的 BigQuery 資料移轉服務會定期更新，以因應 Microsoft SQL Server 導入的新變更。

以下各節將按照發布日期列出異動。

### 2027 年 3 月 16 日

Microsoft SQL Server 連接器計劃更新資料類型對應，更準確地反映來源資料，並確保資料完整性。下表列出來源資料類型，以及對應的已淘汰資料類型對應和更新版資料類型對應：

| Microsoft SQL Server 資料類型 | 已淘汰的 BigQuery 資料類型對應 | 更新 BigQuery 資料類型對應 |
| --- | --- | --- |
| `datetime` | `TIMESTAMP` | `DATETIME` |
| `datetime2` | `TIMESTAMP` | `DATETIME` |
| `smalldatetime` | `TIMESTAMP` | `DATETIME` |

您可以將 `connector.legacyMapping` 參數設為 `true`，繼續在移轉設定中使用已淘汰的資料類型對應。只要將 `connector.legacyMapping` 參數設為 `false`，即可使用更新版資料類型對應。

2026 年 9 月 16 日起，所有移轉設定都會預設使用更新版資料類型對應。2027 年 3 月 16 日起，系統將停止支援已淘汰的資料類型對應。

## MySQL

MySQL 連接器的 BigQuery 資料移轉服務會定期更新，以因應 MySQL 導入的新變更。

以下各節將按照發布日期列出異動。

### 2027 年 3 月 16 日

MySQL 連接器預計更新資料類型對應，更準確地反映來源資料，並確保資料完整性。下表列出來源資料類型，以及對應的已淘汰資料類型對應和更新版資料類型對應：

| MySQL 資料類型 | 已淘汰的 BigQuery 資料類型對應 | 更新 BigQuery 資料類型對應 |
| --- | --- | --- |
| `DATETIME` | `TIMESTAMP` | `DATETIME` |
| `JSON` | `STRING` | `JSON` |
| `GEOMETRY` | `BYTES` | `GEOGRAPHY` |

您可以將 `connector.legacyMapping` 參數設為 `true`，繼續在移轉設定中使用已淘汰的資料類型對應。只要將 `connector.legacyMapping` 參數設為 `false`，即可使用更新版資料類型對應。

2026 年 9 月 16 日起，所有移轉設定都會預設使用更新版資料類型對應。2027 年 3 月 16 日起，系統將停止支援已淘汰的資料類型對應。

## Google Play 管理中心

Google Play 連接器的 BigQuery 資料移轉服務會定期更新，支援 Google Play 推出的新報表和現有報表異動。

以下各節將按照發布日期列出異動。

### 2025 年 12 月 1 日

Google Play 計劃對[收益報表](https://support.google.com/googleplay/android-developer/answer/6135870?hl=zh-tw#financial&zippy=,earnings)進行下列異動。變更後的結果將會顯示於 BigQuery 資料表 `p_Earnings_suffix`。以下各節將列出這些變更。

#### 重新命名資料欄

下列 Google Play 資料欄將重新命名。

| 已淘汰的資料欄 | 新的資料欄 |
| --- | --- |
| `Base_Plan_ID` | `Base_Plan_or_Purchase_Option_ID` |
| `Product_id` | `Package_ID` |

#### 資料欄值變更

`Product_Type` 欄會從數字表示法變更為人類可讀的字串。

#### 新增資料欄

收益報表將新增「`Sales_Channel`」資料欄。這個欄位會提供銷售來源的相關資訊。

## PostgreSQL

PostgreSQL 連接器的 BigQuery 資料移轉服務會定期更新，以因應 PostgreSQL 導入的新變更。

以下各節將按照發布日期列出異動。

### 2027 年 3 月 16 日

PostgreSQL 連接器預計更新資料類型對應，更準確地反映來源資料，並確保資料完整性。下表列出來源資料類型，以及對應的已淘汰資料類型對應和更新版資料類型對應：

| PostgreSQL 資料類型 | 已淘汰的 BigQuery 資料類型對應 | 更新 BigQuery 資料類型對應 |
| --- | --- | --- |
| `timestamp[(p)][without time zone]` | `TIMESTAMP` | `DATETIME` |
| `json` | `STRING` | `JSON` |
| `jsonb` | `STRING` | `JSON` |

您可以將 `connector.legacyMapping` 參數設為 `true`，繼續在移轉設定中使用已淘汰的資料類型對應。只要將 `connector.legacyMapping` 參數設為 `false`，即可使用更新版資料類型對應。

2026 年 9 月 16 日起，所有移轉設定都會預設使用更新版資料類型對應。2027 年 3 月 16 日起，系統將停止支援已淘汰的資料類型對應。

## Salesforce Bulk API

Salesforce 連接器的 BigQuery 資料移轉服務會定期更新，以支援 Salesforce Bulk API 導入的變更。

以下各節將說明 Salesforce 連接器更新至新版 Bulk API 時的異動。異動項目會依發布日期排序，每個項目都會提供相關資訊，說明您需要進行哪些變更，才能繼續接收 Salesforce 的資料。

### October 14, 2025

Salesforce 連接器正式發布後，現在會使用 Salesforce Bulk API V1 64.0 版。Salesforce Bulk API V1 53.0 版支援的幾個欄位已不再支援。

#### 已淘汰的欄位

下表列出 Salesforce 連接器正式發布版淘汰的欄位，以及與各欄位相關聯的 `sObject` 名稱。

| 已淘汰的欄位 | `sObject`名稱 |
| --- | --- |
| `EffectiveDate` | `MobSecurityCertPinConfig` |
| `PermissionsAllowObjectDetectionTraining` | `Profile` |
| `PermissionsAllowObjectDetection` | `Profile` |
| `PermissionsAllowObjectDetectionTraining` | `PermissionSet` |
| `PermissionsAllowObjectDetection` | `PermissionSet` |
| `MaximumPermissionsAllowObjectDetectionTraining` | `PermissionSetLicense` |
| `MaximumPermissionsAllowObjectDetection` | `PermissionSetLicense` |
| `PermissionsAllowObjectDetectionTraining` | `UserPermissionAccess` |
| `PermissionsAllowObjectDetection` | `UserPermissionAccess` |
| `PermissionsAllowObjectDetectionTraining` | `MutingPermissionSet` |
| `PermissionsAllowObjectDetection` | `MutingPermissionSet` |
| `OptionsHstsHeaders` | `Domain` |
| `UserPreferencesHideInvoicesRedirectConfirmation` | `User` |
| `UserPreferencesHideStatementsRedirectConfirmation` | `User` |
| `UserPreferencesHideInvoicesRedirectConfirmation` | `UserChangeEvent` |
| `UserPreferencesHideStatementsRedirectConfirmation` | `UserChangeEvent` |

## Search Ads 360

Search Ads 360 連接器的 BigQuery 資料移轉服務會定期更新，以支援新資料欄，並因應 [Search Ads 360 API](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/overview?hl=zh-tw) 帶來的異動。Search Ads 360 連接器專用的 BigQuery 資料移轉服務會使用最新支援的 API 版本擷取報表資料。

以下各節將概略說明 Search Ads 360 Data API 帶來的異動。異動項目會依發布日期排序，每個項目都會提供相關資訊，說明您需要進行哪些變更，才能繼續接收 Search Ads 360 的資料。

### 2026 年 6 月 1 日

自 2026 年 6 月 1 日起，Search Ads 360 連接器將限制每日資料補充作業，僅限最近 37 個月。如果嘗試回填 37 個月前的資料，系統會傳回錯誤。這項異動是為了因應 [2026 年 6 月 1 日起實施的 Google Ads 新版資料保留政策](https://ads-developers.googleblog.com/2026/05/new-data-retention-policy-for-google.html)。

已移轉並儲存在 BigQuery 資料表中的資料則不受影響。

## ServiceNow

ServiceNow 連接器專用的 BigQuery 資料移轉服務會定期更新，以因應 ServiceNow 導入的新變更。

以下各節將按照發布日期列出異動。

### 2027 年 3 月 16 日

ServiceNow 連接器計劃更新資料類型對應，更準確地反映來源資料，並確保資料完整性。下表列出來源資料類型，以及對應的已淘汰資料類型對應和更新版資料類型對應：

| ServiceNow 資料類型 | 已淘汰的 BigQuery 資料類型對應 | 更新 BigQuery 資料類型對應 |
| --- | --- | --- |
| `glide_list` | `STRING` | `ARRAY` |
| `list` | `STRING` | `ARRAY` |

您可以將 `connector.legacyMapping` 參數設為 `true`，繼續在移轉設定中使用已淘汰的資料類型對應。只要將 `connector.legacyMapping` 參數設為 `false`，即可使用更新版資料類型對應。

2026 年 9 月 16 日起，所有移轉設定都會預設使用更新版資料類型對應。2027 年 3 月 16 日起，系統將停止支援已淘汰的資料類型對應。

## YouTube Reporting API

YouTube 內容擁有者和 YouTube 頻道連接器的 BigQuery 資料移轉服務會定期更新，以支援 [YouTube Reporting API](https://developers.google.com/youtube/reporting?hl=zh-tw) 導入的新報表，並淘汰舊報表。

以下各節將說明 YouTube Reporting API 推出新報表時的異動。變更項目會依發布日期排序，每個項目都會提供相關資訊，說明您需要進行哪些變更，才能繼續接收 YouTube 資料。

### 2025 年 9 月 22 日

[YouTube 內容擁有者連接器](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw)和 [YouTube 頻道連接器](https://docs.cloud.google.com/bigquery/docs/youtube-channel-transfer?hl=zh-tw)計畫推出新報表並淘汰舊報表，以反映 YouTube [Shorts 觀看次數變更](https://support.google.com/youtube/thread/333869549/a-change-to-how-we-count-views-on-shorts?hl=zh-tw)。以下各節將列出這些變更。

新報表預計於 2025 年 7 月 7 日開始提供。您無須採取任何行動，即可取得新報表。舊版報表預計於 2025 年 9 月 22 日起停用。

#### YouTube 內容擁有者連接器 - 已淘汰的表格

針對 YouTube 內容擁有者連接器，下表列出即將淘汰的 BigQuery 資料表，以及結構定義更新後的新資料表。在 2025 年 9 月 22 日前，系統會同時填入已淘汰和新的資料表，讓您有時間遷移。2025 年 9 月 22 日後，系統只會填入新資料表。suffix 的值是您在建立移轉作業時設定的資料表後置字串。

| 已淘汰的表格 | 新資料表 |
| --- | --- |
| `p_content_owner_asset_basic_a2_suffix` | `p_content_owner_asset_basic_a3_suffix` |
| `p_content_owner_asset_combined_a2_suffix` | `p_content_owner_asset_combined_a3_suffix` |
| `p_content_owner_asset_device_os_a2_suffix` | `p_content_owner_asset_device_os_a3_suffix` |
| `p_content_owner_asset_playback_location_a2_suffix` | `p_content_owner_asset_playback_location_a3_suffix` |
| `p_content_owner_asset_province_a2_suffix` | `p_content_owner_asset_province_a3_suffix` |
| `p_content_owner_asset_traffic_source_a2_suffix` | `p_content_owner_asset_traffic_source_a3_suffix` |
| `p_content_owner_basic_a3_suffix` | `p_content_owner_basic_a4_suffix` |
| `p_content_owner_combined_a2_suffix` | `p_content_owner_combined_a3_suffix` |
| `p_content_owner_device_os_a2_suffix` | `p_content_owner_device_os_a3_suffix` |
| `p_content_owner_playback_location_a2_suffix` | `p_content_owner_playback_location_a3_suffix` |
| `p_content_owner_playlist_basic_a1_suffix` | `p_content_owner_playlist_basic_a2_suffix` |
| `p_content_owner_playlist_combined_a1_suffix` | `p_content_owner_playlist_combined_a2_suffix` |
| `p_content_owner_playlist_device_os_a1_suffix` | `p_content_owner_playlist_device_os_a2_suffix` |
| `p_content_owner_playlist_playback_location_a1_suffix` | `p_content_owner_playlist_playback_location_a2_suffix` |
| `p_content_owner_playlist_province_a1_suffix` | `p_content_owner_playlist_province_a2_suffix` |
| `p_content_owner_playlist_traffic_source_a1_suffix` | `p_content_owner_playlist_traffic_source_a2_suffix` |
| `p_content_owner_province_a2_suffix` | `p_content_owner_province_a3_suffix` |
| `p_content_owner_subtitles_a2_suffix` | `p_content_owner_subtitles_a3_suffix` |
| `p_content_owner_traffic_source_a2_suffix` | `p_content_owner_traffic_source_a3_suffix` |
| `p_content_owner_shorts_ad_revenue_summary_a1_suffix` | `p_content_owner_shorts_ad_revenue_summary_a2_suffix` |
| `p_content_owner_shorts_country_ad_revenue_summary_a1_suffix` | `p_content_owner_shorts_country_ad_revenue_summary_a2_suffix` |
| `p_content_owner_shorts_day_ad_revenue_summary_a1_suffix` | `p_content_owner_shorts_day_ad_revenue_summary_a2_suffix` |
| `p_content_owner_shorts_global_ad_revenue_summary_a1_suffix` | `p_content_owner_shorts_global_ad_revenue_summary_a2_suffix` |

#### YouTube 頻道連接器 - 已淘汰的表格

YouTube 頻道連接器方面，下表列出即將淘汰的 BigQuery 資料表，以及採用更新後結構定義的新資料表。在 2025 年 9 月 22 日前，系統會同時填入已淘汰和新的資料表，讓您有時間遷移。2025 年 9 月 22 日後，系統只會填入新資料表。suffix 的值是您在建立移轉作業時設定的資料表後置字串。

| 已淘汰的表格 | 新資料表 |
| --- | --- |
| `p_channel_basic_a2_suffix` | `p_channel_basic_a3_suffix` |
| `p_channel_combined_a2_suffix` | `p_channel_combined_a3_suffix` |
| `p_channel_device_os_a2_suffix` | `p_channel_device_os_a3_suffix` |
| `p_channel_playback_location_a2_suffix` | `p_channel_playback_location_a3_suffix` |
| `p_channel_province_a2_suffix` | `p_channel_province_a3_suffix` |
| `p_channel_subtitles_a2_suffix` | `p_channel_subtitles_a3_suffix` |
| `p_channel_traffic_source_a2_suffix` | `p_channel_traffic_source_a3_suffix` |
| `p_playlist_basic_a1_suffix` | `p_playlist_basic_a2_suffix` |
| `p_playlist_combined_a1_suffix` | `p_playlist_combined_a2_suffix` |
| `p_playlist_device_os_a1_suffix` | `p_playlist_device_os_a2_suffix` |
| `p_playlist_playback_location_a1_suffix` | `p_playlist_playback_location_a2_suffix` |
| `p_playlist_province_a1_suffix` | `p_playlist_province_a2_suffix` |
| `p_playlist_traffic_source_a1_suffix` | `p_playlist_traffic_source_a2_suffix` |

#### 更新後的資料表結構定義

新資料表會有名為 `engaged_views` 的新資料欄。如要進一步瞭解這項指標，請參閱「[Shorts 觀看次數計算方式異動](https://support.google.com/youtubekb/answer/10950071?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-19 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-19 (世界標準時間)。"],[],[]]