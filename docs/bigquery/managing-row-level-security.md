* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用資料列層級安全防護機制

本文說明如何在 BigQuery 中使用資料列層級安全防護機制，限制存取資料表資料列層級的資料。閱讀本文前，請先詳閱「[BigQuery 資料列層級安全防護機制簡介](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)」，瞭解資料列層級安全防護機制總覽。

您可以使用資料列層級存取政策執行下列工作：

* 在資料表上[建立或更新資料列層級存取政策](#create-policy)
* 在資料表上[合併資料列層級存取權政策](#combine_row-level_access_policies)
* [列出資料表的資料列層級存取權政策](#list-policy)
* 從資料表[刪除資料列層級存取權政策](#delete-policy)
* [查詢具有資料列層級存取權政策的資料表](#query-policy)

**注意：**
管理[外部身分識別提供者](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)中使用者存取權時，請將 Google 帳戶主體 ID (例如 `user:kiran@example.com`、`group:support@example.com` 和 `domain:example.com`) 的例項，替換為適當的[員工身分聯盟主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。

## 限制

在 Google Cloud 控制台中選取資料表時，「預覽」分頁無法顯示設有資料列存取權政策的資料表預覽畫面。如要查看資料表的內容，請執行查詢。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。如要執行工作，必須具備的權限 (如有) 會列在工作的「必要權限」部分。

## 建立或更新資料列層級存取政策

您可以使用資料定義語言 (DDL) 陳述式，在 BigQuery 中建立或更新資料表的資料列層級存取權政策。

### 所需權限

如要在 BigQuery 資料表上建立資料列層級存取權政策，您需要下列 IAM 權限：

* `bigquery.rowAccessPolicies.create`
* `bigquery.rowAccessPolicies.setIamPolicy`
* `bigquery.tables.getData` (在目標資料表和已授權子查詢資料列層級存取政策中參照的任何資料表上)
* `bigquery.jobs.create` (執行 DDL 查詢工作)

如要更新 BigQuery 資料表的資料列層級存取權政策，您需要下列 IAM 權限：

* `bigquery.rowAccessPolicies.update`
* `bigquery.rowAccessPolicies.setIamPolicy`
* `bigquery.tables.getData` (在目標資料表和已授權子查詢資料列層級存取政策中參照的任何資料表上)
* `bigquery.jobs.create` (執行 DDL 查詢工作)

下列每個預先定義的 IAM 角色都包含建立及更新資料列層級存取權政策所需的權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataOwner`

#### `bigquery.filteredDataViewer` 角色

建立資料列層級存取權政策時，BigQuery 會自動將 `bigquery.filteredDataViewer` 角色授予受授予者清單的成員。在 Google Cloud 控制台中[列出資料表的資料列層級存取權政策](#list-policy)時，這個角色會與政策受授予者清單的成員相關聯。

**注意：** 請勿透過 IAM 將 `bigquery.filteredDataViewer` 角色直接套用至資源。`bigquery.filteredDataViewer` 是系統管理的角色。只能使用資料列層級存取政策授予角色。詳情請參閱[資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw#filtered-data-viewer)。

### 建立或更新資料列層級存取政策

在資料表上設定資料列層級存取權時，您至少需要兩項資料列存取權政策：

* 可授予資料表完整存取權的政策。第一項資料列存取權政策應授予使用者和群組存取權，讓他們能完整存取資料表中的資料，以進行資料維護或支援。舉例來說，BigQuery 管理員和使用 DML 陳述式轉換資料表資料的服務帳戶。
* 第二項政策，用於篩選存取權。這項政策會根據商業邏輯使用篩選器，授予特定群組存取權。

如要建立或更新資料列層級存取政策，請使用下列其中一個 DDL 陳述式：

* `CREATE ROW ACCESS POLICY` 會建立新的資料列層級存取政策。
* 如果指定資料表上沒有同名的資料列層級存取政策，`CREATE ROW ACCESS POLICY IF NOT EXISTS` 陳述式就會建立新的資料列層級存取政策。
* `CREATE OR REPLACE ROW ACCESS POLICY` 陳述式會更新指定資料表中同名的現有資料列層級存取政策。

  **重點回顧：**
  + 資料表中的每個資料列層級存取政策都必須有不重複的名稱。
  + 與 `WHERE` 子句類似，`filter_expression`
    會比對您要向 `grantee_list` 成員顯示的資料。
  + 如果使用者和群組以半形逗號分隔，且分別加上引號，您可以在`grantee_list`清單中合併一系列使用者和群組。
  + `grantee_list` 中的所有身分都必須存在。如果任何身分識別不存在，系統就不會建立政策，陳述式也會失敗。
  + 您無法對 [JSON 欄](https://docs.cloud.google.com/bigquery/docs/json-data?hl=zh-tw)套用資料列層級存取權政策。如要瞭解資料列層級安全防護機制的其他限制，請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw#limitations)」一節。

### 範例

下列範例說明如何為不同類型的[主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw#allow) (包括 Google 帳戶和聯合身分) 建立及更新資料列存取政策。如要進一步瞭解聯合身分，請參閱「[Workload Identity 聯盟](https://docs.cloud.google.com/iam/docs/workload-identity-federation?hl=zh-tw)」。

#### 建立新政策並授予 Google 帳戶存取權

建立新的資料列存取政策。只有使用者 `abc@example.com` 才能存取資料表。只會顯示 `region = 'APAC'` 的資料列：

```
CREATE ROW ACCESS POLICY apac_filter
ON project.dataset.my_table
GRANT TO ('user:abc@example.com')
FILTER USING (region = 'APAC');
```

#### 建立新政策，並授予員工身分集區中單一身分的存取權

建立新的資料列存取政策。只有工作團隊身分集區中的單一身分可以存取資料表，格式如下：
`principal://iam.googleapis.com/locations/global/workforcePools/POOL_ID/subject/IDENTITY`。
只會顯示 `region = 'APAC'` 的資料列：

```
CREATE ROW ACCESS POLICY apac_filter
ON project.dataset.my_table
GRANT TO ('principal://iam.googleapis.com/locations/global/workforcePools/example-contractors/subject/abc@example.com')
FILTER USING (region = 'APAC');
```

#### 更新政策，授予服務帳戶存取權

更新 `apac_filter` 存取權政策，套用至服務帳戶 `example@exampleproject.iam.gserviceaccount.com`：

```
CREATE OR REPLACE ROW ACCESS POLICY apac_filter
ON project.dataset.my_table
GRANT TO ('serviceAccount:example@exampleproject.iam.gserviceaccount.com')
FILTER USING (region = 'APAC');
```

#### 建立政策並授予使用者和群組存取權

建立資料列存取政策，授予使用者和兩個群組存取權：

```
CREATE ROW ACCESS POLICY sales_us_filter
ON project.dataset.my_table
GRANT TO ('user:john@example.com',
          'group:sales-us@example.com',
          'group:sales-managers@example.com')
FILTER USING (region = 'US');
```

#### 建立政策，並授予群組中員工身分的存取權

建立資料列存取政策，使用以下格式授權群組中的所有員工身分存取資料：`principal://iam.googleapis.com/locations/global/workforcePools/POOL_ID/subject/IDENTITY`

```
CREATE ROW ACCESS POLICY sales_us_filter
ON project.dataset.my_table
GRANT TO ('principal://iam.googleapis.com/locations/global/workforcePools/example-contractors/subject/sales-us@example.com',
          'principal://iam.googleapis.com/locations/global/workforcePools/example-contractors/subject/sales-managers@example.com')
FILTER USING (region = 'US');
```

#### 建立政策並授予所有通過驗證的使用者存取權

以 `allAuthenticatedUsers` 做為受授予者，建立資料列存取政策：

```
CREATE ROW ACCESS POLICY us_filter
ON project.dataset.my_table
GRANT TO ('allAuthenticatedUsers')
FILTER USING (region = 'US');
```

#### 根據目前使用者建立政策和篩選器

根據目前使用者建立資料列存取政策並套用篩選器：

```
CREATE ROW ACCESS POLICY my_row_filter
ON dataset.my_table
GRANT TO ('domain:example.com')
FILTER USING (email = SESSION_USER());
```

#### 建立政策並依資料欄篩選

建立資料列存取政策，並對 `ARRAY` 類型的資料欄套用篩選器：

```
CREATE ROW ACCESS POLICY my_reports_filter
ON project.dataset.my_table
GRANT TO ('domain:example.com')
FILTER USING (SESSION_USER() IN UNNEST(reporting_chain));
```

#### 建立政策並使用區域比較功能

建立含有子查詢的資料列存取政策，以取代多項政策，並為每位使用者設定區域比較：

請看下表，`lookup_table`：

```
+-----------------+--------------+
|      email      |    region    |
+-----------------+--------------+
| xyz@example.com | europe-west1 |
| abc@example.com | us-west1     |
| abc@example.com | us-west2     |
+-----------------+--------------+
```

```
CREATE OR REPLACE ROW ACCESS POLICY apac_filter
ON project.dataset.my_table
GRANT TO ('domain:example.com')
FILTER USING (region IN (
    SELECT
      region
    FROM
      lookup_table
    WHERE
      email = SESSION_USER()));
```

在 `lookup_table` 上使用子查詢，可避免建立多個資料列存取政策。舉例來說，上述陳述式產生的結果與下列陳述式相同，但查詢次數較少：

```
CREATE OR REPLACE ROW ACCESS POLICY us_filter
ON project.dataset.my_table
GRANT TO ('user:abc@example.com')
FILTER USING (region IN ('us-west1', 'us-west2'));

CREATE OR REPLACE ROW ACCESS POLICY eu_filter
ON project.dataset.my_table
GRANT TO ('user:xyz@example.com')
FILTER USING (region = 'europe-west1');
```

如要進一步瞭解語法和可用選項，請參閱 [`CREATE ROW ACCESS POLICY` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_row_access_policy_statement)參考資料。

## 合併資料列層級存取權政策

如果使用者或群組透過兩項以上的資料列層級存取政策取得相同資料表的存取權，則使用者或群組可存取任何政策涵蓋的所有資料。舉例來說，下列政策會授予使用者 `abc@example.com` 存取 `my_table` 資料表中指定資料列的權限：

```
CREATE ROW ACCESS POLICY shoes
ON project.dataset.my_table
GRANT TO ('user:abc@example.com')
FILTER USING (product_category = 'shoes');
```

```
CREATE OR REPLACE ROW ACCESS POLICY blue_products
ON project.dataset.my_table
GRANT TO ('user:abc@example.com')
FILTER USING (color = 'blue');
```

在上述範例中，使用者 `abc@example.com` 可以存取 `my_table` 資料表中 `product_category` 欄位設為 `shoes` 的資料列，也可以存取 `color` 欄位設為 `blue` 的資料列。`abc@example.com`舉例來說，`abc@example.com` 可以存取包含紅鞋和藍車資訊的資料列。

這項存取權等同於下列單一資料列層級存取政策提供的存取權：

```
CREATE ROW ACCESS POLICY shoes_and_blue_products
ON project.dataset.my_table
GRANT TO ('user:abc@example.com')
FILTER USING (product_category = 'shoes' OR color = 'blue');
```

另一方面，如要指定存取權，但必須符合多個條件，請使用含有 `AND` 運算子的篩選器。舉例來說，下列資料列層級存取權政策只會授予 `abc@example.com` 存取權給 `product_category` 欄位設為 `shoes` 且 `color` 欄位設為 `blue` 的資料列：

```
CREATE ROW ACCESS POLICY blue_shoes
ON project.dataset.my_table
GRANT TO ('user:abc@example.com')
FILTER USING (product_category = 'shoes' AND color = 'blue');
```

根據上述資料列層級存取政策，`abc@example.com` 可以存取藍色鞋子的資訊，但無法存取紅色鞋子或藍色汽車的資訊。

## 列出資料表資料列層級存取權政策

您可以使用 Google Cloud 控制台、bq 指令列工具或 `RowAccessPolicies.List` API 方法，列出及查看資料表的所有資料列層級存取權政策。

### 所需權限

如要列出 BigQuery 資料表的資料列層級存取權政策，您需要 `bigquery.rowAccessPolicies.list` IAM 權限。

如要查看 BigQuery 資料表資料列層級存取政策的成員，您需要 `bigquery.rowAccessPolicies.getIamPolicy` IAM 權限。

下列預先定義的 IAM 角色都包含列出及查看資料列層級存取權政策所需的權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataOwner`

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

### 列出資料表資料列層級存取權政策

如要列出資料列層級存取政策，請按照下列步驟操作：

### 控制台

1. 如要查看資料列層級存取權政策，請前往 Google Cloud 控制台的 BigQuery 頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下資料表名稱即可查看詳細資料，然後點選「查看資料列存取權政策」。
3. 「資料列存取權政策」面板開啟後，您會看到資料表中所有資料列層級存取權政策的清單 (依名稱排序)，以及每項政策的 `filter_expression`。
4. 如要查看受資料列層級存取權政策影響的所有角色和使用者，請按一下政策旁的「查看」。舉例來說，在下圖中，您可以在「查看權限」面板中看到，受讓人清單的成員具有「[`bigquery.filteredDataViewer`」角色](#filtered-data-viewer-role)。

   **重要事項：** 新增及移除政策成員時，只能使用 DDL 陳述式。

### bq

輸入 `bq ls` 指令並加上 `--row_access_policies` 旗標。
必須提供資料集和資料表名稱。

```
    bq ls --row_access_policies dataset.table
```

舉例來說，下列指令會列出 ID 為 `my_dataset` 的資料集中，名為 `my_table` 的資料表所套用的資料列層級存取權政策資訊：

```
    bq ls --row_access_policies my_dataset.my_table
```

### API

使用 REST API 參考資料章節中的 [`RowAccessPolicies.List` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/rowAccessPolicies/list?hl=zh-tw)。

## 刪除資料列層級存取政策

如果您有權限，可以使用 DDL 陳述式刪除資料表上的一或多項資料列層級存取政策。

### 所需權限

如要捨棄資料列層級存取權政策，您需要下列 IAM 權限：

* `bigquery.rowAccessPolicies.delete`
* `bigquery.rowAccessPolicies.setIamPolicy`
* `bigquery.jobs.create` (執行 DDL 查詢工作)

如要同時捨棄資料表中的所有資料列層級存取權政策，您需要下列 IAM 權限：

* `bigquery.rowAccessPolicies.delete`
* `bigquery.rowAccessPolicies.setIamPolicy`
* `bigquery.rowAccessPolicies.list`
* `bigquery.jobs.create` (執行 DDL 查詢工作)

下列預先定義的 IAM 角色都包含刪除資料列層級存取權政策所需的權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataOwner`

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

### 刪除資料列層級存取政策

如要從資料表刪除資料列存取權政策，請使用下列 DDL 陳述式：

* `DROP ROW ACCESS POLICY` 陳述式會刪除指定資料表的資料列層級存取權政策。
* 如果指定資料表有資料列存取政策，`DROP ROW ACCESS POLICY IF EXISTS` 陳述式就會刪除資料列層級的存取政策。
* `DROP ALL ROW ACCESS POLICIES` 陳述式會刪除指定資料表的所有資料列層級存取政策。

**重要事項：** 您無法使用 `DROP ROW ACCESS POLICY` 從資料表中刪除最後一項資料列層級存取權政策。嘗試停用會導致錯誤。如要刪除資料表的最後一項資料列層級存取權政策，請改用 `DROP ALL ROW
ACCESS POLICIES`。如要進一步瞭解如何捨棄資料表的最後一項資料列層級存取權政策，請參閱「[資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw#avoid_inadvertent_access_when_re-creating_row-level_access_policies)」。

### 範例

從資料表刪除資料列層級存取權政策：

```
DROP ROW ACCESS POLICY my_row_filter ON project.dataset.my_table;
```

從資料表刪除所有資料列層級存取權政策：

```
DROP ALL ROW ACCESS POLICIES ON project.dataset.my_table;
```

如要進一步瞭解如何刪除資料列層級存取政策，請參閱 [`DROP ROW ACCESS POLICY` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_row_access_policy_statement)參考資料。

## 查詢設有資料列存取政策的資料表

使用者必須先取得 BigQuery 資料表的存取權，才能查詢該資料表，即使他們位於該資料表的資料列存取政策的 `grantee_list` 中也一樣。如果沒有這項權限，查詢就會失敗並顯示 `access
denied` 錯誤。

### 所需權限

如要使用資料列層級存取權政策查詢 BigQuery 資料表，您必須具備該資料表的 `bigquery.tables.getData` 權限。您也需要 `bigquery.rowAccessPolicies.getFilteredData` 權限。

如要透過預先定義的角色取得這些權限，您必須使用 IAM 取得資料表的 [`roles/bigquery.dataViewer`](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer) 角色，並透過資料列層級存取權政策取得資料表的 [`roles/bigquery.filteredDataViewer`](#filtered-data-viewer-role) IAM 角色。

**注意：** 請勿透過 IAM 將 `bigquery.filteredDataViewer` 角色直接套用至資源。`bigquery.filteredDataViewer` 是系統管理的角色。只能使用資料列層級存取政策授予角色。詳情請參閱[資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw#filtered-data-viewer)。

您必須具備所有相關資料欄的 `datacatalog.categories.fineGrainedGet` 權限，才能使用[資料欄層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)。如要透過預先定義的角色取得這項權限，您需要 `datacatalog.categoryFineGrainedReader` 角色。

### 查看查詢結果

在 Google Cloud 控制台中，當您查詢具有資料列層級存取政策的資料表時，BigQuery 會顯示橫幅通知，指出您的結果可能會依資料列層級存取政策篩選。即使您是政策的受讓人清單成員，系統仍會顯示這則通知。

### 工作統計資料

使用 Job API 查詢含有資料列層級存取政策的資料表時，BigQuery 會在 `Job` 回應物件中指出查詢是否讀取任何含有資料列存取政策的資料表：

#### 範例

為求簡單起見，這個 `Job` 物件回應已遭截斷：

```
{
  "configuration": {
    "jobType": "QUERY",
    "query": {
      "priority": "INTERACTIVE",
      "query": "SELECT * FROM dataset.table",
      "useLegacySql": false
    }
  },
  ...
  "statistics": {
    ...
    rowLevelSecurityStatistics: {
      rowLevelSecurityApplied: true
    },
    ...
  },
  "status": {
    "state": "DONE"
  },
  ...
}
```

## 後續步驟

* 如要瞭解資料列層級安全防護機制如何與其他 BigQuery 功能和服務搭配運作，請參閱[將資料列層級的安全性與其他 BigQuery 功能搭配使用](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw)。
* 如要瞭解資料列層級安全性的最佳做法，請參閱 [BigQuery 資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]