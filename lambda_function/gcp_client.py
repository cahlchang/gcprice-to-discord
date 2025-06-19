#!/usr/bin/env python3
"""
GCP Billing APIを使用して請求情報を取得するクライアント
"""
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.cloud import bigquery

logger = logging.getLogger(__name__)

class GCPBillingClient:
    """
    GCP Billing APIクライアントクラス
    """
    def __init__(self, billing_account_id: str, bigquery_project_id: str, bigquery_table_id: str, credentials=None):
        """
        初期化
        
        Args:
            billing_account_id: GCPの請求アカウントID
            bigquery_project_id: BigQueryのプロジェクトID
            bigquery_table_id: BigQueryのテーブルID
            credentials: GCP認証情報オブジェクト (オプション)
        """
        self.billing_account_id = billing_account_id
        self.bigquery_project_id = bigquery_project_id
        self.bigquery_table_id = bigquery_table_id

        if credentials:
            self.credentials = credentials
        else:
            # ADCから認証情報を取得
            scopes = ['https://www.googleapis.com/auth/cloud-billing']
            try:
                self.credentials, project = google.auth.default(scopes=scopes)
                logger.info(f"Successfully obtained ADC credentials for project: {project}")
            except google.auth.exceptions.DefaultCredentialsError as e:
                logger.error(
                    "ADC credentials not found. Make sure you have run "
                    "`gcloud auth application-default login` and have correct access."
                )
                raise e
        
        # Cloud Billing APIクライアントの構築
        self.client = build('cloudbilling', 'v1', credentials=self.credentials)
        
    def get_cost_for_month(self, year: int, month: int) -> Dict[str, Any]:
        """
        指定した月の請求情報を取得
        
        Args:
            year: 年
            month: 月
            
        Returns:
            請求情報を含む辞書
        """
        logger.info(f"Getting billing data for {year}-{month}")
        
        # 期間の開始日と終了日を計算
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        # Cloud Billing APIのフィルタ条件を作成
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        billing_data = self._fetch_billing_data(start_date_str, end_date_str)
        cost_summary = self._summarize_billing_data(billing_data)
        
        return {
            'year': year,
            'month': month,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'total_cost': cost_summary['total_cost'],
            'currency': cost_summary['currency'],
            'services': cost_summary['services']
        }
    
    def get_cost_for_previous_month(self) -> Dict[str, Any]:
        """
        前月の請求情報を取得
        
        Returns:
            請求情報を含む辞書
        """
        # 現在の日付から前月を計算
        today = datetime.now()
        first_day_of_current_month = datetime(today.year, today.month, 1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        previous_month = last_day_of_previous_month.month
        previous_year = last_day_of_previous_month.year
        
        return self.get_cost_for_month(previous_year, previous_month)
    
    def get_cost_for_current_month_to_date(self) -> Dict[str, Any]:
        """
        今月1日から今日までの請求情報を取得
        
        Returns:
            請求情報を含む辞書
        """
        today = datetime.now()
        year = today.year
        month = today.month
        
        # 期間の開始日と終了日を計算
        start_date = datetime(year, month, 1)
        end_date = today + timedelta(days=1)  # 今日の終わりまで含める
        
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        billing_data = self._fetch_billing_data(start_date_str, end_date_str)
        cost_summary = self._summarize_billing_data(billing_data)
        
        return {
            'year': year,
            'month': month,
            'start_date': start_date_str,
            'end_date': today.strftime('%Y-%m-%d'),  # 表示は今日の日付
            'total_cost': cost_summary['total_cost'],
            'currency': cost_summary['currency'],
            'services': cost_summary['services']
        }
    
    def _fetch_billing_data(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        BigQueryから指定した期間の課金データを取得
        """
        from google.cloud import bigquery

        try:
            client = bigquery.Client(project=self.bigquery_project_id, credentials=self.credentials)
            query = f"""
                SELECT
                  service.description as service_name,
                  SUM(cost) as total_cost,
                  currency
                FROM
                  `{self.bigquery_project_id}.cost_exporter.{self.bigquery_table_id}`
                WHERE
                  usage_start_time >= '{start_date}'
                  AND usage_start_time < '{end_date}'
                  AND cost > 0
                GROUP BY service.description, currency
                ORDER BY total_cost DESC
            """
            query_job = client.query(query)  # API request
            rows = query_job.result()  # Waits for query to finish
            result = [dict(row.items()) for row in rows]
            return result

        except Exception as e:
            logger.error(f"Error fetching billing data: {str(e)}")
            raise

    def _summarize_billing_data(self, billing_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        BigQueryから取得した課金データを集計
        """
        try:
            total_cost = 0.0
            currency = 'JPY'  # デフォルト通貨
            services = []

            for row in billing_data:
                service_name = row.get('service_name', 'Unknown Service')
                service_cost = float(row.get('total_cost', 0.0))
                currency = row.get('currency', currency)

                total_cost += service_cost

                services.append({
                    'name': service_name,
                    'cost': service_cost
                })

            # サービスをコストの降順でソート（クエリで実施済みだが念のため）
            services = sorted(services, key=lambda x: x['cost'], reverse=True)

            return {
                'total_cost': total_cost,
                'currency': currency,
                'services': services
            }
        except Exception as e:
            logger.error(f"Error summarizing billing data: {str(e)}")
            return {
                'total_cost': 0.0,
                'currency': currency,
                'services': []
            }
        

def create_gcp_client_from_env() -> GCPBillingClient:
    """
    環境変数から認証情報を取得してGCPクライアントを作成

    Returns:
        GCPBillingClient
    """
    # 環境変数から認証情報とアカウントIDを取得
    billing_account_id = os.environ.get('GCP_BILLING_ACCOUNT_ID')
    bigquery_project_id = os.environ.get('BIGQUERY_PROJECT_ID')
    bigquery_table_id = os.environ.get('BIGQUERY_TABLE_ID')

    if not billing_account_id:
        raise ValueError("Environment variable 'GCP_BILLING_ACCOUNT_ID' is not set")
    if not bigquery_project_id:
        raise ValueError("Environment variable 'BIGQUERY_PROJECT_ID' is not set")
    if not bigquery_table_id:
        raise ValueError("Environment variable 'BIGQUERY_TABLE_ID' is not set")

    # GCP認証情報を環境変数から取得
    credentials_json = os.environ.get('GCP_CREDENTIALS')
    credentials = None
    if credentials_json:
        try:
            credentials_info = json.loads(credentials_json)
            credentials = service_account.Credentials.from_service_account_info(credentials_info)
            logger.info("Successfully loaded GCP credentials from environment variable")
        except Exception as e:
            logger.error(f"Failed to load GCP credentials: {str(e)}")
            raise ValueError("Invalid GCP_CREDENTIALS JSON in environment variable")

    return GCPBillingClient(billing_account_id, bigquery_project_id, bigquery_table_id, credentials)
