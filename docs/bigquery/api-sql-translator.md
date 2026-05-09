Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Translation API 翻譯 SQL 查詢

本文說明如何在 BigQuery 中使用翻譯 API，將以其他 SQL 方言編寫的指令碼翻譯成 GoogleSQL 查詢。翻譯 API 可簡化[將工作負載遷移至 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration-intro?hl=zh-tw) 的程序。

## 事前準備

提交翻譯工作前，請先完成下列步驟：

1. 確認您具備所有必要權限。
2. 啟用 BigQuery Migration API。
3. 收集包含待翻譯 SQL 指令碼和查詢的來源檔案。
4. 將來源檔案上傳至 Cloud Storage。

### 所需權限

如要取得使用 Translation API 建立翻譯工作所需的權限，請要求系統管理員授予 `parent` 資源的[MigrationWorkflow 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquerymigration?hl=zh-tw#bigquerymigration.editor)  (`roles/bigquerymigration.editor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備使用 Translation API 建立翻譯作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用 Translation API 建立翻譯工作，必須具備下列權限：

* `bigquerymigration.workflows.create`
* `bigquerymigration.workflows.get`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 啟用 BigQuery Migration API

如果您的 Google Cloud CLI 專案是在 2022 年 2 月 15 日前建立，請按照下列步驟啟用 BigQuery Migration API：

1. 前往 Google Cloud 控制台的「BigQuery Migration API」頁面。

   [前往 BigQuery Migration API](https://console.cloud.google.com/apis/api/bigquerymigration.googleapis.com/overview?hl=zh-tw)
2. 按一下「啟用」。

**注意：** 2022 年 2 月 15 日後建立的專案會自動啟用這項 API。

### 將輸入檔案上傳至 Cloud Storage

如要使用 Google Cloud 控制台或 BigQuery Migration API 執行翻譯工作，請將包含要翻譯的查詢和指令碼的來源檔案上傳至 Cloud Storage。您也可以將[任何中繼資料檔案](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)或[設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw)上傳至含有來源檔案的同一個 Cloud Storage 值區。如要進一步瞭解如何建立值區，以及將檔案上傳至 Cloud Storage，請參閱「[建立值區](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

## 支援的工作類型

翻譯 API 可將下列 SQL 方言翻譯為 GoogleSQL：

* Amazon Redshift SQL - `Redshift2BigQuery_Translation`
* Apache HiveQL 和 Beeline CLI - `HiveQL2BigQuery_Translation`
* Apache Impala - `Impala2BigQuery_Translation`
* Apache Spark SQL - `SparkSQL2BigQuery_Translation`
* Azure Synapse T-SQL - `AzureSynapse2BigQuery_Translation`
* GoogleSQL (BigQuery) - `Bigquery2Bigquery_Translation`
* Greenplum SQL - `Greenplum2BigQuery_Translation`
* IBM Db2 SQL - `Db22BigQuery_Translation`
* IBM Netezza SQL 和 NZPLSQL - `Netezza2BigQuery_Translation`
* MySQL SQL - `MySQL2BigQuery_Translation`
* Oracle SQL、PL/SQL、Exadata - `Oracle2BigQuery_Translation`
* PostgreSQL SQL - `Postgresql2BigQuery_Translation`
* Presto 或 Trino SQL - `Presto2BigQuery_Translation`
* Snowflake SQL - `Snowflake2BigQuery_Translation`
* SQLite - `SQLite2BigQuery_Translation`
* SQL Server T-SQL - `SQLServer2BigQuery_Translation`
* Teradata 和 Teradata Vantage - `Teradata2BigQuery_Translation`
* Vertica SQL - `Vertica2BigQuery_Translation`

### 使用輔助 UDF 處理不支援的 SQL 函式

將來源 SQL 語法翻譯為 BigQuery 時，部分函式可能沒有直接對應的函式。為解決這個問題，BigQuery 遷移服務 (和更廣泛的 BigQuery 社群) 提供輔助使用者定義函式 (UDF)，可複製這些不支援的來源方言函式行為。

這些 UDF 通常位於 `bqutil` 公開資料集中，因此翻譯後的查詢一開始可以採用 `bqutil.<dataset>.<function>()` 格式參照這些 UDF。例如：`bqutil.fn.cw_count()`。

#### 正式環境的重要注意事項：

雖然 `bqutil` 可方便存取這些輔助 UDF，進行初始轉譯和測試，但基於下列原因，不建議直接依賴 `bqutil` 處理正式版工作負載：

1. 版本管控：`bqutil` 專案會代管這些 UDF 的最新版本，因此定義可能會隨時間變更。如果 UDF 的邏輯更新，直接依賴 `bqutil` 可能會導致生產查詢發生非預期行為或重大變更。
2. 依附元件隔離：將 UDF 部署至自己的專案，可避免外部變更影響正式環境。
3. 自訂：您可能需要修改或最佳化這些 UDF，進一步符合特定商業邏輯或效能需求。只有在這些資源位於您的專案中時，才能執行這項操作。
4. 安全性和治理：貴機構的安全政策可能會限制直接存取 `bqutil` 等公開資料集，以處理正式環境資料。將 UDF 複製到受控環境，符合這類政策規定。

#### 將輔助 UDF 部署至專案：

如要穩定可靠地在實際工作環境中使用，請將這些輔助 UDF 部署到自己的專案和資料集。您可以全面掌控這些應用程式的版本、自訂項目和存取權。
如需部署這些 UDF 的詳細操作說明，請參閱 [GitHub 上的 UDF 部署指南](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/udfs#deploying-the-udfs)。本指南提供必要的指令碼和步驟，協助您將 UDF 複製到環境中。

## 位置

翻譯 API 適用於下列處理位置：

|  | **地區說明** | **區域名稱** | **詳細資料** |
| --- | --- | --- | --- |
| **亞太地區** | | | |
|  | 曼谷 | `asia-southeast3` |  |
|  | 德里 | `asia-south2` |  |
|  | 香港 | `asia-east2` |  |
|  | 雅加達 | `asia-southeast2` |  |
|  | 墨爾本 | `australia-southeast2` |  |
|  | 孟買 | `asia-south1` |  |
|  | 大阪 | `asia-northeast2` |  |
|  | 首爾 | `asia-northeast3` |  |
|  | 新加坡 | `asia-southeast1` |  |
|  | 雪梨 | `australia-southeast1` |  |
|  | 台灣 | `asia-east1` |  |
|  | 東京 | `asia-northeast1` |  |
| **歐洲** | | | |
|  | 比利時 | `europe-west1` |  |
|  | 柏林 | `europe-west10` |  |
|  | 歐洲 (多區域) | `eu` |
|  | 芬蘭 | `europe-north1` |  |
|  | 法蘭克福 | `europe-west3` |  |
|  | 倫敦 | `europe-west2` |  |
|  | 馬德里 | `europe-southwest1` |  |
|  | 米蘭 | `europe-west8` |  |
|  | 荷蘭 | `europe-west4` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 巴黎 | `europe-west9` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 斯德哥爾摩 | `europe-north2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 杜林 | `europe-west12` |  |
|  | 華沙 | `europe-central2` |  |
|  | 蘇黎世 | `europe-west6` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
| **美洲** | | | |
|  | 俄亥俄州哥倫布 | `us-east5` |  |
|  | 達拉斯 | `us-south1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 愛荷華州 | `us-central1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 拉斯維加斯 | `us-west4` |  |
|  | 洛杉磯 | `us-west2` |  |
|  | 墨西哥 | `northamerica-south1` |  |
|  | 北維吉尼亞州 | `us-east4` |  |
|  | 奧勒岡州 | `us-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 魁北克 | `northamerica-northeast1` | [低 CO2](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) 區域 |
|  | 聖保羅 | `southamerica-east1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 鹽湖城 | `us-west3` |  |
|  | 聖地亞哥 | `southamerica-west1` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 南卡羅來納州 | `us-east1` |  |
|  | 多倫多 | `northamerica-northeast2` | [低二氧化碳排放](https://cloud.google.com/sustainability/region-carbon?hl=zh-tw#region-picker) |
|  | 美國 (多區域) | `us` |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` |  |
| **MiddleEast** | | | |
|  | 達曼 | `me-central2` |  |
|  | 杜哈 | `me-central1` |  |
|  | 以色列 | `me-west1` |  |

## 提交翻譯工作

如要使用 Translation API 提交翻譯工作，請使用 [`projects.locations.workflows.create`](https://docs.cloud.google.com/bigquery/docs/reference/migration/rest/v2/projects.locations.workflows/create?hl=zh-tw) 方法，並提供 [`MigrationWorkflow`](https://docs.cloud.google.com/bigquery/docs/reference/migration/rest/v2/projects.locations.workflows?hl=zh-tw#resource:-migrationworkflow) 資源的執行個體，以及[支援的工作類型](#supported_task_types)。

提交工作後，即可[發出查詢來取得結果](#explore_the_translation_output)。

### 建立批次翻譯

下列 `curl` 指令會建立批次翻譯工作，輸入和輸出檔案都儲存在 Cloud Storage 中。`source_target_mapping` 欄位包含一份清單，可將來源 `literal` 項目對應至目標輸出內容的選用相對路徑。

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
  -H "Authorization: Bearer TOKEN" -X POST https://bigquerymigration.googleapis.com/v2alpha/projects/PROJECT_ID/locations/LOCATION/workflows
```

更改下列內容：

* `TYPE`：翻譯的[工作類型](#supported_task_types)，決定來源和目標方言。
* `TARGET_BASE`：所有翻譯輸出內容的基礎 URI。
* `BASE`：所有讀取為翻譯來源的檔案基礎 URI。
* `TARGET_TYPES` (選用)：產生的輸出類型。如未指定，系統會產生 SQL。

  + `sql` (預設)：翻譯後的 SQL 查詢檔案。
  + `suggestion`：AI 生成的建議。

  輸出內容會儲存在輸出目錄的子資料夾中。子資料夾會根據 `TARGET_TYPES` 中的值命名。
* `TOKEN`：用於驗證的權杖。如要產生權杖，請使用 `gcloud auth print-access-token` 指令或 [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/?hl=zh-tw) (使用 `https://www.googleapis.com/auth/cloud-platform` 範圍)。
* `PROJECT_ID`：用於處理翻譯作業的專案。
* `LOCATION`：處理作業的[位置](#locations)。

上述指令會傳回回應，其中包含以 `projects/PROJECT_ID/locations/LOCATION/workflows/WORKFLOW_ID` 格式編寫的工作流程 ID。

#### 批次翻譯範例

如要翻譯 Cloud Storage 目錄 `gs://my_data_bucket/teradata/input/` 中的 Teradata SQL 指令碼，並將結果儲存在 Cloud Storage 目錄 `gs://my_data_bucket/teradata/output/` 中，可以使用下列查詢：

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

**注意：** 本例中的 `"task_name"` 字串是翻譯工作的 ID，可設為任何值。

這項呼叫會傳回訊息，其中包含 `"name"` 欄位中建立的工作流程 ID：

```
{
  "name": "projects/123456789/locations/us/workflows/12345678-9abc-def1-2345-6789abcdef00",
  "tasks": {
    "task_name": { /*...*/ }
  },
  "state": "RUNNING"
}
```

如要取得工作流程的最新狀態，請[執行 `GET` 查詢](#explore_the_translation_output)。
工作會將輸出內容傳送至 Cloud Storage。所有要求的 `target_types` 生成完畢後，工作 `state` 會變更為 `COMPLETED`。如果工作成功，您可以在 `gs://my_data_bucket/teradata/output` 中找到翻譯後的 SQL 查詢。

#### 使用 AI 建議進行批次翻譯的範例

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 翻譯 API 可以透過 BigQuery Vertex AI 整合功能呼叫 Gemini，根據 AI 設定 YAML 檔案，為翻譯後的 SQL 查詢產生建議。

以下範例會翻譯 `gs://my_data_bucket/teradata/input/` Cloud Storage 目錄中的 Teradata SQL 指令碼，並將結果儲存在 `gs://my_data_bucket/teradata/output/` Cloud Storage 目錄中，同時提供額外的 AI 建議：

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

**注意：** 如要產生 AI 建議，Cloud Storage 來源目錄必須包含至少一個後置字元為 `.ai_config.yaml` 的設定 YAML 檔案。如要瞭解如何編寫 AI 建議的設定 YAML 檔案，請參閱[建立以 Gemini 為基礎的設定 YAML 檔案](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#ai_yaml_guidelines)。

工作順利執行後，您可以在 `gs://my_data_bucket/teradata/output/suggestion` Cloud Storage 目錄中找到 AI 建議。

### 建立互動式翻譯工作，並使用字串常值輸入和輸出內容

下列 `curl` 指令會建立翻譯工作，並使用字串常值做為輸入和輸出。`source_target_mapping` 欄位包含一份清單，將來源目錄對應至目標輸出的選用相對路徑。

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
  -H "Authorization: Bearer TOKEN" -X POST https://bigquerymigration.googleapis.com/v2alpha/projects/PROJECT_ID/locations/LOCATION/workflows
```

更改下列內容：

* `TYPE`：翻譯的[工作類型](#supported_task_types)，決定來源和目標方言。
* `PATH`：常值項目的 ID，類似於檔案名稱或路徑。
* `STRING`：要翻譯的輸入資料字串 (例如 SQL)。
* `TARGETS`：使用者希望以 `literal` 格式直接在回應中傳回的預期目標。這些應採用目標 URI 格式 (例如 GENERATED\_DIR + `target_spec.relative_path` + `source_spec.literal.relative_path`)。如果不在這個清單中，就不會傳回回應。產生的目錄 (一般 SQL 翻譯) 為 GENERATED\_DIR`sql/`。
* `TOKEN`：用於驗證的權杖。如要產生權杖，請使用 `gcloud auth print-access-token` 指令或 [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/?hl=zh-tw) (使用 `https://www.googleapis.com/auth/cloud-platform` 範圍)。
* `PROJECT_ID`：用於處理翻譯作業的專案。
* `LOCATION`：處理作業的[位置](#locations)。

上述指令會傳回回應，其中包含以 `projects/PROJECT_ID/locations/LOCATION/workflows/WORKFLOW_ID` 格式編寫的工作流程 ID。

工作完成後，您可以[查詢工作](#explore_the_translation_output)，並在工作流程完成後檢查回應中的內嵌 `translation_literals` 欄位，即可查看結果。

#### 互動式翻譯範例

如要以互動方式翻譯 Hive SQL 字串 `select 1`，您可以使用下列查詢：

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

**注意：** 本例中的 `"task_name"` 字串是翻譯工作的 ID，可設為任何值。

您可以在字面值中使用任何 `relative_path`，但只有在 `target_return_literals` 中加入 `sql/$relative_path`，翻譯後的字面值才會顯示在結果中。您也可以在單一查詢中加入多個常值，但必須在 `target_return_literals` 中加入每個常值的相對路徑。

這項呼叫會傳回訊息，其中包含 `"name"` 欄位中建立的工作流程 ID：

```
{
  "name": "projects/123456789/locations/us/workflows/12345678-9abc-def1-2345-6789abcdef00",
  "tasks": {
    "task_name": { /*...*/ }
  },
  "state": "RUNNING"
}
```

如要取得工作流程的最新狀態，請[執行 `GET` 查詢](#explore_the_translation_output)。
當 `"state"` 變更為 `COMPLETED` 時，工作即完成。如果工作成功，您會在回應訊息中看到翻譯後的 SQL：

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

## 探索翻譯輸出內容

執行翻譯工作後，請使用下列指令指定翻譯工作流程 ID，以擷取結果：

```
curl \
-H "Content-Type:application/json" \
-H "Authorization:Bearer TOKEN" -X GET https://bigquerymigration.googleapis.com/v2alpha/projects/PROJECT_ID/locations/LOCATION/workflows/WORKFLOW_ID
```

更改下列內容：

* `TOKEN`：用於驗證的權杖。如要產生權杖，請使用 `gcloud auth print-access-token` 指令或 [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/?hl=zh-tw) (使用 `https://www.googleapis.com/auth/cloud-platform` 範圍)。
* `PROJECT_ID`：用於處理翻譯作業的專案。
* `LOCATION`：處理作業的[位置](#locations)。
* `WORKFLOW_ID`：建立翻譯工作流程時產生的 ID。

回應會包含遷移工作流程的狀態，以及 `target_return_literals` 中所有已完成的檔案。

回應會包含移轉工作流程的狀態，以及 `target_return_literals` 中所有已完成的檔案。您可以輪詢這個端點，檢查工作流程的狀態。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]