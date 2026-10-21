* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQuery Storage API Client Libraries Stay organized with collections Save and categorize content based on your preferences.

This page shows how to get started with the Cloud Client Libraries for the
BigQuery Storage API. Client libraries make it easier to access
Google Cloud APIs from a supported language. Although you can use
Google Cloud APIs directly by making raw requests to the server, client
libraries provide simplifications that significantly reduce the amount of code
you need to write.

Read more about the Cloud Client Libraries
and the older Google API Client Libraries in
[Client libraries explained](/apis/docs/client-libraries-explained).

## Install the client library

### C++

For more information about installing the C++ library,
see the [GitHub `README`](https://github.com/googleapis/google-cloud-cpp/tree/master/google/cloud/bigquery/quickstart).

### C#

```
Install-Package Google.Cloud.BigQuery.Storage.V1 -Pre
```

For more information, see [Setting Up a C# Development Environment](/dotnet/docs/setup).

### Go

```
go get cloud.google.com/go/bigquery
```

For more information, see [Setting Up a Go Development Environment](/go/docs/setup).

### Java

If you are using [Maven](https://maven.apache.org/), add
the following to your `pom.xml` file. For more information about
BOMs, see [The Google Cloud Platform Libraries BOM](https://cloud.google.com/java/docs/bom).

```
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>com.google.cloud</groupId>
      <artifactId>libraries-bom</artifactId>
      <version>26.70.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
    <dependency>
      <groupId>io.opentelemetry</groupId>
      <artifactId>opentelemetry-bom</artifactId>
      <version>1.52.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>
    <groupId>com.google.cloud</groupId>
    <artifactId>google-cloud-bigquerystorage</artifactId>
  </dependency>
```

If you are using [Gradle](https://gradle.org/),
add the following to your dependencies:

```
implementation platform('com.google.cloud:libraries-bom:26.74.0')

implementation 'com.google.cloud:google-cloud-bigquerystorage'
```

If you are using [sbt](https://www.scala-sbt.org/), add
the following to your dependencies:

```
libraryDependencies += "com.google.cloud" % "google-cloud-bigquerystorage" % "3.21.0"
```

If you're using Visual Studio Code or IntelliJ, you can add client libraries to your
project using the following IDE plugins:

* [Cloud Code for VS Code](/code/docs/vscode/client-libraries)
* [Cloud Code for IntelliJ](/code/docs/intellij/client-libraries)

The plugins provide additional functionality, such as key management for service accounts. Refer
to each plugin's documentation for details.

**Note:** Cloud Java client libraries do not currently support Android.

For more information, see [Setting Up a Java Development Environment](/java/docs/setup).

### Node.js

```
npm install @google-cloud/bigquery-storage
```

For more information, see [Setting Up a Node.js Development Environment](/nodejs/docs/setup).

### PHP

```
composer require google/cloud-bigquery-storage
```

For more information, see [Using PHP on Google Cloud](/php/docs).

### Python

```
pip install --upgrade google-cloud-bigquery-storage
```

For more information, see [Setting Up a Python Development Environment](/python/docs/setup).

### Ruby

```
gem install google-cloud-bigquery-storage
```

For more information, see [Setting Up a Ruby Development Environment](/ruby/docs/setup).

## Set up authentication

To authenticate calls to Google Cloud APIs, client libraries support
[Application Default Credentials (ADC)](/docs/authentication/application-default-credentials);
the libraries look for credentials in a set of defined locations and use those credentials
to authenticate requests to the API. With ADC, you can make
credentials available to your application in a variety of environments, such as local
development or production, without needing to modify your application code.

For production environments, the way you set up ADC depends on the service
and context. For more information, see [Set up Application Default Credentials](/docs/authentication/provide-credentials-adc).

For a local development environment, you can set up ADC with the credentials
that are associated with your Google Account:

1. [Install](/sdk/docs/install) the Google Cloud CLI.
   After installation,
   [initialize](/sdk/docs/initializing) the Google Cloud CLI by running the following command:

   ```
   gcloud init
   ```

   If you're using an external identity provider (IdP), you must first
   [sign in to the gcloud CLI with your federated identity](/iam/docs/workforce-log-in-gcloud).
2. If you're using a local shell, then create local authentication credentials for your user
   account:

   ```
   gcloud auth application-default login
   ```

   You don't need to do this if you're using Cloud Shell.

   If an authentication error is returned, and you are using an external identity provider
   (IdP), confirm that you have
   [signed in to the gcloud CLI with your federated identity](/iam/docs/workforce-log-in-gcloud).

   A sign-in screen appears. After you sign in, your credentials are stored in the
   [local credential file used by ADC](/docs/authentication/application-default-credentials#personal).

## Use the client library

The following example shows basic interactions with the
[BigQuery Storage Read API](/bigquery/docs/reference/storage).

For examples of how to use the BigQuery Storage Write API (gRPC), see
[Perform batch and streaming using the Storage Write API (gRPC)](/bigquery/docs/write-api).

### C++

```
#include "google/cloud/bigquery/storage/v1/bigquery_read_client.h"
#include <iostream>

namespace {
void ProcessRowsInAvroFormat(
    ::google::cloud::bigquery::storage::v1::AvroSchema const&,
    ::google::cloud::bigquery::storage::v1::AvroRows const&) {
  // Code to deserialize avro rows should be added here.
}
}  // namespace

int main(int argc, char* argv[]) try {
  if (argc != 3) {
    std::cerr << "Usage: " << argv[0] << " <project-id> <table-name>\n";
    return 1;
  }

  // project_name should be in the format "projects/<your-gcp-project>"
  std::string const project_name = "projects/" + std::string(argv[1]);
  // table_name should be in the format:
  // "projects/<project-table-resides-in>/datasets/<dataset-table_resides-in>/tables/<table
  // name>" The project values in project_name and table_name do not have to be
  // identical.
  std::string const table_name = argv[2];

  // Create a namespace alias to make the code easier to read.
  namespace bigquery_storage = ::google::cloud::bigquery_storage_v1;
  constexpr int kMaxReadStreams = 1;
  // Create the ReadSession.
  auto client = bigquery_storage::BigQueryReadClient(
      bigquery_storage::MakeBigQueryReadConnection());
  ::google::cloud::bigquery::storage::v1::ReadSession read_session;
  read_session.set_data_format(
      google::cloud::bigquery::storage::v1::DataFormat::AVRO);
  read_session.set_table(table_name);
  auto session =
      client.CreateReadSession(project_name, read_session, kMaxReadStreams);
  if (!session) throw std::move(session).status();

  // Read rows from the ReadSession.
  constexpr int kRowOffset = 0;
  auto read_rows = client.ReadRows(session->streams(0).name(), kRowOffset);

  std::int64_t num_rows = 0;
  for (auto const& row : read_rows)
```