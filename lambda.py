import json
import boto3
import csv

def lambda_handler(event, context):
    # Retrieve bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download CSV file from S3
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    lines = response['Body'].read().decode('utf-8').split('\n')
    
    # Parse CSV file and generate recommendations
    recommendations = []
    migration_strategies = {'lift-and-shift': [], 're-platforming': [], 're-architecting': []}
    csv_data = csv.DictReader(lines)
    for row in csv_data:
        # Analyze server configurations and generate recommendations
        recommendation, migration_strategy = generate_recommendation(row)
        recommendations.append(recommendation)
        if migration_strategy:
            migration_strategies[migration_strategy].append(row['ExternalId'])
    
    # Return recommendations and migration strategies
    return {
        'statusCode': 200,
        'body': {
            'recommendations': recommendations,
            'migration_strategies': migration_strategies
        }
    }

def generate_recommendation(server_config):
    # Analyze server configurations and generate recommendations based on different attributes
    
    recommendation = "Migration Plan Recommendation for server with ExternalId {}: \n".format(server_config['ExternalId'])
    migration_strategy = None
    
    # Example recommendation logic based on CPU utilization
    if float(server_config['CPU.UsagePct.Avg']) > 80:
        migration_strategy = 're-platforming'
        hint = "High CPU utilization may require re-platforming"
        recommendation += "- Analyze current workload and performance requirements.\n"
        recommendation += "- Identify EC2 instances with higher CPU capacity.\n"
        recommendation += "- Perform load testing to ensure new instance meets performance needs.\n"
        recommendation += "- Plan for downtime or rolling updates during migration. (Hint: {})\n".format(hint)
    
    # Example recommendation logic based on RAM utilization
    if float(server_config['RAM.UsedSizeInMB.Avg']) / float(server_config['RAM.TotalSizeInMB']) > 0.75:
        migration_strategy = 're-platforming'
        hint = "High RAM utilization may require re-platforming"
        recommendation += "- Assess memory requirements of current applications.\n"
        recommendation += "- Choose EC2 instance types with more memory.\n"
        recommendation += "- Optimize memory usage to minimize costs.\n"
        recommendation += "- {}.\n".format(hint)
    
    # Example recommendation logic based on disk I/O
    if float(server_config['DiskReadsPerSecondInKB.Avg']) > 1000 or float(server_config['DiskWritesPerSecondInKB.Avg']) > 1000:
        migration_strategy = 're-architecting'
        hint = "High disk I/O may require re-architecting"
        recommendation += "- Evaluate disk I/O patterns and requirements.\n"
        recommendation += "- Select EC2 instances with higher I/O performance or provisioned IOPS.\n"
        recommendation += "- Consider optimizing disk usage or implementing caching mechanisms.\n"
        recommendation += "- {}.\n".format(hint)
    
    # Example recommendation logic based on network throughput
    if float(server_config['NetworkReadsPerSecondInKB.Avg']) > 1000 or float(server_config['NetworkWritesPerSecondInKB.Avg']) > 1000:
        migration_strategy = 're-platforming'
        hint = "High network throughput may require re-platforming"
        recommendation += "- Analyze network traffic patterns and bandwidth requirements.\n"
        recommendation += "- Choose EC2 instances with higher network performance.\n"
        recommendation += "- Implement content delivery networks (CDNs) for static assets.\n"
        recommendation += "- {}.\n".format(hint)
    
    # Example recommendation logic based on operating system
    if server_config['OS.Name'] == 'Windows' and server_config['OS.Version'] == '2012':
        migration_strategy = 're-platforming'
        hint = "Windows Server 2012 may require re-platforming"
        recommendation += "- Check application compatibility with newer Windows Server versions.\n"
        recommendation += "- Plan for OS upgrade and compatibility testing.\n"
        recommendation += "- {}.\n".format(hint)
    
    # Example recommendation logic based on application dependencies
    if server_config['Applications'] != '':
        migration_strategy = 're-platforming'
        hint = "Applications may require re-platforming"
        recommendation += "- Create an inventory of installed applications and dependencies.\n"
        recommendation += "- Validate compatibility of applications with target environment.\n"
        recommendation += "- Plan for application migration or reconfiguration.\n"
        recommendation += "- {}.\n".format(hint)
    
    # Example recommendation logic based on security requirements
    if 'PCI' in server_config['Tags']:
        recommendation += "- Ensure compliance with PCI DSS requirements during migration.\n"
    
    # Example recommendation logic based on cost optimization
    if float(server_config['CPU.UsagePct.Avg']) < 10 and float(server_config['RAM.UsedSizeInMB.Avg']) / float(server_config['RAM.TotalSizeInMB']) < 0.25:
        migration_strategy = 'lift-and-shift'
        hint = "Underutilized servers may be candidates for lift-and-shift"
        recommendation += "- Rightsize or consolidate resources for cost optimization.\n"
        recommendation += "- {}.\n".format(hint)
  
    return recommendation, migration_strategy
