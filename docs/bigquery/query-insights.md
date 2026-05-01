* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 取得查詢效能洞察資料

查詢的*執行圖*會以視覺化方式呈現 BigQuery 執行查詢的步驟。本文說明如何使用查詢執行圖診斷查詢效能問題，以及如何查看查詢效能深入分析。

BigQuery 的查詢效能十分優異，但也是複雜的分散式系統，許多內外部因素都會影響查詢速度。SQL 的宣告式性質也可能隱藏查詢執行的複雜度。也就是說，如果查詢的執行速度比預期慢，或比先前的執行速度慢，您可能難以瞭解發生了什麼事。

查詢執行圖提供動態圖形介面，可檢查查詢計畫和查詢效能詳細資料。您可以查看任何執行中或已完成查詢的查詢執行圖。

您也可以使用查詢執行圖，取得查詢的效能洞察資料。效能深入分析會提供最佳效能建議，協助您提高查詢效能。由於查詢效能涉及多個層面，效能深入分析可能只會顯示查詢效能的局部資訊，而非整體情況。

## 所需權限

如要使用查詢執行圖表，您必須具備下列權限：

* `bigquery.jobs.get`
* `bigquery.jobs.listAll`

您可以透過下列 BigQuery 預先定義的 Identity and Access Management (IAM) 角色取得這些權限：

* `roles/bigquery.admin`
* `roles/bigquery.resourceAdmin`
* `roles/bigquery.resourceEditor`
* `roles/bigquery.resourceViewer`

## 執行圖結構

查詢執行圖表會以圖形呈現主控台中的查詢計畫。每個方塊代表查詢計畫中的一個[階段](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw#stage-overview)，例如：

* **輸入**：從表格讀取資料或選取特定欄
* **聯結**：根據 `JOIN` 條件合併兩個資料表的資料
* **匯總**：執行 `SUM` 等計算
* **排序**：排列結果順序

階段由「步驟」組成，說明每個工作站在階段中執行的個別作業。按一下階段即可開啟並查看步驟。階段也包含[相對和絕對時間碼資訊](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw#per-stage_timing_classification)。階段名稱會歸納他們執行的步驟。舉例來說，如果階段名稱包含「join」，表示該階段的主要步驟是 `JOIN` 作業。如果階段名稱結尾有 `+`，表示該階段會執行額外的重要步驟。舉例來說，如果階段名稱包含 `JOIN+`，表示該階段會執行聯結作業和其他重要步驟。

連接階段的線條代表階段間的中介資料交換。BigQuery 會在階段執行時，將中繼資料儲存在重組記憶體中。邊緣的數字表示各階段之間交換的預估列數。Shuffle 記憶體配額與分配給帳戶的運算單元數量相關。如果超過重組配額，重組記憶體可能會溢出到磁碟，導致查詢效能大幅降低。

## 查看查詢成效洞察

### 控制台

如要查看查詢成效洞察，請按照下列步驟操作：

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中，按一下「Job history」。
4. 按一下「個人記錄」或「專案記錄」。
5. 在工作清單中，找出您感興趣的查詢工作。按一下
   more\_vert
   「動作」，然後選擇「在編輯器中查看工作」。
6. 選取「執行圖」分頁，即可查看查詢各階段的圖表：

   如要判斷查詢階段是否有效能洞察，請查看顯示的圖示。如果階段有info\_outline
   資訊圖示，表示有可用的效能洞察資料。有check\_circle\_outline勾號圖示的階段則沒有。
7. 按一下階段即可開啟階段詳細資料窗格，查看下列資訊：

   * 階段的[查詢計畫資訊](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw#query_plan_information)。
   * 在階段中執行的[步驟](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw#per-stage_step_information)。
   * 任何適用的成效洞察資料。
8. 選用：如要檢查正在執行的查詢，請按一下「同步」sync，更新執行圖表，反映查詢的目前狀態。
9. 選用：如要在圖表上醒目顯示持續時間最長的階段，請按一下「醒目顯示持續時間最長的階段」。
10. 選用：如要在圖表中醒目顯示使用最多時段的階段，請按一下「醒目顯示處理時間最長的階段」。
11. 選用：如要在圖表中加入重組重新分配階段，請按一下「顯示重組重新分配階段」。

    使用這個選項可顯示預設執行圖中隱藏的重新分割和合併階段。

    查詢執行期間會引進重新分區和合併階段，用來改善處理查詢的工作站之間的資料分布狀況。由於這些階段與查詢文字無關，因此系統會隱藏這些階段，簡化顯示的查詢計畫。

如有任何查詢發生成效回歸問題，查詢的「工作資訊」分頁也會顯示成效深入分析：

### SQL

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     `bigquery-public-data`.persistent_udfs.job_url(
       project_id || ':us.' || job_id) AS job_url,
     query_info.performance_insights
   FROM
     `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
   WHERE
     DATE(creation_time) >= CURRENT_DATE - 30 -- scan 30 days of query history
     AND job_type = 'QUERY'
     AND state = 'DONE'
     AND error_result IS NULL
     AND statement_type != 'SCRIPT'
     AND EXISTS ( -- Only include queries which had performance insights
       SELECT 1
       FROM UNNEST(
         query_info.performance_insights.stage_performance_standalone_insights
       )
       WHERE
         slot_contention
         OR insufficient_shuffle_quota
         OR bi_engine_reasons IS NOT NULL
         OR high_cardinality_joins IS NOT NULL
         OR partition_skew IS NOT NULL
       UNION ALL
       SELECT 1
       FROM UNNEST(
         query_info.performance_insights.stage_performance_change_insights
       )
       WHERE input_data_change.records_read_diff_percentage IS NOT NULL
     );
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### API

您可以呼叫 [`jobs.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/list?hl=zh-tw) API 方法，並檢查傳回的 [`JobStatistics2`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobStatistics2) 資訊，以非圖形格式取得查詢成效洞察資料。

## 解讀查詢效能洞察資料

請參閱本節，進一步瞭解成效洞察資料的意義，以及如何解決相關問題。

成效洞察資訊適用於兩類使用者：

* 分析師：您可以在專案中執行查詢。您想瞭解先前執行的查詢為何執行速度變慢，並取得提升查詢效能的訣竅。您具備「[必要權限](#required_permissions)」一節所述的權限。
* 資料湖泊或資料倉儲管理員：管理貴機構的 BigQuery 資源和預留項目。您具備與 [BigQuery 管理員角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)相關聯的權限。

以下各節將根據您的角色，提供如何因應成效洞察的指引。

### 運算單元爭用情況

執行查詢時，BigQuery 會嘗試將查詢所需的工作分解為*工作*。工作是指單一資料切片，會輸入至階段並從階段輸出。單一時段會擷取工作，並執行該階段的資料切片。理想情況下，BigQuery [slot](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw) 會平行執行這些工作，以達到高效能。當查詢有許多工作準備開始執行，但 BigQuery 無法取得足夠的可用運算單元來執行這些工作時，就會發生運算單元爭用情形。

#### 分析師的處置方式

請按照「[減少查詢處理的資料量](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-communication?hl=zh-tw)」一文中的操作說明，減少查詢處理的資料量。

#### 如果您是管理員

採取下列行動，增加運算單元可用性或減少運算單元用量：

* 如果您使用 BigQuery 的[以量計價方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)，查詢會使用共用的運算單元集區。建議您改為購買[預訂](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，並採用[以容量為準的分析價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。您可以透過保留項目，為貴機構的查詢預留專屬運算單元。
* 如果您使用 BigQuery 預留項目，請確認指派給執行查詢專案的預留項目有足夠的運算單元。在下列情況下，預留項目可能沒有足夠的運算單元：

  + 有其他工作正在使用預留運算單元。
    您可以使用[管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)，查看貴機構的預訂使用情況。
  + 預留項目分配的運算單元不足，無法快速執行查詢。您可以使用[時段預估工具](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)，預估保留時段的大小，以便有效處理查詢工作。

  如要解決這個問題，請嘗試下列任一方法：

  + 在該預留項目中新增更多運算單元 (基準運算單元或預留項目的運算單元數量上限)。
  + 建立額外預留項目，並指派給執行查詢的專案。
  + 請將耗用大量資源的查詢分散到一段時間內 (在預留空間內)，或分散到不同的預留空間。
* 確認您查詢的資料表是[叢集資料表](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。分群功能可確保 BigQuery 能快速讀取具有相關資料的資料欄。
* 確認您查詢的資料表已[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。如果是未經分割的資料表，BigQuery 會讀取整個資料表。分區資料表可確保您只查詢感興趣的資料表子集。

### 重組配額不足

執行查詢前，BigQuery 會[將查詢邏輯分解為*階段*](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw#background)。BigQuery 運算單元會執行每個階段的作業。運算單元完成階段工作的執行作業後，會將中間結果儲存在 [shuffle](https://cloud.google.com/blog/products/bigquery/in-memory-query-execution-in-google-bigquery?hl=zh-tw) 中。查詢中的後續階段會從重組讀取資料，繼續執行查詢。如果需要寫入重組的資料量超過重組容量，就會發生重組配額不足的情況。

#### 分析師的處置方式

與時段爭用類似，減少查詢處理的資料量可能會降低隨機播放的使用量。如要減少查詢處理的資料量，請按照「[減少查詢處理的資料量](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-communication?hl=zh-tw)」一文中的操作說明進行。

SQL 中的某些作業會大量使用 Shuffle，尤其是 [`JOIN` 作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)和 [`GROUP BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#group_by_clause)。盡可能減少這些作業中的資料量，或許就能減少隨機重組的使用量。

#### 如果您是管理員

如要減少隨機重組配額爭用情形，請採取下列動作：

* 與運算單元爭用類似，如果您使用 BigQuery 的[以量計價方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)，查詢會使用共用的運算單元集區。建議您改為購買[預訂](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，並採用[以容量為準的分析價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。預留項目可為專案查詢提供專屬運算單元和重組容量。
* 如果您使用 BigQuery 預留項目，運算單元會提供專屬的隨機重組容量。如果保留項目正在執行大量使用 Shuffle 的查詢，可能會導致平行執行的其他查詢無法取得足夠的 Shuffle 容量。如要找出大量使用 Shuffle 容量的工作，請查詢 [`INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視區塊中的 `period_shuffle_ram_usage_ratio` 資料欄](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw)。

  如要解決這個問題，請嘗試下列一或多個解決方案：

  + 在該預訂項目中新增更多運算單元。
  + 建立額外預留項目，並指派給執行查詢的專案。
  + 將需要大量重組的查詢分散到保留項目內的不同時間，或分散到不同保留項目。

如需其他疑難排解資訊，請參閱 BigQuery 疑難排解頁面的「[Shuffle size limit errors](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw#ts-shuffle-limit-errors)」(Shuffle 大小限制錯誤)。

### 資料輸入規模調整

如果收到這項效能深入分析資訊，表示查詢讀取特定輸入資料表的資料量，比上次執行查詢時多出至少 50%。您可以查看[資料表變更記錄](https://docs.cloud.google.com/bigquery/docs/change-history?hl=zh-tw)，瞭解查詢中使用的任何資料表大小是否最近有所增加。

#### 分析師的處置方式

請按照「[減少查詢處理的資料量](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-communication?hl=zh-tw)」一文中的操作說明，減少查詢處理的資料量。

### 高基數聯結

如果查詢包含的聯結在聯結兩端都有重複的鍵，輸出資料表的大小可能會遠大於任一輸入資料表。這項洞察資訊表示輸出資料列與輸入資料列的比率偏高，並提供這些資料列的計數資訊。

#### 分析師的處置方式

檢查聯結條件，確認輸出表格大小增加是預期行為。避免使用[交叉聯結](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#cross_join)。
如果必須使用 cross join，請嘗試使用 `GROUP BY` 子句預先匯總結果，或使用 window 函式。詳情請參閱「[減少使用 `JOIN` 前的資料量](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-communication?hl=zh-tw#reduce_data_before_using_a_join)」。

### 分區偏差

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要提供意見或要求這項功能的支援服務，請傳送電子郵件至 [`bq-query-inspector-feedback@google.com`](mailto:%0Abq-query-inspector-feedback@google.com)。

資料分布不均可能會導致查詢速度緩慢。查詢執行時，BigQuery 會將資料分割成小分區，以便平行處理。如果資料在這些分區中分布不均，就會發生傾斜，通常是因為聯結或分組鍵中經常出現值，導致某些分區明顯大於其他分區。由於單一運算單元會處理整個分區，且無法共用工作，因此過大的分區可能會導致處理速度變慢、發生「超出資源」錯誤，甚至在極端情況下造成運算單元毀損。

執行 `JOIN` 作業時，BigQuery 會根據聯結鍵，將聯結左右兩側的資料分區。如果分割區過大，BigQuery 會嘗試重新平衡資料。如果偏斜程度過於嚴重，無法完全重新平衡，執行圖表的 `JOIN` 階段就會新增分割區偏斜深入分析。

#### 找出分區偏斜

在 BigQuery Studio 中使用「執行圖」分頁，找出查詢的哪個階段發生分割區傾斜。洞察資料會在舞台上加上旗標。從階段詳細資料中，您可以判斷查詢文字的相關部分和正在處理的資料表。詳情請參閱「[瞭解含有查詢文字的步驟](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw#query_text_heatmap)」。

**範例**

以下查詢會將存放區資訊與檔案資訊聯結。如果某些存放區的檔案數量遠多於其他存放區，就可能發生偏斜。

```
SELECT r.repo_name, COUNT(f.path) AS file_count
FROM `bigquery-public-data.github_repos.sample_repos` AS r
JOIN `bigquery-public-data.github_repos.sample_files` AS f
  ON r.repo_name = f.repo_name
WHERE r.watch_count > 10
GROUP BY r.repo_name
```

彙整索引鍵為 `repo_name`。在 `sample_repos` 資料表中，`repo_name` 應為不重複的值。不過，在 `sample_files` 表格中，`repo_name` 可能會出現多次。如果 `sample_files` 中出現的幾個 `repo_name` 值不成比例地頻繁，就會造成資料偏斜。

如要確認資料是否偏斜，請分析較大資料表中的彙整索引鍵 (在本例中為 `sample_files`) 分布情形。執行下列查詢，評估 `repo_name` 的分布情形：

```
SELECT repo_name, COUNT(*) AS occurrences
FROM `bigquery-public-data.github_repos.sample_files`
GROUP BY repo_name
ORDER BY occurrences DESC
```

如果是非常大的資料表，請使用 [`APPROX_TOP_COUNT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw#approx_top_count) 函式，有效估算最常出現的值。

```
SELECT APPROX_TOP_COUNT(repo_name, 100)
FROM `bigquery-public-data.github_repos.sample_files`
```

如果前幾名的值數量比其他值大上好幾個數量級，就表示資料有偏斜。

#### 降低分區偏差

您可以採用下列策略來解決分割區傾斜問題：

* **盡早篩選資料**。在查詢中盡早套用篩選條件，減少處理的資料量。這項功能可減少與傾斜鍵相關聯的資料列數量，再執行 `JOIN` 或 `GROUP BY` 等作業。
* **分割查詢，找出傾斜的鍵**。如果偏差是由幾個特定鍵值所造成，類似於上述範例中的 `repo_name` 欄位，請考慮分割查詢。將傾斜鍵的資料與其餘資料分開處理，然後使用 `UNION ALL` 合併結果。

  **範例**：隔離常用鍵。

  ```
  -- Query for the skewed key
  SELECT r.repo_name, COUNT(f.path) AS file_count
  FROM `bigquery-public-data.github_repos.sample_repos` AS r
  JOIN `bigquery-public-data.github_repos.sample_files` AS f
    ON r.repo_name = f.repo_name
  WHERE r.watch_count > 10 AND r.repo_name = 'popular_repo'
  GROUP BY r.repo_name

  UNION ALL

  -- Query for all other keys
  SELECT r.repo_name, COUNT(f.path) AS file_count
  FROM `bigquery-public-data.github_repos.sample_repos` AS r
  JOIN `bigquery-public-data.github_repos.sample_files` AS f
    ON r.repo_name = f.repo_name
  WHERE r.watch_count > 10 AND r.repo_name != 'popular_repo'
  GROUP BY r.repo_name
  ```
* **處理 `NULL` 和預設值**：如果主要資料欄中含有大量 `NULL` 或空字串值的資料列，就可能導致資料偏斜。如果不需要這些資料列進行分析，請在 `JOIN` 或 `GROUP BY` 前使用 `WHERE` 子句篩除這些資料列。
* **重新排序作業**：在有多個聯結的查詢中，順序可能很重要。
  如有可能，請在查詢中較早執行聯結，大幅減少資料列數。
* **使用近似函式**：如要匯總偏移資料，請考慮是否可接受近似結果。相較於 [`COUNT(DISTINCT)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#count) 等精確函式，[`APPROX_COUNT_DISTINCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw#approx_count_distinct) 等函式對資料偏斜的容許度較高。

## 解讀查詢階段資訊

除了使用[查詢效能深入分析](#interpret_query_performance_insights)，您也可以在查看查詢階段詳細資料時，參考下列指南，判斷查詢是否有問題：

* 如果一或多個階段的「等待時間 (毫秒)」值高於先前的查詢執行次數：
  + 確認是否有足夠的[時段](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)可供工作負載使用。如果沒有，請在執行耗用大量資源的查詢時進行負載平衡，避免查詢彼此競爭。
  + 如果「等待時間 (毫秒)」值高於單一階段的值，請查看前一階段，瞭解是否出現瓶頸。如果查詢中涉及的資料表資料或結構定義有大幅變更，可能會影響查詢效能。
* 如果某個階段的「Shuffle output bytes」(隨機輸出位元組) 值高於先前的查詢執行作業，或高於前一個階段，請評估該階段處理的步驟，查看是否有任何步驟產生大量資料。其中一個常見原因是步驟處理 [`INNER JOIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#inner_join) 時，聯結兩側都有重複的鍵。這可能會傳回大量非預期資料。
* 使用執行圖，依時間長度和處理程序查看頂端階段。請考量這些資料表產生的資料量，以及是否與查詢中參照的資料表大小相符。如果不是，請檢查這些階段的步驟，看看是否有任何步驟可能會產生非預期的暫時資料量。

## 後續步驟

* 請參閱[查詢最佳化指南](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)，瞭解如何提升查詢效能。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]