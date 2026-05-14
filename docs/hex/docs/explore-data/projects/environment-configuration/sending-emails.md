On this page

# Sending emails

Hex has an email sending policy to ensure compliance with its cloud hosting providers and maintain the security and integrity of our platform.

## Email policy[​](#email-policy "Direct link to Email policy")

SMTP (ports 25, 465, and 587) is blocked to prevent spam and other abuses of our platform.

Even if SMTP were available, we strongly recommend against sending email directly in favor of using a dedicated email deliverability platform. Dedicated email deliverability platforms are better at handling deliverability factors such as IP reputation.

To send emails directly from Hex, managed emails services such as [Amazon SES](https://docs.aws.amazon.com/ses/latest/dg/send-email-api.html), [Mailchimp](https://mailchimp.com/developer/transactional/guides/quick-start/), or [SendGrid](https://www.twilio.com/docs/sendgrid/for-developers/sending-email/quickstart-python) can be used.

### Exceptions[​](#exceptions "Direct link to Exceptions")

Organizations can continue to use SMTP to send emails if they are:

* Paying customers using SMTP prior to April 2025
* Organizations with an approved exception
* Single-tenant, non-HIPAA-compliant customers

HIPAA-compliant workspaces will not have the ability to send emails to maintain the protection of personal information.

info

Reach out to [[email protected]](/cdn-cgi/l/email-protection#cbb8bebbbba4b9bf8ba3aeb3e5bfaea8a3) to request your organization be considered for an exception.

#### On this page

* [Email policy](#email-policy)
  + [Exceptions](#exceptions)