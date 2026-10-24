Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立及使用資料表

標準資料表可讓您將資料儲存在 BigQuery 儲存空間，並在該處查詢資料、控管存取權限，以及稽核資料記錄。本文說明如何建立[標準 (內建) 資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)、控管資料表存取權，以及取得資料表相關資訊，例如資料表中繼資料和資料集中的資料表。

如要建立其他資料表類型，請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。如要更新表格屬性、複製表格或刪除表格，請參閱「[管理表格](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)」。

## 事前準備

授予 Identity and Access Management (IAM) 角色，讓使用者具備必要權限，可執行本文件中的各項工作。

### 必要的角色

如要取得建立資料表所需的權限，請要求管理員授予您下列 IAM 角色：

* 如要透過載入資料或將已儲存的查詢結果儲存至資料表的方式建立資料表，則須具備專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`) 角色。
* 在您要建立資料表的資料集，具備 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`) 角色。

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備建立資料表所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能建立資料表：

* `bigquery.tables.create`
  ，用於建立資料表的資料集。
* `bigquery.tables.getData`
  (如果您將查詢結果儲存為資料表，則須具備查詢參照的所有資料表和檢視表的 權限)。
* `bigquery.jobs.create`
  ：如要透過載入資料或將查詢結果儲存至資料表的方式建立資料表，則須具備這項權限。
* `bigquery.tables.updateData`
  ，如果使用查詢結果附加或覆寫資料表，則需要資料表的

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

**注意：** 如果您具備 `bigquery.datasets.create` 權限，則可在建立的資料集中建立資料表。

## 資料表命名

在 BigQuery 中建立資料表時，每個資料集裡的資料表名稱不得重複。資料表名稱可以：

* 包含總計最多 1,024 個 UTF-8 位元組的字元。
* 包含 L (字母)、M (標記)、N (數字)、Pc (連接符號，包括底線)、Pd (破折號)、Zs (空格) 類別的 Unicode 字元。詳情請參閱「[一般類別](https://wikipedia.org/wiki/Unicode_character_property#General_Category)」。

以下皆為有效的資料表名稱範例：`table 01`、`ग्राहक`、`00_お客様`、`étudiant-01`。

注意事項：

* 根據預設，資料表名稱會區分大小寫。`mytable` 和 `MyTable` 可以共存於同一個資料集，除非它們是[不區分大小寫的資料集](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_case-insensitive_dataset)的一部分。
* 部分資料表名稱和資料表名稱前置字元為保留字，如果收到錯誤訊息，指出資料表名稱或前置字串已保留，請選取其他名稱，然後再試一次。
* 如果您在序列中加入多個點運算子 (`.`)，系統會隱含移除重複的運算子。

  例如：
  `project_name....dataset_name..table_name`

  變成：
  `project_name.dataset_name.table_name`

## 製作表格

您可以在 BigQuery 中透過下列方式建立資料表：

* 使用 Google Cloud 控制台或 bq 指令列工具 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令手動建立。
* 透過程式輔助方式呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) API 方法。
* 使用用戶端程式庫。
* 從查詢結果。
* 定義參照外部資料來源的資料表。
* 載入資料時。
* 使用 [`CREATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_new_table) 資料定義語言 (DDL) 陳述式。

### 建立含有結構定義定義的空白資料表

您可以透過下列方式，建立含有結構定義定義的空白資料表：

* 使用 Google Cloud 控制台輸入結構定義。
* 使用 bq 指令列工具，提供內嵌結構定義。
* 使用 bq 指令列工具提交 JSON 結構定義檔案。
* 呼叫 API 的 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)時，在[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#resource:-table)中提供結構定義。

如要進一步瞭解如何指定資料表結構定義，請參閱「[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)」。

您可以在建立資料表後於其中[載入資料](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)，或透過[寫入查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw)填入資料。

如何建立含結構定義的空白資料表：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，點選「資料集」，然後選取資料集。
4. 在「資料集資訊」部分，點選 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「Source」(來源) 部分，從「Create table from」(建立資料表來源) 清單中選取「Empty table」(空白資料表)。
2. 在「Destination」(目的地) 部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要在其中建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位設為「原生資料表」。
3. 在「Schema」(結構定義) 部分，輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。您可以透過下列任一方法手動輸入結構定義資訊：
   * 方法 1：按一下「Edit as text」(以文字形式編輯)，然後以 JSON 陣列的形式貼上結構定義。使用 JSON 陣列時，您會按照[建立 JSON 結構定義檔案](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的相同程序產生結構定義。輸入下列指令，即可查看現有資料表的 JSON 格式結構定義：

     ```
         bq show --format=prettyjson dataset.table
     ```
   * 方法 2：按一下「Add field」(新增欄位)add\_box，然後輸入資料表結構定義。指定每個欄位的「Name」(名稱)、「Type」(類型) 和「Mode」(模式)。
4. 選用：指定**分區和叢集設定**。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。
5. 選用步驟：在「Advanced options」(進階選項) 部分，如要使用客戶自行管理的加密金鑰，請選取「Use a customer-managed encryption key (CMEK)」(使用客戶自行管理的加密金鑰 (CMEK)) 選項。根據預設，BigQuery 會使用 Google-owned and Google-managed encryption key[加密靜態儲存的客戶內容](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
6. 點選「建立資料表」。

**注意：** 使用 Google Cloud 控制台建立空白資料表時，無法新增標籤、說明或到期時間。使用 bq 指令列工具或 API 建立資料表時，可以新增這些選用屬性。在 Google Cloud 控制台建立資料表後，您可以新增到期時間、說明和標籤。

### SQL

以下範例會建立名為 `newtable` 的資料表，並將到期日設為 2023 年 1 月 1 日：

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
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

1. 在 Google Cloud 控制台啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 控制台底部會開啟 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已設定適用於您目前專案的值。工作階段可能要幾秒鐘的時間才能初始化。
2. 使用 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)，並加上 `--table` 或 `-t` 旗標。您可以內嵌提供資料表結構定義資訊，或使用 JSON 結構定義檔案。如需完整的參數清單，請參閱 [`bq mk --table` 參考資料](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)。部分選用參數包括：

   * `--expiration`
   * `--description`
   * `--time_partitioning_field`
   * `--time_partitioning_type`
   * `--range_partitioning`
   * `--clustering_fields`
   * `--destination_kms_key`
   * `--label`

   `--time_partitioning_field`、`--time_partitioning_type`、`--range_partitioning`、`--clustering_fields` 和 `--destination_kms_key` 不在此示範。如要進一步瞭解這些選用參數，請參閱下列連結：

   * 如要進一步瞭解 `--time_partitioning_field`、`--time_partitioning_type` 和 `--range_partitioning`，請參閱「[分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」。
   * 如要進一步瞭解 `--clustering_fields`，請參閱「[分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。
   * 如要進一步瞭解 `--destination_kms_key`，請參閱「[客戶自行管理的加密金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)」。

   如要建立非預設專案中的資料表，請使用下列格式將專案 ID 新增至資料集：`PROJECT_ID:DATASET`。

   如要在現有資料集中建立具有結構定義定義的空白資料表，請輸入下列指令：

   ```
   bq mk \
   --table \
   --expiration=INTEGER \
   --description=DESCRIPTION \
   --label=KEY_1:VALUE_1 \
   --label=KEY_2:VALUE_2 \
   --add_tags=KEY_3:VALUE_3[,...] \
   PROJECT_ID:DATASET.TABLE \
   SCHEMA
   ```

   更改下列內容：

   * `INTEGER` 是資料表的預設生命週期 (以秒為單位)，最小值是 3600 秒 (1 小時)。到期時間為目前世界標準時間加上 [INTEGER] 中的整數值。如果您在建立資料表時設定了資料表的到期時間，則系統會忽略資料集的預設資料表到期時間設定。
   * `DESCRIPTION` 是置於括號中的資料表說明。
   * `KEY_1:VALUE_1` 和 `KEY_2:VALUE_2` 是指定[標籤](https://docs.cloud.google.com/bigquery/docs/labels?hl=zh-tw)的鍵/值組合。
   * `KEY_3:VALUE_3` 是指定[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)的鍵/值組合。在同一個旗標下新增多個標記，並在鍵/值組合之間加上半形逗號。
   * `PROJECT_ID` 是您的專案 ID。
   * `DATASET` 是專案中的資料集。
   * `TABLE` 是您所建立的資料表名稱。
   * `SCHEMA` 是內嵌結構定義定義，格式為 `FIELD:DATA_TYPE,FIELD:DATA_TYPE`，或本機電腦上的 JSON 結構定義檔案路徑。

   在指令列中指定結構定義時，您無法加入 `RECORD` ([`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)) 類型、資料欄說明，也無法指定資料欄模式。所有模式均會使用預設設定 `NULLABLE`。如要加入說明、模式和 `RECORD` 類型，請改為提供 [JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)。

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

   輸入下列指令，使用 JSON 結構定義檔案建立資料表。這個指令會在 `myotherproject` 的 `mydataset` 中建立名為 `mytable` 的資料表。資料表的到期時間設為 3600 秒 (一小時)、說明設為 `This is my table`，標籤則設為 `organization:development`。結構定義檔的路徑為 `/tmp/myschema.json`。

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

使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 Cloud Resource Manager API。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

**建立資料表**

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

下列範例會建立名為 `mytable` 的資料表，然後使用 [`google_bigquery_table_iam_policy`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table_iam#google_bigquery_table_iam_policy) 資源授予存取權。只有在您想將資料表的存取權授予無權存取資料表所在資料集的主體時，才需要執行這個步驟。

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

**使用客戶自行管理的加密金鑰建立資料表**

下列範例會建立名為 `mytable` 的資料表，並使用 [`google_kms_crypto_key`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/kms_crypto_key) 和 [`google_kms_key_ring`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/kms_key_ring) 資源，為資料表指定 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。您必須先[啟用 Cloud Key Management Service API](https://console.cloud.google.com/apis/enableflow?apiid=cloudkms.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com%2F&hl=zh-tw)，才能執行這個範例。

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

### API

使用已定義的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定操作說明進行操作。詳情請參閱 [BigQuery C# API 參考文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定操作說明進行操作。詳情請參閱 [BigQuery PHP API 參考文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定操作說明進行操作。詳情請參閱 [BigQuery Ruby API 參考文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

### 建立沒有結構定義的空白資料表

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

### 根據查詢結果建立資料表

如要從查詢結果建立資料表，請將結果寫入目標資料表。

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，點選「Datasets」(資料集)，然後選取資料集。
4. 在查詢編輯器中，輸入有效的 SQL 查詢。
5. 依序點選「編輯」>「查詢設定」。
6. 選取「為查詢結果設定目的地資料表」選項。
7. 在「Destination」(目的地) 部分，選取要建立資料表的**資料集**，然後選擇**資料表 ID**。
8. 在「Destination table write preference」(目標資料表寫入偏好設定) 區段，選擇下列其中一項：

   * [Write if empty] (空白時寫入)：僅在資料表空白時將查詢結果寫入資料表。
   * [Append to table] (附加到資料表中)：將查詢結果附加到現有的資料表。
   * [Overwrite table] (覆寫資料表)：使用查詢結果覆寫名稱相同的現有資料表。
9. 選用：在「Data location」(資料位置) 部分，選擇[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
10. 如要更新查詢設定，請按一下「儲存」。
11. 按一下「執行」。這會建立查詢工作，將查詢結果寫入指定的資料表。

或者，如果您在執行查詢前忘記指定目的地資料表，可以按一下編輯器上方的「[**Save Results**](#save-query-results)」(儲存結果) 按鈕，將快取結果資料表複製到永久資料表。

### SQL

以下範例使用 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，根據公開 `bikeshare_trips` 資料表中的資料建立 `trips` 資料表：

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
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

詳情請參閱「[從現有資料表建立新資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_new_table_from_an_existing_table)」。

### bq

1. 在 Google Cloud 控制台啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 控制台底部會開啟 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已設定適用於您目前專案的值。工作階段可能要幾秒鐘的時間才能初始化。
2. 輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並指定 `--destination_table` 旗標，根據查詢結果建立永久資料表。指定 `use_legacy_sql=false` 旗標，即可使用 GoogleSQL 語法。如要將查詢結果寫入非預設專案中的資料表，請按照下列格式，將專案 ID 新增至資料集名稱：`project_id:dataset`。

   選用：提供 `--location` 旗標，並將值設為[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

   如要控管現有目的地資料表的寫入配置，請指定下列其中一個選用旗標：

   * `--append_table`：如果目的地資料表存在，查詢結果會附加至該資料表。
   * `--replace`：如果目的地資料表已存在，系統會以查詢結果覆寫該資料表。

     ```
     bq --location=location query \
     --destination_table project_id:dataset.table \
     --use_legacy_sql=false 'query'
     ```

     更改下列內容：
   * `location` 是用於處理查詢的位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京區域使用 BigQuery，可以將旗標值設為 `asia-northeast1`。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
   * `project_id` 是您的專案 ID。
   * `dataset` 是資料集的名稱，其中包含您要寫入查詢結果的資料表。
   * `table` 是要寫入查詢結果的資料表名稱。
   * `query` 是 GoogleSQL 語法的查詢。

     如未指定寫入處置旗標，預設行為是僅在資料表空白時，才將結果寫入資料表。如果資料表存在且並非空白，系統會傳回下列錯誤：`BigQuery error in query operation: Error processing job
     project_id:bqjob_123abc456789_00000e1234f_1: Already
     Exists: Table project_id:dataset.table`。

     範例：

     **注意：**這些範例會查詢位於美國的公開資料集。由於該公開資料集儲存在美國的多地區位置，因此您目的地資料表所屬的資料集也必須位於美國。您無法查詢位於某個位置的資料集，然後將結果寫入位於另一個位置的目的地資料表。 

     輸入下列指令，將查詢結果寫入 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於預設專案中。由於您未在指令中指定任何寫入配置旗標，因此資料表必須為新資料表或空白資料表。否則，系統會傳回 `Already exists` 錯誤。查詢會從[美國姓名資料公開資料集](https://console.cloud.google.com/marketplace/product/social-security-administration/us-names?hl=zh-tw)擷取資料。

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

     輸入下列指令，將查詢結果附加至 `mydataset` 中名為 `mytable` 的目標資料表。該資料集位於 `my-other-project`，而非預設專案。這項指令會使用 `--append_table` 旗標，將查詢結果附加至目的地資料表。

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

如要將查詢結果儲存至永久資料表，請呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法、設定 `query` 工作，並加入 `destinationTable` 屬性的值。如要控管現有目標資料表的寫入配置，請設定 `writeDisposition` 屬性。

如要控管查詢工作的處理位置，請在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中指定 `location` 屬性。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要將查詢結果儲存至永久資料表，請在 [QueryJobConfiguration](https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration?hl=zh-tw) 中，將[目的地資料表](https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.QueryJobConfiguration.Builder?hl=zh-tw#com_google_cloud_bigquery_QueryJobConfiguration_Builder_setDestinationTable_com_google_cloud_bigquery_TableId_)設為所需的 [TableId](https://cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.TableId?hl=zh-tw)。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

如要將查詢結果儲存至永久資料表，請建立 [QueryJobConfig](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob)，並將 [destination](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob_destination) 設為所需的 [TableReference](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.TableReference?hl=zh-tw)。
將工作設定傳遞至 [query 方法](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_query)。

```
from google.cloud
```