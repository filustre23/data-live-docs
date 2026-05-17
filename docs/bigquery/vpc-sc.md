Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 適用的 VPC Service Controls

本頁說明如何使用 VPC Service Controls 建立服務範圍，進一步保護 BigQuery 資源。這些安全防護範圍會限制 BigQuery 的存取權，且與 Identity and Access Management (IAM) 控制項無關。這類功能在下列用途中相當實用：

* 限制資源存取權，防止資料外洩，但輸入和輸出規則中明確允許的資源除外。
* 從第三方來源或 Google Cloud 服務 (例如 Cloud Storage) 安全地將資料載入 BigQuery。
* 控管從 BigQuery 匯出至 Cloud Storage 或其他目標的資料。

詳情請參閱「[VPC Service Controls 總覽](https://docs.cloud.google.com/vpc-service-controls/docs/overview?hl=zh-tw)」。

## 事前準備

* 如要取得設定 service perimeter 所需的權限，請參閱「[透過 IAM 控管 VPC Service Controls 的存取權](https://docs.cloud.google.com/vpc-service-controls/docs/access-control?hl=zh-tw)」。
* 您必須為機構設定存取權政策。詳情請參閱「[建立存取權政策](https://docs.cloud.google.com/access-context-manager/docs/create-access-policy?hl=zh-tw)」。

## 建立 VPC Service Controls 範圍

以下範例說明如何建立 VPC Service Controls perimeter，限制可存取 BigQuery 專案的外部 IP 位址範圍。

1. 建立*存取層級*，只允許從特定 IP 位址範圍 (例如公司網路內的 IP 位址) 存取。如要建立，請使用 [`gcloud access-context-manager levels create`](https://docs.cloud.google.com/sdk/gcloud/reference/access-context-manager/levels/create?hl=zh-tw) 指令：

   ```
   echo """
   - ipSubnetworks:
     - 162.222.181.0/24
     - 2001:db8::/48
   """ > level.yaml

   gcloud access-context-manager levels create ACCESS_LEVEL_NAME \
       --title="TITLE" --basic-level-spec=level.yaml
   ```

   更改下列內容：

   * `ACCESS_LEVEL_NAME`：存取層級的 ID
   * `TITLE`：service perimeter 的人類可讀標題

   如要進一步瞭解如何建立存取層級，請參閱[實作範例](https://docs.cloud.google.com/access-context-manager/docs/create-basic-access-level?hl=zh-tw#example_implementations)。
2. 建立或更新安全防護範圍，保護 BigQuery 資源。以下範例會保護專案。如要瞭解其他用途，例如保護從其他專案的 Cloud Storage bucket 移轉的資料，請參閱[使用案例](#use-cases)。

   ### 建立範圍

   如要建立新安全防護範圍來保護 BigQuery 專案，請使用 [`gcloud access-context-manager perimeters create`](https://docs.cloud.google.com/sdk/gcloud/reference/access-context-manager/perimeters/create?hl=zh-tw) 指令：

   ```
   echo """
   - ingressFrom:
       identityType: ANY_IDENTITY
       sources:
       - accessLevel: accessPolicies/POLICY_NAME/accessLevels/ACCESS_LEVEL_NAME
     ingressTo:
       operations:
       - methodSelectors:
         - method: '*'
         serviceName: bigquery.googleapis.com
       resources:
       - '*'

   """ > ingress.yaml

   gcloud access-context-manager perimeters create BIGQUERY_PERIMETER --title="TITLE" \
       --resources=BIGQUERY_PROJECT_NUMBER \
       --restricted-services=bigquery.googleapis.com \
       --ingress-policies=ingress.yaml
       --policy=POLICY_NAME
   ```

   更改下列內容：

   * `POLICY_NAME`：存取權政策的 ID
   * `ACCESS_LEVEL_NAME`：存取層級的 ID
   * `PERIMETER`：perimeter 的 ID
   * `TITLE`：service perimeter 的簡短標題，方便使用者閱讀
   * `BIGQUERY_PROJECT_NUMBER`：BigQuery 專案的 ID
   * `POLICY_NAME`：存取權政策的 ID

   ### 更新範圍

   如要更新現有範圍，請使用 [`gcloud access-context-manager perimeters update`](https://docs.cloud.google.com/sdk/gcloud/reference/access-context-manager/perimeters/update?hl=zh-tw) 指令：

   ```
   gcloud access-context-manager perimeters update BIGQUERY_PERIMETER --set-ingress-policies=ingress.yaml
   ```

   將 `BIGQUERY_PERIMETER` 替換為保護 BigQuery 資源的周邊防護範圍 ID。

## 測試 perimeter

請先測試 VPC Service Controls 範圍，再強制執行。詳情請參閱「[service perimeter 的模擬測試模式](https://docs.cloud.google.com/vpc-service-controls/docs/dry-run-mode?hl=zh-tw)」和「[使用模擬測試模式測試輸入或輸出政策](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw#using-dryrun-ingress-egress-rules)」。

## 用途

下列用途範例說明如何使用 VPC Service Controls，保護進出 BigQuery 的資料。

### 查詢其他專案中 Cloud Storage 值區的外部資料表資料

下列範例說明如何選擇性地允許 BigQuery 和 Cloud Storage 專案之間的通訊 (如果這些專案由 perimeter 分隔)。

1. 更新 Cloud Storage 專案周邊範圍的輸出規則，允許 BigQuery 專案存取 Cloud Storage 專案：

   ```
   echo """
   - egressFrom:
       identityType: ANY_IDENTITY
     egressTo:
       operations:
       - methodSelectors:
         - method: '*'
         serviceName: storage.googleapis.com
       resources:
       - projects/BIGQUERY_PROJECT_NUMBER
   """ > egress.yaml

   gcloud access-context-manager perimeters update CLOUD_STORAGE_PERIMETER --policy=POLICY_NAME --set-egress-policies=egress.yaml
   ```

   更改下列內容：

   * `BIGQUERY_PROJECT_NUMBER`：BigQuery 專案的 ID
   * `CLOUD_STORAGE_PERIMETER`：保護 Cloud Storage 資源的 perimeter ID
   * `POLICY_NAME`：存取權政策的 ID
2. 更新 BigQuery 專案周邊的輸出規則，允許 Cloud Storage 專案存取 BigQuery 專案：

   ```
   echo """
   - egressFrom:
       identityType: ANY_IDENTITY
     egressTo:
       operations:
       - methodSelectors:
         - method: '*'
         serviceName: storage.googleapis.com
       resources:
       - projects/CLOUD_STORAGE_PROJECT_NUMBER
   """ > egress1.yaml

   gcloud access-context-manager perimeters update BIGQUERY_PERIMETER --policy=POLICY_NAME --set-egress-policies=egress1.yaml
   ```

   更改下列內容：

   * `CLOUD_STORAGE_PROJECT_NUMBER`：Cloud Storage 專案的 ID
   * `PERIMETER`：perimeter 的 ID
   * `POLICY_NAME`：存取權政策的 ID
3. 選用：如果保護 BigQuery 專案的 perimeter 包含 `storage.googleapis.com` 做為受限服務，您必須更新 ingress 規則：

   ```
   echo """
   - ingressFrom:
       identityType: ANY_IDENTITY
       sources:
       - accessLevel: accessPolicies/POLICY_NAME/accessLevels/ACCESS_LEVEL_NAME
     ingressTo:
       operations:
       - methodSelectors:
         - method: '*'
         serviceName: bigquery.googleapis.com
       - methodSelectors:
         - method: '*'
         serviceName: storage.googleapis.com
       resources:
       - '*'

   """ > ingress.yaml

   gcloud access-context-manager perimeters create BIGQUERY_PERIMETER --title="TITLE" \
       --resources=BIGQUERY_PROJECT_NUMBER \
       --restricted-services=bigquery.googleapis.com \
       --ingress-policies=ingress.yaml
       --policy=POLICY_NAME
   ```

### 從 BigQuery Omni 匯入及匯出資料

您可以透過 VPC Service Controls perimeter 限制 BigQuery Omni 與外部雲端服務之間的存取權，進一步防禦。如需更多資訊和範例，請參閱建立 Azure Blob Storage BigLake 資料表時的 [VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw#vpc-service) 設定。

## 後續步驟

* 進一步瞭解 [BigQuery sharing 中的 VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)。
* 瞭解如何[使用外部雲端服務限制 BigQuery Omni 存取權](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw#vpc-service)。
* 瞭解[風險，以及如何透過 VPC Service Controls 降低風險](https://cloud.google.com/security/vpc-service-controls?hl=zh-tw)。
* 進一步瞭解 [BigQuery 中的 VPC Service Controls 支援和限制](https://docs.cloud.google.com/vpc-service-controls/docs/supported-products?hl=zh-tw#table_bigquery)。
* [排解](https://docs.cloud.google.com/vpc-service-controls/docs/troubleshooting?hl=zh-tw#debugging) BigQuery 和 VPC Service Controls 的常見問題。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]