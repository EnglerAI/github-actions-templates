# Migration Guide: AWS CodePipeline → GitHub Actions

This guide helps you migrate Lambda codeitems from GitHub + AWS CI/CD (CodePipeline) to GitHub Actions.

## 📋 Prerequisites

Before starting migration:

1. **AWS OIDC Setup**: Configure GitHub OIDC provider in each AWS account
2. **Repository Secrets**: Configure AWS role ARNs in GitHub secrets
3. **Test Environment**: Have a dev/test environment to validate migration

## 🎯 Migration Benefits

| Metric | Before (CodePipeline) | After (GitHub Actions) |
|--------|----------------------|------------------------|
| **Startup Time** | 30-60 seconds | 5-10 seconds |
| **Total Deploy Time** | 2-5 minutes | 30-90 seconds |
| **Cost** | ~$30/month | $0-10/month |
| **Complexity** | 4+ AWS services | 1 config file |

## 🔧 AWS OIDC Setup (One-Time Per Account)

### Step 1: Create OIDC Provider in IAM

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

### Step 2: Create IAM Role with Trust Policy

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

### Step 3: Attach Required Policies

Attach policies needed for Lambda deployment:
- `AWSLambdaFullAccess` (or custom policy)
- `IAMReadOnlyAccess`
- `AmazonS3ReadOnlyAccess` (for SAM templates)

## 📝 Migration Steps

### Step 1: Create GitHub Workflow File

Create `.github/workflows/deploy.yml` in your repository:

```yaml
name: Deploy Lambda

on:
  push:
    branches: [main, 'env/**']
  pull_request:
    branches: [main, 'env/**']

jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      environment: ${{ steps.env.outputs.environment }}
      aws_role: ${{ steps.env.outputs.aws_role }}
      deploy_allowed: ${{ steps.env.outputs.deploy_allowed }}
    steps:
      - uses: actions/checkout@v4
      - id: env
        run: |
          case "${{ github.ref_name }}" in
            main)
              echo "environment=prd" >> $GITHUB_OUTPUT
              echo "aws_role=${{ secrets.AWS_ROLE_ARN_PRD }}" >> $GITHUB_OUTPUT
              echo "deploy_allowed=true" >> $GITHUB_OUTPUT
              ;;
            env/dev)
              echo "environment=dev" >> $GITHUB_OUTPUT
              echo "aws_role=${{ secrets.AWS_ROLE_ARN_DEV }}" >> $GITHUB_OUTPUT
              echo "deploy_allowed=true" >> $GITHUB_OUTPUT
              ;;
            # Add other environments...
          esac

  deploy:
    needs: setup
    if: needs.setup.outputs.deploy_allowed == 'true'
    uses: your-org/github-actions-templates/.github/workflows/lambda-deploy.yml@main
    with:
      function_name: your-lambda-name
      environment: ${{ needs.setup.outputs.environment }}
      aws_region: us-east-2
      python_version: '3.12'
      use_sam: true
    secrets:
      aws_role_arn: ${{ needs.setup.outputs.aws_role }}
      aws_account_id: ${{ secrets.AWS_ACCOUNT_ID }}
```

### Step 2: Configure GitHub Secrets

Add these secrets to your repository (Settings → Secrets and variables → Actions):

**Required:**
- `AWS_ROLE_ARN_DEV` - IAM role ARN for dev environment
- `AWS_ROLE_ARN_QAT` - IAM role ARN for QAT environment  
- `AWS_ROLE_ARN_STG` - IAM role ARN for staging environment
- `AWS_ROLE_ARN_PRD` - IAM role ARN for production environment
- `AWS_ACCOUNT_ID` - AWS account ID

**Optional:**
- `GITLAB_API_TOKEN` - If using private GitLab packages

### Step 3: Configure GitHub Environments (Optional but Recommended)

Create environments for protection rules:

1. Go to Settings → Environments
2. Create environments: `dev`, `qat`, `stg`, `prd`
3. For `prd` environment:
   - Add required reviewers
   - Add deployment branch rules (only `main`)
   - Add protection rules

### Step 4: Test in Dev Environment

1. **Create test branch**: `git checkout -b test-github-actions`
2. **Commit workflow**: `git add .github/workflows/deploy.yml && git commit -m "Add GitHub Actions workflow"`
3. **Push**: `git push origin test-github-actions`
4. **Create PR to env/dev**
5. **Verify**: Check Actions tab for workflow run
6. **Merge to env/dev**: Deploy should trigger automatically
7. **Validate**: Check Lambda function updated correctly

### Step 5: Migrate Production

Once validated in dev:

1. **Create PR to main**
2. **Review workflow run** (validation only, no deploy)
3. **Merge to main**
4. **Monitor deployment** in Actions tab
5. **Verify production** Lambda function

### Step 6: Clean Up AWS Resources (After 30 Days)

After confirming GitHub Actions works:

1. **Delete CodePipeline**:
   ```bash
   aws codepipeline delete-pipeline --name your-pipeline-name
   ```

2. **Delete CodeBuild Project**:
   ```bash
   aws codebuild delete-project --name your-project-name
   ```

3. **Delete EventBridge Rule**:
   ```bash
   aws events delete-rule --name your-rule-name
   aws events remove-targets --rule your-rule-name --ids "1"
   ```

4. **Delete S3 Artifacts** (after backup):
   ```bash
   aws s3 rm s3://your-artifacts-bucket --recursive
   aws s3 rb s3://your-artifacts-bucket
   ```

## 🔍 Comparison: Before & After

### Before: AWS CodePipeline Setup

**Files Needed:**
- `template.yml` - SAM template
- `buildspec.yml` - CodeBuild configuration
- CloudFormation stack for CodePipeline
- EventBridge rule for triggers

**AWS Resources:**
- CodePipeline pipeline
- CodeBuild project
- S3 bucket for artifacts
- EventBridge rule
- IAM roles (3-4 different roles)

### After: GitHub Actions

**Files Needed:**
- `.github/workflows/deploy.yml` - Workflow configuration
- `template.yml` - SAM template (unchanged)

**AWS Resources:**
- OIDC provider (one per account)
- IAM role (one per environment)

## 🐛 Troubleshooting

### OIDC Authentication Fails

**Error**: `Error: Could not assume role with OIDC`

**Solutions:**
1. Verify OIDC provider exists:
   ```bash
   aws iam list-open-id-connect-providers
   ```

2. Check IAM role trust policy includes correct repository:
   ```json
   "token.actions.githubusercontent.com:sub": "repo:YOUR-ORG/YOUR-REPO:*"
   ```

3. Ensure workflow has `id-token: write` permission:
   ```yaml
   permissions:
     id-token: write
     contents: read
   ```

### Workflow Not Triggering

**Solutions:**
1. Check branch name matches trigger:
   ```yaml
   on:
     push:
       branches: [main, 'env/**']
   ```

2. Verify workflow file is in `.github/workflows/` directory
3. Check workflow syntax with GitHub's workflow validator

### Lambda Update Fails

**Error**: `Function not found`

**Solutions:**
1. Verify function name format: `function-name-environment`
2. Check function exists in AWS:
   ```bash
   aws lambda get-function --function-name your-function-dev
   ```
3. Use SAM deployment if function doesn't exist:
   ```yaml
   with:
     use_sam: true
   ```

### GitLab Private Package Access Fails

**Error**: `Could not find a version that satisfies the requirement`

**Solutions:**
1. Add `GITLAB_API_TOKEN` to repository secrets
2. Ensure token has `read_api` scope
3. Verify package project ID in workflow (71621175)

## 📊 Validation Checklist

Use this checklist for each migrated codeitem:

- [ ] AWS OIDC provider configured
- [ ] IAM roles created with correct trust policies
- [ ] GitHub secrets configured
- [ ] Workflow file created
- [ ] GitHub environments configured (optional)
- [ ] Tested in dev environment
- [ ] Deployed to production successfully
- [ ] Verified Lambda function works correctly
- [ ] Monitored for 7 days
- [ ] AWS CodePipeline resources scheduled for deletion
- [ ] CloudBot metadata updated

## 🎓 Learning Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [AWS OIDC Setup](https://github.com/aws-actions/configure-aws-credentials)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [SAM CLI Reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference.html)

## 💬 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review GitHub Actions logs in the Actions tab
3. Check AWS CloudWatch logs for Lambda errors
4. Review this migration guide
5. Contact the CloudBot team for assistance

## 🎯 Next Steps After Migration

1. **Add Advanced Features**:
   - Matrix builds for multi-version testing
   - Caching for faster builds
   - PR comments with deployment status

2. **Optimize Performance**:
   - Use workflow caching
   - Optimize Lambda package size
   - Use Lambda layers

3. **Enhance Security**:
   - Enable Dependabot
   - Add security scanning
   - Use environment secrets

4. **Monitor & Improve**:
   - Track deployment metrics
   - Set up alerting
   - Optimize workflow runs

