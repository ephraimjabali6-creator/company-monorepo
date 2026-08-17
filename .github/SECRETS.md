Secret management guidance

- Use GitHub Secrets for CI secrets. Do NOT store keys in repo.
- For production, use Vault or AWS Secrets Manager and inject secrets at runtime.

Sample GitHub Actions step to read a secret and pass to a job:

steps:
  - name: Deploy step using secret
    env:
      DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
    run: |
      echo "Using secret in deployment"
      # avoid printing secrets; use them only in env or files with restricted perms
