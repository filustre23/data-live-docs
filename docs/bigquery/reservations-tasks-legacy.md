* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用舊版運算單元保留功能

**注意：** 只有許可清單中的客戶可以使用舊版預訂，包括存取固定費率帳單或特定承諾期。如要確認您是否能使用這些舊版功能，請與管理員聯絡。固定費率計費模式會定義運算資源的計費方式，但固定費率預訂和承諾方案的功能與 Enterprise 版的配額相同。

透過 BigQuery Reservation API，您可以購買專屬運算單元 (稱為「[*承諾*](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)」)、建立運算單元集區 (稱為「[*預留項目*](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations)」)，以及將專案、資料夾和機構指派給這些預留項目。

保留項目可讓您為工作負載指派專屬的運算單元數量。舉例來說，您可能不希望實際工作環境工作負載與測試工作負載爭奪運算單元。您可以建立名為 `prod` 的預留項目，並將生產環境工作負載指派給這個預留項目。詳情請參閱「[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations)」一文。

## 建立預留項目

### 所需權限

如要建立預留項目，您必須具備下列身分與存取權管理 (IAM) 權限：

* `bigquery.reservations.create` [管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)，該專案會維護承諾使用合約的擁有權。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 使用專屬運算單元建立預留項目

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「建立預留項目」。
4. 在「Reservation name」(預留項目名稱) 欄位中，輸入預留項目的名稱。
5. 在「位置」下拉式清單中，選取所需位置。
6. 在「容量模型」部分，選取容量模型。
7. 如果選取「固定費率」選項，請在「基準運算單元」下方，輸入預留項目的運算單元數量。

   1. 在「預留項目大小選取器」清單中，選取預留項目大小上限。
   2. 選用：在「基準運算單元」欄位中，輸入保留項目的基準運算單元數量。如要只使用指定的運算單元容量，請按一下「忽略閒置運算單元」切換鈕。

      可用的自動調度資源運算單元數量，取決於從預留項目大小上限值減去基準運算單元值。舉例來說，如果您建立的預留項目有 100 個基準運算單元，且預留項目大小上限為 400，則預留項目有 300 個自動調度運算單元。如要進一步瞭解基準運算單元，請參閱「[使用預留項目搭配基準和自動調度運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw#using_reservations_with_baseline_and_autoscaling_slots)」一文。
8. 如要停用[閒置運算單元共用功能](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)，請按一下「忽略閒置運算單元」切換鈕。
9. **預估費用**表格會顯示時段明細。
   「運算能力摘要」表格會顯示預留項目的摘要。
10. 按一下 [儲存]。

新的預訂項目會顯示在「預訂」分頁中。

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
   );
   ```

   取代下列項目：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
   * `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，版本選項會限制為 Enterprise 版。
   * `RESERVATION_NAME`：預留項目的名稱

     開頭和結尾必須為小寫英文字母或數字，且只能包含小寫英文字母、數字和連字號。
   * `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量。您無法在同一個預訂中設定 `slot_capacity` 選項和 `edition` 選項。
   * `EDITION`：預訂的方案。將預留項目指派給版本時，功能和價格會有所變更。詳情請參閱 [BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
   * `NUMBER_OF_AUTOSCALING_SLOTS`：指派給預訂的自動調度資源運算單元數量。這等於預留項目大小上限減去基準運算單元數量。
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
    RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果選取 [BigQuery Omni 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，版本選項會限制為 Enterprise 版。
* `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量
* `RESERVATION_NAME`：預留項目名稱
* `EDITION`：預訂的方案。將預留項目指派給版本時，功能和價格會有所變更。詳情請參閱 [BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
* `NUMBER_OF_AUTOSCALING_SLOTS`：指派給預訂的自動調度資源運算單元數量。這等於預留項目大小上限減去基準運算單元數量。

如要瞭解 `--ignore_idle_slots` 旗標，請參閱「[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)」。預設值為 `false`。

### Python

使用這個程式碼範例前，請先安裝 [google-cloud-bigquery-reservation 套件](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest?hl=zh-tw)。
建構 [ReservationServiceClient](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient)。使用 [Reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.types.Reservation?hl=zh-tw) 說明要建立的預訂項目。使用 [create\_reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient_create_reservation) 方法建立預留項目。

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

## 更新預訂

您可以對預訂項目進行下列更新：

* 新增或移除運算單元，即可變更保留項目大小。
* 設定此預留項目中的查詢是否要使用閒置的運算單元。
* 變更分配給預留項目的基準或自動調度運算單元數量。

### 所需權限

如要更新預留項目，您必須具備下列身分與存取權管理 (IAM) 權限：

* `bigquery.reservations.update`，[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)會維護承諾使用合約的所有權。

下列預先定義的 IAM 角色都包含這項權限：

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
3. 按一下「預訂」分頁標籤。
4. 找出要更新的預訂。
5. 展開「動作」more\_vert選項。
6. 按一下 [編輯]。
7. 在「預留項目大小上限選取器」對話方塊中，輸入預留項目大小上限。
8. 在「Baseline slots」(基準運算單元) 欄位中，輸入基準運算單元數量。
9. 按一下 [儲存]。

### SQL

如要變更預留空間大小，請使用[`ALTER RESERVATION SET OPTIONS`資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_reservation_set_options_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER RESERVATION
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME`
   SET OPTIONS (
     slot_capacity = NUMBER_OF_BASELINE_SLOTS,
   );
   ```

   取代下列項目：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
   * `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，例如 `europe-west9`。
   * `RESERVATION_NAME`：預訂的名稱。開頭和結尾必須為小寫英文字母或數字，且只能包含小寫英文字母、數字和連字號。
   * `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要更新預訂大小，請使用 `bq update` 指令並加上 `--reservation` 標記：

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --slots=NUMBER_OF_BASELINE_SLOTS \
    --reservation RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `NUMBER_OF_BASELINE_SLOTS`：要分配給預留項目的基準運算單元數量
* `RESERVATION_NAME`：預留項目名稱

### Python

使用這個程式碼範例前，請先安裝 [google-cloud-bigquery-reservation 套件](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest?hl=zh-tw)。
建構 [ReservationServiceClient](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient)。使用 [Reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.types.Reservation?hl=zh-tw) 和 [FieldMask.paths](https://googleapis.dev/python/protobuf/latest/google/protobuf/field_mask_pb2.html#google.protobuf.field_mask_pb2.FieldMask.paths) 屬性描述更新的屬性。使用 [update\_reservation](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest/google.cloud.bigquery_reservation_v1.services.reservation_service.ReservationServiceClient?hl=zh-tw#google_cloud_bigquery_reservation_v1_services_reservation_service_ReservationServiceClient_update_reservation) 方法更新預訂。

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

`--ignore_idle_slots` 標記可控制在預留項目中執行的查詢是否能使用其他預留項目的閒置運算單元。詳情請參閱「[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)」。你可以更新現有預訂的這項設定。

如要更新預訂，請使用 `bq update` 指令並加上 `--reservation` 旗標。以下範例將 `--ignore_idle_slots` 設為 `true`，也就是說，預留項目只會使用分配給預留項目的時段。

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --ignore_idle_slots=true \
    --reservation RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：專案 ID
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱

### 列出閒置時段設定

如要列出預留項目的[閒置時段](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)設定，請執行下列操作：

### SQL

查詢[`INFORMATION_SCHEMA.RESERVATIONS_BY_PROJECT` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw#schema)的 `ignore_idle_slots` 欄。

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

   取代下列項目：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
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

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
* `LOCATION`：預訂的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)

`ignoreIdleSlots` 欄位包含設定。

## 刪除預留項目

刪除預留項目後，目前使用該預留項目運算單元執行的任何工作都會失敗。為避免發生錯誤，請先讓執行中的工作完成，再刪除預訂。

### 所需權限

如要刪除預留項目，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.reservations.delete`，[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)會維護承諾使用合約的擁有權。

下列預先定義的 IAM 角色都具備這項權限：

* `BigQuery Admin`
* `BigQuery Resource Admin`
* `BigQuery Resource Editor`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 刪除預留項目

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「預訂」分頁標籤。
4. 找出要刪除的預訂。
5. 展開「動作」more\_vert選項。
6. 按一下「Delete」(刪除)。
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

   取代下列項目：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
   * `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
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

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)專案 ID
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)
* `RESERVATION_NAME`：預留項目名稱

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

## 將 BigQuery Reservation API 新增至 VPC Service Controls

**注意：** 使用以特定 BigQuery 版本建立的預留項目時，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

BigQuery Reservation API 支援 [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls?hl=zh-tw)。
如要將 BigQuery Reservation API 與 VPC Service Controls 整合，請按照「[建立服務範圍](https://docs.cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=zh-tw)」中的操作說明，將 BigQuery Reservation API 新增至受保護的服務。

服務範圍可保護範圍內管理專案的預留項目、約期和指派項目存取權。建立指派項目時，VPC Service Controls 會保護管理專案、指派對象專案、資料夾和機構。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]