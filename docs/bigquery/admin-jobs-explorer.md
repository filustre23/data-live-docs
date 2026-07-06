Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 監控工作

BigQuery 管理員可以透過 Google Cloud 控制台的管理工作探索器，監控整個機構的工作。工作探索器提供篩選器和排序選項，可協助您找出、比較及排解有問題的工作。您不必撰寫 `INFORMATION_SCHEMA` 查詢，即可查看工作詳細資料，例如擁有者、專案、運算單元使用情形、花費的時間等。

工作多層檢視可讓您執行下列操作：

* **篩選及識別工作。**依據工作狀態、時間長度、擁有者或運算單元使用情形等條件[套用篩選器](#filter-jobs)，在機構中搜尋特定查詢。
* **排解工作問題**。選取個別工作，即可在「工作詳細資料」頁面 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 上查看查詢執行圖表、SQL 文字和執行記錄。
* **比較成效**。[比較工作](#compare-jobs)
  ([預覽版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，找出顯著的指標差異，並解決潛在的效能問題。
* **取得 AI 協助。**[直接從工作探索器](#troubleshoot-with-ai) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 使用 Gemini Code Assist，分析工作統計資料或說明執行緩慢的查詢。

BigQuery 會透過下列`INFORMATION_SCHEMA`檢視畫面提供工作詳細資料和洞察資訊：

* [`INFORMATION_SCHEMA.JOBS_BY_PROJECT`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-organization?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_BY_USER`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-user?hl=zh-tw)

**注意：** 如果您使用機構限制，請參閱「[啟用 Google 擁有的資源存取權](https://docs.cloud.google.com/resource-manager/docs/organization-restrictions/additional-considerations?hl=zh-tw#google-owned-resources)」。

## 事前準備

如要使用 Gemini Code Assist [在 BigQuery (搶先版) 中排解工作問題](#troubleshoot-with-ai)，請參閱「[設定 Gemini Code Assist](https://docs.cloud.google.com/cloud-assist/set-up-gemini?hl=zh-tw)」，啟用 API 並授予必要角色。

### 必要的角色

如要取得使用作業探索工具監控作業所需的權限，請要求管理員授予您下列 IAM 角色：

* 在專案層級查看工作：
  專案的 [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`)
* 在機構層級查看工作：
  機構的 [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`)
* 依機構中的保留項目篩選：
  [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`)
  機構
* 查看工作詳細資料：
  在執行查詢的專案中，使用 [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`)
* 查看系統層級的詳細資料：
  管理專案的 [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備使用工作探索器監控工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用工作探索器監控工作，必須具備下列權限：

* 查看專案層級的工作：
  `bigquery.jobs.listAll`
  專案
* 查看機構層級的工作：
  `bigquery.jobs.listAll`
  在機構
* 依機構組織中的預留項目篩選：
  `bigquery.reservations.list`
  在機構組織中

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

**注意：** 只有在您定義機構時，才能使用機構檢視畫面。 Google Cloud

如要使用 Gemini Code Assist 排解工作問題，請參閱[使用 Gemini Code Assist 的其他 IAM 需求](https://docs.cloud.google.com/cloud-assist/iam-requirements?hl=zh-tw)。

## 篩選工作

如要篩選包含在 `INFORMATION_SCHEMA.JOBS*` 檢視區塊中的查詢工作，請執行下列操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Jobs explorer」(工作探索工具)。
3. 從「位置」清單中，選取要查看工作的地點。
4. 視需要套用選用的「篩選器」：

   * **工作範圍**：依工作可見度層級篩選工作，例如目前專案、機構和您的工作。您可以選擇查看目前專案、整個機構或僅限您啟動的工作。
   * **狀態**：依目前執行狀態篩選工作，例如已完成、發生錯誤、有效和已加入佇列。這有助於您識別進行中或失敗的工作。
   * **工作類別**：依執行的作業類型篩選工作，例如用於即時資料處理的標準 SQL 查詢或持續查詢。
   * **工作建立原因**：根據 BigQuery 建立工作的原因篩選工作，例如查詢超出逾時時間，或產生的結果過大，無法以單一回應傳回。
   * **工作優先順序**：依工作執行優先順序篩選工作，例如互動式或批次工作。
   * **工作 ID**：依工作的專屬英數 ID 篩選特定工作。
   * **擁有者**：依啟動作業的使用者或服務帳戶電子郵件地址篩選作業。
   * **專案 ID**：篩選在特定專案中執行的工作。只有在「工作範圍」設為「機構」時，才能使用這個篩選器。
   * **預留項目 ID**：篩選使用特定預留項目運算單元的工作。這有助於監控不同工作負載耗用預留容量的情況。
   * **使用時間超過**：篩選使用時間超過指定毫秒數的工作。這是用來找出耗用大量資源查詢的關鍵指標。
   * **時間長度超過**：篩選完成時間超過指定時間長度的工作。您可以使用這項功能，找出執行速度低於預期的查詢。
   * **處理的位元組數超過**：篩選掃描資料量超過指定量的作業。這有助於找出可能導致資料處理費用偏高的查詢。
   * **查詢洞察**：篩選 BigQuery 判定有特定效能問題的工作，例如時段爭用、超出記憶體隨機存取容量，以及資料輸入規模變化。
   * **查詢雜湊**：篩選具有特定查詢雜湊的工作。查詢雜湊可識別查詢的邏輯，並忽略註解、參數值、使用者定義函式和常值中的差異，協助您找出相同查詢邏輯的所有執行作業。如果成功執行非快取命中項目的 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 查詢，就會顯示這個欄位。
   * **標籤**：根據您或貴機構附加至工作的自訂中繼資料標籤篩選工作。方便您依部門或應用程式分類及追蹤工作。

## 排解工作成效問題

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-performance-troubleshooting+feedback@google.com](mailto:bq-performance-troubleshooting+feedback@google.com)。

如要診斷及排解查詢問題，您可以在「工作詳細資料」頁面查看執行指標、SQL 文字和歷來效能差異。

### 查看工作詳細資料

如要查看工作的詳細資料並分析查詢執行作業，請按照下列步驟操作：

1. 前往「Jobs explorer」(工作探索工具) 頁面。

   [前往「Jobs explorer」](https://console.cloud.google.com/bigquery/admin/jobs-explorer?hl=zh-tw)
2. 選用：如要縮小顯示的工作範圍，請[篩選](#filter-jobs)工作。
3. 按一下要調查的工作 ID。如果查詢未建立工作，系統會顯示查詢 ID，但連結會停用。按一下有效的工作 ID，即可開啟「工作詳細資料」頁面，並預設顯示「成效」分頁。

### 可用的查詢資訊

為協助您診斷查詢效能，作業詳細資料中的「效能」分頁會視情況彙整下列資訊和指標：

* **工作詳細資料**：工作相關資訊，包括工作 ID、建立時間、處理的位元組數和運算單元使用量。詳情請參閱「[查看工作詳細資料](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)」。
* **執行記錄**：查詢的歷史執行作業清單，依查詢雜湊分組。你可以從這份清單中選取工作，直接與目前的工作進行比較。詳情請參閱[比較工作](#compare-jobs)。
* **執行圖**：以視覺化方式呈現查詢執行階段。展開「執行圖」部分，檢查時段爭用、隨機播放容量和資料輸入規模。詳情請參閱「[取得查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)」。

  以下範例顯示已啟用 SQL 文字對應的執行圖：
* **執行期間的系統負載**：工作執行期間分配的運算資源和預留設定摘要。

## 比較作業和系統，診斷效能回歸問題

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-performance-troubleshooting+feedback@google.com](mailto:bq-performance-troubleshooting+feedback@google.com)。

您可以透過成效比較工具，分析兩個查詢作業或兩個系統間隔的成效差異。分析結果會顯示查詢詳細資料、資源用量變化，以及基準和目標環境之間差異顯著的系統環境設定。

### 瞭解比較分析

比較工具會評估查詢層級指標和系統層級因素的成效。您可以開啟「僅顯示顯著差異」切換鈕，將檢視畫面限制為變異數大於 20% 的指標。

系統會以不同顏色標示顯著差異，方便您掃描問題：

* **綠色**：指標有所改善 (例如目標執行中的查詢時間縮短)。
* **黃色**：指標下降不到 20%。
* **紅色**：指標降幅超過 20%。

### 比較兩項工作

如要比較基準工作與目標工作執行作業，請按照下列步驟操作：

1. 開啟「Jobs explorer」(工作探索工具) 頁面。

   [前往「Jobs explorer」](https://console.cloud.google.com/bigquery/admin/jobs-explorer?hl=zh-tw)
2. 選用：如要縮小顯示的工作範圍，請[篩選](#filter-jobs)工作。
3. 按一下基準工作的工作 ID，開啟「工作詳細資料」頁面，然後選取「成效」分頁標籤。
4. 在「動作」選單中，按一下「比較工作」。
5. 在「Job one (baseline job)」(工作一 (基準工作)) 欄位中，按一下「Browse」(瀏覽)，開啟「Similar comparable jobs」(類似可比較的工作) 窗格。
6. 選取要與基準比較的目標工作，然後按一下「比較」。
7. 選用：如要著重於重大成效衰退，請開啟「僅顯示顯著差異」。這樣一來，系統只會顯示差異大於 20% 的指標。

如要隨時變更比較的工作，請按一下基準或目標工作欄位中的「瀏覽」，然後從可比較的工作清單中選取新工作。

#### 查詢層級分析

比較兩項工作後，您可以查看「查詢層級分析」部分，比較兩個工作執行項目在下列三個分頁中的差異：

* **指標**：比較核心查詢指標，例如工作時間長度、運算單元時間、已處理的位元組數和未使用的加速器。
* **SQL 文字**：顯示兩項工作的 SQL 陳述式，並醒目顯示文字差異。
* **執行圖表**：比較兩個作業的[執行圖表](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw) (以階段為單位)，找出發生瓶頸的位置。

### 比較兩個系統間隔

管理員和分析師可以執行系統效能比較，分析更廣泛的環境指標。這項工具可讓您比較特定預訂和專案的歷史間隔，瞭解使用率變化，並判斷效能下降的原因是工作負載內部還是外部。

您可以透過下列任一方式前往系統效能比較檢視畫面：

* 在「Job details」(工作詳細資料) 頁面中[比較兩項工作](#compare-two-jobs)後，按一下「System level outputs」(系統層級輸出) 區段中的「View more」(查看更多)，即可查看系統比較詳細資料。
* 如果使用 Gemini Cloud Assist 執行系統比較，Gemini Cloud Assist 會產生連結，開啟系統比較結果。

如要比較不同時間範圍的系統層級資料，請按照下列步驟操作：

1. 在「系統效能比較」檢視畫面中，按一下「系統」。
2. 按一下「瀏覽」，然後選取預留項目或專案範圍，即可選取要分析成效的系統。
3. 定義比較時間範圍：
   * **目標間隔**：選取發生成效問題的日期和時間範圍，然後按一下「套用」。
   * **基準間隔**：選取做為效能基準的參考日期和時間範圍，然後按一下「套用」。

#### 系統層級分析

比較間隔後，檢視畫面會顯示所選環境與父項群組的利用率變化、並行差異和設定差異。這有助於判斷工作負載是否受到時段爭用或設定回歸的影響。資料會按以下三個區塊分類：

* **專案**：比較專案層級的工作並行數、排入佇列的並行數，以及總配額用量。
* **預留項目**：比較共用[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)的預留項目使用率、閒置運算單元共用和專案並行數。
* **設定分析**：比較兩次執行之間的工作負載管理設定，例如預訂大小上限和閒置時段借用規則。

## 使用代理程式成效疑難排解深入分析

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要提供意見或尋求這項功能的支援，請傳送電子郵件至 [bq-performance-troubleshooting+feedback@google.com](mailto:bq-performance-troubleshooting+feedback@google.com)。

監控管理工作或評估效能比較時，BigQuery 會整合基礎觀察診斷與 Gemini Cloud Assist，將即時通訊窗格變成主動式疑難排解助理，協助您排解工作層級和系統層級的異常狀況。

洞察資料的存取權受到控管，如果權限不足，您收到的洞察資料可能有限。如要進一步瞭解權限，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

### 排解即時通訊效能問題

如要初始化情境感知疑難排解功能，並根據效能深入分析採取行動，請按照下列步驟操作：

1. 如要開啟 Gemini Cloud Assist 對話窗格並自動載入相關工作或系統背景資訊，請執行下列其中一項操作：
   * 在「Jobs explorer」(工作探索工具) 或「Job history」(工作記錄) 頁面中，將游標懸停在工作上，然後點按該表格列中的 spark「Gemini」。
   * 在「工作負載管理」頁面中，將游標懸停在預留項目上，然後按一下該表格列中的 spark「Gemini」。
   * 在「Studio」、「Monitoring」或「Jobs explorer」中，按一下 spark「Gemini」。
2. 以自然語言提交提示。例如，要求 Gemini 說明作業執行緩慢的原因、分析特定作業統計資料、分析特定預留空間效能、排解系統效能問題，或是比較兩個類似歷來作業的效能差異。
3. 如果機構層級或預留層級的門檻遭到突破 (例如，由於有效專案並行作業量意外暴增，導致嚴重佇列)，請查看產生的「成效洞察」報表。這份報告會詳細說明下列重大瓶頸：
   * **排隊並行數增加**：並行查詢需求量暴增，超過並行軟性限制或預留配額。
   * **提高專案並行程度**：追蹤確切的高並行專案或頂尖使用者帳戶，這些專案或帳戶會推動共用預留容量或隨選配額的系統負載。
4. 查看「主要指標比較」表格，追蹤精確的數值差異，例如平均專案並行、佇列位置或預留位置上限的變化。
5. 透過 Gemini Cloud Assist 生成的可執行交接連結，直接執行內嵌解決方案。這些捷徑會將你重新導向至產品中的特定工具，並預先填入相關資訊，協助你解決問題：

   * **編輯預留項目**：開啟工作負載管理側邊面板，調整預留項目大小上限或啟用進階縮放功能。
   * **在工作探索工具中查看工作成效**：開啟特定工作的「成效詳細資料」分頁。
   * **在「工作探索」中比較工作效能**：並排比較兩項工作的效能。

## 定價

工作探索工具不收取額外費用。用於填入這些圖表的查詢不會產生費用，也不會使用使用者擁有的預留位置。如果查詢處理的資料量過大，就會逾時。

## 後續步驟

* 瞭解[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)。
* 瞭解如何[購買時段](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw)。
* 瞭解如何[估算運算單元容量需求](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)。
* 瞭解如何[查看運算單元建議和深入分析資料](https://docs.cloud.google.com/bigquery/docs/slot-recommender?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-07-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-07-05 (世界標準時間)。"],[],[]]