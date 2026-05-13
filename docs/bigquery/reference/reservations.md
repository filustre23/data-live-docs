* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQuery Reservation API Client Libraries Stay organized with collections Save and categorize content based on your preferences.

This page shows how to get started with the Cloud Client Libraries for the
BigQuery Reservation API. Client libraries make it easier to access
Google Cloud APIs from a supported language. Although you can use
Google Cloud APIs directly by making raw requests to the server, client
libraries provide simplifications that significantly reduce the amount of code
you need to write.

Read more about the Cloud Client Libraries
and the older Google API Client Libraries in
[Client libraries explained](/apis/docs/client-libraries-explained).

## Install the client library

### C#

```
Install-Package Google.Cloud.BigQuery.Reservation.V1 -Pre
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
      <version>26.80.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>
    <groupId>com.google.cloud</groupId>
    <artifactId>google-cloud-bigqueryreservation</artifactId>
  </dependency>
</dependencies>
```

If you are using [Gradle](https://gradle.org/),
add the following to your dependencies:

```
implementation 'com.google.cloud:google-cloud-bigqueryreservation:2.92.0'
```

If you are using [sbt](https://www.scala-sbt.org/), add
the following to your dependencies:

```
libraryDependencies += "com.google.cloud" % "google-cloud-bigqueryreservation" % "2.92.0"
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
npm install @google-cloud/bigquery-reservation
```

For more information, see [Setting Up a Node.js Development Environment](/nodejs/docs/setup).

### PHP

```
composer require google/cloud-bigquery-reservation
```

For more information, see [Using PHP on Google Cloud](/php/docs).

### Python

```
pip install --upgrade google-cloud-bigquery-reservation
```

For more information, see [Setting Up a Python Development Environment](/python/docs/setup).

### Ruby

```
gem install google-cloud-bigquery-reservation
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

The following example demonstrates some basic interactions with the BigQuery Reservation API by enumerating resources, namely reservations and capacity
commitments.

### Go

```
// The bigquery_reservation_quickstart application demonstrates usage of the
// BigQuery reservation API by enumerating some of the resources that can be
// associated with a cloud project.
package main

import (
	"bytes"
	"context"
	"flag"
	"fmt"
	"log"

	reservation "cloud.google.com/go/bigquery/reservation/apiv1"
	"google.golang.org/api/iterator"
	reservationpb "google.golang.org/genproto/googleapis/cloud/bigquery/reservation/v1"
)

func main() {

	// Define two command line flags for controlling the behavior of this quickstart.
	var (
		projectID = flag.String("project_id", "", "Cloud Project ID, used for session creation.")
		location  = flag.String("location", "US", "BigQuery location used for interactions.")
	)
	// Parse flags and do some minimal validation.
	flag.Parse()
	if *projectID == "" {
		log.Fatal("empty --project_id specified, please provide a valid project ID")
	}
	if *location == "" {
		log.Fatal("empty --location specified, please provide a valid location")
	}

	ctx := context.Background()
	bqResClient, err := reservation.NewClient(ctx)
	if err != nil {
		log.Fatalf("NewClient: %v", err)
	}
	defer bqResClient.Close()

	s, err := reportCapacityCommitments(ctx, bqResClient, *projectID, *location)
	if err != nil {
		log.Fatalf("printCapacityCommitments: %v", err)
	}
	fmt.Println(s)

	s, err = reportReservations(ctx, bqResClient, *projectID, *location)
	if err != nil {
		log.Fatalf("printReservations: %v", err)
	}
	fmt.Println(s)
}

// printCapacityCommitments iterates through the capacity commitments and returns a byte buffer with details.
func reportCapacityCommitments(ctx context.Context, client *reservation.Client, projectID, location string) (string, error) {
	var buf bytes.Buffer
	fmt.Fprintf(&buf, "Capacity commitments in project %s in location %s:\n", projectID, location)

	req := &reservationpb.ListCapacityCommitmentsRequest{
		Parent: fmt.Sprintf("projects/%s/locations/%s", projectID, location),
	}
	totalCommitments := 0
	it := client.ListCapacityCommitments(ctx, req)
	for {
		commitment, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return "", err
		}
		fmt.Fprintf(&buf, "\tCommitment %s in state %s\n", commitment.GetName(), commitment.GetState().String())
		totalCommitments++
	}
	fmt.Fprintf(&buf, "\n%d commitments processed.\n", totalCommitments)
	return buf.String(), nil
}

// printReservations iterates through reservations defined in an admin project.
func reportReservations(ctx context.Context, client *reservation.Client, projectID, location string) (string, error) {
	var buf bytes.Buffer
	fmt.Fprintf(&buf, "Reservations in project %s in location %s:\n", projectID, location)

	req := &reservationpb.ListReservationsRequest{
		Parent: fmt.Sprintf("projects/%s/locations/%s", projectID, location),
	}
	totalReservations := 0
	it := client.ListReservations(ctx, req)
	for {
		reservation, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return "", err
		}
		fmt.Fprintf(&buf, "\tReservation %s has %d slot capacity.\n", reservation.GetName(), reservation.GetSlotCapacity())
		totalReservations++
	}
	fmt.Fprintf(&buf, "\n%d reservations processed.\n", totalReservations)
	return buf.String(), nil
}
```

### Java

```
import com.google.cloud.bigquery.reservation.v1.ReservationServiceClient;
import java.io.IOException;

public class QuickstartSample {

  public static void main(String... args) throws Exception {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "YOUR_PROJECT_ID";
    String location = "LOCATION";
    quickStartSample(projectId, location);
  }

  public static void quickStartSample(String projectId, String location) throws IOException {
    try (ReservationServiceClient client = ReservationServiceClient.create()) {
      // list reservations in the project
      String parent = String.format("projects/%s/locations/%s", projectId, location);
      client
          .listReservations(parent)
          .iterateAll()
          .forEach(res -> System.out.println("Reservation resource name: " + res.getName()));

      // list capacity commitments in the project
      client
          .listCapacityCommitments(parent)
```