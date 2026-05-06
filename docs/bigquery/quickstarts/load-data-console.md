Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 載入及查詢資料

如要開始使用 BigQuery，請建立資料集、將資料載入資料表，並查詢資料表。

---

如要直接在 Google Cloud 控制台中，按照這項工作的逐步指南操作，請按一下「Guide me」(逐步引導)：

[「Guide me」(逐步引導)](https://console.cloud.google.com/freetrial?redirectPath=%2F%3Fwalkthrough_id%3Dbigquery--bigquery-quickstart-load-data-console&hl=zh-tw)

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

### 必要的角色

如要取得建立資料集、建立資料表、載入資料及查詢資料所需的權限，請要求管理員授予您專案的下列 IAM 角色：

* 執行載入工作和查詢工作：
  [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 建立資料集、建立資料表、將資料載入資料表，以及查詢資料表：
  [BigQuery 資料編輯器](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立 BigQuery 資料集

透過 Google Cloud 控制台在美國多區域位置建立資料集來儲存資料。如要瞭解 BigQuery 單一地區與多地區，請參閱[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)的相關說明。

1. 在 Google Cloud 控制台開啟 BigQuery 頁面。
[前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格，點按專案名稱。
4. 按一下 more\_vert
   「查看動作」。
5. 選取「Create dataset」(建立資料集)。
6. 在「建立資料集」頁面中，執行下列操作：

1. 在「Dataset ID」(資料集 ID) 中輸入 `babynames`。
2. 針對「Location type」(位置類型) 選取「Multi-region」(多區域)，然後選擇「US (multiple regions in United States)」(us (多個美國區域))。公開資料集存放在 `us` 多區域位置。為簡單起見，請將資料集儲存在相同位置。
3. 其餘設定請保留預設狀態，然後按一下「Create dataset」(建立資料集)。

## 下載含有來源資料的檔案

您下載的檔案包含約 7 MB 的熱門新生兒命名資料，這項資料是由美國社會安全局提供。

如要進一步瞭解資料，請參閱美國社會安全局的[熱門名字的背景資訊](http://www.ssa.gov/OACT/babynames/background.html)。

1. 在新的瀏覽器分頁中開啟下列網址，下載美國社會安全局的資料：

   ```
   https://www.ssa.gov/OACT/babynames/names.zip
   ```
2. 將檔案解壓縮。

   如要進一步瞭解資料集結構定義，請參閱 ZIP 檔案中的 `NationalReadMe.pdf` 檔案。
3. 如要查看資料樣貌，請開啟 `yob2024.txt` 檔案。這個逗號分隔值檔案內含名字、出生時判定的性別，以及同名的新生兒人數，這個檔案沒有標題列。
4. 請記下 `yob2024.txt` 檔的位置，以便稍後尋找。

## 將資料載入資料表

接著，將資料載入新資料表。

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格，展開專案名稱。
3. 按一下「資料集」，然後在「babynames」資料集旁邊，依序點按 more\_vert「查看動作」和「開啟」。
4. 按一下 add\_box「建立資料表」。

   除非另有指示，否則請保留所有設定的預設值。
5. 在「建立資料表」頁面中，執行下列操作：

1. 在「Source」(來源) 專區中，從「Create table from」(建立資料表來源) 的清單中選擇「Upload」(上傳)。
2. 在「Select file」(選取檔案) 欄位，點按「Browse」(瀏覽)。
3. 找到並開啟本機中的 `yob2024.txt` 檔案，然後點按「Open」(開啟)。
4. 從「File format」(檔案格式) 清單選擇「CSV」。
5. 在「Destination」(目的地) 專區的「Table」(資料表) 欄位，輸入 `names_2024`。
6. 在「Schema」(結構定義) 專區，點按「Edit as text」(以文字形式編輯) 切換按鈕，然後將下列結構定義貼入文字欄位：

```
name:string,assigned_sex_at_birth:string,count:integer
```

7. 點按「Create table」(建立資料表)。

   等待 BigQuery 建立資料表及載入資料。

## 預覽資料表資料

如要預覽資料表資料，請按照下列步驟操作：

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)。
3. 按一下「`babynames`」資料集，然後選取「`names_2024`」資料表。
4. 點按「Preview」(預覽) 分頁標籤，BigQuery 會顯示資料表的前幾個資料列。

並非所有資料表類型都能使用「預覽」分頁。舉例來說，外部資料表或檢視畫面不會顯示「預覽」分頁。

## 查詢資料表資料

接著是查詢資料表。

1. 在「names\_2024」分頁旁邊，按一下 add\_box「SQL 查詢」選項。系統會開啟新的編輯器分頁。
2. 將下列查詢貼入查詢編輯器，這項查詢會擷取 2024 年在美國出生，且當判定為男性的前五名熱門男嬰名字。  

   ```
     SELECT
       name,
       count
     FROM
       `babynames.names_2024`
     WHERE
       assigned_sex_at_birth = 'M'
     ORDER BY
       count DESC
     LIMIT
       5;
   ```
3. 按一下「Run」(執行)。
   查詢結果會顯示在「Query results」(查詢結果) 部分中。

您已成功使用 Google Cloud 控制台查詢公開資料集內的資料表，並將範例資料載入 BigQuery。

## 清除所用資源

為了避免系統向您的 Google Cloud 帳戶收取本頁面所用資源的費用，請按照下列步驟操作。

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。
[前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，按一下「Datasets」(資料集)，然後點選您建立的 `babynames` 資料集。
4. 展開 more\_vert「查看動作」選項，然後點按「刪除」。
5. 在「Delete dataset」(刪除資料集) 對話方塊中，確認刪除指令：輸入字詞 `delete`，然後按一下「Delete」(刪除)。

## 後續步驟

* 如要進一步瞭解如何將資料載入至 BigQuery，請參閱「[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」一文。
* 如要進一步瞭解如何查詢資料，請參閱「[BigQuery 數據分析總覽](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)」一文。
* 如要瞭解如何使用巢狀和重複的資料載入 JSON 檔案，請參閱[載入巢狀和重複的 JSON 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#loading_nested_and_repeated_json_data)。
* 如要進一步瞭解如何透過程式存取 BigQuery，請參閱 [REST API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2?hl=zh-tw) 參考資料，或前往 [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)頁面。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]