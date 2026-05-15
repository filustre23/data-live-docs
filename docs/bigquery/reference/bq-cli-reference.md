Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# bq 指令列工具參考資料

本文說明 `bq` 的語法、指令、標記和引數。`bq` 是 BigQuery 專用的 Python 式指令列工具。

如需使用 bq 指令列工具的教學課程，請參閱「[使用 bq 工具載入及查詢資料](https://docs.cloud.google.com/bigquery/docs/quickstarts/load-data-bq?hl=zh-tw)」。

## 使用 bq 指令列工具的方法

您可以在 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 中輸入 bq 指令列工具指令， Google Cloud 控制台或本機安裝的 [Google Cloud CLI](https://docs.cloud.google.com/sdk/docs?hl=zh-tw) 皆可。

* 如要從 Google Cloud 控制台使用 bq 指令列工具，請啟動 Cloud Shell：

  [啟用 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)
* 如要在本機使用 bq 指令列工具，請[安裝及設定 gcloud CLI](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw)。如要讓安裝保持在最新狀態，請參閱 gcloud CLI 說明文件中的「[管理安裝作業](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw#manage_an_installation)」。

## 指令格式

bq 指令列工具使用下列格式：

`bq COMMAND [FLAGS] [ARGUMENTS]`

部分標記可搭配多個 bq 指令列工具指令使用，這些標記說明請參閱「[通用標記](#global_flags)」一節。

其他標記則為指令專屬，只能搭配特定 bq 指令列工具指令使用。指令專屬標記說明請參閱指令章節。

## 指定旗標的值

指定旗標的值時，等號 (`=`) 為選用。舉例來說，下列兩個指令的作用相同：

```
bq ls --format prettyjson myDataset
bq ls --format=prettyjson myDataset
```

為求明確，本文使用等號。

部分 bq 指令列工具旗標為*布林值*，您可以將旗標值設為 `true` 或 `false`。bq 指令列工具接受下列格式，用於設定布林值標記。

| 值 | 格式 | 範例 |
| --- | --- | --- |
| `true` | `--FLAGNAME=true` | `--debug_mode=true` |
| `true` | `--FLAGNAME` | `--debug_mode` |
| `false` | `--FLAGNAME=false` | `--debug_mode=false` |
| `false` | `--noFLAGNAME` | `--nodebug_mode` |

這份文件使用 `--FLAGNAME=VALUE` 格式表示布林值標記。

所有布林值旗標皆為選用，如果沒有布林值旗標，BigQuery 會使用旗標的預設值。

## 在引數中指定 BigQuery 資源

指定資源的格式取決於環境；在某些情況下，專案和資料集之間的分隔符號是半形冒號 (`:`)，在某些情況下則是半形句號 (`.`)。下表說明如何在不同環境中指定 BigQuery 資料表。

| 背景資訊 | 格式 | 範例 |
| --- | --- | --- |
| bq 指令列工具 | `PROJECT:DATASET.TABLE` | `myProject:myDataset.myTable` |
| GoogleSQL 查詢 | `PROJECT.DATASET.TABLE` | `myProject.myDataset.myTable` |
| 舊版 SQL 查詢 | `PROJECT:DATASET.TABLE` | `myProject:myDataset.myTable` |

如未指定專案，BigQuery 會使用目前的專案。舉例來說，如果目前專案是 `myProject`，BigQuery 會將 `myDataset.myTable` 解讀為 `myProject:myDataset.myTable` (或 `myProject.myDataset.myTable`)。

部分資源 ID 必須使用倒引號 (`` ` ``) 加上引號。如果資源 ID 以英文字母或底線開頭，且只包含英文字母、數字和底線，則不需要加上引號。不過，如果資源 ID 包含其他類型的字元或保留字，您需要以反引號括住 ID (或 ID 中含有特殊字元或保留字的部分)。詳情請參閱「[ID](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#identifiers)」。

## 如何執行指令

將所有[通用旗標](#global_flags)放在 `bq` 指令之前，然後加入指令專屬旗標。您可以加入多個通用旗標或指令專屬旗標。例如：

```
bq --location=us mk --reservation --project_id=project reservation_name
```

您可以使用下列方法指定指令引數：

* `--FLAG ARGUMENT` (如先前範例所示)
* `--FLAG=ARGUMENT`
* `--FLAG='ARGUMENT'`
* `--FLAG="ARGUMENT"`
* `--FLAG 'ARGUMENT'`
* `--FLAG "ARGUMENT"`

更改下列內容：

* `FLAG`：全域或指令專屬旗標
* `ARGUMENT`：旗標的引數

部分指令需要在引數周圍加上引號。如果需要引號，單引號或雙引號都可以。需要引號的引數通常是含有空格、逗號或其他特殊字元的值。如果引數包含 BigQuery 資源，請務必遵循[在指令中指定資源名稱的規則](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#specify-resource)。

**注意：** 下列範例使用 `--nouse_legacy_sql` 旗標。如要從指令列執行 GoogleSQL 查詢，就必須使用這個標記，除非您[在 `.bigqueryrc`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#set_default_values_for_command-line_flags) 中設定預設值，或[在專案或機構層級將設定](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_project_set_options_statement)
`default_sql_dialect_option`設為「default\_legacy\_sql」。

這個範例說明如何透過指令列執行 GoogleSQL 查詢：

```
bq query --nouse_legacy_sql \
'SELECT
   COUNT(*)
 FROM
   `bigquery-public-data`.samples.shakespeare'
```

指定含布林值的標記時，可不用引數。如果指定 `true` 或 `false`，就必須使用 `FLAG=ARGUMENT` 格式。

舉例來說，以下指令在布林值旗標 `--use_legacy_sql` 前加上 `no` 藉此指定 false：

```
bq query --nouse_legacy_sql \
'SELECT
   COUNT(*)
 FROM
   `bigquery-public-data`.samples.shakespeare'
```

如要將 `false` 指定為該旗標的引數，則可輸入以下指令：

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

您可以使用[服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)，代表您執行已授權的 API 呼叫或查詢作業。如要在 bq 指令列工具中使用服務帳戶，請從服務帳戶授權存取 Google Cloud 。詳情請參閱 [gcloud auth activate-service-account](https://docs.cloud.google.com/sdk/gcloud/reference/auth/activate-service-account?hl=zh-tw)。

如要開始使用`bq`指令，並[模擬服務帳戶](https://docs.cloud.google.com/iam/docs/impersonating-service-accounts?hl=zh-tw)，請執行下列指令：

```
gcloud config set auth/impersonate_service_account SERVICE_ACCOUNT_NAME
```

將 `SERVICE_ACCOUNT_NAME` 替換為服務帳戶名稱。

您現在執行的 `bq` 指令會使用服務帳戶憑證。

如要停止從服務帳戶執行 `bq` 指令，請執行下列指令：

```
gcloud config unset auth/impersonate_service_account
```

## 設定指令列旗標的預設值

如要設定指令列旗標的預設值，您可以在 bq 指令列工具的設定檔 `.bigqueryrc` 中加入旗標預設值。設定預設選項前，您必須先建立 `.bigqueryrc` 檔案。您可以使用自己偏好的文字編輯器建立該檔案。建立 `.bigqueryrc` 檔案後，您可以使用 `--bigqueryrc` 通用旗標指定該檔案的路徑。

如果未指定 `--bigqueryrc` 旗標，系統會使用 `BIGQUERYRC` 環境變數。如果未指定該變數，則會使用 `~/.bigqueryrc` 路徑。預設路徑為 `$HOME/.bigqueryrc`。

**附註：**我們不建議使用 `bq init` 指令建立 `.bigqueryrc` 檔案。

### 如何將旗標加入 `.bigqueryrc`

如何將指令列旗標的預設值加入 `.bigqueryrc`：

* 在沒有標頭的檔案頂端加入[通用旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#global_flags)。
* 如要加入指令專屬旗標，請 (用中括弧) 輸入指令名稱，然後在指令名稱後方逐一加入指令專屬旗標 (每行一個)。

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

* 將全域旗標 `--apilog` 設為 `stdout`，在Google Cloud 主控台中列印偵錯輸出內容。
* 將全域旗標 `--format` 設為 `prettyjson`，以使用者可理解的 JSON 格式顯示指令輸出內容。
* 全域標記 `--location` 設為 `US` 多地區位置。
* `query` 指令專屬旗標 `--use_legacy_sql` 設為 `false`，以 GoogleSQL 做為預設查詢語法。

  **附註：**您不能在 `.bigqueryrc` 中使用 `--nouse_legacy_sql`。
* 將 `query` 指令專屬旗標 `--max_rows` 設為 `100`，控制查詢輸出的資料列數。
* 將 `query` 指令專屬旗標 `--maximum_bytes_billed` 設為 10,000,000 個位元組 (10 MB)，讓讀取資料量超過 10 MB 的查詢失敗。
* `load` 指令專屬旗標 [`--destination_kms_key`](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) 會設為 `projects/myproject/locations/mylocation/keyRings/myRing/cryptoKeys/myKey`。

## CLI 說明

如需 bq 指令列工具的相關說明，請執行下列指令：

| 說明 | help 指令格式 | 範例 |
| --- | --- | --- |
| 已安裝的版本 | `bq version` | `bq version` |
| 所有指令的清單和範例 | `bq help` | `bq help` |
| 通用旗標說明 | `bq --help` | `bq --help` |
| 特定指令的說明 | `bq help COMMAND` | `bq help mk` |

## 排解 CLI 指令問題

如要記錄傳送及接收的要求，請按照下列步驟操作：
:   加入 `--apilog=PATH_TO_FILE` 旗標可將執行紀錄儲存至本機檔案。將 `PATH_TO_FILE` 替換為要儲存記錄檔的位置。bq 指令列工具的運作方式為執行符合 REST 樣式的標準 API 呼叫，以方便您在進行疑難排解時查看。向 Cloud Customer Care 回報問題時，附上這份記錄也會有所幫助。
:   使用 `-` 或 `stdout` 取代路徑時，系統會在 Google Cloud 控制台中列印記錄。
    將 `--apilog` 設為 `stderr` 則可輸出標準錯誤檔案。如要記錄更多要求，請使用 `--httplib2_debuglevel=LOG_LEVEL` 旗標。`LOG_LEVEL` 記錄的 HTTP 要求資訊越多。

如要排解錯誤，請按照下列步驟操作：
:   要取得[工作狀態](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)或查看像是資料表和資料集等資源的詳細資訊時，請加入 `--format=prettyjson` 旗標。使用這個旗標會輸出 JSON 格式的回應，包括 `reason` 屬性。您可以使用 `reason` 屬性來查詢[錯誤訊息](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw)。
:   如要進一步瞭解執行指令時發生的錯誤，請使用 `--debug_mode` 旗標。

## 通用標記

您可以在任何 `bq` 指令中使用下列旗標 (如適用)：

**`--api=ENDPOINT`**
:   指定要呼叫的 API 端點。預設值為 `https://www.googleapis.com`。

**`--api_version=VERSION`**
:   指定要使用的 API 版本。預設值為 `v2`。

**`--apilog=FILE`**
:   將所有 API 要求和回應記錄於 `FILE` 所指定的檔案。可能的值如下：

    * 檔案路徑 - 將記錄檔寫入指定檔案
    * `stdout` - 將記錄輸出至標準輸出內容
    * `stderr` - 記錄到標準錯誤
    * `false` - 不會記錄 API 要求和回應 (預設)

**`--use_google_auth={true|false}`**
:   如果設為 `true`，則會啟用使用 Google Auth 程式庫的驗證機制。預設值為 `true`。

**`--bigqueryrc=PATH`**
:   指定 bq 指令列工具設定檔的路徑。如果未指定 `--bigqueryrc` 標記，指令會使用 `BIGQUERYRC` 環境變數。如未設定環境變數，系統會使用 `$HOME/.bigqueryrc`。
    如果該檔案不存在，則會使用 `~/.bigqueryrc`。詳情請參閱「[設定指令列旗標的預設值](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)」。

**`--ca_certificates_file=PATH`**
:   指定[憑證授權單位服務](https://docs.cloud.google.com/certificate-authority-service?hl=zh-tw) (CA) 檔案的位置。

**`--dataset_id=DATASET_ID`**
:   指定要搭配指令使用的預設資料集。如果不適用的話，系統會忽略這個標記。您可以使用 `PROJECT:DATASET` 或 `DATASET` 格式指定 `DATASET_ID` 引數。如果缺少 `PROJECT` 部分，系統會使用預設專案。如要覆寫預設專案設定，請指定 [`--project_id` 標記](#project_id_flag)。

**`--debug_mode={true|false}`**
:   如果設為 `true`，則會針對 Python 例外狀況顯示回溯資料。預設值為 `false`。

**`--disable_ssl_validation={true|false}`**
:   如果設為 `true`，則會啟用 HTTPS 憑證驗證。預設值為 `false`。

**`--discovery_file=PATH`**
:   指定探索時要讀取的 JSON 檔案。

**`--enable_gdrive={true|false}`**
:   如果設為 `false`，就會要求不含 Google 雲端硬碟範圍的新 OAuth 憑證。預設值為 `true`，會要求具有雲端硬碟範圍的新 OAuth 權杖。如要將這個旗標設為 `false`，並使用使用者帳戶進行驗證，請將 `--use_google_auth` 旗標設為 `false`。

**`--fingerprint_job_id={true|false}`**
:   如要使用來自工作設定指紋的工作 ID，請設為 `true`。此設定可避免系統意外多次執行相同工作。預設值為 `false`。

**`--format=FORMAT`**
:   指定指令輸出內容的格式，請使用下列其中一個值：

    * `pretty`：格式化的資料表輸出內容
    * `sparse`：簡化的資料表輸出內容
    * `prettyjson`：容易理解的 JSON 格式
    * `json`：盡可能壓縮到最小的 JSON
    * `csv`：包含標頭的 csv 格式

    `pretty`、`sparse` 和 `prettyjson` 是使用者能理解的格式。`json` 和 `csv` 適合用來傳送至其他程式。如果指定 `none`，指令就不會產生任何輸出內容。如果缺少 `--format` 旗標，系統就會根據指令選擇適當的輸出格式。

**`--headless={true|false}`**
:   如要在沒有使用者互動的情況下執行 `bq` 工作階段，請設為 `true`。舉例來說，`debug_mode` 不會觸發偵錯工具，列印資訊的頻率也會降低。預設值為 `false`。

**`--httplib2_debuglevel=DEBUG_LEVEL`**
:   指定是否要顯示 HTTP 偵錯資訊。如果 `DEBUG_LEVEL` 大於 `0`，除了錯誤訊息外，指令還會將 HTTP 伺服器要求和回應記錄到 stderr。如果 `DEBUG_LEVEL` 不大於 0，或未使用 `--httplib2_debuglevel` 旗標，則只會提供錯誤訊息。

    例如：

    ```
    --httplib2_debuglevel=1
    ```

    **注意：** 這項旗標不支援多層級偵錯，因此您可以將 `DEBUG_LEVEL` 設為任何正數。

**`--job_id=JOB_ID`**
:   指定新職缺的職缺 ID。
    這個旗標僅適用於建立工作的指令：`cp`、`extract`、`load` 和 `query`。如果沒有使用 `--job_id` 標記，指令會產生專屬的工作 ID。詳情請參閱[透過程式執行工作](https://docs.cloud.google.com/bigquery/docs/running-jobs?hl=zh-tw)。

**`--job_property=KEY:VALUE`**
:   要在工作設定的屬性欄位中加入的鍵/值組合。重複使用這個旗標即可指定其他屬性。

**`--location=LOCATION`**
:   對應於區域或多區域[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)的字串。當您使用 `--jobs` 旗標顯示工作相關資訊時，[`bq cancel`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cancel) 和 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令都需要位置旗標。對於下列指令，位置標記是選用的：

    * [`query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query)
    * [`cp`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp)
    * [`load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load)
    * [`extract`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_extract)
    * [`partition`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_partition)
    * [`update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)
    * [`wait`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_wait)
    * 使用 `--dataset`、`--reservation`、`--capacity_commitment` 或 `--reservation_assignment` 旗標時，請使用 [`mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)
    * 使用 `--reservation`、`--capacity_commitment` 或 `--reservation_assignment` 旗標時，請使用 [`ls`](#bq_ls)

    所有其他指令都會忽略 `--location` 旗標。

    **附註：**`--location` 旗標是在 bq 版本 2.0.29 中推出。如要確認 bq 指令列工具的版本，請輸入 `bq version`

**`--max_rows_per_request=MAX_ROWS`**
:   一個整數，用來指定每次讀取所傳回的資料列數量上限。

**`--project_id=PROJECT`**
:   指定用於指令的專案。

**`--proxy_address=PROXY`**
:   指定用來連線至 Google Cloud的 Proxy 主機名稱或 IP 位址。

**`--proxy_password=PASSWORD`**
:   指定透過 Proxy 主機進行驗證時使用的密碼。

**`--proxy_port=PORT`**
:   指定用來連線至 Proxy 主機的通訊埠編號。

**`--proxy_username=USERNAME`**
:   指定透過 Proxy 主機進行驗證時使用的使用者名稱。

**`--quiet={true|false}` 或 `-q={true|false}`**
:   如要在執行工作時停止更新狀態，請設為 `true`。預設值為 `false`。

**`--synchronous_mode={true|false}` 或 `-sync={true|false}`**
:   如要建立工作並立即傳回，且以成功完成的狀態做為錯誤代碼，請設為 `false`。如果設為 `true`，指令就會等候工作完成再傳回結果，並傳回工作完成狀態做為錯誤代碼。預設值為 `true`。

**`--trace=token:TOKEN`**
:   指定要加入 API 要求的追蹤權杖。

**`--use_regional_endpoints={true|false}`**
:   [預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。如要連線至區域端點，請將 `--use_regional_endpoints` 旗標設為 `true`，並將 [`--location`](#location_flag) 旗標設為要連線的區域。預設值為 `false`。

## 已淘汰的通用旗標

下列通用標記用於從檔案指定 bq 指令列工具標記，但已淘汰。如要從檔案指定標記，請使用 [`--bigqueryrc`](#bigqueryrc_flag) 標記。

**`--flagfile=PATH`**

如有指定此旗標時，則會在 bq 指令列工具中插入所提供檔案的旗標定義。預設值為 `''`。詳情請參閱「[設定指令列旗標的預設值](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)」。

## 指令

以下各節說明 bq 指令列工具的指令，以及指令專屬的標記和引數。

### `bq add-iam-policy-binding`

使用 `bq add-iam-policy-binding` 指令擷取資料表或檢視區塊的[身分與存取權管理 (IAM) 政策](https://docs.cloud.google.com/iam/docs/reference/rest/v1/Policy?hl=zh-tw#binding)，並在政策中新增繫結，一次完成所有步驟。

這個指令可取代下列三步驟程序：

1. 使用 [`bq get-iam-policy`](#bq_get-iam-policy) 指令擷取政策檔案 (JSON 格式)。
2. 編輯政策檔案。
3. 使用 [`bq set-iam-policy`](#bq_set-iam-policy) 指令，以新的繫結更新政策。

**注意：** `bq add-iam-policy-binding` 不支援資料集。如要修改資料集存取權，請參閱「[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)」。

#### 劇情概要

```
bq add-iam-policy-binding [FLAGS] --member=MEMBER_TYPE:MEMBER --role=ROLE
  [--table] RESOURCE
```

#### 範例

```
bq add-iam-policy-binding --member=user:myAccount@gmail.com \
  --role=roles/bigquery.dataViewer myDataset.myTable
```

#### 旗標和引數

`bq add-iam-policy-binding` 指令可使用下列旗標和引數：

**`--member=MEMBER_TYPE:MEMBER`**
:   這是必要旗標，使用 `--member` 旗標指定身分與存取權管理政策繫結的成員。`--member` 旗標必須搭配 `--role` 旗標。一組 `--member` 和 `--role` 旗標等於一個繫結。

    `MEMBER_TYPE` 值會指定 IAM 政策繫結中的成員類型。請使用下列其中一個值：

    * `user`
    * `serviceAccount`
    * `group`
    * `domain`

    `MEMBER` 值會指定 IAM 政策繫結中成員的電子郵件地址或網域。

**`--role=ROLE`**
:   這是必要旗標，指定 IAM 政策繫結中的角色部分。`--role` 旗標必須搭配 `--member` 旗標。一組 `--member` 和 `--role` 標記等於一個繫結。

**`--table={true|false}`**
:   如果 `RESOURCE` 引數不是資料表或檢視區塊 ID，請將 `--table` 旗標設為 `true`，系統就會傳回錯誤。預設值為 `false`。為確保與其他指令一致，這個標記也適用於這個指令。

**`RESOURCE`**
:   要新增政策的資料表或檢視區塊。

詳情請參閱 [IAM 政策參考資料](https://docs.cloud.google.com/iam/docs/reference/rest/v1/Policy?hl=zh-tw#binding)。

### `bq cancel`

使用 `bq cancel` 指令取消 BigQuery 工作。

#### 劇情概要

```
bq [--synchronous_mode=false] cancel JOB_ID
```

#### 範例

```
bq cancel bqjob_12345
```

```
bq --synchronous_mode=false cancel bqjob_12345
```

#### 旗標和引數

`bq cancel` 指令會使用下列旗標和引數：

**`--synchronous_mode=false`**
:   如不想等待 `bq cancel` 指令完成，請將全域 [`--synchronous_mode`](#sync_flag) 標記設為 `false`。預設值為 `true`。

**`JOB_ID`**
:   要取消的工作。

如要進一步瞭解如何使用 `bq cancel` 指令，請參閱[管理工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)一文。

### `bq cp`

使用 `bq cp` 指令執行下列工作：

* 建立[資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)、[資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)或[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)的副本。
* 建立資料表副本。
* 建立資料表快照。

#### 劇情概要

```
bq cp [FLAGS] SOURCE_TABLE DESTINATION_TABLE
```

#### 範例

```
bq cp myDataset.myTable myDataset.myTableCopy
```

#### 旗標和引數

`bq cp` 指令會使用下列旗標和引數：

**`--append_table={true|false}` 或 `-a={true|false}`**
:   如要將資料表附加到現有資料表，請設為 `true`。
    預設值為 `false`。

    無法同時使用旗標設定 `--append_table=true` 和 `--clone=true`。

**`--clone={true|false}`**
:   如要建立[資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)，請將值設為 `true`。基礎資料表可以是標準資料表、資料表副本或資料表快照。目的地資料表是資料表副本。預設值為 `false`；如果未指定 `--clone=true` 或 `--snapshot=true`，則目的地資料表與基本資料表是相同類型的資料表。需要 `--no_clobber` 旗標。

    無法同時使用旗標設定 `--append_table=true` 和 `--clone=true`。

**`--destination_kms_key=KEY`**
:   指定用來加密目的地資料表資料的 Cloud KMS [金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)。

    例如：

    ```
    --destination_kms_key=projects/myProject/locations/global/keyRings/myKeyRing/cryptoKeys/myKey
    ```

**`--expiration=SECONDS`**
:   資料表快照失效前的秒數。如果未納入，資料表快照到期時間會設為包含新資料表快照的資料集預設到期時間。搭配 `--snapshot` 旗標使用。

**`--force={true|false}` 或 `-f={true|false}`**
:   如要在無提示的情況下覆寫現有的目的地資料表，請將此屬性設為 `true`。預設值為 `false`；如果目的地資料表已存在，指令會先提示確認，再覆寫資料。

**`--no_clobber={true|false}` 或 `-n={true|false}`**
:   如要禁止覆寫現有的目的地資料表，請設為 `true`。預設值為 `false`；如果目的地資料表已存在，系統會覆寫該資料表。

**`--restore={true|false}`**
:   這個標記即將淘汰。如要從資料表快照建立可寫入的資料表，請使用 `bq cp` 指令或 `bq cp --clone` 指令。

**`--snapshot={true|false}`**
:   如要為 `SOURCE_TABLE` 引數中指定的資料表建立[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)，請將 `true` 設為 `true`。基礎資料表可以是標準資料表、資料表副本或其他資料表快照。預設值為 `false`；如果未指定 `--clone=true` 和 `--snapshot=true`，則目的地資料表會與基本資料表類型相同。需要 `--no_clobber` 旗標。

**`SOURCE_TABLE`**
:   要複製的表格。

**`DESTINATION_TABLE`**
:   要複製到的資料表。

如要進一步瞭解如何使用 `cp` 指令，請參閱下列內容：

* [複製表格](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)
* [建立資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-create?hl=zh-tw)
* [建立資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-create?hl=zh-tw)
* [還原資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-restore?hl=zh-tw)

### `bq extract`

使用 `bq extract` 指令將資料表資料匯出至 Cloud Storage。

#### 劇情概要

```
bq extract [FLAGS] RESOURCE DESTINATION
```

#### 範例

```
bq extract --compression=GZIP --destination_format=CSV --field_delimiter=tab \
    --print_header=false myDataset.myTable gs://my-bucket/myFile.csv.gzip
```

```
bq extract --destination_format=CSV --field_delimiter='|' myDataset.myTable \
  gs://myBucket/myFile.csv
```

#### 旗標和引數

`bq extract` 指令會使用下列旗標和引數：

**`--compression=COMPRESSION_TYPE`**
:   指定匯出檔案所採用的壓縮類型。可能的值如下：

    * `GZIP`
    * `DEFLATE`
    * `SNAPPY`
    * `NONE`

    預設值為 `NONE`。

    如要瞭解各壓縮類型支援的格式，請參閱「[匯出格式與壓縮類型](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw#export_formats_and_compression_types)」。

**`--destination_format=FORMAT`**
:   指定匯出資料的格式。可能的值如下：

    * `CSV`
    * `NEWLINE_DELIMITED_JSON`
    * `AVRO`
    * `PARQUET`

    預設值為 `CSV`。

**`--field_delimiter=DELIMITER`**
:   針對 CSV 匯出內容，指定輸出檔案中用來標示資料欄間界線的字元。分隔符號可以是任何 ISO-8859-1 單一位元組字元。您可以使用 `\t` 或 `tab` 指定分頁符。

**`--print_header={true|false}`**
:   如要禁止系統列印格式有標頭的標頭列，請設為 `false`。預設值為 `true`，且會納入標頭列。

**`RESOURCE`**
:   您要匯出的資料表。

**`DESTINATION`**
:   接收匯出資料的儲存位置。

如要進一步瞭解如何使用 `bq extract` 指令，請參閱[匯出資料表資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)一文。

### `bq get-iam-policy`

使用 `bq get-iam-policy` 指令擷取資源的 [IAM 政策](https://docs.cloud.google.com/iam/docs/reference/rest/v1/Policy?hl=zh-tw#binding)，並列印至 `stdout`。資源可以是資料表、檢視區塊或[配額預留](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_reservations)。政策採用 JSON 格式。

**注意：** `bq get-iam-policy` 不支援資料集。如要取得資料集的 IAM 政策，請參閱「[查看資料集的存取權政策](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#view_the_access_policy_of_a_dataset)」。

#### 劇情概要

```
bq get-iam-policy [FLAGS] RESOURCE
```

#### 範例

```
bq get-iam-policy myDataset.myTable
```

```
bq get-iam-policy --reservation myReservation
```

#### 旗標和引數

`bq get-iam-policy` 指令會使用下列旗標和引數：

**`--table={true|false}` 或 `--t={true|false}`**
:   如要讓系統在 `RESOURCE` 不是資料表或檢視區塊 ID 時傳回錯誤，請將 `--table` 旗標設為 `true`。預設值為 `false`。為確保與其他指令一致，這個標記會受到支援。

**`--reservation={true|false}`**
:   如要取得預訂的身分與存取權管理政策，請設為 `true`
    ([預覽](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))。預設值為 `false`。使用這個旗標時，`RESOURCE` 會視為預訂 ID。預留項目可選擇性加上專案和位置前置字元：`myProject:myLocation.myReservation`。

**`RESOURCE`**
:   要取得政策的資料表或檢視區塊。

如要進一步瞭解 `bq get-iam-policy` 指令，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#bq)」。

### `bq head`

使用 `bq head` 指令顯示資料表的指定資料列和資料欄。根據預設，系統會顯示前 100 列的所有資料欄。

#### 劇情概要

```
bq head [FLAGS] [TABLE]
```

#### 範例

```
bq head --max_rows=10 --start_row=50 --selected_fields=field1,field3 \
  myDataset.myTable
```

#### 旗標和引數

`bq head` 指令會使用下列旗標和引數：

**`--job=JOB or -j=JOB`**
:   如要讀取查詢工作的結果，請使用有效工作 ID 指定這個旗標。

**`--max_rows=MAX or -n=MAX`**
:   一個整數，用來指定顯示資料表資料時要列印的資料列數量上限。預設值為 `100`。

**`--selected_fields=COLUMN_NAMES or -c=COLUMN_NAMES`**
:   以半形逗號分隔的清單，用來指定顯示資料表資料時要傳回的欄位 (包括巢狀和重複欄位) 子集。如未指定此旗標，系統會傳回所有資料欄。

**`--start_row=START_ROW or -s=START_ROW`**
:   一個整數，用來指定顯示資料表資料前要略過的資料列數量。預設值為 `0`，資料表資料會從第一列開始。

**`--table={true|false}` 或 `-t={true|false}`**
:   如果指令引數不是表格或檢視區塊，請設為 `true` 以傳回錯誤。預設值為 `false`。為確保與其他指令一致，這個標記會受到支援。

**`TABLE`**
:   要擷取資料的資料表。

如要進一步瞭解如何使用 `bq head` 指令，請參閱[管理資料表資料](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw)一文。

### `bq help`

使用 `bq help` 指令在工具中顯示 bq 指令列工具說明文件。

#### 劇情概要

`bq help [COMMAND]`

#### 旗標和引數