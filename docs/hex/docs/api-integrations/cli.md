On this page

# CLI overview

Interact with Hex via the command line.

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Requires a [personal access token](/docs/api-integrations/api/overview#personal-access-tokens). Admins must enable API access from the **Integrations** tab in Workspace settings before users can create tokens. See [Workspace assets](/docs/administration/workspace_settings/workspace-assets).
* Hex CLI is being actively developed. Commands and configuration are subject to change.
* CLI tool calls do not currently consume [Credits](/docs/administration/credits). Credit consumption may apply in the future.

The Hex CLI manages Hex projects, cells, runs, data connections, and workspace resources from the command line. This can be used directly or via a local AI agent to automate Hex workflows, create and modify notebook cells, trigger project runs, and inspect workspace state.

## Installation[​](#installation "Direct link to Installation")

Install the CLI with [Homebrew](https://brew.sh/):

```
brew install hex-inc/hex-cli/hex
```

Alternatively, you can manually install the CLI using the following command:

```
curl -fsSL https://hex.tech/install.sh | bash
```

Verify the installation using:

```
hex --version
```

The Hex CLI will automatically check for updates and prompt you any time an update is available. Hex CLI releases are hosted on [GitHub](https://github.com/hex-inc/hex-cli/releases).

info

The Hex CLI is currently available for MacOS and Linux users, and is not supported for Windows. Consider using [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install) to install the CLI.

## Authentication[​](#authentication "Direct link to Authentication")

To get started:

```
hex auth login
```

This will open a web browser to select and log into the workspace you wish to use for the CLI. Credentials are stored securely in your system keyring.

If your workspace has a custom URL (such as for single-tenant or EU customers), specify the base URL as part of the login command:

```
hex auth login -H https://myorganization.hex.tech
```

You can verify authentication with:

```
hex auth status  
hex projects list
```

### Using the CLI with multiple accounts or workspaces[​](#using-the-cli-with-multiple-accounts-or-workspaces "Direct link to Using the CLI with multiple accounts or workspaces")

If you are part of multiple workspaces, you log into each of them separately using the Hex CLI. When logging in, specify a profile name which will be used for each account:

```
hex auth login workspace1  
hex auth login workspace2  
hex auth login euworkspace -H https://eu.hex.tech
```

Switch the currently active account using `hex auth switch <profile_name>`. The currently active account is global and shared across shell sessions.

### Authenticating in CI[​](#authenticating-in-ci "Direct link to Authenticating in CI")

In CI, you can run `hex auth login` with the `--token-from-env <env_var>` flag and pass in a [workspace access token](/docs/api-integrations/api/overview#workspace-tokens) as environment variable.

```
HEX_API_TOKEN="my-token" hex auth login --token-from-env HEX_API_TOKEN  
  
HEX_API_TOKEN="my-token" hex auth login --token-from-env HEX_API_TOKEN -H https://eu.hex.tech
```

## Usage[​](#usage "Direct link to Usage")

The CLI documents itself with the `--help` flag:

```
hex --help  
  
# subcommands are also documented using the `--help` flag  
hex auth --help
```

```
Usage: hex [OPTIONS] [COMMAND]  
  
Commands:  
  app          Manage and run Hex apps  
  project      Manage and run Hex projects  
  cell         Manage project cells  
  run          Manage running Hex projects and apps  
  connection   Manage data connections  
  collection   Manage project collections  
  group        Manage workspace groups  
  user         Manage workspace users  
  auth         Manage authentication with Hex  
  install      Manage additional tools provided by the Hex CLI, such as Claude skills  
  config       Manage CLI configuration  
  completions  Generate shell completion scripts  
  help         Print this message or the help of the given subcommand(s)  
  
Options:  
      --profile <PROFILE>  Profile to use (from ~/.config/hex/config.toml) [env: HEX_PROFILE=]  
      --json               Output as JSON (for scripting)  
  -q, --quiet              Suppress non-essential output  
  -v, --verbose            Show verbose output for debugging  
      --no-color           Disable colored output  
  -h, --help               Print help  
  -V, --version            Print version
```

### Configuration for AI agents[​](#configuration-for-ai-agents "Direct link to Configuration for AI agents")

AI agents that can interact with your command line, such as Claude Code, can be instructed to use the `hex` CLI to accomplish tasks. Install the available Claude skill with `hex install agent-skill --claude`.

## Bugs & issues[​](#bugs--issues "Direct link to Bugs & issues")

Please contact [[email protected]](/cdn-cgi/l/email-protection#780b0d0808170a0c38101d00560c1d1b10) if you encounter any bugs, or other issues.

#### On this page

* [Installation](#installation)
* [Authentication](#authentication)
  + [Using the CLI with multiple accounts or workspaces](#using-the-cli-with-multiple-accounts-or-workspaces)
  + [Authenticating in CI](#authenticating-in-ci)
* [Usage](#usage)
  + [Configuration for AI agents](#configuration-for-ai-agents)
* [Bugs & issues](#bugs--issues)