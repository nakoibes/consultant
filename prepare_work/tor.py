from time import sleep

import requests
import socks
import socket
from bs4 import BeautifulSoup
socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

def checkIP():
    ip = requests.get('http://checkip.dyndns.org').content
    soup = BeautifulSoup(ip, 'html.parser')
    print(soup.find('body').text)

if __name__ == '__main__':

    while True:
        checkIP()
        sleep(5)