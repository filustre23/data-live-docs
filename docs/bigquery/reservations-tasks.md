Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理工作負載預留項目

BigQuery Reservation API 可讓您購買專用運算單元 (稱為「[*承諾使用合約*](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)」)、建立運算單元集區 (稱為「[*預留項目*](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations)」)，以及將專案、資料夾和組織指派給這些預留項目。

您可以透過預留項目，為工作負載指派專屬的運算單元數量。舉例來說，您可能不希望正式環境工作負載與測試工作負載競爭運算單元。您可以建立名為 `prod` 的預留項目，並將正式環境工作負載指派給這個預留項目。詳情請參閱「[瞭解預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)」。

## 建立預留項目

以下各節說明如何建立預留項目。

### 所需權限

如要建立預留項目，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.reservations.create` 角色，位於保留承諾使用合約擁有權的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)。

下列每個預先定義的 IAM 角色都包含這項權限：

* `BigQuery Resource Editor`
* `BigQuery Resource Admin`

如要進一步瞭解 BigQuery 的 IAM 角色，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 建立具備專屬運算單元的預留項目

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，點選「容量管理」。
3. 點選「Create reservation」(建立預留項目)。
4. 在「Reservation name」(預留項目名稱) 欄位中，輸入預留項目名稱。
5. 在「Location」(位置) 清單中選取位置。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，則只能選擇 Enterprise 版本。
6. 在「Edition」(版本) 清單中選取版本。BigQuery 版本功能 (例如自動調度資源) 僅適用於特定版本。詳情請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
7. 在「Max reservation size selector」(預留項目大小上限選取器) 清單中，選取預留項目大小上限。
8. 選用：在「Baseline slots」(基準運算單元) 欄位中，輸入預留項目的基準運算單元數量。

   可用的自動調度資源運算單元數量，是從「Max reservation size」(預留項目大小上限) 減去「Baseline slots」(基準運算單元) 值。舉例來說，如果您建立的預留項目有 100 個基準運算單元，且預留項目大小上限為 400，則預留項目會有 300 個自動調度資源運算單元。如要進一步瞭解基準運算單元，請參閱「[使用預留項目搭配基準和自動調度資源運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw#using_reservations_with_baseline_and_autoscaling_slots)」。
9. 如要停用[閒置運算單元共用](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)功能，並僅使用指定的運算單元容量，請按一下「Ignore idle slots」(忽略閒置運算單元) 切換鈕。
10. 如要展開「Advanced settings」(進階設定) 部分，請按一下 expand\_more 展開箭頭。
11. 選用：如要設定目標工作並行，請將「Override automatic target job concurrency」(覆寫自動目標工作並行) 切換鈕設為開啟，然後輸入「Target Job Concurrency」(目標工作並行)。
12. 選用：如要設定預留項目的預設專案排程政策，請至少設定下列其中一個選項：

    1. 如要限制指派給預留項目的各項專案可同時執行的查詢數量，請將「Override project concurrency」(覆寫專案並行數量) 切換鈕設為開啟位置，然後在「Project Concurrency」(專案並行數量) 欄位中輸入值。
    2. 如要限制指派給預留項目的各項專案運算單元用量，請將「Override project max slots」(覆寫專案運算單元數量上限) 切換鈕設為開啟，然後在「Project Max Slots」(專案運算單元數量上限) 欄位中輸入值。**注意：** 這些設定會做為指派給預留項目的所有專案的預設值。您可以使用[指派規則](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#scheduling-policy-assignments)，覆寫特定專案的限制。
13. 查看「Cost estimate」(費用預估) 表格中顯示的運算單元明細，以及「Capacity summary」(容量摘要) 表格中的預留項目摘要。
14. 按一下 [儲存]。

新的預留項目會顯示在「Slot reservations」(運算單元預留項目) 分頁中。

### SQL

如要建立預留項目，請使用 [`CREATE RESERVATION` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_reservation_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE RESERVATION
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME`
   OPTIONS (
     slot_capacity = NUMBER_OF_BASELINE_SLOTS,
     edition = EDITION,
     autoscale_max_slots = NUMBER_OF_AUTOSCALING_SLOTS,
     scheduling_policy_max_slots = MAX_SLOTS_PER_PROJECT,
     scheduling_policy_concurrency = MAX_CONCURRENCY_PER_PROJECT);
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) 專案 ID
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，則只能選擇 Enterprise 版本。
   * `RESERVATION_NAME`：預留項目名稱

     名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。
   * `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量。您無法在同一預訂中同時設定 `slot_capacity` 選項和 `standard` 版本選項。
   * `EDITION`：預留項目的版本。支援的值為 `STANDARD`、`ENTERPRISE` 和 `ENTERPRISE_PLUS`。將預留項目指派給版本後，功能和定價會有所變動。詳情請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
   * `NUMBER_OF_AUTOSCALING_SLOTS`：指派給預留項目的自動調度資源運算單元數量。這個值等於預留項目大小上限減去基準運算單元數量。
   * `MAX_SLOTS_PER_PROJECT`：指派給預留項目的各項專案執行查詢時，運算單元用量的預設上限。
   * `MAX_CONCURRENCY_PER_PROJECT`：指派給預留項目的每項專案，可同時執行的查詢數量預設上限。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要建立預留項目，請使用 `bq mk` 指令並加上 `--reservation` 旗標：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation \
    --slots=NUMBER_OF_BASELINE_SLOTS \
    --ignore_idle_slots=false \
    --edition=EDITION \
    --autoscale_max_slots=NUMBER_OF_AUTOSCALING_SLOTS \
    --max_slots=MAXIMUM_NUMBER_OF_SLOTS
    --scaling_mode=SCALING_MODE
    RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，則只能選擇 Enterprise 版本。
* `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量
* `RESERVATION_NAME`：預留項目名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。
* `EDITION`：預留項目的版本。支援的值為 `STANDARD`、`ENTERPRISE` 和 `ENTERPRISE_PLUS`。將預留項目指派給版本後，功能和定價會有所變更。詳情請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
* `NUMBER_OF_AUTOSCALING_SLOTS`：指派給預留項目的自動調度資源運算單元數量。這個值等於預留項目大小上限減去基準運算單元數量。無法使用 `--max_slots` 或 `--scaling_mode` 旗標設定。
* `MAXIMUM_NUMBER_OF_SLOTS`：預留項目可使用的運算單元數量上限。這個值必須使用 `--scaling_mode` 旗標 ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)) 設定。
* `SCALING_MODE`：預留項目的資源調度模式。選項包括 `ALL_SLOTS`、`IDLE_SLOTS_ONLY` 或 `AUTOSCALE_ONLY`。這個值必須使用 `--scaling_mode` 旗標 ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)) 設定。

如要瞭解 `--ignore_idle_slots` 旗標，請參閱「[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)」。預設值為 `false`。

### Terraform

使用 [`google_bigquery_reservation`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_reservation) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會建立名為 `my-reservation` 的預留項目：

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
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   每個專案只需執行這個指令一次，而且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確的值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

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

### Python

使用這個程式碼範例前，請先安裝 [google-cloud-bigquery-reservation 套件](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest?hl=zh-tw)。
建構 [ReservationServiceClient](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient)。使用[預留項目](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.types.Reservation?hl=zh-tw)描述要建立的預留項目。使用 [create\_reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient_create_reservation) 方法建立預留項目。

```
# TODO(developer): Set project_id to the project ID containing the
# reservation.
project_id = "your-project-id"

# TODO(developer): Set location to the location of the reservation.
# See: https://cloud.google.com/bigquery/docs/locations for a list of
# available locations.
location = "US"

# TODO(developer): Set reservation_id to a unique ID of the reservation.
reservation_id = "sample-reservation"

# TODO(developer): Set slot_capicity to the number of slots in the
# reservation.
slot_capacity = 100

# TODO(developer): Choose a transport to use. Either 'grpc' or 'rest'
transport = "grpc"

# ...

from google.cloud.bigquery_reservation_v1.services import reservation_service
from google.cloud.bigquery_reservation_v1.types import (
    reservation as reservation_types,
)

reservation_client = reservation_service.ReservationServiceClient(
    transport=transport
)

parent = reservation_client.common_location_path(project_id, location)

reservation = reservation_types.Reservation(slot_capacity=slot_capacity)
reservation = reservation_client.create_reservation(
    parent=parent,
    reservation=reservation,
    reservation_id=reservation_id,
)

print(f"Created reservation: {reservation.name}")
```

### 建立可預測的預留項目

建立設有[運算單元數量上限](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)的預留項目之前，必須先在管理專案啟用預留項目公平性。2026 年 10 月 10 日後建立的管理專案，預設會啟用以預留項目為基礎的公平性機制。

#### 啟用以預留項目為基礎的公平性機制

如果管理專案是在 2026 年 10 月 10 日前建立，且未啟用預留型公平性，請將 [`enable_reservation_based_fairness` 旗標](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)設為 `true`。

如要更新專案的預留項目公平性，您必須對擁有預留項目的[專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)具備 `bigquery.config.update` 權限。預先定義的 `BigQuery Admin` 角色包含這項權限。

如要進一步瞭解如何更新專案的預設設定，請參閱「[管理配置設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#required_permissions)」。

```
ALTER PROJECT `PROJECT_NAME` SET OPTIONS (
    `region-LOCATION.enable_reservation_based_fairness`= true);
```

更改下列內容：

* PROJECT\_NAME：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID
* LOCATION：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)

#### 建立可預測的預留項目

如要建立設有運算單元數量上限的可預測預留項目，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽面板中，前往「Workload management」(工作負載管理) 專區，然後按一下「Create reservation」(建立預留項目)。
3. 在「Reservation name」(預留項目名稱) 欄位中，輸入預留項目名稱。
4. 在「Location」(位置) 清單中選取位置。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，則只能選擇 Enterprise 版本。
5. 在「Edition」(版本) 清單中選取版本。詳情請參閱「[瞭解 BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」一文。
6. 在「Max reservation size selector」(預留項目大小上限選取器) 清單中，選取預留項目大小上限。
7. 選用：在「Baseline slots」(基準運算單元) 欄位中，輸入預留項目的基準運算單元數量。

   可用的自動調度資源運算單元數量，是從「Max reservation size」(預留項目大小上限) 減去「Baseline slots」(基準運算單元) 值。舉例來說，如果您建立的預留項目有 100 個基準運算單元，且預留項目大小上限為 400，則預留項目會有 300 個自動調度資源運算單元。如要進一步瞭解基準運算單元，請參閱「[使用預留項目搭配基準和自動調度資源運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw#using_reservations_with_baseline_and_autoscaling_slots)」。
8. 如要停用[閒置運算單元共用](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)功能，並僅使用指定的運算單元容量，請按一下「Ignore idle slots」(忽略閒置運算單元) 切換鈕。
9. 如要展開「Advanced settings」(進階設定) 部分，請按一下 expand\_more 展開箭頭。
10. 選用：如要設定預留項目的預設專案排程政策，請設定下列選項：

    * **專案並行數量：**限制這個預留項目中，任意特定專案的執行工作並行數量。
    * **專案運算單元數量上限：**限制這個預留項目中，任何特定專案執行查詢時的運算單元用量。**注意：** 這些設定會做為指派給預留項目的所有專案的預設值。您可以使用[指派規則](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#scheduling-policy-assignments)，覆寫特定專案的限制。
11. 在「How to use idle slots?」(如何使用閒置運算單元？) 清單中，選取設定選項。

    * **最容易預測：**先使用基準運算單元，再使用閒置運算單元，最後使用自動調度資源運算單元，直到達到指定的運算單元數量上限。
    * **較難預測：**只會使用基準和閒置運算單元，最多不超過運算單元數量上限。不會使用自動調度資源運算單元。
    * **變化最大：**使用所有可用的閒置運算單元，擴充至基準數量以上。接著，系統會使用自動調度資源運算單元，直到達到最大值和基準值之間的差額。這可能會導致預留項目超出指定的運算單元數量上限。
12. 「Cost estimate」(費用預估) 表格會顯示運算單元細目。「Capacity summary」(運算能力摘要) 表格會顯示預留項目的摘要。
13. 按一下 [儲存]。

新的預留項目會顯示在「Slot reservations」(運算單元預留項目) 分頁中。

### bq

如要建立可預測的預留項目，請使用 `bq mk` 指令搭配 `--reservation` 旗標，並設定 `max_slots` 和 `scaling_mode` 的值：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation \
    --slots=NUMBER_OF_BASELINE_SLOTS \
    --ignore_idle_slots=false \
    --edition=EDITION \
    --max_slots=MAXIMUM_NUMBER_OF_SLOTS \
    --scaling_mode=SCALING_MODE
    RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，則只能選擇 Enterprise 版本。
* `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量
* `RESERVATION_NAME`：預留項目名稱
* `EDITION`：預留項目的版本。將預留項目指派給版本後，功能和定價會有所變動。詳情請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
* `MAXIMUM_NUMBER_OF_SLOTS`：預留項目可使用的運算單元數量上限。這個值必須使用 `--scaling_mode` 旗標設定。
* `SCALING_MODE`：預留項目的資源調度模式。選項包括 `ALL_SLOTS`、`IDLE_SLOTS_ONLY` 或 `AUTOSCALE_ONLY`。這個值必須使用 `max_slots` 旗標設定。這個值必須與 `ignore_idle_slots` 旗標一致。詳情請參閱「[預留項目的可預測性](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)」。

如要瞭解 `--ignore_idle_slots` 旗標，請參閱「[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)」。預設值為 `false`。

### SQL

如要建立可預測的預留項目，請使用 [`CREATE RESERVATION` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_reservation_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE RESERVATION
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME`
   OPTIONS (
     slot_capacity = NUMBER_OF_BASELINE_SLOTS,
     edition = EDITION,
     ignore_idle_slots = IGNORE_IDLE_SLOTS,
     max_slots = MAX_NUMBER_OF_SLOTS,
     scaling_mode = SCALING_MODE,
     scheduling_policy_max_slots = MAX_SLOTS_PER_PROJECT,
     scheduling_policy_concurrency = MAX_CONCURRENCY_PER_PROJECT);
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID。
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，則只能選擇 Enterprise 版本。
   * `RESERVATION_NAME`：預留項目名稱。名稱只能包含小寫英數字元或破折號，開頭須為英文字母，結尾不得為破折號，長度上限為 64 個字元。
   * `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量。您無法在同一預訂中同時設定 `slot_capacity` 選項和 `standard` 版本選項。
   * `EDITION`：預留項目的版本。將預留項目指派給版本後，功能和定價會有所變動。詳情請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
   * `IGNORE_IDLE_SLOTS`：預留項目是否使用[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)。預設值為 `false`。
   * `MAX_NUMBER_OF_SLOTS`：預留項目可使用的運算單元數量上限。這個值必須使用 `scaling_mode` 選項設定。
   * `SCALING_MODE`：預留項目的資源調度模式。選項包括 `ALL_SLOTS`、`IDLE_SLOTS_ONLY` 或 `AUTOSCALE_ONLY`。這個值必須使用 `max_slots` 選項設定。這個值必須與 `ignore_idle_slots` 選項一致。詳情請參閱「[預留項目的可預測性](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)」。
   * `MAX_SLOTS_PER_PROJECT`：指派給預留項目的各項專案執行查詢時，運算單元用量的預設上限。
   * `MAX_CONCURRENCY_PER_PROJECT`：指派給預留項目的每項專案，可同時執行的查詢數量預設上限。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### Terraform

使用 [`google_bigquery_reservation`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_reservation) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例說明如何建立名為 `my-reservation` 的可預測預留項目群組：

```
resource "google_bigquery_reservation" "default" {
  provider          = google-beta
  name              = "my-reservation"
  location          = "us-central1"
  slot_capacity     = 100
  edition           = "ENTERPRISE"
  ignore_idle_slots = true
  concurrency       = 0 # Automatically adjust query concurrency based on available resources
  max_slots         = 300
  scaling_mode      = "AUTOSCALE_ONLY"
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   每個專案只需執行這個指令一次，而且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確的值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

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

如要進一步瞭解可預測的預留項目，請參閱「[可預測的預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)」。

## 更新預留項目

您可以對預留項目進行下列更新：

* 新增或移除運算單元，變更預留項目大小。
* 設定這個預留項目中的查詢是否使用閒置運算單元。
* 變更分配給預留項目的基準或自動調度資源運算單元數量。
* 設定目標工作並行。

如要變更預留項目的版本，請先[刪除](#delete_reservations)預留項目，然後[建立](#create_reservations)更新版本的預留項目。

### 所需權限

如要更新預留項目，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.reservations.update` 角色，位於保留承諾使用合約擁有權的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)。

下列每個預先定義的 IAM 角色都包含這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

如要進一步瞭解 BigQuery 的 IAM 角色，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 啟用 BigQuery 流暢擴充

如要啟用以秒計費功能，且不設預留項目的最短時間，請在管理專案層級啟用，方法是在 `preflight_fluid_autoscaling_reservations` 選項中列出預留項目。BigQuery 流暢擴充設定的變更可能需要幾分鐘才會生效。

如果預留項目使用[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)，則必須在主要和次要區域啟用 BigQuery 流暢擴充功能，確保在容錯移轉後按秒計費。

如要更新採用 BigQuery 流暢擴充功能的預留項目清單，請修改 `preflight_fluid_autoscaling_reservations` 選項中的清單。如要停用某個區域中所有預留項目的這項功能，請將 `preflight_fluid_autoscaling_reservations` 選項設為 NULL。

### SQL

使用 `ALTER PROJECT SET OPTIONS` 陳述式：

* 如要為預訂清單啟用或更新這項功能，請按照下列步驟操作：

  ```
  ALTER PROJECT `ADMIN_PROJECT_ID`
  SET OPTIONS (
    `region-LOCATION.preflight_fluid_autoscaling_reservations` = ["RESERVATION_NAME"]);
  ```
* 如要為某個區域的所有預留項目停用這項功能，請按照下列步驟操作：

  ```
  ALTER PROJECT `ADMIN_PROJECT_ID`
  SET OPTIONS (
    `region-LOCATION.preflight_fluid_autoscaling_reservations` = NULL);
  ```

更改下列內容：

* `ADMIN_PROJECT_ID`：管理專案的 ID。
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，例如 `us-central1`。
* `RESERVATION_NAME`：要啟用 BigQuery 流暢擴充功能的預留項目名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。

### 變更預留項目的大小

您可以在現有預留項目中新增或移除運算單元。

**注意：** 變更預留項目的運算單元數量上限後，最多可能需要一分鐘才會生效。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 點選「Slot reservations」(運算單元預留項目) 分頁標籤。
4. 找出要更新的預訂。
5. 展開 more\_vert「Actions」(動作) 選項。
6. 按一下 [編輯]。
7. 在「Max reservation size selector」(預留項目大小選取器) 對話方塊中，輸入預留項目大小上限。
8. 在「Baseline slots」(基準運算單元) 欄位中，輸入基準運算單元數量。
9. 如要展開「Advanced settings」(進階設定) 部分，請按一下 expand\_more 展開箭頭。
10. 選用：如要設定目標工作並行，請將「Override automatic target job concurrency」(覆寫自動目標工作並行) 切換鈕設為開啟，然後輸入「Target Job Concurrency」(目標工作並行)。
11. 按一下 [儲存]。

### SQL

如要變更預留項目的大小，請使用 [`ALTER RESERVATION SET OPTIONS` 資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_reservation_set_options_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER RESERVATION
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME`
   SET OPTIONS (
     slot_capacity = NUMBER_OF_BASELINE_SLOTS,
     autoscale_max_slots = NUMBER_OF_AUTOSCALING_SLOTS);
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) 專案 ID
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，例如 `europe-west9`。
   * `RESERVATION_NAME`：預留項目名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。
   * `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量。
   * `NUMBER_OF_AUTOSCALING_SLOTS`：指派給預留項目的自動調度資源運算單元數量。這個值等於預留項目大小上限減去基準運算單元數量。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要更新預留項目的大小，請使用 `bq update` 指令並加上 `--reservation` 旗標：

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --slots=NUMBER_OF_BASELINE_SLOTS \
    --autoscale_max_slots=NUMBER_OF_AUTOSCALING_SLOTS \
    --reservation RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量
* `RESERVATION_NAME`：預留項目名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。
* `NUMBER_OF_AUTOSCALING_SLOTS`：指派給預留項目的自動調度資源運算單元數量。這個值等於預留項目大小上限減去基準運算單元數量。

### Python

使用這個程式碼範例前，請先安裝 [google-cloud-bigquery-reservation 套件](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest?hl=zh-tw)。
建構 [ReservationServiceClient](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient)。使用 [Reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.types.Reservation?hl=zh-tw) 和 [FieldMask.paths](https://googleapis.dev/python/protobuf/latest/google/protobuf/field_mask_pb2.html#google.protobuf.field_mask_pb2.FieldMask.paths) 屬性描述更新後的屬性。使用 [update\_reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient_update_reservation) 方法更新預留項目。

```
# TODO(developer): Set project_id to the project ID containing the
# reservation.
project_id = "your-project-id"

# TODO(developer): Set location to the location of the reservation.
# See: https://cloud.google.com/bigquery/docs/locations for a list of
# available locations.
location = "US"

# TODO(developer): Set reservation_id to a unique ID of the reservation.
reservation_id = "sample-reservation"

# TODO(developer): Set slot_capicity to the new number of slots in the
# reservation.
slot_capacity = 50

# TODO(developer): Choose a transport to use. Either 'grpc' or 'rest'
transport = "grpc"

# ...

from google.cloud.bigquery_reservation_v1.services import reservation_service
from google.cloud.bigquery_reservation_v1.types import (
    reservation as reservation_types,
)
from google.protobuf import field_mask_pb2

reservation_client = reservation_service.ReservationServiceClient(
    transport=transport
)

reservation_name = reservation_client.reservation_path(
    project_id, location, reservation_id
)
reservation = reservation_types.Reservation(
    name=reservation_name,
    slot_capacity=slot_capacity,
)
field_mask = field_mask_pb2.FieldMask(paths=["slot_capacity"])
reservation = reservation_client.update_reservation(
    reservation=reservation, update_mask=field_mask
)

print(f"Updated reservation: {reservation.name}")
print(f"\tslot_capacity: {reservation.slot_capacity}")
```

### 設定查詢是否使用閒置運算單元

`--ignore_idle_slots` 旗標可控管在預留項目中執行的查詢，是否能使用其他預留項目的閒置運算單元。詳情請參閱「[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)」。您可以更新現有預留項目的設定。

如要更新預留項目，請使用 `bq update` 指令並加上 `--reservation` 旗標。以下範例將 `--ignore_idle_slots` 設為 `true`，表示預留項目只會使用分配給預留項目的運算單元。

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --ignore_idle_slots=true \
    --reservation RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。

### 列出閒置運算單元設定

如要列出預留項目的[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)設定，請按照下列步驟操作：

### SQL

查詢 [`INFORMATION_SCHEMA.RESERVATIONS_BY_PROJECT` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw#schema)的 `ignore_idle_slots` 欄。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     reservation_name,
     ignore_idle_slots
   FROM
     `ADMIN_PROJECT_ID.region-LOCATION`.INFORMATION_SCHEMA.RESERVATIONS_BY_PROJECT;
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

請使用 `bq ls` 指令，並加上 `--reservation` 旗標：

```
bq ls --reservation \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)

`ignoreIdleSlots` 欄位包含設定。

## 刪除預留項目

如果刪除預留項目，使用該預留項目運算單元的執行中工作都會失敗。為避免發生錯誤，請先讓執行中的工作完成，再刪除預留項目。

### 所需權限

如要刪除預留項目，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.reservations.delete` 角色，位於保留承諾使用合約擁有權的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)。

下列每個預先定義的 IAM 角色都包含這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

如要進一步瞭解 BigQuery 的 IAM 角色，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

**注意：** 您可以刪除具有有效承諾使用合約的預留項目，但仍須支付合約剩餘期間的費用。刪除預留項目或將相關聯專案切換為隨選計價模式，並不會停止這些費用。如要進一步瞭解承諾使用合約到期，請參閱「[承諾使用合約到期](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#commitment_expiration)」一節。如需預留項目、承諾使用合約或費用的其他協助，請與[Google Cloud 支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)聯絡。

### 刪除預留項目

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 點選「Slot reservations」(運算單元預留項目) 分頁標籤。
4. 找出要刪除的預訂。
5. 展開 more\_vert「Actions」(動作) 選項。
6. 點選「刪除」。
7. 點選「Delete reservation」(刪除預留項目) 對話方塊中的「Delete」(刪除)。

### SQL

如要刪除預留項目，請使用 [`DROP RESERVATION` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_reservation_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   DROP RESERVATION
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME`;
   ```

   替換下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) 專案 ID
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `RESERVATION_NAME`：預留項目 ID
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要刪除預留項目，請使用 `bq rm` 指令並加上 `--reservation` 旗標：

```
bq rm \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。

### Python

使用這個程式碼範例前，請先安裝 [google-cloud-bigquery-reservation 套件](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest?hl=zh-tw)。
建構 [ReservationServiceClient](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient)。使用 [delete\_reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient_delete_reservation) 方法刪除預留項目。

```
# TODO(developer): Set project_id to the project ID containing the
# reservation.
project_id = "your-project-id"

# TODO(developer): Set location to the location of the reservation.
# See: https://cloud.google.com/bigquery/docs/locations for a list of
# available locations.
location = "US"

# TODO(developer): Set reservation_id to a unique ID of the reservation.
reservation_id = "sample-reservation"

# TODO(developer): Choose a transport to use. Either 'grpc' or 'rest'
transport = "grpc"

# ...

from google.cloud.bigquery_reservation_v1.services import reservation_service

reservation_client = reservation_service.ReservationServiceClient(
    transport=transport
)
reservation_name = reservation_client.reservation_path(
    project_id, location, reservation_id
)
reservation_client.delete_reservation(name=reservation_name)

print(f"Deleted reservation: {reservation_name}")
```

## 控管預留項目的存取權

您可以控管哪些使用者能存取特定預留項目。如要覆寫查詢的預留項目，使用者必須具備該預留項目的 `reservations.use` 權限。

### 所需權限

如要取得為工作指定特定預留項目所需的權限，請要求管理員授予您預留資源的[資源編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceEditor)  (`roles/bigquery.resourceEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `reservations.use` 權限，可為工作指定特定預留項目。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

### 控管預留項目的存取權

如要管理特定預留資源的存取權，請使用 [`bq
set-iam-policy`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_set-iam-policy) 指令。

如要管理多項預留資源的存取權，請使用 Google Cloud 控制台，在專案、資料夾或組織層級授予 BigQuery 資源編輯者角色。授予角色時，請使用 [IAM 條件](https://docs.cloud.google.com/bigquery/docs/conditions?hl=zh-tw)，在符合指定條件時允許存取預留項目資源。

如要控管預留項目的存取權，請採取下列任一做法：

### 控制台

在 Google Cloud 控制台中，您可以使用條件，允許存取多個預留資源。

1. 前往 Google Cloud 控制台的「IAM」(身分與存取權管理) 頁面。

   [前往 IAM](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project%2Cfolder%2CorganizationId&hl=zh-tw)
2. 選取專案、資料夾或組織。
3. 如要將 `bigquery.resourceEditor` 角色授予在預留資源上已有角色的主體，請按照下列步驟操作：

   1. 在「View by principals」(按照主體查看) 分頁中，前往適當的主體，或使用「Filter」(篩選器) 選項尋找主體。
   2. 按一下「edit 編輯主體」。
   3. 在「Assign roles」(指派角色) 頁面中，按一下 add「Add roles」(新增角色)。
   4. 在「Search for roles」(搜尋角色) 欄位中輸入 `bigquery.resourceEditor`。
   5. 在搜尋結果中勾選「BigQuery Resource Editor」(BigQuery 資源編輯者) 選項，然後按一下「Apply」(套用)。
   6. 按一下 [儲存]。
4. 或者，如要將 `bigquery.resourceEditor` 角色授予在預留資源中沒有角色的主體，請按照下列步驟操作：

   1. 按一下person\_add「Grant Access」(授予存取權)。
   2. 在「Add principals」(新增主體) 頁面的「New principals」(新增主體) 欄位中，輸入主體的 ID，例如 `my-user@example.com`。
   3. 按一下「add 新增角色」。
   4. 在「Search for roles」(搜尋角色) 欄位中輸入 `bigquery.resourceEditor`。
   5. 在搜尋結果中勾選「BigQuery Resource Editor」(BigQuery 資源編輯者) 選項，然後按一下「Apply」(套用)。
   6. 在「BigQuery 資源編輯器」方塊中，按一下「新增條件」。
   7. 在「新增條件」頁面中：

      1. 在「Title」(標題) 和「Description」(說明) 欄位中輸入值。
      2. 在「條件建構工具」中新增條件。舉例來說，如要新增條件，將角色授予結尾為 `/reservation1` 的所有預留項目名稱，請在「Condition type」(條件類型) 部分選擇「Name」(名稱)，在「Operator」(運算子) 部分選擇「Ends with」(結尾為)，並在「Value」(值) 部分輸入 `/reservation1`。
      3. 按一下 [儲存]。
5. 按一下 [儲存]。

### bq

在 bq 指令列工具中，您可以授予個別預留資源的存取權。

如要授予預留項目的存取權，請使用 [`bq
set-iam-policy`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_set-iam-policy) 指令：

```
bq set-iam-policy --reservation RESOURCE FILE_NAME
```

更改下列內容：

* `RESOURCE`：預留項目 ID。例如：`project1:US.reservation1`。
* `FILE_NAME`：包含 JSON 格式政策的檔案。格式應遵循允許政策的 [IAM 政策結構](https://docs.cloud.google.com/iam/docs/allow-policies?hl=zh-tw#structure)。例如：

  ```
  {
    "bindings": [
      {
        "members": [
          "user:my-user@example.com"
        ],
        "role": "roles/bigquery.resourceEditor"
      }
    ],
    "etag": "BwUjMhCsNvY=",
    "version": 1
  }
  ```

如要進一步瞭解 IAM，請參閱「[管理其他資源的存取權](https://docs.cloud.google.com/iam/docs/manage-access-other-resources?hl=zh-tw)」。

## 使用預留項目群組，優先處理閒置運算單元

您可以建立預留項目群組，控管哪些預留項目可優先存取閒置運算單元。預留項目群組內的預留項目會先共用閒置運算單元，然後才開放給專案中的其他預留項目使用。

建立預留項目群組前，必須先啟用[預留項目公平性](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fairness)。

### 所需權限

如要取得更新特定預留項目以設定預留項目群組所需的權限，請要求管理員授予您預留項目資源的[預留項目編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.reservationEditor)  (`roles/bigquery.reservationEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

### 建立預留項目群組

如要建立預留項目群組，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 找出要加入群組的預留項目，然後勾選旁邊的核取方塊。
4. 點選表格標題中的「Create reservation group」(建立預留項目群組) 按鈕。
5. 在「Create reservation group」(建立預留項目群組) 窗格的「Group name」(群組名稱) 欄位中，輸入群組名稱。
6. 選用：在「預留項目」欄位中，選取要新增至群組的其他預留項目。然後按一下「確定」。
7. 點選「建立」。

新的預留項目群組會顯示在「Slot reservations」(運算單元預留項目) 分頁中。

### bq

如要建立預留項目，請使用 `bq mk` 指令並加上 `--reservation` 旗標：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_group \
    RESERVATION_GROUP_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
* `RESERVATION_GROUP_NAME`：預留項目群組的名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。

### Terraform

使用 [`google_bigquery_reservation_group`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_reservation_group) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會建立名為 `my-reservation-group` 的預留項目群組：

```
resource "google_bigquery_reservation_group" "default" {
  name     = "my-reservation-group"
  location = "us-central1"
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   每個專案只需執行這個指令一次，而且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確的值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

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

### 將預留項目新增至預留項目群組

如要將預留項目新增至預留項目群組，請更新預留項目的 `reservation_group` 屬性：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 展開 more\_vert「Actions」(動作) 選項。
4. 按一下 [編輯]。
5. 在「Edit reservation group」(編輯預留項目群組) 窗格中，選取要在「Reservations」(預留項目) 欄位中新增的預留項目。然後點選「OK」。
6. 按一下 [儲存]。

預留項目群組已更新，納入最新的成員預留項目。

### bq

如要更新預留項目並設定預留項目群組，請使用 `bq update` 指令並加上 `--reservation` 旗標：

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_group_name=RESERVATION_GROUP_NAME \
    --reservation RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_GROUP_NAME`：預留項目群組的名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。
* `RESERVATION_NAME`：預留項目名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。

### 列出有預留項目群組的預留項目

如要列出預留項目的預留群組資訊，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 在「Slot reservations」(運算單元預留項目) 分頁中，表格會顯示預留項目群組和預留項目 (不含上層群組)。
4. 點選預留項目群組旁的展開按鈕，即可展開預留項目群組列，在後續列中顯示成員預留項目。

### bq

如要列出預留項目並加入預留項目群組資訊，請使用 `bq ls` 指令並加上 `--reservation` 旗標：

```
bq ls \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)

### 從預留項目群組中移除預留項目

如要從預留項目群組中移除預留項目，請將預留項目的 `reservation_group` 屬性更新為空字串：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 展開 more\_vert「Actions」(動作) 選項。
4. 按一下 [編輯]。
5. 在「Edit reservation group」(編輯預留項目群組) 窗格中，選取要從「Reservations」(預留項目) 欄位中移除的預留項目。然後點選「OK」。
6. 按一下 [儲存]。

預留項目群組已更新，納入最新的成員預留項目。

如果移除的是群組中最後一個預留項目：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 展開 more\_vert「Actions」(動作) 選項。
4. 按一下 [編輯]。
5. 在「編輯預留項目群組」窗格中，按一下「取消分組」。

預留項目群組已刪除。

### bq

如要從預留項目群組中移除預留項目，請使用 `bq update` 指令並加上 `--reservation` 旗標：

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_group_name="" \
    --reservation RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量
* `RESERVATION_NAME`：預留項目名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。

### 移除空白預留項目群組

預留項目群組必須不含任何成員預留項目，才能刪除。刪除最後一個成員預留項目時，預留項目群組不會自動刪除。移除所有成員預留項目後，必須手動刪除預留項目群組。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 找出要刪除的預留項目群組。確認該資源沒有任何預訂項目。
4. 展開預留項目群組的「Actions」(動作) more\_vert 選項。
5. 按一下 [編輯]。
6. 在「編輯預留項目群組」窗格中，按一下「取消分組」。

### bq

如要刪除空的預留項目群組，請使用 `bq rm` 指令並加上 `--reservation_group` 旗標：

```
bq rm \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_group RESERVATION_GROUP_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_GROUP_NAME`：預留項目群組的名稱。名稱只能使用小寫英數字元或連字號，開頭須為英文字母，結尾不得為連字號，長度上限為 64 個字元。

如要進一步瞭解預留項目群組，請參閱「[預留項目群組](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#groups)」。

## 疑難排解預留項目管理工作問題

建立或更新預留項目時，可能會遇到下列錯誤。

### 預留項目大小或基準運算單元數量必須是 50 的倍數

**錯誤訊息**

* `Max reservation size can only be configured in multiples of 50, except when
  covered by excess commitments.`
* `Baseline slots can only be configured in multiples of 50, except when covered
  by excess commitments.`

**原因**

運算單元一律會自動調度資源，並以 50 的倍數為單位。BigQuery 會根據實際用量擴充運算單元，並以 50 個運算單元為單位向上取整。如果沒有承諾使用合約，或合約無法涵蓋增加的部分，則只能以 50 的倍數增加基準和自動調度資源運算單元。

如果 `baseline slots` 或 `max reservation size - baseline slots` 不是 50 的倍數 (且未涵蓋在超額容量承諾使用合約中)，預留項目就無法擴充至大小上限，並會發生這項錯誤。

**解析度**

執行下列其中一個步驟：

* 購買更多承諾使用容量，以因應運算單元增加。
* 選擇基準和運算單元數量上限 (須為 50 的倍數)。

### 必須啟用預留項目公平性，才能使用運算單元數量上限

**錯誤訊息**

* `Cannot use max slots without enabling reservation-based fairness.`

**原因**

您嘗試設定預留項目容量上限 (例如 `max_slots` 或可預測的預留項目)，但必須先在擁有預留項目的專案中，啟用預留項目公平性。

**解析度**

您必須在專案中[啟用以預留項目為基礎的公平性機制](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#fairness)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-19 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-19 (世界標準時間)。"],[],[]]