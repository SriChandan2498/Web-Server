# Note: Server should start interaction with client
import time, socket

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
        # Write you code here to send response to client and recerive response from client
        connection, addr = soc.accept()
        # print()
        print("Received connection from ", addr[0], "(", addr[1], ")\n")
        print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]))
        cMessage = connection.recv(1024)
        cMessage = cMessage.decode()
        # print(cMessage)
        line1 = cMessage.split('\n')[0]
        # print(line1)
        try:
            method, url = line1.split(" ")[0] , line1.split(" ")[1]
            print(method)
            url = url[1:]
            print(url)
        except IndexError as i:
            pass
        # checking for extention
        urlList = url.split(".")

        if(url == "hello.py"):
            connection.send("HTTP/1.1 403 Forbidden\nContent-Type: text/html; charset=UTF-8;\n\n".encode())
            # connection.close()
        elif(urlList[1] == "html"):
            if(urlList[0] == "index"):
                # connection.send("HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8;\n\nWelcome folks!".encode())
                filename='index.html'
                f = open(filename,'rb')
                connection.send("HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8;\n\n".encode())
                l = f.read(1024)
                while (l):
                    connection.send(l)
                    l = f.read(1024)
                f.close()
                # connection.close()
            else:
                connection.send("HTTP/1.1 404 Not Found\nContent-Type: text/html; charset=UTF-8;\n\n".encode())
                # connection.close()
        else:
            connection.send("HTTP/1.1 400 Bad Request\nContent-Type: text/html; charset=UTF-8;\n\n".encode())
        connection.close()
        # != 127.0.0.1/index.html send 400 bad request
        #  search for finding a file in directory
        
startServer()