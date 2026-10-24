Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立及管理存放區

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或提出與這項預先發布版功能相關的問題，請傳送電子郵件至 [bigquery-repositories-feedback@google.com](mailto:bigquery-repositories-feedback@google.com)。

BigQuery 存放區可讓您控管程式碼檔案的版本，並與團隊協作。您可以建立、共用及刪除 BigQuery 存放區，或將其連結至第三方 Git 存放區。

如要以更簡便、以資料夾為基礎的方式進行版本管控，建議使用 [BigQuery Studio Git 存放區](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw)
[(預先發布版)](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。這項整合功能可讓您直接在 BigQuery Studio 檔案瀏覽器中使用 Git 分支版本，並一次複製多個存放區，不必管理個別工作區。

## 事前準備

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery and Dataform APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cdataform.googleapis.com&hl=zh-tw)

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery and Dataform APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cdataform.googleapis.com&hl=zh-tw)

### 必要的角色

如要取得使用存放區和工作區所需的權限，請要求管理員授予您存放區和工作區的下列 IAM 角色：

* 建立及管理共用存放區：[程式碼擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeOwner)  (`roles/dataform.codeOwner`)
* 在共用存放區中建立及刪除工作區：[程式碼編輯器](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeEditor)  (`roles/dataform.codeEditor`)
* 在共用存放區的工作區中建立、修改及版本管控檔案：[程式碼編輯器](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeEditor)  (`roles/dataform.codeEditor`)
* 查看工作區和共用存放區中的檔案：[程式碼檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeViewer)  (`roles/dataform.codeViewer`)
* 建立及管理私人存放區，包括私人存放區中工作區和檔案的所有動作：[程式碼建立者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeCreator)  (`roles/dataform.codeCreator`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

在存放區中具備程式碼編輯器角色的主體，可以編輯存放區中的所有工作區。

不過，在專案層級具備 BigQuery 管理員或 BigQuery Studio 管理員角色的主體，仍可查看您建立的私人存放區。這些主體可以與其他使用者共用您的私人存放區。

#### 存放區的安全性考量

BigQuery 中的程式碼資產是由 Dataform 提供，因此請考量下列安全性影響，再授予使用者這些資產的存取權：

* 程式碼資產的瀏覽權限由專案層級的 Dataform 權限控管。使用者只要具備 `dataform.repositories.list` 權限 (包含在標準 BigQuery 角色中，例如 [BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)、[BigQuery Studio 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser)和 [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user))，就能在 Google Cloud 專案的「Explorer」面板中查看所有程式碼資產，無論這些資產是否由他們建立或與他們共用。如要限制瀏覽權限，可以建立不含 `dataform.repositories.list` 權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。
* 凡是與 Dataform 服務代理共用的 Secret，可編輯這些資產的使用者都有可能存取。為確保憑證安全，請限制只有信任的使用者才能建立及編輯權限，並限制 Dataform 服務代理可存取的密鑰。詳情請參閱「[在套件安裝期間存取 Secret](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#secret-access-risk)」。

詳情請參閱「[Dataform 權限的安全性考量](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#security-considerations-permissions)」。

## 建立存放區

如要建立 BigQuery 存放區，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後點選「Repositories」(存放區)，在詳細資料窗格中開啟「Repositories」(存放區) 分頁。
4. 點選「Add Repository」。
5. 在「Create repository」(建立存放區) 窗格的「Repository ID」(存放區 ID) 欄位中，輸入專屬 ID。

   ID 只能使用數字、英文字母、連字號和底線。
6. 在「Region」(區域) 下拉式選單中，選取要儲存存放區及其內容的 BigQuery 區域。選取最靠近您所在位置的 BigQuery 區域。

   如要查看可用的 BigQuery 區域清單，請參閱「[BigQuery Studio 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqstudio-loc)」。存放區區域不一定要與 BigQuery 資料集的位置相同。
7. 點選「建立」。

## 連線至第三方存放區

本節說明如何將 BigQuery 存放區連結至遠端存放區。連結存放區後，您就可以對存放區所含工作區中的檔案執行 Git 動作。例如從遠端存放區提取更新，以及將變更推送至遠端存放區。

建議您為每個連結的遠端存放區建立專屬的 BigQuery 存放區。為 BigQuery 存放區指定與遠端存放區類似的名稱，以便清楚對應。

您可以透過 HTTPS 或 SSH 連線至遠端存放區。如果遠端存放區未開放給公開網際網路 (例如位於防火牆後方)，將 BigQuery 存放區連結至遠端存放區可能會失敗。下表列出支援的 Git 供應商，以及其存放區可用的連線方法：

| Git 供應商 | 連線方法 |
| --- | --- |
| Azure DevOps Services | SSH |
| Bitbucket | SSH |
| GitHub | SSH 或 HTTPS |
| GitLab | SSH 或 HTTPS |

**重要事項：** 如要建立 BigQuery 存放區，並連結至未列入 `dataform.restrictGitRemotes` 政策許可清單的遠端 Git 存放區，請先將遠端 Git 存放區新增至政策的 `allowedValues` 清單，然後建立新的 BigQuery 存放區，並連結至遠端存放區。詳情請參閱「[限制遠端存放區](https://docs.cloud.google.com/dataform/docs/restrict-git-remotes?hl=zh-tw)」。

### 透過 SSH 連線至遠端存放區

如要透過 SSH 連結遠端存放區，您必須產生安全殼層金鑰和 Secret Manager 密鑰。安全殼層金鑰包含公開和私密安全殼層金鑰。您必須將公開安全殼層金鑰提供給 Git 供應商，並使用私密安全殼層金鑰建立 Secret Manager 密鑰。接著，將密鑰提供給 Dataform 服務代理。

BigQuery 會使用含有私密安全殼層金鑰的密鑰登入 Git 供應商，代表使用者提交變更。BigQuery 會使用使用者的 Google Cloud 電子郵件地址進行這些修訂，方便您辨識每項修訂的執行者。

**警告：** 如果 BigQuery 使用者對自訂服務帳戶具備[扮演權限](https://docs.cloud.google.com/dataform/docs/strict-act-as-mode?hl=zh-tw)，就會共用私密安全殼層金鑰。建議您透過 Git 供應商建立機器使用者，並限制其存取權，僅能存取您打算與 BigQuery 搭配使用的遠端 Git 存放區。只有 Google Cloud 專案擁有者和具備[程式碼擁有者角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner) (`roles/dataform.codeOwner`) 的 BigQuery 使用者，才能使用安全殼層金鑰連結存放區。BigQuery 使用者無法查看安全殼層金鑰本身。

如要透過 SSH 將遠端存放區連結至 BigQuery 存放區，請按照下列步驟操作：

1. 在 Git 供應商中，執行下列操作：

   ### Azure DevOps Services

   1. 在 Azure DevOps Services 中[建立私密安全殼層金鑰](https://learn.microsoft.com/en-us/azure/devops/repos/git/use-ssh-keys-to-authenticate?view=azure-devops#step-1-create-your-ssh-keys)。
   2. [將公開安全殼層金鑰上傳](https://learn.microsoft.com/en-us/azure/devops/repos/git/use-ssh-keys-to-authenticate?view=azure-devops#step-2-add-the-public-key-to-azure-devops)至 Azure DevOps Services 存放區。

   ### Bitbucket

   1. 在 Bitbucket 中[建立私密安全殼層金鑰](https://support.atlassian.com/bitbucket-cloud/docs/configure-ssh-and-two-step-verification/)。
   2. 將[公開安全殼層金鑰上傳](https://support.atlassian.com/bitbucket-cloud/docs/configure-ssh-and-two-step-verification/)至 Bitbucket 存放區。

   ### GitHub

   1. 在 GitHub 中[檢查現有的安全殼層金鑰](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys)。
   2. 如果您沒有任何現有的安全殼層金鑰，或想使用新金鑰，請[建立安全殼層私密金鑰](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)。
   3. [將 GitHub 公開安全殼層金鑰上傳](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)至 GitHub 存放區。

   ### GitLab

   1. 在 GitLab 中[建立私人安全殼層金鑰](https://docs.gitlab.com/ee/user/ssh.html#generate-an-ssh-key-pair)。
   2. [將 GitLab 公開安全殼層金鑰上傳](https://docs.gitlab.com/ee/user/ssh.html#add-an-ssh-key-to-your-gitlab-account)至 GitLab 存放區。
2. 在 Secret Manager 中[建立密鑰](https://docs.cloud.google.com/secret-manager/docs/creating-and-accessing-secrets?hl=zh-tw#create)，並貼上私人安全殼層金鑰做為密鑰值。您的私人安全殼層金鑰應儲存在類似 `~/.ssh/id_ed25519` 的檔案中。為密鑰命名，方便日後尋找。
3. [將 Secret 存取權授予 Dataform 服務代理](https://docs.cloud.google.com/secret-manager/docs/manage-access-to-secrets?hl=zh-tw)。

   Dataform 服務代理 ID 的格式如下：

   ```
   service-PROJECT_NUMBER@gcp-sa-dataform.iam.gserviceaccount.com
   ```
4. 將 [`roles/secretmanager.secretAccessor` 角色](https://docs.cloud.google.com/secret-manager/docs/access-control?hl=zh-tw#secretmanager.secretAccessor)授予服務帳戶。
5. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
6. 點選左側窗格中的 explore「Explorer」。
7. 在「Explorer」窗格中展開專案，然後點選「Repositories」(存放區)，在詳細資料窗格中開啟「Repositories」(存放區) 分頁。
8. 選取要連結至遠端存放區的 BigQuery 存放區。
9. 在編輯器中，選取「設定」分頁標籤。
10. 按一下「與 Git 連線」。
11. 在「Connect to remote repository」(連線至遠端存放區) 窗格中，選取「SSH」圓形按鈕。
12. 在「Remote Git repository URL」(遠端 Git 存放區網址) 欄位中，輸入遠端 Git 存放區的網址，結尾為 `.git`。

    遠端 Git 存放區的網址必須採用下列其中一種格式：

    * 絕對網址：`ssh://git@{host_name}[:{port}]/{repository_path}`，`port` 為選用。
    * 類似 SCP 的網址：`git@{host_name}:{repository_path}`。
13. 在「Default remote branch name」(預設遠端分支版本名稱) 欄位中，輸入遠端 Git 存放區的主要分支版本名稱。
14. 在「Secret」下拉式選單中，選取您建立的 Secret，其中包含 SSH 私密金鑰。
15. 在「SSH public host key value」(SSH 公開主機金鑰值) 欄位中，輸入 Git 供應商的公開主機金鑰。

    ### Azure DevOps Services

    1. 如要擷取 Azure DevOps Services 公開主機金鑰，請在終端機執行下列指令：

       ```
       ssh-keyscan -t rsa ssh.dev.azure.com
       ```
    2. 複製其中一個輸出的金鑰，並省略行首的 `ssh.dev.azure.com`。複製的值必須採用以下格式：

       ```
       ALGORITHM BASE64_KEY_VALUE
       ```

       例如：

       ```
       ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7Hr1oTWqNqOlzGJOfGJ4NakVyIzf1rXYd4d7wo6jBlkLvCA4odBlL0mDUyZ0/QUfTTqeu+tm22gOsv+VrVTMk6vwRU75gY/y9ut5Mb3bR5BV58dKXyq9A9UeB5Cakehn5Zgm6x1mKoVyf+FFn26iYqXJRgzIZZcZ5V6hrE0Qg39kZm4az48o0AUbf6Sp4SLdvnuMa2sVNwHBboS7EJkm57XQPVU3/QpyNLHbWDdzwtrlS+ez30S3AdYhLKEOxAG8weOnyrtLJAUen9mTkol8oII1edf7mWWbWVf0nBmly21+nZcmCTISQBtdcyPaEno7fFQMDD26/s0lfKob4Kw8H
       ```

       請確認這組金鑰仍與 Azure DevOps Services 保持同步。

    ### Bitbucket

    1. 如要擷取 Bitbucket 公開主機金鑰，請在終端機執行下列指令：

       ```
       curl https://bitbucket.org/site/ssh
       ```
    2. 這個指令會傳回公開主機金鑰清單。從清單中選擇其中一個金鑰並複製，但省略行首的 `bitbucket.org`。複製的值必須採用以下格式：

       ```
       ALGORITHM BASE64_KEY_VALUE
       ```

       例如：

       ```
       ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIazEu89wgQZ4bqs3d63QSMzYVa0MuJ2e2gKTKqu+UUO
       ```

       請確認這組金鑰仍與 Bitbucket 同步。

    ### GitHub

    1. 如要擷取 GitHub 公開主機金鑰，請參閱 [GitHub 的安全殼層金鑰指紋](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints)。
    2. 頁面會列出公開主機金鑰。選擇其中一個並複製，省略行首的 `github.com`。複製的值必須採用以下格式：

       ```
       ALGORITHM BASE64_KEY_VALUE
       ```

       例如：

       ```
       ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
       ```

       請確認這組金鑰仍與 GitHub 保持同步。

    ### GitLab

    1. 如要擷取 GitLab 公開主機金鑰，請參閱 [SSH `known_hosts` 項目](https://docs.gitlab.com/ee/user/gitlab_com/#ssh-known_hosts-entries)。
    2. 頁面會列出公開主機金鑰。選擇其中一個並複製，省略行首的 `gitlab.com`。複製的值必須採用以下格式：

       ```
       ALGORITHM BASE64_KEY_VALUE
       ```

       例如：

       ```
       ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAfuCHKVTjquxvt6CM6tdG4SLp1Btn/nOeHHE5UOzRdf
       ```

       請確認這組金鑰仍與 GitLab 同步。
16. 點選「連線」。

### 透過 HTTPS 連結遠端存放區

如要透過 HTTPS 連結遠端存放區，您必須使用個人存取權杖建立 Secret Manager 密鑰，並與 Dataform 服務代理共用該密鑰。

BigQuery 接著會使用存取權杖登入 Git 供應商，代表使用者提交變更。BigQuery 會使用使用者的 Google Cloud 電子郵件地址進行這些修訂，因此您可以知道是誰進行了每次修訂。

**警告：** 私人 HTTPS 權杖會與所有對自訂服務帳戶具備[「以身分執行」權限](https://docs.cloud.google.com/dataform/docs/strict-act-as-mode?hl=zh-tw)的 BigQuery 使用者共用。建議您透過 Git 供應商建立機器使用者，並限制其存取權，僅能存取您打算與 BigQuery 搭配使用的遠端 Git 存放區。只有 Google Cloud 專案擁有者和具備[程式碼擁有者角色](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.codeOwner) (`roles/dataform.codeOwner`) 的 BigQuery 使用者，才能使用 HTTPS 權杖連結存放區。BigQuery 使用者無法查看 HTTPS 權杖本身。

如要透過 HTTPS 將遠端存放區連結至 BigQuery 存放區，請按照下列步驟操作：

1. 在 Git 供應商中，執行下列操作：

   ### GitHub

   1. 在 GitHub 中，建立[精細的個人存取權杖](https://github.blog/2022-10-18-introducing-fine-grained-personal-access-tokens-for-github/)或[傳統個人存取權杖](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#about-personal-access-tokens)。

      * 如要使用精細的 GitHub 個人存取權杖，請按照下列步驟操作：
      1. 選取存放區存取權，僅限所選存放區，然後選取要連結的存放區。
      2. 授予存放區內容的讀取和寫入權限。
      3. 請根據需求設定適當的權杖到期時間。
      * 如要使用傳統 GitHub 個人存取權杖，請按照下列步驟操作：
      1. 將 `repo` 權限授予 BigQuery。
      2. 請根據需求設定適當的權杖到期時間。
   2. 如果貴組織使用 SAML 單一登入 (SSO)，請[授權權杖](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on)。

   ### GitLab

   1. 在 GitLab 中建立 [GitLab 個人存取權杖](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)。
   2. 將權杖命名為 `dataform` (必要)。
   3. 將 `api`、`read_repository` 和 `write_repository` 權限授予 BigQuery。
   4. 請根據需求設定適當的權杖到期時間。
2. 在 Secret Manager 中，[建立包含遠端存放區個人存取權杖的 Secret](https://docs.cloud.google.com/secret-manager/docs/creating-and-accessing-secrets?hl=zh-tw#create)。
3. [將 Secret 存取權授予 Dataform 服務代理](https://docs.cloud.google.com/secret-manager/docs/manage-access-to-secrets?hl=zh-tw)。

   Dataform 服務代理 ID 的格式如下：

   ```
   service-PROJECT_NUMBER@gcp-sa-dataform.iam.gserviceaccount.com
   ```
4. 將 [`roles/secretmanager.secretAccessor` 角色](https://docs.cloud.google.com/secret-manager/docs/access-control?hl=zh-tw#secretmanager.secretAccessor)授予服務帳戶。
5. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
6. 點選左側窗格中的 explore「Explorer」。
7. 在「Explorer」窗格中展開專案，然後點選「Repositories」(存放區)，在詳細資料窗格中開啟「Repositories」(存放區) 分頁。
8. 選取要連結至遠端存放區的 BigQuery 存放區。
9. 在編輯器中，選取「設定」分頁標籤。
10. 按一下「與 Git 連線」。
11. 在「Connect to remote repository」(連線至遠端存放區) 窗格中，選取「HTTPS」圓形按鈕。
12. 在「Remote Git repository URL」(遠端 Git 存放區網址) 欄位中，輸入遠端 Git 存放區的網址，結尾為 `.git`。

    遠端 Git 存放區網址不得包含使用者名稱或密碼。
13. 在「Default remote branch name」(預設遠端分支版本名稱) 欄位中，輸入遠端 Git 存放區的主要分支版本名稱。
14. 在「Secret」下拉式選單中，選取您建立的 Secret，其中包含個人存取權杖。
15. 點選「連線」。

### 編輯遠端存放區連線

如要編輯 BigQuery 存放區與遠端 Git 存放區之間的連線，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Repositories」(存放區)，在詳細資料窗格中開啟「Repositories」(存放區) 分頁。
4. 選取要編輯連線的 BigQuery 存放區。
5. 在編輯器中，選取「設定」分頁標籤。
6. 在存放區頁面中，按一下「Edit Git connection」(編輯 Git 連線)。
7. 編輯連線設定。
8. 按一下「Update」。

## 共用存放區

如要共用存放區，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Repositories」(存放區)，在詳細資料窗格中開啟「Repositories」(存放區) 分頁。
4. 找出要共用的存放區。
5. 按一下 more\_vert「Open actions」(開啟動作)，然後點選「Share」(共用)。
6. 在「共用權限」窗格中，按一下「新增使用者/群組」。
7. 在「Add User/Group」(新增使用者/群組) 窗格的「New Principals」(新增主體) 欄位中，輸入一或多個使用者或群組名稱，並以半形逗號分隔。
8. 在「Role」(角色) 欄位中，選擇要指派給新主體的角色。
9. 按一下 [儲存]。

**注意：** 如果您在 Google Cloud 專案的 [`projects.locations.updateConfig` Dataform API 方法](https://docs.cloud.google.com/dataform/reference/rest/v1beta1/projects.locations/updateConfig?hl=zh-tw)中，將 `enable_private_workspace` 欄位[(預先發布版)](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)設為 `true`，藉此強化安全性，則對於 BigQuery 存放區使用的任何 Dataform 存放區，只有該 Dataform 存放區中 Dataform 工作區的建立者，才能在該 Dataform 工作區中讀取及寫入程式碼。

## 刪除存放區

如要刪除存放區及其中所有內容，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後點選「Repositories」(存放區)，在詳細資料窗格中開啟「Repositories」(存放區) 分頁。
4. 找出要刪除的存放區。
5. 按一下 more\_vert「Open actions」(開啟動作)，然後點選「Delete」(刪除)。
6. 點選「刪除」。

## 後續步驟

* 瞭解如何[使用 BigQuery Studio Git 存放區管理程式碼](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw)。
* 瞭解如何[建立工作區](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]