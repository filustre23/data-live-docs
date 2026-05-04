On this page

# Billing FAQ

Frequently asked questions about Hex billing, pricing, payments, and invoices.

## Billing basics[​](#billing-basics "Direct link to Billing basics")

### How does Hex's billing structure work?[​](#how-does-hexs-billing-structure-work "Direct link to How does Hex's billing structure work?")

#### Self-serve customers[​](#self-serve-customers "Direct link to Self-serve customers")

Self-serve customers are billed monthly. The credit card on file is automatically charged through Stripe upon invoice generation.

* Invoices bill active seats in advance for the upcoming period
* Any seat count changes made during a previously billed period are charged in arrears on a prorated basis on the next invoice, as well as billed in advance on all subsequent invoices until the customer makes further adjustments

#### Order form customers[​](#order-form-customers "Direct link to Order form customers")

**Order form customers** are billed annually and upfront according to the terms in their signed order form.

* Committed seats are billed annually
* Overages for uncommitted seats and usage are billed in arrears separately on a basis specified in the signed order form
* Standard payment terms are **Net 30**, unless otherwise specified in the agreement

### What does "billed in advance" or "billed in arrears" mean?[​](#what-does-billed-in-advance-or-billed-in-arrears-mean "Direct link to What does \"billed in advance\" or \"billed in arrears\" mean?")

#### Billed in advance[​](#billed-in-advance "Direct link to Billed in advance")

Billed in advance means customers are charged for their seats at the start of the upcoming billing period.

**Self-serve example:**

* Invoice 001 is issued on **January 1**
* The customer has **10 active author seats**
* The invoice bills those 10 seats in advance for the period of **January 1 – January 31**

#### Billed in arrears[​](#billed-in-arrears "Direct link to Billed in arrears")

Billed in arrears means customers are charged after the fact for seat changes that occurred during a period that was already billed in advance. These charges are calculated on a prorated basis and appear on the next invoice.

This applies to:

* All seat changes for self-serve customers
* Monthly overages for uncommitted seats and usage for order form customers

**Self-serve example:**

* Invoice 001 billed **10 seats in advance** for **January 1 – January 31**
* On **January 15**, the customer adds **5 additional seats**
* Those 5 seats were active from **January 16 – January 31 (16 days)**
* On Invoice 002, the customer will be charged:
  + **5 seats × seat price × prorated portion of 16 days**

Additionally, assuming no other changes:

* Invoice 002 will also include **15 seats billed in advance** for the next period (**February 1 – February 28**)

### What happens if I adjust seats mid-billing cycle?[​](#what-happens-if-i-adjust-seats-mid-billing-cycle "Direct link to What happens if I adjust seats mid-billing cycle?")

#### Self-serve customers[​](#self-serve-customers-1 "Direct link to Self-serve customers")

All seat adjustments are handled on a prorated basis.

* **Seats added:** The additional seats are prorated for the remaining time in the current period and charged on the next invoice.
* **Seats removed:** A prorated credit for the unused time remaining is applied to the next invoice.

#### Order form customers[​](#order-form-customers-1 "Direct link to Order form customers")

Prorated adjustments apply only to overages in uncommitted seats.

* Committed seats are billed annually and upfront and governed by the terms of the customer's signed order form
* Overages in uncommitted seats are billed on a basis specified in your specific order form

### Can you explain how proration works?[​](#can-you-explain-how-proration-works "Direct link to Can you explain how proration works?")

Proration applies when author seats are added or removed mid-billing cycle. Rather than charging or crediting a full month, credits/charges are based on how long the seat was active during that billing period.

* **Seats added mid-cycle:** You are charged only for the portion of the period that the seats were active.
* **Seats removed mid-cycle:** A prorated credit is applied for the unused time remaining in the period.

For self-serve customers, proration applies to all seat changes. For order form customers, proration applies only to uncommitted seats.

---

## Pricing and plans[​](#pricing-and-plans "Direct link to Pricing and plans")

### Where can I see Hex's pricing?[​](#where-can-i-see-hexs-pricing "Direct link to Where can I see Hex's pricing?")

#### Self-serve customers[​](#self-serve-customers-2 "Direct link to Self-serve customers")

Standard pricing is available on the [Hex pricing page](https://hex.tech/pricing/), which outlines current plan options and per-seat rates. Per-seat rates and total seat counts are also listed directly on the customer's invoice.

#### Order form customers[​](#order-form-customers-2 "Direct link to Order form customers")

Your pricing is governed by your **executed order form** with Hex which outlines:

* Your committed seat count
* Per-seat pricing
* Billing terms

If you need a copy of your order form, please reach out to your Hex account executive.

### Do you offer nonprofit discounts?[​](#do-you-offer-nonprofit-discounts "Direct link to Do you offer nonprofit discounts?")

Yes. Please contact [[email protected]](/cdn-cgi/l/email-protection#24464d48484d4a43575154544b5650644c415c0a5041474c) with your workspace URL and nonprofit documentation.

### Do you offer student or educational plans?[​](#do-you-offer-student-or-educational-plans "Direct link to Do you offer student or educational plans?")

Yes. Please contact [[email protected]](/cdn-cgi/l/email-protection#94f6fdf8f8fdfaf3e7e1e4e4fbe6e0d4fcf1ecbae0f1f7fc) using your educational email address and include your workspace URL.

---

## Workspace management[​](#workspace-management "Direct link to Workspace management")

### How can I adjust seats in my workspace?[​](#how-can-i-adjust-seats-in-my-workspace "Direct link to How can I adjust seats in my workspace?")

Only Hex admins can view, add, and manage users. This can be done directly in the Hex workspace settings. See the [workspace settings overview](/docs/administration/workspace_settings/overview) for a step-by-step guide.

### If I remove seats mid-month, will I receive a refund?[​](#if-i-remove-seats-mid-month-will-i-receive-a-refund "Direct link to If I remove seats mid-month, will I receive a refund?")

Removing seats mid-month **does not** result in a refund to your payment method.

Instead, a prorated credit is applied to your next invoice for the unused time remaining in the period that was billed in advance.

* **Self-serve customers:** All seat removals are credited at the prorated amount.
* **Order form customers:** Only uncommitted seats that are removed are credited at the prorated amount.

---

## Payments[​](#payments "Direct link to Payments")

### What payment methods does Hex accept?[​](#what-payment-methods-does-hex-accept "Direct link to What payment methods does Hex accept?")

#### Self-serve customers[​](#self-serve-customers-3 "Direct link to Self-serve customers")

Self-serve subscriptions must be paid by credit card via Stripe. Your card is automatically charged on a recurring subscription basis at the start of each billing cycle.

info

Hex does **not** support ACH or wire transfer payments for self-serve plans.

#### Order form customers[​](#order-form-customers-3 "Direct link to Order form customers")

Order form customers can pay via:

* **Invoice billing** (e.g., Net 30 terms) — Payment terms are defined in your executed order form and reflected on your invoice.
* **ACH / wire transfer** — Bank details (Stripe-managed Wells Fargo virtual accounts) are listed directly on the invoice. Bank details may also be provided by the Hex team if you are paying one of our other bank accounts. Please reach out to [[email protected]](/cdn-cgi/l/email-protection#82e3f0c2eae7faacf6e7e1ea) if you require validation.
* **Credit card** (via Stripe) — Order form customers may also pay by credit card.

### How can I update my payment information?[​](#how-can-i-update-my-payment-information "Direct link to How can I update my payment information?")

To update your payment information, log in to your Hex account with your account email via the [Stripe billing portal](https://billing.stripe.com/p/login/aFa28s3Tz1V0abs3ZQdQQ00).

If you need assistance confirming or updating your account email, please reach out to [[email protected]](/cdn-cgi/l/email-protection#3f5e4d7f575a47114b5a5c57).

### What happens if my credit card payment fails?[​](#what-happens-if-my-credit-card-payment-fails "Direct link to What happens if my credit card payment fails?")

If your credit card payment fails:

1. **We automatically retry the charge** — Stripe will automatically retry the payment using the card on file. Sometimes failures are temporary (e.g., insufficient funds, bank block, expired card).
2. **You may receive an email notification** — If the payment continues to fail, you'll receive an email prompting you to update your payment method.
3. **Update your card** — You can update your card through the [Stripe billing portal](https://billing.stripe.com/p/login/aFa28s3Tz1V0abs3ZQdQQ00). Once updated, the system will automatically retry the charge.
4. **Continued failed payments** — If payment isn't resolved after multiple attempts, your workspace may be restricted or suspended until the outstanding balance is paid.

---

## Invoices and support[​](#invoices-and-support "Direct link to Invoices and support")

### Why does the banking information on my invoice not match what we have in our system?[​](#why-does-the-banking-information-on-my-invoice-not-match-what-we-have-in-our-system "Direct link to Why does the banking information on my invoice not match what we have in our system?")

Hex uses Stripe as our billing platform. Stripe generates a unique Wells Fargo virtual bank account for each order form customer that is secure and ensures payments are routed accurately. This account appears on your invoice and may differ from your records if you were originally onboarded to pay one of Hex's other bank accounts.

Please update your records and remit payment to the Wells Fargo account listed on the invoice. This is our preferred account for payment.

If your finance team needs confirmation or additional documentation, please reach out to [[email protected]](/cdn-cgi/l/email-protection#f39281b39b968bdd8796909b).

### I paid an invoice, but we are receiving emails stating it's outstanding?[​](#i-paid-an-invoice-but-we-are-receiving-emails-stating-its-outstanding "Direct link to I paid an invoice, but we are receiving emails stating it's outstanding?")

If you've already paid an invoice but are still receiving outstanding payment reminders, this is likely due to a misapplication of payment by Stripe.

Occasionally, payments can be applied to the wrong invoice by Stripe, which can trigger automated reminder emails even though payment was received.

Please forward the past due email to [[email protected]](/cdn-cgi/l/email-protection#7d1c0f3d1518055309181e15) and include:

* The invoice number
* Payment date
* Payment amount
* Any remittance confirmation (if available)

### Why is my bill higher this period? Am I being double charged?[​](#why-is-my-bill-higher-this-period-am-i-being-double-charged "Direct link to Why is my bill higher this period? Am I being double charged?")

If your bill is higher this period, it's usually because seat charges are reflected in two ways on your invoice:

1. Billed in advance
2. Billed in arrears

#### Self-serve customers[​](#self-serve-customers-4 "Direct link to Self-serve customers")

Self-serve customers are billed on a monthly basis. This includes charges for seats billed in advance for the upcoming period, as well as any seat changes from the previously billed period.

Because both charges appear on the same invoice, it can sometimes look like you're being double charged. However, they are covering two different time periods:

* The upcoming full month at your updated seat count (advance)
* The past partial month when new seats were added (arrears)

#### Order form customers[​](#order-form-customers-4 "Direct link to Order form customers")

Order form customers are billed annually and upfront for committed seats. These seats are pre-paid for the annual term aligned with the customer's order form. Any overages for uncommitted seats and usage are billed in arrears separately on a basis specified in the signed order form.

### The billing address information on my invoice is incorrect. Who do I reach out to for updates?[​](#the-billing-address-information-on-my-invoice-is-incorrect-who-do-i-reach-out-to-for-updates "Direct link to The billing address information on my invoice is incorrect. Who do I reach out to for updates?")

You can update your billing information by logging into your Hex account with your account email via the [Stripe billing portal](https://billing.stripe.com/p/login/aFa28s3Tz1V0abs3ZQdQQ00).

If you are having issues, please reach out to [[email protected]](/cdn-cgi/l/email-protection#610013210904194f15040209) and include:

* Your Hex workspace URL
* The information you would like updated

#### On this page

* [Billing basics](#billing-basics)
  + [How does Hex's billing structure work?](#how-does-hexs-billing-structure-work)
  + [What does "billed in advance" or "billed in arrears" mean?](#what-does-billed-in-advance-or-billed-in-arrears-mean)
  + [What happens if I adjust seats mid-billing cycle?](#what-happens-if-i-adjust-seats-mid-billing-cycle)
  + [Can you explain how proration works?](#can-you-explain-how-proration-works)
* [Pricing and plans](#pricing-and-plans)
  + [Where can I see Hex's pricing?](#where-can-i-see-hexs-pricing)
  + [Do you offer nonprofit discounts?](#do-you-offer-nonprofit-discounts)
  + [Do you offer student or educational plans?](#do-you-offer-student-or-educational-plans)
* [Workspace management](#workspace-management)
  + [How can I adjust seats in my workspace?](#how-can-i-adjust-seats-in-my-workspace)
  + [If I remove seats mid-month, will I receive a refund?](#if-i-remove-seats-mid-month-will-i-receive-a-refund)
* [Payments](#payments)
  + [What payment methods does Hex accept?](#what-payment-methods-does-hex-accept)
  + [How can I update my payment information?](#how-can-i-update-my-payment-information)
  + [What happens if my credit card payment fails?](#what-happens-if-my-credit-card-payment-fails)
* [Invoices and support](#invoices-and-support)
  + [Why does the banking information on my invoice not match what we have in our system?](#why-does-the-banking-information-on-my-invoice-not-match-what-we-have-in-our-system)
  + [I paid an invoice, but we are receiving emails stating it's outstanding?](#i-paid-an-invoice-but-we-are-receiving-emails-stating-its-outstanding)
  + [Why is my bill higher this period? Am I being double charged?](#why-is-my-bill-higher-this-period-am-i-being-double-charged)
  + [The billing address information on my invoice is incorrect. Who do I reach out to for updates?](#the-billing-address-information-on-my-invoice-is-incorrect-who-do-i-reach-out-to-for-updates)