* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 連結至 Amazon S3

BigQuery 管理員可以建立[連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，讓資料分析師存取儲存在 Amazon Simple Storage Service (Amazon S3) 值區中的資料。

[BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw) 會透過連線存取 Amazon S3 資料。每個連線都有專屬的 Amazon Web Services (AWS) 身分與存取權管理 (IAM) 使用者。您可以透過 AWS IAM 角色授予使用者權限。AWS IAM 角色中的政策會決定 BigQuery 可存取哪些資料 (每個連線)。

您必須建立連線，才能[查詢 Amazon S3 資料](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)，以及[將查詢結果從 BigQuery 匯出至 Amazon S3 值區](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw)。

## 事前準備

請確認您已建立下列資源：

* 已啟用 [BigQuery Connection API](https://console.cloud.google.com/apis/library/bigqueryconnection.googleapis.com?hl=zh-tw) 的[Google Cloud 專案](https://docs.cloud.google.com/docs/overview?hl=zh-tw#projects)。
* 如果您採用以量計價的收費模式，請務必為專案啟用 [BigQuery Reservation API](https://console.cloud.google.com/apis/library/bigqueryreservation.googleapis.com?hl=zh-tw)。如要瞭解定價資訊，請參閱「[BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)」一文。
* 有權在 AWS 中修改 IAM 政策的 [AWS 帳戶](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)。

## 必要的角色

如要取得建立連結以存取 Amazon S3 資料所需的權限，請要求系統管理員授予您專案的「BigQuery 連線管理員」(`roles/bigquery.connectionAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 為 BigQuery 建立 AWS IAM 政策

請務必遵循 [Amazon S3 的安全性最佳做法](https://docs.aws.amazon.com/AmazonS3/latest/dev/security-best-practices.html)。建議您採取下列做法：

* 設定 AWS 政策，禁止透過 HTTP 存取 Amazon S3 bucket。
* 設定 AWS 政策，禁止公開存取 Amazon S3 儲存空間。
* 使用 Amazon S3 伺服器端加密。
* 將授予 Google 帳戶的權限限制在最低需求。
* 設定 CloudTrail 並啟用 Amazon S3 資料事件。

如要建立 AWS IAM 政策，請使用 AWS 控制台或 Terraform：

### AWS 控制台

1. 前往 AWS IAM 主控台。確認您目前使用的帳戶擁有要存取的 Amazon S3 bucket。

   [前往 AWS IAM 主控台](https://console.aws.amazon.com/iam/home)
2. 選取「政策」**> 建立政策** (在新分頁中開啟)。
3. 按一下「JSON」，然後將下列內容貼到編輯器中：

   ```
   {
    "Version": "2012-10-17",
    "Statement": [
       {
        "Effect": "Allow",
        "Action": [
          "s3:ListBucket"
        ],
        "Resource": [
          "arn:aws:s3:::BUCKET_NAME"
         ]
       },
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetObject",
          EXPORT_PERM
        ],
        "Resource": [
          "arn:aws:s3:::BUCKET_NAME",
           "arn:aws:s3:::BUCKET_NAME/*"
         ]
       }
    ]
   }
   ```

   更改下列內容：

   * `BUCKET_NAME`：您希望 BigQuery 存取的 Amazon S3 值區。
   * `EXPORT_PERM` (選用)：如要[將資料匯出至 Amazon S3 儲存空間](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw)，請提供額外權限。以「`"s3:PutObject"`」取代
     + 如要分開控管匯出存取權，建議您建立另一個連線，並使用不同的 AWS IAM 角色，然後授予該角色僅限寫入的存取權。如要更精細地控管存取權，您也可以限制角色只能存取值區的特定路徑。**注意：** 如果將 JSON 貼到編輯器後發生錯誤，請使用 JSON 編輯器格式化 JSON 文字。
4. 在「Name」欄位中輸入政策名稱，例如 `bq_omni_read_only`。
5. 點選「建立政策」。

系統會建立政策，並以以下格式提供 Amazon Resource Name (ARN)：

```
arn:aws:iam::AWS_ACCOUNT_ID:policy/POLICY_NAME
```

更改下列內容：

* `AWS_ACCOUNT_ID`：連線的 AWS IAM 使用者 ID 編號。
* `POLICY_NAME`：您選擇的政策名稱。

### AWS CLI

如要建立 AWS IAM 政策，請使用 [`aws iam create-policy` 指令](https://docs.aws.amazon.com/cli/latest/reference/iam/create-policy.html)：

```
  aws iam create-policy \
   --policy-name POLICY_NAME \
   --policy-document '{
     "Version": "2012-10-17",
     "Statement": [
        {
         "Effect": "Allow",
         "Action": [
           "s3:ListBucket"
         ],
         "Resource": [
           "arn:aws:s3:::BUCKET_NAME"
          ]
        },
       {
         "Effect": "Allow",
         "Action": [
           "s3:GetObject",
           EXPORT_PERM
         ],
         "Resource": [
           "arn:aws:s3:::BUCKET_NAME",
            "arn:aws:s3:::BUCKET_NAME/*"
          ]
        }
     ]
    }'
```

更改下列內容：

* `POLICY_NAME`：要建立的政策名稱。
* `BUCKET_NAME`：您希望 BigQuery 存取的 Amazon S3 值區。
* `EXPORT_PERM` (選用)：如要[將資料匯出至 Amazon S3 儲存空間](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw)，請提供額外權限。以「`"s3:PutObject"`」取代
  + 如要分開控管匯出存取權，建議您建立另一個連線，並使用不同的 AWS IAM 角色，然後授予該角色僅限寫入的存取權。如要更精細地控管存取權，您也可以限制角色只能存取值區的特定路徑。

系統會建立政策，並以以下格式提供 Amazon Resource Name (ARN)：

```
arn:aws:iam::AWS_ACCOUNT_ID:policy/POLICY_NAME
```

更改下列內容：

* `AWS_ACCOUNT_ID`：連線的 AWS IAM 使用者 ID 編號。
* `POLICY_NAME`：您選擇的政策名稱。

### Terraform

在 Terraform 設定中新增下列項目，即可將政策附加至 Amazon S3 儲存貯體資源：

```
  resource "aws_iam_policy" "bigquery-omni-connection-policy" {
    name = "bigquery-omni-connection-policy"

    policy = <<-EOF
            {
              "Version": "2012-10-17",
              "Statement": [
                  {
                      "Sid": "BucketLevelAccess",
                      "Effect": "Allow",
                      "Action": ["s3:ListBucket"],
                      "Resource": ["arn:aws:s3:::BUCKET_NAME"]
                  },
                  {
                      "Sid": "ObjectLevelAccess",
                      "Effect": "Allow",
                      "Action": ["s3:GetObject",EXPORT_PERM],
                      "Resource": [
                          "arn:aws:s3:::BUCKET_NAME",
                          "arn:aws:s3:::BUCKET_NAME/*"
                          ]
                  }
              ]
            }
            EOF
  }
```

更改下列內容：

* `BUCKET_NAME`：您希望 BigQuery 存取的 Amazon S3 值區。
* `EXPORT_PERM` (選用)：如要[將資料匯出至 Amazon S3 儲存空間](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw)，請提供額外權限。以「`"s3:PutObject"`」取代
  + 如要分開控管匯出存取權，建議您使用不同的 AWS IAM 角色建立另一個連線，並授予該角色僅限寫入的存取權。如要進一步控管存取權，您也可以限制角色只能存取 bucket 的特定路徑。

## 為 BigQuery 建立 AWS IAM 角色

接著，建立可從 BigQuery 存取 Amazon S3 值區的角色。這個角色會使用您在前一節建立的政策。

如要建立 AWS IAM 角色，請使用 AWS 主控台或 Terraform：

### AWS 控制台

1. 前往 AWS IAM 主控台。確認您目前使用的帳戶擁有要存取的 Amazon S3 bucket。

   [前往 AWS IAM 主控台](https://console.aws.amazon.com/iam/home)
2. 依序選取「角色」>「建立角色」。
3. 在「Select type of trusted entity」部分，選取「Web Identity」。
4. 在「識別資訊提供者」部分，選取「Google」。
5. 在「目標對象」中，輸入 `00000` 做為預留位置值。
   您稍後會替換該值。
6. 點選 [Next: Permissions] (下一步：權限)。
7. 如要授予角色 Amazon S3 資料的存取權，請將 IAM 政策附加至該角色。搜尋您在前一節中建立的政策，然後點選切換按鈕。
8. 按一下「下一步：代碼」。
9. 點選「下一步：檢閱」。輸入角色名稱，例如
   `BQ_Read_Only`。
10. 按一下「建立角色」。

### AWS CLI

使用下列指令建立 IAM 角色，並將政策指派給建立的角色：

```
  aws iam create-role \
   --role-name bigquery-omni-connection \
   --max-session-duration 43200 \
   --assume-role-policy-document '{
     "Version": "2012-10-17",
     "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "accounts.google.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "accounts.google.com:sub": "00000"
                }
            }
        }
    ]
}'
```

### Terraform

在 Terraform 設定中新增下列項目，即可建立 IAM 角色，並將政策指派給建立的角色：

```
  resource "aws_iam_role" "bigquery-omni-connection-role" {
    name                 = "bigquery-omni-connection"
    max_session_duration = 43200

    assume_role_policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Federated": "accounts.google.com"
          },
          "Action": "sts:AssumeRoleWithWebIdentity",
          "Condition": {
            "StringEquals": {
              "accounts.google.com:sub": "00000"
            }
          }
        }
      ]
    }
    EOF
  }

  resource "aws_iam_role_policy_attachment" "bigquery-omni-connection-role-attach" {
    role       = aws_iam_role.bigquery-omni-connection-role.name
    policy_arn = aws_iam_policy.bigquery-omni-connection-policy.arn
  }

  output "bigquery_omni_role" {
    value = aws_iam_role.bigquery-omni-connection-role.arn
  }
```

然後將政策附加至角色：

```
  aws iam attach-role-policy \
    --role-name bigquery-omni-connection \
    --policy-arn arn:aws:iam::AWS_ACCOUNT_ID:policy/POLICY_NAME
```

更改下列內容：

* `AWS_ACCOUNT_ID`：連線的 AWS IAM 使用者 ID 編號。
* `POLICY_NAME`：您選擇的政策名稱。

## 建立連結

如要連線至 Amazon S3 儲存空間，請使用Google Cloud 控制台、bq 指令列工具或用戶端程式庫：

### 控制台

**重點提醒：** 在包含要查詢的 Amazon S3 執行個體的 Google Cloud 專案中建立連線。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，點選「新增資料」add。

   「新增資料」對話方塊隨即開啟。
3. 在「Filter By」(依據篩選) 窗格的「Data Source Type」(資料來源類型) 區段中，選取「Storage/Data Lakes」(儲存空間/資料湖泊)。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `aws` 或 `Amazon S3`。
4. 在「精選資料來源」部分，按一下「Amazon S3」。
5. 按一下「Amazon S3 Omni：BigQuery 聯盟」解決方案資訊卡。
6. 在「建立表格」對話方塊的「連線 ID」欄位中，選取「建立新的 S3 連線」。
7. 在「外部資料來源」窗格中，輸入下列資訊：

   * 在「連線類型」中，選取「AWS 中的 BigLake (透過 BigQuery Omni)」。
   * 在「Connection ID」(連線 ID) 專區中輸入連線資源的 ID。可以使用英文字母、數字、破折號和底線。
   * 在「Region」(區域) 部分，選取要建立連線的位置。
   * 選用：在「Friendly name」(好記名稱) 中輸入使用者容易記得的連線名稱，例如 `My connection resource`。好記名稱可以是任何資料值，只要您日後需要修改時可以輕鬆識別連線資源即可。
   * 選用：在「Description」(說明) 中輸入這項連線資源的說明。
   * 在「AWS 角色 ID」部分，輸入您建立的完整 IAM 角色 ID，格式如下：

     ```
     arn:aws:iam::AWS_ACCOUNT_ID:role/ROLE_NAME
     ```
8. 點選「建立連線」。
9. 點選「前往連線」。
10. 在「連線資訊」窗格中，複製「BigQuery Google 身分」。
    這是 Google 主體，每個連線都有專屬主體。範例：

    ```
      BigQuery Google identity: IDENTITY_ID
    ```

### Terraform

```
  resource "google_bigquery_connection" "connection" {
    connection_id = "bigquery-omni-aws-connection"
    friendly_name = "bigquery-omni-aws-connection"
    description   = "Created by Terraform"

    location      = "AWS_LOCATION"
    aws {
      access_role {
        # This must be constructed as a string instead of referencing the
        # AWS resources directly to avoid a resource dependency cycle
        # in Terraform.
        iam_role_id = "arn:aws:iam::AWS_ACCOUNT:role/IAM_ROLE_NAME"
      }
    }
  }
```

更改下列內容：

* `AWS_LOCATION`：[Amazon S3 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations) (位於 Google Cloud中)
* `AWS_ACCOUNT`：您的 AWS 帳戶 ID。
* `IAM_ROLE_NAME`：可從 BigQuery 存取 Amazon S3 值區的角色。使用「[為 BigQuery 建立 AWS 身分與存取權管理角色](#creating-aws-iam-role)」中 `aws_iam_role` 資源的 `name` 引數值。

### bq

```
bq mk --connection --connection_type='AWS' \
--iam_role_id=arn:aws:iam::AWS_ACCOUNT_ID:role/ROLE_NAME \
--location=AWS_LOCATION \
CONNECTION_ID
```

更改下列內容：

* `AWS_ACCOUNT_ID`：連線的 AWS IAM 使用者 ID 號碼
* `ROLE_NAME`：您選擇的角色政策名稱
* `AWS_LOCATION`：[Amazon S3 位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations) (位於 Google Cloud中)
* `CONNECTION_ID`：您為這個連線資源指定的 ID。

指令列會顯示下列輸出內容：

```
  Identity: IDENTITY_ID
```

輸出內容包含下列項目：

* `IDENTITY_ID`：控制項的 Google 主體，適用於每個連線。 Google Cloud

請記下 `IDENTITY_ID` 值。

**注意：** 如要覆寫預設專案，請使用 `--project_id=PROJECT_ID` 參數。將 `PROJECT_ID` 替換為Google Cloud 專案 ID。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.connection.v1.AwsAccessRole;
import com.google.cloud.bigquery.connection.v1.AwsProperties;
import com.google.cloud.bigquery.connection.v1.Connection;
import com.google.cloud.bigquery.connection.v1.CreateConnectionRequest;
import com.google.cloud.bigquery.connection.v1.LocationName;
import com.google.cloud.bigqueryconnection.v1.ConnectionServiceClient;
import java.io.IOException;

// Sample to create aws connection
public class CreateAwsConnection {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    // Example of location: aws-us-east-1
    String location = "MY_LOCATION";
    String connectionId = "MY_CONNECTION_ID";
    // Example of role id: arn:aws:iam::accountId:role/myrole
    String iamRoleId = "MY_AWS_ROLE_ID";
    AwsAccessRole role = AwsAccessRole.newBuilder().setIamRoleId(iamRoleId).build();
    AwsProperties awsProperties = AwsProperties.newBuilder().setAccessRole(role).build();
    Connection connection = Connection.newBuilder().setAws(awsProperties).build();
    createAwsConnection(projectId, location, connectionId, connection);
  }

  static void createAwsConnection(
      String projectId, String location, String connectionId, Connection connection)
      throws IOException {
    try (ConnectionServiceClient client = ConnectionServiceClient.create()) {
      LocationName parent = LocationName.of(projectId, location);
      CreateConnectionRequest request =
          CreateConnectionRequest.newBuilder()
              .setParent(parent.toString())
              .setConnection(connection)
              .setConnectionId(connectionId)
              .build();
      Connection response = client.createConnection(request);
      AwsAccessRole role = response.getAws().getAccessRole();
      System.out.println(
          "Aws connection created successfully : Aws userId :"
              + role.getIamRoleId()
              + " Aws externalId :"
              + role.getIdentity());
    }
  }
}
```

## 為 AWS 角色新增信任關係

BigQuery Omni 提供兩種方法，可安全地存取 Amazon S3 中的資料。您可以授予 Google Cloud 服務帳戶 AWS 角色存取權，或者，如果 AWS 帳戶有 `accounts.google.com` 的[自訂識別資訊提供者](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)，則必須將 Google Cloud 服務帳戶新增為提供者的對象：

* [為 AWS 角色新增信任政策](#add-trust-policy)。
* [設定自訂 AWS 識別資訊提供者](#configuring-custom-idp)。

### 為 AWS 角色新增信任政策

信任關係可讓連線擔任角色，並根據角色政策存取 Amazon S3 資料。

如要新增信任關係，請使用 AWS 控制台或 Terraform：

### AWS 控制台

1. 前往 AWS IAM 主控台。確認您目前使用的帳戶擁有要存取的 Amazon S3 bucket。

   [前往 AWS IAM 主控台](https://console.aws.amazon.com/iam/home)
2. 選取「角色」。
3. 選取您建立的 `ROLE_NAME`。
4. 按一下「編輯」，然後執行下列操作：

   1. 將「工作階段持續時間上限」設為「12 小時」。由於每項查詢最多可執行六小時，因此這段時間允許一次額外的重試。如果將工作階段持續時間延長至 12 小時以上，系統不會提供額外的重試機會。詳情請參閱「[查詢/多重陳述式查詢執行時間限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_script_execution_time_limit)」。
   2. 按一下 [儲存變更]。
5. 選取「信任關係」，然後按一下「編輯信任關係」。
   將政策內容換成下列內容：

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "accounts.google.com"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "accounts.google.com:sub": "IDENTITY_ID"
           }
         }
       }
     ]
   }
   ```

   將 `IDENTITY_ID` 替換為 **BigQuery Google 身分**值，您可以在 Google Cloud 控制台中找到[您建立的連線](#creating-aws-connection)。
6. 按一下「更新信任政策」。

### AWS CLI

如要建立與 BigQuery 連線的信任關係，請使用 [`aws iam update-assume-role-policy` 指令](https://docs.aws.amazon.com/cli/latest/reference/iam/update-assume-role-policy.html)：

```
  aws iam update-assume-role-policy \
    --role-name bigquery-omni-connection \
    --policy-document '{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Federated": "accounts.google.com"
          },
          "Action": "sts:AssumeRoleWithWebIdentity",
          "Condition": {
            "StringEquals": {
              "accounts.google.com:sub": "IDENTITY_ID"
            }
          }
        }
      ]
    }'
  aws iam update-assume-role-policy \
    --role-name bigquery-omni-connection \
    --policy-document '{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Federated": "accounts.google.com"
          },
          "Action": "sts:AssumeRoleWithWebIdentity",
          "Condition": {
            "StringEquals": {
              "accounts.google.com:sub": "IDENTITY_ID"
            }
          }
        }
      ]
    }'
```

更改下列內容：

* `IDENTITY_ID`：**BigQuery Google 身分**值，您可以在 Google Cloud 所建立連線的[控制台](#creating-aws-connection)中找到這個值。

### Terraform

更新 Terraform 設定中的 `aws_iam_role` 資源，新增信任關係：

```
    resource "aws_iam_role" "bigquery-omni-connection-role" {
      name                 = "bigquery-omni-connection"
      max_session_duration = 43200

      assume_role_policy = <<-EOF
          {
            "Version": "2012-10-17",
            "Statement": [
              {
                "Effect": "Allow",
                "Principal": {
                  "Federated": "accounts.google.com"
                },
                "Action": "sts:AssumeRoleWithWebIdentity",
                "Condition": {
                  "StringEquals": {
                    "accounts.google.com:sub": "${google_bigquery_connection.connection.aws[0].access_role[0].identity}"
                  }
                }`
              }
            ]
          }
          EOF
    }
```

**注意：** 在 AWS 中指派角色時，變更可能需要一段時間才會全面生效。如果使用新連線時收到這類錯誤訊息，請稍後再試，或許就能解決問題。

現在可以使用連線了。

### 設定自訂 AWS 識別資訊提供者

如果 AWS 帳戶有 [`accounts.google.com` 的](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)IDENTITY\_ID自訂身分識別提供者，您需要將 `accounts.google.com` 新增為提供者的目標對象。方法如下：

1. 前往 AWS IAM 主控台。確認您目前使用的帳戶擁有要存取的 Amazon S3 bucket。

   [前往 AWS IAM 主控台](https://console.aws.amazon.com/iam/home)
2. 依序前往「IAM」>「身分識別提供者」。
3. 選取 *accounts.google.com* 的識別資訊提供者。
4. 按一下「新增目標對象」，然後將 IDENTITY\_ID 新增為目標對象。

現在可以使用連線了。

## 與使用者共用連線

您可以授予下列角色，讓使用者查詢資料及管理連線：

* `roles/bigquery.connectionUser`：可讓使用者透過連線功能連結外部資料來源，並對其執行查詢。
* `roles/bigquery.connectionAdmin`：允許使用者管理連線。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)

   連線會列在專案中，位於「Connections」(連線) 群組。
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 按一下專案，然後依序點選「連線」和所需連線。
4. 在「詳細資料」窗格中，按一下「共用」即可共用連線。
   接著，按照下列步驟操作：

   1. 在「連線權限」對話方塊中，新增或編輯主體，與其他主體共用連線。
   2. 按一下 [儲存]。

### bq

您無法使用 bq 指令列工具共用連線。
如要共用連線，請使用 Google Cloud 控制台或 BigQuery Connections API 方法共用連線。

### API

請使用 BigQuery Connections REST API 參考資料中的 [`projects.locations.connections.setIAM` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest/v1/projects.locations.connections?hl=zh-tw#methods)，並提供 `policy` 資源的執行個體。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.resourcenames.ResourceName;
import com.google.cloud.bigquery.connection.v1.ConnectionName;
import com.google.cloud.bigqueryconnection.v1.ConnectionServiceClient;
import com.google.iam.v1.Binding;
import com.google.iam.v1.Policy;
import com.google.iam.v1.SetIamPolicyRequest;
import java.io.IOException;

// Sample to share connections
public class ShareConnection {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String location = "MY_LOCATION";
    String connectionId = "MY_CONNECTION_ID";
    shareConnection(projectId, location, connectionId);
  }

  static void shareConnection(String projectId, String location, String connectionId)
      throws IOException {
    try (ConnectionServiceClient client = ConnectionServiceClient.create()) {
      ResourceName resource = ConnectionName.of(projectId, location, connectionId);
      Binding binding =
          Binding.newBuilder()
              .addMembers("group:example-analyst-group@google.com")
              .setRole("roles/bigquery.connectionUser")
              .build();
      Policy policy = Policy.newBuilder().addBindings(binding).build();
      SetIamPolicyRequest request =
          SetIamPolicyRequest.newBuilder()
              .setResource(resource.toString())
              .setPolicy(policy)
              .build();
      client.setIamPolicy(request);
      System.out.println("Connection shared successfully");
    }
  }
}
```

## 後續步驟

* 瞭解不同[連線類型](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)。
* 瞭解如何[管理連線](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)。
* 瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 使用 [BigQuery Omni with AWS 實驗室](https://www.cloudskillsboost.google/catalog_lab/5345?hl=zh-tw)。
* 瞭解 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。
* 瞭解如何[查詢 Amazon S3 資料](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)。
* 瞭解如何[將查詢結果匯出至 Amazon S3 值區](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]