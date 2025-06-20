# GCP Billing to Discord Notifier

A serverless application that fetches GCP billing information and sends notifications to Discord. Runs on AWS Lambda and executes daily at 10:10 AM JST.

## Features

- Fetches billing data from GCP BigQuery
- Displays costs in Japanese Yen (JPY)
- Shows breakdown by service
- Sends well-formatted Discord Embed notifications
- Scheduled execution via EventBridge (daily at 10:10 AM JST)

## Project Structure

```
.
├── lambda_function/        # Lambda function code
│   ├── main.py            # Entry point
│   ├── gcp_client.py      # GCP BigQuery client
│   ├── discord_client.py  # Discord Webhook client
│   ├── formatter.py       # Data formatter (JPY display)
│   └── requirements.txt   # Python dependencies
├── terraform/             # Infrastructure as Code
│   ├── provider.tf        # AWS provider configuration
│   ├── variables.tf       # Variable definitions
│   ├── lambda.tf          # Lambda function and EventBridge
│   ├── iam.tf             # IAM roles and policies
│   └── outputs.tf         # Output values
├── local_test.py          # Local test script
├── build_lambda.sh        # Lambda build script
└── troubleshooting.md     # Troubleshooting guide
```

## Setup

### Prerequisites

- Python 3.9+
- Terraform 1.0+
- AWS CLI configured
- GCP service account with BigQuery read permissions
- Discord Webhook URL

### 1. Environment Configuration

```bash
# Copy and edit .envrc.example
cp .envrc.example .envrc
# Set required environment variables
direnv allow
```

### 2. GCP Credentials Setup

```bash
# Copy service account JSON file
cp gcp_billing_credentials.json.example gcp_billing_credentials.json
# Set actual credentials
```

### 3. Terraform Variables Configuration

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Set required variables
```

## Local Testing

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r lambda_function/requirements.txt

# Run test
python local_test.py
```

## Deployment

```bash
# Build Lambda function
./build_lambda.sh

# Deploy with Terraform
cd terraform
terraform init
terraform plan
terraform apply
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GCP_CREDENTIALS` | GCP service account JSON | `{"type": "service_account", ...}` |
| `GCP_BILLING_ACCOUNT_ID` | GCP billing account ID | `XXXXXX-XXXXXX-XXXXXX` |
| `BIGQUERY_PROJECT_ID` | BigQuery project ID | `your-project-id` |
| `BIGQUERY_TABLE_ID` | BigQuery table ID | `dataset.table` |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL | `https://discord.com/api/webhooks/...` |
| `LOG_LEVEL` | Log level | `INFO` |

## BigQuery Table Structure

The billing data export table requires the following columns:

- `usage_start_time`: Usage start timestamp
- `service.description`: Service name
- `cost`: Cost amount
- `currency`: Currency code (typically USD)

## Troubleshooting

- For authentication errors, check GCP service account permissions
- Lambda function timeout is set to 30 seconds
- See `troubleshooting.md` for detailed troubleshooting guide

## License

MIT License