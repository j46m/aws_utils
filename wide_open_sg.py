#Get all security groups with port 22 open for all IPs

import boto3
import os


aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
aws_session_token = os.environ["AWS_SESSION_TOKEN"]

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name='us-east-1'
)

ec2 = session.client('ec2')

response = ec2.describe_security_groups(
    DryRun=False,
    MaxResults=160
)


for security_group in response['SecurityGroups']:

    for inbound_rule in security_group['IpPermissions']:
        from_port = inbound_rule.get('FromPort', -100)

        if from_port == 22:
            for range in inbound_rule['IpRanges']:
                ip_range = range.get('CidrIp', '-100')
                if ip_range == '0.0.0.0/0':
                    print(f"Security Group ID: {security_group['GroupId']}")
                    print(f"Security Group Name: {security_group['GroupName']}")    
                    print(f"Security Group Description: {security_group['Description']}")  
                    print(f" Port: {from_port}")              
                    print(f" Ip Range: {ip_range}")
                    
    print('================')
