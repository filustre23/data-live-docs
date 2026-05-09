Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理工作負載指派作業

透過 BigQuery Reservation API，您可以購買專屬運算單元 (稱為「[*承諾*](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)」)、建立運算單元集區 (稱為「[*預留項目*](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations)」)，以及將專案、資料夾和機構指派給這些預留項目。

**注意：** 受讓人和預留項目必須位於同一個機構和位置。如果指派作業建立後，您將受讓人移至其他機構，[預訂監控](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)就會不準確。

## 建立保留項目指派作業

如要使用購買的運算單元，請建立「指派作業」，將專案、資料夾或機構指派給運算單元保留項目。您無法在指派層級指派或分配特定數量的運算單元，運算單元是在預訂層級管理及指派。

專案會使用資源階層中指派給專案的最具體單一預留項目。資料夾指派作業會覆寫機構指派作業，專案指派作業則會覆寫資料夾指派作業。[標準版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)保留項目無法指派資料夾和機構。

如要在預訂項目中建立指派項目，預訂項目必須符合下列至少一項條件：

* 並設定了非零的指派基準運算單元數量。
* 設定的自動調度運算單元數量不為零。
* 已設為使用閒置運算單元，且專案中有可用的閒置運算單元。

如果您嘗試將資源指派給不符合至少一項條件的預訂項目，系統會顯示以下訊息：`Assignment is pending, your project will be executed as on-demand.`

您可以將資源指派給[容錯移轉保留項目](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)，但指派作業會在次要位置處於待處理狀態。

### 所需權限

如要建立預留項目指派作業，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.reservationAssignments.create` [管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)和指派對象的 `bigquery.reservationAssignments.create`。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 將機構指派給預留項目

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「預訂」分頁標籤。
4. 在預訂表格中找出預訂項目。
5. 展開「動作」more\_vert選項。
6. 按一下「建立作業」。
7. 在「建立作業」部分，按一下「瀏覽」。
8. 瀏覽或搜尋機構，然後選取所需項目。
9. 在「Job Type」(工作類型) 區段中，選取要為這項預留項目指派的工作類型。選項包括：

   * `QUERY`
   * `CONTINUOUS`
   * `PIPELINE`
   * `BACKGROUND`
   * `ML_EXTERNAL`

   如要進一步瞭解工作類型，請參閱「[預留指派項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)」。預設值為 `QUERY`。

   如要進一步瞭解如何透過 Enterprise Plus 版指派作業，允許使用者使用 Gemini in BigQuery，請參閱「[設定 Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)」。
10. 點選「建立」。

### SQL

如要將機構指派給預訂項目，請使用 [`CREATE ASSIGNMENT` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_assignment_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE ASSIGNMENT
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME.ASSIGNMENT_ID`
   OPTIONS (
     assignee = 'organizations/ORGANIZATION_ID',
     job_type = 'JOB_TYPE');
   ```

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案擁有預訂資源
   * `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `RESERVATION_NAME`：預留項目名稱
   * `ASSIGNMENT_ID`：指派作業的 ID

     ID 在專案和位置中不得重複，開頭和結尾須為小寫英文字母或數字，只能使用小寫英文字母、數字和破折號。
   * `ORGANIZATION_ID`：[機構 ID](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw#retrieving_your_organization_id)
   * `JOB_TYPE`：要指派給這項預留作業的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要將機構的工作指派給預留項目，請使用 `bq mk` 指令，並加上 `--reservation_assignment` 旗標：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --reservation_id=RESERVATION_NAME \
    --assignee_id=ORGANIZATION_ID \
    --job_type=JOB_TYPE \
    --assignee_type=ORGANIZATION
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預訂資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
* `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預訂名稱
* `ORGANIZATION_ID`：[機構 ID](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw#retrieving_your_organization_id)
* `JOB_TYPE`：要指派給這項預留的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`

建立預訂指派項目後，請等待至少 5 分鐘再執行查詢。否則系統可能會按照以量計價的定價模式計費。

### 將專案或資料夾指派給預留項目

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「預訂」分頁標籤。
4. 在預訂表格中找出預訂項目。
5. 展開「動作」more\_vert選項。
6. 按一下「建立作業」。
7. 在「建立作業」部分，按一下「瀏覽」。
8. 瀏覽或搜尋專案或資料夾，並選取所需項目。
9. 在「Job Type」(工作類型) 區段中，選取要為這項預留項目指派的工作類型。選項包括：

   * `QUERY`
   * `CONTINUOUS`
   * `PIPELINE`
   * `BACKGROUND`
   * `ML_EXTERNAL`

   控制台目前不支援建立及修改更精細的背景工作類型，例如 `BACKGROUND_COLUMN_METADATA_INDEX`。

   如要進一步瞭解工作類型，請參閱「[預留指派項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)」。預設值為 `QUERY`。
10. 點選「建立」。

### SQL

如要將專案指派給預留項目，請使用 [`CREATE ASSIGNMENT` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_assignment_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE ASSIGNMENT
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME.ASSIGNMENT_ID`
   OPTIONS(
     assignee="projects/PROJECT_ID",
     job_type="JOB_TYPE");
   ```

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案擁有預訂資源
   * `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `RESERVATION_NAME`：預留項目名稱
   * `ASSIGNMENT_ID`：指派作業的 ID

     ID 在專案和位置中不得重複，開頭和結尾須為小寫英文字母或數字，只能使用小寫英文字母、數字和破折號。
   * `PROJECT_ID`：要指派給預留項目的專案 ID
   * `JOB_TYPE`：要指派給這項預留的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND_CHANGE_DATA_CAPTURE`、`BACKGROUND_COLUMN_METADATA_INDEX`、`BACKGROUND_SEARCH_INDEX_REFRESH`、`BACKGROUND` 或 `ML_EXTERNAL`
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要將工作指派給預留項目，請使用 `bq mk` 指令並加上 `--reservation_assignment` 旗標：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --reservation_id=RESERVATION_NAME \
    --assignee_id=PROJECT_ID \
    --job_type=JOB_TYPE \
    --assignee_type=PROJECT
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預訂資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
* `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預訂名稱
* `PROJECT_ID`：要指派給這項預留量的專案 ID
* `JOB_TYPE`：要指派給這項預訂的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND_CHANGE_DATA_CAPTURE`、`BACKGROUND_COLUMN_METADATA_INDEX`、`BACKGROUND_SEARCH_INDEX_REFRESH`、`BACKGROUND` 或 `ML_EXTERNAL`

### Terraform

請使用 [`google_bigquery_reservation_assignment`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_reservation_assignment) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會將專案指派給名為 `my-reservation` 的預留項目：

```
resource "google_bigquery_reservation" "default" {
  name              = "my-reservation"
  location          = "us-central1"
  slot_capacity     = 100
  edition           = "ENTERPRISE"
  ignore_idle_slots = false # Use idle slots from other reservations
  concurrency       = 0     # Automatically adjust query concurrency based on available resources
  autoscale {
    max_slots = 200 # Allow the reservation to scale up to 300 slots (slot_capacity + max_slots) if needed
  }
}

data "google_project" "project" {}

resource "google_bigquery_reservation_assignment" "default" {
  assignee    = "projects/${data.google_project.project.project_id}"
  job_type    = "QUERY"
  reservation = google_bigquery_reservation.default.id
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

1. 檢查設定，確認 Terraform 即將建立或更新的資源符合您的預期：

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

建立預訂指派項目後，請等待至少 5 分鐘再執行查詢。否則系統可能會按照以量計價的定價模式計費。

如要建立只使用[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)的專案，請[建立預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_reservations)，並指派 `0` 個運算單元給該預留項目，然後按照先前的步驟將專案指派給該預留項目。

**注意：** 在單一區域中，專案最多只能指派給一個預留項目。

### 將專案指派給 `none`

指派給 `none` 代表沒有指派作業。指派給 `none` 的專案會採用以量計價方案。

**注意：** 僅 QUERY 工作支援指派至 `none`。

### SQL

如要將專案指派給 `none`，請使用 [`CREATE ASSIGNMENT` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_assignment_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE ASSIGNMENT
     `ADMIN_PROJECT_ID.region-LOCATION.none.ASSIGNMENT_ID`
   OPTIONS(
     assignee="projects/PROJECT_ID",
     job_type="QUERY");
   ```

   請替換下列項目：

   * `LOCATION`：應採用以量計價定價的職缺[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `ASSIGNMENT_ID`：指派作業的 ID

     ID 在專案和位置中不得重複，開頭和結尾須為小寫英文字母或數字，只能使用小寫英文字母、數字和破折號。
   * `PROJECT_ID`：要指派給預留項目的專案 ID
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要將專案指派給 `none`，請使用 `bq mk` 指令並加上 `--reservation_assignment` 標記：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --reservation_id=none \
    --job_type=QUERY \
    --assignee_id=PROJECT_ID \
    --assignee_type=PROJECT
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預訂資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
* `LOCATION`：應採用以量計價定價的職缺[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `PROJECT_ID`：要指派給 `none` 的專案 ID

### Terraform

請使用 [`google_bigquery_reservation_assignment`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_reservation_assignment) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會將專案指派給 `none`：

```
data "google_project" "project" {}

resource "google_bigquery_reservation_assignment" "default" {
  assignee    = "projects/${data.google_project.project.project_id}"
  job_type    = "QUERY"
  reservation = "projects/${data.google_project.project.project_id}/locations/us/reservations/none"
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

1. 檢查設定，確認 Terraform 即將建立或更新的資源符合您的預期：

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

如果管理專案中沒有任何預留項目，您就必須使用 bq 指令列工具，查看指派給 `none` 的專案。

### 覆寫查詢的預留項目

如要在查詢中使用特定預留項目，您需要下列 Identity and Access Management (IAM) 權限：

* 預留項目或[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的 `bigquery.reservations.use` 權限。

如要指派查詢在特定預留項目中執行，請執行下列任一操作：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「SQL 查詢」add\_box。
3. 在查詢編輯器中輸入有效的 GoogleSQL 查詢。
4. 按一下「更多」settings，然後按一下「查詢設定」。
5. 清除「自動位置設定」核取方塊，然後選取預留項目所在的區域或多區域。
6. 在「預留項目」清單中，選取要執行查詢的預留項目。
7. 按一下 [儲存]。
8. [在編輯器分頁中編寫查詢並執行](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)。查詢會在您指定的預訂中執行。

### SQL

在工作階段中設定 `@@reservation` 系統變數，指派查詢執行的預留位置：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SET @@reservation='RESERVATION';
   SELECT QUERY;
   ```

   更改下列內容：

   * `RESERVATION`：您希望查詢在其中執行的預留位置。
   * `QUERY`：要執行的查詢。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

舉例來說，下列查詢會使用 [`SET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#set) 陳述式，將 `US` 多區域中的 `test-reservation` 設為預留項目，然後呼叫基本查詢：

```
SET @@reservation='projects/project1/locations/US/reservations/test-reservation';
SELECT 42;
```

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 在 Cloud Shell 中，使用 [`bq query` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query)和 `--reservation_id` 旗標執行查詢：

   ```
   bq query --use_legacy_sql=false --reservation_id=RESERVATION_ID
   'QUERY'
   ```

   更改下列內容：

   * `RESERVATION_ID`：要執行查詢的預留位置。
   * `QUERY`：查詢的 SQL 陳述式。

   舉例來說，下列查詢會在 `US` 多地區的 `test-reservation` 預留項目中執行：

   ```
   bq query --reservation_id=project1.US:test-reservation 'SELECT 42;'
   ```

### API

如要使用 API 指定預留位置，請[插入新工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)，並填入 `query` 工作設定屬性。在 `reservation` 欄位中指定預訂。

**注意：** 查詢可以使用在其他專案中宣告的預留項目。不過，查詢和預留項目必須位於相同組織和位置。

### 將運算單元指派給 BigQuery ML 工作負載

以下各節將說明 BigQuery ML 模型的預留空間指派規定。如要建立這些保留項目指派設定，請按照「[將機構指派給保留項目](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-organization)」或「[將專案或資料夾指派給保留項目](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign_my_prod_project_to_prod_reservation)」中的程序操作。

#### 外部模型

下列 BigQuery ML 模型類型會使用外部服務：

* [自動編碼器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder?hl=zh-tw)
* [AutoML](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw)
* [強化型樹狀結構](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
* [深層類神經網路 (DNN)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)
* [隨機森林](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)
* [廣度和深度網路](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)

如要使用這些服務將保留的時段指派給查詢，請建立使用 `ML_EXTERNAL` 工作類型的預留指派項目。如果系統找不到 `ML_EXTERNAL` 工作類型的預訂指派，查詢工作就會使用[以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)模式執行。

如果是外部模型訓練工作，保留項目指派中的運算單元會用於預先處理、訓練和後續處理步驟。訓練期間無法搶佔這些位置，但預先處理和後續處理期間可以使用閒置位置。

#### 矩陣分解模型

如要建立矩陣分解模型，您必須[建立保留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_reservations)，並使用 BigQuery [Enterprise 或 Enterprise Plus 版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)，然後建立使用 `QUERY` 工作類型的保留項目指派作業。

#### 其他模型類型

如果是外部模型或矩陣因式分解模型以外的 BigQuery ML 模型，您可以建立使用 `QUERY` 工作類型的保留項目指派作業，將保留的運算單元指派給使用這些服務的查詢。如果系統找不到指派的保留項目，且工作類型為 `QUERY`，查詢工作就會採用[依用量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。

## 查看保留項目指派作業

### 所需權限

如要搜尋特定專案、資料夾或機構的保留項目指派作業，您必須具備下列 Identity and Access Management (IAM) 權限：

* 管理專案的 `bigquery.reservationAssignments.list`。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`
* `BigQuery Resource Viewer`
* `BigQuery User`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 尋找專案的預留項目指派作業

如要查看是否已將專案、資料夾或機構指派給保留項目，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「預訂」分頁標籤。
4. 在預訂項目表格中展開預訂項目，即可查看指派給該預訂項目的資源，或使用「篩選」欄位依資源名稱篩選。

### SQL

如要找出專案查詢工作指派的保留項目，請查詢 [`INFORMATION_SCHEMA.ASSIGNMENTS_BY_PROJECT` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw#schema)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
     SELECT
       assignment_id
     FROM `region-LOCATION`.INFORMATION_SCHEMA.ASSIGNMENTS_BY_PROJECT
     WHERE
       assignee_id = 'PROJECT_ID'
       AND job_type = 'JOB_TYPE';
   ```

   請替換下列項目：

   * `LOCATION`：要查看預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案擁有預訂資源
   * `PROJECT_ID`：要指派給預留項目的專案 ID
   * `JOB_TYPE`：要指派給這項預留作業的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

**注意：** 這項指令無法在 Cloud Shell 中執行。如要使用這項指令，請從本機指令列運作執行。

如要找出專案的查詢工作所指派的預留項目，請使用 `bq show` 指令搭配 `--reservation_assignment` 旗標：

```
bq show \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --job_type=JOB_TYPE \
    --assignee_id=PROJECT_ID \
    --assignee_type=PROJECT
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預訂資源的專案 ID
* `LOCATION`：要查看預約記錄的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `JOB_TYPE`：要指派給這項預留的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`
* `PROJECT_ID`：專案 ID

## 可更新保留項目指派作業

### 將指派作業移至其他預訂

您可以將指派作業從一個預訂項目移至另一個預訂項目。

如要移動保留項目指派作業，您必須在[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)和指派對象中，具備下列身分與存取權管理 (IAM) 權限。

* `bigquery.reservationAssignments.create`
* `bigquery.reservationAssignments.delete`

下列預先定義的 IAM 角色都包含這些權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

如要移動作業，請使用 `bq update` 指令：

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --destination_reservation_id=DESTINATION_RESERVATION \
    ADMIN_PROJECT_ID:LOCATION.RESERVATION_NAME.ASSIGNMENT_ID
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預訂資源的專案 ID
* `LOCATION`：新預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：要從中移轉指派作業的預訂
* `DESTINATION_RESERVATION`：要將指派項目移至的預訂
* `ASSIGNMENT_ID`：指派作業的 ID

  如要取得指派 ID，請參閱「[列出專案的預訂指派作業](#list-assignment)」。

**注意：** 更新後的預留項目指派只會套用至新工作。現有工作會繼續使用原始預留項目指派。

## 可刪除保留項目指派作業

如要將專案從保留項目中移除，請刪除保留項目指派作業。如果未將專案指派給任何保留項目，該專案會繼承上層資料夾或機構中的任何指派作業，否則會採用以量計價模式 (如果沒有上層指派作業)。

刪除保留項目指派作業後，使用該保留項目中時段執行的工作會繼續執行，直到完成為止。

### 所需權限

如要刪除預留項目指派作業，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.reservationAssignments.delete` [管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)和指派對象的 `bigquery.reservationAssignments.delete`。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

### 將專案從預訂項目中移除

如要將專案從保留項目中移除：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「預訂」分頁標籤。
4. 在預訂表格中展開預訂項目，找出專案。
5. 展開「動作」more\_vert選項。
6. 點選「刪除」。

### SQL

使用 [`DROP ASSIGNMENT`DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_assignment_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   DROP ASSIGNMENT
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME.ASSIGNMENT_ID`;
   ```

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案擁有預訂資源
   * `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `RESERVATION_NAME`：預留項目名稱
   * `ASSIGNMENT_ID`：指派作業的 ID

     如要尋找指派 ID，請參閱「[列出專案的預訂指派作業](#list-assignment)」。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要從預訂項目中移除專案，請使用 `bq rm` 指令搭配 `--reservation_assignment` 標記：

```
bq rm \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment RESERVATION_NAME.ASSIGNMENT_ID
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預訂資源的專案 ID
* `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預訂名稱
* `ASSIGNMENT_ID`：指派作業的 ID

  如要取得指派 ID，請參閱「[尋找專案的預訂指派作業](#list-assignment)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]