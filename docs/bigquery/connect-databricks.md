Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 連線至 Databricks

BigQuery 管理員可以建立[連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，以便從 [Databricks 筆記本](https://docs.gcp.databricks.com/notebooks/index.html)讀取及寫入資料。以下步驟說明如何使用 [Google Cloud 控制台](https://console.cloud.google.com/?hl=zh-tw)和 [Databricks 工作區](https://docs.gcp.databricks.com/administration-guide/account-settings-gcp/workspaces.html)。您也可以使用 `gcloud` 和 `databricks` 指令列工具執行這些步驟，但相關指南不在本教學課程的範圍內。

Databricks on Google Cloud 是託管於 Google Cloud的 Databricks 環境，在 Google Kubernetes Engine (GKE) 上執行，並與 BigQuery 和其他 Google Cloud 技術內建整合。如果您是 Databricks 新手，請觀看「[Databricks 統合資料平台簡介](https://www.youtube.com/watch?v=n-yt_3HvkOI&hl=zh-tw)」影片，概略瞭解 Databricks lakehouse 平台。

## 目標

* 設定 Google Cloud ，以便連線至 Databricks。
* 在 Google Cloud上部署 Databricks。
* 從 Databricks 查詢 BigQuery。

## 費用

本教學課程使用 Google Cloud 控制台的計費元件，包括 BigQuery 和 GKE。適用 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing)和 [GKE 定價](https://cloud.google.com/kubernetes-engine/pricing?hl=zh-tw)。如要瞭解在 Google Cloud上執行 Databricks 帳戶的相關費用，請參閱 Databricks 說明文件的「[設定帳戶並建立工作區](https://docs.gcp.databricks.com/getting-started/try-databricks-gcp.html#set-up-your-account-and-create-a-workspace)」一節。

## 事前準備

將 Databricks 連結至 BigQuery 之前，請先完成下列步驟：

1. 啟用 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)。
2. 為 Databricks 建立服務帳戶。
3. 建立 Cloud Storage bucket 做為暫時儲存空間。

### 啟用 BigQuery Storage API

根據預設，凡是使用 BigQuery 的新專案，都會啟用 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)。如果現有專案未啟用 API，請按照下列操作說明進行：

1. 前往 Google Cloud 控制台的「BigQuery Storage API」頁面。

   [前往 BigQuery Storage API](https://console.cloud.google.com/marketplace/product/google/bigquerystorage.googleapis.com?hl=zh-tw)
2. 確認已啟用 **BigQuery Storage API**。

### 為 Databricks 建立服務帳戶

接著，建立 Identity and Access Management (IAM) 服務帳戶，允許 Databricks 叢集對 BigQuery 執行查詢。建議您授予這個服務帳戶執行工作所需的最低權限。請參閱「[BigQuery 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

1. 前往 Google Cloud 控制台的「Service accounts」(服務帳戶) 頁面。

   [前往「Service Accounts」(服務帳戶)](https://console.cloud.google.com/iam-admin/serviceaccounts?hl=zh-tw)
2. 按一下「Create service account」(建立服務帳戶)，將服務帳戶命名為 `databricks-bigquery`，輸入簡短說明 (例如 `Databricks tutorial
   service account`)，然後按一下「Create and continue」(建立並繼續)。
3. 在「Grant this service account access to project」(將專案存取權授予這個服務帳戶) 下方，指定服務帳戶的角色。如要授予服務帳戶權限，允許其使用 Databricks 工作區和相同專案中的 BigQuery 資料表讀取資料，特別是不參照 materialized view，請授予下列角色：

   * **BigQuery 讀取工作階段使用者**
   * **BigQuery 資料檢視者**

   如要授予寫入資料的權限，請授予下列角色：

   * **BigQuery 工作使用者**
   * **BigQuery 資料編輯者**
4. 記下新服務帳戶的電子郵件地址，以便在後續步驟中參考。
5. 按一下「完成」。

### 建立 Cloud Storage bucket

如要寫入 BigQuery，Databricks 叢集必須能存取 Cloud Storage bucket，才能緩衝處理寫入的資料。

1. 前往 Google Cloud 控制台的「Cloud Storage 瀏覽器」。

   [前往「Storage Browser」(Storage 瀏覽器)](https://console.cloud.google.com/storage/browser?hl=zh-tw)
2. 按一下「建立 bucket」，開啟「建立 bucket」對話方塊。
3. 指定用於將資料寫入 BigQuery 的 bucket 名稱。bucket 名稱必須[全域不重複](https://docs.cloud.google.com/storage/docs/buckets?hl=zh-tw#naming)。如果指定的 bucket 名稱已存在，Cloud Storage 會傳回錯誤訊息。如果發生這種情況，請為 bucket 指定其他名稱。
4. 在本教學課程中，請使用儲存空間位置、儲存空間級別、存取控管和進階設定的預設設定。
5. 按一下「Create」(建立)，建立 Cloud Storage bucket。
6. 依序點選「Permissions」(權限) 和「Add」(新增)，然後在「[Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts?hl=zh-tw)」(服務帳戶) 頁面中，指定您為 Databricks 存取權建立的服務帳戶電子郵件地址。
7. 按一下「選取角色」，然後新增「Storage 管理員」角色。
8. 按一下「儲存」。

## 在 Google Cloud部署 Databricks

請完成下列步驟，準備在 Google Cloud上部署 Databricks。

1. 如要設定 Databricks 帳戶，請按照 Databricks
   說明文件「[Set up your Databricks on Google Cloud
   account](https://docs.gcp.databricks.com/getting-started/try-databricks-gcp.html)」(設定 Databricks on 帳戶) 中的操作說明進行。
2. 註冊後，請進一步瞭解如何[管理 Databricks 帳戶](https://docs.gcp.databricks.com/administration-guide/account-settings-gcp/index.html)。

### 建立 Databricks 工作區、叢集和筆記本

下列步驟說明如何建立 Databricks 工作區、叢集和 Python 筆記本，以便編寫程式碼來存取 BigQuery。

1. 確認 [Databricks 必要條件](https://docs.gcp.databricks.com/getting-started/try-databricks-gcp.html#prerequisites-for-account-and-workspace-creation)。
2. 建立第一個工作區。在「Databricks account console」(Databricks 帳戶控制台)，按一下「Create Workspace」(建立工作區)。
3. 在「Workspace name」(工作區名稱) 中指定 `gcp-bq`，然後選取「Region」(區域)。
4. 如要判斷 Google Cloud 專案 ID，請前往 Google Cloud 控制台，然後將值複製到「**Google Cloud project ID**」欄位。

   [前往 Google Cloud 控制台](https://console.cloud.google.com/welcome?hl=zh-tw)
5. 按一下「Save」(儲存)，建立 Databricks 工作區。
6. 如要建立 Databricks 執行階段 7.6 以上版本的 Databricks 叢集，請在左側選單列中選取「Clusters」(叢集)，然後按一下頂端的「Create Cluster」(建立叢集)。
7. 指定叢集名稱和大小，然後按一下「Advanced Options」(進階選項)，並指定 Google Cloud服務帳戶的電子郵件地址。
8. 點選「建立叢集」。
9. 如要為 Databricks 建立 Python 筆記本，請按照「[建立筆記本](https://docs.gcp.databricks.com/notebooks/notebooks-manage.html#create-a-notebook)」中的操作說明進行。

## 從 Databricks 查詢 BigQuery

完成上述設定後，您就能安全地將 Databricks 連結至 BigQuery。Databricks 使用[開放原始碼 Google Apache Spark 轉接器](https://github.com/GoogleCloudDataproc/spark-bigquery-connector)的分支版本存取 BigQuery。

Databricks 會自動將特定查詢述詞 (例如篩選巢狀資料欄) 推送至 BigQuery，減少資料移轉並加快查詢速度。此外，您也可以先使用 `query()` API 在 BigQuery 上執行 SQL 查詢，減少結果資料集的移轉大小。

下列步驟說明如何存取 BigQuery 中的資料集，並將自己的資料寫入 BigQuery。

### 存取 BigQuery 公開資料集

BigQuery 提供可用的[公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)清單。如要查詢 BigQuery Shakespeare 資料集 (屬於公開資料集)，請按照下列步驟操作：

1. 如要讀取 BigQuery 資料表，請在 Databricks 筆記本中使用下列程式碼片段。

   ```
   table = "bigquery-public-data.samples.shakespeare"
   df = spark.read.format("bigquery").option("table",table).load()
   df.createOrReplaceTempView("shakespeare")
   ```

   按下 `Shift+Return` 執行程式碼。

   現在，您可以透過 Apache Spark DataFrame (`df`) 查詢 BigQuery 資料表。例如，使用下列指令顯示 DataFrame 的前三列：

   ```
   df.show(3)
   ```

   如要查詢其他資料表，請更新 `table` 變數。
2. Databricks 筆記本的主要功能是，您可以在單一筆記本中混合使用不同語言 (例如 Scala、Python 和 SQL) 的儲存格。

   執行上一個建立臨時檢視表的儲存格後，您可以使用下列 SQL 查詢，以視覺化方式呈現莎士比亞作品中的字數。

   ```
   %sql
   SELECT word, SUM(word_count) AS word_count FROM words GROUP BY word ORDER BY word_count DESC LIMIT 12
   ```

   **注意：**輸出內容預設為表格格式。如要改為長條圖，請按一下長條圖圖示，從可用的 Databricks 視覺化圖表中選取。

   儲存格會對 Databricks 叢集中的 DataFrame 執行 Apache Spark SQL 查詢，而非在 BigQuery 中執行。這種做法的好處是，資料分析會在 Apache Spark 層級進行，不會發出其他 BigQuery API 呼叫，也不會產生額外的 BigQuery 費用。
3. 或者，您也可以使用 `query()` API 將 SQL 查詢的執行作業委派給 BigQuery，並最佳化以減少結果資料框架的傳輸大小。與前一個範例不同的是，前一個範例是在 Apache Spark 中完成處理，如果使用這種方法，則會套用定價和查詢最佳化，在 BigQuery 上執行查詢。

   以下範例使用 Scala、`query()` API 和 BigQuery 中的莎士比亞公開資料集，計算莎士比亞作品中最常見的五個字詞。執行程式碼前，您必須先在 BigQuery 中建立名為 `mdataset` 的空白資料集，供程式碼參照。詳情請參閱「[將資料寫入 BigQuery](#writing-data-to-bigquery)」。

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

BigQuery 資料表位於[資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)中。您必須先在 BigQuery 建立新資料集，才能將資料寫入 BigQuery 資料表。如要為 Databricks Python 筆記本建立資料集，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 展開 more\_vert「Actions」(動作) 選項，點選「Create dataset」(建立資料集)，然後命名為 `together`。
3. 在 Databricks Python 筆記本中，使用下列程式碼片段，從含有三個字串項目的 Python 清單建立 Apache Spark 資料框架：

   ```
   from pyspark.sql.types import StringType
   mylist = ["Google", "Databricks", "better together"]

   df = spark.createDataFrame(mylist, StringType())
   ```
4. 在筆記本中新增另一個儲存格，將上一步的 Apache Spark DataFrame 寫入資料集 `together` 中的 BigQuery 資料表 `myTable`。系統會建立或覆寫資料表。請使用您稍早指定的 bucket 名稱。

   ```
   bucket = YOUR_BUCKET_NAME
   table = "together.myTable"

   df.write
     .format("bigquery")
     .option("temporaryGcsBucket", bucket)
     .option("table", table)
     .mode("overwrite").save()
   ```
5. 如要確認資料已成功寫入，請透過 Apache Spark DataFrame (`df`) 查詢並顯示 BigQuery 資料表：

   ```
   display(spark.read.format("bigquery").option("table", table).load)
   ```

## 清除所用資源

移除 Databricks 前，請務必備份資料和筆記本。如要清理並完全移除 Databricks，請在Google Cloud 控制台中取消 Databricks 訂閱，並從Google Cloud 控制台移除您建立的所有相關資源。

刪除 Databricks 工作區時，如果 [Databricks 建立](https://docs.gcp.databricks.com/administration-guide/account-settings-gcp/workspaces.html#secure-the-workspaces-gcs-buckets-in-your-project)的兩個 Cloud Storage bucket (名稱為 `databricks-WORKSPACE_ID` 和 `databricks-WORKSPACE_ID-system`) 不是空的，可能不會遭到刪除。刪除工作區後，您可以在專案的Google Cloud 控制台中手動刪除這些物件。

## 後續步驟

本節列出其他文件和教學課程：

* 瞭解 [Databricks 免費試用詳細資料](https://databricks.com/try-databricks)。
* 瞭解 [Databricks on Google Cloud](https://docs.gcp.databricks.com/)。
* 瞭解 [Databricks BigQuery](https://docs.databricks.com/data/data-sources/google/bigquery.html)。
* 閱讀[網誌公告](https://databricks.com/blog/2020/07/31/announcing-support-for-google-bigquery-in-databricks-runtime-7-1.html)，瞭解 BigQuery 對 Databricks 的支援。
* 瞭解 [BigQuery 範例筆記本](https://docs.databricks.com/_extras/notebooks/source/big-query-python.html)。
* 瞭解 [Databricks on Google Cloud的 Terraform 供應商](https://github.com/databrickslabs/terraform-provider-databricks/blob/master/CHANGELOG.md)。
* 閱讀 [Databricks 網誌](https://databricks.com/blog/)，包括[資料科學主題](https://databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html)和[資料集](https://databricks.com/blog/2020/04/14/covid-19-datasets-now-available-on-databricks.html)的詳細資訊。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-04 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-04 (世界標準時間)。"],[],[]]