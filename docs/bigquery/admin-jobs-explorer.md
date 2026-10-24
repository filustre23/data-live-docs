Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 監控工作

您可以使用 Google Cloud 控制台中的 BigQuery 管理工作探索工具，監控、篩選及排解整個組織的工作，不必手動編寫`INFORMATION_SCHEMA`查詢。您可以追蹤執行趨勢、比較工作效能，以及檢查查詢指標 (例如運算單元用量、時間長度和執行圖表)，以解決瓶頸問題。

如要監控整個組織的運算資源、運算單元承諾使用合約和長期預留項目使用率，請參閱「[監控健康狀態和資源使用率](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)」。

## 功能

您可以使用工作多層檢視執行下列操作：

* **篩選及找出工作**：根據工作狀態、時間長度、擁有者或運算單元用量等條件[套用篩選器](#filter-jobs)，在整個組織中搜尋特定查詢。
* **分析時間軸指標**：使用[指標圖表](#view-metric-chart)，追蹤工作執行趨勢和並行情形。
* **依資源匯總工作**：依擁有者、專案或預留項目[將工作分組](#group-jobs)，查看摘要統計資料，並深入分析篩選後的資料表。
* **疑難排解工作**：選取個別工作，在「[**Job
  details**](#view_job_details)」(工作詳細資料) 頁面 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 查看查詢執行圖、SQL 文字和執行記錄。
* **比較成效**：[比較工作](#compare-jobs) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，找出指標的重大差異，並解決潛在的效能問題。
* **取得 AI 輔助**：[使用 Gemini Code Assist 進行疑難排解](#troubleshoot-with-ai)、[工作探索工具](https://cloud.google.com/products?hl=zh-tw#product-launch-stages) (預先發布版) 分析工作統計資料，或解釋執行速度緩慢的查詢。

BigQuery 會從下列 `INFORMATION_SCHEMA` 檢視表提供工作詳細資料和洞察：

* [`INFORMATION_SCHEMA.JOBS_BY_PROJECT`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-organization?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_BY_USER`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-user?hl=zh-tw)

**注意：** 如果您使用組織權限限制，請參閱「[啟用 Google 擁有的資源存取權](https://docs.cloud.google.com/resource-manager/docs/organization-restrictions/additional-considerations?hl=zh-tw#google-owned-resources)」。

## 事前準備

如要使用 Gemini Code Assist [排解 BigQuery 中的工作問題 (預先發布版)](#troubleshoot-with-ai)，請參閱「[設定 Gemini Code Assist](https://docs.cloud.google.com/cloud-assist/set-up-gemini?hl=zh-tw)」，瞭解如何啟用 API 並授予必要角色。

### 必要的角色

如要取得使用工作探索工具監控工作所需的權限，請要求管理員授予您下列 IAM 角色：

* 在專案層級查看工作：專案的 [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`)
* 查看組織層級的工作：組織的 [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`)
* 查看工作詳細資料：在執行查詢的專案中，具備 [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`) 角色
* 查看系統層級詳細資料：管理專案的 [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備使用工作探索工具監控工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

必須具備下列權限，才能使用工作探索工具監控工作：

* 查看專案層級的工作：專案的 `bigquery.jobs.listAll`
* 查看組織層級的工作：
  `bigquery.jobs.listAll`
  組織

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

**注意：** 只有在您定義 Google Cloud組織後，才能使用組織檢視畫面。

如要使用 Gemini Code Assist 疑難排解工作問題，請參閱[使用 Gemini Code Assist 的其他 IAM 需求](https://docs.cloud.google.com/cloud-assist/iam-requirements?hl=zh-tw)。

## 篩選工作

如要篩選 `INFORMATION_SCHEMA.JOBS*` 檢視表中的查詢工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，點選「Jobs explorer」(工作探索工具)。
3. 在「Jobs explorer」(工作探索工具) 頁面的「Location」(位置) 欄位中，選取要查看工作的所在位置。
4. 在「Filters」(篩選器) 窗格中，視需要套用選用篩選器。如果未顯示這個窗格，請按一下「insert\_chart」insert\_chart「顯示篩選器」。

   可用的篩選器如下：

   * **工作範圍**：依瀏覽權限層級篩選工作，例如目前專案、組織和您的工作。您可以選擇查看目前專案、整個組織或僅限您啟動的工作。
   * **圖表檢視畫面**：
     + **「Finished jobs」(已完成的工作)**：顯示已完成查詢的時間軸資料，區分成功完成的工作和發生錯誤的工作。
     + **並行**：顯示查詢並行的時間軸資料，區分執行中的工作和排入佇列的工作。
   * **分組依據**：依特定資源 (例如擁有者、專案或預留項目) 將顯示的工作分組。詳情請參閱「[依資源將工作分組](#group-jobs)」。
   * **狀態**：依目前執行狀態篩選工作，例如已完成、錯誤、有效和已排入佇列。每個多面向狀態篩選器選項旁會直接顯示摘要計數，指出處於該狀態的工作數量。
   * **專案 ID**：篩選在特定專案中執行的工作。
   * **預留項目 ID**：篩選使用特定預留項目運算單元的工作。這有助於監控不同工作負載如何耗用預留容量。
   * **擁有者**：依啟動工作的使用者或服務帳戶電子郵件地址篩選工作。
   * **工作 ID**：依據專屬英數字元 ID 篩選特定工作。
   * **查詢雜湊**：篩選具有特定查詢雜湊的工作。查詢雜湊會識別查詢的邏輯，忽略註解、參數值、UDF 和常值的差異，協助您找出相同查詢邏輯的所有執行作業。如果 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 查詢成功，但未命中快取，就會顯示這個欄位。
   * **標籤**：根據您或貴組織附加至工作的自訂中繼資料標籤篩選工作。方便您依部門或應用程式分類及追蹤工作。
   * **查詢洞察**：篩選 BigQuery 判定有特定效能問題的工作，例如運算單元爭用、超出記憶體重組容量，以及資料輸入規模變更。
   * **運算單元時間超過**：篩選耗用超過指定運算單元毫秒數的工作。這是找出資源密集查詢的重要指標。
   * **Duration more than** (時間長度超過)：篩選出完成時間超過指定時間長度的工作。您可以使用這項功能，找出執行速度比預期慢的查詢。
   * **Bytes processed more than** (處理的位元組數超過)：篩選掃描資料量超過指定數量的工作。這有助於找出可能導致資料處理費用偏高的查詢。
   * **工作類別**：依執行的作業類型篩選工作，例如標準 SQL 查詢或用於即時資料處理的持續查詢。
   * **工作建立原因**：根據 BigQuery 建立工作的原因篩選工作，例如查詢超過逾時時間，或產生的結果過大，無法在單一回應中傳回。
   * **工作優先順序**：依執行優先順序篩選工作，例如互動式或批次工作。

### 查看工作時間軸指標

工作探索工具包含互動式指標圖表，可顯示符合篩選條件的查詢時間軸資料。您可以使用這張圖表評估工作負載模式，並找出已完成、進行中或排入佇列的工作數量是否突然增加。如要查看整個組織在較長時間範圍內的並行趨勢，請參閱「[指標時間線圖](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw#metric-timeline-charts)」。

如要在工作探索工具中設定指標圖表，請按照下列步驟操作：

1. 前往「**Jobs explorer**」頁面。

   [前往「Jobs explorer」(工作探索工具)](https://console.cloud.google.com/bigquery/admin/jobs-explorer?hl=zh-tw)
2. 前往「篩選器」窗格。如果未顯示這個窗格，請按一下「insert\_chart」insert\_chart「Show filters」(顯示篩選器)。
3. 選取要在圖表中顯示的指標：

   * **「Finished jobs」(已完成的工作)**：顯示已完成查詢的時間軸資料，區分成功完成的工作和發生錯誤的工作。
   * **並行**：顯示查詢並行的時間軸資料，區分執行中的工作和排入佇列的工作。

### 依資源將工作分組

如要匯總工作統計資料，並比較整個組織的用量，您可以按照擁有者、專案或預留項目將工作分組，而不是在未匯總的資料表中查看個別工作。

如要將工作分組，請按照下列步驟操作：

1. 前往「**Jobs explorer**」頁面。

   [前往「Jobs explorer」(工作探索工具)](https://console.cloud.google.com/bigquery/admin/jobs-explorer?hl=zh-tw)
2. 前往「篩選器」窗格。如果未顯示這個窗格，請按一下「insert\_chart」insert\_chart「Show filters」(顯示篩選器)。
3. 按一下「分組依據」，然後選取下列其中一個選項：

   * **None** (預設)：顯示個別工作的未匯總表格。
   * 「Owner」(擁有者)：依執行工作的使用者或服務帳戶電子郵件地址，將工作分組。
   * **專案**：依專案 ID 分組工作。
   * **Reservation**：依預留項目 ID 分組工作。

將「Group by」(分組依據) 設為「Owner」(擁有者)、「Project」(專案) 或「Reservation」(預留項目) 時，BigQuery 會顯示匯總檢視畫面，其中包含各項資源的摘要面板。每個面板都會顯示下列摘要統計資料：

* **執行中的工作**：執行中的工作數量。
* **已排入佇列的工作**：在查詢佇列中等待的工作數量。
* **發生錯誤的工作**：無法完成的工作數量。
* **Completed jobs** (已完成的工作)：成功完成的工作數量。
* **運算單元時間**：該資源的工作耗用的運算單元毫秒總數。
* **處理的位元組**：工作為該資源掃描的資料總量。

如要檢查與特定資源相關聯的個別工作，請按一下該資源的面板，展開並顯示其工作的篩選表格。

## 排解工作效能問題

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要針對這項功能提供意見回饋或尋求支援，請傳送電子郵件至 [bq-performance-troubleshooting+feedback@google.com](mailto:bq-performance-troubleshooting+feedback@google.com)。

如要診斷及排解查詢問題，您可以在「Job details」(工作詳細資料) 頁面查看執行指標、SQL 文字和歷來效能差異。

### 查看工作詳細資料

如要查看工作詳細資料並分析查詢執行情形，請按照下列步驟操作：

1. 前往「**Jobs explorer**」頁面。

   [前往「Jobs explorer」(工作探索工具)](https://console.cloud.google.com/bigquery/admin/jobs-explorer?hl=zh-tw)
2. 選用：如要縮小顯示的工作範圍，請[篩選](#filter-jobs)工作。
3. 按一下要調查的工作 ID。如果查詢未建立工作，系統會顯示查詢 ID，且連結會停用。按一下有效的工作 ID，即可開啟「Job details」(工作詳細資料) 頁面，預設會顯示「Performance」(效能) 分頁。

### 可用的查詢資訊

為協助您診斷查詢效能，工作詳細資料中的「Performance」(效能) 分頁會彙整下列資訊和指標 (如適用)：

* **工作詳細資料**：工作相關資訊，包括工作 ID、建立時間、處理的位元組數和運算單元用量。詳情請參閱「[查看工作詳細資料](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)」。
* **執行記錄**：查詢的歷來執行作業清單，依查詢雜湊分組。您可以從這份清單中選取工作，直接與目前的工作比較。詳情請參閱「[比較工作](#compare-jobs)」。
* **執行圖**：查詢執行階段的示意圖。展開「Execution graph」(執行圖) 區段，檢查運算單元爭用、重組容量和資料輸入規模。詳情請參閱「[取得查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)」。

  以下範例顯示已啟用 SQL 文字對應的執行圖：
* **執行期間的系統負載**：工作執行期間分配的運算資源和預留設定摘要。

## 比較工作和系統，診斷效能迴歸

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要針對這項功能提供意見回饋或尋求支援，請傳送電子郵件至 [bq-performance-troubleshooting+feedback@google.com](mailto:bq-performance-troubleshooting+feedback@google.com)。

您可以使用成效比較工具，分析兩項查詢工作或兩個系統間隔之間的成效差異。分析結果會顯示查詢詳細資料、資源使用率變化，以及基準和目標環境之間有顯著差異的系統環境設定。

### 瞭解比較分析

比較工具會評估查詢層級指標和系統層級因素的成效。您可以開啟「僅顯示顯著差異」切換鈕，只顯示差異大於 20% 的指標。

顯著差異會以不同顏色標示，方便您找出問題：

* **綠色**：指標有所改善 (例如目標執行作業的查詢時間縮短)。
* **黃色**：指標降幅低於 20%。
* **紅色**：指標下降超過 20%。

### 比較兩項工作

如要比較基準工作與目標工作執行作業，請按照下列步驟操作：

1. 開啟「Jobs explorer」(工作探索工具) 頁面。

   [前往「Jobs explorer」(工作探索工具)](https://console.cloud.google.com/bigquery/admin/jobs-explorer?hl=zh-tw)
2. 選用：如要縮小顯示的工作範圍，請[篩選](#filter-jobs)工作。
3. 按一下基準工作的「工作 ID」，開啟「Job details」(工作詳細資料) 頁面，然後選取「Performance」(效能) 分頁標籤。
4. 在「Actions」(動作) 選單中，按一下「Compare Job」(比較工作)。
5. 在「Job one (baseline job)」(工作一 (基準工作)) 欄位中，按一下「Browse」(瀏覽)，開啟「Similar comparable jobs」(類似的可比較工作) 窗格。
6. 選取要與基準比較的工作，然後按一下「Compare」(比較)。
7. 選用：如要著重於重大效能迴歸，請開啟「Show only significant differences」(僅顯示顯著差異)。這樣一來，檢視畫面就只會顯示變異數大於 20% 的指標。

如要隨時變更要比較的任務，請按一下基準或目標任務欄位中的「Browse」(瀏覽)，然後從可比較的任務清單中選取新任務。

#### 查詢層級分析

比較兩項工作後，您可以查看「Query level analysis」(查詢層級分析) 專區，其中有三個分頁，可比較兩項工作的執行情況：

* **指標**：比較核心查詢指標，例如工作時間長度、運算單元時間、已處理的位元組數，以及未使用的加速器。
* **SQL text**：顯示兩項工作的 SQL 陳述式，並醒目顯示文字差異。
* **執行圖**：逐階段比較兩項工作的[執行圖](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)，找出瓶頸所在。

### 比較兩個系統間隔

管理員和分析師可以執行系統效能比較，分析更廣泛的環境指標。這項工具可讓您比較特定預留項目和專案的歷來間隔，瞭解使用率變化，並判斷效能降低的原因是來自工作負載內部或外部。

您可以透過下列任一方式，前往系統效能比較檢視畫面：

* 在「Job details」(工作詳細資料) 頁面[比較兩項工作](#compare-two-jobs)後，按一下「System level outputs」(系統層級輸出內容) 專區中的「View more」(查看更多)，即可查看系統比較詳細資料。
* 如果您使用 Gemini Cloud Assist 執行系統比較，Gemini Cloud Assist 會生成連結，開啟系統比較結果。

如要對不同時間範圍進行系統層級比較，請按照下列步驟操作：

1. 在「系統效能比較」檢視畫面中，按一下「系統」。
2. 按一下「Browse」(瀏覽)，然後選取預留項目或專案範圍，選取要分析效能的系統。
3. 定義比較時間範圍：
   * **目標間隔**：選取發生效能問題的日期和時間範圍，然後按一下「套用」。
   * 「Baseline Interval」(基準間隔)：選取要當做效能基準的參考日期和時間範圍，然後按一下「Apply」(套用)。

#### 系統層級分析

比較時間間隔後，檢視畫面會對應所選環境與其父項群組的使用率變化、並行變化和設定差異。這有助於判斷工作負載是否受到運算單元爭用或設定迴歸的影響。資料會在三個區塊中產生：

* **專案**：比較專案層級的並行工作數量、排入佇列的並行工作數量，以及總運算單元用量。
* **預留項目**：比較共用[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)的預留項目使用率、閒置運算單元共用情形和專案並行數量。
* **設定分析**：比較兩次執行作業的 Workload Manager 設定，例如預留大小上限和閒置運算單元借用規則。

## 使用代理成效疑難排解洞察

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或要求支援，請傳送電子郵件至 [bq-performance-troubleshooting+feedback@google.com](mailto:bq-performance-troubleshooting+feedback@google.com)。

監控管理工作或評估效能比較時，BigQuery 會將基礎觀測能力診斷功能與 Gemini Cloud Assist 整合，在您排解工作層級和系統層級異常狀況時，將對話窗格轉換為主動疑難排解助理。

洞察資訊會受到存取控管，如果權限不足，您收到的洞察資訊可能會受限。如要進一步瞭解權限，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

### 排解即時通訊效能問題

如要初始化情境感知疑難排解功能，並根據效能深入分析採取行動，請按照下列步驟操作：

1. 如要開啟 Gemini Cloud Assist 對話窗格，並自動載入相關工作或系統背景資訊，請執行下列任一操作：
   * 在「Jobs explorer」(工作探索工具) 或「Job history」(工作記錄) 頁面中，將滑鼠游標懸停在工作上，然後按一下該表格列中的 astrophotography\_mode「Gemini」。
   * 在「Workload management」(工作負載管理) 頁面中，將滑鼠游標懸停在預留項目上，然後按一下該表格列中的 astrophotography\_mode「Gemini」。
   * 在「Studio」、「Monitoring」或「Jobs explorer」中，按一下 astrophotography\_mode「Gemini」。
2. 以自然語言提交提示。例如，您可以要求 Gemini 說明工作執行速度緩慢的原因、分析特定工作統計資料、分析特定預留項目的效能、排解系統效能問題，或比較兩項類似歷來工作的效能差異。
3. 如果超出組織層級或預留項目層級的門檻，例如因並行執行中的專案數量突然增加，導致運算單元嚴重排隊，請查看產生的**效能深入分析**報表。這份報告會詳細說明重大瓶頸，例如：
   * **增加排入佇列的並行查詢**：並行查詢需求激增，超過軟性並行限制或預留運算單元分配量。
   * **專案並行數量增加**：追蹤高並行專案或主要使用者帳戶，瞭解哪些項目在共用預留項目或隨選配額中，造成系統負載。
4. 查看「Key Metrics Comparison」(主要指標比較) 表格，追蹤精確的數值差異，例如平均專案並行、佇列運算單元或預留項目運算單元數量上限的變化。
5. Gemini Cloud Assist 會生成可操作的交接連結，您可以直接透過這些連結執行內嵌解決方案。這些捷徑會將您重新導向至特定的產品內工具，並預先填入相關資訊，協助您解答問題及解決問題：

   * 「Edit reservation」(編輯預留項目)：開啟 Workload Manager 側邊面板，調整預留項目大小上限，或啟用進階資源調度功能。
   * **在工作探索工具中查看工作效能**：開啟特定工作的效能詳細資料分頁。
   * **在工作探索工具中比較工作效能**：並排比較兩項工作的效能。

## 定價

工作探索工具無須額外付費。用於填入這些圖表的查詢不會計費，也不會使用使用者擁有的預留項目中的運算單元。如果查詢處理的資料量過大，就會逾時。

## 後續步驟

* 瞭解[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)。
* 瞭解如何[購買運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw)。
* 瞭解如何[預估運算單元容量需求](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)。
* 瞭解如何[查看運算單元建議和深入分析](https://docs.cloud.google.com/bigquery/docs/slot-recommender?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]