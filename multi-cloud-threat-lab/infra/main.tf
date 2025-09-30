terraform {
  required_providers {
    aws = { source = "hashicorp/aws" }
    random = { source = "hashicorp/random" }
  }
  required_version = ">= 1.2"
}

provider "aws" {
  region = var.aws_region
  # If you want to use named profile, set AWS_PROFILE env var before running terraform
}

variable "aws_region" { default = "us-east-1" }

resource "random_id" "rand" {
  byte_length = 4
}

resource "aws_s3_bucket" "trail_bucket" {
  bucket        = "mctlab-cloudtrail-logs-${random_id.rand.hex}"
  force_destroy = true
  acl           = "private"
  tags = {
    Name = "mctlab-cloudtrail-logs"
  }
}

resource "aws_cloudwatch_log_group" "ct_log_group" {
  name              = "/aws/cloudtrail/mctlab"
  retention_in_days = 14
  tags = { Name = "mctlab-cloudtrail-loggroup" }
}

resource "aws_iam_role" "cloudtrail_cwl_role" {
  name = "mctlab-cloudtrail-cwl-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "cloudtrail.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "cloudtrail_cwl_policy" {
  role = aws_iam_role.cloudtrail_cwl_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:PutLogEvents",
          "logs:CreateLogStream",
          "logs:CreateLogGroup",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams"
        ],
        Resource = "${aws_cloudwatch_log_group.ct_log_group.arn}:*"
      }
    ]
  })
}

resource "aws_cloudtrail" "mct_trail" {
  name                          = "mctlab-trail"
  s3_bucket_name                = aws_s3_bucket.trail_bucket.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = false

  cloud_watch_logs_role_arn  = aws_iam_role.cloudtrail_cwl_role.arn
  cloud_watch_logs_group_arn = aws_cloudwatch_log_group.ct_log_group.arn
}

# IAM role for our Lambdas (detector & playbook & ingest)
resource "aws_iam_role" "lambda_exec_role" {
  name = "mctlab-lambda-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "lambda.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

# Attach AWSLambdaBasicExecutionRole managed policy for CloudWatch logs
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Inline policy to allow required actions (EC2 stop, IAM update access key, invoke lambda, S3 read/write)
resource "aws_iam_role_policy" "lambda_extra_policy" {
  role = aws_iam_role.lambda_exec_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ec2:StopInstances",
          "ec2:DescribeInstances",
          "ec2:DescribeNetworkInterfaces"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "iam:UpdateAccessKey",
          "iam:ListAccessKeys",
          "iam:GetUser",
          "iam:ListUsers"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "lambda:InvokeFunction"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = ["${aws_s3_bucket.trail_bucket.arn}/*", aws_s3_bucket.trail_bucket.arn]
      }
    ]
  })
}

output "trail_s3_bucket" {
  value = aws_s3_bucket.trail_bucket.id
}

output "cloudwatch_log_group" {
  value = aws_cloudwatch_log_group.ct_log_group.name
}

output "lambda_exec_role_arn" {
  value = aws_iam_role.lambda_exec_role.arn
}
