Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 已儲存的查詢簡介

您可以使用已儲存的查詢，在 BigQuery 中建立、管理及共用 SQL 指令碼。系統會自動儲存對已儲存的查詢所做的變更，因此關閉查詢編輯器時，不會遺失工作內容。已儲存的查詢功能僅適用於 Google Cloud 控制台。

## 關於已儲存的查詢

已儲存的查詢可透過下列選項，改善協作和查詢管理：

* 使用 Identity and Access Management (IAM) 與特定使用者和群組[共用已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#share-saved-query)。
* 查看查詢版本記錄。
* 還原至先前的查詢版本，或從先前的查詢版本建立分支。

已儲存的查詢是由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 支援的 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 程式碼資產。[Notebook](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw) 也是程式碼資產。所有程式碼資產都會儲存在預設[區域](#supported_regions)。更新預設區域後，之後建立的所有程式碼資產都會變更區域。

## 已儲存的查詢安全性

您可以使用 Identity and Access Management (IAM) 角色控管已儲存的查詢的存取權。詳情請參閱「[共用已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#share-saved-query)」和「[已儲存查詢的安全性考量](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#saved-queries-security)」。

## 支援的地區

所有已儲存的查詢都會儲存在預設[區域](#supported_regions)。更新預設區域後，之後建立的查詢都會變更位置。下表列出 BigQuery Studio 支援的區域：

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

## 配額與限制

詳情請參閱「[已儲存的查詢的配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#saved_query_limits)」。

## 限制

已儲存的查詢有下列限制：

* 您只能將[已儲存的查詢的公開存取權](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#grant-public-access)授予 [`allAuthenticatedUsers`](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 主體。您無法將已儲存的查詢的存取權授予 [`allUsers`](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-users) 主體。
* 如果 Google Cloud 專案包含超過 2,500 項傳統版已儲存的查詢，則無法使用[批次遷移](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#migrate_classic_saved_queries)，將傳統版已儲存的查詢遷移至已儲存的查詢。

## 傳統版已儲存的查詢 (已淘汰)

**已淘汰：** [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/enable-assets?hl=zh-tw) 中的已儲存查詢，日後將全面取代傳統已儲存查詢。我們正在審查淘汰時程。
詳情請參閱「[淘汰傳統版已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#classic-saved-queries-deprecation)」。如要瞭解如何遷移至已儲存的查詢，請參閱「[遷移傳統版已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#migrate_classic_saved_queries)」。

傳統版已儲存查詢完全淘汰後，如要編輯現有查詢，請[遷移至](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#migrate_classic_saved_queries) BigQuery Studio。

傳統版已儲存的查詢是儲存及共用 SQL 的舊方法。與 BigQuery Studio 已儲存的查詢不同，這些查詢只會保留查詢文字和 SQL 版本 (舊版 SQL 或 GoogleSQL)。

在 Google Cloud 控制台中，這些查詢會顯示在「Explorer」窗格的「(Classic) Queries」資料夾中。(如果尚未啟用 BigQuery Studio，則會顯示在「傳統版 Explorer」窗格的「已儲存的查詢 (NUMBER)」資料夾中)。

傳統版已儲存的查詢分為三種：

* **個人** (person)：只有建立者可以查看。

  + 注意：如果個人查詢含有機密資訊，您必須先刪除查詢或移除機密資料，才能進行遷移。
* **專案層級** (people)：任何具備[必要權限](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#required_permissions_for_classic_saved_queries)的主體都能查看。
* **公開** (share)：任何擁有查詢連結的使用者都能查看。

### 遷移和存取權的 IAM 角色

下列預先定義的 BigQuery IAM 角色包含必要的 [Dataform 權限](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin)，可協助您轉換至 BigQuery Studio 已儲存的查詢：

* **[BigQuery 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)** (`roles/bigquery.admin`) 包含 `roles/dataform.admin` 權限。
* **[BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)** (`roles/bigquery.jobUser`) 和 **[BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user)** (`roles/bigquery.user`) 包含：
  + `dataform.locations.get`
  + `dataform.locations.list`
  + `dataform.repositories.create`
  + `dataform.repositories.list`

如果您沒有這些預先定義的角色，請要求[必要權限](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#required_permissions)。[自訂角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#custom)不會自動更新，必須[手動編輯](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw#edit-role)。

## 後續步驟

* 如要瞭解如何建立已儲存的查詢，請參閱「[建立已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw)」。
* 如要瞭解如何管理已儲存的查詢，請參閱「[管理已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]