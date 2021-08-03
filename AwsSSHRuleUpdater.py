# This example requires the requests library be installed.  You can learn more
# about the Requests library here: http://docs.python-requests.org/en/latest/
from requests import get
import boto3
from botocore.exceptions import ClientError
import sys

#Creates a connection to ec2?
ec2 = boto3.resource('ec2')
client= boto3.client('ec2')

#Describes ec2 instance information
response = client.describe_instances()
groups = []
for r in response["Reservations"]:
	for instance in r["Instances"]:
		for security_groups_temp in instance["SecurityGroups"]:
			#print(security_groups_temp)
			groups.append(security_groups_temp)

#Creates dictionary and gives user options
i = 0
pairs_dict = {}
for grps in groups:
	print(str(i) + ". " + grps['GroupName'])
	pairs_dict[i]=grps
	i += 1
select_group = input("Which security group did you want to update? ")

#Error checks user input
try:
	select_group = int(select_group)
	#print(pairs_dict.get(select_group))
except:
	print("Needs to just be a number, re-run the script")
	sys.exit()

for r in response["Reservations"]:
	for instance in r["Instances"]:
		id = instance["SecurityGroups"][int(select_group)]["GroupId"]
security_group = ec2.SecurityGroup(id)

def add_rule():
	NEW_IP = get('https://api.ipify.org').text + "/32"
	response = security_group.authorize_ingress(IpProtocol = "TCP", CidrIp = NEW_IP, FromPort = 22, ToPort = 22)

#def remove_old_rule():
#	response = security_group.revoke_ingress(IpProtocol = "TCP", CidrIp = OLD_IP, FromPort = 22, ToPort = 22)

Update_Rule = input("Are you sure you want to update the Security Group with your current IP? Type, \"Yes\" to update the Security Group: \n")

if Update_Rule == "Yes":
	add_rule()
#	remove_old_rule()
else:
	print("Nothing was changed")