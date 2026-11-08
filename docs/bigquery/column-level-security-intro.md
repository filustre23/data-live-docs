Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料欄層級存取控管機制簡介

**注意：**如果預留項目是以特定 BigQuery 版本建立，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

BigQuery 透過*政策標記* (以 Data Catalog 為基礎) 或*資料治理標記* (以 Resource Manager 標記為基礎)，對機密資料欄提供精細的存取權限。您可以使用這些分類方法建立政策，在執行查詢時檢查使用者是否具備適當存取權。例如，政策可以強制執行存取權檢查，例如：

* 您必須位於`group:high-access`，才能查看包含`TYPE_SSN`的資料欄。

如要強化資料欄層級存取控管，您可以選擇使用[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。資料遮蓋功能可讓您遮蓋機密資料，方法是以空值、預設值或雜湊內容取代資料欄的實際值。

本文說明如何使用政策標記，控管資料欄層級的存取權。或者，您也可以使用[資料治理標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw#data-governance-tags)，這是用於資料欄層級存取控管和資料遮蓋的 Resource Manager 標記。

**注意：**您必須保持啟用 `datacatalog.googleapis.com` API，才能建立及管理用於資料遮蓋和資料欄層級安全性的 Data Catalog 政策標記和分類。雖然 Data Catalog 中繼資料搜尋和目錄功能已淘汰，並轉換至 Knowledge Catalog，但 Policy Tag Manager 服務 (分類和政策標記)、其 `datacatalog.googleapis.com` API 方法和稽核記錄，以及 `roles/datacatalog` Identity and Access Management (IAM) 角色並未淘汰。

## 資料欄層級存取控管工作流程

如要限制資料欄層級的資料存取權，請按照下列步驟操作：

1. **定義分類和政策標記**。建立及管理資料的分類和政策標記。如需相關指南，請參閱「[政策標記最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)」。
2. **將政策標記指派給 BigQuery 資料欄**。在 BigQuery 中，使用結構定義註解，為要限制存取權的每個資料欄指派政策標記。
3. **對分類強制執行存取控管**。強制執行存取控管後，系統會套用分類中所有政策標記定義的存取限制。
4. **管理政策標記的存取權**。使用 [IAM](https://docs.cloud.google.com/iam?hl=zh-tw) 政策限制各項政策標記的存取權。政策會對屬於政策標記的每個資料欄生效。

當使用者嘗試在查詢時存取資料欄資料，BigQuery 會檢查資料欄政策標記和其政策，確認使用者是否有權存取資料。

**注意：**除了現有的[資料集 ACL](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-tw) 之外，系統也會強制執行資料欄層級存取控管。使用者必須同時具備資料集權限和政策標記權限，才能存取受資料欄層級存取控管機制保護的資料。

## 找出需要加上標記的內容

如要判斷您擁有的機密資料類型，以及哪些資料欄需要政策標記，請考慮使用 Sensitive Data Protection，產生整個組織、資料夾或專案的資料剖析檔。*資料剖析檔*包含資料表的指標和中繼資料，可協助您判斷[機密和高風險資料](https://docs.cloud.google.com/sensitive-data-protection/docs/sensitivity-risk-calculation?hl=zh-tw)的存放位置。Sensitive Data Protection 會在專案、資料表和資料欄層級回報這些指標。詳情請參閱「[機密資料探索總覽](https://docs.cloud.google.com/sensitive-data-protection/docs/data-profiles?hl=zh-tw)」。

下圖顯示資料欄資料剖析清單 (按一下即可放大)。資料風險值偏高的資料欄可能含有[高度機密資料](https://docs.cloud.google.com/sensitive-data-protection/docs/sensitivity-risk-calculation?hl=zh-tw#high-sensitivity)，且沒有資料欄層級存取控管機制。或者，這些資料欄可能含有中度或高度機密資料，且可供多人存取。

Sensitive Data Protection 中的資料欄剖析檔

## 用途範例

假設某組織需要將機密資料分為兩個類別：「高」和「中」。

如要設定資料欄層級安全性，資料監管員必須具備[適當權限](#roles)，並按照下列步驟設定[資料分類階層](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)。

1. 資料監管員建立名為「業務重要性」的分類，分類包含節點，或「高」和「中」*政策標記*。
2. 資料管理員決定「高」節點的政策包含名為 **high-tier-access** 的群組存取權。
3. 資料監管員在分類中建立更多層級的節點，位於「High」(高) 和「Medium」(中) 之下。最低層級的節點是葉節點，例如 *employee\_ssn* 葉節點。資料管理員可以為 *employee\_ssn* 葉節點建立不同的存取權政策，也可以不建立。
4. 資料管理員會將政策標記指派給特定資料表資料欄。在本例中，資料管理員將「High」存取權政策指派給資料表中的「employee\_ssn」*employee\_ssn*欄。
5. 在控制台的「Current schema」(目前結構定義) 頁面中，資料監管員可以查看控管特定資料欄的政策標記。在本例中，**employee\_ssn** 欄位於「High」政策標記下方，因此查看 **employee\_ssn** 的結構定義時，控制台會在 `Policy tags` 欄位中顯示分類名稱和政策標記：`Business criticality:High`。

   如要進一步瞭解如何使用控制台設定政策標記，請參閱「[設定資料欄的政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_policy)」。

   或者，您也可以使用 `bq update` 指令設定政策標記。`policyTags` 的 `names` 欄位包含**高**政策標記的 ID `projects/project-id/locations/location/taxonomies/taxonomy-id/policyTags/policytag-id`：

   ```
   [
    ...
    {
      "name": "ssn",
      "type": "STRING",
      "mode": "REQUIRED",
      "policyTags": {
        "names": ["projects/project-id/locations/location/taxonomies/taxonomy-id/policyTags/policytag-id"]
      }
    },
    ...
   ]
   ```

   如要進一步瞭解如何使用 `bq update` 指令設定政策標記，請參閱「[設定資料欄的政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_policy)」。

   **注意：** 每個資料欄只能指派一個政策標記。
6. 管理員對「Medium」政策標記執行類似步驟。

有了這項精細的存取權，您只要控管少數資料分類政策標記，就能管理多個資料欄的存取權。

如要進一步瞭解這些步驟，請參閱「[使用資料欄層級存取控管機制限制存取權](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)」。

## 與資料欄層級存取控管機制搭配使用的角色

下列角色用於 BigQuery 資料欄層級存取控管。

使用者必須具備 Data Catalog 政策標記管理員角色，才能建立及管理分類和政策標記。

| 角色/ID | 權限 | 說明 |
| --- | --- | --- |
| Data Catalog 政策標記管理員 (`datacatalog.categoryAdmin`) | `datacatalog.categories.getIamPolicy`  `datacatalog.categories.setIamPolicy`  `datacatalog.taxonomies.create`  `datacatalog.taxonomies.delete`  `datacatalog.taxonomies.get`  `datacatalog.taxonomies.getIamPolicy`  `datacatalog.taxonomies.list`  `datacatalog.taxonomies.setIamPolicy`  `datacatalog.taxonomies.update`  `resourcemanager.projects.get`  `resourcemanager.projects.list` | 在專案層級套用。  這個角色可授予下列權限：   * 建立、讀取、更新及刪除分類和政策標記。 * 取得及設定政策標記的 IAM 政策。 |

您必須具備 BigQuery 資料政策管理員、BigQuery 管理員或 BigQuery 資料擁有者角色，才能建立及管理資料政策。使用Google Cloud 控制台對分類強制執行存取控管時，服務會自動為您建立資料政策。

| 角色/ID | 權限 | 說明 |
| --- | --- | --- |
| BigQuery 資料政策管理員 (`bigquerydatapolicy.admin`)    BigQuery 管理員 (`bigquery.admin`)    BigQuery 資料擁有者 (`bigquery.dataOwner`) | `bigquery.dataPolicies.create`  `bigquery.dataPolicies.delete`  `bigquery.dataPolicies.get`  `bigquery.dataPolicies.getIamPolicy`  `bigquery.dataPolicies.list`  `bigquery.dataPolicies.setIamPolicy`  `bigquery.dataPolicies.update` | `bigquery.dataPolicies.create` 和 `bigquery.dataPolicies.list` 權限適用於專案層級。其他權限則適用於資料政策層級。  這個角色可執行下列操作：   * 建立、讀取、更新及刪除資料政策。 * 取得及設定資料政策的身分與存取權管理政策。 |

您也需要 `datacatalog.taxonomies.get` 權限，可從多個 [Data Catalog 預先定義角色](https://docs.cloud.google.com/iam/docs/roles-permissions/datacatalog?hl=zh-tw)取得。

使用者必須具備 Data Catalog 精細讀取者角色，才能存取受保護資料欄中的資料。

| 角色/ID | 權限 | 說明 |
| --- | --- | --- |
| 具備精細的讀取權限/`datacatalog.categoryFineGrainedReader` | `datacatalog.categories.fineGrainedGet` | 在政策標記層級套用。  這個角色可授予存取受政策標記限制的資料欄內容。 |

如要進一步瞭解 Data Catalog 角色，請參閱「[Data Catalog IAM 角色](https://docs.cloud.google.com/iam/docs/roles-permissions/datacatalog?hl=zh-tw)」。如要進一步瞭解 BigQuery 角色，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 寫入作業的影響

如要讀取受資料欄層級存取控管保護的資料欄資料，使用者一律須具備資料欄政策標記的精細讀取權限。

適用情況：

* 資料表，包括 Wildcard 資料表
* Views
* 複製資料表

如要將資料寫入受資料欄層級存取控管保護的資料欄，使用者需求取決於寫入類型。

如果寫入作業是*插入*，則不需要精細的讀取權限。不過，除非使用者具備精細的讀取權限，否則無法讀取插入的資料。

如果使用者執行 [INSERT SELECT 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_select_statement)，則必須具備查詢資料表的[精細讀取者角色](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#fine_grained_reader)。

如果寫入作業是*更新*、*刪除*或*合併*，使用者必須具備讀取資料欄的精細讀取權限，才能執行作業。

使用者可以從本機檔案或 Cloud Storage 載入資料。將資料載入資料表時，BigQuery 不會檢查目的地資料表資料欄的精細讀取者權限。這是因為載入資料時，不需要從目的地資料表讀取內容。同樣地，使用者可以從串流載入資料，因為串流載入不會檢查政策標記。除非使用者具備精細的讀取權限，否則無法讀取從串流載入的資料。

詳情請參閱「[資料欄層級存取控管對寫入作業的影響](https://docs.cloud.google.com/bigquery/docs/column-level-security-writes?hl=zh-tw)」。

## 查詢資料表

如果使用者有資料集存取權，且具備 Data Catalog 精細讀取者角色，就能存取資料欄資料。使用者照常執行查詢。

如果使用者有資料集存取權，但沒有 Data Catalog 精細讀取者角色，就無法存取資料欄。如果這類使用者執行 `SELECT *`，就會收到錯誤訊息，列出無法存取的資料欄。如要解決這項錯誤，可以採取下列任一做法：

* 修改查詢，排除使用者無法存取的資料欄。舉例來說，如果使用者無法存取 `ssn` 資料欄，但可以存取其餘資料欄，則可執行下列查詢：

  ```
  SELECT * EXCEPT (ssn) FROM ...
  ```

  在上述範例中，`EXCEPT` 子句會排除 `ssn` 資料欄。
* 請 Data Catalog 管理員將使用者新增為相關資料類別的 Data Catalog 精細讀取者。錯誤訊息會提供使用者需要存取權的政策標記全名。

## 查詢檢視表

資料欄層級安全性對檢視表的影響，與檢視表是否為授權檢視表無關。在這兩種情況下，系統都會以透明的方式強制執行資料欄層級安全性。

「授權檢視表」是下列其中一項：

* 明確授權存取資料集中資料表的檢視表。
* 由於檢視表包含在授權資料集中，因此會隱含授權存取資料集中的資料表。

詳情請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」和「[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)」。

**如果檢視表不是授權檢視表：**

如果使用者具備檢視表基礎資料表和資料集的 IAM 存取權，以及檢視表基礎資料表的資料欄層級存取權，就能查詢檢視表中的資料欄。否則，使用者無法查詢檢視表中的資料欄。

**如果檢視表為授權檢視表：**

只有檢視表基礎資料表中的資料欄層級安全性，才能控管存取權。資料表層級和資料集層級的 IAM 政策 (如有) 不會用於檢查存取權。如果使用者有權存取授權檢視表基礎資料表中的政策標記，就能查詢授權檢視表中的資料欄。

下圖說明如何評估檢視表的存取權。

## 時間旅行和 max\_staleness materialized view 的影響

BigQuery 可讓您查詢資料表先前的狀態。這項功能可讓您查詢先前時間點的資料列。您也可以透過這項功能，還原特定時間點的資料表。

在舊版 SQL 中，您可以使用資料表名稱上的[時間修飾詞](https://docs.cloud.google.com/bigquery/docs/table-decorators?hl=zh-tw#time_decorators)查詢歷來資料。在 GoogleSQL 中，您可以使用資料表的 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 子句查詢歷來資料。

設定 [`max_staleness`](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#max_staleness) 選項的 materialized view 會傳回過時時間間隔內的歷來資料。這項行為類似於在檢視表上次重新整理時使用 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 進行查詢，因為這可讓 BigQuery 查詢已刪除或更新的記錄。假設您在時間 *t* 查詢資料表的歷來資料。在這種情況下：

* 如果時間 *t* 的結構定義與資料表目前的結構定義相同，或是其子集，BigQuery 會根據目前資料表最新的資料欄層級安全性進行檢查。如果使用者可以讀取目前的資料欄，就能查詢這些資料欄的歷來資料。如要刪除或遮蓋受資料欄層級安全性保護的資料欄機密資料，請先清理機密資料，並等待[設定的時間旅行時間範圍](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#configure_the_time_travel_window)結束，再放寬資料欄層級安全性。
* 如果時間 *t* 的結構定義與查詢中資料欄的目前結構定義不同，查詢就會失敗。

## 隱含刪除資料欄層級存取權政策

在某些情況下，系統會隱含 (自動) 移除資料表的政策標記。

自動刪除政策標記的一般原則如下：

* 除非提供含有政策標記的新結構定義，否則使用 [`WRITE_TRUNCATE` 寫入配置](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.write_disposition)的作業一律會覆寫目的地資料表上的任何現有政策標記。
* 如果作業的寫入配置為 `WRITE_APPEND`，系統會保留目的地資料表目前的政策標記。

具體來說，政策標記會在下列情況下隱含移除：

* 取代資料表：使用 [`CREATE OR REPLACE
  TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) DDL 陳述式取代資料表時，原始資料表上的所有現有政策標記都會遭到捨棄。
* 使用 `WRITE_TRUNCATE` 載入或查詢：使用 `WRITE_TRUNCATE` 寫入配置的作業會移除所有現有政策標記。包括使用 [`bq load
  --replace`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令載入資料，以及執行 `writeDisposition` 狀態設為 `WRITE_TRUNCATE` 的查詢。這類作業會完全覆寫資料表，除非您在目的地結構定義中明確提供現有政策標記，否則不會沿用這些標記。

  舉例來說，如果您指定 `--destination_table` 旗標，將查詢結果寫入資料表，除非您使用 `--destination_schema` 旗標指定含有政策標記的結構定義，否則資料表中的任何現有政策標記都會遭到移除。以下範例說明如何使用 `--destination_schema`。

  ```
  bq query --destination_table mydataset.mytable2 \
    --use_legacy_sql=false --destination_schema=schema.json \
    'SELECT * FROM mydataset.mytable1'
  ```

  結構定義變更與查詢執行作業分開進行。如果查詢隨後引發例外狀況，系統可能會略過任何結構定義變更。如果發生這種情況，請檢查目的地資料表結構定義，並視需要[手動更新](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。
* 資料表刪除或到期：如果資料表遭到明確刪除，或達到到期時間並自動移除，所有相關聯的政策標記也會從該資料表的結構定義中移除。
* 資料表複製作業：將沒有政策標記的資料表複製到有政策標記的目的地資料表時，除非使用 [`--append_table`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 旗標或 `"writeDisposition": "WRITE_APPEND"`，否則目的地資料表上的標記會遭到移除。

使用 [`TRUNCATE
TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#truncate_table_statement) DML 陳述式，可移除資料表中的所有資料列，同時保留其結構定義，但不會移除政策標記。

## 位置注意事項

選擇分類的位置時，請考量下列限制。

### 政策標記

分類是區域性資源，例如 BigQuery 資料集和資料表。建立分類時，您必須指定分類的區域或*位置*。

您可以在[所有提供 BigQuery 的區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)建立分類，並將政策標記套用至資料表。不過，如要將分類中的政策標記套用至資料表資料欄，分類和資料表必須位於相同區域。

雖然您無法將政策標記套用至位於其他位置的資料表資料欄，但可以明確複製分類，將分類複製到其他位置。

如要在多個區域位置使用相同的分類和政策標記，請參閱「[跨位置管理政策標記](https://docs.cloud.google.com/bigquery/docs/managing-policy-tags-across-locations?hl=zh-tw#replicating_a_taxonomy_in_a_new_location)」，進一步瞭解如何複製分類。

### 組織

您無法跨組織使用參照。資料表和要套用至資料欄的任何政策標記，都必須位於同一個組織。

## 限制

* 在組織資源之間遷移專案時，政策標記分類不會自動更新。您必須在目的地組織中手動重新建立分類，才能在 Google Cloud 控制台中查看。詳情請參閱「[處理特殊情況](https://docs.cloud.google.com/resource-manager/docs/handle-special-cases?hl=zh-tw#policy-tag-taxonomies)」。
* 如果預留項目是以特定 BigQuery 版本建立，則可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
* BigQuery 僅支援 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)、[BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)和 [BigQuery Omni 資料表](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)的資料欄層級存取控管。
* 一個資料欄只能有一個政策標記。
* 一個資料表最多可有 1,000 個不重複的政策標記。
* 如果啟用資料欄層級存取控管，就無法使用舊版 SQL。如果目標資料表有任何政策標記，系統會拒絕任何舊版 SQL 查詢。
* 政策標記階層從根節點到最低層級子標記，最多只能有五個層級，如以下螢幕截圖所示：
* 機構內所有專案的分類名稱不得重複。
* 如果啟用了資料欄層級或資料列層級存取控管，就無法跨區域複製資料表。如果來源資料表有任何政策標記，則跨區域複製資料表會遭到拒絕。
* 如要瞭解政策標記和分類的配額與限制，請參閱「[資料政策](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#data-policy-management)」。

## 定價

資料欄層級存取控管機制必須同時使用 BigQuery 和 Data Catalog。如要瞭解這些產品的定價資訊，請參閱下列主題：

* [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Data Catalog 定價](https://docs.cloud.google.com/dataplex/pricing?hl=zh-tw#data-catalog-pricing)

## 稽核記錄

讀取含有政策標記的資料表資料時，我們會將參照的政策標記儲存在 Cloud Logging 中。不過，政策標記檢查與觸發檢查的查詢無關。

透過 Cloud Logging，稽核人員可以瞭解哪些人員具備何種存取權，可存取哪些類別的機密資料。詳情請參閱「[稽核政策標記](https://docs.cloud.google.com/bigquery/docs/auditing-policy-tags?hl=zh-tw)」。

如要進一步瞭解 BigQuery 的記錄功能，請參閱「[BigQuery 監控功能簡介](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)」。

如要進一步瞭解 Google Cloud中的記錄功能，請參閱「[Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw)」。

## 後續步驟

* 如要進一步瞭解如何使用資料欄層級存取控管機制，請參閱「[使用資料欄層級存取控管機制限制存取權](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)」。
* 如要瞭解政策標記的最佳做法，請參閱「[BigQuery 最佳做法：使用政策標記](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-08 (世界標準時間)。"],[],[]]