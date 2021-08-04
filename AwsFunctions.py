def add_rule():
	try:
		NEW_IP = get('https://api.ipify.org').text + "/32"
		response = security_group.authorize_ingress(IpProtocol = "TCP", CidrIp = NEW_IP, FromPort = 22, ToPort = 22)
	except:
		print("\nThis rule is already in the Security Group")

def remove_old_rule():
	response = security_group.revoke_ingress(IpProtocol = "TCP", CidrIp = OLD_IP, FromPort = 22, ToPort = 22)
