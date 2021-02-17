# Note: Server should start interaction with client
# != 127.0.0.1/index.html send 400 bad request
#  search for finding a file in directory
        
import time, socket

# sending index.html file
def sendDefaultFile(connection):
    f = open('index.html','rb')
    l = f.read(1024)
    while (l):
        connection.send(l)
        l = f.read(1024)
    f.close()
    
# 200 OK
def sendOK(connection):
    connection.send("HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8;\n\n".encode())

# 404 file not found
def sendFOF(connection):
    connection.send("HTTP/1.1 404 Not Found\nContent-Type: text/html; charset=UTF-8;\n\n".encode())

# 400 Bad Request
def sendBadRequest(connection):
    connection.send("HTTP/1.1 400 Bad Request\nContent-Type: text/html; charset=UTF-8;\n\n".encode())

# 403 Access Denied
def SendForbidden(connection):
    connection.send("HTTP/1.1 403 Forbidden\nContent-Type: text/html; charset=UTF-8;\n\n".encode())

# get method and url
def getMethodandUrl(cmessage):
    line1 = cmessage.split('\n')[0]
    # print(line1)
    try:
        return (line1.split(" ")[0] , line1.split(" ")[1][1:])
    except IndexError as i:
        pass

def startServer():
    print('Setup Server...')
    time.sleep(1)
    # Socket Creation
    soc = socket.socket()
    # Get Host Name
    host_name = socket.gethostname()
    # Get Host IP Address
    ip = socket.gethostbyname(host_name)
    # Port NO 80 for http requests
    port = 80
    # Binding IP Address and Port together
    soc.bind(("", port))
    print(host_name, '({})'.format(ip))
    # Listening for CLient to connect
    soc.listen(1) 
    print('Waiting for incoming connections...')

    while True:
        # accepting connections from clients
        connection, addr = soc.accept()
        print("Received connection from ", addr[0], "(", addr[1], ")\n")
        print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]))
        cMessage = connection.recv(1024)
        cMessage = cMessage.decode()
        # print(cMessage)
        method, url = getMethodandUrl(cMessage)
        print(method)
        print(url)

        # checking for extention
        urlList = url.split(".")

        # response for forbidden file = "hello.py"
        if(url == "hello.py"):
            SendForbidden(connection)

        # response for default page
        elif(url == ""):
            sendDefaultFile(connection)

        # response for index.html page
        elif(urlList[1] == "html"):
            if(urlList[0] == "index"):
                sendOK(connection)
                sendDefaultFile(connection)
            else:
                # response for other html pages
                sendFOF(connection)
        else:
            # response for bad request  
            sendBadRequest(connection)        
        connection.close()

startServer()