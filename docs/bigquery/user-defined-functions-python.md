* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# Python 中用户定义的函数

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**如需在预览版期间获得支持，请发送邮件至 [bq-python-udf-feedback@google.com](mailto:bq-python-udf-feedback@google.com)。

Python 用户定义的函数 (UDF) 使您可以在 Python 中实现标量函数，并在 SQL 查询中进行使用。Python UDF 与 [SQL 和 JavaScript UDF](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/user-defined-functions?hl=zh-cn) 类似，但具有更多功能。借助 Python UDF，您可以通过 [Python 软件包索引 (PyPI)](https://pypi.org/) 安装第三方库，还可以使用 [Cloud 资源连接](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-cn)访问外部服务。

Python UDF 在 BigQuery 托管资源上构建和运行。

## 限制

* `python-3.11` 是唯一受支持的运行时。
* 您无法创建临时 Python UDF。
* 您无法将 Python UDF 与物化视图搭配使用。
* 调用 Python UDF 的查询的结果不会进行缓存，因为 Python UDF 的返回值始终假定为具有非确定性。
* [`INFORMATION_SCHEMA`](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn) 视图中未完全支持 Python UDF。
* 您无法使用 [Routine API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/routines?hl=zh-cn) 创建或更新 Python UDF。
* 不支持 [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/overview?hl=zh-cn)。
* 不支持[客户管理的加密密钥 (CMEK)](https://docs.cloud.google.com/kms/docs/cmek?hl=zh-cn)。
* 不支持以下数据类型：`JSON`、`RANGE`、`INTERVAL` 和 `GEOGRAPHY`。
* 运行 Python UDF 的容器最多只能配置 [2 个 vCPU 和 8 Gi](#configure-container-limits)。

## 所需 IAM 角色

所需的 IAM 角色取决于您是 Python UDF 所有者还是 Python UDF 用户。Python UDF 所有者通常会创建或更新 UDF。Python UDF 用户会调用他人创建的 UDF。

如果您创建或运行引用 Cloud 资源连接的 Python UDF，还需要其他角色。

### UDF 所有者

如果您要创建或更新 Python UDF，则应被授予针对相应资源的以下预定义 IAM 角色：

| 角色 | 所需权限 | 资源 |
| --- | --- | --- |
| [BigQuery Data Editor](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn#bigquery.dataEditor) (`roles/bigquery.dataEditor`) | * `bigquery.routines.create`，用于使用 `CREATE FUNCTION` 语句创建 Python UDF。 * `bigquery.routines.update`，用于使用 `CREATE FUNCTION` 语句更新 Python UDF。 | 在其中创建或更新 Python UDF 的数据集。 |
| [BigQuery Job User](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn#bigquery.jobUser) (`roles/bigquery.jobUser`) | * `bigquery.jobs.create`，用于运行 `CREATE FUNCTION` 语句查询作业。 | 在其中运行 `CREATE FUNCTION` 语句的项目。 |
| [BigQuery Connection Admin](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn#bigquery.connectionAdmin) (`roles/bigquery.connectionAdmin`) | * `bigquery.connections.create`，仅在[创建新的 Cloud 资源连接](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-cn#create-cloud-resource-connection)时才需要。 * `bigquery.connections.delegate`，用于在 `CREATE FUNCTION` 语句中使用连接。 | 您向其授予对外部资源的访问权限的连接。仅当您的 UDF 使用 [`WITH CONNECTION`](#use-online-service) 子句访问外部服务时，才需要此连接。 |

### UDF 用户

如果您要调用 Python UDF，则应被授予针对相应资源的以下预定义 IAM 角色：

| 角色 | 所需权限 | 资源 |
| --- | --- | --- |
| [BigQuery User](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn#bigquery.user) (`roles/bigquery.user`) | `bigquery.jobs.create`，用于运行引用 UDF 的查询作业。 | 在其中运行调用 Python UDF 的查询作业的项目。 |
| [BigQuery Data Viewer](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn#bigquery.dataViewer) (`roles/bigquery.dataViewer`) | `bigquery.routines.get`，用于运行他人创建的 UDF。 | 在其中存储 Python UDF 的数据集。 |
| [BigQuery Connection User](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn#bigquery.connectionUser) (`roles/bigquery.connectionUser`) | `bigquery.connections.use`，用于运行引用 Cloud 资源连接的 Python UDF。 | Python UDF 引用的 Cloud 资源连接。仅当您的 UDF 引用连接时，才需要此连接。 |

如需详细了解 BigQuery 中的角色，请参阅[预定义的 IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn#bigquery)。

## 创建永久性 Python UDF

创建 Python UDF 时，请遵循以下规则：

* Python UDF 的主体必须是带英文引号的字符串字面量，用于表示 Python 代码。如需详细了解带英文引号的字符串字面量，请参阅[带英文引号的字面量的格式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-cn#quoted_literals)。
* Python UDF 的主体必须包含一个 Python 函数，该函数在 Python UDF 选项列表的 `entry_point` 参数中使用。
* 需要在 `runtime_version` 选项中指定 Python 运行时版本。唯一受支持的 Python 运行时版本是 `python-3.11`。如需查看可用选项的完整列表，请参阅 `CREATE FUNCTION` 语句的[函数选项列表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#function_option_list)。

如需创建永久性 Python UDF，请使用 [`CREATE FUNCTION` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_function_statement)，并且不带 `TEMP` 或 `TEMPORARY` 关键字。如需删除永久性 Python UDF，请使用 [`DROP FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#drop_function_statement) 语句。

当您使用 `CREATE FUNCTION` 语句创建 Python UDF 时，BigQuery 会创建或更新基于基础映像的容器映像。容器使用您的代码和任何指定的软件包依赖项，基于基础映像构建而成。创建容器是一个长时间运行的过程。运行 `CREATE FUNCTION` 语句后的第一个查询可能会自动等待映像完成。在没有任何外部依赖项的情况下，容器映像通常应在不到一分钟的时间内创建完成。

### 示例

如需查看创建永久性 Python UDF 的示例，请选择以下选项之一：

### 控制台

以下示例创建一个名为 `multiplyInputs` 的永久性 Python UDF，并从 `SELECT` 语句中调用该 UDF：

1. 转到 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下 `CREATE FUNCTION` 语句：

   ```
   CREATE FUNCTION `PROJECT_ID.DATASET_ID`.multiplyInputs(x FLOAT64, y FLOAT64)
   RETURNS FLOAT64
   LANGUAGE python
   OPTIONS(runtime_version="python-3.11", entry_point="multiply")
   AS r'''

   def multiply(x, y):
     return x * y

   ''';

   -- Call the Python UDF.
   WITH numbers AS
     (SELECT 1 AS x, 5 as y
     UNION ALL
     SELECT 2 AS x, 10 as y
     UNION ALL
     SELECT 3 as x, 15 as y)
   SELECT x, y,
   `PROJECT_ID.DATASET_ID`.multiplyInputs(x, y) AS product
   FROM numbers;
   ```

   替换 PROJECT\_ID。DATASET\_ID 替换为您的项目 ID 和数据集 ID。
3. 点击 play\_circle\_filled **运行**。

   此示例生成以下输出：

   ```
   +-----+-----+--------------+
   | x   | y   | product      |
   +-----+-----+--------------+
   | 1   | 5   |  5.0         |
   | 2   | 10  | 20.0         |
   | 3   | 15  | 45.0         |
   +-----+-----+--------------+
   ```

### BigQuery DataFrame

以下示例使用 BigQuery DataFrames 将自定义函数转换为 Python UDF：

```
import bigframes.pandas as bpd

# Set BigQuery DataFrames options
bpd.options.bigquery.project = your_gcp_project_id
bpd.options.bigquery.location = "US"

# BigQuery DataFrames gives you the ability to turn your custom functions
# into a BigQuery Python UDF. One can find more details about the usage and
# the requirements via `help` command.
help(bpd.udf)

# Read a table and inspect the column of interest.
df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
df["body_mass_g"].peek(10)

# Define a custom function, and specify the intent to turn it into a
# BigQuery Python UDF. Let's try a `pandas`-like use case in which we want
# to apply a user defined function to every value in a `Series`, more
# specifically bucketize the `body_mass_g` value of the penguins, which is a
# real number, into a category, which is a string.
@bpd.udf(
    dataset=your_bq_dataset_id,
    name=your_bq_routine_id,
)
def get_bucket(num: float) -> str:
    if not num:
        return "NA"
    boundary = 4000
    return "at_or_above_4000" if num >= boundary else "below_4000"

# Then we can apply the udf on the `Series` of interest via
# `apply` API and store the result in a new column in the DataFrame.
df = df.assign(body_mass_bucket=df["body_mass_g"].apply(get_bucket))

# This will add a new column `body_mass_bucket` in the DataFrame. You can
# preview the original value and the bucketized value side by side.
df[["body_mass_g", "body_mass_bucket"]].peek(10)

# The above operation was possible by doing all the computation on the
# cloud through an underlying BigQuery Python UDF that was created to
# support the user's operations in the Python code.

# The BigQuery Python UDF created to support the BigQuery DataFrames
# udf can be located via a property `bigframes_bigquery_function`
# set in the udf object.
print(f"Created BQ Python UDF: {get_bucket.bigframes_bigquery_function}")

# If you have already defined a custom function in BigQuery, either via the
# BigQuery Google Cloud Console or with the `udf` decorator,
# or otherwise, you may use it with BigQuery DataFrames with the
# `read_gbq_function` method. More details are available via the `help`
# command.
help(bpd.read_gbq_function)

existing_get_bucket_bq_udf = get_bucket.bigframes_bigquery_function

# Here is an example of using `read_gbq_function` to load an existing
# BigQuery Python UDF.
df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
get_bucket_function = bpd.read_gbq_function(existing_get_bucket_bq_udf)

df = df.assign(body_mass_bucket=df["body_mass_g"].apply(get_bucket_function))
df.peek(10)

# Let's continue trying other potential use cases of udf. Let's say we
# consider the `species`, `island` and `sex` of the penguins sensitive
# information and want to redact that by replacing with their hash code
# instead. Let's define another scalar custom function and decorate it
# as a udf. The custom function in this example has external package
# dependency, which can be specified via `packages` parameter.
@bpd.udf(
    dataset=your_bq_dataset_id,
    name=your_bq_routine_id,
    packages=["cryptography"],
)
def get_hash(input: str) -> str:
    from cryptography.fernet import Fernet

    # handle missing value
    if input is None:
        input = ""

    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(input.encode()).decode()

# We can use this udf in another `pandas`-like API `map` that
# can be applied on a DataFrame
df_redacted = df[["species", "island", "sex"]].map(get_hash)
df_redacted.peek(10)

# If the BigQuery routine is no longer needed, we can clean it up
# to free up any cloud quota
session = bpd.get_global_session()
session.bqclient.delete_routine(f"{your_bq_dataset_id}.{your_bq_routine_id}")
```

## 创建向量化 Python UDF

您可以使用向量化技术来实现 Python UDF，以处理一批行而不是单个行。向量化可以提高查询性能。

如需控制批处理行为，请使用 [`CREATE OR REPLACE FUNCTION` 选项列表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#function_option_list)中的 `max_batching_rows` 选项指定每个批次中的最大行数。如果您指定 `max_batching_rows`，BigQuery 会确定批次中的行数（不会超过 `max_batching_rows` 限制）。如果未指定 `max_batching_rows`，系统会自动确定要进行批处理的行数。

向量化 Python UDF 具有必须进行注解的单个 [`pandas.DataFrame`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) 参数。`pandas.DataFrame` 参数的列数与 `CREATE FUNCTION` 语句中定义的 Python UDF 参数相同。`pandas.DataFrame` 参数中的列名称与 UDF 的参数名称相同。

您的函数需要返回 [`pandas.Series`](https://pandas.pydata.org/docs/reference/api/pandas.Series.html#pandas.Series) 或单列 `pandas.DataFrame`，且行数与输入相同。

以下示例创建一个名为 `multiplyInputs` 的向量化 Python UDF，其中包含两个参数 `x` 和 `y`：

1. 转到 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下 `CREATE FUNCTION` 语句：

   ```
   CREATE FUNCTION `PROJECT_ID.DATASET_ID`.multiplyVectorized(x FLOAT64, y FLOAT64)
   RETURNS FLOAT64
   LANGUAGE python
   OPTIONS(runtime_version="python-3.11", entry_point="vectorized_multiply")
   AS r'''
   import pandas as pd

   def vectorized_multiply(df: pd.DataFrame):
     return df['x'] * df['y']

   ''';
   ```

   替换 PROJECT\_ID。DATASET\_ID 替换为您的项目 ID 和数据集 ID。

   调用 UDF 的方式与上一个示例相同。
3. 点击 play\_circle\_filled **运行**。

## 支持的 Python UDF 数据类型

下表定义了 BigQuery 数据类型、Python 数据类型和 Pandas 数据类型之间的映射：

| BigQuery 数据类型 | 标准 UDF 使用的 Python 内置数据类型 | 向量化 UDF 使用的 Pandas 数据类型 | 向量化 UDF 中用于 ARRAY 和 STRUCT 的 PyArrow 数据类型 |
| --- | --- | --- | --- |
| `BOOL` | `bool` | `BooleanDtype` | `DataType(bool)` |
| `INT64` | `int` | `Int64Dtype` | `DataType(int64)` |
| `FLOAT64` | `float` | `FloatDtype` | `DataType(double)` |
| `STRING` | `str` | `StringDtype` | `DataType(string)` |
| `BYTES` | `bytes` | `binary[pyarrow]` | `DataType(binary)` |
| `TIMESTAMP` | 函数参数：`datetime.datetime`（设置了世界协调时间 [UTC] 时区）  函数返回值：`datetime.datetime`（设置了任意时区） | 函数参数：`timestamp[us, tz=UTC][pyarrow]`  函数返回值：`timestamp[us, tz=*][pyarrow]\(any timezone\)` | `TimestampType(timestamp[us])`，带有时区 |
| `DATE` | `datetime.date` | `date32[pyarrow]` | `DataType(date32[day])` |
| `TIME` | `datetime.time` | `time64[pyarrow]` | `Time64Type(time64[us])` |
| `DATETIME` | `datetime.datetime`（不带时区） | `timestamp[us][pyarrow]` | `TimestampType(timestamp[us])`，不带时区 |
| `ARRAY` | `list` | `list<...>[pyarrow]`，其中元素数据类型为 [`pandas.ArrowDtype`](https://pandas.pydata.org/docs/reference/api/pandas.ArrowDtype.html) | `ListType` |
| `STRUCT` | `dict` | `struct<...>[pyarrow]`，其中字段数据类型为 [`pandas.ArrowDtype`](https://pandas.pydata.org/docs/reference/api/pandas.ArrowDtype.html) | `StructType` |

## 支持的运行时版本

BigQuery Python UDF 支持 `python-3.11` 运行时。此 Python 版本包含一些额外的预安装软件包。对于系统库，请检查运行时基础映像。

| 运行时版本 | Python 版本 | 包含 | 运行时基础映像 |
| --- | --- | --- | --- |
| python-3.11 | Python 3.11 | numpy 1.26.3 pyarrow 14.0.2  pandas 2.1.4  python-dateutil 2.8.2 | [google-22-full/python311](http://us-central1-docker.pkg.dev/serverless-runtimes/google-22-full/runtimes/python311) |

## 使用第三方软件包

您可以通过 [`CREATE FUNCTION` 选项列表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#function_option_list)来使用 [Python 标准库](https://docs.python.org/3/library/index.html)和预安装软件包提供的模块以外的模块。您可以通过 [Python 软件包索引 (PyPI)](https://pypi.org/) 安装软件包，也可以从 Cloud Storage 导入 Python 文件。

### 通过 Python 软件包索引安装软件包

安装软件包时，您必须提供软件包名称，还可以选择使用 [Python 软件包版本说明符](https://packaging.python.org/en/latest/specifications/version-specifiers)提供软件包版本。如果软件包在运行时中，则使用该软件包，除非在 `CREATE FUNCTION` 选项列表中指定了特定版本。如果未指定软件包版本，并且软件包不在运行时中，则使用最新可用版本。仅支持采用 [wheels 二进制格式](https://peps.python.org/pep-0427)的软件包。

以下示例展示了如何创建使用 `CREATE OR REPLACE FUNCTION` 选项列表安装 `scipy` 软件包的 Python UDF：

1. 转到 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下 `CREATE FUNCTION` 语句：

   ```
   CREATE FUNCTION `PROJECT_ID.DATASET_ID`.area(radius FLOAT64)
   RETURNS FLOAT64 LANGUAGE python
   OPTIONS (entry_point='area_handler', runtime_version='python-3.11', packages=['scipy==1.15.3'])
   AS r"""
   import scipy

   def area_handler(radius):
     return scipy.constants.pi*radius*radius
   """;

   SELECT `PROJECT_ID.DATASET_ID`.area(4.5);
   ```

   替换 PROJECT\_ID。DATASET\_ID 替换为您的项目 ID 和数据集 ID。
3. 点击 play\_circle\_filled **运行**。

### 将其他 Python 文件作为库导入

您可以通过从 Cloud Storage 导入 Python 文件，使用[函数选项列表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#function_option_list)来扩展 Python UDF。

**注意：**创建 UDF 的用户需要拥有 Cloud Storage 存储桶的 [`storage.objects.get`](https://docs.cloud.google.com/storage/docs/access-control/iam-permissions?hl=zh-cn#objects) 权限。

在 UDF 的 Python 代码中，您可以使用导入语句并且后跟 Cloud Storage 对象的路径，将 Cloud Storage 中的 Python 文件作为模块导入。例如，如果您要导入 `gs://BUCKET_NAME/path/to/lib1.py`，则导入语句应为 `import path.to.lib1`。

Python 文件名必须是 Python 标识符。对象名称（在 `/` 之后）中的每个 `folder` 名称都应是有效的 Python 标识符。在 ASCII 范围 (U+0001..U+007F) 内，标识符中可以使用以下字符：

* 大写字母和小写字母 A 到 Z。
* 下划线。
* 数字 0 到 9，但数字不能作为标识符中的第一个字符。

以下示例展示了如何创建从名为 `my_bucket` 的 Cloud Storage 存储桶导入 `lib1.py` 客户端库软件包的 Python UDF：

1. 转到 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下 `CREATE FUNCTION` 语句：

   ```
   CREATE FUNCTION `PROJECT_ID.DATASET_ID`.myFunc(a FLOAT64, b STRING)
   RETURNS STRING LANGUAGE python
   OPTIONS (
   entry_point='compute', runtime_version='python-3.11',
   library=['gs://my_bucket/path/to/lib1.py'])
   AS r"""
   import path.to.lib1 as lib1

   def compute(a, b):
     # doInterestingStuff is a function defined in
     # gs://my_bucket/path/to/lib1.py
     return lib1.doInterestingStuff(a, b);

   """;
   ```

   替换 PROJECT\_ID。DATASET\_ID 替换为您的项目 ID 和数据集 ID。
3. 点击 play\_circle\_filled **运行**。

## 为 Python UDF 配置容器限制

您可以使用 [`CREATE FUNCTION` 选项列表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#function_option_list)为运行 Python UDF 的容器指定 CPU 和内存限制。

默认情况下，为每个容器实例分配的内存为 512 MiB，分配的 CPU 为 0.33 个 vCPU。

以下示例通过使用 `CREATE FUNCTION` 选项列表指定容器限制来创建一个 Python UDF：

1. 转到 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下 `CREATE FUNCTION` 语句：

   ```
   CREATE FUNCTION `PROJECT_ID.DATASET_ID`.resizeImage(image BYTES)
   RETURNS BYTES LANGUAGE python
   OPTIONS (entry_point='resize_image', runtime_version='python-3.11',
   packages=['Pillow==11.2.1'], container_memory='2Gi', container_cpu=1)
   AS r"""
   import io
   from PIL import Image

   def resize_image(image_bytes):
     img = Image.open(io.BytesIO(image_bytes))

     resized_img = img.resize((256, 256), Image.Resampling.LANCZOS)
     output_stream = io.BytesIO()
     resized_img.convert('RGB').save(output_stream, format='JPEG')
     return output_stream.getvalue()
   """;
   ```

   替换 PROJECT\_ID。DATASET\_ID 替换为您的项目 ID 和数据集 ID。
3. 点击 play\_circle\_filled **运行**。

### 支持的 CPU 值

Python UDF 支持介于 `0.33` 和 `1.0` 之间的小数形式 CPU 值，以及非小数形式 CPU 值 `1`、`2`。在将小数输入值应用于容器之前，系统会将其四舍五入为两位小数。

### 支持的内存值

Python UDF 容器支持以下格式的内存值：`<integer_number><unit>`。单位必须是以下值之一：`Mi`、`M`、`Gi`、`G`。您可以配置的内存量下限为 256 兆比字节 (256 Mi)。您可以配置的内存量上限为 8 吉比字节 (8 Gi)。

根据您选择的内存值，您还必须指定 CPU 量下限。下表显示了每个内存值对应的 CPU 下限值：

| 内存 | CPU 下限 |
| --- | --- |
| `512 MiB or less` | `0.33` |
| `More than 512 MiB` | `0.5` |
| `More than 1 GiB` | `1` |
| `More than 4 GiB` | `2` |

## 在 Python 代码中调用 Google Cloud 或在线服务

Python UDF 使用 [Cloud 资源连接](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-cn)服务账号访问 Google Cloud 服务或外部服务。您必须向连接的服务账号授予访问相应服务的权限。所需的权限因所访问的服务以及从 Python 代码调用的 API 而异。

如果您创建 Python UDF 时未使用 Cloud 资源连接，则函数会在阻止网络访问的环境中执行。如果您的 UDF 会访问在线服务，则必须使用 Cloud 资源连接创建 UDF。如果不这样做，系统会阻止 UDF 访问网络，直到达到内部连接超时时间。

以下示例展示了如何从 Python UDF 访问 Cloud Translation 服务。此示例包含两个项目：一个名为 `my_query_project` 的项目，您会在其中创建 UDF 和 Cloud 资源连接；以及一个名为 `my_translate_project` 的项目，您会在其中运行 Cloud Translation。

### 创建 Cloud 资源连接

首先，您需要在 `my_query_project` 中创建 Cloud 资源连接。如需创建 Cloud 资源连接，请按照[创建 Cloud 资源连接](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-cn#create-cloud-resource-connection)页面上的步骤操作。

创建连接后，打开连接，然后在**连接信息**窗格中复制服务账号 ID。为连接配置权限时，您需要使用此 ID。当您创建连接资源时，BigQuery 会创建一个唯一的系统服务账号，并将其与该连接相关联。

### 向连接的服务账号授予访问权限

如需向 Cloud 资源连接服务账号授予对项目的访问权限，请在 `my_query_project` 中向该服务账号授予 [Service Usage Consumer 角色](https://docs.cloud.google.com/service-usage/docs/access-control?hl=zh-cn#serviceusage.serviceUsageConsumer) (`roles/serviceusage.serviceUsageConsumer`)，并在 `my_translate_project` 中向该服务账号授予 [Cloud Translation API User 角色](https://docs.cloud.google.com/translate/docs/access-control?hl=zh-cn#cloudtranslate.user) (`roles/cloudtranslate.user`)。

1. 转到 **IAM** 页面。

   [转到 IAM](https://console.cloud.google.com/project/_/iam-admin?hl=zh-cn)
2. 验证是否选择了 `my_query_project`。
3. 点击 person\_add **授予访问权限**。
4. 在**新建主账号**字段中，输入您之前复制的 Cloud 资源连接的服务账号 ID。
5. 在**选择角色**字段中，选择 **Service Usage**，然后选择 **Service Usage Consumer**。
6. 点击**保存**。
7. 在项目选择器中，选择 **`my_translate_project`**。
8. 转到 **IAM** 页面。

   [转到 IAM](https://console.cloud.google.com/project/_/iam-admin?hl=zh-cn)
9. 点击 person\_add **授予访问权限**。
10. 在**新建主账号**字段中，输入您之前复制的 Cloud 资源连接的服务账号 ID。
11. 在**选择角色**字段中，选择 **Cloud Translation**，然后选择 **Cloud Translation API User**。
12. 点击**保存**。

### 创建调用 Cloud Translation 服务的 Python UDF

在 `my_query_project` 中，创建一个 Python UDF，以使用您的 Cloud 资源连接调用 Cloud Translation 服务。

1. 转到 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中输入以下 `CREATE FUNCTION` 语句：

   ```
   CREATE FUNCTION `PROJECT_ID.DATASET_ID`.translate_to_es(x STRING)
   RETURNS STRING LANGUAGE python
   WITH CONNECTION `PROJECT_ID.REGION.CONNECTION_ID`
   OPTIONS (entry_point='do_translate', runtime_version='python-3.11', packages=['google-cloud-translate>=3.11', 'google-api-core'])
   AS r"""

   from google.api_core.retry import Retry
   from google.cloud import translate

   project = "my_translate_project"
   translate_client = translate.TranslationServiceClient()

   def do_translate(x : str) -> str:

       response = translate_client.translate_text(
           request={
               "parent": f"projects/{project}/locations/us-central1",
               "contents": [x],
               "target_language_code": "es",
               "mime_type": "text/plain",
           },
           retry=Retry(),
       )
       return response.translations[0].translated_text

   """;

   -- Call the UDF.
   WITH text_table AS
     (SELECT "Hello" AS text
     UNION ALL
     SELECT "Good morning" AS text
     UNION ALL
     SELECT "Goodbye" AS text)
   SELECT text,
   `PROJECT_ID.DATASET_ID`.translate_to_es(text) AS translated_text
   FROM text_table;
   ```

   替换以下内容：

   * `PROJECT_ID.DATASET_ID`：您的项目 ID 和数据集 ID
   * `REGION.CONNECTION_ID`：您的连接的区域和连接 ID
3. 点击 play\_circle\_filled **运行**。

   输出应如下所示：

   ```
   +--------------------------+-------------------------------+
   | text                     | translated_text               |
   +--------------------------+-------------------------------+
   | Hello                    | Hola                          |
   | Good morning             | Buen dia                      |
   | Goodbye                  | Adios                         |
   +--------------------------+-------------------------------+
   ```

## 支持的位置

所有 BigQuery [多区域和单区域位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)都支持 Python UDF。

## 价格

使用 Python UDF 时无需任何额外的费用。

启用结算功能后，以下规则适用：

* Python UDF 费用采用 [BigQuery 服务 SKU](https://cloud.google.com/skus?amp%3Bfilter=bigquery&%3Bcurrency=USD&hl=zh-cn) 计费。
* 费用与调用 Python UDF 时消耗的计算量和内存量成正比。
* Python UDF 客户还需要支付构建或重新构建 UDF 容器映像的费用。此费用与使用客户代码和依赖项构建映像所用的资源成正比。
* 如果 Python UDF 导致外部或互联网网络出站流量，您还会看到 Cloud Networking 收取的[高级层级](https://cloud.google.com/network-tiers/pricing?hl=zh-cn)互联网出站流量费用。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-02-26。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-02-26。"],[],[]]