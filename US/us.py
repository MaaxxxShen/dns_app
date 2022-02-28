from flask import Flask, request
import requests
import socket
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world! This is User Server. "

@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    # Assume a GET request:
    # http://User_Server:Port/fibonacci?hostname=fibonacci.com&fs_port=K&number=X&as_ip=Y&as_port=Z
    
    # The path accepts five parameters
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")
    
    if None in (hostname, fs_port, number, as_ip, as_port):
        return "400 Bad Request", 400
    else:
        # lookup dns of hostname
        buffer = 1024
        message = "TYPE=A" + "|NAME=" + hostname
        bytesToSend = str.encode(message)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytesToSend, (as_ip, int(as_port)))
        bytesAddressPair = sock.recvfrom(buffer)
        sock.close()
        dnsMessage = bytesAddressPair[0].decode("utf-8")
        if dnsMessage != "bad":
            # good
            fs_ip = dnsMessage[dnsMessage.index("VALUE=") + 6 : dnsMessage.index("TTL=") - 1]
            # Now assume another GET request to Fibonacci Server
            url = "http://" + fs_ip + ":"+ fs_port +"/fibonacci?number=" + number
            r = requests.get(url)
            r.encoding = "utf-8"
            if r.status_code == 200:
                return r.text
            else:
                return "400 Bad Request", 400
        else:
            return "404 Not found", 404

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
