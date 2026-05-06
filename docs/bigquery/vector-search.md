Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用向量搜尋功能搜尋嵌入

本教學課程說明如何使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)和選用的[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)，對儲存在 BigQuery 資料表中的嵌入執行[相似度搜尋](https://wikipedia.org/wiki/Similarity_search)。

搭配向量索引使用 `VECTOR_SEARCH` 時，`VECTOR_SEARCH` 會採用[近似最鄰近](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximation_methods)方法提升向量搜尋效能，但會降低[召回率](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall?hl=zh-tw#recallsearch_term_rules)，因此傳回的結果會更近似。如果沒有向量索引，`VECTOR_SEARCH` 會使用[暴力搜尋](https://en.wikipedia.org/wiki/Brute-force_search)來測量每筆記錄的距離。

## 所需權限

如要執行本教學課程，您需要下列 Identity and Access Management (IAM) 權限：

* 如要建立資料集，您必須具備 `bigquery.datasets.create` 權限。
* 如要建立資料表，您必須具備下列權限：

  + `bigquery.tables.create`
  + `bigquery.tables.updateData`
  + `bigquery.jobs.create`
* 如要建立向量索引，您必須具備要建立索引的資料表 `bigquery.tables.createIndex` 權限。
* 如要捨棄向量索引，您必須具備要捨棄索引的資料表 `bigquery.tables.deleteIndex` 權限。

下列每個預先定義的 IAM 角色都包含使用向量索引所需的權限：

* BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)
* BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)

## 費用

`VECTOR_SEARCH` 函式會採用 [BigQuery 運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)。系統會根據以量計價或版本定價，向您收取相似度搜尋費用。

* 以量計價：系統會根據掃描的位元組數向您收費，包括基本資料表、索引和搜尋查詢。
* 方案價格：系統會根據預留方案中完成工作所需的運算單元向您收費。如果相似度計算的範圍較大或較複雜，費用就會較高。

  **注意：** [標準版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)不支援使用索引。

詳情請參閱 [BigQuery 計價方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw)一文。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com&hl=zh-tw)

## 建立資料集

建立 BigQuery 資料集

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下專案名稱。
3. 依序點按 more\_vert「View actions」(查看動作) >「Create dataset」(建立資料集)。
4. 在「建立資料集」頁面中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `vector_search`。
   * 針對「Location type」(位置類型) 選取「Multi-region」(多區域)，然後選取「US (multiple regions in United States)」(us (多個美國區域))。

     公開資料集儲存在 `US`
     [多地區](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)。為簡單起見，請將資料集存放在相同位置。
   * 其餘設定請保留預設狀態，然後按一下「建立資料集」。

## 建立測試資料表

1. 根據 [Google 專利](https://console.cloud.google.com/marketplace/product/google_patents_public_datasets/google-patents-public-data?hl=zh-tw)公開資料集的子集，建立包含專利嵌入的 `patents` 資料表：

   ```
   CREATE TABLE vector_search.patents AS
   SELECT * FROM `patents-public-data.google_patents_research.publications`
   WHERE ARRAY_LENGTH(embedding_v1) > 0
    AND publication_number NOT IN ('KR-20180122872-A')
   LIMIT 1000000;
   ```
2. 建立包含專利嵌入內容的 `patents2` 資料表，以找出最接近的鄰近項目：

   ```
   CREATE TABLE vector_search.patents2 AS
   SELECT * FROM `patents-public-data.google_patents_research.publications`
   WHERE publication_number = 'KR-20180122872-A';
   ```

## 建立向量索引

1. 在`patents`資料表的 `embedding_v1` 欄上建立 `my_index` 向量索引：

   ```
   CREATE OR REPLACE VECTOR INDEX my_index ON vector_search.patents(embedding_v1)
   STORING(publication_number, title)
   OPTIONS(distance_type='COSINE', index_type='IVF');
   ```
2. 等待幾分鐘，讓系統建立向量索引，然後執行下列查詢，並確認 `coverage_percentage` 值為 `100`：

   ```
   SELECT * FROM vector_search.INFORMATION_SCHEMA.VECTOR_INDEXES;
   ```

## 使用含索引的 `VECTOR_SEARCH` 函式

建立並填入向量索引後，請使用 `VECTOR_SEARCH` 函式，在 `patents2` 資料表的 `embedding_v1` 欄中找出嵌入的最鄰近項目。這項查詢會使用搜尋中的向量索引，因此 `VECTOR_SEARCH` 會使用[近似最鄰近](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximation_methods)方法，找出嵌入項目的最鄰近項目。

**注意：** 向量索引適用於大型資料集。如要查看實際運作情形，請[重新建立 `vector_search.patents` 資料表](https://docs.cloud.google.com/bigquery/docs/vector-search?hl=zh-tw#create_test_tables)，但不要加入 `LIMIT 1000000` 子句，然後[重新建立向量索引](https://docs.cloud.google.com/bigquery/docs/vector-search?hl=zh-tw#create_a_vector_index)，最後執行下列查詢。

使用含索引的 `VECTOR_SEARCH` 函式：

```
SELECT query.publication_number AS query_publication_number,
  query.title AS query_title,
  base.publication_number AS base_publication_number,
  base.title AS base_title,
  distance
FROM
  VECTOR_SEARCH(
    TABLE vector_search.patents,
    'embedding_v1',
    TABLE vector_search.patents2,
    top_k => 5,
    distance_type => 'COSINE',
    options => '{"fraction_lists_to_search": 0.005}');
```

結果類似下方：

```
+--------------------------+-------------------------------------------------------------+-------------------------+--------------------------------------------------------------------------------------------------------------------------+---------------------+
| query_publication_number |                         query_title                         | base_publication_number |                                                        base_title                                                        |      distance       |
+--------------------------+-------------------------------------------------------------+-------------------------+--------------------------------------------------------------------------------------------------------------------------+---------------------+
| KR-20180122872-A         | Rainwater management system based on rainwater keeping unit | CN-106599080-B          | A kind of rapid generation for keeping away big vast transfer figure based on GIS                                        | 0.14471956347590609 |
| KR-20180122872-A         | Rainwater management system based on rainwater keeping unit | CN-114118544-A          | Urban waterlogging detection method and device                                                                           | 0.17472108931171348 |
| KR-20180122872-A         | Rainwater management system based on rainwater keeping unit | KR-20200048143-A        | Method and system for mornitoring dry stream using unmanned aerial vehicle                                               | 0.17561990745619782 |
| KR-20180122872-A         | Rainwater management system based on rainwater keeping unit | KR-101721695-B1         | Urban Climate Impact Assessment method of Reflecting Urban Planning Scenarios and Analysis System using the same         | 0.17696129365559843 |
| KR-20180122872-A         | Rainwater management system based on rainwater keeping unit | CN-109000731-B          | The experimental rig and method that research inlet for stom water chocking-up degree influences water discharged amount | 0.17902723269642917 |
+--------------------------+-------------------------------------------------------------+-------------------------+--------------------------------------------------------------------------------------------------------------------------+---------------------+
```

## 使用 `VECTOR_SEARCH` 函式進行暴力破解

使用 `VECTOR_SEARCH` 函式，找出 `patents2` 資料表中 `embedding_v1` 資料欄內嵌入項目的最鄰近項目。這項查詢不會在搜尋中使用向量索引，因此 `VECTOR_SEARCH` 會找出嵌入項目的精確最鄰近項目。

```
SELECT query.publication_number AS query_publication_number,
  query.title AS query_title,
  base.publication_number AS base_publication_number,
  base.title AS base_title,
  distance
FROM
  VECTOR_SEARCH(
    TABLE vector_search.patents,
    'embedding_v1',
    TABLE vector_search.patents2,
    top_k => 5,
    distance_type => 'COSINE',
    options => '{"use_brute_force":true}');
```

結果類似下方：

```
+--------------------------+-------------------------------------------------------------+-------------------------+--------------------------------------------------------------------------------------------------------------------------+---------------------+
| query_publication_number |                         query_title                         | base_publication_number |                                                        base_title                                                        |      distance       |
+--------------------------+-------------------------------------------------------------+-------------------------+--------------------------------------------------------------------------------------------------------------------------+---------------------+
| KR-20180122872-A         | Rainwater management system based on rainwater keeping unit | CN-106599080-B          | A kind of rapid generation for keeping away big vast transfer figure based on GIS                                        |  0.1447195634759062 |
| KR-20180122872-A         | Rainwater management system based on rainwater keeping unit | CN-114118544-A          | Urban waterlogging detection method and device                                                                           |  0.1747210893117136 |
| KR-20180122872-A         | Rainwater management system based on rainwater keeping unit | KR-20200048143-A        | Method and system for mornitoring dry stream using unmanned aerial vehicle                                               | 0.17561990745619782 |
| KR-20180122872-A         | Rainwater management system based on rainwater keeping unit | KR-101721695-B1         | Urban Climate Impact Assessment method of Reflecting Urban Planning Scenarios and Analysis System using the same         | 0.17696129365559843 |
| KR-20180122872-A         | Rainwater management system based on rainwater keeping unit | CN-109000731-B          | The experimental rig and method that research inlet for stom water chocking-up degree influences water discharged amount | 0.17902723269642928 |
+--------------------------+-------------------------------------------------------------+-------------------------+--------------------------------------------------------------------------------------------------------------------------+---------------------+
```

## 評估回想

使用索引執行向量搜尋時，系統會傳回近似結果，但會降低[召回率](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall?hl=zh-tw#recallsearch_term_rules)。您可以比較向量搜尋傳回的結果 (使用索引) 和向量搜尋傳回的結果 (使用暴力搜尋)，藉此計算召回率。在這個資料集中，`publication_number` 值可做為專利的不重複 ID，因此用於比較。

```
WITH approx_results AS (
  SELECT query.publication_number AS query_publication_number,
    base.publication_number AS base_publication_number
  FROM
    VECTOR_SEARCH(
      TABLE vector_search.patents,
      'embedding_v1',
      TABLE vector_search.patents2,
      top_k => 5,
      distance_type => 'COSINE',
      options => '{"fraction_lists_to_search": 0.005}')
),
  exact_results AS (
  SELECT query.publication_number AS query_publication_number,
    base.publication_number AS base_publication_number
  FROM
    VECTOR_SEARCH(
      TABLE vector_search.patents,
      'embedding_v1',
      TABLE vector_search.patents2,
      top_k => 5,
      distance_type => 'COSINE',
      options => '{"use_brute_force":true}')
)

SELECT
  a.query_publication_number,
  SUM(CASE WHEN a.base_publication_number = e.base_publication_number THEN 1 ELSE 0 END) / 5 AS recall
FROM exact_results e LEFT JOIN approx_results a
  ON e.query_publication_number = a.query_publication_number
GROUP BY a.query_publication_number
```

如果召回率低於預期，可以提高 `fraction_lists_to_search` 值，但缺點是延遲時間和資源用量可能會增加。如要調整向量搜尋，可以嘗試使用不同引數值多次執行 `VECTOR_SEARCH`，將結果儲存至表格，然後比較結果。

## 清除所用資源

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]