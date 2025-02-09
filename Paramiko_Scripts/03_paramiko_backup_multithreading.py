import threading
import time
import paramiko
from Utils.file_handling import write_data

cisco_devnet_device = {'hostname' : 'devnetsandboxiosxe.cisco.com',
                        'username' : 'admin',
                        'password' : 'C1sco12345',
                        'device_type' : 'cisco_ios'}

def paramiko_backup(**device):
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
    if write_data(__file__, output):
        print(f'Written {device["hostname"]} output to a file successfully')
    else:
        print(f'Written {device["hostname"]} output to a file failed.')

backup_thread_list = []
devices = [cisco_devnet_device]
for device in devices:
    backup_thread = threading.Thread(target = paramiko_backup, kwargs = device)
    backup_thread_list.append(backup_thread)
    backup_thread.start()

for thread in backup_thread_list:
    thread.join()