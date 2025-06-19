# GCP Billing to Discord - トラブルシューティング

## 問題: 10:10 JST に通知が来ない

### 確認済み事項

1. **Terraform設定**
   - EventBridgeルール: `cron(10 1 * * ? *)` (UTC 1:10 = JST 10:10) ✅
   - Lambda関数の権限設定 ✅
   - EventBridgeからLambdaへの実行権限 ✅

2. **Lambda関数の動作**
   - ローカルテストは成功 ✅
   - Discord通知も正常に送信される ✅

### 問題の原因

**異なるAWSアカウントが使用されている**
- Terraformデプロイ先: `XXXXXXXXXXXX`
- 現在のAWSプロファイル: `XXXXXXXXXXXX`

### 解決方法

1. **正しいAWSプロファイルで確認**
   ```bash
   # Terraformで使用したプロファイルを確認
   cd terraform
   grep -r "profile" *.tf
   
   # または terraform.tfvars を確認
   cat terraform.tfvars
   ```

2. **CloudWatch Logsの確認**
   ```bash
   # 正しいプロファイルでログを確認
   aws logs tail /aws/lambda/gcp-billing-to-discord \
     --region ap-northeast-1 \
     --profile [正しいプロファイル名] \
     --since 24h
   ```

3. **EventBridgeルールの状態確認**
   ```bash
   # EventBridgeルールが有効か確認
   aws events describe-rule \
     --name gcp-billing-monthly-schedule \
     --region ap-northeast-1 \
     --profile [正しいプロファイル名]
   ```

4. **手動でLambda関数を実行**
   ```bash
   # テストイベントで手動実行
   aws lambda invoke \
     --function-name gcp-billing-to-discord \
     --payload '{"use_current_month": true}' \
     --region ap-northeast-1 \
     --profile [正しいプロファイル名] \
     response.json
   ```

### 追加の確認事項

1. **タイムゾーン設定**
   - EventBridgeはUTCで動作
   - `cron(10 1 * * ? *)` = UTC 01:10 = JST 10:10

2. **Lambda関数の環境変数**
   - すべての必要な環境変数が設定されているか確認
   - 特に認証情報が正しく設定されているか

3. **EventBridge実行履歴**
   ```bash
   # CloudWatchメトリクスで実行履歴を確認
   aws cloudwatch get-metric-statistics \
     --namespace AWS/Events \
     --metric-name SuccessfulRuleMatches \
     --dimensions Name=RuleName,Value=gcp-billing-monthly-schedule \
     --start-time $(date -u -v-24H +%Y-%m-%dT%H:%M:%S) \
     --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
     --period 3600 \
     --statistics Sum \
     --region ap-northeast-1 \
     --profile [正しいプロファイル名]
   ```

### 推奨される次のステップ

1. 正しいAWSプロファイルを使用してCloudWatch Logsを確認
2. EventBridgeルールが実際に実行されているか確認
3. 必要に応じてLambda関数を手動で実行してテスト