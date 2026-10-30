Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BI Engine 和 Tableau Desktop 分析資料

將 BI Engine 與 Tableau Desktop 整合，即可建構由 BigQuery 支援的快速互動式報表和資訊主頁。您可以將 Tableau 連結至 BI Engine 預留項目，執行低延遲分析，並以視覺化方式呈現大量資料集，同時不影響查詢效能。

## 目標

* 建立資料集並複製資料。
* 使用 Google Cloud 控制台建立 BI 預留項目並新增運算資源。
* 使用 Tableau Desktop 連線至 BI Engine 管理的 BigQuery 資料表。
* 使用 Tableau Desktop 建立資訊主頁。

## 費用

在本文件中，您會使用下列 Google Cloud計費元件：

* [BigQuery](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw)
* [BI Engine](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#bi-engine-pricing)

您可以使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)，根據預測用量估算費用。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

完成本文所述工作後，您可以刪除建立的資源，避免繼續計費，詳情請參閱「[清除所用資源](#clean-up)」。

## 事前準備

開始之前，請確認您有可使用的專案、已啟用該專案的計費功能，並已啟用 BigQuery API。

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

1. 啟用 BigQuery API (如果尚未啟用)。

   **啟用 API 所需的角色**

   您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「Service Usage 管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

   如果是新專案，系統會自動啟用 BigQuery API。

### 必要的角色

如要取得建立資料集、建立資料表、複製資料、查詢資料及建立 BI Engine 預留項目所需的權限，請要求管理員授予您專案的下列 IAM 角色：

* 執行複製工作和查詢工作：[BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 建立資料集、建立資料表、將資料複製到資料表，以及查詢資料表：[BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
* 建立 BI Engine 預留項目：[BigQuery 資源管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceAdmin)  (`roles/bigquery.resourceAdmin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如果您在 Tableau Desktop 中使用自訂 OAuth 用戶端連線至 BigQuery，可能需要額外權限。詳情請參閱「[排解錯誤](#troubleshooting_errors)」。

## 建立 BigQuery 資料集

首先，請建立 BigQuery 資料集，用於儲存 BI Engine 代管資料表。如要建立資料集，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，點選專案。
4. 在詳細資料窗格中，依序點選「View actions」(查看動作) more\_vert 和「Create dataset」(建立資料集)。
5. 在「Create dataset」(建立資料集) 頁面執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `biengine_tutorial`。
   * 在「Data location」(資料位置) 中選擇「us (multiple regions in United States)」(us (多個美國區域))，也就是儲存公開資料集的[多區域位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)。
   * 在本教學課程中，您可以選取「Enable table expiration」(啟用資料表到期時間)，然後指定資料表到期前的天數。
6. 讓其他設定維持在預設狀態，然後按一下 [Create dataset] (建立資料集)。

## 複製公開資料集的資料來建立資料表

本教學課程使用 [Google Cloud Public Dataset Program](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw) 提供的資料集。公開資料集是 BigQuery 代管的資料集，可供您存取並整合至應用程式。

在本節中，您將複製[舊金山 311 服務要求](https://console.cloud.google.com/marketplace/details/san-francisco-public-data/sf-311?filter=solution-type%3Adataset&hl=zh-tw)資料集中的資料，建立資料表。您可以使用[Google Cloud 控制台](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=san_francisco_311&%3Bpage=dataset&hl=zh-tw)探索資料集。

### 建立資料表

如要建立資料表，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格，搜尋 `san_francisco_311` 資料集。
4. 依序點選資料集和**「總覽」 > 「資料表」**。
5. 點選「`311_service_requests`」資料表。
6. 按一下工具列中的「複製」。
7. 在「Copy table」(複製資料表) 對話方塊的「Destination」(目的地) 部分，執行下列操作：

   * 在「Project」(專案) 部分，點選「Browse」(瀏覽)，然後選取專案。
   * 在「資料集」部分，選取「biengine\_tutorial」。
   * 在「Table」(資料表) 中輸入 `311_service_requests_copy`。
8. 點選「複製」。
9. 選用步驟：複製工作完成後，請依序展開「`PROJECT_NAME`」>「biengine\_tutorial」，然後依序點選「311\_service\_requests\_copy」>「預覽」，驗證資料表內容。將 **`PROJECT_NAME`** 替換為本教學課程的 Google Cloud 專案名稱。

## 建立 BI Engine 預留項目

1. 在 Google Cloud 控制台的「Administration」(管理) 下方，前往「BI Engine」頁面。

   [前往「BI Engine」頁面](https://console.cloud.google.com/bigquery/admin/bi-engine?hl=zh-tw)

   **注意：** 如果系統提示您啟用 **BigQuery Reservation API**，請點選「啟用」。
2. 按一下 add「Create reservation」(建立預留項目)。
3. 在「Create Reservation」(建立預留項目) 頁面中，設定 BI Engine 預留項目：

   * 在「Project」(專案) 清單中，確認您的 Google Cloud 專案。
   * 在「Location」(位置) 清單中選取位置。位置應與您查詢的[資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)相符。
   * 將「GiB of Capacity」(容量 (GiB)) 滑桿調整至要預留的記憶體容量。以下範例將容量設為 2 GiB。上限為 250 GiB。
4. 點選「下一步」。
5. 在「Preferred Tables」(偏好資料表) 部分，您可以視需要指定要透過 BI Engine 加速的資料表。如要找出資料表名稱，請按照下列步驟操作：

   1. 在「Table Id」(資料表 ID) 欄位中，輸入要由 BI Engine 加速的資料表名稱部分，例如 `311`。
   2. 從建議名稱清單中選取資料表名稱。

      只有指定的資料表才能加速。如未指定偏好資料表，所有專案查詢都能加速。
6. 點選「下一步」。
7. 在「確認並提交」部分，詳閱協議內容。
8. 如果您接受協議條款，請按一下「建立」。

確認預留項目後，詳細資料會顯示在「Reservations」(預留項目) 頁面。

## 透過 Tableau Desktop 連結資料集

如要從 Tableau Desktop 連線至資料集，您必須在 Tableau Desktop 中執行一些步驟，然後在 BI Engine 中執行一些步驟。

### 在 Tableau 中採取的步驟

1. 啟動 [Tableau Desktop](https://www.tableau.com/products/desktop)。
2. 在「Connect」(連結) 下方，選取「Google BigQuery」。
3. 在開啟的分頁中，選取要存取的 BigQuery 資料所屬帳戶。
4. 如果尚未登入，請輸入電子郵件地址或電話號碼，選取「下一步」，然後輸入密碼。
5. 選取「接受」。

Tableau 現在可以存取 BigQuery 資料。

在 [Tableau Desktop](https://www.tableau.com/products/desktop) 的「Data Source」(資料來源) 頁面中：

1. 從「Billing Project」(計費專案) 下拉式選單中，選取您建立預留項目的計費專案。
2. 在「Project」(專案) 下拉式選單中選取專案。
3. 在「Dataset」(資料集) 下拉式選單中，選取資料集 `biengine_tutorial`。
4. 在「Table」(資料表) 下方，選取資料表 `311_service_requests_copy`。

## 建立圖表

將資料來源新增至報表後，下一步是建立圖表。

建立圖表，顯示各社區的主要申訴案件：

1. 在 Google Cloud 控制台中，按一下「New worksheet」(新增工作表)。
2. 將「維度」設為「Complaint Type」。
3. 根據名為 `neighborhood` 的維度進行篩選。
4. 在「測量指標」下方，選取「Number of Records」。
5. 在「Neighborhood」篩選器上按一下滑鼠右鍵，然後點選「Edit Filter」。
6. 新增篩選器來排除空值：選取「空值」**Null**。
7. 按一下 [確定]。

詳情請參閱 [Tableau 說明文件](https://help.tableau.com/current/pro/desktop/en-us/examples_googlebigquery.htm)。

## 清除所用資源

為了避免系統向您的 Google Cloud 帳戶收取本頁面所用資源的費用，請按照下列步驟操作。

如要避免系統向您的 Google Cloud 帳戶收取本快速入門導覽課程所用資源的費用，您可以刪除專案、刪除 BI Engine 預留項目，或同時刪除兩者。

### 刪除專案

如要避免付費，最簡單的方法就是刪除您為了本教學課程所建立的專案。

刪除專案的方法如下：

**注意**：刪除專案會帶來以下影響：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### 刪除預留項目

或者，如果您打算保留專案，可以刪除預留運算資源，避免產生額外的 BI Engine 費用。

如要刪除預留項目，請按照下列步驟操作：

1. 在 Google Cloud 控制台的「Administration」(管理) 下方，前往「BI Engine」頁面。

   [前往「BI Engine」頁面](https://console.cloud.google.com/bigquery/admin/bi-engine?hl=zh-tw)

   **注意：** 如果系統提示您啟用 **BigQuery Reservation API**，請點選「啟用」。
2. 在「Reservations」(預留項目) 部分，找出預留項目。
3. 在「Actions」(動作) 欄中，按一下預留項目右側的 more\_vert 圖示，然後選擇「Delete」(刪除)。
4. 在「Delete reservation?」(要刪除預留項目嗎？) 對話方塊中，輸入「Delete」，然後按一下「DELETE」(刪除)。

## 排解錯誤

如果您在 Tableau Desktop 中使用自訂 OAuth 設定連線至 BigQuery，部分使用者可能會在連線至 Tableau 伺服器時遇到問題，並看到下列錯誤訊息：

```
the app is blocked
```

如要解決這項錯誤，請確認使用者獲派的角色具備將 Tableau 連結至 BigQuery 的所有[必要權限](#required_permissions)。如果問題持續發生，請將使用者新增至 [OAuth 設定檢視者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/oauthconfig?hl=zh-tw#oauthconfig.viewer) (`roles/oauthconfig.viewer`)。

## 後續步驟

* 如需 BI Engine 總覽，請參閱「[BI Engine 簡介](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]