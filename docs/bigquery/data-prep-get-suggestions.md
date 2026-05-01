* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Gemini 準備資料

本文說明如何使用 Gemini 的 SQL 程式碼建議，在 BigQuery 資料準備中清理及轉換資料。

詳情請參閱「[BigQuery 資料準備總覽](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw)」一文。

## 事前準備

* [設定 Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)。
* 授予[必要的 Identity and Access Management (IAM) 角色和權限](https://docs.cloud.google.com/bigquery/docs/manage-data-preparations?hl=zh-tw#required-roles)。

## 啟動資料準備工作階段

建立新的資料準備作業、從現有資料表或 Cloud Storage/Google 雲端硬碟檔案開始，或是開啟現有的資料準備作業，即可開啟 BigQuery 資料準備編輯器。如要進一步瞭解建立資料準備作業時會發生什麼情況，請參閱「[資料準備進入點](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw#entry-points)」。

在 **BigQuery** 頁面中，您可以透過下列方式前往資料準備編輯器：

### 新建

如要在 BigQuery 中建立新的資料準備作業，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。  
   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 前往「建立新項目」清單，然後按一下「資料準備」。
   資料準備編輯器會顯示在新的未命名資料準備分頁中。
3. 在編輯器的搜尋列中輸入表格名稱或關鍵字，然後選取表格。系統會開啟資料準備編輯器，並在「資料」分頁中顯示資料預覽畫面，以及 Gemini 提供的初始資料準備建議。
4. 選用：如要簡化檢視畫面，請依序點選「全螢幕」，開啟全螢幕模式。
5. 選用：如要查看資料準備詳細資料、版本記錄、新增註解或回覆現有註解，請使用工具列。

### 從表格建立

如要從現有資料表建立新的資料準備作業，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。  
   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 按一下資料表名稱旁的 more\_vert，然後依序點選「動作」**>「在以下項目中開啟」>「資料準備」**。系統會開啟資料準備編輯器，並在「資料」分頁中顯示資料預覽畫面，以及 Gemini 提供的初步資料準備建議。
5. 選用：如要簡化檢視畫面，請依序點選「全螢幕」，開啟全螢幕模式。
6. 選用：如要查看資料準備詳細資料、版本記錄、新增註解或回覆現有註解，請使用工具列。

### 從檔案建立

如要從 Cloud Storage 或 Google 雲端硬碟中的檔案建立新的資料準備作業，請按照下列步驟操作：

#### 載入檔案

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。  
   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「建立新項目」清單中，按一下「資料準備」。資料準備編輯器會顯示在新的未命名資料準備分頁中。
3. 在資料來源清單中，按一下「Google Cloud Storage」或「Google 雲端硬碟」。「準備資料」對話方塊隨即開啟。
4. 在「來源」部分中，選取檔案：
   * **Cloud Storage**：從 Cloud Storage 值區選取檔案，或輸入來源路徑。舉例來說，輸入 CSV 檔案的路徑：
     `STORAGE_BUCKET_NAME/FILE_NAME.csv`.
     支援萬用字元搜尋，例如 `*.csv`。
   * **Google 雲端硬碟**：輸入 URI，選取 Google 雲端硬碟中的檔案。如要載入部分資料，可以輸入特定工作表名稱和範圍。**注意：**如果使用 Google 雲端硬碟做為資料來源，您必須使用服務帳戶[執行或排定資料準備作業](https://docs.cloud.google.com/bigquery/docs/orchestrate-data-preparations?hl=zh-tw)。這項作業不支援終端使用者憑證。您也必須與服務帳戶共用 Google 雲端硬碟檔案。

   系統會自動偵測檔案格式。支援的格式包括 Avro、CSV、JSONL、ORC 和 Parquet。其他相容的檔案類型 (例如 DAT、TSV 和 TXT) 會以 CSV 格式讀取。「Google 雲端硬碟」選項也支援 Google 試算表格式。
5. 定義要上傳檔案的外部暫存資料表。在「暫存資料表」部分，輸入新資料表的專案、資料集和資料表名稱。
6. 在「Schema」(結構定義) 區段中，查看結構定義。
   Gemini 會檢查檔案中的資料欄名稱。如果找不到任何內容，系統會提供建議。  
     
    根據預設，資料準備檔案會將資料載入為字串。您可以在[準備檔案資料](#prepare-file-data)時，定義更具體的資料類型。
7. 選用：在「進階選項」中，您可以新增更多資訊，例如工作失敗前允許的錯誤數量。Gemini 會根據檔案內容提供其他選項。
8. 選用：如要在資料準備編輯器中預覽新的暫存表，請選取「產生預覽」。
9. 點按「Create」(建立)。系統會開啟檔案的資料準備編輯器，並在「資料」分頁中顯示資料預覽畫面，以及 Gemini 提供的初始資料準備建議。
10. 選用：如要簡化檢視畫面，請依序點選「全螢幕」，開啟全螢幕模式。
11. 選用：如要查看資料準備詳細資料、版本記錄、新增註解或回覆現有註解，請使用工具列。

#### 準備檔案

在資料檢視畫面中，按照下列步驟準備您載入的暫存資料：

1. 選用：瀏覽轉換建議的建議清單，或選取資料欄並為其產生建議，為相關資料欄定義更強大的資料類型。
2. 選用：定義驗證規則。詳情請參閱「[設定錯誤資料表並新增驗證規則](#configure-validation)」。
3. [新增目的地資料表](#add-or-change-destination)。
4. 如要將資料載入目的地資料表，請[執行資料準備作業](#run-data-prep)。
5. 選用：[排定資料準備作業的執行時間](https://docs.cloud.google.com/bigquery/docs/orchestrate-data-preparations?hl=zh-tw)。
6. 選用步驟：[透過遞增處理資料的方式，最佳化資料準備作業](https://docs.cloud.google.com/bigquery/docs/manage-data-preparations?hl=zh-tw#optimize)。

### 開啟現有檔案

如要開啟現有資料準備作業的編輯器，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。  
   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，點選專案名稱，然後按一下「資料準備」。
4. 選取現有的資料準備作業。系統會顯示資料準備管道的圖表檢視畫面。
5. 選取圖表中的其中一個節點。系統會開啟資料準備編輯器，並在「資料」分頁中顯示資料預覽畫面，以及 Gemini 提供的初步資料準備建議。
6. 選用：如要簡化檢視畫面，請依序點選「全螢幕」，開啟全螢幕模式。
7. 選用：如要查看資料準備詳細資料、版本記錄、新增註解或回覆現有註解，請使用工具列。

   「註解」工具列功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。如要提供意見或尋求這項功能的支援，請傳送電子郵件至 [bqui-workspace-pod@google.com](mailto:bqui-workspace-pod@google.com)。

## 新增資料準備步驟

您會逐步準備資料。您可以預覽或套用 Gemini 建議的步驟。你也可以改善建議，或套用自己的步驟。

## 套用並改善 Gemini 建議

開啟資料表適用的資料準備編輯器時，Gemini 會檢查載入的資料表資料和結構定義，並生成篩選器和轉換建議。建議會顯示在「步驟」清單的資訊卡中。

下圖顯示您可以在哪裡套用及改善 Gemini 建議的步驟：

如要套用 Gemini 建議做為資料準備步驟，請按照下列步驟操作：

1. 在資料檢視畫面中，按一下資料欄名稱或特定儲存格。
   Gemini 會產生篩選和轉換資料的建議。
2. 選用：如要改善建議，請編輯表格中一到三個儲存格的值，示範資料欄中的值應為何種格式。舉例來說，請輸入您要套用至所有日期的格式。
   Gemini 會根據變更生成新的建議。

   **注意：** 系統不會儲存您對資料的範例變更。

   下圖顯示如何編輯值，以改善 Gemini 建議的步驟：
3. 選取建議卡片。

   1. 選用：如要預覽建議卡片的結果，請按一下「預覽」。
   2. 選用：如要使用自然語言修改建議資訊卡，請按一下「編輯」。
4. 按一下「套用」。

## 使用自然語言或 SQL 運算式新增步驟

如果現有建議不符合需求，請新增步驟。選擇資料欄或步驟類型，然後以自然語言描述所需內容。

### 新增轉換

1. 在資料或結構定義檢視中，選擇「轉換」選項。你也可以選擇資料欄或新增範例，協助 Gemini 瞭解資料轉換方式。
2. 在「Description」(說明) 欄位輸入提示詞，例如 `Convert the state
   column to uppercase`。
3. 依序按一下「傳送」
   「傳送」。

   Gemini 會根據提示詞生成 SQL 運算式和新的說明。
4. 在「目標資料欄」清單中，選取或輸入資料欄名稱。
5. 選用步驟：如要更新 SQL 運算式，請修改提示並按一下「傳送」，或手動輸入 SQL 運算式。
6. 選用：按一下「預覽」，然後檢查步驟。
7. 按一下「套用」。

### 攤平 JSON 資料欄

如要更輕鬆地存取及分析鍵/值組合，請將 JSON 欄位扁平化。舉例來說，如果有名為 `user_properties` 的 JSON 資料欄包含 `country` 和 `device_type` 鍵，將這個資料欄扁平化後，`country` 和 `device_type` 就會擷取到各自的頂層資料欄，方便您直接用於分析。

Gemini for BigQuery 建議的作業只會從 JSON 的頂層擷取欄位。如果這些擷取的欄位包含更多 JSON 物件，您可以在額外步驟中將其扁平化，以存取內容。

1. 在 JSON 來源資料表的資料檢視畫面中，選擇資料欄或儲存格。
2. 按一下「平坦化」即可生成建議。
3. 選用：如要更新 SQL 運算式，可以手動輸入 SQL 運算式。
4. 選用：按一下「預覽」，然後檢查步驟。
5. 按一下「套用」。

扁平化作業的行為如下：

* 選取含有 JSON 的儲存格或欄後，資料檢視畫面會顯示「扁平化」選項。點選「新增步驟」時，預設不會顯示這個選項。
* 如果所選資料列中沒有 JSON 金鑰，產生的建議就不會包含該金鑰。如果資料經過平坦化處理，這個問題可能會導致部分資料欄遭到排除。
* 如果資料欄名稱在扁平化期間發生衝突，重複的資料欄名稱會以 `_<i>` 格式結尾。舉例來說，如果已有名稱為 `address` 的資料欄，則新的扁平化資料欄名稱為 `address_1`。
* 扁平化資料欄名稱會遵循 BigQuery 的[資料欄命名慣例](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_names)。
* 如果將 JSON 金鑰欄位留空，預設的資料欄名稱格式為 `f<i>_`。

### 將 `RECORD` 或 `STRUCT` 欄攤平

如要更輕鬆地存取及分析巢狀欄位，請使用 `RECORD` 或 `STRUCT` 資料類型將資料欄扁平化。舉例來說，如果 `event_log` 記錄包含 `timestamp` 和 `action` 欄位，將這項記錄扁平化會將 `timestamp` 和 `action` 擷取至各自的頂層資料欄，方便您直接轉換這些資料欄。

這個程序會從記錄中擷取所有巢狀資料欄 (最多 10 個層級)，並為每個資料欄建立新資料欄。系統會將父項資料欄名稱與巢狀欄位名稱合併，並以底線分隔，藉此建立新的資料欄名稱 (例如 `PARENT-COLUMN-NAME_FIELD-NAME`)。原始資料欄會遭到捨棄。如要保留原始資料欄，可以從「已套用的步驟」清單中[刪除](#delete-applied-step)「Drop column」步驟。

如要將記錄扁平化，請按照下列步驟操作：

1. 在來源資料表的資料檢視畫面中，選擇記錄資料欄。
2. 按一下「平坦化」即可生成建議。
3. 選用：如要更新 SQL 運算式，可以手動輸入 SQL 運算式。
4. 選用：按一下「預覽」，然後檢查步驟。
5. 按一下「套用」。

**注意：** 記錄攤平不會展開記錄中的巢狀 JSON 物件或重複欄位 (陣列)。如要存取這些欄位的內容，必須在個別步驟中將這些欄位攤平。

### 拆分巢狀陣列

取消巢狀結構會將陣列中的每個元素擴展為自己的資料列，並將其他原始資料欄值複製到每個新資料列。這項動作有助於分析含有任意數量元素 (例如 API 回應清單) 的陣列資料欄。

您可以取消巢狀結構的資料欄類型如下：

* **`ARRAY` 資料類型：**會取消巢狀結構，改為陣列基本類型的元素。舉例來說，`ARRAY<STRUCT<...>>` 取消巢狀結構會產生 `STRUCT` 類型的元素。
* **`JSON` 資料欄：**將資料欄中的 JSON 陣列拆分為 `JSON` 類型的元素。

取消巢狀陣列時，系統會建立包含取消巢狀元素的資料欄。根據預設，系統會捨棄原始陣列資料欄。如要保留原始資料欄，請從「已套用的步驟」清單中[刪除](#delete-applied-step)「捨棄資料欄」步驟。

如要取消巢狀陣列，請按照下列步驟操作：

1. 在來源資料表的資料檢視畫面中，選擇 `ARRAY` 資料欄。
2. 按一下「取消巢狀結構」即可生成建議。
3. 選用：如要更新 SQL 運算式，可以手動輸入 SQL 運算式。
4. 選用：按一下「預覽」，然後檢查步驟。
5. 按一下「套用」。

**注意：** 如果原始資料表中的資料欄與取消巢狀結構的陣列中的資料欄同名，取消巢狀結構的陣列資料欄可能會發生錯誤。如要解決這個問題，請先重新命名原始資料表中衝突的資料欄，再執行取消巢狀結構作業。

### 篩選表格列

如要新增可移除資料列的篩選器，請按照下列步驟操作：

1. 在資料或結構定義檢視畫面中，選擇「篩選器」選項。你也可以選擇欄，協助 Gemini 瞭解資料篩選條件。
2. 在「Description」(說明) 欄位輸入提示詞，例如 `Column ID should not
   be NULL`。
3. 按一下「生成」。
   Gemini 會根據提示詞生成 SQL 運算式和新的說明。
4. 選用：如要更新 SQL 運算式，請修改提示並按一下「傳送」，或手動輸入 SQL 運算式。
5. 選用：按一下「預覽」，然後檢查步驟。
6. 按一下「套用」。

#### 篩選運算式格式

篩選條件的 SQL 運算式會保留符合指定條件的資料列。這相當於 `SELECT … WHERE SQL_EXPRESSION` 陳述式。

舉例來說，如要保留資料欄 `year` 大於或等於 `2000` 的記錄，條件為 `year >= 2000`。

運算式必須遵循 [`WHERE` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#where_clause)的 BigQuery SQL 語法。

### 簡化資料

如要從資料中移除重複資料列，請按照下列步驟操作：

1. 在資料或結構定義檢視畫面中，選擇「重複資料刪除」選項。Gemini 會提供初步的重複內容刪除建議。
2. 選用：如要修正建議，請輸入新的說明，然後按一下「傳送」。
3. 選用：如要手動設定重複資料刪除步驟，請使用下列選項：
   * 在「記錄選擇」清單中，選取下列其中一個策略：
     + **第一個**：針對具有相同重複資料刪除鍵值的每一組資料列，這項策略會根據`ORDER BY`運算式選擇第一個資料列，並移除其餘資料列。
     + **最後**：針對具有相同重複資料刪除鍵值的每一組資料列，這項策略會根據 `ORDER BY` 運算式選擇最後一個資料列，並移除其餘資料列。
     + **任何**：針對具有相同重複資料刪除鍵值的每一組資料列，這項策略會從該組中選擇任一資料列，並移除其餘資料列。
     + **Distinct**：移除資料表中所有資料欄的重複資料列。
   * 在「重複資料刪除鍵」欄位中，選擇一或多個資料欄或運算式，以識別重複的資料列。當記錄選擇策略為「First」、「Last」或「Any」時，適用這個欄位。
   * 在「Order by expression」(排序依據運算式) 欄位中，輸入定義資料列順序的運算式。舉例來說，如要選擇最近一列，請輸入 `datetime DESC`。如要依名稱字母順序選擇第一列，請輸入 `last_name` 等欄名。運算式遵循與 BigQuery 中標準 [`ORDER BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#order_by_clause)相同的規則。只有在記錄選擇策略為「第一個」或「最後一個」時，才適用這個欄位。
4. 選用：按一下「預覽」，然後檢查步驟。
5. 按一下「套用」。

### 刪除資料欄

如要從資料準備作業中刪除一或多個資料欄，請按照下列步驟操作：

1. 在資料或結構定義檢視畫面中，選取要捨棄的資料欄。
2. 按一下「放棄」。系統會為已刪除的資料欄新增套用的步驟。

### 透過 Gemini 新增聯結作業

如要在資料準備期間，於兩個來源之間新增聯結作業步驟，請按照下列步驟操作：

1. 在資料準備節點的資料檢視畫面中，前往「建議」清單，然後按一下「聯結」選項。
2. 在「Add join」(新增聯結) 對話方塊中，按一下「Browse」(瀏覽)，然後選取聯結作業涉及的其他資料表 (稱為聯結的右側)。
3. 選用：選取要執行的[彙整作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)類型，例如**內部彙整**。
4. 查看下列欄位中 Gemini 生成的彙整索引鍵資訊：

   * **聯結說明**：聯結作業的 SQL 運算式自然語言說明。編輯說明並點選「傳送」後，Gemini 會建議新的 SQL 聯結條件。
   * **彙整條件**：彙整作業的 `ON` 子句中的 SQL 運算式。您可以使用 `L` 和 `R` 限定符，分別參照左側和右側的來源資料表。舉例來說，如要將左方資料表的 `customer_id` 欄與右方資料表的 `customer_id` 欄彙整，請輸入 `L.customerId = R.customerId`。這些限定詞不區分大小寫。

     **附註：** 如果「join 條件」欄位空白，系統會自動將 join 作業類型設為「cross join」，即使您在上一個步驟選取了不同的 join 類型也是如此。
5. 選用：如要調整 Gemini 的建議，請編輯「加入說明」欄位，然後按一下「傳送」。
6. 選用：如要預覽資料準備作業的聯結設定，請按一下「預覽」。
7. 按一下「套用」。

   系統會建立加入作業步驟。您選取的來源資料表 (聯結右側) 和聯結作業會反映在已套用步驟的清單中，以及資料準備作業圖表檢視畫面中的節點。

### 匯總資料

1. 在資料或結構定義檢視中，選擇「匯總」選項。
2. 在「Description」(說明) 欄位輸入提示詞，例如 `Find the total
   revenue for a region`。
3. 按一下 [傳送]。

   Gemini 會根據提示詞生成分組鍵和彙整運算式。
4. 選用：視需要編輯產生的分組鍵或彙整運算式。
5. 選用：您可以手動新增分組鍵和匯總運算式。

   * 在「分組鍵」欄位中，輸入資料欄名稱或運算式。如果留空，產生的資料表會有一列。如果您輸入運算式，則必須有別名 (`AS` 子句)，例如 `EXTRACT(YEAR FROM order_date) AS order_year`。不得重複。
   * 在「Aggregation expressions」(匯總運算式) 欄位中，輸入具有別名 (`AS` 子句) 的匯總運算式，例如 `SUM(quantity) AS total_quantity`。您可以輸入多個以半形逗號分隔的運算式。請勿輸入重複的內容。如需支援的匯總運算式清單，請參閱[匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw)。
6. 選用：按一下「預覽」，然後檢查步驟。
7. 按一下「套用」。

### 設定錯誤表格並新增驗證規則

您可以新增篩選器來建立驗證規則，將錯誤傳送至錯誤表格，或導致資料準備作業執行失敗。

#### 設定錯誤表格

如要設定錯誤表格，請按照下列步驟操作：

1. 在資料準備編輯器中，前往工具列並依序點選「更多」>「錯誤表格」。
2. 按一下「啟用錯誤表格」。
3. 定義資料表位置。
4. 選用：定義錯誤保留時長上限。
5. 按一下 [儲存]。

#### 新增驗證規則

如要新增驗證規則，請按照下列步驟操作：

1. 在資料或結構定義檢視畫面中，按一下「篩選器」選項。你也可以選擇資料欄，協助 Gemini 瞭解資料篩選條件。
2. 輸入步驟說明。
3. 以 `WHERE` 子句的形式輸入 SQL 運算式。
4. 選用：如要讓 SQL 運算式做為驗證規則，請選取「驗證失敗的資料列移至錯誤表格」核取方塊。您也可以按一下「更多」**> 錯誤表格**，將資料準備工具列中的篩選器變更為驗證。
5. 選用：按一下「預覽」，然後檢查步驟。
6. 按一下「套用」。

### 新增或變更目的地資料表

如要執行或排定資料準備作業，您必須先提供目的地資料表。如要為資料準備輸出內容新增或變更目的地資料表，請按照下列步驟操作：

1. 在資料或結構定義檢視中，按一下「建議」清單中的「目的地」。
2. 選取儲存目的地資料表的專案。
3. 選取其中一個資料集，或載入新的資料集。
4. 輸入目的地資料表。如果資料表不存在，資料準備作業會在第一次執行時建立新資料表。詳情請參閱「[寫入模式](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw#write-mode)」。
5. 選取資料集做為目的地資料集。
6. 按一下 [儲存]。

## 查看已套用步驟的資料樣本和結構定義

如要在資料準備的特定步驟中查看樣本和結構定義詳細資料，請執行下列操作：

1. 在資料準備編輯器中，前往「步驟」清單，然後按一下「已套用的步驟」。
2. 選取步驟。系統會顯示「資料」和「結構定義」分頁，並顯示這個步驟的資料樣本和結構定義。

## 編輯套用的步驟

如要編輯套用的步驟，請按照下列步驟操作：

1. 在資料準備編輯器中，前往「步驟」清單，然後按一下「已套用的步驟」。
2. 選取步驟。
3. 依序按一下步驟旁邊的 more\_vert 和「選單」**>「編輯」**。
4. 在「編輯套用的步驟」對話方塊中，您可以執行下列操作：
   * 編輯步驟說明。
   * 編輯說明並點選「傳送」，即可取得 Gemini 建議。
   * 編輯 SQL 運算式。
5. 在「目標資料欄」欄位中選取資料欄。
6. 選用：按一下「預覽」，然後檢查步驟。
7. 按一下「套用」。

## 刪除套用的步驟

如要刪除套用的步驟，請按照下列步驟操作：

1. 在資料準備編輯器中，前往「步驟」清單，然後按一下「已套用的步驟」。
2. 選取步驟。
3. 依序點選「更多」圖示 more\_vert
   **「選單」>「刪除」**。

## 執行資料準備作業

新增資料準備步驟、[設定目的地](#add-or-change-destination)並修正所有驗證錯誤後，您可以對資料樣本執行測試，也可以部署步驟並排定資料準備作業的執行時間。詳情請參閱「[安排資料準備作業](https://docs.cloud.google.com/bigquery/docs/orchestrate-data-preparations?hl=zh-tw)」。

## 重新整理資料準備範例

系統不會自動重新整理範例中的資料。如果資料準備作業的來源表格資料已變更，但準備作業的資料樣本未反映這些變更，請按一下「更多」**>「重新整理樣本」**。

## 後續步驟

* 瞭解如何[排定資料準備作業](https://docs.cloud.google.com/bigquery/docs/orchestrate-data-preparations?hl=zh-tw)。
* 瞭解如何[管理資料準備作業](https://docs.cloud.google.com/bigquery/docs/manage-data-preparations?hl=zh-tw)。
* 查看 [Gemini 版 BigQuery 的定價](https://cloud.google.com/products/gemini/pricing?hl=zh-tw#gemini-in-bigquery-pricing)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]