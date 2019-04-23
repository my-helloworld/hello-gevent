# -*- coding: UTF-8 -*-

from gevent import monkey 
monkey.patch_all()

import threading
import socket

class ServerThread(threading.Thread):
    """
    服务端线程
    """
    def __init__(self, host='0.0.0.0', port=9090):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
     
    def run(self):
        print("[Listen]%s:%s" % (self.host, self.port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        try:
            while True:
                conn, addr = s.accept()
                print("[Connect]addr=%s:%s" % addr)
                
                socket_thread = SocketThread(conn, addr)
                socket_thread.start()
        finally:
            s.close()


class SocketThread(threading.Thread):
    """
    连接工作线程
    """
    def __init__(self, conn, addr, buffer_size=4096, handler=None):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.buffer_size = buffer_size
        self.handler = handler

    def close(self):
        threading.Thread.interrupt_main(self)
        self.conn.close()

    def handle(self, byte_data):
        handler = self.handler
        if handler is None:
            print("No handler is found")
            return

        self.conn.send(byte_data)

    def run(self):
        try:
            while True:
                data = self.conn.recv(self.buffer_size)
                if not data:
                    print("[Disconnected]addr=%s:%s" % self.addr)
                    break

                print("[Rec]addr=%s:%s" % self.addr + ", data=%s" % data)
                byte_data = bytearray(data)
                self.handle(byte_data)
        finally:
            print("[Close]conn close")
            self.conn.close()


if __name__ == '__main__':
    master_thread = ServerThread()
    master_thread.start()

    
