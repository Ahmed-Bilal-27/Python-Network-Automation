######################### -: Imports :- ##############################
import paramiko
import time
from Utils.file_handling import write_data
######################### -: Imports :- ##############################
cmds = ['terminal length 0', 'show ip interface brief', 'show ip protocols', 'show ssh', 'show version', 'show cdp neighb', 'show running-config', 'show ip ospf neig', 'show ip ospf summa', 'show ip ospf database', 'show clock']
cisco_router_1 = {
                'hostname' : '192.168.134.10',
                'username' : 'Ahmed_Bilal',
                'password' : 'Ahmed_Bilal',
                'device_type' : 'cisco_ios'
}
cisco_router_2 = {
                'hostname' : '192.168.134.2',
                'username' : 'Ahmed_Bilal',
                'password' : 'Ahmed_Bilal',
                'device_type' : 'cisco_ios'
}
cisco_router_3 = {
                'hostname' : '192.168.134.3',
                'username' : 'Ahmed_Bilal',
                'password' : 'Ahmed_Bilal',
                'device_type' : 'cisco_ios'
}
# Method to SSH to a device
def ssh(device, commands):
    try:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        # Connecting to the device
        session.connect(
                        hostname = device['hostname'],
                        username = device['username'],
                        password = device['password'],
                        look_for_keys = False,
                        allow_agent = False
        )
        print(f'{'=' * 25} -: Connected to: {device['hostname']} :- {'=' * 25}')
        shell = session.invoke_shell()
        for cmd in commands:
            print(f'{'$' * 15} -: Executing command: {cmd} :- {'$' * 15}')
            shell.send(f'{cmd}\n')
            time.sleep(1.5)
            output = shell.recv(65535).decode()
            print(output)
            if write_data(__file__, output, cmd = cmd):
                print(f'{'$' * 15} -: Written to file successfully. :- {'$' * 15}')
            else:
                print(f'{'$' * 15} -: Write Failed. :- {'$' * 15}')
        # Closing SSH session
        session.close()
    except paramiko.SSHException:
        print(f'{'!' * 15} -: Unable to connect to the device. :- {'!' * 15}')
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(f'{'!' * 15} -: Unable to connect to the device on port 22. :- {'!' * 15}')

ssh(cisco_router_1, cmds)
ssh(cisco_router_2, cmds)
ssh(cisco_router_3, cmds)