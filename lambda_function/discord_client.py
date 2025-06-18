#!/usr/bin/env python3
"""
Discordにメッセージを送信するクライアント
"""
import json
import logging
import os
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)

class DiscordClient:
    """
    Discordクライアントクラス
    """
    def __init__(self, webhook_url: str):
        """
        初期化
        
        Args:
            webhook_url: DiscordのウェブフックURL
        """
        self.webhook_url = webhook_url
        
    def send_message(self, message: str, embed: Optional[Dict[str, Any]] = None) -> bool:
        """
        Discordにメッセージを送信
        
        Args:
            message: 送信するメッセージ
            embed: 埋め込みメッセージ（オプション）
            
        Returns:
            送信に成功した場合はTrue、失敗した場合はFalse
        """
        payload = {
            'content': message
        }
        
        if embed:
            payload['embeds'] = [embed]
            
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(self.webhook_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()  # HTTPエラーの場合は例外を発生させる
            logger.info(f"Message sent to Discord successfully. Status: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message to Discord: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Discord API response: {e.response.text}")
            return False

def create_discord_client_from_env() -> DiscordClient:
    """
    環境変数からDiscordクライアントを作成
    
    Returns:
        DiscordClient
    """
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        raise ValueError("Environment variable 'DISCORD_WEBHOOK_URL' is not set")
        
    return DiscordClient(webhook_url)
