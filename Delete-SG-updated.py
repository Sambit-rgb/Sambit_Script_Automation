import boto3
from botocore.exceptions import ClientError
import re
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

#ec2Client = boto3.client('ec2')
regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "af-south-1", "ap-east-1", "ap-southeast-3", "ap-south-1", "ap-northeast-3", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-south-1", "eu-west-3", "eu-north-1", "me-south-1", "sa-east-1"]
li = []
#ec2 = None
r = "sg-.*"
res = []
test = None

# for region in regions:
#     # print ('Checking region {}'.format(reg))
#     if region in regions:
ec2 = boto3.client('ec2', region_name="us-west-2")
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

#data = response.items()
# print(data)
lis = list(response)
print(response.get('SecurityGroups', [{}])[0].get('GroupId', ''))
# for o in lis:
#     print(o)
# o = 'sg-73c4eb09'

arr = np.array(lis)
# print(arr)

s = arr[0]
listToStr = ' '.join([str(elem) for elem in s])
# print(type(lis))

f = listToStr.split(", ")

for i in f:
    p = re.findall(r, i)
    for line in re.findall(r, i):
        x = line.replace('"', '').replace("'", '')
        li.append(str(x))
        #print(region)





for i in li:
    if i not in res:
        res.append(i)
nd = str(res)

# for n in res:
#     s = "'"+n+"'"
    #print(s)
    # try:
    #     response = ec2Client.delete_security_group(GroupIds=n)
    #     # print(response)
    #     print("sg deleted" + n)
    #
    # except ClientError as e:
    #     print(e)



#print(res)

Words = nd.split()

for word in Words:
    test = word.replace("'", '').replace(",", '').replace("[", '').replace("]", '')
    print(test)

try:
    #test = 'sg-037ad54b46a28b406'

    res = ec2.delete_security_group(GroupId=test)
    print("sg deleted" + test)

except ClientError as e:
                print(e)

# for region in regions:
#     try:
#         response = ec2Client.describe_security_groups(GroupIds=res)
#         print(response)
#     except ClientError as e:
#         print(e)

    #print(test)




#     for region in regions:
#         ec2 = boto3.resource('ec2', region_name=region)
#
#         if region in regions:
#
# try:
#     test = 'sg-037ad54b46a28b406'
#
#     res = ec2.delete_security_group(GroupId=test)
#     print("sg deleted" + test)
#
# except ClientError as e:
#                 print(e)




