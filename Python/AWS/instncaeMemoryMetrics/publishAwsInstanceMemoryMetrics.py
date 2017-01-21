import boto3
import datetime
import psutil
import time
import platform
import requests
client = boto3.client(
    'cloudwatch',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-west-2'
)
d=datetime.datetime.now()
res=requests.get("http://169.254.169.254/latest/meta-data/instance-id")
instanceid=res.content
def publishMetrics(namespace,metricname,instanceid,value,unit):
        response=client.put_metric_data(
                Namespace=namespace,
                MetricData=[
                        {
                                'MetricName': metricname,
                                'Dimensions': [
                                        {
                                                'Name': 'instanceid',
                                                'Value': instanceid
                                        },
                                ],
                                'Timestamp': (datetime.datetime.utcnow()),
                                'Value': value,
                                'Unit': unit
                        },
                ]
        )
while(1):
        print("Publishing metrics")
        usedmemory=psutil.virtual_memory().used/(1024*1024)
        totalmemory=psutil.virtual_memory().total/(1024*1024)
        utilization=float(usedmemory)/float(totalmemory)*100
        avilable=totalmemory-usedmemory
        print("Utilization value is :%s" %(utilization))
        print("Available memory is :%s MB" %(avilable))
        publishMetrics(platform.system(),"MemoryAvailable",instanceid,avilable,"Megabytes")
        publishMetrics(platform.system(),"MemoryUtilization",instanceid,utilization,"Percent")
        time.sleep(5)
