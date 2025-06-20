#!/usr/bin/env python3
"""
Script for testing Lambda function in local environment
"""
import json
import os
import sys
from datetime import datetime

# Add lambda_function directory to module search path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lambda_function'))

# Import modules
from main import lambda_handler

def setup_env_vars():
    """Set environment variables from .envrc or shell (use default values only when not set)"""
    # Load GCP credentials from file
    if os.environ.get('GCP_CREDENTIALS') == 'gcp_billing_credentials.json':
        with open('gcp_billing_credentials.json', 'r') as f:
            os.environ['GCP_CREDENTIALS'] = f.read()
    
    # Use values from .envrc, only use default values when not set
    os.environ['GCP_BILLING_ACCOUNT_ID'] = os.environ.get('GCP_BILLING_ACCOUNT_ID', '0173B9-D2A6B3-2D4F00')
    os.environ['BIGQUERY_PROJECT_ID'] = os.environ.get('BIGQUERY_PROJECT_ID', 'gen-lang-client-0745454122')
    os.environ['BIGQUERY_TABLE_ID'] = os.environ.get('BIGQUERY_TABLE_ID', 'gcp_billing_export_v1_0173B9_D2A6B3_2D4F00')
    os.environ['DISCORD_WEBHOOK_URL'] = os.environ.get('DISCORD_WEBHOOK_URL', 'YOUR_DISCORD_WEBHOOK_URL')
    os.environ['LOG_LEVEL'] = os.environ.get('LOG_LEVEL', 'DEBUG')

def create_test_event(use_previous_month=True, year=None, month=None):
    """Create test event"""
    event = {
        'use_previous_month': use_previous_month
    }
    
    # When specifying a specific month
    if not use_previous_month and year and month:
        event['year'] = year
        event['month'] = month
    
    return event

def main():
    """Main function"""
    # Set environment variables
    setup_env_vars()
    
    # Test case 1: Get current month's progress (default)
    test_event1 = {'use_current_month': True}
    
    # Test case 2: Get previous month's billing information
    test_event2 = {'use_previous_month': True}
    
    # Test case 3: Get billing information for specific month
    test_event3 = {'year': 2025, 'month': 6}
    
    # Select test case (switch comments to use)
    event = test_event1  # Current month's progress
    # event = test_event2  # Previous month
    # event = test_event3  # Specific month
    
    print(f"Test event: {json.dumps(event, indent=2)}")
    
    # Execute Lambda function
    result = lambda_handler(event, None)
    
    # Display results
    print(f"Status code: {result['statusCode']}")
    print(f"Response: {result['body']}")

if __name__ == "__main__":
    main()
