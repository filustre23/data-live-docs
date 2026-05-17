Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 已儲存的查詢簡介

本文將簡介 BigQuery 中的已儲存查詢。您可以使用已儲存的查詢建立及管理 SQL 指令碼，系統會自動儲存已儲存查詢的變更，因此關閉查詢編輯器時，不會遺失工作內容。儲存的查詢提供下列選項，可提升協作效率及查詢管理成效：

* 使用 Identity and Access Management (IAM)，與特定使用者和群組[共用已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#share-saved-query)。
* 查看查詢版本記錄。
* 還原或從先前的查詢版本建立分支。

儲存的查詢是 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 支援的 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 程式碼資產。[筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)也是程式碼資產。所有程式碼資產都會儲存在預設[區域](#supported_regions)。更新預設區域後，該區域會套用至之後建立的所有程式碼資產。

儲存查詢功能僅適用於 Google Cloud 控制台。

### 已儲存查詢的安全性

您可以使用 Identity and Access Management (IAM) 角色，控管已儲存查詢的存取權。詳情請參閱[共用已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#share-saved-query)。

### 支援的地區

您可以在 BigQuery Studio 中儲存、共用及管理已儲存的查詢。下表列出 BigQuery Studio 適用的區域：

|  | 地區說明 | 地區名稱 | 詳細資料 |
| --- | --- | --- | --- |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` |  |
| **美洲** | | | |
|  | 哥倫布 | `us-east5` |  |
|  | 達拉斯 | `us-south1` |  |
|  | 愛荷華州 | `us-central1` |  |
|  | 洛杉磯 | `us-west2` |  |
|  | 拉斯維加斯 | `us-west4` |  |
|  | 蒙特婁 | `northamerica-northeast1` |  |
|  | 北維吉尼亞州 | `us-east4` |  |
|  | 奧勒岡州 | `us-west1` |  |
|  | 聖保羅 | `southamerica-east1` | [低 CO2](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) 區域 |
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
|  | 比利時 | `europe-west1` | [低 CO2](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) 區域 |
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` | [低 CO2](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) 區域 |
|  | 馬德里 | `europe-southwest1` | [低 CO2](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) 區域 |
|  | 荷蘭 | `europe-west4` | [低 CO2](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) 區域 |
|  | 杜林 | `europe-west12` |  |
|  | 蘇黎世 | `europe-west6` | [低 CO2](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) 區域 |
| **中東地區** | | | |
|  | 杜哈 | `me-central1` |  |
|  | 達曼 | `me-central2` |  |

### 配額與限制

詳情請參閱「[已儲存查詢的配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#saved_query_limits)」。

### 限制

已儲存的查詢有以下限制：

* 您只能將[已儲存查詢的公開存取權授予](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#grant-public-access)[`allAuthenticatedUsers`](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-authenticated-users) 主體。您無法將已儲存查詢的存取權授予 [`allUsers`](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#all-users) 主體。
* 如果 Google Cloud 專案包含超過 2500 個傳統版已儲存查詢，您就無法使用[批次遷移](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#migrate_classic_saved_queries)，將傳統版已儲存查詢遷移至已儲存查詢。

## 傳統版已儲存查詢

**已淘汰：** [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/enable-assets?hl=zh-tw) 中的已儲存查詢，日後將完全取代傳統的已儲存查詢。我們正在審查淘汰時程。
詳情請參閱[傳統版已儲存查詢的淘汰事宜](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#classic-saved-queries-deprecation)。
如要瞭解如何遷移至已儲存的查詢，請參閱「[遷移傳統版已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#migrate_classic_saved_queries)」一節。

傳統版已儲存查詢是較早期的 SQL 查詢儲存及共用方式。
傳統版已儲存查詢會提供查詢文字，且唯一保留的查詢設定是 SQL 版本。這項設定會決定查詢要使用舊版 SQL 還是 GoogleSQL。如要查詢資料，使用者必須能存取已儲存查詢所存取的資料。

您可以在「傳統版 Explorer」窗格的「(傳統版) 查詢」資料夾中查看傳統版已儲存查詢：

****注意：** 如果尚未啟用 BigQuery Studio，傳統儲存的查詢會顯示在「傳統探索器」窗格的「已儲存的查詢」 (NUMBER) 資料夾中，而不是「(傳統) 查詢」資料夾。**

傳統版已儲存查詢可分為 3 種類型：

* **個人**。只有建立者才能查看個人傳統版已儲存查詢。這類檔案會標示 person 圖示。
* **專案層級。**凡是擁有必要[權限](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#required_permissions_for_classic_saved_queries)的主體，都能看到專案層級的儲存查詢。這類檔案會標示 people 圖示。
* **公開。**擁有查詢連結的任何人都可看到公開的傳統版已儲存查詢。這類檔案會標示 share 圖示。

您可以[migrate](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#migrate_classic_saved_queries)傳統版已儲存查詢，改用已儲存查詢，以便運用新功能，也可以[繼續以傳統版已儲存查詢的形式維護這些查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#update_classic_saved_queries)，直到淘汰為止。淘汰時程正在審查中。

傳統的已儲存查詢功能僅適用於Google Cloud 控制台。

## 傳統版已儲存查詢即將淘汰

[BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/enable-assets?hl=zh-tw) 的已儲存查詢功能將取代傳統的已儲存查詢。我們正在審查淘汰時程。
如要在傳統版已儲存查詢淘汰後編輯這類查詢，請先[將傳統版查詢遷移](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#migrate_classic_saved_queries)至 BigQuery Studio 已儲存查詢。

如果使用者 (包括您) 的個人查詢含有不應向專案資料存取者公開的資訊，查詢擁有者必須先刪除查詢或資訊，才能完成遷移作業。

為支援這項轉換，我們在 2024 年 2 月更新了下列 BigQuery IAM 角色：

* [BigQuery 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)
  (`roles/bigquery.admin`) 取得
  [Dataform 管理員](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin)
  (`roles/dataform.admin`) 權限。
* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`) 取得下列權限：

  + `dataform.locations.get`
  + `dataform.locations.list`
  + `dataform.repositories.create`
  + `dataform.repositories.list`
* [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user) (`roles/bigquery.user`) 具有下列權限：

  + `dataform.locations.get`
  + `dataform.locations.list`
  + `dataform.repositories.create`
  + `dataform.repositories.list`

**警告：** 程式碼資產的可見度由專案層級的 Dataform 權限控管。具備 `dataform.repositories.list` 權限的使用者 (這項權限包含在標準 BigQuery 角色中，例如「BigQuery 工作使用者」、「BigQuery Studio 使用者」和「BigQuery 使用者」)，可以在專案的「探索」面板中查看所有程式碼資產，無論這些資產是由他們建立，還是與他們共用。 Google Cloud 如要限制瀏覽權限，可以建立排除 `dataform.repositories.list` 權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。

如要讓沒有 BigQuery 管理員、BigQuery 工作使用者或 BigQuery 使用者角色的使用者使用已儲存的查詢，請在 IAM 中授予他們[必要權限](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#required_permissions)。

[自訂角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#custom)不會自動更新。
如要更新自訂角色並授予[必要權限](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#required_permissions)，請參閱「[編輯現有的自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw#edit-role)」。

## 後續步驟

* 如要瞭解如何建立已儲存的查詢，請參閱[建立已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw)。
* 如要瞭解如何管理已儲存的查詢，請參閱「[管理已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]