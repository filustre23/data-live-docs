* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 已獲授權的資料集

本文說明如何在 BigQuery 中使用*授權資料集*。授權資料集可讓您授權指定資料集中的所有檢視表，存取第二個資料集中的資料。使用授權資料集時，您不需要設定個別[授權檢視畫面](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。

## 總覽

BigQuery 中的[檢視區塊](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)是由 SQL 查詢定義的虛擬資料表。舉例來說，檢視的查詢可能只會傳回資料表的部分資料欄，排除含有個人識別資訊 (PII) 的資料欄。如要查詢檢視區塊，使用者必須有權存取檢視區塊查詢所存取的資源。

### 授權檢視表

如要讓使用者查詢檢視區塊，但不想授予他們檢視區塊所參照資源的直接存取權，可以使用[*已授權檢視區塊*](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。建立授權檢視區時，您可以共用邏輯檢視區或具體化檢視區。授權具體化檢視表後，該檢視表即為「授權具體化檢視表」。

舉例來說，授權檢視表可讓您與特定群組或使用者 (主體) 分享檢視表中的部分資料，而不必授予主體所有基礎資料的存取權。主體可以查看您分享的資料並對其執行查詢，但無法直接存取來源資料集。而是授權檢視表存取來源資料。

### 已獲授權的資料集

如要授予*檢視表集合*資料集存取權，不必逐一授權每個檢視表，可以將檢視表歸入同一個資料集，然後授予包含檢視表的資料集存取包含資料的資料集。然後視需要授予主體存取資料集 (含檢視群組) 或資料集中個別檢視區塊的權限。

可存取其他資料集的資料集稱為「授權資料集」。
授權其他資料集存取資料的資料集稱為「共用資料集」。

**注意：** 由於授權資料集中的所有現有和未來檢視區塊，都能存取共用資料集中的資料表，因此除了在標準資料集中建立或更新檢視區塊所需的權限外，BigQuery 還要求您具備其他權限，才能在授權資料集中建立或更新檢視區塊。詳情請參閱「[在授權資料集中建立或更新檢視區塊](#create_or_update_view)」。

## 所需權限和角色

如要授權或撤銷資料集的授權，您必須具備下列[身分與存取權管理 (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，才能更新要分享的資料集存取控管清單。

| **權限** | **資源** |
| --- | --- |
| `bigquery.datasets.get` | 您要分享的資料集。 |
| `bigquery.datasets.update` | 您要分享的資料集。 |

下列預先定義的 [IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)提供必要權限。

| **角色** | **說明** |
| --- | --- |
| `bigquery.dataOwner` | BigQuery 資料擁有者 |
| `bigquery.admin` | BigQuery 管理員 |

授權資料集後，您可以在授權資料集中建立或更新檢視表。如要瞭解詳情和必要權限，請參閱「[在授權資料集中建立或更新檢視區塊](#create_or_update_view)」。

## 配額與限制

已授權的資料集會受到資料集限制。詳情請參閱「[資料集限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#dataset_limits)」。

資料集的存取控制清單最多可有 2,500 個授權資源，包括[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)、[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)和[授權函式](https://docs.cloud.google.com/bigquery/docs/authorized-functions?hl=zh-tw)。
如果授權檢視區塊數量過多而超出上限，建議將檢視區塊分組到授權資料集中。設計新的 BigQuery 架構 (尤其是多租戶架構) 時，建議將相關檢視區塊分組到授權資料集中。

## 授權資料集

如要授權資料集的現有和未來檢視區塊存取其他資料集，請將要授權的資料集新增至要共用資料集的存取清單，方法如下：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
4. 在隨即顯示的詳細資料窗格中，按一下「共用」，然後選取「授權資料集」選項。
5. 在隨即顯示的「Authorized dataset」(授權資料集) 窗格中，以以下格式輸入要授權的資料集「Dataset ID」(資料集 ID)：

   `PROJECT.AUTHORIZED_DATASET`

   例如：

   `myProject.myDataset`
6. 按一下「新增授權」，然後按一下「關閉」。

### bq

1. 開啟 Cloud Shell：

   [前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)
2. 使用 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令，將要共用資料集的現有中繼資料 (包括存取權控管清單) 寫入 JSON 檔案。

   ```
   bq show --format=prettyjson PROJECT:SHARED_DATASET > FILE_PATH
   ```
3. 使用文字編輯器，將要授權的資料集新增至 FILE\_PATH 建立的 JSON 檔案現有 `access` 區段。

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
5. 如要確認已新增授權的資料集，請再次輸入 `bq show` 指令。例如：

   ```
   bq show --format=prettyjson PROJECT:SHARED_DATASET
   ```

### API

1. 呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法，取得要共用資料集的目前中繼資料，如下所示：

   ```
   GET https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT/datasets/SHARED_DATASET
   ```

   回應主體會傳回 [`Dataset`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw#Dataset) 資源，其中包含資料集的 JSON 中繼資料。
2. 將要授權的資料集新增至 `Dataset` 資源傳回的 JSON 中繼資料 `access` 區段，如下所示：

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
3. 使用 [`datasets.update`](https://docs.cloud.google.com/bigquery/docs/reference/v2/datasets/update?hl=zh-tw) 方法，透過新增的授權更新資料集：

   ```
   PUT https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT/datasets/SHARED_DATASET
   ```

   在要求主體中加入更新的 `Dataset` 資源。
4. 您可以再次呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法，確認已新增授權資料集。

## 撤銷資料集的授權

刪除有權存取其他來源資料集的資料集後，來源資料集的[存取控制清單 (ACL)](https://docs.cloud.google.com/storage/docs/access-control/lists?hl=zh-tw) 最多可能需要 24 小時，才能完全反映這項變更。在這段期間：

* 您將無法透過已刪除的資料集存取來源資料。
* 刪除的資料集可能仍會顯示在來源資料集的 ACL 中，並計入任何授權資料集限制。在 ACL 更新前，您可能無法建立新的授權資料集。

如要撤銷授權資料集中檢視表的存取權，請從共用資料集的存取清單中移除授權資料集，方法如下：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
4. 在隨即顯示的詳細資料窗格中，按一下「共用」，然後選取「授權資料集」選項。
5. 在隨即顯示的「授權資料集」窗格中，找出「目前已授權的資料集」部分中授權資料集的項目。
6. 在要移除的授權資料集旁，按一下刪除圖示，然後按一下「關閉」。

### bq

1. 開啟 Cloud Shell：

   [前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)
2. 使用 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令，將共用資料集的現有中繼資料 (包括存取權控管清單) 寫入 JSON 檔案。

   ```
   bq show --format=prettyjson PROJECT:SHARED_DATASET > FILE_PATH
   ```
3. 使用文字編輯器，從 `access`
   部分移除授權資料集，該部分是在 FILE\_PATH 建立的 JSON 檔案中，如下所示：

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
5. 如要確認授權資料集已移除，請再次輸入 `bq show` 指令。
   例如：

   ```
   bq show --format=prettyjson PROJECT:SHARED_DATASET
   ```

### API

1. 呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法，取得共用資料集的目前中繼資料，如下所示：

   ```
   GET https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT/datasets/SHARED_DATASET
   ```

   回應主體會傳回 [`Dataset`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw#Dataset) 資源，其中包含資料集的 JSON 中繼資料。
2. 從 `Dataset` 資源傳回的 JSON `access` 區段中，移除已授權的資料集，例如：

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

   在要求主體中加入更新的 `Dataset` 資源。
4. 您可以再次呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法，確認授權資料集已移除。

## 在授權資料集中建立或更新檢視表

如要建立或更新授權資料集中的檢視表，除了[建立](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw#required_permissions)或[更新](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw#update_a_view)標準資料集檢視表所需的權限外，您還必須具備「[必要權限和角色](#permissions_datasets)」中列出的共用資料集權限。

下表摘要說明建立或更新授權資料集中的檢視區塊時，所需的[Identity and Access Management (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)：

| **權限** | **資源** |
| --- | --- |
| `bigquery.datasets.get` | 您要分享的資料集。 |
| `bigquery.tables.getData` | 您要建立或更新的新檢視表所參照的共用資料集中的任何資料表或檢視表。 |
| `bigquery.tables.create` | 您要在其中建立檢視區塊的授權資料集。 |
| `bigquery.tables.update` | 您要更新檢視表的授權資料集。 |

如要從授權資料集中[刪除檢視區塊](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw#delete_views)，您不需要任何額外權限。

**注意：** 如要在授權資料集中建立或更新檢視區塊，您不需要具備共用資料集 (或任何其他參照資料集) 的 `bigquery.datasets.update` 權限。這項權限僅供管理資料集的授權清單，包括：

* 授權資料集：一開始授予資料集共用資料集的存取權。
* 管理個別授權檢視表：從共用資料集的授權清單中新增或移除特定檢視表。

  詳情請參閱「[必要的角色](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw#required_permissions)」。

**注意：** 管理檢視區塊的陳述式 (例如 `ALTER VIEW`) 可同時套用至一般檢視區塊和授權檢視區塊。執行這些陳述式時，請確認您管理的是正確的檢視畫面。

## 查詢授權資料集中的檢視表

如要查詢授權資料集中的檢視表，使用者必須具備檢視表的存取權，但不需具備共用資料集的存取權。

詳情請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

## 已授權的資料集範例

以下範例說明如何建立及使用授權資料集。

假設您有兩個資料集，分別命名為 `private_dataset` 和 `public_dataset`。
`private_dataset` 資料集包含名為 `private_table` 的資料表。`public_dataset` 資料集包含名為 `private_table_filtered` 的檢視區塊。`private_table_filtered` 檢視區塊是以查詢為基礎，該查詢會傳回 `private_table` 資料表中的部分欄位，但不是全部。

您可以授予使用者權限，存取 `private_table_filtered` 檢視表傳回的資料，但無法存取 `private_table` 資料表中的所有資料，如下所示：

1. 將 `bigquery.dataViewer` 角色授予使用者，讓他們存取 `public_dataset` 資料集。這個角色包含 `bigquery.tables.getData` 權限，可讓使用者查詢 `public_dataset` 資料集中的檢視區塊。如要瞭解如何授予使用者資料集角色，請參閱[控管資料集存取權](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-tw)。

   使用者現在有權查詢 `public_dataset` 中的檢視區塊，但仍無法存取 `private_dataset` 中的 `private_table` 資料表。如果使用者嘗試直接查詢 `private_table` 資料表，或嘗試透過查詢 `private_table_filtered` 檢視表間接存取 `private_table` 資料表，會收到類似以下的錯誤訊息：

   `Access Denied: Table PROJECT:private_dataset.private_table:
   User does not have permission to query table
   PROJECT:private_dataset.private_table.`
2. 在 Google Cloud 控制台的「BigQuery」頁面中，開啟 `private_dataset` 資料集，按一下「共用」，然後選取「授權資料集」。
3. 在隨即顯示的「Authorized dataset」(已授權資料集) 窗格中，於「Dataset ID」(資料集 ID) 欄位輸入 `PROJECT.public_dataset`，然後按一下「Add Authorization」(新增授權)。

   `public_dataset` 資料集會新增至 `private_dataset` 資料集的存取控制清單，授權 `public_dataset` 資料集中的檢視表查詢 `private_dataset` 資料集中的資料。

   使用者現在可以查詢 `public_dataset` 資料集中的 `private_table_filtered` 檢視區塊，間接存取 `private_dataset` 資料集，但無權直接存取 `private_dataset` 資料集中的資料。

## 限制

* 您可以在不同區域建立授權資料集，但 BigQuery 不支援跨區域查詢。因此，建議您在相同區域中建立資料集。

## 後續步驟

* 如要瞭解如何授權個別檢視表存取資料集中的資料，請參閱「[已授權的檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。
* 如要瞭解如何授權表格函式或使用者定義函式存取資料集中的資料，請參閱「[已授權函式](https://docs.cloud.google.com/bigquery/docs/authorized-functions?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]