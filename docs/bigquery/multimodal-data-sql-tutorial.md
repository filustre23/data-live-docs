Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 SQL 和 BigQuery DataFrames 分析多模態資料

本教學課程說明如何使用 SQL 查詢和 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw) [分析多模態資料](https://docs.cloud.google.com/bigquery/docs/analyze-multimodal-data?hl=zh-tw)。

本教學課程使用公開的 Cymbal 寵物商店資料集中的產品目錄。

## 目標

* 使用
  [`ObjectRef`](https://docs.cloud.google.com/bigquery/docs/work-with-objectref?hl=zh-tw)
  值，將圖片資料與結構化資料一併儲存在 BigQuery [標準資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)中。
* 使用 [`AI.GENERATE_TABLE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-table?hl=zh-tw)，根據標準資料表的圖片資料生成文字。
* 使用 Python UDF 轉換現有圖片，建立新圖片。
* 使用 Python UDF 將 PDF 分塊，以供進一步分析。
* 使用 Gemini 模型和 `AI.GENERATE_TEXT` 函式分析 PDF 區塊資料。
* 使用[`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)，根據標準資料表的圖片資料生成嵌入項目。
* 使用 `ObjectRef` 值陣列處理排序的多模態資料。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* **BigQuery**: you incur costs for the data that you
  process in BigQuery.
* **BigQuery Python UDFs**: you incur costs for
  using Python UDFs.
* **Cloud Storage**: you incur costs for the objects stored
  in Cloud Storage.
* **Vertex AI**: you incur costs for calls to
  Vertex AI models.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

如要瞭解詳情，請參閱下列定價頁面：

* [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [BigQuery Python UDF 定價](https://docs.cloud.google.com/bigquery/docs/user-defined-functions-python?hl=zh-tw#pricing)
* [Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)
* [Vertex AI 定價](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing?hl=zh-tw)

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery、BigQuery Connection、Cloud Storage 和 Vertex AI API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Cstorage.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

### 必要的角色

如要取得完成本教學課程所需的權限，請要求管理員授予您下列 IAM 角色：

* 建立連線：
  [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)
* 將權限授予連線的服務帳戶：
  「專案 IAM 管理員」 (`roles/resourcemanager.projectIamAdmin`)
* 建立 Cloud Storage bucket：
  [Storage Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin)  (`roles/storage.admin`)
* 建立資料集、模型、使用者定義函式和資料表，並執行 BigQuery 工作：
  [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`)
* 建立可讀取及修改 Cloud Storage 物件的網址：
  [BigQuery ObjectRef 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.objectRefAdmin)  (`roles/bigquery.objectRefAdmin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 設定

在本節中，您會建立本教學課程中使用的資料集、連線、資料表和模型。

### 建立資料集

建立 BigQuery 資料集，內含您在本教學課程中建立的物件：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中選取專案。
4. 按一下 more\_vert「View actions」(查看動作)，然後點選「Create dataset」(建立資料集)。「建立資料集」窗格隨即開啟。
5. 在「Dataset ID」(資料集 ID) 中輸入 `cymbal_pets`。
6. 點選「建立資料集」。

### 建立值區

建立 Cloud Storage bucket，用於儲存轉換後的物件：

1. 前往「Buckets」(值區) 頁面。

   [前往「Buckets」(值區) 頁面](https://console.cloud.google.com/storage/browser?hl=zh-tw)
2. 點選 add\_box「Create」(建立)。
3. 在「建立 bucket」頁面的「開始使用」部分，輸入符合[bucket 名稱規定](https://docs.cloud.google.com/storage/docs/buckets?hl=zh-tw#naming)的全球專屬名稱。
4. 點選「建立」。

### 建立連線

建立[Cloud 資源連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，並取得連線的服務帳戶。BigQuery 會使用連線存取 Cloud Storage 中的物件：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，點選「新增資料」add。

   「新增資料」對話方塊隨即開啟。
4. 在「依條件篩選」窗格的「資料來源類型」部分，選取「商用應用程式」。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `Vertex AI`。
5. 在「精選資料來源」部分，點選「Vertex AI」。
6. 按一下「Vertex AI Models: BigQuery Federation」解決方案資訊卡。
7. 在「連線類型」清單中，選取「Vertex AI 遠端模型、遠端函式、BigLake 和 Spanner (Cloud 資源)」。
8. 在「連線 ID」欄位中輸入 `cymbal_conn`。
9. 點選「建立連線」。
10. 點選「前往連線」。
11. 在「連線資訊」窗格中，複製服務帳戶 ID，以供後續步驟使用。

### 將權限授予連線的服務帳戶

將適當的角色授予連線的服務帳戶，以便存取其他服務。您必須在「[事前準備](#before_you_begin)」一節中建立或選取的專案中授予這些角色。在其他專案中授予角色會導致錯誤 `bqcx-1234567890-xxxx@gcp-sa-bigquery-condel.iam.gserviceaccount.com
does not have the permission to access resource`。

#### 授予 Cloud Storage bucket 權限

授予服務帳戶權限，允許使用您建立的 bucket 中的物件：

1. 前往「Buckets」(值區) 頁面。

   [前往「Buckets」(值區) 頁面](https://console.cloud.google.com/storage/browser?hl=zh-tw)
2. 按一下您建立的值區名稱。
3. 按一下「權限」。
4. 按一下 person\_add「授予存取權」。「授予存取權」對話方塊隨即開啟。
5. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
6. 在「Select a role」(請選擇角色) 欄位中，依序選取「Cloud Storage」和「Storage Object User」(Storage 物件使用者)。
7. 按一下 [儲存]。

#### 授予使用 Vertex AI 模型的權限

授予服務帳戶使用 Vertex AI 模型的權限：

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下 person\_add「授予存取權」。「授予存取權」對話方塊隨即開啟。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 在「選取角色」欄位中，依序選取「Vertex AI」和「Vertex AI 使用者」。
5. 按一下 [儲存]。

### 建立範例資料表

建立資料表來儲存 Cymbal 寵物產品資訊。

#### 建立 `products` 資料表

建立包含 Cymbal 寵物產品資訊的標準表格：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 執行下列指令來建立 `products` 資料表：

   ### SQL

   ```
   LOAD DATA OVERWRITE cymbal_pets.products
   FROM
     FILES(
       format = 'avro',
       uris = [
         'gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/tables/products/products_*.avro']);
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   import bigframes.bigquery as bbq
   import bigframes.pandas as bpd

   bbq.load_data(
       "cymbal_pets.products",
       write_disposition="OVERWRITE",
       from_files_options={
           "format": "avro",
           "uris": [
               "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/tables/products/products_*.avro"
           ],
       },
   )
   ```

#### 建立 `product_images` 資料表

建立包含 Cymbal 寵物產品圖片的物件資料表：

* 執行下列指令來建立 `product_images` 資料表：

  ### SQL

  ```
  CREATE OR REPLACE EXTERNAL TABLE cymbal_pets.product_images
    WITH CONNECTION `us.cymbal_conn`
    OPTIONS (
      object_metadata = 'SIMPLE',
      uris = ['gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/*.png'],
      max_staleness = INTERVAL 30 MINUTE,
      metadata_cache_mode = AUTOMATIC);
  ```

  ### BigQuery DataFrames

  在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
  詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

  如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
  詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

  ```
  bbq.create_external_table(
      "cymbal_pets.product_images",
      replace=True,
      connection_name="us.cymbal_conn",
      options={
          "object_metadata": "SIMPLE",
          "uris": [
              "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/*.png"
          ],
      },
  )
  ```

#### 建立 `product_manuals` 資料表

建立包含 Cymbal 寵物產品手冊的物件資料表：

* 執行下列指令來建立 `product_manuals` 資料表：

  ### SQL

  ```
  CREATE OR REPLACE EXTERNAL TABLE cymbal_pets.product_manuals
    WITH CONNECTION `us.cymbal_conn`
    OPTIONS (
      object_metadata = 'SIMPLE',
      uris = ['gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/documents/*.pdf']);
  ```

  ### BigQuery DataFrames

  在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
  詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

  如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
  詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

  ```
  bbq.create_external_table(
      "cymbal_pets.product_manuals",
      replace=True,
      connection_name="us.cymbal_conn",
      options={
          "object_metadata": "SIMPLE",
          "uris": [
              "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/documents/*.pdf"
          ],
      },
  )
  ```

### 建立文字生成模型

建立代表 Vertex AI Gemini 模型的 BigQuery ML [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)：

* 執行下列指令來建立遠端模型：

  ### SQL

  ```
  CREATE OR REPLACE MODEL `cymbal_pets.gemini`
    REMOTE WITH CONNECTION `us.cymbal_conn`
    OPTIONS (ENDPOINT = 'gemini-2.0-flash');
  ```

  ### BigQuery DataFrames

  在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
  詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

  如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
  詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

  ```
  gemini_model = bbq.ml.create_model(
      "cymbal_pets.gemini",
      replace=True,
      connection_name="us.cymbal_conn",
      options={"endpoint": "gemini-2.5-flash"},
  )
  ```

### 建立嵌入生成模型

建立代表 Vertex AI 多模態嵌入模型的 BigQuery ML 遠端模型：

* 執行下列指令來建立遠端模型：

  ### SQL

  ```
  CREATE OR REPLACE MODEL `cymbal_pets.embedding_model`
    REMOTE WITH CONNECTION `us.cymbal_conn`
    OPTIONS (ENDPOINT = 'multimodalembedding@001');
  ```

  ### BigQuery DataFrames

  在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
  詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

  如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
  詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

  ```
  embedding_model = bbq.ml.create_model(
      "cymbal_pets.embedding_model",
      replace=True,
      connection_name="us.cymbal_conn",
      options={"endpoint": "multimodalembedding@001"},
  )
  ```

## 建立包含多模態資料的 `products_mm` 資料表

建立 `products_mm` 資料表，其中包含從 `product_images` 物件資料表填入產品圖片的 `image` 資料欄。建立的 `image` 資料欄是使用 `ObjectRef` 格式的 `STRUCT` 資料欄。

1. 執行下列指令，建立 `products_mm` 資料表並填入 `image` 欄：

   ### SQL

   ```
   CREATE OR REPLACE TABLE cymbal_pets.products_mm
   AS
   SELECT products.* EXCEPT (uri), ot.ref AS image FROM cymbal_pets.products
   INNER JOIN cymbal_pets.product_images ot
   ON ot.uri = products.uri;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_images = bpd.read_gbq("SELECT * FROM cymbal_pets.product_images")
   df_products = bpd.read_gbq("cymbal_pets.products")

   df_products_mm = df_images.merge(df_products, on="uri").drop(columns="uri")
   df_products_mm = df_products_mm.rename(columns={"ref": "image"})
   ```
2. 執行下列指令，查看 `image` 欄資料：

   ### SQL

   ```
   SELECT product_name, image
   FROM cymbal_pets.products_mm
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_products_mm[["product_name", "image"]]
   ```

   結果類似下方：

   ```
   +--------------------------------+--------------------------------------+-----------------------------------------------+------------------------------------------------+
   | product_name                   | image.uri                            | image.version | image.authorizer              | image.details                                  |
   +--------------------------------+--------------------------------------+-----------------------------------------------+------------------------------------------------+
   |  AquaClear Aquarium Background | gs://cloud-samples-data/bigquery/    | 1234567891011 | myproject.region.myconnection | {"gcs_metadata":{"content_type":"image/png",   |
   |                                | tutorials/cymbal-pets/images/        |               |                               | "md5_hash":"494f63b9b137975ff3e7a11b060edb1d", |
   |                                | aquaclear-aquarium-background.png    |               |                               | "size":1282805,"updated":1742492680017000}}    |
   +--------------------------------+--------------------------------------+-----------------------------------------------+------------------------------------------------+
   |  AquaClear Aquarium            | gs://cloud-samples-data/bigquery/    | 2345678910112 | myproject.region.myconnection | {"gcs_metadata":{"content_type":"image/png",   |
   |  Gravel Vacuum                 | tutorials/cymbal-pets/images/        |               |                               | "md5_hash":"b7bfc2e2641a77a402a1937bcf0003fd", |
   |                                | aquaclear-aquarium-gravel-vacuum.png |               |                               | "size":820254,"updated":1742492682411000}}     |
   +--------------------------------+--------------------------------------+-----------------------------------------------+------------------------------------------------+
   | ...                            | ...                                  | ...           |                               | ...                                            |
   +--------------------------------+--------------------------------------+-----------------------------------------------+------------------------------------------------+
   ```

## 使用 Gemini 模型生成產品資訊

使用 Gemini 模型為寵物店產品生成下列資料：

* 在 `products_mm` 表格中新增 `image_description` 欄。
* 填入 `products_mm` 資料表的 `animal_type`、`search_keywords` 和 `subcategory` 欄。
* 執行查詢，傳回每個產品品牌的說明，以及該品牌的產品數量。系統會分析該品牌所有產品的產品資訊 (包括產品圖片)，然後生成品牌說明。

1. 執行下列指令，建立並填入 `image_description` 資料欄：

   ### SQL

   ```
   CREATE OR REPLACE TABLE cymbal_pets.products_mm
   AS
   SELECT
     product_id,
     product_name,
     brand,
     category,
     subcategory,
     animal_type,
     search_keywords,
     price,
     description,
     inventory_level,
     supplier_id,
     average_rating,
     image,
     image_description
   FROM
     AI.GENERATE_TABLE(
       MODEL `cymbal_pets.gemini`,
       (
         SELECT
           ('Can you describe the following image? ', OBJ.GET_ACCESS_URL(image, 'r')) AS prompt,
           *
         FROM
           cymbal_pets.products_mm
       ),
       STRUCT('image_description STRING' AS output_schema));
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_products_mm["url"] = bbq.obj.get_access_url(
       df_products_mm["image"], "R"
   ).to_frame()
   df_products_mm["prompt0"] = "Can you describe the following image?"

   df_products_mm["prompt"] = bbq.struct(df_products_mm[["prompt0", "url"]])
   df_products_mm = bbq.ai.generate_table(
       gemini_model, df_products_mm, output_schema={"image_description": "STRING"}
   )

   df_products_mm = df_products_mm[
       [
           "product_id",
           "product_name",
           "brand",
           "category",
           "subcategory",
           "animal_type",
           "search_keywords",
           "price",
           "description",
           "inventory_level",
           "supplier_id",
           "average_rating",
           "image",
           "image_description",
       ]
   ]
   ```
2. 執行下列程式碼，使用產生的資料更新 `animal_type`、`search_keywords` 和 `subcategory` 欄：

   ### SQL

   ```
   UPDATE cymbal_pets.products_mm p
   SET
     p.animal_type = s.animal_type,
     p.search_keywords = s.search_keywords,
     p.subcategory = s.subcategory
   FROM
     (
       SELECT
         animal_type,
         search_keywords,
         subcategory,
         uri
       FROM
         AI.GENERATE_TABLE(
           MODEL `cymbal_pets.gemini`,
           (
             SELECT
               (
                 'For the image of a pet product, concisely generate the following metadata: '
                 '1) animal_type and 2) 5 SEO search keywords, and 3) product subcategory. ',
                 OBJ.GET_ACCESS_URL(image, 'r'),
                 description) AS prompt,
               image.uri AS uri,
             FROM cymbal_pets.products_mm
           ),
           STRUCT(
             'animal_type STRING, search_keywords ARRAY<STRING>, subcategory STRING' AS output_schema,
             100 AS max_output_tokens))
     ) s
   WHERE p.image.uri = s.uri;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_prompt = bbq.obj.get_access_url(df_products_mm["image"], "R").to_frame()
   df_prompt[
       "prompt0"
   ] = "For the image of a pet product, concisely generate the following metadata: 1) animal_type and 2) 5 SEO search keywords, and 3) product subcategory."

   df_products_mm["prompt"] = bbq.struct(df_prompt[["prompt0", "image"]])

   df_products_mm = df_products_mm.drop(
       columns=["animal_type", "search_keywords", "subcategory"]
   )
   df_products_mm = bbq.ai.generate_table(
       gemini_model,
       df_products_mm,
       output_schema="animal_type STRING, search_keywords ARRAY<STRING>, subcategory STRING",
   )
   ```
3. 執行下列指令，查看產生的資料：

   ### SQL

   ```
   SELECT
     product_name,
     image_description,
     animal_type,
     search_keywords,
     subcategory,
   FROM cymbal_pets.products_mm;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_products_mm[
       [
           "product_name",
           "image_description",
           "animal_type",
           "search_keywords",
           "subcategory",
       ]
   ]
   ```

   結果類似下方：

   ```
   +--------------------------------+-------------------------------------+-------------+------------------------+------------------+
   | product_name                   | image.description                   | animal_type | search_keywords        | subcategory      |
   +--------------------------------+-------------------------------------+-------------+------------------------+------------------+
   |  AquaClear Aquarium Background | The image shows a colorful coral    | fish        | aquarium background    | aquarium decor   |
   |                                | reef backdrop. The background is a  |             | fish tank backdrop     |                  |
   |                                | blue ocean with a bright light...   |             | coral reef decor       |                  |
   |                                |                                     |             | underwater scenery     |                  |
   |                                |                                     |             | aquarium decoration    |                  |
   +--------------------------------+-------------------------------------+-------------+------------------------+------------------+
   |  AquaClear Aquarium            | The image shows a long, clear       | fish        | aquarium gravel vacuum | aquarium         |
   |  Gravel Vacuum                 | plastic tube with a green hose      |             | aquarium cleaning      | cleaning         |
   |                                | attached to one end. The tube...    |             | aquarium maintenance   |                  |
   |                                |                                     |             | fish tank cleaning     |                  |
   |                                |                                     |             | gravel siphon          |                  |
   +--------------------------------+-------------------------------------+-------------+------------------------+------------------+
   | ...                            | ...                                 | ...         |  ...                   | ...              |
   +--------------------------------+-------------------------------------+-------------+------------------------+------------------+
   ```
4. 執行下列程式碼，產生每個產品品牌的說明，以及該品牌產品的數量：

   ### SQL

   ```
   SELECT
     brand,
     brand_description,
     cnt
   FROM
     AI.GENERATE_TABLE(
       MODEL `cymbal_pets.gemini`,
       (
         SELECT
           brand,
           COUNT(*) AS cnt,
           (
             'Use the images and text to give one concise brand description for a website brand page.'
               'Return the description only. ',
             ARRAY_AGG(OBJ.GET_ACCESS_URL(image, 'r')), ' ',
             ARRAY_AGG(description), ' ',
             ARRAY_AGG(category), ' ',
             ARRAY_AGG(subcategory)) AS prompt
         FROM cymbal_pets.products_mm
         GROUP BY brand
       ),
       STRUCT('brand_description STRING' AS output_schema))
   ORDER BY cnt DESC;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_agg = df_products_mm[
       ["image", "description", "category", "subcategory", "brand"]
   ]
   df_agg["image"] = bbq.obj.get_access_url(df_products_mm["image"], "R")
   df_agg = bbq.array_agg(df_agg.groupby(by=["brand"]))

   df_agg["cnt"] = bbq.array_length(df_agg["image"])

   df_prompt = df_agg[["image", "description", "category", "subcategory"]]
   df_prompt[
       "prompt0"
   ] = "Use the images and text to give one concise brand description for a website brand page. Return the description only. "

   df_agg["prompt"] = bbq.struct(
       df_prompt[["prompt0", "image", "description", "category", "subcategory"]]
   )

   df_agg = df_agg.reset_index()

   df_agg = bbq.ai.generate_table(
       gemini_model, df_agg, output_schema={"brand_description": "STRING"}
   )
   df_agg[["brand", "brand_description", "cnt"]]
   ```

   結果類似下方：

   ```
   +--------------+-------------------------------------+-----+
   | brand        | brand.description                   | cnt |
   +--------------+-------------------------------------+-----+
   |  AquaClear   | AquaClear is a brand of aquarium    | 33  |
   |              | and pond care products that offer   |     |
   |              | a wide range of solutions for...    |     |
   +--------------+-------------------------------------+-----+
   |  Ocean       | Ocean Bites is a brand of cat food  | 28  |
   |  Bites       | that offers a variety of recipes    |     |
   |              | and formulas to meet the specific.. |     |
   +--------------+-------------------------------------+-----+
   |  ...         | ...                                 |...  |
   +--------------+-------------------------------------+-----+
   ```

## 建立 Python UDF 來轉換產品圖片

建立 Python UDF，將產品圖片轉換為灰階。

Python UDF 使用開放原始碼程式庫，並採用平行執行方式，同時轉換多張圖片。

1. 執行下列指令，建立 `to_grayscale` UDF：

   ### SQL

   ```
   CREATE OR REPLACE FUNCTION cymbal_pets.to_grayscale(src_json STRING, dst_json STRING)
   RETURNS STRING
   LANGUAGE python
   WITH CONNECTION `us.cymbal_conn`
   OPTIONS (entry_point='to_grayscale', runtime_version='python-3.11', packages=['numpy', 'opencv-python'])
   AS """

   import cv2 as cv
   import numpy as np
   from urllib.request import urlopen, Request
   import json

   # Transform the image to grayscale.
   def to_grayscale(src_ref, dst_ref):
     src_json = json.loads(src_ref)
     srcUrl = src_json["access_urls"]["read_url"]

     dst_json = json.loads(dst_ref)
     dstUrl = dst_json["access_urls"]["write_url"]

     req = urlopen(srcUrl)
     arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
     img = cv.imdecode(arr, -1) # 'Load it as it is'

     # Convert the image to grayscale
     gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

     # Send POST request to the URL
     _, img_encoded = cv.imencode('.png', gray_image)

     req = Request(url=dstUrl, data=img_encoded.tobytes(), method='PUT', headers = {
         "Content-Type": "image/png",
     })
     with urlopen(req) as f:
         pass
     return dst_ref
   """;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   @bpd.udf(
       dataset="cymbal_pets",
       name="to_grayscale",
       packages=["numpy", "opencv-python"],
       bigquery_connection="us.cymbal_conn",
       max_batching_rows=1,
   )
   def to_grayscale(src_ref: str, dst_ref: str) -> str:
       import json
       from urllib.request import Request, urlopen

       import cv2 as cv
       import numpy as np

       src_json = json.loads(src_ref)
       srcUrl = src_json["access_urls"]["read_url"]

       dst_json = json.loads(dst_ref)
       dstUrl = dst_json["access_urls"]["write_url"]

       req = urlopen(srcUrl)
       arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
       img = cv.imdecode(arr, -1)  # 'Load it as it is'

       # Convert the image to grayscale
       gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

       # Send POST request to the URL
       _, img_encoded = cv.imencode(".png", gray_image)

       req = Request(
           url=dstUrl,
           data=img_encoded.tobytes(),
           method="PUT",
           headers={
               "Content-Type": "image/png",
           },
       )
       with urlopen(req):
           pass
       return dst_ref
   ```

## 變換產品圖片風格

建立 `products_grayscale` 資料表，其中包含 `ObjectRef` 欄，內含灰階圖片的目的地路徑和授權者。目的地路徑是從原始圖片路徑衍生而來。

建立資料表後，請執行 `to_grayscale` 函式來建立灰階圖片、將圖片寫入 Cloud Storage bucket，然後傳回 [`ObjectRefRuntime`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-tw#objectrefruntime) 值，其中包含灰階圖片的存取網址和中繼資料。

1. 執行下列指令來建立 `products_grayscale` 資料表：

   ### SQL

   ```
   CREATE OR REPLACE TABLE cymbal_pets.products_grayscale
   AS
   SELECT
     product_id,
     product_name,
     image,
     OBJ.MAKE_REF(
       CONCAT('gs://BUCKET/cymbal-pets-images/grayscale/', REGEXP_EXTRACT(image.uri, r'([^/]+)$')),
       'us.cymbal_conn') AS gray_image
   FROM cymbal_pets.products_mm;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_grayscale = df_products_mm[["product_id", "product_name", "image"]]
   df_grayscale[
       "gray_image_uri"
   ] = f"gs://{BUCKET}/cymbal-pets-images/grayscale/" + df_grayscale[
       "image"
   ].struct.field(
       "uri"
   ).str.extract(
       r"([^/]+)$"
   )

   df_grayscale["gray_image"] = bbq.obj.make_ref(
       df_grayscale["gray_image_uri"], "us.cymbal_conn"
   )

   df_grayscale["image_url"] = bbq.to_json_string(
       bbq.obj.get_access_url(df_grayscale["image"], "r")
   )
   df_grayscale["gray_image_url"] = bbq.to_json_string(
       bbq.obj.get_access_url(df_grayscale["gray_image"], "rw")
   )

   df_grayscale[["image_url", "gray_image_url"]].apply(to_grayscale, axis=1)
   ```

   將 `BUCKET` 替換為[您建立的值區](#create_a_bucket)名稱。
2. 執行下列程式碼，建立灰階圖片、將圖片寫入 Cloud Storage bucket，然後傳回包含灰階圖片存取網址和中繼資料的 `ObjectRefRuntime` 值：

   ### SQL

   ```
   SELECT cymbal_pets.to_grayscale(
     TO_JSON_STRING(OBJ.GET_ACCESS_URL(image, 'r')),
     TO_JSON_STRING(OBJ.GET_ACCESS_URL(gray_image, 'rw')))
   FROM cymbal_pets.products_grayscale;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_grayscale = df_products_mm[["product_id", "product_name", "image"]]
   df_grayscale[
       "gray_image_uri"
   ] = f"gs://{BUCKET}/cymbal-pets-images/grayscale/" + df_grayscale[
       "image"
   ].struct.field(
       "uri"
   ).str.extract(
       r"([^/]+)$"
   )

   df_grayscale["gray_image"] = bbq.obj.make_ref(
       df_grayscale["gray_image_uri"], "us.cymbal_conn"
   )

   df_grayscale["image_url"] = bbq.to_json_string(
       bbq.obj.get_access_url(df_grayscale["image"], "r")
   )
   df_grayscale["gray_image_url"] = bbq.to_json_string(
       bbq.obj.get_access_url(df_grayscale["gray_image"], "rw")
   )

   df_grayscale[["image_url", "gray_image_url"]].apply(to_grayscale, axis=1)
   ```

   結果類似下方：

   ```
   +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | f0                                                                                                                                                                    |
   +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | {"access_urls":{"expiry_time":"2025-04-26T03:00:48Z",                                                                                                                 |
   | "read_url":"https://storage.googleapis.com/mybucket/cymbal-pets-images%2Fgrayscale%2Focean-bites-salmon-%26-tuna-cat-food.png?additional_read URL_information",       |
   | "write_url":"https://storage.googleapis.com/myproject/cymbal-pets-images%2Fgrayscale%2Focean-bites-salmon-%26-tuna-cat-food.png?additional_write URL_information"},   |
   | "objectref":{"authorizer":"myproject.region.myconnection","uri":"gs://myproject/cymbal-pets-images/grayscale/ocean-bites-salmon-&-tuna-cat-food.png"}}                |
   +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | {"access_urls":{"expiry_time":"2025-04-26T03:00:48Z",                                                                                                                 |
   | "read_url":"https://storage.googleapis.com/mybucket/cymbal-pets-images%2Fgrayscale%2Ffluffy-buns-guinea-pig-tunnel.png?additional _read URL_information",             |
   | "write_url":"https://storage.googleapis.com/myproject/cymbal-pets-images%2Fgrayscale%2Focean-bites-salmon-%26-tuna-cat-food.png?additional_write_URL_information"},   |
   | "objectref":{"authorizer":"myproject.region.myconnection","uri":"gs://myproject/cymbal-pets-images%2Fgrayscale%2Ffluffy-buns-guinea-pig-tunnel.png"}}                 |
   +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   |  ...                                                                                                                                                                  |
   +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   ```

## 建立 Python UDF，將 PDF 資料分塊

建立 Python UDF，將含有 Cymbal 寵物產品手冊的 PDF 物件分成多個部分。

PDF 檔案通常很大，可能無法在單次呼叫生成式 AI 模型時處理。將 PDF 分塊後，您就能以模型可用的格式儲存 PDF 資料，方便進行分析。

1. 執行下列指令，建立 `chunk_pdf` UDF：

   ### SQL

   ```
   -- This function chunks the product manual PDF into multiple parts.
   -- The function accepts an ObjectRefRuntime value for the PDF file and the chunk size.
   -- It then parses the PDF, chunks the contents, and returns an array of chunked text.
   CREATE OR REPLACE FUNCTION cymbal_pets.chunk_pdf(src_json STRING, chunk_size INT64, overlap_size INT64)
   RETURNS ARRAY<STRING>
   LANGUAGE python
   WITH CONNECTION `us.cymbal_conn`
   OPTIONS (entry_point='chunk_pdf', runtime_version='python-3.11', packages=['pypdf'])
   AS """
   import io
   import json

   from pypdf import PdfReader  # type: ignore
   from urllib.request import urlopen, Request

   def chunk_pdf(src_ref: str, chunk_size: int, overlap_size: int) -> str:
     src_json = json.loads(src_ref)
     srcUrl = src_json["access_urls"]["read_url"]

     req = urlopen(srcUrl)
     pdf_file = io.BytesIO(bytearray(req.read()))
     reader = PdfReader(pdf_file, strict=False)

     # extract and chunk text simultaneously
     all_text_chunks = []
     curr_chunk = ""
     for page in reader.pages:
         page_text = page.extract_text()
         if page_text:
             curr_chunk += page_text
             # split the accumulated text into chunks of a specific size with overlaop
             # this loop implements a sliding window approach to create chunks
             while len(curr_chunk) >= chunk_size:
                 split_idx = curr_chunk.rfind(" ", 0, chunk_size)
                 if split_idx == -1:
                     split_idx = chunk_size
                 actual_chunk = curr_chunk[:split_idx]
                 all_text_chunks.append(actual_chunk)
                 overlap = curr_chunk[split_idx + 1 : split_idx + 1 + overlap_size]
                 curr_chunk = overlap + curr_chunk[split_idx + 1 + overlap_size :]
     if curr_chunk:
         all_text_chunks.append(curr_chunk)

     return all_text_chunks
   """;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   @bpd.udf(
       dataset="cymbal_pets",
       name="chunk_pdf",
       packages=["pypdf"],
       bigquery_connection="us.cymbal_conn",
       max_batching_rows=1,
   )
   def chunk_pdf(src_ref: str, chunk_size: int, overlap_size: int) -> list[str]:
       import io
       import json
       from urllib.request import urlopen

       from pypdf import PdfReader  # type: ignore

       src_json = json.loads(src_ref)
       srcUrl = src_json["access_urls"]["read_url"]

       req = urlopen(srcUrl)
       pdf_file = io.BytesIO(bytearray(req.read()))
       reader = PdfReader(pdf_file, strict=False)

       # extract and chunk text simultaneously
       all_text_chunks = []
       curr_chunk = ""
       for page in reader.pages:
           page_text = page.extract_text()
           if page_text:
               curr_chunk += page_text
               # split the accumulated text into chunks of a specific size with overlaop
               # this loop implements a sliding window approach to create chunks
               while len(curr_chunk) >= chunk_size:
                   split_idx = curr_chunk.rfind(" ", 0, chunk_size)
                   if split_idx == -1:
                       split_idx = chunk_size
                   actual_chunk = curr_chunk[:split_idx]
                   all_text_chunks.append(actual_chunk)
                   overlap = curr_chunk[split_idx + 1 : split_idx + 1 + overlap_size]
                   curr_chunk = overlap + curr_chunk[split_idx + 1 + overlap_size :]
       if curr_chunk:
           all_text_chunks.append(curr_chunk)

       return all_text_chunks
   ```

## 分析 PDF 資料

執行 `chunk_pdf` 函式，將 `product_manuals` 資料表中的 PDF 資料分塊，然後建立 `product_manual_chunk_strings` 資料表，其中每列包含一個 PDF 分塊。在 `product_manual_chunk_strings` 資料上使用 Gemini 模型，摘要產品手冊中的法律資訊。

1. 執行下列指令來建立 `product_manual_chunk_strings` 資料表：

   ### SQL

   ```
   CREATE OR REPLACE TABLE cymbal_pets.product_manual_chunk_strings
   AS
   SELECT chunked
   FROM cymbal_pets.product_manuals,
   UNNEST (cymbal_pets.chunk_pdf(
     TO_JSON_STRING(
       OBJ.GET_ACCESS_URL(OBJ.MAKE_REF(uri, 'us.cymbal_conn'), 'r')),
       1000,
       100
   )) as chunked;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_manuals = bpd.read_gbq("SELECT * FROM cymbal_pets.product_manuals")
   df_manuals["url"] = bbq.to_json_string(
       bbq.obj.get_access_url(df_manuals["ref"], "R")
   )

   df_manuals["chunk_size"] = 1000
   df_manuals["overlap_size"] = 100

   df_manuals["chunked"] = df_manuals[["url", "chunk_size", "overlap_size"]].apply(
       chunk_pdf, axis=1
   )
   ```
2. 執行下列指令，使用 Gemini 模型分析 PDF 資料：

   ### SQL

   ```
   SELECT
     result
   FROM
     AI.GENERATE_TEXT(
       MODEL `cymbal_pets.gemini`,
       (
         SELECT
           (
             'Can you summarize the product manual as bullet points? Highlight the legal clauses',
             chunked) AS prompt,
         FROM cymbal_pets.product_manual_chunk_strings
       ));
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_chunked = df_manuals["chunked"].explode().to_frame()
   df_chunked[
       "prompt0"
   ] = "Can you summarize the product manual as bullet points? Highlight the legal clauses"

   df_chunked["prompt"] = bbq.struct(df_chunked[["prompt0", "chunked"]])

   result = bbq.ai.generate_text(gemini_model, df_chunked["prompt"])
   result
   ```

   結果類似下方：

   ```
   +-------------------------------------------------------------------------------------------------------------------------------------------+
   | result                                                                                                                                    |
   +-------------------------------------------------------------------------------------------------------------------------------------------+
   | ## CritterCuisine Pro 5000 Automatic Pet Feeder Manual Summary:                                                                           |
   |                                                                                                                                           |
   | **Safety:**                                                                                                                               |
   |                                                                                                                                           |
   | * **Stability:** Place feeder on a level, stable surface to prevent tipping.                                                              |
   | * **Power Supply:** Only use the included AC adapter. Using an incompatible adapter can damage the unit and void the warranty.            |
   | * **Cord Safety:** Keep the power cord out of reach of pets to prevent chewing or entanglement.                                           |
   | * **Children:** Supervise children around the feeder. This is not a toy.                                                                  |
   | * **Pet Health:** Consult your veterinarian before using an automatic feeder if your pet has special dietary needs, health conditions, or |
   +-------------------------------------------------------------------------------------------------------------------------------------------+
   | ## Product Manual Summary:                                                                                                                |
   |                                                                                                                                           |
   | **6.3 Manual Feeding:**                                                                                                                   |
   |                                                                                                                                           |
   | * Press MANUAL button to dispense a single portion (Meal 1 size). **(Meal Enabled)**                                                      |
   |                                                                                                                                           |
   | **6.4 Recording a Voice Message:**                                                                                                        |
   |                                                                                                                                           |
   | * Press and hold VOICE button.                                                                                                            |
   | * Speak clearly into the microphone (up to 10 seconds).                                                                                   |
   | * Release VOICE button to finish recording.                                                                                               |
   | * Briefly press VOICE button to play back the recording.                                                                                  |
   | * To disable the voice message, record a blank message (hold VOICE button for 10 seconds without speaking). **(Meal Enabled)**            |
   |                                                                                                                                           |
   | **6.5 Low Food Level Indicator:**                                                                                                         |
   +-------------------------------------------------------------------------------------------------------------------------------------------+
   | ...                                                                                                                                       |
   +-------------------------------------------------------------------------------------------------------------------------------------------+
   ```

## 生成嵌入項目並執行向量搜尋

從圖片資料生成嵌入項目，然後使用嵌入項目透過[向量搜尋](https://docs.cloud.google.com/bigquery/docs/vector-search-intro?hl=zh-tw)傳回類似圖片。

在正式環境中，建議您先建立[向量索引](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_vector_index_statement)，再執行向量搜尋。向量索引可加快向量搜尋速度，但會降低喚回率，因此傳回的結果較為近似。

1. 執行下列指令來建立
   `products_embeddings` 資料表：

   ### SQL

   ```
   CREATE OR REPLACE TABLE cymbal_pets.products_embedding
   AS
   SELECT product_id, embedding, content as image
   FROM AI.GENERATE_EMBEDDING(
   MODEL `cymbal_pets.embedding_model`,
     (
       SELECT OBJ.GET_ACCESS_URL(image, 'r') as content, image, product_id
       FROM cymbal_pets.products_mm
     )
   );
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_products_mm["content"] = bbq.obj.get_access_url(df_products_mm["image"], "R")
   df_embed = bbq.ai.generate_embedding(
       embedding_model, df_products_mm[["content", "product_id"]]
   )

   df_embed.to_gbq("cymbal_pets.products_embedding", if_exists="replace")
   ```
2. 執行下列指令，執行向量搜尋，傳回與指定輸入圖片相似的產品圖片：

   ### SQL

   ```
   SELECT *
   FROM
   VECTOR_SEARCH(
     TABLE cymbal_pets.products_embedding,
     'embedding',
     (SELECT embedding FROM AI.GENERATE_EMBEDDING(
       MODEL `cymbal_pets.embedding_model`,
       (SELECT OBJ.MAKE_REF('gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/cozy-naps-cat-scratching-post-with-condo.png', 'us.cymbal_conn') as content)
     ))
   );
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_image = bpd.DataFrame(
       {
           "uri": [
               "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/cozy-naps-cat-scratching-post-with-condo.png"
           ]
       }
   ).cache()
   df_image["image"] = bbq.obj.make_ref(df_image["uri"], "us.cymbal_conn")
   df_search = bbq.ai.generate_embedding(
       embedding_model,
       bbq.obj.get_access_url(bbq.obj.fetch_metadata(df_image["image"]), "R"),
   )

   search_result = bbq.vector_search(
       "cymbal_pets.products_embedding", "embedding", df_search["embedding"]
   )
   search_result
   ```

   結果類似下方：

   ```
   +-----------------+-----------------+----------------+----------------------------------------------+--------------------+-------------------------------+------------------------------------------------+----------------+
   | query.embedding | base.product_id | base.embedding | base.image.uri                               | base.image.version | base.image.authorizer         | base.image.details                             | distance       |
   +-----------------+-----------------+----------------+----------------------------------------------+--------------------+-------------------------------+------------------------------------------------+----------------+
   | -0.0112330541   | 181             | -0.0112330541  | gs://cloud-samples-data/bigquery/            | 12345678910        | myproject.region.myconnection | {"gcs_metadata":{"content_type":               | 0.0            |
   | 0.0142525584    |                 |  0.0142525584  | tutorials/cymbal-pets/images/                |                    |                               | "image/png","md5_hash":"21234567hst16555w60j", |                |
   | 0.0135886827    |                 |  0.0135886827  | cozy-naps-cat-scratching-post-with-condo.png |                    |                               | "size":828318,"updated":1742492688982000}}     |                |
   | 0.0149955815    |                 |  0.0149955815  |                                              |                    |                               |                                                |                |
   | ...             |                 |  ...           |                                              |                    |                               |                                                |                |
   |                 |                 |                |                                              |                    |                               |                                                |                |
   |                 |                 |                |                                              |                    |                               |                                                |                |
   +-----------------+-----------------+----------------+----------------------------------------------+--------------------+-------------------------------+------------------------------------------------+----------------+
   | -0.0112330541   | 187             | -0.0190353896  | gs://cloud-samples-data/bigquery/            | 23456789101        | myproject.region.myconnection | {"gcs_metadata":{"content_type":               | 0.4216330832.. |
   | 0.0142525584    |                 |  0.0116206668  | tutorials/cymbal-pets/images/                |                    |                               | "image/png","md5_hash":"7328728fhakd9937djo4", |                |
   | 0.0135886827    |                 |  0.0136198215  | cozy-naps-cat-scratching-post-with-bed.png   |                    |                               | "size":860113,"updated":1742492688774000}}     |                |
   | 0.0149955815    |                 |  0.0173457414  |                                              |                    |                               |                                                |                |
   | ...             |                 |  ...           |                                              |                    |                               |                                                |                |
   |                 |                 |                |                                              |                    |                               |                                                |                |
   |                 |                 |                |                                              |                    |                               |                                                |                |
   +-----------------+-----------------+----------------+----------------------------------------------+--------------------+-------------------------------+------------------------------------------------+----------------+
   | ...             | ...             | ...            | ...                                          | ...                | ...                           | ...                                            | ...            |
   +-----------------+-----------------+----------------+----------------------------------------------+--------------------+-------------------------------+------------------------------------------------+----------------+
   ```

## 使用 `ObjectRef` 值陣列處理排序的多模態資料

本節說明如何完成下列工作：

1. 重新建立 `product_manuals` 表格，使其同時包含 `Crittercuisine 5000` 產品手冊的 PDF 檔案，以及該手冊每一頁的 PDF 檔案。
2. 建立表格，將手冊對應至各個區塊。代表完整手冊的 `ObjectRef` 值會儲存在 `STRUCT<uri STRING, version STRING, authorizer STRING, details JSON>>` 欄中。代表手冊頁面的 `ObjectRef` 值會儲存在 `ARRAY<STRUCT<uri STRING, version STRING, authorizer STRING, details JSON>>` 資料欄中。
3. 一起分析 `ObjectRef` 值陣列，傳回單一產生值。
4. 分別分析 `ObjectRef` 值陣列，並為每個陣列值傳回產生的值。

在分析工作期間，您會將 `ObjectRef` 值陣列轉換為 [`ObjectRefRuntime`](https://docs.cloud.google.com/bigquery/docs/analyze-multimodal-data?hl=zh-tw#objectrefruntime_values) 值的排序清單，然後將該清單傳遞至 Gemini 模型，並在提示中指定 `ObjectRefRuntime` 值。`ObjectRefRuntime` 值會提供已簽署的網址，模型可透過這些網址存取 Cloud Storage 中的物件資訊。

請按照下列步驟，使用 `ObjectRef` 值陣列處理排序的多模態資料：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 執行下列指令，重新建立 `product_manuals` 資料表：

   ### SQL

   ```
   CREATE OR REPLACE EXTERNAL TABLE `cymbal_pets.product_manuals`
     WITH CONNECTION `us.cymbal_conn`
     OPTIONS (
       object_metadata = 'SIMPLE',
       uris = [
           'gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/documents/*.pdf',
           'gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/document_chunks/*.pdf']);
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   bbq.create_external_table(
       "cymbal_pets.product_manuals_all",
       replace=True,
       connection_name="us.cymbal_conn",
       options={
           "object_metadata": "SIMPLE",
           "uris": [
               "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/documents/*.pdf",
               "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/document_chunks/*.pdf",
           ],
       },
   )
   ```
3. 執行下列指令，將 PDF 資料寫入 `map_manual_to_chunks` 資料表：

   ### SQL

   ```
   -- Extract the file and chunks into a single table.
   -- Store the chunks in the chunks column as array of ObjectRefs (ordered by page number)
   CREATE OR REPLACE TABLE cymbal_pets.map_manual_to_chunks
   AS
   SELECT ARRAY_AGG(m1.ref)[0] manual, ARRAY_AGG(m2.ref ORDER BY m2.ref.uri) chunks
   FROM cymbal_pets.product_manuals m1
   JOIN cymbal_pets.product_manuals m2
     ON
       REGEXP_EXTRACT(m1.uri, r'.*/([^.]*).[^/]+')
       = REGEXP_EXTRACT(m2.uri, r'.*/([^.]*)_page[0-9]+.[^/]+')
   GROUP BY m1.uri;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df1 = bpd.read_gbq("SELECT * FROM cymbal_pets.product_manuals_all").sort_values(
       "uri"
   )
   df2 = df1.copy()
   df1["name"] = df1["uri"].str.extract(r".*/([^.]*).[^/]+")
   df2["name"] = df2["uri"].str.extract(r".*/([^.]*)_page[0-9]+.[^/]+")
   df_manuals_all = df1.merge(df2, on="name")
   df_manuals_agg = (
       bbq.array_agg(df_manuals_all[["ref_x", "uri_x"]].groupby("uri_x"))["ref_x"]
       .str[0]
       .to_frame()
   )
   df_manuals_agg["chunks"] = bbq.array_agg(
       df_manuals_all[["ref_y", "uri_x"]].groupby("uri_x")
   )["ref_y"]
   ```
4. 執行下列指令，查看 `map_manual_to_chunks` 資料表中的 PDF 資料：

   ### SQL

   ```
   SELECT *
   FROM cymbal_pets.map_manual_to_chunks;
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_manuals_agg
   ```

   結果類似下方：

   ```
   +-------------------------------------+--------------------------------+-----------------------------------+------------------------------------------------------+-------------------------------------------+---------------------------------+------------------------------------+-------------------------------------------------------+
   | manual.uri                          | manual.version                 | manual.authorizer                 | manual.details                                       | chunks.uri                                | chunks.version                  | chunks.authorizer                  | chunks.details                                        |
   +-------------------------------------+--------------------------------+-----------------------------------+------------------------------------------------------+-------------------------------------------+---------------------------------+------------------------------------+-------------------------------------------------------+
   | gs://cloud-samples-data/bigquery/   | 1742492785900455               | myproject.region.myconnection     | {"gcs_metadata":{"content_type":"application/pef",   | gs://cloud-samples-data/bigquery/         | 1745875761227129                | myproject.region.myconnection      | {"gcs_metadata":{"content_type":"application/pdf",    |
   | tutorials/cymbal-pets/documents/    |                                |                                   | "md5_hash":"c9032b037693d15a33210d638c763d0e",       | tutorials/cymbal-pets/documents/          |                                 |                                    | "md5_hash":"5a1116cce4978ec1b094d8e8b49a1d7c",        |
   | crittercuisine_5000_user_manual.pdf |                                |                                   | "size":566105,"updated":1742492785941000}}           | crittercuisine_5000_user_manual_page1.pdf |                                 |                                    | "size":504583,"updated":1745875761266000}}            |
   |                                     |                                |                                   |                                                      +-------------------------------------------+---------------------------------+------------------------------------+-------------------------------------------------------+
   |                                     |                                |                                   |                                                      | crittercuisine_5000_user_manual_page1.pdf | 1745875760613874                | myproject.region.myconnection      | {"gcs_metadata":{"content_type":"application/pdf",    |
   |                                     |                                |                                   |                                                      | tutorials/cymbal-pets/documents/          |                                 |                                    | "md5_hash":"94d03ec65d28b173bc87eac7e587b325",        |
   |                                     |                                |                                   |                                                      | crittercuisine_5000_user_manual_page2.pdf |                                 |                                    | "size":94622,"updated":1745875760649000}}             |
   |                                     |                                |                                   |                                                      +-------------------------------------------+---------------------------------+------------------------------------+-------------------------------------------------------+
   |                                     |                                |                                   |                                                      | ...                                       | ...                             |  ...                               | ...                                                   |
   +-------------------------------------+--------------------------------+-----------------------------------+------------------------------------------------------+-------------------------------------------+---------------------------------+------------------------------------+-------------------------------------------------------+
   ```
5. 執行下列指令，根據陣列的 `ObjectRef` 值分析結果，從 Gemini 模型產生單一回覆：

   ### SQL

   ```
   WITH
     manuals AS (
       SELECT
         OBJ.GET_ACCESS_URL(manual, 'r') AS manual,
         ARRAY(
           SELECT OBJ.GET_ACCESS_URL(chunk, 'r') AS chunk
           FROM UNNEST(m1.chunks) AS chunk WITH OFFSET AS idx
           ORDER BY idx
         ) AS chunks
       FROM cymbal_pets.map_manual_to_chunks AS m1
     )
   SELECT result AS Response
   FROM
     AI.GENERATE_TEXT(
       MODEL `cymbal_pets.gemini`,
       (
         SELECT
           (
             'Can you provide a page by page summary for the first 3 pages of the attached manual? Only write one line for each page. The pages are provided in serial order',
             manuals.chunks) AS prompt,
         FROM manuals
       ));
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_manuals_agg["chunks_url"] = bbq.array_agg(
       bbq.obj.get_access_url(df_manuals_agg.explode("chunks")["chunks"], "R").groupby(
           "uri_x"
       )
   )
   df_manuals_agg[
       "prompt0"
   ] = "Can you provide a page by page summary for the first 3 pages of the attached manual? Only write one line for each page. The pages are provided in serial order"
   df_manuals_agg["prompt"] = bbq.struct(df_manuals_agg[["prompt0", "chunks_url"]])

   result = bbq.ai.generate_text(gemini_model, df_manuals_agg["prompt"])["result"]
   result
   ```

   結果類似下方：

   ```
   +-------------------------------------------+
   | Response                                  |
   +-------------------------------------------+
   | Page 1: This manual is for the            |
   | CritterCuisine Pro 5000 automatic         |
   | pet feeder.                               |
   | Page 2: The manual covers safety          |
   | precautions, what's included,             |
   | and product overview.                     |
   | Page 3: The manual covers assembly,       |
   | initial setup, and programming the clock. |
   +-------------------------------------------+
   ```
6. 執行下列指令，根據 `ObjectRef` 值陣列的分析結果，從 Gemini 模型產生多個回覆：

   ### SQL

   ```
   WITH
     input_chunked_objrefs AS (
       SELECT row_id, offset, chunk_ref
       FROM
         (
           SELECT ROW_NUMBER() OVER () AS row_id, * FROM `cymbal_pets.map_manual_to_chunks`
         ) AS indexed_table
       LEFT JOIN
         UNNEST(indexed_table.chunks) AS chunk_ref
         WITH OFFSET
     ),
     get_access_urls AS (
       SELECT row_id, offset, chunk_ref, OBJ.GET_ACCESS_URL(chunk_ref, 'r') AS ObjectRefRuntime
       FROM input_chunked_objrefs
     ),
     valid_get_access_urls AS (
       SELECT *
       FROM get_access_urls
       WHERE ObjectRefRuntime['runtime_errors'] IS NULL
     ),
     ordered_output_objrefruntime_array AS (
       SELECT ARRAY_AGG(ObjectRefRuntime ORDER BY offset) AS ObjectRefRuntimeArray
       FROM valid_get_access_urls
       GROUP BY row_id
     )
   SELECT
     page1_summary,
     page2_summary,
     page3_summary
   FROM
     AI.GENERATE_TABLE(
       MODEL `cymbal_pets.gemini`,
       (
         SELECT
           (
             'Can you provide a page by page summary for the first 3 pages of the attached manual? Only write one line for each page. The pages are provided in serial order',
             ObjectRefRuntimeArray) AS prompt,
         FROM ordered_output_objrefruntime_array
       ),
       STRUCT(
         'page1_summary STRING, page2_summary STRING, page3_summary STRING' AS output_schema));
   ```

   ### BigQuery DataFrames

   在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
   詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   result = bbq.ai.generate_table(
       gemini_model,
       df_manuals_agg["prompt"],
       output_schema={
           "page1_summary": "STRING",
           "page2_summary": "STRING",
           "page3_summary": "STRING",
       },
   )[["page1_summary", "page2_summary", "page3_summary"]]
   result
   ```

   結果類似下方：

   ```
   +-----------------------------------------------+-------------------------------------------+----------------------------------------------------+
   | page1_summary                                 | page2_summary                             | page3_summary                                      |
   +-----------------------------------------------+-------------------------------------------+----------------------------------------------------+
   | This manual provides an overview of the       | This section explains how to program      | This page covers connecting the feeder to Wi-Fi    |
   | CritterCuisine Pro 5000 automatic pet feeder, | the feeder's clock, set feeding           | using the CritterCuisine Connect app,  remote      |
   | including its features, safety precautions,   | schedules, copy and delete meal settings, | feeding, managing feeding schedules, viewing       |
   | assembly instructions, and initial setup.     | manually feed your pet, record            | feeding logs, receiving low food alerts,           |
   |                                               | a voice message, and understand           | updating firmware, creating multiple pet profiles, |
   |                                               | the low food level indicator.             | sharing access with other users, and cleaning      |
   |                                               |                                           | and maintaining the feeder.                        |
   +-----------------------------------------------+-------------------------------------------+----------------------------------------------------+
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

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]