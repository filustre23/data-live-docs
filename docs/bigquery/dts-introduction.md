Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料移轉服務簡介

BigQuery 資料移轉服務可讓您自動執行排定的代管資料移轉作業，將資料移轉至 [BigQuery](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)。設定資料移轉作業後，BigQuery 資料移轉服務會定期自動將資料載入 BigQuery。您也可以主動執行資料補充作業，以填補任何中斷或缺漏、[複製資料集](https://docs.cloud.google.com/bigquery/docs/copying-datasets?hl=zh-tw)，以及執行[排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)。您無法使用 BigQuery 資料移轉服務將資料從 BigQuery 移轉出去。

如要設定及管理移轉作業，可以使用 [Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)、[bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw)或 [BigQuery 資料移轉服務 API](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest?hl=zh-tw)。「Pipelines & Connections」(管道與連線) 頁面也提供[簡化的工作流程](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw) ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))，可用於建立移轉作業。如要接收服務更新，請訂閱 [BigQuery DTS 公告群組](https://groups.google.com/g/bigquery-dts-announcements?hl=zh-tw)。

## 支援的資料來源

BigQuery 資料移轉服務支援從下列資料來源載入資料：

| 類別 | 資料來源 |
| --- | --- |
| 雲端儲存空間 | [Amazon Simple Storage Service (Amazon S3)](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw) |
| 雲端儲存空間 | [Azure Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw) |
| 雲端儲存空間 | [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw) |
| 資料庫和資料倉儲 | [Amazon Redshift](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw) |
| 資料庫和資料倉儲 | [Apache Hive metastore](https://docs.cloud.google.com/bigquery/docs/hdfs-data-lake-transfer?hl=zh-tw) |
| 資料庫和資料倉儲 | [Microsoft SQL Server](https://docs.cloud.google.com/bigquery/docs/sqlserver-transfer-intro?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| 資料庫和資料倉儲 | [MySQL](https://docs.cloud.google.com/bigquery/docs/mysql-transfer-intro?hl=zh-tw) |
| 資料庫和資料倉儲 | [Oracle](https://docs.cloud.google.com/bigquery/docs/oracle-transfer-intro?hl=zh-tw) |
| 資料庫和資料倉儲 | [PostgreSQL](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer-intro?hl=zh-tw) |
| 資料庫和資料倉儲 | [Snowflake](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer?hl=zh-tw) |
| 資料庫和資料倉儲 | [Teradata](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw) |
| Google 服務 | [Campaign Manager](https://docs.cloud.google.com/bigquery/docs/doubleclick-campaign-transfer?hl=zh-tw) |
| Google 服務 | [購物比較服務 (CSS) 中心](https://docs.cloud.google.com/bigquery/docs/css-center-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| Google 服務 | [Display & Video 360](https://docs.cloud.google.com/bigquery/docs/display-video-transfer?hl=zh-tw) |
| Google 服務 | [Google Ad Manager](https://docs.cloud.google.com/bigquery/docs/doubleclick-publisher-transfer?hl=zh-tw) |
| Google 服務 | [Google Ads](https://docs.cloud.google.com/bigquery/docs/google-ads-transfer?hl=zh-tw) |
| Google 服務 | [Google Analytics 4](https://docs.cloud.google.com/bigquery/docs/google-analytics-4-transfer?hl=zh-tw) |
| Google 服務 | [Google Merchant Center](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| Google 服務 | [Google Play](https://docs.cloud.google.com/bigquery/docs/play-transfer?hl=zh-tw) |
| Google 服務 | [Search Ads 360](https://docs.cloud.google.com/bigquery/docs/search-ads-transfer?hl=zh-tw) |
| Google 服務 | [YouTube 頻道](https://docs.cloud.google.com/bigquery/docs/youtube-channel-transfer?hl=zh-tw) |
| Google 服務 | [YouTube 內容擁有者](https://docs.cloud.google.com/bigquery/docs/youtube-content-owner-transfer?hl=zh-tw) |
| 行銷平台 | [Facebook 廣告](https://docs.cloud.google.com/bigquery/docs/facebook-ads-transfer-intro?hl=zh-tw) |
| 行銷平台 | [HubSpot](https://docs.cloud.google.com/bigquery/docs/hubspot-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| 行銷平台 | [Klaviyo](https://docs.cloud.google.com/bigquery/docs/klaviyo-transfer-intro?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| 行銷平台 | [Mailchimp](https://docs.cloud.google.com/bigquery/docs/mailchimp-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| 付款平台 | [PayPal](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| 付款平台 | [Shopify](https://docs.cloud.google.com/bigquery/docs/shopify-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| 付款平台 | [Stripe](https://docs.cloud.google.com/bigquery/docs/stripe-transfer?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| SaaS 平台 | [Salesforce](https://docs.cloud.google.com/bigquery/docs/salesforce-transfer-intro?hl=zh-tw) |
| SaaS 平台 | [Salesforce Marketing Cloud](https://docs.cloud.google.com/bigquery/docs/sfmc-transfer?hl=zh-tw) |
| SaaS 平台 | [ServiceNow](https://docs.cloud.google.com/bigquery/docs/servicenow-transfer?hl=zh-tw) |

### 資料傳送服務等級目標注意事項

[資料傳送服務等級目標](https://cloud.google.com/bigquery/sla?e=48754805&hl=zh-tw)適用於使用 BigQuery 資料移轉服務，從 Google Cloud內來源自動排定的資料移轉作業。

如果資料移轉作業涉及第三方或非Google Cloud 來源，這些來源的服務中斷可能會影響 BigQuery 資料移轉服務的效能。因此，資料傳送服務等級目標不適用於從非Google Cloud 來源移轉 BigQuery 資料移轉服務資料。

## 支援的地區

與 BigQuery 相同，BigQuery 資料移轉服務也是[多區域資源](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw#regional_resources)，並提供許多額外的單一區域。

[建立目的地資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存 BigQuery 資料移轉服務移轉的資料時，您要指定 BigQuery 資料集的地區。設定移轉作業時，移轉設定本身會設為與目的地資料集相同的位置。BigQuery 資料移轉服務會在與目的地資料集相同的位置處理及暫存資料。

BigQuery 資料移轉服務支援從任何資料儲存區域，將資料移轉至目的地資料集所在的任何位置。

如要進一步瞭解 BigQuery 資料移轉服務的移轉作業和區域相容性，請參閱「[資料集位置和移轉作業](https://docs.cloud.google.com/bigquery/docs/dts-locations?hl=zh-tw)」。如要瞭解 BigQuery 支援的區域，請參閱「[資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)」。

## 使用預留運算單元移轉資料

只有在專案、資料夾或組織指派給具有下列任一[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)的預留項目時，BigQuery 資料移轉服務觸發的工作才會使用預留項目運算單元：

* 使用 `QUERY` 查詢工作
* 使用 `PIPELINE` 載入工作

[複製資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#copy-datasets)的工作不會使用預留運算單元。

## 定價

如要瞭解 BigQuery 資料移轉服務的定價，請參閱「[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」頁面。

資料移轉至 BigQuery 後，適用標準 BigQuery [儲存空間](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)和[查詢](https://cloud.google.com/bigquery/pricing?hl=zh-tw#queries)定價。

## 配額

如要瞭解 BigQuery 資料移轉服務配額，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」頁面。

## 排解移轉設定問題

如要瞭解如何解決 BigQuery 資料移轉服務的問題，請參閱「[排解移轉設定問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw)」。

## 後續步驟

* 如要瞭解如何建立移轉作業，請參閱[資料來源](#supported_data_sources)的說明文件。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-30 (世界標準時間)。"],[],[]]