Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 對圖片物件資料表執行推論

**注意：** 如果預留項目是以特定 BigQuery 版本建立，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

本文說明如何使用 BigQuery ML，對圖片[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)執行推論。

您可以將物件資料表做為 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)的輸入內容，對圖片資料執行推論。

為此，您必須先選擇合適的模型，將其上傳至 Cloud Storage，然後執行 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)，將模型匯入 BigQuery。您可以自行建立模型，也可以從 [TensorFlow Hub](https://tfhub.dev/) 下載模型。

## 限制

* 只有在透過預留項目使用依容量計價模式時，才能搭配物件資料表使用 BigQuery ML [匯入的模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/inference-overview?hl=zh-tw#inference_using_imported_models)；不支援隨選計價模式。
* 與物件表格相關聯的圖片檔必須符合下列規定：
  + 大小不超過 20 MB。
  + 格式為 JPEG、PNG 或 BMP。
* 與物件資料表相關聯的圖片檔總大小必須小於 1 TB。
* 為獲得最佳清單和查詢效能，請在物件資料表的 `uris` 選項中，指定最多 10 個來源 URI。如果指定超過 10 個 bucket URI，物件資料表可支援的檔案總數會減少，且列出大量檔案時，查詢可能會因 `Resources exceeded during query execution` 記憶體錯誤而失敗。如需參照超過 10 個 bucket，請將這些 bucket 分散到多個物件資料表。
* 模型必須是下列其中一項：

  + [SavedModel](https://www.tensorflow.org/guide/saved_model?hl=zh-tw) 格式的 [TensorFlow](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw) 或 [TensorFlow Lite](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tflite?hl=zh-tw) 模型。
  + [ONNX 格式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw)的 PyTorch 模型。
* 模型必須符合[匯入 TensorFlow 模型的 `CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw)中所述的輸入需求和限制。
* 模型的序列化大小必須小於 450 MB。
* 模型反序列化 (記憶體內) 的大小必須小於 1000 MB。
* 模型輸入張量必須符合下列條件：

  + 資料類型為 `tf.float32`，值為 `[0, 1)`，或資料類型為 `tf.uint8`，值為 `[0, 255)`。
  + 形狀為 `[batch_size, width, height, 3]`，其中：
    - `batch_size` 必須是 `-1`、`None` 或 `1`。
    - `width`和`height`必須大於 0。
* 模型必須使用下列其中一種色域的圖片進行訓練：

  + `RGB`
  + `HSV`
  + `YIQ`
  + `YUV`
  + `GRAYSCALE`

  您可以使用 [`ML.CONVERT_COLOR_SPACE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-convert-color-space?hl=zh-tw)，將輸入圖片轉換為模型訓練時使用的色域。

## 範例模型

TensorFlow Hub 上的下列模型可與 BigQuery ML 和圖片物件資料表搭配使用：

* [ResNet 50](https://tfhub.dev/tensorflow/resnet_50/classification/1)。如要試用這個模型，請參閱「[教學課程：使用分類模型對物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/inference-tutorial-resnet?hl=zh-tw)」。
* [MobileNet V3](https://tfhub.dev/google/imagenet/mobilenet_v3_small_075_224/feature_vector/5)。如要嘗試使用這個模型，請參閱「[教學課程：使用特徵向量模型對物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/inference-tutorial-mobilenet?hl=zh-tw)」。

## 所需權限

* 如要將模型上傳至 Cloud Storage，您需要 `storage.objects.create` 和 `storage.objects.get` 權限。
* 如要將模型載入 BigQuery ML，您需要下列權限：

  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
* 如要執行推論，您必須具備下列權限：

  + 物件資料表中的 `bigquery.tables.getData`
  + `bigquery.models.getData`模型
  + `bigquery.jobs.create`

## 事前準備

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
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
- Enable the BigQuery and BigQuery Connection API APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery and BigQuery Connection API APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)

## 將模型上傳至 Cloud Storage

如要上傳模型，請按照下列步驟操作：

1. 如果您已建立自己的模型，請將模型儲存至本機。如果使用 TensorFlow Hub 的模型，請下載到本機電腦。如果使用 TensorFlow，您應該會取得模型的 `saved_model.pb` 檔案和 `variables` 資料夾。
2. 如有需要，請[建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。
3. 將模型構件[上傳](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)至 bucket。

## 將模型載入 BigQuery ML

載入適用於圖片物件資料表的模型，與載入適用於結構化資料的模型相同。請按照下列步驟將模型載入 BigQuery ML：

```
CREATE MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`
OPTIONS(
  model_type = 'MODEL_TYPE',
  model_path = 'BUCKET_PATH');
```

替換下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：要包含模型的資料集 ID。
* `MODEL_NAME`：模型名稱。
* `MODEL_TYPE`：請使用下列其中一個值：
  + TensorFlow 模型的 `TENSORFLOW`
  + ONNX 格式 PyTorch 模型的 `ONNX`
* `BUCKET_PATH`：模型所在 Cloud Storage bucket 的路徑，格式為 `[gs://bucket_name/[folder_name/]*]`。

下列範例使用預設專案，並使用 `gs://my_bucket/my_model_folder` 中的 `saved_model.pb` 檔案和 `variables` 資料夾，將 TensorFlow 模型載入 BigQuery ML 做為 `my_vision_model`：

```
CREATE MODEL `my_dataset.my_vision_model`
OPTIONS(
  model_type = 'TENSORFLOW',
  model_path = 'gs://my_bucket/my_model_folder/*');
```

## 檢查模型

您可以檢查上傳的模型，查看其輸入和輸出欄位。對物件資料表執行推論時，您需要參照這些欄位。

如要檢查模型，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後點選「資料集」。
4. 按一下包含模型的資料集。
5. 點選「Models」分頁標籤。
6. 在開啟的模型窗格中，按一下「結構定義」分頁標籤。
7. 查看「標籤」部分。這會識別模型輸出的欄位。
8. 查看「功能」部分。這會指出必須輸入模型的欄位。您可以在 `ML.DECODE_IMAGE` 函式的 `SELECT` 陳述式中參照這些引數。

如要進一步檢查 TensorFlow 模型，例如判斷模型輸入的形狀，請[安裝 TensorFlow](https://www.tensorflow.org/install?hl=zh-tw) 並使用 [`saved_model_cli show` 指令](https://www.tensorflow.org/guide/saved_model?hl=zh-tw#show_command)。

## 預先處理圖片

您必須使用 [`ML.DECODE_IMAGE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-decode-image?hl=zh-tw)，將圖片位元組轉換為多維 `ARRAY` 表示法。您可以直接在 `ML.PREDICT` 函式中使用 `ML.DECODE_IMAGE` 輸出內容，也可以將 `ML.DECODE_IMAGE` 的結果寫入資料表資料欄，並在呼叫 `ML.PREDICT` 時參照該資料欄。

以下範例會將 `ML.DECODE_IMAGE` 函式的輸出內容寫入資料表：

```
CREATE OR REPLACE TABLE mydataset.mytable AS (
  SELECT ML.DECODE_IMAGE(data) AS decoded_image FROM mydataset.object_table
  );
```

使用下列函式進一步處理圖片，以便與模型搭配使用：

* [`ML.CONVERT_COLOR_SPACE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-convert-color-space?hl=zh-tw)會將具有 `RGB` 色域的圖片轉換為其他色域。
* [`ML.CONVERT_IMAGE_TYPE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-convert-image-type?hl=zh-tw)會將 [`ML.DECODE_IMAGE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-decode-image?hl=zh-tw)輸出的像素值，從浮點數轉換為範圍為 `[0, 255)` 的整數。
* [`ML.RESIZE_IMAGE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-resize-image?hl=zh-tw)會調整圖片大小。

您可以將這些函式做為 `ML.PREDICT` 函式的一部分，或在包含 `ML.DECODE_IMAGE` 輸出圖片資料的資料表資料欄上執行。

## 執行推論

載入適當的模型，並視需要預先處理圖片資料後，即可對圖片資料執行推論。

如要執行推論，請按照下列步驟操作：

```
SELECT *
FROM ML.PREDICT(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  (SELECT [other columns from the object table,] IMAGE_DATA AS MODEL_INPUT
  FROM PROJECT_ID.DATASET_ID.TABLE_NAME)
);
```

替換下列內容：

* `PROJECT_ID`：模型和物件資料表所在專案的專案 ID。
* `DATASET_ID`：包含模型和物件資料表的資料集 ID。
* `MODEL_NAME`：模型名稱。
* `IMAGE_DATA`：圖片資料，由 `ML.DECODE_IMAGE` 函式的輸出內容表示，或由包含 `ML.DECODE_IMAGE` 或其他圖片處理函式輸出圖片資料的資料表資料欄表示。
* `MODEL_INPUT`：模型的輸入欄位名稱。如要查看這項資訊，請[檢查模型](https://docs.cloud.google.com/bigquery/docs/object-table-inference?hl=zh-tw#inspect_the_model)，並查看「Features」(特徵) 區段中的欄位名稱。
* `TABLE_NAME`：物件資料表的名稱。

### 範例

**範例 1**

以下範例直接在 `ML.PREDICT` 函式中使用 `ML.DECODE_IMAGE` 函式。如果模型的輸入欄位為 `input`，輸出欄位為 `feature`，則會傳回物件資料表中所有圖片的推論結果：

```
SELECT * FROM
ML.PREDICT(
  MODEL `my_dataset.vision_model`,
  (SELECT uri, ML.RESIZE_IMAGE(ML.DECODE_IMAGE(data), 480, 480, FALSE) AS input
  FROM `my_dataset.object_table`)
);
```

**示例 2**

以下範例直接在 `ML.PREDICT` 函式中使用 `ML.DECODE_IMAGE` 函式，並在 `ML.PREDICT` 函式中使用 `ML.CONVERT_COLOR_SPACE` 函式，將圖片色域從 `RBG` 轉換為 `YIQ`。此外，也會說明如何使用物件資料表欄位，篩選推論中包含的物件。如果模型的輸入欄位為 `input`，輸出欄位為 `feature`，則會傳回物件資料表中所有 JPG 圖片的推論結果：

```
SELECT * FROM
  ML.PREDICT(
    MODEL `my_dataset.vision_model`,
    (SELECT uri, ML.CONVERT_COLOR_SPACE(ML.RESIZE_IMAGE(ML.DECODE_IMAGE(data), 224, 280, TRUE), 'YIQ') AS input
    FROM `my_dataset.object_table`
    WHERE content_type = 'image/jpeg')
  );
```

**範例 3**

以下範例使用已寫入資料表資料欄，但未進一步處理的 `ML.DECODE_IMAGE` 結果。它會使用 `ML.PREDICT` 函式中的 `ML.RESIZE_IMAGE` 和 `ML.CONVERT_IMAGE_TYPE` 處理圖片資料。如果模型的輸入欄位為 `input`，輸出欄位為 `feature`，則會傳回解碼圖片資料表中所有圖片的推論結果。

建立解碼圖片資料表：

```
CREATE OR REPLACE TABLE `my_dataset.decoded_images`
  AS (SELECT ML.DECODE_IMAGE(data) AS decoded_image
  FROM `my_dataset.object_table`);
```

對解碼圖片資料表執行推論：

```
SELECT * FROM
ML.PREDICT(
  MODEL`my_dataset.vision_model`,
  (SELECT uri, ML.CONVERT_IMAGE_TYPE(ML.RESIZE_IMAGE(decoded_image, 480, 480, FALSE)) AS input
  FROM `my_dataset.decoded_images`)
);
```

**範例 4**

以下範例使用 `ML.DECODE_IMAGE` 的結果，這些結果已寫入資料表資料欄，並使用 `ML.RESIZE_IMAGE` 預先處理。如果模型的輸入欄位為 `input`，輸出欄位為 `feature`，則會傳回解碼圖片資料表中所有圖片的推論結果。

建立資料表：

```
CREATE OR REPLACE TABLE `my_dataset.decoded_images`
  AS (SELECT ML.RESIZE_IMAGE(ML.DECODE_IMAGE(data) 480, 480, FALSE) AS decoded_image
  FROM `my_dataset.object_table`);
```

對解碼圖片資料表執行推論：

```
SELECT * FROM
ML.PREDICT(
  MODEL `my_dataset.vision_model`,
  (SELECT uri, decoded_image AS input
  FROM `my_dataset.decoded_images`)
);
```

**範例 5**

以下範例直接在 `ML.PREDICT` 函式中使用 `ML.DECODE_IMAGE` 函式。在這個範例中，模型有一個輸出欄位 `embeddings` 和兩個輸入欄位：一個預期圖片 `f_img`，另一個預期字串 `f_txt`。圖片輸入內容來自物件資料表，字串輸入內容則來自標準 BigQuery 資料表，該資料表使用 `uri` 資料欄與物件資料表彙整。

```
SELECT * FROM
  ML.PREDICT(
    MODEL `my_dataset.mixed_model`,
    (SELECT uri, ML.RESIZE_IMAGE(ML.DECODE_IMAGE(my_dataset.my_object_table.data), 224, 224, FALSE) AS f_img,
      my_dataset.image_description.description AS f_txt
    FROM `my_dataset.object_table`
    JOIN `my_dataset.image_description`
    ON object_table.uri = image_description.uri)
  );
```

## 後續步驟

* 瞭解如何[使用遠端函式分析物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-remote-function?hl=zh-tw)。
* 嘗試[使用特徵向量模型對物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/inference-tutorial-mobilenet?hl=zh-tw)。
* 嘗試[使用分類模型對物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/inference-tutorial-resnet?hl=zh-tw)。
* 嘗試[使用遠端函式分析物件資料表](https://docs.cloud.google.com/bigquery/docs/remote-function-tutorial?hl=zh-tw)。
* 嘗試[使用 `ML.ANNOTATE_IMAGE` 函式為圖片加上註解](https://docs.cloud.google.com/bigquery/docs/annotate-image?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]