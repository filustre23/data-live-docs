Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立資訊主頁、圖表及快訊

本文說明如何使用 Cloud Monitoring 建立圖表和快訊，監控 BigQuery 資源。

## 事前準備

使用 Cloud Monitoring 之前，請確認您有下列項目：

* Cloud Billing 帳戶。
* 啟用計費功能的 BigQuery 專案。

如要確認您是否兩者都擁有，請完成[使用 Google Cloud 控制台的快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-web-ui?hl=zh-tw)。

## 查看及建立資訊主頁、圖表和快訊

### 查看 Cloud Monitoring 資訊主頁

如何使用 Cloud Monitoring 監控 BigQuery 專案：

1. 前往 Google Cloud 控制台的「Monitoring」頁面。

   [前往「Monioring」](https://console.cloud.google.com/monitoring?hl=zh-tw)
2. 如果尚未在頁面頂端選取專案名稱，請立即選取。
3. 選取「資訊主頁」>「BigQuery」，即可查看 BigQuery 資源。這個頁面會列出可供使用者設定的資料表、事件和事件回報，以及專案指標或資料集指標的圖表。

### 以視覺化方式呈現可用的運算單元和已分配的運算單元

如要視覺化可用的運算單元與分配至您專案的運算單元，請前往 BigQuery 的資訊主頁，說明請見「[查看 Cloud Monitoring 資訊主頁](#view-dashboards)」：

1. 前往 Google Cloud 控制台的「Monitoring」頁面。

   [前往「Monioring」](https://console.cloud.google.com/monitoring?hl=zh-tw)
2. 依序選取「資訊主頁」>「BigQuery」。
3. 在 BigQuery 的 Cloud Monitoring 資訊主頁上，捲動至名為「Slot Utilization」(使用配額) 的圖表。

**Slot Utilization** 圖表會同時顯示在主要的 Cloud Monitoring 預設資訊主頁，以及適用於 BigQuery 的 Cloud Monitoring 資訊主頁。

### 建立資訊主頁與圖表

在您自己的圖表與資訊主頁中顯示 Cloud Monitoring 收集的指標：

1. 前往 Google Cloud 控制台的「Monitoring」頁面。

   [前往「Monioring」](https://console.cloud.google.com/monitoring?hl=zh-tw)
2. 選取 [Dashboards] (資訊主頁) > [Create Dashboard] (建立資訊主頁)。
3. 按一下 [Add Chart] (新增圖表)。畫面會出現「Add Chart」(新增圖表) 頁面：
4. 在「Find resource type and metric」(尋找資源類型和指標) 面板的欄位中：

   * 在「Resource type」(資源類型) 下拉式清單中選取「Global」(全域)。您可能需要展開「資源類型」清單，才能看到「全域」選項。
   * 在「指標」下拉式清單中，選取「查詢執行時間」。
5. 「Aggregation」(匯總) 窗格的欄位可用來控制執行時間資料的顯示方式。您可以調整這些欄位的預設設定。
6. 按一下 [儲存]。

### 查看配額用量和限制

在 Cloud Monitoring 中，您可以查看配額用量和限制的指標：

1. 前往 Google Cloud 控制台的「Monitoring」頁面。

   [前往「Monioring」](https://console.cloud.google.com/monitoring?hl=zh-tw)
2. 在導覽窗格中，選取「bar\_chart Metrics Explorer」。
3. 在工具列中，依序選取「Explorer」**>「Configuration」**。
4. 在「資源和指標」部分，按一下「選取指標」。
5. 依序選取「Consumer Quota」**>「Quota」>「Quota limit」**，然後按一下「Apply」。
6. 按一下「新增篩選條件」add\_box，然後在「標籤」選單中選取「limit\_name」。
7. 在「值」選單中，選取要查看指標的配額。

**注意：** 您只能查看「BigQuery Storage Write API (gRPC)」的並行連線和輸送量配額用量與限制指標。

### 建立警告

如要建立警告政策，以便在 [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw) 查詢的執行時間第 99 個百分位數超過使用者定義的限制時觸發，請使用下列設定。

#### 建立[警告政策](https://docs.cloud.google.com/monitoring/alerts/using-alerting-ui?hl=zh-tw#create-policy)的步驟。

如要建立警告政策，請按照下列指示操作：

1. 前往 Google Cloud 控制台的 *notifications*「Alerting」(警告) 頁面：

   [前往「Alerting」(警告)](https://console.cloud.google.com/monitoring/alerting?hl=zh-tw)

   如果是使用搜尋列尋找這個頁面，請選取子標題為「Monitoring」的結果。
2. 如果尚未建立通知管道，但想收到通知，請按一下「Edit Notification Channels」(編輯通知管道)，新增通知管道。新增管道後，請返回「Alerting」(警告) 頁面。
3. 在「Alerting」(警告) 頁面，選取「Create policy」(建立政策)。
4. 如要選取資源、指標和篩選條件，請展開「Select a metric」(選取指標) 選單，然後使用「New condition」(新條件) 表格中的值：
   1. 選用：如要限制選單只顯示相關項目，請在篩選列輸入資源或指標名稱。
   2. 選取「資源類型」。例如，選取「VM 執行個體」。
   3. 選取「指標類別」。例如選取「執行個體」。
   4. 選取**指標**。例如，選取「CPU 使用率」。
   5. 選取 [Apply] (套用)。
5. 點選「下一步」，然後設定警告政策觸發條件。如要填寫這些欄位，請使用「設定快訊觸發條件」表格中的值。
6. 點選「下一步」。
7. 選用：如要新增警告政策的通知，請按一下「Notification channels」(通知管道)。在對話方塊中，從選單選取一或多個通知管道，然後按一下「OK」(確定)。

   如要在警示開啟和關閉時收到通知，請勾選「在警示關閉時發送通知」。根據預設，系統只會在開啟快訊時傳送通知。
8. 選用：更新「Alert autoclose duration」(快訊自動關閉期限)。這個欄位會決定 Monitoring 在沒有指標資料下關閉快訊的時機。
9. 選用：按一下「Documentation」(說明文件)，新增要納入通知訊息的資訊。
10. 按一下「Alert name」(警告名稱)，輸入警告政策的名稱。
11. 點按「建立政策」。

| **新條件** 欄位 | 值 |
| --- | --- |
| **資源和指標** | 在「資源」選單中，選取「BigQuery 專案」。  在「指標類別」選單中，選取「查詢」。  在「指標」選單中，選取「查詢執行時間」。 |
| **篩選器** |  |
| **跨時間序列  時間序列分組依據** | `priority` |
| **跨時間序列  時間序列匯總** | `99th percentile` |
| **滾動週期** | `5 m` |
| **滾動週期函式** | `sum` |

| **設定快訊觸發條件** 欄位 | 值 |
| --- | --- |
| **條件類型** | `Threshold` |
| **警告觸發條件** | `Any time series violates` |
| **門檻位置** | `Above threshold` |
| **門檻值** | 這個值由您決定，但建議設為 60 秒。 |
| **重新測試週期** | `most recent value` |

如要建立警告政策，以便在 BigQuery 專案的總掃描位元組數超過使用者定義的限制時接收通知，請使用下列警告政策設定。

| **新條件** 欄位 | 值 |
| --- | --- |
| **資源和指標** | 在「資源」選單中，選取「BigQuery 專案」。  在「指標類別」選單中，選取「查詢」。  在「指標」選單中，選取「聲明掃描位元組費用」。 |
| **篩選器** | *(No filter needed for a project-wide alert)* |
| **跨時間序列  時間序列分組依據** | *(如要匯總所有系列，請留空)* |
| **跨時間序列  時間序列匯總** | `sum` |
| **滾動週期** | `5 m` |
| **滾動週期函式** | `sum` |

| **設定警告觸發條件** 欄位 | 值 |
| --- | --- |
| **條件類型** | `Threshold` |
| **警告觸發條件** | `Any time series violates` |
| **門檻位置** | `Above threshold` |
| **門檻值** | 這個值由您決定。舉例來說，如要在用量超過 1 TiB 時觸發快訊，請輸入 `1000000000000`。 |

警告政策會監控掃描的位元組總數，但您可以根據特定預算設定門檻。如要完成這項以預算為準的警告政策，請先將所需費用門檻轉換為等值的位元組數。公式會採用 BigQuery 隨選運算定價。
詳情請參閱「[以量計價的運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)」。

您可以使用下列公式，將費用門檻轉換為位元組：

```
Threshold in Bytes = (Target Amount / (price per TiB)) * 1,000,000,000,000
```

#### 範例：使用量超過 $100 美元時觸發快訊

假設您希望在專案的查詢費用超過 **$100 美元**時收到快訊。

1. **計算 TiB 的等值資料量：**  
   `$100 / (price per TiB) = Equivalent Data Volume in TiB`
2. **將資料量轉換為位元組：**  
   `(Equivalent Data Volume in TiB) * 1,000,000,000,000 = Threshold Value in Bytes`
3. **設定門檻值：**  
   在政策的「設定警告觸發條件」部分，輸入「門檻值 (以位元組為單位)」做為「門檻值」。

現在，當滾動時間範圍內計費的掃描位元組總數，相當於隨選查詢費用約 **$100 美元**時，系統就會觸發警告政策。

## 可供視覺化的指標

下列指標可供視覺化，但延遲時間可能長達數小時。

| **資源類型** | **名稱** | **單位** | **說明** |
| --- | --- | --- | --- |
| BigQuery | Scanned bytes | 每分鐘位元組數 | 掃描的位元組數。 |
| BigQuery | Scanned bytes billed | 每分鐘位元組數 | 使用隨選分析模型時，計費的傳送位元組數。 由於費用會向上取整，且每項查詢處理的資料量有基本額度，因此「掃描的位元組數」和「計費的掃描位元組數」可能會有所不同。 |
|
| BigQuery | BI Engine Query Fallback Count ([Preview](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) | 查詢 | 以比率表示未使用 BI Engine 的查詢數量。您可以將 **「Group By」(分組依據)** 選項設為 `reason`，將計數依不同的備用廣告原因分開，包括：  * `NO_RESERVATION` * `INSUFFICIENT_RESERVATION` * `UNSUPPORTED_SQL_TEXT` * `INPUT_TOO_LARGE` * `OTHER_REASON` |
| BigQuery | Query count | 查詢 | 進行中的查詢。 |
| BigQuery | Query execution count ([Preview](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) | 查詢 | 執行的查詢數。 |
| BigQuery | Query execution times  - 5th percentile  - 50th percentile  - 95th percentile  - 99th percentile | 秒 | 未快取查詢的執行時間。 |
| BigQuery | Slots used by project | 運算單元 | 專案中查詢工作分配到的 BigQuery 運算單元數。 系統會為每個帳單帳戶分配運算單元，多個專案可以共用相同的運算單元預留量。 |
| BigQuery | Slots used by project and job type | 運算單元 | 在任何時間分配給專案的運算單元數，並按照[工作類型](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)來區別。這也可以視為該專案正在使用的運算單元數。載入和擷取作業是免費作業，會在公開資源集區中執行。 系統會為每個帳單帳戶分配配額，多個專案可以共用相同的配額預留量。 |
| BigQuery | Slots used by project, reservation, and job type | 運算單元 | 專案分配到的 BigQuery 運算單元數量。運算單元分配情況可依預訂和工作類型細分。 |
| BigQuery | Total slots | 運算單元 | 專案可用的運算單元總數。 如果專案與其他專案共用運算單元預留項目，則不會顯示其他專案使用的運算單元。 |
| BigQuery | Slots used across projects in reservations | 運算單元 | 預留項目中分配給各專案的 BigQuery 運算單元數量。請注意，只有在至少一個專案已指派給預訂項目並消耗配額時，系統才會回報指標資料。建議您改用 [`INFORMATION_SCHEMA`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw) 查詢預訂資訊。如要查看從預留項目取用的所有專案的時段用量指標，您必須明確將這些取用專案新增至您查看資訊主頁的專案的[指標範圍](https://docs.cloud.google.com/monitoring/settings?hl=zh-tw)。 |
| BigQuery | Slots used by project in reservation | 運算單元 | 預留項目中分配給專案的 BigQuery 運算單元數。如要查看從預留項目取用容量的所有專案的時段用量指標，您必須明確將這些取用容量的專案新增至專案的[指標範圍](https://docs.cloud.google.com/monitoring/settings?hl=zh-tw)，才能在該專案中查看資訊主頁。 |
| BigQuery 持續性工作 | Estimated backlog logical bytes | 位元組數 | 連續工作各階段的待處理位元組數。 |
| BigQuery 持續性工作 | Estimated backlog records | 記錄 | 連續工作各階段的預估待處理記錄數。 |
| BigQuery 持續性工作 | Estimated bytes processed | 位元組數 | 連續工作各階段的預估處理位元組數。 |
| BigQuery 持續性工作 | Output watermark | 時間戳記 | 最新的時間戳記 (以自 Epoch 紀元以來的微秒數表示)，這個時間點之前的所有資料都已由這項連續工作的階段處理完畢。 |
| BigQuery 持續性工作 | Records read | 記錄 | 每個階段的連續工作讀取的輸入記錄數。 |
| BigQuery 持續性工作 | Records written | 記錄 | 連續工作各階段寫入的輸出記錄數量。 |
| BigQuery 持續性工作 | Slots used | 運算單元時間 (毫秒) | 連續工作使用的運算單元總毫秒數。 |
| BigQuery 資料集 | Stored bytes | 位元組數 | 儲存在資料集內的位元組數；系統會針對資料集內最大的前 100 個資料表，(按名稱) 顯示儲存在每個資料表中的位元組數。資料集中的所有其他資料表 (除了前 100 大資料表以外) 則會以單一總和報告，且摘要中的資料表名稱為空白字串。 |
| BigQuery 資料集 | Table count | 資料表 | 資料集中的資料表數量。 |
| BigQuery 資料集 | Uploaded bytes | 每分鐘位元組數 | 已上傳到資料集中任何資料表的位元組數。 |
| BigQuery 資料集 | 上傳的資料列 | 每分鐘划船次數 | 上傳到資料集中任何資料表的記錄數。 |

如需可用 Google Cloud 指標的完整清單，請參閱[Google Cloud 指標](https://docs.cloud.google.com/monitoring/api/metrics_gcp?hl=zh-tw#gcp-bigquerybiengine)。

## 已知問題

* 如果沒有任何查詢正在執行，系統就不會傳回已分配的時段、可用時段或任何查詢相關變數的資料。請縮小以查看資料。
* 如果同時在美國與歐盟執行查詢，則分配的運算單元和可用的運算單元可能會有錯誤。
* 系統會以特定時間範圍的平均值回報分配的運算單元 (時間範圍的長度視圖表的縮放等級而定)。因此，進行縮放可能會變更分配運算單元的值。放大以檢視最多 1 小時的時間範圍內的資料，即可讓系統顯示已分配運算單元數的真實數值。採用這個時間範圍時，圖表上任何可見的時間都會是 `avg(slots allocated) = slots allocated`。
* Cloud Monitoring 圖表中的資料僅適用於所選專案。
* 指標是即時值，會在特定時間點取樣，因此可能會遺漏取樣間隔之間的資料點。舉例來說，系統每分鐘會對工作計數指標取樣一次。這個值是該特定時間的工作數量，而非整分鐘內的工作數量上限。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-15 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-15 (世界標準時間)。"],[],[]]