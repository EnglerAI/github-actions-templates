# Deployment Checklist - Phase 1.5 Templates

## Prerequisites

### 1. Push Templates to GitHub
```bash
cd github-actions-templates
git add .
git commit -m "Phase 1.5: Enhanced templates with quality and security workflows"
git push origin main
```

**Files to push:**
- ✅ `.github/workflows/lambda-deploy.yml` (enhanced)
- ✅ `.github/workflows/quality-checks.yml` (new)
- ✅ `.github/workflows/security-scans.yml` (new)
- ✅ `.github/workflows/code-analyzer.yml` (new)
- ✅ `.github/workflows/verify-docs.yml` (new)
- ✅ `.github/workflows/python-test.yml` (enhanced)
- ✅ `actions/upload-s3-report/action.yml` (new)
- ✅ `README.md` (updated)
- ✅ `CHANGELOG.md` (updated)
- ✅ `PHASE1.5_COMPLETE.md` (new)
- ✅ `examples/lambda-codeitem-workflow.yml` (updated)

### 2. Verify GitHub Access
- [ ] Templates repository is public OR
- [ ] Calling repositories have access to private templates

### 3. Test Repository Ready
- [ ] `github-e2-lambda` workflow refactored
- [ ] Original workflow backed up
- [ ] All secrets configured

## Testing: DEV Environment

### Push to env/dev
```bash
cd github-e2-lambda
git checkout env/dev
git pull origin env/dev
git add .
git commit -m "Test Phase 1.5 templates - refactored workflow"
git push origin env/dev
```

### Monitor Workflow
Watch GitHub Actions UI: `https://github.com/bengler9/github-e2-lambda/actions`

Expected jobs (in parallel):
1. ✅ setup
2. ✅ verify-docs
3. ✅ quality (flake8, mypy, cfn-lint)
4. ✅ security (bandit, checkov, radon)
5. ✅ test (pytest, coverage)
6. ✅ code-analyzer (git archive → S3)
7. ✅ deploy (SAM → Lambda)
8. ✅ smoke-test (function invocation)

### Verify DEV Results

#### Check GitHub Actions
- [ ] All jobs show green checkmarks
- [ ] No unexpected errors in logs
- [ ] Reports generated correctly
- [ ] Artifacts uploaded

#### Check S3 - Reports Bucket
```bash
aws s3 ls s3://cloudbot-reporting-v2/incoming/851725243339/github-e2-lambda/ \
  --profile app002-dev --region us-east-2 --recursive
```

Expected files (13+ reports):
- [ ] flakereport.txt
- [ ] flaketestreport.txt
- [ ] flakedocsreport.txt
- [ ] flakedocstestreport.txt
- [ ] mypy.xml
- [ ] mypycov.xml
- [ ] bandit.xml
- [ ] checkov.xml
- [ ] radon-cc.xml
- [ ] radon-mi.json
- [ ] radon-raw.json
- [ ] report.xml (pytest)
- [ ] coverage.xml

#### Check S3 - Artifacts Bucket
```bash
aws s3 ls s3://cloudbot-codepipeline-artifacts-us-east-2-851725243339/codeitems/851725243339/github-e2-lambda/ \
  --profile app002-dev --region us-east-2
```

Expected file:
- [ ] codeitem-{SHA}.tar.gz

#### Check Lambda - DEV
```bash
# Get function info
aws lambda get-function \
  --function-name github-e2-lambda \
  --profile app002-dev \
  --region us-east-2 \
  --query 'Configuration.{Name:FunctionName,Runtime:Runtime,LastModified:LastModified,Version:Version,State:State}' \
  --output table

# Invoke function
aws lambda invoke \
  --function-name github-e2-lambda \
  --cli-binary-format raw-in-base64-out \
  --payload '{"test": true, "message": "Template validation DEV"}' \
  --profile app002-dev \
  --region us-east-2 \
  response.json

cat response.json | jq .
```

Expected response:
- [ ] `"success": true`
- [ ] `"environment": "dev"`
- [ ] `"timestamp"` present
- [ ] No errors

## Testing: PRD Environment

### Push to main
```bash
cd github-e2-lambda
git checkout main
git merge env/dev
git push origin main
```

### Monitor PRD Workflow
Same jobs as DEV, but with PRD credentials

### Verify PRD Results

#### Check S3 - Reports Bucket (PRD)
```bash
aws s3 ls s3://cloudbot-reporting-v2/incoming/011528258023/github-e2-lambda/ \
  --profile app002-prd --region us-east-2 --recursive
```

Expected: Same 13+ reports as DEV

#### Check S3 - Artifacts Bucket (PRD)
```bash
aws s3 ls s3://cloudbot-codepipeline-artifacts-us-east-2-011528258023/codeitems/011528258023/github-e2-lambda/ \
  --profile app002-prd --region us-east-2
```

Expected: codeitem-{SHA}.tar.gz

#### Check Lambda - PRD
```bash
# Get function info
aws lambda get-function \
  --function-name github-e2-lambda \
  --profile app002-prd \
  --region us-east-2 \
  --query 'Configuration.{Name:FunctionName,Runtime:Runtime,LastModified:LastModified,Version:Version,State:State}' \
  --output table

# Invoke function
aws lambda invoke \
  --function-name github-e2-lambda \
  --cli-binary-format raw-in-base64-out \
  --payload '{"test": true, "message": "Template validation PRD"}' \
  --profile app002-prd \
  --region us-east-2 \
  response.json

cat response.json | jq .
```

Expected response:
- [ ] `"success": true`
- [ ] `"environment": "prd"`  # Note: Should be "prd" not "dev"
- [ ] No errors

## Performance Comparison

| Metric | Original | Template-Based | Change |
|--------|----------|----------------|--------|
| Total execution time | __ min | __ min | __% |
| Setup to deploy | __ min | __ min | __% |
| Number of jobs | 3 | 8 | +167% |
| Lines of workflow code | 439 | 128 | -70% |
| Features included | 3 | 14+ | +367% |
| Reports generated | 0 | 13+ | ∞ |

## Feature Validation

### New Features (Not in Original)
- [ ] ✅ Flake8 linting (4 report types)
- [ ] ✅ Mypy type checking
- [ ] ✅ cfn-lint template validation
- [ ] ✅ Bandit security scanning
- [ ] ✅ Checkov infrastructure security
- [ ] ✅ Radon complexity analysis
- [ ] ✅ Documentation verification
- [ ] ✅ Code analyzer (git archive)
- [ ] ✅ S3 report uploads
- [ ] ✅ Enhanced error handling
- [ ] ✅ S3 permission testing

### Existing Features (Preserved)
- [ ] ✅ pytest testing
- [ ] ✅ Lambda deployment
- [ ] ✅ Smoke testing
- [ ] ✅ Multi-environment routing
- [ ] ✅ OIDC authentication
- [ ] ✅ SAM deployment

## Common Issues & Solutions

### Issue: Workflow not found
**Solution**: Ensure templates pushed to GitHub main branch

### Issue: S3 uploads fail
**Solution**: Check AWS credentials and IAM permissions

### Issue: cfn-lint fails
**Solution**: May find real issues in template.yml - review findings

### Issue: Quality checks fail
**Solution**: Expected if code has linting issues - review and fix or adjust thresholds

### Issue: Code analyzer upload fails
**Solution**: Check artifacts bucket exists and has correct permissions

## Success Declaration

Template refactoring is successful if:

✅ **All jobs execute** (8 jobs in DEV, 8 in PRD)  
✅ **Lambda deploys** (both environments)  
✅ **Smoke tests pass** (both environments)  
✅ **Reports in S3** (13+ reports per environment)  
✅ **Code archives in S3** (both environments)  
✅ **No regressions** (same behavior as original)  
✅ **Performance maintained** (equal or better)

## Post-Success Actions

1. **Update Planning Documents**
   - Mark Phase 1.5 testing as complete
   - Update context-github-actions.md
   - Update PILOT_SUCCESS_SUMMARY.md

2. **Tag Templates as v1.0.0**
   ```bash
   cd github-actions-templates
   git tag -a v1.0.0 -m "Phase 1.5 complete: Enhanced templates with full GitLab CI parity"
   git push origin v1.0.0
   ```

3. **Create Release Notes**
   - Document Phase 1.5 achievements
   - Highlight new features
   - Include migration instructions

4. **Begin Phase 2**
   - Start bulk migration with complete templates
   - Use v1.0.0 release for all migrations
   - Document migration process

## Timeline

- **Day 1**: Push templates + test DEV (1-2 hours)
- **Day 1**: Push to main + test PRD (1 hour)
- **Day 1**: Validation and documentation (1 hour)
- **Day 2**: Tag v1.0.0 and begin Phase 2

**Total**: 1-2 days for complete validation

## Notes

- Keep `deploy-original.yml` as backup for entire pilot phase
- Document any template improvements needed
- Capture metrics for comparison
- Take screenshots of successful runs for documentation

