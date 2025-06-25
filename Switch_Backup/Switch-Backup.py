import logging
import pandas as pd
from netmiko import ConnectHandler
# logging.basicConfig(level=logging.DEBUG)

import os, sys
os.chdir(sys.path[0])

def Get_Device_Info(filename = 'device_inventory.xlsx'):
    df = pd.read_excel(filename)
    items = df.to_dict(orient='records')
    dev_infos = []
    for i in items:
        backup_cmd = i['backup_cmd']
        del i['backup_cmd']
        dev = i
        dev_infos.append((dev, backup_cmd))
    return dev_infos

def Network_Device_Backup(dev, cmd='dis cur'):
    with ConnectHandler(**dev) as conn:
        output = conn.send_command(command_string = cmd, delay_factor=3)
        file_name = '{}.txt'.format(dev['host'])
        with open(file_name, mode='w', encoding='utf8') as f:
            f.write(output)
            print('{}备份成功！'.format(dev['host']))

def Batch_Backup(inventory_file = 'device_inventory.xlsx'):
    dev_infos = Get_Device_Info(inventory_file)
    for dev_info in dev_infos:
        dev = dev_info[0]
        cmd = dev_info[1]
        Network_Device_Backup(dev, cmd)

if __name__ == '__main__':
    Batch_Backup()
