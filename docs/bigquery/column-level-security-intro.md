Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料欄層級存取控管機制簡介

**注意：** 使用以特定 BigQuery 版本建立的預留項目時，這項功能可能無法使用。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

BigQuery 透過資料的*政策標記* (或依據類型的分類方式)，對機密資料欄提供精細的存取權限。您可以使用 BigQuery 資料欄層級存取權控管功能建立政策，以便在執行查詢當下檢查使用者是否具備適當存取權。舉例來說，政策可以強制執行存取檢查，例如：

* 你必須處於 `group:high-access` 狀態，才能看到包含 `TYPE_SSN` 的資料欄。

如要強化資料欄層級的存取控管，您可以選擇使用[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。
資料遮蓋功能可將資料欄的實際值替換為空值、預設值或雜湊內容，藉此遮蓋機密資料。

## 資料欄層級存取控管工作流程

如要在資料欄層級限制資料存取權，請按照下列步驟操作：

1. **定義分類和政策標記**。為資料建立及管理分類和政策標記。如需相關指南，請參閱「[使用政策標記的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)」。
2. **將政策標記指派給 BigQuery 資料欄**。在 BigQuery 中，使用結構定義註解，為要限制存取權的每個資料欄指派政策標記。
3. **強制執行分類架構的存取控管**。強制執行存取控管後，系統會套用分類中所有政策標記定義的存取限制。
4. **管理政策標記的存取權**。使用 [Identity and Access Management](https://docs.cloud.google.com/iam?hl=zh-tw) (IAM) 政策，限制對每個政策標記的存取權。政策會對屬於政策標記的每個資料欄生效。

使用者在查詢時嘗試存取資料欄資料時，BigQuery 會檢查資料欄政策標記及其政策，判斷使用者是否有權存取資料。

 **注意：**系統會*一併*強制執行資料欄層級存取控管，以及現有的[資料集 ACL](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-tw)。使用者必須同時具備資料集權限和政策標記權限，才能存取受資料欄層級存取控管機制保護的資料。

## 找出需要加上標記的內容

如要判斷您擁有的機密資料類型，以及哪些資料欄需要政策標記，請考慮使用 Sensitive Data Protection，產生機構、資料夾或專案的資料剖析檔。*資料剖析檔*包含資料表的指標和中繼資料，可協助您判斷[機密和高風險資料](https://docs.cloud.google.com/sensitive-data-protection/docs/sensitivity-risk-calculation?hl=zh-tw)的存放位置。
Sensitive Data Protection 會在專案、資料表和資料欄層級回報這些指標。詳情請參閱「[機密資料探索總覽](https://docs.cloud.google.com/sensitive-data-protection/docs/data-profiles?hl=zh-tw)」。

下圖顯示欄資料剖析的清單 (按一下即可放大)。
資料風險值高的資料欄可能含有[高度機密資料](https://docs.cloud.google.com/sensitive-data-protection/docs/sensitivity-risk-calculation?hl=zh-tw#high-sensitivity)，且沒有資料欄層級的存取權控管機制。或者，這些資料欄可能含有中度或高度機密資料，且許多人都能存取。

Sensitive Data Protection 中的資料欄資料剖析檔

## 用途範例

假設某個機構需要將機密資料歸類為「高」和「中」這兩個類別。

如要設定資料欄層級的安全防護機制，資料管理員必須具備[適當權限](#roles)，才能執行下列步驟，設定[資料分類的階層](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)。

1. 資料管理員建立名為「業務關鍵性」的分類。分類包括節點或*政策標記*「高」和「中」。
2. 資料管理員決定「高」節點的政策包含名為「high-tier-access」的群組存取權。
3. 資料管理員在分類法中「高」和「中」底下，建立更多節點層級。最低層級的節點是葉節點，例如 *employee\_ssn* 葉節點。資料管理員可以為 *employee\_ssn* 葉節點建立不同的存取政策，也可以不建立。
4. 資料管理員會將政策標記指派給特定資料表欄。在本範例中，資料管理員會將「高」存取權政策指派給資料表中的「employee\_ssn」*employee\_ssn*資料欄。
5. 在控制台的「目前結構定義」頁面中，資料管理員可以查看控管特定資料欄的政策標記。在本例中，「employee\_ssn」欄位於「High」政策標記下方，因此查看「employee\_ssn」的結構定義時，主控台會在 `Policy tags` 欄位中顯示分類名稱和政策標記：`Business criticality:High`。

   如要瞭解如何使用控制台設定政策標記，請參閱「[在資料欄上設定政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_policy)」。

   或者，您也可以使用 `bq update` 指令設定政策標記。`policyTags` 的 `names` 欄位包含「高」政策標記的 ID，`projects/project-id/locations/location/taxonomies/taxonomy-id/policyTags/policytag-id`：

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

   如要瞭解如何使用 `bq update` 指令設定政策標記，請參閱「[在資料欄上設定政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_policy)」。

   **注意：** 每個資料欄只能指派一個政策標記。
6. 管理員會對「中」政策標記執行類似步驟。

有了這項精細的存取權，您只需控管少數資料分類政策標記，就能管理多個資料欄的存取權。

如要瞭解這些步驟的詳細資訊，請參閱「[使用資料欄層級存取控管機制限制存取權](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)」。

## 搭配資料欄層級存取權控管使用的角色

下列角色用於 BigQuery 資料欄層級的存取權控管。

使用者必須具備「Data Catalog 政策標記管理員」角色，才能建立及管理分類和政策標記。

| 角色/ID | 權限 | 說明 |
| --- | --- | --- |
| Data Catalog 政策標記管理員 (`datacatalog.categoryAdmin`) | `datacatalog.categories.getIamPolicy`  `datacatalog.categories.setIamPolicy`  `datacatalog.taxonomies.create`  `datacatalog.taxonomies.delete`  `datacatalog.taxonomies.get`  `datacatalog.taxonomies.getIamPolicy`  `datacatalog.taxonomies.list`  `datacatalog.taxonomies.setIamPolicy`  `datacatalog.taxonomies.update`  `resourcemanager.projects.get`  `resourcemanager.projects.list` | 適用於專案層級。  這個角色可授予下列權限：   * 建立、讀取、更新及刪除分類和政策標記。 * 取得及設定政策標記的身分與存取權管理政策。 |

如要建立及管理資料政策，您必須具備 BigQuery 資料政策管理員、BigQuery 管理員或 BigQuery 資料擁有者角色。使用Google Cloud 控制台對分類架構強制執行存取控管時，服務會自動為您建立資料政策。

| 角色/ID | 權限 | 說明 |
| --- | --- | --- |
| BigQuery 資料政策管理員 (`bigquerydatapolicy.admin`)    BigQuery 管理員 (`bigquery.admin`)    BigQuery 資料擁有者 (`bigquery.dataOwner`) | `bigquery.dataPolicies.create`  `bigquery.dataPolicies.delete`  `bigquery.dataPolicies.get`  `bigquery.dataPolicies.getIamPolicy`  `bigquery.dataPolicies.list`  `bigquery.dataPolicies.setIamPolicy`  `bigquery.dataPolicies.update` | `bigquery.dataPolicies.create` 和 `bigquery.dataPolicies.list` 權限適用於專案層級。其他權限則適用於資料政策層級。  這個角色可執行下列作業：   * 建立、讀取、更新及刪除資料政策。 * 取得及設定資料政策的身分與存取權管理政策。 |

您也需要 `datacatalog.taxonomies.get` 權限，可透過多個[Data Catalog 預先定義角色](https://docs.cloud.google.com/iam/docs/roles-permissions/datacatalog?hl=zh-tw)取得這項權限。

使用者必須具備 Data Catalog 精細讀取者角色，才能存取受保護資料欄中的資料。

| 角色/ID | 權限 | 說明 |
| --- | --- | --- |
| 精細讀取者/`datacatalog.categoryFineGrainedReader` | `datacatalog.categories.fineGrainedGet` | 適用於政策標記層級。  這個角色可授予存取權，查看受政策標記限制的資料欄內容。 |

如要進一步瞭解 Data Catalog 角色，請參閱「[Data Catalog Identity and Access Management (IAM)](https://docs.cloud.google.com/data-catalog/docs/concepts/iam?hl=zh-tw)」。如要進一步瞭解 BigQuery 角色，請參閱[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

## 寫入作業的影響

如要讀取受資料欄層級存取控管保護的資料欄，使用者一律須透過資料欄政策標記的細部讀取存取權，取得讀取權限。

適用情況：

* 資料表，包括萬用字元資料表
* 觀看次數
* 複製資料表

如要將資料寫入受欄級存取控管保護的欄，使用者必須符合下列條件 (視寫入類型而定)：

如果寫入作業是*插入*，則不需要細部讀取權限。不過，除非使用者具有細部讀取權限，否則無法讀取插入的資料。

如果使用者執行 [INSERT SELECT 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_select_statement)，則必須在查詢的資料表上具備[精細讀取者角色](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#fine_grained_reader)。

如果寫入作業是*更新*、*刪除*或*合併*，使用者必須對讀取資料欄具有精細的讀取存取權，才能執行作業。

使用者可以從本機檔案或 Cloud Storage 載入資料。將資料載入資料表時，BigQuery 不會檢查目的地資料表資料欄的細部讀取者權限。這是因為載入資料不需要從目的地資料表讀取內容。同樣地，使用者可以從串流載入資料，因為串流載入不會檢查政策標記。除非使用者具有精細的讀取權限，否則無法讀取從串流載入的資料。

詳情請參閱「[使用資料欄層級存取權控管功能對寫入作業造成的影響](https://docs.cloud.google.com/bigquery/docs/column-level-security-writes?hl=zh-tw)」。

## 查詢資料表

如果使用者有資料集存取權，且具備 Data Catalog 細部讀取者角色，即可存取欄資料。使用者照常執行查詢。

如果使用者有資料集存取權，但沒有 Data Catalog 細部讀取者角色，就無法存取資料欄資料。如果這類使用者執行 `SELECT *`，系統會顯示錯誤訊息，列出使用者無法存取的資料欄。如要解決這項錯誤，請採取下列任一做法：

* 修改查詢，排除使用者無法存取的資料欄。舉例來說，如果使用者無法存取「`ssn`」欄，但可以存取其餘欄，則可執行下列查詢：

  ```
  SELECT * EXCEPT (ssn) FROM ...
  ```

  在上述範例中，`EXCEPT` 子句會排除 `ssn` 資料欄。
* 請 Data Catalog 管理員將使用者新增為相關資料類別的 Data Catalog 精細讀取者。錯誤訊息會提供使用者需要存取權的政策標記完整名稱。

## 查詢檢視畫面

資料欄層級安全性對檢視畫面的影響，與檢視畫面是否為授權檢視畫面無關。無論是哪種情況，系統都會以透明方式強制執行資料欄層級安全性。

*授權 view* 是指下列其中一種：

* 明確授權可存取資料集內資料表的檢視表。
* 檢視表隱含授權可存取資料集中的資料表，因為檢視表位於授權資料集中。

詳情請參閱「[授權檢視區塊](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」和「[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)」。

**如果檢視區塊不是授權檢視區塊：**

如果使用者具有檢視表基礎資料表和資料集的 IAM 存取權，以及檢視表基礎資料表的資料欄層級存取權，就能查詢檢視表中的資料欄。否則使用者無法查詢檢視區塊中的資料欄。

**如果檢視畫面是授權 view：**

只有檢視表基礎資料表中的資料欄層級安全防護機制，才能控管存取權。系統不會使用資料表層級和資料集層級的 IAM 政策 (如有) 檢查存取權。如果使用者有權存取授權檢視表底層資料表使用的政策標記，就能查詢授權檢視表中的資料欄。

下圖顯示系統如何評估檢視區塊的存取權。

## 時間旅行和具體化檢視表 (含 max\_staleness) 的影響

BigQuery 可讓您查詢先前狀態的資料表。這項功能可讓您查詢先前時間點的資料列。您也可以從特定時間點還原資料表。

在舊版 SQL 中，您可以在資料表名稱上使用[時間修飾符](https://docs.cloud.google.com/bigquery/docs/table-decorators?hl=zh-tw#time_decorators)，查詢歷來資料。在 GoogleSQL 中，您可以使用資料表上的 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 子句查詢歷來資料。

如果具體化檢視區塊設定了 [`max_staleness`](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#max_staleness) 選項，就會傳回過時間隔內的歷來資料。這種行為與上次重新整理檢視區塊時使用 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 的查詢類似，因為這可讓 BigQuery 查詢已刪除或更新的記錄。假設您在時間 *t* 查詢資料表的歷來資料。請按照下列步驟操作：

* 如果時間 *t* 的結構定義與資料表的目前結構定義相同或為其子集，BigQuery 會根據目前資料表的最新資料欄層級安全性進行檢查。如果使用者有權讀取目前的資料欄，就能查詢這些資料欄的歷來資料。如要刪除或遮蓋受資料欄層級安全防護機制保護的資料欄中的機密資料，必須在機密資料清除作業完成後，經過[設定的時間範圍](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#configure_the_time_travel_window)，才能安全地放寬資料欄層級安全防護機制。
* 如果時間 *t* 的結構定義與查詢中資料欄的目前結構定義不同，查詢就會失敗。

## 位置注意事項

選擇分類位置時，請考量下列限制。

### 政策標記

分類是區域資源，例如 BigQuery 資料集和資料表。建立分類時，請指定分類的地區或*位置*。

您可以在[所有提供 BigQuery 的區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)中，建立分類並將政策標記套用至資料表。不過，如要將分類中的政策標記套用至資料表欄，分類和資料表必須位於同一個區域位置。

雖然您無法將政策標記套用至其他位置的資料表欄，但可以明確複製分類架構，將其複製到其他位置。

如要在多個區域地點使用相同的分類和政策標記，請參閱「[跨地點管理政策標記](https://docs.cloud.google.com/bigquery/docs/managing-policy-tags-across-locations?hl=zh-tw#replicating_a_taxonomy_in_a_new_location)」，進一步瞭解如何複製分類。

### 組織

您無法跨機構使用參照。資料表和要套用至資料欄的任何政策標記，都必須位於同一個機構。

## 限制

* 使用以特定 BigQuery 版本建立的預留項目時，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
* BigQuery 僅支援[BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)、[BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)和 [BigQuery Omni 資料表](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)的資料欄層級存取控管。
* 如果覆寫目的地資料表，系統會從資料表移除所有現有的政策標記，除非您使用 `--destination_schema` 旗標指定含有政策標記的結構定義。以下範例說明如何使用 `--destination_schema`。

  ```
  bq query --destination_table mydataset.mytable2 \
    --use_legacy_sql=false --destination_schema=schema.json \
    'SELECT * FROM mydataset.mytable1'
  ```

  結構定義異動與查詢執行作業是分開進行。如果您指定 `--destination_table` 旗標，將查詢結果寫入資料表，且查詢隨後引發例外狀況，則系統可能會略過任何結構定義變更。如果發生這種情況，請檢查目的地資料表結構定義，並視需要[手動更新](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。
* 一個資料欄只能有一個政策標記。
* 表格最多可有 1,000 個不重複的政策標記。
* 啟用資料欄層級存取控管機制後，就無法使用舊版 SQL。如果目標資料表有任何政策標記，系統會拒絕所有舊版 SQL 查詢。
* 從根節點到最低層級的子標記，政策標記階層最多只能有五個層級，如下方螢幕截圖所示：
* 機構內所有專案的分類名稱不得重複。
* 如果已啟用資料欄或資料列層級的存取控管，就無法跨區域複製資料表。如果來源資料表有任何政策標記，系統會拒絕跨區域複製資料表。

## 定價

如要進行資料欄層級的存取權控管，必須同時使用 BigQuery 和 Data Catalog。如要瞭解這些產品的價格資訊，請參閱下列主題：

* [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Data Catalog 定價](https://docs.cloud.google.com/dataplex/pricing?hl=zh-tw#data-catalog-pricing)

## 稽核記錄

讀取含有政策標記的資料表資料時，我們會將參照的政策標記儲存在 Cloud Logging 中。不過，政策標記檢查與觸發檢查的查詢無關。

稽核人員可透過 Cloud Logging 瞭解哪些人有權存取哪些類別的私密資料。詳情請參閱「[稽核政策標記](https://docs.cloud.google.com/bigquery/docs/auditing-policy-tags?hl=zh-tw)」。

如要進一步瞭解 BigQuery 中的記錄，請參閱「[BigQuery 監控簡介](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)」。

如要進一步瞭解記錄檔，請參閱 Google Cloud
[Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw)。

## 後續步驟

* 如要進一步瞭解如何使用資料欄層級存取控管，請參閱「[使用資料欄層級存取控管限制存取權](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)」。
* 如要瞭解政策標記的最佳做法，請參閱 [BigQuery 最佳做法：使用政策標記](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]