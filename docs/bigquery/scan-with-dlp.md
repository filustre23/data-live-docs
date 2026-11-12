Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Sensitive Data Protection 掃描 BigQuery 資料

Sensitive Data Protection 可讓您檢查 BigQuery 資料表，在資料集成長和變更時，識別、管理及保護機密資料。定期掃描有助於符合法規遵循要求，並降低信用卡號碼、醫療資訊、身分證字號、駕照號碼、地址、全名和公司專屬機密等詳細資料外洩的風險。

本文說明如何從 Google Cloud 控制台的「BigQuery」**BigQuery**頁面執行隨選檢查。如要進一步瞭解 Sensitive Data Protection，請參閱 [Sensitive Data Protection 說明文件](https://docs.cloud.google.com/sensitive-data-protection/docs?hl=zh-tw)。

## 掃描 BigQuery 資料的方法

Sensitive Data Protection 是一項全代管服務，可讓您大規模識別及保護機密資料。Sensitive Data Protection 使用超過 150 個預先定義的偵測工具，來識別模式、格式和總和檢查碼。Sensitive Data Protection 也提供一組工具，可對資料進行去識別化處理，包括遮蓋、代碼化、假名化和日期移位，且不會複製客戶資料。

掃描 BigQuery 資料的方式有兩種：

* **機密資料剖析。**Sensitive Data Protection 可針對組織、資料夾或專案中的 BigQuery 資料產生設定檔。*資料剖析檔*包含資料表的指標和中繼資料，可協助您判斷[機密和高風險資料](https://docs.cloud.google.com/sensitive-data-protection/docs/sensitivity-risk-calculation?hl=zh-tw)的存放位置。Sensitive Data Protection 會在專案、資料表和資料欄層級回報這些指標。詳情請參閱「[BigQuery 資料剖析](https://docs.cloud.google.com/sensitive-data-protection/docs/data-profiles?hl=zh-tw)」。
* **隨選檢查：**Sensitive Data Protection 可對單一資料表或部分資料欄執行深度檢查，並回報儲存格層級的發現項目。這類檢查可協助您找出特定資料[類型](https://docs.cloud.google.com/sensitive-data-protection/docs/infotypes-reference?hl=zh-tw)的個別例項，例如表格儲存格中信用卡號碼的精確位置。您可以透過Google Cloud 控制台中的 Sensitive Data Protection 頁面、 Google Cloud 控制台中的「BigQuery」**BigQuery**頁面，或透過 DLP API 以程式輔助方式，執行隨選檢查。

## 事前準備

1. 請先熟悉 [Sensitive Data Protection 定價](https://cloud.google.com/sensitive-data-protection/pricing?hl=zh-tw)和[控管 Sensitive Data Protection 費用的方法](https://docs.cloud.google.com/sensitive-data-protection/docs/best-practices-costs?hl=zh-tw)。
2. [啟用 DLP API](https://docs.cloud.google.com/apis/docs/enable-disable-apis?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=dlp.googleapis.com&hl=zh-tw)
3. 確認建立 Sensitive Data Protection 工作的
   使用者具備適當的預先定義 Sensitive Data Protection
   [Identity and Access Management (IAM) 角色](https://docs.cloud.google.com/sensitive-data-protection/docs/iam-roles?hl=zh-tw)，
   或有足夠的[權限](https://docs.cloud.google.com/sensitive-data-protection/docs/iam-permissions?hl=zh-tw)
   可執行 Sensitive Data Protection 工作。

**注意：** 啟用 DLP API 時，系統會建立服務帳戶，名稱類似於 `service-project_number@dlp-api.iam.gserviceaccount.com`。這個服務帳戶已取得 DLP API 服務代理角色，可使用 BigQuery API 進行驗證。詳情請參閱 Sensitive Data Protection IAM 權限頁面的「[服務帳戶](https://docs.cloud.google.com/sensitive-data-protection/docs/iam-permissions?hl=zh-tw#service_account)」一節。

## 使用 Google Cloud 控制台掃描 BigQuery 資料

如要掃描 BigQuery 資料，請建立 Sensitive Data Protection 工作來分析資料表。您可以在 BigQuery Google Cloud 控制台，使用「Scan with Sensitive Data Protection」(使用 Sensitive Data Protection 掃描) 選項，快速掃描 BigQuery 資料表。

如要使用 Sensitive Data Protection 掃描 BigQuery 資料表，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
4. 依序點選**「總覽」>「資料表」**，然後選取資料表。
5. 在詳細資料窗格中，依序點選
   **「More」(更多) >「Scan with Sensitive Data Protection」(使用 Sensitive Data Protection 掃描)**。
   Sensitive Data Protection 工作建立頁面會在新分頁中開啟。
6. 在「步驟 1：選擇輸入資料」部分，輸入工作 ID。系統會自動產生「Location」(位置) 區段中的值。此外，「Sampling」(取樣) 區段會自動設定為對資料執行取樣掃描，但您可以視需要調整設定。
7. 按一下「繼續」。
8. 選用步驟：在「Step 2: Configure detection」(步驟 2：設定偵測作業)，您可以設定要尋找的資料類型，稱為 `infoTypes`。

   執行下列其中一個步驟：

   * 如要從預先定義的 `infoTypes` 清單中選取，請按一下「Manage infoTypes」(管理 infoType)。接著，選取要搜尋的 infoType。
   * 如要使用現有的[檢查範本](https://docs.cloud.google.com/sensitive-data-protection/docs/creating-templates-inspect?hl=zh-tw)，請在「Template name」(範本名稱) 欄位中輸入範本的完整資源名稱。

   如要進一步瞭解 `infoTypes`，請參閱 Sensitive Data Protection 說明文件中的「[infoType 和 infoType 偵測工具](https://docs.cloud.google.com/sensitive-data-protection/docs/concepts-infotypes?hl=zh-tw)」。
9. 按一下「繼續」。
10. 選用：在「Step 3: Add actions」(步驟 3：新增動作) 部分，開啟「Save to BigQuery」(儲存至 BigQuery)，將 Sensitive Data Protection 發現項目發布至 BigQuery 資料表。如未儲存發現項目，已完成的工作只會包含與發現項目數量和 `infoTypes` 相關的統計資料。將發現項目儲存至 BigQuery，即可儲存精確位置的詳細資料，以及各個發現項目的可信度。
11. 選用：如果您已開啟「Save to BigQuery」(儲存至 BigQuery)，請在「Save to BigQuery」(儲存至 BigQuery) 區段中輸入下列資訊：

    * **專案 ID**：儲存結果的專案 ID。
    * **資料集 ID**：儲存結果的資料集名稱。
    * 選用：**資料表 ID**：儲存結果的資料表名稱。如果未指定資料表 ID，系統會為新資料表指派類似此例的預設名稱：`dlp_googleapis_date_1234567890`。如果您指定現有的資料表，發現項目就會附加至該資料表。

    如要納入偵測到的實際內容，請開啟「包含引言」。
12. 按一下「繼續」。
13. 選用：在「Step 4: Schedule」(步驟 4：時間表) 部分，選取「Specify time span」(指定時間範圍) 或「Create a trigger to run the job on a periodic schedule」(建立觸發條件來定期執行工作)，設定時間範圍或時間表。
14. 按一下「繼續」。
15. 選用：在「Review」(檢查) 頁面中，檢查工作詳細資料。視需要調整先前的設定。
16. 點選「建立」。
17. Sensitive Data Protection 工作完成後，系統會將您重新導向至工作詳細資料頁面，並透過電子郵件通知您。您可以在工作詳細資料頁面查看掃描結果，也可以點選工作完成電子郵件中的連結，前往 Sensitive Data Protection 工作詳細資料頁面。
18. 如果您選擇將 Sensitive Data Protection 發現項目發布至 BigQuery，請在「Job details」(工作詳細資料) 頁面中，按一下「View Findings in BigQuery」(在 BigQuery 中查看發現項目)，在 Google Cloud 控制台中開啟資料表。接下來，您可以查詢資料表和分析發現項目。如要進一步瞭解如何在 BigQuery 中查詢結果，請參閱 Sensitive Data Protection 說明文件中的「[查詢 Sensitive Data Protection 在 BigQuery 的發現結果](https://docs.cloud.google.com/sensitive-data-protection/docs/querying-findings?hl=zh-tw)」。

## 後續步驟

* 進一步瞭解如何[使用 Sensitive Data Protection 檢查 BigQuery 和其他儲存空間存放區中的機密資料](https://docs.cloud.google.com/sensitive-data-protection/docs/inspecting-storage?hl=zh-tw)。
* 進一步瞭解如何[剖析組織、資料夾或專案中的資料](https://docs.cloud.google.com/sensitive-data-protection/docs/data-profiles?hl=zh-tw)。
* 閱讀「身分與安全性」網誌文章：[掌握資料控管權：使用 Sensitive Data Protection 去識別化及模糊處理機密資訊](https://cloud.google.com/blog/products/identity-security/taking-charge-of-your-data-using-cloud-dlp-to-de-identify-and-obfuscate-sensitive-information?hl=zh-tw)。

如要遮蓋或以其他方式去識別化 Sensitive Data Protection 掃描發現的機密資料，請參閱下列內容：

* [檢查文字，將機密資訊去識別化](https://docs.cloud.google.com/sensitive-data-protection/docs/inspect-sensitive-text-de-identify?hl=zh-tw)
* Sensitive Data Protection 說明文件中的「[將機密資料去識別化](https://docs.cloud.google.com/sensitive-data-protection/docs/deidentify-sensitive-data?hl=zh-tw)」
* [GoogleSQL 中的 AEAD 加密概念](https://docs.cloud.google.com/bigquery/docs/aead-encryption-concepts?hl=zh-tw)：瞭解如何加密資料表中的個別值
* [使用 Cloud KMS 金鑰保護資料](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)：瞭解如何在 [Cloud KMS](https://docs.cloud.google.com/kms/docs?hl=zh-tw) 建立及管理自己的加密金鑰，以便加密 BigQuery 資料表




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]