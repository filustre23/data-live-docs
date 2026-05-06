Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 教學課程：使用分類模型對物件資料表執行推論

本教學課程說明如何根據公開資料集的圖片建立物件資料表，然後使用 [ResNet 50 模型](https://tfhub.dev/tensorflow/resnet_50/classification/1)對該物件資料表執行推論。

## ResNet 50 模型

ResNet 50 模型會分析圖片檔案，並輸出代表圖片屬於相應類別可能性的向量批次 (logits)。詳情請參閱[模型 TensorFlow Hub 頁面](https://tfhub.dev/tensorflow/resnet_50/classification/1)的「用法」一節。

ResNet 50 模型輸入會採用 [`DType`](https://www.tensorflow.org/api_docs/python/tf/dtypes/DType?hl=zh-tw) = `float32` 形狀的張量 `float32`。`[-1, 224, 224, 3]`輸出內容是形狀為 `[-1, 1024]` 的張量陣列。`tf.float32`

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
* 如要將模型上傳至 Cloud Storage，您需要 `storage.objects.create` 和 `storage.objects.get` 權限。
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

建立名為 `resnet_inference_test` 的資料集：

### SQL

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「編輯器」窗格中，執行下列 SQL 陳述式：

   ```
   CREATE SCHEMA `PROJECT_ID.resnet_inference_test`;
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
10. 在「連線資訊」窗格，複製「服務帳戶 ID」欄位的值，並儲存在任意位置。您需要這項資訊，才能[授予連線服務帳戶權限](#grant-permissions)。

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

[建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)，存放模型檔案。

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

## 建立物件資料表

根據公開 `gs://cloud-samples-data/vision` bucket 中的圖片檔案，建立名為 `vision_images` 的物件資料表：

### SQL

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「編輯器」窗格中，執行下列 SQL 陳述式：

   ```
   CREATE EXTERNAL TABLE resnet_inference_test.vision_images
   WITH CONNECTION `us.lake-connection`
   OPTIONS(
     object_metadata = 'SIMPLE',
     uris = ['gs://cloud-samples-data/vision/*.jpg']
   );
   ```

### bq

在 Cloud Shell 中執行 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)，建立連線：

```
bq mk --table \
--external_table_definition='gs://cloud-samples-data/vision/*.jpg@us.lake-connection' \
--object_metadata=SIMPLE \
resnet_inference_test.vision_images
```

## 將模型上傳至 Cloud Storage

取得模型檔案，並在 Cloud Storage 中提供：

1. [下載](https://tfhub.dev/tensorflow/resnet_50/classification/1?tf-hub-format=compressed)
   ResNet 50 模型至本機電腦。這會提供模型的 `saved_model.pb` 檔案和 `variables` 資料夾。
2. [上傳](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw) `saved_model.pb` 檔案和 `variables` 資料夾到先前建立的 bucket。

## 將模型載入 BigQuery ML

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「編輯器」窗格中，執行下列 SQL 陳述式：

   ```
   CREATE MODEL `resnet_inference_test.resnet`
   OPTIONS(
     model_type = 'TENSORFLOW',
     model_path = 'gs://BUCKET_NAME/*');
   ```

   將 `BUCKET_NAME` 替換為您先前建立的值區名稱。

## 檢查模型

檢查上傳的模型，查看輸入和輸出欄位：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下 `resnet_inference_test` 資料集。
4. 前往「模型」分頁。
5. 按一下 `resnet` 模型。
6. 在隨即開啟的模型窗格中，按一下「結構定義」分頁標籤。
7. 查看「標籤」部分。這會識別模型輸出的欄位。在本例中，欄位名稱值為 `activation_49`。
8. 查看「功能」部分。這會指出必須輸入模型中的欄位。您可以在 `SELECT` 陳述式中參照這些函式，以供 `ML.DECODE_IMAGE` 函式使用。在本例中，欄位名稱值為 `input_1`。

## 執行推論

使用 `resnet` 模型對 `vision_images` 物件資料表執行推論：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「編輯器」窗格中，執行下列 SQL 陳述式：

   ```
   SELECT *
   FROM ML.PREDICT(
     MODEL `resnet_inference_test.resnet`,
     (SELECT uri, ML.RESIZE_IMAGE(ML.DECODE_IMAGE(data), 224, 224, FALSE) AS input_1
     FROM resnet_inference_test.vision_images)
   );
   ```

   結果應如下所示：

   ```
   -------------------------------------------------------------------------------------------------------------------------------------
   | activation_49           | uri                                                                                           | input_1 |
   —------------------------------------------------------------------------------------------------------------------------------------
   | 1.0254175464297077e-07  | gs://cloud-samples-data/vision/automl_classification/flowers/daisy/21652746_cc379e0eea_m.jpg  | 0.0     |
   —------------------------------------------------------------------------------------------------------------------------------------
   | 2.1671139620593749e-06  |                                                                                               | 0.0     |
   —--------------------------                                                                                               -----------
   | 8.346052027263795e-08   |                                                                                               | 0.0     |
   —--------------------------                                                                                               -----------
   | 1.159310958342985e-08   |                                                                                               | 0.0     |
   —------------------------------------------------------------------------------------------------------------------------------------
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

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]