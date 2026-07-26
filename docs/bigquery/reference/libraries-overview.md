Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery API 和程式庫總覽

本頁面提供與 BigQuery 相關聯的各種 API 總覽。雖然您可以直接向伺服器發出原始要求來使用 API，但用戶端程式庫可讓您以偏好的語言編寫程式碼，並提供簡化功能，大幅減少需要編寫的程式碼數量。BigQuery 支援 C#、Go、Java、Node.js、PHP、Python 和 Ruby 的用戶端程式庫。如要大致瞭解 Google Cloud內的用戶端程式庫，請參閱「[用戶端程式庫說明](https://docs.cloud.google.com/apis/docs/client-libraries-explained?hl=zh-tw)」。

如要查看使用各種 BigQuery 程式庫和 API 的範例，請參閱 [BigQuery 程式碼範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)。

如要使用這些 API，您必須先驗證用戶端身分。您可以透過[應用程式預設憑證](https://docs.cloud.google.com/bigquery/docs/authentication/getting-started?hl=zh-tw)、[服務帳戶金鑰檔案](https://docs.cloud.google.com/bigquery/docs/authentication/service-account-file?hl=zh-tw)或[使用者憑證](https://docs.cloud.google.com/bigquery/docs/authentication/end-user-installed?hl=zh-tw)進行驗證。如要進一步瞭解驗證，請參閱「[驗證簡介](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw)」。

如要進一步瞭解 BigQuery 定價，包括[資料擷取](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)和[資料提取](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing)定價，請參閱[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

## BigQuery API

這個主要 API 提供資源，用於建立、修改及刪除資料集、資料表、工作和常式等核心資源。

* 如要瞭解如何安裝及使用，請參閱 [BigQuery API 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)。
* 如需相關配額資訊，請參閱「[BigQuery API 配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#api_request_quotas)」。

如要查看參考說明文件和原始碼的連結，請選取語言：

### C#

* [API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-dotnet/tree/main/apis/Google.Cloud.BigQuery.V2)

### Go

* [API 參考說明文件](https://docs.cloud.google.com/go/docs/reference/cloud.google.com/go/bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-go/tree/main/bigquery)

### Java

* [API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)
* [原始碼](https://github.com/googleapis/java-bigquery)

### Node.js

* [API 參考說明文件](https://docs.cloud.google.com/nodejs/docs/reference/bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/nodejs-bigquery)

### PHP

* [API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-php/tree/main/BigQuery)

### Python

* [API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/python-bigquery)

### Ruby

* [API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-ruby/tree/main/google-cloud-bigquery)

## BigQuery Data Policy API

使用者可透過這個 API 管理 BigQuery 資料政策，確保資料欄層級的安全性並遮蓋資料。

如要瞭解這個 API 及其用途，請參閱「[BigQuery Data Policy API](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest?hl=zh-tw)」。如要查看參考文件和原始碼的連結，請選取語言：

### C++

* [API 參考說明文件](https://docs.cloud.google.com/cpp/docs/reference/bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-cpp/tree/main/google/cloud/bigquery/datapolicies/v1)

### C#

* [API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.DataPolicies.V1/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-dotnet/tree/main/apis/Google.Cloud.BigQuery.DataPolicies.V1)

### Go

* [API 參考說明文件](https://docs.cloud.google.com/go/docs/reference/cloud.google.com/go/bigquery/latest/datapolicies/apiv1?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-go/tree/main/bigquery/datapolicies)

### Java

* [API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerydatapolicy/latest/overview?hl=zh-tw)
* [原始碼](https://github.com/googleapis/java-bigquerydatapolicy)

### PHP

* [API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery-datapolicies/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-php/tree/main/BigQueryDataPolicies)

### Ruby

* [API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-bigquery-data_policies/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-ruby/tree/main/google-cloud-bigquery-data_policies)

## BigQuery Connection API

這項 API 提供控制平面，可建立遠端連線，讓 BigQuery 與 Cloud SQL 等遠端資料來源互動。BigQuery API 和程式庫會公開部分聯邦查詢功能。

如要進一步瞭解安裝和使用方式，請參閱 [BigQuery Connection 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection?hl=zh-tw)。如要查看參考文件和原始碼的連結，請選取語言：

### C++

* [API 參考說明文件](https://docs.cloud.google.com/cpp/docs/reference/bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-cpp/tree/main/google/cloud/bigquery/connection/v1)

### C#

* [API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.Connection.V1/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-dotnet/tree/main/apis/Google.Cloud.BigQuery.Connection.V1)

### Go

* [API 參考說明文件](https://docs.cloud.google.com/go/docs/reference/cloud.google.com/go/bigquery/latest/connection/apiv1?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-go/tree/main/bigquery/connection)

### Java

* [API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigqueryconnection/latest/overview?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-java/tree/main/java-bigqueryconnection)

### Node.js

* [API 參考說明文件](https://docs.cloud.google.com/nodejs/docs/reference/bigquery-connection/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-node/tree/main/packages/google-cloud-bigquery-connection)

### PHP

* [API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery-connection/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-php/tree/main/BigQueryConnection)

### Python

* [API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigqueryconnection/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/python-bigquery-connection)

### Ruby

* [API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-bigquery-connection/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-ruby/tree/main/google-cloud-bigquery-connection)

## BigQuery Migration API

這個 API 支援多種機制，可協助使用者將現有資料倉儲遷移至 BigQuery。這項技術主要將工作模擬為一系列待處理的工作流程和工作，例如翻譯 SQL。

如要進一步瞭解安裝和使用方式，請參閱 [BigQuery Migration 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/migration?hl=zh-tw)。如要查看參考文件和原始碼的連結，請選取語言：

### C++

* [API 參考說明文件](https://docs.cloud.google.com/cpp/docs/reference/bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-cpp/tree/main/google/cloud/bigquery/migration/v2)

### C#

* [API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.Migration.V2/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-dotnet/tree/main/apis/Google.Cloud.BigQuery.Migration.V2)

### Go

* [API 參考說明文件](https://docs.cloud.google.com/go/docs/reference/cloud.google.com/go/bigquery/latest/migration/apiv2?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-go/tree/main/bigquery/migration)

### Java

* [API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerymigration/latest/overview?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-java/tree/main/java-bigquerymigration)

### Node.js

* [API 參考說明文件](https://docs.cloud.google.com/nodejs/docs/reference/bigquery-migration/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/nodejs-bigquery-migration)

### PHP

* [API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery-migration/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-php/tree/main/BigQueryMigration)

### Python

* [API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquerymigration/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/python-bigquery-migration)

### Ruby

* [API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-bigquery-migration/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-ruby/tree/main/google-cloud-bigquery-migration)

## BigQuery Storage API

這個 API 可為需要從自家應用程式和工具掃描大量受管理資料的消費者，提供高輸送量的資料讀取功能。API 支援平行掃描儲存空間的機制，並提供支援，可運用資料欄專案和篩選等功能。

如要進一步瞭解安裝和使用方式，請參閱 [BigQuery Storage 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw)。如要查看參考文件和原始碼的連結，請選取語言：

### C++

* [API 參考說明文件](https://docs.cloud.google.com/cpp/docs/reference/bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-cpp/tree/main/google/cloud/bigquery/storage/v1)

### C#

* [API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.Storage.V1/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-dotnet/tree/main/apis/Google.Cloud.BigQuery.Storage.V1)

### Go

* [API 參考說明文件](https://docs.cloud.google.com/go/docs/reference/cloud.google.com/go/bigquery/latest/storage/apiv1?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-go/tree/main/bigquery/storage)

### Java

* [API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/overview?hl=zh-tw)
* [原始碼](https://github.com/googleapis/java-bigquerystorage)

### Node.js

* [API 參考說明文件](https://docs.cloud.google.com/nodejs/docs/reference/bigquery-storage/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/nodejs-bigquery-storage)

### PHP

* [API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery-storage/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-php/tree/main/BigQueryStorage)

### Python

* [API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquerystorage/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-python)

### Ruby

* [API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-bigquery-storage/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-ruby/tree/main/google-cloud-bigquery-storage)

## BigQuery Reservation API

這個 API 提供相關機制，讓企業使用者佈建及管理專屬資源，例如配額和 BigQuery BI Engine 記憶體配置。

如要進一步瞭解如何安裝及使用，請參閱 [BigQuery Reservation 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/reservations?hl=zh-tw)。如要查看參考文件和原始碼的連結，請選取語言：

### C++

* [API 參考說明文件](https://docs.cloud.google.com/cpp/docs/reference/bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-cpp/tree/main/google/cloud/bigquery/reservation/v1)

### C#

* [API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.Reservation.V1/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-dotnet/tree/main/apis/Google.Cloud.BigQuery.Reservation.V1)

### Go

* [API 參考說明文件](https://docs.cloud.google.com/go/docs/reference/cloud.google.com/go/bigquery/latest/reservation/apiv1?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-go/tree/main/bigquery/reservation/apiv1)

### Java

* [API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigqueryreservation/latest/overview?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-java/tree/main/java-bigqueryreservation)

### Node.js

* [API 參考說明文件](https://docs.cloud.google.com/nodejs/docs/reference/bigquery-reservation/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-node/tree/main/packages/google-cloud-bigquery-reservation)

### PHP

* [API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery-reservation/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-php/tree/main/BigQueryReservation)

### Python

* [API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigqueryreservation/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/python-bigquery-reservation)

### Ruby

* [API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-bigquery-reservation/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-ruby/tree/main/google-cloud-bigquery-reservation)

## BigQuery sharing (舊稱 Analytics Hub)

這項 API 可讓您在組織內和跨組織共用資料，資料供應商可透過這項功能發布清單，參照共用資源，包括 BigQuery 資料集和 Pub/Sub 主題。透過 BigQuery 共用功能，使用者可以探索及搜尋有權存取的房源資訊。訂閱者可以查看及訂閱清單。訂閱清單時，系統會在專案中建立連結的資料集。

如要進一步瞭解這項 API 和使用方式，請參閱「[Analytics Hub API](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest?hl=zh-tw)」。如要查看參考文件和原始碼的連結，請選取語言：

### C++

* [API 參考說明文件](https://docs.cloud.google.com/cpp/docs/reference/bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-cpp/tree/main/google/cloud/bigquery/analyticshub/v1)

### C#

* [API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.AnalyticsHub.V1/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-dotnet/tree/main/apis/Google.Cloud.BigQuery.AnalyticsHub.V1)

### Go

* [API 參考說明文件](https://docs.cloud.google.com/go/docs/reference/cloud.google.com/go/bigquery/latest/analyticshub/apiv1?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-go/tree/main/bigquery/analyticshub/apiv1)

### Java

* [API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery-data-exchange/latest/overview?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-java/tree/main/java-bigquery-data-exchange)

### Node.js

* [API 參考說明文件](https://docs.cloud.google.com/nodejs/docs/reference/bigquery-data-exchange/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-node/tree/main/packages/google-cloud-bigquery-dataexchange)

### PHP

* [API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery-analyticshub/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-php/tree/main/BigQueryAnalyticsHub)

### Python

* [API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/analyticshub/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/python-bigquery-analyticshub)

### Ruby

* [API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-bigquery-data_exchange/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-ruby/tree/main/google-cloud-bigquery-data_exchange)

## BigQuery 資料移轉服務 API

這個 API 用於受管理的擷取管道。管道的例子包括：排定從 Cloud Storage 定期擷取資料、從 YouTube 等其他 Google 資源自動擷取分析資料，或是從與服務整合的第三方合作夥伴轉移資料。

您也可以透過這個 API，在 BigQuery 中定義及管理排定執行的查詢。

如要進一步瞭解如何安裝及使用，請參閱 [BigQuery 資料移轉服務用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/libraries?hl=zh-tw)。如要查看參考文件和原始碼的連結，請選取語言：

### C++

* [API 參考說明文件](https://docs.cloud.google.com/cpp/docs/reference/bigquery/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-cpp/tree/main/google/cloud/bigquery/datatransfer/v1)

### C#

* [API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.DataTransfer.V1/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-dotnet/tree/main/apis/Google.Cloud.BigQuery.DataTransfer.V1)

### Go

* [API 參考說明文件](https://docs.cloud.google.com/go/docs/reference/cloud.google.com/go/bigquery/latest/datatransfer/apiv1?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-go/tree/main/bigquery/datatransfer/apiv1)

### Java

* [API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerydatatransfer/latest/overview?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-java/tree/main/java-bigquerydatatransfer)

### Node.js

* [API 參考說明文件](https://docs.cloud.google.com/nodejs/docs/reference/bigquery-data-transfer/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-node/tree/main/packages/google-cloud-bigquery-datatransfer)

### PHP

* [API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquerydatatransfer/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-php/tree/main/BigQueryDataTransfer)

### Python

* [API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquerydatatransfer/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/python-bigquery-datatransfer)

### Ruby

* [API 參考說明文件](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-bigquery-data_transfer/latest?hl=zh-tw)
* [原始碼](https://github.com/googleapis/google-cloud-ruby/tree/main/google-cloud-bigquery-data_transfer)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-21 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-21 (世界標準時間)。"],[],[]]