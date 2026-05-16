Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Sensitive Data Protection 掃描 BigQuery 資料

瞭解自己的機密資料位於何處，通常是確認能夠妥善保護和管理這些資料的第一步。知道這點有助於降低信用卡號碼、醫療資訊、身分證字號、駕照號碼、地址、全名以及公司特定機密等敏感詳細資訊的暴露風險。此外，定期掃描資料也有助符合法規遵循要求，並確保您可以在資料隨著使用而增加或改變時，採行最佳做法。請使用 Sensitive Data Protection 檢查 BigQuery 資料表，並保護機密資料，以協助符合法規遵循要求。

掃描 BigQuery 資料的方式有兩種：

* **機密資料剖析。**Sensitive Data Protection 可產生機構、資料夾或專案中 BigQuery 資料的剖析檔。*資料剖析檔*包含資料表的指標和中繼資料，可協助您判斷[機密和高風險資料](https://docs.cloud.google.com/sensitive-data-protection/docs/sensitivity-risk-calculation?hl=zh-tw)的存放位置。Sensitive Data Protection 會在專案、資料表和資料欄層級回報這些指標。詳情請參閱 [BigQuery 資料分析器](https://docs.cloud.google.com/sensitive-data-protection/docs/data-profiles?hl=zh-tw)。
* **隨選檢查。**Sensitive Data Protection 可以對單一資料表或部分資料欄執行深入檢查，並回報檢查結果，精確到儲存格層級。這類檢查有助於找出特定[類型](https://docs.cloud.google.com/sensitive-data-protection/docs/infotypes-reference?hl=zh-tw)的個別資料例項，例如表格儲存格內信用卡號碼的確切位置。您可以透過Google Cloud 控制台的「Sensitive Data Protection」頁面、 Google Cloud 控制台的「BigQuery」**BigQuery**頁面，或透過 DLP API 以程式輔助方式，執行隨選檢查。

本頁面說明如何透過 Google Cloud 控制台的「BigQuery」**BigQuery**頁面執行隨選檢查。

Sensitive Data Protection 是一項全代管服務，可讓 Google Cloud 客戶大規模識別及保護機密資料。此服務會運用超過 150 種預先定義的偵測工具來識別模式、格式和總和檢查碼。此外，Sensitive Data Protection 還會提供一組資料去識別化的工具，包括遮蓋、代碼化、匿名化、日期轉移等做法，這些工具都不需要複製客戶資料。

如要進一步瞭解 Sensitive Data Protection，請參閱[這份說明文件](https://docs.cloud.google.com/sensitive-data-protection/docs?hl=zh-tw)。

## 事前準備

1. 瞭解 [Sensitive Data Protection 定價](https://cloud.google.com/sensitive-data-protection/pricing?hl=zh-tw)以及[如何控管 Sensitive Data Protection 費用](https://docs.cloud.google.com/sensitive-data-protection/docs/best-practices-costs?hl=zh-tw)。
2. [啟用 DLP API](https://docs.cloud.google.com/apis/docs/enable-disable-apis?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=dlp.googleapis.com&hl=zh-tw)
3. 確認將預先定義的適當 Sensitive Data Protection [身分與存取權管理角色](https://docs.cloud.google.com/sensitive-data-protection/docs/iam-roles?hl=zh-tw)或充分的[權限](https://docs.cloud.google.com/sensitive-data-protection/docs/iam-permissions?hl=zh-tw)授予建立 Sensitive Data Protection 工作的使用者，以利其執行 Sensitive Data Protection 工作。

**附註：** 當您啟用 DLP API 後，系統會建立名稱類似 `service-project_number@dlp-api.iam.gserviceaccount.com` 的服務帳戶。系統會將 DLP API 服務代理人角色授予此服務帳戶，因而使服務帳戶能夠透過 BigQuery API 進行驗證。詳情請參閱 Sensitive Data Protection 身分與存取權管理權限頁面上的[服務帳戶](https://docs.cloud.google.com/sensitive-data-protection/docs/iam-permissions?hl=zh-tw#service_account)一節。

## 使用 Google Cloud 控制台掃描 BigQuery 資料

如要掃描 BigQuery 資料，請建立 Sensitive Data Protection 資料表分析工作。您可以使用 BigQuery Google Cloud 控制台中的「使用 Sensitive Data Protection 掃描」選項，快速掃描 BigQuery 資料表。

如何使用 Sensitive Data Protection 掃描 BigQuery 資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「Explorer」explore：

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下資料集。
4. 依序按一下「總覽」**>「表格」**，然後選取所需表格。
5. 依序點選「開啟」**>「透過 Sensitive Data Protection 掃描」**。
   系統會在新分頁中開啟 Sensitive Data Protection 工作建立頁面。
6. 在「步驟 1：選擇輸入資料」中，輸入工作 ID。「Location」(位置) 部分的值會自動產生。此外，還會自動設定「Sampling」(取樣) 區段以針對資料執行範例掃描，但您可以視需要調整設定。
7. 按一下「繼續」。
8. 選用步驟：您可以在**步驟 2：**「Configure detection」(設定偵測作業) 中設定要尋找的資料類型 (稱為 `infoTypes`)。

   執行下列其中一個步驟：

   * 如要從預先定義的 `infoTypes` 清單中選取，請按一下「管理 infoType」。然後選取要搜尋的 infoType。
   * 如要使用現有的[檢查範本](https://docs.cloud.google.com/sensitive-data-protection/docs/creating-templates-inspect?hl=zh-tw)，請在「範本名稱」欄位中輸入範本的完整資源名稱。

   如要進一步瞭解 `infoTypes`，請參閱 Sensitive Data Protection 說明文件中的「[InfoTypes 及 infoType 偵測工具](https://docs.cloud.google.com/sensitive-data-protection/docs/concepts-infotypes?hl=zh-tw)」一文。
9. 按一下「繼續」。
10. 選用：在**步驟 3：**「Add actions」(新增動作) 中，開啟「Save to BigQuery」(儲存至 BigQuery)，以將 Sensitive Data Protection 發現項目發布至 BigQuery 資料表。如果您未儲存發現項目，已完成的工作只會包含發現項目的數量及其 `infoTypes` 的相關統計資料。將發現項目儲存至 BigQuery，即可儲存精確位置的詳細資料，以及各個發現項目的可信度。
11. 選用：如果您已開啟「Save to BigQuery」(儲存至 BigQuery)，請在「Save to BigQuery」(儲存至 BigQuery) 區段中輸入下列資訊：

    * **專案 ID**：儲存結果的專案 ID。
    * 「Dataset ID」(資料集 ID)：儲存結果的資料集名稱。
    * 選用：「Table ID」(資料表 ID)：儲存結果的資料表名稱。如果未指定資料表 ID，系統會為新資料表指派類似此例的預設名稱：`dlp_googleapis_date_1234567890`。如果您指定現有的資料表，發現項目就會附加至該資料表。

    如要納入偵測到的實際內容，請開啟「包含引言」。
12. 按一下「繼續」。
13. 選用：在**步驟 4：**「Schedule」(排程) 中，選取「Specify time span」(指定時距) 或「Create a trigger to run the job on a periodic schedule」(建立觸發條件來定期執行工作) 以設定時距或排程。
14. 按一下「繼續」。
15. 選用：在「Review」(審查) 頁面上，檢查工作的詳細資料。視需要調整先前的設定。
16. 點選「建立」。
17. Sensitive Data Protection 工作完成後，系統會將您重新導向至工作詳細資料頁面，並且透過電子郵件通知您。您可以在工作詳細資料頁面上查看掃描結果，或是在工作完成電子郵件中按一下 Sensitive Data Protection 工作詳細資料頁面的連結。
18. 如果您選擇將 Sensitive Data Protection 發現項目發布至 BigQuery，請在「Job details」(工作詳細資料) 頁面上按一下「View Findings in BigQuery」(在 BigQuery 中查看發現項目)，藉此在 Google Cloud 控制台中開啟資料表。接下來，您可以查詢資料表和分析發現項目。如要進一步瞭解如何在 BigQuery 中查詢結果，請參閱 Sensitive Data Protection 說明文件中的「[在 BigQuery 中查詢 Sensitive Data Protection 發現項目](https://docs.cloud.google.com/sensitive-data-protection/docs/querying-findings?hl=zh-tw)」一文。

## 後續步驟

* 進一步瞭解如何[使用 Sensitive Data Protection 檢查 BigQuery 和其他儲存空間存放區是否有機密資料](https://docs.cloud.google.com/sensitive-data-protection/docs/inspecting-storage?hl=zh-tw)。
* 進一步瞭解如何[剖析機構、資料夾或專案中的資料](https://docs.cloud.google.com/sensitive-data-protection/docs/data-profiles?hl=zh-tw)。
* 請參閱「身分識別與安全性」網誌文章：[使用 Sensitive Data Protection 管理您的資料，以去識別化及模糊處理機密資訊](https://cloud.google.com/blog/products/identity-security/taking-charge-of-your-data-using-cloud-dlp-to-de-identify-and-obfuscate-sensitive-information?hl=zh-tw)。

如果要遮蓋或用其他方式將機密資料保護掃描找到的機密資料去識別化，請參閱下列文章：

* [檢查文字，將機密資訊去識別化](https://docs.cloud.google.com/sensitive-data-protection/docs/inspect-sensitive-text-de-identify?hl=zh-tw)
* Sensitive Data Protection 說明文件中的[將機密資料去識別化](https://docs.cloud.google.com/sensitive-data-protection/docs/deidentify-sensitive-data?hl=zh-tw)資訊
* [GoogleSQL 中的 AEAD 加密概念](https://docs.cloud.google.com/bigquery/docs/aead-encryption-concepts?hl=zh-tw)，以取得在資料表中加密個別值的相關資訊
* [使用 Cloud KMS 金鑰保護資料](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)，藉此瞭解如何在 [Cloud KMS](https://docs.cloud.google.com/kms/docs?hl=zh-tw) 中建立及管理您自己的加密金鑰，用以加密 BigQuery 資料表




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]