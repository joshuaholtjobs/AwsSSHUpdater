from requests import get
		
def add_rule(security_group):
	try:
		NEW_IP = get('https://checkip.amazonaws.com/').text.strip() + "/32"
		response = security_group.authorize_ingress(IpProtocol = "TCP", CidrIp = NEW_IP, FromPort = 22, ToPort = 22)
		print("\nRule Updated")
	except:
		print("\nThis rule is already in the Security Group")

def remove_old_rule():
	response = security_group.revoke_ingress(IpProtocol = "TCP", CidrIp = OLD_IP, FromPort = 22, ToPort = 22)
