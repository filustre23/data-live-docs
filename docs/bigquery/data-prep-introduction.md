Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料準備功能總覽

在 BigQuery 使用 AI 輔助的資料準備功能，可大幅減少手動資料工作所需的時間和心力。資料準備功能會使用 Gemini in BigQuery 分析資料，並提供智慧建議，協助您清理、轉換及充實資料。Dataform 會排定這些資料準備作業。

## 優點

* Gemini 會根據情境生成轉換建議，縮短資料管道開發時間。
* 您可以在預覽畫面中驗證生成結果，並透過自動結構定義對應功能，取得資料品質清理和擴充建議。
* [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 可讓您使用持續整合、持續開發 (CI/CD) 程序，支援跨團隊協作，進行程式碼審查和原始碼控管。

## 資料準備進入點

您可以在「**BigQuery Studio**」頁面建立及管理資料準備作業 (請參閱「[啟動資料準備工作階段](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#open-data-prep-editor)」)。

**提示：**您也可以使用「Pipelines & Connections」(管道和連線) 頁面，透過[簡化的 BigQuery 專屬工作流程](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw)建立資料準備。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

在 BigQuery 資料準備中開啟資料表時，系統會使用您的憑證執行 BigQuery 工作。執行作業會從所選資料表建立範例資料列，並將結果寫入同一專案的暫存資料表。Gemini 會使用樣本資料和結構定義，生成資料準備建議，並顯示在資料準備編輯器中。

## 資料準備編輯器中的檢視畫面

資料準備作業會顯示為「BigQuery」**BigQuery**頁面上的分頁。每個分頁都有一系列子標籤，也就是資料準備*檢視畫面*，您可以在這裡開發及管理資料準備作業。

### 資料檢視

建立新的資料準備作業時，系統會開啟資料準備編輯器分頁，顯示資料檢視畫面，其中包含資料表的代表性樣本。如要查看現有的資料準備作業，請在資料準備管道的圖表檢視中，點選節點前往資料檢視畫面。

資料檢視可讓您執行下列操作：

* 與資料互動，形成資料準備步驟。
* 套用 Gemini 的建議。
* 在儲存格中輸入範例值，提升 Gemini 建議的品質。

在表格的每一欄上方，統計資料剖析 (直方圖) 會顯示預覽列中各欄最高值的計數。

### 圖表檢視

圖表檢視畫面會以視覺化方式呈現資料準備作業。開啟資料準備作業時，這個頁面會顯示在控制台「BigQuery」**BigQuery**頁面的分頁中。圖表會顯示資料準備管道中所有步驟的節點。您可以選取圖表上的節點，設定該節點代表的資料準備步驟。

### 結構定義檢視畫面

資料準備結構定義檢視畫面會顯示有效資料準備步驟的目前結構定義。顯示的結構定義與資料檢視中的資料欄相符。

在結構定義檢視畫面中，您可以執行專屬的結構定義作業，例如移除資料欄，這也會在「Applied steps」(已套用的步驟) 清單中建立步驟。

## Gemini 提供的建議

Gemini 會根據情境提供建議，協助您完成下列資料準備工作：

* 套用轉換和資料品質規則
* 標準化及充實資料
* 自動對應結構定義

每項建議都會顯示在資料準備編輯器的建議清單資訊卡中。資訊卡包含下列資訊：

* 步驟的高階類別，例如「Keep rows」(保留資料列) 或「Transformation」(轉換)
* 步驟說明，例如「**如果 `COLUMN_NAME` 不是 `NULL`，則保留資料列**」
* 用於執行步驟的對應 SQL 運算式

您可以預覽、編輯或套用建議資訊卡，或微調建議。你也可以手動新增步驟。詳情請參閱「[使用 Gemini 準備資料](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw)」。

如要微調 Gemini 的建議，請[提供範例](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#apply-suggestions)，說明要變更資料欄中的哪些內容。

## 資料取樣

BigQuery 會使用資料取樣功能，提供資料準備作業的預覽畫面。您可以在每個節點的資料檢視中查看樣本。

新增 BigQuery 標準資料表做為來源時，系統會使用 BigQuery [`TABLESAMPLE`](https://docs.cloud.google.com/bigquery/docs/table-sampling?hl=zh-tw) 函式準備資料。這個函式會建立 1 萬筆記錄的樣本。

新增檢視表或外部資料表做為來源時，系統會讀取前 100 萬筆記錄。系統會從這些記錄中選取 1 萬筆代表性記錄樣本。

範例中的資料不會自動重新整理。範例資料表會儲存為[快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)，並在大約 24 小時後過期。如要手動重新整理範例資料表，請參閱「[重新整理資料準備範例](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#refresh-data-prep-samples)」。

## 寫入模式

如要盡可能降低成本和處理時間，您可以變更寫入模式設定，以遞增方式處理來源的新資料。舉例來說，假設您在 BigQuery 中有一個資料表，每天都會插入記錄，而 Looker 資訊主頁必須反映變更的資料，則可排定 BigQuery 資料準備作業，以遞增方式從來源資料表讀取新記錄，並將這些記錄傳播至目的地資料表。

如要設定資料準備作業寫入目的地資料表的方式，請參閱「[透過漸進式處理資料，最佳化資料準備作業](https://docs.cloud.google.com/bigquery/docs/manage-data-preparations?hl=zh-tw#optimize)」。

支援的寫入模式如下：

| 寫入模式選項 | 說明 |
| --- | --- |
| 完整重新整理 | 對所有來源資料執行資料準備步驟，然後完整重建目的地資料表。資料表會重新建立，而非截斷。寫入目的地資料表時，預設模式為完整重新整理。 |
| 附加 | 將資料準備作業中的所有資料，以額外資料列的形式插入目的地資料表。 |
| 異動項目 | 只將新的資料插入目的地資料表，或根據您選擇的增量資料欄，將變更的資料插入目的地資料表。資料準備作業會根據您選擇的遞增資料欄，選取最佳的變更記錄偵測機制。系統會為數值和日期時間資料類型挑選最大值，並為類別型資料挑選不重複值。「最大值」只會插入指定資料欄值大於目的地資料表中同一資料欄最大值的記錄。「不重複」只會插入目的地資料表中，指定資料欄值不存在於相同資料欄現有值中的記錄。 |
| 新增或更新 | 使用指定的合併鍵合併資料列。如果目的地資料表中的現有資料列與輸入記錄的指定合併鍵相符，系統就會更新目的地資料表中該資料列的值。否則，系統會在目的地資料表中插入新資料列。 |

## 支援的資料準備步驟

BigQuery 支援下列類型的資料準備步驟：

| 步驟類型 | 說明 |
| --- | --- |
| 來源 | 選取要讀取的 BigQuery 資料表或新增彙整步驟時，系統會新增來源。 |
| 轉換 | 使用 SQL 運算式清理及轉換資料。系統會針對下列運算式顯示建議資訊卡：   * 類型轉換函式，例如 `CAST` * 字串函式，例如 `SUBSTR`、`CONCAT`、`REPLACE`、`UPPER`、`LOWER` 和 `TRIM` * 日期時間函式，例如 `PARSE_DATE`、`TIMESTAMP`、`EXTRACT` 和 `DATE_ADD` * JSON 函式，例如 `JSON_VALUE` 或 `JSON_QUERY`    您也可以在手動轉換步驟中使用任何有效的 BigQuery SQL 運算式。例如：   * 數字運算，例如將瓦特小時轉換為千瓦小時 * 陣列函式，例如 `ARRAY_AGG`、`ARRAY_CONCAT` 和 `UNNEST` * 視窗函式，例如 `ROW_NUMBER`、`LAG`、`LEAD`、`RANK` 和 `NTILE`     詳情請參閱「[新增轉換](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#add-transformation)」。 |
| 篩選器 | 透過 `WHERE` 子句語法移除資料列。新增篩選步驟時，您可以選擇將其設為驗證步驟。   詳情請參閱「[篩選資料列](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#filter-rows)」。 |
| 簡化 | 根據所選索引鍵和排序，從資料中移除重複的資料列。   詳情請參閱「[簡化資料](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#deduplicate)」。 |
| 驗證 | 將不符合驗證規則條件的資料列傳送至錯誤表格。如果資料不符合驗證規則，且未設定錯誤表格，資料準備作業就會在執行期間失敗。    詳情請參閱「[設定錯誤資料表並新增驗證規則](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#configure-validation)」。 |
| 加入 | 彙整兩個來源的值。資料表必須位於相同位置。 join 鍵資料欄必須屬於相同資料類型。資料準備作業支援下列彙整作業：   * 內部彙整 * 左側 join * 右側 join * 完整外部彙整 * Cross Join (如未選取 Join 鍵資料欄，則會使用 Cross Join)     詳情請參閱「[新增彙整作業](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#add-join)」。 |
| 目的地 | 定義輸出資料準備步驟的目的地。如果輸入的目的地資料表不存在，資料準備作業會以目前的結構定義資訊建立新的資料表。   詳情請參閱「[新增或變更目的地資料表](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#add-or-change-destination)」。 |
| 刪除欄 | 從結構定義中刪除資料欄。您可以在結構定義檢視畫面中執行這個步驟。   詳情請參閱「[刪除資料欄](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#delete-column)」。 |

## 排定資料準備作業

如要執行資料準備步驟，並將準備好的資料載入目的地資料表，請建立排程。您可以在資料準備編輯器中排定資料準備作業，並透過 BigQuery 的「Scheduling」(排程) 頁面管理這些作業。詳情請參閱「[排定資料準備作業](https://docs.cloud.google.com/bigquery/docs/orchestrate-data-preparations?hl=zh-tw)」。

## 使用資料準備工作建立管道

您可以建構由資料準備、SQL 查詢和筆記本工作組成的 BigQuery 管道。接著，您可以按照排程執行這些管道。詳情請參閱「[BigQuery 管道簡介](https://docs.cloud.google.com/bigquery/docs/workflows-introduction?hl=zh-tw)」。

## 控管存取權

使用 Identity and Access Management (IAM) 角色、BigQuery 和 Dataform Cloud KMS 金鑰加密，以及 VPC Service Controls，控管資料準備作業的存取權。

### IAM 角色和權限

準備資料的使用者和執行工作的 Dataform 服務帳戶，都必須具備 IAM 權限。詳情請參閱「[必要角色](https://docs.cloud.google.com/bigquery/docs/manage-data-preparations?hl=zh-tw#required-roles)」和「[設定 Gemini for BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)」。

### 使用 Cloud KMS 金鑰加密

在 BigQuery 中，使用預設的客戶自行管理 Cloud KMS 金鑰，在資料集或專案層級加密資料。詳情請參閱「[設定資料集預設金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#dataset_default_key)」和「[設定專案預設金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#project_default_key)」。

根據預設，您可以使用 [Dataform Cloud KMS 金鑰](https://docs.cloud.google.com/dataform/docs/cmek?hl=zh-tw#set-default-key)，在專案層級加密管道程式碼。

### VPC Service Controls 範圍

如果您使用 VPC Service Controls，則必須設定 perimeter，保護 Dataform 和 BigQuery。詳情請參閱 [BigQuery](https://docs.cloud.google.com/vpc-service-controls/docs/supported-products?hl=zh-tw#table_bigquery) 和 [Dataform](https://docs.cloud.google.com/vpc-service-controls/docs/supported-products?hl=zh-tw#dataform) 的 VPC Service Controls 限制。

### 建立資料準備時授予的角色

建立資料準備時，BigQuery 會授予您該資料準備的 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。凡是具備 Google Cloud 專案 Dataform 管理員角色的使用者，都擁有該專案中所有資料準備作業的擁有者存取權。如要覆寫這項行為，請參閱「[在建立資源時授予特定角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-specific-role)」。

## 限制

資料準備功能有下列限制：

* 特定資料準備作業的所有 BigQuery 資料準備來源和目的地資料集，都必須位於相同位置。詳情請參閱「[位置](#supported-locations)」。
* 編輯管道時，資料和互動內容會傳送至 Gemini 資料中心處理。詳情請參閱「[位置](#supported-locations)」。
* Assured Workloads 不支援 Gemini in BigQuery。
* BigQuery 資料準備功能不支援查看、比較或還原資料準備版本。
* Gemini 的回覆是根據您在開發資料準備管道時提供的資料集樣本。詳情請參閱「[Gemini for Google Cloud 如何使用您的資料](https://docs.cloud.google.com/gemini/docs/discover/data-governance?hl=zh-tw)」一文，以及 [Gemini for Google Cloud 『早鳥測試者計畫』](https://cloud.google.com/trusted-tester/gemini-for-google-cloud-preview?hl=zh-tw)條款。
* BigQuery 資料準備功能沒有專屬 API，如要瞭解必要的 API，請參閱「[設定 Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)」。

## 位置

資料處理工作會執行並儲存在來源資料集的位置。如果指定[存放區位置](https://docs.cloud.google.com/dataform/docs/manage-repository?hl=zh-tw#configure-workflow-settings)，則必須與來源資料集位置相同。

資料準備程式碼的儲存區域可以與工作執行區域不同。

Google Cloud 專案中的所有新程式碼資產都會使用預設區域。資產建立後，就無法變更區域。

**重要事項：**如果在建立程式碼資產時變更區域，該區域會成為後續所有程式碼資產的預設區域。現有程式碼資產不受影響。

如要設定新程式碼資產的預設區域，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder Files」(檔案)，開啟檔案瀏覽器：
3. 按一下專案名稱旁的 more\_vert「View files panel actions」(查看檔案面板動作) >「Switch code region」(切換程式碼區域)。
4. 選取要設為預設值的程式碼區域。
5. 按一下「儲存」。

如要查看支援的地區清單，請參閱「[BigQuery Studio 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqstudio-loc)」。

在開發和執行期間，BigQuery 資料處理作業一律會在來源資料集的位置執行。如要瞭解 Gemini in BigQuery 處理資料的位置，請參閱「[Gemini in BigQuery 處理資料的位置](https://docs.cloud.google.com/bigquery/docs/gemini-locations?hl=zh-tw)」。

## 定價

執行資料準備作業和建立資料預覽範例時，會使用 BigQuery 資源，費用依 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)所示費率計算。

資料準備功能包含在 [Gemini in BigQuery 定價](https://cloud.google.com/products/gemini/pricing?hl=zh-tw#gemini-in-bigquery-pricing)中。詳情請參閱「[設定 Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[透過 Gemini in BigQuery 準備資料](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw)。
* 瞭解如何[手動或排定執行資料準備作業](https://docs.cloud.google.com/bigquery/docs/orchestrate-data-preparations?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-08 (世界標準時間)。"],[],[]]