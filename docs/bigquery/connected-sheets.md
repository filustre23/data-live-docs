Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用連結試算表

連結試算表將 BigQuery 的規模帶到熟悉的 Google 試算表介面。透過連結試算表，您可以預覽 BigQuery 資料，並在根據整組資料建立的資料透視表、公式和圖表中使用這些資料。

你還可以執行下列操作：

* 與合作夥伴、分析師或其他相關人員利用熟悉的試算表介面協同合作。
* 不需要額外匯出試算表，就能確保資料分析的單一事實來源。
* 簡化報表和資訊主頁的工作流程。

「連結試算表」會根據您的要求或預先排定的時間表，代替您執行 BigQuery 查詢。這些查詢的結果會儲存在試算表中，方便您分析及共用資料。

## 應用實例

以下列舉幾個用途，說明如何使用連結試算表分析試算表中的大量資料，而不必瞭解 SQL。

* **業務規劃：**建構及準備資料集，讓其他人從資料中找出洞察。例如分析銷售資料，判斷哪些產品在不同地點的銷量較佳。
* **客戶服務：**找出每 10,000 名顧客中，客訴最多的商店。
* **銷售：**建立內部財務和銷售報表，並與業務代表分享收益報表。

## 存取控管

BigQuery 資料集和資料表的直接存取權，是在 BigQuery 內控管。如果只想授予使用者 Google 試算表存取權，請共用試算表，不要授予 BigQuery 存取權。

僅具備 Google 試算表存取權的使用者，可以在試算表中執行分析，並使用其他 Google 試算表功能，但無法執行下列操作：

* 手動重新整理工作表中的 BigQuery 資料。
* 排定重新整理工作表資料的時間。

在連結試算表中篩選資料時，系統會根據你選取的專案，重新整理傳送至 BigQuery 的查詢。您可以在相關專案中使用下列記錄篩選器，查看已執行的查詢：

```
resource.type="bigquery_resource"
protoPayload.metadata.firstPartyAppMetadata.sheetsMetadata.docId != NULL_VALUE
```

### VPC Service Controls

您可以使用 [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls?hl=zh-tw) 限制Google Cloud 資源的存取權。由於 VPC Service Controls 不支援 Google 試算表，因此您可能無法存取 VPC Service Controls 保護的 BigQuery 資料。如果您具備必要的允許權限，且符合 VPC Service Controls 的存取限制規定，只要設定 VPC Service Controls 範圍，即可允許透過連結試算表發出的查詢。如要這麼做，您必須使用下列項目設定 perimeter：

* 存取層級或輸入規則，允許來自 perimeter 外部受信任 IP 位址、身分和受信任用戶端裝置的要求。
* 允許將查詢結果複製到使用者試算表的輸出規則。

請參閱「[設定輸入和輸出政策](https://docs.cloud.google.com/vpc-service-controls/docs/configuring-ingress-egress-policies?hl=zh-tw)」和「[設定存取層級](https://docs.cloud.google.com/vpc-service-controls/docs/use-access-levels?hl=zh-tw)」一文，瞭解如何正確設定[規則](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw)。如要設定 perimeter，允許複製必要資料，請使用下列 YAML 檔案：

```
# Allows egress to Sheets through the Connected Sheets feature
- egressTo:
    operations:
    - serviceName: 'bigquery.googleapis.com'
      methodSelectors:
      - permission: 'bigquery.vpcsc.importData'
    resources:
    - projects/628550087766 # Sheets-owned Google Cloud project
  egressFrom:
    identityType: ANY_USER_ACCOUNT
```

**注意：** 連結試算表已排定的重新整理作業並不會反映任何使用者相關資料 (例如 IP 位址或裝置資訊)。
以使用者相關資料來限制存取權的 VPC Service Controls 範圍會導致排定的重新整理作業失敗。

## 事前準備

首先，請確認您符合在試算表中存取 BigQuery 資料的需求條件，詳情請參閱 Google Workspace 主題「[開始在 Google 試算表中使用 BigQuery 資料](https://support.google.com/docs/answer/9702507?hl=zh-tw)」的「事前準備」一節。

如果您沒有已設定計費功能的 Google Cloud 專案，請按照下列步驟操作：

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).

1. 新專案會自動啟用 BigQuery。如要在現有專案中啟用 BigQuery，請前往

   啟用 BigQuery API (如果尚未啟用)。

   **啟用 API 所需的角色**

   您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「Service Usage 管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

如要避免系統繼續計費，您可以刪除建立的資源。詳情請參閱[清除所用資源](#clean-up)一節。

## 從連結試算表開啟 BigQuery 資料集

以下範例使用公開資料集，說明如何從 Google 試算表連結至 BigQuery：

1. 建立或開啟 Google 試算表。
2. 依序按一下「資料」、「資料連接器」和「連結至 BigQuery」。

   **注意：** 如果找不到「資料連接器」選項，請參閱「[事前準備](#before_you_begin)」一節。
3. 選取已啟用計費功能的 Google Cloud 專案。
4. 點選「公開資料集」。
5. 在搜尋框中輸入 **chicago**，然後選取「chicago\_taxi\_trips」資料集。
6. 選取「taxi\_trips」資料表，然後點選「連線」。

   試算表應類似以下內容：

開始使用試算表。您可以使用熟悉的 Google 試算表技術，建立資料透視表、公式、圖表、計算欄和排定查詢。詳情請參閱[連結試算表教學課程](https://www.youtube.com/watch?v=rkimIhnLKGI&hl=zh-tw)。

雖然試算表只會預覽 500 列，但任何資料透視表、公式和圖表都會使用整組資料。資料透視表傳回的結果列數上限為 200,000 列。

您也可以將資料擷取至 Google 試算表。資料擷取作業傳回的結果，其資料列和儲存格數量上限取決於下列條件：

* 如果列數小於或等於 50,000，則沒有儲存格限制。
* 如果列數大於 5 萬但小於或等於 50 萬，則儲存格數量必須小於或等於 500 萬。
* 如果資料列數量超過 50 萬，則不支援資料提取功能。

使用連結試算表，根據資料建立圖表、資料透視表、公式或其他運算儲存格時，連結試算表會代表您在 BigQuery 中執行查詢。如要查看這項查詢，請按照下列步驟操作：

1. 選取你建立的儲存格或圖表。
2. 將游標懸停在 refresh「Refresh」(重新整理) 上。
3. 選用：如要重新整理連結試算表中的查詢結果，請按一下 refresh「Refresh」(重新整理)。
4. 如要在 BigQuery 中查看查詢，請按一下 info\_outline「Query details on BigQuery」(BigQuery 查詢詳細資料)。

   查詢會在 Google Cloud 控制台中開啟。

## 在連結試算表中開啟資料表

如要在連結試算表中開啟資料表，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集，找出要在 Google 試算表中開啟的資料表。
4. 依序點選**「Overview」(總覽) >「Tables」(資料表)**，然後按一下資料表名稱旁的
   more\_vert **「View actions」(查看動作)**，
   接著依序選取**「Open in」(開啟方式) >「Connected Sheets」(連結試算表)**。

## 在連結試算表中開啟已儲存的查詢

確認您有[已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#view_all_saved_queries)。詳情請參閱「[建立已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw)」。

如要在連結試算表中開啟已儲存的查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「查詢」。找出要在連結試算表中開啟的已儲存查詢。
4. 按一下已儲存的查詢旁的 more\_vert **「Open actions」(開啟動作)**，然後依序點選**「Open in」(開啟方式) >「Connected Sheets」(連結試算表)**。

   或者，按一下已儲存的查詢名稱，在詳細資料窗格中開啟，然後依序點選 **「Open in」(開啟方式) >「Connected Sheets」(連結試算表)**。

## 監控連結試算表的 BigQuery 使用情形

BigQuery 管理員可以監控及稽核連結試算表的資源消耗量，瞭解使用模式、管理費用，以及找出常用報表。下列各節提供 SQL 查詢範例，協助您在組織和專案層級監控這項用量。詳情請參閱「[`JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)」。

所有源自連結試算表的查詢都會指派專屬工作 ID 前置字元：`sheets_dataconnector`。您可以使用這個前置字串，在 `INFORMATION_SCHEMA.JOBS` 檢視畫面中篩選工作。

### 在組織層級依使用者匯總連結試算表用量

下列查詢會提供過去 30 天內，貴組織中熱門連結試算表使用者的摘要，並依計費資料總量排序。這項查詢會匯總每位使用者的查詢總數、計費位元組總數和運算單元毫秒總數。這項資訊有助於瞭解採用情形，以及找出資源的主要使用者。

```
SELECT
  user_email,
  COUNT(*) AS total_queries,
  SUM(total_bytes_billed) AS total_bytes_billed,
  SUM(total_slot_ms) AS total_slot_ms
FROM
  `region-REGION_NAME.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION`
WHERE
  -- Filter for jobs created in the last 30 days
  creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  -- Filter for jobs originating from Connected Sheets
  AND job_id LIKE 'sheets_dataconnector%'
  -- Filter for completed jobs
  AND state = 'DONE'
  AND (statement_type IS NULL OR statement_type <> 'SCRIPT')
GROUP BY
  1
ORDER BY
  total_bytes_billed DESC;
```

將 `REGION_NAME` 替換為專案的區域。例如：`region-us`。

**注意：** 您必須使用區域限定詞來查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

傳回的結果看起來類似下列內容：

```
+---------------------+---------------+--------------------+-----------------+
| user_email          | total_queries | total_bytes_billed | total_slot_ms   |
+---------------------+---------------+--------------------+-----------------+
| alice@example.com   | 152           | 12000000000        | 3500000         |
| bob@example.com     | 45            | 8500000000         | 2100000         |
| charles@example.com | 210           | 1100000000         | 1800000         |
+---------------------+---------------+--------------------+-----------------+
```

### 在組織層級尋找連結試算表查詢的工作記錄

下列查詢會提供連結試算表執行的每項個別工作的詳細記錄。這項資訊有助於稽核及找出特定高成本查詢。

```
SELECT
  job_id,
  creation_time,
  user_email,
  project_id,
  total_bytes_billed,
  total_slot_ms
FROM
  `region-REGION_NAME.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION`
WHERE
  creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND job_id LIKE 'sheets_dataconnector%'
  AND state = 'DONE'
  AND (statement_type IS NULL OR statement_type <> 'SCRIPT')
ORDER BY
  creation_time DESC;
```

將 `REGION_NAME` 替換為專案的區域。例如：`region-us`。

**注意：** 您必須使用區域限定詞來查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

傳回的結果看起來類似下列內容：

```
+---------------------------------+---------------------------------+-----------------+------------+--------------------+---------------+
| job_id                          | creation_time                   | user_email      | project_id | total_bytes_billed | total_slot_ms |
+---------------------------------+---------------------------------+-----------------+------------+--------------------+---------------+
| sheets_dataconnector_bquxjob_1  | 2025-11-06 00:26:53.077000 UTC  | abc@example.com | my_project | 12000000000        | 3500000       |
| sheets_dataconnector_bquxjob_2  | 2025-11-06 00:24:04.294000 UTC  | xyz@example.com | my_project | 8500000000         | 2100000       |
| sheets_dataconnector_bquxjob_3  | 2025-11-03 23:17:25.975000 UTC  | bob@example.com | my_project | 1100000000         | 1800000       |
+---------------------------------+---------------------------------+-----------------+------------+--------------------+---------------+
```

### 依使用者匯總專案層級的連結試算表用量

如果您沒有組織層級權限，或只需要監控特定專案，請執行下列查詢，找出過去 30 天內專案中連結試算表用量最高的使用者。查詢會匯總每位使用者的查詢總數、計費位元組總數和運算單元毫秒總數。這項資訊有助於瞭解採用情形，以及找出資源的主要使用者。

```
SELECT
  user_email,
  COUNT(*) AS total_queries,
  SUM(total_bytes_billed) AS total_bytes_billed,
  SUM(total_slot_ms) AS total_slot_ms
FROM
  -- This view queries the project you are currently running the query in.
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  -- Filter for jobs created in the last 30 days
  creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  -- Filter for jobs originating from Connected Sheets
  AND job_id LIKE 'sheets_dataconnector%'
  -- Filter for completed jobs
  AND state = 'DONE'
  AND (statement_type IS NULL OR statement_type <> 'SCRIPT')
GROUP BY
  user_email
ORDER BY
  total_bytes_billed DESC
LIMIT
  10;
```

將 `REGION_NAME` 替換為專案的區域。例如：`region-us`。

**注意：** 您必須使用區域限定詞來查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

傳回的結果看起來類似下列內容：

```
+---------------------+---------------+--------------------+-----------------+
| user_email          | total_queries | total_bytes_billed | total_slot_ms   |
+---------------------+---------------+--------------------+-----------------+
| alice@example.com   | 152           | 12000000000        | 3500000         |
| bob@example.com     | 45            | 8500000000         | 2100000         |
| charles@example.com | 210           | 1100000000         | 1800000         |
+---------------------+---------------+--------------------+-----------------+
```

### 尋找專案層級的連結試算表查詢工作記錄

如果您沒有組織層級權限，或只需要監控特定專案，請執行下列查詢，查看目前專案所有連結試算表查詢的詳細記錄：

```
SELECT
  job_id,
  creation_time,
  user_email,
  total_bytes_billed,
  total_slot_ms,
  query
FROM
  -- This view queries the project you are currently running the query in.
  `region-REGION_NAME.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE
  creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND job_id LIKE 'sheets_dataconnector%'
  AND state = 'DONE'
  AND (statement_type IS NULL OR statement_type <> 'SCRIPT')
ORDER BY
  creation_time DESC;
```

將 `REGION_NAME` 替換為專案的區域。例如：`region-us`。

**注意：** 您必須使用區域限定詞來查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

傳回的結果看起來類似下列內容：

```
+---------------------------------+---------------------------------+------------------+--------------------+-----------------+---------------------------------+
| job_id                          | creation_time                   | user_email       | total_bytes_billed | total_slot_ms   |  query                          |
+---------------------------------+---------------------------------+------------------+--------------------+-----------------+---------------------------------+
| sheets_dataconnector_bquxjob_1  | 2025-11-06 00:26:53.077000 UTC  | abc@example.com  | 12000000000        | 3500000         |  SELECT ... FROM dataset.table1 |
| sheets_dataconnector_bquxjob_2  | 2025-11-06 00:24:04.294000 UTC  | xyz@example.com  | 8500000000         | 2100000         |  SELECT ... FROM dataset.table2 |
| sheets_dataconnector_bquxjob_3  | 2025-11-03 23:17:25.975000 UTC  | bob@example.com  | 1100000000         | 1800000         |  SELECT ... FROM dataset.table3 |
+---------------------------------+---------------------------------+------------------+--------------------+-----------------+---------------------------------+
```

## 清除所用資源

如要避免系統向您的 Google Cloud 帳戶收取這個教學課程所用資源的費用，請按照下列步驟操作：

**注意**：刪除專案會造成以下影響：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

## 後續步驟

* 如需更多資訊，請參閱 Google Workspace 的「[開始在 Google 試算表中使用 BigQuery 資料](https://support.google.com/docs/answer/9702507?hl=zh-tw)」主題。
* 前往 YouTube 觀看[「使用連結試算表」播放清單](https://www.youtube.com/playlist?list=PLU8ezI8GYqs74i8hy_qln3FvkAuSpE-r1&hl=zh-tw)中的影片。
* 準備好開始實作了嗎？試試實驗室：

  + [連結試算表：Qwik Start](https://www.skills.google/focuses/18108?amp%3Bparent=catalog&hl=zh-tw)
  + [在 Google 試算表中檢視 BigQuery 帳單資料](https://www.skills.google/focuses/6916?amp%3Bparent=catalog&hl=zh-tw)
  + 展現您的專業：完成[在連結試算表中分析 BigQuery 資料技能徽章](https://www.skills.google/course_templates/632+doc?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-23 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-23 (世界標準時間)。"],[],[]]