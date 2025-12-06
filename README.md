# GitHub Actions Templates

Reusable GitHub Actions workflows for CloudBot codeitems. This repository mirrors the patterns established in `gitlab-ci-templates` for consistent CI/CD across GitLab and GitHub platforms.

## 📁 Repository Structure

```
github-actions-templates/
├── .github/workflows/           # Reusable workflows
│   ├── lambda-deploy.yml        # Lambda function deployment (enhanced)
│   ├── terraform-workflow.yml   # Terraform infrastructure
│   ├── python-test.yml          # Python testing with coverage
│   ├── quality-checks.yml       # Code quality (flake8, mypy, cfn-lint)
│   ├── security-scans.yml       # Security scanning (bandit, checkov, radon)
│   ├── code-analyzer.yml        # Code analysis (git archive → S3)
│   └── verify-docs.yml          # Documentation verification
├── actions/                     # Composite actions
│   ├── setup-aws/               # AWS authentication setup
│   ├── determine-environment/   # Multi-environment routing
│   └── upload-s3-report/        # S3 report uploads
├── examples/                    # Example workflows
│   ├── lambda-codeitem-workflow.yml  # Complete Lambda pipeline
│   └── terraform-codeitem-workflow.yml
└── README.md
```

## 🚀 Quick Start

### Using Reusable Workflows

In your codeitem repository, create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main, "env/**"]
  pull_request:
    branches: [main, "env/**"]

jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      environment: ${{ steps.env.outputs.environment }}
      aws_role: ${{ steps.env.outputs.aws_role }}
    steps:
      - uses: actions/checkout@v4
      - uses: your-org/github-actions-templates/actions/determine-environment@main
        id: env

  deploy:
    needs: setup
    uses: your-org/github-actions-templates/.github/workflows/lambda-deploy.yml@main
    with:
      function_name: my-lambda
      environment: ${{ needs.setup.outputs.environment }}
      aws_region: us-east-2
    secrets:
      aws_role_arn: ${{ needs.setup.outputs.aws_role }}
```

## 📦 Available Workflows

### Lambda Deploy (`lambda-deploy.yml`)

Deploy Lambda functions with SAM, S3 uploads, and smoke testing. Enhanced with pilot learnings.

**Inputs:**

- `function_name` (required): Name of Lambda function
- `stack_name` (optional): CloudFormation stack name (defaults to function_name-stack)
- `environment` (required): Target environment (dev/qat/stg/prd)
- `aws_region` (required): AWS region, default: 'us-east-2'
- `python_version` (optional): Python version, default: '3.12'
- `sam_template` (optional): Path to SAM template, default: 'template.yml'
- `requirements_file` (optional): Path to requirements.txt, default: 'requirements.txt'
- `run_tests` (optional): Run tests before deployment, default: true
- `verify_s3_permissions` (optional): Verify S3 permissions before upload, default: true
- `kms_key_alias` (optional): KMS key alias for S3 encryption, default: 'alias/CloudBotPipelineKey'

**Secrets:**

- `aws_role_arn` (required): AWS IAM role ARN for OIDC
- `aws_account_id` (required): AWS Account ID
- `gitlab_api_token` (optional): GitLab API token for private packages

**Features:**

- ✅ Account verification (prevents account mismatch errors)
- ✅ S3 permission testing before upload
- ✅ KMS-encrypted S3 uploads
- ✅ SAM deployment with proper parameters
- ✅ Smoke testing with function invocation
- ✅ Stack name and function name outputs

### Quality Checks (`quality-checks.yml`)

Code quality checks: flake8 linting, mypy type checking, and CloudFormation template validation.

**Inputs:**

- `python_version` (optional): Python version, default: '3.12'
- `requirements_file` (optional): Path to requirements.txt
- `working_directory` (optional): Working directory, default: '.'
- `run_flake8` (optional): Run flake8 linting, default: true
- `run_mypy` (optional): Run mypy type checking, default: true
- `run_cfn_lint` (optional): Run CloudFormation linting, default: true
- `upload_reports` (optional): Upload reports to S3, default: false
- `account_id` (optional): Account ID for S3 uploads

**Secrets:**

- `gitlab_api_token` (optional): GitLab API token for private packages
- `aws_role_arn` (optional): AWS IAM role ARN for S3 uploads
- `aws_account_id` (optional): AWS Account ID

**Features:**

- ✅ Flake8 with multiple report types (code, tests, docs)
- ✅ Mypy with XML reports and coverage
- ✅ cfn-lint for CloudFormation/SAM templates
- ✅ S3 report uploads (matches GitLab CI pattern)
- ✅ GitHub artifacts for all reports

### Security Scans (`security-scans.yml`)

Security scanning: bandit (Python), checkov (infrastructure), and radon (complexity).

**Inputs:**

- `python_version` (optional): Python version, default: '3.12'
- `requirements_file` (optional): Path to requirements.txt
- `working_directory` (optional): Working directory, default: '.'
- `run_bandit` (optional): Run bandit security scan, default: true
- `run_checkov` (optional): Run checkov infrastructure scan, default: true
- `run_radon` (optional): Run radon complexity analysis, default: false
- `upload_reports` (optional): Upload reports to S3, default: false
- `account_id` (optional): Account ID for S3 uploads

**Secrets:**

- `gitlab_api_token` (optional): GitLab API token for private packages
- `aws_role_arn` (optional): AWS IAM role ARN for S3 uploads
- `aws_account_id` (optional): AWS Account ID

**Features:**

- ✅ Bandit security scanning with XML reports
- ✅ Checkov infrastructure security (same skip-checks as GitLab)
- ✅ Radon complexity analysis (cyclomatic complexity, maintainability index)
- ✅ S3 report uploads for CloudBot integration

### Code Analyzer (`code-analyzer.yml`)

Upload code archives to S3 for CloudBot code analysis (matches GitLab CI pattern).

**Inputs:**

- `account_id` (optional): Account ID for S3 path
- `project_name` (optional): Project name (defaults to repository name)
- `upload_reports` (optional): Upload code archive to S3, default: false
- `aws_region` (optional): AWS region, default: 'us-east-2'
- `kms_key_alias` (optional): KMS key alias, default: 'alias/CloudBotPipelineKey'

**Secrets:**

- `aws_role_arn` (required): AWS IAM role ARN for S3 uploads
- `aws_account_id` (optional): AWS Account ID

**Features:**

- ✅ Git archive creation (tar.gz format)
- ✅ Upload to CloudBot artifacts bucket
- ✅ KMS encryption
- ✅ Matches GitLab CI code analyzer pattern

### Verify Docs (`verify-docs.yml`)

Verify documentation exists and is properly formatted.

**Inputs:**

- `working_directory` (optional): Working directory, default: '.'

**Features:**

- ✅ Checks README.md exists
- ✅ Markdownlint validation
- ✅ Matches GitLab CI verify_docs job

### Python Test (`python-test.yml`)

Python testing with pytest and coverage reporting.

**Note:** Security scanning (bandit) and complexity analysis (radon) are handled by the `security-scans.yml` workflow. Use that workflow for security and complexity checks.

**Inputs:**

- `python_version` (optional): Python version, default: '3.12'
- `requirements_file` (optional): Path to requirements.txt
- `working_directory` (optional): Working directory, default: '.'
- `coverage_threshold` (optional): Minimum coverage percentage, default: 0
- `upload_reports` (optional): Upload reports to S3, default: false
- `account_id` (optional): Account ID for S3 uploads

**Secrets:**

- `gitlab_api_token` (optional): GitLab API token for private packages
- `aws_role_arn` (optional): AWS IAM role ARN for S3 uploads
- `aws_account_id` (optional): AWS Account ID

**Features:**

- ✅ pytest with coverage
- ✅ JUnit XML reports
- ✅ Coverage threshold enforcement
- ✅ S3 uploads for test and coverage reports
- ✅ Codecov integration
- ✅ PR comments with test results

### Terraform Workflow (`terraform-workflow.yml`)

Complete Terraform workflow with validation, planning, and apply.

**Inputs:**

- `terraform_version` (optional): Terraform version, default: '1.12.2'
- `terraform_directory` (optional): Working directory, default: 'terraform'
- `environment` (required): Target environment
- `aws_region` (required): AWS region

**Secrets:**

- `aws_role_arn` (required): AWS IAM role ARN

## 🔐 AWS Authentication (OIDC)

All workflows use OIDC for secure AWS authentication (no long-lived credentials).

### Prerequisites

1. **GitHub OIDC Provider** in AWS IAM
2. **IAM Role** with trust relationship:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:your-org/your-repo:*"
        }
      }
    }
  ]
}
```

### Setup GitHub Secrets

For each environment, create secrets:

- `AWS_ROLE_ARN_DEV`
- `AWS_ROLE_ARN_QAT`
- `AWS_ROLE_ARN_STG`
- `AWS_ROLE_ARN_PRD`

## 🌍 Multi-Environment Pattern

Branch-based environment routing (matches GitLab CI pattern):

| Branch    | Environment | Use Case               |
| --------- | ----------- | ---------------------- |
| `main`    | `prd`       | Production deployments |
| `env/dev` | `dev`       | Development testing    |
| `env/qat` | `qat`       | QA testing             |
| `env/stg` | `stg`       | Staging/pre-production |

The `determine-environment` action automatically routes based on branch.

## 🔧 Composite Actions

### `setup-aws`

Configures AWS credentials using OIDC.

```yaml
- uses: your-org/github-actions-templates/actions/setup-aws@main
  with:
    aws-role-arn: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: us-east-2
```

### `determine-environment`

Determines target environment from branch name.

```yaml
- uses: your-org/github-actions-templates/actions/determine-environment@main
  id: env
# Outputs: environment, aws_role, deploy_allowed, is_production
```

### `upload-s3-report`

Upload report files to CloudBot reporting S3 bucket (matches GitLab CI pattern).

```yaml
- uses: your-org/github-actions-templates/actions/upload-s3-report@main
  with:
    report_file: ./bandit.xml
    report_type: bandit
    account_id: ${{ secrets.AWS_ACCOUNT_ID }}
  secrets:
    aws_role_arn: ${{ secrets.AWS_ROLE_ARN }}
```

## 📊 Migration from GitLab CI

| GitLab CI                | GitHub Actions                     | Notes              |
| ------------------------ | ---------------------------------- | ------------------ |
| `extends: .default-plan` | `uses: .../terraform-workflow.yml` | Reusable workflows |
| `rules:`                 | `if:` conditions                   | Similar logic      |
| `before_script:`         | Composite actions                  | Cleaner pattern    |
| `artifacts:`             | `upload-artifact` action           | Different syntax   |
| `stages:`                | `needs:`                           | More flexible      |

## 🤝 Contributing

When adding new workflows:

1. Follow existing patterns for consistency
2. Use OIDC for AWS authentication
3. Support multi-environment routing
4. Include comprehensive documentation
5. Test in pilot codeitem first

## 📝 Examples

See `examples/` directory for complete codeitem configurations.

## 🐛 Troubleshooting

### OIDC Authentication Fails

- Verify IAM OIDC provider exists in target AWS account
- Check IAM role trust policy includes correct repository
- Ensure `id-token: write` permission in workflow

### Workflow Not Triggering

- Check branch name matches trigger pattern
- Verify `ENABLE_PIPELINE` variable (if used)
- Check workflow file syntax

### Environment Not Detected

- Ensure branch follows naming convention (main, env/dev, etc.)
- Check `determine-environment` action outputs

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [AWS OIDC Setup](https://github.com/aws-actions/configure-aws-credentials)
- [GitLab CI Templates](https://gitlab.com/your-org/gitlab-ci-templates) (reference)

## 🎯 Feature Parity with GitLab CI

| GitLab CI Job              | GitHub Actions Workflow        | Status      |
| -------------------------- | ------------------------------ | ----------- |
| `.default-flake8`          | `quality-checks.yml` (flake8)  | ✅ Complete |
| `.default-mypy`            | `quality-checks.yml` (mypy)    | ✅ Complete |
| `.default-bandit`          | `security-scans.yml` (bandit)  | ✅ Complete |
| `.default-checkov`         | `security-scans.yml` (checkov) | ✅ Complete |
| `.default-radon`           | `security-scans.yml` (radon)   | ✅ Complete |
| `.default-code_analyzer`   | `code-analyzer.yml`            | ✅ Complete |
| `.default-test`            | `python-test.yml`              | ✅ Enhanced |
| `.default-verify_docs`     | `verify-docs.yml`              | ✅ Complete |
| `.default-deploy` (Lambda) | `lambda-deploy.yml`            | ✅ Enhanced |
| `.default-plan`            | `terraform-workflow.yml`       | ✅ Complete |
| `.default-apply`           | `terraform-workflow.yml`       | ✅ Complete |

**All workflows support:**

- ✅ S3 report uploads (matches GitLab pattern)
- ✅ Multi-environment routing
- ✅ OIDC authentication
- ✅ GitLab private package support

## 🎯 Roadmap

- [x] Lambda deployment workflow (enhanced with pilot learnings)
- [x] Quality checks workflow (flake8, mypy, cfn-lint)
- [x] Security scans workflow (bandit, checkov, radon)
- [x] Code analyzer workflow
- [x] Documentation verification
- [x] Enhanced Python testing with S3 uploads
- [x] S3 report upload action
- [ ] Docker build/push workflow
- [ ] Helm deployment workflow
- [ ] Matrix build examples
- [ ] Advanced caching patterns
