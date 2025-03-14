import re
import paramiko
import time
from Utils.file_handling import write_json_data

version_pattern = re.compile(r'Cisco .+ Version (\S+),')
model_pattern = re.compile(r'Cisco (\S+).+bytes of memory\.')
serial_no_pattern = re.compile(r'Processor board ID (\S+)')
uptime_pattern = re.compile(r'(.+) uptime is (.*)')

device_01 = {
	'host': '192.168.134.10',
	'username': 'Ahmed_Bilal',
	'password': 'Ahmed_Bilal'
}
device_02 = {
	'host': '192.168.134.2',
	'username': 'Ahmed_Bilal',
	'password': 'Ahmed_Bilal'
}
device_03 = {
	'host': '192.168.134.3',
	'username': 'Ahmed_Bilal',
	'password': 'Ahmed_Bilal'
}
device_info = {}
def cisco_parse_version(host, username, password):
	try:
		print(f'{'=' * 25} -: Connected to: {host} :- {'=' * 25}')

		ssh_client = paramiko.SSHClient()

		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
		# Connecting to the device
		ssh_client.connect(hostname = host,
						   port = 22,
						   username = username,
						   password = password,
						   look_for_keys = False,
						   allow_agent = False)

		# Getting device shell
		shell = ssh_client.invoke_shell()

		shell.send(b'terminal length 0\n')
		time.sleep(0.5)
		shell.recv(65535).decode()
		shell.send(b'show version\n')
		# Stopping or putting the current thread to sleep
		time.sleep(1.5)
		output = shell.recv(65535).decode()
		ssh_client.close()

		# Regex Parsing
		version_match = version_pattern.search(output)
		print('IOS Version'.ljust(18) + ': ' + version_match.group(1))
		device_info['IOS Version'] = version_match.group(1)
		model_match = model_pattern.search(output)
		print('Model '.ljust(18) + ': ' + model_match.group(1))
		device_info['Device Model'] = model_match.group(1)
		serial_no_match = serial_no_pattern.search(output)
		print('Serial Number '.ljust(18) + ': ' + serial_no_match.group(1))
		device_info['Device Serial'] = serial_no_match.group(1)
		uptime_match = uptime_pattern.search(output)
		print('Host Name '.ljust(18) + ': ' + uptime_match.group(1))
		print('Device Uptime '.ljust(18) + ': ' + uptime_match.group(2))
		device_info['Hostname'] = uptime_match.group(1)
		device_info['Device Uptime'] = uptime_match.group(2)
		# Writing to file
		if write_json_data(script = __file__, data = device_info, host = host):
			print(f'{'$' * 15} -: Written to file successfully. :- {'$' * 15}')
		else:
			print(f'{'$' * 15} -: Write Failed. :- {'$' * 15}')
		print(f"\n{'#' * 25}\nFinished Executing Script\n{'#' * 25} ")
	except paramiko.ssh_exception.AuthenticationException:
		print(f'{'=' * 20} -: Authentication Failed :- {'=' * 20}')
	except AttributeError:
		print("Parsing Error, Please check the command")
		print(f'{'=' * 20} -: Parsing Error, Please check the command :- {'=' * 20}')
	except:
		print(f'{'=' * 20} -: Can not connect to Device :- {'=' * 20}')
cisco_parse_version(**device_01)
cisco_parse_version(**device_02)
cisco_parse_version(**device_03)