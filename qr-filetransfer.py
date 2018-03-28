#!/usr/bin/python3

import http.server
import socketserver
import sys
import os
import threading
from urllib.parse import quote

import psutil
import qrcode


#获取网卡名称和其ip地址，不包括回环  
def get_netcard():  
    netcard_info = []  
    info = psutil.net_if_addrs()  
    for k,v in info.items():  
        for item in v:  
            if item[0] == 2 and not item[1]=='127.0.0.1':  
                netcard_info.append((k,item[1]))  
    return netcard_info


def url_to_qrcode(url):
    text = qrcode.make(url)
    text.show()


def http_server(port):
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(('', port), Handler)
    print("serving at port", port)
    httpd.serve_forever()


def choose_networkcard():
    netcard_info = get_netcard()
    netcard_info_line = ''
    for i,v in enumerate(netcard_info):
        netcard_info_line += '[{}]:'.format(i)
        netcard_info_line += 'name: ' + v[0]
        netcard_info_line += '  ip: ' + v[1]
        netcard_info_line += '\n'
    print('usually the network ip startswith 192.168')
    choice = input(netcard_info_line)
    try:
        choice = int(choice)
    except ValueError as e:
        print('wrong choice,exit now')
        os._exit(1)
    else:
        if isinstance(choice,int) and choice <= len(netcard_info):
            ip = netcard_info[choice][1]
            return ip
        else:
            print('wrong choice,exit now')
            os._exit(1)


def main():
    port = 8001
    t = threading.Thread(target=http_server,args=(port,))
    t.start()
    if len(sys.argv) < 2:
        print('need file arg')
        os._exit(1)
    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print('So far only support file translate')
        os._exit(1)
    ip = choose_networkcard()
    url = 'http://' + ip + ':{port}/'.format(port=port) + quote(file_path)
    url_to_qrcode(url)


if __name__ == '__main__':
    main()