Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# MATERIALIZED\_VIEWS 檢視區塊

`INFORMATION_SCHEMA.MATERIALIZED_VIEWS` 檢視畫面包含具體化檢視表的狀態。

## 所需權限

如要取得查詢 `INFORMATION_SCHEMA.MATERIALIZED_VIEWS` 檢視畫面所需的權限，請要求系統管理員授予您專案或資料集的「BigQuery 中繼資料檢視者」 (`roles/bigquery.metadataViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備查詢 `INFORMATION_SCHEMA.MATERIALIZED_VIEWS` 檢視畫面所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要查詢 `INFORMATION_SCHEMA.MATERIALIZED_VIEWS` 檢視畫面，必須具備下列權限：

* `bigquery.tables.get`
* `bigquery.tables.list`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.MATERIALIZED_VIEWS` 檢視表時，查詢結果會為資料集中的每個具體化檢視表包含一個資料列。

`INFORMATION_SCHEMA.MATERIALIZED_VIEWS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `table_catalog` | `STRING` | 包含資料集的專案名稱。也稱為「`projectId`」。 |
| `table_schema` | `STRING` | 包含具體化檢視的資料集名稱。也稱為「`datasetId`」。 |
| `table_name` | `STRING` | materialized view 的名稱。也稱為「`tableId`」。 |
| `last_refresh_time` | `TIMESTAMP` | 上次重新整理這個具體化檢視區塊的時間。 |
| `refresh_watermark` | `TIMESTAMP` | 具體化檢視表的重新整理浮水印。實體化檢視表快取會包含實體化檢視表基礎資料表在此時間之前所含的資料。 |
| `last_refresh_status` | `RECORD` | 上次自動重新整理作業的錯誤結果，以 [ErrorProto](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/ErrorProto?hl=zh-tw) 物件表示。如果顯示這個圖示，表示上次自動重新整理失敗。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含資料集或區域限定詞。如果是含有資料集限定符的查詢，您必須具備該資料集的權限。如要查詢含有區域限定符的資料，您必須具備專案權限。
詳情請參閱「[語法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)」。下表說明這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.MATERIALIZED_VIEWS `` | 專案層級 | `REGION` |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.MATERIALIZED_VIEWS` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：專案 ID。 Google Cloud 如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。
* `DATASET_ID`：資料集的 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

例如：

```
-- Returns metadata for views in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.MATERIALIZED_VIEWS;

-- Returns metadata for all views in a region.
SELECT * FROM region-us.INFORMATION_SCHEMA.MATERIALIZED_VIEWS;
```

## 範例

##### 範例 1：

以下範例會從 `INFORMATION_SCHEMA.MATERIALIZED_VIEWS` 檢視表擷取所有不正常的具體化檢視區塊。系統會傳回預設專案 (`myproject`) 中 `mydataset` 內，具有非 `NULL` `last_refresh_status` 值的具體化檢視區塊。

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：`` `project_id`.dataset.INFORMATION_SCHEMA.MATERIALIZED_VIEWS ``；例如 `` `myproject`.mydataset.INFORMATION_SCHEMA.MATERIALIZED_VIEWS ``。

```
SELECT
  table_name, last_refresh_status
FROM
  mydataset.INFORMATION_SCHEMA.MATERIALIZED_VIEWS
WHERE
  last_refresh_status IS NOT NULL;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
  +---------------+---------------------------------------------------------------------+
  |  table_name   |                        last_refresh_status                          |
  +---------------------------------------------------------------------+---------------+
  |  myview       |   {"reason":"invalidQuery","location":"query","message":"..."}      |
  +---------------------------------------------------------------------+---------------+
```

##### 範例 2：

下列範例會擷取預設專案 (`myproject`) 中 `mydataset` 內具體化檢視 `myview` 的 `last_refresh_time` 和 `refresh_watermark`。結果會顯示實體化檢視上次重新整理的時間，以及將基礎資料表的資料收集到實體化檢視快取的時間。

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：`` `project_id`.dataset.INFORMATION_SCHEMA.MATERIALIZED_VIEWS ``；例如 `` `myproject`.mydataset.INFORMATION_SCHEMA.MATERIALIZED_VIEWS ``。

```
SELECT
  table_name, last_refresh_time, refresh_watermark
FROM
  mydataset.INFORMATION_SCHEMA.MATERIALIZED_VIEWS
WHERE
  table_name = 'myview';
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
  +---------------+------------------------------------------------+
  |  table_name   |  last_refresh_time     | refresh_watermark     |
  +---------------+------------------------------------------------+
  |  myview       | 2023-02-22 19:37:17    | 2023-03-08 16:52:57   |
  +---------------+------------------------------------------------+
```

**注意：** 如果基礎資料表近期沒有變更，BigQuery 會定期增加 `refresh_watermark`，表示 materialized view 是最新狀態，但不會實際重新整理。因此，`last_refresh_time`可能會早於`refresh_watermark`。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]