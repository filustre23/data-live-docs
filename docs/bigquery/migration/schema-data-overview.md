Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 結構定義與資料移轉總覽

本文將說明將結構定義和資料從現有資料倉儲轉移到 BigQuery 的概念和工作。

將資料倉儲遷移至雲端是一個複雜的過程，需要規劃、資源和時間。為了化繁為簡，您應該以分階段的疊代方式遷移資料倉儲。反覆進行結構定義和資料遷移，可改善結果。

## 結構定義和資料遷移程序

在遷移歷程開始時，上游系統會動態饋給現有資料倉儲，而下游系統會將該資料用於報表、資訊主頁，以及做為其他程序的動態饋給。

這種一般的資料流動支援許多分析[用途](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#use-case)，如下圖所示：

此過程的結束狀態是盡可能在 BigQuery 上執行更多的用途。這個狀態可讓您將現有資料倉儲的用量降至最低，終而廢除使用。您可以控制要遷移哪些用途以及遷移時間，方法是在遷移作業的[準備與探索](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#prepare-and-discover)階段，排定這些用途的優先順序。

### 將結構定義和資料移轉至 BigQuery

在遷移作業的[規劃](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#plan)階段中，您可以找出要遷移的用途。然後在[執行](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#execute)階段開始遷移疊代作業。如要管理疊代，同時以盡可能避免服務中斷的方式執行分析環境，請遵循以下高階流程：

1. 轉移資料表並設定和測試下游程序。

   * 使用 BigQuery 資料移轉服務或其他 ETL 工具，將每個用途的資料表群組原封不動地轉移至 BigQuery。如需工具相關資訊，請參閱[初始資料移轉](#initial-data-transfer)部分。
   * 設定要讀取 BigQuery 資料表的下游程序的測試版本。

   這個初始步驟會劃分資料流動過程，下圖顯示產生的流動過程。現在，有部分下游系統會讀取 BigQuery，如標為 B 的流程所示。其他系統依然讀取現有資料倉儲，如標為 A 的流程所示。
2. 設定幾個測試上游程序，將資料寫入 BigQuery 資料表而不是寫入現有資料倉儲 (或是除了寫入現有資料倉儲外，另再寫入 BigQuery 資料表)。

   測試之後，設定實際工作環境上游和下游程序以寫入和讀取 BigQuery 資料表。這些程序可以使用 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference?hl=zh-tw) 連線到 BigQuery，並整合新的雲端產品，如 [數據分析](https://lookerstudio.google.com/?hl=zh-tw) 和 [Dataflow](https://docs.cloud.google.com/dataflow/docs?hl=zh-tw)。

   此時，您有三個資料流動過程：

   1. 現有。資料和程序不會改變，仍會以現有資料倉儲為中心。
   2. [卸載](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#offload)。
      上游程序會動態饋給現有資料倉儲資料，然後資料卸載至 BigQuery，接著動態饋給下游程序。
   3. [完全遷移](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#full-migration)。
      上游和下游程序不再寫入或讀取現有資料倉儲。

      下圖是具有全部三個流動過程的系統：
3. 選取其他用途以進行遷移作業，然後前往步驟 1 開始新的[執行疊代作業](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#migrating-using-an-iterative-approach)。
   繼續疊代完成這些步驟，直到所有用途全都遷移到 BigQuery 中。選取用途時，您可以重新查看仍處於卸載狀態的用途，以便將其移至完全遷移狀態。對於完全遷移的用途，建議您遵循「[在 BigQuery 中改進結構定義](#evolving_your_schema_in_bigquery)」中的指導方針，繼續改進程序。

### 在 BigQuery 中改進結構定義

資料倉儲的結構定義會對資料結構以及資料實體之間的關係給予定義。結構定義是資料設計的核心，因此會影響上游和下游的許多程序。

資料倉儲遷移作業提供了一個獨特的機會，可以對轉移到 BigQuery 之後的結構定義進行改進。本節提供一系列步驟做為改進結構定義的指導方針，這些指導方針可以幫助您在變更結構定義期間，保持資料倉儲環境的運作，同時將上游和下游程序的中斷情況降至最低。

本節中的步驟主要針對單一用途進行結構定義的轉換。

視您想要的改進程度而定，您可以停在某個中間步驟，或是繼續進行到系統完全改進為止。

1. 將用途依原狀轉移至 BigQuery。

   在繼續執行後續步驟之前，請確保用途的上游和下游程序已在寫入和讀取 BigQuery。不過，也有可能從只有下游程序在讀取 BigQuery 的中間狀態開始。在這種情況下，請您只運用下游部分的指導方針。在下圖的範例用途中，上游和下游程序會對 BigQuery 資料表進行寫入和讀取。
2. 套用輕量最佳化。

   1. 重新建立資料表，並套用[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[叢集處理](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。
      針對這項工作，您可以使用從查詢結果建立資料表的方法。詳情請參閱有關分區資料表的[討論](https://docs.cloud.google.com/bigquery/docs/creating-column-partitions?hl=zh-tw#creating_a_partitioned_table_from_a_query_result)和[範例](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_partitioned_table_from_the_result_of_a_query)，以及叢集資料表的相關[討論](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw#create_a_clustered_table_from_a_query_result)和[範例](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_clustered_table_from_the_result_of_a_query)。
   2. 將上游和下游程序重新導向至新資料表。
3. 建立門面元件檢視畫面。

   如果您想要進一步改進結構定義而不僅止於輕量最佳化，請為資料表建立「門面檢視表」。[門面模式](https://wikipedia.org/wiki/Facade_pattern)是一種掩飾底層程式碼或結構以隱藏複雜性的設計方法。在這種情況下，門面檢視表會遮蓋基礎資料表，以隱藏下游程序變更資料表所造成的複雜性。

   這些檢視表可以描繪一個新的結構定義，不會有技術負債，並且模型的建立會考量到新的擷取和消耗情境。

   就運作原理來看，資料表和檢視表查詢的定義本身可以變更。但是這些檢視表會將這些變更提取出來做為資料倉儲的內部實作詳細資料，並且始終會傳回相同的結果。由門面檢視表構成的[抽象層](https://wikipedia.org/wiki/Abstraction_layer)會根據需要，讓上游和下游系統與變更隔離開來，並且只在適當情況下才會顯示變更。
4. 轉換下游程序。

   您可以將部分下游程序轉換為讀取門面檢視表而不是讀取實際資料表。這時這些程序已經從改進的結構定義中受益。就運作原理來看，門面檢視表還是會從來源 BigQuery 結構定義取得資料。這一點對於這些程序而言是透明的，如下圖所示：

   我們已經先說明下游程序轉換，比起轉換非技術相關人員無法看見的上游程序，這可讓您以遷移後的資訊主頁或報表形式更快顯示商業價值。不過，您也可以改用上游程序來進行轉換。這些工作的優先順序完全取決於您的需求。
5. 轉換上游程序。

   您可以將部分上游程序轉換為寫入新的結構定義。由於檢視表為唯讀，所以您可以根據新結構定義建立資料表，然後修改門面檢視表的查詢定義。有些檢視區塊仍會查詢來源結構定義，而有些檢視區塊則會查詢新建立的資料表，或對兩者執行 SQL `UNION` 運算，如下圖所示：

   此時，您可以在建立新資料表時利用[巢狀和重複欄位](#denormalization)。如此一來，您可以進一步將模型去標準化，並直接利用 BigQuery 底層直欄式的資料表示法。

   門面檢視表的一個優點是，您的下游程序可以繼續轉換，而不受這些底層結構定義變更和上游程序變更的影響。
6. 完全改進您的用途。

   最後，您可以轉換其餘的上游和下游程序。當所有這些程序都進展為寫入新的資料表並讀取新的門面檢視表時，您可以修改門面檢視表的查詢定義，使其不再讀取來源結構定義。接著，您可以從資料流程中淘汰來源模型中的資料表。下圖呈現了不再使用來源資料表的狀態。

   如果門面檢視表不會匯總欄位或篩選資料欄，那您可以將下游程序設為讀取改進後的資料表，然後淘汰門面檢視表以降低複雜性，如下圖所示：

## 執行結構定義和資料的初始轉移作業

本節將討論將結構定義和資料從現有資料倉儲遷移至 BigQuery 的實際考量事項。

我們建議在遷移的初始疊代作業期間，應轉移結構定義而不進行任何變更。這項功能可帶來下列優點：

* 無需針對新結構定義調整動態饋給資料倉儲的資料管道。
* 可避免在員工的訓練資料清單中加入新的結構定義。
* 可利用自動化工具執行結構定義與資料移轉作業。

此外，使用雲端功能的概念驗證 (PoC) 和其他資料探索活動也可以順暢無礙地進行，即使遷移作業同時進行。

### 選擇轉移方法

您可以從多種方法選擇其一，進行初始移轉。

* 如果是 Amazon Redshift 和 Teradata 資料倉儲，您可以使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，直接將現有系統中的結構定義和資料載入 BigQuery。在遷移程序中，Cloud Storage 仍會用於暫存資料。
* 對於任何資料倉儲，您可以擷取包含結構定義和資料的檔案，將這些檔案上傳至 Cloud Storage，然後使用下列其中一個選項，將這些檔案中的結構定義和資料載入 BigQuery：
  + [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)
  + [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)
  + [批次載入](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)

如要進一步瞭解選擇資料移轉方法時的考量事項，請參閱「[選擇資料擷取方法](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw#methods)」。

### 考慮資料轉換

根據您的資料擷取格式，以及在載入 BigQuery 前要對資料進行修剪或是充實而定，您可能會加入轉換資料的步驟。您可以轉換現有環境或 Google Cloud中的資料：

* 如果您在目前環境中轉換資料，請考慮可用的運算容量和工具對於總處理量會造成什麼樣的限制。此外，如果在轉換程序中充實資料，請考慮是否需要額外的移轉時間或網路頻寬。
* 如果轉換資料的選項設為開啟 Google Cloud，請參閱「[使用 ETL 工具載入資料](#load_data_using_an_etl_tool)」，進一步瞭解相關選項。

### 將現有結構定義和資料擷取至檔案

現有平台可能提供工具，用於將資料匯出為各家廠商通用的格式，例如 [Apache AVRO](https://avro.apache.org/docs/current/) 或 CSV。為降低移轉作業的複雜性，我們建議使用 AVRO、[ORC](https://orc.apache.org/) 或 [Parquet](https://parquet.apache.org/)，其中結構定義資訊已隨資料一起嵌入。如果您選擇 CSV 或類似的簡單分隔資料格式，則必須另外指定結構定義。操作方式取決於您選取的資料移轉方法。舉例來說，如要批次上傳，您可以在載入時指定結構定義，也可以根據 CSV 檔案內容自動偵測結構定義。

從現有平台擷取這些檔案時，請將檔案複製到現有環境的暫存儲存空間。

### 將檔案上傳至 Cloud Storage

除非您使用 BigQuery 資料移轉服務直接從現有的 Amazon Redshift 或 Teradata 資料倉儲載入資料，否則必須將擷取的檔案上傳至 Cloud Storage 的 bucket。根據轉移的資料量和可用的網路頻寬，您可以選擇以下移轉選項：

* 如果您擷取的資料位於其他雲端供應商處，請使用 [Storage 移轉服務](https://docs.cloud.google.com/storage/transfer?hl=zh-tw)。
* 如果資料位於地端部署環境或具有良好網路頻寬的主機代管機房，請使用 [Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)。gcloud CLI 支援多執行緒平行上傳，可在發生錯誤後繼續上傳，並加密傳輸中的流量以確保安全性。

  + 如果無法使用 gcloud CLI，可以嘗試使用 Google 合作夥伴的[第三方](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw#third-party_tools)工具。
  + 如果網路頻寬有限，可使用[壓縮技術](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw#decrease_data_size)限制資料大小，或修改目前與 Google Cloud 的連線來[增加頻寬](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw#increase_network_bandwidth)。
* 如果無法取得足夠的網路頻寬，您可以使用 [Transfer Appliance](https://docs.cloud.google.com/transfer-appliance?hl=zh-tw) 執行離線移轉作業。

建立 Cloud Storage 值區，並要透過網路轉移資料時，請選擇最靠近資料中心的位置，藉此將網路延遲縮至最短。如果可以，請選擇與 BigQuery 資料集位置相同的[值區位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#data-locations)。

如要詳細瞭解將資料搬移至 Cloud Storage 的最佳做法 (包括估算費用)，請參閱[轉移龐大資料集的策略](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw)。

### 將結構定義和資料載入 BigQuery

使用「[選擇移轉方法](#choose_a_transfer_method)」一節中討論的其中一個選項，將結構定義和資料載入 BigQuery。

如要進一步瞭解一次載入作業，請參閱 BigQuery 說明文件中的[從 Cloud Storage 載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage?hl=zh-tw)。如需排程定期載入作業的詳細資訊，請參閱 BigQuery 資料移轉服務說明文件中的「[Cloud Storage 移轉總覽](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw)」。

#### 使用 ETL 工具載入資料

如果資料載入 BigQuery 時需要進一步轉換，請使用下列任一選項：

* [Cloud Data Fusion](https://docs.cloud.google.com/data-fusion/docs?hl=zh-tw)：
  這個工具使用內含預先設定連接器和轉換的開放原始碼程式庫，以圖形方式建構全代管 ETL/ELT 資料管道。
* [Dataflow](https://docs.cloud.google.com/dataflow/docs?hl=zh-tw)。
  這個工具使用 [Apache Beam](https://beam.apache.org/) 模型來定義並執行複雜的資料轉換和擴充圖。Dataflow 是無伺服器模式，完全由 Google 代管，讓您可以存取幾乎沒有任何限制的處理能力。
* [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc/docs?hl=zh-tw)。這個工具會在全代管雲端服務上執行 Apache Spark 和 Apache Hadoop 叢集。
* 第三方工具。請與我們的[合作夥伴](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw)聯絡。當您想要將資料管道的建構外部化時，他們可以提供各種有效的選擇。

下圖呈現了本節所述的模式。資料移轉工具是 [gcloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)，其中有一個轉換步驟會利用 Dataflow 並且會直接寫入 BigQuery，也許是使用 Apache Beam 內建的 [Google BigQuery I/O 連接器。](https://beam.apache.org/documentation/io/built-in/google-bigquery/)

將初始資料集載入 BigQuery 後，您就可以開始利用 [BigQuery 的強大功能](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)。

但是，就如您轉移結構定義時一樣，上傳資料也是疊代程序的一部分。後續疊代作業可以從擴大轉移至 BigQuery 的資料足跡開始，接著可以將上游資料動態饋給重新轉送至 BigQuery，這樣就不需要繼續執行現有資料倉儲。這些主題將在下一節中說明。

### 驗證資料

資料移轉至 BigQuery 後，您可以使用[資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator) (DVT) 確認資料移轉是否成功。DVT 是開放原始碼的 Python CLI 工具，可讓您比較各種來源的資料與 BigQuery 中的目標資料。您可以指定要執行的匯總作業 (例如計數、總和、平均值)，以及要套用這些作業的資料欄。詳情請參閱「[使用 DVT 自動執行資料驗證](https://cloud.google.com/blog/products/databases/automate-data-validation-with-dvt?hl=zh-tw)」。

## 反覆疊代初始轉移作業

本節將探討在初次轉移資料後如何繼續後續的工作，以便充分利用 BigQuery。

資料子集現在已位於 BigQuery 中。現在準備要增加資料在 BigQuery 中使用的足跡，以減少對現有資料倉儲的依賴。

您為後續疊代作業選擇什麼方法，會取決於對您的用途而言，將資料更新到目前這一秒有多重要。如果資料分析師可以定期重複處理合併到資料倉儲中的資料，則可以選擇已排定時間的選項。您可以透過與初始移轉作業類似的方式建立排定的移轉作業，然後使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw)、其他 ETL 工具 (例如 Google [Storage 移轉服務](https://docs.cloud.google.com/storage/transfer?hl=zh-tw)) 或[第三方](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw#third-party_tools)實作。

如果您使用 BigQuery 資料移轉服務，首先要決定要移動的資料表，然後建立資料表名稱模式來納入這些資料表。最後一步是設定執行移轉作業的重複排程。

另一方面，如果您的用途需要近乎即時地存取新資料，則需要使用串流方法。您可以採用兩種方法：

* 使用 Google Cloud 產品設定載入管道。Google 提供了一組[串流 Dataflow 範本](https://docs.cloud.google.com/dataflow/docs/guides/templates/provided-streaming?hl=zh-tw)來協助完成這項工作。
* 使用我們[合作夥伴](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw)提供的解決方案。

在短期內，增加 BigQuery 資料的足跡以及將其用於下游程序的足跡，應該將重點放在滿足您的優先用途，而中期目標是移除現有資料倉儲。請善用初始疊代，不要花費大量資源來把從現有資料倉儲到 BigQuery 的擷取管道改到完善，因為最後還是需要調整這些管道，使其不再使用現有資料倉儲。

### 最佳化結構定義

將資料表依原狀遷移到 BigQuery，可讓您利用其獨特的功能。例如，不需要重建索引或重新排列資料區塊 (「清空」)，也不會因版本升級導致任何停機或效能下降。

不過，在遷移的初始疊代作業之外，保持資料倉儲模型不變也有以下缺點：

* 與結構定義相關的現有問題和技術負債仍存在。
* 查詢最佳化有所限制，如果在稍後階段更新結構定義，則可能需要重做查詢最佳化。
* 無法充分利用其他 BigQuery 功能，例如巢狀和重複欄位、分區和叢集處理。

在進行最終轉移前，建議您對在結構定義中建立的資料表套用分區和叢集，以提升系統效能。

#### 分區

BigQuery 可讓您將資料劃分為多個區段 [(稱為「分區」)](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)，讓資料的管理和查詢更容易也更有效率。您可以根據 [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type) 或 [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type) 資料欄將資料表分區，BigQuery 也可以新增虛擬資料欄，用於在擷取期間自動將資料分區。需要較小分區的查詢，效能較高，因為只會掃描資料子集，並且可透過將讀取的位元組數降至最低的方式來降低費用。

分區並不會影響資料表的現有結構。因此，即使未修改結構定義，仍應考慮建立分區資料表。

#### 分群

在 BigQuery 中，不會使用索引來查詢資料。BigQuery 的基礎模型、儲存和查詢技術，以及大規模平行架構，都經過最佳化調整，可提供優異效能。執行查詢時，處理的資料越多，同時新增到掃描資料和匯總結果的機器就越多。
當資料集很大時，上述方式可隨之調度因應，不會出現處理問題，但索引重建就無法擴充自如。

不過，還是有進一步最佳化查詢的空間，也就是透過[叢集處理](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)這類技術。
透過叢集處理，BigQuery 會根據您指定的幾個資料欄值，自動排序資料，並將它們並置於最佳大小的區塊中。與未使用叢集處理的狀況相較，使用這類處理可以提高查詢效能。經過叢集處理後，BigQuery 可以更準確地估計執行查詢的費用，使用叢集資料欄時，查詢也會排除不必要資料的掃描，並且可以更快計算匯總，因為區塊會將含有近似值的記錄並置。

檢查常用於篩選的資料欄查詢，並在這些資料欄中利用叢集處理建立資料表。如要進一步瞭解叢集，請參閱[叢集資料表簡介](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。

### 去標準化

資料遷移是疊代程序。
因此，一旦您將初始結構定義搬移至雲端、執行輕量最佳化並測試了一些關鍵用途，就可能需要探索可從 BigQuery 基礎設計中受益的其他功能，其中包括巢狀和重複欄位。

資料倉儲結構定義歷來使用下列模型：

* [星形結構定義](https://wikipedia.org/wiki/Star_schema)：
  這是一個去標準化的模型，其中資訊資料表會收集如訂單金額、折扣和數量等指標，以及一組索引鍵。這些索引鍵屬於維度資料表，例如客戶、供應商、地區等。就圖形方面，此模型像一個星形，中心的資訊資料表被維度資料表所環繞。
* [雪花形結構定義](https://wikipedia.org/wiki/Snowflake_schema)：
  這與星形結構定義類似，但它的維度資料表已標準化，為結構定義提供了獨特雪花的外觀。

BigQuery 支援星形和雪花形結構定義，但其原生結構定義表示法並非這兩種結構定義。相反的，它使用[巢狀和重複欄位](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw)，以便更自然地呈現資料。詳情請參閱 BigQuery 說明文件中的[範例結構定義](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw#example_schema)。

變更結構定義以使用巢狀和重複的欄位是一個很好的改進選擇，這樣可減少查詢所需的彙整數量，並使結構定義與 BigQuery 內部資料表示法一致。在內部，BigQuery 使用 [Dremel 模型](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets/?hl=zh-tw)組織資料，並以名為 [Capacitor](https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw) 的資料欄形式儲存格式儲存。

如要針對個案判斷最佳去標準化方法，請考慮在 BigQuery 中[使用巢狀和重複欄位](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-nested?hl=zh-tw)，以及[處理結構定義變更](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)的技巧。

## 後續步驟

進一步瞭解資料倉儲遷移作業的下列步驟：

* [遷移作業總覽](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw)
* [遷移評估](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)
* [資料管道](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw)
* [批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)
* [互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)
* [資安與資管](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)
* [資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator#data-validation-tool)

您也可以瞭解如何從特定資料倉儲技術遷移到 BigQuery：

* [從 Netezza 遷移](https://docs.cloud.google.com/architecture/dw2bq/netezza/netezza-bq-migration-guide?hl=zh-tw)
* [從 Oracle 遷移](https://docs.cloud.google.com/bigquery/docs/migration/oracle-migration?hl=zh-tw)
* [從 Amazon Redshift 遷移](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw)
* [從 Teradata 遷移](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw)
* [從 Snowflake 遷移](https://docs.cloud.google.com/architecture/dw2bq/snowflake/snowflake-bq-migration-guide?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]