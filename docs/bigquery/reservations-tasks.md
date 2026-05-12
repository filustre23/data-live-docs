Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理工作負載預留項目

透過 BigQuery Reservation API，您可以購買專屬運算單元 (稱為「[*承諾*](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)」)、建立運算單元集區 (稱為「[*預留項目*](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations)」)，以及將專案、資料夾和機構指派給這些預留項目。

保留項目可讓您為工作負載指派專屬的運算單元數量。舉例來說，您可能不希望實際工作環境工作負載與測試工作負載爭奪運算單元。您可以建立名為 `prod` 的預留項目，並將正式版工作負載指派給這個預留項目。詳情請參閱「[瞭解預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)」。

## 建立預留項目

### 所需權限

如要建立預留項目，您必須具備下列身分與存取權管理 (IAM) 權限：

* `bigquery.reservations.create`，[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)會維護承諾使用合約的擁有權。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Resource Editor`
* `BigQuery Resource Admin`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 使用專屬運算單元建立預留項目

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「建立預留項目」。
4. 在「Reservation name」(預留項目名稱) 欄位中，輸入預留項目的名稱。
5. 在「位置」清單中選取位置。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，版本選項會限制為 Enterprise 版。
6. 從「Edition」(版本) 清單中選取版本。BigQuery 版本功能 (例如自動調度資源) 僅適用於該版本。詳情請參閱 [BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
7. 在「預留項目大小選取器」清單中，選取預留項目大小上限。
8. 選用：在「Baseline slots」(基準運算單元) 欄位中，輸入保留項目的基準運算單元數量。

   可用的自動調度資源運算單元數量，取決於從「預留項目大小上限」減去「基準運算單元」值。舉例來說，如果您建立的預留項目有 100 個基準運算單元，且預留項目大小上限為 400，則預留項目會有 300 個自動調度運算單元。如要進一步瞭解基準運算單元，請參閱「[使用預留項目搭配基準和自動調度資源運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw#using_reservations_with_baseline_and_autoscaling_slots)」一文。
9. 如要停用[閒置的運算單元共用功能](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)，並只使用指定的運算單元容量，請按一下「忽略閒置的運算單元」切換鈕。
10. 如要展開「進階設定」部分，請按一下expand\_more展開箭頭。
11. 選用：如要設定目標工作並行數，請按一下「覆寫自動目標工作並行設定」切換鈕，然後輸入「目標工作並行數」。
12. **預估費用**表格會顯示時段明細。「運算能力摘要」表格會顯示預留項目摘要。
13. 按一下 [儲存]。

新預訂的時段會顯示在「預訂時段」分頁中。

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
     autoscale_max_slots = NUMBER_OF_AUTOSCALING_SLOTS);
   ```

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案擁有預訂資源
   * `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，版本選項會限制為 Enterprise 版。
   * `RESERVATION_NAME`：預留項目名稱

     名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。
   * `NUMBER_OF_BASELINE_SLOTS`：要分配給預訂的基準時段數量。您無法在同一個預訂中設定 `slot_capacity` 選項和 `standard` 版本選項。
   * `EDITION`：預訂的方案。將預留項目指派給版本時，功能和價格會有所變更。詳情請參閱 [BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
   * `NUMBER_OF_AUTOSCALING_SLOTS`：指派給預留項目的自動調度資源運算單元數量。這等於預留項目大小上限減去基準運算單元數量。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要建立預訂項目，請使用 `bq mk` 指令並加上 `--reservation` 旗標：

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
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，版本選項會限制為 Enterprise 版。
* `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量
* `RESERVATION_NAME`：預訂名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。
* `EDITION`：預訂的方案。將預留項目指派給版本時，功能和價格會有所變更。詳情請參閱 [BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
* `NUMBER_OF_AUTOSCALING_SLOTS`：指派給預留項目的自動調度資源運算單元數量。這等於預留項目大小上限減去基準運算單元數量。無法使用 `--max_slots` 或 `--scaling_mode` 旗標設定這項功能。
* `MAXIMUM_NUMBER_OF_SLOTS`：預留項目可使用的運算單元數量上限。這個值必須使用 `--scaling_mode` 標記設定 ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))。
* `SCALING_MODE`：預訂的資源調度模式。選項包括 `ALL_SLOTS`、`IDLE_SLOTS_ONLY` 或 `AUTOSCALE_ONLY`。這個值必須使用 `--scaling_mode` 標記設定 ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))。

如要瞭解 `--ignore_idle_slots` 標記，請參閱「[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)」。預設值為 `false`。

### Terraform

請使用 [`google_bigquery_reservation`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_reservation) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會建立名為 `my-reservation` 的預訂：

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

### Python

使用這個程式碼範例前，請先安裝 [google-cloud-bigquery-reservation 套件](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest?hl=zh-tw)。
建構 [ReservationServiceClient](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient)。使用 [Reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.types.Reservation?hl=zh-tw) 說明要建立的預訂。使用 [create\_reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient_create_reservation) 方法建立預留項目。

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

建立設有[運算單元數量上限](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)的預留項目之前，請務必先啟用[以預留項目為準的公平性](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fairness)。

#### 啟用以預留項目為基礎的公平性機制

如要啟用以預訂為準的公平性，請將 [`enable_reservation_based_fairness` 旗標](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)設為 `true`。

如要更新專案的預留項目公平性，您必須對擁有預留項目的[專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)具有 `bigquery.config.update` 權限。預先定義的 `BigQuery Admin` 角色包含這項權限。

如要進一步瞭解如何更新專案的預設設定，請參閱「[管理設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#required_permissions)」。

```
ALTER PROJECT `PROJECT_NAME` SET OPTIONS (
    `region-LOCATION.enable_reservation_based_fairness`= true);
```

更改下列內容：

* PROJECT\_NAME：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID
* LOCATION：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)

#### 建立可預測的預留項目

如要建立設有運算單元數量上限的預留項目，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽面板中，前往「運算資源管理」部分，然後點選「建立預留項目」。
3. 在「Reservation name」(預留項目名稱) 欄位中，輸入預留項目的名稱。
4. 在「位置」清單中選取位置。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，版本選項會限制為 Enterprise 版。
5. 從「Edition」(版本) 清單中選取版本。詳情請參閱[瞭解 BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
6. 在「預留項目大小選取器」清單中，選取預留項目大小上限。
7. 選用：在「Baseline slots」(基準運算單元) 欄位中，輸入保留項目的基準運算單元數量。

   可用的自動調度資源運算單元數量，取決於從「預留項目大小上限」減去「基準運算單元」值。舉例來說，如果您建立的預留項目有 100 個基準運算單元，且預留項目大小上限為 400，則預留項目會有 300 個自動調度運算單元。如要進一步瞭解基準運算單元，請參閱「[使用預留項目搭配基準和自動調度資源運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw#using_reservations_with_baseline_and_autoscaling_slots)」一文。
8. 如要停用[閒置的運算單元共用功能](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)，並只使用指定的運算單元容量，請按一下「忽略閒置的運算單元」切換鈕。
9. 如要展開「進階設定」部分，請按一下expand\_more展開箭頭。

   在「如何使用閒置時段？」清單中，選取設定選項。

   * **最容易預測：**先耗用基準運算單元，接著是閒置運算單元，最後是自動調度資源運算單元，但不會超過指定的運算單元數量上限。
   * **較難預測：**只會使用基準和閒置運算單元，且不會超過運算單元數量上限。不會使用自動調度資源運算單元。
   * **變化最大：**會使用所有可用的閒置運算單元，以便擴充至基準值以上，接著才會使用自動調度運算單元，但不會超過上限與基準值之間的差異。這可能會導致預訂項目超過指定的運算單元數量上限。
10. **預估費用**表格會顯示時段明細。「運算能力摘要」表格會顯示預留項目摘要。
11. 按一下 [儲存]。

新預訂的時段會顯示在「預訂時段」分頁中。

### bq

如要建立可預測的預訂項目，請使用 `bq mk` 指令搭配 `--reservation` 旗標，並設定 `max_slots` 和 `scaling_mode` 的值：

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
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，版本選項會限制為 Enterprise 版。
* `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量
* `RESERVATION_NAME`：預留項目名稱
* `EDITION`：預訂的方案。將預留項目指派給版本時，功能和價格會有所變更。詳情請參閱 [BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
* `MAXIMUM_NUMBER_OF_SLOTS`：預留項目可使用的運算單元數量上限。這個值必須使用 `--scaling_mode` 標記設定。
* `SCALING_MODE`：預訂的資源調度模式。選項包括 `ALL_SLOTS`、`IDLE_SLOTS_ONLY` 或 `AUTOSCALE_ONLY`。這個值必須使用 `max_slots` 標記設定。這個值必須與 `ignore_idle_slots` 旗標一致。詳情請參閱「[預留項目預測](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)」。

如要瞭解 `--ignore_idle_slots` 標記，請參閱「[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)」。預設值為 `false`。

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
     ignore_idle_slots=IGNORE_IDLE_SLOTS
     max_slots = MAX_NUMBER_OF_SLOTS,
     scaling_mode = SCALING_MODE);
   ```

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID。
   * `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，版本選項會限制為 Enterprise 版。
   * `RESERVATION_NAME`：預留項目名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。
   * `NUMBER_OF_BASELINE_SLOTS`：要分配給預訂的基準時段數量。您無法在同一個預訂中設定 `slot_capacity` 選項和 `standard` 版本選項。
   * `EDITION`：預訂的方案。將預留項目指派給版本時，功能和價格會有所變更。詳情請參閱 [BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
   * `IGNORE_IDLE_SLOTS`：預留項目是否使用[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)。預設值為 `false`。
   * `MAX_NUMBER_OF_SLOTS`：預留項目可使用的運算單元數量上限。這個值必須使用 `scaling_mode` 選項設定。
   * `SCALING_MODE`：預訂的資源調度模式。選項包括 `ALL_SLOTS`、`IDLE_SLOTS_ONLY` 或 `AUTOSCALE_ONLY`。這個值必須使用 `max_slots` 選項設定。這個值必須與 `ignore_idle_slots` 選項一致。詳情請參閱「[預留項目可預測性](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)」。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### Terraform

請使用 [`google_bigquery_reservation`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_reservation) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會建立名為 `my-reservation` 的可預測預訂群組：

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

如要進一步瞭解可預測的預留項目，請參閱「[可預測的預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)」。

## 更新預訂

您可以對預訂項目進行下列更新：

* 新增或移除運算單元，即可變更保留項目大小。
* 設定此預留項目中的查詢是否要使用閒置運算單元。
* 變更分配給預留項目的基準或自動調度資源運算單元數量。
* 設定目標工作並行。

如要變更預訂的集數，請先[刪除](#delete_reservations)預訂，然後[建立](#create_reservations)更新集數的預訂。

### 所需權限

如要更新預留項目，您需要下列 Identity and Access Management (IAM) 權限：

* `bigquery.reservations.update`，[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)會維護承諾使用合約的擁有權。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 變更預留項目大小

你可以為現有預約新增或移除時段。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「運算單元預留項目」分頁標籤。
4. 找出要更新的預訂。
5. 展開「動作」more\_vert選項。
6. 按一下 [編輯]。
7. 在「預留項目大小上限選取器」對話方塊中，輸入預留項目大小上限。
8. 在「Baseline slots」(基準運算單元) 欄位中，輸入基準運算單元數量。
9. 如要展開「進階設定」部分，請按一下expand\_more展開箭頭。
10. 選用：如要設定目標工作並行數，請按一下「覆寫自動目標工作並行設定」切換鈕，然後輸入「目標工作並行數」。
11. 按一下 [儲存]。

### SQL

如要變更預訂大小，請使用[`ALTER RESERVATION SET OPTIONS`資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_reservation_set_options_statement)。

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

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案擁有預訂資源
   * `LOCATION`：保留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，例如 `europe-west9`。
   * `RESERVATION_NAME`：預訂名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。
   * `NUMBER_OF_BASELINE_SLOTS`：要分配給預訂的基準時段數量。
   * `NUMBER_OF_AUTOSCALING_SLOTS`：指派給預留項目的自動調度資源運算單元數量。這等於預留項目大小上限減去基準運算單元數量。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要更新預訂大小，請使用 `bq update` 指令並加上 `--reservation` 標記：

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
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量
* `RESERVATION_NAME`：預訂名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。
* `NUMBER_OF_AUTOSCALING_SLOTS`：指派給預留項目的自動調度資源運算單元數量。這等於預留項目大小上限減去基準運算單元數量。

### Python

使用這個程式碼範例前，請先安裝 [google-cloud-bigquery-reservation 套件](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest?hl=zh-tw)。
建構 [ReservationServiceClient](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient)。使用 [Reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.types.Reservation?hl=zh-tw) 和 [FieldMask.paths](https://googleapis.dev/python/protobuf/latest/google/protobuf/field_mask_pb2.html#google.protobuf.field_mask_pb2.FieldMask.paths) 屬性描述更新的屬性。使用 [update\_reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient_update_reservation) 方法更新預留項目。

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

### 設定查詢是否要使用閒置運算單元

`--ignore_idle_slots` 旗標可控制在預留項目中執行的查詢是否能使用其他預留項目的閒置運算單元。詳情請參閱「[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)」。您可以在現有預訂中更新這項設定。

如要更新預訂項目，請使用 `bq update` 指令並加上 `--reservation` 旗標。以下範例將 `--ignore_idle_slots` 設為 `true`，也就是說，預留項目只會使用分配給預留項目的時段。

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --ignore_idle_slots=true \
    --reservation RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預訂名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。

### 列出閒置時段設定

如要列出預留項目的[閒置時段](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)設定，請執行下列操作：

### SQL

查詢 [`INFORMATION_SCHEMA.RESERVATIONS_BY_PROJECT` 檢視區塊的 `ignore_idle_slots` 資料欄](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw#schema)。

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

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：擁有預訂資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
   * `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

請使用 `bq ls` 指令，並加上 `--reservation` 旗標：

```
bq ls --reservation \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預訂資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
* `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)

`ignoreIdleSlots` 欄位包含設定。

## 刪除預留項目

如果刪除預留項目，任何使用該預留項目運算單元的工作都會失敗。為避免發生錯誤，請先讓執行中的工作完成，再刪除預訂。

### 所需權限

如要刪除預留項目，您需要下列 Identity and Access Management (IAM) 權限：

* `bigquery.reservations.delete`，[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)會維護承諾使用合約的擁有權。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

**注意：** 您可以刪除有有效承諾的預訂，但仍須支付承諾剩餘期間的費用。刪除預訂或將相關聯的專案切換為以量計價模式，都不會停止收取這些費用。如要進一步瞭解承諾到期，請參閱「[承諾到期](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#commitment_expiration)」。如需預訂、承諾或費用方面的其他協助，請與[Google Cloud 支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)聯絡。

### 刪除預留項目

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「預訂」分頁標籤。
4. 找出要刪除的預訂。
5. 展開「動作」more\_vert選項。
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

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案擁有預訂資源
   * `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
   * `RESERVATION_NAME`：預訂 ID
3. 按一下「執行」play\_circle。

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

* `ADMIN_PROJECT_ID`：擁有預訂資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預訂名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。

### Python

使用這個程式碼範例前，請先安裝 [google-cloud-bigquery-reservation 套件](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest?hl=zh-tw)。
建構 [ReservationServiceClient](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient)。
使用 [delete\_reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient_delete_reservation) 方法刪除預留項目。

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

## 控管預訂存取權

您可以控管哪些使用者能存取特定預訂。如要讓使用者覆寫查詢的預留項目，他們必須擁有該預留項目的 `reservations.use` 權限。

### 所需權限

如要取得為工作指定特定預留所需的權限，請要求系統管理員授予預留資源的[資源編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceEditor)  (`roles/bigquery.resourceEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `reservations.use` 權限，可為工作指定特定預留空間。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

### 控管預訂項目的存取權

如要管理特定預留資源的存取權，請使用 [`bq
set-iam-policy`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_set-iam-policy) 指令。

如要管理多個預留項目資源的存取權，請使用 Google Cloud 控制台在專案、資料夾或機構上授予 BigQuery 資源編輯者角色。授予角色時，請使用 [IAM 條件](https://docs.cloud.google.com/bigquery/docs/conditions?hl=zh-tw)，在符合指定條件時允許存取預留項目資源。

如要控管預訂項目的存取權，請採取下列任一做法：

### 控制台

在 Google Cloud 控制台中，您可以使用條件允許存取多個預訂資源。

1. 前往 Google Cloud 控制台的「IAM」(身分與存取權管理) 頁面。

   [前往 IAM](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project%2Cfolder%2CorganizationId&hl=zh-tw)
2. 選取專案、資料夾或機構。
3. 如要將 `bigquery.resourceEditor` 角色授予在預留資源中擁有角色的主體，請按照下列步驟操作：

   1. 在「View by principals」(按照主體查看) 分頁中，前往適當的主體，或使用「Filter」(篩選) 選項尋找主體。
   2. 按一下「Edit principal」(編輯主體)edit。
   3. 在「指派角色」頁面上，按一下
      add「新增角色」。
   4. 在「Search for roles」(搜尋角色) 欄位中輸入 `bigquery.resourceEditor`。
   5. 在搜尋結果中勾選「BigQuery 資源編輯器」選項，然後點選「套用」。
   6. 按一下 [儲存]。
4. 或者，如要將 `bigquery.resourceEditor` 角色授予沒有預留資源角色的主體，請按照下列步驟操作：

   1. 按一下 person\_add「授予存取權」。
   2. 在「新增主體」頁面的「新增主體」欄位中，輸入主體的 ID，例如 `my-user@example.com`。
   3. 按一下 add「新增角色」。
   4. 在「Search for roles」(搜尋角色) 欄位中輸入 `bigquery.resourceEditor`。
   5. 在搜尋結果中勾選「BigQuery 資源編輯器」選項，然後點選「套用」。
   6. 在「BigQuery 資源編輯器」方塊中，按一下「新增條件」。
   7. 在「新增條件」頁面中：

      1. 在「名稱」和「說明」欄位中輸入值。
      2. 在「條件建構工具」中新增條件。舉例來說，如要新增條件，將角色授予所有以 `/reservation1` 結尾的預訂名稱，請在「條件類型」中選擇「名稱」，在「運算子」中選擇「結尾為」，並在「值」中輸入 `/reservation1`。
      3. 按一下 [儲存]。
5. 按一下 [儲存]。

### bq

在 bq 指令列工具中，您可以授予個別預留資源的存取權。

如要授予預留項目存取權，請使用 [`bq
set-iam-policy`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_set-iam-policy) 指令：

```
bq set-iam-policy --reservation RESOURCE FILE_NAME
```

更改下列內容：

* `RESOURCE`：預留項目 ID。
  例如：`project1:US.reservation1`。
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

## 使用預留項目群組優先使用閒置運算單元

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bigquery-wlm-feedback@google.com](mailto:bigquery-wlm-feedback@google.com)。

您可以建立預留項目群組，控管哪些預留項目可優先存取閒置運算單元。預留項目群組中的預留項目會先共用閒置運算單元，再將這些運算單元提供給專案中的其他預留項目。

建立預留項目群組前，請先啟用[以預留項目為準的公平性](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fairness)。

### 所需權限

如要取得更新特定預留項目以設定預留群組所需的權限，請要求系統管理員授予預留資源的[預留項目編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.reservationEditor)  (`roles/bigquery.reservationEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

### 建立預留項目群組

如要建立預留項目群組，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 找出要新增至群組的預訂項目，然後選取旁邊的核取方塊。
4. 按一下表格標題中的「建立預留項目群組」按鈕。
5. 在「建立預訂群組」窗格的「群組名稱」欄位中，輸入群組名稱。
6. 選用：在「預訂」欄位中，選取要新增至群組的其他預訂。然後按一下「確定」。
7. 點選「建立」。

新的預訂群組會顯示在「預訂時段」分頁中。

### bq

如要建立預訂項目，請使用 `bq mk` 指令並加上 `--reservation` 旗標：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_group \
    RESERVATION_GROUP_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
* `RESERVATION_GROUP_NAME`：預訂群組的名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。

### Terraform

請使用 [`google_bigquery_reservation_group`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_reservation_group) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會建立名為 `my-reservation-group` 的預訂群組：

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

### 將預留項目新增至預留項目群組

如要將預訂項目新增至預訂項目群組，請更新預訂項目的 `reservation_group` 屬性：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 展開「動作」more\_vert選項。
4. 按一下 [編輯]。
5. 在「編輯預留項目群組」窗格中，選取「預留項目」欄位中要新增的預留項目。然後點選「OK」。
6. 按一下 [儲存]。

預留項目群組會更新為最新的成員預留項目。

### bq

如要更新預訂項目並設定預訂群組，請使用 `bq update` 指令搭配 `--reservation` 旗標：

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_group_name=RESERVATION_GROUP_NAME \
    --reservation RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_GROUP_NAME`：預訂群組的名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。
* `RESERVATION_NAME`：預訂名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。

### 列出有預留項目群組的預留項目

如要列出預訂項目的預訂群組資訊，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 在「運算單元預留項目」分頁中，您可以在表格中查看預留項目群組和預留項目 (沒有父項群組)。
4. 按一下預留項目群組旁的展開按鈕，預留項目群組資料列就會展開，並在後續資料列中顯示成員預留項目。

### bq

如要列出保留項目並納入保留項目群組資訊，請使用 `bq ls` 指令搭配 `--reservation` 旗標：

```
bq ls \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)

### 從預訂群組中移除預訂項目

如要從預留項目群組中移除預留項目，請將預留項目的 `reservation_group` 屬性更新為空字串：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 展開「動作」more\_vert選項。
4. 按一下 [編輯]。
5. 在「編輯預留項目群組」窗格中，選取「預留項目」欄位中要移除的預留項目。然後點選「OK」。
6. 按一下 [儲存]。

預留項目群組會更新為最新的成員預留項目。

如果要移除的預訂是群組中的最後一個預訂：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 展開「動作」more\_vert選項。
4. 按一下 [編輯]。
5. 在「編輯預留項目群組」窗格中，按一下「取消分組」。

預留項目群組已刪除。

### bq

如要從預留項目群組移除預留項目，請使用 `bq update` 指令並加上 `--reservation` 旗標：

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_group_name="" \
    --reservation RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量
* `RESERVATION_NAME`：預訂名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。

### 移除空白預留項目群組

只有在預留項目群組不含任何成員預留項目時，才能刪除該群組。刪除最後一個成員預留項目時，系統不會自動刪除預留項目群組。移除所有成員預約後，您必須手動刪除預約群組。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 找出要刪除的預訂群組。確認該帳戶沒有任何預訂記錄。
4. 展開預留項目群組的「動作」more\_vert選項。
5. 按一下 [編輯]。
6. 在「編輯預留項目群組」窗格中，按一下「取消分組」。

### bq

如要刪除空白預訂群組，請使用 `bq rm` 指令並加上 `--reservation_group` 旗標：

```
bq rm \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_group RESERVATION_GROUP_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_GROUP_NAME`：預訂群組的名稱。名稱只能包含小寫英數字元或連字號，開頭必須是字母，而且結尾不得為連字號，長度上限為 64 個字元。

如要進一步瞭解預留項目群組，請參閱「[預留項目群組](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#groups)」。

## 疑難排解

建立或更新預訂時，可能會遇到下列錯誤：

發生錯誤：`Max reservation size can only be configured in multiples of 50, except when covered by excess commitments.`

發生錯誤：`Baseline slots can only be configured in multiples of 50, except when covered by excess commitments.`
:   運算單元一律會自動調度至 50 的倍數。系統會根據實際用量向上調整，並將用量四捨五入至最接近的 50 個時段增量。如果沒有承諾使用，或承諾使用無法涵蓋增加的運算單元，基準和自動調度資源運算單元只能以 50 的倍數增加。
:   如果 `reservation size - baseline slots` 不是 50 的倍數，預留項目就無法擴充至最大預留項目大小，因此會導致這個錯誤。
:   **解決方法：**

    * 購買更多承諾使用容量，以因應運算單元增加的需求。
    * 選擇的基準和最大運算單元數量必須是 50 的倍數。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]