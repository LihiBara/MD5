"""
author - lihi
date   - 2 / 11 / 22
client
"""
import os
import socket
from threading import Thread
import hashlib

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080
liba = str(os.cpu_count()) + "#"
DATA_PER_CORE = 10000000
ANSWER = ""
DIGITS = 4


def prot_recv(client_socket):
    """
    the protocol gets a msg with a # and return it without it
    :param client_socket:
    :return: the massage from the server without the #
    """
    res = ""
    data = ''
    while data != "#":
        res += data
        data = client_socket.recv(1).decode()
    return res


def check(start, crack_hash, digits):
    """
    the function getting the hash of every number
in the range and checks if it is our hash string
    :param start:
    :param crack_hash:
    :param digits:
    :return: the answer if it finds the right hash string
    """
    global ANSWER
    for i in range(start, start + DATA_PER_CORE):
        str2hash = str(i).zfill(digits)
        result = hashlib.md5(str2hash.encode())
        if result.hexdigest() == crack_hash:
            ANSWER = str2hash + "#"
            return ANSWER


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        hash_string = prot_recv(client_socket)
        threads = []
        client_socket.send(liba.encode())
        # sends to the server the liba's number
        start_range = prot_recv(client_socket)
        print(os.cpu_count())
        for i in range(os.cpu_count()):
            thread = Thread(target=check,
                            args=(int(start_range), hash_string, DIGITS))
            s = int(start_range)
            s += DATA_PER_CORE
            start_range = str(s)
            threads.append(thread)
            thread.start()
        while ANSWER == "" and threads:
            for i in threads:
                if not i.is_alive():
                    threads.remove(i)
        if ANSWER != "":
            client_socket.send(('a' + ANSWER).encode())
        else:
            client_socket.close()
            main()
    except socket.error as err:
        print('error in communication with server - ' + str(err))
    finally:
        client_socket.close()


if __name__ == '__main__':
    main()
