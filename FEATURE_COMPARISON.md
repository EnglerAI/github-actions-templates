# Feature Comparison: GitLab CI vs GitHub Actions Templates

This document compares the features available in GitLab CI templates vs GitHub Actions templates to identify gaps.

## Feature Parity Status

### ✅ Fully Implemented in Both

| Feature                | GitLab CI                            | GitHub Actions                          | Status |
| ---------------------- | ------------------------------------ | --------------------------------------- | ------ |
| **Quality Checks**     |
| Flake8 linting         | `.default-flake8`                    | `quality-checks.yml` (flake8)           | ✅     |
| Mypy type checking     | `.default-mypy`                      | `quality-checks.yml` (mypy)             | ✅     |
| CloudFormation linting | N/A                                  | `quality-checks.yml` (cfn-lint)         | ✅     |
| Terraform linting      | `.default-tf_lint`                   | `terraform-workflow.yml` (fmt/validate) | ✅     |
| **Security Scans**     |
| Bandit security scan   | `.default-bandit`                    | `security-scans.yml` (bandit)           | ✅     |
| Checkov IaC scan       | `.default-checkov`                   | `security-scans.yml` (checkov)          | ✅     |
| Radon complexity       | `.default-radon`                     | `security-scans.yml` (radon)            | ✅     |
| **Testing**            |
| Python tests (pytest)  | `.default-test`                      | `python-test.yml`                       | ✅     |
| **Documentation**      |
| Verify docs            | `.default-verify_docs`               | `verify-docs.yml`                       | ✅     |
| **Code Analysis**      |
| Code archive to S3     | `.default-code_analyzer`             | `code-analyzer.yml`                     | ✅     |
| **Deployment**         |
| Lambda deployment      | `.default-deploy`                    | `lambda-deploy.yml`                     | ✅     |
| Terraform plan/apply   | `.default-plan`, `.default-apply`    | `terraform-workflow.yml`                | ✅     |
| **Versioning & Releases** |
| Auto-tagging           | `.default-auto_tag`                  | `auto-tag-release.yml`                  | ✅     |
| Auto-release           | `.default-auto_tag`                  | `auto-tag-release.yml`                  | ✅     |
| **Branch Management**  |
| Reset env branches     | `.default-reset_env_branches`        | `reset-env-branches.yml`                | ✅     |
| **Build & Push**       |
| Build and push Docker  | `.default-build_and_push`            | `docker-build-push.yml`                 | ✅     |

### ❌ Missing in GitHub Actions

| Feature                       | GitLab CI                        | GitHub Actions | Priority  | Notes                            |
| ----------------------------- | -------------------------------- | -------------- | --------- | -------------------------------- |
| **Infrastructure Management** |
| Detect drift                  | `.default-detect_drift`          | ❌ Missing     | 🟡 Medium | Terraform state drift detection  |
| Verify infrastructure         | `.default-verify_infrastructure` | ❌ Missing     | 🟡 Medium | Post-deploy verification         |
| **Vue.js Specific**           |
| Vue lint                      | `.default-vue_lint`              | ❌ Missing     | 🟢 Low    | Vue.js specific                  |
| Vue test                      | `.default-vue_test`              | ❌ Missing     | 🟢 Low    | Vue.js specific                  |
| Vue build                     | `.default-vue_build`             | ❌ Missing     | 🟢 Low    | Vue.js specific                  |
| Vue deploy                    | `.default-vue_deploy`            | ❌ Missing     | 🟢 Low    | Vue.js specific                  |

## Implemented: Auto-Tagging & Auto-Release

**GitLab:** `.default-auto_tag` — SemVer tags + GitLab Release on push to `main`.

**GitHub:** `auto-tag-release.yml` reusable workflow — same SemVer rules and GitHub Releases.

Versioning:

- `main` → patch bump (`v1.2.3` → `v1.2.4`)
- Commit message overrides: `INCREASE MINOR VERSION`, `INCREASE MAJOR VERSION`
- Branch-based suffixes retained for non-main callers (`env/dev` → `-beta`, etc.)
- Release notes prefer recently merged PR body; fall back to commit message

Call after successful deploy on `main` (see `template-inf-mod-cmp-tf-simple` deploy.yml).

## Implemented: Branch Reset

**GitLab:** `.default-reset_env_branches`

**GitHub:** `reset-env-branches.yml` — resets `env/dev` from `main` after production deploy.

## Remaining Feature Gaps

### 1. Infrastructure Drift Detection (🟡 MEDIUM PRIORITY)

**GitLab Implementation:**

- `.default-detect_drift` job
- Compares Terraform state with actual infrastructure
- Creates issues when drift detected

**GitHub Equivalent Needed:**

- Add drift detection job to `terraform-workflow.yml`
- Use GitHub Issues API to create issues
- Run on schedule or manual trigger

**Impact:** Medium - Useful for infrastructure codeitems but not critical for Lambda functions.

### 2. Infrastructure Verification (🟡 MEDIUM PRIORITY)

**GitLab Implementation:**

- `.default-verify_infrastructure` job
- Post-deployment verification checks
- Multiple variants for different infrastructure types

**GitHub Equivalent Needed:**

- Add verification step to `terraform-workflow.yml` or `lambda-deploy.yml`
- Customizable verification scripts

**Impact:** Medium - Good practice but can be added later.

### 3. Vue.js Specific Jobs (🟢 LOW PRIORITY)

**GitLab:** `.default-vue_lint`, `.default-vue_test`, `.default-vue_build`, `.default-vue_deploy`

**GitHub:** Still missing dedicated Vue reusable workflows (partial coverage may exist via other deploy workflows).

## Recommendation

Current templates cover core CI/CD (quality, security, testing, deployment, auto-tag/release, env branch reset, Docker build/push). Remaining gaps are medium/low priority and can be added incrementally.

## Implementation Priority

1. **Done:** Integrate current templates; auto-tag-release; reset-env-branches; docker-build-push
2. **As needed:** Drift detection, infrastructure verification, Vue-specific workflows

## Notes

- Most Lambda codeitems don't need Docker build/push
- Most codeitems don't need infrastructure drift detection
- Auto-tagging/release is how Terraform modules are published for `git::...?ref=vX.Y.Z` consumption (no GitHub Packages Terraform format)
- Branch reset keeps environment branches in sync with main after production deploy
- Can always add features later without breaking existing workflows
