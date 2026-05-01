* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 教學課程：使用特徵向量模型對物件資料表執行推論

本教學課程說明如何根據[花卉資料集](https://www.tensorflow.org/datasets/catalog/tf_flowers?hl=zh-tw)中的圖片建立物件資料表，然後使用 [MobileNet V3 模型](https://tfhub.dev/google/imagenet/mobilenet_v3_small_075_224/feature_vector/5)對該物件資料表執行推論。

## MobileNet V3 模型

MobileNet V3 模型會分析圖片檔案，並傳回特徵向量陣列。特徵向量陣列是描述所分析圖片特徵的數字元素清單。每個特徵向量都會說明多維度特徵空間，並提供圖片在這個空間中的座標。您可以運用圖片的向量資訊進一步分類圖片，例如使用餘弦相似度將類似圖片分組。

MobileNet V3 模型輸入內容會採用 [`DType`](https://www.tensorflow.org/api_docs/python/tf/dtypes/DType?hl=zh-tw)
`tf.float32` 形狀的 `[-1, 224, 224, 3]` 張量。輸出內容是形狀為 `[-1, 1024]` 的張量陣列。`tf.float32`

## 所需權限

* 如要建立資料集，您需要 `bigquery.datasets.create` 權限。
* 如要建立連線資源，您必須具備下列權限：

  + `bigquery.connections.create`
  + `bigquery.connections.get`
* 如要將權限授予連線的服務帳戶，您需要下列權限：

  + `resourcemanager.projects.setIamPolicy`
* 如要建立物件資料表，您必須具備下列權限：

  + `bigquery.tables.create`
  + `bigquery.tables.update`
  + `bigquery.connections.delegate`
* 如要建立 bucket，您必須具備 `storage.buckets.create` 權限。
* 如要將資料集和模型上傳至 Cloud Storage，您需要 `storage.objects.create` 和 `storage.objects.get` 權限。
* 如要將模型載入 BigQuery ML，您需要下列權限：

  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
* 如要執行推論，您需要下列權限：

  + `bigquery.tables.getData` 物件表格
  + 模型上的 `bigquery.models.getData`
  + `bigquery.jobs.create`

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* **BigQuery**: You incur storage costs for the object table
  you create in BigQuery.
* **BigQuery ML**: You incur costs for the model you
  create and the inference you perform in BigQuery ML.
* **Cloud Storage**: You incur costs for the objects you
  store in Cloud Storage.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

如要進一步瞭解 BigQuery 儲存空間定價，請參閱 BigQuery 說明文件中的「[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

如要進一步瞭解 BigQuery ML 定價，請參閱 BigQuery 說明文件中的「[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)」一文。

如要進一步瞭解 Cloud Storage 定價，請參閱 [Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)頁面。

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
- Enable the BigQuery and BigQuery Connection API APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery and BigQuery Connection API APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)

### 建立保留項目

如要搭配物件資料表使用[匯入的模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/inference-overview?hl=zh-tw#inference_using_imported_models)，您必須[建立保留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_reservations)，並使用 BigQuery [Enterprise 或 Enterprise Plus 版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)，然後[建立保留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#create_reservation_assignments)，並使用 `QUERY` 工作類型。

## 建立資料集

建立名為 `mobilenet_inference_test` 的資料集：

### SQL

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「編輯器」窗格中，執行下列 SQL 陳述式：

   ```
   CREATE SCHEMA `PROJECT_ID.mobilenet_inference_test`;
   ```

   將 `PROJECT_ID` 替換為專案 ID。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)
2. 執行 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)來建立資料集：

   ```
   bq mk --dataset --location=us PROJECT_ID:resnet_inference_test
   ```

   將 `PROJECT_ID` 替換為專案 ID。

## 建立連線

建立名為 `lake-connection` 的連線：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中，點選「新增資料」add。

   「新增資料」對話方塊隨即開啟。
4. 在「Filter By」(依據篩選) 窗格的「Data Source Type」(資料來源類型) 專區中，選取「Databases」(資料庫)。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `Vertex AI`。
5. 在「精選資料來源」部分，點選「Vertex AI」。
6. 按一下「Vertex AI Models: BigQuery Federation」解決方案資訊卡。
7. 在「連線類型」清單中，選取「Vertex AI 遠端模型、遠端函式、BigLake 和 Spanner (Cloud 資源)」。
8. 在「連線 ID」欄位中輸入 `lake-connection`。
9. 點選「建立連線」。
10. 在「Explorer」窗格中展開專案，按一下「Connections」，然後選取 `us.lake-connection` 連線。
11. 在「連線資訊」窗格中，複製「服務帳戶 ID」欄位的值。您需要這項資訊，才能在下一個步驟中，[授予權限](#grant-permissions)給您建立的 Cloud Storage bucket 上的連線服務帳戶。

### bq

1. 在 Cloud Shell 中執行 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-connection)，建立連線：

   ```
   bq mk --connection --location=us --connection_type=CLOUD_RESOURCE \
   lake-connection
   ```
2. 執行 [`bq show` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show)，擷取連線相關資訊：

   ```
   bq show --connection us.lake-connection
   ```
3. 從 `properties` 欄複製 `serviceAccountId` 屬性的值，並儲存在某處。您需要這項資訊，才能將權限[授予](#grant-permissions)連線的服務帳戶。

## 建立 Cloud Storage 值區

1. [建立 Cloud Storage 值區](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。
2. 在儲存區中[建立兩個資料夾](https://cloud.google.com/storage/docs/folders?hl=zh-tw#tools)，一個命名為 `mobilenet` (用於存放模型檔案)，另一個命名為 `flowers` (用於存放資料集)。

## 將權限授予連線的服務帳戶

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 點選「授予存取權」。

   「新增主體」對話方塊隨即開啟。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 在「Select a role」(請選擇角色) 欄位中，依序選取「Cloud Storage」和「Storage Object Viewer」(Storage 物件檢視者)。
5. 按一下 [儲存]。

### gcloud

在 Cloud Shell 中執行 [`gcloud storage buckets add-iam-policy-binding` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/storage/buckets/add-iam-policy-binding?hl=zh-tw)：

```
gcloud storage buckets add-iam-policy-binding gs://BUCKET_NAME \
--member=serviceAccount:MEMBER \
--role=roles/storage.objectViewer
```

將 `MEMBER` 換成您先前複製的服務帳戶 ID。將 `BUCKET_NAME` 改成您先前建立的值區名稱。

詳情請參閱「[將主體新增至值區層級政策](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add)」。

**注意：** 新權限最多可能需要一分鐘才會生效。

## 將資料集上傳至 Cloud Storage

取得資料集檔案，並在 Cloud Storage 中提供：

1. [下載](https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz)花朵資料集至本機電腦。
2. 解壓縮 `flower_photos.tgz` 檔案。
3. [上傳](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw) `flower_photos` 資料夾至先前建立值區的 `flowers` 資料夾。
4. 上傳完成後，請刪除 `flower_photos` 資料夾中的 `LICENSE.txt` 檔案。

## 建立物件資料表

根據您上傳的 flowers 資料集，建立名為 `sample_images` 的物件資料表：

### SQL

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「編輯器」窗格中，執行下列 SQL 陳述式：

   ```
   CREATE EXTERNAL TABLE mobilenet_inference_test.sample_images
   WITH CONNECTION `us.lake-connection`
   OPTIONS(
     object_metadata = 'SIMPLE',
     uris = ['gs://BUCKET_NAME/flowers/*']);
   ```

   請將 `BUCKET_NAME` 替換為您先前建立的值區名稱。

### bq

在 Cloud Shell 中執行 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)，建立連線：

```
bq mk --table \
--external_table_definition='gs://BUCKET_NAME/flowers/*@us.lake-connection' \
--object_metadata=SIMPLE \
mobilenet_inference_test.sample_images
```

請將 `BUCKET_NAME` 替換為您先前建立的值區名稱。

## 將模型上傳至 Cloud Storage

取得模型檔案，並在 Cloud Storage 中提供：

1. [下載](https://tfhub.dev/google/imagenet/mobilenet_v3_small_075_224/feature_vector/5?tf-hub-format=compressed)
   MobileNet V3 模型到本機電腦。這會提供模型的 `saved_model.pb` 檔案和 `variables` 資料夾。
2. [上傳](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw) `saved_model.pb` 檔案和 `variables` 資料夾至先前建立的值區中的 `mobilenet` 資料夾。

## 將模型載入 BigQuery ML

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「編輯器」窗格中，執行下列 SQL 陳述式：

   ```
   CREATE MODEL `mobilenet_inference_test.mobilenet`
   OPTIONS(
     model_type = 'TENSORFLOW',
     model_path = 'gs://BUCKET_NAME/mobilenet/*');
   ```

   將 `BUCKET_NAME` 替換為您先前建立的值區名稱。

## 檢查模型

檢查上傳的模型，查看輸入和輸出欄位：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下 `mobilenet_inference_test` 資料集。
4. 前往「模型」分頁。
5. 按一下 `mobilenet` 模型。
6. 在隨即開啟的模型窗格中，按一下「結構定義」分頁標籤。
7. 查看「標籤」部分。這會識別模型輸出的欄位。在本例中，欄位名稱值為 `feature_vector`。
8. 查看「功能」部分。這會指出必須輸入模型中的欄位。您可以在 `SELECT` 陳述式中參照這些函式，以供 `ML.DECODE_IMAGE` 函式使用。在本例中，欄位名稱值為 `inputs`。

## 執行推論

使用 `mobilenet` 模型對 `sample_images` 物件資料表執行推論：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「編輯器」窗格中，執行下列 SQL 陳述式：

   ```
   SELECT *
   FROM ML.PREDICT(
     MODEL `mobilenet_inference_test.mobilenet`,
     (SELECT uri, ML.RESIZE_IMAGE(ML.DECODE_IMAGE(data), 224, 224, FALSE) AS inputs
     FROM mobilenet_inference_test.sample_images)
   );
   ```

   結果應如下所示：

   ```
   --------------------------------------------------------------------------------------------------------------
   | feature_vector         | uri                                                        | inputs               |
   —-------------------------------------------------------------------------------------------------------------
   | 0.850297749042511      | gs://mybucket/flowers/dandelion/3844111216_742ea491a0.jpg  | 0.29019609093666077  |
   —-------------------------------------------------------------------------------------------------------------
   | -0.27427938580513      |                                                            | 0.31372550129890442  |
   —-------------------------                                                            ------------------------
   | -0.23189745843410492   |                                                            | 0.039215687662363052 |
   —-------------------------                                                            ------------------------
   | -0.058292809873819351  |                                                            | 0.29985997080802917  |
   —-------------------------------------------------------------------------------------------------------------
   ```

## 清除所用資源

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]