Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 查詢計畫與時程 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

BigQuery 在查詢工作中內嵌了診斷查詢計畫和時間資訊。這與其他資料庫和分析系統中 `EXPLAIN` 等陳述式提供的資訊類似。這項資訊可從 [`jobs.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw) 等方法的回應中擷取。

如果是長時間執行的查詢，BigQuery 會定期更新這些統計資料。這些更新與工作狀態的輪詢頻率無關，但通常不會超過每 30 秒一次。此外，如果查詢作業未使用執行資源 (例如模擬測試要求或可從快取結果提供的結果)，就不會包含額外的診斷資訊，但可能會有其他統計資料。

## 背景

BigQuery 執行查詢時，會將 SQL 轉換為由「階段」組成的執行圖。階段是由「步驟」組成，這些基本作業會執行查詢的邏輯。BigQuery 採用大量分散式平行架構，可平行執行階段，縮短延遲時間。各階段之間是使用**重組** (一種快速分散式記憶體架構) 通訊。

查詢計畫會使用「工作單元」和「工作人員」這兩個詞彙，描述階段平行處理。在 BigQuery 的其他位置，您可能會看到「運算單元」一詞，這是查詢執行作業多個層面的抽象表示法，包括運算、記憶體和 I/O 資源。運算單元會並行執行階段的個別工作單位。頂層工作統計資料會根據這項抽象會計作業，使用 `totalSlotMs` 提供個別查詢費用。

查詢執行作業的另一項重要屬性是，BigQuery 可以在查詢執行期間修改查詢計畫。舉例來說，BigQuery 會導入*重新分區階段*，改善查詢工作站之間的資料分布狀況，進而提升平行處理能力並縮短查詢延遲時間。

除了查詢計畫外，查詢工作也會顯示**時間軸**，其中會列出已完成、待處理和作用中的工作單元。查詢可以同時有多個作用中工作站，各在不同的階段，因此時程主要是用來顯示查詢的整體進度。

## 使用 Google Cloud 控制台查看執行圖

在 [Google Cloud 控制台](https://console.cloud.google.com/bigquery?hl=zh-tw)中，按一下「執行作業詳細資料」按鈕，即可查看已完成查詢的查詢計畫詳細資料。

## 查詢計劃資訊

在 API 回應中，查詢計畫會以查詢階段清單的形式呈現。清單中的每個項目都會顯示各階段的總覽統計資料、詳細步驟資訊和階段時間分類。 Google Cloud 控制台不會顯示所有詳細資料，但 API 回應中可能會包含所有詳細資料。

### 瞭解執行圖表

在 Google Cloud 控制台中，按一下「執行圖」分頁標籤，即可查看查詢計畫詳細資料。

「執行圖表」面板的結構如下：

* 中間是**執行圖**。節點代表階段，邊緣則代表階段之間交換的隨機記憶體。
* 左側面板會顯示**查詢文字熱度圖**。顯示查詢執行的主要查詢文字，以及任何參照的檢視區塊。
* 右側面板會顯示查詢或階段詳細資料。

#### 瀏覽執行圖

執行圖會根據時段，為圖中的節點套用色彩配置，其中紅色越深的節點，相較於圖中的其他階段，佔用的時段就越多。

如要瀏覽執行圖表，可以：

* 按住圖表背景並拖曳，即可平移至圖表的不同區域。
* 使用滑鼠滾輪縮放圖表。
* 按住右上角的**迷你地圖**，即可平移至圖表的不同區域。

按一下圖表中的階段，即可查看所選階段的詳細資料。階段詳細資料包含：

* 統計資料。如要瞭解統計資料的詳細資訊，請參閱「[階段總覽](#stage-overview)」。
* 步驟詳細資料。步驟說明執行查詢邏輯的個別作業。

#### 步驟詳細資料

階段由步驟組成，步驟是執行查詢邏輯的個別作業。步驟包含*子步驟*，以虛擬程式碼說明步驟的作用。
子步驟會使用變數來描述步驟之間的關係。變數開頭為貨幣符號，後面接著不重複的數字。變數編號不會在各階段共用。

下圖顯示階段的步驟：

以下是階段步驟的範例：

```
  READ
  $30:l_orderkey, $31:l_quantity
  FROM lineitem

  AGGREGATE
  GROUP BY $100 := $30
  $70 := SUM($31)

  WRITE
  $100, $70
  TO __stage00_output
  BY HASH($100)
```

範例步驟說明下列事項：

* 這個階段從資料表 lineitem 讀取 l\_orderkey 和 l\_quantity 欄，並分別將值儲存在 $30 和 $31 變數中。
* 這個階段會匯總 $30 和 $31 變數，並分別將匯總結果儲存到 $100 和 $70 變數中。
* 這個階段會將 $100 和 $70 變數的結果寫入 shuffle。這個階段會根據 $100，在隨機記憶體中排序結果。

如要瞭解步驟類型和最佳化方式的完整詳細資料，請參閱「[解讀及最佳化步驟](#interpret-and-optimize-steps)」。

如果查詢的執行圖過於複雜，提供完整子步驟可能會導致擷取查詢資訊時發生酬載大小問題，因此 BigQuery 可能會截斷子步驟。

#### 查詢文字熱視圖

BigQuery 可以將部分階段步驟對應至查詢文字。查詢文字熱視圖會顯示所有對應的查詢文字和階段步驟。系統會根據階段的總運算單元時間，醒目顯示查詢文字，這些階段的步驟已對應查詢文字。

下圖顯示醒目顯示的查詢文字：

將指標懸停在查詢文字的對應部分上方時，會顯示工具提示，列出對應查詢文字的所有階段步驟，以及階段時段。按一下對應的查詢文字，即可選取執行圖中的階段，並在右側面板中開啟階段詳細資料。

查詢文字的單一部分可以對應到多個階段。工具提示會列出每個對應的階段及其時段。點選查詢文字會醒目顯示對應階段，並將圖表的其餘部分調暗。隨後按一下特定階段，即可查看詳細資料。

下圖顯示查詢文字與步驟詳細資料的關聯：

在階段的「步驟詳細資料」部分中，如果步驟對應至查詢文字，該步驟會顯示程式碼圖示。按一下程式碼圖示，即可醒目顯示左側查詢文字中對應的部分。

請務必注意，熱度圖顏色是根據整個階段的時段計算。由於 BigQuery 不會測量步驟的運算單元時間，熱度圖不會顯示對應查詢文字特定部分的實際運算單元時間。在大多數情況下，階段只會執行單一複雜步驟，例如聯結或匯總。因此熱視圖顏色是適當的。不過，如果階段是由執行多項複雜作業的步驟組成，熱視圖顏色可能會過度呈現熱視圖中的實際時段。在這種情況下，請務必瞭解組成階段的其他步驟，以便更全面地掌握查詢的成效。

如果查詢使用檢視區塊，且階段的步驟已對應至檢視區塊的查詢文字，查詢文字熱度圖就會顯示檢視區塊的名稱和查詢文字，以及對應項目。不過，如果檢視區塊遭到刪除，或是您失去檢視區塊的 `bigquery.tables.get` [IAM 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)，查詢文字熱度圖就不會顯示檢視區塊的階段步驟對應。

### 階段總覽

每個階段的總覽欄位可包含下列項目：

| API 欄位 | 說明 |
| --- | --- |
| `id` | 階段的專屬數字 ID。 |
| `name` | 階段的簡式摘要名稱。階段內的 `steps` 會提供執行步驟的額外詳細資料。 |
| `status` | 階段的執行狀態。可能的狀態包括「待處理」、「執行中」、「已完成」、「失敗」及「已取消」。 |
| `inputStages` | 構成階段相依關係圖的 ID 清單。例如，JOIN 階段通常需要兩個相依階段，用來準備 JOIN 關係左右兩側的資料。 |
| `startMs` | 時間戳記 (以 UNIX 時間為單位)，顯示階段中第一個工作站開始執行的時間。 |
| `endMs` | 時間戳記 (以 UNIX 時間為單位)，顯示最後一個工作站執行完成的時間。 |
| `steps` | 階段中執行步驟的詳細清單。詳情請參閱下一節。 |
| `recordsRead` | 所有階段工作站中階段的輸入大小，以記錄數表示。 |
| `recordsWritten` | 所有階段工作站中階段的輸出大小，以記錄數表示。 |
| `parallelInputs` | 階段中可平行執行的工作單元數。視階段和查詢而定，這可能代表資料表中的資料欄區隔數量，或是中間隨機排序中的分割數量。 |
| `completedParallelInputs` | 階段中已完成的工作單元數。在某些查詢中，不一定要完成階段中的所有輸入後，該階段才能完成。 |
| `shuffleOutputBytes` | 代表某一查詢階段中所有工作站上的寫入位元組總數。 |
| `shuffleOutputBytesSpilled` | 在階段之間傳輸大量資料的查詢，可能需要以磁碟型傳輸為備用方法。溢出位元組統計資料會顯示溢出至磁碟的資料量。取決於最佳化演算法，因此任何指定查詢都不具決定性。 |

### 每階段時間分類

查詢階段提供相對和絕對兩種格式的階段時間分類。由於每個執行階段均代表一或多個獨立工作站執行的工作，因此提供的資訊會分成平均時間和最長時間兩種。這些時間分別代表某一階段中所有工作站的平均效能，以及指定分類中耗時最長的工作站效能。平均時間和最長時間會進一步分成絕對和相對表示法。在依比例的統計資料部分，會以任一區段中任何工作站所費的最長時間比例提供資料。

Google Cloud 控制台會利用相對時間表示法來呈現階段時間。

階段時間資訊的報告如下所示：

| 相對時間 | 絕對時間 | 比率分子 |
| --- | --- | --- |
| `waitRatioAvg` | `waitMsAvg` | 一般工作站在等待排程上花費的時間。 |
| `waitRatioMax` | `waitMsMax` | 最慢的工作站在等待排程上花費的時間。 |
| `readRatioAvg` | `readMsAvg` | 一般工作站在讀取輸入資料上花費的時間。 |
| `readRatioMax` | `readMsMax` | 最慢的工作站在讀取輸入資料上花費的時間。 |
| `computeRatioAvg` | `computeMsAvg` | 一般工作站受 CPU 限制的時間。 |
| `computeRatioMax` | `computeMsMax` | 最慢的工作站受 CPU 限制的時間。 |
| `writeRatioAvg` | `writeMsAvg` | 一般工作站在寫入輸出資料上花費的時間。 |
| `writeRatioMax` | `writeMsMax` | 最慢的工作站在寫入輸出資料上花費的時間。 |

### 步驟總覽

步驟包含每個工作站在階段中執行的作業，以作業的排序清單呈現。每個步驟作業都有類別，且部分作業會提供更詳細的資訊。查詢計畫中的作業類別如下：

| 步驟類別 | 說明 |
| --- | --- |
| `READ` | 從輸入資料表或中繼重組中讀取一或多個資料欄。步驟詳細資料只會顯示讀取的前 16 欄。 |
| `WRITE` | 將一或多個資料欄寫入輸出資料表或中繼重組中。若是階段的 `HASH` 分區輸出，這也包含做為分區索引鍵使用的資料欄。 |
| `COMPUTE` | 運算式評估和 SQL 函式。 |
| `FILTER` | 由 `WHERE`、`OMIT IF` 和 `HAVING` 子句使用。 |
| `SORT` | `ORDER BY` 作業，包括資料欄索引鍵和排序順序。 |
| `AGGREGATE` | 為 `GROUP BY` 或 `COUNT` 等子句實作匯總。 |
| `LIMIT` | 實作 `LIMIT` 子句。 |
| `JOIN` | 為 `JOIN` 等子句實作彙整；包括彙整類型和可能的彙整條件。 |
| `ANALYTIC_FUNCTION` | 叫用 window 函式 (又稱「分析函式」)。 |
| `USER_DEFINED_FUNCTION` | 使用者定義函式的呼叫。 |

## 解讀及最佳化步驟

以下各節說明如何解讀查詢計畫中的步驟，並提供查詢最佳化方法。

### `READ` 步

`READ` 步驟表示某個階段正在存取資料以進行處理。資料可直接從查詢參照的資料表讀取，或從重組記憶體讀取。讀取前一階段的資料時，BigQuery 會從重組記憶體讀取資料。使用隨選時段時，掃描的資料量會影響費用；使用預訂時，則會影響效能。

#### 潛在成效問題

* **掃描未分區資料表的大量資料：**如果查詢只需要一小部分資料，這可能表示掃描資料表效率不彰。[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)可能是個不錯的最佳化策略。
* **掃描大型資料表，但篩選比例很小：**這表示篩選器無法有效減少掃描的資料。建議您修改篩選條件。
* **溢出至磁碟的隨機位元組：**這表示資料未透過叢集等最佳化技術有效儲存，而叢集可將類似資料保留在叢集中。

#### 最佳化

* **目標篩選：**策略性地使用 `WHERE` 子句，盡早篩除查詢中的不相關資料。進而減少查詢需要處理的資料量。
* **分區和叢集：**BigQuery 會使用資料表分區和叢集，有效找出特定資料區段。請根據一般查詢模式，確保資料表已分區和分群，盡量減少 `READ` 步驟期間掃描的資料量。
* **選取相關資料欄：**避免使用 `SELECT *` 陳述式。請改為選取特定資料欄，或使用 `SELECT * EXCEPT` 避免讀取不必要的資料。
* **具體化檢視表：**具體化檢視表可預先計算及儲存常用的匯總，進而減少在查詢的 `READ` 步驟中讀取基礎資料表的需要。

### `COMPUTE` 步

在 `COMPUTE` 步驟中，BigQuery 會對您的資料執行下列動作：

* 評估查詢中 `SELECT`、`WHERE`、`HAVING` 和其他子句的運算式，包括計算、比較和邏輯運算。
* 執行內建 SQL 函式和使用者定義函式。
* 根據查詢中的條件篩選資料列。

#### 最佳化

查詢計畫可找出 `COMPUTE` 步驟中的瓶頸。尋找需要大量運算或處理大量資料列的階段。

* **將 `COMPUTE` 步驟與資料量相互關聯：**如果某個階段顯示大量運算作業，並處理大量資料，則可能適合進行最佳化。
* **資料偏斜：**如果某個階段的運算上限遠高於運算平均值，表示該階段花費不成比例的時間處理少數資料切片。建議查看資料分布情形，確認是否有資料偏斜。
* **考慮資料類型：**為資料欄使用適當的資料類型。舉例來說，使用整數、日期時間和時間戳記，而不是字串，可以提升效能。

### `WRITE` 步

中繼資料和最終輸出內容都會經過 `WRITE` 步驟。

* **寫入重組記憶體：**在多階段查詢中，`WRITE` 步驟通常會將處理過的資料傳送至另一個階段，以進行進一步處理。這是重組記憶體的典型做法，可合併或匯總多個來源的資料。這個階段寫入的資料通常是中繼結果，而非最終輸出。
* **最終輸出：**查詢結果會寫入目的地或暫時性資料表。

#### 雜湊分區

當查詢計畫中的階段將資料寫入雜湊分區輸出內容時，BigQuery 會寫入輸出內容中包含的資料欄，以及選為分區鍵的資料欄。

#### 最佳化

雖然 `WRITE` 步驟本身可能無法直接最佳化，但瞭解其角色有助於找出早期階段的潛在瓶頸：

* **減少寫入的資料量：**著重於透過篩選和彙整作業，將前幾個階段最佳化，以減少這個步驟寫入的資料量。
* **分區：**資料表分區可大幅提升寫入作業的效能。如果寫入的資料僅限於特定分區，BigQuery 就能更快完成寫入作業。

  如果 DML 陳述式含有 `WHERE` 子句，且該子句針對資料表分區資料欄設有靜態條件，則 BigQuery 只會修改相關資料表分區。
* **去正規化取捨：**去正規化有時會導致中間`WRITE`步驟的結果集較小。但缺點是儲存空間用量增加，以及資料一致性問題。

### `JOIN` 步

在 `JOIN` 步驟中，BigQuery 會合併兩個資料來源的資料。聯結可包含聯結條件。聯結會耗用大量資源。在 BigQuery 中彙整大型資料時，彙整索引鍵會獨立重組，在相同時段對齊，以便在每個時段執行本機彙整。

`JOIN` 步驟的查詢計畫通常會顯示下列詳細資料：

* **Join 模式：**指出使用的 Join 類型。每種型別都會定義結果集中要納入多少個聯結資料表的資料列。
* **彙整資料欄：**這些資料欄用於比對資料來源之間的資料列。選擇的資料欄會直接影響彙整作業的效能。

#### 加入模式

* **廣播聯結：**當一個資料表 (通常是較小的資料表) 可以容納在單一 worker 節點或運算單元的記憶體中時，BigQuery 可以將其廣播至所有其他節點，有效執行聯結。在步驟詳細資料中尋找 `JOIN EACH WITH ALL`。
* **雜湊聯結：**如果資料表很大或不適合廣播聯結，系統可能會使用雜湊聯結。BigQuery 會使用雜湊和隨機排序作業，隨機排序左側和右側資料表，讓相符的鍵最終位於相同位置，以執行本機聯結。由於需要移動資料，雜湊聯結是成本高昂的作業，但可有效比對雜湊中的資料列。在步驟詳細資料中尋找 `JOIN EACH WITH EACH`。
* **Self join：**SQL 反模式，指資料表與自身彙整。
* **cross join：**SQL 反模式，會產生比輸入資料更大的輸出資料，因此可能導致嚴重的效能問題。
* **偏斜的彙整：**一個資料表中彙整索引鍵的資料分布非常偏斜，可能會導致效能問題。請找出最長運算時間遠大於查詢計畫中平均運算時間的案例。詳情請參閱[高基數聯結](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#high_cardinality_join)和[分區傾斜](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#partition_skew)。

#### 偵錯

* **資料量過大：**如果查詢計畫顯示在 `JOIN` 步驟中處理了大量資料，請調查聯結條件和聯結鍵。建議您篩選或使用更具選擇性的彙整鍵。
* **資料分布不均：**分析聯結鍵的資料分布情形。如果某個資料表非常傾斜，請探索查詢分割或預先篩選等策略。
* **高基數彙整：**如果彙整產生的資料列數量遠多於左側和右側的輸入資料列，查詢效能可能會大幅降低。避免產生大量資料列的聯結。
* **資料表排序錯誤：**請確保已選擇適當的聯結類型，例如 `INNER` 或 `LEFT`，並根據查詢需求，將資料表從大到小排序。

#### 最佳化

* **選擇性彙整鍵：**盡可能使用 `INT64`，而非 `STRING` 做為彙整鍵。`STRING` 比較比 `INT64` 比較慢，因為前者會比較字串中的每個字元。整數只需要單一比較。
* **先篩選再聯結：**在聯結前，先在個別表格上套用 `WHERE` 子句篩選器。這會減少聯結作業涉及的資料量。
* **避免在聯結資料欄上使用函式：**避免在聯結資料欄上呼叫函式。而是使用 ELT SQL 管道，在擷取或擷取後程序中，將資料表資料標準化。這種做法可免除動態修改聯結資料欄的需要，因此能更有效率地聯結資料，同時確保資料完整性。
* **避免使用自連接：**自連接常用於計算列相關關係。不過，自我聯結可能會使輸出列數增加四倍，導致效能問題。請考慮使用窗型 (分析) 函式，而非依賴自連接。
* **先處理大型資料表：**即使 SQL 查詢最佳化工具可以判斷聯結的哪一側應使用哪個資料表，仍請適當排序聯結的資料表。最佳做法是先放置最大的表格，接著是最小的表格，然後依遞減大小放置。
* **去正規化：**在某些情況下，策略性地去正規化資料表 (新增多餘資料) 可完全消除聯結。不過，這種做法會導致儲存空間和資料一致性方面的取捨。
* **分區和叢集：**根據彙整索引鍵將資料表分區，並將共置資料叢集化，可讓 BigQuery 鎖定相關資料分區，大幅加快彙整速度。
* **最佳化偏移的聯結：**為避免偏移的聯結造成效能問題，請盡可能預先篩選資料表中的資料，或將查詢作業拆分成兩個以上的查詢作業。

### `AGGREGATE` 步

在 `AGGREGATE` 步驟中，BigQuery 會匯總及分組資料。

#### 偵錯

* **階段詳細資料：**檢查匯總的輸入和輸出列數，以及重組大小，判斷匯總步驟減少了多少資料，以及是否涉及資料重組。
* **Shuffle 大小：**如果 Shuffle 大小很大，可能表示在匯總期間，大量資料在工作站節點之間移動。
* **檢查資料分布：**確保資料均勻分布在各個分區。資料分布不均可能會導致匯總步驟中的工作負載不平衡。
* **檢查匯總：**分析匯總子句，確認這些子句是否必要且有效率。

#### 最佳化

* **叢集：**在 `GROUP
  BY`、`COUNT` 或其他匯總子句中，對經常使用的資料欄建立叢集。
* **分區：**選擇符合查詢模式的分區策略。建議使用擷取時間分區資料表，減少彙整期間掃描的資料量。
* **提早彙整：**盡可能在查詢管道中提早執行彙整作業。這樣可以減少匯總期間需要處理的資料量。
* **隨機排序最佳化：**如果隨機排序是瓶頸，請想辦法盡量減少隨機排序。舉例來說，您可以取消正規化資料表，或使用叢集將相關資料放在相同位置。

#### 極端案例

* **DISTINCT 聚合：**含有 `DISTINCT` 聚合的查詢可能需要大量運算資源，尤其是處理大型資料集時。如要取得近似結果，請考慮使用 `APPROX_COUNT_DISTINCT` 等替代函式。
* **大量群組：**如果查詢會產生大量群組，可能會耗用大量記憶體。在這種情況下，請考慮限制群組數量或使用其他匯總策略。

### `REPARTITION` 步

`REPARTITION` 和 `COALESCE` 都是最佳化技術，BigQuery 會直接套用至查詢中的隨機資料。

* **`REPARTITION`：**這項作業的目的是重新平衡工作節點之間的資料分配。假設在重組後，某個 worker 節點的資料量過大，`REPARTITION` 步驟會更平均地重新分配資料，避免單一工作站成為瓶頸。對於聯結等需要大量運算的作業，這一點尤其重要。
* **`COALESCE`：**如果資料經過重組後，產生許多小型資料桶，就會執行這個步驟。`COALESCE` 步驟會將這些儲存區合併為較大的儲存區，減少管理大量小型資料片段的相關負擔。處理非常小的中繼結果集時，這項功能特別實用。

如果查詢計畫中出現 `REPARTITION` 或 `COALESCE` 步驟，不一定表示查詢有問題。這通常表示 BigQuery 正在主動最佳化資料分配，以提升效能。不過，如果這些作業重複發生，可能表示資料本身有偏差，或是查詢導致過多的資料重組。

#### 最佳化

如要減少 `REPARTITION` 步驟的數量，請嘗試下列做法：

* **資料分配：**確保資料表已有效分區和分群。資料分布越平均，隨機排序後出現顯著不平衡的可能性就越低。
* **查詢結構：**分析查詢，找出可能導致資料偏斜的來源。
  舉例來說，是否有高選擇性的篩選器或聯結，導致單一工作站處理的資料子集很小？
* **合併策略：**嘗試不同的合併策略，看看是否能讓資料分布更平均。

如要減少 `COALESCE` 步驟的數量，請嘗試下列做法：

* **匯總策略：**考慮在查詢管道中提早執行匯總作業。這有助於減少可能導致 `COALESCE` 步驟的小型中繼結果集數量。
* **資料量：**如果處理的資料集非常小，`COALESCE` 可能就不是主要問題。

請勿過度最佳化。過早最佳化可能會使查詢變得更複雜，但不會帶來顯著效益。

## 聯合查詢說明

[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)可讓您使用 [`EXTERNAL_QUERY` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query)，將查詢陳述式傳送至外部資料來源。聯合查詢會受到稱為 [SQL 下推](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#sql_pushdowns)的最佳化技術影響，查詢計畫會顯示下推至外部資料來源的作業 (如有)。舉例來說，如果您執行下列查詢：

```
SELECT id, name
FROM EXTERNAL_QUERY("<connection>", "SELECT * FROM company")
WHERE country_code IN ('ee', 'hu') AND name like '%TV%'
```

查詢計畫會顯示下列階段步驟：

```
$1:id, $2:name, $3:country_code
FROM table_for_external_query_$_0(
  SELECT id, name, country_code
  FROM (
    /*native_query*/
    SELECT * FROM company
  )
  WHERE in(country_code, 'ee', 'hu')
)
WHERE and(in($3, 'ee', 'hu'), like($2, '%TV%'))
$1, $2
TO __stage00_output
```

在這個計畫中，`table_for_external_query_$_0(...)` 代表 `EXTERNAL_QUERY` 函式。您可以在括號中看到外部資料來源執行的查詢。根據上述步驟，您可以發現：

* 外部資料來源只會傳回 3 個所選資料欄。
* 外部資料來源只會傳回 `country_code` 為 `'ee'` 或 `'hu'` 的資料列。
* `LIKE` 運算子不會下推，而是由 BigQuery 評估。

為進行比較，如果沒有下推，查詢計畫會顯示下列階段步驟：

```
$1:id, $2:name, $3:country_code
FROM table_for_external_query_$_0(
  SELECT id, name, description, country_code, primary_address, secondary address
  FROM (
    /*native_query*/
    SELECT * FROM company
  )
)
WHERE and(in($3, 'ee', 'hu'), like($2, '%TV%'))
$1, $2
TO __stage00_output
```

這次外部資料來源會傳回 `company` 資料表的所有資料欄和資料列，並由 BigQuery 執行篩選作業。

## 時程中繼資料

查詢時間軸會報告特定時間點的進度，提供整體查詢進度的快照檢視畫面。時間軸會以一系列樣本表示，這些樣本會回報下列詳細資料：

| 欄位 | 說明 |
| --- | --- |
| `elapsedMs` | 查詢開始執行後經歷的毫秒數。 |
| `totalSlotMs` | 查詢使用的運算單元毫秒數累計表示法。 |
| `pendingUnits` | 已排定和等待執行的工作單元總數。 |
| `activeUnits` | 工作站處理中的有效工作單元總數。 |
| `completedUnits` | 執行這項查詢時已完成的工作單元總數。 |

## 查詢範例

下列查詢會計算莎士比亞公開資料集中的列數，而查詢的第二個條件是將結果侷限在參照「哈姆雷特」的列：

```
SELECT
  COUNT(1) as rowcount,
  COUNTIF(corpus = 'hamlet') as rowcount_hamlet
FROM `publicdata.samples.shakespeare`
```

按一下「執行作業詳細資料」即可查看查詢計畫：

顏色指標會顯示所有階段中所有步驟的相對時間。

如要進一步瞭解執行階段的步驟，請點選 arrow\_drop\_down 展開階段的詳細資料：

在本例中，所有區段中耗費最長時間的是單一工作站在階段 01 等待階段 00 完成的時間。這是因為階段 01 需要有階段 00 的輸入，所以必須在第一個階段將輸出寫入中繼 Shuffle 後才能開始。

## 錯誤報告

查詢工作可能會在執行中失敗。因為系統會定期更新計畫資訊，所以您可以在執行圖中觀察到失敗的發生位置。在 Google Cloud 控制台中，階段名稱旁的勾號和驚嘆號分別標示著這個階段成功和失敗。

如要進一步瞭解如何解讀及解決錯誤，請參閱[疑難排解指南](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw)。

## API 表示法範例

查詢計畫資訊會內嵌於工作回應資訊，您可以呼叫 [`jobs.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw) 擷取這項資訊。舉例來說，下列摘錄的 JSON 回應適用於傳回哈姆雷特查詢範例的工作，其中顯示查詢計畫和時間軸資訊。

```
"statistics": {
  "creationTime": "1576544129234",
  "startTime": "1576544129348",
  "endTime": "1576544129681",
  "totalBytesProcessed": "2464625",
  "query": {
    "queryPlan": [
      {
        "name": "S00: Input",
        "id": "0",
        "startMs": "1576544129436",
        "endMs": "1576544129465",
        "waitRatioAvg": 0.04,
        "waitMsAvg": "1",
        "waitRatioMax": 0.04,
        "waitMsMax": "1",
        "readRatioAvg": 0.32,
        "readMsAvg": "8",
        "readRatioMax": 0.32,
        "readMsMax": "8",
        "computeRatioAvg": 1,
        "computeMsAvg": "25",
        "computeRatioMax": 1,
        "computeMsMax": "25",
        "writeRatioAvg": 0.08,
        "writeMsAvg": "2",
        "writeRatioMax": 0.08,
        "writeMsMax": "2",
        "shuffleOutputBytes": "18",
        "shuffleOutputBytesSpilled": "0",
        "recordsRead": "164656",
        "recordsWritten": "1",
        "parallelInputs": "1",
        "completedParallelInputs": "1",
        "status": "COMPLETE",
        "steps": [
          {
            "kind": "READ",
            "substeps": [
              "$1:corpus",
              "FROM publicdata.samples.shakespeare"
            ]
          },
          {
            "kind": "AGGREGATE",
            "substeps": [
              "$20 := COUNT($30)",
              "$21 := COUNTIF($31)"
            ]
          },
          {
            "kind": "COMPUTE",
            "substeps": [
              "$30 := 1",
              "$31 := equal($1, 'hamlet')"
            ]
          },
          {
            "kind": "WRITE",
            "substeps": [
              "$20, $21",
              "TO __stage00_output"
            ]
          }
        ]
      },
      {
        "name": "S01: Output",
        "id": "1",
        "startMs": "1576544129465",
        "endMs": "1576544129480",
        "inputStages": [
          "0"
        ],
        "waitRatioAvg": 0.44,
        "waitMsAvg": "11",
        "waitRatioMax": 0.44,
        "waitMsMax": "11",
        "readRatioAvg": 0,
        "readMsAvg": "0",
        "readRatioMax": 0,
        "readMsMax": "0",
        "computeRatioAvg": 0.2,
        "computeMsAvg": "5",
        "computeRatioMax": 0.2,
        "computeMsMax": "5",
        "writeRatioAvg": 0.16,
        "writeMsAvg": "4",
        "writeRatioMax": 0.16,
        "writeMsMax": "4",
        "shuffleOutputBytes": "17",
        "shuffleOutputBytesSpilled": "0",
        "recordsRead": "1",
        "recordsWritten": "1",
        "parallelInputs": "1",
        "completedParallelInputs": "1",
        "status": "COMPLETE",
        "steps": [
          {
            "kind": "READ",
            "substeps": [
              "$20, $21",
              "FROM __stage00_output"
            ]
          },
          {
            "kind": "AGGREGATE",
            "substeps": [
              "$10 := SUM_OF_COUNTS($20)",
              "$11 := SUM_OF_COUNTS($21)"
            ]
          },
          {
            "kind": "WRITE",
            "substeps": [
              "$10, $11",
              "TO __stage01_output"
            ]
          }
        ]
      }
    ],
    "estimatedBytesProcessed": "2464625",
    "timeline": [
      {
        "elapsedMs": "304",
        "totalSlotMs": "50",
        "pendingUnits": "0",
        "completedUnits": "2"
      }
    ],
    "totalPartitionsProcessed": "0",
    "totalBytesProcessed": "2464625",
    "totalBytesBilled": "10485760",
    "billingTier": 1,
    "totalSlotMs": "50",
    "cacheHit": false,
    "referencedTables": [
      {
        "projectId": "publicdata",
        "datasetId": "samples",
        "tableId": "shakespeare"
      }
    ],
    "statementType": "SELECT"
  },
  "totalSlotMs": "50"
},
```

## 使用執行資訊

BigQuery 查詢計畫會提供服務執行查詢的方式相關資訊，但服務的代管性質限制了部分詳細資料是否可以直接操作。使用這項服務時，系統會自動執行許多最佳化作業，這與其他環境不同，因為在其他環境中，調整、佈建和監控作業可能需要專門的專業人員。

如要瞭解可提升查詢執行和效能的具體技巧，請參閱[最佳做法說明文件](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)。查詢計畫和時間軸統計資料可協助您瞭解是否有特定階段霸占資源使用量。舉例來說，如果 JOIN 階段產生的輸出資料列比輸入資料列多很多，可能表示可以在查詢中更早進行篩選。

此外，時間軸資訊有助於判斷特定查詢是否單獨執行緩慢，或是因為其他查詢爭用相同資源而受到影響。如果您發現作用中的單元數在整個查詢生命週期中依然有限，但已排入佇列的工作單元數量卻一直很高，這可能代表減少並行查詢的數量會大幅改善某些查詢的整體執行時間。

**注意：** 部分查詢處理作業會在任何階段的內容之外進行。在某些情況下，系統可能會在第一個階段調度前或最後一個階段完成後，累積大量延遲或時段用量。例如某些形式的分區修剪、各種中繼資料作業，以及[補償過多的運算單元用量](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#excess_slot_usage)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]