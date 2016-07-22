# 2016, Ivo Nutar

import exceptions
import socket
import global_vars


class Fuzzable:

    def __init__(self):
        return


class Client(Fuzzable):
    pass


class Server(Fuzzable):
    pass


class Connection:

    sock = None

    def __init__(self):
        return

    @staticmethod
    def get_host_addr(host):
        # TODO Not particularly good function
        try:
            host_addr = socket.gethostbyname(host)
        except socket.gaierror:
            try:
                socket.inet_aton(host)
                return host
            except socket.error:
                raise AttributeError("Host address %s is not correct" % host)

        return host_addr

    def connect(self, host, host_proto, host_port):

        if host_proto == "TCP":
            proto = socket.SOCK_STREAM
        elif host_proto == "UDP":
            proto = socket.SOCK_DGRAM
        else:
            raise exceptions.UnknownProtocolException("%s is unknown protocol" % host_proto)

        host_addr = self.get_host_addr(host)

        self.sock = socket.socket(socket.AF_INET, proto)
        self.sock.bind((global_vars.LOCAL_ADDR, global_vars.LOCAL_PORT))
        self.sock.connect((host_addr, host_port))

        return

    def close(self):

        self.sock.close()

        return 0

    def send_data(self, data):

        self.sock.sendall(data)

        return 0

    def recv_data(self):

        total_data = []

        while True:
            data = self.sock.recv(8192)
            if not data:
                break
            total_data.append(data)

        return ''.join(total_data)


class Logger:

    logger = None

    def __init__(self):
        return

    def get_logger(self):
        return self.logger


class DatabasePoller:

    def __init__(self):
        pass
