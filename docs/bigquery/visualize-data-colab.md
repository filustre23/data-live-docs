* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 以圖表呈現查詢結果

您可以使用[視覺化儲存格](https://docs.cloud.google.com/colab/docs/visualization-cells?hl=zh-tw)產生及自訂圖表，在筆記本環境中進行大規模分析。在本快速入門導覽課程中，您將瞭解如何完成下列工作：

1. 使用 `bigquery-public-data.ml_datasets.penguins` 公開資料集執行 SQL 查詢。
2. 使用 SQL 儲存格疊代查詢結果。
3. 使用視覺化儲存格分析不同物種的企鵝特徵。

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

1. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
2. 確認已啟用 BigQuery API。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery&hl=zh-tw)

   如果您建立新專案，系統會自動啟用 BigQuery API。

### 所需權限

如要建立及執行 Notebook，您必須具備下列 Identity and Access Management (IAM) 角色：

* [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user)
* [Colab Enterprise 使用者 (`roles/aiplatform.colabEnterpriseUser`)](https://docs.cloud.google.com/vertex-ai/docs/general/access-control?hl=zh-tw#aiplatform.colabEnterpriseUser)

## 建立筆記本

如要建立新筆記本，請按照「[從 BigQuery 編輯器建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#create-notebook-console)」一文中的操作說明進行。

## 執行查詢

如要在筆記本中執行 SQL 查詢，請按照下列步驟操作：

1. 如要在筆記本中建立新的 SQL 儲存格，請按一下「SQL」add。
2. 輸入下列查詢：

   ```
   SELECT * FROM `bigquery-public-data.ml_datasets.penguins`;
   ```
3. 按一下 play\_circle「Run cell」(執行儲存格)。

   查詢結果會自動儲存到名為 `df` 的 DataFrame 中。
4. 建立另一個 SQL 儲存格，並將標題變更為 `female_penguins`。
5. 輸入下列查詢，參照您剛建立的 DataFrame，並篩選結果，只納入雌性企鵝：

   ```
   SELECT * FROM {df} WHERE sex = 'FEMALE';
   ```
6. 按一下 play\_circle「Run cell」(執行儲存格)。

   查詢結果會自動儲存到名為 `female_penguins` 的 DataFrame 中。

## 以視覺化方式呈現結果

1. 如要在筆記本中建立新的圖表儲存格，請按一下「圖表」add。
2. 按一下「選擇資料框架」，然後選取 `female_penguins`。

   系統隨即會顯示圖表介面。
3. 按一下「散布圖」開啟圖表選單，然後選取
   bar\_chart「直條圖」。
4. 在「指標」部分，確認顯示 `culmen_length_mm` 和 `culmen_depth_mm`。如果缺少指標，請按一下「新增指標」add\_circle\_outline，然後選取所需指標。如要移除指標，請將指標懸停在指標名稱上，然後按一下「關閉」圖示 close。
5. 針對每個指標，按一下「編輯」edit。
   在「匯總」部分，選取「平均值」。

## 清除所用資源

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

## 後續步驟

* 進一步瞭解 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)。
* 進一步瞭解 [Colab Enterprise 中的 SQL 儲存格](https://docs.cloud.google.com/colab/docs/sql-cells?hl=zh-tw)。
* 進一步瞭解 [Colab Enterprise 中的視覺化儲存格](https://docs.cloud.google.com/colab/docs/visualization-cells?hl=zh-tw)。
* 瞭解如何[使用 BigQuery DataFrame 繪製圖表](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw)。
* 瞭解如何[使用 BigQuery DataFrames 筆記本](https://github.com/googleapis/python-bigquery-dataframes/tree/main/notebooks/getting_started/getting_started_bq_dataframes.ipynb)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]