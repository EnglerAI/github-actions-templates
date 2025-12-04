# Push Instructions - Phase 1.5 Templates

## Quick Start (Recommended Path)

### Step 1: Push Templates to GitHub
```bash
cd /Users/brianengler/Code/github-repos/github-actions-templates
git status
git add .
git commit -m "Phase 1.5: Enhanced templates with full GitLab CI parity

- Added quality-checks.yml (flake8, mypy, cfn-lint)
- Added security-scans.yml (bandit, checkov, radon)  
- Added code-analyzer.yml (git archive → S3)
- Added verify-docs.yml (markdownlint)
- Enhanced lambda-deploy.yml (pilot learnings applied)
- Enhanced python-test.yml (S3 uploads added)
- Added upload-s3-report action
- Updated examples and documentation
- Ready for testing with github-e2-lambda"

git push origin main
```

### Step 2: Test with github-e2-lambda (DEV)
```bash
cd /Users/brianengler/Code/github-repos/github-e2-lambda
git checkout env/dev
git pull origin env/dev
git add .
git commit -m "Refactor to use github-actions-templates v1.0.0

- Reduced workflow from 439 to 128 lines (-70%)
- Added quality checks (flake8, mypy, cfn-lint)
- Added security scans (bandit, checkov, radon)
- Added code analyzer (git archive → S3)
- Added documentation verification
- Enhanced testing with S3 uploads
- Original workflow backed up as deploy-original.yml"

git push origin env/dev
```

### Step 3: Monitor DEV Deployment
Open GitHub Actions: https://github.com/bengler9/github-e2-lambda/actions

Watch for:
- ✅ 8 jobs execute (setup, verify-docs, quality, security, test, code-analyzer, deploy, smoke-test)
- ✅ All jobs show green checkmarks
- ✅ Lambda deploys successfully
- ✅ Smoke test passes

### Step 4: Verify DEV S3 Uploads
```bash
# Reports bucket
aws s3 ls s3://cloudbot-reporting-v2/incoming/851725243339/github-e2-lambda/ \
  --profile app002-dev --region us-east-2 --recursive | tail -20

# Artifacts bucket  
aws s3 ls s3://cloudbot-codepipeline-artifacts-us-east-2-851725243339/codeitems/ \
  --profile app002-dev --region us-east-2 --recursive | grep github-e2-lambda
```

### Step 5: Test in PRD
```bash
cd /Users/brianengler/Code/github-repos/github-e2-lambda
git checkout main
git merge env/dev
git push origin main
```

### Step 6: Verify PRD S3 Uploads
```bash
# Reports bucket
aws s3 ls s3://cloudbot-reporting-v2/incoming/011528258023/github-e2-lambda/ \
  --profile app002-prd --region us-east-2 --recursive | tail -20

# Artifacts bucket
aws s3 ls s3://cloudbot-codepipeline-artifacts-us-east-2-011528258023/codeitems/ \
  --profile app002-prd --region us-east-2 --recursive | grep github-e2-lambda
```

## What Will Happen

### Templates Push
- Templates become available at `bengler9/github-actions-templates@main`
- Workflows can be referenced by other repositories

### github-e2-lambda DEV Push
GitHub Actions will run:

1. **setup** - Determine environment (env/dev → dev)
2. **verify-docs** - Check README.md exists and validates
3. **quality** - Run flake8 (4 reports), mypy (2 reports), cfn-lint
4. **security** - Run bandit, checkov, radon (6 reports)
5. **test** - Run pytest with coverage (2 reports)
6. **code-analyzer** - Create git archive, upload to S3
7. **deploy** - Package → S3 → SAM deploy → Lambda update
8. **smoke-test** - Invoke Lambda, verify response

**Expected**: ~13+ reports uploaded to S3, Lambda deployed, all green ✅

### github-e2-lambda PRD Push
Same workflow, but:
- Environment = prd
- Uses PRD AWS account
- Deploys to PRD Lambda
- Uploads to PRD S3 buckets

## Files Being Pushed

### github-actions-templates (15+ files)
```
✅ .github/workflows/lambda-deploy.yml
✅ .github/workflows/quality-checks.yml
✅ .github/workflows/security-scans.yml
✅ .github/workflows/code-analyzer.yml
✅ .github/workflows/verify-docs.yml
✅ .github/workflows/python-test.yml
✅ actions/upload-s3-report/action.yml
✅ examples/lambda-codeitem-workflow.yml
✅ README.md
✅ CHANGELOG.md
✅ PHASE1.5_COMPLETE.md
✅ DEPLOYMENT_CHECKLIST.md
✅ READY_TO_TEST.md
✅ PUSH_INSTRUCTIONS.md
```

### github-e2-lambda (4 files)
```
✅ .github/workflows/deploy.yml (refactored - 128 lines)
✅ .github/workflows/deploy-original.yml (backup - 439 lines)
✅ REFACTORED_TO_TEMPLATES.md
✅ TEMPLATE_TESTING_GUIDE.md
```

## Expected Outcomes

### Success Indicators ✅
- All GitHub Actions jobs green
- Lambda deployed to both DEV and PRD
- 13+ reports per environment in S3
- Code archives in S3
- Smoke tests passing
- No errors in logs

### Possible Findings (Not Failures)
- Flake8 may find linting issues (expected)
- cfn-lint may suggest improvements (expected)
- Checkov may flag security notices (expected)
- These are informational, not blocking

## Rollback Plan

If critical issues found:
```bash
cd github-e2-lambda
git checkout env/dev
cp .github/workflows/deploy-original.yml .github/workflows/deploy.yml
git add .github/workflows/deploy.yml
git commit -m "Rollback to original workflow"
git push origin env/dev
```

## After Successful Testing

1. **Document Results**
   - Capture metrics (execution time, reports count)
   - Take screenshots of green workflow runs
   - Note any improvements or issues

2. **Tag Templates v1.0.0**
   ```bash
   cd github-actions-templates
   git tag -a v1.0.0 -m "Phase 1.5 complete: Production-ready templates with full GitLab CI parity

   Features:
   - Quality checks (flake8, mypy, cfn-lint)
   - Security scans (bandit, checkov, radon)
   - Code analyzer (git archive → S3)
   - Documentation verification
   - Enhanced Lambda deployment
   - S3 report uploads
   - Full feature parity with GitLab CI"
   
   git push origin v1.0.0
   ```

3. **Update Planning**
   - Mark Phase 1.5 testing complete
   - Update context-github-actions.md
   - Begin Phase 2 preparation

4. **Proceed to Phase 2**
   - Use v1.0.0 templates for all migrations
   - Start with remaining Lambda codeitems
   - Every migration gets full feature set

## Timeline

- **Push templates**: 5 min
- **Push to env/dev**: 5 min
- **DEV execution + validation**: 15 min
- **Push to main**: 5 min
- **PRD execution + validation**: 15 min
- **Documentation**: 15 min

**Total**: ~1 hour

---

**Ready to proceed!** Follow steps above to test Phase 1.5 enhancements. 🚀

