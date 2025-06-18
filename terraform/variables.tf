# 変数定義

variable "aws_region" {
  description = "AWSリージョン"
  type        = string
  default     = "ap-northeast-1"
}

variable "environment" {
  description = "環境識別子（dev, stage, prod）"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "プロジェクト名"
  type        = string
  default     = "gcprice-to-discord"
}

# Lambda関数設定
variable "lambda_function_name" {
  description = "Lambda関数名"
  type        = string
  default     = "gcp-billing-to-discord"
}

variable "lambda_role_name" {
  description = "Lambda実行ロール名"
  type        = string
  default     = "gcp-billing-to-discord-role"
}

variable "lambda_memory_size" {
  description = "Lambda関数のメモリサイズ (MB)"
  type        = number
  default     = 256
}

variable "lambda_timeout" {
  description = "Lambda関数のタイムアウト時間 (秒)"
  type        = number
  default     = 30
}

variable "lambda_runtime" {
  description = "Lambda関数のランタイム"
  type        = string
  default     = "python3.9"
}

variable "lambda_log_retention_days" {
  description = "ログ保持日数"
  type        = number
  default     = 14
}

# EventBridge設定
variable "eventbridge_rule_name" {
  description = "EventBridgeルール名"
  type        = string
  default     = "gcp-billing-monthly-schedule"
}

# スケジュール設定
variable "schedule_expression" {
  description = "Lambda関数実行スケジュール (cron式)"
  type        = string
  default     = "cron(10 1 * * ? *)" # 毎日午前10:10(JST) = UTC 1:10
}

# ロギング設定
variable "log_level" {
  description = "ログレベル (DEBUG, INFO, WARNING, ERROR)"
  type        = string
  default     = "INFO"
}

# タグ設定
variable "tags" {
  description = "リソースに付与するタグ"
  type        = map(string)
  default = {
    Owner       = "DevOps"
    Application = "GCP Billing"
  }
}

# シークレット変数（.tfvarsで上書き推奨）
variable "discord_webhook_url" {
  description = "Discord Webhook URL"
  type        = string
  sensitive   = true
  default     = ""
}

variable "gcp_credentials" {
  description = "GCP認証情報 (JSON形式)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "gcp_credentials_json" {
  description = "GCP認証情報 (JSON形式) - 別名"
  type        = string
  sensitive   = true
  default     = ""
}

variable "gcp_billing_account_id" {
  description = "GCPの請求先アカウントID"
  type        = string
  sensitive   = true
  default     = ""
}

variable "bigquery_project_id" {
  description = "BigQueryプロジェクトID"
  type        = string
  sensitive   = true
  default     = ""
}

variable "bigquery_table_id" {
  description = "BigQueryテーブルID (project.dataset.table形式)"
  type        = string
  sensitive   = true
  default     = ""
}
