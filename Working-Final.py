import boto3
from botocore.exceptions import ClientError
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


# regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2",
#            "af-south-1", "ap-east-1", "ap-southeast-3", "ap-south-1",
#            "ap-northeast-3", "ap-northeast-2", "ap-southeast-1",
#            "ap-southeast-2", "ap-northeast-1", "ca-central-1", "eu-central-1",
#            "eu-west-1", "eu-west-2", "eu-south-1", "eu-west-3", "eu-north-1", "me-south-1", "sa-east-1"]
ec2 = boto3.client('ec2')
regions = ec2.describe_regions().get('Regions',[])
x = None
u = None


for region in regions:
    reg = region['RegionName']
    ec2 = boto3.client('ec2', region_name=reg)
    # print(reg)
    try:
        response = ec2.describe_security_groups(
            Filters=[
                {
                    'Name': 'egress.ip-permission.protocol',
                    'Values': ['-1']
                },
                {
                    'Name': 'egress.ip-permission.cidr',
                    'Values': ['0.0.0.0/0']
                },
                # {
                #     'Name': 'egress.ip-permission.ipv6-cidr',
                #     'Values': ['::/0']
                # }

                # {
                #     'Name': 'vpc-id',
                #     'Values': ['vpc-8b4f1fef', 'vpc-cidr-assoc-b6ab5ddf', 'vpc-042706c8095c94586', 'vpc-cidr-assoc-089d6d5243c7c5a63', 'vpc-020367f8b09da2065', 'vpc-cidr-assoc-02760a097304c6bda', 'vpc-0a706cf43eed25465', 'vpc-cidr-assoc-0483bbfdb8dd80574', 'vpc-cidr-assoc-09b48ec5506c4dd70', 'vpc-54416f2d', 'vpc-cidr-assoc-001d3a6b', 'vpc-0f0877c19ff21cd2c', 'vpc-cidr-assoc-0391dddd73edae3fd', 'vpc-d410f9bd', 'vpc-cidr-assoc-72bc431b', 'vpc-00700b36bc4c449d3', 'vpc-cidr-assoc-090cb898fb07e4fd8', 'vpc-0cee1a6a53be2b8da', 'vpc-cidr-assoc-09adc89609660348b', 'vpc-0a69457d4c445c50f', 'vpc-cidr-assoc-0c814fbbfd7bc327d', 'vpc-01ca48c5dca991477', 'vpc-cidr-assoc-0db11afb8ff4cc9e4', 'vpc-001bee531cc43ca71', 'vpc-cidr-assoc-070c3f441696ddd65', 'vpc-0826461ea29d14680', 'vpc-cidr-assoc-09ad6835e4bbf0d7a', 'vpc-7e8c3716', 'vpc-cidr-assoc-73c76a1b', 'vpc-041f6dc90fef2ae99', 'vpc-cidr-assoc-023136509c7b9cc50', 'vpc-4c0e0e28', 'vpc-cidr-assoc-efd0c186', 'vpc-be1010da', 'vpc-cidr-assoc-51d0c138', 'vpc-046c10003ed2beab9', 'vpc-cidr-assoc-0e466536da0402282', 'vpc-1d9ff578', 'vpc-cidr-assoc-fd52b594', 'vpc-0b5f86cc148cf2e1f', 'vpc-cidr-assoc-0283d43fbb6425dca', 'vpc-0fe36f6b', 'vpc-cidr-assoc-003069aae02ea6d68', 'vpc-cidr-assoc-1d56c174', 'vpc-b86a76dd', 'vpc-cidr-assoc-a1b0cbc8', 'vpc-DO-NOT-USE}]}', 'vpc-038dac18271b11bcb', 'vpc-cidr-assoc-0852a8e52579f3821', 'vpc-VPC}', 'vpc-0d40125325bb979e0', 'vpc-cidr-assoc-0fe7d548714366c7c', 'vpc-7376f615', 'vpc-cidr-assoc-42a4e02a', 'vpc-064d16a873b421b2b', 'vpc-cidr-assoc-0f5c90814534cca5f', 'vpc-0eede7f6e6ee59b69', 'vpc-cidr-assoc-084d4b2b512a0863b', 'vpc-03fc320e3ecfe899f', 'vpc-cidr-assoc-0700c863cd16b0d95', 'vpc-0dbcff45437e01cee', 'vpc-cidr-assoc-0adc284c5fd9f3f85', 'vpc-3e38d957', 'vpc-cidr-assoc-4b3fd822', 'vpc-04af124ce045822be', 'vpc-cidr-assoc-0f13c707276153660', 'vpc-cidr-assoc-005e361dc1b3df265', 'vpc-19a72471', 'vpc-cidr-assoc-bbc715d3', 'vpc-126e9b7b', 'vpc-cidr-assoc-0fc63066', 'vpc-fc74b395', 'vpc-cidr-assoc-89739be0', 'vpc-a89ce2cd', 'vpc-cidr-assoc-e83cd781', 'vpc-081a6fbee758968ef', 'vpc-cidr-assoc-0436cad9af3ee49cf', 'vpc-d2b993b6', 'vpc-cidr-assoc-a855bdc0', 'vpc-00fc6db15465ddb91', 'vpc-cidr-assoc-0a821716057ca1cad', 'vpc-0c0686577528dc418', 'vpc-cidr-assoc-0e02155ae4e45adb0', 'vpc-71fb8b14', 'vpc-cidr-assoc-e570a28c', 'vpc-c4dd8aa0', 'vpc-cidr-assoc-ab88d3c2', 'vpc-0e066ee619ee35194', 'vpc-cidr-assoc-013841283294b96e1', 'vpc-48d7a42d', 'vpc-cidr-assoc-50ea0839', 'vpc-0e11a9f132d38a049', 'vpc-cidr-assoc-02f7bb84e5861328d', 'vpc-9f85acfb', 'vpc-cidr-assoc-7a481413', 'vpc-0b890d4c24f68c656', 'vpc-cidr-assoc-099d351f8fc25b3f7', 'vpc-arnav-cloud}]}', 'vpc-0b1e575eb27e55c98', 'vpc-cidr-assoc-06b7a7b1596d023ec', 'vpc-0a0575ded59b8b3b8', 'vpc-cidr-assoc-0cbfb134bdd25c83b', 'vpc-401be828', 'vpc-cidr-assoc-1efd0776', 'vpc-0cd5055e5277776c6', 'vpc-cidr-assoc-0b3bcfa38ae84de9c', 'vpc-cidr-assoc-04669e99367c75577', 'vpc-canada}]}', 'vpc-cc40b5a5', 'vpc-cidr-assoc-c5cc2fac', 'vpc-0b96d3427a343cdf6', 'vpc-cidr-assoc-099935100b80f989a', 'vpc-0ee993f3eea2201a7', 'vpc-cidr-assoc-011abeed25747de76', 'vpc-50227a38', 'vpc-cidr-assoc-478ede2e', 'vpc-0f71199efa1ecd612', 'vpc-cidr-assoc-09aeb2ae0c9e6c28b', 'vpc-76f8801f', 'vpc-cidr-assoc-05917e6c', 'vpc-095471de9b4635e9e', 'vpc-cidr-assoc-044c987c905a9d7e3', 'vpc-0c023466454f203d4', 'vpc-cidr-assoc-05e2beba4d95c64d3', 'vpc-dc2f17b9', 'vpc-cidr-assoc-d56998bc', 'vpc-08f63b46627d2dbb2', 'vpc-cidr-assoc-0d8be8e82b69c849a', 'vpc-059c60fc66929d64f', 'vpc-cidr-assoc-0a7836983402b43da', 'vpc-0c5e291f260069e9e', 'vpc-cidr-assoc-000d35a4de314de69', 'vpc-0dc4f3f5b8793e86a', 'vpc-cidr-assoc-0035944ac1d518b93', 'vpc-64bb2303', 'vpc-cidr-assoc-904ee6f8', 'vpc-0fdc3728aede81f5e', 'vpc-cidr-assoc-0b4548514c29df05c', 'vpc-006f0c22bd859a934', 'vpc-cidr-assoc-0f8912580548c1b8e', 'vpc-e73df88f', 'vpc-cidr-assoc-96eb22fe', 'vpc-02e7877b3d8fc08b5', 'vpc-cidr-assoc-02568a7106374a9b3', 'vpc-3058b159', 'vpc-cidr-assoc-8fb95ae6', 'vpc-0207f2d404e12ecb2', 'vpc-cidr-assoc-0792d2b497b4aa3a8', 'vpc-03c0f88c8e685062c', 'vpc-cidr-assoc-0df1b972a91a62fc0', 'vpc-007ef871f72fde82f', 'vpc-cidr-assoc-045dd986013aeace7', 'vpc-0beae9d01975ac715', 'vpc-cidr-assoc-0e2772a905eea2367', 'vpc-0890f7d71e07a4fc8', 'vpc-cidr-assoc-057b8f37daf3b8ef6', 'vpc-daff45b3', 'vpc-cidr-assoc-bd3bb2d4', 'vpc-aade0ac3', 'vpc-cidr-assoc-35e3305c', 'vpc-ecfb1785', 'vpc-cidr-assoc-62bc530b', 'vpc-0a209c843b3b0af30', 'vpc-cidr-assoc-0348092c152e5a963', 'vpc-417c4f24', 'vpc-cidr-assoc-75c0201c', 'vpc-0b6f4a6f', 'vpc-cidr-assoc-53e8993a']
                # }
            ]
        )
        # print(response)

        for sg in response['SecurityGroups']:
            x = sg['Description']

            u = sg['GroupId']
            v = sg['GroupName']
            # print(u+' '+x)
            # print(v)
            try:

                res = ec2.delete_security_group(GroupId=u)
                print("sg deleted" + u)

            except ClientError as e:
                print(e)



        # for sg in response['SecurityGroups']:
        #     x = sg['Description']
        #     for uid in sg['IpPermissions']:
        #         for securityGroup in uid['UserIdGroupPairs']:
        #             x1 = "SG ID: {}".format(securityGroup['GroupId'])
        #             y = x1.replace("SG ID: ", '')

                    # print(y+'  '+x)


                    # try:
                    #
                    #     res = ec2.delete_security_group(GroupId=y)
                    #     print("sg deleted" + y)
                    #
                    # except ClientError as e:
                    #     print(e)

    except Exception as E:
        print(region, E)
        continue