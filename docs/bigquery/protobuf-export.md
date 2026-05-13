Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將資料匯出為 Protobuf 欄

本文說明如何使用 BigQuery 使用者定義函式 (UDF)，將 BigQuery 資料匯出為通訊協定緩衝區 (Protobuf) 資料欄。

## 使用 Protobuf 資料欄的時機

BigQuery 提供多種內建函式，可格式化所選資料。其中一個做法是將多個資料欄值合併為單一 Protobuf 值，這麼做有以下優點：

* 物件類型安全。
* 與 JSON 相比，壓縮率更高，資料傳輸時間和成本也更低。
* 彈性，因為大多數程式設計語言都有處理 Protobuf 的程式庫。
* 從多個資料欄讀取及建構單一物件時，負擔較小。

雖然其他欄類型也能提供類型安全，但使用 Protobuf 欄可提供完整型別的物件，減少應用程式層或管道其他部分的工作量。

不過，以 Protobuf 欄匯出 BigQuery 資料時，有以下限制：

* 系統無法妥善建立 Protobuf 資料欄的索引或篩選資料。依據 Protobuf 欄的內容搜尋可能效果不佳。
* 以 Protobuf 格式排序資料可能很困難。

如果匯出工作流程受到這些限制，建議您考慮使用其他方法匯出 BigQuery 資料：

* 使用[排程查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)搭配 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/other-statements?hl=zh-tw#export_data_statement)，即可依日期或時間排序匯出的 BigQuery 資料，並排定定期匯出作業。BigQuery 支援將資料匯出為 Avro、CSV、JSON 和 Parquet 格式。
* 使用 [Dataflow](https://docs.cloud.google.com/dataflow/docs/overview?hl=zh-tw) 以 Avro 或 CSV 檔案格式匯出 BigQuery 資料。

## 必要的角色

如要取得將 BigQuery 資料匯出為 Protobuf 欄所需的權限，請要求系統管理員在專案中授予您下列 IAM 角色：

* 建立使用者定義函式：
  [BigQuery 資料編輯器](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
* 從 BigQuery 資料表匯出資料：
  [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 讀取及上傳檔案至 Cloud Storage：
  [Storage Object Creator](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectCreator)  (`roles/storage.objectCreator`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立 UDF

建立 UDF，將 BigQuery `STRUCT` 資料類型轉換為 Protobuf 欄：

1. 在指令列中，複製 `bigquery-utils.git` 存放區：

   ```
   git clone https://github.com/GoogleCloudPlatform/bigquery-utils.git
   ```
2. 前往 Protobuf 匯出資料夾：

   ```
   cd bigquery-utils/tools/protobuf_export
   ```
3. 使用 [`cp` 指令](https://man7.org/linux/man-pages/man1/cp.1.html)或作業系統的檔案瀏覽器，將 proto 檔案複製到 `./protos` 子資料夾。

   「`./protos`」資料夾中已有一個名為「`dummy.proto`」的範例 proto 檔案。
4. 從 GitHub 存放區安裝必要套件：

   ```
   npm install
   ```
5. 使用 webpack 組合套件：

   ```
   npx webpack --config webpack.config.js --stats-error-details
   ```
6. 在 `./dist` 子資料夾中找出 `pbwrapper.js` 檔案，然後[將檔案上傳至 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)。
7. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
8. 使用查詢編輯器建立名為 `toMyProtoMessage` 的 UDF，從現有的 BigQuery 資料表資料欄建構 Protobuf 資料欄：

   ```
   CREATE FUNCTION
     DATASET_ID.toMyProtoMessage(input STRUCT<INPUT_FIELDS>)
     RETURNS BYTES
       LANGUAGE js OPTIONS ( library=["gs://BUCKET_NAME/pbwrapper.js"]
   ) AS r"""
   let message = pbwrapper.setup("PROTO_PACKAGE.PROTO_MESSAGE")
   return pbwrapper.parse(message, input)
     """;
   ```

   更改下列內容：

   * `DATASET_ID`：要包含 UDF 的資料集 ID。
   * `INPUT_FIELDS`：用於 proto 檔案的 [proto 訊息類型](https://protobuf.dev/programming-guides/proto3/#simple)中的欄位，格式為 `field_name_1 field_type_1 [, field_name_2 field_type_2, ...]`。

     您必須將使用底線的任何訊息類型欄位，改為使用[駝峰式大小寫](https://en.wikipedia.org/wiki/Camel_case)。舉例來說，如果訊息類型如下所示，則輸入欄位值必須為 `itemId int64, itemDescription string`：

     ```
     message ThisMessage {
       int64 item_id = 1;
       string item_description = 2;
     }
     ```
   * `BUCKET_NAME`：包含 `pbwrapper.js` 檔案的 Cloud Storage bucket 名稱。
   * `PROTO_PACKAGE`：proto 檔案的[套件](https://protobuf.dev/programming-guides/proto3/#packages)。
   * `PROTO_MESSAGE`：proto 檔案的訊息類型。

   舉例來說，如果您使用提供的 `dummy.proto` 檔案，`CREATE FUNCTION` 陳述式會如下所示：

   ```
   CREATE OR REPLACE FUNCTION
     mydataset.toMyProtoMessage(input STRUCT<dummyField STRING>)
     RETURNS BYTES
       LANGUAGE js OPTIONS ( library=["gs://mybucket/pbwrapper.js"]
   ) AS r"""
   let message = pbwrapper.setup("dummypackage.DummyMessage")
   return pbwrapper.parse(message, input)
     """;
   ```

## 將資料欄格式設為 Protobuf 值

執行 `toMyProtoMessage` UDF，將 BigQuery 資料表欄格式化為 Protobuf 值：

```
  SELECT
    UDF_DATASET_ID.toMyProtoMessage(STRUCT(INPUT_COLUMNS)) AS protoResult
  FROM
    `PROJECT_ID.DATASET_ID.TABLE_NAME`
  LIMIT
    100;
```

更改下列內容：

* `UDF_DATASET_ID`：包含 UDF 的資料集 ID。
* `INPUT_COLUMNS`：要格式化為 Protobuf 值的資料欄名稱，格式為 `column_name_1 [, column_name_2, ...]`。
  資料欄可以是任何支援的[純量值型別](https://protobuf.dev/programming-guides/proto3/#scalar)或非純量型別，包括 `ARRAY` 和 `STRUCT`。輸入資料欄必須與 proto 訊息類型欄位的類型和數量相符。
* `PROJECT_ID`：包含表格的專案 ID。如果資料集位於目前專案中，您可以略過識別專案的步驟。
* `DATASET_ID`：包含表格的資料集 ID。
* `TABLE_NAME`：包含要格式化資料欄的資料表名稱。

舉例來說，如果您使用以 `dummy.proto` 為基礎的 `toMyProtoMessage` UDF，下列 `SELECT` 陳述式會正常運作：

```
SELECT
  mydataset.toMyProtoMessage(STRUCT(word)) AS protoResult
FROM
  `bigquery-public-data.samples.shakespeare`
LIMIT 100;
```

## 使用 Protobuf 值

以 Protobuf 格式匯出 BigQuery 資料後，您現在可以將資料做為完全型別的物件或結構體使用。

下列程式碼範例提供幾種處理或使用匯出資料的方式：

### Go

```
// package Main queries Google BigQuery.
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
	"google.golang.org/Protobuf/proto"

	pb "path/to/proto/file_proto"
)

const (
	projectID = "your-project-id"
)

// Row contains returned row data from bigquery.
type Row struct {
	RowKey string `bigquery:"RowKey"`
	Proto  []byte `bigquery:"ProtoResult"`
}

func main() {
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		log.Fatalf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	rows, err := query(ctx, client)
	if err != nil {
		log.Fatal(err)
	}
	if err := printResults(os.Stdout, rows); err != nil {
		log.Fatal(err)
	}
}

// query returns a row iterator suitable for reading query results.
func query(ctx context.Context, client *bigquery.Client) (*bigquery.RowIterator, error) {

	query := client.Query(
		`SELECT 
  concat(word, ":", corpus) as RowKey, 
  <dataset-id>.toMyProtoMessage(
    STRUCT(
      word, 
      CAST(word_count AS BIGNUMERIC)
    )
  ) AS ProtoResult 
FROM 
  ` + "` bigquery - public - data.samples.shakespeare `" + ` 
LIMIT 
  100;
`)
	return query.Read(ctx)
}

// printResults prints results from a query.
func printResults(w io.Writer, iter *bigquery.RowIterator) error {
	for {
		var row Row
		err := iter.Next(&row)
		if err == iterator.Done {
			return nil
		}
		if err != nil {
			return fmt.Errorf("error iterating through results: %w", err)
		}
		message := &pb.TestMessage{}
		if err = proto.Unmarshal(row.Proto, message); err != nil {
			return err
		}
		fmt.Fprintf(w, "rowKey: %s, message: %v\n", row.RowKey, message)
	}
}
```

### Java

```
package proto;

import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FieldValueList;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobId;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;
import path.to.proto.TestMessage;
import java.util.UUID;

/** Queries Google BigQuery */
public final class Main {
  public static void main(String[] args) throws Exception {
    String projectId = "your-project-id";
    BigQuery bigquery = BigQueryOptions.newBuilder().setProjectId(projectId).build().getService();

    QueryJobConfiguration queryConfig =
        QueryJobConfiguration.newBuilder(
                " SELECT "
                    + "concat(word , \":\",corpus) as RowKey,"
                    + "<dataset-id>.toMyProtoMessage(STRUCT(word, "
                    + "CAST(word_count AS BIGNUMERIC))) AS ProtoResult "
                    + "FROM "
                    + "`bigquery-public-data.samples.shakespeare` "
                    + "ORDER BY word_count DESC "
                    + "LIMIT 20")
            .setUseLegacySql(false)
            .build();

    // Create a job ID so that we can safely retry.
    JobId jobId = JobId.of(UUID.randomUUID().toString());
    Job queryJob = bigquery.create(JobInfo.newBuilder(queryConfig).setJobId(jobId).build());

    // Wait for the query to complete.
    queryJob = queryJob.waitFor();

    // Check for errors
    if (queryJob == null) {
      throw new RuntimeException("Job no longer exists");
    } else if (queryJob.getStatus().getError() != null) {
      // You can also look at queryJob.getStatus().getExecutionErrors() for all
      // errors, not just the latest one.
      throw new RuntimeException(queryJob.getStatus().getError().toString());
    }

    // Get the results.
    TableResult result = queryJob.getQueryResults();

    // Print all pages of the results.
    for (FieldValueList row : result.iterateAll()) {
      String key = row.get("RowKey").getStringValue();
      byte[] message = row.get("ProtoResult").getBytesValue();
      TestMessage testMessage = TestMessage.parseFrom(message);
      System.out.printf("rowKey: %s, message: %s\n", key, testMessage);
    }
  }
}
```

### Python

```
"""Queries Google BigQuery."""

from google.cloud import bigquery
from path.to.proto import awesome_pb2


def main():
  project_id = "your-project-id"
  client = bigquery.Client(project=project_id)
  query_job = client.query(query="""
               SELECT
			concat(word , ":",corpus) as RowKey,
			<dataset-id>.toMyProtoMessage(
			    STRUCT(
			      word, 
			      CAST(word_count AS BIGNUMERIC)
			    )
			  ) AS ProtoResult 
		FROM
				  `bigquery-public-data.samples.shakespeare`
		ORDER BY word_count DESC
		LIMIT 20
    """)
  rows = query_job.result()
  for row in rows:
    message = awesome_pb2.TestMessage()
    message.ParseFromString(row.get("ProtoResult"))
    print(
        "rowKey: {}, message: {}".format(row.get("RowKey"), message)
    )
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]