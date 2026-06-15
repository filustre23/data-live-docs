Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 串流插入複雜類型的資料 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

將各種 BigQuery 支援的資料類型插入資料表。

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
	"cloud.google.com/go/civil"
)

// ComplexType represents a complex row item
type ComplexType struct {
	Name         string                 `bigquery:"name"`
	Age          int                    `bigquery:"age"`
	School       []byte                 `bigquery:"school"`
	Location     bigquery.NullGeography `bigquery:"location"`
	Measurements []float64              `bigquery:"measurements"`
	DatesTime    DatesTime              `bigquery:"datesTime"`
}

// DatesTime shows different date/time representation
type DatesTime struct {
	Day        civil.Date     `bigquery:"day"`
	FirstTime  civil.DateTime `bigquery:"firstTime"`
	SecondTime civil.Time     `bigquery:"secondTime"`
	ThirdTime  time.Time      `bigquery:"thirdTime"`
}

// insertingDataTypes demonstrates inserting data into a table using the streaming insert mechanism.
func insertingDataTypes(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	// Manually defining schema
	schema := bigquery.Schema{
		{Name: "name", Type: bigquery.StringFieldType},
		{Name: "age", Type: bigquery.IntegerFieldType},
		{Name: "school", Type: bigquery.BytesFieldType},
		{Name: "location", Type: bigquery.GeographyFieldType},
		{Name: "measurements", Type: bigquery.FloatFieldType, Repeated: true},
		{Name: "datesTime", Type: bigquery.RecordFieldType, Schema: bigquery.Schema{
			{Name: "day", Type: bigquery.DateFieldType},
			{Name: "firstTime", Type: bigquery.DateTimeFieldType},
			{Name: "secondTime", Type: bigquery.TimeFieldType},
			{Name: "thirdTime", Type: bigquery.TimestampFieldType},
		}},
	}
	// Infer schema from struct
	// schema, err := bigquery.InferSchema(ComplexType{})

	table := client.Dataset(datasetID).Table(tableID)
	err = table.Create(ctx, &bigquery.TableMetadata{
		Schema: schema,
	})
	if err != nil {
		return fmt.Errorf("table.Create: %w", err)
	}
	day, err := civil.ParseDate("2019-01-12")
	if err != nil {
		return fmt.Errorf("civil.ParseDate: %w", err)
	}
	firstTime, err := civil.ParseDateTime("2019-02-17T11:24:00.000")
	if err != nil {
		return fmt.Errorf("civil.ParseDateTime: %w", err)
	}
	secondTime, err := civil.ParseTime("14:00:00")
	if err != nil {
		return fmt.Errorf("civil.ParseTime: %w", err)
	}
	thirdTime, err := time.Parse(time.RFC3339Nano, "2020-04-27T18:07:25.356Z")
	if err != nil {
		return fmt.Errorf("time.Parse: %w", err)
	}
	row := &ComplexType{
		Name:         "Tom",
		Age:          30,
		School:       []byte("Test University"),
		Location:     bigquery.NullGeography{GeographyVal: "POINT(1 2)", Valid: true},
		Measurements: []float64{50.05, 100.5},
		DatesTime: DatesTime{
			Day:        day,
			FirstTime:  firstTime,
			SecondTime: secondTime,
			ThirdTime:  thirdTime,
		},
	}
	rows := []*ComplexType{row}
	// Uncomment to simulate insert errors.
	// This example row is missing required fields.
	// badRow := &ComplexType{
	// 	Name: "John",
	// 	Age:  24,
	// }
	// rows = append(rows, badRow)

	inserter := table.Inserter()
	err = inserter.Put(ctx, rows)
	if err != nil {
		if multiErr, ok := err.(bigquery.PutMultiError); ok {
			for _, putErr := range multiErr {
				fmt.Printf("failed to insert row %d with err: %v \n", putErr.RowIndex, putErr.Error())
			}
		}
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryError;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.InsertAllRequest;
import com.google.cloud.bigquery.InsertAllResponse;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.StandardTableDefinition;
import com.google.cloud.bigquery.TableDefinition;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;
import java.util.Base64;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Sample to insert data types in a table
public class InsertingDataTypes {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    insertingDataTypes(datasetName, tableName);
  }

  public static void insertingDataTypes(String datasetName, String tableName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Inserting data types
      Field name = Field.of("name", StandardSQLTypeName.STRING);
      Field age = Field.of("age", StandardSQLTypeName.INT64);
      Field school = Field.of("school", StandardSQLTypeName.BYTES);
      Field location = Field.of("location", StandardSQLTypeName.GEOGRAPHY);
      Field measurements =
          Field.newBuilder("measurements", StandardSQLTypeName.FLOAT64)
              .setMode(Field.Mode.REPEATED)
              .build();
      Field day = Field.of("day", StandardSQLTypeName.DATE);
      Field firstTime = Field.of("firstTime", StandardSQLTypeName.DATETIME);
      Field secondTime = Field.of("secondTime", StandardSQLTypeName.TIME);
      Field thirdTime = Field.of("thirdTime", StandardSQLTypeName.TIMESTAMP);
      Field datesTime =
          Field.of("datesTime", StandardSQLTypeName.STRUCT, day, firstTime, secondTime, thirdTime);
      Schema schema = Schema.of(name, age, school, location, measurements, datesTime);

      TableId tableId = TableId.of(datasetName, tableName);
      TableDefinition tableDefinition = StandardTableDefinition.of(schema);
      TableInfo tableInfo = TableInfo.newBuilder(tableId, tableDefinition).build();

      bigquery.create(tableInfo);

      // Inserting Sample data
      Map<String, Object> datesTimeContent = new HashMap<>();
      datesTimeContent.put("day", "2019-1-12");
      datesTimeContent.put("firstTime", "2019-02-17 11:24:00.000");
      datesTimeContent.put("secondTime", "14:00:00");
      datesTimeContent.put("thirdTime", "2020-04-27T18:07:25.356Z");

      Map<String, Object> rowContent = new HashMap<>();
      rowContent.put("name", "Tom");
      rowContent.put("age", 30);
      rowContent.put("school", Base64.getEncoder().encodeToString("Test University".getBytes()));
      rowContent.put("location", "POINT(1 2)");
      rowContent.put("measurements", new Float[] {50.05f, 100.5f});
      rowContent.put("datesTime", datesTimeContent);

      InsertAllResponse response =
          bigquery.insertAll(InsertAllRequest.newBuilder(tableId).addRow(rowContent).build());

      if (response.hasErrors()) {
        // If any of the insertions failed, this lets you inspect the errors
        for (Map.Entry<Long, List<BigQueryError>> entry : response.getInsertErrors().entrySet()) {
          System.out.println("Response error: \n" + entry.getValue());
        }
      }
      System.out.println("Rows successfully inserted into table");
    } catch (BigQueryException e) {
      System.out.println("Insert operation not performed \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function insertingDataTypes() {
  // Inserts data of various BigQuery-supported types into a table.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  // Describe the schema of the table
  // For more information on supported data types, see
  // https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
  const schema = [
    {
      name: 'name',
      type: 'STRING',
    },
    {
      name: 'age',
      type: 'INTEGER',
    },
    {
      name: 'school',
      type: 'BYTES',
    },
    {
      name: 'metadata',
      type: 'JSON',
    },
    {
      name: 'location',
      type: 'GEOGRAPHY',
    },
    {
      name: 'measurements',
      mode: 'REPEATED',
      type: 'FLOAT',
    },
    {
      name: 'datesTimes',
      type: 'RECORD',
      fields: [
        {
          name: 'day',
          type: 'DATE',
        },
        {
          name: 'firstTime',
          type: 'DATETIME',
        },
        {
          name: 'secondTime',
          type: 'TIME',
        },
        {
          name: 'thirdTime',
          type: 'TIMESTAMP',
        },
      ],
    },
  ];

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
  const options = {
    schema: schema,
  };

  // Create a new table in the dataset
  const [table] = await bigquery
    .dataset(datasetId)
    .createTable(tableId, options);

  console.log(`Table ${table.id} created.`);

  // The DATE type represents a logical calendar date, independent of time zone.
  // A DATE value does not represent a specific 24-hour time period.
  // Rather, a given DATE value represents a different 24-hour period when
  // interpreted in different time zones, and may represent a shorter or longer
  // day during Daylight Savings Time transitions.
  const bqDate = bigquery.date('2019-1-12');
  // A DATETIME object represents a date and time, as they might be
  // displayed on a calendar or clock, independent of time zone.
  const bqDatetime = bigquery.datetime('2019-02-17 11:24:00.000');
  // A TIME object represents a time, as might be displayed on a watch,
  // independent of a specific date and timezone.
  const bqTime = bigquery.time('14:00:00');
  // A TIMESTAMP object represents an absolute point in time,
  // independent of any time zone or convention such as Daylight
  // Savings Time with microsecond precision.
  const bqTimestamp = bigquery.timestamp('2020-04-27T18:07:25.356Z');
  const bqGeography = bigquery.geography('POINT(1 2)');
  const schoolBuffer = Buffer.from('Test University');
  // a JSON field needs to be converted to a string
  const metadata = JSON.stringify({
    owner: 'John Doe',
    contact: 'johndoe@example.com',
  });
  // Rows to be inserted into table
  const rows = [
    {
      name: 'Tom',
      age: '30',
      location: bqGeography,
      school: schoolBuffer,
      metadata: metadata,
      measurements: [50.05, 100.5],
      datesTimes: {
        day: bqDate,
        firstTime: bqDatetime,
        secondTime: bqTime,
        thirdTime: bqTimestamp,
      },
    },
    {
      name: 'Ada',
      age: '35',
      measurements: [30.08, 121.7],
    },
  ];

  // Insert data into table
  await bigquery.dataset(datasetId).table(tableId).insert(rows);

  console.log(`Inserted ${rows.length} rows`);
}
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"
require "base64"

##
# Inserts a row with various data types into a table.
#
# @param dataset_id [String] The ID of the dataset to create the table in.
# @param table_id   [String] The ID of the table to create.
def inserting_data_types dataset_id, table_id
  bigquery = Google::Cloud::Bigquery.new
  dataset = bigquery.dataset dataset_id
  table = dataset.table table_id

  # Create the table if it doesn't exist.
  unless table
    dataset.create_table table_id do |t|
      t.string "name"
      t.integer "age"
      t.bytes "school"
      t.geography "location"
      t.float "measurements", mode: :repeated
      t.record "datesTime" do |s|
        s.date "day"
        s.datetime "firstTime"
        s.time "secondTime"
        s.timestamp "thirdTime"
      end
    end
    table = dataset.table table_id
  end

  dates_time_content = {
    "day"        => "2019-1-12",
    "firstTime"  => "2019-02-17 11:24:00.000",
    "secondTime" => "14:00:00",
    "thirdTime"  => "2020-04-27T18:07:25.356Z"
  }

  row_content = {
    "name"         => "Tom",
    "age"          => 30,
    "school"       => Base64.strict_encode64("Test University"),
    "location"     => "POINT(1 2)",
    "measurements" => [50.05, 100.5],
    "datesTime"    => dates_time_content
  }

  response = table.insert [row_content]

  if response.success?
    puts "Rows successfully inserted into table"
  else
    puts "Insert operation not performed"
    response.insert_errors.each do |error|
      puts "Error: #{error.errors}"
    end
  end
end
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]