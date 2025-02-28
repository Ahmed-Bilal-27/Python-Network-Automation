from netmiko import Netmiko
from Utils.file_handling import write_data
# from Utils.find_difference import diff
# ips = ['192.168.134.10', '192.168.134.2', '192.168.134.3']
ips = ['192.168.134.10']
for ip in ips:
    device = {'ip' : ip,
             'username' : 'Ahmed_Bilal',
             'password' : 'Ahmed_Bilal',
             'device_type' : 'cisco_ios'}

    connect = Netmiko(**device)

    print('Connected to the device')
    config = connect.send_command('show ip protocols')
    print(f'\n\n{config}')
    if write_data(__file__, config):
        print('Written to file successfully!!!')
    else:
        print('Failed to write!!!')

#diff('1-2-2025_18-15-39 01_netmiko_demo', '1-2-2025_18-15-53 01_netmiko_demo')