Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理工作負載指派項目

BigQuery Reservation API 可讓您購買專用運算單元 (稱為「[承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)」)、建立運算單元集區 (稱為「[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations)」)，以及將專案、資料夾和組織指派給這些預留項目。

本文說明如何為組織、資料夾、專案和個別主體建立、尋找、移動及刪除預留項目指派作業。此外，也會說明如何執行工作，例如設定專案上限和排定政策覆寫。詳情請參閱「[瞭解預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)」。

## 建立預留項目指派作業

如要使用購買的運算單元，請建立*指派作業*，將專案、資料夾、組織或主體指派給運算單元預留項目。您無法在指派層級指派或分配特定數量的運算單元，運算單元是在預留項目層級管理及指派。

**注意：**指派對象和預留項目必須位於相同組織和位置。如果建立指派作業後，將指派對象移至其他組織，[預留項目監控](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)就會不準確。

### 指派邏輯和條件

專案會使用資源階層中最具體的單一預留項目。BigQuery 會使用下列評估邏輯來選取正確的預留項目：

1. **資源階層優先順序：**BigQuery 會根據被指派者資源上層結構 (專案 > 資料夾 > 組織) 評估指派項目。資料夾和組織指派作業不適用於[標準版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)預留項目。
2. **使用 `principal` 屬性指派使用者專屬作業 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：**BigQuery 預留項目指派作業支援選用的 `principal` 屬性，管理員可根據執行工作的服務帳戶或使用者身分，將查詢轉送至特定預留項目。在特定被指派者資源中，主體相符的指派作業優先順序高於未設定主體的一般指派作業。

   每個專案的使用者專屬指派項目數量預設上限為 100 個。如需變更預設限制的協助，請與 [bigquery-wlm-feedback@google.com](mailto:bigquery-wlm-feedback@google.com) 聯絡。

   **提示：**如要確保特定使用者能正確轉送，不受專案層級的一般指派影響，請在該專案層級建立另一個使用者專屬指派。

如要為預留項目建立指派作業，預留項目必須至少符合下列其中一項條件：

* 已設定非零的指派基準運算單元數量。
* 設定的自動調度運算單元數量不為零。
* 設為使用閒置的運算單元，且專案中有可用的閒置運算單元。

如果您嘗試將資源指派給不符合上述任一條件的預留項目，會收到下列訊息：`Assignment is pending, your project will be executed as on-demand.`

您可以將資源指派給[容錯移轉預留項目](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)，但指派作業會在次要位置中暫停。

### 所需權限

如要建立預留項目指派作業，您必須具備下列 Identity and Access Management (IAM) 權限：

* [管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)和被指派者的 `bigquery.reservationAssignments.create`。

下列各項預先定義的 IAM 角色都包含這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

如要進一步瞭解 BigQuery 的 IAM 角色，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 將組織指派給預留項目

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 按一下「Reservations」(預留項目) 分頁標籤。
4. 在預留項目表格中找出預留項目。
5. 展開 more\_vert「Actions」(動作) 選項。
6. 按一下「建立作業」。
7. 在「Create an assignment」(建立指派作業) 部分，按一下「Browse」(瀏覽)。
8. 瀏覽或搜尋機構，並選取所需項目。
9. 在「Job Type」(工作類型) 部分，選取要指派給這項預留項目的工作類型。您可以使用的選項包括：

   * `QUERY`
   * `CONTINUOUS`
   * `PIPELINE`
   * `BACKGROUND`
   * `ML_EXTERNAL`

   如要進一步瞭解工作類型，請參閱「[預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)」。預設值為 `QUERY`。

   如要進一步瞭解如何允許使用者透過 Enterprise Plus 版指派項目使用 Gemini in BigQuery，請參閱「[設定 Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)」。
10. 選用：在「User」(使用者) 欄位中，輸入使用者、服務帳戶或第三方身分的電子郵件地址。
11. 點選「建立」。

### SQL

如要將組織指派給預留項目，請使用 [`CREATE ASSIGNMENT` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_assignment_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE ASSIGNMENT
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME.ASSIGNMENT_ID`
   OPTIONS (
     assignee = 'organizations/ORGANIZATION_ID',
     job_type = 'JOB_TYPE',
     principal = 'PRINCIPAL');
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) 專案 ID
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `RESERVATION_NAME`：預留項目名稱
   * `ASSIGNMENT_ID`：作業 ID

     ID 在專案和位置中不得重複，開頭和結尾須為小寫英文字母或數字，且只能使用小寫英文字母、數字和破折號。
   * `ORGANIZATION_ID`：[組織 ID](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw#retrieving_your_organization_id)
   * `JOB_TYPE`：要指派給這項預留項目的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`
   * 選用：`PRINCIPAL`：指定使用者、服務帳戶或第三方身分的身分格式

     `principal` 欄位僅支援下列 [IAM 主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw) 格式：

     + Google 帳戶
     + 服務帳戶
     + 工作團隊身分集區中的單一身分
     + workload identity pool 中的單一身分
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要將組織的工作指派給預留項目，請使用 `bq mk` 指令，並加上 `--reservation_assignment` 旗標：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --reservation_id=RESERVATION_NAME \
    --assignee_type=ORGANIZATION \
    --assignee_id=ORGANIZATION_ID \
    --job_type=JOB_TYPE \
    --principal=PRINCIPAL
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱
* `ORGANIZATION_ID`：[組織 ID](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw#retrieving_your_organization_id)
* `JOB_TYPE`：要指派給這項預留項目的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`
* 選用：`PRINCIPAL`：指定使用者、服務帳戶或第三方身分的身分格式。

  `--principal` 旗標僅支援下列 [IAM 主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw) 格式：

  + Google 帳戶
  + 服務帳戶
  + 工作團隊身分集區中的單一身分
  + workload identity pool 中的單一身分

建立預留項目指派作業後，請至少等待 5 分鐘再執行查詢。否則，系統可能會依據隨選定價模式收取查詢費用。

### 設定專案上限和排程政策覆寫

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bigquery-wlm-feedback@google.com](mailto:bigquery-wlm-feedback@google.com)。

您可以建立專案上限 (一種指派規則)，為預留項目的預設[排程政策](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#scheduling-policies)設定專案專屬覆寫值。舉例來說，您可以限制專案的運算單元用量和並行查詢數量。

其他類型的預留項目指派作業會決定專案使用的預留項目，而專案上限則是僅控管特定專案排程行為的指派資源。

建立專案上限時，須遵守下列限制：

* *指派對象*必須是 Google Cloud 專案。不支援資料夾和組織。
* *工作類型*必須取消設定，或明確設為 `JOB_TYPE_UNSPECIFIED`。
* `max_slots` 政策值變更後，必須先啟動新的查詢，更新才會生效。
* 專案層級的運算單元消耗量上限不會強制套用至 `ML_EXTERNAL` 工作的訓練階段。詳情請參閱「[將運算單元指派給 BigQuery ML 工作負載](#assign-ml-workload)」。

如要透過這些排程政策指派作業建立專案上限，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，依序前往**「Administration」(管理) >「Workload
   management」(工作負載管理)**。
3. 按一下「指派規則」分頁標籤。
4. 按一下「建立指派規則」。
5. 在「Rule type」(規則類型) 清單中，選取「Project cap」(專案上限)。
6. 在「Select a project」(選取專案) 清單中選取專案，然後按一下「Continue」(繼續)。
7. 在「Reservation」(預留項目) 清單中選取預留項目，然後按一下「Continue」(繼續)。
8. 在「Project override」(專案覆寫) 區段中，在「Max slots」(運算單元數量上限) 和「Max concurrency」(並行數量上限) 欄位中輸入值。
9. 點選「建立」。

### SQL

如要建立專案排程政策指派作業，請使用 `CREATE
ASSIGNMENT` DDL 陳述式，並搭配 `scheduling_policy_max_slots` 和 `scheduling_policy_concurrency` 選項。

```
CREATE ASSIGNMENT
  `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME.ASSIGNMENT_ID`
OPTIONS (
  assignee = 'projects/PROJECT_ID',
  scheduling_policy_max_slots = MAX_SLOTS,
  scheduling_policy_concurrency = MAX_CONCURRENCY);
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱
* `ASSIGNMENT_ID`：作業 ID
* `PROJECT_ID`：指派的 Google Cloud 專案 ID
* `MAX_SLOTS`：專案中執行查詢的運算單元用量上限
* `MAX_CONCURRENCY`：：專案允許同時執行的查詢數量
  上限

### bq

如要使用 `bq` 指令列工具建立排程政策指派作業，請使用 `bq mk` 指令，並加上 `--scheduling_policy_max_slots` 和 `--scheduling_policy_concurrency` 旗標。

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --reservation_id=RESERVATION_NAME \
    --assignee_id=PROJECT_ID \
    --assignee_type=PROJECT \
    --scheduling_policy_max_slots=MAX_SLOTS \
    --scheduling_policy_concurrency=MAX_CONCURRENCY
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱
* `PROJECT_ID`：指派的 Google Cloud 專案 ID
* `MAX_SLOTS`：專案中執行查詢的運算單元用量上限
* `MAX_CONCURRENCY`：：專案允許同時執行的查詢數量
  上限

如要修改或移除現有的排程政策指派作業，請使用 `ALTER ASSIGNMENT` DDL 陳述式：

```
ALTER ASSIGNMENT
  `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME.ASSIGNMENT_ID`
SET OPTIONS (
  scheduling_policy_max_slots = NEW_MAX_SLOTS,
  scheduling_policy_concurrency = NEW_MAX_CONCURRENCY);
-- To remove a scheduling policy setting, set its values to null. To all
   settings, delete the assignment.
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱
* `ASSIGNMENT_ID`：作業 ID
* `NEW_MAX_SLOTS`：專案中執行查詢的運算單元用量上限
* `NEW_MAX_CONCURRENCY`：：專案允許同時執行的查詢數量
  上限

如要查看有效的排程政策覆寫，請查看 `INFORMATION_SCHEMA.ASSIGNMENTS` 檢視畫面中的 `scheduling_policy` 和 `assignment_type` 欄。

### 將專案或資料夾指派給預留項目

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 按一下「Reservations」(預留項目) 分頁標籤。
4. 在預留項目表格中找出預留項目。
5. 展開 more\_vert「Actions」(動作) 選項。
6. 按一下「建立作業」。
7. 在「Create an assignment」(建立指派作業) 部分，按一下「Browse」(瀏覽)。
8. 瀏覽或搜尋專案或資料夾，然後選取所需項目。
9. 在「Job Type」(工作類型) 部分，選取要指派給這項預留項目的工作類型。您可以使用的選項包括：

   * `QUERY`
   * `CONTINUOUS`
   * `PIPELINE`
   * `BACKGROUND`
   * `ML_EXTERNAL`

   目前無法透過控制台建立及修改更精細的背景工作類型，例如 `BACKGROUND_COLUMN_METADATA_INDEX`。

   如要進一步瞭解工作類型，請參閱「[預留項目指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)」。預設值為 `QUERY`。
10. 選用：在「User」(使用者) 欄位中，輸入使用者、服務帳戶或第三方身分的電子郵件地址。
11. 點選「建立」。

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
     job_type="JOB_TYPE",
     principal="PRINCIPAL");
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) 專案 ID
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `RESERVATION_NAME`：預留項目名稱
   * `ASSIGNMENT_ID`：作業 ID

     ID 在專案和位置中不得重複，開頭和結尾須為小寫英文字母或數字，且只能使用小寫英文字母、數字和破折號。
   * `PROJECT_ID`：要指派給預留項目的專案 ID
   * `JOB_TYPE`：要指派給這項預留項目的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`
   * 選用：`PRINCIPAL`：指定使用者、服務帳戶或第三方身分的身分格式。`principal` 欄位僅支援下列 [IAM 主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw) 格式：

     + Google 帳戶
     + 服務帳戶
     + 工作團隊身分集區中的單一身分
     + workload identity pool 中的單一身分
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要將工作指派給預留項目，請使用 `bq mk` 指令並加上 `--reservation_assignment` 旗標：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --reservation_id=RESERVATION_NAME \
    --assignee_type=PROJECT \
    --assignee_id=PROJECT_ID \
    --job_type=JOB_TYPE \
    --principal=PRINCIPAL
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱
* `PROJECT_ID`：要指派給這項預留項目的專案 ID
* `JOB_TYPE`：要指派給這項預留項目的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`
* 選用：`PRINCIPAL`：指定使用者、服務帳戶或第三方身分的身分格式。

  `--principal` 旗標僅支援下列 [IAM 主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw) 格式：

  + Google 帳戶
  + 服務帳戶
  + 工作團隊身分集區中的單一身分
  + workload identity pool 中的單一身分

### Terraform

使用 [`google_bigquery_reservation_assignment`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_reservation_assignment) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

   這項指令在每個專案中只需執行一次，且可在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確的值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為「根模組」)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱必須有 `.tf` 副檔名，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在進行教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   您也可以從 GitHub 複製程式碼。如果 Terraform 程式碼片段是端對端解決方案的一部分，建議您採用這種做法。
3. 請查看並修改範例參數，以便套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請視需要加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 要建立或更新的資源符合預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台的使用者介面中，前往資源頁面，確認 Terraform 已建立或更新資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

建立預留項目指派作業後，請至少等待 5 分鐘再執行查詢。否則，系統可能會依據隨選定價模式收取查詢費用。

如要建立僅使用[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)的專案，請[建立預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_reservations)並指派 `0` 個運算單元，然後按照上述步驟將專案指派給該預留項目。

**注意：**在單一區域中，一項專案最多只能指派給一個預留項目。

### 使用者專屬作業

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

您可以將預留項目指派給特定主體，例如專案、資料夾或組織中的使用者或服務帳戶。這項功能很實用，可將特定使用者的工作負載轉送至專屬預留項目。

決定要用於工作的預留項目時，BigQuery 會按照下列順序評估指派項目：

1. 評估資源階層，從專案開始，接著是上層資料夾，然後是機構。
2. 在階層的每個層級，BigQuery 會先檢查是否有指派項目與執行工作的特定主體相符。
3. 如果沒有任何指派項目與該層級的主體相符，請檢查是否有不含主體的一般指派項目。
4. 如果找不到指派項目，請移至階層中的下一個層級。

沒有主體的專案層級指派作業，會覆寫有主體的資料夾層級指派作業。

#### 支援的主體格式

`principal` 選項支援下列 [IAM v2 主體](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)格式：

| 身分類型 | 主體格式 |
| --- | --- |
| 使用者 | `principal://goog/subject/EMAIL_ADDRESS` |
| 服務帳戶 | `principal://iam.googleapis.com/projects/-/serviceAccounts/EMAIL_ADDRESS` |
| 員工身分集區身分 | `principal://iam.googleapis.com/locations/global/workforcePools/POOL_ID/subject/SUBJECT_ID` |
| workload identity pool 身分 | `principal://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/subject/SUBJECT_ID` |

**注意：**`unknown_or_deleted_user` 是系統使用的標記值，代表已刪除或停用的使用者帳戶。您無法使用這個值指派預留項目。

#### 將主體指派給預留項目

### SQL

如要建立使用者專屬指派作業，請使用 `CREATE ASSIGNMENT` DDL 陳述式和 `principal` 選項。

```
CREATE ASSIGNMENT
  `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME.ASSIGNMENT_ID`
OPTIONS (
  assignee = 'projects/PROJECT_ID',
  principal = 'principal://goog/subject/EMAIL_ADDRESS',
  job_type = 'QUERY');
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱
* `ASSIGNMENT_ID`：作業 ID
* `PROJECT_ID`：專案 ID
* `EMAIL\_ADDRESS：使用者的電子郵件地址
* `JOB_TYPE`：要指派給這項預留項目的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`

### bq

如要建立使用者專屬指派作業，請使用 `bq mk` 指令搭配 `--principal` 旗標：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --reservation_id=RESERVATION_NAME \
    --assignee_id=PROJECT_ID \
    --assignee_type=PROJECT \
    --principal=PRINCIPAL \
    --job_type=JOB_TYPE
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱
* `ASSIGNMENT_ID`：作業 ID
* `PROJECT_ID`：專案 ID
* `PRINCIPAL: the principal identifier, for example,`principal://goog/subject/EMAIL\_ADDRESS`
* `JOB_TYPE`：要指派給這項預留項目的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`

### 將專案指派給 `none`

指派給 `none` 代表沒有指派。指派給 `none` 的專案採用隨選計價模式。

**注意：**只有查詢工作支援指派給 `none`。

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

   替換下列內容：

   * `LOCATION`：應使用以量計價模式的工作[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `ASSIGNMENT_ID`：作業 ID

     ID 在專案和位置中不得重複，開頭和結尾須為小寫英文字母或數字，且只能使用小寫英文字母、數字和破折號。
   * `PROJECT_ID`：要指派給預留項目的專案 ID
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要將專案指派給 `none`，請使用 `bq mk` 指令並加上 `--reservation_assignment` 旗標：

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

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：應使用隨選定價模式的工作[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `PROJECT_ID`：要指派給 `none` 的專案 ID

### Terraform

使用 [`google_bigquery_reservation_assignment`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_reservation_assignment) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會將專案指派給 `none`：

```
resource "google_bigquery_reservation_assignment" "default" {
  assignee    = "projects/PROJECT_ID"
  job_type    = "QUERY"
  reservation = "projects/ADMIN_PROJECT_ID/locations/LOCATION/reservations/none"
}
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：應使用隨選定價模式的工作[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `PROJECT_ID`：要指派給 `none` 的專案 ID

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   這項指令在每個專案中只需執行一次，且可在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確的值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為「根模組」)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱必須有 `.tf` 副檔名，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在進行教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   您也可以從 GitHub 複製程式碼。如果 Terraform 程式碼片段是端對端解決方案的一部分，建議您採用這種做法。
3. 請查看並修改範例參數，以便套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請視需要加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 要建立或更新的資源符合預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台的使用者介面中，前往資源頁面，確認 Terraform 已建立或更新資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

如果管理專案中沒有預留項目，則必須使用 bq 指令列工具，查看指派給 `none` 的專案。

### 覆寫查詢的預留項目

如要在查詢中使用特定預留項目，您必須具備下列 Identity and Access Management (IAM) 權限：

* 預留項目或其[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的 `bigquery.reservations.use`。

如要指派查詢在特定預留項目中執行，請執行下列任一操作：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 add\_box「SQL query」(SQL 查詢)。
3. 在查詢編輯器中，輸入有效的 GoogleSQL 查詢。
4. 依序點選「編輯」>「查詢設定」。
5. 取消勾選「Automatic location setting」(自動位置設定) 核取方塊，然後選取預留項目所在的區域或多區域。
6. 在「Reservation」(預留項目) 清單中，選取要執行查詢的預留項目。
7. 按一下「儲存」。
8. [在編輯器分頁中編寫查詢並執行](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)。查詢會在您指定的預留項目中執行。

### SQL

在工作階段中設定 `@@reservation` 系統變數，指派查詢執行的預留項目：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SET @@reservation='RESERVATION';
   SELECT QUERY;
   ```

   更改下列內容：

   * `RESERVATION`：要執行查詢的預留項目。
   * `QUERY`：要執行的查詢。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

舉例來說，下列查詢會使用 [`SET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#set) 陳述式，將預留項目設為 `US` 多區域中的 `test-reservation`，然後呼叫基本查詢：

```
SET @@reservation='projects/project1/locations/US/reservations/test-reservation';
SELECT 42;
```

### bq

1. 在 Google Cloud 控制台啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 控制台底部會開啟 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已設定適用於您目前專案的值。工作階段可能要幾秒鐘的時間才能初始化。
2. 在 Cloud Shell 中，使用 [`bq query` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query)搭配 `--reservation_id` 旗標執行查詢：

   ```
   bq query --use_legacy_sql=false --reservation_id=RESERVATION_ID
   'QUERY'
   ```

   更改下列內容：

   * `RESERVATION_ID`：要執行查詢的預留項目。
   * `QUERY`：查詢的 SQL 陳述式。

   舉例來說，下列查詢會在 `US` 多區域的 `test-reservation` 預留項目中執行：

   ```
   bq query --reservation_id=project1.US:test-reservation 'SELECT 42;'
   ```

### API

如要使用 API 指定預留項目，請[插入新工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)，並填入 `query` 工作設定屬性。在 `reservation` 欄位中指定預留項目。

**注意：**查詢可以使用在其他專案中宣告的預留項目。不過，查詢和預留項目必須位於相同的組織和位置。

### 將運算單元指派給 BigQuery ML 工作負載

下列各節提供 BigQuery ML 模型預留項目指派規定的相關資訊。如要建立這些預留項目指派作業，請按照「[將組織指派給預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-organization)」或「[將專案或資料夾指派給預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign_my_prod_project_to_prod_reservation)」中的程序操作。

#### 外部模型

下列 BigQuery ML 模型類型會使用外部服務：

* [自動編碼器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder?hl=zh-tw)
* [AutoML](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw)
* [提升樹](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
* [深層類神經網路 (DNN)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)
* [隨機森林](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)
* [Wide-and-Deep 網路](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)

如要將預留運算單元指派給使用這些服務的查詢，請建立使用 `ML_EXTERNAL` 工作類型的預留項目指派作業。如果找不到 `ML_EXTERNAL` 工作類型的預留項目指派作業，查詢工作會依[隨選定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)執行。

如果是外部模型訓練工作，預留項目指派作業中的運算單元會用於預先處理、訓練和後續處理步驟。訓練期間，運算單元無法先占，但預先處理和後續處理期間，可以使用閒置的運算單元。

#### 矩陣分解模型

如要建立矩陣分解模型，您必須使用 BigQuery [Enterprise 或 Enterprise Plus 版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)[建立預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_reservations)，然後建立使用 `QUERY` 工作類型的預留項目指派作業。

#### 其他模型類型

如果 BigQuery ML 模型不是外部模型或矩陣分解模型，您可以建立使用 `QUERY` 工作類型的預留項目指派作業，將預留運算單元指派給使用這些服務的查詢。如果找不到工作類型為 `QUERY` 的預留項目指派作業，查詢工作會採用[隨選計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。

## 查看預留項目指派作業

### 所需權限

如要搜尋特定專案、資料夾或組織的預留項目指派作業，您必須具備下列 Identity and Access Management (IAM) 權限：

* 管理專案的 `bigquery.reservationAssignments.list`。

下列各項預先定義的 IAM 角色都包含這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`
* `BigQuery Resource Viewer`
* `BigQuery User`

如要進一步瞭解 BigQuery 的 IAM 角色，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 找出專案的預留項目指派作業

如要查看是否已將專案、資料夾或機構指派給保留項目，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 按一下「Reservations」(預留項目) 分頁標籤。
4. 在預留項目表格中，展開預留項目即可查看指派給該預留項目的資源，或使用「Filter」(篩選器) 欄位依資源名稱篩選。

### SQL

如要找出專案查詢工作指派給哪個預留項目，請查詢 [`INFORMATION_SCHEMA.ASSIGNMENTS_BY_PROJECT` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw#schema)。

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

   替換下列內容：

   * `LOCATION`：要查看的預留項目[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) 專案 ID
   * `PROJECT_ID`：要指派給預留項目的專案 ID
   * `JOB_TYPE`：要指派給這項預留項目的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

**注意：**這個指令無法在 Cloud Shell 執行。如要使用這個指令，請從本機指令列執行。

如要查看專案的查詢工作指派給哪項預留項目，請使用 `bq show` 指令並加上 `--reservation_assignment` 旗標：

```
bq show \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --job_type=JOB_TYPE \
    --assignee_id=PROJECT_ID \
    --assignee_type=PROJECT
```

如要尋找使用者專屬指派項目，請加入 `--principal` 旗標：

```
bq show \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --job_type=JOB_TYPE \
    --assignee_id=PROJECT_ID \
    --assignee_type=PROJECT \
    --principal=PRINCIPAL
```

更改下列內容：

* `ADMIN_PROJECT_ID`：預留資源所屬專案的 ID
* `LOCATION`：要查看的預留項目[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `JOB_TYPE`：要指派給這項預留項目的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，例如 `QUERY`、`CONTINUOUS`、`PIPELINE`、`BACKGROUND` 或 `ML_EXTERNAL`
* `PROJECT_ID`：專案 ID
* `PRINCIPAL`：主體 ID，例如 `principal://goog/subject/EMAIL_ADDRESS`

如要查看有效的使用者專屬指派規則，請在 `INFORMATION_SCHEMA.ASSIGNMENTS` 檢視畫面中查看 `principal` 欄，或執行 `bq ls
--reservation_assignment`。此外，您也可以查詢 `INFORMATION_SCHEMA.JOBS` 檢視表，確認哪個預留項目執行了特定工作。使用 `bq show --reservation_assignment` 指令時，您可以加入選用的 `--principal` 旗標，篩選特定使用者指派項目。

## 更新預留項目指派作業

### 將指派項目移至其他預留項目

您可以將指派項目從一個預留項目移至另一個預留項目。

如要移動預留項目指派作業，您必須具備[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)和指派對象的下列 Identity and Access Management (IAM) 權限。

* `bigquery.reservationAssignments.create`
* `bigquery.reservationAssignments.delete`

下列每個預先定義的 IAM 角色都包含這些權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

如要進一步瞭解 BigQuery 的 IAM 角色，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要移動指派作業，請使用 `bq update` 指令：

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --destination_reservation_id=DESTINATION_RESERVATION \
    ADMIN_PROJECT_ID:LOCATION.RESERVATION_NAME.ASSIGNMENT_ID
```

更改下列內容：

* `ADMIN_PROJECT_ID`：預留資源所屬專案的 ID
* `LOCATION`：新預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：要從哪個預留項目移出指派作業
* `DESTINATION_RESERVATION`：要將指派作業移至哪個預留項目
* `ASSIGNMENT_ID`：作業 ID

  如要取得指派作業 ID，請參閱「[列出專案的預留項目指派作業](#list-assignment)」。

**注意：**更新後的預留項目指派作業僅適用於新工作。現有工作會繼續使用原本的預留項目指派作業。

## 可刪除保留項目指派作業

如要從預留項目中移除專案，請刪除預留項目指派作業。如果專案未指派給任何預留項目，則會沿用上層資料夾或組織中的任何指派項目；如果沒有上層指派項目，則會採用隨選定價。

刪除預留項目指派作業時，使用該預留項目中運算單元執行的工作會繼續執行，直到完成為止。

### 所需權限

如要刪除預留項目指派作業，您必須具備下列 Identity and Access Management (IAM) 權限：

* [管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)和被指派者的 `bigquery.reservationAssignments.delete`。

下列各項預先定義的 IAM 角色都包含這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

### 從預留項目中移除專案

如要將專案從保留項目中移除：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 按一下「Reservations」(預留項目) 分頁標籤。
4. 在預留項目表格中，展開預留項目即可找到專案。
5. 展開 more\_vert「Actions」(動作) 選項。
6. 點選「刪除」。

### SQL

使用 [`DROP ASSIGNMENT` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_assignment_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   DROP ASSIGNMENT
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME.ASSIGNMENT_ID`;
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) 專案 ID
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `RESERVATION_NAME`：預留項目名稱
   * `ASSIGNMENT_ID`：作業 ID

     如要找出指派作業 ID，請參閱「[列出專案的預留項目指派作業](#list-assignment)」。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要從預留項目中移除專案，請使用 `bq rm` 指令並加上 `--reservation_assignment` 旗標：

```
bq rm \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment RESERVATION_NAME.ASSIGNMENT_ID
```

更改下列內容：

* `ADMIN_PROJECT_ID`：預留資源所屬專案的 ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱
* `ASSIGNMENT_ID`：作業 ID

  如要取得指派作業 ID，請參閱「[尋找專案的預留項目指派作業](#list-assignment)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-08 (世界標準時間)。"],[],[]]