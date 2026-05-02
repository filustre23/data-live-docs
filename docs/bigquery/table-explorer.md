* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用資料表探索工具建立查詢

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-studio-product-team@google.com](mailto:bq-studio-product-team@google.com)。

本文將說明如何使用資料表探索工具檢查資料表資料，以及建立資料探索查詢。

## 關於資料表探索工具

資料表探索工具提供自動化方式，可讓您以視覺化方式探索資料表資料，並根據所選資料表欄位建立查詢。

在資料表探索器中，選取要檢查的資料表欄位。
一次最多可選取 10 個資料表欄位。

資料表探索工具會將所選欄位顯示為互動式資訊卡，並列出每個欄位最多 10 個最常見的值，依 `count` 欄排序。您可以選取要仔細檢查的欄位和相異值，與資訊卡互動。資料表探索工具會根據您的選取項目建立資料探索查詢。

您可以將這項查詢複製到查詢編輯器的新查詢中，
或在資料表瀏覽器中套用查詢。套用查詢後，資料表探索工具會執行查詢，並以查詢結果重新整理顯示的資訊卡。如要繼續探索表格資料，請從更新後的資訊卡中選取更多欄位或值。

## 限制

* 資料表探索器適用於 BigQuery 資料表、BigLake 資料表、外部資料表和檢視區塊。
* 資料表探索工具一次只能探索一個資料表。這項功能不支援同時探索多個資料表，也不支援產生跨資料表作業，例如 `JOIN` 作業。
* 資料表探索工具會建立 SQL 查詢，直接反映您選取的資料表欄位和不重複值。您可以執行表格探索工具建立的查詢，或在查詢編輯器中手動編輯查詢。資料表探索器不會提供 AI 輔助功能，生成、補全或說明 SQL 查詢。
* 如要探索資料表資料，並為設有資料欄層級存取權控管 (ACL) 或使用者權限受限的資料表產生查詢，您必須擁有所有選取欄位的讀取權限。如要執行產生的查詢，您必須具備足夠的[權限](#roles)。

## 定價

資料表探索工具會根據您選取的資料表欄位和相異值執行查詢，並顯示資料表探索結果。這些查詢會產生運算定價費用。在您確認選取的資料表欄位並觸發查詢執行作業前，資料表探索工具會顯示每個查詢將處理的資料量。

如果您執行資料表多層檢視產生的查詢，也可能會產生運算費用。

如要進一步瞭解 BigQuery 的運算價格，請參閱[價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

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
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery API.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery API.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com&hl=zh-tw)

### 必要角色和權限

如要取得查看表格資料及使用表格瀏覽器產生查詢所需的權限，請要求管理員授予您下列 IAM 角色：

* 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)。
* [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
  在要探索的所有資料表和檢視畫面中。

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備查看資料表資料，以及使用資料表探索工具產生查詢所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要查看資料表資料及使用資料表探索工具產生查詢，必須具備下列權限：

* `bigquery.jobs.create`
  無論資料儲存於何處，都會在執行查詢的專案中顯示。
* `bigquery.tables.getData`
  ，即可探索所有資料表和檢視區塊。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[使用身分與存取權管理功能控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 探索資料表中的資料，建立查詢

如要探索資料表資料，並根據所選資料表欄位和值建立查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」。
4. 依序點選「總覽」**>「表格」**，然後選取要建立查詢的表格。
5. 點按「資料表探索工具」分頁標籤，然後點按「選取欄位」。
6. 在「選取欄位」窗格中，選取最多 10 個要探索的資料表欄位。
7. 如果是分區資料表，請在「分區篩選器」部分設定自訂分區篩選器。探索資料表時，分區篩選器可減少可計費的運算量。

   1. 選取「套用自訂分區篩選器」。
   2. 在顯示的設定欄位中，設定分割篩選器。

   篩選器設定的顯示方式取決於資料表的分區類型：小時、天、月、年或範圍。
8. 按一下 [儲存]。

   點按「儲存」後，BigQuery 會執行查詢，顯示所選欄位的常見值，這會產生費用。您可以在「選取欄位」窗格頂端，查看將處理的資料量。

   表格探索工具會將所選欄位顯示為資訊卡，並列出最多十個最常見的值，依 `Count` 欄排序。在「產生的查詢」部分，您會看到可執行的查詢，顯示相同的資料。
9. 選用：如要修改結果，可以嘗試下列做法：

   1. 在顯示的所選欄位資訊卡中，選取相異值，進一步篩選資料。
   2. 如要還原所有變更，請按一下「重設」。
   3. 在「Generated Query」(產生的查詢) 區段中，按一下「Copy to query」(複製到查詢)，將生成的程式碼複製到查詢編輯器中新的「未命名的查詢」。在新建立的查詢分頁中，您可以編輯、執行及管理查詢。
10. 如要執行生成的查詢，請按一下「套用」。

    BigQuery 會執行產生的查詢，並以查詢結果重新整理顯示的資訊卡。
11. 如要繼續探索表格，請從重新整理後顯示的資訊卡中選取新欄位或相異值。

## 疑難排解

```
Access Denied: Project [project_id]: User does not have bigquery.jobs.create
permission in project [project_id].
```

如果主體沒有在專案中建立查詢工作的權限，就會發生這個錯誤。

**解決方法**：管理員必須授予您查詢專案的 `bigquery.jobs.create` 權限。除了存取所查詢資料所需的權限外，您還必須具備這項權限。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[生成資料洞察以探索資料](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)。
* 瞭解如何[在 BigQuery 中透過 Gemini 輔助撰寫查詢](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw)。
* 瞭解如何使用[資料畫布](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw)，以自然語言問題疊代查詢結果。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]