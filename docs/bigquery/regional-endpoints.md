Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 區域端點

本頁面說明如何使用 [Private Service Connect 區域端點](https://docs.cloud.google.com/vpc/docs/about-accessing-regional-google-apis-endpoints?hl=zh-tw)存取 BigQuery 中的資源。您可以使用地區端點執行工作負載，確保符合[資料駐留](https://docs.cloud.google.com/assured-workloads/docs/data-residency?hl=zh-tw)和資料主權規定，要求流量會直接傳送至端點中指定的區域。

## 總覽

區域端點是要求端點，可協助限制要求，只有在受影響的資源位於端點指定的位置時，要求才會繼續進行。舉例來說，如果您在刪除資料集要求中使用 `https://bigquery.us-central1.rep.googleapis.com` 端點，則只有在資料集位於 `US-CENTRAL1` 時，要求才會繼續執行。

與全域端點不同，區域端點可將要求限制在資源所在的端點指定位置，全域端點則可將要求轉送至資源所在位置以外的其他位置。區域端點會終止 TLS 工作階段，位置由端點指定，適用於從網際網路、其他Google Cloud 資源 (例如 Compute Engine 虛擬機器)、使用 VPN 或 Interconnect 的地端服務，以及虛擬私有雲 (VPC) 收到的要求。

區域端點可確保資料落地，將靜態和傳輸中的表格資料保留在端點指定的區域。這不包括資源中繼資料，例如資料集名稱和 IAM 政策。詳情請參閱「[服務資料注意事項](https://docs.cloud.google.com/assured-workloads/docs/data-residency?hl=zh-tw#service-data)」。

BigQuery 包含多個 API。下列 API 可搭配區域端點使用：

| API | 網址 | 參考資料 |
| --- | --- | --- |
| BigQuery API | `bigquery.LOCATION.rep.googleapis.com` | [REST](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw) |
| BigQuery Storage API | `bigquerystorage.LOCATION.rep.googleapis.com` | [RPC](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc?hl=zh-tw) |
| BigQuery Reservations API | `bigqueryreservation.LOCATION.rep.googleapis.com` | [RPC](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rpc?hl=zh-tw) 和 [REST](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rest?hl=zh-tw) |
| BigQuery Migration API | `bigquerymigration.LOCATION.rep.googleapis.com` | [REST](https://docs.cloud.google.com/bigquery/docs/reference/migration/rest?hl=zh-tw) |
| BigQuery 資料移轉服務 API | `bigquerydatatransfer.LOCATION.rep.googleapis.com` | [RPC](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rpc?hl=zh-tw) 和 [REST](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest?hl=zh-tw) |

## 支援的地區

您可以使用區域端點，將資料保留在下列位置：

* 亞太地區

  + 德里 `asia-south2`
  + 孟買 `asia-south1`
* 歐洲

  + 比利時 `europe-west1`
  + 法蘭克福 `europe-west3`
  + 倫敦 `europe-west2`
  + 米蘭 `europe-west8`
  + 荷蘭 `europe-west4`
  + 巴黎 `europe-west9`
  + 蘇黎世 `europe-west6`
* 中東

  + 達曼 `me-central2`
* 美洲

  + 俄亥俄州哥倫布 `us-east5`
  + 達拉斯 `us-south1`
  + 愛荷華州 `us-central1`
  + 拉斯維加斯 `us-west4`
  + 洛杉磯 `us-west2`
  + 蒙特婁 `northamerica-northeast1`
  + 北維吉尼亞州 `us-east4`
  + 奧勒岡州 `us-west1`
  + 鹽湖城 `us-west3`
  + 南卡羅來納州 `us-east1`
  + 多倫多 `northamerica-northeast2`

## 支援的作業

您只能使用區域端點，對儲存在端點指定位置的資源執行存取或變動作業。區域端點無法用於執行作業，存取或變更端點指定位置以外的資源。

舉例來說，使用區域端點 `https://bigquery.us-central1.rep.googleapis.com` 時，您可以讀取位於 `US-CENTRAL1` 的資料集中的資料表，但只有在來源和目的地資料集都位於 `US-CENTRAL1` 時，才能將資料表從來源資料集複製到目的地資料集。如果您嘗試從 `US-CENTRAL1` 外部讀取或複製表格，系統會顯示錯誤訊息。

## 限制和規定

區域端點無法用於執行下列作業：

* 存取或變動端點指定位置以外資源的作業
* 將資源從一個位置複製、複製或重寫到另一個位置。

使用區域端點時，請注意下列限制：

* 區域端點不支援[相互傳輸層安全標準 (mTLS)](https://docs.cloud.google.com/chrome-enterprise-premium/docs/understand-mtls?hl=zh-tw)。
* 使用地區端點不會限制在端點區域外建立資源。如要限制資源建立作業，請使用[機構政策服務資源位置限制](https://docs.cloud.google.com/resource-manager/docs/organization-policy/defining-locations?hl=zh-tw)。
* [跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)和[跨區域資料表複製](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy_tables_across_regions)不受端點保護限制。
* 執行[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)

## 使用地區端點的工具

### 控制台

如要存取 BigQuery 資源，並遵守資料落地或主權規定，請使用管轄區Google Cloud 控制台網址：

| 資源 | 網址 |
| --- | --- |
| 專案的資料集清單 | `https://console.JURISDICTION.cloud.google.com/bigquery?project=PROJECT_ID` |
| 資料集的資料表清單 | `https://console.JURISDICTION.cloud.google.com/bigquery/projects/PROJECT_ID/datasets/DATASET_NAME/tables` |
| 資料表詳細資料 | `https://console.JURISDICTION.cloud.google.com/bigquery/projects/PROJECT_ID/datasets/DATASET_NAME/tables/TABLE_NAME` |

將 `JURISDICTION` 替換為下列其中一個值：

* `eu` (如果資源位於歐盟境內)
* `sa` 如果資源位於沙烏地阿拉伯王國
* `us` (如果資源位於美國)

**注意：** 您無法使用管轄區 Google Cloud 控制台，上傳 `eu`、`sa` 或 `us` 中的檔案。

### 指令列

如要設定 Google Cloud CLI 以搭配使用區域端點，請完成下列步驟：

1. 請確認您使用的是 Google Cloud CLI 402.0.0 以上版本。
2. 將 `api_endpoint_overrides/bigquery` 屬性設為要使用的區域端點：

   ```
   gcloud config set api_endpoint_overrides/bigquery https://bigquery.LOCATION.rep.googleapis.com/bigquery/v2/
   ```

   或者，您也可以將 `CLOUDSDK_API_ENDPOINT_OVERRIDES_BIGQUERY` 環境變數設為端點：

   ```
   CLOUDSDK_API_ENDPOINT_OVERRIDES_BIGQUERY=https://bigquery.LOCATION.rep.googleapis.com/bigquery/v2/ gcloud  alpha bq  datasets list
   ```

### REST API

如果是 REST API，請將要求傳送至區域端點，格式如下：`https://bigquery.LOCATION.rep.googleapis.com`，而非傳送至[服務端點](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw#service-endpoint)。

## 限制全域 API 端點用量

如要強制使用區域端點，請使用 `constraints/gcp.restrictEndpointUsage` 組織政策限制，封鎖對全域 API 端點的要求。詳情請參閱「[限制端點用量](https://docs.cloud.google.com/docs/security/compliance/restrict-endpoint-usage?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]