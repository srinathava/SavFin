import socket

def sendData(conn, data):
    # print 'seinding [%s]' % data
    data_len = len(data)
    total_sent = 0
    while total_sent < data_len:
        sent = conn.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError, "Socket connection broken by client!"
        total_sent += sent

HOST = '127.0.0.1'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
sendData(s, 'Hello, world')
s.close()
