import os, datetime

path = "/data/chendewu/projects/netmiko/Backups/20250704"
files = os.listdir(path)
for file in files:
    file_path = os.path.join(path, file)
    print(file_path)