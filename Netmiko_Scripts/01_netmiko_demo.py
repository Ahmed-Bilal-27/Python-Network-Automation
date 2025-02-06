from netmiko import Netmiko
from Utils.file_handling import write_data
from Utils.find_difference import diff

cisco_devnet_device = {'ip' : 'devnetsandboxiosxe.cisco.com',
                        'username' : 'admin',
                        'password' : 'C1sco12345',
                        'device_type' : 'cisco_ios'}

connect = Netmiko(**cisco_devnet_device)

print('Connected to the device')
config = connect.send_command('sh run')
print(f'\n\n{config}')
if (write_data(__file__, config)):
    print('Written to file successfully!!!')
else:
    print('Failed to write!!!')

#diff('1-2-2025_18-15-39 01_netmiko_demo', '1-2-2025_18-15-53 01_netmiko_demo')