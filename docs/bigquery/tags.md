Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用標記控管存取權

本文說明如何搭配 BigQuery 資源使用標記，以控管存取權。

標記是可附加至資源的鍵/值組合。 Google Cloud您可以在 BigQuery 中透過下列方式使用標記：

* **有條件地授予或拒絕政策**：您可以將標記附加至 BigQuery 資料表、檢視區塊和資料集，並使用 [Identity and Access Management (IAM)](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw)，根據這些資源的標記，有條件地授予角色或[拒絕存取](https://docs.cloud.google.com/iam/docs/deny-access?hl=zh-tw) ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。如要進一步瞭解拒絕政策，請參閱「[拒絕政策](https://docs.cloud.google.com/iam/docs/deny-overview?hl=zh-tw)」。
* **資料欄層級存取控管**：您可以將[資料治理標記](#data-governance-tags) (搶先版) 附加至資料表資料欄，並搭配資料政策使用，限制資料欄資料的存取權。

您可以直接將標記附加至資源，也可以從 Google Cloud 資源階層中的上層資源[繼承](https://docs.cloud.google.com/resource-manager/docs/tags/tags-overview?hl=zh-tw#inheritance)標記。

本文著重於搭配 IAM 使用標記，有條件地授予或拒絕 BigQuery 資料表、檢視區塊和資料集的存取權。

如要進一步瞭解如何在資源階層中使用標記，請參閱「[標記總覽](https://docs.cloud.google.com/resource-manager/docs/tags/tags-overview?hl=zh-tw)」。 Google Cloud

如要同時授予多個相關 BigQuery 資源的權限 (包括尚未建立的資源)，請考慮使用 [IAM 條件](https://docs.cloud.google.com/bigquery/docs/conditions?hl=zh-tw)。

## 限制

* BigQuery Omni 資料表、隱藏資料集中的資料表或臨時資料表，都不支援資料表標記。BigQuery Omni 資料集不支援資料集標記。此外，BigQuery Omni 中的跨區域查詢，在檢查其他區域的資料表存取權時，不會使用標記。
* 每個資料表或資料集最多可附加 50 個標記。
* 萬用字元查詢中參照的所有資料表，都必須具有完全相同的標記鍵和值。
* 如果使用者對資料集或資料表具有條件式存取權，就無法透過 Google Cloud 控制台修改該資源的權限。您只能透過 bq 工具和 BigQuery API 修改權限。
* BigQuery 以外的部分服務無法正確驗證 IAM 標記條件。如果標記條件為肯定，也就是說，只有當資源具有特定標記時，使用者才能獲得資源的角色，那麼無論資源附加哪些標記，使用者都會遭到拒絕存取。如果標記條件為負值，表示只有在資源*沒有*特定標記時，使用者才能獲得資源的角色，系統就不會檢查標記條件。

  **最佳做法：**使用正向 IAM 標記條件，而非負向條件，以免不慎授予角色。

## 必要的角色

您必須授予 IAM 角色，讓使用者具備必要[權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)，才能執行本文件中的各項工作。

下列兩個預先定義的 IAM 角色都包含所有必要的 BigQuery 權限：

* BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)
* BigQuery 管理員 (`roles/bigquery.admin`)

新增及移除標記的 Resource Manager 權限包含在[標記使用者角色](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw#required-permissions-attach) (`roles/resourcemanager.tagUser`) 中。

### 所需權限

如要在 BigQuery 中使用標記，您需要下列權限：

| 作業 | BigQuery 介面 (API、CLI、控制台) 和 Terraform | Cloud Resource Manager API 或 gcloud |
| --- | --- | --- |
| 在資料表或檢視表中附加標籤 | * 資料表或檢視表的 `bigquery.tables.createTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.create` 權限 * 建立資料表或檢視表時附加標籤的 `bigquery.tables.create` 權限 * 更新資料表或檢視表時附加標記的 `bigquery.tables.update` 權限 | * 資料表或檢視表的 `bigquery.tables.createTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.create` 權限 |
| 從資料表或檢視畫面移除標籤 | * 資料表或檢視表的 `bigquery.tables.deleteTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.delete` 權限 * 更新資料表或檢視表時，移除標記的 `bigquery.tables.update` 權限 | * 資料表或檢視表的 `bigquery.tables.deleteTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.delete` 權限 |
| 將標記附加至資料集 | * 資料集的 `bigquery.datasets.createTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.create` 權限 * `bigquery.datasets.create` 建立資料集時附加標記的權限 * 更新資料集時附加標記的 `bigquery.datasets.update` 權限 | * 資料集的 `bigquery.datasets.createTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.create` 權限 |
| 從資料集中移除標記 | * 資料集的 `bigquery.datasets.deleteTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.delete` 權限 * 更新資料集時移除標記的 `bigquery.datasets.update` 權限 | * 資料集的 `bigquery.datasets.deleteTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.delete` 權限 |

如要在 Google Cloud 控制台中列出標記鍵和鍵值，您需要下列權限：

* 如要列出與上層機構或專案相關聯的標記鍵，您需要標記鍵父項層級的 `resourcemanager.tagKeys.list` 權限，以及每個標記鍵的 `resourcemanager.tagKeys.get` 權限。如要在 BigQuery 控制台中查看標記鍵清單，請按一下資料集名稱，然後點選「編輯詳細資料」，或按一下資料表或檢視表名稱，然後依序點選「詳細資料」>「編輯詳細資料」。
* 如要列出與上層機構或專案相關聯的鍵標記值，您需要標記值父項層級的 `resourcemanager.tagValues.list` 權限，以及每個標記值的 `resourcemanager.tagValues.get` 權限。**如要在 BigQuery 控制台中查看標記鍵值清單，請按一下資料集名稱，然後點選「編輯詳細資料」，或按一下資料表或檢視名稱，然後依序點選「詳細資料」>「編輯詳細資料」**。

如要在 Cloud Resource Manager API 或 gcloud 中使用標記，您需要下列權限：

* 如要列出附加至表格的標記，或使用 Cloud Resource Manager API 或 gcloud CLI 查看，您需要 `bigquery.tables.listTagBindings` IAM 權限。
* 如要列出資料表或檢視表的有效標記，您需要 `bigquery.tables.listEffectiveTags` IAM 權限。
* 如要使用 Cloud Resource Manager API 或 gcloud CLI 列出附加至資料集的標記，您需要 `bigquery.datasets.listTagBindings`
  IAM 權限。
* 如要列出資料集的有效標記，您必須具備 `bigquery.datasets.listEffectiveTags` IAM 權限。

## 建立標記鍵和值

您可以先建立標記，再將其附加至 BigQuery 資源，也可以使用Google Cloud 控制台建立資源時，手動建立標記。

如要瞭解如何建立標記鍵和標記值，請參閱 Resource Manager 說明文件中的「[建立標記](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw#creating_tag)」和「[新增標記值](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw#adding_tag_values)」。

## 為資料集加上標記

以下各節說明如何將標記附加至新資料集和現有資料集、列出附加至資料集的標記，以及從資料集卸離標記。

### 建立新資料集時附加標記

建立標記後，即可將其附加至新的 BigQuery 資料集。針對任何指定標記鍵，您只能將一個標記值附加至資料集。
一個資料集最多可附加 50 個標記。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，選取要建立資料集的專案。
4. 依序點按「查看動作」>「建立資料集」。more\_vert
5. 輸入新資料集的資訊。詳情請參閱「[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)」。
6. 展開「代碼」部分。

   1. 如要套用現有標籤，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後選擇「目前範圍」，並選取「選取目前的機構」或「選取目前的專案」。

         或者，按一下「選取範圍」搜尋資源，或查看目前的資源清單。
      2. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   2. 如要手動輸入新標記，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後依序選擇「手動輸入 ID」>「機構」、「專案」或「標記」。
      2. 如要為專案或機構建立標記，請在對話方塊中輸入 `PROJECT_ID` 或 `ORGANIZATION_ID`，然後按一下「儲存」。
      3. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   3. 選用：如要在表格中新增其他代碼，請按一下「新增代碼」，然後按照先前的步驟操作。
7. 點選「建立資料集」。

### SQL

使用 [`CREATE SCHEMA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_schema_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE SCHEMA PROJECT_ID.DATASET_ID
   OPTIONS (
     tags = [('TAG_KEY_1', 'TAG_VALUE_1'), ('TAG_KEY_2', 'TAG_VALUE_2')];)
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：您要建立的資料集 ID。
   * `TAG_KEY_1`：您要設為資料集第一個標記的[命名空間鍵名](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'my-project/env'` 或 `'556741164180/department'`。
   * `TAG_VALUE_1`：標記值的[簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'prod'` 或 `'sales'`。
   * `TAG_KEY_2`：第二個標記的命名空間鍵名。
   * `TAG_VALUE_2`：第二個標記值的簡稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用加上 `--add_tags` 旗標的 [`bq mk --dataset` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)：

```
bq mk --dataset \
    --add_tags=TAG \
    PROJECT_ID:DATASET_ID
```

更改下列內容：

* `TAG`：要附加至新資料集的標記。多個標記之間以半形逗號分隔。例如：`556741164180/env:prod,myProject/department:sales`。每個標記都必須有[命名空間限定的鍵名和值簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)。
* `PROJECT_ID`：您要建立資料集的專案 ID。
* `DATASET_ID`：新資料集的 ID。

### Terraform

請使用 [`google_bigquery_dataset`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會建立名為 `my_dataset` 的資料集，然後填入 `resource_tags` 欄位，將標記附加至該資料集：

```
# Create tag keys and values
data "google_project" "default" {}

resource "google_tags_tag_key" "env_tag_key" {
  parent     = "projects/${data.google_project.default.project_id}"
  short_name = "env2"
}

resource "google_tags_tag_key" "department_tag_key" {
  parent     = "projects/${data.google_project.default.project_id}"
  short_name = "department2"
}

resource "google_tags_tag_value" "env_tag_value" {
  parent     = "tagKeys/${google_tags_tag_key.env_tag_key.name}"
  short_name = "prod"
}

resource "google_tags_tag_value" "department_tag_value" {
  parent     = "tagKeys/${google_tags_tag_key.department_tag_key.name}"
  short_name = "sales"
}

# Create a dataset
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "my_dataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

  # Attach tags to the dataset
  resource_tags = {
    (google_tags_tag_key.env_tag_key.namespaced_name) : google_tags_tag_value.env_tag_value.short_name,
    (google_tags_tag_key.department_tag_key.namespaced_name) : google_tags_tag_value.department_tag_value.short_name
  }
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   每項專案只需要執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的範例程式碼。

   將範例程式碼複製到新建立的 `main.tf` 中。

   視需要從 GitHub 複製程式碼。如果 Terraform 程式碼片段是端對端解決方案的一部分，建議您使用這種做法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

呼叫 [`datasets.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw)，並將標記新增至 `resource_tags` 欄位。

### 將標記附加至現有資料集

建立標記後，即可將其附加至現有資料集。針對任何指定標記鍵，您只能將一個標記值附加至資料集。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「Dataset info」(資料集資訊) 部分，按一下 mode\_edit「Edit details」(編輯詳細資料)。
5. 展開「代碼」部分。

   1. 如要套用現有標籤，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後選擇「目前範圍」，並選取「選取目前的機構」或「選取目前的專案」。

         或者，按一下「選取範圍」搜尋資源，或查看目前的資源清單。
      2. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   2. 如要手動輸入新標記，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後依序選擇「手動輸入 ID」>「機構」、「專案」或「標記」。
      2. 如要為專案或機構建立標記，請在對話方塊中輸入 `PROJECT_ID` 或 `ORGANIZATION_ID`，然後按一下「儲存」。
      3. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   3. 選用：如要在表格中新增其他代碼，請按一下「新增代碼」，然後按照先前的步驟操作。
6. 按一下 [儲存]。

### SQL

使用 [`ALTER SCHEMA SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)。

以下範例會覆寫現有資料集的所有標記。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER SCHEMA PROJECT_ID.DATASET_ID
   SET OPTIONS (
     tags = [('TAG_KEY_1', 'TAG_VALUE_1'), ('TAG_KEY_2', 'TAG_VALUE_2')];)
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：包含資料表的資料集 ID。
   * `TABLE_ID`：要標記的資料表名稱。
   * `TAG_KEY_1`：您要設為資料表第一個標記的[命名空間鍵名](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'my-project/env'` 或 `'556741164180/department'`。
   * `TAG_VALUE_1`：標記值的[簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'prod'` 或 `'sales'`。
   * `TAG_KEY_2`：第二個標記的命名空間鍵名。
   * `TAG_VALUE_2`：第二個標記值的簡稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

以下範例使用 `+=` 運算子，將標記附加至資料集，而不覆寫現有標記。如果現有標記的鍵相同，系統會覆寫該標記。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER SCHEMA PROJECT_ID.DATASET_ID
   SET OPTIONS (
     tags += [('TAG_KEY_1', 'TAG_VALUE_1'), ('TAG_KEY_2', 'TAG_VALUE_2')];)
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：包含資料表的資料集 ID。
   * `TABLE_ID`：要標記的資料表名稱。
   * `TAG_KEY_1`：您要設為資料表第一個標記的[命名空間鍵名](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'my-project/env'` 或 `'556741164180/department'`。
   * `TAG_VALUE_1`：標記值的[簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'prod'` 或 `'sales'`。
   * `TAG_KEY_2`：第二個標記的命名空間鍵名。
   * `TAG_VALUE_2`：第二個標記值的簡稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用加上 `--add_tags` 旗標的 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)：

```
bq update \
    --add_tags=TAG \
    PROJECT_ID:DATASET_ID
```

更改下列內容：

* `TAG`：要附加至資料集的標記。
  多個標記之間以半形逗號分隔。例如：`556741164180/env:prod,myProject/department:sales`。每個標記都必須有[命名空間限定的鍵名和值簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)。
* `PROJECT_ID`：現有資料集所在的專案 ID。
* `DATASET_ID`：現有資料集的 ID。

### gcloud

如要使用指令列將標記附加至資料集，請使用 [`gcloud resource-manager tags bindings create` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/resource-manager/tags/bindings/create?hl=zh-tw)建立標記繫結資源：

```
gcloud resource-manager tags bindings create \
    --tag-value=TAG_VALUE_NAME \
    --parent=RESOURCE_ID \
    --location=LOCATION
```

更改下列內容：

* `TAG_VALUE_NAME`：要附加的標記值永久 ID 或命名空間名稱，例如 `tagValues/4567890123` 或 `1234567/my_tag_key/my_tag_value`。
* `RESOURCE_ID`：資料集的完整 ID，包括 API 網域名稱 (`//bigquery.googleapis.com/`)，用於識別資源類型。例如：`//bigquery.googleapis.com/projects/my_project/datasets/my_dataset`。
* `LOCATION`：資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

### Terraform

將標記新增至資料集的 `resource_tags` 欄位，然後使用 `google_bigquery_dataset` 資源套用更新後的設定。詳情請參閱「[建立新資料集時附加標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw#attach_tags_when_you_create_a_new_dataset)」一文中的 Terraform 範例。

### API

呼叫 [`datasets.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw)，取得資料集資源，包括 `resource_tags` 欄位。將標記新增至 `resource_tags` 欄位，然後使用 [`datasets.update` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/update?hl=zh-tw)傳回更新後的資料集資源。

### 列出附加至資料集的標記

下列步驟會列出直接附加至資料集的標記繫結。這些方法不會傳回從父項資源沿用的標記。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。

   標記會顯示在「Dataset info」(資料集資訊) 部分。

### bq

如要列出附加至資料集的標記，請使用 [`bq show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show)。

```
bq show PROJECT_ID:DATASET_ID
```

更改下列內容：

* `PROJECT_ID`：包含資料集的專案 ID。
* `DATASET_ID`：要列出標記的資料集 ID。

### gcloud

如要取得附加至資源的標記繫結清單，請使用 [`gcloud resource-manager tags bindings list` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/resource-manager/tags/bindings/list?hl=zh-tw)：

```
gcloud resource-manager tags bindings list \
    --parent=RESOURCE_ID \
    --location=LOCATION
```

更改下列內容：

* `RESOURCE_ID`：資料集的完整 ID，包括 API 網域名稱 (`//bigquery.googleapis.com/`)，用於識別資源類型。例如：`//bigquery.googleapis.com/projects/my_project/datasets/my_dataset`。
* `LOCATION`：資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

輸出結果會與下列內容相似：

```
name: tagBindings/%2F%2Fbigquery.googleapis.com%2Fprojects%2Fmy_project%2Fdatasets%2Fmy_dataset/tagValues/4567890123
parent: //bigquery.googleapis.com/projects/my_project/datasets/my_dataset
tagValue: tagValues/4567890123
```

您可以使用 `gcloud resource-manager tags bindings list`，列出 BigQuery 資料集繼承的標記。您也可以使用 `namespacedTagValue` 屬性的 [`--filter`](https://docs.cloud.google.com/sdk/gcloud/reference/topic/filters?hl=zh-tw) 選項，依專案 ID、標籤值或標籤鍵篩選標籤。

```
gcloud resource-manager tags bindings list \
    --parent=//bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID \
    --effective \
    --filter=namespacedTagValue:TAG_FILTER
```

請替換下列項目：

* `PROJECT_ID`：包含資料集的專案 ID。
* `DATASET_ID`：資料集 ID。
* `TAG_FILTER`：根據下列其中一個項目指定值，篩選出已繼承的標記：

  + 依專案 ID 篩選標記。例如 `myproject`。
  + 指定標記值的永久 ID 或命名空間名稱，即可篩選標記值。例如 `tagValues/4567890123` 或 `1234567/my_tag_key/my_tag_value`。
  + 指定標記鍵的顯示名稱，即可篩選標記鍵。
    例如 `tagkey`。

### Terraform

使用 `terraform state show` 指令列出資料集的屬性，包括 `resource_tags` 欄位。在已執行資料集 Terraform 設定檔的目錄中，執行下列指令。

```
terraform state show google_bigquery_dataset.default
```

### API

呼叫 [`datasets.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw)，取得資料集資源。資料集資源包含附加至資料集的標記，位於 `resource_tags` 欄位中。

### 觀看次數

使用 [`INFORMATION_SCHEMA.SCHEMATA_OPTIONS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata-options?hl=zh-tw)。

舉例來說，下列查詢會顯示區域中所有資料集附加的所有標記。這項查詢會傳回資料表，其中包含 `schema_name` (資料集名稱)、`option_name` (一律為 `'tags'`)、`object_type` (一律為 `ARRAY<STRUCT<STRING, STRING>>`) 和 `option_value` 等資料欄，其中包含代表與每個資料集相關聯標記的 `STRUCT` 物件陣列。如果資料集沒有指派的標記，`option_value` 欄會傳回空陣列。

```
SELECT * from region-REGION.INFORMATION_SCHEMA.SCHEMATA_OPTIONS
WHERE option_name='tags'
```

更改下列內容：

* `REGION`：資料集所在的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

**注意：** 您可以使用 [`gcloud resource-manager tags bindings list`](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw#gcloud_1) 指令，列出 BigQuery 資料集和資料表繼承的標記。

### 從資料集卸離標記

如要從資源卸離標記，請刪除標記繫結資源。如要刪除標記，請務必先將標記從資料集中分離，再刪除標記。詳情請參閱「[刪除代碼](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw#deleting)」。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「Dataset info」(資料集資訊) 部分，按一下 mode\_edit「Edit details」(編輯詳細資料)。
5. 在「標記」部分中，找出要刪除的標記，然後按一下旁邊的「刪除項目」delete。
6. 按一下 [儲存]。

### SQL

使用 [`ALTER SCHEMA SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)。

以下範例使用 `-=` 運算子，從資料集卸離標記。如要從資料集卸離所有標記，可以指定 `tags=NULL` 或 `tags=[]`。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE PROJECT_ID.DATASET_ID.TABLE_ID
   SET OPTIONS (
     tags -= [('TAG_KEY_1', 'TAG_VALUE_1'), ('TAG_KEY_2', 'TAG_VALUE_2')];)
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：包含資料表的資料集 ID。
   * `TABLE_ID`：要從中卸離標記的資料表名稱。
   * `TAG_KEY_1`：要取消連結的第一個標記的[命名空間索引鍵名稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'my-project/env'` 或 `'556741164180/department'`。
   * `TAG_VALUE_1`：要卸離的標記值[簡短名稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'prod'` 或 `'sales'`。
   * `TAG_KEY_2`：要卸離的第二個標記的命名空間鍵名。
   * `TAG_VALUE_2`：要卸除的第二個標記值簡稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用加上 `--remove_tags` 旗標的 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)：

```
bq update \
    --remove_tags=REMOVED_TAG \
    PROJECT_ID:DATASET_ID
```

更改下列內容：

* `REMOVED_TAG`：要從資料集中移除的標記。多個標記之間以半形逗號分隔。僅接受沒有值配對的鍵。例如：`556741164180/env,myProject/department`。每個標記都必須有[命名空間鍵名](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)。
* `PROJECT_ID`：包含資料集的專案 ID。
* `DATASET_ID`：要從中卸離標記的資料集 ID。

或者，如要從資料集移除「所有」標記，請使用 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)並搭配 `--clear_all_tags` 標記：

```
bq update \
    --clear_all_tags
    PROJECT_ID:DATASET_ID
```

### gcloud

如要使用指令列從資料集卸離標記，請使用 [`gcloud resource-manager tags bindings delete` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/resource-manager/tags/bindings/delete?hl=zh-tw)刪除標記繫結：

```
gcloud resource-manager tags bindings delete \
    --tag-value=TAG_VALUE_NAME \
    --parent=RESOURCE_ID \
    --location=LOCATION
```

更改下列內容：

* `TAG_VALUE_NAME`：要取消連結的標記值永久 ID 或命名空間名稱，例如 `tagValues/4567890123` 或 `1234567/my_tag_key/my_tag_value`。
* `RESOURCE_ID`：資料集的完整 ID，包括 API 網域名稱 (`//bigquery.googleapis.com/`)，用於識別資源類型。例如：`//bigquery.googleapis.com/projects/my_project/datasets/my_dataset`。
* `LOCATION`：資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

### Terraform

從資料集的 `resource_tags` 欄位移除標記，然後使用 `google_bigquery_dataset` 資源套用更新後的設定。

### API

呼叫 [`datasets.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw)，取得資料集資源，包括 `resource_tags` 欄位。從 `resource_tags` 欄位移除標記，並使用 [`datasets.update` 方法傳回更新後的資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/update?hl=zh-tw)。

## 標記資料表

以下各節說明如何將標記附加至新資料表和現有資料表、列出附加至資料表的標記，以及從資料表卸離標記。

### 建立新資料表時附加標記

建立標籤後，您可以將其附加至新表格。針對任何指定標記鍵，您只能將一個標記值附加至表格。每個表格最多可附加 50 個標記。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 add\_box「建立資料表」。
5. 輸入新資料表的資訊。詳情請參閱「[建立及使用資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)」。
6. 展開「代碼」部分。

   1. 如要套用現有標籤，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後選擇「目前範圍」，並選取「選取目前的機構」或「選取目前的專案」。

         或者，按一下「選取範圍」搜尋資源，或查看目前的資源清單。
      2. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   2. 如要手動輸入新標記，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後依序選擇「手動輸入 ID」>「機構」、「專案」或「標記」。
      2. 如要為專案或機構建立標記，請在對話方塊中輸入 `PROJECT_ID` 或 `ORGANIZATION_ID`，然後按一下「儲存」。
      3. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   3. 選用：如要在表格中新增其他代碼，請按一下「新增代碼」，然後按照先前的步驟操作。
7. 點選「建立資料表」。

### SQL

使用 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE PROJECT_ID.DATASET_ID.TABLE_ID
   OPTIONS (
     tags = [('TAG_KEY_1', 'TAG_VALUE_1'), ('TAG_KEY_2', 'TAG_VALUE_2')];)
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：您要在其中建立資料表的資料集 ID。
   * `TABLE_ID`：新資料表的名稱。
   * `TAG_KEY_1`：您要設為資料表第一個標記的[命名空間鍵名](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'my-project/env'` 或 `'556741164180/department'`。
   * `TAG_VALUE_1`：標記值的[簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'prod'` 或 `'sales'`。
   * `TAG_KEY_2`：第二個標記的命名空間鍵名。
   * `TAG_VALUE_2`：第二個標記值的簡稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用加上 `--add_tags` 旗標的 [`bq mk --table` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)：

```
bq mk --table \
    --schema=SCHEMA \
    --add_tags=TAG \
    PROJECT_ID:DATASET_ID.TABLE_ID
```

更改下列內容：

* `SCHEMA`：[內嵌結構定義](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create_an_empty_table_with_a_schema_definition)。
* `TAG`：要附加至新表格的標記。多個標記之間以半形逗號分隔。例如：`556741164180/env:prod,myProject/department:sales`。每個標記都必須有[命名空間限定鍵名和值簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)。
* `PROJECT_ID`：您要建立表格的專案 ID。
* `DATASET_ID`：您要在其中建立表格的資料集 ID。
* `TABLE_ID`：新資料表的 ID。

### Terraform

請使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會建立名為 `mytable` 的資料表，然後填入 `resource_tags` 欄位，將標記附加至該資料表：

```
# Create tag keys and values
data "google_project" "default" {}

resource "google_tags_tag_key" "env_tag_key" {
  parent     = "projects/${data.google_project.default.project_id}"
  short_name = "env3"
}

resource "google_tags_tag_key" "department_tag_key" {
  parent     = "projects/${data.google_project.default.project_id}"
  short_name = "department3"
}

resource "google_tags_tag_value" "env_tag_value" {
  parent     = "tagKeys/${google_tags_tag_key.env_tag_key.name}"
  short_name = "prod"
}

resource "google_tags_tag_value" "department_tag_value" {
  parent     = "tagKeys/${google_tags_tag_key.department_tag_key.name}"
  short_name = "sales"
}

# Create a dataset
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "MyDataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days
}

# Create a table
resource "google_bigquery_table" "default" {
  dataset_id  = google_bigquery_dataset.default.dataset_id
  table_id    = "mytable"
  description = "table description"

  # Attach tags to the table
  resource_tags = {
    (google_tags_tag_key.env_tag_key.namespaced_name) : google_tags_tag_value.env_tag_value.short_name,
    (google_tags_tag_key.department_tag_key.namespaced_name) : google_tags_tag_value.department_tag_value.short_name
  }
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   每項專案只需要執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的範例程式碼。

   將範例程式碼複製到新建立的 `main.tf` 中。

   視需要從 GitHub 複製程式碼。如果 Terraform 程式碼片段是端對端解決方案的一部分，建議您使用這種做法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

使用已定義的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)。在 `resource_tags` 欄位中加入標記。

### 將標記附加至現有資料表

建立標記後，即可將其附加至現有資料表。針對任何指定標記鍵，您只能將一個標記值附加至表格。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」。
4. 依序按一下「總覽」**>「表格」**，然後選取表格。
5. 按一下「詳細資料」分頁標籤，然後點選「編輯詳細資料」mode\_edit。
6. 展開「代碼」部分。

   1. 如要套用現有標籤，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後選擇「目前範圍」，並選取「選取目前的機構」或「選取目前的專案」。

         或者，按一下「選取範圍」搜尋資源，或查看目前的資源清單。
      2. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   2. 如要手動輸入新標記，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後依序選擇「手動輸入 ID」>「機構」、「專案」或「標記」。
      2. 如要為專案或機構建立標記，請在對話方塊中輸入 `PROJECT_ID` 或 `ORGANIZATION_ID`，然後按一下「儲存」。
      3. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   3. 選用：如要在表格中新增其他代碼，請按一下「新增代碼」，然後按照先前的步驟操作。
7. 按一下 [儲存]。

### SQL

使用 [`ALTER TABLE SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)。

以下範例會覆寫現有資料表的所有標記。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE PROJECT_ID.DATASET_ID.TABLE_ID
   SET OPTIONS (
     tags = [('TAG_KEY_1', 'TAG_VALUE_1'), ('TAG_KEY_2', 'TAG_VALUE_2')];)
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：包含資料表的資料集 ID。
   * `TABLE_ID`：要標記的資料表名稱。
   * `TAG_KEY_1`：您要設為資料表第一個標記的[命名空間鍵名](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'my-project/env'` 或 `'556741164180/department'`。
   * `TAG_VALUE_1`：標記值的[簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'prod'` 或 `'sales'`。
   * `TAG_KEY_2`：第二個標記的命名空間鍵名。
   * `TAG_VALUE_2`：第二個標記值的簡稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

以下範例使用 `+=` 運算子將標記附加至資料表，不會覆寫現有標記。如果現有標記的鍵相同，系統會覆寫該標記。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE PROJECT_ID.DATASET_ID.TABLE_ID
   SET OPTIONS (
     tags += [('TAG_KEY_1', 'TAG_VALUE_1'), ('TAG_KEY_2', 'TAG_VALUE_2')];)
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：包含資料表的資料集 ID。
   * `TABLE_ID`：要標記的資料表名稱。
   * `TAG_KEY_1`：您要設為資料表第一個標記的[命名空間鍵名](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'my-project/env'` 或 `'556741164180/department'`。
   * `TAG_VALUE_1`：標記值的[簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'prod'` 或 `'sales'`。
   * `TAG_KEY_2`：第二個標記的命名空間鍵名。
   * `TAG_VALUE_2`：第二個標記值的簡稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用加上 `--add_tags` 旗標的 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)：

```
bq update \
    --add_tags=TAG \
    PROJECT_ID:DATASET_ID.TABLE_ID
```

更改下列內容：

* `TAG`：要附加至資料表的標記。多個標記之間以半形逗號分隔。例如：`556741164180/env:prod,myProject/department:sales`。每個標記都必須有[命名空間限定鍵名和值簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)。
* `PROJECT_ID`：包含資料表的專案 ID。
* `DATASET_ID`：包含表格的資料集 ID。
* `TABLE_ID`：要更新的資料表 ID。

### gcloud

如要透過指令列將標記附加至資料表，請使用 [`gcloud resource-manager tags bindings create` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/resource-manager/tags/bindings/create?hl=zh-tw)建立標記繫結資源：

```
gcloud resource-manager tags bindings create \
    --tag-value=TAG_VALUE_NAME \
    --parent=RESOURCE_ID \
    --location=LOCATION
```

更改下列內容：

* `TAG_VALUE_NAME`：要附加的標記值永久 ID 或命名空間名稱，例如 `tagValues/4567890123` 或 `1234567/my_tag_key/my_tag_value`。
* `RESOURCE_ID`：資料表的完整 ID，包括 API 網域名稱 (`//bigquery.googleapis.com/`)，用於識別資源類型。例如：
  `//bigquery.googleapis.com/projects/my_project/datasets/my_dataset/tables/my_table`
* `LOCATION`：資料表的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

### Terraform

在資料表的 `resource_tags` 欄位中新增標記，然後使用 `google_bigquery_table` 資源套用更新後的設定。詳情請參閱「[建立新資料表時附加標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw#attach_tags_when_you_create_a_new_table)」中的 Terraform 範例。

### API

使用已定義的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.update` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/update?hl=zh-tw)。在 `resource_tags` 欄位中加入標記。

### 列出附加至資料表的標記

您可以列出直接附加至資料表的標記。這個程序不會列出從父項資源繼承的標記。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」。
4. 依序按一下「總覽」**>「表格」**，然後選取表格。

   標記會顯示在「詳細資料」分頁中。

### bq

使用 [`bq show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show)，然後尋找 `tags` 欄。如果表格中沒有任何代碼，系統就不會顯示 `tags` 欄。

```
bq show \
    PROJECT_ID:DATASET_ID.TABLE_ID
```

更改下列內容：

* `PROJECT_ID`：包含資料表的專案 ID。
* `DATASET_ID`：包含表格的資料集 ID。
* `TABLE_ID`：資料表的 ID。

### gcloud

如要取得附加至資源的標記繫結清單，請使用 [`gcloud resource-manager tags bindings list` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/resource-manager/tags/bindings/list?hl=zh-tw)：

```
gcloud resource-manager tags bindings list \
    --parent=RESOURCE_ID \
    --location=LOCATION
```

更改下列內容：

* `RESOURCE_ID`：資料表的完整 ID，包括 API 網域名稱 (`//bigquery.googleapis.com/`)，用於識別資源類型。例如：`//bigquery.googleapis.com/projects/my_project/datasets/my_dataset/tables/my_table`。
* `LOCATION`：資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

輸出結果會與下列內容相似：

```
name: tagBindings/%2F%2Fbigquery.googleapis.com%2Fprojects%2Fmy_project%2Fdatasets%2Fmy_dataset/tagValues/4567890123
parent: //bigquery.googleapis.com/projects/my_project/datasets/my_dataset
tagValue: tagValues/4567890123
```

您可以使用 `gcloud resource-manager tags bindings list`，列出 BigQuery 資料表繼承的標記。您也可以使用 `namespacedTagValue` 屬性的 [`--filter`](https://docs.cloud.google.com/sdk/gcloud/reference/topic/filters?hl=zh-tw) 選項，依專案 ID、標籤值或標籤鍵篩選標籤。

```
gcloud resource-manager tags bindings list \
    --parent=//bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET_ID/tables/TABLE_ID \
    --effective \
    --filter=namespacedTagValue:TAG_FILTER
```

請替換下列項目：

* `PROJECT_ID`：包含資料集的專案 ID。
* `DATASET_ID`：資料集 ID。
* `TAG_FILTER`：根據下列其中一個項目指定值，篩選出已繼承的標記：

  + 依專案 ID 篩選標記。例如 `myproject`。
  + 指定標記值的永久 ID 或命名空間名稱，即可篩選標記值。例如 `tagValues/4567890123` 或 `1234567/my_tag_key/my_tag_value`。
  + 指定標記鍵的顯示名稱，即可篩選標記鍵。
    例如 `tagkey`。

### Terraform

使用 `terraform state show` 指令列出資料表的屬性，包括 `resource_tags` 欄位。在執行資料表 Terraform 設定檔的目錄中執行這項指令。

```
terraform state show google_bigquery_table.default
```

### API

使用已定義的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw)，然後尋找 `resource_tags` 欄位。

### 觀看次數

使用 [`INFORMATION_SCHEMA.TABLE_OPTIONS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-table-options?hl=zh-tw)。

舉例來說，下列查詢會顯示資料集中所有資料表附加的所有標記。這項查詢會傳回資料表，其中包含 `schema_name` (資料集名稱)、`option_name` (一律為 `'tags'`)、`object_type` (一律為 `ARRAY<STRUCT<STRING, STRING>>`) 和 `option_value` 等資料欄，其中包含代表與每個資料集相關聯標記的 `STRUCT` 物件陣列。如果資料表沒有指派的標記，`option_value` 欄會傳回空陣列。

```
SELECT * from DATASET_ID.INFORMATION_SCHEMA.TABLE_OPTIONS
WHERE option_name='tags'
```

將 `DATASET_ID` 替換為包含資料表的資料集 ID。

**注意：** 您可以使用 [`gcloud resource-manager tags bindings list`](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw#gcloud_4) 指令，列出 BigQuery 資料集和資料表繼承的標記。

### 從資料表取消連結標記

如要從資料表移除標記關聯，請刪除標記繫結。
如要刪除標記，必須先將標記從表格卸離，才能刪除。詳情請參閱「[刪除代碼](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw#deleting)」。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」。
4. 依序按一下「總覽」**>「表格」**，然後選取表格。
5. 按一下「詳細資料」分頁標籤，然後點選「編輯詳細資料」mode\_edit。
6. 在「標記」部分中，找出要刪除的標記，然後按一下旁邊的「刪除項目」delete。
7. 按一下 [儲存]。

### SQL

使用 [`ALTER TABLE SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)。

下列範例使用 `-=` 運算子，從資料表卸離標記。如要從資料表卸離所有標記，可以指定 `tags=NULL` 或 `tags=[]`。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE PROJECT_ID.DATASET_ID.TABLE_ID
   SET OPTIONS (
     tags -= [('TAG_KEY_1', 'TAG_VALUE_1'), ('TAG_KEY_2', 'TAG_VALUE_2')];)
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：包含資料表的資料集 ID。
   * `TABLE_ID`：要從中卸離標記的資料表名稱。
   * `TAG_KEY_1`：要取消連結的第一個標記的[命名空間索引鍵名稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'my-project/env'` 或 `'556741164180/department'`。
   * `TAG_VALUE_1`：要卸離的標記值[簡短名稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'prod'` 或 `'sales'`。
   * `TAG_KEY_2`：要卸離的第二個標記的命名空間鍵名。
   * `TAG_VALUE_2`：要卸除的第二個標記值簡稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要從資料表移除部分標記，請使用帶有 `--remove_tags` 旗標的 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)：

```
bq update \
    --remove_tags=TAG_KEYS \
    PROJECT_ID:DATASET_ID.TABLE_ID
```

更改下列內容：

* `TAG_KEYS`：要從資料表分離的標記鍵，以半形逗號分隔。例如：`556741164180/env,myProject/department`。每個標記鍵都必須有[命名空間鍵名](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)。
* `PROJECT_ID`：包含資料表的專案 ID。
* `DATASET_ID`：包含表格的資料集 ID。
* `TABLE_ID`：要更新的資料表 ID。

如要從資料表移除所有標記，請使用 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)搭配 `--clear_all_tags` 標記：

```
bq update \
    --clear_all_tags \
    PROJECT_ID:DATASET_ID.TABLE_ID
```

### gcloud

如要透過指令列從資料表移除標記關聯，請使用 [`gcloud resource-manager tags bindings delete` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/resource-manager/tags/bindings/delete?hl=zh-tw)刪除標記繫結：

```
gcloud resource-manager tags bindings delete \
    --tag-value=TAG_VALUE_NAME \
    --parent=RESOURCE_ID \
    --location=LOCATION
```

更改下列內容：

* `TAG_VALUE_NAME`：要刪除的標記值永久 ID 或命名空間名稱，例如 `tagValues/4567890123` 或 `1234567/my_tag_key/my_tag_value`。
* `RESOURCE_ID`：資料表的完整 ID，包括 API 網域名稱 (`//bigquery.googleapis.com/`)，用於識別資源類型。例如：`//bigquery.googleapis.com/projects/my_project/datasets/my_dataset/tables/my_table`。
* `LOCATION`：資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

### Terraform

從資料表的 `resource_tags` 欄位移除標記，然後使用 `google_bigquery_table` 資源套用更新後的設定。

### API

使用已定義的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.update` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/update?hl=zh-tw)，然後移除 `resource_tags` 欄位中的標記。如要移除所有標記，請移除 `resource_tags` 欄位。

## 標記其他類似表格的資源

您也可以為 BigQuery 檢視表、具體化檢視表、副本和快照加上標記。

## 標記欄

您可以為資料表資料欄加上[資料治理標記](#data-governance-tags)，以便在資料欄層級控管存取權及遮蓋資料。

## 刪除標記

如果資料表、資料檢視或資料集參照標記，您就無法刪除標記。刪除標記鍵或值本身之前，請先卸離所有現有的標記繫結資源。如要刪除標記鍵和標記值，請參閱「[刪除標記](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw#deleting)」。

## 範例

假設您是機構管理員，您的資料分析師都是群組 analysts@example.com 的成員，該群組在專案 `userData` 中具有 BigQuery 資料檢視者 IAM 角色。公司聘用資料分析實習生，根據公司政策，該實習生只能在 `userData` 專案中查看 `anonymousData` 資料集。您可以使用標記控管存取權。

1. [建立標記](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw#creating_tag)，鍵為 `employee_type`，值為 `intern`：
2. 前往 Google Cloud 控制台的「IAM」(身分與存取權管理) 頁面。

   [前往「IAM」(身分與存取權管理) 頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
3. 找出要限制資料集存取權的實習生，然後點選該列中的「Edit principal」(編輯主體)edit。
4. 在「角色」選單中，選取「BigQuery 資料檢視者」。
5. 按一下「新增條件」。
6. 在「Title」(標題) 和「Description」(說明) 欄位中，輸入描述要建立的 IAM 標記條件的值。
7. 在「條件建構工具」分頁中，按一下「新增」。
8. 在「條件類型」選單中，依序選取「資源」和「標記」。
9. 在「運算子」選單中，選取「有值」。
10. 在「Value path」(值路徑) 欄位中，以以下形式輸入標記值路徑：
    `ORGANIZATION/TAG_KEY/TAG_VALUE`。
    例如：`example.org/employee_type/intern`。

    這項 IAM 標記條件會限制實習生只能存取具有 `intern` 標記的資料集。
11. 如要儲存代碼條件，請按一下「儲存」。
12. 如要儲存您在「編輯權限」窗格中所做的變更，請按一下「儲存」。
13. 如要將 `intern` 代碼值附加至 `anonymousData` 資料集，請使用指令列執行 `gcloud resource-manager tags bindings create` 指令。例如：

    ```
    gcloud resource-manager tags bindings create \
        --tag-value=tagValues/4567890123 \
        --parent=//bigquery.googleapis.com/projects/userData/datasets/anonymousData \
        --location=US
    ```

## 使用資料治理標記控管資料欄存取權

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或尋求這項功能支援，請傳送電子郵件至 [bigquery-security-feedback@google.com](mailto:bigquery-security-feedback@google.com)。

您可以使用資料治理標記，在 BigQuery 中強制執行資料欄層級安全防護機制和資料遮蓋。資料治理標記是一種 Resource Manager 標記，可附加至機密資料欄，並用於 BigQuery 資料政策，授予使用者條件式存取權。

建立資料治理標記並附加至 BigQuery 資料欄，即可設定資料欄層級的安全防護機制。然後，建立參照這些標記的 BigQuery 資料政策。這些政策會套用資料遮蓋規則，或授予特定使用者原始資料存取權，確保只有授權主體能查看私密資料。

詳情請參閱「[欄層級存取控管簡介](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)」和「[資料遮蓋簡介](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)」。

### 開始使用控管標記前的注意事項

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。

   **注意：**如果您先前已安裝 gcloud CLI，請執行 `gcloud components update`，確認您使用的是最新版本。
2. 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
3. 執行下列指令，[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) gcloud CLI：

   ```
   gcloud init
   ```
4. 如要建立及管理資料治理標記，請務必使用 [BigQuery Enterprise 版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。

#### 資料治理標記的必要角色

如要取得使用資料治理標記控管資料欄存取權所需的權限，請要求管理員授予您下列 IAM 角色：

* 建立資料治理標記：
  + 專案或機構的[標記管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/resourcemanager?hl=zh-tw#resourcemanager.tagAdmin)  (`roles/resourcemanager.tagAdmin`)
  + 機構的[機構檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/resourcemanager?hl=zh-tw#resourcemanager.organizationViewer)  (`roles/resourcemanager.organizationViewer`)
* 為資料欄附加或移除標記：
  + 資料表的 [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)
  + [標記使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/resourcemanager?hl=zh-tw#resourcemanager.tagUser)  (`roles/resourcemanager.tagUser`)
    機構、專案或標記值
* 建立及管理資料政策：
  專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquerydatapolicy?hl=zh-tw#bigquerydatapolicy.admin)  (`roles/bigquerydatapolicy.admin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

### 建立資料治理標記

建立資料治理標記鍵和值。

#### 建立標記鍵

如要為資料治理標記建立鍵，請在建立標記鍵時，將 `purpose` 欄位設為 `DATA_GOVERNANCE`。設定這個用途可將標記歸類為資料欄層級安全防護或資料遮蓋，並與 BigQuery 中的一般資源標記區分。

### gcloud

1. 執行 [`gcloud resource-manager tags keys create`](https://docs.cloud.google.com/sdk/gcloud/reference/resource-manager/tags/keys/create?hl=zh-tw) 指令：

   ```
   gcloud resource-manager tags keys create TAG_KEY \
       --parent=projects/PROJECT_ID \
       --purpose=DATA_GOVERNANCE
   ```

   更改下列內容：

   * `TAG_KEY`：標記鍵的簡稱。
   * `PROJECT_ID`：專案的 ID。 Google Cloud如要提供機構，而非專案，請使用 `organizations/ORGANIZATION_ID`，而非 `projects/PROJECT_ID`。

### API

1. 將 `POST` 要求傳送至 `tagKeys` 端點：

   ```
   curl --request POST \
     "https://cloudresourcemanager.googleapis.com/v3/tagKeys" \
     --header "Authorization: Bearer $(gcloud auth print-access-token)" \
     --header 'Accept: application/json' \
     --header 'Content-Type: application/json' \
     --data '{"shortName":"TAG_KEY","parent":"projects/PROJECT_ID","purpose":"DATA_GOVERNANCE"}' \
     --compressed
   ```

   更改下列內容：

   * `TAG_KEY`：標記鍵的簡稱。
   * `PROJECT_ID`：專案的 ID。 Google Cloud如要提供機構，而非專案，請使用 `organizations/ORGANIZATION_ID`，而非 `projects/PROJECT_ID`。

#### 建立標記值

如要為標記鍵新增一或多個值，請按照下列步驟操作。

### gcloud

1. 執行 [`gcloud resource-manager tags keys list`](https://docs.cloud.google.com/sdk/gcloud/reference/resource-manager/tags/keys/list?hl=zh-tw) 指令，取得標記鍵的命名空間名稱：

   ```
   gcloud resource-manager tags keys list --parent=projects/PROJECT_ID
   ```
2. 執行 [`gcloud resource-manager tags values create`](https://docs.cloud.google.com/sdk/gcloud/reference/resource-manager/tags/values/create?hl=zh-tw) 指令，建立新值：

   ```
   gcloud resource-manager tags values create TAG_VALUE \
       --parent=PROJECT_ID/TAG_KEY
   ```

   更改下列內容：

   * `TAG_VALUE`：使用者指定的代碼值簡稱。
   * `PROJECT_ID`：專案的 ID。 Google Cloud如要提供機構而非專案，請改用 `ORGANIZATION_ID`。

### API

1. 取得標記鍵的命名空間名稱：

   ```
   curl --request GET \
       "https://cloudresourcemanager.googleapis.com/v3/tagKeys/namespaced?name=PROJECT_ID/TAG_KEY" \
       --header "Authorization: Bearer $(gcloud auth print-access-token)" \
       --header 'Accept: application/json'
   ```

   回應包含 `name` 欄位，例如 `tagKeys/4567890123`。
2. 向 `tagValues` 端點傳送 `POST` 要求，並提供標記鍵名稱：

   ```
   curl --request POST \
     "https://cloudresourcemanager.googleapis.com/v3/tagValues" \
     --header "Authorization: Bearer $(gcloud auth print-access-token)" \
     --header 'Accept: application/json' \
     --header 'Content-Type: application/json' \
     --data '{"shortName":"TAG_VALUE","parent":"tagKeys/TAG_KEY_ID"}' \
     --compressed
   ```

   更改下列內容：

   * `TAG_VALUE`：使用者指定的代碼值簡稱。
   * `PROJECT_ID`：專案的 ID。 Google Cloud如要提供機構而非專案，請改用 `ORGANIZATION_ID`。
   * `TAG_KEY_ID`：步驟 1 中標記鍵的命名空間名稱，例如，如果標記鍵名稱為 `tagKeys/4567890123`，則標記鍵 ID 為 `4567890123`。

#### 建立階層式標記值

您也可以選擇建立以標記值為父項的子項標記值，並建立分層的資料治理標記值階層樹狀結構。階層最多可有 5 個層級，如下圖所示：

### gcloud

如要建立子項標記值，請執行 [`gcloud resource-manager tags values create`](https://docs.cloud.google.com/sdk/gcloud/reference/resource-manager/tags/values/create?hl=zh-tw) 指令，並在 `--parent` 旗標中指定父項標記值：

```
gcloud resource-manager tags values create CHILD_TAG_VALUE \
--parent=PROJECT_ID/TAG_KEY/PARENT_TAG_VALUE
```

更改下列內容：

* `CHILD_TAG_VALUE`：您要建立的子代標記值的簡稱。
* `PROJECT_ID`：專案的 ID。 Google Cloud
  如要提供機構而非專案，請改用 `ORGANIZATION_ID`。
* `TAG_KEY`：標記鍵的簡稱，也就是標記值的父項。
* `PARENT_TAG_VALUE`：父項標記值的簡稱。

### API

如要建立子項標記值，請在 `parent` 欄位中使用父項的標記值資源名稱 (例如 `tagValues/123456789012`)：

```
curl --request POST \
  "https://cloudresourcemanager.googleapis.com/v3/tagValues" \
  --header "Authorization: Bearer $(gcloud auth print-access-token)" \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --data '{"shortName":"CHILD_TAG_VALUE","parent":"tagValues/PARENT_TAG_VALUE_ID"}' \
  --compressed
```

更改下列內容：

* `CHILD_TAG_VALUE`：您要建立的子代標記值的簡稱。
* `PARENT_TAG_VALUE_ID`：父項代碼值的數值 ID。

### 將資料治理標記附加至 BigQuery 資料欄

將您建立的資料治理標記附加至要保護的 BigQuery 資料欄。

### SQL

#### 建立含有標記資料欄的新資料表

如要在建立新資料表時附加資料治理標記，請使用 [`CREATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) 陳述式。在資料欄上設定 `data_governance_tags` 選項，即可指定標記。

```
CREATE TABLE PROJECT_ID.DATASET_ID.TABLE_ID (
  COLUMN_NAME INT64 OPTIONS (data_governance_tags=[("PROJECT_ID/TAG_KEY", "TAG_VALUE")])
);
```

更改下列內容：

* `PROJECT_ID`：專案的 ID。 Google Cloud
  如要提供機構，而非專案做為標記的父項，請改用 `ORGANIZATION_ID` 做為標記鍵格式 (`ORGANIZATION_ID/TAG_KEY`)。
* `DATASET_ID`：資料表所在的資料集 ID。
* `TABLE_ID`：您要建立的資料表 ID。
* `COLUMN_NAME`：要標記的資料欄名稱。
* `TAG_KEY`：要套用的標記鍵。
* `TAG_VALUE`：要套用的標記值。

#### 在現有資料表中加入標記

如要將資料治理標記附加至現有資料表中的資料欄，請使用 [`ALTER TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options) 陳述式，在資料欄上設定 `data_governance_tags` 選項。

```
ALTER TABLE PROJECT_ID.DATASET_ID.TABLE_ID
ALTER COLUMN COLUMN_NAME SET OPTIONS (data_governance_tags=[("PROJECT_ID/TAG_KEY", "TAG_VALUE")]);
```

### bq CLI

#### 建立含有已標記資料欄的新資料表

1. 如要建立定義標記的本機 JSON 結構定義檔，請執行 `bq mk` 指令：

   ```
   bq mk \
       --table \
       --project_id=PROJECT_ID \
       --description="description of my table" \
       --schema=SCHEMA_FILE.json \
       DATASET_ID.TABLE_ID
   ```

   更改下列內容：

   * `PROJECT_ID`：專案的 ID。 Google Cloud如要提供機構，而非專案做為代碼的父項，請改用 `ORGANIZATION_ID` 做為代碼鍵格式 (`ORGANIZATION_ID/TAG_KEY`)。
   * `DATASET_ID`：資料表所在的資料集 ID。
   * `TABLE_ID`：要建立的資料表 ID。

#### 在現有資料表中加入標記

1. 如要將標記新增至現有資料表，請先將結構定義匯出至本機檔案：

   ```
   bq show \
       --project_id=PROJECT_ID \
       --schema \
       --format=prettyjson \
       DATASET_ID.TABLE_ID > SCHEMA_FILE.json
   ```
2. 編輯結構定義檔案，將 `dataGovernanceTagsInfo` 物件新增至資料欄。例如：

   ```
   [
     {
       "description": "my sensitive column",
       "mode": "NULLABLE",
       "name": "Column_X",
       "type": "INT64",
       "dataGovernanceTagsInfo": {
         "dataGovernanceTags": {
           "PROJECT_ID/TAG_KEY": "TAG_VALUE"
         }
       }
     },
     {
       "mode": "REQUIRED",
       "name": "column2",
       "type": "FLOAT"
     }
   ]
   ```
3. 更新資料表，使用 `bq
   update` 指令將標記附加至機密資料欄：

   ```
   bq update \
       --project_id=PROJECT_ID \
       --schema=SCHEMA_FILE.json \
       DATASET_ID.TABLE_ID
   ```

   您也可以使用 `bq update` 指令移除現有標記，並附加新標記。

### API

#### 建立含有標記資料欄的新資料表

請使用 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法。在要求主體中加入 `dataGovernanceTagsInfo` 欄位。

```
```json
{
  "schema": {
    "fields": [
      {
        "name": "Column_X",
        "type": "INT64",
        "description": "sensitive column",
        "dataGovernanceTagsInfo": {
          "dataGovernanceTags": {
            "PROJECT_ID/TAG_KEY": "TAG_VALUE"
          }
        }
      }
    ]
  }
}
```
```

#### 在現有資料表中加入標記

1. 使用 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) 方法擷取目前的資料表資源。
2. 修改表格資源，加入目標資料欄的 `dataGovernanceTagsInfo` 欄位。
3. 使用更新後的資料表資源呼叫 [`tables.update`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/update?hl=zh-tw) 或 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法。

### 建立及管理資料政策

建立及管理參照資料治理標記的 BigQuery 資料政策，套用遮蓋規則或原始資料存取權政策。

為已標記的資料欄建立資料政策後，只有政策中指定的使用者可以存取該資料欄 (前提是他們也具有資料表的存取權)。其他使用者一律無法存取。

#### 建立資料政策

### API

建立使用預先定義`SHA256`遮蓋規則的資料政策，或建立原始資料存取權政策。

##### 使用預先定義的`SHA256`遮蓋規則建立資料政策

如要使用預先定義的 `SHA256` 遮蓋規則建立資料政策，請將 `POST` 要求傳送至 `dataPolicies` 端點：

```
curl --request POST \
    "https://bigquerydatapolicy.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/dataPolicies" \
    --header "Authorization: Bearer $(gcloud auth print-access-token)" \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/json' \
    --data '{"dataPolicy":{"dataPolicyType":"DATA_MASKING_POLICY","dataMaskingPolicy":{"predefinedExpression":"SHA256"},"grantees": ["principal://goog/subject/EMAIL_ADDRESS"],"dataGovernanceTag":{"key":"PROJECT_ID/TAG_KEY","value":"TAG_VALUE"}},"dataPolicyId":"POLICY_ID"}' \
    --compressed
```

更改下列內容：

* `PROJECT_ID`：專案的 ID。 Google Cloud如要提供機構而非專案做為代碼的父項，請改用 `ORGANIZATION_ID` 格式 (`ORGANIZATION_ID/TAG_KEY`) 的 `dataGovernanceTag.key`。
* `LOCATION`：要建立資料政策的區域。詳情請參閱「[資料政策位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#data-policy-locations)」。
* `EMAIL_ADDRESS`：要授予存取權的使用者電子郵件地址。
* `TAG_KEY`：標記鍵的簡稱。
* `TAG_VALUE`：使用者指定的標記值簡稱。
* `POLICY_ID`：資料政策的 ID。

##### 建立原始資料存取權政策

如要建立原始資料存取權政策，請將 `dataPolicyType` 設為
`RAW_DATA_ACCESS_POLICY`：

```
curl --request POST \
    "https://bigquerydatapolicy.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/dataPolicies" \
    --header "Authorization: Bearer $(gcloud auth print-access-token)" \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/json' \
    --data '{"dataPolicy":{"dataPolicyType":"RAW_DATA_ACCESS_POLICY","grantees": ["principal://goog/subject/EMAIL_ADDRESS"],"dataGovernanceTag":{"key":"PROJECT_ID/TAG_KEY","value":"TAG_VALUE"}},"dataPolicyId":"POLICY_ID"}' \
    --compressed
```

#### 更新資料政策

更新現有資料政策，授予其他使用者存取權。

### API

1. 如要直接更新政策來新增使用者，請先取得目前的政策和 `etag`：

   ```
   curl --request GET \
       "https://bigquerydatapolicy.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/dataPolicies/POLICY_ID" \
       --header "Authorization: Bearer $(gcloud auth print-access-token)" \
       --header 'Accept: application/json' \
       --header 'Content-Type: application/json' \
       --compressed
   ```
2. 使用更新後的受贈者清單和上一步的 `etag`，傳送 `PATCH` 要求：

   ```
   curl -X PATCH \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "Content-Type: application/json" \
     -d '{
       "grantees": ["principal://goog/subject/user1@example.com","principal://iam.googleapis.com/projects/-/serviceAccounts/SA_EMAIL_ADDRESS"],
       "etag": "ETAG"
     }'  \
   "https://bigquerydatapolicy.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/dataPolicies/POLICY_ID?updateMask=grantees"
   ```

   將 `ETAG` 換成上一步中 `GET` 要求傳回的 `etag` 值。

   或者，您也可以使用 `addGrantees` 方法將使用者新增至政策：

   ```
   curl -X POST \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "Content-Type: application/json" \
     -d '{
       "grantees": ["principal://goog/subject/user1@example.com","principal://iam.googleapis.com/projects/-/serviceAccounts/SA_EMAIL_ADDRESS"]
     }'  \
   "https://bigquerydatapolicy.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/dataPolicies/POLICY_ID:addGrantees"
   ```
3. 如要從政策中移除使用者，請使用 `removeGrantees` 方法：

   ```
   curl -X POST \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "Content-Type: application/json" \
     -d '{
       "grantees": ["principal://goog/subject/user1@example.com","principal://iam.googleapis.com/projects/-/serviceAccounts/SA_EMAIL_ADDRESS"]
     }'  \
   "https://bigquerydatapolicy.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/dataPolicies/POLICY_ID:removeGrantees"
   ```

#### 刪除資料政策

### API

如要刪除資料政策，請向 `dataPolicies` 端點傳送 `DELETE` 要求：

```
curl --request DELETE \
"https://bigquerydatapolicy.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/dataPolicies/POLICY_ID" \
--header "Authorization: Bearer $(gcloud auth print-access-token)" \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--compressed
```

#### 列出資料政策

### API

如要列出參照代碼鍵的資料政策，請使用 `filter` 參數，將 `GET` 要求傳送至 `dataPolicies` 端點：

```
curl --request GET \
"https://bigquerydatapolicy.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/dataPolicies?filter=dataGovernanceTag:PROJECT_ID/TAG_KEY" \
--header "Authorization: Bearer $(gcloud auth print-access-token)" \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--compressed
```

### 與其他功能的互動

本節說明資料治理標記如何與其他 BigQuery 功能互動。

| 功能 | 互動 |
| --- | --- |
| 資訊結構定義 | 附加至資料欄的資料治理標記會納入 `INFORMATION_SCHEMA.COLUMNS` 和 `INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` 檢視畫面。 |
| 資料表複製 | 如果資料表具有資料欄層級安全性功能，包括含有資料治理標記的資料表，系統會停用跨區域資料表副本。 |
| 時間回溯 | 存取歷來資料表資料時，須遵守附加至資料表的存取政策和標記。 |

### 設定預設資料政策專案

存取受資料治理標記保護的資料欄時，BigQuery 預設只會評估資料表所在專案中的資料政策。除非管理員在機構層級設定預設資料政策專案，否則其他專案中定義的資料政策不適用。

如果為貴機構設定了預設資料政策專案，BigQuery 在判斷資料欄存取權時，會同時評估資料表專案和預設資料政策專案的資料政策。

如果使用者同時受到資料表專案和預設資料政策專案中相衝突的資料政策限制，系統會優先採用資料表專案中的資料政策。

如要使用 DDL 或 `INFORMATION_SCHEMA` 檢視表，在機構層級設定或查看 `default_data_policy_projects` 選項，請參閱預設設定文件中的「[資料管理設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#data-management-settings)」。

### 資料治理標記的限制

* BigQuery Omni 資料表不支援資料欄的資料治理標記。
* 您可以使用 Google Cloud 控制台查看資料欄的資料治理標記，但無法繫結或取消繫結。
* 每個資料欄可繫結一個標記，每個資料表最多可繫結 1,000 個不重複的標記。
* 如果您使用 BigQuery Storage Read API、`tabledata.list` 呼叫或萬用字元資料表查詢已標記的資料欄，除非資料政策授予您存取權，否則會收到存取遭拒錯誤。
* 如果是 `STRUCT` 欄位，您只能將資料治理標記套用至葉節點欄位。
* 您可以刪除附加至資料欄的標記值。如果刪除標記值，系統會保留資料欄的標記繫結，但由於標記值已不存在，您可能會無法存取該資料欄。

### 排解資料治理標記問題

本節說明如何排解使用資料治理標記控管欄存取權時的常見問題。

#### 代碼名稱格式有誤

建立標記時，您會定義簡稱 (例如 `ssn`)。不過，將標記附加至結構定義中的資料欄，或在條件中使用標記時，標記鍵必須採用命名空間格式 (`PROJECT_ID/TAG_KEY` 或 `ORGANIZATION_ID/TAG_KEY`)，標記值則仍使用簡稱。如果只提供標記鍵的簡稱，會產生 `Invalid tagKey` 或 `Invalid
tagValue` 錯誤。

#### 跨專案套用政策

根據預設，系統只會評估資料表專案的資料政策。
除非在機構層級設定預設資料政策專案，否則其他專案的政策不會套用。如要進一步瞭解如何設定及評估跨專案政策，請參閱「[設定預設資料政策專案](#configure-default-data-policy-project)」。

## 後續步驟

* 如要查看 Google Cloud中的代碼總覽，請參閱「[代碼總覽](https://docs.cloud.google.com/resource-manager/docs/tags/tags-overview?hl=zh-tw)」。
* 如要進一步瞭解如何使用標記，請參閱[建立及管理標記](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw)。
* 進一步瞭解[如何對資料欄套用政策](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)。
* 如要瞭解如何使用 IAM 條件控管 BigQuery 資源的存取權，請參閱「[使用 IAM 條件控管存取權](https://docs.cloud.google.com/bigquery/docs/conditions?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-07-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-07-16 (世界標準時間)。"],[],[]]