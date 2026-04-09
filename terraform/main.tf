data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_s3_bucket" "resume" {
  bucket           = format("resume-%s-%s-an", data.aws_caller_identity.current.account_id, data.aws_region.current.region)
  bucket_namespace = "account-regional"
  force_destroy    = true
}

data "aws_iam_policy_document" "origin_bucket_policy" {
  statement {
    sid    = "AllowCloudFrontServicePrincipal"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "${aws_s3_bucket.resume.arn}/*"
    ]

    condition {
      test     = "StringLike"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.resume_distribution.arn]
    }
  }
  statement {

    sid    = "GithubUpload"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [var.iam_role_arn]
    }

    actions = [
      "s3:PutObject",
      "s3:PutObjectAcl"
    ]

    resources = [
      "${aws_s3_bucket.resume.arn}/*"
    ]
  }
  statement {
    sid    = "GithubUploadList"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [var.iam_role_arn]
    }

    actions = [
      "s3:ListBucket",
    ]

    resources = [
      "${aws_s3_bucket.resume.arn}"
    ]
  }
}


resource "aws_s3_bucket_policy" "allow_cloudfront_access" {
  bucket = aws_s3_bucket.resume.id
  policy = data.aws_iam_policy_document.origin_bucket_policy.json
}

locals {
  s3_origin_id = "resumebucket"
  my_domain    = "gregoryeberwine.com"
  is_prod      = length(var.domain_aliases) > 0
}

resource "aws_cloudfront_origin_access_control" "default" {
  name                              = "default-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_acm_certificate" "mydomain" {
  count             = local.is_prod ? 1 : 0
  domain_name       = local.my_domain
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_cloudfront_distribution" "resume_distribution" {
  origin {
    domain_name              = aws_s3_bucket.resume.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.default.id
    origin_id                = local.s3_origin_id
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  price_class = "PriceClass_100"

  aliases = var.domain_aliases

  default_cache_behavior {
    cache_policy_id  = "658327ea-f89d-4fab-a63d-7e88639e58f6"
    target_origin_id = local.s3_origin_id
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]

    viewer_protocol_policy = "redirect-to-https"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  viewer_certificate {
    acm_certificate_arn            = local.is_prod ? aws_acm_certificate_validation.mydomain[0].certificate_arn : null
    cloudfront_default_certificate = local.is_prod ? false : true
    ssl_support_method             = local.is_prod ? "sni-only" : null
  }
}

resource "aws_route53_record" "cert_validation" {
  for_each = local.is_prod ? {
    for dvo in aws_acm_certificate.mydomain[0].domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  } : {}

  provider = aws.dns

  zone_id = var.route53_zone_id
  name    = each.value.name
  type    = each.value.type
  ttl     = 300
  records = [each.value.record]
}

resource "aws_acm_certificate_validation" "mydomain" {
  count                   = local.is_prod ? 1 : 0
  certificate_arn         = aws_acm_certificate.mydomain[0].arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}

resource "aws_route53_record" "a" {
  count    = local.is_prod ? 1 : 0
  provider = aws.dns

  zone_id = var.route53_zone_id
  name    = local.my_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.resume_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.resume_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "aaaa" {
  count    = local.is_prod ? 1 : 0
  provider = aws.dns

  zone_id = var.route53_zone_id
  name    = local.my_domain
  type    = "AAAA"

  alias {
    name                   = aws_cloudfront_distribution.resume_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.resume_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}