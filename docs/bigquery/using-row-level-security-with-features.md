Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將資料列層級的安全性與其他 BigQuery 功能搭配使用

本文說明如何將資料列層級存取權安全防護機制與其他 BigQuery 功能搭配使用。

閱讀本文前，請先參閱「[BigQuery 資料列層級安全防護機制簡介](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)」和「[使用資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」，瞭解資料列層級安全防護機制。

**注意：**
管理[外部身分識別資訊提供者](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)中使用者存取權時，請將 Google 帳戶主體 ID (例如 `user:kiran@example.com`、`group:support@example.com` 和 `domain:example.com`) 替換為適當的[員工身分聯盟主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。

## `TRUE` 篩選器

資料列層級存取權政策可篩選您在執行查詢時看到的結果資料。如要執行非查詢作業 (例如 DML)，您必須擁有資料表中所有資料列的完整存取權。如要授予完整存取權，請使用資料列存取政策，並將篩選運算式設為 `TRUE`。這項資料列層級存取權政策稱為「*`TRUE` 篩選器*」。

任何使用者 (包括服務帳戶) 都可以獲得`TRUE`篩選器存取權。

非查詢作業的例子包括：

* 其他 BigQuery API，例如 [BigQuery Storage Read API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)。
* 部分 [`bq` 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)指令，例如 [`bq head`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_head) 指令。
* [複製資料表](#features_that_work_with_the_true_filter)

### `TRUE` 篩選器範例

```
CREATE ROW ACCESS POLICY all_access ON project.dataset.table1
GRANT TO ("group:all-rows-access@example.com")
FILTER USING (TRUE);
```

### 可搭配 `TRUE` 篩選器使用的功能

對受資料列存取權政策保護的資料表使用 [DML](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw) 作業時，您必須使用 `TRUE` 篩選器，這表示您有權存取整個資料表。不會變更資料表結構定義的任何作業，都會保留資料表中的所有資料列存取政策。

舉例來說，[`ALTER TABLE RENAME
TO`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_rename_to_statement) 陳述式會將原始資料表的資料列存取政策複製到新資料表。再舉一例，[`TRUNCATE
TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#truncate_table_statement) 陳述式會移除資料表中的所有資料列，但會保留資料表結構定義和任何資料列存取政策。

#### 複製工作

如要[複製含有至少一項資料列層級存取政策的資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)，您必須先取得來源資料表的`TRUE`篩選器存取權。來源資料表的所有資料列層級存取政策也會複製到新的目的地資料表。如果將沒有資料列層級存取政策的來源資料表，複製到有資料列層級存取政策的目的地資料表，則目的地資料表的資料列層級存取政策會遭到移除，除非使用 `--append_table` 旗標或設定 `"writeDisposition": "WRITE_APPEND"`。

允許跨區域複製，且會複製所有政策。如果查詢在子查詢政策中含有無效的資料表參照，複製完成後，後續查詢可能會中斷。

資料表的資料列層級存取政策名稱不得重複。複製期間，如果資料列層級存取政策名稱發生衝突，就會導致輸入內容無效錯誤。

**注意：** 複製資料表後，複製的任何資料列層級 或資料欄層級 存取權政策，都會與原始資料表的安全性無關。目的地資料表的安全性不會與原始資料表的安全性同步。

##### 複製設有資料列層級存取權政策的資料表時，所需的權限

如要複製含有至少一項資料列層級存取權政策的資料表，除了[複製資料表和分區的角色](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#roles_to_copy_tables_and_partitions)之外，您還必須具備下列權限。

| **權限** | **資源** |
| --- | --- |
| `bigquery.rowAccessPolicies.list` | 來源資料表。 |
| `bigquery.rowAccessPolicies.getIamPolicy` | 來源資料表。 |
| [`TRUE` 篩選器](#the_true_filter) | 來源資料表。 |
| `bigquery.rowAccessPolicies.create` | 目的地資料表。 |
| `bigquery.rowAccessPolicies.setIamPolicy` | 目的地資料表。 |

#### BigQuery API 中的 Tabledata.list

如要在具有資料列層級存取權政策的資料表上，使用 BigQuery API 中的 `tabledata.list` 方法，您需要 `TRUE` 篩選器存取權。

#### DML

如要執行 DML 陳述式，更新具有資料列層級存取權政策的資料表，您需要該資料表的`TRUE`篩選器存取權。

特別是 `MERGE` 陳述式會與資料列層級存取政策互動，如下所示：

* 如果目標資料表包含資料列層級存取權政策，則您需要`TRUE`目標資料表的篩選存取權。
* 如果來源資料表包含資料列層級的存取權政策，則 `MERGE`
  陳述式只會對使用者可見的資料列採取行動。

#### 資料表快照

[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)支援資料列層級安全防護機制。如要瞭解基本資料表 (來源資料表) 和資料表快照 (目的地資料表) 的必要權限，請參閱「[複製含有資料列層級存取權政策的資料表時所需的權限](#required_permissions_to_copy_a_table_with_a_row-level_access_policy)」。

## 含有 JSON 資料欄的 BigQuery 資料表

資料列層級存取政策無法套用至 [JSON 欄](https://docs.cloud.google.com/bigquery/docs/json-data?hl=zh-tw)。
如要進一步瞭解資料列層級安全防護機制的限制，請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw#limitations)」一節。

## BigQuery BI Engine 和數據分析

[BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 不會加速對具有一或多項資料列層級存取權政策的資料表執行的查詢，這些查詢會在 BigQuery 中以標準查詢的形式執行。

系統會根據基礎來源資料表的資料列層級存取權政策，篩選數據分析資訊主頁中的資料。

## 資料欄層級的安全防護機制

列層級安全防護和欄層級安全防護完全相容，包括[欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。

重點如下：

* 您可以套用資料列層級的存取權政策，篩選任何資料欄中的資料，即使您無法存取該資料欄中的資料也沒問題。
  + 如果嘗試透過子查詢資料列層級存取政策存取這些資料欄，系統會顯示存取遭拒的錯誤訊息。這些資料欄不屬於系統參照資料欄。
  + 嘗試使用非子查詢資料列層級存取權政策存取這些資料欄時，會略過資料欄層級安全防護機制。
* 如果資料欄因資料欄層級安全防護機制而受到限制，且查詢的 `SELECT` 陳述式或子查詢資料列層級存取權政策中包含該資料欄的名稱，您就會收到錯誤訊息。
* 資料欄層級安全防護機制也適用於 `SELECT *` 查詢陳述式。系統會將 `SELECT *` 視為明確指定受限資料欄的查詢。

### 資料列層級安全防護機制和資料欄層級安全防護機制互動的範例

這個範例會逐步說明如何保護資料表，然後查詢資料表。

#### 資料

假設您擁有名為 `my_dataset` 的資料集 DataOwner 角色，該資料集包含名為 `my_table` 的資料表，其中有三個資料欄。表格包含下表顯示的資料。

在這個範例中，其中一位使用者是 **Alice**，電子郵件地址為 `alice@example.com`。第二位使用者是 Alice 的同事 **Bob**。

| **rank** | **水果** | **color** |
| --- | --- | --- |
| 1 | apple | 紅色 |
| 2 | orange | orange |
| 3 | 萊姆綠 | 綠色 |
| 4 | 檸檬 | 黃色 |

#### 安全性

您希望 Alice 能查看 `rank` 欄中含有奇數的所有資料列，但不能查看含有偶數的資料列。您不希望阿斌看到任何資料列，
包括偶數或奇數列。您不希望任何人看到 `fruit` 欄中的任何資料。

* 如要限制 Alice 查看偶數列，請建立資料列層級的存取權政策，其中包含以 `rank` 資料欄顯示資料為依據的篩選運算式。如要避免 Bob 看到偶數或奇數列，請不要將他加入受讓人清單。

  ```
  CREATE ROW ACCESS POLICY only_odd ON my_dataset.my_table GRANT
  TO ('user:alice@example.com') FILTER USING (MOD(rank, 2) = 1);
  ```
* 如要禁止所有使用者查看名為 `fruit` 的資料欄中的資料，請建立資料欄層級的安全政策標記，禁止所有使用者存取該資料欄中的任何資料。

最後，您也會透過兩種方式限制存取名為 `color` 的資料欄：資料欄同時受資料欄層級安全防護政策標記控管，禁止任何人存取，*且*受資料列層級存取權政策影響，該政策會篩選 `color` 資料欄中的部分資料列資料。

* 這項第二個資料列層級存取權政策只會顯示 `color` 資料欄中含有 `green` 值的資料列。

  ```
  CREATE ROW ACCESS POLICY only_green ON my_dataset.my_table
  GRANT TO ('user:alice@example.com') FILTER USING (color="green");
  ```

#### Bob 的查詢

如果 Alice 的同事 Bob 嘗試從 `my_dataset.my_table` 查詢資料，他不會看到任何資料列，因為 Bob 不在資料表任何資料列層級存取權政策的受讓人清單中。

| **查詢** | **`my_dataset.my_table`** | | | **註解** |
| --- | --- | --- | --- | --- |
|  | **`rank`**   (部分資料受到資料列存取政策 `only_odd` 影響) | **`fruit`**   (所有資料都受到 CLS 政策標記保護) | **`color`**   (所有資料都受到 CLS 政策標記保護，*且*部分資料受到資料列存取政策 `only_green` 影響) |  |
| `SELECT rank FROM my_dataset.my_table` | (0) rows returned. |  |  | Bob 不在列層級存取政策的受讓人清單中，因此這項查詢會成功，但不會傳回任何資料列資料。   系統會向 Bob 顯示訊息，指出他的結果可能會受到資料列存取政策的篩選。 |

#### Alice 的查詢

當艾麗執行查詢來存取 `my_dataset.my_table` 的資料時，結果取決於她執行的查詢和安全性，如下表所示。

| **查詢** | **`my_dataset.my_table`** | | | **註解** |
| --- | --- | --- | --- | --- |
|  | **`rank`**   (部分資料受到資料列存取政策 `only_odd` 影響) | **`fruit`**   (所有資料都受到 CLS 政策標記保護) | **`color`**   (所有資料都受到 CLS 政策標記保護，*且*部分資料受到資料列存取政策 `only_green` 影響) |  |
| `SELECT rank FROM my_dataset.my_table` | 系統會傳回 1 個資料列。 |  |  | Alice 位於 `only_odd` 和 `only_green` 資料列層級存取權政策的受讓人清單中。因此，Alice 只會看到奇數排名和綠色。因此，Alice 會看到以下資料列：    `rank: 3, color: green`。   Alice 無法看到「水果」欄，因為該欄受到資料欄層級安全性政策限制。    系統會向 Alice 顯示訊息，指出系統可能會根據資料列存取政策篩選結果。 |
| `SELECT fruit FROM my_dataset.my_table` |  | `access denied` |  | 查詢中明確指定了 `fruit` 欄。    系統會套用資料欄層級安全防護機制。    存取遭拒。 |
| `SELECT color FROM my_dataset.my_table` |  |  | 系統會傳回 1 個資料列。 | Alice 位於 `only_odd` 和 `only_green` 資料列層級存取權政策的受讓人清單中。因此，Alice 只會看到奇數排名和綠色。因此，Alice 會看到以下資料列：    `rank: 3, color: green`。   Alice 無法看到「水果」欄，因為該欄受到資料欄層級安全性政策限制。    系統會向 Alice 顯示訊息，指出系統可能會根據資料列存取政策篩選結果。 |
| `SELECT rank, fruit FROM my_dataset.my_table` |  | `access denied` |  | 查詢中明確指定了 `fruit` 欄。    資料欄層級安全性政策會先套用，再套用 `rank` 資料欄的資料列層級存取政策。    存取遭拒。 |
| `SELECT rank, color FROM my_dataset.my_table` |  |  | 系統會傳回 1 個資料列。 | Alice 位於 `only_odd` 和 `only_green` 資料列層級存取權政策的受讓人清單中。因此，Alice 只會看到奇數排名和綠色。因此，Alice 會看到以下資料列：    `rank: 3, color: green`。   Alice 無法看到「水果」欄，因為該欄受到資料欄層級安全性政策限制。    系統會向 Alice 顯示訊息，指出系統可能會根據資料列存取政策篩選結果。 |
| `SELECT fruit, color FROM my_dataset.my_table` |  | `access denied` |  | 查詢中明確指定了 `fruit` 欄。    `fruit` 資料欄的資料欄層級安全防護機制會先套用， 再套用 `color` 資料欄資料的資料列層級存取政策。   存取遭拒。 |
| `SELECT * FROM my_dataset.my_table` | 系統會傳回 1 個資料列。 |  |  | Alice 位於 `only_odd` 和 `only_green` 資料列層級存取權政策的受讓人清單中。因此，Alice 只會看到奇數排名和綠色。因此，Alice 會看到以下資料列：    `rank: 3, color: green`。   Alice 無法看到「水果」欄，因為該欄受到資料欄層級安全性政策限制。    系統會向 Alice 顯示訊息，指出系統可能會根據資料列存取政策篩選結果。 |

#### `TRUE` 篩選器存取權

最後，如[`TRUE` 篩選器存取權一節](#the_true_filter)所述，如果 Alice 或 Bob 擁有 `TRUE` 篩選器存取權，就能查看資料表中的所有資料列，並在非查詢作業中使用。不過，如果資料表設有資料欄層級的安全防護機制，這項機制仍會生效，並可能影響結果。

## 執行圖

如果作業採用資料列層級存取政策，就無法使用[查詢執行圖](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)。

## 擷取工作

如果資料表設有資料列層級的存取權政策，執行擷取工作時，系統只會將您可檢視的資料匯出至 Cloud Storage。

## 舊版 SQL

舊版 SQL 不支援資料列層級存取權政策。查詢含有資料列層級存取政策的資料表時，必須使用 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-tw)。系統會拒絕舊版 SQL 查詢。

## 分區和分群資料表

資料列層級安全防護機制不會參與查詢[修剪](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)，這是[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)的功能。

資料列層級安全防護機制與分區和叢集資料表相容，但系統不會在分區修剪期間套用篩除資料列資料的資料列層級存取權政策。如果資料表使用資料列層級安全性，您仍可指定在分區資料欄上運作的 `WHERE` 子句，對資料表使用分區修剪功能。同樣地，資料列層級存取政策本身不會為針對叢集資料表的查詢帶來任何效能優勢，但不會干擾您套用的其他篩選條件。

執行資料列層級存取權政策時，系統會使用政策中的篩選器執行查詢修剪作業。

## 重新命名資料表

如要重新命名含有至少一項資料列存取政策的資料表，您不需要 `TRUE` 篩選器存取權。您可以[使用 DDL 陳述式重新命名資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_rename_to_statement)。

您也可以複製資料表，並為目的地資料表指定不同名稱。如果來源資料表設有資料列層級存取權政策，請參閱本頁面的[資料表複製工作](#features_that_work_with_the_true_filter)，瞭解詳情。

## 串流更新

如要使用[變更資料擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)功能執行串流資料表 `UPDATE` 或 `DELETE` 作業，您必須具備 `TRUE` 篩選器存取權。

## 時間回溯

如果資料表設有 (或曾設有) 資料列層級存取權政策，只有資料表管理員可以存取該資料表的歷來資料。如果其他使用者在具有資料列層級存取權的資料表上使用時間旅行裝飾器，就會收到 `access
denied` 錯誤訊息。詳情請參閱「[時間旅行和資料列層級存取權](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel_and_row-level_access)」。

## 邏輯、具體化和授權檢視表

本節說明不同類型的 BigQuery 檢視區塊，以及這些檢視區塊如何與資料列層級安全防護機制互動。

### 邏輯或具體化檢視表

系統會根據資料表查詢建立邏輯或具體化檢視表。
查詢結果通常是資料表資料的子集。

這兩種檢視畫面顯示的資料，都會根據基礎來源資料表的資料列層級存取權政策進行篩選。不過，您無法在資料列層級存取政策中參照檢視表或具體化檢視表。

### 具體化檢視表的效能

此外，如果[materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)是衍生自具有資料列層級存取權政策的基礎資料表，查詢效能會與直接查詢來源資料表時相同。換句話說，如果來源資料表採用資料列層級安全防護機制，查詢具體化檢視區時，您不會看到相較於查詢來源資料表，典型的效能優勢。

### 授權檢視表

您也可以授權邏輯或具體化檢視，也就是與特定使用者或群組 (主體) 共用檢視。主體隨後可以查詢檢視區塊，但無法存取基礎資料表。詳情請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

## 萬用字元查詢

如果資料表設有資料列層級存取權政策，對這類資料表執行[萬用字元查詢](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)會失敗，並顯示 `INVALID_INPUT` 錯誤。

## 後續步驟

* 如要瞭解資料列層級存取政策的最佳做法，請參閱「[BigQuery 資料列層級安全防護最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]