# GCP価格情報Discord通知ツール

GCPの請求情報を取得し、Discordに通知するLambda関数とそのTerraformデプロイコードです。

## プロジェクト構造

```
.
├── lambda_function/        # Lambda関数のコード
│   ├── main.py            # エントリポイント
│   ├── gcp_client.py      # GCP APIクライアント
│   ├── discord_client.py  # Discord APIクライアント
│   ├── formatter.py       # データフォーマッタ
│   └── requirements.txt   # 依存関係
├── terraform/             # Terraformコード
│   ├── provider.tf        # プロバイダ設定
│   ├── variables.tf       # 変数定義
│   ├── lambda.tf          # Lambda関数リソース
│   └── iam.tf             # IAMリソース
└── local_test.py          # ローカルテスト用スクリプト
```

## ローカルでのテスト方法

依存関係の競合を避けるため、仮想環境を使用してテストすることをお勧めします。

### 仮想環境の作成とテスト

```bash
# 1. 仮想環境を作成
python -m venv gcp_billing_env

# 2. 仮想環境を有効化
# Windowsの場合
# gcp_billing_env\Scripts\activate
# macOS/Linuxの場合
source gcp_billing_env/bin/activate

# 3. 必要なパッケージをインストール
pip install -r lambda_function/requirements.txt

# 4. ローカルテストスクリプトを実行する前に、テストスクリプト内の環境変数を設定
# - GCP_CREDENTIALS: GCPサービスアカウントの認証情報
# - GCP_BILLING_ACCOUNT_ID: GCP請求アカウントID
# - DISCORD_WEBHOOK_URL: DiscordのウェブフックURL

# 5. テストスクリプトを実行
python local_test.py
```

### ローカルテストの設定

`local_test.py`ファイル内の`setup_env_vars()`関数を編集して、実際の認証情報とアカウントIDを設定してください。

```python
def setup_env_vars():
    """環境変数を設定"""
    # GCPの認証情報 (サービスアカウントのJSONを文字列として貼り付け)
    os.environ['GCP_CREDENTIALS'] = '{"type": "service_account", ...}'
    os.environ['GCP_BILLING_ACCOUNT_ID'] = 'YOUR_BILLING_ACCOUNT_ID'
    
    # DiscordのウェブフックURL
    os.environ['DISCORD_WEBHOOK_URL'] = 'https://discord.com/api/webhooks/...'
    
    # ログレベル
    os.environ['LOG_LEVEL'] = 'DEBUG'
```

## Terraformでのデプロイ方法

```bash
# 1. Terraformディレクトリに移動
cd terraform

# 2. 初期化
terraform init

# 3. 計画の確認
terraform plan

# 4. デプロイ
terraform apply
```

## 設定

Terraformの`variables.tf`ファイルで以下の変数を設定できます：

- `aws_region`: AWSリージョン
- `function_name`: Lambda関数名
- `schedule_expression`: CloudWatchイベントのスケジュール式
- `discord_webhook_url`: DiscordのウェブフックURL
- `gcp_credentials`: GCPサービスアカウントの認証情報
- `gcp_billing_account_id`: GCP請求アカウントID
