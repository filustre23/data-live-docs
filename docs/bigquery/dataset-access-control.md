Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料集層級存取控管異動

如果選擇對資料集層級的存取控管機制強制執行 `enable_fine_grained_dataset_acls_option` 設定，則必須具備 `bigquery.datasets.getIamPolicy` Identity and Access Management (IAM) 權限，才能查看資料集的存取控管機制，以及查詢[`INFORMATION_SCHEMA.OBJECT_PRIVILEGES`](https://docs.cloud.google.com/bigquery/docs/information-schema-object-privileges?hl=zh-tw)檢視畫面。您必須具備 `bigquery.datasets.setIamPolicy` 權限，才能更新資料集的存取控管機制，或[使用 API 建立具有存取控管機制的資料集](#changes_to_api_methods)。

如果未選擇加入，資料集層級的存取權控管機制不會變更。

## 啟用違規處置

您可以選擇強制執行權限變更。選擇加入後，您必須具備 `bigquery.datasets.getIamPolicy` 權限才能取得資料集的存取控管，並具備 `bigquery.datasets.setIamPolicy` 權限才能更新資料集的存取控管，或使用 API 建立含有存取控管的資料集。

如要選擇強制執行，請在機構或專案層級將 `enable_fine_grained_dataset_acls_option` 設定設為 `TRUE`。如要在選擇加入後選擇退出，請在組織或專案層級將 `enable_fine_grained_dataset_acls_option` 設定設為 `FALSE`。如要瞭解如何啟用設定，請參閱「[管理設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)」。

### 設定範例

下列範例說明如何設定及移除 `enable_fine_grained_dataset_acls_option` 設定。

#### 調整組織設定

如要調整組織設定，請使用 [`ALTER ORGANIZATION SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_organization_set_options_statement)。以下範例會在機構層級將 `enable_fine_grained_dataset_acls_option` 設為 `TRUE`：

```
ALTER ORGANIZATION
SET OPTIONS (
  `region-REGION.enable_fine_grained_dataset_acls_option` = TRUE);
```

將 REGION 替換為與組織相關聯的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)，例如 `us` 或 `europe-west6`。

以下範例會清除機構層級的`enable_fine_grained_dataset_acls_option`設定：

```
ALTER ORGANIZATION
SET OPTIONS (
  `region-REGION.enable_fine_grained_dataset_acls_option` = FALSE);
```

#### 配置專案設定

如要調整專案設定，請使用 [`ALTER PROJECT SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_project_set_options_statement)。`ALTER PROJECT SET OPTIONS` DDL 陳述式可接受 `project_id` 變數。如未指定 `project_id`，系統會預設為查詢執行的目前專案。

以下範例將 `enable_fine_grained_dataset_acls_option` 設為 `TRUE`。

```
ALTER PROJECT PROJECT_ID
SET OPTIONS (
  `region-REGION.enable_fine_grained_dataset_acls_option` = TRUE);
```

將 PROJECT\_ID 替換為專案 ID。

以下範例會清除專案層級 `enable_fine_grained_dataset_acls_option` 設定：

```
ALTER PROJECT PROJECT_ID
SET OPTIONS (
  `region-REGION.enable_fine_grained_dataset_acls_option` = FALSE);
```

## 自訂角色異動

如果選擇強制執行權限變更，則授予 `bigquery.datasets.get`、`bigquery.datasets.create` 或 `bigquery.datasets.update` 權限，但未授予 `bigquery.datasets.getIamPolicy` 或 `bigquery.datasets.setIamPolicy` 權限的任何自訂角色都會受到影響。

如果自訂角色只包含 `bigquery.datasets.get`、`bigquery.datasets.update` 或 `bigquery.datasets.create` 權限，則必須更新為包含 `bigquery.datasets.getIamPolicy` 或 `bigquery.datasets.setIamPolicy` 權限，才能維持自訂角色的現有功能。如果自訂角色只需要查看或更新資料集的中繼資料，請使用新的 `dataset_view` 和 `update_mode` 參數。

標準 BigQuery 預先定義的使用者角色不受這項異動影響。具體來說，`roles/bigquery.admin`、`roles/bigquery.dataOwner`、`roles/bigquery.dataEditor`、`roles/bigquery.dataViewer`、`roles/bigquery.metadataViewer`、`roles/bigquery.user`、`roles/bigquery.studioAdmin` 和 `roles/bigquery.securityAdmin` 已授予對應的 `bigquery.datasets.getIamPolicy` 或 `bigquery.datasets.setIamPolicy` 權限。不過，其他只需要資料集中繼資料存取權的預先定義角色，不包含 `bigquery.datasets.getIamPolicy` 或 `bigquery.datasets.setIamPolicy` 權限。這些角色包括[授權常式角色](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)、其他服務的中繼資料角色，以及部分[服務代理角色](https://docs.cloud.google.com/iam/docs/service-agents?hl=zh-tw)。

## bq 指令列工具指令異動

選擇提早實施後，下列 bq 工具指令會受到影響。

### bq show

您可以使用 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令搭配下列旗標：

**`--dataset_view={METADATA|ACL|FULL}`**
:   指定查看資料集的存取控管或中繼資料時，如何套用權限。請使用下列其中一個值：

    * `METADATA`：僅供檢視資料集的中繼資料。必須具備「`bigquery.datasets.get`」權限，才能使用這個值。
    * `ACL`：僅供檢視資料集的存取控管機制。必須具備「`bigquery.datasets.getIamPolicy`」權限，才能使用這個值。
    * `FULL`：查看資料集的中繼資料和存取控管。這個值需要 `bigquery.datasets.get` 權限和 `bigquery.datasets.getIamPolicy` 權限。

### bq update

您可以搭配下列旗標使用 [`bq update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令：

**`--update_mode={UPDATE_METADATA|UPDATE_ACL|UPDATE_FULL}`**
:   指定更新資料集的存取控管或中繼資料時，如何套用權限。請使用下列其中一個值：

    * `UPDATE_METADATA`：僅更新資料集的中繼資料。必須具備 `bigquery.datasets.update` 權限，才能使用這個值。
    * `UPDATE_ACL`：僅更新資料集的存取控管機制。這個值需要 `bigquery.datasets.setIamPolicy` 權限。
    * `UPDATE_FULL`：同時更新資料集的中繼資料和存取控管。這個值需要 `bigquery.datasets.update` 權限和 `bigquery.datasets.setIamPolicy` 權限。

## 資料控制語言 (DCL) 陳述式的變更

如果選擇提早實施，您必須具備下列權限，才能使用[資料控制語言 (DCL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw) 對資料集執行 `GRANT` 和 `REVOKE` 陳述式：

* `bigquery.datasets.setIamPolicy`

## `INFORMATION_SCHEMA` 檢視查詢異動

如果選擇提早實施，則必須具備 `bigquery.datasets.getIamPolicy` 權限，才能查詢 [`INFORMATION_SCHEMA.OBJECT_PRIVILEGES`](https://docs.cloud.google.com/bigquery/docs/information-schema-object-privileges?hl=zh-tw) 檢視表。

## API 方法異動

選擇提早實施後，下列 REST v2 API 資料集方法會受到影響。

### datasets.get 方法

[`datasets.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw)有一個名為 `dataset_view` 的額外[查詢參數](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw#query-parameters)。

這個參數可讓您進一步控管 `datasets.get` 方法傳回的資訊。`dataset_view` 參數可讓您指定只傳回中繼資料、只傳回存取控管，或兩者都傳回，而非一律傳回存取控管和中繼資料。

[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)中的 `access` 欄位包含資料集的存取控管。其他欄位 (例如 `friendlyName`、`description` 和 `labels`) 代表資料集的中繼資料。

下表列出 `dataset_view` 參數支援的不同值，以及各值所需權限和 API 回應：

| 參數值 | 必要權限 | API 回應 |
| --- | --- | --- |
| `DATASET_VIEW_UNSPECIFIED` (或空白) | * `bigquery.datasets.get` * `bigquery.datasets.getIamPolicy` | 預設值。傳回資料集的中繼資料和存取控管機制。 |
| `METADATA` | * `bigquery.datasets.get` | 傳回資料集的中繼資料。 |
| `ACL` | * `bigquery.datasets.getIamPolicy` | 傳回資料集的存取控管、必要欄位，以及資料集資源中僅供輸出的欄位。 |
| `FULL` | * `bigquery.datasets.get` * `bigquery.datasets.getIamPolicy` | 傳回資料集的 metadata 和存取權控管。 |

如果您未選擇提早強制執行，或選擇提早強制執行後又退出，則可以使用 `dataset_view` 參數，並搭配 `METADATA` 或 `ACL` 值。`FULL` 和 `DATASET_VIEW_UNSPECIFIED` (或空白) 值預設為先前的行為；`bigquery.datasets.get` 權限可讓您取得中繼資料和存取權控管。

#### 範例

下列範例會傳送 `GET` 要求，並將 `dataset_view` 參數設為 `METADATA`：

```
GET https://bigquery.googleapis.com/bigquery/v2/projects/YOUR_PROJECT/datasets/YOUR_DATASET?datasetView=METADATA&key=YOUR_API_KEY HTTP/1.1
```

更改下列內容：

* YOUR\_PROJECT：換成您的專案名稱
* YOUR\_DATASET：資料集名稱
* YOUR\_API\_KEY：您的 API 金鑰

### datasets.update 方法

[`datasets.update` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/update?hl=zh-tw)有一個名為 `update_mode` 的額外[查詢參數](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/update?hl=zh-tw#query-parameters)。

這個參數可讓您進一步控管 `datasets.update` 方法更新的欄位。`update_mode` 參數可讓您指定是否只更新中繼資料、只更新存取控管機制，或兩者都更新，而非一律允許更新存取控管機制和中繼資料。

[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)中的 `access` 欄位包含資料集的存取控管機制。其他欄位 (例如 `friendlyName`、`description` 和 `labels`) 則代表資料集的中繼資料。

下表列出 `update_mode` 參數支援的不同值，以及各值所需權限和 API 回應：

| 參數值 | 必要權限 | API 回應 |
| --- | --- | --- |
| `UPDATE_MODE_UNSPECIFIED` (或空白) | * `bigquery.datasets.update` * `bigquery.datasets.setIamPolicy` | 預設值。傳回資料集更新後的中繼資料和存取控管機制。 |
| `UPDATE_METADATA` | * `bigquery.datasets.update` | 傳回資料集的更新中繼資料。 |
| `UPDATE_ACL` | * `bigquery.datasets.update` * `bigquery.datasets.setIamPolicy` | 傳回資料集更新後的存取控管、必要欄位，以及資料集資源中僅供輸出的欄位。 |
| `UPDATE_FULL` | * `bigquery.datasets.update` * `bigquery.datasets.setIamPolicy` | 傳回資料集的更新中繼資料和存取權控管。 |

如果您未選擇提早實施，或選擇加入後又退出，BigQuery 會預設為先前的行為；`bigquery.datasets.update` 權限可讓您更新中繼資料和存取控管。

#### 範例

下列範例會傳送 `PUT` 要求，並將 `update_mode` 參數設為 `METADATA`：

```
PUT https://bigquery.googleapis.com/bigquery/v2/projects/YOUR_PROJECT/datasets/YOUR_DATASET?updateMode=METADATA&key=YOUR_API_KEY HTTP/1.1
```

更改下列內容：

* YOUR\_PROJECT：換成您的專案名稱
* YOUR\_DATASET：資料集名稱
* YOUR\_API\_KEY：API 金鑰名稱

### datasets.patch 方法

[`datasets.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw)有一個名為 `update_mode` 的額外[查詢參數](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw#query-parameters)。

這個參數可讓您進一步控管 `datasets.patch` 方法更新的欄位。`update_mode` 參數可讓您指定是否只更新中繼資料、只更新存取控管機制，或兩者都更新，而非一律允許更新存取控管機制和中繼資料。

[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)中的 `access` 欄位包含資料集的存取控管機制。其他欄位 (例如 `friendlyName`、`description` 和 `labels`) 代表資料集的中繼資料。

下表列出 `update_mode` 參數支援的不同值，以及各值所需權限和 API 回應：

| 參數值 | 必要權限 | API 回應 |
| --- | --- | --- |
| `UPDATE_MODE_UNSPECIFIED` (或空白) | * `bigquery.datasets.update` * `bigquery.datasets.setIamPolicy` | 預設值。傳回資料集更新後的中繼資料和存取控管機制。 |
| `UPDATE_METADATA` | * `bigquery.datasets.update` | 傳回資料集的更新中繼資料。 |
| `UPDATE_ACL` | * `bigquery.datasets.setIamPolicy` | 傳回資料集更新後的存取控管、必要欄位，以及資料集資源中僅供輸出的欄位。 |
| `UPDATE_FULL` | * `bigquery.datasets.update` * `bigquery.datasets.setIamPolicy` | 傳回資料集的更新中繼資料和存取權控管。 |

如果您未選擇提早實施，或選擇加入後又退出，BigQuery 會預設為先前的行為；`bigquery.datasets.update` 權限可讓您更新中繼資料和存取控管。

#### 範例

下列範例會傳送 `PUT` 要求，並將 `update_mode` 參數設為 `METADATA`：

```
PUT https://bigquery.googleapis.com/bigquery/v2/projects/YOUR_PROJECT/datasets/YOUR_DATASET?updateMode=METADATA&key=YOUR_API_KEY HTTP/1.1
```

更改下列內容：

* YOUR\_PROJECT：換成您的專案名稱
* YOUR\_DATASET：資料集名稱
* YOUR\_API\_KEY：您的 API 金鑰名稱

### datasets.insert 方法

如果您選擇提早實施，並使用 [`datasets.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw)建立具有存取控管機制的資料集，BigQuery 會驗證使用者是否具備 `bigquery.datasets.create` 和 `bigquery.datasets.setIamPolicy` 權限。

如果您使用 API 建立沒有存取控管機制的資料集，則只需要 `bigquery.datasets.create` 權限。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]