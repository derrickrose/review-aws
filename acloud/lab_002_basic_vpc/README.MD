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

### Create route table for our public subnet, associate to public subnet and add route

- Go click Route tables on the left hand menu
- Click Create route table
- Enter name dev-miaradia-routetable-public-subnet
- Select our VPC (dev-miaradia-vpc)
- Click Create route table
- Go to Actions > Edit subnet associations
- Select our public subnet (dev-miaradia-subnet-public-a)
- Click Save associations
- Click Edit routes > Add route
- Add as destination 0.0.0.0/0 (all destination a part from VPC go through the I.G.) for Target select our internet
  gateway
- Click Save changes

Note: at this point we have 2 route tables (one default create by aws)
We should associate the second route table to the network private ?

### Create 2 EC2 instances : the first one linked to public network and second one to private

The objective is to connect to the first one inside the public network via ssh
then from there reach the second one inside private network

- Search for EC2
- Click launch instance
- Enter name dev-miaradia-ec2-public, amazon linux ami, 64 bits, t3.micro,
- Create new key pair dev-miaradia-keypair-ec2-public.pem (if windows use *.ppk)
- Edit Network settings, select public subnet, and enable auto-asign public IP
- Create new security group dev-miaradia-securitygroup-ec2-public and allow connection from My IP address which will use
  SSH port 22 TCP
- Click Launch instance
- Same way to create the second ec2 instance but linked to private network : dev-miaradia-ec2-private, ...
- Not forget to allow connection from the ip ranges within the VPC then click Launch instance (10.0.0.0/16)

### Connect to the public instance

- Go to instances, click on the Instance ID of public ec2 then click connect
- But before that, we should change the access level to the keypair file by running
  command : `chmod 400 dev-miaradia-keypair-ec2-public.pem`
- then connect using the command ssh -i "dev-miaradia-keypair-ec2-public.pem" ec2-user@54.221.26.186
  Note user is ec2-user and public ip adress is 54.... in this case
- Notice we now connected to the instance's terminal which looks like `[ec2-user@ip-10-0-1-187 ~]$`
- then create an empty keypair and paste the keypair of the private instance which we going to use to connect to it
- then connect to the private instance through the connection made onto the public one

Note : if a problem of connection verify the network or security group

### Add a role to our network to control the access to it (Network Access Control nACL)

nACL is a way to control access to our network on VPC level

- By default, with the VPC is already attached a nACL (and associated to subnets)
- The Rules in the nACL list is applied from lowest to highest number
- By creating and associating a nACL (already attached to a VPC) to a subnet, the association with the default one is
  taken off
