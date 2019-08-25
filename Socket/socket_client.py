import socket
import os
import hashlib
client = socket.socket()
client.connect(('localhost',8000))
while True:
    file_name = input('Please input the file name：').strip()
    if len(file_name) == 0:
        continue
    else:
        client.send(file_name.encode("utf-8"))
        info = client.recv(1024)
        response = info.decode()
        if response == 'Yes':
            print('the file is downloading, please wait...')
            file_size_bytes = client.recv(1024)
            file_size = int(file_size_bytes.decode())
            print('file total size:',file_size)
            file_name_new = os.path.splitext(file_name)[0] +'_new' + os.path.splitext(file_name)[-1]
            print(file_name_new)
            with open(file_name_new,'wb') as f:
                received_md5 = hashlib.md5()
                received_size = 0
                while received_size < file_size:
                    if file_size - received_size > 1024:
                        size = 1024
                    else:
                        size = file_size - received_size
                    file_content = client.recv(size)
                    received_md5.update(file_content)
                    received_size += len(file_content)
                    f.write(file_content)
                else:
                    send_md5 = (client.recv(1024)).decode()
                    if send_md5 == received_md5.hexdigest():
                        print('Download completed...')
                    else:
                        print('the file is broken...')
            print('''----------file info---------
            file total size: %s
            received file size: %s
            send_md5: %s
            received_md5: %s
            ''' %(file_size,received_size,send_md5,received_md5.hexdigest()))
        else:
            print('the file is not exist....')

