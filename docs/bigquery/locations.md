Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [資源](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 位置

本頁面說明「位置」的概念，以及可儲存和處理資料的不同區域。儲存空間和分析的價格也取決於資料位置和預訂。如要進一步瞭解各個位置的價格，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。如要瞭解如何設定資料集的位置，請參閱「[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)」。如要瞭解預留位置，請參閱「[管理不同地區的預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#manage_reservations_in_different_regions)」。

如要進一步瞭解 BigQuery 資料移轉服務如何使用位置資訊，請參閱[資料位置和移轉作業](https://docs.cloud.google.com/bigquery/docs/dts-locations?hl=zh-tw)。

## 地點和區域

BigQuery 提供兩種資料和運算位置：

* 「地區」是特定的地理位置，例如倫敦。
* 「多地區」是指包含許多獨立區域的大型地理區域，例如美國或歐洲。多區域位置提供的配額比單一區域大，但多區域位置不會提供區域備援。資料會儲存在單一區域，且運算作業只會在該區域內提供。如要跨區域備援，BigQuery 提供[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)功能。

無論是哪種位置類型，BigQuery 都會自動將資料副本儲存在所選位置的單一區域內，兩個不同的可用區。即使多區域位於同一區域，系統仍會將其視為與其他區域不同。如要進一步瞭解資料可用性和耐久性，請參閱「[災難復原規劃](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw#disaster_planning)」。

## 支援的地區

BigQuery 資料集可儲存在下列地區和多地區。如要進一步瞭解地區和區域，請參閱[地理位置與地區](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw)。

### 區域

下表列出 BigQuery 在美洲的可用地區。

| **地區說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 俄亥俄州哥倫布 | `us-east5` |  |
| 達拉斯 | `us-south1` |  |
| 愛荷華州 | `us-central1` |  |
| 拉斯維加斯 | `us-west4` |  |
| 洛杉磯 | `us-west2` |  |
| 墨西哥 | `northamerica-south1` |  |
| 蒙特婁 | `northamerica-northeast1` |  |
| 北維吉尼亞州 | `us-east4` |  |
| 奧勒岡州 | `us-west1` |  |
| 鹽湖城 | `us-west3` |  |
| 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 聖地亞哥 | `southamerica-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 南卡羅來納州 | `us-east1` |  |
| 多倫多 | `northamerica-northeast2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|

下表列出 BigQuery 適用的亞太地區。

| **地區說明** | **區域名稱** | **詳細資料** |
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

下表列出 BigQuery 適用的歐洲地區。

| **地區說明** | **區域名稱** | **詳細資料** |
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
| 杜林 | `europe-west12` |  |
| 華沙 | `europe-central2` |  |
| 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |

下表列出 BigQuery 服務在中東地區的可用區域。

| **地區說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 達曼 | `me-central2` |  |
| 杜哈 | `me-central1` |  |
| 特拉維夫市 | `me-west1` |  |

下表列出 BigQuery 在非洲的適用區域。

| **地區說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 約翰尼斯堡 | `africa-south1` |  |

### 多區域

下表列出 BigQuery 適用的多區域。選取多區域時，BigQuery 會在多區域內選取單一區域，用於儲存及處理資料。

| **多地區說明** | **多區域名稱** |
| --- | --- |
| 歐盟1[成員國](https://europa.eu/european-union/about-eu/countries_en)境內的資料中心 | `EU` |
| 美國資料中心2 | `US` |

**注意：**選取多區域位置不會提供跨區域複製或區域備援功能，因此如果發生區域服務中斷，資料集可用性不會提高。資料會儲存在地理位置內的單一區域。

1 位於 `EU` 多地區的資料只會儲存在下列其中一個位置：`europe-west1` (比利時) 或 `europe-west4` (荷蘭)。
BigQuery 會自動決定資料的儲存和處理位置。

2 位於 `US` 多地區的資料只會儲存在下列其中一個位置：`us-central1` (愛荷華州)、`us-west1` (奧勒岡州) 或 `us-central2` (奧克拉荷馬州)。BigQuery 會自動決定資料的儲存和處理位置。

## BigQuery Studio 位置

BigQuery Studio 可讓您儲存、共用及管理程式碼資產版本，例如[筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)和[已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw)。

下表列出 BigQuery Studio 適用的地區：

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
|  | 俄勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
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
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 馬德里 | `europe-southwest1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 杜林 | `europe-west12` |  |
|  | 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **中東地區** | | | |
|  | 杜哈 | `me-central1` |  |
|  | 達曼 | `me-central2` |  |

## BigQuery Omni 位置

BigQuery Omni 會在與包含所查詢資料表的資料集相同位置處理查詢。建立資料集後，就無法變更位置。您的資料會儲存在 AWS 或 Azure 帳戶中。BigQuery Omni 區域支援 Enterprise 版本的預留項目和隨選運算 (分析) 定價。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

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

本節說明[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)支援的位置，以及遠端模型處理作業的發生位置。  

#### 地區位置

如要瞭解 Google 模型和合作夥伴模型支援的遠端模型位置，請參閱下列說明文件：

* 如要瞭解 Gemini 模型和嵌入模型支援的區域，請參閱「[Google 模型端點位置](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#google_model_endpoint_locations)」。
* 如要瞭解 Claude、Llama 和 Mistral AI 模型支援的地區，請參閱「[Google Cloud 合作夥伴模型端點位置](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#genai-partner-models)」。

下表列出透過 Cloud AI 服務支援遠端模型的區域，以及部署至 Vertex AI 的自訂模型。資料欄名稱會指出遠端模型的類型。

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
|  | 俄勒岡州 | `us-west1` | ● |  |  |  |  | ● |
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
|  | 特拉維夫市 | `me-west1` | ● |  |  |  |  |  |

如果您要建立遠端模型的資料集位於單一地區，Vertex AI 模型端點就必須位於相同地區。如果您指定模型端點網址，請使用與資料集相同區域的端點。舉例來說，如果資料集位於 `us-central1` 地區，請指定端點 `https://us-central1-aiplatform.googleapis.com/v1/projects/myproject/locations/us-central1/publishers/google/models/<target_model>`。如果您指定模型名稱，BigQuery ML 會自動選擇正確區域中的端點。

#### 多地區位置

遠端模型的多區域支援如下：

* Gemini 模型支援 `US` 和 `EU` 多區域。
* `US` 多區域中的 Claude、Llama 和 Mistral AI 模型，可使用 `US` 多區域內任一區域的 Vertex AI 端點。`EU` 多區域中的 Claude、Llama 和 Mistral AI 模型可使用 Vertex AI 端點，適用於 `EU` 多區域內的任何單一區域，但 `eu-west2` 和 `eu-west6` 除外。
* 這兩個多區域都不支援 Vertex AI 部署的模型。
* [Cloud AI 服務](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)支援 `US` 和 `EU` 多區域。

如果建立遠端模型的資料集位於多地區，則 Vertex AI 模型端點必須位於該多地區內的區域。舉例來說，如果資料集位於 `eu` 多區域，則可以指定 `europe-west1` 區域端點的網址 `https://europe-west1-aiplatform.googleapis.com/v1/projects/myproject/locations/europe-west1/publishers/google/models/<target_model>`。如果您指定模型名稱而非端點網址，BigQuery ML 預設會對 `eu` 多區域中的資料集使用 `europe-west4` 端點，並對 `us` 多區域中的資料集使用 `us-central1` 端點。

#### 全域端點

如要使用[支援的 Gemini 模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#supported_models)，可以指定[全域端點](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#use_the_global_endpoint)。

全域端點涵蓋全球，與單一區域相比，可用性和可靠性更高。對要求使用全域端點可提高整體可用性，同時減少資源耗盡 (429) 錯誤，這類錯誤會在您超出區域端點配額時發生。如要在 Gemini 2.0 以上版本未開放的區域使用，可以改用全球端點，避免資料遷移至其他區域。您只能使用部署至全域端點的模型和 `AI.GENERATE_TEXT` 函式。

如果您對資料處理位置有要求，請勿使用全域端點，因為使用全域端點時，您無法控管或瞭解處理要求所在的區域。

#### Google 模型和合作夥伴模型的處理位置

如要瞭解 Vertex AI 中託管的 Google 模型所用的處理位置，請參閱「[模型適用的機器學習處理 Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency?hl=zh-tw#ml-processing-google-models) 」一文。這項資訊涵蓋部署至單一或多個區域的模型。使用全域端點的模型無法保證任何特定處理位置。

如要瞭解 Vertex AI 代管合作夥伴模型時使用的處理位置，請參閱「[合作夥伴模型的機器學習處理 Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency?hl=zh-tw#ml-processing-partner-models) 」。

### 非遠端模型的位置

本節說明支援[模型](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw#supported_models)的位置 (遠端模型除外)，以及模型處理作業的發生位置。  

#### 地區位置

下表列出所有模型類型 (遠端模型除外) 支援的位置：

|  | 地區說明 | 區域名稱 | 匯入的模型 | 內建 模型 訓練 | DNN/自動編碼器/ 增強型樹狀結構/ 廣度和深度模型 模型訓練 | AutoML 模型 訓練 | 超參數 調整 | 整合 Vertex AI Model Registry |
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
|  | 俄勒岡州 | `us-west1` | ● | ● | ● |  | ● | ● |
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
|  | 特拉維夫市 | `me-west1` | ● | ● |  |  |  |  |
| **非洲** | | | | | | | | |
|  | 約翰尼斯堡 | `africa-south1` | ● | ● |  |  |  |  |

#### 多地區位置

`US` 和 `EU` 多區域支援所有模型 (遠端模型除外)。

位於 `EU` 多地區的資料不會儲存在 `europe-west2` (倫敦) 或 `europe-west6` (蘇黎世) 資料中心。

只有單一區域整合支援 Vertex AI Model Registry 整合。如果您將多區域 BigQuery ML 模型傳送至 Model Registry，該模型會在 Vertex AI 中轉換為區域模型。BigQuery ML 美國多區域模型會同步至 Vertex AI
`us-central1`，BigQuery ML 歐盟多區域模型則會同步至 Vertex AI `europe-west4`。單一區域模型不會有任何變更。

#### 處理位置

如果是遠端模型以外的模型，BigQuery ML 會在與包含資料的資料集相同位置中處理及暫存資料。

BigQuery ML 會根據[服務專屬條款](https://cloud.google.com/terms/service-terms?hl=zh-tw#13-google-bigquery-service)，將資料儲存在選取的位置。

## BigQuery SQL 翻譯器支援的地區

將舊版資料倉儲中的資料遷移至 BigQuery 時，您可以使用多種 SQL 翻譯器，將 SQL 查詢翻譯為 GoogleSQL 或其他支援的 SQL 方言。包括[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)、[SQL 翻譯 API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw) 和[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)。

BigQuery SQL 翻譯工具可在下列處理位置使用：

|  | **地區說明** | **區域名稱** | **詳細資料** |
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
|  | 米蘭 | `europe-west8` |  |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 巴黎 | `europe-west9` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 斯德哥爾摩 | `europe-north2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 杜林 | `europe-west12` |  |
|  | 華沙 | `europe-central2` |  |
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
|  | 魁北克 | `northamerica-northeast1` | [低 CO2](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) 區域 |
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

下表列出支援連續查詢的區域：

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
|  | 俄勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
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
|  | 米蘭 | `europe-west8` |  |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 巴黎 | `europe-west9` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 斯德哥爾摩 | `europe-north2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 杜林 | `europe-west12` |  |
|  | 華沙 | `europe-central2` |  |
|  | 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **中東地區** | | | |
|  | 杜哈 | `me-central1` |  |
|  | 達曼 | `me-central2` |  |
|  | 特拉維夫市 | `me-west1` |  |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` |  |

## BigQuery 分區和叢集建議工具位置

[BigQuery 分區和分群建議工具](https://docs.cloud.google.com/bigquery/docs/manage-partition-cluster-recommendations?hl=zh-tw)會產生分區或分群建議，協助您最佳化 BigQuery 資料表。

分區與分群建議工具適用於下列處理位置：

|  | **地區說明** | **區域名稱** | **詳細資料** |
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

BigQuery sharing (舊稱 Analytics Hub) 適用於下列區域和多重區域。

#### 區域

下表列出美洲地區中可共用的區域。

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
| 俄勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 鹽湖城 | `us-west3` |  |
| 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| 聖地亞哥 | `southamerica-west1` |  |
| 南卡羅來納州 | `us-east1` |  |
| 多倫多 | `northamerica-northeast2` |  |
|

下表列出亞太地區可分享的區域。

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

下表列出歐洲地區中可分享的區域。

| 地區說明 | 區域名稱 | 詳細資料 |
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
| 杜林 | `europe-west12` |  |
| 華沙 | `europe-central2` |  |
| 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |

下表列出可共用位置資訊的中東地區。

| **地區說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 達曼 | `me-central2` |  |
| 杜哈 | `me-central1` |  |
| 特拉維夫市 | `me-west1` |  |

下表列出非洲可分享位置資訊的地區。

| **地區說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- |
| 約翰尼斯堡 | `africa-south1` |  |

#### 多區域

下表列出可共用的多重區域。

| 多地區說明 | 多地區名稱 |
| --- | --- |
| 歐盟1[成員國](https://europa.eu/european-union/about-eu/countries_en)境內的資料中心 | `EU` |
| 美國資料中心 | `US` |

1 位於 `EU` 多地區的資料，不會存放在 `europe-west2` (倫敦) 或 `europe-west6` (蘇黎世) 資料中心。

#### Omni 區域

下表列出可分享的 Omni。

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

如要確保 BigQuery 查詢儲存在特定區域或多區域，請在工作要求中指定位置。指定位置可確保您使用全域 BigQuery 端點時，查詢會在正確位置執行。

如果您未指定位置，查詢可能會暫時儲存在 BigQuery 路由器記錄中，因為查詢會用於判斷 BigQuery 中的處理位置。

如果[專案](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw#projects)在 `US` 以外的區域有以容量為準的預訂方案，且查詢未參考資料集中的任何資料表或其他資源，則提交工作時，您必須明確指定以容量為準的預訂方案位置。以容量為準的承諾會與位置資訊 (例如 `US` 或 `EU`) 綁定。如果工作地點不在你的容量範圍內，系統會自動將該工作的價格改為隨選價格。

您可以透過下列方式明確指定工作的執行位置：

* 使用查詢編輯器在 Google Cloud 控制台中查詢資料時，請依序點選 settings「更多」>「查詢設定」，展開「進階選項」，然後選取「資料位置」。
* 撰寫 SQL 查詢時，請在查詢的第一個陳述式中設定 [`@@location` 系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)。
* 使用 bq 指令列工具時，請提供 `--location`
  [通用旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#global_flags)，然後將該值設定為您的位置。
* 當您使用 API 時，請在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，將 `location` 屬性的值指定為您的地區。

如果您指定的位置與要求中資料集的位置不相符，BigQuery 就會傳回錯誤。要求中涉及的所有資料集所在位置 (包括讀取及寫入的資料集) 都必須與推測或指定的工作所在位置相符。

單一區域位置與多區域位置不符，即使單一區域位置包含在多區域位置中也是如此。因此，如果位置同時包含單一區域位置和多區域位置，系統會將查詢做為[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)執行。舉例來說，如果工作的位置設為 `US`，但工作參照 `us-central1` 中的資料集，則工作會是全域查詢。同樣地，如果工作參照 `US` 中的一個資料集，以及 `us-central1` 中的另一個資料集，就會成為全域查詢。如果 `JOIN` 陳述式中的資料表同時位於區域和多區域，也會發生這種情況。

[動態查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#execute_immediate)會在執行時才進行剖析，因此無法用於自動判斷查詢的區域。

## 預設位置

如果沒有[明確指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)，系統會透過下列其中一種方式判斷位置：

* 要求中參照的資料集位置。舉例來說，如果查詢參考了儲存在 `asia-northeast1` 區域資料集內的資料表或檢視區塊，查詢工作就會在 `asia-northeast1` 執行。
* 要求中參照的連線指定區域。
* 目的地資料表的位置。

如果未明確指定位置，且系統無法從要求中的資源判斷位置，就會使用預設位置。如果未設定預設位置，工作會在 `US` 多地區執行。

如要進一步瞭解如何設定預設位置，請參閱「[指定全域設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#global-settings)」。

## 地點、預約和工作

容量使用承諾是地區性資源。購買運算單元時，這些運算單元僅限於特定區域或多區域。如果您的唯一容量承諾位於 `EU`，則無法在 `US` 中建立預留項目。建立預留項目時，您需要指定位置 (區域) 和運算單元數量。這些運算單元會從該區域的容量使用承諾中提取。

同樣地，在某個區域執行工作時，只有在工作位置與預留項目位置相符時，工作才會使用預留項目，除非工作是[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)。舉例來說，如果您在 `EU` 中將預留項目指派給專案，並在該專案中對位於 `US` 的資料集執行查詢，則該查詢不會在 `EU` 預留項目中執行。如果沒有任何 `US` 預訂方案，工作會以隨選模式執行。

## 位置注意事項

選擇資料的位置時，請考慮下列事項：

### Cloud Storage

您可以使用 BigQuery，透過下列方式與 Cloud Storage 資料互動：

* 使用 BigLake 或非 BigLake 外部資料表[查詢 Cloud Storage 資料](#query-storage-data-location)
* [將 Cloud Storage 資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#load-data-location-considerations)

#### 查詢 Cloud Storage 資料

使用 [BigLake](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw) 或[非 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-data?hl=zh-tw)查詢 Cloud Storage 中的資料時，所查詢資料的位置必須與 BigQuery 資料集的位置相同，否則查詢會產生[資料移轉費用](https://cloud.google.com/storage/pricing?hl=zh-tw#network-buckets)。例如：

* [單一區域值區](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#location-r)：如果您的 BigQuery 資料集位於華沙 (`europe-central2`) 區域，對應的 Cloud Storage 值區也必須位於華沙區域，或是包含華沙的任何 Cloud Storage 雙重區域。如果您的 BigQuery 資料集位於`US`多區域`us-central1`，則 Cloud Storage 值區可以位於愛荷華州 (`us-central1`) 單一區域，或任何包含愛荷華州的雙區域。即使值區位於資料集多地區內的位置，從任何其他單一地區發出的查詢仍會產生資料移轉費用。舉例來說，如果外部資料表位於 `US` 多區域，而 Cloud Storage bucket 位於奧勒岡 (`us-west1`)，則這項工作會產生資料移轉費用。

  如果您的 BigQuery 資料集位於`EU`多區域，則 Cloud Storage bucket 可以位於荷蘭 (`europe-west4`) 單一區域，或任何包含荷蘭 (`europe-west4`) 的雙重區域。即使 bucket 位於資料集多區域內的位置，從任何其他單一區域發出的查詢仍會產生資料移轉費用。舉例來說，如果外部資料表位於 `EU` 多區域，而 Cloud Storage 值區位於華沙 (`europe-central2`)，則這項工作會產生資料移轉費用。
* [雙地區值區](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#location-dr)：如果您的 BigQuery 資料集位於東京 (`asia-northeast1`) 地區，對應的 Cloud Storage 值區必須位於東京地區，或位於包含東京的雙地區，例如 `ASIA1` 雙地區。

  如果 Cloud Storage 值區位於`NAM4`雙區域，或任何包含愛荷華州(`us-central1`) 區域的雙區域，對應的 BigQuery 資料集可以位於`US`多區域或愛荷華州(`us-central1`)。

  如果 Cloud Storage bucket 位於`EUR4`雙地區，或包含荷蘭 (`europe-west4`) 地區的任何雙地區，對應的 BigQuery 資料集可以位於`EU`多地區或荷蘭 (`europe-west4`)。
* [多區域 bucket](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#location-mr)：不建議搭配多區域 Cloud Storage bucket 使用多區域資料集位置，因為外部查詢效能取決於最低延遲和最佳網路頻寬。

  如果 BigQuery 資料集位於`US`多區域，對應的 Cloud Storage bucket 必須位於包含愛荷華州 (`us-central1`) 的雙區域，例如 `NAM4`雙區域，或包含愛荷華州 (`us-central1`) 的自訂雙區域。

  如果 BigQuery 資料集位於`EU`多區域`europe-west4`，對應的 Cloud Storage 值區必須位於包含荷蘭 (`europe-west4`) 的雙重區域，例如`EUR4`雙重區域，或是包含荷蘭 (`europe-west4`) 的自訂雙重區域。

如要進一步瞭解支援的 Cloud Storage 位置，請參閱 Cloud Storage 說明文件中的[值區位置](https://docs.cloud.google.com/storage/docs/bucket-locations?hl=zh-tw)一文。

#### 將 Cloud Storage 資料載入 BigQuery

從 Cloud Storage 載入資料時，載入的資料必須與 BigQuery 資料集位於相同位置，否則載入工作會產生資料移轉費用。

如要進一步瞭解載入資料移轉費用，請參閱「[查詢 Cloud Storage 資料](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#query-storage-data-location)」一節，因為這兩者適用相同的指引。

詳情請參閱「[批次載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)」。

### Bigtable

從 Bigtable 查詢資料或將資料匯出至 Bigtable 時，請務必考慮位置。

#### 查詢 Bigtable 資料

透過 BigQuery [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)[查詢 Bigtable 中的資料](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-tw)時，Bigtable 執行個體必須與 BigQuery 資料集位於相同位置：

* 單一區域：如果 BigQuery 資料集位於比利時 (`europe-west1`) 區域，對應的 Bigtable 執行個體就必須位於比利時區域。
* 多區域：外部查詢效能取決於最低延遲時間和最佳網路頻寬，因此**不**建議使用多區域資料集位置，查詢 Bigtable 外部資料表。

如要進一步瞭解支援的 Bigtable 位置，請參閱「[Bigtable 位置](https://docs.cloud.google.com/bigtable/docs/locations?hl=zh-tw)」。

#### 將資料匯出至 Bigtable

* 如果 BigQuery 資料集位於多個地區，則必須設定 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)，將資料傳送至該多地區內的 Bigtable 叢集。舉例來說，如果您的 BigQuery 資料集位於 `US` 多區域，Bigtable 集群可以位於美國境內的 `us-west1` (奧勒岡) 區域。
* 如果 BigQuery 資料集位於單一區域，則必須設定 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)，將資料傳送至相同區域的 Bigtable 叢集。舉例來說，如果您的 BigQuery 資料集位於 `asia-northeast1` (東京) 區域，Bigtable 叢集也必須位於 `asia-northeast1` (東京) 區域。

### Google 雲端硬碟

上述的位置注意事項並不適用於 [Google 雲端硬碟](https://docs.cloud.google.com/bigquery/external-data-drive?hl=zh-tw)外部資料來源。

### Cloud SQL

透過 BigQuery [聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)[查詢 Cloud SQL 中的資料](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-tw)時，Cloud SQL 執行個體必須與 BigQuery 資料集位於相同位置。

* 單一區域：如果 BigQuery 資料集位於比利時 (`europe-west1`) 區域位置，對應的 Cloud SQL 執行個體就必須位於比利時區域。
* 多地區：如果 BigQuery 資料集位於 `US` 多地區，對應的 Cloud SQL 執行個體必須位於美國地理區域的單一地區。

如要進一步瞭解支援的 Cloud SQL 位置，請參閱「[Cloud SQL 位置](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_regions)」。

### Spanner

透過 BigQuery [聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)[查詢 Spanner 中的資料](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw)時，Spanner 執行個體必須與 BigQuery 資料集位於相同位置。

* 單一區域：如果 BigQuery 資料集位於比利時 (`europe-west1`) 區域位置，對應的 Spanner 執行個體必須位於比利時區域。
* 多區域：如果 BigQuery 資料集位於 `US` 多區域，對應的 Spanner 執行個體必須位於美國地理區域的單一區域。

如要進一步瞭解支援的 Spanner 位置，請參閱「[Spanner 位置](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_regions)」。

### 分析工具

將 BigQuery 資料集與[分析工具](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)放在同一位置：

* [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc/docs/concepts/overview?hl=zh-tw)：使用 [BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/bigquery?hl=zh-tw)查詢 BigQuery 資料集時，BigQuery 資料集應與 Managed Service for Apache Spark 叢集位於同一位置。
所有 [Compute Engine 位置](https://docs.cloud.google.com/compute/docs/regions-zones?hl=zh-tw#available)都支援 Managed Service for Apache Spark。* [Vertex AI Workbench](https://docs.cloud.google.com/vertex-ai/docs/workbench/introduction?hl=zh-tw)：在 Vertex AI Workbench 中使用 [Jupyter 筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw#jupyter_notebooks)查詢 BigQuery 資料集時，BigQuery 資料集應與 Vertex AI Workbench 執行個體位於同一位置。
查看[支援的 Vertex AI Workbench 位置](https://docs.cloud.google.com/vertex-ai/docs/general/locations?hl=zh-tw#vertex-ai-workbench-locations)。

### 資料管理計畫

擬定資料管理方案：

* 如果您選擇的是地區儲存資源，例如 BigQuery 資料集或 Cloud Storage 值區，則請擬定[資料異地備援管理](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw#geographic_management_of_data)方案。

## 限制地點

您可以使用[機構政策服務](https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview?hl=zh-tw)，限制可建立資料集的位置。詳情請參閱「[限制資源位置](https://docs.cloud.google.com/resource-manager/docs/organization-policy/defining-locations?hl=zh-tw)」和「[支援資源位置的服務](https://docs.cloud.google.com/resource-manager/docs/organization-policy/defining-locations-supported-services?hl=zh-tw#bigquery)」。

## 資料集安全性

如要在 BigQuery 中控管資料集存取權，請參閱「[控管資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。如要瞭解資料加密，請參閱「[靜態資料加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。
* 瞭解如何[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)。
* 瞭解 BigQuery 的[計價方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。
* 瞭解[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)。
* [查看我們在世界各地提供的所有 Google Cloud 服務](https://docs.cloud.google.com/about/locations?hl=zh-tw#region)。
* [探索其他位置概念](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw)，例如區域，這些概念適用於其他 Google Cloud 服務。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]