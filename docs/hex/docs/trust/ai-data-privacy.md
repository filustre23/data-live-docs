On this page

# AI data privacy

Data privacy is our top priority.

Hex offers first-class support for data privacy through initiatives like Workspace AI features opt-out, Bring Your Own Key (BYOK), and geographic data residency.

## Workspace AI features opt-out[​](#workspace-ai-features-opt-out "Direct link to Workspace AI features opt-out")

Hex admins can opt-out their entire workspace from AI features from the **Settings > AI & agents** settings page. Opting out of AI features at the **AI & agents settings**-level will disable AI features for all users.

### AI training opt-out[​](#ai-training-opt-out "Direct link to AI training opt-out")

Depending on your plan, Hex may use data from your AI sessions to improve Hex's AI features. You can opt out of this at any time in **Settings** > **AI & agents** without disabling AI features. See your applicable [Terms of Service](/docs/legal/terms-and-conditions) for details.

## Third-party partner interactions[​](#third-party-partner-interactions "Direct link to Third-party partner interactions")

* Hex's LLM providers do not train on customer data and have a zero retention policy. Hex's use of AI session data to improve its AI features is governed by your applicable [Terms of Service](/docs/legal/terms-and-conditions). Hex does not disclose customer data to other customers. **Our LLM providers have a zero retention policy**, so your data is never stored.
* **Hex uses Customer Database Metadata like schemas and Customer Data project code and output content as model context**. This means that any sensitive information in your projects, table or column names, or in your code, could be passed to a model for inference.
* **Hex's AI features are built on Hex’s secure data platform**. These features are protected by secure practices and policies, are included in our third-party audits and bug bounty program, and safeguarded by the principle of least-privilege. You can learn more on our [Data Privacy and Usage FAQ](/docs/trust/data-privacy-and-usage-faq), [Trust Center](https://trust.hex.tech/), and read our [AI Product Specific Terms](/docs/legal/hex-service-agreement#hex-magic-and-hex-magic-typeahead-collectively-hex-magic).

## Bring Your Own Key (BYOK)[​](#bring-your-own-key-byok "Direct link to Bring Your Own Key (BYOK)")

info

* Available on the **Enterprise** [plan](https://hex.tech/pricing).
* BYOK is supported for OpenAI and Anthropic.

warning

When using your own API key, please note that Hex does not take responsibility for any cost incurred by the API calls. We encourage you to set up billing alerts for your API keys to monitor usage and costs.

When you enable Hex's AI features, Enterprise Admins can specify their own API key for those AI features
to use when making OpenAI and Anthropic API calls.

To use an API key generated in OpenAI or Anthropic, head to **Settings > AI & agents** and select the **Add an API key** button at the right side of the **Model provider** setting (Under **Model settings**).

Once a key has been added, you can add a new API key from the refresh button at the right side of the **Model provider** setting.

tip

BYOK is currently available only for OpenAI and Anthropic. Please reach out to [[email protected]](/cdn-cgi/l/email-protection#1764626767786563577f726f396372747f) if you're interested in using another provider.

#### On this page

* [Workspace AI features opt-out](#workspace-ai-features-opt-out)
  + [AI training opt-out](#ai-training-opt-out)
* [Third-party partner interactions](#third-party-partner-interactions)
* [Bring Your Own Key (BYOK)](#bring-your-own-key-byok)