import socket
import traceback
def dnsLookup(s):
    with open("sample_dns.txt", "r") as f:
        for line in f:
            if s in line:
                return line
    f.close()
    return None

def dnsRegister(s):
    # can add, update record, but not delete
    # not support for one2many record
    f = open("sample_dns.txt", "r")
    lines = f.readlines()
    f.close()
    f = open("sample_dns.txt", "w")
    if len(lines) == 0:
        f.write(s)
    else:
        splitter = s.index("VALUE=")
        keyword = s[0 : splitter - 1]
        for line in lines:
            # print(line)
            if keyword not in line:
                f.write(line)
        f.write(s)
    f.close()

        
localPort = 53533
bufferSize = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(('', localPort))

print("AS up and listening")

while True:
    bytesAddressPair = sock.recvfrom(bufferSize)
    dnsMessage = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print('Received from %s:%s.' % address)
    query = dnsMessage.decode("utf-8")
    # DNS query
    if "VALUE=" not in query:
        # splitter = query.index("NAME=")
        # type = query[5 : splitter - 1]
        # hostname = query[splitter + 5 : ]
        record = dnsLookup(query)
        if record != None:
            sock.sendto(str.encode(record), address)
        else:
            sock.sendto(str.encode("bad"), address)
        print("DNS lookup")
    # DNS registration
    else:
        try:
            dnsRegister(query)
            print("DNS register")
        except IOError:
            sock.sendto(str.encode("error"), address)
            print(traceback.format_exc())
        else:
            sock.sendto(str.encode("good"), address)
