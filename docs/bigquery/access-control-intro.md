* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 安全性和存取權控管簡介

本文將概述如何使用 Identity and Access Management (IAM) 控管 BigQuery 的存取權。IAM 可讓您對特定 BigQuery 資源授予精細的存取權，協助預防其他資源遭到存取；IAM 可協助您套用最低權限安全原則，確保[IAM 主體](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw)只擁有實際需要的權限。

當使用者、群組或服務帳戶等 IAM 主體呼叫 Google Cloud API 時，該主體必須具備使用資源所需的最低 IAM 權限。如要授予主體必要權限，請將 IAM 角色授予主體。

本文說明如何使用預先定義和自訂 IAM 角色，允許主體存取 BigQuery 資源。

如要瞭解如何管理 Google Cloud中的存取權，請參閱 [IAM 總覽](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw)。

## IAM 角色類型

角色是一組權限，可授予 IAM 主體。您可以在 IAM 中使用下列類型的角色，授予 BigQuery 資源的存取權：

* [**預先定義角色**](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)由 Google Cloud 管理，可因應常見的用途和存取權控管模式。
* [**自訂角色**](https://docs.cloud.google.com/iam/docs/understanding-custom-roles?hl=zh-tw)：根據使用者指定的權限清單提供存取權。如要瞭解如何建立自訂角色，請參閱 IAM 說明文件中的「[建立及管理自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)」。

**注意：** BigQuery 新增功能時，預先定義的 IAM 角色可能會新增權限。此外，您隨時可以將新的預先定義 IAM 角色新增至 BigQuery。如果貴機構要求角色定義不得變更，請建立[自訂 IAM 角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。

如要判斷某個或某幾個權限是否包含在預先定義的 IAM 角色中，請利用下列其中一種方式：

* [BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)參考資料
* [IAM 角色和權限索引](https://docs.cloud.google.com/iam/docs/roles-permissions?hl=zh-tw)
* [`gcloud iam roles describe`](https://docs.cloud.google.com/sdk/gcloud/reference/iam/roles/describe?hl=zh-tw) 指令
* IAM API 中的 [`roles.get()`](https://docs.cloud.google.com/iam/reference/rest/v1/roles/get?hl=zh-tw) 方法

## BigQuery 中的 IAM 角色

權限不會直接指派給使用者、群組或服務帳戶。而是授予使用者、群組或服務帳戶一或多個預先定義或自訂角色，讓他們有權對資源執行動作。您可以在特定資源上授予這些角色，但這些角色也會套用至[資源階層](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw)中該資源的所有子系。

當您將多個角色類型指派給使用者時，授予的權限就是各角色權限的聯集。

您可以授予下列 BigQuery 資源的存取權：

* 資料集和資料集中的下列資源：
  + 資料表和檢視表
  + 處理常式
* 連線
* 已儲存的查詢
* 資料面板
* 資料準備
* pipeline
* 存放區

### 授予 Resource Manager 資源的存取權

您可以透過 Resource Manager 授予主體 BigQuery 角色，然後在機構、資料夾或專案中授予該角色，藉此設定 BigQuery 資源的存取權。

如果您將角色授予機構和專案等 Resource Manager 資源，您將授予機構或專案中「所有」 BigQuery 資源的權限。

如要進一步瞭解如何使用 IAM 管理 Resource Manager 資源的存取權，請參閱 IAM 說明文件中的[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

### 授予資料集存取權

您可以在資料集層級指派角色，以便提供特定資料集的存取權，而不必提供專案其他資源的完整存取權。在 [IAM 資源階層](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw#policy_hierarchy)中，BigQuery 資料集是專案的子資源。如要進一步瞭解如何在資料集層級指派角色，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

**注意：** 請勿將 BigQuery 基本角色授予資料集。BigQuery 的資料集層級基本角色在 IAM 推出前就已經存在。BigQuery 基本角色提供的存取權過多且不平均，因此不建議使用。舉例來說，`Owner`基本角色「不」提供資料表存取權限。詳情請參閱「[基本角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control-basic-roles?hl=zh-tw)」。

### 授予資料集內個別資源的存取權

您可以授予角色資料集內特定類型資源的存取權，不必提供資料集資源的完整存取權。

角色可套用至資料集中的下列資源：

* 資料表和檢視表
* 處理常式

**注意：** 角色無法套用至模型。

如要進一步瞭解如何在資料表、檢視區塊或常式層級指派角色，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

## 後續步驟

* 如要進一步瞭解如何將角色指派給 BigQuery 資源，請參閱「[使用 IAM 控制資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。
* 如要查看 BigQuery 預先定義的 IAM 角色和權限清單，請參閱「[BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]