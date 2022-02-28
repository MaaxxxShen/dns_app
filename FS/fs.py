from flask import Flask, request
import socket

app = Flask(__name__)

spec = None

def fibonacci_dp(K):
    a = 0
    b = 1
    if K == 0:
        return a
    while (K > 1):
        tmp = a + b
        a = b
        b = tmp
        K = K - 1
    return b

@app.route('/')
def hello_world():
    return 'Hello world! This is Fibonacci Server. '

@app.route('/register', methods = ['PUT'])
def register():
    if request.is_json:
        global spec
        spec = request.get_json()
        print(spec)
        
        buffer = 1024
        as_ip = spec['as_ip']
        as_port = spec['as_port']
        message = "TYPE=A" + "|NAME=" + spec['hostname'] + "|VALUE=" + spec['ip'] + "|TTL=10\n"
        bytesToSend = str.encode(message)
        
        print("UDP target IP: %s" % as_ip)
        print("UDP target port: %s" % as_port)
        print("message: %s" % message)
        
        sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
        sock.sendto(bytesToSend, (as_ip, int(as_port)))
        
        print("Expecting response from AS")
        
        msgReceived = sock.recvfrom(buffer)
        sock.close()
        if msgReceived[0].decode("utf-8") == "good":
            return "Registration is successful", 201
        else:
            return "DNS service failed", 503
        
    else:
        return "Request was not JSON", 400

@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    number = request.args.get("number", -1, int)
    # if number == None or not isinstance(number, int):
    if number == None or number == -1:
        return  "400 Bad Request", 400
    else:
        return "The Fibonacci number for the seqeunce number " + str(number) + " is: " + str(fibonacci_dp(number))

app.run(host='0.0.0.0',
        port=9090,
        debug=True)


