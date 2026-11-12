Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Google Cloud 控制台在 BigQuery ML 中建立機器學習模型

本文說明如何使用 Google Cloud 控制台建立 BigQuery ML 模型。

## 必要的角色

* 如要建立模型並執行推論，您必須具備下列角色：

  + BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)
  + BigQuery 使用者 (`roles/bigquery.user`)

## 事前準備

1. 在 Google Cloud 控制台的專案選取器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需具備特定 IAM 角色，只要您已獲派某個專案的角色，即可選取該專案。
   * **建立專案**：如要建立專案，您必須具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。如果採用這種做法，當您完成這些步驟後，就可以直接刪除該專案，並移除相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認 Google Cloud 專案已啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project)。
3. 啟用 BigQuery 和 BigQuery Connection API (如果尚未啟用)。

   **啟用 API 所需的角色**

   您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過擁有者角色 (`roles/owner`) 取得這項權限。否則，您可以透過 Service Usage 管理員角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)

## 特定模型的前置作業

建立模型前，請務必先完成所建模型類型的必要條件：

* 如要使用查詢選取模型的訓練資料，必須將該查詢設為[已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw)。
* 矩陣分解模型需要預留項目。詳情請參閱「[定價](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw#pricing)」。
* 下列遠端模型需要 [Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)：

  + [Gemini Enterprise Agent Platform 和合作夥伴模型的遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)
  + [開放式模型上的遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)
  + [Cloud AI 服務的遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)
  + [Gemini Enterprise Agent Platform 中的遠端模型與自訂模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https?hl=zh-tw)

  連線的服務帳戶也必須具備特定角色，具體取決於遠端模型的類型。
* 如要匯入模型，您必須將模型上傳至 Cloud Storage bucket。

## 建立資料集

建立 BigQuery 資料集來存放資源：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，點選專案名稱。
4. 依序點選 more\_vert**「查看動作」>「建立資料集」**。
5. 在「Create dataset」(建立資料集) 頁面執行下列操作：

   1. 在「資料集 ID」部分，輸入資料集名稱。
   2. 在「位置類型」部分，選取「區域」或「多區域」。

      * 如果選取「Region」(區域)，請從「Region」(區域) 清單中選取位置。
      * 如果選取「Multi-region」(多區域)，請從「Multi-region」(多區域) 清單中選取「US」(美國) 或「Europe」(歐洲)。
   3. 點選「建立資料集」。

### bq

1. 如要建立新的資料集，請使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset) 指令並加上 `--location` 旗標：

   ```
   bq --location=LOCATION mk -d DATASET_ID
   ```

   更改下列內容：

   * `LOCATION`：資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `DATASET_ID`：您要建立的資料集 ID。
2. 確認資料集已建立：

   ```
   bq ls
   ```

## 建立內部或外部訓練的模型

請按照下列程序建立以下類型的模型：

* 時間序列模型：

  + [`ARIMA_PLUS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)
  + [`ARIMA_PLUS_XREG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)
* 貢獻分析：[貢獻分析](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw)
* 分類：

  + [邏輯迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)
  + [提升決策樹分類](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
  + [隨機森林分類](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
  + [深層類神經網路 (DNN) 分類](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
  + [寬深分類](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
  + [AutoML 分類](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
* 迴歸：

  + [線性迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)
  + [提升樹迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
  + [隨機森林迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
  + [深層類神經網路 (DNN) 迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
  + [寬深迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
  + [AutoML 迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
* 分群法：[K-means](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw)
* 建議：[矩陣分解](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw)
* 降低維度：

  + [主成分分析 (PCA)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca?hl=zh-tw)
  + [自動編碼器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder?hl=zh-tw)

這些模型會根據類型提供不同的選項。雖然 BigQuery ML 自動調整功能在大多數情況下都能正常運作，但您也可以選擇在程序中手動調整模型。如要這麼做，請參閱特定模型類型的說明文件，進一步瞭解模型選項。

建立模型的步驟如下：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，依序點選「Datasets」(資料集) 和您建立的資料集。
4. 按一下資料集旁的 more\_vert「View actions」(查看動作)，然後點選「Create BQML Model」(建立 BQML 模型)。

   「Create new model」(建立新模型) 窗格隨即開啟。
5. 在「Model name」(模型名稱) 中輸入模型名稱。
6. 如要建立包含模型 `CREATE MODEL` 陳述式的已儲存的查詢，請選取「Save Query」(儲存查詢)。

   1. 在「查詢名稱」中，輸入已儲存的查詢名稱。
   2. 在「區域」部分，選擇已儲存的查詢的區域。
7. 按一下「繼續」。
8. 在「建立方法」部分，選取「在 BigQuery 中訓練模型」。
9. 在「Modeling objective」(模型建立目標) 部分，選取模型的模型建立目標。
10. 按一下「繼續」。
11. 在「Model options」(模型選項) 頁面中，選取模型類型。可選取的模型類型會因您選擇的模型目標而異。
12. 在「Training data」(訓練資料) 部分，執行下列任一操作：

    * 選取「Table/View」(資料表/檢視表)，從資料表或檢視表取得訓練資料，然後選取專案、資料集和檢視表或資料表名稱。
    * 選取「Query」(查詢)，從已儲存的查詢取得訓練資料，然後選取已儲存的查詢。
13. 在「Selected input label columns」(所選輸入標籤欄) 中，從資料表、檢視表或查詢中選擇要用作模型輸入內容的資料欄。
14. 如果畫面上顯示「Required options」(必要選項) 專區，請指定要求的資料欄資訊：

    * 如果是分類和迴歸模型，請在「INPUT\_LABEL\_COLS」**INPUT\_LABEL\_COLS**部分選取包含標籤資料的資料欄。
    * 如果是矩陣分解模型，請選取下列項目：

      + 在「RATING\_COL」**RATING\_COL**部分，選取包含評分資料的資料欄。
      + 在「USER\_COL」**USER\_COL**部分，選取包含使用者資料的資料欄。
      + 在「ITEM\_COL」**ITEM\_COL**部分，選取包含項目資料的資料欄。
    * 如果是時間序列預測模型，請選取下列項目：

      + 在「TIME\_SERIES\_TIMESTAMP\_COL」**TIME\_SERIES\_TIMESTAMP\_COL**部分，選取含有訓練模型時要使用的時間點資料欄。
      + 在「TIME\_SERIES\_DATA\_COL」**TIME\_SERIES\_DATA\_COL**部分，選取含有要預測資料的資料欄。
15. 選用：在「Optional」(選用) 部分，指定其他模型調整引數的值。可用的引數會因建立的模型類型而異。
16. 選用：如果畫面上顯示「Hyperparameter tuning」(超參數調整) 專區，您可以指定 **NUM\_TRIALS** 選項，為模型啟用 [超參數調整](/bigquery/docs/hyperparameter-tuning-tutorial)。可用於超參數調整的引數，會因您建立的模型類型而異。
17. 按一下「建立模型」。
18. 模型建立完成後，按一下「Go to model」(前往模型) 即可查看模型詳細資料。

## 依據預先訓練模型建立遠端模型

請按照下列程序建立下列類型的遠端模型：

* [Agent Platform 模型或合作夥伴模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)
* [模型與開放式模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)

建立模型的步驟如下：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，依序點選「Datasets」(資料集) 和您建立的資料集。
4. 按一下資料集旁的 more\_vert「View actions」(查看動作)，然後點選「Create BQML Model」(建立 BQML 模型)。

   「Create new model」(建立新模型) 窗格隨即開啟。
5. 在「Model name」(模型名稱) 中輸入模型名稱。
6. 如要建立包含模型 `CREATE MODEL` 陳述式的已儲存的查詢，請選取「Save Query」(儲存查詢)。

   1. 在「查詢名稱」中，輸入已儲存的查詢名稱。
   2. 在「區域」部分，選擇已儲存的查詢的區域。
7. 按一下「繼續」。
8. 在「Creation method」(建立方法) 區段中，選取「Connect to Vertex AI LLM service and Cloud AI services」(連線至 Vertex AI LLM 服務和 Cloud AI 服務)。
9. 在「Model options」(模型選項) 頁面，依據用途選取「Google and Partner Models」(Google 和合作夥伴模型) 或「Open Models」(開放模型)。
10. 在「Remote connection」(遠端連線) 部分，執行下列任一操作：

    * 如果您已設定[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，或同時具備 BigQuery 管理員和專案 IAM 管理員角色，請選取「Default connection」(預設連線)。
    * 如果未設定預設連線，或缺少適當角色，請選取「Cloud 資源連結」。

      1. 在「Project」(專案)，選取要使用的連線所在的專案。
      2. 在「Location」(位置) 部分，選取連線使用的位置。
      3. 在「Connection」(連線) 部分，選取要用於遠端模型的連線，或選取「Create new connection」(建立新連線) 建立新連線。

         **重要事項：**如果建立新的連線，請務必先為連線的服務帳戶授予適當角色，再繼續操作。如要進一步瞭解應授予哪些角色，請參閱您要建立的遠端模型類型參考文件。
11. 在「Required options」(必要選項) 部分，執行下列任一操作：

    * 如果是 Google 模型和合作夥伴模型上的遠端模型，請指定要使用的端點。這是模型的名稱，例如 `gemini-3.5-flash`。如要進一步瞭解支援的模型，請參閱 [`ENDPOINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw#endpoint)。
    * 如要透過開放原始碼模型使用遠端模型，請複製並貼上要使用的端點。這是部署至 Agent Platform 的模型共用公開端點，格式為 `https://location-aiplatform.googleapis.com/v1/projects/project/locations/location/endpoints/endpoint_id`。詳情請參閱 [`ENDPOINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#endpoint) 的說明。
12. 按一下「建立模型」。
13. 模型建立完成後，按一下「Go to model」(前往模型) 即可查看模型詳細資料。

## 在自訂模型上建立遠端模型

請按照下列程序，透過[部署至 Gemini Enterprise Agent Platform 的自訂模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https?hl=zh-tw)建立遠端模型。

建立模型的步驟如下：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，依序點選「Datasets」(資料集) 和您建立的資料集。
4. 按一下資料集旁的 more\_vert「View actions」(查看動作)，然後點選「Create BQML Model」(建立 BQML 模型)。

   「Create new model」(建立新模型) 窗格隨即開啟。
5. 在「Model name」(模型名稱) 中輸入模型名稱。
6. 如要建立包含模型 `CREATE MODEL` 陳述式的已儲存的查詢，請選取「Save Query」(儲存查詢)。

   1. 在「查詢名稱」中，輸入已儲存的查詢名稱。
   2. 在「區域」部分，選擇已儲存的查詢的區域。
7. 按一下「繼續」。
8. 在「Creation method」(建立方法) 區段，選取「Connect to user managed Vertex AI endpoints」(連線至使用者管理的 Vertex AI 端點)。
9. 在「Model options」(模型選項) 頁面的「Remote connection」(遠端連線) 部分，執行下列任一操作：

   * 如果您已設定[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，或同時具備 BigQuery 管理員和專案 IAM 管理員角色，請選取「Default connection」(預設連線)。
   * 如果未設定預設連線，或缺少適當角色，請選取「Cloud 資源連結」。

     1. 在「Project」(專案)，選取要使用的連線所在的專案。
     2. 在「Location」(位置) 部分，選取連線使用的位置。
     3. 在「Connection」(連線) 部分，選取要用於遠端模型的連線，或選取「Create new connection」(建立新連線) 建立新連線。

        **重要事項：**如果建立新的連線，請務必先為連線的服務帳戶授予適當角色，再繼續操作。如要進一步瞭解應授予哪些角色，請參閱您要建立的遠端模型類型參考文件。
10. 在「Required options」(必要選項) 部分，指定要使用的端點。這是部署至 Agent Platform 的模型共用公開端點，格式為 `https://location-aiplatform.googleapis.com/v1/projects/project/locations/location/endpoints/endpoint_id`。詳情請參閱 [`ENDPOINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https?hl=zh-tw#endpoint)。
11. 按一下「建立模型」。
12. 模型建立完成後，按一下「Go to model」(前往模型) 即可查看模型詳細資料。

## 透過 Cloud AI 服務建立遠端模型

請按照下列程序，透過 [Cloud AI 服務](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)建立遠端模型。

建立模型的步驟如下：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，依序點選「Datasets」(資料集) 和您建立的資料集。
4. 按一下資料集旁的 more\_vert「View actions」(查看動作)，然後點選「Create BQML Model」(建立 BQML 模型)。

   「Create new model」(建立新模型) 窗格隨即開啟。
5. 在「Model name」(模型名稱) 中輸入模型名稱。
6. 如要建立包含模型 `CREATE MODEL` 陳述式的已儲存的查詢，請選取「Save Query」(儲存查詢)。

   1. 在「查詢名稱」中，輸入已儲存的查詢名稱。
   2. 在「區域」部分，選擇已儲存的查詢的區域。
7. 按一下「繼續」。
8. 在「Creation method」(建立方法) 區段中，選取「Connect to Vertex AI LLM service and Cloud AI services」(連線至 Vertex AI LLM 服務和 Cloud AI 服務)。
9. 在「Model options」(模型選項) 頁面，選取「Cloud AI Services」(Cloud AI 服務)。
10. 在「Remote connection」(遠端連線) 部分，執行下列任一操作：

    * 如果您已設定[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，或同時具備 BigQuery 管理員和專案 IAM 管理員角色，請選取「Default connection」(預設連線)。
    * 如果未設定預設連線，或缺少適當角色，請選取「Cloud 資源連結」。

      1. 在「Project」(專案)，選取要使用的連線所在的專案。
      2. 在「Location」(位置) 部分，選取連線使用的位置。
      3. 在「Connection」(連線) 部分，選取要用於遠端模型的連線，或選取「Create new connection」(建立新連線) 建立新連線。

         **重要事項：**如果建立新的連線，請務必先為連線的服務帳戶授予適當角色，再繼續操作。如要進一步瞭解應授予哪些角色，請參閱您要建立的遠端模型類型參考文件。
11. 在「Required options」(必要選項) 部分，選取要使用的 Cloud AI 服務類型。
12. 如果您使用`CLOUD_AI_DOCUMENT_V1`服務，請在「Optional」(選用) 區段中指定[文件處理器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw#document_processor)資訊。如果您使用 `CLOUD_AI_SPEECH_TO_TEXT_V2` 服務，可以視需要指定[語音辨識工具](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw#speech_recognizer)資訊。
13. 按一下「建立模型」。
14. 模型建立完成後，按一下「Go to model」(前往模型) 即可查看模型詳細資料。

## 建立匯入的模型

請按照下列程序匯入下列類型的模型，建立 BigQuery ML 模型：

* [ONNX](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw)
* [TensorFlow](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw)
* [TensorFlow Lite](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tflite?hl=zh-tw)
* [XGBoost](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-xgboost?hl=zh-tw)

建立模型的步驟如下：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，依序點選「Datasets」(資料集) 和您建立的資料集。
4. 按一下資料集旁的 more\_vert「View actions」(查看動作)，然後點選「Create BQML Model」(建立 BQML 模型)。

   「Create new model」(建立新模型) 窗格隨即開啟。
5. 在「Model name」(模型名稱) 中輸入模型名稱。
6. 如要建立包含模型 `CREATE MODEL` 陳述式的已儲存的查詢，請選取「Save Query」(儲存查詢)。

   1. 在「查詢名稱」中，輸入已儲存的查詢名稱。
   2. 在「區域」部分，選擇已儲存的查詢的區域。
7. 按一下「繼續」。
8. 在「Creation method」(建立方法) 部分，選取「Import model」(匯入模型)。
9. 在「Model options」(模型選項) 頁面中，選取要匯入的模型類型。
10. 在「GCS path」(GCS 路徑)，瀏覽或貼上包含模型的 Cloud Storage bucket URI。
11. 按一下「建立模型」。
12. 模型建立完成後，按一下「Go to model」(前往模型) 即可查看模型詳細資料。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]