Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 驗證 BigQuery 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本文說明如何以程式輔助方式向 BigQuery 進行驗證。向 BigQuery 進行驗證的方法，取決於您用來存取 API 的介面，以及執行程式碼的環境。

如需驗證 BigQuery 的簡短範例，請參閱「[開始使用驗證](https://docs.cloud.google.com/bigquery/docs/authentication/getting-started?hl=zh-tw)」。

如要進一步瞭解 Google Cloud 驗證，請參閱「[驗證方式](https://docs.cloud.google.com/docs/authentication?hl=zh-tw)」。

## API 存取權

BigQuery 支援透過程式輔助方式存取。您可以透過下列方式存取 API：

* [用戶端程式庫](#client-libraries)
* [Google Cloud CLI](#gcloud)
* [REST](#rest)

### 用戶端程式庫

[BigQuery API 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)提供高階語言支援，可透過程式輔助方式向 BigQuery 進行驗證。為驗證向 Google Cloud API 發出的呼叫，用戶端程式庫支援[應用程式預設憑證 (ADC)](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw)。程式庫會在定義的一組位置中尋找憑證，並使用這些憑證驗證向 API 發出的要求。有了 ADC，您可以在各種環境 (例如本機開發環境或正式環境)，為應用程式提供憑證，不用修改應用程式程式碼。

### Google Cloud CLI

使用 [gcloud CLI](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw) 存取 BigQuery 時，使用使用者帳戶[登入 gcloud CLI](https://docs.cloud.google.com/sdk/docs/authorizing?hl=zh-tw)，可提供 gcloud CLI 指令所使用的憑證。

如果組織的安全政策禁止使用者帳戶具備必要權限，可以採用[服務帳戶模擬](#sa-impersonation)。

詳情請參閱「[使用 gcloud CLI 進行驗證](https://docs.cloud.google.com/docs/authentication/gcloud?hl=zh-tw)」。如要進一步瞭解如何透過 gcloud CLI 使用 BigQuery，請參閱「[安裝 gcloud CLI](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw)」。

### REST

您可以使用 gcloud CLI 憑證或[應用程式預設憑證](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw)，向 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw) 進行驗證。如要進一步瞭解 REST 要求的驗證機制，請參閱「[使用 REST 進行驗證](https://docs.cloud.google.com/docs/authentication/rest?hl=zh-tw)」。如要瞭解憑證類型，請參閱「[gcloud CLI 憑證和 ADC 憑證](https://docs.cloud.google.com/docs/authentication/gcloud?hl=zh-tw#gcloud-credentials)」。

## 設定 BigQuery 的驗證機制

驗證機制的設定方式取決於執行程式碼的環境。

以下是最常用的驗證機制設定方式。如要瞭解更多驗證選項和相關資訊，請參閱「[驗證方式](https://docs.cloud.google.com/docs/authentication?hl=zh-tw)」。

### 適用於本機開發環境

您可以透過下列方式，為本機開發環境設定憑證：

* [用戶端程式庫或第三方工具的使用者憑證](#client-libs)
* [透過指令列發出 REST 要求的使用者憑證](#rest-requests)
* [服務帳戶模擬](#sa-impersonation)

#### 用戶端程式庫或第三方工具

在本機環境中設定[應用程式預設憑證 (ADC)](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw)：

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
   完成後，執行下列指令來[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) Google Cloud CLI：

   ```
   gcloud init
   ```

   若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
2. 如果您使用本機殼層，請為使用者帳戶建立本機驗證憑證：

   ```
   gcloud auth application-default login
   ```

   如果您使用 Cloud Shell，則不需要執行這項操作。

   如果系統傳回驗證錯誤，且您使用外部識別資訊提供者 (IdP)，請確認您已[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。

   登入畫面會隨即顯示。登入後，您的憑證會儲存在 [ADC 使用的本機憑證檔案](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw#personal)中。

如要進一步瞭解如何在本機環境中使用 ADC，請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

#### 透過指令列發出 REST 要求

透過指令列發出 REST 要求時，只要在用於傳送要求的指令中加入 [`gcloud auth print-access-token`](https://docs.cloud.google.com/sdk/gcloud/reference/auth/print-access-token?hl=zh-tw)，即可使用 gcloud CLI 憑證。

下列範例會列出指定專案的服務帳戶。您可以將相同模式用於任何 REST 要求。

使用任何要求資料之前，請先替換以下項目：

* PROJECT\_ID：您的 Google Cloud 專案 ID。

如要傳送要求，請展開以下其中一個選項：

#### curl (Linux、macOS 或 Cloud Shell)

執行下列指令：

```
curl -X GET \  
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \  
     "https://iam.googleapis.com/v1/projects/PROJECT_ID/serviceAccounts"
```

#### PowerShell (Windows)

執行下列指令：

```
$cred = gcloud auth print-access-token  
$headers = @{ "Authorization" = "Bearer $cred" }  
  
Invoke-WebRequest `  
    -Method GET `  
    -Headers $headers `  
    -Uri "https://iam.googleapis.com/v1/projects/PROJECT_ID/serviceAccounts" | Select-Object -Expand Content
```

如要進一步瞭解如何使用 REST 和 gRPC 進行驗證，請參閱「[使用 REST 進行驗證](https://docs.cloud.google.com/docs/authentication/rest?hl=zh-tw)」。如要瞭解本機 ADC 憑證與 gcloud CLI 憑證的差異，請參閱「[gcloud CLI 驗證設定和 ADC 設定](https://docs.cloud.google.com/docs/authentication/gcloud?hl=zh-tw#gcloud-credentials)」。

#### 服務帳戶模擬

在多數情況下，您可以使用使用者憑證，從本機開發環境進行驗證。如果無法這麼做，或者需要測試指派給服務帳戶的權限，可以使用服務帳戶模擬功能。您必須具備 `iam.serviceAccounts.getAccessToken` 權限，這項權限包含在[服務帳戶權杖建立者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountTokenCreator) (`roles/iam.serviceAccountTokenCreator`) 身分與存取權管理角色中。

您可以使用 [`gcloud config set` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/config?hl=zh-tw)，設定 gcloud CLI 來使用服務帳戶模擬功能：

```
gcloud config set auth/impersonate_service_account SERVICE_ACCT_EMAIL
```

對於特定語言，您可以使用服務帳戶模擬功能建立本機 ADC 檔案，供用戶端程式庫使用。這種做法僅適用於 Go、Java、Node.js 和 Python 用戶端程式庫，不適用於其他語言。如要使用服務帳戶模擬功能設定本機 ADC 檔案，請搭配 [`gcloud auth application-default login` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/auth/application-default/login?hl=zh-tw)使用 [`--impersonate-service-account` 旗標](https://docs.cloud.google.com/sdk/gcloud/reference?hl=zh-tw#--impersonate-service-account)：

```
gcloud auth application-default login --impersonate-service-account=SERVICE_ACCT_EMAIL
```

如要進一步瞭解服務帳戶模擬功能，請參閱「[使用服務帳戶模擬功能](https://docs.cloud.google.com/docs/authentication/use-service-account-impersonation?hl=zh-tw)」。

### 透過 Google Cloud

如要驗證在 Google Cloud上執行的工作負載，請使用附加至程式碼執行所在運算資源的服務帳戶憑證，例如 [Compute Engine 虛擬機器 (VM) 執行個體](https://docs.cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances?hl=zh-tw#using)。對於在 Google Cloud 運算資源上執行的程式碼，我們建議採用這種驗證方式。

對於大多數服務，您必須在建立要執行程式碼的資源時附加服務帳戶，之後無法新增或替換服務帳戶。Compute Engine 是例外狀況，可讓您隨時將服務帳戶附加至 VM 執行個體。

請使用 gcloud CLI 建立服務帳戶，並附加至資源：

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
   完成後，執行下列指令來[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) Google Cloud CLI：

   ```
   gcloud init
   ```

   若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
2. 設定驗證方法：

   1. 確認您具備「建立服務帳戶」身分與存取權管理角色 (`roles/iam.serviceAccountCreator`) 和「專案 IAM 管理員」角色 (`roles/resourcemanager.projectIamAdmin`)。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   2. 建立服務帳戶：

      ```
      gcloud iam service-accounts create SERVICE_ACCOUNT_NAME
      ```

      將 `SERVICE_ACCOUNT_NAME` 換成服務帳戶的名稱。
   3. 如要授予服務帳戶專案和資源的存取權，請將角色授予該帳戶：

      ```
      gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com" --role=ROLE
      ```

      請替換下列項目：

      * `SERVICE_ACCOUNT_NAME`：服務帳戶名稱
      * `PROJECT_ID`：您建立服務帳戶的專案 ID
      * `ROLE`：要授予的角色
      **注意**：`--role` 旗標會影響服務帳戶在專案中可存取的資源。您之後可以撤銷這些角色或授予其他角色。
      在正式環境中，請勿授予「擁有者」、「編輯者」或「檢視者」角色。請改為授予符合需求的[預先定義角色](https://docs.cloud.google.com/iam/docs/understanding-roles?hl=zh-tw#predefined_roles)或[自訂角色](https://docs.cloud.google.com/iam/docs/understanding-custom-roles?hl=zh-tw)。
   4. 如要將其他角色授予服務帳戶，請執行上一個步驟中的指令。
   5. 將必要角色指派給要將服務帳戶附加至其他資源的主體。

      ```
      gcloud iam service-accounts add-iam-policy-binding SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com --member="user:USER_EMAIL" --role=roles/iam.serviceAccountUser
      ```

      更改下列內容：

      * `SERVICE_ACCOUNT_NAME`：服務帳戶名稱
      * `PROJECT_ID`：您建立服務帳戶的專案 ID
      * `USER_EMAIL`：Google 帳戶的電子郵件地址
3. 建立要執行程式碼的資源，並將服務帳戶附加至該資源。例如，如果您使用 Compute Engine：

   建立 Compute Engine 執行個體。請依照下列步驟來設定執行個體：
   * 將 `INSTANCE_NAME` 替換成您偏好的執行個體名稱。
   * 將 `--zone` 標記設定為您要在其中建立執行個體的[區域](https://docs.cloud.google.com/compute/docs/zones?hl=zh-tw#available)。
   * 將 `--service-account` 旗標設為您建立的服務帳戶電子郵件地址。

   ```
   gcloud compute instances create INSTANCE_NAME --zone=ZONE --service-account=SERVICE_ACCOUNT_EMAIL
   ```

如要進一步瞭解如何向 Google API 進行驗證，請參閱「[驗證方式](https://docs.cloud.google.com/docs/authentication?hl=zh-tw)」。

### 地端部署或其他雲端服務供應商

如要從 Google Cloud 外部設定驗證，建議使用 workload identity federation。詳情請參閱驗證說明文件中的「[為地端部署或其他雲端服務供應商設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-on-premises?hl=zh-tw)」。

## BigQuery 存取權控管

向 BigQuery 進行驗證後，您必須獲得授權才能存取 Google Cloud 資源。BigQuery 會使用 Identity and Access Management (IAM) 進行授權。

如要進一步瞭解 BigQuery 的角色，請參閱「[BigQuery 中的 IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。如要進一步瞭解 IAM 和授權，請參閱「[IAM 總覽](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw)」一文。

## 後續步驟

* [開始使用驗證功能](https://docs.cloud.google.com/bigquery/docs/authentication/getting-started?hl=zh-tw)。
* [透過使用者帳戶驗證已安裝的應用程式](https://docs.cloud.google.com/bigquery/docs/authentication/end-user-installed?hl=zh-tw)。
* [使用 JSON Web Token 進行驗證](https://docs.cloud.google.com/bigquery/docs/json-web-tokens?hl=zh-tw)。
* 瞭解[Google Cloud 驗證方式](https://docs.cloud.google.com/docs/authentication?hl=zh-tw#auth-decision-tree)。
* 查看[驗證用途](https://docs.cloud.google.com/docs/authentication/use-cases?hl=zh-tw)清單。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]