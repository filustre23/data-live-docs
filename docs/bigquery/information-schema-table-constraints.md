Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# TABLE\_CONSTRAINTS 檢視畫面

`TABLE_CONSTRAINTS` 檢視畫面包含 BigQuery 資料集中的[主鍵和外鍵](https://docs.cloud.google.com/bigquery/docs/primary-foreign-keys?hl=zh-tw)關係。

## 所需權限

您需要下列[身分與存取權管理 (IAM) 權限](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw)：

* `bigquery.tables.get`，即可查看主鍵和外鍵定義。
* `bigquery.tables.list`，即可查看資料表資訊結構定義。

下列每個[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)都具備執行本文詳述工作流程所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

**注意：** 角色會依授予的權限遞增排序。建議您使用清單中較早出現的預先定義角色，避免分配過多權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 結構定義

`INFORMATION_SCHEMA.TABLE_CONSTRAINTS` 檢視表具有下列結構定義：

| 資料欄名稱 | 類型 | 意義 |
| --- | --- | --- |
| `constraint_catalog` | `STRING` | 限制專案名稱。 |
| `constraint_schema` | `STRING` | 限制資料集名稱。 |
| `constraint_name` | `STRING` | 限制名稱。 |
| `table_catalog` | `STRING` | 受限資料表專案名稱。 |
| `table_schema` | `STRING` | 受限資料表的資料集名稱。 |
| `table_name` | `STRING` | 受限的資料表名稱。 |
| `constraint_type` | `STRING` | 可以是 `PRIMARY KEY` 或 `FOREIGN KEY`。 |
| `is_deferrable` | `STRING` | `YES` 或 `NO`，視限制是否可延遲而定。系統僅支援 `NO`。 |
| `initially_deferred` | `STRING` | 系統僅支援 `NO`。 |
| `enforced` | `STRING` | `YES` 或 `NO`，視限制是否強制執行而定。  僅支援 `NO`。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含資料集限定詞。如果查詢含有資料集限定詞，您必須具備該資料集的權限。詳情請參閱「[語法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)」。下表列出這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]DATASET.INFORMATION_SCHEMA.TABLE_CONSTRAINTS;` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。

## 範例

以下查詢會顯示資料集中單一資料表的限制：

```
SELECT *
FROM PROJECT_ID.DATASET.INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE table_name = TABLE;
```

更改下列內容：

* `PROJECT_ID`：選用。雲端專案的名稱。如未指定，這項指令會使用預設專案。
* `DATASET`：資料集名稱。
* `TABLE`：資料表名稱。

反之，下列查詢會顯示單一資料集中所有資料表的限制。

```
SELECT *
FROM PROJECT_ID.DATASET.INFORMATION_SCHEMA.TABLE_CONSTRAINTS;
```

在現有限制下，查詢結果類似於下列內容：

```
+-----+---------------------+-------------------+-----------------------+---------------------+--------------+------------+-----------------+---------------+--------------------+----------+
| Row | constraint_catalog  | constraint_schema |    constraint_name    |    table_catalog    | table_schema | table_name | constraint_type | is_deferrable | initially_deferred | enforced |
+-----+---------------------+-------------------+-----------------------+---------------------+--------------+------------+-----------------+---------------+--------------------+----------+
|   1 | myConstraintCatalog | myDataset         | orders.pk$            | myConstraintCatalog | myDataset    | orders     | PRIMARY KEY     | NO            | NO                 | NO       |
|   2 | myConstraintCatalog | myDataset         | orders.order_customer | myConstraintCatalog | myDataset    | orders     | FOREIGN KEY     | NO            | NO                 | NO       |
+-----+---------------------+-------------------+-----------------------+---------------------+--------------+------------+-----------------+---------------+--------------------+----------+
```

如果資料表或資料集沒有限制，查詢結果會如下所示：

```
+-----------------------------+
| There is no data to display |
+-----------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]