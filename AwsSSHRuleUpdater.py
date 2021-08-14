from botocore.exceptions import ClientError
import boto3
import sys
from AwsFunctions import add_rule, remove_old_rule
import pprint

#Creates a connection to ec2 & client
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

#Stores selected security group into ID so user can change settings
id = response["SecurityGroups"][int(select_group)]["GroupId"]
print("")
print(response["SecurityGroups"][int(select_group)]["GroupName"])
print("")

security_group = ec2.SecurityGroup(id)
#security_group = str(security_group)

#Describes rules for selected instance
response = client.describe_security_groups(GroupIds=[id])
pprint.pprint(response)
for i in response['SecurityGroups']:
	print("---------------")
	print("Security Group Name: "+i['GroupName'])
	print("")
	print("the Egress(outbound) rules are as follows: ")
	print("")
	for j in i['IpPermissionsEgress']:
		print("IP Protocol: "+j['IpProtocol'])
		for k in j['IpRanges']:
			print("IP Ranges: "+k['CidrIp'])
			try:
				print("Description: "+k['Description'])
			except:
				print("No Description")
	print("")
	print("The Ingress(inbound) rules are as follows: ")
	print("")
	for j in i['IpPermissions']:
		print("IP Protocol: "+j['IpProtocol'])
		try:
			print("PORT: "+str(j['FromPort']))
			for k in j['IpRanges']:
				print("IP Ranges: "+k['CidrIp'])
				try:
					print("Description: "+k['Description'])
					print("")
				except:
					print("No Description")
		except Exception:
			print("No value for ports, ip ranges, and/or description available for this security group")
			print("")
			continue



'''
#SecurityGroupRuleIds wants list datatype, list of security group rule IDS?
response = client.describe_security_group_rules(SecurityGroupRuleIds=)

pprint.pprint(response)

security_group = ec2.SecurityGroup(id)

Update_Rule = input("Are you sure you want to update the Security Group with your current IP? Type \"Yes\" to update the Security Group: \n")

if Update_Rule == "Yes":
	add_current_location(security_group)
else:
	print("Nothing was changed")
'''