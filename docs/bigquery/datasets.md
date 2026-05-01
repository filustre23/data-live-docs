* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立資料集

本文說明如何在 BigQuery 中建立資料集來儲存資料。資料集是頂層容器，可用於整理及控管資料表和檢視表的存取權。

如要瞭解如何處理其他資料集類型，請參閱下列資源：

* 如要瞭解 Spanner 外部資料集，請參閱「[建立 Spanner 外部資料集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)」。
* 如要瞭解 AWS Glue 聯合資料集，請參閱「[建立 AWS Glue 聯合資料集](https://docs.cloud.google.com/bigquery/docs/glue-federated-datasets?hl=zh-tw)」。

如要瞭解如何查詢公開資料集中的資料表，請參閱「[透過控制台查詢公開資料集 Google Cloud](https://docs.cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console?hl=zh-tw) 」。

## 資料集的限制

BigQuery 資料集有下列限制：

* [資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)只能在建立時設定。資料集建立後，就無法變更位置。
* 查詢中參考的所有資料表，都必須儲存在同一個位置的資料集中。
* 外部資料集不支援資料表到期時間、副本、時空旅行、預設定序、預設捨入模式，也不支援啟用或停用不區分大小寫的資料表名稱。
* [複製資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)時，包含來源資料表和目的地資料表的資料集必須位於相同位置。
* 每個專案的資料集名稱皆不得重複。
* 變更資料集的[儲存空間計費模式](#dataset_storage_billing_models)後，必須等待 14 天才能再次變更。
* 如果現有[固定費率的舊版運算單元承諾使用](https://docs.cloud.google.com/bigquery/docs/reservations-commitments-legacy?hl=zh-tw)與資料集位於相同區域，您就無法為資料集啟用實體儲存空間帳單。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。

### 所需權限

如要建立資料集，您需要 `bigquery.datasets.create` 身分與存取權管理 (IAM) 權限。

下列每個預先定義的 IAM 角色都包含建立資料集所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.user`
* `roles/bigquery.admin`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

**注意：** 系統會自動為資料集建立者指派該資料集的 [BigQuery 資料擁有者 (`roles/bigquery.dataOwner`) 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner)。因此，即使未明確授予權限，使用者或服務帳戶只要有權建立資料集，也能刪除資料集。

## 建立資料集

建立資料集時，您通常會指定資料的儲存位置。如未指定位置，系統會使用[預設位置](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#global-settings)。詳情請參閱「[指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)」。

**注意：** 如果您將資料集的位置選擇為 `EU`，或是歐盟中的某個區域，您的核心 BigQuery 客戶資料就會存放在歐盟。如需核心 BigQuery 客戶資料的定義，請參閱[服務專屬條款](https://console.cloud.google.com/terms/service-terms?hl=zh-tw#13-google-bigquery-service)。

如何建立資料集：

### 控制台

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。
[前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)2. 點選左側窗格中的 explore「Explorer」。
3. 選取要建立資料集的專案。
4. 依序點選 more\_vert「View actions」(查看動作) 和「Create dataset」(建立資料集)。

### SQL

使用 [`CREATE SCHEMA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_schema_statement)。

如要在非預設專案中建立資料集，請採用下列格式將專案 ID 新增至資料集 ID：`PROJECT_ID.DATASET_ID`。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE SCHEMA PROJECT_ID.DATASET_ID
     OPTIONS (
       default_kms_key_name = 'KMS_KEY_NAME',
       default_partition_expiration_days = PARTITION_EXPIRATION,
       default_table_expiration_days = TABLE_EXPIRATION,
       description = 'DESCRIPTION',
       labels = [('KEY_1','VALUE_1'),('KEY_2','VALUE_2')],
       location = 'LOCATION',
       max_time_travel_hours = HOURS,
       storage_billing_model = BILLING_MODEL);
   ```

   請替換下列項目：

   * `PROJECT_ID`：專案 ID
   * `DATASET_ID`：您要建立的資料集 ID
   * `KMS_KEY_NAME`：預設 Cloud Key Management Service 金鑰的名稱，用於保護這個資料集中新建立的資料表，除非在建立時提供其他金鑰。您無法在具有這組參數的資料集中，建立 Google 加密資料表。
   * `PARTITION_EXPIRATION`：新建立的分區資料表中分區的預設生命週期 (以天為單位)。預設的分區到期時間沒有最小值。到期時間為分區日期加上整數值。在資料集的分區資料表中建立的任何分區，都會在分區日期後 `PARTITION_EXPIRATION` 天刪除。如果您在建立或更新分區資料表時使用 `time_partitioning_expiration` 選項，系統會優先採用資料表層級的分區到期時間，而不是資料集層級的預設分區到期時間。
   * `TABLE_EXPIRATION`：新建立資料表的預設生命週期 (以天為單位)。最小值為 0.042 天 (1 小時)。到期時間為目前時間加整數值。在資料集中建立的任何資料表，都會在建立時間後 `TABLE_EXPIRATION` 天刪除。如果您在[建立資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create-table)時未設定資料表到期時間，系統就會套用這個值。
   * `DESCRIPTION`：資料集說明
   * `KEY_1:VALUE_1`：要設為這個資料集第一個標籤的鍵/值組合
   * `KEY_2:VALUE_2`：要設為第二個標籤的鍵/值組合
   * `LOCATION`：資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。資料集建立後即無法變更位置。
   * `HOURS`：新資料集的時間回溯期 (以小時為單位)。`HOURS` 值必須是 24 的倍數 (48、72、96、120、144、168)，且介於 48 (2 天) 和 168 (7 天) 之間的整數。如果未指定這個選項，預設值為 168 小時。
   * `BILLING_MODEL`：設定資料集的[儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)。將 `BILLING_MODEL` 值設為 `PHYSICAL`，即可在計算儲存空間費用時使用實際位元組，設為 `LOGICAL` 則可使用邏輯位元組。預設值為 `LOGICAL`。

     變更資料集的計費模式後，最久需要 24 小時才會生效。

     變更資料集的儲存空間計費模式後，必須等待 14 天，才能再次變更儲存空間計費模式。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要建立新的資料集，請使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset) 指令，並加上 `--location` 旗標。如需可能的完整參數清單，請參閱 [`bq mk --dataset` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)參考資料。

如要在非預設專案中建立資料集，請採用下列格式將專案 ID 新增至資料集：`PROJECT_ID:DATASET_ID`。

```
bq --location=LOCATION mk \
    --dataset \
    --default_kms_key=KMS_KEY_NAME \
    --default_partition_expiration=PARTITION_EXPIRATION \
    --default_table_expiration=TABLE_EXPIRATION \
    --description="DESCRIPTION" \
    --label=KEY_1:VALUE_1 \
    --label=KEY_2:VALUE_2 \
    --add_tags=KEY_3:VALUE_3[,...] \
    --max_time_travel_hours=HOURS \
    --storage_billing_model=BILLING_MODEL \
    PROJECT_ID:DATASET_ID
```

更改下列內容：

* `LOCATION`：資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。資料集在建立之後，該位置就無法改變。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)，設定該位置的預設值。
* `KMS_KEY_NAME`：預設 Cloud Key Management Service 金鑰的名稱，用於保護這個資料集中新建立的資料表，除非在建立時提供其他金鑰。您無法使用這組參數在資料集中建立 Google 加密資料表。
* `PARTITION_EXPIRATION`：新建分區資料表中分區的預設生命週期 (以秒為單位)。預設的分區到期時間沒有最小值。到期時間為分區日期加上整數值。在資料集的分區資料表中所建立的任何分區，都會以分區建立日期為起始點，在 `PARTITION_EXPIRATION` 秒後刪除。如果您在建立或更新分區資料表時使用 `--time_partitioning_expiration` 旗標，系統會優先採用資料表層級的分區到期時間，而不是資料集層級的預設分區到期時間。
* `TABLE_EXPIRATION`：新建立資料表的預設生命週期 (以秒為單位)。最小值是 3600 秒 (1 小時)。到期時間為目前時間加整數值。在資料集中建立的任何資料表都會在建立時間後 `TABLE_EXPIRATION` 秒刪除。如果您在[建立資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create-table)時未設定資料表到期時間，系統就會套用這個值。
* `DESCRIPTION`：資料集說明
* `KEY_1:VALUE_1`：要設為這個資料集第一個標籤的鍵值組，而 `KEY_2:VALUE_2` 則是要設為第二個標籤的鍵值組。
* `KEY_3:VALUE_3`：您要在資料集上設定為標記的鍵值組。在相同標記下新增多個標記，並在鍵/值組合之間加上半形逗號。
* `HOURS`：新資料集的時間回溯視窗時長 (以小時為單位)。`HOURS` 值必須是 24 的倍數 (48、72、96、120、144、168)，且介於 48 (2 天) 和 168 (7 天) 之間。如果未指定這個選項，預設值為 168 小時。
* `BILLING_MODEL`：設定資料集的[儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)。將 `BILLING_MODEL` 值設為 `PHYSICAL`，即可在計算儲存空間費用時使用實體位元組；設為 `LOGICAL` 則可使用邏輯位元組。預設為 `LOGICAL`。

  變更資料集的計費模式後，最久需要 24 小時才會生效。

  變更資料集的儲存空間計費模式後，必須等待 14 天，才能再次變更儲存空間計費模式。
* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID` 是您要建立的資料集 ID。

舉例來說，下列指令會建立名為 `mydataset` 的資料集，並將資料位置設定為 `US`，而預設的資料表到期時間為 3,600 秒 (1 小時)，說明則為 `This is my dataset`。這個指令採用 `-d` 捷徑，而不是使用 `--dataset` 旗標。如果您省略 `-d` 和 `--dataset`，該指令預設會建立資料集。

```
bq --location=US mk -d \
    --default_table_expiration 3600 \
    --description "This is my dataset." \
    mydataset
```

如要確認資料集是否已建立，請輸入 `bq ls` 指令。此外，您可以在建立新的資料集時，採用下列格式來建立資料表：`bq mk -t dataset.table`。如要進一步瞭解如何建立資料表，請參閱「[建立資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create-table)」。

### Terraform

請使用 [`google_bigquery_dataset`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset) 資源。

**注意：** 您必須啟用 Cloud Resource Manager API，才能使用 Terraform 建立 BigQuery 物件。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

**建立資料集**

下列範例會建立名為 `mydataset` 的資料集：

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
```

使用 `google_bigquery_dataset` 資源建立資料集時，系統會自動將資料集存取權授予專案層級[基本角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#basic)的所有帳戶。如果您在建立資料集後執行 [`terraform show` 指令](https://developer.hashicorp.com/terraform/cli/commands/show)，資料集的 [`access` 區塊](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset#nested_access)會類似下列內容：

如要授予資料集存取權，建議您使用其中一個 [`google_bigquery_iam` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_iam)，如下例所示，除非您打算在資料集中建立授權物件，例如[授權 view](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。在這種情況下，請使用 [`google_bigquery_dataset_access` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_access)。如需範例，請參閱該說明文件。

**建立資料集並授予存取權**

以下範例會建立名為 `mydataset` 的資料集，然後使用 [`google_bigquery_dataset_iam_policy`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_iam#google_bigquery_dataset_iam_policy) 資源授予存取權。

**注意：** 如要搭配這個資料集使用授權物件 (例如[授權檢視區塊](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw))，請勿採用這種做法。在這種情況下，請使用 `google_bigquery_dataset_access` 資源。如需範例，請參閱 [`google_bigquery_dataset_access`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset_access)。

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

# Update the user, group, or service account
# provided by the members argument with the
# appropriate principals for your organization.
data "google_iam_policy" "default" {
  binding {
    role = "roles/bigquery.dataOwner"
    members = [
      "user:raha@altostrat.com",
    ]
  }
  binding {
    role = "roles/bigquery.admin"
    members = [
      "user:raha@altostrat.com",
    ]
  }
  binding {
    role = "roles/bigquery.user"
    members = [
      "group:analysts@altostrat.com",
    ]
  }
  binding {
    role = "roles/bigquery.dataViewer"
    members = [
      "serviceAccount:bqcx-1234567891011-abcd@gcp-sa-bigquery-condel.iam.gserviceaccount.com",
    ]
  }
}

resource "google_bigquery_dataset_iam_policy" "default" {
  dataset_id  = google_bigquery_dataset.default.dataset_id
  policy_data = data.google_iam_policy.default.policy_data
}
```

**使用客戶自行管理的加密金鑰建立資料集**

下列範例會建立名為 `mydataset` 的資料集，並使用 [`google_kms_crypto_key`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/kms_crypto_key) 和 [`google_kms_key_ring`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/kms_key_ring) 資源，為資料集指定 Cloud Key Management Service 金鑰。您必須先[啟用 Cloud Key Management Service API](https://console.cloud.google.com/flows/enableapi?apiid=cloudkms.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com&hl=zh-tw)，才能執行這個範例。

```
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "mydataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

  default_encryption_configuration {
    kms_key_name = google_kms_crypto_key.crypto_key.id
  }

  labels = {
    billing_group = "accounting",
    pii           = "sensitive"
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

   視需要從 GitHub 複製程式碼。如果 Terraform 程式碼片段是端對端解決方案的一部分，建議您使用這個方法。
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

### API

請呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法，搭配已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Apis.Bigquery.v2.Data;
using Google.Cloud.BigQuery.V2;

public class BigQueryCreateDataset
{
    public BigQueryDataset CreateDataset(
        string projectId = "your-project-id",
        string location = "US"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        var dataset = new Dataset
        {
            // Specify the geographic location where the dataset should reside.
            Location = location
        };
        // Create the dataset
        return client.CreateDataset(
            datasetId: "your_new_dataset_id", dataset);
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

	"cloud.google.com/go/bigquery"
)

// createDataset demonstrates creation of a new dataset using an explicit destination location.
func createDataset(projectID, datasetID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	meta := &bigquery.DatasetMetadata{
		Location: "US", // See https://cloud.google.com/bigquery/docs/locations
	}
	if err := client.Dataset(datasetID).Create(ctx, meta); err != nil {
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
import com.google.cloud.bigquery.Dataset;
import com.google.cloud.bigquery.DatasetInfo;

public class CreateDataset {

  public static void runCreateDataset() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    createDataset(datasetName);
  }

  public static void createDataset(String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      DatasetInfo datasetInfo = DatasetInfo.newBuilder(datasetName).build();

      Dataset newDataset = bigquery.create(datasetInfo);
      String newDatasetName = newDataset.getDatasetId().getDataset();
      System.out.println(newDatasetName + " created successfully");
    } catch (BigQueryException e) {
      System.out.println("Dataset was not created. \n" + e.toString());
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

async function createDataset() {
  // Creates a new dataset named "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_new_dataset";

  // Specify the geographic location where the dataset should reside
  const options = {
    location: 'US',
  };

  // Create a new dataset
  const [dataset] = await bigquery.createDataset(datasetId, options);
  console.log(`Dataset ${dataset.id} created.`);
}
createDataset();
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/** Uncomment and populate these variables in your code */
// $projectId = 'The Google project ID';
// $datasetId = 'The BigQuery dataset ID';

$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$dataset = $bigQuery->createDataset($datasetId);
printf('Created dataset %s' . PHP_EOL, $datasetId);
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset to create.
# dataset_id = "{}.your_dataset".format(client.project)

# Construct a full Dataset object to send to the API.
dataset = bigquery.Dataset(dataset_id)

# TODO(developer): Specify the geographic location where the dataset should reside.
dataset.location = "US"

# Send the dataset to the API for creation, with an explicit timeout.
# Raises google.api_core.exceptions.Conflict if the Dataset already
# exists within the project.
dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def create_dataset dataset_id = "my_dataset", location = "US"
  bigquery = Google::Cloud::Bigquery.new

  # Create the dataset in a specified geographic location
  bigquery.create_dataset dataset_id, location: location

  puts "Created dataset: #{dataset_id}"
end
```

## 為資料集命名

在 BigQuery 中建立資料集時，每個專案的資料集名稱不得重複。資料集名稱可包含下列項目：

* 最多 1,024 個字元。
* 字母 (大寫或小寫)、數字和底線。

資料集名稱預設會區分大小寫。`mydataset` 和 `MyDataset` 可在同一專案中並存，除非其中一個已關閉大小寫區分功能。如需範例，請參閱「[建立不區分大小寫的資料集](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_case-insensitive_dataset)」和「[資源：資料集](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw#resource:-dataset)」。

資料集名稱不得包含空格或特殊字元，例如 `-`、`&`、`@` 或 `%`。

### 隱藏的資料集

隱藏資料集是指名稱以底線開頭的資料集。您可以查詢隱藏資料集中的資料表和檢視表，方式與查詢其他資料集相同。隱藏資料集有下列限制：

* 這些檔案會隱藏在 Google Cloud 控制台的「Explorer」面板中。
* 不會顯示在任何 `INFORMATION_SCHEMA` 檢視畫面中。
* 無法與[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)搭配使用。
* 這些資料集無法做為下列授權資源的來源資料集：
  + [已授權的資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)
  + [獲得授權的處理常式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)
  + [授權 view](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)
* 不會顯示在 Data Catalog (已淘汰) 或 Knowledge Catalog 中。
* 無法做為建立[資料集副本](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#dataset_replication)的來源資料集

## 資料集安全性

如要在 BigQuery 中控管資料集存取權，請參閱「[控管資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。如要瞭解資料加密，請參閱「[靜態資料加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)」。

## 後續步驟

* 如要進一步瞭解如何列出專案中的資料集，請參閱[列出資料集](https://docs.cloud.google.com/bigquery/docs/listing-datasets?hl=zh-tw)一文。
* 如要進一步瞭解資料集中繼資料，請參閱[取得資料集相關資訊](https://docs.cloud.google.com/bigquery/docs/dataset-metadata?hl=zh-tw)一文。
* 如要進一步瞭解如何變更資料集屬性，請參閱[更新資料集](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw)。
* 如要進一步瞭解如何建立及管理標籤，請參閱[建立及管理標籤](https://docs.cloud.google.com/bigquery/docs/labels?hl=zh-tw)。

## 歡迎試用

如果您未曾使用過 Google Cloud，歡迎建立帳戶，親自體驗實際使用 BigQuery 的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。

[免費試用 BigQuery](https://console.cloud.google.com/freetrial?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]