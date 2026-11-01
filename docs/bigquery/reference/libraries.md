Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見

# BigQuery API 用戶端程式庫 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本頁說明如何開始使用 BigQuery API 適用的 Cloud 用戶端程式庫。有了用戶端程式庫，您可以透過支援的語言，更輕鬆地存取Google Cloud API。雖然您可以直接向伺服器發出原始要求來使用Google Cloud API，但用戶端程式庫提供簡化功能，可大幅減少需要編寫的程式碼數量。

如要進一步瞭解 Cloud 用戶端程式庫和舊版 Google API 用戶端程式庫，請參閱「[用戶端程式庫說明](https://docs.cloud.google.com/apis/docs/client-libraries-explained?hl=zh-tw)」。

## 安裝用戶端程式庫

### C#

```
Install-Package Google.Cloud.BigQuery.V2 -Pre
```

詳情請參閱「[設定 C# 開發環境](https://docs.cloud.google.com/dotnet/docs/setup?hl=zh-tw)」。

### Go

```
go get cloud.google.com/go/bigquery
```

詳情請參閱「[設定 Go 開發環境](https://docs.cloud.google.com/go/docs/setup?hl=zh-tw)」。

### Java

如果您使用 [Maven](https://maven.apache.org/)，請將下列指令新增至 `pom.xml` 檔案。如要進一步瞭解 BOM，請參閱「[Google Cloud Platform 程式庫 BOM](https://cloud.google.com/java/docs/bom?hl=zh-tw)」。

```
<!--  Using libraries-bom to manage versions.
See https://github.com/GoogleCloudPlatform/cloud-opensource-java/wiki/The-Google-Cloud-Platform-Libraries-BOM -->
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>com.google.cloud</groupId>
      <artifactId>libraries-bom</artifactId>
      <version>26.62.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>
    <groupId>com.google.cloud</groupId>
    <artifactId>google-cloud-bigquery</artifactId>
  </dependency>
</dependencies>
```

如果您使用 [Gradle](https://gradle.org/)，請在依附元件中加入以下指令：

```
implementation platform('com.google.cloud:libraries-bom:26.45.0')

implementation 'com.google.cloud:google-cloud-bigquery'
```

如果您使用 [sbt](https://www.scala-sbt.org/)，請在依附元件中加入以下指令：

```
libraryDependencies += "com.google.cloud" % "google-cloud-bigquery" % "2.42.2"
```

如果您使用的是 Visual Studio Code 或 IntelliJ，可以使用下列 IDE 外掛程式，將用戶端程式庫新增至專案：

* [Cloud Code for VS Code](https://docs.cloud.google.com/code/docs/vscode/client-libraries?hl=zh-tw)
* [Cloud Code for IntelliJ](https://docs.cloud.google.com/code/docs/intellij/client-libraries?hl=zh-tw)

這些外掛程式會提供其他功能，例如服務帳戶的金鑰管理功能。詳情請參閱各外掛程式的說明文件。

**注意：**Cloud Java 用戶端程式庫目前不支援 Android。

詳情請參閱「[設定 Java 開發環境](https://docs.cloud.google.com/java/docs/setup?hl=zh-tw)」。

### Node.js

```
npm install @google-cloud/bigquery
```

詳情請參閱「[設定 Node.js 開發環境](https://docs.cloud.google.com/nodejs/docs/setup?hl=zh-tw)」。

### PHP

```
composer require google/cloud-bigquery
```

詳情請參閱「[在 Google Cloud 上使用 PHP](https://docs.cloud.google.com/php/docs?hl=zh-tw)」。

### Python

```
pip install --upgrade google-cloud-bigquery
```

詳情請參閱「[設定 Python 開發環境](https://docs.cloud.google.com/python/docs/setup?hl=zh-tw)」。

### Ruby

```
gem install google-cloud-bigquery
```

詳情請參閱「[設定 Ruby 開發環境](https://docs.cloud.google.com/ruby/docs/setup?hl=zh-tw)」。

### Rust

```
cargo add google-cloud-bigquery
```

詳情請參閱「[開始使用 Rust](https://docs.cloud.google.com/rust/docs/quickstart?hl=zh-tw)」。

## 設定驗證方法

為驗證向 Google Cloud API 發出的呼叫，用戶端程式庫支援[應用程式預設憑證 (ADC)](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw)；程式庫會在定義的一組位置中尋找憑證，並使用這些憑證驗證向 API 發出的要求。有了 ADC，無需修改應用程式程式碼，就能在各種環境 (例如本機開發環境或正式環境)，為應用程式提供憑證。

在正式環境中，設定 ADC 的方式取決於服務和背景。詳情請參閱「[設定應用程式預設憑證](https://docs.cloud.google.com/docs/authentication/provide-credentials-adc?hl=zh-tw)」。

在本機開發環境中，您可以使用與 Google 帳戶相關聯的憑證設定 ADC：

1. [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
   安裝完成後，請執行下列指令，[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) Google Cloud CLI：

   ```
   gcloud init
   ```

   若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
2. 如果您使用的是本機殼層，請為使用者帳戶建立本機驗證憑證：

   ```
   gcloud auth application-default login
   ```

   如果您使用的是 Cloud Shell，則不必執行這項操作。

   如果系統傳回驗證錯誤，且您使用的是外部識別資訊提供者 (IdP)，請確認您已[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。

   登入畫面會隨即顯示。登入後，您的憑證會儲存在 [ADC 使用的本機憑證檔案](https://docs.cloud.google.com/docs/authentication/application-default-credentials?hl=zh-tw#personal)中。

## 使用用戶端程式庫

以下範例說明如何初始化用戶端，並對 BigQuery API 公開資料集執行查詢。

**注意：**不支援 JRuby。

### C#

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryQuery
{
    public void Query(
        string projectId = "your-project-id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        string query = @"
            SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013`
            WHERE state = 'TX'
            LIMIT 100";
        BigQueryJob job = client.CreateQueryJob(
            sql: query,
            parameters: null,
            options: new QueryOptions { UseQueryCache = false });
        // Wait for the job to complete.
        job = job.
```