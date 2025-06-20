#!/usr/bin/env python3
"""
Lambda function to retrieve GCP billing information and notify Discord
"""
import json
import logging
import os
from typing import Any, Dict

from discord_client import DiscordClient, create_discord_client_from_env
from formatter import DiscordMessageFormatter, create_formatter
from gcp_client import GCPBillingClient, create_gcp_client_from_env

# Logger configuration
logger = logging.getLogger()
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logger.setLevel(log_level)

# Add handler to output logs to stdout
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function entry point
    
    Args:
        event: Lambda event
        context: Lambda context
        
    Returns:
        Lambda response
    """
    logger.info(f"Lambda function started. Event: {json.dumps(event)}")
    
    try:
        # Initialize clients and formatter
        gcp_client: GCPBillingClient = create_gcp_client_from_env()
        discord_client: DiscordClient = create_discord_client_from_env()
        message_formatter: DiscordMessageFormatter = create_formatter()
        
        # Determine the month to get billing information from the event
        use_previous_month = event.get('use_previous_month', False)
        use_current_month = event.get('use_current_month', True)
        year = event.get('year')
        month = event.get('month')
        
        if use_current_month:
            logger.info("Fetching billing data for the current month to date.")
            billing_data = gcp_client.get_cost_for_current_month_to_date()
        elif use_previous_month:
            logger.info("Fetching billing data for the previous month.")
            billing_data = gcp_client.get_cost_for_previous_month()
        elif year and month:
            logger.info(f"Fetching billing data for {year}-{month}.")
            billing_data = gcp_client.get_cost_for_month(year, month)
        else:
            logger.error("Invalid event parameters: must specify use_current_month, use_previous_month, or provide 'year' and 'month'.")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': "Invalid event parameters"})
            }
            
        logger.info(f"Billing data fetched: {json.dumps(billing_data, indent=2)}")
        
        # Format billing information to Discord message format
        discord_embed = message_formatter.format_billing_data(billing_data)
        logger.debug(f"Formatted Discord embed: {json.dumps(discord_embed, indent=2)}")
        
        # Send message to Discord
        if billing_data['start_date'] == f"{billing_data['year']}-{billing_data['month']:02d}-01" and billing_data['end_date'] != f"{billing_data['year']}-{billing_data['month']:02d}-01":
            # Up to the middle of this month
            message_content = f"{billing_data['year']}年{billing_data['month']}月のGCP Billing Information ({billing_data['start_date']}〜{billing_data['end_date']})"
        else:
            # Entire month
            message_content = f"{billing_data['year']}年{billing_data['month']}月のGCP Billing Information"
        success = discord_client.send_message(message_content, embed=discord_embed)
        
        if success:
            logger.info("Successfully sent billing information to Discord.")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Billing information sent successfully'})
            }
        else:
            logger.error("Failed to send billing information to Discord.")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to send billing information to Discord'})
            }
            
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        return {
            'statusCode': 400, # Bad Request (configuration error)
            'body': json.dumps({'error': f"Configuration error: {str(ve)}"})
        }
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"An unexpected error occurred: {str(e)}"})
        }

if __name__ == '__main__':
    # Configuration for local testing (assuming environment variables are set)
    # Please run from local_test.py
    pass
