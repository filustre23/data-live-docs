Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立已儲存的查詢

您可以將在查詢編輯器中編寫的 SQL 儲存為已儲存的查詢，並與其他使用者共用，讓團隊成員重複使用及協作查詢。已儲存的查詢是由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 提供的 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 程式碼資產。

如要進一步瞭解如何刪除已儲存的查詢，以及管理已儲存的查詢記錄，請參閱「[管理已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw)」。

## 所需權限

設定適當權限，以便建立、編輯或查看已儲存的查詢。

所有具備 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`) 的使用者，都擁有專案中建立的所有已儲存的查詢的擁有者存取權。

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 建立已儲存的查詢的權限

如要建立及執行已儲存的查詢，您必須具備下列 IAM 權限：

* `dataform.locations.get`
* `dataform.locations.list`
* `dataform.repositories.list`
* `dataform.repositories.create`

您可以透過下列 IAM 角色取得這些權限：

* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
* [程式碼建立者](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeCreator) (`roles/dataform.codeCreator`)

**注意：**在專案中獲派程式碼建立者角色的使用者，可以使用 Dataform API 或 Dataform 指令列介面 (CLI)，列出該專案中的程式碼資產名稱。**注意：**建立已儲存的查詢時，BigQuery 會授予您該查詢的 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。凡是具備 Google Cloud 專案 Dataform 管理員角色的使用者，都擁有該專案中所有已儲存的查詢的擁有者存取權。如要覆寫這項行為，請參閱「[在建立資源時授予特定角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-specific-role)」。

### 編輯已儲存的查詢的權限

如要編輯及執行已儲存的查詢，您需要下列 IAM 角色：

* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
* [程式碼編輯器](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor) (`roles/dataform.codeEditor`)

### 具備查看已儲存的查詢的權限

如要查看及執行已儲存的查詢，您必須具備下列 IAM 角色：

* [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
* [程式碼檢視者](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer) (`roles/dataform.codeViewer`)

### 已儲存的查詢的安全性考量

BigQuery 中的程式碼資產是由 Dataform 提供，因此請考量下列安全性影響，再授予使用者這些資產的存取權：

* 程式碼資產的瀏覽權限由專案層級的 Dataform 權限控管。使用者只要具備 `dataform.repositories.list` 權限 (包含在標準 BigQuery 角色中，例如 [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)、[BigQuery Studio 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser)和 [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user))，就能在 Google Cloud 專案的「Explorer」面板中查看所有程式碼資產，無論這些資產是否由他們建立或與他們共用。如要限制瀏覽權限，可以建立不含 `dataform.repositories.list` 權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。
* 凡是與 Dataform 服務代理共用的 Secret，可編輯這些資產的使用者都有可能存取。為確保憑證安全，請限制只有信任的使用者才能建立及編輯權限，並限制 Dataform 服務代理可存取的密鑰。詳情請參閱「[在套件安裝期間存取 Secret](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#secret-access-risk)」。

詳情請參閱「[Dataform 權限的安全性考量](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#security-considerations-permissions)」。

## 設定程式碼資產的預設區域

Google Cloud 專案中的所有新程式碼資產都會使用預設區域。資產建立後，就無法變更區域。

**重要事項：** 如果在建立程式碼資產時變更區域，該區域會成為後續所有程式碼資產的預設區域。現有程式碼資產不受影響。

如要設定新程式碼資產的預設區域，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder Files」(檔案)，開啟檔案瀏覽器：
3. 按一下專案名稱旁的 more\_vert「View files panel actions」(查看檔案面板動作) >「Switch code region」(切換程式碼區域)。
4. 選取要設為預設值的程式碼區域。
5. 按一下 [儲存]。

如要查看支援的地區清單，請參閱「[BigQuery Studio 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqstudio-loc)」。

## 使用 CMEK 加密

您可以使用 Dataform API 的預設專案層級 CMEK 金鑰，以客戶自行管理的加密金鑰 (CMEK) 加密 Dataform 支援的已儲存的查詢。您無法在 Google Cloud 控制台中，將個別 CMEK 金鑰套用至已儲存的查詢。新設定只會套用至新建立的已儲存的查詢。

如要進一步瞭解及查看設定預設金鑰的操作說明，請參閱「[使用 CMEK 保護 BigQuery Studio 程式碼資產](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#cmek-studio)」。

## 建立已儲存的查詢

如要建立已儲存的查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「add\_box SQL 查詢」。
3. 在查詢編輯器中輸入有效的 SQL 查詢。例如，您可以查詢[公開資料集](https://cloud.google.com/bigquery/public-data?hl=zh-tw)：

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

   或者，您也可以使用「**Reference**」面板建構新查詢。
4. 按一下「
   **儲存」>「已儲存的查詢」**，或按下 `Control+S` 鍵 (macOS 則為 `Command+S` 鍵)。
5. 在「儲存查詢」對話方塊中，輸入已儲存的查詢的名稱。
6. 選用：如要變更這項已儲存的查詢和日後所有其他程式碼資產使用的區域，請在「Region」(區域) 欄位中選取新區域。
7. 按一下 [儲存]。

   系統會建立已儲存的查詢的第一個版本。
8. 選用：儲存查詢後，您可以使用下列工具列查看查詢詳細資料或[版本記錄](#open_a_saved_query_version_as_a_new_query)、新增註解、回覆現有註解，或取得現有註解的連結：

   「Comments」(註解) 工具列功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。如要提供意見或尋求支援，請傳送電子郵件至 [bqui-workspace-pod@google.com](mailto:bqui-workspace-pod@google.com)。

## 共用已儲存的查詢

如要與使用者共用已儲存的查詢，請先授予該使用者已儲存查詢的存取權，並將其新增至適當的 IAM 角色。接著，您會產生已儲存的查詢的連結，並與使用者共用該連結。

與您共用查詢的使用者只能看到最新版本的查詢。自動儲存但未明確儲存的變更不會顯示在共用查詢中。

如要分享已儲存的查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下 folder「Files」(檔案)，開啟檔案瀏覽器。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Files」(檔案) 窗格中，展開專案和子資料夾，找出要共用的已儲存的查詢。
4. 按一下已儲存的查詢旁的 more\_vert「View actions」(查看動作)，然後依序點選「Share」(共用) >「Manage permissions」(管理權限)。
5. 在「管理權限」窗格中，按一下「新增使用者/群組」。
6. 在「New principals」(新增主體) 欄位中輸入主體。
7. 在「Role」(角色) 清單中，選取下列其中一個角色：

   * [**程式碼擁有者**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner)：可對已儲存的查詢執行任何動作，包括刪除或共用。
   * [**程式碼編輯器**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeEditor)：可以編輯查詢。
   * [**程式碼檢視者**](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeViewer)：可以查看查詢。**注意：** 主體也必須具備 [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user) 角色，才能執行已儲存的查詢。
8. 選用：如要查看完整的角色清單和進階共用設定，請按一下「Advanced sharing」(進階共用)。
9. 按一下 [儲存]。
10. 如要返回已儲存的查詢詳細資料，請按一下「Close」(關閉)。
11. 如要產生已儲存的查詢連結，請依序點選 more\_vert「View actions」(查看動作) >「Share」(共用) >「Copy link」(複製連結)。

    連結會複製到剪貼簿。

## 將已儲存的查詢版本開啟為新查詢

如要將現有已儲存查詢的任何版本開啟為新查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder Files」(檔案)，開啟檔案瀏覽器：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Files」(檔案) 窗格中，展開專案和子資料夾，找出要開啟的已儲存的查詢。
4. 按一下已儲存的查詢，然後點選「history 版本記錄」。
5. 按一下已儲存的查詢版本旁的 more\_vert「View actions」(查看動作)，然後點選「Open as new query」(以新查詢開啟)。

## 更新已儲存的查詢

停止輸入兩秒後，系統會自動儲存您對已儲存的查詢文字所做的變更，並在「版本記錄」 中顯示為「您的變更」。自動儲存的變更不會成為查詢的新版本。每次開啟查詢時，系統都會顯示自動儲存的變更，但除非您明確將變更儲存為查詢的新[版本](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#work_with_saved_query_versions)，否則其他人都看不到這些變更。自動儲存查詢功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder Files」(檔案)，開啟檔案瀏覽器：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Files」(檔案) 窗格中，展開專案和子資料夾，找出要更新的已儲存的查詢。
4. 按一下已儲存的查詢即可開啟。
5. 修改查詢。
6. 如要儲存修改後的查詢，請依序點選
   **「Save query」(儲存查詢) >「Save query」(儲存查詢)**
   ，或按下 `Control+S` 鍵 (在 macOS 上為 `Command+S` 鍵)。

   系統會建立新版查詢。

## 上傳已儲存的查詢

您可以上傳本機 SQL 查詢，在 BigQuery Studio 中做為已儲存的查詢使用。上傳的已儲存的查詢也會顯示在 Google Cloud 控制台的 BigQuery 頁面中。

如要上傳已儲存的查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder Files」(檔案)，開啟檔案瀏覽器：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Files」(檔案) 窗格中，找到要上傳查詢的資料夾，點選旁邊的 more\_vert「View actions」(查看動作)，然後依序點選「Upload」(上傳) >「Query」(查詢)。
4. 在「Upload SQL」(上傳 SQL) 對話方塊的「SQL」欄位中，按一下「Browse」(瀏覽)，然後選取要上傳的查詢。
5. 選用：在「SQL name」(SQL 名稱) 欄位中，編輯查詢名稱。
6. 在「Region」(區域) 欄位中，選取要上傳已儲存的查詢的區域。
7. 按一下「上傳」。

您可以透過「檔案」或「Explorer」窗格存取已儲存的查詢。

## 排解已儲存查詢的問題

本節說明如何解決已儲存的查詢的常見問題。

### 無法儲存查詢

如果無法儲存查詢，可能是因為專案未啟用 Dataform API。大多數專案會自動啟用 Dataform API，但如果專案使用[限制資源服務用量](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-resources?hl=zh-tw)組織政策限制 (例如[安全專案](https://docs.cloud.google.com/assured-workloads/docs/concepts?hl=zh-tw))，則不會啟用。

如要解決這個問題，請確認 Dataform API 已啟用：

1. 在 Google Cloud 控制台中，前往「APIs & Services」(API 與服務) 頁面。
2. 搜尋 **Dataform API**，確認已啟用。
3. 如果 API 尚未啟用，請點選「啟用」。
4. 請使用已儲存的查詢重試。

### 已儲存的查詢的區域不符

變更[程式碼資產的預設區域](#set-the-default-region-for-code-assets)，只會影響變更後建立的資產。現有資產會保留在[原始區域](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#supported_regions)。

如要解決這個問題，請確保為已儲存查詢選取的區域符合其中一個支援的區域。如有需要，請在支援的區域建立新的已儲存查詢，或調整程式碼資產的預設區域。

## 傳統版已儲存的查詢

**已淘汰：** [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/enable-assets?hl=zh-tw) 中的已儲存查詢，日後將全面取代傳統已儲存查詢。我們正在審查淘汰時程。
詳情請參閱「[淘汰傳統版已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#classic-saved-queries-deprecation)」。如要瞭解如何遷移至已儲存的查詢，請參閱「[遷移傳統版已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#migrate_classic_saved_queries)」。

請參閱下列各節，瞭解如何建立及更新[傳統已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw#classic_saved_queries)。如要進一步瞭解如何共用、遷移及刪除傳統版已儲存的查詢，請參閱「[傳統版已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#classic_saved_queries)」。

**注意：** 如果您尚未啟用 BigQuery Studio，傳統已儲存的查詢會顯示在「**Explorer**」窗格的「**Saved queries (NUMBER)**」資料夾中，而非「**(Classic) Queries**」資料夾。

### 傳統版已儲存的查詢的必要權限

如要建立、查看、更新及刪除傳統版已儲存的查詢，必須具備下列 IAM 權限：

* **私人**傳統版已儲存的查詢：
  + 建立私人傳統版已儲存的查詢不需要特殊權限。您可以在任何專案中儲存私人查詢，但只有您能查看、更新或刪除該查詢。
* **專案層級**傳統版已儲存的查詢：
  + 如要**建立**專案層級的傳統版已儲存的查詢，必須具備 `bigquery.savedqueries.create` 權限。`bigquery.admin` 這個預先定義的角色具備 `bigquery.savedqueries.create` 權限。
  + 如要**查看**專案層級的傳統版已儲存的查詢，必須具備 `bigquery.savedqueries.get` 和 `bigquery.savedqueries.list` 權限。`bigquery.admin` 和 `bigquery.user` 這些預先定義的角色具備 `bigquery.savedqueries.get` 與 `bigquery.savedqueries.list` 權限。
  + 如要**更新**專案層級的傳統版已儲存的查詢，必須具備 `bigquery.savedqueries.update` 權限。`bigquery.admin` 這個預先定義的角色具備 `bigquery.savedqueries.update` 權限。
  + 如要**刪除**專案層級的傳統版已儲存的查詢，必須具備 `bigquery.savedqueries.delete` 權限。`bigquery.admin` 這個預先定義的角色具備 `bigquery.savedqueries.delete` 權限。
* **公開**傳統版已儲存的查詢：
  + 建立公開的傳統版已儲存的查詢不需要特殊權限。您可以在任何專案中儲存公開的傳統版已儲存查詢，但只有您能更新或刪除該查詢。任何知道連結的使用者，都能查看公開的傳統版已儲存的查詢。

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 建立傳統版已儲存的查詢

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「add\_box SQL 查詢」。
3. 在查詢編輯器中輸入有效的 SQL 查詢。例如，您可以查詢[公開資料集](https://cloud.google.com/bigquery/public-data?hl=zh-tw)：

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
4. 依序點選**「 儲存查詢 (傳統版)」 > 「儲存查詢 (傳統版)」**。
5. 在「Save query」(儲存查詢) 對話方塊中，輸入查詢名稱，然後將「Visibility」(瀏覽權限) 設為下列其中一個選項：

   * **個人 (只能由您編輯)**：私人傳統版已儲存的查詢。
   * 專案層級傳統版已儲存的查詢：**專案 (可由具備適當權限的主體編輯)**。
   * **Public**：公開的傳統版已儲存的查詢。
6. 按一下 [儲存]。

### 共用傳統版已儲存的查詢

您可以共用已設為專案或公開瀏覽權限的傳統版已儲存的查詢。具備[必要權限](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#required_permissions_for_classic_saved_queries)的主體可以查看、更新或刪除查詢。公開瀏覽權限可讓任何擁有查詢連結的使用者查看查詢，但無法更新或刪除。

如要與其他使用者共用傳統版已儲存的查詢，請產生並分享傳統版已儲存查詢的連結。

如要執行傳統共用查詢，使用者必須有權存取查詢存取的資料。詳情請參閱「[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_dataset)」。

如果您打算共用傳統版已儲存的查詢，建議在查詢中加入註解，說明查詢用途。

如要共用傳統版已儲存的查詢，請按照下列步驟操作：

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「Explorer」窗格中展開專案，然後按一下「(傳統版) 查詢」。
3. 找出並點選要授予存取權的傳統版已儲存的查詢。您可以使用搜尋功能或篩選器找出查詢。
4. 按一下查詢旁的 more\_vert「View actions」(查看動作)，然後點選「Copy link」(複製連結)。
5. 將連結分享給要授予查詢存取權的使用者。

### 更新傳統版已儲存的查詢

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，依序展開專案和「(傳統版) 查詢」資料夾，如有需要，也請展開「專案查詢」資料夾。
4. 按一下傳統版已儲存的查詢名稱，即可開啟查詢。
5. 修改查詢。
6. 如要儲存修改後的查詢，請依序點選
   **「Save Query (Classic)」(儲存查詢 (傳統版)) >「Save query (Classic)」(儲存查詢 (傳統版))**。

### 排解傳統版已儲存查詢的問題

本節說明如何解決傳統版已儲存的查詢的常見問題。

#### 無法存取已停用使用者的已儲存的查詢

BigQuery Studio 已儲存的查詢可由專案管理員存取，但如果建立私人傳統已儲存查詢的使用者已離開組織，且其 Google 帳戶已停用或停權，則無法存取這些查詢。除了原始擁有者外，所有使用者的 Google Cloud 控制台都不會再顯示這些查詢。

如要復原這些查詢，Google Workspace 或 Cloud Identity 管理員必須執行下列步驟：

1. 暫時重新啟用已停用的使用者帳戶。
2. 重設使用者密碼。
3. 以重新啟用的使用者身分登入 Google Cloud 控制台。
4. 在查詢編輯器中，開啟各項已儲存的查詢。
5. 按一下「儲存」或「將查詢另存為」。
6. 將「瀏覽權限」從「個人」變更為「專案」。
7. 按一下 [儲存]。這樣一來，同一專案中具備必要權限的其他使用者就能查看查詢。
8. 所有查詢都遷移完畢後，請重新將使用者帳戶停權。

為避免發生這個問題，請將業務關鍵或團隊共用的查詢儲存為「Project」(專案) 瀏覽權限。

## 後續步驟

* 瞭解如何[管理已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]