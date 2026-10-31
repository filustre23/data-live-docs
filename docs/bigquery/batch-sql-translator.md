Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用批次 SQL 翻譯器遷移程式碼

BigQuery 的批次 SQL 翻譯器可將其他 SQL 方言編寫的指令碼，大量翻譯成 GoogleSQL 查詢。您可以透過Google Cloud 控制台或指令列提交及查看批次翻譯工作的結果，加快大規模工作負載遷移作業。

如要建構自訂軟體整合、自動化 CI/CD 管道或其他程式輔助工作流程，請直接[呼叫 BigQuery Migration API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw)。如要瞭解支援的方言和處理位置，請參閱「[支援的 SQL 方言](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#supported_sql_dialects)」和「[位置](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#locations)」。

## 事前準備

提交翻譯工作前，請先完成下列步驟。

### 啟用 SQL 翻譯

啟用必要的 API，並取得使用 BigQuery SQL 翻譯工具所需的權限。詳情請參閱「[啟用 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#enable_sql_translations)」。

### 所需權限

如要取得使用互動式翻譯工具、Translation API 或批次 SQL 翻譯工具建立翻譯工作所需的權限，請要求管理員授予您 `parent` 資源的下列 IAM 角色：

* 查看及監控遷移工作：[MigrationWorkflow 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquerymigration?hl=zh-tw#bigquerymigration.viewer)  (`roles/bigquerymigration.viewer`)
* 提交遷移工作：[MigrationWorkflow 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquerymigration?hl=zh-tw#bigquerymigration.editor)  (`roles/bigquerymigration.editor`)
* 存取 Cloud Storage bucket 以取得輸入內容和檔案：Storage 物件管理員 (`roles/storage.objectAdmin`) - 位於來源和目的地 Cloud Storage bucket。

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備所需權限，可透過互動式翻譯工具、翻譯 API 或批次 SQL 翻譯工具建立翻譯工作。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用互動式翻譯工具、Translation API 或批次 SQL 翻譯工具建立翻譯工作，必須具備下列權限：

* `bigquerymigration.workflows.create`
* `bigquerymigration.workflows.get`
* `bigquerymigration.workflows.list`
* `bigquerymigration.workflows.delete`
* `bigquerymigration.subtasks.get`
* `bigquerymigration.subtasks.list`
* `storage.objects.get`
* `storage.objects.list`
* `storage.objects.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 收集來源檔案

來源檔案必須是文字檔，且包含來源方言的有效 SQL。來源檔案也可以包含註解。請盡可能使用各種方法，確保 SQL 有效。

### 建立中繼資料檔案

為協助服務產生更準確的翻譯結果，建議您提供中繼資料檔案。但這不是強制要求。

您可以使用 `dwh-migration-dumper` 指令列擷取工具產生中繼資料資訊。準備好中繼資料檔案後，您可以將這些檔案與來源檔案一併加入翻譯來源資料夾。翻譯工具會自動偵測並使用這些詞彙翻譯來源檔案，您不需要進行任何額外設定。

如要使用 `dwh-migration-dumper` 工具產生中繼資料資訊，請參閱「[產生翻譯的中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)」。

### 建立 YAML 設定檔

您可以視需要建立及使用[設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw)，自訂批次翻譯。這些檔案可用於以各種方式轉換翻譯輸出內容。舉例來說，您可以[建立設定 YAML 檔案，在翻譯期間變更 SQL 物件的大小寫](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#change_object-name_case)。

請使用下列其中一種方法，在翻譯工作中加入設定 YAML 檔案。

### 控制台

[將設定 YAML 檔案上傳至包含來源檔案的 Cloud Storage 目錄](#upload-files)。選取該目錄做為輸入位置時，翻譯工作會自動納入設定 YAML 檔案。

### gcloud

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

[`gcloud alpha bq translation translate-batch` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/alpha/bq/translation/translate-batch?hl=zh-tw)搭配使用的旗標，取決於設定 YAML 檔案的儲存位置：

* 如果設定 YAML 檔案與來源檔案位於相同目錄，則不需要任何額外旗標。在 `--source-gcs-uris` 或 `--source-local-dirs` 旗標中設定該目錄時，工作會自動納入設定 YAML 檔案。
* 如果設定 YAML 檔案是單獨儲存在本機電腦上，請使用 `--source-local-files` 旗標上傳檔案，並將檔案新增至工作。
* 如果設定 YAML 檔案另外儲存在 Cloud Storage，請使用 `--source-gcs-files` 旗標將檔案新增至工作。

舉例來說，下列指令會從本機電腦上傳來源檔案和個別儲存的設定 YAML 檔案，然後執行翻譯工作：

```
gcloud alpha bq translation translate-batch \
  --source-dialect=SOURCE_DIALECT \
  --target-dialect=TARGET_DIALECT \
  --location=LOCATION \
  --source-local-dirs=LOCAL_DIR=SOURCE_URI \
  --source-local-files=LOCAL_CONFIG_YAML=CONFIG_YAML_URI \
  --target-gcs-path=TARGET_URI
```

更改下列內容：

* `LOCAL_CONFIG_YAML`：設定 YAML 檔案的本機路徑，例如 `./configs/change-case.config.yaml`。
* `CONFIG_YAML_URI`：指令將設定 YAML 檔案上傳至的 Cloud Storage URI，例如 `gs://my_data_bucket/teradata/configs/change-case.config.yaml`。這個 URI 必須位於 `SOURCE_URI` 目錄之外。

如需其他預留位置的說明，請參閱「[提交翻譯工作](#submit_a_translation_job)」。

### 將輸入檔案上傳至 Cloud Storage

將包含要翻譯的查詢和指令碼的來源檔案上傳至 Cloud Storage。您也可以將[任何中繼資料檔案](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)或[設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw)，上傳至包含來源檔案的同一個 Cloud Storage bucket 和目錄。如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

### 選擇提交翻譯工作的方式

提交批次翻譯工作的方式有兩種：

* **Google Cloud 控制台**：使用使用者介面設定及提交工作。這種方法需要將來源檔案上傳至 Cloud Storage。
* **Google Cloud CLI**：使用 gcloud CLI 從指令列提交工作。`translate-batch` 指令會接受來源和目標位置做為旗標，並可為您將本機目錄和檔案上傳至 Cloud Storage。詳情請參閱「[提交翻譯工作](#submit_a_translation_job)」。

這兩種選項都要求來源檔案必須可透過 Cloud Storage 存取，且都會建立相同類型的翻譯工作。從指令列提交的工作，仍會顯示在Google Cloud 控制台的翻譯工作清單中。

## 提交翻譯工作

請使用下列其中一種方法啟動翻譯工作，並查看進度。如要查看結果，請參閱「[探索翻譯輸出內容](#explore_the_translation_output)」。

### 控制台

這些步驟假設您已將來源檔案上傳至 Cloud Storage bucket。

如要使用 Google Cloud 控制台提交批次翻譯工作，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」(SQL 轉譯) 頁面。

   [前往「SQL Translation」(SQL 翻譯) 頁面](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在「SQL 翻譯」面板中，按一下「開始翻譯」。
3. 在「Translation configuration」(翻譯設定) 中輸入下列資訊：

   1. 在「Display name」(顯示名稱) 中，輸入翻譯工作的名稱。名稱可包含英文字母、數字或底線。
   2. 在「Processing location」(處理位置) 中，選取要執行翻譯工作的位置。舉例來說，如果您位於歐洲，且不希望資料跨越任何位置限制範圍，請選取 `eu` 區域。選擇與來源檔案 bucket 相同的位置，翻譯工作才能發揮最佳效能。
   3. 在「Source dialect」(來源方言) 中，選取要翻譯的 SQL 方言。
   4. 在「目標方言」部分，選取「GoogleSQL」。
4. 點選「下一步」。
5. 在「File location details」(檔案位置詳細資料) 部分，指定要用於翻譯輸入和輸出的 Cloud Storage 路徑。您可以輸入 `bucket_name/folder_name/` 格式的路徑，或使用「Browse」(瀏覽) 選項前往資料夾。

   1. 在「Output directory location」(輸出目錄位置)，指定翻譯檔案的目的地 Cloud Storage 資料夾路徑。這是所有翻譯輸出的根目錄。
   2. 選擇一或多個「Input directory locations」(輸入目錄位置)，其中包含要翻譯的 SQL 檔案路徑。
   3. 如有需要，每個輸入目錄都可以在根輸出目錄下方，選擇性地指定**輸出子目錄名稱**。
6. 點選「下一步」。
7. 選取任何選用設定，自訂中繼資料和任何其他翻譯輸出內容。
8. 選用：如要進一步自訂翻譯行為，請建立設定 YAML 檔案，並將這些檔案放在輸入 Cloud Storage bucket 中。這些檔案可用於重新命名物件、啟用最佳化功能、使用 Gemini 強化翻譯等。如要進一步瞭解設定 YAML 檔案，請參閱「[建立設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw)」。
9. 按一下「Create」(建立)，啟動翻譯工作。

   建立翻譯工作後，您可以在翻譯工作清單中查看其狀態。

### gcloud

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要提交批次翻譯工作，請使用 [`gcloud alpha bq translation translate-batch` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/alpha/bq/translation/translate-batch?hl=zh-tw)。用於識別來源檔案的旗標，取決於檔案位於 Cloud Storage 還是本機電腦。

#### 翻譯 Cloud Storage 中的 SQL 檔案

如要翻譯已[上傳至 Cloud Storage](#upload-files) 的 SQL 檔案，請使用 `--source-gcs-uris` 旗標識別來源目錄。如要納入不在 `--source-gcs-uris` 中的檔案，可以使用 `--source-gcs-files` 旗標：

```
gcloud alpha bq translation translate-batch \
    --source-dialect=SOURCE_DIALECT \
    --target-dialect=TARGET_DIALECT \
    --location=LOCATION \
    --source-gcs-uris=SOURCE_URI \
    --target-gcs-path=TARGET_URI
```

更改下列內容：

* `SOURCE_DIALECT`：來源 SQL 檔案的方言，例如 `teradata`。如需支援的值，請參閱「[支援的 SQL 方言](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#supported_sql_dialects)」。
* `TARGET_DIALECT`：來源檔案要翻譯成的方言。例如：`bigquery`。
* `LOCATION`：處理工作的[位置](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#locations)，例如 `us`。
* `SOURCE_URI`：包含來源檔案的 Cloud Storage 目錄，例如 `gs://my_data_bucket/teradata/input/`。
* `TARGET_URI`：接收翻譯檔案的 Cloud Storage 目錄，例如 `gs://my_data_bucket/teradata/output/`。

#### 翻譯本機電腦上的 SQL 檔案

如要翻譯本機電腦上的檔案，請使用 `--source-local-dirs` 旗標，將每個本機目錄對應至 Cloud Storage URI。這個指令會將目錄上傳至該 URI，然後將 URI 納入翻譯工作，因此您不必自行上傳檔案：

```
gcloud alpha bq translation translate-batch \
    --source-dialect=SOURCE_DIALECT \
    --target-dialect=TARGET_DIALECT \
    --location=LOCATION \
    --source-local-dirs=LOCAL_DIR=SOURCE_URI \
    --target-gcs-path=TARGET_URI
```

將 `LOCAL_DIR` 替換為包含來源檔案的本機目錄，例如 `./teradata_queries`。如需其他預留位置的說明，請參閱「[翻譯 Cloud Storage 中的 SQL 檔案](#translate-gcs-files)」。

如要對應個別檔案而非目錄，請使用 `--source-local-files` 旗標。

#### 新增選用旗標

如要在翻譯後的 SQL 旁生成 Gemini 建議，請新增 `--enable-ai-suggestion` 旗標。

根據預設，指令會等待翻譯工作完成。如要提交工作並立即返回，請新增 `--async` 旗標。接著，指令會輸出翻譯 ID，您可以將該 ID 傳遞至 [`gcloud alpha bq translation describe` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/alpha/bq/translation/describe?hl=zh-tw)，以檢查工作狀態：

```
gcloud alpha bq translation describe TRANSLATION_ID \
    --location=LOCATION
```

#### 擷取輸出檔案

翻譯工作會將結果寫入您在 `--target-gcs-path` 旗標中設定的 Cloud Storage 目錄。這個目標目錄會存放翻譯檔案、翻譯摘要報表，以及任何 AI 建議檔案。

如要將輸出內容複製到本機電腦，請使用下列指令：

```
gcloud storage cp --recursive TARGET_URI LOCAL_DIRECTORY
```

更改下列內容：

* `TARGET_URI`：目標基礎 URI，例如 `gs://my_data_bucket/teradata/output/`。
* `LOCAL_DIRECTORY`：接收檔案的本機目錄。

即使您是透過指令列提交工作，該工作也會顯示在Google Cloud 控制台的翻譯工作清單中。如要查看翻譯輸出內容的品質，請參閱「[探索翻譯輸出內容](#explore_the_translation_output)」。

## 翻譯中繼資料

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

除了翻譯 SQL 指令碼，您也可以翻譯描述來源資料倉儲的中繼資料。中繼資料翻譯工作會讀取從來源系統擷取的中繼資料檔案，並寫入 GoogleSQL 資料定義語言 (DDL) 陳述式，在 BigQuery 中重新建立這些物件。

輸入內容是一或多個中繼資料 ZIP 檔案。如要瞭解如何使用 `dwh-migration-dumper` 工具產生這些檔案，請參閱「[產生翻譯中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)」。

您可以使用 Google Cloud 控制台或 gcloud CLI 翻譯中繼資料。選取下列選項之一：

### 控制台

中繼資料翻譯是常規翻譯工作的輸出選項：

1. 按照「[提交翻譯工作](#submit_a_translation_job)」中的步驟設定工作，並使用存放中繼資料 ZIP 檔案的 Cloud Storage 目錄做為輸入位置。
2. 在「選用設定」中，選取「DDL」。
3. 按一下「建立」，建立工作。

工作會將翻譯後的 DDL 陳述式和 SQL 寫入輸出目錄。

### gcloud

您可以將中繼資料翻譯視為獨立工作，或批次 SQL 翻譯工作的額外輸出內容。

**單獨翻譯中繼資料**

如果輸入內容是中繼資料 ZIP 檔案，且沒有要翻譯的 SQL，請使用 [`gcloud alpha bq translation translate-metadata` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/alpha/bq/translation/translate-metadata?hl=zh-tw)：

```
gcloud alpha bq translation translate-metadata \
  --source-dialect=SOURCE_DIALECT \
  --target-dialect=TARGET_DIALECT \
  --location=LOCATION \
  --source-gcs-uris=SOURCE_URI \
  --target-gcs-path=TARGET_URI
```

更改下列內容：

* `SOURCE_DIALECT`：來源中繼資料的方言，例如 `teradata`。如需支援的值，請參閱「[支援的 SQL 方言](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#supported_sql_dialects)」。
* `TARGET_DIALECT`：目標資料表的方言。例如：`bigquery`。
* `LOCATION`：處理工作的[位置](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#locations)，例如 `us`。
* `SOURCE_URI`：包含中繼資料 ZIP 檔案的 Cloud Storage 目錄，例如 `gs://my_data_bucket/teradata/metadata/`。
* `TARGET_URI`：接收翻譯 DDL 陳述式的 Cloud Storage 目錄，例如 `gs://my_data_bucket/teradata/ddl_output/`。

如要指向個別中繼資料 ZIP 檔案，而非目錄，請使用 `--source-gcs-files` 旗標。如要從本機電腦上傳中繼資料檔案，做為工作的一部分，請使用 `--source-local-dirs` 或 `--source-local-files` 旗標。

與批次翻譯工作一樣，指令會等待工作完成。新增 `--async` 旗標，即可提交工作並立即傳回翻譯 ID。

**在批次 SQL 翻譯中翻譯中繼資料**

如果批次翻譯輸入內容已包含中繼資料 ZIP 檔案，就不需要執行第二項工作。使用 `--target-types` 旗標，將 `metadata` 新增至批次工作的翻譯輸出內容，工作就會在單次執行中寫入翻譯後的 SQL 和 DDL 陳述式：

```
gcloud alpha bq translation translate-batch \
  --source-dialect=SOURCE_DIALECT \
  --target-dialect=TARGET_DIALECT \
  --location=LOCATION \
  --source-gcs-uris=SOURCE_URI \
  --target-gcs-path=TARGET_URI \
  --target-types=sql,metadata
```

如要瞭解 [`translate-batch` 指令](#submit_a_translation_job)接受的其他旗標，請參閱「[提交翻譯工作](#submit_a_translation_job)」。

## 生成來源 DDL

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如果來源 SQL 參照的資料表沒有定義，翻譯工具不一定能解析物件，導致 `RelationNotFound` 或 `AttributeNotFound` 問題。

解決這些問題的最佳方法，是提供來源物件的實際定義。對來源系統執行 `dwh-migration-dumper` 工具，並將產生的中繼資料 ZIP 檔案納入翻譯輸入內容。如需操作說明，請參閱「[產生翻譯的中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)」。擷取的中繼資料會準確描述物件，因此翻譯工具不需猜測即可解析。

如果無法擷取中繼資料 (例如無法再存取來源系統)，可以問問 Gemini 改為從來源 SQL 推論缺少的 DDL 陳述式。Gemini 會根據物件在查詢中的使用方式推論這些 DDL 陳述式，因此請務必先檢查並驗證這些陳述式，再加以使用。

您可以使用Google Cloud 控制台或 gcloud CLI，為翻譯作業產生來源 DDL。選取下列其中一個選項：

### 控制台

Gemini 會在一般翻譯工作中生成來源 DDL 建議：

1. 按照「[提交翻譯工作](#submit_a_translation_job)」中的步驟設定工作。
2. 在「選用設定」中，選取「Gemini AI 建議」。
3. 按一下「建立」，建立工作。

如果翻譯作業產生 `RelationNotFound` 或 `AttributeNotFound` 問題，則會針對未解決的物件，產生建議的來源 DDL 陳述式。這項工作也會翻譯 SQL，因此您不必另外建立工作。

### gcloud

[`gcloud alpha bq translation generate-source-ddl` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/alpha/bq/translation/generate-source-ddl?hl=zh-tw)會讀取來源 SQL，並傳回建議的來源 DDL 陳述式：

```
gcloud alpha bq translation generate-source-ddl \
  --source-dialect=SOURCE_DIALECT \
  --target-dialect=TARGET_DIALECT \
  --location=LOCATION \
  --source-gcs-uris=SOURCE_URI \
  --target-gcs-path=TARGET_URI
```

將 `SOURCE_URI` 替換為包含來源 SQL 檔案的 Cloud Storage 目錄，並將 `TARGET_URI` 替換為接收產生的 DDL 陳述式的 Cloud Storage 目錄。其他預留位置與「[翻譯中繼資料](#translate_metadata)」一節所述相同。

如要改為在翻譯工作中產生建議，請將 `--enable-ai-suggestion` 旗標新增至 [`translate-batch` 指令](#submit_a_translation_job)。

接著，您可以將產生的 DDL 陳述式做為後續翻譯工作的輸入內容，提高翻譯品質。詳情請參閱「[`RelationNotFound` 或 `AttributeNotFound` 翻譯問題](#batch-relation-attribute-not-found)」。

## 探索翻譯輸出內容

無論是透過指令列或 Google Cloud 控制台提交翻譯工作，您都可以在 Google Cloud 控制台查看工作結果。批次 SQL 轉譯器會將下列檔案輸出至指定目的地：

* 翻譯後的檔案。
* CSV 格式的翻譯摘要報表。
* AI 建議檔案。

### Google Cloud 控制台輸出內容

如要查看翻譯工作詳細資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」(SQL 轉譯) 頁面。

   [前往「SQL Translation」(SQL 翻譯) 頁面](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中，找出要查看翻譯詳細資料的工作。然後按一下翻譯工作名稱。
   您可以查看桑基圖，瞭解工作的整體品質、輸入的程式碼行數 (不含空白行和註解)，以及翻譯過程中發生的問題清單。建議您由左至右優先修正。早期階段的問題可能會導致後續階段出現其他問題。
3. 將滑鼠游標懸停在錯誤或警告列上，然後查看建議，決定偵錯翻譯工作的後續步驟。
4. 選取「Log Summary」(記錄摘要) 分頁標籤，即可查看翻譯問題摘要，包括問題類別、建議動作，以及各問題的發生頻率。點選桑基圖視覺化長條，即可篩選問題。您也可以選取問題類別，查看與該問題類別相關聯的記錄訊息。
5. 選取「Log Messages」(記錄訊息) 分頁標籤，即可查看各項翻譯問題的詳細資料，包括問題類別、特定問題訊息，以及發生問題的檔案連結。點選桑基圖視覺化長條，即可篩選問題。您可以在「**Log
   Message**」分頁中選取問題，開啟「[**Code**](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw#code-tab)」
   分頁，其中會顯示輸入和輸出檔案 (如有)。
6. 按一下「Job details」(工作詳細資料) 分頁標籤，查看翻譯工作設定詳細資料。

### 摘要報告

摘要報表是 CSV 檔案，內含翻譯工作期間遇到的所有警告和錯誤訊息表格。

如要在 Google Cloud 控制台查看摘要檔案，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」(SQL 轉譯) 頁面。

   [前往「SQL Translation」(SQL 翻譯) 頁面](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中，找出您感興趣的工作，然後按一下工作名稱，或依序點選**「More options」(更多選項) >「Show details」(顯示詳細資料)**。
3. 在「Job details」(工作詳細資料) 分頁的「Translation report」(翻譯報表) 部分，按一下「translation\_report.csv」。
4. 在「Object details」(物件詳細資料) 頁面中，按一下「Authenticated URL」(已驗證網址) 列中的值，即可在瀏覽器中查看檔案。

下表說明摘要檔案的資料欄：

| **資料欄** | **說明** |
| --- | --- |
| 時間戳記 | 問題發生的時間戳記。 |
| FilePath | 與問題相關聯的來源檔案路徑。 |
| FileName | 與問題相關聯的來源檔案名稱。 |
| ScriptLine | 發生問題的行號。 |
| ScriptColumn | 發生問題的資料欄編號。 |
| TranspilerComponent | 發生警告或錯誤的翻譯引擎內部元件。這個資料欄可能為空。 |
| 環境 | 與警告或錯誤相關聯的翻譯方言環境。這個資料欄可能為空。 |
| ObjectName | 來源檔案中與警告或錯誤相關聯的 SQL 物件。這個資料欄可能為空。 |
| 嚴重性 | 問題的嚴重程度，分為警告或錯誤。 |
| 類別 | 翻譯問題類別。 |
| SourceType | 問題來源。這個資料欄的值可以是 `SQL` (表示輸入 SQL 檔案有問題)，或 `METADATA` (表示中繼資料套件有問題)。 |
| 訊息 | 翻譯問題警告或錯誤訊息。 |
| ScriptContext | 來源檔案中與問題相關聯的 SQL 程式碼片段。 |
| 動作 | 建議您採取行動來解決問題。 |

### 「Code」分頁

程式碼分頁可讓您進一步查看特定翻譯工作的輸入和輸出檔案資訊。在程式碼分頁中，您可以檢查翻譯工作使用的檔案、並排比較輸入檔案和翻譯結果，找出不準確之處，以及查看工作中特定檔案的記錄摘要和訊息。

如要存取程式碼分頁，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」(SQL 轉譯) 頁面。

   [前往「SQL Translation」(SQL 翻譯) 頁面](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中，找出您感興趣的工作，然後按一下工作名稱，或依序點選**「More options」(更多選項) >「Show details」(顯示詳細資料)**。
3. 選取「程式碼」分頁標籤。「程式碼」分頁包含下列面板：

   * 檔案總管：包含用於翻譯的所有 SQL 檔案。按一下檔案，即可查看翻譯輸入和輸出內容，以及翻譯中的任何翻譯問題。
   * **以 Gemini 補強的輸入內容**：翻譯引擎翻譯的輸入 SQL。如果您[在 Gemini 設定](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#ai_yaml_guidelines)中，為來源 SQL 指定 Gemini 自訂規則，翻譯工具會先轉換原始輸入內容，再翻譯 Gemini 強化後的輸入內容。如要查看原始輸入內容，請按一下「View original input」(查看原始輸入內容)。
   * **翻譯輸出內容**：翻譯結果。如果您在 [Gemini 設定](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#ai_yaml_guidelines)中，為目標 SQL 指定了 Gemini 自訂規則，則轉換作業會套用至轉譯結果，做為 Gemini 強化輸出內容。如果有 Gemini 強化輸出內容，可以點選「Gemini suggestion」(Gemini 建議) 按鈕，查看 Gemini 強化輸出內容。
4. 選用：如要在 [BigQuery 互動式 SQL 翻譯器](#debug-interactive-translator)中查看輸入檔案和輸出檔案，請按一下「Edit」(編輯)。您可以編輯檔案，並將輸出檔案存回 Cloud Storage。

**注意：** 您可以從[「Results」(結果) 頁面](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw#explore_the_translation_output)查看整體翻譯工作的記錄摘要和訊息

### 「設定」分頁

您可以在「Configuration」(設定) 分頁中新增、重新命名、查看或編輯設定 YAML 檔案。**結構定義探索工具**會顯示支援設定類型的說明文件，協助您編寫設定 YAML 檔案。編輯 YAML 設定檔後，您可以重新執行工作，使用新的設定。

如要存取「設定」分頁，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」(SQL 轉譯) 頁面。

   [前往「SQL Translation」(SQL 翻譯) 頁面](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中，找出您感興趣的工作，然後按一下工作名稱，或依序點選**「More options」(更多選項) >「Show details」(顯示詳細資料)**。
3. 在「Translation details」(翻譯詳細資料) 視窗中，按一下「Configuration」(設定) 分頁標籤。

如要新增設定檔，請按照下列步驟操作：

1. 依序點選「more\_vert」more\_vert。
2. 接著，您可以在顯示的面板中，選擇新設定 YAML 檔案的類型、位置和名稱。
3. 點選「建立」。

如要編輯現有設定檔，請按照下列步驟操作：

1. 按一下設定 YAML 檔案。
2. 編輯檔案，然後按一下「儲存」。
3. 按一下「重新執行」，即可使用編輯過的設定 YAML 檔案執行新的轉譯工作。

如要重新命名現有的設定檔，請依序點選 more\_vert「More options」(更多選項) >「Rename」(重新命名)。

### 翻譯後的檔案

系統會在目的地路徑中，為每個來源檔案產生對應的輸出檔案。輸出檔案包含翻譯後的查詢。

**重要事項：** 我們會盡力翻譯，請盡可能驗證翻譯後的查詢。

## 使用輔助 UDF 處理不支援的 SQL 函式

將 SQL 從來源方言翻譯成 BigQuery 時，某些函式可能沒有直接對應的函式。為解決這個問題，BigQuery 遷移服務 (以及更廣泛的 BigQuery 社群) 提供輔助 user-defined function (UDF)，可複製這些不支援的來源方言函式行為。

這些 UDF 通常位於 `bqutil` 公開資料集，因此翻譯後的查詢一開始會使用 `bqutil.<dataset>.<function>()` 格式參照這些 UDF。例如：`bqutil.fn.cw_count()`。

### 正式環境注意事項

雖然 `bqutil` 可讓您輕鬆存取這些輔助 UDF，進行初步翻譯和測試，但基於下列原因，不建議直接依賴 `bqutil` 處理正式環境工作負載：

1. 版本管控：`bqutil` 專案會託管這些 UDF 的最新版本，這表示其定義可能會隨時間變更。如果 UDF 的邏輯更新，直接依賴 `bqutil` 可能會導致非預期的行為，或破壞正式版查詢。
2. 依附元件隔離：將 UDF 部署至自己的專案，可將正式環境與外部變更隔離。
3. 自訂：您可能需要修改或最佳化這些 UDF，以更符合特定商業邏輯或效能需求。但前提是這些映像檔必須位於您的專案中。
4. 安全性與管理：貴組織的安全性政策可能會限制直接存取 `bqutil` 等公開資料集，以處理正式環境資料。將 UDF 複製到受控環境符合這類政策。

### 將輔助 UDF 部署至專案

為讓您完全控管 UDF 版本、自訂和存取權，建議您將輔助 UDF 部署至自己的專案和資料集，以便在正式環境中可靠穩定地使用。如要進一步瞭解將輔助 UDF 部署至環境所需的指令碼和步驟，請參閱「[部署 UDF](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/udfs#deploying-the-udfs)」。

## 疑難排解

本節說明如何對個別查詢進行偵錯，以及如何解決最常見的翻譯錯誤。

### 使用互動式 SQL 翻譯器，對批次翻譯的 SQL 查詢進行偵錯

您可以使用 BigQuery 互動式 SQL 翻譯器，透過與來源資料庫相同的中繼資料或物件對應資訊，查看或偵錯 SQL 查詢。完成批次翻譯工作後，BigQuery 會產生翻譯設定 ID，其中包含工作的中繼資料、物件對應或結構定義搜尋路徑等資訊 (視查詢而定)。您可以使用批次翻譯設定 ID 搭配互動式 SQL 翻譯器，以指定設定執行 SQL 查詢。

您可以使用Google Cloud 控制台或 gcloud CLI，對批次翻譯的 SQL 查詢進行偵錯。選取下列其中一個選項：

### 控制台

如要使用批次翻譯設定 ID 啟動互動式 SQL 翻譯，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」(SQL 轉譯) 頁面。

   [前往「SQL Translation」(SQL 翻譯) 頁面](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中，找出您感興趣的工作，然後依序點選「more\_vert More Options」(更多選項) **>「Open Interactive Translation」(開啟互動式翻譯)**。

   BigQuery 互動式 SQL 翻譯器現在會開啟，並顯示對應的批次翻譯設定 ID。如要查看互動式翻譯的翻譯設定 ID，請在互動式 SQL 翻譯工具中，依序點選「Tools」(工具) >「Query translation」(查詢翻譯) >「Translation settings」(翻譯設定)。

如要在互動式 SQL 翻譯器中偵錯批次翻譯檔案，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「SQL Translation」(SQL 轉譯) 頁面。

   [前往「SQL Translation」(SQL 翻譯) 頁面](https://console.cloud.google.com/bigquery/migrations?hl=zh-tw)
2. 在翻譯工作清單中，找出您感興趣的工作，然後按一下工作名稱，或依序點選**「More options」(更多選項) >「Show details」(顯示詳細資料)**。
3. 在「Translation details」(翻譯詳細資料) 視窗中，按一下「Code」(程式碼) 分頁標籤。
4. 在檔案總管中，按一下檔案名稱即可開啟檔案。
5. 按一下輸出檔案名稱旁的「Edit」(編輯)，在互動式 SQL 翻譯器 ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)) 中開啟檔案。

   您會看到輸入和輸出檔案填入互動式 SQL 翻譯器，該翻譯器現在使用對應的批次翻譯設定 ID。
6. 如要將編輯過的輸出檔案儲存回 Cloud Storage，請在
   互動式 SQL 轉譯器中，依序點選**「Save」(儲存) >「Save To GCS」(儲存至 GCS)**。

### gcloud

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要重新翻譯及檢查單一查詢，而不開啟Google Cloud 控制台，請使用 [`gcloud alpha bq translation translate` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/alpha/bq/translation/translate?hl=zh-tw)。如果您已將批次翻譯問題縮小至單一查詢，並想在本機反覆測試，這項功能就非常實用。

```
gcloud alpha bq translation translate \
  --source-dialect=SOURCE_DIALECT \
  --target-dialect=TARGET_DIALECT \
  --location=LOCATION \
  --input-file=INPUT_FILE \
  --output-file=OUTPUT_FILE \
  --translation-log-file=LOG_FILE \
  --explanation-output-file=EXPLANATION_FILE
```

更改下列內容：

* `INPUT_FILE`：包含要翻譯查詢的本機檔案。如果省略這個旗標，指令會從標準輸入內容讀取查詢。
* `OUTPUT_FILE`：接收翻譯查詢的本機檔案。如果省略這個旗標，指令會將查詢寫入標準輸出內容。
* `LOG_FILE`：接收翻譯記錄的本機 YAML 檔案，其中包含Google Cloud 控制台「Log Messages」(記錄訊息) 分頁中顯示的問題訊息。
* `EXPLANATION_FILE`：本機檔案，用於接收 Gemini 生成的翻譯說明。

如要重複使用批次工作的中繼資料，讓查詢解析相同的物件，請新增 `--metadata-gcs-uri` 旗標。詳情請參閱「[將查詢翻譯為 GoogleSQL](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw#translate_a_query_into_standard_sql)」。

### 排解翻譯錯誤

以下各節說明使用批次 SQL 轉譯器時常見的錯誤。

### `RelationNotFound` 或 `AttributeNotFound` 翻譯問題

使用[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw#submit_a_translation_job)翻譯查詢後，可能會遇到翻譯失敗的情況，並顯示 `RelationNotFound` 或 `AttributeNotFound` 錯誤。

如要找出失敗的翻譯，請前往 Google Cloud 控制台 BigQuery 的「Translation details」(翻譯詳細資料) 頁面，然後開啟「Log Messages」(記錄訊息) 分頁。

翻譯服務最適合搭配中繼資料 DDL 使用。如果找不到 SQL 物件定義，轉譯引擎會引發 `RelationNotFound` 或 `AttributeNotFound` 問題。建議使用中繼資料擷取器產生中繼資料套件，確保所有物件定義都存在。建議您先新增中繼資料，再解決大部分的翻譯錯誤，因為這個步驟通常可以修正許多因缺少中繼資料而間接造成的其他錯誤。

詳情請參閱「[產生翻譯和評估的中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)」。

#### 使用 Gemini 修正翻譯問題

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

如要修正失敗的翻譯工作，並解決 `RelationNotFound` 或 `AttributeNotFound` 錯誤，您也可以使用 Gemini 解決這些問題：

1. 前往「Translation details」(翻譯詳細資料) 頁面，然後開啟「Log Messages」(記錄訊息) 分頁。
2. 在「類別」欄中，按一下含有「`RelationNotFound`」或「`AttributeNotFound`」訊息的查詢。
3. 如要前往程式碼分頁中包含錯誤的檔案和行，請按一下

   錯誤訊息。
4. 在「動作」欄中，按一下「建議修正」。
5. 選取下列其中一個選項：「套用」或「套用並重新執行」：

   * 如要將產生的結構定義檔案從輸出目錄複製到輸入目錄，請按一下「Apply」。
   * 如要將產生的結構定義檔案從輸出目錄複製到輸入目錄，並開啟重新執行視窗，請按一下「Apply and rerun」。

## 配額與限制

* 適用 [BigQuery Migration API 配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#migration-api-limits)。
* 每個專案最多可有 10 項進行中的翻譯工作。
* 雖然來源和中繼資料檔案總數沒有硬性限制，但建議將檔案數量控制在 1000 個以下，以提升效能。

## 定價

使用批次 SQL 轉譯器不會產生費用。不過，用於儲存輸入和輸出檔案的儲存空間會產生一般費用。詳情請參閱「[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

## 替代遷移工作流程指令列工具

您也可以使用翻譯設定檔，透過 Google Cloud CLI (`gcloud bq migration-workflows`) 或 bq 指令列工具提交批次翻譯工作。

這些步驟假設您已將來源檔案上傳至 Cloud Storage bucket。

### 建立轉譯設定檔

翻譯設定檔會定義來源檔案的路徑、輸出目的地，以及翻譯的來源和目標方言。您可以使用 YAML 或 JSON 格式編寫這個檔案。

**注意：** 轉譯設定檔與[設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw)不同。翻譯設定檔會定義工作本身。YAML 設定檔可自訂翻譯工具轉換 SQL 的方式。

以下範例顯示 Teradata 至 BigQuery 翻譯的翻譯設定 YAML 檔案：

```
tasks:
  translation_task:
    type: Teradata2BigQuery_Translation
    translationDetails:
      sourceTargetMapping:
      - sourceSpec:
          baseUri: gs://bq-translations/input
        targetSpec:
          relativePath: output
      targetBaseUri: gs://bq-translations
      targetTypes:
      - sql
      sourceEnvironment:
        defaultDatabase: default_db
        schemaSearchPath:
        - foo
```

以下範例顯示 Teradata 至 BigQuery 翻譯的翻譯設定 JSON 檔案：

```
{
  "tasks": {
    "translation_task": {
      "type": "Teradata2BigQuery_Translation",
      "translationDetails": {
        "sourceTargetMapping": [
          {
            "sourceSpec": {
              "literal": {
                "literalString": "sel 1",
                "relativePath": "my_input_1"
              },
              "encoding": "UTF-8"
            }
          },
          {
            "sourceSpec": {
              "literal": {
                "literalString": "sel 2",
                "relativePath": "my_input_2"
              },
              "encoding": "UTF-8"
            }
          }
        ],
        "targetReturnLiterals": [
          "sql/my_input_1",
          "sql/my_input_2"
        ]
      }
    }
  }
}
```

### 提交及管理翻譯工作

使用下列其中一項指令列工具，提交及管理翻譯工作。

### gcloud

如要建立翻譯工作並執行工作流程，請使用下列指令：

```
gcloud bq migration-workflows create --location=LOCATION --config-file=CONFIG_FILE
```

如要建立及執行工作流程，並立即傳回工作流程連結，請新增 `--async` 旗標：

```
gcloud bq migration-workflows create --location=LOCATION --config-file=CONFIG_FILE --async
```

如要列出翻譯工作，請使用下列指令：

```
gcloud bq migration-workflows list --location=LOCATION
```

如要查看特定翻譯工作的詳細資料，請使用下列指令：

```
gcloud bq migration-workflows describe projects/PROJECT_ID/locations/LOCATION/workflows/WORKFLOW_ID
```

更改下列內容：

* `LOCATION`：執行這項翻譯工作的 Google Cloud 專案位置。
* `CONFIG_FILE`：翻譯設定檔的路徑。
* `PROJECT_ID`：執行這項翻譯工作的 Google Cloud 專案 ID。
* `WORKFLOW_ID`：翻譯工作的 ID。

### bq

如要執行翻譯工作，請使用下列指令：

```
bq mk --migration_workflow --location=LOCATION --config_file=CONFIG_FILE
```

如要列出所有翻譯工作，請使用下列指令：

```
bq ls --migration_workflow --location=LOCATION
```

如要查看特定翻譯工作的詳細資料，請使用下列指令：

```
bq show --migration_workflow projects/PROJECT_ID/locations/LOCATION/workflows/WORKFLOW_ID
```

如要從清單中移除翻譯工作，請使用下列指令：

```
bq rm --migration_workflow projects/PROJECT_ID/locations/LOCATION/workflows/WORKFLOW_ID
```

更改下列內容：

* `LOCATION`：執行這項翻譯工作的 Google Cloud 專案位置。
* `CONFIG_FILE`：翻譯設定檔的路徑。
* `PROJECT_ID`：執行這項翻譯工作的 Google Cloud 專案 ID。
* `WORKFLOW_ID`：翻譯工作的 ID。

### 擷取輸出檔案

如要在工作完成後下載輸出檔案，請按照「[擷取輸出檔案](#retrieve-output-files)」一節所述，使用 `gcloud storage cp`。如要在 Google Cloud 控制台中查看工作，請參閱「[探索翻譯輸出內容](#explore_the_translation_output)」。

## 後續步驟

進一步瞭解資料倉儲遷移作業的下列步驟：

* [遷移作業總覽](https://docs.cloud.google.com/bigquery/docs/migration-intro?hl=zh-tw)
* [遷移評估](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)
* [結構定義與資料移轉總覽](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw)
* [資料管道](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw)
* [互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)
* [資料安全性與管理](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)
* [資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator#data-validation-tool)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-30 (世界標準時間)。"],[],[]]