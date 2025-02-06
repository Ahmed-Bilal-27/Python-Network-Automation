import os
from Utils.file_handling import read_data, write_data
import difflib
import webbrowser

def diff(base, new):
    base_content = read_data(base)
    new_content = read_data(new)
    compare = difflib.HtmlDiff().make_file(fromlines = base_content, tolines = new_content, fromdesc = 'Reference Content',
                                           todesc = 'Current Config')

    # write_data(script = f'{base} vs {new}', data = compare, file_type = '.html')
    # webbrowser.open_new_tab(os.path.realpath(f'../Output_Files/1-2-2025_18-33-27 1-2-2025_18-15-39 01_netmiko_demo vs 1-2-2025_18-15-53 01_netmiko_demo.html'))