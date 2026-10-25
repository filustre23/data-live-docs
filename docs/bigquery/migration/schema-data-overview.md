Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 結構定義與資料移轉總覽

本文件探討將結構定義和資料從現有資料倉儲移轉至 BigQuery 的概念和工作。

將資料倉儲遷移至雲端是一個複雜的過程，需要規劃、資源和時間。為克服這項複雜問題，您應分階段反覆執行資料倉儲遷移作業。多次疊代結構定義和資料遷移，可改善結果。

## 結構定義和資料遷移程序

在遷移作業開始時，您有上游系統會將資料饋送至現有的資料倉儲，以及下游系統會使用該資料製作報表、資訊主頁，以及做為其他程序的動態饋給。

這種一般的資料流動支援許多分析[用途](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#use-case)，如下圖所示：

此過程的結束狀態是盡可能在 BigQuery 上執行更多的用途。這個狀態可讓您盡可能減少使用現有的資料倉儲，並最終將其淘汰。在遷移的[準備和探索](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#prepare-and-discover)階段，您可以排定用途的優先順序，控管要遷移哪些用途以及遷移時間。

### 將結構定義和資料移轉至 BigQuery

在遷移的[規劃](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#plan)階段，您會找出要遷移的用途。接著，您會在[執行](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#execute)階段開始遷移疊代。如要管理疊代，同時以盡可能避免服務中斷的方式執行分析環境，請遵循以下高階流程：

1. 轉移資料表並設定和測試下游程序。

   * 使用 BigQuery 資料移轉服務或其他 ETL 工具，將每個用途的資料表群組原封不動地轉移至 BigQuery。如要瞭解工具，請參閱[初始資料移轉](#initial-data-transfer)一節。
   * 設定要讀取 BigQuery 資料表的下游程序的測試版本。

   這個初始步驟會劃分資料流動過程，下圖顯示產生的流動過程。現在，有部分下游系統會讀取 BigQuery，如標為 B 的流程所示。其他則仍從現有資料倉儲讀取，如標示為 A 的流程所示。
2. 設定一些測試上游程序，將資料寫入 BigQuery 資料表，而非 (或除了) 現有資料倉儲。

   測試之後，設定實際工作環境上游和下游程序以寫入和讀取 BigQuery 資料表。這些程序可以使用 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference?hl=zh-tw) 連線至 BigQuery，並整合[數據分析](https://lookerstudio.google.com/?hl=zh-tw)和 [Dataflow](https://docs.cloud.google.com/dataflow/docs?hl=zh-tw) 等新雲端產品。

   此時，您有三個資料流動過程：

   1. 現有。資料和程序維持不變，仍以現有資料倉儲為中心。
   2. [卸載](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#offload)。
      上游程序會將資料饋送至現有的資料倉儲，資料會卸載至 BigQuery，然後饋送至下游程序。
   3. [完全遷移](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#full-migration)。
      上游和下游程序不會再寫入或讀取現有資料倉儲。

      下圖是具有全部三個流動過程的系統：
3. 選取其他用途以進行遷移作業，然後前往步驟 1 開始新的[執行疊代作業](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#migrating-using-an-iterative-approach)。
   繼續疊代完成這些步驟，直到所有用途全都遷移到 BigQuery 中。選取用途時，您可以重新查看仍處於卸載狀態的用途，以便將其移至完全遷移狀態。對於已完全遷移的用途，請考慮按照「[在 BigQuery 中演進結構定義](#evolving_your_schema_in_bigquery)」中的指南，繼續演進程序。

### 在 BigQuery 中演進結構定義

資料倉儲的結構定義會對資料結構以及資料實體之間的關係給予定義。結構定義是資料設計的核心，因此會影響上游和下游的許多程序。

資料倉儲遷移作業提供了一個獨特的機會，可以對轉移到 BigQuery 之後的結構定義進行改進。本節提供一系列步驟做為改進結構定義的指導方針，這些指導方針可以幫助您在變更結構定義期間，保持資料倉儲環境的運作，同時將上游和下游程序的中斷情況降至最低。

本節中的步驟主要針對單一用途進行結構定義的轉換。

視您想要的改進程度而定，您可以停在某個中間步驟，或是繼續進行到系統完全改進為止。

1. 將用途原封不動地轉移至 BigQuery。

   在繼續執行後續步驟之前，請確保用途的上游和下游程序已在寫入和讀取 BigQuery。不過，也有可能從只有下游程序在讀取 BigQuery 的中間狀態開始。在這種情況下，請您只運用下游部分的指導方針。在下圖的範例用途中，上游和下游程序會對 BigQuery 資料表進行寫入和讀取。
2. 套用輕量最佳化。

   1. 重新建立資料表，並套用[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。針對這項工作，您可以使用從查詢結果建立資料表的方法。詳情請參閱分區資料表的[討論](https://docs.cloud.google.com/bigquery/docs/creating-column-partitions?hl=zh-tw#creating_a_partitioned_table_from_a_query_result)和[範例](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_partitioned_table_from_the_result_of_a_query)，以及分群資料表的[討論](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw#create_a_clustered_table_from_a_query_result)和[範例](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#creating_a_clustered_table_from_the_result_of_a_query)。
   2. 將上游和下游程序重新導向至新資料表。
3. 建立外觀檢視畫面。

   如要進一步調整結構定義，而不只是進行輕度最佳化，請為資料表建立*外觀檢視畫面*。[外觀模式](https://wikipedia.org/wiki/Facade_pattern)是一種設計方法，可遮蓋基礎程式碼或結構，隱藏複雜性。在這種情況下，門面檢視表會遮蓋基礎資料表，隱藏資料表變更對下游程序造成的複雜性。

   檢視表可以描述新的結構定義，不受技術債影響，並以新的擷取和使用情境為考量進行建模。

   就運作原理來看，資料表和檢視表查詢的定義本身可以變更。但是這些檢視表會將這些變更提取出來做為資料倉儲的內部實作詳細資料，並且始終會傳回相同的結果。這個由外觀檢視表組成的[抽象層](https://wikipedia.org/wiki/Abstraction_layer)，可視需要將上游和下游系統與變更隔離，並僅在適當的時候顯示變更。
4. 轉換下游程序。

   您可以轉換部分下游程序，從外觀檢視表 (而非實際資料表) 讀取資料。這時這些程序已經從改進的結構定義中受益。對這些程序來說，外觀檢視表在幕後仍從來源 BigQuery 結構定義取得資料，如下圖所示：

   我們已經先說明下游程序轉換，比起轉換非技術相關人員無法看見的上游程序，這可讓您以遷移後的資訊主頁或報表形式更快顯示商業價值。不過，您也可以改用上游程序來進行轉換。這些工作的優先順序完全取決於您的需求。
5. 轉換上游程序。

   您可以將部分上游程序轉換為寫入新的結構定義。由於檢視表為唯讀，因此您會根據新的結構定義建立資料表，然後修改 facade 檢視表的查詢定義。部分檢視表仍會查詢來源結構定義，其他檢視表則會查詢新建立的資料表，或對兩者執行 SQL `UNION` 作業，如下圖所示：

   此時，您可以在建立新資料表時，利用[巢狀和重複欄位](#denormalization)。如此一來，您可以進一步將模型去標準化，並直接利用 BigQuery 底層直欄式的資料表示法。

   門面檢視表的優點是，下游程序可以繼續轉換，不受這些基礎結構定義變更和上游程序變更的影響。
6. 完全改進您的用途。

   最後，您可以轉換其餘的上游和下游程序。當所有這些項目都演變為寫入新資料表並從新的外觀檢視表讀取時，您需要修改外觀檢視表的查詢定義，不再從來源結構定義讀取。接著，您可以從資料流程中淘汰來源模型中的資料表。下圖顯示不再使用來源資料表的狀態。

   如果 facade 檢視表不會匯總欄位或篩選資料欄，您可以將下游程序設為從演進後的資料表讀取資料，然後停用 facade 檢視表以降低複雜度，如下圖所示：

## 初步移轉結構定義和資料

本節說明將結構定義和資料從現有資料倉儲遷移至 BigQuery 的實際考量。

建議您在遷移作業的初始疊代期間，不對結構定義進行任何變更，直接轉移結構定義。這項做法有以下優點：

* 無需針對新結構定義調整動態饋給資料倉儲的資料管道。
* 可避免在員工的訓練資料清單中加入新的結構定義。
* 可利用自動化工具執行結構定義與資料移轉作業。

此外，使用雲端功能的概念驗證 (PoC) 和其他資料探索活動也可以順暢無礙地進行，即使遷移作業同時進行。

### 選擇轉移方法

您可以採用多種方法之一進行初始移轉。

* 如果是 Amazon Redshift 和 Teradata 資料倉儲，您可以使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，直接將現有系統的結構定義和資料載入 BigQuery。Cloud Storage 仍會用於在遷移過程中暫存資料。
* 無論是哪種資料倉儲，您都可以擷取包含結構定義和資料的檔案，將這些檔案上傳至 Cloud Storage，然後使用下列其中一個選項，將這些檔案中的結構定義和資料載入 BigQuery：
  + [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)
  + [BigQuery Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)
  + [批次載入](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)

如要進一步瞭解選擇資料移轉方法時的考量事項，請參閱「[選擇資料擷取方法](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw#methods)」。

### 考慮轉換資料

視資料擷取格式，以及是否要在將資料載入 BigQuery 前，先修剪或充實資料而定，您可能需要加入轉換資料的步驟。您可以在現有環境或 Google Cloud中轉換資料：

* 如果您在目前的環境中轉換資料，請考量可用的運算能力和工具可能會如何限制處理量。此外，如果您在轉換過程中充實資料，請考量是否需要額外的傳輸時間或網路頻寬。
* 如果您在 Google Cloud上轉換資料，請參閱「[使用 ETL 工具載入資料](#load_data_using_an_etl_tool)」，進一步瞭解相關選項。

### 將現有結構定義和資料擷取至檔案

您現有的平台可能提供工具，可將資料匯出為不限供應商的格式，例如 [Apache AVRO](https://avro.apache.org/docs/current/) 或 CSV。為降低移轉複雜度，建議使用 AVRO、[ORC](https://orc.apache.org/) 或 [Parquet](https://parquet.apache.org/)，這些格式會將結構定義資訊嵌入資料中。如果選擇 CSV 或類似的簡單分隔資料格式，則必須另外指定結構定義。具體做法取決於您選取的資料移轉方法。
舉例來說，如果是批次上傳，您可以在載入時指定結構定義，或允許系統根據 CSV 檔案內容自動偵測結構定義。

從現有平台擷取這些檔案時，請將檔案複製到現有環境中的暫存儲存空間。

### 將檔案上傳至 Cloud Storage

除非您使用 BigQuery 資料移轉服務，直接從現有的 Amazon Redshift 或 Teradata 資料倉儲載入資料，否則必須將擷取的檔案上傳至 Cloud Storage 中的 bucket。視要移轉的資料量和可用的網路頻寬而定，您可以選擇下列移轉選項：

* 如果您擷取的資料位於其他雲端供應商處，請使用 [Storage 移轉服務](https://docs.cloud.google.com/storage/transfer?hl=zh-tw)。
* 如果資料位於地端部署環境或網路頻寬良好的主機代管機房，請使用 [Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)。gcloud CLI 支援多執行緒平行上傳，可在發生錯誤後繼續上傳，並會加密傳輸中的流量，確保安全。

  + 如果無法使用 gcloud CLI，可以嘗試 Google 合作夥伴提供的[第三方](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw#third-party_tools)工具。
  + 如果網路頻寬有限，您可以使用[壓縮技術](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw#decrease_data_size)限制資料大小，也可以修改目前的 Google Cloud 連線，[增加頻寬](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw#increase_network_bandwidth)。
* 如果無法取得足夠的網路頻寬，您可以使用 [Transfer Appliance](https://docs.cloud.google.com/transfer-appliance?hl=zh-tw) 執行離線移轉作業。

建立 Cloud Storage bucket 並透過網路移轉資料時，請選擇最靠近資料中心的位置，盡可能縮短網路延遲時間。如果可以，請[選擇與 BigQuery 資料集相同的位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#data-locations)。

如要進一步瞭解將資料移至 Cloud Storage 的最佳做法 (包括預估費用)，請參閱「[移轉大型資料集的策略](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw)」。

### 將結構定義和資料載入 BigQuery

使用「[選擇移轉方法](#choose_a_transfer_method)」中討論的其中一種選項，將結構定義和資料載入 BigQuery。

如要進一步瞭解一次性載入，請參閱 BigQuery 說明文件中的「[從 Cloud Storage 載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage?hl=zh-tw)」。如要進一步瞭解定期排定的載入作業，請參閱 BigQuery 資料移轉服務說明文件中的「[Cloud Storage 資料移轉簡介](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw)」一節。

#### 使用 ETL 工具載入資料

如果資料在載入 BigQuery 時需要進一步轉換，請使用下列其中一個選項：

* [Cloud Data Fusion](https://docs.cloud.google.com/data-fusion/docs?hl=zh-tw)：
  這個工具使用內含預先設定連接器和轉換的開放原始碼程式庫，以圖形方式建構全代管 ETL/ELT 資料管道。
* [Dataflow](https://docs.cloud.google.com/dataflow/docs?hl=zh-tw)。這項工具會使用 [Apache Beam](https://beam.apache.org/) 模型，定義及執行複雜的資料轉換和擴充圖。Dataflow 是無伺服器服務，由 Google 全代管，可提供近乎無限的處理能力。
* [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc/docs?hl=zh-tw)。這個工具會在全代管雲端服務上執行 Apache Spark 和 Apache Hadoop 叢集。
* 第三方工具。與我們的[合作夥伴](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw)聯絡。當您想要將資料管道的建構外部化時，他們可以提供各種有效的選擇。

下圖呈現了本節所述的模式。資料移轉工具是 [gcloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)，其中包含轉換步驟，可運用 Dataflow 並直接寫入 BigQuery，可能使用 Apache Beam 內建的 [Google BigQuery I/O 連接器](https://beam.apache.org/documentation/io/built-in/google-bigquery/)。

將初始資料集載入 BigQuery 後，您就可以開始利用 [BigQuery 的強大功能](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)。

但是，就如您轉移結構定義時一樣，上傳資料也是疊代程序的一部分。後續疊代作業可以從擴大轉移至 BigQuery 的資料足跡開始，接著，您可以將上游資料動態饋給重新轉送至 BigQuery，這樣就不必繼續執行現有的資料倉儲。下一節將探討這些主題。

### 驗證資料

資料已存入 BigQuery，現在可以使用 [Data Validation Tool](https://github.com/GoogleCloudPlatform/professional-services-data-validator) (DVT) 確認資料是否成功移轉。DVT 是開放原始碼的 Python CLI 工具，可讓您比較各種來源的資料與 BigQuery 中的目標資料。您可以指定要執行的匯總作業 (例如計數、加總、平均)，以及要套用這些作業的資料欄。詳情請參閱「[使用 DVT 自動驗證資料](https://cloud.google.com/blog/products/databases/automate-data-validation-with-dvt?hl=zh-tw)」。

## 反覆執行初始轉移作業

本節說明在初始資料移轉後如何繼續操作，以便充分利用 BigQuery。

資料子集現在已位於 BigQuery 中。您正準備增加 BigQuery 中使用的資料量，進而減少對現有資料倉儲的依賴。

您為後續疊代作業選擇什麼方法，會取決於對您的用途而言，將資料更新到目前這一秒有多重要。如果資料分析師可以定期重複處理合併到資料倉儲中的資料，則可以選擇已排定時間的選項。您可以透過與初始移轉作業類似的方式建立排定的移轉作業，您可以使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw)、其他 ETL 工具 (例如 Google 的 [Storage 移轉服務](https://docs.cloud.google.com/storage/transfer?hl=zh-tw))，或[第三方](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw#third-party_tools)實作。

如果您使用 BigQuery 資料移轉服務，首先要決定要移動的資料表，然後建立資料表名稱模式來納入這些資料表。最後，您設定了週期性排程，指定執行移轉作業的時間。

另一方面，如果您的用途需要近乎即時地存取新資料，則需要使用串流方法。您可以採用兩種方法：

* 使用 Google Cloud 產品設定載入管道。Google 提供一組[串流 Dataflow 範本](https://docs.cloud.google.com/dataflow/docs/guides/templates/provided-streaming?hl=zh-tw)，可協助您完成這項工作。
* 使用[合作夥伴](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw)提供的解決方案。

短期內，增加 BigQuery 資料的使用範圍並用於下游程序時，應著重於滿足優先順序最高的使用案例，中期目標則是停用現有的資料倉儲。請妥善運用初始疊代，不要花費大量資源，將現有資料倉儲中的擷取管道完美遷移至 BigQuery。最終，您需要調整這些管道，不使用現有的資料倉儲。

### 盡可能改良結構定義

只要將資料表原封不動地遷移至 BigQuery，即可運用其獨特功能。例如，不需要重建索引或重新排列資料區塊 (「清空」)，也不會因版本升級導致任何停機或效能下降。

不過，在遷移的初始疊代作業之外，保持資料倉儲模型不變也有以下缺點：

* 與結構定義相關的現有問題和技術債仍會存在。
* 查詢最佳化有所限制，如果在稍後階段更新結構定義，則可能需要重做查詢最佳化。
* 無法充分利用其他 BigQuery 功能，例如巢狀和重複欄位、分區和叢集處理。

在進行最終轉移作業時，建議您對結構定義中建立的資料表套用分區和分群，以提升系統效能。

#### 分區

BigQuery 可讓您將資料劃分為多個區段 [(稱為「分區」)](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)，讓資料的管理和查詢更容易也更有效率。您可以根據 [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type) 或 [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type) 資料欄將資料表分區，或讓 BigQuery 新增虛擬資料欄，在擷取期間自動將資料分區。需要較小分區的查詢，效能較高，因為只會掃描資料子集，並且可透過將讀取的位元組數降至最低的方式來降低費用。

分區並不會影響資料表的現有結構。因此，即使未修改結構定義，也建議您建立分區資料表。

#### 分群

在 BigQuery 中，系統不會使用任何索引來查詢資料。BigQuery 的效能是透過基礎模型、儲存和查詢技術，以及大規模平行架構進行最佳化。執行查詢時，處理的資料越多，同時新增到掃描資料和匯總結果的機器就越多。
當資料集很大時，上述方式可隨之調度因應，不會出現處理問題，但索引重建就無法擴充自如。

不過，還是有進一步最佳化查詢的空間，也就是透過[叢集處理](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)這類技術。
透過叢集處理，BigQuery 會根據您指定的幾個資料欄值，自動排序資料，並將它們並置於最佳大小的區塊中。與未使用叢集處理的狀況相較，使用這類處理可以提高查詢效能。經過叢集處理後，BigQuery 可以更準確地估計執行查詢的費用，使用叢集資料欄時，查詢也會排除不必要資料的掃描，並且可以更快計算匯總，因為區塊會將含有近似值的記錄並置。

檢查常用於篩選的資料欄查詢，並在這些資料欄中利用叢集處理建立資料表。如要進一步瞭解分群，請參閱「[分群資料表簡介](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)」。

### 去標準化

資料遷移是反覆進行的程序。因此，一旦您將初始結構定義搬移至雲端、執行輕量最佳化並測試了一些關鍵用途，就可能需要探索可從 BigQuery 基礎設計中受益的其他功能，其中包括巢狀和重複欄位。

資料倉儲結構定義歷來使用下列模型：

* [星形結構定義](https://wikipedia.org/wiki/Star_schema)：
  這是一個去標準化的模型，其中資訊資料表會收集如訂單金額、折扣和數量等指標，以及一組索引鍵。這些索引鍵屬於維度資料表，例如客戶、供應商、地區等。就圖形方面，此模型像一個星形，中心的資訊資料表被維度資料表所環繞。
* [雪花形結構定義](https://wikipedia.org/wiki/Snowflake_schema)：
  這與星形結構定義類似，但它的維度資料表已標準化，為結構定義提供了獨特雪花的外觀。

BigQuery 支援星形和雪花形結構定義，但其原生結構定義表示法並非這兩種結構定義。而是使用[巢狀和重複欄位](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw)，以更自然的方式呈現資料。詳情請參閱 BigQuery 說明文件中的[結構定義範例](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw#example_schema)。

變更結構定義以使用巢狀和重複的欄位是一個很好的改進選擇，這樣可減少查詢所需的彙整數量，並使結構定義與 BigQuery 內部資料表示法一致。在內部，BigQuery 使用 [Dremel 模型](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets/?hl=zh-tw)組織資料，並以名為 [Capacitor](https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw) 的資料欄形式儲存格式儲存。

如要決定最適合您情況的反正規化方法，請考慮在 BigQuery 中[使用巢狀和重複欄位](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-nested?hl=zh-tw)，以及[處理結構定義變更](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)的技術。

## 後續步驟

進一步瞭解資料倉儲遷移作業的下列步驟：

* [遷移作業總覽](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw)
* [遷移評估](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)
* [資料管道](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw)
* [批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)
* [互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)
* [資料安全性與管理](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)
* [資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator#data-validation-tool)

您也可以瞭解如何從特定資料倉儲技術遷移至 BigQuery：

* [從 Netezza 遷移](https://docs.cloud.google.com/architecture/dw2bq/netezza/netezza-bq-migration-guide?hl=zh-tw)
* [從 Oracle 遷移](https://docs.cloud.google.com/bigquery/docs/migration/oracle-migration?hl=zh-tw)
* [從 Amazon Redshift 遷移](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw)
* [從 Teradata 遷移](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw)
* [從 Snowflake 遷移](https://docs.cloud.google.com/architecture/dw2bq/snowflake/snowflake-bq-migration-guide?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]