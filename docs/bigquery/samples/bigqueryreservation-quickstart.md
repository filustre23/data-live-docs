Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 回報容量使用承諾和保留項目 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

列出特定專案和位置的所有容量使用承諾和預訂。將結果列印到 Cloud Console。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [BigQuery Reservation API 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/reservations?hl=zh-tw)

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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
	"cloud.google.com/go/bigquery/reservation/apiv1/reservationpb"
	"google.golang.org/api/iterator"
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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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
          .iterateAll()
          .forEach(
              commitment ->
                  System.out.println("Capacity commitment resource name: " + commitment.getName()));
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Imports the Google Cloud client library
const {
  ReservationServiceClient,
} = require('@google-cloud/bigquery-reservation');

// Creates a client
const client = new ReservationServiceClient();

// project = 'my-project' // Project to list reservations for.
// location = 'US' // BigQuery location.

async function listReservations() {
  const [reservations] = await client.listReservations({
    parent: `projects/${project}/locations/${location}`,
  });

  console.info(`found ${reservations.length} reservations`);
  console.info(reservations);
}

async function listCapacityCommitments() {
  const [commitments] = await client.listCapacityCommitments({
    parent: `projects/${project}/locations/${location}`,
  });

  console.info(`found ${commitments.length} commitments`);
  console.info(commitments);
}

listReservations();
listCapacityCommitments();
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import argparse

from google.cloud import bigquery_reservation_v1


def main(
    project_id: str = "your-project-id", location: str = "US", transport: str = "grpc"
) -> None:
    # Constructs the client for interacting with the service.
    client = bigquery_reservation_v1.ReservationServiceClient(transport=transport)

    report_reservations(client, project_id, location)


def report_reservations(
    client: bigquery_reservation_v1.ReservationServiceClient,
    project_id: str,
    location: str,
) -> None:
    """Prints details and summary information about reservations defined within
    a given admin project and location.
    """
    print("Reservations in project {} in location {}".format(project_id, location))
    req = bigquery_reservation_v1.ListReservationsRequest(
        parent=client.common_location_path(project_id, location)
    )
    total_reservations = 0
    for reservation in client.list_reservations(request=req):
        print(
            f"\tReservation {reservation.name} "
            f"has {reservation.slot_capacity} slot capacity."
        )
        total_reservations = total_reservations + 1
    print(f"\n{total_reservations} reservations processed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=str)
    parser.add_argument("--location", default="US", type=str)
    args = parser.parse_args()
    main(project_id=args.project_id, location=args.location)
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigqueryreservation&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]