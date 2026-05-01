* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 示範批次查詢翻譯 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用 BigQuery Migration Service 翻譯儲存在 Cloud Storage 中的查詢

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// The bigquery_migration_quickstart application demonstrates basic usage of the
// BigQuery migration API by executing a workflow that performs a batch SQL
// translation task.
package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"time"

	migration "cloud.google.com/go/bigquery/migration/apiv2"
	"cloud.google.com/go/bigquery/migration/apiv2/migrationpb"
)

func main() {
	// Define command line flags for controlling the behavior of this quickstart.
	projectID := flag.String("project_id", "", "Cloud Project ID.")
	location := flag.String("location", "us", "BigQuery Migration location used for interactions.")
	outputPath := flag.String("output", "", "Cloud Storage path for translated resources.")
	// Parse flags and do some minimal validation.
	flag.Parse()
	if *projectID == "" {
		log.Fatal("empty --project_id specified, please provide a valid project ID")
	}
	if *location == "" {
		log.Fatal("empty --location specified, please provide a valid location")
	}
	if *outputPath == "" {
		log.Fatalf("empty --output specified, please provide a valid cloud storage path")
	}

	ctx := context.Background()
	migClient, err := migration.NewClient(ctx)
	if err != nil {
		log.Fatalf("migration.NewClient: %v", err)
	}
	defer migClient.Close()

	workflow, err := executeTranslationWorkflow(ctx, migClient, *projectID, *location, *outputPath)
	if err != nil {
		log.Fatalf("workflow execution failed: %v\n", err)
	}

	reportWorkflowStatus(workflow)
}

// executeTranslationWorkflow constructs a migration workflow that performs batch SQL translation.
func executeTranslationWorkflow(ctx context.Context, client *migration.Client, projectID, location, outPath string) (*migrationpb.MigrationWorkflow, error) {

	// Construct the workflow creation request.  In this workflow, we have only a single translation task present.
	req := &migrationpb.CreateMigrationWorkflowRequest{
		Parent: fmt.Sprintf("projects/%s/locations/%s", projectID, location),
		MigrationWorkflow: &migrationpb.MigrationWorkflow{
			DisplayName: "example SQL conversion",
			Tasks: map[string]*migrationpb.MigrationTask{
				"example_conversion": {
					Type: "Translation_Teradata2BQ",
					TaskDetails: &migrationpb.MigrationTask_TranslationConfigDetails{
						TranslationConfigDetails: &migrationpb.TranslationConfigDetails{
							SourceLocation: &migrationpb.TranslationConfigDetails_GcsSourcePath{
								GcsSourcePath: "gs://cloud-samples-data/bigquery/migration/translation/input/",
							},
							TargetLocation: &migrationpb.TranslationConfigDetails_GcsTargetPath{
								GcsTargetPath: outPath,
							},
							SourceDialect: &migrationpb.Dialect{
								DialectValue: &migrationpb.Dialect_TeradataDialect{
									TeradataDialect: &migrationpb.TeradataDialect{
										Mode: migrationpb.TeradataDialect_SQL,
									},
								},
							},
							TargetDialect: &migrationpb.Dialect{
								DialectValue: &migrationpb.Dialect_BigqueryDialect{},
							},
						},
					},
				},
			},
		},
	}

	// Create the workflow using the request.
	workflow, err := client.CreateMigrationWorkflow(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("CreateMigrationWorkflow: %w", err)
	}
	fmt.Printf("workflow created: %s", workflow.GetName())

	// This is an asyncronous process, so we now poll the workflow
	// until completion or a suitable timeout has elapsed.
	timeoutCtx, cancel := context.WithTimeout(ctx, 5*time.Minute)
	defer cancel()
	for {
		select {
		case <-timeoutCtx.Done():
			return nil, fmt.Errorf("task %s didn't complete due to context expiring", workflow.GetName())
		default:
			polledWorkflow, err := client.GetMigrationWorkflow(timeoutCtx, &migrationpb.GetMigrationWorkflowRequest{
				Name: workflow.GetName(),
			})
			if err != nil {
				return nil, fmt.Errorf("polling ended in error: %w", err)
			}
			if polledWorkflow.GetState() == migrationpb.MigrationWorkflow_COMPLETED {
				// polledWorkflow contains the most recent metadata about the workflow, so we return that.
				return polledWorkflow, nil
			}
			// workflow still isn't complete, so sleep briefly before polling again.
			time.Sleep(5 * time.Second)
		}
	}
}

// reportWorkflowStatus prints information about the workflow execution in a more human readable format.
func reportWorkflowStatus(workflow *migrationpb.MigrationWorkflow) {
	fmt.Printf("Migration workflow %s ended in state %s.\n", workflow.GetName(), workflow.GetState().String())
	for k, task := range workflow.GetTasks() {
		fmt.Printf(" - Task %s had id %s", k, task.GetId())
		if task.GetProcessingError() != nil {
			fmt.Printf(" with processing error: %s", task.GetProcessingError().GetReason())
		}
		fmt.Println()
	}
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquerymigration&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]