Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料位置和傳輸

無論來源資料儲存在何處，BigQuery 資料移轉服務都能將外部來源的資料移轉至 BigQuery。移轉設定會自動使用目的地資料集的位置，暫存及處理資料，但某些資料倉儲遷移作業需要共置的暫存資源。如要進一步瞭解 BigQuery 位置，請參閱「[資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)」。

## 轉移位置

移轉設定有位置。設定移轉設定時，請在與目的地資料集相同的專案中設定。移轉設定的位置會自動設為您為目的地資料集指定的位置。BigQuery 資料移轉服務會在與目的地 BigQuery 資料集相同的位置處理及暫存資料。如果在建立移轉作業時沒有目的地資料集，則必須先在 BigQuery 中建立資料集，再設定移轉作業。

## 來源資料位置

要移轉至 BigQuery 的來源資料可能會有位置。不過，來源資料的儲存位置與 BigQuery 中目的地資料集的位置無關。

## 資料倉儲遷移作業的位置考量

從 [Teradata](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw) 遷移資料倉儲時，必須使用 Cloud Storage bucket 做為移轉程序的一部分。Cloud Storage bucket 必須與 BigQuery 目的地資料集位於相同位置。

Redshift 資料倉儲遷移作業不需要共置的 Cloud Storage bucket。

**重點提示：** 您可以複製資料集，或手動將資料集移至其他位置。詳情請參閱「[管理資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw)」。如要進一步瞭解如何使用 Cloud Storage 儲存及移動大型資料集，請參閱「[搭配使用 Cloud Storage 與大數據](https://docs.cloud.google.com/storage/docs/working-with-big-data?hl=zh-tw)」。

## 後續步驟

* 查看[全球各地提供的所有 Google Cloud 服務](https://cloud.google.com/about/locations/?hl=zh-tw#region)。
* [探索其他以位置為基礎的概念](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw)，例如適用於其他 Google Cloud 服務的可用區。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]