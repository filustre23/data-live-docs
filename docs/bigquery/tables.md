Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立及使用資料表

本文說明如何在 [BigQuery](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables) 中建立及使用標準 (內建) 資料表。如要瞭解如何建立其他類型的資料表，請參閱下列文章：

* [建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)
* [建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)

建立資料表後，您可以執行下列作業：

* 控管資料表資料的存取權。
* 取得資料表的相關資訊。
* 列出資料集中的資料表。
* 取得資料表中繼資料。

如要進一步瞭解如何管理資料表，包括更新資料表屬性、複製資料表及刪除資料表，請參閱[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)一文。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文各項工作所需的權限。

### 必要的角色

如要取得建立資料表所需的權限，請要求管理員授予您下列 IAM 角色：

* 如果您要透過載入資料或將查詢結果儲存至資料表來建立資料表，請在專案中指派 [BigQuery Job User](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)。
* 資料集的「BigQuery 資料編輯者」 (`roles/bigquery.dataEditor`)，您要在該資料集建立資料表。

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備建立表格所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立資料表，您必須具備下列權限：

* `bigquery.tables.create`
  在要建立資料表的資料集上。
* `bigquery.tables.getData`
  如果您要將查詢結果儲存為資料表，則必須擁有查詢參照的所有資料表和檢視區塊的存取權。
* `bigquery.jobs.create`
  專案，如果您是透過載入資料或將查詢結果儲存至資料表來建立資料表。
* `bigquery.tables.updateData`
  資料表，如果您要使用查詢結果附加或覆寫資料表，就需要這個權限。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

**注意：** 如果您擁有 `bigquery.datasets.create` 權限，可以在建立的資料集中建立資料表。

## 資料表命名

在 BigQuery 中建立資料表時，每個資料集裡的資料表名稱不得重複。資料表名稱可以：

* 包含的字元總計最多 1,024 個 UTF-8 位元組。
* 包含類別 L (字母)、M (標記)、N (數字)、Pc (連接符，包括底線)、Pd (破折號)、Zs (空格) 的 Unicode 字元。詳情請參閱「[一般類別](https://wikipedia.org/wiki/Unicode_character_property#General_Category)」。

以下都是有效的資料表名稱範例：`table 01`、`ग्राहक`、`00_お客様`、`étudiant-01`。

注意事項：

* 根據預設，資料表名稱會區分大小寫。`mytable` 和 `MyTable` 可以共存在同一個資料集中，除非是[已關閉大小寫區分功能的資料集](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_case-insensitive_dataset)。
* 部分資料表名稱和資料表名稱前置字串已保留。如果收到錯誤訊息，指出資料表名稱或前置字元已保留，請選取其他名稱，然後再試一次。
* 如果您在序列中加入多個點運算子 (`.`)，系統會自動移除重複的運算子。

  例如：
  `project_name....dataset_name..table_name`

  變成這樣：
  `project_name.dataset_name.table_name`

## 製作表格

您可以在 BigQuery 中透過下列方式建立資料表：

* 手動使用 Google Cloud 控制台或 bq 指令列工具
  [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令。
* 呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) API 方法，透過程式建立。
* 使用用戶端程式庫。
* 從查詢結果建立。
* 定義參照外部資料來源的資料表。
* 載入資料時建立。
* 使用[`CREATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_new_table)資料定義語言 (DDL) 陳述式。

### 建立具有結構定義的空白資料表

您可以透過下列方式，建立具有結構定義的空白資料表：

* 使用 Google Cloud 控制台輸入結構定義。
* 使用 bq 指令列工具以內嵌方式提供結構定義。
* 使用 bq 指令列工具提交 JSON 結構定義檔案。
* 呼叫 API 的 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)時，在[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#resource:-table)中提供結構定義。

如要進一步瞭解如何指定資料表結構定義，請參閱[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)一文。

您可以在建立資料表後於其中[載入資料](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)，或透過[寫入查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw)填入資料。

如何建立含結構定義的空白資料表：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「來源」部分，從「建立資料表來源」清單中選取「空白資料表」。
2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。
   你可以使用下列任一方法手動輸入結構定義資訊：
   * 選項 1：按一下「以文字形式編輯」，然後以 JSON 陣列的形式貼上結構定義。如果您使用 JSON 陣列，可透過與[建立 JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)一樣的程序產生結構定義。您可以輸入下列指令，查看現有資料表的 JSON 格式結構定義：

     ```
         bq show --format=prettyjson dataset.table
     ```
   * 選項 2：按一下 add\_box
     「新增欄位」，然後輸入表格結構定義。指定每個欄位的「Name」(名稱)、「[Type](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#standard_sql_data_types)」(類型) 和「[Mode](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#modes)」(模式)。
4. 選用：指定「分區與叢集設定」。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。
5. 選用步驟：如要使用客戶自行管理的加密金鑰，請在「Advanced options」(進階選項) 部分選取「Use a customer-managed encryption key (CMEK)」(使用客戶自行管理的加密金鑰 (CMEK)) 選項。根據預設，BigQuery 會使用 Google-owned and Google-managed encryption key[加密靜態儲存的客戶內容](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
6. 點選「建立資料表」。

**注意：** 使用 Google Cloud 控制台建立空白資料表時，您無法新增標籤、說明或到期時間。您可以在使用 bq 指令列工具或 API 建立資料表時，新增這些選用屬性。在 Google Cloud 控制台中建立資料表後，即可新增到期時間、說明和標籤。

### SQL

下列範例會建立名為 `newtable` 的資料表，並將到期日設為 2023 年 1 月 1 日：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE mydataset.newtable (
     x INT64 OPTIONS (description = 'An optional INTEGER field'),
     y STRUCT <
       a ARRAY <STRING> OPTIONS (description = 'A repeated STRING field'),
       b BOOL
     >
   ) OPTIONS (
       expiration_timestamp = TIMESTAMP '2023-01-01 00:00:00 UTC',
       description = 'a table that expires in 2023',
       labels = [('org_unit', 'development')]);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 請使用 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)，並加上 `--table` 或 `-t` 旗標。您可以透過內嵌方式或 JSON 結構定義檔提供資料表結構定義資訊。如需完整的參數清單，請參閱 [`bq mk --table` 參考資料](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)。部分選用參數包括：

   * `--expiration`
   * `--description`
   * `--time_partitioning_field`
   * `--time_partitioning_type`
   * `--range_partitioning`
   * `--clustering_fields`
   * `--destination_kms_key`
   * `--label`

   `--time_partitioning_field`、`--time_partitioning_type`、`--range_partitioning`、`--clustering_fields` 和 `--destination_kms_key` 不在此處示範。如要進一步瞭解這些選用參數，請參閱下列連結：

   * 如要進一步瞭解 `--time_partitioning_field`、`--time_partitioning_type` 和 `--range_partitioning`，請參閱[分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)。
   * 如要進一步瞭解 `--clustering_fields`，請參閱[叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)。
   * 如要進一步瞭解 `--destination_kms_key`，請參閱[客戶管理的加密金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。

   如要建立非預設專案中的資料表，請使用下列格式將專案 ID 新增至資料集：`project_id:dataset`。

   如要在具有結構定義的現有資料集中建立空白資料表，請輸入下列內容：

   ```
   bq mk \
   --table \
   --expiration=integer \
   --description=description \
   --label=key_1:value_1 \
   --label=key_2:value_2 \
   --add_tags=key_3:value_3[,...] \
   project_id:dataset.table \
   schema
   ```

   更改下列內容：

   * integer 是資料表的預設生命週期 (以秒為單位)，最小值是 3600 秒 (1 小時)。到期時間為目前世界標準時間加上 [INTEGER] 中的整數值。如果您在建立資料表時設定了資料表的到期時間，則系統會忽略資料集的預設資料表到期時間設定。
   * description 是置於括號中的資料表說明。
   * key\_1:value\_1 和 key\_2:value\_2 是指定[標籤](https://docs.cloud.google.com/bigquery/docs/labels?hl=zh-tw)的鍵/值組合。
   * key\_3：value\_3 是指定[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)的鍵值組。在相同旗標下新增多個標記，並以逗號分隔鍵/值組合。
   * project\_id 是您的專案 ID。
   * dataset 是專案中的資料集。
   * table 是您所建立的資料表名稱。
   * schema 是格式為 field:data\_type,field:data\_type 的內嵌結構定義，或本機上 JSON 結構定義檔的路徑。

   在指令列中指定結構定義時，無法加入 `RECORD` ([`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)) 類型和資料欄說明，也不能指定資料欄模式。所有模式均會使用預設設定 `NULLABLE`。如要加入說明、模式和 `RECORD` 類型，請改為提供 [JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)。

   範例：

   輸入以下指令，使用內嵌結構定義建立資料表。這個指令會在預設專案的 `mydataset` 中建立名為 `mytable` 的資料表。資料表的到期時間設為 3600 秒 (一小時)、說明設為 `This is my table`，標籤則設為 `organization:development`。此指令使用 `-t` 捷徑，而非 `--table`。結構定義以內嵌方式指定為：`qtr:STRING,sales:FLOAT,year:STRING`。

   ```
   bq mk \
    -t \
    --expiration 3600 \
    --description "This is my table" \
    --label organization:development \
    mydataset.mytable \
    qtr:STRING,sales:FLOAT,year:STRING
   ```

   輸入下列指令，使用 JSON 結構定義檔建立資料表。這個指令會在預設專案的 `mydataset` 中建立名為 `mytable` 的資料表。資料表的到期時間設為 3600 秒 (一小時)、說明設為 `This is my table`，標籤則設為 `organization:development`。結構定義檔的路徑為 `/tmp/myschema.json`。

   ```
   bq mk \
    --table \
    --expiration 3600 \
    --description "This is my table" \
    --label organization:development \
    mydataset.mytable \
    /tmp/myschema.json
   ```

   輸入下列指令，使用 JSON 結構定義檔建立資料表。這個指令會在 `myotherproject` 的 `mydataset` 中建立名為 `mytable` 的資料表。資料表的到期時間設為 3600 秒 (一小時)、說明設為 `This is my table`，標籤則設為 `organization:development`。結構定義檔的路徑為 `/tmp/myschema.json`。

   ```
   bq mk \
    --table \
    --expiration 3600 \
    --description "This is my table" \
    --label organization:development \
    myotherproject:mydataset.mytable \
    /tmp/myschema.json
   ```

   您可以在建立資料表後，[更新](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)資料表的到期時間、說明和標籤。您也可以[修改結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。

### Terraform

請使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 Cloud Resource Manager API。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

**建立表格**

以下範例會建立名為 `mytable` 的資料表：

```
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "mydataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

  labels = {
    billing_group = "accounting",
    pii           = "sensitive"
  }
}

resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = "mytable"

  schema = <<EOF
[
  {
    "name": "ID",
    "type": "INT64",
    "mode": "NULLABLE",
    "description": "Item ID"
  },
  {
    "name": "Item",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

}
```

**建立資料表並授予存取權**

下列範例會建立名為 `mytable` 的資料表，然後使用 [`google_bigquery_table_iam_policy`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table_iam#google_bigquery_table_iam_policy) 資源授予存取權。只有在您想將資料表存取權授予給無權存取資料表所屬資料集的主體時，才需要執行這個步驟。

```
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "mydataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

  labels = {
    billing_group = "accounting",
    pii           = "sensitive"
  }
}

resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = "mytable"

  schema = <<EOF
[
  {
    "name": "ID",
    "type": "INT64",
    "mode": "NULLABLE",
    "description": "Item ID"
  },
  {
    "name": "Item",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

}

data "google_iam_policy" "default" {
  binding {
    role = "roles/bigquery.dataOwner"
    members = [
      "user:raha@altostrat.com",
    ]
  }
}

resource "google_bigquery_table_iam_policy" "policy" {
  dataset_id  = google_bigquery_table.default.dataset_id
  table_id    = google_bigquery_table.default.table_id
  policy_data = data.google_iam_policy.default.policy_data
}
```

**使用客戶管理的加密金鑰建立資料表**

下列範例會建立名為 `mytable` 的資料表，並使用 [`google_kms_crypto_key`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/kms_crypto_key) 和 [`google_kms_key_ring`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/kms_key_ring) 資源，為資料表指定 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。您必須先[啟用 Cloud Key Management Service API](https://console.cloud.google.com/flows/enableapi?apiid=cloudkms.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com%2F&hl=zh-tw)，才能執行這個範例。

```
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "mydataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

  labels = {
    billing_group = "accounting",
    pii           = "sensitive"
  }
}

resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = "mytable"

  schema = <<EOF
[
  {
    "name": "ID",
    "type": "INT64",
    "mode": "NULLABLE",
    "description": "Item ID"
  },
  {
    "name": "Item",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

  encryption_configuration {
    kms_key_name = google_kms_crypto_key.crypto_key.id
  }

  depends_on = [google_project_iam_member.service_account_access]
}

resource "google_kms_crypto_key" "crypto_key" {
  name     = "example-key"
  key_ring = google_kms_key_ring.key_ring.id
}

resource "random_id" "default" {
  byte_length = 8
}

resource "google_kms_key_ring" "key_ring" {
  name     = "${random_id.default.hex}-example-keyring"
  location = "us"
}

# Enable the BigQuery service account to encrypt/decrypt Cloud KMS keys
data "google_project" "project" {
}

resource "google_project_iam_member" "service_account_access" {
  project = data.google_project.project.project_id
  role    = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member  = "serviceAccount:bq-${data.google_project.project.number}@bigquery-encryption.iam.gserviceaccount.com"
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

使用已定義的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;

public class BigQueryCreateTable
{
    public BigQueryTable CreateTable(
        string projectId = "your-project-id",
        string datasetId = "your_dataset_id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        var dataset = client.GetDataset(datasetId);
        // Create schema for new table.
        var schema = new TableSchemaBuilder
        {
            { "full_name", BigQueryDbType.String },
            { "age", BigQueryDbType.Int64 }
        }.Build();
        // Create the table
        return dataset.CreateTable(tableId: "your_table_id", schema: schema);
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
)

// createTableExplicitSchema demonstrates creating a new BigQuery table and specifying a schema.
func createTableExplicitSchema(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydatasetid"
	// tableID := "mytableid"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	sampleSchema := bigquery.Schema{
		{Name: "full_name", Type: bigquery.StringFieldType},
		{Name: "age", Type: bigquery.IntegerFieldType},
	}

	metaData := &bigquery.TableMetadata{
		Schema:         sampleSchema,
		ExpirationTime: time.Now().AddDate(1, 0, 0), // Table will be automatically deleted in 1 year.
	}
	tableRef := client.Dataset(datasetID).Table(tableID)
	if err := tableRef.Create(ctx, metaData); err != nil {
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.StandardTableDefinition;
import com.google.cloud.bigquery.TableDefinition;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;

public class CreateTable {

  public static void runCreateTable() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    Schema schema =
        Schema.of(
            Field.of("stringField", StandardSQLTypeName.STRING),
            Field.of("booleanField", StandardSQLTypeName.BOOL));
    createTable(datasetName, tableName, schema);
  }

  public static void createTable(String datasetName, String tableName, Schema schema) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      TableDefinition tableDefinition = StandardTableDefinition.of(schema);
      TableInfo tableInfo = TableInfo.newBuilder(tableId, tableDefinition).build();

      bigquery.create(tableInfo);
      System.out.println("Table created successfully");
    } catch (BigQueryException e) {
      System.out.println("Table was not created. \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library and create a client
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function createTable() {
  // Creates a new table named "my_table" in "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";
  // const schema = 'Name:string, Age:integer, Weight:float, IsMagic:boolean';

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
  const options = {
    schema: schema,
    location: 'US',
  };

  // Create a new table in the dataset
  const [table] = await bigquery
    .dataset(datasetId)
    .createTable(tableId, options);

  console.log(`Table ${table.id} created.`);
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/** Uncomment and populate these variables in your code */
// $projectId = 'The Google project ID';
// $datasetId = 'The BigQuery dataset ID';
// $tableId = 'The BigQuery table ID';
// $fields = [
//    [
//        'name' => 'field1',
//        'type' => 'string',
//        'mode' => 'required'
//    ],
//    [
//        'name' => 'field2',
//        'type' => 'integer'
//    ],
//];

$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$dataset = $bigQuery->dataset($datasetId);
$schema = ['fields' => $fields];
$table = $dataset->createTable($tableId, ['schema' => $schema]);
printf('Created table %s' . PHP_EOL, $tableId);
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"

schema = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def create_table dataset_id = "my_dataset"
  bigquery = Google::Cloud::Bigquery.new
  dataset  = bigquery.dataset dataset_id
  table_id = "my_table"

  table = dataset.create_table table_id do |updater|
    updater.string  "full_name", mode: :required
    updater.integer "age",       mode: :required
  end

  puts "Created table: #{table_id}"
end
```

### 建立不含結構定義的空白資料表

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardTableDefinition;
import com.google.cloud.bigquery.TableDefinition;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;

// Sample to create a table without schema
public class CreateTableWithoutSchema {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    createTableWithoutSchema(datasetName, tableName);
  }

  public static void createTableWithoutSchema(String datasetName, String tableName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      TableDefinition tableDefinition = StandardTableDefinition.of(Schema.of());
      TableInfo tableInfo = TableInfo.newBuilder(tableId, tableDefinition).build();

      bigquery.create(tableInfo);
      System.out.println("Table created successfully");
    } catch (BigQueryException e) {
      System.out.println("Table was not created. \n" + e.toString());
    }
  }
}
```

### 從查詢結果建立資料表

如要從查詢結果建立資料表，請將結果寫入目標資料表。

### 控制台

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在查詢編輯器中輸入有效的 SQL 查詢。
5. 按一下「更多」，然後選取「查詢設定」。
6. 選取「為查詢結果設定目標資料表」選項。
7. 在「目的地」部分，選取要建立資料表的「資料集」，然後選擇「資料表 ID」。
8. 在「Destination table write preference」(目標資料表寫入偏好設定) 區段，選擇下列其中一項：

   * [Write if empty] (空白時寫入)：僅在資料表空白時將查詢結果寫入資料表。
   * [Append to table] (附加到資料表中)：將查詢結果附加到現有的資料表。
   * [Overwrite table] (覆寫資料表)：使用查詢結果覆寫名稱相同的現有資料表。
9. 選用：針對「Data location」(資料位置)，選擇您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
10. 如要更新查詢設定，請按一下「儲存」。
11. 按一下「執行」。這會建立一個查詢工作，將查詢結果寫入您指定的資料表。

如果您在執行查詢前忘記指定目的地資料表，也可以按一下編輯器上方的 [[Save Results] (儲存結果)](#save-query-results) 按鈕，將快取結果資料表複製至永久資料表。

### SQL

以下範例使用 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，從公開 `bikeshare_trips` 資料表中的資料建立 `trips` 資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE mydataset.trips AS (
     SELECT
       bike_id,
       start_time,
       duration_minutes
     FROM
       bigquery-public-data.austin_bikeshare.bikeshare_trips
   );
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

詳情請參閱「[從現有資料表建立新資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_new_table_from_an_existing_table)」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令並指定 `--destination_table` 旗標，根據查詢結果建立永久資料表。指定 `use_legacy_sql=false` 旗標以使用 GoogleSQL 語法。如要將查詢結果寫入不在預設專案內的資料表，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

   選用：提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

   如要控管現有目的地資料表的寫入配置，請指定以下其中一種選用旗標：

   * `--append_table`：如果目的地資料表已存在，查詢結果會附加至該資料表。
   * `--replace`：如果目的地資料表已存在，查詢結果會覆寫該資料表。

     ```
     bq --location=location query \
     --destination_table project_id:dataset.table \
     --use_legacy_sql=false 'query'
     ```

     更改下列內容：
   * `location` 是用於處理查詢的位置名稱，`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
   * `project_id` 是您的專案 ID。
   * `dataset` 是包含您要寫入查詢結果之資料表的資料集名稱。
   * `table` 是您要寫入查詢結果的資料表名稱。
   * `query` 是採用 GoogleSQL 語法的查詢。

     如未指定任何寫入配置旗標，預設動作是僅在資料表空白時，才將結果寫入資料表。如果資料表存在但並非空白，系統會傳回下列錯誤：`BigQuery error in query operation: Error processing job
     project_id:bqjob_123abc456789_00000e1234f_1: Already
     Exists: Table project_id:dataset.table`。

     範例：

     **注意：**這些範例會查詢位於美國的公開資料集。由於該公開資料集儲存在美國的多地區位置，因此您目的地資料表所屬的資料集也必須位於美國。您無法查詢位於某個位置的資料集，然後將結果寫入位於另一個位置的目的地資料表。 

     輸入下列指令，將查詢結果寫入 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於預設專案中。由於您未在指令中指定任何寫入配置旗標，因此資料表必須為新資料表或空白資料表。否則，系統會傳回 `Already exists` 錯誤。查詢會從[美國人名資料公開資料集](https://console.cloud.google.com/marketplace/product/social-security-administration/us-names?hl=zh-tw)中擷取資料。

     ```
     bq query \
     --destination_table mydataset.mytable \
     --use_legacy_sql=false \
     'SELECT
     name,
     number
     FROM
     `bigquery-public-data`.usa_names.usa_1910_current
     WHERE
     gender = "M"
     ORDER BY
     number DESC'
     ```

     輸入下列指令，使用查詢結果覆寫 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於預設專案中。該指令使用 `--replace` 旗標來覆寫目標資料表。

     ```
     bq query \
     --destination_table mydataset.mytable \
     --replace \
     --use_legacy_sql=false \
     'SELECT
     name,
     number
     FROM
     `bigquery-public-data`.usa_names.usa_1910_current
     WHERE
     gender = "M"
     ORDER BY
     number DESC'
     ```

     輸入下列指令，將查詢結果附加至 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於 `my-other-project`，而非預設專案。指令使用 `--append_table` 旗標將查詢結果附加至目的地資料表。

     ```
     bq query \
     --append_table \
     --use_legacy_sql=false \
     --destination_table my-other-project:mydataset.mytable \
     'SELECT
     name,
     number
     FROM
     `bigquery-public-data`.usa_names.usa_1910_current
     WHERE
     gender = "M"
     ORDER BY
     number DESC'
     ```

     各範例的輸出內容如下。為了方便閱讀，以下僅顯示部分輸出內容。

     ```
     Waiting on bqjob_r123abc456_000001234567_1 ... (2s) Current status: DONE
     +---------+--------+
     |  name   | number |
     +---------+--------+
     | Robert  |  10021 |
     | John    |   9636 |
     | Robert  |   9297 |
     | ...              |
     +---------+--------+
     ```

### API

如要將查詢結果儲存至永久資料表，請呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法，設定 `query` 工作，然後加入 `destinationTable` 屬性的值。如要控管現有目標資料表的寫入配置，請設定 `writeDisposition` 屬性。

如要控管查詢工作的處理位置，請在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中指定 `location` 屬性。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// queryWithDestination demonstrates saving the results of a query to a specific table by setting the destination
// via the API properties.
func queryWithDestination(w io.Writer, projectID, destDatasetID, destTableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	q := client.Query("SELECT 17 as my_col")
	q.Location = "US" // Location must match the dataset(s) referenced in query.
	q.QueryConfig.Dst = client.Dataset(destDatasetID).Table(destTableID)
	// Run the query and print results when the query job is completed.
	job, err := q.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}
	if err := status.Err(); err != nil {
		return err
	}
	it, err := job.Read(ctx)
	for {
		var row []bigquery.Value
		err := it.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintln(w, row)
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要將查詢結果儲存至永久資料表，請在 [QueryJobConfiguration](https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration?hl=zh-tw) 中將[目標資料表](https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration.Builder?hl=zh-tw#com_google_cloud_bigquery_QueryJobConfiguration_Builder_setDestinationTable_com_google_cloud_bigquery_TableId_)設為所要的 [TableId](https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.TableId?hl=zh-tw)。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableId;

public class SaveQueryToTable {

  public static void runSaveQueryToTable() {
    // TODO(developer): Replace these variables before running the sample.
    String query = "SELECT corpus FROM `bigquery-public-data.samples.shakespeare` GROUP BY corpus;";
    String destinationTable = "MY_TABLE";
    String destinationDataset = "MY_DATASET";

    saveQueryToTable(destinationDataset, destinationTable, query);
  }

  public static void saveQueryToTable(
      String destinationDataset, String destinationTableId, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Identify the destination table
      TableId destinationTable = TableId.of(destinationDataset, destinationTableId);

      // Build the query job
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query).setDestinationTable(destinationTable).build();

      // Execute the query.
      bigquery.query(queryConfig);

      // The results are now saved in the destination table.

      System.out.println("Saved query ran successfully");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Saved query did not run \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function queryDestinationTable() {
  // Queries the U.S. given names dataset for the state of Texas
  // and saves results to permanent table.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  // Create destination table reference
  const dataset = bigquery.dataset(datasetId);
  const destinationTable = dataset.table(tableId);

  const query = `SELECT name
    FROM \`bigquery-public-data.usa_names.usa_1910_2013\`
    WHERE state = 'TX'
    LIMIT 100`;

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
  const options = {
    query: query,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
    destination: destinationTable,
  };

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(options);

  console.log(`Job ${job.id} started.`);
  console.log(`Query results loaded to table ${destinationTable.id}`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要將查詢結果儲存至永久性資料表，請建立 [QueryJobConfig](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob)，並將[目的地](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob_destination)設為所要的 [TableReference](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.TableReference?hl=zh-tw)。接著，將工作設定傳送至[查詢方法](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_query)。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the destination table.
# table_id = "your-project.your_dataset.your_table_name"

job_config = bigquery.QueryJobConfig(destination=table_id)

sql = """
    SELECT corpus
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus;
"""

# Start the query, passing in the extra configuration.
query_job = client.query(sql, job_config=job_config)  # Make an API request.
query_job.result()  # Wait for the job to complete.

print("Query results loaded to the table {}".format(table_id))
```

### 建立參照外部資料來源的資料表

「外部資料來源」是指可以直接透過 BigQuery 查詢的資料來源，即使資料未儲存在 BigQuery 儲存空間中也一樣。舉例來說，您可能有資料在其他 Google Cloud 資料庫、Cloud Storage 的檔案或其他雲端產品中，而且想在不遷移資料的狀況下，在 BigQuery 中進行分析。

詳情請參閱[外部資料來源簡介](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)。

### 在載入資料時建立資料表

將資料載入 BigQuery 時，您可將資料載入新的資料表或分區、將資料附加至現有的資料表或分區，或是覆寫資料表或分區。您不必在載入資料前先建立空白的資料表，因為系統可讓您在建立新資料表時一併載入資料。

將資料載入 BigQuery 時，您可以提供資料表或分區結構定義，或是將結構定義[自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)用於支援此功能的資料格式。

有關如何載入資料的詳情，請參閱[將資料載入 BigQuery 的簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)。

### 建立多模態資料表

您可以建立含有一個或多個 [`ObjectRef`](https://docs.cloud.google.com/bigquery/docs/objectref-columns?hl=zh-tw) 欄的資料表，以便儲存與資料表中其他結構化資料相關的非結構化資料中繼資料。舉例來說，在產品資料表中，您可以建立 `ObjectRef` 欄，儲存產品圖片資訊和其他產品資料。非結構化資料本身會儲存在 Cloud Storage 中，並透過[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)在 BigQuery 中提供。

如要瞭解如何建立多模態資料表，請參閱「[使用 SQL 和 BigQuery DataFrames 分析多模態資料](https://docs.cloud.google.com/bigquery/docs/multimodal-data-sql-tutorial?hl=zh-tw)」。

## 控管資料表的存取權

如要設定資料表和檢視表的存取權，您可以為下列層級的實體授予 IAM 角色，這些層級會依允許的資源範圍排序 (從最大到最小)：

* [Google Cloud 資源階層](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw)中的較高層級，例如專案、資料夾或機構層級
* 資料集層級
* 資料表或檢視畫面層級

您也可以使用下列方法，限制資料表中的資料存取權：

* [資料欄層級安全防護](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)
* [資料欄資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)
* [資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)

透過 IAM 保護的任何資源，存取權都是累加的。舉例來說，如果實體沒有專案等高層級的存取權，您可以授予實體資料集層級的存取權，這樣實體就能存取資料集中的資料表和檢視區塊。同樣地，如果實體沒有高層級或資料集層級的存取權，您可以在資料表或檢視表層級授予實體存取權。

在[Google Cloud資源階層](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw)中的較高層級 (例如專案、資料夾或機構層級) 授予 IAM 角色，可讓實體存取更多資源。舉例來說，在專案層級將特定角色授予實體，可讓該實體擁有適用於專案中所有資料集的權限。

在資料集層級授予角色，即可讓實體對特定資料集裡的資料表和檢視表執行指定作業，即使實體沒有較高層級的存取權也一樣。如要瞭解如何設定資料集層級的存取權控管設定，請參閱[控管資料集存取權](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-tw)一文。

在資料表或檢視表層級授予角色，即可讓實體對特定資料表和檢視表執行指定作業，即使實體沒有較高層級的存取權也一樣。如要瞭解如何設定資料表層級的存取權控管設定，請參閱[控管資料表和檢視區塊的存取權](https://docs.cloud.google.com/bigquery/docs/table-access-controls?hl=zh-tw)一文。

您也可以建立 [IAM 自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。建立自訂角色之後，您就能依據要讓實體執行的特定作業授予權限。

您無法對受 IAM 保護的任何資源設定「拒絕」權限。

如要進一步瞭解角色和權限，請參閱 IAM 說明文件中的「[瞭解角色](https://docs.cloud.google.com/iam/docs/understanding-roles?hl=zh-tw)」和 BigQuery 的「[IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 取得資料表相關資訊

您可以透過下列方式取得資料表的相關資訊或中繼資料：

* 使用 Google Cloud 控制台。
* 使用 bq 指令列工具的 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令。
* 呼叫 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) API 方法
* 使用用戶端程式庫。
* 查詢 [`INFORMATION_SCHEMA.VIEWS`](https://docs.cloud.google.com/bigquery/docs/information-schema-views?hl=zh-tw) 檢視畫面。

### 所需權限

您至少要具備 `bigquery.tables.get` 權限，才能取得資料表相關資訊。以下是具有 `bigquery.tables.get` 權限的預先定義 IAM 角色：

* `bigquery.metadataViewer`
* `bigquery.dataViewer`
* `bigquery.dataOwner`
* `bigquery.dataEditor`
* `bigquery.admin`

此外，當具備 `bigquery.datasets.create` 權限的使用者建立資料集時，會獲得該資料集的 `bigquery.dataOwner` 存取權。`bigquery.dataOwner` 存取權可讓使用者擷取資料表的中繼資料。

如要進一步瞭解 BigQuery 中的身分與存取權管理角色和權限，請參閱[存取權控管](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)。

### 取得資料表資訊

如何取得資料表的相關資訊：

### 控制台

1. 在導覽面板的「Resources」(資源) 區段中，展開您的專案，然後選取資料集。
2. 按一下資料集名稱來展開資料集，畫面上會顯示資料集中的資料表和檢視表。
3. 按一下資料表名稱。
4. 在「詳細資料」面板中，按一下「詳細資料」，即可顯示資料表的說明和相關資訊。
5. 您也可以切換至「結構定義」分頁標籤，查看資料表的結構定義。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。
2. 發出 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令，即可顯示所有資料表資訊。使用 `--schema` 旗標可以只顯示資料表結構定義資訊。`--format` 旗標可用來控制輸出內容。

   如果您要取得非預設專案中之資料表的相關資訊，請使用下列格式將專案 ID 新增至資料集：`project_id:dataset`。

   ```
   bq show \
   --schema \
   --format=prettyjson \
   project_id:dataset.table
   ```

   其中：

   * project\_id 是您的專案 ID。
   * dataset 是資料集名稱。
   * table 是資料表名稱。

   範例：

   輸入下列指令，顯示 `mydataset` 中 `mytable` 的所有相關資訊。`mydataset` 在您的預設專案中。

   ```
   bq show --format=prettyjson mydataset.mytable
   ```

   輸入下列指令，顯示 `mydataset` 中 `mytable` 的所有相關資訊。`mydataset` 在 `myotherproject` 中，而不是在您的預設專案中。

   ```
   bq show --format=prettyjson myotherproject:mydataset.mytable
   ```

   輸入下列指令，系統即會單獨顯示 `mydataset` 中 `mytable` 的結構定義資訊。`mydataset` 在 `myotherproject` 中，而不是在您的預設專案中。

   ```
   bq show --schema --format=prettyjson myotherproject:mydataset.mytable
   ```

### API

呼叫 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) 方法，並提供所有相關參數。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
)

// printTableInfo demonstrates fetching metadata from a table and printing some basic information
// to an io.Writer.
func printTableInfo(w io.Writer, projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background
```