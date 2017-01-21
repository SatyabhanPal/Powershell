import boto3
import datetime

client = boto3.client(
    'cloudwatch',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id='AKIAIRLTODWZYZPJCCTA',
    aws_secret_access_key='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'
)
print(client.list_metrics())
d=datetime.datetime.now()
print(d)
response=client.put_metric_data(
    Namespace='windows',
    MetricData=[
        {
            'MetricName': 'MemoryUtilization',
            'Dimensions': [
                {
                    'Name': 'instanceid',
                    'Value': 'i-0af25281fa3a80b3f'
                },
            ],
            'Timestamp': (datetime.datetime.utcnow()),
            'Value': 50.0,
            'Unit': 'Percent'
        },
    ]
)
print(response)