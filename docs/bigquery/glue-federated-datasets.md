Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立及管理 AWS Glue 聯合資料集

*聯合資料集*會鏡像處理外部資料來源的結構定義和資料表，讓這些項目顯示為 BigQuery 資料集中的唯讀資料表。您可以使用聯合資料集，在 BigQuery 中有效存取 AWS Glue 的資料。

## 事前準備

確認您已連線，可存取 AWS Glue 資料。

* 如要建立或修改連線，請按照「[連結至 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-tw)」一文中的操作說明進行。建立該連結時，請在 [BigQuery 的 AWS Identity and Access Management 政策](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-tw#creating-aws-iam-policy)中，加入 AWS Glue 的下列政策陳述式。除了 Amazon S3 bucket 中儲存 AWS Glue 資料表資料的其他權限外，也請加入這項陳述式。

  ```
  {
   "Effect": "Allow",
   "Action": [
     "glue:GetDatabase",
     "glue:GetTable",
     "glue:GetTables",
     "glue:GetPartitions"
   ],
   "Resource": [
     "arn:aws:glue:REGION:ACCOUNT_ID:catalog",
     "arn:aws:glue:REGION:ACCOUNT_ID:database/DATABASE_NAME",
     "arn:aws:glue:REGION:ACCOUNT_ID:table/DATABASE_NAME/*"
   ]
  }
  ```

  更改下列內容：

  + `REGION`：AWS 區域，例如 `us-east-1`
  + `ACCOUNT_ID:`：12 碼的 AWS 帳戶 ID
  + `DATABASE_NAME`：AWS Glue 資料庫名稱

### 所需權限

如要取得建立聯邦資料集所需的權限，請要求系統管理員授予您「[BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) 」(`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立聯邦資料集所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立聯邦資料集，必須具備下列權限：

* `bigquery.datasets.create`
* `bigquery.connections.use`
* `bigquery.connections.delegate`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 建立聯合資料集

如要建立聯邦資料集，請按照下列步驟操作：

### 控制台

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，選取要建立資料集的專案。
4. 按一下 more\_vert「View actions」(查看動作)，然後點選「Create dataset」(建立資料集)。
5. 在「建立資料集」頁面中，執行下列操作：

   * 針對「Dataset ID」(資料集 ID)，輸入唯一的資料集名稱。
   * 在「位置類型」部分，選擇資料集的 AWS 位置，例如 `aws-us-east-1`。建立資料集後，就無法變更位置。
   * 以「外部資料集」來說，請執行下列操作：

     + 勾選「外部資料集的連結」旁邊的方塊。
     + 在「External dataset type」(外部資料集類型) 中，選取 `AWS Glue`。
     + 在「外部來源」中，輸入 `aws-glue://`，然後輸入 AWS Glue 資料庫的 [Amazon Resource Name (ARN)](https://docs.aws.amazon.com/glue/latest/dg/glue-specifying-resource-arns.html)，例如 `aws-glue://arn:aws:glue:us-east-1:123456789:database/test_database`。
     + 在「連線 ID」部分，選取 AWS 連線。
   * 其他預設設定則保留不變。
6. 點選「建立資料集」。

### SQL

使用[`CREATE EXTERNAL SCHEMA`資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_schema_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE EXTERNAL SCHEMA DATASET_NAME
   WITH CONNECTION PROJECT_ID.CONNECTION_LOCATION.CONNECTION_NAME
     OPTIONS (
       external_source = 'AWS_GLUE_SOURCE',
       location = 'LOCATION');
   ```

   請替換下列項目：

   * `DATASET_NAME`：BigQuery 中新資料集的名稱。
   * `PROJECT_ID`：您的專案 ID。
   * `CONNECTION_LOCATION`：AWS 連線的位置，例如 `aws-us-east-1`。
   * `CONNECTION_NAME`：AWS 連線的名稱。
   * `AWS_GLUE_SOURCE`：AWS Glue 資料庫的 [Amazon 資源名稱 (ARN)](https://docs.aws.amazon.com/glue/latest/dg/glue-specifying-resource-arns.html)，並加上識別來源的前置字元，例如 `aws-glue://arn:aws:glue:us-east-1:123456789:database/test_database`。
   * `LOCATION`：BigQuery 中新資料集的位置，例如 `aws-us-east-1`。建立資料集後，就無法變更位置。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

在指令列環境中，使用 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)建立資料集：

```
bq --location=LOCATION mk --dataset \
    --external_source aws-glue://AWS_GLUE_SOURCE \
    --connection_id PROJECT_ID.CONNECTION_LOCATION.CONNECTION_NAME \
    DATASET_NAME
```

更改下列內容：

* `LOCATION`：BigQuery 中新資料集的位置，例如 `aws-us-east-1`。建立資料集後，就無法變更位置。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定預設位置值。
* `AWS_GLUE_SOURCE`：AWS Glue 資料庫的 [Amazon 資源名稱 (ARN)](https://docs.aws.amazon.com/glue/latest/dg/glue-specifying-resource-arns.html)，例如 `arn:aws:glue:us-east-1:123456789:database/test_database`。
* `PROJECT_ID`：BigQuery 專案 ID。
* `CONNECTION_LOCATION`：AWS 連線的位置，例如 `aws-us-east-1`。
* `CONNECTION_NAME`：AWS 連線的名稱。
* `DATASET_NAME`：BigQuery 中新資料集的名稱。如要在非預設專案中建立資料集，請採用下列格式將專案 ID 新增至資料集名稱：`PROJECT_ID`:`DATASET_NAME`。

### Terraform

使用 [`google_bigquery_dataset` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset#example-usage---bigquery-dataset-external-reference-aws-docs)。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會建立 AWS Glue 聯合資料集：

```
resource "google_bigquery_dataset" "dataset" {
  provider                    = google-beta
  dataset_id                  = "example_dataset"
  friendly_name               = "test"
  description                 = "This is a test description."
  location                    = "aws-us-east-1"

external_dataset_reference {
  external_source = "aws-glue://arn:aws:glue:us-east-1:999999999999:database/database"
  connection      = "projects/project/locations/aws-us-east-1/connections/connection"
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

### API

使用已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)和 AWS Glue 資料庫的 [`externalDatasetReference` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw#ExternalDatasetReference)，呼叫 [`datasets.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw)。

## 列出聯合資料集中的資料表

如要列出可在聯邦資料集中查詢的資料表，請參閱「[列出資料集](https://docs.cloud.google.com/bigquery/docs/listing-datasets?hl=zh-tw)」。

## 取得資料表資訊

如要取得聯邦資料集中的資料表相關資訊 (例如結構定義詳細資料)，請參閱「[取得資料表資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_table_information)」。

## 控管資料表的存取權

如要管理對同盟資料集中資料表的存取權，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

此外，系統也支援對聯邦資料集中的資料表套用[資料列層級安全防護](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)、[資料欄層級安全防護](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。

如果執行可能導致安全性政策失效的結構定義作業 (例如刪除 AWS Glue 中的資料欄)，工作就會失敗，直到政策更新為止。此外，如果您在 AWS Glue 中刪除資料表並重新建立，安全性政策就不會再套用至重新建立的資料表。

## 查詢 AWS Glue 資料

[查詢聯合式資料集中的資料表](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)，與查詢任何其他 BigQuery 資料集中的資料表相同。

您可以查詢下列格式的 AWS Glue 資料表：

* CSV (壓縮和未壓縮)
* JSON (壓縮和未壓縮)
* Parquet
* ORC
* Avro
* Iceberg
* Delta Lake

## 資料表對應詳細資料

您在 AWS Glue 資料庫中授予存取權的每個資料表，都會以對等資料表的形式顯示在 BigQuery 資料集中。

### 格式

各個 BigQuery 資料表的格式取決於相應 [AWS Glue 資料表](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-catalog-tables.html#aws-glue-api-catalog-tables-Table)的下列欄位：

* `InputFormat` (`Table.StorageDescriptor.InputFormat`)
* `OutputFormat` (`Table.StorageDescriptor.OutputFormat`)
* `SerializationLib` (`Table.StorageDescriptor.SerdeInfo.SerializationLibrary`)

但 Iceberg 資料表是例外，這類資料表會使用 `TableType` (`Table.Parameters["table_type"]`) 欄位。

舉例來說，具有下列欄位的 AWS Glue 資料表會對應至 BigQuery 中的 ORC 資料表：

* `InputFormat` = `"org.apache.hadoop.hive.ql.io.orc.OrcInputFormat"`
* `OutputFormat` = `"org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat"`
* `SerializationLib` = `"org.apache.hadoop.hive.ql.io.orc.OrcSerde"`

### 位置

每個 BigQuery 資料表的位置取決於下列因素：

* Iceberg 資料表：AWS Glue 資料表中的 `Table.Parameters["metadata_location"]` 欄位
* 非 Iceberg 非分區資料表：AWS Glue 資料表中的 `Table.StorageDescriptor.Location` 欄位
* 非 Iceberg 分區資料表：AWS Glue GetPartitions API

### 其他屬性

此外，系統會自動將部分 AWS Glue 資料表屬性對應至 BigQuery 中的格式專屬選項：

| **格式** | **SerializationLib** | **AWS Glue 資料表值** | **BigQuery 選項** |
| --- | --- | --- | --- |
| CSV | LazySimpleSerDe | Table.StorageDescriptor.SerdeInfo.Parameters["field.delim"] | [CsvOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#csvoptions).fieldDelimiter |
| CSV | LazySimpleSerDe | Table.StorageDescriptor.Parameters["serialization.encoding"] | [CsvOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#csvoptions).encoding |
| CSV | LazySimpleSerDe | Table.StorageDescriptor.Parameters["skip.header.line.count"] | [CsvOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#csvoptions).skipLeadingRows |
| CSV | OpenCsvSerDe | Table.StorageDescriptor.SerdeInfo.Parameters["separatorChar"] | [CsvOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#csvoptions).fieldDelimiter |
| CSV | OpenCsvSerDe | Table.StorageDescriptor.SerdeInfo.Parameters["quoteChar"] | [CsvOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#csvoptions).quote |
| CSV | OpenCsvSerDe | Table.StorageDescriptor.Parameters["serialization.encoding"] | [CsvOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#csvoptions).encoding |
| CSV | OpenCsvSerDe | Table.StorageDescriptor.Parameters["skip.header.line.count"] | [CsvOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#csvoptions).skipLeadingRows |
| JSON | Hive [JsonSerDe](https://github.com/apache/hive/blob/master/hcatalog/core/src/main/java/org/apache/hive/hcatalog/data/JsonSerDe.java) | Table.StorageDescriptor.Parameters["serialization.encoding"] | [JsonOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#jsonoptions).encoding |

## 在同盟資料集中建立檢視表

您無法在同盟資料集中建立檢視區塊。不過，您可以在標準資料集中建立檢視表，並以聯邦資料集中的資料表為基礎。詳情請參閱「[建立檢視區塊](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)」。

## 刪除聯邦資料集

刪除聯合資料集與刪除任何其他 BigQuery 資料集相同。詳情請參閱「[刪除資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#delete-datasets)」。

## 定價

如要瞭解定價資訊，請參閱「[BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)」一文。

## 限制

* 適用所有 [BigQuery Omni 限制](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#limitations)。
* 您無法在 AWS Glue 聯邦資料集的資料表中新增、刪除或更新資料或中繼資料。
* 您無法在 AWS Glue 聯邦資料集中建立新資料表、檢視區塊或具體化檢視區塊。
* 不支援[`INFORMATION_SCHEMA`檢視](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)。
* 不支援[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)。
* 與資料表建立預設值相關的資料集層級設定不會影響聯邦資料集，因為您無法手動建立資料表。
* Avro 資料表不支援 Apache Hive 資料類型 `UNION`。
* 須遵守[外部表格限制](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#limitations)。

## 後續步驟

* 進一步瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 試試 [BigQuery Omni with AWS 實驗室](https://www.cloudskillsboost.google/catalog_lab/5345?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]