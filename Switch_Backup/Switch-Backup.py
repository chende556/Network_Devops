import logging
import pandas as pd
from netmiko import ConnectHandler
import datetime
# from netmiko import redispatch
logging.basicConfig(filename='/data/chendewu/projects/netmiko/logs/backup_logs/netmiko_log.txt', level=logging.DEBUG)
import os, sys
os.chdir(sys.path[0])

def Get_Device_Info(filename):
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
        time = datetime.datetime.now().strftime('%Y%m%d%H%M')
        output = conn.send_command(command_string = cmd, delay_factor=3)
        file_name = '{}_{}.txt'.format(dev['host'], time)
        log_name = '{}_{}_log.txt'.format(dev['host'], time)
        file_path = '/data/chendewu/projects/netmiko/Backups/'
        log_path = '/data/chendewu/projects/netmiko/logs/backup_logs/'
        logfile = os.path.join(log_path, log_name)
        file = os.path.join(file_path, file_name)
        # logging.basicConfig(filename=logfile, level=logging.DEBUG)
        with open(file, mode='w', encoding='utf8') as f:
            f.write(output)
            print('{} backup success!'.format(dev['host']))
        # with open('/data/chendewu/projects/netmiko/logs/backup_logs/session_log.txt', mode='w', encoding='utf8') as f:
        #     net_connect.session_log = f

def Batch_Backup(inventory_file = '/data/chendewu/projects/netmiko/Device_Inventory/device_inventory.xlsx'):
    dev_infos = Get_Device_Info(inventory_file)
    for dev_info in dev_infos:
        dev = dev_info[0]
        cmd = dev_info[1]
        Network_Device_Backup(dev, cmd)

if __name__ == '__main__':
    Batch_Backup()
