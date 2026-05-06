Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 監控及查看 BigQuery 資料移轉服務的記錄

BigQuery 資料移轉服務的[監控](#monitor)和[記錄](#logs)功能，可提供服務工作負載效能和狀態的相關資訊。BigQuery 資料移轉服務會將監控資料匯出至 [Cloud Monitoring](https://docs.cloud.google.com/monitoring/docs?hl=zh-tw)。

## 監控 BigQuery 資料移轉服務

監控指標可用於以下目的：

* 評估資料移轉設定的用量和效能。
* 排解問題。
* 監控轉移作業的執行狀態。

如要使用 Monitoring 建立自訂資訊主頁、設定快訊及查詢指標，您可以使用 Google Cloud 控制台或 [Monitoring API](https://docs.cloud.google.com/monitoring/api?hl=zh-tw)。

### 在 Metrics Explorer 中查看轉移資料

1. 前往 Google Cloud 控制台的「Monitoring」頁面。

   [前往「Monitoring」頁面](https://console.cloud.google.com/monitoring?hl=zh-tw)
2. 在導覽窗格中，按一下「指標探索工具」。
3. 選取專案。
4. 在「Find resource type and metric」(尋找資源類型和指標) 方塊中，輸入下列內容：

   * 在「Resource type」(資源類型) 部分輸入 `BigQuery DTS Config`。
   * 在「指標」中，選取「移轉設定的監控指標」中列出的其中一個指標，例如 `Completed run count`。
5. 選用：選取對齊器、縮減器和其他參數。
6. 指標會顯示在「指標探索工具」視窗中。

### 定義 Cloud Monitoring 快訊

您可以為 BigQuery 資料移轉服務指標定義[監控快訊](https://docs.cloud.google.com/monitoring/alerts?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「Monitoring」頁面。

   [前往「Monitoring」頁面](https://console.cloud.google.com/monitoring?hl=zh-tw)
2. 在導覽窗格中，依序選取「快訊」**>「建立政策」**。

   如要進一步瞭解快訊政策和相關概念，請參閱「[快訊政策類型](https://docs.cloud.google.com/monitoring/alerts/types-of-conditions?hl=zh-tw)」。
3. 按一下「新增條件」，然後選取條件類型。
4. 選取指標與篩選器。指標的資源類型是 **BigQuery DTS 設定**。
5. 按一下 [Save Condition] (儲存條件)。
6. 輸入政策名稱，然後按一下「儲存政策」。

如要進一步瞭解快訊政策和概念，請參閱[快訊簡介](https://docs.cloud.google.com/monitoring/alerts?hl=zh-tw)。

### 定義 Cloud Monitoring 自訂資訊主頁

您可以根據 BigQuery 資料移轉服務指標建立自訂資訊主頁：

1. 前往 Google Cloud 控制台的「Monitoring」頁面。

   [前往「Monitoring」頁面](https://console.cloud.google.com/monitoring?hl=zh-tw)
2. 在導覽窗格中，選取「資訊主頁」**>「建立資訊主頁」**。
3. 按一下 [Add Chart] (新增圖表)。
4. 為圖表命名。
5. 選取指標與篩選器。指標的資源類型是 **BigQuery DTS 設定**。
6. 按一下 [儲存]。

詳情請參閱「[管理自訂資訊主頁](https://docs.cloud.google.com/monitoring/charts/dashboards?hl=zh-tw)」。

### 指標回報頻率與保留期

系統會以 1 分鐘為間隔，分批將 BigQuery 資料移轉服務執行的指標匯出至 Monitoring。監控資料會保留 6 週。

資訊主頁會以 `1h` (1 小時)、`6H` (6 小時)、`1D` (1 天)、`1W` (1 週) 和 `6W` (6 週) 的預設間隔時間提供資料分析。您可以手動索取從 `1M` (1 分鐘) 到 `6W` (6 週) 之間任何間隔時間的資料分析。

### 監控移轉設定的指標

BigQuery 資料移轉服務設定的下列指標會匯出至 Monitoring：

| **指標** | **說明** |
| --- | --- |
| 執行延遲分布 | 每個移轉設定的每次移轉作業執行時間分布情形 (以秒為單位)。 |
| 有效執行次數 | 每個移轉設定的執行中或待處理移轉工作數。 |
| 已完成的執行作業數 | 每個移轉設定在一段時間內完成的移轉執行次數。 |

### 篩選指標的維度

系統會針對每項 BigQuery 資料移轉服務設定匯總指標。您可以依據下列維度篩選匯總的指標：

| **屬性** | **說明** |
| --- | --- |
| `TRANSFER_STATE` | 代表移轉作業目前的移轉狀態。這項維度可包含下列其中一個值：   * `unspecified` * `pending` * `running` * `succeeded` * `failed` * `cancelled` |
| `ERROR_CODE` | 代表轉移作業的最終錯誤代碼。這項維度可包含下列其中一個值：   * `OK` * `CANCELLED` * `UNKNOWN` * `INVALID_ARGUMENT` * `DEADLINE_EXCEEDED` * `NOT_FOUND` * `ALREADY_EXISTS` * `PERMISSION_DENIED` * `UNAUTHENTICATED` * `RESOURCE_EXHAUSTED` * `FAILED_PRECONDITION` * `ABORTED` * `OUT_OF_RANGE` * `UNIMPLEMENTED` * `INTERNAL` * `UNAVAILABLE` * `DATA_LOSS` |
| `RUN_CAUSE` | 代表觸發轉移作業的方式。這項維度可包含下列其中一個值：   * `USER_REQUESTED` * `AUTO_SCHEDULE` |

## BigQuery 資料移轉服務記錄

系統會使用 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw) 記錄每次 BigQuery 資料移轉服務的執行作業。系統會自動為所有資料轉移作業啟用記錄功能。

### 必要的角色

「記錄檢視者」角色 (`roles/logging.viewer`) 賦予您對 Logging 所有功能的唯讀存取權。如要進一步瞭解適用於記錄資料的身分與存取權管理 (IAM) 權限和角色，請參閱 [Logging 存取權控管指南](https://docs.cloud.google.com/logging/docs/access-control?hl=zh-tw)。

### 查看記錄

如要查看記錄，請前往「Logs Explorer」頁面。

[前往記錄檔探索工具](https://console.cloud.google.com/logs?hl=zh-tw)

BigQuery 資料移轉服務記錄會先依移轉設定建立索引，然後再依個別移轉作業建立索引。

#### 查看移轉作業記錄

如要只顯示特定轉移作業 `run_id` 的記錄項目，請在**查詢建立工具**中新增下列篩選條件：

```
resource.type="bigquery_dts_config"
labels.run_id="transfer_run_id"
```

#### 查看移轉設定記錄

如要顯示特定轉移作業 `config_id` 的記錄項目，請在「查詢建立工具」中新增下列篩選條件：

```
resource.type="bigquery_dts_config"
resource.labels.config_id="transfer_config_id"
```

#### 查看所有記錄檔

如要查看所有 BigQuery 資料移轉服務記錄，請執行下列任一操作：

* 在「Fields」(欄位) 窗格中，選取「Resource type」(資源類型) 的「BigQuery DTS Config」(BigQuery DTS 設定)。
* 在「查詢建立工具」中新增下列篩選器：

  ```
  resource.type="bigquery_dts_config"
  ```

如要進一步瞭解如何使用記錄檔探索工具，請參閱「[使用記錄檔探索工具](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw)」。

### 記錄格式

BigQuery 資料移轉服務會以以下格式記錄訊息：

```
{
  "insertId": "0000000000",
  "jsonPayload": {
    "message": "DTS transfer run message."
  },
  "resource": {
    "type": "bigquery_dts_config",
    "labels": {
      "project_id": "my_project_id",
      "config_id": "transfer_config_id",
      "location": "us"
    }
  },
  "timestamp": "2020-11-25T04:45:48.545732221Z",
  "severity": "INFO",
  "labels": {
    "run_id": "transfer_run_id"
  },
  "logName": "projects/your_project_id/logs/bigquerydatatransfer.googleapis.com%2Ftransfer_config",
  "receiveTimestamp": "2020-11-25T04:45:48.960214929Z"
}
```

### 記錄內容

BigQuery 資料移轉服務記錄檔項目包含的資訊適合用於監控移轉執行作業及進行偵錯。記錄項目包含下列資訊類型：

* `timestamp`：用於計算記錄項目的存在時間，並強制執行記錄的保留期限
* `severity`：可以是 `INFO`、`WARNING` 或 `ERROR`
* `message_text`：保留說明目前轉移作業執行狀態的字串

## 後續步驟

* 進一步瞭解 [Monitoring](https://docs.cloud.google.com/monitoring?hl=zh-tw)。
* 請參閱 [Cloud 稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw)和 [Cloud Logging](https://docs.cloud.google.com/logging?hl=zh-tw)的總覽。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]