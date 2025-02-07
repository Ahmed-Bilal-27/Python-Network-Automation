import time
import paramiko
from Utils.file_handling import write_data

cisco_devnet_device = {'hostname' : 'devnetsandboxiosxe.cisco.com',
                        'username' : 'admin',
                        'password' : 'C1sco12345',
                        'device_type' : 'cisco_ios'}

ssh_client = paramiko.client.SSHClient()

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
# Connecting to the device
ssh_client.connect(hostname = cisco_devnet_device['hostname'],
                   port = 22,
                   username = cisco_devnet_device['username'],
                   password = cisco_devnet_device['password'],
                   look_for_keys = False,
                   allow_agent = False)

# Getting device shell
shell = ssh_client.invoke_shell()

shell.send(b'terminal length 0\n')
shell.send(b'show running-config\n')
# Stopping or putting the current thread to sleep
time.sleep(3)
output = shell.recv(65535).decode()
ssh_client.close()
if (write_data(__file__, output)):
    print('Written to file successfully')
else:
    print('Writing to file failed.')