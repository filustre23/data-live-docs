* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立管道

本文說明如何在 BigQuery 中建立[管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)。管道由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 提供支援。

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
- Enable the BigQuery, Dataform, and Vertex AI APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cdataform.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery, Dataform, and Vertex AI APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cdataform.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

### 管道的必要角色

如要取得建立管道所需的權限，請要求管理員授予您專案的下列 IAM 角色：

* 如何建立管道：
  [程式碼建立者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeCreator)  (`roles/dataform.codeCreator`)
* 如要編輯及執行管道：
  [Dataform 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.editor)  (`roles/dataform.editor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如要進一步瞭解 Dataform IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw)」。

**注意：** 建立管道時，BigQuery 會授予您該管道的 [Dataform 管理員角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)。在 Google Cloud 專案中獲派 Dataform 管理員角色的所有使用者，都擁有專案中建立的所有管道的擁有者存取權。如要覆寫這項行為，請參閱[在建立資源時授予特定角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-specific-role)。

### 筆記本選項的必要角色

如要取得在筆記本選項中選取執行階段範本所需的權限，請要求管理員授予您專案的「Notebook Runtime User」 (`roles/aiplatform.notebookRuntimeUser`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如果沒有這個角色，可以選取預設的筆記本執行階段規格。

### 設定程式碼資產的預設區域

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

## 建立管道

您也可以在 Google Cloud 控制台中使用 BigQuery 的「管道和連線」頁面，建立使用[簡化 BigQuery 專屬工作流程](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw)的 Dataform 管道。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要建立管道，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在編輯器窗格的分頁列中，按一下「+」符號旁的箭頭 arrow\_drop\_down，然後點選「Pipeline」(管道)。
3. 選用：如要重新命名管道，請按一下管道名稱，然後輸入新名稱。
4. 按一下「立即開始」，然後前往「設定」分頁標籤。
5. 在「驗證」部分，選擇使用 Google 帳戶或服務帳戶的使用者憑證授權管道。

   * 如要使用 Google 帳戶的使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。

     **注意：** 系統不支援使用使用者憑證驗證以 API 為基礎的執行作業。如要使用 Dataform API [執行管道中的所有工作](#run-pipeline-all-tasks)，必須將管道設為使用服務帳戶。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。如需建立服務帳戶，請按一下「新增服務帳戶」。
6. 在「Processing location」(處理位置) 部分，選取管道的處理位置。

   * 如要啟用自動選取位置功能，請選取「自動選取位置」。這個選項會根據要求中參照的資料集選取位置。選取程序如下：

     + 如果查詢參照相同位置的資料集，BigQuery 會使用該位置。
     + 如果查詢參照來自兩個以上不同位置的資料集，就會發生錯誤。如要進一步瞭解這項限制，請參閱「[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)」。
     + 如果查詢未參照任何資料集，BigQuery 預設會使用 `US` 多區域。
   * 如要選取特定區域，請選取**區域**，然後在**區域**選單中選擇區域。或者，您也可以在查詢中使用[`@@location` 系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)。詳情請參閱「[指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)」。
   * 如要選取多區域，請選取**多區域**，然後在**多區域**選單中選擇多區域。

   管道處理位置不一定要與程式碼資產的預設儲存位置相符。

### SQLX 選項

如要設定管道的 SQLX 設定，請在「SQLX options」(SQLX 選項) 區段中執行下列操作：

1. 在「Default project」(預設專案) 欄位中，輸入現有Google Cloud 專案的名稱。這個值用於 `workflow_settings.yaml` 檔案中的 `defaultProject`，以及 `dataform.json` 檔案中的 `defaultDatabase`。管線工作在執行期間會使用預設專案。

   **注意：** 系統不會驗證專案名稱，因此您可以輸入任何非空白字串。不過，如果專案不存在，管道執行作業就會失敗。
2. 選用：在「預設資料集」欄位中，搜尋並選取現有資料集。系統會根據所選專案和處理位置，篩選可用資料集清單。這個值用於 `workflow_settings.yaml` 檔案中的 `defaultDataset`。管道工作在執行期間會使用預設資料集。

   **注意：** 設定預設資料集後，如果變更管道的區域，系統會使資料集選取項目失效。變更專案也可能導致資料集選取失效。如果所選專案中沒有指定資料集，系統會建立該資料集。

### 筆記本選項

如要在管道中新增筆記本，請在「Notebook options」(筆記本選項) 部分執行下列操作：

1. 在「執行階段範本」欄位中，接受預設的筆記本執行階段，或搜尋並選取現有的執行階段。

   * 如要查看預設執行階段的規格，請按一下相鄰的箭頭。
   * 如要建立新的執行階段，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。**注意：**筆記本執行階段範本必須與指定該範本的管道位於相同區域。**注意：**在 BigQuery 管道中加入筆記本時，無法變更 Vertex AI 執行階段執行個體的網路。執行階段僅限使用預設網路，不支援選取其他網路。
2. 在「Cloud Storage bucket」欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket，用來儲存管道中筆記本的輸出內容。
3. 按照「[將主體新增至值區層級政策](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add)」一文中的步驟，將自訂 Dataform 服務帳戶新增為主體，加入您打算用來儲存排定管線執行作業輸出的 Cloud Storage 值區，並將[儲存空間管理員角色](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin) (`roles/storage.admin`) 授予這個主體。

   所選自訂 Dataform 服務帳戶必須取得所選值區的 Storage 管理員 IAM 角色。

## 新增管道工作

如要將工作新增至管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 如要新增程式碼素材資源，請選取下列其中一個選項：

   ### SQL 查詢

   1. 按一下「新增工作」，然後選取「查詢」。
      您可以建立新查詢，或匯入現有查詢。
   2. 選用：在「查詢工作詳細資料」窗格的「在以下項目後執行」選單中，選取要先於查詢執行的工作。

   **建立新的查詢**

   1. 按一下「編輯查詢」旁的 arrow\_drop\_down 箭頭選單，然後選取「在內容中」或「在新分頁中」。
   2. 搜尋現有查詢。
   3. 選取查詢名稱，然後按下 **Enter** 鍵。
   4. 按一下 [儲存]。
   5. 選用：如要重新命名查詢，請點選管道窗格中的查詢名稱，然後依序點選「編輯查詢」、畫面頂端的現有查詢名稱，然後輸入新名稱。

   **匯入現有查詢**

   1. 按一下「編輯查詢」旁的arrow\_drop\_down箭頭選單，然後按一下「匯入副本」。
   2. 搜尋要匯入的現有查詢，或從搜尋窗格選取現有查詢。匯入查詢時，系統會將查詢的來源檔案複製到管道中，因此原始查詢不會受到影響。
   3. 按一下「編輯」開啟匯入的查詢。
   4. 按一下 [儲存]。

   ### 筆記本

   1. 按一下「新增工作」，然後選取「筆記本」。
      您可以建立新筆記本或匯入現有筆記本。
      如要變更筆記本執行階段範本的設定，請參閱[筆記本選項](#notebook_options)。
   2. 選用：在「Notebook task details」(筆記本工作詳細資料) 窗格中，選取「Run after」(在下列工作完成後執行) 選單，然後選取要在筆記本之前執行的工作。

   **建立新筆記本**

   1. 按一下「編輯記事本」旁的箭頭選單 arrow\_drop\_down，然後選取「在內容中」或「在新分頁中」。
   2. 搜尋現有筆記本。
   3. 選取筆記本名稱，然後按下 **Enter** 鍵。
   4. 按一下 [儲存]。
   5. 選用：如要重新命名筆記本，請按一下管道窗格中的筆記本名稱，然後按一下「編輯筆記本」，按一下畫面頂端的現有筆記本名稱，然後輸入新名稱。

   **匯入現有筆記本**

   1. 按一下「編輯記事本」旁的箭頭選單 arrow\_drop\_down，然後點選「匯入副本」。
   2. 搜尋要匯入的現有筆記本，或從搜尋窗格選取現有筆記本。匯入筆記本時，原始筆記本不會變更，因為筆記本的來源檔案會複製到管道中。
   3. 如要開啟匯入的筆記本，請按一下「編輯」。
   4. 按一下 [儲存]。

   ### 資料準備

   1. 按一下「新增工作」，然後選取「資料準備」。
      您可以建立新的資料準備作業，也可以匯入現有作業。
   2. 選用：在「資料準備工作詳細資料」窗格的「Run after」(在下列工作完成後執行) 選單中，選取要先執行的工作。

   **建立新的資料準備作業**

   1. 按一下「編輯資料準備」旁的 arrow\_drop\_down 箭頭選單，然後選取「在內容中」或「在新分頁中」。
   2. 搜尋現有的資料準備作業。
   3. 選取資料準備作業名稱，然後按下 **Enter** 鍵。
   4. 按一下 [儲存]。
   5. 選用：如要重新命名資料準備作業，請按一下管道窗格中的資料準備名稱，然後依序點選「編輯資料準備作業」和畫面頂端的名稱，並輸入新名稱。

   **匯入現有的資料準備作業**

   1. 按一下「編輯資料準備」旁的箭頭下拉式選單 arrow\_drop\_down，然後點選「匯入副本」。
   2. 搜尋要匯入的現有資料準備項目，或從搜尋窗格選取現有資料準備項目。匯入資料準備時，原始資料不會變更，因為資料準備的來源檔案會複製到管道中。
   3. 如要開啟匯入的資料準備作業，請按一下「編輯」。
   4. 按一下 [儲存]。

   ### 資料表

   **預覽**

   這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
   詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

   **注意：** 如要提供意見回饋或尋求支援，請傳送電子郵件至
   [dataform-preview-support@google.com](mailto:dataform-preview-support@google.com)。
   1. 按一下「新增工作」，然後選取「表格」。
   2. 在「建立新項目」窗格中，選取「資料表」或「遞增資料表」。
   3. 確認資料表的預設專案，或選取新專案。
   4. 確認資料表的預設資料集，或選取新的資料集。
   5. 輸入資料表名稱。
   6. 在「表格工作詳細資料」窗格中，按一下「開啟」即可開啟工作。
   7. 使用「詳細資料」**>「設定」**中的設定，或資料表程式碼編輯器的 `config` 區塊，設定工作。

      如要變更中繼資料，請使用「設定」分頁。您可以在這個分頁中，透過程式碼編輯器編輯 `config` 區塊中的特定值，例如格式為 JavaScript 物件的字串或陣列。使用這個分頁可避免語法錯誤，並確認設定正確無誤。

      選用：在「Run after」(在下列項目後執行) 選單中，選取要在表格前執行的工作。

      您也可以在編輯器的 `config` 區塊中，定義管道工作的後設資料。詳情請參閱「[建立資料表](https://docs.cloud.google.com/dataform/docs/reference/sample-scripts?hl=zh-tw#creating_tables)」。

      編輯器會驗證程式碼，並顯示驗證狀態。

      **注意：** 在 `config` 區塊中使用 JavaScript 函式做為值時，您無法在「設定」分頁中編輯 JavaScript 函式。
   8. 在「詳細資料」**> 已編譯的查詢**中，查看從 SQLX 程式碼編譯的 SQL。
   9. 按一下「執行」，在管道中執行 SQL。
   10. 在「查詢結果」中檢查資料預覽。

   ### 查看

   **預覽**

   這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
   詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

   **注意：** 如要提供意見回饋或尋求支援，請傳送電子郵件至
   [dataform-preview-support@google.com](mailto:dataform-preview-support@google.com)。
   1. 按一下「新增工作」，然後選取「查看」。
   2. 在「建立新項目」窗格中，選取「檢視」或「具體化檢視」。
   3. 確認檢視畫面的預設專案，或選取新專案。
   4. 確認檢視區塊的預設資料集，或選取新的資料集。
   5. 輸入檢視區塊名稱。
   6. 在「查看工作詳細資料」窗格中，按一下「開啟」即可開啟工作。
   7. 使用「詳細資料」**>「設定」**中的設定，或在檢視區塊的程式碼編輯器中，使用 `config` 區塊設定工作。

      如要變更中繼資料，請使用「設定」分頁。您可以在這個分頁中，透過程式碼編輯器編輯 `config` 區塊中的特定值，例如格式為 JavaScript 物件的字串或陣列。使用這個分頁可避免語法錯誤，並確認設定正確無誤。

      (選用) 在「Run after」(在下列項目後執行) 選單中，選取要先執行的工作。

      您也可以在編輯器的 `config` 區塊中，定義管道工作的後設資料。詳情請參閱「[使用 Dataform Core 建立檢視區塊](https://docs.cloud.google.com/dataform/docs/reference/sample-scripts?hl=zh-tw#create-view)」。

      編輯器會驗證程式碼，並顯示驗證狀態。

      **注意：** 在 `config` 區塊中使用 JavaScript 函式做為值時，您無法在「設定」分頁中編輯 JavaScript 函式。
   8. 在「詳細資料」**> 已編譯的查詢**中，查看從 SQLX 程式碼編譯的 SQL。
   9. 按一下「執行」，在管道中執行 SQL。
   10. 在「查詢結果」中檢查資料預覽。

## 編輯管道工作

如要編輯管道工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下選取的工作。
5. 如要變更前一個工作，請在「Run after」(在後執行) 選單中，選取要排在目前工作之前的工作。
6. 如要編輯所選工作的內容，請按一下「編輯」。
7. 在新開啟的分頁中編輯工作內容，然後儲存變更。

## 刪除管道工作

如要從管道中刪除工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下選取的工作。
5. 在「工作詳細資料」窗格中，依序按一下「刪除」「刪除」。

## 分享管道

**重要事項：** 如果您在 [`projects.locations.updateConfig` Dataform API 方法](https://docs.cloud.google.com/dataform/reference/rest/v1beta1/projects.locations/updateConfig?hl=zh-tw)中，將 `enable_private_workspace` 欄位[(預先發布版)](https://cloud.google.com/products?hl=zh-tw#product-launch-stages) 設為 `true`，只有管道建立者才能讀取及寫入該管道中的程式碼。詳情請參閱「[啟用私人工作區](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#enable-private-workspaces)」。**注意：** 您可以共用管道，但無法共用管道中的工作。

如要共用管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「共用」，然後選取「管理權限」。
5. 按一下「新增使用者/群組」。
6. 在「新增主體」欄位中，輸入至少一位使用者或群組的名稱。
7. 在「指派角色」中選取角色。
8. 按一下 [儲存]。

## 分享管道連結

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「共用」，然後選取「共用連結」。系統會將管道網址複製到電腦的剪貼簿。

## 執行管道

執行管道時，您可以選擇執行管道中的所有工作、手動選取要執行的特定工作，或是執行具有所選標記的工作。

### 執行管道中的所有工作

如要手動執行目前版本的管道，請選取下列其中一個選項：

### 控制台

如要執行管道中的所有工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 依序點按 play\_circle\_filled「執行」>「執行所有工作」。如果為[驗證](#create_a_pipeline)選取「使用我的使用者憑證執行」，則必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。
5. 選用：如要檢查執行作業，請[查看過去的手動執行作業](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw#view-manual-runs)。

### API

**注意：** Dataform API 不支援管道執行的使用者憑證。如要使用 API，請務必在管道設定的「驗證」部分選取服務帳戶。

如要手動執行管道，請編譯預設工作區，並使用編譯結果建立工作流程叫用。

1. 如要為預設工作區建立編譯結果，請使用 [`projects.locations.repositories.compilationResults.create` 方法](https://docs.cloud.google.com/dataform/reference/rest/v1/projects.locations.repositories.compilationResults/create?hl=zh-tw)。

   使用下列資訊執行 API 要求：

   ```
   curl -X POST \
      -H "Authorization: Bearer $(gcloud auth print-access-token)" \
      -H "Content-Type: application/json" \
      -d '{
         "workspace": "projects/PROJECT_ID/locations/LOCATION/repositories/REPOSITORY_ID/workspaces/default"
      }' \
      "https://dataform.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/repositories/REPOSITORY_ID/compilationResults"
   ```

   更改下列內容：

   * `LOCATION`：存放區的 Google Cloud 區域，例如 `us-central1`。如要在 Google Cloud 控制台中找出存放區位置，請前往「Explorer」窗格，選取管道，開啟「Settings」分頁，然後按一下「Open pipeline in Dataform」。位置位於網址中，格式為 `/locations/LOCATION/`。
   * `PROJECT_ID`：Google Cloud 專案的專屬 ID。
   * `REPOSITORY_ID`：Dataform 存放區的專屬 ID，例如 `my-secure-repo`。如要在 Google Cloud 控制台中找到存放區 ID，請前往「Explorer」窗格，選取管道，開啟「Settings」分頁，然後查看「Dataform repository ID」欄位。
2. 在回應主體中找出 `name` 欄位，並複製其值，例如 `projects/my-project/locations/us-central1/repositories/my-repo/compilationResults/12345-67890`。
3. 使用 [`projects.locations.repositories.workflowInvocations.create` 方法](https://docs.cloud.google.com/dataform/reference/rest/v1/projects.locations.repositories.workflowInvocations/create?hl=zh-tw)觸發管道執行。

   使用下列資訊執行 API 要求：

   ```
   curl -X POST \
      -H "Authorization: Bearer $(gcloud auth print-access-token)" \
      -H "Content-Type: application/json" \
      -d '{
         "compilationResult": "COMPILATION_RESULT"
      }' \
      "https://dataform.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/repositories/REPOSITORY_ID/workflowInvocations"
   ```

   更改下列內容：

   * `COMPILATION_RESULT`：您在上一個步驟中複製的編譯結果完整資源名稱。
   * `LOCATION`：存放區的 Google Cloud 區域，例如 `us-central1`。
   * `PROJECT_ID`：Google Cloud 專案的專屬 ID。
   * `REPOSITORY_ID`：Dataform 存放區的專屬 ID，例如 `my-secure-repo`。

### 在管道中執行所選工作

如要在管道中執行所選工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 依序按一下「play\_circle\_filled」**執行**
   >「選取要執行的工作」。
5. 在「Run」(執行) 窗格的「Authentication」(驗證) 部分，使用 Google 帳戶或服務帳戶的使用者憑證授權執行作業。

   * 如要使用 Google 帳戶的使用者憑證 ([預覽版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「使用使用者憑證執行」。
   * 如要使用自訂服務帳戶，請選取「以所選服務帳戶執行」，然後選取自訂服務帳戶。

     **注意：** 如要在選單中查看服務帳戶，您必須具備專案層級的 `iam.serviceAccounts.list` 權限，這項權限包含在「查看服務帳戶」角色 (`roles/iam.serviceAccountViewer`) 中。如果沒有這項權限，您可以按一下「手動輸入」，然後輸入服務帳戶 ID，選取服務帳戶。

     如需建立服務帳戶，請按一下「新增服務帳戶」。
6. 確認已選取「Selection of tasks」(選取工作)。
7. 在「Select tasks to run」(選取要執行的工作) 選單中，搜尋特定工作並選取要執行的工作。

   「工作」表格會列出您選取的工作。按一下工作名稱，即可直接在 SQL 編輯器中開啟。
8. 選用：設定下列執行選項：

   * **包含依附元件**：選取這個選項即可執行所選工作及其依附元件。
   * **包含附屬元件**：選取這個選項，即可執行所選工作及其遞移下游附屬元件。
   * **以全面重新整理的方式執行**：選取這個選項，即可從頭重建所有資料表。
   * **以高優先順序執行互動式工作 (預設)**：選取這個選項可設定 BigQuery 查詢工作優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果清除這個選項，查詢會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行，優先順序較低。
9. 按一下「執行」。如果驗證方法選取「使用使用者憑證執行」，則必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。
10. 選用：如要檢查執行作業，請[查看過去的手動執行作業](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw#view-manual-runs)。

### 在管道中執行具有所選標記的工作

如要在管道中執行含有選定標記的工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 依序點選「執行」play\_circle\_filled「依代碼執行」，然後執行下列任一操作：

   * 按一下要執行的代碼。
   * 按一下 checklist「選取要執行的代碼」。
5. 在「執行」窗格的「驗證」部分，使用 Google 帳戶或服務帳戶的使用者憑證授權執行作業。

   * 如要使用 Google 帳戶的使用者憑證 ([預覽版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「使用使用者憑證執行」。
   * 如要使用自訂服務帳戶，請選取「以所選服務帳戶執行」，然後選取自訂服務帳戶。

     **注意：** 如要在選單中查看服務帳戶，您必須具備專案層級的 `iam.serviceAccounts.list` 權限，這項權限包含在「查看服務帳戶」角色 (`roles/iam.serviceAccountViewer`) 中。如果沒有這項權限，您可以按一下「手動輸入」，然後輸入服務帳戶 ID，選取服務帳戶。

     如需建立服務帳戶，請按一下「新增服務帳戶」。
6. 確認已選取「選取代碼」。
7. 在「選取要執行的代碼」選單中，搜尋特定代碼並選取要執行的代碼。

   「工作」表格會列出您選取的工作。按一下工作名稱，即可直接在 SQL 編輯器中開啟。
8. 選用：設定下列執行選項：

   * **包含依附元件**：選取這個選項即可執行所選工作及其依附元件。
   * **包含附屬元件**：選取這個選項，即可執行所選工作及其遞移下游附屬元件。
   * **以全面重新整理的方式執行**：選取這個選項，即可從頭重建所有資料表。
   * **以高優先順序執行互動式工作 (預設)**：選取這個選項可設定 BigQuery 查詢工作優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果清除這個選項，查詢會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行，優先順序較低。
9. 按一下「執行」。如果驗證方法選取「使用使用者憑證執行」，則必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。
10. 選用：如要檢查執行作業，請[查看過去的手動執行作業](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw#view-manual-runs)。

### 授權給您的 Google 帳戶

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [dataform-preview-support@google.com](mailto:dataform-preview-support@google.com)。

如要使用[Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)使用者憑證驗證資源，您必須手動授予 BigQuery 管道權限，讓管道取得 Google 帳戶的存取權杖，並代表您存取來源資料。您可以使用 OAuth 對話方塊介面手動授予核准。

您只需要授予 BigQuery 管道一次權限。

如要撤銷授予的權限，請按照下列步驟操作：

1. 前往 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)。
2. 按一下「BigQuery Pipelines」。
3. 按一下 [移除存取權]。

**警告：** 撤銷存取權後，這個 Google 帳戶在所有區域擁有的管道日後都無法執行。

如果管道包含筆記本，您也必須手動授予 Colab Enterprise 權限，才能取得 Google 帳戶的存取權杖，並以您的名義存取來源資料。你只需要授予一次權限。你可以在 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)撤銷這項權限。

## 後續步驟

* 進一步瞭解 [BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)。
* 瞭解如何[管理管道](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw)。
* 瞭解如何[排定管道](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]