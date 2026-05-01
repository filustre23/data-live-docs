On this page

# Using packages

Working with packages is an important part of using Python in Hex.

## Use a pre-installed package[​](#use-a-pre-installed-package "Direct link to Use a pre-installed package")

Hex has a number of popular packages pre-installed and immediately ready for `import` into your project. You can see the list of pre-installed packages in the Environment tab in the left-hand bar.

## Install new packages through `pip`[​](#install-new-packages-through-pip "Direct link to install-new-packages-through-pip")

You can add new packages to a project using pip, much as you would in a local environment.

Create a new cell, and use a `!` to trigger a terminal command:

```
!pip install astropy
```

Because projects are run from top to bottom with a new kernel every time a user visits, packages installed with `!pip install` have to be reinstalled every time your project runs, which can slow down project runtime.

tip

We recommend using `!uv pip install` instead of `!pip install` for a big speed boost; [see below](#install-new-packages-through-uv-pip) 🚀

Note that when you run `!pip install`, Hex will print a message suggesting you change the command to `!uv pip install` for performance. To disable this message, use `!python -m pip install` instead.

## Install new packages through `uv pip`[​](#install-new-packages-through-uv-pip "Direct link to install-new-packages-through-uv-pip")

[`uv pip`](https://docs.astral.sh/uv/) is a drop-in replacement for pip that installs packages [10-100x faster](https://github.com/astral-sh/uv/blob/main/BENCHMARKS.md). Hex's images comes pre-installed with uv.

Use `uv pip install` exactly the same way as `pip install`:

```
!uv pip install astropy
```

Packages installed with `!uv pip install` will still be reinstalled every time your project runs. Because it's faster, though, they won't add nearly as much to project startup time as `!pip install` would.

You can read more about the [`uv pip` interface](https://docs.astral.sh/uv/pip/) and its [compatibility with pip](https://docs.astral.sh/uv/pip/compatibility/) on Astral's documentation.

### Fixed package versioning[​](#fixed-package-versioning "Direct link to Fixed package versioning")

When starting a new kernel, Hex loads specific versions of some packages that are core to its functionality. This process causes these packages to remain fixed to the versions that Hex imports. Attempting to update the version of these packages can result in errors. Below is a list of packages whose versions cannot be changed:

| Package |
| --- |
| `cryptography` |
| `duckdb` |
| `ipykernel` |
| `ipython` |
| `ipython_genutils` |
| `jedi` |
| `Jinja2` |
| `jinjasql` |
| `numpy` |
| `pandas` |
| `psutil` |
| `pyarrow` |
| `snowflake-connector-python` |
| `vegafusion` |
| `vegafusion-python-embed` |

To check the default version of any package, check the "Pre-installed packages" list found in the Environment tab.

### Troubleshoot package installation[​](#troubleshoot-package-installation "Direct link to Troubleshoot package installation")

Occasionally after upgrading a package, importing the package will result in a `ContextualVersionConflict` exception that indicates the package is still on the version originally installed in Hex. This can happen if the package relies on the `pkg_resources` module to check for version conflicts during its setup. You can resolve this issue by reloading `pkg_resources` after the package installation, but before the package is imported:

```
import pkg_resources  
from importlib import reload  
  
!uv pip install {my_package}  
  
reload(pkg_resources)  
  
import {my_package}
```

## Git packages[​](#git-packages "Direct link to Git packages")

If your workspace has been set up to use packages from a Git repository, you can install those packages for use in any project. See [Git packages](/docs/administration/workspace_settings/workspace-assets#Git-packages) for setup instructions.

To use a package that's been added in your workspace, follow these steps:

**1.** Import your workspace package from the **Environments** section of the left sidebar. Once you've done this, your repo will show up as a folder in your project's [file directory](/docs/explore-data/projects/environment-configuration/files#file-directory) with the naming convention of `{{Git user}}-{{Git package name}}`.

[](/assets/medias/import-gh-35fc57a467748685a2f9f0493efda41d.mp4)

**2.** To import functions from `.py` files included in your package, you will first need to add the path to those files to your Python path. Packages are automatically saved to a directory with a naming convention of `{{GitHub origin of repository}}-{{GitHub package name}}`. For example, the `draw_hexagon` package is associated with the `jackjackins` GitHub user, so the following code would be used to set the path to import functions from the package.

```
import sys, os  
sys.path.append(os.path.abspath('jackjackins-draw_hexagon/'))
```

info

If you are not sure which path to use, you can run `!ls` in a code cell to see the exact name of the directory (the directory will appear after the package has been added to the project).

**3.** Depending on how your [Git package](/docs/administration/workspace_settings/workspace-assets#Git-packages) has been configured, some modules may have already been installed. In this case, those modules are immediately available for use, just `import {{package name}}` in a Python cell as usual.

Git packages are re-imported from Git with every kernel restart of your project. If your package is particularly large this can add some overhead to the initial performance and load time of your projects. Additionally, if your Git package was configured to import a specific branch of the package, upon each kernel restart, the latest version of the branch will be imported.

## Set number of available cores[​](#set-number-of-available-cores "Direct link to Set number of available cores")

Some packages attempt to autodetect the number of available cores, so they can generate a certain number of threads accordingly. In some cases, a package may incorrectly scope the kernel being used in the project. To optimize performance for packages that behave in this way, users can use [`hextoolkit`](/tutorials/connect-to-data/using-the-hextoolkit) to correctly assign the number of available cores using code like the following:

```
import hextoolkit.kernel  
num_cpus = hextoolkit.kernel.cpu_count()
```

Then, the package-specific parameter used to set the number of available cores can be set to `num_cpus`.

#### On this page

* [Use a pre-installed package](#use-a-pre-installed-package)
* [Install new packages through `pip`](#install-new-packages-through-pip)
* [Install new packages through `uv pip`](#install-new-packages-through-uv-pip)
  + [Fixed package versioning](#fixed-package-versioning)
  + [Troubleshoot package installation](#troubleshoot-package-installation)
* [Git packages](#git-packages)
* [Set number of available cores](#set-number-of-available-cores)