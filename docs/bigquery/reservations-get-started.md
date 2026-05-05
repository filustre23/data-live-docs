* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 開始使用預留項目功能

瞭解如何在 BigQuery 中建立及指派預留項目。

您可以透過 BigQuery 預留項目購買專用處理容量 (以運算單元為單位)，而不必根據處理的每個位元組資料支付*以量計價*費用。預訂可讓您更準確地預測費用，工作負載效能通常也更穩定。預訂項目會與版本建立關聯，提供不同規模的定價，並符合不同機構的需求。

使用預留項目時，您可以建立指派作業，將特定專案、資料夾或整個機構連結至特定預留項目。Google Cloud 這樣一來，您就能隔離工作負載、確保重要工作有足夠的資源，並更有效管理 BigQuery 支出。

在本教學課程中，您將建立具有 100 個自動調度資源運算單元的標準版預留項目，並將專案指派給該預留項目。然後選擇刪除預留項目，以免產生費用。

**注意：** 本教學課程會產生費用。購買運算單元之前，請先瞭解[預訂定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。為避免在本教學課程完成後產生費用，請務必按照「[清除](#clean-up)」一節的說明刪除預留項目。


---

如要直接在 Google Cloud 控制台中，按照這項工作的逐步指南操作，請按一下「Guide me」(逐步引導)：

[「Guide me」(逐步引導)](https://console.cloud.google.com/freetrial?redirectPath=%2F%3Fwalkthrough_id%3Dbigquery__reservations-get-started&hl=zh-tw)

---

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)

   您可以建立個別 Google Cloud 專案來管理預訂，並為專案提供描述性名稱，例如 `bq-COMPANY_NAME-admin`。
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery Reservation API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigqueryreservation.googleapis.com&hl=zh-tw)

   詳情請參閱「[啟用 BigQuery Reservation API](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#enabling-reservations-api)」。
4. 在 Google Cloud 控制台中查看運算單元配額：

   [查看運算單元配額](https://console.cloud.google.com/iam-admin/quotas?service=bigqueryreservation.googleapis.com&%3Bmetric=bigqueryreservation.googleapis.com%2Ftotal_slots&hl=zh-tw)

   購買運算單元之前，要購買運算單元的區域中必須具備充足的運算單元配額。

   如果區域中的運算單元配額少於您要購買的運算單元數量，請參閱「[申請提高配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requesting_a_quota_increase)」一文。

### 必要的角色

如要取得建立預留項目、將專案指派給預留項目，以及刪除預留項目所需的權限，請要求管理員授予專案的 [BigQuery 資源編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceEditor)  (`roles/bigquery.resourceEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立自動調度資源預留項目

在 `US` 多區域中建立名為 `test` 的預留項目，並為其分配最多 100 個自動調度資源運算單元。自動調度資源程序會根據工作負載需求，擴充或縮減自動調度資源的配額。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「建立預留項目」。
4. 在「Reservation name」(預留項目名稱) 欄位輸入 `test`。
5. 從「Location」(位置) 下拉式選單中選取「us (multiple regions in United States)」(us (多個美國區域))。
6. 從「Edition」(版本) 清單中選取「Standard」(標準)。詳情請參閱[瞭解 BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的相關說明。
7. 在「Max reservation size selector」(預留項目大小選取器)，選取「Small (100 Slots)」(小 (100 個運算單元))。
8. 其他設定均保留預設值，然後點選「儲存」。

如要瞭解如何使用 SQL 或 bq 工具建立預留項目，請參閱「[使用專屬時段建立預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_a_reservation_with_dedicated_slots)」。

## 將專案指派給預留項目

將專案指派給 `test` 預留項目。從這個專案執行的任何查詢工作，都會使用 `test` 預留項目的運算單元集區。(在本教學課程中，您不會執行工作)。

您可以指派與建立預訂的管理專案位於相同機構和區域的任何專案。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「運算單元預留項目」分頁標籤。
4. 在「Actions」(動作) 欄找到預留項目 **`test`**，然後點選「Actions」(動作)。more\_vert
5. 按一下「建立作業」。
6. 在「Select an organization, folder or project」(選取組織、資料夾或專案) 部分，點選「Browse」(瀏覽)。
7. 瀏覽或搜尋專案，並選取所需項目。
8. 點選「建立」。

建立預訂指派項目後，請等待至少 5 分鐘再執行查詢。否則系統可能會按照以量計價的定價模式計費。

如要瞭解如何使用 SQL 或 bq 工具將專案指派給保留項目，請參閱「[將專案或資料夾指派給保留項目](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign_my_prod_project_to_prod_reservation)」。

## 清除所用資源

為了避免系統向您的 Google Cloud 帳戶收取本頁面所用資源的費用，請按照下列步驟操作。

### 刪除專案

如要避免付費，最簡單的方法就是刪除您為了本教學課程所建立的專案。

刪除專案的方法如下：

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### 刪除保留項目

刪除預留項目後，目前使用該預留項目運算單元執行的任何工作都會失敗。為避免發生錯誤，請先讓進行中的工作完成，再刪除預訂。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「運算單元預留項目」分頁標籤。
4. 找到預留項目 **`test`**，然後點選**切換節點**。
5. 針對該預留項目中的各項指派作業，依序點選「Actions」(動作) 和「Delete」(刪除)。
6. 在「Actions」(動作) 欄找到預留項目 **`test`**，然後點選 more\_vert「Actions」(動作)。
7. 點選「刪除」。

如要瞭解如何使用 SQL 或 bq 工具刪除預留項目，請參閱「[刪除預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#delete_a_reservation)」。

## 後續步驟

* 如要瞭解如何使用 BigQuery 預留項目管理工作負載，請參閱「[瞭解預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)」。
* 如要進一步瞭解運算單元，請參閱「[瞭解運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)」一文。
* 如要瞭解如何使用 BigQuery 指派項目來整理工作負載，請參閱「[管理工作負載指派項目](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)」。
* 如要瞭解如何購買承諾使用合約，請參閱「[運算單元承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]