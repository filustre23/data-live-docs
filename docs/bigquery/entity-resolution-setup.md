Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 BigQuery 中設定及使用實體解析

本文說明如何為使用者和身分提供者實作[實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-intro?hl=zh-tw)。

您可以使用這份文件與識別資訊提供者建立連結，並使用他們的服務比對記錄。身分識別提供者可以參考這份文件，在 Google Cloud Marketplace 設定要與您共用的服務。

## 使用者工作流程

以下各節說明如何在 BigQuery 中設定實體解析。如要查看完整設定的視覺化呈現方式，請參閱[實體解析架構](https://docs.cloud.google.com/bigquery/docs/entity-resolution-intro?hl=zh-tw#architecture)。

### 事前準備

1. 與識別資訊提供者聯絡。BigQuery 支援使用 [LiveRamp](mailto:LiveRampIdentitySupport@liveramp.com) 和 [TransUnion](mailto:PDLtucloudappsupport@transunion.com) 進行實體解析。
2. 向識別資訊提供者索取下列項目：
   * 服務帳戶憑證
   * 遠端函式簽章
3. 在 Google Cloud 專案中建立兩個資料集：
   * 輸入資料集
   * 輸出資料集

### 必要的角色

如要取得執行實體解析作業所需的權限，請要求管理員授予您下列 IAM 角色：

* 如要讓身分識別提供者的服務帳戶讀取輸入資料集並寫入輸出資料集，請按照下列步驟操作：
  + 輸入資料集的 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
  + 輸出資料集的「BigQuery 資料編輯者」 (`roles/bigquery.dataEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

### 翻譯或解析實體

如需特定身分識別提供者的操作說明，請參閱以下各節。

### LiveRamp

#### 必要條件

* 在 BigQuery 中設定 LiveRamp 嵌入式 ID。詳情請參閱[在 BigQuery 中啟用 LiveRamp 內嵌式 ID](https://docs.liveramp.com/identity/en/liveramp-embedded-identity-in-bigquery.html#enabling-liveramp-embedded-identity-in-bigquery)。
* 與 LiveRamp 協調，啟用 API 憑證以搭配使用 Embedded Identity。詳情請參閱「[驗證](https://docs.liveramp.com/identity/en/liveramp-embedded-identity-in-bigquery.html#id74765)」。

#### 設定

首次使用 LiveRamp Embedded Identity 時，請務必執行下列步驟。設定完成後，您只需要在執行作業之間修改輸入表格和中繼資料表格。

##### 建立輸入資料表

在輸入資料集中建立資料表。在資料表中填入 RampID、目標網域和目標類型。如需詳細資料和範例，請參閱「[輸入資料表資料欄和說明](https://docs.liveramp.com/identity/en/perform-rampid-transcoding-in-bigquery.html#input-table-columns-and-descriptions)」。

##### 建立中繼資料表

中繼資料表可控管在 BigQuery 上執行的 LiveRamp Embedded Identity。在輸入資料集中建立中繼資料表。在「中繼資料」表格中填入用戶端 ID、執行模式、目標網域和目標類型。如需詳細資料和範例，請參閱「[中繼資料表資料欄和說明](https://docs.liveramp.com/identity/en/perform-rampid-transcoding-in-bigquery.html#metadata-table-columns-and-descriptions)」。

##### 與 LiveRamp 分享資料表

授予 LiveRamp Google Cloud 服務帳戶權限，以便查看及處理輸入資料集中的資料。如需詳細資訊和範例，請參閱「[與 LiveRamp 共用資料表和資料集](https://docs.liveramp.com/identity/en/perform-rampid-transcoding-in-bigquery.html#share-tables-and-datasets-with-liveramp-71)」。

#### 執行內嵌身分工作

如要在 BigQuery 中使用 LiveRamp 執行內嵌身分工作，請完成下列步驟：

1. 確認網域中編碼的所有 RampID 都位於輸入表格中。
2. 執行工作前，請確認中繼資料表是否仍正確無誤。
3. 請傳送電子郵件至 [LiveRampIdentitySupport@liveramp.com](mailto:LiveRampIdentitySupport@liveramp.com)，提出工作程序要求。請一併提供輸入資料表、中繼資料表和輸出資料集的專案 ID、資料集 ID 和資料表 ID (如適用)。

結果通常會在三個工作天內傳送到輸出資料集。

#### LiveRamp 支援

如有支援問題，請與 [LiveRamp Identity 支援團隊](mailto:LiveRampIdentitySupport@liveramp.com)聯絡。

#### LiveRamp 帳單

[LiveRamp](https://cloud.google.com/find-a-partner/partner/liveramp?hl=zh-tw) 會處理實體解析的帳單。

### TransUnion

#### 必要條件

* 如要簽署協議以存取這項服務，請與 [TransUnion Cloud 支援團隊](mailto:PDLtucloudappsupport@transunion.com)聯絡。提供 Google Cloud 專案 ID、輸入資料類型、用途和資料量。
* TransUnion Cloud Support 會為您的 Google Cloud 專案啟用這項服務，並提供詳細的導入指南，其中包含可用的輸出資料。

#### 設定

在 BigQuery 環境中使用 TransUnion 的 TruAudience Identity Resolution and Enrichment 服務時，必須完成下列步驟。

##### 建立外部連線

[建立外部資料來源的連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)，類型為「**Vertex AI 遠端模型、遠端函式和 BigLake (Cloud 資源)**」。您可以使用這個連線，從Google Cloud 帳戶觸發 TransUnion Google Cloud 帳戶中託管的身分解析服務。

複製連線 ID 和服務帳戶 ID，然後將這些 ID 提供給 TransUnion 客戶服務團隊。

##### 建立遠端函式

[建立遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#create_a_remote_function)，與 TransUnion Google Cloud 專案上代管的服務自動化調度管理端點互動，將必要的中繼資料 (包括結構定義對應) 傳遞至 TransUnion 服務。使用您建立的外部連線 ID，以及 TransUnion 客戶交付團隊提供的 TransUnion 代管 Cloud 函式端點。

##### 建立輸入資料表

在輸入資料集中建立資料表。TransUnion 支援姓名、郵寄地址、電子郵件、電話、出生日期、IPv4 位址和裝置 ID 做為輸入資料。請按照 TransUnion 提供給您的導入指南，設定格式。

##### 建立中繼資料表

建立中繼資料表，儲存身分識別解析服務處理資料所需的設定，包括結構定義對應。如需詳細資料和範例，請參閱 TransUnion 提供給您的實作指南。

##### 建立工作狀態表

建立資料表，接收有關輸入批次處理作業的最新資訊。您可以查詢這個資料表，觸發管道中的其他下游程序。可能的工作狀態包括 `RUNNING`、`COMPLETED` 或 `ERROR`。

##### 建立服務叫用

收集所有中繼資料、封裝資料，並傳遞至 TransUnion 代管的叫用 Cloud Functions 端點後，請按照下列程序呼叫 TransUnion 身分解析服務。

```
-- create service invocation procedure
CREATE OR REPLACE
  PROCEDURE
    `<project_id>.<dataset_id>.TransUnion_get_identities`(metadata_table STRING, config_id STRING)
      begin
        declare sql_query STRING;

declare json_result STRING;
declare base64_result STRING;

SET sql_query =
  '''select to_json_string(array_agg(struct(config_id,key,value))) from `''' || metadata_table
  || '''` where  config_id="''' || config_id || '''" ''';

EXECUTE immediate sql_query INTO json_result;

SET base64_result = (SELECT to_base64(CAST(json_result AS bytes)));

SELECT `<project_id>.<dataset_id>.remote_call_TransUnion_er`(base64_result);

END;
```

##### 建立相符的輸出資料表

執行下列 SQL 指令碼，建立相符的輸出資料表。這是應用程式的標準輸出內容，包括比對標記、分數、永久性個人 ID 和住家 ID。

```
-- create output table
CREATE TABLE `<project_id>.<dataset_id>.TransUnion_identity_output`(
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

##### 設定中繼資料

請按照 TransUnion 提供給您的導入指南，將輸入結構定義對應至應用程式結構定義。這項中繼資料也會設定協作 ID 的產生方式。協作 ID 是可共用的非持續性 ID，可用於資料無塵室。

#### 授予讀取和寫入權限

向 TransUnion 客戶交付團隊取得 Apache Spark 連線的服務帳戶 ID，並授予該帳戶輸入和輸出資料表所在資料集的讀取和寫入權限。建議您提供服務帳戶 ID，並在資料集上指派 [BigQuery 資料編輯者角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor)。

#### 叫用應用程式

您可以執行下列指令碼，從環境中叫用應用程式。

**注意：** 只要輸入資料表對應至不同的中繼資料設定，您就可以使用多個輸入資料表。

```
call `<project_id>.<dataset_id>.TransUnion_get_identities`("<project_id>.<dataset_id>.TransUnion_er_metadata","1");
-- using metadata table, and 1 = config_id for the batch run
```

#### 支援

如遇技術問題，請與 [TransUnion Cloud 支援團隊](mailto:PDLtucloudappsupport@transunion.com)聯絡。

#### 帳單與用量

TransUnion 會追蹤應用程式的使用情況，並用於結算。如要瞭解詳情，現有客戶可以與 TransUnion 交付代表聯絡。

## 識別資訊提供者工作流程

以下各節說明如何在 BigQuery 中設定實體解析。如要查看完整設定的視覺化呈現方式，請參閱[實體解析架構](https://docs.cloud.google.com/bigquery/docs/entity-resolution-intro?hl=zh-tw#architecture)。

### 事前準備

1. 建立 [Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run?hl=zh-tw) 工作或 [Cloud Run 函式](https://docs.cloud.google.com/functions/docs/concepts/overview?hl=zh-tw#functions)，與遠端函式整合。這兩種做法都適合用於此目的。
2. 取得與 Cloud Run 或 Cloud Run 函式相關聯的服務帳戶名稱：

   1. 前往 Google Cloud 控制台的「Cloud Functions」頁面。

      [前往 Cloud Functions 頁面](https://console.cloud.google.com/functions?hl=zh-tw)
   2. 按一下函式名稱，然後點選「詳細資料」分頁標籤。
   3. 在「General Information」(一般資訊) 窗格中，找出並記錄遠端函式的服務帳戶名稱。
3. 建立[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#create_a_remote_function)。
4. 向使用者取得使用者主體。

### 必要的角色

如要取得執行實體解析作業所需的權限，請要求管理員授予您下列 IAM 角色：

* 如要讓與函式相關聯的服務帳戶讀取及寫入相關聯的資料集，並啟動工作：
  + 專案的「BigQuery 資料編輯者」 (`roles/bigquery.dataEditor`)
  + 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 如要讓使用者主體查看及連線至遠端函式，請按照下列步驟操作：
  + [BigQuery 連線使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionUser)  (`roles/bigquery.connectionUser`)
    連線
  + [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
    在控制層資料集上使用遠端函式

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

### 共用實體解析遠端函式

修改下列遠端介面程式碼，並分享給使用者。使用者需要這個代碼才能啟動實體解析工作。

```
`PARTNER_PROJECT_ID.DATASET_ID`.match`(LIST_OF_PARAMETERS)
```

將 LIST\_OF\_PARAMETERS 替換為傳遞至遠端函式的參數清單。

### 選填：提供工作的中繼資料

您可以視需要使用個別的遠端函式提供工作的中繼資料，或在使用者輸出資料集中寫入新的狀態資料表。中繼資料的例子包括工作狀態和指標。

## 識別資訊提供者的計費方式

如要簡化客戶計費和新手上路流程，請將實體解析服務與 [Google Cloud Marketplace](https://docs.cloud.google.com/marketplace?hl=zh-tw) 整合。您可以根據實體解析作業用量設定[定價模式](https://docs.cloud.google.com/marketplace/docs/partners/integrated-saas/select-pricing?hl=zh-tw)，並由 Google 為您處理帳單事宜。詳情請參閱「[提供軟體即服務 (SaaS) 產品](https://docs.cloud.google.com/marketplace/docs/partners/integrated-saas?hl=zh-tw)」。

## 後續步驟

* 瞭解 [BigQuery sharing 中的實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-intro?hl=zh-tw)。
* 瞭解如何[建立遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#create_a_remote_function)。
* 瞭解如何[建立連至外部資料來源的連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)。
* 身分識別供應商請參閱[這篇文章](https://docs.cloud.google.com/marketplace/docs/partners/integrated-saas?hl=zh-tw)，瞭解如何透過 Google Cloud Marketplace 提供實體解析服務。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]