Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理分區和叢集建議

本文說明分割區和叢集建議工具的運作方式、如何查看建議和洞察資料，以及如何套用分割區和叢集建議。

## 推薦工具的運作方式

BigQuery 分區和分群建議工具會產生[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)或[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)建議，協助您最佳化 BigQuery 資料表。建議工具會分析 BigQuery 資料表的工作流程，並提供建議，協助您使用資料表分區或資料表叢集，進一步改善工作流程並降低查詢費用。

如要進一步瞭解建議工具服務，請參閱「[建議工具總覽](https://docs.cloud.google.com/recommender/docs/overview?hl=zh-tw)」。

分區和叢集處理建議工具會使用貴機構過去最多 30 天的工作負載執行資料，分析每個 BigQuery 資料表，找出次佳的分區和叢集處理設定。此外，這項建議工具還會運用機器學習技術，預測不同分區或叢集設定可將工作負載執行作業最佳化多少。如果建議工具發現資料表分區或分群可大幅節省費用，就會產生建議。分區與分群建議工具會產生下列類型的建議：

| 現有資料表類型 | 建議子類型 | 建議範例 |
| --- | --- | --- |
| 未分區、未叢集 | 分區 | 「根據 column\_C 按照 DAY 分區，每個月約可省下 64 個運算單元時數」 |
| 未分區、未叢集 | 叢集 | 「根據 column\_C 分群，每月約可省下 64 個運算單元小時」 |
| 已分區，未叢集 | 叢集 | 「根據 column\_C 分群，每月約可省下 64 個運算單元小時」 |

每項建議都包含三個部分：

* 分區或叢集特定資料表的指引
* 要分區或叢集化的資料表中的特定資料欄
* 套用建議後預估每月可省下的費用

為計算潛在工作負載節省量，建議工具會假設過去 30 天的歷來執行工作負載資料代表未來的工作負載。

**注意：** 在某些情況下，預估節省金額可能會過高。詳情請參閱「[高估節省金額](#overestimation)」一文。

建議事項 API 也會以*洞察*的形式傳回資料表工作負載資訊。
[深入分析](https://docs.cloud.google.com/recommender/docs/insights/using-insights?hl=zh-tw)是可協助您瞭解專案工作負載的發現項目，可提供更多背景資訊，說明分區或叢集建議如何改善工作負載成本。

## 限制

* 分區和叢集建議工具不支援使用舊版 SQL 的 BigQuery 資料表。產生建議時，建議工具會在分析中排除任何舊版 SQL 查詢。此外，如果對使用舊版 SQL 的 BigQuery 資料表套用分區建議，該資料表中的所有舊版 SQL 工作流程都會中斷。

  套用分割區建議前，請先[將舊版 SQL 工作流程遷移至 GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-tw)。
* BigQuery 不支援就地變更資料表的分區架構。您只能在資料表副本上變更資料表的分區。詳情請參閱「[套用分區建議](#apply_partition_recommendations)」。
* 分區和分群建議工具每天都會執行，不過，如果執行時間超過 24 小時，系統就會略過隔天的執行作業。

## 位置

分區與分群建議工具適用於下列處理位置：

|  | **地區說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- | --- |
| **亞太地區** | | | |
|  | 德里 | `asia-south2` |  |
|  | 香港 | `asia-east2` |  |
|  | 雅加達 | `asia-southeast2` |  |
|  | 孟買 | `asia-south1` |  |
|  | 大阪 | `asia-northeast2` |  |
|  | 首爾 | `asia-northeast3` |  |
|  | 新加坡 | `asia-southeast1` |  |
|  | 雪梨 | `australia-southeast1` |  |
|  | 台灣 | `asia-east1` |  |
|  | 東京 | `asia-northeast1` |  |
| **歐洲** | | | |
|  | 比利時 | `europe-west1` |  |
|  | 柏林 | `europe-west10` |  |
|  | 歐洲 (多區域) | `eu` |
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` |  |
|  | 荷蘭 | `europe-west4` |  |
|  | 蘇黎世 | `europe-west6` |  |
| **美洲** | | | |
|  | 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 拉斯維加斯 | `us-west4` |  |
|  | 洛杉磯 | `us-west2` |  |
|  | 蒙特婁 | `northamerica-northeast1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 北維吉尼亞州 | `us-east4` |  |
|  | 奧勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 鹽湖城 | `us-west3` |  |
|  | 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 多倫多 | `northamerica-northeast2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 美國 (多區域) | `us` |

## 事前準備

* [啟用 Recommender API](https://docs.cloud.google.com/recommender/docs/enable-api?hl=zh-tw)。

### 所需權限

如要取得存取分區和叢集建議所需的權限，請要求管理員授予您「[BigQuery 分區分群建議工具檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/recommender?hl=zh-tw#recommender.bigqueryPartitionClusterViewer) 」(`roles/recommender.bigqueryPartitionClusterViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備存取分區和叢集建議所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要存取分區和叢集建議，您必須具備下列權限：

* `recommender.bigqueryPartitionClusterRecommendations.get`
* `recommender.bigqueryPartitionClusterRecommendations.list`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 查看建議

本節說明如何使用 Google Cloud 控制台、Google Cloud CLI 或 Recommender API，查看分區和叢集建議與深入分析。

**附註：** 您也可以使用 BigQuery 資料移轉服務，將建議匯出至 BigQuery。詳情請參閱「[將建議匯出至 BigQuery](https://docs.cloud.google.com/recommender/docs/bq-export/export-recommendations-to-bq?hl=zh-tw)」一文。

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「最佳化建議」。

   「最佳化建議」分頁會列出專案可用的所有最佳化建議。
3. 在「最佳化 BigQuery 工作負載成本」面板中，按一下「查看全部」。

   費用建議表格會列出為目前專案產生的所有建議。舉例來說，下列螢幕截圖顯示建議工具分析 `example_table` 資料表後，建議分群 `example_column` 欄，以節省大約位元組和運算單元的數量。
4. 如要進一步瞭解表格洞察資料和建議，請按一下建議。

### gcloud

如要查看特定專案的分區或叢集建議，請使用 [`gcloud recommender recommendations list` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/recommender/recommendations/list?hl=zh-tw)：

```
gcloud recommender recommendations list \
    --project=PROJECT_NAME \
    --location=REGION_NAME \
    --recommender=google.bigquery.table.PartitionClusterRecommender \
    --format=FORMAT_TYPE \
```

更改下列內容：

* `PROJECT_NAME`：包含 BigQuery 資料表的專案名稱
* `REGION_NAME`：專案所在的區域
* `FORMAT_TYPE`：支援的 [gcloud CLI 輸出格式](https://docs.cloud.google.com/sdk/gcloud/reference?hl=zh-tw#--format)，例如 JSON

下表說明推薦工具 API 回應中的重要欄位：

| 屬性 | 適用於子類型 | 說明 |
| --- | --- | --- |
| `recommenderSubtype` | 分區或叢集 | 指出建議類型。 |
| `content.overview.partitionColumn` | 分區 | 建議的分區資料欄名稱。 |
| `content.overview.partitionTimeUnit` | 分區 | 建議的分區時間單位。舉例來說，`DAY` 表示建議在建議的資料欄中建立每日分區。 |
| `content.overview.clusterColumns` | 叢集 | 建議的叢集資料欄名稱。 |

* 如要進一步瞭解建議工具回應中的其他欄位，請參閱「[REST 資源：`projects.locations.recommendersrecommendation`](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/projects.locations.recommenders.recommendations?hl=zh-tw#resource:-recommendation)」。
* 如要進一步瞭解如何使用 Recommender API，請參閱「[使用 API - 建議](https://docs.cloud.google.com/recommender/docs/using-api?hl=zh-tw)」。

如要使用 gcloud CLI 查看表格洞察，請使用 [`gcloud recommender insights list` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/recommender/insights/list?hl=zh-tw)：

```
gcloud recommender insights list \
    --project=PROJECT_NAME \
    --location=REGION_NAME \
    --insight-type=google.bigquery.table.StatsInsight \
    --format=FORMAT_TYPE \
```

更改下列內容：

* `PROJECT_NAME`：包含 BigQuery 資料表的專案名稱
* `REGION_NAME`：專案所在的區域
* `FORMAT_TYPE`：支援的 [gcloud CLI 輸出格式](https://docs.cloud.google.com/sdk/gcloud/reference?hl=zh-tw#--format)，例如 JSON

下表說明洞察 API 回應中的重要欄位：

| 屬性 | 適用於子類型 | 說明 |
| --- | --- | --- |
| `content.existingPartitionColumn` | 叢集 | 現有的分區資料欄 (如有) |
| `content.tableSizeTb` | 全部 | 資料表大小 (以 TB 為單位) |
| `content.bytesReadMonthly` | 全部 | 每月從資料表讀取的位元組數 |
| `content.slotMsConsumedMonthly` | 全部 | 在資料表上執行的工作負載每月耗用的運算單元時間 (毫秒) |
| `content.queryJobsCountMonthly` | 全部 | 每月在資料表上執行的工作數 |

* 如要進一步瞭解洞察回應中的其他欄位，請參閱 [REST 資源：`projects.locations.insightTypes.insights`](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/projects.locations.insightTypes.insights?hl=zh-tw#resource:-insight)。
* 如要進一步瞭解如何使用洞察資料，請參閱「[使用 API - 洞察](https://docs.cloud.google.com/recommender/docs/insights/using-api?hl=zh-tw)」。

### REST API

如要查看特定專案的分區或叢集建議，請使用 REST API。您必須為每個指令提供驗證權杖，這類權杖可使用 gcloud CLI 取得。如要進一步瞭解如何取得驗證權杖，請參閱「[取得 ID 權杖的方法](https://docs.cloud.google.com/docs/authentication/get-id-token?hl=zh-tw)」。

您可以透過 `curl list` 要求，查看特定專案的所有最佳化建議：

```
curl
    -H "Authorization: Bearer $GCLOUD_AUTH_TOKEN"
    -H "x-goog-user-project: PROJECT_NAME" https://recommender.googleapis.com/v1/projects/my-project/locations/us/recommenders/google.bigquery.table.PartitionClusterRecommender/recommendations
```

更改下列內容：

* `GCLOUD_AUTH_TOKEN`：有效的 gcloud CLI 存取權杖名稱
* `PROJECT_NAME`：包含 BigQuery 資料表的專案名稱

下表說明推薦工具 API 回應中的重要欄位：

| 屬性 | 適用於子類型 | 說明 |
| --- | --- | --- |
| `recommenderSubtype` | 分區或叢集 | 指出建議類型。 |
| `content.overview.partitionColumn` | 分區 | 建議的分區資料欄名稱。 |
| `content.overview.partitionTimeUnit` | 分區 | 建議的分區時間單位。舉例來說，`DAY` 表示建議在建議的資料欄中建立每日分區。 |
| `content.overview.clusterColumns` | 叢集 | 建議的叢集資料欄名稱。 |

* 如要進一步瞭解建議工具回應中的其他欄位，請參閱「[REST 資源：`projects.locations.recommendersrecommendation`](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/projects.locations.recommenders.recommendations?hl=zh-tw#resource:-recommendation)」。
* 如要進一步瞭解如何使用 Recommender API，請參閱「[使用 API - 建議](https://docs.cloud.google.com/recommender/docs/using-api?hl=zh-tw)」。

如要使用 REST API 查看資料表洞察，請執行下列指令：

```
curl
-H "Authorization: Bearer $GCLOUD_AUTH_TOKEN"
-H "x-goog-user-project: PROJECT_NAME" https://recommender.googleapis.com/v1/projects/my-project/locations/us/insightTypes/google.bigquery.table.StatsInsight/insights
```

更改下列內容：

* `GCLOUD_AUTH_TOKEN`：有效的 gcloud CLI 存取權杖名稱
* `PROJECT_NAME`：包含 BigQuery 資料表的專案名稱

下表說明洞察 API 回應中的重要欄位：

| 屬性 | 適用於子類型 | 說明 |
| --- | --- | --- |
| `content.existingPartitionColumn` | 叢集 | 現有的分區資料欄 (如有) |
| `content.tableSizeTb` | 全部 | 資料表大小 (以 TB 為單位) |
| `content.bytesReadMonthly` | 全部 | 每月從資料表讀取的位元組數 |
| `content.slotMsConsumedMonthly` | 全部 | 在資料表上執行的工作負載每月耗用的運算單元時間 (毫秒) |
| `content.queryJobsCountMonthly` | 全部 | 每月在資料表上執行的工作數 |

* 如要進一步瞭解洞察回應中的其他欄位，請參閱 [REST 資源：`projects.locations.insightTypes.insights`](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/projects.locations.insightTypes.insights?hl=zh-tw#resource:-insight)。
* 如要進一步瞭解如何使用洞察資料，請參閱「[使用 API - 洞察](https://docs.cloud.google.com/recommender/docs/insights/using-api?hl=zh-tw)」。

### 查看 `INFORMATION_SCHEMA` 建議

您也可以使用`INFORMATION_SCHEMA`檢視畫面查看建議和洞察資料。舉例來說，您可以透過 `INFORMATION_SCHEMA.RECOMMENDATIONS` 檢視畫面，根據節省的時段數查看前三項最佳化建議，如下列範例所示：

```
SELECT
   recommender,
   target_resources,
   LAX_INT64(additional_details.overview.bytesSavedMonthly) / POW(1024, 3) as est_gb_saved_monthly,
   LAX_INT64(additional_details.overview.slotMsSavedMonthly) / (1000 * 3600) as slot_hours_saved_monthly,
  last_updated_time
FROM
  `region-us`.INFORMATION_SCHEMA.RECOMMENDATIONS
WHERE
   primary_impact.category = 'COST'
AND
   state = 'ACTIVE'
ORDER by
   slot_hours_saved_monthly DESC
LIMIT 3;
```

**附註：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+---------------------------------------------------+--------------------------------------------------------------------------------------------------+
|                    recommender                    |   target_resources      | est_gb_saved_monthly | slot_hours_saved_monthly |  last_updated_time
+---------------------------------------------------+--------------------------------------------------------------------------------------------------+
| google.bigquery.materializedview.Recommender      | ["project_resource"]    | 140805.38289248943   |        9613.139166666666 |  2024-07-01 13:00:00
| google.bigquery.table.PartitionClusterRecommender | ["table_resource_1"]    | 4393.7416711859405   |        56.61476777777777 |  2024-07-01 13:00:00
| google.bigquery.table.PartitionClusterRecommender | ["table_resource_2"]    |   3934.07264107652   |       10.499466666666667 |  2024-07-01 13:00:00
+---------------------------------------------------+--------------------------------------------------------------------------------------------------+
```

詳情請參閱下列資源：

* [`INFORMATION_SCHEMA.RECOMMENDATIONS` 查看](https://docs.cloud.google.com/bigquery/docs/information-schema-recommendations?hl=zh-tw)
* [`INFORMATION_SCHEMA.RECOMMENDATIONS_BY_ORGANIZATION` 查看](https://docs.cloud.google.com/bigquery/docs/information-schema-recommendations-by-org?hl=zh-tw)
* [`INFORMATION_SCHEMA.INSIGHTS` 查看](https://docs.cloud.google.com/bigquery/docs/information-schema-insights?hl=zh-tw)

## 套用叢集建議

如要套用叢集建議，請執行下列任一操作：

* [直接將叢集套用至原始資料表](#apply_clusters_directly_to_the_original_table)
* [將叢集套用至複製的表格](#apply_clusters_to_a_copied_table)
* [在具體化檢視表中套用叢集](#apply_clusters_in_a_materialized_view)

### 直接將叢集套用至原始表格

您可以將叢集建議直接套用至現有的 BigQuery 資料表。這個方法比[將建議套用至複製的資料表](#apply_clusters_to_a_copied_table)更快，但不會保留備份資料表。

請按照下列步驟，將新的叢集規格套用至未分區或分區資料表。

1. 在 bq 工具中，更新資料表的叢集規格，以符合新的叢集：

   ```
    bq update --clustering_fields=CLUSTER_COLUMN DATASET.ORIGINAL_TABLE
   ```

   更改下列內容：

   * `CLUSTER_COLUMN`：您要叢集化的資料欄，例如 `mycolumn`
   * `DATASET`：包含資料表的資料集名稱，例如 `mydataset`
   * `ORIGINAL_TABLE`：原始資料表的名稱，例如 `mytable`

   您也可以呼叫 `tables.update` 或 `tables.patch` API 方法來[修改叢集規格](https://docs.cloud.google.com/bigquery/docs/manage-clustered-tables?hl=zh-tw#modifying-cluster-spec)。
2. 如要根據新的叢集規格將所有資料列叢集化，請執行下列 `UPDATE` 陳述式：

   ```
   UPDATE DATASET.ORIGINAL_TABLE SET CLUSTER_COLUMN=CLUSTER_COLUMN WHERE true
   ```

   **注意：** 如果將新的叢集規格套用至長期儲存空間中的資料表，該資料表就會恢復為有效儲存空間價格。詳情請參閱[儲存空間價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。

### 將叢集套用至複製的資料表

將叢集建議套用至 BigQuery 資料表時，您可以先複製原始資料表，然後將建議套用至複製的資料表。這個方法可確保您在需要復原叢集設定變更時，原始資料不會遺失。

您可以使用這個方法，將叢集建議套用至未分區和已分區的資料表。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，使用 `LIKE` 運算子建立空白資料表，並沿用原始資料表的相同中繼資料 (包括分群規格)：

   ```
   CREATE TABLE DATASET.COPIED_TABLE
   LIKE DATASET.ORIGINAL_TABLE
   ```

   更改下列內容：

   * `DATASET`：包含資料表的資料集名稱，例如 `mydataset`
   * `COPIED_TABLE`：複製的資料表名稱，例如 `copy_mytable`
   * `ORIGINAL_TABLE`：原始資料表的名稱，例如 `mytable`
3. 在 Google Cloud 控制台中開啟 Cloud Shell 編輯器。

   [啟用 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)
4. 在 Cloud Shell 編輯器中，使用 `bq update` 指令更新所複製資料表的叢集規格，以符合建議的叢集：

   ```
    bq update --clustering_fields=CLUSTER_COLUMN DATASET.COPIED_TABLE
   ```

   將 `CLUSTER_COLUMN` 替換為要用於叢集化的資料欄，例如 `mycolumn`。

   您也可以呼叫 `tables.update` 或 `tables.patch` API 方法來[修改叢集規格](https://docs.cloud.google.com/bigquery/docs/manage-clustered-tables?hl=zh-tw#modifying-cluster-spec)。
5. 在查詢編輯器中，擷取資料表結構定義，其中包含原始資料表的分區和分群設定 (如有)。如要擷取結構定義，請查看原始資料表的 `INFORMATION_SCHEMA.TABLES` 檢視畫面：

   ```
   SELECT
     ddl
   FROM
     DATASET.INFORMATION_SCHEMA.TABLES
   WHERE
     table_name = 'ORIGINAL_TABLE'
   ```

   輸出內容是 ORIGINAL\_TABLE 的完整資料定義語言 (DDL) 陳述式，包括 `PARTITION BY` 子句。如要進一步瞭解 DDL 輸出內容中的引數，請參閱 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)。

   DDL 輸出內容會指出原始資料表中的分區類型：

   | 分區類型 | 輸出範例 |
   | --- | --- |
   | 未分割 | 缺少 `PARTITION BY` 子句。 |
   | 依資料表資料欄分區 | `PARTITION BY c0` |
   | `PARTITION BY DATE(c0)` |
   | `PARTITION BY DATETIME_TRUNC(c0, MONTH)` |
   | 依擷取時間分區 | `PARTITION BY _PARTITIONDATE` |
   | `PARTITION BY DATETIME_TRUNC(_PARTITIONTIME, MONTH)` |
6. 將資料擷取至複製的資料表。使用的程序取決於分區類型。

   * 如果原始資料表未分區，或依資料表欄分區，請將原始資料表的資料擷取到複製的資料表：

     ```
     INSERT INTO DATASET.COPIED_TABLE
     SELECT * FROM DATASET.ORIGINAL_TABLE
     ```
   * 如果原始資料表是依擷取時間分區，請按照下列步驟操作：

     1. 使用 `INFORMATION_SCHEMA.COLUMNS` 檢視畫面擷取資料欄清單，以形成資料擷取運算式：

        ```
        SELECT
        ARRAY_TO_STRING((
        SELECT
          ARRAY(
          SELECT
            column_name
          FROM
            DATASET.INFORMATION_SCHEMA.COLUMNS
          WHERE
            table_name = 'ORIGINAL_TABLE')), ", ")
        ```

        輸出內容是以半形逗號分隔的資料欄名稱清單。
     2. 將原始資料表的資料匯入複製的資料表：

        ```
        INSERT DATASET.COPIED_TABLE (COLUMN_NAMES, _PARTITIONTIME)
        SELECT *, _PARTITIONTIME FROM DATASET.ORIGINAL_TABLE
        ```

        將 `COLUMN_NAMES` 替換為上一個步驟的輸出內容 (以逗號分隔的資料欄清單)，例如 `col1, col2, col3`。

   您現在已擁有分群複製資料表，內含與原始資料表相同的資料。
   在後續步驟中，您會以新建立的分群資料表取代原始資料表。
7. 將原始資料表重新命名為備份資料表：

   ```
   ALTER TABLE DATASET.ORIGINAL_TABLE
   RENAME TO BACKUP_TABLE
   ```

   將 `BACKUP_TABLE` 替換為備份資料表的名稱，例如 `backup_mytable`。
8. 將複製的資料表重新命名為原始資料表：

   ```
   ALTER TABLE DATASET.COPIED_TABLE
   RENAME TO ORIGINAL_TABLE
   ```

   原始資料表現在會根據叢集建議進行叢集處理。

建議您檢查叢集資料表，確保所有資料表函式都能正常運作。許多資料表函式可能與資料表 ID 相關聯，而非資料表名稱，因此建議先查看下列資料表函式，再繼續操作：

* 存取權和權限，例如 [IAM 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)、[資料列層級存取權](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)或[資料欄層級存取權](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)。
* 資料表構件，例如[資料表本機副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)、[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)或[搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)。
* 任何進行中的資料表程序狀態，例如任何[具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)，或您複製資料表時執行的任何工作。
* 可使用[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)功能存取歷來資料表資料。
* 與原始資料表相關聯的任何中繼資料，例如 `table_option_list` 或 `column_option_list`。詳情請參閱「[資料定義語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)」。

如有任何問題，您必須手動將受影響的構件遷移至新表格。

查看叢集資料表後，您可以選擇使用下列指令刪除備份資料表：

```
    DROP TABLE DATASET.BACKUP_TABLE
```

### 在具體化檢視表中套用叢集

您可以建立資料表的具體化檢視，儲存套用建議後原始資料表的資料。使用具體化檢視套用最佳化建議，可確保叢集資料透過[自動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)保持最新狀態。
查詢、維護及儲存具體化檢視區塊時，請留意[價格注意事項](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#materialized_views_pricing)。如要瞭解如何建立叢集化具體化檢視表，請參閱「[叢集化具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#cluster_materialized_views)」。

## 套用分區建議

如要套用分區建議，請務必將建議套用至原始表格的副本。BigQuery 不支援就地變更資料表的分區架構，例如將未分區的資料表變更為分區資料表、變更資料表的分區架構，或是建立與基礎資料表分區架構不同的具體化檢視。您只能在資料表副本上變更資料表的分區。

**注意：** 請先將舊版 SQL 工作流程遷移至 GoogleSQL，再套用分割區建議。詳情請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/manage-partition-cluster-recommendations?hl=zh-tw#limitations)」一節。

### 將分區建議套用至複製的資料表

將分區建議套用至 BigQuery 資料表時，您必須先複製原始資料表，然後將建議套用至複製的資料表。這樣一來，如果需要復原分割區，就能保留原始資料。

下列程序會使用範例建議，依分區時間單位 `DAY` 將資料表分區。

1. 使用分區建議建立複製的資料表：

   ```
   CREATE TABLE DATASET.COPIED_TABLE
   PARTITION BY DATE_TRUNC(PARTITION_COLUMN, DAY)
   AS SELECT * FROM DATASET.ORIGINAL_TABLE
   ```

   更改下列內容：

   * `DATASET`：包含資料表的資料集名稱，例如 `mydataset`
   * `COPIED_TABLE`：複製的資料表名稱，例如 `copy_mytable`
   * `PARTITION_COLUMN`：您要分區的資料欄，例如 `mycolumn`

   如要進一步瞭解如何建立分區資料表，請參閱[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)。
2. 將原始資料表重新命名為備份資料表：

   ```
   ALTER TABLE DATASET.ORIGINAL_TABLE
   RENAME TO BACKUP_TABLE
   ```

   將 `BACKUP_TABLE` 替換為備份資料表的名稱，例如 `backup_mytable`。
3. 將複製的資料表重新命名為原始資料表：

   ```
   ALTER TABLE DATASET.COPIED_TABLE
   RENAME TO ORIGINAL_TABLE
   ```

   原始資料表現在會根據分區建議分區。

建議您檢查分區資料表，確保所有資料表函式都能正常運作。許多資料表函式可能與資料表 ID 相關聯，而非資料表名稱，因此建議先查看下列資料表函式，再繼續操作：

* 存取權和權限，例如 [IAM 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)、[資料列層級存取權](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)或[資料欄層級存取權](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)。
* 資料表構件，例如[資料表本機副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)、[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)或[搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)。
* 任何進行中的資料表程序狀態，例如任何[具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)，或您複製資料表時執行的任何工作。
* 可使用[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)功能存取歷來資料表資料。
* 與原始資料表相關聯的任何中繼資料，例如 `table_option_list` 或 `column_option_list`。詳情請參閱「[資料定義語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)」。
* 可使用舊版 SQL 將查詢結果寫入分區資料表。[分區資料表不完全支援舊版 SQL](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#limitations)。其中一個解決方法是[將舊版 SQL 工作流程遷移至 GoogleSQL](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#limitations)，再套用分割區建議。

如有任何問題，您必須手動將受影響的構件遷移至新表格。

查看分區資料表後，您可以選擇使用下列指令刪除備份資料表：

```
    DROP TABLE DATASET.BACKUP_TABLE
```

## 高估節省金額

在某些情況下，BigQuery 叢集建議工具可能會提供預估節省金額，但該金額可能過於龐大，例如超過特定資料表的每月帳單位元組總數。這通常是由稱為「子查詢加總」的模式所造成。

### 導致高估的原因

如果工作負載涉及複雜的 GoogleSQL 查詢，且多次參照相同資料表，就最容易發生高估情況。相關示例包括：

* 查詢在單一大型資料表上進行多次自我聯結。
* 查詢含有多個通用資料表運算式或子查詢，但這些運算式或子查詢掃描的基礎資料表相同。

### 為什麼會發生高估情形

BigQuery 執行計畫通常會將複雜查詢分成多個不同的「階段」。分群建議工具會分別計算每個階段的潛在節省金額，並加總這些金額。

如果單一工作包含多個階段，且每個階段都從同一資料表讀取資料，建議工具可能會計算該單一工作中每個階段的潛在節省金額，而不是在工作層級重複計算節省金額。這可能會導致系統高估複雜查詢模式資料表的建議。

### 確認工作負載是否受到影響

如要驗證特定叢集建議，可以在 Google Cloud 控制台中執行下列查詢，找出可能導致高估的工作。

這項查詢會在工作記錄中搜尋單一工作掃描相同資料表，且執行階段超過 10 個的執行個體。

```
SELECT
  job_id,
  project_id,
  user_email,
  table_name,
  scan_count,
  total_billed_gb,
  creation_time
FROM (
  SELECT
    job_id,
    project_id,
    user_email,
    creation_time,
    total_bytes_billed / (1024*1024*1024) as total_billed_gb,
    -- Extract the table name from the 'READ' substeps
    REGEXP_EXTRACT(substep, r'FROM ([^ ]+)') as table_name,
    COUNT(DISTINCT stage.id) as scan_count
  FROM `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS,
  UNNEST(job_stages) as stage,
  UNNEST(stage.steps) as step,
  UNNEST(step.substeps) as substep
  WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 14 DAY)
    AND step.kind = 'READ'
    AND substep LIKE 'FROM %'
    -- Exclude internal intermediate stages
    AND NOT REGEXP_CONTAINS(substep, r'FROM __stage')
  GROUP BY 1, 2, 3, 4, 5, 6
)
WHERE scan_count > 10 -- Adjust this threshold to find more complex query patterns
ORDER BY scan_count DESC
LIMIT 100;
```

將 `REGION_NAME` 替換為專案所在的區域。

如果建議中的資料表有高 `scan_count` (例如大於 20) 的工作，該資料表的預估節省金額可能就會膨脹。雖然叢集仍可能帶來效能優勢，但實際節省的費用不會達到建議所指的程度。

## 定價

將建議套用至表格時，可能會產生下列費用：

* **處理成本。**套用建議時，您會對 BigQuery 專案執行資料定義語言 (DDL) 或資料操縱語言 (DML) 查詢。
* **儲存空間費用**。如果使用複製資料表的方法，複製 (或備份) 的資料表會佔用額外儲存空間。

系統會根據與專案相關聯的帳單帳戶，收取標準處理和儲存費用。詳情請參閱 [BigQuery 計價方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw)一文。

## 疑難排解

**問題：**特定表格未顯示任何建議。

如果資料表符合下列條件，系統可能不會顯示分區建議：

* 表格小於 100 GB。
* 資料表已分區或叢集。

如果資料表符合下列條件，系統可能不會顯示叢集建議：

* 表格小於 10 GB。
* 資料表已叢集化。

在下列情況下，系統可能會抑制分區和叢集建議：

* 資料表因[資料操縱語言 (DML) 作業](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw)而產生高昂的寫入成本。
* 過去 30 天內未讀取資料表。
* 預估每月節省的金額太少 (節省的運算單元時數不到 1 小時)。

**問題：**預估節省金額過高。

如果工作負載涉及複雜查詢，且在多個不同的執行階段中多次參照相同資料表，系統可能會高估每月預估節省金額。詳情請參閱「[高估節省金額](#overestimation)」一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]