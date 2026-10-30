Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 在筆記本中探索查詢結果 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

直接在 [Colab Enterprise 筆記本](https://docs.cloud.google.com/colab/docs/introduction?hl=zh-tw)中開啟 BigQuery 查詢結果，即可順暢地從編寫 SQL 轉換為使用 Python 分析資料。透過 SQL 和程式碼儲存格探索資料，您就能有效篩選及分類大型資料集，再進行深入分析。

在本教學課程中，您將查詢 [BigQuery 公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)中的資料，並在筆記本中探索查詢結果。

## 目標

* 在 BigQuery 中建立及執行查詢。
* 使用 SQL 儲存格和程式碼儲存格，在筆記本中探索查詢結果。

## 費用

本教學課程使用的資料集可透過[Google Cloud 公開資料集計畫](https://cloud.google.com/blog/products/data-analytics/big-data-analytics-in-the-cloud-with-free-public-datasets?hl=zh-tw)取得。Google 會支付這些資料集的儲存費用，並提供資料的公開存取權。對資料執行查詢時，系統會向您收取費用。詳情請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」一文。

## 事前準備

1. 在 Google Cloud 控制台的專案選取器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時不需要特定 IAM 角色，只要您獲派某個專案的角色，即可選取該專案。
   * **建立專案**：如要建立專案，您必須具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，不要選取現有專案。如果採用這種做法，當您完成這些步驟後，就可以直接刪除該專案，並移除相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認 Google Cloud 專案已啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project)。
3. 啟用 BigQuery API (如果尚未啟用)。

   **啟用 API 所需的角色**

   您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「Service Usage 管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

   新專案會自動啟用 BigQuery。

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

### 所需權限

如要建立及執行筆記本，您必須具備下列 Identity and Access Management (IAM) 角色：

* [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user)
* [Notebook 執行階段使用者 (`roles/aiplatform.notebookRuntimeUser`)](https://docs.cloud.google.com/vertex-ai/docs/general/access-control?hl=zh-tw#aiplatform.notebookRuntimeUser)
* [程式碼建立者 (`roles/dataform.codeCreator`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeCreator)

## 在筆記本中開啟查詢結果

您可以執行 SQL 查詢，然後使用筆記本探索資料。如果您想先修改 BigQuery 中的資料再使用，或只需要資料表中的部分欄位，這個方法就很實用。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 前往 `bigquery-public-data` 專案，按一下 arrow\_right「Toggle node」(切換節點) 展開專案，然後按一下「Datasets」(資料集)。「Details」(詳細資料) 窗格中會開啟新分頁，顯示專案中所有資料集的清單。
4. 在 filter\_list「Filter」(篩選器) 方塊中，選擇「Dataset ID」(資料集 ID)，然後輸入 **ml\_datasets**。
5. 在「**資料集**」頁面，依序點選 **「ml\_datasets」 > 「penguins」**。
6. 按一下「search 查詢」。
7. 在產生的查詢中，加入星號 (`*`) 來選取欄位，如下例所示：

   ```
   SELECT * FROM `bigquery-public-data.ml_datasets.penguins` LIMIT 1000;
   ```
8. 按一下「play\_circle 執行」。
9. 在「Query results」(查詢結果) 部分，依序點選「Open in」(開啟方式) 和「Notebook」。

## 準備使用筆記本

連線至執行階段並設定應用程式預設值，準備使用筆記本。

1. 在筆記本標頭中，按一下「Connect」(連線)，[連線至預設執行階段](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#connect_to_the_default_runtime)。
2. 在「Setup」程式碼區塊中，按一下 play\_circle「Run cell」。

## 探索資料

1. 依序點選「arrow\_drop\_down **插入程式碼儲存格
   選項」 > 「新增 SQL 儲存格」**。
2. 在 SQL 儲存格中輸入下列查詢：

   ```
   SELECT * FROM `bigquery-public-data.ml_datasets.penguins` LIMIT 1000;
   ```
3. 按一下「執行儲存格」圖示 play\_circle。

   查詢結果會顯示在 [BigQuery DataFrame](https://docs.cloud.google.com/bigquery/docs/reference/bigquery-dataframes?hl=zh-tw) 中。
4. 或者，如要使用先前在查詢編輯器中執行的查詢工作，將查詢結果載入 BigQuery DataFrame，請按照下列步驟操作：

   1. 前往「Result set loaded from BigQuery job as a DataFrame」(從 BigQuery 工作載入為 DataFrame 的結果集) 專區。
   2. 在程式碼區塊中，按一下 play\_circle「Run cell」(執行儲存格)。

      查詢結果會顯示在 BigQuery DataFrame 中。
5. 如要取得資料的描述性指標，請按照下列步驟操作：

   1. 前往「Show descriptive statistics using describe()」部分。
   2. 在程式碼區塊中，按一下 play\_circle「Run cell」(執行儲存格)。

      結果會顯示在 BigQuery DataFrame 中。
6. 選用：使用其他 Python 函式或套件探索及分析資料。

下列範例使用 [`bigframes.pandas`](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw) 分析資料，並使用 [`bigframes.ml`](https://docs.cloud.google.com/bigquery/docs/dataframes-ml-ai?hl=zh-tw) 根據 BigQuery DataFrame 中的 **penguins** 資料建立線性迴歸模型。這個範例會計算模型的 R2 分數，並以統計指標表格的形式傳回。不會生成圖表。

```
import bigframes.pandas as bpd

# Load data from BigQuery
query_or_table = "bigquery-public-data.ml_datasets.penguins"
bq_df = bpd.read_gbq(query_or_table)

# Inspect one of the columns (or series) of the DataFrame:
bq_df["body_mass_g"]

# Compute the mean of this series:
average_body_mass = bq_df["body_mass_g"].mean()
print(f"average_body_mass: {average_body_mass}")

# Find the heaviest species using the groupby operation to calculate the
# mean body_mass_g:
(
    bq_df["body_mass_g"]
    .groupby(by=bq_df["species"])
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Create the Linear Regression model
from bigframes.ml.linear_model import LinearRegression

# Filter down to the data we want to analyze
adelie_data = bq_df[bq_df.species == "Adelie Penguin (Pygoscelis adeliae)"]

# Drop the columns we don't care about
adelie_data = adelie_data.drop(columns=["species"])

# Drop rows with nulls to get our training data
training_data = adelie_data.dropna()

# Pick feature columns and label column
X = training_data[
    [
        "island",
        "culmen_length_mm",
        "culmen_depth_mm",
        "flipper_length_mm",
        "sex",
    ]
]
y = training_data[["body_mass_g"]]

model = LinearRegression(fit_intercept=False)
model.fit(X, y)
model.score(X, y)
```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

如要避免付費，最簡單的方法就是刪除您為了本教學課程所建立的 Google Cloud 專案。

**注意**：刪除專案會造成以下影響：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

## 後續步驟

* 進一步瞭解如何[在 BigQuery 中建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。
* 進一步瞭解如何[使用 BigQuery DataFrames 探索資料](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]