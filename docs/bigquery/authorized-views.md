* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 授權檢視表

本文說明如何在 BigQuery 中建立授權檢視表和授權具體化檢視表。資料管理員可以建立*授權 view*，與特定使用者和群組 (主體) 分享資料集中的部分資料。主體可以查看您分享的資料並對其執行查詢，但無法直接存取來源資料集。

### 查看類型

邏輯檢視表是 BigQuery 的預設檢視表類型，而具體化檢視表是預先運算的檢視表，會定期快取查詢結果，以提高效能和效率。

邏輯檢視表的授權檢視表稱為授權檢視表，但具體化檢視表的授權檢視表稱為*授權具體化檢視表*。

如果邏輯檢視區塊依賴[大型或運算成本高昂的查詢](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#use_cases)，則可以改為建立具體化檢視區塊。如要瞭解邏輯檢視表和具體化檢視表的用途，請參閱「[邏輯檢視表和具體化檢視表總覽](https://docs.cloud.google.com/bigquery/docs/logical-materialized-view-overview?hl=zh-tw)」。

### 建立授權檢視表的高階步驟

如要建立及共用檢視區塊，請參閱下列高階步驟，這些步驟適用於授權邏輯檢視區塊和授權具體化檢視區塊。

**注意：** 您也可以[共用資料集中的所有檢視畫面](#share-all-views)。

* 建立資料集，以便加入來源資料。
* 執行查詢，將資料載入來源資料集中的目的地資料表。
* 建立資料集，以便加入授權 view。
* 從 SQL 查詢建立授權 view，限制資料分析師可在查詢結果中查看的資料欄。
* 授予資料分析師執行查詢工作的權限。
* 授予資料分析師對內含已授權檢視表的資料集存取權。
* 將來源資料集的檢視權限授予已授權的檢視表。

## 替代方案

雖然授權檢視畫面具有彈性且可擴充，但下列其中一種方法可能更適合您的用途：

* 在資料表上設定資料列層級政策。
* 在資料表上設定資料欄層級的政策。
* 將資料儲存在不同的資料表中。
* 分享資料集中的所有檢視表 (授權資料集)。

### 使用資料列層級或資料欄層級安全性，或使用不同的資料表

資料管理員可以在資料表上設定資料列層級的存取權政策，或建立個別資料表來存放機密資料，藉此限制使用者查看該資料的權限。將資料儲存在另一個資料表中會隔離資料，並移除查看資料表中有多少資料列的功能。

此外，資料管理員可以建立及套用政策標記，限制使用者查看資料表中的資料欄。

將資料儲存在獨立資料表中是最安全的方法，但彈性最低。設定資料列層級政策既彈性又安全，而共用授權檢視畫面既彈性又可提供最佳效能。

如要詳細比較這些方法，請參閱下列資源：

* [授權檢視表、資料列層級安全性和個別資料表比較](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw#comparison_of_authorized_views_row-level_security_and_separate_tables)
* [資料列層級安全性簡介](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)
* [資料列層級安全性的用途示例](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw#example_use_cases)
* [資料欄層級存取控管機制簡介](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)

### 共用資料集中的所有檢視畫面

如要授予檢視表集合資料集的存取權，不必逐一授權每個檢視表，可以將檢視表歸入資料集，然後授予包含檢視表的資料集存取包含資料的資料集。

然後視需要授予主體權限，存取含有檢視群組的資料集，或資料集中的個別檢視畫面。可存取其他資料集的資料集稱為「授權資料集」。授權其他資料集存取資料的資料集稱為「共用資料集」。

資料集的存取控制清單最多可有 2,500 個授權資源，包括[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)、[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)和[授權函式](https://docs.cloud.google.com/bigquery/docs/authorized-functions?hl=zh-tw)。
如果授權檢視區塊數量過多而超出上限，建議將檢視區塊分組到授權資料集中。設計新的 BigQuery 架構 (尤其是多租戶架構) 時，建議將相關檢視區塊分組到授權資料集中。

詳情請參閱「[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)」和「[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw#authorize_a_dataset)」。

## 限制

* 在其他資料集中建立授權檢視表或具體化檢視表時，來源資料集和授權檢視表資料集必須位於相同的區域[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
* 刪除授權 view 後，系統最多可能需要 24 小時，才會從檢視表清單中移除該授權 view。這段期間您無法存取已授權的檢視表，但已刪除的已授權檢視表可能會出現在檢視表清單中，並計入[已授權檢視表上限](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#dataset_limits)。如果新的授權 view 會超出這項限制，系統就會禁止建立額外的授權 view。

## 事前準備

[授予身分與存取權管理 (IAM) 角色](#required_permissions)，讓使用者具備必要權限，可查詢您分享的授權檢視區塊或授權具體化檢視區塊。

### 授權檢視區塊和 VPC Service Controls

在 VPC Service Controls 範圍內使用已授權檢視表時，允許主體存取內含檢視表的專案的輸入規則，也必須允許存取內含來源資料的任何專案，檢視表會從這些專案存取資料。主體不需要來源資料專案的 Identity and Access Management 權限，但除了包含檢視區塊的專案外，輸入規則也必須允許存取資料來源專案中的 BigQuery。

### 必要的角色

如要建立或更新授權檢視表，您必須具備該檢視表所屬資料集的權限，以及提供該檢視表存取權的資料集的權限。

此外，您還需要授予使用者或群組專案和資料集的存取權，才能存取檢視區塊。

**注意：** 除非您是資料擁有者，否則無法變更授權檢視區塊的 SQL 查詢。

#### 包含檢視表的資料集管理員權限

BigQuery 會將檢視表視為資料表資源，因此建立檢視表需要的權限和建立資料表相同。您還需擁有檢視表 SQL 查詢所參照的資料表查詢權限。

如要建立資料檢視，您需要 `bigquery.tables.create` IAM 權限。`roles/bigquery.dataEditor` 預先定義的 IAM 角色包含建立檢視區塊所需的權限。

此外，如果您具備 `bigquery.datasets.create` 權限，可以在您建立的資料集中建立檢視區塊。如要為不屬於您的資料建立檢視區塊，您必須具備該資料表的 `bigquery.tables.getData` 權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

#### 第二個資料集的管理員權限，可授予檢視表存取權

如要更新資料集屬性，您需要下列 IAM 權限：

* `bigquery.datasets.update`
* `bigquery.datasets.setIamPolicy` (僅在 Google Cloud 控制台中更新資料集存取權控管設定時需要)

`roles/bigquery.dataOwner` 預先定義的 IAM 角色包含更新資料集屬性所需的權限。

此外，如果您具備 `bigquery.datasets.create` 權限，可以更新所建立資料集的屬性。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

#### 專案和資料集的檢視權限

如要與使用者或群組共用授權檢視，您必須授予使用者或群組下列 IAM 權限：

* 專案的 `roles/bigquery.jobUser` IAM 角色，其中包含授權 view。這個角色會授予 `bigquery.jobs.create` 權限，這是對檢視區執行查詢工作時的必要權限。
* 包含授權 view 的資料集的 `roles/bigquery.dataViewer` IAM 角色。這個角色會授予 `bigquery.tables.getData`，這是查詢檢視區塊的必要權限。

## 使用授權 view

以下各節說明如何使用授權檢視區塊和授權具體化檢視區塊。

### 建立授權檢視表

如要建立授權 view，請選擇下列其中一個選項。如需授權、共用及刪除授權 view 的完整步驟，請參閱「[建立授權 view](https://docs.cloud.google.com/bigquery/docs/create-authorized-views?hl=zh-tw)」教學課程。

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，輸入要用來建立授權 view 的查詢。
3. 依序點選「儲存」>「儲存檢視畫面」。
4. 在「Save view」(儲存檢視表) 對話方塊中，執行下列操作：

   1. 在「Project」(專案) 部分，輸入要儲存檢視表的專案。
   2. 在「Dataset」(資料集) 部分，輸入要儲存檢視表的資料集。這個資料集必須與來源查詢中使用的資料集不同。
   3. 在「Table」(資料表) 部分，輸入檢視表的名稱。
   4. 按一下 [儲存]。
5. 授予可使用授權 view 的使用者[必要權限](#user_permissions_on_the_project_and_dataset_for_the_view)。
6. 在「Explorer」窗格中，選取來源查詢中使用的資料集。
7. 在「詳細資料」窗格中，依序點選「共用」>「授權檢視」。
8. 在「Authorized views」(授權 view) 窗格中，為「Authorized view」(授權 view) 輸入檢視表的完整名稱，格式為 PROJECT\_ID.DATASET\_ID.VIEW\_NAME。
9. 按一下「新增授權」。

### Terraform

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，請務必啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

```
# Creates an authorized view.

# Create a dataset to contain the view.
resource "google_bigquery_dataset" "view_dataset" {
  dataset_id  = "view_dataset"
  description = "Dataset that contains the view"
  location    = "us-west1"
}

# Create the view to authorize.
resource "google_bigquery_table" "movie_view" {
  project     = google_bigquery_dataset.view_dataset.project
  dataset_id  = google_bigquery_dataset.view_dataset.dataset_id
  table_id    = "movie_view"
  description = "View to authorize"

  view {
    query          = "SELECT item_id, avg(rating) FROM `movie_project.movie_dataset.movie_ratings` GROUP BY item_id ORDER BY item_id;"
    use_legacy_sql = false
  }
}


# Authorize the view to access the dataset
# that the query data originates from.
resource "google_bigquery_dataset_access" "view_authorization" {
  project    = "movie_project"
  dataset_id = "movie_dataset"

  view {
    project_id = google_bigquery_table.movie_view.project
    dataset_id = google_bigquery_table.movie_view.dataset_id
    table_id   = google_bigquery_table.movie_view.table_id
  }
}

# Specify the IAM policy for principals that can access
# the authorized view. These users should already
# have the roles/bigqueryUser role at the project level.
data "google_iam_policy" "principals_policy" {
  binding {
    role = "roles/bigquery.dataViewer"
    members = [
      "group:example-group@example.com",
    ]
  }
}

# Set the IAM policy on the authorized  view.
resource "google_bigquery_table_iam_policy" "authorized_view_policy" {
  project     = google_bigquery_table.movie_view.project
  dataset_id  = google_bigquery_table.movie_view.dataset_id
  table_id    = google_bigquery_table.movie_view.table_id
  policy_data = data.google_iam_policy.principals_policy.policy_data
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 程式碼片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 檢查設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### 管理授權檢視區塊的使用者或群組

授權檢視畫面後，您可以為資料集、資料表或檢視畫面完成下列工作，維持存取權：

* 查看存取權政策。
* 授予存取權。
* 撤銷存取權。
* 拒絕存取。

詳情請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

### 移除資料檢視的授權

**注意：** 移除檢視區塊後，請等待 24 小時再重複使用該檢視區塊名稱，或使用不重複的名稱。詳情請參閱「[配額與限制](#quotas_and_limits)」。

如要移除檢視區塊的授權，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 依序點選「總覽」**>「表格」**，然後選取所需表格。
5. 依序點選「共用」person\_add>「授權檢視」。
6. 按一下 delete 即可**移除授權**。
7. 按一下 [關閉]。

### bq

如要移除檢視區塊的授權，請使用 `bq rm` 指令。輸入要移除授權的檢視表 `table_id`。

```
    bq rm \
    project_id:dataset:table_id
```

### API

呼叫 [`tables.delete`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete?hl=zh-tw) 方法，並使用 `projectID`、`datasetID` 和 `tableID` 屬性移除資料集的授權 view。詳情請參閱「[資料表](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)」。

## 配額與限制

* 授權檢視表會受到資料集限制。詳情請參閱「[資料集限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#dataset_limits)」。
* 移除授權檢視後，系統最多可能需要 24 小時，才會移除所有檢視參照。為避免發生錯誤，請等待 24 小時再重新使用已移除的資料檢視名稱，或為資料檢視建立專屬名稱。

## 進階主題

以下各節說明授權檢視區塊的進階使用方法。

### 結合資料列層級安全防護機制與授權檢視畫面

系統會根據基礎來源資料表的資料列層級存取權政策，篩選邏輯檢視或具體化檢視中顯示的資料。

如要瞭解資料列層級安全防護機制與具體化檢視表的互動方式，請參閱「[將資料列層級的安全性與其他 BigQuery 功能搭配使用](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#logical_materialized_and_authorized_views)」。

### 結合資料欄層級安全防護機制與授權檢視畫面

資料欄層級安全性對檢視區的影響，與檢視區是否為授權檢視區無關。

如要詳細瞭解權限的套用方式，請參閱「[查詢檢視區塊](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw#views)」一文，瞭解資料欄層級的安全性。

### 使用 BigQuery sharing 搭配授權檢視表

BigQuery sharing (舊稱 Analytics Hub) 是資料交換平台，提供下列功能：

* 讓您跨機構界線大規模分享資料和洞察資訊。
* 採用完善的安全和隱私權架構。
* 支援將 BigQuery 資料集 (稱為「共用資料集」) 及其相關聯的授權檢視表和授權資料集發布給一組訂閱者。

*連結的資料集*是唯讀 BigQuery 資料集，做為共用資料集的指標或參照。訂閱共用*產品資訊*會在專案中建立連結的資料集，但不會複製資料集，因此訂閱者可以讀取資料，但無法新增或更新其中的物件。

系統[不支援](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#limitations)參照連結資料集中資料表的具體化檢視表。

詳情請參閱「[共用簡介](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)」。

## 後續步驟

* 如需建立授權檢視表的教學課程，請參閱[建立授權檢視表](https://docs.cloud.google.com/bigquery/docs/create-authorized-views?hl=zh-tw)。
* 如要建立邏輯檢視區塊，請參閱「[建立邏輯檢視區塊](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)」。
* 如要建立支援其他類型存取控管的具體化檢視表，請參閱「[建立具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#access_control)」。
* 如要取得檢視表中繼資料，請參閱[取得檢視表相關資訊](https://docs.cloud.google.com/bigquery/docs/view-metadata?hl=zh-tw)一文。
* 如要管理檢視畫面，請參閱「[管理檢視畫面](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]