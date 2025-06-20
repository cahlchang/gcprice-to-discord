# GCP Billing to Discord - Troubleshooting Guide

## Issue: No notification at 10:10 JST

### Verified Items

1. **Terraform Configuration**
   - EventBridge rule: `cron(10 1 * * ? *)` (UTC 1:10 = JST 10:10) ✅
   - Lambda function permissions ✅
   - EventBridge to Lambda execution permissions ✅

2. **Lambda Function Operation**
   - Local test successful ✅
   - Discord notifications sent successfully ✅

### Root Cause

**Different AWS accounts being used**
- Terraform deployment target: `XXXXXXXXXXXX`
- Current AWS profile: `XXXXXXXXXXXX`

### Solutions

1. **Verify with correct AWS profile**
   ```bash
   # Check the profile used by Terraform
   cd terraform
   grep -r "profile" *.tf
   
   # Or check terraform.tfvars
   cat terraform.tfvars
   ```

2. **Check CloudWatch Logs**
   ```bash
   # Check logs with correct profile
   aws logs tail /aws/lambda/gcp-billing-to-discord \
     --region ap-northeast-1 \
     --profile [correct-profile-name] \
     --since 24h
   ```

3. **Verify EventBridge Rule Status**
   ```bash
   # Check if EventBridge rule is enabled
   aws events describe-rule \
     --name gcp-billing-monthly-schedule \
     --region ap-northeast-1 \
     --profile [correct-profile-name]
   ```

4. **Manually Execute Lambda Function**
   ```bash
   # Manual execution with test event
   aws lambda invoke \
     --function-name gcp-billing-to-discord \
     --payload '{"use_current_month": true}' \
     --region ap-northeast-1 \
     --profile [correct-profile-name] \
     response.json
   ```

### Additional Checks

1. **Timezone Settings**
   - EventBridge operates in UTC
   - `cron(10 1 * * ? *)` = UTC 01:10 = JST 10:10

2. **Lambda Function Environment Variables**
   - Verify all required environment variables are set
   - Especially check that credentials are correctly configured

3. **EventBridge Execution History**
   ```bash
   # Check execution history via CloudWatch Metrics
   aws cloudwatch get-metric-statistics \
     --namespace AWS/Events \
     --metric-name SuccessfulRuleMatches \
     --dimensions Name=RuleName,Value=gcp-billing-monthly-schedule \
     --start-time $(date -u -v-24H +%Y-%m-%dT%H:%M:%S) \
     --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
     --period 3600 \
     --statistics Sum \
     --region ap-northeast-1 \
     --profile [correct-profile-name]
   ```

### Recommended Next Steps

1. Use correct AWS profile to check CloudWatch Logs
2. Verify EventBridge rule is actually executing
3. Manually execute Lambda function for testing if needed