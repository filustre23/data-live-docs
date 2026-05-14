Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 bq 工具

在本教學課程中，您將瞭解如何使用 BigQuery 專用的 Python 指令列介面 (CLI) 工具 `bq` 建立資料集、載入範例資料，以及查詢資料表。完成本教學課程後，您將熟悉 `bq`，並瞭解如何使用 CLI 操作 BigQuery。

如需所有 `bq` 指令和標記的完整參考資料，請參閱 [bq 指令列工具參考資料](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw)。

---

如要直接在 Google Cloud 控制台中，按照這項工作的逐步指南操作，請按一下「Guide me」(逐步引導)：

[「Guide me」(逐步引導)](https://console.cloud.google.com/freetrial?redirectPath=%2F%3Fwalkthrough_id%3Dbigquery--load-data-bq&hl=zh-tw)

---

## 事前準備

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
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
- If you're using an existing project for this guide,
  [verify that you have
  the permissions required to complete this guide](#required_roles). If you created a new
  project, then you already have the required permissions.

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
- If you're using an existing project for this guide,
  [verify that you have
  the permissions required to complete this guide](#required_roles). If you created a new
  project, then you already have the required permissions.

1. 啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery&hl=zh-tw)

   新專案會自動啟用 BigQuery API。
2. 選用：
   [啟用專案的計費功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw)。如果您不想啟用帳單或提供信用卡，仍可按照本文步驟操作。BigQuery 提供沙箱，方便您執行這些步驟。詳情請參閱「[啟用 BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw#setup)」一文。
   **注意：**如果專案有帳單帳戶，且您想使用 BigQuery 沙箱，請[停用專案的帳單功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw#disable_billing_for_a_project)。

在 Google Cloud 控制台中啟用 Cloud Shell。

[啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

Google Cloud 主控台底部會開啟一個 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已針對您目前的專案設定好相關值。工作階段可能要幾秒鐘的時間才能初始化。

### 必要的角色

如要取得建立資料集、建立資料表、載入資料及查詢資料所需的權限，請要求管理員授予您專案的下列 IAM 角色：

* 執行載入工作和查詢工作：
  [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 建立資料集、建立資料表、將資料載入資料表，以及查詢資料表：
  [BigQuery 資料編輯器](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 下載含有來源資料的檔案

您下載的檔案包含約 7 MB 的熱門新生兒命名資料，這項資料是由美國社會安全局提供。

如要進一步瞭解資料，請參閱美國社會安全局的[熱門名字的背景資訊](http://www.ssa.gov/OACT/babynames/background.html)。

1. 在新的瀏覽器分頁中開啟下列網址，下載美國社會安全局的資料：

   ```
   https://www.ssa.gov/OACT/babynames/names.zip
   ```
2. 將檔案解壓縮。

   如要進一步瞭解資料集結構定義，請查看解壓縮後的 `NationalReadMe.pdf` 檔案。
3. 如要查看資料樣貌，請開啟 `yob2024.txt` 檔案。這個逗號分隔值檔案內含名字、出生時判定的性別，以及同名的新生兒人數，這個檔案沒有標題列。
4. 將該檔案移到工作目錄。

   * 如果使用 Cloud Shell，請依序點選 more\_vert「More」(顯示更多項目) >「Upload」(上傳)，按一下「Choose Files」(選擇檔案) 後再選取 `yob2024.txt` 檔案，最後點選「Upload」(上傳)。
   * 如果使用本機殼層，請將 `yob2024.txt` 檔案複製或移到執行 bq 工具的目錄。

## 建立資料集

1. 如果您是從說明文件啟動 Cloud Shell，請輸入下列指令來設定專案 ID，這樣就不必在每個 CLI 指令中指定專案 ID。

   ```
   gcloud config set project PROJECT_ID
   ```

   將 PROJECT\_ID 替換為您的專案 ID。

1. 輸入下列指令，建立資料集 `babynames`：

   ```
   bq mk --dataset babynames
   ```

   輸出結果大致如下：

   ```
   Dataset 'babynames' successfully created.
   ```
2. 確認資料集 `babynames` 已顯示於專案：

   ```
   bq ls --datasets=true
   ```

   輸出結果會與下列內容相似：

   ```
     datasetId
   -------------
     babynames
   ```

## 將資料載入資料表

1. 在 `babynames` 資料集中，將來源檔案 `yob2024.txt` 載入新資料表 `names2024`：

   ```
   bq load babynames.names2024 yob2024.txt name:string,assigned_sex_at_birth:string,count:integer
   ```

   輸出結果大致如下：

   ```
   Upload complete.
   Waiting on bqjob_r3c045d7cbe5ca6d2_0000018292f0815f_1 ... (1s) Current status: DONE
   ```
2. 確認資料表 `names2024` 已顯示於資料集 `babynames`：

   ```
   bq ls --format=pretty babynames
   ```

   輸出結果大致如下。某些資料欄會省略，用以簡化輸出內容。

   ```
   +-----------+-------+
   |  tableId  | Type  |
   +-----------+-------+
   | names2024 | TABLE |
   +-----------+-------+
   ```
3. 確認新資料表 `names2024` 的結構定義為 `name: string`、`assigned_sex_at_birth: string` 和 `count: integer`：

   ```
   bq show babynames.names2024
   ```

   輸出結果大致如下。某些資料欄會省略，用以簡化輸出內容。

   ```
     Last modified        Schema                      Total Rows   Total Bytes
   ----------------- ------------------------------- ------------ ------------
   14 Mar 17:16:45   |- name: string                    31904       607494
                     |- assigned_sex_at_birth: string
                     |- count: integer
   ```

## 查詢資料表資料

1. 判定資料中最常見的女生名字：

   ```
   bq query \
       'SELECT
         name,
         count
       FROM
         babynames.names2024
       WHERE
         assigned_sex_at_birth = "F"
       ORDER BY
         count DESC
       LIMIT 5'
   ```

   輸出結果大致如下：

   ```
   +-----------+-------+
   |   name    | count |
   +-----------+-------+
   | Olivia    | 14718 |
   | Emma      | 13485 |
   | Amelia    | 12740 |
   | Charlotte | 12552 |
   | Mia       | 12113 |
   +-----------+-------+
   ```
2. 判定資料中最少見的男生名字：

   ```
   bq query \
       'SELECT
         name,
         count
       FROM
         babynames.names2024
       WHERE
         assigned_sex_at_birth = "M"
       ORDER BY
         count ASC
       LIMIT 5'
   ```

   輸出結果大致如下：

   ```
   +---------+-------+
   |  name   | count |
   +---------+-------+
   | Aaran   |     5 |
   | Aadiv   |     5 |
   | Aadarsh |     5 |
   | Aarash  |     5 |
   | Aadrik  |     5 |
   +---------+-------+
   ```

   來源資料會省略出現少於 5 次的名字，因此最少次數是 5。

## 清除所用資源

為了避免系統向您的 Google Cloud 帳戶收取本頁面所用資源的費用，請刪除含有這些資源的 Google Cloud 專案。

### 刪除專案

如果您使用 [BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)查詢公開資料集，專案就不會啟用帳單功能，因此您不需要刪除專案。

如要避免付費，最簡單的方法就是刪除您為了本教學課程所建立的專案。

刪除專案的方法如下：

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### 刪除資源

如果使用現有專案，請刪除稍早建立的資源：

1. 刪除資料集 `babynames`：

   ```
   bq rm --recursive=true babynames
   ```

   旗標 `--recursive` 會刪除資料集內的所有資料表，包括資料表 `names2024`。

   輸出結果大致如下：

   ```
   rm: remove dataset 'myproject:babynames'? (y/N)
   ```
2. 輸入 `y` 來確認刪除指令。

## 後續步驟

* 瞭解 [BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)。
* 進一步瞭解如何[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)。
* 進一步瞭解如何[在 BigQuery 查詢資料](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]