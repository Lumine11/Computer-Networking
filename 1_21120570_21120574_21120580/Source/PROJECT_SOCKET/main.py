import socket
import threading
from asyncio.windows_events import NULL
from os import error
import os.path
from wsgiref.util import request_uri
import time

HOST = socket.gethostbyname('127.0.0.1')
PORT = 8080
ADDR =('127.0.0.1',PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
FORMAT='utf8'
global check_
try:
    SERVER.bind((HOST,PORT))
    print(f'* Running on http://{HOST}:{PORT}')
except socket.error as e:
    print(f'socket error: {e}')
    print('socket error: %s' %(e))

Close_Msg=''
def _start():
    global Close_Msg
    SERVER.listen() 
    while True:
        conn, addr = SERVER.accept()
        thread = threading.Thread(target=_handle, args=(conn, addr))
        thread.start()

URL = 'taolao'
def _handle(conn,addr):
    while True:
        data = conn.recv(1024).decode()
        backupdata = data;
        if not data: 
            conn.close()
            break
        global URL
        request_line = data.split('\r\n')[0]
        request_method = request_line.split(' ')[0]
        reuqest_url = (request_line.split(' ')[1]).strip('/')
        print(request_line + ' 200 Ok')
        print(request_method, reuqest_url)
        if request_method == 'GET':
            if reuqest_url == '':   #index page
                URL =''
                url = 'index.html'
                Content_type = 'text/html'
            elif reuqest_url == 'favicon.ico': 
                url = reuqest_url
                URL = url
                Content_type = 'image/x-icon'
            elif reuqest_url == 'css/style.css':
                url = 'style.css'
                Content_type = 'text/css'
                URL = url
            elif reuqest_url == 'css/utils.css':
                url ='utils.css'
                URL = url
                Content_type='text/css'

            elif reuqest_url.find('jpg',0,len(reuqest_url)) != -1:
                url = reuqest_url.split('/')[1]
                URL = url
                Content_type='image/jpeg'

            elif reuqest_url.find('png',0,len(reuqest_url)) != -1:
                url = reuqest_url.split('/')[1]
                URL = url
                print('--------------')
                print(url)
                Content_type='image/png'
            else: 
                url = '404.html'
                URL = url
                Content_type = 'text/html'
            print('Content-type: '+ Content_type )

        if request_method == 'POST':              
                USERNAME = 'admin'
                PASSW = 'psw=123456'
                
                usp = backupdata.split('uname=')[1]
                print(usp)
                usp=usp.split('&')
                print(usp)


                if usp[0] == USERNAME and usp[1] == PASSW:
                   url = 'images.html'
                   URL='images.html'
                   Content_type = 'text/html'
                else:
                    url = '401.html'
                    URL = url
                    Content_type = 'text/html'
        
        data = readfile_(url,Content_type)
        conn.send(data)

def readfile_(Name,Content_Type):
    f = open (Name,'rb')
    fdata = response_(Content_Type)
    fdata+=f.read()
    return fdata

def FileSize (url):
    file_path = open(url,"r")
    file_path.seek(0,os.SEEK_END)
    sz = file_path.tell()
    file_path.close()
    return sz

def response_ (Content_Type):

    msg_header = 'HTTP/1.1 200 \n'
    msg_header += f'Content_Type: {Content_Type}\n'
    msg_header += 'Connection : keep-alive\n'
    if  URL!='taolao':
        if URL=='':
            Fakeurl='index.html'
        else:
            Fakeurl = URL
        msg_header += f'Content-length: { FileSize(Fakeurl) }'
    msg_header += '\r\n\r\n'
    msg_header = msg_header.encode()
    return msg_header

if __name__ == '__main__':
    _start()