Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# bq 指令列工具參考資料

本文說明 `bq` 的語法、指令、旗標和引數。
是 BigQuery 的 Python 指令列工具。

如需使用 bq 指令列工具的教學課程，請參閱「[使用 bq 工具載入及查詢資料](https://docs.cloud.google.com/bigquery/docs/quickstarts/load-data-bq?hl=zh-tw)」。

## bq 指令列工具的使用方式

您可以在 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 中輸入 bq 指令列工具指令，方法是透過 Google Cloud 控制台，或從本機安裝的 [Google Cloud CLI](https://docs.cloud.google.com/sdk/docs?hl=zh-tw)。

* 如要透過 Google Cloud 控制台使用 bq 指令列工具，請啟用 Cloud Shell：

  [啟用 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)
* 如要在本機使用 bq 指令列工具，請[安裝並設定 gcloud CLI](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw)。如要讓安裝項目保持最新狀態，請參閱 gcloud CLI 說明文件中的「[管理安裝項目](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw#manage_an_installation)」。

## 指令格式

bq 指令列工具使用下列格式：

`bq COMMAND [FLAGS] [ARGUMENTS]`

部分旗標可與多個 bq 指令列工具指令搭配使用，這些旗標會在「[全域旗標](#global_flags)」一節中說明。

其他旗標則為指令專用，只能與特定 bq 指令列工具指令搭配使用。指令專屬旗標則會在指令章節中說明。

## 指定標記的值

指定旗標值時，等號 (`=`) 為選用。例如，以下兩個指令的作用相同：

```
bq ls --format prettyjson myDataset
bq ls --format=prettyjson myDataset
```

為求明確，本文使用等號。

部分 bq 指令列工具旗標為*布林值*，您可以將旗標值設為 `true` 或 `false`。bq 指令列工具接受下列格式來設定布林旗標。

| 值 | 格式 | 範例 |
| --- | --- | --- |
| `true` | `--FLAGNAME=true` | `--debug_mode=true` |
| `true` | `--FLAGNAME` | `--debug_mode` |
| `false` | `--FLAGNAME=false` | `--debug_mode=false` |
| `false` | `--noFLAGNAME` | `--nodebug_mode` |

本文件使用 `--FLAGNAME=VALUE` 格式表示布林值旗標。

所有布林值旗標都是選用項目；如果沒有布林值旗標，BigQuery 會使用旗標的預設值。

## 在引數中指定 BigQuery 資源

指定資源的格式取決於情境；在某些情況下，專案和資料集之間的分隔符號是冒號 (`:`)，在某些情況下則是半形句號 (`.`)。下表說明如何在不同情境中指定 BigQuery 資料表。

| 背景資訊 | 格式 | 範例 |
| --- | --- | --- |
| bq 指令列工具 | `PROJECT:DATASET.TABLE` | `myProject:myDataset.myTable` |
| GoogleSQL 查詢 | `PROJECT.DATASET.TABLE` | `myProject.myDataset.myTable` |
| 舊版 SQL 查詢 | `PROJECT:DATASET.TABLE` | `myProject:myDataset.myTable` |

如未指定專案，BigQuery 會使用目前的專案。舉例來說，如果目前的專案是 `myProject`，BigQuery 會將 `myDataset.myTable` 解讀為 `myProject:myDataset.myTable` (或 `myProject.myDataset.myTable`)。

部分資源 ID 必須使用反引號 (`` ` ``) 括住。如果資源 ID 開頭為英文字母或底線字元，且僅包含英文字母、數字和底線字元，則不需括住。不過，如果資源 ID 包含其他類型的字元或保留關鍵字，則須在 ID (或 ID 中含有特殊字元或保留關鍵字的部分) 前後加上反引號。詳情請參閱「[ID](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#identifiers)」。

## 如何執行指令

請將任何[通用旗標](#global_flags)放在 `bq` 指令之前，然後加入指令專屬旗標。您可以加入多個全域或指令專屬旗標。例如：

```
bq --location=us mk --reservation --project_id=project reservation_name
```

您可以透過下列方式指定指令引數：

* `--FLAG ARGUMENT` (如前述範例所示)
* `--FLAG=ARGUMENT`
* `--FLAG='ARGUMENT'`
* `--FLAG="ARGUMENT"`
* `--FLAG 'ARGUMENT'`
* `--FLAG "ARGUMENT"`

更改下列內容：

* `FLAG`：全域或指令專屬旗標
* `ARGUMENT`：旗標的引數

部分指令需要使用引號括住引數。如果需要引號，單引號或雙引號皆可。需要引號的引數通常是包含空格、逗號或其他特殊字元的值。如果引數包含 BigQuery 資源，請務必遵循[在指令中指定資源名稱的規則](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#specify-resource)。

**注意：** 下列範例使用 `--nouse_legacy_sql` 旗標。除非您[在 `.bigqueryrc` 中設定預設值](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#set_default_values_for_command-line_flags)，或在專案或組織層級[將設定](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_project_set_options_statement)
`default_sql_dialect_option` 設為「default\_legacy\_sql」，否則必須使用這個旗標，才能從指令列執行 GoogleSQL 查詢。

以下範例說明如何在指令列執行 GoogleSQL 查詢：

```
bq query --nouse_legacy_sql \
'SELECT
   COUNT(*)
 FROM
   `bigquery-public-data`.samples.shakespeare'
```

指定含布林值的標記時，可不用引數。如果指定 `true` 或 `false`，則必須使用 `FLAG=ARGUMENT` 格式。

舉例來說，以下指令在布林值旗標 `--use_legacy_sql` 前加上 `no` 藉此指定 false：

```
bq query --nouse_legacy_sql \
'SELECT
   COUNT(*)
 FROM
   `bigquery-public-data`.samples.shakespeare'
```

或者，如要將 `false` 指定為旗標的引數，可以輸入以下內容：

```
bq query --use_legacy_sql=false \
'SELECT
   COUNT(*)
 FROM
   `bigquery-public-data`.samples.shakespeare'
```

### 在指令碼中執行指令

您可以在指令碼中執行 bq 指令列工具，就像執行 [Google Cloud CLI 指令](https://docs.cloud.google.com/sdk/docs/scripting-gcloud?hl=zh-tw)一樣。以下是 Bash 指令碼中 `gcloud` 和 `bq` 指令的範例：

```
#!/bin/bash
gcloud config set project myProject
bq query --use_legacy_sql=false --destination_table=myDataset.myTable \
'SELECT
   word,
   SUM(word_count) AS count
 FROM
   `bigquery-public-data`.samples.shakespeare
 WHERE
   word LIKE "%raisin%"
 GROUP BY
   word'
```

### 使用服務帳戶

您可以使用[服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)，代表您執行已授權的 API 呼叫或查詢工作。如要在 bq 指令列工具中使用服務帳戶，請從服務帳戶授權存取 Google Cloud 。詳情請參閱「[gcloud auth activate-service-account](https://docs.cloud.google.com/sdk/gcloud/reference/auth/activate-service-account?hl=zh-tw)」。

如要開始使用[服務帳戶模擬](https://docs.cloud.google.com/iam/docs/impersonating-service-accounts?hl=zh-tw)執行 `bq` 指令，請執行下列指令：

```
gcloud config set auth/impersonate_service_account SERVICE_ACCOUNT_NAME
```

將 `SERVICE_ACCOUNT_NAME` 替換為服務帳戶名稱。

您現在執行的 `bq` 指令會使用服務帳戶憑證。

如要停止透過服務帳戶執行 `bq` 指令，請執行下列指令：

```
gcloud config unset auth/impersonate_service_account
```

## 設定指令列旗標的預設值

如要設定指令列旗標的預設值，請將這些旗標加入 bq 指令列工具的設定檔 `.bigqueryrc`。設定預設選項前，您必須先建立 `.bigqueryrc` 檔案。您可以使用偏好的文字編輯器建立檔案。建立 `.bigqueryrc` 檔案後，您可以使用 `--bigqueryrc` 全域旗標指定檔案路徑。

如未指定 `--bigqueryrc` 旗標，系統會使用 `BIGQUERYRC` 環境變數。如未指定，則會使用路徑 `~/.bigqueryrc`。預設路徑為 `$HOME/.bigqueryrc`。

**附註：**我們不建議使用 `bq init` 指令建立 `.bigqueryrc` 檔案。

### 如何為`.bigqueryrc`加上標記

如何將指令列旗標的預設值加入 `.bigqueryrc`：

* 將[全域旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#global_flags)放在檔案頂端，不加標頭。
* 如要使用指令專屬旗標，請輸入指令名稱 (以括號括住)，並在指令名稱後方加入指令專屬旗標 (每行一個)。

例如：

```
--apilog=stdout
--format=prettyjson
--location=US

[query]
--use_legacy_sql=false
--max_rows=100
--maximum_bytes_billed=10000000

[load]
--destination_kms_key=projects/myproject/locations/mylocation/keyRings/myRing/cryptoKeys/myKey
```

上述範例會為下列旗標設定預設值：

* 全域旗標 `--apilog` 設為 `stdout`，將偵錯輸出內容輸出至Google Cloud 控制台。
* 全域旗標 `--format` 設為 `prettyjson`，以人類可讀的 JSON 格式顯示指令輸出內容。
* 全域旗標 `--location` 設為 `US` 多區域位置。
* `query` 指令專屬旗標 `--use_legacy_sql` 設為 `false`，將 GoogleSQL 設為預設查詢語法。

  **附註：**您不能在 `.bigqueryrc` 中使用 `--nouse_legacy_sql`。
* `query` 指令專屬旗標 `--max_rows` 設為 `100`，用於控制查詢輸出中的資料列數量。
* `query` 指令專屬旗標 `--maximum_bytes_billed` 設為 10,000,000 位元組 (10 MB)，因此讀取超過 10 MB 資料的查詢會失敗。
* `load` 指令專屬旗標 [`--destination_kms_key`](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) 設為 `projects/myproject/locations/mylocation/keyRings/myRing/cryptoKeys/myKey`。

## CLI 說明

您可以執行下列指令，取得 bq 指令列工具的說明：

| 說明 | 說明指令格式 | 範例 |
| --- | --- | --- |
| 已安裝的版本 | `bq version` | `bq version` |
| 所有指令清單和範例 | `bq help` | `bq help` |
| 全域旗標說明 | `bq --help` | `bq --help` |
| 特定指令的說明 | `bq help COMMAND` | `bq help mk` |

## 疑難排解 CLI 指令

如要記錄傳送和接收的要求，請按照下列步驟操作：
:   新增 `--apilog=PATH_TO_FILE` 旗標，將作業記錄儲存至本機檔案。將 `PATH_TO_FILE` 替換為要儲存記錄的位置。bq 指令列工具會發出標準 REST 式 API 呼叫，這在疑難排解時很有幫助。向 Cloud Customer Care 回報問題時，也可以附上這份記錄。
:   使用 `-` 或 `stdout` (而非路徑) 會將記錄輸出至 Google Cloud 控制台。將 `--apilog` 設為 `stderr`，會輸出至標準錯誤檔案。如要記錄更多要求，請使用 `--httplib2_debuglevel=LOG_LEVEL` 旗標。`LOG_LEVEL` 越高，記錄的 HTTP 要求資訊就越多。

如要排解錯誤，請按照下列步驟操作：
:   取得[工作狀態](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)或查看資料表和資料集等資源的詳細資訊時，請輸入 `--format=prettyjson` 旗標。使用這個旗標會以 JSON 格式輸出回應，包括 `reason` 屬性。您可以使用 `reason` 屬性查看[錯誤訊息](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw)。
:   如要進一步瞭解執行指令時發生的錯誤，請使用 `--debug_mode` 旗標。

## 通用標記

您可以視情況搭配任何 `bq` 指令使用下列旗標：

**`--alpha=FEATURE_NAME`**
:   指定要啟用的 Alpha 版功能。

**`--api=ENDPOINT`**
:   指定要呼叫的 API 端點。預設值為 `https://bigquery.googleapis.com`。

**`--api_version=VERSION`**
:   指定要使用的 API 版本。預設值為 `v2`。

**`--apilog=FILE`**
:   將所有 API 要求和回應記錄到 `FILE` 指定的檔案。可能的值如下：

    * 檔案路徑：記錄會寫入指定檔案
    * `stdout` - 記錄到標準輸出內容
    * `stderr`：將記錄輸出至標準錯誤
    * `false`：不記錄 API 要求和回應 (預設)

**`--bigquery_discovery_api_key=API_KEY`**
:   指定用於導覽文件要求的 API 金鑰。

**`--bigqueryrc=PATH`**
:   指定 bq 指令列工具設定檔的路徑。如未指定 `--bigqueryrc` 旗標，指令會使用 `BIGQUERYRC` 環境變數。如未設定環境變數，則會使用 `$HOME/.bigqueryrc`。如果該檔案不存在，則會使用 `~/.bigqueryrc`。詳情請參閱「[設定指令列旗標的預設值](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)」。

**`--ca_certificates_file=PATH`**
:   指定[憑證授權單位服務](https://docs.cloud.google.com/certificate-authority-service?hl=zh-tw) (CA) 檔案的位置。

**`--dataset_id=DATASET_ID`**
:   指定要與指令搭配使用的預設資料集。如果不適用的話，系統會忽略這個標記。您可以使用 `PROJECT:DATASET` 或 `DATASET` 格式指定 `DATASET_ID` 引數。如果缺少 `PROJECT` 部分，則會使用預設專案。您可以指定 [`--project_id` 旗標](#project_id_flag)，覆寫預設專案設定。

**`--debug_mode={true|false}`**
:   如果設為 `true`，則會顯示 Python 例外狀況的回溯。預設值為 `false`。

**`--disable_ssl_validation={true|false}`**
:   如果設為 `true`，則會停用 HTTPS 憑證驗證。預設值為 `false`。

**`--discovery_file=PATH`**
:   指定要讀取以進行探索的 JSON 檔案。

**`--enable_gdrive={true|false}`**
:   如果設為 `false`，則會要求不含 Google 雲端硬碟範圍的新 OAuth 權杖。預設值為 `true`，會要求具有雲端硬碟範圍的新 OAuth 權杖。如要在使用使用者帳戶驗證時將這個旗標設為 `false`，則必須將 `--use_google_auth` 旗標設為 `false`。

**`--enable_resumable_uploads={true|false}`**
:   針對從本機檔案載入資料的工作，啟用透過 HTTP 支援續傳的上傳作業。預設值為 `true`。

**`--fingerprint_job_id={true|false}`**
:   如要使用衍生自工作設定指紋的工作 ID，請設為 `true`。這可避免不小心多次執行相同工作。預設值為 `false`。

**`--format=FORMAT`**
:   指定指令輸出內容的格式，請使用下列其中一個值：

    * `pretty`：格式化的資料表輸出內容
    * `sparse`：簡化的資料表輸出內容
    * `prettyjson`：容易理解的 JSON 格式
    * `json`：盡可能壓縮到最小的 JSON
    * `csv`：包含標頭的 csv 格式

    `pretty`、`sparse` 和 `prettyjson` 應為人類可讀。`json` 和 `csv` 應由其他程式使用。如果指定 `none`，指令不會產生任何輸出內容。如果沒有 `--format` 旗標，系統會根據指令選擇適當的輸出格式。

**`--headless={true|false}`**
:   如要在沒有使用者互動的情況下執行 `bq` 工作階段，請設為 `true`。例如，`debug_mode` 不會中斷偵錯工具，且資訊列印的頻率會降低。預設值為 `false`。

**`--httplib2_debuglevel=DEBUG_LEVEL`**
:   指定是否顯示 HTTP 偵錯資訊。如果 `DEBUG_LEVEL` 大於 `0`，指令除了記錄錯誤訊息，也會將 HTTP 伺服器要求和回應記錄到 stderr。如果 `DEBUG_LEVEL` 不大於 0，或未使用 `--httplib2_debuglevel` 旗標，則只會提供錯誤訊息。

    例如：

    ```
    --httplib2_debuglevel=1
    ```

    **注意：** 這個旗標不支援多層級偵錯，因此您可以將 `DEBUG_LEVEL` 設為任何正數。

**`--job_id=JOB_ID`**
:   指定新工作的 ID。這個旗標僅適用於建立工作的指令：`cp`、`extract`、`load` 和 `query`。如果不使用 `--job_id` 旗標，指令會產生專屬工作 ID。詳情請參閱「[透過程式輔助方式執行工作](https://docs.cloud.google.com/bigquery/docs/running-jobs?hl=zh-tw)」。

**`--job_property=KEY:VALUE`**
:   要納入工作設定 properties 欄位的鍵/值組合。重複使用這個旗標即可指定其他屬性。

**`--jobs_query_use_request_id={true|false}`**
:   如果設為 `true`，系統會在 `jobs.query` 要求中傳送要求 ID。預設值為 `false`。

**`--jobs_query_use_results_from_response={true|false}`**
:   如果設為 `true`，則會使用 `jobs.query` 回應的結果。預設值為 `true`。