# AWS OIDC Setup for GitHub Actions

This guide walks through setting up AWS IAM OIDC (OpenID Connect) for secure GitHub Actions authentication.

## 🎯 Why OIDC?

**Benefits over long-lived credentials:**
- ✅ No secrets to manage or rotate
- ✅ Short-lived tokens (1-12 hours)
- ✅ Fine-grained permissions per repository
- ✅ Audit trail in AWS CloudTrail
- ✅ Automatic token refresh by GitHub

## 🏗️ Architecture

```
GitHub Actions Workflow
        ↓
  OIDC Token Request
        ↓
GitHub OIDC Provider (token.actions.githubusercontent.com)
        ↓
  AWS IAM OIDC Provider
        ↓
    IAM Role (Trust Policy checks token)
        ↓
  Temporary AWS Credentials
        ↓
   AWS API Calls
```

## 📝 Setup Steps

### Step 1: Create OIDC Provider (One-Time Per AWS Account)

#### Using AWS CLI:

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1 \
  --tags Key=ManagedBy,Value=CloudBot Key=Purpose,Value=GitHubActions
```

#### Using AWS Console:

1. Go to IAM → Identity providers → Add provider
2. Select **OpenID Connect**
3. **Provider URL**: `https://token.actions.githubusercontent.com`
4. **Audience**: `sts.amazonaws.com`
5. Click **Get thumbprint** (should be: `6938fd4d98bab03faadb97b34396831e3780aea1`)
6. Click **Add provider**

#### Using Terraform:

```hcl
resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com",
  ]

  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1"
  ]

  tags = {
    ManagedBy = "CloudBot"
    Purpose   = "GitHubActions"
  }
}
```

### Step 2: Create IAM Role for Each Repository/Environment

#### Using AWS CLI:

```bash
# Create trust policy file
cat > trust-policy.json << 'EOF'
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
          "token.actions.githubusercontent.com:sub": "repo:YOUR-ORG/YOUR-REPO:*"
        }
      }
    }
  ]
}
EOF

# Replace ACCOUNT_ID, YOUR-ORG, YOUR-REPO
sed -i 's/ACCOUNT_ID/123456789012/g' trust-policy.json
sed -i 's/YOUR-ORG/your-github-org/g' trust-policy.json
sed -i 's/YOUR-REPO/your-repo-name/g' trust-policy.json

# Create role
aws iam create-role \
  --role-name github-actions-lambda-deploy-dev \
  --assume-role-policy-document file://trust-policy.json \
  --description "GitHub Actions role for Lambda deployment (dev)" \
  --tags Key=ManagedBy,Value=CloudBot Key=Environment,Value=dev
```

#### Using Terraform:

```hcl
data "aws_caller_identity" "current" {}

resource "aws_iam_role" "github_actions_lambda_deploy" {
  name = "github-actions-lambda-deploy-${var.environment}"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_org}/${var.github_repo}:*"
          }
        }
      }
    ]
  })

  tags = {
    ManagedBy   = "CloudBot"
    Environment = var.environment
  }
}
```

### Step 3: Attach Permissions Policy

#### Lambda Deployment Permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LambdaDeployment",
      "Effect": "Allow",
      "Action": [
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "lambda:GetFunction",
        "lambda:GetFunctionConfiguration",
        "lambda:PublishVersion",
        "lambda:CreateAlias",
        "lambda:UpdateAlias",
        "lambda:InvokeFunction"
      ],
      "Resource": "arn:aws:lambda:*:*:function:*"
    },
    {
      "Sid": "SAMDeployment",
      "Effect": "Allow",
      "Action": [
        "cloudformation:CreateChangeSet",
        "cloudformation:DescribeChangeSet",
        "cloudformation:ExecuteChangeSet",
        "cloudformation:DescribeStacks",
        "cloudformation:DescribeStackEvents",
        "cloudformation:GetTemplateSummary",
        "cloudformation:ListStackResources"
      ],
      "Resource": "arn:aws:cloudformation:*:*:stack/*"
    },
    {
      "Sid": "S3Access",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::your-artifacts-bucket/*",
        "arn:aws:s3:::your-artifacts-bucket"
      ]
    },
    {
      "Sid": "IAMPassRole",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::*:role/*",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "lambda.amazonaws.com"
        }
      }
    },
    {
      "Sid": "LogsAccess",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups"
      ],
      "Resource": "arn:aws:logs:*:*:log-group:/aws/lambda/*"
    }
  ]
}
```

#### Attach Policy:

```bash
# Create policy file (save above JSON as lambda-deploy-policy.json)

# Create policy
aws iam create-policy \
  --policy-name github-actions-lambda-deploy \
  --policy-document file://lambda-deploy-policy.json

# Attach to role
aws iam attach-role-policy \
  --role-name github-actions-lambda-deploy-dev \
  --policy-arn arn:aws:iam::ACCOUNT_ID:policy/github-actions-lambda-deploy
```

Or use AWS managed policies:

```bash
aws iam attach-role-policy \
  --role-name github-actions-lambda-deploy-dev \
  --policy-arn arn:aws:iam::aws:policy/AWSLambdaFullAccess
```

## 🔐 Trust Policy Details

### Basic Trust Policy (Single Repository)

```json
{
  "StringLike": {
    "token.actions.githubusercontent.com:sub": "repo:myorg/myrepo:*"
  }
}
```

### Restrict to Specific Branch

```json
{
  "StringLike": {
    "token.actions.githubusercontent.com:sub": "repo:myorg/myrepo:ref:refs/heads/main"
  }
}
```

### Allow Multiple Repositories

```json
{
  "StringLike": {
    "token.actions.githubusercontent.com:sub": [
      "repo:myorg/repo1:*",
      "repo:myorg/repo2:*"
    ]
  }
}
```

### Restrict to Environment

```json
{
  "StringLike": {
    "token.actions.githubusercontent.com:sub": "repo:myorg/myrepo:environment:production"
  }
}
```

### Combined Conditions

```json
{
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
  },
  "StringLike": {
    "token.actions.githubusercontent.com:sub": "repo:myorg/myrepo:*"
  },
  "StringEquals": {
    "token.actions.githubusercontent.com:environment": "production"
  }
}
```

## 🧪 Testing OIDC Setup

### Test Workflow

Create `.github/workflows/test-oidc.yml`:

```yaml
name: Test OIDC

on:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT_ID:role/github-actions-lambda-deploy-dev
          aws-region: us-east-2
      
      - name: Verify AWS Identity
        run: |
          echo "=== AWS Identity ==="
          aws sts get-caller-identity
          
          echo "=== Test S3 Access ==="
          aws s3 ls
          
          echo "=== Test Lambda Access ==="
          aws lambda list-functions --max-items 5
```

Run manually from Actions tab and check output.

## 🔍 Troubleshooting

### Error: "Not authorized to perform sts:AssumeRoleWithWebIdentity"

**Causes:**
1. OIDC provider not created
2. Trust policy doesn't match repository
3. Missing `id-token: write` permission

**Solutions:**
```yaml
# Ensure workflow has correct permissions
permissions:
  id-token: write  # REQUIRED for OIDC
  contents: read
```

### Error: "An error occurred (AccessDenied) when calling..."

**Cause:** IAM role lacks required permissions

**Solution:** Attach appropriate policies to role

### Error: "OpenIDConnect provider's HTTPS certificate doesn't match"

**Cause:** Incorrect thumbprint

**Solution:** Use official thumbprint: `6938fd4d98bab03faadb97b34396831e3780aea1`

### Error: "Invalid identity token"

**Causes:**
1. Token expired (unlikely, GitHub handles refresh)
2. Clock skew between GitHub and AWS
3. Corrupted token

**Solution:** Re-run workflow; if persists, recreate OIDC provider

## 📊 Role Naming Convention

Recommended naming pattern:

```
github-actions-{service}-{action}-{environment}

Examples:
- github-actions-lambda-deploy-dev
- github-actions-lambda-deploy-prd
- github-actions-terraform-apply-dev
- github-actions-ecr-push-dev
```

## 🔄 Multi-Account Setup

For organizations with multiple AWS accounts:

```hcl
# In each AWS account (dev, qat, stg, prd)
module "github_oidc" {
  source = "./modules/github-oidc"
  
  github_org   = "your-org"
  repositories = [
    "repo1",
    "repo2"
  ]
  environment = "dev"  # or qat, stg, prd
}
```

## 📝 Validation Checklist

- [ ] OIDC provider created in IAM
- [ ] IAM role created with trust policy
- [ ] Trust policy includes correct repository path
- [ ] Permissions policies attached to role
- [ ] Role ARN saved to GitHub secrets
- [ ] Test workflow runs successfully
- [ ] `id-token: write` permission in workflows
- [ ] Role session duration appropriate (default: 1 hour)

## 🔗 Resources

- [GitHub OIDC Docs](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [AWS IAM OIDC Docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)

## 💡 Best Practices

1. **Least Privilege**: Grant only required permissions
2. **Environment Separation**: Different roles per environment
3. **Audit Regularly**: Review CloudTrail logs
4. **Tag Resources**: Use consistent tagging
5. **Monitor Usage**: Set up CloudWatch alarms
6. **Document Roles**: Maintain role inventory
7. **Test Changes**: Validate in dev first
8. **Use Conditions**: Restrict by branch/environment where possible

