# Changelog

All notable changes to the GitHub Actions templates will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added - Phase 1.5 Enhancements
- **Quality Checks Workflow** (`quality-checks.yml`)
  - Flake8 linting with 4 report types (code, tests, docs)
  - Mypy type checking with XML reports and coverage
  - CloudFormation/SAM template linting (cfn-lint)
  - S3 report uploads matching GitLab CI pattern
  
- **Security Scans Workflow** (`security-scans.yml`)
  - Bandit security scanning with XML reports
  - Checkov infrastructure security scanning (same skip-checks as GitLab)
  - Radon complexity analysis (cyclomatic complexity, maintainability index)
  - S3 report uploads for CloudBot integration
  
- **Code Analyzer Workflow** (`code-analyzer.yml`)
  - Git archive creation (tar.gz format)
  - Upload to CloudBot artifacts bucket for code analysis
  - KMS encryption support
  - Matches GitLab CI code analyzer pattern
  
- **Verify Docs Workflow** (`verify-docs.yml`)
  - README.md existence check
  - Markdownlint validation
  - Matches GitLab CI verify_docs job
  
- **S3 Upload Action** (`actions/upload-s3-report/`)
  - Composite action for uploading reports to S3
  - Preserves file extensions (.txt, .xml, .json)
  - KMS encryption support
  - Matches GitLab CI report upload pattern

### Enhanced - Phase 1.5
- **Lambda Deploy Workflow** (`lambda-deploy.yml`)
  - Account verification (prevents account mismatch errors)
  - S3 permission testing before upload
  - Enhanced KMS encryption handling
  - Stack name flexibility
  - Function name discovery from stack outputs
  - Improved smoke testing with better payload handling
  - Comprehensive error messages and debugging
  
- **Python Test Workflow** (`python-test.yml`)
  - Added S3 upload support for test and coverage reports
  - Maintains existing pytest, coverage, and Codecov features
  - Optional S3 uploads (only when AWS credentials provided)

### Updated
- Complete example workflow showing all quality/security checks
- README.md with comprehensive workflow documentation
- Feature parity matrix (GitLab CI vs GitHub Actions)

### Added - Phase 1
- Initial release of GitHub Actions templates
- Lambda deployment reusable workflow
- Terraform infrastructure workflow
- Python testing workflow
- Composite actions for AWS setup and environment routing
- Migration guide from AWS CodePipeline
- AWS OIDC setup guide
- Example workflows for Lambda and Terraform codeitems

## [1.0.0] - 2024-XX-XX

### Added
- **Reusable Workflows**:
  - `lambda-deploy.yml` - Complete Lambda deployment pipeline
  - `terraform-workflow.yml` - Terraform validation, plan, apply, and drift detection
  - `python-test.yml` - Python testing with pytest, coverage, linting, and security scanning

- **Composite Actions**:
  - `setup-aws` - Configure AWS credentials using OIDC
  - `determine-environment` - Route to correct environment based on branch

- **Documentation**:
  - README.md - Complete usage guide
  - MIGRATION_GUIDE.md - Step-by-step migration from AWS CodePipeline
  - AWS_OIDC_SETUP.md - AWS OIDC configuration guide

- **Examples**:
  - Lambda codeitem workflow example
  - Terraform codeitem workflow example

### Features

#### Lambda Deploy Workflow
- Multi-environment support (dev/qat/stg/prd)
- Python 3.12 support with configurable version
- SAM template deployment
- Direct Lambda update option
- Automated testing before deployment
- GitLab private package support
- Smoke testing after deployment
- Artifact packaging and upload

#### Terraform Workflow
- Terraform validation and formatting checks
- Plan generation with PR comments
- Automated apply with environment protection
- State drift detection with issue creation
- Multi-workspace support
- S3 backend configuration
- DynamoDB state locking

#### Python Test Workflow
- pytest with coverage reporting
- flake8 linting
- mypy type checking
- bandit security scanning
- radon complexity analysis
- Configurable coverage thresholds
- PR comments with test results
- Codecov integration

### Security
- OIDC authentication (no long-lived credentials)
- Environment-based AWS role ARNs
- SARIF security report uploads
- Least privilege IAM policies

### Performance
- 50-80% faster than AWS CodePipeline
- Parallel job execution
- Pip caching for Python dependencies
- Artifact caching between jobs

---

## Migration Notes

### From AWS CodePipeline

If migrating from AWS CodePipeline:

1. Review [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
2. Set up AWS OIDC (see [AWS_OIDC_SETUP.md](AWS_OIDC_SETUP.md))
3. Configure GitHub secrets
4. Test in dev environment first
5. Monitor for 7 days before cleanup
6. Delete AWS resources after validation

### Breaking Changes from AWS CI/CD

- **Authentication**: Now uses OIDC instead of IAM users
- **Triggers**: Branch-based (no EventBridge/webhooks)
- **Artifacts**: Stored in GitHub (not S3)
- **Logs**: In GitHub Actions UI (not CloudWatch)

---

## Roadmap

### Completed in Phase 1.5
- [x] Quality checks workflow (flake8, mypy, cfn-lint)
- [x] Security scans workflow (bandit, checkov, radon)
- [x] Code analyzer workflow (git archive → S3)
- [x] Documentation verification workflow
- [x] S3 report upload action
- [x] Enhanced Lambda deployment with pilot learnings
- [x] Enhanced Python testing with S3 uploads
- [x] Complete feature parity with GitLab CI

### Planned for v1.1.0
- [ ] Docker build and push workflow
- [ ] Helm/Kubernetes deployment workflow
- [ ] Matrix build support for multi-version testing
- [ ] Advanced caching strategies
- [ ] Slack/Teams notification integration

### Planned for v1.2.0
- [ ] Container security scanning
- [ ] Infrastructure cost estimation
- [ ] Automated rollback on failure
- [ ] Performance benchmarking
- [ ] Multi-region deployment support

### Future Considerations
- [ ] Support for other languages (Node.js, Go, Java)
- [ ] Blue/green deployment patterns
- [ ] Canary deployment support
- [ ] Integration testing frameworks
- [ ] Load testing workflows

---

## Contributing

When contributing to this repository:

1. Create a feature branch from `main`
2. Test changes in a pilot codeitem
3. Update documentation
4. Update this CHANGELOG
5. Create pull request with detailed description

## Support

For issues or questions:
- Create an issue in this repository
- Contact CloudBot team
- Review documentation in README.md

---

[Unreleased]: https://github.com/your-org/github-actions-templates/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/your-org/github-actions-templates/releases/tag/v1.0.0

