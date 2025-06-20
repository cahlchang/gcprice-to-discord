# Create Lambda deployment package
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda_function"
  output_path = "${path.module}/dist/lambda_function.zip"
}

# Lambda function
resource "aws_lambda_function" "gcp_price_to_discord" {
  function_name = var.lambda_function_name
  filename      = data.archive_file.lambda_zip.output_path
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.lambda_handler"
  runtime       = var.lambda_runtime
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  environment {
    variables = {
      DISCORD_WEBHOOK_URL    = var.discord_webhook_url
      GCP_CREDENTIALS        = var.gcp_credentials_json
      GCP_BILLING_ACCOUNT_ID = var.gcp_billing_account_id
      BIGQUERY_PROJECT_ID    = var.bigquery_project_id
      BIGQUERY_TABLE_ID      = var.bigquery_table_id
      LOG_LEVEL              = var.log_level
    }
  }

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  tags = var.tags
}

# CloudWatch Logs group
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = var.lambda_log_retention_days

  tags = var.tags
}

# EventBridge rule (daily execution)
resource "aws_cloudwatch_event_rule" "daily_schedule" {
  name                = var.eventbridge_rule_name
  description         = "Daily GCP cost information retrieval schedule"
  schedule_expression = var.schedule_expression

  tags = var.tags
}

# EventBridge target (Lambda function)
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_schedule.name
  target_id = "InvokeLambda"
  arn       = aws_lambda_function.gcp_price_to_discord.arn

  # Set parameters to retrieve current month's progress
  input = jsonencode({
    use_current_month = true
  })
}
