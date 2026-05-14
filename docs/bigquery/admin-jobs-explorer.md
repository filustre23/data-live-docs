Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用管理工作探索工具

BigQuery 管理員可以使用管理工作探索器，監控整個機構的工作活動。工作探索器也提供一系列篩選器和排序選項，可協助您排解問題並找出有問題的工作。工作探索器可讓您快速查看工作資訊 (例如擁有者、專案、時段用量、持續時間等)，不必深入瞭解 `INFORMATION_SCHEMA`，也不必撰寫 `INFORMATION_SCHEMA` 查詢。

您也可以選取個別工作，開啟[工作詳細資料頁面](#get-job-details)，其中提供執行圖、SQL 文字和執行記錄等查詢詳細資料，協助您診斷及排解查詢問題。您可以在這個頁面[比較兩項工作](#compare-jobs)，找出兩者之間的重大差異，並解決潛在的效能問題。

BigQuery 提供下列`INFORMATION_SCHEMA`檢視畫面，顯示工作詳細資料和洞察資訊：

* [`INFORMATION_SCHEMA.JOBS_BY_PROJECT`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-organization?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_BY_USER`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-user?hl=zh-tw)

**注意：** 如果您使用組織權限限制，請參閱「[啟用 Google 擁有的資源存取權](https://docs.cloud.google.com/resource-manager/docs/organization-restrictions/additional-considerations?hl=zh-tw#google-owned-resources)」一文。

## 必要的角色

如要取得使用管理工作探索器所需的權限，請要求系統管理員授予您機構或專案的 [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備使用管理工作探索工具所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用管理工作探索器，必須具備下列權限：

* 如要查看專案層級的資料：
  `bigquery.jobs.listAll`
  專案
* 如要查看機構層級的資料：
  `bigquery.jobs.listAll`
  在機構上
* 如要依貴機構的預訂記錄篩選：
  `bigquery.reservations.list`
  在機構上

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

**注意：** 只有在您定義 Google Cloud 機構時，才能使用這個機構檢視畫面。

## 篩選工作

如要篩選 `INFORMATION_SCHEMA.JOBS*` 檢視區塊中包含的查詢工作，請執行下列操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Jobs explorer」(工作探索工具)。
3. 從「位置」清單中，選取要查看工作的地點。
4. 視需要套用選用的「篩選器」：

   * **工作範圍**。例如目前的專案、機構和您的工作。
   * **狀態**。例如已完成、發生錯誤、進行中和已加入佇列。
   * **工作優先順序**：例如互動式或批次工作。
   * **工作 ID**。
   * **擁有者**。工作擁有者的電子郵件 ID (僅適用於工作範圍為專案或機構時)。
   * **專案 ID**。(僅適用於工作範圍為機構時)
   * **預訂 ID**。(僅適用於工作範圍為機構時)
   * **運算單元時間超過**。工作耗費的時間超過指定時段。
   * **持續時間超過**。工作時間超過指定時長。
   * **處理的位元組數超過**。處理的位元組數超過指定位元組數的工作。
   * **查詢洞察**。查詢洞察類型，例如時段競爭、超過記憶體重組容量，以及資料輸入規模調整。
   * **查詢雜湊**。查詢雜湊包含查詢的雜湊。這是十六進位 STRING 雜湊，會忽略註解、參數值、UDF 和常值。如果 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 查詢成功，但未命中快取，就會顯示這個欄位。
   * **標籤**。`key:value` 組合，可指派給工作。您可以透過鍵、值或 `key:value` 組合進行篩選。
   * **工作類別**。查詢類型，例如「標準」或「持續查詢」。

## 查看查詢執行詳細資料

如要查看工作的查詢執行詳細資料，請按照下列步驟操作：

1. 前往「Jobs explorer」(工作探索工具) 頁面。

   [前往「Jobs explorer」(工作探索工具)](https://console.cloud.google.com/bigquery/admin/jobs-explorer?hl=zh-tw)
2. 如要查看工作，請按一下「工作探索工具」。
3. [篩選工作](#filter-jobs)，查看受限的工作。
4. 按一下要查看查詢執行詳細資料的工作。
5. 在「查詢結果」窗格中，按一下「執行圖表」分頁標籤，即可查看工作的執行詳細資料。

如要瞭解如何解讀洞察資料，請參閱「[解讀查詢效能洞察資料](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#interpret_query_performance_insights)」。

## 取得 BigQuery 工作詳細資料

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-performance-troubleshooting+feedback@google.com](mailto:bq-performance-troubleshooting+feedback@google.com)。

在管理工作探索器中，您可以查看 BigQuery 詳細資料頁面。BigQuery 工作詳細資料頁面會將多項查詢詳細資料整合至一個頁面，協助您診斷及排解查詢問題。「效能」分頁會彙整查詢資訊，包括執行圖表、SQL 文字和執行記錄。

「效能」分頁也支援查詢比較，可讓您比較查詢的歷來用量，並分析及解決任何可能的效能下降問題。如要進一步瞭解如何比較工作，請參閱[比較工作](#compare-jobs)。

### 事前準備

如要取得處理 BigQuery 工作詳細資料和系統層級詳細資料所需的權限，請要求管理員在機構或專案中授予您下列 IAM 角色：

* 查看工作詳細資料：
  BigQuery 資源檢視者 (`roles/bigquery.resourceViewer`) - 執行查詢的專案
* 查看系統層級詳細資料：
  BigQuery 資源檢視者 (`roles/bigquery.resourceViewer`) - 管理專案

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備處理 BigQuery 工作詳細資料和系統層級詳細資料所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用 BigQuery 工作詳細資料和系統層級詳細資料，您必須具備下列權限：

* 如要查看專案層級的資料：
  `bigquery.jobs.listAll`
  專案
* 如要查看機構層級的資料：
  `bigquery.jobs.listAll`
  在機構上
* 如要依貴機構的預訂記錄篩選：
  `bigquery.reservations.list`
  在機構上

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 查看工作詳細資料

如要查看工作詳細資料頁面，請按照下列步驟操作：

1. 前往「Jobs Explorer」(工作探索工具) 頁面。

   [前往 Jobs Explorer](https://console.cloud.google.com/bigquery/admin/jobs-explorer?hl=zh-tw)
2. 選用：[篩選](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw#filter-jobs)工作機會，縮小顯示範圍。
3. 按一下要查看的工作 ID。如果查詢未建立工作，系統會顯示查詢 ID，並停用連結。如果是其他查詢，按一下工作 ID 會顯示「工作詳細資料」頁面。

系統預設會顯示「成效」分頁。你可以前往其他分頁，查看更多工作資訊。

### 可用的查詢資訊

下表說明「成效」分頁中提供的資訊和指標。

* **SQL 查詢**：建立這項工作的 SQL 查詢文字。
* **工作詳細資料**：工作相關資訊，包括工作 ID、建立時間、處理的位元組數等。詳情請參閱「[查看工作詳細資料](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)」。
* **效能差異**：與先前執行相同查詢時相比，這項作業的效能資訊。BigQuery 會比較目前的工作與過去執行的工作，找出處理的位元組數相近 (± 5%) 且工作時間最短的工作 (如有)。如果沒有這類過去的執行作業，BigQuery 會將目前的工作與過去 30 天的平均執行作業進行比較。如果沒有先前的執行作業，這個部分會指出系統找不到類似的工作可供比較。
* **執行記錄**：這項查詢的其他執行作業清單 (依查詢雜湊排序)。從這個面板中，您可以選取要與目前查看工作進行比較的工作。如要進一步瞭解如何比較工作，請參閱「[比較工作](#compare-jobs)」。
* **執行期間的系統負載**：BigQuery 用於執行工作的資源說明。包括這項工作使用的預訂設定資訊 (如適用)。
* **執行圖**：這項工作的執行圖。詳情請參閱「[取得查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)」。

## 比較工作

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-performance-troubleshooting+feedback@google.com](mailto:bq-performance-troubleshooting+feedback@google.com)。

您可以透過工作成效比較功能，比較基準工作與目標工作，並透過查詢分析功能，找出兩項工作之間差異顯著的詳細資料。這有助於排解兩個查詢工作之間潛在的效能問題。

比較兩個查詢時，請考量工作時間、時段時間和處理的位元組等重要詳細資料，以便最佳化查詢。

### 事前準備

如要取得處理 BigQuery 工作詳細資料和系統層級詳細資料所需的權限，請要求管理員在機構或專案中授予您下列 IAM 角色：

* 查看工作詳細資料：
  BigQuery 資源檢視者 (`roles/bigquery.resourceViewer`) - 執行查詢的專案
* 查看系統層級詳細資料：
  BigQuery 資源檢視者 (`roles/bigquery.resourceViewer`) - 管理專案

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備處理 BigQuery 工作詳細資料和系統層級詳細資料所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用 BigQuery 工作詳細資料和系統層級詳細資料，您必須具備下列權限：

* 如要查看專案層級的資料：
  `bigquery.jobs.listAll`
  專案
* 如要查看機構層級的資料：
  `bigquery.jobs.listAll`
  在機構上
* 如要依貴機構的預訂記錄篩選：
  `bigquery.reservations.list`
  在機構上

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 瞭解工作效能比較

以下各節說明「工作成效比較」頁面，以及該頁面提供的疑難排解資訊。

開啟「僅顯示顯著差異」切換鈕，即可只查看這兩個工作之間的所有指標顯著差異。

顯著差異會以綠色、黃色和紅色醒目顯示：

* **綠色**：變更朝正向發展。舉例來說，查詢時間越短越好，因此如果目標工作比基準工作更快完成，就會標示為綠色。
* **黃色**：變動方向為負值，但差異小於 20%。
* **紅色**：變更朝負面方向發展，且差異大於 20%。

#### 查詢層級分析

「查詢層級分析」窗格會說明兩個工作在查詢層級的差異。其中包含「指標」、「SQL 文字」和「執行圖表」三個分頁。

* 「指標」分頁會說明這兩項工作的查詢指標。使用這個分頁判斷工作時間、未使用的加速器和其他指標之間是否有差異。
* 「SQL text」(SQL 文字) 分頁會顯示建立作業的兩項 SQL 陳述式，並醒目顯示兩者之間的差異。使用這個分頁，判斷 SQL 陳述式變更是否影響工作效能。
* 「執行圖」分頁會比較這兩項作業的[執行圖](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)。使用這個分頁，判斷工作執行期間是否在任何階段發生差異。

#### 系統層級分析

「系統層級分析」窗格會說明可能影響系統層級這兩項工作的因素。其中包含三個部分：「專案」資料表、「預訂」資料表和「設定」資料表。

「系統層級分析」窗格會根據兩項查詢的差異，建議可改善的項目。

舉例來說，如果某項工作獲得的運算單元比先前的執行作業少，可能是因為系統的資源受限。如果出現這類訊息，請查看專案層級指標，確認專案整體是否分配到較少的時段。如果專案並未獲得較少的運算單元，則可能是專案層級發生爭用，例如工作並行數增加。如果專案收到的運算單元較少，請檢查預訂層級，找出任何限制。

* 「專案」表格會比較專案層級的這兩項工作。使用這個表格判斷是否能在專案層級進行最佳化。
* 「預留項目」表格會比較[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)層級的這兩項工作。使用這份表格找出兩項查詢之間預訂用量的差異，這些差異可能會影響工作效能。
* 「設定」表格會比較這兩項作業的預留設定。使用這份表格偵測預留項目設定的任何變更，這些變更可能導致效能受到影響。

### 比較兩項工作

如要比較兩項工作：

1. 前往「Jobs Explorer」(工作探索工具) 頁面。

   [前往 Jobs Explorer](https://console.cloud.google.com/bigquery/admin/jobs-explorer?hl=zh-tw)
2. 選用：[篩選](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw#filter-jobs)工作機會，縮小顯示範圍。
3. 按一下要查看及比較的初始工作 ID。系統隨即會顯示「工作詳細資料」頁面。
4. 按一下「成效」分頁標籤。
5. 按一下「比較工作」。
6. 在「Job one (baseline job)」(工作一 (基準工作)) 欄位中，按一下「Browse」(瀏覽)。系統隨即會顯示「類似的同類工作」面板。
7. 找出要與基準工作比較的工作，然後按一下「比較」。系統會顯示工作效能比較。
8. 如要只查看兩項工作之間的顯著差異，請開啟「僅顯示顯著差異」切換鈕。

#### 變更要比較的工作

如要變更比較的工作，請按照下列步驟操作：

1. 前往「工作效能比較」頁面。
2. 在「Job one (baseline job)」(工作一 (基準工作)) 欄位中，按一下「Browse」(瀏覽)。
3. 在「類似的同類工作」窗格中，找出要比較的工作，然後按一下「比較」。

## 定價

您無須額外付費，即可使用工作探索工具。用於填入這些圖表的查詢不會產生費用，也不會使用使用者擁有的預留項目中的運算單元。如果查詢處理的資料量過大，就會逾時。

## 後續步驟

* 瞭解[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)。
* 瞭解如何[購買時段](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw)。
* 瞭解如何[估算運算單元容量需求](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)。
* 瞭解如何[查看運算單元建議和深入分析資料](https://docs.cloud.google.com/bigquery/docs/slot-recommender?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]