#!/usr/bin/env python3
"""
ローカル環境でLambda関数をテストするためのスクリプト
"""
import json
import os
import sys
from datetime import datetime

# lambda_functionディレクトリをモジュール検索パスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lambda_function'))

# モジュールをインポート
from main import lambda_handler

def setup_env_vars():
    """環境変数を.envrcやシェルから取得して設定（未設定時のみデフォルト値）"""
    # GCPの認証情報をファイルから読み込み
    if os.environ.get('GCP_CREDENTIALS') == 'gcp_billing_credentials.json':
        with open('gcp_billing_credentials.json', 'r') as f:
            os.environ['GCP_CREDENTIALS'] = f.read()
    
    # .envrcの値を使用、未設定時のみデフォルト値
    os.environ['GCP_BILLING_ACCOUNT_ID'] = os.environ.get('GCP_BILLING_ACCOUNT_ID', '0173B9-D2A6B3-2D4F00')
    os.environ['BIGQUERY_PROJECT_ID'] = os.environ.get('BIGQUERY_PROJECT_ID', 'gen-lang-client-0745454122')
    os.environ['BIGQUERY_TABLE_ID'] = os.environ.get('BIGQUERY_TABLE_ID', 'gcp_billing_export_v1_0173B9_D2A6B3_2D4F00')
    os.environ['DISCORD_WEBHOOK_URL'] = os.environ.get('DISCORD_WEBHOOK_URL', 'YOUR_DISCORD_WEBHOOK_URL')
    os.environ['LOG_LEVEL'] = os.environ.get('LOG_LEVEL', 'DEBUG')

def create_test_event(use_previous_month=True, year=None, month=None):
    """テスト用のイベントを作成"""
    event = {
        'use_previous_month': use_previous_month
    }
    
    # 特定月を指定する場合
    if not use_previous_month and year and month:
        event['year'] = year
        event['month'] = month
    
    return event

def main():
    """メイン関数"""
    # 環境変数を設定
    setup_env_vars()
    
    # テストケース1: 今月の途中経過を取得（デフォルト）
    test_event1 = {'use_current_month': True}
    
    # テストケース2: 前月の請求情報を取得
    test_event2 = {'use_previous_month': True}
    
    # テストケース3: 特定月の請求情報を取得
    test_event3 = {'year': 2025, 'month': 6}
    
    # テストケースを選択（コメントアウトを切り替えて使用）
    event = test_event1  # 今月の途中経過
    # event = test_event2  # 前月
    # event = test_event3  # 特定月
    
    print(f"テストイベント: {json.dumps(event, indent=2)}")
    
    # Lambda関数を実行
    result = lambda_handler(event, None)
    
    # 結果を表示
    print(f"ステータスコード: {result['statusCode']}")
    print(f"レスポンス: {result['body']}")

if __name__ == "__main__":
    main()
