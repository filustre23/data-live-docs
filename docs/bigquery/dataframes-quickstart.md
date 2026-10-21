Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 試用 BigQuery DataFrames

BigQuery DataFrames 可將可擴充的 Python 分析和機器學習 (ML) 帶入 BigQuery。運算作業會在 BigQuery 中執行，並採用伺服器端處理方式，因此您可分析及建立大型資料集模型，不受本機或筆記本記憶體限制。您可以使用類似 pandas (`bigframes.pandas`) 和 BigQuery ML (`bigframes.bigquery`) 的語法，不必編寫 SQL。

在本快速入門導覽課程中，您將在 [BigQuery 筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)中使用 [BigQuery DataFrames API](https://dataframes.bigquery.dev/reference/index.html)，執行下列分析和 ML 工作：

* 在公開資料集上建立 DataFrame。`bigquery-public-data.ml_datasets.penguins`
* 計算企鵝的平均體重。
* 清理並準備企鵝資料子集，以供訓練。
* 使用 `bigframes.bigquery.ml.create_model` 訓練[線性迴歸模型](https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.create_model.html)。
* 使用 `bigframes.bigquery.ml.evaluate` [評估](https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.evaluate.html)模型。

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

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

   如果您建立新專案，系統會自動啟用 BigQuery API。

### 所需權限

如要建立及執行 Notebook，您需要下列 Identity and Access Management (IAM) 角色：

* [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user)
* [筆記本執行階段使用者 (`roles/aiplatform.notebookRuntimeUser`)](https://docs.cloud.google.com/vertex-ai/docs/general/access-control?hl=zh-tw#aiplatform.notebookRuntimeUser)
* [程式碼建立工具 (`roles/dataform.codeCreator`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeCreator)

## 建立筆記本

按照「[從 BigQuery 編輯器建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#create-notebook-console)」一文中的操作說明，建立新的筆記本。

## 試用 BigQuery DataFrames

如要試用 BigQuery DataFrames，請按照下列步驟操作：

1. 在筆記本中建立新的程式碼儲存格。
2. 在程式碼儲存格中新增下列程式碼：

   ```
   import bigframes.pandas as bpd

   # Set BigQuery DataFrames options
   # Note: The project option is not required in all environments.
   # On BigQuery Studio, the project ID is automatically detected.
   bpd.options.bigquery.project = your_gcp_project_id

   # Use "partial" ordering mode to generate more efficient queries, but the
   # order of the rows in DataFrames may not be deterministic if you have not
   # explictly sorted it. Some operations that depend on the order, such as
   # head() will not function until you explictly order the DataFrame. Set the
   # ordering mode to "strict" (default) for more pandas compatibility.
   bpd.options.bigquery.ordering_mode = "partial"

   # Create a DataFrame from a BigQuery table
   query_or_table = "bigquery-public-data.ml_datasets.penguins"
   df = bpd.read_gbq(query_or_table)

   # Efficiently preview the results using the .peek() method.
   df.peek()
   ```
3. 修改 `bpd.options.bigquery.project = your_gcp_project_id` 行，指定您的 Google Cloud 專案 ID。例如：`bpd.options.bigquery.project = "myProjectID"`。
4. 執行程式碼儲存格。

   程式碼會傳回 `DataFrame` 物件，其中包含企鵝的相關資料。
5. 在筆記本中建立新的程式碼儲存格，並加入下列程式碼：

   ```
   # Use the DataFrame just as you would a pandas DataFrame, but calculations
   # happen in the BigQuery query engine instead of the local system.
   average_body_mass = df["body_mass_g"].mean()
   print(f"average_body_mass: {average_body_mass}")
   ```
6. 執行程式碼儲存格。

   這段程式碼會計算企鵝的平均體重，並將結果列印到控制台。Google Cloud
7. 在筆記本中建立新的程式碼儲存格，並加入下列程式碼：

   ```
   import bigframes.bigquery as bbq
   from google.cloud import bigquery

   # Ensure a dataset exists to store the model
   client = bigquery.Client(project=bpd.options.bigquery.project)
   client.create_dataset("bq_quickstart", exists_ok=True)

   # Filter down to the Adelie Penguin species
   adelie_data = df[df.species == "Adelie Penguin (Pygoscelis adeliae)"]

   # Drop the columns that are not needed
   adelie_data = adelie_data.drop(columns=["species"])

   # Drop rows with nulls to get the training data
   training_data = adelie_data.dropna()

   # Train a linear regression model
   model_name = f"{bpd.options.bigquery.project}.bq_quickstart.penguin_weight"
   model_metadata = bbq.ml.create_model(
       model_name,
       replace=True,
       options={"model_type": "LINEAR_REG"},
       training_data=training_data.rename(columns={"body_mass_g": "label"}),
   )

   # Evaluate the model
   evaluation = bbq.ml.evaluate(model_name)
   print(evaluation)
   ```
8. 執行程式碼儲存格。

   這段程式碼會直接在 BigQuery 中訓練線性迴歸模型，並傳回模型的評估指標。

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

* 繼續瞭解 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)。
* 瞭解如何[使用 BigQuery DataFrame 呈現圖表](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw)。
* 瞭解如何[使用 BigQuery DataFrames 筆記本](https://github.com/googleapis/python-bigquery-dataframes/tree/main/notebooks/getting_started/getting_started_bq_dataframes.ipynb)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-13 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-13 (世界標準時間)。"],[],[]]