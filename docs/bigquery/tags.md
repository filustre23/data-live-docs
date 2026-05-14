Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 為資料表、檢視表和資料集加上標籤

本文說明如何使用標記，有條件地將[身分與存取權管理 (IAM)](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw) 政策套用至 BigQuery 資料表、檢視區塊和資料集。

您也可以使用標記，透過 IAM 政策有條件地[拒絕存取](https://docs.cloud.google.com/iam/docs/deny-access?hl=zh-tw) BigQuery 資料表、檢視區塊和資料集 ([預覽版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。詳情請參閱「[拒絕政策](https://docs.cloud.google.com/iam/docs/deny-overview?hl=zh-tw)」。

標記是可直接附加至資料表、檢視表或資料集的鍵/值組合，或是資料表、檢視表或資料集可從其他[資源](https://docs.cloud.google.com/resource-manager/docs/tags/tags-overview?hl=zh-tw#inheritance)Google Cloud 繼承的鍵/值組合。您可以根據資源是否具備特定標記，有條件地套用政策。舉例來說，您可能會根據條件，將 BigQuery 資料檢視者角色授予任何含有 `environment:dev` 標記的資料集主體。

如要進一步瞭解如何在資源階層中使用標記，請參閱「[標記總覽](https://docs.cloud.google.com/resource-manager/docs/tags/tags-overview?hl=zh-tw)」。 Google Cloud

如要同時授予多個相關 BigQuery 資源的權限 (包括尚未建立的資源)，請考慮使用 [IAM 條件](https://docs.cloud.google.com/bigquery/docs/conditions?hl=zh-tw)。

## 限制

* BigQuery Omni 資料表、隱藏資料集中的資料表或臨時資料表，都不支援資料表標記。BigQuery Omni 資料集不支援資料集標記。此外，BigQuery Omni 中的跨區域查詢，在檢查其他區域的資料表存取權時，不會使用標記。
* 每個資料表或資料集最多可附加 50 個標記。
* 萬用字元查詢中參考的所有資料表，都必須具有完全相同的標記鍵和值。
* 如果使用者對資料集或資料表具有條件式存取權，就無法透過 Google Cloud 控制台修改該資源的權限。您只能透過 bq 工具和 BigQuery API 修改權限。
* BigQuery 以外的部分服務無法正確驗證 IAM 標記條件。如果標記條件為肯定，也就是說，只有當資源具有特定標記時，使用者才能獲得資源的角色，那麼無論資源附加哪些標記，使用者都會遭到拒絕存取。如果標記條件為負值，也就是說，只有在資源*沒有*特定標記時，使用者才能獲得資源的角色，系統就不會檢查標記條件。

  舉例來說，Data Catalog 無法驗證 BigQuery 資料集和資料表的 IAM 標記條件。假設有條件式 IAM 政策，可讓實習生在具有 `employee_type=intern` 標記的資料集上擔任 BigQuery 資料檢視者角色。由於這是正向標記條件，即使資料集有 `employee_type=intern` 標記，實習生也無法在 Data Catalog 中搜尋並查看資料集。如果標記條件變更為負面條件，實習生只能查看「沒有」`employee_type=intern` 標記的資料集，系統就會完全略過檢查，實習生就能查看他們在 BigQuery 中通常無法存取的資料集。

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
| 在資料表或檢視表中附加標籤 | * 資料表或檢視表的 `bigquery.tables.createTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.create` 權限 * 建立資料表或檢視表時附加標記的 `bigquery.tables.create` 權限 * 更新資料表或檢視表時附加標記的 `bigquery.tables.update` 權限 | * 資料表或檢視表的 `bigquery.tables.createTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.create` 權限 |
| 從資料表或檢視畫面移除標記 | * 資料表或檢視表的 `bigquery.tables.deleteTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.delete` 權限 * 更新資料表或檢視表時，移除標記的 `bigquery.tables.update` 權限 | * 資料表或檢視表的 `bigquery.tables.deleteTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.delete` 權限 |
| 將標記附加至資料集 | * 資料集的 `bigquery.datasets.createTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.create` 權限 * `bigquery.datasets.create` 建立資料集時附加標記的權限 * 更新資料集時附加標記的 `bigquery.datasets.update` 權限 | * 資料集的 `bigquery.datasets.createTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.create` 權限 |
| 從資料集中移除標記 | * 資料集的 `bigquery.datasets.deleteTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.delete` 權限 * 更新資料集時移除標記的 `bigquery.datasets.update` 權限 | * 資料集的 `bigquery.datasets.deleteTagBinding` 權限 * 標記值的 `resourcemanager.tagValueBindings.delete` 權限 |

如要在 Google Cloud 控制台中列出標記鍵和鍵值，您需要下列權限：

* 如要列出與上層機構或專案相關聯的標記鍵，您必須在標記鍵的父項層級具備 `resourcemanager.tagKeys.list` 權限，且具備每個標記鍵的 `resourcemanager.tagKeys.get` 權限。如要在 BigQuery 控制台中查看標記鍵清單，請按一下資料集名稱，然後點選「編輯詳細資料」，或按一下資料表或檢視表名稱，然後依序點選「詳細資料」**「編輯詳細資料」**。
* 如要列出與上層機構或專案相關聯的鍵標記值，您需要標記值父項層級的 `resourcemanager.tagValues.list` 權限，以及每個標記值的 `resourcemanager.tagValues.get` 權限。如要在 BigQuery 控制台中查看標記鍵值清單，請按一下資料集名稱，然後點選「編輯詳細資料」，或按一下資料表或檢視名稱，然後依序點選「詳細資料」**>「編輯詳細資料」**。

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
每個資料集最多可附加 50 個標記。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，選取要建立資料集的專案。
4. 依序點按「查看動作」「建立資料集」。more\_vert
5. 輸入新資料集的資訊。詳情請參閱「[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)」。
6. 展開「代碼」部分。

   1. 如要套用現有標籤，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後選擇「目前範圍」，並選取「目前的機構」或「目前的專案」。

         或者，按一下「選取範圍」搜尋資源，或查看目前資源的清單。
      2. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   2. 如要手動輸入新標記，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後依序選擇「手動輸入 ID」>「機構」、「專案」或「標記」。
      2. 如要為專案或機構建立標記，請在對話方塊中輸入 `PROJECT_ID` 或 `ORGANIZATION_ID`，然後按一下「儲存」。
      3. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   3. 選用：如要在表格中新增其他標記，請按一下「新增代碼」，然後按照先前的步驟操作。
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

* `TAG`：要附加至新資料集的標記。多個標記之間以半形逗號分隔。例如：`556741164180/env:prod,myProject/department:sales`。每個標記都必須有[命名空間限定鍵名和值簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)。
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

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

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
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
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
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

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

      1. 按一下「選取範圍」旁的下拉式箭頭，然後選擇「目前範圍」，並選取「目前的機構」或「目前的專案」。

         或者，按一下「選取範圍」搜尋資源，或查看目前資源的清單。
      2. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   2. 如要手動輸入新標記，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後依序選擇「手動輸入 ID」>「機構」、「專案」或「標記」。
      2. 如要為專案或機構建立標記，請在對話方塊中輸入 `PROJECT_ID` 或 `ORGANIZATION_ID`，然後按一下「儲存」。
      3. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   3. 選用：如要在表格中新增其他標記，請按一下「新增代碼」，然後按照先前的步驟操作。
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
  多個標記之間以半形逗號分隔。例如：`556741164180/env:prod,myProject/department:sales`。每個標記都必須有[命名空間限定鍵名和值簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)。
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

下列步驟會列出直接附加至資料集的標記繫結。這些方法不會傳回從父項資源繼承的標記。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。

   標記會顯示在「資料集資訊」部分。

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

### Terraform

使用 `terraform state show` 指令列出資料集的屬性，包括 `resource_tags` 欄位。在資料集 Terraform 設定檔的執行目錄中執行這項指令。

```
terraform state show google_bigquery_dataset.default
```

### API

呼叫 [`datasets.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw)，取得資料集資源。資料集資源包含附加至 `resource_tags` 欄位中資料集的標記。

### 觀看次數

使用 [`INFORMATION_SCHEMA.SCHEMATA_OPTIONS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata-options?hl=zh-tw)。

舉例來說，下列查詢會顯示區域中所有資料集附加的所有標記。這項查詢會傳回資料表，其中包含 `schema_name` (資料集名稱)、`option_name` (一律為 `'tags'`)、`object_type` (一律為 `ARRAY<STRUCT<STRING, STRING>>`) 和 `option_value` 等資料欄，其中包含代表與每個資料集相關聯標記的 `STRUCT` 物件陣列。如果資料集沒有指派的標記，`option_value` 欄會傳回空陣列。

```
SELECT * from region-REGION.INFORMATION_SCHEMA.SCHEMATA_OPTIONS
WHERE option_name='tags'
```

更改下列內容：

* `REGION`：資料集所在的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

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
   * `TAG_KEY_1`：要卸離的第一個標記的[命名空間索引鍵名稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'my-project/env'` 或 `'556741164180/department'`。
   * `TAG_VALUE_1`：要分離的標記值[簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'prod'` 或 `'sales'`。
   * `TAG_KEY_2`：要卸離的第二個標記的命名空間鍵名。
   * `TAG_VALUE_2`：要卸離的第二個標記值簡稱。
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
* `PROJECT_ID`：資料集所在專案的 ID。
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

從資料集的 `resource_tags` 欄位中移除標記，然後使用 `google_bigquery_dataset` 資源套用更新後的設定。

### API

呼叫 [`datasets.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw)，取得資料集資源，包括 `resource_tags` 欄位。從 `resource_tags` 欄位移除標記，並使用 [`datasets.update` 方法傳回更新後的資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/update?hl=zh-tw)。

## 標記資料表

以下各節說明如何將標記附加至新資料表和現有資料表、列出附加至資料表的標記，以及從資料表卸離標記。

### 建立新資料表時附加標記

建立標記後，您可以將其附加至新表格。針對任何指定的標記鍵，您只能將一個標記值附加至表格。每個表格最多可附加 50 個標記。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 add\_box「建立資料表」。
5. 輸入新資料表的資訊。詳情請參閱「[建立及使用資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)」。
6. 展開「代碼」部分。

   1. 如要套用現有標籤，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後選擇「目前範圍」，並選取「目前的機構」或「目前的專案」。

         或者，按一下「選取範圍」搜尋資源，或查看目前資源的清單。
      2. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   2. 如要手動輸入新標記，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後依序選擇「手動輸入 ID」>「機構」、「專案」或「標記」。
      2. 如要為專案或機構建立標記，請在對話方塊中輸入 `PROJECT_ID` 或 `ORGANIZATION_ID`，然後按一下「儲存」。
      3. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   3. 選用：如要在表格中新增其他標記，請按一下「新增代碼」，然後按照先前的步驟操作。
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
* `PROJECT_ID`：您要建立資料表的專案 ID。
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

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

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
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
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
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

使用已定義的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)。在 `resource_tags` 欄位中加入標記。

### 將標記附加至現有資料表

建立標記後，即可附加至現有資料表。針對任何指定的標記鍵，您只能將一個標記值附加至表格。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」。
4. 依序點選「總覽」**>「表格」**，然後選取所需表格。
5. 按一下「詳細資料」分頁標籤，然後點選「編輯詳情」mode\_edit。
6. 展開「代碼」部分。

   1. 如要套用現有標籤，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後選擇「目前範圍」，並選取「目前的機構」或「目前的專案」。

         或者，按一下「選取範圍」搜尋資源，或查看目前資源的清單。
      2. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   2. 如要手動輸入新標記，請按照下列步驟操作：

      1. 按一下「選取範圍」旁的下拉式箭頭，然後依序選擇「手動輸入 ID」>「機構」、「專案」或「標記」。
      2. 如要為專案或機構建立標記，請在對話方塊中輸入 `PROJECT_ID` 或 `ORGANIZATION_ID`，然後按一下「儲存」。
      3. 針對「Key 1」和「Value 1」，請從清單中選擇適當的值。
   3. 選用：如要在表格中新增其他標記，請按一下「新增代碼」，然後按照先前的步驟操作。
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

以下範例使用 `+=` 運算子將標記附加至資料表，而不覆寫現有標記。如果現有標記的鍵相同，系統會覆寫該標記。

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

### 列出附加至資料表的代碼

您可以列出直接附加至資料表的標記。這個程序不會列出從父項資源繼承的標記。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」。
4. 依序點選「總覽」**>「表格」**，然後選取所需表格。

   標記會顯示在「詳細資料」分頁中。

### bq

使用 [`bq show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show)，然後尋找 `tags` 欄。如果表格中沒有任何代碼，就不會顯示 `tags` 欄。

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

### Terraform

使用 `terraform state show` 指令列出資料表的屬性，包括 `resource_tags` 欄位。在表格的 Terraform 設定檔執行所在目錄中，執行這項指令。

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

### 從資料表取消連結標記

如要從資料表移除標記關聯，請刪除標記繫結。
如要刪除標記，必須先將標記從表格卸離，才能刪除。詳情請參閱「[刪除代碼](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw#deleting)」。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」。
4. 依序點選「總覽」**>「表格」**，然後選取所需表格。
5. 按一下「詳細資料」分頁標籤，然後點選「編輯詳情」mode\_edit。
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
   * `TAG_KEY_1`：要卸離的第一個標記的[命名空間索引鍵名稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'my-project/env'` 或 `'556741164180/department'`。
   * `TAG_VALUE_1`：要分離的標記值[簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，例如 `'prod'` 或 `'sales'`。
   * `TAG_KEY_2`：要卸離的第二個標記的命名空間鍵名。
   * `TAG_VALUE_2`：要卸離的第二個標記值簡稱。
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

* `TAG_KEYS`：要從資料表卸離的標記鍵，以半形逗號分隔。例如：`556741164180/env,myProject/department`。每個標記鍵都必須有[命名空間鍵名](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)。
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

從資料表的 `resource_tags` 欄位中移除標記，然後使用 `google_bigquery_table` 資源套用更新後的設定。

### API

使用已定義的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.update` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/update?hl=zh-tw)，然後移除 `resource_tags` 欄位中的標記。如要移除所有標記，請移除 `resource_tags` 欄位。

## 標記其他類似表格的資源

您也可以為 BigQuery 檢視表、具體化檢視表、副本和快照加上標記。

## 刪除標記

如果資料表、檢視區塊或資料集參照標記，您就無法刪除標記。刪除標記鍵或值本身之前，請先取消所有現有標記繫結資源的連結。如要刪除標記鍵和標記值，請參閱「[刪除標記](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw#deleting)」。

## 範例

假設您是機構管理員，您的資料分析師都是群組 analysts@example.com 的成員，該群組在專案 `userData` 中具有 BigQuery 資料檢視者 IAM 角色。公司聘用了一位資料分析實習生，根據公司政策，這位實習生只能在 `userData` 專案中查看 `anonymousData` 資料集。您可以使用標記控管存取權。

1. [建立標記](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw#creating_tag)，鍵為 `employee_type`，值為 `intern`：
2. 前往 Google Cloud 控制台的「IAM」(身分與存取權管理) 頁面。

   [前往「IAM」(身分與存取權管理) 頁面](https://console.cloud.google.com/iam-admin/iam?hl=zh-tw)
3. 找出要限制資料集存取權的實習生，然後點選該列中的「Edit principal」(編輯主體)edit。
4. 在「角色」選單中，選取「BigQuery 資料檢視者」。
5. 按一下「新增條件」。
6. 在「Title」(標題) 和「Description」(說明) 欄位中，輸入說明要建立的 IAM 標記條件的值。
7. 在「條件建構工具」分頁中，按一下「新增」。
8. 在「條件類型」選單中，依序選取「資源」和「標記」。
9. 在「運算子」選單中，選取「有值」。
10. 在「Value path」(值路徑) 欄位中，以
    `ORGANIZATION/TAG_KEY/TAG_VALUE`. 形式輸入標記值路徑。例如：`example.org/employee_type/intern`。

    這項 IAM 標記條件會限制實習生只能存取具有 `intern` 標記的資料集。
11. 如要儲存代碼條件，請按一下「儲存」。
12. 如要儲存您在「編輯權限」窗格中所做的變更，請按一下「儲存」。
13. 如要將 `intern` 標記值附加至 `anonymousData` 資料集，請使用指令列執行 `gcloud resource-manager tags bindings create` 指令。例如：

    ```
    gcloud resource-manager tags bindings create \
        --tag-value=tagValues/4567890123 \
        --parent=//bigquery.googleapis.com/projects/userData/datasets/anonymousData \
        --location=US
    ```

## 後續步驟

* 如要查看 Google Cloud中的代碼總覽，請參閱「[代碼總覽](https://docs.cloud.google.com/resource-manager/docs/tags/tags-overview?hl=zh-tw)」。
* 如要進一步瞭解如何使用標記，請參閱[建立及管理標記](https://docs.cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing?hl=zh-tw)。
* 如要瞭解如何使用 IAM 條件控管 BigQuery 資源的存取權，請參閱「[使用 IAM 條件控管存取權](https://docs.cloud.google.com/bigquery/docs/conditions?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]