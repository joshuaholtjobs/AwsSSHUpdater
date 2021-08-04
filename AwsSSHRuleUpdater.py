from requests import get
from botocore.exceptions import ClientError
import boto3
import sys
from AwsFunctions import add_rule, remove_old_rule

#Creates a connection to ec2?
ec2 = boto3.resource('ec2')
client= boto3.client('ec2')

#Describes ec2 instance information and adds security groups to list
response = client.describe_instances()
groups = []
for r in response["Reservations"]:
	for instance in r["Instances"]:
		for security_groups_temp in instance["SecurityGroups"]:
			groups.append(security_groups_temp)

#Makes a list of groups for user to select from
i = 0
for grp in groups:
	print(str(i) + ". " + grp['GroupName'])
	i += 1
select_group = input("Which security group did you want to update? ")

#Error checks user input
try:
	select_group = int(select_group)
except:
	print("Needs to just be a number, re-run the script")
	sys.exit()

for r in response["Reservations"]:
	for instance in r["Instances"]:
		id = instance["SecurityGroups"][int(select_group)]["GroupId"]
security_group = ec2.SecurityGroup(id)

Update_Rule = input("Are you sure you want to update the Security Group with your current IP? Type, \"Yes\" to update the Security Group: \n")

if Update_Rule == "Yes":
	add_rule()
#	remove_old_rule()
else:
	print("Nothing was changed")