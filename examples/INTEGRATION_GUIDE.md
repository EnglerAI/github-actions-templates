# Integration Guide: Adding Templates to Your Codeitem

This guide explains how to integrate the reusable workflow templates into your Lambda codeitem.

## Two Options for Getting Started

### Option 1: Copy from Example Template (Recommended for New Codeitems)

**Best for:** New codeitems or when you want a clean starting point

1. Copy `examples/lambda-codeitem-workflow.yml` to your codeitem as `.github/workflows/deploy.yml`
2. Replace all placeholders:
   - `YOUR_CODEITEM_NAME` → Your codeitem name
   - `YOUR_STACK_NAME` → Your CloudFormation stack name
   - `YOUR_FUNCTION_NAME` → Your Lambda function name
3. Customize branch names, Python version, and other settings
4. Configure secrets and environments (see below)

**Advantages:**
- ✅ Clean, well-documented starting point
- ✅ All customization points clearly marked
- ✅ No repository-specific code to remove

### Option 2: Copy from github-e2-lambda (Reference Implementation)

**Best for:** When you want to see a working example

1. Copy `.github/workflows/deploy.yml` from `github-e2-lambda` repository
2. Replace repository-specific values:
   - `github-e2-lambda` → Your codeitem name
   - `github-e2-lambda-stack` → Your stack name
   - Branch names if different
3. Customize Python version, scan toggles, and other settings
4. Configure secrets and environments (see below)

**Advantages:**
- ✅ Real, working example
- ✅ Shows actual usage patterns
- ✅ Can see how it's been customized

## Required Setup

### 1. GitHub Repository Secrets

Add these secrets in your repository (Settings → Secrets and variables → Actions):

- `AWS_ROLE_ARN_DEV` - IAM role ARN for dev environment
- `AWS_ACCOUNT_ID_DEV` - AWS account ID for dev environment  
- `AWS_ROLE_ARN_PRD` - IAM role ARN for production environment
- `AWS_ACCOUNT_ID_PRD` - AWS account ID for production environment

**Example:**
```
AWS_ROLE_ARN_DEV=arn:aws:iam::123456789012:role/github-oidc-role
AWS_ACCOUNT_ID_DEV=123456789012
```

### 2. GitHub Environments

Create environments in your repository (Settings → Environments):

- **dev** - For development deployments
- **prd** - For production deployments

**Configuration:**
- Deployment branches: "No restriction" (or configure as needed)
- No protection rules required (unless you want manual approvals)

### 3. Customize Your Workflow

**Key customization points:**

1. **Workflow name** (line 1)
2. **Branch names** (lines 6-7, 10-11)
3. **Environment mapping** (lines 41-52 in setup job)
4. **Stack name** (lines 45, 51)
5. **Python version** (multiple locations)
6. **Function name** (line 160)
7. **AWS region** (line 163)
8. **SAM template path** (line 165)
9. **KMS key alias** (line 168)

## Testing Your Integration

1. **Create a feature branch** and open a PR
   - Should run: verify-docs, quality, security, test
   - Should NOT deploy (deploy_allowed = false)

2. **Merge to env/dev branch**
   - Should run all checks
   - Should upload reports to S3
   - Should deploy to dev environment
   - Should run smoke tests

3. **Merge to main branch**
   - Should run all checks
   - Should deploy to production environment
   - Should run smoke tests

## Troubleshooting

### Workflow Not Triggering
- Check branch names match your trigger patterns
- Verify workflow file is in `.github/workflows/` directory
- Check workflow file syntax (YAML validation)

### AWS Authentication Fails
- Verify IAM OIDC provider is configured in AWS
- Check IAM role trust policy includes your repository
- Ensure `id-token: write` permission is set on jobs

### Jobs Skipping Unexpectedly
- Check that all dependencies in `needs:` are also checked in `if:` conditions
- Verify environment exists and has no restrictions
- Check that secrets are referenced correctly (not passed through outputs)

### Deploy Job Skipping
- Verify `deploy_allowed` output is 'true'
- Check that all prerequisite jobs succeeded or were skipped
- Ensure GitHub Environments (dev/prd) exist
- Check environment deployment branch restrictions

## Next Steps

After integration:
1. Test the full pipeline (PR → dev → main)
2. Customize scan toggles based on your needs
3. Adjust coverage thresholds if needed
4. Add additional environments (qat, stg) if needed

## Support

- See `README.md` for detailed workflow documentation
- See `examples/lambda-codeitem-workflow.yml` for the template
- See `github-e2-lambda/.github/workflows/deploy.yml` for a working example











