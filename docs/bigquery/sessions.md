Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用工作階段

BigQuery 的[工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)可讓您在多個 SQL 查詢中維護狀態，例如臨時資料表、臨時函式和變數。您可以在 Google Cloud 控制台、bq 指令列工具或 BigQuery API 中建立、執行查詢、列出及終止工作階段。

完成這些步驟前，請確認您具備必要[權限](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw#roles_and_permissions)。

## 建立工作階段

如要擷取一組 SQL 活動，請建立 BigQuery 工作階段。建立工作階段後，您可以在工作階段中執行互動式查詢，直到工作階段[終止](#terminate-session)為止。工作階段中的所有查詢都會在工作階段建立的位置執行 (處理)。

### 控制台

在 Google Cloud 控制台中，每個工作階段都會指派給一個編輯器分頁。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 add\_box**Compose new query**。系統會開啟新的編輯器分頁。
3. 依序點選「編輯」>「查詢設定」。系統隨即會顯示「Query settings」(查詢設定) 面板。
4. 在「Session management」(工作階段管理) 部分，按一下「Use session mode」(使用工作階段模式)，啟用工作階段模式。
5. 在**「Additional settings」(其他設定) > 「Data location」(資料位置)** 中，選取
   位置。工作階段建立後，其中的所有查詢都會限制在這個位置，且無法變更。
6. 按一下「儲存」。
7. [在編輯器分頁中編寫查詢](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw)並執行。執行這項查詢後，系統會建立新的工作階段。

### bq

開啟 [Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)，然後輸入下列 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令：

```
bq query \
--nouse_legacy_sql \
--create_session
[--location 'SESSION_LOCATION'] \
'SQL_STATEMENT'
```

其中：

* SESSION\_LOCATION：將工作階段繫結至[實體位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。將工作階段中的所有查詢限制在這個位置。選填。
* SQL\_STATEMENT：工作階段的第一個 SQL 陳述式。

工作階段 ID 會與查詢結果一併傳回。

### API

使用下列參數呼叫 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 方法：

```
{
  "query": "SQL_STATEMENT",
  "createSession": true,
  ["location": "SESSION_LOCATION"]
}
```

其中：

* SQL\_STATEMENT：工作階段的第一個 SQL 陳述式。
* SESSION\_LOCATION：將工作階段繫結至[實體位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。將工作階段中的所有查詢限制在這個位置。選填。

回應主體大致如下：

```
{
  "jobReference": {
    "projectId": "myProject",
    "jobId": "job_123"
  },
  "statistics": {
    "sessionInfo": {
      "sessionId": "CgwKCmZhbGl1LXRlc3QQARokMDAzYjI0OWQtZ"
    }
  }
}
```

## 在工作階段中執行查詢

建立工作階段後，您可以在該工作階段中執行查詢：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下包含工作階段的編輯器分頁。
3. 在工作階段中新增查詢，然後點選「執行」。

### bq

開啟 [Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)，然後輸入下列 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令：

```
bq query \
--nouse_legacy_sql \
--session_id=SESSION_ID \
'SQL_STATEMENT'
```

其中：

* SESSION\_ID：請替換成要使用的[工作階段 ID](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#get-id)。
* SQL\_STATEMENT：要在工作階段中執行的 SQL 陳述式。

查詢結果後面會顯示工作階段 ID。

如果您要使用 Cloud Shell 執行大量查詢，可以將工作階段 ID 新增至 [`.bigqueryrc`](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#adding_flags_to_bigqueryrc) 中的 `[query]`，這樣就不必將工作階段 ID 複製及貼到每個指令中。

`.bigqueryrc` 中的工作階段 ID 如下所示：

```
[query]
--session_id=CgwKCmZhbGl1LXRlc3QQARokMDAzYjI0OWQtZ
```

將工作階段 ID 新增至 `.bigqueryrc` 後，您就可以從 `bq query` 指令中省略 `--session_id` 旗標。如要使用其他工作階段，或工作階段終止，則必須更新 `.bigqueryrc` 檔案。

### API

使用下列參數呼叫 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 方法：

```
{
  "query": "SQL_STATEMENT",
  "connectionProperties": [{
    "key": "session_id",
    "value": "SESSION_ID"
  }]
}
```

其中：

* SQL\_STATEMENT：工作階段的第一個 SQL 陳述式。
* SESSION\_ID：[工作階段 ID](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#get-id)。

## 終止工作階段

工作階段可以手動或自動終止。終止工作階段的記錄會保留 20 天。

### 自動終止工作階段

工作階段會在閒置 24 小時後或 7 天後自動終止，以先到者為準。

### 終止目前的工作階段

您可以使用 SQL 陳述式終止目前的工作階段，或在Google Cloud 控制台中終止 (如果工作階段是在控制台中建立)。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 找出含有工作階段的編輯器分頁，然後關閉。工作階段終止。

### SQL

如要終止工作階段，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CALL BQ.ABORT_SESSION();
   ```
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### 依 ID 終止工作階段

您可以使用工作階段 ID 終止工作階段。您不必加入工作階段，就能透過這種方式終止工作階段。

[取得工作階段 ID](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#get-id)，然後執行下列陳述式：

```
CALL BQ.ABORT_SESSION(SESSION_ID);
```

將 SESSION\_ID 替換為要終止的工作階段 ID。

## 取得目前活動時段的 ID

在某些情況下，您需要參照工作階段，才能繼續在其中工作。舉例來說，如果您使用 Cloud Shell，每次執行該工作階段的指令時，都必須加入工作階段 ID。

### 控制台

在 Google Cloud 控制台的工作階段中執行新查詢時，不必提供工作階段 ID。只要繼續在包含工作階段的編輯器分頁中操作即可。不過，如果您想在 Cloud Shell 或 API 呼叫中參照工作階段，就必須知道在控制台中建立的工作階段 ID。

完成這些步驟之前，請確認您已在有效工作階段中執行至少一項查詢。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下包含工作階段的編輯器分頁。
3. 在「Query results」(查詢結果) 中，按一下「Job information」(工作資訊)。
4. 在「Job information」(工作資訊) 清單中，搜尋工作階段 ID：

   ```
   Session ID: CgwKCmZhbGl1LXRlc3QQARokMDAzYjI0OWQtZ
   ```

### bq

如要在 Cloud Shell 的工作階段中執行查詢指令，您必須在指令中加入工作階段 ID。[建立工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#create-session)或[列出工作階段](#list-sessions)時，即可取得工作階段 ID。

使用 Cloud Shell 建立工作階段時，傳回的工作階段 ID 會與下列內容類似：

```
In session: CgwKCmZhbGl1LXRlc3QQARokMDAzYjI0OWQtZ
```

### API

如要透過 API 呼叫將 SQL 指令傳遞至工作階段，您必須在 API 呼叫中加入工作階段 ID。[建立工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#create-session)或[列出工作階段](#list-sessions)時，即可取得工作階段 ID。

使用 API 呼叫建立工作階段時，回應中的工作階段 ID 會類似下列內容：

```
sessionId: CgwKCmZhbGl1LXRlc3QQARokMDAzYjI0OWQtZ
```

## 列出有效和無效的工作階段

如要取得有效和無效工作階段的工作階段 ID，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，點選「工作記錄」。
4. 選取工作記錄類型：

   * 如要顯示近期工作的資訊，請按一下「個人記錄」。
   * 如要顯示專案中近期工作的資訊，請按一下「Project history」(專案記錄)。
5. 在「Session ID」欄中，您可以查看工作的階段 ID。

### SQL

如要取得最近三個工作階段的清單 (包括進行中和已終止的工作階段)，請在編輯器分頁中執行下列查詢：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     session_id,
     MAX(creation_time) AS last_modified_time
   FROM `region-REGION_NAME`.INFORMATION_SCHEMA.SESSIONS_BY_USER>
   WHERE
     session_id IS NOT NULL
     AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 20 DAY)
   GROUP BY session_id
   ORDER BY last_modified_time DESC;
   ```

   將 REGION\_NAME 替換為要列出工作階段的區域名稱。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

結果大致如下：

```
+-------------------------------------------------------------------------+
| session_id                                        | last_modified_time  |
+-------------------------------------------------------------------------+
| CgwKCmZhbGl1LXRlc3QQARokMGQ5YWWYzZmE0YjhkMDBm     | 2021-06-01 23:04:26 |
| CgwKCmZhbGl1LXRlc3QQARokMDAzYjI0OWQtZTczwZjA1NDc2 | 2021-05-30 22:43:02 |
| CgwKCmZhbGl1LXRlc3QQY2MzLTg4ZDEtYzVhOWZiYmM5NzZk  | 2021-04-07 22:31:21 |
+-------------------------------------------------------------------------+
```

## 查看工作階段記錄

工作階段會擷取一段時間內的 SQL 活動。這項資訊會儲存在工作階段記錄中。工作階段記錄可讓您追蹤工作階段中的變更。無論工作成功或失敗，都會記錄在工作階段記錄中，方便您日後查看。

### 控制台

如要在 Google Cloud 控制台查看工作階段記錄，您可以依工作階段 ID 篩選「Personal History」(個人記錄) 或「Project History」(專案記錄)，查看在特定工作階段中執行的所有 SQL 查詢。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，點選「工作記錄」。
4. 選取要查看的工作記錄類型：

   * 如要顯示近期工作的資訊，請按一下「Personal history」(個人記錄)。
   * 如要顯示專案中近期工作的資訊，請按一下「Project history」(專案記錄)。
5. 按一下「filter\_list 篩選器」，然後選取「工作階段 ID」。
6. 在「Session ID」欄位中，搜尋工作階段 ID：

   ```
   Session ID: CgwKCmZhbGl1LXRlc3QQARokMDAzYjI0OWQtZ
   ```

### SQL

如要查看特定工作階段的歷來資料，請先[取得工作階段 ID](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#get-id)，然後按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     *
   FROM
     `region-REGION_NAME`.INFORMATION_SCHEMA.SESSIONS_BY_USER
   WHERE
     session_info.session_id = 'SESSION_ID';
   ```

   替換下列內容：

   * REGION\_NAME：要查看工作階段資料的區域名稱
   * SESSION\_ID：要擷取歷來資料的工作階段 ID
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

#### 範例

下列指令會傳回工作階段 ID 為 `CgwKCmZhbGl1LXRlc3QQARokMDAzYjI0` 的工作階段記錄。您可以將這個工作階段 ID 替換成自己的 ID。

```
SELECT
  creation_time, query
FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_USER
WHERE
  session_info.session_id = 'CgwKCmZhbGl1LXRlc3QQARokMDAzYjI0'
  AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 20 DAY);
```

結果大致如下：

```
+---------------------+------------------------------------------------------------------------------------------+
|    creation_time    |                                          query                                           |
+---------------------+------------------------------------------------------------------------------------------+
| 2021-06-01 23:04:26 | SELECT * FROM Purchases;                                                                 |
| 2021-06-01 23:02:51 | CREATE TEMP TABLE Purchases(total INT64) AS SELECT * FROM UNNEST([10,23,3,14,55]) AS a;  |
+---------------------+------------------------------------------------------------------------------------------+
```

## 後續步驟

* 請參閱「[工作階段簡介](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)」。
* 進一步瞭解如何[在工作階段中編寫查詢](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]