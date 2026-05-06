Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 客戶自行管理的 Cloud KMS 金鑰

**注意：** 使用以特定 BigQuery 版本建立的預留項目時，這項功能可能無法使用。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

根據預設，BigQuery 會[加密靜態儲存的內容](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。BigQuery 會為您處理並管理這個預設加密作業，您不必採取任何其他動作。首先，系統會使用「資料加密金鑰」對 BigQuery 資料表中的資料進行加密，然後使用「金鑰加密金鑰」為資料加密金鑰進行加密，這個方法稱為[信封式加密](https://docs.cloud.google.com/kms/docs/envelope-encryption?hl=zh-tw)。
金鑰加密金鑰不會直接加密您的資料，其用途是對 Google 用來加密您資料的資料加密金鑰進行加密。

如果您想自行控管加密作業，可以針對 BigQuery 使用客戶代管的加密金鑰 (CMEK)。您可以在 [Cloud KMS](https://docs.cloud.google.com/kms/docs?hl=zh-tw) 中控制及管理用來保護您資料的金鑰加密金鑰，而不是由 Google 擁有及管理。本文詳細說明如何手動建立 BigQuery 適用的 Cloud KMS 金鑰。

進一步瞭解  [Google Cloud](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw) 的加密選項。如要瞭解 CMEK 的具體資訊，包括優點和限制，請參閱[客戶代管加密金鑰](https://docs.cloud.google.com/kms/docs/cmek?hl=zh-tw)。

## 事前準備

* BigQuery 代管儲存空間中的所有資料資產都支援 CMEK。不過，如果您也查詢儲存在[外部資料來源](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw) (例如 Cloud Storage) 的資料，且這些資料已透過 CMEK 加密，則資料加密作業會由 [Cloud Storage](https://docs.cloud.google.com/storage/docs/encryption/customer-managed-keys?hl=zh-tw) 管理。舉例來說，BigLake 資料表支援 Cloud Storage 中以 CMEK 加密的資料。

  BigQuery 和 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)不支援客戶提供的加密金鑰 (CSEK)。
* 決定您要在同一個 Google Cloud 專案或不同的專案中執行 BigQuery 和 Cloud KMS。為了方便說明，本文的範例將採用下列慣例：

  + `PROJECT_ID`：執行 BigQuery 專案的專案 ID
  + `PROJECT_NUMBER`：執行 BigQuery 的專案專案編號
  + `KMS_PROJECT_ID`：執行 Cloud KMS 的專案 ID (即使這個專案就是執行 BigQuery 的專案)如要瞭解 Google Cloud 專案 ID 和專案編號，請參閱「[找出專案名稱、編號和 ID](https://docs.cloud.google.com/resource-manager/docs/view-update-projects?hl=zh-tw#identifying_projects)」。
* 新專案會自動啟用 BigQuery。如果您是使用現有專案來執行 BigQuery，請[啟用 BigQuery API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery&hl=zh-tw)。
* 針對執行 Cloud KMS 的 Google Cloud 專案，[啟用 Cloud Key Management Service API](https://console.cloud.google.com/flows/enableapi?apiid=cloudkms.googleapis.com&hl=zh-tw)。

每次查詢 CMEK 加密資料表時，系統都會使用 Cloud KMS 執行一次解密呼叫。詳情請參閱 [Cloud KMS 定價](https://cloud.google.com/kms/pricing?hl=zh-tw)。

## 加密規格

BigQuery 中用來保護您資料的 Cloud KMS 金鑰是 AES-256 金鑰。這類金鑰的用途是對加密您資料的資料加密金鑰進行加密，因此才會在 BigQuery 中當做金鑰加密金鑰使用。

## 手動或自動建立金鑰

您可以手動建立 CMEK 金鑰，也可以使用 Cloud KMS Autokey。
Autokey 會自動佈建及指派 CMEK 金鑰，簡化建立及管理金鑰的程序。使用 Autokey 時，您不需要事先佈建金鑰環、金鑰和服務帳戶。而是會在建立 BigQuery 資源時，視需要產生。詳情請參閱「[Autokey 總覽](https://docs.cloud.google.com/kms/docs/autokey-overview?hl=zh-tw)」。

### 手動建立金鑰環和金鑰

針對執行 Cloud KMS 的 Google Cloud 專案，按照[建立金鑰環和金鑰](https://docs.cloud.google.com/kms/docs/creating-keys?hl=zh-tw)一文的指示建立金鑰環和金鑰。請在與您 BigQuery 資料集位置相符的位置建立金鑰環：

* 所有多地區資料集都應使用相符位置的多地區金鑰環。舉例來說，`US` 地區中的資料集應使用來自 `us` 地區的金鑰環加以保護，`EU` 地區中的資料集則應使用 `europe` 區域中的金鑰環加以保護。
* 地區資料集應使用相符地區金鑰。舉例來說，`asia-northeast1` 地區中的資料集應使用來自 `asia-northeast1` 地區的金鑰環加以保護。
* 在 Google Cloud 控制台中為 BigQuery 設定 CMEK 時，無法使用 `global` 區域。不過，使用 bq 指令列工具或 GoogleSQL 為 BigQuery 設定 CMEK 時，可以指定 `global` 地區。

如要進一步瞭解支援 BigQuery 和 Cloud KMS 的地區，請參閱 [Cloud 據點](https://cloud.google.com/about/locations/?hl=zh-tw)。

## 授予加密和解密權限

如要使用 CMEK 金鑰保護 BigQuery 資料，請授予 BigQuery 服務帳戶使用該金鑰加密及解密的權限。[Cloud KMS CryptoKey Encrypter/Decrypter](https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles?hl=zh-tw#predefined_roles) 角色會授予這項權限。

請確認您已建立服務帳戶，然後使用Google Cloud 控制台取得 BigQuery 服務帳戶 ID。接著，請提供適當的角色給該服務帳戶，從而使用 Cloud KMS 進行加密和解密。

### 觸發服務帳戶建立作業

建立專案時，系統不會一併建立 BigQuery 服務帳戶。如要觸發服務帳戶的建立作業，請輸入使用該帳戶的指令 (例如 [`bq show --encryption_service_account`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#encryption_service_account_flag) 指令)，或呼叫 [projects.getServiceAccount](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/projects/getServiceAccount?hl=zh-tw) API 方法。例如：

```
bq show --encryption_service_account --project_id=PROJECT_ID
```

### 取得服務帳戶 ID

BigQuery 服務帳戶 ID 的格式如下：

```
bq-PROJECT_NUMBER@bigquery-encryption.iam.gserviceaccount.com
```

以下技巧說明如何判斷專案的 BigQuery 服務帳戶 ID。

### 控制台

1. 前往 Google Cloud 控制台的「資訊主頁」[頁面](https://console.cloud.google.com/home?hl=zh-tw)。

   [前往「資訊主頁」頁面](https://console.cloud.google.com/首頁?hl=zh-tw)
2. 按一下頁面頂端的 [Select from] (可用的選項) 下拉式清單。在顯示的「Select from」(可用的選項) 視窗中，選取您的專案。
3. 專案資訊主頁的「Project info」(專案資訊) 卡片會顯示專案 ID 和專案編號。
4. 在下列字串中，將 PROJECT\_NUMBER 替換為您的專案編號。這個新字串會識別您的 BigQuery 服務帳戶 ID。

   ```
   bq-PROJECT_NUMBER@bigquery-encryption.iam.gserviceaccount.com
   ```

### bq

使用 `bq show` 指令並加上 `--encryption_service_account` 標記，即可取得服務帳戶 ID：

```
bq show --encryption_service_account
```

該指令會顯示服務帳戶 ID：

```
                  ServiceAccountID
-------------------------------------------------------------
bq-PROJECT_NUMBER@bigquery-encryption.iam.gserviceaccount.com
```

### 指派加密者/解密者角色

將 Cloud KMS CryptoKey Encrypter/Decrypter [角色](https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles?hl=zh-tw#predefined_roles)指派給您複製到剪貼簿的 BigQuery 系統服務帳戶。這個帳戶的格式如下：

```
bq-PROJECT_NUMBER@bigquery-encryption.iam.gserviceaccount.com
```

### 控制台

1. 在 Google Cloud 控制台中開啟「Cryptographic Keys」(加密編譯金鑰) 頁面。

   [開啟「Cryptographic Keys」(加密編譯金鑰) 頁面](https://console.cloud.google.com/security/kms?hl=zh-tw)
2. 按一下包含金鑰的金鑰環名稱。
3. 按一下要新增角色的加密金鑰核取方塊。系統會開啟「權限」分頁。
4. 按一下「新增成員」。
5. 輸入服務帳戶的電子郵件地址：`bq-PROJECT_NUMBER@bigquery-encryption.iam.gserviceaccount.com`。

   * 如果服務帳戶已在成員清單中，表示已獲指派角色。請按一下 `bq-PROJECT_NUMBER@bigquery-encryption.iam.gserviceaccount.com` 服務帳戶目前的角色下拉式清單。
6. 依序按一下「選取角色」下拉式清單 >「Cloud KMS」>「Cloud KMS 加密編譯金鑰加密者/解密者」角色。
7. 按一下「儲存」，將角色套用至 `bq-PROJECT_NUMBER@bigquery-encryption.iam.gserviceaccount.com` 服務帳戶。

### gcloud

您可以使用 Google Cloud CLI 指派角色：

```
gcloud kms keys add-iam-policy-binding \
--project=KMS_PROJECT_ID \
--member serviceAccount:bq-PROJECT_NUMBER@bigquery-encryption.iam.gserviceaccount.com \
--role roles/cloudkms.cryptoKeyEncrypterDecrypter \
--location=KMS_KEY_LOCATION \
--keyring=KMS_KEY_RING \
KMS_KEY
```

更改下列內容：

* `KMS_PROJECT_ID`：執行 Cloud KMS 的 Google Cloud專案 ID
* `PROJECT_NUMBER`：執行 BigQuery 的 Google Cloud 專案編號 (而非專案 ID)
* `KMS_KEY_LOCATION`：Cloud KMS 金鑰的位置名稱
* `KMS_KEY_RING`：Cloud KMS 金鑰的金鑰環名稱
* `KMS_KEY`：Cloud KMS 金鑰的名稱

## 金鑰資源 ID

使用 CMEK 時需要 Cloud KMS 金鑰的資源 ID，如範例所示。這個鍵會區分大小寫，且採用下列格式：

```
projects/KMS_PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY
```

**注意：** 您無法指定包含 `/cryptoKeyVersions/` 權杖的金鑰資源 ID。BigQuery 一律會使用標示為 `primary` 的金鑰版本，在建立資料表時保護資料表。

### 擷取金鑰資源 ID

1. 在 Google Cloud 控制台中開啟「Cryptographic Keys」(加密編譯金鑰) 頁面。

   [開啟「Cryptographic Keys」(加密編譯金鑰) 頁面](https://console.cloud.google.com/security/kms?hl=zh-tw)
2. 按一下包含金鑰的金鑰環名稱。
3. 找到您要擷取資源 ID 的金鑰環，按一下「更多」圖示 *more\_vert*。
4. 按一下「複製資源名稱」。金鑰的資源 ID 會複製到剪貼簿。資源 ID 也稱為資源名稱。

## 建立受 Cloud KMS 保護的資料表

如何建立受 Cloud KMS 保護的資料表：

### 控制台

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下資料集。資料集會在分頁中開啟。
4. 在詳細資料窗格中，按一下 add\_box「建立資料表」。
5. 在「Create table」(建立資料表) 頁面中填寫[建立包含結構定義的空白資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create_an_empty_table_with_a_schema_definition)的必要資訊。請先設定加密類型，並完成指定要與資料表搭配使用的 Cloud KMS 金鑰，接著才按一下「建立資料表」：

   1. 點選「進階選項」。
   2. 按一下「客戶管理的金鑰」。
   3. 選取金鑰。如果清單中未顯示你要使用的金鑰，請輸入金鑰的[資源 ID](#key_resource_id)。
6. 點選「建立資料表」。

### SQL

使用 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，並加上 `kms_key_name` 選項：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE DATASET_ID.TABLE_ID (
     name STRING, value INT64
   ) OPTIONS (
       kms_key_name
         = 'projects/KMS_PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY');
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

您可以使用 bq 指令列工具搭配 `--destination_kms_key` 旗標來建立資料表。`--destination_kms_key` 旗標會指定要與資料表搭配使用的金鑰[資源 ID](#key_resource_id)。

如何建立包含結構定義的空白資料表：

```
bq mk --schema name:string,value:integer -t \
--destination_kms_key projects/KMS_PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY \
DATASET_ID.TABLE_ID
```

如何從查詢建立資料表：

```
bq query --destination_table=DATASET_ID.TABLE_ID \
--destination_kms_key projects/KMS_PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY \
"SELECT name,count FROM DATASET_ID.TABLE_ID WHERE gender = 'M' ORDER BY count DESC LIMIT 6"
```

如要進一步瞭解 bq 指令列工具，請參閱[使用 bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)。

### Terraform

請使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會建立名為 `mytable` 的資料表，並使用 [`google_kms_crypto_key`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/kms_crypto_key) 和 [`google_kms_key_ring`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/kms_key_ring) 資源，為資料表指定 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。

如要執行這個範例，您必須啟用 [Cloud Resource Manager API](https://console.cloud.google.com/flows/enableapi?apiid=cloudresourcemanager.googleapis.com&hl=zh-tw) 和 [Cloud Key Management Service API](https://console.cloud.google.com/flows/enableapi?apiid=cloudkms.googleapis.com&hl=zh-tw)。

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

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// createTableWithCMEK demonstrates creating a table protected with a customer managed encryption key.
func createTableWithCMEK(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydatasetid"
	// tableID := "mytableid"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	tableRef := client.Dataset(datasetID).Table(tableID)
	meta := &bigquery.TableMetadata{
		EncryptionConfig: &bigquery.EncryptionConfig{
			// TODO: Replace this key with a key you have created in Cloud KMS.
			KMSKeyName: "projects/cloud-samples-tests/locations/us/keyRings/test/cryptoKeys/test",
		},
	}
	if err := tableRef.Create(ctx, meta); err != nil {
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
import com.google.cloud.bigquery.EncryptionConfiguration;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.StandardTableDefinition;
import com.google.cloud.bigquery.TableDefinition;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;

// Sample to create a cmek table
public class CreateTableCMEK {

  public static void runCreateTableCMEK() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String kmsKeyName = "MY_KEY_NAME";
    Schema schema =
        Schema.of(
            Field.of("stringField", StandardSQLTypeName.STRING),
            Field.of("booleanField", StandardSQLTypeName.BOOL));
    // i.e. projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{cryptoKey}
    EncryptionConfiguration encryption =
        EncryptionConfiguration.newBuilder().setKmsKeyName(kmsKeyName).build();
    createTableCMEK(datasetName, tableName, schema, encryption);
  }

  public static void createTableCMEK(
      String datasetName, String tableName, Schema schema, EncryptionConfiguration configuration) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      TableDefinition tableDefinition = StandardTableDefinition.of(schema);
      TableInfo tableInfo =
          TableInfo.newBuilder(tableId, tableDefinition)
              .setEncryptionConfiguration(configuration)
              .build();

      bigquery.create(tableInfo);
      System.out.println("Table cmek created successfully");
    } catch (BigQueryException e) {
      System.out.println("Table cmek was not created. \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

建立資料表前，請先將 [Table.encryption\_configuration](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.Table?hl=zh-tw#google_cloud_bigquery_table_Table_encryption_configuration) 屬性設為 [EncryptionConfiguration](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.encryption_configuration.EncryptionConfiguration?hl=zh-tw) 物件，透過客戶代管的加密金鑰保護新資料表。

```
from google.cloud import bigquery

client = bigquery.Client()

# TODO(dev): Change table_id to the full name of the table you want to create.
table_id = "your-project.your_dataset.your_table_name"

# Set the encryption key to use for the table.
# TODO: Replace this key with a key you have created in Cloud KMS.
kms_key_name = "projects/your-project/locations/us/keyRings/test/cryptoKeys/test"

table = bigquery.Table(table_id)
table.encryption_configuration = bigquery.EncryptionConfiguration(
    kms_key_name=kms_key_name
)
table = client.create_table(table)  # API request

print(f"Created {table_id}.")
print(f"Key: {table.encryption_configuration.kms_key_name}.")
```

### 查詢受 Cloud KMS 金鑰保護的資料表

不需要任何特殊設定，即可查詢 Cloud KMS 保護的資料表。BigQuery 會儲存用於加密資料表內容的金鑰名稱，並且在查詢受 Cloud KMS 保護的資料表時使用該金鑰。

只要 BigQuery 可存取用來加密資料表內容的 Cloud KMS 金鑰，包括 BigQuery 主控台和 bq 指令列工具在內的所有現有工具，其執行方式都與使用預設加密資料表相同。

### 使用 Cloud KMS 金鑰保護查詢結果

根據預設，查詢結果會儲存在以Google-owned and Google-managed encryption key加密的暫存資料表中。如果專案已有[預設金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#project_default_key)，系統會將該金鑰套用至臨時 (預設) 查詢結果資料表。如要改用 Cloud KMS 金鑰加密查詢結果，請選取下列其中一個選項：

### 控制台

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 [Compose new query] (撰寫新查詢)。
3. 在查詢文字區域中輸入有效的 GoogleSQL 查詢。
4. 依序點按「更多」、「查詢設定」和「進階選項」。
5. 選取「客戶管理的加密技術」。
6. 選取金鑰。如果清單中未顯示你要使用的金鑰，請輸入金鑰的[資源 ID](#key_resource_id)。
7. 按一下 [儲存]。
8. 按一下「執行」。

### bq

指定 `--destination_kms_key` 旗標，透過您的 Cloud KMS 金鑰來保護目的地資料表或查詢結果 (如果使用臨時資料表)。
`--destination_kms_key` 旗標會指定與目的地或結果資料表搭配使用的金鑰[資源 ID](#key_resource_id)。

(選用) 使用 `--destination_table` 旗標來指定查詢結果的目的地。如果不使用 `--destination_table`，則查詢結果會寫入臨時資料表。

如何查詢資料表：

```
bq query \
--destination_table=DATASET_ID.TABLE_ID \
--destination_kms_key projects/KMS_PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY \
"SELECT name,count FROM DATASET_ID.TABLE_ID WHERE gender = 'M' ORDER BY count DESC LIMIT 6"
```

如要進一步瞭解 bq 指令列工具，請參閱[使用 bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

建立資料表前，請先將 [Table.encryption\_configuration](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.Table?hl=zh-tw#google_cloud_bigquery_table_Table_encryption_configuration) 屬性設為 [EncryptionConfiguration](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.encryption_configuration.EncryptionConfiguration?hl=zh-tw) 物件，透過客戶代管的加密金鑰保護新資料表。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// queryWithDestinationCMEK demonstrates saving query results to a destination table and protecting those results
// by specifying a customer managed encryption key.
func queryWithDestinationCMEK(w io.Writer, projectID, dstDatasetID, dstTableID string) error {
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
	q.QueryConfig.Dst = client.Dataset(dstDatasetID).Table(dstTableID)
	q.DestinationEncryptionConfig = &bigquery.EncryptionConfig{
		// TODO: Replace this key with a key you have created in Cloud KMS.
		KMSKeyName: "projects/cloud-samples-tests/locations/us-central1/keyRings/test/cryptoKeys/test",
	}
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

建立資料表前，請先將 [Table.encryption\_configuration](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.table.Table?hl=zh-tw#google_cloud_bigquery_table_Table_encryption_configuration) 屬性設為 [EncryptionConfiguration](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.encryption_configuration.EncryptionConfiguration?hl=zh-tw) 物件，透過客戶代管的加密金鑰保護新資料表。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.EncryptionConfiguration;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;

// Sample to query on destination table with encryption key
public class QueryDestinationTableCMEK {

  public static void runQueryDestinationTableCMEK() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String kmsKeyName = "MY_KMS_KEY_NAME";
    String query =
        String.format("SELECT stringField, booleanField FROM %s.%s", datasetName, tableName);
    EncryptionConfiguration encryption =
        EncryptionConfiguration.newBuilder().setKmsKeyName(kmsKeyName).build();
    queryDestinationTableCMEK(query, encryption);
  }

  public static void queryDestinationTableCMEK(String query, EncryptionConfiguration encryption) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      QueryJobConfiguration config =
          QueryJobConfiguration.newBuilder(query)
              // Set the encryption key to use for the destination.
              .setDestinationEncryptionConfiguration(encryption)
              .build();

      TableResult results = bigquery.query(config);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));
      System.out.println("Query performed successfully with encryption key.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

先將 [QueryJobConfig.destination\_encryption\_configuration](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJobConfig?hl=zh-tw#google_cloud_bigquery_job_QueryJobConfig_destination_encryption_configuration) 屬性設為 [EncryptionConfiguration](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.encryption_configuration.EncryptionConfiguration?hl=zh-tw)，透過客戶代管的加密金鑰來保護查詢目的地資料表，接著才執行查詢。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the destination table.
# table_id = "your-project.your_dataset.your_table_name"

# Set the encryption key to use for the destination.
# TODO(developer): Replace this key with a key you have created in KMS.
# kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
#     your-project, location, your-ring, your-key
# )

job_config = bigquery.QueryJobConfig(
    destination=table_id,
    destination_encryption_configuration=bigquery.EncryptionConfiguration(
        kms_key_name=kms_key_name
    ),
)

# Start the query, passing in the extra configuration.
query_job = client.query(
    "SELECT 17 AS my_col;", job_config=job_config
)  # Make an API request.
query_job.result()  # Wait for the job to complete.

table = client.get_table(table_id)  # Make an API request.
if table.encryption_configuration.kms_key_name == kms_key_name:
    print("The destination table is written using the encryption configuration")
```

### 載入受 Cloud KMS 保護的資料表

如何在受 Cloud KMS 保護的資料表中載入資料檔案：

### 主控台

指定載入資料表時要使用的金鑰，以透過客戶代管的加密金鑰來保護載入工作目的地資料表。

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下資料集。資料集會在分頁中開啟。
4. 在詳細資料窗格中，按一下「建立資料表」。
5. 輸入載入資料表時要使用的選項，但請先按一下 [Advanced options] (進階選項)，再點選 [Create table] (建立資料表)。
6. 在「Encryption」(加密) 底下，選取 [Customer-managed key] (客戶管理的金鑰)。
7. 按一下「選取客戶代管的金鑰」下拉式選單，然後選取要使用的金鑰。如果找不到任何可用的金鑰，請輸入[金鑰資源 ID](#key_resource_id)。
8. 點選「建立資料表」。

### bq

設定 `--destination_kms_key` 旗標，透過客戶代管的加密金鑰來保護載入工作目的地資料表。

```
bq --location=LOCATION load \
--autodetect \
--source_format=FORMAT \
--destination_kms_key projects/KMS_PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY \
DATASET.TABLE \
path_to_source
```

例如：

```
bq load \
--autodetect \
--source_format=NEWLINE_DELIMITED_JSON \
--destination_kms_key projects/KMS_PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY \
test2.table4 \
gs://cloud-samples-data/bigquery/us-states/us-states.json
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

// importJSONWithCMEK demonstrates loading newline-delimited JSON from Cloud Storage,
// and protecting the data with a customer-managed encryption key.
func importJSONWithCMEK(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states.json")
	gcsRef.SourceFormat = bigquery.JSON
	gcsRef.AutoDetect = true
	loader := client.Dataset(datasetID).Table(tableID).LoaderFrom(gcsRef)
	loader.WriteDisposition = bigquery.WriteEmpty
	loader.DestinationEncryptionConfig = &bigquery.EncryptionConfig{
		// TODO: Replace this key with a key you have created in KMS.
		KMSKeyName: "projects/cloud-samples-tests/locations/us-central1/keyRings/test/cryptoKeys/test",
	}

	job, err := loader.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}

	if status.Err() != nil {
		return fmt.Errorf("job completed with error: %v", status.Err())
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
import com.google.cloud.bigquery.EncryptionConfiguration;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.TableId;

// Sample to load JSON data with configuration key from Cloud Storage into a new BigQuery table
public class LoadJsonFromGCSCMEK {

  public static void runLoadJsonFromGCSCMEK() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String kmsKeyName = "MY_KMS_KEY_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.json";
    // i.e. projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{cryptoKey}
    EncryptionConfiguration encryption =
        EncryptionConfiguration.newBuilder().setKmsKeyName(kmsKeyName).build();
    loadJsonFromGCSCMEK(datasetName, tableName, sourceUri, encryption);
  }

  public static void loadJsonFromGCSCMEK(
      String datasetName, String tableName, String sourceUri, EncryptionConfiguration encryption) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      LoadJobConfiguration loadConfig =
          LoadJobConfiguration.newBuilder(tableId, sourceUri)
              // Set the encryption key to use for the destination.
              .setDestinationEncryptionConfiguration(encryption)
              .setFormatOptions(FormatOptions.json())
              .setAutodetect(true)
              .build();

      // Load data from a GCS JSON file into the table
      Job job = bigquery.create(JobInfo.of(loadConfig));
      // Blocks until this load table job completes its execution, either failing or succeeding.
      job = job.waitFor();
      if (job.isDone()) {
        System.out.println("Table loaded succesfully from GCS with configuration key");
      } else {
        System.out.println(
            "BigQuery was unable to load into the table due to an error:"
                + job.getStatus().getError());
      }
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Column not added during load append \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

將 [LoadJobConfig.destination\_encryption\_configuration](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_destination_encryption_configuration) 屬性設為 [EncryptionConfiguration](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.encryption_configuration.EncryptionConfiguration?hl=zh-tw)，透過客戶代管的加密金鑰來保護載入工作目的地資料表，然後載入資料表。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name

# Set the encryption key to use for the destination.
# TODO: Replace this key with a key you have created in KMS.
# kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
#     "cloud-samples-tests", "us", "test", "test"
# )

job_config = bigquery.LoadJobConfig(
    autodetect=True,
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    destination_encryption_configuration=bigquery.EncryptionConfiguration(
        kms_key_name=kms_key_name
    ),
)

uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"

load_job = client.load_table_from_uri(
    uri,
    table_id,
    location="US",  # Must match the destination dataset location.
    job_config=job_config,
)  # Make an API request.

assert load_job.job_type == "load"

load_job.result()  # Waits for the job to complete.

assert load_job.state == "DONE"
table = client.get_table(table_id)

if table.encryption_configuration.kms_key_name == kms_key_name:
    print("A table loaded with encryption configuration key")
```

## 以串流方式將資料傳入受 Cloud KMS 保護的資料表

您可以直接以串流方式將資料傳入受 CMEK 保護的 BigQuery 資料表，而不必指定任何其他參數。請注意，系統會在緩衝區和最終位置中，使用您的 Cloud KMS 金鑰對這些資料進行加密。在搭配 CMEK 資料表使用串流功能前，請先瞭解要符合哪些條件才能確保[金鑰可供使用及存取](#key_access)。

如要進一步瞭解串流功能，請參閱[使用 BigQuery Storage Write API 串流資料](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)。

## 將資料表的保護機制從預設加密改成 Cloud KMS 防護

### bq

您可以使用 `bq cp` 指令搭配 `--destination_kms_key` 旗標，將受預設加密保護的資料表複製到新資料表或受 Cloud KMS 保護的原始資料表中。`--destination_kms_key` 旗標會指定要與目的地資料表搭配使用的金鑰[資源 ID](#key_resource_id)。

如何將採預設加密機制的資料表複製到受 Cloud KMS 保護的新資料表：

```
bq cp \
--destination_kms_key projects/KMS_PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY \
SOURCE_DATASET_ID.SOURCE_TABLE_ID DESTINATION_DATASET_ID.DESTINATION_TABLE_ID
```

如何將採預設加密機制的資料表複製到受 Cloud KMS 保護的相同資料表：

```
bq cp -f \
--destination_kms_key projects/KMS_PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY \
DATASET_ID.TABLE_ID DATASET_ID.TABLE_ID
```

如要將資料表的保護機制從 Cloud KMS 防護改成預設加密，請在不使用 `--destination_kms_key` 旗標的情況下，直接執行 `bq cp` 將檔案複製到同一個檔案。

如要進一步瞭解 bq 指令列工具，請參閱[使用 bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// copyTableWithCMEK demonstrates creating a copy of a table and ensuring the copied data is
// protected with a customer managed encryption key.
func copyTableWithCMEK(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	srcTable := client.DatasetInProject("bigquery-public-data", "samples").Table("shakespeare")
	copier := client.Dataset(datasetID).Table(tableID).CopierFrom(srcTable)
	copier.DestinationEncryptionConfig = &bigquery.EncryptionConfig{
		// TODO: Replace this key with a key you have created in Cloud KMS.
		KMSKeyName: "projects/cloud-samples-tests/locations/us-central1/keyRings/test/cryptoKeys/test",
	}
	job, err := copier.Run(ctx)
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
import com.google.cloud.bigquery.CopyJobConfiguration;
import com.google.cloud.bigquery.EncryptionConfiguration;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.TableId;

// Sample to copy a cmek table
public class CopyTableCMEK {

  public static void runCopyTableCMEK() {
    // TODO(developer): Replace these variables before running the sample.
    String destinationDatasetName = "MY_DESTINATION_DATASET_NAME";
    String destinationTableId = "MY_DESTINATION_TABLE_NAME";
    String sourceDatasetName = "MY_SOURCE_DATASET_NAME";
    String sourceTableId = "MY_SOURCE_TABLE_NAME";
    String kmsKeyName = "MY_KMS_KEY_NAME";
    EncryptionConfiguration encryption =
        EncryptionConfiguration.newBuilder().setKmsKeyName(
```