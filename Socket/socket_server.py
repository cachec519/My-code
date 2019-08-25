import socket
import os
import hashlib
server = socket.socket()
server.bind(('localhost',8000))
server.listen(5)
while True:
    conn,addr = server.accept()
    print(conn,addr)
    while True:
        data = conn.recv(1024)
        file_name = data.decode()
        print(file_name)
        if os.path.isfile(file_name):
            print('begin to send')
            conn.send('Yes'.encode('utf-8'))
            file_size = os.stat(file_name).st_size
            conn.send(str(file_size).encode())
            with open(file_name,'rb') as f:
                md5 = hashlib.md5()
                for line in f:
                    md5.update(line)
                    conn.send(line)
                conn.send(md5.hexdigest().encode('utf-8'))
                print('file has sent over...')
                print('send size:',file_size)
                print('file_md5:',md5.hexdigest())
        else:
            conn.send("False".encode('utf-8'))