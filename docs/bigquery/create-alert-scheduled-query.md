Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用排程查詢設定快訊

本文說明如何使用 BigQuery 排程查詢設定快訊。這種做法支援查詢邏輯定義的自訂用途。

## 事前準備

使用 Cloud Monitoring 之前，請確認您有下列項目：

* Cloud Billing 帳戶。
* 啟用計費功能的 BigQuery 專案。

如要確認您是否兩者都擁有，請完成[使用 Google Cloud 控制台的快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console?hl=zh-tw#before-you-begin)。

## 建立 SQL 查詢

在 BigQuery 中建立並執行 SQL 查詢，產生快訊的輸出內容。查詢會擷取您要監控的邏輯。
詳情請參閱「[執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)」。

## 設定排程查詢

您可以為查詢進行排程，讓查詢週期性執行，從每 15 分鐘到每幾個月都可以。您可以對記錄儲存區執行任何查詢。詳情請參閱「[排定查詢時間](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)」。

### 瞭解資料列計數指標

排定的查詢會在 Cloud Monitoring 中自動建立指標。這項指標會記錄 SQL 查詢在上次評估期間傳回的資料列數。您可以在 Monitoring 中建立快訊政策，監控這個資料列計數指標。

下列[指標](https://docs.cloud.google.com/monitoring/api/metrics_gcp_a_b?hl=zh-tw#gcp-bigquerydatatransfer)是量規，其中包含排定查詢的最新資料列計數：

`bigquerydatatransfer.googleapis.com/transfer_config/last_execution_job_rows`

所有排定的查詢都會使用不同的標籤，將資料列計數寫入這項指標。定義快訊政策時，您需要 `config_id` 標籤。如要找出 `config_id` 標籤，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduled queries」(已排定的查詢) 頁面：

   [前往「Scheduled queries」(已排定的查詢) 頁面](https://console.cloud.google.com/bigquery/scheduled-queries?hl=zh-tw)
2. 按一下要建立快訊的排程查詢。
3. 前往「詳細資料」分頁。
4. 檢查「資源名稱」中的最後一個字串，如下列螢幕截圖所示：

**注意：** 系統會連續 5 週重複顯示資料列數量的最後已知值。
如果停用排程查詢或查詢失敗，指標在 35 天內會維持最後一個已知值。35 天後，指標就會消失。

如果排定的查詢發生問題，排定查詢的「執行記錄」分頁會顯示錯誤訊息。

### 監控排程查詢

監控排定的查詢，確保順利執行：

* 在排定查詢的「執行記錄」分頁中尋找錯誤。
* 檢查儲存在[`bigquerydatatransfer.googleapis.com/transfer_config/completed_runs` 指標](https://docs.cloud.google.com/monitoring/api/metrics_gcp_a_b?hl=zh-tw#gcp-bigquerydatatransfer) `completion_state` 欄位中的每個排定執行作業最終狀態。
* 在 [BigQuery 資料移轉服務記錄](https://docs.cloud.google.com/bigquery/docs/dts-monitor?hl=zh-tw#logs)中尋找錯誤。

## 建立快訊政策

使用[指標門檻警示](https://docs.cloud.google.com/monitoring/alerts/using-alerting-ui?hl=zh-tw)，偵測排定查詢傳回的資料列數是否與門檻不同。

如要針對排程查詢傳回的資料列數量設定快訊，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的 *notifications*「Alerting」(警告) 頁面：

   [前往「Alerting」(快訊)](https://console.cloud.google.com/monitoring/alerting?hl=zh-tw)

   如果您是使用搜尋列尋找這個頁面，請選取子標題為「Monitoring」的結果。
2. 按一下「建立政策」。
3. 為排定查詢選取列數指標。在「選取指標」**選單中，依序點選「BigQuery DTS Config」>「Transfer\_config」>「Last executed job row count」**。
4. 在「新增篩選器」中，按一下「新增篩選器」。
5. 在「Filter」選單中，選取「config\_id」。
6. 在「值」選單中，選取要建立快訊的排定查詢 `config_id`：

   如果未設定篩選器，快訊會測試每個排定查詢的輸出內容。如要找出已排定時程查詢的 `config_id`，請參閱「[瞭解資料列計數指標](#understand_the_row_count_metric)」。
7. 保留預設的「轉換資料」設定，然後按一下「下一步」。
8. 在「條件類型」部分選取「門檻」。
9. 選取所需條件。舉例來說，如要在查詢傳回任何資料列時觸發快訊，請設定下列條件：

   1. 針對「Alert trigger」(快訊觸發條件)，選取「Any time series violates」(任何時間序列違反條件時)。
   2. 在「Threshold position」(門檻位置) 中選取「Above threshold」(高於門檻)。
   3. 在「Threshold value」(門檻值) 中，輸入 `0`。
10. 保留預設的「Advanced Options」(進階選項)，然後點選「Next」(下一步)。
11. 選用：如要設定快訊通知，請按一下「Use notification channel」(使用通知管道) 切換鈕，然後設定通知管道和主旨行。您也可以設定事件結案通知。

    如不想收到通知，請取消選取「使用通知管道」切換按鈕。
12. 選用：如果您有多項快訊政策，可以[為這些政策加上註解標籤](https://docs.cloud.google.com/monitoring/alerts/labels?hl=zh-tw)，指出政策是從排定查詢作業衍生而來。
13. 選用：在「Documentation」(說明文件) 欄位中，您可以新增有助於解讀快訊的連結。舉例來說，您可以新增「記錄檔探索工具」頁面的連結，並使用類似的查詢，以便探索觸發快訊的資料。你也可以連結至特定行程查詢的詳細資料頁面。
14. 在「為快訊政策命名」中，輸入快訊名稱。
15. 點選「建立政策」。

## 限制

排定查詢的快訊政策有下列限制：

* 排定查詢執行頻率和擷取延遲時間，會影響從記錄發出到收到快訊的總時間。舉例來說，如果查詢每 30 分鐘執行一次，且您新增 15 分鐘的擷取延遲時間，系統會在發出違規記錄項目後約 15 分鐘觸發快訊。在某些情況下，可能需要最多 45 分鐘。
* 排程查詢和快訊政策的設定不會連結或同步處理。在一個位置編輯設定可能會破壞關係，導致無法使用快訊功能。

## 後續步驟

* 瞭解如何建立及執行[排程查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]