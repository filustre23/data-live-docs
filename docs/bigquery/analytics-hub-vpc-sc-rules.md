Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 設定 BigQuery 共用的 VPC Service Controls 規則

透過輸入和輸出規則，BigQuery sharing (舊稱 Analytics Hub) 的發布者和訂閱者，可以存取受 VPC Service Controls 範圍保護的跨專案資料。您可以在「呼叫端專案」(即發起要求的網路或用戶端 Google Cloud 專案，例如 SQL 查詢或 Google Cloud CLI 指令) 與託管資料交換、資訊清單和資料集的專案之間設定這些規則。

設定這些規則前，請先熟悉 [VPC Service Controls 範圍](https://docs.cloud.google.com/vpc-service-controls/docs/service-perimeters?hl=zh-tw)、[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)、[資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)、[清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)和[連結的資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)。

## 限制

BigQuery 共用功能不支援[以方法為基礎的規則](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw)。您必須指定 `method: '*'`，允許輸入和輸出規則中的所有方法：

```
- ingressTo:
    operations:
      - methodSelectors:
          - method: '*'
        serviceName: analyticshub.googleapis.com
    resources:
      - projects/PROJECT_NUMBER
```

如果 service perimeter 也保護 BigQuery 資源，您必須允許 BigQuery 服務的輸入和輸出規則。建立資料交換時，不一定要允許輸入和輸出規則。BigQuery 的輸入和輸出規則與 BigQuery sharing 規則類似：

```
- ingressTo:
    operations:
      - methodSelectors:
          - method: '*'
        serviceName: bigquery.googleapis.com
    resources:
      - projects/PROJECT_NUMBER
```

將 `PROJECT_NUMBER` 替換為受 service perimeter 保護的目標專案編號。

## 建立資料交換

在下圖中，呼叫端專案和包含資料交換作業的專案位於不同的 service perimeter：

**圖 1.**建立資料交換作業的 VPC Service Controls 規則。

圖 1 顯示下列元件：

* **呼叫端**：BigQuery 共用管理員。
* **專案 R**：呼叫端專案。
* **專案 E**：託管資料交換和清單的專案。

如果您是 BigQuery sharing 管理員，在與呼叫端專案不同的專案中[建立資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#create-exchange)時，必須新增下列輸入和輸出規則：

| 專案 | 規則 |
| --- | --- |
| Project R | 專案 E 的輸出規則 |
| 專案 E (資料交換) | 專案 R 的輸入規則 |

## 建立產品資訊

在下圖中，包含資料交換和共用資料集的專案位於不同的 service perimeter：

**圖 2**：建立產品資訊的 VPC Service Controls 規則。

圖 2 顯示下列元件：

* **呼叫端**：BigQuery sharing 管理員或發布者。
* **專案 R**：呼叫端專案。
* **專案 E**：託管資料交換和清單的專案。
* **專案 S**：託管共用資料集的專案。

如果您是 BigQuery sharing 發布商，在資料交換庫中建立的產品資訊與共用資料集位於不同專案時，必須新增下列輸入和輸出規則：

| 專案 | 規則 |
| --- | --- |
| Project R | 專案 E 的輸出規則  專案 S 的輸出規則 |
| 專案 E (資料交換) | 專案 S 的輸出規則  專案 R 的輸入規則 |
| 專案 S (共用資料集) | 專案 E 的輸出規則  專案 R 的輸入規則 |

## 訂閱產品資訊

在下圖中，包含產品資訊的專案和該產品資訊的連結資料集位於不同的 service perimeter：

**圖 3**：訂閱清單的 VPC Service Controls 規則。

圖 3 顯示下列元件：

* **呼叫端**：BigQuery sharing 訂閱者。
* **專案 R**：呼叫端專案。
* **專案 E**：託管資料交換和清單的專案。
* **專案 L**：託管連結資料集的專案。

身為 BigQuery sharing 訂閱者，當您訂閱資料交換中的項目，而該資料交換位於與您專案不同的專案時，您必須新增下列輸入和輸出規則：

| 專案 | 規則 |
| --- | --- |
| Project R | 專案 E 的輸出規則  專案 L 的輸出規則 |
| 專案 E (產品資訊) | 專案 L 的輸出規則  專案 R 的輸入規則 |
| 專案 L (連結的資料集) | 專案 E 的輸出規則  專案 R 的輸入規則 |

## 更新商店資訊

更新清單時 (例如修改受限匯出政策)，BigQuery 共用功能會使用背景工作站，將這些變更套用至相關聯的連結資料集。如果 VPC Service Controls perimeter 設有 IP 限制，保護 Google Cloud 專案，perimeter 可能會封鎖來自 Google 基礎架構的背景 worker，導致連結的資料集無法同步。

如要讓背景工作站更新連結的資料集，請設定輸入或輸出規則，讓執行 API 呼叫的使用者或服務帳戶略過 IP 限制。

如要修改訂閱者專案 perimeter 的輸入政策，請新增輸入規則，允許呼叫主體從任何來源 IP 位址 (`*`) 存取 `bigquery.googleapis.com` 服務：

```
- ingressFrom:
    sources:
      - accessLevel: "*"
    identities:
      - "user:CALLING_USER_EMAIL"
      - "serviceAccount:AUTOMATION_SA_EMAIL"
  ingressTo:
    resources:
      - "projects/SUBSCRIBER_PROJECT_NUMBER"
    operations:
      - serviceName: "bigquery.googleapis.com"
        methodSelectors:
          - method: "*"
```

或者，如要修改發布者 perimeter 的輸出政策，請將呼叫身分新增至訂閱者專案輸出規則中的 `identities` 清單：

```
- egressFrom:
    identities:
      - "user:CALLING_USER_EMAIL"
      - "serviceAccount:AUTOMATION_SA_EMAIL"
  egressTo:
    resources:
      - "projects/SUBSCRIBER_PROJECT_NUMBER"
    operations:
      - serviceName: "bigquery.googleapis.com"
        methodSelectors:
          - method: "*"
```

更改下列內容：

* `CALLING_USER_EMAIL`：執行 API 呼叫來更新產品資訊的使用者電子郵件地址。如果更新是由真人使用者執行，請加入這個身分。
* `AUTOMATION_SA_EMAIL`：服務帳戶的電子郵件地址，該帳戶會執行 API 呼叫來更新商家資訊。如果是由自動化程序或指令碼進行更新，請加入這個身分。
* `SUBSCRIBER_PROJECT_NUMBER`：訂閱者專案的專案編號，該專案包含連結的資料集。

## 查詢連結資料集中的資料表

在下圖中，呼叫端專案和包含連結資料集的專案位於不同的 service perimeter：

**圖 4**：查詢連結資料集的 VPC Service Controls 規則。

圖 4 顯示下列元件：

* **呼叫端**：BigQuery sharing 訂閱者，或連結資料集的任何 BigQuery 工作使用者。
* **專案 R**：呼叫端專案。
* **專案 L**：託管連結資料集的專案。
* **專案 V**：託管共用資料集 (包含資料表) 的專案。

如果您是 BigQuery sharing 訂閱者，在查詢連結資料集中的資料表時，必須新增下列輸入和輸出規則：

| 專案 | 規則 |
| --- | --- |
| Project R | 專案 L 的輸出規則 |
| 專案 L (連結的資料集) | 專案 R 的輸入規則 |

## 查詢連結資料集中的檢視表

本節說明查詢連結資料集中的檢視表時，必須遵守的 VPC Service Controls 規則。規則會因檢視表和基礎資料表是否位於相同專案而異。

### 檢視表和基礎資料表位於不同專案

在下圖中，包含連結資料集的專案，以及與檢視表相關聯的基礎資料表，位於不同的 service perimeter。檢視表 (專案 S) 和與檢視表相關聯的基礎資料表 (專案 V) 位於不同專案：

**圖 5.** 當檢視表和基礎資料表位於不同專案時，查詢檢視表的 VPC Service Controls 規則。

圖 5 顯示下列元件：

* **呼叫端**：BigQuery sharing 訂閱者，或連結資料集的任何 BigQuery 工作使用者。
* **專案 R**：呼叫端專案。
* **專案 L**：託管連結資料集的專案。
* **專案 S**：託管共用資料集的專案。
* **專案 V**：託管資料集的專案，其中包含與檢視表相關聯的基礎資料表。

如果您是 BigQuery sharing 訂閱者，在連結的資料集中查詢檢視表時，必須新增下列輸入和輸出規則：

| 專案 | 規則 |
| --- | --- |
| Project R | 專案 L 的輸出規則  專案 V 的輸出規則 |
| 專案 L (連結的資料集) | 專案 R 的輸入規則  專案 V 的輸出規則 |
| Project V | 專案 L 的輸出規則  專案 R 的輸入規則 |

### 檢視表和基礎資料表位於同一個專案

在下圖中，檢視表 (Project V) 和與檢視表 (Project V) 相關聯的基礎資料表位於同一個專案中：

**圖 6**：當檢視表和基礎資料表位於相同專案時，查詢檢視表的 VPC Service Controls 規則。

圖 6 顯示下列元件：

* **呼叫端**：BigQuery sharing 訂閱者，或連結資料集的任何 BigQuery 工作使用者。
* **專案 R**：呼叫端專案。
* **專案 L**：託管連結資料集的專案。
* **專案 V**：託管檢視表和與檢視表相關聯的基礎資料表的專案。

如果您是 BigQuery sharing 訂閱者，在連結的資料集中查詢檢視表時，必須新增下列輸入和輸出規則：

| 專案 | 規則 |
| --- | --- |
| Project R | 專案 L 的輸出規則 |
| 專案 L (連結的資料集) | 專案 R 的輸入規則 |

## 查詢連結資料集中的授權檢視表

在下圖中，授權檢視表和與授權檢視表 (專案 V) 相關聯的基礎資料表位於同一個專案中：

**圖 7.**VPC Service Controls 規則，用於查詢連結資料集中的授權檢視表。

圖 7 顯示下列元件：

* **呼叫端**：BigQuery sharing 訂閱者，或連結資料集的任何 BigQuery 工作使用者。
* **專案 R**：呼叫端專案。
* **專案 L**：託管連結資料集的專案。
* **專案 V**：這個專案託管授權檢視表，以及與檢視表相關聯的基礎資料表。

**注意：** 如果共用資料集和與授權檢視表相關聯的基礎資料表不在同一個專案和 VPC Service Controls service perimeter 內，service perimeter 會拒絕訂閱者的查詢。如要解決這個問題，請確認共用資料集和與授權檢視表相關聯的基礎資料表位於同一個專案。

如果您是 BigQuery sharing 訂閱者，在連結資料集中查詢授權檢視表時，必須新增下列輸入和輸出規則：

| 專案 | 規則 |
| --- | --- |
| Project R | 專案 L 的輸出規則 |
| 專案 L (連結的資料集) | 專案 R 的輸入規則 |

## 後續步驟

* 瞭解如何[排解 VPC Service Controls 問題](https://docs.cloud.google.com/vpc-service-controls/docs/troubleshooting?hl=zh-tw)。
* 瞭解[輸入和輸出規則](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw)。
* 瞭解如何[設定輸入和輸出政策](https://docs.cloud.google.com/vpc-service-controls/docs/configuring-ingress-egress-policies?hl=zh-tw)。
* 瞭解如何[建立產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)。
* 瞭解如何[訂閱產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)。
* 瞭解[共用稽核記錄](https://docs.cloud.google.com/bigquery/docs/analytics-hub-audit-logging?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-21 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-21 (世界標準時間)。"],[],[]]