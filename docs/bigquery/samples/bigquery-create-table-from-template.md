* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用範本建立資料表 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用某個資料表的屬性 (結構定義、分割、叢集) 建立新資料表，新資料表會採用相同的設定，但內容為空白。

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// createTableFromTemplateTable demonstrates how to use the properties of one
// table (schema, partitioning, clustering) to create a new empty table with
// the same configuration.
func createTableFromTemplateTable(srcProjectID, srcDatasetID, srcTableID, dstProjectID, dstDatasetID, dstTableID string) error {
	// srcProjectID := "bigquery-public-data"
	// srcDatasetID := "samples"
	// srcTableID := "shakespeare"
	// dstProjectID := "my-project-id"
	// dstDatasetID := "mydataset"
	// dstTableID := "mytable"
	ctx := context.Background()

	// We'll construct the client based on the destination project.
	client, err := bigquery.NewClient(ctx, dstProjectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	srcTableRef := client.DatasetInProject(srcProjectID, srcDatasetID).Table(srcTableID)

	srcMeta, err := srcTableRef.Metadata(ctx)
	if err != nil {
		return fmt.Errorf("failed to get source table metadata: %w", err)
	}

	dstTableRef := client.Dataset(dstDatasetID).Table(dstTableID)

	// We'll use some (but not all) of the metadata from the source table
	// to define the destination table.  Other properties to consider include
	// attributes like expiration policy and managed encryption settings.
	dstMeta := &bigquery.TableMetadata{
		Description: fmt.Sprintf("table structure copied from %s.%s.%s",
			srcTableRef.ProjectID, srcTableRef.DatasetID, srcTableRef.TableID),
		Schema:     srcMeta.Schema,
		Clustering: srcMeta.Clustering,
		// A table will only have one partitioning configuration, the others will be empty/nil.
		TimePartitioning:  srcMeta.TimePartitioning,
		RangePartitioning: srcMeta.RangePartitioning,
		// Retain the same enforcement of partition filtering as well.
		RequirePartitionFilter: srcMeta.RequirePartitionFilter,
	}

	if err := dstTableRef.Create(ctx, dstMeta); err != nil {
		return err
	}

	return nil
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]