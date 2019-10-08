import socket
import time
import json
import datetime
import os
import sys
from urllib.parse import quote, unquote, urlencode, urljoin


base_path = os.path.dirname(os.path.abspath(__file__))
file_type_dic = {'png':'image/png', 'jpg':'image/jpg', 'jpeg':'image/jpeg',
                 'py':'text/plain', 'txt':'text/plain', 'html':'text/html',
                 'js':'application/javascript','css':'text/css', 'woff':'application/octet-stream',
                 'gif':'image/gif'
                 }

def index(client):
    client.send("HTTP/1.1 200 OK\r\n\r\n".encode("utf8"))
    client.send("<h1 style='color:red'>Hello, index</h1>".encode("utf8"))

def data(client):
    client.send("HTTP/1.1 200 OK\r\n\r\n".encode())
    client.send("<h1 style='color:red'>Hello, data</h1>".encode())

def time_now(client):
    client.send("HTTP/1.1 200 OK\r\n".encode())
    client.send("Token:11111111111\r\n\r\n".encode())
    client.send(("<h1 style='color:red'>%s</h1>"%(str(datetime.datetime.now()))).encode())

url_mapping = {
    '/': index,
    '/data': data,
    '/time':time_now
}

def handle_request(client):
    request_data = client.recv(1024).decode()
    if not request_data:
        return None

    data = request_data.split('\r\n')
    uri = data[0].split()[1]
    uri = unquote(uri)        # 中文路径问题
    if '?' in uri:
        uri, params = uri.split('?')
    print('请求路径')
    print(uri)

    full_path = os.path.join(base_path, uri[1:])
    headers = {"HTTP/1.1 200 OK":"","Content-Type:":"text/html; charset=utf-8"}

    files = ''
    print(full_path)
    if os.path.exists(full_path):
        if os.path.isdir(full_path):
            files = os.listdir(full_path)
            files = ['<a href="%s">%s</a><br>'%(("/" + uri[1:] + "/"+ name).replace('//', '/'), name) for name in files]
            files = ''.join(files).encode()
        elif os.path.isfile(full_path):
            filename = full_path.split('\\')[-1]
            file_type = file_type_dic.get(filename.split('.')[-1])
            if file_type:
                headers['Content-Type:'] = file_type + '; charset=utf-8'
            else:
                headers['Content-Disposition:'] = 'attachment; filename=%s'%(filename)
            with open(full_path, 'rb') as f:
                files = f.read()
    else:
       files = "<h1 style='color:red'>网页找不到</h1>".encode()

    response = '\r\n'.join(k + v for k, v in headers.items()) + '\r\n\r\n'
    client.send(response.encode())
    client.send(files)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8800))
    sock.listen(1)

    while True:
        print("the server is waiting for client-connection....")
        connection, address = sock.accept()
        try:
            handle_request(connection)
        except Exception as e:
            print('error:', e)
        connection.close()


if __name__ == '__main__':
    pass
    # 路径拼接
    # path = os.path.dirname(__file__)
    # path_new = os.path.join(path, '')
    # print('tt/tt.txt')
    # print(path, path_new)
    # print(os.path.exists(path_new))
    # print(os.path.isdir(path_new))
    main()
