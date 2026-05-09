Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 MCP 將大型語言模型連結至 BigQuery

本指南說明如何使用 [MCP Toolbox for Databases](https://github.com/googleapis/mcp-toolbox)，將 BigQuery 專案連結至各種整合開發環境 (IDE) 和開發人員工具。這項工具使用 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction)，這是一項開放協定，可將大型語言模型 (LLM) 連線至 BigQuery 等資料來源，讓您直接透過現有工具執行 SQL 查詢，並與專案互動。

如果您使用 Gemini CLI，可以運用 BigQuery 擴充功能。如要瞭解如何操作，請參閱「[使用 Gemini CLI 開發](https://docs.cloud.google.com/bigquery/docs/develop-with-gemini-cli?hl=zh-tw)」。如果您打算為 Gemini CLI 建構自訂工具，請繼續閱讀。

本指南將示範下列 IDE 的連線程序：

* Cursor
* Windsurf (原名 Codeium)
* Visual Studio Code (Copilot)
* Cline (VS Code 擴充功能)
* Claude 電腦版
* Claude 代碼
* Antigravity

## 事前準備

1. 在 Google Cloud 控制台的[專案選擇器頁面](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)中，選取或建立 Google Cloud 專案。
2. [請確認您已為 Google Cloud 專案啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project)。
3. [在 Google Cloud 專案中啟用 BigQuery API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com%2F&hl=zh-tw)。
4. 設定完成這項工作所需的角色和權限。如要連結至專案，您需要 [BigQuery 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)角色 (`roles/bigquery.user`)、BigQuery 資料檢視者角色 (`roles/bigquery.dataViewer`) 或對等的身分與存取權管理 (IAM) 權限。
5. 為環境設定[應用程式預設憑證 (ADC)](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)。

## 與 Antigravity 連結

您可以透過下列方式將 BigQuery 連結至 Antigravity：

* 使用 MCP 商店
* 使用自訂設定

**注意：**您不需要下載 MCP Toolbox 二進位檔，即可使用這些方法。

### MCP 商店

在 Antigravity 中連線至 BigQuery 最簡單的方法，就是使用內建的 MCP 儲存庫。

1. 開啟 [Antigravity](https://antigravity.google/docs/mcp?hl=zh-tw)，然後開啟**編輯器的代理程式面板**。
2. 按一下面板頂端的「...」圖示，然後選取「MCP Servers」(MCP 伺服器)。
3. 在可用伺服器清單中找到「BigQuery」，然後按一下「安裝」。
4. 按照畫面上的提示，安全地連結帳戶 (如適用)。

在 MCP 商店中安裝 BigQuery 後，編輯器就會自動提供伺服器的資源和工具。

### 自訂設定

如要連線至自訂 MCP 伺服器，請按照下列步驟操作：

1. 開啟 [Antigravity](https://antigravity.google/docs/mcp?hl=zh-tw)，然後使用編輯器代理程式面板頂端的「...」下拉式選單，前往 MCP 商店。
2. 如要開啟 **mcp\_config.json** 檔案，請依序點選「MCP Servers」(MCP 伺服器) >「Manage MCP Servers」(管理 MCP 伺服器) >「View raw config」(查看原始設定)。
3. 新增下列設定，將環境變數換成您的值，然後儲存。

```
{
  "mcpServers": {
    "bigquery": {
      "command": "npx",
      "args": ["-y","@toolbox-sdk/server","--prebuilt","bigquery","--stdio"],
      "env": {
          "BIGQUERY_PROJECT": "PROJECT_ID"
      }
    }
  }
}
```

## 安裝 MCP Toolbox

如果您只打算使用 BigQuery Gemini CLI 擴充功能，就不需要安裝 MCP Toolbox，因為這些擴充功能會一併提供必要的伺服器功能。如要使用其他 IDE 和工具，請按照本節中的步驟安裝 MCP Toolbox。

這個工具箱是開放原始碼的 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 伺服器，位於 IDE 和 BigQuery 之間，可為 AI 工具提供安全有效率的控制層。

1. 以二進位檔形式下載最新版 MCP Toolbox。選取與作業系統 (OS) 和 CPU 架構對應的[二進位檔](https://github.com/googleapis/mcp-toolbox/releases)。您必須使用 MCP Toolbox V0.7.0 以上版本：

   ### linux/amd64

   ```
   curl -O https://storage.googleapis.com/mcp-toolbox-for-databases/VERSION/linux/amd64/toolbox
   ```

   將 `VERSION` 替換為 MCP Toolbox 版本，例如 `v0.7.0`。

   ### macOS darwin/arm64

   ```
   curl -O https://storage.googleapis.com/mcp-toolbox-for-databases/VERSION/darwin/arm64/toolbox
   ```

   將 `VERSION` 替換為 MCP Toolbox 版本，例如 `v0.7.0`。

   ### macOS darwin/amd64

   ```
   curl -O https://storage.googleapis.com/mcp-toolbox-for-databases/VERSION/darwin/amd64/toolbox
   ```

   將 `VERSION` 替換為 MCP Toolbox 版本，例如 `v0.7.0`。

   ### windows/amd64

   ```
   curl -O https://storage.googleapis.com/mcp-toolbox-for-databases/VERSION/windows/amd64/toolbox
   ```

   將 `VERSION` 替換為 MCP Toolbox 版本，例如 `v0.7.0`。
2. 將該二進位檔設為可執行：

   ```
   chmod +x toolbox
   ```
3. 驗證安裝項目：

   ```
   ./toolbox --version
   ```

## 設定用戶端和連線

本節說明如何將 BigQuery 連線至工具。

如果您使用獨立的 Gemini CLI，則不需要安裝或設定 MCP Toolbox，因為擴充功能會將必要的伺服器功能綁在一起。

如要使用其他與 MCP 相容的工具和 IDE，請先[安裝 MCP Toolbox](#install)。

### Claude 代碼

1. 安裝 [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)。
2. 在專案根目錄中建立 `.mcp.json` 檔案 (如果不存在)。
3. 新增設定、將環境變數替換為您的值，然後儲存：

   ```
           {
             "mcpServers": {
               "bigquery": {
                 "command": "./PATH/TO/toolbox",
                 "args": ["--prebuilt","bigquery","--stdio"],
                 "env": {
                   "BIGQUERY_PROJECT": "PROJECT_ID"
                 }
               }
             }
           }
   ```
4. 重新啟動 Claude Code，載入新設定。重新開啟時，工具會顯示已偵測到設定的 MCP 伺服器。

### Claude 電腦版

1. 開啟 [Claude Desktop](https://claude.ai/download)，然後前往「設定」。
2. 在「開發人員」分頁中，按一下「編輯設定」開啟設定檔。
3. 新增設定、將環境變數替換為您的值，然後儲存：

   ```
           {
             "mcpServers": {
               "bigquery": {
                 "command": "./PATH/TO/toolbox",
                 "args": ["--prebuilt","bigquery","--stdio"],
                 "env": {
                   "BIGQUERY_PROJECT": "PROJECT_ID"
                 }
               }
             }
           }
   ```
4. 重新啟動 Claude Desktop。
5. 新的即時通訊畫面會顯示槌子 (MCP) 圖示和新的 MCP 伺服器。

### Cline

1. 在 VS Code 中開啟 [Cline](https://github.com/cline/cline) 擴充功能，然後輕觸「MCP Servers」圖示。
2. 輕觸「設定 MCP 伺服器」開啟設定檔。
3. 新增下列設定，將環境變數替換為您的值，然後儲存：

   ```
           {
             "mcpServers": {
               "bigquery": {
                 "command": "./PATH/TO/toolbox",
                 "args": ["--prebuilt","bigquery","--stdio"],
                 "env": {
                   "BIGQUERY_PROJECT": "PROJECT_ID"
                 }
               }
             }
           }
   ```

伺服器連線成功後，會顯示綠色的「有效」狀態。

### Cursor

1. 在專案根目錄中建立 `.cursor` 目錄 (如果不存在)。
2. 如果 `.cursor/mcp.json` 檔案不存在，請建立並開啟該檔案。
3. 新增下列設定，將環境變數替換為您的值，然後儲存：

   ```
           {
             "mcpServers": {
               "bigquery": {
                 "command": "./PATH/TO/toolbox",
                 "args": ["--prebuilt","bigquery","--stdio"],
                 "env": {
                   "BIGQUERY_PROJECT": "PROJECT_ID"
                 }
               }
             }
           }
   ```
4. 開啟「游標」，然後依序前往「設定」>「游標設定」>「MCP」。伺服器連線後，會顯示綠色的「有效」狀態。

### Visual Studio Code (Copilot)

1. 開啟 [VS Code](https://code.visualstudio.com/docs/copilot/overview)，並在專案根目錄中建立 `.vscode` 目錄 (如果不存在)。
2. 如果 `.vscode/mcp.json` 檔案不存在，請建立並開啟該檔案。
3. 新增下列設定，將環境變數替換為您的值，然後儲存：

   ```
           {
             "servers": {
               "bigquery": {
                 "command": "./PATH/TO/toolbox",
                 "args": ["--prebuilt","bigquery","--stdio"],
                 "env": {
                   "BIGQUERY_PROJECT": "PROJECT_ID"
                 }
               }
             }
           }
   ```
4. 重新載入 VS Code 視窗。與 MCP 相容的擴充功能會自動偵測設定並啟動伺服器。

### 滑浪風帆

1. 開啟 [Windsurf](https://docs.codeium.com/windsurf)，然後前往 Cascade 助理。
2. 按一下 MCP 圖示，然後點選「設定」開啟設定檔。
3. 新增下列設定，將環境變數替換為您的值，然後儲存：

   ```
           {
             "mcpServers": {
               "bigquery": {
                 "command": "./PATH/TO/toolbox",
                 "args": ["--prebuilt","bigquery","--stdio"],
                 "env": {
                   "BIGQUERY_PROJECT": "PROJECT_ID"
                 }
               }
             }
           }
   ```

> **注意：**`BIGQUERY_PROJECT` 環境變數會指定 MCP Toolbox 要使用的預設 Google Cloud 專案 ID。所有 BigQuery 作業 (例如執行查詢) 都是在這個專案中執行。

## 使用工具

您的 AI 工具現已透過 MCP 連線至 BigQuery。你可以要求 AI 助理列出資料表、建立資料表，或是定義及執行其他 SQL 陳述式。

LLM 可使用下列工具：

* **analyze\_contribution**：執行貢獻分析，也稱為主要驅動因素分析。
* **ask\_data\_insights**：執行資料分析、取得洞察資訊，或回答有關 BigQuery 資料表內容的複雜問題。
* **execute\_sql**：執行 SQL 陳述式。
* **預測**：預測時間序列資料。
* **get\_dataset\_info**：取得資料集中繼資料。
* **get\_table\_info**：取得表格中繼資料。
* **list\_dataset\_ids**：列出資料集。
* **list\_table\_ids**：列出資料表。
* **search\_catalog**：使用自然語言搜尋資料表。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]