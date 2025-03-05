from Utils.file_handling import write_data
from csv import reader
import paramiko
import time

conf_dict = {}
# Opening CSV file
with open("../Input_Files/01_config_in_row.csv", "r") as csv_file:
	csv_content = reader(csv_file)
	for device in csv_content:
		# if IP Address is empty then continue
		if not device[0]:
			continue
        # if IP Address key is not in the dictionary then create new key with empty list as value
		if device[0] not in conf_dict.keys():
			conf_dict[device[0]] = []
		# Length of commands
		n = len(device)
        # Starting from 1 because 1st column (0th index) is the key (IP Address)
		for conf in range(1,n):
            # Ignore empty space
			if not device[conf]:
				continue
            # Appending command to each corresponding IP address
			conf_dict[device[0]].append(device[conf])
session = paramiko.SSHClient()
session.load_system_host_keys()
for ip in conf_dict.keys():
    try:
        # Connecting to the device
        session.connect(
            hostname = ip,
            username = 'Ahmed_Bilal',
            password = 'Ahmed_Bilal',
            look_for_keys=False,
            allow_agent=False
        )
        print(f'{'=' * 25} -: Connected to: {ip} :- {'=' * 25}')
        shell = session.invoke_shell()
        for cmd in conf_dict[ip]:
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