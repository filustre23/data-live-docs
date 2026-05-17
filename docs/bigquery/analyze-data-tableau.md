Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BI Engine 和 Tableau Desktop 分析資料

BigQuery BI Engine 可讓您執行快速的低延遲分析服務，並透過 BigQuery 支援的報表和資訊主頁進行互動式分析。

本入門教學課程適用於使用商業智慧 (BI) 工具 Tableau Desktop 建構報表和資訊主頁的資料分析師和業務分析師。

## 目標

在本教學課程中，您將完成下列工作：

* 建立資料集並複製資料。
* 使用 Google Cloud 控制台建立 BI 預留項目並新增容量。
* 使用 Tableau Desktop 連線至由 BI Engine 管理的 BigQuery 資料表。
* 使用 Tableau Desktop 建立資訊主頁。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* [BigQuery](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw)
* [BI Engine](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#bi-engine-pricing)

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

完成本文所述工作後，您可以刪除建立的資源，避免繼續計費，詳情請參閱「[清除所用資源](#clean-up)」。

## 事前準備

開始前，請確認您有可用的專案、已為該專案啟用帳單，以及已啟用 BigQuery API。

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

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

   新專案會自動啟用 BigQuery API。

### 必要的角色

如要取得建立資料集、資料表、複製資料、查詢資料及建立 BI Engine 預留項目所需的權限，請要求管理員授予您專案的下列 IAM 角色：

* 執行複製工作和查詢工作：
  [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 建立資料集、建立資料表、將資料複製到資料表，以及查詢資料表：
  [BigQuery 資料編輯器](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
* 建立 BI Engine 預留空間：
  [BigQuery 資源管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceAdmin)  (`roles/bigquery.resourceAdmin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如果您在 Tableau Desktop 中使用自訂 OAuth 用戶端連線至 BigQuery，可能需要額外權限。詳情請參閱「[排解錯誤](#troubleshooting_errors)」。

## 建立 BigQuery 資料集

第一步是建立 BigQuery 資料集，用於儲存 BI Engine 管理的資料表。如要建立資料集，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，按一下專案。
4. 在詳細資料窗格中，依序點選 more\_vert「View actions」(查看動作) 和「Create dataset」(建立資料集)。
5. 在「建立資料集」頁面中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `biengine_tutorial`。
   * 在「Data location」(資料位置) 中選擇「us (multiple regions in United States)」(us (多個美國區域))，這是公開資料集儲存的[多區域位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)。
   * 在本教學課程中，您可以選取「Enable table expiration」(啟用資料表到期時間)，然後指定資料表到期前天數。
6. 讓其他設定維持在預設狀態，然後按一下 [Create dataset] (建立資料集)。

## 複製公開資料集中的資料來建立資料表

本教學課程使用 [Google Cloud Public Dataset Program](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw) 提供的資料集。公開資料集是 BigQuery 託管的資料集，可供您存取並整合到應用程式中。

在本節中，您將複製「舊金山 311 服務申請」資料集中的資料，然後建立資料表。您可以使用 [Google Cloud 控制台](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=san_francisco_311&%3Bpage=dataset&hl=zh-tw)探索資料集。

### 建立資料表

如要建立資料表，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格，搜尋 `san_francisco_311` 資料集。
4. 按一下資料集，然後依序點選「總覽」**>「資料表」**。
5. 按一下「`311_service_requests`」資料表。
6. 按一下工具列中的「複製」。
7. 在「Copy table」(複製資料表) 對話方塊的「Destination」(目的地) 區段中，執行下列操作：

   * 在「Project」(專案) 部分，點按「Browse」(瀏覽)，然後選取專案。
   * 在「資料集」部分，選取「biengine\_tutorial」。
   * 在「Table」(資料表) 中輸入 `311_service_requests_copy`。
8. 按一下「複製」。
9. **選用步驟：複製作業完成後，請依序展開 **`PROJECT_NAME` > biengine\_tutorial**，然後按一下「311\_service\_requests\_copy」>「Preview」(預覽)**，確認表格內容。將 **`PROJECT_NAME`** 替換為本教學課程的 Google Cloud 專案名稱。

## 建立 BI Engine 預留項目

1. 在 Google Cloud 控制台的「管理」下方，前往「BI Engine」頁面。

   [前往 BI Engine 頁面](https://console.cloud.google.com/bigquery/admin/bi-engine?hl=zh-tw)

   **注意：** 如果系統提示您啟用 **BigQuery Reservation API**，請點選「啟用」。
2. 按一下 add「建立預留項目」。
3. 在「建立預留項目」頁面中，設定 BI Engine 預留項目：

   * 在「Project」(專案) 清單中，確認 Google Cloud 專案。
   * 在「位置」清單中選取位置。位置應與您要查詢的[資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)相符。
   * 調整「容量 (GiB)」滑桿，設定要保留的記憶體容量。以下範例會將容量設為 2 GiB。上限為 250 GiB。
4. 點選「下一步」。
5. 在「偏好資料表」部分中，視需要指定要透過 BI Engine 加速的資料表。如要找出資料表名稱，請按照下列步驟操作：

   1. 在「資料表 ID」欄位中，輸入要透過 BI Engine 加速的資料表名稱部分內容，例如 `311`。
   2. 從建議名稱清單中選取資料表名稱。

      只有指定的資料表符合加速資格。如未指定偏好的資料表，專案中的所有查詢都符合加速資格。
6. 點選「下一步」。
7. 在「確認並提交」部分，詳閱協議。
8. 如果您接受協議條款，請按一下「建立」。

確認預訂後，詳細資料會顯示在「預訂」頁面。

## 從 Tableau Desktop 連線至資料集

如要從 Tableau Desktop 連線至資料集，您需要在 Tableau Desktop 中執行一些步驟，然後在 BI Engine 中執行一些步驟。

### 在 Tableau 中採取的步驟

1. 啟動 [Tableau Desktop](https://www.tableau.com/products/desktop)。
2. 在「連結」下方，選取「Google BigQuery」。
3. 在開啟的分頁中，選取要存取 BigQuery 資料的帳戶。
4. 如果尚未登入，請輸入電子郵件地址或電話號碼，選取「下一步」，然後輸入密碼。
5. 選取「接受」。

Tableau 現在可以存取您的 BigQuery 資料。

在 [Tableau Desktop](https://www.tableau.com/products/desktop) 的「資料來源」頁面中：

1. 從「帳單專案」下拉式選單中，選取您建立預訂的帳單專案。
2. 從「專案」下拉式選單中選取專案。
3. 在「資料集」下拉式選單中，選取資料集 `biengine_tutorial`。
4. 在「Table」(資料表) 下方，選取表格 `311_service_requests_copy`。

## 建立圖表

將資料來源新增到報表後，下一步就是建立視覺化效果。

建立圖表，顯示各鄰近地區的熱門申訴：

1. 在 Google Cloud 控制台點選「New worksheet」(新工作表)。
2. 將「Dimension」(維度) 設為「Complaint Type」(申訴類型)。
3. 根據名為 `neighborhood` 的維度篩選。
4. 在「測量指標」下方，選取「記錄數」。
5. 在「Neighborhood」篩選器上按一下滑鼠右鍵，然後點選「Edit Filter」。
6. 新增篩選器來排除空值：選取「Null」**Null**。
7. 按一下 [確定]。

詳情請參閱 [Tableau 說明文件](https://help.tableau.com/current/pro/desktop/en-us/examples_googlebigquery.htm)。

## 清除所用資源

為了避免系統向您的 Google Cloud 帳戶收取本頁面所用資源的費用，請按照下列步驟操作。

如要避免系統向您的 Google Cloud 帳戶收取本快速入門導覽課程所用資源的費用，請刪除專案、刪除 BI Engine 預留空間，或同時刪除兩者。

### 刪除專案

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

### 刪除預留項目

或者，如果您打算保留專案，可以刪除容量預留項目，避免產生額外的 BI Engine 費用。

如要刪除預訂，請按照下列步驟操作：

1. 在 Google Cloud 控制台的「管理」下方，前往「BI Engine」頁面。

   [前往 BI Engine 頁面](https://console.cloud.google.com/bigquery/admin/bi-engine?hl=zh-tw)

   **注意：** 如果系統提示您啟用 **BigQuery Reservation API**，請點選「啟用」。
2. 在「預訂」部分，找出您的預訂。
3. 在「動作」欄中，按一下預訂項目右側的 more\_vert 圖示，然後選擇「刪除」。
4. 在「Delete reservation?」(要刪除預訂項目嗎？) 對話方塊中輸入「Delete」(刪除)，然後按一下「DELETE」(刪除)。

## 排解錯誤

如果您在 Tableau Desktop 中使用自訂 OAuth 設定連線至 BigQuery，部分使用者可能會無法連線至 Tableau Server，並收到以下錯誤訊息：

```
the app is blocked
```

如要解決這個錯誤，請確認使用者已獲派角色，且該角色具備將 Tableau 連線至 BigQuery 的所有[必要權限](#required_permissions)。如果問題仍未解決，請將使用者新增至 [OAuth 設定檢視者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/oauthconfig?hl=zh-tw#oauthconfig.viewer) (`roles/oauthconfig.viewer`)。

## 後續步驟

* 如需 BI Engine 總覽，請參閱「[BI Engine 簡介](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]