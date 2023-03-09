import boto3
from botocore.exceptions import ClientError
import re
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2",
           "af-south-1", "ap-east-1", "ap-southeast-3", "ap-south-1",
           "ap-northeast-3", "ap-northeast-2", "ap-southeast-1",
           "ap-southeast-2", "ap-northeast-1", "ca-central-1", "eu-central-1",
           "eu-west-1", "eu-west-2", "eu-south-1", "eu-west-3", "eu-north-1", "me-south-1", "sa-east-1"]

def sg_delete(region):
    # Region
    ec2 = boto3.client('ec2', region_name=region)
    # Filter Condition
    response = ec2.describe_security_groups(
        Filters=[
            {
                'Name': 'egress.ip-permission.protocol',
                'Values': ['-1']
            },
            {
                'Name': 'egress.ip-permission.cidr',
                'Values': ['0.0.0.0/0']
            }
        ],
        GroupIds=[],
        GroupNames=[]
    )
    test = response.get('SecurityGroups', [{}])[0].get('GroupId', '')
    # Delete Operation
    try:

        res = ec2.delete_security_group(GroupId=test)
        print("sg deleted" + test)

    except ClientError as e:
        print(e)

# Delete for all region
for r in regions:
    sg_delete(r)






