Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 SQL、物件資料表和 BigQuery DataFrame 分析多模態資料 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用 SQL 查詢、[`AI.GENERATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw)、[`AI.EMBED` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-embed?hl=zh-tw)和 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)，[分析 Cymbal 寵物商店公開資料集的多模態資料](https://docs.cloud.google.com/bigquery/docs/analyze-multimodal-data?hl=zh-tw)。

`AI.GENERATE` 函式可讓您分析結構化和非結構化資料的任何組合，`AI.EMBED` 函式則可讓您從 BigQuery 中的文字或圖片資料建立[嵌入](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-embed?hl=zh-tw#embeddings)。

您可以使用 [`VECTOR_SEARCH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search) 函式尋找相似圖片。`VECTOR_SEARCH` 函式可讓您對嵌入執行語意搜尋或混合搜尋，找出相似的實體。

本教學課程使用永久[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)，儲存 `ObjectRef` 值。

## 目標

* 使用 `ObjectRef` 值，在 BigQuery 資料表中儲存圖片資料和結構化資料。
* 使用 `AI.GENERATE` 函式充實資料。
* 使用 `AI.EMBED` 函式，根據圖片資料生成嵌入。
* 使用 `VECTOR_SEARCH` 函式尋找相似圖片。
* 使用 `ObjectRef` 值陣列，總結使用手冊。

## 費用

在本文件中，您會使用下列 Google Cloud計費元件：

* **BigQuery**: you incur costs for the data that you
  process in BigQuery.
* **Cloud Storage**: you incur costs for reading the objects
  stored in Cloud Storage.
* **Gemini Enterprise Agent Platform**: you incur costs for
  calls to Agent Platform models.

您可以使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)，根據預測用量估算費用。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

如要進一步瞭解費用，請參閱下列定價頁面：

* [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)
* [Agent Platform 定價](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing?hl=zh-tw)

## 事前準備

1. 在 Google Cloud 控制台的專案選取器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需具備特定 IAM 角色，只要您在專案中獲派角色，即可選取該專案。
   * **建立專案**：如要建立專案，您必須具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，不要選取現有專案。如果採用這種做法，當您完成這些步驟後，就可以直接刪除該專案，並移除相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認 Google Cloud 專案已啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project)。
3. 啟用 BigQuery、BigQuery Connection、Cloud Storage 和 Agent Platform API (如有尚未啟用的 API)。

   **啟用 API 所需的角色**

   如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過擁有者角色 (`roles/owner`) 取得這項權限。否則，您可以透過服務使用情形管理員角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Cstorage.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

### 必要的角色

如要取得完成本教學課程所需的權限，請要求管理員授予您下列 IAM 角色：

* 建立資料集和資料表：[BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)
* 執行 BigQuery 工作：[BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 建立連線：[BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)
* 將權限授予連線的服務帳戶：[專案 IAM 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/resourcemanager?hl=zh-tw#resourcemanager.projectIamAdmin)  (`roles/resourcemanager.projectIamAdmin`)
* 建立網址，以便讀取及修改 Cloud Storage 物件：[BigQuery ObjectRef 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.objectRefAdmin)  (`roles/bigquery.objectRefAdmin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立資料集、資料表、模型和連結

在本節中，您將建立本教學課程使用的資料集、連線、資料表和模型。

### 建立資料集

請選擇下列其中一種方式，建立 BigQuery 資料集，用來存放您在本教學課程中建立的物件：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」中展開專案，然後按一下「資料集」。
4. 在「Datasets」(資料集) 頁面，按一下「Create dataset」(建立資料集)add。
5. 在「Create dataset」(建立資料集) 頁面執行下列操作：

   1. 在「Dataset ID」(資料集 ID) 中輸入 `cymbal_pets`。
   2. 在「資料位置」部分，選取「US」。
   3. 其餘設定請保留預設狀態，然後點選「Create dataset」(建立資料集)。

### SQL

使用 [`CREATE SCHEMA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_schema_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE SCHEMA PROJECT_ID.cymbal_pets
     OPTIONS (
       description = 'Dataset for BigQuery ML tutorial',
       location = 'US');
   ```

   將 `PROJECT_ID` 替換為您的專案 ID。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

您會收到類似以下的確認訊息：`The dataset
named cymbal_pets was created.`

### 建立連線

建立 [Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，並取得連結的服務帳戶。BigQuery 會使用連線存取 Cloud Storage 中的物件。

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中，點選「連線」。
3. 在「Connections」(連線) 頁面，按一下「Create connection」(建立連線)。
4. 在「外部資料來源」頁面，執行下列操作：

   1. 在「連線類型」部分，選擇「Vertex AI 遠端模型、遠端函式、Lakehouse 和 Spanner (Cloud 資源)」。
   2. 在「連線 ID」欄位輸入 `cymbal_conn`。
   3. 其餘設定維持不變，然後點選「Create connection」(建立連線)。
5. 在「Connections」(連線) 頁面中，按一下 `cymbal_conn`。
6. 在「連線資訊」窗格，複製「服務帳戶 ID」值，後續步驟會用到這項資訊。

### 授予 Agent Platform 模型的使用權限

將 Agent Platform 使用者角色授予連線的服務帳戶，以便存取 Agent Platform 中的遠端模型。您必須在先前建立或選取的專案中授予這個角色。如果在其他專案授予角色，會導致 `bqcx-1234567890-abcd@gcp-sa-bigquery-condel.iam.gserviceaccount.com
does not have the permission to access resource` 錯誤。

如要授予服務帳戶使用 Agent Platform 模型的權限，請按照下列步驟操作：

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理) 頁面](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下person\_add「Grant access」(授予存取權)。
3. 在「Grant access」(授予存取權) 對話方塊中，執行下列操作：

   1. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
   2. 在「選取角色」欄位中，選擇或搜尋「Agent Platform User」。
   3. 按一下 [儲存]。

### 建立 `products` 資料表

如要建立包含 Cymbal Pets 產品資訊的標準資料表，請按照下列步驟從 Cloud Storage 載入資料：

1. 前往 Google Cloud 控制台的「Studio」頁面。

   [前往 Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如要建立 `products` 資料表，請選擇下列其中一個選項：

   ### SQL

   將這個指令貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   LOAD DATA OVERWRITE cymbal_pets.products
   FROM
     FILES(
       format = 'avro',
       uris = [
         'gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/tables/products/products_*.avro']);
   ```

   您會收到類似以下的確認訊息：`Data was
   successfully loaded into managed table.`

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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

### 建立 `product_images` 資料表

如要建立包含 Cymbal Pets 產品圖片的物件資料表 (`product_images`)，請選取下列其中一個選項：

### SQL

將這個指令貼到查詢編輯器，然後點選「play\_circle 執行」：

```
CREATE OR REPLACE EXTERNAL TABLE cymbal_pets.product_images
  WITH CONNECTION `us.cymbal_conn`
  OPTIONS (
    object_metadata = 'SIMPLE',
    uris = ['gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/*.png'],
    max_staleness = INTERVAL 30 MINUTE,
    metadata_cache_mode = AUTOMATIC);
```

您會收到類似以下的確認訊息：`This
statement created a new table named product_images.`

### BigQuery DataFrames

試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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

### 可建立模型

本教學課程中的 SQL 指令說明如何呼叫 AI 函式，不需建立模型。如果您按照 BigQuery DataFrames 操作說明操作，請選取該選項，建立代表 Gemini 模型和多模態嵌入模型的[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。

### SQL

您可以略過這個步驟。

### BigQuery DataFrames

試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
gemini_model = bbq.ml.create_model(
    "cymbal_pets.gemini",
    replace=True,
    connection_name="us.cymbal_conn",
    options={"endpoint": "gemini-3.5-flash"},
)
```

```
gemini_model = bbq.ml.create_model(
    "cymbal_pets.gemini",
    replace=True,
    connection_name="us.cymbal_conn",
    options={"endpoint": "gemini-3.5-flash"},
)
```

```
embedding_model = bbq.ml.create_model(
    "cymbal_pets.embedding_model",
    replace=True,
    connection_name="us.cymbal_conn",
    options={"endpoint": "gemini-embedding-2"},
)
```

```
embedding_model = bbq.ml.create_model(
    "cymbal_pets.embedding_model",
    replace=True,
    connection_name="us.cymbal_conn",
    options={"endpoint": "gemini-embedding-2"},
)
```

## 建立含有多模態資料的 `products_mm` 資料表

建立 `products_mm` 資料表，其中包含 `image` 資料欄，並填入 `product_images` 物件資料表中的產品圖片。建立的 `image` 資料欄是 [`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type) 資料欄，使用 [`ObjectRef`](https://docs.cloud.google.com/bigquery/docs/work-with-objectref?hl=zh-tw) 值將圖片資料與結構化資料一併儲存在 BigQuery [標準資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)中。

`ObjectRef` 值是 `STRUCT` 類型，具有預先定義的結構定義，可參照 Cloud Storage 物件進行[多模態分析](https://docs.cloud.google.com/bigquery/docs/analyze-multimodal-data?hl=zh-tw)。`ObjectRef` 值可由 [`OBJ` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-tw)、[AI 函式](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw)或 [Python 使用者定義函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions-python?hl=zh-tw)處理。

如要建立 `products_mm` 資料表並填入資料，請按照下列步驟操作：

1. 如要建立 `products_mm` 資料表，請選擇下列其中一個選項：

   ### SQL

   將這個指令貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   CREATE OR REPLACE TABLE cymbal_pets.products_mm
   AS
   SELECT products.* EXCEPT (uri), ot.ref AS image FROM cymbal_pets.products
   INNER JOIN cymbal_pets.product_images ot
   ON ot.uri = products.uri;
   ```

   您會收到類似以下的確認訊息：`This
   statement created a new table named products_mm.`

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_images = bpd.read_gbq("SELECT * FROM cymbal_pets.product_images")
   df_products = bpd.read_gbq("cymbal_pets.products")

   df_products_mm = df_images.merge(df_products, on="uri").drop(columns="uri")
   df_products_mm = df_products_mm.rename(columns={"ref": "image"})
   ```

   ```
   df_images = bpd.read_gbq("SELECT * FROM cymbal_pets.product_images")
   df_products = bpd.read_gbq("cymbal_pets.products")

   df_products_mm = df_images.merge(df_products, on="uri").drop(columns="uri")
   df_products_mm = df_products_mm.rename(columns={"ref": "image"})
   ```
2. 如要查看「`image`」欄資料，請選擇下列其中一個選項：

   ### SQL

   將這個指令貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   SELECT product_name, image
   FROM cymbal_pets.products_mm
   ```

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_products_mm[["product_name", "image"]]
   ```

   ```
   df_products_mm[["product_name", "image"]]
   ```

   結果大致如下：

   ```
   +--------------------------------+--------------------------------------+---------------+-------------------------------+------------------------------------------------+
   | product_name                   | image.uri                            | image.version | image.authorizer              | image.details                                  |
   +--------------------------------+--------------------------------------+---------------+-------------------------------+------------------------------------------------+
   |  AquaClear Aquarium Background | gs://cloud-samples-data/bigquery/    | 1234567891011 | myproject.region.myconnection | {"gcs_metadata":{"content_type":"image/png",   |
   |                                | tutorials/cymbal-pets/images/        |               |                               | "md5_hash":"494f63b9b137975ff3e7a11b060edb1d", |
   |                                | aquaclear-aquarium-background.png    |               |                               | "size":1282805,"updated":1742492680017000}}    |
   +--------------------------------+--------------------------------------+---------------+-------------------------------+------------------------------------------------+
   |  AquaClear Aquarium            | gs://cloud-samples-data/bigquery/    | 2345678910112 | myproject.region.myconnection | {"gcs_metadata":{"content_type":"image/png",   |
   |  Gravel Vacuum                 | tutorials/cymbal-pets/images/        |               |                               | "md5_hash":"b7bfc2e2641a77a402a1937bcf0003fd", |
   |                                | aquaclear-aquarium-gravel-vacuum.png |               |                               | "size":820254,"updated":1742492682411000}}     |
   +--------------------------------+--------------------------------------+---------------+-------------------------------+------------------------------------------------+
   | ...                            | ...                                  | ...           |                               | ...                                            |
   +--------------------------------+--------------------------------------+---------------+-------------------------------+------------------------------------------------+
   ```

## 生成產品資訊

使用 [`AI.GENERATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw)為寵物用品店產品生成下列資料：

* 在 `products_mm` 資料表中新增 `image_description` 資料欄。
* 填入 `products_mm` 資料表的 `animal_type`、`search_keywords` 和 `subcategory` 欄。
* 執行查詢，傳回每個產品品牌的說明，以及該品牌的產品數量。系統會分析該品牌所有產品的產品資訊 (包括產品圖片)，生成品牌說明。

使用 `AI.GENERATE` 函式時，您可以選擇根據指定的自訂結構定義，生成文字或[結構化輸出內容](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw#use_structured_output)。這個函式會向 Gemini 模型傳送要求，並傳回包含生成資料、完整模型回覆和狀態的結構體。

如要產生產品資料，請按照下列步驟操作：

1. 如要使用 `AI.GENERATE` 生成產品資訊，請選擇下列其中一個選項：

   ### SQL

   如要建立 `image_description` 欄並填入資料，請將下列內容貼到查詢編輯器，然後按一下 play\_circle「Run」(執行)：

   ```
   -- Add the column to the existing table
   ALTER TABLE bqml_tutorial.products_mm
   ADD COLUMN IF NOT EXISTS image_description STRING;

   -- Populate the new column using the AI.GENERATE function
   UPDATE bqml_tutorial.products_mm
   SET image_description = AI.GENERATE(
   ('Describe the following image: ', image),
   endpoint => 'gemini-3.5-flash'
   ).result
   WHERE image_description IS NULL;
   ```

   您會收到類似以下的確認訊息：`This
   statement altered the table named products_mm.`

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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
2. 如要查看 `image_description` 欄的內容，請將下列內容貼到查詢編輯器中，然後按一下 play\_circle「Run」(執行)：

   ```
   SELECT product_name, image_description
   FROM cymbal_pets.products_mm;
   ```

   結果大致如下：

   ```
   +--------------------------------+-------------------------------------+
   | product_name                   | image_description                   |
   +--------------------------------+-------------------------------------+
   |  AquaClear Aquarium Background | The image shows a colorful coral    |
   |                                | reef backdrop. The background is a  |
   |                                | blue ocean with a bright light...   |
   |                                |                                     |
   |                                |                                     |
   +--------------------------------+-------------------------------------+
   |  AquaClear Aquarium            | The image shows a long, clear       |
   |  Gravel Vacuum                 | plastic tube with a green hose      |
   |                                | attached to one end. The tube...    |
   |                                |                                     |
   |                                |                                     |
   +--------------------------------+-------------------------------------+
   | ...                            | ...                                 |
   +--------------------------------+-------------------------------------+
   ```
3. 如要使用產生的資料更新 `animal_type`、`search_keywords` 和 `subcategory` 資料欄，請選擇下列其中一個選項：

   ### SQL

   將下列內容貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   UPDATE cymbal_pets.products_mm t
   SET
   animal_type = r.animal_type,
   search_keywords = SPLIT(r.search_keywords, ','),
   subcategory = r.subcategory
   FROM (
   SELECT
     product_id,
     g.* EXCEPT(full_response, status)
   FROM bqml_tutorial.products_mm,
   UNNEST([AI.GENERATE(
     ('For the image and description of a pet product, concisely generate the following metadata: 1) animal_type and 2) 5 SEO search keywords (comma separated), and 3) product subcategory. ', image, description),
     endpoint => 'gemini-3.5-flash',
     output_schema => 'animal_type STRING, search_keywords STRING, subcategory STRING'
   )]) AS g
   ) r
   WHERE t.product_id = r.product_id;
   ```

   您會收到類似以下的確認訊息：`This
   statement modified 205 rows in products_mm.`

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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
4. 如要查看產生的資料，請選擇下列其中一個選項：

   ### SQL

   將下列內容貼到查詢編輯器，然後按一下「play\_circle 執行」：

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

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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

   結果大致如下：

   ```
   +--------------------------------+-------------------------------------+-------------+------------------------+------------------+
   | product_name                   | image_description                   | animal_type | search_keywords        | subcategory      |
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
5. 如要產生每個產品品牌的說明，以及該品牌產品的數量，請選擇下列其中一個選項：

   ### SQL

   將下列內容貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   SELECT
   brand,
   COUNT(*) AS cnt,
   AI.GENERATE(('Use the images and text to give one concise brand description ',
               'for a website brand page. Return the description only.',
                 ARRAY_AGG(image LIMIT 10), ARRAY_AGG(description), ARRAY_AGG(category),
                 ARRAY_AGG(subcategory)),
               endpoint => 'gemini-2.5-pro').result AS brand_description
   FROM
   cymbal_pets.products_mm
   GROUP BY brand
   ORDER BY cnt DESC;
   ```

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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

   結果大致如下：

   ```
   +--------------+-------------------------------------+-----+
   | brand        | brand_description                   | cnt |
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

## 生成嵌入項目並執行向量搜尋

從圖片資料生成嵌入，然後使用[向量搜尋](https://docs.cloud.google.com/bigquery/docs/vector-search-intro?hl=zh-tw)，透過嵌入傳回相似圖片。

在正式環境中，建議您先建立[向量索引](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_vector_index_statement)，再執行向量搜尋。向量索引可讓您更快速地執行向量搜尋，並傳回更近似的結果，但召回率會降低。

如要建立嵌入並執行向量搜尋，請按照下列步驟操作：

1. 如要建立 `products_embeddings` 資料表，請選擇下列其中一個選項：

   ### SQL

   將下列內容貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   CREATE OR REPLACE TABLE cymbal_pets.products_embedding
   AS (
   SELECT
     product_id,
     AI.EMBED(image, endpoint => 'gemini-embedding-2').result AS embedding,
     image
   FROM cymbal_pets.products_mm
   );
   ```

   您會收到類似以下的確認訊息：`This
   statement created a new table named products_embedding.`

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_products_mm["content"] = bbq.obj.get_access_url(df_products_mm["image"], "R")
   df_embed = bbq.ai.generate_embedding(
       embedding_model, df_products_mm[["content", "product_id"]]
   )

   df_embed.to_gbq("cymbal_pets.products_embedding", if_exists="replace")
   ```

   ```
   df_products_mm["content"] = bbq.obj.get_access_url(df_products_mm["image"], "R")
   df_embed = bbq.ai.generate_embedding(
       embedding_model, df_products_mm[["content", "product_id"]]
   )

   df_embed.to_gbq("cymbal_pets.products_embedding", if_exists="replace")
   ```
2. 如要執行向量搜尋，傳回與指定輸入圖片相似的產品圖片，請選擇下列其中一個選項：

   ### SQL

   將下列內容貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   SELECT *
   FROM
   VECTOR_SEARCH(
     TABLE cymbal_pets.products_embedding,
     'embedding',
     query_value => AI.EMBED(
                     OBJ.MAKE_REF('gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/cozy-naps-cat-scratching-post-with-condo.png'),
                     endpoint => 'gemini-embedding-2').result);
   ```

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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

   結果大致如下：

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

本節說明如何使用 `ObjectRef` 值陣列處理排序的多模態資料，產生使用手冊摘要。BigQuery 可使用陣列，同時分析多個非結構化檔案。

您將完成下列工作：

1. 建立 `product_manuals` 資料表，其中包含 `Crittercuisine Pro 5000` 產品手冊的 PDF 檔案，以及該手冊各頁面的 PDF 檔案。
2. 建立表格，將手冊對應至其區塊。完整手冊和手冊頁面分別儲存在 `ObjectRef` 資料欄中。
3. 一併分析 `ObjectRef` 值陣列，傳回單一生成值。
4. 分別分析 `ObjectRef` 值陣列，並傳回每個陣列值的生成值。

如要使用 `ObjectRef` 值處理排序的多模態資料，請按照下列步驟操作：

1. 如要建立 `product_manuals` 資料表，請選擇下列其中一個選項：

   ### SQL

   將下列內容貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   CREATE OR REPLACE EXTERNAL TABLE `cymbal_pets.product_manuals`
   WITH CONNECTION `us.cymbal_conn`
   OPTIONS (
     object_metadata = 'SIMPLE',
     uris = [
         'gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/documents/*.pdf',
         'gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/document_chunks/*.pdf']);
   ```

   您會收到類似以下的確認訊息：`This
   statement created a new table named product_manuals.`

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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
2. 如要將 PDF 資料寫入 `map_manual_to_chunks` 資料表，請選擇下列其中一個選項：

   ### SQL

   將下列內容貼到查詢編輯器，然後按一下「play\_circle 執行」：

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

   您會收到類似以下的確認訊息：`This
   statement created a new table named map_manual_to_chunks.`

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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
3. 如要查看 `map_manual_to_chunks` 資料表中的 PDF 資料，請選擇下列其中一個選項：

   ### SQL

   將下列內容貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   SELECT *
   FROM cymbal_pets.map_manual_to_chunks;
   ```

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

   如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
   詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

   ```
   df_manuals_agg
   ```

   ```
   df_manuals_agg
   ```

   結果大致如下：

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
4. 如要根據 `ObjectRef` 值陣列的分析結果，從 Gemini 模型生成單一回覆，請選擇下列其中一個選項：

   ### SQL

   將下列內容貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   SELECT
   AI.GENERATE((
     '''Can you provide a page by page summary for the first 3 pages of the attached manual?
     Only write one line for each page. The pages are provided in serial order''',
     chunks),
     endpoint => 'gemini-3.5-flash').result AS Response,
   FROM cymbal_pets.map_manual_to_chunks;
   ```

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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

   結果大致如下：

   ```
   +---------------------------------------------------------------------------+
   | Response                                                                  |
   +---------------------------------------------------------------------------+
   | Here is a one-line summary for each of the first 3 pages:                 |
   |                                                                           |
   | Page 1 introduces the CritterCuisine Pro 5000 automatic pet feeder and    |
   | presents the initial part of the manual's Table of Contents.              |
   | Page 2 lists the items included with the feeder and details important     |
   | safety precautions for its use.                                           |
   | Page 3 describes the feeder's key features, provides assembly and initial |
   | setup instructions, and begins the programming guide with clock setting.  |
   +---------------------------------------------------------------------------+
   ```
5. 如要根據 `ObjectRef` 值陣列的分析結果，從 Gemini 模型生成多個回覆，請選擇下列其中一個選項：

   ### SQL

   將下列內容貼到查詢編輯器，然後按一下「play\_circle 執行」：

   ```
   WITH results AS (
   SELECT
     AI.GENERATE((
       '''Can you provide a page by page summary for the first 3 pages of the attached manual?
       Only write one line for each page. The pages are provided in serial order''',
       chunks),
       endpoint => 'gemini-3.5-flash',
       output_schema =>  'page1_summary STRING, page2_summary STRING, page3_summary STRING').*
   FROM cymbal_pets.map_manual_to_chunks)
   SELECT page1_summary, page2_summary, page3_summary
   FROM results;
   ```

   ### BigQuery DataFrames

   試用這個範例前，請先按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定操作說明操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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

   結果大致如下：

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

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

**注意**：刪除專案會造成以下影響：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

或者，如要保留專案並刪除本教學課程中使用的資源，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中展開專案，然後點選「資料集」。
3. 在 `bqml_tutorial` 資料集，依序點按 more\_vert
   **「Open actions」(開啟動作) >「Delete」(刪除)**。
4. 在「Delete dataset」(刪除資料集) 對話方塊中，按一下「Delete」(刪除) 即可確認。
5. 點選左側窗格中的「連線」。
6. 針對 `cymbal_conn` 連線，依序點選more\_vert
   **「Open actions」(開啟動作) > 「Delete」(刪除)**。
7. 在「Delete connection」(刪除連線) 對話方塊中輸入 `delete`，然後按一下「Delete」(刪除) 確認操作。

## 後續步驟

* 如要進一步瞭解如何處理多模態資料，請參閱「[在 BigQuery 中分析多模態資料](https://docs.cloud.google.com/bigquery/docs/analyze-multimodal-data?hl=zh-tw)」。
* 如要進一步瞭解 `ObjectRef` 值，請參閱「[使用 ObjectRef 值](https://docs.cloud.google.com/bigquery/docs/work-with-objectref?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]