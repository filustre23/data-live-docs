* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 共用 VPC Service Controls 規則

本文說明輸入和輸出規則，讓 BigQuery sharing (原為 Analytics Hub) 中的發布者和訂閱者，存取具有 VPC Service Controls 邊界的專案資料。本文假設您已熟悉 [VPC Service Controls 範圍](https://docs.cloud.google.com/vpc-service-controls/docs/service-perimeters?hl=zh-tw)、[共用資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#shared_datasets)、[資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)、[資訊主頁](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)和[連結資料集](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)。

*呼叫端專案*是指啟動要求的網路或用戶端 Google Cloud 專案，例如 SQL 查詢或 Google Cloud CLI 指令。

## 建立資料交換庫

在下圖中，包含資料交換和共用資料集的專案位於不同的服務安全防護範圍：

**圖 1.** 建立資料交換的 VPC Service Controls 規則。

圖 1 標示了下列元件：

* **呼叫端**：BigQuery 共用管理員。
* **專案 R**：呼叫端專案。
* **專案 E**：主機代管資料交換庫和清單。

身為 BigQuery sharing 管理員，如果您在與呼叫端專案不同的專案中[建立資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#create-exchange)，則必須新增下列輸入和輸出規則：

| **專案** | **規則** |
| --- | --- |
| Project R | 專案 E 的輸出規則 |
| 專案 E (資料交換) | 專案 R 的輸入規則 |

## 建立商家資訊

在下圖中，包含資料交換和共用資料集的專案位於不同的服務安全防護範圍：

**圖 2**：建立房源資訊的 VPC Service Controls 規則。

圖 2 標示了下列元件：

* **呼叫端**：BigQuery 共用管理員或發布者。
* **專案 R**：呼叫端專案。
* **專案 E**：主機代管資料交換庫和清單。
* **專案 S**：代管共用資料集。

如果您在資料交易所建立的資訊公開項目與共用資料集位於不同專案，則必須新增下列輸入和輸出規則，允許 BigQuery 共用發布者建立資訊公開項目：

| **專案** | **規則** |
| --- | --- |
| Project R | 專案 E 的輸出規則  專案 S 的輸出規則 |
| 專案 E (資料交換) | 專案 S 的輸出規則  專案 R 的輸入規則 |
| 專案 S (共用資料集) | 專案 E 的輸出規則  專案 R 的輸入規則 |

## 訂閱產品資訊

在下圖中，包含商家資訊和該商家資訊連結資料集的專案位於不同的服務範圍：

**圖 3**：訂閱資訊的 VPC Service Controls 規則。

圖 3 標示了下列元件：

* **呼叫端**：BigQuery 共用訂閱者。
* **專案 R**：呼叫端專案。
* **專案 E**：主機代管資料交換庫和清單。
* **專案 L**：代管連結的資料集。

如果您是 BigQuery 共用訂閱者，且訂閱的資料交易所屬專案與您的專案不同，則必須新增下列輸入和輸出規則：

| **專案** | **規則** |
| --- | --- |
| Project R | 專案 E 的輸出規則  專案 L 的輸出規則 |
| 專案 E (房源) | 專案 L 的輸出規則  專案 R 的輸入規則 |
| 專案 L (連結的資料集) | 專案 E 的輸出規則  專案 R 的輸入規則 |

## 查詢連結資料集中的資料表

在下圖中，呼叫端專案和包含連結資料集的專案位於不同的服務範圍：

**圖 4**：查詢連結資料集的 VPC Service Controls 規則。

圖 4 標示了下列元件：

* **呼叫端**：BigQuery 共用訂閱者或連結資料集的任何 BigQuery 工作使用者。
* **專案 R**：呼叫端專案。
* **專案 L**：代管連結的資料集。
* **專案 V**：代管含有資料表的共用資料集。

如果您是 BigQuery 共用訂閱者，在連結的資料集中查詢資料表時，必須新增下列輸入和輸出規則：

| **專案** | **規則** |
| --- | --- |
| Project R | 專案 L 的輸出規則 |
| 專案 L (連結的資料集) | 專案 R 的輸入規則 |

## 查詢連結資料集中的檢視區塊

本節說明查詢連結資料集中的檢視區塊時，所需的 VPC Service Controls 規則。規則會因檢視區塊及其基礎資料表是否位於同一專案或不同專案而異。

### 情境 1

在下圖中，包含連結資料集的專案，以及與檢視區塊相關聯的基礎資料表，位於不同的服務安全防護範圍。檢視區塊 (專案 S) 和與檢視區塊相關聯的基礎資料表 (專案 V) 位於不同專案中：

**圖 5.** 查詢連結資料集中的檢視區塊時，適用的 VPC Service Controls 規則。

圖 5 標示了下列元件：

* **呼叫端**：BigQuery 共用訂閱者或連結資料集的任何 BigQuery 工作使用者。
* **專案 R**：呼叫端專案。
* **專案 L**：代管連結的資料集。
* **專案 S**：代管共用資料集。
* **專案 V**：代管包含與檢視區塊相關聯基本資料表的資料集。

如果您是 BigQuery 共用訂閱者，在連結的資料集中查詢檢視區塊時，必須新增下列輸入和輸出規則：

| **專案** | **規則** |
| --- | --- |
| Project R | 專案 L 的輸出規則  專案 V 的輸出規則 |
| 專案 L (連結的資料集) | 專案 R 的輸入規則  專案 V 的輸出規則 |
| Project V | 專案 L 的輸出規則  專案 R 的輸入規則 |

### 情境 2

在下圖中，檢視區塊 (專案 V) 和與檢視區塊 (專案 V) 相關聯的基礎資料表位於同一個專案中：

**圖 6**：查詢連結資料集中的檢視區塊時，適用的 VPC Service Controls 規則。

圖 6 標示了下列元件：

* **呼叫端**：BigQuery 共用訂閱者或連結資料集的任何 BigQuery 工作使用者。
* **專案 R**：呼叫端專案。
* **專案 L**：代管連結的資料集。
* **專案 V**：同時代管檢視區塊和與檢視區塊相關聯的基礎資料表。

如果您是 BigQuery 共用訂閱者，在連結的資料集中查詢檢視區塊時，必須新增下列輸入和輸出規則：

| **專案** | **規則** |
| --- | --- |
| Project R | 專案 L 的輸出規則 |
| 專案 L (連結的資料集) | 專案 R 的輸入規則 |

## 查詢連結資料集中的授權檢視表

在下圖中，授權檢視區塊和與授權檢視區塊 (專案 V) 相關聯的基礎資料表位於同一個專案中：

**圖 7.** 查詢連結資料集中的檢視區塊時，適用的 VPC Service Controls 規則。

圖 7 標示了下列元件：

* **呼叫端**：BigQuery 共用訂閱者或連結資料集的任何 BigQuery 工作使用者。
* **專案 R**：呼叫端專案。
* **專案 L**：代管連結的資料集。
* **專案 V**：同時代管已授權的檢視區塊，以及與該檢視區塊相關聯的基礎資料表。

**注意：** 如果共用資料集和授權檢視區塊相關聯的基礎資料表不在同一個專案和 VPC Service Controls 範圍內，服務範圍會拒絕訂閱者的查詢。如要解決這個問題，請確認共用資料集和與授權檢視畫面相關聯的基底資料表位於同一個專案中。

如果您是 BigQuery 共用訂閱者，在連結的資料集中查詢檢視區塊時，必須新增下列輸入和輸出規則：

| **專案** | **規則** |
| --- | --- |
| Project R | 專案 L 的輸出規則 |
| 專案 L (連結的資料集) | 專案 R 的輸入規則 |

## 限制

BigQuery 共用功能不支援[以方法為準的規則](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw)。如要啟用方法規則，必須允許所有方法。例如：

```
          ingressTo:
            operations:
            - methodSelectors:
              - method: '*'
              serviceName: analyticshub.googleapis.com
            resources:
            - projects/PROJECT_ID
```

如果 BigQuery 資源也受到服務範圍保護，您必須允許 BigQuery 服務的輸入和輸出規則。建立資料交換時，不一定要允許輸入和輸出規則。BigQuery 的進入和退出規則與 BigQuery 共用規則類似。例如：

```
          ingressTo:
            operations:
            - methodSelectors:
              - method: '*'
              serviceName: bigquery.googleapis.com
            resources:
            - projects/PROJECT_ID
```

## 後續步驟

* 瞭解如何[排解 VPC Service Controls 問題](https://docs.cloud.google.com/vpc-service-controls/docs/troubleshooting?hl=zh-tw)。
* 瞭解[輸入和輸出規則](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw)。
* 瞭解如何[設定輸入和輸出政策](https://docs.cloud.google.com/vpc-service-controls/docs/configuring-ingress-egress-policies?hl=zh-tw)。
* 瞭解如何[建立房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw#create_a_listing)。
* 瞭解如何[訂閱房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)。
* 瞭解[共用稽核記錄](https://docs.cloud.google.com/bigquery/docs/analytics-hub-audit-logging?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]