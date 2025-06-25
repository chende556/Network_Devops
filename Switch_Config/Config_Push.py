import pandas as pd
import re
from netmiko import ConnectHandler

def Get_Device_Info(filename):
    df = pd.read_excel(filename)
    df = df.fillna('')
    items = df.to_dict(orient='records')
    devs = []
    for item in items:
        session_log = '{}.log'.format(item['host'])
        item['session_log'] = session_log
        del item['backup_cmd']
        dev = item
        devs.append(dev)
    return devs

def Push_Config(filename):
    devs = Get_Device_Info(filename)
    for dev in devs:
        push_result = {
        'push_success': True,
        'session_log': dev['session_log']
        }
        try:
            with ConnectHandler(**dev) as conn:
                conn.send_command(command_string = 'system-view', expect_string=r']')
                conn.send_command(command_string = 'info-center enable', expect_string = r']')
                conn.send_command(command_string = 'info-center loghost 192.168.40.192 log-counter disable port 1515', expect_string = r']')
                conn.send_command(command_string = 'info-center loghost source Vlanif99', expect_string = r']')
                conn.send_command(command_string = 'info-center snmp channel 2', expect_string = r']')
                conn.send_command(command_string = 'info-center console channel 2', expect_string = r']')
                conn.send_command(command_string = 'info-center monitor channel 2', expect_string = r']')
                conn.send_command(command_string = 'info-center timestamp log date', expect_string = r']')
                conn.send_command(command_string = 'quit', expect_string = r'>')
                conn.save_config()
        except Exception as e:
            push_result['push_success'] = False
            print("{}设备无法进行配置，异常日志为{}".format(dev['host'], dev['session_log']))
        print(dev['host'] + " has configured success !")

if __name__ == '__main__':
    Push_Config(filename=r'E:\work\CN_Office\Scrips\Python_Scripts\Configure_Device\config_device_inventory.xlsx')
