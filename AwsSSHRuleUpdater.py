from botocore.exceptions import ClientError
import boto3
import sys
from AwsFunctions import add_rule, remove_old_rule
import pprint

#Creates a connection to ec2?
ec2 = boto3.resource('ec2')
client= boto3.client('ec2')

#Stores security groups into a variable
response = client.describe_security_groups()

#Prints a numbered list for user to choose a group from
i = 0
for group in response["SecurityGroups"]:
	print(str(i) + ". " + group['GroupName'])
	i += 1

#Takes user's choice
select_group = input("Which security group did you want to update? (Use corresponding number): ")

#Makes sure input is a integer
try:
	select_group = int(select_group)
except:
	print("Needs to just be a valid number, re-run the script")
	sys.exit()

id = response["SecurityGroups"][int(select_group)]["GroupId"]
print("")
print(response["SecurityGroups"][int(select_group)]["GroupName"])
security_group = ec2.SecurityGroup(id)

Update_Rule = input("Are you sure you want to update the Security Group with your current IP? Type \"Yes\" to update the Security Group: \n")

if Update_Rule == "Yes":
	add_rule(security_group)
#	remove_old_rule()
else:
	print("Nothing was changed")