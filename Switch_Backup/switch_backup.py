import logging
import pandas as pd
from netmiko import ConnectHandler
import datetime, paramiko
# from netmiko import redispatch
logging.basicConfig(filename='/data/chendewu/projects/netmiko/logs/backup_logs/netmiko_log.txt', level=logging.DEBUG)
import os, sys
import move_file, sync_nas
os.chdir(sys.path[0])

def get_device_info(filename):
    df = pd.read_excel(filename)
    items = df.to_dict(orient='records')
    dev_infos = []
    for i in items:
        backup_cmd = i['backup_cmd']
        del i['backup_cmd']
        dev = i
        dev_infos.append((dev, backup_cmd))
    return dev_infos

def network_device_backup(dev, cmd='dis cur'):
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

def batch_backup(inventory_file):
    dev_infos = get_device_info(inventory_file)
    for dev_info in dev_infos:
        dev = dev_info[0]
        cmd = dev_info[1]
        network_device_backup(dev, cmd)

if __name__ == '__main__':
    batch_backup(inventory_file='/data/chendewu/projects/netmiko/Device_Inventory/device_inventory.xlsx')
    move_file.mv_file()
    sftp_info = sync_nas.get_info(filename='/data/chendewu/projects/netmiko/Device_Inventory/sftp_info.json')
    sync_nas.sftp_put(sftp_info)
    
