On this page

# Hex Security Addendum

*Last Modified: June 17, 2025*

This Hex Security Addendum ("**Addendum**") is incorporated into and made a part of under one or more separate agreement(s) executed between Hex Technologies Inc. ("**Hex**") and Customer covering Customer's use of the Services (each an "**Agreement**").

## 1. Purpose[​](#1-purpose "Direct link to 1. Purpose")

This Addendum describes Hex's security program, security certifications, and technical and organizational security controls (together, the "**Information Security Program**") to protect (a) Customer Data from unauthorized use, access, disclosure, or theft and (b) the Services. As security threats change, Hex continues to update the Information Security Program and strategy to help protect Customer Data and the Services. As such, Hex reserves the right to update this Addendum from time to time; provided, however, any update will not materially reduce the overall protections set forth in this Addendum. The then-current terms of this Addendum are available at <https://learn.hex.tech/docs/legal/security-addendum>. This Addendum does not apply to any Services that are identified as alpha, beta, not generally available, limited release, developer preview, or any similar Services offered by Hex.

## 2. Definitions[​](#2-definitions "Direct link to 2. Definitions")

Capitalized terms used in this Addendum without a definition will have the meanings given to them in the Agreement.

Solely for the purposes of this Addendum and the Information Security Program, Hex defines "**Customer Data**" as data or information originated by Customer that Customer submits or provides in the course of using the Services. For the avoidance of doubt, Customer Data does not include Aggregated Statistics.

## 3. Security Organization and Program[​](#3-security-organization-and-program "Direct link to 3. Security Organization and Program")

Hex maintains a risk-based assessment security program. The framework for the Information Security Program includes administrative, organizational, technical, and physical safeguards reasonably designed to protect the Services and confidentiality, integrity, and availability of Customer Data. The Information Security Program is intended to be appropriate to the nature of the Services and the size and complexity of Hex's business operations. Hex has a separate and dedicated Information Security team that manages the Information Security Program. Hex's security framework is aligned to established information security industry standards, including SOC 2. Security is managed at the highest levels of the company, with Hex's Head of Security & IT meeting with executive management regularly to discuss issues and coordinate company-wide security initiatives. Information security policies and standards are reviewed and approved by management at least annually and are made available to all Hex employees for their reference.

## 4. Confidentiality[​](#4-confidentiality "Direct link to 4. Confidentiality")

Hex has controls in place to maintain the confidentiality of Customer Data in accordance with the Agreement. All Hex employees and contract personnel are bound by Hex's internal policies regarding maintaining the confidentiality of Customer Data and are contractually obligated to comply with these obligations.

## 5. People Security[​](#5-people-security "Direct link to 5. People Security")

### 5.1 Employee Background Checks[​](#51-employee-background-checks "Direct link to 5.1 Employee Background Checks")

Hex performs criminal background checks on all new employees at the time of hire in accordance with applicable local laws. Additionally, depending on the nature and scope of a new employee's role, Hex may also conduct additional checks, including verifying a new employee's education and previous employment and performing reference checks.

### 5.2 Employee Training[​](#52-employee-training "Direct link to 5.2 Employee Training")

At the time of hire and at least once (1) per year, Hex employees must complete a security and privacy awareness training which covers Hex's security policies, security best practices, and privacy principles. Employees on a leave of absence may have additional time to complete this annual training. Hex's dedicated security team also performs phishing awareness campaigns and communicates emerging threats to employees. Hex has also established an anonymous method for employees to report any unethical behavior where anonymous reporting is legally permitted.

## 6. Third-Party Vendor Management[​](#6-third-party-vendor-management "Direct link to 6. Third-Party Vendor Management")

### 6.1 Vendor Assessment[​](#61-vendor-assessment "Direct link to 6.1 Vendor Assessment")

Hex may use third-party vendors to provide the Services. Hex carries out a security risk-based assessment of prospective vendors before working with them to validate they meet Hex's security requirements. Hex periodically reviews each vendor in light of Hex's security and business continuity standards, including the type of access and classification of data being accessed (if any), controls necessary to protect data, and legal or regulatory requirements. Hex ensures that Customer Data is returned and/or deleted at the end of a vendor relationship.

### 6.2 Vendor Agreements[​](#62-vendor-agreements "Direct link to 6.2 Vendor Agreements")

Hex enters into written agreements with all of its vendors which include confidentiality, privacy, and security obligations that provide an appropriate level of protection for Customer Data that these vendors may process.

## 7. Security Certifications and Attestations[​](#7-security-certifications-and-attestations "Direct link to 7. Security Certifications and Attestations")

Hex holds the following security-related certifications and attestations:

* HIPAA Security and Breach Notification Rules
* PCI DSS (as a Service Provider)
* SOC 2 Type II (Trust Service Criteria: Security, Confidentiality, Availability)

At least annually, Hex will engage with an independent assessor to conduct a compliance assessment and provide a full certification, attestation, review, or report. The results of such assessments are available (under appropriate non-disclosure obligations) to Customers at <https://trust.hex.tech/>. To the extent Hex decides to discontinue a certification or attestation, Hex will adopt or maintain an equivalent, industry-recognized framework.

## 8. Hosting Architecture and Data Segregation[​](#8-hosting-architecture-and-data-segregation "Direct link to 8. Hosting Architecture and Data Segregation")

### 8.1 Amazon Web Services[​](#81-amazon-web-services "Direct link to 8.1 Amazon Web Services")

The Services are hosted on Amazon Web Services ("**AWS**") and protected by the security and environmental controls of AWS. The production environment within AWS where the Services and Customer Data are hosted are logically isolated in a Virtual Private Cloud (VPC). Customer Data stored within AWS is encrypted at all times. AWS does not have access to unencrypted Customer Data. More information about AWS security is available at <https://aws.amazon.com/security/> and <https://aws.amazon.com/compliance/shared-responsibility-model/>. For AWS compliance audits and reports, please see <https://aws.amazon.com/compliance/>.

### 8.2 Services[​](#82-services "Direct link to 8.2 Services")

For the Services, all network access between production hosts is restricted, using access control lists to allow only authorized services to interact in the production network. Access control lists are in use to manage network segregation between different security zones in the production and corporate environments. Access control lists are reviewed regularly. Hex separates Customer Data using logical identifiers. Customer Data is tagged with a unique customer identifier that is assigned to segregate Customer Data ownership. The Services are designed and built to identify and allow authorized access only to and from Customer Data identified with customer-specific tags. These controls prevent other customers from having access to Customer Data.

## 9. Physical Security[​](#9-physical-security "Direct link to 9. Physical Security")

AWS is strictly controlled both at the perimeter and at building ingress points by professional security staff utilizing video surveillance, intrusion detection systems, and other electronic means. Authorized staff must pass two-factor authentication (2FA) a minimum of two (2) times to access data center floors. All visitors and contractors are required to present identification and are signed in and continually escorted by authorized staff. These facilities are designed to withstand adverse weather and other reasonably predictable natural conditions. Each data center has redundant electrical power systems that are available twenty-four (24) hours a day, seven (7) days a week. Uninterruptible power supplies and on-site generators are available to provide back-up power in the event of an electrical failure. More information about AWS data center security is available at <https://aws.amazon.com/compliance/data-center/controls/>.

In addition, Hex headquarters and office spaces have a physical security program that manages visitors, building entrances, closed circuit televisions, and overall office security.

## 10. Security by Design[​](#10-security-by-design "Direct link to 10. Security by Design")

Hex follows security by design principles when it designs the Services. Hex also applies the Hex Secure Software Development Lifecycle ("**Secure SDLC**") standard to perform numerous security-related activities for the Services across different phases of the product creation lifecycle from requirements gathering and product design all the way through product deployment. These activities include, but are not limited to, the performance of (a) internal security reviews before deploying new Services or code; (b) penetration testing by independent third-parties; and/or (c) threat models for new Services to detect potential security threats and vulnerabilities.

## 11. Access Controls[​](#11-access-controls "Direct link to 11. Access Controls")

### 11.1 Provisioning Access[​](#111-provisioning-access "Direct link to 11.1 Provisioning Access")

To minimize the risk of data exposure, Hex follows the principles of least privilege through a team-based-access-control model when provisioning system access. Hex personnel are authorized to access Customer Data based on their job function, role, and responsibilities. Access rights to production environments that are not time-based are reviewed at least quarterly. An employee's access to Customer Data is promptly removed upon termination of their employment. In order to access the production environment, an authorized user must have unique credentials with multi-factor authentication enabled. Before an engineer is granted access to the production environment, access must be approved by management. Hex logs high risk actions and changes in the production environment. Hex leverages automation to identify any deviation from internal technical standards that could indicate anomalous/unauthorized activity to raise an alert within minutes of a configuration change.

### 11.2 Password Controls[​](#112-password-controls "Direct link to 11.2 Password Controls")

Hex's current policy for employee password management follows the NIST SP 800-63B guidance, and as such, Hex's policy focuses on high entropy by using longer passwords, with multi-factor authentication, and does not require special characters or frequent changes. When a customer logs into their account, Hex hashes the credential of the user before it is stored. A customer may also utilize social authentication or federated authentication, as applicable to their subscription. Any vendor default credentials are promptly modified by Hex.

## 12. Change Management[​](#12-change-management "Direct link to 12. Change Management")

Hex has a formal change management process it follows to administer changes to the production environment for the Services, including any changes to its underlying software, applications, and systems. Each change is reviewed and evaluated in a test environment before being deployed into the production environment for the Services. All changes, including the evaluation of the changes in a test environment, are documented using a formal, auditable system of record. A rigorous assessment is carried out for all high-risk changes to evaluate their impact on the overall security of the Services. Deployment approval for high-risk changes is required from the correct organizational stakeholders. Plans and procedures are also implemented for high-risk changes in the event a deployed change needs to be rolled back to preserve the security of the Services.

## 13. Configuration Management[​](#13-configuration-management "Direct link to 13. Configuration Management")

Hex establishes secure baseline configurations for the system(s) of the Services that access or store Customer Data according to the principle of least functionality.

## 14. Encryption[​](#14-encryption "Direct link to 14. Encryption")

For the Services, (a) the databases that store Customer Data are encrypted using the Advanced Encryption Standard (AES) with at least 256-bits and (b) Customer Data is encrypted when in transit between Customer's software application and the Services using TLS v1.2 or higher.

## 15. Vulnerability & Patch Management[​](#15-vulnerability--patch-management "Direct link to 15. Vulnerability & Patch Management")

Hex maintains controls and policies to mitigate the risk of security vulnerabilities in a measurable time frame that balances risk and the business/operational requirements. Hex uses a third-party tool to conduct vulnerability scans regularly to assess vulnerabilities in Hex's cloud infrastructure and corporate systems. Critical software patches are evaluated, tested, and applied proactively.

## 16. Penetration Testing[​](#16-penetration-testing "Direct link to 16. Penetration Testing")

Hex performs penetration tests and engages independent third-party entities to conduct application and network-level penetration tests on at least an annual basis. Security threats and vulnerabilities that are detected are prioritized, triaged, and remediated promptly. Results of application-level penetration tests are publicized at <https://trust.hex.tech/>. Hex maintains a bug bounty program, which allows independent security researchers to report security threats and vulnerabilities on an ongoing basis.

## 17. Security Incident Management[​](#17-security-incident-management "Direct link to 17. Security Incident Management")

Hex maintains security incident management policies and procedures in accordance with NIST SP 800-61. Hex's Incident Response Team assesses all relevant security threats and vulnerabilities and establishes appropriate remediation and mitigation actions. Hex retains security logs for a minimum of one (1) year. Access to these security logs is limited to authorized personnel. Security logs are secured in a manner to prevent unauthorized access, modification, and accidental or deliberate destruction. Hex utilizes third-party tools to detect, mitigate, and prevent Distributed Denial of Service (DDoS) attacks.

## 18. Discovery, Investigation, and Notification of a Security Incident[​](#18-discovery-investigation-and-notification-of-a-security-incident "Direct link to 18. Discovery, Investigation, and Notification of a Security Incident")

Hex will promptly investigate a Security Incident upon discovery. To the extent permitted by applicable law, Hex will notify Customer of a Security Incident in accordance with the Data Protection Addendum. Security Incident notifications will be provided to Customer via email to the email address(es) designated by Customer in its account. Such notifications will include a brief summary of the available facts and the status of Hex's investigation.

## 19. Resilience and Service Continuity[​](#19-resilience-and-service-continuity "Direct link to 19. Resilience and Service Continuity")

### 19.1 Resilience[​](#191-resilience "Direct link to 19.1 Resilience")

The hosting infrastructure for the Services (a) spans multiple fault-independent availability zones in geographic regions physically separated from one another and (b) is able to detect and route around issues experienced by hosts or even whole data centers in real time and employ orchestration tooling that has the ability to regenerate hosts, building them from the latest backup.

### 19.2 Service Continuity[​](#192-service-continuity "Direct link to 19.2 Service Continuity")

Hex also leverages specialized tools available within the hosting infrastructure for the Services to monitor server performance, data, and traffic load capacity within each availability zone and colocation data center. If suboptimal server performance or overloaded capacity is detected on a server within an availability zone or colocation data center, these specialized tools increase the capacity or shift traffic to relieve any suboptimal server performance or capacity overload. Hex is also promptly notified in the event of any suboptimal server performance or overloaded capacity.

## 20. Backups and Recovery[​](#20-backups-and-recovery "Direct link to 20. Backups and Recovery")

### 20.1 Customer Data Backups[​](#201-customer-data-backups "Direct link to 20.1 Customer Data Backups")

Hex performs regular backups of Customer Data, which is hosted on AWS's data center infrastructure. Customer Data that is backed up is retained redundantly across multiple availability zones and/or regions and encrypted in transit and at rest. Such backups are tested and validated for correctness and completeness at least annually.

### 20.2 Disaster Recovery[​](#202-disaster-recovery "Direct link to 20.2 Disaster Recovery")

Hex maintains, regularly tests (no less than annually), and provides appropriate training for a contingency plan covering the Services.

#### On this page

* [1. Purpose](#1-purpose)
* [2. Definitions](#2-definitions)
* [3. Security Organization and Program](#3-security-organization-and-program)
* [4. Confidentiality](#4-confidentiality)
* [5. People Security](#5-people-security)
  + [5.1 Employee Background Checks](#51-employee-background-checks)
  + [5.2 Employee Training](#52-employee-training)
* [6. Third-Party Vendor Management](#6-third-party-vendor-management)
  + [6.1 Vendor Assessment](#61-vendor-assessment)
  + [6.2 Vendor Agreements](#62-vendor-agreements)
* [7. Security Certifications and Attestations](#7-security-certifications-and-attestations)
* [8. Hosting Architecture and Data Segregation](#8-hosting-architecture-and-data-segregation)
  + [8.1 Amazon Web Services](#81-amazon-web-services)
  + [8.2 Services](#82-services)
* [9. Physical Security](#9-physical-security)
* [10. Security by Design](#10-security-by-design)
* [11. Access Controls](#11-access-controls)
  + [11.1 Provisioning Access](#111-provisioning-access)
  + [11.2 Password Controls](#112-password-controls)
* [12. Change Management](#12-change-management)
* [13. Configuration Management](#13-configuration-management)
* [14. Encryption](#14-encryption)
* [15. Vulnerability & Patch Management](#15-vulnerability--patch-management)
* [16. Penetration Testing](#16-penetration-testing)
* [17. Security Incident Management](#17-security-incident-management)
* [18. Discovery, Investigation, and Notification of a Security Incident](#18-discovery-investigation-and-notification-of-a-security-incident)
* [19. Resilience and Service Continuity](#19-resilience-and-service-continuity)
  + [19.1 Resilience](#191-resilience)
  + [19.2 Service Continuity](#192-service-continuity)
* [20. Backups and Recovery](#20-backups-and-recovery)
  + [20.1 Customer Data Backups](#201-customer-data-backups)
  + [20.2 Disaster Recovery](#202-disaster-recovery)