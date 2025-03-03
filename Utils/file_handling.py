import time

def write_data(script, data, cmd = None, file_type = '.txt'):
    timestamp = f'{time.localtime().tm_mday}-{time.localtime().tm_mon}-{time.localtime().tm_year}_{time.localtime().tm_hour}-{time.localtime().tm_min}-{time.localtime().tm_sec}'
    script_name = script.split('/')[-1].split('.')[0]
    filename = f'{timestamp} {cmd} {script_name}'
    path = f'../Output_Files/{filename}{file_type}'
    with open(path, 'w') as file:
        file.write(data)
    return True

def read_data(filename, file_type = '.txt'):
    path = f'../Output_Files/{filename}{file_type}'
    with open(path, 'r') as file:
        data = file.readlines()
    return data