Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Cloud Storage 資料載入 BigQuery

您可以使用 Cloud Storage 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 Cloud Storage 載入 BigQuery。使用 BigQuery 資料移轉服務，您可以排定週期性移轉工作，將 Cloud Storage 中的最新資料新增至 BigQuery。

如要瞭解 Cloud Storage 移轉作業的運作方式，請參閱「[Cloud Storage 資料移轉簡介](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw)」。

## 限制

從 Cloud Storage 到 BigQuery 的週期性資料移轉作業有下列限制：

* 凡是符合萬用字元或資料移轉執行階段參數所定義模式的檔案*都必須*共用您為目的地資料表定義的架構，否則移轉作業會失敗。如果執行作業期間資料表結構定義有變更，也會導致移轉作業失敗。
* 由於 [Cloud Storage 物件可以建立版本](https://docs.cloud.google.com/storage/docs/object-versioning?hl=zh-tw)，因此請務必注意，BigQuery 資料移轉作業不支援封存的 Cloud Storage 物件。物件必須處於使用中狀態才能轉移。
* 與[從 Cloud Storage 到 BigQuery 的個別資料載入](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage?hl=zh-tw)不同，對於持續進行的資料移轉，您必須先建立目的地資料表，再設定移轉作業。如果是 CSV 和 JSON 檔案，您也必須預先定義[資料表結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。BigQuery 無法在週期性資料移轉程序中建立資料表。
* 從 Cloud Storage 移轉資料時，系統預設會將「Write preference」(寫入偏好設定) 參數設為 `APPEND`。在這個模式下，未經修改的檔案只能載入 BigQuery 一次。如果檔案的 `last modification time` 屬性更新，系統會重新載入檔案。
* 如果 Cloud Storage 檔案在資料移轉期間經過修改，BigQuery 資料移轉服務無法保證所有檔案都會移轉，或只移轉一次。
* 從 Cloud Storage bucket 將資料載入 BigQuery 時，會受到下列限制：

  + BigQuery 無法保證外部資料來源的資料一致性。查詢執行期間，基礎資料的變更可能會導致非預期的行為。
  + BigQuery 不支援 [Cloud Storage 物件版本管理](https://docs.cloud.google.com/storage/docs/object-versioning?hl=zh-tw)。如果您在 Cloud Storage URI 中加入版本編號，載入工作就會失敗。
* 視 Cloud Storage 來源資料的格式而定，可能會有其他限制。詳情請參閱下列資源：

  + [CSV 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#limitations)
  + [JSON 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#limitations)
  + [Parquet 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw)
  + [Firestore 匯出限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-firestore?hl=zh-tw#limitations)
  + [Avro 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw#limitations)
  + [巢狀與重複資料的限制](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw#limitations)

## 間隔下限

* 系統會立即選取來源檔案進行資料移轉，沒有檔案存在時間下限。
* 週期性資料移轉作業之間的最短間隔時間為 15 分鐘。定期資料移轉的預設間隔為每 24 小時一次。
* 您可以設定[事件觸發的移轉](https://docs.cloud.google.com/bigquery/docs/event-driven-transfer?hl=zh-tw)，自動排定資料移轉時間，縮短間隔。

## 事前準備

建立 Cloud Storage 資料移轉作業前，請先完成下列事項：

* 確認您已完成「[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)」中的所有必要動作。
* 請擷取您的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw#google-cloud-storage-uri)。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* [建立資料移轉目的地資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create_an_empty_table_with_a_schema_definition)，並指定結構定義。您可以建立 BigQuery 資料表或[建立 Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw#create-iceberg-tables)。
* 如果您打算指定客戶自行管理的加密金鑰 (CMEK)，請確認[服務帳戶具備加密和解密權限](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#grant_permission)，且您擁有使用 CMEK 所需的 [Cloud KMS 金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱「[指定移轉作業加密金鑰](#CMEK)」。

## 所需權限

將資料載入 BigQuery 時，您必須具備相關權限才能將資料載入新的或現有的 BigQuery 資料表和分區。如要載入 Cloud Storage 中的資料，您也必須具備資料所屬值區的存取權。請確認您已擁有下列必要權限：

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能建立 BigQuery 資料移轉服務資料移轉作業：

* BigQuery 資料移轉服務權限：
  + `bigquery.transfers.update`
  + `bigquery.transfers.get`
* BigQuery 權限：
  + `bigquery.datasets.get`
  + `bigquery.datasets.getIamPolicy`
  + `bigquery.datasets.update`
  + `bigquery.datasets.setIamPolicy`
  + `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

詳情請參閱「[授予 `bigquery.admin` 存取權](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#grant_bigqueryadmin_access)」。

### 必要的 Cloud Storage 角色

您必須具備個別 bucket 的 `storage.objects.get` 權限或更高權限。如果使用 URI [萬用字元](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw#wildcard-support)，則必須具備 `storage.objects.list` 權限。如要在每次成功移轉資料後刪除來源檔案，您也需要 `storage.objects.delete` 權限。`storage.objectAdmin` 預先定義的 [IAM 角色](https://docs.cloud.google.com/storage/docs/access-control/iam-roles?hl=zh-tw)包含所有這些權限。

## 設定 Cloud Storage 轉移作業

如要在 BigQuery 資料移轉服務中建立 Cloud Storage 資料移轉作業，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「Data transfers」(資料移轉) 頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「建立轉移作業」add。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Google Cloud Storage」。
4. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
5. 在「Schedule options」(排程選項) 部分選取「Repeat frequency」(重複執行頻率)：

   * 如果選取「Hours」(小時)、「Days」(天)、「Weeks」(週)或「Months」(月)，必須一併指定頻率。您也可以選取「Custom」(自訂)，自行指定重複頻率。您可以選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
   * 如果選取「On-demand」，這項資料移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 如果選取「Event-driven」(以事件為依據)，則須一併指定**Pub/Sub 訂閱項目**。請選取[訂閱項目](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a subscription」(建立訂閱項目)。這個選項會啟用[以事件為依據的移轉作業](https://docs.cloud.google.com/bigquery/docs/event-driven-transfer?hl=zh-tw)，事件傳送至 Pub/Sub 訂閱項目時，就會觸發移轉作業。

     **注意事項：**您必須完成所有[必要設定](https://docs.cloud.google.com/bigquery/docs/event-driven-transfer?hl=zh-tw#gcs-event-driven-transfers)，才能進行以事件為依據的移轉作業。
6. 在「Destination settings」(目的地設定) 部分：

   * 在「Dataset」(資料集) 部分，選取您為了儲存資料而建立的資料集。
   * 如要移轉至 BigQuery 資料表，請選取「Native table」(原生資料表)。
   * 如要移轉至 Iceberg 代管資料表，請選取「Iceberg Managed」。
7. 在「Data source details」(資料來源詳細資料) 區段：

   1. 在「Destination table」(目標資料表) 中輸入目標資料表的名稱。
      目的地資料表的名稱必須符合[資料表命名規則](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#table_naming)，並支援[參數](https://docs.cloud.google.com/bigquery/docs/gcs-transfer-parameters?hl=zh-tw)。
   2. 在「Cloud Storage URI」輸入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw#google-cloud-storage-uri)。可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw#wildcard-support)和[參數](https://docs.cloud.google.com/bigquery/docs/gcs-transfer-parameters?hl=zh-tw)。如果 URI 與所有檔案都不相符，不會覆寫目的地資料表中任何資料。
   3. 「Write preference」(寫入偏好設定) 提供下列選項：

      * 「APPEND」(附加)：逐步將新的資料附加至現有目的地資料表。「Write preference」(寫入偏好設定) 的預設值為「APPEND」(附加)。
      * 「MIRROR」(建立鏡像)：每次資料移轉時，覆寫目的地資料表資料。

      如要進一步瞭解 BigQuery 資料移轉服務如何使用「APPEND」(附加) 或「MIRROR」(建立鏡像) 來擷取資料，請參閱 [Cloud Storage 移轉作業資料擷取](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw#data-ingestion)的相關說明。
      如要進一步瞭解 `writeDisposition` 欄位，請參閱 [`JobConfigurationLoad`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationload)。
   4. 如要在每次成功移轉資料後刪除來源檔案，請勾選「Delete source files after transfer」方塊。系統會盡可能執行刪除工作，但不保證一定達成。如果第一次刪除來源檔案失敗，不會再重試。
   5. 在「Transfer Options」部分執行下列操作：

      1. 在「All Formats」底下：
         1. 在「Number of errors allowed」(允許的錯誤數量) 欄位中，輸入 BigQuery 在執行工作時可忽略的錯誤記錄數量上限。如果損壞記錄數量超過這個值，該項工作就會失敗，並在結果傳回 `invalid` 錯誤。預設值為 `0`。
         2. (選用步驟) 在「Decimal target types」部分，輸入以半形逗號分隔的清單，內含來源小數值可能轉換成的 SQL 資料類型。系統會依據下列條件，選取要轉換的 SQL 資料類型：
            * 系統會按照 `NUMERIC`、[`BIGNUMERIC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_types) 和 `STRING` 的順序，選取下列清單中第一個支援來源資料有效位數和小數位數的資料類型，用來轉換。
            * 如果清單中的資料類型都不支援有效位數和小數位數，則會選取指定清單中支援範圍最廣的資料類型。如果讀取來源資料時，值超過支援的範圍，就會擲回錯誤。
            * 資料類型 `STRING` 支援所有有效位數和小數位數值。
            * 如果將這個欄位留空，ORC 的預設資料類型為 `NUMERIC,STRING`，其他檔案格式則為 `NUMERIC`。
            * 這個欄位不得含有重複的資料類型。
            * 您在這個欄位提供資料類型時採用的順序不會有影響。
      2. 如要在移轉資料時，捨棄不符合目的地資料表結構定義的資料，請勾選「JSON, CSV」(JSON、CSV) 底下的「Ignore unknown values」(略過不明的值) 方塊。
      3. 如果您希望資料移轉作業將 Avro 邏輯類型轉換為對應的 BigQuery 資料類型，請在「AVRO」底下勾選「Use avro logical types」方塊。預設會忽略多數類型的 `logicalType` 屬性，並改用基礎 Avro 類型。
      4. 在「CSV」**CSV** 下方：

         1. 在「Field delimiter」(欄位分隔符號) 部分輸入分隔欄位的字元。預設值為半形逗號。
         2. 在「Quote character」(引用字元) 輸入 CSV 檔案中用來引用資料區段的字元，預設值為英文雙引號 (`"`)。
         3. 如果您不想匯入來源檔案中的標題列，請在「Header rows to skip」(要略過的標題列) 輸入不要匯入的標題列數。預設值為 `0`。
         4. 如果要允許在引用欄位中使用換行符號，請勾選 [Allow quoted newlines] (允許引用換行符號) 的方塊。
         5. 若允許移轉缺少 `NULLABLE` 資料欄的資料列，請勾選「Allow jagged rows (CSV)」(允許空值資料列 (CSV)) 方塊。

         請參閱[此處](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#csv-options)，進一步瞭解 CSV 適用選項。
8. 在「Service Account」(服務帳戶) 選單，選取與貴組織 Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與資料移轉作業建立關聯，這樣就不需要使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)。

   * 如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立資料移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立資料移轉作業。
   * 服務帳戶必須具備 BigQuery 和 Cloud Storage 的[必要權限](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw#required_permissions)。
9. 選用步驟：在「Notification options」(通知選項) 部分執行下列操作：

   1. 按一下啟用電子郵件通知的切換開關。啟用這個選項之後，若移轉失敗，資料移轉設定的擁有者會收到電子郵件通知。
   2. 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
10. 選用步驟：如果您使用 [CMEK](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)，請在「Advanced options」(進階選項) 部分選取「Customer-managed key」(客戶管理的金鑰)，畫面隨即會列出可用的 CMEK 供您選擇。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱[指定移轉作業加密金鑰](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw#CMEK)的相關說明。
11. 按一下 [儲存]。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。還需加上以下旗標：

* `--data_source`
* `--display_name`
* `--target_dataset`
* `--params`

選用標記：

* `--destination_kms_key`：如果您使用客戶自行管理的加密金鑰 (CMEK) 進行這項資料移轉作業，請指定 Cloud KMS 金鑰的[金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱「[指定移轉作業加密金鑰](#CMEK)」。
* `--service_account_name`：指定要用於 Cloud Storage 移轉驗證的服務帳戶，而非使用者帳戶。

使用 bq 指令列工具設定 Cloud Storage 資料移轉作業時，須遵守下列限制：

* 您無法使用 bq 指令列工具設定移轉排程。
  使用 bq 指令列工具建立 Cloud Storage 資料移轉作業時，系統會使用「Schedule」(排程) 的預設值 (每 24 小時) 設定移轉設定。
* 您無法使用 bq 指令列工具設定通知。

下列範例顯示使用所有必要參數建立 Cloud Storage 資料移轉作業的指令：

```
bq mk \
--transfer_config \
--project_id=PROJECT_ID \
--data_source=DATA_SOURCE \
--display_name=NAME \
--target_dataset=DATASET \
--destination_kms_key="DESTINATION_KEY" \
--params='PARAMETERS' \
--service_account_name=SERVICE_ACCOUNT_NAME
```

更改下列內容：

* PROJECT\_ID 是您的專案 ID。如未提供 `--project_id` 指定特定專案，系統會使用預設專案。
* DATA\_SOURCE 是資料來源，例如 `google_cloud_storage`。
* NAME 是資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATASET 是移轉設定的目標資料集。
* DESTINATION\_KEY：[Cloud KMS 金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)，例如 `projects/project_name/locations/us/keyRings/key_ring_name/cryptoKeys/key_name`。
* PARAMETERS 包含所建立移轉設定的參數，格式為 JSON。例如：`--params='{"param":"param_value"}'`。
  + `destination_table_name_template`：目的地 BigQuery 資料表的名稱。
  + `data_path_template`：包含要轉移檔案的 Cloud Storage URI。可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw#wildcard-support)和[參數](https://docs.cloud.google.com/bigquery/docs/gcs-transfer-parameters?hl=zh-tw)。
  + `write_disposition`：決定是否將相符的檔案附加至目的地資料表，或完全鏡像處理。支援的值為 `APPEND` 或 `MIRROR`。如要瞭解 BigQuery 資料移轉服務如何在 Cloud Storage 移轉作業中附加或建立資料鏡像，請參閱「[Cloud Storage 移轉作業資料擷取](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw#data-ingestion)」。
  + `file_format`：要移轉的檔案格式。格式可以是 `CSV`、`JSON`、`AVRO`、`PARQUET` 或 `ORC`。預設值為 `CSV`。
  + `max_bad_records`：對於任何 `file_format` 值，可忽略的不良記錄數量上限。預設值為 `0`。
  + `decimal_target_types`：針對任何 `file_format` 值，以半形逗號分隔的清單，列出來源小數值可能轉換成的 SQL 資料類型。如未提供這個欄位，`ORC` 的資料類型預設為 `"NUMERIC,STRING"`，其他檔案格式則為 `"NUMERIC"`。
  + `ignore_unknown_values`：針對任何 `file_format` 值，設為 `TRUE` 即可接受含有與結構定義不符值的資料列。詳情請參閱[`JobConfigurationLoad`參考表格](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.ignore_unknown_values)中的「`ignoreUnknownvalues`」欄位詳細資料。
  + `use_avro_logical_types`：如果是 `AVRO` `file_format` 值，請設為 `TRUE`，將邏輯類型解讀為對應類型 (例如 `TIMESTAMP`)，而非僅使用原始類型 (例如 `INTEGER`)。
  + `parquet_enum_as_string`：針對 `PARQUET` `file_format` 值，請設為 `TRUE`，將 `PARQUET` `ENUM` 邏輯型別推斷為 `STRING`，而非預設的 `BYTES`。
  + `parquet_enable_list_inference`：如為 `PARQUET` `file_format` 值，請設為 `TRUE`，以便專門針對 `PARQUET` `LIST` 邏輯型別使用結構定義推論