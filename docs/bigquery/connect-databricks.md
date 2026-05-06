Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見

# 將 Databricks 連結至 BigQuery 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何連結 BigQuery 資料表或檢視區塊，以便從 [Databricks 筆記本](https://docs.gcp.databricks.com/notebooks/index.html)讀取及寫入資料。以下步驟說明如何使用 [Google Cloud 控制台](https://console.cloud.google.com/?hl=zh-tw)和 [Databricks 工作區](https://docs.gcp.databricks.com/administration-guide/account-settings-gcp/workspaces.html)。您也可以使用 `gcloud` 和 `databricks` 指令列工具執行這些步驟，但相關指引不在本教學課程的範圍內。

Databricks on Google Cloud 是託管於 Google Cloud的 Databricks 環境，在 Google Kubernetes Engine (GKE) 上執行，並與 BigQuery 和其他 Google Cloud 技術提供內建整合功能。如果您是 Databricks 新手，請觀看「[Databricks 整合式資料平台簡介](https://www.youtube.com/watch?v=n-yt_3HvkOI&hl=zh-tw)」影片，瞭解 Databricks lakehouse 平台。

## 目標

* 設定 Google Cloud 以連線至 Databricks。
* 在 Google Cloud上部署 Databricks。
* 從 Databricks 查詢 BigQuery。

## 費用

本教學課程使用 Google Cloud 控制台的可計費元件，包括 BigQuery 和 GKE。適用 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing)和 [GKE 定價](https://cloud.google.com/kubernetes-engine/pricing?hl=zh-tw)。如要瞭解在 Google Cloud上執行的 Databricks 帳戶相關費用，請參閱 Databricks 說明文件中的「[設定帳戶並建立工作區](https://docs.gcp.databricks.com/getting-started/try-databricks-gcp.html#set-up-your-account-and-create-a-workspace)」一節。

## 事前準備

將 Databricks 連結至 BigQuery 前，請先完成下列步驟：

1. 啟用 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)。
2. 為 Databricks 建立服務帳戶。
3. 建立 Cloud Storage bucket，做為暫時儲存空間。

### 啟用 BigQuery Storage API

對於使用 BigQuery 的任何新專案，系統預設會啟用 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)。如果現有專案尚未啟用 API，請按照下列操作說明進行：

1. 前往 Google Cloud 控制台的「BigQuery Storage API」頁面。

   [前往 BigQuery Storage API](https://console.cloud.google.com/marketplace/product/google/bigquerystorage.googleapis.com?hl=zh-tw)
2. 確認已啟用 **BigQuery Storage API**。

### 為 Databricks 建立服務帳戶

接著，建立 Identity and Access Management (IAM) 服務帳戶，允許 Databricks 叢集對 BigQuery 執行查詢。建議您為這個服務帳戶提供執行工作所需的最低權限。請參閱「[BigQuery 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

1. 前往 Google Cloud 控制台的「Service accounts」(服務帳戶) 頁面。

   [前往「Service Accounts」(服務帳戶)](https://console.cloud.google.com/iam-admin/serviceaccounts?hl=zh-tw)
2. 按一下「建立服務帳戶」，將服務帳戶命名為「`databricks-bigquery`」，輸入簡短說明 (例如「`Databricks tutorial
   service account`」)，然後按一下「建立並繼續」。
3. 在「將專案存取權授予這個服務帳戶」下方，指定服務帳戶的角色。如要授予服務帳戶權限，讓服務帳戶在同一個專案中讀取 Databricks 工作區和 BigQuery 資料表中的資料，且不參照具體化檢視區塊，請授予下列角色：

   * **BigQuery 讀取工作階段使用者**
   * **BigQuery 資料檢視者**

   如要授予寫入資料的權限，請指派下列角色：

   * **BigQuery 工作使用者**
   * **BigQuery 資料編輯者**
4. 記下新服務帳戶的電子郵件地址，以供後續步驟參考。
5. 按一下 [完成]。

### 建立 Cloud Storage 值區

如要寫入 BigQuery，Databricks 叢集必須有權存取 Cloud Storage 值區，才能緩衝處理寫入的資料。

1. 前往 Google Cloud 控制台的「Cloud Storage 瀏覽器」。

   [前往 Storage 瀏覽器](https://console.cloud.google.com/storage/browser?hl=zh-tw)
2. 按一下「建立值區」，開啟「建立值區」對話方塊。
3. 指定用於將資料寫入 BigQuery 的 bucket 名稱。bucket 名稱必須是[全域不重複名稱](https://docs.cloud.google.com/storage/docs/buckets?hl=zh-tw#naming)。
   如果您指定的值區名稱已存在，Cloud Storage 會傳回錯誤訊息。如果發生這種情況，請為 bucket 指定其他名稱。
4. 在本教學課程中，請使用儲存位置、儲存空間類別、存取控管和進階設定的預設設定。
5. 按一下「建立」建立 Cloud Storage 值區。
6. 按一下「權限」，然後按一下「新增」，並在「服務帳戶」頁面上，指定您為 Databricks 存取權建立的服務帳戶電子郵件地址。
7. 按一下「選取角色」，然後新增「儲存空間管理員」角色。
8. 按一下 [儲存]。

## 在 Google Cloud上部署 Databricks

請完成下列步驟，準備在 Google Cloud上部署 Databricks。

1. 如要設定 Databricks 帳戶，請按照 Databricks 文件「[設定 Databricks on Google Cloud帳戶](https://docs.gcp.databricks.com/getting-started/try-databricks-gcp.html)」中的操作說明進行。
2. 註冊後，請參閱[這篇文章](https://docs.gcp.databricks.com/administration-guide/account-settings-gcp/index.html)，進一步瞭解如何管理 Databricks 帳戶。

### 建立 Databricks 工作區、叢集和筆記本

下列步驟說明如何建立 Databricks 工作區、叢集和 Python 筆記本，以便編寫程式碼來存取 BigQuery。

1. 確認 [Databricks 的必要條件](https://docs.gcp.databricks.com/getting-started/try-databricks-gcp.html#prerequisites-for-account-and-workspace-creation)。
2. 建立第一個工作區。在 [Databricks 帳戶控制台](https://accounts.gcp.databricks.com/workspaces)中，按一下「Create Workspace」(建立工作區)。
3. 指定`gcp-bq`做為**工作區名稱**，然後選取**區域**。
4. 如要判斷 Google Cloud 專案 ID，請前往 Google Cloud 控制台，然後將值複製到「**Google Cloud 專案 ID**」欄位。

   [前往 Google Cloud 控制台](https://console.cloud.google.com/welcome?hl=zh-tw)
5. 按一下「儲存」，即可建立 Databricks 工作區。
6. 如要使用 Databricks 執行階段 7.6 以上版本建立 Databricks 叢集，請在左側選單列選取「Clusters」(叢集)，然後點選頂端的「Create Cluster」(建立叢集)。
7. 指定叢集名稱和大小，然後按一下「進階選項」，並指定服務帳戶的電子郵件地址。 Google Cloud
8. 點選「建立叢集」。
9. 如要建立 Databricks 適用的 Python 筆記本，請按照「[建立筆記本](https://docs.gcp.databricks.com/notebooks/notebooks-manage.html#create-a-notebook)」一文的說明操作。

## 從 Databricks 查詢 BigQuery

完成上述設定後，您就能安全地將 Databricks 連線至 BigQuery。Databricks 會使用[開放原始碼 Google Spark Adapter](https://github.com/GoogleCloudDataproc/spark-bigquery-connector) 的分支版本存取 BigQuery。

Databricks 會自動將特定查詢述詞 (例如篩選巢狀資料欄) 下推至 BigQuery，藉此減少資料移轉量並加快查詢速度。此外，新增的這項功能可先透過 `query()` API 在 BigQuery 上執行 SQL 查詢，再進行資料移轉，因此可縮減產生的資料集移轉大小。

下列步驟說明如何在 BigQuery 中存取資料集，以及將自己的資料寫入 BigQuery。

### 存取 BigQuery 的公開資料集

BigQuery 提供可用[公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)清單。如要查詢屬於公開資料集的 BigQuery 莎士比亞資料集，請按照下列步驟操作：

1. 如要讀取 BigQuery 資料表，請在 Databricks 筆記本中使用下列程式碼片段。

   ```
   table = "bigquery-public-data.samples.shakespeare"
   df = spark.read.format("bigquery").option("table",table).load()
   df.createOrReplaceTempView("shakespeare")
   ```

   按下 `Shift+Return` 執行程式碼。

   現在您可以透過 Spark DataFrame (`df`) 查詢 BigQuery 資料表。舉例來說，使用下列程式碼即可顯示 DataFrame 的前三列：

   ```
   df.show(3)
   ```

   如要查詢其他資料表，請更新 `table` 變數。
2. Databricks 筆記本的主要功能是，您可以在單一筆記本中混合使用不同語言 (例如 Scala、Python 和 SQL) 的儲存格。

   執行上一個建立暫時檢視區塊的儲存格後，您可以使用下列 SQL 查詢，以視覺化方式呈現莎士比亞作品的字數。

   ```
   %sql
   SELECT word, SUM(word_count) AS word_count FROM words GROUP BY word ORDER BY word_count DESC LIMIT 12
   ```

   **注意：** 輸出內容預設為表格格式。如要改為長條圖，請按一下長條圖示，從可用的 Databricks 視覺化效果中選取。

   上方的儲存格會對 Databricks 叢集中的資料架構執行 Spark SQL 查詢，而不是 BigQuery。這種做法的好處是資料分析會在 Spark 層級進行，不會再發出 BigQuery API 呼叫，因此不會產生額外的 BigQuery 費用。
3. 或者，您也可以使用 `query()` API 將 SQL 查詢的執行作業委派給 BigQuery，並進行最佳化，以減少產生的資料架構傳輸大小。與上述範例 (處理作業在 Spark 中完成) 不同，如果您使用這種方法，在 BigQuery 上執行查詢時，系統會套用定價和查詢最佳化設定。

   以下範例使用 Scala、`query()` API 和 BigQuery 中的莎士比亞公開資料集，計算莎士比亞作品中最常見的五個字詞。執行程式碼前，請先在 BigQuery 中建立名為 `mdataset` 的空白資料集，供程式碼參照。詳情請參閱「[將資料寫入 BigQuery](#writing-data-to-bigquery)」。

   ```
   %scala
   // public dataset
   val table = "bigquery-public-data.samples.shakespeare"

   // existing dataset where the Google Cloud user has table creation permission
   val tempLocation = "mdataset"
   // query string
   val q = s"""SELECT word, SUM(word_count) AS word_count FROM ${table}
       GROUP BY word ORDER BY word_count DESC LIMIT 10 """

   // read the result of a GoogleSQL query into a DataFrame
   val df2 =
     spark.read.format("bigquery")
     .option("query", q)
     .option("materializationDataset", tempLocation)
     .load()

   // show the top 5 common words in Shakespeare
   df2.show(5)
   ```

   如需更多程式碼範例，請參閱 [Databricks BigQuery 範例筆記本](https://docs.databricks.com/_extras/notebooks/source/big-query-python.html)。

## 將資料寫入 BigQuery

BigQuery 資料表位於[資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)中。
如要將資料寫入 BigQuery 資料表，您必須先在 BigQuery 中建立新資料集。如要為 Databricks Python 筆記本建立資料集，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 展開「動作」more\_vert選項，點選「建立資料集」，然後命名 `together`。
3. 在 Databricks Python 筆記本中，使用下列程式碼片段，從含有三個字串項目的 Python 清單建立簡單的 Spark 資料架構：

   ```
   from pyspark.sql.types import StringType
   mylist = ["Google", "Databricks", "better together"]

   df = spark.createDataFrame(mylist, StringType())
   ```
4. 在筆記本中新增另一個儲存格，將上一個步驟中的 Spark 資料架構寫入資料集 `together` 的 BigQuery 資料表 `myTable`。系統會建立或覆寫資料表。使用您先前指定的值區名稱。

   ```
   bucket = YOUR_BUCKET_NAME
   table = "together.myTable"

   df.write
     .format("bigquery")
     .option("temporaryGcsBucket", bucket)
     .option("table", table)
     .mode("overwrite").save()
   ```
5. 如要確認資料是否已成功寫入，請透過 Spark DataFrame (`df`) 查詢及顯示 BigQuery 資料表：

   ```
   display(spark.read.format("bigquery").option("table", table).load)
   ```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

移除 Databricks 前，請務必先備份資料和筆記本。如要清除並徹底移除 Databricks，請在Google Cloud 控制台中取消 Databricks 訂閱，並從Google Cloud 控制台中移除您建立的所有相關資源。

如果刪除 Databricks 工作區，系統可能不會刪除 Databricks [建立的](https://docs.gcp.databricks.com/administration-guide/account-settings-gcp/workspaces.html#secure-the-workspaces-gcs-buckets-in-your-project) 兩個 Cloud Storage bucket (名稱為 `databricks-WORKSPACE_ID` 和 `databricks-WORKSPACE_ID-system`)，除非這些 bucket 為空。工作區刪除後，您可以在專案的Google Cloud 控制台中手動刪除這些物件。

## 後續步驟

本節提供其他文件和教學課程的清單：

* 瞭解 [Databricks 免費試用詳細資料](https://databricks.com/try-databricks)。
* 瞭解 [Databricks on Google Cloud](https://docs.gcp.databricks.com/)。
* 瞭解 [Databricks BigQuery](https://docs.databricks.com/data/data-sources/google/bigquery.html)。
* 請參閱 [BigQuery 支援 Databricks 的網誌公告](https://databricks.com/blog/2020/07/31/announcing-support-for-google-bigquery-in-databricks-runtime-7-1.html)。
* 瞭解 [BigQuery 範例筆記本](https://docs.databricks.com/_extras/notebooks/source/big-query-python.html)。
* 瞭解 [Databricks 的 Terraform 供應商 Google Cloud](https://github.com/databrickslabs/terraform-provider-databricks/blob/master/CHANGELOG.md)。
* 請參閱 [Databricks 網誌](https://databricks.com/blog/)，進一步瞭解[資料科學主題](https://databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html)和[資料集](https://databricks.com/blog/2020/04/14/covid-19-datasets-now-available-on-databricks.html)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]