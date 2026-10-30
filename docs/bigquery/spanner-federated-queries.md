Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Spanner 聯合查詢

BigQuery 的[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)功能可讓您即時查詢 Spanner 中的資料，不必複製或移動資料。您可以建立 Spanner 外部資料集，或使用 [`EXTERNAL_QUERY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query) 函式，查詢 Spanner 資料。

## 瞭解角色和權限

從 BigQuery 查詢 Spanner 時，會遇到兩種不同類型的角色，分別在不同層級管理存取權。

* **IAM 角色：**這些角色控管Google Cloud 資源的存取權，包括 Spanner 執行個體和資料庫。這些角色決定哪些主體可以存取 Spanner 服務，並在執行個體或資料庫層級執行動作，例如連線、讀取資料或管理。您可以透過 IAM 控制台或 Google Cloud CLI 管理 Identity and Access Management (IAM) 角色。例如 `roles/bigquery.connectionUser` 和 `roles/spanner.databaseReader`。詳情請參閱「[Spanner IAM 角色](https://docs.cloud.google.com/spanner/docs/iam?hl=zh-tw)」和「[授予權限](https://docs.cloud.google.com/spanner/docs/grant-permissions?hl=zh-tw)」。
* **Spanner 資料庫角色：**這些角色是在 Spanner 資料庫中使用 DDL 陳述式定義，例如 [`CREATE ROLE`](https://docs.cloud.google.com/spanner/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_role) 和 [`GRANT`](https://docs.cloud.google.com/spanner/docs/reference/standard-sql/data-definition-language?hl=zh-tw#grant_statement)。這些角色可精細控管資料庫中特定結構定義物件 (例如資料表、資料欄和檢視表) 的存取權。這是[精細存取控管](https://docs.cloud.google.com/spanner/docs/fgac-about?hl=zh-tw) (FGAC) 的一部分。如果貴組織實施 FGAC 來管理資料庫內的權限，請使用資料庫角色。

### 判斷您是否為 FGAC 使用者

如要判斷應要求哪些權限，請先確認您是否為 FGAC 使用者。請詢問 Spanner 資料庫管理員，您對 Spanner 資料庫的存取權是否透過精細的存取控管機制管理。

如果管理員將您的帳戶指派給特定 Spanner 資料庫角色 (例如在資料庫角色資源上，授予帳戶 `roles/spanner.databaseRoleUser` 這個 IAM 角色)，藉此授予權限，則您可能是 FGAC 使用者。如果是這種情況，您必須知道可使用的資料庫角色名稱。您必須設定 BigQuery 連線，才能使用其中一個資料庫角色。

如果管理員為您的帳戶授予更廣泛的資料庫層級 IAM 角色 (例如 `roles/spanner.databaseReader`)，您可能就不是 FGAC 使用者。在這種情況下，連線時不需要使用特定資料庫角色。

### 比較角色應用

雖然 IAM 控制資料庫資源本身的存取權，但 Spanner 資料庫角色會控制該資料庫內物件的權限。

如要使用 FGAC 資料庫角色，通常需要下列權限：

* `spanner.databases.useRoleBasedAccess` IAM 權限，通常透過 `roles/spanner.fineGrainedAccessUser` 角色授予。
* 使用特定資料庫角色的權限，透過 `roles/spanner.databaseRoleUser` 角色和 IAM 條件授予。

如要進一步瞭解如何設定這些權限，請參閱「[設定 FGAC](https://docs.cloud.google.com/spanner/docs/configure-fgac?hl=zh-tw)」。

## 使用外部資料集

如要查詢 Spanner 資料表，最簡單的方法是[建立外部資料集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)。建立外部資料集後，相應 Spanner 資料庫中的資料表就會顯示在 BigQuery 中，您可以在查詢中使用這些資料表，例如在 join、union 或子查詢中。不過，資料不會從 Spanner 移至 BigQuery 儲存空間。

建立外部資料集後，就不必建立連線來查詢 Spanner 資料。

## 使用 `EXTERNAL_QUERY` 函式

與其他聯合資料庫一樣，您也可以使用 [`EXTERNAL_QUERY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query) 函式查詢 Spanner 資料。如要進一步控管連線參數，這個方法可能很實用。

### 事前準備

* 確認 BigQuery 管理員已建立 [Spanner 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spanner?hl=zh-tw#create-spanner-connection)，並與您[共用](https://docs.cloud.google.com/bigquery/docs/connect-to-spanner?hl=zh-tw#share_connections)。請參閱「[選擇合適的連線](#right-connection)」。
* 如要取得查詢 Spanner 執行個體所需的權限，請要求管理員授予您連線的 BigQuery 連線使用者 (`roles/bigquery.connectionUser`) IAM 角色。您也必須具備 Spanner 資料庫的適當權限，具體取決於[您是否為 FGAC 使用者](#determine-fgac-user)。
  + 如果您是精細存取控管使用者：
    - 您必須具備使用 FGAC 所需的 IAM 角色。這些角色通常是 `roles/spanner.fineGrainedAccessUser` 和 `roles/spanner.databaseRoleUser`。這些角色會與指定資料庫角色的條件搭配使用。
    - 您在連線中指定的 Spanner 資料庫角色，必須具備查詢參照的所有結構定義物件的 `SELECT` 權限。資料庫管理員會使用 [`GRANT`](https://docs.cloud.google.com/spanner/docs/reference/standard-sql/data-definition-language?hl=zh-tw#grant_statement) DDL 陳述式 (或[對等的 PostgreSQL 陳述式](https://docs.cloud.google.com/spanner/docs/reference/postgresql/data-definition-language?hl=zh-tw#grant_statement)) 授予權限。
  + 如果您不是精細的存取控管使用者，則必須具備資料庫的 Spanner 資料庫讀取者 (`roles/spanner.databaseReader`) IAM 角色。

  如要瞭解如何授予 IAM 角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

### 選擇合適的連線

如果您是 Spanner 精細存取控管使用者，使用 [`EXTERNAL_QUERY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query) 函式執行聯合查詢時，必須使用指定資料庫角色的 Spanner 連線。這個資料庫角色是 Spanner 資料庫中 FGAC 設定的一部分，與 IAM 角色分開。之後，您透過這個連線執行的所有查詢，都會使用授予該資料庫角色的權限。

如果使用的連線未指定資料庫角色，您必須具備「[事前準備](#begin)」中指出的 IAM 角色。

### 查詢資料

如要透過 GoogleSQL 查詢將聯合查詢傳送至 Spanner，請使用 [`EXTERNAL_QUERY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query) 函式。

根據資料庫指定的方言，使用 GoogleSQL 或 PostgreSQL 制定 Spanner 查詢。

下列範例會對名為 `orders` 的 Spanner 資料庫執行聯合查詢，並將結果與名為 `mydataset.customers` 的 BigQuery 資料表彙整：

```
SELECT c.customer_id, c.name, rq.first_order_date
FROM mydataset.customers AS c
LEFT OUTER JOIN EXTERNAL_QUERY(
  'my-project.us.example-db',
  '''SELECT customer_id, MIN(order_date) AS first_order_date
  FROM orders
  GROUP BY customer_id''') AS rq
  ON rq.customer_id = c.customer_id
GROUP BY c.customer_id, c.name, rq.first_order_date;
```

## Spanner Data Boost

Data Boost 是全代管的無伺服器功能，可為支援的 Spanner 工作負載提供獨立運算資源。Data Boost 可讓您執行分析查詢和資料匯出作業，同時盡可能減少對已佈建 Spanner 執行個體上現有工作負載的影響。Data Boost 可讓您使用獨立的運算資源執行聯合查詢，與佈建的執行個體分開，避免影響 Spanner 上的現有工作負載。Data Boost 最適合用於執行複雜的臨時查詢，或在不影響現有 Spanner 工作負載的情況下處理大量資料。使用 Data Boost 執行聯合查詢，可大幅降低 CPU 消耗量，在某些情況下還能縮短查詢延遲時間。

### 事前準備

如要取得啟用 Data Boost 存取權所需的權限，請要求管理員授予您 Spanner 資料庫的 [Cloud Spanner 資料庫讀取者 (使用 Data Boost)](https://docs.cloud.google.com/iam/docs/roles-permissions/spanner?hl=zh-tw#spanner.databaseReaderWithDataBoost)  (`roles/spanner.databaseReaderWithDataBoost`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `spanner.databases.useDataBoost` 權限，可啟用 Data Boost 存取權。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

`roles/spanner.databaseReaderWithDataBoost` IAM 角色可授予 Data Boost 使用權限。除了讀取資料所需的基本權限 (例如非 FGAC 使用者的 `roles/spanner.databaseReader`，或適當的精細存取控管權限) 之外，還必須具備這個角色。

搭配 Spanner 使用外部資料集時，一律會使用 Data Boost，因此需要 `spanner.databases.useDataBoost` 權限。

### 啟用 Data Boost

使用外部資料集時，系統一律會使用 Data Boost，您不必手動啟用。

如要對 `EXTERNAL_QUERY` 查詢使用 Data Boost，請在[建立查詢使用的連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spanner?hl=zh-tw)時啟用這項功能。

## 並行讀取資料

Spanner 可將特定查詢分成較小的部分或分區，並平行擷取分區。如需更多資訊 (包括限制清單)，請參閱 Spanner 說明文件中的「[平行讀取資料](https://docs.cloud.google.com/spanner/docs/reads?hl=zh-tw#read_data_in_parallel)」。

如要查看 Spanner 查詢的查詢執行計畫，請參閱「[瞭解 Spanner 如何執行查詢](https://docs.cloud.google.com/spanner/docs/sql-best-practices?hl=zh-tw#how-execute-queries)」。

對外部資料集執行聯合查詢時，一律會使用「平行讀取資料」選項。

如要在使用 [`EXTERNAL_QUERY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query) 時啟用平行讀取功能，請在[建立連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spanner?hl=zh-tw)時啟用。

## 管理查詢執行優先順序

使用 `EXTERNAL_QUERY` 函式執行聯合查詢時，您可以指定 `query_execution_priority` 選項，為個別查詢指派優先順序 (`high`、`medium` 或 `low`)：

```
SELECT *
FROM EXTERNAL_QUERY(
  'my-project.us.example-db',
  '''SELECT customer_id, MIN(order_date) AS first_order_date
  FROM orders
  GROUP BY customer_id''',
  '{"query_execution_priority":"high"}');
```

預設優先順序為 `medium`。

優先順序為 `high` 的查詢會與交易流量競爭。優先順序為 `low` 的查詢會盡可能執行，但可能會遭到背景負載 (例如排定的備份) 優先處理。

**注意：** 優先順序為 `low` 的查詢，順位會低於可能無法在 BigQuery 逾時前完成的查詢 (例如備份工作)。

使用外部資料集執行聯合查詢時，所有查詢的優先順序一律為 `medium`。

## 查看 Spanner 資料表結構定義

如果使用外部資料集，Spanner 資料表會直接顯示在 BigQuery Studio 中，您也可以查看其結構定義。

不過，您也可以在不定義外部資料集的情況下查看結構定義。您也可以使用 `EXTERNAL_QUERY` 函式查詢 `information_schema` 檢視表，存取資料庫中繼資料。以下範例會傳回 `MyTable` 資料表中的資料欄資訊：

### Google SQL 資料庫

```
SELECT *
FROM EXTERNAL_QUERY(
  'my-project.us.example-db',
  '''SELECT t.column_name, t.spanner_type, t.is_nullable
    FROM information_schema.columns AS t
    WHERE
      t.table_catalog = ''
      AND t.table_schema = ''
     AND t.table_name = 'MyTable'
    ORDER BY t.ordinal_position
  ''');
```

### PostgreSQL 資料庫

```
SELECT * from EXTERNAL_QUERY(
'my-project.us.postgresql-example-db',
'''SELECT t.column_name, t.data_type, t.is_nullable
   FROM information_schema.columns AS t
   WHERE t.table_schema = 'public' AND t.table_name = 'MyTable'
   ORDER BY t.ordinal_position''');
```

詳情請參閱 Spanner 說明文件中的下列資訊結構定義參考資料：

* [GoogleSQL 資訊架構](https://docs.cloud.google.com/spanner/docs/information-schema?hl=zh-tw)
* [PostgreSQL 資訊結構定義](https://docs.cloud.google.com/spanner/docs/information-schema-pg?hl=zh-tw)

## 定價

* BigQuery 方面則適用標準[聯合查詢定價](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#pricing)。
* 在 Spanner 端，查詢須遵守 [Spanner 定價](https://cloud.google.com/spanner/pricing?hl=zh-tw)。

## 跨區域查詢

BigQuery 支援聯合查詢，其中 Spanner 執行個體和 BigQuery 資料集位於不同區域。這類查詢會產生額外的 Spanner 資料移轉費用。詳情請參閱「[Spanner 定價](https://cloud.google.com/spanner/pricing?hl=zh-tw#network)」。

系統會根據下列 [SKU](https://cloud.google.com/skus/sku-groups/cloud-spanner?hl=zh-tw) 向您收取資料移轉費用：

* 網路區域內跨可用區資料轉出
* 網路跨區域資料轉出至同一洲
* 網路跨區域資料轉出至不同洲

資料移轉費用取決於您執行查詢的 BigQuery 區域，以及具有讀寫或唯讀副本的最鄰近 Spanner 區域。

如果是 BigQuery 多區域設定 (`US` 或 `EU`)，從 Spanner 移轉資料的費用計算方式如下：

* BigQuery `US` 多區域：Spanner 區域 `us-central1`
* BigQuery `EU` 多區域：Spanner 區域 `europe-west1`

例如：

* BigQuery (`US` 多區域) 和 Spanner (`us-central1`)：在相同區域內移轉資料會產生費用。
* BigQuery (`US` 多區域) 和 Spanner (`us-west4`)：
  在同一洲的不同區域之間移轉資料時，會產生費用。

## 疑難排解

本節說明如何排解將聯合查詢傳送至 Spanner 時可能遇到的問題。

問題：查詢無法進行根分區。
:   **解決方法：**如果將連線設為平行讀取資料，查詢執行計畫中的第一個運算子必須是分散式聯集，或者執行計畫不得有任何分散式聯集。如要解決這個錯誤，請查看查詢執行計畫並重寫查詢。詳情請參閱「[瞭解 Spanner 如何執行查詢](https://docs.cloud.google.com/spanner/docs/sql-best-practices?hl=zh-tw#how-execute-queries)」。

問題：已超過期限。
:   **解決方法：**選取[平行讀取資料](#read_data_in_parallel)選項，並重寫查詢，使其可根分區。詳情請參閱「[瞭解 Spanner 如何執行查詢](https://docs.cloud.google.com/spanner/docs/sql-best-practices?hl=zh-tw#how-execute-queries)」。

## 後續步驟

* 瞭解如何[建立 Spanner 外部資料集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)
* 瞭解[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)。
* 瞭解 [Spanner 到 BigQuery 的資料類型對應](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#spanner-mapping)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]