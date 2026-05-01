On this page

# SSO

Hex supports integrating with SSO providers via the OpenID Connect (OIDC) protocol.

info

* Available on the Enterprise [plan](https://hex.tech/pricing/).
* Users will need the Admin workspace role to configure SSO.
* Hex supports SSO via OpenID Connect (OIDC). SAML is not supported.

Enabling Single Sign-On (SSO) centralizes the authentication process, enabling users to sign in once with their primary workspace platform using a single set of credentials and gain access to other approved applications without needing to log in separately to each one.

You can configure Hex to authenticate users through your chosen SSO provider using the OpenID Connect (OIDC) protocol. Hex does not support SAML.

## Configuring SSO[​](#configuring-sso "Direct link to Configuring SSO")

To configure SSO in Hex, there are two primary steps:

1. Creating the OIDC application in your SSO provider's administrative platform
2. Configuring Hex to integrate with your SSO provider via Hex's workspace settings page

### Create an OIDC Application in an SSO Provider[​](#create-an-oidc-application-in-an-sso-provider "Direct link to Create an OIDC Application in an SSO Provider")

tip

* Creating an OIDC application likely requires administrative credentials within the SSO provider's platform. You may need to work with the team at your organization that handles Identity and Access Management (IAM) to complete this step, often IT or Security.
* [Reference the OpenID Connect specification](https://openid.net/specs/openid-connect-discovery-1_0.html)

You should refer to your SSO provider's documentation for the specific steps to create an OIDC application. OIDC is built on top of the OAuth 2.0 authorization framework. Depending on how your provider has structured their documentation, you may see OIDC credentials referred to as OAuth 2.0 credentials.

For quick reference, we link to the documentation for several major providers below. If your provider is not listed below and you are not sure where to find their documentation, we recommend reaching out to them directly for instruction.

Documentation for common SSO providers:

* [Google](https://developers.google.com/identity/openid-connect/openid-connect)
* [Okta](https://support.okta.com/help/s/article/create-an-oidc-web-app-in-dashboard?language=en_US)
* [Azure/Entra](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)
* [Duo](https://duo.com/docs/sso-oidc-generic#configure-single-sign-on)

For many providers, you will follow a set of steps similar to those below:

1. Log into the SSO provider's administrative platform
2. Navigate to the page where applications are managed
3. Create a new application or integration
4. Give the new application a name (e.g. *Hex*)
5. Select OpenID Connect as the sign-in method
6. Select 'website' or 'web' as the platform type
7. Fill out the Hex redirect URIs, which you can find below
8. Fill out any additional required fields per your SSO provider's documentation
9. Save the application configuration

Once configured, the SSO provider will generate a **Client ID** and **Client Secret** for the app. You will need to enter these, along with the **Issuer**, into Hex's platform to complete the configuration. See the Configuring Hex to Integrate With Your SSO Provider section below for more detail.

#### Redirect URIs[​](#redirect-uris "Direct link to Redirect URIs")

You will need to provide redirect URIs when creating the OIDC application. Choose from the options below based on where your Hex workspace is hosted.

You can find where your workspace is hosted by logging into Hex and checking the part of the URL between `https://` and `/<YOUR-ORG-NAME-OR-ID>`.

For Hex workspaces hosted at `app.hex.tech`:

* Sign-In Redirect URI should be in the format `https://app.hex.tech/auth/<YOUR-ORG-NAME>/sso`
* Sign-Out Redirect URI should be in the format `https://app.hex.tech/<YOUR-ORG-NAME>`

For Hex workspaces hosted at `eu.hex.tech`:

* Sign-In Redirect URI should be in the format `https://eu.hex.tech/auth/<YOUR-ORG-NAME>/sso`
* Sign-Out Redirect URI should be in the format `https://eu.hex.tech/<YOUR-ORG-NAME>`

For Hex workspaces hosted at `hc.hex.tech`:

* Sign-In Redirect URI should be in the format `https://hc.hex.tech/auth/<YOUR-ORG-NAME>/sso`
* Sign-Out Redirect URI should be in the format `https://hc.hex.tech/<YOUR-ORG-NAME>`

For single-tenant dedicated installs:

* Sign-In Redirect URI should be in the format `https://<YOUR-HEX-DOMAIN-NAME>/auth/global/sso`
* Sign-Out Redirect URI should be in the format `https://<YOUR-HEX-DOMAIN-NAME>`

### Configure Hex to Integrate With Your SSO Provider[​](#configure-hex-to-integrate-with-your-sso-provider "Direct link to Configure Hex to Integrate With Your SSO Provider")

tip

* We strongly recommend validating that the SSO login flow works as expected before opting to **Enforce SSO**.

Once you have created the OIDC application with your SSO provider and noted the **Client ID**, **Client Secret**, and **Issuer**, you will need to set up the SSO integration in your Hex workspace.

1. Navigate to the **SSO** tab in the **Access & Security** section of your **Workspace settings** page
2. Fill out the **Issuer** field (see below for examples of what this may look like)
3. Fill out the **Client ID** and **Client Secret** fields
4. Toggle the **Enable SSO** switch on to allow users to sign on with SSO
5. Log out and back in to confirm the SSO login flow works as intended
6. *Optional:* Toggle the **Enforce SSO** switch to require users to sign on with SSO

caution

When SSO is enforced, the login page will only display the SSO button. The email/password login form will be hidden for all users, including workspace Admins.

Hex strongly recommends testing your SSO login flow before enabling enforcement. If your SSO provider becomes misconfigured and workspace Admins are locked out, they can navigate directly to `https://app.hex.tech/<YOUR-ORG-NAME>/login?password=true` to access a password login form. This URL is not linked anywhere in the Hex UI and is intended only as a last-resort emergency option—it will only work for workspace Admin accounts. Note that password-based login is planned for deprecation in the future.

#### Common SSO Provider Configuration Endpoint Formats[​](#common-sso-provider-configuration-endpoint-formats "Direct link to Common SSO Provider Configuration Endpoint Formats")

The response from the configuration endpoint will give you the Issuer. This will look like a URL that ends in `/.well-known/openid-configuration`.

It's important to note that the actual issuer URL may vary based on your specific SSO provider setup and configuration. Therefore, always refer your SSO provider's documentation or your organization's configuration details for the precise issuer URL format to use.

* **Google:** `https://accounts.google.com/.well-known/openid-configuration`
* **Okta:** `https://<YOUR-OKTA-ACCOUNT>.okta.com/.well-known/openid-configuration`
* **Azure/Entra:** `https://login.microsoftonline.com/<YOUR-TENANT>/v2.0/.well-known/openid-configuration`
* **Duo:** `https://sso-<integration_key>.duo.com/.well-known/openid-configuration`

#### On this page

* [Configuring SSO](#configuring-sso)
  + [Create an OIDC Application in an SSO Provider](#create-an-oidc-application-in-an-sso-provider)
  + [Configure Hex to Integrate With Your SSO Provider](#configure-hex-to-integrate-with-your-sso-provider)