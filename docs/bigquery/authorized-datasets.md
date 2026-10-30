Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 已獲授權的資料集

在 BigQuery 中，您可以透過*授權資料集*，授權指定資料集中的所有檢視表存取第二個資料集中的資料。有了已授權資料集，您就不必設定個別[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。

## 總覽

BigQuery 中的[檢視表](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)是由 SQL 查詢定義的虛擬資料表。舉例來說，檢視表的查詢可能只會傳回資料表的部分資料欄，不含含有個人識別資訊 (PII) 的資料欄。如要查詢檢視表，使用者必須有權存取檢視表查詢所存取的資源。

### 授權檢視表

如要讓使用者查詢檢視表，但不直接授予檢視表參照資源的存取權，可以使用[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。建立授權 view 時，您可以共用邏輯 view 或 materialized view。授權的 materialized view 稱為「授權 materialized view」。

舉例來說，授權檢視表可讓您與指定群組或使用者 (主體) 共用檢視表中較有限的資料，而不必授予主體所有基礎資料的存取權。主體可以查看您分享的資料並執行查詢，但無法直接存取來源資料集。而是由授權檢視表存取來源資料。

### 已獲授權的資料集

如要將資料集的存取權授予*一組檢視表*，而不必個別授權，可以將檢視表分組到資料集，然後將含有資料的資料集存取權授予含有檢視表的資料集。接著，您可以視需要將資料集與檢視表群組的存取權，或資料集中個別檢視表的存取權，授予主體。

可存取其他資料集的資料集稱為「已授權資料集」。授權其他資料集存取其資料的資料集稱為「共用資料集」。

**注意：** 由於已授權資料集中所有現有和未來的檢視表都能存取共用資料集中的資料表，因此在已授權資料集中建立或更新檢視表時，BigQuery 需要額外權限，而不僅僅是在標準資料集中建立或更新檢視表所需的權限。詳情請參閱「[在授權資料集中建立或更新檢視表](#create_or_update_view)」。

## 所需權限和角色

如要授權資料集或撤銷資料集的授權，您必須具備下列 [Identity and Access Management (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，才能更新共用資料集的存取控管清單。

| **權限** | **資源** |
| --- | --- |
| `bigquery.datasets.get` | 您要共用的資料集。 |
| `bigquery.datasets.update` | 您要共用的資料集。 |

下列預先定義的 [IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)提供必要權限。

| **角色** | **說明** |
| --- | --- |
| `bigquery.dataOwner` | BigQuery 資料擁有者 |
| `bigquery.admin` | BigQuery 管理員 |

資料集獲得授權後，您可以在授權資料集中建立或更新檢視表。如要進一步瞭解相關資訊和必要權限，請參閱「[在授權資料集中建立或更新檢視表](#create_or_update_view)」。

## 配額與限制

已授權的資料集受資料集限制。詳情請參閱「[資料集限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#dataset_limits)」。

資料集的存取控制清單最多可有 2,500 項授權資源，包括[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)、[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)和[授權函式](https://docs.cloud.google.com/bigquery/docs/authorized-functions?hl=zh-tw)。
如果授權檢視表數量過多而超過這項限制，建議您將檢視表分組為授權資料集。
最佳做法是在設計新的 BigQuery 架構 (尤其是多租戶架構) 時，將相關檢視表分組到授權資料集。

## 授權資料集

如要授權資料集目前和未來的檢視表存取其他資料集，請將要授權的資料集新增至要共用的資料集存取清單，如下所示：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
4. 在隨即顯示的詳細資料窗格中，按一下「Sharing」(共用)，然後選取「Authorize Datasets」(授權資料集) 選項。
5. 在顯示的「Authorized dataset」(授權資料集) 窗格中，輸入要授權的資料集「Dataset ID」(資料集 ID)，格式如下：

   `PROJECT.AUTHORIZED_DATASET`

   例如：

   `myProject.myDataset`
6. 依序點選「新增授權」和「關閉」。

### bq

1. 開啟 Cloud Shell：

   [前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)
2. 使用 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令，將要共用的資料集現有中繼資料 (包括存取控制清單) 寫入 JSON 檔案。

   ```
   bq show --format=prettyjson PROJECT:SHARED_DATASET > FILE_PATH
   ```
3. 使用文字編輯器，將要授權的資料集新增至 FILE\_PATH 建立的 JSON 檔案中現有的 `access` 區段。

   例如：

   ```
   "access": [
    ...
    {
      "dataset": {
        "dataset": {
          "project_id": "PROJECT",
          "dataset_id": "AUTHORIZED_DATASET"
        },
        "target_types": "VIEWS"
      }
    }
   ]
   ```
4. 使用 [`bq update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令更新共用資料集。例如：

   ```
   bq update --source FILE_PATH PROJECT:SHARED_DATASET
   ```
5. 如要確認已新增授權資料集，請再次輸入 `bq show` 指令。例如：

   ```
   bq show --format=prettyjson PROJECT:SHARED_DATASET
   ```

### API

1. 呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法，取得要共用的資料集目前中繼資料，如下所示：

   ```
   GET https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT/datasets/SHARED_DATASET
   ```

   回應主體會傳回 [`Dataset`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw#Dataset) 資源，其中包含資料集的 JSON 中繼資料。
2. 將要授權的資料集新增至 `Dataset` 資源中傳回的 JSON 中繼資料 `access` 部分，如下所示：

   ```
   "access": [
    ...
    {
      "dataset": {
        "dataset": {
          "project_id": "PROJECT",
          "dataset_id": "AUTHORIZED_DATASET"
        },
        "target_types": "VIEWS"
      }
    }
   ]
   ```
3. 使用 [`datasets.update`](https://docs.cloud.google.com/bigquery/docs/reference/v2/datasets/update?hl=zh-tw) 方法，以新增的授權更新資料集：

   ```
   PUT https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT/datasets/SHARED_DATASET
   ```

   在要求主體中加入更新後的 `Dataset` 資源。
4. 您可以再次呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法，確認已新增授權資料集。

## 撤銷資料集授權

刪除有權存取其他來源資料集的資料集後，來源資料集的[存取控制清單 (ACL)](https://docs.cloud.google.com/storage/docs/access-control/lists?hl=zh-tw) 最多可能需要 24 小時才會完全反映這項變更。在這段期間：

* 您將無法透過已刪除的資料集存取來源資料。
* 已刪除的資料集可能仍會顯示在來源資料集的 ACL 中，並計入已授權資料集的限制。在 ACL 更新前，您可能無法建立新的授權資料集。

如要撤銷已授權資料集中授予檢視表的存取權，請從共用資料集的存取清單中移除已授權資料集，步驟如下：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
4. 在隨即顯示的詳細資料窗格中，按一下「Sharing」(共用)，然後選取「Authorize Datasets」(授權資料集) 選項。
5. 在顯示的「Authorized dataset」(已授權資料集) 窗格中，找出「Currently authorized datasets」(目前已授權資料集) 部分中的已授權資料集項目。
6. 按一下要移除的授權資料集旁的刪除圖示，然後按一下「Close」(關閉)。

### bq

1. 開啟 Cloud Shell：

   [前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)
2. 使用 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令，將共用資料集的現有中繼資料 (包括存取控制清單) 寫入 JSON 檔案。

   ```
   bq show --format=prettyjson PROJECT:SHARED_DATASET > FILE_PATH
   ```
3. 使用文字編輯器，從 FILE\_PATH 建立的 JSON 檔案 `access` 部分中移除授權資料集，如下所示：

   ```
     {
       "dataset": {
         "dataset": {
           "project_id": "PROJECT",
           "dataset_id": "AUTHORIZED_DATASET"
         },
         "target_types": "VIEWS"
       }
     }
   ```
4. 使用 [`bq update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令更新共用資料集。例如：

   ```
   bq update --source FILE_PATH PROJECT:SHARED_DATASET
   ```
5. 如要確認已移除授權資料集，請再次輸入 `bq show` 指令。例如：

   ```
   bq show --format=prettyjson PROJECT:SHARED_DATASET
   ```

### API

1. 呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法，取得共用資料集目前的中繼資料，如下所示：

   ```
   GET https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT/datasets/SHARED_DATASET
   ```

   回應主體會傳回 [`Dataset`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw#Dataset) 資源，其中包含資料集的 JSON 中繼資料。
2. 從 `Dataset` 資源傳回的 JSON `access` 區段中移除已授權資料集，例如：

   ```
    {
      "dataset": {
        "dataset": {
          "project_id": "PROJECT",
          "dataset_id": "AUTHORIZED_DATASET"
        },
        "target_types": "VIEWS"
      }
    }
   ```
3. 使用 [`datasets.update`](https://docs.cloud.google.com/bigquery/docs/reference/v2/datasets/update?hl=zh-tw) 方法更新資料集，移除授權：

   ```
   PUT https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT/datasets/SHARED_DATASET
   ```

   在要求主體中加入更新後的 `Dataset` 資源。
4. 您可以再次呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法，確認已移除授權資料集。

## 在已授權資料集中建立或更新檢視表

如要建立或更新已授權資料集中的檢視表，除了[建立](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw#required_permissions)或[更新](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw#update_a_view)標準資料集檢視表所需的權限外，您還必須具備「[必要權限和角色](#permissions_datasets)」中列出的共用資料集權限。

下表摘要說明建立或更新授權資料集中的檢視表，所需具備的 [Identity and Access Management (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)：

| **權限** | **資源** |
| --- | --- |
| `bigquery.datasets.get` | 您要共用的資料集。 |
| `bigquery.tables.getData` | 您建立或更新的新檢視表，參照了共用資料集中的任何資料表或檢視表。 |
| `bigquery.tables.create` | 您要在其中建立檢視表的授權資料集。 |
| `bigquery.tables.update` | 要更新檢視表的授權資料集。 |

您不需要任何額外權限，即可從授權資料集[刪除檢視表](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw#delete_views)。

**注意：** 您不需要具備共用資料集 (或任何其他參照資料集) 的 `bigquery.datasets.update` 權限，即可在授權資料集內建立或更新檢視表。這項權限僅限用於管理資料集的授權清單，包括：

* 授權資料集：一開始授予資料集共用資料集的存取權。
* 管理個別授權檢視表：在共用資料集的授權清單中，新增或移除特定檢視表。

  詳情請參閱「[必要的角色](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw#required_permissions)」。

**注意：** 管理檢視表的陳述式 (例如 `ALTER VIEW`) 可套用至一般檢視表和授權檢視表。執行這些陳述式時，請確認您管理的是正確的檢視表。

## 查詢已授權資料集中的檢視表

如要查詢授權資料集中的檢視表，使用者必須具備檢視表的存取權，但不一定要有共用資料集的存取權。

詳情請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

## 已授權資料集範例

以下範例說明如何建立及使用授權資料集。

假設您有兩個資料集，分別名為 `private_dataset` 和 `public_dataset`。`private_dataset` 資料集包含名為 `private_table` 的資料表。`public_dataset` 資料集包含名為 `private_table_filtered` 的檢視表。`private_table_filtered` 檢視表是以查詢為基礎，會傳回 `private_table` 資料表中的部分欄位，但並非全部。

您可以授予使用者 `private_table_filtered` 檢視表傳回的資料存取權，但不能授予 `private_table` 資料表中的所有資料存取權，如下所示：

1. 將 `public_dataset` 資料集的 `bigquery.dataViewer` 角色授予使用者。這個角色具備 `bigquery.tables.getData` 權限，可讓使用者查詢 `public_dataset` 資料集中的檢視表。如要瞭解如何為使用者授予資料集的角色，請參閱「[使用資料集存取控管機制](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#work_with_dataset_access_controls)」。

   使用者現在有權查詢 `public_dataset` 中的檢視表，但仍無法存取 `private_dataset` 中的 `private_table` 資料表。如果使用者嘗試直接查詢 `private_table` 資料表，或嘗試透過查詢 `private_table_filtered` 檢視表間接存取 `private_table` 資料表，就會收到類似下列的錯誤訊息：

   `Access Denied: Table PROJECT:private_dataset.private_table:
   User does not have permission to query table
   PROJECT:private_dataset.private_table.`
2. 在 Google Cloud 控制台的「BigQuery」頁面中，開啟`private_dataset`資料集，按一下「Sharing」(共用)，然後選取「Authorize Datasets」(授權資料集)。
3. 在顯示的「Authorized dataset」(授權資料集) 窗格中，在「Dataset ID」(資料集 ID) 欄位中輸入 `PROJECT.public_dataset`，然後按一下「Add Authorization」(新增授權)。

   `public_dataset` 資料集會新增至 `private_dataset` 資料集的存取控制清單，授權 `public_dataset` 資料集中的檢視表查詢 `private_dataset` 資料集中的資料。

   使用者現在可以查詢 `public_dataset` 資料集中的 `private_table_filtered` 檢視表，間接存取 `private_dataset` 資料集，而不需要任何直接存取 `private_dataset` 資料集中資料的權限。

## 限制

* 您可以在不同區域建立授權資料集，但 BigQuery 不支援跨區域查詢。因此，建議您在相同區域建立資料集。
* 您無法在次要副本中建立授權資料集。詳情請參閱「[資料集複製中的資源行為](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#resource-behavior)」。

## 後續步驟

* 如要瞭解如何授權個別檢視表存取資料集中的資料，請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。
* 如要瞭解如何授權資料表函式或 user-defined function 存取資料集中的資料，請參閱「[授權函式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-28 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-28 (世界標準時間)。"],[],[]]