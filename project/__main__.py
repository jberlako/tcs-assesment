"""An AWS Python Pulumi program"""

import pulumi
import pulumi_awsx as awsx
from pulumi import Output
from pulumi_aws import s3
from pulumi_aws import ec2
from pulumi_aws import ebs
import json

# Get config values
config = pulumi.Config()
vol_size = config.get('volume_size') or 4
ec2_type = config.get('instance_type') or 't2.micro'


# Create VPC and security group to enable SSH
vpc = awsx.ec2.Vpc("tcs-assessment-vpc")
allow_ssh = ec2.SecurityGroup("tcs-ssh",
    vpc_id=vpc.vpc_id,
    ingress=[
        ec2.SecurityGroupIngressArgs(
            description="SSH",
            from_port=22,
            to_port=22,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"]
        )
    ],
    egress=[ec2.SecurityGroupEgressArgs(
        from_port=0,
        to_port=0,
        protocol="-1",
        cidr_blocks=["0.0.0.0/0"]
    )])


# Select AMI for EC2
aws_linux_ami = ec2.get_ami(filters=[ec2.GetAmiFilterArgs(
        name="name",
        values=["amzn2-ami-hvm-*"],
    )],
    most_recent=True,
    owners=['amazon'])

# Create and run python script at launch
user_data = """
#!/bin/bash
echo "with open('hundred.txt', 'w') as hundred_file:\n" > hundred.py
echo "    for i in range(1, 101):\n" > hundred.py
echo "        hundred_file.write(str(i) + ' ')" > hundred.py
python hundred.py
"""

server = ec2.Instance('tcs-assessment',
    ami=aws_linux_ami.id,
    instance_type=ec2_type,
    subnet_id=vpc.private_subnet_ids.apply(lambda id: id[0]),
    availability_zone="us-east-1a",
    user_data=user_data,
    vpc_security_group_ids=[allow_ssh.id],
    tags={
        "Hello": "World"
    })

# Configure and mount EBS Volume
storage = ebs.Volume("tcs-ebs",
    availability_zone="us-east-1a",
    size=vol_size)
storage_att = ec2.VolumeAttachment("tcs-att",
    device_name="/dev/sdh",
    volume_id=storage.id,
    instance_id=server.id)

# Create ListBucket permission policy for EC2 VPC members
def bucket_list_permission(bucket_name, vpc_id):
    return Output.json_dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:ListBucket"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:SourceVpc": vpc_id
                }
            },
            "Resource": [
                Output.format("arn:aws:s3:::{0}", bucket_name)
            ]
        }]
    })

# Create Bucket with policy
bucket = s3.Bucket('tcs-assessment')
bucket_policy = s3.BucketPolicy("tcs-list-policy", 
    bucket=bucket.id, 
    policy=bucket_list_permission(bucket.id, vpc.vpc_id))

# Export the name of the instance and bucket
pulumi.export('instance_name', server.id)
pulumi.export('bucket_name', bucket.id)
