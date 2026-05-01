* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立已儲存的查詢

在查詢編輯器中撰寫 SQL 時，您可以儲存查詢並與他人共用。儲存的查詢是 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 程式碼資產，由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 提供支援。

如要進一步瞭解如何刪除已儲存的查詢及管理已儲存的查詢記錄，請參閱「[管理已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw)」一文。

## 所需權限

設定適當的權限，即可建立、編輯或查看已儲存的查詢。

所有具備 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`) 的使用者，都能以擁有者身分存取專案中建立的所有已儲存查詢。

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[使用身分與存取權管理功能控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 建立已儲存查詢的權限

如要建立及執行已儲存的查詢，您必須具備下列 IAM 權限：

* `dataform.locations.get`
* `dataform.locations.list`
* `dataform.repositories.list`
* `dataform.repositories.create`

  **注意：** 擁有 `dataform.repositories.create` 權限的使用者，可以使用預設的 Dataform 服務帳戶執行程式碼，並取得授予該服務帳戶的所有權限。詳情請參閱「[Dataform 權限的安全性考量](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#security-considerations-permissions)」。

您可以透過下列 IAM 角色取得這些權限：

* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
* [程式碼建立者](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeCreator) (`roles/dataform.codeCreator`)

**警告：** 程式碼資產的顯示設定受專案層級的 Dataform 權限規範。具備 `dataform.repositories.list` 權限的使用者 (這項權限包含在標準 BigQuery 角色中，例如「BigQuery Job User」、「BigQuery Studio User」和「BigQuery User」)，可以在專案的「Explorer」面板中查看所有程式碼資產，無論這些資產是由他們建立，還是與他們共用。 Google Cloud 如要限制可見度，可以建立排除 `dataform.repositories.list` 權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。**注意：**獲指派專案中程式碼建立者角色的使用者，可以使用 Dataform API 或 Dataform 指令列介面 (CLI)，列出該專案中程式碼資產的名稱。**注意：**建立已儲存的查詢時，BigQuery 會授予您該查詢的 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。在 Google Cloud 專案中獲派 Dataform 管理員角色的所有使用者，都擁有專案中所有已儲存查詢的擁有者存取權。如要覆寫這項行為，請參閱[在建立資源時授予特定角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-specific-role)。

### 編輯已儲存查詢的權限

如要編輯及執行已儲存的查詢，您必須具備下列 IAM 角色：

* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
* [程式碼編輯器](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor) (`roles/dataform.codeEditor`)

### 查看已儲存查詢的權限

如要查看及執行已儲存的查詢，您需要下列 IAM 角色：

* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
* [程式碼檢視者](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer) (`roles/dataform.codeViewer`)

## 設定程式碼資產的預設區域

Google Cloud 專案中的所有新程式碼資產都會使用預設區域。資產建立後，就無法變更區域。

**重要事項：** 如果在建立程式碼資產時變更區域，該區域會成為後續所有程式碼資產的預設區域。現有的程式碼資產不會受到影響。

如要設定新程式碼資產的預設區域，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 folder「檔案」，開啟檔案瀏覽器：
3. 在專案名稱旁，按一下
   more\_vert
   「View files panel actions」(查看檔案面板動作) >「Switch code region」(切換程式碼區域)。
4. 選取要設為預設的程式碼區域。
5. 按一下 [儲存]。

如需支援的區域清單，請參閱「[BigQuery Studio 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqstudio-loc)」。

## 建立已儲存的查詢

如要建立已儲存的查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「SQL 查詢」add\_box。
3. 在查詢編輯器中輸入有效的 SQL 查詢。舉例來說，您可以查詢[公開資料集](https://cloud.google.com/bigquery/public-data?hl=zh-tw)：

   ```
   SELECT
     name,
     SUM(number) AS total
   FROM
     `bigquery-public-data.usa_names.usa_1910_2013`
   GROUP BY
     name
   ORDER BY
     total DESC
   LIMIT
     10;
   ```

   或者，您也可以使用「參考」[面板](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#use-reference-panel)建構新查詢。
4. 按一下「儲存」
5. 在「儲存查詢」對話方塊中，輸入已儲存的查詢的名稱。
6. 選用：如要變更這項已儲存的查詢和所有其他程式碼資產日後使用的區域，請在「區域」欄位中選取新區域。
7. 按一下 [儲存]。

   系統會建立已儲存查詢的第一個版本。
8. 選用：儲存查詢後，您可以使用下列工具列查看查詢詳細資料或[版本記錄](#open_a_saved_query_version_as_a_new_query)、新增註解，或是回覆現有註解或取得相關連結：

   「註解」工具列功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。如要提供意見回饋或尋求這項功能的支援，請傳送電子郵件至 [bqui-workspace-pod@google.com](mailto:bqui-workspace-pod@google.com)。

## 共用已儲存的查詢

如要與使用者共用已儲存的查詢，請先授予該使用者已儲存查詢的存取權，並將他們新增至適當的 IAM 角色。然後產生已儲存的查詢的連結，並與使用者共用該連結。

與您共用查詢的使用者只會看到最新版本的查詢。
系統不會在共用查詢中顯示自動儲存但您未明確儲存的變更。

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
4. 找出並點選要授予存取權的已儲存查詢。您可以使用搜尋功能或篩選器尋找查詢。
5. 依序點按「共用」person\_add和「管理權限」。
6. 在「管理權限」窗格中，按一下「新增使用者/群組」。
7. 在「New principals」(新增主體) 欄位中輸入主體。
8. 在「Role」(角色) 清單中，選取下列其中一個角色：

   * [**程式碼擁有者**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner)：可以對已儲存的查詢執行任何動作，包括刪除或共用查詢。
   * [**程式碼編輯器**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor)：可編輯查詢。
   * [**程式碼檢視者**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer)：可以查看查詢。**注意：** 主體也必須具備 [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user) 角色，才能執行已儲存的查詢。
9. 選用：如要查看完整的角色清單和進階共用設定，請按一下「進階共用設定」。
10. 按一下 [儲存]。
11. 如要返回已儲存的查詢資訊，請按一下「關閉」。
12. 如要產生已儲存的查詢的連結，請按一下「分享」圖示 person\_add，然後按一下「取得連結」。

    連結即會複製到剪貼簿。

## 將已儲存的查詢版本開啟為新查詢

如要開啟現有已儲存的查詢的任何版本做為新查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
4. 選取已儲存的查詢。你可以使用搜尋功能或篩選器尋找查詢。
5. 按一下 history「版本記錄」。
6. 按一下已儲存的查詢版本旁的 more\_vert「查看動作」，然後點選「以新查詢開啟」。

## 更新已儲存的查詢

停止輸入文字兩秒後，系統會自動儲存您對已儲存的查詢文字所做的變更，並在「版本記錄」中顯示為「您的變更」。自動儲存的變更並非查詢的新版本。
您開啟查詢時，系統會重新顯示自動儲存的變更，但除非您明確將變更儲存為查詢的[新版本](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#work_with_saved_query_versions)，否則其他人都看不到這些變更。自動儲存的查詢會顯示在「預覽」中。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Queries」。
4. 選取已儲存的查詢。你可以使用搜尋功能或篩選器尋找查詢。
5. 修改查詢。
6. 如要儲存修改後的查詢，請依序點按 「儲存查詢」**>「儲存查詢」**，或按下 `Control+S` 鍵 (在 macOS 上為 `Command+S` 鍵)。

   系統會建立查詢的新版本。

## 上傳已儲存的查詢

您可以上傳本機 SQL 查詢，在 BigQuery Studio 中做為已儲存的查詢使用。上傳已儲存的查詢後， Google Cloud 控制台的 BigQuery 頁面也會顯示該查詢。

如要上傳已儲存的查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後執行下列其中一個步驟：

   * 在「查詢」旁，依序點按「查看動作」more\_vert>「上傳 SQL 查詢」。
   * 在 Google Cloud 專案名稱旁，依序點按 more\_vert「查看動作」>「上傳至專案」>「SQL 查詢」。
4. 在「Upload SQL」(上傳 SQL) 對話方塊的「SQL」欄位中，按一下「Browse」(瀏覽)，然後選取要上傳的查詢。
5. 選用：在「SQL 名稱」欄位中，編輯查詢名稱。
6. 在「Region」(區域) 欄位中，選取要上傳已儲存的查詢的區域。
7. 按一下「上傳」。

您可以透過「Explorer」窗格存取已儲存的查詢。

## 傳統版已儲存查詢

**已淘汰：** [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/enable-assets?hl=zh-tw) 中的已儲存查詢，日後將完全取代傳統的已儲存查詢。我們正在審查淘汰時程。詳情請參閱[傳統版已儲存查詢的淘汰事宜](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#classic-saved-queries-deprecation)。
如要瞭解如何遷移至已儲存的查詢，請參閱「[遷移傳統版已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#migrate_classic_saved_queries)」一文。

請參閱下列章節，瞭解如何建立及更新[傳統儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#classic_saved_queries)。如要進一步瞭解如何共用、遷移及刪除傳統版已儲存查詢，請參閱「[傳統版已儲存查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#classic_saved_queries)」。

**附註：** 如果尚未啟用 BigQuery Studio，傳統版儲存的查詢會顯示在**傳統版探索器**窗格的「已儲存的查詢」 **(NUMBER)** 資料夾中，而不是「(傳統版) 查詢」資料夾。

### 傳統版已儲存查詢的必要權限

如要建立、查看、更新及刪除傳統儲存查詢，必須要有以下 IAM 權限：

* **不公開**的傳統版已儲存查詢：
  + 建立不公開的傳統已儲存查詢不需要任何特殊權限。您可以在任何專案中儲存不公開的查詢，但只有您可以查看、更新或刪除該查詢。
* **專案層級**的傳統版已儲存查詢：
  + **建立**專案層級的傳統版已儲存的查詢需要擁有 `bigquery.savedqueries.create` 權限。`bigquery.admin` 這個預先定義的角色具備 `bigquery.savedqueries.create` 權限。
  + **查看**專案層級的傳統版已儲存的查詢需要擁有 `bigquery.savedqueries.get` 與 `bigquery.savedqueries.list` 權限。`bigquery.admin` 和 `bigquery.user` 這些預先定義的角色具備 `bigquery.savedqueries.get` 與 `bigquery.savedqueries.list` 權限。
  + **更新**專案層級的傳統版已儲存的查詢需要擁有 `bigquery.savedqueries.update` 權限。`bigquery.admin` 這個預先定義的角色具備 `bigquery.savedqueries.update` 權限。
  + **刪除**專案層級的傳統版已儲存的查詢需要擁有 `bigquery.savedqueries.delete` 權限。`bigquery.admin` 這個預先定義的角色具備 `bigquery.savedqueries.delete` 權限。
* **公開**的傳統版已儲存查詢：
  + 建立公開的傳統已儲存查詢不需要任何特殊權限。您可以在任何專案中儲存公開的傳統版已儲存的查詢，但只有您可以更新或刪除查詢。擁有連結的任何人都可查看公開的已儲存的傳統查詢。

**注意：** 在專案層級獲得 `dataform.repository.list` 權限的使用者，可以查看專案中建立的所有已儲存的查詢。

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 建立傳統版已儲存的查詢

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「SQL 查詢」add\_box。
3. 在查詢編輯器中輸入有效的 SQL 查詢。舉例來說，您可以查詢[公開資料集](https://cloud.google.com/bigquery/public-data?hl=zh-tw)：

   ```
   SELECT
     name,
     SUM(number) AS total
   FROM
     `bigquery-public-data.usa_names.usa_1910_2013`
   GROUP BY
     name
   ORDER BY
     total DESC
   LIMIT
     10;
   ```
4. 依序點按 「儲存查詢 (傳統版)」**>「儲存查詢 (傳統版)」**。
5. 在「Save query」(儲存查詢) 對話方塊中，輸入查詢的名稱，然後將「Visibility」(瀏覽權限) 設定為下列其中一個選項：

   * **個人 (只能由您編輯)**：適用於不公開的傳統版已儲存的查詢。
   * **專案 (可由具備適當權限的主體編輯)**，適用於專案層級的傳統版已儲存的查詢。
   * **公開**：傳統版已儲存的公開查詢。
6. 按一下 [儲存]。

### 共用傳統版已儲存的查詢

您可以共用已設為專案或公開瀏覽權限的傳統版已儲存查詢。專案層級瀏覽權限可讓具備[必要權限](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#required_permissions_for_classic_saved_queries)的主體檢視、更新或刪除查詢。公開瀏覽權限可讓擁有查詢連結的任何人查看查詢，但無法更新或刪除查詢。

如要與其他使用者共用傳統版已儲存的查詢，請產生並分享傳統版已儲存查詢的連結。

如要執行傳統共用查詢，使用者必須能存取查詢所存取的資料。詳情請參閱「[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)」。

如果您打算共用傳統版已儲存的查詢，請考慮在查詢中加入說明用途的註解。

1. 點選左側窗格中的「類別」「傳統版 Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「傳統版 Explorer」窗格中展開專案，按一下「(傳統版) 查詢」，然後找出要共用的傳統版已儲存的查詢。
3. 按一下查詢旁的 more\_vert「查看動作」，然後點選「取得連結」。
4. 將連結分享給要授予查詢存取權的使用者。

### 更新傳統版已儲存的查詢

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的「類別」「傳統版 Explorer」：
3. 在「傳統版 Explorer」窗格中，展開專案和「(傳統版) 查詢」資料夾，以及「專案查詢」資料夾 (如有需要)。
4. 按一下已儲存的傳統查詢名稱即可開啟。
5. 修改查詢。
6. 如要儲存修改後的查詢，請依序點按「儲存查詢 (傳統版)」**>「儲存查詢 (傳統版)」**。

## 後續步驟

* 瞭解如何[管理已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]