Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 JWT 進行驗證

BigQuery API 會接受 [JSON Web Token (JWT)](https://datatracker.ietf.org/doc/rfc7519/) 來驗證要求。

最佳做法是使用[應用程式預設憑證 (ADC) 驗證 BigQuery](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw)。如果您無法使用 ADC，且使用服務帳戶進行驗證，則可以改用[已簽署的 JWT](https://developers.google.com/identity/protocols/oauth2/service-account?hl=zh-tw#jwt-auth)。有了 JWT，您就能向 Google 授權伺服器發出網路要求，不必呼叫 API。

您可以透過下列方式使用 JWT 進行驗證：

* 如果是在 Google Cloud 控制台或使用 gcloud CLI 建立的服務帳戶金鑰，請[使用提供 JWT 簽署功能的用戶端程式庫](#client-libraries)。
* 如果是系統管理的服務帳戶，請[使用 REST API 或 gcloud CLI](#rest-gcloud)。

### 範圍和目標對象

盡可能使用服務帳戶的[範圍](https://developers.google.com/identity/protocols/oauth2/scopes?hl=zh-tw)。如果無法使用，您可以使用[目標對象聲明](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3)。針對 BigQuery API，請將目標對象值設為 `https://bigquery.googleapis.com/`。

### 使用用戶端程式庫建立 JWT

如果是在 Google Cloud 控制台或使用 gcloud CLI 建立的服務帳戶金鑰，請使用提供 JWT 簽署功能的用戶端程式庫。以下清單列出適合常見程式設計語言的選項：

* Go：[func JWTAccessTokenSourceFromJSON](https://pkg.go.dev/golang.org/x/oauth2/google#JWTAccessTokenSourceFromJSON)
* Java：[類別 ServiceAccountCredentials](https://docs.cloud.google.com/java/docs/reference/google-auth-library/latest/com.google.auth.oauth2.ServiceAccountCredentials?hl=zh-tw)
* Node.js：[類別 JWTAccess](https://docs.cloud.google.com/nodejs/docs/reference/google-auth-library/latest/google-auth-library/jwtaccess?hl=zh-tw)
* PHP：[ServiceAccountJwtAccessCredentials](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest?hl=zh-tw#authentication)
* Python：[google.auth.jwt 模組](https://googleapis.dev/python/google-auth/latest/reference/google.auth.jwt.html)
* Ruby：[類別：Google::Auth::ServiceAccountJwtHeaderCredentials](https://www.rubydoc.info/gems/googleauth/Google/Auth/ServiceAccountJwtHeaderCredentials)

#### Java 範例

以下範例使用 [Java 專用 BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)建立並簽署 JWT。在用戶端程式庫中，BigQuery API 的預設範圍設為 `https://www.googleapis.com/auth/bigquery`。

```
import com.google.auth.oauth2.ServiceAccountCredentials;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.common.collect.ImmutableList;

import java.io.FileInputStream;
import java.io.IOException;
import java.net.URI;

public class Example {
    public static void main(String... args) throws IOException {
        String projectId = "myproject";
        // Load JSON file that contains service account keys and create ServiceAccountCredentials object.
        String credentialsPath = "/path/to/key.json";
        ServiceAccountCredentials credentials = null;
        try (FileInputStream is = new FileInputStream(credentialsPath)) {
          credentials =  ServiceAccountCredentials.fromStream(is);
          // The default scope for BigQuery is used.
          // Alternatively, use `.setScopes()` to set custom scopes.
          credentials = credentials.toBuilder()
              .setUseJwtAccessWithScope(true)
              .build();
        }
        // Instantiate BigQuery client with the credentials object.
        BigQuery bigquery =
                BigQueryOptions.newBuilder().setCredentials(credentials).build().getService();
        // Use the client to list BigQuery datasets.
        System.out.println("Datasets:");
        bigquery
            .listDatasets(projectId)
            .iterateAll()
            .forEach(dataset -> System.out.printf("%s%n", dataset.getDatasetId().getDataset()));
    }
}
```

### 使用 REST 或 gcloud CLI 建立 JWT

對於系統管理的服務帳戶，您必須手動組合 JWT，然後使用 REST 方法 [`projects.serviceAccounts.signJwt`](https://docs.cloud.google.com/iam/docs/reference/credentials/rest/v1/projects.serviceAccounts/signJwt?hl=zh-tw) 或 Google Cloud CLI 指令 [`gcloud beta iam service-accounts sign-jwt`](https://cloud.google.com/sdk/gcloud/reference/beta/iam/service-accounts/sign-jwt?hl=zh-tw) 簽署 JWT。如要使用這兩種方法，您必須是「服務帳戶符記建立者」身分的 Cloud Identity and Access Management 角色成員。

#### gcloud CLI 範例

以下範例顯示 Bash 指令碼，該指令碼會組合 JWT，然後使用 `gcloud beta iam service-accounts sign-jwt` 指令簽署 JWT。

```
#!/bin/bash

SA_EMAIL_ADDRESS="myserviceaccount@myproject.iam.gserviceaccount.com"

TMP_DIR=$(mktemp -d /tmp/sa_signed_jwt.XXXXX)
trap "rm -rf ${TMP_DIR}" EXIT
JWT_FILE="${TMP_DIR}/jwt-claim-set.json"
SIGNED_JWT_FILE="${TMP_DIR}/output.jwt"

IAT=$(date '+%s')
EXP=$((IAT+3600))

cat <<EOF > $JWT_FILE
{
  "aud": "https://bigquery.googleapis.com/",
  "iat": $IAT,
  "exp": $EXP,
  "iss": "$SA_EMAIL_ADDRESS",
  "sub": "$SA_EMAIL_ADDRESS"
}
EOF

gcloud beta iam service-accounts sign-jwt --iam-account $SA_EMAIL_ADDRESS $JWT_FILE $SIGNED_JWT_FILE

echo "Datasets:"
curl -L -H "Authorization: Bearer $(cat $SIGNED_JWT_FILE)" \
-X GET \
"https://bigquery.googleapis.com/bigquery/v2/projects/myproject/datasets?alt=json"
```

## 後續步驟

* 進一步瞭解 [BigQuery 驗證](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw)。
* 瞭解如何[使用使用者憑證進行驗證](https://docs.cloud.google.com/bigquery/docs/authentication/end-user-installed?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]