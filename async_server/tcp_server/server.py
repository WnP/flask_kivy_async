#!/usr/bin/env python
import json
import redis
import asyncore
import socket

redis_db = redis.StrictRedis(host='localhost', port=6379, db=1)
REDIS_PREFIX = 'kivy_flask_'
server_address = ('0.0.0.0', 5010)


class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            try:
                rgb = json.loads(data)
            except ValueError:
                rgb = False
            if rgb and isinstance(rgb, list) and len(rgb) == 3:
                redis_db.set(REDIS_PREFIX + 'r', rgb[0])
                redis_db.set(REDIS_PREFIX + 'g', rgb[1])
                redis_db.set(REDIS_PREFIX + 'b', rgb[2])

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)

if __name__ == '__main__':
    server = EchoServer(*server_address)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print '\nGoodBye'
