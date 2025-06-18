#!/usr/bin/env python3
"""
請求情報をDiscordメッセージ形式に整形するフォーマッタ
"""
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class DiscordMessageFormatter:
    """
    Discordメッセージフォーマッタクラス
    """
    
    def __init__(self, exchange_rate: float = 150.0):
        """
        初期化
        
        Args:
            exchange_rate: USDからJPYへの為替レート (デフォルト: 150.0)
        """
        self.exchange_rate = exchange_rate
    def format_billing_data(self, billing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        請求情報をDiscord埋め込みメッセージ形式に整形
        
        Args:
            billing_data: 請求情報
            
        Returns:
            Discord埋め込みメッセージ形式の辞書
        """
        year = billing_data['year']
        month = billing_data['month']
        total_cost = billing_data['total_cost']
        currency = billing_data['currency']
        services = billing_data['services']
        
        # 通貨がJPYの場合はそのまま使用、USDの場合は変換
        if currency == 'JPY':
            total_cost_display = total_cost
        else:
            total_cost_display = total_cost * self.exchange_rate
        
        title = f"{year}年{month}月 GCP請求情報"
        description = f"合計金額: **¥{total_cost_display:,.0f}**"
        
        fields = []
        if services:
            for service in services:
                if currency == 'JPY':
                    service_cost_display = service['cost']
                else:
                    service_cost_display = service['cost'] * self.exchange_rate
                fields.append({
                    "name": service['name'],
                    "value": f"¥{service_cost_display:,.0f}",
                    "inline": True 
                })
        else:
            fields.append({
                "name": "サービス利用なし",
                "value": "請求情報がありませんでした。",
                "inline": False
            })
            
        # フィールド数が多すぎる場合は調整（Discordの制限は25フィールド）
        if len(fields) > 25:
            logger.warning(f"Too many fields for Discord embed ({len(fields)}). Truncating to 25.")
            fields = fields[:24] 
            fields.append({
                "name": "その他",
                "value": "多数のサービス利用があります...",
                "inline": False
            })

        embed = {
            "title": title,
            "description": description,
            "color": 0x4285F4,  # Google Blue
            "fields": fields,
            "footer": {
                "text": "GCP Billing Notifier"
            }
        }
        
        return embed

def create_formatter(exchange_rate: float = 150.0) -> DiscordMessageFormatter:
    """
    DiscordMessageFormatterのインスタンスを作成
    
    Args:
        exchange_rate: USDからJPYへの為替レート (デフォルト: 150.0)
    
    Returns:
        DiscordMessageFormatter
    """
    return DiscordMessageFormatter(exchange_rate)
