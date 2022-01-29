import socket
import threading
import struct
import time

class DNS_Relay:
    def __init__(self, file_name, server_name):
        self.file_name = file_name
        self.url_ip = {}
        self.server_name = server_name
        self.dns_id = {}

    def start(self):
        f = open(self.file_name, 'r', encoding='utf-8')
        for line in f:
            ip, name = line.split(' ')
            self.url_ip[name.strip('\n')] = ip
        f.close()

        buffer_size = 1024
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(('', 53))
        server.setblocking(False)
        while True:
            try:
                data, addr = server.recvfrom(buffer_size)
                threading.Thread(target=self.name_to_ip, args=(server, data, addr)).start()
            except:
                pass

    def name_to_ip(self, server, data, addr):
        start_time = time.time()
        dns_message = DNS_Message(data)
        if dns_message.QR == 0:  # 查询报文
            name = dns_message.name
            if name in self.url_ip and dns_message.type == 1:
                ip = self.url_ip[name]
                res = dns_message.generate_message(ip)
                server.sendto(res, addr)
                res_time = time.time() - start_time
                if ip == '0.0.0.0':
                    print('【拦截】   域名：{}'.format(name).ljust(50),
                          'IP：{}'.format(ip).ljust(15),'时间：{} s\n'.format(res_time),end='')
                else:
                    print('【本地】   域名：{}'.format(name).ljust(50),
                          'IP：{}'.format(ip).ljust(15),'时间：{} s\n'.format(res_time),end='')
            else:
                server.sendto(data, self.server_name)
                self.dns_id[dns_message.ID] = (name, addr, start_time)
        if dns_message.QR == 1:  # 响应报文
            if dns_message.ID in self.dns_id:
                name, destination, start_time = self.dns_id[dns_message.ID]
                server.sendto(data, destination)
                res_time = time.time()-start_time
                print('【中继】   域名：{}'.format(name).ljust(50),'时间：{} s\n'.format(res_time),end='')
                try:
                    del self.dns_id[dns_message.ID]
                except:
                    pass


class DNS_Message:
    def __init__(self, data):
        self.ID, self.flags, self.quests, self.answers, self.author, self.addition = struct.unpack('>HHHHHH',data[0:12])
        self.QR = (self.flags & 0x8000) >>15
        self.name = self.get_name(data)
        self.querybytes, self.type, self.classify = self.get_query(data[12:])

    def get_name(self, data):
        name = ''
        i = 12
        while data[i] != 0:
            for len in range(1, data[i]+1):
                name += chr(data[i+len])
            name += '.'
            i += data[i] + 1
        return name[:-1].strip()

    def get_query(self, data):
        i, length = 0, 0
        while True:
            if length == 0:
                if data[i] == 0:
                    break
                else:
                    length = int(data[i])
            else:
                length -= 1
            i += 1
        querybytes = data[0:i+1]
        type, classify = struct.unpack('>HH', data[i+1:i+5])
        return querybytes, type, classify

    def generate_message(self, ip):
        message = struct.pack('>H', self.ID)
        message += struct.pack('>H', 0x8583 if ip == '0.0.0.0' else 0x8180)
        answers = 1
        message += struct.pack('>HHHH', self.quests, answers, self.author, self.addition)

        message += self.querybytes + struct.pack('>HH', self.type, self.classify)

        name, type, classify, ttl, datalength = 0xc00c, 1, 1, 200, 4
        message += struct.pack('>HHHLH', name, type, classify, ttl, datalength)
        s_ip = ip.split('.')
        message += struct.pack('BBBB', int(s_ip[0]), int(s_ip[1]), int(s_ip[2]), int(s_ip[3]))
        return message



if __name__ == '__main__':
    relay_server = DNS_Relay(file_name='example.txt', server_name=('223.5.5.5', 53))
    relay_server.start()
