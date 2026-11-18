Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 存放區和工作區簡介

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：**如要提供意見回饋或提出與這項預先發布版功能相關的問題，請傳送電子郵件至 [bigquery-repositories-feedback@google.com](mailto:bigquery-repositories-feedback@google.com)。

BigQuery 存放區和工作區可讓您對程式碼資產 (例如 SQL 查詢、Python 筆記本、資料畫布和資料準備) 套用 Git 版本管控。版本管控功能可協助您追蹤檔案變更、與團隊協作而不覆寫共用工作，並在需要時還原至先前的修訂版本。共用程式碼集會儲存在內建或連結的第三方 Git 存放區。接著，您可以使用個別工作區編輯檔案、修訂變更，以及推送或提取分支版本之間的更新。

如要使用資料夾版本管控功能，建議您使用 [BigQuery Studio Git 存放區](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw)。這項整合功能可讓您直接在 BigQuery Studio 檔案瀏覽器中使用 Git 分支版本，並一次複製多個存放區，不必管理個別工作區。

## 存放區

BigQuery 存放區的功能與 Git 存放區相同，可為您在 BigQuery 中使用的檔案提供版本管控。您可以使用 BigQuery 內建的 Git 功能，或連結至現有的第三方 Git 存放區。您可以在每個存放區建立[工作區](#workspaces)，編輯儲存在其中的程式碼。

如要進一步瞭解如何建立及管理存放區，請參閱「[建立及管理存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw)」。

## 工作區

您可以在 BigQuery 的工作區編輯及管理儲存在[存放區](#repositories)中的程式碼。您可以在工作區建立及修改檔案，而上層存放區會使用 Git 記錄變更及管理檔案版本。

如要進一步瞭解如何建立及管理工作區，請參閱「[建立及管理工作區](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw)」。

## 位置

您可以在所有 [BigQuery Studio 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqstudio-loc)建立存放區。存放區中的每個工作區都使用與存放區相同的位置。

## 配額

使用 BigQuery 工作區和存放區時，須遵守 [Dataform 配額](https://docs.cloud.google.com/dataform/docs/quotas?hl=zh-tw#quotas)。

## 定價

建立、更新或刪除存放區或工作區，或儲存工作區中的檔案，都不會產生費用。

如要進一步瞭解 BigQuery 定價，請參閱「[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」一文。

## 後續步驟

* 如要瞭解如何使用 BigQuery Studio Git 存放區管理程式碼，請參閱「[使用 BigQuery Studio Git 存放區管理程式碼](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw)」。
* 如要瞭解如何建立及使用存放區，請參閱「[建立及管理存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw)」。
* 如要瞭解如何建立及使用工作區，請參閱「[建立及管理工作區](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-18 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-18 (世界標準時間)。"],[],[]]