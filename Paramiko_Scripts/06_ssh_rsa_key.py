import paramiko
import time
from Utils.file_handling import write_data

cisco_device = {
                'hostname' : '192.168.134.10',
                'username' : 'Ahmed_Bilal',
                'password' : 'Ahmed_Bilal',
                'device_type' : 'cisco_ios'
}

session = paramiko.SSHClient()

session.load_system_host_keys()
#session.load_host_keys('/home/ubuntu-24-04-1/.ssh/known_hosts')
#session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#key = getenv('/home/ubuntu-24-04-1/.ssh/id_rsa')
key_file = paramiko.RSAKey.from_private_key_file('/home/ubuntu-24-04-1/.ssh/id_rsa')
session.connect(
                hostname = cisco_device['hostname'],
                username = cisco_device['username'],
                password = cisco_device['password'],
                #timeout = 50,
                #key_filename = key,
                pkey = key_file,
                #disabled_algorithms = {'pubkeys': ['rsa-sha2-512', 'rsa-sha2-256']},
                allow_agent = False,
                look_for_keys = False
)
# Connected to device
print(f'{'=' * 25} -: Connected to: {cisco_device['hostname']} :- {'=' * 25}')
commands = ['terminal length 0', 'show ip interface brief', 'show ip protocols', 'show ssh', 'show version', 'show cdp neighb', 'show running-config']
shell = session.invoke_shell()
for cmd in commands:
    print(f'{'$' * 15} -: Executing command: {cmd} :- {'$' * 15}')
    #stdin, stdout, stderr = session.exec_command(cmd)
    #output = stdout.read().decode()
    shell.send(f'{cmd}\n'.encode())
    time.sleep(2)
    output = shell.recv(65535).decode()
    #err = stderr.read().decode()
    print(output)
    #if err:
    #    print(f'{'$' * 15} -: Error: {err} :- {'$' * 15}')
    if write_data(__file__, output, cmd = cmd):
        print(f'{'$' * 15} -: Written to file successfully. :- {'$' * 15}')
    else:
        print(f'{'$' * 15} -: Write Failed. :- {'$' * 15}')
# Closing SSH session
session.close()