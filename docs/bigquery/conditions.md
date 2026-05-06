Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 IAM 條件控管存取權

本文說明如何使用 [IAM 條件](https://docs.cloud.google.com/iam/docs/conditions-overview?hl=zh-tw)控管 BigQuery 資源的存取權。

透過 IAM 條件，您可以在符合指定條件時，授予 BigQuery 資源的存取權。舉例來說，您可以授予資源存取權一段時間，或在一天中的特定時段定期授予存取權。您可以在資源的機構、資料夾、專案和資料集層級新增 IAM 條件。子項資源會沿用附帶條件的允許政策。如要進一步瞭解資源層級，請參閱[資源階層](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw#resource-hierarchy)。

IAM 條件可同時授予多個相關資源的身分與存取權管理 (IAM) 權限，包括尚未建立的資源。如要授予不相關的 BigQuery 資源群組權限，請考慮使用 [IAM 標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)。

## 事前準備

1. [授予使用者 IAM 角色](#required_permissions)，其中包含執行本文件各項工作所需的權限。
2. [啟用 IAM API](#enable-api)。

### 必要的角色

如要取得將 IAM Conditions 套用至 BigQuery 資源所需的權限，請要求管理員授予您下列 IAM 角色：

* 專案：
  [專案 IAM 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/resourcemanager?hl=zh-tw#resourcemanager.projectIamAdmin)  (`roles/resourcemanager.projectIamAdmin`)
* 資料集：
  [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備將 IAM 條件套用至 BigQuery 資源所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要將 IAM 條件套用至 BigQuery 資源，您必須具備下列權限：

* 在專案層級設定條件式 IAM 存取權：
   `resourcemanager.projects.setIamPolicy`
* 設定資料集的 IAM 條件式存取權：
  + `bigquery.datasets.setIamPolicy`
  + `bigquery.datasets.update`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如果您打算在整個機構中使用 IAM 條件，也需要[管理機構政策的權限](https://docs.cloud.google.com/resource-manager/docs/organization-policy/using-constraints?hl=zh-tw#required-roles)。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 啟用 IAM API

如要啟用 IAM API，請選取下列其中一個選項：

### 控制台

前往 **Identity and Access Management (IAM) API** 頁面，然後啟用 API。

[啟用 API](https://console.cloud.google.com/apis/library/iam.googleapis.com?hl=zh-tw)

### gcloud

執行 [`gcloud services enable` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable?hl=zh-tw)：

```
gcloud services enable iam.googleapis.com
```

## 查看資料集的條件式存取權政策

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 依序點選 person\_add「共用」>「權限」。
5. 按一下相關聯角色旁的「條件：」**`TITLE`**，即可查看該角色的條件。

### bq

如要在 Cloud Shell 中查看或更新條件式存取政策，必須使用 Cloud Shell 503.0.0 以上版本。

如要取得現有存取權政策，並以 JSON 格式輸出至本機檔案，請在 Cloud Shell 中使用 [`bq show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_get-iam-policy)：

```
bq show --format=prettyjson PROJECT_ID:DATASET > PATH_TO_FILE
```

更改下列內容：

* PROJECT\_ID：專案 ID
* DATASET：資料集名稱
* PATH\_TO\_FILE：本機上 JSON 檔案的路徑

資料集資源 JSON 檔案中的 `access` 屬性包含存取權政策。

### API

如要查看附帶條件的資料集存取權政策，請使用 `accessPolicyVersion=3` 做為要求參數，呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw)。資料集資源中的 `access` 屬性包含存取政策。

## 修改資源的條件存取權

下列各節說明如何為不同資源新增或移除條件式存取權。

### 為機構、資料夾或專案新增條件

如要在 BigQuery 中為機構、資料夾或專案新增條件式存取權，請參閱「[允許使用條件的政策](https://docs.cloud.google.com/iam/docs/conditions-overview?hl=zh-tw#syntax_overview)」。建立條件時，請參閱[屬性格式表](#attribute_formats)。

### 為資料集新增條件式存取權

如要為資料集新增條件，請選取下列其中一種方法。建立條件時，請參考[屬性格式表](#attribute_formats)。

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在詳細資料窗格中，依序點選 person\_add「共用」**>「權限」**。
5. 按一下「新增主體」person\_add。
6. 在「New principals」(新增主體) 欄位中輸入主體。
7. 在「Select a role」(選取角色) 清單中，選取預先定義的角色或自訂角色。
8. 按一下「新增 IAM 條件」。
9. 使用[狀況屬性](#condition_attributes)，在 `condition` 欄位中新增條件。
10. 在「新增 IAM 條件」面板中，按一下「儲存」。
11. 在「授予存取權給『`DATASET`』」面板中，按一下「儲存」。

### bq

如要在 Cloud Shell 中查看或更新條件式存取政策，必須使用 Cloud Shell 503.0.0 以上版本。

如要使用 Cloud Shell 授予資料集的條件式存取權，請按照[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)的指示操作。您可以將條件式存取條件新增至資料集 JSON 檔案的 `access` 區段。

舉例來說，在資料集 JSON 檔案的 `access` 區段中新增下列內容，即可將 `roles/bigquery.dataViewer` 角色授予 `cloudysanfrancisco@gmail.com`，效期至 2032 年 12 月 31 日：

```
"access": [
  {
    "role": "roles/bigquery.dataViewer",
    "userByEmail": "cloudysanfrancisco@gmail.com",
    "condition": {
      "title": "Grant roles/bigquery.dataViewer until 2033",
      "description": "Role expires on December 31, 2032.",
      "expression": "request.time < timestamp('2032-12-31T12:00:00Z')"
    }
  }
]
```

### API

如要使用 BigQuery API 授予資料集的條件式存取權，請按照[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)的指示，在要求參數中加入 `accessPolicyVersion=3`。

您可以將含有存取條件的項目新增至資料集資源的 [`access.condition`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw) 屬性。

對於設有條件式存取政策的資料集，使用者可以透過標準的讀取、修改及更新流程更新無條件存取設定，而不需指定 `accessPolicyVersion` 要求參數。

### 從資料集移除條件式存取權

如要從資料集中移除條件，請選取下列其中一種做法。建立條件時，請參閱[屬性格式表](#attribute_formats)。

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在詳細資料窗格中，依序點選 person\_add「共用」**>「權限」**。
5. 選取要撤銷存取權的主體。
6. 按一下「刪除」圖示 delete。
7. 在「Delete principal?」(要刪除主體嗎？) 對話方塊中，點選「Delete」(刪除)。

### bq

如要在 Cloud Shell 中查看或更新條件式存取政策，必須使用 Cloud Shell 503.0.0 以上版本。

如要使用 Cloud Shell 移除資料集的條件式存取權，請按照「[撤銷資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#revoke_access_to_a_dataset)」一文中的操作說明進行。您可以從資料集 JSON 檔案的 `access` 區段中，移除含有條件的項目。

### API

如要使用 BigQuery API 撤銷資料集的條件式存取權，請按照[撤銷資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#revoke_access_to_a_dataset)的指示，在要求參數中加入 `accessPolicyVersion=3`。

您可以從資料集資源的 `access` 屬性中移除附帶條件的項目。

對於設有條件式存取政策的資料集，使用者可以透過標準的讀取、修改及更新流程更新無條件存取設定，而不需指定 `accessPolicyVersion` 要求參數。

## 條件屬性

您可以根據下列屬性，在 BigQuery 資源上設定 IAM 條件：

* `request.time`：使用者嘗試存取 BigQuery 資源的時間。如需更多詳細資料和範例，請參閱[日期/時間屬性](https://docs.cloud.google.com/iam/docs/conditions-attribute-reference?hl=zh-tw#date-time)。
* `resource.name`：BigQuery 資源的路徑。如需格式，請參閱[屬性格式](#attribute_formats)中的表格。
* `resource.type`：BigQuery 資源的類型。如需格式，請參閱[屬性格式](#attribute_formats)中的表格。
* `resource.service`：BigQuery 資源使用的服務。 Google Cloud 如需格式，請參閱[屬性格式](#attribute_formats)中的表格。
* `resource.tags`：附加至 BigQuery 資源的標記。標記僅支援 BigQuery 資料集、資料表和檢視資源。如需格式，請參閱「[屬性格式](#attribute_formats)」和 [IAM 文件](https://docs.cloud.google.com/iam/docs/conditions-attribute-reference?hl=zh-tw#resource-tags)中的表格。

### 屬性格式

為 BigQuery 資料集建立條件時，請使用下列格式：

| 屬性 | 值 |
| --- | --- |
| `resource.type` | `bigquery.googleapis.com/Dataset` |
| `resource.name` | `projects/PROJECT_ID/datasets/DATASET_ID` |
| `resource.service` | `bigquery.googleapis.com` |
| `resource.tags` | 支援 `hasTagKey`、`hasTagKeyId`、`matchTag` 和 `matchTagId`。詳情請參閱「[資源標記](https://docs.cloud.google.com/iam/docs/conditions-attribute-reference?hl=zh-tw#resource-tags)」。 |

為 BigQuery 資料表和檢視表建立條件時，請使用下列格式：

| 屬性 | 值 |
| --- | --- |
| `resource.type` | `bigquery.googleapis.com/Table` |
| `resource.name` | `projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID` |
| `resource.service` | `bigquery.googleapis.com` |
| `resource.tags` | 支援 `hasTagKey`、`hasTagKeyId`、`matchTag` 和 `matchTagId`。詳情請參閱「[資源標記](https://docs.cloud.google.com/iam/docs/conditions-attribute-reference?hl=zh-tw#resource-tags)」。 |

為 BigQuery 常式建立條件時，請使用下列格式：

| 屬性 | 值 |
| --- | --- |
| `resource.type` | `bigquery.googleapis.com/Routine` |
| `resource.name` | `projects/PROJECT_ID/datasets/DATASET_ID/routines/ROUTINE_ID` |
| `resource.service` | `bigquery.googleapis.com` |

為 BigQuery 模型建立條件時，請使用下列格式：

| 屬性 | 值 |
| --- | --- |
| `resource.type` | `bigquery.googleapis.com/Model` |
| `resource.name` | `projects/PROJECT_ID/datasets/DATASET_ID/models/MODEL_ID` |
| `resource.service` | `bigquery.googleapis.com` |

更改下列內容：

* `PROJECT_ID`：包含您要授予存取權資源的專案 ID
* `DATASET_ID`：您要授予存取權的資料集 ID
* `TABLE_ID`：您要授予存取權的資料表或檢視區塊 ID
* `ROUTINE_ID`：要授予存取權的常式 ID
* `MODEL_ID`：您要授予存取權的模型 ID

## 條件最佳做法

在 BigQuery 中建立條件時，請遵循下列最佳做法：

* 建議您為 `resource.type`、`resource.name` 和 `resource.service` 使用正向條件，以提高準確度。由於不支援的類型會以空字串表示，因此負面條件可能會比對到各種資源。詳情請參閱[負面條件](#negative_conditions)。
* 資料集層級的 IAM 條件僅適用於資料集內的資源 (例如資料表、檢視區塊、模型和常式)。不應使用這些角色授予資料集或專案層級的角色，例如 `bigquery.user` 或 `bigquery.jobUser`。
* 請勿在資料集層級政策中使用條件，因為這不會影響授權。`resource.type == 'bigquery.googleapis.com/Dataset'`這項屬性是用來控管資料表、檢視表、常式和模型等子資料集資源的存取權。
* 即使不需要這麼詳細，也請在條件中加入 `resource.type`、`resource.name` 和 `resource.service`。這樣做有助於在工作流程中的資源變更時維持條件，避免日後無意間納入其他資源。
* 授予權限時，請盡可能只授予最少的權限組合，確保不會不慎授予過於寬鬆的存取權。
* 請謹慎使用 `resource.name.startsWith`。BigQuery 資料表和檢視區塊路徑會以父項專案 ID 和資料集 ID 為前置字元。條件不夠具體可能會授予過多存取權。不過，您可以使用 `resource.name.startsWith` 屬性，讓使用者對資料表執行萬用字元查詢。舉例來說，使用 `resource.name.startsWith("projects/my_project/datasets/my_dataset/tables/table_prefix")` 條件授予的存取權，可讓使用者執行 `SELECT * FROM my_dataset.table_prefix*` 查詢。
* 請勿為資料集、資料表、檢視區塊、常式和模型以外的 BigQuery 資源新增條件。
* 請確認您在正確的資源上授予正確的權限。舉例來說，列出資源的權限 (`bigquery.RESOURCE.list`) 必須在父項層級授予，但刪除資源的權限 (`bigquery.RESOURCE.delete`) 必須在資源層級授予。如要刪除資料集 (也會刪除所有內含資源)，您必須具備資料集的資料表、模型和常式刪除權限。
* 請注意，[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)和[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)不會影響權限。

### 負面情況

`resource.name != resource` 等負面條件可能會無意中授予過於寬鬆的存取權。不支援的 BigQuery 資源會具有空白的資源屬性，也就是符合所有負面條件。BigQuery 以外服務中的資源也可能符合負面條件。

此外，如果使用者使用萬用字元執行查詢，負面條件也會造成問題。舉例來說，請考慮負面條件 `resource.name != /projects/my_project/datasets/my_dataset/tables/secret`。這項條件似乎是授予所有資源的存取權，但名為 `secret` 的資料表除外。不過，使用者仍可使用萬用字元查詢 (例如 `SELECT * from my_project.my_dataset.secre*;`) 查詢該資料表。

此外，資料表、常式和模型的負面條件可能會對父項資料集提供過於寬鬆的存取權。使用者可能因此能夠刪除這些資源，因為刪除權限是在資料集層級管理。

## 限制

* 您無法使用 IAM 條件新增[授權檢視](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)、[授權常式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)或[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)授權。
* 如果查看含有條件的資源時使用不相容的 `accessPolicyVersion`，繫結可能會包含 `withcond`，後面接著雜湊值。詳情請參閱「[排解政策和角色繫結中的 `withcond` 問題](https://docs.cloud.google.com/iam/docs/troubleshooting-withcond?hl=zh-tw)」。
* 如果使用者對資料集或資料表具有條件式存取權，就無法透過 Google Cloud 控制台修改該資源的權限。權限修改作業僅支援透過 bq 工具和 BigQuery API 進行。
* IAM 條件不直接支援資料列層級和資料欄層級存取權控管。不過，具備條件式存取權的使用者可以在資料表上授予自己 BigQuery 管理員角色 (`roles/bigquery.admin`)，然後修改資料列和資料欄存取政策。
* IAM 政策變更最多可能需要五分鐘才會生效。
* 具備條件式存取權的使用者可能無法查詢[`INFORMATION_SCHEMA`檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)。
* 如果使用者僅具備條件式資料表存取權，就無法執行[表格萬用字元函式](https://docs.cloud.google.com/bigquery/docs/reference/legacy-sql?hl=zh-tw#tablewildcardfunctions)。

## 範例

以下是 BigQuery 中 IAM 條件的用途範例。

### 授予特定資料表的讀取權限

這個範例會為 `dataset_1` 資料集中的 `table_1` 資料表授予 `cloudysanfrancisco@gmail.com` BigQuery 資料檢視者角色。具備這個角色的使用者可以查詢資料表，並透過 bq 工具存取資料表。使用者無法在 Google Cloud 控制台中查看資料表，因為他們沒有資料集的 `bigquery.tables.list` 權限。

```
{
  "members": [cloudysanfrancisco@gmail.com],
  "role": roles/bigquery.dataViewer,
  "condition": {
    "title": "Table dataset_1.table_1",
    "description": "Allowed to read table with name table_1 in dataset_1 dataset",
    "expression":
resource.name == projects/project_1/datasets/dataset_1/tables/table_1
&& resource.type == bigquery.googleapis.com/Table
  }
}
```

### 授予特定資料集的清單存取權

這個範例會將 `cloudysanfrancisco@gmail.com` 指派為 `dataset_2` 資料集的 BigQuery 中繼資料檢視者角色。使用者可透過這個角色列出資料集中的所有資源，但無法對這些資源執行任何查詢。

```
{
  "members": [cloudysanfrancisco@gmail.com],
  "role": roles/bigquery.metadataViewer,
  "condition": {
    "title": "Dataset dataset_2",
    "description": "Allowed to list resources in dataset_2 dataset",
    "expression":
resource.name == projects/project_2/datasets/dataset_2
&& resource.type == bigquery.googleapis.com/Dataset
  }
}
```

### 授予特定前置字串的所有資料集內所有資料表的擁有者存取權

這個範例會將 BigQuery 資料擁有者角色授予 `cloudysanfrancisco@gmail.com`，適用於所有資料集中開頭為 `public_` 前置字元的所有資料表：

```
{
  "members": [cloudysanfrancisco@gmail.com],
  "role": roles/bigquery.dataOwner,
  "condition": {
    "title": "Tables public_",
    "description": "Allowed owner access to tables in datasets with public_ prefix",
    "expression":
resource.name.startsWith("projects/project_3/datasets/public_")
&& resource.type == bigquery.googleapis.com/Table
  }
}
```

### 授予特定前置字串的所有資料集內，所有資料表、模型和常式的擁有者存取權

這個範例會將 BigQuery 資料擁有者角色授予 `cloudysanfrancisco@gmail.com`，適用於所有資料集中以 `general_` 前置字元開頭的所有資料表、模型和常式：

```
{
  "members": [cloudysanfrancisco@gmail.com],
  "role": roles/bigquery.dataOwner,
  "condition": {
    "title": "Tables general_",
    "description": "Allowed owner access to tables in datasets with general_ prefix",
    "expression":
resource.name.startsWith("projects/project_4/datasets/general_")
&& resource.type == bigquery.googleapis.com/Table
  }
},
{
  "members": [cloudysanfrancisco@gmail.com],
  "role": roles/bigquery.dataOwner,
  "condition": {
    "title": "Models general_",
    "description": "Allowed owner access to models in datasets with general_ prefix",
    "expression":
resource.name.startsWith("projects/project_4/datasets/general_")
&& resource.type == bigquery.googleapis.com/Model
  }
},
{
  "members": [cloudysanfrancisco@gmail.com],
  "role": roles/bigquery.dataOwner,
  "condition": {
    "title": "Routines general_",
    "description": "Allowed owner access to routines in datasets with general_ prefix",
    "expression":
resource.name.startsWith("projects/project_4/datasets/general_")
&& resource.type == bigquery.googleapis.com/Routine
  }
}
```

## 後續步驟

* 進一步瞭解如何使用 IAM 條件[設定臨時存取權](https://docs.cloud.google.com/iam/docs/configuring-temporary-access?hl=zh-tw)。
* 進一步瞭解如何使用 IAM 條件[設定資源型存取權](https://docs.cloud.google.com/iam/docs/configuring-resource-based-access?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]