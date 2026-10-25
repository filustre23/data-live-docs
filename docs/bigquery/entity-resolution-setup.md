Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 BigQuery 設定及使用實體解析

BigQuery 的[實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-intro?hl=zh-tw)功能可讓您比對、簡化及擴充資料集中的記錄，不必移動基礎資料。使用者可以將 BigQuery 資料集連結至 LiveRamp 或 TransUnion 等識別資訊提供者，並呼叫遠端函式，就地解析識別資訊。身為識別資訊提供者，您可以設定遠端函式端點，並在 Google Cloud Marketplace 發布實體解析服務。

## 為使用者設定實體解析

如要以使用者身分進行實體解析，請在 BigQuery 中準備輸入和輸出資料集，將資料集存取權授予識別資訊提供者，並叫用其比對服務。如要進一步瞭解架構，請參閱「[實體解析架構](https://docs.cloud.google.com/bigquery/docs/entity-resolution-intro?hl=zh-tw#architecture)」。

### 事前準備

1. 與識別資訊提供者聯絡。BigQuery 支援使用 [LiveRamp](mailto:LiveRampIdentitySupport@liveramp.com) 和 [TransUnion](mailto:PDLtucloudappsupport@transunion.com) 進行實體解析。
2. 向識別資訊提供者取得下列項目：
   * 服務帳戶憑證
   * 遠端函式簽章
3. 在 Google Cloud 專案中建立下列資料集：
   * 輸入資料集
   * 輸出資料集

### 必要的角色

為確保識別資訊提供者的服務帳戶具備必要權限，可讀取輸入資料集並寫入輸出資料集，請要求管理員將下列 IAM 角色授予識別資訊提供者的服務帳戶：

**重要事項：**您必須將這些角色授予識別資訊提供者的服務帳戶，*而非*您的使用者帳戶。如果未將角色授予正確的主體，可能會發生權限錯誤。

* 輸入資料集的 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 輸出資料集的 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

管理員或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，將必要權限授予識別資訊提供者的服務帳戶。

### 使用識別資訊提供者解析實體

建立資料集並授予必要角色後，即可設定資料表，並透過所選識別資訊提供者執行比對工作。下表摘要說明各個支援的識別資訊提供者，其整合方法和所需資料表：

| 識別資訊提供者 | 整合方法 | 資料集中的必要資料表 | 工作叫用 |
| --- | --- | --- | --- |
| **LiveRamp** | LiveRamp Embedded Identity | 含有 RampID 的輸入資料表、中繼資料表 | 傳送電子郵件給 LiveRamp 支援團隊 |
| **TransUnion** | 透過 BigQuery 外部連結使用 TruAudience 遠端函式 | 含有實體屬性的輸入資料表、中繼資料表、工作狀態資料表、比對輸出資料表 | 使用 `CALL` 的 SQL 預存程序呼叫 |

選取識別資訊提供者，查看特定設定和工作執行操作說明：

### LiveRamp

#### LiveRamp 必要條件

在 BigQuery 設定 LiveRamp 實體解析前，請先完成下列必要條件：

* 在 BigQuery 設定 LiveRamp Embedded Identity。詳情請參閱「[在 BigQuery 中啟用 LiveRamp Embedded Identity](https://docs.liveramp.com/identity/en/liveramp-embedded-identity-in-bigquery.html#enabling-liveramp-embedded-identity-in-bigquery)」。
* 與 LiveRamp 協調，啟用與 Embedded Identity 搭配使用的 API 憑證。詳情請參閱「[驗證](https://docs.liveramp.com/identity/en/liveramp-embedded-identity-in-bigquery.html#id74765)」。

#### 設定 LiveRamp 實體解析

首次使用 LiveRamp Embedded Identity 時，請完成下列設定步驟。後續執行時，您只需要更新輸入資料表和中繼資料表。

##### 建立 LiveRamp 輸入資料表

在輸入資料集中建立資料表，並填入下列資料欄：

* RampIDs
* 目標網域
* 目標類型

如要進一步瞭解輸入資料表結構定義，請參閱「[輸入資料表資料欄和說明](https://docs.liveramp.com/identity/en/perform-rampid-transcoding-in-bigquery.html#input-table-columns-and-descriptions)」。

##### 建立 LiveRamp 中繼資料表

如要控管 LiveRamp Embedded Identity 在 BigQuery 中的執行作業，請在輸入資料集中建立中繼資料表。在中繼資料表中填入下列設定欄：

* 用戶端 ID
* 執行模式
* 目標網域
* 目標類型

如要進一步瞭解中繼資料表格結構定義，請參閱「[中繼資料表格資料欄和說明](https://docs.liveramp.com/identity/en/perform-rampid-transcoding-in-bigquery.html#metadata-table-columns-and-descriptions)」。

#### 授予 LiveRamp 資料集存取權

建立必要資料表後，請授予 LiveRamp 存取權，以便查看及處理輸入資料集中的資料。將資料集存取權授予 LiveRampGoogle Cloud 服務帳戶。如要進一步瞭解如何共用資料集，請參閱「[與 LiveRamp 共用資料表和資料集](https://docs.liveramp.com/identity/en/perform-rampid-transcoding-in-bigquery.html#share-tables-and-datasets-with-liveramp-71)」。

#### 執行 LiveRamp 實體解析工作

設定資料表並授予資料集存取權後，請在 BigQuery 中使用 LiveRamp 執行實體解析工作：

1. 在輸入表格中，確認網域的所有 RampID 都已列出。
2. 執行工作前，請確認中繼資料資料表設定正確無誤。
3. 如要提交工作處理要求，請傳送電子郵件至 [LiveRampIdentitySupport@liveramp.com](mailto:LiveRampIdentitySupport@liveramp.com)。請在要求中附上專案 ID、資料集 ID，以及輸入資料表、中繼資料表和輸出資料集的任何適用資料表 ID。

LiveRamp 通常會在三個工作天內，將比對結果傳送至輸出資料集。

#### 取得 LiveRamp 支援和帳單資訊

LiveRamp 負責管理 BigQuery Embedded Identity 的技術支援和計費事宜：

* **技術支援**：如需設定或執行工作的協助，請與 [LiveRamp Identity 支援團隊](mailto:LiveRampIdentitySupport@liveramp.com)聯絡。
* **計費**：[LiveRamp](https://cloud.google.com/find-a-partner/partner/liveramp?hl=zh-tw) 會直接向您收取實體解析費用。

### TransUnion

#### TransUnion 必要條件

在 BigQuery 設定 TransUnion 實體解析前，請先傳送電子郵件給 [TransUnion 雲端支援團隊](mailto:PDLtucloudappsupport@transunion.com)，簽署服務存取協議。請在要求中提供下列資訊：

* 您的 Google Cloud 專案 ID
* 輸入資料類型
* 預定用途
* 預估資料量

TransUnion 雲端支援團隊核准要求後，會為您的 Google Cloud 專案啟用服務，並提供導入指南，其中包含可用的輸出結構定義。

#### 設定 TransUnion 實體解析

首次在 BigQuery 中使用 TransUnion TruAudience Identity Resolution and Enrichment 服務時，請完成下列設定步驟。

##### 建立外部連線

如要將 Google Cloud 帳戶連結至 TransUnion Google Cloud 帳戶中託管的身分解析服務，請[建立 Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)。設定連線時，請選取「Vertex AI 遠端模型、遠端函式、BigLake 和 Spanner (Cloud Resource)」做為連線類型。

建立連線後，請複製連線 ID 和服務帳戶 ID，然後將這些 ID 提供給 TransUnion 客戶交付團隊。

##### 建立遠端函式

如要將結構定義對應和設定中繼資料傳遞至 TransUnion 服務自動調度管理工具端點，請[建立遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#create_a_remote_function)。建立遠端函式時，請指定外部連線的連線 ID，以及 TransUnion 客戶交付團隊提供的 Cloud Run 函式端點網址。

##### 建立 TransUnion 輸入資料表

在輸入資料集中建立輸入資料表。TransUnion 支援下列實體屬性做為輸入欄：

* 名稱
* 郵遞地址
* 電子郵件地址
* 電話號碼
* 出生日期
* IPv4 位址
* 裝置 ID

請按照 TransUnion 提供的導入指南，遵循結構定義和格式規範。如果將每個輸入資料表對應至中繼資料表中的不同 `config_id` 參數，則可使用多個輸入資料表。

##### 建立 TransUnion 中繼資料表

如要儲存身分辨識服務所需的結構定義對應和設定，請在輸入資料集中建立中繼資料表。如要進一步瞭解中繼資料結構定義，請參閱 TransUnion 提供的導入指南。

##### 建立工作狀態資料表

如要接收批次處理更新，請在資料集中建立工作狀態資料表。如要監控工作並觸發管道中的下游程序，請查詢這份工作狀態資料表。表格會記錄下列狀態：

* `RUNNING`：身分解析服務正在處理批次。
* `COMPLETED`：服務已完成批次處理，並將結果寫入輸出資料表。
* `ERROR`：服務在處理批次時發生錯誤。

##### 建立服務叫用程序

`TransUnion_get_identities` 預存程序會封裝設定中繼資料，並叫用 TransUnion Cloud Run 函式端點。如要建立這個預存程序，請執行下列 SQL 陳述式：

```
-- create service invocation procedure
CREATE OR REPLACE PROCEDURE
  `PROJECT_ID.DATASET_ID.TransUnion_get_identities`(metadata_table STRING, config_id STRING)
BEGIN
  DECLARE sql_query STRING;
  DECLARE json_result STRING;
  DECLARE base64_result STRING;

  SET sql_query =
    '''SELECT TO_JSON_STRING(ARRAY_AGG(STRUCT(config_id, key, value))) FROM `''' || metadata_table
    || '''` WHERE config_id="''' || config_id || '''" ''';

  EXECUTE IMMEDIATE sql_query INTO json_result;

  SET base64_result = (SELECT TO_BASE64(CAST(json_result AS BYTES)));

  SELECT
    `PROJECT_ID.DATASET_ID.remote_call_TransUnion_er`(
      base64_result);
END;
```

更改下列內容：

* `PROJECT_ID`：您的 Google Cloud 專案 ID。
* `DATASET_ID`：您建立程序和遠端函式的資料集 ID。

##### 建立相符的輸出資料表

比對輸出表格會儲存 TransUnion 的實體解析結果，包括比對標記、連結分數、永久個人 ID 和家庭 ID。如要建立相符的輸出資料表，請執行下列 SQL 陳述式：

```
-- create output table
CREATE TABLE `PROJECT_ID.DATASET_ID.TransUnion_identity_output`(
  batchid STRING,
  uniqueid STRING,
  ekey STRING,
  hhid STRING,
  collaborationid STRING,
  firstnamematch STRING,
  lastnamematch STRING,
  addressmatches STRING,
  addresslinkagescores STRING,
  phonematches STRING,
  phonelinkagescores STRING,
  emailmatches STRING,
  emaillinkagescores STRING,
  dobmatches STRING,
  doblinkagescore STRING,
  ipmatches STRING,
  iplinkagescore STRING,
  devicematches STRING,
  devicelinkagescore STRING,
  lastprocessed STRING);
```

更改下列內容：

* `PROJECT_ID`：您的 Google Cloud 專案 ID。
* `DATASET_ID`：建立比對輸出資料表的資料集 ID。

##### 設定結構定義對應中繼資料

如要將輸入結構定義對應至 TransUnion 應用程式結構定義，請按照 TransUnion 提供的導入指南操作。這項中繼資料也會設定服務產生協作 ID 的方式，這些 ID 是可共用的非永久 ID，可用於[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)。

#### 將資料集存取權授予 TransUnion

建立必要的資料表和預存程序後，請授予 TransUnion 讀取輸入資料和寫入比對結果的權限。向 TransUnion 客戶交付團隊取得 Apache Spark 連線服務帳戶 ID。接著，在包含輸入和輸出資料表的資料集，將 BigQuery 資料編輯者角色 (`roles/bigquery.dataEditor`) 授予該服務帳戶。

#### 執行 TransUnion 實體解析工作

設定資料表並授予資料集存取權後，即可開始執行實體解析批次作業。如要叫用實體解析服務，請呼叫 `TransUnion_get_identities` 預存程序：

```
CALL `PROJECT_ID.DATASET_ID.TransUnion_get_identities`(
  "PROJECT_ID.DATASET_ID.TransUnion_er_metadata",
  "CONFIG_ID");
```

更改下列內容：

* `PROJECT_ID`：您的 Google Cloud 專案 ID。
* `DATASET_ID`：資料集 ID，其中包含中繼資料資料表和預存程序。
* `CONFIG_ID`：批次執行的設定 ID，例如 `"1"`。

#### 取得 TransUnion 支援和帳單資訊

如需 TruAudience Identity Resolution and Enrichment in BigQuery 的技術問題或帳單諮詢方面的協助，請直接與 TransUnion 聯絡：

* **技術支援**：如需設定、結構定義對應或疑難排解方面的協助，請與 [TransUnion Cloud 支援團隊](mailto:PDLtucloudappsupport@transunion.com)聯絡。
* **帳單**：TransUnion 會追蹤服務用量，以便計算費用。如要瞭解帳戶和定價詳情，請洽詢 TransUnion 傳送代表。

## 為識別資訊提供者設定實體解析

身為識別資訊提供者，您可以向 BigQuery 使用者提供實體解析服務。這種架構可保護您的智慧財產，因為您不會公開專屬的身分圖或比對邏輯。

如要設定服務，請部署自動調度管理工具端點、建立 BigQuery 遠端函式、授予必要角色，並與使用者共用遠端函式簽章。如要進一步瞭解架構，請參閱「[實體解析架構](https://docs.cloud.google.com/bigquery/docs/entity-resolution-intro?hl=zh-tw#architecture)」。

### 事前準備

在 BigQuery 中設定實體解析服務之前，請確認您具備下列條件：

* 部署在Google Cloud 專案或外部資料庫中的身分圖譜資料集和比對邏輯。
* 從使用者取得的使用者主體 ID，例如使用者、服務帳戶或 Google 群組電子郵件地址。

### 必要的角色

為確保識別資訊提供者的服務帳戶具備必要權限，可執行實體解析工作，請要求管理員將下列 IAM 角色授予識別資訊提供者的服務帳戶：

**重要事項：**您必須將這些角色授予識別資訊提供者的服務帳戶，*而非*您的使用者帳戶。如果未將角色授予正確的主體，可能會發生權限錯誤。

* 如要讓與函式相關聯的服務帳戶讀取及寫入相關聯的資料集，並啟動工作，請按照下列步驟操作：
  + 專案的 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
  + 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 如要讓使用者主體查看及連線至遠端函式：
  + 連線的 [BigQuery 連線使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionUser)  (`roles/bigquery.connectionUser`)
  + 具備遠端函式的控制層資料集 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

管理員或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，將必要權限授予識別資訊提供者的服務帳戶。

### 設定遠端函式端點

如要處理使用者的實體解析要求，請部署自動調度管理工具端點，並連結至 BigQuery 遠端函式：

1. 如要處理遠端函式傳來的比對成功的請求，請建立 [Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run?hl=zh-tw) 工作或 [Cloud Run 函式](https://docs.cloud.google.com/functions/docs/concepts/overview?hl=zh-tw)。您可以為端點選擇任一選項。
2. 如要找出與 Cloud Run 工作或 Cloud Run 函式相關聯的服務帳戶電子郵件地址，請完成下列步驟：

   1. 前往 Google Cloud 控制台的「Cloud Run」頁面。

      [前往 Cloud Run](https://console.cloud.google.com/run?hl=zh-tw)。
   2. 按一下函式或工作的名稱，然後點選「Security」(安全性) 分頁標籤。
   3. 在「Service account」(服務帳戶) 欄位中，找出並記錄遠端函式的服務帳戶電子郵件地址。
3. 在控制層資料集中，[建立遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#create_a_remote_function)，連線至 Cloud Run 工作或 Cloud Run 函式端點。

### 共用實體解析遠端函式

建立遠端函式並將必要角色授予使用者後，請與他們共用下列遠端函式簽章。使用者呼叫這個遠端函式，即可啟動實體解析工作。

```
`PARTNER_PROJECT_ID.DATASET_ID.match`(LIST_OF_PARAMETERS)
```

更改下列內容：

* `PARTNER_PROJECT_ID`：識別資訊提供者的 Google Cloud 專案 ID。
* `DATASET_ID`：包含遠端函式的資料集 ID。
* `LIST_OF_PARAMETERS`：要傳遞至遠端函式的參數清單。

### 選用：提供實體解析工作中繼資料

如要向使用者提供工作中繼資料，您可以公開獨立的遠端函式，或將工作狀態資料表寫入使用者的輸出資料集。舉例來說，您可以回報 `RUNNING`、`COMPLETED` 或 `ERROR` 等執行狀態，以及處理指標。

### 與 Cloud Marketplace 整合以進行計費

如要透過 Google 管理客戶帳單和新手上路流程，請將實體解析服務與 [Cloud Marketplace](https://cloud.google.com/marketplace?hl=zh-tw) 整合。這項整合功能可讓您根據實體解析工作用量設定[定價模式](https://docs.cloud.google.com/marketplace/docs/partners/integrated-saas/select-pricing?hl=zh-tw)，並由 Google 處理服務帳單。詳情請參閱「[提供軟體即服務 (SaaS) 產品](https://docs.cloud.google.com/marketplace/docs/partners/integrated-saas?hl=zh-tw)」。

## 後續步驟

* 瞭解 [BigQuery 共用中的實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-intro?hl=zh-tw)。
* 瞭解如何[建立遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#create_a_remote_function)。
* 瞭解如何[建立 Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)。
* 如果是識別資訊提供者，請參閱[這篇文章](https://docs.cloud.google.com/marketplace/docs/partners/integrated-saas?hl=zh-tw)，瞭解如何在 Google Cloud Marketplace 提供實體解析服務。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]