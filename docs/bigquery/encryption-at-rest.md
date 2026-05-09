Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 靜態資料加密

根據預設，BigQuery 會加密靜態客戶內容。BigQuery 會為您處理加密作業，您不必採取任何其他動作。這項做法稱為「Google 預設加密機制」。
Google 預設加密功能使用的強化金鑰管理系統，與我們加密自家資料時使用的系統相同。這些系統包括嚴格的金鑰存取權控管與稽核措施。每個 BigQuery 物件的資料和中繼資料都使用[進階加密標準 (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) 進行加密。

如要控管加密金鑰，您可以在 [Cloud KMS](https://docs.cloud.google.com/kms/docs?hl=zh-tw) 中使用客戶自行管理的加密金鑰 (CMEK)，搭配整合 CMEK 的服務 (包括 BigQuery)。使用 Cloud KMS 金鑰可讓您控管保護等級、位置、輪替時間表、使用權限和存取權，以及加密範圍。
使用 Cloud KMS 還可[追蹤金鑰用量](https://docs.cloud.google.com/kms/docs/view-key-usage?hl=zh-tw)、查看稽核記錄，以及控管金鑰生命週期。
您可以在 Cloud KMS 中控制及管理用來保護資料的對稱[金鑰加密金鑰 (KEK)](https://docs.cloud.google.com/kms/docs/envelope-encryption?hl=zh-tw#key_encryption_keys)，而不是由 Google 擁有及管理這些金鑰。

使用 CMEK 設定資源後，存取 BigQuery 資源的體驗與使用 Google 預設加密機制類似。如要進一步瞭解加密選項，請參閱「[客戶自行管理的 Cloud KMS 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)」一文。

## 使用 Cloud KMS Autokey 的 CMEK

您可以手動建立 CMEK 來保護 BigQuery 資源，也可以使用 Cloud KMS Autokey。Autokey 會根據需求產生金鑰環和金鑰，以支援在 BigQuery 中建立資源。如果服務代理尚未建立，系統會建立服務代理，並授予必要的 Identity and Access Management (IAM) 角色，供服務代理使用金鑰進行加密和解密作業。詳情請參閱「[Autokey 總覽](https://docs.cloud.google.com/kms/docs/autokey-overview?hl=zh-tw)」。

如要瞭解如何使用手動建立的 CMEK 保護 BigQuery 資源，請參閱[客戶管理的 Cloud KMS 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。

如要瞭解如何使用 Cloud KMS Autokey 建立的 CMEK 保護 BigQuery 資源，請參閱「[搭配 BigQuery 資源使用 Autokey](https://docs.cloud.google.com/kms/docs/create-resource-with-autokey?hl=zh-tw#bigquery-autokey)」。

## 加密資料表中的個別值

如果您想要加密 BigQuery 資料表中的個別值，請使用「用於相關資料的驗證加密」(AEAD) [加密函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw)。如果您希望將自己所有客戶的資料都保存在共用的資料表中，請使用 AEAD 函式，以不同的金鑰將每位客戶的資料加密。AEAD 加密函式是以 AES 為基礎。詳情請參閱「[GoogleSQL 中的 AEAD 加密概念](https://docs.cloud.google.com/bigquery/docs/aead-encryption-concepts?hl=zh-tw)」。

## 用戶端加密

用戶端加密與 BigQuery 靜態資料加密無關。如果您選擇使用用戶端加密技術，則必須負責管理用戶端金鑰和密碼編譯作業。您必須先將資料加密，再將資料寫入 BigQuery。在這種情況下，您的資料會被加密兩次，第一次是使用您的金鑰，第二次是使用 Google 金鑰。相同道理，從 BigQuery 讀取的資料會經過兩次解密，第一次是使用 Google 金鑰，第二次是使用您的金鑰。

**重要事項：**BigQuery 不會知道您的資料是否已在用戶端加密，也不會知道您的用戶端加密金鑰。如果您使用用戶端加密技術，則須妥善管理您的加密金鑰，以及用戶端加密、解密的各個環節。

## 傳輸中的資料

為了確保您的資料在網際網路上傳輸讀寫作業時能安全無虞， Google Cloud 會使用傳輸層安全標準 (TLS)。詳情請參閱  [Google Cloud](https://docs.cloud.google.com/security/encryption-in-transit?hl=zh-tw)中的傳輸加密一文。

在 Google 資料中心內，您的資料在機器之間傳輸時會經過加密。

## 後續步驟

如要進一步瞭解 BigQuery 和其他 Google Cloud 產品的靜態資料加密，請參閱「 [Google Cloud中的靜態資料加密](https://docs.cloud.google.com/security/encryption/default-encryption?hl=zh-tw)」一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]