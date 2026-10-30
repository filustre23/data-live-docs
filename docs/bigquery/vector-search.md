Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用向量搜尋功能搜尋嵌入 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)和[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)，對儲存在 BigQuery 資料表中的嵌入執行[相似度搜尋](https://wikipedia.org/wiki/Similarity_search)。

向量搜尋是一種技術，可使用嵌入項目比較相似的物件，並為 Google 搜尋、YouTube 和 Google Play 等 Google 產品提供支援。您可以運用向量搜尋大規模執行語意搜尋，也可以執行**混合搜尋**，結合語意搜尋和詞彙 (關鍵字) 搜尋。使用向量搜尋功能時，您可以搭配[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)，運用反向檔案索引 (IVF) 和 [ScaNN 演算法](https://research.google/blog/announcing-scann-efficient-vector-similarity-search/?hl=zh-tw)等基礎技術。

向量搜尋是以嵌入為基礎建構而成。嵌入是高維度數值向量，代表特定實體，例如一段文字或音訊檔案。機器學習 (ML) 模型會使用嵌入技術，將這類實體的語意編碼，方便推理及比較。舉例來說，在叢集、分類和建議模型中，常見的作業是測量[嵌入空間](https://en.wikipedia.org/wiki/Latent_space)中向量之間的距離，找出語意上最相似的項目。

## 目標

* 使用 `VECTOR_SEARCH` 函式，對儲存在 BigQuery 資料表中的嵌入執行相似度搜尋。
* 使用向量索引提升向量搜尋效能。
* 執行使用向量索引的搜尋，以及不使用索引的搜尋。
* 比較使用索引的搜尋結果和未使用索引的搜尋結果，評估召回率。

## 費用

`VECTOR_SEARCH` 函式會採用 [BigQuery 運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)。系統會根據以量計價或版本定價，向您收取相似度搜尋費用。

* 以量計價：系統會根據基本資料表、索引和搜尋查詢中掃描的位元組數向您收費。
* 方案價格：系統會根據預留方案中完成工作所需的運算單元數量向您收費。如果相似度計算的資料量較大或較複雜，費用就會較高。

  **注意：** [標準版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)不支援使用索引。

詳情請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您在專案中獲派角色，即可選取該專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 如果尚未啟用 BigQuery API，請啟用。

   **啟用 API 時所需的角色**

   如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「服務使用情形管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com&hl=zh-tw)

### 必要的角色

如要取得完成本教學課程所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* 建立資料集、資料表和向量索引：
  [BigQuery 資料編輯器](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
* 執行 BigQuery 工作：
  [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立資料集

如要建立 BigQuery 資料集，請選取下列任一選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」中展開專案，然後按一下「Datasets」。
4. 在「資料集」頁面，按一下 add「建立資料集」。
5. 在「建立資料集」窗格中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 選取「資料位置」的「美國」。

   其餘預設設定均保留原樣。
6. 點選「建立資料集」。

### bq

如要建立新的資料集，請使用 [`bq mk --dataset` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)。

1. 建立名為 `bqml_tutorial` 的資料集，並將資料位置設為 `US`：

   ```
   bq mk --dataset \
     --location=US \
     --description "BigQuery ML tutorial dataset." \
     bqml_tutorial
   ```
2. 確認資料集已建立完成：

   ```
   bq ls
   ```

### API

使用已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法：

```
{
  "datasetReference": {
     "datasetId": "bqml_tutorial"
  }
}
```

## 建立資料表來儲存資料和嵌入

在本節中，您將建立包含專利嵌入內容的 `patents` 資料表。這些嵌入內容是以 [Google 專利](https://console.cloud.google.com/marketplace/product/google_patents_public_datasets/google-patents-public-data?hl=zh-tw)公開資料集的部分資料為基礎，您也會建立 `patents2` 資料表，其中包含專利嵌入，可找出最相近鄰點。

如要建立資料表，請按照下列步驟操作：

1. 如要建立 `patents` 資料表，請在查詢編輯器中貼上下列內容，然後點選 play\_circle「執行」：

   ```
   CREATE TABLE bqml_tutorial.patents AS
   SELECT * FROM `patents-public-data.google_patents_research.publications`
   WHERE ARRAY_LENGTH(embedding_v1) > 0
    AND publication_number NOT IN ('KR-20180122872-A')
   LIMIT 1000000;
   ```

   你會收到類似以下的確認訊息：`This statement
   created a new table named patents.`
2. 如要建立包含專利嵌入的 `patents2` 資料表，以找出最接近的鄰居，請將下列內容貼到查詢編輯器，然後按一下 play\_circle「執行」：

   ```
   CREATE TABLE bqml_tutorial.patents2 AS
   SELECT * FROM `patents-public-data.google_patents_research.publications`
   WHERE publication_number = 'KR-20180122872-A';
   ```

   你會收到類似以下的確認訊息：`This statement
   created a new table named patents2.`

## 建立向量索引

搭配向量索引使用 `VECTOR_SEARCH` 時，`VECTOR_SEARCH` 會採用「近似最鄰近」方法提升向量搜尋效能，但會降低[召回率](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall?hl=zh-tw#recallsearch_term_rules)，因此傳回的結果會更近似。如果沒有向量索引，`VECTOR_SEARCH` 會使用[暴力搜尋](https://en.wikipedia.org/wiki/Brute-force_search)來測量每筆記錄的距離。

在本節中，您將在 `patents` 資料表的 `embedding_v1` 資料欄上建立 `my_index` 向量索引。接著，您會驗證索引是否可用。

如要建立向量索引，請按照下列步驟操作：

1. 如要在 `patents` 資料表的 `embedding_v1` 欄上建立 `my_index` 向量索引，請在查詢編輯器中貼上下列內容，然後點選 play\_circle「執行」：

   ```
   CREATE OR REPLACE VECTOR INDEX my_index ON bqml_tutorial.patents(embedding_v1)
   STORING(publication_number, title)
   OPTIONS(distance_type='COSINE', index_type='IVF');
   ```

   你會收到類似以下的確認訊息：`The vector index
   creation on table bqml_tutorial.patents was initiated. Please query
   bqml_tutorial.INFORMATION_SCHEMA.VECTOR_INDEXES to check the progress
   of the index.`
2. 如要確認向量索引是否已準備就緒，請將下列內容貼到查詢編輯器中，然後按一下「執行」play\_circle：

   ```
   SELECT * FROM bqml_tutorial.INFORMATION_SCHEMA.VECTOR_INDEXES;
   ```

   在查詢結果中，確認 `index_status` 為 `ACTIVE`，且 `coverage_percentage` 值為 `100`。「`coverage_percentage`」可能要過幾分鐘才會抵達「`100`」。

## 使用含索引的 `VECTOR_SEARCH` 函式

建立並填入向量索引後，請使用 `VECTOR_SEARCH` 函式，在 `patents2` 資料表的 `embedding_v1` 欄中找出嵌入的最鄰近項目。這項查詢會使用搜尋中的向量索引，因此 `VECTOR_SEARCH` 會使用[近似最鄰近](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximation_methods)方法，找出嵌入項目的最鄰近項目。

**注意：** 向量索引適用於大型資料集，如要查看實際運作情形，請[重新建立 `vector_search.patents` 資料表](#create_test_tables_to_store_data_and_embeddings)，但不要加入 `LIMIT 1000000` 子句，然後[重新建立向量索引](#create_a_vector_index)，並執行下列查詢。

如要搭配索引使用 `VECTOR_SEARCH` 函式，請將下列內容貼到查詢編輯器中，然後按一下 play\_circle「執行」：

```
SELECT query.publication_number AS query_publication_number,
  query.title AS query_title,
  base.publication_number AS base_publication_number,
  base.title AS base_title,
  distance
FROM
  VECTOR_SEARCH(
    TABLE bqml_tutorial.patents,
    'embedding_v1',
    TABLE bqml_tutorial.patents2,
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

在本節中，您會使用 `VECTOR_SEARCH` 函式，在 `patents2` 資料表的 `embedding_v1` 欄中，找出最鄰近的嵌入。這項查詢不會在搜尋中使用向量索引，因此 `VECTOR_SEARCH` 會找出嵌入項目的確切最近鄰。

如要使用 `VECTOR_SEARCH` 強制執行，請在查詢編輯器中貼上下列內容，然後按一下 play\_circle「執行」：

```
SELECT query.publication_number AS query_publication_number,
  query.title AS query_title,
  base.publication_number AS base_publication_number,
  base.title AS base_title,
  distance
FROM
  VECTOR_SEARCH(
    TABLE bqml_tutorial.patents,
    'embedding_v1',
    TABLE bqml_tutorial.patents2,
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

使用索引執行向量搜尋時，系統會傳回近似結果，但會降低[召回率](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall?hl=zh-tw#recallsearch_term_rules)。您可以比較向量搜尋 (含索引) 傳回的結果，以及向量搜尋 (含暴力破解) 傳回的結果，藉此計算召回率。`publication_number` 值是專利的專屬 ID，因此可用於下列查詢中的比較。

如要評估召回率，請在查詢編輯器中貼上下列內容，然後點選「執行」play\_circle：

```
WITH approx_results AS (
  SELECT query.publication_number AS query_publication_number,
    base.publication_number AS base_publication_number
  FROM
    VECTOR_SEARCH(
      TABLE bqml_tutorial.patents,
      'embedding_v1',
      TABLE bqml_tutorial.patents2,
      top_k => 5,
      distance_type => 'COSINE',
      options => '{"fraction_lists_to_search": 0.005}')
),
  exact_results AS (
  SELECT query.publication_number AS query_publication_number,
    base.publication_number AS base_publication_number
  FROM
    VECTOR_SEARCH(
      TABLE bqml_tutorial.patents,
      'embedding_v1',
      TABLE bqml_tutorial.patents2,
      top_k => 5,
      distance_type => 'COSINE',
      options => '{"use_brute_force":true}')
)

SELECT
  a.query_publication_number,
  SUM(CASE WHEN a.base_publication_number = e.base_publication_number THEN 1 ELSE 0 END) / 5 AS recall
FROM exact_results e LEFT JOIN approx_results a
  ON e.query_publication_number = a.query_publication_number
GROUP BY a.query_publication_number;
```

結果如下所示：

```
+--------------------------+--------+
| query_publication_number | recall |
+--------------------------+--------+
| KR-20180122872-A         |    1.0 |
+--------------------------+--------+
```

如果召回率低於預期，可以提高 `fraction_lists_to_search` 值，但延遲時間和資源用量可能會增加。如要調整向量搜尋，您可以嘗試多次執行 `VECTOR_SEARCH`，使用不同的引數值，將結果儲存至表格，然後比較結果。

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

如要保留專案，但刪除本教學課程中使用的資源，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中展開專案，然後按一下「資料集」。
3. 針對 `bqml_tutorial` 資料集，依序點按 more\_vert
   **「Open actions」(開啟動作) >「Delete」(刪除)**。
4. 在「Delete dataset」(刪除資料集) 對話方塊中，按一下「Delete」(刪除) 進行確認。

## 後續步驟




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]