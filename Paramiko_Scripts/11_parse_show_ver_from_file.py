import re

from Utils.file_handling import write_json_data

version_pattern = re.compile(r'Cisco .+ Version (\S+),')
model_pattern = re.compile(r'Cisco (\S+).+bytes of memory\.')
serial_no_pattern = re.compile(r'Processor board ID (\S+)')
uptime_pattern = re.compile(r'(.+) uptime is (.*)')
device_info = {}
with open('../Output_Files/01_show_version_output.txt', 'r') as file:
    output = file.read()

    version_match = version_pattern.search(output)
    print('IOS Version'.ljust(18)+': '+version_match.group(1))
    device_info['IOS Version'] = version_match.group(1)
    model_match = model_pattern.search(output)
    print('Model '.ljust(18)+': '+model_match.group(1))
    device_info['Device Model'] = model_match.group(1)
    serial_no_match = serial_no_pattern.search(output)
    print('Serial Number '.ljust(18)+': '+serial_no_match.group(1))
    device_info['Device Serial'] = serial_no_match.group(1)
    uptime_match = uptime_pattern.search(output)
    print('Host Name '.ljust(18)+': '+uptime_match.group(1))
    print('Device Uptime '.ljust(18)+': '+uptime_match.group(2))
    device_info['Hostname'] = uptime_match.group(1)
    device_info['Device Uptime'] = uptime_match.group(2)

if write_json_data(script = __file__, data = device_info):
    print(f'{'$' * 15} -: Written to file successfully. :- {'$' * 15}')
else:
    print(f'{'$' * 15} -: Write Failed. :- {'$' * 15}')