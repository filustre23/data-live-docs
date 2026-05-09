Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 ONNX 格式的 PyTorch 模型進行預測 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

[開放式神經網路交換格式](https://onnx.ai/) (ONNX) 提供統一格式，可表示任何機器學習架構。BigQuery ML 支援 ONNX，因此您可以：

* 使用您喜愛的架構訓練模型。
* 將模型轉換為 ONNX 模型格式。
* 將 ONNX 模型匯入 BigQuery，並使用 BigQuery ML 進行預測。

本教學課程說明如何將使用 [PyTorch](https://pytorch.org/) 訓練的 ONNX 模型匯入 BigQuery 資料集，並使用這些模型預測 SQL 查詢。

**重要事項：** 如要使用匯入的模型和物件資料表執行預測，必須先預訂資源。詳情請參閱「[匯入 ONNX 模型時的限制](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw#limitations)」。

## 目標

* 使用 [PyTorch](https://pytorch.org/) 匯入預先訓練模型。
* 使用 [torch.onnx](https://pytorch.org/docs/stable/onnx.html) [將模型轉換為 ONNX 格式](https://github.com/onnx/tutorials#converting-to-onnx-format)。
* 使用 `CREATE MODEL` 陳述式將 ONNX 模型匯入 BigQuery。
* 使用 `ML.PREDICT` 函式，透過匯入的 ONNX 模型進行預測。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [BigQuery ML](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)
* [Cloud Storage](https://docs.cloud.google.com/storage/pricing?hl=zh-tw)

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

完成本文所述工作後，您可以刪除建立的資源，避免繼續計費，詳情請參閱「[清除所用資源](#clean-up)」。

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
2. 啟用 BigQuery、BigQuery Connection 和 Cloud Storage API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cstorage-component.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)
3. 請確認您具備[必要權限](#required_roles)，可執行本文件中的工作。

### 必要的角色

如果您建立新專案，您就是專案擁有者，並已獲得完成本教學課程所需的所有 Identity and Access Management (IAM) 權限。

如果您使用現有專案，請執行下列操作。

請確認您在專案中具備下列角色：

* [BigQuery Studio 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser) (`roles/bigquery.studioAdmin`)
* [BigQuery Connection 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.connectionAdmin) (`roles/bigquery.connectionAdmin`)
* [儲存空間管理員](https://docs.cloud.google.com/storage/docs/access-control/iam-roles?hl=zh-tw#standard-roles) `(roles/storage.admin)`

#### 檢查角色

1. 前往 Google Cloud 控制台的「IAM」頁面。

   [前往「IAM」頁面](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
2. 選取專案。
3. 在「主體」欄中，找出所有識別您或您所屬群組的資料列。如要瞭解自己所屬的群組，請與管理員聯絡。
4. 針對指定或包含您的所有列，請檢查「角色」欄，確認角色清單是否包含必要角色。


#### 授予角色

1. 前往 Google Cloud 控制台的「IAM」頁面。

   [前往「IAM」頁面](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
2. 選取專案。
3. 按一下person\_add「Grant access」(授予存取權)。
4. 在「New principals」(新增主體) 欄位中，輸入您的使用者 ID。 這通常是指 Google 帳戶的電子郵件地址。
5. 按一下「選取角色」，然後搜尋角色。
6. 如要授予其他角色，請按一下add「Add another role」(新增其他角色)，然後新增其他角色。
7. 按一下「Save」(儲存)。

如要進一步瞭解 BigQuery 中的 IAM 權限，請參閱 [IAM 權限](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)。

## 選用：訓練模型並轉換為 ONNX 格式

下列程式碼範例說明如何將預先訓練的分類模型匯入 PyTorch，以及如何將產生的模型轉換為 ONNX 格式。本教學課程使用儲存在 `gs://cloud-samples-data/bigquery/ml/onnx/resnet18.onnx` 的預先建構範例模型。如果您使用範例模型，則不必完成這些步驟。

### 建立圖片分類的 PyTorch 視覺模型

請使用下列程式碼範例匯入 PyTorch 預先訓練的 [resnet18](https://pytorch.org/vision/main/models/generated/torchvision.models.resnet18.html) 模型，該模型會接受 BigQuery ML [`ML.DECODE_IMAGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-decode-image?hl=zh-tw) 和 [`ML.RESIZE_IMAGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-resize-image?hl=zh-tw) 函式傳回的已解碼圖片資料。

```
import torch
import torch.nn as nn

# Define model input format to match the output format of
# ML.DECODE_IMAGE function: [height, width, channels]
dummy_input = torch.randn(1, 224, 224, 3, device="cpu")

# Load a pretrained pytorch model for image classification
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)

# Reshape input format from [batch_size, height, width, channels]
# to [batch_size, channels, height, width]
class ReshapeLayer(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        x = x.permute(0, 3, 1, 2)  # reorder dimensions
        return x

class ArgMaxLayer(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
       return torch.argmax(x, dim=1)

final_model = nn.Sequential(
    ReshapeLayer(),
    model,
    nn.Softmax(),
    ArgMaxLayer()
)
```

### 將模型轉換為 ONNX 格式

請使用下列範例，透過 [torch.onnx](https://pytorch.org/docs/stable/onnx.html) 匯出 PyTorch 視覺模型。匯出的 ONNX 檔案名稱為 `resnet18.onnx`。

```
torch.onnx.export(final_model,            # model being run
                  dummy_input,            # model input
                  "resnet18.onnx",        # where to save the model
                  opset_version=10,       # the ONNX version to export the model to
                  input_names = ['input'],         # the model's input names
                  output_names = ['class_label'])  # the model's output names
```

### 將 ONNX 模型上傳至 Cloud Storage

儲存模型後，請按照下列步驟操作：

* [建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw) 來儲存模型。
* [將 ONNX 模型上傳至 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)。

## 建立資料集

建立 BigQuery 資料集來儲存機器學習模型。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下專案名稱。
3. 依序點按 more\_vert「View actions」(查看動作) >「Create dataset」(建立資料集)
4. 在「建立資料集」頁面中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 針對「位置類型」選取「多區域」，然後選取「美國」。
   * 其餘設定請保留預設狀態，然後按一下「建立資料集」。

### bq

如要建立新的資料集，請使用 [`bq mk --dataset` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)。

1. 建立名為 `bqml_tutorial` 的資料集，並將資料位置設為 `US`。

   ```
   bq mk --dataset \
     --location=US \
     --description "BigQuery ML tutorial dataset." \
     bqml_tutorial
   ```
2. 確認資料集已建立完成：

   ```
   bq ls
   ```

### API

請呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法，搭配已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)。

```
{
  "datasetReference": {
     "datasetId": "bqml_tutorial"
  }
}
```

## 將 ONNX 模型匯入 BigQuery

下列步驟說明如何使用 [`CREATE MODEL`](https://pytorch.org/vision/main/models/generated/torchvision.models.resnet18.html) 陳述式，將 Cloud Storage 中的 ONNX 範例模型匯入資料集。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列 [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw) 陳述式。

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.imported_onnx_model`
    OPTIONS (MODEL_TYPE='ONNX',
     MODEL_PATH='BUCKET_PATH')
   ```

   請將 `BUCKET_PATH` 改成您上傳至 Cloud Storage 的模型路徑。如果您使用範例模型，請將 `BUCKET_PATH` 替換為下列值：`gs://cloud-samples-data/bigquery/ml/onnx/resnet18.onnx`。

   作業完成後，您會看到類似以下的訊息：`Successfully created model named imported_onnx_model`。

   新模型會顯示在「資源」面板中。模型會以模型圖示來表示：

### bq

1. 輸入下列 `CREATE MODEL` 陳述式，從 Cloud Storage 匯入 ONNX 模型。

   ```
   bq query --use_legacy_sql=false \
   "CREATE OR REPLACE MODEL
     `bqml_tutorial.imported_onnx_model`
   OPTIONS
     (MODEL_TYPE='ONNX',
      MODEL_PATH='BUCKET_PATH')"
   ```

   請將 `BUCKET_PATH` 改成您上傳至 Cloud Storage 的模型路徑。如果您使用範例模型，請將 `BUCKET_PATH` 替換為這個值：`gs://cloud-samples-data/bigquery/ml/onnx/resnet18.onnx`。
2. 匯入模型後，請確認模型是否顯示在資料集中。

   ```
   bq ls -m bqml_tutorial
   ```

   輸出結果會與下列內容相似：

   ```
   tableId               Type
   --------------------- -------
   imported_onnx_model  MODEL
   ```

如要進一步瞭解如何將 ONNX 模型匯入 BigQuery，包括格式和儲存空間需求，請參閱[匯入 ONNX 模型的 `CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw)。

## 在 BigQuery 建立物件資料表，用於分析圖片資料

[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)是位於 Cloud Storage 中的非結構化資料物件的唯讀資料表。物件資料表可讓您透過 BigQuery 分析非結構化資料。

在本教學課程中，您將使用 `ML.PREDICT` 函式，輸出儲存在 Cloud Storage bucket 中輸入圖片的預測類別標籤。

建立物件資料表時，您需要執行下列操作：

* 建立 Cloud Storage bucket，並上傳金魚圖片。
* 建立 Cloud 資源連結，用於存取物件資料表。
* 將存取權授予資源連線的服務帳戶。

### 建立 bucket 並上傳圖片

請按照下列步驟建立 Cloud Storage bucket，並上傳金魚圖片。

### 控制台

**注意：** 使用 Google Cloud 控制台建立 bucket 時，您只需要為 bucket 設定全域不重複的名稱；其他步驟都是選用或預設設定。

1. 前往 Google Cloud 控制台的「Cloud Storage bucket」頁面。  

   [前往「Buckets」(值區) 頁面](https://console.cloud.google.com/storage/browser?hl=zh-tw)
2. 點選 add\_box「建立」。
3. 在「建立 bucket」頁面中，輸入 bucket 資訊。

   1. 在「開始使用」部分，執行下列操作：

      1. 在方塊中輸入 `bqml_images`。
      2. 按一下「繼續」。
   2. 在「Choose where to store your data」(選擇資料的儲存位置) 部分，執行下列操作：

      1. 「位置類型」請選取「多區域」。
      2. 從位置類型選單中，選取「US (多個美國區域)」。
      3. 按一下「繼續」。
   3. 在「為資料選擇儲存空間級別」專區中：

      1. 選取「設定預設級別」。
      2. 選取「標準」。
      3. 按一下「繼續」。
   4. 其餘區段則保留預設值。
4. 點選「建立」。

### 指令列

輸入下列 `gcloud storage buckets create` 指令：

```
gcloud storage buckets create gs://bqml_images --location=us
```

如果要求成功，指令會傳回下列訊息：

```
Creating gs://bqml_images/...
```

### 將圖片上傳至 Cloud Storage bucket

建立 bucket 後，請下載金魚圖片，然後上傳至 Cloud Storage bucket。

如要上傳圖片，請完成下列步驟：

### 控制台

1. 前往 Google Cloud 控制台的「Cloud Storage bucket」頁面。  

   [前往「Buckets」(值區) 頁面](https://console.cloud.google.com/storage/browser?hl=zh-tw)
2. 在 bucket 清單中，點按「`bqml_images`」。
3. 在值區的「物件」分頁中，執行下列任一操作：

   * 將檔案從桌面或檔案管理員拖曳到 Google Cloud 控制台的主要窗格。
   * 依序點選「上傳」**>「上傳檔案」**，在出現的對話方塊中選取要上傳的圖片檔，然後按一下「開啟」。

### 指令列

輸入下列 `gcloud storage cp` 指令：

```
gcloud storage cp OBJECT_LOCATION gs://bqml_images/IMAGE_NAME
```

更改下列內容：

* `OBJECT_LOCATION`：圖片檔案的本機路徑。例如：`Desktop/goldfish.jpg`。
* `IMAGE_NAME`：圖片名稱。例如：`goldfish.jpg`。

如果成功，回應會類似以下內容：

```
Completed files 1/1 | 164.3kiB/164.3kiB
```

### 建立 BigQuery Cloud 資源連線

您必須擁有 Cloud 資源連結，才能連線至本教學課程稍後建立的[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)。

您可以透過雲端資源連線，查詢儲存在 BigQuery 外部的資料，例如 Cloud Storage 或 Spanner 等 Google Cloud 服務，或是 AWS 或 Azure 等第三方來源。這些外部連結會使用 BigQuery Connection API。

請按照下列步驟建立 Cloud 資源連線。

### 控制台

1. 前往「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中，點選「新增資料」add。

   「新增資料」對話方塊隨即開啟。
4. 在「依條件篩選」窗格的「資料來源類型」部分，選取「資料庫」。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `Vertex AI`。
5. 在「精選資料來源」部分，點選「Vertex AI」。
6. 按一下「Vertex AI Models: BigQuery Federation」解決方案資訊卡。
7. 在「連線類型」清單中，選取「Vertex AI 遠端模型、遠端函式和 BigLake (Cloud 資源)」。
8. 在「連線 ID」欄位中輸入 `bqml_tutorial`。
9. 確認已選取「多區域 - 美國」。
10. 點選「建立連線」。
11. 按一下視窗底部的「前往連線」。或者，在「Explorer」窗格中，依序點選「Connections」和 **`us.bqml_tutorial`**。
12. 在「連線資訊」窗格中，複製服務帳戶 ID。設定連線的權限時，您需要這個 ID。建立連線資源時，BigQuery 會建立專屬的系統服務帳戶，並將其與連線建立關聯。

### bq

1. 建立連線：

   ```
   bq mk --connection --location=US --project_id=PROJECT_ID \
       --connection_type=CLOUD_RESOURCE bqml_tutorial
   ```

   將 `PROJECT_ID` 替換為Google Cloud 專案 ID。`--project_id` 參數會覆寫預設專案。

   建立連線資源時，BigQuery 會建立專屬的系統服務帳戶，並將其與連線建立關聯。

   **疑難排解**：如果收到下列連線錯誤訊息，請[更新 Google Cloud SDK](https://docs.cloud.google.com/sdk/docs/quickstart?hl=zh-tw)：

   ```
   Flags parsing error: flag --connection_type=CLOUD_RESOURCE: value should be one of...
   ```
2. 擷取並複製服務帳戶 ID，以供後續步驟使用：

   ```
   bq show --connection PROJECT_ID.us.bqml_tutorial
   ```

   輸出結果會與下列內容相似：

   ```
   name                          properties
   1234.REGION.CONNECTION_ID {"serviceAccountId": "connection-1234-9u56h9@gcp-sa-bigquery-condel.iam.gserviceaccount.com"}
   ```

### 設定連線存取權

將 Storage 物件管理員角色授予 Cloud 資源連線的服務帳戶。您必須在上傳圖片檔案的專案中授予這個角色。

**注意：** 如果連線位於不同專案，系統會傳回以下錯誤：
`bqcx-1234567890-xxxx@gcp-sa-bigquery-condel.iam.gserviceaccount.com does not have the permission to access
resource`。

如要授予角色，請按照下列步驟操作：

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)
2. 按一下 person\_add「授予存取權」。
3. 在「新增主體」欄位，輸入先前複製的 Cloud 資源連結服務帳戶 ID。
4. 在「Select a role」(請選擇角色) 欄位中，依序選取「Cloud Storage」和「Storage object admin」(Storage 物件管理員)。
5. 按一下 [儲存]。

### 建立物件資料表

請按照下列步驟，使用您上傳至 Cloud Storage 的金魚圖片，建立名為 `goldfish_image_table` 的物件資料表。

### 控制台

1. 前往「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)
2. 在查詢編輯器中輸入這項查詢，即可建立物件資料表。

   ```
   CREATE EXTERNAL TABLE `bqml_tutorial.goldfish_image_table`
   WITH CONNECTION `us.bqml_tutorial`
   OPTIONS(
   object_metadata = 'SIMPLE',
   uris = ['gs://bqml_images/IMAGE_NAME'],
   max_staleness = INTERVAL 1 DAY,
   metadata_cache_mode = 'AUTOMATIC');
   ```

   將 `IMAGE_NAME` 替換成圖片檔案的名稱，例如 `goldfish.jpg`。

   作業完成後，您會看到類似 `This statement created a new table named goldfish_image_table` 的訊息。

### bq

1. 輸入下列 `CREATE EXTERNAL TABLE` 陳述式，建立物件資料表。

   ```
   bq query --use_legacy_sql=false \
   "CREATE EXTERNAL TABLE `bqml_tutorial.goldfish_image_table`
   WITH CONNECTION `us.bqml_tutorial`
   OPTIONS(
   object_metadata = 'SIMPLE',
   uris = ['gs://bqml_images/IMAGE_NAME'],
   max_staleness = INTERVAL 1 DAY,
   metadata_cache_mode = 'AUTOMATIC')"
   ```

   將 `IMAGE_NAME` 替換成圖片檔案的名稱，例如 `goldfish.jpg`。
2. 建立物件資料表後，請確認該資料表是否顯示在資料集中。

   ```
   bq ls bqml_tutorial
   ```

   輸出結果會與下列內容相似：

   ```
   tableId               Type
   --------------------- --------
   goldfish_image_table  EXTERNAL
   ```

詳情請參閱「[建立物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)」。

## 使用匯入的 ONNX 模型進行預測

**重要事項：**您必須預訂，才能使用匯入的模型和物件表格執行預測。詳情請參閱有關匯入 ONNX 模型的[限制](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw#limitations)。  
  
如果沒有預訂，使用 `ML.PREDICT` 執行查詢會產生這項錯誤：`` BigQuery ML inference using imported models and
object tables requires a reservation, but no reservations were assigned for
job type `QUERY`...` ``。

您可以使用下列包含 [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw) 函式的查詢，根據輸入物件資料表 `goldfish_image_table` 中的圖片資料進行預測。這項查詢會根據 [ImageNet 標籤](https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt)字典，輸出輸入圖片的預測類別標籤。

在查詢中，您必須使用 [`ML.DECODE_IMAGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-decode-image?hl=zh-tw) 函式解碼圖片資料，`ML.PREDICT` 才能解讀資料。系統會呼叫 [`ML.RESIZE_IMAGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-resize-image?hl=zh-tw) 函式，將圖片大小調整為符合模型輸入大小 (224\*224)。

如要進一步瞭解如何對圖片物件資料表執行推論，請參閱[對圖片物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/object-table-inference?hl=zh-tw)。

如要根據圖片資料進行預測，請按照下列步驟操作。

### 控制台

1. 前往「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列 `ML.PREDICT` 查詢。

   ```
    SELECT
      class_label
    FROM
      ML.PREDICT(MODEL bqml_tutorial.imported_onnx_model,
        (
        SELECT
          ML.RESIZE_IMAGE(ML.DECODE_IMAGE(DATA),
            224,
            224,
            FALSE) AS input
        FROM
          bqml_tutorial.goldfish_image_table))
   ```

   查詢結果類似於下列內容：

### bq

輸入下列 `bq query` 指令：

```
bq query --use_legacy_sql=false \
'SELECT
  class_label
FROM
  ML.PREDICT(MODEL `bqml_tutorial.imported_onnx_model`,
    (
    SELECT
      ML.RESIZE_IMAGE(ML.DECODE_IMAGE(DATA),
        224,
        224,
        FALSE) AS input
    FROM
      bqml_tutorial.goldfish_image_table))'
```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

### 控制台

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### gcloud

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

刪除 Google Cloud 專案：

```
gcloud projects delete PROJECT_ID
```

### 刪除個別資源

或者，如要移除本教學課程中使用的個別資源，請執行下列操作：

1. [刪除匯入的模型](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw)。
2. (選用) [刪除資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#delete-datasets)。
3. [刪除 Cloud 資源連線](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#delete-connections)。
4. [刪除 Cloud Storage 值區](https://cloud.google.com/storage/docs/deleting-buckets?hl=zh-tw#delete-bucket)。

## 後續步驟

* 如要進一步瞭解如何匯入 ONNX 模型，請參閱「[ONNX 模型的 `CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw)」。
* 如要進一步瞭解可用的 ONNX 轉換器和教學課程，請參閱「[轉換為 ONNX 格式](https://github.com/onnx/tutorials#converting-to-onnx-format)」。
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要開始使用 BigQuery ML，請參閱[在 BigQuery ML 中建立機器學習模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]