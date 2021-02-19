# Author: Sri Sai Chandan J,2020501017
# References : Various onine resources and guidance from mentor

import time,socket,os       

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
def sendForbidden(connection):
    connection.send("HTTP/1.1 403 Forbidden\nContent-Type: text/html; charset=UTF-8;\n\n".encode())

# 415 Unsupported Media Type
def sendUnsupportedMediaType(connection):
    connection.send("HTTP/1.1 415 Unsupported Media Type\nContent-Type: text/html; charset=UTF-8;\n\n".encode())

# 501 Not Implemented
def sendUnimplementedMethod(connection):
    connection.send("HTTP/1.1 501 Not Implemented\nContent-Type: text/html; charset=UTF-8;\n\n".encode())


# get method and url
def getMethodandUrl(cmessage):
    line1 = cmessage.split('\n')[0]
    # print(line1)
    try:
        return (line1.split(" ")[0] , line1.split(" ")[1][1:])
    except IndexError as i:
        return (line1,"")

# sending file
def sendFile(filename,connection):
    f = open(filename,'rb')
    l = f.read()
    connection.send(l)
    f.close()

# sending response for request
def urlResponse(url,method,connection):
    badRequest = False

    # response for forbidden file = "admin.csv"
    if(url == "admin.csv"):
            sendForbidden(connection)
            return

    # response for unimplemented methods
    if( method != "GET" and method != "HEAD"):
        badRequest = True
        sendUnimplementedMethod(connection)
        return
    
    if(not badRequest):
        # response for unsupported media
        if(url == "favicon.ico"):
            sendUnsupportedMediaType(connection)
            return
        else:
            if(url == "" or url == "index.html"):
                url ="."
            if(os.path.isdir(url)):
                sendOK(connection)
                loadDirectory(url,connection)
                return
            
            elif(os.path.isfile(url)):
                sendFile(root+"\\"+url,connection)
                return
            else:
                sendFOF(connection)
                return 
    else:
        sendBadRequest(connection)
        return

def loadDirectory(url,connection):
    parent = url.split("/")[-2:-1]
    if(len(parent)>0):
        parent=parent[0]
    else:
        parent = "../"
    html = f'''
            <html>
            <head>
            <title>Index of </title>
            </head>
            <body>
            <h1>Index of /{url}</h1>
            <table>
            <th>Files and Directories</th>
            <tr><td><a href='./{parent}'>..</a></td></tr>
            '''      
            
    for filename in os.listdir(url):
        html += "<tr><td><a href='/"+url+"/"+filename+"'>"+filename+"</a></td></tr>"
    html += '</table></body></html>'
    connection.send(html.encode())

def createSocket(IP,port):
    print('Setup Server...')
    time.sleep(1)
    # Socket Creation
    soc = socket.socket()
    # Get Host Name
    host_name = socket.gethostname()
    # Get Host IP Address
    ip = socket.gethostbyname(host_name)
    print(host_name, '({})'.format(ip))
    # Binding IP Address and Port together
    soc.bind((IP,port))
    return soc

def startServer(soc):
    soc.listen(1) 
    print('Waiting for incoming connections...')
    respondToClients(soc)

def respondToClients(soc):
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
        urlResponse(url,method,connection)
        connection.close()

    
root = "C:\\Users\\Chandan Zna\\Documents\\MSIT 2020\\MSIT 1st year\\FCN\\Web Server"
soc = createSocket("",80)
startServer(soc)
