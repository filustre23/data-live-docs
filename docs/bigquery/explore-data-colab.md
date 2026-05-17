Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 在筆記本中探索查詢結果 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

您可以在 [BigQuery Colab Enterprise 筆記本](https://docs.cloud.google.com/colab/docs/introduction?hl=zh-tw)中使用 [SQL 儲存格](https://docs.cloud.google.com/colab/docs/sql-cells?hl=zh-tw)或程式碼儲存格，探索查詢結果。

在本教學課程中，您將查詢 [BigQuery 公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)的資料，並在筆記本中探索查詢結果。

## 目標

* 在 BigQuery 中建立及執行查詢。
* 使用 SQL 儲存格和程式碼儲存格，在筆記本中探索查詢結果。

## 費用

本教學課程使用[Google Cloud 公開資料集計畫](https://cloud.google.com/blog/products/data-analytics/big-data-analytics-in-the-cloud-with-free-public-datasets?hl=zh-tw)提供的資料集。這些資料集的儲存空間費用由 Google 支付，Google 也將這些資料集提供給大眾存取。您需要支付資料查詢費用。詳情請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

   新專案會自動啟用 BigQuery。

## 設定程式碼資產的預設區域

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

### 所需權限

如要建立及執行 Notebook，您必須具備下列 Identity and Access Management (IAM) 角色：

* [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user)
* [筆記本執行階段使用者 (`roles/aiplatform.notebookRuntimeUser`)](https://docs.cloud.google.com/vertex-ai/docs/general/access-control?hl=zh-tw#aiplatform.notebookRuntimeUser)
* [程式碼建立工具 (`roles/dataform.codeCreator`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeCreator)

## 在筆記本中開啟查詢結果

您可以執行 SQL 查詢，然後使用筆記本探索資料。如果您想先修改 BigQuery 中的資料再進行處理，或是只需要資料表中的部分欄位，這個方法就非常實用。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 前往 `bigquery-public-data` 專案，按一下 arrow\_right「Toggle node」(切換節點) 展開專案，然後按一下「Datasets」(資料集)。詳細資料窗格會開啟新分頁，顯示專案中的所有資料集清單。
4. 在「篩選條件」filter\_list方塊中，選擇「資料集 ID」，然後輸入「ml\_datasets」。
5. 在「資料集」**頁面，依序點選「ml\_datasets」>「企鵝」**。
6. 按一下「查詢」search。
7. 在產生的查詢中加入星號 (`*`) 以選取欄位，如下列範例所示：

   ```
   SELECT * FROM `bigquery-public-data.ml_datasets.penguins` LIMIT 1000;
   ```
8. 按一下「執行」play\_circle。
9. 在「查詢結果」部分，依序點選「開啟方式」和「Notebook」。

## 準備使用筆記本

連線至執行階段並設定應用程式預設值，準備使用筆記本。

1. 在筆記本標頭中，按一下「連線」即可[連線至預設執行階段](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#connect_to_the_default_runtime)。
2. 在「設定」程式碼區塊中，按一下「執行儲存格」play\_circle。

## 探索資料

1. 依序點選 arrow\_drop\_down「插入程式碼儲存格」
   選項 >「新增 SQL 儲存格」。
2. 在 SQL 儲存格中輸入下列查詢：

   ```
   SELECT * FROM `bigquery-public-data.ml_datasets.penguins` LIMIT 1000;
   ```
3. 按一下 play\_circle「Run cell」(執行儲存格)。

   查詢結果會顯示在 [BigQuery DataFrame](https://docs.cloud.google.com/bigquery/docs/reference/bigquery-dataframes?hl=zh-tw) 中。
4. 或者，如要使用先前在查詢編輯器中執行的查詢工作，將查詢結果載入 BigQuery DataFrame，請按照下列步驟操作：

   1. 前往「**以 DataFrame 形式從 BigQuery 工作載入的結果集**」一節。
   2. 在程式碼區塊中，按一下 play\_circle「Run cell」(執行儲存格)。

      查詢結果會顯示在 BigQuery DataFrame 中。
5. 如要取得資料的描述性指標，請按照下列步驟操作：

   1. 前往「使用 describe() 顯示描述性統計資料」部分。
   2. 在程式碼區塊中，按一下 play\_circle「Run cell」(執行儲存格)。

      結果會顯示在 BigQuery DataFrame 中。
6. 選用：使用其他 Python 函式或套件探索及分析資料。

下列程式碼範例顯示如何使用 [`bigframes.pandas`](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw) 分析資料，以及如何使用 [`bigframes.ml`](https://docs.cloud.google.com/bigquery/docs/dataframes-ml-ai?hl=zh-tw) 從 BigQuery DataFrame 中的 **penguins** 資料建立線性迴歸模型：

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

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

## 後續步驟

* 進一步瞭解如何[在 BigQuery 中建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。
* 進一步瞭解如何[使用 BigQuery DataFrame 探索資料](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]