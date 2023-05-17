# tcs-assesment
 Repository containing files for TCS Coding Assignment

## Assessment Tasks
---

Write a pulumi script that accomplishes the following

- Create an EC2 instance
  - Instance type should be configurable
  - Instance EBS volume size should be configurable
  - Mount EBS volume to instance
  - Instance should be in a private subnet
  - Add tags to the instance
- Upload a python script to the EC2 instance and run it
  - Script should create a file containing the numbers 1-100
- Create an S3 Bucket
  - Grant the created EC2 instance ListBucket permissions

---

## Configuration Options

In order to configure the **EC2 instance type**, use the following command

```bash
pulumi config set instance_type t2.micro
```

You can specify any EC2 instance type supported by the AWS CLI. The default
value is **t2.micro**.

In order to configure the **size of the EBS volume**, use the following command

```bash
pulumi config set volume_size 4
```

You can set a number which is the size of the EBS volume in gigabytes (GiB). The
default value is **4**.

---

## Running the script

Execute the pulumi script from within the ```project``` directory with

```bash
pulumi up
```

When the script is complete you will find the following in your AWS console.

1. An EC2 instance with your configured instance type, and a mounted EBS volume
at /dev/sdh with the specified size. The instance will be in a private subnet 
labeled **tcs-assessment** and tagged with the following keypair;

```json
{
  "Hello": "World"
}
```

2. If you SSH to the instance, in the home directory you will find a file named
hundred.txt that contains the numbers 1-100 in sequence.

3. In your S3 console, you'll see a Bucket named **tcs-assessment**. You can
verify on the permissions view that the created EC2 instance is a member of the 
VPC that has list permissions on the bucket.

---

[Download my resume](https://docs.google.com/document/d/1Mbz48TXGh-C0rkAA372xG8xmhDrJDX0qF0LmPI6BOso/edit?usp=sharing)