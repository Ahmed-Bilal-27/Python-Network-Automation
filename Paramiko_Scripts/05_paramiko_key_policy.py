import time
import paramiko
from Utils.file_handling import write_data

cisco_devnet_device = {'hostname' : 'devnetsandboxiosxe.cisco.com',
                        'username' : 'admin',
                        'password' : 'C1sco12345',
                        'device_type' : 'cisco_ios'}

ssh_client = paramiko.SSHClient()

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh_client.load_system_host_keys()
#ssh_client.load_host_keys('/home/ubuntu-24-04-1/.ssh/known_hosts')
#ssh_client.set_missing_host_key_policy(paramiko.RejectPolicy())
#ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
# Connecting to the device
ssh_client.connect(hostname = cisco_devnet_device['hostname'],
                   username = cisco_devnet_device['username'],
                   password = cisco_devnet_device['password'])
session = ssh_client.invoke_shell()
print('Connected to a device')
commands = ['terminal length 0', 'show ip interface brief', 'show ip protocols', 'show tcp', 'show etherchannel summary', 'show cdp neighb']
for command in commands:
    session.send(f'{command}\n'.encode())
    time.sleep(3)
    output = session.recv(65535).decode()
    print(output)
    if write_data(__file__, output):
        print('Written to file successfully')
    else:
        print('Writing to file failed.')