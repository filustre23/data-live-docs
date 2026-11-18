Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [資源](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 位置

本頁面說明「位置」的概念，以及可儲存及處理資料的不同區域。儲存和分析的定價也取決於資料位置和預留項目。如要進一步瞭解位置定價，請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」。如要瞭解如何設定資料集的位置，請參閱「[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)」。如要瞭解預留項目位置，請參閱「[管理不同區域的預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#manage_reservations_in_different_regions)」。

如要進一步瞭解 BigQuery 資料移轉服務如何使用位置，請參閱「[資料位置和移轉](https://docs.cloud.google.com/bigquery/docs/dts-locations?hl=zh-tw)」。

## 位置和區域

BigQuery 提供兩種資料和運算位置：

* 「地區」是特定的地理位置，例如倫敦。
* 「多區域」是指包含許多不重複且不連續區域的大型地理區域，例如美國或歐洲。多區域位置提供的配額比單一區域多，但多區域不提供區域備援。資料會儲存在單一區域，且運算作業僅在該區域內進行。BigQuery 提供[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)功能，可跨區域備援。

無論是哪種位置類型，BigQuery 都會自動將資料副本儲存在所選位置中，單一區域內的兩個不同可用區。多區域與其他區域視為不同，即使位於同一可用區也是如此。如要進一步瞭解資料可用性和耐用性，請參閱「[災難規劃](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw#disaster_planning)」。

## 支援的地區

BigQuery 資料集可以儲存在下列區域和多區域。如要進一步瞭解區域和可用區，請參閱「[地理位置與區域](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw)」一文。

### 區域

下表列出提供 BigQuery 的美洲區域。

| **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 俄亥俄州哥倫布 | `us-east5` |  |
| 達拉斯 | `us-south1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 洛杉磯 | `us-west2` |  |
| 拉斯維加斯 | `us-west4` |  |
| 墨西哥 | `northamerica-south1` |  |
| 蒙特婁 | `northamerica-northeast1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 北維吉尼亞州 | `us-east4` |  |
| 奧克拉荷馬州 | `us-central2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 奧勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 鹽湖城 | `us-west3` |  |
| 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 聖地亞哥 | `southamerica-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 南卡羅來納州 | `us-east1` |  |
| 多倫多 | `northamerica-northeast2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |

下表列出提供 BigQuery 的亞太地區。

| **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 曼谷 | `asia-southeast3` |  |
| 德里 | `asia-south2` |  |
| 香港 | `asia-east2` |  |
| 雅加達 | `asia-southeast2` |  |
| 墨爾本 | `australia-southeast2` |  |
| 孟買 | `asia-south1` |  |
| 大阪 | `asia-northeast2` |  |
| 首爾 | `asia-northeast3` |  |
| 新加坡 | `asia-southeast1` |  |
| 雪梨 | `australia-southeast1` |  |
| 台灣 | `asia-east1` |  |
| 東京 | `asia-northeast1` |  |

下表列出提供 BigQuery 的歐洲區域。

| **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 比利時 | `europe-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 柏林 | `europe-west10` |  |
| 芬蘭 | `europe-north1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 法蘭克福 | `europe-west3` |  |
| 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 米蘭 | `europe-west8` |  |
| 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 巴黎 | `europe-west9` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 斯德哥爾摩 | `europe-north2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 杜林 | `europe-west12` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 華沙 | `europe-central2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |

下表列出提供 BigQuery 的中東區域。

| **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 達曼 | `me-central2` |  |
| 杜哈 | `me-central1` |  |
| 特拉維夫 | `me-west1` |  |

下表列出提供 BigQuery 的非洲區域。

| **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 約翰尼斯堡 | `africa-south1` |  |

### 多區域

**注意：**BigQuery 將在今年稍晚停止使用「多區域」一詞。`US` 和 `EU` 區域名稱會列在單一區域清單中，並分別與 `us-central1` 和 `europe-west4` 區域共置。現有的資料落地設定不會變更。
下表列出提供 BigQuery 的多區域。選取多區域時，BigQuery 會在多區域中選取單一區域，用於儲存及處理資料。

| **多區域說明** | **多區域名稱** |
| --- | --- |
| 歐盟[成員國](https://europa.eu/european-union/about-eu/countries_en)境內的資料中心1 | `EU` |
| 美國資料中心2 | `US` |

**注意：**選取多區域位置不會提供跨區域複製或區域備援功能，因此如果發生區域服務中斷，資料集可用性不會增加。資料會儲存在地理位置內的單一區域。

1 位於 `EU` 多區域的資料只會儲存在下列其中一個位置：`europe-west1` (比利時) 或 `europe-west4` (荷蘭)。BigQuery 會自動決定資料的確切儲存和處理位置。

2 位於 `US` 多區域的資料只會儲存在下列其中一個位置：`us-central1` (愛荷華州)、`us-west1` (奧勒岡州) 或 `us-central2` (奧克拉荷馬州)。BigQuery 會自動決定資料的儲存和處理位置。

## BigQuery Studio 程式碼資產位置

BigQuery Studio 可讓您儲存、共用及管理程式碼資產的版本，例如[筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)和[已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw)。

下表列出 BigQuery Studio 支援的區域：

|  | 地區說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- | --- |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` |  |
| **美洲** | | | |
|  | 哥倫布 | `us-east5` |  |
|  | 達拉斯 | `us-south1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 洛杉磯 | `us-west2` |  |
|  | 拉斯維加斯 | `us-west4` |  |
|  | 蒙特婁 | `northamerica-northeast1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 北維吉尼亞州 | `us-east4` |  |
|  | 奧勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 南卡羅來納州 | `us-east1` |  |
| **亞太地區** | | | |
|  | 香港 | `asia-east2` |  |
|  | 雅加達 | `asia-southeast2` |  |
|  | 孟買 | `asia-south1` |  |
|  | 首爾 | `asia-northeast3` |  |
|  | 新加坡 | `asia-southeast1` |  |
|  | 雪梨 | `australia-southeast1` |  |
|  | 台灣 | `asia-east1` |  |
|  | 東京 | `asia-northeast1` |  |
| **歐洲** | | | |
|  | 比利時 | `europe-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 芬蘭 | `europe-north1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 米蘭 | `europe-west8` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 杜林 | `europe-west12` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 華沙 | `europe-central2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **中東地區** | | | |
|  | 達曼 | `me-central2` |  |
|  | 杜哈 | `me-central1` |  |
|  | 特拉維夫 | `me-west1` |  |

## BigQuery Omni 位置

BigQuery Omni 處理查詢的位置，與包含查詢資料表的資料集相同。資料集建立後即無法變更位置。您的資料會保留在 AWS 或 Azure 帳戶中。BigQuery Omni 區域支援 Enterprise 版預留項目和隨選運算 (分析) 定價。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

|  | 地區說明 | 區域名稱 | 共置 BigQuery 區域 |
| --- | --- | --- | --- |
| **AWS** | | | |
|  | AWS - 美國東部 (北維吉尼亞州) | `aws-us-east-1` | `us-east4` |
|  | AWS - 美國西部 (奧勒岡州) | `aws-us-west-2` | `us-west1` |
|  | AWS - 亞太地區 (首爾) | `aws-ap-northeast-2` | `asia-northeast3` |
|  | AWS - 亞太地區 (雪梨) | `aws-ap-southeast-2` | `australia-southeast1` |
|  | AWS - 歐洲 (愛爾蘭) | `aws-eu-west-1` | `europe-west1` |
|  | AWS - 歐洲 (法蘭克福) | `aws-eu-central-1` | `europe-west3` |
| **Azure** | | | |
|  | Azure - 美國東部 2 | `azure-eastus2` | `us-east4` |

## BigQuery ML 位置

以下各節說明 BigQuery ML 模型支援的位置。

### 遠端模型的位置

本節說明[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)支援的位置，以及遠端模型處理作業的位置。  

#### 地區位置

如要瞭解 Google 模型和合作夥伴模型支援的遠端模型位置，請參閱下列說明文件：

* 如要瞭解 Gemini 模型和嵌入模型支援的地區，請參閱「[Google 模型端點位置](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#google_model_endpoint_locations)」。
* 如要瞭解 Claude、Llama 和 Mistral AI 模型支援的地區，請參閱「[Google Cloud 合作夥伴模型端點位置](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#genai-partner-models)」。

下表列出 Cloud AI 服務遠端模型和部署至 Agent Platform 的自訂模型支援哪些區域。資料欄名稱代表遠端模型的類型。

|  | 地區說明 | 區域名稱 | Vertex AI 部署的模型 | Cloud Natural Language API | Cloud Translation API | Cloud Vision API | Document AI API | Speech-to-Text API |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **美洲** | | | | | | | | |
|  | 俄亥俄州哥倫布 | `us-east5` |  |  |  |  |  |  |
|  | 達拉斯 | `us-south1` | ● |  |  |  |  |  |
|  | 愛荷華州 | `us-central1` | ● |  |  |  |  | ● |
|  | 拉斯維加斯 | `us-west4` | ● |  |  |  |  |  |
|  | 洛杉磯 | `us-west2` | ● |  |  |  |  |  |
|  | 墨西哥 | `northamerica-south1` |  |  |  |  |  |  |
|  | 蒙特婁 | `northamerica-northeast1` | ● |  |  |  |  |  |
|  | 北維吉尼亞州 | `us-east4` | ● |  |  |  |  |  |
|  | 奧勒岡州 | `us-west1` | ● |  |  |  |  | ● |
|  | 鹽湖城 | `us-west3` | ● |  |  |  |  |  |
|  | 聖保羅 | `southamerica-east1` | ● |  |  |  |  |  |
|  | 聖地亞哥 | `southamerica-west1` |  |  |  |  |  |  |
|  | 南卡羅來納州 | `us-east1` | ● |  |  |  |  | ● |
|  | 多倫多 | `northamerica-northeast2` | ● |  |  |  |  |  |
| **歐洲** | | | | | | | | |
|  | 比利時 | `europe-west1` | ● |  |  |  |  | ● |
|  | 芬蘭 | `europe-north1` |  |  |  |  |  |  |
|  | 法蘭克福 | `europe-west3` | ● |  |  |  |  | ● |
|  | 倫敦 | `europe-west2` | ● |  |  |  |  | ● |
|  | 馬德里 | `europe-southwest1` |  |  |  |  |  |  |
|  | 米蘭 | `europe-west8` | ● |  |  |  |  |  |
|  | 荷蘭 | `europe-west4` | ● |  |  |  |  | ● |
|  | 巴黎 | `europe-west9` | ● |  |  |  |  |  |
|  | 斯德哥爾摩 | `europe-north2` |  |  |  |  |  |  |
|  | 杜林 | `europe-west12` |  |  |  |  |  |  |
|  | 華沙 | `europe-central2` | ● |  |  |  |  |  |
|  | 蘇黎世 | `europe-west6` | ● |  |  |  |  |  |
| **亞太地區** | | | | | | | | |
|  | 曼谷 | `asia-southeast3` |  |  |  |  |  |  |
|  | 德里 | `asia-south2` |  |  |  |  |  |  |
|  | 香港 | `asia-east2` | ● |  |  |  |  |  |
|  | 雅加達 | `asia-southeast2` | ● |  |  |  |  |  |
|  | 墨爾本 | `australia-southeast2` |  |  |  |  |  |  |
|  | 孟買 | `asia-south1` | ● |  |  |  |  | ● |
|  | 大阪 | `asia-northeast2` |  |  |  |  |  |  |
|  | 首爾 | `asia-northeast3` | ● |  |  |  |  |  |
|  | 新加坡 | `asia-southeast1` | ● |  |  |  |  | ● |
|  | 雪梨 | `australia-southeast1` | ● |  |  |  |  | ● |
|  | 台灣 | `asia-east1` | ● |  |  |  |  |  |
|  | 東京 | `asia-northeast1` | ● |  |  |  |  | ● |
| **中東地區** | | | | | | | | |
|  | 達曼 | `me-central2` |  |  |  |  |  |  |
|  | 杜哈 | `me-central1` |  |  |  |  |  |  |
|  | 特拉維夫 | `me-west1` | ● |  |  |  |  |  |

如果建立遠端模型的資料集位於單一區域，Agent Platform 模型端點必須位於相同區域。如果指定模型端點網址，請使用與資料集位於相同區域的端點。舉例來說，如果資料集位於 `us-central1` 區域，請指定端點 `https://us-central1-aiplatform.googleapis.com/v1/projects/myproject/locations/us-central1/publishers/google/models/<target_model>`。如果指定模型名稱，BigQuery ML 會自動選擇正確區域中的端點。

#### 多地區位置

遠端模型的多區域支援如下：

* Gemini 模型支援 `US` 和 `EU` 多區域。
* `US` 多區域中的 Claude、Llama 和 Mistral AI 模型，可以使用 `US` 多區域中任何單一區域的 Agent Platform 端點。`EU` 多區域中的 Claude、Llama 和 Mistral AI 模型，可以使用 `EU` 多區域內任何單一區域的 Agent Platform 端點，但 `eu-west2` 和 `eu-west6` 除外。
* 這兩個多區域都不支援 Vertex AI 部署的模型。
* `US` 和 `EU` 多區域支援 [Cloud AI 服務](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)。

如果建立遠端模型的資料集位於多區域，則 Agent Platform 模型端點必須位於該多區域內的區域。舉例來說，如果資料集位於 `eu` 多區域，您可以指定 `europe-west1` 區域端點的網址 `https://europe-west1-aiplatform.googleapis.com/v1/projects/myproject/locations/europe-west1/publishers/google/models/<target_model>`。如果指定模型名稱而非端點網址，BigQuery ML 預設會針對 `eu` 多區域中的資料集使用 `europe-west4` 端點，並針對 `us` 多區域中的資料集使用 `us-central1` 端點。

#### 全球端點

如果是[支援的 Gemini 模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#supported_models)，您可以指定[全域端點](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#use_the_global_endpoint)。

全域端點涵蓋全球，可用性和可靠性高於單一區域。使用全域端點傳送要求，可提高整體可用性，並減少資源耗盡 (429) 錯誤。當您超過區域端點的配額時，就會發生這類錯誤。如要在不支援 Gemini 2.0+ 的區域使用該模型，可以改用全域端點，避免將資料遷移至其他區域。只有部署至全域端點的模型，才能使用 `AI.GENERATE_TEXT` 函式。

如果對資料處理位置有要求，請勿使用全域端點，因為使用全域端點時，您無法控管或得知處理要求的區域。

#### Google 模型和合作夥伴模型的處理位置

如要瞭解託管於 Agent Platform 的 Google 模型所使用的 ML 處理位置，請參閱「 [Google Cloud 模型的 ML 處理](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency?hl=zh-tw#ml-processing-google-models)」。這項資訊涵蓋部署至區域或多區域的模型。使用全域端點的模型不保證任何特定處理位置。

如要瞭解託管於 Agent Platform 的合作夥伴模型使用哪些 ML 處理位置，請參閱「[合作夥伴模型的 Google Cloud ML 處理](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency?hl=zh-tw#ml-processing-partner-models)」。

### 非遠端模型的位置

本節說明遠端模型以外的[模型](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw#supported_models)支援位置，以及模型處理作業的執行位置。  

#### 地區位置

下表列出遠端模型以外所有模型類型支援的位置：

|  | 地區說明 | 區域名稱 | 匯入 模型 | 內建 模型 訓練 | DNN/自動編碼器/ Boosted Tree/ 廣度和深度模型 訓練 | AutoML 模型 訓練 | 超參數 調整 | 整合 Vertex AI Model Registry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **美洲** | | | | | | | | |
|  | 俄亥俄州哥倫布 | `us-east5` | ● | ● |  |  |  |  |
|  | 達拉斯 | `us-south1` | ● | ● |  |  |  |  |  |
|  | 愛荷華州 | `us-central1` | ● | ● | ● | ● | ● | ● |
|  | 拉斯維加斯 | `us-west4` | ● | ● |  | ● |  | ● |
|  | 洛杉磯 | `us-west2` | ● | ● | ● |  |  | ● |
|  | 墨西哥 | `northamerica-south1` | ● | ● |  |  |  |  |  |  |
|  | 蒙特婁 | `northamerica-northeast1` | ● | ● | ● | ● | ● | ● |
|  | 北維吉尼亞州 | `us-east4` | ● | ● | ● | ● | ● | ● |
|  | 奧勒岡州 | `us-west1` | ● | ● | ● |  | ● | ● |
|  | 鹽湖城 | `us-west3` | ● | ● | ● |  |  |  |
|  | 聖保羅 | `southamerica-east1` | ● | ● | ● | ● |  |  |
|  | 聖地亞哥 | `southamerica-west1` | ● | ● |  |  |  |  |
|  | 南卡羅來納州 | `us-east1` | ● | ● | ● |  | ● | ● |
|  | 多倫多 | `northamerica-northeast2` | ● | ● |  | ● |  |  |
| **歐洲** | | | | | | | | |
|  | 比利時 | `europe-west1` | ● | ● | ● | ● | ● | ● |
|  | 柏林 | `europe-west10` | ● | ● |  |  |  |  |
|  | 芬蘭 | `europe-north1` | ● | ● | ● |  |  |  |
|  | 法蘭克福 | `europe-west3` | ● | ● | ● | ● | ● | ● |
|  | 倫敦 | `europe-west2` | ● | ● | ● | ● | ● | ● |
|  | 馬德里 | `europe-southwest1` | ● | ● |  |  |  |  |
|  | 米蘭 | `europe-west8` | ● | ● |  |  |  |  |
|  | 荷蘭 | `europe-west4` | ● | ● | ● | ● | ● | ● |
|  | 巴黎 | `europe-west9` | ● | ● |  |  |  |  |
|  | 斯德哥爾摩 | `europe-north2` | ● | ● |  |  |  |  |
|  | 杜林 | `europe-west12` |  | ● |  |  |  |  |
|  | 華沙 | `europe-central2` | ● | ● |  |  |  |  |
|  | 蘇黎世 | `europe-west6` | ● | ● | ● | ● | ● | ● |
| **亞太地區** | | | | | | | | |
|  | 曼谷 | `asia-southeast3` | ● | ● |  |  |  |  |
|  | 德里 | `asia-south2` | ● | ● |  |  |  |  |
|  | 香港 | `asia-east2` | ● | ● | ● | ● | ● | ● |
|  | 雅加達 | `asia-southeast2` | ● | ● |  |  |  | ● |
|  | 墨爾本 | `australia-southeast2` | ● | ● |  |  |  |  |
|  | 孟買 | `asia-south1` | ● | ● | ● | ● |  | ● |
|  | 大阪 | `asia-northeast2` | ● | ● | ● |  |  |  |
|  | 首爾 | `asia-northeast3` | ● | ● | ● | ● | ● | ● |
|  | 新加坡 | `asia-southeast1` | ● | ● | ● | ● | ● | ● |
|  | 雪梨 | `australia-southeast1` | ● | ● | ● | ● | ● | ● |
|  | 台灣 | `asia-east1` | ● | ● | ● | ● | ● | ● |
|  | 東京 | `asia-northeast1` | ● | ● | ● | ● | ● | ● |
| **中東地區** | | | | | | | | |
|  | 達曼 | `me-central2` |  | ● |  |  |  |  |
|  | 杜哈 | `me-central1` |  | ● |  |  |  |  |
|  | 特拉維夫 | `me-west1` | ● | ● |  |  |  |  |
| **非洲** | | | | | | | | |
|  | 約翰尼斯堡 | `africa-south1` | ● | ● |  |  |  |  |

#### 多地區位置

`US` 和 `EU` 多區域支援遠端模型以外的所有支援模型。

位於 `EU` 多區域的資料不會儲存在 `europe-west2` (倫敦) 或 `europe-west6` (蘇黎世) 資料中心。

Vertex AI Model Registry 整合功能僅支援單一區域整合。如果將多區域 BigQuery ML 模型傳送至 Model Registry，模型會在 Vertex AI 轉換為區域模型。BigQuery ML 多區域美國模型會同步至 Agent Platform `us-central1`，BigQuery ML 多區域歐盟模型則會同步至 Agent Platform `europe-west4`。單一區域模型則沒有任何異動。

#### 處理位置

如果是遠端模型以外的模型，BigQuery ML 會在資料集所在位置處理及暫存資料。

BigQuery ML 會依據《[服務專屬條款](https://cloud.google.com/terms/service-terms?hl=zh-tw#13-google-bigquery-service)》，將資料儲存在所選位置。

## BigQuery 遷移服務位置

BigQuery 遷移服務提供多項工具，可協助您從舊版資料倉儲遷移至 BigQuery。BigQuery 遷移服務包含多個 SQL 翻譯工具，可將 SQL 查詢翻譯成 GoogleSQL 或其他支援的 SQL 方言。包括[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)、[SQL Translation API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw) 和[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)。

BigQuery 遷移服務也包含[遷移歷程服務](https://docs.cloud.google.com/bigquery/docs/migration/migration-lineage?hl=zh-tw)，可將來源資料庫中的資料流程視覺化，協助您規劃資料倉儲遷移作業，以及[遷移驗證服務](https://docs.cloud.google.com/bigquery/docs/migration/migration-validation?hl=zh-tw)，可驗證遷移的資料。

BigQuery 遷移服務中的工具可在下列處理位置使用：

|  | **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- | --- |
| **亞太地區** | | | |
|  | 曼谷 | `asia-southeast3` |  |
|  | 德里 | `asia-south2` |  |
|  | 香港 | `asia-east2` |  |
|  | 雅加達 | `asia-southeast2` |  |
|  | 墨爾本 | `australia-southeast2` |  |
|  | 孟買 | `asia-south1` |  |
|  | 大阪 | `asia-northeast2` |  |
|  | 首爾 | `asia-northeast3` |  |
|  | 新加坡 | `asia-southeast1` |  |
|  | 雪梨 | `australia-southeast1` |  |
|  | 台灣 | `asia-east1` |  |
|  | 東京 | `asia-northeast1` |  |
| **歐洲** | | | |
|  | 比利時 | `europe-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 柏林 | `europe-west10` |  |
|  | 歐洲 (多區域) | `eu` |
|  | 芬蘭 | `europe-north1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 米蘭 | `europe-west8` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 巴黎 | `europe-west9` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 斯德哥爾摩 | `europe-north2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 杜林 | `europe-west12` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 華沙 | `europe-central2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **美洲** | | | |
|  | 俄亥俄州哥倫布 | `us-east5` |  |
|  | 達拉斯 | `us-south1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 拉斯維加斯 | `us-west4` |  |
|  | 洛杉磯 | `us-west2` |  |
|  | 墨西哥 | `northamerica-south1` |  |
|  | 北維吉尼亞州 | `us-east4` |  |
|  | 奧勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 鳳凰城 | `us-west8` |  |
|  | 魁北克 | `northamerica-northeast1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 鹽湖城 | `us-west3` |  |
|  | 聖地亞哥 | `southamerica-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 南卡羅來納州 | `us-east1` |  |
|  | 多倫多 | `northamerica-northeast2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 美國 (多區域) | `us` |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` |  |
| **MiddleEast** | | | |
|  | 達曼 | `me-central2` |  |
|  | 杜哈 | `me-central1` |  |
|  | 以色列 | `me-west1` |  |

## BigQuery 持續查詢位置

下表列出支援持續查詢的區域：

|  | 地區說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- | --- |
| **美洲** | | | |
|  | 美國 (多區域) | `us` |
|  | 哥倫布 | `us-east5` |  |
|  | 達拉斯 | `us-south1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 拉斯維加斯 | `us-west4` |  |
|  | 洛杉磯 | `us-west2` |  |
|  | 墨西哥 | `northamerica-south1` |  |
|  | 蒙特婁 | `northamerica-northeast1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 北維吉尼亞州 | `us-east4` |  |
|  | 奧克拉荷馬州 | `us-central2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 奧勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 鹽湖城 | `us-west3` |  |
|  | 聖地亞哥 | `southamerica-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 南卡羅來納州 | `us-east1` |  |
|  | 多倫多 | `northamerica-northeast2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **亞太地區** | | | |
|  | 德里 | `asia-south2` |  |
|  | 香港 | `asia-east2` |  |
|  | 雅加達 | `asia-southeast2` |  |
|  | 墨爾本 | `australia-southeast2` |  |
|  | 孟買 | `asia-south1` |  |
|  | 大阪 | `asia-northeast2` |  |
|  | 首爾 | `asia-northeast3` |  |
|  | 新加坡 | `asia-southeast1` |  |
|  | 雪梨 | `australia-southeast1` |  |
|  | 台灣 | `asia-east1` |  |
|  | 東京 | `asia-northeast1` |  |
| **歐洲** | | | |
|  | 歐洲 (多區域) | `eu` |
|  | 比利時 | `europe-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 柏林 | `europe-west10` |  |
|  | 芬蘭 | `europe-north1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 米蘭 | `europe-west8` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 巴黎 | `europe-west9` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 斯德哥爾摩 | `europe-north2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 杜林 | `europe-west12` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 華沙 | `europe-central2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **中東地區** | | | |
|  | 杜哈 | `me-central1` |  |
|  | 達曼 | `me-central2` |  |
|  | 特拉維夫 | `me-west1` |  |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` |  |

## BigQuery 分區和分群建議工具位置

[BigQuery 分區和分群建議工具](https://docs.cloud.google.com/bigquery/docs/manage-partition-cluster-recommendations?hl=zh-tw)會產生分區或分群建議，協助您最佳化 BigQuery 資料表。

分區和分群建議工具適用於下列處理位置：

|  | **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- | --- |
| **亞太地區** | | | |
|  | 德里 | `asia-south2` |  |
|  | 香港 | `asia-east2` |  |
|  | 雅加達 | `asia-southeast2` |  |
|  | 孟買 | `asia-south1` |  |
|  | 大阪 | `asia-northeast2` |  |
|  | 首爾 | `asia-northeast3` |  |
|  | 新加坡 | `asia-southeast1` |  |
|  | 雪梨 | `australia-southeast1` |  |
|  | 台灣 | `asia-east1` |  |
|  | 東京 | `asia-northeast1` |  |
| **歐洲** | | | |
|  | 比利時 | `europe-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 柏林 | `europe-west10` |  |
|  | 歐洲 (多區域) | `eu` |
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **美洲** | | | |
|  | 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 拉斯維加斯 | `us-west4` |  |
|  | 洛杉磯 | `us-west2` |  |
|  | 蒙特婁 | `northamerica-northeast1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 北維吉尼亞州 | `us-east4` |  |
|  | 奧勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 鹽湖城 | `us-west3` |  |
|  | 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 多倫多 | `northamerica-northeast2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 美國 (多區域) | `us` |

## BigQuery 共用位置

BigQuery sharing (舊稱 Analytics Hub) 適用於下列區域和多區域。

#### 區域

下表列出可使用分享功能的美洲地區。

| 地區說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- |
| 俄亥俄州哥倫布 | `us-east5` |  |
| 達拉斯 | `us-south1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 拉斯維加斯 | `us-west4` |  |
| 洛杉磯 | `us-west2` |  |
| 墨西哥 | `northamerica-south1` |  |
| 蒙特婁 | `northamerica-northeast1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 北維吉尼亞州 | `us-east4` |  |
| 奧克拉荷馬州 | `us-central2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 奧勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 鹽湖城 | `us-west3` |  |
| 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 聖地亞哥 | `southamerica-west1` |  |
| 南卡羅來納州 | `us-east1` |  |
| 多倫多 | `northamerica-northeast2` |  |
|

下表列出亞太地區可共用資料的區域。

| 地區說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- |
| 德里 | `asia-south2` |  |
| 香港 | `asia-east2` |  |
| 雅加達 | `asia-southeast2` |  |
| 墨爾本 | `australia-southeast2` |  |
| 孟買 | `asia-south1` |  |
| 大阪 | `asia-northeast2` |  |
| 首爾 | `asia-northeast3` |  |
| 新加坡 | `asia-southeast1` |  |
| 雪梨 | `australia-southeast1` |  |
| 台灣 | `asia-east1` |  |
| 東京 | `asia-northeast1` |  |

下表列出可分享資料的歐洲地區。

| 地區說明 | 區域名稱 | 詳細資料 |
| --- | --- | --- |
| 比利時 | `europe-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 柏林 | `europe-west10` |  |
| 芬蘭 | `europe-north1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 法蘭克福 | `europe-west3` |  |
| 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 米蘭 | `europe-west8` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 巴黎 | `europe-west9` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 杜林 | `europe-west12` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 華沙 | `europe-central2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |

下表列出中東地區可使用分享功能的國家/地區。

| **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 達曼 | `me-central2` |  |
| 杜哈 | `me-central1` |  |
| 特拉維夫 | `me-west1` |  |

下表列出可分享位置資訊的非洲地區。

| **區域說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 約翰尼斯堡 | `africa-south1` |  |

#### 多區域

下表列出可共用的多區域。

| 多地區說明 | 多地區名稱 |
| --- | --- |
| 歐盟[成員國](https://europa.eu/european-union/about-eu/countries_en)境內的資料中心1 | `EU` |
| 美國資料中心 | `US` |

1 位於 `EU` 多區域的資料不會儲存在 `europe-west2` (倫敦) 或 `europe-west6` (蘇黎世) 資料中心。

#### Omni 區域

下表列出可分享內容的 Omni 裝置。

|  | Omni 區域說明 | Omni 區域名稱 |
| --- | --- | --- |
| **AWS** | | |
|  | AWS - 美國東部 (北維吉尼亞州) | `aws-us-east-1` |
|  | AWS - 美國西部 (奧勒岡州) | `aws-us-west-2` |
|  | AWS - 亞太地區 (首爾) | `aws-ap-northeast-2` |
|  | AWS - 亞太地區 (雪梨) | `aws-ap-southeast-2` |
|  | AWS - 歐洲 (愛爾蘭) | `aws-eu-west-1` |
|  | AWS - 歐洲 (法蘭克福) | `aws-eu-central-1` |
| **Azure** | | |
|  | Azure - 美國東部 2 | `azure-eastus2` |

## 指定位置

如要確保 BigQuery 查詢儲存在特定區域或多區域，請在工作要求中指定位置。指定位置可確保使用全域 BigQuery 端點時，查詢會在正確的位置執行。

如未指定位置，當查詢用於決定 BigQuery 中的處理位置時，可能會暫時儲存在 BigQuery 路由器記錄中。

如果[專案](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw#projects)在 `US` 以外的區域有依運算能力計費的預留項目，且查詢未參照資料集內的任何資料表或其他資源，則提交工作時，必須明確指定依運算能力計費的預留項目位置。依據容量的承諾使用合約會與位置 (例如 `US` 或 `EU`) 繫結。如果您在運算資源位置以外的地方執行工作，該工作的定價會自動轉為隨選定價。

您可以透過下列方式，明確指定執行工作的位置：

* 在 Google Cloud 控制台的查詢編輯器中查詢資料時，請依序點選settings「More」(更多) >「Query settings」(查詢設定)，展開「Advanced options」(進階選項)，然後選取「Data location」(資料位置)。
* 編寫 SQL 查詢時，請在查詢的第一個陳述式中設定 [`@@location` 系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)。
* 使用 bq 指令列工具時，請提供 `--location` [全域旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#global_flags)，並將值設為您的位置。
* 當您使用 API 時，請在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，將 `location` 屬性的值指定為您的地區。

如果指定的位置與要求中資料集的位置不相符，BigQuery 就會傳回錯誤。要求中涉及的所有資料集所在位置 (包括讀取及寫入的資料集) 都必須與推測或指定的工作所在位置相符。

單一區域位置與多區域位置不相符，即使單一區域位置包含在多區域位置中也一樣。因此，如果位置同時包含單一區域和多區域位置，查詢就會以[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)的形式執行。舉例來說，如果工作的地點設為 `US`，且參照 `us-central1` 中的資料集，則該工作會是全域查詢。同樣地，如果工作參照 `US` 中的一個資料集和 `us-central1` 中的另一個資料集，則會是全域查詢。如果 `JOIN` 陳述式同時包含區域和多區域中的資料表，也適用這項規則。

[動態查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#execute_immediate)在執行前不會剖析，因此無法用於自動判斷查詢的區域。

## 預設位置

如果您未[明確指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)，系統會透過下列其中一種方式決定位置：

* 要求中參照的資料集位置。舉例來說，如果查詢參照儲存在 `asia-northeast1` 區域的資料集中的資料表或檢視表，查詢工作就會在 `asia-northeast1` 執行。
* 要求中參照的連線指定區域。
* 目的地資料表的位置。

如果未明確指定位置，且無法從要求中的資源判斷，則會使用預設位置。如未設定預設位置，工作會在 `US` 多區域執行。

如要進一步瞭解如何設定預設位置，請參閱「[指定全域設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#global-settings)」。

## 位置、預留項目和工作

容量使用承諾是地區性資源。購買運算單元時，這些運算單元僅限於特定區域或多區域。如果您的運算資源承諾使用合約僅限於 `EU`，則無法在 `US` 建立預留項目。建立預留項目時，您必須指定位置 (區域) 和運算單元數量。這些運算單元會從您在該區域的承諾使用資源中提取。

同樣地，在某個區域執行工作時，只有在工作位置與預留項目位置相符時，才會使用預留項目，除非工作是[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)。舉例來說，如果您將預留項目指派給 `EU` 中的專案，並在該專案中對位於 `US` 的資料集執行查詢，則該查詢不會在 `EU` 預留項目中執行。如果沒有任何 `US` 預留項目，系統會以隨選方式執行工作。

## 位置注意事項

選擇資料的位置時，請考慮下列事項：

### Cloud Storage

您可以透過下列方式，使用 BigQuery 與 Cloud Storage 資料互動：

* 使用 BigLake 或非 BigLake 外部資料表[查詢 Cloud Storage 資料](#query-storage-data-location)
* [將 Cloud Storage 資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#load-data-location-considerations)

#### 查詢 Cloud Storage 資料

使用 [BigLake](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw) 或[非 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-data?hl=zh-tw)查詢 Cloud Storage 中的資料時，查詢的資料必須與 BigQuery 資料集位於相同位置，否則查詢會產生[資料移轉費用](https://cloud.google.com/storage/pricing?hl=zh-tw#network-buckets)。例如：

* [單一區域 bucket](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#location-r)：如果 BigQuery 資料集位於華沙 (`europe-central2`) 區域，對應的 Cloud Storage bucket 也必須位於華沙區域，或任何包含華沙的 Cloud Storage 雙區域。如果 BigQuery 資料集位於 `US` 多區域，Cloud Storage bucket 則可位於愛荷華州 (`us-central1`) 單一區域，或任何包含愛荷華州的雙區域。即使 bucket 位於資料集多區域範圍內，從任何其他單一區域執行的查詢仍會產生資料移轉費用。舉例來說，如果外部資料表位於 `US` 多區域，而 Cloud Storage bucket 位於奧勒岡州 (`us-west1`)，則工作會產生資料移轉費用。

  如果 BigQuery 資料集位於 `EU` 多區域，Cloud Storage bucket 則可位於荷蘭 (`europe-west4`) 單一區域，或任何包含荷蘭 (`europe-west4`) 的雙區域。從任何其他單一區域執行的查詢都會產生資料移轉費用，即使 bucket 位於資料集多區域內的位置也一樣。舉例來說，如果外部資料表位於 `EU` 多區域，而 Cloud Storage bucket 位於華沙 (`europe-central2`)，則工作會產生資料移轉費用。
* [雙區域 bucket](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#location-dr)：如果 BigQuery 資料集位於東京 (`asia-northeast1`) 區域，對應的 Cloud Storage bucket 必須位於東京區域，或包含東京的雙區域，例如 `ASIA1` 雙區域。

  如果 Cloud Storage bucket 位於 `NAM4` 雙區域或任何包含愛荷華州 (`us-central1`) 區域的雙區域，則對應的 BigQuery 資料集可以位於 `US` 多區域或愛荷華州 (`us-central1`)。

  如果 Cloud Storage bucket 位於 `EUR4` 雙區域或任何包含荷蘭 (`europe-west4`) 區域的雙區域，則對應的 BigQuery 資料集可以位於 `EU` 多區域或荷蘭 (`europe-west4`)。
* [多區域 bucket](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#location-mr)：**不建議**在外部資料表使用多區域資料集位置和多區域 Cloud Storage bucket，因為外部查詢效能取決於最低延遲時間和最佳網路頻寬。

  如果 BigQuery 資料集位於 `US` 多區域，對應的 Cloud Storage bucket 必須位於包含愛荷華州 (`us-central1`) 的雙區域 (例如 `NAM4` 雙區域)，或包含愛荷華州 (`us-central1`) 的自訂雙區域。

  如果 BigQuery 資料集位於 `EU` 多區域，對應的 Cloud Storage bucket 必須位於包含荷蘭 (`europe-west4`) 的雙區域 (例如 `EUR4` 雙區域)，或包含荷蘭 (`europe-west4`) 的自訂雙區域。

如要進一步瞭解支援的 Cloud Storage 位置，請參閱 Cloud Storage 說明文件中的「[Bucket 位置](https://docs.cloud.google.com/storage/docs/bucket-locations?hl=zh-tw)」。

#### 將 Cloud Storage 資料載入 BigQuery

從 Cloud Storage 載入資料時，載入的資料必須與 BigQuery 資料集位於相同位置，否則載入工作會產生資料移轉費用。

如要進一步瞭解載入資料移轉費用，請參閱「[查詢 Cloud Storage 資料](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#query-storage-data-location)」一節，因為批次載入和查詢都適用相同的指南。

詳情請參閱「[批次載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)」。

### Bigtable

從 Bigtable 查詢資料或將資料匯出至 Bigtable 時，必須考量位置。

#### 查詢 Bigtable 資料

透過 BigQuery [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)[查詢 Bigtable 中的資料](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-tw)時，Bigtable 執行個體必須與 BigQuery 資料集位於相同位置：

* 單一區域：如果 BigQuery 資料集位於比利時 (`europe-west1`) 區域位置，對應的 Bigtable 執行個體必須位於比利時區域。
* 多區域：外部查詢效能取決於最低延遲時間和最佳網路頻寬，因此**不建議**在 Bigtable 外部資料表使用多區域資料集位置。

如要進一步瞭解支援的 Bigtable 位置，請參閱「[Bigtable 位置](https://docs.cloud.google.com/bigtable/docs/locations?hl=zh-tw)」。

#### 將資料匯出至 Bigtable

* 如果 BigQuery 資料集位於多區域，則必須設定 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)，將資料轉送至該多區域內的 Bigtable 叢集。舉例來說，如果 BigQuery 資料集位於 `US` 多區域，Bigtable 叢集可以位於 `us-west1` (奧勒岡州) 區域，該區域位於美國境內。
* 如果 BigQuery 資料集位於單一區域，則必須設定 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)，將資料轉送至同一區域中的 Bigtable 叢集。舉例來說，如果 BigQuery 資料集位於 `asia-northeast1` (東京) 區域，Bigtable 叢集也必須位於 `asia-northeast1` (東京) 區域。

### Google 雲端硬碟

位置考量不適用於 [Google 雲端硬碟](https://docs.cloud.google.com/bigquery/external-data-drive?hl=zh-tw)外部資料來源。

### Cloud SQL

透過 BigQuery [聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)[查詢 Cloud SQL 中的資料](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-tw)時，Cloud SQL 執行個體必須與 BigQuery 資料集位於相同位置。

* 單一區域：如果 BigQuery 資料集位於比利時 (`europe-west1`) 區域位置，對應的 Cloud SQL 執行個體必須位於比利時區域。
* 多區域：如果 BigQuery 資料集位於 `US` 多區域，對應的 Cloud SQL 執行個體必須位於美國地理區域中的單一區域。

如要進一步瞭解支援的 Cloud SQL 位置，請參閱「[Cloud SQL 位置](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_regions)」。

### Spanner

透過 BigQuery [聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)[查詢 Spanner 中的資料](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw)時，Spanner 執行個體必須與 BigQuery 資料集位於相同位置。

* 單一區域：如果 BigQuery 資料集位於比利時 (`europe-west1`) 區域位置，對應的 Spanner 執行個體必須位於比利時區域。
* 多區域：如果 BigQuery 資料集位於 `US` 多區域，對應的 Spanner 執行個體必須位於美國地理區域中的單一區域。

如要進一步瞭解支援的 Spanner 位置，請參閱「[Spanner 位置](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_regions)」。

### 分析工具

將 BigQuery 資料集與[分析工具](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)放在相同位置：

* [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc/docs/concepts/overview?hl=zh-tw)：使用 [BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/bigquery?hl=zh-tw)查詢 BigQuery 資料集時，BigQuery 資料集應與 Managed Service for Apache Spark 叢集位於相同位置。
所有 [Compute Engine 位置](https://docs.cloud.google.com/compute/docs/regions-zones?hl=zh-tw#available)都支援 Managed Service for Apache Spark。* [Vertex AI Workbench](https://docs.cloud.google.com/vertex-ai/docs/workbench/introduction?hl=zh-tw)：在 Vertex AI Workbench 中使用 [Jupyter 筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw#other_programmatic_analysis_solutions)查詢 BigQuery 資料集時，BigQuery 資料集應與 Vertex AI Workbench 執行個體位於相同位置。
查看[支援的 Vertex AI Workbench 位置](https://docs.cloud.google.com/vertex-ai/docs/general/locations?hl=zh-tw#vertex-ai-workbench-locations)。

### 資料管理計畫

制定資料管理計畫：

* 如果選擇區域性儲存資源 (例如 BigQuery 資料集或 Cloud Storage bucket)，請制定[資料地理位置管理](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw#geographic_management_of_data)計畫。

## 限制位置

您可以使用[組織政策服務](https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview?hl=zh-tw)，限制資料集的建立位置。詳情請參閱「[限制資源位置](https://docs.cloud.google.com/resource-manager/docs/organization-policy/defining-locations?hl=zh-tw)」和「[資源位置支援的服務](https://docs.cloud.google.com/resource-manager/docs/organization-policy/defining-locations-supported-services?hl=zh-tw#bigquery)」。

## 資料集安全性

如要控管 BigQuery 資料集的存取權，請參閱「[控管資料集的存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。如要瞭解資料加密，請參閱「[靜態資料加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。
* 瞭解如何[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)。
* 瞭解 BigQuery 的[計價方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。
* 瞭解[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)。
* [查看全球各地提供的所有 Google Cloud 服務](https://docs.cloud.google.com/about/locations?hl=zh-tw#region)。
* [探索其他以位置為基礎的概念](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw)，例如適用於其他 Google Cloud 服務的可用區。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-17 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-17 (世界標準時間)。"],[],[]]