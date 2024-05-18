# Cloud-Migration-Strategy-Planner-for-Clients-AWS-Free-Tier-Only-
The Cloud Migration Strategy Planner aims to assist businesses in planning and executing their migration to the cloud effectively. This tool will analyze existing on-premises infrastructure, recommend suitable migration strategies, estimate costs, and provide a roadmap for the migration journey.

AWS Services Used:
1. AWS Discovery Services: Utilize AWS Application Discovery Service to collect data about on-premises servers, including configuration, utilization, and dependencies. This service is available within the AWS Free Tier.
2. Amazon S3: Store data collected by the discovery service in an S3 bucket. The Free Tier provides 5 GB of standard storage per month.
3. AWS Lambda: Develop Lambda functions to process data from the discovery service, perform analysis, and generate migration recommendations. Lambda offers 1 million free requests per month and 400,000 GB-seconds of compute time per month in the Free Tier.
4. Amazon DynamoDB: Store metadata and configuration information related to migration projects in DynamoDB. DynamoDB offers 25 GB of storage and 25 provisioned write capacity units and 25 provisioned read capacity units per month within the Free Tier.
5. Amazon API Gateway: Create RESTful APIs using API Gateway to interact with Lambda functions securely. This service includes 1 million API calls per month within the Free Tier.
6. Amazon CloudWatch: Monitor the health and performance of Lambda functions and API Gateway endpoints using CloudWatch metrics and alarms. CloudWatch is available within the Free Tier.

