import telnetlib
from Utils.file_handling import write_data

cmds = ['terminal length 0', 'show ip interface brief', 'show ip protocols', 'show ssh', 'show version', 'show cdp neighb', 'show running-config', 'show ip ospf neig', 'show ip ospf summa', 'show ip ospf database', 'show clock']
user = "Ahmed_Bilal"
password = "Ahmed_Bilal"
IPs = open('../Input_Files/03_IPs.txt')
for IP in IPs:
    HOST = IP.strip()
    print(f'{'$' * 15} -: Configuring switch with IP {HOST} :- {'$' * 15}')
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b"Username: ")
    tn.write(f"{user}\n".encode())
    if password:
        tn.read_until(b"Password: ")
        tn.write(f"{password}\n".encode())
    for cmd in cmds:
        tn.write(cmd.encode() + b"\n")
        output = tn.read_all().decode()
        print(output)
        if write_data(__file__, output, cmd=cmd):
            print(f'{'$' * 15} -: Written to file successfully. :- {'$' * 15}')
        else:
            print(f'{'$' * 15} -: Write Failed. :- {'$' * 15}')