variable "iam_role_arn" {
  description = "IAM role ARN for GitHub Actions OIDC"
  type        = string
  sensitive   = true
}

variable "domain_aliases" {
  type    = list(string)
  default = []
}

variable "route53_role_arn" {
  description = "IAM role ARN for cross-account Route 53 access"
  type        = string
  default     = ""
}

variable "route53_zone_id" {
  description = "Route 53 hosted zone ID in the DNS account"
  type        = string
  default     = ""
}