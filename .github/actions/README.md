# Reusable Composite Actions

This directory contains reusable composite actions for self-hosted runners. These actions encapsulate common setup and installation patterns to reduce duplication and ensure consistency across workflows.

## Available Actions

### `setup-git-self-hosted`
Configures Git for self-hosted runners with proper HOME directory and safe.directory settings.

**Usage:**
```yaml
- uses: ./.github/actions/setup-git-self-hosted
```

### `setup-python-self-hosted`
Sets up Python and pip for self-hosted runners, handling installation and PATH configuration.

**Inputs:**
- `python_version` (optional): Python version to use (default: '3.12')

**Usage:**
```yaml
- uses: ./.github/actions/setup-python-self-hosted
  with:
    python_version: '3.12'
```

### `setup-pip-environment`
Creates and activates a virtual environment or sets up pip with --user flag to avoid externally-managed-environment errors.

**Outputs:**
- `pip_cmd`: Command to use for pip (e.g., "pip" or "python3 -m pip")
- `pip_flag`: Flag to use with pip (e.g., "" or "--user")

**Usage:**
```yaml
- uses: ./.github/actions/setup-pip-environment
  id: pip_env
- run: ${{ steps.pip_env.outputs.pip_cmd }} install ${{ steps.pip_env.outputs.pip_flag }} package-name
```

### `install-aws-cli`
Installs AWS CLI using pip, AWS CLI v2 installer, or package manager with proper fallbacks.

**Inputs:**
- `install_jq` (optional): Also install jq for JSON parsing (default: 'false')

**Usage:**
```yaml
- uses: ./.github/actions/install-aws-cli
  with:
    install_jq: 'true'
```

### `install-sam-cli`
Installs AWS SAM CLI using pip with --user flag or virtual environment to avoid externally-managed-environment errors.

**Usage:**
```yaml
- uses: ./.github/actions/install-sam-cli
```

### `setup-aws-path`
Ensures AWS CLI and SAM CLI are in PATH for subsequent steps.

**Usage:**
```yaml
- uses: ./.github/actions/setup-aws-path
```

## Environment Variables

All actions expect the `HOME` environment variable to be set to `${{ github.workspace }}/.home` at the job level:

```yaml
jobs:
  my-job:
    runs-on: self-hosted
    env:
      HOME: ${{ github.workspace }}/.home
    steps:
      - uses: ./.github/actions/setup-git-self-hosted
```

## Best Practices

1. Always set `HOME` environment variable at the job level
2. Use `setup-git-self-hosted` before `actions/checkout@v4`
3. Use `setup-python-self-hosted` before any Python-related steps
4. Use `setup-pip-environment` when installing Python packages
5. Use `install-aws-cli` before any AWS CLI commands
6. Use `setup-aws-path` in steps that need AWS CLI/SAM CLI

