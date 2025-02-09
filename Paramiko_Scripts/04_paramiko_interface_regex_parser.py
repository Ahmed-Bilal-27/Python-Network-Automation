import re
from pprint import pprint
import time
import paramiko

intf_pattern = re.compile(r"(\S+)\s+(([\d\.]+)|unassigned)\s+\S+\s+\S+\s+(up|administratively down)\s+(\S+)")

cisco_devnet_device = {'hostname' : 'devnetsandboxiosxe.cisco.com',
                        'username' : 'admin',
                        'password' : 'C1sco12345',
                        'device_type' : 'cisco_ios'}

def paramiko_intf_parser(device):
    ssh_client = paramiko.client.SSHClient()

    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    # Connecting to the device
    ssh_client.connect(hostname = device['hostname'],
                       port = 22,
                       username = device['username'],
                       password = device['password'],
                       look_for_keys = False,
                       allow_agent = False)

    # Getting device shell
    shell = ssh_client.invoke_shell()
    print(f'Connecting to {device["hostname"]}')
    shell.send(b'terminal length 0\n')
    shell.send(b'show ip interface brief\n')
    # Stopping or putting the current thread to sleep
    time.sleep(3)
    output = shell.recv(65535).decode()
    ssh_client.close()
    print("Parsing the output\n")
    intf_iter = intf_pattern.finditer(output)
    ################# Printing the output ####################
    # for intf in intf_iter:
    #     print(f"\n{'*' * 30}")
    #     print(f"Interface Name: {intf.group(1)}")
    #     print(f"Interface IP: {intf.group(2)}")
    #     print(f"Interface Status: {intf.group(4)}")
    #     print(f"{'#' * 30}\n")
    ################# Creating dictionary ####################
    intf_list = []
    for intf in intf_iter:
        if intf.group(2) == 'unassigned':
            continue

        intf_dict = {}
        intf_dict['Interface Name'] = intf.group(1)
        intf_dict['Interface IP'] = intf.group(2)
        intf_dict['Interface Status'] = intf.group(4)
        intf_list.append(intf_dict)
    pprint(intf_list)
paramiko_intf_parser(cisco_devnet_device)