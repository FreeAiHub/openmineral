# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

The OpenMineral team takes security bugs seriously. We appreciate your efforts to responsibly disclose your findings, and will make every effort to acknowledge your contributions.

To report a security issue, please use the GitHub Security Advisory ["Report a Vulnerability"](https://github.com/openmineral/platform/security/advisories/new) tab.

The OpenMineral team will send a response indicating the next steps in handling your report. After the initial reply to your report, the security team will keep you informed of the progress towards a fix and full announcement, and may ask for additional information or guidance.

### What to include in your report

Please include the following information along with your report:

* Your name and affiliation (if any).
* A description of the technical details of the vulnerabilities. It is very important to let us know how we can reproduce your findings.
* An explanation of who can exploit this vulnerability, and what they gain when doing so -- write an attack scenario. This will help us evaluate your report quickly, especially if the issue is complex.
* Whether this vulnerability is public or known to third parties. If it is, please provide details.

### What to expect

If you submit a report, here's what you can expect:

* Your report will be acknowledged within 2 business days.
* We'll provide a more detailed response within 7 business days indicating the next steps in handling your report.
* We'll work with you to understand and resolve the issue quickly.
* We'll keep you informed about our progress.
* We'll publicly acknowledge your responsible disclosure, if you wish.

## Security Measures

### Authentication & Authorization
- JWT tokens with secure signing algorithms
- Role-based access control (RBAC)
- Multi-factor authentication support
- OAuth 2.0/OpenID Connect integration

### Data Protection
- Encryption at rest for sensitive data
- TLS 1.3 for data in transit
- Secure key management with HashiCorp Vault
- Regular security audits and penetration testing

### Infrastructure Security
- Container image scanning with Trivy
- Kubernetes security policies with OPA Gatekeeper
- Network policies and service mesh (Istio)
- Regular dependency updates and vulnerability scanning

### Compliance
- SOC 2 Type II compliance ready
- GDPR compliance for EU users
- Financial services regulatory compliance
- Regular security training for development team

## Security Contact

For urgent security matters, please contact: security@openmineral.com

For general security questions, please use GitHub Discussions.