Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 安排查詢

BigQuery 排定查詢可讓您自動執行週期性 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 工作負載，包括[資料定義語言 (DDL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw) 和[data manipulation language (DML)](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw) 陳述式。如要依日期和時間整理結果，您可以將查詢字串和目的地資料表參數化。建立或更新排程時，BigQuery 會將排定時間從當地時間轉換為世界標準時間，不受日光節約時間影響。

## 事前準備

* 排定的查詢會使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)的功能。確認您已完成「[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)」中的所有必要動作。
* 授予 Identity and Access Management (IAM) 角色，讓使用者具備執行本文件中各項工作所需的權限。
* 如果您打算指定客戶自行管理的加密金鑰 (CMEK)，請確認[服務帳戶具備加密和解密權限](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#grant_permission)，且您擁有使用 CMEK 所需的 [Cloud KMS 金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱「[指定排定查詢的加密金鑰](#CMEK)」。

## 限制

* 如果排定的查詢在整點 (例如 09:00) 執行，可能會觸發多次，導致非預期的結果，例如 `INSERT` 作業造成資料重複。為避免這類非預期結果，請使用非整點的時間表 (例如 08:58 或 09:03)。

### 所需權限

如要排定查詢，您必須具備下列 IAM 權限：

* 如要建立移轉作業，您必須具備 `bigquery.transfers.update` 和 `bigquery.datasets.get` 權限，或 `bigquery.jobs.create`、`bigquery.transfers.get` 和 `bigquery.datasets.get` 權限。

  **注意：** 如果您使用 Google Cloud 控制台或 bq 指令列工具排定查詢，則必須具備 `bigquery.transfers.get` 權限。
* 如要執行排定的查詢，您必須具備下列權限：

  + 目標資料集的 `bigquery.datasets.get` 權限。
  + 專案的 `bigquery.jobs.create` 權限。

如要修改或刪除排定的查詢，您必須具備下列其中一項權限：

* 專案的 `bigquery.transfers.update` 和 `bigquery.transfers.get` 權限。
* 如要使用使用者憑證執行排定的查詢，該使用者必須擁有排定的查詢，且您必須具備專案的 `bigquery.jobs.create` 權限。
* 如果您以服務帳戶的身分執行排定的查詢，呼叫排定查詢的使用者必須具備專案的 `bigquery.transfers.update` 和 `bigquery.transfers.get` 權限。授予 [IAM 服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`iam.serviceAccountUser`) 角色後，使用者就能以服務帳戶的身分執行工作，但不會獲得排程查詢設定的管理權限。

預先定義的 [BigQuery 管理員 (`roles/bigquery.admin`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin) IAM 角色包含排定或修改查詢所需的權限。

如要進一步瞭解 BigQuery 的 IAM 角色，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要建立或更新由服務帳戶執行的排定查詢，您必須具備該服務帳戶的存取權。如要進一步瞭解如何將服務帳戶角色授予使用者，請參閱「[服務帳戶使用者角色](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#user-role)」。如要在Google Cloud 控制台的排定查詢 UI 中選取服務帳戶，您必須具備下列 IAM 權限：

* `iam.serviceAccounts.list`：列出服務帳戶。
* `iam.serviceAccountUser`，將服務帳戶指派給排定的查詢。

**注意：** 如果您使用的是 bq 指令列工具，請使用 `--service_account_name` 旗標，而非以服務帳戶身分進行驗證。

## 設定選項

以下各節將說明設定選項。

### 查詢字串

查詢字串必須有效，且以 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 撰寫。每次執行排定的查詢時，都可以接收下列[查詢參數](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw#parameterized-timestamps)。

如要在排定查詢前，手動測試含有 `@run_time` 和 `@run_date` 參數的查詢字串，請使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw)。

#### 可用的參數

| 參數 | GoogleSQL 類型 | 值 |
| --- | --- | --- |
| `@run_time` | [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type) | 以世界標準時間表示。對於具有定期執行排程的查詢，`run_time` 用以表示預定的執行時間。舉例來說，如果排定的查詢設為「每 24 小時」，則兩次連續查詢之間的 `run_time` 差異正好是 24 小時，即使實際執行時間可能略有不同。 |
| `@run_date` | [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type) | 代表邏輯日曆日期。 |

#### 範例

在以下範例中，系統會查詢名為 [`hacker_news.stories`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=hacker_news&%3Bpage=dataset&hl=zh-tw) 的公開資料集，而 `@run_time` 參數是該查詢字串的一部分。

```
SELECT @run_time AS time,
  title,
  author,
  text
FROM `bigquery-public-data.hacker_news.stories`
LIMIT
  1000
```

### 目標資料表

設定排定查詢時，如果結果的目的地資料表不存在，BigQuery 會嘗試為您建立資料表。

如果您使用的是 DDL 或 DML 查詢，請在 Google Cloud 控制台中選擇「Processing location」(處理位置) 或區域。建立目的地資料表的 DDL 或 DML 查詢必須指定處理位置。

如果目的地資料表確實存在，且您使用 `WRITE_APPEND`
[寫入偏好設定](#write_preference)，BigQuery 會將資料附加至目的地資料表，並嘗試對應結構定義。BigQuery 會自動允許新增及重新排序欄位，並容許缺少選用欄位。如果資料表結構定義在兩次執行之間變更過多，導致 BigQuery 無法自動處理變更，排定的查詢就會失敗。

查詢可參照來自不同專案和不同資料集的資料表。設定排程查詢時，資料表名稱不需要包含目的地資料集。目的地資料集會另外指定。

排定查詢的目的地資料集和資料表，必須與排定查詢位於相同專案。

#### 寫入偏好設定

您選取的寫入偏好設定，會決定查詢結果寫入現有目的地資料表的方式。

* `WRITE_TRUNCATE`：如果資料表存在，BigQuery 會覆寫資料表資料。
* `WRITE_APPEND`：如果資料表存在，BigQuery 會將資料附加至資料表。

如果使用 DDL 或 DML 查詢，就無法使用寫入偏好設定選項。

唯有 BigQuery 成功完成查詢，才能建立、截斷或附加目的地資料表。建立、截斷或附加的動作是在工作完成時，以一次完整更新的形式進行。

#### 分群

如果資料表是使用 DDL 陳述式 `CREATE TABLE AS SELECT` 建立，排程查詢只能在新資料表上建立叢集。請參閱「[使用資料定義語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)」頁面的「[依據查詢結果建立分群資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_clustered_table_from_the_result_of_a_query)」一節。

#### 分區選項

排程查詢可建立分區或非分區的目的地資料表。您可以在 Google Cloud 控制台、bq 指令列工具和 API 設定方法中使用分區功能。如果您使用 DDL 或 DML 查詢搭配分區，請將「Destination table partitioning」(目的地資料表分區) 欄位留空。

您可以在 BigQuery 中使用下列類型的資料表分區：

* [整數範圍分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#integer_range)：根據特定 `INTEGER` 資料欄中的值範圍，將資料表分區。
* [時間單位資料欄分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)：根據 [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type)、[`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type) 或 [`DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#datetime_type) 資料欄分區的資料表。
* [擷取時間分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#ingestion_time)：依擷取時間分區的資料表。BigQuery 會根據擷取資料的時間，自動將資料列指派至分區。

如要在Google Cloud 控制台中使用排定查詢建立分區資料表，請使用下列選項：

* 如要使用整數範圍分區，請將「Destination table partitioning field」(目的地資料表分區欄位) 留空。
* 如要使用時間單位資料欄分區，請在[設定排定的查詢](#set_up_scheduled_queries)時，在「Destination table partitioning」(目的地資料表分區) 欄位中指定資料欄名稱。
* 如要使用擷取時間分區，請將「Destination table partitioning field」(目的地資料表分區欄位) 留空，並在目的地資料表的名稱中指明日期分區。例如：`mytable${run_date}`。詳情請參閱「[參數範本語法](#param-templating-syntax)」。

#### 可用的參數

設定排定的查詢時，可使用執行階段參數，指定要以何種方式對目的地資料表進行分區。

| 參數 | 範本類型 | 值 |
| --- | --- | --- |
| `run_time` | 格式化的時間戳記 | 採用世界標準時間，依排程而定。對於具有定期執行排程的查詢，`run_time` 用以表示預定的執行時間。舉例來說，如果排定的查詢設為「每 24 小時」，則兩次連續查詢之間的`run_time`差異正好是 24 小時，即使實際執行時間可能略有不同。  請參閱「[`TransferRun.runTime`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs.runs?hl=zh-tw)」。 |
| `run_date` | 日期字串 | `run_time` 參數的日期，採用以下格式：`%Y-%m-%d`；例如 `2018-01-01`。這個格式與擷取時間分區資料表相容。 |

#### 範本系統

可使用範本語法讓排定的查詢支援目的地資料表名稱中的執行階段參數。

#### 參數範本語法

範本語法支援基本字串範本和時間偏移。參數會以下列格式參照：

* `{run_date}`
* `{run_time[+\-offset]|"time_format"}`

| **參數** | **Purpose** |
| --- | --- |
| `run_date` | 這個參數會由格式為 `YYYYMMDD` 的日期取代。 |
| `run_time` | 這個參數支援下列屬性： `offset`  時間偏移，依序以小時 (h)、分鐘 (m) 和秒 (s) 表示。  不支援天 (d)。 可使用小數，例如：`1.5h`。  `time_format` 格式設定字串。最常見的格式參數是年 (%Y)、月 (%m)、日 (%d)。 就分區資料表而言，YYYYMMDD 是必要的後置字串，相當於「%Y%m%d」。  進一步瞭解 [datetime 元素的格式設定](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators?hl=zh-tw#supported-format-elements-for-datetime)。 |

**使用須知：**

* run\_time、offset 和 time\_format 之間不得有空格字元。
* 如果字串要包含大括號，可以按以下方式加以逸出：`'\{' and '\}'`。
* 如果 time\_format 要包含引號或分隔號，例如 `"YYYY|MM|DD"`，可以在格式字串按以下方式加以逸出：`'\"'` 或 `'\|'`。

#### 參數範本範例

以下範例說明如何以不同的時間格式指定目的地資料表名稱，以及如何設定執行時間時區。

| **run\_time (UTC)** | **範本化參數** | **輸出目的地資料表名稱** |
| --- | --- | --- |
| 2018-02-15 00:01:00 | `mytable` | `mytable` |
| 2018-02-15 00:01:00 | `mytable_{run_time|"%Y%m%d"}` | `mytable_20180215` |
| 2018-02-15 00:01:00 | `mytable_{run_time+25h|"%Y%m%d"}` | `mytable_20180216` |
| 2018-02-15 00:01:00 | `mytable_{run_time-1h|"%Y%m%d"}` | `mytable_20180214` |
| 2018-02-15 00:01:00 | `mytable_{run_time+1.5h|"%Y%m%d%H"}` 或 `mytable_{run_time+90m|"%Y%m%d%H"}` | `mytable_2018021501` |
| 2018-02-15 00:01:00 | `{run_time+97s|"%Y%m%d"}_mytable_{run_time+97s|"%H%M%S"}` | `20180215_mytable_000237` |

**注意：**使用日期或時間參數建立資料表時，如果資料表名稱結尾為日期格式 (例如 `YYYYMMDD`)，BigQuery 會[將這些資料表分組](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)。在 Google Cloud 控制台中，這些分組資料表可能會顯示為`mytable_(1)`等名稱，代表資料分割資料表的集合。

### 使用服務帳戶

您可以設定排定的查詢，以服務帳戶的身分進行驗證。服務帳戶是與 Google Cloud 專案相關聯的特殊帳戶。服務帳戶可以使用自己的服務憑證 (而非使用者的憑證) 執行工作，例如排定的查詢或批次處理管道。

如要進一步瞭解如何透過服務帳戶進行驗證，請參閱[驗證功能簡介](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#sa-impersonation)一文。

* 您可以使用服務帳戶[設定排定的查詢](#set_up_scheduled_queries)。如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立移轉作業。
* 您可以使用 bq 指令列工具或 Google Cloud 控制台，以服務帳戶的憑證更新現有的排定查詢。詳情請參閱「[更新排定查詢憑證](#update_scheduled_query_credentials)」。

### 使用排定的查詢指定加密金鑰

您可以指定[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/kms/docs/cmek?hl=zh-tw)，為移轉作業執行作業加密資料。您可以使用 CMEK 支援[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)的移轉作業。

指定移轉作業的 CMEK 時，BigQuery 資料移轉服務會將 CMEK 套用至任何擷取資料的中繼磁碟快取，確保整個資料移轉工作流程符合 CMEK 規範。

如果現有移轉作業原本並非使用 CMEK 建立，則無法更新現有移轉作業來新增 CMEK。舉例來說，您無法將原本預設加密的目的地資料表，變更為使用 CMEK 加密。反之，您也無法將 CMEK 加密的目的地資料表變更為其他加密類型。

如果移轉設定最初是以 CMEK 加密建立，則可更新移轉作業的 CMEK。更新移轉設定的 CMEK 時，BigQuery 資料移轉服務會在下次執行移轉作業時，將 CMEK 傳播至目的地資料表，並在移轉作業執行期間，以新的 CMEK 取代任何過時的 CMEK。詳情請參閱「[更新移轉作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#update_a_transfer)」。

您也可以使用[專案預設金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#project_default_key)。指定移轉作業的專案預設金鑰時，BigQuery 資料移轉服務會將專案預設金鑰，設為任何新移轉設定的預設金鑰。

## 設定排定的查詢

**提示：** 您也可以使用[「Pipelines & Connections」(管道與連線) 頁面](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw)設定排定的查詢。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要排定查詢，請選取下列任一選項。如需排程語法的說明，請參閱「[設定排程格式](https://docs.cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml?hl=zh-tw#formatting_the_schedule)」。如要進一步瞭解排程語法，請參閱「[資源：`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig)」。或者，您也可以[使用 Gemini Cloud Assist 安排查詢](https://docs.cloud.google.com/bigquery/docs/use-cloud-assist?hl=zh-tw#schedule_a_query)，只要在提示中提供排程詳細資料即可。

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 執行您有興趣的查詢。如果對結果滿意，請依序點選「File」(檔案) >「Schedule」(排程)。
3. 排程查詢的選項會在「New scheduled query」(新增排程查詢) 窗格中開啟。
4. 請在「New scheduled query」(新增排程查詢) 窗格中進行以下操作：

   * 針對「Name for the scheduled query」(已排定查詢的名稱)，請輸入名稱，例如 `My scheduled query`。排定查詢名稱可以是任何值，只要日後需要修改查詢時能輕鬆識別即可。
   * 選用：根據預設，查詢會排定為「每日」執行。如要變更預設排程，請從「Repeats」(重複) 下拉式選單中選取所需選項：

     + 如要指定自訂頻率，請選取「Custom」(自訂)，然後在「Custom schedule」(自訂排程) 欄位中輸入類似 Cron 的時間規格，例如 `every mon 23:30`、`every 6 hours` 或 `every hour on mon,tue,wed,thu,fri`。如要進一步瞭解有效排程 (包括自訂間隔)，請參閱「[資源：`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig)」下的 `schedule` 欄位。

       **注意：** 排定的查詢之間至少須間隔 5 分鐘。
     + 如要變更開始時間，請選取「Start at set time」(在所設時間開始執行) 選項，然後輸入所選的開始日期和時間。

       **注意：** 如果指定的開始時間晚於排程時間，則查詢會在下一個週期首次執行。舉例來說，如果查詢是在 `2022-06-05 23:50` 建立，排程為 `daily 00:00`，開始時間為 `2022-06-06 10:00`，則要到 `2022-06-07 00:00` 才會執行。
     + 如要指定結束時間，請選取「Schedule end time」(排定結束時間) 選項，然後輸入所選的結束日期和時間。
     + 如要儲存查詢但不設定排程，以便日後隨選執行，請在「Repeats」(重複) 選單中選取「On-demand」(隨選)。
5. 如果是 GoogleSQL `SELECT` 查詢，請選取「Set a destination table for query results」(為查詢結果設定目的地資料表) 選項，並提供下列目的地資料集相關資訊。

   * 在「Dataset name」(資料集名稱) 部分選擇適當的目的地資料集。
   * 在「Table name」(資料表名稱) 部分，輸入目的地資料表的名稱。
   * 在「Destination table write preference」(目的地資料表寫入偏好設定) 部分，選擇「Append to table」(附加至資料表) 將資料附加至資料表，或選擇「Overwrite table」(覆寫資料表) 覆寫目的地資料表。
6. 選擇「位置類型」。

   * 如果已啟用查詢結果的目的地資料表，可以選取「Automatic location selection」(自動選取位置)，自動選取目的地資料表所在的位置。
   * 否則，請選擇要查詢的資料所在位置。
7. **進階選項**：

   * 選用：CMEK
     如果您使用[客戶自行管理的加密金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)，可以在「Advanced options」(進階選項) 下方選取「Customer-managed key」(客戶自行管理的金鑰)。畫面隨即會列出可用的 CMEK 供您選擇。如要瞭解客戶自行管理的加密金鑰 (CMEK) 如何與 BigQuery 資料移轉服務搭配運作，請參閱「[指定排定查詢的加密金鑰](#CMEK)」。
   * 以服務帳戶身分驗證
     如果有一或多個服務帳戶與 Google Cloud 專案相關聯，您可以將服務帳戶與排定的查詢建立關聯，而非使用使用者憑證。在「Scheduled query credential」(排定的查詢憑證) 下方，按一下選單即可查看可用的服務帳戶清單。如果您以聯合身分登入，則必須使用服務帳戶。
8. 其他設定：

   * 選用：勾選[「Send email notifications」(傳送電子郵件通知)](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，允許系統在移轉作業執行失敗時傳送電子郵件通知。
   * 選用：在「Pub/Sub topic」(Pub/Sub 主題) 中，輸入 Pub/Sub [主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，例如 `projects/myproject/topics/mytopic`。
9. 按一下 [儲存]。

### bq

使用 bq 指令列工具排定查詢有兩種方式。**方法 2** 則可讓您使用更多選項排定查詢。

**方法 1：**使用 **`bq query`** 指令。

如要建立排定的查詢，請在 `bq query` 指令中加入 `destination_table` (或 `target_dataset`)、`--schedule` 和 `--display_name` 選項。

```
bq query \
--display_name=name \
--destination_table=table \
--schedule=interval
```

更改下列內容：

* `name`：排定查詢的顯示名稱。顯示名稱可以是任何值，只要日後需要修改查詢時能輕鬆識別即可。
* `table`：查詢結果的目的地資料表。
  + 與 DDL 和 DML 查詢搭配使用時，`--target_dataset` 是為查詢結果指定目標資料集的另一種方式。
  + `--destination_table` 或 `--target_dataset` 請擇一使用，不能兩者同時使用。
* `interval`。與 `bq query` 搭配使用時，可將查詢設為週期性排定查詢。必須設定查詢的執行頻率。如要進一步瞭解有效排程 (包括自訂間隔)，請參閱「[資源：`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig)」下的 `schedule` 欄位。範例：
  + `--schedule='every 24 hours'`
  + `--schedule='every 3 hours'`
  + `--schedule='every monday 09:00'`
  + `--schedule='1st sunday of sep,oct,nov 00:00'`

選用標記：

* `--project_id` 是您的專案 ID。如果未指定 `--project_id`，系統會使用預設專案。
* 每次執行排定的查詢後，`--replace` 都會以查詢結果覆寫目的地資料表。所有現有資料都會遭到清除。如果是非分區資料表，結構定義也會一併清除。
* `--append_table` 會將結果附加至目的地資料表。
* 如果是 DDL 和 DML 查詢，您也可以提供 `--location` 旗標，指定要處理的特定區域。如未指定 `--location`，系統會使用最近的 Google Cloud 位置。

如果在排定查詢時未指定 `--replace` 和 `--append\_table`，則不會設定寫入偏好設定。
視查詢而定，後續排定的執行作業可能會發生錯誤。

舉例來說，下列指令會使用查詢 `SELECT 1 from mydataset.test` 建立名為 `My Scheduled Query` 的排定查詢。目的地資料表為資料集 `mydataset` 中的 `mytable`。排程查詢會在預設的專案內建立：

```
    bq query \
    --use_legacy_sql=false \
    --destination_table=mydataset.mytable \
    --display_name='My Scheduled Query' \
    --schedule='every 24 hours' \
    --replace=true \
    'SELECT
      1
    FROM
      mydataset.test'
```

**方法 2：**使用 **`bq mk`** 指令。

排程查詢是一種移轉作業。如要排定查詢，您可以使用 bq 指令列工具建立移轉設定。

查詢必須使用 StandardSQL 方言才能進行排程。

輸入 `bq mk` 指令，並提供下列必要旗標：

* `--transfer_config`
* `--data_source`
* `--target_dataset` (DDL 和 DML 查詢可不填)
* `--display_name`
* `--params`

選用標記：

* `--project_id` 是您的專案 ID。如果未指定 `--project_id`，系統會使用預設專案。
* `--schedule` 是您希望查詢執行的頻率。如未指定 `--schedule`，預設設定為依建立時間計算「every 24 hours」(每 24 小時)。
* 如果是 DDL 和 DML 查詢，您也可以提供 `--location` 旗標，指定要處理的特定區域。如未指定 `--location`，系統會使用最近的 Google Cloud 位置。
* `--service_account_name` 是用於透過服務帳戶 (而非個別使用者帳戶) 來驗證排程查詢。
* 如果您在這項移轉作業使用客戶自行管理的加密金鑰 (CMEK)，`--destination_kms_key` 會指定金鑰的[金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱「[指定排定查詢的加密金鑰](#CMEK)」。

```
bq mk \
--transfer_config \
--target_dataset=dataset \
--display_name=name \
--params='parameters' \
--data_source=data_source
```

更改下列內容：

* `dataset`：移轉設定的目標資料集。
  + DDL 和 DML 查詢可視需要使用這個參數。是其他所有查詢的必要參數。
* `name`：移轉設定的顯示名稱。顯示名稱可以是任何值，方便您日後需要修改查詢時識別。
* `parameters`：包含所建立移轉設定的參數，格式為 JSON。例如：`--params='{"param":"param_value"}'`。
  + 針對排程查詢，您必須提供 `query` 參數。
  + `destination_table_name_template` 參數是目的地資料表的名稱。
    - DDL 和 DML 查詢可視需要使用這個參數。是其他所有查詢的必要參數。
  + 針對 `write_disposition` 參數，您可以選擇 `WRITE_TRUNCATE` 來截斷 (覆寫) 目的地資料表，或選擇 `WRITE_APPEND` 將查詢結果附加到目的地資料表。
    - DDL 和 DML 查詢可選用這個參數。是其他所有查詢的必要參數。
* `data_source`。資料來源：`scheduled_query`。
* 選用：`--service_account_name` 旗標用於透過服務帳戶 (而非個別使用者帳戶) 進行驗證。
* 選用：`--destination_kms_key` 指定 Cloud KMS 金鑰的[金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)，例如 `projects/project_name/locations/us/keyRings/key_ring_name/cryptoKeys/key_name`。

**注意：**如要將結果寫入擷取時間分區資料表，請參閱[目的地資料表](#destination_table)一節的操作說明。如果您建立移轉設定時，將
`destination_table_name_template` 參數設為擷取時間
分區資料表，排定的查詢
就會失敗，並顯示
錯誤訊息`partitioning_field`。**注意：** 您無法使用指令列
工具設定通知。

舉例來說，下列指令會使用查詢 `SELECT 1
from mydataset.test` 建立名為 `My Scheduled Query` 的排定查詢移轉設定。目的地資料表 `mytable` 每次寫入時皆會截斷，而目標資料集為 `mydataset`。排定的查詢會在預設專案中建立，並以服務帳戶身分進行驗證：

```
bq mk \
--transfer_config \
--target_dataset=mydataset \
--display_name='My Scheduled Query' \
--params='{"query":"SELECT 1 from mydataset.test","destination_table_name_template":"mytable","write_disposition":"WRITE_TRUNCATE"}' \
--data_source=scheduled_query \
--service_account_name=abcdef-test-sa@abcdef-test.iam.gserviceaccount.com
```

首次執行指令時，您會收到類似以下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照訊息中的操作說明進行，在指令列中貼上驗證碼。

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.CreateTransferConfigRequest;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ProjectName;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.protobuf.Struct;
import com.google.protobuf.Value;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

// Sample to create a scheduled query
public class CreateScheduledQuery {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    final String datasetId = "MY_DATASET_ID";
    final String query =
        "SELECT CURRENT_TIMESTAMP() as current_time, @run_time as intended_run_time, "
            + "@run_date as intended_run_date, 17 as some_integer";
    Map<String, Value> params = new HashMap<>();
    params.put("query", Value.newBuilder().setStringValue(query).build());
    params.put(
        "destination_table_name_template",
        Value.newBuilder().setStringValue("my_destination_table_{run_date}").build());
    params.put("write_disposition", Value.newBuilder().setStringValue("WRITE_TRUNCATE").build());
    params.put("partitioning_field", Value.newBuilder().build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Scheduled Query Name")
            .setDataSourceId("scheduled_query")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .setSchedule("every 24 hours")
            .build();
    createScheduledQuery(projectId, transferConfig);
  }

  public static void createScheduledQuery(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = dataTransferServiceClient.createTransferConfig(request);
      System.out.println("\nScheduled query created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("\nScheduled query was not created." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery_datatransfer

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

# The project where the query job runs is the same as the project
# containing the destination dataset.
project_id = "your-project-id"
dataset_id = "your_dataset_id"

# This service account will be used to execute the scheduled queries. Omit
# this request parameter to run the query as the user with the credentials
# associated with this client.
service_account_name = "abcdef-test-sa@abcdef-test.iam.gserviceaccount.com"

# Use standard SQL syntax for the query.
query_string = """
SELECT
  CURRENT_TIMESTAMP() as current_time,
  @run_time as intended_run_time,
  @run_date as intended_run_date,
  17 as some_integer
"""

parent = transfer_client.common_project_path(project_id)

transfer_config = bigquery_datatransfer.TransferConfig(
    destination_dataset_id=dataset_id,
    display_name="Your Scheduled Query Name",
    data_source_id="scheduled_query",
    params={
        "query": query_string,
        "destination_table_name_template": "your_table_{run_date}",
        "write_disposition": "WRITE_TRUNCATE",
        "partitioning_field": "",
    },
    schedule="every 24 hours",
)

transfer_config = transfer_client.create_transfer_config(
    bigquery_datatransfer.CreateTransferConfigRequest(
        parent=parent,
        transfer_config=transfer_config,
        service_account_name=service_account_name,
    )
)

print("Created scheduled query '{}'".format(transfer_config.name))
```

## 使用服務帳戶設定排定的查詢

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.CreateTransferConfigRequest;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ProjectName;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.protobuf.Struct;
import com.google.protobuf.Value;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

// Sample to create a scheduled query with service account
public class CreateScheduledQueryWithServiceAccount {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    final String datasetId = "MY_DATASET_ID";
    final String serviceAccount = "MY_SERVICE_ACCOUNT";
    final String query =
        "SELECT CURRENT_TIMESTAMP() as current_time, @run_time as intended_run_time, "
            + "@run_date as intended_run_date, 17 as some_integer";
    Map<String, Value> params = new HashMap<>();
    params.put("query", Value.newBuilder().setStringValue(query).build());
    params.put(
        "destination_table_name_template",
        Value.newBuilder().setStringValue("my_destination_table_{run_date}").build());
    params.put("write_disposition", Value.newBuilder().setStringValue("WRITE_TRUNCATE").build());
    params.put("partitioning_field", Value.newBuilder().build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Scheduled Query Name")
            .setDataSourceId("scheduled_query")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .setSchedule("every 24 hours")
            .build();
    createScheduledQueryWithServiceAccount(projectId, transferConfig, serviceAccount);
  }

  public static void createScheduledQueryWithServiceAccount(
      String projectId, TransferConfig transferConfig, String serviceAccount) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .setServiceAccountName(serviceAccount)
              .build();
      TransferConfig config = dataTransferServiceClient.createTransferConfig(request);
      System.out.println(
          "\nScheduled query with service account created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("\nScheduled query with service account was not created." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery_datatransfer

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

# The project where the query job runs is the same as the project
# containing the destination dataset.
project_id = "your-project-id"
dataset_id = "your_dataset_id"

# This service account will be used to execute the scheduled queries. Omit
# this request parameter to run the query as the user with the credentials
# associated with this client.
service_account_name = "abcdef-test-sa@abcdef-test.iam.gserviceaccount.com"

# Use standard SQL syntax for the query.
query_string = """
SELECT
  CURRENT_TIMESTAMP() as current_time,
  @run_time as intended_run_time,
  @run_date as intended_run_date,
  17 as some_integer
"""

parent = transfer_client.common_project_path(project_id)

transfer_config = bigquery_datatransfer.TransferConfig(
    destination_dataset_id=dataset_id,
    display_name="Your Scheduled Query Name",
    data_source_id="scheduled_query",
    params={
        "query": query_string,
        "destination_table_name_template": "your_table_{run_date}",
        "write_disposition": "WRITE_TRUNCATE",
        "partitioning_field": "",
    },
    schedule="every 24 hours",
)

transfer_config = transfer_client.create_transfer_config(
    bigquery_datatransfer.CreateTransferConfigRequest(
        parent=parent,
        transfer_config=transfer_config,
        service_account_name=service_account_name,
    )
)

print("Created scheduled query '{}'".format(transfer_config.name))
```

## 查看排定查詢狀態

### 控制台

如要查看排定查詢的狀態，請在導覽選單中按一下「Scheduling」(排程)，然後篩選「Scheduled Query」(排定的查詢)。按一下排定的查詢，即可查看詳細資料。

### bq

排程查詢是一種移轉作業。如要顯示排定查詢的詳細資料，可以先使用 bq 指令列工具列出移轉設定。

輸入 `bq ls` 指令並加上移轉旗標 `--transfer_config`。還需加上以下旗標：

* `--transfer_location`

例如：

```
bq ls \
--transfer_config \
--transfer_location=us
```

如要顯示單一排定查詢的詳細資料，請輸入 `bq show`
指令，並提供該
排定查詢或移轉設定的 `transfer_path`。

例如：

```
bq show \
--transfer_config \
projects/862514376110/locations/us/transferConfigs/5dd12f26-0000-262f-bc38-089e0820fe38
```

### API

請使用 [`projects.locations.transferConfigs.list`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/list?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ListTransferConfigsRequest;
import com.google.cloud.bigquery.datatransfer.v1.ProjectName;
import java.io.IOException;

// Sample to get list of transfer config
public class ListTransferConfigs {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    listTransferConfigs(projectId);
  }

  public static void listTransferConfigs(String projectId) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      ListTransferConfigsRequest request =
          ListTransferConfigsRequest.newBuilder().setParent(parent.toString()).build();
      dataTransferServiceClient
          .listTransferConfigs(request)
          .iterateAll()
          .forEach(config -> System.out.print("Success! Config ID :" + config.getName() + "\n"));
    } catch (ApiException ex) {
      System.out.println("Config list not found due to error." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_datatransfer_v1

client = bigquery_datatransfer_v1.DataTransferServiceClient()


def list_transfer_configs(project_id: str, location: str) -> None:
    """Lists transfer configurations in a given project.

    This sample demonstrates how to list all transfer configurations in a project.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the transfer config, for example "us-central1"
    """

    parent = client.common_location_path(project_id, location)

    try:
        for config in client.list_transfer_configs(parent=parent):
            print(f"Name: {config.name}")
            print(f"Display Name: {config.display_name}")
            print(f"Data source: {config.data_source_id}")
            print(f"Destination dataset: {config.destination_dataset_id}")
            if "time_based_schedule" in config.schedule_options_v2:
                print(
                    f"Schedule: {config.schedule_options_v2.time_based_schedule.schedule}"
                )
            else:
                print("Schedule: None")
            print("---")
    except google.api_core.exceptions.NotFound:
        print(
            f"Error: Project '{project_id}' not found or contains no transfer configs."
        )
    except google.api_core.exceptions.PermissionDenied:
        print(
            f"Error: Permission denied for project '{project_id}'. Please ensure you have the correct permissions."
        )
```

## 更新排定的查詢

### 控制台

如要更新排定的查詢，請按照下列步驟操作：

1. 在導覽選單中，按一下「Scheduled queries」(排定的查詢) 或「Scheduling」(排程)。
2. 在排定查詢清單中，按一下要變更的查詢名稱。
3. 在開啟的「Scheduled query details」(排定查詢詳細資料) 頁面中，按一下「Edit」(編輯)。
4. 選用：在查詢編輯器窗格中變更查詢文字。
5. 按一下「Schedule query」(排定查詢)，然後選取「Update scheduled query」(更新排定的查詢)。
6. 選用：變更查詢的其他排程選項。
7. 按一下「Update」。

### bq

排程查詢是一種移轉作業。如要更新排定的查詢，可以使用 bq 指令列工具建立移轉設定。

輸入 `bq update` 指令，並加上必要的 `--transfer_config` 旗標。

選用標記：

* `--project_id` 是您的專案 ID。如果未指定 `--project_id`，系統會使用預設專案。
* `--schedule` 是您希望查詢執行的頻率。如未指定 `--schedule`，預設設定為依建立時間計算「every 24 hours」(每 24 小時)。
* `--service_account_name` 只有在同時設定 `--update_credentials` 時才會生效。詳情請參閱「[更新排定查詢憑證](#update_scheduled_query_credentials)」。
* `--target_dataset` (DDL 和 DML 查詢可選用) 是另一種命名查詢結果目標資料集的方式，可與 DDL 和 DML 查詢搭配使用。
* `--display_name` 是排定查詢的名稱。
* `--params`：以 JSON 格式建立的移轉設定參數。例如：--params='{"param":"param\_value"}'。
* 如果您使用客戶自行管理的加密金鑰 (CMEK) 進行這項移轉作業，`--destination_kms_key` 會指定 Cloud KMS 金鑰的[金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)。如要瞭解客戶自行管理的加密金鑰 (CMEK) 如何與 BigQuery 資料移轉服務搭配運作，請參閱「[指定排定查詢的加密金鑰](#CMEK)」。

```
bq update \
--target_dataset=dataset \
--display_name=name \
--params='parameters'
--transfer_config \
RESOURCE_NAME
```

更改下列內容：

* `dataset`：移轉設定的目標資料集。這個參數對於 DDL 和 DML 查詢為選用。其他所有查詢都必須提供。
* `name`：移轉設定的顯示名稱。顯示名稱可以是任何值，方便您日後需要修改查詢時識別。
* `parameters`：包含所建立移轉設定的參數，格式為 JSON。例如：`--params='{"param":"param_value"}'`。
  + 針對排程查詢，您必須提供 `query` 參數。
  + `destination_table_name_template` 參數是目的地資料表的名稱。DDL 和 DML 查詢可視需要使用這個參數。所有其他查詢都必須提供這項資訊。
  + 針對 `write_disposition` 參數，您可以選擇 `WRITE_TRUNCATE` 來截斷 (覆寫) 目的地資料表，或選擇 `WRITE_APPEND` 將查詢結果附加至目的地資料表。如果是 DDL 和 DML 查詢，則可選擇是否要使用這項參數。所有其他查詢都必須提供這項資訊。
* 選用：`--destination_kms_key` 指定 Cloud KMS 金鑰的[金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)，例如 `projects/project_name/locations/us/keyRings/key_ring_name/cryptoKeys/key_name`。
* `RESOURCE_NAME`：移轉作業的資源名稱 (也稱為移轉設定)。如果不知道移轉作業的資源名稱，請使用 [`bq ls --transfer_config --transfer_location=location`](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#list_transfer_configurations) 找出資源名稱。

**注意：**如要將結果寫入擷取時間分區資料表，請參閱[目的地資料表](#destination_table)一節的操作說明。如果您建立移轉設定時，將 `destination_table_name_template` 參數設為擷取時間分區資料表，排定的查詢就會失敗，並顯示錯誤訊息。**注意：** 您無法使用指令列工具設定通知。`partitioning_field`

舉例來說，下列指令會使用查詢 `SELECT 1
from mydataset.test` 更新名為 `My Scheduled Query` 的排定查詢移轉設定。每次寫入時，目的地資料表 `mytable` 都會遭到截斷，目標資料集為 `mydataset`：

```
bq update \
--target_dataset=mydataset \
--display_name='My Scheduled Query' \
--params='{"query":"SELECT 1 from mydataset.test","destination_table_name_template":"mytable","write_disposition":"WRITE_TRUNCATE"}'
--transfer_config \
projects/myproject/locations/us/transferConfigs/1234a123-1234-1a23-1be9-12ab3c456de7
```

### API

請使用 [`projects.transferConfigs.patch`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.transferConfigs/patch?hl=zh-tw) 方法，並透過 `transferConfig.name` 參數提供移轉作業的資源名稱。如果您不知道轉移作業的資源名稱，請使用 [`bq ls --transfer_config --transfer_location=location`](#viewing_a_scheduled_query) 指令列出所有轉移作業，或呼叫 [`projects.locations.transferConfigs.list`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/list?hl=zh-tw) 方法，並使用 `parent` 參數提供專案 ID。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.cloud.bigquery.datatransfer.v1.UpdateTransferConfigRequest;
import com.google.protobuf.FieldMask;
import com.google.protobuf.util.FieldMaskUtil;
import java.io.IOException;

// Sample to update transfer config.
public class UpdateTransferConfig {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setName(configId)
            .setDisplayName("UPDATED_DISPLAY_NAME")
            .build();
    FieldMask updateMask = FieldMaskUtil.fromString("display_name");
    updateTransferConfig(transferConfig, updateMask);
  }

  public static void updateTransferConfig(TransferConfig transferConfig, FieldMask updateMask)
      throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      UpdateTransferConfigRequest request =
          UpdateTransferConfigRequest.newBuilder()
              .setTransferConfig(transferConfig)
              .setUpdateMask(updateMask)
              .build();
      TransferConfig updateConfig = dataTransferServiceClient.updateTransferConfig(request);
      System.out.println("Transfer config updated successfully :" + updateConfig.getDisplayName());
    } catch (ApiException ex) {
      System.out.print("Transfer config was not updated." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_datatransfer_v1
from google.protobuf import field_mask_pb2


client = bigquery_datatransfer_v1.DataTransferServiceClient()


def update_transfer_config(
    project_id: str,
    location: str,
    transfer_config_id: str,
) -> None:
    """Updates a data transfer configuration.

    This sample shows how to update the display name for a transfer
    configuration.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the transfer config, for example "us-central1"
        transfer_config_id: The transfer configuration ID
    """
    transfer_config_name = client.transfer_config_path(
        project=f"{project_id}/locations/{location}",
        transfer_config=transfer_config_id,
    )

    transfer_config = bigquery_datatransfer_v1.types.TransferConfig(
        name=transfer_config_name,
        display_name="My New Transfer Config display name",
    )
    update_mask = field_mask_pb2.FieldMask(paths=["display_name"])

    try:
        response = client.update_transfer_config(
            transfer_config=transfer_config,
            update_mask=update_mask,
        )

        print(f"Updated transfer config: {r
```