Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BigQuery 用戶端程式庫查詢公開資料集

瞭解如何使用 BigQuery 用戶端程式庫查詢公開資料集。

---

如要直接在Google Cloud 控制台中，按照這項工作的逐步指南操作，請選取偏好的程式設計語言：

### C#

[參加 C# 導覽](https://console.cloud.google.com/?walkthrough_id=bigquery--csharp-client-library&hl=zh-tw)

### Go

[參加 Go 導覽](https://console.cloud.google.com/?walkthrough_id=bigquery--go-client-library&hl=zh-tw)

### Java

[參加 Java 導覽](https://console.cloud.google.com/?walkthrough_id=bigquery--java-client-library&hl=zh-tw)

### Node.js

[參加 Node.js 導覽](https://console.cloud.google.com/?walkthrough_id=bigquery--node-client-library&hl=zh-tw)

### PHP

[參加 PHP 導覽](https://console.cloud.google.com/?walkthrough_id=bigquery--php-client-library&hl=zh-tw)

### Python

[參加 Python 導覽](https://console.cloud.google.com/?walkthrough_id=bigquery--python-client-library&hl=zh-tw)

### Ruby

[參加 Ruby 導覽](https://console.cloud.google.com/?walkthrough_id=bigquery--ruby-client-library&hl=zh-tw)

---

## 事前準備

1. [建立或選取 Google Cloud 專案](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw)。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。
   * 建立 Google Cloud 專案：

     ```
     gcloud projects create PROJECT_ID
     ```

     將 `PROJECT_ID` 替換為您要建立的 Google Cloud 專案名稱。
   * 選取您建立的 Google Cloud 專案：

     ```
     gcloud config set project PROJECT_ID
     ```

     將 `PROJECT_ID` 替換為 Google Cloud 專案名稱。
2. 選擇[免付費使用 BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)，或[為專案啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw)。 Google Cloud

   如果專案未啟用計費功能，會自動前往 BigQuery 沙箱讓您執行操作。沙箱可供您免付費使用部分 BigQuery 功能，協助熟悉 BigQuery。如果您只打算將專案用於本文練習，建議使用 BigQuery 沙箱。
3. 將角色授予使用者帳戶。針對下列每個 IAM 角色，執行一次下列指令：
   `roles/serviceusage.serviceUsageAdmin, roles/bigquery.jobUser`

   ```
   gcloud projects add-iam-policy-binding PROJECT_ID --member="user:USER_IDENTIFIER" --role=ROLE
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID。
   * `USER_IDENTIFIER`：使用者帳戶的 ID。 例如：`myemail@example.com`。
   * `ROLE`：授予使用者帳戶的 IAM 角色。
4. 啟用 BigQuery API：

   **啟用 API 時所需的角色**

   如要啟用 API，您需要具備服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   ```
   gcloud services enable bigquery
   ```

   新專案會自動啟用 BigQuery API。
5. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)
6. 在 Cloud Shell 中啟用 Google Cloud 專案：

   ```
   gcloud config set project PROJECT_ID
   ```

   將 PROJECT\_ID 替換為您為本逐步導覽選取的專案。

   輸出結果會與下列內容相似：

   ```
   Updated property [core/project].
   ```

## 查詢公開資料集

選取下列其中一種語言：

### C#

1. 在 Cloud Shell 中，建立新的 C# 專案和檔案：

   ```
   dotnet new console -n BigQueryCsharpDemo
   ```

   輸出結果大致如下。為簡化輸出結果，這裡省略了幾行內容。

   ```
   Welcome to .NET 6.0!
   ---------------------
   SDK Version: 6.0.407
   ...
   The template "Console App" was created successfully.
   ...
   ```

   這個指令會建立名為 `BigQueryCsharpDemo` 的 C# 專案和 `Program.cs` 檔案。
2. 開啟 Cloud Shell 編輯器：

   ```
   cloudshell workspace BigQueryCsharpDemo
   ```
3. 接著要在 Cloud Shell 編輯器中開啟終端機，請點選「Open Terminal」(開啟終端機)。
4. 開啟專案目錄：

   ```
   cd BigQueryCsharpDemo
   ```
5. 安裝 C# 專用的 BigQuery 用戶端程式庫：

   ```
   dotnet add package Google.Cloud.BigQuery.V2
   ```

   輸出結果大致如下。為簡化輸出結果，這裡省略了幾行內容。

   ```
   Determining projects to restore...
   Writing /tmp/tmpF7EKSd.tmp
   ...
   info : Writing assets file to disk.
   ...
   ```
6. 將變數 `GOOGLE_PROJECT_ID` 設成 `GOOGLE_CLOUD_PROJECT` 這個值，然後匯出變數：

   ```
   export GOOGLE_PROJECT_ID=$GOOGLE_CLOUD_PROJECT
   ```
7. 點選「Open Editor」(開啟編輯器)。
8. 在「Explorer」窗格中，找出 `BIGQUERYCSHARPDEMO` 專案。
9. 點選 `Program.cs` 檔案即可開啟。
10. 如要依據 `bigquery-public-data.stackoverflow` 資料集建立查詢，讓系統傳回瀏覽量最高的前 10 個 Stack Overflow 頁面和相應瀏覽次數，請將檔案內容改成下列程式碼：

    ```
    using System;
    using Google.Cloud.BigQuery.V2;

    namespace GoogleCloudSamples
    {
        public class Program
        {
            public static void Main(string[] args)
            {
                string projectId = Environment.GetEnvironmentVariable("GOOGLE_PROJECT_ID");
                var client = BigQueryClient.Create(projectId);
                string query = @"SELECT
                    CONCAT(
                        'https://stackoverflow.com/questions/',
                        CAST(id as STRING)) as url, view_count
                    FROM `bigquery-public-data.stackoverflow.posts_questions`
                    WHERE tags like '%google-bigquery%'
                    ORDER BY view_count DESC
                    LIMIT 10";
                var result = client.ExecuteQuery(query, parameters: null);
                Console.Write("\nQuery Results:\n------------\n");
                foreach (var row in result)
                {
                    Console.WriteLine($"{row["url"]}: {row["view_count"]} views");
                }
            }
        }
    }
    ```
11. 點選「Open Terminal」(開啟終端機)。
12. 在終端機中執行 `Program.cs` 指令碼。如果系統提示您授權 Cloud Shell 並同意條款，請按一下「Authorize」(授權)。

    ```
    dotnet run
    ```

    結果大致如下：

    ```
    Query Results:
    ------------
    https://stackoverflow.com/questions/35159967: 170023 views
    https://stackoverflow.com/questions/22879669: 142581 views
    https://stackoverflow.com/questions/10604135: 132406 views
    https://stackoverflow.com/questions/44564887: 128781 views
    https://stackoverflow.com/questions/27060396: 127008 views
    https://stackoverflow.com/questions/12482637: 120766 views
    https://stackoverflow.com/questions/20673986: 115720 views
    https://stackoverflow.com/questions/39109817: 108368 views
    https://stackoverflow.com/questions/11057219: 105175 views
    https://stackoverflow.com/questions/43195143: 101878 views
    ```

您已成功使用 BigQuery C# 用戶端程式庫查詢公開資料集。

### Go

1. 在 Cloud Shell 中，建立新的 Go 專案和檔案：

   ```
   mkdir bigquery-go-quickstart \
       && touch \
       bigquery-go-quickstart/app.go
   ```

   這個指令會建立名為 `bigquery-go-quickstart` 的 Go 專案及名為 `app.go` 的檔案。
2. 開啟 Cloud Shell 編輯器：

   ```
   cloudshell workspace bigquery-go-quickstart
   ```
3. 接著要在 Cloud Shell 編輯器中開啟終端機，請點選「Open Terminal」(開啟終端機)。
4. 開啟專案目錄：

   ```
   cd bigquery-go-quickstart
   ```
5. 建立 `go.mod` 檔案：

   ```
   go mod init quickstart
   ```

   輸出結果會與下列內容相似：

   ```
   go: creating new go.mod: module quickstart
   go: to add module requirements and sums:
           go mod tidy
   ```
6. 安裝 Go 專用的 BigQuery 用戶端程式庫：

   ```
   go get cloud.google.com/go/bigquery
   ```

   輸出結果會與下列內容相似：為簡化輸出結果，這裡省略了幾行內容。

   ```
   go: downloading cloud.google.com/go/bigquery v1.49.0
   go: downloading cloud.google.com/go v0.110.0
   ...
   go: added cloud.google.com/go/bigquery v1.49.0
   go: added cloud.google.com/go v0.110.0
   ```
7. 點選「Open Editor」(開啟編輯器)。
8. 在「Explorer」窗格中，找出 `BIGQUERY-GO-QUICKSTART` 專案。
9. 點選 `app.go`，開啟這個檔案。
10. 接著請將下列程式碼複製到 `app.go` 檔案中，依據 `bigquery-public-data.stackoverflow` 資料集建立查詢，讓系統傳回瀏覽量最高的前 10 個 Stack Overflow 頁面和相應瀏覽次數：

    ```
    // Command simpleapp queries the Stack Overflow public dataset in Google BigQuery.
    package main

    import (
    	"context"
    	"fmt"
    	"io"
    	"log"
    	"os"

    	"cloud.google.com/go/bigquery"
    	"google.golang.org/api/iterator"
    )


    func main() {
    	projectID := os.Getenv("GOOGLE_CLOUD_PROJECT")
    	if projectID == "" {
    		fmt.Println("GOOGLE_CLOUD_PROJECT environment variable must be set.")
    		os.Exit(1)
    	}

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
    			CONCAT(
    				'https://stackoverflow.com/questions/',
    				CAST(id as STRING)) as url,
    			view_count
    		FROM ` + "`bigquery-public-data.stackoverflow.posts_questions`" + `
    		WHERE tags like '%google-bigquery%'
    		ORDER BY view_count DESC
    		LIMIT 10;`)
    	return query.Read(ctx)
    }

    type StackOverflowRow struct {
    	URL       string `bigquery:"url"`
    	ViewCount int64  `bigquery:"view_count"`
    }

    // printResults prints results from a query to the Stack Overflow public dataset.
    func printResults(w io.Writer, iter *bigquery.RowIterator) error {
    	for {
    		var row StackOverflowRow
    		err := iter.Next(&row)
    		if err == iterator.Done {
    			return nil
    		}
    		if err != nil {
    			return fmt.Errorf("error iterating through results: %w", err)
    		}

    		fmt.Fprintf(w, "url: %s views: %d\n", row.URL, row.ViewCount)
    	}
    }
    ```
11. 點選「Open Terminal」(開啟終端機)。
12. 在終端機中執行 `app.go` 指令碼。如果系統提示您授權 Cloud Shell 並同意條款，請按一下「Authorize」(授權)。

    ```
    go run app.go
    ```

    結果大致如下：

    ```
    https://stackoverflow.com/questions/35159967 : 170023 views
    https://stackoverflow.com/questions/22879669 : 142581 views
    https://stackoverflow.com/questions/10604135 : 132406 views
    https://stackoverflow.com/questions/44564887 : 128781 views
    https://stackoverflow.com/questions/27060396 : 127008 views
    https://stackoverflow.com/questions/12482637 : 120766 views
    https://stackoverflow.com/questions/20673986 : 115720 views
    https://stackoverflow.com/questions/39109817 : 108368 views
    https://stackoverflow.com/questions/11057219 : 105175 views
    https://stackoverflow.com/questions/43195143 : 101878 views
    ```

您已成功使用 BigQuery Go 用戶端程式庫查詢公開資料集。

### Java

1. 在 Cloud Shell 中，使用 Apache Maven 建立新的 Java 專案：

   ```
   mvn archetype:generate \
       -DgroupId=com.google.app \
       -DartifactId=bigquery-java-quickstart \
       -DinteractiveMode=false
   ```

   這個指令會建立名為 `bigquery-java-quickstart` 的 Maven 專案。

   輸出結果大致如下。為簡化輸出結果，這裡省略了幾行內容。

   ```
   [INFO] Scanning for projects...
   ...
   [INFO] Building Maven Stub Project (No POM) 1
   ...
   [INFO] BUILD SUCCESS
   ...
   ```

   除了 Maven，還有許多依附元件管理系統可以使用。如要進一步瞭解如何設定 Java 開發環境，以搭配用戶端程式庫使用，請參閱[這份說明文件](https://docs.cloud.google.com/java/docs/setup?hl=zh-tw)。
2. 重新命名 Maven 預設建立的 `App.java` 檔案：

   ```
   mv \
       bigquery-java-quickstart/src/main/java/com/google/app/App.java \
       bigquery-java-quickstart/src/main/java/com/google/app/SimpleApp.java
   ```
3. 開啟 Cloud Shell 編輯器：

   ```
   cloudshell workspace bigquery-java-quickstart
   ```
4. 如果出現提示，詢問是否要同步處理 Java 類別路徑或設定，請點選「Always」(一律)。

   若在本逐步操作說明課程中，未看到提示或未發生類別路徑相關錯誤，請按照下列步驟操作：

   1. 依序點選「File」>「Preferences」>「Open Settings (UI)」。
   2. 依序點選「Extensions」>「Java」。
   3. 捲動至「Configuration: Update Build Configuration」，然後選取「automatic」。
5. 在「Explorer」窗格中，找出 `BIGQUERY-JAVA-QUICKSTART` 專案。
6. 點開 `pom.xml` 檔案。
7. 找到 `<dependencies>` 標記，在現有依附元件的後方新增下列依附元件。請勿替換任何現有的依附元件。

   ```
   <dependency>
     <groupId>com.google.cloud</groupId>
     <artifactId>google-cloud-bigquery</artifactId>
   </dependency>
   ```
8. 在結尾標記 `</dependencies>` 的後面那行新增下列內容：

   ```
   <dependencyManagement>
     <dependencies>
       <dependency>
         <groupId>com.google.cloud</groupId>
         <artifactId>libraries-bom</artifactId>
         <version>26.1.5</version>
         <type>pom</type>
         <scope>import</scope>
       </dependency>
     </dependencies>
   </dependencyManagement>
   ```
9. 在「Explorer」窗格中，找到 `BIGQUERY-JAVA-QUICKSTART` 專案，然後依序點選「src」>「main/java/com/google/app」>「SimpleApp.java」。檔案會隨即開啟。
10. 如要針對 `bigquery-public-data.stackoverflow` 資料集建立查詢，請保留檔案的第一行 `package com.google.app;`，然後將其他內容改成下列程式碼：

    ```
    import com.google.cloud.bigquery.BigQuery;
    import com.google.cloud.bigquery.BigQueryException;
    import com.google.cloud.bigquery.BigQueryOptions;
    import com.google.cloud.bigquery.FieldValueList;
    import com.google.cloud.bigquery.Job;
    import com.google.cloud.bigquery.JobId;
    import com.google.cloud.bigquery.JobInfo;
    import com.google.cloud.bigquery.QueryJobConfiguration;
    import com.google.cloud.bigquery.TableResult;


    public class SimpleApp {

      public static void main(String... args) throws Exception {
        // TODO(developer): Replace these variables before running the app.
        String projectId = "MY_PROJECT_ID";
        simpleApp(projectId);
      }

      public static void simpleApp(String projectId) {
        try {
          BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();
          QueryJobConfiguration queryConfig =
              QueryJobConfiguration.newBuilder(
                      "SELECT CONCAT('https://stackoverflow.com/questions/', "
                          + "CAST(id as STRING)) as url, view_count "
                          + "FROM `bigquery-public-data.stackoverflow.posts_questions` "
                          + "WHERE tags like '%google-bigquery%' "
                          + "ORDER BY view_count DESC "
                          + "LIMIT 10")
                  // Use standard SQL syntax for queries.
                  // See: https://cloud.google.com/bigquery/sql-reference/
                  .setUseLegacySql(false)
                  .build();

          JobId jobId = JobId.newBuilder().setProject(projectId).build();
          Job queryJob = bigquery.create(JobInfo.newBuilder(queryConfig).setJobId(jobId).build());

          // Wait for the query to complete.
          queryJob = queryJob.waitFor();

          // Check for errors
          if (queryJob == null) {
            throw new RuntimeException("Job no longer exists");
          } else if (queryJob.getStatus().getExecutionErrors() != null
              && queryJob.getStatus().getExecutionErrors().size() > 0) {
            // TODO(developer): Handle errors here. An error here do not necessarily mean that the job
            // has completed or was unsuccessful.
            // For more details: https://cloud.google.com/bigquery/troubleshooting-errors
            throw new RuntimeException("An unhandled error has occurred");
          }

          // Get the results.
          TableResult result = queryJob.getQueryResults();

          // Print all pages of the results.
          for (FieldValueList row : result.iterateAll()) {
            // String type
            String url = row.get("url").getStringValue();
            String viewCount = row.get("view_count").getStringValue();
            System.out.printf("%s : %s views\n", url, viewCount);
          }
        } catch (BigQueryException | InterruptedException e) {
          System.out.println("Simple App failed due to error: \n" + e.toString());
        }
      }
    }
    ```

    此查詢會傳回前 10 個最常觀看的 Stack Overflow 頁面及其觀看次數。
11. 對「SimpleApp.java」按一下滑鼠右鍵，然後點選「Run Java」。如果系統提示您授權 Cloud Shell 並同意條款，請點選「Authorize」(授權)。

    結果大致如下：

    ```
    https://stackoverflow.com/questions/35159967 : 170023 views
    https://stackoverflow.com/questions/22879669 : 142581 views
    https://stackoverflow.com/questions/10604135 : 132406 views
    https://stackoverflow.com/questions/44564887 : 128781 views
    https://stackoverflow.com/questions/27060396 : 127008 views
    https://stackoverflow.com/questions/12482637 : 120766 views
    https://stackoverflow.com/questions/20673986 : 115720 views
    https://stackoverflow.com/questions/39109817 : 108368 views
    https://stackoverflow.com/questions/11057219 : 105175 views
    https://stackoverflow.com/questions/43195143 : 101878 views
    ```

您已成功使用 BigQuery Java 用戶端程式庫查詢公開資料集。

### Node.js

1. 在 Cloud Shell 中，建立新的 Node.js 專案和檔案：

   ```
   mkdir bigquery-node-quickstart \
       && touch \
       bigquery-node-quickstart/app.js
   ```

   以下指令會建立名為 `bigquery-node-quickstart` 的 Node.js 專案和 `app.js` 檔案。
2. 開啟 Cloud Shell 編輯器：

   ```
   cloudshell workspace bigquery-node-quickstart
   ```
3. 接著要在 Cloud Shell 編輯器中開啟終端機，請點選「Open Terminal」(開啟終端機)。
4. 開啟專案目錄：

   ```
   cd bigquery-node-quickstart
   ```
5. 安裝 Node.js 專用的 BigQuery 用戶端程式庫：

   ```
   npm install @google-cloud/bigquery
   ```

   輸出結果會與下列內容相似：

   ```
   added 63 packages in 2s
   ```
6. 點選「Open Editor」(開啟編輯器)。
7. 在「Explorer」窗格中，找出 `BIGQUERY-NODE-QUICKSTART` 專案。
8. 點選 `app.js`，開啟這個檔案。
9. 接著請將下列程式碼複製到 `app.js` 檔案中，依據 `bigquery-public-data.stackoverflow` 資料集建立查詢，讓系統傳回瀏覽量最高的前 10 個 Stack Overflow 頁面和相應瀏覽次數：

   ```
   // Import the Google Cloud client library
   const {BigQuery} = require('@google-cloud/bigquery');

   async function queryStackOverflow() {
     // Queries a public Stack Overflow dataset.

     // Create a client
     const bigqueryClient = new BigQuery();

     // The SQL query to run
     const sqlQuery = `SELECT
       CONCAT(
         'https://stackoverflow.com/questions/',
         CAST(id as STRING)) as url,
       view_count
       FROM \`bigquery-public-data.stackoverflow.posts_questions\`
       WHERE tags like '%google-bigquery%'
       ORDER BY view_count DESC
       LIMIT 10`;

     const options = {
       query: sqlQuery,
       // Location must match that of the dataset(s) referenced in the query.
       location: 'US',
     };

     // Run the query
     const [rows] = await bigqueryClient.query(options);

     console.log('Query Results:');
     rows.forEach(row => {
       const url = row['url'];
       const viewCount = row['view_count'];
       console.log(`url: ${url}, ${viewCount} views`);
     });
   }
   queryStackOverflow();
   ```
10. 點選「Open Terminal」(開啟終端機)。
11. 在終端機中執行 `app.js` 指令碼。如果系統提示您授權 Cloud Shell 並同意條款，請按一下「Authorize」(授權)。

    ```
    node app.js
    ```

    結果大致如下：

    ```
    Query Results:
    url: https://stackoverflow.com/questions/35159967, 170023 views
    url: https://stackoverflow.com/questions/22879669, 142581 views
    url: https://stackoverflow.com/questions/10604135, 132406 views
    url: https://stackoverflow.com/questions/44564887, 128781 views
    url: https://stackoverflow.com/questions/27060396, 127008 views
    url: https://stackoverflow.com/questions/12482637, 120766 views
    url: https://stackoverflow.com/questions/20673986, 115720 views
    url: https://stackoverflow.com/questions/39109817, 108368 views
    url: https://stackoverflow.com/questions/11057219, 105175 views
    url: https://stackoverflow.com/questions/43195143, 101878 views
    ```

您已成功使用 BigQuery Node.js 用戶端程式庫查詢公開資料集。

### PHP

1. 在 Cloud Shell 中，建立新的 PHP 專案和檔案：

   ```
   mkdir bigquery-php-quickstart \
       && touch \
       bigquery-php-quickstart/app.php
   ```

   這個指令會建立名為 `bigquery-php-quickstart` 的 PHP 專案和 `app.php` 檔案。
2. 開啟 Cloud Shell 編輯器：

   ```
   cloudshell workspace bigquery-php-quickstart
   ```
3. 接著要在 Cloud Shell 編輯器中開啟終端機，請點選「Open Terminal」(開啟終端機)。
4. 開啟專案目錄：

   ```
   cd bigquery-php-quickstart
   ```
5. 安裝 PHP 專用的 BigQuery 用戶端程式庫：

   ```
   composer require google/cloud-bigquery
   ```

   輸出內容大致如下。為簡化輸出結果，這裡省略了幾行內容。

   ```
   Running composer update google/cloud-bigquery
   Loading composer repositories with package information
   Updating dependencies
   ...
   No security vulnerability advisories found
   Using version ^1.24 for google/cloud-bigquery
   ```
6. 點選「Open Editor」(開啟編輯器)。
7. 在「Explorer」窗格中，找出 `BIGQUERY-PHP-QUICKSTART` 專案。
8. 點選 `app.php`，開啟這個檔案。
9. 接著請將下列程式碼複製到 `app.php` 檔案中，依據 `bigquery-public-data.stackoverflow` 資料集建立查詢，讓系統傳回瀏覽量最高的前 10 個 Stack Overflow 頁面和相應瀏覽次數：

   ```
   <?php
   # ...

   require __DIR__ . '/vendor/autoload.php';

   use Google\Cloud\BigQuery\BigQueryClient;


   $bigQuery = new BigQueryClient();
   $query = <<<ENDSQL
   SELECT
     CONCAT(
       'https://stackoverflow.com/questions/',
       CAST(id as STRING)) as url,
     view_count
   FROM `bigquery-public-data.stackoverflow.posts_questions`
   WHERE tags like '%google-bigquery%'
   ORDER BY view_count DESC
   LIMIT 10;
   ENDSQL;
   $queryJobConfig = $bigQuery->query($query);
   $queryResults = $bigQuery->runQuery($queryJobConfig);

   if ($queryResults->isComplete()) {
       $i = 0;
       $rows = $queryResults->rows();
       foreach ($rows as $row) {
           printf('--- Row %s ---' . PHP_EOL, ++$i);
           printf('url: %s, %s views' . PHP_EOL, $row['url'], $row['view_count']);
       }
       printf('Found %s row(s)' . PHP_EOL, $i);
   } else {
       throw new Exception('The query failed to complete');
   }
   ```
10. 點選「Open Terminal」(開啟終端機)。
11. 在終端機中執行 `app.php` 指令碼。如果系統提示您授權 Cloud Shell 並同意條款，請按一下「Authorize」(授權)。

    ```
    php app.php
    ```

    結果大致如下：

    ```
    --- Row 1 ---
    url: https://stackoverflow.com/questions/35159967, 170023 views
    --- Row 2 ---
    url: https://stackoverflow.com/questions/22879669, 142581 views
    --- Row 3 ---
    url: https://stackoverflow.com/questions/10604135, 132406 views
    --- Row 4 ---
    url: https://stackoverflow.com/questions/44564887, 128781 views
    --- Row 5 ---
    url: https://stackoverflow.com/questions/27060396, 127008 views
    --- Row 6 ---
    url: https://stackoverflow.com/questions/12482637, 120766 views
    --- Row 7 ---
    url: https://stackoverflow.com/questions/20673986, 115720 views
    --- Row 8 ---
    url: https://stackoverflow.com/questions/39109817, 108368 views
    --- Row 9 ---
    url: https://stackoverflow.com/questions/11057219, 105175 views
    --- Row 10 ---
    url: https://stackoverflow.com/questions/43195143, 101878 views
    Found 10 row(s)
    ```

您已成功使用 BigQuery PHP 用戶端程式庫查詢公開資料集。

### Python

1. 在 Cloud Shell 中，建立新的 Python 專案和檔案：

   ```
   mkdir bigquery-python-quickstart \
       && touch \
       bigquery-python-quickstart/app.py
   ```

   這個指令會建立名為 `bigquery-python-quickstart` 的 Python 專案和 `app.py` 檔案。
2. 開啟 Cloud Shell 編輯器：

   ```
   cloudshell workspace bigquery-python-quickstart
   ```
3. 接著要在 Cloud Shell 編輯器中開啟終端機，請點選「Open Terminal」(開啟終端機)。
4. 開啟專案目錄：

   ```
   cd bigquery-python-quickstart
   ```
5. 安裝 Python 專用的 BigQuery 用戶端程式庫：

   ```
   pip install --upgrade google-cloud-bigquery
   ```

   輸出內容大致如下：為簡化輸出結果，這裡省略了幾行內容。

   ```
   Installing collected packages: google-cloud-bigquery
   ...
   Successfully installed google-cloud-bigquery-3.9.0
   ...
   ```
6. 點選「Open Editor」(開啟編輯器)。
7. 在「Explorer」窗格中，找出 `BIGQUERY-PYTHON-QUICKSTART` 專案。
8. 點選 `app.py`，開啟這個檔案。
9. 接著請將下列程式碼複製到 `app.py` 檔案中，依據 `bigquery-public-data.stackoverflow` 資料集建立查詢，讓系統傳回瀏覽量最高的前 10 個 Stack Overflow 頁面和相應瀏覽次數：

   ```
   from google.cloud import bigquery



   def query_stackoverflow() -> None:
       client = bigquery.Client()
       results = client.query_and_wait(
           """
           SELECT
             CONCAT(
               'https://stackoverflow.com/questions/',
               CAST(id as STRING)) as url,
             view_count
           FROM `bigquery-public-data.stackoverflow.posts_questions`
           WHERE tags like '%google-bigquery%'
           ORDER BY view_count DESC
           LIMIT 10"""
       )  # Waits for job to complete.

       for row in results:
           print("{} : {} views".format(row.url, row.view_count))


   if __name__ == "__main__":
       query_stackoverflow()
   ```
10. 點選「Open Terminal」(開啟終端機)。
11. 在終端機中執行 `app.py` 指令碼。如果系統提示您授權 Cloud Shell 並同意條款，請按一下「Authorize」(授權)。

    ```
    python app.py
    ```

    結果大致如下：

    ```
    https://stackoverflow.com/questions/35159967 : 170023 views
    https://stackoverflow.com/questions/22879669 : 142581 views
    https://stackoverflow.com/questions/10604135 : 132406 views
    https://stackoverflow.com/questions/44564887 : 128781 views
    https://stackoverflow.com/questions/27060396 : 127008 views
    https://stackoverflow.com/questions/12482637 : 120766 views
    https://stackoverflow.com/questions/20673986 : 115720 views
    https://stackoverflow.com/questions/39109817 : 108368 views
    https://stackoverflow.com/questions/11057219 : 105175 views
    https://stackoverflow.com/questions/43195143 : 101878 views
    ```

您已成功使用 BigQuery Python 用戶端程式庫查詢公開資料集。

### Ruby

1. 在 Cloud Shell 中，建立新的 Ruby 專案和檔案：

   ```
   mkdir bigquery-ruby-quickstart \
       && touch \
       bigquery-ruby-quickstart/app.rb
   ```

   這個指令會建立名為 `bigquery-ruby-quickstart` 的 Ruby 專案和 `app.rb` 檔案。
2. 開啟 Cloud Shell 編輯器：

   ```
   cloudshell workspace bigquery-ruby-quickstart
   ```
3. 接著要在 Cloud Shell 編輯器中開啟終端機，請點選「Open Terminal」(開啟終端機)。
4. 開啟專案目錄：

   ```
   cd bigquery-ruby-quickstart
   ```
5. 安裝 Ruby 專用的 BigQuery 用戶端程式庫：

   ```
   gem install google-cloud-bigquery
   ```

   輸出內容會類似如下。為簡化輸出結果，這裡省略了幾行內容。

   ```
   23 gems installed
   ```
6. 點選「Open Editor」(開啟編輯器)。
7. 在「Explorer」窗格中，找出 `BIGQUERY-RUBY-QUICKSTART` 專案。
8. 點選 `app.rb`，開啟這個檔案。
9. 接著請將下列程式碼複製到 `app.rb` 檔案中，依據 `bigquery-public-data.stackoverflow` 資料集建立查詢，讓系統傳回瀏覽量最高的前 10 個 Stack Overflow 頁面和相應瀏覽次數：

   ```
   require "google/cloud/bigquery"

   # This uses Application Default Credentials to authenticate.
   # @see https://cloud.google.com/bigquery/docs/authentication/getting-started
   bigquery = Google::Cloud::Bigquery.new

   sql     = "SELECT " \
             "CONCAT('https://stackoverflow.com/questions/', CAST(id as STRING)) as url, view_count " \
             "FROM `bigquery-public-data.stackoverflow.posts_questions` " \
             "WHERE tags like '%google-bigquery%' " \
             "ORDER BY view_count DESC LIMIT 10"
   results = bigquery.query sql

   results.each do |row|
     puts "#{row[:url]}: #{row[:view_count]} views"
   end
   ```
10. 點選「Open Terminal」(開啟終端機)。
11. 在終端機中執行 `app.rb` 指令碼。如果系統提示您授權 Cloud Shell 並同意條款，請按一下「Authorize」(授權)。

    ```
    ruby app.rb
    ```

    結果大致如下：

    ```
    https://stackoverflow.com/questions/35159967: 170023 views
    https://stackoverflow.com/questions/22879669: 142581 views
    https://stackoverflow.com/questions/10604135: 132406 views
    https://stackoverflow.com/questions/44564887: 128781 views
    https://stackoverflow.com/questions/27060396: 127008 views
    https://stackoverflow.com/questions/12482637: 120766 views
    https://stackoverflow.com/questions/20673986: 115720 views
    https://stackoverflow.com/questions/39109817: 108368 views
    https://stackoverflow.com/questions/11057219: 105175 views
    https://stackoverflow.com/questions/43195143: 101878 views
    ```

您已成功使用 BigQuery Ruby 用戶端程式庫查詢公開資料集。

## 清除所用資源

如要避免系統向您的 Google Cloud 帳戶收費，請刪除 Google Cloud 專案，或刪除您在本逐步操作說明課程中建立的資源。

### 刪除專案

如要避免付費，最簡單的方法就是刪除您為了本教學課程所建立的專案。

刪除專案的方法如下：

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### 刪除資源

如果使用現有專案，請刪除稍早建立的資源：

### C#

1. 在 Cloud Shell 中，移至上一層目錄：

   ```
   cd ..
   ```
2. 刪除您建立的 `BigQueryCsharpDemo` 資料夾：

   ```
   rm -R BigQueryCsharpDemo
   ```

   `-R` 旗標會刪除資料夾中的所有資產。

### Go

1. 在 Cloud Shell 中，移至上一層目錄：

   ```
   cd ..
   ```
2. 刪除您建立的 `bigquery-go-quickstart` 資料夾：

   ```
   rm -R bigquery-go-quickstart
   ```

   `-R` 旗標會刪除資料夾中的所有資產。

### Java

1. 在 Cloud Shell 中，移至上一層目錄：

   ```
   cd ..
   ```
2. 刪除您建立的 `bigquery-java-quickstart` 資料夾：

   ```
   rm -R bigquery-java-quickstart
   ```

   `-R` 旗標會刪除資料夾中的所有資產。

### Node.js

1. 在 Cloud Shell 中，移至上一層目錄：

   ```
   cd ..
   ```
2. 刪除您建立的 `bigquery-node-quickstart` 資料夾：

   ```
   rm -R bigquery-node-quickstart
   ```

   `-R` 旗標會刪除資料夾中的所有資產。

### PHP

1. 在 Cloud Shell 中，移至上一層目錄：

   ```
   cd ..
   ```
2. 刪除您建立的 `bigquery-php-quickstart` 資料夾：

   ```
   rm -R bigquery-php-quickstart
   ```

   `-R` 旗標會刪除資料夾中的所有資產。

### Python

1. 在 Cloud Shell 中，移至上一層目錄：

   ```
   cd ..
   ```
2. 刪除您建立的 `bigquery-python-quickstart` 資料夾：

   ```
   rm -R bigquery-python-quickstart
   ```

   `-R` 旗標會刪除資料夾中的所有資產。

### Ruby

1. 在 Cloud Shell 中，移至上一層目錄：

   ```
   cd ..
   ```
2. 刪除您建立的 `bigquery-ruby-quickstart` 資料夾：

   ```
   rm -R bigquery-ruby-quickstart
   ```

   `-R` 旗標會刪除資料夾中的所有資產。

## 後續步驟

* 進一步瞭解如何使用 [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)。
* 進一步瞭解 [BigQuery 公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)。
* 瞭解如何[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)。
* 進一步瞭解如何[在 BigQuery 查詢資料](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)。
* 掌握 [BigQuery 最新消息](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)。
* 瞭解 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。
* 瞭解 [BigQuery 配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]