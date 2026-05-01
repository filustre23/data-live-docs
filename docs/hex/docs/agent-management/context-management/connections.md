On this page

# Connections

Connect different data sources to Hex for use in analysis and tasks by the Hex Agent.

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Only **Admins** and **Managers** can create or edit external connections.

Connections let you bring context from outside of Hex into the Context Studio so the Hex Agent can use it when reasoning about your workspace.

## Pushing context to Hex[​](#pushing-context-to-hex "Direct link to Pushing context to Hex")

Upload [guides](/docs/agent-management/context-management/guides) from an external source such as a GitHub repository, so the Hex Agent can reference them alongside guides authored directly in Hex.

External guides are stored in Hex and are not fetched live from the source. You keep them up to date by pushing new content through the API, most commonly via a GitHub Action.

See [Programmatically upload guides in CI](/docs/agent-management/context-management/guides#programmatically-upload-guides-in-ci) for a full walkthrough, including the recommended `hex_context_toolkit.yml` workflow.

#### On this page

* [Pushing context to Hex](#pushing-context-to-hex)