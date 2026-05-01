* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用 BigQuery DataFrame 部署及套用遠端函式 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用 BigQuery DataFrames API 將 Python 函式部署為 Cloud Function，並做為遠端函式使用。

## 程式碼範例

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import bigframes.pandas as bpd

# Set BigQuery DataFrames options
bpd.options.bigquery.project = your_gcp_project_id
bpd.options.bigquery.location = "US"

# BigQuery DataFrames gives you the ability to turn your custom scalar
# functions into a BigQuery remote function. It requires the GCP project to
# be set up appropriately and the user having sufficient privileges to use
# them. One can find more details about the usage and the requirements via
# `help` command.
help(bpd.remote_function)

# Read a table and inspect the column of interest.
df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
df["body_mass_g"].head(10)

# Define a custom function, and specify the intent to turn it into a remote
# function. It requires a BigQuery connection. If the connection is not
# already created, BigQuery DataFrames will attempt to create one assuming
# the necessary APIs and IAM permissions are setup in the project. In our
# examples we will be letting the default connection `bigframes-default-connection`
# be used. We will also set `reuse=False` to make sure we don't
# step over someone else creating remote function in the same project from
# the exact same source code at the same time. Let's try a `pandas`-like use
# case in which we want to apply a user defined scalar function to every
# value in a `Series`, more specifically bucketize the `body_mass_g` value
# of the penguins, which is a real number, into a category, which is a
# string.
@bpd.remote_function(
    reuse=False,
    cloud_function_service_account="default",
)
def get_bucket(num: float) -> str:
    if not num:
        return "NA"
    boundary = 4000
    return "at_or_above_4000" if num >= boundary else "below_4000"

# Then we can apply the remote function on the `Series` of interest via
# `apply` API and store the result in a new column in the DataFrame.
df = df.assign(body_mass_bucket=df["body_mass_g"].apply(get_bucket))

# This will add a new column `body_mass_bucket` in the DataFrame. You can
# preview the original value and the bucketized value side by side.
df[["body_mass_g", "body_mass_bucket"]].head(10)

# The above operation was possible by doing all the computation on the
# cloud. For that, there is a google cloud function deployed by serializing
# the user code, and a BigQuery remote function created to call the cloud
# function via the latter's http endpoint on the data in the DataFrame.

# The BigQuery remote function created to support the BigQuery DataFrames
# remote function can be located via a property `bigframes_remote_function`
# set in the remote function object.
print(f"Created BQ remote function: {get_bucket.bigframes_remote_function}")

# The cloud function can be located via another property
# `bigframes_cloud_function` set in the remote function object.
print(f"Created cloud function: {get_bucket.bigframes_cloud_function}")

# Warning: The deployed cloud function may be visible to other users with
# sufficient privilege in the project, so the user should be careful about
# having any sensitive data in the code that will be deployed as a remote
# function.

# Let's continue trying other potential use cases of remote functions. Let's
# say we consider the `species`, `island` and `sex` of the penguins
# sensitive information and want to redact that by replacing with their hash
# code instead. Let's define another scalar custom function and decorate it
# as a remote function. The custom function in this example has external
# package dependency, which can be specified via `packages` parameter.
@bpd.remote_function(
    reuse=False,
    packages=["cryptography"],
    cloud_function_service_account="default",
)
def get_hash(input: str) -> str:
    from cryptography.fernet import Fernet

    # handle missing value
    if input is None:
        input = ""

    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(input.encode()).decode()

# We can use this remote function in another `pandas`-like API `map` that
# can be applied on a DataFrame
df_redacted = df[["species", "island", "sex"]].map(get_hash)
df_redacted.head(10)
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]