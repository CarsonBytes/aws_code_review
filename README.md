# AWS Security Demo Repository

This repository demonstrates **automated AI-powered code review (Amazon Q Developer)** and **security scanning (Amazon Inspector)** triggered automatically during pull requests.

## Real-World Example

This demo is based on the real PR [CarsonBytes/aws_code_review#5](https://github.com/CarsonBytes/aws_code_review/pull/5) which shows:

1. **Amazon Inspector** bot scanning for security vulnerabilities
2. **Amazon Q Developer** bot providing code review with security recommendations
3. Both tools automatically commenting on PR changes
4. Security issues blocking merge until remediated

### What Happened in the Real PR

When the PR was opened, both bots automatically reviewed the code:

**Amazon Inspector Bot:**
- Scanned CloudFormation template for security issues
- Found missing `AssumeRolePolicyDocument` property (High severity)
- Left inline comments on vulnerable resources

**Amazon Q Developer Bot:**
- Performed comprehensive security review
- Found 3 critical issues:
  1. IAM role with `AdministratorAccess` (violates least privilege)
  2. Vulnerable `requests` library version 2.25.1 with known CVEs
  3. Missing input validation in `order_logic` function
- Provided specific suggested fixes for each issue
- Blocked merge until issues are addressed

## How It Works

### PR Trigger Flow

```
Developer creates PR
         ↓
GitHub Actions workflow activates
         ↓
    ┌────┴────┐
    ↓         ↓
Q Developer  Amazon Inspector
Code Review  Security Scan
    ↓         ↓
  Results → PR Status
```

### Q Developer (demo1_q_developer)
- **Triggered**: On PR creation/modification
- **Purpose**: AI-powered code quality and security review
- **Checks**: Code patterns, best practices, potential bugs, security vulnerabilities
- **Location**: `demo1_q_developer/` - Simple order manager demonstrating code review
- **Features**:
  - Natural language code suggestions (`/q` command)
  - CWE-linked security recommendations
  - Suggested code fixes

### Amazon Inspector (demo2_pr_inspector)
- **Triggered**: Via GitHub Actions workflow on PR
- **Purpose**: Automated security vulnerability scanning
- **Checks**: Security issues in code and infrastructure
- **Location**: `demo2_pr_inspector/` - Application + CloudFormation template with security issues
- **Features**:
  - Severity classification (Critical, High, Medium, Low)
  - PR blocking on critical/high findings
  - Detailed vulnerability reports

## Repository Structure

```
aws_demo2/
├── demo1_q_developer/          # Q Developer demo - code review example
│   ├── order_manager.py        # Sample code for AI review
│   ├── test_order_manager.py   # Tests
│   └── requirements.txt
│
├── demo2_pr_inspector/         # Inspector demo - security scan example
│   ├── order_logic.py          # App with security vulnerabilities
│   ├── template.yaml           # CloudFormation with security issues
│   ├── test_vulnerabilities.py # Vulnerability tests
│   └── requirements.txt
│
└── .github/workflows/
    └── inspector-pr-scan.yml   # GitHub Actions workflow
```

## CI/CD Workflow (.github/workflows/inspector-pr-scan.yml)

The workflow runs on every PR to `main` or `master`:

```yaml
on:
  pull_request:
    branches: [main, master]
```

### Steps:
1. **Checkout code** - Gets PR code
2. **Configure AWS Credentials** - Uses GitHub Secrets
3. **Run Amazon Inspector Scan** - Scans repository for vulnerabilities
4. **Check Results** - Blocks merge if Critical/High findings exist

### PR Status Outcomes:
- ✅ **No critical/high vulnerabilities** → PR can merge
- ❌ **Critical or High vulnerabilities found** → PR blocked

## Demo Applications

### demo1_q_developer - Code Quality Demo
Simple Python application showing code patterns Q Developer reviews:
- Order management logic
- Mock database
- Payment gateway integration
- **Intentional**: Hardcoded API key for demonstration

### demo2_pr_inspector - Security Vulnerability Demo
Contains multiple vulnerability types for Inspector to detect:

**Application (order_logic.py):**
- Command injection
- Insecure pickle deserialization
- Hardcoded AWS credentials
- SQL injection
- Path traversal
- Weak MD5 encryption

**Infrastructure (template.yaml):**
- IAM role with AdministratorAccess
- Public S3 bucket
- Open security group (all traffic)
- KMS key with wildcard policy
- Lambda with excessive permissions

## Real PR Review Comments (from CarsonBytes/aws_code_review#5)

### Amazon Inspector Bot Comment
```
⏳ I'm reviewing this pull request for security vulnerabilities and code quality issues.
✅ I finished the code review, and left comments with the issues I found.
```

### Amazon Q Developer Bot Comment
```
## Security Review Summary

This PR introduces critical security vulnerabilities that must be addressed before merge:

### Critical Issues Found:

1. IAM Overprivileged Role: The CloudFormation template grants AdministratorAccess,
   violating least privilege principles and creating significant security risks

2. Vulnerable Dependency: The requests library version 2.25.1 contains known CVEs

3. Missing Input Validation: The order_logic function lacks input validation

### Action Required:

Please address all security findings before this PR can be approved.
```

### Suggested Fix for IAM Issue
```yaml
# Before (VULNERABLE)
ManagedPolicyArns:
  - arn:aws:iam::aws:policy/AdministratorAccess

# After (FIXED)
ManagedPolicyArns:
  - arn:aws:iam::aws:policy/ReadOnlyAccess
```

### Suggested Fix for Input Validation
```python
# Before (VULNERABLE)
def update_delivery_date(order_id, new_date):
    return {"status": "updated", "new_date": new_date}

# After (FIXED)
def update_delivery_date(order_id, new_date):
    if not order_id or not new_date:
        raise ValueError("Invalid input parameters")
    return {"status": "updated", "new_date": new_date}
```

## Setup

### Required GitHub Secrets
Add these to your repository settings:

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | AWS region (default: us-east-1) |

### Running Locally

```bash
# Install dependencies
cd demo2_pr_inspector
pip install -r requirements.txt

# Run vulnerability tests
python test_vulnerabilities.py
```

## Learning Points

1. **Q Developer** provides AI-powered code review automatically on every PR
2. **Amazon Inspector** scans for security vulnerabilities in PRs
3. **Automated blocking** prevents insecure code from reaching production
4. **Natural language suggestions** (`/q` command) let developers fix issues quickly
5. **CWE-linked recommendations** provide context and remediation guidance
6. **Both tools work together** for comprehensive security coverage

## Related Resources

- [Original PR Example](https://github.com/CarsonBytes/aws_code_review/pull/5)
- [Amazon Inspector Documentation](https://docs.aws.amazon.com/inspector/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Database](https://cwe.mitre.org/)
