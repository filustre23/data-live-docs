Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# CONSTRAINT\_COLUMN\_USAGE 檢視區塊

`CONSTRAINT_COLUMN_USAGE` 檢視區塊包含[限制](https://docs.cloud.google.com/bigquery/docs/primary-foreign-keys?hl=zh-tw)使用的所有資料欄。如為`PRIMARY KEY`限制，這些是 `KEY_COLUMN_USAGE` 檢視畫面中的資料欄。如果是 `FOREIGN KEY` 限制，這些是參照資料表的資料欄。

## 必要的角色

如要取得查詢 `INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE` 檢視畫面所需的權限，請要求管理員授予您專案的「[BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor) 」(`roles/bigquery.dataEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備查詢 `INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE` 檢視畫面所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要查詢 `INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE` 檢視畫面，必須具備下列權限：

* 查看主鍵和外鍵定義：
  `bigquery.tables.get`
* 查看資料表資訊結構定義：
  `bigquery.tables.list`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 結構定義

`INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `table_catalog` | `STRING` | 資料集所屬專案的名稱。 |
| `table_schema` | `STRING` | 包含資料表的資料集名稱。也稱為「`datasetId`」。 |
| `table_name` | `STRING` | 資料表的名稱。也稱為「`tableId`」。 |
| `column_name` | `STRING` | 資料欄名稱。 |
| `constraint_catalog` | `STRING` | 限制專案名稱。 |
| `constraint_schema` | `STRING` | 限制資料集名稱。 |
| `constraint_name` | `STRING` | 限制條件名稱。如果資料欄用於主鍵，則可以是主鍵名稱；如果資料欄用於外鍵，則可以是外鍵名稱。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含資料集限定詞。如要查詢具有資料集限定詞的資料，您必須具備該資料集的權限。詳情請參閱「[語法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)」。下表列出這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]DATASET.INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE;` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`： Google Cloud 專案 ID。如未指定，系統會使用預設專案。

## 範例

以下查詢會顯示資料集中單一資料表的限制：

```
SELECT *
FROM PROJECT_ID.DATASET.INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE
WHERE table_name = TABLE;
```

更改下列內容：

* `PROJECT_ID`：選用。雲端專案的名稱。如未指定，這項指令會使用預設專案。
* `DATASET`：資料集名稱。
* `TABLE`：資料表名稱。

反之，下列查詢會顯示單一資料集中所有資料表的限制。

```
SELECT *
FROM PROJECT_ID.DATASET.INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE;
```

在現有限制下，查詢結果類似於下列內容：

```
+-----+---------------------+--------------+------------+-------------+---------------------+-------------------+-------------------------+
| row |    table_catalog    | table_schema | table_name | column_name | constraint_catalog  | constraint_schema |     constraint_name     |
+-----+---------------------+--------------+------------+-------------+---------------------+-------------------+-------------------------+
|   1 | myConstraintCatalog | myDataset    | orders     | o_okey      | myConstraintCatalog | myDataset         | orders.pk$              |
|   2 | myConstraintCatalog | myDataset    | orders     | o_okey      | myConstraintCatalog | myDataset         | lineitem.lineitem_order |
+-----+---------------------+--------------+------------+-------------+---------------------+-------------------+-------------------------+
```

**注意：** `lineitem.lineitem_order` 是在 `lineitem` 資料表中定義的外鍵。

如果資料表或資料集沒有限制，查詢結果會如下所示：

```
+-----------------------------+
| There is no data to display |
+-----------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]