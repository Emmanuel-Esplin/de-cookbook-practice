# Security Policy

## Reporting a Vulnerability

Do not report vulnerabilities by publishing exploit details or sensitive information in a public issue. Use GitHub's private vulnerability reporting for this repository when available. Include the affected path, impact, and steps to reproduce, while avoiding real credentials or personal data.

## Sensitive Data

- Never commit passwords, tokens, private keys, cloud credentials, or `.env` files.
- Do not publish personal, payment-card, customer, or otherwise restricted data. Use synthetic records for examples.
- Keep input datasets, generated output, local notebooks, and notebook cell output out of public commits unless they have been reviewed for privacy, licensing, and necessity.
- Store local secrets outside the repository or inject them through environment variables. Use placeholders in examples and configuration templates.
- If a secret is exposed, revoke or rotate it immediately. Removing it in a later commit does not remove it from Git history; history cleanup and provider-side secret handling are also required.

The `.gitignore` rules are a convenience, not a security boundary. Review staged changes and scan the complete history before publishing.