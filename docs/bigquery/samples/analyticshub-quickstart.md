Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用 Analytics Hub 建立資料交換和項目 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本快速入門導覽課程會示範如何使用 Analytics Hub API 建立資料交換庫和清單。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [Sharing 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub?hl=zh-tw)

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// The analyticshub quickstart application demonstrates usage of the
// Analytics hub API by creating an example data exchange and listing.
package main

import (
	"context"
	"flag"
	"fmt"
	"log"

	analyticshub "cloud.google.com/go/bigquery/analyticshub/apiv1"
	"cloud.google.com/go/bigquery/analyticshub/apiv1/analyticshubpb"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func main() {

	// Define the command line flags for controlling the behavior of this quickstart.
	var (
		projectID            = flag.String("project_id", "", "Cloud Project ID, used for session creation.")
		location             = flag.String("location", "US", "BigQuery location used for interactions.")
		exchangeID           = flag.String("exchange_id", "ExampleDataExchange", "identifier of the example data exchange")
		listingID            = flag.String("listing_id", "ExampleDataExchange", "identifier of the example data exchange")
		exampleDatasetSource = flag.String("dataset_source", "", "dataset source in the form projects/myproject/datasets/mydataset")
		delete               = flag.Bool("delete_exchange", true, "delete exchange at the end of quickstart")
	)
	flag.Parse()
	// Perform simple validation of the specified flags.
	if *projectID == "" {
		log.Fatal("empty --project_id specified, please provide a valid project ID")
	}
	if *exampleDatasetSource == "" {
		log.Fatalf("empty --dataset_source specified, please provide in the form \"projects/myproject/datasets/mydataset\"")
	}

	// Instantiate the client.
	ctx := context.Background()
	ahubClient, err := analyticshub.NewClient(ctx)
	if err != nil {
		log.Fatalf("NewClient: %v", err)
	}
	defer ahubClient.Close()

	// Then, create the data exchange (or return information about one already bearing the example name), and
	// print information about it.
	exchange, err := createOrGetDataExchange(ctx, ahubClient, *projectID, *location, *exchangeID)
	if err != nil {
		log.Fatalf("failed to get information about the exchange: %v", err)
	}
	fmt.Printf("\nData Exchange Information\n")
	fmt.Printf("Exchange Name: %s\n", exchange.GetName())
	if desc := exchange.GetDescription(); desc != "" {
		fmt.Printf("Exchange Description: %s", desc)
	}

	// Finally, create a listing within the data exchange and print information about it.
	listing, err := createListing(ctx, ahubClient, *projectID, *location, *exchangeID, *listingID, *exampleDatasetSource)
	if err != nil {
		log.Fatalf("failed to create the listing within the exchange: %v", err)
	}
	fmt.Printf("\n\nListing Information\n")
	fmt.Printf("Listing Name: %s\n", listing.GetName())
	if desc := listing.GetDescription(); desc != "" {
		fmt.Printf("Listing Description: %s\n", desc)
	}
	fmt.Printf("Listing State: %s\n", listing.GetState().String())
	if source := listing.GetSource(); source != nil {
		if dsSource, ok := source.(*analyticshubpb.Listing_BigqueryDataset); ok && dsSource.BigqueryDataset != nil {
			if dataset := dsSource.BigqueryDataset.GetDataset(); dataset != "" {
				fmt.Printf("Source is a bigquery dataset: %s", dataset)
			}
		}
	}
	// Optionally, delete the data exchange at the end of the quickstart to clean up the resources used.
	if *delete {
		fmt.Printf("\n\n")
		if err := deleteDataExchange(ctx, ahubClient, *projectID, *location, *exchangeID); err != nil {
			log.Fatalf("failed to delete exchange: %v", err)
		}
		fmt.Printf("Exchange projects/%s/locations/%s/dataExchanges/%s was deleted.\n", *projectID, *location, *exchangeID)
	}
	fmt.Printf("\nQuickstart completed.\n")
}

// createOrGetDataExchange creates an example data exchange, or returns information about the exchange already bearing
// the example identifier.
func createOrGetDataExchange(ctx context.Context, client *analyticshub.Client, projectID, location, exchangeID string) (*analyticshubpb.DataExchange, error) {
	req := &analyticshubpb.CreateDataExchangeRequest{
		Parent:         fmt.Sprintf("projects/%s/locations/%s", projectID, location),
		DataExchangeId: exchangeID,
		DataExchange: &analyticshubpb.DataExchange{
			DisplayName:    "Example Data Exchange",
			Description:    "Exchange created as part of an API quickstart",
			PrimaryContact: "",
			Documentation:  "https://link.to.optional.documentation/",
		},
	}

	resp, err := client.CreateDataExchange(ctx, req)
	if err != nil {
		// We'll handle one specific error case specially, the case of the exchange already existing.  In this instance,
		// we'll issue a second request to fetch the exchange information for the already present exchange and return it.
		if code := status.Code(err); code == codes.AlreadyExists {
			getReq := &analyticshubpb.GetDataExchangeRequest{
				Name: fmt.Sprintf("projects/%s/locations/%s/dataExchanges/%s", projectID, location, exchangeID),
			}
			resp, err = client.GetDataExchange(ctx, getReq)
			if err != nil {
				return nil, fmt.Errorf("error getting dataExchange: %w", err)
			}
			return resp, nil
		}
		// For all other cases, return the error from creation request.
		return nil, err
	}
	return resp, nil
}

// createListing creates an example listing within the specified exchange using the provided source dataset.
func createListing(ctx context.Context, client *analyticshub.Client, projectID, location, exchangeID, listingID, sourceDataset string) (*analyticshubpb.Listing, error) {
	req := &analyticshubpb.CreateListingRequest{
		Parent:    fmt.Sprintf("projects/%s/locations/%s/dataExchanges/%s", projectID, location, exchangeID),
		ListingId: listingID,
		Listing: &analyticshubpb.Listing{
			DisplayName: "Example Exchange Listing",
			Description: "Example listing created as part of an API quickstart",
			Categories: []analyticshubpb.Listing_Category{
				analyticshubpb.Listing_CATEGORY_OTHERS,
			},
			Source: &analyticshubpb.Listing_BigqueryDataset{
				BigqueryDataset: &analyticshubpb.Listing_BigQueryDatasetSource{
					Dataset: sourceDataset,
				},
			},
		},
	}
	return client.CreateListing(ctx, req)
}

// deleteDataExchange deletes a data exchange.
func deleteDataExchange(ctx context.Context, client *analyticshub.Client, projectID, location, exchangeID string) error {
	req := &analyticshubpb.DeleteDataExchangeRequest{
		Name: fmt.Sprintf("projects/%s/locations/%s/dataExchanges/%s", projectID, location, exchangeID),
	}
	return client.DeleteDataExchange(ctx, req)
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
/**
 * TODO(developer): Uncomment these variables before running the sample.
 */
/**
 *  Required. The parent resource path of the DataExchanges.
 *  e.g. `projects/myproject/locations/US`.
 */
// const parent = 'abc123'
/**
 *  The maximum number of results to return in a single response page. Leverage
 *  the page tokens to iterate through the entire collection.
 */
// const pageSize = 1234
/**
 *  Page token, returned by a previous call, to request the next page of
 *  results.
 */
// const pageToken = 'abc123'

// Imports the Dataexchange library
const {AnalyticsHubServiceClient} =
  require('@google-cloud/bigquery-data-exchange').v1beta1;

// Instantiates a client
const dataexchangeClient = new AnalyticsHubServiceClient();

async function callListDataExchanges() {
  // Construct request
  const request = {
    parent,
  };

  // Run request
  const iterable = await dataexchangeClient.listDataExchangesAsync(request);
  for await (const response of iterable) {
    console.log(response);
  }
}

callListDataExchanges();
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=analyticshub&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]