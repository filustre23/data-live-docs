* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 更新資料表快照中繼資料

本文說明如何使用 Google Cloud 控制台、[`bq update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令或 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API，更新資料表快照的說明、到期日或存取權政策。本文適用於熟悉 BigQuery 中[資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)和[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)的使用者。

## 權限與角色

本節說明更新資料表快照中繼資料所需的[身分與存取權管理 (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，以及授予這些權限的[預先定義 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。

### 權限

如要更新資料表快照的中繼資料，您需要下列權限：

| **權限** | **資源** |
| --- | --- |
| `bigquery.tables.update` | 資料表快照 |

### 角色

提供必要權限的預先定義 BigQuery 角色如下：

| **角色** | **資源** |
| --- | --- |
| 下列任一項：   `bigquery.dataEditor`  `bigquery.dataOwner`  `biguqery.admin` | 資料表快照 |

## 限制

您可以更新資料表快照的中繼資料，但無法更新資料，因為資料表快照資料為唯讀。如要更新資料表快照的資料，您必須先將資料表快照還原至標準資料表，然後更新標準資料表的資料。詳情請參閱「[還原資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-restore?hl=zh-tw)」。

## 更新資料表快照的中繼資料

變更資料表快照的說明、到期時間和存取政策，與變更標準資料表的中繼資料方式相同。以下各節提供幾個範例。

### 更新說明

如要變更資料表快照的說明，請使用下列任一選項：

### 主控台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「Explorer」explore：

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下含有資料表快照的資料集。
4. 依序點按「總覽」**>「資料表」**，然後點選要更新的資料表快照名稱。
5. 前往「詳細資料」分頁，然後點選「編輯詳細資料」。
6. 在「Description」(說明) 欄位中，新增或更新表格快照的說明。
7. 按一下 [儲存]。

### bq

在 Cloud Shell 中輸入下列指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq update \
--description="DESCRIPTION" \
PROJECT_ID:DATASET_NAME.SNAPSHOT_NAME
```

請替換下列項目：

* `DESCRIPTION`：描述快照的文字。
  例如：`Snapshot after table schema change X.`。
* `PROJECT_ID`：包含快照的專案 ID。
* `DATASET_NAME`：包含快照的資料集名稱。
* `SNAPSHOT_NAME`：快照的名稱。

### API

使用下列參數呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 包含快照的專案 ID。 |
| `datasetId` | 包含快照的資料集名稱。 |
| `tableId` | 快照名稱。 |
| 「要求主體」`description`欄位 | 描述快照的文字。例如 `Snapshot after table schema change X`。 |

建議使用 `tables.patch` 方法，而非 `tables.update` 方法，因為 `tables.update` 方法會取代整個 `Table` 資源。

### 更新到期時間

您可以透過下列任一選項，變更資料表快照的到期時間：

### 主控台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「Explorer」explore：
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下含有資料表快照的資料集。
4. 依序點按「總覽」**>「資料表」**，然後點選要更新的資料表快照名稱。
5. 前往「詳細資料」分頁，然後點選「編輯詳細資料」。
6. 在「Expiration time」(到期時間) 欄位中，輸入資料表快照的新到期時間。
7. 按一下 [儲存]。

### bq

在 Cloud Shell 中輸入下列指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq update \
--expiration=EXPIRATION_TIME \
PROJECT_ID:DATASET_NAME.SNAPSHOT_NAME
```

請替換下列項目：

* `EXPIRATION_TIME`：從目前時間到有效期限的時間 (以秒為單位)。
* `PROJECT_ID`：包含快照的專案 ID。
* `DATASET_NAME`：包含快照的資料集名稱。
* `SNAPSHOT_NAME`：快照的名稱。

### API

使用下列參數呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `projectId` | 包含快照的專案 ID。 |
| `datasetId` | 包含快照的資料集名稱。 |
| `tableId` | 快照名稱。 |
| 「要求主體」`expirationTime`欄位 | 快照到期時間，以自 Epoch 紀元時間起算的毫秒數表示。 |

建議使用 `tables.patch` 方法，而非 `tables.update` 方法，因為 `tables.update` 方法會取代整個 `Table` 資源。

### 更新存取權

您可以透過下列任一方式，授權使用者查看資料表快照中的資料：

### 主控台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「Explorer」explore：
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下含有資料表快照的資料集。
4. 依序點按「總覽」**>「資料表」**，然後按一下要共用的資料表快照名稱。
5. 在隨即顯示的快照窗格中，依序按一下「共用」和「新增主體」。
6. 在隨即顯示的「新增主體」窗格中，輸入要授予表格快照存取權的[主體](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw) ID。
7. 在「Select a role」(選取角色) 下拉式選單中，依序選擇「BigQuery」和「BigQuery Data Viewer」(BigQuery 資料檢視者)。
8. 按一下 [儲存]。

### bq

在 Cloud Shell 中輸入下列指令：

[前往 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

```
bq add-iam-policy-binding \
    --member="user:PRINCIPAL" \
    --role="roles/bigquery.dataViewer" \
    PROJECT_ID:DATASET_NAME.SNAPSHOT_NAME
```

請替換下列項目：

* `PRINCIPAL`：您要授予資料表快照存取權的[主體](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw)。
* `PROJECT_ID`：包含快照的專案 ID。
* `DATASET_NAME`：包含快照的資料集名稱。
* `SNAPSHOT_NAME`：快照的名稱。

### API

使用下列參數呼叫 [`tables.setIamPolicy`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/setIamPolicy?hl=zh-tw) 方法：

| **參數** | **值** |
| --- | --- |
| `Resource` | ``` projects/PROJECT_ID/datasets/DATASET_NAME/tables/SNAPSHOT_NAME ``` |
| 要求主體 | ``` {       "policy": {         "bindings": [           {             "members": [               "user:PRINCIPAL"             ],             "role": "roles/bigquery.dataViewer"           }         ]       }     } ``` |

請替換下列項目：

* `PROJECT_ID`：包含快照的專案 ID。
* `DATASET_NAME`：包含快照的資料集名稱。
* `SNAPSHOT_NAME`：快照的名稱。
* `PRINCIPAL`：您要授予資料表快照存取權的[主體](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw#concepts_related_identity)。

## 後續步驟

* [列出資料集中的資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-list?hl=zh-tw)。
* [查看資料表快照的中繼資料](https://docs.cloud.google.com/bigquery/docs/table-snapshots-metadata?hl=zh-tw)。
* [刪除資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-delete?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]