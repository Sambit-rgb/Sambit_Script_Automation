import boto3
from botocore.exceptions import ClientError


ec2Client = boto3.client('ec2')
regions = ec2Client.describe_regions().get('Regions',[])
unused_sgs = None
for region in regions:
    reg=region['RegionName']
    print ('Checking region {}'.format(reg))

    ec2 = boto3.resource('ec2', region_name=reg)

    sgs = list(ec2.security_groups.all())
    insts = list(ec2.instances.all())


    # all_sgs = set([sg.group_name for sg in sgs])
    all_sgs = set([sg.group_id for sg in sgs])
    all_inst_sgs = set([sg['GroupId'] for inst in insts for sg in inst.security_groups])

    unused_sgs = all_sgs - all_inst_sgs
    # print(all_inst_sgs)

    # print(set([sg.group_id for sg in sgs]))


    print ('    Total SGs:', len(all_sgs))
    print ('    SGS attached to instances:', len(all_inst_sgs))
    print ('    Orphaned SGs:', len(unused_sgs))
    print ('    Unattached SG ID:', unused_sgs)


    for i in unused_sgs:
        try:
            # res1 = ec2.connect_to_region
            # reg = region['RegionName']
            ec = boto3.client('ec2', region_name=reg)
            res = ec.delete_security_group(GroupId=i)
            print('The Deleted Security Group Is ' + i)

        except ClientError as e:
            print(e)



