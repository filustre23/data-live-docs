Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Translation API 翻譯 SQL 查詢

本文說明如何在 BigQuery 中使用 BigQuery Migration API，將其他 SQL 方言編寫的指令碼翻譯成 GoogleSQL 查詢。

**注意：** 如要透過 Google Cloud 控制台或指令列執行翻譯工作，請參閱「[使用批次 SQL 翻譯器翻譯 SQL 查詢](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)」。只有在建構自訂軟體整合、自動化 CI/CD 管道或程式輔助工作流程時，才應使用本頁所述的 BigQuery Migration API。

如要查看這項 SQL 翻譯工具支援的 SQL 方言和處理位置清單，請參閱「[支援的 SQL 方言](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#supported_sql_dialects)」和「[位置](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#locations)」。

## 事前準備

提交翻譯工作前，請先完成下列步驟。

### 選擇翻譯模式

BigQuery Migration API 支援兩種翻譯模式。這兩種模式使用相同的 API 方法，並以非同步工作的形式執行。這些模式的差異在於提供來源 SQL 和接收翻譯 SQL 的方式：

* **批次翻譯**：API 會從 Cloud Storage 讀取來源檔案，並將翻譯後的檔案和報告寫入 Cloud Storage。如要一次翻譯多個檔案 (例如遷移整個程式碼集)，請使用批次翻譯。
* **互動式翻譯**：在要求主體中以字串常值形式傳遞 SQL，並從工作流程回應中讀取翻譯後的 SQL。您不必將 SQL 或翻譯輸出內容儲存在 Cloud Storage。使用互動式翻譯，視需要翻譯個別查詢，例如翻譯應用程式或開發人員工具的查詢。

### 啟用翻譯

啟用必要的 BigQuery Migration API。詳情請參閱「[啟用 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#enable-api)」。

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

### 將輸入檔案上傳至 Cloud Storage

如要執行批次翻譯工作，您必須將包含待翻譯查詢和指令碼的來源檔案上傳至 Cloud Storage。您也可以將[任何中繼資料檔案](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)或[設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw)上傳到含有來源檔案的同一個 Cloud Storage bucket。

如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

### 不支援的 SQL 函式

如果來源查詢參照的 SQL 函式在 GoogleSQL 中沒有直接對應項目，您可以使用輔助 user-defined function (UDF)。詳情請參閱「[使用輔助 UDF 處理不支援的 SQL 函式](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw#handling_unsupported_sql_functions_with_helper_udfs)」。

## 提交翻譯工作

如要使用 BigQuery Migration API 提交翻譯工作，請使用 [`projects.locations.workflows.create`](https://docs.cloud.google.com/bigquery/docs/reference/migration/rest/v2/projects.locations.workflows/create?hl=zh-tw) 方法，並提供 [`MigrationWorkflow`](https://docs.cloud.google.com/bigquery/docs/reference/migration/rest/v2/projects.locations.workflows?hl=zh-tw#resource:-migrationworkflow) 資源的執行個體，以及[支援的工作類型](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#supported_sql_dialects)。

提交工作後，您可以[輪詢工作狀態](#check_job_status)。

### 建立批次翻譯

下列 `curl` 指令會建立批次翻譯工作，並將輸入和輸出檔案儲存在 Cloud Storage。`source_target_mapping` 欄位包含一份清單，可將來源目錄對應至目標輸出的選用相對路徑。

```
curl -d "{
  \"tasks\": {
      string: {
        \"type\": \"TYPE\",
        \"translation_details\": {
            \"target_base_uri\": \"TARGET_BASE\",
            \"source_target_mapping\": {
              \"source_spec\": {
                  \"base_uri\": \"BASE\"
              }
            },
            \"target_types\": \"TARGET_TYPES\",
        }
      }
  }
  }" \
  -H "Content-Type:application/json" \
  -H "Authorization: Bearer TOKEN" -X POST https://bigquerymigration.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/workflows
```

更改下列內容：

* `TYPE`：翻譯的[工作類型](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#supported_sql_dialects)，決定原文和譯文的方言。
* `TARGET_BASE`：所有翻譯輸出的基本 URI。
* `BASE`：所有檔案的基本 URI，這些檔案會做為翻譯來源讀取。
* `TARGET_TYPES` (選用)：生成的輸出類型。如未指定，系統會生成 SQL。

  + `sql` (預設)：翻譯後的 SQL 查詢檔案。
  + `suggestion`：AI 生成的建議。

  輸出內容會儲存在輸出目錄的子資料夾中。子資料夾的名稱會根據 `TARGET_TYPES` 中的值命名。
* `TOKEN`：驗證權杖。如要產生權杖，請使用 `gcloud auth print-access-token` 指令或 [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/?hl=zh-tw) (使用範圍 `https://www.googleapis.com/auth/cloud-platform`)。
* `PROJECT_ID`：處理翻譯的專案。
* `LOCATION`：處理工作的[位置](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#locations)。

上述指令會傳回回應，其中包含格式為 `projects/PROJECT_ID/locations/LOCATION/workflows/WORKFLOW_ID` 的工作流程 ID。

#### 批次翻譯範例

如要翻譯 Cloud Storage 目錄 `gs://my_data_bucket/teradata/input/` 中的 Teradata SQL 指令碼，並將結果儲存在 Cloud Storage 目錄 `gs://my_data_bucket/teradata/output/` 中，您可以使用下列查詢：

```
{
  "tasks": {
     "task_name": {
       "type": "Teradata2BigQuery_Translation",
       "translation_details": {
         "target_base_uri": "gs://my_data_bucket/teradata/output/",
           "source_target_mapping": {
             "source_spec": {
               "base_uri": "gs://my_data_bucket/teradata/input/"
             }
          },
       }
    }
  }
}
```

**注意：** 本例中的字串 `"task_name"` 是翻譯工作的 ID，可設為任何值。

這項呼叫會傳回一則訊息，其中 `"name"` 欄位包含建立的工作流程 ID：

```
{
  "name": "projects/123456789/locations/us/workflows/12345678-9abc-def1-2345-6789abcdef00",
  "tasks": {
    "task_name": { /*...*/ }
  },
  "state": "RUNNING"
}
```

如要取得工作流程的最新狀態，請[執行 `GET` 查詢](#check_job_status)。工作會隨著進度將輸出內容傳送至 Cloud Storage。所有要求的`target_types`產生後，工作`state`會變更為`COMPLETED`。如果工作成功，您可以在 `gs://my_data_bucket/teradata/output` 中找到翻譯後的 SQL 查詢。

#### 使用 AI 建議進行批次翻譯的範例

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** Translation API 可透過 BigQuery Agent Platform 整合功能呼叫 Gemini，根據 AI 設定 YAML 檔案，為翻譯後的 SQL 查詢生成建議。

以下範例會翻譯位於 `gs://my_data_bucket/teradata/input/` Cloud Storage 目錄中的 Teradata SQL 指令碼，並將結果儲存在 Cloud Storage 目錄 `gs://my_data_bucket/teradata/output/`，同時提供額外的 AI 建議：

```
{
  "tasks": {
     "task_name": {
       "type": "Teradata2BigQuery_Translation",
       "translation_details": {
         "target_base_uri": "gs://my_data_bucket/teradata/output/",
           "source_target_mapping": {
             "source_spec": {
               "base_uri": "gs://my_data_bucket/teradata/input/"
             }
          },
          "target_types": "suggestion",
       }
    }
  }
}
```

**注意：** 如要生成生成式 AI 建議，Cloud Storage 來源目錄必須包含至少一個後置字串為 `.ai_config.yaml` 的設定 YAML 檔案。如要瞭解如何編寫 AI 建議的設定 YAML 檔案，請參閱「[建立以 Gemini 為基礎的設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#ai_yaml_guidelines)」。

工作順利執行後，您可以在 `gs://my_data_bucket/teradata/output/suggestion` Cloud Storage 目錄中找到 AI 建議。

### 建立互動式翻譯

下列 `curl` 指令會建立互動式翻譯工作，並以字串文字輸入和輸出。`source_target_mapping` 欄位包含一份清單，可將來源 `literal` 項目對應至目標輸出的選用相對路徑。

```
curl -d "{
  \"tasks\": {
      string: {
        \"type\": \"TYPE\",
        \"translation_details\": {
        \"source_target_mapping\": {
            \"source_spec\": {
              \"literal\": {
              \"relative_path\": \"PATH\",
              \"literal_string\": \"STRING\"
              }
            }
        },
        \"target_return_literals\": \"TARGETS\",
        }
      }
  }
  }" \
  -H "Content-Type:application/json" \
  -H "Authorization: Bearer TOKEN" -X POST https://bigquerymigration.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/workflows
```

更改下列內容：

* `TYPE`：翻譯的[工作類型](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#supported_sql_dialects)，決定原文和譯文的方言。
* `PATH`：常值項目的 ID，類似於檔案名稱或路徑。
* `STRING`：要翻譯的常值輸入資料字串 (例如 SQL)。
* `TARGETS`：使用者希望直接在回應中傳回的預期目標，格式為 `literal`。這些項目應採用目標 URI 格式 (例如 GENERATED\_DIR + `target_spec.relative_path` + `source_spec.literal.relative_path`)。不在這份清單中的項目不會在回應中傳回。一般 SQL 翻譯產生的目錄 GENERATED\_DIR 為 `sql/`。
* `TOKEN`：驗證權杖。如要產生權杖，請使用 `gcloud auth print-access-token` 指令或 [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/?hl=zh-tw) (使用範圍 `https://www.googleapis.com/auth/cloud-platform`)。
* `PROJECT_ID`：處理翻譯的專案。
* `LOCATION`：處理工作的[位置](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#locations)。

上述指令會傳回回應，其中包含格式為 `projects/PROJECT_ID/locations/LOCATION/workflows/WORKFLOW_ID` 的工作流程 ID。

建立工作流程後，請[查看工作狀態](#check_job_status)來檢視結果。

#### 互動式翻譯範例

如要以互動方式翻譯 Apache Hive SQL 字串 `select 1`，可以使用下列查詢：

```
"tasks": {
  string: {
    "type": "HiveQL2BigQuery_Translation",
    "translation_details": {
      "source_target_mapping": {
        "source_spec": {
          "literal": {
            "relative_path": "input_file",
            "literal_string": "select 1"
          }
        }
      },
      "target_return_literals": "sql/input_file",
    }
  }
}
```

**注意：** 本例中的字串 `"task_name"` 是翻譯工作的 ID，可設為任何值。

您可以在常值中使用任何 `relative_path`，但只有在 `target_return_literals` 中加入 `sql/$relative_path`，翻譯後的常值才會顯示在結果中。您也可以在單一查詢中加入多個常值，在這種情況下，每個常值的相對路徑都必須包含在 `target_return_literals` 中。

這項呼叫會傳回一則訊息，其中 `"name"` 欄位包含建立的工作流程 ID：

```
{
  "name": "projects/123456789/locations/us/workflows/12345678-9abc-def1-2345-6789abcdef00",
  "tasks": {
    "task_name": { /*...*/ }
  },
  "state": "RUNNING"
}
```

如要取得工作流程的最新狀態，請[查看工作狀態](#check_job_status)。當 `"state"` 變更為 `COMPLETED` 時，工作即完成。如果工作成功，您會在回應訊息中看到翻譯後的 SQL：

```
{
  "name": "projects/123456789/locations/us/workflows/12345678-9abc-def1-2345-6789abcdef00",
  "tasks": {
    "string": {
      "id": "0fedba98-7654-3210-1234-56789abcdef",
      "type": "HiveQL2BigQuery_Translation",
      /* ... */
      "taskResult": {
        "translationTaskResult": {
          "translatedLiterals": [
            {
              "relativePath": "sql/input_file",
              "literalString": "-- Translation time: 2023-10-05T21:50:49.885839Z\n-- Translation job ID: projects/123456789/locations/us/workflows/12345678-9abc-def1-2345-6789abcdef00\n-- Source: input_file\n-- Translated from: Hive\n-- Translated to: BigQuery\n\nSELECT\n    1\n;\n"
            }
          ],
          "reportLogMessages": [
            ...
          ]
        }
      },
      /* ... */
    }
  },
  "state": "COMPLETED",
  "createTime": "2023-10-05T21:50:49.543221Z",
  "lastUpdateTime": "2023-10-05T21:50:50.462758Z"
}
```

## 檢查工作狀態

翻譯工作會以非同步方式執行。提交工作流程後，請傳送包含工作流程 ID 的 `GET` 要求，擷取工作流程狀態：

```
curl \
  -H "Content-Type:application/json" \
  -H "Authorization:Bearer TOKEN" \
  -X GET https://bigquerymigration.googleapis.com/v2/projects/PROJECT_ID/locations/LOCATION/workflows/WORKFLOW_ID
```

更改下列內容：

* `TOKEN`：驗證權杖。如要產生權杖，請使用 `gcloud auth print-access-token` 指令或 [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/?hl=zh-tw) (使用範圍 `https://www.googleapis.com/auth/cloud-platform`)。
* `PROJECT_ID`：執行翻譯工作的專案。
* `LOCATION`：處理工作的[位置](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations?hl=zh-tw#locations)。
* `WORKFLOW_ID`：建立翻譯工作流程時傳回的工作流程 ID。

### 工作流程狀態

回應包含 `state` 欄位，指出工作流程的目前狀態：

* `STATE_UNSPECIFIED`：未指定工作流程狀態。
* `RUNNING`：工作流程正在執行中。定期輪詢端點，直到狀態變更為止。
* `PAUSED`：工作流程已暫停。
* `COMPLETED`：工作流程順利完成。現在可以擷取結果。
* `FAILED`：工作流程發生錯誤。檢查回應中的 `taskResult` 和 `reportLogMessages` 欄位，查看錯誤詳細資料。

當工作流程 `state` 達到 `COMPLETED` 或 `FAILED` 時，即可停止輪詢。

## 擷取結果

擷取結果的方式取決於您提交的是[批次翻譯還是互動式翻譯](#translation-modes)：

* **批次翻譯**：翻譯檔案、摘要報告和任何 AI 建議，都會寫入您在 `target_base_uri` 中指定的 Cloud Storage 目的地目錄。您可以使用 gcloud CLI 儲存空間指令、Cloud Storage 用戶端程式庫或 REST API，直接從 Cloud Storage 讀取這些檔案：

  ```
  gcloud storage cp --recursive TARGET_URI LOCAL_DIRECTORY
  ```

  更改下列內容：

  + `TARGET_URI`：目標基礎 URI，例如 `gs://my_data_bucket/teradata/output/`。
  + `LOCAL_DIRECTORY`：接收檔案的本機目錄。

  如要進一步瞭解目的地 bucket 中產生的檔案，請參閱「[探索翻譯輸出內容](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw#explore_the_translation_output)」。
* **互動式翻譯**：如果工作設定為字串常值輸入和 `target_return_literals`，翻譯後的查詢會直接在工作流程回應的 `translatedLiterals` 欄位中傳回：

  ```
  "taskResult": {
    "translationTaskResult": {
      "translatedLiterals": [
        {
          "relativePath": "sql/input_file",
          "literalString": "SELECT 1;\n"
        }
      ]
    }
  }
  ```

  擷取 `translatedLiterals` 中每個項目的 `literalString` 欄位，即可取得翻譯後的查詢。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]