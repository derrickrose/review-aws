# Basic VPC

A vpc composed of :

- 2 subnets in different availability zones
- internet gateway to allow traffic to and from internet
- Network ACLs with security groups
- Route tables
- 2 EC2 instances

## Steps

### Creating our VPC

- Go to *Your VPCs* and click *Create VPC* (explorer window in the left)
- Choose VPC only
- Enter name dev-miaradia-vpc
- Choose IPv4 CIDR manual input
- Enter CIDR
- Choose No IPv6 CIDR block
- and click Create VPC at the bottom of the page

### Create subnets

- Go to Subnets (explorer window in the left)
- Click on Create subnet
- Select our VPC (dev-miaradia-vpc)
- Enter subnet name dev-miaradia-subnet-public-a
- Select availability zone us-east-1a
- Enter subnet CIDR bloc 10.0.1.0/24
- Click Add new subnet and enter the information : dev-miaradia-subnet-private-b with CIDR 10.0.2.0/24 and AZ
  us-east-1b
- Click on Create subnet

### Assign an automatic public IP address to our public subnet

- Go to Subnets
- Check our public subnet (dev-miaradia-subnet-public-a) and clik button Actions > Edit subnet settings
- Check Enable auto-assign public IPv4 address and Save

### Attach an Internet Gateway to our VPC

- Go to Internet gateways (explorer window in the left)
- Click Create internet gateway
- Enter name dev-miaradia-internet-gateway
- Click Create internet gateway
- Then now select Actions > Attach to VPC
- Select our vpc (dev-miaradia-vpc)
- Click Attach internet gateway

### Create route table for our public subnet

