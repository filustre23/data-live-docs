* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理各個位置的政策標記

本文說明如何在 BigQuery 中，跨區域位置管理政策標記，以進行資料欄層級安全防護和動態資料遮蓋。

BigQuery 透過政策標記，為敏感資料表欄提供[精細的存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)功能，並支援依據類型分類資料。

建立資料分類分類法並將政策標記套用至資料後，您可以在各個位置進一步管理政策標記。

## 位置注意事項

分類是區域資源，例如 BigQuery 資料集和資料表。建立分類時，請指定分類的地區或*位置*。

您可以在[所有提供 BigQuery 的區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)中，建立分類並將政策標記套用至資料表。不過，如要將分類中的政策標記套用至資料表欄，分類和資料表必須位於同一個區域位置。

雖然您無法將政策標記套用至位於不同位置的資料表欄，但可以明確複製分類架構，將其複製到其他位置。

## 在不同地點使用分類

您可以明確複製 (或複製) 分類和政策標記定義到其他位置，不必在每個位置手動建立新的分類。複製分類時，您可以在多個位置使用相同的資料欄層級安全性政策標記，簡化管理作業。

複製後，分類和政策標記在每個位置都會保留相同的 ID。

**注意：** 跨地點同步分類時，只會同步分類和分類中的政策標記。系統不會同步處理授予政策標記的權限，以及受該政策標記控管的資料欄，且這些權限和資料欄可能會因位置而異。

您可以再次同步分類和政策標記，確保多個位置的分類和政策標記一致。如要明確複製分類法，請呼叫 [Data Catalog](https://docs.cloud.google.com/data-catalog/docs?hl=zh-tw) API。日後同步處理複製的分類時，會使用相同的 API 指令，覆寫先前的分類。

為方便同步分類，您可以使用 [Cloud Scheduler](https://docs.cloud.google.com/scheduler/docs?hl=zh-tw)，定期在各區域同步分類，您可以設定排程，也可以手動按下按鈕。如要使用 Cloud Scheduler，請設定服務帳戶。

## 在新位置複製分類

### 所需權限

複製分類架構的使用者憑證或服務帳戶必須具備「Data Catalog 政策代碼管理員」角色。

如要進一步瞭解如何授予「政策標記管理員」角色，請參閱「[透過 BigQuery 資料欄層級的安全防護機制限制存取權](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)」。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

如要跨營業地點複製分類，請按照下列步驟操作：

### API

呼叫 Data Catalog API 的 [`projects.locations.taxonomies.import`](https://docs.cloud.google.com/data-catalog/docs/reference/rest/v1/projects.locations.taxonomies/import?hl=zh-tw) 方法，並在 HTTP 字串中提供 `POST` 要求和目的地專案與位置的名稱。

`POST https://datacatalog.googleapis.com/{parent}/taxonomies:import`

`parent` 路徑參數是您要將分類複製到的目標專案和位置。示例：
`projects/MyProject/locations/eu`

**重點：** 如要在日後同步處理各個地點的複製分類，請重複上述步驟。

## 同步處理複製的分類

如要同步處理已在各個位置複製的分類，請按照「[在新的位置複製分類](#replicating_a_taxonomy_in_a_new_location)」一節所述，重複進行 Data Catalog API 呼叫。

或者，您也可以使用服務帳戶和 Cloud Scheduler，按照指定時間表同步分類。在 Cloud Scheduler 中設定服務帳戶後，您也可以透過 Google Cloud 控制台的 Cloud Scheduler 頁面或 Google Cloud CLI，觸發隨選 (未排程) 同步作業。

**注意：**分類架構複製到其他位置後，在其中一個位置所做的變更不會自動反映到其他位置。使用者或服務帳戶必須具備適當權限，才能再次明確同步分類。

## 使用 Cloud Scheduler 同步處理複製的分類

如要使用 Cloud Scheduler 在各個地點之間同步複製的分類，您需要服務帳戶。

### 服務帳戶

您可以將複製同步的權限授予現有的服務帳戶，也可以建立新的服務帳戶。

如要建立新的服務帳戶，請參閱「[建立服務帳戶](https://docs.cloud.google.com/iam/docs/service-accounts-create?hl=zh-tw)」。

### 所需權限

1. 用來同步分類的服務帳戶必須具備「Data Catalog Policy Tag Admin」角色。詳情請參閱「[Data Catalog 政策標記管理員角色](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#policy_tags_admin)」。
2. [啟用 Cloud Scheduler API](https://console.cloud.google.com/apis/library/cloudscheduler.googleapis.com?hl=zh-tw)

### 使用 Cloud Scheduler 設定分類架構同步

如要使用 Cloud Scheduler 在各個位置同步複製的分類，請按照下列步驟操作：

### 控制台

首先，請建立同步工作及其排程。

1. 按照操作說明[在 Cloud Scheduler 中建立工作](https://docs.cloud.google.com/scheduler/docs/schedule-run-cron-job?hl=zh-tw#create_a_job)。
2. 如需「目標」，請參閱「[透過驗證建立排程器工作](https://docs.cloud.google.com/scheduler/docs/http-target-auth?hl=zh-tw#creating_a_scheduler_job_with_authentication)」一文中的操作說明。

接著，新增排定同步處理作業所需的驗證。

1. 按一下「顯示更多」即可顯示驗證欄位。
2. 在「Auth header」(驗證標頭) 部分，選取「Add OAuth token」(新增 OAuth 權杖)。
3. 新增服務帳戶資訊。
4. 在「範圍」中，輸入「https://www.googleapis.com/auth/cloud-platform」。
5. 按一下「建立」即可儲存排程同步。

現在請測試工作設定是否正確。

1. 建立工作後，請按一下「立即執行」，測試工作設定是否正確。隨後，Cloud Scheduler 會根據您指定的時間表觸發 HTTP 要求。

**重點：** 如要在日後隨選 (非排程) 同步複製的分類架構，請在 Google Cloud 控制台的「Cloud Scheduler」頁面中，按一下「立即執行」。

### gcloud

語法：

```
  gcloud scheduler jobs create http "JOB_ID" --schedule="FREQUENCY" --uri="URI" --oath-service-account-email="CLIENT_SERVICE_ACCOUNT_EMAIL" --time-zone="TIME_ZONE" --message-body-from-file="MESSAGE_BODY"
```

更改下列內容：

1. `${JOB_ID}` 是工作的名稱。在專案中不得重複。
   請注意，即使您刪除了關聯的工作，仍然不得在專案中再次使用此名稱。
2. `${FREQUENCY}` 是時間表，也稱為*工作間隔*，亦即執行工作的頻率。例如「每 3 小時」。
   您在這裡提供的字串可以是任何與 crontab 相容的字串。
   熟悉舊版 App Engine Cron 的開發人員也可以使用 [App Engine Cron](https://docs.cloud.google.com/appengine/docs/standard/python/config/cronref?hl=zh-tw) 語法。
3. `${URI}` 是端點的完整網址。
4. `--oauth-service-account-email` 定義權杖類型。請注意，`*.googleapis.com` 上託管的 Google API 預期會使用 OAuth 權杖。
5. `${CLIENT_SERVICE_ACCOUNT_EMAIL}` 是用戶端服務帳戶的電子郵件地址。
6. `${MESSAGE_BODY}` 是包含 POST 要求主體的檔案路徑。

您也可以使用 [Google Cloud CLI 參考資料](https://docs.cloud.google.com/sdk/gcloud/reference/scheduler/jobs/create/http?hl=zh-tw)中所述的其他選項參數。

範例：

```
  gcloud scheduler jobs create http cross_regional_copy_to_eu_scheduler --schedule="0 0 1 * *" --uri="https://datacatalog.googleapis.com/v1/projects/my-project/locations/eu/taxonomies:import" --oauth-service-account-email="policytag-manager-service-acou@my-project.iam.gserviceaccount.com" --time-zone="America/Los_Angeles" --message-body-from-file=request_body.json
```

## 後續步驟

* 如需政策標記資料欄層級安全防護機制總覽，請參閱「[BigQuery 資料欄層級安全防護機制簡介](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)」。
* 如要進一步瞭解如何建立及套用政策標記，請參閱「[使用 BigQuery 資料欄層級安全防護機制限制存取權](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)」。
* 如要瞭解使用 BigQuery 資料欄層級安全防護機制對寫入作業的影響，請參閱「[使用 BigQuery 資料欄層級安全防護機制對寫入作業的影響](https://docs.cloud.google.com/bigquery/docs/column-level-security-writes?hl=zh-tw)」。
* 如要瞭解使用政策標記的最佳做法，請參閱「[在 BigQuery 中使用政策標記](https://docs.cloud.google.com/bigquery/docs/best-practices-policy-tags?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]