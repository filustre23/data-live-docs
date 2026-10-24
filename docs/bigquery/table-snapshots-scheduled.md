Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用排定的查詢建立資料表快照

本文說明如何使用[服務帳戶](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#using_a_service_account)執行排定的 [DDL 查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)，建立資料表的每月快照。本文件將逐步引導您完成下列範例：

1. 在 `PROJECT` 專案中，建立名為 `snapshot-bot` 的服務帳戶。
2. 授予 `snapshot-bot` 服務帳戶所需權限，以便對 `DATASET` 資料集中的 `TABLE` 資料表建立[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)，並將資料表快照儲存在 `BACKUP` 資料集。
3. 編寫查詢，建立 `TABLE` 資料表的每月快照，並將快照放入 `BACKUP` 資料集。由於無法覆寫現有的資料表快照，因此資料表快照必須具有不重複的名稱。為此，查詢會將目前日期附加至資料表快照名稱，例如 `TABLE_20220521`。資料表快照會在 40 天後失效。
4. 排定 `snapshot-bot` 服務帳戶在每月第一天執行查詢。

**注意：** 如要自訂這份文件，在文字和範例中使用您自己的專案、資料集和/或資料表名稱，請編輯下列變數：`PROJECT`、`DATASET`、`BACKUP`、`TABLE`。

本文適用於熟悉 [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw) 和 [BigQuery 資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)的使用者。

## 權限與角色

本節說明建立服務帳戶和排定查詢時，需要哪些 [Identity and Access Management (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，以及哪些[預先定義的 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)可授予這些權限。

### 權限

如要使用服務帳戶，您必須具備下列權限：

| **權限** | **資源** | **資源類型** |
| --- | --- | --- |
| `iam.serviceAccounts.*` | `PROJECT` | 專案 |

如要排定查詢，您必須具備下列權限：

| **權限** | **資源** | **資源類型** |
| --- | --- | --- |
| `bigquery.jobs.create` | `PROJECT` | 專案 |

### 角色

如要使用服務帳戶，您必須具備下列預先定義的角色提供的權限：

| **角色** | **資源** | **資源類型** |
| --- | --- | --- |
| 下列任一項：   `roles/iam.serviceAccountAdmin`  `roles/editor`  `roles/owner` | `PROJECT` | 專案 |

預先定義的 BigQuery 角色可提供排定查詢所需的權限，如下所示：

| **角色** | **資源** | **資源類型** |
| --- | --- | --- |
| 下列任一項：   `roles/bigquery.user`  `roles/bigquery.jobuser`  `roles/bigquery.admin` | `PROJECT` | 專案 |

## 建立 `snapshot-bot` 服務帳戶

請按照下列步驟建立 `snapshot-bot`
[服務帳戶](https://docs.cloud.google.com/iam/docs/service-accounts?hl=zh-tw)，並授予在 `PROJECT` 專案中執行查詢所需的[權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)：

### 控制台

1. 前往 Google Cloud 控制台的「Service accounts」(服務帳戶) 頁面：

   [前往「Service accounts」(服務帳戶)](https://console.cloud.google.com/iam-admin/serviceaccounts?hl=zh-tw)
2. 選取 `PROJECT` 專案。
3. 建立 `snapshot-bot` 服務帳戶：

   1. 按一下「建立服務帳戶」。
   2. 在「Service account name」(服務帳戶名稱) 欄位中，輸入 **snapshot-bot**。
   3. 按一下「建立並繼續」。
4. 為服務帳戶授予執行 BigQuery 工作所需的權限：

   1. 在「Grant this service account access to project」(將專案存取權授予這個服務帳戶) 區段中，選取[「BigQuery User」(BigQuery 使用者)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery) 角色。
   2. 按一下「完成」。

BigQuery 會使用電子郵件地址 `snapshot-bot@PROJECT.iam.gserviceaccount.com` 建立服務帳戶。

如要確認 BigQuery 已建立具備指定權限的服務帳戶，請按照下列步驟操作：

### 控制台

確認 BigQuery 已建立服務帳戶：

1. 前往 Google Cloud 控制台的「Service accounts」(服務帳戶) 頁面：

   [前往「Service Accounts」(服務帳戶)](https://console.cloud.google.com/iam-admin/serviceaccounts?hl=zh-tw)
2. 選取 `PROJECT` 專案。
3. 按一下 **snapshot-bot@PROJECT.iam.gserviceaccount.com**。
4. 確認「Service account status」(服務帳戶狀態) 訊息指出服務帳戶處於有效狀態。

確認 BigQuery 已授予服務帳戶執行查詢所需的權限：

1. 在 Google Cloud 控制台中，前往「Manage resources」(管理資源) 頁面：

   [前往「Manage Resources」(管理資源) 頁面](https://console.cloud.google.com/cloud-resource-manager?hl=zh-tw)
2. 按一下「`PROJECT`」。
3. 按一下「顯示資訊面板」。
4. 在「Permissions」(權限) 分頁中，展開「BigQuery User」(BigQuery 使用者) 節點。
5. 確認 **snapshot-bot** 服務帳戶已列出。

## 將權限授予服務帳戶

本節說明如何授予 `snapshot-bot` 服務帳戶所需權限，以便為 `BACKUP` 資料集中的 `DATASET.TABLE` 資料表建立資料表快照。

### 建立基礎資料表快照的權限

如要授予 `snapshot-bot` 服務帳戶建立 `DATASET.TABLE` 資料表快照所需的權限，請按照下列步驟操作：

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，展開 `PROJECT` 專案節點。
4. 按一下**「資料集」**，然後點選**「DATASET」**資料集。
5. 依序點選**「總覽」>「資料表」**，然後點選「**TABLE**」資料表。
6. 按一下「分享」，「共用」窗格隨即開啟。
7. 點選「新增主體」。「授予存取權」窗格隨即開啟。
8. 在「New principals」(新增主體) 中，輸入服務帳戶的電子郵件地址：**snapshot-bot@PROJECT.iam.gserviceaccount.com**。
9. 從「Select a role」(選取角色) 下拉式選單中，選取[「BigQuery Data Editor」(BigQuery 資料編輯者)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery) 角色。
10. 按一下 [儲存]。
11. 在「Share」(共用) 窗格中，展開「BigQuery Data Editor」(BigQuery 資料編輯者) 節點，確認 **snapshot-bot@PROJECT.iam.gserviceaccount.com** 服務帳戶已列出。
12. 按一下 [關閉]。

### bq

1. 在 Google Cloud 控制台啟用 Cloud Shell：

   [啟用 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)
2. 輸入下列 [`bq add-iam-policy-binding`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_add-iam-policy-binding) 指令：

   ```
   bq add-iam-policy-binding \
   --member=serviceAccount:snapshot-bot@PROJECT.iam.gserviceaccount.com \
   --role=roles/bigquery.dataEditor DATASET.TABLE
   ```

BigQuery 會確認新的政策繫結已新增。

### 在目的地資料集建立資料表的權限

請按照下列步驟，授予 `snapshot-bot` 服務帳戶在 `BACKUP` 資料集建立資料表快照所需的權限：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，展開 `PROJECT` 專案節點。
4. 按一下**「資料集」**，然後點選**「BACKUP」**資料集。
5. 依序點選**「共用」>「管理權限」**。資料集權限窗格隨即開啟。
6. 按一下「Add principal」(新增主體)。在「新增主體」欄位中，輸入服務帳戶的電子郵件地址：**snapshot-bot@PROJECT.iam.gserviceaccount.com**。
7. 在「Select a role」(選取角色) 下拉式選單中，選取「[BigQuery Data Owner](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)」(BigQuery 資料擁有者) 角色。
8. 按一下 [儲存]。
9. 在資料集權限窗格中，確認 **snapshot-bot@PROJECT.iam.gserviceaccount.com** 服務帳戶列在「BigQuery Data Owner」(BigQuery 資料擁有者) 節點下方。
10. 按一下 [關閉]。

您的 `snapshot-bot` 服務帳戶現在具備下列資源的下列 IAM 角色：

| 角色 | 資源 | 資源類型 | 目的 |
| --- | --- | --- | --- |
| BigQuery 資料編輯者 | `PROJECT:DATASET.TABLE` | 資料表 | 建立 `TABLE` 資料表的快照。 |
| BigQuery 資料擁有者 | `PROJECT:BACKUP` | 資料集 | 在 `BACKUP` 資料集建立及刪除資料表快照。 |
| BigQuery 使用者 | `PROJECT` | 專案 | 執行排定的查詢，建立資料表快照。 |

這些角色會提供 `snapshot-bot` 服務帳戶所需的權限，以便執行查詢，建立 `DATASET.TABLE` 資料表的資料表快照，並將資料表快照放入 `BACKUP` 資料集。

## 編寫多陳述式查詢

本節說明如何編寫[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)，使用 [`CREATE SNAPSHOT TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_snapshot_table_statement)建立 `DATASET.TABLE` 資料表的[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。快照會儲存在 `BACKUP` 資料集，並在一天後過期。

```
-- Declare variables
DECLARE snapshot_name STRING;
DECLARE expiration TIMESTAMP;
DECLARE query STRING;

-- Set variables
SET expiration = DATE_ADD(current_timestamp(), INTERVAL 1 DAY);
SET snapshot_name = CONCAT(
                      "BACKUP.TABLE_",
                      FORMAT_DATETIME('%Y%m%d', current_date()));

-- Construct the query to create the snapshot
SET query = CONCAT(
              "CREATE SNAPSHOT TABLE ",
              snapshot_name,
              " CLONE mydataset.mytable OPTIONS(expiration_timestamp = TIMESTAMP '",
              expiration,
              "');");

-- Run the query
EXECUTE IMMEDIATE query;
```

## 排定每月查詢

[排定](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)查詢在每月第一天的上午 5:00 執行，如下所示：

### bq

1. 在 Google Cloud 控制台啟用 Cloud Shell：

   [啟用 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)
2. 輸入下列 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令：

   ```
   bq query --use_legacy_sql=false --display_name="Monthly snapshots of the TABLE table" \
   --location="us" --schedule="1 of month 05:00" \
   --project_id=PROJECT \
   'DECLARE snapshot_name STRING;
   DECLARE expiration TIMESTAMP;
   DECLARE query STRING;
   SET expiration = DATE_ADD(@run_time, INTERVAL 40 DAY);
   SET snapshot_name = CONCAT("BACKUP.TABLE_",
     FORMAT_DATETIME("%Y%m%d", @run_date));
   SET query = CONCAT("CREATE SNAPSHOT TABLE ", snapshot_name,
     " CLONE PROJECT.DATASET.TABLE OPTIONS(expiration_timestamp=TIMESTAMP \"",
     expiration, "\");");
   EXECUTE IMMEDIATE query;'
   ```
3. BigQuery 會排定查詢。

bq 指令列工具指令中的多重陳述式查詢與您在 Google Cloud 控制台執行的查詢不同，差異如下：

* bq 指令列工具查詢會使用 `@run_date`，而非 `current_date()`。在排定的查詢中，`@run_date` 參數包含目前日期。但在互動式查詢中，不支援 `@run_date` 參數。您可以使用 `current_date()`，而非 `@run_date`，在排定互動式查詢前進行測試。
* bq 指令列工具查詢使用 `@run_time` 而非 `current_timestamp()` 的原因類似：互動式查詢不支援 `@run_time` 參數，但可以使用 `current_timestamp()` 代替 `@run_time` 來測試互動式查詢。
* bq 指令列工具查詢使用斜線和雙引號 `\"`，而非單引號 `'`，因為單引號是用來括住查詢。

## 設定服務帳戶來執行排定的查詢

查詢目前排定使用您的憑證執行。
請按照下列步驟更新排定的查詢，改用 `snapshot-bot` 服務帳戶憑證執行：

1. 執行 [`bq ls`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_ls) 指令，取得排定查詢工作的身分：

   ```
   bq ls --transfer_config=true --transfer_location=us
   ```

   輸出看起來類似以下內容：

   | `name` | `displayName` | `dataSourceId` | `state` |
   | --- | --- | --- | --- |
   | `projects/12345/locations/us/transferConfigs/12345` | `Monthly snapshots of the TABLE table` | `scheduled_query` | `RUNNING` |
2. 使用 **`name`** 欄位中的 ID，執行下列 [`bq update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令：

   ```
   bq update --transfer_config --update_credentials \
   --service_account_name=snapshot-bot@PROJECT.iam.gserviceaccount.com \
   projects/12345/locations/us/transferConfigs/12345
   ```

Cloud Shell 會確認排定的查詢已成功更新。

## 檢查成果

本節說明如何確認查詢已正確排定、如何查看查詢執行時是否發生錯誤，以及如何確認每月快照是否已建立。

### 查看排定的查詢

如要確認 BigQuery 已排定每月資料表快照查詢，請按照下列步驟操作：

### 控制台

1. 在 Google Cloud 控制台中，前往「Scheduled queries」(已排定的查詢) 頁面：

   [前往「Scheduled queries」(已排定的查詢) 頁面](https://console.cloud.google.com/bigquery/scheduled-queries?hl=zh-tw)
2. 按一下**「Monthly snapshots of the TABLE table」**。
3. 按一下「設定」。
4. 確認「Query string」(查詢字串) 包含查詢，且查詢已排定在每個月的第一天執行。

### 查看排定查詢的執行記錄

排定的查詢執行後，您可以按照下列步驟查看是否執行成功：

### 控制台

1. 在 Google Cloud 控制台中，前往「Scheduled queries」(已排定的查詢) 頁面：

   [前往「Scheduled queries」(已排定的查詢) 頁面](https://console.cloud.google.com/bigquery/scheduled-queries?hl=zh-tw)
2. 按一下查詢說明「**Monthly snapshots of the TABLE table**」
3. 按一下「執行記錄」。

您可以查看查詢執行的日期和時間、執行是否成功，以及失敗時發生的錯誤。如要查看特定執行的詳細資料，請按一下「Run history」(執行記錄) 表格中的資料列。「Run details」(執行作業詳細資料) 窗格會顯示其他詳細資料。

### 查看資料表快照

如要確認資料表快照是否已建立，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面：

   [前往「BigQuery」](https://console.cloud.google.com/bigquery/scheduled-queries?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中開啟 `BACKUP` 資料集，並確認已建立 `TABLE_YYYYMMDD` 快照，其中 `YYYYMMDD` 是每個月的第一天。

   例如：

   * `TABLE_20220601`
   * `TABLE_20220701`
   * `TABLE_20220801`

## 後續步驟

* 如要進一步瞭解資料表快照，請參閱「[使用資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)」。
* 如要進一步瞭解如何排定查詢，請參閱「[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)」。
* 如要進一步瞭解 Google Cloud 服務帳戶，請參閱「[服務帳戶](https://docs.cloud.google.com/iam/docs/service-accounts?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]