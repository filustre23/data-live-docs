Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過使用者帳戶驗證已安裝的應用程式

本指南說明當您的應用程式已安裝在使用者電腦上時，如何透過使用者帳戶進行驗證，取得 BigQuery API 存取權。

為確保應用程式只能存取使用者可用的 BigQuery 資料表，請藉由使用者憑證進行驗證。使用者憑證只能對使用者的 Google Cloud 專案執行查詢，而無法對應用程式的專案執行查詢。因此，系統僅會向使用者收取查詢費用，而非應用程式費用。

## 事前準備

1. [建立](https://console.cloud.google.com/projectcreate?hl=zh-tw)一個代表已安裝應用程式的 Google Cloud 專案。
2. 安裝 [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)。
3. 安裝驗證程式庫。

   ### Java

   如果您使用 Maven，請在 pom 檔案中加入下列依附元件。

   ```
   <dependency>
     <groupId>com.google.oauth-client</groupId>
     <artifactId>google-oauth-client-java6</artifactId>
     <version>1.31.0</version>
   </dependency>
   <dependency>
     <groupId>com.google.oauth-client</groupId>
     <artifactId>google-oauth-client-jetty</artifactId>
     <version>1.31.0</version>
   </dependency>
   ```

   ### Python

   安裝 [Google Auth 的 oauthlib 整合](https://github.com/googleapis/google-cloud-python/tree/main/packages/google-auth-oauthlib)。

   ```
   pip install --upgrade google-auth-oauthlib
   ```

   ### Node.js

   安裝 [Google Auth 的 oauthlib 整合](https://github.com/googleapis/google-auth-library-nodejs)。

   ```
   npm install google-auth-library  
   npm install readline-promise
   ```

## 設定用戶端憑證

使用以下按鈕選取專案並建立必要憑證。

Get Credentials (取得憑證)

### 手動建立憑證

1. 前往 Google Cloud 控制台的「憑證」[頁面](https://console.cloud.google.com/apis/credentials?hl=zh-tw)。
2. 填寫 [OAuth 同意畫面](https://console.cloud.google.com/apis/credentials/consent?hl=zh-tw)中的必填欄位。
3. 在[「Credentials」(憑證) 頁面](https://console.cloud.google.com/apis/credentials?hl=zh-tw)中，按一下 [Create credentials] (建立憑證) 按鈕。

   選擇 [OAuth client ID] (OAuth 用戶端 ID)。
4. 將應用程式類型設為「Desktop」(桌面)，然後按一下「Create」(建立)。
5. 點選 [Download JSON] (下載 JSON) 按鈕下載憑證。

   將憑證檔案儲存至 `client_secrets.json`。這個檔案必須與您的應用程式一同發布。

## 驗證及呼叫 API

1. 使用用戶端憑證執行 [OAuth 2.0 流程](https://developers.google.com/identity/protocols/OAuth2?hl=zh-tw)。

   ### Java

   ```
   import com.google.api.client.auth.oauth2.Credential;
   import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp;
   import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver;
   import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
   import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
   import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
   import com.google.api.client.json.JsonFactory;
   import com.google.api.client.json.jackson2.JacksonFactory;
   import com.google.api.client.util.store.FileDataStoreFactory;
   import com.google.api.gax.paging.Page;
   import com.google.auth.oauth2.GoogleCredentials;
   import com.google.auth.oauth2.UserCredentials;
   import com.google.cloud.bigquery.BigQuery;
   import com.google.cloud.bigquery.BigQueryException;
   import com.google.cloud.bigquery.BigQueryOptions;
   import com.google.cloud.bigquery.Dataset;
   import com.google.common.collect.ImmutableList;
   import java.io.File;
   import java.io.IOException;
   import java.io.InputStream;
   import java.io.InputStreamReader;
   import java.nio.file.Files;
   import java.nio.file.Path;
   import java.nio.file.Paths;
   import java.security.GeneralSecurityException;
   import java.util.List;

   // Sample to authenticate by using a user credential
   public class AuthUserFlow {

     private static final File DATA_STORE_DIR =
         new File(AuthUserFlow.class.getResource("/").getPath(), "credentials");
     private static final JsonFactory JSON_FACTORY = JacksonFactory.getDefaultInstance();
     // i.e redirect_uri http://localhost:61984/Callback
     private static final int LOCAL_RECEIVER_PORT = 61984;

     public static void runAuthUserFlow() {
       // TODO(developer): Replace these variables before running the sample.
       /**
        * Download your OAuth2 configuration from the Google Developers Console API Credentials page.
        * https://console.cloud.google.com/apis/credentials
        */
       Path credentialsPath = Paths.get("path/to/your/client_secret.json");
       List<String> scopes = ImmutableList.of("https://www.googleapis.com/auth/bigquery");
       authUserFlow(credentialsPath, scopes);
     }

     public static void authUserFlow(Path credentialsPath, List<String> selectedScopes) {
       // Reading credentials file
       try (InputStream inputStream = Files.newInputStream(credentialsPath)) {

         // Load client_secret.json file
         GoogleClientSecrets clientSecrets =
             GoogleClientSecrets.load(JSON_FACTORY, new InputStreamReader(inputStream));
         String clientId = clientSecrets.getDetails().getClientId();
         String clientSecret = clientSecrets.getDetails().getClientSecret();

         // Generate the url that will be used for the consent dialog.
         GoogleAuthorizationCodeFlow flow =
             new GoogleAuthorizationCodeFlow.Builder(
                     GoogleNetHttpTransport.newTrustedTransport(),
                     JSON_FACTORY,
                     clientSecrets,
                     selectedScopes)
                 .setDataStoreFactory(new FileDataStoreFactory(DATA_STORE_DIR))
                 .setAccessType("offline")
                 .setApprovalPrompt("auto")
                 .build();

         // Exchange an authorization code for  refresh token
         LocalServerReceiver receiver =
             new LocalServerReceiver.Builder().setPort(LOCAL_RECEIVER_PORT).build();
         Credential credential = new AuthorizationCodeInstalledApp(flow, receiver).authorize("user");

         // OAuth2 Credentials representing a user's identity and consent
         GoogleCredentials credentials =
             UserCredentials.newBuilder()
                 .setClientId(clientId)
                 .setClientSecret(clientSecret)
                 .setRefreshToken(credential.getRefreshToken())
                 .build();

         // Initialize client that will be used to send requests. This client only needs to be created
         // once, and can be reused for multiple requests.
         BigQuery bigquery =
             BigQueryOptions.newBuilder().setCredentials(credentials).build().getService();

         Page<Dataset> datasets = bigquery.listDatasets(BigQuery.DatasetListOption.pageSize(100));
         if (datasets == null) {
           System.out.println("Dataset does not contain any models");
           return;
         }
         datasets
             .iterateAll()
             .forEach(
                 dataset -> System.out.printf("Success! Dataset ID: %s ", dataset.getDatasetId()));

       } catch (BigQueryException | IOException | GeneralSecurityException ex) {
         System.out.println("Project does not contain any datasets \n" + ex.toString());
       }
     }
   }
   ```

   ### Python

   ```
   from google_auth_oauthlib import flow

   # A local server is used as the callback URL in the auth flow.
   appflow = flow.InstalledAppFlow.from_client_secrets_file(
       "client_secrets.json", scopes=["https://www.googleapis.com/auth/bigquery"]
   )

   # This launches a local server to be used as the callback URL in the desktop
   # app auth flow. If you are accessing the application remotely, such as over
   # SSH or a remote Jupyter notebook, this flow will not work. Use the
   # `gcloud auth application-default login --no-browser` command or workload
   # identity federation to get authentication tokens, instead.
   #
   appflow.run_local_server()

   credentials = appflow.credentials
   ```

   ### Node.js

   ```
   const {OAuth2Client} = require('google-auth-library');
   const readline = require('readline-promise').default;

   function startRl() {
     const rl = readline.createInterface({
       input: process.stdin,
       output: process.stdout,
     });

     return rl;
   }

   /**
    * Download your OAuth2 configuration from the Google
    * Developers Console API Credentials page.
    * https://console.cloud.google.com/apis/credentials
    */
   const keys = require('./oauth2.keys.json');

   /**
    * Create a new OAuth2Client, and go through the OAuth2 content
    * workflow. Return the full client to the callback.
    */
   async function getRedirectUrl() {
     const rl = main.startRl();
     // Create an oAuth client to authorize the API call.  Secrets are kept in a `keys.json` file,
     // which should be downloaded from the Google Developers Console.
     const oAuth2Client = new OAuth2Client(
       keys.installed.client_id,
       keys.installed.client_secret,
       keys.installed.redirect_uris[0]
     );

     // Generate the url that will be used for the consent dialog.
     const authorizeUrl = oAuth2Client.generateAuthUrl({
       access_type: 'offline',
       scope: 'https://www.googleapis.com/auth/bigquery',
       prompt: 'consent',
     });

     console.info(
       `Please visit this URL to authorize this application: ${authorizeUrl}`
     );

     const code = await rl.questionAsync('Enter the authorization code: ');
     const tokens = await main.exchangeCode(code);
     rl.close();

     return tokens;
   }

   // Exchange an authorization code for an access token
   async function exchangeCode(code) {
     const oAuth2Client = new OAuth2Client(
       keys.installed.client_id,
       keys.installed.client_secret,
       keys.installed.redirect_uris[0]
     );

     const r = await oAuth2Client.getToken(code);
     console.info(r.tokens);
     return r.tokens;
   }

   async function authFlow(projectId = 'project_id') {
     /**
      * TODO(developer):
      * Save Project ID as environment variable PROJECT_ID="project_id"
      * Uncomment the following line before running the sample.
      */
     // projectId = process.env.PROJECT_ID;

     const tokens = await main.getRedirectUrl();

     const credentials = {
       type: 'authorized_user',
       client_id: keys.installed.client_id,
       client_secret: keys.installed.client_secret,
       refresh_token: tokens.refresh_token,
     };

     return {
       projectId,
       credentials,
     };
   }
   ```
2. 使用驗證過的憑證連結至 BigQuery API。

   ### Java

   ```
   import com.google.api.client.auth.oauth2.Credential;
   import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp;
   import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver;
   import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
   import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
   import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
   import com.google.api.client.json.JsonFactory;
   import com.google.api.client.json.jackson2.JacksonFactory;
   import com.google.api.client.util.store.FileDataStoreFactory;
   import com.google.auth.oauth2.GoogleCredentials;
   import com.google.auth.oauth2.UserCredentials;
   import com.google.cloud.bigquery.BigQuery;
   import com.google.cloud.bigquery.BigQueryException;
   import com.google.cloud.bigquery.BigQueryOptions;
   import com.google.cloud.bigquery.QueryJobConfiguration;
   import com.google.cloud.bigquery.TableResult;
   import com.google.common.collect.ImmutableList;
   import java.io.File;
   import java.io.IOException;
   import java.io.InputStream;
   import java.io.InputStreamReader;
   import java.nio.file.Files;
   import java.nio.file.Path;
   import java.nio.file.Paths;
   import java.security.GeneralSecurityException;
   import java.util.List;

   // Sample to query by using a user credential
   public class AuthUserQuery {

     private static final File DATA_STORE_DIR =
         new File(AuthUserQuery.class.getResource("/").getPath(), "credentials");
     private static final JsonFactory JSON_FACTORY = JacksonFactory.getDefaultInstance();
     // i.e redirect_uri http://localhost:61984/Callback
     private static final int LOCAL_RECEIVER_PORT = 61984;

     public static void runAuthUserQuery() {
       // TODO(developer): Replace these variables before running the sample.
       /**
        * Download your OAuth2 configuration from the Google Developers Console API Credentials page.
        * https://console.cloud.google.com/apis/credentials
        */
       Path credentialsPath = Paths.get("path/to/your/client_secret.json");
       List<String> scopes = ImmutableList.of("https://www.googleapis.com/auth/bigquery");
       String query =
           "SELECT name, SUM(number) as total"
               + "  FROM `bigquery-public-data.usa_names.usa_1910_current`"
               + "  WHERE name = 'William'"
               + "  GROUP BY name;";
       authUserQuery(credentialsPath, scopes, query);
     }

     public static void authUserQuery(
         Path credentialsPath, List<String> selectedScopes, String query) {
       // Reading credentials file
       try (InputStream inputStream = Files.newInputStream(credentialsPath)) {

         // Load client_secret.json file
         GoogleClientSecrets clientSecrets =
             GoogleClientSecrets.load(JSON_FACTORY, new InputStreamReader(inputStream));
         String clientId = clientSecrets.getDetails().getClientId();
         String clientSecret = clientSecrets.getDetails().getClientSecret();

         // Generate the url that will be used for the consent dialog.
         GoogleAuthorizationCodeFlow flow =
             new GoogleAuthorizationCodeFlow.Builder(
                     GoogleNetHttpTransport.newTrustedTransport(),
                     JSON_FACTORY,
                     clientSecrets,
                     selectedScopes)
                 .setDataStoreFactory(new FileDataStoreFactory(DATA_STORE_DIR))
                 .setAccessType("offline")
                 .setApprovalPrompt("auto")
                 .build();

         // Exchange an authorization code for  refresh token
         LocalServerReceiver receiver =
             new LocalServerReceiver.Builder().setPort(LOCAL_RECEIVER_PORT).build();
         Credential credential = new AuthorizationCodeInstalledApp(flow, receiver).authorize("user");

         // OAuth2 Credentials representing a user's identity and consent
         GoogleCredentials credentials =
             UserCredentials.newBuilder()
                 .setClientId(clientId)
                 .setClientSecret(clientSecret)
                 .setRefreshToken(credential.getRefreshToken())
                 .build();

         // Initialize client that will be used to send requests. This client only needs to be created
         // once, and can be reused for multiple requests.
         BigQuery bigquery =
             BigQueryOptions.newBuilder().setCredentials(credentials).build().getService();

         QueryJobConfiguration queryConfig = QueryJobConfiguration.newBuilder(query).build();

         TableResult results = bigquery.query(queryConfig);

         results
             .iterateAll()
             .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

         System.out.println("Query performed successfully.");

       } catch (BigQueryException | IOException | GeneralSecurityException | InterruptedException ex) {
         System.out.println("Query not performed \n" + ex.toString());
       }
     }
   }
   ```

   ### Python

   ```
   from google.cloud import bigquery

   # TODO: Uncomment the line below to set the `project` variable.
   # project = 'user-project-id'
   #
   # The `project` variable defines the project to be billed for query
   # processing. The user must have the bigquery.jobs.create permission on
   # this project to run a query. See:
   # https://cloud.google.com/bigquery/docs/access-control#permissions

   client = bigquery.Client(project=project, credentials=credentials)

   query_string = """SELECT name, SUM(number) as total
   FROM `bigquery-public-data.usa_names.usa_1910_current`
   WHERE name = 'William'
   GROUP BY name;
   """
   results = client.query_and_wait(query_string)

   # Print the results.
   for row in results:  # Wait for the job to complete.
       print("{}: {}".format(row["name"], row["total"]))
   ```

   ### Node.js

   ```
   async function query() {
     const {BigQuery} = require('@google-cloud/bigquery');

     const credentials = await main.authFlow();
     const bigquery = new BigQuery(credentials);

     // Queries the U.S. given names dataset for the state of Texas.
     const query = `SELECT name, SUM(number) as total
     FROM \`bigquery-public-data.usa_names.usa_1910_current\`
     WHERE name = 'William'
     GROUP BY name;`;

     // For all options, see https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
     const options = {
       query: query,
     };

     // Run the query as a job
     const [job] = await bigquery.createQueryJob(options);
     console.log(`Job ${job.id} started.`);

     // Wait for the query to finish
     const [rows] = await job.getQueryResults();

     // Print the results
     console.log('Rows:');
     rows.forEach(row => console.log(row));

     return rows;
   }

   const main = {
     query,
     authFlow,
     exchangeCode,
     getRedirectUrl,
     startRl,
   };
   module.exports = {
     main,
   };

   if (module === require.main) {
     query().catch(console.error);
   }
   ```

在您執行程式碼範例時，程式碼會開啟瀏覽器，並要求存取與用戶端密碼相關聯的專案。您可以使用系統產生的憑證存取使用者的 BigQuery 資源，因為這個範例要求的是 [BigQuery 範圍](https://developers.google.com/identity/protocols/googlescopes?hl=zh-tw#bigqueryv2)。

## 後續步驟

1. 瞭解[其他驗證應用程式以存取 BigQuery API 的方式](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw)。
2. 瞭解[所有 Cloud API 的使用者憑證驗證作業](https://docs.cloud.google.com/docs/authentication/use-cases?hl=zh-tw#app-users)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]