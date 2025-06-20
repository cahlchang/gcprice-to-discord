#!/usr/bin/env python3
"""
Client for sending messages to Discord
"""
import json
import logging
import os
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)

class DiscordClient:
    """
    Discord client class
    """
    def __init__(self, webhook_url: str):
        """
        Initialize
        
        Args:
            webhook_url: Discord webhook URL
        """
        self.webhook_url = webhook_url
        
    def send_message(self, message: str, embed: Optional[Dict[str, Any]] = None) -> bool:
        """
        Send message to Discord
        
        Args:
            message: Message to send
            embed: Embed message (optional)
            
        Returns:
            True if successful, False if failed
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
            response.raise_for_status()  # Raise exception for HTTP errors
            logger.info(f"Message sent to Discord successfully. Status: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message to Discord: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Discord API response: {e.response.text}")
            return False

def create_discord_client_from_env() -> DiscordClient:
    """
    Create Discord client from environment variables
    
    Returns:
        DiscordClient
    """
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        raise ValueError("Environment variable 'DISCORD_WEBHOOK_URL' is not set")
        
    return DiscordClient(webhook_url)
