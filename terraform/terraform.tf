terraform {
  backend "s3" {
    key    = "frontend/terraform.tfstate"
    region = "us-east-1"
    use_lockfile = true
    encrypt = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.37.0"
    }
  }

  required_version = "~> 1.14.8"
}

provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "dns"
  region = "us-east-1"
  dynamic "assume_role" {
    for_each = var.route53_role_arn != "" ? [1] : []
    content {
      role_arn = var.route53_role_arn
    }
  }
}