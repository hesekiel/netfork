# 2016, Ivo Nutar

import exceptions
import socket
import global_vars
import MySQLdb


class Fuzzable:

    def __init__(self):
        return


class Client(Fuzzable):
    pass


class Server(Fuzzable):
    pass


class Connection:

    target_addr = None
    target_proto = None
    target_port = None

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

        self.target_addr = self.get_host_addr(host)

        self.sock = socket.socket(socket.AF_INET, proto)
        self.sock.bind((global_vars.LOCAL_ADDR, global_vars.LOCAL_PORT))
        self.sock.connect((self.target_addr, host_port))

        self.target_proto = host_proto
        self.target_port = host_port
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
            try:
                data = self.sock.recv(8192, socket.MSG_DONTWAIT)
            except:
                self.connect(self.target_addr, self.target_proto, self.target_port)
                return None
            if not data:
                break
            total_data.append(data)
        self.connect(self.target_addr, self.target_proto, self.target_port)
        return ''.join(total_data)


class Logger:

    logger = None

    def __init__(self):
        return

    def get_logger(self):
        return self.logger


class DatabasePoller:

    host = None
    user = None
    passwd = None
    db = None
    db_con = None
    db_cur = None

    def __init__(self):
        pass

    # TODO find out how to use password hash
    def open(self, db, user, passwd, host=global_vars.DB_HOST):

        self.db_con = MySQLdb.connect(host, user, passwd, db)
        self.db_cur = self.db_con.cursor()

        return 0

    def close(self):

        self.db_con.close()

        return 0

    def execute(self, cmd):

        self.db_cur.execute(cmd)

        return self.db_cur.fetchall()
