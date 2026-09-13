# GitHub Actions Templates — Pack Taxonomy (parity with GitLab)

This mirrors the three-layer model in
[`gitlab-ci-templates/docs/ARCHITECTURE.md`](../../gitlab-repos/gitlab-ci-templates/docs/ARCHITECTURE.md).

## Mapping

| GitLab pack / fragment | GitHub Actions equivalent |
|------------------------|---------------------------|
| `fragments/before_scripts.yml` (AWS env) | `actions/setup-aws`, `actions/determine-environment` |
| `fragments/workflow-*.yml` | `on:` blocks in consumer `deploy.yml` / examples |
| `jobs/terraform.yml` | `terraform-workflow.yml`, INF `*-tf-deploy.yml` |
| `jobs/python.yml` | `python-test.yml`, `quality-checks.yml`, `security-scans.yml` |
| `jobs/cloudformation.yml` | `cloudformation-deploy.yml`, INF `*-cf-deploy.yml` |
| `jobs/lambda.yml` | `lambda-deploy.yml`, `lambda-layer-deploy.yml`, `tul-cli-*-deploy.yml` |
| `jobs/vue.yml` | `vue-*-deploy.yml`, `vue-static-deploy.yml` |
| `jobs/k8s.yml` | `docker-build-push.yml`, `helm-eks-deploy.yml`, `svc-api-*-deploy.yml` |
| `jobs/docs.yml` | `verify-docs.yml` |
| `jobs/ops.yml` | `code-analyzer.yml`, `reset-env-branches.yml`, `auto-tag-release.yml` |
| `templates/.gitlab-ci-*.yml` | Consumer `deploy.yml` + `examples/*-codeitem-workflow.yml` |

## Versioning parity

- Pin reusable workflow `uses:` to a semver tag (e.g. `@v1.0.0`), not `@main`.
- Keep workflow/action names aligned with GitLab type abbreviations (`inf-sto-obj`, `svc-api`, `vue-spa`, …).

## Adding a type/language

1. Add reusable workflow(s) under `.github/workflows/`.
2. Add composite action under `actions/` only if setup is shared.
3. Add `examples/<type>-codeitem-workflow.yml`.
4. Mirror the same type in `gitlab-ci-templates` type composers + packs.
