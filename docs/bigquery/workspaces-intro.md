* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 工作區簡介

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或提出與這項預先發布版功能相關的問題，請傳送電子郵件至 [bigquery-repositories-feedback@google.com](mailto:%20bigquery-repositories-feedback@google.com)。

本文將說明 BigQuery 的工作區概念。您可以在[存放區](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw)中使用工作區，編輯存放區中儲存的程式碼。存放區會使用 Git 記錄變更及管理檔案版本，對檔案執行版本管控。

在 BigQuery 頁面中，工作區會依字母順序顯示在相關聯的存放區下方。如要查看存放區，請按照下列步驟操作：

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
2. 在「Explorer」窗格中，點選「Repositories」。

## 支援的檔案類型

您可以建立或上傳下列類型的檔案至存放區：

* SQL 查詢
* Python 筆記本
* [資料畫布](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw)
* [準備資料](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw)
* 任何其他類型的檔案

詳情請參閱「[在工作區中處理檔案](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw#work_with_files_in_a_workspace)」。

## Git 整合

在工作區中建立及修改檔案時，您可以執行 Git 動作，例如提交變更及將變更推送至存放區。詳情請參閱「[使用檔案進行版本管控](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw#use_version_control_with_a_file)」。

## 位置

每個工作區都與包含該工作區的存放區使用相同的[位置](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw#locations)。

## 配額

使用 BigQuery 工作區時，適用 [Dataform 配額](https://docs.cloud.google.com/dataform/docs/quotas?hl=zh-tw#quotas)。

## 定價

建立、更新或刪除工作區，以及在工作區中儲存檔案，都不會產生費用。

若要深入瞭解 BigQuery 價格，請參閱[價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

## 後續步驟

* 如要瞭解如何建立及使用存放區，請參閱「[建立存放區](https://docs.cloud.google.com/bigquery/docs/repositories?hl=zh-tw)」一文。
* 如要瞭解如何建立及使用工作區，請參閱[建立工作區](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw)一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]