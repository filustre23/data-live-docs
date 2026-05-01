On this page

# Supplier Security Requirements Addendum

*Last Modified: March 7, 2025*

These Supplier Security Requirements apply to Supplier when it provides Services to Hex. Terms used here but not defined here are defined in the Agreement. These Security Requirements are hereby incorporated by reference and shall be bound by all terms of the Agreement, unless otherwise explicitly set forth herein. These Security Requirements are intended to supplement the Agreement. Where there is a conflict between the provisions of these Security Requirements and the Agreement, the provisions of these Security Requirements shall apply.

## 1. Third-Party Testing and Validation.[​](#1-third-party-testing-and-validation "Direct link to 1. Third-Party Testing and Validation.")

### 1.1. General Testing.[​](#11-general-testing "Direct link to 1.1. General Testing.")

**a. Periodic Tests.** Supplier shall allow Hex, or Hex's delegate, to periodically test the security of the Services. When testing Hex or its delegate shall: (i) carefully conduct tests that are reasonably designed to safely uncover possible vulnerabilities without undue risk; and (ii) make commercially reasonable efforts to tailor the tests as needed to specifically achieve the purpose of the test.

**b. Timing.** Hex or its delegate may conduct the security tests in Section 1.1 at any time during the term of the Agreement. Hex will: (i) provide Supplier with reasonable notice prior to conducting the tests; (ii) promptly inform Supplier of any findings; and (iii) delay further disclosure until Supplier has had reasonable time to resolve issues identified in the findings.

### 1.2. Vulnerability Disclosure Policy.[​](#12-vulnerability-disclosure-policy "Direct link to 1.2. Vulnerability Disclosure Policy.")

**a. Generally.** Supplier shall publish a Vulnerability Disclosure Policy ("VDP") on its public website. This VDP shall: (i) welcome arbitrary security research; (ii) include all internet-facing assets in scope; (iii) provide safe harbor from the Computer Fraud and Abuse Act ("CFAA") and the Digital Millennium Copyright Act ("DMCA") (and any similar or successor legislation) actions for all good faith research; and (iv) permit responsible disclosure of any vulnerability findings, save that any such disclosure does not violate the confidentiality of Supplier's customers' data.

**b. Contact and Service Level Agreement.** Supplier shall: (i) post a method by which the public can contact Supplier to report security vulnerabilities; and (ii) use best efforts to respond to these reported security vulnerabilities within a commercially reasonable period of time based on the severity and impact of the vulnerability.

**c. Bug Bounty Program.** Supplier agrees that Hex may make deliverables or results of the Services subject to Hex's own Bug Bounty Program ("BBP"). Hex will notify Supplier of any material security-related vulnerabilities in the Services or deliverables identified through its BBP. Supplier understands that research and disclosures are governed by Hex's BBP, which requires good faith and responsible behavior by participants.

### 1.3. Application and Network Penetration Testing.[​](#13-application-and-network-penetration-testing "Direct link to 1.3. Application and Network Penetration Testing.")

**a. Annual Testing.** Supplier shall, at least once per year, perform a suite of independent third-party tests. These tests will be performed upon: (i) the Services; (ii) all aspects of Supplier's internet-facing perimeter; and (iii) systems supporting the Services (such as build/release infrastructure). Supplier will supply Hex with full details (not just executive summaries) of all third-party tests from the previous year, including names of third-party testers, number of person hours used, severity of any identified issues, and current remediation status for such issues.

**b. Sharing Results.** Supplier shall, upon Hex's request and under suitable non-disclosure obligations, share with Hex: (i) confirmation that the tests required by this Section 1.3 were performed; and (ii) the third-party tests results from Sections 1.3(a)(i) and (ii) above.

### 1.4. Fixing Issues.[​](#14-fixing-issues "Direct link to 1.4. Fixing Issues.")

Supplier will fix all critical and high severity vulnerabilities that could affect the security of Hex Data, of which Supplier becomes aware, within thirty days of becoming aware of the vulnerability. If Supplier cannot fix the vulnerability within thirty days, Supplier will promptly inform Hex, including all details of the risk to Hex arising from Supplier's inability to fix the vulnerability.

## 2. Technical Security Measures.[​](#2-technical-security-measures "Direct link to 2. Technical Security Measures.")

### 2.1. Transport Encryption.[​](#21-transport-encryption "Direct link to 2.1. Transport Encryption.")

Supplier will maintain an SSL Server Test rating (please see <https://www.ssllabs.com/ssltest/>) of at least "A" for any external website used to store or access Hex Data. If Supplier's rating falls below "A," Supplier will: (a) notify Hex if this rating is below "A" for two months; and (b) have two months from the date it notifies Hex within which to increase its rating back to an "A."

### 2.2. SAML/OIDC Authentication Integration.[​](#22-samloidc-authentication-integration "Direct link to 2.2. SAML/OIDC Authentication Integration.")

If the Services include a SaaS service, Supplier will integrate the Services with SAML 2.0 or OIDC authentication for Hex's user authentication needs. This SAML 2.0 / OIDC authentication integration will be the only method by which Hex users log in to the Services.

### 2.3. Multi-factor Authentication.[​](#23-multi-factor-authentication "Direct link to 2.3. Multi-factor Authentication.")

Supplier will use a multi-factor authentication ("MFA") login solution for the Services, provided that text or phone call are not acceptable factors. MFA must be used for: (a) any VPN connections into the Supplier's internal networks; (b) any connections into Supplier's production environment; (c) Supplier's e-mail, if it can be accessed from the internet; and (d) any services Supplier uses that contain Hex Data.

### 2.4. Patching.[​](#24-patching "Direct link to 2.4. Patching.")

Supplier will promptly apply any high or critical severity security patches to their production servers, endpoints, and endpoint management systems.

### 2.5. Detection and Alerting.[​](#25-detection-and-alerting "Direct link to 2.5. Detection and Alerting.")

Supplier will proactively monitor, detect, and alert its internal security team regarding suspicious or malicious activity within Supplier's production and corporate environments.

### 2.6. Scanning.[​](#26-scanning "Direct link to 2.6. Scanning.")

Supplier will run regular automated scans against their internet-facing perimeter, production perimeter, and internal network. Supplier will promptly fix high and critical severity findings.

### 2.7. Environment Separation and Access.[​](#27-environment-separation-and-access "Direct link to 2.7. Environment Separation and Access.")

Supplier will maintain a boundary between its corporate and production environments. Supplier will maintain controls gating access into the production boundary, and Supplier will only provide production environment access to employees or contractors who maintain the production environment.

### 2.8. Logging.[​](#28-logging "Direct link to 2.8. Logging.")

Supplier will maintain system logs for all systems that access, transmit, or store Hex Data for a minimum of one year. Such logs will uniquely identify individual users and their access to associated systems and identify the attempted or executed activities of such users. All systems creating system logs will be synchronized to a central time source. Supplier will secure system logs in a manner to prevent unauthorized access, modification, and accidental or deliberate destruction. Supplier will make available to Hex (on a set cycle or upon request by Hex) relevant log records concerning Hex's use of the Services for ingestion into Hex's log management and analysis tool in a manner mutually agreed to by both Supplier and Hex.

## 3. Policy and Compliance.[​](#3-policy-and-compliance "Direct link to 3. Policy and Compliance.")

### 3.1. Security Incidents.[​](#31-security-incidents "Direct link to 3.1. Security Incidents.")

**a. Notification and Timing.** Supplier will notify Hex in writing of any Security Incident within twenty-four hours of Supplier becoming aware of the Security Incident. This notification is required even if Supplier has not conclusively established the nature or extent of the Security Incident. Supplier will not communicate with any third-party regarding a Security Incident except as specified by Hex, or as required by law.

**b. Required Information.** Supplier's Security Incident notification will describe the known details of the incident, the status of Supplier's investigation, and, if applicable, the potential number of persons affected. Supplier will be solely responsible for all costs associated with any security breach; which includes, if applicable, for notices to and credit monitoring for affected individuals.

### 3.2. Compliance Certification.[​](#32-compliance-certification "Direct link to 3.2. Compliance Certification.")

Supplier shall: (a) maintain compliance with at least one of the following: (i) SOC 2; (ii) ISO 27001; or (iii) FedRAMP; (b) provide audit reports or evidence of these certifications to Hex upon request; and (c) ensure that all Supplier subcontractors or third-party delegates adhere to the same standards.

### 3.3. Secure Development Lifecycle.[​](#33-secure-development-lifecycle "Direct link to 3.3. Secure Development Lifecycle.")

Supplier shall maintain and follow a Secure Development Lifecycle ("SDL") for the development of its products and services. Supplier's SDL will be supported by at least one full-time security engineer. Supplier will provide Hex a copy of its SDL policy and process documents upon request.

### 3.4. Background Checks.[​](#34-background-checks "Direct link to 3.4. Background Checks.")

Supplier shall maintain processes to determine whether a prospective member of Supplier's workforce is sufficiently trustworthy to work in an environment that contains Supplier information systems and Hex Data. Without limiting the foregoing, Supplier shall have performed criminal background screening on all of its personnel who will render services and/or have access to Hex Data prior to assigning such personnel to provide Services under this Agreement. To the extent permissible under applicable law, such background screening shall at a minimum cover all residences for a seven-year period (for U.S. personnel), or the maximum time period in accordance with local law requirements for non-U.S. personnel.

### 3.5. Anti-Bribery and Corruption.[​](#35-anti-bribery-and-corruption "Direct link to 3.5. Anti-Bribery and Corruption.")

Hex strictly prohibits bribery or other improper payments in connection with its business operations. This prohibition applies to all business activities, anywhere in the world, whether involving public officials or other commercial enterprises. Supplier and its officers, directors, and employees must adhere to the highest standards of business ethical conduct and may not, either directly or indirectly offer or give anything of value to a government official or any other person as an incentive to, or in exchange or as a reward for, obtaining an inappropriate business advantage for Supplier or Hex.

### 3.6. Modern Slavery.[​](#36-modern-slavery "Direct link to 3.6. Modern Slavery.")

Supplier warrants that it actively engages with diverse stakeholders, including industry associations, non-governmental organizations, suppliers, and other companies, to strengthen its efforts to identify, prevent, and address the risk of all forms of modern slavery in its operations and business relationships. The term modern slavery means child labor, forced labor, and human trafficking in any form -- including slave labor, prison labor, indentured servitude, or bonded labor.

### 3.7. Supporting Information.[​](#37-supporting-information "Direct link to 3.7. Supporting Information.")

Upon Hex's request, Supplier will provide its policy and process documents relating to any of the security controls referenced in these Security Requirements to Hex.

### 3.8. Handling of Hex Data.[​](#38-handling-of-hex-data "Direct link to 3.8. Handling of Hex Data.")

Supplier will not move Hex Data from Supplier's production environment unless specifically asked to do so by Hex. Specifically, Hex Data must not be downloaded to phones or laptops, and must not be shared with third parties that are not subcontractors of Supplier. Supplier will delete Hex Data permanently upon Hex's request.

### 3.9. Termination of Agreement.[​](#39-termination-of-agreement "Direct link to 3.9. Termination of Agreement.")

If the Agreement is terminated for any reason, Supplier will, for a period of thirty days from the date of termination, make available a file of Hex Data in an industry standard format for download by Hex.

## 4. Modifications.[​](#4-modifications "Direct link to 4. Modifications.")

Hex may periodically update these Security Requirements by posting a new version at the following URL: <https://learn.hex.tech/docs/legal/supplier-security-addendum>. If Hex changes these Security Requirements in a manner that materially increases Supplier's obligations, Hex will notify Supplier, and Supplier will have thirty days within which to object to the changes. If Supplier does not object within this timeframe, Supplier agrees to comply with the modified Security Requirements. If Supplier objects within this time frame, and Supplier and Hex cannot resolve the objection within thirty days, then Hex may terminate the Agreement immediately upon written notice to Supplier.

## 5. Definitions.[​](#5-definitions "Direct link to 5. Definitions.")

"**Affiliate**" means any entity which controls, is controlled by, or under common control with a party, where "control" means ownership or control, direct or indirect, of fifty percent (50%) or more of such entity's voting capital, and any such entity shall be an Affiliate of such party only as long as such ownership or control exists.

"**Agreement**" means the executed Agreement between Supplier and Hex.

"**Hex**" means Hex Technologies Inc., a Delaware corporation, and its Affiliates.

"**Hex Data**" means any data that is provided to Supplier by Hex or on behalf of Hex.

"**Security Incident**" means any: (i) breach or suspected breach of the security of the Services or the systems used to provide the Services that may have resulted in the compromise of Hex Data; or (ii) other unauthorized access to or use of Hex Data, or Supplier's reasonable belief that access or use may have occurred.

"**Security Requirements**" means this addendum to the Agreement.

"**Services**" means the products or services provided by Supplier to Hex.

"**Suppliers**" means those vendors who provide services to Hex.

#### On this page

* [1. Third-Party Testing and Validation.](#1-third-party-testing-and-validation)
  + [1.1. General Testing.](#11-general-testing)
  + [1.2. Vulnerability Disclosure Policy.](#12-vulnerability-disclosure-policy)
  + [1.3. Application and Network Penetration Testing.](#13-application-and-network-penetration-testing)
  + [1.4. Fixing Issues.](#14-fixing-issues)
* [2. Technical Security Measures.](#2-technical-security-measures)
  + [2.1. Transport Encryption.](#21-transport-encryption)
  + [2.2. SAML/OIDC Authentication Integration.](#22-samloidc-authentication-integration)
  + [2.3. Multi-factor Authentication.](#23-multi-factor-authentication)
  + [2.4. Patching.](#24-patching)
  + [2.5. Detection and Alerting.](#25-detection-and-alerting)
  + [2.6. Scanning.](#26-scanning)
  + [2.7. Environment Separation and Access.](#27-environment-separation-and-access)
  + [2.8. Logging.](#28-logging)
* [3. Policy and Compliance.](#3-policy-and-compliance)
  + [3.1. Security Incidents.](#31-security-incidents)
  + [3.2. Compliance Certification.](#32-compliance-certification)
  + [3.3. Secure Development Lifecycle.](#33-secure-development-lifecycle)
  + [3.4. Background Checks.](#34-background-checks)
  + [3.5. Anti-Bribery and Corruption.](#35-anti-bribery-and-corruption)
  + [3.6. Modern Slavery.](#36-modern-slavery)
  + [3.7. Supporting Information.](#37-supporting-information)
  + [3.8. Handling of Hex Data.](#38-handling-of-hex-data)
  + [3.9. Termination of Agreement.](#39-termination-of-agreement)
* [4. Modifications.](#4-modifications)
* [5. Definitions.](#5-definitions)