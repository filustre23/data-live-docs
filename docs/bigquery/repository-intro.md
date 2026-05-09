Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 存放區簡介

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或提出與這項預先發布版功能相關的問題，請傳送電子郵件至 [bigquery-repositories-feedback@google.com](mailto:%20bigquery-repositories-feedback@google.com)。

本文說明 BigQuery 中的存放區概念。您可以使用存放區，對 BigQuery 中使用的檔案執行版本管控。BigQuery 會使用 Git 記錄變更及管理檔案版本。

每個 BigQuery 存放區都代表一個 Git 存放區。您可以使用 BigQuery 的內建 Git 功能，也可以連線至第三方 Git 存放區。在每個存放區中，您可以建立一或多個[工作區](https://docs.cloud.google.com/bigquery/docs/workspaces-intro?hl=zh-tw)，編輯存放區中儲存的程式碼。

如要查看存放區，請前往 BigQuery 頁面，在左側窗格中依序點選「Explorer」explore和「Repositories」。存放區會依字母順序顯示在詳細資料窗格的新分頁中。

**重要事項：** 如果您在 BigQuery 存放區中建立資產 (例如查詢、筆記本 (包括含 Apache Spark 工作的筆記本)、BigQuery 管道或 Dataform 工作流程)，就無法在 BigQuery 存放區中排定執行時間。如要排定及執行 Dataform 工作流程，您必須使用 Dataform 存放區。如要排定查詢和筆記本的執行時間，請使用 BigQuery Studio。詳情請參閱「[排定查詢時間](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)」、「[排定筆記本時間](https://docs.cloud.google.com/bigquery/docs/orchestrate-notebooks?hl=zh-tw)」和「[排定管道時間](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)」。

## 第三方存放區

您可以視需要將 BigQuery 存放區連結至第三方 Git 存放區。在本例中，第三方存放區會儲存存放區程式碼，而非 BigQuery。BigQuery 會與第三方存放區互動，讓您在 BigQuery 工作區中編輯及執行存放區內容。視您選擇的存放區類型而定，您可以使用 SSH 或 HTTPS 連線至第三方存放區。

下表列出支援的 Git 供應商，以及其存放區可用的連線方法：

| Git 供應商 | 連線方法 |
| --- | --- |
| Microsoft Azure DevOps Services | SSH |
| Bitbucket | SSH |
| GitHub | SSH 或 HTTPS |
| GitLab | SSH 或 HTTPS |

詳情請參閱「[連線至第三方存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw#connect-third-party)」。

## 服務帳戶

所有 BigQuery 存放區都會連結至預設的 Dataform 服務代理程式。這個服務帳戶是根據專案編號產生，格式如下：

```
service-YOUR_PROJECT_NUMBER@gcp-sa-dataform.iam.gserviceaccount.com
```

系統會強制執行[嚴格的「以…身分執行」模式](https://docs.cloud.google.com/dataform/docs/strict-act-as-mode?hl=zh-tw)，並要求所有存放區使用自訂服務帳戶或 Google 帳戶的使用者憑證，才能排定管道和筆記本的執行時間。

## 位置

您可以在所有 [BigQuery Studio 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqstudio-loc)建立存放區。

## 配額

使用 BigQuery 存放區時，適用 [Dataform 配額](https://docs.cloud.google.com/dataform/docs/quotas?hl=zh-tw#quotas)。

## 定價

建立、更新或刪除存放區無須付費。

若要深入瞭解 BigQuery 價格，請參閱[價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

## 後續步驟

* 瞭解如何[建立存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw)。
* 瞭解如何[建立工作區](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]