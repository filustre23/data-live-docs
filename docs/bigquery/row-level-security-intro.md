Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料列層級安全防護機制簡介

**注意：**如果預留項目是以特定 BigQuery 版本建立，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

本文說明資料列層級安全性的概念、在 BigQuery 中的運作方式、何時應使用資料列層級安全性保護資料，以及其他詳細資料。

## 什麼是資料列層級安全性？

資料列層級安全性可讓您篩選資料，並根據符合條件的使用者條件，存取資料表中的特定資料列。

BigQuery 支援專案、資料集和資料表層級的存取控管，以及透過政策標記實施[資料欄層級安全防護](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)。資料列層級安全性可透過資料列層級存取權政策，對 BigQuery 資料表中的部分資料啟用精細的存取控管，進而擴充最小權限原則。

一個資料表可以有多項資料列層級存取權政策。資料列層級存取權政策可與 [資料欄層級安全性](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)、[資料集層級](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)、[資料表層級](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_table_or_view)和[專案層級](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)存取控管機制[並存於資料表](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#example_of_row-level_security_and_column-level_security_interacting)。

## 資料列層級安全性的運作方式

概括來說，資料列層級安全性涉及在目標 BigQuery 資料表上建立資料列層級存取權政策。這些政策會做為篩選器，根據使用者或群組是否在允許清單中，隱藏或顯示特定資料列。任何未明確列入允許清單的使用者或群組，都無法存取。

**注意：**如果您建立新的資料列層級安全性政策來限制資料列存取權，則必須將先前具備完整存取權的使用者新增至 [`TRUE` 篩選器](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#the_true_filter)，才能維持其存取權。

具備 Identity and Access Management (IAM) 角色 [BigQuery 管理員或 BigQuery 資料擁有者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)的授權使用者，可以建立 BigQuery 資料表的資料列層級存取權政策。

建立資料列層級存取權政策時，您必須指定資料表名稱，以及哪些使用者或群組 (稱為「`grantee-list`」) 可以存取特定資料列。政策也包含要篩選的資料，稱為`filter_expression`。`filter_expression` 的功能類似於一般查詢中的 `WHERE` 子句。

**注意：**與 `WHERE` 子句一樣，`filter_expression` 會比對您要向 `grantee_list` 中的主體顯示的資料。不在 `grantee_list` 中的使用者則無法查看任何資料列。

如要瞭解如何建立及使用資料列層級存取權政策，請參閱「[管理資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」。

如要瞭解建立資料列層級存取權政策時的完整語法、用法和選項，請參閱 [DDL 參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_row_access_policy_statement)。

### 應用實例

以下範例說明資料列層級安全性的潛在使用案例。

**注意：**
管理[外部識別資訊提供者](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)中的使用者存取權時，請將 Google 帳戶主體 ID 的例項 (例如 `user:kiran@example.com`、`group:support@example.com` 和 `domain:example.com`) 替換為適當的[員工身分聯盟主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。

#### 依區域篩選資料列

假設資料表 `dataset1.table1` 包含屬於不同區域的資料列 (以 `region` 欄表示)。

您可以使用下列查詢建立及填入範例資料表：

```
CREATE TABLE IF NOT EXISTS
  dataset1.table1 (partner STRING,
    contact STRING,
    country STRING,
    region STRING);
INSERT INTO
  dataset1.table1 (partner,
    contact,
    country,
    region)
VALUES
  ('Example Customers Corp', 'alice@examplecustomers.com', 'Japan', 'APAC'),
  ('Example Enterprise Group', 'bob@exampleenterprisegroup.com', 'Singapore', 'APAC'),
  ('Example HighTouch Co.', 'carrie@examplehightouch.com', 'USA', 'US'),
  ('Example Buyers Inc.', 'david@examplebuyersinc.com', 'USA', 'US');
```

資料擁有者或管理員可透過資料列層級安全性功能，實施相關政策。下列陳述式會實作一項政策，限制亞太地區郵寄群組中的使用者只能查看亞太地區的合作夥伴：

```
CREATE ROW ACCESS POLICY
  apac_filter
ON
  dataset1.table1 GRANT TO ("group:sales-apac@example.com")
FILTER USING
  (region="APAC" );
```

因此，`sales-apac@example.com` 群組中的使用者只能查看 `region` 值為 `APAC` 的資料列。

下列陳述式會實作一項政策，限制個人和群組只能查看美國地區的合作夥伴：

```
CREATE ROW ACCESS POLICY
  us_filter
ON
  dataset1.table1 GRANT TO ("group:sales-us@example.com",
"user:jon@example.com")
FILTER USING
  (region="US");
```

因此，群組 `sales-us@example.com` 中的使用者和使用者 `jon@example.com` 只能查看 `region` 值為 `US` 的資料列。

不屬於 `APAC` 或 `US` 群組的使用者不會看到任何資料列。

#### 根據機密資料篩選資料列

現在，假設您有另一個用途，需要使用包含薪資資訊的資料表。

您可以使用下列查詢建立及填入範例資料表：

```
CREATE OR REPLACE TABLE
  dataset1.table1 (name STRING,
    department STRING,
    salary INT64,
    email STRING);
INSERT INTO
  dataset1.table1 ( name,
    department,
    salary,
    email)
VALUES
  ('Jim D', 'HR', 100000, 'jim@example.com'),
  ('Anna K', 'Finance', 100000, 'anna@example.com'),
  ('Bruce L', 'Engineering', 100000, 'bruce@example.com'),
  ('Carrie F', 'Business', 100000, 'carrie@example.com');
```

下列陳述式中的資料列存取權政策，會限制只有公司網域成員才能查詢。此外，使用 `SESSION_USER()` 函式時，系統會根據執行查詢的使用者電子郵件地址，限制使用者只能存取屬於自己的資料列。

```
CREATE ROW ACCESS POLICY
  salary_personal
ON
  dataset1.table1 GRANT TO ("domain:example.com")
  FILTER USING
  (Email=SESSION_USER());
```

下圖說明資料列存取權政策如何限制含有薪資資訊的資料表。在這個範例中，使用者名稱為 Jim，電子郵件地址為 `jim@example.com`。

如需更多資料列層級安全防護機制的範例，請參閱「[使用資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」。

#### 根據對照表篩選資料列資料

有了子查詢支援，資料列存取權政策就能參照其他資料表，並將其做為對照表。篩選規則中使用的資料可以儲存在資料表中，而單一子查詢資料列存取政策可以取代多個已設定的資料列存取政策。如要更新資料列存取政策，只需更新對照表，即可取代多項資料列存取政策。您不必逐一更新資料列存取權政策。

如需篩選資料列資料的範例，請參閱「[使用資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」。

## 資料列層級安全防護機制與其他方法的使用時機

[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)、資料列層級存取權政策，以及將資料儲存在不同的資料表中，都能提供不同程度的安全性、效能和便利性。請務必根據用途選擇合適的機制，確保資料獲得適當的安全防護。

### 與授權檢視表比較：安全漏洞

如果使用不當，資料列層級安全防護機制和[透過授權檢視表強制執行資料列層級存取權](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw#combine_row-level_security_with_authorized_views)都可能存在安全漏洞。

*使用授權檢視表或資料列層級存取權政策，實施資料列層級安全性時，建議您使用[稽核記錄](#audit_logging_and_monitoring)監控任何可疑活動。*

查詢時間長度等側通道可能會洩漏儲存體 shard 邊緣的資料列資訊。這類攻擊可能需要瞭解資料表的分區方式，或需要大量查詢。

如要進一步瞭解如何防範這類旁路攻擊，請參閱「[資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw#limit-side-channel-attacks)」。

### 授權檢視表、資料列層級安全性和獨立資料表的比較

下表比較授權檢視表、資料列層級存取權政策和獨立資料表的彈性、效能和安全性。

| **方法** | **安全性考量** | **建議** |
| --- | --- | --- |
| **授權**  **檢視表** | 建議使用，可享有彈性。容易受到精心設計的查詢、查詢時間和其他類型的旁路攻擊。 | 如需與他人共用資料，且彈性和效能很重要，則授權檢視表是不錯的選擇。舉例來說，您可以使用授權檢視表，在工作群組內共用資料。 |
| **資料列層級存取政策** | 建議用於兼顧彈性和安全性。容易受到[查詢時間旁路攻擊](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw#limit-side-channel-attacks)。 | 如需與他人共用資料，並想為檢視表或資料表切片提供額外安全性，資料列層級存取權政策是不錯的選擇。舉例來說，您可以使用資料列層級存取權政策，與使用相同資訊主頁的使用者共用資料，即使部分使用者可存取的資料比其他人多也沒問題。 |
| **分開表格** | 建議用於安全性。使用者必須具備資料表存取權，才能推論資料。 | 如需與他人共用資料，且必須隔離資料，則適合使用獨立資料表。舉例來說，如果資料列總數必須保密，您可以使用個別資料表與第三方合作夥伴和供應商共用資料。 |

## 建立及管理資料列層級存取權政策

如要瞭解如何建立、更新 (重新建立)、列出、查看及刪除資料表的資料列層級存取權政策，以及如何查詢具有資料列層級存取權政策的資料表，請參閱「[使用資料列層級存取權安全性](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」。

## 隱含刪除資料列層級存取權政策

在某些情況下，資料列存取政策可能會從資料表中隱含 (自動) 移除。

自動刪除資料列存取權政策的一般原則如下：

* 使用 [`WRITE_TRUNCATE` 寫入配置](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.write_disposition)的操作，一律會覆寫目的地資料表上任何現有的資料列存取政策。
* 如果作業的寫入配置為 `WRITE_APPEND`，系統會保留目的地資料表目前的資料列存取權政策，並將來源資料表的政策新增至目的地資料表。

具體來說，資料列存取權政策會在下列情況下隱含移除：

* 取代資料表：使用 [`CREATE OR REPLACE
  TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) DDL 陳述式取代資料表時，原始資料表的所有現有資料列存取政策都會遭到捨棄。即使替換查詢是根據原始資料表的資料，也會發生這種情況。
* 使用 `WRITE_TRUNCATE` 載入或查詢：使用 `WRITE_TRUNCATE` 寫入處置的操作會移除所有現有的資料列存取權政策。包括使用 [`bq load
  --replace`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令載入資料，以及在 `writeDisposition` 狀態設為 `WRITE_TRUNCATE` 的情況下執行查詢。這類作業會完全覆寫資料表，且不會沿用資料列存取權政策。
* 資料表刪除或到期：如果資料表明確遭到刪除，或達到到期時間並自動移除，所有相關聯的資料列存取權政策也會一併刪除。
* 資料表複製作業：將沒有資料列存取政策的資料表複製到有資料列存取政策的目的地資料表時，除非使用 [`--append_table`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 旗標或 `"writeDisposition": "WRITE_APPEND"`，否則目的地資料表的政策會遭到移除。如要進一步瞭解資料表複製工作，請參閱「[搭配其他 BigQuery 功能使用資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#features_that_work_with_the_true_filter)」。

使用 [`TRUNCATE
TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#truncate_table_statement) DML 陳述式，在保留資料表結構定義的同時移除所有資料列，不會移除資料列存取政策。

## 配額

如要進一步瞭解資料列層級安全性的配額和限制，請參閱 BigQuery [配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#row-level_security)。

## 定價

BigQuery 內建資料列層級安全防護機制，不需額外付費。不過，資料列層級存取權政策可能會透過下列方式，影響執行查詢的費用：

* 資料列層級存取權政策可能會產生額外費用，尤其是包含子查詢且參照其他資料表的政策。
* 資料列層級存取政策篩選器不會參與[分區和分群資料表](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#partitioned_and_clustered_tables)的查詢剪除。這不代表在執行主要查詢時，會讀取更多資料。不會利用資料列存取政策述詞進一步剪除。
* 使用資料列層級存取權政策篩選器時，並非所有使用者篩選器都會提早套用。這可能會增加從資料表讀取的資料量，並可能讀取更多資料列並產生費用。

如要進一步瞭解 BigQuery 查詢定價，請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」。

## 限制

如要瞭解資料列層級安全防護機制的限制，請參閱 BigQuery [資料列層級安全防護機制限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#row-level_security)。以下各節說明其他資料列層級安全性限制。

### 效能限制

* 處理含有資料列層級存取權政策的資料表時，部分 BigQuery 功能不會加速，例如 [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#bi-engine) 和[具體化檢視表](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#logical_materialized_and_authorized_views)。
* 資料列層級安全性不參與查詢[剪除](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#overview)，這是[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)的功能。詳情請參閱「[分區和分群資料表](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#partitioned_and_clustered_tables)」。這項限制不會降低主要查詢的執行速度。
* 查詢具有資料列層級安全性的資料表時，效能可能會略微降低。

如要進一步瞭解資料列層級安全性如何與某些 BigQuery 功能和服務互動，請參閱「[搭配使用資料列層級安全性與其他 BigQuery 功能](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)」。

### 其他限制

* 如果預留項目是以特定 BigQuery 版本建立，則可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
* 資料列存取權政策與舊版 SQL 不相容。查詢具有資料列層級存取權政策的資料表時，必須使用 GoogleSQL。系統會拒絕舊版 SQL 查詢並傳回錯誤。
* 您無法對 [JSON 資料欄](https://docs.cloud.google.com/bigquery/docs/json-data?hl=zh-tw)套用資料列層級存取權政策。
* 如果資料表設有資料列存取政策，則不支援 Wildcard 資料表查詢。
* 資料列存取政策無法套用至臨時資料表。
* 如果資料表參照其他具有資料列層級安全性的資料表，則無法對該資料表套用資料列層級存取權政策。
* BigQuery 的部分功能與資料列層級安全性不相容。詳情請參閱「[使用資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)」。

  + 包含[子查詢](#filter_row_data_based_on_lookup_table)的資料列存取權政策與 [BigQuery Storage Read API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 不相容。BigQuery Storage Read API 僅支援簡單的篩選器述詞。
* 非查詢作業 (包括服務帳戶工作) 如果需要完整存取資料表資料，可以使用資料列層級安全性搭配 [`TRUE` 篩選器](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#the_true_filter)。例如[資料表複製](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#features_that_work_with_the_true_filter)、[Managed Service for Apache Spark 工作流程](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#tabledata-list)等。詳情請參閱「[使用資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)」。
* 您可以使用 DDL 陳述式或[資料列存取政策 API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw#rest-resource:-v2.rowaccesspolicies)，建立、取代或刪除資料列層級存取政策。您也可以在 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw)中，執行資料列存取權政策 API 中的所有可用動作。您可以在Google Cloud 控制台中列出及查看資料列層級存取權政策。
* [預覽或瀏覽資料表](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw#browse-table)與資料列層級安全性不相容。
* [資料表取樣](https://docs.cloud.google.com/bigquery/docs/table-sampling?hl=zh-tw)與資料列層級安全性不相容。
* 資料列層級存取權政策會對其內部的頂層子查詢結果，施加 100 MB 的限制。超過這個門檻會導致查詢失敗。請注意，這項限制是以政策為單位套用，不會影響使用者查詢。
* 如果 `search_value` 的類型為 `FLOAT`、`STRUCT`、`ARRAY`、`JSON` 或 `GEOGRAPHY`，則資料列存取權政策不支援頂層 [`IN` 子查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/subqueries?hl=zh-tw#in_subquery_concepts)。
* 如果因刪除任何參照資料表，而無法評估資料列層級存取權政策述詞，查詢就會失敗。
* 子查詢資料列層級存取權政策僅支援 BigQuery 資料表、BigLake 外部資料表和 BigLake 代管資料表。
* 只有在要捨棄或重新命名的資料欄不屬於任何資料列存取權政策時，才允許使用修改資料表結構定義的資料欄[重新命名](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw#change_a_columns_name)和[捨棄](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw#delete_a_column)陳述式。
* [資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)僅適用於具有非子查詢資料列存取權政策的查詢。資料遮蓋功能會套用至資料列層級安全性之上。舉例來說，如果 `location = "US"` 套用了資料列存取權政策，且 `location` 經過遮蓋，使用者就能看到 `location = "US"` 的資料列，但結果中的位置欄位會經過遮蓋。如果查詢涉及子查詢資料列存取政策，則須具備資料列存取政策參照資料欄的「精細讀取者」存取權。

## 稽核記錄和監控

您可透過兩種方式監控 BigQuery 的資料列層級安全性：使用 Cloud Logging 的稽核記錄追蹤政策生命週期和資料存取事件，或查詢 `INFORMATION_SCHEMA.ROW_ACCESS_POLICIES` 檢視表，檢查有效的資料列層級存取權政策定義和中繼資料。

### 稽核記錄

讀取具有一或多個資料列層級存取權政策的資料表資料時，系統會針對該讀取要求，在 IAM 授權資訊中顯示已授權讀取存取權的資料列層級存取權政策，以及子查詢中參照的任何對應資料表。

建立及刪除資料列層級存取權政策時，系統會記錄稽核記錄，並可透過 [Cloud Logging](https://docs.cloud.google.com/logging/docs/overview?hl=zh-tw) 存取。稽核記錄包含資料列層級存取權政策的名稱。不過，資料列層級存取權政策的 `filter_expression` 和 `grantee_list` 定義會從記錄中省略，因為這些定義可能包含使用者或其他機密資訊。列出及查看資料列層級存取權政策時，不會記錄稽核記錄。

如要進一步瞭解 BigQuery 的記錄功能，請參閱「[BigQuery 監控功能簡介](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)」。

如要進一步瞭解 Google Cloud中的記錄功能，請參閱「[Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw)」。

### 使用 `INFORMATION_SCHEMA` 監控

您可以查詢 [`INFORMATION_SCHEMA.ROW_ACCESS_POLICIES` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-row-access-policies?hl=zh-tw)，擷取資料集或區域中有效資料列層級存取權政策的即時中繼資料。檢視表會傳回各項政策的目標資料表、政策名稱、篩選條件述詞 (`filter_predicate`)、建立時間和上次修改時間。

## 後續步驟

* 如要瞭解如何管理資料列層級安全性，請參閱「[使用資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」。
* 如要瞭解資料列層級安全性如何與其他 BigQuery 功能和服務搭配運作，請參閱「[搭配使用資料列層級安全性與其他 BigQuery 功能](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)」。
* 如要瞭解資料列層級安全性的最佳做法，請參閱「[BigQuery 資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-18 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-18 (世界標準時間)。"],[],[]]