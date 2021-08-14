import pprint
import boto3
import sys
from AwsFunctions import add_current_location, remove_old_rule
from botocore.exceptions import ClientError

#Creates a connection to ec2 & client
ec2 = boto3.resource('ec2')
client= boto3.client('ec2')

#Stores all security groups found into a variable
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

#Pretty prints json response, used for editing code)
#pprint.pprint(response)

#Loops through user-selected security group and prints all the inbound
#and outbound rules. (Is there a better way to do this?)
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
					print("---------------")
					print("")
		except Exception:
			print("No value for ports, ip ranges, and/or description available for this security group")
			print("---------------")
			print("")
			continue

print("Would you like to:")
print("1. Add current IP as an SSH rule to access attached servers")
print("2. Manually add a rule (Not functional yet)")
print("3. Delete a Rule (Not functional yet)")
print("")
Selection = input("Enter a number: ")

if Selection == "1":
	add_current_location(security_group)
elif Selection == "2":
	print("Not Functional Yet")
elif Selection == "3":
	print("Not Functional Yet")
else:
	print("No valid option selected, re-run script")