#!/usr/bin/env python3
"""
Formatter for converting billing information to Discord message format
"""
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class DiscordMessageFormatter:
    """
    Discord message formatter class
    """
    
    def __init__(self, exchange_rate: float = 150.0):
        """
        Initialize
        
        Args:
            exchange_rate: USD to JPY exchange rate (default: 150.0)
        """
        self.exchange_rate = exchange_rate
    def format_billing_data(self, billing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format billing information to Discord embed message format
        
        Args:
            billing_data: Billing information
            
        Returns:
            Dictionary in Discord embed message format
        """
        year = billing_data['year']
        month = billing_data['month']
        total_cost = billing_data['total_cost']
        currency = billing_data['currency']
        services = billing_data['services']
        
        # Use as-is if currency is JPY, convert if USD
        if currency == 'JPY':
            total_cost_display = total_cost
        else:
            total_cost_display = total_cost * self.exchange_rate
        
        title = f"{year}年{month}月 GCP Billing Information"
        description = f"Total amount: **¥{total_cost_display:,.0f}**"
        
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
                "name": "No service usage",
                "value": "No billing information found.",
                "inline": False
            })
            
        # Adjust if too many fields (Discord limit is 25 fields)
        if len(fields) > 25:
            logger.warning(f"Too many fields for Discord embed ({len(fields)}). Truncating to 25.")
            fields = fields[:24] 
            fields.append({
                "name": "Others",
                "value": "Many more services used...",
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
    Create DiscordMessageFormatter instance
    
    Args:
        exchange_rate: USD to JPY exchange rate (default: 150.0)
    
    Returns:
        DiscordMessageFormatter
    """
    return DiscordMessageFormatter(exchange_rate)
