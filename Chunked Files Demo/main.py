import web3
import time
import eth_account.messages
import web3.contract
import sys
import socket
from threading import Thread, Lock
from lib import *
import json
from lib import w3
from customer import init_customer
from provider import init_provider

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 29290        # Port to listen on (non-privileged ports are > 1023)


if __name__ == '__main__':
    #print(sys.argv)
    #print(len(sys.argv))
    if(len(sys.argv) < 3):
        print("USAGE: <filename> is_provider address [port]")
        sys.exit()
    is_provider = sys.argv[1] == "True"
    address = sys.argv[2]
    port = PORT
    if(len(sys.argv) > 3):
        port = int(sys.argv[3])

    if(is_provider):
        init_provider(address,HOST, port)
    else:
        init_customer(address,HOST, port)


    

    



