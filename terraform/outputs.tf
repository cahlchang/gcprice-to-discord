output "lambda_function_arn" {
  description = "Lambda function ARN"
  value       = aws_lambda_function.gcp_price_to_discord.arn
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.gcp_price_to_discord.function_name
}

output "eventbridge_rule_name" {
  description = "EventBridge rule name"
  value       = aws_cloudwatch_event_rule.daily_schedule.name
}

output "cloudwatch_log_group" {
  description = "CloudWatch Logs group name"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}