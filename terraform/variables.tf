# Variable definitions

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-1"
}

variable "aws_profile" {
  description = "AWS profile name"
  type        = string
  default     = ""
}

variable "environment" {
  description = "Environment identifier (dev, stage, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "gcprice-to-discord"
}

# Lambda function configuration
variable "lambda_function_name" {
  description = "Lambda function name"
  type        = string
  default     = "gcp-billing-to-discord"
}

variable "lambda_role_name" {
  description = "Lambda execution role name"
  type        = string
  default     = "gcp-billing-to-discord-role"
}

variable "lambda_memory_size" {
  description = "Lambda function memory size (MB)"
  type        = number
  default     = 256
}

variable "lambda_timeout" {
  description = "Lambda function timeout (seconds)"
  type        = number
  default     = 30
}

variable "lambda_runtime" {
  description = "Lambda function runtime"
  type        = string
  default     = "python3.9"
}

variable "lambda_log_retention_days" {
  description = "Log retention days"
  type        = number
  default     = 14
}

# EventBridge configuration
variable "eventbridge_rule_name" {
  description = "EventBridge rule name"
  type        = string
  default     = "gcp-billing-monthly-schedule"
}

# Schedule configuration
variable "schedule_expression" {
  description = "Lambda function execution schedule (cron expression)"
  type        = string
  default     = "cron(10 1 * * ? *)" # Daily at 10:10 AM (JST) = UTC 1:10
}

# Logging configuration
variable "log_level" {
  description = "Log level (DEBUG, INFO, WARNING, ERROR)"
  type        = string
  default     = "INFO"
}

# Tag configuration
variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default = {
    Owner       = "DevOps"
    Application = "GCP Billing"
  }
}

# Secret variables (recommended to override in .tfvars)
variable "discord_webhook_url" {
  description = "Discord Webhook URL"
  type        = string
  sensitive   = true
  default     = ""
}

variable "gcp_credentials" {
  description = "GCP credentials (JSON format)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "gcp_credentials_json" {
  description = "GCP credentials (JSON format) - alias"
  type        = string
  sensitive   = true
  default     = ""
}

variable "gcp_billing_account_id" {
  description = "GCP billing account ID"
  type        = string
  sensitive   = true
  default     = ""
}

variable "bigquery_project_id" {
  description = "BigQuery project ID"
  type        = string
  sensitive   = true
  default     = ""
}

variable "bigquery_table_id" {
  description = "BigQuery table ID (project.dataset.table format)"
  type        = string
  sensitive   = true
  default     = ""
}
