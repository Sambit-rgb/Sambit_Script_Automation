import boto3
from botocore.exceptions import ClientError
from csv import DictReader
import re

# text = input("aws_access_key_id: ")
# text1 = input("aws_secret_access_key: ")
# text2 = input("aws_session_token: ")
# Create EC2 client
# ec2 = boto3.client('ec2',
#                    aws_access_key_id= text,
#                    aws_secret_access_key= text1,
#                    aws_session_token= text2
#                    )

#Then use the session to get the resource
session = boto3.Session(profile_name='sambit')


#Then use the client to get the resource change the credential file for access,session,token
ec2 = session.client('ec2', region_name='us-west-2')

l = "/Users/sambitmohanty/Downloads/aquacloud-report-2022-06-13 11_20_46.csv"
f = (":\s(.*?)\s\(")
pattern = re.compile(f)



# iterate over
with open(l, 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        test = pattern.search(row['Message'])
        sg_name = test.group(1)

        # Delete security group
        try:
            response = ec2.delete_security_group(GroupId=sg_name)
            print('The Deleted Security Group Is ' + sg_name )

        except ClientError as e:
            print(e)








