# Cloud Resume Challenge — Frontend

The frontend for my [Cloud Resume Challenge](https://cloudresumechallenge.dev/) project. A static resume site hosted on AWS, deployed and managed with Terraform and GitHub Actions.

**Live site:** [gregoryeberwine.com](https://gregoryeberwine.com)
**Backend repo:** [resume-backend](https://github.com/gregoryeberwine/resume-backend)

## Architecture

![Cloud Resume Challenge Architecture](architecture-diagram.png)

## Stack

- **S3** — Static site hosting (HTML/CSS)
- **CloudFront** — CDN with TLS certificate
- **Route 53** — DNS (custom domain)
- **OAC** — Origin Access Control to keep the S3 bucket private
- **Terraform** — Infrastructure as code for all AWS resources
- **GitHub Actions** — CI/CD pipeline (OIDC auth, Terraform apply, S3 deploy, CloudFront cache invalidation)
- **Playwright** — End-to-end tests (page title, email link, visitor counter, performance checks)

## CI/CD Pipeline

On push to `main`, the GitHub Actions workflow:

1. Runs tests against a local web server
2. Authenticates to AWS via OIDC (no stored credentials)
3. Runs `terraform apply` to ensure infrastructure is current
4. Syncs site files to S3
5. Invalidates the CloudFront cache
6. Runs tests against the live web page

## Repo Structure

```
├── .github/workflows/   # GitHub Actions CI/CD
├── site/                 # HTML, CSS
├── terraform/            # Infrastructure as code
├── tests/                # Playwright test suite
└── requirements.txt
```
