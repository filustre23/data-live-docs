Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 稽核政策標記

本文件說明如何使用 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw) 稽核政策標記相關活動。舉例來說，您可以決定：

* 授予或移除政策標記存取權的主體電子郵件地址
* 獲得授權或遭撤銷權限的使用者電子郵件地址
* 存取權異動的政策標記

## 存取記錄檔

如要進一步瞭解查看記錄所需的權限，請參閱 [Cloud Logging 存取權控管指南](https://docs.cloud.google.com/logging/docs/access-control?hl=zh-tw)。

## 查看政策標記事件的記錄

1. 前往 Google Cloud 控制台的「Logs Explorer」頁面。

   [前往「Logs Explorer」](https://console.cloud.google.com/logs/query?hl=zh-tw)
2. 在資源下拉式選單中，依序點選「Audited Resource」和「Audited Resources」，然後點選「datacatalog.googleapis.com」。您會看到 Data Catalog 資源的近期稽核記錄項目。
3. 如要查看記錄項目，請選取 Data Catalog `SetIamPolicy` 方法。
4. 按一下記錄項目，即可查看對 `SetIamPolicy` 方法的呼叫詳細資料。
5. 按一下記錄項目欄位，即可查看 `SetIamPolicy` 項目的詳細資料。

   * 按一下 `protoPayload`，然後點選 `authenticationInfo`，即可查看設定 IAM 政策實體的 `principalEmail`。
   * 按一下 `protoPayload`、`request` 和 `policy`，然後按一下 `bindings`，即可查看已變更的繫結 (包括主體和角色)。

## 後續步驟

瞭解[政策標記的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]