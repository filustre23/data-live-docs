Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 SQL 預存程序

*預存程序*是一組陳述式，可從其他查詢或其他預存程序呼叫。程序可以接受輸入引數，並傳回輸出值。您可以在 BigQuery 資料集中命名及儲存程序。多位使用者可透過預存程序存取或修改多個資料集的資料。也可以包含[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)。

部分預存程序已內建於 BigQuery，不需要建立。這些稱為「系統程序」，如要進一步瞭解，請參閱「[系統程序參考資料](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw)」。

預存程序支援*程序語言陳述式*，可讓您執行定義變數和實作控制流程等動作。如要進一步瞭解程序語言陳述式，請參閱「[程序語言參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)」。

## 建立預存程序

選擇下列其中一個選項來建立預存程序：

### SQL

如要建立程序，請使用 [`CREATE PROCEDURE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_procedure) 陳述式。

在下列概念範例中，`procedure_name` 代表程序，而程序主體會出現在 [`BEGIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#begin) 和 `END` 陳述式之間：

```
CREATE PROCEDURE dataset_name.procedure_name()
BEGIN
-- statements here
END
```

以下範例顯示包含多重陳述式查詢的程序。多重陳述式查詢會設定變數、執行 `INSERT` 陳述式，並以格式化文字字串的形式顯示結果。

```
CREATE OR REPLACE PROCEDURE mydataset.create_customer()
BEGIN
  DECLARE id STRING;
  SET id = GENERATE_UUID();
  INSERT INTO mydataset.customers (customer_id)
    VALUES(id);
  SELECT FORMAT("Created customer %s", id);
END
```

在上述範例中，程序的名稱為 `mydataset.create_customer`，程序主體則顯示在 [`BEGIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#begin) 和 `END` 陳述式之間。

如要呼叫程序，請使用 [`CALL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#call) 陳述式：

```
CALL mydataset.create_customer();
```

### Terraform

使用 [`google_bigquery_routine` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_routine)。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 Cloud Resource Manager API。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會建立名為 `my_stored_procedure` 的預存程序：

```
# Creates a SQL stored procedure.

# Create a dataset to contain the stored procedure.
resource "google_bigquery_dataset" "my_dataset" {
  dataset_id = "my_dataset"
}

# Create a stored procedure.
resource "google_bigquery_routine" "my_stored_procedure" {
  dataset_id      = google_bigquery_dataset.my_dataset.dataset_id
  routine_id      = "my_stored_procedure"
  routine_type    = "PROCEDURE"
  language        = "SQL"
  definition_body = "SELECT * FROM `bigquery-public-data.ml_datasets.penguins`;"
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   每項專案只需要執行一次這個指令，且可以在任何目錄中執行。

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
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的範例程式碼。

   將範例程式碼複製到新建立的 `main.tf`。

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

### 透過輸入參數傳遞值

程序可以有輸入參數。輸入參數可讓程序輸入資料，但無法輸出資料。

```
CREATE OR REPLACE PROCEDURE mydataset.create_customer(name STRING)
BEGIN
  DECLARE id STRING;
  SET id = GENERATE_UUID();
  INSERT INTO mydataset.customers (customer_id, name)
    VALUES(id, name);
  SELECT FORMAT("Created customer %s (%s)", id, name);
END
```

### 使用輸出參數傳遞值

程序可以有輸出參數。輸出參數會從程序傳回值，但不允許程序輸入。如要建立輸出參數，請在參數名稱前使用 `OUT` 關鍵字。

舉例來說，這個版本的程序會透過 `id` 參數傳回新顧客 ID：

```
CREATE OR REPLACE PROCEDURE mydataset.create_customer(name STRING, OUT id STRING)
BEGIN
  SET id = GENERATE_UUID();
  INSERT INTO mydataset.customers (customer_id, name)
    VALUES(id, name);
  SELECT FORMAT("Created customer %s (%s)", id, name);
END
```

如要呼叫這個程序，您必須使用變數來接收輸出值：

```
--- Create a new customer record.
DECLARE id STRING;
CALL mydataset.create_customer("alice",id);

--- Display the record.
SELECT * FROM mydataset.customers
WHERE customer_id = id;
```

### 使用輸入/輸出參數傳遞值

程序也可以有輸入/輸出參數。輸入/輸出參數會從程序傳回值，也會接受程序的輸入內容。如要建立輸入/輸出參數，請在參數名稱前使用 `INOUT` 關鍵字。詳情請參閱「[引數模式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#argument_mode)」。

## 授權處理常式

您可以將預存程序授權為*常式*。
授權常式可讓您與特定使用者或群組分享查詢結果，而不授予他們產生結果的基礎資料表存取權。舉例來說，授權常式可以計算資料的匯總值，或查閱資料表值並用於計算。

授權常式可以[建立](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)、[捨棄](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_table_statement)及[操控資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw)，也可以[叫用基礎資料表上的其他預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw#call_a_stored_procedure)。

詳情請參閱「[已授權的日常安排](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)」。

## 呼叫預存程序

建立預存程序後，請使用 `CALL` 陳述式呼叫該程序。舉例來說，下列陳述式會呼叫預存程序 `create_customer`：

```
CALL mydataset.create_customer();
```

**注意：** 直接在查詢中加入程序的 SQL 陳述式，而不是呼叫預存程序，會造成少許效能負擔。

## 呼叫系統程序

如要呼叫內建系統程序，請使用 `CALL` 陳述式。
舉例來說，下列陳述式會呼叫系統程序 `BQ.REFRESH_MATERIALIZED_VIEW`：

```
CALL BQ.REFRESH_MATERIALIZED_VIEW;
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]