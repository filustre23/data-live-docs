Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 開始使用驗證功能

應用程式預設憑證 (ADC) 可讓應用程式以服務帳戶憑證做為身分識別，藉此存取 BigQuery 資源。

請注意，BigQuery 不支援使用 [API 金鑰](https://docs.cloud.google.com/docs/authentication/api-keys-use?hl=zh-tw)。

## 事前準備

選取這個頁面上的分頁，瞭解如何使用範例：

### C#

如要在本機開發環境中使用本頁的 .NET 範例，請安裝並初始化 gcloud CLI，然後使用您的使用者憑證設定應用程式預設憑證。

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
2. 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
3. 如果您使用本機殼層，請為使用者帳戶建立本機驗證憑證：

   ```
   gcloud auth application-default login
   ```

   如果您使用 Cloud Shell，則不需要執行這項操作。

   如果系統傳回驗證錯誤，且您使用外部識別資訊提供者 (IdP)，請確認您已[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。

詳情請參閱[這篇文章](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#local-development)，瞭解如何設定本機開發環境的驗證機制。

### Go

如要在本機開發環境中使用本頁的 Go 範例，請安裝並初始化 gcloud CLI，然後使用使用者憑證設定應用程式預設憑證。

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
2. 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
3. 如果您使用本機殼層，請為使用者帳戶建立本機驗證憑證：

   ```
   gcloud auth application-default login
   ```

   如果您使用 Cloud Shell，則不需要執行這項操作。

   如果系統傳回驗證錯誤，且您使用外部識別資訊提供者 (IdP)，請確認您已[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。

詳情請參閱[這篇文章](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#local-development)，瞭解如何設定本機開發環境的驗證機制。

### Java

如要在本機開發環境中使用本頁面的 Java 範例，請安裝並初始化 gcloud CLI，然後使用使用者憑證設定應用程式預設憑證。

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
2. 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
3. 如果您使用本機殼層，請為使用者帳戶建立本機驗證憑證：

   ```
   gcloud auth application-default login
   ```

   如果您使用 Cloud Shell，則不需要執行這項操作。

   如果系統傳回驗證錯誤，且您使用外部識別資訊提供者 (IdP)，請確認您已[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。

詳情請參閱[這篇文章](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#local-development)，瞭解如何設定本機開發環境的驗證機制。

### Node.js

如要在本機開發環境中使用本頁的 Node.js 範例，請安裝並初始化 gcloud CLI，然後使用您的使用者憑證設定應用程式預設憑證。

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
2. 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
3. 如果您使用本機殼層，請為使用者帳戶建立本機驗證憑證：

   ```
   gcloud auth application-default login
   ```

   如果您使用 Cloud Shell，則不需要執行這項操作。

   如果系統傳回驗證錯誤，且您使用外部識別資訊提供者 (IdP)，請確認您已[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。

詳情請參閱[這篇文章](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#local-development)，瞭解如何設定本機開發環境的驗證機制。

### PHP

如要在本機開發環境中使用本頁的 PHP 範例，請安裝並初始化 gcloud CLI，然後使用使用者憑證設定應用程式預設憑證。

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
2. 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
3. 如果您使用本機殼層，請為使用者帳戶建立本機驗證憑證：

   ```
   gcloud auth application-default login
   ```

   如果您使用 Cloud Shell，則不需要執行這項操作。

   如果系統傳回驗證錯誤，且您使用外部識別資訊提供者 (IdP)，請確認您已[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。

詳情請參閱[這篇文章](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#local-development)，瞭解如何設定本機開發環境的驗證機制。

### Python

如要在本機開發環境中使用本頁的 Python 範例，請安裝並初始化 gcloud CLI，然後使用您的使用者憑證設定應用程式預設憑證。

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
2. 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
3. 如果您使用本機殼層，請為使用者帳戶建立本機驗證憑證：

   ```
   gcloud auth application-default login
   ```

   如果您使用 Cloud Shell，則不需要執行這項操作。

   如果系統傳回驗證錯誤，且您使用外部識別資訊提供者 (IdP)，請確認您已[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。

詳情請參閱[這篇文章](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#local-development)，瞭解如何設定本機開發環境的驗證機制。

### Ruby

如要在本機開發環境中使用本頁的 Ruby 範例，請安裝並初始化 gcloud CLI，然後使用您的使用者憑證設定應用程式預設憑證。

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
2. 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
3. 如果您使用本機殼層，請為使用者帳戶建立本機驗證憑證：

   ```
   gcloud auth application-default login
   ```

   如果您使用 Cloud Shell，則不需要執行這項操作。

   如果系統傳回驗證錯誤，且您使用外部識別資訊提供者 (IdP)，請確認您已[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。

詳情請參閱[這篇文章](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#local-development)，瞭解如何設定本機開發環境的驗證機制。

如要瞭解如何設定正式環境的驗證機制，請參閱「[為在 Google Cloud上執行的程式碼設定應用程式預設憑證](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#on-gcp)」。

## 應用程式預設憑證

用戶端程式庫可以使用[應用程式預設憑證](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw)，輕鬆向 Google API 進行驗證，然後傳送要求給這些 API。有了應用程式預設憑證，您就能在本機測試應用程式並部署，不必變更基礎程式碼。詳情請參閱「[進行驗證以使用用戶端程式庫](https://docs.cloud.google.com/docs/authentication/client-libraries?hl=zh-tw)」一文。

當您使用 [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)建立服務物件時，如果未傳遞明確憑證，您的應用程式將會使用應用程式預設憑證進行驗證。下列範例說明如何使用 ADC 向 BigQuery 進行驗證。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[事前準備](#byb)」。

```
using Google.Apis.Bigquery.v2.Data;
using Google.Cloud.BigQuery.V2;

public class BigQueryCreateDataset
{
    public BigQueryDataset CreateDataset(
        string projectId = "your-project-id",
        string location = "US"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        var dataset = new Dataset
        {
            // Specify the geographic location where the dataset should reside.
            Location = location
        };
        // Create the dataset
        return client.CreateDataset(
            datasetId: "your_new_dataset_id", dataset);
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[事前準備](#byb)」。

```
// Sample bigquery-quickstart creates a Google BigQuery dataset.
package main

import (
	"context"
	"fmt"
	"log"

	"cloud.google.com/go/bigquery"
)

func main() {
	ctx := context.Background()

	// Sets your Google Cloud Platform project ID.
	projectID := "YOUR_PROJECT_ID"

	// Creates a client.
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		log.Fatalf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	// Sets the name for the new dataset.
	datasetName := "my_new_dataset"

	// Creates the new BigQuery dataset.
	if err := client.Dataset(datasetName).Create(ctx, &bigquery.DatasetMetadata{}); err != nil {
		log.Fatalf("Failed to create dataset: %v", err)
	}

	fmt.Printf("Dataset created\n")
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[事前準備](#byb)」。

```
public static void implicit() {
  // Instantiate a client. If you don't specify credentials when constructing a client, the
  // client library will look for credentials in the environment, such as the
  // GOOGLE_APPLICATION_CREDENTIALS environment variable.
  BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

  // Use the client.
  System.out.println("Datasets:");
  for (Dataset dataset : bigquery.listDatasets().iterateAll()) {
    System.out.printf("%s%n", dataset.getDatasetId().getDataset());
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[事前準備](#byb)」。

```
// Import the Google Cloud client library using default credentials
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[事前準備](#byb)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/** Uncomment and populate these variables in your code */
//$projectId = 'The Google project ID';

$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[事前準備](#byb)」。

```
from google.cloud import bigquery

# If you don't specify credentials when constructing the client, the
# client library will look for credentials in the environment.
client = bigquery.Client()
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[事前準備](#byb)」。

```
require "google/cloud/bigquery"

# This uses Application Default Credentials to authenticate.
# @see https://cloud.google.com/bigquery/docs/authentication/getting-started
bigquery = Google::Cloud::Bigquery.new

sql     = "SELECT " \
          "CONCAT('https://stackoverflow.com/questions/', CAST(id as STRING)) as url, view_count " \
          "FROM `bigquery-public-data.stackoverflow.posts_questions` " \
          "WHERE tags like '%google-bigquery%' " \
          "ORDER BY view_count DESC LIMIT 10"
results = bigquery.query sql

results.each do |row|
  puts "#{row[:url]}: #{row[:view_count]} views"
end
```

## 後續步驟

* 進一步瞭解 [BigQuery 驗證](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw)。
* 瞭解如何[以使用者憑證進行驗證](https://docs.cloud.google.com/bigquery/docs/authentication/end-user-installed?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]