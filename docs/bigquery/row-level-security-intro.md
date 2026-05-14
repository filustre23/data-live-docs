Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料列層級安全防護機制簡介

**注意：** 使用以特定 BigQuery 版本建立的預留項目時，這項功能可能無法使用。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

本文說明資料列層級安全防護機制的概念、在 BigQuery 中的運作方式、何時應使用資料列層級安全防護機制保護資料，以及其他詳細資訊。

## 什麼是資料列層級安全性？

資料列層級安全防護機制可讓您篩選資料，並根據符合資格的使用者條件，存取資料表中的特定資料列。

BigQuery 支援專案、資料集和資料表層級的存取控管，以及透過政策標記提供的[資料欄層級安全防護](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)。資料列層級安全防護機制透過資料列層級存取權政策，對 BigQuery 資料表中的部分資料啟用精細的存取控管，進一步落實最低權限原則。

一個資料表可以有多個資料列層級存取權政策。資料列層級存取權政策[可與資料表上的](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#example_of_row-level_security_and_column-level_security_interacting) [資料欄層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)，以及
[資料集層級](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)、[資料表層級](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_table_or_view)和[專案層級](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)存取權控管機制並存。

## 資料列層級安全防護機制的運作方式

從較高的層級來看，資料列層級安全防護機制涉及在目標 BigQuery 資料表上建立資料列層級存取權政策。這些政策會做為篩選器，根據使用者或群組是否在允許清單中，隱藏或顯示特定資料列。如果使用者或群組未明確列入允許清單，系統會拒絕其存取要求。

**注意：** 如果您建立新的資料列層級安全性政策來限制資料列存取權，則必須將先前擁有完整存取權的使用者新增至[`TRUE`篩選器](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#the_true_filter)，才能維持存取權。

具備身分與存取權管理 (IAM) 角色 ([BigQuery 管理員或 BigQuery 資料擁有者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)) 的授權使用者，可以在 BigQuery 資料表上建立資料列層級存取權政策。

建立資料列層級存取政策時，請依名稱指定資料表，以及哪些使用者或群組 (稱為`grantee-list`) 可以存取特定資料列資料。這項政策也包含您要篩選的資料，稱為 `filter_expression`。`filter_expression` 函式的運作方式與一般查詢中的 `WHERE` 子句類似。

**注意：**與 `WHERE` 子句類似，`filter_expression` 會比對您想讓主體在 `grantee_list` 中看到的資料。不在 `grantee_list` 中的使用者無法看到任何資料列。

如需建立及使用資料列層級存取權政策的操作說明，請參閱「[管理資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」。

如需建立資料列層級存取權政策時的完整語法、用法和選項，請參閱 [DDL 參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_row_access_policy_statement)。

### 應用實例

以下範例說明列層級安全性的可能用途。

**注意：**
管理[外部身分識別資訊提供者](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)中使用者存取權時，請將 Google 帳戶主體 ID (例如 `user:kiran@example.com`、`group:support@example.com` 和 `domain:example.com`) 替換為適當的[員工身分聯盟主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。

#### 依據區域篩選資料列資料

假設表格 `dataset1.table1` 包含屬於不同區域的資料列 (以 `region` 欄表示)。

您可以使用下列查詢建立範例資料表並填入資料：

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

資料列層級安全防護機制可讓資料擁有者或管理員實施政策。以下陳述式會實施一項政策，限制亞太地區郵寄群組中的使用者只能查看亞太地區的合作夥伴：

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

如果使用者不屬於 `APAC` 或 `US` 群組，就不會看到任何資料列。

#### 根據敏感資料篩選資料列資料

現在來看看另一個用途，假設您有一個包含薪資資訊的資料表。

您可以使用下列查詢建立範例資料表並填入資料：

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

下列陳述式中的資料列存取權政策會限制查詢，僅限公司網域的成員。此外，使用 `SESSION_USER()` 函式時，系統會根據執行查詢的使用者電子郵件地址，限制只能存取該使用者所屬的資料列。

```
CREATE ROW ACCESS POLICY
  salary_personal
ON
  dataset1.table1 GRANT TO ("domain:example.com")
  FILTER USING
  (Email=SESSION_USER());
```

下圖顯示資料列存取權政策如何限制含有薪資資訊的資料表。在這個範例中，使用者名為 Jim，電子郵件地址為 `jim@example.com`。

如需更多資料列層級安全防護機制範例，請參閱「[使用資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」。

#### 根據對照表篩選資料列資料

有了子查詢支援功能，資料列存取政策就能參照其他資料表，並將這些資料表做為查閱資料表。篩選規則中使用的資料可以儲存在資料表中，而單一子查詢資料列存取政策可以取代多個已設定的資料列存取政策。如要更新資料列存取政策，只需要更新查閱表，即可取代多項資料列存取政策。您不需要更新每個資料列存取政策。

如需篩選資料列資料的範例，請參閱「[使用資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」。

## 資料列層級的安全性與其他方法的適用時機

[授權檢視區塊](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)、資料列層級存取權政策，以及將資料儲存在不同資料表中，都能提供不同層級的安全性、效能和便利性。請務必為您的用途選擇合適的機制，確保資料受到適當程度的保護。

### 與授權觀看次數的比較：漏洞

如果使用不當，資料列層級安全性和[使用授權檢視畫面強制執行資料列層級存取權](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw#combine_row-level_security_with_authorized_views)都可能出現安全漏洞。

*使用授權檢視畫面或資料列層級存取政策來確保資料列層級安全時，建議您使用[稽核記錄](#audit_logging_and_monitoring)監控任何可疑活動。*

側通道 (例如查詢時間長度) 可能會洩漏儲存空間分片邊緣的資料列資訊。這類攻擊可能需要瞭解資料表的分片方式，或是發出大量查詢。

如要進一步瞭解如何防範這類旁通道攻擊，請參閱「[資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw#limit-side-channel-attacks)」。

### 授權檢視表、資料列層級安全防護機制和獨立資料表比較

下表比較授權 view、資料列層級存取權政策和獨立資料表的彈性、效能和安全性。

| **方法** | **安全性考量** | **建議** |
| --- | --- | --- |
| **授權**  **檢視畫面** | 建議使用這個選項，享有較高的彈性。可能容易受到精心設計的查詢、查詢時間長度和其他類型的側通道攻擊。 | 需要與他人共用資料，且彈性和效能都很重要時，授權檢視畫面是不錯的選擇。舉例來說，您可以使用授權檢視畫面，在工作群組內共用資料。 |
| **資料列層級存取政策** | 建議使用，兼顧彈性和安全性。可能容易受到[查詢時間旁路攻擊](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw#limit-side-channel-attacks)。 | 如要與他人共用資料，並為檢視畫面或資料表切片提供額外安全防護，建議採用資料列層級存取權政策。舉例來說，您可以使用資料列層級存取權政策，與使用相同資訊主頁的人員共用資料，即使部分人員可存取的資料比其他人多也沒問題。 |
| **獨立表格** | 建議用於安全性用途。使用者必須有資料表存取權，才能推斷資料。 | 如果您需要與他人共用資料，且必須隔離資料，建議使用個別資料表。舉例來說，如果總列數必須保密，您可以透過個別表格與第三方合作夥伴和供應商分享資料。 |

## 建立及管理資料列層級存取政策

如要瞭解如何建立、更新 (重新建立)、列出、查看及刪除資料表的資料列層級存取權政策，以及如何查詢含有資料列層級存取權政策的資料表，請參閱「[使用資料列層級存取權安全性](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」。

## 隱含刪除資料列層級存取權政策

在幾種情況下，系統會從資料表隱含 (自動) 移除資料列存取政策。

自動刪除資料列存取政策的一般原則如下：

* 使用 [`WRITE_TRUNCATE` 寫入配置](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.write_disposition)的作業一律會覆寫目的地資料表上現有的任何資料列存取權政策。
* 如果作業的 `WRITE_APPEND` 寫入配置為「WRITE\_APPEND」，系統會保留目的地資料表目前的資料列存取權政策，並將來源資料表的政策新增至目的地資料表。

具體來說，在下列情況下，系統會隱含移除資料列存取權政策：

* 取代資料表：使用 [`CREATE OR REPLACE
  TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) DDL 陳述式取代資料表時，系統會捨棄原始資料表的所有現有資料列存取政策。即使替代查詢是以原始資料表的資料為依據，也會發生這種情況。
* 使用 `WRITE_TRUNCATE` 載入或查詢：使用 `WRITE_TRUNCATE` 寫入處置的操作會移除所有現有的資料列存取政策。包括使用 [`bq load
  --replace`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令載入資料，以及執行查詢並將 `writeDisposition` 狀態設為 `WRITE_TRUNCATE`。這類作業會完全覆寫資料表，且不會沿用資料列存取政策。
* 刪除或到期資料表：如果資料表遭到明確刪除，或是達到到期時間而自動移除，所有相關聯的資料列存取政策也會一併刪除。
* 資料表複製作業：將沒有資料列存取政策的資料表複製到有資料列存取政策的目的地資料表時，系統會移除目的地資料表的政策，除非使用 [`--append_table`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 旗標或 `"writeDisposition": "WRITE_APPEND"`。如要進一步瞭解資料表複製工作，請參閱[將資料列層級的安全性與其他 BigQuery 功能搭配使用](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#features_that_work_with_the_true_filter)。

使用 [`TRUNCATE
TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#truncate_table_statement) DML 陳述式 (可移除資料表中的所有資料列，同時保留結構定義) 不會移除資料列存取政策。

## 配額

如要進一步瞭解資料列層級安全性的配額和限制，請參閱 BigQuery 的「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#row-level_security)」。

## 定價

BigQuery 內建資料列層級安全防護機制，不需額外付費。不過，資料列層級存取權政策可能會透過下列方式影響查詢的執行費用：

* 如果資料列層級存取權政策包含參照其他資料表的子查詢，可能會產生額外費用。
* 資料列層級存取政策篩選器不會參與[分區和叢集資料表](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#partitioned_and_clustered_tables)的查詢修剪作業。這不代表在執行主要查詢時會讀取更多資料。不會利用資料列存取政策述詞進一步修剪。
* 使用資料列層級存取政策篩選器時，系統不會提早套用所有使用者篩選器。
  這可能會增加從資料表讀取的資料量，並讀取更多資料列，進而產生更多費用。

如要進一步瞭解 BigQuery 查詢的定價，請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」一文。

## 限制

如要瞭解資料列層級安全防護機制的限制，請參閱 BigQuery 的[資料列層級安全防護機制限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#row-level_security)。下列各節說明其他列層級安全性限制。

### 效能限制

* 使用含有資料列層級存取權政策的資料表時，部分 BigQuery 功能不會加速，例如 [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#bi-engine) 和[具體化檢視表](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#logical_materialized_and_authorized_views)。
* 資料列層級安全防護機制不會參與查詢[修剪](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#overview)，這是[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)的功能。詳情請參閱[分區和叢集資料表](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#partitioned_and_clustered_tables)。這項限制不會減緩主要查詢的執行速度。
* 查詢設有資料列層級安全防護機制的資料表時，效能可能會稍微降低。

如要進一步瞭解資料列層級安全防護機制與部分 BigQuery 功能和服務的互動方式，請參閱[將資料列層級的安全性與其他 BigQuery 功能搭配使用](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)。

### 其他限制

* 使用以特定 BigQuery 版本建立的預留項目時，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
* 資料列存取政策不支援舊版 SQL。查詢含有資料列層級存取權政策的資料表時，必須使用 GoogleSQL。系統會拒絕舊版 SQL 查詢，並顯示錯誤訊息。
* 您無法對 [JSON 欄](https://docs.cloud.google.com/bigquery/docs/json-data?hl=zh-tw)套用資料列層級的存取權政策。
* 不支援對含有資料列存取政策的 Wildcard 資料表執行查詢。
* 資料列存取政策無法套用至臨時資料表。
* 您無法將資料列層級存取權政策套用至參照其他資料表的資料表，而這些資料表具有資料列層級安全性。
* 部分 BigQuery 功能與資料列層級安全防護機制不相容。詳情請參閱「[使用資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)」。

  + 包含[子查詢](#filter_row_data_based_on_lookup_table)的資料列存取政策與 [BigQuery Storage Read API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 不相容。BigQuery Storage Read API 僅支援簡單的篩選條件述詞。
* 需要完整存取資料表資料的非查詢作業 (包括服務帳戶工作)，可以使用[`TRUE`篩選器](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#the_true_filter)搭配資料列層級安全性。例如[複製資料表](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#features_that_work_with_the_true_filter)、[Managed Service for Apache Spark 工作流程](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#tabledata-list)等。詳情請參閱「[使用資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)」。
* 您可以使用 DDL 陳述式或[資料列存取政策 API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw#rest-resource:-v2.rowaccesspolicies)，建立、取代或刪除資料列層級的存取政策。您也可以在 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)中，對資料列存取權政策 API 執行所有可用動作。您可以在Google Cloud 控制台列出及查看資料列層級存取權政策。
* [預覽或瀏覽資料表](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw#browse-table)與資料列層級安全防護機制不相容。
* [資料表取樣](https://docs.cloud.google.com/bigquery/docs/table-sampling?hl=zh-tw)與資料列層級安全防護機制不相容。
* 資料列層級存取權政策會對頂層子查詢的結果設下 100 MB 的限制。
  超過這個門檻時，查詢就會失敗。請注意，這項限制是依據政策套用，不會影響使用者查詢。
* 在資料列存取權政策中，無法使用類型為 `FLOAT`、`STRUCT`、`ARRAY`、`JSON` 或 `GEOGRAPHY` 的頂層 [`IN`子查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/subqueries?hl=zh-tw#in_subquery_concepts)。`search_value`
* 如果因刪除任何參照資料表而無法評估資料列層級存取政策述詞，查詢就會失敗。
* 子查詢資料列層級存取權政策僅支援 BigQuery 資料表、BigLake 外部資料表和 BigLake 受管理資料表。
* 只有在要捨棄或重新命名的資料欄不屬於任何資料列存取政策時，才能使用修改資料表結構定義的資料欄[重新命名](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw#change_a_columns_name)和[捨棄](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw#delete_a_column)陳述式。
* [資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)僅適用於具有非子查詢資料列存取政策的查詢。資料遮蓋功能會套用至列層級安全防護。舉例來說，如果 `location = "US"` 套用了資料列存取權政策，且 `location` 已遮蓋，使用者就能查看 `location = "US"` 的資料列，但結果中的位置資訊欄位會遭到遮蓋。如果查詢涉及子查詢資料列存取政策，則必須具備資料列存取政策所參照資料欄的「精細讀取者」存取權。

## 稽核記錄和監控

讀取含有至少一項資料列層級存取權政策的資料表時，系統會將授權讀取存取權的資料列層級存取權政策，以及子查詢中參照的任何對應資料表，顯示在該讀取要求的 IAM 授權資訊中。

系統會稽核記錄列層級存取權政策的建立和刪除作業，並透過 [Cloud Logging](https://docs.cloud.google.com/logging/docs/overview?hl=zh-tw) 提供存取權。稽核記錄會包含資料列層級存取權政策的名稱。不過，記錄檔會省略資料列層級存取政策的 `filter_expression` 和 `grantee_list` 定義，因為這些定義可能包含使用者或其他私密資訊。系統不會稽核記錄資料列層級存取政策的列出和查看作業。

如要進一步瞭解 BigQuery 中的記錄，請參閱「[BigQuery 監控簡介](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)」。

如要進一步瞭解記錄檔，請參閱 Google Cloud
[Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw)。

## 後續步驟

* 如要瞭解如何管理資料列層級安全防護機制，請參閱「[使用資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」。
* 如要瞭解資料列層級安全防護機制如何與其他 BigQuery 功能和服務搭配運作，請參閱[將資料列層級的安全性與其他 BigQuery 功能搭配使用](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)。
* 如要瞭解資料列層級安全性的最佳做法，請參閱 [BigQuery 資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]