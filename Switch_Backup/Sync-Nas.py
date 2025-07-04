import paramiko, time, os
import logging
import pandas as pd
import paramiko.sftp_client
import datetime
from stat import S_ISDIR as isdir

# print current time, day 
cur_time = datetime.datetime.now().strftime('%Y%m%d')

def Get_Info(filename):
    df = pd.read_json(filename)
    infos = df.to_dict(orient='records')
    info = infos[0]
    return info
    # print((info[0])['local_file'])

def ceate_remote_dir(remote_path):
    try:
        sftp.mkdir(remote_path)
        print("{} has been created on remote server".format(remote_path))
    except IOError as e:
        if e.errno !=17:
            print("Error creating directory {}: {}".format(remote_path, e))

def sftp_put(local_path, remote_path):
    files = os.listdir(local_path)
    for file in files:
        sub_lf = os.path.join(local_path, file)
        sub_rf = os.path.join(remote_path, file)
        sftp.put(sub_lf, sub_rf)
        print("{} has been uploaded to remote server".format(sub_lf))
    sftp.close
    transport.close

if __name__ == '__main__':
    filename='/data/chendewu/projects/netmiko/Device_Inventory/sftp_info.json'
    sftp_info = Get_Info(filename)
    ip = sftp_info['ip']
    port = sftp_info['port']
    username = sftp_info['username']
    passwd = sftp_info['password']
    l_path = "{}/{}".format(sftp_info['local_path'], cur_time)
    r_path = "{}/{}".format(sftp_info['remote_path'], cur_time)
    transport = paramiko.Transport(ip, port)
    transport.connect(username=username, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    ceate_remote_dir(remote_path=r_path)
    sftp_put(local_path=l_path, remote_path=r_path)
    # sftp_put(filename='/data/chendewu/projects/netmiko/Device_Inventory/sftp_info.json')