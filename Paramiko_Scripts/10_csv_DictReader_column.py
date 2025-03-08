from Utils.file_handling import write_data
from csv import DictReader
import paramiko
import time

conf_dict ={}
with open("../Input_Files/02_config_in_column.csv", "r") as csv_file:
	csv_content = DictReader(csv_file)
	column_names = csv_content.fieldnames
	for row in csv_content:
		for column_name in column_names:
			if not column_name:
				continue
			if not row[column_name]:
				continue
			if column_name not in conf_dict.keys():
				conf_dict[column_name] = []
			conf_dict[column_name].append(row[column_name])
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
            if write_data(__file__, output):
                print(f'{'$' * 15} -: Written to file successfully. :- {'$' * 15}')
            else:
                print(f'{'$' * 15} -: Write Failed. :- {'$' * 15}')
        # Closing SSH session
        session.close()
    except paramiko.SSHException:
        print(f'{'!' * 15} -: Unable to connect to the device. :- {'!' * 15}')
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(f'{'!' * 15} -: Unable to connect to the device on port 22. :- {'!' * 15}')