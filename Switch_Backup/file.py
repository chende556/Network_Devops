import os, datetime
from pathlib import Path
import shutil

time = datetime.datetime.now().strftime('%Y%m%d')
s_pth = "/data/chendewu/projects/netmiko/Backups/"
d_path = "/data/chendewu/projects/netmiko/Backups/{}".format(time)

def create_folder(dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
        print("the folder have been created")
    else:
        print("the folder have existed")

def mv_file(source_path, dest_path):
    create_folder(dest_path)
    source = Path(source_path)
    for file in source.glob("*.txt".format(time)):
        shutil.move(str(file), dest_path)
        print("{} have moved to the new folder".format(file))

if __name__ == '__main__':
    mv_file(s_pth, d_path)

