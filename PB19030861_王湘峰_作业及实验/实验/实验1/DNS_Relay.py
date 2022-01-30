import struct
import socket
from time import time
import threading


class DNS_Package:
    def __init__(self, data):
        self.type = b''
        self.classify = b''
        self.querybytes = b''
        self.position = 0

        self.name = self.get_name(data)
        self.id, self.flags = struct.unpack('>HH', data[0:4])
        self.quests, self.answers, self.author, self.addition = struct.unpack('>HHHH', data[4:12])
        self.is_query = not (self.flags & 0x8000)
        if self.is_query:
            self.query = self.query_part(data[12:])

    def get_name(self, data):
        name = ''
        i = 12
        while data[i] != 0:
            for j in range(1, data[i] + 1):
                name += chr(data[i + j])
            name += '.'
            i += data[i] + 1
        self.position = i - 12
        return name[:-1]

    def query_part(self, data):
        p = self.position
        self.querybytes = data[:p + 1]
        self.type, self.classify = struct.unpack('>HH', data[p + 1:p + 5])
        return self.querybytes + struct.pack('>HH', self.type, self.classify)

    def generate_answer(self, ip):
        # Header
        response = struct.pack('>H', self.id)
        if ip == '0.0.0.0':
            response += struct.pack('>H', 0x8583)  # Flags: 0x8583 Intercept query
        else:
            response += struct.pack('>H', 0x8180)  # Flags: 0x8180 Standard query , No error
        self.answers = 1
        response += struct.pack('>HHHH', self.quests, self.answers, self.author, self.addition)
        # Query
        response += self.query
        # Answer Author and Addition
        response += b'\xC0\x0C'  # point to name
        response += b'\x00\x01'  # TYPE:A
        response += b'\x00\x01'  # Class: IN (0x0001)
        response += b'\x00\x00\x00\xC8'  # Time to live: 200
        response += b'\x00\x04'  # Data length: 4
        # ip data
        s = ip.split(".")
        response += struct.pack('BBBB', int(s[0]), int(s[1]), int(s[2]), int(s[3]))
        return response


class DNS_Relay:
    def __init__(self, config='config'):
        self.config = config
        self.map = {}  # dict<name:str, ip:str>
        self.read_config()
        self.nameserver = ('223.5.5.5', 53)
        self.relay = {}  # dict{id: int, tuple<addr,name, start_time>}

    def read_config(self):
        with open(self.config, 'r') as f:
            for line in f:
                if line.strip() != '':
                    ip, name = line.split(' ')
                    self.map[name.strip()] = ip.strip()

    def handle(self, s, data, addr):
        start = time()
        dns_package = DNS_Package(data)
        ID = dns_package.id
        if dns_package.is_query:
            name = dns_package.name
            # print(dns_package.type)
            if name in self.map and dns_package.type == 1:
                ip = self.map[name]
                response = dns_package.generate_answer(ip)
                s.sendto(response, addr)
                print(name, end='\t')
                if ip == '0.0.0.0':
                    print(' INTERCEPT {}s'.format(time() - start))
                else:
                    print(' RESOLVED {}s'.format(time() - start))
            else:
                s.sendto(data, self.nameserver)
                self.relay[ID] = (addr, name, start)
        else:
            if ID in self.relay:
                target_addr, name, start_time = self.relay[ID]
                s.sendto(data, target_addr)
                print(name, ' RELAY {}s'.format(time() - start_time))
                del self.relay[ID]

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('0.0.0.0', 53))
        while True:
            try:
                data, addr = s.recvfrom(512)
                thread = threading.Thread(target=self.handle, args=(s, data, addr))
                thread.start()
                thread.join(timeout=1)
            except Exception:
                pass


if __name__ == '__main__':
    dns_relay = DNS_Relay('example.txt')
    dns_relay.run()
