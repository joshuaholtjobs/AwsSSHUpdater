# This example requires the requests library be installed.  You can learn more
# about the Requests library here: http://docs.python-requests.org/en/latest/
from requests import get
import boto3
from botocore.exceptions import ClientError

#Grabs public IP and adds CIDR
NEW_IP = get('https://api.ipify.org').text + "/32"

#Creates a connection to ec2
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

#EC2 instance information
response = client.describe_instances()

#Loops through everything in response and sets ID to first security group listed on EC2
for r in response["Reservations"]:
	for instance in r["Instances"]:
		id = instance["SecurityGroups"][0]["GroupId"]
		security_group = ec2.SecurityGroup(id)

#Adds current IP to SecurityGroup		
response = security_group.authorize_ingress(IpProtocol = "TCP", CidrIp = NEW_IP, FromPort = 22, ToPort = 22)

#Removes current IP from security group
#response = security_group.revoke_ingress(IpProtocol = "TCP", CidrIp = NEW_IP, FromPort = 22, ToPort = 22)