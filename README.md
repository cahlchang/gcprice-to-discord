# GCP Billing to Discord Notifier

GCPの請求情報を取得し、Discordに通知するサーバーレスアプリケーションです。AWS Lambda上で動作し、毎日10:10 AM JSTに自動実行されます。

## 機能

- GCP BigQueryから請求データを取得
- 日本円（JPY）でコストを表示
- サービス別の内訳を表示
- Discord Embedフォーマットで見やすく通知
- EventBridgeによる定期実行（毎日10:10 AM JST）

## プロジェクト構造

```
.
├── lambda_function/        # Lambda関数のコード
│   ├── main.py            # エントリポイント
│   ├── gcp_client.py      # GCP BigQueryクライアント
│   ├── discord_client.py  # Discord Webhookクライアント
│   ├── formatter.py       # データフォーマッタ（JPY表示）
│   └── requirements.txt   # Python依存関係
├── terraform/             # インフラストラクチャコード
│   ├── provider.tf        # AWSプロバイダ設定
│   ├── variables.tf       # 変数定義
│   ├── lambda.tf          # Lambda関数とEventBridge
│   ├── iam.tf             # IAMロールとポリシー
│   └── outputs.tf         # 出力値
├── local_test.py          # ローカルテスト用スクリプト
├── build_lambda.sh        # Lambda関数のビルドスクリプト
└── troubleshooting.md     # トラブルシューティングガイド
```

## セットアップ

### 前提条件

- Python 3.9+
- Terraform 1.0+
- AWS CLI設定済み
- GCPサービスアカウント（BigQuery読み取り権限付き）
- Discord Webhook URL

### 1. 環境設定

```bash
# .envrc.exampleをコピーして編集
cp .envrc.example .envrc
# 必要な環境変数を設定
direnv allow
```

### 2. GCP認証情報の準備

```bash
# サービスアカウントJSONファイルをコピー
cp gcp_billing_credentials.json.example gcp_billing_credentials.json
# 実際の認証情報を設定
```

### 3. Terraform変数の設定

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# 必要な変数を設定
```

## ローカルテスト

```bash
# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 依存関係をインストール
pip install -r lambda_function/requirements.txt

# テスト実行
python local_test.py
```

## デプロイ

```bash
# Lambda関数をビルド
./build_lambda.sh

# Terraformでデプロイ
cd terraform
terraform init
terraform plan
terraform apply
```

## 環境変数

| 変数名 | 説明 | 例 |
|--------|------|-----|
| `GCP_CREDENTIALS` | GCPサービスアカウントJSON | `{"type": "service_account", ...}` |
| `GCP_BILLING_ACCOUNT_ID` | GCP請求アカウントID | `XXXXXX-XXXXXX-XXXXXX` |
| `BIGQUERY_PROJECT_ID` | BigQueryプロジェクトID | `your-project-id` |
| `BIGQUERY_TABLE_ID` | BigQueryテーブルID | `dataset.table` |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL | `https://discord.com/api/webhooks/...` |
| `LOG_LEVEL` | ログレベル | `INFO` |

## BigQueryテーブル構造

請求データエクスポートテーブルには以下のカラムが必要です：

- `usage_start_time`: 使用開始時刻
- `service.description`: サービス名
- `cost`: コスト金額
- `currency`: 通貨コード（通常USD）

## トラブルシューティング

- 認証エラーが発生する場合は、GCPサービスアカウントの権限を確認してください
- Lambda関数のタイムアウトは30秒に設定されています
- 詳細なトラブルシューティングは `troubleshooting.md` を参照してください

## ライセンス

MIT License