Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料移轉服務執行通知

BigQuery 資料移轉服務執行通知可讓您自動追蹤排定的資料移轉作業狀態。您可以設定 Pub/Sub，在移轉作業成功或失敗時傳送機器可讀訊息，也可以設定電子郵件快訊，在作業失敗時接收人類可讀詳細資料，或同時使用這兩個選項。

## Pub/Sub 通知

Pub/Sub 通知會將移轉作業執行的相關資訊傳送至 [Pub/Sub](https://docs.cloud.google.com/pubsub?hl=zh-tw) 主題。Pub/Sub 通知是由下列[狀態](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/TransferState?hl=zh-tw)的已完成移轉作業觸發：

* `SUCCEEDED`
* `FAILED`
* `CANCELLED`

只要是您有足夠權限的專案，您就能將通知傳送至其中的任何 Pub/Sub 主題。Pub/Sub 主題收到通知後，即可將結果訊息傳送給主題訂閱者 (數量不限)。

### 事前準備

設定 Pub/Sub 移轉作業執行通知前，請先完成下列事項：

1. 為要接收通知的專案啟用 Pub/Sub API。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=pubsub&hl=zh-tw)
2. 針對要接收通知的專案取得足夠的權限：

   * 如果您擁有要接收通知的專案，表示您非常有可能已經具備必要權限。
   * 如果您打算建立主題來接收通知，則應具備 [`pubsub.topics.create`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles) 權限。
   * 無論您打算使用新的或現有的主題，都應具備 [`pubsub.topics.getIamPolicy`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles) 和 [`pubsub.topics.setIamPolicy`](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#tbl_roles) 權限。如果您建立主題，通常已具備該主題的權限。下列預先定義的 IAM 角色同時具備 `pubsub.topics.getIamPolicy` 和 `pubsub.topics.setIamPolicy` 權限：`pubsub.admin`。詳情請參閱「[Pub/Sub 存取控管](https://docs.cloud.google.com/pubsub/docs/access_control?hl=zh-tw#console)」。
3. [具備現有的 Pub/Sub 主題](https://docs.cloud.google.com/pubsub/docs/create-topic?hl=zh-tw)，可接收通知。

**注意：** 請勿從 `pubsub.publisher` 預先定義的 IAM 角色中移除 [BigQuery 資料移轉服務代理程式](https://docs.cloud.google.com/iam/docs/service-agents?hl=zh-tw#bigquerydatatransfer.serviceAgent)。移除後，系統可能無法將通知發布至 Pub/Sub 主題。**注意：** 建立 Pub/Sub 主題時，請勿指定任何自訂結構定義。指定自訂結構定義可能會導致通知發布失敗。

### 通知格式

傳送至 Pub/Sub 主題的通知包含兩個部分：

* **屬性**：用於說明事件的鍵/值組合。
* **酬載**：含變更物件的中繼資料的字串。

#### 屬性

屬性是鍵/值組合，包含在 BigQuery 資料移轉服務傳送至 Pub/Sub 主題的所有通知中。無論通知酬載為何，通知都會包含以下鍵值組合：

| **屬性名稱** | **範例** | **說明** |
| --- | --- | --- |
| **eventType** | `TRANSFER_RUN_FINISHED` | 最新發生事件的類型，值一定是 `TRANSFER_RUN_FINISHED`。 |
| **payloadFormat** | `JSON_API_V1` | 物件酬載的格式，值一定是 `JSON_API_V1`。 |

#### 酬載

酬載是含移轉執行的中繼資料的字串。目前無法變更酬載類型，我們會因應日後的 API 版本變更配合提供相關功能。

| **酬載類型** | **說明** |
| --- | --- |
| **JSON\_API\_V1** | 酬載會是 UTF-8 JSON 序列化字串，其中包含 [`TransferRun` 的資源表示法](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs.runs?hl=zh-tw#TransferRun)。 |

## 電子郵件通知

如果移轉作業失敗，系統會傳送人類可讀的電子郵件通知。這些訊息會傳送至*轉移管理員* (即設定轉移作業的帳戶) 的電子郵件地址。您無法設定訊息內容，也無法設定訊息收件者。

如果您使用服務帳戶驗證移轉設定，可能無法存取電子郵件，接收移轉作業通知電子郵件。在這種情況下，建議您設定 [Pub/Sub 通知](#notifications)，以便接收移轉作業執行通知。

如要將移轉作業執行電子郵件通知傳送給更多使用者，請設定電子郵件轉送規則來發布訊息。如果您使用 Gmail，則可[自動將 Gmail 郵件轉寄到其他帳戶](https://support.google.com/mail/answer/10957?hl=zh-tw)。

電子郵件通知是由 BigQuery 資料移轉服務傳送，內含移轉設定和移轉作業的詳細資料，以及失敗作業的執行記錄連結。例如：

```
From: bigquery-data-transfer-service-noreply@google.com
To: TRANSFER_ADMIN
Title: BigQuery Data Transfer Service — Transfer Run Failure —
DISPLAY_NAME

Transfer Configuration
Display Name: DISPLAY_NAME
Source: DATA_SOURCE
Destination: PROJECT_ID

Run Summary
Run: RUN_NAME
Schedule Time: SCHEDULE_TIME
Run Time: RUN_TIME
View Run History


Google LLC 1600 Amphitheatre Parkway, Mountain View, CA 94043

This email was sent because you indicated you are willing to receive Run
Notifications from the BigQuery Data Transfer Service. If you do not wish to
receive such emails in the future, click View Transfer Configuration and
un-check the "Send E-mail Notifications" option.
```

## 開啟或編輯通知

如要開啟通知或編輯現有通知，請選擇下列其中一項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選導覽選單中的「資料移轉」。
3. 如要為新的移轉作業啟用通知，請按一下 add「Create transfer」(建立移轉作業)。如要調整現有移轉作業的通知，請按一下移轉作業名稱，然後按一下「Edit」(編輯)。
4. 在「Notification options」(通知選項) 部分，按一下要啟用的通知類型旁的切換鈕。

   * **電子郵件通知**：啟用這個選項後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   * **Pub/Sub 通知**：啟用這個選項時，請選擇[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.CreateTransferConfigRequest;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ProjectName;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.protobuf.Struct;
import com.google.protobuf.Value;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

// Sample to get run notification
public class RunNotification {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    final String datasetId = "MY_DATASET_ID";
    final String pubsubTopicName = "MY_TOPIC_NAME";
    final String query =
        "SELECT CURRENT_TIMESTAMP() as current_time, @run_time as intended_run_time, "
            + "@run_date as intended_run_date, 17 as some_integer";
    Map<String, Value> params = new HashMap<>();
    params.put("query", Value.newBuilder().setStringValue(query).build());
    params.put(
        "destination_table_name_template",
        Value.newBuilder().setStringValue("my_destination_table_{run_date}").build());
    params.put("write_disposition", Value.newBuilder().setStringValue("WRITE_TRUNCATE").build());
    params.put("partitioning_field", Value.newBuilder().build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Scheduled Query Name")
            .setDataSourceId("scheduled_query")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .setSchedule("every 24 hours")
            .setNotificationPubsubTopic(pubsubTopicName)
            .build();
    runNotification(projectId, transferConfig);
  }

  public static void runNotification(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = dataTransferServiceClient.createTransferConfig(request);
      System.out.println(
          "\nScheduled query with run notification created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("\nScheduled query with run notification was not created." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
transfer_config_name = "projects/1234/locations/us/transferConfigs/abcd"
pubsub_topic = "projects/PROJECT-ID/topics/TOPIC-ID"
from google.cloud import bigquery_datatransfer
from google.protobuf import field_mask_pb2

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

transfer_config = bigquery_datatransfer.TransferConfig(name=transfer_config_name)
transfer_config.notification_pubsub_topic = pubsub_topic
update_mask = field_mask_pb2.FieldMask(paths=["notification_pubsub_topic"])

transfer_config = transfer_client.update_transfer_config(
    {"transfer_config": transfer_config, "update_mask": update_mask}
)

print(f"Updated config: '{transfer_config.name}'")
print(f"Notification Pub/Sub topic: '{transfer_config.notification_pubsub_topic}'")
```

## 執行通知定價

如果設定 Pub/Sub 執行通知，則會產生 Pub/Sub 費用。詳情請參閱 Pub/Sub [定價](https://cloud.google.com/pubsub/pricing?hl=zh-tw)頁面。

## 後續步驟

* [進一步瞭解 Pub/Sub](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw)。
* 進一步瞭解如何建立 Pub/Sub [主題](https://docs.cloud.google.com/pubsub/docs/create-topic?hl=zh-tw)。
* 進一步瞭解 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]