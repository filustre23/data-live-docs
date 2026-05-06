Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# SCHEMATA\_REPLICAS\_BY\_FAILOVER\_RESERVATION 檢視區塊

`INFORMATION_SCHEMA.SCHEMATA_REPLICAS_BY_FAILOVER_RESERVATION` 檢視畫面包含與容錯移轉預留項目相關聯的結構定義副本資訊。`INFORMATION_SCHEMA.SCHEMATA_REPLICAS_BY_FAILOVER_RESERVATION` 檢視畫面範圍僅限於容錯移轉預留資源的專案，而非範圍僅限於包含資料集的專案的 [`INFORMATION_SCHEMA.SCHEMATA_REPLICAS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-schemata-replicas?hl=zh-tw)。

## 必要角色

如要取得查詢 `INFORMATION_SCHEMA.SCHEMATA_REPLICAS_BY_FAILOVER_RESERVATION` 檢視畫面所需的權限，請要求系統管理員授予專案的「[BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer) 」(`roles/bigquery.resourceViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 結構定義

`INFORMATION_SCHEMA.SCHEMATA_REPLICAS_BY_FAILOVER_RESERVATION` 檢視表具有下列結構定義：

| 欄 | 類型 | 說明 |
| --- | --- | --- |
| `failover_reservation_project_id` | `STRING` | 如果容錯移轉預留項目管理員專案與副本相關聯，則為該專案的 ID。 |
| `failover_reservation_name` | `STRING` | 容錯移轉預留項目的名稱 (如與副本相關聯)。 |
| `catalog_name` | `STRING` | 資料集所屬專案的專案 ID。 |
| `schema_name` | `STRING` | 資料集的資料集 ID。 |
| `replica_name` | `STRING` | 副本名稱。 |
| `location` | `STRING` | 建立副本的單一區域或多區域。 |
| `replica_primary_assigned` | `BOOL` | 如果值為 `TRUE`，代表副本已指派為主要副本。將次要副本變更為主要副本時，這項狀態會立即生效。 |
| `replica_primary_assignment_complete` | `BOOL` | 如果值為 `TRUE`，表示主要指派作業已完成。 如果值為 `FALSE`，即使 `replica_primary_assigned` 等於 `TRUE`，備用資源也不會 (還不會) 成為主要備用資源。如要瞭解次要副本升級為主要副本所需的時間，請參閱「[升級次要副本](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#promote_the_secondary_replica)」。 |
| `creation_time` | `TIMESTAMP` | 副本的建立時間。首次建立副本時，副本不會與主要副本完全同步，直到 `creation_complete` 等於 `TRUE` 為止。`creation_time` 的值會在 `creation_complete` 等於 `TRUE` 之前設定。 |
| `creation_complete` | `BOOL` | 如果值為 `TRUE`，表示主要副本已完成與次要副本的初始完整同步。 |
| `replication_time` | `TIMESTAMP` | `replication_time` 的值表示資料集的舊度。  副本中的部分資料表可能早於這個時間戳記。這個值只會顯示在次要區域。  如果資料集包含含有串流資料的表格，`replication_time` 的值就不會準確。 |
| `sync_status` | `JSON` | [跨區域複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)和[災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)資料集的主要和次要副本之間的同步狀態。如果副本是主要副本，或資料集未使用複製功能，則傳回 `NULL`。 |
| `replica_primary_assignment_time` | `TIMESTAMP` | 觸發主要資料庫切換至副本的時間。 |
| `replica_primary_assignment_completion_time` | `TIMESTAMP` | 主要執行個體切換至副本的時間。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [RESERVATION_PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.SCHEMATA_REPLICAS_BY_FAILOVER_RESERVATION[_BY_PROJECT] `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：專案 ID。 Google Cloud 如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 範例

本節列出 `INFORMATION_SCHEMA.SCHEMATA_REPLICAS_BY_FAILOVER_RESERVATION` 檢視區塊的查詢範例。

**範例：列出某個區域中的所有複製資料集**

以下範例會列出 `US` 區域中的所有複製資料集：

```
SELECT *
FROM `region-us`.INFORMATION_SCHEMA.SCHEMATA_REPLICAS_BY_FAILOVER_RESERVATION
WHERE failover_reservation_name = "failover_reservation";
```

結果大致如下：

```
+--------------+--------------+--------------+----------+--------------------------+-------------------------------------+---------------------+-------------------+---------------------+---------------------------------+---------------------------+-------------------------------------------------------------------------------+
| catalog_name | schema_name  | replica_name | location | replica_primary_assigned | replica_primary_assignment_complete |    creation_time    | creation_complete |  replication_time   | failover_reservation_project_id | failover_reservation_name |                                  sync_status                                  |
+--------------+--------------+--------------+----------+--------------------------+-------------------------------------+---------------------+-------------------+---------------------+---------------------------------+---------------------------+-------------------------------------------------------------------------------+
| project2     | test_dataset | us-east4     | us-east4 |                     true |                                true | 2024-05-09 20:34:06 |              true |                NULL | project1                        | failover_reservation      |                                                                          NULL |
| project2     | test_dataset | us           | US       |                    false |                               false | 2024-05-09 20:34:05 |              true | 2024-05-10 18:31:06 | project1                        | failover_reservation      | {"last_completion_time":"2024-06-06 18:31:06","error_time":null,"error":null} |
+--------------+--------------+--------------+----------+--------------------------+-------------------------------------+---------------------+-------------------+---------------------+---------------------------------+---------------------------+-------------------------------------------------------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]