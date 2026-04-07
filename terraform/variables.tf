variable "iam_role_arn" {
  description = "IAM role ARN for GitHub Actions OIDC"
  type        = string
  sensitive   = true
}